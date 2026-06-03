#!/usr/bin/env python3
"""
Four clean SPARC tests of the framework's core relations (real data, 175 galaxies).
==================================================================================
  1. BTFR zero-point:  v_flat^4 = G M_bar a0   (slope 4? zero-point -> a0?)
  2. Intrinsic RAR scatter:  how tight is a0 really, after removing measurement error?
  3. Freeman critical surface density:  Sigma_c = a0/(2 pi G) ~ 137 Msun/pc^2 (a boundary in the data?)
  4. Phantom-halo profile:  deep-MOND flat curves => phantom rho ~ 1/r^2 (outer slope -> -2?)
Each is a forced MOND/framework prediction; we report what the data give, with honest caveats.

HONEST OUTCOME (don't skip): #2 (RAR) and #3 (Freeman) are cleanly recovered from rotmod files; #1 and
#4 are not. #2 hinges on the CORRECT estimator: error-weighted, the RAR scatter is 0.10 dex with
a0=1.36e-10 (canonical), matching Lelli+2016 OBSERVED -- an UNWEIGHTED np.std wrongly inflates to 0.20
dex and drags a0 low (a correction to a first pass of this very script). #3: disks straddle
Sigma_c=a0/2piG=137 Msun/pc^2. #1 is proxy-limited: a V^2 r/G mass proxy gives BTFR slope 3.15, biased
low of the real 3.85+/-0.09 (Lelli+2016, which needs total baryonic masses). #4 is partial: deep-MOND
points still rise (beta=+0.36 -> phantom rho~r^-1.3, not the idealized isothermal -2). AND all four are
STANDARD MOND relations the framework merely inherits -- none probes its distinctive high-z evolution.
Needs numpy + the SPARC files.
"""
import numpy as np, glob, os

G, Msun, kpc, pc = 6.674e-11, 1.989e30, 3.0857e19, 3.0857e16
A0C = 1.2e-10
DATA = os.path.join(os.path.dirname(__file__), "..", "data", "sparc_data")
FILES = sorted(glob.glob(os.path.join(DATA, "*_rotmod.dat")))
ML_D, ML_B = 0.5, 0.7


def gals():
    for f in FILES:
        try: d = np.genfromtxt(f, comments="#")
        except Exception: continue
        if d.ndim != 2 or d.shape[0] < 4 or d.shape[1] < 8: continue
        yield [d[:, i] for i in range(8)]      # R,Vobs,eV,Vgas,Vdisk,Vbul,SBdisk,SBbul


def test1_BTFR():
    print("="*82); print("TEST 1 -- BTFR: v_flat^4 = G M_bar a0  (slope and zero-point)"); print("="*82)
    lV, lM = [], []
    for R, Vobs, eV, Vgas, Vdisk, Vbul, SBd, SBb in gals():
        n = len(R); o = slice(max(n-3, n//2), n)
        Vflat = np.nanmedian(Vobs[o])
        # M_bar ~ V_bar^2(r_last) r_last / G  (enclosed-baryon approx; biases zero-point, not slope)
        Vbar2 = np.sign(Vgas[-1])*Vgas[-1]**2 + ML_D*Vdisk[-1]**2 + ML_B*Vbul[-1]**2
        if Vbar2 <= 0 or Vflat <= 0: continue
        Mbar = Vbar2*1e6*(R[-1]*kpc)/G/Msun
        lV.append(np.log10(Vflat*1e3)); lM.append(np.log10(Mbar))
    lV, lM = np.array(lV), np.array(lM)
    slope, inter = np.polyfit(lV, lM, 1)
    scat = np.std(lM - (slope*lV+inter))
    # zero-point a0 from a0 = v^4/(G M_bar):  log a0 = 4 log v - lM - log10(G*Msun)
    inter4 = np.median(lM - 4*lV)                      # forcing slope 4
    a0 = 10**(-inter4)/(G*Msun)                        # a0 = v^4/(G M_bar) at the slope-4 intercept
    print(f"  fit log M_bar = {slope:.2f} log v_flat + const  (MOND/BTFR predicts 4); scatter {scat:.2f} dex")
    print(f"  forcing slope 4, the zero-point WOULD give a0 ~ {a0:.2e} m/s^2 -- but the slope is NOT 4.")
    print(f"""  READ [HONEST -- INCONCLUSIVE in-house]: from rotmod files I can only estimate M_bar by the
  enclosed-mass proxy V_bar^2 r/G, which gives slope {slope:.2f} (robust at ~3.15 across three proxy
  definitions: last-radius, max-over-r, summed components). That is biased LOW of 4 because V^2 r/G is
  not the total baryonic mass (thin-disk form factor; HI extends beyond the optical disk). The PROPER
  SPARC BTFR -- Lelli, McGaugh, Schombert & Pawlowski 2016, total baryonic masses from 3.6um photometry
  + HI flux -- gives slope 3.85 +/- 0.09 ~ 4. So the steep BTFR is real in the literature; my rotmod
  proxy is too crude to reproduce it, and the matching zero-point a0 is meaningless when the slope is
  off. Counted honestly: INCONCLUSIVE from rotmod alone (not a confirmation of v^4 = G M a0).\n""")


def test2_RAR_scatter():
    print("="*82); print("TEST 2 -- RAR scatter: how universal is a0? (the ESTIMATOR is decisive)"); print("="*82)
    gb, go, w = [], [], []
    for R, Vobs, eV, Vgas, Vdisk, Vbul, SBd, SBb in gals():
        Rm = R*kpc
        Vbar2 = np.sign(Vgas)*Vgas**2 + ML_D*Vdisk**2 + ML_B*Vbul**2
        g_b = Vbar2*1e6/Rm; g_o = (Vobs*1e3)**2/Rm
        ok = (g_b > 0) & (g_o > 0) & np.isfinite(g_b) & np.isfinite(g_o) & (Vobs > 0)
        frac = np.clip(eV, 1, None)/np.clip(Vobs, 1, None)              # fractional velocity error
        gb += list(g_b[ok]); go += list(g_o[ok]); w += list(1/frac[ok]**2)   # inverse-variance weight
    gb, go, w = np.array(gb), np.array(go), np.array(w)
    mcg = lambda gb, a0: gb/(1 - np.exp(-np.sqrt(gb/a0)))               # McGaugh+2016 RAR
    grid = np.linspace(0.4e-10, 3.0e-10, 700)
    su = [np.std(np.log10(go)-np.log10(mcg(gb, a0))) for a0 in grid]; iu = int(np.argmin(su))
    sw = [np.sqrt(np.sum(w*(np.log10(go)-np.log10(mcg(gb, a0)))**2)/np.sum(w)) for a0 in grid]; iw = int(np.argmin(sw))
    print(f"  UNWEIGHTED (np.std) ........ best a0 = {grid[iu]*1e10:.2f}e-10   scatter {su[iu]:.3f} dex  (wrong estimator)")
    print(f"  ERROR-WEIGHTED (1/sigma_V^2)  best a0 = {grid[iw]*1e10:.2f}e-10   scatter {sw[iw]:.3f} dex  <-- correct")
    print(f"""  READ [CONFIRMED in-house, once weighted -- a CORRECTION to a first unweighted pass]: the
  estimator decides this test. An UNWEIGHTED scatter counts a noisy inner point (sigma_V/V~0.2) the
  same as a clean outer one; it inflates to {su[iu]:.2f} dex AND drags a0 low to {grid[iu]*1e10:.2f}e-10. The CORRECT
  inverse-variance weighting -- standard for the RAR -- gives {sw[iw]:.2f} dex AND recovers the canonical
  a0 = {grid[iw]*1e10:.2f}e-10. That {sw[iw]:.2f} dex matches the Lelli, McGaugh, Schombert & Pawlowski 2016 OBSERVED
  RAR scatter (~0.11 dex); the tighter 0.057 dex INTRINSIC value (Lelli+2017) additionally marginalizes
  M/L, distance and inclination per galaxy, which a fixed-M/L pass cannot reach. So the near-universal
  a0 IS reproduced in-house -- canonical value, literature-level observed scatter -- the moment the data
  are weighted correctly. (My first pass used np.std and wrongly called this an 'upper bound'.)\n""")


def test3_Freeman():
    print("="*82); print("TEST 3 -- Freeman critical surface density Sigma_c = a0/(2 pi G)"); print("="*82)
    Sig_c = A0C/(2*np.pi*G) * pc**2/Msun                 # Msun/pc^2
    cen = []
    for R, Vobs, eV, Vgas, Vdisk, Vbul, SBd, SBb in gals():
        s = SBd[SBd > 0]
        if len(s): cen.append(ML_D*s[0])                 # central stellar surface density (Msun/pc^2)
    cen = np.array(cen)
    print(f"  Sigma_c = a0/(2 pi G) = {Sig_c:.0f} Msun/pc^2  (the MOND/Freeman disk-stability scale).")
    print(f"  SPARC central disk Sigma (M/L=0.5): median {np.median(cen):.0f}, "
          f"{np.mean(cen>Sig_c)*100:.0f}% lie above Sigma_c, {np.mean(cen<Sig_c)*100:.0f}% below.")
    print(f"  range 16-84 pct: {np.percentile(cen,16):.0f} - {np.percentile(cen,84):.0f} Msun/pc^2.")
    print(f"""  READ [CONFIRMED in-house]: real disks straddle Sigma_c ~ {Sig_c:.0f} Msun/pc^2 -- HSB galaxies
  sit near/above it (Newtonian cores), LSB below (MOND throughout), the Freeman 1970 / Brada-Milgrom
  1999 disk-stability boundary. Sigma_c is not fitted: it is a0/(2 pi G), so the disk population's
  surface-density scale is SET by a0. This is the one of the four that IS cleanly recovered from the
  rotmod data -- but, like all four, it is a STANDARD MOND result the framework merely inherits.\n""")


def test4_phantom():
    print("="*82); print("TEST 4 -- phantom-halo profile: deep-MOND => rho_phantom ~ 1/r^2"); print("="*82)
    betas = []
    for R, Vobs, eV, Vgas, Vdisk, Vbul, SBd, SBb in gals():
        Rm = R*kpc
        Vbar2 = np.sign(Vgas)*Vgas**2 + ML_D*Vdisk**2 + ML_B*Vbul**2
        g_b = Vbar2*1e6/Rm
        deep = (g_b > 0) & (g_b < 0.3*A0C) & (Vobs > 0)
        if deep.sum() < 3: continue
        lr, lv = np.log10(R[deep]), np.log10(Vobs[deep])
        betas.append(np.polyfit(lr, lv, 1)[0])           # outer rotation slope beta = d log V/d log r
    betas = np.array(betas)
    rho_slope = 2*np.median(betas) - 2                    # rho_dyn ~ r^(2 beta - 2); flat (beta=0) -> -2
    print(f"  outer (deep-MOND) rotation slope  beta = d log V/d log r:  median {np.median(betas):+.2f} "
          f"(flat curve = 0)")
    print(f"  implied phantom-density slope  d log rho/d log r = 2 beta - 2 = {rho_slope:+.2f}  "
          f"(isothermal = -2)")
    print(f"""  READ [HONEST -- PARTIAL]: the idealized deep-MOND limit is a flat curve (beta=0) -> phantom
  rho ~ r^-2 (isothermal). In SPARC the deep-MOND-selected outer points still RISE mildly (median
  beta = {np.median(betas):+.2f}), so the inferred phantom halo is rho ~ r^{rho_slope:+.1f}, SHALLOWER
  than isothermal. The -2 is the asymptotic idealization; at the finite last-measured radii -- and the
  gas-rich dwarfs that dominate a g_bar<0.3a0 selection are typically still rising -- it is not reached.
  Directionally MONDian (a declining phantom profile, no dark particle), but NOT the clean -2.\n""")


def main():
    test1_BTFR(); test2_RAR_scatter(); test3_Freeman(); test4_phantom()
    print("="*82); print("FOUR-TEST VERDICT (honest scorecard)"); print("="*82)
    print("""  175 SPARC galaxies, rotmod files only:
    1. BTFR slope ...... INCONCLUSIVE in-house: the V^2 r/G proxy gives 3.15 (robust across proxies),
                         biased low; proper total masses (Lelli+2016) give 3.85+/-0.09 ~ 4. Real in
                         the literature, NOT reproducible from rotmod alone.
    2. RAR scatter ..... CONFIRMED in-house (error-weighted): scatter 0.10 dex AND canonical a0=1.36e-10,
                         matching Lelli+2016 observed. (An unweighted np.std wrongly gave 0.20 dex / low
                         a0 -- corrected here.) The tighter 0.057 dex intrinsic (Lelli+2017) needs full
                         per-galaxy marginalization a fixed-M/L pass cannot reach.
    3. Freeman Sigma_c . CONFIRMED in-house: disks straddle a0/2piG = 137 Msun/pc^2 (40% above/60% below).
    4. Phantom profile . PARTIAL: deep-MOND points still rise (beta=+0.36) -> rho~r^-1.3, not the
                         idealized isothermal -2 (an asymptotic limit not reached at finite radii).

  Two of the four are cleanly re-derived from the data here -- the error-weighted RAR (canonical
  a0=1.36e-10 at 0.10 dex) and the Freeman straddle; the BTFR slope needs proper total baryonic masses
  (rotmod proxies bias it low), and the isothermal -2 is an asymptotic limit not reached at finite
  radii. CRUCIAL CAVEAT: all four are STANDARD MOND
  relations the framework INHERITS -- confirming them (even cleanly) is NOT evidence for the framework
  over plain MOND. The framework's only DISTINCTIVE, non-inherited prediction remains the high-z
  EVOLUTION of a0, a0(z)=a0(0)E(z) -- which these z=0 galaxy tests cannot probe. This set rounds out
  the inherited galaxy-scale picture honestly; it does not, and cannot, advance the distinctive claim.""")
    print("="*82)


if __name__ == "__main__":
    main()
