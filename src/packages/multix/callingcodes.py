#-*- coding: utf-8 -*-
# callingcodes.py  (c)2021  Henrique Moreira

"""
Phone Calling Codes, within 'multixml'
"""

# pylint: disable=missing-function-docstring

import sys
import lxml
from lxml import etree

def main():
    main_test("reader", sys.argv[1:])

def main_test(*args):
    what = args[0]
    params = args[1]
    if len(params) != 1:
        return None
    xml_input1 = params[0]
    print("# Reading xml_input1:", xml_input1, "; action:", what)
    return fetch_phone_number_metadata(xml_input1)


def fetch_phone_number_metadata(xml_input1):
    in_file = xml_input1
    root = etree.fromstring(open(in_file, "r", encoding="utf-8").read())
    did = [elem for elem in root]
    for item in did:
        assert item.tag == "territories", f"Unknown item tag: {item.tag}"
        fish(item)
    return 0

def fish(item):
    idx = 0
    text = ""
    for elem in item:
        ### TODO
        is_comment = elem.tag is etree.Comment
        if is_comment:
            
        print(f"::: #{idx}:", elem.tag, elem.attrib, ".")
        print("TEXT:", elem.text)
        print()
        idx += 1
    return True


# Main script
if __name__ == "__main__":
    print("Please import me.")
    main()
