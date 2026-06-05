#!/usr/bin/env python3
"""
The framework's deepest, coefficient-INDEPENDENT, falsifiable form: a0(z) and sqrt(rho_DE(z)) are the same curve.
================================================================================================================
Reasoning all the way down: the framework's LITERAL formula is a0 = c^2 sqrt(Lambda/32pi). That is neither H nor the
total density -- it is LAMBDA (the dark energy). The cH(z)/Z form (~sqrt rho_total) and the event-horizon form are
derivation ROUTES that equal c^2 sqrt(Lambda) only today and extrapolate differently; the faithful reading is the
formula as written: a0 tracks Lambda. (Supports: the literal formula; 'MOND as a vacuum effect' (Milgrom) -- a0 is a
vacuum property, matter is transient; the data, Limbach 2008/Milgrom 2017, disfavor the rising rho_total form; and
holographic DE (Li 2004) takes the event/vacuum cutoff over the Hubble one. The apparent-horizon route that gives
rho_total is legitimate but is the disfavored extrapolation.)

THE PAYOFF -- the empirical test SEPARATES cleanly into two pieces of very different cleanliness:
  (A) VALUE  test: a0(0) <-> Lambda_0. Coefficient-DEPENDENT (the route-forced 32pi); good only to ~30% in a0
      (~60% in Lambda). A consistency check, not a measurement. THIS is where the whole coefficient-forcing saga
      lives -- and it does NOT block the test below.
  (B) SHAPE  test: a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE0). The (c/2)sqrt(G) and the 32pi CANCEL in the ratio, so this
      is COEFFICIENT-INDEPENDENT. The framework's distinctive, falsifiable content is just: the galaxy-measured a0(z)
      curve and the cosmology-measured sqrt(rho_DE(z)) curve are IDENTICAL in shape. Either they match or it dies.

=> The framework's testability is DECOUPLED from the unsolved coefficient: you never need to derive 32pi to test it.
Needs numpy.
"""
import numpy as np

Om,OL=0.315,0.685; c=2.998e8; G=6.674e-11; Mpc=3.086e22; H0=67.4e3/Mpc
Lam0=3*OL*H0**2/c**2; a0_obs=1.2e-10
w0,wa=-0.752,-0.86                                   # DESI DR2
rhoDE=lambda a: a**(-3*(1+w0+wa))*np.exp(-3*wa*(1-a))


def main():
    print("#"*96); print("# a0 = c^2 sqrt(Lambda/32pi)  <=>  a0 IS the cosmological constant. The falsifiable bridge."); print("#"*96+"\n")

    print("="*96); print("(A) VALUE test -- coefficient-DEPENDENT (~30%); a consistency check, where the 32pi problem lives"); print("="*96)
    a0_pred=c**2*np.sqrt(Lam0/(32*np.pi))
    print(f"   a0(0) from cosmological Lambda = {a0_pred:.2e};  observed = {a0_obs:.2e}  -> off {100*(a0_obs/a0_pred-1):.0f}% (route-forced 32pi)")
    print(f"   => the VALUE bridge is a ~30% consistency check, NOT precise. The coefficient saga is confined HERE.\n")

    print("="*96); print("(B) SHAPE test -- coefficient-INDEPENDENT: the clean, distinctive, falsifiable bridge"); print("="*96)
    print("   a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE0)   [(c/2)sqrt(G) and 32pi cancel in the ratio]")
    print(f"   {'z':>4}{'a0(z)/a0(0)=sqrt(rho_DE)':>26}{'constant-Lambda null':>22}")
    for z in (1,2,3):
        print(f"   {z:>4}{np.sqrt(rhoDE(1/(1+z))):>26.3f}{1.00:>22.2f}")
    print("   => galaxy-measured a0(z) MUST equal cosmology-measured sqrt(rho_DE(z)), shape-to-shape, NO free coeff.\n")

    print("="*96); print("THE FALSIFICATION TABLE -- a one-to-one link between two INDEPENDENT measurements"); print("="*96)
    rows=[("Lambda constant (w=-1)","a0 constant","CONSISTENT (the safe core)"),
          ("Lambda constant (w=-1)","a0 evolves","FALSIFIED"),
          ("DE dynamical (DESI)","a0 ~ sqrt(rho_DE)","CONFIRMED (distinctive)"),
          ("DE dynamical (DESI)","a0 constant","FALSIFIED")]
    print(f"   {'cosmology (DESI/BAO) says':>26}   {'galaxies (a0(z)) say':>20}   verdict")
    for a,b,v in rows: print(f"   {a:>26}   {b:>20}   {v}")
    print()

    print("="*96); print("VERDICT"); print("="*96)
    print("""  The framework's deepest statement is a0 = c^2 sqrt(Lambda/32pi): the MOND scale IS the cosmological constant,
  written as a galactic acceleration. Its empirical content splits into (A) a coefficient-limited ~30% VALUE check
  -- the only place the unsolved 32pi matters -- and (B) a coefficient-INDEPENDENT SHAPE bridge: a0(z)/a0(0) =
  sqrt(rho_DE(z)/rho_DE0). The whole framework reduces to one falsifiable claim: the galaxy-measured a0(z) curve and
  the cosmology-measured sqrt(rho_DE(z)) curve are the SAME curve. This DECOUPLES the test from the coefficient
  problem -- you never need to derive 32pi to falsify or confirm the framework; you only need the two curves. It
  also makes the framework a bridge between galaxy dynamics and cosmology: a0(z) becomes an independent probe of
  dark-energy evolution, cross-checkable against DESI's w(z). Honest residue: the distinctive (declining) branch is
  contingent on DESI; under constant Lambda it is the safe constant null; and the decisive shape measurement needs
  z~3 resolved kinematics (the ~7% signal), which DESI cannot supply.""")
    print("#"*96)


if __name__=="__main__":
    main()
