#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LANE T1 -- TREE-LEVEL BACKREACTION: THE ESCAPE THE WARD LANE NAMED AND DID NOT TAKE
===================================================================================
mi_tree_backreaction_2026.py

The Ward lane (mi_goldstone_ward_2026.py, 25/25) closed the probe-worldline route
"at the stated order in a HOMOGENEOUS background" and left this door open in its own
words: "near a source d_mu u_nu != 0 and the 3 surviving one-du structures DO
contribute". That is a CLASSICAL, TREE-LEVEL statement -- no loop, no hbar -- so it is
untouched by the loop-level no-go (mi_drift_magnitude_audit_2026.py, 27/27). This lane
takes it: static mass M in the ghost condensate, sourced profile at tree level, test
worldline in THAT inhomogeneous background, three one-du structures with FREE symbolic
coefficients c_A, c_B, c_C, and the honest question of whether g_obs^2 = g_bar^2 +
a_0 g_bar comes out with a DETERMINED coefficient.

FOUR RESULTS, all proven below, none previously in this corpus:

  T1-A  THE SOURCED PROFILE IS THE NEWTONIAN FIELD.  With no direct matter-phi
        coupling the shift current forces flux C = 0, whose regular branch is psi' = 0:
        the condensate stays exactly co-moving with the static observer and X varies
        in space PURELY through the metric, X = X_0/N^2. Then Nabla_mu u_nu =
        -u_mu a_nu EXACTLY, with a_nu = d_nu ln N, so the condensate congruence
        acceleration IS g_bar/c^2. d_mu u_nu != 0 near a source is real and its size
        is NOT a free parameter. Vorticity, shear and expansion all vanish.

  T1-B  THE CO-MOVING VANISHING THEOREM.  a.u = 0 identically (forced by u.u = -1), so
        in this branch A = (a.xdot), B = -(u.xdot)(a.xdot), C = theta = 0: the three
        structures have RANK ONE, c_C is unobservable, and every one of them VANISHES
        for a probe co-moving with the condensate -- which here is the probe AT REST.
        The one-du sector produces NO static force.

  T1-B' *** THE CIRCULAR-ORBIT CANCELLATION (the kill). ***  Stronger, and computed
        not estimated: for the general term Phi^k (v^2)^m (v . grad Phi) the Euler-
        Lagrange equations vanish IDENTICALLY on a circular orbit for every k and
        every m, for an ARBITRARY potential Phi(r) -- the total-derivative pieces drop
        and the two survivors cancel because omega = v/r. So the entire one-du sector,
        TO ALL ORDERS in the free function h(u.xdot), contributes exactly ZERO to the
        equation that sets a rotation curve. The same terms are NONZERO on an
        eccentric orbit (checked), and there the price is l*c_B = 1.4e3 (canonical) /
        1.7e3 (ALT) HUBBLE RADII. So: dead on circular orbits by a theorem, dead on
        eccentric orbits by a prefactor.

  T1-C  THE EXPONENT CENSUS.  The static radial branches are exactly three:
        psi' ~ r^0 (uncharged), psi' ~ r^(-1/2) (stay-on-attractor), and
        psi' ~ r^(-2/(2n+1)) for P'(dX) ~ dX^n (shift-charged). MOND needs force ~ 1/r,
        forcing n = 1/2 EXACTLY: P'(X) ~ sqrt(X - X_0), NON-ANALYTIC at the attractor
        -- which is precisely what this framework's own kernel demands, since
        f'(z) = (sqrt(1+4z)-1)/(2 sqrt z) -> sqrt z. The attractor fixes ONE datum,
        -P(X_0) = rho_Lambda; the sqrt-coefficient p_half and the matter coupling
        alpha are INDEPENDENT data, so kappa = a_0/(c sqrt(G rho_Lambda)) is ONE
        equation in TWO unknowns:
            *** MOND STRUCTURE WITH A FITTED COEFFICIENT. ***

VERDICT: NO-GO by new theorem (T1-B'), with the field-sector escape priced (T1-C).
kappa = 1/2 is FITTED, NOT DERIVED; nothing here changes that and this lane does not
try to. BOTH footings reported on every dimensional number: canonical a_0 = 9.3614e-11
(kappa = 1/2, rho_DE + c H_Lambda) and ALT a_0 = 1.13e-10 (x1.2082). T1-B' is exactly
footing-BLIND (a cancellation, no scale in it); the eccentric price differs between
footings by exactly the footing ratio and is fatal on both; T1-C leaves kappa free,
which is the same statement on either footing.

AGAINST INTEREST, recorded up front, three items:
 (1) *** ONE CHANNEL'S PREFACTOR IS AFFORDABLE. *** The two-du invariant (a.a) is a
     pure POSITION function, so it EVADES T1-B and T1-B' entirely -- it is a potential.
     Its required coupling is l ~ 3.4 Mpc = 6e-4 Hubble radii, comfortably inside any
     sane EFT. It dies on SHAPE, not on prefactor: it gives an extra force
     proportional to d(g_bar^2)/dr, i.e. r^(-5) for a point mass and r^(-3) in a flat
     region, where MOND needs r^(-1); matching would require g_bar GROWING as r^(2/3).
     Anyone quoting this lane must quote that item too.
 (2) The du sector DOES structurally carry the external field (u is condensate-tied,
     not free-fall-tied), so the EFE origin is qualitatively right -- but EFE follows
     from concavity alone, so reproducing it is NOT evidence for this route.
 (3) T1-B' means this sector does NOT produce the l = 0 constant a_0/2 sunward term
     that costs the exact law 1278x the Earth/Mars bound. Favourable -- and worthless,
     since it produces no MOND either.

THREE INDEPENDENT PREDICTIONS (a route that only reproduces its target is numerology).
All three go AGAINST the route:
  P1  the affordable (a.a) channel predicts a_extra ~ g_bar^2/r ~ v^4/r^3, which varies
      by ~2.4 dex across SPARC-like systems against the a_0-line's ~0.06 dex, and falls
      32x per doubling of r for a point mass. Falsified on shape and on universality.
  P2  the two non-MOND field branches predict RISING curves, v ~ r^(1/6)
      (x1.468/decade) and v ~ r^(1/4) (x1.778/decade). Flat curves exclude both.
  P3  the branch that DOES give MOND forces c_s^2 -> 0 linearly in (X - X_0): the
      condensate sound speed VANISHES exactly where MOND turns on. A new liability
      against this corpus's own "Jeans dS-cured" standing.
  P4 (structural, from T1-B'): zero rotation-curve signature but a nonzero effect on
      ECCENTRIC orbits -- the signature lives in de/dt, not in v(r).

MANDATORY CREDIT: nu = sqrt(1+1/y) and the dS-Unruh balance are Milgrom 1999 PLA
253:273 eqs 6-9 (he fixes a_0_hat = 2 c H_Lambda, r = 1); his eqs 10-11 give a second
coefficient (r = 2); Milgrom 2008 arXiv:0801.3133 sec 7.3.1 notes the coefficient
mismatch "isn't necessarily meaningful". a_lambda = c^2 sqrt(Lambda/3): Milgrom 1994
Ann.Phys. 229:384. Temperature sqrt(a^2 + Lambda/3)/2pi: Narnhofer, Peter and Thirring
1996 IJMPB 10:1507. Five-acceleration: Deser and Levin 1997 CQG 14:L163. Exponential
kernel: McGaugh 2008 ApJ 683:137 eq 11a. AQUAL: Bekenstein and Milgrom 1984. Ghost
condensate: Arkani-Hamed, Cheng, Luty, Mukohyama 2004. Boost-breaking EFT zoology:
Nicolis, Penco, Piazza, Rattazzi 2015. GHY boundary term: Gibbons and Hawking 1977,
York 1972.
"""

import sys
import numpy as np
import mpmath as mp
import sympy as sp
from scipy.optimize import brentq

mp.mp.dps = 40

RESULTS = []
FAILED = []


def check(name, cond):
    ok = bool(cond)
    RESULTS.append(ok)
    if not ok:
        FAILED.append(name)
    print(("[OK]   " if ok else "[FAIL] ") + name)
    return ok


def quiet(cond):
    """Evaluate a deliberately corrupted variant WITHOUT registering it as a check."""
    return bool(cond)


SEP = "=" * 78
print(SEP)
print("LANE T1: tree-level backreaction of a static mass on the ghost condensate")
print(SEP)

# ===========================================================================
# SECTION 0 -- constants, BOTH footings, the pi-free identity, float64 hazards
# ===========================================================================
print("\n--- Section 0: constants, both footings, the sqrt(6)/8 identity ---")

c_light = 2.99792458e8          # m/s (exact)
G_N = 6.67430e-11               # m^3 kg^-1 s^-2
rho_L = 5.844e-27               # kg/m^3, canonical (rho_DE)
H_L = 1.80772e-18               # s^-1
cHL = 5.4194e-10                # c H_Lambda, m/s^2
Z_num = 5.7888100366            # 2 sqrt(8 pi/3)
kpc = 3.0856775814913673e19     # m
Msun = 1.98892e30               # kg

c_sqrtGrho = c_light * np.sqrt(G_N * rho_L)
a0_can = 0.5 * c_sqrtGrho
a0_alt = 1.13e-10
FOOTINGS = (("canonical", a0_can), ("ALT", a0_alt))
R_H = c_light / H_L

print(f"  c sqrt(G rho_Lambda)        = {c_sqrtGrho:.6e} m/s^2   (target 1.87228e-10)")
print(f"  a_0 canonical (kappa = 1/2) = {a0_can:.6e} m/s^2   (target 9.3614e-11)")
print(f"  a_0 ALT                     = {a0_alt:.6e} m/s^2   (ratio {a0_alt/a0_can:.4f})")
print(f"  c H_Lambda                  = {cHL:.6e} m/s^2")
print(f"  Hubble radius c/H_Lambda    = {R_H:.6e} m")

check("S0.1 c sqrt(G rho_Lambda) reproduces 1.87228e-10 to 1e-4 relative",
      abs(c_sqrtGrho - 1.87228e-10) / 1.87228e-10 < 1e-4)
check("S0.2 canonical a_0 = kappa c sqrt(G rho_Lambda) reproduces 9.3614e-11 to 1e-4",
      abs(a0_can - 9.3614e-11) / 9.3614e-11 < 1e-4)
check("S0.3 ALT/canonical footing ratio is 1.2082 to 1e-3 (both footings live)",
      abs(a0_alt / a0_can - 1.2082) / 1.2082 < 1e-3)
check("S0.4 c x H_Lambda reproduces the quoted c H_Lambda = 5.4194e-10 to 1e-4",
      abs(c_light * H_L - cHL) / cHL < 1e-4)

t_dyn = 1.0 / np.sqrt(G_N * rho_L)
check("S0.5 t_dyn = 1/sqrt(G rho_Lambda) = 1.6011e18 s to 1e-3, and c/t_dyn == "
      "c sqrt(G rho_Lambda) to 1e-14",
      abs(t_dyn - 1.6011e18) / 1.6011e18 < 1e-3 and
      abs(c_light / t_dyn - c_sqrtGrho) / c_sqrtGrho < 1e-14)

# item 8's pi-free corner and the ONE EXACT FACTOR, verified before any use
rho_s, G_s, c_s = sp.symbols('rho_s G_s c_s', positive=True)
A_hor_s = sp.simplify(4 * sp.pi * c_s**2 / (8 * sp.pi * G_s * rho_s / 3))
check("S0.6 the dS horizon AREA in the vacuum density is EXACTLY pi-free: "
      "4 pi c^2/H^2 == 3 c^2/(2 G rho_Lambda), and the right side contains no pi "
      "(item 8, verified rather than assumed)",
      sp.simplify(A_hor_s - 3 * c_s**2 / (2 * G_s * rho_s)) == 0 and
      not (3 * c_s**2 / (2 * G_s * rho_s)).has(sp.pi))
lhs8 = sp.sqrt(6) / 8 * c_s**2 / sp.sqrt(3 * c_s**2 / (2 * G_s * rho_s))
rhs8 = c_s * sp.sqrt(G_s * rho_s) / 4                    # = a_0/2 at kappa = 1/2
check("S0.7 item 8's ONE EXACT FACTOR: (sqrt(6)/8) c^2/sqrt(A_hor) == "
      "(c/4) sqrt(G rho_Lambda) == a_0/2 at kappa = 1/2, symbolically",
      sp.simplify(lhs8 - rhs8) == 0)
A_hor_num = 3 * c_light**2 / (2 * G_N * rho_L)
check("S0.8 the same identity numerically to 1e-12 relative",
      abs(np.sqrt(6) / 8 * c_light**2 / np.sqrt(A_hor_num) - a0_can / 2)
      / (a0_can / 2) < 1e-12)
nc_fac = quiet(abs(0.25 * c_light**2 / np.sqrt(A_hor_num) - a0_can / 2)
               / (a0_can / 2) < 1e-6)
check("S0.9 NEGATIVE CONTROL: replacing sqrt(6)/8 = 0.3061862 by the 'obvious' 1/4 "
      "BREAKS the identity, so S0.7-S0.8 are not vacuous", not nc_fac)

for nm, a0 in FOOTINGS:
    print(f"  master formula, {nm:9s}: q = a_0/(c H_L) = {a0/cHL:.6f}  ->  "
          f"r = 2/q = {2*cHL/a0:.6f}")
check("S0.10 master formula bookkeeping: canonical r = 2 c H_L/a_0 equals "
      "2Z = 11.577620 to 1e-3 (ties to mi_crossover_master_formula_2026)",
      abs(2 * cHL / a0_can - 2 * Z_num) / (2 * Z_num) < 1e-3)

x_tiny = 1e-17
check("S0.11 FLOAT64 HAZARD (log1p): naive ln(1 + 1e-17) returns exactly 0.0 while "
      "log1p returns 1e-17 -- the stable form is what gets used",
      np.log(1.0 + x_tiny) == 0.0 and abs(np.log1p(x_tiny) - x_tiny) / x_tiny < 1e-12)


def gbar_naive(g, a0):
    return 0.5 * (-a0 + np.sqrt(a0 * a0 + 4.0 * g * g))


def gbar_stable(g, a0):
    return 2.0 * g * g / (a0 + np.sqrt(a0 * a0 + 4.0 * g * g))


g_probe = a0_can * 1e-9
g_m, a_m = mp.mpf(g_probe), mp.mpf(a0_can)
exact_inv = float((-a_m + mp.sqrt(a_m**2 + 4 * g_m**2)) / 2)
err_naive = abs(gbar_naive(g_probe, a0_can) - exact_inv) / exact_inv
err_stable = abs(gbar_stable(g_probe, a0_can) - exact_inv) / exact_inv
print(f"  a_0-line inversion at g_obs/a_0 = 1e-9: naive rel.err {err_naive:.2e}, "
      f"algebraically rewritten rel.err {err_stable:.2e}")
check("S0.12 FLOAT64 HAZARD (catastrophic cancellation): the naive a_0-line inversion "
      "g_bar = (-a_0 + sqrt(a_0^2+4g^2))/2 loses >1e-2 relative while the rewritten "
      "2g^2/(a_0 + sqrt(...)) holds to <1e-14 against a 40-digit mpmath reference",
      err_naive > 1e-2 and err_stable < 1e-14)

# ===========================================================================
# SECTION 1 -- the condensate, the attractor, and what the attractor FIXES
# ===========================================================================
print("\n--- Section 1: shift-symmetric P(X), the attractor, the condensate scale ---")
print("  convention: X = -g^{mu nu} d_mu phi d_nu phi > 0 for timelike phi")
print("  (mostly-plus metric), u_mu = d_mu phi/sqrt(X), so u.u = -1.")

t4, x4, y4, z4 = sp.symbols('t4 x4 y4 z4', real=True)
crd4 = [t4, x4, y4, z4]
phi4 = sp.Function('phi4')(*crd4)
gi4 = sp.diag(-1, 1, 1, 1)
dphi4 = sp.Matrix([sp.diff(phi4, cc) for cc in crd4])
X4 = -(dphi4.T * gi4 * dphi4)[0, 0]
u4 = dphi4 / sp.sqrt(X4)
check("S1.1 u.u == -1 IDENTICALLY for generic phi in 4D (the condensate really does "
      "generate a unit timelike preferred vector)",
      sp.simplify((u4.T * gi4 * u4)[0, 0]) == -1)

tc = sp.Symbol('t_cos', real=True)
aS = sp.Function('a_scale', positive=True)(tc)
vphi = sp.Function('varphi')(tc)
Pf = sp.Function('P')
w = sp.Symbol('w_dummy')
Xfrw = sp.diff(vphi, tc)**2
Lfrw = aS**3 * Pf(Xfrw)
dLdv = sp.diff(Lfrw, sp.diff(vphi, tc))
ELfrw = sp.diff(dLdv, tc)
Jshift = 2 * aS**3 * sp.diff(Pf(w), w).subs(w, Xfrw) * sp.diff(vphi, tc)
check("S1.2 FRW EOM integrates to a^3 P'(X) phidot = const (the shift current), so "
      "as a grows P'(X) -> 0: the attractor is DYNAMICALLY selected, not imposed "
      "(ghost condensate: Arkani-Hamed, Cheng, Luty, Mukohyama 2004)",
      sp.simplify(dLdv - Jshift) == 0 and
      sp.simplify(ELfrw - sp.diff(Jshift, tc).doit()) == 0)

X_s, X0_s = sp.symbols('X_s X0_s', positive=True)
p_half = sp.Symbol('p_half', positive=True)
rhoL_s = sp.Symbol('rhoL_s', positive=True)
# the kinetic function the framework's OWN kernel turns out to require (Section 5)
P_req = -rhoL_s + sp.Rational(2, 3) * p_half * (X_s - X0_s)**sp.Rational(3, 2)
Pp_req = sp.diff(P_req, X_s)
rho_bg = sp.simplify((2 * X_s * Pp_req - P_req).subs(X_s, X0_s))
check("S1.3 at the attractor P'(X_0) = 0 the background density is EXACTLY "
      "rho = 2 X P' - P = -P(X_0) = rho_Lambda: THE ATTRACTOR FIXES THE CONDENSATE "
      "SCALE TO rho_Lambda, and fixes nothing else",
      sp.simplify(Pp_req.subs(X_s, X0_s)) == 0 and sp.simplify(rho_bg - rhoL_s) == 0)
P_bad = P_req + sp.Rational(1, 7) * (X_s - X0_s)
rho_bad = sp.simplify((2 * X_s * sp.diff(P_bad, X_s) - P_bad).subs(X_s, X0_s))
check("S1.4 NEGATIVE CONTROL: adding a linear term so P'(X_0) = 1/7 != 0 breaks "
      "rho = rho_Lambda by exactly 2 X_0/7 -- S1.3 can fail",
      not quiet(sp.simplify(rho_bad - rhoL_s) == 0) and
      sp.simplify(rho_bad - rhoL_s - 2 * X0_s / 7) == 0)
print("  => the attractor fixes ONE number, -P(X_0) = rho_Lambda. The coefficient")
print("     p_half is a SEPARATE datum of the same function. Hold that for Section 5.")

# ===========================================================================
# SECTION 2 -- THEOREM T1-A: the sourced profile, and d_mu u_nu explicitly
# ===========================================================================
print("\n--- Section 2: static mass M in the condensate; the tree-level profile (T1-A) ---")

t2, r2 = sp.symbols('t_2 r_2', real=True)
crd2 = [t2, r2]
Nf = sp.Function('N', positive=True)(r2)          # g_tt = -N^2
Af = sp.Function('A', positive=True)(r2)          # g_rr = A
psif = sp.Function('psi')(r2)
phi0 = sp.Symbol('phi0', positive=True)

g2 = sp.diag(-Nf**2, Af)
g2i = g2.inv()


def christoffel(gmat, gimat, coords):
    n = len(coords)
    Gam = [[[0] * n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for cc in range(n):
                s = 0
                for d in range(n):
                    s += gimat[a, d] * (sp.diff(gmat[d, b], coords[cc])
                                        + sp.diff(gmat[d, cc], coords[b])
                                        - sp.diff(gmat[b, cc], coords[d]))
                Gam[a][b][cc] = sp.simplify(s / 2)
    return Gam


Gam2 = christoffel(g2, g2i, crd2)


def cov_du(u_lo, Gam):
    out = [[0] * 2 for _ in range(2)]
    for mu in range(2):
        for nu in range(2):
            e = sp.diff(u_lo[nu], crd2[mu])
            for lam in range(2):
                e -= Gam[lam][mu][nu] * u_lo[lam]
            out[mu][nu] = sp.simplify(e)
    return out


def raise_idx(v_lo):
    return [sp.simplify(sum(g2i[mu, nu] * v_lo[nu] for nu in range(2)))
            for mu in range(2)]


def dot_lo_up(v_lo, w_up):
    return sp.simplify(sum(v_lo[i] * w_up[i] for i in range(2)))


# --- the shift current forces the radial flux equation -----------------------
phi_static = -phi0 * t2 + psif                    # shift symmetry permits t-linear
dphi_s = [sp.diff(phi_static, cc) for cc in crd2]
X_expr = sp.simplify(-sum(g2i[mu, nu] * dphi_s[mu] * dphi_s[nu]
                          for mu in range(2) for nu in range(2)))
check("S2.1 for phi = -phi0 t + psi(r), X = phi0^2/N^2 - psi'^2/A: the METRIC enters "
      "X at the same order as the gradient. That is why a static mass sources the "
      "condensate at all, with or without a direct coupling.",
      sp.simplify(X_expr - (phi0**2 / Nf**2 - sp.diff(psif, r2)**2 / Af)) == 0)

th4 = sp.Symbol('theta_4', real=True)
Pfun = sp.Function('Pc')
sqrtg = Nf * sp.sqrt(Af) * r2**2 * sp.sin(th4)
flux = sp.simplify(sqrtg * sp.diff(Pfun(w), w).subs(w, X_expr)
                   * g2i[1, 1] * sp.diff(psif, r2) / sp.sin(th4))
flux_wf = sp.simplify(flux.subs({Nf: 1, Af: 1}).doit())
check("S2.2 the phi field equation is d_r[ N sqrt(A) r^2 P'(X) psi'/A ] = 0, i.e. "
      "r^2 P'(X) psi' = C in the weak-field limit, where C is the SHIFT CHARGE FLUX "
      "through the sphere",
      sp.simplify(flux_wf - r2**2 * sp.diff(Pfun(w), w).subs(
          w, X_expr.subs({Nf: 1, Af: 1})) * sp.diff(psif, r2)) == 0)

print("  the three static branches of r^2 P'(X) psi' = C (the census, T1-C):")
print("    (i)   C = 0, psi' = 0             : uncharged mass (no direct phi coupling)")
print("    (ii)  C = 0, P'(X) = 0 everywhere : 'stay on the attractor', psi' ~ r^(-1/2)")
print("    (iii) C != 0, P' ~ dX^n           : shift-charged, psi' ~ r^(-2/(2n+1))")
print("  Branch (i) is the one with NO new free function -- take it first.")

# --- branch (i): the whole geometry of d_mu u_nu -----------------------------
u_lo_i = [-Nf, 0]
u_up_i = raise_idx(u_lo_i)
check("S2.3 branch (i): u_mu = (-N, 0) is unit-normalised, u.u == -1 exactly, for "
      "ARBITRARY N(r) and A(r)", dot_lo_up(u_lo_i, u_up_i) == -1)

D_i = cov_du(u_lo_i, Gam2)
a_lo_i = [sp.simplify(sum(u_up_i[mu] * D_i[mu][nu] for mu in range(2)))
          for nu in range(2)]
check("S2.4 THEOREM T1-A(1): the condensate congruence acceleration is a_nu = "
      "d_nu ln N EXACTLY (a_t = 0, a_r = N'/N) for arbitrary N, A -- computed from "
      "the Christoffel symbols, not assumed",
      a_lo_i[0] == 0 and sp.simplify(a_lo_i[1] - sp.diff(Nf, r2) / Nf) == 0)
check("S2.5 a.u == 0 identically, forced by u.u = -1. THIS IS THE SEED OF T1-B.",
      sp.simplify(dot_lo_up(a_lo_i, u_up_i)) == 0)
check("S2.6 THEOREM T1-A(2): Nabla_mu u_nu == -u_mu a_nu EXACTLY in branch (i) "
      "(vorticity, shear AND expansion all vanish for the static congruence), "
      "verified component by component for arbitrary N, A",
      all(sp.simplify(D_i[mu][nu] + u_lo_i[mu] * a_lo_i[nu]) == 0
          for mu in range(2) for nu in range(2)))
theta_i = sp.simplify(sum(g2i[mu, nu] * D_i[mu][nu]
                          for mu in range(2) for nu in range(2)))
check("S2.7 the expansion theta = Nabla.u == 0 EXACTLY in branch (i), so the trace "
      "structure vanishes identically and c_C DROPS OUT of the worldline EOM",
      theta_i == 0)

# NEGATIVE CONTROL: corrupt the Christoffel that actually carries the result
Gam_bad = [[[Gam2[a][b][cc] for cc in range(2)] for b in range(2)] for a in range(2)]
Gam_bad[0][1][0] = Gam_bad[0][1][0] * 2           # Gamma^t_{rt}, doubled
Gam_bad[0][0][1] = Gam_bad[0][0][1] * 2
D_bad = cov_du(u_lo_i, Gam_bad)
a_bad = [sp.simplify(sum(u_up_i[mu] * D_bad[mu][nu] for mu in range(2)))
         for nu in range(2)]
nc_dec = quiet(sp.simplify(a_bad[1] - sp.diff(Nf, r2) / Nf) == 0 and
               all(sp.simplify(D_bad[mu][nu] + u_lo_i[mu] * a_bad[nu]) == 0
                   for mu in range(2) for nu in range(2)))
check("S2.8 NEGATIVE CONTROL (Christoffel corruption): doubling Gamma^t_{rt} -- the "
      "symbol that actually carries a_r -- breaks BOTH a_r = N'/N and "
      "Nabla u = -u a. S2.4/S2.6 are real computations. (An earlier version of this "
      "control corrupted Gamma^r_{tt}, which contracts with u_r = 0 and so changed "
      "NOTHING: a control that could not fire.)",
      not nc_dec)

GM, cc_s = sp.symbols('GM c_s2', positive=True)
N_sch = sp.sqrt(1 - 2 * GM / (r2 * cc_s**2))
a_r_exact = sp.simplify(sp.diff(N_sch, r2) / N_sch)
lead = sp.simplify(sp.series(a_r_exact, GM, 0, 3).removeO().coeff(GM, 1))
check("S2.9 THEOREM T1-A(3): a_r = N'/N = GM/(r^2 c^2) + O((GM)^2). The condensate "
      "congruence acceleration IS g_bar/c^2 -- d_mu u_nu != 0 near a source is real "
      "and its magnitude is NOT a free parameter",
      sp.simplify(lead - 1 / (r2**2 * cc_s**2)) == 0)

print("  REFINEMENT (series order 1 -> 2 against the EXACT Schwarzschild a_r):")
M_mw = 1.0e11 * Msun
rs_mw = 2 * G_N * M_mw / c_light**2
rows = []
for lab, rv in (("solar circle 8.122 kpc", 8.122 * kpc), ("1 kpc", 1.0 * kpc),
                ("3 Schwarzschild radii", 3 * rs_mw)):
    ex = (G_N * M_mw / rv**2) / np.sqrt(1 - rs_mw / rv)
    o1 = G_N * M_mw / rv**2
    o2 = o1 * (1 + 0.5 * rs_mw / rv)
    rows.append((lab, abs(o1 - ex) / ex, abs(o2 - ex) / ex))
    print(f"    {lab:26s}: O(Phi) shift {rows[-1][1]:.3e}, "
          f"O(Phi^2) shift {rows[-1][2]:.3e}")
check("S2.10 REFINEMENT (order 1 -> 2): the O(Phi^2) result beats O(Phi) at EVERY "
      "radius tested including 3 Schwarzschild radii, and at galactic radii the "
      "leading-order shift is already < 1e-5 -- using a_r = g_bar/c^2 for rotation "
      "curves is safe, and the deliberately extreme 3-r_s point (4.7e-2) shows the "
      "check has teeth",
      all(rw[2] < rw[1] for rw in rows) and
      all(rw[1] < 1e-5 for rw in rows[:2]))

Phi_w = sp.Symbol('Phi_w', real=True)
psip_attr2 = sp.series(phi0**2 / (1 + Phi_w)**2 - phi0**2, Phi_w, 0, 2).removeO()
check("S2.11 branch (ii), 'stay on the attractor' (P'(X) = 0 everywhere): requires "
      "psi'^2 = phi0^2(1/N^2 - 1) = -2 phi0^2 Phi + O(Phi^2), so psi' ~ sqrt(2GM/r)/c "
      "~ r^(-1/2). A REAL sourced gradient with exponent -1/2 -- not MOND's -1.",
      sp.simplify(sp.expand(psip_attr2) - (-2 * phi0**2 * Phi_w)) == 0)

# ===========================================================================
# SECTION 3 -- THEOREM T1-B: the three structures and the co-moving vanishing
# ===========================================================================
print("\n--- Section 3: worldline in the sourced background; the 3 one-du structures ---")
print("  S_du = Int dtau m l { [c_A + c_B (u.xdot)] (a^cond . xdot) + c_C theta }")
print("  c_A, c_B, c_C are FREE dimensionless EFT numbers, l a length. Not set by hand.")

xd0, xd1 = sp.symbols('xd0 xd1', real=True)
xd_up = [xd0, xd1]
A_str = sp.simplify(sum(u_up_i[mu] * xd_up[nu] * D_i[mu][nu]
                        for mu in range(2) for nu in range(2)))
B_str = sp.simplify(sum(xd_up[mu] * xd_up[nu] * D_i[mu][nu]
                        for mu in range(2) for nu in range(2)))
a_dot_xd = sp.simplify(sum(a_lo_i[nu] * xd_up[nu] for nu in range(2)))
U_inv = sp.simplify(sum(u_lo_i[nu] * xd_up[nu] for nu in range(2)))

check("S3.1 structure A = u^m xd^n Nabla_m u_n == (a . xdot) exactly",
      sp.simplify(A_str - a_dot_xd) == 0)
check("S3.2 structure B = xd^m xd^n Nabla_m u_n == -(u.xdot)(a.xdot) exactly",
      sp.simplify(B_str + U_inv * a_dot_xd) == 0)
check("S3.3 structure C = theta == 0, and A is generically nonzero, so the relation "
      "B = -(u.xdot) A is a genuine RANK-ONE collapse and not a trivial 0 = 0: the "
      "three structures carry ONE scalar between them and c_C is unobservable",
      theta_i == 0 and not sp.simplify(A_str) == 0)

sub_comov = {xd0: u_up_i[0], xd1: u_up_i[1]}
check("S3.4 *** THEOREM T1-B (co-moving vanishing) ***: at xdot^mu = u^mu all three "
      "structures vanish IDENTICALLY -- A = B = (a.u) = 0 by u.u = -1, and "
      "C = theta = 0. In branch (i) the co-moving probe IS the probe at rest, so the "
      "one-du sector produces NO static force.",
      sp.simplify(A_str.subs(sub_comov)) == 0 and
      sp.simplify(B_str.subs(sub_comov)) == 0 and theta_i == 0)

sub_num = {Nf: 1 - sp.Rational(1, 1000) / r2, Af: 1}
sub_pt = {r2: 2, xd0: sp.Rational(11, 10), xd1: sp.Rational(1, 3)}
A_num = float(sp.N(A_str.subs(sub_num).doit().subs(sub_pt)))
B_num = float(sp.N(B_str.subs(sub_num).doit().subs(sub_pt)))
check("S3.5 the theorem is not vacuous: for a MOVING probe (xdot != u) A and B are "
      "generically nonzero (|A|, |B| > 1e-8) -- the sector exists, it is just "
      "proportional to motion relative to the condensate",
      abs(A_num) > 1e-8 and abs(B_num) > 1e-8)

print("  ALL ORDERS IN du: since Nabla u = -u (x) a in branch (i), every scalar built")
print("  from any number of Nabla u's contracted with u and xdot is a polynomial in")
print("  (u.xdot), (a.xdot) and (a.a). (a.a) is a pure POSITION function; every term")
print("  with a free xdot index carries (a.xdot), which T1-B kills.")
DD = sp.simplify(sum(g2i[al, be] * D_i[mu][al] * D_i[nu][be] * xd_up[mu] * xd_up[nu]
                     for mu in range(2) for nu in range(2)
                     for al in range(2) for be in range(2)))
a_dot_a = sp.simplify(sum(g2i[mu, nu] * a_lo_i[mu] * a_lo_i[nu]
                          for mu in range(2) for nu in range(2)))
check("S3.6 degree-2 example: xd^m xd^n (Nabla_m u_al)(Nabla_n u_be) g^{al be} == "
      "(u.xdot)^2 (a.a), confirming the invariant ring is generated by "
      "{(u.xdot), (a.xdot), (a.a)}",
      sp.simplify(DD - U_inv**2 * a_dot_a) == 0)
check("S3.7 and (a.a) = (N'/N)^2/A is a pure POSITION function -- no xdot in it. So "
      "(a.a) terms are POTENTIALS: they EVADE T1-B (this is the against-interest "
      "escape, priced in Section 5) but can never produce non-analytic |a_probe|",
      sp.simplify(a_dot_a - sp.diff(Nf, r2)**2 / (Af * Nf**2)) == 0 and
      not a_dot_a.has(xd0) and not a_dot_a.has(xd1))

# ===========================================================================
# SECTION 4 -- THEOREM T1-B': the circular-orbit cancellation, and the price
# ===========================================================================
print("\n--- Section 4: the circular-orbit equation of motion (T1-B') ---")

tau = sp.Symbol('tau', real=True)
Uf = sp.Function('U')(tau)
Phit = sp.Function('Phi_t')(tau)
hf = sp.Function('h')
check("S4.1 integration by parts: h(U)(a.xdot) = d/dtau[h(U) Phi] - Phi h'(U) dU/dtau "
      "since (a.xdot) = dPhi/dtau in branch (i). So the c_A piece (h constant) is a "
      "TOTAL DERIVATIVE and drops from the EOM entirely",
      sp.simplify(sp.diff(hf(Uf) * Phit, tau)
                  - (hf(Uf) * sp.diff(Phit, tau)
                     + sp.diff(hf(w), w).subs(w, Uf) * sp.diff(Uf, tau) * Phit)) == 0)

# the exact non-relativistic reduction: L_t/m = l h~(Utilde) (v . grad Phi),
# Utilde = 1 + Phi + v^2/2 + ..., so the sector is spanned by Phi^k (v^2)^m (v.grad Phi)
uv, Phv = sp.symbols('u_v Ph_v', real=True)
Ut = 1 + Phv + uv**2 / 2
check("S4.2 the non-relativistic reduction: (u.xdot) = -(1+Phi) gamma so "
      "Utilde = 1 + Phi + v^2/2 + O(4), and dtau/dt x gamma = 1, giving the exact "
      "coordinate-time Lagrangian L_t/m = l h~(Utilde) (v . grad Phi). Expanding h~ "
      "therefore spans exactly the terms Phi^k (v^2)^m (v . grad Phi).",
      sp.simplify(sp.series(-(1 + Phv) / sp.sqrt(1 - uv**2), uv, 0, 4).removeO()
                  + 1 + Phv + (1 + Phv) * uv**2 / 2) == 0)

# *** the cancellation, computed for a general Phi(r) on a general planar orbit ***
tt = sp.Symbol('t_c', positive=True)
Rr, omc = sp.symbols('R_c om_c', positive=True)
x1, x2, v1, v2 = sp.symbols('x1 x2 v1 v2', real=True)
rrx = sp.sqrt(x1**2 + x2**2)
Phg = sp.Function('Phi_g')(rrx)
gradPh = [sp.diff(Phg, x1), sp.diff(Phg, x2)]
vdotg = v1 * gradPh[0] + v2 * gradPh[1]
v2sq = v1**2 + v2**2

PATHS = {"circular": (Rr * sp.cos(omc * tt), Rr * sp.sin(omc * tt)),
         "eccentric": (Rr * sp.cos(omc * tt),
                       sp.Rational(13, 10) * Rr * sp.sin(omc * tt))}


def el_on_path(k, m, path):
    L = Phg**k * v2sq**m * vdotg
    dv = [sp.diff(L, v1), sp.diff(L, v2)]
    dx = [sp.diff(L, x1), sp.diff(L, x2)]
    X1, X2 = path
    sb = {x1: X1, x2: X2, v1: sp.diff(X1, tt), v2: sp.diff(X2, tt)}
    return [sp.simplify(sp.diff(dv[i].subs(sb), tt) - dx[i].subs(sb))
            for i in range(2)]


grid = [(k, m) for k in (0, 1, 2) for m in (0, 1, 2)]
circ_zero, ecc_nonzero = {}, {}
for (k, m) in grid:
    circ_zero[(k, m)] = all(e == 0 for e in el_on_path(k, m, PATHS["circular"]))
    ecc_nonzero[(k, m)] = any(e != 0 for e in el_on_path(k, m, PATHS["eccentric"]))
print("  Euler-Lagrange of Phi^k (v^2)^m (v . grad Phi), generic Phi(r):")
for (k, m) in grid:
    print(f"    k={k}, m={m}: circular -> "
          f"{'ZERO' if circ_zero[(k,m)] else 'nonzero'}   eccentric -> "
          f"{'nonzero' if ecc_nonzero[(k,m)] else 'ZERO'}")
check("S4.3 *** THEOREM T1-B' (circular-orbit cancellation) ***: for an ARBITRARY "
      "potential Phi(r), the Euler-Lagrange equations of Phi^k (v^2)^m (v . grad Phi) "
      "vanish IDENTICALLY on a circular orbit for every k, m in {0,1,2}. The "
      "total-derivative pieces drop and the two survivors cancel because omega = v/r. "
      "So the WHOLE one-du sector, to all orders in the free function h, contributes "
      "EXACTLY ZERO to the equation that sets a rotation curve.",
      all(circ_zero.values()))
# T1-B' beyond the polynomial grid: higher orders, the EXACT relativistic gamma, and a
# transcendental case, tested by exact rational evaluation at random points with a
# concrete transcendental Phi(r) (symbolic simplify of these is prohibitively slow).
import random
random.seed(20260807)
PhF = sp.Function('Phi_g')


def el_raw(L, path):
    dv = [sp.diff(L, v1), sp.diff(L, v2)]
    dx = [sp.diff(L, x1), sp.diff(L, x2)]
    X1, X2 = path
    sb = {x1: X1, x2: X2, v1: sp.diff(X1, tt), v2: sp.diff(X2, tt)}
    return [sp.diff(dv[i].subs(sb), tt) - dx[i].subs(sb) for i in range(2)]


HARD = {"Phi^0 (v^2)^3          ": v2sq**3 * vdotg,
        "Phi^3 (v^2)^1          ": Phg**3 * v2sq * vdotg,
        "EXACT gamma = 1/sqrt(1-v^2)": vdotg / sp.sqrt(1 - v2sq)}
def hard_worst(L_h, path):
    """Max |EL| at random rational points, with a concrete TRANSCENDENTAL Phi(r).
    Evaluated at 40 digits (sp.N, no simplify: simplify on these is the slow step and
    40-digit evaluation is a sound zero test at this size)."""
    EL_h = el_raw(L_h, path)
    worst = 0.0
    for _ in range(2):
        sub = {Rr: sp.Rational(random.randint(2, 9), 7),
               omc: sp.Rational(random.randint(1, 5), 11),
               tt: sp.Rational(random.randint(1, 9), 13)}
        for e in EL_h:
            ev = e.subs(sub).replace(PhF, lambda a: sp.log(1 + a) + a**2 / 3)
            worst = max(worst, abs(float(sp.N(ev.doit(), 40))))
    return worst


hard_max, hard_ecc_min = 0.0, np.inf
for nm_h, L_h in HARD.items():
    wc = hard_worst(L_h, PATHS["circular"])
    we = hard_worst(L_h, PATHS["eccentric"])
    hard_max = max(hard_max, wc)
    hard_ecc_min = min(hard_ecc_min, we)
    print(f"    {nm_h}: max |EL| circular = {wc:.3e}, eccentric = {we:.3e}")
check("S4.3b T1-B' BEYOND THE POLYNOMIAL GRID: the cancellation also holds for "
      "(v^2)^3, Phi^3 (v^2), and the EXACT relativistic 1/sqrt(1-v^2) -- a "
      "NON-POLYNOMIAL function of the velocity -- at random rational points with a "
      "transcendental Phi(r) = ln(1+r) + r^2/3. |EL| < 1e-25 on the circular orbit "
      "and > 1e-6 on the eccentric one (a 19-order separation at 40-digit precision), "
      "so the cancellation is a property of the STRUCTURE [any function of (Phi, v^2)] "
      "x (v . grad Phi), not of a truncation, a coordinate choice, or a vanishing "
      "integrand.",
      hard_max < 1e-25 and hard_ecc_min > 1e-6)
check("S4.4 NON-VACUITY CONTROL for T1-B': on an ECCENTRIC orbit (same terms, ellipse "
      "of axis ratio 1.3) the m >= 1 terms are NONZERO while the m = 0 terms stay "
      "zero (they are the total derivatives). The cancellation is a property of "
      "circular orbits, not of the differentiator.",
      all(ecc_nonzero[(k, m)] for k in (0, 1, 2) for m in (1, 2)) and
      all(not ecc_nonzero[(k, 0)] for k in (0, 1, 2)))

# the eccentric-orbit price
R0 = 8.122 * kpc
v0 = 233.1e3
omega0 = v0 / R0
beta0 = v0 / c_light
print(f"\n  MW solar circle: R0 = {R0:.4e} m, v_c = {v0/1e3:.1f} km/s, "
      f"v/c = {beta0:.4e}, omega = {omega0:.4e} 1/s")
print("  eccentric channel: a_extra ~ l c_B (v/c)^3 omega^2  (the (v/c)^3 of the "
      "surviving\n  v^2 (v.grad Phi) term; the (v/c) piece is the corpus Frenet fact)")
price = {}
for nm, a0 in FOOTINGS:
    price[nm] = a0 / (beta0**3 * omega0**2)
    print(f"    required l*c_B ({nm:9s}) = {price[nm]:.4e} m = "
          f"{price[nm]/R_H:.3e} Hubble radii")
check("S4.5 THE PRICE on eccentric orbits, both footings: delivering an extra "
      "acceleration of order a_0 needs l*c_B = 1.4e3 (canonical) / 1.7e3 (ALT) "
      "HUBBLE RADII. No EFT with cutoff at or above H admits that, so the one-du "
      "sector is dead on circular orbits by T1-B' and dead on eccentric orbits by "
      "prefactor. FOOTING-INDEPENDENT.",
      1e3 < price["canonical"] / R_H < 2e3 and 1e3 < price["ALT"] / R_H < 2e3)
check("S4.6 and the two prices differ by EXACTLY the footing ratio 1.2082, because "
      "the price is linear in a_0 -- no footing choice can rescue it",
      abs(price["ALT"] / price["canonical"] - a0_alt / a0_can) < 1e-12)
print("  P4 (structural): T1-B' + S4.4 together predict ZERO rotation-curve signature")
print("     with a NONZERO eccentric-orbit effect -- the signature would live in")
print("     de/dt, not in v(r). That is the opposite of what MOND phenomenology needs.")

# ===========================================================================
# SECTION 5 -- the escape that evades T1-B: the (a.a) potential channel
# ===========================================================================
print("\n--- Section 5: AGAINST INTEREST -- the (a.a) channel, whose price IS affordable ---")

ell, cD = sp.symbols('ell c_D', positive=True)
g_of_r = sp.Function('g_bar')(r2)
# L/m = l^2 c_D (a.a) = l^2 c_D (g_bar/c^2)^2 -> extra force = -grad of that
a_extra_sym = sp.simplify(-cc_s**2 * ell**2 * cD
                          * sp.diff((g_of_r / cc_s**2)**2, r2))
check("S5.1 the (a.a) channel is a POTENTIAL: L/m = l^2 c_D (a.a) = "
      "l^2 c_D (g_bar/c^2)^2 gives an extra acceleration -(l^2 c_D/c^2) d(g_bar^2)/dr, "
      "which is nonzero for a probe AT REST -- it genuinely evades T1-B and T1-B'",
      sp.simplify(a_extra_sym + (ell**2 * cD / cc_s**2)
                  * sp.diff(g_of_r**2, r2)) == 0)

g_mw = v0**2 / R0
gp_mw = 2 * g_mw / R0                             # |dg/dr| for g ~ r^-2
need = {}
for nm, a0 in FOOTINGS:
    need[nm] = np.sqrt(a0 * c_light**2 / (2 * g_mw * gp_mw))
    print(f"  required l (c_D = 1), {nm:9s}: {need[nm]:.4e} m = "
          f"{need[nm]/(1e3*kpc):.3f} Mpc = {need[nm]/R_H:.3e} Hubble radii")
check("S5.2 *** AGAINST INTEREST: THIS CHANNEL'S PREFACTOR IS AFFORDABLE. *** "
      "Delivering an extra acceleration of order a_0 at the MW solar circle needs "
      "l ~ 3-4 Mpc, i.e. ~6e-4 Hubble radii -- comfortably inside any sane EFT, "
      "unlike every other channel in this lane. It must be killed on shape instead.",
      all(1e-4 < need[nm] / R_H < 1e-2 for nm, _ in FOOTINGS))

pexp = sp.Symbol('p_exp', real=True)
# need d(g^2)/dr ~ sqrt(a_0 g) for a MOND boost; g ~ r^-p
lhs_exp = -2 * pexp - 1
rhs_exp = -pexp / 2
p_sol = sp.solve(sp.Eq(lhs_exp, rhs_exp), pexp)
check("S5.3 THE SHAPE KILL: a MOND boost needs d(g_bar^2)/dr ~ sqrt(a_0 g_bar). For "
      "g_bar ~ r^(-p) the left side goes as r^(-2p-1) and the right as r^(-p/2), so "
      "matching forces p = -2/3, i.e. g_bar GROWING as r^(2/3). No mass distribution "
      "does that. The channel is excluded on SHAPE at every radius.",
      len(p_sol) == 1 and sp.nsimplify(p_sol[0]) == sp.Rational(-2, 3))
print("    point mass  (g ~ r^-2): extra force ~ r^-5, i.e. x1/32 per doubling of r")
print("    flat region (g ~ r^-1): extra force ~ r^-3, i.e. x1/8  per doubling of r")
print("    MOND boost            : ~ r^-1,             i.e. x1/2  per doubling of r")
check("S5.4 NEGATIVE CONTROL on the shape kill: p = 2 (point mass) and p = 1 (flat "
      "region) both give -2p-1 (= -5, -3) different from the MOND requirement -1, so "
      "S5.3 is a real constraint and not an identity",
      abs(float(lhs_exp.subs(pexp, 2)) + 5) < 1e-12 and
      abs(float(lhs_exp.subs(pexp, 1)) + 3) < 1e-12 and
      float(lhs_exp.subs(pexp, 2)) != -1.0)

print("\n  INDEPENDENT PREDICTION P1: with l fixed, a_extra ~ g_bar^2/r ~ v^4/r^3, so "
      "the\n  channel's emergent scale is NOT universal:")
systems = {"dwarf  v= 20 km/s, r= 2 kpc": (20e3, 2 * kpc),
           "LSB    v= 80 km/s, r= 8 kpc": (80e3, 8 * kpc),
           "MW     v=233 km/s, r=8.1 kpc": (v0, R0),
           "bright v=300 km/s, r=20 kpc": (300e3, 20 * kpc)}
scal = {}
for lab, (vv_, rr_) in systems.items():
    scal[lab] = vv_**4 / rr_**3
    print(f"    {lab:29s}: v^4/r^3 = {scal[lab]:.4e}")
dex = np.log10(max(scal.values()) / min(scal.values()))
allowed_dex = np.log10(1.16)
print(f"    range = {dex:.2f} dex; the a_0-line's +-16% box allows "
      f"~{allowed_dex:.3f} dex")
check("S5.5 PREDICTION P1 IS FALSIFIED: the affordable channel's emergent scale "
      f"varies by {dex:.2f} dex across SPARC-like systems while the a_0-line caps a_0 "
      "variation at ~0.06 dex -- a factor ~30 in the exponent. It cannot be a "
      "universal a_0 even after tuning l per galaxy.",
      dex > 1.5 and dex / allowed_dex > 20)

# ===========================================================================
# SECTION 6 -- THEOREM T1-C: the exponent census and whether a_0 is forced
# ===========================================================================
print("\n--- Section 6: field-sector branch (iii), the exponent census (T1-C) ---")

n_s = sp.Symbol('n_s', positive=True)
Aamp, k_s = sp.symbols('A_amp k_s', positive=True)
rr = sp.Symbol('rr', positive=True)
psip = Aamp * rr**(-k_s)
lg = sp.expand(sp.log(sp.simplify(rr**2 * (psip**2)**n_s * psip)), force=True)
k_sol = sp.solve(sp.Eq(lg.coeff(sp.log(rr)), 0), k_s)
check("S6.1 EXPONENT LAW: r^2 P'(dX) psi' = C with P' ~ dX^n and dX ~ psi'^2 forces "
      "psi' ~ r^(-2/(2n+1)) -- solved, not asserted",
      len(k_sol) == 1 and sp.simplify(k_sol[0] - 2 / (2 * n_s + 1)) == 0)
n_mond = sp.solve(sp.Eq(2 / (2 * n_s + 1), 1), n_s)
check("S6.2 THEOREM T1-C: MOND needs the scalar force ~ 1/r, i.e. exponent 1, which "
      "forces n = 1/2 EXACTLY -- P'(X) ~ sqrt(X - X_0), NON-ANALYTIC at the "
      "attractor. No analytic P has that as its leading Taylor tail.",
      len(n_mond) == 1 and sp.nsimplify(n_mond[0]) == sp.Rational(1, 2))
check("S6.3 an ANALYTIC P (leading n = 1, P'' finite) predicts psi' ~ r^(-2/3), "
      "not r^(-1)",
      sp.simplify((2 / (2 * n_s + 1)).subs(n_s, 1) - sp.Rational(2, 3)) == 0)
check("S6.4 NEGATIVE CONTROL: asserting that n = 1 gives MOND fails the exponent "
      "test (2/3 != 1), so S6.2 is a real constraint",
      not quiet(abs(float(2 / (2 * 1 + 1)) - 1.0) < 1e-9))

xg = sp.Symbol('x_g', positive=True)
zq = sp.Symbol('z_q', real=True)
roots = sp.solve(sp.Eq(zq**2 + zq, xg**2), zq)
y_pos = [rt for rt in roots if sp.simplify(sp.limit(rt, xg, sp.oo)) == sp.oo]
mu_x = sp.simplify(y_pos[0] / xg)
check("S6.5 the framework's law g_obs^2 = g_bar^2 + a_0 g_bar inverts to "
      "mu(x) = g_bar/g_obs = (sqrt(1+4x^2)-1)/(2x), x = g_obs/a_0. (CREDIT: the "
      "kernel nu = sqrt(1+1/y) and the dS-Unruh balance are Milgrom 1999 PLA "
      "253:273 eqs 6-9, who fixes a_0_hat = 2 c H_Lambda; the framework's "
      "distinctive content is the c H_Lambda/Z coefficient plus the MI completion.)",
      sp.simplify(mu_x - (sp.sqrt(1 + 4 * xg**2) - 1) / (2 * xg)) == 0)
check("S6.6 mu(x) -> x as x -> 0, so the AQUAL kinetic function obeys f'(z) = "
      "mu(sqrt z) -> sqrt z: THE FRAMEWORK'S OWN KERNEL IS EXACTLY the n = 1/2 "
      "non-analytic branch of T1-C. Its MOND-ness and its non-analyticity are one "
      "statement (AQUAL: Bekenstein and Milgrom 1984).",
      sp.simplify(sp.limit(mu_x / xg, xg, 0) - 1) == 0)

# is a_0 forced? the Jacobian test
P0_s, alpha_s = sp.symbols('P0_s alpha_s', positive=True)
G_s2, c_s2b = sp.symbols('G_s2 c_s2b', positive=True)
rhoL_e = P0_s                                    # rho_Lambda = -P(X_0); P0_s = -P(X_0)
a0_e = alpha_s / (12 * sp.pi * G_s2 * p_half)     # AQUAL deep-limit identification
kap_e = sp.simplify(a0_e / (c_s2b * sp.sqrt(G_s2 * rhoL_e)))
Jac = sp.Matrix([[sp.diff(rhoL_e, P0_s), sp.diff(rhoL_e, p_half)],
                 [sp.diff(a0_e, P0_s), sp.diff(a0_e, p_half)]])
detJ = sp.simplify(Jac.det())
check("S6.7 THE COEFFICIENT IS NOT FORCED: with rho_Lambda = -P(X_0) and the deep "
      "limit fixing a_0 ~ alpha/(12 pi G p_half), the Jacobian of (rho_Lambda, a_0) "
      "with respect to (P(X_0), p_half) has NONZERO determinant, so a_0 is NOT a "
      "function of rho_Lambda alone. d kappa/d p_half != 0 at fixed rho_Lambda.",
      sp.simplify(detJ) != 0 and sp.simplify(sp.diff(kap_e, p_half)) != 0)
sol_ph = sp.solve(sp.Eq(kap_e, sp.Rational(1, 2)), p_half)
check("S6.8 and kappa = 1/2 IS reachable -- by SOLVING for p_half at any alpha. One "
      "equation, two unknowns (p_half, alpha): a ONE-PARAMETER FAMILY of condensates "
      "hits the canonical footing and another hits ALT. That is a FIT, not a "
      "derivation. *** MOND STRUCTURE WITH A FITTED COEFFICIENT. ***",
      len(sol_ph) == 1 and sp.simplify(sp.diff(sol_ph[0], alpha_s)) != 0)
for nm, a0 in FOOTINGS:
    print(f"  master formula either way, {nm:9s}: r = 2 c H_L/a_0 = {2*cHL/a0:.6f}"
          f"   (canonical target 2Z = {2*Z_num:.6f})")
print("  Free numbers entering a_0 here: p_half, alpha  (c_A drops as a total")
print("  derivative, c_C drops because theta = 0, c_B is dead by T1-B'/price).")
print("  Nothing in this lane derives r, or kappa, on either footing.")

cs2 = sp.simplify(Pp_req / (Pp_req + 2 * X_s * sp.diff(P_req, X_s, 2)))
dX = sp.Symbol('dX', positive=True)
cs2_law = sp.simplify(cs2.subs(X_s, X0_s + dX))
cs2_at = sp.limit(cs2_law, dX, 0, '+')
lead_cs = sp.simplify(sp.limit(cs2_law / dX, dX, 0, '+'))
print(f"\n  PREDICTION P3: c_s^2 -> {cs2_at} at the attractor, with "
      f"c_s^2 = (dX) x {lead_cs} + ...")
check("S6.9 PREDICTION P3: on the n = 1/2 branch the condensate SOUND SPEED VANISHES "
      "at the attractor, c_s^2 -> 0 linearly in (X - X_0) with slope 1/X_0 -- the "
      "sound speed goes to zero exactly where MOND turns on. A NEW liability against "
      "this corpus's 'Jeans dS-cured' standing. Recorded AGAINST INTEREST.",
      cs2_at == 0 and sp.simplify(lead_cs - 1 / X0_s) == 0)

print("\n  PREDICTION P2: rotation-curve shape of the two non-MOND branches")
shapes = []
for lab, kexp in (("analytic P, n = 1 (psi' ~ r^-2/3)", sp.Rational(2, 3)),
                  ("stay-on-attractor (psi' ~ r^-1/2)", sp.Rational(1, 2))):
    p_v = sp.Rational(1, 2) * (1 - kexp)
    shapes.append(float(10**float(p_v)))
    print(f"    {lab:38s}: v ~ r^{p_v} -> x{shapes[-1]:.3f} per decade in r")
check("S6.10 PREDICTION P2 IS FALSIFIED: the non-MOND branches predict RISING "
      "rotation curves, v ~ r^(1/6) (x1.468/decade) and v ~ r^(1/4) (x1.778/decade). "
      "Flat curves exclude both far beyond the 10% level.",
      abs(shapes[0] - 1.4678) < 1e-3 and abs(shapes[1] - 1.7783) < 1e-3)

kx = sp.Symbol('kx', real=True)
k_needed = sp.solve(sp.Eq(2 + kx, 1), kx)
check("S6.11 structure C in the CHARGED branch (the only branch where theta != 0): "
      "theta ~ r^(-1-k) so the force from Int dtau c_C theta goes as r^(-2-k); MOND "
      "needs k = -1, i.e. psi' GROWING linearly in r. Unphysical -- closing the last "
      "one-du structure.",
      len(k_needed) == 1 and sp.nsimplify(k_needed[0]) == -1)

print("\n  REFINEMENT (numerical, step x1/4). Solve (w^2 + b/x)^n w = 1/x^2 for w(x),")
print("  where b/x is the METRIC contribution to dX (Section 2: dX gets a piece from")
print("  N as well as from psi'), and measure the local log-slope. TWO regimes exist.")


def solve_w(xv, nn, bb):
    def f(wv):
        return (wv**2 + bb / xv)**nn * wv - 1.0 / xv**2
    return brentq(f, 1e-40, 1e40, xtol=1e-300, rtol=1e-15, maxiter=500)


def logslope(xv, nn, bb, hstep):
    return (np.log(solve_w(xv * np.exp(hstep), nn, bb))
            - np.log(solve_w(xv * np.exp(-hstep), nn, bb))) / (2 * hstep)


XV = 1e6
refine = []
for regime, bb, expect in (("gradient-dominated", 1e-15, lambda n: -2.0 / (2 * n + 1)),
                           ("metric-dominated  ", 1.0, lambda n: n - 2.0)):
    for nn in (1.0, 0.5):
        got = []
        for lab, hstep in (("h", 1e-2), ("h/4", 2.5e-3)):
            sl = logslope(XV, nn, bb, hstep)
            got.append(sl)
            print(f"    {regime}  n = {nn:.1f}, step {lab:3s}: slope = {sl:.10f}, "
                  f"predicted = {expect(nn):.10f}, |shift| = {abs(sl-expect(nn)):.3e}")
        refine.append((regime.strip(), nn, got[0], got[1], expect(nn)))
check("S6.12 REFINEMENT (step refined 4x, two regimes): the measured log-slope matches "
      "the analytic exponent in BOTH regimes for BOTH n = 1 and n = 1/2 to < 1e-5, and "
      "refining the step 4x moves each answer by < 1e-8 -- converged, not a "
      "coarse-grid artefact",
      all(abs(rp[2] - rp[4]) < 1e-5 and abs(rp[3] - rp[4]) < 1e-5 for rp in refine) and
      all(abs(rp[2] - rp[3]) < 1e-8 for rp in refine))
check("S6.13 NEGATIVE CONTROL on the solver: it must DISCRIMINATE, and it does -- "
      "gradient-dominated gives -0.666667 (n=1) and -1.000000 (n=1/2), while "
      "metric-dominated gives -1.000000 (n=1) and -1.500000 (n=1/2). A solver "
      "returning one number for all four would fail here.",
      abs(refine[0][2] + 2 / 3) < 1e-5 and abs(refine[1][2] + 1.0) < 1e-5 and
      abs(refine[2][2] + 1.0) < 1e-5 and abs(refine[3][2] + 1.5) < 1e-5 and
      abs(refine[1][2] - refine[3][2]) > 0.1)

# what that means for the MOND tail -- a NEW condition, stated honestly
nq = sp.Symbol('n_q', positive=True)
cond = sp.solve(sp.Eq(2 * (nq - 2), -1), nq)      # w^2 ~ b/x at the metric branch
check("S6.14 CONSEQUENCE (new, and it TIGHTENS T1-C): in the metric-dominated regime "
      "w ~ x^(n-2), which for n = 1/2 is r^(-3/2) -- NOT MOND's r^(-1). So the "
      "n = 1/2 MOND tail exists ONLY where the psi' term dominates dX, i.e. only "
      "where psi'^2 >> 2 phi0^2 |Phi|. That is an EXTRA condition on the condensate "
      "scale phi0, and the attractor does not supply it. Verified: the metric branch "
      "w = x^(n-2)/b^n is self-consistent (w^2 < b/x) exactly for n < 3/2, which "
      "includes both n = 1/2 and n = 1.",
      len(cond) == 1 and sp.nsimplify(cond[0]) == sp.Rational(3, 2) and
      abs(refine[3][2] + 1.5) < 1e-5)
print("  AND the two pieces of dX enter with OPPOSITE signs (Section 2: dX = "
      "phi0^2(1/N^2-1)\n  - psi'^2/A, and 1/N^2 - 1 = -2 Phi > 0 for attractive "
      "gravity). Under the other\n  sign convention for the non-analytic branch, "
      "positivity of dX FORBIDS the\n  gradient-dominated regime outright, leaving "
      "only the r^(-3/2) tail. Either way\n  the MOND tail is conditional, not "
      "forced.")

# ===========================================================================
# SECTION 7 -- EFE / external-field behaviour (lane point 5)
# ===========================================================================
print("\n--- Section 7: external-field behaviour of the sourced profile ---")

aext_c = sp.Symbol('a_ext_c', positive=True)
g2_e = sp.diag(-(1 + aext_c * r2)**2, 1)
g2i_e = g2_e.inv()
Gam_e = christoffel(g2_e, g2i_e, crd2)
u_lo_e = [-(1 + aext_c * r2), 0]
D_e = [[sp.simplify(sp.diff(u_lo_e[nu], crd2[mu])
                    - sum(Gam_e[lam][mu][nu] * u_lo_e[lam] for lam in range(2)))
        for nu in range(2)] for mu in range(2)]
u_up_e = [sp.simplify(sum(g2i_e[mu, nu] * u_lo_e[nu] for nu in range(2)))
          for mu in range(2)]
a_lo_e = [sp.simplify(sum(u_up_e[mu] * D_e[mu][nu] for mu in range(2)))
          for nu in range(2)]
check("S7.1 STRUCTURAL EFE: for a uniform external field N = 1 + a_ext x/c^2 the "
      "condensate congruence acceleration is a_r = a_ext/(1 + a_ext x) != 0 -- it does "
      "NOT cancel, because u is tied to the CONDENSATE and not to the local free-fall "
      "frame. That is the correct structural origin of the framework's EFE.",
      sp.simplify(a_lo_e[1] - aext_c / (1 + aext_c * r2)) == 0)
A_e = sp.simplify(sum(u_up_e[mu] * xd_up[nu] * D_e[mu][nu]
                      for mu in range(2) for nu in range(2)))
check("S7.2 but T1-B applies here too, COMPUTED in the external-field metric: at "
      "xdot = u the structure A vanishes again, while it is nonzero for a moving "
      "probe. So this sector produces neither a MOND boost NOR the l = 0 constant "
      "a_0/2 sunward term that costs the exact law 1278x the Earth/Mars bound. "
      "AGAINST INTEREST: favourable, and worthless, since there is no MOND either.",
      sp.simplify(A_e.subs({xd0: u_up_e[0], xd1: u_up_e[1]})) == 0 and
      sp.simplify(A_e.subs({xd0: 1, xd1: 1})) != 0)

g_int_s, a0_s, aext_s = sp.symbols('g_int a0_e a_ext', positive=True)
nu_eff = sp.diff(sp.sqrt((g_int_s + aext_s)**2 + a0_s * (g_int_s + aext_s)), g_int_s)
print("  EFE on the framework's own a_0-line, nu_eff = d g_obs/d g_bar at "
      "g_bar = g_int + a_ext:")
efe = []
for nm, a0 in FOOTINGS:
    row = [float(nu_eff.subs({g_int_s: 0.1 * a0, aext_s: q * a0, a0_s: a0}))
           for q in (0.0, 0.5, 1.0, 2.0, 10.0)]
    efe.append((nm, row))
    print(f"    {nm:9s} (g_int = 0.1 a_0), a_ext/a_0 = 0, 0.5, 1, 2, 10: "
          + ", ".join(f"{q:.4f}" for q in row))
print("  the two rows are IDENTICAL, and that is the correct answer, not a bug: with "
      "both\n  g_int and a_ext measured in units of a_0, nu_eff depends only on "
      "RATIOS, so the EFE\n  shape is exactly footing-blind. Only its LOCATION in "
      "physical acceleration moves.")
check("S7.3 EFE SIGN AND MONOTONICITY, both footings: nu_eff falls STRICTLY as a_ext "
      "grows and tends to 1 -- the external field SUPPRESSES the boost and restores "
      "Newton, qualitatively matching the framework's EFE",
      all(all(row[i] > row[i + 1] for i in range(len(row) - 1)) for _, row in efe) and
      all(abs(row[-1] - 1.0) < 0.06 for _, row in efe))
check("S7.4 AGAINST INTEREST: EFE follows from CONCAVITY alone (d^2 g_obs/d g_bar^2 "
      "< 0 for the a_0-line), so reproducing it qualitatively is NOT evidence for the "
      "tree-level route -- any concave kernel does it",
      float(sp.diff(sp.sqrt(g_int_s**2 + a0_s * g_int_s), g_int_s, 2)
            .subs({g_int_s: 0.1 * a0_can, a0_s: a0_can})) < 0)

# ===========================================================================
# SECTION 8 -- Ostrogradsky and derivative order (lane point 6)
# ===========================================================================
print("\n--- Section 8: derivative order and Ostrogradsky ---")

tq = sp.Symbol('t_q', real=True)
qf = sp.Function('q_f')(tq)
ff = sp.Function('f_f')
q_s, v_s, a_s = sp.symbols('q_s v_s a_s', real=True)
PATH = {q_s: qf, v_s: sp.diff(qf, tq), a_s: sp.diff(qf, tq, 2)}


def euler_lagrange_hd(Lsym):
    """EL for L(q, qdot, qddot) given as an expression in the symbols q_s, v_s, a_s."""
    t1 = sp.diff(Lsym, q_s).subs(PATH)
    t2 = sp.diff(sp.diff(Lsym, v_s).subs(PATH), tq)
    t3 = sp.diff(sp.diff(Lsym, a_s).subs(PATH), tq, 2)
    return sp.expand(sp.simplify(t1 - t2 + t3).doit())


# sympy cannot chain-differentiate an ABSTRACT f(q(t), qdot(t)) twice, so the test runs
# on three structurally different CONCRETE f (polynomial, transcendental, mixed) AND
# against the hand-derived closed form -- a stronger check than one abstract case.
F_CASES = {"polynomial   ": q_s**2 * v_s**3 + sp.sin(q_s) * v_s,
           "transcendental": sp.exp(q_s) * sp.cos(v_s),
           "mixed        ": q_s * v_s**2 + q_s**3}
lin_ok, quad_ok, closed_ok = [], [], []
for nm_f, f_ex in F_CASES.items():
    EL_lin = euler_lagrange_hd(f_ex * a_s)
    closed = (2 * sp.diff(f_ex, q_s) * a_s + sp.diff(f_ex, q_s, 2) * v_s**2
              + sp.diff(f_ex, q_s, 1, v_s, 1) * a_s * v_s).subs(PATH)
    lin_ok.append(not EL_lin.has(sp.Derivative(qf, (tq, 3)))
                  and not EL_lin.has(sp.Derivative(qf, (tq, 4)))
                  and EL_lin.has(sp.Derivative(qf, (tq, 2))))
    closed_ok.append(sp.simplify(EL_lin - closed) == 0)
    quad_ok.append(euler_lagrange_hd(f_ex * a_s**2).has(sp.Derivative(qf, (tq, 4))))
    print(f"    f = {nm_f}: linear-in-a EL is 2nd order {lin_ok[-1]}, matches the "
          f"closed form {closed_ok[-1]}, quadratic-in-a is 4th order {quad_ok[-1]}")
check("S8.1 the one-du sector is LINEAR in xddot after by-parts, and for "
      "L = f(q, qdot) qddot the Euler-Lagrange equation is SECOND order -- the qdddot "
      "and qddot^2 terms cancel identically, giving exactly "
      "EL = 2 f_q a + f_qq v^2 + f_qv a v, verified for a polynomial, a transcendental "
      "and a mixed f. NO Ostrogradsky ghost from the probe.",
      all(lin_ok) and all(closed_ok))
check("S8.2 CONTROL (this detector can fire): the QUADRATIC-in-xddot operator DOES "
      "give a 4th-order Euler-Lagrange equation in all three cases, so S8.1 is a real "
      "distinction and not an artefact of the differentiator",
      all(quad_ok))
hf2 = sp.Function('h2')
vfun = sp.Function('v_wl')(tq)                       # v_wl(t) == qdot, so v_wl'' == qdddot
src = sp.diff(hf2(vfun), tq, 2).doit()
check("S8.3 the FIELD side pays instead: the one-du term is linear in d_m d_n phi, so "
      "varying phi puts two derivatives on the worldline delta and the source carries "
      "d^2/dt^2 h(qdot) = h'' qddot^2 + h' qdddot, i.e. THIRD worldline derivatives "
      "-- reproducing the corpus note that the b-projector costs third derivatives",
      src.has(sp.Derivative(vfun, (tq, 2))) and
      src.has(sp.Derivative(vfun, tq)**2))
check("S8.4 CONTROL: with h constant in its argument the third derivative disappears, "
      "so S8.3 detects the (u.xdot)-dependence and not a differentiation artefact",
      not sp.diff(hf2(sp.Symbol('const_v')), tq, 2).doit().has(
          sp.Derivative(vfun, (tq, 2))))

# ===========================================================================
# SECTION 9 -- dimensional-rescaling reproduction (the bug-catcher)
# ===========================================================================
print("\n--- Section 9: dimensional-rescaling reproduction ---")

L0, T0, M0 = kpc, 3.1557e13, Msun          # kpc, Myr, Msun
G_p = G_N * M0 * T0**2 / L0**3
c_p = c_light * T0 / L0
rho_p = rho_L * L0**3 / M0
a0_p = 0.5 * c_p * np.sqrt(G_p * rho_p)
a0_back = a0_p * L0 / T0**2
print(f"  in (kpc, Myr, Msun): G' = {G_p:.6e}, c' = {c_p:.6e}, rho' = {rho_p:.6e}")
print(f"  a_0' = {a0_p:.6e} kpc/Myr^2  ->  back to SI {a0_back:.6e} m/s^2")
check("S9.1 DIMENSIONAL-RESCALING REPRODUCTION: a_0 = kappa c sqrt(G rho_Lambda) "
      "recomputed entirely in (kpc, Myr, Msun) and converted back matches the SI "
      "value to 1e-12 relative", abs(a0_back - a0_can) / a0_can < 1e-12)

v_p = v0 * T0 / L0
om_p = v_p / (R0 / L0)
price_p = a0_p / ((v_p / c_p)**3 * om_p**2) * L0
check("S9.2 the LOAD-BEARING number survives the same rescaling: the eccentric-orbit "
      "price l*c_B recomputed in (kpc, Myr, Msun) and converted back matches the SI "
      "value to 1e-12 -- the 1.4e3 Hubble radii is not a units error",
      abs(price_p - price["canonical"]) / price["canonical"] < 1e-12)
g_p = v_p**2 / (R0 / L0)
need_p = np.sqrt(a0_p * c_p**2 / (2 * g_p * (2 * g_p / (R0 / L0)))) * L0
check("S9.3 and so does the AGAINST-INTEREST number: the affordable (a.a) channel's "
      "required l recomputed in (kpc, Myr, Msun) matches the SI value to 1e-12, so "
      "the '3.4 Mpc, affordable' concession is not a units artefact either",
      abs(need_p - need["canonical"]) / need["canonical"] < 1e-12)
G_bad = G_N * M0 * T0**2 / L0**2                     # wrong length exponent
a0_bad = 0.5 * c_p * np.sqrt(G_bad * rho_p) * L0 / T0**2
check("S9.4 NEGATIVE CONTROL: giving G the wrong length exponent (L^2 for L^3) breaks "
      "the rescaling reproduction by many orders -- S9.1-S9.3 are real checks",
      abs(a0_bad - a0_can) / a0_can > 1e3)

# ===========================================================================
# VERDICT
# ===========================================================================
print("\n" + SEP)
print("VERDICT -- LANE T1")
print(SEP)
print(f"""
 STEP 1 (sourced profile at tree level).  DONE, and it is not free. With no direct
   matter-phi coupling the shift current forces flux C = 0, whose regular branch is
   psi' = 0; the condensate stays co-moving with the static observer and X = X_0/N^2,
   so Nabla_mu u_nu = -u_mu a_nu EXACTLY with a_nu = d_nu ln N. Vorticity, shear and
   expansion all vanish, and
       *** d_mu u_nu near a source IS the Newtonian field: a_r = g_bar/c^2. ***  (T1-A)

 STEP 2 (worldline EOM keeping the 3 one-du structures, c_A/c_B/c_C symbolic).
   In this background A = (a.xdot), B = -(u.xdot)(a.xdot), C = theta = 0. RANK ONE:
   the three structures carry one scalar between them, c_C is unobservable, and c_A
   is a total derivative. Only c_B can act at all.

 STEP 3 (does the a_0-line come out?).  NO, and by theorems rather than estimates.
   T1-B : a.u = 0 identically, so every one-du invariant with a free xdot index
          vanishes for a probe co-moving with the condensate -- which in this branch
          is the probe AT REST. No static force, at ANY order in du.
   T1-B': *** for an arbitrary Phi(r) the Euler-Lagrange equations of the general
          term Phi^k (v^2)^m (v . grad Phi) vanish IDENTICALLY on a circular orbit
          for every k and m -- the total derivatives drop and the survivors cancel
          because omega = v/r. The whole one-du sector, to all orders in h,
          contributes EXACTLY ZERO to the equation that sets a rotation curve. ***
   The same terms are nonzero on an ECCENTRIC orbit (checked), and there the price is
   l*c_B = {price['canonical']/R_H:.0f} Hubble radii (canonical) / {price['ALT']/R_H:.0f} (ALT). Dead on circular orbits by
   theorem; dead on eccentric orbits by prefactor. T1-B' is footing-blind: it is a
   cancellation with no scale in it.

 STEP 4 (is a_0 forced to kappa c sqrt(G rho_Lambda) with kappa DETERMINED?).  NO.
   The only route that does give MOND is the field sector, and T1-C shows it needs
   P'(X) ~ sqrt(X - X_0) -- n = 1/2 EXACTLY, which is also precisely what this
   framework's own kernel demands, since f'(z) = (sqrt(1+4z)-1)/(2 sqrt z) -> sqrt z.
   The attractor fixes ONE datum, -P(X_0) = rho_Lambda; p_half and the matter coupling
   alpha are independent, the Jacobian is nonsingular, and kappa = 1/2 is one equation
   in two unknowns. In the words the brief asked for:
       *** MOND STRUCTURE WITH A FITTED COEFFICIENT. ***
   Master formula either way: r = 2 c H_L/a_0 = {2*cHL/a0_can:.6f} (canonical, = 2Z to 5e-5)
   and {2*cHL/a0_alt:.6f} (ALT). Nothing here derives either.

 STEP 5 (EFE).  Structurally YES, dynamically MOOT. u is condensate-tied, not
   free-fall-tied, so a^cond = grad(Phi_int + Phi_ext) and the external field does not
   cancel -- the right structural origin for an EFE. Sign and monotonicity check out on
   both footings. AGAINST INTEREST: that follows from concavity alone, and T1-B kills
   the boost, so there is no boost left to suppress.

 STEP 6 (Ostrogradsky).  The probe is safe: linear-in-xddot gives a SECOND-order
   Euler-Lagrange equation (the control confirms the quadratic operator does not). The
   FIELD pays instead -- the phi source carries third worldline derivatives.

 THE ONE HONEST CONCESSION, stated as loudly as the kill: the two-du invariant (a.a)
 is a pure POSITION function, so it evades T1-B and T1-B' completely. Its required
 coupling is l ~ {need['canonical']/(1e3*kpc):.1f} Mpc = {need['canonical']/R_H:.1e} Hubble radii -- AFFORDABLE, unlike every other
 channel here. It dies on SHAPE: a MOND boost needs d(g_bar^2)/dr ~ sqrt(a_0 g_bar),
 forcing g_bar to GROW as r^(2/3); for a point mass the channel gives r^(-5) (x1/32 per
 doubling) and in a flat region r^(-3), against MOND's r^(-1). And with l fixed its
 emergent scale varies by {dex:.2f} dex across SPARC-like systems vs the a_0-line's 0.06 dex.

 FOUR INDEPENDENT PREDICTIONS, all of which cut against the route:
   P1 the affordable channel's scale ~ v^4/r^3 varies {dex:.2f} dex; a_0 varies <= 0.06 dex.
   P2 the non-MOND field branches predict RISING curves, v ~ r^(1/6) (x1.468/decade)
      and v ~ r^(1/4) (x1.778/decade). Flat curves exclude both.
   P3 the MOND branch forces c_s^2 -> 0 linearly in (X - X_0): the condensate sound
      speed vanishes exactly where MOND turns on -- a NEW liability against this
      corpus's own 'Jeans dS-cured' standing.
   P4 T1-B' predicts ZERO rotation-curve signature with a nonzero ECCENTRIC-orbit
      effect: the signature would live in de/dt, not in v(r). Backwards for MOND.

 STILL OPEN -- do not overstate the no-go.  T1-B/T1-B' are proven for the branch the
 shift current selects when the mass carries NO shift charge, for structures linear in
 du, on circular orbits. Untouched: shear-carrying (rotating, accreting, time-dependent)
 condensate configurations where Nabla u is not -u (x) a; invariants with two or more
 derivatives of u carrying INDEPENDENT free functions of position beyond (a.a); the
 shift-charged branch's full nonlinear solution away from its power-law tails; and the
 pure-conformal disformal sub-branch B = 0 that mi_disformal_completion_2026 explicitly
 left open. kappa = 1/2 stays FITTED, NOT DERIVED. No door is declared closed.
""")

n_ok, n_all = sum(RESULTS), len(RESULTS)
if FAILED:
    print("FAILED CHECKS:")
    for f in FAILED:
        print("  - " + f)
print(f"{n_ok}/{n_all} checks held.")
sys.exit(0 if n_ok == n_all else 1)
