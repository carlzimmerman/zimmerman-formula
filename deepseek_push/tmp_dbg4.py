import re

lines = open('G070_data/dwarf_tab.tex').read().splitlines()
pat = re.compile(r"^\s*(\S+(?:\s+\S+)?)\s*&[^&]*&[^&]*&\s*\$?\s*([0-9.]+)")
for i in (60, 61, 62):
    l = lines[i]
    # show exact escape bytes around the name
    j = l.find('Bo')
    print(i, repr(l[:l.find('&')]))
    m = pat.match(l)
    print('   match:', m.groups() if m else None)