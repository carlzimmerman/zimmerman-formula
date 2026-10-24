# X16_beta_binary_radiation: with C1 inside its window, how much does the khronon's scalar radiation change the binary-pulsar orbital decay, and does it stay inside the observed Ṗ_b agreement with GR? FROZEN CRITERIA

Written and committed (with `ASSUMPTION_LEDGER.md` and `LITERATURE_MAP.md`) before any lane script exists and before any
number is computed by code. Rules: `rebuild_2026_10_22/BRIEF.md`, `doors_push_2026_10_22/BRIEF.md`. κ = ½ is FITTED.
Footings canonical a₀ = 9.3603e-11 m/s² and alt a₀ = 1.1312e-10 m/s², never pooled. No dark-matter particle. Never "theory
closed"; nothing here says the data favour the framework. Theory-consistency lane; the only data are published binary-pulsar
timing summaries already transcribed in the record. Small jobs only: `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15`,
< 1 GB RSS, minutes; `compute_queue/` and every other lane untouched (record scripts are run only as byte-identical copies
inside this lane's directory, outputs kept here); no downloads.

Launched from X15's "What this does not show": C1 turns the khronon into a propagating, superluminal, dispersive scalar
(ω² ∝ k⁴ on the stiff side) and "binary-pulsar scalar radiation from this mode was not computed"; C8 K7's "no radiative
channel" holds only at β = 0.

## 0. What was read, and the not-blind statement

Read before freezing: X15 (README, FROZEN_CRITERIA, ASSUMPTION_LEDGER, LITERATURE_MAP, the whole script
`x15_c1_preferred_frame.py`, its `.out`); X14 README (C1 rows, window); `covariant_push_2026_10_22/V3_FULL_PICTURE.md` §1–3,
`THEORY_V3_DRAFT.md` §0–1; C8 README and its K7 code (`c8_instantaneous.py` L433–461, JSON K7 block); P3 README (double
pulsar rows); I1 README head (tilted-slice Hadamard result); C5 README causality lines; CFG291 (README, FROZEN_CRITERIA,
script L85–240: Barausse 2019 transcription, pulsar table, Peters–Mathews); the pulsar ledger
`real_research/reviews/mi_pulsar_pta_precision_ledger_2026.py` L160–200; `real_research/reviews/
mi_sign_from_perturbation_drift_2026.py` L55–75 (B1913+16 masses). One PROVISIONAL web look-up (LITERATURE_MAP L1: Yagi,
Blas, Barausse & Yunes 2014, the flux coefficients).

**Not blind.** Before freezing I reasoned on paper (no script, no code-computed number):
- Eliminating P, n and the longitudinal shift from X15's linear system gives one scalar ψ with kinetic coefficient
  Z_ψ = (2 + 3β)/(Kβ) and a source Σ = T + (2/η)ρ − ωJ/(Bk), B = β/(2 + 3β); on shell and for a conserved source Σ = T + ρ.
  So the scalar couples to the trace of the stress (monopole), to ρ's quadrupole only through k² (suppressed by 1/c_S⁴),
  and, in the binary's momentum frame, to the sensitivity mass dipole through 2/η ≈ c_S²/B (enhanced).
- Expected: v3s + C1's scalar flux equals Yagi et al.'s khronometric flux (Eqs. 121–124) at α = η(k_S), β_BPS = 0,
  λ = β, c_s = ω/k_S, times 2/n_g (n_g = d ln ω²/d ln k → 4 on the stiff side). With the constant-α control the match
  should be exact, including the dipole if the momentum frame is used (the Σm v = 0 frame gives an extra
  (1 + B/c_S²)⁻² = (2 − α)²/4).
- Rough sizes: k_S ~ 1e-13 m⁻¹ (λ_S ~ 400 AU), c_S ~ 20–50 c, η(k_S) ~ 1e-9; monopole δ ≲ 1e-11 (B1913+16), quadrupole
  ≲ 1e-16; dipole coefficient ~1e4, so the double pulsar would need |s₁ − s₂| ≳ 7e-7 (J1738+0333 ~1e-5) to notice.
  Weak-field sensitivities with this lane's α(k = 1/R_NS) are ~1e-27; the P-hedgehog self-energy envelope is ~3e-15. A
  counterfactual s ~ β|Ω/m| would sit near the double-pulsar threshold.
These expectations shaped which quantities §3–§6 compute. Thresholds are published bounds or structural margins (factor
1e3 validity margins, exact residuals), not tuned to them.

## 1. Definitions

- **v3s** (V3_FULL_PICTURE §1; THEORY_V3_DRAFT §0–1) and **C1** (X14: −βK²/(4K) on the khronon leaves, Hořava λ = 1 + β;
  B = β/(2 + 3β)), as in X15 FROZEN §1. K ≡ 4πG, c = 1 in the symbolic part.
- **Linear system (step 1).** X15's quadratic unitary-gauge Lagrangian (function `lagrangian`, copied with provenance),
  fields n, ψ, N1, N3, P1, P3, k along z, with the source generalised from X15's moving point mass to a general conserved
  or non-conserved source: L_src = −ρn − Tψ + J_xN1 + J_zN3 (ρ = T⁰⁰, T = T^ii, J_i = T⁰ⁱ, Fourier amplitudes). Plus the
  tensor sector L_T = (1/16K)[ḣ_ijḣ_ij − ∂_zh_ij∂_zh_ij] + ½h_ijT^ij (h_ij = h₊e⁺ + h_×e^×), to which C1 adds
  −(1 + β)K²/(4K) with K = ½ḣ_ii = 0.
- **Screened radiation zone.** Θ = 1 (D·P > 0: the binary's hedgehog m/(2πL★²r) and the Galactic phantom), M ∈ {1, 100}
  (1 = bare screened; 100 = ILLUSTRATIVE upper value of the Galactic background's (1 + x)², x ≤ 9, treated as isotropic).
  μ_K term and khronon charge transport dropped in the radiation system; their sizes are checked (P-LIN).
- **Power formula** (derived in-lane from dE_field/dt = ⟨∫J·Φ̇⟩). For a source Re[S e^{−iωt}] coupled as +S·Φ, with
  𝒟(ω, k) the plane-wave Euler–Lagrange matrix (EL = 𝒟A + S) and 𝒢 = −𝒟⁻¹(ω + i0):
  P(ω) = (ω/2)∫d³k/(2π)³ S†[(𝒢 − 𝒢†)/2i]S. At a simple pole ω² = ω_S²(k):
  **P = (πω/2)∫d³k/(2π)³ S†R S δ(ω² − ω_S²(k))**, R = lim_{ω²→ω_S²}(ω_S² − ω²)(−𝒟⁻¹);
  n_g ≡ d ln ω_S²/d ln k at k_S, so ∫d³k δ(ω² − ω_S²) f = (k_S³/(n_gω²))∫dΩ f.
- **Binary source** (leading order in k a; CM **momentum** frame, Σm_a(1 + s_a)v_a = 0):
  ρ̃ = −ik·D − ½k_ik_jI_ij, J_z = (ω/k)(−½k_ik_jI_ij) (the s = 0 part is conserved; J(k⁰) = 0), T̃ = −½ω²I_kk,
  I_ij = μ r_ir_j, D = Σm_ax_a with Ḋ = −Σm_as_av_a = −μ(s₁ − s₂)v. Sensitivity s_A = −d ln m_A/d ln γ (Yagi/Foster).
  The sensitivity-weighted quadrupole terms (Yagi 𝒜₂, 𝒜₃, ℬ₂, ℬ₃) are bounded with the literature coefficients mapped as
  in §4 X-LIT (reported, included in δ as an upper bound).
- **Harmonics.** Kepler orbit sampled at N = 8192 points uniform in mean anomaly (Newton solve of E − e sin E = M), FFT;
  X(t) = X₀ + Σ_{n≥1} Re[X_n e^{−inΩt}], n = 1 … 400, ω_n = nΩ. Per-harmonic powers use k_S(ω_n), c_S(ω_n) = ω_n/k_S,
  η(k_S), n_g at that harmonic.
- **δ** ≡ Ṗ_b(scalar)/Ṗ_b(GR) = P_S/P_GR (Ṗ_b/P_b = −(3/2)Ė_b/E_b; the conservative orbit change is ε = (a/L★)² ~ 1e-18,
  C8 K7). P_GR is the same machinery's tensor flux. ΔṖ_b = δ × Ṗ_b,GR is reported.

## 2. Binaries and bounds (record transcriptions only; no new data)

δ⁺ = the 2σ upper edge of the allowed δ (healthy scalar radiation adds energy loss, δ > 0; sign checked by D-RES), the
strictest of the record's transcriptions.

| system | inputs used (m₁, m₂ [M☉], P_b [d], e) | record Ṗ_b(GR) used in S0-5 | agreement (record) | δ⁺ used | source lines |
|---|---|---|---|---|---|
| J0737−3039A/B | 1.338185, 1.248868, 0.1022515592973, 0.087777023 | −1.247920e-12 | Ṗ_obs/Ṗ_GR = 0.999963(63) | (0.999963 − 1) + 2(6.3e-5) = **8.9e-5** (CFG291's 95 % 1.3e-4 is looser) | ledger L181–183; C8 L436–437; masses CFG291 L97 / mi_sign L66 |
| B1913+16 | 1.4398, 1.3886, 0.322997448918, 0.6171340 | −2.402531e-12 | 0.9983(16) | −0.0017 + 2(0.0016) = **1.5e-3** | ledger L184–186; C8 L438–439; inputs mi_sign L62–64 |
| J1738+0333 | 1.46, 0.181, 0.3547907398724, 3.4e-7 | −27.7e-15 (+1.5/−1.9) | Ṗ_int = −25.9(32)e-15 | (25.9 + 2·3.2)/27.7 − 1 = **0.1661** (CFG291's 0.188 is looser) | ledger L187–189; C8 L440–441; CFG291 L91–93 |
| J0348+0432 | 2.01, 0.172, 0.102424062722, 2.0e-6 | −0.258e-12 (+0.008/−0.011) | 1.05 ± 0.18 | 1.05 + 2(0.18) − 1 = **0.41** | CFG291 L94–96 (FROZEN §4) |

1σ precisions (reported as δ/σ): 6.3e-5, 1.6e-3, 3.2/27.7, 0.18. Paths: ledger = `real_research/reviews/
mi_pulsar_pta_precision_ledger_2026.py`; mi_sign = `real_research/reviews/mi_sign_from_perturbation_drift_2026.py`; C8 =
`covariant_push_2026_10_22/C8_instantaneous/c8_instantaneous.py`; CFG291 = `campaign_fresh_gravity/
CFG291_khronon_binary_pulsar/cfg291_khronon_binary_pulsar.py`. Constants: GM☉ = 1.32712440018e20 m³/s², T☉ = GM☉/c³.

## 3. Step 0: reproductions (stop rule: any failure → verdict UNDECIDED, nothing further is scored)

Record files and their sha256 (as committed): X15 script 2bf28103…f9e1, X15 JSON dd864fc9…8e5e; X14 script 32fd2a12…5012,
X14 JSON 5af0afb8…f96a; C8 script d8f78c26…1ae2, C8 JSON 1d7bc58b…b7d7; ledger f1688d81…dbff; P3 JSON 30eaf641…db14.

- **S0-1 (X15's own code).** A byte-identical copy of X15's script (sha checked) is run in this lane's directory (its
  outputs, incl. A22's redirected JSON, are moved to `step0_reruns/`): exit 0, 13/13 PASS, verdict "C1 SURVIVES PPN"; the
  rerun's S0_3 ω² root strings (Θ = 1, 0), D.alpha1_k, D.alpha2_k identical to X15's committed JSON; surviving_windows equal
  to 1e-12 relative.
- **S0-2 (X14's own code).** A byte-identical copy of X14's script is run in `step0_reruns/x14/`: exit 0, 24/24; its C1
  FT_window β_min (both footings) and β_max (μ_K = 0.1, 0.03) equal X14's committed JSON to 1e-12 relative; this lane's
  recomputation from X14's formulas (copied from X15 S0-2) equals them to 1e-12. The window used downstream is the rerun's.
- **S0-3 (this lane's system ↔ X3/X14/X15).** The scalar block's determinant has exactly one ω² root, equal to
  βk²(M − 1 + ΘL★²k²/2)/(2 + 3β) (residual 0; Θ = 1 and 0) and to X15's S0_3 root strings; the tensor block gives ω² = k²
  with C1 present (c_T = 1).
- **S0-4 (the record's double-pulsar GR-agreement number, C8's own code).** A byte-identical copy of C8's script is run in
  `step0_reruns/c8/`: exit 0, K7 PASS; its K7 block (a_m, eps, eps_over_precision, nonlinear, all three systems, all L★)
  equals C8's committed JSON to 1e-12 relative and worst_ratio = 3.219e-14 (to 1e-3). The PSR dicts parsed by AST (no
  execution) from the ledger and from C8's script agree on P_b, M_tot and the precision for J0737/B1913/J1738, and the
  J0737 source string contains "0.999963(63)". This lane's own K7 recomputation (C8's formula, this lane's inputs)
  reproduces C8's JSON eps to 1e-9 relative.
- **S0-5 (Peters–Mathews from this lane's inputs).** GR Ṗ_b = −(192π/5)(2π/P_b)^{5/3}T☉^{5/3}m₁m₂m^{−1/3}f(e) within 1e-3 of
  the record's value for J0737 and B1913, and within 1e-2 of (and inside the quoted interval of) J1738's and J0348's.
- Reported only: P3's `double_pulsar_mixing_eps_max` (read from its JSON, not rerun).

## 4. Step 1: derivation (sympy, PYTHONHASHSEED=0) — required checks

- **D-HERM.** 𝒟(ω, k) of the six-field system is Hermitian (residual 0); after eliminating P3 the (n, ψ, N3) block is
  real symmetric; the vector block (N1, P1) has no ω-dependent zero.
- **D-GR (normalisation control).** The tensor sector through the power formula gives P_GR = (G/10)ω⁶|Q|² per harmonic
  (Q = STF part of I, residual 0), i.e. (G/5)⟨Q⃛Q⃛⟩.
- **D-RES.** At the scalar pole the residue matrix is rank 1, S†RS ≥ 0 for β > 0 (positive radiated energy), and
  S†RS = KB|Σ|², Σ ≡ T + (2/η)ρ − ωJ_z/(Bk), η = 2/(M + ΘL★²k²/2) (residual 0).
- **D-ON.** For J_z = (ω/k)ρ on shell, Σ = T + ρ (residual 0).
- **D-FORM.** With the isotropic angular identities (checked numerically by quadrature to 1e-12, check ANG), per harmonic:
  P_quad = (GB/(30n_g))ω⁶|Q|²/c_S⁷; P_mono = (GB/(4n_g))Z²ω⁶|I_kk|²/c_S³, Z = 1 + 1/(3c_S²);
  P_dip = (G/(3n_gB))(1 + B/c_S²)²ω⁴|D|²/c_S (residual 0); n_g = 2 + L★²k²/(M − 1 + L★²k²/2) exactly.
- **ANG.** ∫dΩ|k̂k̂Q|² = (8π/15)Q:Q*, ∫dΩ k̂k̂Q = 0, ∫dΩ|k̂·D|² = (4π/3)|D|² for random complex STF Q and D (quadrature,
  1e-12).
- **X-LIT (required; literature PROVISIONAL).** Constant-α control (P sector replaced by α(∇n)²/(4K), same machinery,
  n_g = 2): P_quad/P_GR = 𝒜₁ − 1/c_t, P_mono = G ℬ₁⟨I⃛I⃛⟩, P_dip = G 𝒞⟨Σ̇Σ̇⟩ (Σ̇ = μ(s₁ − s₂)a) with Yagi et al. 2014
  Eqs. 118, 120–124 at β_BPS = 0, λ = β, the khronometric α₁, α₂ of CFG291 F3 — all three exactly (residual 0). Then the
  statement "v3s + C1's per-harmonic coefficients = (2/n_g) × Yagi's at α = η(k_S), c_s = ω/k_S" (residual 0). The
  Einstein-aether (Foster) coefficients, Yagi Eqs. 107–114, are compared in the matching limit c₁₄ = η, c₊ = 0, c₂ = β
  (scalar parts; reported).
- **D-LIM.** At fixed (ω, β, M) each per-harmonic coefficient (quad, mono, dip) → 0 as L★ → ∞ (sympy limit on the exact
  stiff-side forms).
- **D-K4.** At every scored (binary, harmonic ≤ 400 with non-negligible power, β, footing, M): L★²k_S²/2 ≥ 1e3·max(M − 1, 1)
  (stiff, k⁴ side), |n_g − 4| ≤ 1e-2, and k_S·a(1 + e) ≤ 1e-2 (multipole/near-zone validity).
- **H-PM.** The harmonic sum of P_GR reproduces the Peters–Mathews (32/5)G⁴μ²m³f(e)/(c⁵a⁵) for each binary to 1e-6
  relative, and Σ_n ½ω_n⁴|D_n|² reproduces ⟨|D̈|²⟩ = μ²(Gm)²(1 + e²/2)/(a⁴(1 − e²)^{5/2}) per unit (s₁ − s₂)² to 1e-6.
- **P-LIN.** Linear validity: C1 dominance over khronon charge transport, Bc²k_S² ≥ 1e3·Kρ_τ at r = 2π/k_S and
  Bc²/(Kρ_τa²) ≥ 1e3 at r = a, ρ_τ = m/(2πL★²r) + 1e-21 kg/m³ (Galactic phantom, ILLUSTRATIVE as X15); the dropped μ_K
  correction μ_K²L★²/2 ≤ 1e-3.
- **P-WAVE.** Wave linearity (the switch stays on): the radiated δ(D·P) = k_S²|ψ|/K at r = 2π/k_S, with the far field
  |ψ| = KB|Σ|k_S²/(2πr n_gω²) of the strongest harmonic, summed over channels under sensitivity bracket σ3, is ≤ 1e-3 of
  the background hedgehog D·P = m/(2πL★²r).

## 5. Step 2: scoring

- Grid: 41 log-spaced β on [β_min(foot), β_max(μ_K)] (S0-2's rerun window), footings with L★ = 21.682 / 22.849 pc,
  μ_K ∈ {0.1, 0.03} Mpc⁻¹, M ∈ {1, 100}. Dispersion: ω_n² = Bc²k²(M − 1 + L★²k²/2) solved for k_S.
- **Sensitivity brackets** (no NS sensitivity is computed in the record or here). R_NS = 12 km, |Ω/m|_max = 0.3 (CFG291),
  white dwarfs s = 0; NS–NS |s₁ − s₂| ≤ s_NS of the heavier star (conservative), |S| ≤ s_NS.
  - σ0: s = 0.
  - σ1: s_NS = |Ω/m|_max |α₁(k) − (2/3)α₂(k)| at k = 1/R_NS, with X15's α₁(k) = −4η(k),
    α₂(k) = η(η(1 + 2β) − β)/(β(2 − η)) (Foster 2007 eq. 70 form).
  - σ2: 3 × σ1 (Yagi et al. PRL: realistic NS sensitivities up to 200 % above the weak-field value).
  - σ3 (envelope): max(σ2, G m_NS/(c²L★)), the fraction of the star's mass in its P hedgehog's self-energy out to L★
    (ESTIMATE; for a weakly gravitating body this piece is already in the linear system, so counting it as a sensitivity is
    deliberately generous).
  - σX (counterfactual, reported only, no verdict weight): s_NS = β|Ω/m|_max (as if the khronon charge scaled with C1's λ;
    contradicts Barausse 2019's vanishing at α = β_BPS = 0 for any λ).
- δ_total = δ_mono + δ_quad + δ_dip(|s₁ − s₂|) + δ_S (the sensitivity-weighted Yagi terms mapped × 2/n_g, bound).
  A grid point **passes** iff δ_total ≤ δ⁺ for all four binaries under σ0, σ1, σ2 and σ3, at both M.
- Reported for every point: δ per channel, ΔṖ_b, δ/σ_1σ, and s_crit = the |s₁ − s₂| at which δ_dip alone reaches δ⁺ − δ_rest.

## 6. Verdict (scored per footing, never pooled)

W(foot, μ_K) = passing grid points.
- **C1 PASSES BINARY PULSARS** iff every required check passes and W is the whole grid (41/41) on both footings at both μ_K.
- **WINDOW NARROWED TO …** iff every required check passes, W is non-empty on both footings at μ_K = 0.1 Mpc⁻¹ but not the
  whole grid somewhere; the surviving edges are reported per footing and μ_K.
- **WINDOW CLOSED** iff W is empty on both footings at both μ_K.
- **UNDECIDED** iff any S0 check fails (stop rule), any required step-1 check fails, the footings disagree on emptiness at
  μ_K = 0.1, or no other class applies.
- The verdict line also names the condition: σX's outcome and the s_crit range (the NS sensitivity must stay below s_crit).

## 7. Reported only (no verdict weight)

- **R1 GW170817.** c_T = 1 with C1 (from S0-3's tensor root); c_S at 100 Hz at the window edges; tensor→scalar Cherenkov is
  kinematically closed (the scalar is faster); GW170817 bounds c_T, not the scalar.
- **R2 causality.** Phase and group speeds per binary; on the khronon leaves ω_S(k) is real for every real k (Petrovskii);
  on a slice tilted by w = 369 km/s the boosted dispersion is a quartic in ω′ — the critical κ above which it has complex
  roots (I1-type) is reported; for a hypersurface-orthogonal khronon ∮∇ln N·dx = 0, so no closed signal loops; compared
  with C5/C8's statement (criterion A violated, criterion B satisfied).
- **R3** V_CM: relative size O(V/c_S) at V = 369 km/s (estimate). **R4** β → 0⁺ and L★ → ∞ scaling exponents of the three
  coefficients (fixed ω). **R5** dipole in the Σm v = 0 frame vs the momentum frame. **R6** absolute ΔṖ_b at the window
  edges. **R7** the k² → k⁴ crossover frequency for M = 100.

## 8. Checks, MUTATE, outputs

- Required checks: S0-1 … S0-5, D-HERM, D-GR, D-RES, D-ON, D-FORM, ANG, X-LIT, D-LIM, D-K4, H-PM, P-LIN, P-WAVE. The script
  exits 0 iff every required check passes.
- **MUTATE** (`X16_MUTATE=1`, all at once, outputs `*_MUTATE*`, step-0 reruns in `step0_reruns_MUTATE/`); each named check
  must FAIL:
  - m1: X15's own script run with `X15_MUTATE=1` → **S0-1**;
  - m2: H₀ doubled in this lane's copy of X14's β_max formula → **S0-2**;
  - m3: C1's sign flipped (β → −β) in this lane's action for the dispersion check → **S0-3**;
  - m4: J0737's P_b × 1.01 in this lane's inputs → **S0-4** (own K7 recomputation) and **S0-5**;
  - m5: tensor source h_ijT^ij instead of ½h_ijT^ij → **D-GR**;
  - m6: dipole source in the Σm_av_a = 0 frame instead of the momentum frame → **X-LIT**;
  - m7: Kepler's equation skipped (E = mean anomaly) → **H-PM**.
- Outputs: `x16_beta_binary_radiation.out`, `x16_beta_binary_radiation_results.json` and `_MUTATE` twins; README with the
  verdict, the radiated-power formula and its β, η dependence, δ per binary vs bounds, every amendment labelled PRE-RESULT
  or POST-RESULT, and "what this does not show".
- Git: pathspec commits of this lane only; never push; no rebase or amend.
