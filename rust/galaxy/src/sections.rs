use std::{clone, vec};
use serde::{de::value::Error, Deserialize, Serialize};
use crate::galaxy::*;


impl Payload for Sections{
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

// order of analog signal
#[derive(strum_macros::Display)]
#[derive(Debug, Serialize, Deserialize, Clone)]
pub enum SecOrder {
    constant,
    linear,
    square,
    cubic,
} 



//overwrite options for analog signal
#[derive(Debug, Serialize, Deserialize)]
enum SecSet{
    KeepNone  = 0,
    KeepValue  = 1,
    KeepSlop   = 2,
}
#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct SectionAO{
    yl: f32,
    yr: f32,
    dl: f32,
    dr: f32,
    n: i32,
    s: SecOrder,
}

impl SectionAO{
    pub fn new(yl: f32, yr:f32,dl: f32, dr: f32, n: i32, s: SecOrder) -> Self{
        Self { yl, yr, dl, dr, n , s}
    }
    pub fn to_json(&self) -> Result<String, serde_json::Error>{
        serde_json::to_string(self)
    }
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct SectionsAO{
    name: String,
    port: i32,
    secs: Vec<SectionAO>,
}

impl SectionsAO{
    pub fn new(name: String, port: i32) -> Self{
        Self{
            name, port, secs: Vec::new(),
        }
    }
    pub fn append(&mut self, s: &SectionAO){
        self.secs.push(s.clone());
    }
    pub fn delete(&mut self){
        self.secs.clear();
    }
    pub fn to_json(&self) -> Result<String, serde_json::Error>{
        serde_json::to_string(self)
    }
}

#[derive(Debug, Serialize, Deserialize)]
struct SectionDO{
    v: bool,
    n: i32,
}

impl SectionDO{
    fn new(&mut self, value: bool, n: i32){
        self.v = value;
        self.n = n;
    }
    fn to_json(&self) -> Result<String, serde_json::Error>{
        serde_json::to_string(self)
    }
}

#[derive(Debug, Serialize, Deserialize)]
struct SectionsDO{
    name: String,
    port: i32,
    secs: Vec<SectionDO>,
}

impl SectionsDO {
    fn new(&mut self, name: String, port: i32, secs: Vec<SectionDO>){
        self.name = name;
        self. port = port;
        self.secs = secs;
    }
    fn append(&mut self, s: SectionDO){
        self.secs.push(s);
    }
    fn delete(&mut self){
        self.secs.clear();

    }
    fn to_json(&self) -> Result<String, serde_json::Error>{
        serde_json::to_string(&self)
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
    secsao: Vec<SectionsAO>,
    secsdo: Vec<SectionsDO>,
    cmd: SecCommands,
}
  
impl Sections {
    pub fn new(op: SecOperation, samples: i32, cmd: SecCommands) -> Sections{
        Sections { operations:op, samples: samples, secsao: vec![], secsdo: vec![], cmd}
    }
    pub fn appendao(&mut self, s: &SectionsAO){
        self.secsao.push(s.clone());
    }
    pub fn appenddo(&mut self, s: SectionsDO){
        self.secsdo.push(s);
    }
    pub fn deleteao(&mut self){
        self.secsao.clear();
    }
    pub fn deletedo(&mut self){
        self.secsdo.clear();
    }
    pub fn to_payload(&self, cmd: SecCommands)->Result<String, serde_json::Error>{
        let mut jsonstr:String  = String::new();
        let mut secstr:String  = String::new();

        match cmd {
            SecCommands::none => {
                jsonstr = format!("{{\"cmd\":\"{}\"}}  ", cmd.to_str())             
            },
            SecCommands::set => {
                for s in &self.secsao{
                    secstr.push_str(&s.to_json().unwrap());
                    secstr.push(',');
                }       
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