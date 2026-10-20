# CFG884 — FROZEN CRITERIA: do Sextans' two stellar populations need extended mass beyond one finite clump?

Frozen before any script (owner block 880–889; the LEDGER row says 884–889 are free for this chat; no CFG884 dir, row or
commit existed). κ = ½ fitted; footings a0 = 9.3603e-11 (canonical, primary) and 1.1312e-10 (alt), never pooled;
ν_e(y) = 1/(1 − e^{−√y}); raw data, framework-native only (no ΛCDM halo profile anywhere); no dark-matter particle; not
theory closed.

## Question
Sextans has two chemically separated populations (Tolstoy et al. 2025, A&A 698, A53, Table 2): a compact, colder
metal-rich one (MR) and an extended, hotter metal-poor one (MP). One gravitational potential must support both. Does the
CFG877 finite cold clump (one per faint dwarf) supply it, or does the MP population require extended extra mass?

## Inputs (repo only)
- **Populations (PROVISIONAL):** values from `sol61_push/cfg853_independent_transport_2026_10_19/source_extraction.json`
  (sha256 9a6114429005c7436d2e2cd1cf766bdeb7e11f8c2c4f6692d8f4a9d7e1115839), a web-tool extraction made by another session
  and never checked against the publisher's table. They are copied into this lane as `inputs_tolstoy2025_table2.json` (with
  that hash) so the lane does not depend on an uncommitted file. Distance D0 = 84.7 kpc (the source's adopted RR Lyrae value).
  - MR: number fraction 0.63, projected Plummer half-number elliptical radius Rh = 0.339 ± 0.021 deg, σ = 7.0 ± 0.4 km/s.
  - MP: fraction 0.37, Rh = 0.62 ± 0.05 deg, σ = 10.5 (+0.8 / −0.7) km/s.
  - Global σ = 8.3 ± 0.3 km/s (FLAMES only; reported, not scored).
- **Stars:** `real_research/data/dsph/lvd_dwarf_mw.csv`, Sextans: m_V = 10.95 (M_V = m_V − DM; the LVD's own M_V −8.72 is
  m_V − 19.67), ellipticity e = 0.27, rhalf = 22.8 arcmin (major axis). L_V = 10^{0.4(4.83 − M_V)} with M_V recomputed at the
  distance in use. Υ_V = 2 primary, bracket {1, 2, 3} (no SFH-based Υ exists for Sextans in CFG827). No gas (HI upper limit only).
- **Clump and extended component (no refit):** V_x from `CFG870_cored_component_joint/cfg870_results.json`
  (10.6547 canonical / 10.5870 alt km/s), r_c = 104 pc.
  - (C) CFG877 finite clump: M_x(<r) = min[V_x² r³/(G (r² + r_c²)), M_cl], M_cl = 81 (V_x/√2)⁴/(4 G a0).
  - (X) CFG870 extended (uncapped) component: M_x(<r) = V_x² r³/(G (r² + r_c²)).
  - As in CFG870/877, the component's gravity G M_x(<r)/r² adds linearly to the law's acceleration from the baryons. The
    clump is not passed through ν_e (CFG877's construction).
- Constants as in CFG877: G = 6.674e-11, M_⊙ = 1.989e30 kg, pc = 3.0857e16 m.

## Potentials (per footing)
- (L) law alone: g_L(r) = g_N(r) ν_e(g_N(r)/a0), g_N = G M_*(<r)/r².
  - **Stellar mass profile, primary:** two Plummer spheres with mass fractions 0.63/0.37 (the selected-sample number
    fractions read as mass fractions; disclosed) and scales equal to the MR/MP tracer scales (central Rh).
  - **Variant (in the nuisance grid):** one Plummer sphere with the LVD rhalf.
  - Total M_* = Υ_V L_V.
- (C) g_L + G M_x,C(<r)/r²;  (X) g_L + G M_x,X(<r)/r².
- **Reported, not deciding — EFE variant:** g_N ν_e((g_N + g_ext)/a0), with g_ext = G·6.0e10 M_⊙/R_GC², R_GC = 88.91 kpc
  (CFG820's algebraic form and MW constant, applied per radius). It can only lower the law term, so the isolated law is the
  lenient choice for under-prediction.

## Geometry
- Angular radii are converted at distance D as a = D tan(Rh) × c.
- **Primary:** c = √(1 − e) = 0.8544 (circularized, as CFG877/LVD rhalf_sph).
- **Variant:** c = 1 (major axis).
- The same c multiplies the tracer scales, the stellar scales and the aperture. One LVD ellipticity is used for both
  populations (per-population ellipticities were not extracted).

## Prediction: population-averaged line-of-sight dispersion
For a Plummer tracer of scale a (3D ν ∝ (1 + r²/a²)^{−5/2}), constant anisotropy β, the spherical Jeans equation
(ν σ_r² = r^{−2β} ∫_r^∞ s^{2β} ν g ds) is projected and averaged with the projected Plummer number weighting inside a circular
aperture R_max: ⟨σ²_los⟩ = ∫_0^{R_max} 2πR Σ σ²_los dR / ∫_0^{R_max} 2πR Σ dR, evaluated as one radial kernel integral
∫ W(s) g(s) ds.
- **Primary aperture: R_max = ∞ (the whole population).** There the moment is exactly β-independent: ⟨σ²_los⟩ =
  (1/3)∫4πs³ν g ds (projected virial identity; it holds for any spherical g, including the law's).
- The source gives no radial range for the 303-star sample. Because each population's Rh was fitted from that sample,
  coverage must reach beyond Rh_MP = 0.62°. The finite apertures R_max = 1.0° and 1.5° (elliptical, × c) are therefore
  nuisance cases.

## Nuisance grid Θ (all values allowed; "lenient" = the most favourable member of the grid)
- **Shared by both populations, S:**
  - Υ_V ∈ {1, 2*, 3};
  - c ∈ {0.8544*, 1};
  - D ∈ {D0·10^{−0.02}, D0*, D0·10^{+0.02}} (±0.1 mag, the LVD distance-modulus error);
  - R_max ∈ {1.0°, 1.5°, ∞*};
  - stellar profile ∈ {two-Plummer*, LVD single}.
- **Per population, P:**
  - β ∈ {−0.5, 0*, +0.3};
  - Rh ∈ {Rh − err, Rh*, Rh + err}.
  - (+0.3 is radial anisotropy, which strictly violates the An–Evans cusp condition for a cored Plummer tracer. It is kept
    only as a lenient case. β is irrelevant at R_max = ∞.)
- **Primary point θ0** = all starred values. The stellar profile uses the central Rh even when the tracer Rh is varied.

## Statistic
z(θ) = ln(σ_obs/σ_pred)/√(e_ln² + 0.05²), with:
- e_ln = ln(σ_obs/(σ_obs − e_−)) when σ_pred < σ_obs, and ln((σ_obs + e_+)/σ_obs) otherwise;
- 0.05 a model-systematics floor in ln σ (CFG883's).

Positive z means the model under-predicts.

## Classes (per footing)
Definitions:
- robust_under(M, p): z ≥ 3 at every θ ∈ Θ;
- robust_over(M, p): z ≤ −3 at every θ;
- matches(M): some s ∈ S exists for which each population has some (β, Rh) ∈ P with |z| < 2;
- fails(M): robust_under or robust_over for at least one population.

Decision, in order:
1. **FINITE CLUMP CONSISTENT** — matches(C).
2. **SEXTANS NEEDS EXTENDED MASS** — not 1, robust_under(C, MP), and matches(X): the CFG870 extended form suffices.
3. **BOTH FORMS FAIL** — not 1, robust_under(C, MP), and fails(X). Sextans needs extra mass beyond one clump that the CFG870
   extended form cannot supply either; the failing population and direction are recorded.
4. **CLUMP SHORT, EXTENDED MARGINAL** — not 1, robust_under(C, MP), and X neither matches nor fails.
5. **UNDECIDED** — otherwise. Any robust_over(C, ·) is labelled inside it.

Overall: if the footings agree, that class. Otherwise "canonical class (alt class)", with canonical as the headline
(primary footing).

**Also reported (not deciding):**
- σ_pred and z at θ0 for L, C, X and both populations, plus the min–max over Θ;
- whether X over-predicts MR (robust_over(X, MR) and z at θ0);
- the EFE variant at θ0;
- the global mixture σ² = Σ f_p σ_p² against 8.3 ± 0.3;
- the **required-mass diagnostic**: on top of baselines L and C at θ0 (whole population, β-free), the extra Newtonian mass
  from y_i = 3 a_i (σ_obs,i² − σ_B,i²)/G. For each baseline:
  - the single-tracer floors y_i;
  - the sharp two-tracer floor M ≥ y1[(h² − 1)/(h²/R^{2/3} − 1)]^{3/2} (h = a_MP/a_MR, R = y_MP/y_MR, valid for 1 < R < h³);
  - the saturating shell radius;
  - M/M_cl.

## Controls
- **K1a (code identity, deciding):** for a Newtonian self-consistent isotropic Plummer (g = G M r/(r² + a²)^{3/2}), the
  kernel's aperture average equals the analytic (πGM/32a)·(1 + X²)[1 − (1 + X²)^{−3/2}]/X² (X = R_max/a), which tends to
  πGM/(32a) as X → ∞. Required to 1e-6 relative at X = 0.5, 1, 3 and ∞.
- **K1b (deciding):** at R_max = ∞, β = −0.5 and +0.3 return the same value as β = 0 (πGM/32a) to 1e-6. At R_max = 50a the
  three β agree to 1e-3 (the aperture tends to the whole population).
- **K1c (deciding, CFG877 identity):**
  - M_cl from the formula equals `cfg877_results.json` Mcl_Msun to 1e-9;
  - the radius where the cored profile reaches M_cl is printed (the audit's 237 / 205 pc, to ±1 pc);
  - a re-implementation of CFG876/877's Wolf-form Sextans prediction (law_cfg876 + clump at r12) equals the stored
    5.565162739890287 / 5.533173671715427 km/s to 1e-9.
- **K1d (reported):** the Jeans whole-population σ² against the Wolf form g(r12) r12/3 (r12 = 4/3 R_e = 4/3 a, since a Plummer tracer's projected half-number radius is a) for
  both tracers in potential C at θ0. Expected to agree within ~10 %; informational.
- **K3 (reported, external, not deciding):** with that session's inputs (M_V −8.72, Υ 2, c = 1, D0, two-Plummer 0.63/0.37,
  a = D tan Rh, ν_e), reproduce CFG853's baseline whole-population moments: 16.45296 / 21.02271 km²/s² canonical and
  18.06947 / 23.09294 alt (`baseline_run_002/results.json`, exponential kernel), plus its sharp floor 7.6447e8 / 9.2064e8 M_⊙,
  to 1e-4 relative. That packet is uncommitted, so this is a cross-check only.
- **MUTATE** (`CFG884_MUTATE=injectC|injectX`, separate outputs `*_MUTATE_<mode>.*`):
  - injectC: σ_obs of both populations is replaced by model C's θ0 prediction (per footing; errors kept). Required:
    FINITE CLUMP CONSISTENT on both footings, so the class flips from any non-consistent real result.
  - injectX: the same with model X's θ0 prediction. Required: matches(X) on both footings and class ≠ BOTH FORMS FAIL.
  - Both are plumbing checks that the statistic responds. They are not power estimates.

## Pre-freeze disclosures
- **Hand estimates made before freezing** (Wolf/virial forms, Υ 2, canonical):
  - law alone ≈ 4.2 km/s for both populations;
  - C: MR ≈ 5.7, MP ≈ 5.1 km/s;
  - X: MR ≈ 7.3, MP ≈ 7.4 km/s;
  - expectation: C robustly short on MP (~7σ), X short on MP by ~3–4σ at θ0, possibly reachable in lenient corners.
  - Analytic point noted before freezing: for any flat-V_c component a Plummer tracer's whole-population σ²_los = V_c²/3,
    independent of its scale, so an isothermal-like extended form cannot by itself create the MR/MP contrast (σ² ratio 2.25).
- **Seen before freezing:** CFG853's RESULT.txt, VIRIAL_DERIVATION.md, BASELINE_EXTENSION.md and baseline_run_002 numbers
  (law-baseline moments 16.45/21.02 km²/s², extra-mass floor 7.6e8 M_⊙ canonical); the CFG877 audit (Sextans needs 3.71× M_cl
  in the Wolf form).
- **Data limits:**
  - the extraction is provisional;
  - Table 2 gives elliptical number-density fits and Gaussian widths of a selected 303-star sample, not complete spherical
    virial moments, and the Jeans tracer density is taken equal to the sample weighting;
  - fractions are read as mass fractions;
  - membership, binaries (which inflate σ; no binary correction is applied) and instrument offsets are not modelled;
  - Sextans' tidal history and non-equilibrium are not modelled;
  - one ellipticity is used for both populations.
