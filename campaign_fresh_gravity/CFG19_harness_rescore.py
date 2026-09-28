#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG19 -- THE HARNESS RE-SCORED WITH CFG18: candidate B (CFG4's target + FG001's hierarchical ownership) with its accreted satellites
scored on their infall baryons, as FG001's class A states.

WHAT CHANGES.  FG097's committed harness scores B's population gates from FG001's committed scorecard.  Two of those gates -- the M31
dwarfs (LVD) and the M31 dwarfs (Collins+13), on both footings -- were computed with the satellites' stripped present-day stars.
CFG18 (committed) re-scored them with the infall baryons (the conservative bracket: HI non-detections as zero gas).  This lane takes
B's committed gate rows, replaces exactly those four rows with CFG18's values (pass iff within 2 sigma, the harness's own rule), and
recounts.  Nothing else is touched: the MW ultra-faints stay FG001's (CFG18 leaves them failing), and Chae's D1/D2 gates stay FG001's
(CFG8's refit is a different statistic and is NOT substituted).

PRE-DECLARED (before this script's first run)
  C1  CONTROL  recounting B's committed rows reproduces the harness's committed 38/48 and every other candidate's committed score.
  H1  [MUTATE must fail] with CFG18's four M31 rows, B passes 42/48 scored gates (4 flips, all FAIL -> PASS).
MUTATE=1: CFG18's rows are not substituted -- B stays at 38/48 and H1 must FAIL (rc = 1).
Run: python3 campaign_fresh_gravity/CFG19_harness_rescore.py
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG19_harness_rescore", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
H = json.load(open(os.path.join(HERE, "CFG7_harness_fg097_results.json")))["numbers"]["SCORES"]
C18 = json.load(open(os.path.join(HERE, "CFG18_satellite_infall_gas_results.json")))["numbers"]["RES"]

# ================================================================================================ C1
R.banner("C1  CONTROL: the harness's committed scores recounted from its rows")
dev = 0
for name, s in H.items():
    n = sum(r["ok"] for r in s["rows"] if "reported" not in r["gate"]); t = sum(1 for r in s["rows"] if "reported" not in r["gate"])
    dev += abs(n - s["npass"]) + abs(t - s["ntot"])
    P(f"    {name:58s}: {n}/{t} (committed {s['npass']}/{s['ntot']})")
check("C1 CONTROL: every candidate's committed score is reproduced by recounting its committed rows", f"total |d| {dev}", dev == 0)

# ================================================================================================ H1
R.banner("H1  CANDIDATE B WITH CFG18's M31 ROWS")
bname = [n for n in H if n.startswith("B ")][0]
rows = [dict(r) for r in H[bname]["rows"]]
MAP = {"pop: M31 dwarfs (LVD)": "m31", "pop: M31 dwarfs (Collins+13)": "col"}
flips = []
for r in rows:
    if r["gate"] in MAP and not MUTATE:
        v = C18[f"{MAP[r['gate']]}|zero|{r['foot']}"]
        new_ok = v["z"] <= 2.0
        if new_ok != r["ok"]:
            flips.append((r["gate"], r["foot"], r["ok"], new_ok, v["z"]))
        r["ok"] = new_ok
        r["value"] = f"{v['z']:.2f} sigma (CFG18: infall baryons, non-detections as zero)"
npass = sum(r["ok"] for r in rows if "reported" not in r["gate"]); ntot = sum(1 for r in rows if "reported" not in r["gate"])
for g, f, o, nn, z in flips:
    P(f"    {g:34s} {f:9s}: {'PASS' if o else 'FAIL'} -> {'PASS' if nn else 'FAIL'} ({z:.2f} sigma)")
P(f"    B re-scored: {npass}/{ntot} (committed {H[bname]['npass']}/{H[bname]['ntot']}); still failing: " +
  "; ".join(f"{r['gate']} {r['foot']}" for r in rows if not r["ok"] and "reported" not in r["gate"]))
check("H1 with CFG18's four M31 rows candidate B passes 42/48 scored gates (4 flips, all FAIL -> PASS)" +
      ("  [MUTATE: not substituted]" if MUTATE else ""), f"{npass}/{ntot}; flips {len(flips)}",
      npass == 42 and ntot == 48 and len(flips) == 4 and all(nn and not o for _, _, o, nn, _ in flips))
R.num("B_rescored", dict(npass=npass, ntot=ntot, flips=[dict(gate=g, foot=f, z=z) for g, f, o, nn, z in flips],
                         rows=rows))
nf = R.write()
sys.exit(1 if nf else 0)
