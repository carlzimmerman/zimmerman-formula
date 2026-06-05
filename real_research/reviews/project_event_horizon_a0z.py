#!/usr/bin/env python3
"""
A DOOR found by trying hard: a0 tied to the INSTANTANEOUS event horizon -> mild, distinctive, DATA-VIABLE a0(z).
================================================================================================================
The framework's evolving claim uses the APPARENT/Hubble horizon: a0 proportional 1/R_H = H(z)/c -> a0(z=2)=3.0 a0,
which the published tests (Milgrom 2017 'all but excludes ~4 a0 at z~2'; Limbach 2008 favors constant/sqrt-Lambda)
DISFAVOR. The geometric/constant version (a0 proportional sqrt(Lambda)) is safe but not distinctive. I claimed last
turn you cannot have BOTH. That was wrong -- there is a THIRD prescription the repo MISSED:

  The repo (apparent_vs_event_discriminators.py) treated the EVENT horizon as EQUIVALENT to constant (a0 ~ sqrt
  Lambda). But that is only the event horizon's ASYMPTOTIC (t->inf) value. The INSTANTANEOUS event-horizon radius
  R_e(z) = a c integral_t^inf dt'/a  SHRINKS in the past, so a0 ~ 1/R_e(z) gives a MILD evolution -- a0(z=2)=1.47,
  not flat. This is a genuine third option BETWEEN the disfavored Hubble version (3.0) and the not-distinctive
  constant version (1.0).

WHY THE EVENT HORIZON IS PRINCIPLED (not cherry-picked): holographic dark energy (Li 2004, hep-th/0403127) shows the
Hubble-horizon IR cutoff gives the WRONG equation of state (Hsu/Li: rho~H^2 -> w=0, no acceleration), and the FIX is
to use the future EVENT horizon as the IR cutoff. If a0 is the IR gravity scale (holographic / CKN-type), the event
horizon is the CORRECT choice for the same reason -- and it happens to give a data-viable a0(z).

RESULT: a0(event horizon)(z) = 1.09, 1.20, 1.47, 1.76 at z=0.5,1,2,3 -- DISTINCTIVE (evolves; testable at z~3 where
it predicts 1.76 vs constant 1.0 vs Hubble 4.6) AND VIABLE (1.47 at z=2 is far below Milgrom's ~4; ~1.24 at z=1.2 is
near Limbach's favored constant). Honest costs: the event horizon is teleological (depends on the infinite future --
the known cost of holographic DE); the evolution is milder so harder to distinguish from constant; it requires the
event-horizon (holographic) prescription over the apparent-horizon (Cai-Kim thermodynamic) one. Needs numpy, scipy.
"""
import numpy as np
from scipy.integrate import quad

Om,OL=0.315,0.685; c=2.998e8; Mpc=3.086e22; H0=67.4e3/Mpc; Z=2*np.sqrt(8*np.pi/3)
Ea=lambda a: np.sqrt(Om*a**-3+OL); E=lambda z: Ea(1/(1+z))
chi_event=lambda a: quad(lambda ap: 1/(ap**2*Ea(ap)), a, np.inf)[0]
def Re(z): a=1/(1+z); return a*chi_event(a)          # instantaneous event horizon, units c/H0


def main():
    print("#"*100); print("# The event-horizon door: a mild, distinctive, DATA-VIABLE a0(z) the repo collapsed to 'constant'"); print("#"*100+"\n")
    Re0=Re(0)
    print("="*100); print("(1) the THREE prescriptions for a0(z)/a0(0)  (a0 ~ 1/R_horizon)"); print("="*100)
    print(f"  {'z':>4}{'Hubble/apparent (=E)':>22}{'EVENT horizon':>15}{'constant (sqrtLam)':>20}")
    for z in (0,0.5,1,1.2,2,3):
        print(f"  {z:>4}{E(z):>22.2f}{Re0/Re(z):>15.2f}{1.00:>20.2f}")
    print(f"  (event horizon today R_e(0)={Re0:.3f} c/H0 ~ de Sitter radius {1/np.sqrt(OL):.3f} within 5% -> matches")
    print(f"   the geometric core a0=c^2 sqrt(Lambda/32pi) at z=0, and -> it exactly as t->inf.)\n")

    print("="*100); print("(2) is the EVENT-horizon version consistent with the published tests that kill the Hubble one?"); print("="*100)
    print(f"   Milgrom 2017: 'all but excludes ~4 a0 at z~2'.   event-horizon a0(z=2) = {Re0/Re(2):.2f}  -> SAFE (<<4).")
    print(f"   Limbach 2008: favors constant/sqrt(Lambda) (tested to z=1.2). event a0(z=1.2)={Re0/Re(1.2):.2f} ~ near constant -> consistent.")
    print(f"   Hubble version for comparison: a0(z=2)=E(2)={E(2):.2f} (near the ~4 line, disfavored); a0(z=1.2)={E(1.2):.2f}.\n")

    print("="*100); print("(3) is it still DISTINCTIVE / testable? YES -- a specific z~3 prediction between the extremes"); print("="*100)
    print(f"   at z=3:  Hubble {E(3):.2f}  vs  EVENT {Re0/Re(3):.2f}  vs  constant 1.00  -- three DISTINCT predictions.")
    print(f"   the same z~3 deep-MOND disc test separates all three; the event version predicts a0 ~{Re0/Re(3):.1f}x today.\n")

    print("="*100); print("VERDICT -- a genuine door, with honest costs"); print("="*100)
    print(f"""  Trying hard found a real third option the repo missed by approximating the event horizon as its constant
  asymptotic value. Tying a0 to the INSTANTANEOUS event horizon (the PRINCIPLED holographic IR cutoff, Li 2004 --
  the same fix holographic dark energy uses because the Hubble cutoff fails) gives a MILD, DISTINCTIVE, DATA-VIABLE
  evolution: a0(z=2)=1.47, a0(z=3)=1.76 -- distinct from both the disfavored Hubble version (3.0/4.6) and the
  not-distinctive constant (1.0), and consistent with Milgrom 2017 and Limbach 2008 (which kill the Hubble version).
  This CORRECTS my 'can't have distinctive AND safe' claim: the event-horizon formulation IS both. HONEST COSTS:
  (i) the event horizon is teleological (depends on the infinite future -- holographic DE's known cost); (ii) the
  evolution is mild, so harder to distinguish from constant than the Hubble version was (but still a specific z~3
  prediction); (iii) it requires the event-horizon (holographic) prescription over the apparent-horizon (Cai-Kim
  thermodynamic) derivation the framework originally used. Net: the distinctive claim is NOT dead -- it just lives
  on the EVENT horizon, not the Hubble horizon, and there it survives the current data. That is the door.""")
    print("#"*100)


if __name__=="__main__":
    main()
