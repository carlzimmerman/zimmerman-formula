# DATA — Jeanneau+26 low-acceleration bTFR refit (Lane D)

**2026-07-16.** Freeze: `FROZEN_CUTS.md` (written 19:34, BEFORE any per-galaxy number).
Script: `apply_frozen_cut.py` (exit 0; re-asserts the banked fork anchors and the paper's own
mass bookkeeping before printing anything). Subsample: `subsample.csv` (N=61).
Raw table: `jeanneau26_catalog_cds.csv` (verbatim CDS download).

## 1. Data provenance (ladder rung by rung, exactly what exists)

1. **arXiv:2603.28856 source** (fetched, 3.1 MB tarball): full LaTeX + figure PDFs, **no
   ancillary/machine-readable per-galaxy files**, no CDS-availability sentence in the text.
   Used for conventions (see §2).
2. **CDS/VizieR: the per-galaxy table IS public** — VizieR catalog **`J/A+A/709/A120`**
   ("z~1 star-forming galaxies Tully-Fisher relation", Jeanneau+, 2026, bibcode
   2026A&A...709A.120J, CC-BY-4.0, archive created 12-May-2026), single table
   `catalog` = the paper's **Table E1**, downloaded via TAPVizieR (`SELECT * FROM
   "J/A+A/709/A120/catalog"`), **95 rows = exactly their fiducial TFR fit sample** (their
   Tab. 4 bTFR row: a=3.14, b_ref=3.54, b=3.54±0.06, N=95).
3. VizieR rung not needed beyond rung 2; no printed-table extraction needed.

**Columns present:** Cluster, IdR21, IdHFFDS, RA/DE, zR21, muR21 (magnification, harmonic
mean; **no per-galaxy σ_μ column**), S/NMax, RPSF, **Reff** (arcsec, *intrinsic/source-plane*
single-Sérsic F160W radius from the Lenstool `cleanlens` forward model — the paper's √μ·Re/R_PSF
selection criterion confirms Reff is delensed), Incl, FB/T, logM\*(16/50/84), logSFR(16/50/84),
**logMHI** (incl. He, NeutralUniverseMachine scaling), **logMMol** (Tacconi+20 scaling),
**logMBar**, **logV1.8, logV2.0** (GalPaK3D+lensing circular velocity, pressure-support
corrected) with posterior stds, sigma0±.
Bookkeeping verified: M_bar = M\* + M_HI + M_mol to <1e-4 dex on all 95 rows.

## 2. Conventions taken from the paper (not re-derived)

- Fiducial bTFR: log M_bar = 3.14·log v_c(2Re) + b, local reference **Lelli+19 b_ref = 3.54**;
  their fit b = 3.54±0.06 → Δb = 0.00±0.06. Quality cuts already baked into the 95 rows
  (v1.8/σ0 > 1, Δv1.8/v1.8 < 30%, S/N_eff > 10, √μRe/R_PSF > 1/2, i > 30°, ZCONF=3) — per
  FROZEN_CUTS §2 we apply **their membership and nothing else**.
- Paper cosmology 0.3/0.7/70 used for the arcsec→kpc conversion of THEIR Reff (their
  convention; Planck-parameter stress changes nothing — same N=61, same median).
- Gas masses are **model-mediated by construction** (Tacconi+20 molecular + NUM HI with
  0.8 dex scatter in log τ_HI; their §4.2): every gas caveat of the parent ledger applies with
  MORE force here — the deep subsample's median gas fraction is **0.83** (full 95: 0.70).

## 3. Pipeline validity gate (frozen §3)

Full-95 median offset vs their line: **−0.037 dex** → reproduces their 0.00±0.06 within the
frozen ±0.05 gate. PASS (convention correctly reproduced before any subsample number).

## 4. The frozen cut, applied

`g_bar < 0.5·a0_canon` with g_bar from inverting g_obs = v_c(2Re)²/(2Re) through the
framework's own ν at a0_canon = 9.36e-11 (equivalently g_obs < 8.11e-11 m/s²):

- **N = 61 of 95** — NOT "roughly a third": this lensed dwarf-heavy sample sits much deeper
  in the a0 regime than the parent's typical-values forecast (median g_bar/a0 = **0.16**,
  quartiles 0.06/0.16/0.25, range 0.00–0.49). The parent's forecast dilution >0.6 is exceeded:
  **median dilution 0.76 (canonical a0), 0.82 (ALT's own a0)** — both footings' own a0, per
  the VERIFY correction.
- z range 0.55–1.45, median 1.06 (quartiles 0.80/1.06/1.26); logM\* 7.6–10.1 (median 8.9);
  median v_c(2Re) = 81 km/s; magnification median 2.4 (range 1.3–43.7).
- Boundary stress (frozen §4 fallback — no per-galaxy σ_μ exists): Re ±0.14 dex (their
  OII-vs-broadband structural MAD) moves N to 47/71; Planck-conversion N unchanged at 61.

## 5. Result (frozen estimator, both footings)

| quantity | value |
|---|---|
| PRIMARY median offset Δb (fixed slope 3.14) | **+0.140 dex** (bootstrap 68%: +0.102…+0.242; stat ±0.070; MAD 0.309) |
| weighted mean (check) | +0.217 dex |
| free-slope TLS (check) | slope 5.96 (68%: 4.60–8.52) → **1.4σ from 3.14, below the 2σ flag** (wide CI; restricted v-range) |
| honest band (stat ⊕ 0.20 gas ⊕ 0.16 local-ref ⊕ 0.06 convention) | **±0.272 dex** |
| gas stress (HI ×0.5 / ×2) | +0.089 / +0.320 dex |
| selection stress (Re −0.14/+0.14 dex) | +0.322 (N=47) / +0.102 (N=71) |
| fork predictions (exact per-galaxy, own ν, own a0): canonical pure-Λ | 0.000 |
| canonical DESI-CPL | −0.000 (range −0.020…+0.022) |
| **ALT ρ_tot/cH0** | **−0.243** (range −0.341…−0.106) |
| size-term residual (canonical + vdW14, deep-cancellation check) | −0.035 dex (full-95: −0.059) → cancels as forecast |
| ΛCDM halo term at median z=1.06 | −0.363 dex (does NOT cancel) |

Acceleration split inside their own sample (context): deep 61 at **+0.14**, high-acceleration
complement 34 at **−0.41** (median v 188 km/s) — at fixed slope 3.14 the residuals tilt
strongly with velocity/acceleration. At essentially the same z on both sides, this is a
**gas-model/slope shape effect** (NUM HI feeds the low-mass end hardest), not a redshift drift
of anything.

## 6. Verdict (mechanical, frozen §5 — with the rule collision disclosed)

- **Two frozen rules fire simultaneously** because Δb landed POSITIVE — away from BOTH
  footings, a case the freeze did not anticipate: (i) B(0.272) > |Δ_ALT|(0.243) →
  **STILL-UNDERPOWERED**; (ii) |Δb−0| < B while |Δb−Δ_ALT| = 0.383 > B → nominal "ALT-side
  constraint at 1.41σ".
- **Headline: STILL-UNDERPOWERED, with a 1.41σ ALT-side lean (not a constraint).** The
  structural rule wins because the honest band exceeds the fork separation — a measurement AT
  the ALT point could not have been distinguished from canonical, so the test cannot deliver
  a clean kill in either direction; and the central value itself is gas-model-suspect: the
  +0.14 median moves to +0.09/+0.32 under the HI ×0.5/×2 stress alone, in a subsample that is
  83% scaling-relation gas by median. The stat-only 5.5σ-from-ALT (2.0σ-from-canonical) is
  printed for transparency and is **DO-NOT-CLAIM** (it treats NUM-HI/Tacconi gas as noiseless).
- Signs, straight: the deep third does NOT lean ALT — the drift ALT needs (−0.24) is 0.38 dex
  away from the measured +0.14, on stat errors a large gap; but the same gas model that makes
  the point sit HIGH is the binding systematic, and it is big enough to absorb the whole gap.
  Symmetrically: this is NOT a canonical win either (0.51σ from 0 with a band wider than the
  separation, and the positive offset means even canonical is only "compatible", not hit).
- **What the parent forecast got wrong, honestly:** the forecast "canonical ~0.00 vs ALT −0.15
  …−0.20, separation larger than the subsample stat error" was right about the separation
  (−0.24 exceeded it) and about the stat error (±0.07), but wrong that this would decide
  anything: the coherent gas-model floor (±0.20) does not shrink with N, and the deep cut
  RAISES the gas-mediated fraction. The deep cut buys acceleration leverage and pays for it
  in gas-model exposure — the trade is a wash at current gas-measurement quality.
- **A real if modest product survives:** on its OWN terms the refit disfavors the undiluted
  ALT drift at ~1.4σ with everything carried honestly — the first published-data number
  directly ON the ALT branch in the near-deep regime (the parent had only the full-sample
  0.65σ). ALT is dented, not killed; canonical is compatible, not confirmed.

## 7. ΛCDM-degeneracy (mandatory statement)

The deep cut does NOT convert this into an MI-vs-ΛCDM test. The size term cancels (−0.035,
confirmed) but the ΛCDM halo-scaling drift (−0.363 at z=1.06) does not — it sits on the same
side as ALT and 0.12 dex beyond it, exactly the parent's degeneracy. What changes: a
DEEP-regime FLAT-or-positive zero-point now pressures ALT *and* the no-gas-compensation ΛCDM
halo edge simultaneously (both predict falling); both escape the same way, via rising gas
fractions — which is precisely the (model-mediated) gas the measurement is built on. So the
subsample CAN say: "the ALT drift is not seen where it should be least diluted (1.4σ, gas-
capped)"; it CANNOT say anything about MI-vs-ΛCDM, and a negative result would have been
ALT/ΛCDM-degenerate anyway. Footing-internal, exactly as banked.

## 8. Deviations / fallbacks log (frozen-file discipline)

1. **No deviation in selection or estimator.** Cut, estimator, error model run as frozen.
2. Fallback used (pre-authorized, frozen §4): per-galaxy σ_μ not published → magnification
   carried via the authors' global prescription (their uniform ±0.2 dex M_bar error, which
   they state covers magnification/SED systematics) + the Re ±0.14 dex selection stress;
   lens-model velocity spread is 0.003 dex MAD (their App. D) — negligible.
3. arcsec→kpc used the PAPER's 0.3/0.7/70 (frozen file was silent on the conversion
   cosmology; parent-banked Planck values change nothing — logged, stress-tested).
4. Decision-rule collision (§6) resolved toward the structural (UNDERPOWERED) verdict with
   the σ-distances reported verbatim — disclosed rather than silently picking a rule.
