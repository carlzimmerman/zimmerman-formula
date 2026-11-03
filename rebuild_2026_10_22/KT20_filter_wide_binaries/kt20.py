#!/usr/bin/env python3
"""KT20: wide-binary prediction of KT17's filter (xi = 0.55 sqrt(G M / a0)) against plain QUMOND, 1D external-field form, simple nu. Prediction only, nothing graded. python3 kt20.py [--mutate]. kappa = 1/2 FITTED and held fixed; not theory closed."""
import json, math, os, sys
import numpy as np
from scipy.special import erf
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__)); MUT = "--mutate" in sys.argv; OUT = []; RES = {}; fail = 0
def P(s): print(s, flush=True); OUT.append(s)
G, MS, AU = 6.6743e-11, 1.98892e30, 1.495978707e11; A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; GE = (1.9e-10, 2.32e-10); EPS = 0.55
S = np.array([1, 2, 3, 5, 7, 10, 15, 20, 30], float) * 1e3
nu = (lambda y: np.ones_like(np.asarray(y, float))) if MUT else (lambda y: 0.5 + np.sqrt(0.25 + 1 / np.maximum(y, 1e-300)))
def gh(r, M, xi):
    x = r / xi; return G * M / r ** 2 * (erf(x / math.sqrt(2)) - math.sqrt(2 / math.pi) * x * np.exp(-x * x / 2))
def gam(s_au, M, a0, ge, xi):
    r = s_au * AU; gN = G * M / r ** 2; h = gN if xi <= 0 else gh(r, M, xi); return (gN + (nu(np.sqrt(ge * ge + h * h) / a0) - 1) * h) / gN
for foot, a0 in A0.items():
    for M in (1.0, 1.5):
        rM = math.sqrt(G * M * MS / a0); xi = EPS * rM
        for ge in GE:
            gp = gam(S, M * MS, a0, ge, 0.0); gf = gam(S, M * MS, a0, ge, xi); ex = (gf - 1) / np.maximum(gp - 1, 1e-300)
            k = f"{foot}|M{M}|ge{ge:.3g}"; RES[k] = dict(xi_AU=xi / AU, r_M_AU=rM / AU, s_kAU=(S / 1e3).tolist(), gamma_plain=gp.tolist(), gamma_filter=gf.tolist(), excess_ratio=ex.tolist())
            if not MUT:
                f = lambda s: (gam(np.array([s]), M * MS, a0, ge, xi)[0] - 1) / (gam(np.array([s]), M * MS, a0, ge, 0.0)[0] - 1) - 0.5; sh = brentq(f, 50, 1e5); RES[k]["s_half_AU"] = sh
                ok = ex[-1] > 0.95; RES[k]["C2"] = bool(ok)
                rr = S * AU; gN = G * M * MS / rr ** 2; e1 = float(np.max(np.abs(gp - nu(np.sqrt(ge * ge + gN * gN) / a0)) / gp)); fail += e1 > 1e-10
                P(f"[{k}] r_M {rM / AU:.0f} AU, xi {xi / AU:.0f} AU, s_half {sh:.0f} AU; C1 {e1:.1e}; C2 excess ratio at 30 kAU {ex[-1]:.3f} {'PASS' if ok else 'REPORTED (below 0.95)'}")
                P("    s kAU      " + " ".join(f"{s / 1e3:6.0f}" for s in S)); P("    gamma plain " + " ".join(f"{v:6.3f}" for v in gp)); P("    gamma filt  " + " ".join(f"{v:6.3f}" for v in gf)); P("    excess ratio" + " ".join(f"{v:6.3f}" for v in ex))
            else: P(f"[{k}] MUTATE gamma plain max |g-1| {np.max(np.abs(gp - 1)):.1e}, filter {np.max(np.abs(gf - 1)):.1e}")
RES["fail"] = fail; P(f"failed checks: {fail}")
sfx = "_MUTATE" if MUT else ""; open(os.path.join(HERE, f"kt20{sfx}.out"), "w").write("\n".join(OUT) + "\n"); json.dump(RES, open(os.path.join(HERE, f"kt20{sfx}.json"), "w"), indent=1)
sys.exit(1 if (MUT or fail) else 0)
