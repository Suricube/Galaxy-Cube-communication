use std::{vec, collections::HashMap};
use std::str::FromStr;
use serde::{Deserialize, Serialize};
use serde_json::{Error, Value};
use strum_macros::{EnumString, Display};

pub mod dosections;
use dosections::*;
pub mod aosections;
use aosections::*;


#[derive(EnumString, Display, Debug, PartialEq,)]
#[strum(serialize_all = "lowercase")]
pub enum SecCmd {
    Config,
    Set
}

#[derive(Serialize, Deserialize)]
pub struct GenericMsg {
    cmd: String,
    #[serde(default)]
    uuid: Option<String>,
    #[serde(flatten)]
    properties: HashMap<String, Value>,
    #[serde(default)]
    meta: Option<HashMap<String, Value>>,
}


pub trait SectionType {
    fn to_msg(&self)->Result<String, serde_json::Error>;
    fn parse(msg: String)->Result<Self, serde_json::Error> where Self: Sized;
}

impl SectionType for SectionDO {
    fn to_msg(&self)->Result<String, serde_json::Error> {
        Ok("sss".to_string())
    }
    fn parse(msg: String)-> Result<Self, serde_json::Error> {
        Ok(SectionDO::default())
    }
}

impl SectionType for SectionAO {
    fn to_msg(&self)->Result<String, serde_json::Error> {
        Ok("sss".to_string())
    }
    fn parse(msg: String)-> Result<Self, serde_json::Error> {
        let s: SectionAO = serde_json::from_str(&msg).unwrap();
        Ok(s)
    }
}

pub struct Sections<T: SectionType + serde::Serialize + Clone + Copy + Default> {
    name: String,
    port: u32,
    sections: Option<Vec<T>>
}

impl<T: SectionType + serde::Serialize + Clone + Copy + Default> Sections<T>{
    pub fn new(name: String, port: u32) -> Self{
        Self{
            name, port, sections: None,
        }
    }
    pub fn append(&mut self, s: T){
        match &self.sections {
            Some(s) => (),
            None => self.sections = Some(vec![s.clone()]),
        }
    }
    pub fn delete(&mut self){
        self.sections = None;
    }
    pub fn to_json(&mut self) -> Result<String, serde_json::Error>{
        let mut msg = String::new();
        match &self.sections {
            Some(s) =>   {
                for v in s {
                    msg.push_str(serde_json::to_string(&v).unwrap().as_str());
                }
            },
            None => msg ="{}".to_string(),
        }
        Ok(msg)
    }
    pub fn from_json(msg: String) -> Result<Self, serde_json::Error>{
        let v: GenericMsg = serde_json::from_str(&msg)?;
        let props = serde_json::to_string(&v.properties["properties"]).unwrap();
        let cmd = v.cmd;
        let cmd = SecCmd::from_str(&cmd).unwrap();
        let uuid = v.uuid;
        match cmd {
            SecCmd::Config => (),
            SecCmd::Set => {
                let s = T::parse(props);
                return Ok(Self{name: "name".to_string(), port: 0u32, sections: Some(vec![s.unwrap()])})
            },
        }
        Ok(Self{name: "name".to_string(), port: 0u32, sections: Some(vec![])})
    }
}















/* 
impl Pyload for Sections{
    fn payload(&self) -> String{
    let mut jsonstr:String  = String::new();
        match self.cmd {
            SecCommands::none => {
                jsonstr = format!("{{\"cmd\":\"{}\"}}  ", self.cmd)             
            },
            SecCommands::set => {
                let mut secstr:String  = String::new();
                for s in &self.secsao{
                    secstr.push_str(&s.to_json().unwrap());
                    secstr.push(',');
                }       
                jsonstr = format!("{{\"cmd\":\"{}\"}}", self.cmd.to_str());
                jsonstr = serde_json::to_string(&self).unwrap();              
            },
            SecCommands::start => {
                jsonstr = format!("{{\"cmd\":\"{}\"}}", self.cmd.to_str()) 
            },
            SecCommands::stop => {
                jsonstr = format!("{{\"cmd\":\"{}\"}}", self.cmd.to_str()) 
            }     
        }
        println!("{}",jsonstr);
        //let re:String= serde_json::from_str(&jsonstr).unwrap();
        jsonstr
    }
}

impl Name for Sections{
    fn name(&self) -> String{
        "sections".to_string()
    }
}
 impl Device for Sections{
    fn device(&self) -> DeviceTypes {
        DeviceTypes::Device
    }
}

// section types
#[derive(Debug, Serialize, Deserialize)]
enum SecType {
    analog,
    digital,
}
impl SecType {
    pub fn as_str(&self) -> &'static str {
        match self {
            SecType::analog => "analog",
            SecType::digital => "digital",
        }
    }
}



#[derive(Debug, Serialize, Deserialize)]
pub enum SecOperation{
    finite,
    continuos,
}
impl SecOperation{
    pub fn as_str(&self) -> &'static str {
        match self {
            &SecOperation::finite => "finite",
            &SecOperation::continuos => "continuos",
        }
    }
    
}

#[derive(Debug, Serialize, Deserialize, strum_macros::Display)]
pub enum SecCommands{
    none,
    set,
    start,
    stop,
}

impl SecCommands{
    pub fn to_str(&self) -> &'static str {
        match self {
            &SecCommands::none => "none",
            &SecCommands::set => "set",
            &SecCommands::start => "start",
            &SecCommands::stop => "stop",

        }
    }
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Sections{
    operations: SecOperation,
    samples: i32,
    cmd: SecCommands,
}
  
impl Sections {
    pub fn new(op: SecOperation, samples: i32, cmd: SecCommands) -> Sections{
        Sections { operations:op, samples: samples, cmd}
    }
    pub fn to_payload(&self, cmd: SecCommands)->Result<String, serde_json::Error>{
        let mut jsonstr:String  = String::new();
        let mut secstr:String  = String::new();

        match cmd {
            SecCommands::none => {
                jsonstr = format!("{{\"cmd\":\"{}\"}}  ", cmd.to_str())             
            },
            SecCommands::set => {
//                for s in &self.secsao{
//                    secstr.push_str(&s.to_json().unwrap());
//                    secstr.push(',');
//                }       
                jsonstr = format!("{{\"cmd\":\"{}\"}}", cmd.to_str())                
            },
            SecCommands::start => {
                jsonstr = format!("{{\"cmd\":\"{}\"}}", cmd.to_str()) 
            },
            SecCommands::stop => {
                jsonstr = format!("{{\"cmd\":\"{}\"}}", cmd.to_str()) 
            }     
        }
        Ok(jsonstr)
    }
    pub fn to_msg(&self, cmd: SecCommands) -> String{
        format!("{{\"type\":\"{}\",\"name\":\"{}\",\"payload\":{}}}", self.device(), self.name(), self.to_payload(cmd).unwrap()) 
    }
}

    */