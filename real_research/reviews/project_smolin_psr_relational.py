#!/usr/bin/env python3
"""
THE SMOLIN / SUFFICIENT-REASON DOOR: reread the apparent-vs-event a0 under PSR + relationalism.
==============================================================================================
Proceeding on Lee Smolin's principles (Principle of Sufficient Reason; relationalism/Mach; the reality of
time). These are METHODOLOGICAL priors -- serious physics, not data -- and they MATERIALLY change the reading
of the framework: all three favor the RISING / relational a0, and they REVERSE the 'tilt toward constant'
that project 3d derived from a (non-relational) local-realizability criterion. The non-locality 3d flagged as
an obstruction becomes the Machian FEATURE. Honest about status: this strengthens the THEORETICAL prior for
the distinctive bet; it does not settle the data (gas-limited) or the still-underived coefficient Z (a
standing PSR-failure). Needs numpy.
"""
import numpy as np

c, Mpc = 2.99792458e8, 3.0857e22
H0 = 67.4e3/Mpc
Z = 2*np.sqrt(8*np.pi/3)
Om, OL = 0.315, 0.685
E = lambda z: np.sqrt(Om*(1+z)**3 + OL)


def main():
    print("#"*92); print("# THE SMOLIN / SUFFICIENT-REASON DOOR -- a0 under PSR + relationalism"); print("#"*92 + "\n")

    print("="*92); print("PRINCIPLE 1 -- the Principle of Sufficient Reason (no brute facts)"); print("="*92)
    print(f"""  PSR: every fact about the universe must have a rational reason; nothing is arbitrary.
    * CONSTANT a0 = c sqrt(Lambda)/Z ties the MOND scale to LAMBDA -- the single most PSR-VIOLATING number in
      physics (the cosmological-constant problem: Lambda's value is unexplained at ~120 orders of magnitude).
      Tying a0 to Lambda inherits the deepest brute fact we have.
    * RISING a0 = cH(z)/Z ties a0 to the ACTUAL cosmic density rho(z) = 3H^2/8piG -- a relational fact about
      what IS present, evolving with it. a0 is then EXPLAINED by the cosmic state, not by a brute constant.
  => PSR PREFERS the rising/relational reading. (Observed a0={1.2:.1f}e-10 = c H0/{c*H0/1.2e-10:.1f}.)\n""")

    print("="*92); print("PRINCIPLE 2 -- relationalism / Mach (local set by global)"); print("="*92)
    print("""  Leibniz-Mach: properties are relational; local inertia/dynamics are fixed by the whole universe, not by
  a fixed background. a0 = cH/Z literally says a LOCAL acceleration scale is set by the GLOBAL cosmic horizon
  -- a textbook Machian statement. The concrete mechanism is the Deser-Levin cosmic-horizon Unruh floor
  T(a) = (hbar/2pi c k) sqrt(a^2 + (cH)^2): every system, however isolated, feels a residual ~cH from the
  horizon. THIS IS THE KEY REFRAME OF PROJECT 3d:
    * 3d found NO LOCAL covariant field reproduces a0=cH/Z inside galaxies (theta->0, R->R_local) and called
      it a 'tilt toward constant a0'. But that verdict used a NON-relational criterion -- local realizability.
    * Under Mach, a0 is RELATIONAL by nature (set by the global horizon), so it SHOULD be non-local; the
      absence of a local realization is the Machian SIGNATURE, not a defect. The honest 'escape' 3d named (the
      cosmic external field) is, under relationalism, the CORRECT realization, not a fallback.
  => relationalism REVERSES 3d: the rising/relational a0 is the principled reading; non-locality is the feature.\n""")

    print("="*92); print("PRINCIPLE 3 -- the reality of time (constants can evolve)"); print("="*92)
    print(f"""  Smolin: time is fundamental, not emergent; laws/constants can evolve. Then a0(z) = a0(0) E(z) EVOLVING
  with cosmic time (E(2) = {E(2):.2f}, E(3) = {E(3):.2f}) is natural -- a0 is a feature of the present cosmic state. A
  CONSTANT a0 is a FROZEN parameter -- the timeless block-universe picture Smolin rejects. => favors rising.\n""")

    print("="*92); print("THE PSR DEMAND ON Z (honest -- a standing failure, not resolved)"); print("="*92)
    a0_cleanZ2 = c*H0/2
    print(f"""  PSR cuts both ways: it also DEMANDS the coefficient Z be DERIVED, not posited. Here the framework does
  NOT yet satisfy PSR:
    * the CLEAN, reasoned value -- a0 = surface gravity of the Hubble horizon = c^2/2R_H = cH/2 -- gives Z=2,
      a0 = {a0_cleanZ2*1e10:.2f}e-10; but OBSERVED a0 = 1.2e-10 needs Z = {c*H0/1.2e-10:.1f}.
    * the extra factor sqrt(8pi/3) ~ {np.sqrt(8*np.pi/3):.2f} (from the choice R* = c/sqrt(G rho) rather than the Hubble radius)
      is NOT yet sufficiently reasoned -- R* is a dimensional combination, not a clean horizon (escape velocity
      there is c sqrt(8pi/3) ~ 2.9c, not c).
  => Z = 2 sqrt(8pi/3) = {Z:.2f} remains a brute coefficient = a PSR-FAILURE. The DSSYK coefficient calculation
     (project 4c: c1, lambda_dS, T_dS/E0) is the PSR-mandated derivation, and it is still open. PSR sharpens
     the demand; it does not, by itself, supply Z.\n""")

    print("="*92); print("VERDICT"); print("="*92)
    print("""  Under Smolin's principles -- the ones requested -- the framework's DISTINCTIVE bet is the THEORETICALLY
  PREFERRED reading: rising/relational a0 satisfies PSR (explained by the cosmic state, not brute Lambda), is
  Machian (local scale from the global horizon, with a concrete Deser-Levin mechanism), and fits the reality
  of time (an evolving a0). This REVERSES project 3d: its 'tilt to constant' rested on local realizability,
  which relationalism rejects -- non-locality is the Machian feature, and the cosmic-external-field realization
  is the correct one. HONEST BOUNDS: (1) this is a principled PRIOR, not data -- the gas-limited galaxy data
  are unchanged, and someone who takes Lambda as fundamental will prefer constant a0; (2) PSR equally DEMANDS
  the coefficient Z, which the framework does NOT yet supply (Z=5.79 is brute; the clean Z=2 is wrong by 2.9x)
  -- a standing PSR-failure pointing straight at the open DSSYK coefficient calc. Net: under sufficient reason
  the rising bet is theory-FAVORED and the real unfinished business is DERIVING Z -- exactly where to push next.""")
    print("="*92)


if __name__ == "__main__":
    main()
