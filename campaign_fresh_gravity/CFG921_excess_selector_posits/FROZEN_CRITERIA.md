# CFG921 FROZEN CRITERIA: excess-selector constraint intersection (five candidate new posits vs the CFG820–920 facts)

Block 920–929 (LEDGER reservation row CFG920–929: "CFG921 excess-selector constraint intersection (candidate new posits vs
the CFG820–920 facts)"). Frozen 2026-10-20, committed ALONE before any script of this lane exists and before any number of
this lane has been computed. Kind: CONSTRAINT INTERSECTION (pre-registered; five candidate posits, at most one new constant
each, one calibrator class, graded on every other class).

κ = ½ is FITTED. The footings 9.3603e-11 / 1.1312e-10 m/s² are scored separately and never pooled. Raw data and
framework-native quantities only (no HMcode, BAHAMAS, ΛCDM mass function or ΛCDM halo relation enters any number). The extra
mass is cold energy, not a particle. No knob scans: each posit has one constant, fixed once on the calibrator. Not "theory
closed". Any post-hoc change will be a dated, labelled AMENDMENT_A*.md committed before the numbers it affects are reported.

## 1. Question

CFG919's theory note: the record's kinetic system (CFG638) sees the baryons only through ρ_b, so its settled state cannot
order the excess by kinematic state; any selector is a NEW POSIT. Question: does ANY single new posit, with at most ONE new
constant fixed on ONE calibrator class, reproduce the open excess facts of CFG820–920 together?

## 2. Record check and disclosure (NOT blind)

Read before freezing (targeted reads only): THEORY_CANONICAL_2026-10-18.md with all its addenda; LEDGER rows CFG820, 821,
827, 829, 838, 839, 843, 845, 850, 851, 852, 853, 860, 861, 870–878, 880–884, 888, 889, 912–916, 919, 920, the CFG920–929
reservation row, CFG580–582, CFG686, CFG687; the CFG923 result commit headline (late binding vs the framework clock:
canonical CONTRADICTED, alt UNDERDETERMINED) and the CFG922 criteria commit headline (cluster-core baryon re-check, in
progress); CFG919 README, FROZEN_CRITERIA, code and results JSON; CFG914 code (input section); CFG918 criteria head
(unrelated capacity bound); CFG638/CFG541 README lines on the phantom (the PM uses the QUMOND phantom).

Numbers seen before freezing (all from committed outputs of other lanes):
- CFG919 V0 cells and class means (canonical / alt, E in ln units): DW +0.856 ± 0.102 / +0.765 ± 0.102; SS +0.137 / +0.057
  (± 0.084); SL +0.002 / −0.053 (± 0.050); LD +0.008 / −0.083 (± 0.091); LS +0.293 / +0.203 (± 0.067); CL +0.560 / +0.476
  (± 0.077); GC +0.254 ± 0.134; the per-window cells (e.g. DW 1.71 at 10^−13.2 falling to 0.40 at 10^−11.8; CL −0.35 at
  10^−12.2 rising to +1.18 at 10^−10.9; LS 0.55 → 0.01); F1 A 0.558 ± 0.049 / 0.455 ± 0.049.
- CFG687 A (b0.67, rc0.15, f0.20): MID 1.910 ± 0.119 / 1.754 ± 0.109, OUTER 1.012 ± 0.087 / 0.927 ± 0.080.
- CFG850 (+0.123, 0.0): A_red 1.451 / 1.324, A_sph 1.486 / 1.356, A_disc 1.066 / 0.973.
- CFG845 D −0.273 ± 0.026; CFG820 L95 23.96 / 24.72 pc; CFG876 law-alone large-dwarf E +0.241 ± 0.105 / +0.195 ± 0.105;
  CFG860 c0 −0.150 ± 0.122, cG −0.064 ± 0.093 (both footings); CFG920 median M_req 3.815 / 3.185 and class UNDERDETERMINED;
  CFG912 lens median log M_gal red 10.81 / blue 10.45 (parsed by CFG914's K3b).

Expectations formed before freezing from back-of-envelope estimates (disclosed; nothing computed):
- P1 should fail by orders of magnitude, because lens and cluster dispersions exceed the dwarfs' by 10–100×.
- P2 and P3 should under-predict the red lenses and the clusters.
- P4's red-lens prediction should depend strongly on the lens central size. A rough estimate passes only for R_e ≈ 1 kpc,
  below the declared bracket.
- P5 should give |δ| ≲ 0.1, short of the dwarfs.
- P2–P5 should all fail the cluster facts.

Sibling lanes: CFG922 (cluster-core baryon census) is in progress and is NOT used. The VC variant (section 6) reports every
class with the cluster facts withheld, conditional on CFG922. CFG923 is not used as an input.

## 3. Common definitions

- **Excess:** E = ln(g_obs/g_law) exactly as CFG919 defines it (ν_e law; clusters: CFG687's law with its own FP0 a0, as
  CFG914/919). g_L(g) = g·ν_e(g/a0). Phantom fraction φ = 1 − g_bar/g_L. Clusters: φ = 1 − M_b/M_L per cluster and band
  (CFG914's law687 arrays).
- **Cold surplus geometry (P1–P4).** Extra cold energy gravitates in the Newtonian way (class A, CFG888). A surplus s per unit
  settled cold energy (ρ_c = (1 + s) ρ_ph) gives g = g_L + s(g_L − g_bar), so E = ln(1 + sφ). P1 and P3 have their own forms
  below.
- **Kinematic and structural inputs** (declared here; brackets are used by the lenient-corner rule of section 6):

| class | random σ / rotation v_rot | mass fractions | density ρ̄_b (P4) | bracket |
|---|---|---|---|---|
| DW: 83 LVD dwarfs (CFG880 sample, CFG919 cells) | stars: v_rot 0, σ_* SELF-CONSISTENT (σ_*² = r12·g/3, Wolf; the posit sets g); gas inside r12 (CFG880 gas_in): σ_g 10 km/s, v_rot 0 | w = (M*/2)/(M*/2 + M_g,in), Υ_V 2 (= CFG919 f_sph) | (M*/2 + M_g,in)/(4π r12³/3) | σ_g ∈ {6, 10, 20} km/s |
| SS/SL: SPARC (CFG919 selection) | CFG919 convention: σ_d 10 km/s, v_rot = V_flat (max V_obs if V_flat = 0) | M*/M_b = 0.5 L[3.6]/(0.5 L[3.6] + 1.33 M_HI) (SPARC Table 1) | (M_b/2)/(4π r12³/3), r12 = (4/3) R_eff | σ_d ∈ {6, 10, 20} km/s |
| LS/LD: B21 isolated lenses, Sérsic n > 2 / n < 2 | central galaxy: f_P 0.8 / 0.2 (CFG919 proxy); v_c² = r12·g_L(G(M*/2)/r12²); σ² = f_P v_c²/3; v_rot² = (1 − f_P) v_c² | P3 only: M*/M_b 0.95 / 0.65 | (M*/2)/(4π r12³/3) | f_P (LD, LS) ∈ {(0.2, 0.8), (0.43, 0.57), (0.10, 0.97)}; M* shift ∈ {−0.2, 0, +0.2} dex; R_e × {0.5, 1, 2}; P3 M*/M_b: n>2 {0.90, 1.00}, n<2 {0.50, 0.80} |
| CL: eRASS1 stack (CFG687, MID+OUTER, per cluster and band) | v_c² = G M_L/R; σ² = v_c²/3; v_rot 0 | M*/M_b = 0.2/1.2 (CFG687 f_s 0.20) | M_b/(4π R³/3) | — |
| GC: 31 globulars (CFG883), unscreened diagnostic only | Baumgardt σ0, ARot (class-median v/σ if missing) | stars only | 1.6 L_V/2 inside 4/3 r_hl | — |

- **Lens central masses:** M* = 10^(10.81 + 0.123) for n > 2 (CFG912 red median + CFG850 shift) and 10^10.45 for n < 2 (blue
  median). These are declared proxies, because B21's Sérsic bins have no own medians on disk.
- **Lens central sizes:** R_e from the Shen et al. 2003 size–mass relations, an empirical input, not ΛCDM:
  - early type: log R_e = 0.56 log M − 5.54;
  - late type: R_e = 0.10 M^0.14 (1 + M/3.98e10)^0.25 kpc;
  - in both, r12 = (4/3) R_e.
- **Lensing regime:** lensing measures 30–300 kpc, so the central galaxy's surplus factor (s, X or L) applies to the phantom
  field at each B21 point.

## 4. Candidates (forms fixed here; one constant θ each, except P5 with none)

- **P1: stress coupling. θ = c_* (a velocity).**
  - Cold energy is sourced by the trace of the baryons' random-motion stress: ρ_x = 3P_b/c_*², with P_b = Σ_k ρ_k σ_k².
    Ordered rotation is excluded by symmetry (CFG919).
  - It gravitates in the Newtonian way, so M_x = X·M_b with X = 3 Σ_k m_k σ_k²/c_*², and E = ln(1 + X/ν).
  - Dwarfs are self-consistent:
    u² = [1 + 3(1 − w)σ_g²/(ν c_*²)] / (1 − w r12 g_bar/c_*²), with u = σ_*/σ_law and E = 2 ln u.
  - No equilibrium ("runaway") if w r12 g_bar ≥ c_*².
- **P2: velocity-space capture. θ = v_2.**
  - Cold energy is cold and at rest in the system frame. Baryons capture and retain it in proportion to their velocity-space
    density at the cold energy's velocity.
  - This is the unsaturated (v_cap ≪ σ) limit, so the capture amplitude and v_cap fold into one constant:
    s = Σ_k m_k (v_2/σ_k)³ exp(−v_rot,k²/2σ_k²).
  - Dwarfs are self-consistent: u² = 1 + φ[w(v_2/(uσ_law))³ + (1 − w)(v_2/σ_g)³].
- **P3: late binding with post-binding escape. θ = v_w.**
  - Cold energy settles to the law's phantom of the baryons present at binding and is latched thereafter. The latch is part
    of the posit (CFG915 LC family).
  - Star formation after binding drives outflows that escape with energy-driven efficiency (v_w/v_c)²; the post-binding star
    fraction (1 − q) is absorbed into v_w. Hence L = M_b(t_bind)/M_b,now = 1 + (M*/M_b,now)(v_w/v_c)².
  - Present field: g = g_bar + [g_L(L g_bar) − L g_bar], so E = ln(g/g_L(g_bar)).
  - Clusters use the same form with CFG687's law: E = ln[(1 + Lν(Lg_b/a0) − L)/ν(g_b/a0)].
  - Dwarfs are self-consistent with v_c² = 3σ_*² = 3u²σ_law².
- **P4: phase-space-density capture, the "second variable at fixed pressure support". θ = Q_*.**
  - The retained surplus is proportional to the baryons' phase-space density at the cold energy's velocity:
    s = (ρ̄_b/Q_*) Σ_k m_k (2πσ_k²)^−3/2 exp(−v_rot,k²/2σ_k²).
  - Dwarfs are self-consistent: u² = 1 + φ(ρ̄_b/Q_*)[w(2πu²σ_law²)^−3/2 + (1 − w)(2πσ_g²)^−3/2].
- **P5: geometry. No new constant (the one extra candidate, justified from the record).**
  - Settled, ρ_c = ρ_ph and the record's field equation is QUMOND (CFG541/919). CFG919's theory note item 3 lists geometry as
    "not done".
  - For spheres QUMOND equals the algebraic law. For flattened discs the in-plane field departs by δ_disc(R).
  - κ is fitted on discs with the algebraic law, which absorbs ⟨δ_disc⟩. Hence spherical systems and the point-mass lensing
    regime are predicted at E = −⟨δ_disc⟩, and SPARC discs at 0.
  - δ_disc is computed for a razor-thin exponential disc by Hankel-transform quadrature of the QUMOND phantom (surface term
    (ν0 − 1)Σ plus volume term −g_N·∇ν/4πG, spherical truncation at 100 R_d).
  - ⟨δ⟩ is the mean over central g_N/a0 ∈ {0.1, 1, 10} × R/R_d ∈ [1, 6].
  - P5 is graded on every class including DW (it has nothing to calibrate).

### 4b. What each posit predicts, derived from the forms before any comparison

| fact | P1 stress | P2 velocity capture | P3 late binding | P4 phase-space capture | P5 geometry |
|---|---|---|---|---|---|
| dwarfs | E grows with w r12 g_bar/c_*² (baryonic potential depth); runaway possible | colder dwarfs carry more | slow, gas-poor dwarfs carry more | compact cold dwarfs carry more | −⟨δ⟩ ≈ 0 (under) |
| red lenses (σ ~ 10× dwarfs) | X ~ 100× dwarfs: far ABOVE dwarfs (DW − LS sign wrong) | s ~ 1e-3 of dwarfs: ≈ 0 (under) | L ≈ 1: ≈ 0 (under) | depends on R_e (ρ̄ ∝ R_e^−3) | −⟨δ⟩ (under) |
| blue lenses | large (σ ~ 60 km/s) | ≈ 0 (rotation offset) | ≈ 0 | ≈ 0 (rotation offset) | −⟨δ⟩ |
| SPARC | σ_d = 10 km/s, same as dwarfs, at smaller ν: large | ≈ 0 | small (SS), ≈ 0 (SL) | ≈ 0 | 0 |
| clusters | enormous | ≈ 0 (under) | ≈ 0 (under) | ≈ 0 (under) | −⟨δ⟩ (under) |
| cluster rise with g_bar | rises (ν falls) | flat | flat | flat | flat |
| dwarf fall with g_bar | likely rises (sign risk) | falls (colder at low g) | falls (slower at low g) | ? | flat |
| gas split (HI-bearing − gas-free) | small | ≈ 0 | negative (less loss) | positive (gas adds ρ̄) | 0 |
| size split (log r12 at fixed g_bar) | positive (r12 g_bar) | negative | ? | negative (ρ̄ ∝ g_bar/r12) | 0 |

## 5. Calibrator and facts

**Calibrator (one class, all posits): DW.** These are the 83 LVD dwarfs of CFG880, in CFG919's V0 cells.
- θ is fixed so that the GLS class mean of the predicted DW cells equals the observed class mean.
- Predicted cells use the same cells and the same covariance weights. A predicted DW cell is the mean of the per-dwarf
  self-consistent E_pred,i of its members.
- θ_± come from calibrating to the class mean ± its se; σ_pred = |pred(θ_+) − pred(θ_−)|/2.
- The calibration is solved by root finding (brentq). If no θ reaches the observed mean, the result is "calibration impossible",
  and the posit FAILS.

**Graded facts (sources = committed lanes; "here" = computed by this lane's frozen estimator from the CFG919 inputs):**

| id | fact | source and number (canonical / alt) | estimator |
|---|---|---|---|
| F0 | dwarf excess (graded for P5 only) | CFG919 DW +0.856 ± 0.102 / +0.765 ± 0.102 (+0.37 / +0.33 dex); CFG827 +0.38 in ln σ | GLS class mean |
| F1 | red/spheroidal lens excess | CFG919 LS +0.293 ± 0.067 / +0.203 ± 0.067; CFG850 A_sph 1.486 / 1.356 | GLS class mean of predicted LS cells (A_pred = GLS amplitude of g_L·e^E_pred on B21's windows) |
| F2 | blue/disc lenses on the law | CFG919 LD +0.008 ± 0.091 / −0.083 ± 0.091; CFG829 A_blue 1.016 ± 0.086 | same |
| F3 | small rotating discs on the law | CFG919 SS +0.137 ± 0.084 / +0.057 ± 0.084; CFG845 D −0.273 ± 0.026 (H-PRIM excluded) | galaxy means per cell, then GLS class mean |
| F4 | large discs on the law | CFG919 SL +0.002 ± 0.050 / −0.053 ± 0.050 | same |
| F5 | cluster excess (×1.8) | CFG919 CL +0.560 ± 0.077 / +0.476 ± 0.077; CFG687 A_MID 1.910 ± 0.119 / 1.754 ± 0.109 | stacked A_pred = Σ W·P·e^E_pred / Σ W·P per cell, then GLS class mean |
| F6 | cluster excess rises with g_bar | here: GLS slope dE/dlog g_bar over the CL cells (CFG919 cells −0.35 → +1.18) | GLS line, cell covariance + floor |
| F7 | dwarfs carry 3–5× the red lenses at the same g_bar | here: GLS mean of E_DW − E_LS over the windows where both exist (CFG919: 1.71/1.41 vs 0.55/0.28) | GLS, DW diag + LS block |
| F8a | dwarf cells shape (uniform excess below 1e-12) | here: χ² of predicted vs observed DW cells after calibration, dof n − 1 | χ² p |
| F8b | dwarf excess falls with g_bar | here: GLS slope over the DW cells | GLS line |
| F9 | no gas trend in the dwarfs | here: OLS E_i = a + b·lg_i + c·HI_i on the 83 dwarfs, bootstrap se (2000, rng 921); source CFG860 NOT GAS (c0 −0.150 ± 0.122, cG −0.064 ± 0.093), CFG874 | coefficient c |
| F10 | the excess spans small and large dwarfs | here: OLS E_i = a + b·lg_i + d·log10 r12_i, same bootstrap; source CFG876 (large dwarfs, law alone, +0.241 ± 0.105 / +0.195 ± 0.105) | coefficient d |

Notes on the facts:
- HI_i = CFG919's HI-bearing flag (gas inside r12 > 0).
- For F9 and F10 the prediction applies the same OLS design to E_pred,i.

**Conditional, no class weight (as CFG919):**
- **GC:** globulars carry no excess. Source: CFG820 L* ≥ 23.96 / 24.72 pc; CFG883 6 of 13 diagnostic globulars exclude a
  clump. Every cold-energy posit (P1–P4) is screened at r < L* (r_hl of globulars < 24 pc). Each posit's UNSCREENED
  prediction is reported to show what the screening must remove. P5 does not apply.

**Not graded, with reason:**
- No tide or host trend (CFG838 ρ −0.00; CFG839 +0.08; CFG843 +0.055 ± 0.117; CFG875 k −0.19 ± 0.15): no posit carries a host
  variable, so all are consistent by construction.
- No age trend (CFG827 slope +0.010 ± 0.012): no minimal form predicts age without SFH inputs (CFG923's domain).
- CFG920 chemistry: P3 is compatible by construction, because late binding is CFG920's escape. CFG923 tests the clock.
- CFG880's per-dwarf scatter (0.38 in ln σ_x): reported as a diagnostic (predicted vs observed residual scatter of the
  per-dwarf E).

## 6. Grading rule, trials factor, variants

**Per fact:** z_f = (pred − obs)/√(se_obs² + σ_pred²).

**Lenient-corner rule.**
- Each fact is evaluated at every bracket corner of section 3 that can affect it. When the dwarf gas σ_g changes, θ is
  re-calibrated.
- A fact counts as FAILED only if it fails at EVERY corner: min |z| ≥ 3, or the sign is wrong at every corner.
- SURVIVES is judged at the nominal corner.

**Sign wrong** (F1, F5, F6, F7, F8b, F9, F10) means all three hold:
- sign(pred) = −sign(obs);
- |obs| ≥ 2 se_obs;
- |pred| ≥ se_obs.

A near-zero prediction is judged by z, not by sign.

**F8a** counts as FAILED if p < 0.0027 (3σ two-sided equivalent) at every σ_g corner.

**Class per posit and footing:**
- **FAILS:** calibration impossible; or any graded fact FAILED as defined above.
- **SURVIVES:** at the nominal corner every graded fact has |z| < 2 and no sign is wrong; F8a p ≥ 0.05; and the joint χ² of the
  class-mean facts F1–F5 (5 dof) has p ≥ 0.05.
- **UNDERDETERMINED:** otherwise.

**Overall per posit:**
- FAILS only if FAILS on both footings; SURVIVES only if SURVIVES on both.
- Otherwise SPLIT BY FOOTING → UNDERDETERMINED, with both footings reported.

**Trials factor:** N_T = 5 candidates.
- Every FAIL is also tested at the Bonferroni threshold over N_T × 11 graded facts = 55 tests at two-sided p = 0.0027:
  z_TF = Φ⁻¹(1 − 0.0027/110) ≈ 4.06, computed exactly in the script.
- A FAIL is labelled "robust to the trials factor" if its decisive |z| ≥ z_TF (or a sign is wrong); otherwise "local".
- Any SURVIVES is labelled "best of 5 tried". Its fit is not evidence for it; its sealed prediction (section 8) is the test.

**Variants** (reported per footing). If V6 or V7 changes a posit's class on either footing, the posit is labelled FRAGILE; its
class is not changed.
- **V6:** floor 0.10 dex (CFG919 V6).
- **V7:** no +0.123 dex on the n > 2 lenses (CFG919 V7; the LS central mass proxy also drops the shift).

**VC** (cluster facts F5 and F6 withheld): reported as a CONDITIONAL class pending CFG922's baryon census. It does not
trigger FRAGILE and does not change the class.

## 7. Controls

Any K failure stops the lane: no class is reported (exit 2).

**K-tests:**
- **K1:** CFG919's input and cell code, exec'd read-only (writes refused), passes all of CFG919's own K-checks. CFG919 exec's
  CFG914, which carries its 9 checks.
- **K2:** CFG919 V0 cells reproduced exactly (cls, w, lg, E, f, n, se_stat to ≤ 1e-12), both footings.
- **K3:** CFG919 V0 class means (E, se, all 7 classes) and F1 (A, sA, χ²) reproduced to ≤ 1e-9 by this lane's own GLS, both
  footings.
- **K4:** quoted source numbers read from the source JSON/out files and matched to the precision quoted in section 5:
  - CFG687 A_MID and A_OUTER;
  - CFG829 blue window A;
  - CFG850 A_red, A_sph, A_disc;
  - CFG845 D and sD;
  - CFG820 L95;
  - CFG876 law-alone large-dwarf E;
  - CFG860 c0 and cG;
  - CFG920 median M_req and overall class.
- **K5 (solvers):**
  - with zero surplus (P1 c_* → ∞, P2 v_2 = 0, P3 v_w = 0, P4 1/Q_* = 0), every dwarf, lens, SPARC and cluster prediction
    is E = 0 to ≤ 1e-12;
  - P1's closed form agrees with an independent bisection of its self-consistency equation to ≤ 1e-9;
  - each self-consistent root satisfies its equation to ≤ 1e-10.
- **K6:** per-dwarf inputs. w equals CFG919's f_sph exactly; σ_law² equals r12·g_L/3 to ≤ 1e-9.
- **K7 (P5 numerics):**
  - (a) Newtonian midplane g_R of the thin exponential disc vs Freeman's analytic I0K0 − I1K1 formula, ≤ 1e-3 relative on
    R/R_d ∈ [0.5, 8];
  - (b) Hankel volume-integral midplane field of a Plummer sphere vs GM(<r)/r², ≤ 1e-2;
  - (c) QUMOND midplane field of the Plummer sphere (same phantom code path) vs the algebraic ν g_N, ≤ 2e-2.
- **K8:** interpolated calibration (used only by INJECT) agrees with the exact brentq θ to ≤ 1e-3 in every predicted class
  mean.

**MUTATE run, sign** (CFG921_MUTATE=sign → cfg921_MUTATE_sign.out / cfg921_results_MUTATE_sign.json; exit 1 = bites):
- M1a: P1–P4 with the surplus sign reversed (ρ_x → −ρ_x, s → −s, L → 1/L). The calibration must be impossible, so FAILS, on
  both footings.
- M1b: each of P1–P4's nominal predictions sign-flipped (E_pred → −E_pred) at its calibrated θ and graded. Must be FAILS on
  both footings.
- Bites only if all 16 cases FAIL.

**MUTATE run, inject** (CFG921_MUTATE=inject → cfg921_MUTATE_inject.out / cfg921_results_MUTATE_inject.json; exit 0 =
recovered):
- For each posit P1–P5 and footing, 200 realizations (rng 921) of synthetic data generated from that posit's nominal
  predictions:
  - DW cells and other classes' cells ~ N(pred, block covariance + floor²);
  - per-dwarf E_i ~ N(E_pred,i, sE_i² + τ²), with τ² = max(0, var(OLS residual) − mean sE²) from the observed F9 fit.
- The full grading (re-calibration included) is run on each realization.
- Required for every posit and footing: FAILS ≤ 10% and SURVIVES ≥ 40%.

## 8. Sealed prediction (for survivors)

For any posit that SURVIVES on a footing:
- A file SEALED_PREDICTION_<posit>.md is written after the main run and committed alone, before any data of the target class
  is opened by this lane.
- Target classes, untested here:
  - (i) early-type galaxies with stellar dynamics (ATLAS3D JAM is on disk, unread by this lane);
  - (ii) ultra-diffuse galaxies;
  - (iii) tidal dwarf galaxies.
- The prediction is a formula in baryonic inputs with the calibrated θ, plus numbers for declared representative inputs. It
  reads no object data.

If no posit survives, no sealed prediction is written, and the README says so.

## 9. Compute and hygiene

- One core (OMP_NUM_THREADS=1, nice -n 10), < 1 GB, one process at a time. No PDE solver: P5 uses quadrature on a fixed grid.
  Nothing downloaded.
- No other lane's files are edited: CFG919/914/880/883/687 code is exec'd read-only; the other lanes' JSON/out files are read.
- Outputs: cfg921.py → cfg921.out, cfg921_results.json; MUTATE outputs named by mode.
- Commits use explicit paths only.
