#!/usr/bin/env python3
"""
THE DECISIVE z~3 TEST: does a0 rise to ~6e-10 in real high-z disks? The Big Wheel says NO (local a0).
====================================================================================================
The framework's central distinctive bet is a0(z) = cH(z)/Z = a0(0) E(z): at z~3.25, E=4.99, so it predicts
a0 ~ 6.0e-10 -- a FIVE-fold rise over the local 1.2e-10. The cleanest possible test is a gas-traced flat
rotation curve of a real z~3 disk: in MOND the flat velocity and baryonic mass obey V_flat^4 = G a0 M_bar, so
a0_eff = V_flat^4 / (G M_bar) reads the acceleration scale straight off the data.

Two gold-standard z~3 disks now exist (the non-rotators in MAGAZ3NE etc. cannot be used -- no rotation curve):

  THE BIG WHEEL (z=3.25, Nature Astronomy 2025, arXiv:2409.17956) -- the CLEAN galaxy-scale test:
    V_rot = 280 (+32/-31) km/s   (inclination-corrected MAXIMUM, at R_eff = 9.6 kpc; inc 48-52 deg)
    M_star = 3.7 (+2.6/-2.2)e11  (non-parametric SED; a parametric fit gives 1.7e11 -- likely overestimated:
                                  see the dynamical-mass check below) ; M_gas(H2,CO) = 1.8 (+1.0/-0.8)e11
    sigma_int = 61 km/s, V/sigma = 4.5 (rotation-dominated; modest asymmetric-drift correction)

  ADF22.1 (z=3.09, arXiv:2604.07440) -- a PROTO-CLUSTER halo, NOT a clean galaxy test:
    V ~ 530 km/s, M_bar = 5.2 (+0.6/-0.7)e11, inc 72 deg, but log M200 = 12.9 (~8e12, group/proto-cluster),
    baryons only 0.43x cosmic, "falls below the z=0 baryonic Fall relation" -> the cluster missing-mass regime.

RESULT (computed below, Monte-Carlo errors): the Big Wheel gives a0_eff ~ 1e-10 -- the LOCAL value -- and a
robust gas-only floor on M_bar caps a0_eff <~ 1.9e-10, FAR below the predicted 6e-10. A risen a0=6e-10 would
make this baryon load spin at ~370-460 km/s; it spins at 280. So the cleanest z~3 disk DISFAVORS a0 ∝ E(z).
ADF22.1's a0_eff ~ 11e-10 is elevated, but that is its proto-cluster missing-mass (M200~8e12), not a clean a0.

This TENSIONS the MUSE-DARK III statistical "rising" signal: the direct gold-standard disk does not show the
predicted x5 rise. Honest state: the framework's central bet is under real observational tension from the best
single z~3 rotation curve, with the usual caveats (one galaxy; M_bar systematics, bounded here; pressure
support, applied). Needs numpy. Data: the two papers above (values hard-coded with their quoted errors).
"""
import numpy as np

G = 6.674e-11; Msun = 1.989e30; kpc = 3.086e19
Om, OL = 0.315, 0.685
E = lambda z: np.sqrt(Om*(1+z)**3 + OL)
A0_LOCAL = 1.2e-10
HE = 1.36   # helium correction to the CO-derived H2 mass


def mc_a0(V_kms, V_err, Mstar, Mstar_err, Mgas, Mgas_err, sigma=0.0, R_kpc=None, n=200000, rng=None):
    """Monte-Carlo a0_eff = V_circ^4/(G M_bar). M_bar = M_star + 1.36 M_gas. Optional asymmetric-drift
    correction V_circ^2 = V_rot^2 + ~3.4 sigma^2 (exponential disk at ~1 R_eff)."""
    rng = rng or np.random.RandomState(1)
    V = rng.normal(V_kms, V_err, n)*1e3
    Vc = np.sqrt(np.maximum(V**2 + 3.4*(sigma*1e3)**2, 1.0)) if sigma else V
    Ms = np.clip(rng.normal(Mstar, Mstar_err, n), 0, None)
    Mg = np.clip(rng.normal(Mgas, Mgas_err, n), 0, None)
    Mbar = np.clip((Ms + HE*Mg), 0.05, None)*1e11*Msun   # floor avoids rare zero-mass MC draws
    a0 = Vc**4/(G*Mbar)
    return a0


def main():
    print("#"*92)
    print("# THE z~3 TEST -- does a0 rise to ~6e-10 in real high-z disks? (Big Wheel, ADF22.1)")
    print("#"*92 + "\n")
    print("="*92); print("FRAMEWORK PREDICTION vs LOCAL"); print("="*92)
    for z in (3.25, 3.09):
        print(f"  z={z}: E(z)={E(z):.2f}  ->  a0 predicted = 1.2e-10 x E(z) = {1.2*E(z):.2f}e-10  (local = 1.20e-10)")
    print()

    print("="*92); print("THE BIG WHEEL (z=3.25) -- the clean galaxy-scale test"); print("="*92)
    # dynamical-mass sanity check at R_eff
    V, Verr, Reff = 280.0, 31.0, 9.6
    Mdyn = (V*1e3)**2*(Reff*kpc)/G/Msun/1e11
    print(f"  dynamical mass within R_eff: M_dyn(<{Reff}kpc) = V^2 R/G = {Mdyn:.2f}e11 Msun.")
    print(f"  -> the SED M_star=3.7e11 implies > {Mdyn:.1f}e11 baryons inside R_eff alone (unphysical: M_bar<=M_dyn),")
    print(f"     so the SED stellar mass is OVERestimated; the true M_bar is nearer gas + reduced stars.\n")
    a0 = mc_a0(280, 31, Mstar=3.7, Mstar_err=2.4, Mgas=1.8, Mgas_err=0.9, sigma=61)
    lo, med, hi = np.percentile(a0, [16, 50, 84])/1e-10
    a0_lowM = mc_a0(280, 31, Mstar=1.7, Mstar_err=1.0, Mgas=1.8, Mgas_err=0.9, sigma=61)
    l2, m2, h2 = np.percentile(a0_lowM, [16, 50, 84])/1e-10
    # robust gas-only floor on M_bar -> upper bound on a0
    Vc = np.sqrt(280**2 + 3.4*61**2)*1e3
    a0_gasfloor = Vc**4/(G*(HE*1.8)*1e11*Msun)/1e-10
    print(f"  a0_eff (M_star=3.7e11 SED):      {med:.2f} (+{hi-med:.2f}/-{med-lo:.2f}) e-10")
    print(f"  a0_eff (M_star=1.7e11 parametric): {m2:.2f} (+{h2-m2:.2f}/-{m2-l2:.2f}) e-10")
    print(f"  a0_eff ROBUST UPPER BOUND (gas mass only, no stars): {a0_gasfloor:.2f} e-10")
    Vneed = (6.0e-10*G*(HE*1.8)*1e11*Msun)**0.25/1e3
    print(f"  to reach the predicted 6.0e-10 even with gas-only M_bar, the disk would need V_flat = {Vneed:.0f} km/s")
    print(f"  (observed maximum: 280 km/s).  => a0 is ~LOCAL, NOT risen x5.\n")

    print("="*92); print("ADF22.1 (z=3.09) -- proto-cluster halo, the cluster missing-mass regime"); print("="*92)
    a0_adf = mc_a0(530, 20, Mstar=2.7, Mstar_err=0.6, Mgas=2.5/HE, Mgas_err=0.9/HE, sigma=0)  # Mbar=5.2e11 total
    la, ma, ha = np.percentile(a0_adf, [16, 50, 84])/1e-10
    print(f"  a0_eff = {ma:.1f} (+{ha-ma:.1f}/-{ma-la:.1f}) e-10  -- ELEVATED, ~2x even the framework's 5.7e-10.")
    print(f"  BUT log M200=12.9 (~8e12 Msun, proto-cluster), baryons 0.43x cosmic, below the z=0 baryonic Fall")
    print(f"  relation: this is the cluster MISSING-MASS regime (like local clusters), NOT a clean a0(z) probe.")
    print(f"  Its high a0_eff is consistent with EITHER risen a0 OR cluster dark matter -- degenerate, ambiguous.\n")

    print("="*92); print("VERDICT -- reported straight"); print("="*92)
    print(f"""  The clean galaxy-scale z~3 disk -- the Big Wheel -- has a0_eff ~ {med:.1f}e-10, the LOCAL value, with a
  robust gas-only ceiling of {a0_gasfloor:.1f}e-10. The framework predicts {1.2*E(3.25):.1f}e-10 at z=3.25. The disk spins far
  too SLOWLY (280 km/s vs the ~{Vneed:.0f}+ km/s a risen a0 would demand) for a0 to have risen x5. So the single best
  z~3 rotation curve DISFAVORS a0 ∝ E(z). ADF22.1 looks elevated but is a proto-cluster halo (missing-mass
  regime), so it cannot clean-test a0(z).
  This is a REAL tension with the MUSE-DARK III statistical 'rising' signal: the most direct probe -- a gas-
  traced z~3 disk -- does not show the predicted rise. Caveats kept honest: one clean galaxy; the SED stellar
  mass is overestimated (shown via M_dyn), which we bound with a gas-only floor; pressure support is applied
  (V/sigma=4.5, small). Net: the framework's central bet (a0 rises ∝ cH(z)/Z) is under genuine observational
  tension from the best high-z disk available -- the rate, if a0 rises at all, looks far shallower than E(z).
  The decisive program is now a SAMPLE of clean z~3 gas-traced disks (not protocluster monsters), where the
  Big Wheel is the first point and it points the wrong way for the strong-rise prediction.""")
    print("="*92)


if __name__ == "__main__":
    main()
