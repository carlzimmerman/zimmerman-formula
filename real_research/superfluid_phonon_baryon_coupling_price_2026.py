#!/usr/bin/env python3
"""
PRICING THE PHONON-BARYON COUPLING  alpha*(Lambda_c/M_Pl)*theta*rho_b
against the one result Carl's framework most depends on: MATTER COUPLES TO g_{mu nu} ALONE.

Framework premises (N1-N7), reasoned from on their own terms:
  N1  a0 = kappa c sqrt(G rho_Lambda): canonical 9.3619e-11, alt 1.1279e-10  (BOTH always)
  N5  a0-line: g_obs^2 = g_bar^2 + a0 g_bar  =>  nu = sqrt(1+a0/g_bar),  U(y) -> 1/2 (SATURATES)
  N6  Q_0 pinned 0.0024-0.0146 Mpc^-1
  N7  AeST: Q = A^mu grad_mu phi (temporal), Y = q^{mu nu} grad phi grad phi (spatial),
      A_mu = {-(1+Psi), grad_i alpha}  =>  A^0 = 1 - Psi  =>  Q CARRIES Psi ITSELF.

TWO READINGS of "the phonon force", reported separately because they differ by 6 orders:
  READING A (framework-native): the phonon force IS the a0-line anomaly, (nu-1)*g_bar.
             Deep-Newtonian it SATURATES at a0/2.  This is R1's constant sunward anomaly.
  READING B (BK-native): BK's condensate has NO interpolation function -- the Newtonian
             regime is the ABSENCE of the medium -- so inside the condensate the phonon
             force is sqrt(a0*g_bar) with no turn-off.
"""
import math

G, c = 6.674e-11, 2.99792458e8
Msun = 1.98892e30
AU   = 1.495978707e11
pc   = 3.0856775814913673e16
kpc, Mpc = 1e3*pc, 1e6*pc
hbar_c_eV_m = 1.973269804e-7          # eV*m

A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}

nu      = lambda gb, a0: math.sqrt(1.0 + a0/gb)          # N5
a_readA = lambda gb, a0: (nu(gb, a0) - 1.0)*gb           # saturates -> a0/2
a_readB = lambda gb, a0: math.sqrt(a0*gb)                # BK, unscreened

# ---- composition handles: BK couples to rho_b = m_N n_B, i.e. to BARYON NUMBER ----
# (MICROSCOPE flew Pt-Rh and Ti-Al-V alloys; pure-element means used as the proxy.)
pairs = {"MICROSCOPE Ti-Pt": ((47.919, 47.867), (195.13, 195.084)),
         "LLR Earth-Moon (Fe/Si proxy)": ((55.91, 55.845), (28.11, 28.085))}
dBmu = {k: abs(a[0]/a[1] - b[0]/b[1]) for k, (a, b) in pairs.items()}

ETA_MICRO_TASK, ETA_MICRO_PUB, ETA_LLR = 1e-15, 1.5e-15, 1.4e-13
GAMMA_CASSINI = 2.3e-5
g_micro   = 8.00
gN_1AU    = G*Msun/AU**2
S_EPH     = 1.27e-5                 # R1's ephemeris ceiling on U -> s (units of a0)
Mb_gal    = 6e10*Msun

print("="*80); print("PHONON-BARYON COUPLING: THE PRICE. Both footings, both readings."); print("="*80)
for k, v in dBmu.items(): print(f"  Delta(B/mu) {k}: {v:.3e}")
print(f"  g(MICROSCOPE alt)={g_micro} m/s^2   gN(Sun,1AU)={gN_1AU:.4e} m/s^2")

for foot, a0 in A0.items():
    print("\n"+"="*80); print(f"FOOTING {foot}:  a0 = {a0:.4e} m/s^2"); print("="*80)
    for rname, aph in (("A  a0-line saturating (framework-native)", a_readA),
                       ("B  BK unscreened sqrt(a0 g) (BK-native) ", a_readB)):
        aE, aS = aph(g_micro, a0), aph(gN_1AU, a0)
        print(f"\n-- READING {rname}")
        print(f"   a_phi(Earth) = {aE:.4e} m/s^2 = {aE/a0:.4g} a0 ;"
              f"  a_phi(Sun@1AU) = {aS:.4e} = {aS/a0:.4g} a0")
        # (a) WEP
        eta = dBmu["MICROSCOPE Ti-Pt"]*aE/g_micro
        etl = dBmu["LLR Earth-Moon (Fe/Si proxy)"]*aS/gN_1AU
        print(f"   (a) eta_MICROSCOPE = {eta:.3e}  -> {eta/ETA_MICRO_TASK:.3g}x the 1e-15 bound,"
              f" {eta/ETA_MICRO_PUB:.3g}x the published 1.5e-15")
        print(f"       eta_LLR        = {etl:.3e}  -> {etl/ETA_LLR:.3g}x the 1.4e-13 bound")
        # (b) gamma_PPN solar system: scalar force on mass, none on light => gamma-1 = -2eps/(1+eps)
        eps = aS/gN_1AU
        gm1 = -2.0*eps/(1.0+eps)
        print(f"   (b) eps(1AU)={eps:.4e} -> gamma_PPN-1 = {gm1:+.4e} ->"
              f" {abs(gm1)/GAMMA_CASSINI:.4g} sigma vs Cassini")
        # (d) fifth force vs the framework's OWN ephemeris ceiling
        print(f"   (d) sunward anomaly {aS:.3e} vs ceiling s*a0={S_EPH*a0:.3e}"
              f"  -> OVER by {aS/(S_EPH*a0):.4g}x ; screening needed {S_EPH*a0/aS:.3e}")

    # (c) lensing deficit -- identical for baryon-only AND for a conformal coupling
    print("\n-- (c) LENSING: a baryon-only coupling (and a CONFORMAL one) does not bend light.")
    for lab, r in (("40 kpc", 40*kpc), ("2.2 Mpc", 2.2*Mpc)):
        gb = G*Mb_gal/r**2
        print(f"       {lab:>8}: g_bar={gb:.3e}, M_dyn/M_lens = nu = {nu(gb,a0):.3f}"
              f"  -> lensing signal short by {nu(gb,a0):.4g}x")

    # (d cont.) does the PHASE BOUNDARY screen the solar system?  BK condensation criterion.
    m_eV, rho_GeVcm3, sig_kms = 0.6, 0.4, 150.0
    n_cm3 = rho_GeVcm3*1e9/m_eV
    eV3_per_cm3 = (1e-2/hbar_c_eV_m)**-3          # (cm^-1 -> eV) cubed
    n_eV3 = n_cm3*eV3_per_cm3
    Tc = 2*math.pi/m_eV*(n_eV3/2.612)**(2.0/3.0)
    T  = m_eV*(sig_kms*1e3/c)**2
    print(f"\n-- (d) PHASE BOUNDARY? BK criterion at the solar circle (m={m_eV} eV,"
          f" rho={rho_GeVcm3} GeV/cm^3, sigma={sig_kms} km/s):")
    print(f"       T={T:.3e} eV, T_c={Tc:.3e} eV, T/T_c={T/Tc:.3e}  -> DEEPLY CONDENSED")
    print(f"       to decondense at 1 AU: sigma x{math.sqrt(Tc/T):.1f} = {sig_kms*math.sqrt(Tc/T):.3e} km/s"
          f" (Galactic escape ~ 550 km/s => x{sig_kms*math.sqrt(Tc/T)/550:.0f} too big),"
          f" or rho down to {(T/Tc)**1.5:.2e} of ambient")
    print(f"       Sun sits at 8 kpc inside a ~100 kpc condensate: boundary 12.5x away in radius.")
    v0, R0 = 233e3, 8.2*kpc
    g_ext = v0**2/R0
    print(f"       acceleration-threshold boundary? g_ext(solar circle)=v^2/R={g_ext:.3e}"
          f" = {g_ext/a0:.3f} a0  > a0  => an 'a>a0 decondenses' rule would decondense the whole"
          f" solar neighbourhood and destroy the MW rotation curve at R_0. EXCLUDED.")

# ---- the R1 escape via Q, and why it fails: mass-dependence of the Psi-term ----
print("\n"+"="*80)
print("THE R1 ESCAPE VIA Q -- AND ITS DEFEAT (mass-dependent weight)")
print("="*80)
print("AeST: A^0 = 1-Psi  =>  Q-Q_0 ~= -Q_0*Psi.  So X=(Q-Q_0)-Y/2m ~= -Q_0*Psi - |grad phi|^2/2m")
print("  = EXACTLY BK's X = ... - m*Phi - (grad theta)^2/2m.  Carl's combination IS realized,")
print("  and R1's premise (F = F(Y) alone) FAILS.  But:")
for foot, a0 in A0.items():
    print(f"\n  footing {foot}:")
    for lab, M in (("Earth", 5.972e24), ("Sun", Msun), ("MW baryons 6e10 Msun", Mb_gal)):
        rM  = math.sqrt(G*M/a0)
        Psi = math.sqrt(G*M*a0)/c**2       # potential AT the body's own MOND radius
        print(f"    {lab:>22}: r_M={rM/AU:11.4g} AU, Psi(r_M)={Psi:.4e}  (Psi ∝ sqrt(M))")
    print(f"    Y at the a0-crossover = (a0/c^2)^2 is MASS-INDEPENDENT by construction.")
    print(f"    => weight ratio (Q-Q_0)/(Y/2m) ∝ sqrt(M):"
          f" Sun->galaxy x{math.sqrt(Mb_gal/Msun):.3e},"
          f" Earth->galaxy x{math.sqrt(Mb_gal/5.972e24):.3e}")
print("\n  A SINGLE m cannot put the X-crossover at a0 in both the solar system and a galaxy.")
print("  Psi-term negligible everywhere -> F->F(Y) -> R1's ephemeris gap returns in full.")
print("  Psi-term dominant in galaxies   -> no gradient-driven MOND force at all.")
print("="*80)
