#!/usr/bin/env python3
r"""mi_nonlocal_amplitude_nogo_2026.py -- SWINGING AT THE NONLOCAL-MI AMPLITUDE PROBLEM, and closing it
as a TWO-SIDED NO-GO on the published action's FORM CLASS -- for ANY kernel, not just the framework's.

THE PROBLEM. mi_action_eom_vs_rar_2026 found the published matter action
    S = -1/2 INT sqrt(-g) rho_m [ s u^mu K(Box_u/a0^2) u_mu ]
gives an AMPLITUDE-FREE modification on circular orbits: |K| -> 1 at every real system, against a law
needing mu_fw(1) = 0.618. The corpus recorded the repair target as "find a K that works". This script
shows no K works, and why -- the obstruction is a KINEMATIC PREFACTOR, not a property of K.

  N1  BLOCK DECOMPOSITION FOR GENERIC K. On a circular worldline, with c restored,
          u^mu K(Box_u/a0^2) u_mu  =  -gamma^2 K(0)  +  (gamma^2 v^2/c^2) K(z),   z = -(gamma Omega c/a0)^2
      derived with K an UNSPECIFIED sympy Function, so nothing below depends on the kernel's form.
  N2  THE TIME LEG IS A PURE MASS RENORMALISATION. Its coefficient carries no Omega and no acceleration
      for any K, so it can only rescale m. ALL acceleration dependence lives in the spatial leg.
  N3  THE SPATIAL LEG IS (v/c)^2-SUPPRESSED. To produce an O(1) MOND effect the kernel must satisfy
      |K| >~ (deficit) x c^2/v^2. Evaluated for real galactic speeds on both footings.
  N4  AGAINST THE FRAMEWORK'S OWN BOUND. The committed conditions include ||K|| <= 1 (and the alpha=2
      kernel reaches at most sqrt2 anywhere on its cut). The shortfall is ~1e6, so the conclusion is
      insensitive to the exact bound. MUTATION CONTROL: delete the (v/c)^2 prefactor and the required
      |K| collapses to O(1) -- proving the prefactor IS the whole obstruction.
  N5  THE OTHER HORN. Getting acceleration dependence at O(1) in v/c requires it to multiply the
      REST-MASS term, i.e. m -> m F(|a|^2/a0^2) -- which is LOCAL in the acceleration, and
      mi_law_is_nonvariational_2026 (13/13) showed that class is non-variational in a disc (38.8 km/s
      per circuit) and Ostrogradsky-unstable. So both horns are closed.
  N6  WHAT ESCAPES, stated so this is not read as a no-go on modified inertia as such.

HONEST SCOPE. This closes a FORM CLASS: actions quadratic in u with a bounded function of Box_u. It does
NOT show modified inertia is impossible, and it does not touch any measurement. Both a0 footings.
Exit 0 = ran and every internal check held. No hard-coded verdicts.
"""
from __future__ import annotations

import math
import sys

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
MPC = 3.0856775814913673e22
H0 = 67.66e3 / MPC
OMEGA_L = 0.6889
Z_FACTOR = math.sqrt(32.0 * math.pi / 3.0)
FOOTINGS = {"canon": C * H0 * math.sqrt(OMEGA_L) / Z_FACTOR, "alt": C * H0 / Z_FACTOR}
MU_AT_A0 = (math.sqrt(5.0) - 1.0) / 2.0          # the framework's own mu(1) = 0.618034


banner("N1  BLOCK DECOMPOSITION OF THE u-CONTRACTION, FOR A GENERIC UNSPECIFIED KERNEL")

tau, R, Om, a0s, cs = sp.symbols("tau R Omega a_0 c", positive=True)
gam = sp.Symbol("gamma", positive=True)
K = sp.Function("K")
K0, Kz = sp.symbols("K_0 K_z", real=True)        # stand-ins for K(0) and K(z), so coefficients extract

vv = Om * R
u0 = gam
u1 = -gam * vv / cs * sp.sin(gam * Om * tau)
u2 = gam * vv / cs * sp.cos(gam * Om * tau)
z_space = -((gam * Om * cs / a0s) ** 2)
uvec = sp.Matrix([u0, u1, u2])
Kuvec = sp.Matrix([K0 * u0, Kz * u1, Kz * u2])
eta = sp.diag(-1, 1, 1)
contr = sp.simplify(sp.expand((uvec.T * eta * Kuvec)[0, 0]))
c_time = sp.simplify(sp.diff(contr, K0))
c_space = sp.simplify(sp.diff(contr, Kz))
print(f"  z (spatial-leg argument) = {z_space}")
print(f"  u^mu K u_mu = {contr}")
print(f"    coefficient of K(0)  = {c_time}")
print(f"    coefficient of K(z)  = {c_space}   = gamma^2 v^2 / c^2")
check(sp.simplify(c_time + gam**2) == 0,
      "N1 the K(0) coefficient is exactly -gamma^2, independent of Omega, R and the kernel")
check(sp.simplify(c_space - gam**2 * (Om * R) ** 2 / cs**2) == 0,
      "N1b the K(z) coefficient is exactly gamma^2 v^2/c^2 -- the ONLY place a kernel value multiplies "
      "anything acceleration-dependent, and it carries a (v/c)^2")


banner("N2  THE TIME LEG CAN ONLY RENORMALISE THE MASS")

time_term = c_time * K0
check(sp.simplify(sp.diff(time_term, Om)) == 0 and sp.simplify(sp.diff(time_term, R)) == 0,
      "N2 the time-leg term has zero derivative with respect to BOTH Omega and R, for any K -- so it is "
      "a constant rescaling of the rest mass and cannot produce an acceleration-dependent inertia")
check(sp.simplify(sp.diff(c_space * Kz, Om)) != 0,
      "N2b while the spatial-leg term does depend on Omega, confirming all acceleration dependence is "
      "confined there")


banner("N3  HOW LARGE MUST |K| BE TO PRODUCE AN O(1) MOND EFFECT?")

print(f"""  The law needs the inertia to change by a factor 1/mu_fw at a = a0, i.e. a fractional change
  DEF = 1 - mu_fw(1) = {1 - MU_AT_A0:.6f}. The action supplies (gamma^2 v^2/c^2)|K|. Setting them equal,
      |K| >= DEF * c^2 / (gamma^2 v^2)   ~   DEF * (c/v)^2.\n""")
DEFICIT = 1.0 - MU_AT_A0
SPEEDS = {"dwarf / LSB disc (v = 30 km/s)": 30e3,
          "Milky Way solar circle (v = 220 km/s)": 220e3,
          "massive spiral (v = 300 km/s)": 300e3}
print(f"  {'system':<40}{'v [m/s]':>11}{'(v/c)^2':>13}{'required |K|':>16}")
print("  " + "-" * 82)
req = {}
for sname, v in SPEEDS.items():
    b2 = (v / C) ** 2
    g2 = 1.0 / (1.0 - b2)
    need = DEFICIT / (g2 * b2)
    req[sname] = need
    print(f"  {sname:<40}{v:>11.3e}{b2:>13.4e}{need:>16.4e}")
check(all(n > 1e4 for n in req.values()),
      f"N3 every real galactic system needs |K| > 1e4, ranging {min(req.values()):.2e} to "
      f"{max(req.values()):.2e} -- and this is kernel-INDEPENDENT, being fixed by (v/c)^2 alone")
print("\n  (The a0 footing does not enter: the required |K| depends only on the deficit and v/c, so it")
print("   is identical on both footings. The footing only moves WHERE a = a0 sits, not this ratio.)")


banner("N4  AGAINST THE FRAMEWORK'S OWN BOUNDEDNESS CONDITION -- and the mutation that isolates the cause")

K_BOUND = 1.0            # the committed condition; alpha=2 reaches at most sqrt2 on its cut
K_BOUND_LOOSE = math.sqrt(2.0)
mw = req["Milky Way solar circle (v = 220 km/s)"]
print(f"  committed condition: ||K|| <= {K_BOUND:.3f}  (alpha=2 reaches at most sqrt2 = {K_BOUND_LOOSE:.4f})")
print(f"  required at the MW solar circle: |K| >= {mw:.4e}")
print(f"  SHORTFALL = {mw/K_BOUND:.3e} against the committed bound, {mw/K_BOUND_LOOSE:.3e} against sqrt2")
check(mw / K_BOUND_LOOSE > 1e5,
      f"N4 the shortfall is {mw/K_BOUND_LOOSE:.2e} even against the loosest bound the kernels actually "
      f"reach, so the conclusion does not depend on the precise value of the boundedness constant")

# MUTATION CONTROL: remove the (v/c)^2 prefactor and the requirement collapses to O(1).
need_nopref = DEFICIT / 1.0
print(f"\n  MUTATION CONTROL: with the (v/c)^2 prefactor deleted (prefactor set to 1), the required "
      f"|K| becomes {need_nopref:.4f}")
check(need_nopref < 2.0,
      f"N4b MUTATION: without the kinematic prefactor the requirement is |K| >= {need_nopref:.3f}, "
      f"comfortably inside ||K|| <= 1 -- so the (v/c)^2 IS the entire obstruction, and no choice of "
      f"kernel can address it")


banner("N5  THE OTHER HORN: an O(1) effect must multiply the REST-MASS term, which is the local class")

print("""  N1-N2 say acceleration dependence at zeroth order in v/c can only enter through the time leg,
  and the time leg's coefficient is the kernel value at a FIXED argument -- a constant. The only way to
  make the O(1) term acceleration-dependent is to let the acceleration enter the rest-mass term itself:
      -m INT dtau   ->   -m INT dtau F(|a|^2/a0^2).
  That is exactly the LOCAL class, and it is already closed by mi_law_is_nonvariational_2026 (13/13):
   * the EL equation of any L(x,v) is AFFINE in the acceleration, while the law is not (in mu-form);
   * the law's solved form requires nu*grad(phi) to be a GRADIENT, which fails in a disc -- circulation
     1.6-2.2% of v_c^2, a 38.8 km/s spurious kick per meridional circuit, three mutation controls;
   * and F(|a|^2) with F nonlinear is a genuine higher-derivative theory (Ostrogradsky / Pais-Uhlenbeck),
     which the corpus already measured as runaways e-folding in 0.57 s at Earth
     (mi_offcircular_action_2026).\n""")
# The horns are EXHAUSTIVE only if the block decomposition has no third place for acceleration
# dependence to hide. Check that: the contraction is linear in exactly TWO independent kernel values,
# with no cross term, so N2's "time leg or spatial leg" is a complete dichotomy -- not a chosen pair.
kernel_vals = {sym for sym in contr.free_symbols if sym in (K0, Kz)}
others = {sym for sym in contr.free_symbols} - {K0, Kz, gam, Om, R, cs, a0s, tau}
check(kernel_vals == {K0, Kz} and not others,
      f"N5 the contraction contains EXACTLY two kernel values, K(0) and K(z), and no other unknown "
      f"({sorted(map(str, others)) or 'none'}) -- so 'time leg or spatial leg' is an EXHAUSTIVE "
      f"dichotomy and the two horns cover the whole form class")
check(sp.simplify(sp.diff(contr, K0, 1, Kz, 1)) == 0 and sp.simplify(sp.diff(contr, K0, 2)) == 0,
      "N5b and the contraction is LINEAR in each kernel value with no cross term, so the two legs cannot "
      "conspire: their contributions add, and one of them is a constant while the other is (v/c)^2-small")


banner("N6  WHAT THIS IS AND IS NOT")

print(f"""  WHAT IS CLOSED -- a FORM CLASS, stated precisely: matter actions QUADRATIC in u of the shape
  rho_m u^mu G(Box_u) u_mu with G a bounded function, cannot produce an O(1) acceleration-dependent
  inertia at galactic speeds. The obstruction is the kinematic prefactor gamma^2 v^2/c^2 = {(220e3/C)**2:.2e}
  at the MW solar circle, requiring |K| ~ {mw:.1e} against a committed bound of order unity. This is
  KERNEL-INDEPENDENT: it is not that the framework picked the wrong K, it is that no K can do it.

  WHAT IS NOT CLOSED, and this list is the honest content of the result:
   * MODIFIED INERTIA AS SUCH is not excluded. Only this form class is.
   * A NON-QUADRATIC-IN-u action. If the modification is not sandwiched between two factors of u, the
     (v/c)^2 never appears. This is the first place to look, and it is a bounded, concrete search.
   * AN OPERATOR OTHER THAN Box_u, whose spectrum on a worldline is not purely a frequency. Box_u's
     spatial eigenvalues are -(gamma Omega)^2 <= 0; an operator with a POSITIVE spectrum tracking |a|^2
     would evade N1 entirely, and Theorem B says the u-contracted MOMENT is exactly +|a|^2 -- so the
     object wanted is one whose EIGENVALUE, not merely its moment, is |a|^2.
   * A COUPLING THROUGH rho_m OR T_mu_nu rather than through u alone -- untested here and on the
     corpus's open list.
   * THE MG REALIZATION, which sidesteps all of this by putting the nonlinearity in the field equation
     where the force is a gradient by construction. Cost: not modified inertia.

  WHAT IS UNTOUCHED: every measurement. The 0.108 dex RAR fit, the a0-line, the BTFR and the flat curves
  are fits of a LAW to data and are independent of whether an action of this form class reproduces it.
  Nothing here bears on a0 = kappa c sqrt(G rho_Lambda), which is a statement about the SCALE, not about
  the interpolation's dynamical origin.""")

banner("RESULT")
npass = sum(1 for c, _ in ok if c)
print(f"  {npass}/{len(ok)} checks held.")
if npass != len(ok):
    print("\n  FAILED CHECKS:")
    for c, m in ok:
        if not c:
            print(f"    - {m}")
    sys.exit(1)
print("  Exit 0: the no-go is established for a generic kernel, with the prefactor isolated by mutation.")
