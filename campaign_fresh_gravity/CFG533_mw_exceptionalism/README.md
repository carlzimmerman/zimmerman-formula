# CFG533: "MW exceptionalism". The law gets EXTERNAL outer slopes right; the MW's steep 15–27.5 kpc decline is a MW-specific tension (LOCALISED TO MW as frozen), but the MW is not an outlier against the external scatter

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (45897b75d).
- **Script:** `cfg533_mw_exceptionalism.py`. Runs in a few seconds; nice 10, 2 threads.
  - Outputs: `cfg533.out` and `cfg533_results.json`.
  - MUTATE: `CFG533_MUTATE=1` writes `cfg533_MUTATE.out` and `cfg533_results_MUTATE.json`. It exits 1, meaning DETECTED.
- **Data:** only data on disk.
  - SPARC: `SPARC_Lelli2016c.mrt` and the 175 rotmod files (not SPARC_table.txt).
  - The CFG532 `.tex` sources in `../_external_data/cfg532_work/src/`.
  - `cfg532b_results.json`, read for the MW numbers.
  - Nothing was downloaded.
- **Settings:**
  - κ = ½ is FITTED. Footings 9.36e-11 / 1.13e-10, never pooled.
  - Kernel ν_mono; no EFE.
  - The cold energy's MASS is still required. This is not "theory closed", and nothing here says the data favour the framework.

## A. External control on SPARC

**Setup:**
- Sample: Q ≤ 2 and Inc ≥ 30°, which leaves 153 galaxies.
- Law: ALG on rotmod baryons (Υ 0.5 / 0.7).
  - Control K2 reproduces CFG516's ALG rms exactly: 0.1117 / 0.1005.
- The MW's 15–27.5 kpc window, mapped two declared ways:
  - **S-Rd:** R/R_d ∈ [6, 11], using R_d,MW = 2.5 kpc.
  - **S-rM:** R/r_M ∈ [1.508, 2.765] canonical and [1.657, 3.038] alt, using r_M,MW = 9.95 / 9.05 kpc.
- Slope estimator: the same as CFG532's.
- Δ = b_data − b_law. The ensemble error comes from the galaxy-to-galaxy scatter.

Numbers below are from `cfg533_results.json`.

| window | foot | N reaching | mean Δ ± SE (Z) | median Δ | median slope data / law | data ≤ −0.28 | MW Δ percentile (RM-v / RM-φ) | verdict |
|---|---|---|---|---|---|---|---|---|
| S-Rd | can | 37 / 153 | −0.003 ± 0.026 (−0.11) | −0.000 | −0.006 / −0.027 | 3/37 | 22% / 11% | MATCHES |
| S-Rd | alt | 37 | −0.009 ± 0.026 (−0.33) | −0.005 | −0.006 / −0.023 | 3/37 | 19% / 11% | MATCHES |
| S-rM | can | 79 | −0.003 ± 0.018 (−0.17) | −0.027 | +0.069 / +0.044 | 2/79 | 15% / 4% | MATCHES |
| S-rM | alt | 79 | −0.009 ± 0.018 (−0.48) | −0.034 | +0.069 / +0.052 | 2/79 | 10% / 4% | MATCHES |

**Verdict A: LAW MATCHES EXTERNAL SLOPES.** All four cells are diagnostic, and all four match.

**MW analogues** (reported; they do not set the verdict):

| definition | in the sample | reach S-Rd | reach S-rM | mean Δ (S-Rd / S-rM, canonical) | measured slope ≤ −0.28 |
|---|---|---|---|---|---|
| AN-V (V_flat 180–260 km/s) | 27 | 8 | 17 | +0.031 ± 0.023 / −0.015 ± 0.034 | 0/8 and 1/17 |
| AN-M (M_b within ×2 of the MW) | 37 | 16 | 25 | −0.011 ± 0.043 (NOT DIAGNOSTIC) / −0.021 ± 0.027 | 3/16 and 1/25 |

Per-galaxy slopes (data / law) are in the `.out` file. Examples on S-Rd: NGC 2903 −0.13 / −0.12, NGC 5907 +0.04 / −0.05, UGC 6786 −0.16 / −0.10. Alt values are within 0.01.

## The match, checked as hard as a fail

Post-run diagnostics (a)–(d) were added after the first run. They are disclosed and are not verdict inputs.

**(a) Not a trivial "flat matches flat".** Selecting galaxies on the PREDICTION, which is independent of data noise, the law-predicted decliners (b_law ≤ −0.10) also match:

| window | foot | N | Δ | ⟨b_data⟩ / ⟨b_law⟩ |
|---|---|---|---|---|
| S-Rd | can | 11 | +0.021 ± 0.052 | −0.117 / −0.138 |
| S-Rd | alt | 9 | +0.042 ± 0.057 | — |
| S-rM | can | 15 | +0.033 ± 0.035 | −0.113 / −0.146 |
| S-rM | alt | 13 | +0.016 ± 0.039 | — |

Where the law predicts a MW-like mild decline (−0.14), external HI curves show that decline, or a slightly milder one. They do not show a steeper one.

**(b) Regression of b_data on b_law.** The slope is 0.97 ± 0.07 (S-rM) and 0.69 ± 0.17 / 0.70 ± 0.18 (S-Rd). The law tracks galaxy-to-galaxy slope variation fully in the r_M scaling, and only partly in the R_d scaling.

**(c) The external scatter is large, and mostly not measurement error.**
- std(Δ) = 0.16, while the median per-galaxy slope error is 0.048 (S-Rd) and 0.078 (S-rM). The implied intrinsic scatter is 0.14–0.15.
- The MW's miss (0.164–0.216; CFG532b primary Ou+Jiao) therefore sits at the 4th–22nd percentile of the external Δ distribution. **The MW is NOT an outlier in Δ.** About 1 external galaxy in 5–25 deviates from the law's outer slope by at least as much, in the same direction.
- What is rarer is the MW's measured slope itself. Only 2.5–8% of external galaxies have b ≤ −0.28, and among V_flat analogues 0/8 (S-Rd) and 1/17 (S-rM).

**(d) Selecting on data is biased low.** Galaxies selected on b_data ≤ −0.20 show Δ −0.13 to −0.17. This is regression to the mean by construction and is not evidence; it is reported only to show that steep external decliners, like the MW, also fall below the law.

**Limits:**
- Only 37 of 153 galaxies, and 8 V_flat analogues, reach 6–11 R_d. HI curves rarely extend that far in R_d for massive spirals, which is the review's own "MeerKAT/SKA needed" point.
- R_d,MW = 2.5 kpc is McMillan17's thin disc. A longer MW R_d would move the S-Rd window inward.
- SPARC M_b for S-rM takes the bulge at Υ 0.5 (declared).
- The external law is ALG, not RM-v. CFG532 found ALG's MW shape miss to be the same size.

## B. Inside view: direction dependence

All 31 table environments in the on-disk sources were scanned.
- Two keyword candidates were inspected by eye; neither is a split rotation curve:
  - Wang+23's single anticentre V_c table;
  - SL24's reduced χ² per |z| slice.
- **No tabulated V_c split by azimuth, hemisphere or height exists on disk. Verdict B: NO DATA.**

**Authors' text-level statements** (quoted, converted to the largest Δslope they allow; not verdict inputs):

| source | statement | largest Δslope allowed |
|---|---|---|
| Zhou+23 | φ split ±30°, ≲ 1% | ≲ 0.02 |
| Jiao+23 | l split 160–180° vs 180–200°, < 2% within 22 kpc | ≲ 0.05 |
| Jiao+23 | beyond 22 kpc, "comparable to the cross-term" (up to ~8%) | ≲ 0.14 |
| Feng+26 | Cepheid wedges ≤ 3% to 17.6 kpc | ≲ 0.19 (short lever) |
| Wang+23 | no significant \|Z\| dependence of V_φ beyond 15 kpc | figures only, unsigned \|Z\| |

So the existing splits rule out a direction-dependent decline of the needed size (~0.16–0.22) only inside ~22 kpc, and only within ±20–30° of the anticentre. Beyond 22 kpc the authors' own split systematic is as large as the miss.

**What would be needed (NOT fetched; needs the owner's go):**
- Gaia DR3 RVS/LAMOST/APOGEE red-giant subsets binned by (R, φ, sign z) at 15–27 kpc; or the Wang+23 3D LIM cell maps (their Figs. 1–4, as data, not figures).
- Ideally, DR4 (2026-12-02) with wider azimuth coverage, to test north vs south and leading vs trailing azimuths of the warp and the LMC direction.

## C. Disequilibrium bracket (ORDER OF MAGNITUDE, PROVISIONAL)

Inputs: the review's on-disk numbers (Sgr bending-wave non-circular motions of 10–20 km/s at R ~ 20 kpc; LMC reflex of "tens of km/s") and V ≈ 200 km/s.

- **A bias ramping from 0 at 15 kpc to 10 or 20 km/s at 27.5 kpc** gives Δslope ≈ 0.08 or 0.17. That brackets the MW miss of 0.16–0.22.
- **A uniform offset** changes the amplitude, not the slope.
- **A mis-modelled Jeans pressure term** (σ_R = 28.4 km/s on disk, from Zhou+23; 35 km/s recalled) shifts V by only 2–3 km/s per unit error in the log-derivatives, i.e. Δslope ≈ 0.02 per unit error. So the pressure term alone would need errors of several units.
- **Plain reading:** the review's disequilibrium amplitudes are large enough, *if they grow outward*, to produce the whole MW miss. This is not a demonstration that they do.

## Overall (as frozen): MW TENSION LOCALISED TO MW

- Over SPARC, the law predicts external outer slopes in the MW's scaled window with no bias: |mean Δ| ≤ 0.009 at SE 0.018–0.026, in both scalings and both footings. It also matches where it predicts a MW-like decline.
- The MW's 15–27.5 kpc stellar-Jeans decline is therefore not reproduced by a general outer-shape failure of the law in HI galaxies. It belongs to the MW: its measurement (distance scale, Jeans terms) or its dynamical state.
- **Two honest qualifications:**
  1. "Localised" does not say which of the two, and B has no split data to test disequilibrium directly.
  2. The external galaxy-to-galaxy scatter in Δ (0.14–0.15 intrinsic) is about as large as the MW's miss. The MW sits at the 4th–22nd percentile, so it is a ~1–1.5σ draw in Δ, not an exceptional one. This also means a single galaxy's outer slope is not a sharp test of the law at the 0.15 level.
- The CFG532b MW shape result (Z −3 to −4.8 against the MW data) stands as measured. CFG533 does not remove it.

## Controls and MUTATE

- **K1:** the slope estimator returns exactly −0.5 for Kepler and 0 for flat.
- **K2:** ALG reproduces CFG516's rms to 4 decimals (0.1117 / 0.1005; 163 galaxies, 3269 points).
- **K3:** the MW combined Δ is read from JSON: −0.164 / −0.204 / −0.176 / −0.216.
- **MUTATE** (Keplerian tail beyond each window's inner edge): **DETECTED in 4/4 cells.** Mean Δ is +0.50 (S-Rd, Z +16.5) and +0.62 (S-rM, Z +19.4), and every analogue subset also MISSES.

## Disclosures

- Pre-freeze reading is listed in FROZEN_CRITERIA §Disclosures. No SPARC slope was seen before freezing.
- Post-run diagnostics (a)–(d) were added after the first run. They are not verdict inputs.
- The Part B manual-inspection string was written after the first run printed the two candidates.
- Part C uses one recalled value (σ_R = 35 km/s), which is flagged.
- κ is fitted, and the cold energy's mass is still required. This is not "theory closed".
