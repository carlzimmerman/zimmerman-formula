# QX26 frozen criteria: does stellar IMF variation explain the hot/early-type step?

Frozen before any script producing a graded number. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Footings
(canonical a0 9.3603e-11, alt 1.1312e-10) never pooled. Shared rules: closure_2026_11_06/SWARM_BRIEF.md.

## Question

QX20 found a step: hot and early-type systems sit +0.2 to +0.45 dex above SPARC under the plain law. QX18 found
that Salpeter stellar masses would pass the X-ray ellipticals (+0.071 / +0.053), where Kroupa fails (+0.210 /
+0.189).

Hypothesis tested (a baryon-accounting systematic, not new gravity): massive early types have heavier IMFs, so
Kroupa/Chabrier stellar masses under-count their stars, and that is part or all of the step.

## The one IMF relation (chosen by rule before grading)

Rule: use the published relation that
- covers the sigma range of the graded early types (about 100-350 km/s);
- is homogeneous across low and high sigma;
- has coefficients the lane can verify.

That is **Posacki, Cappellari, Treu, Pellegrini & Ciotti 2015, MNRAS 446, 493** (ATLAS3D + SLACS):

    log10 alpha = (0.38 +- 0.04) log10(sigma_e / 200 km/s) - (0.06 +- 0.01),   alpha = (M/L)_dyn / (M/L)_Salpeter-pop

The coefficients were checked by web lookup on 2026-11-06 against the arXiv abstract (arXiv:1407.5633). That
lookup is PROVISIONAL per the record's rule; the published PDF was not checked.

Disclosed limits of this choice:
- alpha comes from Jeans dynamical models that include a dark halo. It is therefore a halo-model-processed input,
  and the label is conditional on it.
- The relation's own range is sigma_e of about 90-400 km/s.

Only the central coefficients are used. Their errors are reported as a systematic, not graded.

Applied stellar mass: M_* = alpha(sigma_e) x M_*^Salpeter-pop.
- Where a class's masses are Kroupa or Chabrier, M_*^Salp = M_*^K / 0.63 (Salpeter-to-Chabrier/Kroupa conversion
  0.63, Madau & Dickinson 2014; literature, transcribed).
- The Humphrey+2006 table carries its own ups_salp, and that is used directly.

## Per-class inputs (literature, transcribed; provisional)

**X-ray ellipticals** (QX18's data, Humphrey+2006): central sigma_0 from HyperLEDA, transcribed by the lane and not
read from a file.

| Galaxy | sigma_0 (km/s) |
|---|---|
| NGC720 | 239 |
| NGC1407 | 271 |
| NGC4125 | 226 |
| NGC4261 | 309 |
| NGC4472 | 282 |
| NGC4649 | 331 |
| NGC6482 | 302 |

sigma_e = 0.87 sigma_0 (aperture correction sigma(R)/sigma_e = (R/R_e)^-0.066 at R = R_e/8, Cappellari+2006).
Robustness: every elliptical label must hold with all sigma_0 scaled x0.9 and x1.1. Otherwise the label is
BRACKET-DEPENDENT and the primary is reported with that tag.

**KiDS early-type lenses** (QX21 T1: Brouwer+2021 Fig. 8, CFG61 K1 bins 8-14): there is no per-lens sigma.
- Proxy: a sigma_e bracket {130, 170, 210} km/s for isolated early types at log M_* 10.3-11 (literature bracket,
  ATLAS3D mass-sigma). The primary is 170.
- KiDS masses are Chabrier (LePhare; literature, transcribed).
- The correction applies to M_* only. f_cold is set to 0 for early types, the maximum correction.
- Late types get no correction: alpha(sigma_e <= 100) times 1/0.63 is about 1.06, which is below the M_* systematic.
  This is reported.

**dSphs** (sigma 7-12 km/s): outside the relation's range. Rule: no correction (Kroupa floor). Also reported: the
alpha that would be needed to null QX21's +0.2.

**X-COP and groups** (QX20's points): M_* = M_b - M_gas (X-COP), and f* = 0.5 x M_gas (groups, QX20's primary). The
stellar term is scaled by the IMF factor at the BCG / central sigma_e bracket:
- X-COP: {250, 300, 350}, primary 300;
- groups: {200, 250, 300}, primary 250.

Stellar masses are taken as Kroupa-equivalent. That is stated, not checked.

**SPARC bulges** (consistency): no per-galaxy bulge sigma is on disk. Bulge Upsilon = 1.4 U is multiplied by the IMF
factor at sigma_e = {100, 150, 200} km/s. The factors are alpha / 0.63 relative to the record's Kroupa-like
baseline, floored at 1.

## Graded statistics and lines

- **(1) Ellipticals.** D_IMF = mean over galaxies of the mean over 2/4/8 R_e of log10(M_obs / M_law(M_*^IMF)).
  - Line: |D_IMF| <= 0.15 (G7).
  - Fraction removed: F = (D_K - D_IMF) / D_K.
- **(2) KiDS.**
  - Predicted change: Delta = mean over K1 bins of s_law(g_k) x log10 f, where s_law = dlog g_law / dlog g_bar at the
    bin's g_bar and f is the early-type mass factor. Points shift along g_bar by log f.
  - Residual: R = (D - D_law) - Delta. QX21: D - D_law = +0.158 +- 0.064.
  - F = Delta / (D - D_law).
- **(3) dSphs and SPARC.** dSphs: reported. SPARC: the PAPER67 line (rms <= 0.110 and median U 0.50-0.80, QX8's
  algebraic-mode grader) must still hold at every bulge factor in the bracket. If it fails, the IMF relation BREAKS
  SPARC.
- **(4) X-COP and groups.** F = fraction of the class-mean offset removed. X-COP line: |mean| <= 0.05 (HO1).

Labels per class, on the primary inputs:
- **STEP EXPLAINED BY IMF:** F >= 0.8 and the class line is met (for KiDS: |R| < 2 x 0.064).
- **PARTLY:** 0.2 <= F < 0.8.
- **NOT:** F < 0.2.

## Known answers and controls (separate outputs, qx26_MUTATE.*)

- KA1: alpha switched off (Kroupa; ups_krou; f = 1) reproduces QX18's D (+0.210 / +0.189) to 1e-3, and QX20's
  X-COP / groups class means to 1e-3.
- KA2: the SPARC algebraic grade at bulge factor 1 reproduces QX8 KA1 (0.054087 @ 0.52, 0.053718 @ 0.44) to 1e-5.
- MUTATE: a planted alpha x 2 must over-correct the ellipticals (F > 1.0). If it does not, the test has no power.

## Scope

A label here is about stellar-mass accounting under one published IMF relation with halo-processed dynamics. It is
not a statement about gravity, and it adopts nothing.
