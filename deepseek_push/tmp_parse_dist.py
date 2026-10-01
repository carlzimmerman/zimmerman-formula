import re

txt = open('G070_data/dwarf_tab.tex').read()
pat = re.compile(r'^\s+(\S+(?:\s+\S+)?)\s*&[^&]*&[^&]*&\s*\$?\s*([0-9.]+)', re.M)
out = {}
for m in pat.finditer(txt):
    name = ' '.join(m.group(1).split())
    out[name] = float(m.group(2))
for k in ['Sculptor','Fornax','Carina','Sextans','Ursa~Minor','Draco','Leo~I','Leo~II',
          'Reticulum~II','Segue~1','Tucana~II','Bootes~I','Ursa~Major~I','Leo~IV','Hercules',
          'Eridanus~II','Crater~II','Hydrus~I','Willman~1','Aquarius~II','Coma~Berenices',
          'Bootes~II','Canes~Venatici~I','Leo~T','Carina~II','Carina~III','Leo~V',
          'Pegasus~III','Pisces~II','Horologium~I','Ursa~Major~II','Canes~Venatici~II']:
    if k in out:
        print(f'{k:24s} {out[k]:8.1f} kpc')
print('total parsed:', len(out))