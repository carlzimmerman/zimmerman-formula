#!/usr/bin/env python3
"""CFG567: re-parse Genzel+2020 (arXiv:2006.03046) Table D1 from the fetched PDF (pdftotext -layout, git-ignored
under _external_data/cfg567/) and check the G-rows of cfg567_census.csv against it. V_out ~ vc(Re) and
R_out = (Rout/Re) x Re are a PROVISIONAL reading (falling curves would lower V_out). Rows 38-41 did not parse
(page break) and are not in the census."""
import csv, re, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
TXT = os.path.join(HERE, '..', '_external_data', 'cfg567', '2006.03046.txt')
L = open(TXT).read().splitlines()
got = {}
for l in L[2342:2460]:
    t = l.split()
    if len(t) < 20 or not re.fullmatch(r'\d{1,2}', t[0]) or '"' not in l:
        continue
    i = 1
    while i < len(t) and not re.fullmatch(r'-?\d+\.\d+', t[i]):
        i += 1
    f = t[i:]; k = [j for j, x in enumerate(f) if x.endswith('"')][0]
    ro = float(f[k - 3]) if re.search('[A-Za-z]', f[k - 1]) else float(f[k - 2])
    got['G' + t[0]] = (float(f[9]), round(ro * float(f[11]), 2))
rows = {r['cid']: r for r in csv.DictReader(open(os.path.join(HERE, 'cfg567_census.csv'))) if r['cid'].startswith('G')}
bad = [c for c in rows if (float(rows[c]['V_out_kms']), float(rows[c]['R_out_kpc'])) != got.get(c)]
print(f'parsed {len(got)} RC41 rows; census G-rows {len(rows)}; mismatches {bad}')
sys.exit(1 if bad or len(got) != len(rows) else 0)
