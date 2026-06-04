#!/usr/bin/env python3
"""
The normalization-evolution LOCK: a0(0) and the a0(z) slope are not independent -- declining FORCES a0(0)~0.93.
=============================================================================================================
Carl's target: derive, from the two-horizon / density structure, a scale that is rho_total-normalized today
(a0(0)~1.2) but rho_DE-evolving (declining a0(z)). Taking a real run at it, the honest -- and deeper -- result
is that this CANNOT be done cleanly, because the normalization and the evolution are LOCKED together. That lock
turns the "22% normalization tension" from a free knob into a falsifiable, linked PREDICTION.

THE FAMILY. The most general natural two-component scale is a0 ~ sqrt(rho_total) * OmegaLambda(z)^beta, with
OmegaLambda(z) = OmegaLambda/E(z)^2 the dark-energy FRACTION (it weights the total density toward the dark
energy). This interpolates: beta=0 is the apparent horizon (sqrt(rho_total), rising); beta=1/2 is the event
horizon (sqrt(rho_DE), constant for constant Lambda); beta>1/2 weights dark energy more (declining). Then
        a0(z)  ~  OmegaLambda^beta  *  E(z)^(1 - 2 beta),
so the EVOLUTION exponent is (1 - 2 beta) and the z=0 NORMALIZATION is a0(0) = a0_apparent * OmegaLambda^beta.
ONE parameter beta sets BOTH. They are locked.

THE LOCK.
   rising   (beta < 1/2): a0(0) up to 1.12 (apparent), a0(z) rises   -- disfavored by the high-z disks
   constant (beta = 1/2): a0(0) = 1.12 * sqrt(OmegaLambda) = 0.93     -- the event-horizon value
   declining(beta > 1/2): a0(0) < 0.93, a0(z) declines               -- the data-favored shape
  => a0(0) = 1.2 is INTRINSICALLY the rising (apparent) value. You cannot have a0(0)=1.2 AND a declining a0(z)
     from any single-density principle. DECLINING FORCES a0(0) <= 0.93. (And the DESI evolving-DE form
     a0 = (c/2)sqrt(G rho_DE(z)) gives a0(0)=0.93 with declining, the same lock by a different mechanism.)

THE PREDICTION (the payoff -- the tension becomes falsifiable, not free). Accepting the high-z data (a0 not
rising) LOCKS a0(0) ~ 0.93e-10, NOT 1.2. The framework does not get to tune 1.2; it PREDICTS a0(0) ~ 0.93,
equivalently a stellar mass-to-light ratio Upsilon_disk ~ 0.6-0.7 (vs the canonical 3.6um value 0.5), since
the RAR has a0 ~ 1/Upsilon. This is testable two ways: (1) a precise, M/L-controlled a0 measurement -- 0.93 or
1.2? (2) independent stellar-population Upsilon_disk -- 0.5 or 0.65? Forcing 1.2 + declining would require a
hybrid (apparent normalization + event evolution) with no single-density principle -- overfitting, which we do
not do.

NET: the real run did not produce a fitted form for 1.2 + declining -- it produced a structural LOCK that makes
the normalization a falsifiable linked prediction (declining => a0(0)~0.93 => Upsilon~0.65). A cleaner, more
honest result than a tuned coefficient. Needs numpy.
"""
import numpy as np

Om, OL = 0.315, 0.685
E = lambda z: np.sqrt(Om*(1+z)**3 + OL)
c = 2.998e8; G = 6.674e-11; H0 = 67e3/3.086e22; Z = 2*np.sqrt(8*np.pi/3)
A0_APP = c*H0/Z/1e-10     # apparent normalization ~ 1.12


def main():
    print("#"*92)
    print("# The normalization-evolution LOCK: declining a0(z) FORCES a0(0) ~ 0.93, not 1.2")
    print("#"*92 + "\n")

    print("="*92); print("THE FAMILY: a0 ~ sqrt(rho_total)*OmegaLambda(z)^beta = OmegaLambda^beta * E(z)^(1-2beta)"); print("="*92)
    print(f"  ONE knob beta sets BOTH the evolution exponent (1-2beta) AND the z=0 value (a0_apparent*OL^beta):")
    print(f"  {'beta':>6}{'horizon/weight':>20}{'evolution':>14}{'a0(0) e-10':>13}{'a0(2)/a0(0)':>14}")
    for b, lab in [(0.0, "apparent rho_tot"), (0.25, "mixed"), (0.5, "event rho_DE"),
                   (0.75, "DE-weighted"), (1.0, "strong DE")]:
        print(f"  {b:>6.2f}{lab:>20}{'E^%+.1f'%(1-2*b):>14}{A0_APP*OL**b:>13.2f}{E(2.0)**(1-2*b):>14.2f}")
    print()

    print("="*92); print("THE LOCK"); print("="*92)
    print(f"""  a0(0) = 1.2 is intrinsically the RISING (apparent) value. A DECLINING a0(z) requires beta>1/2, which
  forces a0(0) < a0_apparent*sqrt(OmegaLambda) = {A0_APP*np.sqrt(OL):.2f}e-10. Normalization and evolution are NOT
  independent -- one parameter sets both. You cannot have a0(0)=1.2 AND declining from any single-density scale.
  (The DESI evolving-DE form a0=(c/2)sqrt(G rho_DE(z)) gives the same: a0(0)={A0_APP*np.sqrt(OL):.2f}, declining.)\n""")

    print("="*92); print("THE PREDICTION (the tension becomes falsifiable, not a free knob)"); print("="*92)
    a0_pred = A0_APP*np.sqrt(OL)
    ups = 0.5*1.20/a0_pred
    print(f"  Accepting the high-z data (a0 NOT rising) LOCKS a0(0) ~ {a0_pred:.2f}e-10. The framework PREDICTS this --")
    print(f"  it does not tune 1.2. Equivalent prediction: stellar M/L Upsilon_disk ~ {ups:.2f} (vs canonical 0.5),")
    print(f"  since the RAR has a0 ~ 1/Upsilon. Falsifiable two ways:")
    print(f"    (1) a precise, M/L-controlled a0 measurement: {a0_pred:.2f} or 1.20?")
    print(f"    (2) independent stellar-population Upsilon_disk: ~0.5 or ~{ups:.2f}?")
    print(f"  (Upsilon is approximate -- only the stellar part of g_bar scales with it; gas does not -- so read it")
    print(f"   as 'somewhat above 0.5', ~0.6-0.7.)\n")

    print("="*92); print("VERDICT"); print("="*92)
    print(f"""  The real run did not yield a fitted form for 1.2 + declining -- it yielded a structural LOCK: the
  normalization a0(0) and the evolution slope are tied by one parameter (which density/horizon weight), so a
  declining a0(z) FORCES a0(0) ~ {a0_pred:.2f}e-10, never 1.2. That converts the '22% normalization tension' from a free
  knob into a falsifiable, linked PREDICTION: if a0 is not rising (the high-z data), then a0(0) ~ 0.93 and
  Upsilon_disk ~ 0.65. Forcing 1.2 + declining needs a hybrid with no single-density principle -- overfitting,
  which we refuse. So the honest target was unreachable, and that is the result: the framework predicts a
  specific (low) a0(0) locked to the declining shape, not a tunable 1.2. A telescope (precise a0) or a stellar-
  population M/L decides it.""")
    print("="*92)


if __name__ == "__main__":
    main()
