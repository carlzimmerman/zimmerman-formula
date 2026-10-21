# CFG927 FROZEN CRITERIA: a SEALED high-L CMB-lensing forecast. At what multipole range and noise level would CMB lensing tell theory-v2 from its control, and the KiDS-excluded CFG596 P1 from its control?

- **Written:** 2026-10-20, committed ALONE, before any CFG927 script or number exists.
- **Block:** CFG920–929 (orchestrator reservation; CFG927 = "sealed high-L CMB-lensing discrimination forecast for theory-v2 vs its
  control" in the LEDGER 920–929 row).
- **Settings:** κ = ½ is FITTED. Footings 9.3603e-11 / 1.1312e-10 m s⁻² are never pooled; each pair is forecast on its own footing.
  "Cold energy" throughout; its mass is required; no particle species. Not "theory closed". A forecast is not a measurement: nothing here
  says the data favour the framework or its control. Framework-native models only: no ΛCDM fit result, no CAMB/CLASS nonlinear spectrum,
  no halofit / HMcode / BAHAMAS / halo model, and no "within X% of ΛCDM" yardstick enters any model, forecast or class.
- **Compute rule (a 1024³ job, NC2x, is live):** one process at a time, `OMP_NUM_THREADS=1`, `nice -n 10`, each process < 1 GB
  (measured with `/usr/bin/time -l` on the first call of each script; stop if > 1 GB). No running process is touched. Nothing is
  downloaded. NC2x's outputs are not read. The engine file names of CFG596/650/654 never appear on a command line.

## 0. Disclosure: what was seen before this file was written

- CFG917 in full: FROZEN_CRITERIA (0289e4ad4), ADDENDUM A1 (187f895aa), README, `cfg917_lib.py` (sha256 ec1e971bdb31c7b4…),
  `cfg917_cmb_lensing.py`, and the stored outputs `cfg917_T1x/T2x/NC1x[_MUTATE].out/json`. Numbers seen there: the PR4 8–400 Δχ² (NC1x
  −0.276, T1x −0.088, T2x −0.085; P1 vs P0 +1.881 with AGG +10.05, KLOW +10.40), every CFG917 robustness member, the per-band B_F/B_S0
  (0.9998 → 0.9901 for T1x over the 9 bands), the coverage of the 8–400 signal (k < 0.08: 0.696; z > 1 in support: 0.155; z ≤ 1 in support:
  0.149; k > 7.98: 0.000), the measured P_grav,F/P_grav,S0 at k = 0.1/0.3/0.5/1 h/Mpc per snapshot (T1x: 0.994/0.972/0.959/0.943 at z = 0,
  0.994/0.965/0.933/0.890 at z = 1), MUTATE M2 (±10% amplitude → symmetric Δχ² ≈ 17–18 on PR4 8–400), the support (0.0802–7.98 h/Mpc,
  127 bins), K5 x_b values.
- On-disk published numbers checked for the survey models (see §5 provenance): CFG649 FROZEN_CRITERIA/README (ACT DR6 baseline L 40–763;
  amplitude errors σ_A = 0.028 for Planck 8–400 / PR4 1.011 ± 0.028 and σ_A = 0.023 for ACT DR6 1.013 ± 0.023, both "labelled context");
  CFG363 FROZEN_CRITERIA (ACT DR6 baseline 40–763); `real_research/KEATING_EXPERIMENTAL_DOORS_2026-06.md` (Simons Observatory "CMB-lensing
  map over 40% sky"). No white-noise level, beam or CMB multipole range for ACT DR6, SO or CMB-S4 lensing was found on disk, so those are
  round illustrative values (§5). The FFP10 lensed CMB spectra file header (D_ℓ in μK², L 1–6900) and the PR4 bandpower file header.
- **No CFG927 number was computed.** A back-of-envelope estimate (not computed) was formed: the k > 7.98 h/Mpc share of the S0 C_L
  integrand should be ≲ 1% at L ≤ 3000, the S4-like ±5% injection should be far above 9, and an ACT-like 40–763 forecast for theory-v2
  should be small. These expectations change no rule below.

## 1. Pairs and inputs (read-only)

| pair | F (framework) | S0 (control) | footing | inputs |
|---|---|---|---|---|
| T1x | `_external_data/cfg650_work/T1x/` theory-v2 RES canonical | `_external_data/cfg596_work/P0/` S0 canonical | canonical | inherited |
| T2x | `_external_data/cfg650_work/T2x/` theory-v2 RES alt | P0 (same) | alt | inherited |
| NC1x | `_external_data/cfg654_work/NC1x/` theory-v2 RES canonical | `_external_data/cfg654_work/NCS0/` S0 | canonical | native |
| P1 | `_external_data/cfg596_work/P1/` CFG596 candidate B (KiDS-EXCLUDED, Δχ² +68.7) | P0 (same) | canonical | inherited |

- The run-file globs are copied verbatim from `cfg917_cmb_lensing.py` (PAIRS). Exactly one JSON per glob, else stop.
- **NC2x is not in this forecast** (live run, outputs not read). A later NC2x forecast with the same script would be a dated addendum and
  is not part of the sealed table.

## 2. Model: CFG917's own machinery, read-only

- `cfg917_lib.py` is imported unchanged (sha256 recorded at run time): `Inputs` (each run's own background, growth, linear spectrum),
  `load_run`, `PairModel` (measured P_grav nodes at a = 0.5…1; realisation-variance correction on k ≤ 1 h/Mpc exactly as CFG917, `vc`
  taken from the stored `cfg917_<PAIR>.json` model block, True for T1x/T2x/NC1x; True for P1 as in CFG917's M3), `zgrid()` (400 + 600 log
  nodes), the CFG917 rules: k < k_lo = 0.0802 both arms = own linear spectrum; k > k_top power law; z > 1 primary continuation `lin`.
- **Extended projector.** `limber_X` caps L at 2500. CFG927 uses a verbatim copy of `LB.limber_X` whose only change is the output length
  (L up to 3000). K3 checks the copy against `LB.limber_X` on L 2–2500.
- Field: the gravitating field P_grav for both arms (CFG917 verdict field).

## 3. The box support cut (declared and honoured)

- **Support top:** k_top = πN/(4L_box) = 7.98 h/Mpc (CFG649/CFG917 rule; N = 1024, L_box = 100 Mpc/h). Above it the model is a power-law
  extrapolation.
- **Per-L shares** from the primary projection with region masks:
  - s_S0(L) = X_S0^{k > k_top}(L) / X_S0(L);
  - s_Δ(L) = |ΔX^{k > k_top}(L)| / (|ΔX^{k > k_top}(L)| + |ΔX^{k ≤ k_top}(L)|), ΔX = X_F − X_S0.
- **Rule:** L is COMPUTABLE iff s_S0(L) ≤ 0.10 and s_Δ(L) ≤ 0.10. L_sup(pair) = the largest L ≤ 3000 such that every L′ in [8, L] is
  computable ("≥ 3000" if all are).
- Any forecast cell whose L_max exceeds L_sup is **NOT COMPUTABLE**. Its computable part, L_min to L_sup, is reported separately and
  labelled "computable part only". No forecast is made above L = 3000.
- **Reported, not a computability rule:** the shares of X_S0 and of ΔX from k < k_lo (both arms identical by construction: the compensated
  source rule) and from z > 1 (resting on the z > 1 continuation), at L = 400, 763, 1000, 2000, 3000.

## 4. Statistic

- **Fisher-style forecast Δχ²** (Gaussian covariance, fiducial = the control S0, no data):
  Δχ²_fc = f_sky Σ_{L = L_min}^{L_max} (2L + 1)/2 · (X_F,L − X_S0,L)² / (X_S0,L + N^X_L)²,
  with X_L = [L(L+1)]² C_L^φφ / 2π and N^X_L = [L(L+1)]² N_L^φφ / 2π. Integer L, no binning.
- **Meaning, for a future real-data scorer:** if S0 is true, the real χ²(F) − χ²(S0) has expectation +Δχ²_fc and standard deviation
  2√Δχ²_fc; if F is true, expectation −Δχ²_fc, same spread (Gaussian, linear-in-amplitude limit). Both are sealed with the table.
- **PR4 Asimov row (context):** ΔBᵀ C⁻¹ ΔB on the PR4 8–400 CMB-marginalised covariance, ΔB = (W + M)(X_F − X_S0) with CFG917's windows
  (the fiducial-correction constant cancels).

## 5. Survey noise models

**Reconstruction noise.** Flat-sky Hu & Okamoto (2002) quadratic estimators TT, TE, EE, EB, TB. Minimum-variance combination
1/N_MV = Σ_XY 1/N_XY (estimator cross-covariances ignored: a standard, slightly optimistic approximation). TE and TB use the diagonal
filter F = f/(C^XX_tot,ℓ1 C^YY_tot,ℓ2) (slightly sub-optimal). EE and TT use F = f/(2 C_tot,ℓ1 C_tot,ℓ2). EB uses
F = f/(C^EE_tot,ℓ1 C^BB_tot,ℓ2). Response f_XY uses the FFP10 lensed TT, EE, TE (`FFP10_wdipole_lensedCls.dat`, sha256 7b0bfb4502248500…)
and C^BB = 0 (no primordial B). Total power = lensed spectrum + noise; lensed BB enters total power (no delensing, no iterative
reconstruction: conservative for the S4-like model). Noise N_ℓ^TT = (Δ_T · π/10800)² exp[ℓ(ℓ+1)θ²/(8 ln 2)], Δ_P = √2 Δ_T, θ = beam FWHM.
Fields outside their CMB multipole range get zero weight. N_L is computed at 64 log-spaced L in [2, 3000] and interpolated log-log to
integer L.

**Numerics.** Polar grid in ℓ1 (L along x): midpoint rule, radial step Δℓ = 4 over [ℓ_min, max(ℓ_max^T, ℓ_max^P)], 256 angles on [0, π]
doubled by symmetry; processed in radial chunks (memory cap).

| model | Δ_T [μK-arcmin] | beam [arcmin] | CMB ℓ range T / P | f_sky | L_min | provenance |
|---|---|---|---|---|---|---|
| ACT-DR6-like | 15 | 1.4 | 600–3000 / 600–3000 | 0.25 | 40 | L_min 40 and the baseline 40–763 from on-disk files (CFG649, CFG363); Δ_T, beam, ℓ range, f_sky ILLUSTRATIVE round values |
| SO-baseline-like | 6 | 1.4 | 30–3000 / 30–5000 | 0.40 | 30 | f_sky 0.40 from the on-disk quote (SO "lensing map over 40% sky"); the rest ILLUSTRATIVE |
| S4-like | 1 | 1.4 | 30–3000 / 30–5000 | 0.40 | 30 | all ILLUSTRATIVE round values |
| CV-limited (context, "ceiling") | 0 (N_L = 0) | — | — | 0.40 | 30 | ILLUSTRATIVE; no class weight |
| Planck-like (anchor only) | 30 | 5 | 100–2048 / 100–2048 | 0.65 | 8 | ILLUSTRATIVE; used only for K7 |

**Noise scan (context, sealed with the table):** f_sky 0.40, beam 1.4′, ℓ ranges as SO/S4, Δ_T ∈ {20, 10, 6, 3, 2, 1, 0.5} μK-arcmin
plus N_L = 0, range L 30–min(3000, L_sup). Per pair: Δχ²_fc at each Δ_T and Δ_T,9 = the Δ_T where Δχ²_fc = 9 (log-log interpolation
between scan points; "> 20" if Δχ²_fc(20) ≥ 9; "< 0.5" if Δχ²_fc(0.5) < 9 but N_L = 0 gives ≥ 9; "unreachable at f_sky 0.4" if N_L = 0
gives < 9).

## 6. Forecast cells and classes

- **Graded models:** ACT-DR6-like, SO-baseline-like, S4-like. **Ranges:** L_min (40 ACT-like; 30 SO/S4) to L_max ∈ {400, 763, 1000,
  2000, 3000}. Also stored: the cumulative Δχ²_fc(L_max) for every integer L_max, and L_9 = the smallest L_max with Δχ²_fc ≥ 9 ("none ≤ 3000"
  otherwise, or "≥ L_sup" if it would lie beyond L_sup).
- **Classes per cell:** DISCRIMINATING Δχ²_fc ≥ 9; MARGINAL 4 ≤ Δχ²_fc < 9; BLIND Δχ²_fc < 4; NOT COMPUTABLE if L_max > L_sup (§3).
- **Robustness members** (CFG917's definitions, each changes one thing): ZHOLD, ZREL (the two alternative z > 1 continuations), KCUT
  (measured spectra only to 4.02 h/Mpc), KLOW (F carries the low-bin F/S0 ratio below k_lo), BG (the other input set's distances). Each
  cell reports every member's Δχ²_fc. A cell is **ROBUST** if every member gives the primary's class, otherwise **RULE-DEPENDENT** with the
  member range printed. The class is the primary's.
- **Per-pair reading:** for each graded model, the shortest listed L range at which the primary is DISCRIMINATING (and whether that cell
  is ROBUST), or "not within L ≤ min(3000, L_sup)".
- If any gating K test fails for a pair, or its MUTATE does not bite, every cell of that pair reads **NOT DIAGNOSTIC (forecast)**.

## 7. K tests (gating unless marked)

- **K1** F ≡ S0 (the S0 JSON as both arms): Δχ²_fc = 0 (≤ 1e-12) in every cell and member, the PR4 Asimov row, and PR4 Δχ².
- **K2** CFG917's PR4-range result reproduced through this path: for T1x, T2x, NC1x the primary Δχ² and the six members (AGG, ZHOLD,
  ZREL, KCUT, KLOW, BG) equal the stored `cfg917_<PAIR>.json` values, and for P1 the stored `cfg917_T1x_MUTATE.json` M3_context values,
  each to ≤ 1e-6 absolute.
- **K3** the extended projector equals `LB.limber_X` on L 2–2500 (≤ 1e-12 relative, both arms, primary).
- **K4** noise numerical convergence: halving Δℓ and doubling the angle count changes N_L^MV by ≤ 1% at every L node, for ACT-like,
  SO-like, S4-like, the Planck-like anchor and the scan's 0.5 μK-arcmin member.
- **K5** noise-code analytic identity: flat C^TT = const on ℓ ∈ [30, 3000], no noise, TT only: N_L = 8π² / (L⁴ · Area), Area =
  lens(R = 3000, L) − 2π·30², lens = 2R² arccos(L/2R) − (L/2)√(4R² − L²); at L = 100, 1000, 2000 to ≤ 0.5%.
- **K6** z-grid doubling (`LB.zgrid(800, 1200)`) changes every primary Δχ²_fc cell by ≤ max(0.01, 1%) and leaves L_sup unchanged.
- **K7 (reported, non-gating) noise anchors:** Fisher σ(A) = [f_sky Σ (2L+1)/2 · X²/(X + N^X)²]^(−1/2) on the FFP10 PP spectrum: Planck-like
  over 8–400 vs the on-disk 0.028; ACT-like over 40–763 vs the on-disk 0.023. A ratio outside [0.5, 2] flags that model as UNANCHORED in the
  README; no class changes.

## 8. MUTATE (`CFG927_MUTATE=1`, run FIRST per pair, separate outputs `cfg927_<PAIR>_MUTATE.out/json`)

- **M1** F ≡ S0 → Δχ²_fc = 0 (≤ 1e-12), every model and range.
- **M2** P̂_F = (1 ± 0.05) P̂_S0 at all k, z, injected on the P grid through the extended projector:
  (a) the pipeline Δχ²_fc equals the analytic 0.05² · f_sky Σ (2L+1)/2 · X_S0²/(X_S0 + N^X)² to ≤ 1e-8 relative for every graded model over
  its widest range; and (b) the S4-like forecast over L 30–min(3000, L_sup) is DISCRIMINATING (≥ 9) for both signs.
- **M3 (context, no bite requirement):** box-only ±5% (applied only where k_lo ≤ k ≤ k_top and z ≤ 1), all graded models and ranges.
- MUTATE bites iff M1 is exact and both M2 conditions hold.

## 9. Disclosed shared inputs (they do not cancel; both arms carry them)

- The noise model uses the FFP10 (ΛCDM) lensed CMB spectra and illustrative survey parameters: the same N_L for both arms.
- Inherited runs: EH σ8 = 0.811 linear spectrum, matter + Λ background without radiation. Native runs: CFG654 §6 inputs.
- Limber at L ≥ 8; Gaussian covariance (no non-Gaussian, N1, mean-field, foreground or super-sample terms); flat-sky quadratic estimator.
- The z > 1 continuation and the k < k_lo identity are CFG917's declared rules; ZHOLD/ZREL/KLOW bracket them; their shares are reported.

## 10. Outputs and the seal

- `cfg927_noise.py` → `cfg927_noise.out/json` (N_L curves, K4, K5, K7); `cfg927_forecast.py --pair <PAIR>` →
  `cfg927_<PAIR>[_MUTATE].out/json`; `cfg927_table.py` → `cfg927_forecast_table.json/md` and `FORECAST_HASH.txt` (sha256 of the table
  files, every pair output, the noise output, the scripts and `cfg917_lib.py`). The table is committed with the hash file and never
  edited; a future real-data test scores against it. Any post-hoc change is a dated, labelled amendment; this file is never edited.

Commit rule: explicit paths only; no push. κ = ½ FITTED; footings never pooled; cold energy mass required; not theory closed.
