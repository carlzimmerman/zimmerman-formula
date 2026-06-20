#!/usr/bin/env python3
"""
CRUX (ii)-B, CORRECTED with the RIGHT template: the framework's cold component is
AeST's cosmological scalar, which the literature (Skordis-Zlosnik 2021; arXiv:2308.00342
verbatim) says evolves as "shift-symmetric k-essence (Scherrer 2004): energy density
~ (1+z)^3 PLUS small DECAYING corrections" -- i.e. EXACTLY 'w=0 at leading order +
gradient corrections'. So the controlling template is SCHERRER 2004 (astro-ph/0402316),
NOT the bare GDM tuning.

SCHERRER 2004 (purely kinetic k-essence as unified dark matter), verbatim equations
(extracted /tmp/scherrer.txt):
  * rho = -F0 + 4 F2 X0^2 eps1 (a/a1)^-3                              (Eq 22)  [dust + (-F0)=CC]
  * sound speed   c_s^2 = (X - X0)/(3X - X0)                          (Eq 23)
  * near extremum c_s^2 = (1/2) eps1 (a/a1)^-3                        (Eq 24)
  * KEY: "the sound speed can be made ARBITRARILY SMALL during the epoch of structure
    formation by DECREASING the value of eps1" -> "indistinguishable from LCDM in that
    particular problem". c_s^2 << 1 for the entire range of validity.

THE DECISIVE STRUCTURAL POINT (both ways):
  c_s^2 at structure formation is set by the FREE amplitude eps1, NOT by M alone.
  - The bare-GDM bound M >~ 10 eV (Furukawa-Yokoyama-Ichiki 1001.4634 Eq 4.2) came from
    a SPECIFIC tuning: they FIXED X0 (and hence eps1) by demanding Omega_gdm=0.3 TODAY
    with the working Lagrangian P=(X-M^4)^2/8M^4, which ties c_s^2(eq) to M. That is ONE
    slice of the parameter space, not the general statement.
  - Scherrer's general result: eps1 (= the off-minimum displacement = the framework's
    FREE I0/amplitude, banked) is an INDEPENDENT knob. Decreasing eps1 makes c_s^2 -> 0
    at structure formation => the P(k) suppression is pushed to arbitrarily small scales.

So crux (ii)-B has a SHARP both-ways answer:
 (A) There IS a computable feature: c_s^2(a) = (1/2) eps1 a^-3 -> a Jeans cutoff in P(k).
 (B) Its scale/amplitude is controlled by the SAME FREE amplitude (eps1 ~ I0 ~ Omega_dm
     displacement) -- so it is NOT a parameter-free prediction. For the data-favored AeST
     point it is TUNED BELOW observable scales (CDM-degenerate). It only becomes a kill if
     you ALSO insist on a specific (non-free) c_s^2 -- which the framework does not.

This script quantifies: given the framework's M-window and the data-favored small-c_s
choice, WHERE is the residual P(k) feature, and is its amplitude ever in the S8 window?
"""
import numpy as np
c=2.99792458e8; G=6.67430e-11; Mpc=3.0856775814913673e22
h=0.674; H0=h*100e3/Mpc; Om_m=0.315
a_eq=1/3400.0
H_eq=H0*np.sqrt(Om_m*a_eq**-3*2.0)     # s^-1

print("="*82)
print("(1) c_s^2(a) = (1/2) eps1 a^-3  (Scherrer Eq 24) -- the gradient-correction pressure")
print("="*82)
print("  c_s^2 is COLD today, grows as a^-3 into the past. Jeans wavenumber k_J = sqrt(3/2) aH/c_s.")
print("  k_J is LARGEST (cutoff most damaging) at matter-radiation EQUALITY (then grows ~a in MD).")
print("  => the controlling number is c_s^2(a_eq) = (1/2) eps1 (a_eq/a1)^-3.")
print()
print("  Comoving Jeans wavenumber at equality:")
print("     k_J,eq(comoving) = sqrt(3/2) * a_eq * H_eq / (c_s(eq) * c)   [comoving Mpc^-1]")
print()

def kJ_eq_comoving_Mpc(cs2_eq):
    cs = np.sqrt(cs2_eq)           # in units of c
    kJ_phys = np.sqrt(1.5)*H_eq/(cs*c)   # physical m^-1
    kJ_com  = kJ_phys*a_eq               # comoving m^-1  (k_com = a k_phys)
    return kJ_com*Mpc                     # comoving Mpc^-1

print(f"  {'c_s^2(eq)':>12} | {'k_J,eq (Mpc^-1)':>15} | {'k_J,eq (h/Mpc)':>14} | {'lambda_J (Mpc)':>14}")
print("  "+"-"*64)
for cs2 in [1e-2,1e-4,1e-6,1e-8,1e-10,1e-12]:
    kJ=kJ_eq_comoving_Mpc(cs2)
    print(f"  {cs2:>12.0e} | {kJ:>15.4f} | {kJ/h:>14.4f} | {2*np.pi/kJ:>14.2f}")
print()
print("  Observed P(k) shows NO suppression for k/h <~ 1 Mpc^-1 (linear regime).")
print("  => REQUIRE k_J,eq >~ 1 h/Mpc  =>  c_s^2(eq) <~ a few x 1e-8.")
print("  This is a MILD bound on the FREE amplitude eps1; it does NOT bound M independently.")
print()

print("="*82)
print("(2) MAP c_s^2(eq) to the framework's parameters -- is the data-favored point natural?")
print("="*82)
# GDM's tuning (Omega_dm=0.3 today, P=(X-M^4)^2/8M^4) GIVES c_s^2(eq) tied to M:
#   from GDM Eq 4.2, k_J,eq = 1 Mpc^-1 (Om h2/0.11)^-5/6 (M/10eV)^4/3
#   invert to the IMPLIED c_s^2(eq) for that tuned slice:
def cs2_eq_from_M_GDMtuning(M_eV):
    kJ = 1.0*(0.121/0.11)**(-5/6)*(M_eV/10.0)**(4/3)   # Mpc^-1 comoving
    cs = np.sqrt(1.5)*a_eq*H_eq/( (kJ/Mpc)*c )           # back out c_s (units c)
    return cs**2
print("  On the GDM tuned slice (Omega_dm fixed today => c_s^2 tied to M):")
print(f"    {'M (eV)':>8} | {'c_s^2(eq) [GDM slice]':>22} | status")
for M_eV in [0.1,1.0,10.0,30.0,100.0]:
    cs2=cs2_eq_from_M_GDMtuning(M_eV)
    stat = "OK (k_J>1h/Mpc)" if cs2<3e-8 else "EXCLUDED (suppresses observed P(k))"
    print(f"    {M_eV:>8.2f} | {cs2:>22.3e} | {stat}")
print()
print("  => On THAT slice, M~0.1eV is excluded BECAUSE the tuning forces c_s^2(eq)~O(1).")
print("  BUT the framework does NOT use that slice: its dark-MATTER amplitude I0 (=eps1)")
print("  is the FREE off-minimum displacement (banked: d rho_dust/d Lambda=0; a^3 K'(Q)=I0).")
print("  Dialing eps1 DOWN (smaller displacement from the w=-1 minimum) lowers c_s^2(eq)")
print("  INDEPENDENTLY of M -> pushes k_J,eq above 1 h/Mpc -> CDM-degenerate. This is EXACTLY")
print("  what Skordis-Zlosnik 2021 do when they FIT Planck: the AeST cold mode is c_s~0,")
print("  the residual is 'small decaying corrections' (2308.00342 verbatim), not a cutoff.")
print()

print("="*82)
print("(3) S8 / sigma8: can the residual EVER land in the 5-8% therapeutic window?")
print("="*82)
print("  For c_s^2 small enough to pass P(k) at k<1 h/Mpc, the suppression at the sigma8")
print("  scale (k~0.2 h/Mpc) is, by construction, BELOW the cutoff => negligible.")
print("  To get a 5-8% sigma8 suppression at k~0.2 h/Mpc you'd need k_J,eq ~ 0.2 h/Mpc,")
print("  i.e. the cutoff RIGHT AT the sigma8 scale:")
kJ_target=0.2*h   # h/Mpc -> Mpc^-1
# invert kJ_eq_comoving to c_s^2:
cs_target=np.sqrt(1.5)*a_eq*H_eq/((kJ_target/Mpc)*c)
print(f"    k_J,eq = 0.2 h/Mpc = {kJ_target:.3f} Mpc^-1  =>  c_s^2(eq) ~ {cs_target**2:.2e}")
print("  But a cutoff AT 0.2 h/Mpc is a SHARP Jeans truncation, not a gentle 5-8% tilt:")
print("  Jeans suppression goes as exp/-(k/k_J)^2 type or a hard P->0 for k>k_J, so AT the")
print("  cutoff it removes ~ALL power above 0.2 h/Mpc -> sigma8 crashes by tens of %, and")
print("  k<0.2 h/Mpc is UNTOUCHED -> the SHAPE is wrong for S8 (data want a broadband ~8%")
print("  amplitude shift, not a knee at 0.2 h/Mpc + intact large scales + dead small scales).")
print("  Worse: a knee at 0.2 h/Mpc would also kill BAO wiggles at 0.05-0.3 h/Mpc and the")
print("  Lyman-alpha forest (k~1-10 h/Mpc) -> grossly excluded, not a tension cure.")
print()
print("  CONCLUSION (b): there is NO eps1 that gives a GENTLE, broadband 5-8% S8 relief.")
print("  Either c_s^2 is small (k_J>1h/Mpc) -> negligible/CDM-degenerate (honest null), or")
print("  c_s^2 is large enough to touch sigma8 -> a SHARP knee that over-suppresses + breaks")
print("  BAO/Lyman-alpha -> excluded. The GC-dust pressure is the WRONG SHAPE for S8.")
print()

print("="*82)
print("(4) ISW / late-time interplay with the w=-1 minimum")
print("="*82)
print("  - The exact minimum is w=-1 (the framework's Lambda/dark-energy face). The dust is")
print("    the displacement. Late-time, as Lambda comes to dominate, the dust c_s^2 (~a^-3)")
print("    is at its SMALLEST -> ISW from the dust's pressure is MINIMIZED exactly when ISW")
print("    matters (z<1). So the condensate's own late-time pressure ISW is NEGLIGIBLE.")
print("  - The genuine late-time/large-scale modification is the AeST mu-term (grad^2 Phi +")
print("    mu^2 Phi = src), a Yukawa/oscillatory Phi at r > mu^-1 ~ Mpc. It DOES touch large-")
print("    scale Phi (hence ISW + the lensing/cluster sector), but it is the SAME free mu")
print("    already in the ledger (the lensing/cluster scale), NOT a NEW distinctive number,")
print("    and Skordis-Zlosnik 2021 already fit Planck's low-l/ISW with it. No new front.")
print()

print("="*82)
print("NET (both ways)")
print("="*82)
print("  (a) c_s^2(k,a): YES computable -- c_s^2(eq)=(1/2)eps1 a_eq^-3 (Scherrer Eq 24), a")
print("      a^-3 cold-but-pressured dust with a Jeans cutoff k_J,eq. DEPARTS from w=0 at")
print("      k > k_J,eq. Real, not zero.")
print("  (b) S8/sigma8: the SIGN is right (suppresses small-scale growth) but the SHAPE and")
print("      AMPLITUDE are wrong -- it's a sharp Jeans KNEE controlled by the FREE eps1, not")
print("      a broadband ~8% tilt. Tuned safe (eps1 small) => negligible/CDM-degenerate;")
print("      tuned to touch sigma8 => over-suppresses + breaks BAO/Lyman-alpha. NO")
print("      therapeutic window. Does NOT relieve S8.")
print("  (c) ISW: the dust's own late-time pressure-ISW is minimized when ISW matters")
print("      (c_s^2~a^-3 smallest at low z). The only large-scale handle is the free AeST")
print("      mu-term, already in the ledger, already Planck-fit. No new ISW front.")
print()
print("  HONEST STATUS: crux (ii)-B is a NULL for a NEW distinctive front -- the feature is")
print("  real but its scale/amplitude rides the SAME free amplitude (eps1=I0) that already")
print("  makes the dark-matter AMOUNT free, so it is tunable to CDM-degeneracy and is what")
print("  AeST already does to fit Planck. It does NOT touch S8 (wrong shape). NOT a kill")
print("  either (the data-favored point is viable). Out-of-window/degenerate, by tuning the")
print("  already-free amplitude. Both ways: real-but-not-distinctive, not a bonus, not a kill.")
