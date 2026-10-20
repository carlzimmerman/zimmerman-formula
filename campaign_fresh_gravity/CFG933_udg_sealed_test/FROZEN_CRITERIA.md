# CFG933 FROZEN CRITERIA: scoring CFG928's sealed P2 prediction on the ultra-diffuse galaxies already on disk

Written 2026-10-20 and committed ALONE, before any script of this lane exists and before any E is computed with the sealed
estimator. Block 930–939 (orchestrator reservation; CFG933 row reserved in the LEDGER at 5cff5e3bd).

κ = ½ is FITTED. The footings 9.3603e-11 and 1.1312e-10 m/s² are scored separately and never pooled. Raw data and
framework-native quantities only. The extra mass is cold energy, not a particle. Not "theory closed".

## 0. Status and disclosure (NOT blind with respect to the record)

- **What is tested.** The sealed prediction `CFG928_posit_regrade_imf/SEALED_PREDICTION_P2.md` (seal commit 3fa5a2bfc; CFG928
  criteria ba971914e, results 82a69be8f): P2 "velocity-space capture" (v_2 = 6.9503 / 6.4575 km/s, fixed on the 83 LVD
  dwarfs) predicts that gas-free pressure-supported UDGs sit nearly on the isolated law, E = +0.02 to +0.14 ln (canonical)
  and +0.016 to +0.105 (alt) for M* 3e7–3e8 M☉.
- **What was seen before this file was written:**
  - CFG31's README and JSON: the 11 Coma UDGs' stars-only isolated offset +0.397 / +0.357 dex in acceleration (L23's
    estimator, inverse-variance weighted). The seal disclosed the same number.
  - L23's data prefix (`fable_independent_2026/L23_udg_verify.py`, read, not run) and the Coma table
    `real_research/data/freundlich2022_coma_udgs.tsv`: L, M/L, R_e, σ and its error, published log g_bar and log g_obs.
  - CFG655's frozen DF2/DF4 table (as carried in `CFG657_trail_capture_rule/cfg657_capture.py`) and CFG655's ledger
    headline (σ_law, the isolated law, fails DF2/DF4 at 4.4–4.9σ from below).
- **What was NOT computed:** no E_obs or E_pred with the sealed estimator, no unweighted mean, no se, no class.
- **Expectations formed from what was seen (disclosed, not tested):**
  - Per galaxy, the sealed estimator has the same form as L23's isolated one (Wolf σ at r12 = 4/3 R_e, M_b/2 inside r12,
    ν_e). So E_obs,i ≈ ln 10 × L23's offset_i, and the differences from CFG31's +0.397 dex come from the sample rule, the
    unweighted mean and its se, and the admitted NGC 1052 objects.
  - The Coma subsample probably sits near the kill line. The NGC 1052 objects probably sit well BELOW the isolated law,
    where P2 cannot go (P2 has E_pred ≥ 0).
  - The criteria below were drafted knowing the size of the σ errors in the Coma table. They were not tuned to any E value.

## 1. Question

Do the gas-free pressure-supported UDGs on disk satisfy CFG928's sealed P2 prediction under the sealed estimator and kill
line? Each footing gets one class:
- **P2 EXCLUDED:** the kill line is met;
- **P2 CONSISTENT:** within the predicted band within errors, with enough power to tell;
- **NOT DIAGNOSTIC:** N < 5, errors too large, or the admitted sample is not one population (section 6).

## 2. The sealed estimator (unchanged; executed from CFG928's own code)

**Code path.**
- `CFG921_excess_selector_posits/cfg921.py` is exec'd read-only up to its MAIN section, exactly as cfg928.py does it (writes
  refused, sys.exit trapped). Its own K-checks must pass.
- CFG928's `udg_inputs`, `udg_from` and `udg_E` are exec'd from the text of cfg928.py, unchanged, with cfg921's `dw_pred`,
  `nu_e`, A0 and the CFG880 constants (G 6.674e-11, M☉ 1.989e30, pc 3.0857e16).
- θ, θ+ and θ− are read from `cfg928_results.json` → `sealed_numbers` → `P2|canonical` and `P2|alt`.

**Per galaxy** (inputs M*, R_e, M_g,in = 0 for gas-free; σ_g = 10 km/s, inert when w = 1):
- r12 = (4/3) R_e and g_bar = G (M*/2 + M_g,in)/r12²;
- ν = ν_e(g_bar/a0) = 1/(1 − exp(−√(g_bar/a0))), φ = 1 − 1/ν, and σ_law² = r12 g_bar ν/3;
- E_pred: solve u² = 1 + φ [w (v_2/(u σ_law))³ + (1 − w)(v_2/σ_g)³] for u ≥ 1, E_pred = 2 ln u, σ_pred = u σ_law;
- E_pred± from θ±; s_pred,i = |E_pred(θ+) − E_pred(θ−)|/2;
- **E_obs = 2 ln(σ_obs/σ_law).**

**Environment and external field.** E is relative to the ISOLATED, EFE-free ν_e law, as in CFG921 and CFG928 and as the seal
states. Coma's field and NGC 1052's field are NOT applied. The posit carries no host variable, so the same prediction is
scored in every environment (the seal: "applies to UDGs in every environment"). Distances, sizes and masses are the sources'.

## 3. Data universe and the sample rule (applied mechanically by the script)

**Universe.** Objects on disk that their source labels as ultra-diffuse galaxies, with a measured stellar or globular-cluster
line-of-sight dispersion, a size and a stellar mass:
- the 11 Coma UDGs in `real_research/data/freundlich2022_coma_udgs.tsv` (Freundlich+2022 Tables 1–2; σ from
  Chilingarian+2019, and van Dokkum+ for DF44 and DFX1). These are the objects L23 and CFG31 used;
- NGC 1052-DF2 and -DF4, from CFG655's frozen table as carried in cfg657_capture.py's GAL dict;
- DF9 and LEDA 4014647 sit in the same table and are tested by rule S1;
- excluded from the universe: the LVD dwarfs (they are P2's calibration set, and the LVD compilation carries no UDG
  label) and the Toloba+2014 Virgo dEs (labelled dE). No other UDG with σ, size and M* was found in `real_research/data`
  (top level, `dsph/`, `virgo_de/`) or in the lanes read (CFG31, CFG58, CFG655, CFG657, CFG768, CFG769). No repo-wide search
  was run.

**Rules, in order.** A galaxy enters the primary sample only if it passes all five:
- **S1 UDG size:** R_e ≥ 1.5 kpc at the source distance. This is the van Dokkum+2015 size criterion; the surface-brightness
  criterion is taken from the source's UDG label, since μ_0 is not on disk.
- **S2 gas-free:** the record carries no cold gas inside r12. For Coma, L23/CFG31 R1 ("stars only, the current baryons");
  for DF2/DF4, CFG655 ("Gas: none").
- **S3 pressure-supported:** the dynamical datum is a measured line-of-sight dispersion, and no rotation-supported
  kinematics is on disk.
- **S4 the seal's mass window:** 3e7 ≤ M* ≤ 3e8 M☉ at the primary M* (section 4).
- **S5 not in P2's calibration set** (the 83 LVD dwarfs).

**Expected membership** (the rules applied to the tabulated R_e and M*; the script recomputes it, see K4):
- **Admitted (11):** 9 Coma objects (DFX1, J125848.94+281037.1, J125904.20+281507.7, J125929.89+274303.0,
  J125937.23+274815.2, J130005.40+275333.0, J130026.26+272735.2, J130028.34+274820.5, J130038.63+272835.3) plus
  NGC 1052-DF2 (M* 2.0e8, R_e 2.0 kpc) and NGC 1052-DF4 (1.5e8, 1.6 kpc).
- **Out:**
  - DF44 (M* = 3.0e8 × 1.30 = 3.9e8 > 3e8; S4);
  - J125904.06+281422.4 (R_e 1.4 kpc; S1);
  - DF9 (R_e 1.1; S1);
  - LEDA 4014647 (R_e 0.60; S1).

**DF2/DF4.** The record labels them collision debris ("dark-matter deficient", class E in CFG655), a different formation
channel. The seal's population wording (gas-free, pressure-supported UDGs, M* 3e7–3e8, every environment) does not exclude
them, so they are admitted. They are also reported separately (section 6).

## 4. M* and Υ

- **Primary.** M* is the source's stellar mass:
  - Coma: L × (M/L)_SSP from the table (Chilingarian+2019 full-spectrum SSP M/L; I band for DF44/DFX1, R band otherwise;
    not fitted to the dynamics). This is the M* of L23 and CFG31.
  - DF2/DF4: CFG655's M* at D_ref = 20 Mpc.
- **Why not the seal's M* = 2 L_V.** The seal's kill line names the CFG880 convention M* = 2 L_V. That convention converts an
  M_V-only catalogue (LVD) into a mass. No L_V is on disk for any of these UDGs; the Coma luminosities are in R or I. The
  measured stellar mass is therefore used.
  - This choice is declared here, before any E is computed.
  - It is bracketed by the S-set's M* ±0.2 dex.
  - The literal Υ = 2 applied to the tabulated band luminosity is reported as R3 (no class weight). For old populations L_R
    and L_I exceed L_V, so R3 overstates the mass the seal's convention would give.
- **Gas.** M_g,in = 0 for every admitted galaxy (S2), so w = 1.

## 5. Errors

- **Per galaxy:** sE_i = 2 e_i/σ_obs,i, the record's dwarf convention (CFG914). e_i is the measured σ error on the side
  toward the prediction: e− if σ_obs > σ_pred, else e+. Coma errors are symmetric.
  - M*, distance and aperture errors are NOT in sE_i. They enter through the sample scatter term and the S-set.
- **Sample mean:** the unweighted arithmetic mean over the N galaxies of a graded sample (the seal's "sample mean"):
  ⟨E_obs⟩ and ⟨E_pred⟩.
- **se_obs** = max( std(E_obs,i; ddof 1)/√N , √(Σ sE_i²)/N ). This is the record's cell convention (CFG914 bins_persystem,
  CFG919 cells_persys).
- **σ_pred** of the sample mean = |⟨E_pred(θ+)⟩ − ⟨E_pred(θ−)⟩|/2. One constant, so it is fully correlated across galaxies.
- **se_c** = √(se_obs² + σ_pred²).

## 6. Kill-line arithmetic and classes

**Graded samples:**
- **G-pool:** every admitted galaxy (expected N = 11).
- **G-Coma:** the admitted Coma members (expected N = 9).
- **G-group:** the admitted NGC 1052 members (expected N = 2). It is never graded by the kill line (N < 5). Per galaxy it
  reports z_i = (E_obs,i − E_pred,i)/√(sE_i² + s_pred,i²).

**Kill line, per graded sample with N ≥ 5** (the seal, verbatim in form):
- Δ = ⟨E_obs⟩ − ⟨E_pred⟩ and z = Δ/se_c.
- The kill line is met iff |Δ| ≥ 3 se_c, i.e. |z| ≥ 3. It is two-sided.
- The seal's example: gas-free, M* ≈ 1e8, se_obs ≈ 0.10, canonical ⇒ excluded if ⟨E_obs⟩ ≥ +0.06 + 0.30 = +0.36 ln.

**Power.** A sample is diagnostic iff 3 se_c < |F0 − ⟨E_pred⟩|. F0 is the LVD dwarf class mean on that footing, read from
`cfg928_results.json` → scenarios.C1.<footing>.observed.F0.obs (+0.8562 canonical, +0.7649 alt). In words: the sample
could exclude a UDG excess as large as the dwarf excess that P2 was calibrated on. The seal's own comparison is "at most about
1/6 of the LVD dwarf class mean".

**Heterogeneity H.** Residuals r_i = E_obs,i − E_pred,i. H fires iff |⟨r⟩_Coma − ⟨r⟩_group| ≥ 3 √(se_Coma² + se_group²),
each se by the section 5 convention. It is evaluated when both populations have N ≥ 2. If H fires, the two environments do
not share one residual level, and the pooled mean is not read as consistency.

**Class per footing, in this order:**
- **P2 EXCLUDED:** the kill line is met on G-pool or on G-Coma.
  - Add the qualifier MARGINAL if every met |z| is below 3.205. That is the two-look threshold, two-sided p = 0.0027/2.
- **NOT DIAGNOSTIC:** otherwise, if any of the following holds:
  - N(G-pool) < 5;
  - G-pool or G-Coma (if N ≥ 5) fails the power test;
  - H fires.
- **P2 CONSISTENT:** otherwise.
  - Add the qualifier "2–3σ tension" if the largest |z| over G-pool and G-Coma is ≥ 2.

**Labels:**
- **FRAGILE:** the class changes under any S-variant (section 7).
- **CONTROL-LIMITED:** set by a MUTATE failure (section 8).

## 7. Sensitivity set S (carries the FRAGILE label) and reported rows R (no class weight)

**Membership is fixed at the primary**: the variants do not re-select. Every variant is run on both footings and given the
full section-6 class.
- **S-M+ / S-M−:** every M* × 10^(±0.2).
- **S-D− / S-D+ (distance):**
  - Coma × 0.95 / × 1.05 (L23's ±5%);
  - DF2 at 17.6 / 21.7 Mpc (the TRGB pair CFG655 required);
  - DF4 × 0.95 / × 1.05.
  - Scaling: M* ∝ D², R_e ∝ D, σ unchanged.
- **S-A− / S-A+ (aperture and anisotropy):** every σ_obs and its errors × 1/1.15 / × 1.15. This is L23's "15% coherent
  error in σ" (0.12 dex in g).

**Reported rows:**
- **R1 L23's weighting.** Inverse-variance weighted means with weights sE_i⁻² and se = (Σ sE_i⁻²)^(−1/2) (plus σ_pred), on
  G-pool and G-Coma.
- **R2 sample variants:**
  - (a) the source label only, dropping S1 (adds J125904.06+281422.4);
  - (b) dropping S4 (adds DF44);
  - (c) both (all 11 Coma + DF2 + DF4);
  - (d) all 11 Coma alone.
- **R3 Υ = 2 on the tabulated band luminosity** (Coma; DF2/DF4 unchanged).
- **R4 DF2/DF4 secondary dispersions** from CFG655's table: DF2 Emsellem+19 stars 10.8 +3.2/−4.0; DF4 stars 8.0 +2.3/−1.9.
  Per galaxy z only.
- **R5 the disclosed question.** The sealed-estimator E for CFG31's 11 Coma UDGs: unweighted mean and L23-weighted mean, at
  both footings. Does CFG31's +0.397 / +0.357 dex hold under the sealed estimator?

## 8. Controls

**K-tests** (any failure stops the lane: no class is reported, and a dated amendment is required):
- **K1:** L23's committed isolated offsets reproduced by this lane's own code. The path: its own TSV parse, M* = L × M/L,
  g_obs = 3σ²/r12, g_bar = G(M*/2)/r12², ν_e at h9's a0 (9.36e-11 / 1.13e-10), L23's inverse-variance weights with
  err = hypot(elgobs, elgbar). The tolerances:
  - +0.3965 / +0.357, parsed from L23_udg_verify.out, within 6e-4 (CFG31's tolerance; printed rounding);
  - CFG31's C1 "mine" (+0.396517 / +0.357273) within 1e-9;
  - CFG31's R1 stars-only at the campaign footings (+0.396511 / +0.357051) within 1e-9.
- **K2:** CFG928's sealed band reproduced from CFG928's code.
  - The path: cfg921 exec'd read-only (its own checks pass), then cfg928's udg_* functions exec'd from its text, at θ, θ±
    from the JSON.
  - All 9 sealed rows × 2 footings must match cfg928_results.json to ≤ 1e-12 relative: E_free, s_pred, σ_law, log g_bar
    and σ_pred.
  - θ must equal the seal's 6.9503 / 6.4575 to its printed digits.
  - The band's ends must round to the seal's +0.022 / +0.140 (canonical) and +0.016 / +0.105 (alt).
- **K3:** this lane's standalone P2 solver (bisection on ln u) equals the CFG928 code path to ≤ 1e-9, on the grid and on
  every universe galaxy's inputs.
- **K4 inputs:**
  - DF2/DF4 equal CFG657's GAL dict (evaluated from its source text) and CFG655's printed table.
  - The constants equal L23's.
  - The mechanically computed membership equals section 3's expectation.
- **K5:** with M* = L × M/L at the campaign footings, the sealed-path E_obs,i = ln 10 × (L23-form offset_i) to ≤ 1e-12 for
  all 11 Coma UDGs. This shows the two estimators coincide galaxy by galaxy.

**MUTATE** (separate outputs `_MUTATE_onlaw` and `_MUTATE_plus04`):
- **Set-up:** the primary membership and each galaxy's real fractional errors (sE_i), with:
  - **onlaw:** σ_obs,i := σ_law,i (E_obs = 0);
  - **plus04:** σ_obs,i := σ_law,i × 10^0.2 (E_obs = +0.4 dex in g = +0.921 ln).
- **Required:**
  - onlaw → P2 CONSISTENT on both footings;
  - plus04 → P2 EXCLUDED on both footings.
- **If onlaw fails:** CONSISTENT is not available to the main run. It would read NOT DIAGNOSTIC, labelled CONTROL-LIMITED.
- **If plus04 fails:** the sample cannot exclude a CFG31-sized offset. CONSISTENT is again not available, labelled
  CONTROL-LIMITED.
- **EXCLUDED** is arithmetic on the kill line and is unaffected by the MUTATE outcome.

## 9. Compute, hygiene, amendments

- One core (OMP_NUM_THREADS=1, nice -n 10), one process at a time, each under 1 GB. Nothing downloaded.
- Run order:
  - K only (`CFG933_MODE=K`);
  - MUTATE onlaw, then plus04 (`CFG933_MODE=onlaw|plus04`);
  - main.
- Committed outputs: `cfg933{_K,_MUTATE_onlaw,_MUTATE_plus04,}.out` and the matching `cfg933_results*.json`.
- Other lanes' files are only read: CFG928's sealed files, cfg921.py, L23, CFG31, CFG655/657.
- Any change after this commit is a dated, labelled amendment (AMENDMENT_A*.md) that states whether any number had been
  seen.
- κ = ½ FITTED; footings never pooled; not theory closed. EXCLUDED is reported as plainly as CONSISTENT. Nothing here says
  the data favour the framework.
