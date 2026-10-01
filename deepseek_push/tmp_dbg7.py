import re

txt = open('G070_data/dwarf_tab.tex').read()
pat = re.compile(r"^\s*(\S+(?:\s+\S+)?)\s*&[^&]*&[^&]*&\s*\$?\s*([0-9.]+)", re.M)
for m in pat.finditer(txt):
    if abs(m.start() - 10634) < 200:
        print(m.start(), repr(m.group(1)), m.group(2), 'end=', m.end())
# and what is at the Bootes line?
i = txt.find('o}tes~II')
seg = txt[i-6:i+40]
print('segment:', repr(seg))
m2 = pat.match(txt, i - 4)   # right after the \n
print('match from i-4:', m2.groups() if m2 else None)