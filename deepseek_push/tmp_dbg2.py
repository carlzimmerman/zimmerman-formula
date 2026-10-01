import re
txt = open('G070_data/dwarf_tab.tex').read()
pat = re.compile(r"^\s+(\S+(?:\s+\S+)?)\s*&[^&]*&[^&]*&\s*\$?\s*([0-9.]+)", re.M)
names = sorted(" ".join(m.group(1).split()).replace("~", " ") for m in pat.finditer(txt))
print(len(names))
for n in names:
    print(repr(n))
print('---- raw lines containing Bootes-ish:')
for i, l in enumerate(txt.splitlines()):
    if 'oot' in l or 'Segue' in l.lower() or 'Willman' in l:
        print(i, l[:90])