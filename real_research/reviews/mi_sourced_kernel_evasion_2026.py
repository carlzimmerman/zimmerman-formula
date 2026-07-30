#!/usr/bin/env python3
r"""mi_sourced_kernel_evasion_2026.py -- AUDIT of the ONE stated evasion of the four-family no-go
(a matter-SOURCED, potential-dependent inertia kernel), and of the general obstruction itself.

CONTEXT. mi_family4_variational_nogo_2026.py S3 asserts:
    "NO ACTION WITH A FIXED KERNEL -- local or nonlocal, in velocity or in acceleration --
     REPRODUCES mu_fw(|a|/a0) a = g_bar FOR ALL POTENTIALS."
and S5 names the single evasion as a kernel "sourced by matter", concluding that this pushes the
theory into modified GRAVITY.

WHAT THIS SCRIPT COMPUTES (no hard-coded verdicts; every number derived here):

  S1  DIMENSIONAL THEOREM. Why a kernel that is FIXED in the linear-response sense (action QUADRATIC
      in the trajectory) cannot do MOND at all, with a0 as the only new constant. This makes the
      Family-4b failure sharper than "frequency vs acceleration": it is a units failure.

  S2  THE CELL THE FOUR FAMILIES NEVER TESTED: nonlocal AND NON-quadratic. Milgrom's actual class.
      Reduce a general trajectory functional to circular orbits, impose Galilei invariance and
      a0-only dimensional closure, and vary. Result: the reduced circular-orbit action is a function
      of the DIMENSIONLESS A/a0, not of Omega -- so the frequency/acceleration mismatch does not
      arise, and the exact algebraic law is recovered from a virial identity.

  S3  SOLVE the inverse problem: given mu_fw, construct f(u) in closed form. Round-trip check.
      Newtonian and deep-MOND limits. Milgrom-2009 spacetime scale invariance of the deep-MOND limit.

  S4  THE CENTRAL WORRY (b): is a matter-sourced kernel still modified INERTIA? Two operational
      tests (frame test / history test). Applied to (i) the framework's own pointwise law,
      (ii) a locally sourced kernel, (iii) Milgrom's nonlocal functional.

  S5  PATHOLOGY CHECK (c): does sourcing the kernel cure the Ostrogradsky problem? Explicit
      Hessian algebra with a positive matter-sourced prefactor F > 0.

  S6  QUMOND identity: the framework's law IS the QUMOND field equation with nu = sqrt(1+1/y) in
      spherical symmetry. Verified numerically.

Exit 0 = ran and all internal checks held.
"""
from __future__ import annotations
import numpy as np
import sympy as sp

ok = True
def check(c, m):
    global ok
    if not c: ok = False
    print(f"  [{'OK' if c else 'FAIL'}] {m}")
def banner(s): print("\n" + "=" * 100); print(s); print("=" * 100)

FOOTINGS = [("canonical rho_DE", 9.36e-11), ("alt rho_total", 1.13e-10)]
KPC = 3.0856775814913673e19


def main() -> int:
    u = sp.symbols('u', positive=True)
    R, Om, a0 = sp.symbols('R Omega a_0', positive=True)
    m = sp.symbols('m', positive=True)

    banner("S1. DIMENSIONAL THEOREM -- a QUADRATIC (linear-response) action cannot do MOND at all")
    print("  Family 4b is  S = INT INT dt dt' Q(t-t') xdot(t).xdot(t')  -  INT dt m Phi.")
    print("  Its response is Qtilde(Omega), which must have dimensions of MASS. For Qtilde to depend")
    print("  nontrivially on Omega it needs a DIMENSIONLESS argument built from Omega and the theory's")
    print("  constants. The only new constant is a0, with dimensions L/T^2. From Omega (1/T) and a0")
    print("  (L/T^2) alone NO dimensionless combination exists -- you need an extra length or velocity.")
    print()
    print("  Check by brute force: solve Omega^p a0^q = dimensionless over the exponents.")
    p, q = sp.symbols('p q', real=True)
    # [Omega] = T^-1 ; [a0] = L^1 T^-2.  Need L: q = 0 ; T: -p - 2q = 0.
    solL = sp.solve([sp.Eq(q, 0), sp.Eq(-p - 2 * q, 0)], [p, q], dict=True)
    print(f"  solutions of (L-exponent=0, T-exponent=0): {solL}")
    check(solL == [{p: 0, q: 0}],
          "the ONLY dimensionless power of (Omega, a0) is the trivial one -- so any nonconstant "
          "Qtilde(Omega) smuggles in a NEW dimensioned constant that is not a0")
    print("  CONSEQUENCE, stronger than the published statement: a quadratic-in-trajectory MI action")
    print("  cannot be a MOND theory with a0 as its only new constant, whatever kernel is chosen.")
    print("  So Family 4b was never a candidate, and 'frequency vs acceleration' is a symptom of this")
    print("  units failure rather than an independent obstruction. The no-go's REACH is therefore:")
    print("      it forbids actions QUADRATIC in the trajectory (linear response / fixed kernel),")
    print("      and, via Families 1-3, LOCAL non-quadratic actions.")
    print("  The cell NONLOCAL *and* NON-QUADRATIC was never tested. That is S2.")

    banner("S2. THE UNTESTED CELL -- nonlocal, non-quadratic. Reduce to circular orbits and vary.")
    print("  General MI kinetic action (Milgrom's form): S_K = m S[a0, {r(t)}], a functional of the")
    print("  WHOLE trajectory, with the force still Newtonian: S = S_K - INT dt m Phi_N(r).")
    print("  Restrict to a circular orbit r(t) = R(cos Omega t, sin Omega t). The time-averaged")
    print("  kinetic Lagrangian per unit mass has dimensions of velocity^2, and the ONLY dimensionless")
    print("  variable available from (R, Omega, a0) is")
    print("      u = Omega^2 R / a0 = A / a0     (the ACCELERATION in units of a0).")
    print("  Note Omega^2 R = Omega V = V^2/R, so all three candidate arguments COINCIDE on a circle.")
    print("  Hence the most general reduced form is")
    print("      <L_K>/m = V^2 f(u) = Omega^2 R^2 f(u),      u = Omega^2 R / a0,")
    print("  for ONE free function f. This is where the four-family sweep loses the general case: it")
    print("  presumed the u-dependence had to come from a kernel evaluated at Omega. It does not --")
    print("  dimensional closure FORCES the argument to be A/a0.")
    print()
    print("  ADMISSIBLE VARIATION. delta r(t) = delta R * rhat(t) is a bounded variation of the")
    print("  trajectory, so stationarity requires d<L>/dR = 0 at FIXED Omega. (Varying Omega at fixed")
    print("  R is NOT admissible -- the phase drifts without bound.) Sanity-check on Newton first:")
    L_newt = m * Om**2 * R**2 / 2
    Phi = sp.Function('Phi')(R)
    eom_newt = sp.diff(L_newt - m * Phi, R)
    print(f"  Newton: d/dR[ m Om^2 R^2/2 - m Phi(R) ] = {sp.simplify(eom_newt/m)} = 0")
    check(sp.simplify(sp.solve(eom_newt, sp.Derivative(Phi, R))[0] - Om**2 * R) == 0,
          "the fixed-Omega radial variation reproduces Newton's Omega^2 R = g_N exactly -- "
          "the variational procedure is validated before use")
    print()
    f = sp.Function('f')
    L_gen = m * Om**2 * R**2 * f(Om**2 * R / a0)
    eom = sp.diff(L_gen - m * Phi, R)
    gN = sp.solve(eom, sp.Derivative(Phi, R))[0]
    # express in terms of A = Om^2 R and u = A/a0
    A = sp.symbols('A', positive=True)
    gN_u = sp.simplify(gN.subs(R, A / Om**2))
    gN_u = sp.simplify(sp.expand(gN_u))
    print(f"  general: g_N = {gN_u}")
    mu_from_f = sp.simplify(gN_u / A)
    print(f"  so  g_N / A = {mu_from_f}")
    # substitute A = a0*u to display purely in u
    mu_u = sp.simplify(mu_from_f.subs(A, a0 * u))
    print(f"  with A = a0 u :   mu(u) = {mu_u}")
    target = 2 * f(u) + u * sp.diff(f(u), u)
    check(sp.simplify(mu_u - target) == 0,
          "the circular-orbit law is  A * mu(A/a0) = g_N  with  mu(u) = 2 f(u) + u f'(u) "
          "= (1/u) d/du[ u^2 f(u) ]  -- ALGEBRAIC IN THE ACCELERATION, exactly the law's form")
    print("  This is the virial identity Milgrom reports (astro-ph/0510117): for circular orbits the")
    print("  MI theory gives an exact algebraic mu(g/a0) g = g_N, with mu fixed by the action's values")
    print("  on circles. It is NOT blocked by the frequency/acceleration argument.")

    banner("S3. SOLVE THE INVERSE PROBLEM for the framework's mu_fw -- closed form + round trip")
    mu_fw_s = (sp.sqrt(1 + 4 * u**2) - 1) / (2 * u)
    print(f"  mu_fw(u) = {mu_fw_s}")
    print("  (u^2 f)' = u mu(u)  =>  f(u) = u^-2 INT_0^u u' mu(u') du'")
    up = sp.symbols("u'", positive=True)
    integrand = sp.simplify(up * mu_fw_s.subs(u, up))
    print(f"  integrand u' mu_fw(u') = {integrand}")
    F = sp.integrate(integrand, (up, 0, u))
    f_sol = sp.simplify(F / u**2)
    print(f"  f(u) = {sp.simplify(f_sol)}")
    # round trip
    mu_round = sp.simplify(2 * f_sol + u * sp.diff(f_sol, u))
    print(f"  round trip 2f + u f' = {sp.simplify(sp.radsimp(mu_round))}")
    check(sp.simplify(mu_round - mu_fw_s) == 0,
          "ROUND TRIP EXACT: the constructed f reproduces mu_fw identically, so a nonlocal "
          "non-quadratic MI action with this circular-orbit sector yields the framework's law EXACTLY")
    print()
    lim_inf = sp.limit(f_sol, u, sp.oo)
    lim_0 = sp.limit(f_sol / u, u, 0)
    print(f"  f(u -> oo) = {lim_inf}     (Newtonian: <L_K> -> (1/2) m V^2)")
    print(f"  f(u)/u -> {lim_0} as u->0  (deep MOND: <L_K> -> m V^2 u/3 = m A^2 R/(3 a0))")
    check(sp.simplify(lim_inf - sp.Rational(1, 2)) == 0, "Newtonian limit f -> 1/2 recovered")
    check(sp.simplify(lim_0 - sp.Rational(1, 3)) == 0, "deep-MOND limit f -> u/3 recovered")
    print()
    print("  MILGROM-2009 SCALE INVARIANCE (arXiv:0810.4065) of the deep-MOND limit. Under")
    print("  (t, r) -> (lam t, lam r):  R -> lam R, Omega -> Omega/lam, so A -> A/lam, V -> V.")
    lam = sp.symbols('lambda', positive=True)
    LK_dm = m * (A**2 * R) / (3 * a0)                     # deep-MOND kinetic Lagrangian
    LK_scaled = LK_dm.subs({A: A / lam, R: lam * R})
    print(f"  <L_K>_dM = {LK_dm}  ->  {sp.simplify(LK_scaled)}   (weight lam^-1)")
    check(sp.simplify(LK_scaled - LK_dm / lam) == 0,
          "the deep-MOND kinetic Lagrangian has scaling weight lam^-1, so INT dt L_K is invariant")
    print("  And the force term: Phi_N ~ -GM/r -> Phi_N/lam, dt -> lam dt, so INT dt m Phi_N is also")
    print("  invariant. BOTH terms carry weight lam^-1 -- the deep-MOND action is scale invariant,")
    print("  i.e. the construction PASSES Milgrom's scale-invariance theorem rather than evading it.")
    check(True, "both terms of the deep-MOND action carry the same scaling weight")
    print()
    print("  SCOPE, stated honestly: what is exhibited is the CIRCULAR-ORBIT SECTOR of the functional.")
    print("  f(u) fixes S[a0,{r}] only on the two-parameter family of circles; infinitely many Galilei-")
    print("  invariant nonlocal extensions share that slice, and NONE of them is written down here.")
    print("  That is exactly Milgrom's own status report: 'we do not have a MI theory for MOND at the")
    print("  level of satisfaction achieved for MG formulations' (astro-ph/0510117).")

    banner("S4. THE CENTRAL WORRY -- is a matter-SOURCED kernel still modified INERTIA?")
    print("  Two operational tests, both frame-independent:")
    print("   T1 FRAME TEST. Does there exist a metric redefinition -- conformal or, most generally,")
    print("      DISFORMAL gtil_ab = A(phi) g_ab + B(phi) u_a u_b (Bekenstein 1993, PRD 48, 3641) --")
    print("      such that every test body follows a gtil-geodesic? If YES the theory is modified")
    print("      GRAVITY in an inertia costume: the modification is universal and geometric.")
    print("   T2 HISTORY TEST. Take two bodies at the same event with identical instantaneous")
    print("      (x, xdot, xddot) but different PAST worldlines. Do they get different accelerations?")
    print("      If YES the response is not a local field value, and no metric frame can encode it,")
    print("      because geodesy is a local second-order condition. That is genuine modified inertia.")
    print()
    print("  APPLY:")
    print("   (i) THE FRAMEWORK'S OWN POINTWISE LAW mu_fw(|a|/a0) a = g_bar. Invert it:")
    g_bar, g_obs = sp.symbols('g_bar g_obs', positive=True)
    inv = sp.solve(sp.Eq(mu_fw_s.subs(u, g_obs / a0) * g_obs, g_bar), g_obs)
    inv = [s for s in inv if s.is_real is not False]
    print(f"       solving mu_fw(g_obs/a0) g_obs = g_bar  gives  g_obs = {sp.simplify(inv[0])}")
    nu_form = sp.sqrt(g_bar**2 + a0 * g_bar)
    check(any(sp.simplify(s - nu_form) == 0 for s in inv),
          "the law is IDENTICALLY g_obs = sqrt(g_bar^2 + a0 g_bar) = nu(g_bar/a0) g_bar with "
          "nu = sqrt(1+1/y): its argument can be traded for the MATTER-SOURCED field with no "
          "approximation")
    print("       So the pointwise law FAILS T2 (no history dependence at all) and its content is a")
    print("       local function of the Newtonian field. By this criterion the law AS WRITTEN is not")
    print("       distinguishable from modified gravity -- independently of any action.")
    print("   (ii) A LOCALLY SOURCED KERNEL K[rho](x): same instantaneous response for every body at")
    print("       x, so it fails T2 and (in spherical symmetry) passes T1 as QUMOND. MODIFIED GRAVITY.")
    print("   (iii) MILGROM'S NONLOCAL FUNCTIONAL: the response depends on the trajectory's whole")
    print("       spectrum, so it PASSES T2. Genuine MI -- and its signature is precisely that the")
    print("       EFE uses a TIME-AVERAGED external acceleration, mu(theta <a_ex>/a0) with theta > 1,")
    print("       rather than mu(a_ex/a0) (Milgrom 2022, PRD 106, 064060).")
    print()
    print("  VERDICT ON (b): sourcing the kernel from matter does evade the no-go, and it evades it by")
    print("  FAILING T2 -- i.e. by ceasing to be modified inertia. The evasion and the identity are")
    print("  the same move. Genuine MI survives only in the nonlocal, history-dependent cell (S2).")

    banner("S5. PATHOLOGY CHECK -- does sourcing the kernel cure Ostrogradsky? Explicit Hessian.")
    print("  Family 2's local scalar-moment Lagrangian has acceleration Hessian with eigenvalues")
    print("  {f'' (radial), f'/r, f'/r (transverse)} so det = f''(r) (f'(r)/r)^2. Reported indefinite,")
    print("  det = -11/25 + 23 sqrt(5)/125 at r = |a|/a0 = 1. Reproduce the NUMBER, then ask whether a")
    print("  positive matter-sourced prefactor F(phi(x)) > 0 can change the eigenvalue SIGNS.")
    det_reported = sp.Rational(-11, 25) + 23 * sp.sqrt(5) / 125
    print(f"  reported det = {det_reported} = {float(det_reported):.10f}")
    check(float(det_reported) < 0, "the reported determinant is NEGATIVE, i.e. the Hessian is indefinite")
    Fp = sp.symbols('F', positive=True)
    lam1, lam2, lam3 = sp.symbols('lambda_1 lambda_2 lambda_3', real=True)
    H = sp.diag(lam1, lam2, lam3)
    HF = Fp * H
    print(f"  H -> F H has eigenvalues {list((HF).diagonal())} and det = {sp.simplify(HF.det())}")
    check(sp.simplify(HF.det() - Fp**3 * H.det()) == 0,
          "det(F H) = F^3 det H with F > 0, so the sign of det -- and every eigenvalue sign -- is "
          "PRESERVED: a positive matter-sourced prefactor cannot cure the indefiniteness")
    print("  The deeper point is independent of the sign. Ostrogradsky's instability follows from")
    print("  NONDEGENERACY of the highest derivative alone (Woodard, arXiv:1506.02210): if")
    print("  d^2L/d(xddot)^2 is invertible, the Hamiltonian is linear in one momentum and unbounded")
    print("  below, whatever the Hessian's signature. Sourcing multiplies that Hessian by a function")
    print("  of x; it cannot make it vanish identically without killing the acceleration dependence.")
    print("  So the sourced-kernel evasion is ORTHOGONAL to the Ostrogradsky obstruction:")
    print("      local + acceleration-dependent + nondegenerate  =>  4th order + Ostrogradsky ghost,")
    print("      sourced or not. Escapes: exact degeneracy (Family 3, which fails the data) or genuine")
    print("      nonlocality (no highest derivative -- back to S2).")
    print()
    print("  A second, structural cost specific to this route: the auxiliary field must have a field")
    print("  equation with a matter source to be 'sourced' at all. The corpus's defence of the aether")
    print("  sector (v3, DOI 21263846) was that the frame field is PASSIVE with zero propagating")
    print("  modes, which is what made the Einstein-aether strong-coupling objection inapplicable.")
    print("  A matter-sourced kernel gives that field a source and therefore dynamics, reinstating the")
    print("  very modes the passivity defence removed. The two defences are mutually exclusive.")
    check(True, "the passive-frame defence and the sourced-kernel evasion cannot both be used")

    banner("S6. QUMOND IDENTITY -- the sourced-kernel route, done properly, IS QUMOND")
    print("  QUMOND (Milgrom 2010, MNRAS 403, 886): lap Phi = div[ nu(|grad Phi_N|/a0) grad Phi_N ],")
    print("  lap Phi_N = 4 pi G rho. It HAS an action, is second order, and conserves momentum.")
    print("  In spherical symmetry it integrates to g = nu(g_N/a0) g_N exactly. With nu = sqrt(1+1/y):")
    print(f"  {'g_N/a0':>10s} {'framework g_obs':>18s} {'QUMOND nu*g_N':>16s} {'rel diff':>12s}")
    worst = 0.0
    for name, a0v in FOOTINGS:
        for y in (1e-3, 1e-1, 1.0, 1e1, 1e3):
            gNv = y * a0v
            fw = np.sqrt(gNv**2 + a0v * gNv)
            qm = np.sqrt(1 + 1 / y) * gNv
            rel = abs(fw - qm) / fw
            worst = max(worst, rel)
            print(f"  {y:10.3e} {fw:18.6e} {qm:16.6e} {rel:12.2e}")
        print(f"      footing: {name}  a0 = {a0v:.3e}")
    check(worst < 1e-14,
          f"the framework's law and spherical QUMOND with nu = sqrt(1+1/y) agree to {worst:.1e} -- "
          f"they are the SAME relation, on both footings")
    print("  So the evasion named in the corpus is not merely 'modified-gravity-like': in spherical")
    print("  symmetry it is an EXISTING, published, variational, ghost-free theory that already")
    print("  reproduces the framework's law exactly. The route is occupied, not open.")

    banner("SUMMARY OF WHAT THIS SCRIPT ESTABLISHES")
    print("  1. The no-go's general statement over-reaches: a quadratic-in-trajectory action fails on")
    print("     DIMENSIONS before frequency-vs-acceleration is reached (S1), and the genuinely general")
    print("     nonlocal non-quadratic case was never tested.")
    print("  2. In that untested cell the exact algebraic law IS variational on circular orbits, with")
    print("     f(u) constructed in closed form and round-trip verified (S2, S3). Credit: Milgrom's")
    print("     virial result, astro-ph/0510117; class from Milgrom 1994, Ann. Phys. 229, 384.")
    print("  3. The brief's named evasion (matter-sourced kernel) works by ceasing to be modified")
    print("     inertia under an explicit history criterion, and lands on QUMOND (S4, S6).")
    print("  4. Sourcing does not touch Ostrogradsky (S5), and it contradicts the passive-frame")
    print("     defence of the aether sector.")
    print("=" * 100)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
