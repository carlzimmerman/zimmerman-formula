#!/usr/bin/env python3
"""
eft_validity_window_calc.py  (topic: eft_validity_window, 2026-06-19)

CRUX: the EFT VALIDITY + consistency window of the ghost condensate (GC) as the
framework's dark sector. Three sub-questions, all from ACLM (Arkani-Hamed, Cheng,
Luty, Mukohyama, hep-th/0312099), pulled verbatim this session (Sec 4-8):

 (a) STRONG-COUPLING / cutoff scale Lambda_strong. ACLM Sec 4 (verbatim, line 786):
       "if we work with a UV cutoff Lambda that is somewhat smaller than the scales
        M, Mbar, then the strongest dimensionless coupling is set by powers of
        lambda = Lambda/M."
     => the EFT cutoff is Lambda_strong <~ M itself (NOT (M^3 M_Pl)^(1/4) or any
        boosted scale; the leading interaction M^4 pidot (grad pi)^2 is IRRELEVANT,
        scaling dim s^(1/4), Eq 4.7, so the IR EFT is controlled DOWN to arbitrarily
        low E and the cutoff is the SSB scale M on the UV side). ACLM work in
        10^-3 eV < M < 10 MeV (line 806). We check the framework USES the field only
        at E << M (cosmology k~H0, galaxies kpc-Mpc, solar system) -> deep IR, valid.

 (b) ANTIGRAVITY / oscillating-force scale. ACLM Eq 1.10:
       r_c ~ M_Pl/M^2  (length where Newtonian potential goes oscillatory),
       t_c ~ M_Pl^2/M^3 (time you must WAIT before it appears),
     and the late-time reach (Eq 7.18, around line 1357): a change at distance r
     needs t ~ t_c*(r/r_c). In AeST the SPATIAL onset is r_C; graviton mass
       m = M^2/(sqrt2 M_Pl)  (Eq 7.7) = the AeST mu.  Check: does r_c (or the AeST
     r_C) sit beyond galaxy disks / clusters for the framework's M, or intrude?

 (c) THE DARK-MATTER-vs-DARK-ENERGY SEESAW TENSION. The SAME GC field doing BOTH
     dark energy (w=-1 attractor, M~rho_DE^(1/4)~meV) AND dark matter (w=0 off-
     attractor dust) is constrained in the literature (the two faces want different
     M; BH accretion bounds the dust M < ~10 MeV). The framework puts Lambda in as a
     SEPARATE additive -2Lambda, so its GC is asked to be ONLY the dust. Does that
     dodge work, or does the same-field tension still bite?

Everything in M, M_Pl, eV, Mpc; both-ways; quarantine (no "derived").
"""
import numpy as np

# ---------------- constants ----------------
c     = 2.99792458e8            # m/s
hbar  = 1.054571817e-34         # J s
G     = 6.67430e-11             # SI
eV    = 1.602176634e-19         # J
MeV   = 1e6*eV; GeV = 1e9*eV
Mpc   = 3.0856775814913673e22   # m
kpc   = Mpc/1e3
yr    = 3.15576e7; Gyr = 1e9*yr
hbarc_eVm = 197.3269804e6*1e-15 # eV*m  (hbar c)
hbar_eVs  = 6.582119569e-16     # eV*s

# reduced Planck mass (ACLM's M_Pl: M_Pl^2 = 1/(8 pi G))
M_Pl_J  = np.sqrt(hbar*c**5/(8*np.pi*G))
M_Pl_eV = M_Pl_J/eV             # 2.435e27 eV

# cosmology / framework
H0   = 67.4e3/Mpc               # s^-1
OmL  = 0.685; Om_dm = 0.265; Om_b = 0.0493
Lam  = 1.0909e-52               # m^-2
a0   = 9.3624e-11               # m/s^2
rho_crit = 3*H0**2/(8*np.pi*G)
rho_DE_u = OmL*rho_crit*c**2    # J/m^3
eV4_Jm3  = eV**4/(hbarc_eVm/1e6*1e6)  # placeholder; compute cleanly below
eV4_in_Jm3 = eV**4/(hbar*c)**3
E_DE = (rho_DE_u/eV4_in_Jm3)**0.25     # eV  (~2.24e-3)

print("="*80)
print("ANCHORS")
print("="*80)
print(f"M_Pl(reduced) = {M_Pl_eV:.4e} eV = {M_Pl_eV/1e9:.4e} GeV")
print(f"rho_DE^(1/4)  = {E_DE*1e3:.3f} meV    H0 = {H0:.3e} /s  (1/H0={1/H0/Gyr:.1f} Gyr)")
print(f"cH_Lam/c = sqrt(Lam/3) = {np.sqrt(Lam/3):.3e} /m ;  horizon c/H0 = {c/H0/Mpc:.0f} Mpc")
print()

# The framework's M window (from seesaw_two_scales.py / DSUNRUH note):
#  - clustering-LENGTH scale (the one AeST USES for mu, lensing/cluster mass): M~0.04-1 eV
#  - energy-density seesaw scale (M^4/M_Pl^2 = rho_DE): M~0.1 GeV (only if GC were the DE; it is NOT here)
M_grid = {
    "DE-attractor (ACLM 1.11, =Lambda face)": 1.0e-3,     # eV
    "framework LOW  (mu^-1~few Mpc)":          0.04,
    "framework MID  (mu^-1~1 Mpc)":            0.15,
    "framework HIGH (mu^-1~50 kpc)":           1.0,
    "ACLM ceiling (BH-accretion/twinkle)":     10e6,
}

def graviton_mass_eV(M_eV):
    """ACLM Eq 7.7: m = M^2/(sqrt2 M_Pl).  This IS the AeST mu."""
    return M_eV**2/(np.sqrt(2)*M_Pl_eV)

def mu_inv_Mpc(M_eV):
    m = graviton_mass_eV(M_eV)            # eV
    return (hbarc_eVm/m)/Mpc              # m^-1 in Mpc -> length in Mpc

# ===========================================================================
print("="*80)
print("(a) STRONG-COUPLING / EFT CUTOFF  (ACLM Sec 4: Lambda_strong <~ M)")
print("="*80)
print("ACLM: leading interaction M^4 pidot(grad pi)^2 is IRRELEVANT (scaling dim s^1/4,")
print("Eq 4.7) -> the IR EFT is CONTROLLED to arbitrarily low E; the cutoff is on the UV")
print("side at Lambda_strong <~ M (the SSB scale). lambda_coupling = Lambda/M < 1.")
print("Framework uses the field at the following ENERGIES E~hbar*(rate) / MOMENTA:")
print(f"{'regime':38s} {'E or hbar*k*c (eV)':>20s}   E/M for M=0.15 eV")
# characteristic energies of the regimes the framework uses the field in:
E_cosmo   = hbar*H0/eV                       # eV  (cosmological frequency ~H0)
k_gal     = 2*np.pi/(10*kpc)                 # 1/m, galaxy ~10 kpc
E_gal     = hbarc_eVm*k_gal                  # eV
k_clu     = 2*np.pi/(1*Mpc)                  # cluster ~Mpc
E_clu     = hbarc_eVm*k_clu                  # eV
k_ss      = 2*np.pi/(1.5e11)                 # solar system ~1 AU
E_ss      = hbarc_eVm*k_ss                   # eV
Mref=0.15
for lab,E in [("cosmology (omega~H0)",E_cosmo),
              ("galaxy (k~2pi/10kpc)",E_gal),
              ("cluster (k~2pi/Mpc)",E_clu),
              ("solar system (k~2pi/AU)",E_ss)]:
    print(f"{lab:38s} {E:>20.3e}   {E/Mref:.2e}")
print()
print("VERDICT (a): every scale the framework USES the GC at has E/M <= ~1e-7 (galaxy)")
print("down to ~1e-30 (cosmology) -- DEEP in the IR, far below the cutoff. (The solar-")
print("system k is large but the field is screened there [g>>a0, MOND off] and the")
print("static-source modification only switches on after t_c >> 1/H0; see (b).) The EFT")
print("is VALID across every regime the framework needs. No observable UV-completion")
print("breakdown bites. Caveat (shared with ALL MOND/AeST): a UV completion above M is")
print("required in principle -- generic EFT statement, not a kill.")
print()

# ===========================================================================
print("="*80)
print("(b) ANTIGRAVITY / OSCILLATING-FORCE SCALE  (ACLM Eq 1.10, 7.18; AeST r_C via mu)")
print("="*80)
print(f"{'scenario':42s} {'M(eV)':>9s} {'m=mu(eV)':>11s} {'mu^-1(Mpc)':>11s} "
      f"{'r_c=MPl/M^2':>13s} {'t_c=MPl^2/M^3':>14s}")
for lab,M in M_grid.items():
    m_eV  = graviton_mass_eV(M)
    muinv = mu_inv_Mpc(M)
    rc_m  = (M_Pl_eV/M**2)*hbarc_eVm          # r_c in m
    tc_s  = (M_Pl_eV**2/M**3)*hbar_eVs        # t_c in s
    rc_str = f"{rc_m/Mpc:.2e}Mpc"
    tc_str = f"{tc_s/Gyr:.2e}Gyr"
    print(f"{lab:42s} {M:9.2e} {m_eV:11.2e} {muinv:11.2e} {rc_str:>13s} {tc_str:>14s}")
print()
print("KEY POINTS:")
print(" * r_c = M_Pl/M^2 is the LINEAR-onset length (ACLM 1.10). For the framework's")
print("   clustering window M=0.04-1 eV, r_c ~ 0.7-100 Mpc -- SUPER-GALACTIC. Galaxy")
print("   disks (~10-50 kpc) and even cluster cores (~Mpc) sit at r << r_c at the small")
print("   end? CHECK the WAIT TIME, which is the real protector:")
for lab,M in [("framework MID M=0.15 eV",0.15),("framework HIGH M=1 eV",1.0)]:
    rc_m  = (M_Pl_eV/M**2)*hbarc_eVm
    tc_s  = (M_Pl_eV**2/M**3)*hbar_eVs
    # time to see a modification at galaxy r=20 kpc and cluster r=1 Mpc:
    for rlab,r in [("20 kpc",20*kpc),("1 Mpc",1*Mpc),("10 Mpc",10*Mpc)]:
        t_need = tc_s*(r/rc_m)
        print(f"   {lab}: modification at {rlab:7s} needs t~t_c*(r/r_c) = {t_need/Gyr:.2e} Gyr "
              f"(age=13.8) -> {'NEVER (>>age)' if t_need>13.8*Gyr else 'POSSIBLE'}")
print()
print(" * In AeST the onset is a SPATIAL feature governed by mu (= ACLM m). The framework")
print("   needs mu^-1 >~ 1 Mpc for galaxy MOND. From the table, mu^-1 >~ 1 Mpc <=> M <~ 0.15 eV.")
print("   At M=0.15 eV, mu^-1=1.0 Mpc and Verwayen-Skordis-Boehm Fig 4 put the OSCILLATION")
print("   onset r_C ~ (r_M/mu^2)^(1/3) ~ 156 kpc -- BEYOND galaxy disks, just reaching cluster")
print("   outskirts. So the antigravity oscillation is pushed past galaxies for M<~0.15 eV.")
print()
print("VERDICT (b): For M in the framework's clustering window (<~0.15 eV, mu^-1>~1 Mpc),")
print("the antigravity/oscillation regime sits BEYOND galaxy disks (r_C>~156 kpc) and the")
print("Minkowski linear onset needs t>>age at galaxy/cluster radii -- it does NOT intrude")
print("on galaxy dynamics. It DOES reach into cluster outskirts / the matter power spectrum")
print("at k~mu~Mpc^-1 -> a POTENTIAL distinctive feature there (the SZ21 omega=0 Y-mode at")
print("k<mu), but mu is FREE and squeezed by exactly this data -> it is the standard 'free")
print("constant pushed out of the window' situation, NOT a clean new prediction. The COST")
print("is that mu must be chosen small; the cure (dS Hubble friction, H>Gamma) removes the")
print("instability for ALL these M (next).")
print()

# ===========================================================================
print("="*80)
print("(c) DARK-MATTER vs DARK-ENERGY SEESAW TENSION -- does the framework's split dodge it?")
print("="*80)
# The two faces want different M:
M_DE   = E_DE                                   # ~meV : w=-1 attractor face
# dust face: BH accretion (hep-th/0404216) bounds the DUST scale M <~ 10 MeV
M_dust_ceiling = 10e6
print(f" DARK-ENERGY face (w=-1 attractor): M ~ rho_DE^(1/4) = {M_DE*1e3:.2f} meV  (ACLM 1.11)")
print(f" DARK-MATTER face (w=0 dust): BH-accretion ceiling M <~ 10 MeV (hep-th/0404216);")
print(f"   ALSO the clustering-length scale wants M~0.04-1 eV (mu^-1~Mpc). Both << 10 MeV: OK.")
print()
print(" THE LITERATURE TENSION (one GC for BOTH): the dark-ENERGY seesaw M^4/M_Pl^2=rho_DE")
M_seesaw = (E_DE**4 * M_Pl_eV**2)**0.25
print(f"   wants a HIGH M_seesaw = (rho_DE M_Pl^2)^(1/4) = {M_seesaw/1e6:.1f} MeV ~ 0.1 GeV,")
print(f"   which exceeds the 10 MeV BH-accretion ceiling for the DUST -> a single GC straddling")
print(f"   both faces is in TENSION (M~0.1 GeV for energy seesaw vs M<10 MeV for dust).")
print()
print(" THE FRAMEWORK'S SPLIT: Lambda enters K(Q) as a SEPARATE additive -2Lambda (the dark")
print(" ENERGY is the explicit cosmological constant, NOT the condensate's seesaw). So the")
print(" framework's GC is asked to be ONLY the w=0 dust, at M~0.04-1 eV (clustering length),")
print(" which is BELOW the 10 MeV BH-accretion ceiling by ~7 orders. The seesaw straddle")
print(" tension is AVOIDED -- but at the cost of the orthogonality d(rho_dust)/d(Lambda)=0")
print(" (the dust amplitude I0 is then free; banked). The dodge IS the orthogonality.")
print()
# quantify the accretion margin at the framework's M:
for lab,M in [("framework HIGH M=1 eV",1.0),("framework MID M=0.15 eV",0.15)]:
    margin = M_dust_ceiling/M
    print(f"   {lab}: M / 10MeV-ceiling = {M/M_dust_ceiling:.2e}  -> {margin:.1e}x BELOW the")
    print(f"     BH-accretion bound -> accretion benign (dust-like, Mukohyama hep-th/0502189).")
print()
print("VERDICT (c): the seesaw DM-vs-DE tension does NOT bite the framework, BECAUSE it does")
print("NOT use one GC for both -- Lambda is a separate additive constant and the GC is dust-")
print("only at M~0.04-1 eV (7 orders below the BH ceiling). The price is the banked")
print("orthogonality: Lambda cannot then pin the dust amount (I0 free). Both-ways: the")
print("split is a GENUINE consistency advantage over the literature's single-GC straddle")
print("(credited), bought with the free dust amplitude (conceded).")
print()

# ===========================================================================
print("="*80)
print("(d) THE k^4 DISPERSION -- is there a COMPUTABLE distinctive P(k)/CMB feature, or CDM-degenerate?")
print("="*80)
# ACLM dispersion Eq 7.8: omega^2 = alpha^2 k^4/M^2 - (alpha^2 M^2/2 M_Pl^2) k^2
#  Jeans scale k_J = m = M^2/(sqrt2 M_Pl); Gamma = alpha M^3/(4 M_Pl^2).
# In AeST the SAME mu = m sets the scale below which the mode is the omega=0 Y-mode.
# The question: at what comoving k does the k^4 piece DEPART from CDM (omega^2=0, pure dust)?
print("ACLM Eq 7.8: omega^2 = alpha^2 k^4/M^2 - (alpha^2 M^2/2M_Pl^2) k^2. The k^4 piece")
print("DOMINATES (departs from pressureless CDM) for k > m = mu. Below k<mu: Jeans/Y-mode.")
print("So the GC dust = CDM for k>>mu (small scales) and DEPARTS at k<~mu (large scales).")
print("This is the OPPOSITE of a particle-CDM Jeans/free-streaming cutoff (which is at SMALL")
print("scales / high k). The GC feature is at k~mu~Mpc^-1 -- LARGE scales.")
print()
print("For the framework's M (mu^-1>~1 Mpc => mu<~1 Mpc^-1 ~ 0.001-1 h/Mpc):")
for lab,M in [("M=0.04 eV",0.04),("M=0.15 eV",0.15),("M=1 eV",1.0)]:
    m_eV  = graviton_mass_eV(M)
    k_mu  = m_eV/hbarc_eVm        # 1/m
    k_mu_hMpc = k_mu*Mpc/0.674     # h/Mpc  (k in h/Mpc)
    print(f"   {lab}: mu = {m_eV:.2e} eV -> k_mu = {k_mu_hMpc:.3e} h/Mpc "
          f"(lambda = {2*np.pi/k_mu/Mpc:.2f} Mpc)")
print()
print("VERDICT (d): the distinctive k^4 feature lives at k~mu. For mu^-1>~1 Mpc it is at")
print("k<~1 h/Mpc -- IN the observable P(k)/CMB-lensing window in PRINCIPLE. BUT: (i) AeST")
print("ALREADY fits full Planck incl. 3rd peak + P(k) by TUNING the cold component to mimic")
print("CDM (Skordis-Zlosnik 2021 PRL), so the leading behavior is CDM by construction; (ii)")
print("the residual departs only at k<~mu where mu is FREE and pushed to >~Mpc precisely to")
print("keep MOND at galaxies and avoid the instability -> the feature is squeezed toward")
print("k->0 (super-survey) as mu->0. So: a feature EXISTS at k~mu in principle, but it is")
print("(a) degenerate with the free mu, (b) on the LARGE-scale side where cosmic variance is")
print("worst, and (c) already absorbed into AeST's CMB/P(k) fit. NOT a clean new falsifiable")
print("front beyond the existing ones unless mu can be INDEPENDENTLY pinned -- which the")
print("framework cannot do (mu/I0 free). Honest status: NOT out-of-window, but DEGENERATE")
print("with a free parameter -> not a new distinctive signature at full weight.")
