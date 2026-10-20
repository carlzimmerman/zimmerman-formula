# CFG926: three small reframings of the pressure-supported excess (B): fossil a0, IMF α–σ, lensing estimator

**Bottom line.**
- **R4, fossil a0:** the framework's own a0(z) cannot make the excess. FLAT a0 gives exactly zero (**NO EFFECT**). The DESI
  √ρ_DE a0(z) gives the wrong sign: old dwarfs would sit 0.07 dex *below* the law (**WORSENS**, bracket-dependent). Only the
  rival a0 ∝ H(z) gives a positive fossil (**PARTIAL**). It matches the dwarf mean, overshoots the red lenses, gives 28% of
  the cluster excess with the wrong g_bar slope, and predicts a dwarf age trend at the edge of CFG827's bound (1.9σ). That
  is evidence about a0(z), not a rescue.
- **R5, IMF α–σ:** **RESOLVES the red-lens excess** on both footings as frozen. Give early types the ATLAS3D dynamical stellar
  M/L (≈ 1.5× Chabrier at σ ≈ 186 km/s) on top of CFG667's +0.123 dex, and keep discs at Chabrier. F1 falls from +0.127 to
  +0.048 dex canonical (62% removed) and from +0.088 to +0.009 dex alt. The red/blue split drops below 2σ.
  - This rests on the declared asymmetry (discs not bottom-heavy). The fitted α–σ slope is shallow, and it accounts for only
    −0.02 dex of the split. With one relation applied to both lens classes, the split barely moves (**PARTIAL (MIXED)**).
  - On CFG850's colour-window statistic the canonical removal is 49%, and under the record's own SLUGGS IMF ceiling (post hoc)
    it is 45%. Both of those would read PARTIAL.
  - Clusters: NO EFFECT. Dwarfs: unchanged.
- **R6, lensing estimator:** **NO EFFECT** on both footings, at every corner and every truncation. With isotropic stacking the
  4GΔΣ conversion biases round and flat lenses alike to 0.002 dex. The point-mass g_bar effect is 0.01 dex and goes the wrong
  way.

The dwarf and cluster-core excesses remain unexplained by these three reframings.

κ = ½ is FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s² are never pooled. Raw data and framework-native quantities only. The
extra mass is cold energy, not a particle. Not "theory closed". Nothing here says the data favour the framework.

- **Kind:** HYPOTHESIS TEST (three reframings, pre-registered). Block 920–929 (LEDGER row "CFG926 small reframings B").
- **Criteria:** `FROZEN_CRITERIA.md`, 48a7a31ae, committed alone before any script or number.
- **Amendment:** `AMENDMENT_A1.md`, caca2bc7f, POST HOC, written before any run. It clarifies two controls (K6e, MUTATE geom)
  whose frozen wording assumed identical lens windows, the alt-footing CFG827 slope, and the corner bookkeeping. No class rule,
  threshold, target, input or bracket was changed.
- **Not blind:** the record's numbers for the facts, CFG850/851, CFG827, CFG922, CFG395 and AUDIT_SLUGGS were read before
  freezing. The expectations formed then are disclosed in criteria §0.

## Classes (per footing; E in ln units, dex = E/ln 10)

| reframing | canonical | alt | key numbers (canonical / alt) |
|---|---|---|---|
| R4 FLAT a0 (framework) | NO EFFECT | NO EFFECT | every prediction exactly 0 (by construction) |
| R4 M-DEC √ρ_DE, DESI CPL (framework, primary) | **WORSENS** [BRACKET-DEPENDENT: NO EFFECT / WORSENS] | **WORSENS** [same] | dwarfs F0 pred −0.161 / −0.162; red lenses −0.054; clusters +0.011 |
| R4 M-DEC corners DESY5 / Union3 | WORSENS / WORSENS | WORSENS / WORSENS | F0 pred −0.199 / −0.232 |
| R4 M-DEC clamped at z 2.5 (variant) | NO EFFECT | NO EFFECT | F0 pred −0.069 |
| R4 a0 ∝ H(z) (RIVAL, contrast) | **PARTIAL** [PARTIAL / PARTIAL (MIXED)] | **PARTIAL** [PARTIAL / PARTIAL (MIXED) / RESOLVES] | F0 +0.814 vs +0.856 / +0.815 vs +0.765; F1 +0.495 vs +0.293 / +0.497 vs +0.203; F5 +0.157 vs +0.560 / +0.159 vs +0.476 |
| R5 IMF α–σ on red lenses (primary target) | **RESOLVES** (9/9 corners) | **RESOLVES** (9/9 corners) | F1 +0.293 → +0.112 / +0.203 → +0.022 |
| R5 on BCG / cluster cores (secondary) | NO EFFECT | NO EFFECT | removal ≤ 0.018 (CFG922 bound) |
| R6 4GΔΣ conversion, round vs flat (primary) | **NO EFFECT** (all corners, all truncations) | **NO EFFECT** | Δ_est −0.0041 / −0.0041 vs E_obs +0.286 |
| R6 full B21 estimator (conversion + point-mass g_bar) | NO EFFECT | NO EFFECT | Δ_est −0.023 / −0.023 (wrong direction) |

## R4: fossil a0

**Posit.** Pressure-supported systems keep a0(z_f) from their formation epoch. Their predicted excess is
E = ln[ν(g_bar/(a0 F(z_f))) / ν(g_bar/a0)], with F = a0(z)/a0(0). Rotators re-settle, so E = 0 for them; the rotator condition
holds by construction and is not a test.

**Inputs.**
- a0(z) laws: CFG223's definitions, reused.
- Background: the one the footings encode (Ω_Λ = (9.3603/11.312)² = 0.6847, H0 = 67.40 km/s/Mpc).
- Dwarfs: Weisz+14 τ50 through CFG824's reader. 29 of the 83 LVD dwarfs are matched. The 33 unmatched ultra-faints get
  13.3 Gyr (corner 12.59). The 21 unmatched brighter dwarfs get the matched median, 10.56 Gyr (corners 4.92 and 12.59).
- Red lenses: declared z_f ∈ [1, 3], primary 1.83. Clusters: z_f ∈ [0.3, 1.0], primary 0.61.

**Framework laws.** FLAT is identically zero.

The DESI-tracking a0 is lower in the past: F = 0.74 at the dwarfs' median z_f of 3.4, 0.89 for the lenses, 1.025 for the
clusters. So it pushes the old dwarfs below the law:
- F0 −0.161 ln (−0.070 dex), WORSENS in 5 of the 6 dwarf corners;
- red lenses −0.054, clusters +0.011, both NO EFFECT.

This is the same sign that CFG395 found in early-type HI (−0.03 to −0.04 dex, deep limit). Two qualifications:
- Beyond z ≈ 2.5 the CPL curve is an extrapolation. Clamping it there gives −0.069, NO EFFECT.
- The predicted age slope, −0.008 per Gyr, is consistent with CFG827 (z +1.5).

**The rival a0 ∝ H(z)** (F = 5.2 for the dwarfs, 2.8 for the lenses, 1.42 for the clusters):

| target | predicted | observed | label |
|---|---|---|---|
| dwarfs F0 (canonical) | +0.814 | +0.856 ± 0.102 | RESOLVES-target (z +0.23; fallback spread ±0.15) |
| CFG827 age slope | +0.0326 / Gyr | +0.0101 ± 0.0121 | inside 2σ, barely (z −1.86; alt −1.90) |
| red lenses F1 | +0.495 | +0.293 | overshoots by 0.20: NO EFFECT |
| clusters F5 | +0.157 | +0.560 | PARTIAL (28%) |

The diagnostics are not graded:
- The cluster slope F6 comes out −0.015, against +0.83 observed: wrong sign.
- The dwarf g_bar slope F8b (−0.40 vs −0.66) and size slope F10 (−0.61 vs −1.36) have the right sign. The oldest, faintest
  dwarfs get the largest fossil.
- Mean E_σ on CFG827's 28 dwarfs: +0.233 fossil vs +0.325 observed.
- If the HI-bearing dwarfs re-settle (variant), the class does not change.

**Corners.** On the alt footing the rival reaches RESOLVES only at the low edge of both declared brackets (z_f = 1 for lenses
and clusters; F1 +0.280, F5 +0.267). It does so for every dwarf fallback (6 of 54 corners per H(z) law). On the canonical
footing no corner resolves: F5 +0.267 against 0.560 just misses half.

**What it means (the frozen reading rule).**
- Only the rival's a0(z) moves the excesses. That is evidence about a0(z): it would point toward a0 ∝ H(z) and away from the
  framework's distinctive FLAT / DE-tracking a0. It is not a rescue of the framework.
- Even so, the rival fossil fails the clusters' amplitude and slope. It overshoots the red lenses unless they froze late
  (z_f ≈ 1). Its dwarf age trend sits at 1.9σ from CFG827's measurement.
- The record's independent standing of the rival is unchanged: L37, the CMB n_s test fails for a0 ∝ H(z); CFG223, high-z
  kinematics cannot separate it.

## R5: IMF α–σ for old spheroids

**Relation.** Zero free constants. It is fitted once on the on-disk ATLAS3D table (Cappellari+13 XV/XX, qual ≥ 1, N = 187),
never on lensing:
- log α_Salp = −0.0748 + 0.0986 log(σ_e/200) (OLS);
- log σ_e = 2.1496 + 0.2792 (log M*_Chab − 10.5);
- Salpeter/Chabrier = 1.778 (SLACS median, as CFG922).

Red/n > 2 lenses at log M* 10.81 + 0.123 have σ = 186 km/s, which gives Δ_IMF = +0.172 dex (bootstrap and ±0.2 dex mass
corners: 0.157–0.192).

**Framework-native check (R5-law).** Solve the ATLAS3D JAM M/L with the law's own ν at r½ instead of Cappellari's NFW
halos. α_law sits only 0.017 / 0.033 dex below the literature α, and gives Δ_IMF +0.168 / +0.154. So the law's inner dynamics
allow this IMF at σ ≈ 186 km/s.

**Red-lens target (F1, CFG919/921 cells, rebuilt through CFG919's own cell code).**

| | canonical | alt |
|---|---|---|
| F1 before (with CFG667 +0.123) | +0.293 ± 0.067 (+0.127 dex) | +0.203 ± 0.067 (+0.088 dex) |
| F1 after (+0.123 + 0.172) | **+0.112 (+0.048 dex), 62% removed** | **+0.022 (+0.009 dex), 89% removed** |
| corners (9) | F1 0.087–0.130, all RESOLVES | F1 −0.003–0.040, all RESOLVES |
| split n>2 − n<2, cells | 0.286 (z 2.53) → 0.104 (z 0.92) | 0.286 (2.53) → 0.105 (0.93) |
| CFG850 window: A_red / colour z | 1.451 → 1.208 / 3.98 → 1.82 (49% of ln A removed) | 1.324 → 1.102 / 3.98 → 1.82 (65%) |
| CFG850 window: A_sph / Sérsic z | 1.486 → 1.250 / 3.81 → 1.73 | 1.356 → 1.140 / 3.81 → 1.73 |
| IMF alone, without CFG667: F1 / A_red | 0.431 → 0.260 / 1.587 → 1.369 | 0.340 → 0.170 / 1.448 → 1.249 |
| CFG851 lens law after (b, log g†) | 0.057, −11.24 (was 0.060, −10.05) | 0.048, −11.61 |

**Why the result is conditional.**
1. **The asymmetry carries it.** The fitted slope is shallow: 0.099 per dex of σ in OLS on the on-disk table. The σ-dependence
   alone changes the red − blue split by only −0.046 ln (−0.02 dex); this is the reported zero-slope run.
   - If the same relation is applied to the n < 2 lenses (σ 137 km/s, Δ +0.159; variant R5-blue), F2 falls to −0.112 / −0.203.
     The disc lenses then sit 0.05–0.09 dex below the law, the split stays at z 2.1, and the class is PARTIAL (MIXED).
   - R5 resolves the red lenses only if discs are not bottom-heavy. That is the literature reading, and it was declared
     before any number, but it is a premise, not a result.
2. **The statistic matters.** On CFG850's colour window (10^−13.3–10^−11.9) the canonical removal is 49%, just short of half,
   which would be PARTIAL. On the graded F1 cells it is 62%.
3. **The record's own SLUGGS ceiling** (AUDIT_SLUGGS: under the law a Salpeter mass already over-predicts the inner JAM mass by
   a median 0.12 dex, so Δ ≤ +0.13; post hoc, no class weight). Canonical F1 → +0.163 (45%, PARTIAL); alt +0.072 (64%,
   RESOLVES). Those SLUGGS centrals are more massive than the KiDS red lenses, so the ceiling is generous.

**Other targets and conditions.**
- **Clusters / BCGs:** α_Chab 1.53–1.60 at σ 250–400 km/s supplies < 1% of CFG922's needed mass (α_need 72.4 / 59.8).
  Removal ≤ 0.018 ln: NO EFFECT, as CFG922 found.
- **Dwarfs:** unchanged in the primary rule. Extrapolated to σ ≈ 10 km/s, the shallow relation gives α_Chab ≈ 1.1 (slightly
  heavier, not lighter), so F0 drops by only 0.033 (0.856 → 0.823): NO EFFECT, right direction.
- **Rotators:** unchanged in the primary rule.

## R6: lensing estimator, round vs flat

**Model.** QUMOND field, with Gauss's law for the spherically averaged enclosed mass:
- round lenses: Hernquist with CFG921's R_e relation;
- flat lenses: a razor-thin exponential disc from ring sums.

An isotropic stack sees only the spherical average; this is exact and was checked by Monte Carlo. The B21 estimator is then
g_obs = 4GΔΣ (B21 Eq. 7), compared with g_law(G M_b/R²).

| | canonical | alt |
|---|---|---|
| β_conv = 4GΔΣ / g_true: n>2 / n<2 | 1.002–1.017 / 1.004–1.027 | 1.002–1.015 / 1.004–1.025 |
| Δ_est (conversion), = Δ_samp + Δ_geom | **−0.0041** (+0.0007 − 0.0047) | **−0.0041** |
| β_full: n>2 / n<2 | 0.970–0.998 / 1.004–1.027 | 0.968–0.997 / 1.004–1.024 |
| Δ_est (full estimator) | −0.0234 (wrong direction) | −0.0233 |
| observed n>2 − n<2 | +0.286 | +0.286 |
| truncation 3 Mpc / 1 Mpc | Δ_conv −0.0040 / −0.0030 | −0.0041 / −0.0031 |
| max \|Δ_conv\| over 9 mass corners | 0.0042 | 0.0043 |

- In the stack the conversion is nearly the same for both geometries. The law's profile at 30–300 kpc is close to isothermal,
  for which 4GΔΣ is exact.
- The only geometric difference that survives is the extended spheroid's light inside R. It makes B21's point-mass g_bar too
  high for round lenses, so their true excess is about 0.01 dex *larger*.
- **Orientation selection** (e.g., edge-on discs migrating between classes): this breaks isotropy.
  - The frozen bound, 3·max|q2| = 0.22, is set by the innermost grid radius (10 kpc ≈ 5 R_d).
  - At the actual n < 2 window radii (32–231 kpc; post hoc, no class weight), max |q2| = 0.019 and the class-weighted mean is
    0.005. So even a fully aligned selection moves ΔΣ by ≲ 2%.
- Independent corroboration from the record: CFG531(c) finds the early/late split in ESD space with the law's own projected
  profile (ε early +0.83, late −0.31). The split is not an artefact of the 4GΔΣ conversion.

## Controls

| control | result |
|---|---|
| K1 | CFG850's 10 rows (A_red, A_blue, z_colour, A_sph, A_disc, z_sersic) through CFG829's loader: max diff 0 |
| K2 | CFG851 (b, log g†, χ²) at shifts 0.123 and 0, both footings: max rel diff 0 |
| K3 | CFG921's own K1–K4, K6 pass inside the read-only exec; CFG921 facts F0–F10 (value, se) reproduced, max diff 0 (F0 +0.8562 ± 0.1019 / +0.7649 ± 0.1018); this lane's arbitrary-shift lens path equals F1/F2 to 6e-17 |
| K4 | CFG824 τ50/τ90 (36), CFG827 Υ_SFH/E_SFH (36) and the OOS slope (+0.0101 ± 0.0121) reproduced exactly |
| K5 | CFG223 C1: M-DEC 0.989 / 0.874 / 0.775, E(1), E(2) 1.790 / 3.032; footing background H0 67.400, age 13.79 Gyr |
| K6 | SIS β = 1 (2e-11); point mass 4/π (0); Plummer ESD (2e-16); ring sums vs Freeman at 3 R_d (1.5e-7); far field (3e-6); point-mass scale invariance (2e-12); Monte-Carlo isotropy within 0.9σ |
| K7 | CFG922 α_need 72.43 / 59.83, SLACS S/C 1.778, α_max 3.782 |
| MUTATE z0 | z_f = 0 for every system: max \|prediction\| 2.7e-17, **BITES** (exit 1) |
| MUTATE imf0 | α ≡ 1: max change 5.6e-17, **BITES** (exit 1) |
| MUTATE geom | flat class given the round model: max \|Δ_geom\| 0, Δ_samp unchanged, **BITES** (exit 1) |

## Post-hoc items (dated 2026-10-20, all after the first main run; reporting only, no class moved)

- R4 corner list in the JSON, to identify the alt RESOLVES corners.
- R5 SLUGGS-ceiling sensitivity.
- R6 q2 at the window points.

The frozen classes were identical before and after they were added. Run order: K, the three MUTATEs, main. After the
diagnostics were added, all five were re-run; the computations were unchanged.

## Limitations

- **Formation epochs.** The red-lens and cluster brackets are declared, recalled and PROVISIONAL. 54 of 83 dwarfs have no
  Weisz+14 SFH and use the declared fallback. τ50 is capped at 12.59 Gyr for SFHs whose oldest node already exceeds half.
- **Observation epoch.** The fossil is taken relative to a0(0) at z_obs = 0 for every system. The rival's own shift at the
  lenses' z ≈ 0.25 is ≤ 0.03 dex (CFG255), not modelled.
- **IMF relation.** It is OLS on one on-disk table. Published fits that treat errors in both variables are steeper (not on disk,
  not used). The LePhare IMF is Chabrier per CFG922, provisional. The IMF is applied to total g_bar as CFG850 does, which
  slightly favours R5. Stacks use the class median mass, with ±0.2 dex corners.
- **R6 model.** Razor-thin discs, Hernquist spheroids, no gas disc, no external field (truncation is only an estimator
  sensitivity; the EFE is CFG925's domain).
- Lens σ, masses and sizes are proxies (B21 medians, the ATLAS3D σ–M* relation, Shen+03 sizes).

## Reproduce

One core, < 0.3 GB, seconds each; nothing downloaded.
- `CFG926_KONLY=1 OMP_NUM_THREADS=1 nice -n 10 python3 cfg926.py` → `cfg926_K.out`, `cfg926_K.json` (exit 0)
- `CFG926_MUTATE=z0|imf0|geom ...` → `cfg926_MUTATE_<mode>.out/.json` (exit 1 = bites)
- `OMP_NUM_THREADS=1 nice -n 10 python3 cfg926.py` → `cfg926.out`, `cfg926_results.json` (exit 0)

Committed code is exec'd read-only, with every write refused and `sys.exit` trapped:
- CFG921 (and through it CFG919/914/880/883/687);
- CFG829, CFG851, CFG824, CFG827.

No other lane's file was edited.
