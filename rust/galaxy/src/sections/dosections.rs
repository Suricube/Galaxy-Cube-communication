use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize, Copy, Clone, Default)]
pub struct SectionDO{
    v: bool,
    n: u32,
}

impl SectionDO{
    pub fn new(value: bool, n: u32) -> Self{
        Self {v: value, n: n}
    }
}
