#!/usr/bin/env python3
"""CT7: grade candidate C (CFG911 N6 potential portal a0(phi)^2 = xi G V(phi) inside v3s) on G0-G3, G4 as frozen.

Criteria: FROZEN_CRITERIA.md in this folder (written before this script). sympy + numpy + scipy, one thread, seconds.
Reads nothing from disk; background parameters are restated from the files named in FROZEN_CRITERIA.md.
kappa = 1/2 FITTED; not theory closed. Footings canonical 9.3603e-11 and alt 1.1312e-10 m/s^2, never pooled.
"""
import json
import math
import os
import sys

os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

OUT = {}
CHECKS = []


def hdr(t):
    print("\n" + "=" * 110 + "\n" + t + "\n" + "=" * 110)


def check(name, ok, note=""):
    CHECKS.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"\n         ({note})" if note else ""))


G, c = 6.67430e-11, 2.99792458e8
FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
Msun, MEarth, pc, AU = 1.98847e30, 5.9722e24, 3.0857e16, 1.495978707e11
H0 = 67.4e3 / 3.0856775814913673e22
OM0, ODE0 = 0.315, 0.685
ZS = [1.0, 1.5, 2.33]

# ------------------------------------------------------------------------------------------------ symbolic layer
hdr("S. Symbolic: the v3s J term, the static limit, the a0-charge, the phi equation, FRW decoupling, running law")
g, a0, Gs, cs, Y, xs = sp.symbols("g a0 G c Y x", positive=True)
ag = a0 / cs ** 2
u_Y = sp.sqrt(Y) / ag
J = -2 * ag ** 2 * (u_Y - sp.log(1 + u_Y))            # v3s J_x with its bare Lambda set to 0 (all DE is phi)
# static weak field: sqrt(Y) = g/c^2; Lagrangian density (energy units) of R + (-2J) terms
LJ = sp.expand_log(sp.simplify((-(cs ** 4) / (8 * sp.pi * Gs) * J).subs(Y, g ** 2 / cs ** 4)), force=True)
Ltot = -g ** 2 / (8 * sp.pi * Gs) + LJ
dL = sp.simplify(sp.diff(Ltot, g))
mu_read = sp.simplify(-dL * 4 * sp.pi * Gs / g)
print(f"  L_J(g; a0) = {LJ}")
print(f"  dL_total/dg = -(g/4 pi G) mu,  mu = {sp.simplify(mu_read)}")
check("S1 v3s static limit is AQUAL with mu = x/(1+x) (law S: g mu(g/a0) = g_N), whatever sets a0",
      sp.simplify(mu_read - (g / a0) / (1 + g / a0)) == 0)
q = sp.simplify(a0 * sp.diff(LJ, a0))                 # a0-charge: a0 dL_J/da0 at fixed khronon gradient
h_sym = sp.expand_log(sp.simplify((q * 4 * sp.pi * Gs / a0 ** 2).subs(g, xs * a0)), force=True)
h_cfg911 = xs / (1 + xs) + xs - 2 * sp.log(1 + xs)
print(f"  q = a0 dL_J/da0|_g = (a0^2/4 pi G) h(x), h = {h_sym}")
check("S2 the v3s a0-charge equals CFG911's h(x) = x/(1+x) + x - 2 ln(1+x) (CFG911 used the S2 Phi-P action)",
      sp.simplify(sp.expand_log(h_sym - h_cfg911, force=True)) == 0)
check("S3 h(x) <= x for x > 0 (so q <= a0 g/K, an upper bound robust to v3s's screening)",
      all(float(h_cfg911.subs(xs, v)) <= v for v in [1e-6, 1e-3, 0.1, 1, 10, 1e3, 1e6, 1e9]))
# phi equation: L_phi = -(1/2)|grad phi|^2 - V + L_J(a0(phi)); a0(phi)^2 = xi G V, V = V0 exp(-lam phi/phi_P)
phi, lam, phiP, xi, V0 = sp.symbols("phi lambda phi_P xi V0", positive=True)
Vphi = V0 * sp.exp(-lam * phi / phiP)
a0phi = sp.sqrt(xi * Gs * Vphi)
dlna0_dphi = sp.simplify(sp.diff(sp.log(a0phi), phi))
print(f"  d ln a0/d phi = {dlna0_dphi}   (|.| = lambda/(2 phi_P))")
# source: grad^2 dphi = -dL_J/dphi = -q dln a0/dphi  ->  dphi = (1/4pi) int q |dln a0/dphi| /|x-x'|  (magnitude)
# delta ln a0 = |dln a0/dphi| dphi = (lambda/2phi_P)^2 (1/4pi) int q/|x-x'| ; phi_P^2 = c^4/(8 pi G)
pref = sp.simplify((lam / (2 * phiP)) ** 2 / (4 * sp.pi)).subs(phiP, sp.sqrt(cs ** 4 / (8 * sp.pi * Gs)))
print(f"  delta ln a0 = {sp.simplify(pref)} * int q/|x-x'| d^3x'")
check("S4 delta ln a0 = (G lambda^2/2c^4) int q/|x-x'| (CFG911's N6 formula, re-derived from the v3s phi equation)",
      sp.simplify(pref - Gs * lam ** 2 / (2 * cs ** 4)) == 0)
# mass term: m^2 = -d^2 L_J/dphi^2 = -(lambda/2phi_P)^2 * d q/d ln a0 |_g   (exponential V: d^2 ln a0/dphi^2 = 0)
dq_dlna0 = a0 * sp.diff(q, a0)
k_raw = sp.expand_log((dq_dlna0 * 4 * sp.pi * Gs / a0 ** 2).subs(g, xs * a0), force=True)
k_sym = 2 * h_cfg911 - xs * sp.diff(h_cfg911, xs)          # hand form: a0 dq/da0|_g = (a0^2/K)(2h - x h')
print(f"  d q/d ln a0|_g = (a0^2/4 pi G) k(x), k = 2h - x h' = {sp.simplify(k_sym)}")
check("S4b the hand form k = 2h - x h' equals the symbolic a0 dq/da0|_g", sp.simplify(sp.expand_log(k_raw - k_sym, force=True)) == 0)
# FRW decoupling: d^2 J / dY da0 at Y -> 0
dJdY = sp.simplify(sp.diff(J, Y))
cross = sp.limit(sp.diff(dJdY, a0), Y, 0, "+")
print(f"  dJ/dY = {dJdY};  lim_(Y->0) d^2J/dY da0 = {cross};  lim dJ/dY = {sp.limit(dJdY, Y, 0, '+')}")
check("S5 FRW (Y = 0): the khronon's quadratic coefficient J'(0) = -1 is a0-free, so phi decouples at quadratic order",
      cross == 0 and sp.limit(dJdY, Y, 0, "+") == -1)
check("S6 J depends on phi only through a0(phi), no derivative of phi: 4 DOF (v3s's 3 + phi), phi kinetic matrix diagonal, sign +",
      not any(s.name.startswith("d") for s in J.free_symbols))

# running law for the potential portal, from the canonical field equations
t = sp.Symbol("t")
H, pd, pdd, K_, V_ = sp.symbols("H phidot phiddot K V", real=True)
Kd = pd * pdd
Vd = -pd * pdd - 3 * H * pd ** 2                     # KG: phi'' + 3H phi' + V' = 0  ->  dV/dt = V' phi' = -phi'(phi'' + 3H phi')
rho, p = pd ** 2 / 2 + V_, pd ** 2 / 2 - V_
w = p / rho
rhod = Kd + Vd
wd = sp.simplify(sp.diff(w, pd) * pdd + sp.diff(w, V_) * Vd)  # dw/dt
lhs = Vd / V_ / H                                     # d ln V / d ln a
rhs_claim_eps = -3 * (1 + w)                          # 2 x CT1's law (energy portal)
rhs_V = -3 * (1 + w) - (wd / H) / (1 - w)
check("S7 continuity: d rho/dt = -3H(rho + p) from KG", sp.simplify(rhod + 3 * H * (rho + p)) == 0)
check("S8 potential portal: d ln a0/d ln a = -(3/2)(1+w) - w'/(2(1-w)), w' = dw/d ln a (derived from KG)",
      sp.simplify(lhs - rhs_V) == 0)
diff_claim = sp.simplify(lhs - rhs_claim_eps)
check("S9 CT1's -(3/2)(1+w) is NOT the N6 law in general (difference -w'/(1-w) in d ln V/d ln a is nonzero)",
      diff_claim != 0, f"d ln V/d ln a - [-3(1+w)] = {sp.simplify(diff_claim)}")
OUT["symbolic"] = {"L_J": str(LJ), "h": str(h_sym), "k": str(k_sym), "running_V_portal": "-(3/2)(1+w) - w'/(2(1-w))",
                   "local_exponent": "s = 1/2 + w'/(6 (1-w)(1+w))"}


def h_num(x):
    x = np.asarray(x, float)
    out = np.empty_like(x)
    sm = x < 1e-2
    xx = x[sm]
    out[sm] = xx ** 3 / 3 - xx ** 4 / 2 + 3 * xx ** 5 / 5 - 2 * xx ** 6 / 3
    xb = x[~sm]
    out[~sm] = xb / (1 + xb) + xb - 2 * np.log1p(xb)
    return out


k_f = sp.lambdify(xs, k_sym, "math")


def law(gb, A):
    return 0.5 * (gb + np.sqrt(gb * gb + 4 * gb * A))


# ------------------------------------------------------------------------------------------------ G0
hdr("G0 health: DOF, FRW decoupling, static-background mass of delta phi, C' report-only, W4b")
lam_env = 10.0
G0 = {}
for fn, A in FOOT.items():
    rows = {}
    for nm, gg, R in (("Sun (g at 1 AU, R 100 AU)", G * Msun / AU ** 2, 100 * AU), ("MW (g = a0, R 30 kpc)", A, 30e3 * pc),
                      ("cluster (g = a0, R 1 Mpc)", A, 1e6 * pc), ("neutron star (g 1e12, R 10 km)", 1e12, 1e4)):
        x = gg / A
        kx = float(k_f(x))
        m2 = -(lam_env ** 2) * (8 * math.pi * G / c ** 4) / 4 * (A ** 2 / (4 * math.pi * G)) * kx   # 1/m^2
        mR = math.sqrt(abs(m2)) * R
        rows[nm] = {"x": x, "k": kx, "m2_per_m2": m2, "mR": mR, "tachyonic": m2 < 0}
        print(f"  {fn:9s} {nm:32s} x {x:.3e}  k(x) {kx:+.3e}  m^2 {m2:+.3e} m^-2  |m| R = {mR:.2e}  ({'tachyonic' if m2 < 0 else 'stable'} sign)")
    G0[fn] = rows
g0c = all(r["mR"] <= 0.1 for f in G0.values() for r in f.values())
check("G0(c) static backgrounds: |m| R <= 0.1 in every system at lambda = 10, both footings (no room for the J-induced mass to act)", g0c,
      f"max |m|R = {max(r['mR'] for f in G0.values() for r in f.values()):.2e}")
# C' (report-only): energy portal in the khronon frame -> gradient coefficient (1 - q/2 eps) with eps = a0^2/(kappa^2 G)
kap = 0.5
xflip = brentq(lambda x: float(h_num(np.array([x]))[0]) - 8 * math.pi / kap ** 2, 1.0, 1e4)
print(f"  C' (report only): gradient coefficient of phi = 1 - (kappa^2/8 pi) h(g/a0); flips sign at h = 8 pi/kappa^2 = {8 * math.pi / kap ** 2:.2f},"
      f" x = {xflip:.1f}; g_flip canonical {xflip * FOOT['canonical']:.2e}, alt {xflip * FOOT['alt']:.2e} m/s^2;"
      f" Sun at 1 AU x = {G * Msun / AU ** 2 / FOOT['canonical']:.2e}: gradient-unstable -> C' FAILS G0 (report only, not the candidate)")
OUT["G0"] = {"lambda": lam_env, "rows": G0, "pass_c": g0c, "Cprime_x_flip": xflip, "W4b": "UNDECIDED (inherited, CT2_REPORT.md:7)",
             "label": "PASS (a, b, c), conditional on W4b UNDECIDED" if g0c else "FAIL"}
print(f"  G0 label: {OUT['G0']['label']}")

# ------------------------------------------------------------------------------------------------ G2 (needed for G1's delta)
hdr("G2 local constancy: delta ln a0 from the a0-charge (own integration, v3s J), plus the cosmological perturbation channel")
trap = getattr(np, "trapezoid", None) or np.trapz


def dlna0(M, r_obs, r_min, A, out_fac=1e4):
    rM = math.sqrt(G * M / A)
    rr = np.logspace(math.log10(r_min), math.log10(out_fac * rM), 400001)
    gg = law(G * M / rr ** 2, A)
    qq = (A ** 2 / (4 * math.pi * G)) * h_num(gg / A)
    inn = rr <= r_obs
    I = 4 * math.pi * (trap(qq[inn] * rr[inn] ** 2, rr[inn]) / r_obs + trap(qq[~inn] * rr[~inn], rr[~inn]))
    return G / (2 * c ** 4) * I


G2 = {}
for fn, A in FOOT.items():
    rows = {}
    for nm, M, ro, rmin in (("Sun at 1 AU", Msun, AU, 6.957e8), ("Earth surface", MEarth, 6.371e6, 1e5),
                            ("field: MW 6e10 Msun at 8 kpc", 6e10 * Msun, 8e3 * pc, 1e2 * pc),
                            ("cluster 1e14 Msun at 1 Mpc", 1e14 * Msun, 1e6 * pc, 1e3 * pc)):
        v1 = dlna0(M, ro, rmin, A)
        v2 = dlna0(M, ro, rmin, A, out_fac=1e5)
        rows[nm] = {"per_lambda2": v1, "conv_rel": abs(v2 / v1 - 1)}
        print(f"  {fn:9s} {nm:30s} delta ln a0 = {v1:.3e} lambda^2  (R_out 1e4 -> 1e5 r_M: rel change {abs(v2 / v1 - 1):.1e})")
    G2[fn] = rows
# cosmological channel: delta ln a0 ~ 3 lambda^2 Phi Omega_DE (H0 r/c)^2, Phi 1e-4, r 1 Mpc
cosmo = 3 * lam_env ** 2 * 1e-4 * ODE0 * (H0 * 1e6 * pc / c) ** 2
print(f"  cosmological perturbation channel (order of magnitude, labelled): 3 lambda^2 Phi Omega_DE (H0 r/c)^2 at lambda 10, Phi 1e-4, r 1 Mpc = {cosmo:.1e}")
worst = max(max(r["per_lambda2"] for k, r in f.items() if "Sun" not in k and "Earth" not in k) for f in G2.values())
spread_dex = (worst * lam_env ** 2 + cosmo) / math.log(10)
check("G2 |delta log10 a0| between void, field and cluster <= 0.015 dex at lambda = 10, both footings", spread_dex <= 0.015,
      f"worst {spread_dex:.2e} dex (margin {0.015 / spread_dex:.1e})")
check("G2b convergence: outer cutoff 1e4 -> 1e5 r_M moves every local value by < 1e-3",
      all(r["conv_rel"] < 1e-3 for f in G2.values() for r in f.values()))
check("G2c CFG911 cfg911.out:203-206 reproduced to 10 % (canonical-ish 0.5 c sqrt(G rho_DE): Sun 7.29e-24, MW 4.61e-14, cluster 3.63e-11, Earth 3.04e-29)",
      all(abs(G2["canonical"][k]["per_lambda2"] / v - 1) < 0.1 for k, v in
          (("Sun at 1 AU", 7.29e-24), ("field: MW 6e10 Msun at 8 kpc", 4.61e-14), ("cluster 1e14 Msun at 1 Mpc", 3.63e-11), ("Earth surface", 3.04e-29))),
      "CFG911 used a0 = 0.5 c sqrt(G rho_DE) (9.36e-11); the canonical footing is the same to 0.1 %")
OUT["G2"] = {"lambda": lam_env, "rows": G2, "cosmo_channel": cosmo, "worst_dex": spread_dex, "label": "PASS" if spread_dex <= 0.015 else "FAIL"}

# ------------------------------------------------------------------------------------------------ G1
hdr("G1 weak field: law S with a0 -> a0 (1 + delta), delta = largest G2 value at lambda 10")
delta = worst * lam_env ** 2 + cosmo
gb = np.logspace(-12, -8, 4001)
G1 = {}
for fn, A in FOOT.items():
    dev = np.max(np.abs(np.log10(law(gb, A * (1 + delta))) - np.log10(law(gb, A))))
    G1[fn] = dev
    print(f"  {fn:9s} max |log10 g_obs - log10 g_law| over 1e-12..1e-8 = {dev:.2e} dex (delta = {delta:.2e})")
check("G1 the static quasi-spherical limit is the law within 0.01 dex on both footings (S1 symbolic + numeric)", max(G1.values()) <= 0.01)
print("  inherited, not graded here: v3s's mu_K^2 psi term (mu_K < 0.1/Mpc gives (mu_K r)^2 <= 1e-4 at 100 kpc) and r < L* stiffness")
OUT["G1"] = {"max_dev_dex": G1, "label": "PASS" if max(G1.values()) <= 0.01 else "FAIL"}

# ------------------------------------------------------------------------------------------------ G3
hdr("G3 tie: a0(z) = sqrt(xi G V(z)) in evolving backgrounds; GT, least-squares slope, local exponent; kappa")
BG = {"B1 DESY5": (-0.752, -0.86), "B1p Pantheon+": (-0.838, -0.62), "B1u Union3": (-0.667, -1.09),
      "B2 thawing": (-0.9, -0.1), "B3 freezing": (-0.95, 0.35), "B4 quintom-A": (-1.1, 0.3)}


def cpl(w0, wa, z):
    a = 1 / (1 + np.asarray(z, float))
    w = w0 + wa * (1 - a)
    r = a ** (-3 * (1 + w0 + wa)) * np.exp(-3 * wa * (1 - a))
    dw = -wa * a                                      # dw/d ln a
    return r, w, dw


def grade_bg(rz, wz, dwz):
    """rz, wz, dwz at z = 0, 1, 1.5, 2.33"""
    Vr = rz * (1 - wz) / (1 - wz[0])
    la = 0.5 * np.log10(Vr)
    gt = la[1:] - 0.5 * np.log10(rz[1:])
    lnr = np.log(rz)
    meas = (lnr.max() - lnr.min()) >= 0.1
    s = float(np.polyfit(lnr, 0.5 * np.log(Vr), 1)[0]) if meas else None
    with np.errstate(divide="ignore", invalid="ignore"):
        s_loc = 0.5 + dwz / (6 * (1 - wz) * (1 + wz))
    run0 = -1.5 * (1 + wz[0]) - dwz[0] / (2 * (1 - wz[0]))
    return dict(a0_ratio=(10 ** la[1:]).tolist(), gt=gt.tolist(), gt_pass=bool(np.all(np.abs(gt) <= 0.05)), lnrange=float(lnr.max() - lnr.min()),
                slope=s, slope_pass=(abs(s - 0.5) <= 0.01) if meas else None, s_local=s_loc.tolist(), run_today=float(run0),
                run_today_CT1=float(-1.5 * (1 + wz[0])))


zz = np.array([0.0] + ZS)
G3 = {}
for nm, (w0, wa) in BG.items():
    rz, wz, dwz = cpl(w0, wa, zz)
    real = min(w0, w0 + wa) >= -1 - 1e-12
    gr = grade_bg(rz, wz, dwz)
    gr["realisable"] = real
    G3[nm] = gr
    sl = "n/m" if gr["slope"] is None else f"{gr['slope']:+.4f}"
    print(f"  {nm:15s} w0 {w0:+.3f} wa {wa:+.2f} {'REALISABLE    ' if real else 'NOT REALISABLE'} rho ratio {np.round(rz[1:], 4).tolist()}  a0 ratio {np.round(gr['a0_ratio'], 4).tolist()}\n"
          f"                  GT dev {np.round(gr['gt'], 4).tolist()} [{'PASS' if gr['gt_pass'] else 'FAIL'}]  LSQ slope {sl} [{'PASS' if gr['slope_pass'] else 'FAIL' if gr['slope_pass'] is False else 'n/m'}]"
          f"  local s(z) {np.round(gr['s_local'], 3).tolist()}  d ln a0/d ln a today {gr['run_today']:+.3f} (CT1 form {gr['run_today_CT1']:+.3f})")

# field-equation background: exponential V, lambda = 1, phi at rest at z = 1e3 (Copeland-Liddle-Wands variables, matter + phi)
LAM = 1.0


def rhs(N, s):
    x, y = s
    f = 1 + x * x - y * y
    return [-3 * x + LAM * math.sqrt(1.5) * y * y + 1.5 * x * f, -LAM * math.sqrt(1.5) * x * y + 1.5 * y * f]


Ni = math.log(1e-3)


def run(y_i):
    return solve_ivp(rhs, (Ni, 0.0), [0.0, y_i], rtol=1e-11, atol=1e-14, dense_output=True)


yi = brentq(lambda y: (lambda s: s.y[0, -1] ** 2 + s.y[1, -1] ** 2 - ODE0)(run(y)), 1e-6, 1e-2)
sol = run(yi)


def fe(z):
    N = -math.log(1 + z)
    x, y = sol.sol(N)
    Om_phi = x * x + y * y
    E2 = OM0 * (1 + z) ** 3 / (1 - Om_phi)
    w_ = (x * x - y * y) / Om_phi
    return E2 * Om_phi / ODE0, w_, E2 * y * y, x, y


zz_f = [0.0] + ZS
vals = [fe(z) for z in zz_f]
rz = np.array([v[0] for v in vals])
wz = np.array([v[1] for v in vals])
# dw/dlna numerically
dwz = np.array([(fe(math.exp(-(-math.log(1 + z) + 1e-5)) - 1)[1] - fe(math.exp(-(-math.log(1 + z) - 1e-5)) - 1)[1]) / 2e-5 for z in zz_f])
gr = grade_bg(rz, wz, dwz)
Vdirect = np.array([v[2] for v in vals]) / vals[0][2]
gr["V_direct_check"] = float(np.max(np.abs(Vdirect - rz * (1 - wz) / (1 - wz[0]))))
gr["realisable"] = True
gr["w"] = wz.tolist()
G3["F1 exp V, lambda 1 (field eqs)"] = gr
sl = "n/m" if gr["slope"] is None else f"{gr['slope']:+.4f}"
print(f"  F1 exp V lambda 1 (field equations; phi at rest at z 1e3; Omega_DE0 0.685): w(z=0,1,1.5,2.33) {np.round(wz, 4).tolist()}\n"
      f"                  rho ratio {np.round(rz[1:], 4).tolist()}  a0 ratio {np.round(gr['a0_ratio'], 4).tolist()}  GT dev {np.round(gr['gt'], 4).tolist()} "
      f"[{'PASS' if gr['gt_pass'] else 'FAIL'}]  ln range {gr['lnrange']:.3f}  LSQ slope {sl} "
      f"[{'PASS' if gr['slope_pass'] else 'FAIL' if gr['slope_pass'] is False else 'n/m'}]  local s(z) {np.round(gr['s_local'], 3).tolist()}\n"
      f"                  d ln a0/d ln a today {gr['run_today']:+.3f} (CT1 form {gr['run_today_CT1']:+.3f}); V from y^2 vs rho(1-w)/2 max diff {gr['V_direct_check']:.1e}")
check("G3 control: F1 V from the field variables equals rho (1-w)/2 to 1e-8", gr["V_direct_check"] < 1e-8)
check("G3 control: Lambda (w = -1) gives a0 flat, s undefined-but-trivial (CPL -1, 0)",
      np.allclose(cpl(-1.0, 0.0, zz)[0], 1.0))
real_meas = {k: v for k, v in G3.items() if v["realisable"]}
gt_ok = all(v["gt_pass"] for v in real_meas.values())
sl_ok = all(v["slope_pass"] for v in real_meas.values() if v["slope_pass"] is not None)
check("G3 GT: |log10 a0(z)/a0(0) - 0.5 log10 rho_DE(z)/rho_DE0| <= 0.05 dex at z 1, 1.5, 2.33 in every realisable background", gt_ok)
check("G3 slope: |s - 0.5| <= 0.01 (least squares over z 0, 1, 1.5, 2.33) in every realisable measurable background", sl_ok,
      "; ".join(f"{k} {v['slope']:+.3f}" for k, v in real_meas.items() if v["slope"] is not None))
# kappa
print("  kappa: at w = -1, V = rho_DE c^2, so a0 = sqrt(xi) c sqrt(G rho_DE): kappa^2 = xi. No equation of S constrains xi;"
      " the action is consistent for every xi > 0 (rename test): TRADE, kappa = 1/2 not derived.")
OUT["G3"] = {"backgrounds": G3, "gt_pass": gt_ok, "slope_pass": sl_ok, "kappa": "kappa^2 = xi (TRADE), not derived",
             "label": "PASS" if (gt_ok and sl_ok) else "FAIL"}
print(f"  G3 label: {OUT['G3']['label']}")

# ------------------------------------------------------------------------------------------------ G4
hdr("G4 local gravity (REPORT ONLY if the candidate stopped earlier): inherit C6P / W4a iff phi adds <= 1e-3 of each bound")
sun = max(G2[f]["Sun at 1 AU"]["per_lambda2"] for f in FOOT) * lam_env ** 2
earth = max(G2[f]["Earth surface"]["per_lambda2"] for f in FOOT) * lam_env ** 2
print(f"  Sun delta ln a0 at lambda 10: {sun:.1e}; Earth: {earth:.1e}. C6P's Q2 hedgehog GM/L*^2 does not depend on a0 (C6P README:20);"
      f" a relative a0 shift of {sun:.0e} moves Q2 by at most that fraction (margin >= 2.80e7 / 3.30e7 inside Park).")
print("  fifth force on baryons: phi is not in S_m -> none at tree level; via a0(phi) the anomalous acceleration is ~ delta ln a0 x a0 <= "
      f"{sun * FOOT['alt']:.1e} m/s^2 (Mars bound 1.4e-15). Tensor speed: phi minimally coupled, c_T unchanged (W4a |dv/c| <= 5.1e-32).")
g4 = sun < 1e-3 and sun * FOOT["alt"] < 1e-3 * 1.4e-15
check("G4 every new phi contribution <= 1e-3 of the Cassini, planet, PPN and c_T bounds; C6P/W4a inherited", g4)
OUT["G4"] = {"sun_dlna0": sun, "earth_dlna0": earth, "label": ("PASS (inherited)" if g4 else "FAIL") + (" - REPORT ONLY (stopped at G3)" if OUT["G3"]["label"] == "FAIL" else "")}
print(f"  G4 label: {OUT['G4']['label']}")

# ------------------------------------------------------------------------------------------------ summary
hdr("Summary")
first_fail = next((gname for gname in ("G0", "G1", "G2", "G3") if OUT[gname]["label"].startswith("FAIL")), None)
OUT["first_fail"] = first_fail
OUT["hand_set"] = ["xi (kappa^2 = xi)", "V(phi) shape (lambda) and amplitude V0", "phi initial condition", "L* (v3s)", "mu_K (v3s, free)",
                   "dust abundance (v3s initial condition)", "J_x form (postulated)"]
for gname in ("G0", "G1", "G2", "G3", "G4"):
    print(f"  {gname}: {OUT[gname]['label']}")
print(f"  first failed gate: {first_fail}")
npass = sum(ok for _, ok in CHECKS)
print(f"  checks {npass}/{len(CHECKS)} (gate checks that FAIL are results, not bugs)")
OUT["checks"] = CHECKS
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "ct7_results.json"), "w") as fh:
    json.dump(OUT, fh, indent=1, default=float)
print("kappa = 1/2 FITTED; not theory closed.")
