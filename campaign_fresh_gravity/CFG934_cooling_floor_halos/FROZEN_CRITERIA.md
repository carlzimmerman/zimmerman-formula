# CFG934 FROZEN CRITERIA: cooling-floor primordial halos (H-CF), a parameter-free supply for faint dwarfs

- **Date:** 2026-10-20. Block 930–939 (reserved in the LEDGER row "CFG930–939", 10-20 ~18:30 entry). Agent lane.
- **Kind:** HYPOTHESIS TEST. One new supply RULE, zero new fitted constants. Declared inputs are bracketed, never fitted.
- **Settings:** κ = ½ is FITTED. Footings 9.3603e-11 and 1.1312e-10 m/s² are scored separately and never pooled. The extra
  mass is cold energy, not a particle species. Verdicts use raw data and framework-native inputs only. No Moster, Behroozi,
  ΛCDM mass function, abundance matching or Dutton–Macciò c(M) enters any verdict; CFG42's Moster + Dutton–Macciò inputs appear
  ONLY in the K1 reproduction test. Not "theory closed". Nothing here can say the data favour the framework.
- These criteria are committed ALONE, before any CFG934 script exists and before any CFG934 number is computed. Any later
  change is a dated, labelled amendment in a separate file.

## 0. Disclosure (not blind)

H-CF was formed AFTER the following were seen: CFG42 (collapse debris closes the MW ultra-faints, crossing zero near a
collapse mass of ~3e8, over-predicts the classical satellites by ~0.11 dex), CFG45 (sum 6/7, max 4/7), CFG65 (cusp vs core),
CFG827/CFG828 (uniform dwarf excess), CFG870–CFG872, CFG877 (finite clump σ ≈ 7.5 km/s), CFG878 (neutral-gas cooling-floor
σ 7.36–8.22 km/s, post hoc), CFG880 (clump σ not universal, s_int 0.38), CFG919/CFG921/CFG928 (selectors), CFG930 (native
collapse debris with catchment supply leaves f_ex = 0 everywhere; native cusp below the phantom at every dwarf aperture),
CFG931 (Lelli+15 tidal dwarfs 0.69 dex below the bare law, INFO), CFG932 (the dwarf excess needs ~100× the catchment
supply) and CFG933 (Coma UDGs +0.33 dex, DF2/DF4 below the law). The profile convention below (ρ_s = C ρ̄_m(z_coll),
C ∈ {1500, 3000, 6000}) is adopted from CFG930 for consistency with the record.

Before freezing, the agent did back-of-envelope arithmetic only (no lane code, no sample prediction):
- **E1.** At T_vir = 1e4 K the virial velocity is fixed, V_vir ≈ 11.6 km/s (μ 1.22) or ≈ 16.7 km/s (μ 0.59), whatever the
  epoch; textbook M_cool at z ≈ 9 is ~3e7 (μ 1.22) to ~1e8 M☉ (μ 0.59), and M_cool ∝ (1+z)^(−3/2).
- **E2 (expectation).** Under the sum reading, f_ex is likely 0 for systems whose law phantom inside the edge exceeds M_cool
  (expected for M_b ≳ 1e6 M☉), so H-CF should act mainly on the ultra-faints and leave the brighter dwarfs at the bare law;
  the LVD-83 class excess is therefore expected NOT to close under (S).
- **E3 (expectation).** The Weisz+14 grid caps τ at 12.59 Gyr (z ≈ 5), so the ultra-faints' floor halos are less dense than
  at z ≈ 9; whether they close is uncertain.
Sample membership (names, hosts, M_V) of CFG42, CFG874 and CFG880 was inspected to write §2.4; no prediction was computed.

## 1. Hypothesis H-CF and posits

**H-CF.** Before any bound system exists, cold energy is ordinary cold collisionless matter (CFG649/CFG654) and collapses
into primordial halos. A system can form stars only if its primordial halo reached the atomic-hydrogen cooling threshold,
T_vir ≈ 1e4 K, at its formation epoch z_f. So every star-forming dwarf sits in a primordial halo of mass at least
M_cool(z_f). H-CF takes the debris supply to BE that floor halo (the minimal, parameter-free assignment; any larger mass would
need an assembly history, i.e. a parameter). It replaces CFG42's Moster masses and the catchment supply for faint dwarfs.

| posit | status | value / source |
|---|---|---|
| **cooling-floor supply rule: collapse mass = M_cool(z_f)** | **NEW (the only new rule)** | this lane |
| T_vir = 1.0e4 K, T_vir = μ m_p V_c²/(2 k_B), V_c² = G M_vir/r_vir | declared (atomic physics; BL01 eq. 26 convention) | fixed |
| μ | declared BRACKET | 0.59 (ionised) / 1.22 (neutral) |
| z_f | inherited data, declared BRACKET | Weisz+14 τ50 / τ90 (§2.4) |
| Δ_vir(z_f) | framework-native | CFG654 N0 turnaround table (§2.2) |
| ρ_s = C ρ̄_m(z_coll), z_coll = z_f | declared generic collapse physics (as CFG930), BRACKET | C ∈ {1500, 3000, 6000} |
| background h, Ω_m, Ω_r, f_b | framework-native (CFG654 A1 CMB set) | cfg654_delta_ta_results_cmb.json "native" |
| readings (S) sum / (M) max, f_ex, CFG35 edge | inherited (CFG35/CFG42/CFG45) | unchanged |
| galaxy law, κ = ½ | inherited, κ FITTED | ν_e (exponential) of every reused estimator |

## 2. Inputs and construction

### 2.1 Background (framework-native)
- h, Ω_m, Ω_r, f_b from `CFG654_independent_inputs/cfg654_delta_ta_results_cmb.json` key "native"; flat, Ω_Λ = 1 − Ω_m − Ω_r.
  The CFG630 trickle (≤ 3.4e-6 of Ω_Λ) is neglected.
- H(z) = 100 h √(Ω_m(1+z)³ + Ω_r(1+z)⁴ + Ω_Λ) km/s/Mpc; cosmic time t(z) = ∫_z^∞ dz'/[(1+z')H(z')] by quadrature; age t0.
- ρ̄_m(z) = Ω_m ρ_c0 (1+z)³, ρ_c0 = 3H0²/(8πG).
- Lookback τ → z_f by inverting t(z_f) = t0 − τ.

### 2.2 Virial overdensity (framework-native)
- Δ_ta(z) = the N0 table of `cfg654_delta_ta_cmb.json` (shell turning around at z; mean density inside / ρ̄_m), interpolated
  linearly in ln(1+z) (nodes reproduced exactly).
- Collapse at z_c with turnaround at z_ta where t(z_ta) = t(z_c)/2 and r_vir = r_ta/2:
  **Δ_vir(z_c) = 8 Δ_ta(z_ta) [(1+z_ta)/(1+z_c)]³** (relative to ρ̄_m(z_c)).
- Variant V1: Δ_vir = 18π² at every z.

### 2.3 Floor mass and debris profile
- **M_cool(z) = (2 k_B T / (μ m_p G))^(3/2) · (4π/3 · Δ_vir(z) ρ̄_m(z))^(−1/2)** (total: cold + baryons), constants CODATA
  (k_B 1.380649e-23, m_p 1.67262192e-27, G 6.67430e-11, M☉ 1.98892e30 for this formula only).
- r_vir = (3 M_cool / (4π Δ_vir ρ̄_m(z_f)))^(1/3).
- **NFW** with characteristic density ρ_s = C ρ̄_m(z_coll), z_coll = z_f: the concentration c solves
  (Δ_vir/3) c³/m(c) = C (1+z_coll)³/(1+z_f)³ (= C at z_coll = z_f), m(t) = ln(1+t) − t/(1+t).
  M_NFW(<r) = M_cool m(c r/r_vir)/m(c) for r ≤ r_vir and M_cool beyond (truncated at r_vir).
- The cold part is (1 − f_b) M_NFW, f_b native (CFG42's FB only in K1).
- Variant V2: z_coll = the 13.3-Gyr-lookback onset (CFG827/CFG923's first-bin age) for every system, M_cool still at z_f.

### 2.4 Formation epoch z_f (data)
- τ50, τ90 = lookback times at which the Weisz+14 cumulative SFH (VizieR J/ApJ/789/147: table6 combined fields where given,
  else table5) reaches 50% / 90%, linear in log t between grid points, capped at the 12.59-Gyr grid edge: CFG824's rule,
  re-implemented and checked equal to CFG824's committed tau50/tau90 in K3.
- Names: CFG824's NAMEMAP plus "Sex A" → "Sextans A", "Sex B" → "Sextans B"; Collins+13 "And X" → "Andromeda X".
- **Missing SFH (declared default):** the median τ (τ50 and τ90 separately) of the Weisz+14 objects that have an LVD row, in
  the same group: {satellite = LVD host mw, lmc or m_031; field = any other host} × {faint M_V > −7.7; bright M_V ≤ −7.7}. A
  group with fewer than 3 Weisz objects falls back to the luminosity-class median over all hosts. FG001 samples: ufd, UL, cls,
  col, m31 are satellites. Variant V6: the luminosity-class median for every missing object.
- **SPARC dwarfs:** z_f = 0 at every corner (they form stars today; z_f = 0 gives the largest floor mass, the conservative
  side for "untouched").

### 2.5 Readings (CFG45's definitions, unchanged)
- **f_ex = max(0, 1 − M_ph,edge(M_b) / ((1 − f_b) M_cool))**, M_ph,edge = the law's phantom inside CFG35's edge
  r_e = 0.40 r_ta (CFG35/CFG36 `edge_phantom`, exec'd read-only through CFG42: ν_mono, CFG7's turnaround convention and its
  inherited flat-Λ background, unchanged and disclosed).
- **(S) sum, PRIMARY:** g = g_law + G f_ex (1 − f_b) M_NFW(<r)/r².
- **(M) max, ALTERNATIVE:** g = g_N + max((ν − 1) g_N, (1 − f_b) G M_NFW(<r)/r²), i.e. dark mass inside r = max(phantom,
  cold floor halo), no f_ex.
- M_b for f_ex: the estimator's stars (Υ_V L_V) + gas as the source lane counts it (CFG42: 1.33 M_HI, plus CFG18 infall gas
  for cls/col/m31); CFG874 isolated and LVD-83: Υ_V L_V + 1.33 M_HI (all HI); SPARC: 0.61 L_3.6 + 1.33 M_HI (CFG42 H4).

## 3. Classes, estimators and statistics (each class keeps its source lane's statistic and error)

Main runs use the exact footings. K tests use each source lane's own constants (CFG42: hunt_lib's 9.36e-11 / 1.13e-10).

| class | sample and statistic | error |
|---|---|---|
| **U** MW ultra-faints | FG001/CFG42: 31 resolved + 9 upper limits; Kaplan–Meier median of log10(σ_obs/σ_pred), σ² = g r/3 at r = (4/3) r_h with half the baryons | bootstrap (1000, seed 42) ⊕ Υ_V 1–4 floor (CFG42); NO collapse-mass floor (H-CF has no free collapse mass) |
| **C** MW classical dSphs | FG001/CFG42: 14 (incl. LMC/SMC as in FG001), CFG18 infall gas; median offset | 1.2533 rms/√n ⊕ Υ_V 1–4 floor (CFG42) |
| **M** M31 dSphs | Collins+13 (14) and M31 LVD (34) as CFG42 (infall gas); each graded; **class = the more severe** | as C |
| **I** isolated LG dwarfs | CFG874's 11 (grp I, ≥ 300 kpc from MW and M31), Υ_V 2, HI inside r12 by CFG874's disc rule; mean of D = log10(3σ²/r12 / g_pred) | CFG874's bootstrap of the mean (4000, seed 874, its interleaved draw), replayed exactly |
| **S** SPARC gas-rich dwarfs | CFG42 H4: 110 with log M* < 10 (M* = 0.61 L_3.6), point mass, d log v at R_HI = 0.5 log10(g_pred/g_law) | rule: fraction with d log v < 0.03 dex |
| **L** LVD-83 | CFG880's 83 (= CFG919/CFG921 dwarfs), CFG880's estimator (Υ_V 2, CFG874 gas inside r12, ν_e); E_i = ln(σ_obs/σ_pred); class statistic = unweighted mean E | se = max(std(E)/√N, √(Σε_i²)/N), ε_i = (em+ep)/(2σ_obs) (CFG919's cell rule) |

For I and L under (S): g_pred = g_law + G f_ex (1 − f_b) M_NFW(<r12)/r12²; under (M) as §2.5 with the estimator's g_N.

**Class rule:** z = statistic/error. |z| < 2 CONSISTENT; 2 ≤ |z| < 3 TENSION; |z| ≥ 3 CONTRADICTED (sign reported:
negative = over-predicted). **S:** fraction ≥ 0.90 CONSISTENT; 0.75–0.90 TENSION; < 0.75 CONTRADICTED.

## 4. Verdict

- **Corners (per footing, per reading):** μ {0.59, 1.22} × τ {τ50, τ90} × C {1500, 3000, 6000} = 12.
- **H-CF SURVIVES:** every class (U, C, M, I, S, L) CONSISTENT at every corner on both footings, reading (S), zero fitted
  constants.
- **H-CF FAILS:** at least one class CONTRADICTED at all 12 corners on at least one footing, reading (S).
- **H-CF PARTIAL:** otherwise. Labelled "corner-selectable" if at least one corner has all six classes CONSISTENT on both
  footings (choosing that corner is a discrete fit, not a survival).
- **(M)** gets the same rule and is reported as the alternative verdict; the headline is (S).
- **Variants** (reported; any variant that changes the (S) verdict marks it **FRAGILE**): V1 Δ_vir = 18π²; V2 onset z_coll;
  V3 Υ_V 1 and Υ_V 4 for I and L; V4 CFG930's uniform recipe (Υ ×½–×2 floor added to I and L); V5 CFG827's Υ_SFH where
  available for I and L; V6 luminosity-class τ default.

## 5. Controls (run first; the lane stops and reports no class if any K fails)

- **K1** CFG42 reproduced THROUGH THIS LANE'S GENERIC ESTIMATOR with CFG42's own inputs (Moster `halo_mass` at Υ_V 2,
  Dutton–Macciò `nfw_enclosed`, CFG42's FB, its collapse-mass floor variants and constants): UF (km, err, f_ups, f_mh, tot, z)
  law and rule, CL (med, tot, z) for cls/col/m31 law and rule, H4 (n, nfex, frac, max), both footings, to 1e-9 absolute
  against `CFG42_satellites_rule_results.json`.
- **K1b** CFG45's (M) reading: UF (km, z), CL (med, z) and SPARC dwarf|M (frac_lt003, max) to 1e-6 against
  `CFG45_rule_readings_results.json`.
- **K2** (a) M_cool at z = 9 with Δ = 18π², μ = 0.6, T = 1.98e4 K equals BL01 eq. 26's 1e8 h⁻¹ M☉ × [Ω_m/Ω_m^z ·
  Δ_c/18π²]^(−1/2) (Δ_c = 18π² Ω_m^z, native h, Ω_m, Ω_m^z) within 2% (BL01's coefficient is rounded); (b) V_c(M_cool) =
  √(2k_B T/(μ m_p)) to 1e-10; (c) NFW enclosed mass equals the quadrature of its density to 1e-6; (d) the c solve satisfies
  its equation to 1e-10.
- **K3** CFG827's dwarf excess: every committed E_SFH row reproduced with CFG827's own law and committed Υ_SFH (exec'd
  read-only, no writes) to 1e-9, its OOS weighted flat mean (ufd.flat) to 1e-9, and the OOS unweighted mean (≈ +0.38) printed;
  this lane's τ50/τ90 equal CFG824's committed values to 1e-12.
- **K4** CFG874's primary isolated E and se_E, both footings, reproduced by this lane's replay to 1e-12.
- **K5** CFG880's sample: N = 83 with host counts {mw 37, m_031 31, field 7, lmc 6, m_033 1, ngc_3109 1}.
- **K6** native background: Δ_ta interpolation equals the table at its nodes (exact); Δ_vir(z = 30) within 3% of 18π².

**MUTATE** (separate outputs, after K, before main):
- **T100** (T_vir × 100): must over-predict everything: U, C, M (both), I and L each with statistic < 0 and z ≤ −2 at
  every corner on both footings, and S not CONSISTENT at every corner. Else the control did not bite (reported, verdict
  flagged).
- **T001** (T_vir × 0.01, no effective floor): must return the bare law: every class statistic equal to the bare law's
  within 1e-3 (S reading; exact 0 expected because f_ex = 0), and U's class equal to the bare law's class.

## 6. Reported separately, ungraded

- **Clusters:** f_ex and the (M) comparison for M_b 1e13 and 1e14 M☉ at z_f = 0 (a separate problem; no grade).
- **Tidal dwarfs and NGC 1052-DF2/DF4** (thought to form without a primordial halo): H-CF gives them no debris (σ_pred =
  σ_law). Compared qualitatively with CFG933 (DF2/DF4 below the isolated law) and CFG931's INFO (Lelli+15 TDGs 0.69 dex below
  the bare law). Also reported: what H-CF would give them if they had a floor halo (z_f scan below).
- **Coma UDGs** (CFG933's 9 admitted, its σ_law and σ_obs): H-CF prediction at z_f ∈ {0, 0.5, 1, 2, 3, 5} (no SFH on disk),
  both μ, C 3000, (S) and (M), against E_obs +0.760 / +0.669 ln.
- **CFG880 scatter and the common scale:** for L, the maximum-likelihood intrinsic scatter s_int of E_i (Gaussian, ε_i ⊕
  s_int) under the bare law, under H-CF at each corner and under CFG877's universal clump (CFG880's σ_x = V_x/√2, r_c 104 pc),
  with the same estimator; Spearman ρ between H-CF's predicted ln(σ_pred/σ_law) and the observed ln(σ_obs/σ_law); the spread
  of the predicted total mass inside 300 pc; the floor halos' V_vir and V_max (fixed by T and μ).
- M_cool, r_vir, c and z_f per object in the JSON.

## 7. Compute and repository rules

One core (OMP_NUM_THREADS=1, nice -n 10), one process at a time, each process under 1 GB; no downloads; other lanes' code is
exec'd read-only (no writes) and their JSON only read. Outputs: `cfg934_K.out/.json`, `cfg934_MUTATE_T100.out` +
`cfg934_results_MUTATE_T100.json`, `cfg934_MUTATE_T001.out` + `cfg934_results_MUTATE_T001.json`, `cfg934.out` +
`cfg934_results.json`. Commits with explicit paths only; no push; no edits to the LEDGER, THEORY_CANONICAL files or other
lanes' files.
