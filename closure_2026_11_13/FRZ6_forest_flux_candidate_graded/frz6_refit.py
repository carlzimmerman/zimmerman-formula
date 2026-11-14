#!/usr/bin/env python3
"""FRZ6 reported reading (i) (FROZEN_CRITERIA.md section 9): FRZ5's primary refit applied to this lane's ratios.
FRZ5's frz5_refit.py (closure_2026_11_13/FRZ5_forest_nuisance_refit) is executed read-only from its own path up to its
"reading G" marker (P1D3's per-bin amplitude, tilt and smoothing template; profiled Asimov Delta chi^2 on the full
covariance); its refit() is then applied to the 755-point ratio of every case in frz6_grade_<footing>.json.
A template reading, not a physical gas model; never the label.
Usage: nice -n 19 python3 -I -B frz6_refit.py <footing> -> frz6_refit_<footing>.json / .out
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, json, io, contextlib
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
FRZ5 = os.path.join(REPO, "closure_2026_11_13", "FRZ5_forest_nuisance_refit")
FOOT = sys.argv[1]; assert FOOT in ("canonical", "alt")
SRC = os.path.join(FRZ5, "frz5_refit.py"); src = open(SRC).read()
cut = src.index("# ------------------------------------------------------------------ reading G")
ns = {"__file__": SRC, "__name__": "frz5_refit_prefix_frz6"}; _a = sys.argv; sys.argv = ["frz5_refit.py", FOOT]
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:cut], SRC, "exec"), ns)
sys.argv = _a
import numpy as np
refit, chi2_w, chi2_rec = ns["refit"], ns["chi2_w"], ns["chi2_rec"]
G = json.load(open(os.path.join(HERE, f"frz6_grade_{FOOT}.json")))
OUT = []; RES = dict(lane="FRZ6", footing=FOOT, reading="FRZ5 primary refit (template), reported beside the label", cases={},
                     note="kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
def P(s): print(s, flush=True); OUT.append(s)
for key, r in G["r_points"].items():
    r = np.array(r); fx = chi2_w(r); fr = chi2_rec(r); rf = refit(r)
    RES["cases"][key] = dict(fixed=fx, fixed_record_form=fr, grade_flux=G["rows"][key]["flux"], refit=rf)
    P(f"[{FOOT}] {key}: fixed {fx:.4f} (record form {fr:.4f}; grade {G['rows'][key]['flux']:.4f}) -> refit {rf['dchi2']:.4f}; max|A-1| {rf['max_absA_minus1']:.3f}, "
      f"max|alpha| {rf['max_abs_alpha']:.3f}, max|R-R0| {rf['max_abs_dR']:.3f} Mpc/h; honest {rf['honest']}")
json.dump(RES, open(os.path.join(HERE, f"frz6_refit_{FOOT}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"frz6_refit_{FOOT}.out"), "w").write("\n".join(OUT) + "\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.\n")
