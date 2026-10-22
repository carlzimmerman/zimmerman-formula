# D6_u_mechanism FROZEN CRITERIA (written and committed alone, before any script or number of this lane)

Door: the u(r) retained/sourcing-fraction mechanism (P4 of `deepseek_push/DS_FINAL_2026_10_21/THEORY.md`;
register door 2 in `deepseek_push/CANDIDATE_LAWS_REGISTER.md`). Date 2026-10-22.

Settings: κ = ½ FITTED. Footings a0 = 9.3603e-11 (canonical) and 1.1312e-10 (alt) m s⁻², read from
`campaign_fresh_gravity/CFG4_common.py`; reported separately, never pooled. Cold energy, no particle. Not
"theory closed". Nothing here may say the data favour the framework over ΛCDM.

Not blind (disclosed): the record's u numbers (A21, A29, A41: u_MID = 0.4716 ± 0.0362, 8-bin u, step fit,
r_sp = 1.3674 r200c) and CFG959's f_P rule were read before this freeze. No number of this lane exists yet.

## Definitions (fixed now)

- **u_P4** (THEORY P4, A21 eq. 5, A29 eq. 1): the law's phantom share of the observed excess over baryons,
  `u = (P_l − P_N)/(D − P_N)` (ΔΣ or mass), i.e. local reading ρ_cold = ρ_ph/u (A41 model3d).
- **u_959** (CFG959 FROZEN §2): the UNRELAXED (retained, not settled) fraction, `u_959 = f_P = 3σ²/(v²+3σ²)`;
  CFG959's mass-conserving reading sources the law with the settled share (1 − u_959). Hence the mapping
  **u_P4 = 1 − f_P** (primary; ignoring the supply cap, which only lowers it). The identity mapping
  u_P4 = f_P is reported only.

## Q1 — does CFG959's f_P give u ≈ 0.47 inside splashback, and the scaling?

- Input: the cluster f_P that CFG959 actually used (read from its frozen table / script; record value), and the
  v/σ that u_P4 = 0.4716 would require (algebra).
- **T1 MATCH** iff |u_P4(cluster) − 0.4716| ≤ 2 × 0.0362 under the primary mapping. Otherwise NO MATCH, reported
  with the distance in σ and the v/σ needed.
- **T1s scaling.** Compute d ln u/d ln M_v of (a) f_P for dispersion-supported systems and (b) the record's
  u_catch = R_tot f_ret/R_cosmic (A21 eq. 12) at fixed f_ret in the deep limit y_v → 0. A21 eq. (12) states
  +1/6. **RECORD ERROR** iff the computed deep-limit slope at fixed f_ret is −1/6 within 0.01.
- Circularity: stated from the inputs (f_P uses kinematics, not the shear amplitudes).

## Q2 — a stream-counting mechanism with zero fitted constants

"Derived" means: u(x), x = r/r_sp, is computed from the self-similar spherical collisionless secondary-infall
solution in an Einstein–de Sitter background (Bertschinger 1985; Fillmore & Goldreich 1984; radial orbits),
solved self-consistently by iteration in this lane, with (i) the accretion index ε taken from a DECLARED bracket,
not fitted: ε = 1 (Bertschinger point seed, Γ = dlnM/dlna = 1), ε = 1/2 (Γ = 2), ε = 1/3 (Γ = 3); (ii) r_sp the
solution's own outermost caustic, mapped to each cluster by the record's r_sp,i = 1.3674 r200c,i (A41). Nothing
is adjusted to the u data.

Two hypotheses, both u = 1 outside r_sp (single stream), u = 1 beyond the solution's turnaround radius:
- **H-1S** (single stream sources): only cold matter that has never passed pericentre (first infall) sources the
  phantom. u_3D(x) = ρ_first-infall/ρ_total.
- **H-VR** (inflow sources; the "≈ ½ from phase mixing" candidate): only cold matter with v_r < 0 sources.
  u_3D(x) = ρ(v_r<0)/ρ_total inside r_sp.

Model per cluster: ρ_cold = ρ_ph/u_3D(r/r_sp,i) (A41's local reading), baryons and phantom from CFG687's own
law model (β = 2/3, r_c = 0.15 R500, f_* = 0.20, kernel ν_mono), projected to the 8 CFG687 bins and stacked with
CFG687's weights. Scored against the CFG687 per-cluster stack (318 eRASS1 × KiDS, `cfg687_percluster.npz`).

- **T2a (band):** predicted u_MID within 2 × 0.0362 of 0.4716.
- **T2b (profile):** 8-bin χ² of D against the zero-parameter model with the 30-patch jackknife covariance
  (eigenvalues clipped at 1e-2 of the largest, A41's convention), p ≥ 0.01 for 8 dof.
- A hypothesis **PASSES at an ε** iff T2a and T2b both pass. Class: **DERIVED-MATCH** if it passes at all three ε;
  **CONDITIONAL(ε)** if at some; **FAILS** if at none. Both footings scored; the class must hold on both.
- **Second prediction P2m (mass):** the same model's u_MID in the three CFG687 gas-mass terciles vs the data's
  tercile u_MID (jackknife σ). PASS iff all three within 2σ.
- **Second prediction P2g (galaxy scale):** the same u_3D(x) evaluated at the galaxy-lensing radii of Q3a
  (x = R/r_sp,gal) vs the measured u_gal of Q3a. PASS iff within 2σ in the primary range.

## Q3 — an independent u measurement without the cluster shear amplitudes

- **Q3a KiDS-1000 isolated galaxy lensing** (Brouwer+21 Fig. 3, 4 stellar-mass bins, full covariance, on disk in
  `real_research/data/lensing_rar/brouwer2021_rar/`). Point-mass baryons + the law's phantom (ν_mono), CFG801's
  zero-knob log M* = 10.14 / 10.46 / 10.70 / 10.89 (provisional, record) as M_b. Since u rises with M_b, M_b = M*
  gives the **minimum** u_gal (any real gas adds to M_b and raises u). u_gal = Σ(P_l − P_N)/Σ(D − P_N) with
  inverse-variance weights over the primary range R ≤ min(0.31 Mpc, r_sp,gal), r_sp,gal = 0.83 r200m of the law
  profile (same convention as the clusters). σ from the covariance (linear propagation).
  **T3a:** "u ≈ 0.47 inside splashback" is EXCLUDED at galaxy scale iff u_gal,min − 0.4716 > 3σ on both footings.
  Also reported: the Δlog M_b that would bring u_gal down to 0.4716.
- **Q3b X-COP hydrostatic** (12 clusters, on disk in `real_research/data/xcop/`): u_X(r) = M_ph/(M_HSE/(1−b) − M_b)
  at 0.3–1.0 R500 (inside r_sp), b = 0 and b = 0.3 bracket (CFG432's). Cluster median and bootstrap σ.
  **T3b:** consistent with 0.4716 iff within 2σ (reported per b and footing).
- **De-circularisation:** possible NOW iff Q3b gives a shear-independent cluster u with σ ≤ 0.10 at both b ends
  agreeing with each other within 2σ; otherwise say what is missing.

## Verdict mapping

- CRISP FINDING: any T-line outcome that is decisive (a ≥ 3σ exclusion, a DERIVED-MATCH, or a confirmed RECORD
  ERROR) with the number in `d6_u_mechanism_results.json`.
- Otherwise RUNNABLE NOW / DATA-GATED / SCOPED NO-GO / NOTHING NEW as the brief defines.

## Checks (K-lines; correctness, independent of outcome) and MUTATE

K1 law model reproduces the npz PL; K2 A21 u_MID = 0.4716 reproduced from the npz; K3 self-similar ε = 1 interior
mass slope d ln M/d ln λ = 3/4 ± 0.05 (Bertschinger's known result); K4 M(λ=1) = 1 normalisation; K5 KiDS data
load matches CFG801's v_circ; K6 the deep-limit slope is computed symbolically and numerically and agree.
`--mutate`: drop the baryon subtraction in the inversion (u = P_l/(D − P_N)); must break K2. Outputs
`*_MUTATE.out`, `*_results_MUTATE.json`. OMP_NUM_THREADS=1, nice, single thread, minutes.

## AMENDMENT A1 (2026-10-22; after prototyping the solver and the data loaders, BEFORE any frozen T-line was scored)

Seen before this amendment: the ε = 1 and ε = 1/2 u_3D tables (u_VR ≈ 0.50 inside r_sp; u_1S ≈ 0.03–0.3), the ε = 1
caustic λ_sp = 0.361 and interior slope ≈ 0.63 at λ 0.01–0.03; prototype numbers for the galaxy u (≈ 0.6–0.7 at M_b = M*)
and X-COP u (≈ 0.34 at b = 0). None of the frozen pass lines was evaluated. Changes, none of which touches a pass line:
1. Numerical: τ_max scales with ε so every ε resolves the same λ floor, τ_max = 300^{(8/9)/α} (ε = 1/3 at τ_max = 300 needs
   ~33 000 pericentre passages per iteration, hours). Settings listed in `SS_PAR`.
2. K3 is evaluated over λ = 0.01–0.03 as coded. The prototype gives 0.63, so K3 is expected to FAIL: the iterated solution
   has not reached the asymptotic 3/4 at the resolved radii (a τ_max = 3000 test was started and stopped for compute).
   Added **K3b**: Bertschinger's ε = 1 outermost caustic r_sp/r_ta = 0.364 ± 0.01 (published value) as the solver check.
3. Added a POST-HOC, reported-only diagnostic: X-COP u evaluated at the shear bands' own x = r/r_sp (INNER, MID).
   It carries no verdict weight.
