mod sections;
use sections::*;
use sections::dosections::SectionDO;
use sections::aosections::{SectionAO, SecOrder};
mod component;
use component::*;

#[derive(strum_macros::Display)]
enum SpecCmd {
    SetSection,
}

impl CompCmd for SpecCmd {
    fn get(&self)->String {
        self.to_string()
    }
}

fn main() {
    let mut s: Sections<SectionDO> = Sections::new("nnn".to_string(),0);
    s.append(SectionDO::new(true,10));
    s.append(SectionDO::new(false,10));

    let mut d: Sections<SectionAO> = Sections::new("nnn".to_string(),0);
    d.append(SectionAO::new(0., 0., 1., 1., 10, SecOrder::Square));
    println!("{}",d.to_json().unwrap());

    let mut e: Sections<SectionAO> = Sections::from_json(r#"{"cmd":"set","properties":{"yl":1.0,"yr":0.1,"dl":1.0,"dr":2.0,"n":11,"order":"Square"}}"#.to_string()).unwrap();
    println!("{}",e.to_json().unwrap());

    let pl = Payload::from_json(r#"{"cmd":"set","reply":{"ss":0},"meta":{},"properties":{"yl":1.0,"yr":0.1,"dl":1.0,"dr":2.0,"n":11,"order":"Square"}}"#.to_string()).unwrap();
    println!("{}",pl.to_msg());

    let s = Payload::set_cmd(SpecCmd::SetSection)
        .set_meta("{}".to_string())
        .set_uuid("00.00.00".to_string())
        .set_props("dddd".to_string())
        .to_msg();
    println!("{}",s);
    
}