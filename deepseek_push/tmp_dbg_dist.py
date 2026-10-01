import csv, re
DIST = {}
txt = open('G070_data/dwarf_tab.tex').read()
pat = re.compile(r"^\s+(\S+(?:\s+\S+)?)\s*&[^&]*&[^&]*&\s*\$?\s*([0-9.]+)", re.M)
for m in pat.finditer(txt):
    name = " ".join(m.group(1).split()).replace("~", " ")
    DIST[name] = float(m.group(2))
names = [r["name"] for r in csv.DictReader(open('G070_dsph_compendium.csv')) if r["name"].strip()]
missing = []
for n in names:
    hit = DIST.get(n) or DIST.get(n.replace(" ", "~"))
    if not hit:
        missing.append(n)
print("compendium objects:", len(names))
print("parsed distances:", len(DIST))
print("MISSING:", missing)
for k in sorted(DIST):
    if 'Draco' in k or 'Bootes' in k or 'Sagittar' in k or 'Tucana' in k or 'Pisces' in k or 'Pegasus' in k or 'Horologium' in k or 'Coma' in k:
        print('  ', repr(k), DIST[k])