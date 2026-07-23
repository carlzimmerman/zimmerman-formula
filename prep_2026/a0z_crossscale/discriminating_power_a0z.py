#!/usr/bin/env python3
"""
DISCRIMINATING POWER + REQUIRED PRECISION for the framework a0(z) prediction.

Builds on (does NOT rebuild/contradict) desi_posterior_a0z.py and desi_posterior_a0z_fullband.py
(same FULL closed-form law, same DESI DR2 w0waCDM posteriors, same 2x2 correlated Cholesky MC,
same seed 0). Footing-independence of the RATIO is proved exactly in footing_honesty_audit.py;
here it is re-demonstrated numerically (two footings -> identical ratio) so this script stands alone.

The law under test (de Sitter-Unruh MODIFIED INERTIA):
    a0(z) = a0(0) * sqrt(rho_DE(z)/rho_DE0)
    CPL:   rho_DE(z)/rho_DE0 = (1+z)^{3(1+w0+wa)} * exp(-3 wa z/(1+z))
    RATIO: a0(z)/a0(0)       = (1+z)^{1.5(1+w0+wa)} * exp(-1.5 wa z/(1+z))   [FULL, never truncated]

This law is NON-MONOTONIC: a small low-z BUMP (ratio>1, peak ~z0.35, +~3.6% at Pantheon+ central),
crossing 1 near z~0.9, DECLINING to ~0.74 at z=3. Never Taylor/truncate it.

TWO COMPLEMENTARY QUANTITIES (kept strictly separate to avoid a manufactured win):

  (a) THEORY-SIDE separation [ceiling on discriminating power set by CURRENT cosmology]:
      given DESI's (w0,wa) posterior, the PREDICTED ratio has central R_bar(z) and spread
      sigma_pred(z). Separation-from-flat = |R_bar - 1| / sigma_pred. This is how confidently
      the framework-as-informed-by-DESI ALREADY predicts a departure from flat=1, BEFORE any
      galaxy a0 is measured. Even a PERFECT galaxy measurement cannot make the framework-vs-flat
      test exceed this ceiling without better COSMOLOGY (that is the Rubin/Euclid forecast, a
      separate file). Today it tops out ~2-2.5 sigma at z=3.

  (b) MEASUREMENT-SIDE required precision [galaxy side]:
      ASSUME the framework's central R_bar(z) is the truth. What fractional 1-sigma precision
      sigma_meas on a MEASURED a0(z)/a0(0) rejects flat=1 at 3 sigma and 5 sigma?
      sigma_meas = |R_bar - 1| / N_sigma. This is a pure model-independent detection-of-departure
      requirement; sigma_pred does NOT enter it. A real confirmation needs BOTH sides to deliver:
      cosmology must shrink sigma_pred (Rubin/Euclid) AND galaxies must reach sigma_meas (part b).

  (c) DEEP-MOND MEASUREMENT PENALTY (calibration rule 4): a0 is read out as a0=g_obs^2/g_bar, so
      d ln a0 = 2 d ln g_obs - d ln g_bar => sigma(ln a0) ~ 2 sigma(ln g_obs). The per-point log
      scatter on a0 is DOUBLED. Consequences: the UNDERLYING RC/RAR data must be ~2x tighter than
      the precision quoted on a0(z), and reaching a target aggregate precision needs 4x the sample
      vs a naive (un-amplified) estimate.

  (d) HONEST testability verdict per z + the single most realistic (z, precision, instrument).

LCDM-DISSOLUTION: if w -> -1 the ratio collapses to EXACTLY 1 for all z and is INDISTINGUISHABLE
from constant-a0 MOND. The entire prediction is CONDITIONAL on DESI's w0wa evolution being real.

MUSE-DARK III (Ciocan 2026) rising-a0 is LCDM-degenerate TENSION/WATCH, NOT confirmation; a mild
rise is predicted ONLY in the tiny low-z bump (+~3.6%, exactly where a0 is hardest to measure).

No 'theory closed'. A weak-testability / NULL outcome is verified as rigorously as a win.
"""
import numpy as np
from scipy.special import erfcinv

# ---------------------------------------------------------------------------------------------
# shared law + DESI DR2 posteriors (identical to the parent scripts)
# ---------------------------------------------------------------------------------------------
def a0ratio(z, W0, WA):
    """FULL non-monotonic closed form a0(z)/a0(0); z scalar, W0/WA scalars or arrays."""
    return (1.0 + z)**(1.5*(1.0 + W0 + WA)) * np.exp(-1.5*WA*z/(1.0 + z))

DATASETS = [   # (label, w0, sw0, wa, swa, corr, LCDM-excl-sigma)
    ("DESI+CMB+Pantheon+", -0.838, 0.055, -0.62, 0.22, -0.86, 2.8),
    ("DESI+CMB+DESY5",     -0.752, 0.057, -0.86, 0.22, -0.86, 4.2),
    ("DESI+CMB+Union3",    -0.667, 0.088, -1.09, 0.31, -0.87, 3.8),
]
ZTEST = [0.35, 1.0, 2.0, 3.0]

def mc_pair(w0, sw0, wa, swa, corr, N=400000):
    L = np.linalg.cholesky(np.array([[sw0**2, corr*sw0*swa], [corr*sw0*swa, swa**2]]))
    g = np.random.default_rng(0)                       # seed 0, parity with parent scripts
    with np.errstate(divide="ignore", over="ignore", invalid="ignore"):
        pr = np.array([w0, wa]) + g.standard_normal((N, 2)) @ L.T
    return pr[:, 0], pr[:, 1]

# ---------------------------------------------------------------------------------------------
# footing-independence: demonstrate numerically that the RATIO is identical on both footings
# (canonical a0(0)=9.36e-11 vs alt a0(0)=1.13e-10). Rule (2): ONE ratio band, never two.
# ---------------------------------------------------------------------------------------------
print("="*92)
print("FOOTING-INDEPENDENCE OF THE RATIO  (Rule 2: one band, not two)")
print("="*92)
A0_CANON, A0_ALT = 9.36e-11, 1.13e-10
zc = np.array(ZTEST)
r_from_canon = (A0_CANON * a0ratio(zc, -0.838, -0.62)) / (A0_CANON * a0ratio(0.0, -0.838, -0.62))
r_from_alt   = (A0_ALT   * a0ratio(zc, -0.838, -0.62)) / (A0_ALT   * a0ratio(0.0, -0.838, -0.62))
print(f"  a0(0) footings: canonical {A0_CANON:.3e} m/s^2 (rho_DE/cH_Lambda, Z=sqrt(32pi/3))")
print(f"                  alt       {A0_ALT:.3e} m/s^2 (rho_total/cH0)")
print(f"  ratio a0(z)/a0(0) from canonical footing at z={ZTEST}:\n     {np.round(r_from_canon,6)}")
print(f"  ratio a0(z)/a0(0) from alt       footing at z={ZTEST}:\n     {np.round(r_from_alt,6)}")
assert np.allclose(r_from_canon, r_from_alt, rtol=0, atol=1e-12), "footing leaked into the ratio!"
print("  max |canonical - alt| ratio difference = "
      f"{np.max(np.abs(r_from_canon - r_from_alt)):.2e}  -> IDENTICAL (a0(0), Z cancel).")
print("  => The RATIO depends only on (w0,wa,z). Only the ABSOLUTE a0(z)=ratio*a0(0) carries the")
print("     footing (a0(3) ~= 0.74*{9.36e-11 canonical, 1.13e-10 alt}). Load-bearing scale: note both.")

# ---------------------------------------------------------------------------------------------
# (a) THEORY-SIDE separation from flat, per z, per dataset:  |R_bar - 1| / sigma_pred
# ---------------------------------------------------------------------------------------------
print("\n" + "="*92)
print("(a) THEORY-SIDE SEPARATION FROM FLAT=1  (ceiling set by CURRENT DESI cosmology, no galaxy data)")
print("    N_sigma = |median - 1| / sigma_pred ; sigma_pred = std of the DESI-propagated predicted ratio")
print("    (+) = predicted RISE (low-z bump), (-) = predicted DECLINE. Near the z~0.9 crossover ~ 0.")
print("="*92)
central = {}   # (label, z) -> (median, sigma_pred, signed_sep)
for label, w0, sw0, wa, swa, corr, excl in DATASETS:
    W0, WA = mc_pair(w0, sw0, wa, swa, corr)
    print(f"\n[{label}]  (LCDM excl {excl:.1f}s)   w0={w0:+.3f}, wa={wa:+.3f}, corr {corr:+.2f}")
    print(f"    {'z':>5} | {'median':>7} | {'sigma_pred':>10} | {'signed sep':>11} | note")
    print(f"    {'-'*5}-+-{'-'*7}-+-{'-'*10}-+-{'-'*11}-+-----")
    for z in ZTEST:
        r = a0ratio(z, W0, WA)
        med, sd = float(np.median(r)), float(np.std(r))
        sep = (med - 1.0) / sd                    # signed: +rise / -decline
        central[(label, z)] = (med, sd, sep)
        note = ("bump/RISE" if med > 1.0 else "decline")
        if abs(med - 1.0) < 0.02: note = "near crossover (~null)"
        print(f"    {z:>5.2f} | {med:>7.3f} | {sd:>10.3f} | {sep:>+11.2f} | {note}")
    # parity: one-sided tail decline significance at z=3 (matches parent's method)
    r3 = a0ratio(3.0, W0, WA)
    frac = max(np.mean(r3 >= 1.0), 0.5/len(r3))
    print(f"    [parity] z=3 one-sided tail decline significance ~ {np.sqrt(2)*erfcinv(2*frac):.1f} sigma")

print("\n  READING (a): the theory-side separation is NON-MONOTONIC and has TWO local peaks -- the")
print("  low-z BUMP (z~0.35) and the high-z DECLINE (z~3) -- with a NULL at the z~0.9 crossover.")
print("  Both peaks sit near ~2 sigma at DESI-current precision; that ~2-2.5 sigma is the CEILING a")
print("  perfect galaxy a0(z) could reach against flat FOR THE FRAMEWORK today. Beating it needs")
print("  better COSMOLOGY (Rubin/Euclid -> forecast_rubin_a0z.py), not just better galaxy data.")

# ---------------------------------------------------------------------------------------------
# (b) MEASUREMENT-SIDE required precision: reject flat=1 at 3 / 5 sigma given central prediction
#     sigma_meas = |R_bar - 1| / N_sigma      (pure detection-of-departure; sigma_pred not involved)
# ---------------------------------------------------------------------------------------------
print("\n" + "="*92)
print("(b) MEASUREMENT-SIDE REQUIRED PRECISION  (assume framework central R_bar(z) is truth)")
print("    sigma_meas on a0(z)/a0(0) needed to reject flat=1:  sigma_meas = |R_bar-1| / N_sigma")
print("="*92)
print(f"    {'dataset':22} {'z':>5} {'R_bar':>6} {'|effect|':>8} | {'req sigma_meas 3s':>17} | {'5s':>7}")
print(f"    {'-'*22} {'-'*5} {'-'*6} {'-'*8} + {'-'*17} + {'-'*7}")
req = {}
for label, *_ in [(d[0],) for d in DATASETS]:
    for z in ZTEST:
        med, sd, sep = central[(label, z)]
        eff = abs(med - 1.0)
        s3, s5 = eff/3.0, eff/5.0
        req[(label, z)] = (med, eff, s3, s5)
        tag3 = f"{100*s3:5.2f}%"
        tag5 = f"{100*s5:5.2f}%"
        hard = "  <- sub-% : impractical" if s3 < 0.01 else ""
        print(f"    {label:22} {z:>5.2f} {med:>6.3f} {eff:>8.3f} | {tag3:>17} | {tag5:>7}{hard}")
print("\n  READING (b): the required a0 precision is set by the EFFECT SIZE, which is wildly z-dependent:")
print("   - z=0.35 bump (~3.6%): needs ~1.2% (3s) / ~0.7% (5s) on a0  -> brutal.")
print("   - z=1 (near crossover, ~1%): needs ~0.3% -> effectively UNTESTABLE (degenerate with flat).")
print("   - z=2 (~13%): needs ~4-5% (3s) / ~2.5-3% (5s) on a0.")
print("   - z=3 (~26%): needs ~7-8% (3s) / ~4-5% (5s) on a0  -> the MOST FORGIVING target.")
print("  NOTE the anti-correlation: the BIG effect is at high z (forgiving precision) but the good")
print("  DATA is at low z (tiny effect). This tension is the crux of the testability verdict (d).")

# ---------------------------------------------------------------------------------------------
# (c) DEEP-MOND PENALTY -> underlying RC precision (~2x tighter) + required sample size N
# ---------------------------------------------------------------------------------------------
print("\n" + "="*92)
print("(c) DEEP-MOND PENALTY: a0=g_obs^2/g_bar => sigma(ln a0)=2 sigma(ln g_obs). Rule (4).")
print("    Underlying RC precision must be ~2x tighter; N ~ (sigma_pt(a0)/sigma_meas)^2.")
print("="*92)
# per-point log-scatter on g (natural log). SPARC-quality floor 0.10 dex is OPTIMISTIC; high-z
# resolved kinematics (turbulence, beam smearing, pressure support, inner-disk-only) are far worse.
DEX = np.log(10.0)
scatter_cases = [("SPARC-quality floor, 0.10 dex", 0.10),
                 ("realistic high-z, 0.20 dex",    0.20)]
print("  per-point sigma(ln g) -> amplified per-point sigma(ln a0) = 2*sigma(ln g):")
for name, dexg in scatter_cases:
    sg = dexg*DEX
    print(f"    {name:32}: sigma(ln g)={sg:.3f} -> sigma_pt(ln a0)={2*sg:.3f} ({2*dexg:.2f} dex)")
print()
print(f"    {'z':>5} {'target':>7} {'req sigma_meas(a0)':>18} {'req sigma_g (/2)':>17} "
      f"{'N (0.10dex)':>12} {'N (0.20dex)':>12}")
print(f"    {'-'*5} {'-'*7} {'-'*18} {'-'*17} {'-'*12} {'-'*12}")
# use the Pantheon+ (representative central) effect sizes for the headline required-N table
for z in ZTEST:
    med, eff, s3, s5 = req[("DESI+CMB+Pantheon+", z)]
    for tgt_name, sm in (("3 sigma", s3), ("5 sigma", s5)):
        req_sg = sm/2.0                                     # underlying RC precision (2x tighter)
        N_opt = (2*0.10*DEX / sm)**2                        # SPARC-floor per-point scatter
        N_hiz = (2*0.20*DEX / sm)**2                        # realistic high-z per-point scatter
        # z=1 effect is sub-% -> N explodes; cap the printed value with a marker
        n_opt_s = f"{N_opt:,.0f}" if N_opt < 1e7 else ">1e7"
        n_hiz_s = f"{N_hiz:,.0f}" if N_hiz < 1e7 else ">1e7"
        print(f"    {z:>5.2f} {tgt_name:>7} {100*sm:>16.2f}% {100*req_sg:>16.2f}% "
              f"{n_opt_s:>12} {n_hiz_s:>12}")
print("\n  READING (c): even at the SPARC-quality floor the low-z bump needs ~1500 (3s) / ~4000 (5s)")
print("  deep-MOND rotation curves at ~0.6% underlying precision -- and the deep-MOND regime")
print("  (galaxy outskirts, g<a0) is barely reachable at z~0.35 (needs SKA-era deep HI; Halpha")
print("  traces the inner high-g disk). z=2-3 need only ~40-340 curves at the SPARC floor, BUT at")
print("  realistic high-z scatter (0.20 dex) that quadruples to ~150-1400, and those outer-disk,")
print("  low-acceleration curves scarcely exist above z~1. Doubling per-point scatter = 4x the N.")

# ---------------------------------------------------------------------------------------------
# (d) HONEST testability verdict per z + the single most realistic (z, precision, instrument)
# ---------------------------------------------------------------------------------------------
print("\n" + "="*92)
print("(d) TESTABILITY VERDICT PER z  +  the single most realistic kill-or-confirm")
print("="*92)
verdicts = [
 ("z=0.35 (BUMP, +3.6%)",
  "needs ~1.2%/0.7% a0 (3/5s) -> ~0.6% underlying RC, ~1500-4000 curves; deep-MOND regime "
  "INACCESSIBLE at this z (SKA-era HI). VERDICT: effect too small, data unreachable -> not realistic."),
 ("z=1.0 (near z~0.9 crossover)",
  "effect ~1% and sign-ambiguous across datasets (0.99 P+ vs 1.03 U3); needs ~0.3% a0. "
  "VERDICT: sits on the null -> effectively UNTESTABLE regardless of precision."),
 ("z=2.0 (~13% decline)",
  "needs ~4-5%/2.5-3% a0 (3/5s) -> ~2-2.5% underlying RC, ~120-340 curves (SPARC floor) / "
  "~500-1400 (high-z scatter). z~1.5-2.5 is exactly where JWST NIRSpec/grism + ALMA CO/[CII] "
  "resolved kinematics samples are growing. VERDICT: the SWEET SPOT (effect vs data availability)."),
 ("z=3.0 (~26% decline)",
  "CLEANEST effect, most forgiving precision (~7-8%/4-5% a0 -> ~3.5-4% RC, ~40-100 curves at "
  "the SPARC floor). BUT z=3 outer-disk RCs in the deep-MOND regime barely exist and are "
  "turbulence/beam-smearing dominated (scatter >>0.10 dex). VERDICT: cleanest in principle, "
  "data-starved in practice."),
]
for z_lbl, txt in verdicts:
    print(f"\n  {z_lbl}:\n    {txt}")

print("\n  " + "-"*88)
print("  SINGLE MOST REALISTIC (z, precision, instrument):")
print("    z ~ 2,  target sigma_meas(a0) ~ 5% (=> ~2.5% underlying RC precision, ~a few hundred to")
print("    ~1000 resolved outer-disk kinematics),  instrument = JWST NIRSpec-IFU/grism + ALMA")
print("    CO/[CII] dynamics (ELT/MOSAIC in the 2030s). This yields a ~3 sigma model-independent")
print("    detection of the ~13% a0 decline. Rationale: z=3 has the biggest signal but the RC data")
print("    quality collapses and the deep-MOND regime is unreachable; z=0.35 needs ~1% precision on")
print("    an inaccessible regime; z=1 is on the null. z~2 is the only place where a large-enough")
print("    effect and an attainable (if campaign-level, >2030) data set overlap.")

print("\n  " + "-"*88)
print("  OVERARCHING HONEST CAVEATS (not overrideable by any single favorable number):")
for c in [
  "1. CEILING: even a perfect galaxy a0(z) tops out at the part-(a) ~2-2.5 sigma framework-vs-flat "
  "ceiling until DESI's w0wa sharpens (Rubin/Euclid). Galaxy precision alone cannot exceed it.",
  "2. CONDITIONAL: if w -> -1 the ratio is EXACTLY 1 for all z and is INDISTINGUISHABLE from "
  "constant-a0 MOND. All discriminating power is inherited from DESI's w0wa evolution being real.",
  "3. FOOTING: the RATIO is footing-independent (proved); only the absolute a0(z)=ratio*a0(0) "
  "carries the footing (9.36e-11 canonical vs 1.13e-10 alt). Both noted where scale is load-bearing.",
  "4. PENALTY: a0=g_obs^2/g_bar doubles per-point log scatter -> underlying RC precision must be "
  "~2x tighter and the required sample ~4x larger than a naive estimate.",
  "5. MUSE-DARK III rising-a0 is LCDM-degenerate TENSION/WATCH, NOT confirmation; the only predicted "
  "rise is the tiny low-z bump (+3.6%, at the z where a0 is hardest to measure). Not cited as support.",
  "6. No 'theory closed'. The galaxy-side distinctive test is a >2030, campaign-level prospect; a "
  "weak-testability finding is stated as plainly as a win would be.",
]:
    print("   * " + c)

# ---------------------------------------------------------------------------------------------
# regression check vs parent medians (self-consistency)
# ---------------------------------------------------------------------------------------------
PARENT = {"DESI+CMB+Pantheon+": {1.0:0.989, 2.0:0.874, 3.0:0.775},
          "DESI+CMB+DESY5":     {1.0:1.009, 2.0:0.862, 3.0:0.737},
          "DESI+CMB+Union3":    {1.0:1.031, 2.0:0.855, 3.0:0.707}}
print("\n" + "="*92)
print("REGRESSION CHECK vs desi_posterior_a0z.py medians (z=1,2,3; tol 0.004)")
print("="*92)
ok = True
for label, *_ in [(d[0],) for d in DATASETS]:
    for z in (1.0, 2.0, 3.0):
        here = central[(label, z)][0]
        d = abs(here - PARENT[label][z])
        if d > 0.004: ok = False
        print(f"    {label:20} z={z:.0f}: here={here:.3f} parent={PARENT[label][z]:.3f} "
              f"d={d:.4f} [{'OK' if d<=0.004 else 'MISMATCH'}]")
assert ok, "regression mismatch vs parent script"
print("  ALL MEDIANS MATCH parent to <= 0.004.")
print("\nEXIT 0")
