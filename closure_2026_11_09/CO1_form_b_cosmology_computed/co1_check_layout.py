#!/usr/bin/env python3
"""CO1 check (reported, not a known answer of the criteria; written after the halo-model part ran): co1_hm.py's layout against
independent SI arithmetic and closed forms. Galaxy regime: r_M and r_t in SI, and the cold component's transform by direct
quadrature of the truncated m(x) - 1 profile. Cluster regime: v_vir, f_core and the phantom's cap radius by an SI root-find.
  python3 co1_check_layout.py   -> co1_check_layout.out
kappa = 1/2 FITTED; not theory closed."""
import os, sys, math, io, contextlib, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
LINES = []
_print = print
def print(*a):
    s = " ".join(str(x) for x in a); _print(s, flush=True); LINES.append(s)
from scipy.special import sici
from scipy.integrate import quad
sys.argv = ["x"]
src = open("co1_hm.py").read(); cut = src.index("RES = dict(lane=")
g = {"__file__": os.path.abspath("co1_hm.py"), "__name__": "chk"}
with contextlib.redirect_stdout(io.StringIO()): exec(compile(src[:cut], "co1_hm.py", "exec"), g)
L = g["L"]; layout = g["layout"]; h = g["h"]; FB = g["FB"]
Gsi, Msun, Mpc = 6.6743e-11, 1.98847e30, 3.0856775814913673e22
for foot, a0 in (("canonical", 9.3603e-11), ("alt", 1.1312e-10)):
    X = g["XSH"][foot]
    for lm in (11.0, 12.0):
        i = int(np.argmin(abs(g["LM"] - lm))); hb = L["HB"][i]
        r, M, inf = layout(hb, foot, mode="B")
        # SI: M_b in kg, r_M in m -> Mpc/h
        Mb_si = (1 - FB) * hb["Mta"] / X / h * Msun; rM_si = math.sqrt(Gsi * Mb_si / a0); rM_h = rM_si / Mpc * h; rt_h = math.sqrt(X * (X + 1)) * rM_h
        # cold transform: closed form of the truncated m(x) - 1 profile by direct quadrature in x
        Mb = Mb_si / Msun * h
        for k in (1.0, 3.0):
            f = lambda x: (x / math.sqrt(0.25 + x * x)) * (math.sin(k * rM_h * x) / (k * rM_h * x))
            Uc = Mb * quad(f, 0, math.sqrt(X * (X + 1)), limit=400)[0]
            unc = (FB * hb["Mta"] - Mb)
            # code: total U minus point baryons minus uncondensed (reference-shaped) part
            rR, MR, _ = layout(hb, foot, mode="L"); UL = L["U_of"](rR, MR, np.array([k]))[0] / hb["Mta"]
            Ucode = L["U_of"](r, M, np.array([k]))[0] - Mb - unc * UL
            print(f"{foot:9s} logM {lm}: r_M {rM_h*1e3/h:.3f} kpc (code {inf['rM']*1e3/h:.3f}), r_t {rt_h/h*1e3:.1f} kpc (code {inf['rt']/h*1e3:.1f}); k {k}: U_cold quad {Uc:.5e} code {Ucode:.5e} rel {Ucode/Uc-1:+.1e}")
    # cluster: capped phantom radius by SI root-find for M200m 1e14
    i = int(np.argmin(abs(g["LM"] - 14.0))); hb = L["HB"][i]; r, M, inf = layout(hb, foot, mode="B")
    v = math.sqrt(Gsi * hb["M200c"] / h * Msun / (hb["r200c"] / h * Mpc)) / 1e3
    fc = 0.5 * (1 - (g["VST"][foot] / v) ** 2); E = (1 - fc) * (1 - FB) * hb["M200c"]
    from scipy.optimize import brentq
    def ph(rr):
        mb = float(g["bar_cum"](hb, FB * hb["M200c"], np.array([rr]), hb["r200c"])[0]); mb_si = mb / h * Msun; r_si = rr / h * Mpc
        y = Gsi * mb_si / r_si ** 2 / a0; W = 1.5 * v * v / (1.5 * v * v + 15.0 ** 2)
        return W * mb * (math.sqrt(0.25 + 1 / y) - 0.5)
    rtr = brentq(lambda rr: ph(rr) - E, 1e-3 * hb["r200c"], 3 * hb["r200c"])
    print(f"{foot:9s} cluster logM200m 14: v_vir SI {v:.1f} km/s (code {inf['v_vir']:.1f}); f_core {fc:.4f} (code {inf['f_core']:.4f}); R_trunc/R200c SI {rtr/hb['r200c']:.4f} (code {inf['Rtrunc_over_R200c']:.4f})")

open(os.path.join(HERE, "co1_check_layout.out"), "w").write("\n".join(LINES) + "\n")
