mod galaxy;
use galaxy::*;
mod sections;
use sections::*;


fn main() {
    let mut secs = Sections::new(SecOperation::continuos, 100, SecCommands::set);
    let ao = SectionAO::new(0.,1.,2.,3.,4, SecOrder::constant);
    let mut aos = SectionsAO::new("AO0".to_string(), 3);
    aos.append(&ao);
    aos.append(&ao);
    secs.appendao(&aos);
    println!("{}", Galaxy::to_str(&secs));
    
}