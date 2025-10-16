''' galaxy section claas'''
from enum import Enum

# section types
class SecType(str, Enum):
    analog = "analog"
    digital= "digital"

# order of analog signal
class SecOrder(str, Enum):
    constant = 'constant'
    linear   = 'linear'
    square   = 'square'
    cubic    = 'cubic'

# overwrite options for analog signal
class SecSet(Enum):
    keepnone   = 0
    keepvalue  = 1
    keepslop   = 2

class SectionAO:
    def __init__(self,yl: float,yr:float,dl:float,dr:float,n: int,s: SecOrder):
        self.yl = yl
        self.yr = yr
        self.dl = dl
        self.dr = dr
        self.n  = n
        self.order = s
    
    def to_json(self):
        return "{\"yl\":"+str(self.yl)+",\"yr\":"+str(self.yr)+",\"dl\":"+str(self.dl)+",\"dr\":"+str(self.dr)+",\"n\":"+str(self.n)+",\"order\":\""+self.order+"\"}"

class SectionsAO:
    def __init__(self,name: str,port: int):
        self.name = name
        self.port = port
        self.secs: list[SectionAO] = []

    def append(self,s: SectionAO):
        self.secs.append(s)

    def delete(self):
        self.secs = []

    def to_json(self):
        secstr =""
        for s in self.secs:
            secstr += s.to_json() + ","
        if secstr[-1] == ",":
            secstr = secstr[:-1]
        jsonstr = "{\"type\":\"analog\",\"name\":\""+self.name+"\",\"port\":"+str(self.port)+",\"secs:\":["+secstr+"]}"
        return jsonstr


class SectionDO:
    def __init__(self, value: bool,n: int):
        self.v = value
        self.n = n
    
    def to_json(self):
        return "{\"value\":"+str(self.v)+",\"n\":"+str(self.n)+"}"

class SectionsDO:
    def __init__(self,name: str,port: int):
        self.name = name
        self.port = port
        self.secs: list[SectionDO] = []

    def append(self,s: SectionDO):
        self.secs.append(s)

    def delete(self):
        self.secs = []

    def to_json(self):
        secstr =""
        for s in self.secs:
            secstr += s.to_json() + ","
        if secstr[-1] == ",":
            secstr = secstr[:-1]
        jsonstr = "{\"type\":\"digital\",\"name\":\""+self.name+"\",\"port\":"+str(self.port)+",\"secs:\":["+secstr+"]}"
        return jsonstr

# section types
class SecOperation(str, Enum):
    finite     = "finite"
    continuous = "continuous"

# section types
class SecCommands(str, Enum):
    none  = "none"
    set   = "set"
    start = "start"
    stop  = "stop"

class Sections:
    def __init__(self,name: str,op: SecOperation, samples: int):
        self.operation = op
        self.samples = samples
        self.secsao: list[SectionsAO] = []
        self.secsdo: list[SectionsDO] = []

    def appendao(self,s: SectionsAO):
        self.secsao.append(s)

    def appenddo(self,s: SectionsDO):
        self.secsdo.append(s)

    def deleteao(self):
        self.secsao = []

    def deletedo(self):
        self.secsdo = []

    def to_payload(self, cmd: SecCommands):
        jsonstr = ""
        match cmd:
            case SecCommands.set:
                secstr =""
                for s in self.secsao:
                    secstr += s.to_json() + ","
                for s in self.secsdo:
                    secstr += s.to_json() + ","
                if secstr[-1] == ",":
                    secstr = secstr[:-1]
                jsonstr = "{\"cmd\":\"" + cmd + "\",\"operation\":\"" + self.operation + "\",\"samples\":\"" + str(self.samples) + "\",\"secs\":[" + secstr + "]}" 
            case SecCommands.start:
                jsonstr = "{\"cmd\":\"" + SecCommands.start + "\"}"               
            case SecCommands.stop:
                jsonstr = "{\"cmd\":\"" + SecCommands.stop + "\"}"               
            case _:
                jsonstr = "{\"cmd\":\"" + SecCommands.none + "\"}"               
        return jsonstr
    