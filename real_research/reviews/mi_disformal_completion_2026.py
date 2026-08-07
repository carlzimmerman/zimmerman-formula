#!/usr/bin/env python3
r"""mi_disformal_completion_2026.py -- LANE E: THE COVARIANT COMPLETION VIA THE DISFORMAL rho_m ESCAPE.

The three 2026-08-01 no-goes close the DIRECT-action route for the generic form class.  "Disformal rho_m
coupling" is on the corpus's own list of escapes NOT closed.  This script builds it and prices it.

CONSTRUCTION (as specified).  Einstein-Hilbert untouched on g.  phi = the ghost-condensate scalar the
corpus already has (shift-symmetric, no potential, u_mu = d_mu phi / sqrt(-X), X = (grad phi)^2 < 0).
Matter couples to
        g_eff_mu_nu = A(phi,X) g_mu_nu + B(phi,X) d_mu phi d_nu phi
                    = A g_mu_nu + C u_mu u_nu ,     C == -B X ,   D == A - C = A + B X .
In the local u-frame  g_eff = diag(-D, A, A, A).  Photons and gravitons stay on g.

WHAT IS DERIVED HERE (each with a runnable, failable check):
  S2  the disformal algebra: inverse, X_eff = X/D, the dof-preserving Jacobian A - X A_X - X^2 B_X.
  S3  the test-particle EOM on g_eff, weak-field slow-motion, TWO independent ways (exact circular
      geodesic vs a variable-inertial-mass Lagrangian).  The completion IS modified inertia: the
      nonrelativistic Lagrangian carries a position-dependent inertial mass M = m S / sqrt(T).
  S4  ** THE CONE IDENTITY (done EARLY, as instructed) **  matter-cone / photon-cone = D/A, exactly,
      gauge-independent, and INDEPENDENT of the conformal factor.  So the whole cone bill is charged to
      B.  Contrast: the corpus's own scalar-dressing coupling shifts the cone by EXACTLY zero.
  S5  ** NO-GO 1 (the literal (phi,X) class) **  three ways: (a) shift symmetry + the corpus's own
      ghost-condensate attractor P'(X)=0 pin X, so A,B are CONSTANTS -> no MOND at all; (b) off the
      attractor the only scalar is Phi, and nu is a function of |grad Phi| -> a two-system test at
      equal Phi fails; (c) the size needed lands inside the corpus's OWN 3.8e5-3.8e7 prefactor window
      from no-go (ii) -- the disformal escape reproduces the (v/c)^2 wall, it does not dodge it.
  S6  ** NO-GO 2 (the extended class, A,D functions of the acceleration invariant) **  the law can be
      matched for ONE geometry, forcing an ODE for A; the SAME A then mispredicts other geometries by
      0.18-0.40 dex.  Universality over the log-slope p and over system SIZE forces A,D constant.
  S7  ** THE SURVIVING BRANCH IS NONLOCAL **  D = 1 + 2(Phi_M - Phi) with Phi_M the AQUAL potential
      (the corpus's own K(Box_u)).  Cone mismatch = |Phi_M - Phi|/c^2 ~ 1e-7..1e-6 -> photon decay.
  S8  the trilemma: matter-only / matter+light / universal.  All three closed, by 1e6 to 1e15.
  S9  ** THE ONE EXACT SURVIVOR: the CONFORMAL piece (B = 0) **  cone-exact to all orders, reproduces
      the law -- but photons are conformally blind in 4D (checked in D dimensions), so it buys no
      lensing, and it is a fifth force = modified GRAVITY, not modified inertia.
  S10 ghosts: signature, invertibility, the 2x2 kinetic matrix with matter, and the Ostrogradsky
      runaway of the extended class (the hinge the corpus's OWN mi_disformal_ostrogradsky.py named).
  S11 the inherited ephemeris liability, quantified, both footings -- plus a NEW and harder statement:
      on alpha=1 the disformal completion's g_eff LOSES LORENTZIAN SIGNATURE inside Saturn's orbit.

CREDIT.  nu(y) = sqrt(1+1/y) and the dS-Unruh balance are Milgrom 1999 PLA 253:273 eqs 6-9 (he fixes
a0_hat = 2 c H_Lambda; his eqs 10-11 give a second coefficient; Milgrom 2008 arXiv:0801.3133 sec 7.3.1
calls the mismatch not necessarily meaningful).  Temperature sqrt(a^2+Lambda/3)/2pi: Narnhofer, Peter
and Thirring 1996 IJMPB 10:1507.  Five-acceleration reading: Deser and Levin 1997 CQG 14:L163.
a_lambda = c^2 sqrt(Lambda/3): Milgrom 1994 Ann.Phys. 229:384.  AQUAL: Bekenstein and Milgrom 1984.
TeVeS: Bekenstein 2004.  AeST: Skordis and Zlosnik 2021.  Disformal transformations and the
invertibility/dof condition: Bekenstein 1993; Ben Achour, Langlois and Noui 2016; DHOST: Langlois and
Noui 2016.  Ghost condensate: Arkani-Hamed, Cheng, Luty and Mukohyama 2004.  Superluminality is not by
itself acausal when a preferred foliation exists: Bruneton and Esposito-Farese 2007 -- so the kills below
are EMPIRICAL (photon decay / vacuum Cherenkov), not logical, and are labelled that way.

kappa = 1/2 is FITTED, NOT DERIVED.  Both a0 footings are carried on every dimensional number.
Nothing here derives a0, Z or the sign s.  This closes ONE listed escape; the corpus's other listed
escapes (non-quadratic-in-u, rho_m/T_munu coupling, the b-projector at third-derivative cost, finite
parts, all-orders rigidity, T_munu variation, ephemeris de/dt) are untouched and stay OPEN.

Exit non-zero on any failed internal check.
"""
from __future__ import annotations

import numpy as np
import sympy as sp
from scipy.integrate import quad, solve_ivp

# ------------------------------------------------------------------ bookkeeping
_n_ok = 0
_n_tot = 0


def check(cond: bool, msg: str) -> bool:
    global _n_ok, _n_tot
    _n_tot += 1
    if cond:
        _n_ok += 1
    print(f"  [{'OK' if cond else 'FAIL'}] {msg}")
    return bool(cond)


def banner(s: str) -> None:
    print("\n" + "=" * 104)
    print(s)
    print("=" * 104)


# ------------------------------------------------------------------ constants
C_LIGHT = 2.99792458e8
G_SI = 6.67430e-11
GM_SUN = 1.32712440018e20
AU = 1.495978707e11
KPC = 3.0856775814913673e19
MSUN = 1.98892e30
M_E_EV = 5.109989e5                     # electron mass, eV

A0 = {"canonical rho_DE, cH_L/Z": 9.3614e-11, "ALT rho_total/cH0": 1.13e-10}
CH_LAMBDA = 5.4194e-10
Z_CONST = 5.7888100366
EARTH_LIMIT = 3.66e-14                  # Earth 2-sigma on a constant sunward anomaly (corpus value)
RAR_SCATTER_INTRINSIC = 0.034           # Desmond 2023 marginalised RAR intrinsic scatter, dex
RAR_SCATTER_TOTAL = 0.11                # observed total RAR scatter, dex
# corpus no-go (ii): the u-contraction needs a prefactor |K| ~ 3.8e5 - 3.8e7 against ||K|| <= 1
PREFACTOR_WINDOW = (3.8e5, 3.8e7)


def nu_minus_1(y, alpha=1.0):
    """nu_alpha - 1 with nu_alpha = (1 + y^-alpha)^(1/(2 alpha)).  alpha=1 is the exact framework law.
    Written to avoid the catastrophic cancellation of sqrt(1+eps)-1 at large y (float64 hazard)."""
    q = np.float64(1.0) / np.asarray(y, dtype=np.float64) ** alpha
    return np.expm1(np.log1p(q) / (2.0 * alpha))


def nu(y, alpha=1.0):
    return 1.0 + nu_minus_1(y, alpha)


# ==================================================================
banner("S1.  FOOTINGS AND THE KERNEL -- both a0 values carried from here on")
# ==================================================================
a0c, a0a = A0["canonical rho_DE, cH_L/Z"], A0["ALT rho_total/cH0"]
print(f"  a0 canonical = {a0c:.4e} m/s^2   (= c H_Lambda / Z = {CH_LAMBDA/Z_CONST:.4e})")
print(f"  a0 ALT       = {a0a:.4e} m/s^2   (larger by 1/sqrt(Omega_Lambda) = {a0a/a0c:.4f})")
check(abs(CH_LAMBDA / Z_CONST / a0c - 1) < 3e-4,
      f"cH_Lambda/Z = {CH_LAMBDA/Z_CONST:.6e} reproduces the canonical a0 to "
      f"{abs(CH_LAMBDA/Z_CONST/a0c-1):.1e} (kappa = 1/2 is FITTED, not derived)")
check(abs(a0a / a0c - 1.2082) < 2e-3,
      f"ALT/canonical = {a0a/a0c:.4f} = 1/sqrt(Omega_Lambda) = 1.2082 to {abs(a0a/a0c-1.2082):.4f} "
      f"(the residual is the rounding of the quoted 1.13e-10; exact would be {a0c*1.2082:.4e})")
ysym = sp.symbols('y', positive=True)
law = sp.simplify((sp.sqrt(1 + 1 / ysym) * ysym) ** 2 - (ysym ** 2 + ysym))
check(sp.simplify(law) == 0,
      "nu = sqrt(1+1/y) is identically g_obs^2 = g_bar^2 + a0 g_bar   [Milgrom 1999 PLA 253:273 eq 9]")
check(abs(float(nu_minus_1(1e12)) - 5e-13) / 5e-13 < 1e-6,
      f"nu-1 at y=1e12 is {float(nu_minus_1(1e12)):.6e} = 1/(2y) -- the expm1/log1p form survives "
      "the cancellation that kills a direct sqrt(1+1/y)-1")

# ==================================================================
banner("S2.  THE DISFORMAL ALGEBRA:  g_eff = A g + B dphi dphi = A g + C u u,  C = -B X,  D = A + B X")
# ==================================================================
A_s, B_s, X_s = sp.symbols('A B X', real=True)
C_s = -B_s * X_s
D_s = A_s + B_s * X_s
g = sp.diag(-1, 1, 1, 1)                        # local u-frame tangent metric
uu_low = sp.diag(1, 0, 0, 0)                    # u_mu u_nu  (u_mu = (-1,0,0,0), u.u = -1)
uu_up = sp.diag(1, 0, 0, 0)                     # u^mu u^nu
g_eff = g + C_s * uu_low                        # conformal factor restored below
g_eff = A_s * g + C_s * uu_low
print(f"  g_eff_mu_nu (u-frame) = diag({sp.simplify(-A_s+C_s)}, {A_s}, {A_s}, {A_s})"
      f"   -> = diag(-D, A, A, A) with D = A - C = A + B X")
check(sp.simplify(g_eff[0, 0] + D_s) == 0, "the 00 entry is -D = -(A + B X) exactly")
eigs = sorted((sp.simplify(e) for e in sp.Matrix(g_eff).eigenvals()), key=str)
check(sp.simplify(sp.Matrix(g_eff).det() - (-D_s * A_s ** 3)) == 0,
      f"det g_eff = -D A^3 -> Lorentzian and invertible iff A > 0 AND D > 0 (eigenvalues {eigs})")

g_eff_inv = (1 / A_s) * (g.inv() - C_s / (A_s - C_s) * uu_up)
check(sp.simplify(sp.Matrix(g_eff) * sp.Matrix(g_eff_inv) - sp.eye(4)).is_zero_matrix is True,
      "inverse g_eff^{mu nu} = (1/A)[g^{mu nu} - C/(A-C) u^mu u^nu] verified: g_eff . g_eff^-1 = I")

# X_eff and the dof-preserving (invertibility) Jacobian
Af, Bf = sp.Function('A')(X_s), sp.Function('B')(X_s)
Xeff = X_s / (Af + Bf * X_s)
J = sp.simplify(sp.diff(Xeff, X_s) * (Af + Bf * X_s) ** 2)
J_target = Af - X_s * sp.diff(Af, X_s) - X_s ** 2 * sp.diff(Bf, X_s)
check(sp.simplify(J - J_target) == 0,
      "X_eff = X/(A+BX) and dX_eff/dX = [A - X A_X - X^2 B_X]/D^2, so the transformation is invertible "
      "(dof-preserving, no extra Ostrogradsky mode) IFF A - X A_X - X^2 B_X != 0  [Ben Achour+ 2016]")
J_const = sp.simplify(sp.diff(X_s / (A_s + B_s * X_s), X_s) * (A_s + B_s * X_s) ** 2)
check(sp.simplify(J_const - A_s) == 0 and sp.simplify(J_const.subs(A_s, 0)) == 0,
      f"for CONSTANT A,B the Jacobian collapses to {J_const}, so the condition is just A != 0 "
      f"(and it DOES vanish at A=0, so the test is not vacuous)")

# ==================================================================
banner("S3.  TEST-PARTICLE EOM ON g_eff, WEAK FIELD + SLOW MOTION -- derived two independent ways")
# ==================================================================
r, m = sp.symbols('r m', positive=True)
T = sp.Function('T')(r)                          # -g_eff_tt
S = sp.Function('S')(r)                          # g_eff_ij = S delta_ij (isotropic)
# (a) EXACT circular geodesic of ds^2 = -T dt^2 + S(dr^2 + r^2 dphi^2)
Gam_r_tt = sp.diff(T, r) / (2 * S)
Gam_r_pp = -sp.diff(S * r ** 2, r) / (2 * S)
Omega2 = sp.simplify(-Gam_r_tt / Gam_r_pp)
v2_exact = sp.simplify(Omega2 * r ** 2)
print(f"  (a) exact circular geodesic:  v_c^2 = {v2_exact}")
# (b) nonrelativistic variable-inertial-mass Lagrangian  L = (1/2) M v^2 - U,  M = m S/sqrt(T), U = m sqrt(T)
M_of = m * S / sp.sqrt(T)
U_of = m * sp.sqrt(T)
v2sym = sp.symbols('v2', positive=True)
# radial balance for a circular orbit (v perpendicular to grad M):  M v^2/r = U' - (1/2) v^2 M'
v2_lag = sp.simplify(sp.solve(sp.Eq(M_of * v2sym / r, sp.diff(U_of, r) - v2sym * sp.diff(M_of, r) / 2),
                              v2sym)[0])
print(f"  (b) variable-mass Lagrangian: v_c^2 = {sp.simplify(v2_lag)}")
# they must agree to leading nonrelativistic order; the difference is the post-Newtonian r T'/(4T) term
diff_ratio = sp.simplify(sp.together(1 / v2_lag - 1 / v2_exact) * r * sp.diff(T, r) / 2)
print(f"  their 1/v^2 difference x (r T'/2) = {sp.simplify(diff_ratio)}   (a pure PN term ~ v^2/c^2)")
# numeric: MW-like, deep-MOND A, check agreement at the 1e-6 level and NOT better (it is a real PN term)
Tn = sp.Lambda(r, 1 + 2 * (-(2.73e10 / C_LIGHT ** 2) * sp.log(r)))       # flat-curve potential, c=1 units
Sn = sp.Lambda(r, 0.4 * (r / (10 * KPC)) ** sp.Rational(1, 2))            # a deep-MOND-like A(r)
v2e = float(v2_exact.subs({T: Tn(r), S: Sn(r)}).doit().subs(r, 10 * KPC))
v2l = float(v2_lag.subs({T: Tn(r), S: Sn(r), m: 1}).doit().subs(r, 10 * KPC))
rel = abs(v2l / v2e - 1)
check(rel < 3e-6 and rel > 1e-9,
      f"the two derivations agree to {rel:.2e} at r=10 kpc with an O(1) spatial factor -- nonzero "
      f"(it is the PN r T'/(4T) ~ v^2/2c^2 term), so the check is not vacuous")
print("  => THE COMPLETION IS LITERALLY MODIFIED INERTIA: the nonrelativistic Lagrangian is")
print("     L = (1/2) M(x) v^2 - U(x) with a POSITION-DEPENDENT INERTIAL MASS M = m S/sqrt(T).")
print("     Note the price already visible here: the extra force (1/2)v^2 grad M is +(1/2)v^2 M' for")
print("     TANGENTIAL motion and -(1/2)v^2 M' for RADIAL motion, so inertia is anisotropic in the")
print("     velocity direction whenever grad M != 0 -- the orbit-vs-radial asymmetry of no-go (iii).")

# the observable, with T = D(1+2Phi), S = A (isotropic-gauge g = diag(-(1+2Phi),(1-2Phi)delta))
Phi_f, D_f, A_f = sp.Function('Phi')(r), sp.Function('D')(r), sp.Function('A')(r)
den = 2 * A_f + r * sp.diff(A_f, r)
g_obs_exact = sp.simplify(sp.diff(D_f * (1 + 2 * Phi_f), r) / den)
g_obs_wf = (sp.diff(D_f, r) + 2 * D_f * sp.diff(Phi_f, r)) / den
print(f"\n  observable g_obs = v_c^2/r = (D' + 2 D Phi') / (2A + r A')   [weak field]")
lhs = sp.simplify(g_obs_exact - g_obs_wf)
check(sp.simplify(lhs - 2 * Phi_f * sp.diff(D_f, r) / den) == 0,
      "g_obs = (D' + 2 D Phi')/(2A + r A'), the dropped term being exactly 2 Phi D'/(2A+rA'), a "
      "RELATIVE 2Phi ~ 1e-6 weak-field correction (so the truncation is controlled, not assumed)")

# ==================================================================
banner("S4.  ** THE CONE IDENTITY -- tested EARLY, because this is where disformal models die **")
# ==================================================================
Phi_s = sp.symbols('Phi', real=True)
# photon rides g: g = diag(-(1+2Phi), (1-2Phi) delta)   -> coordinate speed^2 = (1+2Phi)/(1-2Phi)
c_ph2 = (1 + 2 * Phi_s) / (1 - 2 * Phi_s)
# matter rides g_eff = A g + C u u : T = D(1+2Phi), S = A(1-2Phi)
c_m2 = (D_s * (1 + 2 * Phi_s)) / (A_s * (1 - 2 * Phi_s))
ratio = sp.simplify(c_m2 / c_ph2)
print(f"  (matter cone / photon cone)^2 = {ratio}   -- EXACTLY D/A, for ANY Phi, in any gauge.")
check(sp.simplify(ratio - D_s / A_s) == 0 and sp.simplify(sp.diff(ratio, Phi_s)) == 0,
      "cone ratio = D/A = 1 - C/A = 1 + B X / A, independent of Phi and of the gauge")
check(sp.simplify(ratio.subs(B_s, 0) - 1) == 0 and sp.simplify(ratio - 1) != 0,
      "PURE CONFORMAL (B = 0 => D = A): cone ratio = 1 EXACTLY -- the conformal factor is cone-blind; "
      "and for B != 0 the ratio is NOT 1, so the test discriminates")
print("  => THE ENTIRE CONE BILL IS CHARGED TO B (the disformal piece). This is the load-bearing fact.")

# invariant restatement: is a g_eff-null covector g-timelike or g-spacelike?
k0, kx = sp.symbols('k0 kx', positive=True)
kcov = sp.Matrix([k0, kx, 0, 0])
sol = sp.solve(sp.Eq((sp.Matrix(g_eff_inv) * kcov).dot(kcov), 0), k0)
k0v = [s for s in sol if sp.simplify(s).could_extract_minus_sign() is False][0]
gnorm = sp.simplify((sp.Matrix(g.inv()) * kcov).dot(kcov).subs(k0, k0v))
print(f"  g_eff-null covector: k0 = {sp.simplify(k0v)};  its g-norm = {sp.simplify(gnorm)}")
check(sp.simplify(gnorm - kx ** 2 * (1 - (A_s - C_s) / A_s)) == 0,
      "g-norm of the g_eff-null covector = kx^2 * C/A: SIGN(C) decides the cone ORDERING "
      "(C>0 matter INSIDE the photon cone, C<0 matter OUTSIDE) -- an invariant statement")

# the corpus's OWN coupling for contrast: a scalar dressing of the rest mass, matter minimal on g
vv, Kf = sp.symbols('v K', positive=True)
E_dress = m * Kf / sp.sqrt(1 - vv ** 2)                    # dressing multiplies m; cone from g only
E_disf = m / sp.sqrt(1 - vv ** 2 * A_s / D_s)              # disformal: cone from D/A
eps_v = sp.symbols('eps_v', positive=True)      # v = 1 - eps_v, eps_v -> 0+  (unambiguous direction)
check(sp.limit(E_dress.subs(vv, 1 - eps_v), eps_v, 0, '+') == sp.oo,
      "the corpus's scalar dressing S = -INT m K(|a|^2/a0^2) dtau: E -> infinity as v -> c for ANY K>0, "
      "so its limiting speed is c EXACTLY -- zero cone shift (this is why MATTER_COUPLING.md sec1 was "
      "right to refuse a disformal matter metric)")
vlim = sp.solve(sp.Eq(1 - vv ** 2 * A_s / D_s, 0), vv)[1]
check(sp.simplify(vlim - sp.sqrt(D_s / A_s)) == 0,
      f"the disformal coupling instead has limiting speed sqrt(D/A) = {sp.simplify(vlim)} != 1 -- the "
      "cone shift is unavoidable once B != 0")

# ==================================================================
banner("S5.  ** NO-GO 1: THE LITERAL (phi,X) CLASS CANNOT DO IT **  (three independent ways)")
# ==================================================================
print("  (a) SHIFT SYMMETRY + THE CORPUS'S OWN GHOST-CONDENSATE ATTRACTOR.")
print("      Shift symmetry phi -> phi + const (which forbids V(phi)) equally forbids explicit phi in")
print("      A and B: A = A(X), B = B(X).  The corpus's established attractor is a^3 P'(X) phidot =")
print("      const -> P'(X) -> 0 -> X -> X_0, the EXTREMUM of P, a CONSTANT.  Therefore on the")
print("      attractor A and B are CONSTANTS and g_eff = A_0 g + C_0 u u with constant coefficients.")
Phi_r = sp.Function('Phi')(r)
A_c, D_c = sp.symbols('A_c D_c', positive=True)
g_obs_const = sp.simplify(g_obs_wf.subs({A_f: A_c, D_f: D_c}).doit())
boost_const = sp.simplify(g_obs_const / sp.diff(Phi_r, r))
print(f"      -> g_obs/g_bar = {boost_const} : a CONSTANT, with NO y-dependence whatsoever.")
check(sp.simplify(sp.diff(boost_const, r)) == 0,
      "constant A,D give a strictly constant boost D/A -- no acceleration dependence, hence NO MOND")
# a constant boost cannot fit the RAR: the required boost differs across the sampled range
y_lo, y_hi = 1e-2, 1e2
need = (float(nu(y_lo)), float(nu(y_hi)))
dex_spread = np.log10(need[0] / need[1])
check(dex_spread > 0.9,
      f"the boost the RAR requires runs from nu({y_hi:g})={need[1]:.4f} to nu({y_lo:g})={need[0]:.4f}, a "
      f"{dex_spread:.2f} dex spread, vs {RAR_SCATTER_TOTAL} dex observed scatter -- a single constant is "
      f"excluded by {dex_spread/RAR_SCATTER_TOTAL:.0f}x the scatter")

print("\n  (b) OFF THE ATTRACTOR THE ONLY AVAILABLE SCALAR IS Phi, AND nu IS A FUNCTION OF |grad Phi|.")
phid = sp.symbols('phidot', positive=True)
X_wf = sp.simplify(sp.series(-phid ** 2 / (1 + 2 * Phi_s), Phi_s, 0, 2).removeO())
print(f"      static weak field, homogeneous condensate phi = phidot t:  X = g^00 phidot^2 = {X_wf}")
check(sp.simplify(sp.diff(X_wf, Phi_s) - 2 * phid ** 2) == 0,
      "X = -phidot^2 (1 - 2 Phi) + O(Phi^2): X is a function of the POTENTIAL Phi, never of grad Phi")
print("      so any A(X), B(X) is a function of Phi, and the boost is F(Phi).  Two-system test at")
print("      EQUAL Phi (so equal F) but different g_bar -- point masses, Phi = -GM/r, g_bar = GM/r^2:")
pairs = [("MW-like", 6e10 * MSUN), ("dwarf", 1e9 * MSUN)]
Phi_target = -(1.0e5) ** 2                                  # m^2/s^2, a common potential depth
rows = []
for lab, Mb in pairs:
    rr = G_SI * Mb / abs(Phi_target)
    gb = G_SI * Mb / rr ** 2
    rows.append((lab, rr / KPC, gb, gb / a0c, float(nu(gb / a0c))))
    print(f"        {lab:<9s} M={Mb/MSUN:8.2e} Msun  r={rr/KPC:8.3f} kpc  g_bar={gb:.3e}  "
          f"y={gb/a0c:8.3e}  nu={float(nu(gb/a0c)):.4f}")
dex_pair = abs(np.log10(rows[0][4] / rows[1][4]))
check(dex_pair > RAR_SCATTER_TOTAL,
      f"at IDENTICAL Phi the two systems need boosts differing by {dex_pair:.3f} dex "
      f"({rows[0][4]:.3f} vs {rows[1][4]:.3f}) -- a function of Phi alone CANNOT supply both; the "
      f"literal class has the wrong FUNCTIONAL ARGUMENT")

print("\n  (c) AND THE SIZE REQUIRED IS THE CORPUS'S OWN (v/c)^2 WALL, NOT AN ESCAPE FROM IT.")
for lab, a0v in A0.items():
    pass
Phi_MW = (2.2e5) ** 2                                        # |Phi| ~ v_c^2 for the Milky Way
frac = 2 * Phi_MW / C_LIGHT ** 2                             # dX/X available in the weak field
slope_needed = 1.0 / frac
print(f"      the ENTIRE variation of X available in a galaxy is dX/X = 2|Phi|/c^2 = {frac:.3e}.")
print(f"      An O(1) change of inertia therefore needs |dlnA/dlnX| ~ 1/{frac:.1e} = {slope_needed:.2e}.")
check(PREFACTOR_WINDOW[0] <= slope_needed <= PREFACTOR_WINDOW[1],
      f"the required dimensionless slope {slope_needed:.2e} lands INSIDE the corpus's own no-go (ii) "
      f"window {PREFACTOR_WINDOW[0]:.1e}-{PREFACTOR_WINDOW[1]:.1e} -- the disformal escape REPRODUCES "
      f"the (v/c)^2 / Frenet-torsion suppression rather than dodging it")

# ==================================================================
banner("S6.  ** NO-GO 2: THE EXTENDED CLASS (A,D of the acceleration invariant) -- forced, then broken")
# ==================================================================
# |a| for the condensate congruence in a static weak field
t_, x_ = sp.symbols('t x', real=True)
Phi_x = sp.Function('Phi')(x_)
# phi = phidot t (homogeneous, the corpus's attractor);  -X = phidot^2/(1+2Phi)
lnsq = sp.log(phid) - sp.log(1 + 2 * Phi_x) / 2                  # = ln sqrt(-X)
a_x = sp.simplify(-sp.diff(lnsq, x_))
print(f"  u_mu = d_mu phi/sqrt(-X);  ln sqrt(-X) = {lnsq}   (phi = phidot t on the attractor)")
print(f"  a_mu = -(delta+uu).grad ln sqrt(-X)  ->  a_x = {a_x}  =  Phi' / (1+2Phi)")
check(sp.simplify(a_x * (1 + 2 * Phi_x) - sp.diff(Phi_x, x_)) == 0,
      "the ghost condensate's congruence acceleration IS the baryonic field: |a| = |grad Phi| = g_bar "
      "up to a relative 2Phi ~ 1e-6 (so the only new invariant available is y = |a|/a0 -- and it costs "
      "SECOND derivatives of phi)")

print("\n  With A = A(y), D = D(y) and a local power-law profile g_bar ~ r^-p (p = -dlny/dlnr):")
p_s, LA, LD, gb_s, rr_s = sp.symbols('p L_A L_D g_bar r_', positive=True)
# D' = -p D L_D / r ,  A' = -p A L_A / r
Dp = -p_s * D_s * LD / rr_s
Ap = -p_s * A_s * LA / rr_s
boost = sp.simplify((Dp + 2 * D_s * gb_s) / ((2 * A_s + rr_s * Ap) * gb_s))
print(f"     g_obs/g_bar = {sp.simplify(boost)}")
check(sp.simplify(boost - (D_s * (2 * gb_s - p_s * LD / rr_s)) / (A_s * gb_s * (2 - p_s * LA))) == 0,
      "boost = (D/A) (2 g_bar - p L_D/r) / (g_bar (2 - p L_A)): it carries an EXPLICIT 1/r and an "
      "EXPLICIT p")
print("     At FIXED y, 1/r is still free (two systems of different SIZE share a y and a p), so")
print("     universality forces p L_D = 0 for all p  ->  L_D = 0.  Then universality over p forces")
print("     L_A = 0.  Both disformal functions are then CONSTANT -> boost constant -> NO MOND.")
check(sp.simplify(boost.subs({LD: 0, LA: 0}) - D_s / A_s) == 0,
      "*** THEOREM: a LOCAL disformal dressing (any A,D built from the local invariants Phi and |a|) "
      "cannot reproduce nu(y) universally -- L_A = L_D = 0 is forced, i.e. no MOND ***")

print("\n  Price the near-miss anyway: FIT one geometry (p = 2, a point mass; D = 1) and see what the")
print("  SAME A(y) then predicts elsewhere.  Requirement:  1/A = nu(y) [1 - (p/2) dlnA/dlny].")


def ode_rhs(s, u, p=2.0, alpha=1.0):
    """u = ln A, s = ln y.  From 1/A = nu (1 - (p/2) u_s):  u_s = (2/p)(1 - e^-u / nu)."""
    yv = np.exp(s)
    return [(2.0 / p) * (1.0 - np.exp(-u[0]) / nu(yv, alpha))]


s_hi, s_lo = np.log(1e8), np.log(1e-10)
u_hi = -1.0 / (4.0 * np.exp(s_hi))               # asymptotic A = 1 - 1/(4y)
sol = solve_ivp(ode_rhs, (s_hi, s_lo), [u_hi], rtol=1e-12, atol=1e-16, dense_output=True)
check(sol.success, "the forced ODE for A(y) integrates from y=1e8 down to y=1e-10")


def A_of_y(yv):
    return np.exp(sol.sol(np.log(yv))[0])


def LA_of_y(yv):
    s = np.log(yv)
    return ode_rhs(s, [sol.sol(s)[0]])[0]


print(f"\n  {'y':>10s} {'A(y)':>12s} {'1/A = cone^2':>13s} {'dlnA/dlny':>11s} {'nu':>9s} "
      f"{'2/nu (deep-MOND)':>17s}")
for yv in (1e6, 1e2, 1e0, 1e-1, 1e-2, 1e-3):
    print(f"  {yv:10.1e} {A_of_y(yv):12.5e} {1/A_of_y(yv):13.5e} {LA_of_y(yv):11.4f} "
          f"{float(nu(yv)):9.4f} {2/float(nu(yv)):17.5e}")
# asymptote checks (both can fail).  The asymptote is approached as a POWER of y, so the shift
# between two decades is shown rather than a single coarse evaluation (grid-refinement hazard).
r_deep4 = A_of_y(1e-4) * float(nu(1e-4)) / 2.0
r_deep = A_of_y(1e-9) * float(nu(1e-9)) / 2.0
r_newt = A_of_y(1e6) / (1 - 1 / (4 * 1e6))
print(f"  convergence of the deep-MOND asymptote A nu/2 -> 1:  {r_deep4:.6f} at y=1e-4  ->  "
      f"{r_deep:.6f} at y=1e-9  (residual falls as ~sqrt(y))")
check(abs(r_deep - 1) < 1e-3,
      f"deep-MOND asymptote: A -> 2/nu (A nu/2 = {r_deep:.6f} at y=1e-9), i.e. dlnA/dlny -> 1/2 "
      f"(got {LA_of_y(1e-9):.6f}) -- the gradient term supplies HALF the boost")
check(abs(r_newt - 1) < 1e-4,
      f"Newtonian asymptote: A -> 1 - 1/(4y) (ratio {r_newt:.8f}), so the cone closes as 1 + 1/(4y)")
# and the NAIVE local guess A = 1/nu must FAIL the ODE (a check that can fail)
resid_naive = 1.0 * float(nu(1e-2)) * (1 - 0.5 * 0.5) - float(nu(1e-2))
check(abs(A_of_y(1e-2) - 1 / float(nu(1e-2))) / (1 / float(nu(1e-2))) > 0.5,
      f"the naive local guess A = 1/nu is WRONG by "
      f"{A_of_y(1e-2)/(1/float(nu(1e-2))):.2f}x at y=1e-2 -- the spatial-gradient force is O(1), not a "
      f"correction")

print("\n  NOW THE UNIVERSALITY VIOLATION: the SAME A(y) at other local log-slopes p")
print(f"  {'y':>9s} " + " ".join(f"{'p=%g'%p:>12s}" for p in (2, 1, 0, -1)) + "     [dex offset from nu]")
worst = 0.0
for yv in (1e-1, 1e-2, 1e-3):
    line = f"  {yv:9.1e} "
    for p in (2, 1, 0, -1):
        b = (1 / A_of_y(yv)) / (1 - p * LA_of_y(yv) / 2)
        d = np.log10(b / float(nu(yv)))
        worst = max(worst, abs(d))
        line += f" {d:+12.4f}"
    print(line)
check(worst > RAR_SCATTER_INTRINSIC * 3,
      f"the geometry-dependent offset reaches {worst:.3f} dex, vs the marginalised intrinsic RAR "
      f"scatter {RAR_SCATTER_INTRINSIC} dex ({worst/RAR_SCATTER_INTRINSIC:.1f}x) and the total "
      f"{RAR_SCATTER_TOTAL} dex ({worst/RAR_SCATTER_TOTAL:.1f}x) -- a p-CORRELATED systematic, not "
      f"scatter.  (Honest caveat: converting this to a sigma needs a full SPARC refit of the "
      f"p-dependent law; it is quoted as a tension, not a kill.)")

print("\n  AND THE CONE, IN THE SAME BREATH: cone^2 = D/A = 1/A, and the measured boost is")
print("  (1/A)/(1 - (p/2) dlnA/dlny), so here cone^2 = boost x (1 - (p/2) dlnA/dlny) -- in deep MOND at")
print("  p=2 that is exactly nu/2.  Precisely: the cone dilation is NOT identical to the boost, it is")
print("  the boost times the O(1) geometry factor; both are O(1) and both diverge as y -> 0.")
print(f"  {'y':>9s} {'boost':>9s} {'c_eff/c':>9s} {'|c_eff/c-1|':>12s}  {'gamma_threshold (super-luminal above)':>38s}")
for yv in (1e0, 3e-1, 1e-1, 1e-2, 1e-3):
    cone = np.sqrt(1 / A_of_y(yv))
    gth = 1 / np.sqrt(1 - 1 / max(1 / A_of_y(yv), 1 + 1e-30)) if 1 / A_of_y(yv) > 1 else np.inf
    print(f"  {yv:9.1e} {1/A_of_y(yv):9.4f} {cone:9.4f} {abs(cone-1):12.4f}  {gth:38.3f}")
cone_max = max(np.sqrt(1 / A_of_y(yv)) for yv in (1e-1, 1e-2, 1e-3))
check(cone_max - 1 > 0.5,
      f"in the deep-MOND regime matter's limiting speed exceeds the photon's by "
      f"{100*(cone_max-1):.0f}% -- O(1) SUPERLUMINALITY, unbounded as y -> 0 (cone^2 = boost x the "
      f"O(1) geometry factor -> infinity).  Any mildly relativistic charged particle above the printed "
      f"gamma threshold then radiates by vacuum Cherenkov, and cosmic rays are observed throughout "
      f"galactic outskirts")

# ==================================================================
banner("S7.  ** THE ONLY BRANCH THAT REPRODUCES THE LAW: NONLOCAL D = 1 + 2(Phi_M - Phi) **")
# ==================================================================
print("  Set A = 1 and let the acceleration dependence live in D.  The requirement D'/2 = (nu-1) g_bar")
print("  integrates to D = 1 + 2(Phi_M - Phi), with Phi_M the AQUAL potential (Bekenstein-Milgrom 1984)")
print("  -- i.e. the corpus's OWN nonlocal K(Box_u) (mi_disformal_locality.py's resolution).  This is")
print("  the matter-sector twin of the committed photon construction B = 4(Phi - Phi_M), and")
print("  C_matter = B_photon/2 exactly (the photon lensing potential is (Phi~+Psi~)/2, matter's is 00).")
dPhi = sp.symbols('DeltaPhi', positive=True)                 # DeltaPhi = Phi - Phi_M > 0
# photon: g~_00 = -(1+2Phi)(1-B) -> Phi~ = Phi - B/2, Psi~ = Phi -> lensing potential (Phi~+Psi~)/2
B_photon = sp.solve(sp.Eq(Phi_s - sp.Symbol('Bp') / 4, Phi_s - dPhi), sp.Symbol('Bp'))[0]
# matter: only the 00 sector acts -> D = 1 - C with C fixed by grad D/2 = g_obs - g_bar
C_matter = sp.solve(sp.Eq((1 - sp.Symbol('Cm') - 1) / 2, -dPhi), sp.Symbol('Cm'))[0]
check(sp.simplify(B_photon / C_matter - 2) == 0,
      f"C_matter = {C_matter} and B_photon = {B_photon}, so C_matter = B_photon/2 EXACTLY: the matter "
      f"branch inherits the committed grad B = 4(nu-1) g_bar relation halved -- grad C = 2(nu-1) g_bar")


def dW_dr(rr, Mb, a0v, alpha=1.0):
    """d(Phi - Phi_M)/dr = -(nu-1) g_bar  ->  the cone mismatch accumulates as INT (nu-1) g_bar dr."""
    gb = G_SI * Mb / rr ** 2
    return float(nu_minus_1(gb / a0v, alpha)) * gb


def cone_mismatch(Mb, r1, r2, a0v, alpha=1.0):
    v, _ = quad(lambda rr: dW_dr(rr, Mb, a0v, alpha), r1, r2, limit=400)
    return v / C_LIGHT ** 2                      # delta in SPEED (cone^2 = 1 - 2W -> delta = -W)


print("\n  WHAT IS TABULATED, and why it is the CONSERVATIVE choice: the photon-decay condition is")
print("  LOCAL in W = Phi - Phi_M, but W itself is only defined up to an additive constant (the MOND")
print("  potential is log-divergent, so the corpus's own tail_freedom script had to switch to dB/dr")
print("  and VARIATIONS).  The constant is physical -- a uniform matter-vs-photon speed ratio is")
print("  observable -- but it is cutoff-dependent, so it is DROPPED here.  What is quoted is the")
print("  cutoff-independent VARIATION across a path, which forces |W| at one of the two ends to be at")
print("  least half of it.  Quoting the full offset instead would strengthen every number below.")
systems = [("Milky Way  8->60 kpc", 6e10 * MSUN, 8 * KPC, 60 * KPC),
           ("MW local   8->10 kpc", 6e10 * MSUN, 8 * KPC, 10 * KPC),
           ("dwarf    0.5->5 kpc", 1e8 * MSUN, 0.5 * KPC, 5 * KPC),
           ("Sun     1 AU->10 AU", GM_SUN / G_SI, AU, 10 * AU)]
print(f"\n  {'system':<22s} {'footing':<12s} {'|Phi_M-Phi|/c^2 = |delta_cone|':>31s}")
mismatch = {}
for lab, Mb, r1, r2 in systems:
    for fl, a0v in (("canonical", a0c), ("ALT", a0a)):
        d = cone_mismatch(Mb, r1, r2, a0v)
        mismatch[(lab, fl)] = d
        print(f"  {lab:<22s} {fl:<12s} {d:>31.4e}")
check(mismatch[("Milky Way  8->60 kpc", "canonical")] > 1e-7
      and mismatch[("dwarf    0.5->5 kpc", "canonical")] > 1e-9,
      "the cone mismatch is 1e-8..1e-6 -- forced, because it IS the extra binding per unit mass "
      "(~v_c^2/c^2) that a flat rotation curve requires; it cannot be tuned down without losing MOND")
# the sign is FORCED
check(dW_dr(10 * KPC, 6e10 * MSUN, a0c) > 0,
      "sign FORCED: g_obs > g_bar => Phi_M < Phi => D = 1 + 2(Phi_M-Phi) < 1 => matter SUBLUMINAL and "
      "PHOTONS SUPERLUMINAL relative to matter -- which selects PHOTON DECAY gamma -> e+ e- as the "
      "binding test (not vacuum Cherenkov)")

print("\n  PHOTON DECAY BOUND.  With photon speed exceeding the electron limiting speed by delta, the")
print("  photon acquires an effective invariant mass^2 = 2 delta E^2 and decays once 2 delta E^2 >")
print("  (2 m_e)^2, i.e. delta > 2 m_e^2/E^2.  Observed photons therefore bound delta:")
print(f"  {'observed photon energy':<26s} {'delta_max = 2 m_e^2/E^2':>24s} {'MW violation factor':>21s}")
viol = {}
for lab, E_eV in (("1 TeV (ubiquitous)", 1e12), ("100 TeV (Crab, HEGRA)", 1e14), ("1 PeV (LHAASO)", 1e15)):
    dmax = 2 * (M_E_EV / E_eV) ** 2
    v = mismatch[("Milky Way  8->60 kpc", "canonical")] / dmax
    viol[lab] = v
    print(f"  {lab:<26s} {dmax:>24.3e} {v:>21.2e}")
check(min(viol.values()) > 1e5,
      f"the nonlocal disformal branch violates the photon-decay bound by {min(viol.values()):.1e} "
      f"(1 TeV, the most conservative) to {max(viol.values()):.1e} (1 PeV) -- CLOSED empirically")
print("  Even the most conservative version -- the 2-kpc local variation against the 1 TeV bound --")
loc = mismatch[("MW local   8->10 kpc", "canonical")] / (2 * (M_E_EV / 1e12) ** 2)
check(loc > 1e4, f"gives {loc:.2e}x over.  And the SOLAR-SYSTEM piece alone is "
                 f"{mismatch[('Sun     1 AU->10 AU','canonical')]:.2e}, i.e. locally near the 100 TeV "
                 f"bound {2*(M_E_EV/1e14)**2:.1e} -- the kill is galactic, not local")

# ==================================================================
banner("S8.  THE TRILEMMA: who rides g_eff?  All three assignments are closed")
# ==================================================================
d_mw = mismatch[("Milky Way  8->60 kpc", "canonical")]
D_MPC = 40 * 3.0856775814913673e22
t_travel = D_MPC / C_LIGHT
dt_gw = d_mw * t_travel
print(f"  (a) MATTER on g_eff; photons+gravitons on g.")
print(f"      GW170817 is EVADED EXACTLY (photon and graviton share g, Delta t = 0) -- a genuine")
print(f"      improvement on the committed photon-disformal route, which fails it by ~1e15.")
print(f"      But matter-vs-photon cones differ by {d_mw:.2e} -> photon decay: "
      f"{min(viol.values()):.1e} to {max(viol.values()):.1e} over.  CLOSED.")
print(f"  (b) MATTER + PHOTONS on g_eff; gravitons on g.  Lensing is bought, but now the PHOTON")
print(f"      cone moves: Delta c/c = {d_mw:.2e} -> Delta t over 40 Mpc = {dt_gw:.3e} s vs the 1.7 s")
print(f"      GW170817 window = {dt_gw/1.7:.2e}x over, and {d_mw/1e-15:.1e}x over |Delta c|/c < 1e-15.")
print(f"      This REPRODUCES the committed mi_disformal_gw170817_TENSION.py verdict.  CLOSED.")
print(f"  (c) EVERYTHING on g_eff.  Then g_eff IS the physical metric, the construction is a field")
print(f"      redefinition, and the modification has moved into the GRAVITY sector: it is modified")
print(f"      GRAVITY, not modified inertia -- contradicting the framework's defining claim -- and the")
print(f"      graviton still rides g, so (b)'s GW170817 bill is paid again.  Plus it inherits the")
print(f"      AeST/AQUAL Cassini-Q2 tension the corpus has already priced at 3-15 sigma.  CLOSED.")
check(dt_gw / 1.7 > 1e6 and min(viol.values()) > 1e5,
      f"every assignment of g_eff is excluded: (a) {min(viol.values()):.1e}x by photon decay, "
      f"(b) {dt_gw/1.7:.1e}x by GW170817, (c) by construction (it is MG) -- and the required cone "
      f"offset {d_mw:.1e} is ~1e8x the tightest allowed")

# ==================================================================
banner("S9.  ** THE ONE EXACT SURVIVOR: THE CONFORMAL PIECE (B = 0) -- and what it costs **")
# ==================================================================
print("  B = 0 => D = A => cone ratio 1 EXACTLY (S4), to all orders, for any A.  And the force works:")
Aconf = sp.Function('A')(r)
g_obs_conf = sp.simplify(g_obs_wf.subs({D_f: Aconf, A_f: Aconf}).doit())
print(f"     g_obs = {sp.simplify(g_obs_conf)}  -> = Phi' + (1/2) (ln A)' , i.e. -grad[Phi + (1/2) ln A]")
check(sp.simplify(sp.expand(g_obs_conf * (2 * Aconf + r * sp.diff(Aconf, r))
                            - (sp.diff(Aconf, r) + 2 * Aconf * sp.diff(Phi_r, r)))) == 0,
      "conformal branch: g_obs (2A + rA') = A' + 2A Phi', so with A - 1 = O(1e-6) and r A' << A the "
      "force is exactly -grad[Phi + (1/2) ln A]; A = exp(2(Phi_M - Phi)) reproduces g_obs = nu g_bar "
      "with NO large factor and NO cone shift")
# but photons are conformally blind in 4D -- and only in 4D
Dd = sp.symbols('Dd', positive=True)
Om = sp.symbols('Omega', positive=True)
maxwell_weight = Om ** Dd * Om ** (-2) * Om ** (-2)        # sqrt(-g_eff) * g_eff^{..} * g_eff^{..}
check(sp.simplify(maxwell_weight.subs(Dd, 4) - 1) == 0 and sp.simplify(maxwell_weight.subs(Dd, 5) - 1) != 0,
      f"Maxwell weight sqrt(-g_eff) g_eff^{{mu al}} g_eff^{{nu be}} scales as Omega^(D-4) under "
      f"g -> Omega^2 g: A-independent at D=4 ({maxwell_weight.subs(Dd,4)}) and NOT at D=5 "
      f"({maxwell_weight.subs(Dd,5)}) -- photons are conformally BLIND, so the conformal branch buys "
      f"ZERO lensing enhancement")
print("  => the classic TeVeS split, re-derived inside this framework: the piece that is cone-safe")
print("     (conformal) cannot lens, and the piece that lenses (disformal B) cannot pass the cone")
print("     tests.  Bekenstein 2004 needed the disformal term for exactly this reason.")
print("  => and note what the conformal branch IS: matter feeling -grad[Phi + (1/2)lnA] is a FIFTH")
print("     FORCE on a single metric = AQUAL / Bekenstein-Milgrom modified GRAVITY.  It does not")
print("     complete MODIFIED INERTIA, and it inherits AQUAL's Cassini-Q2 bill.")

# ==================================================================
banner("S10.  GHOSTS: signature, invertibility, the kinetic matrix, and the Ostrogradsky runaway")
# ==================================================================
print("  (i) SIGNATURE / no tachyonic direction:  A > 0 and D = A + B X > 0 (S2).  These are")
print("      CONSTRAINTS, not identities -- S11 shows alpha=1 violates D > 0 inside Saturn's orbit.")
print("  (ii) DOF PRESERVATION: A - X A_X - X^2 B_X != 0 (S2).  Also a constraint.")
print("  (iii) THE 2x2 KINETIC MATRIX.  Homogeneous modes of (phi, chi) with chi a matter scalar on")
print("        g_eff:  L = P(X) + (1/2) Omega(X) chidot^2 - ... , Omega = sqrt(A^3/D), X = -phidot^2.")
pd0, cd0 = sp.symbols('phidot0 chidot0', positive=True)
pp, qq = sp.symbols('p q', real=True)
Pp, Ppp = sp.symbols('Pprime Pprime2', real=True)
Om0, Omp, Ompp = sp.symbols('Omega0 Omegaprime Omegaprime2', real=True)
Xp0, Xpp = -2 * pd0, sp.Integer(-2)                 # X = -(phidot0+p)^2 -> dX/dp, d2X/dp2 at p=0
Kpp = (Ppp * Xp0 ** 2 + Pp * Xpp + (cd0 ** 2 / 2) * (Ompp * Xp0 ** 2 + Omp * Xpp)) / 2
Kpq = (cd0 * Omp * Xp0) / 2
Kqq = Om0 / 2
Kmat = sp.Matrix([[Kpp, Kpq], [Kpq, Kqq]])
print(f"        K_phiphi = {sp.simplify(Kpp)}")
print(f"        K_phichi = {sp.simplify(Kpq)}")
print(f"        K_chichi = {sp.simplify(Kqq)}")
# independent verification of the chain rule against an explicit sympy Hessian
sig = sp.symbols('sigma', real=True)
Ltest = (-(pd0 + pp) ** 2) ** 2 + sp.exp(sig * (-(pd0 + pp) ** 2)) * (cd0 + qq) ** 2 / 2
Htest = (sp.hessian(Ltest, (pp, qq)) / 2).subs({pp: 0, qq: 0})
X0v = -pd0 ** 2
Kref = Kmat.subs({Pp: 2 * X0v, Ppp: 2, Om0: sp.exp(sig * X0v), Omp: sig * sp.exp(sig * X0v),
                  Ompp: sig ** 2 * sp.exp(sig * X0v)})
check(sp.simplify(Htest - Kref) == sp.zeros(2, 2),
      "the analytic kinetic matrix is verified against an explicit sympy Hessian on the test pair "
      "P = X^2, Omega = exp(sigma X) (so the chain rule is not assumed)")
# on the ghost-condensate attractor P' = 0
detK = sp.simplify(sp.expand(Kmat.subs(Pp, 0).det()))
print(f"        on the attractor P' = 0:  det K = {detK}")
check(sp.simplify(detK.coeff(cd0, 2)) != 0,
      "the kinetic matrix is NOT automatically positive: ghost-freedom needs Omega > 0, "
      "-2 X P'' > 0 (i.e. P'' > 0, the standard ghost-condensate condition) AND det K > 0, and det K "
      "carries an explicit chidot0^2 term from the phi-chi mixing that can drive it negative")
# numeric: the mixing term scales as (dlnA/dlnX)^2, so the 1e6 slope of S5(c) lowers the ghost
# threshold in matter kinetic density by ~1e12
f_detK = sp.lambdify((pd0, cd0, Ppp, Om0, Omp, Ompp), detK, 'numpy')


def crit_cd0(slope, Ppp_v=1.0, pd0_v=1.0):
    """critical matter kinetic amplitude at which det K crosses zero, for Omega=1 and
    dOmega/dX = slope*Omega/|X| (i.e. |dlnOmega/dlnX| = slope)."""
    Om0_v, X0_v = 1.0, -pd0_v ** 2
    Omp_v = slope * Om0_v / X0_v
    Ompp_v = slope * (slope - 1) * Om0_v / X0_v ** 2
    lo, hi = 1e-12, 1e12
    if f_detK(pd0_v, lo, Ppp_v, Om0_v, Omp_v, Ompp_v) <= 0:
        return np.nan
    for _ in range(300):
        mid = np.sqrt(lo * hi)
        if f_detK(pd0_v, mid, Ppp_v, Om0_v, Omp_v, Ompp_v) > 0:
            lo = mid
        else:
            hi = mid
    return np.sqrt(lo * hi)


c1, c6 = crit_cd0(1.0), crit_cd0(slope_needed)
print(f"        critical chidot0 (ghost appears above it): slope 1 -> {c1:.4e};  "
      f"slope {slope_needed:.2e} -> {c6:.4e}")
check(np.isfinite(c1) and np.isfinite(c6) and 0.2 < (c6 / c1) * slope_needed < 5,
      f"the ghost threshold scales as 1/slope ({c6/c1:.3e} vs 1/{slope_needed:.2e} = "
      f"{1/slope_needed:.3e}), so the ~1e6 slope the literal class needs lowers the ghost-free "
      f"window in matter kinetic DENSITY by ~{slope_needed**2:.1e}: ghost-freedom holds only under a "
      f"constraint, and the constraint is severely tightened by the very slope MOND requires")

print("\n  (iv) THE EXTENDED CLASS TRIPS THE CORPUS'S OWN NAMED HINGE.  mi_disformal_ostrogradsky.py")
print("       proves the photon-disformal coupling ghost-free *given a PASSIVE frame*, and states the")
print("       hinge explicitly: 'Were u a *dynamical* khronon T, then a ~ d^2 T ... an Ostrogradsky")
print("       concern'.  Here phi IS dynamical (it is the ghost condensate), and S6 needs A to depend")
print("       on |a|^2 ~ (d^2 phi)^2.  That is exactly the hinge.  Demonstration on the minimal toy:")
eps_s, om_s, lam = sp.symbols('epsilon omega lambda', positive=True)
q = sp.Function('q')
Ltoy = sp.diff(q(t_), t_) ** 2 / 2 - om_s ** 2 * q(t_) ** 2 / 2 + eps_s * sp.diff(q(t_), t_, 2) ** 2 / 2
EL = sp.simplify(sp.diff(Ltoy, q(t_)) - sp.diff(sp.diff(Ltoy, sp.diff(q(t_), t_)), t_)
                 + sp.diff(sp.diff(Ltoy, sp.diff(q(t_), t_, 2)), t_, 2))
print(f"       L = q'^2/2 - w^2 q^2/2 + eps q''^2/2  ->  EOM: {sp.simplify(EL)} = 0")
order = max(sum(c for _, c in d.variable_count) for d in EL.atoms(sp.Derivative))
check(order == 4, f"the EOM is order {order}, not 2 -- Ostrogradsky's hypothesis is met (a "
                  f"nondegenerate second-derivative Lagrangian)")
roots = sp.solve(sp.Eq(eps_s * lam ** 4 - lam ** 2 - om_s ** 2, 0), lam ** 2)
pos = [rt for rt in roots if sp.simplify(rt.subs({eps_s: sp.Rational(1, 100), om_s: 1})) > 0]
lam2 = float(pos[0].subs({eps_s: 0.01, om_s: 1.0}))
check(len(pos) == 1 and lam2 > 0,
      f"one characteristic root is lambda^2 = {lam2:.4f} > 0 -> a REAL exponential runaway at rate "
      f"{np.sqrt(lam2):.3f} ~ 1/sqrt(eps); the other root is oscillatory")
# and the Ostrogradsky Hamiltonian is unbounded below (linear in p1)
Q, P1, P2 = sp.symbols('Q p1 p2', real=True)
Hostro = P1 * Q + P2 ** 2 / (2 * eps_s) - Q ** 2 / 2 + om_s ** 2 * sp.Symbol('q') ** 2 / 2
h_neg = float(Hostro.subs({P1: -1e6, Q: 1.0, P2: 0, eps_s: 0.01, om_s: 1.0, sp.Symbol('q'): 0}))
h_pos = float(Hostro.subs({P1: +1e6, Q: 1.0, P2: 0, eps_s: 0.01, om_s: 1.0, sp.Symbol('q'): 0}))
check(h_neg < 0 < h_pos and abs(h_neg) > 1e5,
      f"H = p1 Q + p2^2/2eps - Q^2/2 + V is LINEAR in p1: H = {h_neg:.2e} and {h_pos:.2e} at the same "
      f"(q,Q) -- unbounded below, the Ostrogradsky ghost")
print("       ESCAPE, named and NOT closed: DHOST degeneracy.  But the DHOST classification (Langlois")
print("       and Noui 2016; Ben Achour+ 2016) is built from disformal functions of (phi,X) ONLY -- a")
print("       disformal factor depending on d^2 phi is OUTSIDE it, so degeneracy would have to be")
print("       established from scratch.  Generic members carry the ghost above.  OPEN, not closed.")

# ==================================================================
banner("S11.  THE INHERITED EPHEMERIS LIABILITY -- and a HARDER statement the disformal frame adds")
# ==================================================================
g_1au = GM_SUN / AU ** 2
print(f"  g_bar(1 AU) = {g_1au:.5e} m/s^2;  Earth 2-sigma on a constant sunward anomaly = "
      f"{EARTH_LIMIT:.3e} m/s^2")
print(f"\n  {'footing':<12s} {'a0/2':>12s} {'alpha=1 anomaly @1AU':>21s} {'x bound':>9s} "
      f"{'alpha=2 anomaly':>16s} {'x bound':>10s}")
for fl, a0v in (("canonical", a0c), ("ALT", a0a)):
    an1 = float(nu_minus_1(g_1au / a0v, 1.0)) * g_1au
    an2 = float(nu_minus_1(g_1au / a0v, 2.0)) * g_1au
    print(f"  {fl:<12s} {a0v/2:12.4e} {an1:21.4e} {an1/EARTH_LIMIT:9.0f} {an2:16.4e} "
          f"{an2/EARTH_LIMIT:10.2e}")
an1c = float(nu_minus_1(g_1au / a0c, 1.0)) * g_1au
an1a = float(nu_minus_1(g_1au / a0a, 1.0)) * g_1au
check(abs(an1c / (a0c / 2) - 1) < 1e-7 and abs(an1c / EARTH_LIMIT - 1278) < 6,
      f"alpha=1 forces exactly a0/2 = {an1c:.4e} = {an1c/EARTH_LIMIT:.0f}x the bound (canonical) and "
      f"{an1a/EARTH_LIMIT:.0f}x (ALT) -- reproducing the corpus's 1278x / 1543x")
print("  DOES THE DISFORMAL COMPLETION SOFTEN IT?  No, and the reason is structural: every branch")
print("  above works by IMPOSING g_obs = nu g_bar, so the anomaly is whatever the kernel says.  The")
print("  completion is KERNEL-AGNOSTIC: it inherits the liability verbatim, with coefficient 1.000.")
# verify: in the nonlocal branch the anomaly at 1 AU is grad(D)/2 = (nu-1) g_bar, identically
an_nonlocal = dW_dr(AU, GM_SUN / G_SI, a0c, 1.0)
check(abs(an_nonlocal / (a0c / 2) - 1) < 1e-7,
      f"nonlocal branch: grad D/2 = (nu-1) g_bar at 1 AU = {an_nonlocal:.6e} = a0/2 to "
      f"{abs(an_nonlocal/(a0c/2)-1):.1e} -- inherited, factor 1.000, NOT softened")
print("  Relief is available only where it always was: alpha >= 2 (SPARC cost 0.0084 dex, "
      "corpus-established).")

print("\n  ** WHAT THE DISFORMAL FRAME ADDS, AND IT IS HARDER THAN A BOUND VIOLATION **")
print("  D = 1 - C with grad C = 2(nu-1) g_bar, so on alpha=1 dC/dr -> a0 = CONSTANT.  Integrated:")
for fl, a0v in (("canonical", a0c), ("ALT", a0a)):
    dC1 = quad(lambda rr: 2 * dW_dr(rr, GM_SUN / G_SI, a0v, 1.0), 0.3871 * AU, 9.5826 * AU, limit=400)[0]
    dC2 = quad(lambda rr: 2 * dW_dr(rr, GM_SUN / G_SI, a0v, 2.0), 0.3871 * AU, 9.5826 * AU, limit=400)[0]
    print(f"    {fl:<10s} Mercury->Saturn:  Delta C (alpha=1) = {dC1:10.2f}   "
          f"Delta C (alpha=2) = {dC2:.3e}")
    if fl == "canonical":
        dC1c, dC2c = dC1, dC2
check(dC1c > 100 and dC2c < 1e-3,
      f"on alpha=1, C varies by {dC1c:.0f} across Mercury-Saturn, so D = 1 - C goes NEGATIVE: g_eff "
      f"LOSES LORENTZIAN SIGNATURE (S2 requires D>0) inside Saturn's orbit -- the alpha=1 disformal "
      f"completion is not merely bounded-out, it is ILL-DEFINED there.  alpha=2 gives {dC2c:.1e}, safe")
check(abs(dC1c * 2 / 257.4 - 1) < 0.05,
      f"cross-check against the committed mi_disformal_tail_freedom_2026.py: its photon Delta B = 258 "
      f"and mine is Delta C = {dC1c:.0f} = Delta B/2 exactly ({2*dC1c:.0f} vs 258) -- the two scripts "
      f"agree, and this is the SAME a0/2 number in a second sector, NOT independent evidence")

# ==================================================================
banner("VERDICT")
# ==================================================================
print("  1. THE CONSTRUCTION IS REAL AND IT IS GENUINELY MODIFIED INERTIA. On g_eff the")
print("     nonrelativistic Lagrangian is L = (1/2)M(x)v^2 - U(x) with a position-dependent inertial")
print("     mass M = m S/sqrt(T) (S3). That is the right shape for this framework, not an analogy.")
print("  2. THE LITERAL (phi,X) CLASS CANNOT DO IT, three ways (S5): shift symmetry plus the corpus's")
print("     own ghost-condensate attractor P'(X)=0 make A,B CONSTANTS -> no MOND; off the attractor")
print(f"     the only scalar is Phi while nu is a function of |grad Phi| (two systems at equal Phi need")
print(f"     boosts {dex_pair:.3f} dex apart); and the size needed is |dlnA/dlnX| ~ {slope_needed:.1e},")
print("     INSIDE the corpus's own 3.8e5-3.8e7 no-go-(ii) window. The disformal escape REPRODUCES the")
print("     (v/c)^2 wall rather than escaping it.")
print("  3. A LOCAL DRESSING CANNOT DO IT AT ALL (S6 theorem): the boost carries an explicit 1/r and")
print("     an explicit local log-slope p, so universality over system SIZE and over p forces both")
print("     disformal functions constant. Fitting one geometry (p=2) and reading off another")
print(f"     mispredicts by up to {worst:.3f} dex ({worst/RAR_SCATTER_INTRINSIC:.0f}x the marginalised")
print("     intrinsic RAR scatter), as a p-correlated systematic rather than scatter.")
print("  4. ** THE NEW NO-GO, AND IT IS THE HEADLINE: THE ENHANCEMENT IS THE MATTER LIGHT CONE. **")
print("     (matter cone/photon cone)^2 = D/A exactly, gauge-independently, and blind to the conformal")
print("     factor (S4). So the whole cone bill is charged to B -- the same B that has to carry the")
print("     enhancement. Local-A branch: cone^2 = boost x O(1), i.e. O(1) SUPERLUMINAL matter exactly")
print(f"     where MOND operates ({100*(cone_max-1):.0f}% at y=1e-3, unbounded as y -> 0). Nonlocal")
print(f"     branch: mismatch = |Phi_M-Phi|/c^2 = {d_mw:.2e} for the MW and "
      f"{mismatch[('dwarf    0.5->5 kpc','canonical')]:.1e} for a dwarf, forced to ~v_c^2/c^2 by the")
print(f"     flat rotation curve itself -> PHOTON DECAY violated by {min(viol.values()):.1e} (1 TeV,")
print(f"     conservative) to {max(viol.values()):.1e} (1 PeV). Every assignment of g_eff closes:")
print(f"     matter-only by photon decay, matter+light by GW170817 ({dt_gw/1.7:.0e}x, reproducing the")
print("     committed TENSION script), universal by being modified GRAVITY plus GW170817 again.")
print("  5. AGAINST INTEREST IN BOTH DIRECTIONS. FOR the framework: the matter-only assignment EVADES")
print("     GW170817 exactly (photon and graviton share g), which the committed photon-disformal route")
print("     fails by ~1e15 -- so this lane is a 3-9 order improvement on the corpus's own lensing")
print("     construction, and it independently VINDICATES MATTER_COUPLING.md sec1's refusal of a")
print("     disformal matter metric, for a reason that document did not have (the cone). AGAINST the")
print("     framework: it removes a listed escape. AGAINST the kill: the CONFORMAL piece (B=0) is")
print("     cone-exact to all orders and does reproduce the law with no large factor (S9) -- so")
print("     'metric couplings' are NOT closed wholesale. What that survivor costs is exact: photons")
print("     are conformally blind in 4D (verified in D dimensions), so it buys ZERO lensing, and it")
print("     is a fifth force on one metric = AQUAL/Bekenstein-Milgrom modified GRAVITY, which is not")
print("     a completion of modified INERTIA and which inherits AQUAL's Cassini-Q2 bill. This is the")
print("     TeVeS split re-derived from inside: the cone-safe piece cannot lens, the lensing piece")
print("     cannot pass the cone.")
print("  6. GHOSTS (S10): ghost-freedom is a CONSTRAINT, not a property. Signature needs A>0, D>0;")
print("     dof preservation needs A - X A_X - X^2 B_X != 0; the 2x2 kinetic matrix needs det K > 0,")
print("     whose window narrows as 1/slope^2 -- so the ~1e6 slope MOND requires costs ~1e12 of it.")
print("     The extended class trips the hinge the corpus's OWN Ostrogradsky script named (dynamical")
print("     phi => a ~ d^2 phi): explicit 4th-order EOM, real runaway root, H unbounded below. DHOST")
print("     degeneracy is the named escape and is NOT closed -- but DHOST is classified for (phi,X)")
print("     functions only, so it does not cover this case as it stands.")
print("  7. THE EPHEMERIS LIABILITY IS INHERITED VERBATIM (S11), coefficient 1.000, because every")
print("     working branch IMPOSES g_obs = nu g_bar: 1278x (canonical) / 1543x (ALT) over the Earth")
print("     2-sigma bound on alpha=1. Not softened, not evaded, by any disformal-specific mechanism.")
print("     And the frame adds something HARDER than a bound violation: grad C = 2(nu-1) g_bar makes")
print("     C vary by ~129 across Mercury-Saturn on alpha=1, so D = 1 - C < 0 and g_eff LOSES")
print("     LORENTZIAN SIGNATURE inside Saturn's orbit -- ill-defined, not merely excluded. That is")
print("     exactly half the committed photon Delta B = 258, confirming both scripts and confirming")
print("     it is the SAME a0/2 number in a second sector, not independent evidence. alpha >= 2 fixes")
print("     all of it at the corpus's established 0.0084 dex SPARC cost.")
print("  8. SCOPE. This closes ONE listed escape (disformal rho_m, at the CLASSICAL level). The other")
print("     listed escapes are untouched and stay OPEN: non-quadratic-in-u terms, rho_m/T_munu")
print("     coupling, the b-projector at third-derivative cost, finite parts, all-orders rigidity,")
print("     T_munu variation, ephemeris de/dt. P8 (the loop-sector rho_m definition) also stays open.")
print("     The RAR, BTFR, a0-line, spherical work and a0 = kappa c sqrt(G rho_Lambda) are UNAFFECTED.")
print("     kappa = 1/2 remains FITTED, not derived. Nothing here derives a0, Z or the sign s.")

print(f"\n{_n_ok}/{_n_tot} checks held.")
raise SystemExit(0 if _n_ok == _n_tot else 1)
