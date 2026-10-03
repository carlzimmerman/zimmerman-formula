#!/usr/bin/env python3
"""CFG305 step 2: build the PUBLISHED RC100 CSV (FROZEN_CRITERIA.md, 82dfcc1b3).

Takes real_research/data/rc100_nestorshachar2023_table3_CORRECTED.csv (CFG289), puts in only the cells CONFIRMED by cfg305_confirm.py
(cfg305_confirm_results.json), recomputes the four derived columns only in rows where V_c, R_e or log M_baryon changed (CFG289's rules
and constants), and writes real_research/data/rc100_nestorshachar2023_table3_PUBLISHED.csv.  Controls B1-B4 as frozen.
Also writes (MUTATE=1) the MUTATE copy into a given scratch path: row 50 log M_baryon +0.30 dex, its derived columns recomputed.
Run:  python3 campaign_fresh_gravity/CFG305_published_tables/cfg305_build_published.py
      MUTATE=1 python3 .../cfg305_build_published.py <out_csv>     (writes only <out_csv>; never a repo file)
"""
import csv, hashlib, io, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CORR = os.path.join(REPO, "real_research", "data", "rc100_nestorshachar2023_table3_CORRECTED.csv")
OUT = os.path.join(REPO, "real_research", "data", "rc100_nestorshachar2023_table3_PUBLISHED.csv")
CONF = os.path.join(HERE, "cfg305_confirm_results.json")
G, KPC, MSUN, A_REF = 6.674e-11, 3.0857e19, 1.989e30, 1.2e-10
PRIMARY = ["name", "z", "logMbar_Msun", "Re_kpc", "fDM_within_Re", "Vc_Re_kms", "sigma0_kms"]
NUMF = ["z", "logMbar_Msun", "Re_kpc", "fDM_within_Re", "Vc_Re_kms", "sigma0_kms"]
DERIVED = ["g_Re_ms2", "a0_Vc4_over_GMbar_ms2", "a0_over_1.2e-10", "deepMOND_g_lt_a0"]
INPUTS = {"Vc_Re_kms", "Re_kpc", "logMbar_Msun"}
MUT = os.environ.get("MUTATE", "") == "1"
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


def put_derived(n):
    g, a = derived(n)
    n["g_Re_ms2"] = f"{g:.4e}"
    n["a0_Vc4_over_GMbar_ms2"] = f"{a:.4e}"
    n["a0_over_1.2e-10"] = f"{a / A_REF:.3f}"
    n["deepMOND_g_lt_a0"] = "1" if g < A_REF else "0"


def write(rows, cols, raw, path):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=cols, lineterminator="\r\n" if "\r\n" in raw else "\n")
    w.writeheader()
    w.writerows(rows)
    open(path, "w", newline="").write(buf.getvalue())
    return buf.getvalue()


raw = open(CORR, newline="").read()
Cr = list(csv.DictReader(io.StringIO(raw)))
cols = list(Cr[0].keys())
CF = json.load(open(CONF))

if MUT:
    # MUTATE copy: the PUBLISHED CSV with row 50 log M_baryon +0.30 dex (derived recomputed); written only to the given scratch path
    out_csv = os.path.abspath(sys.argv[1])
    assert not out_csv.startswith(REPO + os.sep), "MUTATE copy must not be written inside the repo"
    praw = open(OUT, newline="").read()
    R = list(csv.DictReader(io.StringIO(praw)))
    r50 = next(r for r in R if r["idx"] == "50")
    old = r50["logMbar_Msun"]
    r50["logMbar_Msun"] = f"{float(old) + 0.30:.2f}"
    put_derived(r50)
    write(R, cols, praw, out_csv)
    print(f"MUTATE copy: row 50 ({r50['name']}) logMbar {old} -> {r50['logMbar_Msun']}; a0_Vc4/GMbar -> {r50['a0_Vc4_over_GMbar_ms2']}; sha256 {sha(out_csv)[:16]}")
    sys.exit(0)

P(f"CFG305 build: CORRECTED {os.path.relpath(CORR, REPO)} sha256 {sha(CORR)[:16]}; confirm results sha256 {sha(CONF)[:16]}; "
  f"FROZEN_CRITERIA.md sha256 {sha(os.path.join(HERE, 'FROZEN_CRITERIA.md'))[:16]}")
conf = CF["rc100_confirmed_cells"]
P(f"  confirmed cells to apply: {[(c['idx'], c['field'], c['published']) for c in conf]}")
cmap = {(c["idx"], c["field"]): c["published"] for c in conf}
changed, recomputed = [], []
Pb = []
for r in Cr:
    n = dict(r)
    for f in NUMF:
        if (r["idx"], f) in cmap:
            changed.append(dict(idx=r["idx"], name=r["name"], field=f, corrected=n[f], published=cmap[(r["idx"], f)]))
            n[f] = cmap[(r["idx"], f)]
    if any(c["idx"] == r["idx"] and c["field"] in INPUTS for c in changed):
        put_derived(n)
        recomputed.append(r["idx"])
    Pb.append(n)
out_text = write(Pb, cols, raw, OUT)

# B1: derived reproduction on every row whose derived cells are not recomputed
worst, nrows = 0.0, 0
for r in Pb:
    if r["idx"] in recomputed:
        continue
    g, a = derived(r)
    worst = max(worst, abs(g / float(r["g_Re_ms2"]) - 1), abs(a / float(r["a0_Vc4_over_GMbar_ms2"]) - 1))
    nrows += 1
check("B1 the frozen constants reproduce the derived columns of every row whose derived cells are not recomputed (<= 5e-5 relative)", worst <= 5e-5,
      f"worst relative deviation {worst:.2e} over {nrows} rows")
# B2: header + untouched rows byte-identical
ol, nl = raw.splitlines(), out_text.splitlines()
touched = {c["idx"] for c in changed}
same = ol[0] == nl[0] and len(ol) == len(nl) and all(ol[i + 1] == nl[i + 1] for i, r in enumerate(Cr) if r["idx"] not in touched)
check("B2 header and every untouched row byte-identical to the CORRECTED CSV", same, f"{len(Cr) - len(touched)} untouched rows, touched rows {sorted(touched, key=int)}")
# B3: exactly the confirmed primary cells + derived cells of rows with a changed input
diff_cells = [(a["idx"], f) for a, b in zip(Cr, Pb) for f in cols if a[f] != b[f]]
prim = sorted((i, f) for i, f in diff_cells if f in PRIMARY)
der = sorted((i, f) for i, f in diff_cells if f in DERIVED)
ok3 = prim == sorted(cmap) and all(i in recomputed for i, _ in der) and not [x for x in diff_cells if x[1] not in PRIMARY + DERIVED]
check("B3 exactly the confirmed primary cells differ from the CORRECTED CSV, plus only derived cells of rows with a changed V_c/R_e/log M_baryon", ok3,
      f"primary {prim}; derived {der}")
# B4: six numeric primary fields equal the published parse in all 100 rows
PUB = CF["rc100_published"]
mism = [(r["idx"], f) for r in Pb for f in NUMF if abs(float(r[f]) - float(PUB[r["idx"]][f].replace("−", "-"))) > 1e-9]
check("B4 the PUBLISHED CSV's six numeric primary fields equal the published Table B1 parse in all 100 rows", not mism and len(Pb) == 100, f"mismatches {mism}")

P("\nCHANGED CELLS (CORRECTED -> PUBLISHED) and the derived consequences")
for c in changed:
    P(f"  row {c['idx']:>3} {c['name']:<12} {c['field']:<14} {c['corrected']:>8} -> {c['published']}")
for a, b in zip(Cr, Pb):
    if a["idx"] in touched:
        P(f"  row {a['idx']:>3} {a['name']:<12} g_Re {a['g_Re_ms2']} -> {b['g_Re_ms2']}; a0_Vc4/GMbar {a['a0_Vc4_over_GMbar_ms2']} -> {b['a0_Vc4_over_GMbar_ms2']} "
          f"(a0/1.2e-10 {a['a0_over_1.2e-10']} -> {b['a0_over_1.2e-10']}); deepMOND {a['deepMOND_g_lt_a0']} -> {b['deepMOND_g_lt_a0']}"
          + ("" if a["idx"] in recomputed else "  [sigma0-only change: derived cells kept]"))
r78 = dict(next(r for r in Pb if r["idx"] == "78"))
g78, a78 = derived(r78)
P(f"  (row 78 for information: recomputing its derived cells with the frozen constants would give g_Re {g78:.4e}, a0 {a78:.4e}; kept: {r78['g_Re_ms2']}, {r78['a0_Vc4_over_GMbar_ms2']})")
flips = [a["idx"] for a, b in zip(Cr, Pb) if a["deepMOND_g_lt_a0"] != b["deepMOND_g_lt_a0"]]
P(f"  deepMOND flag flips: {flips if flips else 'none'}")
P(f"\nwrote {os.path.relpath(OUT, REPO)} sha256 {sha(OUT)}")
n_ok = sum(c["ok"] for c in checks)
P(f"{n_ok}/{len(checks)} checks pass")
json.dump(dict(corrected_sha256=sha(CORR), published_sha256=sha(OUT), confirm_results_sha256=sha(CONF), changed=changed, derived_recomputed_rows=recomputed,
               deepMOND_flips=flips, checks=checks), open(os.path.join(HERE, "cfg305_build_published_results.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg305_build_published.out"), "w").write("\n".join(lines) + "\n")
sys.exit(0 if n_ok == len(checks) else 1)
