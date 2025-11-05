import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time,json

def on_message(client, userdata, msg):
    # on_message is kind of the decorator for client.on_message, which is always waiting for the message sent by the subscribed channels
    #print(msg.topic+" "+str(msg.payload))
    payload = str(msg.payload)[2:-1]
    # in msg.payload, there is additional b' in the start and ' in the end of the string, need to remove them for json.loads to load.
    # the correct output for  print(msg.payload) should be {"msg":"hello"} instead '{"msg":"hello"}'. watch out the quote sign.
    print(payload.strip()) 
    try:
        MsgDict = json.loads(payload.strip())
        #print(MsgDict)
    except:
        print("string format error.")
        pass

def config_trigger_in():
    #for configuring external trigger-in
    TrigInConfig = dict()
    TrigInConfig["external_triggers"] = ["do_nothing","do_pause","do_stop","do_trigger"]
    TrigInConfig["software_trigger"] = False
    TrigInConfig["software_pause"] = False
    TrigInConfig["software_stop"] = True
    
    TrigIn = dict()
    TrigIn["cmd"] = "configure_trigger_lines"
    TrigIn["config"] = TrigInConfig

    return TrigIn

def setTTLSection(polarity:bool,duration):
    # duration: microsecond
    CLOCKTIME = 1/62.5
    tick = duration/CLOCKTIME
    section = dict()
    section["value"] = polarity
    section["duration"] = {"ticks": int(tick)}
    
    return section

def TTL_voltage_command():

    PayloadConfig = dict()
    PayloadConfig["sections"] = [setTTLSection(False,10000),setTTLSection(True,10000)]
    PayloadConfig["section_order"] = getSectionOrder([(0,"discontinous"),(1,"discontinous"),(0,"discontinous"),(1,"discontinous")])

    Payload = dict()
    Payload["cmd"] = "load_digital_sections"
    Payload["config"] = PayloadConfig
    Payload["modules"] = [0,1,2]

    TrigSettings = config_trigger_in()

    TTLSettings = dict()
    TTLSettings["type"] = "DSG"
    TTLSettings["name"] = "Name"
    TTLSettings["payload"] = [Payload,TrigSettings]

    TTLSettingsStr = str(TTLSettings)
    TTLSettingsStr = TTLSettingsStr.replace("True","true")
    TTLSettingsStr = TTLSettingsStr.replace("False","false")
    TTLSettingsStr = TTLSettingsStr.replace("\'","\"")

    return TTLSettingsStr 

def setVoltageSection(value,duration):
    Section  = dict()
    Section["duration"] = {"microseconds":duration}
    Section["starting_level"] = value
    Section["starting_derivative"] = 0
    Section["ending_level"] = 0
    Section["ending_derivative"] = 0
    Section["interpolation"] = "constant"

    return Section

def getSectionOrder(config:list):
    # config example: [(0,"discontinous"),(1,"discontinous"),...]
    SectionOrder = list()
    for aSect in config:
        aSectDict = dict()
        aSectDict["number"] = aSect[0]
        aSectDict["transition"] = aSect[1]
        SectionOrder.append(aSectDict)
    
    return SectionOrder

def voltage_value_command(value):
    # counter_type = 0 does nothing, 
    # counter_type = 1 counts the number of sections(e.g. there is 5 sections in the section_order, if count_type = 1 and count_value =3, then it execute 1-3 event in the section_order)  
    # counter_type = 2 counts the number of repetitions(e.g. there is 5 sections in the section_order, if count_type = 2 and count_value =3, then it repeats the whole section_order 3 times)
    # structure of payload: [{"cmd":str,"config":{"sections":[],"section_order":[]},"modules":[]}]

    PayloadConfig = dict()
    PayloadConfig["sections"] = [setVoltageSection(value,25000),setVoltageSection(0,50000)]
    PayloadConfig["section_order"] = getSectionOrder([(0,"discontinous"),(1,"discontinous"),(0,"discontinous"),(1,"discontinous")])

    Payload = dict()
    Payload["cmd"] = "load_voltage_sections"
    Payload["config"] = PayloadConfig
    Payload["modulus"] = [0,1,2]

    TrigSettings = config_trigger_in()

    VoltageSettings = dict()
    VoltageSettings["name"] = "Name"
    VoltageSettings["type"] = "ASG"
    VoltageSettings["payload"] = [Payload,TrigSettings]

    VoltageSettingsStr = str(VoltageSettings)
    VoltageSettingsStr = VoltageSettingsStr.replace("True","true")
    VoltageSettingsStr = VoltageSettingsStr.replace("False","false")
    VoltageSettingsStr = VoltageSettingsStr.replace("\'","\"")

    return VoltageSettingsStr

def decorateDict(dictstr:str):
    for n,a in enumerate(dictstr):
        if a == "," or a == "]" or a == "}" or a == "[" or a == "{":
            dictstr = dictstr[0:n+1]+"\n"+dictstr[n+1:]
    
    return dictstr

def onset_command(status):
    # "cmd": "start", "stop" is for software triggering
    command = \
        """
{
    "type": "ASG",
    "name": "Name", 
    "payload":[{
        "cmd": """ + "\""+ status + "\""+""",
        "modules":[
        0,
        1,
        2
        ]
    }]
}        
        """
    return command

client = mqtt.Client()
#client.username_pw_set(username = "root", password = "root")

# client.connect() connects this PC to the broker with IP:192.168.1.111
# paho can't connect other client device to the broker.
client.connect("192.168.1.111",1883,60)

Topic_ASG = "suricube/galaxy_cube/123/firmware-test"
Topic_Status = "suricube/galaxy_cube/123/pub"
#Old topic :Topic_ASG = "suricube/galaxy_cube/11/analog_signal_generator"
#client.on_message = on_message
#client.subscribe("suricube/galaxy_cube/",0)
#client.publish("suricube/galaxy_cube/","Not cool at all")

##client.publish(Topic_ASG, onset_command("stop"))
client.subscribe(Topic_ASG)
client.subscribe(Topic_Status)
#client.publish(Topic_ASG, config_trigger_in([1,0,0,0]))
#client.publish(Topic_ASG, voltage_value_command(-3))
client.publish(Topic_ASG, TTL_voltage_command())
time.sleep(0.5)
client.publish(Topic_ASG, onset_command("start"))
# The above line is for software triggering. Don't need to run the line for external triggering 
time.sleep(10)
client.publish(Topic_ASG, onset_command("stop"))
#publish.single(Topic_ASG, payload=raw_value_command(30000),  hostname="192.168.1.111", port=1883, protocol=mqtt.MQTTv5, client_id="Python test")
#publish.single(Topic_ASG, payload=onset_command("start"),  hostname="192.168.1.111", port=1883, protocol=mqtt.MQTTv5, client_id="Python test")

client.loop_forever()

# ABOUT ONBOARD CLIENT:
# Onboard client is already connected while setting up the board
# The subscription of the onboard client is also done in the setup.
# Further subscription or connection must be made in Rust or other interface


# Below is what should work.
"""
{
  "name": "Name",
  "type": "ASG",
  "payload": [
    {
      "cmd": "load_voltage_sections",
      "config": {
        "sections": [
          {
            "duration": {
              "microseconds": 25000
            },
            "starting_level": 3,
            "starting_derivative": 0,
            "ending_level": 0,
            "ending_derivative": 0,
            "interpolation": "constant"
          },
          {
            "duration": {
              "microseconds": 50000
            },
            "starting_level": 0,
            "starting_derivative": 0,
            "ending_level": 0,
            "ending_derivative": 0,
            "interpolation": "constant"
          }
        ],
        "section_order": [
          {
            "number": 0,
            "transition": "discontinous"
          },
          {
            "number": 1,
            "transition": "discontinous"
          },
          {
            "number": 0,
            "transition": "discontinous"
          },
          {
            "number": 1,
            "transition": "discontinous"
          }
        ]
      },
      "modules": [
        0,
        1,
        2,
        3
      ]
    },
    {
      "cmd": "configure_trigger_lines",
      "config": {
        "external_triggers": [
          "do_nothing",
          "do_pause",
          "do_stop",
          "do_trigger"
        ],
        "software_trigger": true,
        "software_pause": true,
        "software_stop": true
      }
    },
    {
      "cmd": "stop"
    }
  ]
}
"""