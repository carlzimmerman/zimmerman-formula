import csv
import re


def _norm_name(nm):
    return re.sub(r"\{[^{}]*\}", "", nm).replace("~", " ")


pat = re.compile(r"^\s*(\S+(?:\s+\S+)?)\s*&[^&]*&[^&]*&\s*\$\s*([0-9.]+)", re.M)
out = {}
for m in pat.finditer(open('G070_data/dwarf_tab.tex').read()):
    out[_norm_name(m.group(1))] = float(m.group(2))
print('n_dist:', len(out))
for k in sorted(out):
    if 'Boo' in k or 'Venatici' in k:
        print('  KEY:', repr(k), out[k])
missing = [r['name'] for r in csv.DictReader(open('G070_dsph_compendium.csv'))
           if r['name'].strip() and _norm_name(r['name']) not in out]
print('MISSING:', missing)