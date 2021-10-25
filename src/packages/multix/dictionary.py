#-*- coding: iso-8859-1 -*-
# multix/ dictionary.py  (c)2021  Henrique Moreira

""" Dictionary string-ify
"""

# pylint: disable=missing-function-docstring

IGNORE_CASE = True

def stringify(item, level=0, opts=None) -> str:
    """ Dumps as string """
    if isinstance(item, str):
        return str_string(item, level, opts)
    if isinstance(item, dict):
        return dictionary_string(item, level, opts)
    if isinstance(item, (list,)):
        return list_string(item, level, opts)
    return str(item)

def str_string(item, level=0, opts=None) -> str:
    res = f'"{item}"'
    return res

def dictionary_string(item:dict, level=0, opts=None) -> str:
    """ Returns a string equivalent for dictionary """
    res = ""
    idx, n_elem = 0, len(item)
    criteria = str.casefold if IGNORE_CASE else str
    if level:
        res = "{"
    for key in sorted(item, key=criteria):
        idx += 1
        entry = item[key]
        shown = stringify(entry, level+1, opts)
        inter = "\n" if level <= 0 else " "
        post = "\n" if level <= 0 else ", "
        if idx >= n_elem and post[0] >= " ":
            post = ""
        quote_key = "'"
        this = f"{quote_key}{key}{quote_key}:{inter}{shown}{post}"
        res += this
    if level:
        res += "}"
    return res

def list_string(item:list, level=0, opts=None) -> str:
    """ Returns a string equivalent for dictionary """
    res = " " * level * 2
    res += "["
    idx, n_elem = 0, len(item)
    for entry in item:
        idx += 1
        shown = stringify(entry, level+1, opts)
        res += shown
        if idx < n_elem:
            res += ", "
    post = "\n" if level <= 0 else ""
    res += "]" + post
    return res

if __name__ == "__main__":
    print("Please import me.")
