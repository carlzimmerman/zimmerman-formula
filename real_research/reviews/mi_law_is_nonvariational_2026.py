#!/usr/bin/env python3
r"""mi_law_is_nonvariational_2026.py -- SWINGING AT THE CLOSURE-VS-ACTION GAP, and finding the
obstruction is one level deeper than the action: THE FRAMEWORK'S OWN LAW IS NOT VARIATIONAL IN A DISC.

THE PLAN THAT MOTIVATED THIS. mi_action_eom_vs_rar_2026 showed the framework's law is not the EOM of
its published action, and named the obvious repair: build the action on the SCALAR first moment,
S = -1/2 INT sqrt(-g) rho_m F(u^mu Box_u u_mu / a0^2), since Theorem B makes that argument exactly
+|a|^2. This script tests that repair. It fails, for a reason that also kills every other candidate of
that shape, and the reason is worth more than the repair would have been.

WHAT IS ESTABLISHED (each step symbolic, with a mutation control that must break it)

  T1  The Euler-Lagrange equation of ANY L(x, v) is AFFINE in the acceleration, with coefficient matrix
      d^2L/dv_i dv_j depending on (x, v) only. Proved by explicit chain rule in 2D.
  T2  The framework's law WRITTEN IN mu-FORM, mu_fw(|a|/a0) a_i + d_i phi = 0, is NOT affine in the
      acceleration: d^2E_1/dA_1^2 = 2 sqrt5/(25 a0) at |a| = a0. So in that form it is the EL equation
      of no first-order Lagrangian. MUTATION: Newtonian mu = 1 gives exactly 0.
  T3  But the SOLVED form a_i = nu(|grad phi|/a0)(-d_i phi) IS affine (coefficient delta_ij), so T2 is
      about the writing, not the physics. Everything reduces to ONE question: is nu*grad(phi) a
      GRADIENT? The obstruction is curl F = nu_R phi_z - nu_z phi_R, which vanishes IFF grad(nu) is
      parallel to grad(phi) -- iff the level sets of |grad phi| coincide with the equipotentials.
  T4  SPHERICAL SYMMETRY: they do coincide, identically. So the framework's law IS variational for a
      point mass or any spherical system, and admits a potential Psi with grad Psi = nu grad phi.
  T5  A DISC: they do not. Quantified for a Miyamoto-Nagai disc with Milky-Way parameters, BOTH kernels
      and BOTH a0 footings, as the circulation INT F.dl around a closed meridional loop -- the spurious
      work per unit mass gained per circuit. MUTATION: nu = const returns 0 to machine precision.
  T6  What this costs and what it does not, and the PRIOR ART, which is not ours.

PRIOR ART, up front. That the ALGEBRAIC MOND relation g = nu(g_N) g_N is not derivable from a
Lagrangian and violates conservation laws in non-symmetric configurations is KNOWN and is not a
discovery of this script -- see Milgrom's own remarks and the review of Famaey & McGaugh (2012),
Living Rev. Relativity 15, 10, which treats the algebraic relation as a limit/recipe rather than a
theory. What is computed here is specific: the size of the defect for THIS framework's own mu, in the
disc geometry where THIS framework's 0.108 dex RAR fit is performed, on both footings.

Exit 0 = ran and every internal check held. No hard-coded verdicts.
"""
from __future__ import annotations

import math
import sys

import numpy as np
import sympy as sp

ok: list[tuple[bool, str]] = []


def check(cond: bool, msg: str) -> bool:
    cond = bool(cond)
    ok.append((cond, msg))
    print(f"  [{'OK' if cond else 'FAIL'}] {msg}")
    return cond


def banner(t: str) -> None:
    print("\n" + "=" * 100)
    print(f"  {t}")
    print("=" * 100)


C = 2.99792458e8
G = 6.67430e-11
MSUN = 1.98892e30
KPC = 3.0856775814913673e19
MPC = 3.0856775814913673e22
H0 = 67.66e3 / MPC
OMEGA_L = 0.6889
Z_FACTOR = math.sqrt(32.0 * math.pi / 3.0)
FOOTINGS = {"canon": C * H0 * math.sqrt(OMEGA_L) / Z_FACTOR, "alt": C * H0 / Z_FACTOR}


# ------------------------------------------------- the framework's own nu, both kernels
def nu1(y: np.ndarray) -> np.ndarray:
    """alpha=1: g_obs^2 = g_bar^2 + a0 g_bar  =>  nu = sqrt(1 + 1/y)."""
    return np.sqrt(1.0 + 1.0 / y)


def nu2(y: np.ndarray) -> np.ndarray:
    """alpha=2: mu(x)=x/sqrt(1+x^2) => y = x^2/sqrt(1+x^2) => x^4 - y^2 x^2 - y^2 = 0."""
    y2 = y * y
    x2 = (y2 + np.sqrt(y2 * y2 + 4.0 * y2)) / 2.0
    return np.sqrt(x2) / y


NUS = {"alpha=1": nu1, "alpha=2": nu2}


banner("T1  THE EL EQUATION OF ANY L(x,v) IS AFFINE IN THE ACCELERATION")

x1, x2, v1, v2, A1, A2 = sp.symbols("x1 x2 v1 v2 A1 A2", real=True)
Lsym = sp.Function("L")(x1, x2, v1, v2)
X, V, Avec = (x1, x2), (v1, v2), (A1, A2)
E = []
for i in range(2):
    dLdv = sp.diff(Lsym, V[i])
    tot = (sum(V[j] * sp.diff(dLdv, X[j]) for j in range(2))
           + sum(Avec[j] * sp.diff(dLdv, V[j]) for j in range(2)))
    E.append(sp.expand(tot - sp.diff(Lsym, X[i])))
print(f"  E_1 = {E[0]}")
check(sp.diff(E[0], A1, 2) == 0 and sp.diff(E[0], A1, 1, A2, 1) == 0,
      "T1 every second derivative of E_1 with respect to the accelerations VANISHES -> the EL equation "
      "of any L(x,v) is AFFINE in the acceleration")
check(sp.diff(E[0], A1) == sp.diff(Lsym, v1, 2),
      "T1b and the coefficient of A_1 is exactly d^2L/dv_1^2, a function of (x,v) only -- it cannot "
      "itself depend on the acceleration")


banner("T2  THE FRAMEWORK'S LAW IN mu-FORM IS NOT AFFINE  (and the control that proves the test bites)")

a0s = sp.Symbol("a0", positive=True)
am = sp.sqrt(A1**2 + A2**2)
mu_fw = (sp.sqrt(1 + 4 * (am / a0s) ** 2) - 1) / (2 * (am / a0s))
E1 = sp.simplify(mu_fw * A1)
d2 = sp.simplify(sp.diff(E1, A1, 2))
val = sp.simplify(d2.subs({A2: 0, A1: a0s}))
print(f"  d^2E_1/dA_1^2 at |a| = a0 :  {val}   =  {float(val.subs(a0s, 1)):.6f} / a0")
check(sp.simplify(val) != 0,
      f"T2 the framework's mu-form law is NOT affine in the acceleration ({val}), so in that form it is "
      f"the EL equation of NO first-order Lagrangian")
check(sp.diff(1 * A1, A1, 2) == 0,
      "T2b MUTATION CONTROL: with mu = 1 (Newtonian) the same quantity is exactly 0, so the test "
      "discriminates and did not merely fire on the algebra's complexity")


banner("T3  THE SOLVED FORM IS AFFINE -- so everything reduces to ONE gradient question")

R, z = sp.symbols("R z", real=True)
phiF, nuF = sp.Function("phi")(R, z), sp.Function("nu")(R, z)
FR, Fz = -nuF * sp.diff(phiF, R), -nuF * sp.diff(phiF, z)
curl = sp.simplify(sp.diff(FR, z) - sp.diff(Fz, R))
print(f"  a_i = nu(|grad phi|/a0)(-d_i phi): coefficient of the acceleration is delta_ij, so AFFINE.")
print(f"  curl F (azimuthal) = {curl}")
target = sp.diff(nuF, R) * sp.diff(phiF, z) - sp.diff(nuF, z) * sp.diff(phiF, R)
check(sp.simplify(curl - target) == 0,
      "T3 curl F = nu_R phi_z - nu_z phi_R exactly -> it vanishes IFF grad(nu) || grad(phi), i.e. iff "
      "the level sets of |grad phi| coincide with the equipotentials")


banner("T4  SPHERICAL SYMMETRY -- the level sets DO coincide, so the law IS variational there")

r = sp.Symbol("r", positive=True)
phi_sph = sp.Function("f")(r)                    # any spherical potential
gmag = sp.Abs(sp.diff(phi_sph, r))               # |grad phi| = |f'(r)|, a function of r ALONE
print(f"  spherical: phi = f(r), |grad phi| = |f'(r)| -- BOTH depend on r only, so nu = nu(r) too.")
# in spherical symmetry F is radial with magnitude depending only on r => curl == 0 identically
rr, th = sp.symbols("rho theta", positive=True)
phi_pm = -sp.Symbol("GM", positive=True) / rr    # point mass, as a concrete instance
g_pm = sp.simplify(sp.diff(phi_pm, rr))
check(sp.simplify(sp.diff(g_pm, th)) == 0,
      "T4 for a point mass |grad phi| has no angular dependence, so nu is a function of r alone and "
      "F = -nu(r) f'(r) r_hat is a pure radial field of r -> curl == 0 IDENTICALLY")
# Construct Psi EXPLICITLY for a point mass on the alpha=1 kernel and verify grad Psi = nu grad phi.
rv, GMs, a0p = sp.symbols("r GM a_0", positive=True)
phi_r = -GMs / rv
g_r = sp.diff(phi_r, rv)                       # = GM/r^2, the Newtonian magnitude
y_r = g_r / a0p
nu_r = sp.sqrt(1 + 1 / y_r)                    # alpha=1: nu = sqrt(1 + 1/y)
integrand = sp.simplify(nu_r * g_r)
Psi = sp.integrate(integrand, rv)
resid = sp.simplify(sp.diff(Psi, rv) - integrand)
print(f"  explicit Psi for a point mass (alpha=1):  Psi(r) = {sp.simplify(Psi)}")
print(f"  d(Psi)/dr - nu*phi' = {resid}")
check(sp.simplify(resid) == 0,
      "T4b a potential Psi with grad Psi = nu grad phi is CONSTRUCTED explicitly for a point mass and "
      "verified to satisfy it exactly -- so the framework's law is fully variational for spherical "
      "systems, not merely un-obstructed")


banner("T5  A DISC -- the level sets do NOT coincide. How large is the defect?")

# Miyamoto-Nagai disc, Milky-Way-like: phi = -GM / sqrt(R^2 + (a + sqrt(z^2+b^2))^2)
M_DISC = 6.0e10 * MSUN
A_MN, B_MN = 3.0 * KPC, 0.3 * KPC
GM = G * M_DISC


def phi_mn(Rv, zv):
    zeta = np.sqrt(zv * zv + B_MN * B_MN)
    return -GM / np.sqrt(Rv * Rv + (A_MN + zeta) ** 2)


def grad_phi_mn(Rv, zv):
    zeta = np.sqrt(zv * zv + B_MN * B_MN)
    s2 = Rv * Rv + (A_MN + zeta) ** 2
    s3 = s2 ** 1.5
    return GM * Rv / s3, GM * (A_MN + zeta) * zv / (s3 * zeta)


def force(Rv, zv, nufun, a0):
    """F = nu(|grad phi|/a0) * (-grad phi), the framework's law solved for the acceleration."""
    pR, pz = grad_phi_mn(Rv, zv)
    g = np.hypot(pR, pz)
    n = nufun(g / a0)
    return -n * pR, -n * pz


_TRAPZ = getattr(np, "trapezoid", None) or np.trapz   # np.trapezoid is numpy>=2.0 only


def circulation(nufun, a0, R1, R2, z1, z2, N=1400):
    """INT F.dl anticlockwise around the meridional rectangle [R1,R2] x [z1,z2], in m^2/s^2."""
    tot = 0.0
    Rs = np.linspace(R1, R2, N)
    zs = np.linspace(z1, z2, N)
    dR, dz = Rs[1] - Rs[0], zs[1] - zs[0]
    fR, _ = force(Rs, np.full_like(Rs, z1), nufun, a0);  tot += _TRAPZ(fR, dx=dR)
    _, fz = force(np.full_like(zs, R2), zs, nufun, a0);  tot += _TRAPZ(fz, dx=dz)
    fR, _ = force(Rs, np.full_like(Rs, z2), nufun, a0);  tot -= _TRAPZ(fR, dx=dR)
    _, fz = force(np.full_like(zs, R1), zs, nufun, a0);  tot -= _TRAPZ(fz, dx=dz)
    return tot


LOOP = (4.0 * KPC, 12.0 * KPC, 0.0 * KPC, 2.0 * KPC)
V_CIRC = 200e3
print(f"  Miyamoto-Nagai: M = {M_DISC/MSUN:.2e} Msun, a = {A_MN/KPC:.1f} kpc, b = {B_MN/KPC:.1f} kpc")
print(f"  loop: R = {LOOP[0]/KPC:.0f}-{LOOP[1]/KPC:.0f} kpc, z = {LOOP[2]/KPC:.0f}-{LOOP[3]/KPC:.0f} kpc\n")
print(f"  {'kernel':<10}{'footing':<9}{'circulation [m^2/s^2]':>24}{'as fraction of v_c^2':>22}")
print("  " + "-" * 90)
circs = {}
for kname, nufun in NUS.items():
    for fname, a0 in FOOTINGS.items():
        cval = circulation(nufun, a0, *LOOP)
        circs[(kname, fname)] = cval
        print(f"  {kname:<10}{fname:<9}{cval:>24.6e}{abs(cval)/V_CIRC**2:>22.4%}")

check(all(abs(v) > 0 for v in circs.values()),
      "T5 the circulation is NONZERO on every kernel and every footing -> nu*grad(phi) is not a "
      "gradient in a disc, so the framework's law admits NO potential there and is NOT variational")
frac = max(abs(v) for v in circs.values()) / V_CIRC**2
check(frac > 1e-3,
      f"T5b and it is not a rounding effect: the largest circulation is {frac:.2%} of v_c^2 = "
      f"(200 km/s)^2, i.e. a spurious energy gain of that order per meridional circuit")

# N-CONVERGENCE: the number is load-bearing, so show it is not a quadrature artefact.
seq = [circulation(nu1, FOOTINGS["canon"], *LOOP, N=N) for N in (700, 1400, 2800, 5600)]
rel = abs(seq[-1] - seq[-2]) / abs(seq[-1])
print(f"\n  N-convergence (alpha=1, canon): " + "  ".join(f"{v:.6e}" for v in seq))
check(rel < 1e-4,
      f"T5e the circulation is CONVERGED -- the last doubling of the quadrature changes it by "
      f"{rel:.2e}, so {seq[-1]:.4e} m^2/s^2 is the integral and not a discretisation artefact")

# PHYSICAL READING: what the non-conservation is worth in velocity
dE = abs(seq[-1])
dv = math.sqrt(2.0 * dE)
print(f"  physical reading: a closed meridional circuit gains {dE:.3e} m^2/s^2 of specific energy,")
print(f"  an equivalent velocity kick of sqrt(2 dE) = {dv/1e3:.1f} km/s = {dv/V_CIRC:.1%} of v_c.")
check(dv / V_CIRC > 0.05,
      f"T5f and stated in velocity rather than energy the defect is {dv/1e3:.1f} km/s, {dv/V_CIRC:.1%} of "
      f"a 200 km/s disc -- large enough that it cannot be dismissed as a formal blemish")

# MUTATION CONTROL: a constant nu must give exactly zero circulation
zero = circulation(lambda y: np.ones_like(y), FOOTINGS["canon"], *LOOP)
print(f"\n  MUTATION CONTROL, nu = 1 identically (Newtonian): circulation = {zero:.3e} m^2/s^2")
check(abs(zero) < 1e-4 * max(abs(v) for v in circs.values()),
      "T5c MUTATION: with nu constant the circulation collapses to numerical zero, so the effect is "
      "produced by nu's DEPENDENCE on |grad phi| and not by the quadrature or the loop choice")
# and it must vanish for a SPHERICAL potential too, confirming T4 numerically
sav_a, sav_b = A_MN, B_MN
A_MN, B_MN = 0.0, 1e-9 * KPC          # collapses Miyamoto-Nagai to a point mass
sph = circulation(nu1, FOOTINGS["canon"], *LOOP)
A_MN, B_MN = sav_a, sav_b
print(f"  MUTATION CONTROL, same law on a SPHERICAL (point-mass) potential: {sph:.3e} m^2/s^2")
check(abs(sph) < 1e-4 * max(abs(v) for v in circs.values()),
      "T5d MUTATION: the same law on a spherical potential gives numerical zero, confirming T4 -- the "
      "defect is a property of the GEOMETRY, not of the law alone")


banner("T6  WHAT THIS COSTS, WHAT IT DOES NOT, AND WHOSE RESULT IT IS")

print(f"""  THE ANSWER TO THE REPAIR THAT MOTIVATED THIS SCRIPT: it cannot work, and not because the
  scalar F(u.Box_u u) is the wrong choice. T1 says any first-order Lagrangian gives an acceleration-
  affine EOM; T3-T5 say the framework's law, in the geometry where it is fit, is not the gradient of
  anything. A law that admits no potential in a disc is not the EL equation of ANY action there --
  local, nonlocal, scalar-argument or operator-argument. So the closure-vs-action gap is not a gap to
  be closed by writing a better action. It is an OBSTRUCTION one level below the action.

  WHAT IS *NOT* DAMAGED, and this is most of the corpus:
   * THE RAR FIT AND EVERY ROTATION-CURVE NUMBER. Circular-orbit fitting uses only the RADIAL force in
     the midplane, v_c^2/R = |F_R(R, 0)|. A non-vanishing circulation is a statement about closed
     loops that leave the plane. The 0.108 dex fit, the a0-line and the BTFR are untouched.
   * SPHERICAL SYSTEMS. By T4 the law is exactly variational there, so dwarf-spheroidal and cluster
     work built on spherical models does not inherit this.
   * The MOND regime itself, and the interpolation's shape.

  WHAT IS DAMAGED:
   * There is no energy functional for disc dynamics under this law, hence no conserved energy for
     off-plane orbits, no well-posed N-body problem, and no variational route from the law to a
     lensing or cosmological extension.
   * Vertical dynamics is not predicted by the same law that fits the rotation curve: the two are
     inequivalent at the {frac:.1%} level of v_c^2 per circuit, i.e. {dv/1e3:.0f} km/s of spurious
     velocity ({dv/V_CIRC:.0%} of v_c) around the loop computed above.
   * It explains, at the root, WHY the published action's EOM was not the law
     (mi_action_eom_vs_rar_2026) -- the law was never the EOM of anything in this geometry.

  PRIOR ART, which is not ours and must be said first. That the ALGEBRAIC MOND relation
  g = nu(g_N) g_N is non-variational and violates conservation laws away from symmetry is KNOWN --
  Milgrom's own remarks, and Famaey & McGaugh (2012), Living Rev. Relativity 15, 10, which present the
  algebraic relation as a recipe rather than a theory, precisely for this reason. AQUAL and QUMOND
  exist to cure it, and they cure it by modifying GRAVITY, where the force is a gradient by
  construction. What is this script's own contribution is narrow: the defect's SIZE for this
  framework's own mu, on both kernels and both a0 footings, in the disc geometry where this framework's
  own fit is performed -- and the observation that it is the root of the corpus's named
  closure-vs-action gap rather than a separate issue.

  WHAT WOULD FIX IT, in decreasing order of plausibility:
   1. Adopt the MG realization (AQUAL/QUMOND-like) for disc dynamics, where the force is a gradient by
      construction and the circulation is identically zero. Cost: the framework stops being modified
      INERTIA in that regime, which is its distinctive claim.
   2. A genuinely nonlocal MI whose response reproduces mu_fw in the midplane while remaining
      variational -- this is what the published K(Box_u) action was for, and its amplitude problem
      (|K| -> 1, no MOND) is the open item to solve. This is the honest place to push.
   3. Accept the law as a midplane RECIPE, state that off-plane dynamics is outside its scope, and stop
      describing it as a force law. Honest, and much weaker than the current presentation.""")

banner("RESULT")
npass = sum(1 for c, _ in ok if c)
print(f"  {npass}/{len(ok)} checks held.")
if npass != len(ok):
    print("\n  FAILED CHECKS:")
    for c, m in ok:
        if not c:
            print(f"    - {m}")
    sys.exit(1)
print("  Exit 0: every internal check held, including three mutation controls.")
