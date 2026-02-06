use serde::{Deserialize, Serialize};

// order of analog signal
#[derive(strum_macros::Display)]
#[derive(Debug, Serialize, Deserialize, Clone, Copy, Default)]
pub enum SecOrder {
    #[default]
    Constant,
    Linear,
    Square,
    Cubic,
} 

//overwrite options for analog signal
#[derive(Debug, Serialize, Deserialize)]
enum _SecSet{
    KeepNone  = 0,
    KeepValue  = 1,
    KeepSlop   = 2,
}
#[derive(Debug, Serialize, Deserialize, Clone, Copy, Default)]
pub struct SectionAO{
    yl: f32,
    yr: f32,
    dl: f32,
    dr: f32,
    n: i32,
    order: SecOrder,
}

impl SectionAO{
    pub fn new(yl: f32, yr:f32,dl: f32, dr: f32, n: i32, order: SecOrder) -> Self{
        Self {yl, yr, dl, dr, n , order}
    }
    pub fn to_json(&self) -> Result<String, serde_json::Error>{
        serde_json::to_string(self)
    }
}
