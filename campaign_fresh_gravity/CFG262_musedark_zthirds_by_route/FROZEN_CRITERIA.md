# CFG262 — FROZEN CRITERIA: MUSE-DARK implied-a₀ levels in redshift thirds, by baryon route (z ≈ 0.5, 0.9, 1.2)

**This file is committed before any CFG262 script exists and before this lane has computed any implied-a₀ level (an s\*, a median log a₀, a D = g_obs/g_bar, or a g_perp) for any MUSE-DARK third.**

> **κ = ½ FITTED. a₀(z) FLAT is the framework's distinctive law, a₀ ∝ H(z) the rival, ΛCDM has no a₀ (the "PROXY" is CFG223's effective-a₀ curve). Every quantity here is a model output of one GalPaK3D/DC14 analysis per galaxy plus an SED mass (CFG236 §7): the levels cannot tell a z-dependent a₀ from a z-dependent prior, pressure term, inclination or decomposition. No sentence in the outputs says the data favour a law, and a lean is not a detection.**

Request (the owner, relayed 2026-10-01 by the "High-z kinematic corpus analysis" session; a relay is a request, not an approval of anything that needs one): MUSE-DARK z-binned points **by route** for the one-chart figure, in the `chart_a0z_points.csv` shape (s\* on the canonical 9.3603e-11, 68/95 % interval, inner ±0.15 dex and outer ±0.30 dex baryon bands, no-root flags, extra columns). CFG198's level was withdrawn by CFG199 (an artefact of its g_obs scale); CFG199 gives only a no-pressure LOWER bound for the lowest third; CFG236 shows the route contrast is the z-trend of M_route/M_fit and that no mass is shown wrong. Nothing is fetched: the 126 `true_Vrot.dat` files and the catalogues are on disk (hash-checked by CFG236's verifier).

## 0. What I read and saw before this freeze (disclosure; the hand estimates in §8 were written after it)
1. **READ in full:** `CFG236_musedark_referee/README.md` (the referee; reproduction YES), `CFG199_musedark_level_pressure/README.md`, `CFG236_FROZEN_CRITERIA.md` (top 60 lines), the machinery of `CFG236_common.py` (`routes`, `gperp_reading`, `thirds`, `sample`, `load_dat`, `verify_hashes`) and the `[DAT]` block of `CFG236_main.py`. **Not opened:** CFG198's and CFG199's scripts, any `.out`/`.json` of theirs, the papers.
2. **Numbers from the record that bear on levels:** CFG199 route (i) lowest third, no-pressure lower bound: −10.38 [−10.71, −10.12] (reading a), −10.14 [−10.45, −9.94] (reading b); CFG236 with the asymmetric-drift term on: −10.05 (a + drift), −9.93 (b + drift), against footings −10.03 / −9.95 (log₁₀ of 9.3603e-11 / 1.1312e-10); CFG236 slopes in dex per unit z: route (i) +0.63…+0.65, route (ii) −0.20…−0.22, route (iii) +0.075 (R198), the censoring of D ≤ 1.05 rows (24 of the route-(ii) rows; 9 low-z, 15 high-z) biasing route (ii) upward, the prior-dominated gas (97 of 109 rows), CFG236's best-supported velocity reading "(c) projected + asymmetric drift" (α = 0.92, the file's σ).
3. **Baryon-side and redshift facts, printed while designing (no velocity, no g_obs, no D):** the sample S has 109 galaxies, z 0.280–1.438, equal-count thirds N = 37 / 36 / 36 with z median 0.523 / 0.878 / 1.204, log M\*_SED median 8.68 / 9.18 / 9.40; fDM(R_e) median 0.76 / 0.81 / 0.88; inclination median 56.7° / 59.3° / 60.0°; μ_mol median 1.48 / 1.62 / 1.93; σ_fit, inclination finite in all 109, log_Mdyn finite in 108. **The CFG236-style impossibility proxy** (half the route's disc mass plus π R_e² Σ_HI above the model's log_Mdyn, with log_Mdyn read as the mass within R_e, unverified): route (ii) SED + H₂ **0.32 / 0.33 / 0.58**, route (iii) SED 0.19 / 0.17 / 0.28 by third.
4. **A median-residual estimator has a root only if the median D of the row exceeds 1** (f(s → 0) = median log D; f decreases to −∞ with s), so the proxy 0.58 in the highest third of route (ii) is a **no-root risk** foreseen before the freeze.

## 1. Data and sample (the CFG236 chain, unchanged)
- `data_assembly/musedark_catalogues/musedark_numeric.csv` (126 rows) and the external run files (`<repo parent>/_external_data/muse_dark/numeric/ID####/DC14_####_true_Vrot.dat`; read-only; verified by `CFG236_common.verify_hashes()` against the repo manifest).
- **Sample S:** finite z, logMstar_phot, DC14_logMdisk, fDM_at_Re, Re_kpc, gas_density; has_bulge = 0; 0 < fDM < 1 → **109** (126 → 124 → 110 → 109).
- **Thirds:** equal-count terciles of S by z (`CFG236_common.thirds`), the same 109 galaxies for every route and reading (not the route-(i)-finite subsets CFG199 used).
- Geometry and constants exactly CFG236's (thin exponential disc at R_e, R_d = R_e/1.678, g_HI = π G Σ_HI, G = 4.30091e-6, 1 (km/s)²/kpc = 3.2408e-14 m s⁻²; μ_mol as coded; v_f(R_e) = mean over the two sides of |v| at |rad_Re| = 1 and σ_1 likewise).

## 2. The rows (fixed here; 18 rows)
For each of the 3 thirds, each of the 3 routes (the R199 construction, the model's own velocity):
- **route (i)** (fitted masses; the model's own decomposition): g_bar,i = (1 − fDM) g_perp, D_i = 1/(1 − fDM);
- **route (ii)** (SED M\* + H₂): g_bar,ii = g_bar,i ρ_ii, ρ = [g_disc(M\*(1 + μ)) + g_HI] / [g_disc(M_fit) + g_HI], D_ii = g_perp / g_bar,ii;
- **route (iii)** (SED M\*, no H₂): the same with M\*;

and each of the 2 readings of the file's velocity (g_perp = v_perp²/R_e):
- **reading b** (the file's v is the projected line-of-sight velocity: v_perp = v_f / sin i), **no pressure term: a LOWER bound** on the level (CFG199's preferred reading and the chart's existing arrow);
- **reading bD** (reading b plus the asymmetric-drift term D1: v_c² = v_perp² + 0.92 × 1.678 σ_1², σ_1 from the same file at R_e): **the pressure-corrected reading CFG236 found best supported; the headline row set.**
Reading (a) (v_perp = v_f) and its drift variant are reported as sensitivity rows, never as points.

## 3. The estimator and the statistics (the programme's, unchanged)
- **Headline: CFG223's implied-a₀ scale s\*** — the root of median_i log₁₀[D_i / ν(g_bar,i / (a₀ s))] = 0 on log₁₀ s ∈ [−3, 3] (64 bisection steps), copied verbatim in `CFG229_class_m_gold/a0implied.py` (imported, read-only), **ν_mono** (`CFG4_common.nu_mono`; numerically the exponential RAR kernel here), a₀ = 9.3603e-11 canonical; a root exists only if the median D of the row exceeds 1, otherwise the row is flagged **no root** (the chart's floor convention: s = 0.001).
- **Interval:** galaxy bootstrap, B = 10,000 resamples of the third's galaxies (seed = crc32(row label) mod 100000), 68 % = 16–84 and 95 % = 2.5–97.5 percentiles of log₁₀ s\*; the fraction of unbounded resamples is reported and a row with more than 5 % unbounded resamples is called **unbounded**.
- **Historical estimator, reported beside it for continuity (never the headline):** the median log₁₀ a₀,i over the rows with D > 1.05 (CFG199/CFG236's level), with its own 95 % bootstrap interval; the rows dropped are counted per third.
- **Absolute a₀ is footing-independent:** the alt footing returns the same a₀ (control M1).

## 4. Bands, named systematics and knobs (declared, not measured)
- **Baryon bands (the programme's standard):** g_bar × 10^(±0.15) and × 10^(±0.30) at fixed g_obs (D × 10^∓), s\* re-solved on the actual rows; a band solution without a root sets the noroot-corner flag. **Route-specific meaning:** route (i) — the model's own decomposition freedom (the baryon fraction is an output of the fit, not a measurement); routes (ii) and (iii) — the SED M\* zero point (CFG236: the SED mass is itself an SED-fit output) and the H₂ scaling relation.
- **Named systematics (reported, outside the bands):** (a) the pressure term: reading b against bD, the whole difference between the two row sets; (b) the gas prior (Σ_HI is a prior value in 97 of 109 rows): Σ_HI = 0 and 15 M⊙/pc² and the coefficient × 0.5 / × 2, routes (ii) and (iii); (c) the z-dependent SED-mass bias τ = ±0.25 dex per unit z (CFG236's declared plausibility ceiling) and an H₂ z-tilt t_H = ±0.3 dex per unit z, routes (ii) and (iii): the effect on each third's level and on the differences between thirds; (d) μ_mol with the natural-log reading (CFG236's sensitivity); (e) the kernel P2 for ν_mono.
- **Recipe half-width** = the quadrature over the knobs (b), (d), (e) and the estimator alternative (the historical estimator) of the largest |Δ log₁₀ s\*| inside each knob, in dex, excluding the baryon bands and the τ / t_H drifts (reported separately, as CFG260/CFG261).
- **Expected laws for the flags:** FLAT s = 1; H(z) and PROXY from CFG223's `curves` interpolated at the third's median z; flags are three letters per law (in the 95 % interval / in its hull with the inner band / with the outer band).

## 5. Stage A — the blind pre-flight (committed, with its outputs, before stage B is run)
**No level is computed: no g_perp, D, s\* or median a₀ of any third is printed or formed by the pre-flight.** It uses the catalogue columns, the baryon side (g_bar of routes (ii) and (iii) from the SED mass, μ_mol, R_e, Σ_HI) and a noiseless model world.

**Controls (each can fail):**
- **C1** the 882 run files and 9 catalogue files match their manifests (882 / 882 and 9 / 9); **C2** the sample chain counts 126 / 124 / 14 / 110 / 109 and the thirds N = 37 / 36 / 36; **C3** route identity: with M\*_SED := M_fit and μ := 0 routes (ii) and (iii) give ρ ≡ 1 and g_bar,ii = g_bar,iii = g_bar,i exactly; **C4** the imported `implied` equals CFG223's original `nuv`/`implied` bit-for-bit on 200 random sets (the CFG229 control, re-run here); **C5** noiseless world D_i = ν(g_bar,i / (a₀ s_true)) returns s_true to 1e-6 dex for s_true = 0.5, 1, 2.5 for each route's baryon side; **C6** counts only: the number of galaxies with a finite v_f(R_e), finite σ_1 and a finite D1 reading in each third (no value printed).
- **C7** the bootstrap machinery on a noiseless world with an injected log-normal scatter of 0.6 dex (per-galaxy, seed 262) returns an interval containing s_true in ≥ 88 % of 400 draws of N = 36 at the 95 % level and ≥ 60 % at 68 % (coverage; a record-based planning scatter: CFG199's lowest-third interval implies about 0.6 dex).

**Reported (pre-flight tables):**
- **A1 baryon lever** d log₁₀ s\*/d(baryon dex) by route and third, from the noiseless world on the baryon side (routes (ii), (iii): y_i = g_bar,i/a₀ from the SED baryons; route (i): y_i = ν⁻¹(1/(1 − fDM)) so the world sits on the law): the distribution of y, the lever with its no-root flag.
- **A2 no-root forecast:** the impossibility proxy of §0.3 per third and route (the fraction of galaxies whose route baryons exceed the model's mass within R_e), the frozen rule **NO ROOT LIKELY iff the fraction ≥ 0.50**, and the third's count of rows with proxy D < 1.
- **A3 precision forecast:** SD of log₁₀ s\* for N = 36 at a per-galaxy scatter of 0.6 dex (planning number, the record's) = 1.2533 × 0.6/√36 = 0.125 dex.
- **A4 z-dependent calibration drifts:** the effect of τ = ±0.25 dex per unit z and t_H = ±0.3 on the thirds' relative levels (lever × drift × Δz between thirds' medians, 0.355 and 0.326 in z).
- **A5 FLAT versus H(z) from the thirds' levels:** the rival's expected change in log₁₀ s\* between the thirds (CFG223's H(z) at 0.523 → 1.204, +0.18…+0.20 dex) against 2 √(2 × 0.125² + (lever τ Δz)²) = POSSIBLE_SYS iff the rival's change exceeds it.

**Decisions (the frozen map):**
- **PF-D1 ESTIMATOR VALIDATED** iff C1–C7 pass. **PF-D2 ROOT FORECAST** per route and third as A2. **PF-D3 DRAWABLE** per row iff PF-D1 passes and the forecast is not NO ROOT LIKELY; a NO ROOT LIKELY row is drawn as a floor triangle (its data may still produce a root; scored at stage B). **PF-D4 FLAT versus H(z)** from the thirds' levels: POSSIBLE_SYS or NOT POSSIBLE by A5. The measurement is run in any case, labelled.

## 6. Stage B — the measurement (run once, after stage A and the script are committed)
- Per row: s\*, a₀, the 68 / 95 % bootstrap intervals, the bands (inner, outer), the recipe knob table, the τ / t_H drift rows, the historical-estimator level with its interval, the no-root status and the median D, the number of rows with D < 1 and D ≤ 1.05, flags per law, and the **routes' contrast** (s\*(ii)/s\*(i), s\*(iii)/s\*(i) per third) with the thirds' differences per route.
- Points file `cfg262_points.csv`: first 18 columns = `chart_a0z_points.csv`'s header (M4), then `recipe_half_dex, recipe_lo, recipe_hi, n, route, reading, third, median_D, n_D_lt1, quality, flags_FLAT, flags_H(z), flags_PROXY, hist_level_log10, hist_lo95, hist_hi95`. Quality strings: "pressure-corrected, SED/fit-calibrated" (bD) or "no-pressure LOWER bound" (b), and for route (i) "model-internal decomposition".
- **No verdict words.** Descriptive only.

**Controls at stage B:**
- **M1** the alt footing gives the same absolute a₀ in every row with a root (≤ 1e-9 dex).
- **M2 MUTATE=1 (separate output files):** every galaxy's D is scaled by ν(y_i/2)/ν(y_i) with y_i = g_bar,i/a₀ (the law at s = 2 planted on its own baryons) → every row's log₁₀ s\* with a root moves by +0.301 ± 0.05 against the main run (a failure declares the estimator NON-REACTIVE).
- **M3 reproduction of the record (reported; load-bearing):** the historical estimator on route (i), lowest third of the route-(i)-finite galaxies, reproduces CFG199's −10.38 (reading a) and −10.14 (reading b) to ±0.05 dex and CFG236's −10.05 (a + drift) and −9.93 (b + drift) to ±0.05 (a loader/definition check; the numbers are the record's, not blind).
- **M4** the points file's first 18 columns equal the chart header. **M5** sum rule: for every route and reading the three thirds partition the 109 galaxies (counts add to 109).
- **SELFTEST** (before the measurement, `_SELFTEST` outputs): fabricated g_perp from the law at s_true on each route's baryons plus 0.6 dex log-normal scatter; the pipeline returns s_true inside its 95 % interval for every row.

## 7. Run order and outputs
`cfg262_musedark_zthirds.py` with `STAGE=A` then `STAGE=B` once (and `MUTATE=1`); README; failed first runs kept as `*_firstrun*`; every post-hoc change a dated addendum written before the rerun. Commit explicit paths only; push; hashes to the orchestrator for the re-run (no LEDGER.md edit for this lane).

## 8. Hand estimates (written after §0; scored by stage A / stage B and kept as they fall)
- **HE1 root forecast:** NO ROOT LIKELY only for route (ii), third 3 (proxy 0.58); every other route-third has proxy 0.17–0.33 and a root. At stage B, route (ii) third 3 has median D ≤ 1 with probability about 0.55.
- **HE2 levers:** route (i) lever in [−1.6, −0.9] (y of order 0.03–0.5); routes (ii)/(iii) in [−4, −1] and steeper where y exceeds 1 (CFG229: about −2 near y ≈ 5).
- **HE3 precision:** the bootstrap SD of log₁₀ s\* is 0.10–0.20 dex per third on routes with a root.
- **HE4 z drift on the thirds' levels:** a τ of 0.25 dex per unit z moves the third-3-minus-third-1 level difference of routes (ii)/(iii) by |lever| × 0.25 × 0.68 = 0.17 × |lever| ≈ 0.2–0.5 dex.
- **HE5 FLAT versus H(z):** NOT POSSIBLE for routes (ii) and (iii) (calibration drift ≳ 0.2 dex against the rival's +0.19); POSSIBLE_SYS for route (i) only if its lever is near −1 and the drift scenario is not applied to it.
- **HE6 levels (scored at stage B; not estimated blind except from the record):** route (i), reading b: third-1 s\* ≈ 0.77 (−10.14 against the canonical footing), rising with z; reading bD: third-1 s\* ≈ 1.2 (−9.93); route (i) third-3 level above third-1 by 0.2–0.5 dex in both readings; route (ii) levels in the range 0.3–2 with no clear rise and the third-3 row no-root or low; route (iii) between (i) and (ii).
- **HE7 route contrast:** s\*(i) exceeds s\*(ii) in every third and reading; the contrast widens with z.
- **HE8 coverage (C7) passes; M1–M5 pass; M3 passes at ±0.05 dex (the arithmetic of the record).**

## 9. What this lane cannot say
- It does not measure a₀ at z ≈ 0.5–1.2: g_obs and g_bar of route (i) and the velocities are outputs of one model fit; the SED mass is the only measured baryon quantity, and it is itself an SED-fit output.
- It cannot say which baryon mass is right (CFG236: nothing in the repo shows it) and it does not separate FLAT from H(z) or from PROXY at these calibration bands.
- A level above, below or on the canonical a₀ is not read as support or tension for any law. A no-root row is a statement about the baryon model against the dynamics (a Newtonian-floor failure), not about the law.
