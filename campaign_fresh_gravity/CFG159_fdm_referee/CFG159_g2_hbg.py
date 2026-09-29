#!/usr/bin/env python3
"""
CFG159_g2_hbg -- G2 formula check (frozen line P8): linear-growth suppression of an ultralight scalar with the Hu-Barkana-Gruzinov (2000)
transfer-function fit, evaluated from the published form (recollection):
    T_F(x) = cos(x^3)/(1 + x^8),  x = 1.61 m22^(1/18) k / k_J,eq,  k_J,eq = 9 m22^(1/2) /Mpc,  m22 = m / 1e-22 eV,  k comoving in /Mpc.
NOT independent of CFG119 (same fit).  MUTATE=1: the denominator exponent 8 -> 6 (the fit's shape changed): the m_min line must move; exit 1.
Exit 0 iff all P8 lines pass (main) / exit 1 when the control bites (MUTATE).
"""
import os, sys, math, json
import numpy as np
from scipy.optimize import brentq
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("MUTATE", "") == "1"
BASE = "CFG159_g2_hbg" + ("_MUTATE" if MUT else "")
EXP = 6 if MUT else 8
lines = []
def P(s=""):
    print(s); lines.append(s)
def T(x): return math.cos(x**3)/(1 + x**EXP)
def xk(m_eV, k):
    m22 = m_eV/1e-22
    return 1.61*m22**(1/18)*k/(9*m22**0.5)
def k_at(m_eV, target):
    """smallest k [1/Mpc] with T_F = target (first crossing from above)"""
    f = lambda k: T(xk(m_eV, k)) - target
    ks = np.logspace(-2, 4, 4000); v = [f(k) for k in ks]
    for i in range(len(ks) - 1):
        if v[i] > 0 >= v[i+1]: return brentq(f, ks[i], ks[i+1], xtol=1e-14, rtol=1e-14)
    return float("nan")
checks = []
def check(name, detail, ok): checks.append((name, ok)); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
P(f"CFG159 G2 formula check   mode = {'MUTATE (x^6)' if MUT else 'main'}")
ms = [1e-23, 1e-22, 1e-21, 1e-20]
kh = [k_at(m, 0.5) for m in ms]; k95 = [k_at(m, 0.95) for m in ms]
P("  m [eV]      k(T=1/2)   k(T=0.95)   T_F(30/Mpc)")
for m, a, b in zip(ms, kh, k95): P(f"  {m:.0e}   {a:8.3f}   {b:8.3f}   {T(xk(m, 30.0)):.4f}")
rd = lambda got, want, tol: all(abs(g/w - 1) <= tol for g, w in zip(got, want))
check("half-amplitude scale k_1/2 = 1.6, 4.5, 12.5, 34.8 /Mpc within 2%", ", ".join(f"{x:.3f}" for x in kh), rd(kh, [1.6, 4.5, 12.5, 34.8], 0.02))
check("T_F >= 0.95 up to k = 1.2, 3.5, 9.7, 26.9 /Mpc within 3%", ", ".join(f"{x:.3f}" for x in k95), rd(k95, [1.2, 3.5, 9.7, 26.9], 0.03))
# POST-HOC (undeclared; does not re-score the frozen line above): the half-POWER scale (T_F^2 = 1/2) and HBG's quoted closed form 4.5 m22^(4/9)
kp = [k_at(m, 0.5**0.5) for m in ms]; kc = [4.5*(m/1e-22)**(4/9) for m in ms]
P("  post-hoc: k(T_F^2 = 1/2) = " + ", ".join(f"{x:.3f}" for x in kp) + "  (vs README 1.6, 4.5, 12.5, 34.8: " + ", ".join(f"{100*(a/b-1):+.1f}%" for a, b in zip(kp, [1.6, 4.5, 12.5, 34.8])) + ")")
P("  post-hoc: 4.5 m22^(4/9) = " + ", ".join(f"{x:.3f}" for x in kc) + "  (HBG's quoted closed form; equals the README numbers)")
g = lambda lm: T(xk(10**lm, 30.0)) - 0.95
mmin = 10**brentq(g, -23.0, -18.0, xtol=1e-14)
check("m_min(T_F(30/Mpc) >= 0.95) = 1.28e-20 eV within 3%", f"{mmin:.4e} eV", abs(mmin/1.28e-20 - 1) <= 0.03)
t30 = T(xk(1e-20, 30.0))
check("T_F(30/Mpc, m = 1e-20) = 0.897 +- 0.005 (10.3% low)", f"{t30:.4f} ({100*(1-t30):.1f}% low)", abs(t30 - 0.897) <= 0.005)
rc = 0 if all(o for _, o in checks) else 1
if MUT:
    P(f"MUTATE: control {'BITES' if rc else 'DOES NOT BITE'}")
P("kappa = 1/2 is fitted; a formula check only, shared with CFG119; nothing here says the data favour either model.")
with open(os.path.join(HERE, BASE + ".out"), "w") as f: f.write("\n".join(lines) + "\n")
with open(os.path.join(HERE, BASE + "_results.json"), "w") as f:
    json.dump(dict(k_half=kh, k_halfpower=kp, k_closed=kc, k95=k95, m_min=mmin, T30=t30, checks=[dict(name=n, ok=o) for n, o in checks], exit_code=rc), f, indent=1)
sys.exit(rc)
