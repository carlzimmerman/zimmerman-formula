#!/usr/bin/env python3
"""
Developing the event-horizon door: consistency re-check (IMPROVES) + the DESI/holographic extension (does NOT pan out).
=====================================================================================================================
The event-horizon a0(z) (THE_EVENT_HORIZON_DOOR.md) is mild, distinctive, and data-viable. Two follow-ups, honestly:

PART 1 -- CONSISTENCY RE-CHECK vs the Hubble version (CMB/clusters/sigma8). RESULT: a genuine IMPROVEMENT.
  * CLUSTERS: the residual D = M_dyn/M_MOND ~ a0 (fixed kinematics), so D(z)/D0 = a0(z)/a0(0). The event version
    rises x1.20 (z=1), x1.47 (z=2) vs the Hubble version's x1.79, x3.03 -- the cluster strike is MUCH SOFTER.
  * CMB: a0(event, z=1100) is still ~300x today, but a0 is absent from the LINEAR equations (O(delta^3) gradient
    suppression) regardless of its value -> CMB-safe at linear order by the SAME proof (project_cmb_boltzmann_aest).
  * sigma8: the EFE-freezing argument (a_H/a0 = Z, frozen) BREAKS for the event version (a0 no longer tracks H, so
    a_H/a0 rises 1.0,1.5,2.1 at z=0,1,2) -- but sigma8 stays neutral via the SAME O(delta^3) suppression. Honest:
    one protective mechanism instead of two; still neutral.

PART 2 -- the DESI extension. The event horizon IS the holographic-DE IR cutoff (Li 2004). IF the framework went
  FULLY holographic (rho_DE ~ 1/R_e^2, dynamical), the SAME structure would set a0 AND the dark-energy w(z), giving
  a now-testable prediction vs DESI 2024. RESULT: it does NOT pan out. Standard event-horizon holographic DE gives
  w = -(1/3)(1 + 2 sqrt(Omega_DE)/c_h): w0 ~ -0.89 (c_h=1), in DESI's ballpark, BUT wa ~ +0.23 (POSITIVE) -- a
  'thawing' history (w: -1/3 -> -1). DESI wants wa = -0.75 (NEGATIVE, phantom-crossing). OPPOSITE evolution. So no
  DESI bonus; the event-horizon a0 door stands on a LCDM (constant-Lambda) background only. Needs numpy, scipy.
"""
import numpy as np
from scipy.integrate import quad

Om,OL=0.315,0.685
Ea=lambda a: np.sqrt(Om*a**-3+OL); E=lambda z: Ea(1/(1+z))
chi_event=lambda a: quad(lambda ap: 1/(ap**2*Ea(ap)), a, np.inf)[0]
Re=lambda z:(1/(1+z))*chi_event(1/(1+z)); Re0=Re(0)
a0e=lambda z: Re0/Re(z)
w_holo=lambda OmDE,ch: -(1/3)*(1+2*np.sqrt(OmDE)/ch)


def main():
    print("#"*98); print("# Developing the event-horizon door: consistency (IMPROVES) + DESI extension (FAILS)"); print("#"*98+"\n")

    print("="*98); print("(1) CONSISTENCY RE-CHECK -- the event version is MILDER on clusters, still CMB-safe + sigma8-neutral"); print("="*98)
    print(f"   CLUSTERS  residual D(z)/D0 = a0(z)/a0(0):   {'z':>4}{'Hubble (=E)':>14}{'EVENT':>9}")
    for z in (0.5,1,2): print(f"   {'':38}{z:>4}{E(z):>14.2f}{a0e(z):>9.2f}")
    print(f"   -> event-horizon cluster strike is much softer (x1.47 vs x3.03 at z=2). GENUINE IMPROVEMENT.")
    print(f"   CMB:    a0(event,z=1100)/a0(0) = {a0e(1100):.0f}, but a0 is O(delta^3) -> absent from linear eqns -> CMB-safe (same proof).")
    print(f"   sigma8: a_H/a0 (rel) = {E(0)/a0e(0):.2f},{E(1)/a0e(1):.2f},{E(2)/a0e(2):.2f} at z=0,1,2 -> EFE-freezing BREAKS, but O(delta^3) keeps sigma8 neutral.\n")

    print("="*98); print("(2) DESI extension: event horizon = holographic-DE cutoff (Li 2004) -- does the w(z) match DESI?"); print("="*98)
    print(f"   {'c_h':>6}{'w0 (holo)':>12}{'wa (holo)':>12}")
    for ch in (0.8,1.0):
        dOm=OL*(1-OL)*(1+2*np.sqrt(OL)/ch); wa=-(-(1/3)*(1/np.sqrt(OL))/ch)*dOm
        print(f"   {ch:>6}{w_holo(OL,ch):>12.2f}{wa:>12.2f}")
    print(f"   DESI 2024 (BAO+CMB+DESY5):  w0 = -0.83 +/- 0.08,   wa = -0.75 +/- 0.25")
    print(f"   => w0 in the ballpark, but holographic wa is POSITIVE (thawing, w:-1/3->-1) while DESI wa is NEGATIVE")
    print(f"      (phantom-crossing). OPPOSITE evolution -> the DESI extension FAILS. Door stands on LCDM only.\n")

    print("="*98); print("VERDICT"); print("="*98)
    print("""  Developed honestly, the event-horizon door is CONSOLIDATED and in one respect IMPROVED: its cluster tension is
  much milder than the Hubble version's (x1.47 vs x3.03 at z=2), and it remains CMB-safe at linear order and
  sigma8-neutral (now via O(delta^3) suppression alone, since EFE-freezing is specific to the Hubble version). The
  tempting extension -- going fully holographic so the SAME event-horizon structure sets a0 AND a DESI-testable w(z)
  -- does NOT work: standard holographic DE evolves the wrong way (wa>0 thawing vs DESI's wa<0 crossing). So the
  event-horizon a0 door stands on a constant-Lambda (LCDM) background, with NO bonus DESI connection. Net: a real,
  consolidated, somewhat-improved distinctive formulation -- still resting on the single z~3 test, now with the
  added bonus that it is gentler on clusters than the version the data already disfavored.""")
    print("#"*98)


if __name__=="__main__":
    main()
