#!/usr/bin/env python3
"""CFG305 step 3b (a parametrised copy of CFG289's cfg289_supplement.py, plus CFG289's L323 flagged-rows post-hoc; FROZEN_CRITERIA.md,
82dfcc1b3).  Run in the group-O mirrors that cfg305_rerun.py filled (O_ORIG = the CORRECTED table, O_FIX = the PUBLISHED table):

  * CFG90's cfg90.py hard-codes the repository's absolute path, so in both mirrors it read the real repo's original CSV.  As in CFG289,
    a copy with REPO pointed at each mirror is run in both mirrors (the committed script is untouched).  It writes cfg90.out etc. into
    the mirror's CFG90 dir, so cfg305_compare.py's cfg90 entry then compares the mirror-path runs (as in CFG289).
  * CFG52's pooled.py and mock_bias.py (computed from feas.py's per-galaxy output; neither names the CSV).
  * CFG289's post-hoc (cfg289_posthoc_l323_flagged_rows.py), parametrised: L323 on the mode's table without rows {67, 83} and without
    the 16 flagged rows; the flag sets are also re-derived from each table (eq. 8 at R_e: V_c^2 - 3.36 sigma0^2 < 0; V_rot/sigma0 < 2.3).
    The mirror's L323 outputs are saved before and restored byte-for-byte afterwards.
Usage: python3 campaign_fresh_gravity/CFG305_published_tables/cfg305_supplement.py <scratch_dir>
Writes cfg90_mirrorpath_{ORIG,FIX}.out, cfg52_{pooled,mock_bias}_{ORIG,FIX}.out and cfg305_l323_flagged_{ORIG,FIX}.out into this lane.
"""
import csv, json, math, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
scratch = os.path.abspath(sys.argv[1])
TABLE = {"ORIG": os.path.join(REPO, "real_research", "data", "rc100_nestorshachar2023_table3_CORRECTED.csv"),
         "FIX": os.path.join(REPO, "real_research", "data", "rc100_nestorshachar2023_table3_PUBLISHED.csv")}
L323 = "real_research/dark_sector_2026/L323_rc100_framework_vs_lcdm_stress.py"
EQ8 = {"67", "83"}
CUT = {"41", "43", "44", "47", "60", "61", "66", "68", "70", "75", "84", "88", "98", "99"}      # CFG289's post-hoc list (CFG287)


def scrub(t, zf):
    return t.replace(zf, "<mirror>").replace(os.path.dirname(zf), "<base>").replace(scratch, "<scratch>")


for mode in ("ORIG", "FIX"):
    zf = os.path.join(scratch, f"O_{mode}", "zf")
    # ---- CFG90 with the mirror path (kept from cfg289_supplement.py)
    d90 = os.path.join(zf, "campaign_fresh_gravity", "CFG90_a0z_rederivation")
    src = open(os.path.join(d90, "cfg90.py")).read()
    patched, n = re.subn(r'^REPO = ".*"$', f'REPO = "{zf}"', src, count=1, flags=re.M)
    assert n == 1, "cfg90.py REPO line not found"
    open(os.path.join(d90, "cfg90_mirrorpath.py"), "w").write(patched)
    subprocess.run([sys.executable, "cfg90_mirrorpath.py"], cwd=d90, capture_output=True, check=True)
    out = scrub(open(os.path.join(d90, "cfg90.out")).read(), zf)
    open(os.path.join(HERE, f"cfg90_mirrorpath_{mode}.out"), "w").write(out)
    # ---- CFG52 pooled / mock_bias
    d52 = os.path.join(zf, "campaign_fresh_gravity", "CFG52_a0z_feasibility")
    for s in ("pooled.py", "mock_bias.py"):
        p = subprocess.run([sys.executable, s], cwd=d52, capture_output=True, text=True, check=True)
        open(os.path.join(HERE, f"cfg52_{s[:-3]}_{mode}.out"), "w").write(scrub(p.stdout, zf))
    print(f"{mode}: cfg90 (mirror path) and CFG52 pooled/mock_bias written")
    # ---- L323 without RC100's own flagged rows (CFG289's post-hoc, parametrised)
    csv_m = os.path.join(zf, "real_research", "data", "rc100_nestorshachar2023_table3.csv")
    dls = os.path.join(zf, "real_research", "dark_sector_2026")
    keep = {f: open(os.path.join(dls, f), "rb").read() for f in os.listdir(dls)
            if f.startswith("L323_") and os.path.isfile(os.path.join(dls, f)) and not os.path.islink(os.path.join(dls, f))}
    csv_keep = open(csv_m, "rb").read()
    rows = list(csv.DictReader(open(TABLE[mode], newline="")))
    hdr = list(rows[0].keys())
    eq8_re, cut_re = set(), set()
    for r in rows:
        v2 = float(r["Vc_Re_kms"]) ** 2 - 3.36 * float(r["sigma0_kms"]) ** 2
        if v2 < 0:
            eq8_re.add(r["idx"])
        elif math.sqrt(v2) / float(r["sigma0_kms"]) < 2.3:
            cut_re.add(r["idx"])
    lines = [f"CFG305 (CFG289's L323 flagged-rows post-hoc, parametrised): L323 on the {'CORRECTED' if mode == 'ORIG' else 'PUBLISHED'} RC100 table without RC100's own flagged rows",
             f"  flags re-derived from this table: eq.-8 violators {sorted(eq8_re, key=int)}; below V_rot/sigma0 = 2.3 at R_e: {sorted(cut_re, key=int)}",
             f"  equal to the frozen lists (eq8 {sorted(EQ8, key=int)}, 14-row cut): eq8 {eq8_re == EQ8}, cut {cut_re == CUT}"]
    try:
        for tg, drop in (("all 100 rows", set()), ("without rows 67, 83 (eq. 8)", EQ8), ("without the 16 flagged rows", EQ8 | CUT)):
            with open(csv_m, "w", newline="") as fh:
                w = csv.DictWriter(fh, fieldnames=hdr, lineterminator="\n")
                w.writeheader()
                w.writerows([r for r in rows if r["idx"] not in drop])
            p = subprocess.run([sys.executable, L323], cwd=zf, capture_output=True, text=True)
            d = json.load(open(os.path.join(dls, "L323_rc100_framework_vs_lcdm_stress_results.json")))
            lines.append(f"\n  {tg} (n = {len(rows) - len(drop)}; L323 rc {p.returncode})")
            for k, v in d["checks"].items() if isinstance(d["checks"], dict) else []:
                if k.startswith(("S1", "S4")):
                    lines.append(f"    [{'PASS' if v.get('ok') else 'FAIL'}] {k[:70]} | {v['measured']}")
    finally:
        open(csv_m, "wb").write(csv_keep)
        for f, b in keep.items():
            open(os.path.join(dls, f), "wb").write(b)
    open(os.path.join(HERE, f"cfg305_l323_flagged_{mode}.out"), "w").write(scrub("\n".join(lines) + "\n", zf))
    print(f"{mode}: L323 flagged-rows post-hoc written (mirror L323 outputs restored)")
