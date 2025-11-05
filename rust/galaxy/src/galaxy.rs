use serde::{de::value::Error, Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
#[derive(strum_macros::Display)]
pub enum  DeviceTypes{
    System,
    Device,
}
#[derive(Debug, Serialize, Deserialize)]  
pub struct Galaxy{
    device: DeviceTypes,
    name: String,
    payload: serde_json::Value,
}

impl Galaxy{
    pub fn new(devtype: DeviceTypes, name: String)-> Self{
        Galaxy { device: devtype, name: name, payload: serde_json::Value::Null}
    }
    pub fn to_json(&mut self, payload: serde_json::Value) -> Result<String, serde_json::Error>{
        self.payload = payload;
        serde_json::to_string(self)
    }
    pub fn to_str<T: Payload + Name + Device> (device: &T) -> String{
        format!("{}, {}, {}",device.payload(), device.name(), device.device().to_string().to_lowercase())
    }
}
pub trait Device{
    fn device(&self) -> DeviceTypes;
}
pub trait Name{
    fn name(&self) -> String;
}

pub trait Payload{
    fn payload(&self) -> String;
}


