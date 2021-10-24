#-*- coding: iso-8859-1 -*-
# multix/ callingcodes.test.py  (c)2021  Henrique Moreira

""" converts names to simpler ASCII

Dedicated to country names and such.

See also:
	[1] two letter country: ISO 3166-1 alpha-2
"""

from  waxpage.redit import char_map


def ascii_str(astr:str) -> str:
    there = astr
    there = there.replace("\xc5", "A")	# Aland islands (first 'A' is Angstrom, 0xC5)
    there = there.replace(chr(8217), "'")	# Cote d'Ivoire (right angle), 0x2019
    return char_map.simpler_ascii(there)

if __name__ == "__main__":
    print("Please import me.")
