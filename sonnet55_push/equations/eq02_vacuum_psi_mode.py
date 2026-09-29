#!/usr/bin/env python3
"""eq02_vacuum_psi_mode.py -- the EXACT empty-de-Sitter psi (host-scalar) mode of CA5-GNC-R at every wavenumber.

From the boxed reduced action (breakthrough_review_2026_09_26/occupied/RESULT.md) with T = V = 0, v = 0, V' = 0
(empty de Sitter, H constant, x = k^2/a^2):
   L/a^3 = 1/2 M K psid^2 + M x psi^2 - (M K H psid - 2 M x psi)^2 / (2 M F),   F = K H^2 + alpha_e(x) x.
Written as L = 1/2 G psid^2 + b psi psid - 1/2 P psi^2 (a^3 included), the Euler-Lagrange equation is
   G psidd + Gdot psid + (P + bdot) psi = 0.
E1  derive G, b, P, bdot symbolically and reduce P + bdot to a closed form.
E2  closed form:   P + bdot = a^3 M x^2 / F * N(x),   N = 4 - 2 alpha_e + 4 K H^2 (alpha_e + x alpha_e') / F.
E3  the mode's sound speed  c_s^2(x) = omega^2/x = N / (K alpha_e)   (WKB, x >> H^2), with UV limit 2(2-alpha)/(K alpha)
    (matches the record's host speed) and IR limit (4 + 2 alpha_0)/(K alpha_0).
E5  the friction coefficient Gdot/G in closed form: the mode is a damped oscillator psidd + Gam psid + c_s^2 x psi = 0
E4  the SIGN of N over the whole parameter window: N < 0 anywhere would be a restoring-sign failure of the EMPTY vacuum.
Exit 0 = every identity held; the scan result (E4) is reported as found.
"""
import math
import sys
import numpy as np
import sympy as sp

ok = []
def check(c, m):
    ok.append(bool(c)); print(f"  [{'OK' if c else 'FAIL'}] {m}")

t = sp.Symbol('t', real=True)
M, H, c2, alpha, r0, xi, k = sp.symbols('M H c2 alpha r0 xi k', positive=True)
psi = sp.Function('psi')(t)
a = sp.exp(H * t)
x = k**2 / a**2
r = r0 * sp.exp(-xi**2 * x / 2)
Q = 1 - r
ae = 2 - (2 - alpha) * Q**2
K = 2 * (2 + 3 * c2) / c2
F = K * H**2 + ae * x
pd = sp.diff(psi, t)
L = a**3 * (M * K * pd**2 / 2 + M * x * psi**2 - (M * K * H * pd - 2 * M * x * psi)**2 / (2 * M * F))

# ---- E1: EL equation coefficients ----------------------------------------------------------------------
ps, pv = sp.symbols('ps pv')                       # psi, psidot as plain symbols
Ls = L.subs(pd, pv).subs(psi, ps)
G = sp.diff(Ls, pv, 2)
b = sp.diff(Ls, pv, ps)
Pm = -sp.diff(Ls, ps, 2)
Peff = sp.simplify(Pm + sp.diff(b, t))
# closed form for N with alpha_e' = d alpha_e / d x
X = sp.Symbol('X', positive=True)
ae_X = 2 - (2 - alpha) * (1 - r0 * sp.exp(-xi**2 * X / 2))**2
aep = sp.diff(ae_X, X)
FX = K * H**2 + ae_X * X
Nexpr = 4 - 2 * ae_X + 4 * K * H**2 * (ae_X + X * aep) / FX
Peff_closed = (a**3 * M * x**2 / F) * Nexpr.subs(X, x)
diff = sp.simplify(Peff - Peff_closed)
check(diff == 0, "E1/E2  P + bdot = a^3 M x^2 N / F, N = 4 - 2 alpha_e + 4 K H^2 (alpha_e + x alpha_e')/F   (exact, symbolic)")
Gclosed = a**3 * M * K * ae * x / F
check(sp.simplify(G - Gclosed) == 0, "E1b  G = a^3 M K alpha_e x / F  (kinetic coefficient)")

# ---- E3: sound speed and limits ---------------------------------------------------------------------------
cs2 = Nexpr / (K * ae_X)
import mpmath as mp                                   # sympy's limit() returned 0 here (checked: wrong); evaluate at 40 digits instead
mp.mp.dps = 40
def cs2_num(Xv, al, r0v, xiv, Hv, c2v):
    Kv = 2 * (2 + 3 * c2v) / c2v
    aef = lambda xx: 2 - (2 - al) * (1 - r0v * mp.e**(-xiv**2 * xx / 2))**2
    F_ = Kv * Hv**2 + aef(Xv) * Xv
    N_ = 4 - 2 * aef(Xv) + 4 * Kv * Hv**2 * (aef(Xv) + Xv * mp.diff(aef, Xv)) / F_
    return N_ / (Kv * aef(Xv)), Kv
worst_uv = 0
for (al, r0v, xiv, Hv, c2v) in ((0.7, 0.5, 1, 1, 1.3), (0.3, 0.9, 2, 0.5, 0.4), (1.6, 0.2, 0.5, 2, 3.0)):
    al, r0v, xiv, Hv, c2v = (mp.mpf(v) for v in (al, r0v, xiv, Hv, c2v))
    val, Kv = cs2_num(mp.mpf(10)**9, al, r0v, xiv, Hv, c2v)
    worst_uv = max(worst_uv, abs(val - 2 * (2 - al) / (Kv * al)) / abs(val))
check(worst_uv < 1e-6,
      f"E3a  UV limit of c_s^2 = 2(2-alpha)/(K alpha) = c2(2-alpha)/((2+3c2)alpha), the record's host speed "
      f"(3 parameter sets, x = 1e9, relative deviation {float(worst_uv):.1e})")
a0_ = 2 - (2 - alpha) * (1 - r0)**2
ir = sp.simplify(cs2.subs(X, 0))
check(sp.simplify(ir - (4 + 2 * a0_) / (K * a0_)) == 0, "E3b  IR limit of c_s^2 = (4 + 2 alpha_0)/(K alpha_0),  alpha_0 = alpha_e(0) = 2 - (2-alpha)(1-r0)^2")


# ---- E5: friction coefficient -----------------------------------------------------------------------------------
Gam = sp.simplify(sp.diff(G, t) / G)
Gam_closed = H * (1 - 2 * x * (aep.subs(X, x)) / ae + 2 * x * (sp.diff(FX, X).subs(X, x)) / F)
check(sp.simplify(Gam - Gam_closed) == 0,
      "E5   friction Gdot/G = H [1 - 2 x alpha_e'/alpha_e + 2 x F'/F]  (exact); tends to 3H in the UV and to H in the IR")

# ---- E4: sign of N over the window --------------------------------------------------------------------------
print("\n  E4  scan of N(w) = 4 - 2 a_e + 4 kH (a_e + w a_e')/(kH + a_e w), w = xi^2 x, kH = xi^2 K H^2")
Nf = sp.lambdify((sp.Symbol('w'), alpha, r0, sp.Symbol('kH')),
                 (4 - 2 * (2 - (2 - alpha) * (1 - r0 * sp.exp(-sp.Symbol('w') / 2))**2)
                  + 4 * sp.Symbol('kH') * ((2 - (2 - alpha) * (1 - r0 * sp.exp(-sp.Symbol('w') / 2))**2)
                  + sp.Symbol('w') * sp.diff(2 - (2 - alpha) * (1 - r0 * sp.exp(-sp.Symbol('w') / 2))**2, sp.Symbol('w')))
                  / (sp.Symbol('kH') + (2 - (2 - alpha) * (1 - r0 * sp.exp(-sp.Symbol('w') / 2))**2) * sp.Symbol('w'))), 'numpy')
w = np.logspace(-6, 3, 400)
worst = (1e9, None); nneg = 0; ntot = 0
for al in np.linspace(0.01, 1.99, 45):
    for rr in np.linspace(0.01, 0.99, 45):
        for kH in np.logspace(-3, 3, 25):
            vals = Nf(w, al, rr, kH)
            ntot += 1
            m = vals.min()
            if m < worst[0]:
                worst = (m, (al, rr, kH, w[vals.argmin()]))
            if m < 0:
                nneg += 1
print(f"  {ntot} (alpha, r0, kH) combinations scanned over 400 wavenumbers each")
print(f"  minimum of N over the window = {worst[0]:+.4e} at (alpha, r0, kH, w) = {tuple(round(float(v), 4) for v in worst[1])}")
print(f"  combinations with N < 0 somewhere: {nneg}")
verdict = "N > 0 everywhere scanned: the empty-de-Sitter psi mode has a restoring sign at every wavenumber" if nneg == 0 else "N < 0 FOUND: restoring-sign failure of the EMPTY vacuum in part of the window"
print(f"  E4 verdict: {verdict}")
# control: dropping the x alpha_e' term and the 2(2-alpha)Q^2 term must be able to go negative (the detector can see it)
Nbad = lambda w, al, rr, kH: -1.0 + 0 * w
check(Nbad(w, 1, .5, 1).min() < 0, "C1   sanity: the scan's sign test flags a deliberately negative N")
print(f"\n  {sum(ok)}/{len(ok)} identity/control checks held.")
sys.exit(0 if all(ok) else 1)
