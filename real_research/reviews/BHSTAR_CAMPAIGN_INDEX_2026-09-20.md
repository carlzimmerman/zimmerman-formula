# THE BH* CAMPAIGN — SESSION INDEX (2026-09-19/20)

Master pointer for the arXiv:2609.09274 absorption campaign ("black hole stars" =
LRDs). Everything below is committed and pushed. Full narrative:
`real_research/reviews/black_hole_stars_2609.09274_REVIEW_2026-09-19.md` (SS1-23).

## THE VERDICTS (standing after the referee pass)

1. **The paper absorbed and reproduced** (18/18): LRDs = accreting BHs in optically
   thick envelopes; engines 10^3.4-4.3 Msun (Gamma-free); the overmassive-BH talking
   point is dead; our record never carried it.
2. **The dial is dead (Wave U, THE BREAKTHROUGH)**: Gamma = kappa_es sigma T_eff^4 /
   (c g_phot) — the Eddington factor is an OUTPUT of the line-wing fit (Lean I12,
   the third M-cancellation theorem). Measured: Gamma = 56.6 at the stack — 13%
   ABOVE the assumed cap of 50. The chain Gamma -> M -> r_B -> test has ZERO dials.
3. **The quartic constant from first principles (Wave Q)**: (1-beta)/beta^4 =
   (M/M_E)^2 with M_E = sqrt(48 k^4 u^2/(a mu^4 m_p^4 pi G^3)) = 51.8 Msun
   (u = the Lane-Emden n=3 moment 2.01824, RK4-integrated) — zero fitted anchors;
   confirms the calibration to 3.8%.
4. **The double ceiling (Waves N/Q)**: global (equilibrium, homologous)
   [5.09e7, 1.21e8] Msun; pulsational (accreting MESA, absorbed) 1e5-6; LF cutoff
   1e5.7 — three independent scales, 1.7-3.1 dex apart. LRD engines sit below all.
5. **The regime coincidence: CONSISTENT-OPEN** (Waves K/P/R/S): g_B/a0(rho_B) = 1.00
   at the Balmer layer as a CONDITIONAL prediction r_B = r* = 100 au sqrt(M/1e4)
   (1e10/n)^{1/4} (exact identity, Lean I07); the U-route disfavoring VOIDED by the
   recombination pin's own opacity (tau_ion/tau_es >= 1e3 even at 0.01% neutral,
   Lean I10); the wind kinematics bracket r* (r_launch = 72 au no-CAK, 490-652 au
   CAK; the in-situ CAK factor 3.6 measured).
6. **Honest kills on the record**: the kappa-suppression hypothesis (L1, the
   Chandrasekhar K-table), the envelope-stabilization hypothesis (L2, the pressure
   census), the gas-virial thermodynamics (M1, superseded by the quartic), the
   first draft's 50-yr variability claim (R1, the photosphere samples it).

## THE KEPLER-GRADE PREDICTIONS (Wave T, 4/4 — zero free parameters)

- **KP1**: r_B^4 n_H c^2 mu m_p = 4 G M^2 (Lean I11). Two observables + one
  Gamma-free mass; one law, every LRD, one constant (5.01e68 m at 1e4 Msun).
  Falsifier: any object off by > x2 in radius.
- **KP2**: v_inf ∝ M^{1/4} — spread exactly 10^0.225 = 1.68 across the published
  band; a classic M^{1/2} scaling (x4.5) kills the recombination-pinned family.
- **KP3**: T_eff follows the Saha curve in n_H (5572 K at 1e9 -> 7236 K at 1e12).
- **KP4**: no equilibrium SMS above 1.21e8 Msun; accreting ones die at 1e5-6.

## THE LEAN CERTIFICATES (I01-I12, 33 theorems, zero sorry, axioms
{propext, Classical.choice, Quot.sound}, all parent-verified)

I01 boost/xpr/eddington_a0_closure/gap envelope/a0blind (10) · I02 ceiling S5 (3) ·
I03 regime_invariant (1) · I04 K-table absorption (2) · I05 quartic two-sided beta
band (2) · I06 ceiling bracket stable_band/unstable_band (2) · I07 the conditional
identity + tolerance (3) · I08 quartic_constant first-principles (1) · I09 kinematic
identities (2) · I10 void_theorem (1) · I11 kepler_law KP1 (1) · I12 the dial
readout (2).

## THE LANES (17, 121+ checks, all PASS after in-lane fixes)

black_hole_stars_2609.09274_check 18/18 · bhstar_g1 9/9 · g2 13/13 · h1 6/6 ·
h2 5/5 · j1 7/7 · k1 5/5 · l1 5/5 (the K-table kill) · l2 4/4 (the census kill) ·
m1 6/6 (the quartic) · n1 5/5 (the bracket) · p1 8/8 (the empirical audit) ·
q1 5/5 (first principles) · r1 6/6 (the wind kinematics) · s1 4/4 (the void) ·
t1 4/4 (the predictions) · u1 4/4 (the dial).

Plus the CFJC paper: real_research/papers/CFJC_RFC0001_bhstar_regime_coincidence.md.

## THE OPEN ITEMS (the next session's work)

0. **I13 — algebra certified; variational comparison derived (2026-09-22
   correction)**: the Gamma_1 kernel identities and scalar crossing remain
   Lean-certified. The defined `omega2` is not generally the fundamental
   eigenvalue. The Newtonian homologous trial quotient is `3 W_beta/J`,
   `J = integral rho r^4 dr`, so I13's inertia convention must be `I=J/3`.
   The exact GR work form now supplies an upper bound on the fundamental
   eigenvalue, and a positive-comparison-function identity supplies a lower
   bound when its endpoint conditions hold. Negative trial work certifies
   instability; positive trial work alone does not certify stability.
   The leading PN structural integral independently reproduces the n=3
   coefficient `1.124474311979` in the `Gamma_1-4/3` convention, or
   `C_gr=3.373422935937` in I13's `3 Gamma_1-4` convention. This replaces the
   unsupported `[2.25,3.35]` band; for uniform density the latter coefficient
   is instead `19/14`. These numerical evaluations are not interval proofs.
   Derivation, benchmarks, and precise scope:
   [I13 operator comparison](spectral_spine_closure_2026_09_22/i13/REPORT.md).
1. **MESA — actual equilibrium sequence and radial spectrum remain open**:
   require authenticated `r,m,rho,P,Gamma_1` profiles, density/internal-energy
   convention, and inner/outer mechanical conditions. A BH envelope must not
   silently use a regular stellar center. Evaluate the exact GR form or
   control the PN remainder, then solve/bracket the lowest radial mode along
   the sequence. The physical mass ceiling and its proposed luminosity-cutoff
   identification are not established by the scalar crossing alone.
2. **Reverberation/lensing**: the direct r_B on the z=7.04 lensed LRD closes KP1 in
   one object (the paper's own program).
3. **Per-object KP2/KP3**: the 117-LRD P-Cygni terminal velocities + the CLOUDY
   (n_H, T) pairs against the quarter-power law and the Saha curve.
4. **The referee finding R-F3**: the Gamma distribution [36, 90] measured per object
   from the existing log g fits — the dial's true range.

## THE CONVENTIONS THAT HELD

Append-only corrections (sec 21's correction of the premature clean claim) ·
re-derive, never silently retcon (M1's re-anchor, R1's re-frame) · the parent reads
the axiom output before claiming clean · in-lane unit traps: KPC e16/e19, erg/W,
Eddington-W/erg (7 dex), cm/m, 1e10.5 literals, the n=2.5/n=3 Lane-Emden column,
the auto-bound pi (open Real!), the cgs Saha constant 2.4e15.

## 2026-09-22 AUDIT + DOOR SWING (append-only; full record: `real_research/bhstar_audit_2026/BHSTAR_AUDIT_AND_DOOR_SWING_2026-09-22.md`)

- **Verdict 5 (regime coincidence) is DEMOTED, not killed:** it is not a framework result.
  - L323 9/9; Lean I17.
  - a0 is evaluated at the gas's own density; the framework's law is flat, and the local-density
    branch is SPARC-excluded as a law.
  - The ratio is exactly 2(v_c/c)(t_ff/t_dyn).
  - A unique crossing is guaranteed in every ρ ∝ r^−p envelope with p < 4.
  - P(chance within ×2 of the Balmer layer) = 0.31, and the honest error bar is ±0.47 dex, not ±0.02.
  - The same classifier labels the Earth's surface air "strong-a0".
  - KP1 ⟺ its own definition; KP2's M^{1/4} comes from the published family alone.
  - The framework's own BH* prediction is a NULL: every layer sits at ≥ 5.6e5 a0.
- **Verdict 2 ("the dial is dead / Γ = 56.6") is corrected.**
  - Γ = 48.1 at κ_es = 0.34, below the cap.
  - The cap sits inside log g ± 0.2.
  - Stacks span Γ 30–123 and the one per-object fit (the Egg) gives 226, so [36, 90] is too narrow (L325).
- **Lean I01–I13 docstring corrections** (I10 947 < 1e3; I05/m1 "500×" → 5×10⁵; I01 R_crit
  inversion; I02 direction; I04 vacuous `kappa_min_tabulated`; I11 κ = ½ enters, so it is not
  parameter-free; I12 κ_es unstated) are listed in the audit record §3.
- **Open items:**
  - Item 2 (reverberation): still shut. No firm LRD lag exists anywhere. Ji+25's 45 ld is
    ≈ 34 ld from its own stated arithmetic.
  - Item 3: KP2 undecided (slope 0.32 ± 0.12, N = 11), the ×1.68 clustering clause fails
    (×7.8), and KP3 cannot run (no per-object n_H).
  - Item 1 (MESA): profiles are on request only.
- **NEW live framework test: A2744-QSO1, the naked BH at z = 7.04** (L324 6/6; Lean I18).
  - The RAR phantom fraction is exactly e^{−r_M/r}, so "extended mass sub-dominant at r" is
    equivalent to a0 < GM/(r ln 2)².
  - The flat framework passes.
  - The a0 ∝ H(z) rival is disfavoured at 0.9–2.0σ on the headline mass: a HINT only, and
    ΛCDM is not discriminated.
  - Registered: v_c/v_Kepler at 375 pc is 1.15–1.93 for the framework, 1.00 for Newton and
    1.94–3.45 for the rival.
- **CORRECTION (same day) to the QSO1 entry above:** L324 now uses the PUBLISHED Nature numbers
  (PMC13215880), which supersede arXiv v1: spectroastrometric i-corrected mass 6.9–7.2, and 1-D
  bins at 100 and 150 pc.
  - At the low end (10^6.9) the flat framework **FAILS** the sub-dominance bound at 200 pc on both
    footings and at 150 pc on the alt footing (Lean I18 `framework_fails_200_low`,
    `alt_fails_150_low`).
  - At the MOKA3D 10^7.7 it passes.
  - The rival fails at every reading.
  - The verdict is two-sided and mass-reading-limited.
  - Data are public (Zenodo 19402518), so a joint (M, i, law) MOKA3D refit is the decisive swing.
  - The registered 375 pc bands widen with the lower published masses: framework 1.15–2.24,
    Newton 1.00, rival 1.94–4.08. They overlap across the full mass range, so the refit must
    weigh M jointly (at fixed M the rival sits ≥ 1.5× above the framework).
