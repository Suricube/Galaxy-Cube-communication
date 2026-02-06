use std::string::ToString;
use std::{collections::HashMap};
use strum_macros::{EnumString, Display};
use serde::{Serialize, Deserialize};
use serde_json::{Value};

pub trait CompCmd {
    fn get(&self)->String;
}

#[derive(EnumString, Display, Debug)]
#[strum(serialize_all = "lowercase")]
pub enum Cmd {
    Config,
    Set
}

impl CompCmd for Cmd {
    fn get(&self)->String {
        self.to_string()
    }
}


#[derive(Serialize, Deserialize, Debug)]
pub struct GenericMsg {
    cmd: String,
    #[serde(default)]
    uuid: Option<String>,
    #[serde(flatten)]
    properties: HashMap<String, Value>,
    #[serde(default)]
    meta: Option<HashMap<String, Value>>,
    #[serde(default)]
    reply: Option<HashMap<String, Value>>,
}

pub struct Payload {
    cmd: String,
    uuid: Option<String>,
    props: String,
    meta: Option<String>,
    reply: Option<String>,
}

impl Payload {
    pub fn set_cmd<T: CompCmd>(cmd: T) -> Self{
        Payload{cmd: cmd.get(),uuid: None, props:"{}".to_string(),meta: None, reply: None}
    }
    pub fn from_json(msg: String) -> Result<Self, serde_json::Error>{
        let gmsg: GenericMsg = serde_json::from_str(&msg)?;
        let props = serde_json::to_string(&gmsg.properties["properties"]).unwrap();
        let mut meta = None;
        match gmsg.meta {
            Some(m) => meta = Some(serde_json::to_string(&m).unwrap()),
            None => (),
        }
        let mut reply = None;
        match gmsg.reply {
            Some(r) => reply = Some(serde_json::to_string(&r).unwrap()),
            None => (),
        }
        Ok(Payload{cmd: gmsg.cmd, uuid: gmsg.uuid, props: props, meta: meta, reply: reply})
    }
    pub fn set_uuid(mut self, uuid: String) -> Payload{
        self.uuid = Some(uuid);
        self        
    }
    pub fn set_meta(mut self, meta: String) -> Payload{
        self.meta = Some(meta);
        self        
    }
    pub fn set_props(mut self, props: String) -> Payload{
        self.props = props;
        self        
    }
    pub fn to_msg(self)-> String {
        let mut s = format!("{{\"cmd\":\"{}\"",self.cmd);
        match self.uuid {
            Some(uuid) => s.push_str(format!(",\"uuid\":\"{}\"", uuid).as_str()),
            None => (),
        }
        s.push_str(format!(",\"properties\":{}",self.props).as_str());
        match self.meta {
            Some(meta) => s.push_str(format!(",\"meta\":{}", meta).as_str()),
            None => (),
        }
        match self.reply {
            Some(reply) => s.push_str(format!(",\"reply\":{}", reply).as_str()),
            None => (),
        }
        s.push_str("}");
        s
    }
}