import csv, re


def _norm_name(nm):
    return re.sub(r"\{[^{}]*\}", "", nm).replace("~", " ")


pat = re.compile(r"^\s*(\S+(?:\s+\S+)?)\s*&[^&]*&[^&]*&\s*\$?\s*([0-9.]+)", re.M)
out = {}
for m in pat.finditer(open('G070_data/dwarf_tab.tex').read()):
    out[_norm_name(m.group(1))] = float(m.group(2))
print('n_dist:', len(out))
print('Boötes-ish keys:', [k for k in out if 'oot' in k or 'Venatici II' in k])
missing = []
for r in csv.DictReader(open('G070_dsph_compendium.csv')):
    if not r['name'].strip():
        continue
    if _norm_name(r['name']) not in out:
        missing.append(r['name'])
print('MISSING:', missing)