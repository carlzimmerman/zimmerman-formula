#!/usr/bin/env python3
"""X53 AMENDMENT A1 diagnostics (post-result, REPORTED ONLY; no graded line changes).
Is the LAW class driven by the halo EDGE (outer shape) or by the halo NORMALISATION (EM1's SPARC M200 relation)?
(H) with a profiled shift in log M200 (common to all bins; then per bin), truncated at R200 vs untruncated (Burkert to 100 R200),
each with CFG805's two-halo term (b_eff >= 0 per bin). Executes x53_outer_lensing.py's definitions read-only (up to its scoring loop).

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x53_diag_A1.py   -> x53_diag_A1.out, x53_diag_A1_results.json
kappa = 1/2 FITTED; not theory closed.
"""
import os, sys, io, json, time, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
os.environ.pop("X53_MUTATE", None)
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "x53_outer_lensing.py")
T = open(SRC).read()
code = T[:T.index("for foot in FOOTS:\n    P(f\"\\n=== [{foot}]")]
NS = {"__file__": SRC, "__name__": "x53_ro"}
with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
    exec(compile(code, SRC, "exec"), NS)
T0 = time.time()
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))

orig = NS["halo_setup"]; BGb = NS["BG"]
def halo_shift(foot, logMbrel, cfg_h):
    return orig(foot, logMbrel + cfg_h.get("dlM", 0.0) / BGb[cfg_h["bg"]]["b"], cfg_h)
NS["halo_setup"] = halo_shift
stack_H, stack_model, fit = NS["stack_H"], NS["stack_model"], NS["fit"]
IDX_ALL, IDX_PRIM, Rn, CENTRAL0 = NS["IDX_ALL"], NS["IDX_PRIM"], NS["Rn"], NS["CENTRAL0"]
HP = dict(NS["H_PRIMARY"])
SH = np.round(np.arange(-0.3, 1.2001, 0.05), 2)
RES = dict(lane="X53 A1 diagnostics (reported only)", shifts=SH.tolist(), footings={})
P("X53 AMENDMENT A1 diagnostics (post-result, reported only): profiled log M200 shift for (H), truncated vs untruncated; c_f 4; with CFG805 2h")
for foot in ("canonical", "alt"):
    mL = stack_model(foot, Rn, CENTRAL0)
    fo = {}
    for lab, idx in (("primary", IDX_PRIM), ("all", IDX_ALL)):
        fo[lab] = dict(L2H=fit(mL, idx, True)[0]["chi2"], L=fit(mL, idx, False)[0]["chi2"])
    for trunc in (True, False):
        NS["MUT"] = not trunc                                    # rcut = 100 R200 when untruncated (geometry only; law untouched)
        TAB = {float(s): stack_H(foot, dict(HP, dlM=float(s)))[0] for s in SH}
        key = "truncated" if trunc else "untruncated(100 R200)"
        o = {}
        for lab, idx in (("primary", IDX_PRIM), ("all", IDX_ALL)):
            c0 = {s: fit(TAB[s], idx, True)[0]["chi2"] for s in TAB}
            sc = min(c0, key=c0.get)
            # per-bin shifts, coordinate descent from the common best
            Ls = [sc] * 4
            def mk(Ls): return np.array([TAB[Ls[b]][b] for b in range(4)])
            for _ in range(3):
                for b in range(4):
                    Ls[b] = min(TAB, key=lambda s: fit(mk(Ls[:b] + [s] + Ls[b + 1:]), idx, True)[0]["chi2"])
            rb, _ = fit(mk(Ls), idx, True)
            o[lab] = dict(common_shift=sc, chi2_common=c0[sc], dchi2_common_vs_L2H=c0[sc] - fo[lab]["L2H"], chi2_at_0=c0[0.0],
                          perbin_shift=Ls, chi2_perbin=rb["chi2"], dchi2_perbin_vs_L2H=rb["chi2"] - fo[lab]["L2H"], b_perbin=rb["b"],
                          edge_of_grid=bool(sc in (SH[0], SH[-1]) or any(s in (SH[0], SH[-1]) for s in Ls)))
            P(f"  [{foot} {key} {lab}] L2H {fo[lab]['L2H']:.1f}; H2H at shift 0 {c0[0.0]:.1f}; best common dlogM200 {sc:+.2f}: chi2 {c0[sc]:.1f} "
              f"(dchi2 vs L2H {c0[sc] - fo[lab]['L2H']:+.1f}, 1 extra param); per-bin {Ls}: chi2 {rb['chi2']:.1f} (dchi2 vs L2H {rb['chi2'] - fo[lab]['L2H']:+.1f}, 4 extra), "
              f"b {np.round(rb['b'], 2).tolist()}" + ("  [grid edge]" if o[lab]["edge_of_grid"] else ""))
        fo[key] = o
        P(f"  [{time.time() - T0:.0f} s]")
    NS["MUT"] = False
    RES["footings"][foot] = fo
open(os.path.join(HERE, "x53_diag_A1.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, "x53_diag_A1_results.json"), "w"), indent=1, default=float)
