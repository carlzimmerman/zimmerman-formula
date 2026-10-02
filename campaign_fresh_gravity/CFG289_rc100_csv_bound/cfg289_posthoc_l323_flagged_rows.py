#!/usr/bin/env python3
"""CFG289 POST-HOC (labelled; written after the classification, at the owner's question "are we sure RC100 did it right?"):
is L323's flip on the corrected table carried by RC100's own problem rows?

CFG287 flagged, from the paper's own equations: rows 67 and 83 give V_rot(R_e)^2 < 0 by its eq. 8, and 14 rows have
V_rot(R_e)/sigma0 < 2.3 (its selection cut, if applied at R_e).  This re-runs L323 in the FIX mirror (made by cfg289_rerun.py) on the
corrected table (a) without rows 67/83 and (b) without all 16, and prints L323's S1 (the level tie) and S4 (the trend) rows.
Usage: python3 campaign_fresh_gravity/CFG289_rc100_csv_bound/cfg289_posthoc_l323_flagged_rows.py <scratch_dir>
No verdict of CFG289 depends on it.
"""
import csv, json, os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
zf = os.path.join(os.path.abspath(sys.argv[1]), "FIX", "zf")
CSV = os.path.join(zf, "real_research", "data", "rc100_nestorshachar2023_table3.csv")
L323 = "real_research/dark_sector_2026/L323_rc100_framework_vs_lcdm_stress.py"
RES = os.path.join(zf, "real_research", "dark_sector_2026", "L323_rc100_framework_vs_lcdm_stress_results.json")
EQ8 = {"67", "83"}
CUT = {"41", "43", "44", "47", "60", "61", "66", "68", "70", "75", "84", "88", "98", "99"}
corrected = os.path.join(REPO, "real_research", "data", "rc100_nestorshachar2023_table3_CORRECTED.csv")
rows = list(csv.DictReader(open(corrected, newline="")))
hdr = list(rows[0].keys())
lines = []
P = lambda s: (print(s), lines.append(s))
P("CFG289 POST-HOC: L323 on the corrected RC100 table without RC100's own flagged rows (labelled; no verdict depends on it)")
try:
    for tag, drop in (("all 100 rows", set()), ("without rows 67, 83 (eq. 8)", EQ8), ("without the 16 flagged rows", EQ8 | CUT)):
        with open(CSV, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=hdr, lineterminator="\n")
            w.writeheader()
            w.writerows([r for r in rows if r["idx"] not in drop])
        p = subprocess.run([sys.executable, L323], cwd=zf, capture_output=True, text=True)
        d = json.load(open(RES))
        P(f"\n  {tag} (n = {len(rows) - len(drop)}; L323 rc {p.returncode})")
        for k, v in d["checks"].items() if isinstance(d["checks"], dict) else []:
            if k.startswith(("S1", "S4")):
                P(f"    [{'PASS' if v.get('ok') else 'FAIL'}] {k[:70]} | {v['measured']}")
finally:
    shutil.copyfile(corrected, CSV)       # leave the FIX mirror as the driver made it
open(os.path.join(HERE, "cfg289_posthoc_l323_flagged_rows_POSTHOC.out"), "w").write("\n".join(lines) + "\n")
