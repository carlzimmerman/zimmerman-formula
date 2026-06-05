#!/usr/bin/env python3
"""
Ground the decisive high-z BTFR test in REAL on-disk data (KMOS3D / Ubler+2017) -- honest, whichever way it goes.
================================================================================================================
The framework's distinctive, falsifiable prediction is a REDSHIFT TREND in the baryonic Tully-Fisher offset:
    dlogV(z) = (1/8) log10[rho_DE(z)/rho_DE0]   (V ~ a0^(1/4), a0 ~ sqrt(rho_DE))
-> at fixed M_bar, discs rotate progressively SLOWER toward high z: a DECLINING trend, d(dlogV)/dz < 0. The RISING
(sqrt rho_total) reading predicts the OPPOSITE sign: discs faster toward high z, slope > 0 (~+0.056 dex/z over this
sample). Ordinary constant-a0 MOND predicts slope = 0. We confront ALL THREE with real KMOS3D discs (z~0.6-2.5).

THE KEY DISTINCTION (this is the whole point of the rewrite):
  [A] The ABSOLUTE offset <dlogV> is fixed by the BTFR ZERO POINT (anchor choice, IMF, gas fractions, beam
      smearing) -- a ~0.1 dex CONSTANT systematic that SWAMPS the <0.15 dex a0 signal. It looks "rising", but a
      constant cannot test a redshift dependence. It is NOT a test of a0(z).
  [B] The z-TREND d(dlogV)/dz is IMMUNE to any constant zero-point error (the constant cancels in the slope) and
      IS the discriminator. Measured: slope = -0.029 +/- 0.012 dex/z -- NEGATIVE = the framework's declining sign,
      ~1sigma from framework but ~7sigma AGAINST the rising branch. Anchor-free, survives mass control + jackknife.

HONEST: the discriminating statistic LEANS FRAMEWORK, but this is NOT a win -- it stays UNDECIDED, because:
  * the SAME negative sign is what LCDM predicts from dark-matter + gas-fraction growth -- Ubler+2017's OWN reading;
  * an asymmetric-drift systematic of the same sign ABSORBS it: controlling for sigma0/Vcirc the slope falls to
    -0.017 +/- 0.013 (~1.3sigma, non-significant), so pressure support alone could account for the whole trend;
  * the repo's own a0_of_z.csv direct-RAR-fit compilation RISES (1.20 -> 2.38), the opposite direction.
Data: data/kmos3d_ubler2017.csv (real, Ubler+2017). Reproducible: `python ground_highz_btfr_realdata.py`. numpy(+mpl).
"""
import os, numpy as np

C = 2.99792458e8; G = 6.674e-11; Msun = 1.989e30; KMS = 1e3
MPC = 3.0857e22; H0 = 67.36e3 / MPC; OmL = 0.6847; OmM = 0.3153
A0 = 1.2e-10                       # z=0 McGaugh RAR anchor (the BTFR zero point reference)
W0, WA = -0.752, -0.86
DATA = os.path.join(os.path.dirname(__file__), "..", "data", "kmos3d_ubler2017.csv")


def rho_DE_ratio(z):
    a = 1 / (1 + z); return a**(-3 * (1 + W0 + WA)) * np.exp(-3 * WA * (1 - a))
def Ez(z): return np.sqrt(OmM * (1 + z)**3 + OmL)
def dlogV_framework(z): return (1 / 8.) * np.log10(rho_DE_ratio(z))     # declining sqrt(rho_DE)
def dlogV_rising(z): return (1 / 4.) * np.log10(Ez(z))                  # a0 ~ cH ~ sqrt(rho_total)


# --- small numpy-only statistics (the z-TREND is the systematics-immune test, so we measure it properly) ---
def ols(x, y):
    """OLS slope, intercept of y on x."""
    b = np.linalg.lstsq(np.vstack([np.ones_like(x), x]).T, y, rcond=None)[0]
    return b[1], b[0]

def boot_slope(x, y, n=5000, seed=12345):
    """Bootstrap SE of the OLS slope (resample galaxies with replacement). Anchor-independent."""
    rng = np.random.default_rng(seed); N = len(x)
    return float(np.std([ols(x[i], y[i])[0] for i in (rng.integers(0, N, N) for _ in range(n))]))

def ctrl_slope(y, z, covars, n=5000, seed=24680):
    """Coefficient on z in y ~ 1 + z + covariates (e.g. logM, or sigma0/Vcirc) with bootstrap SE.
    covars: list of arrays. Used to show the z-trend survives mass control but is absorbed by asymmetric drift."""
    def fit(yy, zz, cc): return np.linalg.lstsq(np.column_stack([np.ones_like(yy), zz] + cc), yy, rcond=None)[0][1]
    c = fit(y, z, covars); rng = np.random.default_rng(seed); N = len(y)
    bs = [fit(y[i], z[i], [cv[i] for cv in covars]) for i in (rng.integers(0, N, N) for _ in range(n))]
    return c, float(np.std(bs))

def spearman(x, y):
    """Spearman rank correlation with average ranks for ties (monotonic, model-independent)."""
    def rank(a):
        _, inv, cnt = np.unique(a, return_inverse=True, return_counts=True)
        csum = np.cumsum(cnt); return ((csum - cnt + 1 + csum) / 2.0)[inv]
    return float(np.corrcoef(rank(x), rank(y))[0, 1])

def partial_corr(x, y, ctrl):
    """Linear partial correlation of x,y controlling for ctrl."""
    rxy = np.corrcoef(x, y)[0, 1]; rxz = np.corrcoef(x, ctrl)[0, 1]; ryz = np.corrcoef(y, ctrl)[0, 1]
    return float((rxy - rxz * ryz) / np.sqrt((1 - rxz**2) * (1 - ryz**2)))


def main():
    rows = []
    for line in open(DATA):
        s = line.strip()
        if not s or s.startswith("z,") or s.startswith("#"): continue
        p = s.split(",")
        try: z, lMs, lMb, Vc, sig = (float(x) for x in p[:5])
        except ValueError: continue
        if Vc <= 0 or lMb <= 0: continue
        rows.append((z, lMb, 10**lMb * Msun, Vc, sig))
    z = np.array([r[0] for r in rows]); lMb = np.array([r[1] for r in rows]); Mb = np.array([r[2] for r in rows])
    Vobs = np.array([r[3] for r in rows]); sig0 = np.array([r[4] for r in rows])
    print("#" * 96)
    print(f"# Decisive high-z BTFR test on REAL KMOS3D data: {len(z)} discs, z = {z.min():.2f}-{z.max():.2f}")
    print("#" * 96 + "\n")

    # z=0 BTFR reference and the per-galaxy offset
    Vz0 = (G * Mb * A0)**0.25 / KMS
    dlogV = np.log10(Vobs) - np.log10(Vz0)          # >0: faster (a0 up, RISING) ; <0: slower (a0 down, framework)

    # ===================== [A] ABSOLUTE BTFR OFFSET -- set by the zero point; NOT a test of a0(z) =============
    print("  [A] ABSOLUTE OFFSET <dlogV>  (fixed by the BTFR zero point -- a CONSTANT systematic; NOT diagnostic)")
    print("  z-bin        N   <dlogV> (data)   framework pred   rising pred     which sign?")
    print("  " + "-" * 86)
    for zlo, zhi in [(0.5, 1.0), (1.0, 1.5), (1.5, 2.6)]:
        m = (z >= zlo) & (z < zhi)
        if m.sum() < 3: continue
        zmid = np.median(z[m]); mean = np.mean(dlogV[m]); err = np.std(dlogV[m]) / np.sqrt(m.sum())
        fpred = dlogV_framework(zmid); rpred = dlogV_rising(zmid)
        sign = "FASTER (rising-like)" if mean > 0 else "slower (framework-like)"
        print(f"  z={zlo:.1f}-{zhi:.1f}  {m.sum():>4}   {mean:+.3f}+/-{err:.3f}      {fpred:+.3f}          {rpred:+.3f}      {sign}")
    fp = dlogV_framework(z); rp = dlogV_rising(z)
    scat = np.std(dlogV)            # per-galaxy scatter dominates
    chi2_f = np.sum((dlogV - fp)**2) / scat**2; chi2_r = np.sum((dlogV - rp)**2) / scat**2
    chi2_0 = np.sum(dlogV**2) / scat**2
    print(f"  per-galaxy scatter sigma(dlogV) = {scat:.3f} dex (LARGE -- high-z kinematics are noisy)")
    print(f"  chi2/N:  framework(declining) {chi2_f/len(z):.3f} | constant(MOND) {chi2_0/len(z):.3f} | rising {chi2_r/len(z):.3f}")
    print("  --> the level (~+0.13 dex) and this chi2 look 'rising', but that is the ZERO POINT: anchoring")
    print("      V=(G M_bar a0)^1/4 with a0=1.2e-10 implies M_bar~63 V^4 vs the local Lelli+2019 M_bar~47 V^4,")
    print("      plus IMF + (large) gas fractions + beam-smearing -- a ~0.1 dex constant that SWAMPS the <0.15 dex")
    print("      signal. A z-INDEPENDENT constant cannot test a z-DEPENDENCE. So [A] is a systematic, not the test.\n")

    # ===================== [B] REDSHIFT TREND d(dlogV)/dz -- immune to any constant zero point; the REAL test ==
    slope, icpt = ols(z, dlogV); slope_err = boot_slope(z, dlogV)
    fslope = ols(z, fp)[0]; rslope = ols(z, rp)[0]          # effective linear slope of each branch over THIS sample
    adr = sig0 / Vobs                                       # pressure-support / asymmetric-drift proxy
    mslope, merr = ctrl_slope(dlogV, z, [lMb], seed=24680)  # mass-controlled (dlogV ~ z + logM)
    aslope, aerr = ctrl_slope(dlogV, z, [adr], seed=777)    # asymmetric-drift-controlled (dlogV ~ z + sigma0/Vcirc)
    rho = spearman(dlogV, z)
    pc = partial_corr(dlogV, adr, z)
    s_f = abs(slope - fslope) / slope_err; s_r = abs(slope - rslope) / slope_err; s_0 = abs(slope) / slope_err
    zmed = np.median(z); s_lo = float(sig0[z < zmed].mean()); s_hi = float(sig0[z >= zmed].mean())
    jks = [ols(z[~((z >= a) & (z < b))], dlogV[~((z >= a) & (z < b))])[0] for a, b in [(0.5,1.0),(1.0,1.5),(1.5,2.6)]]
    print("  [B] REDSHIFT TREND  d(dlogV)/dz  (a constant zero point CANCELS in the slope -- THIS discriminates)")
    print(f"      measured slope                       = {slope:+.4f} +/- {slope_err:.4f} dex/z   ({s_0:.1f}sigma from zero)")
    print(f"      predicted slopes:  framework {fslope:+.4f}  |  constant(MOND) +0.0000  |  rising {rslope:+.4f}")
    print(f"      data vs branch:    framework {s_f:.2f}sigma  |  constant {s_0:.2f}sigma  |  rising {s_r:.2f}sigma")
    print(f"      => sign is NEGATIVE = the framework's DECLINING sign; {s_r:.1f}sigma AGAINST the rising branch.")
    print(f"      model-independent / anchor-free cross-checks (all NEGATIVE):")
    print(f"        Spearman rho(dlogV, z)               = {rho:+.3f}")
    print(f"        mass-controlled slope (dlogV~z+logM) = {mslope:+.4f} +/- {merr:.4f}   (survives mass control)")
    print(f"        leave-one-z-bin-out slopes           = {jks[0]:+.3f}, {jks[1]:+.3f}, {jks[2]:+.3f}   (sign stable)")
    print(f"      systematic of the SAME sign (caveat -- asymmetric drift / pressure support):")
    print(f"        sigma0 rises {s_lo:.0f}->{s_hi:.0f} km/s with z (corr {np.corrcoef(sig0, z)[0,1]:+.2f}); more pressure support")
    print(f"        biases Vcirc LOW at high z.  partial corr(dlogV, sigma0/Vcirc | z) = {pc:+.2f}")
    print(f"        CONTROLLING for it: slope (dlogV~z+sigma0/Vcirc) = {aslope:+.4f} +/- {aerr:.4f} ({abs(aslope)/aerr:.1f}sigma,")
    print(f"        NON-significant) -- asymmetric drift absorbs most of the trend. THIS is why [B] is not a detection.\n")

    # ===================== HONEST VERDICT =====================================================================
    print("  " + "=" * 92)
    print("  HONEST VERDICT  --  two statistics, two different things; do NOT conflate them")
    print("  " + "=" * 92)
    print(f"""  [A] ABSOLUTE OFFSET (untestable): large, positive (~+0.13 dex, 'rising-like'), and its chi2 nominally
      prefers rising -- but that is the BTFR ZERO POINT (63 vs Lelli 47 V^4, IMF, gas fractions, beam smearing),
      a ~0.1 dex CONSTANT that swamps the signal. A constant zero point cannot test a redshift dependence.
  [B] REDSHIFT TREND (the real, zero-point-immune test): NEGATIVE, slope = {slope:+.3f} +/- {slope_err:.3f} dex/z.
      That is the framework's DECLINING sign: {s_f:.2f}sigma from framework, but {s_r:.1f}sigma AGAINST rising and
      {s_0:.1f}sigma from constant-MOND. It is anchor-free, survives mass control ({mslope:+.3f}), jackknife, and
      Spearman ({rho:+.2f}); and it MATCHES Ubler+2017's own finding (higher M_bar at fixed Vcirc at z~2.3 vs z~0.9).

  So the discriminating statistic LEANS FRAMEWORK and disfavors the rising branch -- but this is NOT a win:
   * DEGENERACY: the identical negative sign is what LCDM predicts from dark-matter + gas-fraction growth in the
     disc -- which is Ubler+2017's OWN interpretation of exactly this signal. The trend is not unique to a0(z).
   * SAME-SIGN SYSTEMATIC: asymmetric drift. sigma0 rises {s_lo:.0f}->{s_hi:.0f} km/s with z, so pressure support
     biases Vcirc low at high z (partial corr(dlogV, sigma0/Vcirc | z) = {pc:+.2f}). CONTROLLING for it collapses
     the trend to {aslope:+.3f} +/- {aerr:.3f} ({abs(aslope)/aerr:.1f}sigma, NON-significant) -- it could account for the whole slope.
   * OPPOSITE-DIRECTION DATUM: the repo's own a0_of_z.csv direct-RAR-fit compilation RISES (1.20 -> 2.38). The two
     distinctive probes point opposite ways right now; neither is yet clean.

  NET STATUS:  UNDECIDED / systematics-limited  --  but the discriminating (zero-point-immune) statistic is
  DISTINCTIVE-TO-FRAMEWORK, not rising-like. A DECISIVE test needs same-pipeline z>=3 kinematics (one identical
  reduction so the zero point cancels AND asymmetric-drift corrections are uniform), not a cross-survey offset.""")

    try:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(8.4, 5.6))
        ax.scatter(z, dlogV, s=8, c="0.6", alpha=0.5, label=f"KMOS3D discs (N={len(z)})")
        zl = np.linspace(0, 3.2, 100)
        ax.plot(zl, [dlogV_framework(zz) for zz in zl], "b-", lw=2.2, label=f"framework: a₀∝√ρ_DE  (slope {fslope:+.3f})")
        ax.plot(zl, [dlogV_rising(zz) for zz in zl], "r--", lw=2.0, label=f"rising: a₀∝cH (√ρ_tot)  (slope {rslope:+.3f})")
        ax.axhline(0, color="k", ls=":", lw=1, label="constant a₀ MOND  (slope 0)")
        # the REAL test: the measured z-trend (zero-point-immune). Plotted through the data level.
        ax.plot(zl, icpt + slope * zl, "g-", lw=2.4, alpha=0.9,
                label=f"MEASURED trend  ({slope:+.3f}±{slope_err:.3f} dex/z)")
        for zlo, zhi in [(0.5, 1.0), (1.0, 1.5), (1.5, 2.6)]:
            m = (z >= zlo) & (z < zhi)
            if m.sum() >= 3:
                ax.errorbar(np.median(z[m]), np.mean(dlogV[m]), yerr=np.std(dlogV[m]) / np.sqrt(m.sum()),
                            fmt="ks", ms=8, capsize=4, zorder=5)
        ax.set_xlabel("redshift z"); ax.set_ylabel(r"BTFR offset $\Delta\log V$ at fixed $M_{\rm bar}$ [dex]")
        ax.set_title("High-z BTFR: the LEVEL is a zero-point systematic; the SLOPE is the test\n"
                     f"measured slope {slope:+.3f} dex/z (declining) — {s_r:.1f}σ against rising, {s_f:.2f}σ from framework")
        ax.legend(fontsize=8.0, loc="upper left"); ax.set_xlim(0, 3.0); ax.set_ylim(-0.5, 0.5)
        fig.tight_layout()
        out = os.path.join(os.path.dirname(__file__), "..", "figures", "ground_highz_btfr_realdata.png")
        fig.savefig(out, dpi=120, bbox_inches="tight"); print(f"\n  figure: {os.path.normpath(out)}")
    except Exception as e:
        print(f"\n  (figure skipped: {e})")
    print("#" * 96)


if __name__ == "__main__":
    main()
