#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG48 referee -- independent re-derivation of CFG48's headline numbers with the referee's own code (nothing imported from CFG48, CFG44,
CFG4 or DE12; constants typed here).  Companion to CFG48_REFEREE.md.

  R1  the top-hat turnaround contrast at z = 0 in flat LCDM (Omega_m = 0.3153): CFG48 quotes Delta_ta = 11.81 (CFG4's convention).
  R2  B's edge r_e = 0.4 r_ta of the collapse mass M_b (1 + Omega_c/Omega_b), x_e = r_e / r_M, and the negative shell of a flux-gated
      field, M_law(r_e) - M_b = M_b (sqrt(1 + x_e^2) - 1) (P2 point mass): CFG48 G1 quotes 3.21e11, 2.15e12, 1.4e13 Msun at M_b = 1e10, 1e11, 1e12.
  R3  Gauss, numerically: a point mass under a smooth gate W(r) in the flux-gated QUMOND and AQUAL forms -> M_dyn = M_b wherever W = 0.
  R4  the exchange reaction on the baryons, derived here from CFG44's point-mass identities (P = a0 M / 8 pi r^2; rho_c = a0/(4 pi G r sqrt(1+x^2));
      sigma^2 = V_c^2/2; internal energy 3/2 P): the reaction potential is the enclosed-mass derivative of the fluid energy outside s, so the
      force per unit baryon mass is 4 pi s^2 d(eps)/dM.  P-slaved -> (3/4) a0; sigma-slaved (rho_c fixed) -> (3/8) a0 (2 + x^2)/(1 + x^2).
      CFG48 G4 quotes a/g_law = 0.06 (x = 0.3), 0.40 / 0.53 (x = 1), 11.3 / 22.5 (x = 30).
  R5  the energy the exchange must supply: E_c(<r_e) = (3/2) int P dV = (3/4) a0 M_b r_e (point mass, from r = 0), against (1/2) M_b V_f^2 with
      V_f^4 = G M_b a0: ratio 1.5 x_e.  CFG48 G4 quotes 49.6, 33.8, 23.0.
  R6  the mediator requirement alpha_req = x_e^2 / 2 (CFG48 G5): 546, 118, 55, 25 at M_b = 1e10, 1e12, 1e13, 1e14.
Tolerance for 'reproduced': 1% (the quoted numbers are printed to 2-3 figures).
"""
import math
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

G = 4.30091727e-6                       # kpc (km/s)^2 / Msun
A0 = 9.3603e-11 * 3.0857e19 / 1e6       # canonical a0 in (km/s)^2 / kpc
OMM, H, OBH2, OCH2 = 0.3153, 0.6736, 0.02237, 0.1200
OML = 1 - OMM
RHOC = 2.77536627e11 * H ** 2 / 1e9     # Msun / kpc^3
lines, rows = [], []


def out(s=""):
    print(s); lines.append(s)


def rep(label, mine, quoted, tol=0.01):
    ok = all(abs(m / q - 1) <= tol for m, q in zip(np.atleast_1d(mine), np.atleast_1d(quoted)))
    rows.append((label, ok)); out(f"  [{'OK ' if ok else 'DIFF'}] {label}: mine {np.round(np.atleast_1d(mine), 4).tolist()} vs CFG48 {np.atleast_1d(quoted).tolist()}")
    return ok


# R1 --- top-hat turnaround in flat LCDM, H0 = 1 units; shell of comoving radius 1, growing-mode start
def t_of_a(a):
    f = lambda aa: 1.0 / (aa * math.sqrt(OMM / aa ** 3 + OML))
    from scipy.integrate import quad
    return quad(f, 0, a, limit=200)[0]


def turnaround(di, ai=1e-3):
    Hi = math.sqrt(OMM / ai ** 3 + OML)
    y0 = [ai, Hi * ai * (1 - di / 3)]
    k = 0.5 * OMM * (1 + di)
    ev = lambda t, y: y[1]; ev.terminal = True; ev.direction = -1
    s = solve_ivp(lambda t, y: [y[1], -k / y[0] ** 2 + OML * y[0]], [t_of_a(ai), 5.0], y0, events=ev, rtol=1e-11, atol=1e-13)
    return (s.t_events[0][0], s.y_events[0][0][0]) if len(s.t_events[0]) else (np.inf, np.nan)


t0 = t_of_a(1.0)
di = brentq(lambda d: turnaround(d)[0] - t0, 1e-3, 1e-2, xtol=1e-14)
Rta = turnaround(di)[1]
Dta = (1 + di) / Rta ** 3
out("R1  top-hat turnaround contrast at z = 0 (flat LCDM, Omega_m = 0.3153), the referee's own integration")
rep("R1 Delta_ta(z=0) = 1 + delta_NL at turnaround", Dta, 11.81)

# R2 --- edges and negative shells
FC = 1 + OCH2 / OBH2


def r_ta(Mb):
    return (3 * Mb * FC / (4 * math.pi * Dta * OMM * RHOC)) ** (1 / 3)


def xe(Mb):
    return 0.4 * r_ta(Mb) / math.sqrt(G * Mb / A0)


out("\nR2  B's edge (0.4 r_ta of the cosmic-share collapse mass) and the flux-gated negative shell M_b (sqrt(1 + x_e^2) - 1)")
for Mb in (1e10, 1e11, 1e12):
    out(f"    M_b = {Mb:.0e}: r_ta = {r_ta(Mb):7.1f} kpc, r_e = {0.4 * r_ta(Mb):6.1f} kpc, r_M = {math.sqrt(G * Mb / A0):5.1f} kpc, x_e = {xe(Mb):5.2f}")
shell = [Mb * (math.sqrt(1 + xe(Mb) ** 2) - 1) for Mb in (1e10, 1e11, 1e12)]
rep("R2 negative shell (Msun) at M_b = 1e10, 1e11, 1e12 (G1's printed values; the README rounds the last to 1.4e13)", shell, [3.21e11, 2.15e12, 1.44e13], tol=0.01)

# R3 --- Gauss numerically for a smooth gate, both flux-gated forms (nu = P2; AQUAL mu from the same law)
out("\nR3  Gauss with a smooth gate W(r) = 1/2 erfc((r - r_e)/w): M_dyn = r^2 g / G for a point mass")
from scipy.special import erfc
nu = lambda y: 0.5 + math.sqrt(0.25 + 1 / y)          # P2
Mb = 1e11; re = 0.4 * r_ta(Mb); w = 0.05 * re
worst = 0.0
for r in np.linspace(0.2 * re, 3 * re, 400):
    W = 0.5 * erfc((r - re) / w)
    gN = G * Mb / r ** 2
    g_q = gN + W * (nu(gN / A0) - 1) * gN                  # QUMOND: grad Phi = grad Phi_N + W (nu - 1) grad Phi_N
    # AQUAL: [W mu(g/a0) + 1 - W] g = gN, with mu the inverse of the P2 law: mu(s) = s / (1 + s) for P2
    g_a = brentq(lambda g: (W * (g / A0) / (1 + g / A0) + 1 - W) * g - gN, gN * 0.999, gN * 1e4)
    if W < 1e-12:
        worst = max(worst, abs(r * r * g_q / G / Mb - 1), abs(r * r * g_a / G / Mb - 1))
out(f"    beyond the edge (W < 1e-12): max |M_dyn / M_b - 1| = {worst:.1e} for both forms")
rows.append(("R3 Gauss: M_dyn = M_b beyond a smooth edge, QUMOND and AQUAL", worst < 1e-9))
out(f"  [{'OK ' if worst < 1e-9 else 'DIFF'}] R3 Gauss holds to {worst:.1e}")

# R4 --- the exchange reaction from CFG44's identities
out("\nR4  the exchange reaction per unit baryon mass, derived here: F = 4 pi s^2 d eps/dM at fixed r")


def reaction(x, mode):
    Mb = 1e11; rM = math.sqrt(G * Mb / A0); r = x * rM
    if mode == "P":
        deps = 1.5 * A0 / (8 * math.pi * r ** 2)                             # eps = (3/2) P, P = a0 M / 8 pi r^2
    else:
        gN = lambda M: G * M / r ** 2
        Vc2 = lambda M: r * math.sqrt(gN(M) ** 2 + A0 * gN(M))                 # P2
        rho_c = A0 / (4 * math.pi * G * r * math.sqrt(1 + x * x))
        dM = Mb * 1e-6
        deps = 1.5 * rho_c * 0.5 * (Vc2(Mb + dM) - Vc2(Mb - dM)) / (2 * dM)   # eps = (3/2) rho_c sigma^2, sigma^2 = V_c^2 / 2
    F = 4 * math.pi * r ** 2 * deps
    gl = math.sqrt((G * Mb / r ** 2) ** 2 + A0 * G * Mb / r ** 2)
    return F / A0, F / gl


for mode, closed in (("sigma", lambda x: 0.375 * (2 + x * x) / (1 + x * x)), ("P", lambda x: 0.75)):
    vals = [reaction(x, mode) for x in (0.3, 1.0, 30.0)]
    out(f"    {mode}-slaved: a/a0 = {[round(v[0], 4) for v in vals]} (closed {[round(closed(x), 4) for x in (0.3, 1, 30)]}); a/g_law = {[round(v[1], 3) for v in vals]}")
rep("R4 sigma-slaved a/g_law at x = 0.3, 1, 30", [reaction(x, "sigma")[1] for x in (0.3, 1.0, 30.0)], [0.062, 0.398, 11.26], tol=0.01)
rep("R4 P-slaved a/g_law at x = 1, 30", [reaction(x, "P")[1] for x in (1.0, 30.0)], [0.530, 22.49], tol=0.01)

# R5 --- the energy ratio
out("\nR5  E_c(<r_e) / (1/2 M_b V_f^2) = 1.5 x_e")
rep("R5 energy ratio at M_b = 1e10, 1e11, 1e12", [1.5 * xe(M) for M in (1e10, 1e11, 1e12)], [49.6, 33.8, 23.0], tol=0.01)

# R6 --- the mediator requirement
out("\nR6  alpha_req = x_e^2 / 2")
rep("R6 alpha_req at M_b = 1e10, 1e12, 1e13, 1e14", [xe(M) ** 2 / 2 for M in (1e10, 1e12, 1e13, 1e14)], [546, 118, 55, 25], tol=0.02)

# R7 --- sensitivity (not a reproduction): the COMMITTED r_ta convention (CFG4_target.r_turnaround, CFG11/CFG12 rta_of): where the LAW's
#          enclosed mass (phantom included; P2 here, M_b sqrt(1 + x^2)) falls to Delta_ta rho_m -- CFG48 used the cosmic-share collapse mass instead
out("\nR7  sensitivity to the r_ta convention: CFG48's (cosmic-share collapse mass) vs the committed one (the law's enclosed mass, P2)")
for Mb in (1e10, 1e11, 1e12, 1e13, 1e14):
    rM = math.sqrt(G * Mb / A0)
    f = lambda r: Mb * math.sqrt(1 + (r / rM) ** 2) - 4 / 3 * math.pi * Dta * OMM * RHOC * r ** 3
    rt_law = brentq(f, rM, 1e6)
    xl = 0.4 * rt_law / rM
    out(f"    M_b = {Mb:.0e}: r_ta {r_ta(Mb):7.0f} -> {rt_law:7.0f} kpc; x_e {xe(Mb):5.1f} -> {xl:5.1f}; shell/M_b {math.sqrt(1 + xe(Mb) ** 2) - 1:5.1f} -> "
        f"{math.sqrt(1 + xl ** 2) - 1:5.1f}; energy ratio {1.5 * xe(Mb):5.1f} -> {1.5 * xl:5.1f}; alpha_req {xe(Mb) ** 2 / 2:6.0f} -> {xl ** 2 / 2:6.0f}")

nd = sum(not ok for _, ok in rows)
out(f"\n  {len(rows) - nd}/{len(rows)} CFG48 numbers reproduced by the referee's own code")
open(__file__.replace(".py", ".out"), "w").write("\n".join(lines) + "\n")
