#-*- coding: utf-8 -*-
# callingcodes.test.py  (c)2021  Henrique Moreira

"""
Phone Calling Codes, within 'multixml'
"""

# pylint: disable=missing-function-docstring

import sys
import os
import multix.callingcodes as callingcodes

def main():
    code = main_test("reader", sys.argv[1:])
    assert code == 0, "Bogus code: {}".format(code if code else "NONE!")

def main_test(*args):
    what = args[0]
    param = args[1]
    if len(param) != 1:
        return None
    return main_run(what, param)

def main_run(what:str, param:list, debug=1):
    default_xml_input1 = callingcodes.PHONE_METADATA
    fname = param[0]
    if fname in (".",):
        xml_input1 = default_xml_input1.replace("$MULTI_BASE/", env_var("MULTI_BASE") + "/")
    else:
        xml_input1 = fname
    print("# Reading xml_input1:", xml_input1, "; action:", what)
    territory = callingcodes.fetch_phone_number_metadata(xml_input1)
    assert isinstance(territory, dict)
    if debug > 0:
        for ccode in territory["code-list"]:
            name, item = territory["name"][ccode], territory["info"][ccode]
            print("#", ccode, name)
    code = len(territory) > 100
    assert code == 0
    return code

def env_var(avar:str):
    value = os.environ.get(avar)
    assert value is not None, "Please define environment variable: {}".format(avar)
    astr = value
    return astr.replace("\\", "/")

# Main script
if __name__ == "__main__":
    main()
