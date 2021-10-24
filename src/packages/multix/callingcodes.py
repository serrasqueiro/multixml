#-*- coding: utf-8 -*-
# multix/ callingcodes.py  (c)2021  Henrique Moreira

"""
Phone Calling Codes functions, within 'multixml'
"""

# pylint: disable=missing-function-docstring

#import lxml
from lxml import etree
from waxpage.redit import char_map
from multix.countryascii import ascii_str

PHONE_METADATA = "$MULTI_BASE/aggregates/ggle/libphonenumber/resources/PhoneNumberMetadata.xml"

def fetch_phone_number_metadata(xml_input1, debug=0) -> dict:
    territory = None
    in_file = xml_input1
    root = etree.fromstring(open(in_file, "r", encoding="utf-8").read())
    did = [elem for elem in root]
    for item in did:
        assert item.tag == "territories", f"Unknown item tag: {item.tag}"
        assert not territory
        territory = fish(item, debug=debug)
    return territory

def fish(item, debug=0) -> dict:
    """ Digs into PhoneNumberMetadata XML """
    idx = 0
    last_elem = None
    territory = {
        "code-list": [],
        "name": {},
        "info": {},
    }
    text, twoletter = "", ""
    for elem in item:
        src_line = elem.sourceline
        pre = f"::: line {src_line}, #{idx}:"
        is_comment = elem.tag is etree.Comment
        if is_comment:
            comment = shorter_comment(elem.text)
            if last_elem is None or last_elem.text.strip() == "":
                text = elem.text.strip()
                astr = text.split(" ")[-1]
                if len(astr) >= 4 and astr[0] == "(" and astr[-1] == ")":
                    twoletter = astr[1:-1].strip()
                    name = text[:-len(twoletter)-2].strip()
                    assert len(twoletter) >= 2, f"twoletter too short: '{twoletter}'"
                    territory["code-list"].append(twoletter)
                    assert twoletter not in territory["name"], f"Duplicate territory twoletter: '{twoletter}'"
                    territory["name"][twoletter] = ascii_str(name)
                    territory["info"][twoletter] = []
                else:
                    twoletter = ""
                shown = f"territory:key={twoletter}: {text}" if twoletter else f"territory:?: {comment}"
            else:
                shown = comment
            if debug > 0:
                print(pre, shown)
        else:
            if debug > 0:
                print(pre, elem.tag, elem.attrib, ".")
            if twoletter:
                territory["info"][twoletter].append((elem.tag, elem.attrib, elem))
        idx += 1
        last_elem = elem
    assert text
    return territory

def shorter_comment(astr:str) -> str:
    new = astr.rstrip()
    new = char_map.simpler_ascii(new, 1)
    alist = new.split("\n")
    new = '\\n'.join([lead.strip() for lead in alist])
    return new

# Main script
if __name__ == "__main__":
    print("Please import me.")
