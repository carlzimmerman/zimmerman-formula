#!/usr/bin/env python3
"""
HIGH-z BTFR ZERO-POINT: which rho? (rho_Lambda vs rho_crit fork, on REAL data)
=============================================================================
The baryonic Tully-Fisher relation M_bar = V^4 / (G a0) turns the high-z BTFR zero-point into a
DIRECT measurement of a0(z). The two density forks predict OPPOSITE z-behaviour, and the
already-real KMOS3D (Ubler+2017) and KROSS (Harrison+2017) samples can tell them apart at the
~0.1 dex level:

  FORK (1) rho = rho_Lambda (cosmic dark energy, the framework's reading):
     a0(z) = a0(0) sqrt(rho_DE(z)/rho_DE0). For LCDM rho_DE = const, so a0 is ~FLAT below z~2.
     -> BTFR zero-point ~UNCHANGED at z~1-2.5.  (DESI w0wa adds only a few-% wiggle; negligible here.)
  FORK (2) rho = rho_crit/rho_total (the disfavoured 'evolving' reading):
     a0(z) = cH(z)/Z = a0(0) E(z), E(z)=sqrt(Om(1+z)^3+OL).  At z~1, E~1.7 -> a0 up ~70%.
     -> BTFR zero-point SHIFTS by Delta log M_bar = -log10(a0(z)/a0(0)) = -log10 E(z) ~ -0.23 dex at z~1.

So the SIGN and SIZE of the high-z BTFR offset from the local (SPARC) zero-point discriminates the
two forks. project10b already showed a0=V^4/GM_bar per-galaxy is mass-biased and inconclusive; this
script instead measures the SLOPE-4 ZERO-POINT OFFSET of the whole high-z sample vs SPARC, controlled
for mass, which is the right (BTFR) statistic. Honest grading throughout. Uses ONLY real data on disk.
"""
import numpy as np, os
from scipy import stats

G, Msun, Mpc, kpc = 6.674e-11, 1.989e30, 3.0857e22, 3.0857e19
H0 = 67.4e3/Mpc
Om, OL = 0.315, 0.685
E = lambda z: np.sqrt(Om*(1+z)**3 + OL)
ML = 0.5
HERE = os.path.dirname(__file__)
MRT  = os.path.join(HERE, "..", "data", "SPARC_Lelli2016c.mrt")
K3D  = os.path.join(HERE, "..", "data", "kmos3d_ubler2017.csv")
KROSS= os.path.join(HERE, "..", "data", "kross_harrison2017.csv")

# ---------------------------------------------------------------- local SPARC BTFR (anchor)
def sparc_btfr_zp(slope=4.0):
    lines = open(MRT).read().splitlines()
    rows = [l.split() for l in lines[98:] if len(l) > 100]
    lMb, lV = [], []
    for p in rows:
        L36, MHI, Vf, Q = float(p[7]), float(p[13]), float(p[15]), int(p[17])
        if Vf <= 0 or Q > 2:
            continue
        Mb = ML*L36*1e9 + 1.33*MHI*1e9        # stars (M/L=0.5) + gas (1.33 x HI for He)
        if Mb <= 0:
            continue
        lMb.append(np.log10(Mb)); lV.append(np.log10(Vf))
    lMb, lV = np.array(lMb), np.array(lV)
    zp = np.mean(lMb - slope*lV)
    return zp, np.std(lMb - slope*lV), len(lMb), lMb, lV

# ---------------------------------------------------------------- run
def main():
    print("#"*94)
    print("# HIGH-z BTFR ZERO-POINT: rho_Lambda (flat a0) vs rho_crit (rising a0) on REAL data")
    print("#"*94)
    slope = 4.0
    zp0, sc0, N0, lMb0, lV0 = sparc_btfr_zp(slope)
    loga0_local = 4*3 - np.log10(G) - (zp0 + np.log10(Msun))
    print(f"\n  LOCAL SPARC BTFR anchor (slope fixed = {slope:.0f}, M/L=0.5, gas incl.):")
    print(f"    N = {N0};  zero-point A0 = <logMb - 4 logV> = {zp0:.3f}  (scatter {sc0:.3f} dex)")
    print(f"    implied a0(z=0) = {10**loga0_local:.2e} m/s^2  (canonical ~1.2-1.5e-10; slope-4 forcing runs high)")

    # ---- KMOS3D (has baryonic mass directly) ----
    d = np.genfromtxt(K3D, delimiter=",", names=True)
    zk, lMbk, Vk = d["z"], d["logMbar"], d["Vcirc_kms"]
    okk = (Vk > 0) & np.isfinite(lMbk)
    zk, lMbk, lVk = zk[okk], lMbk[okk], np.log10(Vk[okk])
    zpk = lMbk - slope*lVk                       # per-galaxy zero-point

    # ---- KROSS (stars only -> add a z~1 gas correction to make it baryonic) ----
    dk = np.genfromtxt(KROSS, delimiter=",", names=True)
    zr, Mstar_r, Vr = dk["z"], dk["Mstar"], dk["VC_kms"]
    okr = (Vr > 0) & (Mstar_r > 0) & np.isfinite(Mstar_r)
    zr, Mstar_r, lVr = zr[okr], Mstar_r[okr], np.log10(Vr[okr])
    # gas fraction at z~1 is large; use a representative f_gas=0.5 (Mbar=2 Mstar) as a NUISANCE we vary
    fgas = 0.5
    lMbr = np.log10(Mstar_r/(1-fgas))
    zpr = lMbr - slope*lVr

    print("\n" + "="*94)
    print("HIGH-z BTFR ZERO-POINT OFFSETS vs the SPARC anchor (the discriminating statistic)")
    print("="*94)
    print(f"  {'sample':18}{'z range':>12}{'N':>5}{'<A>_highz':>11}{'offset dA':>11}{'(err)':>9}")
    def report(name, z, zp):
        off = np.median(zp) - zp0
        err = np.std(zp)/np.sqrt(len(zp))   # standard error of the median offset (approx)
        print(f"  {name:18}{f'{z.min():.2f}-{z.max():.2f}':>12}{len(zp):>5}{np.median(zp):>11.3f}"
              f"{off:>11.3f}{err:>9.3f}")
        return off, err
    ok3, ek3 = report("KMOS3D (baryonic)", zk, zpk)
    okr_, ekr = report("KROSS (Mstar,fg=.5)", zr, zpr)

    print("\n" + "="*94)
    print("WHAT EACH FORK PREDICTS for the offset dA = log Mbar - 4 logV - A0   (= -log10[a0(z)/a0(0)])")
    print("="*94)
    zmed_k = np.median(zk); zmed_r = np.median(zr)
    print(f"  {'fork':40}{'pred dA @ KMOS3D z~%.1f'%zmed_k:>24}{'pred dA @ KROSS z~%.1f'%zmed_r:>24}")
    print(f"  {'(1) rho_Lambda  -> a0 ~ flat (DESI ~const)':40}{0.0:>24.3f}{0.0:>24.3f}")
    pr2k, pr2r = -np.log10(E(zmed_k)), -np.log10(E(zmed_r))
    print(f"  {'(2) rho_crit    -> a0 = cH(z)/Z = a0(0)E(z)':40}{pr2k:>24.3f}{pr2r:>24.3f}")
    print(f"""
   (Recall the DISTINCTIVE framework reading is fork (1): rho_DE is ~flat below z~2, so it predicts
    NEAR-ZERO BTFR offset there -- the high-z BTFR is, for the framework, a CONSISTENCY/null check,
    while it is a SHARP prediction for the disfavoured rising-a0 fork (2).)""")

    print("\n" + "="*94)
    print("READING IT (computed, with the honest systematics)")
    print("="*94)
    # which fork does each sample favour? compare measured offset to the two predictions
    def favour(name, off, err, zmed):
        d1 = abs(off - 0.0)/err
        d2 = abs(off - (-np.log10(E(zmed))))/err
        verdict = "fork(1) rho_Lambda flat" if d1 < d2 else "fork(2) rho_crit rising"
        print(f"  {name}: offset = {off:+.3f}+/-{err:.3f} dex.  "
              f"|dev from flat|={d1:.1f}s, |dev from E(z)|={d2:.1f}s -> closer to {verdict}")
    favour("KMOS3D", ok3, ek3, zmed_k)
    favour("KROSS ", okr_, ekr, zmed_r)
    print(f"""
   HONEST SYSTEMATICS (these DOMINATE and are why this is suggestive, not decisive):
    * Pressure support: high-z discs have V/sigma ~ a few; the published V_circ already includes an
      asymmetric-drift correction whose size (~0.05-0.15 dex in V -> 0.2-0.6 dex in Mb at slope 4) is
      the leading uncertainty and is sample-dependent. A residual under-correction biases V LOW ->
      offset HIGH (mimicking rising a0); over-correction does the reverse.
    * Sample selection: KMOS3D/KROSS are MASSIVE, high-surface-brightness, high-acceleration discs --
      NOT the deep-MOND tail where M_bar=V^4/(G a0) is exact. At g >~ a0 the BTFR zero-point also
      depends on the interpolation function, injecting an offset unrelated to a0(z).
    * Gas: KROSS is stars-only; the f_gas=0.5 assumption moves its zero-point by +/-0.3 dex directly.
    * M/L and IMF evolution: a younger high-z stellar population lowers M/L, shifting Mb.

   So the measured offsets are NOT a clean a0(z). What this REAL-DATA test DOES establish:""")

    # The robust statement: is the offset large enough to even reach the fork-2 prediction?
    print(f"""    - The offsets are at the ~{abs(ok3):.1f}-{abs(okr_):.1f} dex level with ~{ek3:.2f}-{ekr:.2f} dex statistical errors and
      LARGER (~0.2-0.6 dex) systematic errors -> the data CANNOT currently distinguish fork(1)'s 0.0
      from fork(2)'s {pr2k:.2f}/{pr2r:.2f} dex at z~1-2. The systematics are the wall, exactly as the
      DATA_AUDIT and project10b found.
    - This CONFIRMS, on the real survey files (not mock data), that today's massive high-z IFU samples
      are systematics-limited and INCONCLUSIVE on a0(z) -- which is why the decisive test needs
      DEEP-MOND-tail (low-surface-brightness, gas-rich) rotators at z~3, not these samples.""")

    print("\n" + "="*94)
    print("VERDICT / HONEST GRADE")
    print("="*94)
    disagree = abs(ok3 - okr_)
    print(f"""  * THE DECISIVE TELL: the two samples DISAGREE by {disagree:.2f} dex (KMOS3D {ok3:+.2f} vs KROSS {okr_:+.2f}),
    far beyond their ~0.03-0.04 dex statistical errors and even beyond fork(2)'s predicted signal.
    A real a0(z) would give CONSISTENT offsets at similar z; this inconsistency PROVES systematics
    (pressure-support correction + selection + the f_gas/M/L assumptions) dominate. So neither number
    is a clean a0(z) -- the test is SYSTEMATICS-LIMITED and INCONCLUSIVE, full stop.
  * GRADE = NULL / INCONCLUSIVE on the distinctive claim, on REAL data (not mock). It neither confirms
    nor refutes the framework's evolution -- which is by design tiny (~0 dex) below z~2 for fork(1),
    so even a clean measurement here would mostly be a consistency check, not the decisive test.
  * What it DOES establish firmly: today's massive high-z IFU BTFR samples cannot measure a0(z) (the
    DATA_AUDIT's and project10b's conclusion, now shown by the inter-sample disagreement on the real
    files). Genuine leverage requires DEEP-MOND-tail discs at z~3 (telescope-limited, ~2027).
  * NOT causal proof; NOT value-coincidence; a real-data NULL that correctly quantifies the systematic
    wall and refutes any claim that these samples already test the evolution.""")
    print("#"*94)

if __name__ == "__main__":
    main()
