#-*- coding: iso-8859-1 -*-
# multix/ callingjson.py  (c)2021  Henrique Moreira

""" Simple json conversion
"""

# pylint: disable=missing-function-docstring

import json

def json_str(alist:list) -> str:
    """ Converts list to JSON """
    assert isinstance(alist, list)
    astr = json.dumps(alist, indent=4, sort_keys=True)
    return astr

if __name__ == "__main__":
    print("Please import me.")
