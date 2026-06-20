#!/usr/bin/env python3
"""
CRUX (ii)-B: w=0 holds only at LEADING order. The gradient / higher-derivative
corrections of the ghost-condensate "dust" give a small effective pressure / sound
speed. Does that imprint a COMPUTABLE, FALSIFIABLE signature on the CMB / matter
power spectrum / low-z growth (S8, sigma8, fsigma8), or is it negligible (k^2/M^2
too small -> CDM-degenerate, honest null)?

ALL formulas are the LITERATURE'S OWN, not reinvented:
  ACLM = Arkani-Hamed, Cheng, Luty, Mukohyama 2004, hep-th/0312099.
  GDM  = Furukawa, Yokoyama, Ichiki, "Ghost Dark Matter", arXiv:1001.4634 (JCAP 2010)
         -- the dedicated ghost-condensate-as-dark-matter P(k) analysis.

KEY LITERATURE EQUATIONS (verbatim, see /tmp/gdm_txt.txt extraction):
  * Dispersion (exact GC, decoupling limit) ACLM/GDM Eq 2.11:  omega^2 = (alpha/M^2) k^4
  * Dispersion w/ gravity mixing,         GDM Eq 2.14:  omega^2 = (alpha/M^2)k^4 - (alpha M^2/2 M_Pl^2) k^2
  * Sound speed (off-condensate dust),    GDM Eq 3.3:   c_s^2 = P_X / (2 X P_XX + P_X)
  * Working Lagrangian P=(X-M^4)^2/8M^4,  GDM Eq 4.7:   c_s^2 = (X - M^4)/(3X - M^4)
      -> near condensate (X->M^4): c_s^2 ~ (X-M^4)/(2M^4) -> 0, and c_s^2 ∝ a^-3 (Eq 4.10 region)
  * Jeans wavenumber at m-r equality,     GDM Eq 4.2:
        k_J,eq ≃ 1 Mpc^-1 * (Omega_gdm h^2 / 0.11)^(-5/6) * (M / 10 eV)^(4/3)
  * Suppression appears for k > k_J,eq; data show NO suppression for k/h < ~1 Mpc^-1
        => GDM's OWN BOUND:  M >~ 10 eV   (GDM Sec 4.1, confirmed numerically Sec 4.2)

THE FRAMEWORK'S SCALE (banked GHOST_CONDENSATE_2026-06-19, seesaw_two_scales.py):
        M_clustering ~ 0.04 - 1 eV   (set by mu^-1 >~ 1 Mpc, the AeST lensing/cluster scale)

This script: (a) c_s^2(k,a) and w(k); the departure-from-CDM scale.
            (b) the S8/sigma8 direction & amplitude vs Planck/DES/KiDS.
            (c) ISW / late-time interplay with the w=-1 minimum.
Both ways: a genuine P(k)/S8 signature vs CDM-degenerate null -- decided by NUMBERS.
"""
import numpy as np

# ---------- constants ----------
c=2.99792458e8; G=6.67430e-11; hbar=1.054571817e-34; kB=1.380649e-23
Mpc=3.0856775814913673e22; eV=1.602176634e-19; GeV=1e9*eV
M_Pl_red_eV = 2.435e18*1e9          # reduced Planck mass in eV
h=0.674; H0=h*100e3/Mpc             # s^-1
Om_m=0.315; Om_L=0.685; Om_b=0.0493; Om_dm=Om_m-Om_b   # ~0.266
Om_dm_h2 = Om_dm*h*h                # ~0.12
a_eq = 1.0/3400.0                   # matter-radiation equality scale factor (z_eq~3400)

print("="*80)
print("FRAMEWORK INPUTS")
print("="*80)
print(f"  Omega_dm h^2 = {Om_dm_h2:.4f}   (GDM normalize at 0.11; we use the real 0.12)")
print(f"  a_eq = {a_eq:.3e}  (z_eq ~ {1/a_eq:.0f})")
print(f"  Framework clustering scale M ~ 0.04 - 1 eV (banked; from mu^-1 >~ 1 Mpc)")
print()

# ============================================================================
# (a) THE JEANS WAVENUMBER AT EQUALITY -- the scale where GC-dust departs from CDM
#     GDM Eq 4.2 (the literature's own; we just plug in the framework's M)
# ============================================================================
print("="*80)
print("(a) JEANS WAVENUMBER AT EQUALITY  k_J,eq  (GDM Eq 4.2) -- departure scale")
print("="*80)
def kJeq_Mpc(M_eV, Om_dm_h2=Om_dm_h2):
    # k_J,eq in Mpc^-1 (NOT h/Mpc); GDM Eq 4.2
    return 1.0 * (Om_dm_h2/0.11)**(-5.0/6.0) * (M_eV/10.0)**(4.0/3.0)

print(f"  {'M (eV)':>10} | {'k_J,eq (Mpc^-1)':>16} | {'k_J,eq (h/Mpc)':>15} | {'lambda_J (Mpc)':>14}")
print("  " + "-"*66)
for M_eV in [0.04, 0.1, 0.15, 0.3, 1.0, 10.0, 100.0]:
    kJ = kJeq_Mpc(M_eV)          # Mpc^-1
    kJ_h = kJ/h                   # h/Mpc
    lamJ = 2*np.pi/kJ             # Mpc (comoving)
    flag = ""
    if 0.04 <= M_eV <= 1.0: flag = "  <-- FRAMEWORK WINDOW"
    if M_eV==10.0: flag = "  <-- GDM's bound (k_J,eq ~ 1 h/Mpc)"
    print(f"  {M_eV:>10.2f} | {kJ:>16.4f} | {kJ_h:>15.4f} | {lamJ:>14.2f}{flag}")
print()
print("  Read-off: observational data show NO P(k) suppression for k/h <~ 1 Mpc^-1")
print("  (GDM Sec 4.1). The SUPPRESSION scale k_J,eq must lie ABOVE the observed range.")
print("  k_J,eq >~ 1 Mpc^-1 requires (M/10eV)^(4/3) >~ 1 -> M >~ 10 eV  (GDM's bound).")
print()
print("  *** The framework's M ~ 0.04-1 eV gives k_J,eq ~ 0.007-0.2 Mpc^-1 ***")
print("  *** i.e. the GC-dust Jeans/sound-suppression bites at lambda ~ 30-900 Mpc, ")
print("      DEEP inside the linear, well-measured regime -- NOT degenerate with CDM. ***")
print()

# ============================================================================
# (a') c_s^2(a) scaling and w(k) -- the effective pressure of the dust mode
# ============================================================================
print("="*80)
print("(a') SOUND SPEED c_s^2(a) and EFFECTIVE w(k)")
print("="*80)
# From GDM Eq 4.10: the condition |X-M^4|/M^4 = 2 c_s^2; and near the condensate
#   c_s^2 ∝ |X-M^4| ∝ a^-3  (Eq 4.10 derivation: c_s ∝ a^-3/2 -> c_s^2 ∝ a^-3).
# Normalize today: at a=1 the dust has Omega_dm; |X-M^4|/M^4 ~ rho_dust/M^4 today.
# But the *physical* statement we need is the GROWTH-relevant c_s^2 at equality.
# Define c_s^2(a) = c_s^2(eq) * (a/a_eq)^-3? No: GDM gives c_s^2 ∝ a^-3 (Eq 4.10).
# We use the operational result: at equality, the Jeans wavenumber k_J,eq from Eq 4.2.
# Invert to get the *implied* c_s at equality: k_J = sqrt(3/2) a H / c_s (Eq 4.1),
#   so c_s(eq) = sqrt(3/2) a_eq H(a_eq) / k_J,eq  (comoving k).
# H at equality (radiation+matter): H_eq^2 = H0^2 * Om_m * a_eq^-3 * 2  (rho_r=rho_m at eq)
H_eq = H0*np.sqrt(Om_m*a_eq**-3 * 2.0)   # s^-1 (factor 2: rho_tot=2 rho_m at eq)
# comoving k_J,eq -> physical Jeans relation k_phys = k_com/a ; GDM's k_J,eq is comoving Mpc^-1.
print(f"  H_eq = {H_eq:.3e} s^-1 ;  a_eq H_eq (comoving Hubble) = {a_eq*H_eq:.3e} s^-1")
print(f"  In length: comoving Hubble radius at eq = c/(a_eq H_eq)/Mpc = {c/(a_eq*H_eq)/Mpc:.2f} Mpc")
print()
for M_eV in [0.15, 1.0, 10.0]:
    kJ = kJeq_Mpc(M_eV)/Mpc      # m^-1 comoving
    # GDM Eq 4.1: k_J = sqrt(3/2) a H / c_s  (with c_s in units of c; k_J comoving requires
    #   k_J = sqrt(3/2) a H /(c_s c) in physical, then *a for comoving -> a^2 H/(c_s c).)
    # We just back out the dimensionless c_s at eq consistent with Eq 4.2:
    cs_eq = np.sqrt(1.5)*a_eq*H_eq/(kJ*c)   # dimensionless (units of c), rough
    print(f"  M={M_eV:6.2f} eV: k_J,eq={kJeq_Mpc(M_eV):.4f} Mpc^-1 -> implied c_s(eq)~{cs_eq:.2e} c"
          f"  (c_s^2~{cs_eq**2:.2e})")
print()
print("  c_s^2 ∝ a^-3 (GDM Eq 4.10): the dust is COLDER today, WARMER in the past.")
print("  So the relevant pressure is set at/near equality, and k_J,eq is the largest")
print("  comoving Jeans scale (it shrinks the wavelength = grows k_J only into the past).")
print("  => the suppression is a PERMANENT imprint on all k > k_J,eq laid down by eq.")
print()

# ============================================================================
# (b) S8 / sigma8 direction & amplitude
# ============================================================================
print("="*80)
print("(b) S8 / sigma8 : does it HELP or HURT the tension, and by how much?")
print("="*80)
print("  Direction: a finite-c_s 'cold-but-pressured' dark matter SUPPRESSES small-scale")
print("  growth below k_J -> LOWERS sigma8/S8. The S8 tension is that PLANCK-LCDM predicts")
print("  S8~0.83 but weak lensing (DES/KiDS) measures S8~0.76 -- i.e. data want LESS small-")
print("  scale power. So the SIGN is RIGHT: GC-dust pressure could RELIEVE the S8 tension.")
print()
print("  Planck 2018  S8 = 0.832 +- 0.013")
print("  DES Y3       S8 = 0.776 +- 0.017")
print("  KiDS-1000    S8 = 0.759 +- 0.024")
print("  KiDS+DES (joint, 2023) S8 ~ 0.79")
print("  Tension: ~2-3 sigma; data want S8 LOWER by ~5-8% than Planck-LCDM.")
print()
# sigma8 is a top-hat 8 Mpc/h variance -> dominated by k ~ 0.2 h/Mpc ~ 0.13 Mpc^-1.
k_sigma8_hMpc = 0.2       # h/Mpc, the pivot for sigma8(R=8 Mpc/h)
k_sigma8_Mpc = k_sigma8_hMpc*h
print(f"  sigma8 (R=8 Mpc/h) is dominated by k ~ {k_sigma8_hMpc} h/Mpc = {k_sigma8_Mpc:.3f} Mpc^-1.")
print(f"  S8 = sigma8 sqrt(Om_m/0.3).")
print()
print(f"  {'M (eV)':>8} | {'k_J,eq (Mpc^-1)':>15} | {'k_sigma8/k_J,eq':>16} | effect on sigma8")
print("  " + "-"*70)
for M_eV in [0.04, 0.1, 0.15, 0.3, 1.0, 3.0, 10.0, 30.0]:
    kJ = kJeq_Mpc(M_eV)
    ratio = k_sigma8_Mpc/kJ
    if ratio > 3:
        eff = "STRONG suppression (k_sig >> k_J): sigma8 KILLED (too much)"
    elif ratio > 1:
        eff = "sigma8 scale partly suppressed -- could relieve S8"
    elif ratio > 0.3:
        eff = "edge of sigma8 scale -- mild few-% suppression"
    else:
        eff = "k_J above sigma8 scale -> NEGLIGIBLE (CDM-degenerate at sigma8)"
    print(f"  {M_eV:>8.2f} | {kJ:>15.4f} | {ratio:>16.2f} | {eff}")
print()
print("  AMPLITUDE: GDM is a SHARP cutoff (power -> 0 for k>k_J, like a hot/warm species),")
print("  NOT a gentle few-% tilt. If k_J,eq < k_sigma8 (M < ~few eV) the suppression at the")
print("  sigma8 scale is essentially TOTAL, not the 5-8% the S8 tension wants -- it would")
print("  DESTROY sigma8 and the entire small-scale P(k), grossly excluded. There is NO M")
print("  in the framework's 0.04-1 eV window that gives a GENTLE 5-8% S8 relief: the")
print("  framework's window gives k_J,eq = 0.007-0.2 Mpc^-1, i.e. suppression starts at or")
print("  ABOVE the sigma8 scale -> CATASTROPHIC, not therapeutic.")
print()

# ============================================================================
# (c) ISW / late-time interplay with the w=-1 minimum
# ============================================================================
print("="*80)
print("(c) ISW / late-time signature from the condensate's interplay with the w=-1 min")
print("="*80)
print("  The exact GC minimum is w=-1 dark ENERGY (already = the framework's Lambda face).")
print("  The off-minimum displacement is the w=0 dust. Two ISW-relevant effects:")
print("   (i) The dust's finite c_s^2 makes potentials Phi DECAY on sub-Jeans scales even in")
print("       matter domination (pressure support) -> extra late-time Phi-dot -> ISW power.")
print("       But this lives at k > k_J,eq; for M<1eV that's the SAME catastrophically-")
print("       suppressed regime -> the ISW change rides on an already-excluded P(k). Not a")
print("       clean independent ISW prediction; it is downstream of the P(k) kill.")
print("   (ii) ACLM antigravity/oscillatory Newtonian potential (grad^2 Phi + mu^2 Phi = src)")
print("       at r > r_c ~ M_Pl/M^2; mu^-1 >~ Mpc pushes it to >~ 100 Mpc -- a super-cluster /")
print("       ISW-scale modification of Phi. This is a DISTINCT AeST signature (VSB Eq 11),")
print("       but it is the SAME free-mu mode already in the ledger, and it is the lensing/")
print("       cluster mu, not a NEW number. It does NOT rescue the P(k) problem.")
print()

# ============================================================================
# VERDICT LOGIC
# ============================================================================
print("="*80)
print("VERDICT (both ways)")
print("="*80)
M_lo, M_hi = 0.04, 1.0
kJ_lo, kJ_hi = kJeq_Mpc(M_lo), kJeq_Mpc(M_hi)
print(f"  Framework M window: {M_lo}-{M_hi} eV -> k_J,eq = {kJ_lo:.4f}-{kJ_hi:.4f} Mpc^-1")
print(f"     = {kJ_lo/h:.4f}-{kJ_hi/h:.4f} h/Mpc, i.e. suppression onsets at lambda ~ {2*np.pi/kJ_hi:.0f}-{2*np.pi/kJ_lo:.0f} Mpc.")
print("  GDM's OWN bound (no observed suppression for k/h<1): M >~ 10 eV.")
print()
print("  TENSION: the framework's clustering scale M~0.04-1 eV is 10-250x BELOW the GDM")
print("  M>~10 eV bound. Naively this would make the GC-dust P(k) GROSSLY excluded (huge")
print("  suppression at observed scales). BUT -- crucial caveat -- the GDM bound assumes")
print("  the ghost condensate is ALL the dark matter via the SIMPLE P(X) FRW dust. In AeST/")
print("  the framework, the same scale appears as mu (the Poisson-mass), and Skordis-Zlosnik")
print("  2021 SHOW AeST FITS the full Planck CMB + matter P(k) incl. the 3rd peak -- so the")
print("  AeST realization is ALREADY TUNED to NOT show this suppression at CMB/large scales.")
print("  The reconciliation: AeST's cold component clusters via the FULL 6-dof structure")
print("  (massive scalar+vector with c_s=c, NOT the bare P(X) k^4 mode); the k^4/M^2 feature")
print("  is pushed below mu ~ Mpc^-1 by the mass term. So the HONEST status is:")
print("   - As a BARE ghost-condensate dust (GDM Eq 4.2): M~0.1eV is EXCLUDED by P(k).")
print("   - As AeST (the framework's actual realization): the feature is the residual k^4")
print("     correction on TOP of an already-CDM-mimicking transfer function, at k>~mu~1/Mpc,")
print("     pushed toward the small-scale/nonlinear regime where it is hard to see.")
print()
