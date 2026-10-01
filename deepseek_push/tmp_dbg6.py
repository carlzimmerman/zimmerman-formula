import re

txt = open('G070_data/dwarf_tab.tex').read()
print('has CRLF:', '\r\n' in txt, '| lone CR:', '\r' in txt.replace('\r\n', ''))
pat = re.compile(r"^\s*(\S+(?:\s+\S+)?)\s*&[^&]*&[^&]*&\s*\$?\s*([0-9.]+)", re.M)
names = [m.group(1) for m in pat.finditer(txt)]
print('n_matches:', len(names))
print('any Bootes:', [n for n in names if 'oo' in n])
# manually test the exact line with finditer offsets
it = list(pat.finditer(txt))
print('first 5:', [m.group(1) for m in it[:5]])
# find the offset of the Bootes line within txt
i = txt.find('o}tes~II')
print('offset of Bootes II:', i)
print('line around:', repr(txt[i-30:i+30]))
m = pat.match(txt, i-30)
print('match at offset:', m.group(1) if m else None, m.group(2) if m else None)