# CFG926 FROZEN CRITERIA: three small reframings of the pressure-supported excess (B)

Committed alone, before any script of this lane and before any number of this lane. Block 920–929 (row reserved in the
LEDGER, 2026-10-20 ~14:30: "CFG926 small reframings B (fossil a0 at formation, IMF α–σ for old spheroids, lensing ESD
estimator for round vs flat lenses)"). Kind: HYPOTHESIS TEST (three reframings, pre-registered). κ = ½ is FITTED.
Footings 9.3603e-11 (canonical) and 1.1312e-10 (alt) m/s² are graded separately and never pooled. Raw data and
framework-native quantities only. The extra mass is cold energy, not a particle. Not "theory closed". Nothing here says
the data favour the framework.

## 0. What was read before freezing (disclosure; not blind)

- THEORY_CANONICAL_2026-10-18.md (with its 10-19/10-20 addenda and notes).
- CFG921 README and `cfg921.py` (fact list F0–F10, the K machinery, `obs_struct`, `fact_values`, `lens_central`, CFG919
  exec'd read-only); `cfg921_results.json` "observed" block. Seen: F0 dwarfs +0.856 ± 0.102 / +0.765 ± 0.102, F1 red/sph
  lenses +0.293 ± 0.067 / +0.203 ± 0.067, F2 blue/disc +0.008 ± 0.091 / −0.083 ± 0.091, F3 +0.137 / +0.057, F4 +0.002 /
  −0.053, F5 clusters +0.560 ± 0.077 / +0.476 ± 0.077, F6 +0.83 / +0.84, F8b −0.66, F10 −1.36 (ln units).
- CFG919 README and the cell code (`build`, `lens_set`, `cells_lens`, LWIN, FLOOR0); CFG850 README + code (A_red 1.587 →
  1.451 at +0.123 → 1.324 at +0.20, A_blue 1.016, colour split 5.0σ / 4.0σ / 2.9σ); CFG851 README + code (b 0.060,
  log g† −10.05); CFG849, CFG829 (+ code), CFG840 READMEs; CFG667 README + head of code (+0.123 dex OLD − YOUNG on Taylor+11
  masses); CFG827 README + code + criteria (slope +0.010 ± 0.012 per Gyr, mean E +0.38 ln σ, 25/28 above); CFG824 head
  (τ50 / τ90 reader).
- Prior record on these reframings, cited and not redone: CFG395 (fossil a0 in ETG HI: under the record's DE-tracking a0(z)
  the fossil sign is NEGATIVE, deep-limit −0.030 to −0.043 dex; NON-DISCRIMINATING); CFG390 ledger row ("fossil switch FAIL",
  "fossil a0 not possible on SPARC"); CFG922 (IMF on cluster-core stars CANNOT: needed α 72.4 / 59.8 vs SLACS α_max 3.78;
  Salpeter/Chabrier 1.778; needed-mass entries read from `cfg922_results_A1.json`); CFG531 (early/late split persists in the
  own-law ESD-space profile, ε early +0.83 vs late −0.31; a recalled mass-based IMF was PROVISIONAL there); AUDIT_SLUGGS
  (under the law a Salpeter mass already over-predicts the inner JAM mass of massive ETGs in 15/16, +0.12 dex); CFG108 note;
  CFG223 a0(z) laws and its C1 values (M-DEC R(1,2,3) = 0.990, 0.874, 0.775; E(1), E(2) = 1.790, 3.032); the B21 README
  (g_obs = 4GΔΣ, B21 Eq. 7; Radius column = g_bar).
- Data files inspected for format only: `real_research/data/atlas3d_fj_table.tsv` (260 rows, qual 0–3),
  `slacs_auger2009_lenses.tsv`, Weisz+14 `table5/6.tsv`.
- **Expectations formed before freezing (disclosed):** FLAT a0 gives exactly zero (by construction); the record's DESI
  √ρ_DE a0(z) gives a small negative (wrong-sign) fossil for z_f ≳ 0.6 and a tiny positive bump below; the rival a0 ∝ H(z)
  gives a positive fossil of the dwarf order, probably overshooting red lenses for z_f ≳ 2, too small and with the wrong
  g_bar slope for clusters, and an age trend in dwarfs. R5: a Cappellari-like relation gives the red lenses roughly
  +0.15 to +0.25 dex more stellar mass (mental estimate); clusters NO EFFECT (CFG922). R6: expected tiny (orientation
  averaging). No number of this lane was computed before this commit.

## 1. Common inputs and facts (read-only reuse)

- **CFG921 machinery**, exec'd read-only (all writes refused, `sys.exit` trapped): lines from the top of `cfg921.py` to the
  "P5: QUMOND thin-disc quadrature" marker (K1–K4, K6, per-system inputs DWD/CLD, `lens_central`), and from the "observed
  structures per footing / variant" marker to `ZTF =` (`obs_struct`, `fact_values`, `obs_facts`). Through it CFG919, CFG914,
  CFG880, CFG883, CFG687 are exec'd/read exactly as CFG921 does. The P5 quadrature and the grading code are not run.
- **Facts graded here** (V0 structure, FLOOR0 = 0.05 dex per cell, ln units): F0 dwarfs (83 LVD, Υ_V = 2, CFG880 gas),
  F1 lenses n > 2 with +0.123 dex (CFG667) on M*, F2 lenses n < 2, F3/F4 SPARC small/large, F5 eRASS1 clusters (MID+OUTER),
  plus diagnostics F6 (cluster slope), F8b (dwarf slope), F7 (DW − LS matched). Observed values = CFG921's, reproduced (K3).
- **Threshold:** 0.05 dex = 0.05 ln 10 = 0.1151 in ln units.
- **Grading of one target** (observed excess E_obs, residual after the reframing E_res, both ln):
  - RESOLVES-target: |E_res| ≤ 0.5 |E_obs| (at least half removed, no overshoot beyond half).
  - PARTIAL-target: |E_obs| − |E_res| ≥ 0.1151.
  - WORSENS-target: |E_res| − |E_obs| ≥ 0.1151.
  - NO EFFECT-target: otherwise.
- **Class of a reframing (per footing, per declared variant):**
  - **RESOLVES:** every graded target is RESOLVES-target AND the rotator condition holds AND the dwarf condition holds.
  - **PARTIAL:** not RESOLVES and at least one graded target is PARTIAL-target or better (label "PARTIAL (MIXED)" if another
    graded target WORSENS).
  - **WORSENS:** no target PARTIAL or better and at least one WORSENS-target, or a condition is broken by ≥ 0.1151.
  - **NO EFFECT:** otherwise.
- **Rotator condition:** SPARC small/large (F3, F4) and blue/disc lenses (F2) after the reframing stay within 2σ of zero
  and move by < 0.1151.
- **Dwarf condition:** R4 targets the dwarfs, so its condition is |F0_obs − F0_pred| < 2 √(se² + s_pred²) AND the CFG827
  age slope consistent within 2σ (section 2). R5 and R6 do not target the dwarfs; their condition is that the dwarfs' excess
  is not increased by ≥ 1 se_F0.
- **Brackets:** corners declared below are each graded; a class that changes across corners is labelled BRACKET-DEPENDENT
  (the primary class is the one at the primary values).

## 2. R4 — fossil a0

**Posit.** Pressure-supported systems freeze their cold energy at formation z_f; gas-rich rotators keep re-settling to
today's a0. Per system the law's prediction becomes g_bar ν(g_bar / (a0 F(z_f))) instead of g_bar ν(g_bar / a0), so the
predicted excess is E_pred = ln[ν(y/F)/ν(y)], y = g_bar/a0 (today's g_bar; the frozen quantity is a0 only).
ν = ν_e for dwarfs and lenses, ν_mono for clusters (as CFG921). Rotators (SPARC, n < 2 lenses): E_pred = 0 by the posit
(the rotator condition is therefore met by construction, recorded as such, not as a test).

**a0(z) laws, F(z) = a0(z)/a0(0)** (CFG223's definitions, reused):
- FLAT: F = 1 (framework).
- M-DEC: F = √[(1+z)^{3(1+w0+wa)} exp(−3 wa z/(1+z))] (framework, a0 ∝ √ρ_DE). Primary (w0, wa) = (−0.838, −0.62)
  (Pantheon+ central, as CFG223); corners DESY5 (−0.752, −0.86), Union3 (−0.667, −1.09). Variant M-DEC-c: F held at its
  z = 2.5 value beyond z = 2.5 (the chart's solid range; CPL beyond is extrapolation).
- H(z): F = E(z) = √[Ω_m(1+z)³ + Ω_Λ] (the RIVAL; declared contrast only).
- **Background (framework-native):** the footings encode Ω_Λ = (9.3603/11.312)² = 0.68471, Ω_m = 1 − Ω_Λ, and
  H0 = √(8π/3)·2·a0_alt/c = 67.40 km/s/Mpc (alt footing = ½c√(Gρ_crit)). Lookback time t_L(z) = ∫ dz/[(1+z)H]; z(τ) by
  inversion. Variant: Ω_m = 0.308 (CFG680–685 raw BAO under flat a0), same H0.

**Formation epochs (declared):**
- Dwarfs: Weisz+14 τ50 per dwarf from CFG824's reader (table6 combined where given, else table5; linear in log t; τ = 12.59
  Gyr when the oldest-node fraction already exceeds 0.5). Matched to the 83 LVD names by exact name after CFG824's NAMEMAP.
  Unmatched dwarfs: M_V > −7.7 (ultra-faint) → τ50 = 13.3 Gyr (CFG827's UFD burst; corner 12.59); brighter unmatched →
  the median τ50 of the matched dwarfs (corners: matched minimum and maximum). s_pred for the dwarf condition = half the
  F0_pred range over these fallback corners. Variant R4-hi: HI-bearing dwarfs (DWD `hi`) re-settle (E_pred = 0).
- Red/n > 2 lenses: declared bracket z_f ∈ [1, 3] (recalled stellar-age range of massive early types, PROVISIONAL, not on
  disk); primary = geometric midpoint in (1+z): z_f = √8 − 1 = 1.828.
- Clusters: declared assembly bracket z_f ∈ [0.3, 1.0]; primary = √2.6 − 1 = 0.612.
- Observation epoch: the facts are measured against a0(0); z_obs = 0 for all (the rival's own z_obs shift for lenses at
  z ~ 0.25 is a caveat, ≤ 0.03 dex, CFG255).

**Predictions through CFG921's operators:** dwarfs per dwarf → cell means → F0/F8b operators; lenses per B21 point →
cell value ln(w·(g_law·e^{E_pred})) with CFG921's window weights → F1 operator; clusters per (cluster, band) →
ln(Σ W·P·e^{E_pred}/Σ W·P) per window → F5/F6 operators.

**Graded targets:** F0 (dwarfs), F1 (red lenses), F5 (clusters). E_res = E_obs − E_pred.
**Dwarf condition, part 2 (CFG827 age slope):** on CFG827's 28 out-of-sample dwarfs (SFH Υ at [M/H] −1.31, CFG827's law
and weights), E_fossil,σ = ½ ln[ν(y/F(z50))/ν(y)]; s_pred = CFG827's weighted slope of E_fossil,σ vs τ90;
z_slope = (s_obs − s_pred)/se_obs with s_obs ± se_obs from `cfg827_results.json`. |z_slope| < 2 required.
Reported (no class weight): mean E_fossil,σ vs mean E_SFH on the same 28; F6 and F8b predicted vs observed.

**Reading rule (frozen):** if only the rival H(z) moves the excesses, that is evidence about a0(z) (against the framework's
distinctive FLAT / DE-tracking a0), not a rescue, and is reported that way, together with the record's independent
standing of the rival (L37: a0 ∝ H(z) fails the CMB n_s test; CFG223: high-z kinematics cannot separate it).

## 3. R5 — stellar M/L of old spheroids (IMF α–σ)

**Relation (zero free constants; fitted once on on-disk external data, never on lensing):**
- ATLAS3D (Cappellari+13 XV/XX, `atlas3d_fj_table.tsv`), galaxies with qual ≥ 1 and finite values:
  y = logML_stars − logML_Salp (Cappellari's IMF normalisation α_Salp), x = logsig_e − log10(200). OLS y = a + b x.
  Uncertainty: 2000 bootstrap resamples (seed 926); the 16/84% of log α at the target σ are corners.
- σ for a lens class: ATLAS3D OLS log σ_e = c + d (log M*_Chab − 10.5), log M*_Chab = logL + logML_Salp − log10(S/C),
  S/C = SLACS median Salpeter/Chabrier mass ratio (CFG922's 1.778, recomputed from the table).
- Shift relative to the LePhare (Chabrier, provisional per CFG922) masses: Δ_IMF = max(0, a + b x(σ) + log10(S/C))
  (primary clip: no system lighter than Chabrier).
- Framework-native variant R5-law: per ATLAS3D galaxy solve Υ_JAM = Υ_* ν_e(G Υ_* (L/2) / r12² / a0) for Υ_* (r12 from
  logr12 arcsec and Dist_Mpc), y_law = log10(Υ_*/Υ_Salp), same OLS; per footing.

**Application:**
- Red/n > 2 lenses (F1, CFG919 cells rebuilt with `lens_set("sph", f, shift)` + `cells_lens`, GLS with FLOOR0):
  shift = 0.123 (CFG667) + Δ_IMF(σ at log M* = 10.81 + 0.123), corners log M* ± 0.2 dex and the bootstrap 16/84%.
  Also reported: IMF alone without the +0.123; the CFG850 window amplitudes (colour and Sérsic splits, z) and CFG851's
  b, log g† after the correction (diagnostic).
- Rotators primary: blue/n < 2 lenses and SPARC unchanged (disc-dominated systems are not bottom-heavy; the relation is
  calibrated on early types). Variant R5-blue: Δ_IMF at log M* = 10.45 applied to the n < 2 lenses (upper bound, since discs
  have lower σ at fixed M*).
- Dwarfs primary: clipped → zero change. Variant R5-dw: unclipped (lighter) per dwarf at σ_obs = σ_law e^{E/2}:
  g_bar' = g_bar (α w + 1 − w), E' = E − ln[g_bar' ν(g_bar'/a0) / (g_bar ν(g_bar/a0))].
- BCG / cluster cores (secondary target, F5): α_Chab at σ_BCG = 300 km/s (corners 250, 400) applied to all central stars.
  With CFG922's needed α_need and needed concentrated mass (U entry: λ and mass), the removable fraction is
  f_m = (α_Chab − 1)/(α_need − 1); upper bound on the removal ΔE ≤ ln(1 + f_m·X), X = λ·M_need,4/M_need,U (Newtonian
  response bound, concave law). Graded as a target with E_res = E_obs − bound.

**Graded target:** F1 (primary; the question asked). Secondary target F5 labelled separately; it moves the overall class
only if it WORSENS. Rotator and dwarf conditions as section 1. Re-derived split significance: (F1 − F2)/√(se1² + se2²)
on the cells, and CFG850's z_colour / z_sersic, after the correction.

## 4. R6 — lensing estimator for round vs flat lenses

**B21 estimator** (B21 Eq. 7, README on disk): g_obs = 4GΔΣ(R), compared with g_law(g_bar,B21), g_bar,B21 = G M_b/R²
(point mass at the projected radius).

**Declared projection model (analytic/numeric, no data fit):**
- Round (n > 2): Hernquist, M_b = 10^(10.81 + 0.123) M☉, a = R_e/1.8153, R_e = 10^(0.56 lm − 5.54) kpc (CFG921's LS
  relation). Flat (n < 2): razor-thin exponential disc, M_b = 10^10.45 M☉, R_d = R_e/1.678, R_e = 0.10 M^0.14
  (1 + M/3.98e10)^0.25 kpc (CFG921's LD relation). Corners: masses ± 0.2 dex.
- Field: QUMOND (the record's settled field, as CFG921 P5): ∇²Φ = ∇·[ν_e(|g_N|/a0) g_N]. Gauss's law gives the exact
  spherically averaged enclosed total mass M_tot(<r) = (r²/G)⟨ν_e(|g_N|/a0) g_N·r̂⟩ over the sphere. Disc g_N from ring
  sums (complete elliptic integrals); sphere analytic.
- Stack: isotropic lens orientations ⇒ the stacked ESD is the ESD of the spherically averaged density (exact; checked
  numerically, K). ΔΣ(R) = M_cyl(R)/(πR²) − Σ(R), M_cyl = ∫ M(R cosh t) sech²t dt, Σ = 2R ∫ ρ(R cosh t) cosh t dt.
- Truncation: primary none (isolated law to infinity); variants M_tot held constant beyond r_t = 3 Mpc and 1 Mpc
  (estimator sensitivity only; external-field physics is CFG925's).
- β_conv(R) = 4GΔΣ(R) / [G M_tot(<R)/R²] (pure conversion); β_full(R) = 4GΔΣ(R) / g_law(G M_b/R²) (conversion + point-mass
  g_bar). Evaluated at every B21 point of the F1 / F2 windows (R = √(G M_b / g_bar)); cell value ln(w·(g_law·β)) with
  CFG921's weights; class value through the F1/F2 operators. Δ_est = F1_β(round) − F2_β(flat).
- Orientation-selection bound (reported, no class weight): q2(r) = P2 Legendre coefficient over the monopole of
  ν|g_N| g_N·r̂ on the sphere for the disc; bound 3·max|q2| over the window radii.

**Graded target:** the n > 2 − n < 2 difference, E_obs = F1 − F2; E_res = E_obs − Δ_est. Primary class from β_conv (the
question asked); β_full reported with its own class. Rotator condition: F2 − F2_β(flat) within 2σ of zero. Dwarfs untouched
(stellar kinematics), condition met by construction.

## 5. Controls

- **K1:** CFG850 rows (A_red, A_blue, A_sph, A_disc, z_colour, z_sersic at shifts 0, 0.123, 0.20; both footings) reproduced
  through CFG829's loader to ≤ 1e-9.
- **K2:** CFG851 (b, log g†, χ²) for the red calibration at shifts 0.123 and 0 (both footings) reproduced through CFG851's
  `calibrate` to ≤ 1e-6 relative (Nelder–Mead; deterministic).
- **K3:** CFG921's own K-checks K1–K4, K6 pass inside the exec; CFG921's observed facts F0–F10 (both footings) reproduced by
  `obs_facts` to ≤ 1e-9; F1 rebuilt by this lane's arbitrary-shift path at shift 0.123 equals CFG921's F1 to ≤ 1e-9.
- **K4:** CFG824 τ50/τ90 (36 rows) and CFG827 E_SFH, Υ_SFH (36 rows) reproduced to ≤ 1e-9; CFG827 OOS slope reproduced.
- **K5:** a0(z) laws: CFG223's C1 values (M-DEC 0.990 / 0.874 / 0.775 ± 0.002 at z = 1, 2, 3; E(1), E(2) = 1.790, 3.032
  ± 0.002 at Ω_m 0.315) and the footing background (H0 67.40 ± 0.01; age of the universe finite and > every τ50).
- **K6 (R6 numerics):** SIS → β = 1 (≤ 1e-4); point mass → 4/π (≤ 1e-4); Plummer Newtonian ΔΣ vs closed form (≤ 1e-4);
  ring-sum disc g_N vs Freeman midplane field at 3 R_d (≤ 1e-3); point-mass red vs point-mass blue law profiles give
  Δ_est = 0 (≤ 1e-6); Monte-Carlo isotropy check of M_cyl for an oblate cloud (≤ 4 MC σ).
- **K7:** CFG922's needed α (72.43 / 59.83) and SLACS S/C (1.778) and α_max (3.78) reproduced from the files.
- Any K failure: the lane stops, no class.
- **MUTATE** (separate outputs `_MUTATE_<mode>`; exit 1 = bites):
  - `z0`: z_f = 0 for every system → every R4 prediction exactly 0 (≤ 1e-12) under every law.
  - `imf0`: α ≡ 1 (zero slope, zero offset) → R5 F1 returns to the baseline exactly (≤ 1e-12), every R5 shift 0.
  - `geom`: the flat class given the round model with the round class's (M, R_e) → Δ_est = 0 (≤ 1e-12).
  - Reported only: `imf0` variant with zero slope but kept offset (α = α(200 km/s) for every class, blue and dwarfs
    unclipped) → the change in the F1 − F2 split.

## 6. Outputs and rules

- Scripts in this directory; outputs named by mode: `cfg926_K.out/.json` (K only), `cfg926_MUTATE_<mode>.out/.json`,
  `cfg926.out`, `cfg926_results.json`. One core (OMP_NUM_THREADS=1, nice -n 10), < 1 GB, one process at a time. Nothing
  downloaded. No other lane's file edited.
- Any post-hoc change is a dated, labelled amendment (AMENDMENT_A*.md), never an edit of this file.
- Reported plainly whatever the class: NO EFFECT and WORSENS as plainly as RESOLVES. κ = ½ FITTED; footings never pooled;
  not theory closed; no claim that the data favour the framework.
