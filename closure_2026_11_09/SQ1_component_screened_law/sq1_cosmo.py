#!/usr/bin/env python3
"""SQ1 Q-web (FROZEN_CRITERIA.md 7e8fa69c63): WM1's wm1_cosmo.py executed read-only with in-process patches: a cold component (no
relic), nu -> 1 + (nu - 1) S(z). Graded G: S at the cosmic mean density, x = x0 (1 + z)^3, x0 = rho_bar_chi / rho_screen. Reported C:
S = f_V x S(0.2) for z < 1 (the source's depleted state; f_V from sq1.json), S(mean) above.
    python3 sq1_cosmo.py <G|C> <footing>   -> parts/cosmo_SQ<G|C>_<footing>.json
kappa = 1/2 FITTED; not theory closed; adopts nothing."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
WM1 = os.path.join(REPO, "closure_2026_11_09", "WM1_warm_component_law_baryons"); os.makedirs(os.path.join(HERE, "parts"), exist_ok=True)
MODE, FOOT = sys.argv[1], sys.argv[2]; os.environ["SS1_FOOT"] = FOOT; os.environ["WM1_V"] = "W"
FV = json.load(open(os.path.join(HERE, "sq1.json")))[FOOT]["Q2"]["f_V"] if MODE == "C" else 0.0
def sub(s, o, n):
    assert s.count(o) == 1, o; return s.replace(o, n)
src = open(os.path.join(WM1, "wm1_cosmo.py")).read()
src = sub(src, "y = np.maximum(y, 1e-30); return 0.5 + np.sqrt(0.25 + 1.0 / y)", "y = np.maximum(y, 1e-30); return 1 + (0.5 + np.sqrt(0.25 + 1.0 / y) - 1) * SQ_S(z)")
src = sub(src, 'if V == "W":\n    s5 = open', 'if False:   # SQ1: KA-W2 passed in WM1 with this code unchanged (nu patched here)\n    s5 = open')
src = sub(src, "WP = dict(BASE, omega_cdm=1e-7, N_ncdm=1, m_ncdm=M_EV, T_ncdm=TNCDM, deg_ncdm=1.0, tol_ncdm_bg=1e-10)", "WP = dict(BASE)   # SQ1: cold component (no relic)")
src = sub(src, "onc = float(Mw.Omega_nu) * h * h", "onc = OD   # SQ1: cold")
src = sub(src, 'f"cosmo_{V}_{FOOT}.json"', 'f"cosmo_SQ{SQ_MODE}_{FOOT}.json"')
pre = f'''SQ_MODE = {MODE!r}; SQ_FV = {FV!r}
def SQ_S(z):
    import math as _m
    rs = A0 * (100 * h * 1e3 / 3.0857e22) / (2 * _m.pi * 6.6743e-11 * 2.99792458e8); rhoc = 3 * (100 * h * 1e3 / 3.0857e22) ** 2 / (8 * _m.pi * 6.6743e-11)
    x = OD / h ** 2 * rhoc / rs * (1 + z) ** 3; Sm = 1 / (1 + x * x)
    return (SQ_FV / (1 + 0.04)) if (SQ_MODE == "C" and z < 1) else Sm
'''
ns = {"__file__": os.path.join(HERE, "wm1_cosmo.py"), "__name__": "__main__"}
exec(compile(pre + src, "sq1_patched_wm1_cosmo", "exec"), ns)
