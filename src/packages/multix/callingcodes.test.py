#-*- coding: utf-8 -*-
# multix/ callingcodes.test.py  (c)2021  Henrique Moreira

"""
Phone Calling Codes test, within 'multixml'
"""

# pylint: disable=missing-function-docstring

import sys
import os
import multix.callingcodes as callingcodes
import multix.dictionary as dictionary
from multix.callingjson import json_str

DEBUG = 0

def main():
    code = main_test("reader", sys.argv[1:])
    assert code == 0, "Bogus code: {}".format(code if code else "NONE!")

def main_test(*args):
    """ Main test! """
    debug = DEBUG
    what = args[0]
    param = args[1]
    if len(param) != 1:
        return None
    result = {
        "territory-list": [],
        "code-list": [],
        "info-list": [],
        "main-region-extra": {},
        "json-territory-names": "",
        "json-calling-numbers": "",
    }
    code = dump_calling_codes(what, param, result, debug)
    return code

def dump_calling_codes(what, param, result, debug=0):
    """
    :param what: action, currently unused
    :param param: arguments
    :param result: dictionary
    :param debug: 0
    :return: integer code, 0 is Ok
    """
    code = main_run(what, param, result, debug=debug)
    if debug > 0:
        print("\n" + "RESULT:\n" + dictionary.stringify(result), "<<<")
        print("Territories:", dictionary.stringify(result["code-list"]), "<<<")
    print(result["json-calling-numbers"])
    return code

def main_run(what:str, param:list, result:dict, debug=0):
    """ Main run! """
    default_xml_input1 = callingcodes.PHONE_METADATA
    fname = param[0]
    if fname in (".",):
        xml_input1 = default_xml_input1.replace("$MULTI_BASE/", env_var("MULTI_BASE") + "/")
    else:
        xml_input1 = fname
    print("# Reading xml_input1:", xml_input1, "; action:", what)
    code = parse_phone_metadata((xml_input1,), result, debug=debug)
    return code

def parse_phone_metadata(inputs:tuple, result:dict, debug=0) -> int:
    """ Main parse: Phone Calling Codes XML """
    territories_list = []
    xml_input1 = inputs[0]
    territory = callingcodes.fetch_phone_number_metadata(xml_input1)
    assert isinstance(territory, dict)
    code_list = territory["code-list"]
    for ccode in code_list:
        name = territory["name"][ccode]
        if debug > 0:
            print("#", ccode, name)
        adict = {
            "IdStr": ccode,
            "Name": name,
        }
        territories_list.append(adict)
    code = len(territory) > 100
    assert code == 0
    result["json-territory-names"] = json_str(territories_list)
    result["territory-list"] = territories_list
    result["code-list"] = territory["code-list"]
    # Build information
    infos = {}
    for key in territory["info"]:
        tag, attrib, _ = territory["info"][key][0]
        assert tag == "territory"
        ccode = attrib["countryCode"]
        assert ccode
        assert int(ccode) >= 1, f"Invalid ccode: '{ccode}'"
        item = {
            "Code": attrib["id"],
            "CCode": int(ccode),  # Calling code!
            "MainRegions": None,
        }
        infos[key] = item
    assert not result["info-list"]
    for key in code_list:
        elem = infos[key]
        result["info-list"].append(elem)
        if key in territory["main-region"]:
            main_regions = territory["main-region"][key]
            result["main-region-extra"][key] = main_regions
            infos[key]["Main"] = main_regions
    result["json-calling-numbers"] = json_str(result["info-list"])
    return code

def env_var(avar:str):
    value = os.environ.get(avar)
    assert value is not None, "Please define environment variable: {}".format(avar)
    astr = value
    return astr.replace("\\", "/")

# Main script
if __name__ == "__main__":
    main()
