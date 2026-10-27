#!/usr/bin/env python3
"""X53 step 0 (stop rule, FROZEN_CRITERIA.md section 6): rerun the committed CFG801, CFG803 and CFG805 scripts UNCHANGED in a
scratch copy (outputs land in the scratch copy, never in their folders) and compare with the frozen headline numbers.

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x53_step0.py   -> x53_step0.out, x53_step0_results.json
kappa = 1/2 FITTED; not theory closed.
"""
import os, sys, json, shutil, subprocess, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CFG = os.path.join(REPO, "campaign_fresh_gravity")
LANES = ["CFG801_settled_edge_vs_kids", "CFG803_infall_profile_vs_kids", "CFG804_catchment_supply_derived", "CFG805_two_halo_t1x"]
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))

T0 = time.time()
tmp = tempfile.mkdtemp(prefix="x53_step0_")
os.makedirs(os.path.join(tmp, "campaign_fresh_gravity"))
os.symlink(os.path.join(REPO, "real_research"), os.path.join(tmp, "real_research"))
for L in LANES:
    d = os.path.join(tmp, "campaign_fresh_gravity", L); os.makedirs(d)
    for f in os.listdir(os.path.join(CFG, L)):
        if f.endswith(".py"):
            shutil.copy2(os.path.join(CFG, L, f), d)
env = dict(os.environ, OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1", PYTHONHASHSEED="0")
for k in ("CFG801_MUTATE", "CFG803_MUTATE", "CFG805_MUTATE"):
    env.pop(k, None)
RUNS = [("CFG801_settled_edge_vs_kids", "cfg801.py", []), ("CFG801_settled_edge_vs_kids", "cfg801.py", ["alt"]),
        ("CFG803_infall_profile_vs_kids", "cfg803.py", []), ("CFG805_two_halo_t1x", "cfg805.py", [])]
for L, s, a in RUNS:
    d = os.path.join(tmp, "campaign_fresh_gravity", L)
    r = subprocess.run([sys.executable, s] + a, cwd=d, env=env, capture_output=True, text=True)
    P(f"  ran {L}/{s} {' '.join(a)}: exit {r.returncode} [{time.time() - T0:.0f} s]")
    if r.returncode != 0:
        P(r.stderr[-2000:])
def J(L, f): return json.load(open(os.path.join(tmp, "campaign_fresh_gravity", L, f)))
c1, c1a = J(RUNS[0][0], "cfg801_results.json"), J(RUNS[0][0], "cfg801_results_alt.json")
c3, c5 = J(RUNS[2][0], "cfg803_results.json"), J(RUNS[3][0], "cfg805_results.json")
k5txt = open(os.path.join(tmp, "campaign_fresh_gravity", RUNS[3][0], "cfg805.out")).read()
k1_805 = [l for l in k5txt.splitlines() if "K1 b=0" in l][0]
d805_b0 = float(k1_805.split("all radii")[1].split("(")[0])
ROWS = [("CFG801 canonical primary", c1["primary R<=0.31 Mpc"]["dchi2"], 197.07, 1.0),
        ("CFG801 canonical all radii", c1["all radii"]["dchi2"], 753.02, 1.0),
        ("CFG801 alt primary", c1a["primary R<=0.31 Mpc"]["dchi2"], 234.00, 1.0),
        ("CFG801 alt all radii", c1a["all radii"]["dchi2"], 813.04, 1.0),
        ("CFG803 primary dC", c3["primary"]["dC"], 0.13, 0.2),
        ("CFG803 all dC", c3["all"]["dC"], 2.75, 0.2),
        ("CFG805 b=0 (CFG804) all", d805_b0, 148.7, 0.2),
        ("CFG805 with two-halo all", c5["all"]["dchi2"], 11.06, 0.2)]
ok = True; RES = dict(lane="X53_step0", rows={})
for lab, v, ref, tol in ROWS:
    p = abs(v - ref) <= tol; ok &= p
    RES["rows"][lab] = dict(value=v, frozen=ref, tol=tol, pass_=p)
    P(f"  {lab:30s} {v:+9.2f}  (frozen {ref:+.2f} +- {tol}): {'PASS' if p else 'FAIL'}")
RES["b_eff_cfg805_D"] = c5["all"]["b_D"]; RES["b_eff_cfg805_B"] = c5["all"]["b_B"]
P(f"  CFG805 b_eff (D_der+2h, all radii) {[round(x, 2) for x in c5['all']['b_D']]}")
P(f"STEP 0 (stop rule): {'PASS' if ok else 'FAIL'}   [{time.time() - T0:.0f} s]")
RES["step0_pass"] = bool(ok)
shutil.rmtree(tmp, ignore_errors=True)
json.dump(RES, open(os.path.join(HERE, "x53_step0_results.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "x53_step0.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if ok else 1)
