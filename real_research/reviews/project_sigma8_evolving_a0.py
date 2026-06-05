#!/usr/bin/env python3
"""
Does EVOLVING a0 = cH(z)/Z make the sigma8 / S8 tension BETTER, WORSE, or UNCHANGED
vs constant-a0 MOND?  An honest, order-of-magnitude adjudication.
====================================================================================

THE SETUP (all established, not contested here):
  * Weak lensing (KiDS-1000, DES-Y3) finds S8 = sigma8 sqrt(Om/0.3) a few % BELOW the
    Planck-LCDM prediction: structure is slightly LESS clustered than LCDM wants.
        Planck:  S8 ~ 0.83     KiDS/DES:  S8 ~ 0.76-0.78    (the "S8 tension", ~2-3 sigma)
  * MOND / modified gravity GENERICALLY ENHANCES growth: extra gravity below a0 speeds up
    collapse (Sanders 1998, McGaugh 1999, Nusser 2002). Enhanced growth -> HIGHER sigma8.
    => Standard (constant-a0) MOND already pushes the WRONG WAY for the low-S8 tension.
    (This is the repo's own UNIFICATION_DOORS_LEDGER line: "sigma8: NEW anti-MOND front".)

THE QUESTION (this file): the framework's distinctive claim is that a0 EVOLVES, a0(z)=cH(z)/Z,
  so a0 is LARGER at higher z (during the structure-growth epoch). Naively: more a0 during
  growth -> more enhancement -> even higher sigma8 -> EVEN WORSE than constant-a0 MOND.
  Is that right? Work it honestly, including the counter-checks (saturation; whether the
  enhancement even operates at the scales/epochs that set S8; the framework's own theorems).

HONESTY LABELS:
  [FACT]      arithmetic / definitional, not in dispute
  [DERIVED]   follows from a stated MOND/EFE premise with an order-of-mag estimate
  [THEOREM]   the framework's own delta-Y=0 order-counting claim (from bridge1_aest_equations.md)
  [TENSION]   an internal inconsistency in the framework, flagged honestly
  [VERDICT]   the bottom line

Run:  python real_research/reviews/project_sigma8_evolving_a0.py   (needs numpy)
"""
import numpy as np

# ---------------------------------------------------------------- constants / cosmology
c    = 2.99792458e8          # m/s
G    = 6.674e-11             # SI
Mpc  = 3.0857e22             # m
Msun = 1.989e30              # kg
h    = 0.674
Om   = 0.315
OL   = 0.685
H0   = h * 100e3 / Mpc       # 1/s
rho_crit0 = 1.878e-26 * h**2 # kg/m^3
rho_m0    = Om * rho_crit0
a0_today  = 1.2e-10          # m/s^2 (SPARC z=0 anchor)
Z         = 2 * np.sqrt(8 * np.pi / 3)   # 5.789

E   = lambda z: np.sqrt(Om * (1 + z)**3 + OL)          # H(z)/H0
a0z = lambda z: a0_today * E(z)                        # the evolving law cH(z)/Z

# interpolation / EFE screening functions: G_eff/G = 1/mu(x), x = g/a0
mu_simple   = lambda x: x / (1 + x)
mu_standard = lambda x: x / np.sqrt(1 + x * x)


# ============================================================================
def part0_evolution():
    print("=" * 78)
    print("PART 0 [FACT]  a0 is LARGER at higher z -- the magnitude of the evolution")
    print("=" * 78)
    print("  E(z)=H(z)/H0=sqrt(0.315(1+z)^3+0.685); a0(z)=a0(0)*E(z).")
    print(f"  {'z':>5}{'E(z)':>9}{'a0(z)/a0(0)':>14}{'a0(z) [m/s^2]':>16}")
    for z in (0.0, 0.5, 1.0, 2.0, 3.0):
        print(f"  {z:>5.1f}{E(z):>9.3f}{E(z):>14.3f}{a0z(z):>16.2e}")
    print("  => during the structure-growth epoch z~0.5-3, a0 is 1.3x (z=0.5) to 4.6x (z=3)")
    print("     its present value. So IF a0 sets the growth boost, evolving a0 deposits MORE")
    print("     extra gravity exactly when structure is assembling -> naive expectation: MORE")
    print("     growth enhancement than constant-a0 MOND -> HIGHER sigma8 -> WORSE S8. We now")
    print("     test that naive chain link by link.\n")


# ============================================================================
def part1_naive_direction():
    print("=" * 78)
    print("PART 1 [DERIVED]  The NAIVE deep-MOND growth boost, and why MORE a0 = MORE growth")
    print("=" * 78)
    print("""  Linear growth obeys  D'' + 2H D' = 4 pi G_eff rho_m D.  Any G_eff > G speeds growth.
  In deep MOND (internal g << a0) the isolated boost diverges as G_eff/G ~ (a0/g)^(1/2):
  larger a0 -> larger G_eff -> faster D -> higher sigma8. Toy growth-rate scaling f=dlnD/dlna
  ~ Om(z)^gamma with an enhanced effective Newton constant pushes f, hence sigma8, UP.""")
    # toy: amplitude of growth enhancement ~ sqrt(G_eff/G) integrated; here show the *direction*
    # via the unscreened deep-MOND G_eff at a fiducial internal acceleration vs a0(z).
    g_internal = 2.3e-13        # self-gravity of an 8 Mpc/h, delta~1 perturbation (Part 2)
    print(f"  {'z':>5}{'a0(z)':>11}{'(a0/g)^1/2 UNSCREENED':>24}{'naive G_eff/G':>15}")
    for z in (0.0, 1.0, 2.0, 3.0):
        ratio = np.sqrt(a0z(z) / g_internal)
        print(f"  {z:>5.1f}{a0z(z):>11.2e}{ratio:>24.1f}{ratio:>15.1f}")
    print("""  If THIS (the isolated deep-MOND boost) were the operative physics, evolving a0 would
  be catastrophic for S8: G_eff/G ~ 20-50, growing with z, sigma8 wildly too high. BUT this
  unscreened number is physically WRONG for cosmology -- it ignores the External Field Effect
  from the cosmic field every perturbation is bathed in. That is Part 3, and it is decisive.\n""")


# ============================================================================
def part2_which_regime():
    print("=" * 78)
    print("PART 2 [FACT]  Do the SCALES that set S8 sit in the MOND or Newtonian regime?")
    print("=" * 78)
    print("""  S8 = sigma8 sqrt(Om/0.3); sigma8 is the rms LINEAR density contrast in 8 Mpc/h spheres
  -- a LINEAR-theory quantity dominated by k ~ 0.1-0.2 h/Mpc. Compute the self-gravity of
  such a perturbation: g = G (delta M)/R^2 at R=8 Mpc/h, delta~1 (sigma8~0.8 ~ order unity).""")
    R8 = 8 / h * Mpc
    M8 = 4 / 3 * np.pi * R8**3 * rho_m0
    print(f"  R = 8 Mpc/h = {R8/Mpc:.1f} Mpc;  mean mass enclosed M8 = {M8/Msun:.2e} Msun")
    print(f"  {'delta':>7}{'g_self [m/s^2]':>16}{'g/a0(0)':>12}{'regime':>14}")
    for delta in (0.5, 1.0, 2.0):
        g = G * (delta * M8) / R8**2
        reg = "deep-MOND" if g < a0_today else "Newtonian"
        print(f"  {delta:>7.1f}{g:>16.2e}{g / a0_today:>12.2e}{reg:>14}")
    print("""  => g_self ~ 2e-13 m/s^2, i.e. g/a0 ~ 2e-3 -- about 500x BELOW a0. On the NAIVE
  internal-acceleration criterion, S8-scale perturbations are DEEPLY in the low-acceleration
  regime, NOT Newtonian. So one cannot dismiss the effect by saying 'those scales are
  Newtonian, a0 irrelevant.' They are not Newtonian. (Only collapsed cluster cores reach
  g ~ a0; the linear 8 Mpc/h field is far below it.) The escape, if there is one, is NOT
  'wrong regime' -- it is the External Field Effect, Part 3.\n""")


# ============================================================================
def part3_efe_freezing():
    print("=" * 78)
    print("PART 3 [DERIVED]  The decisive correction: the cosmic field, the EFE, and Z-freezing")
    print("=" * 78)
    print("""  Every cosmological perturbation is embedded in the homogeneous cosmic dynamical field,
  whose acceleration scale is a_H = cH(z). By the framework's OWN definition a0=cH/Z, so
       a_H / a0(z) = cH(z) / (cH(z)/Z) = Z = 5.789  at EVERY epoch  [FACT, exact].
  The cosmic field is ABOVE a0 (by the fixed factor Z). Under the External Field Effect a
  weak sub-system (g_internal << a0) bathed in a stronger uniform field g_ext is screened:
  its boost is set by mu(g_ext/a0), NOT by the divergent isolated (a0/g_internal)^1/2.""")
    print(f"  {'mu form':>26}{'x=g_ext/a0=Z':>14}{'mu(Z)':>9}{'G_eff/G=1/mu':>14}")
    for nm, mu in (("simple   x/(1+x)", mu_simple(Z)),
                   ("standard x/sqrt(1+x^2)", mu_standard(Z))):
        print(f"  {nm:>26}{Z:>14.3f}{mu:>9.3f}{1 / mu:>14.3f}")
    print(f"""  => the EFE-regulated growth boost is only G_eff/G ~ 1.01-1.17 (mu-dependent), NOT 20-50.
  And here is the crux for the BETTER/WORSE/UNCHANGED question:
       because x = g_ext/a0 = Z is EPOCH-INDEPENDENT (it is fixed by the very law a0=cH/Z),
       the EFE boost G_eff/G = 1/mu(Z) is the SAME at z=0 and z=3 and z=1100.
  The a0(z) running CANCELS: a0 rises, but the cosmic field a_H=cH rises in lockstep, so the
  ratio that controls the boost never moves. Constant-a0 MOND and evolving-a0 MOND therefore
  predict the SAME large-scale growth boost. Evolving a0 adds ~NOTHING beyond constant-a0 MOND
  on linear / S8 scales. [DERIVED, order-of-magnitude; the rigorous version is Part 4.]\n""")


# ============================================================================
def part4_order_counting_theorem():
    print("=" * 78)
    print("PART 4 [THEOREM]  The framework's stronger claim: a0 is ABSENT from LINEAR growth")
    print("=" * 78)
    print("""  bridge1_aest_equations.md gives an order-counting theorem on the AeST action. The
  a0-dependent MOND term is  F ~ (1/a0) Y^(3/2),  Y = q^{mu nu} grad_mu phi grad_nu phi, with
  q projecting ORTHOGONAL to the cosmic aether A. On FRW the scalar is purely temporal, so
        background:    Ybar = 0           (spatial projection of a temporal gradient)
        linear order:  deltaY = 0         (same projection kills the cross term)
        => Y = O(delta phi^2),  so  (1/a0)Y^(3/2) = O(delta phi^3)  -- THIRD order.
  The a0 term contributes NOTHING to the second-order action, i.e. nothing to the LINEAR
  equations of motion. bridge1_linear_boltzmann.py confirms this numerically: flipping the
  running-a0 term on/off changes the linear transfer function by 0 (to machine precision).""")
    print("""  IF this theorem holds, the conclusion is sharper than Part 3's 'frozen boost':
       sigma8 is a LINEAR quantity  ->  it is EXACTLY a0-free  ->  D(z), sigma8, S8 take their
       a0-free (effectively LCDM-dust) values for ANY a0(z), constant or evolving.
  Then evolving a0 is EXACTLY UNCHANGED vs constant-a0 MOND for S8 -- BOTH equal LCDM at
  linear order; the MOND boost (and any a0-running) lives only at NONLINEAR / quasi-static
  (galaxy, cluster-core) scales, which are not what sigma8/S8 at 8 Mpc/h measures.\n""")


# ============================================================================
def part5_internal_tension():
    print("=" * 78)
    print("PART 5 [TENSION]  The honest internal inconsistency -- you cannot have it both ways")
    print("=" * 78)
    print("""  The framework makes TWO claims that pull against each other on this exact axis:
    (A) PRO-MOND structure wins (FALSIFICATION_MATRIX, TESTABLE_PREDICTIONS, TOE docs):
        'MOND drives ACCELERATED early structure growth' -> explains El Gordo (6.2 sigma),
        JWST early-massive galaxies, fast bars, the KBC void. This REQUIRES enhanced growth.
    (B) CMB/S8 safety (bridge1 theorem, bullet_and_s8_reexamination): a0 is ABSENT from
        linear growth -> sigma8 is a0-free -> the framework does NOT enhance linear clustering.
  These cannot both be fully true. The reconciliation the framework actually relies on:
    * the GENUINE MOND growth enhancement is a NONLINEAR effect (collapse of already-mildly-
      overdense regions, where internal g climbs toward a0 and the EFE screening weakens).
      It boosts the abundance of RARE, MASSIVE, COLLAPSED objects (clusters like El Gordo) and
      the speed of nonlinear collapse -- the high-sigma tail.
    * sigma8/S8 is the LINEAR variance at 8 Mpc/h (Part 2: g/a0 ~ 2e-3, EFE-screened by the
      Z-fixed cosmic field, Part 3; and a0-free at linear order, Part 4). It is NOT the rare
      tail. So the framework's structure 'wins' and its S8 'safety' live at DIFFERENT scales.
  Honest reading: the enhancement that helps El Gordo is real but NONLINEAR/high-tail; the
  LINEAR amplitude that sets S8 is (by the theorem) ~untouched. The a0(z) RUNNING does not
  change this split -- it is frozen out of both the linear amplitude (Part 4) and, via the
  Z-fixed EFE, out of the large-scale boost (Part 3).\n""")


# ============================================================================
def part6_verdict():
    print("=" * 78)
    print("PART 6 [VERDICT]  Better / Worse / Unchanged, and the order-of-magnitude estimate")
    print("=" * 78)
    print(f"""  DIRECTION of the naive chain (Part 1): YES, taken at face value a larger a0 during the
  growth epoch means MORE extra gravity -> MORE growth -> HIGHER sigma8 -> WORSE for low-S8.
  My prior was that evolving a0 makes the low-S8 tension WORSE (another strike).

  BUT the naive chain breaks at the step that matters, and it breaks the SAME way for the
  running as for the constant law:
   * [Part 2] S8 scales ARE deep-MOND on the internal-acceleration test (g/a0~2e-3), so the
     effect is NOT killed by 'wrong regime' -- that easy out is false.
   * [Part 3] but every perturbation sits in the cosmic field a_H=cH=Z*a0, and x=a_H/a0=Z is
     EPOCH-INDEPENDENT BY CONSTRUCTION. The EFE boost G_eff/G=1/mu(Z)~1.01-1.17 is therefore
     FROZEN across z. a0 rises, a_H rises in lockstep, the controlling ratio never moves
     -> the a0(z) running CANCELS out of large-scale growth.
   * [Part 4] the framework's order-counting THEOREM goes further: a0 is absent from the
     LINEAR equations entirely (MOND term is O(delta^3)), so sigma8 is EXACTLY a0-free for
     ANY a0(z). Verified numerically in bridge1_linear_boltzmann.py (0 to machine precision).

  ORDER-OF-MAGNITUDE: the change in linear sigma8 from constant-a0 -> evolving-a0 MOND is
     |Delta sigma8 / sigma8|_running-vs-constant  ~  0   (Part 4 theorem; <~1% if the theorem
     is only approximate, since the residual EFE boost is Z-frozen, Part 3). It is NOT the
     ~10-50% that the naive unscreened reading (Part 1) would give.

  DOES THE EFFECT OPERATE AT S8-RELEVANT SCALES?  The relevant scales (8 Mpc/h, linear) are
  deep-MOND by internal acceleration (so 'Newtonian, irrelevant' is the WRONG reason to call
  it neutral) -- but the cosmic-field EFE freezes the boost in z, and the order-counting
  theorem removes a0 from the linear sector altogether. So the a0-RUNNING does NOT operate at
  the linear scales that set S8. The genuine MOND growth enhancement that the framework
  invokes for El Gordo/JWST is NONLINEAR (the rare massive tail), a different observable.

  ===========================================================================
  HONEST VERDICT vs constant-a0 MOND, for the S8 tension:  ~UNCHANGED (NEUTRAL).
  ===========================================================================
   * NOT 'worse': the naive 'more a0 -> more growth' is correct as a sign but is FROZEN OUT
     by the Z=g_ext/a0 epoch-independence (EFE, Part 3) and by the a0-absent-from-linear-growth
     theorem (Part 4). Evolving a0 adds essentially nothing to constant-a0 MOND at S8 scales.
   * The S8 PROBLEM IS REAL AND INHERITED, but it belongs to MOND-as-modified-gravity in
     GENERAL (enhanced growth, wrong sign), NOT specifically to the a0(z) evolution. Constant
     and evolving MOND share whatever S8 exposure exists; the EVOLUTION is not an extra strike.
   * Caveat to my own neutrality: this rests on (i) the EFE freezing AND (ii) the O(delta^3)
     theorem. (ii) is an order-counting argument on a Y^(3/2) NON-ANALYTIC term whose
     perturbation theory around Y=0 is delicate (the doc flags this). A full modified-Boltzmann
     run (hi_class + AeST) is the only way to PROVE |Delta sigma8| ~ 0 rather than argue it.
     Until then: 'unchanged' is the honest best estimate, with a residual <~few-% uncertainty
     that is NOT in the worsening direction in any controlled limit computed here.""")
    print("=" * 78)


def main():
    print("#" * 78)
    print("#  sigma8 / S8 under EVOLVING a0=cH(z)/Z  vs  constant-a0 MOND -- honest verdict")
    print("#" * 78 + "\n")
    part0_evolution()
    part1_naive_direction()
    part2_which_regime()
    part3_efe_freezing()
    part4_order_counting_theorem()
    part5_internal_tension()
    part6_verdict()


if __name__ == "__main__":
    main()
