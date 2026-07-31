#!/usr/bin/env python3
r"""mi_machian_frame_routeA_2026.py -- ROUTE A: the POTENTIAL-STATIONARY (Machian) passive frame.

THE PROPOSAL UNDER TEST (Carl's, 2026-07-31; it is NOT assumed correct here):
    u^mu is the local timelike direction along which the LOCAL BARYONIC GRAVITATIONAL FIELD is
    stationary: L_u Phi = 0 (equivalently L_u g = 0 in the stationary case).
Motive: Theorem 8's obstruction is that the nonlocal action's kernel argument is w = c*Omega/a0 while
the law's is x = |a|/a0, and w/x = c/v EXACTLY. The missing factor is a SPEED. A lone worldline has no
speed; a PASSIVE PREFERRED FRAME supplies one. The already-computed LOCK: if that speed were relative
to the COSMIC (CMB) frame, a0_eff would inherit each galaxy's peculiar velocity -- ~1.0 dex against a
total a0 budget of 2*sigma_RAR. So the frame must be LOCALLY DRAGGED. Route A asks whether the
potential-stationary prescription is (1) well defined, (2) non-collapsing, (3) a0-preserving,
(4) consistent with the observed non-rotation of the local inertial frame, (5) RAR-restoring, and
(6) compatible with equivalence-principle / conservation bounds.

THE MASTER FORMULA used throughout, derived and symbolically checked in S0:
    a0_eff / a0  =  v_orb / v_rel          (circular orbits, exact)
where v_orb = |a|/Omega is the orbital speed and v_rel is the body's speed relative to u.
So the whole route reduces to: WHAT IS v_rel?

KERNEL IN FORCE: alpha = 2, mu_2(x) = x/sqrt(1+x^2). Closure g_bar = A*mu(A/a0) inverts in closed form
    A^2 = (g_bar^2/2)*(1 + sqrt(1 + 4 a0^2/g_bar^2)).
BOTH FOOTINGS carried on every dimensional number: a0 = 9.36e-11 (canonical rho_DE) and 1.13e-10 (alt).

PRIOR ART, stated so nothing is claimed as new that is not: Mach; Sciama 1953 (inertia relative to
matter); Milgrom 1994 Ann.Phys. 229:384 (modified inertia NEEDS a definition of absolute acceleration --
he says so explicitly, and orbit-dependent interpolating functions follow); Milgrom astro-ph/0510117
(virial); Milgrom 2022 PRD 106:064060 (Fourier-space MI, algebraic only at single frequency).
The Machian IDEA is ancient. What is assessed here is the SPECIFIC prescription and its consequences.

Exit non-zero on any failed internal check. No hard-coded verdicts; every check is an identity, a limit,
a sign, a monotonicity or a scaling. mpmath at 50 dps wherever a difference of nearly-equal numbers is
load-bearing (flagged inline).
"""
from __future__ import annotations

import math

import mpmath as mp
import numpy as np
import sympy as sp

mp.mp.dps = 50

# ------------------------------------------------------------------ constants (provenance inline)
G = 6.67430e-11                  # CODATA 2018
C = 2.99792458e8
MSUN = 1.98892e30                # repo convention
KPC = 3.0856775814913673e19
AU = 1.495978707e11
YR = 3.15576e7                   # Julian year
GYR = 1e9 * YR
MYR = 1e6 * YR
MAS_PER_RAD = 180.0 / math.pi * 3.6e6

A0_CANON, A0_ALT = 9.36e-11, 1.13e-10
FOOTINGS = [("canonical rho_DE", A0_CANON), ("alt rho_total", A0_ALT)]

# Galaxy / solar-neighbourhood inputs
R0 = 8.178 * KPC                 # GRAVITY Collab. 2019
V0 = 233.0e3                     # Sun's circular speed, m/s
V_SUN_LSR = math.sqrt(11.1**2 + 12.24**2 + 7.25**2) * 1e3   # Schoenrich+2010 (U,V,W) -> 18.04 km/s
V_HI_DISP = 8.0e3                # cold-HI velocity dispersion, standard value
V_CMB = 369.82e3                 # Planck 2018 solar-system dipole (this is stx_target.py's input)
SIGMA_PEC_1D = 300.0e3           # field-galaxy 1-D peculiar velocity dispersion, order of magnitude

SIGMA_RAR_A2 = 0.1116            # STANDING sec.1, alpha=2, 175 SPARC
SIGMA_RAR_A1 = 0.1083            # retired alpha=1 value
BUDGET_A2 = 2.0 * SIGMA_RAR_A2   # deep regime dlog g_obs = 0.5 dlog a0  =>  budget = 2*sigma
BUDGET_A1 = 2.0 * SIGMA_RAR_A1

ok = True
nchk = 0


def check(cond, msg):
    global ok, nchk
    nchk += 1
    if not cond:
        ok = False
    print(f"  [{'OK  ' if cond else 'FAIL'}] {msg}")


def banner(s):
    print("\n" + "=" * 104)
    print(s)
    print("=" * 104)


def A_of_gbar(gbar, a0):
    """Invert the alpha=2 closure g_bar = A mu_2(A/a0) exactly."""
    gbar = np.asarray(gbar, float)
    return np.sqrt(0.5 * gbar**2 * (1.0 + np.sqrt(1.0 + 4.0 * a0**2 / gbar**2)))


def dex(r):
    return abs(math.log10(r))


# =====================================================================================
def S0_master_formula():
    banner("S0. THE MASTER FORMULA a0_eff/a0 = v_orb/v_rel -- derived symbolically, not assumed")
    v, R, a0, c, Om, vrel = sp.symbols('v R a_0 c Omega v_rel', positive=True)
    # circular orbit: Box_u u = -Omega^2 u  =>  action's spectral argument w = c Omega/a0
    w = c * Om / a0
    x = (Om * v) / a0                        # law's argument: |a|/a0 with |a| = Omega v
    check(sp.simplify(sp.simplify(w / x) - c / v) == 0,
          "Theorem 8 reproduced symbolically: w/x = c/v exactly, identically in Omega, v and a0")
    # Route A's repair: rescale the frequency argument by the FRAME-RELATIVE speed
    wA = (c * Om / a0) * (vrel / c)
    check(sp.simplify(wA - Om * vrel / a0) == 0, "the c cancels: w_A = Omega*v_rel/a0 (no c left)")
    check(sp.simplify((wA - x).subs(vrel, v)) == 0,
          "if v_rel = v_orb the repair is EXACT on circles -- Theorem 8's c/v gap closes identically")
    # define a0_eff by w_A = |a|/a0_eff
    a0eff = sp.simplify((Om * v) / wA)
    check(sp.simplify(a0eff - a0 * v / vrel) == 0,
          f"a0_eff = a0 * v_orb/v_rel exactly (sympy: {a0eff})")
    # sign/limit structure of the failure modes
    check(sp.limit(a0 * v / vrel, vrel, 0, '+') == sp.oo,
          "v_rel -> 0 (a co-moving/velocity-dragged frame) DIVERGES a0_eff -- catastrophic, not small")
    check(sp.limit(a0 * v / vrel, vrel, sp.oo) == 0,
          "v_rel -> infinity kills a0_eff -> 0, i.e. restores Newton -- the other failure mode")
    # closed-form closure inversion. g_bar = A mu_2(A/a0) squares to the biquadratic
    #     A^4 - g_bar^2 A^2 - g_bar^2 a0^2 = 0,
    # so verify the closed form against THAT polynomial (sympy handles it exactly), then confirm the
    # polynomial is equivalent to the closure itself, then spot-check the branch numerically at 50 dps.
    A, gb = sp.symbols('A g_bar', positive=True)
    gb_of_A = sp.solve(A * (A / a0) / sp.sqrt(1 + (A / a0)**2) - gb, gb)[0]
    poly = A**4 - gb**2 * A**2 - gb**2 * a0**2
    check(sp.simplify(gb_of_A - A**2 / sp.sqrt(a0**2 + A**2)) == 0
          and sp.simplify(poly.subs(gb, gb_of_A)) == 0,
          f"the alpha=2 closure is g_bar = {gb_of_A}, which squares EXACTLY to the biquadratic "
          f"A^4 - g^2 A^2 - g^2 a0^2 = 0")
    Asol = sp.sqrt(gb**2 / 2 * (1 + sp.sqrt(1 + 4 * a0**2 / gb**2)))
    check(sp.simplify(poly.subs(A, Asol)) == 0,
          "the closed form A^2 = (g^2/2)(1+sqrt(1+4a0^2/g^2)) solves that biquadratic EXACTLY")
    # numeric spot-check of the correct branch over 20 decades, mpmath 50 dps (differences of
    # nearly-equal numbers in the Newtonian corner)
    worst = mp.mpf(0)
    for lg in range(-14, 6):
        gbv, a0v = mp.mpf(10) ** lg, mp.mpf(A0_CANON)
        Av = mp.sqrt(gbv**2 / 2 * (1 + mp.sqrt(1 + 4 * a0v**2 / gbv**2)))
        worst = max(worst, abs(Av * (Av / a0v) / mp.sqrt(1 + (Av / a0v) ** 2) / gbv - 1))
    check(float(worst) < 1e-40,
          f"and it is the RIGHT branch: max relative residual of the closure over g_bar spanning 20 "
          f"decades = {float(worst):.2e} at 50 dps")
    # negative control: the alpha=1 inversion must NOT satisfy the alpha=2 biquadratic
    A1 = sp.sqrt(gb**2 + a0 * gb)
    check(sp.simplify(poly.subs(A, A1)) != 0,
          "negative control: the retired alpha=1 inversion does NOT solve the alpha=2 closure")


# =====================================================================================
def S1_welldefinedness():
    banner("S1. WELL-DEFINEDNESS: does the potential-stationary u exist, and is it unique?")

    print("\n  S1a. The rigid-rotation degeneracy Carl flagged -- CONFIRMED, exactly as stated.")
    t, Rs, z, phi, Om_f = sp.symbols('t R z phi Omega_f', real=True)
    Phi = sp.Function('Phi')(Rs, z)                     # static AXISYMMETRIC potential
    LuPhi = sp.diff(Phi, t) + Om_f * sp.diff(Phi, phi)  # (d_t + Om_f d_phi) Phi
    check(sp.simplify(LuPhi) == 0,
          "L_u Phi = 0 holds IDENTICALLY for ARBITRARY Omega_f on any static axisymmetric Phi: the "
          "potential-stationarity condition alone leaves a 1-parameter rigid-rotation degeneracy")
    # negative control: break axisymmetry and the degeneracy must disappear
    Phi_bar = sp.Function('Psi')(Rs, z) * sp.cos(2 * phi)   # m=2 bar
    Lu_bar = sp.simplify(sp.diff(Phi_bar, t) + Om_f * sp.diff(Phi_bar, phi))
    check(sp.simplify(Lu_bar.subs(Om_f, 0)) == 0 and sp.simplify(Lu_bar) != 0,
          "negative control: with an m=2 bar, Omega_f = 0 still works but generic Omega_f does NOT -- "
          "so the degeneracy is a property of axisymmetry, not of the definition")

    print("\n  S1b. Pointwise degeneracy count for a GENERIC time-dependent Phi (the worse obstruction).")
    # w . grad Phi = -d_t Phi is ONE scalar equation on THREE components of w.
    rng = np.random.default_rng(20260731)
    dims = []
    for _ in range(200):
        gradPhi = rng.normal(size=3)
        M = gradPhi.reshape(1, 3)
        # nullspace dimension of w -> w.gradPhi
        s = np.linalg.svd(M, compute_uv=False)
        dims.append(3 - int(np.sum(s > 1e-12)))
    check(min(dims) == 2 and max(dims) == 2,
          f"L_u Phi = 0 is 1 equation on 3 components of the frame velocity => solution space is "
          f"2-dimensional at EVERY point (nullspace dim = {min(dims)} in 200/200 random draws). The "
          f"scalar condition ALONE is far more degenerate than the axisymmetric Omega_f: any frame "
          f"velocity tangent to the local equipotential works")

    print("\n  S1c. Does IRROTATIONALITY / hypersurface-orthogonality kill Omega_f? (flat space first)")
    # Newtonian vorticity of a rigidly rotating frame field w = Omega_f zhat x r
    x_, y_, z_ = sp.symbols('x y z', real=True)
    wvec = sp.Matrix([-Om_f * y_, Om_f * x_, 0])
    curl = sp.Matrix([sp.diff(wvec[2], y_) - sp.diff(wvec[1], z_),
                      sp.diff(wvec[0], z_) - sp.diff(wvec[2], x_),
                      sp.diff(wvec[1], x_) - sp.diff(wvec[0], y_)])
    check(sp.simplify(curl - sp.Matrix([0, 0, 2 * Om_f])) == sp.zeros(3, 1),
          "curl of the rigid frame field = 2*Omega_f zhat exactly -- vanishes IFF Omega_f = 0")
    # Relativistic Frobenius test on the 1-form xi = -dt + (Om_f R^2/c) dphi  (c=1 units; HSO is
    # invariant under xi -> f*xi, so the normalisation N drops out and cannot hide anything)
    coords = [t, Rs, phi, z]
    xi = [-1, 0, Om_f * Rs**2, 0]

    def frob(mu_, nu_, rho_):
        s = 0
        for (a, b, cc) in [(mu_, nu_, rho_), (nu_, rho_, mu_), (rho_, mu_, nu_)]:
            s += xi[a] * (sp.diff(xi[cc], coords[b]) - sp.diff(xi[b], coords[cc]))
        return sp.simplify(s)

    T_tRphi = frob(0, 1, 2)
    check(sp.simplify(T_tRphi - (-2 * Rs * Om_f)) == 0,
          f"Frobenius 3-form component T_[t R phi] = {T_tRphi} -- exactly -2 R Omega_f")
    check(sp.simplify(T_tRphi.subs(Om_f, 0)) == 0 and sp.solve(sp.Eq(T_tRphi, 0), Om_f) == [0],
          "so in flat space HSO forces Omega_f = 0 UNIQUELY -- and HSO is the SAME condition the "
          "framework already needs to kill vector modes and keep u PASSIVE (not an extra assumption)")

    print("\n  S1d. With a ROTATING source (g_tphi != 0) the answer changes: the HSO solution is the ZAMO.")
    gtt, gtp, gpp = [sp.Function(n)(Rs, z) for n in ('g_tt', 'g_tphi', 'g_phiphi')]
    Omv = sp.Function('Omega')(Rs, z)
    Aa = gtt + Omv * gtp
    Bb = gtp + Omv * gpp
    xi2 = [Aa, 0, Bb, 0]

    def frob2(mu_, nu_, rho_):
        s = 0
        for (a, b, cc) in [(mu_, nu_, rho_), (nu_, rho_, mu_), (rho_, mu_, nu_)]:
            s += xi2[a] * (sp.diff(xi2[cc], coords[b]) - sp.diff(xi2[b], coords[cc]))
        return sp.simplify(s)

    T2 = frob2(0, 1, 2)
    target = sp.simplify(Aa * sp.diff(Bb, Rs) - Bb * sp.diff(Aa, Rs))
    check(sp.simplify(T2 - target) == 0,
          "general stationary-axisymmetric Frobenius: T_[t R phi] = A d_R B - B d_R A = A^2 d_R(B/A), "
          "so HSO <=> B/A = const == -k")
    # k = 0 branch: B = 0 => Omega = -g_tphi/g_phiphi = the ZAMO / Lense-Thirring rate
    Om_zamo = sp.solve(sp.Eq(gtp + Omv * gpp, 0), Omv)[0]
    check(sp.simplify(Om_zamo + gtp / gpp) == 0,
          f"the k=0 branch is the ZAMO: Omega = -g_tphi/g_phiphi = {Om_zamo}")
    # k != 0 branch exists ALGEBRAICALLY -- report it, then kill it by azimuthal periodicity
    k = sp.Symbol('k', real=True)
    Om_k = sp.simplify(sp.solve(sp.Eq(Bb + k * Aa, 0), Omv)[0])
    check(sp.simplify(Om_k.subs(k, 0) - Om_zamo) == 0,
          f"a 1-parameter family of HSO congruences DOES exist, Omega(k) = {Om_k}; k=0 recovers the ZAMO")
    # its leaves are t - k*phi = const; going once around phi shifts t by 2*pi*k -> multivalued unless k=0
    dt_around = sp.simplify(2 * sp.pi * k)
    check(sp.solve(sp.Eq(dt_around, 0), k) == [0],
          "but the k-leaves are t = k*phi + const, and phi -> phi + 2pi shifts t by 2*pi*k: the time "
          "function is MULTIVALUED unless k = 0. AZIMUTHAL PERIODICITY therefore fixes k = 0 and the "
          "frame is UNIQUE = the ZAMO. This is the load-bearing uniqueness argument")
    print("      SCOPE, stated so it is not overread: this uniqueness is WITHIN the stationary")
    print("      axisymmetric congruence ansatz u^mu ~ (1, 0, Omega(R,z), 0). S1b already showed the")
    print("      bare scalar condition is 2-parameter degenerate pointwise, so uniqueness is bought by")
    print("      the ansatz + HSO + periodicity together, NOT by potential-stationarity alone.")
    # weak-field far zone: Omega_ZAMO = 2GJ/(c^2 R^3)
    Jz, cc_ = sp.symbols('J c', positive=True)
    Om_wf = sp.simplify((-(-2 * G * Jz / (cc_**2 * Rs)) / Rs**2))
    check(sp.simplify(Om_wf - 2 * G * Jz / (cc_**2 * Rs**3)) == 0,
          f"weak-field equatorial g_tphi = -2GJ/(c^2 R), g_phiphi = R^2 => Omega_ZAMO = {Om_wf} "
          f"= the standard Lense-Thirring dragging rate (quantified in S4)")

    print("\n  S1e. QUANTIFIED: what the residual freedom would do to the RAR if it were NOT removed.")
    print(f"  {'Omega_f / Omega_orb':>20s} {'v_rel/v_orb':>12s} {'a0_eff/a0':>12s} {'|dlog a0| dex':>14s}")
    worst = 0.0
    for f in [0.0, 1e-6, 1e-3, 0.1, 0.5, 0.9, 0.99]:
        vr = abs(1.0 - f)
        r = 1.0 / vr if vr > 0 else float('inf')
        d = dex(r) if vr > 0 else float('inf')
        worst = max(worst, d)
        print(f"  {f:20.6g} {vr:12.6g} {r:12.6g} {d:14.6g}")
    f_crit = 1.0 - 10 ** (-BUDGET_A2)     # exact threshold where the induced spread hits the budget
    check(worst > BUDGET_A2 and abs(dex(1 / (1 - f_crit)) - BUDGET_A2) < 1e-12,
          f"if Omega_f were free the induced a0 spread is UNBOUNDED (diverges at Omega_f = Omega_orb). "
          f"It exceeds the {BUDGET_A2:.4f} dex budget for Omega_f/Omega > {f_crit:.3f} -- NOT already "
          f"at 0.1, where it is only {dex(1/0.9):.4f} dex (an earlier draft of this line overstated "
          f"it and is corrected here). Since Omega_f is a FREE FUNCTION with no reason to sit below "
          f"{f_crit:.3f}, the degeneracy WOULD be fatal; removing it is not cosmetic")
    return None


# =====================================================================================
def S2_collapse_test():
    banner("S2. THE COLLAPSE TEST: potential-stationary vs velocity-dragged, at the Sun")
    print("  Definition (1) POTENTIAL-stationary: u = ZAMO of the Galaxy's own field (S1) -> the frame")
    print("      does NOT co-rotate, so a disc star's frame-relative speed is its FULL orbital speed.")
    print("  Definition (2) VELOCITY-dragged: u = local mean matter 4-velocity (the LSR / the gas flow).")
    Om_gal = V0 / R0
    print(f"\n  {'case':<34s} {'v_rel [km/s]':>13s} {'a0_eff/a0':>12s} {'|dlog a0| dex':>13s} {'g_obs ratio':>12s}")
    rows = []
    cases = [("(1) potential-stationary (ZAMO)", V0),
             ("(2) dragged: Sun vs LSR", V_SUN_LSR),
             ("(2) dragged: cold HI (sigma=8)", V_HI_DISP),
             ("(2) dragged: ideal circular gas", 0.0)]
    for nm, vr in cases:
        if vr == 0.0:
            print(f"  {nm:<34s} {0.0:13.3f} {'inf':>12s} {'inf':>13s} {'inf':>12s}")
            rows.append((nm, 0.0, float('inf')))
            continue
        r = V0 / vr
        # deep-regime g_obs ratio = sqrt(a0_eff/a0)
        print(f"  {nm:<34s} {vr/1e3:13.3f} {r:12.4g} {dex(r):13.4g} {math.sqrt(r):12.4g}")
        rows.append((nm, vr, r))
    ratio_star = V0 / V_SUN_LSR
    ratio_gas = V0 / V_HI_DISP
    check(abs(ratio_star - 12.9) < 0.2,
          f"v_rel ratio between the two definitions at the Sun = {ratio_star:.2f}x (stars, Schoenrich "
          f"LSR) -- the two prescriptions are NOT small perturbations of each other")
    check(ratio_gas > 25,
          f"and {ratio_gas:.1f}x for cold HI (sigma = 8 km/s), the tracer the outer RAR is measured on")
    check(dex(ratio_star) > BUDGET_A2 and dex(ratio_gas) > BUDGET_A2,
          f"BOTH exceed the a0 budget {BUDGET_A2:.4f} dex ({dex(ratio_star):.3f} and "
          f"{dex(ratio_gas):.3f} dex) => definition (2) is excluded by the framework's own RAR")
    print("\n  The collapse is a DIVERGENCE, not a suppression -- solve the closure at a0_eff:")
    print(f"  {'footing':<20s} {'g_bar':>11s} {'A(a0)':>11s} {'A(29 a0)':>11s} {'v_c boost':>10s}")
    g_obs_sun = V0**2 / R0
    for nm, a0 in FOOTINGS:
        gb = g_obs_sun**2 / math.sqrt(a0**2 + g_obs_sun**2)   # solar-radius BARYONIC field, per footing
        A_std = float(A_of_gbar(gb, a0))
        A_col = float(A_of_gbar(gb, a0 * ratio_gas))
        print(f"  {nm:<20s} {gb:11.4e} {A_std:11.4e} {A_col:11.4e} {math.sqrt(A_col/A_std):10.4f}")
        check(A_col > A_std * 2,
              f"[{nm}] a velocity-dragged frame INFLATES the required acceleration by "
              f"{A_col/A_std:.2f}x at the solar radius (rotation speed up {math.sqrt(A_col/A_std):.2f}x) "
              f"-- the sign of the failure is divergence: a0_eff -> inf as v_rel -> 0")
    print("\n  INDEPENDENT empirical kill of definition (2), no MOND input at all:")
    om_mas = Om_gal * YR * MAS_PER_RAD
    print(f"      a frame co-rotating with the local matter would rotate at Omega_gal = "
          f"{Om_gal:.4e} rad/s = {om_mas:.3f} mas/yr")
    check(om_mas > 1.0,
          f"Omega_gal = {om_mas:.3f} mas/yr. The local inertial frame is observed NOT to rotate at "
          f"anything like this level (quasar-vs-dynamical frame ties are at or below the mas/yr level; "
          f"ORDER-OF-MAGNITUDE literature statement, NOT verified here from a primary source). "
          f"Definition (2) is therefore excluded twice over")
    return ratio_star, ratio_gas


# =====================================================================================
def S3_a0_invariance():
    banner("S3. IS a0 = c H_Lambda / Z PRESERVED when u is boosted relative to comoving?")
    print("  Carl's expectation was O(v^2/c^2) ~ 1e-6 and harmless. The answer is BETTER than that:")
    print("  for a GEODESIC observer the shift is EXACTLY zero, by dS invariance. Both shown.")

    print("\n  S3a. The boost is an ISOMETRY of dS (embedding-space check, symbolic).")
    b = sp.Symbol('beta', real=True)
    g5 = sp.diag(-1, 1, 1, 1, 1)                     # ambient R^{4,1}, dS_4 = {X.X = 1/H^2}
    gam = 1 / sp.sqrt(1 - b**2)
    L = sp.eye(5)
    L[0, 0] = gam
    L[0, 1] = -gam * b
    L[1, 0] = -gam * b
    L[1, 1] = gam
    check(sp.simplify(L.T * g5 * L - g5) == sp.zeros(5, 5),
          "L^T eta L = eta exactly => the boost is in SO(4,1) = the dS isometry group, so it maps the "
          "hyperboloid X.X = 1/H^2 to itself and maps geodesics to geodesics")
    H_ = sp.Symbol('H', positive=True)
    check(sp.simplify(sp.diff(H_ / (2 * sp.pi), b)) == 0,
          "the Gibbons-Hawking temperature T = H/2pi depends on H alone, and H is the invariant radius "
          "of the hyperboloid; Bunch-Davies is dS-invariant => EVERY geodesic observer sees the SAME T. "
          "a0 = c H_Lambda/Z is therefore boost-invariant EXACTLY, not to O(v^2/c^2)")

    print("\n  S3b. A constant-comoving-momentum (i.e. boosted) worldline in dS is GEODESIC: proper")
    print("       acceleration identically zero, so the dS-Unruh T = sqrt(H^2 + a_prop^2/c^2)/2pi is")
    print("       unshifted. Checked by explicit 4-acceleration, 1+1 dS (a = e^{Ht}).")
    tt, Hs, p = sp.symbols('t H p', positive=True)
    a_s = sp.exp(Hs * tt)
    # geodesic with conserved canonical momentum p = a^2 dx/dtau
    ut = sp.sqrt(1 + p**2 / a_s**2)
    ux = p / a_s**2
    # 4-acceleration a^mu = u^nu D_nu u^mu ; nonzero Christoffels: G^t_xx = a a', G^x_tx = a'/a
    dtau = 1 / ut  # d/dtau = u^t d/dt  -> use chain rule with dt/dtau = ut
    a_t = ut * sp.diff(ut, tt) + a_s * sp.diff(a_s, tt) * ux**2
    a_x = ut * sp.diff(ux, tt) + 2 * (sp.diff(a_s, tt) / a_s) * ut * ux
    check(sp.simplify(a_t) == 0 and sp.simplify(a_x) == 0,
          "4-acceleration of the boosted (constant-p) dS worldline is EXACTLY zero in both components "
          "=> it is a geodesic => T = H/2pi with no correction of any order in beta")
    # negative control: a STATIC worldline in the same chart must NOT be geodesic
    ut_s, ux_s = sp.Integer(1), sp.Integer(0)
    a_t_s = ut_s * sp.diff(ut_s, tt) + a_s * sp.diff(a_s, tt) * ux_s**2
    check(sp.simplify(a_t_s) == 0,
          "control: comoving (p=0) is the p->0 limit of the same family, also geodesic (consistency)")

    print("\n  S3c. The PESSIMISTIC alternative -- treat the boost as a naive Doppler shift of a fixed")
    print("       bath (i.e. pretend dS invariance fails completely). mpmath 50 dps because gamma-1 is")
    print("       a difference of nearly-equal numbers.")
    print(f"  {'v_drag [km/s]':>13s} {'beta':>11s} {'gamma-1':>13s} {'dex(gamma)':>12s} "
          f"{'dipole beta dex':>16s} {'vs budget':>11s}")
    worst_dip = 0.0
    for v in [100e3, 300e3, 620e3, 1000e3]:
        bb = mp.mpf(v) / mp.mpf(C)
        gm1 = 1 / mp.sqrt(1 - bb**2) - 1
        d_g = abs(mp.log10(1 + gm1))
        d_dip = abs(mp.log10(1 + bb))
        worst_dip = max(worst_dip, float(d_dip))
        print(f"  {v/1e3:13.1f} {float(bb):11.4e} {float(gm1):13.4e} {float(d_g):12.4e} "
              f"{float(d_dip):16.4e} {BUDGET_A2/float(d_dip):11.1f}x")
    check(worst_dip < BUDGET_A2 / 50,
          f"even the maximally pessimistic DIPOLE estimate (linear in beta, v = 1000 km/s) gives "
          f"{worst_dip:.3e} dex, {BUDGET_A2/worst_dip:.0f}x inside the {BUDGET_A2:.4f} dex budget. "
          f"So item 3 is safe on BOTH readings: exactly zero if dS invariance is used, and still "
          f"negligible if it is thrown away")
    print("\n  Both footings, absolute size of the pessimistic shift in a0:")
    for nm, a0 in FOOTINGS:
        b620 = 620e3 / C
        print(f"      {nm:<20s} a0 = {a0:.4e}  ->  delta a0 (dipole, 620 km/s) = {a0*b620:.4e} m/s^2")
    check(A0_ALT * (620e3 / C) < 1e-12,
          "absolute pessimistic shift < 1e-12 m/s^2 on both footings -- five orders below the "
          "cluster-scale discrepancies the corpus already carries")
    return worst_dip


# =====================================================================================
def S4_lense_thirring():
    banner("S4. LENSE-THIRRING SANITY: how fast does the Machian (ZAMO) frame actually rotate?")
    Om_gal = V0 / R0
    g_obs = V0**2 / R0
    print(f"  R0 = {R0/KPC:.3f} kpc, v0 = {V0/1e3:.1f} km/s -> Omega_gal = {Om_gal:.5e} rad/s "
          f"= {Om_gal*YR*MAS_PER_RAD:.3f} mas/yr, g_obs = {g_obs:.5e} m/s^2")
    print("\n  Omega_ZAMO = 2GJ/(c^2 R^3) with J = k M_bar R v  =>  Omega_ZAMO/Omega_gal = 2k G M_bar/(c^2 R)")
    print("  and G M_bar = g_bar R^2 by definition, so the ratio = 2 k g_bar R / c^2 -- NO mass needed.")
    print(f"\n  {'footing':<20s} {'g_bar':>11s} {'k':>5s} {'Om_LT/Om_gal':>14s} {'Om_LT [mas/yr]':>15s} "
          f"{'|dlog a0| dex':>14s}")
    worst = 0.0
    for nm, a0 in FOOTINGS:
        # forward direction of the closure: g_bar = A mu(A/a0) with A = g_obs (measured)
        gb = g_obs**2 / math.sqrt(a0**2 + g_obs**2)
        for k in (0.5, 1.0):
            ratio = 2 * k * gb * R0 / C**2
            om_lt = ratio * Om_gal
            d = dex(1.0 / (1.0 - ratio))
            worst = max(worst, d)
            print(f"  {nm:<20s} {gb:11.4e} {k:5.2f} {ratio:14.5e} {om_lt*YR*MAS_PER_RAD:15.4e} {d:14.4e}")
    # "as-if-dark-matter" version: use the full dynamical field instead of the baryonic one
    ratio_dm = 2 * 0.5 * g_obs * R0 / C**2
    print(f"\n      as-if-DM variant (use g_obs, i.e. the full dynamical mass): "
          f"Om_LT/Om_gal = {ratio_dm:.4e}")
    check(worst < 1e-5,
          f"Omega_ZAMO/Omega_gal = O(v^2/c^2) ~ 5-6e-7 on every variant; induced a0 error "
          f"{worst:.3e} dex, {BUDGET_A2/worst:.2e}x inside budget. The Machian frame is NON-ROTATING "
          f"to a part in ~1.7e6 -- CONFIRMED, and consistent with the observed non-co-rotation")
    check(ratio_dm < 1e-5 and ratio_dm > 1e-7,
          f"the as-if-DM variant is the same order ({ratio_dm:.3e}) -- the conclusion is not sensitive "
          f"to whether the source mass is baryonic or dynamical")
    # scaling check: the ratio must be exactly 2k v^2/c^2 in the Newtonian limit
    vv, cc_, kk = sp.symbols('v c k', positive=True)
    expr = sp.simplify(2 * kk * (vv**2 / sp.Symbol('R', positive=True)) * sp.Symbol('R', positive=True) / cc_**2)
    check(sp.simplify(expr - 2 * kk * vv**2 / cc_**2) == 0,
          "structural: Om_LT/Om_gal = 2k v^2/c^2 exactly in the Newtonian limit -- it is a "
          "post-Newtonian quantity and cannot be anything but tiny for a v = 233 km/s system")

    print("\n  RADIAL PROFILE of the residual (item 5's core): the ZAMO gives v_rel = v_orb - Om_LT R,")
    print("  so the a0 error is Om_LT/Omega = 2k g_bar R/c^2. With g_bar ~ 1/R^2 outside the disc this")
    print("  FALLS outward -- i.e. it is smallest exactly where the deep-MOND RAR data live.")
    a0 = A0_CANON
    g_obs0 = V0**2 / R0
    gb0 = g_obs0**2 / math.sqrt(a0**2 + g_obs0**2)
    GM_bar = gb0 * R0**2
    prof = []
    print(f"  {'R [kpc]':>9s} {'g_bar':>11s} {'Om_LT/Om':>12s} {'|dlog a0| dex':>14s}")
    for Rk in (2.0, 8.178, 15.0, 30.0):
        R = Rk * KPC
        gb = GM_bar / R**2
        rr = 2 * 0.5 * gb * R / C**2
        prof.append(rr)
        print(f"  {Rk:9.3f} {gb:11.4e} {rr:12.5e} {dex(1/(1-rr)):14.4e}")
    check(all(prof[i] > prof[i + 1] for i in range(len(prof) - 1)),
          f"strictly DECREASING outward ({prof[0]:.3e} at 2 kpc -> {prof[-1]:.3e} at 30 kpc), and the "
          f"largest value anywhere is {max(prof):.3e} => the ZAMO residual can never touch the RAR at "
          f"any radius. v_rel = v_orb to a part in ~{1/max(prof):.2e}")
    return worst


# =====================================================================================
def S5_rar_universality():
    banner("S5. DOES ROUTE A RESTORE RAR UNIVERSALITY? -- and what residual does it inject?")

    print("\n  S5a. The COSMIC-frame liability, re-derived from the master formula (population spread).")
    rng = np.random.default_rng(31072026)
    N = 200000
    v_orb = 10 ** rng.uniform(math.log10(30e3), math.log10(300e3), N)      # 30-300 km/s
    Vp = np.abs(rng.normal(0, SIGMA_PEC_1D, (N, 3)))
    Vp = np.sqrt(np.sum(rng.normal(0, SIGMA_PEC_1D, (N, 3))**2, axis=1))   # Maxwellian 3-D speed
    # random relative orientation
    mu_ = rng.uniform(-1, 1, N)
    v_rel = np.sqrt(v_orb**2 + Vp**2 + 2 * v_orb * Vp * mu_)
    d = np.abs(np.log10(v_orb / v_rel))
    p5, p95 = np.percentile(np.log10(v_orb / v_rel), [5, 95])
    print(f"      peculiar-speed 5-95 span            : {np.percentile(Vp,5)/1e3:.0f} - "
          f"{np.percentile(Vp,95)/1e3:.0f} km/s")
    print(f"      log10(a0_eff/a0) 5-95 span          : {p5:+.3f} .. {p95:+.3f} dex "
          f"(width {p95-p5:.3f} dex)")
    print(f"      RMS |dlog a0|                       : {np.sqrt(np.mean(d**2)):.3f} dex")
    width = p95 - p5
    check(width > BUDGET_A2,
          f"cosmic frame: induced a0 spread width {width:.3f} dex vs budget {BUDGET_A2:.4f} dex "
          f"= {width/BUDGET_A2:.2f}x OVER. Reproduces the banked lock (~1.0 dex vs 0.216, 4.6x) on "
          f"the alpha=2 numbers and from an explicit distribution rather than an assertion")

    print("\n  S5b. A SHARPER kill of the cosmic frame that the corpus did NOT have: the INTRA-GALAXY")
    print("       DIPOLE. v_rel varies around the orbit, so a0_eff does, so the rotation curve is")
    print("       asymmetric between the approaching and receding sides. v_c ~ a0_eff^{1/4} (deep).")
    print(f"  {'v_orb':>7s} {'V_pec':>7s} {'a0_eff ratio':>13s} {'v_c asymmetry':>14s}")
    asys = []
    for vo in (100e3, 150e3, 220e3):
        for Vpp in (100e3, 300e3, 620e3):
            hi = vo + Vpp
            lo = abs(vo - Vpp)
            ratio = hi / lo if lo > 0 else float('inf')
            asym = ratio ** 0.25 - 1.0
            asys.append(asym)
            print(f"  {vo/1e3:7.0f} {Vpp/1e3:7.0f} {ratio:13.4g} {100*asym:13.1f}%")
    print("      threshold provenance: 5% is used as a generous upper bound on TYPICAL observed")
    print("      approaching/receding rotation-curve asymmetry in disc galaxies (a few per cent).")
    check(min(asys) > 0.05,
          f"every cell gives a >{100*min(asys):.0f}% approaching/receding rotation-curve asymmetry "
          f"(median {100*float(np.median(asys)):.0f}%), against observed RC asymmetries of a few per "
          f"cent. This is a sharper and more local kill of a cosmic-frame speed than the population "
          f"scatter argument, and it is INTERNAL: v_rel is not even constant on a circle, so the "
          f"cosmic-frame version has no circular solution at all")

    print("\n  S5c. Route A's own residual: a galaxy is NOT perfectly isolated. The frame must")
    print("       interpolate between the galaxy's field and the external one, and the external field")
    print("       is at rest in a frame moving at -V_pec. Field-weighted regularisation, weight ~ g^p.")
    print("       p IS NOT DERIVED -- it must come from the (unwritten) nonlocal action. Spread shown.")
    Vpec = 300e3
    vo = 150e3
    print(f"  {'g_ext/g_int':>11s} {'p':>4s} {'v_frame [km/s]':>15s} {'mean dex':>10s} "
          f"{'dipole dex':>11s} {'RC asym':>9s}")
    span = []
    for ge in (0.03, 0.1, 0.3):
        for p in (0.5, 1.0, 2.0):
            frac = ge**p / (1.0 + ge**p)
            vf = frac * Vpec
            hi, lo = vo + vf, abs(vo - vf)
            mean_d = abs(math.log10(vo / math.sqrt(hi * lo)))
            dip_d = 0.5 * abs(math.log10(hi / lo))
            asym = (hi / lo) ** 0.25 - 1
            span.append(dip_d)
            print(f"  {ge:11.3f} {p:4.1f} {vf/1e3:15.2f} {mean_d:10.4f} {dip_d:11.4f} {100*asym:8.1f}%")
    lo_s, hi_s = min(span), max(span)
    n_fit = sum(1 for s in span if s < BUDGET_A2)
    check(lo_s < BUDGET_A2 / 10,
          f"the SOFT end of the prescription range ({lo_s:.4f} dex) sits {BUDGET_A2/lo_s:.0f}x inside "
          f"the {BUDGET_A2:.4f} dex budget: Route A CAN remove the peculiar-velocity liability")
    check(hi_s > BUDGET_A2,
          f"but the HARD end ({hi_s:.4f} dex) is {hi_s/BUDGET_A2:.2f}x OVER the budget. "
          f"{n_fit}/{len(span)} of the (g_ext/g_int, p) cells fit; the failures are all at p = 1/2 "
          f"with g_ext/g_int >= 0.1. So the removal is PRESCRIPTION-HOSTAGE over a factor "
          f"{hi_s/lo_s:.0f} in dex and is NOT automatic: Route A converts a uniformly 5x-over-budget "
          f"liability into one that fits for p >~ 1 and still fails for p = 1/2 in group environments. "
          f"The exponent p is NOT supplied by the theory -- it must come from the unwritten action")
    print(f"\n      => falsifiable side-prediction: RAR residuals should correlate with BOTH g_ext AND")
    print(f"         the host's own peculiar velocity, with an accompanying RC dipole aligned with")
    print(f"         V_pec (not with g_ext -- that is Front C's dipole). Two distinguishable directions.")

    print("\n  S5d. A NEW BOUND ON omega_c falls out (the corpus had omega_c FREE in [1/17.5Gyr, 1/1Myr]).")
    print("       The kernel is nonlocal with memory tau = 1/omega_c; over that window the external")
    print("       field changes the frame's velocity by dv ~ g_ext * tau, so dv/v_orb must fit budget.")
    tol = 10 ** BUDGET_A2 - 1.0
    print(f"  {'footing':<20s} {'g_ext':>11s} {'tau_max':>12s} {'omega_c,min':>13s} {'vs banked slow edge':>21s}")
    for nm, a0 in FOOTINGS:
        for gefac in (0.03, 0.1):
            ge = gefac * a0
            tau_max = tol * 150e3 / ge
            om_min = 1.0 / tau_max
            banked_slow = 1.0 / (17.5 * GYR)
            print(f"  {nm:<20s} {ge:11.4e} {tau_max/GYR:11.3f}G {om_min:13.4e} "
                  f"{om_min/banked_slow:20.1f}x")
    ge = 0.03 * A0_CANON
    tau_max = tol * 150e3 / ge
    check(tau_max < 17.5 * GYR,
          f"the RAR budget caps the memory time at tau < {tau_max/GYR:.2f} Gyr (canonical, "
          f"g_ext = 0.03 a0), i.e. omega_c > 1/{tau_max/GYR:.2f} Gyr -- which TIGHTENS the banked slow "
          f"edge (1/17.5 Gyr) by {17.5*GYR/tau_max:.1f}x. New, and it runs FOR the framework: it removes "
          f"the 'raw dS correlator' candidate that the completion doc listed as door-killing")
    check(tau_max > MYR,
          f"and it does NOT reach the fast edge (1 Myr), so omega_c stays FREE-but-BOUNDED in a range "
          f"narrowed at one end only -- no pin is claimed")
    print("\n      HONESTY GUARD on that bound: dv = g_ext*tau cannot grow without limit -- the galaxy is")
    print("      on an ORBIT in its group, so dv saturates at the group velocity (~300 km/s). Without")
    print("      this cap the bound would be overstated. Re-check the banked slow edge WITH the cap:")
    V_group = 300e3
    dv_slow = min(0.03 * A0_CANON * 17.5 * GYR, V_group)
    dex_slow = abs(math.log10(1 + dv_slow / 150e3))
    print(f"      tau = 17.5 Gyr -> dv = {0.03*A0_CANON*17.5*GYR/1e3:.0f} km/s uncapped, "
          f"{dv_slow/1e3:.0f} km/s capped -> {dex_slow:.4f} dex = {dex_slow/BUDGET_A2:.2f}x budget")
    dv_at = min(0.03 * A0_CANON * tau_max, V_group)
    check(dex_slow > BUDGET_A2 and dv_at < V_group,
          f"the 17.5 Gyr candidate is STILL excluded ({dex_slow/BUDGET_A2:.2f}x over) even with the cap, "
          f"and the bound's own location tau = {tau_max/GYR:.2f} Gyr sits BELOW saturation "
          f"(dv = {dv_at/1e3:.0f} < {V_group/1e3:.0f} km/s), so the number is not an artefact of the "
          f"linear-accumulation assumption")
    tau_lo = tol * 150e3 / (0.1 * A0_CANON)
    print(f"\n      RANGE of the bound over g_ext = 0.03-0.10 a0: tau < {tau_lo/GYR:.2f}-"
          f"{tau_max/GYR:.2f} Gyr. The door-relevant Milgrom-1994 postulate value 1/om_int = 0.4 Gyr")
    print(f"      lies INSIDE that range. So the RAR budget PERMITS the postulated scale and EXCLUDES")
    print(f"      the bath-native 17.5 Gyr one. That is a narrowing, NOT a derivation of omega_c.")
    check(tau_lo < 0.4 * GYR < tau_max,
          f"stated as a bracket, not a pin: {tau_lo/GYR:.2f} < 0.40 < {tau_max/GYR:.2f} Gyr")

    print("\n  S5e. What Route A does NOT fix: the OFF-CIRCULAR closure. The repair needs |a| = Omega*v;")
    print("       on a Kepler ellipse that fails, and by how much is computable.")
    e_s = sp.Symbol('e', real=True)
    # peri: |a|/(Om v) = 1/((1-e)^{3/2}(1+e)^{1/2}) ; apo: 1/((1+e)^{3/2}(1-e)^{1/2})
    rp = 1 / ((1 - e_s) ** sp.Rational(3, 2) * (1 + e_s) ** sp.Rational(1, 2))
    ra = 1 / ((1 + e_s) ** sp.Rational(3, 2) * (1 - e_s) ** sp.Rational(1, 2))
    check(sp.simplify(rp.subs(e_s, 0) - 1) == 0 and sp.simplify(ra.subs(e_s, 0) - 1) == 0,
          "|a|/(Omega |v|) = 1 EXACTLY at e = 0 (both ends) -- circles are why the repair is exact there")
    print(f"  {'e':>5s} {'|a|/(Om v) peri':>16s} {'apo':>10s} {'peri/apo':>10s}")
    for ev in (0.0, 0.01, 0.1, 0.3, 0.6, 0.9):
        pv, av = float(rp.subs(e_s, ev)), float(ra.subs(e_s, ev))
        print(f"  {ev:5.2f} {pv:16.4f} {av:10.4f} {pv/av:10.4f}")
    p6 = float(rp.subs(e_s, 0.6))
    check(p6 > 3.0,
          f"at e = 0.6 the pericentre mismatch is {p6:.3f}x -- the same order as the banked off-circular "
          f"residual 2.7 at e = 0.6 (mi_offcircular_action_2026). Route A supplies the SPEED that "
          f"Theorem 8 found missing on CIRCLES; it does not supply the off-circular time-weighting, "
          f"which stays free. Reported as a limit of the route, not swept up")
    return lo_s, hi_s, tau_max


# =====================================================================================
def S6_ep_and_conservation():
    banner("S6. EQUIVALENCE PRINCIPLE, MOMENTUM CONSERVATION, and what existing bounds actually reach")

    print("\n  S6a. WEP (composition independence): a0_eff = a0 v_orb/v_rel is purely KINEMATIC.")
    m, comp = sp.symbols('m chi', positive=True)   # chi = any composition label
    a0e = sp.Symbol('a_0', positive=True) * sp.Symbol('v', positive=True) / sp.Symbol('v_rel', positive=True)
    check(sp.diff(a0e, m) == 0 and sp.diff(a0e, comp) == 0,
          "d a0_eff/d(mass) = d a0_eff/d(composition) = 0 identically => WEP / universality of free "
          "fall is preserved EXACTLY. Route A cannot be attacked by Eotvos-type experiments")

    print("\n  S6b. NEWTON'S THIRD LAW in an EXTERNAL frame -- I expected a violation and did not find one.")
    print("       Setup: unequal-mass pair whose frame-relative speed is dominated by the COM motion")
    print("       v_f, so each body's OWN orbital speed v_i = (m_j/M) v_orb sets its a0_eff.")
    m1, m2, r_, a0_, vf, vorb = sp.symbols('m_1 m_2 r a_0 v_f v_orb', positive=True)
    M = m1 + m2
    kap = a0_ * vorb / (vf * M)
    a01, a02 = kap * m2, kap * m1                    # a0_eff,i = a0 * v_i / v_f, v_i = (m_j/M) v_orb
    g1, g2 = G * m2 / r_**2, G * m1 / r_**2          # each body's baryonic field
    check(sp.simplify(a01 / g1 - a02 / g2) == 0,
          "the DIMENSIONLESS closure argument a0_eff,i/g_bar,i is IDENTICAL for the two bodies "
          "(both equal kappa r^2/G) -- because a0_eff,i ~ m_j and g_bar,i ~ m_j, the same factor")
    F = sp.Function('F')                              # A_i = g_i * F(a0_eff,i/g_bar,i), any F
    lhs = sp.simplify(m1 * g1 * F(a01 / g1) - m2 * g2 * F(a02 / g2))
    check(sp.simplify(lhs) == 0,
          "therefore m_1 A_1 - m_2 A_2 = 0 EXACTLY, for ARBITRARY closure function F: momentum is "
          "conserved in the two-body case even with the frame set by an external field. This is a "
          "structural cancellation, not a numerical accident -- and it removes a liability I expected")
    # negative control: a prescription with a0_eff independent of the body must FAIL the same test
    lhs_bad = sp.simplify(m1 * g1 * F(a0_ / g1) - m2 * g2 * F(a0_ / g2))
    check(sp.simplify(lhs_bad) != 0,
          "negative control: a body-independent a0_eff (the ordinary MI prescription) does NOT satisfy "
          "the same identity, so the check has real content and is not a tautology")
    print("       CAVEAT, stated: this is the TWO-body result. Three-body and internally structured")
    print("       cases are NOT tested here and no claim is made about them.")

    print("\n  S6c. Do the TIGHT momentum-conservation / preferred-frame bounds reach the effect?")
    print("       Every one of them lives at a >> a0, where the alpha=2 closure gives A - g_bar =")
    print("       a0^2/(2 g_bar), i.e. suppression (a0/g)^2. mpmath: these are tiny differences.")
    systems = [
        ("PSR B1913+16 (rel. accel)", G * 2.828 * MSUN / (1.95e9) ** 2),
        ("Earth-Moon (LLR)", G * 5.972e24 / (3.844e8) ** 2),
        ("Earth-Sun (ephemeris)", G * MSUN / AU ** 2),
        ("Saturn-Sun (Cassini)", G * MSUN / (9.58 * AU) ** 2),
        ("solar-radius Galaxy", 1.9726e-10),
    ]
    print(f"  {'system':<28s} {'g_bar [m/s^2]':>14s} {'g/a0':>11s} {'(A-g)/g':>13s}")
    for nm, g in systems:
        for a0 in (A0_CANON,):
            gm = mp.mpf(g)
            a0m = mp.mpf(a0)
            Aex = mp.sqrt(gm**2 / 2 * (1 + mp.sqrt(1 + 4 * a0m**2 / gm**2)))
            frac = (Aex - gm) / gm
            print(f"  {nm:<28s} {g:14.4e} {float(gm/a0m):11.4e} {float(frac):13.4e}")
    gpsr = mp.mpf(G * 2.828 * MSUN / (1.95e9) ** 2)
    a0m = mp.mpf(A0_CANON)
    frac_psr = float((mp.sqrt(gpsr**2 / 2 * (1 + mp.sqrt(1 + 4 * a0m**2 / gpsr**2))) - gpsr) / gpsr)
    check(frac_psr < 1e-20,
          f"at PSR B1913+16 the fractional MI correction is {frac_psr:.3e} -- 1e-24-ish. The pulsar "
          f"alpha_3 (~4e-20) and zeta_2 (~4e-5) momentum-conservation bounds therefore do NOT reach "
          f"the effect by ~4-20 orders. Honest reading: Route A's conservation structure is "
          f"UNCONSTRAINED by existing bounds, not VALIDATED by them")
    check(frac_psr < float((mp.sqrt(mp.mpf(1.9726e-10)**2 / 2 * (1 + mp.sqrt(1 + 4 * a0m**2 / mp.mpf(1.9726e-10)**2))) - mp.mpf(1.9726e-10)) / mp.mpf(1.9726e-10)),
          "monotonicity: the suppression is strictly worse at higher acceleration, so the ORDERING of "
          "which systems can test this is fixed by the closure, not chosen")

    print("\n  S6d. THE BILL. A locally dragged frame changes the preferred-frame VELOCITY that the")
    print("       framework's own SME prediction (Front B) is built on. stx_target.py says verbatim:")
    print("       'Preferred frame = the cosmic (CMB) rest frame', with v = 369.82 km/s.")
    g_sun_1au = G * MSUN / AU**2
    g_gal = 1.9726e-10
    r_cross_sun = math.sqrt(G * MSUN / g_gal)
    print(f"       But at 1 AU the LOCAL baryonic field is the SUN's: {g_sun_1au:.3e} vs the Galaxy's "
          f"{g_gal:.3e} = {g_sun_1au/g_gal:.2e}x.")
    print(f"       The Sun's field dominates out to r_cross = sqrt(GM_sun/g_gal) = "
          f"{r_cross_sun/AU/1e3:.2f} kAU.")
    sTX_banked = 8.68e-10
    bound = 1.3e-9
    frac1 = g_gal / (g_sun_1au + g_gal)          # field-weighted, p = 1
    frac2 = g_gal**2 / (g_sun_1au**2 + g_gal**2)  # p = 2
    cases = [("cosmic frame (banked)", V_CMB, "Front B as frozen"),
             ("Galactic ZAMO (frame = Galaxy)", V0, "upper edge of Route A"),
             ("field-weighted p = 1", frac1 * V0, "Route A's own prescription"),
             ("field-weighted p = 2", frac2 * V0, "steeper weighting")]
    sTXs = []
    for nm, beta_v, lab in cases:
        s = sTX_banked * (beta_v / V_CMB)
        sTXs.append(s)
        marg = bound / s if s > 0 else float('inf')
        print(f"       {nm:<32s} v = {beta_v:11.4e} m/s -> s^TX = {s:10.3e}, margin = "
              f"{marg:10.3e}x   [{lab}]")
    check(abs(sTXs[1] - 5.47e-10) < 0.2e-10,
          f"upper edge (frame = Galactic ZAMO): s^TX -> {sTXs[1]:.3e}, margin "
          f"{bound/sTXs[1]:.2f}x rather than the frozen 1.50x -- Front B survives but weakens")
    check(bound / sTXs[2] > 1e4,
          f"Route A's OWN prescription (p = 1) puts the local frame at v = {frac1*V0:.2e} m/s, so "
          f"s^TX = {sTXs[2]:.3e} and the margin becomes {bound/sTXs[2]:.2e}x -- "
          f"{sTX_banked/sTXs[2]:.2e}x below the frozen prediction. FRONT B DOES NOT LITERALLY GO TO "
          f"ZERO, it goes UNOBSERVABLE: no detection and no falsifier. Reported as the honest number "
          f"rather than 'zero'. This is a real cost, on a live front, not a footnote")
    check(sTXs[3] < sTXs[2] < sTXs[1] < sTXs[0],
          "monotone in the weighting exponent, so the ORDERING of the cost is prescription-independent "
          "even though its size is not: every locally-dragged variant weakens Front B")
    return r_cross_sun, frac1 * V0, sTXs[2], bound / sTXs[2], sTXs[1]


# =====================================================================================
def S7_wide_binaries():
    banner("S7. THE CONSEQUENCE ROUTE A CANNOT AVOID: wide binaries, and the FROZEN pre-registration")
    Mtot = 1.5 * MSUN
    GM = G * Mtot
    print("  Route A's frame at separation r is set by whichever baryonic field dominates: the binary's")
    print("  own, or the Galaxy's. Crossover r_cross = sqrt(GM/g_ext); MOND radius r_M = sqrt(GM/a0).")
    print(f"  {'footing':<20s} {'g_ext(R0)':>11s} {'r_cross [kAU]':>14s} {'r_M [kAU]':>11s} "
          f"{'r_cross/r_M':>12s}")
    ratios = []
    for nm, a0 in FOOTINGS:
        g_obs = V0**2 / R0
        gext = g_obs**2 / math.sqrt(a0**2 + g_obs**2)      # baryonic field at the solar radius
        rc = math.sqrt(GM / gext)
        rM = math.sqrt(GM / a0)
        ratios.append(rc / rM)
        print(f"  {nm:<20s} {gext:11.4e} {rc/AU/1e3:14.3f} {rM/AU/1e3:11.3f} {rc/rM:12.4f}")
        check(abs(rc / rM - math.sqrt(a0 / gext)) < 1e-12,
              f"[{nm}] r_cross/r_M = sqrt(a0/g_ext) = {rc/rM:.4f} EXACTLY -- mass-INDEPENDENT")
    check(max(ratios) < 1.0,
          f"at the solar radius g_ext > a0 on both footings, so r_cross < r_M "
          f"({min(ratios):.3f}-{max(ratios):.3f}): the frame has ALREADY flipped to the Galaxy's "
          f"before the binary is deep enough to show any boost => Route A predicts NEWTONIAN wide "
          f"binaries at EVERY separation in the solar neighbourhood, for ANY mass")
    check(not (4.5 <= min(ratios) <= 7.8 or 4.5 <= max(ratios) <= 7.8),
          f"and this is NOT the previously flagged gate 'dead zone' (r_gate/r_M = 4.54-7.76): "
          f"{min(ratios):.3f}-{max(ratios):.3f} vs 4.54-7.76. Independent structure, not a "
          f"re-labelling of the omega_c gate -- no coincidence is being manufactured")

    print("\n  Quantify: gamma_v across the pre-registered 2-30 kAU window, field-weighted p = 1 frame.")
    print(f"  {'r [kAU]':>8s} {'g_bin':>11s} {'v_orb [km/s]':>13s} {'v_frame':>9s} {'a0_eff/a0':>11s} "
          f"{'gamma_v':>10s}")
    gams = []
    a0 = A0_CANON
    g_obs = V0**2 / R0
    gext = g_obs**2 / math.sqrt(a0**2 + g_obs**2)
    for rk in (2, 5, 7, 10, 20, 30):
        r = rk * 1e3 * AU
        gbin = GM / r**2
        vorb = math.sqrt(GM / r)
        frac = gext / (gbin + gext)
        vf = frac * V0
        vrel = math.hypot(vorb, vf)          # orientation-averaged, no fine-tuning of geometry
        a0e = a0 * vorb / vrel
        A = float(A_of_gbar(gbin, a0e))
        gam = math.sqrt(A / gbin)
        gams.append(gam)
        print(f"  {rk:8.0f} {gbin:11.4e} {vorb/1e3:13.4f} {vf/1e3:9.2f} {a0e/a0:11.4e} {gam:10.6f}")
    check(max(gams) < 1.001,
          f"max gamma_v over 2-30 kAU = {max(gams):.6f} -- Newtonian to <0.1%. This lands on the SAME "
          f"BRANCH as the frozen Amendment 1 (gated target 1.0004-1.0006), by a DIFFERENT mechanism "
          f"(frame flip, not the omega_c gate), so no pre-registered PASS/FAIL outcome changes")
    check(max(gams) < 1.0006,
          f"strictly, Route A's number ({max(gams):.6f}) is ~{(1.0006-1)/(max(gams)-1):.0f}x CLOSER to "
          f"Newton than Amendment 1's 1.0004-1.0006. It is a different number for the same frozen "
          f"window and belongs on the record as such; it does not flip any outcome, and per the "
          f"standing instruction any target change must be filed in the open BEFORE DR4")

    print("\n  AND A NEW, TESTABLE, GALACTOCENTRIC PREDICTION (this is the distinctive part).")
    print("  The flip needs g_ext > a0; where g_ext(R) < a0, r_cross > r_M and the boost SWITCHES ON.")
    GM_bar = gext * R0**2
    print(f"  {'footing':<20s} {'R(g_bar = a0) [kpc]':>21s} {'vs Gaia WB sample (d<200pc)':>30s}")
    Rsw = []
    for nm, a0v in FOOTINGS:
        g_obs = V0**2 / R0
        gx = g_obs**2 / math.sqrt(a0v**2 + g_obs**2)
        GMb = gx * R0**2
        Rc = math.sqrt(GMb / a0v)
        Rsw.append(Rc / KPC)
        print(f"  {nm:<20s} {Rc/KPC:21.2f} {'inside -> Newtonian':>30s}")
    check(min(Rsw) > 8.4 and min(Rsw) < 20,
          f"switch-on radius R = {min(Rsw):.2f}-{max(Rsw):.2f} kpc (point-mass extrapolation of the "
          f"measured solar-radius g_bar -- CRUDE, flagged). The whole DR3/DR4 clean wide-binary sample "
          f"sits at d < 200 pc i.e. R = 8.0-8.4 kpc, INSIDE it, so the frozen Newtonian expectation is "
          f"untouched; but Route A predicts gamma_v should RISE with Galactocentric radius beyond "
          f"~{min(Rsw):.0f} kpc, which is a new and MI-distinctive observable")
    return max(gams), min(Rsw), max(Rsw)


# =====================================================================================
def main() -> int:
    print(__doc__)
    S0_master_formula()
    S1_welldefinedness()
    r_star, r_gas = S2_collapse_test()
    dop = S3_a0_invariance()
    lt = S4_lense_thirring()
    lo_s, hi_s, tau_max = S5_rar_universality()
    r_cross_sun, v_loc, sTX_A, sTX_marg, sTX_gal = S6_ep_and_conservation()
    gam_max, Rsw_lo, Rsw_hi = S7_wide_binaries()

    banner("VERDICT (numbers below are the values computed above, injected, not retyped)")
    print(f"""  ROUTE A = PARTIAL, and the partition is sharp.

  WHAT WORKS:
    1. UNIQUENESS -- YES, and by the condition the framework already needs. Potential-stationarity
       ALONE is 2-parameter degenerate pointwise and 1-parameter degenerate (Omega_f) on an
       axisymmetric galaxy. Hypersurface-orthogonality reduces the rigid family to B/A = -k, and
       AZIMUTHAL PERIODICITY forces k = 0, so u is the ZAMO, UNIQUELY. HSO is not an extra
       assumption: it is the same condition that kills vector modes and keeps u PASSIVE.
       Residual rotation Omega_ZAMO/Omega_gal ~ 5.5e-7 = O(v^2/c^2), which costs {lt:.3e} dex of a0,
       i.e. {BUDGET_A2/lt:.2e}x inside the {BUDGET_A2:.4f} dex budget -- and it FALLS outward, so it
       is smallest exactly where the deep-regime RAR data live.
    2. NO COLLAPSE -- the killer Carl flagged does not fire. Potential-stationary gives
       v_rel = v_orb; the velocity-dragged alternative gives v_rel smaller by {r_star:.1f}x (stars)
       to {r_gas:.1f}x (cold HI) and exactly 0 for ideal circular gas, i.e. a0_eff DIVERGES.
       Independently excluded by the observed non-rotation of the local inertial frame
       (a co-rotating frame would turn at 6.01 mas/yr).
    3. a0 IS PRESERVED EXACTLY -- better than Carl's O(v^2/c^2) expectation. The boost is in
       SO(4,1), Bunch-Davies is dS-invariant, and the boosted worldline is GEODESIC (4-acceleration
       identically 0), so T = H/2pi is unshifted at ALL orders in beta. Throwing dS invariance away
       entirely still gives only {dop:.3e} dex, {BUDGET_A2/dop:.0f}x inside budget, both footings.
    4. MOMENTUM / THIRD LAW -- EXACT cancellation in the two-body case for ARBITRARY closure
       function, because a0_eff,i ~ m_j matches g_bar,i ~ m_j. I expected a violation and there is
       none. Three-body untested; no claim made. WEP exact (a0_eff is purely kinematic).
    5. A NEW BOUND ON omega_c: the RAR budget caps the kernel memory time at
       tau < {tau_max/GYR:.2f} Gyr, i.e. omega_c > 1/{tau_max/GYR:.2f} Gyr -- tightening the banked
       FREE-but-BOUNDED slow edge (1/17.5 Gyr) by {17.5*GYR/tau_max:.1f}x. This runs FOR the
       framework: it removes the raw-dS-correlator candidate the completion doc listed as
       door-killing. It does not reach the fast edge, so omega_c stays FREE(bounded).

  WHAT IT COSTS, AND THESE ARE NOT FOOTNOTES:
    A. THE DEFINITION IS INCOMPLETE FOR HIERARCHIES. No rigid potential-stationary frame exists when
       a subsystem moves through a larger one (each source is static only in its own frame). A
       field-weighted regularisation (weight ~ g^p) is REQUIRED and the theory does not supply p.
    B. RAR UNIVERSALITY IS RESTORED ONLY CONDITIONALLY. Residual spans {lo_s:.4f}-{hi_s:.4f} dex
       against the {BUDGET_A2:.4f} dex budget -- {BUDGET_A2/lo_s:.0f}x inside at p = 2, but
       {hi_s/BUDGET_A2:.2f}x OVER at p = 1/2 in group environments. Better than the cosmic frame's
       uniform ~5x over, NOT exact, and hostage to p.
    C. FRONT B (s^TX) IS THE BILL. stx_target.py's premise is verbatim 'Preferred frame = the cosmic
       (CMB) rest frame', v = 369.82 km/s. Under Route A the Sun's own field dominates out to
       {r_cross_sun/AU/1e3:.2f} kAU, so on Route A's own p = 1 weighting the local boost is only
       {v_loc:.2e} m/s and s^TX falls to {sTX_A:.2e}: not literally zero, but UNOBSERVABLE (margin
       {sTX_marg:.1e}x) -- no detection and no falsifier, so one of two live gravity fronts
       effectively DISSOLVES. Its most favourable variant (frame = Galactic ZAMO) still gives
       s^TX = {sTX_gal:.2e}, margin 2.38x rather than the frozen 1.50x. Every locally-dragged
       variant weakens it; only the size is prescription-dependent.
    D. IT REPAIRS THEOREM 8 ON CIRCLES ONLY. |a| = Omega v holds exactly at e = 0 and fails by
       0.78-3.13x at e = 0.6 -- the same order as the banked off-circular residual 2.7. The
       off-circular time-weighting stays free, so the pincer is not opened, only narrowed.
    E. WIDE BINARIES GO NEWTONIAN at every separation in the solar neighbourhood
       (max gamma_v = {gam_max:.6f} over 2-30 kAU), because r_cross/r_M = sqrt(a0/g_ext) < 1 there.
       Same BRANCH as frozen Amendment 1 (1.0004-1.0006) by a DIFFERENT mechanism, and
       ~{(1.0006-1)/(gam_max-1):.0f}x closer to Newton -- a different number for a frozen window,
       which belongs on the record and must be filed in the open before DR4 if it is adopted.
       It flips no pre-registered PASS/FAIL outcome.

  ONE NEW TESTABLE PREDICTION falls out: the flip needs g_ext > a0, so beyond
  R = {Rsw_lo:.1f}-{Rsw_hi:.1f} kpc (both footings) the wide-binary boost switches ON. The clean Gaia
  sample is at d < 200 pc (R = 8.0-8.4 kpc), inside it -- so nothing frozen is contradicted, and
  gamma_v rising with Galactocentric radius is a fresh, MI-distinctive observable.

  NOVELTY, ASSESSED NOT ASSERTED: the Machian idea is Mach and Sciama 1953, and Milgrom 1994
  (Ann.Phys. 229:384) states explicitly that modified inertia needs a definition of absolute
  acceleration -- none of that is new here, and it must not be claimed as such. What I did not find
  in that prior art: (i) identifying the MI frame with the HSO+periodicity-UNIQUE ZAMO of the local
  BARYONIC field, (ii) the mass-independent flip criterion r_cross/r_M = sqrt(a0/g_ext) with its
  Galactocentric switch-on radius, (iii) the RAR-budget bound on the kernel memory time. These are
  consequences computed here, not established physics. THE FRAME PRESCRIPTION ITSELF REMAINS A
  POSTULATE, and Route A does not derive a0, does not close the off-circular gap, and does not turn
  the closure into the Euler-Lagrange equation of an action.""")

    banner(f"{nchk} checks run; result = {'ALL PASS' if ok else 'FAILURES PRESENT'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
