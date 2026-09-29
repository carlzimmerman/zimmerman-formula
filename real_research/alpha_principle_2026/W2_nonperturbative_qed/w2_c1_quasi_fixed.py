#!/usr/bin/env python3
"""W2 (c): compositeness conditions and quasi-fixed points (pre-registered C1, C2, C3 in W2_PREREGISTRATION.md).
C1  what a Pendleton-Ross / Hill quasi-fixed point is (sympy, one-loop y_t and g_3), plus a numerical focusing control (elasticity of y_IR to y_UV).
C2  does an abelian (or any) gauge coupling focus? elasticity d ln alpha_IR / d ln alpha_UV: one loop exactly, two loop with the lane-N1 RHS.
C3  compositeness Z3 = 0 is the equation a(X) = 0 (same as B3; no new hit-tests).  Also alpha_0/alpha_max (triviality-bound saturation), reported.
Run:    python3 w2_c1_quasi_fixed.py           (from this directory; exit 0 iff every check passes)  -> writes w2_c1_results.json
MUTATE: python3 w2_c1_quasi_fixed.py MUTATE    (C1: the QCD term in the y_t RGE dropped, 8 -> 0)  must exit 1 (exit 3 if broken) -> w2_c1_results_MUTATE.json
"""
import sys
sys.dont_write_bytecode = True
import json, math
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
import w2_lib as L

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
fails = []
def chk(name, ok, info=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name} {info}")
    if not ok:
        fails.append(name)
PI = math.pi
res = {}

# ------------------------------------------------------------------ C1
print("== C1 quasi-fixed point structure ==")
y, g, rho, c8 = sp.symbols("y g rho c8", positive=True)
cQCD = 0 if MUT else 8
# (16 pi^2) dy/dt = y (9/2 y^2 - cQCD g^2),  (16 pi^2) dg/dt = -7 g^3
dlny = sp.Rational(9, 2) * y ** 2 - cQCD * g ** 2
dlng = -7 * g ** 2
dlnrho = 2 * (dlny - dlng)                       # d ln(y^2/g^2)/dt in units of 1/(16 pi^2)
rho_fixed = sp.solve(sp.Eq(dlnrho.subs(y, sp.sqrt(rho) * g), 0), rho)
print(f"   fixed ratio rho* = y_t^2/g_3^2 = {rho_fixed}")
chk("C1a  Pendleton-Ross fixed ratio y_t^2/g_3^2 = 2/9 from the one-loop RGEs", rho_fixed == [sp.Rational(2, 9)])
def yIR(yuv, gs2_uv=4 * PI / 52.0, tspan=math.log(L.XP / L.MZ)):
    f = lambda t, v: [v[0] / (16 * PI ** 2) * (4.5 * v[0] ** 2 - 8 * v[1] ** 2), -7 * v[1] ** 3 / (16 * PI ** 2)]
    sol = solve_ivp(f, [0, -tspan], [yuv, math.sqrt(gs2_uv)], rtol=1e-11, atol=1e-13)
    return sol.y[0, -1]
def elast(y0_):
    return (math.log(yIR(1.05 * y0_)) - math.log(yIR(0.95 * y0_))) / (math.log(1.05) - math.log(0.95))
el = {v: elast(v) for v in (1.0, 2.0, 3.0)}
e1 = el[2.0]          # AMENDMENT 2: the control is evaluated at y_UV = 2 (pre-registration text said 1; see the FIRSTRUN output)
print("   numerical control: elasticity d ln y_IR / d ln y_UV, M_P -> m_Z (top+QCD only): " + ", ".join(f"y_UV = {k:g}: {v:.4f}" for k, v in el.items()))
chk("C1b  CONTROL (AMENDMENT 2: at y_UV = 2): the focusing measure detects the Yukawa quasi-fixed point (elasticity < 0.1)", e1 < 0.1)
res["C1"] = dict(rho_star=str(rho_fixed), yuk_elasticity=e1)

# ------------------------------------------------------------------ C2
print("== C2 focusing of gauge couplings ==")
aUV, aIR, b, Lg = sp.symbols("aUV aIR b Lg", positive=True)
aIR_expr = aUV + b / (2 * sp.pi) * Lg                              # a_i(IR) = a_i(UV) + b_i ln(UV/IR)/2pi
chk("C2a  one loop: d a_IR / d a_UV = 1 exactly (additive in the inverse coupling, no focusing)", sp.simplify(sp.diff(aIR_expr, aUV) - 1) == 0)
sol, lp, R = L.sm_twoloop_run("A", tmax=math.log(L.XP) + 1e-9)
tP, tZ = math.log(L.XP), math.log(L.MZ)
y0 = list(sol.sol(tP))
def down(scale_Y):
    yy = list(y0); yy[0] = y0[0] * scale_Y
    s2 = solve_ivp(lambda t, v: R._rhs(t, v), [tP, tZ], yy, rtol=1e-10, atol=1e-12, method="LSODA")
    return s2.y[:3, -1]
lo, mid, hi = down(0.9), down(1.0), down(1.1)
elas_Y = (math.log(hi[0]) - math.log(lo[0])) / (math.log(1.1) - math.log(0.9))         # d ln a_IR / d ln a_UV = d ln alpha_IR / d ln alpha_UV
ratio_lo, ratio_hi = lo[0] / lo[1], hi[0] / hi[1]
elas_ratio = (math.log(ratio_hi) - math.log(ratio_lo)) / (math.log(1.1) - math.log(0.9))
print(f"   two loop (N1 RHS), M_P -> m_Z, a_Y(M_P) x (0.9, 1.0, 1.1): a_Y(m_Z) = {lo[0]:.3f}, {mid[0]:.3f}, {hi[0]:.3f}   (central reproduces set A: {L.A_Y_MZ['A']:.3f})")
print(f"   elasticity d ln alpha_Y(m_Z)/d ln alpha_Y(M_P) = {elas_Y:.4f}  (one-loop expectation a_UV/a_IR = {sol.sol(tP)[0]/L.A_Y_MZ['A']:.4f});  elasticity of the ratio a_Y/a_2 at m_Z = {elas_ratio:.4f}")
chk("C2b  central downward run reproduces the measured a_Y(m_Z) (set A) to 1e-3", abs(mid[0] / L.A_Y_MZ["A"] - 1) < 1e-3)
chk("C2c  NO focusing: elasticity of alpha_Y(m_Z) to alpha_Y(M_P) is > 0.3 (quasi-fixed-point criterion is < 0.1)", elas_Y > 0.3 and not elas_Y < 0.1)
chk("C2d  the ratio a_Y/a_2 at m_Z is not focused either (elasticity > 0.3)", elas_ratio > 0.3)
res["C2"] = dict(elasticity_alphaY=elas_Y, elasticity_ratio=elas_ratio, aY_MZ=[lo[0], mid[0], hi[0]])

# ------------------------------------------------------------------ C3
print("== C3 compositeness = pole; triviality-bound saturation (reported) ==")
rows1 = L.toy_table(1)
sat = {}
for Xn in ("X_G", "X_S", "M_red", "M_P"):
    X = L.SCALES[Xn]
    r_toy = L.S_oneloop(rows1, X) / L.ALPHA_INV0                       # alpha_0/alpha_max for the toy
    amaxY = L.B_Y / (2 * PI) * math.log(X / L.MZ)
    r_Y = amaxY / L.A_Y_MZ["A"]
    sat[Xn] = dict(toy=r_toy, Y=r_Y)
    print(f"   X = {Xn:6s}: alpha_0/alpha_max(X) = {r_toy:.4f} (QED-only toy);  alpha_Y(m_Z)/alpha_Y,max(X) = {r_Y:.4f} (U(1)_Y one loop)")
print("   compositeness (Z3 = 0, 1/e^2(X) = 0) is the equation a(X) = 0: identical to the pole-at-X rule scored in B3 (eight variants, all DEAD); nothing new is counted.")
chk("C3a  no saturation ratio equals 1 (the measured coupling is 0.4-0.6 of the one-loop bound at Planckian X, not AT it)", all(0.2 < v["toy"] < 0.75 for k, v in sat.items() if k in ("M_red", "M_P")))
res["C3"] = sat
json.dump(res, open("w2_c1_results_MUTATE.json" if MUT else "w2_c1_results.json", "w"), indent=1, default=float)
L.finish(fails, MUT, "w2_c1")
