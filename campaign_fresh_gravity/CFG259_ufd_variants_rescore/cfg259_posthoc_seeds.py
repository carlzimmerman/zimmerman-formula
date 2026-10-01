#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG259 POST HOC (labelled; not in the frozen criteria): bootstrap-seed stability of the FINAL Gate H class under BOTH kernels.
Why: in the main run the P2-kernel class is H2 at every variant (frozen 20-seed check), but the FINAL class (P2 and RAR must agree) moves from H4 at DV0 to H2 at DV1-DV4 because the
RAR-kernel alt-footing Delta chi2_V2 crosses 9 (8.60 at DV0; 9.24-10.11 in the variants).  The frozen seed check covered the P2 kernel only; this reports the RAR kernel and the FINAL class.
Reuses the main script's functions unchanged (its source up to the variants section is exec'd with stdout silenced, which re-runs its controls C1-C4); seeds 259001-259020 as in the main run.
Reporting only: no decision of the main run depends on this file."""
import os, sys, io, json, contextlib, time
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "cfg259_rescore.py")).read()
pre = src[:src.index("# ================================================================================================ the variants")]
_e = os.environ.pop("MUTATE", None)
g = {"__file__": os.path.join(HERE, "cfg259_rescore.py"), "__name__": "cfg259_prefix"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(pre, "cfg259_rescore.py", "exec"), g)
if _e is not None:
    os.environ["MUTATE"] = _e
import numpy as np
T0 = time.time()
LOG = []
def P(s=""):
    print(s, flush=True); LOG.append(str(s))

build, set_data, reset_data, S3 = g["build"], g["set_data"], g["reset_data"], g["S3"]
VARS = ("DV0", "DV1", "DV2", "DV3", "DV4")
P("CFG259 POST HOC: 20-seed stability of the Gate H classes under both kernels (seeds 259001-259020); controls of the main script re-run silently: "
  + ("all pass" if all(c["ok"] for c in g["CK"]) else "SOME FAIL"))
P(f"  {'variant':6s} {'FINAL H2':>9s} {'FINAL H4':>9s} {'P2 H2':>6s} {'RAR H2':>7s} | {'P2 alt d_V2 mean+-SD (min)':>28s} {'RAR alt d_V2 mean+-SD (min)':>29s} | {'RAR can d_V2 mean+-SD':>22s}")
RES = {}
for dv in VARS:
    reset_data(); set_data(build(dv)[0]); rows = []
    for k in range(1, 21):
        s3 = S3(("P2", "RAR"), seed=259000 + k)
        rows.append(dict(p2=s3["P2"]["cls"], rar=s3["RAR"]["cls"], final=s3["final"], p2a=s3["P2"]["alt|V2"]["delta"], ra=s3["RAR"]["alt|V2"]["delta"], rc=s3["RAR"]["canonical|V2"]["delta"]))
    reset_data()
    fin = [r["final"] for r in rows]
    p2a = np.array([r["p2a"] for r in rows]); ra = np.array([r["ra"] for r in rows]); rc = np.array([r["rc"] for r in rows])
    RES[dv] = dict(final={c: fin.count(c) for c in ("H1", "H2", "H3", "H4")}, p2_H2=sum(1 for r in rows if r["p2"] == "H2"), rar_H2=sum(1 for r in rows if r["rar"] == "H2"),
                   p2_alt_dV2=[float(p2a.mean()), float(p2a.std(ddof=1)), float(p2a.min())], rar_alt_dV2=[float(ra.mean()), float(ra.std(ddof=1)), float(ra.min())], rar_can_dV2=[float(rc.mean()), float(rc.std(ddof=1))])
    P(f"  {dv:6s} {fin.count('H2'):>7d}/20 {fin.count('H4'):>7d}/20 {RES[dv]['p2_H2']:>4d}/20 {RES[dv]['rar_H2']:>5d}/20 | {p2a.mean():+9.2f} +- {p2a.std(ddof=1):.2f} ({p2a.min():+.2f})   {ra.mean():+9.2f} +- {ra.std(ddof=1):.2f} ({ra.min():+.2f}) | {rc.mean():+9.2f} +- {rc.std(ddof=1):.2f}")
P(f"  ({time.time() - T0:.0f} s)")
json.dump(RES, open(os.path.join(HERE, "cfg259_posthoc_seeds_results.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg259_posthoc_seeds.out"), "w").write("\n".join(LOG) + "\n")
