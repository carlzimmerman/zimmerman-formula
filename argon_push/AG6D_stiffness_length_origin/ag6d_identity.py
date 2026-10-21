#!/usr/bin/env python3
"""AG6D Part A: the stiffness term (gamma/2)|grad P|^2, gamma = K L*^2/2, K = 4 pi G, read as the cold medium's EoS.

FROZEN_CRITERIA.md section 2 (b94d6b89b). Tests:
  A1 (sympy)   radial P: vector Laplacian == grad div (exact); toroidal control: div = 0, vector Laplacian != 0.
  A2 (numeric) compact radial profiles: |E_grad - E_div| / E_grad < 1e-6 (difference is a boundary term).
  A3           e = K rho^Gamma: gamma_eff = e''(rho_bar) constant over rho_bar in [1e-30, 1e-18] only for Gamma = 2;
               plus k_J,phys = sqrt(2)/L* for every rho_bar (gamma = 2 pi G L*^2).
  A4           Lane-Emden n=1 first zero = pi (1e-6), R_TF/L* = pi/sqrt2 (1e-6); n=1.5: R ~ M^(-1/3) (1e-3).
MUTATE (AG6D_MUTATE=1): the constant-L* check is run with Gamma = 5/3 instead of 2; it must FAIL -> exit 1.
"""
import json, os, sys
import numpy as np
import sympy as sp
from scipy.integrate import quad, solve_ivp

MUT = os.environ.get("AG6D_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__))
G = 6.67430e-11
PC = 3.0856775814913673e16
out_lines = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    out_lines.append(s)


res = {"lane": "AG6D", "part": "A", "mutate": MUT}

# ---------------- A1: sympy, Cartesian components -------------------------------------------------------------
x, y, z = sp.symbols("x y z", real=True)
r = sp.sqrt(x**2 + y**2 + z**2)
X = (x, y, z)


def vec_lap(F):
    return [sum(sp.diff(Fi, v, 2) for v in X) for Fi in F]


def grad_div(F):
    d = sum(sp.diff(F[i], X[i]) for i in range(3))
    return [sp.diff(d, v) for v in X], d


def grad_sq(F):
    return sum(sp.diff(F[j], X[i])**2 for i in range(3) for j in range(3))


radial_profiles = {"r*exp(-r^2)": r * sp.exp(-r**2), "r^3*exp(-r)": r**3 * sp.exp(-r), "r/(1+r^2)^2": r / (1 + r**2)**2}
rng = np.random.default_rng(20261020)
pts = rng.uniform(0.2, 2.0, size=(6, 3))
a1_ok = True
a1 = {}
for name, p in radial_profiles.items():
    F = [p * v / r for v in X]
    L = vec_lap(F)
    GD, _ = grad_div(F)
    worst = 0.0
    for q in pts:
        sub = dict(zip(X, q))
        for i in range(3):
            lv = float(L[i].subs(sub).evalf(30))
            gv = float(GD[i].subs(sub).evalf(30))
            worst = max(worst, abs(lv - gv) / max(1e-300, abs(lv) + abs(gv)))
    # exact symbolic check on the x component
    exact = sp.simplify(L[0] - GD[0]) == 0
    a1[name] = {"exact_symbolic_x": bool(exact), "worst_numeric_rel": worst}
    a1_ok &= bool(exact) and worst < 1e-12
    P(f"A1 radial {name:14s}: (vecLap - grad div)_x simplifies to 0: {exact}; worst numeric rel diff {worst:.1e}")
# toroidal control: P = f(r) (-y, x, 0)/r
f = r * sp.exp(-r**2)
Ft = [-f * y / r, f * x / r, sp.Integer(0)]
GDt, dt = grad_div(Ft)
Lt = vec_lap(Ft)
div_zero = sp.simplify(dt) == 0
q = dict(zip(X, pts[0]))
lap_val = max(abs(float(Lt[i].subs(q).evalf(30))) for i in range(3))
a1["toroidal"] = {"div_is_zero": bool(div_zero), "vecLap_max_abs_at_point": lap_val}
a1_ok &= bool(div_zero) and lap_val > 1e-6
P(f"A1 toroidal control: div P = 0: {div_zero}; |vector Laplacian| = {lap_val:.3e} (>0: identity is for longitudinal P only)")
res["A1"] = {"pass": a1_ok, **a1}

# ---------------- A2: energies, |grad P|^2 vs (div P)^2, radial ----------------------------------------------
# check the gradient-tensor formula |grad P|^2 = p'^2 + 2 p^2/r^2 symbolically at points, then integrate
rr = sp.symbols("rr", positive=True)
a2 = {}
a2_ok = True
profiles_1d = {
    "r(1-r^2)^2 [r<1]": (rr * (1 - rr**2)**2, 1.0),
    "r^2(1-r)^3 [r<1]": (rr**2 * (1 - rr)**3, 1.0),
    "r*exp(-r^2) [r<12]": (rr * sp.exp(-rr**2), 12.0),
}
for name, (pr, rmax) in profiles_1d.items():
    # symbolic gradient-tensor check in Cartesian at random points
    pc = pr.subs(rr, r)
    F = [pc * v / r for v in X]
    g2 = grad_sq(F)
    dp = sp.diff(pr, rr)
    formula = (dp**2 + 2 * pr**2 / rr**2).subs(rr, r)
    wt = 0.0
    for qq in pts * (0.4 if rmax == 1.0 else 1.0):
        sub = dict(zip(X, qq))
        wt = max(wt, abs(float((g2 - formula).subs(sub).evalf(30))))
    fg = sp.lambdify(rr, (dp**2 + 2 * pr**2 / rr**2) * 4 * sp.pi * rr**2, "numpy")
    fd = sp.lambdify(rr, (dp + 2 * pr / rr)**2 * 4 * sp.pi * rr**2, "numpy")
    Eg = quad(fg, 1e-12, rmax, epsabs=0, epsrel=1e-13, limit=400)[0]
    Ed = quad(fd, 1e-12, rmax, epsabs=0, epsrel=1e-13, limit=400)[0]
    bnd = float((-8 * sp.pi * rr * pr**2).subs(rr, rmax))
    rel = abs(Eg - Ed) / Eg
    ok = rel < 1e-6 and wt < 1e-12
    a2_ok &= ok
    a2[name] = {"E_grad": Eg, "E_div": Ed, "rel_diff": rel, "boundary_term": bnd, "tensor_formula_err": wt}
    P(f"A2 {name:20s}: E_grad {Eg:.10e}  E_div {Ed:.10e}  rel diff {rel:.1e}  (boundary -8pi r p^2 = {bnd:.1e}); "
      f"tensor-formula err {wt:.1e}")
res["A2"] = {"pass": a2_ok, **a2}

# ---------------- A3: uniqueness of Gamma = 2, and the density-independent Jeans length ----------------------
rhob = np.logspace(-30, -18, 121)
a3 = {}


def gamma_eff(Gam, rho, Kp=1.0):
    return Kp * Gam * (Gam - 1) * rho**(Gam - 2)


a3_ok = True
for Gam in (2.0, 4 / 3, 5 / 3, 3.0):
    ge = gamma_eff(Gam, rhob)
    span = float(np.log10(ge.max() / ge.min()))
    third = Gam * (Gam - 1) * (Gam - 2)
    a3[f"Gamma={Gam:.4f}"] = {"log10_span_gamma_eff": span, "e3_coeff": third}
    P(f"A3 Gamma = {Gam:.4f}: gamma_eff = e''(rho_bar) spans {span:.3e} dex over rho_bar 1e-30..1e-18; "
      f"e''' coefficient Gamma(Gamma-1)(Gamma-2) = {third:+.4f}")
    if abs(Gam - 2.0) < 1e-12:
        a3_ok &= (ge.max() / ge.min() - 1) < 1e-12 and third == 0.0
    else:
        a3_ok &= span > 1.0
# Jeans: gamma = 2 pi G L*^2 -> c_s^2 = gamma rho, k_J^2 = 4 pi G rho / c_s^2 = 2/L*^2 for every rho
Lstar = 24.0 * PC
gam = 2 * np.pi * G * Lstar**2
assert abs(gam - 4 * np.pi * G * Lstar**2 / 2) / gam < 1e-15
cs2 = gam * rhob
kJ = np.sqrt(4 * np.pi * G * rhob / cs2)
kJ_err = float(np.max(np.abs(kJ * Lstar / np.sqrt(2) - 1)))
a3_ok &= kJ_err < 1e-12
a3["kJ_times_Lstar_over_sqrt2_minus1_max"] = kJ_err
P(f"A3 Jeans: k_J,phys * L*/sqrt2 - 1 = {kJ_err:.1e} for every rho_bar (density- and epoch-independent Jeans length)")
for rho_msun_pc3 in (0.01, 0.1, 1.0):
    rho = rho_msun_pc3 * 1.98841e30 / PC**3
    P(f"   c_s = sqrt(2 pi G L*^2 rho) at L* = 24 pc, rho = {rho_msun_pc3} Msun/pc^3: {np.sqrt(2*np.pi*G*Lstar**2*rho):.1f} m/s "
      f"(at 1 kpc: {np.sqrt(2*np.pi*G*(1000*PC)**2*rho)/1e3:.2f} km/s)")
res["A3"] = {"pass": bool(a3_ok), **a3}

# ---------------- A4: Lane-Emden ------------------------------------------------------------------------------


def lane_emden(n):
    def rhs(xi, s):
        th, dth = s
        return [dth, -max(th, 0.0)**n - 2 * dth / xi]

    xi0 = 1e-6
    s0 = [1 - xi0**2 / 6 + n * xi0**4 / 120, -xi0 / 3 + n * xi0**3 / 30]
    ev = lambda xi, s: s[0]
    ev.terminal = True
    ev.direction = -1
    sol = solve_ivp(rhs, (xi0, 20), s0, rtol=1e-12, atol=1e-14, events=ev, method="DOP853")
    xi1 = sol.t_events[0][0]
    dth1 = sol.y_events[0][0][1]
    return xi1, dth1


xi1, dth1 = lane_emden(1.0)
err_pi = abs(xi1 - np.pi)
# n=1: alpha^2 = 2 Kp / (4 pi G), Kp = gamma/2 = pi G L*^2 -> alpha = L*/sqrt2, R = xi1 alpha
Kp = gam / 2
alpha = np.sqrt(2 * Kp / (4 * np.pi * G))
R_over_L = xi1 * alpha / Lstar
err_R = abs(R_over_L - np.pi / np.sqrt(2))
P(f"A4 n=1: first zero xi1 = {xi1:.12f} (|xi1 - pi| = {err_pi:.1e}); R_TF/L* = {R_over_L:.10f} vs pi/sqrt2 = {np.pi/np.sqrt(2):.10f}")
P(f"   R_TF = {R_over_L*24:.2f} pc at L* = 24 pc, {R_over_L*1000:.0f} pc at L* = 1 kpc (mass-independent)")
# n = 1.5: R vs M slope at fixed Kp
n15 = 1.5
xi1b, dth1b = lane_emden(n15)
Kp15 = 1.0e7  # arbitrary SI-consistent constant; slope is scale-free


def RM(rhoc, n, xi1, dth1, K):
    al = np.sqrt((n + 1) * K * rhoc**(1 / n - 1) / (4 * np.pi * G))
    return xi1 * al, 4 * np.pi * al**3 * rhoc * (-xi1**2 * dth1)


R1, M1 = RM(1e-20, n15, xi1b, dth1b, Kp15)
R2, M2 = RM(1e-17, n15, xi1b, dth1b, Kp15)
slope15 = np.log(R2 / R1) / np.log(M2 / M1)
R1a, M1a = RM(1e-20, 1.0, xi1, dth1, Kp)
R2a, M2a = RM(1e-17, 1.0, xi1, dth1, Kp)
slope1 = np.log(R2a / R1a) / np.log(M2a / M1a)
P(f"A4 n=1.5: dlnR/dlnM = {slope15:.6f} (expect -1/3); n=1: dlnR/dlnM = {slope1:.2e} (expect 0)")
a4_ok = err_pi < 1e-6 and err_R < 1e-6 and abs(slope15 + 1 / 3) < 1e-3 and abs(slope1) < 1e-9
res["A4"] = {"pass": bool(a4_ok), "xi1_n1": xi1, "R_TF_over_Lstar": R_over_L, "slope_n1.5": slope15, "slope_n1": slope1,
             "xi1_n1.5": xi1b}

# ---------------- verdict + MUTATE ---------------------------------------------------------------------------
Gam_test = 5 / 3 if MUT else 2.0
ge = gamma_eff(Gam_test, rhob)
Lstar_eff = np.sqrt(2 * ge / (4 * np.pi * G))  # gamma = K L*^2 / 2
const_L = float(np.log10(Lstar_eff.max() / Lstar_eff.min()))
const_ok = const_L < 1e-10
P(f"Constant-L* check with Gamma = {Gam_test:.4f}: L*_eff(rho_bar) spans {const_L:.3e} dex -> "
  f"{'CONSTANT' if const_ok else 'NOT CONSTANT'}")
res["constant_Lstar_check"] = {"Gamma": Gam_test, "log10_span": const_L, "constant": const_ok}
allpass = a1_ok and a2_ok and a3_ok and a4_ok and const_ok
res["verdict"] = "IDENTITY HOLDS (longitudinal)" if allpass else "IDENTITY FAILS"
P(f"A1 {a1_ok}  A2 {a2_ok}  A3 {a3_ok}  A4 {a4_ok}  constant-L* {const_ok}")
P(f"VERDICT Part A: {res['verdict']}" + ("  [MUTATE run: failure expected]" if MUT else ""))
with open(os.path.join(HERE, f"ag6d_identity_results{TAG}.json"), "w") as fh:
    json.dump(res, fh, indent=1, default=float)
with open(os.path.join(HERE, f"ag6d_identity{TAG}.out"), "w") as fh:
    fh.write("\n".join(out_lines) + "\n")
sys.exit(0 if allpass else 1)
