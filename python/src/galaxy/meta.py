''' galaxy meta msgs'''

def to_meta(desc: str, version: str)-> dict:
    msg = {
        "desc":desc,
        "vesion":version
    }
    return msg
