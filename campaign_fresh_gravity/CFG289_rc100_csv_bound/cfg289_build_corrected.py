#!/usr/bin/env python3
"""CFG289 step 1: build the corrected RC100 CSV (FROZEN_CRITERIA.md, 80f05e155).

Takes the repo's original real_research/data/rc100_nestorshachar2023_table3.csv, puts in the 17 paper values listed in
data_assembly/rc100_provenance/rc100_table3_six_fields_paper_values.csv (changed_cells), recomputes the four derived columns for the
changed rows only, and writes real_research/data/rc100_nestorshachar2023_table3_CORRECTED.csv.  Controls C1-C4 as frozen.
Run from anywhere: python3 campaign_fresh_gravity/CFG289_rc100_csv_bound/cfg289_build_corrected.py
"""
import csv, hashlib, io, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
ORIG = os.path.join(REPO, "real_research", "data", "rc100_nestorshachar2023_table3.csv")
PAPER = os.path.join(REPO, "data_assembly", "rc100_provenance", "rc100_table3_six_fields_paper_values.csv")
OUT = os.path.join(REPO, "real_research", "data", "rc100_nestorshachar2023_table3_CORRECTED.csv")
G, KPC, MSUN, A_REF = 6.674e-11, 3.0857e19, 1.989e30, 1.2e-10
PRIMARY = ["name", "z", "logMbar_Msun", "Re_kpc", "fDM_within_Re", "Vc_Re_kms", "sigma0_kms"]
lines, checks = [], []
P = lambda s="": (print(s), lines.append(s))
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()


def check(name, ok, detail=""):
    checks.append(dict(check=name, ok=bool(ok), detail=detail))
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"\n         {detail}" if detail else ""))


def derived(r):
    V = float(r["Vc_Re_kms"]) * 1e3
    g = V * V / (float(r["Re_kpc"]) * KPC)
    a = V ** 4 / (G * 10 ** float(r["logMbar_Msun"]) * MSUN)
    return g, a


raw = open(ORIG, newline="").read()
O = list(csv.DictReader(io.StringIO(raw)))
cols = list(O[0].keys())
PV = {r["idx"]: r for r in csv.DictReader(open(PAPER, newline=""))}
P(f"CFG289 build: original {os.path.relpath(ORIG, REPO)} sha256 {sha(ORIG)[:16]}; paper values {os.path.relpath(PAPER, REPO)} sha256 {sha(PAPER)[:16]}")
P(f"  FROZEN_CRITERIA.md sha256 {sha(os.path.join(HERE, 'FROZEN_CRITERIA.md'))[:16]}")

# C1: derived-column reproduction on untouched rows
worst = 0.0
for r in O:
    if PV[r["idx"]]["changed_cells"].strip():
        continue
    g, a = derived(r)
    worst = max(worst, abs(g / float(r["g_Re_ms2"]) - 1), abs(a / float(r["a0_Vc4_over_GMbar_ms2"]) - 1))
check("C1 the frozen constants reproduce the original's derived columns on the untouched rows (<= 5e-5 relative)", worst <= 5e-5,
      f"worst relative deviation {worst:.2e} over {sum(1 for r in O if not PV[r['idx']]['changed_cells'].strip())} rows")

# build
changed = []
C = []
for r in O:
    p = PV[r["idx"]]
    n = dict(r)
    for f in PRIMARY:
        if n[f] != p[f]:
            changed.append(dict(idx=r["idx"], field=f, original=n[f], paper=p[f]))
            n[f] = p[f]
    if any(c["idx"] == r["idx"] for c in changed):
        g, a = derived(n)
        n["g_Re_ms2"] = f"{g:.4e}"
        n["a0_Vc4_over_GMbar_ms2"] = f"{a:.4e}"
        n["a0_over_1.2e-10"] = f"{a / A_REF:.3f}"
        n["deepMOND_g_lt_a0"] = "1" if g < A_REF else "0"
    C.append(n)

buf = io.StringIO()
w = csv.DictWriter(buf, fieldnames=cols, lineterminator="\n" if "\r\n" not in raw else "\r\n")
w.writeheader()
w.writerows(C)
out_text = buf.getvalue()
open(OUT, "w", newline="").write(out_text)

# C2: untouched rows byte-identical
orig_lines, new_lines = raw.splitlines(), out_text.splitlines()
touched = {c["idx"] for c in changed}
same = all(orig_lines[i + 1] == new_lines[i + 1] for i, r in enumerate(O) if r["idx"] not in touched) and orig_lines[0] == new_lines[0]
check("C2 header and every untouched row byte-identical to the original", same and len(orig_lines) == len(new_lines),
      f"{len(O) - len(touched)} untouched rows, {len(touched)} touched")

# C3: exactly the 17 listed cells
SHORT = {"name": "name", "logMbar": "logMbar_Msun", "fDM": "fDM_within_Re", "Vc": "Vc_Re_kms", "z": "z", "Re": "Re_kpc", "sigma0": "sigma0_kms"}
listed = []
for i, p in PV.items():
    for f in [x.strip() for x in p["changed_cells"].replace(";", ",").split(",") if x.strip()]:
        listed.append((i, SHORT[f]))
got = sorted((c["idx"], c["field"]) for c in changed)
check("C3 exactly 17 primary/name cells differ from the original and they are the cells listed in changed_cells",
      len(changed) == 17 and sorted(listed) == got, f"changed {len(changed)}; listed {len(listed)}; listed == changed: {sorted(listed) == got}")

# C4: primary fields equal the paper-values file in all rows
mism = [(r["idx"], f) for r in C for f in PRIMARY if r[f] != PV[r["idx"]][f]]
check("C4 the corrected copy's primary fields equal the paper-values file in all 100 rows", not mism and len(C) == 100, f"mismatches {len(mism)}")

P("\nCHANGED CELLS (original -> paper) and the derived consequences")
for c in changed:
    P(f"  row {c['idx']:>3} {c['field']:<14} {c['original']:>14} -> {c['paper']}")
flips = []
for r0, r1 in zip(O, C):
    if r0["idx"] in touched and r0["deepMOND_g_lt_a0"] != r1["deepMOND_g_lt_a0"]:
        flips.append(r0["idx"])
    if r0["idx"] in touched:
        P(f"  row {r0['idx']:>3} {r1['name']:<14} a0_Vc4/GMbar {r0['a0_Vc4_over_GMbar_ms2']} -> {r1['a0_Vc4_over_GMbar_ms2']}; "
          f"g_Re {r0['g_Re_ms2']} -> {r1['g_Re_ms2']}; deepMOND {r0['deepMOND_g_lt_a0']} -> {r1['deepMOND_g_lt_a0']}")
P(f"  deepMOND flag flips: {flips if flips else 'none'}")
P(f"\nwrote {os.path.relpath(OUT, REPO)} sha256 {sha(OUT)[:16]}")
n_ok = sum(c["ok"] for c in checks)
P(f"{n_ok}/{len(checks)} checks pass")
json.dump(dict(original_sha256=sha(ORIG), paper_values_sha256=sha(PAPER), corrected_sha256=sha(OUT), changed=changed,
               deepMOND_flips=flips, checks=checks), open(os.path.join(HERE, "cfg289_build_corrected_results.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg289_build_corrected.out"), "w").write("\n".join(lines) + "\n")
sys.exit(0 if n_ok == len(checks) else 1)
