# Route 2 — Wide-Binary Baselines & Discrimination Gaps (framework vs MOND vs Newton)

**C. Zimmerman framework, 2026-06-14.** Scripts: `/tmp/route2_baselines.py`, `route2_reconcile.py`,
`route2_full.py`, `route2_dr4_snr.py`, `route2_contamination.py`. Builds on banked machinery
(`door6_wide_binaries_ultra.py`, `widebinary_chae2601_confront.py`, `widebinary_saadting_2603_confront.py`,
`efe_clinch_framework.py`). a0/Z never asserted derived. gamma = G_eff/G_N (the boost Chae/Banik/Saad-Ting
measure; Newton gamma=1; velocity boost = sqrt(gamma)).

## Convention fixed (matches banked scripts)
g_ext = Vc^2/R0 = (229 km/s)^2 / 8.178 kpc = **2.078e-10 m/s^2** = **2.22 a0_DE** = **1.73 a0_MOND**.
The framework's LOWER a0 makes y=g_ext/a0 LARGER (2.22 vs 1.73) — it sits **deeper** in the EFE-suppressed
regime than standard MOND. That is the entire source of the both-ways tension.

## The discriminator gamma (deep-regime, simple-mu — the brief's / Chae's footing)
| theory | a0 (m/s^2) | gamma = G_eff/G_N | velocity boost |
|---|---|---|---|
| Newton | — | 1.000 | 0% |
| **framework** | 9.36e-11 | **1.337** | +15.6% |
| standard MOND | 1.20e-10 | 1.410 | +18.7% |

Reproduces the brief's 1.32/1.40 exactly (it is `nu_simple(y)`, the radial pure-EFE boost).

**Discrimination gaps:**
- gap(framework − Newton) = **0.337**  (the "is there an a0" test)
- gap(MOND − framework)  = **0.073**  (the distinctive test)
- gap(MOND − Newton)     = 0.410
- **ratio gap_MF / gap_FN = 0.22** — the framework-MOND separation is only 22% of the framework-Newton gap.

## ESTIMATOR DEPENDENCE (the honesty caveat — do not bury)
gamma is NOT unique; it depends on (a) the interpolation function and (b) whether you take the deep-regime
cap or the per-separation realized boost. The spread is enormous:

| estimator | framework gamma | MOND gamma | gap_FN | gap_MF |
|---|---|---|---|---|
| radial pure-EFE, simple-mu (**brief/Chae**) | 1.337 | 1.410 | 0.337 | 0.073 |
| QUMOND angle-avg, simple-mu | 1.247 | 1.304 | 0.247 | 0.057 |
| radial pure-EFE, **standard-mu (framework's DSSYK-sharp)** | 1.083 | 1.124 | 0.083 | 0.041 |
| QUMOND angle-avg, standard-mu | 1.037 | 1.059 | 0.037 | 0.023 |

**The framework's OWN preferred (sharp/DSSYK) interpolation gives gamma~1.04-1.08, not 1.32.** The 1.32
figure is the SOFT (simple-mu) end. Per-separation QUMOND with the sharp interp even goes slightly
sub-Newtonian (gamma 0.95-0.99) in this EFE regime — a known feature of the radial-1D model at y~2. So the
"+15% boost" is interpolation-optimistic; the conservative framework expectation is a few percent.

## Per-separation gamma(s) — the realized boost (simple-mu, optimistic end)
| s (kAU) | g_int/a0_F | gamma_Newton | gamma_framework | gamma_MOND | D(F-N) | D(M-F) |
|---|---|---|---|---|---|---|
| 3 | 10.56 | 1.000 | 1.017 | 1.025 | 0.017 | 0.008 |
| 5 | 3.80 | 1.000 | 1.033 | 1.046 | 0.033 | 0.013 |
| 7 | 1.94 | 1.000 | 1.044 | 1.061 | 0.044 | 0.017 |
| 10 | 0.95 | 1.000 | 1.053 | 1.074 | 0.053 | 0.020 |
| 15 | 0.42 | 1.000 | 1.061 | 1.083 | 0.061 | 0.022 |
| 20 | 0.24 | 1.000 | 1.063 | 1.087 | 0.063 | 0.023 |
| 30 | 0.11 | 1.000 | 1.066 | 1.090 | 0.066 | 0.024 |

The realized per-pair gap_MF is **0.008-0.024** — far below any plausible precision. The 0.073 gap is the
DEEP-bin cap, which only the widest, deep-internal pairs (g_int << a0) approach.

## DR4 SNR forecast (deep-regime discriminator, gap/sigma_gamma)
Existing precision: Chae 2023 sigma_gamma ~ 0.06 on 26,615 pairs (El-Badry 2021 catalog, <200 pc).

| scenario | sigma_gamma | F-vs-N SNR | M-vs-F SNR | verdict |
|---|---|---|---|---|
| Chae-2023-level (26.6k) | 0.060 | 5.6 | **1.2** | super-Newt OK, MOND-degenerate |
| DR4 conservative | 0.025 | 13.5 | **2.9** | 3-way only if systematics clean |
| DR4 optimistic (full 3D RV) | 0.018 | 18.7 | **4.1** | 3-way clean (statistics) |
| DR4 systematics-floor (triples) | 0.030 | 11.2 | **2.4** | MOND-marginal |

## CONTAMINATION — the dominant systematic (why it is NOT statistics-limited)
The disagreement between Chae (gamma~1.43, +MOND) and Banik 2024 (Newtonian, claimed 19σ, **contested**) on the
SAME Gaia data implies the triple/close-binary systematic on gamma is **delta_gamma_sys ~ 0.3-0.4** — larger
than the whole framework-Newton gap and ~5x the framework-MOND gap. Banik infers a ~63% triple/multiple
fraction in the raw sample.

Residual-triple bias model (each residual triple inflates v^2 by ~0.5):
| residual triple fraction | gamma bias | as % of gap_MF=0.073 |
|---|---|---|
| 1% | 0.005 | 7% |
| 2% | 0.010 | 14% |
| 5% | 0.025 | 34% |
| 10% | 0.050 | 68% |

A **2-5% residual triple fraction biases gamma by 0.01-0.025 = comparable to the entire framework-MOND gap.**
DR4's real lever is contamination control (epoch RVs + astrometric-acceleration triple flags drive f_res down),
NOT raw N. Pushing the systematic below 0.073 needs residual triples <~8% AND eccentricity-deprojection
systematic <0.02 — hard but plausible with full 3D RV orbits (Chae 2026's 36-pair method scaled up).

## BOTH-WAYS VERDICT (the lower-a0 tension, answered honestly)
The framework's lower a0 is genuinely a double-edged sword, and the two edges land differently:

1. **framework vs Newton — the lower a0 does NOT blunt it.** Gap 0.337; framework retains ~82% of MOND's
   super-Newtonian excess. At any DR4 precision this is a clean **>10σ** test (SNR 11-19). The "is there an
   a0 at all" question is cleanly answerable.

2. **framework vs standard MOND — the lower a0 DOES blunt it into near-degeneracy.** Gap 0.073 is only 22% of
   the framework-Newton gap, and **comparable to the residual-triple + eccentricity systematic floor.** Best
   case (full-3D-RV DR4, systematics controlled to ~0.02) reaches ~4σ; the realistic, systematics-limited case
   is ~2-3σ — **below clean resolution.** So **framework-vs-MOND is MOND-degenerate at DR4** unless systematics
   beat ~0.02, which the Chae/Banik 0.3-0.4 discrepancy suggests is not yet achievable.

**The test does NOT collapse to a pure binary, but it is asymmetric:** it is a clean 2-way discriminator
(super-Newtonian YES/NO) plus a marginal, systematics-limited third axis (which a0). The honest framing:
wide binaries cleanly test the framework's PREMISE (is local MOND real) but do NOT cleanly test its
DISTINCTIVE value (a0=9.36 vs 1.2e-10). And the 1.32 number itself is interpolation-optimistic — the
framework's own sharp interp predicts ~1.04-1.08, which would push gap_FN down to ~0.08 and make even
framework-vs-Newton a ~3-4σ (not 10σ) test. Reported both ways: no manufactured 3-way win, no dismissal of
the real (clean) super-Newtonian discriminator.
