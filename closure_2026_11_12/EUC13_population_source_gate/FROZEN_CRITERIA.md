# EUC13 (POPULATION SOURCE GATE): FROZEN CRITERIA

2026-11-12. Written and committed alone, before any EUC13 script exists, before the field-galaxy catalogue is fetched
and before any EUC13 number is computed. TEST lane. κ = ½ FITTED; not theory closed. Adopts nothing.

## 0. What this lane is, and what it is not

ECLIPSE (Euclid DR1-Foundation strong lenses) has no lensed-source redshifts. EUC1-F (b_med on sample P at the true,
row-level source redshifts) stays open and is **not** redesigned, graded or renamed here. This lane builds the missing
input as a **distribution** (the source-redshift distribution of Euclid's lensed sources) from published data,
standard lensing physics and the framework's own law, and grades a separate **population gate, EUC13-P**.

A population gate is weaker evidence than row-level redshifts: it grades a modelled population, not measured
sources. Whatever it reads, EUC1-F remains the gate that matters. No outcome is a pass of the theory; a favourable
reading awaits an independent re-grade.

## 1. Sample, statistic, machinery

- Sample P exactly as EUC1 (`euc1.select(rows, ("A",))`, N = 3,192), catalogue hashes checked by `euc1.load`.
- b = log10 of the Salpeter-mass boost law S needs to make the observed effective Einstein radius at source
  redshift z_s: `euc1.build` + `euc1.run_b` / `Engine.solve_b` with `euc1.EUCLID` geometry, imported, not rewritten.
- Footings canonical a0 = 9.3603e-11, alt 1.132e-10 m/s^2; never pooled.
- Statistics on P: b_med (median b) and f25 (fraction with b > 0.25, EUC1's line).
- Support: every drawn source satisfies z_s >= z_l + 0.2 (EUC1/EUC10 guard); z_s <= 6.0.
- Speed device (instrument, checked by KA5): for each lens, b is tabulated against x = log10(Σ_cr(z_l, z_s) /
  Σ_cr(z_l, 1100)) on 33 points x = 0, 0.05, ..., 1.60 (direct solve beyond 1.60), and interpolated linearly.

## 2. Members

### M1, M2 (empirical): published source redshifts drawn onto P

M1 = AGEL DR2 (N 90), M2 = DESI Strong Lens Foundry IV, MUSE (N 49): rows of
`closure_2026_11_12/EUC10_published_source_redshifts/euc10_partB_samples.csv`, unchanged. Recipe per draw exactly as
EUC10 Part B: for each P lens, 10 nearest systems in z_l (z_l only; θ_E is not tabulated), draw one at random, keep its
z_s if z_s > z_l + 0.2, else redraw (<= 20 tries, else dropped from that realisation).

Selection, stated: both are ground-based (DES/DECaLS/Legacy Surveys) searches for bright, wide arcs; both need a
spectroscopic success (AGEL: Keck/VLT optical-NIR, flag >= 2; SLF IV: MUSE 475-935 nm, Q_z <= 2), which favours
emission-line sources and under-samples 1.5 < z < 2.5 and faint high-z sources; their lenses are brighter and wider
than Euclid's. Both are expected to put sources lower in redshift than Euclid's fainter arcs.

### M3 (forward model, framework-native lensing weight)

For each P lens i, a predictive distribution p_i(z_s) on z = 0.025, 0.075, ..., 5.975 (bins of 0.05), restricted to
z_s >= z_l + 0.2:

1. **Arc brightness.** Lens VIS flux F_L = `flux_detection_total` (μJy) of the lens's own MER object
   (`MER_object_id` of `ECLIPSE_object_catalogue.csv`, found in EUC3's cached MER tables
   `_external_data/euclid_dr1_eclipse/nisp_tables/mer_*.csv`). Arc VIS magnitude m_arc = 23.9 − 2.5 log10(r F_L),
   r = `eclipse_vis_ratio_ls_l` (> 0). Lenses without both (171 of 3,192 by an input-availability count made before
   freezing) take m_arc drawn per realisation from the 20 P lenses nearest in (z_l / 0.1, log10 θ_E / 0.1) that have one.
2. **Field population.** COSMOS2020 Classic (Weaver et al. 2022, VizieR J/ApJS/258/11/classic), galaxies with
   FlagCOMBINED = 0 and a valid `lpzBEST`, aggregated into counts N(m, z): HSC i AUTO magnitude in 0.1-mag bins from
   16.0 to 28.0, lpzBEST in the 0.05 bins above. HSC i stands in for VIS (VIS spans about 530-920 nm, i is centred
   near 770 nm; expected colour difference about 0.1-0.3 mag, small next to the magnification bracket). The CfA
   TAPVizieR endpoint did not answer before freezing (HTTP 000) while the CfA VizieR ASU service did; the aggregate
   is therefore built locally from a column-restricted ASU download (columns HSCimagAuto, lpzBEST, FlagCOMBINED;
   HSCimagAuto < 28), recorded in the MANIFEST. If the ASU download fails too, M3 is NOT BUILT and the gate runs on
   M1 and M2, flagged.
3. **Magnification bracket (three settings).** μ = 3 and μ = 10 fixed (intrinsic m = m_arc + 2.5 log10 μ;
   n(z | m) = N(m ± 0.25, z), normalised); and **μ marginal** (magnification bias on):
   n(z) ∝ ∫ p(μ) N(m_arc + 2.5 log10 μ ± 0.25, z) dμ with p(μ) ∝ μ^-3 on 2 <= μ <= 30 (the total-magnification
   distribution of a doubly/quadruply imaged source behind an isothermal lens), counts not normalised per magnitude,
   so fainter, more numerous sources carry their weight. Intrinsic magnitudes fainter than 27.5 are evaluated at 27.5
   (fraction of weight so clamped reported).
4. **Lensing weight (two forms).** w_i(z_s) = θ_E,i(z_s; B_i)^2, the lens's strong-lensing cross-section:
   - **full**: the law's own lens. θ_E(z_s; B) solves M_2D(<R) = π R^2 Σ_cr(z_l, z_s) with M_2D from
     `Engine.M2D(B, a0, "S")` on a radius grid R = f R_E, f = 0.2-5 (31 log-spaced points), log-interpolated;
     θ_E capped at the grid ends. B_i is solved **self-consistently**: B_i = 10^(median of b_i(z_s) under p_i),
     starting from b_i at z_s = 1100, three iterations, per footing; the largest change in the last iteration is
     reported.
   - **sis**: the law's saturated (constant-deflection) limit, w(z_s) = (D_ls / D_s)^2, B-free.
   p_i(z_s) ∝ n(z_s | arc) × w_i(z_s).
5. **Bounding the approximation (readings only, not in the envelope).** The cross-section weight uses a lens mass
   inferred from the same data (it does not condition on the observed θ_E with a free mass). Readings with B_i fixed
   at b = 0 and b = 0.5 (full form, μ marginal) show how much this choice moves b_med.

M3 has six settings: {μ 3, μ 10, μ marginal} × {full, sis}.

### Validation of M3 (a gate on the member, not on the theory), sis weight (validation lenses have no stellar masses)

- **V1, DESI SLF IV.** Systems of M2's 49 whose primary source row in `x/2509.18078/main.tex` (cached under
  `_external_data/euc10_published_source_z/lit/`) gives a magnitude: VIS proxy = DESI i if given, else −2.5 log10 of
  the mean flux of the given r and z; lens redshift from the same table. For each μ setting, the mixture
  (1/N) Σ p_k is compared with the observed z_s: **passes** if |median(mixture) − median(observed)| <= 0.25 **and**
  the one-sample Kolmogorov-Smirnov p (observed z_s against the mixture CDF) > 0.01.
- **V2, ECLIPSE lenses with a known source redshift.** The 14 lenses of `euc10_matches.csv` with status USED plus
  EUC2's confirmed pairs not already among them (L012826 1.1374, L014688 0.9926, L006816 0.4685), each evaluated if
  it has an arc magnitude (step 1) and a key-catalogue photo-z (lens z = DESI deflector spec-z if present, else
  photo-z). PIT u_k = CDF_k(z_s,true). **Passes** if the KS p of {u_k} against uniform > 0.01 **and** at most one lens
  has min(u_k, 1 − u_k) < 0.005. Fewer than 5 evaluable lenses: V2 not applied (stated).
- A μ setting survives if it passes V1 and V2; its full and sis forms both survive or both drop. If no μ setting
  survives, **M3 is dropped** and the gate is graded on M1 and M2, flagged. Validation is computed and printed before
  any P number of M3, and the script grades whatever survives without intervention.
- Limits stated now: V1's sources are bright and spectroscopically confirmed; V2's lenses are mostly the wide,
  group-type systems where published follow-up concentrates.

## 3. Intervals (honest, per member and setting)

400 replicates (seed 20261112). Each replicate: (a) P resampled with replacement; (b) one realisation of the catalogued
errors of P exactly as EUC1's robustness run 6 (photo-z 70 % interval / 1.04, mass errors, θ_E and θ_e half-widths;
40 error realisations precomputed with their own b tables, replicate r uses realisation r mod 40); (c) one source draw
per lens; (d) for M1/M2, the published sample resampled with replacement before matching. In M3 the predictive is built
at catalogued values; under an error realisation the drawn z_s is truncated to z_s >= z_l' + 0.2 by redraw.

Point estimate: catalogued values, no resampling, median over 200 draws (for M1/M2 this is EUC10's Part B recipe).
Interval: point + (q2.5 − q50, q97.5 − q50) of the replicate distribution (recentred, because perturbing measured values
adds their noise a second time; EUC1 A2). Raw replicate percentiles are reported beside it.

M3's interval is the **envelope** over its surviving settings: lowest lower bound to highest upper bound.

## 4. The gate EUC13-P (per footing, never pooled)

- **POPULATION GATE HOLDS** if every surviving member's 95 % upper bound on b_med(P) <= 0.15;
- **POPULATION GATE FAILS** if every surviving member's 95 % lower bound >= 0.25;
- otherwise **NO VERDICT**.
- Second statistic, f25, the same way on EUC1's lines: CEILING BROKEN if every surviving member's lower bound >= 0.25,
  CEILING HOLDS if every upper bound <= 0.10, else NO VERDICT. Reported beside the gate word, not the gate word.
- Any failed instrument check or known answer: NOT EVALUABLE.

## 5. Readings (not gates)

- θ_E classes (effective Einstein radius): < 1.0″, 1.0-1.3″, >= 1.3″, per member, b_med with the same interval, placed
  against EUC5's sealed bands (canonical / alt: −0.19 to +0.22 / −0.19 to +0.21; −0.05 to +0.30 / −0.06 to +0.34;
  +0.03 to +0.32 / +0.03 to +0.31) as "inside / above / below". This is **not EUC5-F** (which is on sample S at row-level
  redshifts) and the bands are not moved.
- Each member's median z_s on P; M3's B-fixed readings (§2 M3.5); M3 per setting.

## 6. Known answers and checks (all must pass, else NOT EVALUABLE)

- KA1 SLACS at true z_s through EUC1's K5 path: +0.082 / +0.070 (± 0.003).
- KA2 EUC1 source-free b_med on P: −0.019 / −0.044 (± 0.001), N = 3,192.
- KA3 EUC10 Part B reproduced with its own recipe, before anything changes: AGEL +0.238 / +0.220, SLF IV +0.298 / +0.282
  (± 0.002).
- KA4 the same two numbers through EUC13's tabulated-b path: within 0.005 of KA3's values.
- KA5 tabulated b against direct solves on 300 random (lens, z_s) pairs per footing: max |Δb| <= 0.003.
- KA6 COSMOS2020 aggregate sanity: median lpzBEST of galaxies with 23.5 < i < 24.5 between 0.6 and 1.6 (a wide window
  on the published depth-dependent n(z); checks the column and units, not the model).
- **Mutation twin** (`EUC13_MUTATE=newton`, a0 → 1e-30): b_med must rise for every member on both footings; exit 1.

## 7. Order and amendments

FROZEN_CRITERIA (this file, alone) → fetch script and fetch (MANIFEST) → `euc13.py` and outputs → RESULT.md (verdict
first, <= 100 lines). Any change after a number is seen goes in `AMENDMENT_A1.md`, committed alone, disclosed as post hoc,
the frozen word standing beside it. No scanning of μ, weights or tolerances.

## 8. Disclosure: seen before freezing

- The lead's brief, with: EUC1 conditional readings +0.146 / +0.125 (z_s = 3), +0.232 / +0.213 (z_s ≈ 2), break
  redshifts 4.34 / 3.58; EUC10 Part B +0.238 / +0.220 (AGEL), +0.298 / +0.282 (SLF IV); SLACS +0.082 / +0.070; EUC1
  source-free −0.019 / −0.044; and the lead's UNVERIFIED hand estimate: M3's typical source near z 1.5-2 reading
  +0.25 to +0.30, AGEL just under 0.25 on canonical, likeliest word NO VERDICT both footings, f25 well above 0.25 in
  every member.
- EUC1 RESULT.md in full (incl. f25 by z_s: canonical 0.47 / 0.37 / 0.32 / 0.28 at z_s 2 / 2.5 / 3 / 4), EUC10
  RESULT.md and RERUN_AND_IDS.md (matched lenses and their b), EUC2's pair table, EUC5's bands.
- The first six systems of SLF IV's source table (redshifts and DESI magnitudes, e.g. sources at r ≈ 20-24) and
  EUC10's statement that its sample medians are z_s 1.95 (AGEL) and 1.43 (SLF IV).
- ECLIPSE column lists; input coverage only: 3,192 P lenses, all with a positive VIS flux ratio, 3,021 with their MER
  object in EUC3's cached tables. No ratio, flux, magnitude or b value of any P lens was looked at.
- COSMOS2020 VizieR metadata (column names only). No COSMOS row was downloaded.

Adopts nothing. κ = ½ FITTED; not theory closed.
