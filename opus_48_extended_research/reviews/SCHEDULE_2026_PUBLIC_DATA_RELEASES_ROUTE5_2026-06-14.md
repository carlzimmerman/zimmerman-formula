# Route 5 — The 2026 Public-Data-Release Schedule (web-verified, framework-workable only)

*Opus 4.8, 2026-06-14. Each date web-verified against the official source (ESA Cosmos, DESI/LBL, MPE eROSITA,
Euclid Consortium, Rubin/LSST, arXiv). Confidence stated per row. Framework: a0 = c²√(Λ/32π) = 9.36e-11;
the ONE distinctive prediction is a0(z)/a0(0)=√(ρ_DE(z)/ρ_DE0) (#9). Both ways — realistic dates, realistic
workability, rival wins credited, N/A only where genuine. Quarantine held.*

## TL;DR
The single calendar-2026 release that materially moves the framework is **Gaia DR4 (2 Dec 2026, HIGH confidence)** —
it is the ONLY 2026 release that touches the framework's z=0 discriminators (wide binaries #6, EFE #5) with workable
public data. Everything else in 2026 is either (a) a z=0 channel where the framework is MOND-DEGENERATE (Euclid DR1
lensing #8, eRASS DR2 clusters #7 — workable, but tests *value-of-a0/MOND*, not the framework's distinctive a0(z)),
or (b) continuous archival inflow (JWST/MAST, ALMA) that feeds the distinctive high-z BTFR #9 forward model but has
no single 2026 "release date." **DESI's full-survey (DR3) dark-energy result — the a0(z) #9 cosmological input — is
2027, NOT 2026** (DESI completed observations Apr 2026; first 5-yr results expected 2027). The 2026 DESI item is the
full DR2 *spectra* going public (~mid-2026), which we already consume as the w0wa input.

---

## THE SCHEDULE (ranked by framework relevance)

### TIER 1 — directly tests a framework prediction with workable 2026 public data

**1. Gaia DR4 — 2 December 2026 (HIGH confidence; official ESA date)**
- Source: cosmos.esa.int/web/gaia/data-release-4 — "Wednesday, 2 December 2026," first 5.5 yr, ~500 TB, 2.8B sources,
  full astrometric time-series + greatly expanded non-single-star / astrometric-orbit catalogue.
- Bears on: **#6 wide binaries** (the framework's sharpest *named* z=0 discriminator) AND **#5 EFE/SEP** (Milky-Way
  disc kinematics at low internal acceleration).
- CAN WE WORK IT: **YES** — public, downloadable (Gaia archive), and we have the banked pipeline
  (route3_dr4_forecast.py, FRAMEWORK_GAMMA_S_FORWARD_MODEL_DR4_FORECAST, DR4_WIDEBINARY_FORECAST_ROUTE5).
- **Both ways (the honest caveat, from our own forecast):** DR4 will cleanly test the PREMISE (is there *any* low-a
  boost beyond Newton?) but is **systematics-limited, not statistics-limited**, and is unlikely to isolate the
  framework's gamma from standard-MOND. The framework's OWN sharp (dS-Unruh MI) interpolation predicts gamma≈1.137
  (+6.6%), even SMALLER than soft-MOND's +16%, pushing it closest to the Newton null and hardest to confirm; a0=9.36
  vs 1.20 shifts gamma by <0.07, below the optimistic ±0.03-0.05 DR4 systematic floor. So: workable and important,
  but MOND-DEGENERATE, not a clean framework-vs-MOND discriminator. RIVALS: LCDM/Newton predict ZERO boost (gamma=1)
  — DR4 genuinely tests this and LCDM could WIN if the null holds; standard-MOND predicts a similar/larger boost.

### TIER 2 — workable 2026 release, but a MOND-degenerate / shared channel (tests value-of-a0, not the framework)

**2. Euclid DR1 — 21 October 2026 (MEDIUM-HIGH confidence; Euclid Consortium / Caltech timeline)**
- Source: euclid.caltech.edu/page/data-release-timeline + cosmos.esa.int/web/euclid/euclid-dr1 — "expected 21 Oct
  2026," first Wide-Survey DR (~first ~1900 deg² to full depth equivalent), weak-lensing shear catalogues + cluster
  catalogues. (Q1 quick release was 19 Mar 2025; DR1 is the first science-grade public WL catalogue.)
- Bears on: **#8 weak-lensing RAR / morphology split** and **#7 clusters**.
- CAN WE WORK IT: **YES (with effort)** — public shear + cluster catalogues, downloadable; the framework predicts ONE
  lensing RAR with ZERO morphology split and a saturated α_∞. **Both ways:** this is a z=0 / shared-MOND channel —
  it tests the *value* of a0 and the morphology-split question, NOT the distinctive a0(z). RIVAL WIN credited: LCDM
  PREDICTS the +0.26 dex early/late-type lensing split (different halos by morphology) — the framework predicts no
  split, and the existing 8.6-9.2σ split is a FAILING front for the framework / a clean LCDM win. Euclid DR1 will
  sharpen exactly this comparison. Verdict: workable, important for confronting our weakest front, but not where the
  framework can WIN.

**3. eROSITA eRASS DR2 — ~mid-2026 (MEDIUM confidence; MPE erosita.mpe.mpg.de schedule, exact date not fixed)**
- Source: erosita.mpe.mpg.de/erass/ — "DR2 planned ~mid-2026" (DR1 was 31 Jan 2024; DR3 is H2-2028). Deeper all-sky
  (eRASS:4/5 cumulative) X-ray cluster catalogue + profiles for the **western/German hemisphere** (the half the
  German consortium can release publicly).
- Bears on: **#7 clusters** (residual missing-mass η after the MOND boost).
- CAN WE WORK IT: **YES** — public (western hemisphere), downloadable; extends the eRASS1 (Bulbul+2024, 9830
  clusters) sample we already use for the η(R500) audit. **Both ways:** clusters are an INHERITED MOND failure the
  framework does NOT fix — RIVAL WIN credited: LCDM accounts for the cluster mass with DM (η=1, LCDM WINS). Our own
  cluster work (CLUSTER_COMPREHENSIVE_REVIEW_SYNTHESIS) lands the true η~1.0-1.3 after XRISM kills the η~2 HSE branch;
  density-a0 flattens the deficit to ±30% but is NOT a cure. eRASS DR2 lets us re-run the η audit on a larger sample —
  it can DISCONFIRM the framework further, not confirm it. Hemisphere split caps the usable sky to ~half.

### TIER 3 — continuous archival inflow (no single 2026 "release date"); feeds the DISTINCTIVE #9 forward model

**4. JWST high-z resolved kinematics — continuous, public via MAST after ~12-mo proprietary period (HIGH confidence it
   exists; no single 2026 date)**
- Source: MAST; recent public sets — JADES/FRESCO/CONGRESS (272 Hα emitters z≈3.9-6.5, NIRCam grism), COSMOS-Web
  (public on MAST). New z≳3 resolved rotation curves drip into the public archive throughout 2026.
- Bears on: **#2 BTFR** and **#9 a0(z)** — the DISTINCTIVE high-z BTFR offset (−7.3% in V at z=3, −0.033 dex).
- CAN WE WORK IT: **YES, partially** — public reduced data on MAST; we have the forward model
  (highz_btfr_offset_forward_model_2026-06-14.py, route3_highz_kinematics_a0z_forecast.py). **Both ways (the real
  bottleneck):** this is the framework's ONE distinctive channel, BUT (a) JWST grism gives a few z≳3 BTFR points, not
  the ~30-60 needed for 3-5σ; (b) the DESI w0wa prior imposes a σ(β)≈0.5-0.6 FLOOR independent of sample size,
  capping single-redshift significance at ~1.6-2.0σ. So JWST 2026 inflow REFINES, does not DECIDE, #9. RIVAL: LCDM is
  N/A on a0(z) (no acceleration scale evolves); constant-a0 MOND predicts ZERO offset → JWST high-z BTFR is the
  cleanest in-principle discriminator, just not yet decisive.

**5. ALMA high-z cold-gas RCs — continuous archive (ALMA-ALPAKA-style mining); no 2026 release date (HIGH confidence it
   exists)**
- Source: ALMA Science Archive; ALMA-ALPAKA ([CO]/[CI]/[CII] resolved kinematics, z=0.5-4, non-lensed SF galaxies).
- Bears on: **#9 a0(z) / #2 BTFR** — cold-gas rotation gives the cleanest dynamical V_flat for the high-z BTFR offset.
- CAN WE WORK IT: **YES, partially** — fully public archive, downloadable; same DESI-prior floor caveat as JWST. ALMA
  cold-gas RCs are arguably the *cleanest* tracer for the offset (rotation-dominated discs), but the z≳3 sample is
  thin. Complements JWST; neither alone decides #9 in 2026.

### TIER 4 — 2026 activity, but NOT framework-workable as a distinctive test (listed for completeness, both ways)

**6. DESI — full DR2 spectra public ~mid-2026 (MEDIUM); full-survey (DR3) dark-energy result 2027 (HIGH that it's NOT
   2026)**
- Source: desi.lbl.gov — DR2 cosmology chains released 6 Oct 2025; full DR2 spectra public in 2026; observations
  COMPLETED Apr 2026; first 5-yr (DR3) dark-energy results "expected 2027."
- Bears on: **#9 a0(z) INPUT** (w0,wa → ρ_DE(z) → a0(z)). We ALREADY consume the DR2 w0=−0.752, wa=−0.86 chains as
  the bridge input (kessler2026, confront_li2026_dde_a0z, xu2026_w0wacdm_confront).
- CAN WE WORK IT: the 2026 spectra release adds little for us (we use the cosmology chains, already public). The
  *decisive* DESI update for #9 — the verdict on dynamical-DE — is **DR3 in 2027**, outside the 2026 window. Listed so
  the schedule is honest about the a0(z) input cadence. **Meta-falsifier reminder:** if DESI reverts to w=−1, the
  framework loses ALL distinctive content (identical to constant-a0 MOND).

**7. MUSE-DARK III (Ciocan+2026, arXiv 2604.22613) — PUBLISHED 2026, not a "release" (HIGH confidence)**
- 79 SF galaxies, 0.33<z<1.44, finds a0 RISING with z (a0(z~1)=2.38e-10; a1=1.59e-10/z). Bears DIRECTLY on **#9**.
- CAN WE WORK IT: the paper's measured points are already in hand (muse_dark_iii_confront.py). **Both ways (critical):**
  this is the CONTESTED rising-vs-declining front — MUSE-DARK measures a0 RISING, the framework predicts a0 DECLINING
  (√ρ_DE). Per the standing memos this WEAKENS/CONTESTS the declining reading but is LCDM-degenerate and
  non-diagnostic (the rising √ρ_total branch, not the framework's branch). It is a 2026 *publication*, not a future
  data release — no new 2026 download pending. Flagged because it's the most relevant 2026 a0(z) datum and it cuts
  AGAINST the framework's sign.

**8. SPT-3G / ACT DR6 CMB lensing — 2025-2026 releases (HIGH confidence the data exists; N/A as a framework test)**
- ACT DR6 lensing (43σ), SPT-3G M2PM + survey completion 2026, joint APS-L lensing power spectrum (61σ).
- Bears on: cluster mass calibration (#7 INDIRECTLY) only.
- CAN WE WORK IT: **NO (not as a distinctive test).** CMB lensing power spectrum is a ΛCDM growth-of-structure probe;
  the framework makes NO distinctive CMB-lensing prediction (it's a galaxy/cluster-dynamics modified-inertia theory).
  N/A-leaning. Could feed cluster mass priors at the margin, but not a framework test. EXCLUDED from workable.

**9. Vera Rubin / LSST — DP2 Jul-Sep 2026 (HIGH confidence); DR1/DRY1 LATER (not 2026)**
- Source: rubinobservatory.org / dp1.lsst.io — DP1 was 30 Jun 2025 (commissioning, 7 fields); DP2 Jul-Sep 2026 is
  STILL commissioning-grade (LSSTCam), and the 6-month DR1 was CANCELED in favor of the full Year-1 release (DRY1),
  which depends on the (unannounced) survey-start date and ~1 yr of processing → NOT 2026.
- Bears on: **#8 lensing** eventually.
- CAN WE WORK IT in 2026: **NO** — DP2 has no science-grade shear catalogue; the framework-workable WL catalogue
  (DRY1 shear) is post-2026. EXCLUDED from 2026 workable.

**10. XRISM — per-paper results 2025-2026, no clean bulk public DR (LOW-MEDIUM confidence on a 2026 archive release)**
- Perseus/Coma/A2029/Centaurus turbulence + bulk-velocity maps published through 2026; bears on **#7** (HSE bias →
  the η~2 branch). We already USE the XRISM result qualitatively (it kills the η~2 HSE branch, lowering true η to
  ~1.0-1.3).
- CAN WE WORK IT: **MARGINAL** — XRISM science is released paper-by-paper, not as a downloadable bulk catalogue we can
  re-fit; the GO archive opens per-target. We can ingest published velocity-dispersion numbers (as done) but cannot
  "work the data" in 2026 the way we work eRASS/Gaia catalogues. EXCLUDED from cleanly-workable.

---

## RIVAL-PREDICTION SUMMARY for the 2026-active channels (both ways)
- **LCDM** WINS clusters (#7: DM → η=1) and the lensing morphology split (#8: different halos by type → predicted
  split). LCDM predicts ZERO wide-binary boost (#6) and ZERO EFE (#5) — Gaia DR4 genuinely tests this, LCDM could win
  if null holds. LCDM is N/A on a0(z) (#9 — no evolving acceleration scale).
- **Standard MOND** matches the framework at z=0 (DR4 #6, Euclid lensing-RAR #8 value) and FAILS clusters the same
  way; crucially predicts a0(z)=CONSTANT → the discriminator vs the framework on #9 (JWST/ALMA/DESI-2027).
- **Verlinde** has a MOND-like scale + excess-lensing prediction (testable vs Euclid #8, mixed); N/A on
  wide-binaries/a0(z) specifics.
- **String / SUSY / QFT(SM) / GR-alone** — GENUINELY N/A on every galactic-dynamics channel here (no acceleration
  scale, no rotation-curve prediction); GR-alone = Newtonian = the LCDM column. No rival prediction manufactured.

## Confidence ledger (dates)
- Gaia DR4 2 Dec 2026 — HIGH (official ESA Cosmos date).
- Euclid DR1 21 Oct 2026 — MEDIUM-HIGH (Euclid Consortium/Caltech published timeline; ESA-side dates have slipped
  before).
- eRASS DR2 ~mid-2026 — MEDIUM (MPE schedule, exact day not pinned; hemisphere-limited).
- DESI full DR2 spectra ~mid-2026 — MEDIUM; DESI DR3/full-survey DE result 2027 — HIGH that it is NOT 2026.
- Rubin DP2 Jul-Sep 2026 — HIGH; Rubin science-WL (DRY1) — HIGH that it is NOT 2026.
- JWST/ALMA — continuous, no single date (HIGH that inflow exists).
- MUSE-DARK III, SPT-3G/ACT, XRISM — published 2026 results, not future downloadable DRs.
