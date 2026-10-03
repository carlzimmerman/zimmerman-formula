#!/usr/bin/env python3
"""CFG303 POST HOC (labelled; written after the frozen R1 run, Addendum 2 section A2.5): why the S5 identity control (C-i for the MNRAS v3.1
inversion) failed with N 100 against 99.  Hypothesis: f = 1 - (1 - f_DM) g_obs / g_obs, rebuilt in floating point, puts the one galaxy that sits
exactly on the paper's f_DM = 0.02 window edge just inside the open window (0.02, 0.98).  The frozen FAIL stands whatever this finds.
Run:  python3 campaign_fresh_gravity/CFG303_lcdm_free_inputs/cfg303_posthoc_s5_identity.py      Outputs: cfg303_posthoc_s5_identity.out / _results.json
"""
import os, sys, io, csv, json, contextlib, tempfile
sys.dont_write_bytecode = True
LANE = os.path.dirname(os.path.abspath(__file__)); CFG = os.path.dirname(LANE); REPO = os.path.dirname(CFG)
FPN = os.path.join(REPO, "qwen_claude_field_theory", "papers_2026", "mnras_submission_2026_v3", "paper_numbers.py")
src = open(FPN).read(); ns = {"__file__": FPN, "__name__": "cfg303_exec"}


def block(a, b):
    return src[src.index(a):src.index(b)]


with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:src.index('head("S2  ')], "pn[header]", "exec"), ns)
    exec(compile(block('head("S4  THE REDSHIFT LAWS', "g0, r0, c0_ = gmax_nfw("), "pn[S4]", "exec"), ns)
    exec(compile(block("import csv\ndef rc100_run", "R5 = rc100_run(RC100)"), "pn[S5]", "exec"), ns)
JPN = json.load(open(FPN.replace(".py", ".json")))["S5"]
rows = list(csv.DictReader(open(ns["RC100"], newline="")))
OUT, CHK = [], []
P = lambda s="": (print(s), OUT.append(s))
edge = []
for r in rows:
    fd = float(r["fDM_within_Re"]); g = float(r["g_Re_ms2"]); f2 = 1 - ((1 - fd) * g) / g
    if (0.02 < f2 < 0.98) != (0.02 < fd < 0.98):
        edge.append(dict(idx=r["idx"], name=r["name"], fDM=fd, f_rebuilt=f2))
P(f"rows whose window membership flips when f is rebuilt as 1 - (1 - f_DM) g / g: {edge}")
tmp = tempfile.mkdtemp(prefix="cfg303ph_")
res = {}
for lab, nd in (("rebuilt, full precision", None), ("rebuilt, rounded to 10 decimals", 10)):
    p = os.path.join(tmp, lab.split(",")[1].strip().replace(" ", "_") + ".csv")
    with open(p, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["idx", "z", "fDM_within_Re", "g_Re_ms2", "Vc_Re_kms", "sigma0_kms"])
        for r in rows:
            fd = float(r["fDM_within_Re"]); g = float(r["g_Re_ms2"]); f2 = 1 - ((1 - fd) * g) / g
            w.writerow([r["idx"], r["z"], repr(f2 if nd is None else round(f2, nd)), r["g_Re_ms2"], r["Vc_Re_kms"], r["sigma0_kms"]])
    o = ns["rc100_run"](p, verbose=False)
    d = max(abs(o[k] - JPN[k]) / abs(JPN[k]) for k in ("slope", "slope_err", "median_a0", "median_y", "weakest_excl_Hz"))
    res[lab] = dict(N=o["N"], max_rel_diff=d)
    P(f"  {lab}: N {o['N']} (committed {JPN['N']}); max relative difference from paper_numbers.json S5 {d:.1e}")
ok = len(edge) == 1 and res["rebuilt, rounded to 10 decimals"]["N"] == JPN["N"] and res["rebuilt, rounded to 10 decimals"]["max_rel_diff"] <= 1e-12
P(f"[{'PASS' if ok else 'FAIL'}] (post hoc) the identity failure is the single f_DM = 0.02 edge galaxy moved inside the window by floating point; rounding f restores the committed S5 exactly")
P(f"{int(ok)}/1 checks pass")
json.dump(dict(edge=edge, runs=res, ok=ok), open(os.path.join(LANE, "cfg303_posthoc_s5_identity_results.json"), "w"), indent=1)
open(os.path.join(LANE, "cfg303_posthoc_s5_identity.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if ok else 1)
