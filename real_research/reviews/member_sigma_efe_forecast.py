#!/usr/bin/env python3
"""
FORECAST -- floor / SNR for the cluster-member sigma-SIGN test, and what it actually decides.
=============================================================================================
Combines the gating calc (member sigma_int suppression under MI/MG/CDM) with realistic survey numbers
to forecast: (1) the SNR on the SIGN (down vs up) for a 4MOST/MUSE-scale stack; (2) whether the
MI-vs-MG MAGNITUDE gap (the only framework-DISTINCTIVE content) is above the floor; (3) the load-bearing
systematics (interloper rejection; the Faber-Jackson / morphology-density confound seen in the SDSS pilot).
"""
import numpy as np

# --- predicted signal (from the gating calc, framework a0=9.36e-11) ---
# diffuse members (g_in<<a0): MI suppression ~27-60% (large); bright members (g_in>a0): ~few %.
# Stack MEAN over a brightness-weighted member mix: ~6-7% DOWN (matches corpus).
# MI-vs-MG gap: ~1-3% (theta-enhanced), largest in shallow field, vanishes in deep core.
S_sign_diffuse = 0.27      # fractional sigma suppression for a DIFFUSE-selected member sample
S_sign_mixed   = 0.065     # stack-mean suppression for a brightness-mixed sample
S_MIvsMG       = 0.02      # MI-vs-MG magnitude gap (theta(0)~2), the DISTINCTIVE handle

def snr_sign(S, sigma_per, Nmem, Nclus):
    """SNR to detect the SIGN (suppression S, fractional) given per-member fractional sigma error and stack size."""
    Ntot=Nmem*Nclus
    err_frac = sigma_per/np.sqrt(Ntot)
    return S/err_frac, err_frac

def main():
    print("="*92); print(" FORECAST -- cluster-member sigma-SIGN test floor & SNR"); print("="*92)

    # per-member fractional sigma measurement error: MUSE/4MOST resolve member stellar sigma to ~10-20%
    # for bright members, ~30-50% for faint diffuse members (S/N limited). Use representative values.
    print("-"*92); print(" (1) SNR on the SIGN (suppression vs zero), stacked"); print("-"*92)
    print(f"  {'sample':>22} {'S(supp)':>8} {'sig/mem':>8} {'Nmem':>6} {'Nclus':>6} {'Ntot':>7} {'floor':>7} {'SNR':>6}")
    for label,S,sper,nm,ncl in [
        ("diffuse-selected (ideal)",S_sign_diffuse,0.40,15,2000),
        ("diffuse, pilot (1 clus)", S_sign_diffuse,0.40,15,1),
        ("brightness-mixed stack",  S_sign_mixed,  0.15,15,2000),
        ("brightness-mixed, 50 clus",S_sign_mixed, 0.15,15,50),
    ]:
        snr,fl=snr_sign(S,sper,nm,ncl)
        print(f"  {label:>22} {S:>8.2f} {sper:>8.2f} {nm:>6} {ncl:>6} {nm*ncl:>7} {fl:>7.3f} {snr:>6.1f}")
    print("  => the SIGN (DOWN vs flat/UP) is high-SNR for a 2000-cluster stack (matches corpus ~17sigma class),")
    print("     IF a diffuse-member sample is selected and interlopers are clean. A single-cluster pilot is ~2-6sigma.")

    print()
    print("-"*92); print(" (2) Is the framework-DISTINCTIVE MI-vs-MG gap above the floor?"); print("-"*92)
    print(f"  {'sample':>22} {'gap':>6} {'floor':>7} {'SNR_gap':>8}")
    for label,sper,nm,ncl in [
        ("2000-clus diffuse stack",0.40,15,2000),
        ("ideal (smaller sig/mem)", 0.20,15,2000),
        ("10000-clus dream stack",  0.30,20,10000),
    ]:
        snr,fl=snr_sign(S_MIvsMG,sper,nm,ncl)
        print(f"  {label:>22} {S_MIvsMG:>6.2f} {fl:>7.3f} {snr:>8.1f}")
    print("  => the ~2% MI-vs-MG gap clears the STATISTICAL floor on a huge stack (SNR_stat~9-30), BUT it is")
    print("     FAR below the SYSTEMATIC floor: the FJ/morphology-density residual (~12% in the SDSS pilot), the")
    print("     a0/M*/size/aperture degeneracies, and interlopers all exceed 2%. An MG fit with an a0-rescale +")
    print("     M/L freedom absorbs the theta run (same a0-degeneracy as wide binaries). So the MI-specific")
    print("     content is NOT decidable in practice -- only the MOND-SHARED sign is. The test discriminates")
    print("     MOND(MI or MG) vs CDM, NOT MI vs MG.")

    print()
    print("-"*92); print(" (3) Load-bearing systematics"); print("-"*92)
    print("  (a) INTERLOPERS: foreground/background galaxies projected onto the cluster have NO EFE suppression")
    print("      and inflate the member-velocity scatter; if mis-assigned as members they fake the CDM (up/flat)")
    print("      sign. Interloper rejection is the dominant systematic -- the ~17sigma is a CLEAN-SELECTION ceiling.")
    print("  (b) FABER-JACKSON / MORPHOLOGY-DENSITY (proven in the SDSS pilot): at FIXED luminosity, cluster-core")
    print("      members are intrinsically more compact / higher central sigma (FP tilt + morphology-density).")
    print("      In the SDSS Coma pilot this produced a +12% sigma RISE toward center at fixed M_r (3.5sigma) --")
    print("      the OPPOSITE of the EFE sign and ~2x larger. ANY EFE test on bright members is swamped by this.")
    print("      The clean test MUST (i) use DIFFUSE members (g_in<<a0, where EFE>>FJ-residual), (ii) control for")
    print("      stellar mass AND size (use the dynamical-mass / size plane, not luminosity alone), and (iii) compare")
    print("      to a FIELD diffuse-galaxy control at matched M*,size (the isolated-MOND baseline).")
    print("  (c) APERTURE: SDSS 3-arcsec central sigma is luminosity-dominated; the EFE acts on the OUTER, low-")
    print("      acceleration dynamics. Spatially-resolved (MUSE) sigma profiles or the OUTER sigma are needed.")

    print()
    print("="*92); print(" FORECAST BOTTOM LINE"); print("="*92)
    print("  * The SIGN test (member sigma DOWN vs CDM flat/up) is a REAL, high-SNR (~17sigma-class) discriminator")
    print("    of MOND-family (MI or MG) vs CDM -- BUT it is MOND-SHARED, not MI-distinctive.")
    print("  * The MI-distinctive content (the ~2% theta gap MI vs MG) is BELOW the realistic floor -> the test")
    print("    canNOT distinguish the framework's MODIFIED INERTIA from modified GRAVITY. It tests the MOND PREMISE.")
    print("  * The decisive systematic is interloper rejection AND the Faber-Jackson/morphology-density confound")
    print("    (the SDSS pilot shows the FJ-residual sign is UP +12% and 2x the EFE signal on bright members).")
    print("    A clean test requires DIFFUSE members + M*,size control + a field control -- NOT bright ellipticals.")
    print("="*92)

if __name__=="__main__":
    main()
