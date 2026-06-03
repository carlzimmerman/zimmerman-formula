#!/usr/bin/env python3
"""
STRESS TEST of the geometric origin of a0 -- adversarial, ultrathink. What survives, what is a bet.
==================================================================================================
The deep dive (GEOMETRIC_ORIGIN_OF_A0.md) argued a0 ~ cH is the de Sitter horizon's acceleration. Here
we ATTACK that claim on every front and report what survives honestly. The headline finding: the horizon
fixes the MAGNITUDE (a0 must be cosmic) but NOT the evolution -- and the more standard reading (event
horizon / sqrt(Lambda), Milgrom-Verlinde) gives a CONSTANT a0, while the framework's evolving a0 prop H(z)
is the apparent-horizon CHOICE. The evolution is a testable bet, not a theorem. Needs numpy.
"""
import numpy as np

c, G, hbar, kB, Mpc = 2.99792458e8, 6.674e-11, 1.0546e-34, 1.381e-23, 3.0857e22
H0, Om, OL = 67.4e3/Mpc, 0.315, 0.685
Z, a0_obs = 2*np.sqrt(8*np.pi/3), 1.2e-10
E = lambda z: np.sqrt(Om*(1+z)**3 + OL)
HL = H0*np.sqrt(OL)                                    # asymptotic de Sitter H (event horizon)


def attack1():
    print("="*92); print("ATTACK 1 -- the coefficient is NOT O(1): the horizon fixes a0 only to ~1 dex"); print("="*92)
    print(f"  The horizon COINCIDENCE (Rindler=de Sitter) is at a=cH0={c*H0:.2e}, but observed a0={a0_obs:.2e}")
    print(f"  -- a factor {c*H0/a0_obs:.1f} BELOW. Thermodynamic matching schemes span:")
    for nm, a in [("naive DeltaT  2cH", 2*c*H0), ("framework cH/Z", c*H0/Z),
                  ("Milgrom cH/2pi", c*H0/(2*np.pi)), ("observed", a0_obs)]:
        print(f"     {nm:18} = {a:.2e}  ({a/a0_obs:5.2f}x obs)")
    print(f"""  VERDICT: spread {2*c*H0/(c*H0/(2*np.pi)):.0f}x (2cH..cH/2pi). The geometry explains why a0~1e-10 (cosmic), NOT why it
  is 1.2 vs 6.5 e-10. The exact value -- the coefficient Z -- is UNPREDICTED. A real, quantified weakness.\n""")


def attack2():
    print("="*92); print("ATTACK 2 -- the 'three independent readings' are NOT independent"); print("="*92)
    print("""  Horizon-coincidence, Unruh-floor, and cosmic-free-fall-time are three RESTATEMENTS of the single
  dimensional fact a0 ~ cH -- not three independent confirmations of it. (Honest correction to the deep
  dive's wording.) They are pedagogically distinct but carry the same one bit of physics: a0 is a
  cosmic-horizon-scale acceleration. The strength of that bit is exactly Attack-1's ~1 dex.\n""")


def attack3():
    print("="*92); print("ATTACK 3 [THE BIG ONE] -- WHICH horizon? apparent (evolving) vs event (constant)"); print("="*92)
    print("""  The rigorous Gibbons-Hawking temperature is the de Sitter EVENT-horizon temperature -> a0 prop
  sqrt(Lambda) = CONSTANT. This is the STANDARD emergent-gravity reading: Milgrom's a0 ~ c sqrt(Lambda/3),
  Verlinde's de Sitter entropy. The framework instead ties a0 to rho_crit = 3H^2/8piG (TOTAL density, the
  APPARENT/Hubble horizon) -> a0 prop H(z) -> EVOLVES. The two are indistinguishable at z=0 but diverge:""")
    print(f"     apparent-horizon a0(0)=cH0/Z      = {c*H0/Z:.2e}  (evolves as E(z))")
    print(f"     event-horizon    a0  =c H_Lambda/Z= {c*HL/Z:.2e}  (CONSTANT; differs at z=0 only by sqrt(OmL)={np.sqrt(OL):.2f})")
    print(f"     {'z':>4}{'a0 apparent (framework)':>26}{'a0 event (Milgrom/Verlinde)':>30}{'ratio':>8}")
    for z in (0, 1, 2, 3):
        ap, ev = c*H0/Z*E(z), c*HL/Z
        print(f"     {z:>4}{ap:>26.2e}{ev:>30.2e}{ap/ev:>8.2f}")
    print("""  THE TENSION, stated plainly: 'a0 comes from the horizon' does NOT force the evolution. The MORE
  STANDARD horizon (the event horizon / Lambda) gives CONSTANT a0; the framework's increase requires the
  APPARENT horizon. So the framework's signature claim is a CHOICE between two defensible horizons.
  FOR the apparent horizon (a real argument, not a fudge): local galaxy dynamics respond to the
  INSTANTANEOUS cosmic state (the Hubble horizon at that epoch), not the asymptotic future (the event
  horizon depends on the unknowable future expansion). Apparent-horizon thermodynamics (Cai-Kim 2005) is
  the standard FRW framework, with T=H/2pi on the Hubble sphere. So a0 prop H(z) is defensible -- but it
  is a bet, discriminated from the standard constant-Lambda reading by ~5x at z=3. (And SIV gives a THIRD
  answer, a0 DECREASING -- framework_vs_siv.py. The z~3 point separates all three.)\n""")


def attack4():
    print("="*92); print("ATTACK 4 -- the MECHANISM (horizon -> MOND) is posited, not derived"); print("="*92)
    print("""  The horizon COINCIDENCE is geometry; the claim that it CAUSES the MOND transition is a posited
  modified-INERTIA (Milgrom/McCulloch: inertia from the Unruh bath). The modified-GRAVITY version with the
  same temperature gives the WRONG sign (anti-MOND, clausius_sign_calculation.py); only an entropy/DOF
  modification gives MOND, and that piece is posited/contested. So 'the horizon makes MOND' is a hypothesis
  with a known sign-hazard and no complete action -- the standing open mechanism.\n""")


def robustness_pass():
    print("="*92); print("ROBUSTNESS PASS -- does a0 HAVE to be cosmic? (the part that SURVIVES)"); print("="*92)
    aP = np.sqrt(c**7/(hbar*G**2))
    print(f"  Planck acceleration = {aP:.1e} m/s^2; a0/aP = {a0_obs/aP:.1e}. The length giving a0 is c^2/a0 =")
    print(f"  {c**2/a0_obs/Mpc/1e3:.0f} Gpc -- COSMIC. No microphysical scale (QCD, electroweak, Planck) yields 1e-10 m/s^2.")
    print("  VERDICT: a0 MUST be cosmic-scale. The horizon origin SURVIVES for the magnitude -- robustly. PASS.\n")


def synthesis():
    print("="*92); print("SYNTHESIS -- what the stress test leaves standing"); print("="*92)
    print("""  SURVIVES (robust):  the MAGNITUDE. a0 ~ cH is forced -- a0 must be a cosmic-horizon-scale
     acceleration (no microphysics gives 1e-10). This is the real, durable geometric content.
  A BET (testable):   the EVOLUTION. a0 prop H(z) is the APPARENT-horizon reading (defensible by
     locality), but the standard EVENT-horizon reading gives CONSTANT a0 (Milgrom/Verlinde, sqrt(Lambda)),
     and SIV gives DECREASING. 'The horizon' does not pick one; the z~3 measurement does (the three
     diverge ~5x by z=3). The framework's distinctiveness IS this bet.
  UNPINNED:           the COEFFICIENT Z. Fixed only to ~1 dex (2cH..cH/2pi); the exact 5.79 is a posit.
  POSITED:            the MECHANISM. Horizon->MOND is modified inertia (temperature->anti-MOND for gravity);
     no complete action; the deep-MOND sign is the open problem.

  HONEST BOTTOM LINE: the geometric origin is REAL but NARROW -- it robustly explains the SCALE of a0 and
  nothing more. The evolution, the coefficient, and the mechanism are a testable bet, a posit, and an open
  problem respectively. The stress test does not break the framework, but it strips it to exactly one
  robust claim (a0 is cosmic-horizon-scale) plus one falsifiable bet (it tracks the APPARENT horizon, so
  it rises with z) -- and that bet, not the geometry, is what a z~3 measurement will confirm or kill.""")
    print("="*92)


def main():
    print("#"*92); print("# STRESS TEST: the geometric origin of a0 -- adversarial"); print("#"*92 + "\n")
    attack1(); attack2(); attack3(); attack4(); robustness_pass(); synthesis()


if __name__ == "__main__":
    main()
