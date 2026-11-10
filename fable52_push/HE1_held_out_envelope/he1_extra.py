#!/usr/bin/env python3
"""HE1 extras: POST HOC, REPORTED ONLY (written after the graded run; no label rests on it).

E1  The quasi-static stability reading. he1.py re-solved the envelope at fixed sigma and share with the wall displaced by
    +-5 %, taking any root of the share condition within +-30 in ln rho_w. For the census and cap shares at log M_b >= 10.45 it
    found non-restoring responses with p_env / p_wall of 0.17 and 136, which suggests a different branch. Here, at the four
    KiDS masses and every X at the primary R_out:
    (a) d ln M_env(R_out) / d ln rho_w at fixed sigma and R_w (central differences). A negative value means the equilibrium sits
        past the turnover of the share condition (a Bonnor-Ebert-type branch).
    (b) the root nearest the unperturbed ln rho_w (scan of +-3 in steps of 0.01, then brentq) for displacements of +-1 % and
        +-5 %, and whether p_env' against p_wall(R_w') restores.
    (c) the density contrast rho(R_w) / rho(R_out).
    Result: the local response restores everywhere; the census / cap envelopes at log M_b >= 10.45 sit past the turnover.
Run: python3 he1_extra.py -> he1_extra.json / he1_extra.out.   kappa = 1/2 FITTED; not theory closed.  Adopts nothing.
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import json, math
import numpy as np
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "he1.py")).read(); cut = src.index("# ====================================================================== KNOWN ANSWERS")
NS = {"__file__": os.path.join(HERE, "he1.py"), "__name__": "he1_lib"}
_a = sys.argv; sys.argv = ["he1.py"]
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:cut], "he1.py", "exec"), NS)
sys.argv = _a
envelope, env_solve, Wd, A0, FOOT, KIDS, XNAMES = (NS[k] for k in ("envelope", "env_solve", "Wd", "A0", "FOOT", "KIDS", "XNAMES"))
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
RES = dict(lane="HE1", part="extras, post hoc, reported only", note="kappa = 1/2 FITTED; not theory closed; adopts nothing", E1={})
P("HE1 extras (post hoc, reported only). E1: quasi-static stability at fixed sigma and share, primary R_out.")
def menv(xw, s, lr, xo): return env_solve(xw, s, math.exp(lr), xo).y[1, -1] - 1.0
for f in FOOT:
    RES["E1"][f] = {}
    for Xn in XNAMES:
        for lm in KIDS:
            e = envelope(lm, A0[f], Xn, "rta")
            if not e.balance: continue
            lr0 = math.log(e.rho_w); h = 1e-3
            dlnM = (math.log(menv(e.xw, e.s, lr0 + h, e.xo)) - math.log(menv(e.xw, e.s, lr0 - h, e.xo))) / (2 * h)
            contrast = math.exp(lr0 - float(e.lr[-1]))
            rows = {}
            for frac in (0.01, -0.01, 0.05, -0.05):
                xn = e.xw * (1 + frac)
                F = lambda lr: menv(xn, e.s, lr, e.xo) - e.X
                grid = lr0 + np.arange(-3.0, 3.0001, 0.01); vals = np.array([F(g) for g in grid])
                roots = []
                for i in range(grid.size - 1):
                    if vals[i] * vals[i + 1] <= 0:
                        roots.append(brentq(F, grid[i], grid[i + 1], xtol=1e-12))
                if not roots:
                    rows[f"{frac:+.2f}"] = dict(root=None); continue
                lr = min(roots, key=lambda r: abs(r - lr0))
                pe = math.exp(lr) * e.s; pw = Wd(xn) / (4 * math.pi)
                rows[f"{frac:+.2f}"] = dict(n_roots_within_3=len(roots), dlnrho=lr - lr0, p_env_over_p_wall=pe / pw,
                                            restoring=bool((pe > pw) if frac > 0 else (pe < pw)))
            RES["E1"][f][f"{Xn}|{lm}"] = dict(x_w=e.xw, x_out=e.xo, X=e.X, dlnM_dlnrho=dlnM, contrast=contrast, rows=rows)
            P(f"[{f}] X {Xn:6s} log M_b {lm}: x_w {e.xw:6.1f}, x_out {e.xo:6.1f}; d ln M_env / d ln rho_w {dlnM:+.3f}; contrast rho(R_w)/rho(R_out) {contrast:9.1f}; "
              + "; ".join(f"{k}: " + (f"p_env/p_wall {v['p_env_over_p_wall']:.3f} ({'restoring' if v['restoring'] else 'NOT restoring'}; {v['n_roots_within_3']} roots)" if v.get('root', 1) is not None and 'p_env_over_p_wall' in v else "no root") for k, v in rows.items()))
P("")
P("Reading. With the root nearest the unperturbed state, every displacement of the wall restores (one -5 % case has no root")
P("within +-3 in ln rho_w). he1.py's reported quasi-static entries for X_census / X_cap at log M_b >= 10.45 took a second root")
P("about e^1 away and are not the local response. A negative d ln M_env / d ln rho_w (those same envelopes; density contrast")
P("59-250) means they sit past the turnover of the share condition at fixed sigma, the analogue of a Bonnor-Ebert sphere beyond")
P("its critical contrast (about 14). That points to a gravothermal instability of the envelope itself, which no gate here")
P("grades. X_share envelopes have contrast 1.2-1.3 and d ln M / d ln rho near +0.93. kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
json.dump(RES, open(os.path.join(HERE, "he1_extra.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "he1_extra.out"), "w").write("\n".join(OUT) + "\n")
