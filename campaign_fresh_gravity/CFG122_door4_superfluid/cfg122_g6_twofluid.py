#!/usr/bin/env python3
"""CFG122 G6 -- the two-fluid loophole at the EQUATION-OF-STATE level (frozen criteria G6).
Required c_s^2(rho; M_b) from the target (CFG44 B2 E1 formula, point mass; sympy-checked against the target's own dP/drho):
     rho_t(x) = a0/(4 pi G r_M x sqrt(1+x^2)),   c_s,req^2(x) = V_f^2 (1+x^2)^(3/2)/(x (1+2 x^2)),  V_f^2 = sqrt(G M a0) (c = 1)
Two-fluid EOS at the halo temperature T = m sigma^2, sigma^2 = V_f^2/2 (the BTFR: postulated, as in CFG44's surviving 'temperature-slaved fluid'; the convention factor is scanned at
x 1/2 and x 2 as a REPORTED row), ideal-Bose-gas saturation of the normal component:
     rho_crit(T) = m zeta(3/2) (m T/2 pi)^(3/2);  rho < rho_crit: normal isothermal gas, c_s^2 = T/m;
     rho > rho_crit: rho_s = rho - rho_crit, P = P_n^sat + K rho_s^3, K = 1/(12 m^6 Lam^2), c_s^2 = dP/drho|_T = 3 K rho_s^2.
PASS iff some (m, Lam) in the declared plane m in [1e-3, 1e3] eV x Lam in [1e-7, 1e1] eV (60 x 60 log grid; Lam FREE here: the a0 tie is not needed for the EOS) matches the required c_s^2
within 10% at all x in [0.1, 30] for all four masses.  Both a0 footings.
MUTATE (not part of the frozen G6 controls; the frozen controls are a, b, c): none.
Run: python3 cfg122_g6_twofluid.py"""
import os, sys, math
import numpy as np
import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cfg122_common import *

R = Report("cfg122_g6_twofluid")
P, check = R.P, R.check
N_PL = 60
mg = 10 ** np.linspace(-3, 3, N_PL)
Lg = 10 ** np.linspace(-7, 1, N_PL)
Mm, LL = np.meshgrid(mg, Lg, indexing="ij")
xg = np.geomspace(0.1, 30.0, 200)

R.banner("G6 control: sympy check of the required c_s^2(x) against dP/drho along the target")
x = sp.symbols("x", positive=True)
rho_x = 1 / (x * sp.sqrt(1 + x ** 2))          # in units a0/(4 pi G r_M)
g_x = sp.sqrt(1 + x ** 2) / x ** 2             # g_tot / (G M / r_M^2)
cs2_x = sp.simplify(rho_x * g_x / (-sp.diff(rho_x, x)))     # units G M/r_M = V_f^2
target_form = (1 + x ** 2) ** sp.Rational(3, 2) / (x * (1 + 2 * x ** 2))
check("G6.0  c_s,req^2 = rho g_tot/|d rho/dr| = V_f^2 (1+x^2)^(3/2)/(x(1+2x^2))  (CFG44 B2 E1, sympy)", f"{cs2_x}", sp.simplify(cs2_x - target_form) == 0)
xs_ = np.array([0.1, 1.0, 10.0])
P("  required c_s^2/V_f^2 at x = 0.1, 1, 10, 30: " + ", ".join(f"{float(target_form.subs(x, v)):.4g}" for v in (0.1, 1.0, 10.0, 30.0)) + "   (deep limit 1/2 = V_f^2/2 = sigma^2; inner: proportional to M rho)")


def cs2_twofluid(rho, m, Lam, sig2, conv=1.0):
    T = conv * m * sig2
    rho_crit = m * ZETA32 * (m * T / (2 * math.pi)) ** 1.5
    K = 1.0 / (12 * m ** 6 * Lam ** 2)
    rs = np.maximum(rho - rho_crit, 0.0)
    return np.where(rho > rho_crit, 3 * K * rs ** 2, T / m), rho_crit


out = {}
for foot in FOOTINGS:
    a0n = a0_nat(foot)
    for conv, tag in ((1.0, "T = m sigma^2 (frozen)"), (0.5, "x 1/2 (reported)"), (2.0, "x 2 (reported)")):
        allerr = np.zeros(Mm.shape)
        per_mass = {}
        for Mmsun in MASSES:
            M = Mmsun * MSUN_EV
            rMv = float(rM(M, a0n)); V2 = float(Vf2(M, a0n)); sig2 = 0.5 * V2
            rho_t = a0n / (4 * math.pi * G_N * rMv * xg * np.sqrt(1 + xg ** 2))
            cs2_req = V2 * (1 + xg ** 2) ** 1.5 / (xg * (1 + 2 * xg ** 2))
            err = np.zeros(Mm.shape)
            for i in range(N_PL):
                for j in range(N_PL):
                    c2, _ = cs2_twofluid(rho_t, Mm[i, j], LL[i, j], sig2, conv)
                    err[i, j] = np.max(np.abs(c2 / cs2_req - 1.0))
            per_mass[Mmsun] = err
            allerr = np.maximum(allerr, err)
        npass = int(np.sum(allerr <= 0.10))
        i0 = np.unravel_index(np.argmin(allerr), allerr.shape)
        out[(foot, tag)] = dict(npass=npass, best=float(allerr[i0]), m=float(mg[i0[0]]), Lam=float(Lg[i0[1]]),
                                per_mass_best={f"{M:.0e}": float(per_mass[M].min()) for M in MASSES})
        P(f"  [{foot}] {tag}: cells matching at all four masses within 10%: {npass}/{N_PL * N_PL}; closest approach (worst-mass error) {allerr[i0]:.3g} at m = {mg[i0[0]]:.3g} eV, Lam = {Lg[i0[1]]:.3g} eV; "
          f"per-mass best {['%.3g' % per_mass[M].min() for M in MASSES]}")
R.num("G6", {f"{k[0]}|{k[1]}": v for k, v in out.items()})
# fraction of the x-range matched by the best single-mass EOS (reported): where does the normal isothermal component match?
for foot in FOOTINGS:
    a0n = a0_nat(foot)
    M = 1e11 * MSUN_EV
    V2 = float(Vf2(M, a0n))
    cs2_req = V2 * (1 + xg ** 2) ** 1.5 / (xg * (1 + 2 * xg ** 2))
    ok_norm = np.abs(0.5 * V2 / cs2_req - 1) <= 0.10
    P(f"  [{foot}] reported: the isothermal normal component alone (c_s^2 = sigma^2 = V_f^2/2) matches the required c_s^2 within 10% for x >= {xg[ok_norm].min():.3g} (all x above); "
      f"the required c_s^2 is {cs2_req[0] / V2:.3g} V_f^2 at x = 0.1: the inner region needs a stiffer, mass-dependent EOS")
ok = all(out[(f, "T = m sigma^2 (frozen)")]["npass"] > 0 for f in FOOTINGS)
R.verdict("G6", "PASS" if ok else "FAIL",
          f"cells matching at all four masses within 10%: {[out[(f, 'T = m sigma^2 (frozen)')]['npass'] for f in FOOTINGS]}; closest approach {[round(out[(f, 'T = m sigma^2 (frozen)')]['best'], 3) for f in FOOTINGS]} (worst-mass error); "
          "cost even if it passed: the BTFR postulate for T, uniform T in equilibrium, the per-halo R_c")
nf, gf = R.write()
sys.exit(1 if (nf or gf) else 0)
