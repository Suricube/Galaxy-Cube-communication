import random
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe
import json
import time
from typing import Literal

HOSTNAME = "192.168.1.111"
PUB_TOPIC = "hello/suricube/torust"
SUB_TOPIC = "hello/suricube/tomqqtx"


# Print iterations progress
# https://stackoverflow.com/questions/3173320/text-progress-bar-in-terminal-with-block-characters
def printProgressBar(
    iteration,
    total,
    prefix="",
    suffix="",
    decimals=1,
    length=100,
    fill="█",
    printEnd="\r",
):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + "-" * (length - filledLength)
    print(f"\r{prefix} |{bar}| {percent}% {suffix}", end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


def reset_cmd(actor_name: str) -> dict:
    return {
        "actor_name": actor_name,
        "function_name": "reset",
    }


def simple_asg_signal(
    actor_name, start_level: float, height: float, n_sections: int, time_in_us: int
) -> dict:

    section_order = [{"number": 0, "transition": "continous"}] * n_sections
    section_order[0] = {
        "number": 0,
        "transition": "discontinous",
    }  # first section is discontinous - makes sure the ASG starts at the right level

    return {
        "command": "function_component",
        "parameters": [
            {
                "actor_name": actor_name,
                "function_name": "execute_json_command",
                "function_parameters": {
                    "set_voltage_signal": {
                        "sections": [
                            {
                                "duration": {"microseconds": time_in_us / n_sections},
                                "starting_level": start_level,
                                "starting_derivative": 0.0,
                                "ending_level": start_level + height / n_sections,
                                "ending_derivative": 0.0,
                                "interpolation": "linear",
                            }
                        ],
                        "section_order": section_order,
                        "repetitions": "infinite",
                    }
                },
            }
        ],
    }


def set_asg_settings(
    actor_name: str,
    up_shifting: int = 20, 
    down_shifting: int = 20,
    clocks_per_cycle: int = 40,
) -> dict:
    settings = {
        "command": "function_component",
        "parameters": [
            {
                "actor_name": actor_name,
                "function_name": "execute_json_command",
                "function_parameters": {
                    "set_settings": {
                        "up_shifting": up_shifting,
                        "down_shifting": down_shifting,
                        "clocks_per_cycle": clocks_per_cycle,
                        "fpga_clock_freq": 124998749.0,
                        "a": 0.00015,
                        "b": -5.0,
                        "repetitions": "infinite",
                        "trigger_module_selection": 255,
                        "driver_selection": 3,
                        "SLICE_STARTING_BYTE": 0,
                        "ORDER_STARTING_BYTE": 400,
                    }
                },
            }
        ],
    }
    return settings


def raw_signal(
    actor_name, start_level: float, height: float, n_sections: int, time_in_us: int
) -> dict:
    length = int(time_in_us *1_000 / 4 / 8 / n_sections) + 2 
    section_order = [{"number": 0, "transition": "continous"}] * n_sections
    section_order[0] = {    
        "number": 0,
        "transition": "discontinous",
    }  # first section is discontinous - makes sure the ASG starts at the right level
    cmd = {
        "command": "function_component",
        "parameters": [
            {
                "actor_name": actor_name,
                "function_name": "execute_json_command",
                "function_parameters": {
                    "set_analog_signal": {
                        "sections": [
                            {
                                "length": length ,
                                "s0_0": 0,
                                "s1_0": 100,
                                "s2_0": 0,
                                "s3_0": 0,
                                "interpolation": "linear",
                                "shifts": [1, 20, 20],
                            }
                        ],
                        "section_order": section_order,
                        "repetitions": "infinite",
                    }
                },
            }
        ],
    }
    print(cmd)
    return cmd


def set_pulse_forwarder(
    output_pin: str = "pulse_0",
    input_signal_generator_type: Literal["asg", "dsg"] = "asg",
    input_signal_generator_index: int = 0,
) -> dict:
    return {
        "command": "function_component",
        "parameters": [
            {
                "actor_name": output_pin,
                "function_name": "execute_json_command",
                "function_parameters": {
                    "set_settings": {
                        "select_signal_generator": {
                            input_signal_generator_type: input_signal_generator_index
                        },
                        "select_pulse_type": "pulse_at_section",
                        "pulse_divider_value": 0,
                        "pulse_delayer": 0,
                        "pulse_width": 2000,  # 8ns * 1000 = 8us
                        "flags": 0,
                    }
                },
            }
        ],
    }


def set_cmd(mqtt_client: mqtt.Client):
    reset_all_cmd = {"command": "reset_all"}

    wait_for_cmd = {"command": "wait_for", "parameters": 1}  # 10ms

    stop_trigger_cmd = {
        "command": "function_component",
        "parameters": {
            "actor_name": "galaxy_gpio",
            "function_name": "execute_json_command",
            "function_parameters": "stop",
        },
    }

    start_trigger_cmd = {
        "command": "function_component",
        "parameters": {
            "actor_name": "galaxy_gpio",
            "function_name": "execute_json_command",
            "function_parameters": "start",
        },
    }

    # mqtt_client.publish(PUB_TOPIC, json.dumps(reset_all_cmd, indent=4), qos=1)
    mqtt_client.publish(PUB_TOPIC, json.dumps(stop_trigger_cmd, indent=4), qos=1)
    mqtt_client.publish(PUB_TOPIC, json.dumps(set_asg_settings("ASG_0", up_shifting=40, down_shifting=35, clocks_per_cycle=4), indent=4), qos=1)
    mqtt_client.publish(
        PUB_TOPIC,
        json.dumps(raw_signal("ASG_0", 0.0, 1, 800, 40), indent=4),
        qos=1,
    )
    pulse_json = json.dumps(
        set_pulse_forwarder(),
        indent=4,
    )
    #print(pulse_json)
    mqtt_client.publish(PUB_TOPIC, pulse_json, qos=1)

    mqtt_client.publish(PUB_TOPIC, json.dumps(wait_for_cmd, indent=4), qos=1)
    mqtt_client.publish(PUB_TOPIC, json.dumps(stop_trigger_cmd, indent=4), qos=1)
    mqtt_client.publish(PUB_TOPIC, json.dumps(start_trigger_cmd, indent=4), qos=1)


if __name__ == "__main__":

    # To print the responses
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    def on_message_print(client, userdata, message):
        userdata["n_responses"] += 1
        print(
            "%d \t [%s] >> %s"
            % (userdata["n_responses"], message.topic, message.payload.decode("utf-8"))
        )

    mqttc.on_message = on_message_print
    mqttc.user_data_set({"n_responses": 0})
    mqttc.connect(HOSTNAME, 1883, 60)
    mqttc.subscribe(SUB_TOPIC, qos=1)
    mqttc.loop_start()

    set_cmd(mqttc)
    time.sleep(2)

    mqttc.loop_stop()
    user_data = mqttc.user_data_get()
