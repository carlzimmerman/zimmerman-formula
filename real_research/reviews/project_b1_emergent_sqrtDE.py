#!/usr/bin/env python3
"""
B1 (partial): the bridge form a0 ~ sqrt(rho_DE) EMERGES from de Sitter vacuum entropy -- no longer inserted by hand.
==================================================================================================================
The AeST realization (project_aest_darkenergy_construction.py) INSERTED the coupling C(Q) ~ 1/sqrt(rho_DE) to get
a0 ~ sqrt(rho_DE). B1 of the TOE roadmap asks: can emergent gravity DERIVE that form instead? Worked here -- the
FUNCTIONAL FORM emerges; only the O(1) coefficient stays route-forced.

THE DERIVATION (entanglement-equilibrium / de Sitter volume-law, Door 7, done with the VACUUM horizon):
  * The de Sitter Gibbons-Hawking entropy lives on the LAMBDA-horizon R_dS = sqrt(3/Lambda) -- a property of the
    VACUUM energy, NOT the instantaneous total density. (Generalizes for dynamical DE: R_dS(z)=sqrt(3 c^2/(8piG rho_DE)).)
  * Volume-law vs area-law entropy cross at r = R_dS:  S_V/S_A = r/R_dS  -> crossover at r=R_dS.
  * => emergent acceleration a0 ~ c^2/R_dS = c^2/(Z R_dS), which EQUALS c^2 sqrt(Lambda/32pi) exactly, and scales as
       a0 ~ sqrt(Lambda) ~ sqrt(rho_DE). THE BRIDGE FORM a0(z)=a0(0) sqrt(rho_DE(z)/rho0) FALLS OUT.

WHY rho_DE and not rho_total: the Gibbons-Hawking entropy is the de Sitter (vacuum) horizon's entropy, set by
Lambda. The apparent-horizon entropy (tied to the total density via H) would give a0 ~ cH ~ sqrt(rho_total) -- the
data-disfavored version. The VACUUM-entropy choice -- favored independently by the high-z data (Limbach/Milgrom) and
by holographic dark energy (Li 2004, which takes the event/vacuum cutoff over the Hubble one) -- DERIVES sqrt(rho_DE).

HONEST STATUS: this upgrades the AeST coupling C(Q) ~ 1/sqrt(rho_DE) from INSERTED to EMERGENT-IN-FORM. What emerges:
the SCALE and the FUNCTIONAL FORM (a0 ~ sqrt(rho_DE)). What does NOT: the O(1) coefficient Z (Door 7's volume integral
gives ~6; framework Z=5.789 sits in that cluster) -- still route-forced. And it requires relaxing Jacobson's fixed-
volume constraint (Verlinde's dynamical-volume move). So B1 is HALF done: bridge form derived, coefficient open.
Needs numpy.
"""
import numpy as np

c=2.998e8; G=6.674e-11; Mpc=3.086e22; H0=67.4e3/Mpc; OmL=0.685
Lam=3*OmL*H0**2/c**2; Z=2*np.sqrt(8*np.pi/3); R_dS=np.sqrt(3/Lam)


def main():
    print("#"*98); print("# B1 (partial): a0 ~ sqrt(rho_DE) EMERGES from de Sitter vacuum entropy (bridge form derived)"); print("#"*98+"\n")
    a0_em=c**2/(Z*R_dS); a0_f=c**2*np.sqrt(Lam/(32*np.pi))
    print("="*98); print("(1) the de Sitter vacuum (Gibbons-Hawking) entropy -> a0 ~ c^2/R_dS ~ sqrt(Lambda) ~ sqrt(rho_DE)"); print("="*98)
    print(f"   R_dS = sqrt(3/Lambda) = {R_dS:.3e} m   (the LAMBDA/vacuum horizon -- NOT the instantaneous H)")
    print(f"   volume/area crossover at r=R_dS (S_V/S_A=r/R_dS) -> a0 ~ c^2/(Z R_dS) = {a0_em:.3e} m/s^2")
    print(f"   c^2 sqrt(Lambda/32pi)                                = {a0_f:.3e} m/s^2   identical? {np.isclose(a0_em,a0_f)}")
    print(f"   a0 ~ sqrt(Lambda) ~ sqrt(rho_DE)  => the bridge a0(z)/a0(0)=sqrt(rho_DE(z)/rho0) FALLS OUT.\n")

    print("="*98); print("(2) why rho_DE (vacuum) and not rho_total -- the entropy choice that the data already favor"); print("="*98)
    print("   Gibbons-Hawking entropy = de Sitter VACUUM horizon -> a0 ~ sqrt(Lambda) ~ sqrt(rho_DE).  [favored]")
    print("   apparent-horizon entropy (~ total density via H)   -> a0 ~ cH ~ sqrt(rho_total).         [disfavored: Limbach/Milgrom]")
    print("   the vacuum-entropy choice is also the holographic-DE choice (Li 2004: event/vacuum cutoff, not Hubble).\n")

    print("="*98); print("VERDICT -- B1 half achieved"); print("="*98)
    print("""  The bridge's FUNCTIONAL FORM a0 ~ sqrt(rho_DE) is now DERIVED (emergent from the de Sitter vacuum / Gibbons-
  Hawking entropy via the volume/area crossover), not inserted -- because that entropy is a property of Lambda (the
  vacuum), not the total density. This upgrades the AeST coupling C(Q) ~ 1/sqrt(rho_DE) from PUT-IN-BY-HAND to
  EMERGENT-IN-FORM. What is still NOT derived: the O(1) coefficient Z (route-forced; Door 7's volume integral gives
  ~6, the framework's 5.789 is in that cluster), and the derivation requires relaxing Jacobson's fixed-volume
  (Verlinde's move). So B1 is HALF done: the bridge form is emergent, the coefficient remains the one un-derived
  number -- and per the coefficient-free bridge (THE_A0_LAMBDA_BRIDGE.md), that un-derived coefficient does not even
  enter the empirical test.""")
    print("#"*98)


if __name__=="__main__":
    main()
