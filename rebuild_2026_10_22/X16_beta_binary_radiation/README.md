# X16_beta_binary_radiation: with C1 inside its window, how much does the khronon scalar's radiation change binary-pulsar orbital decay, and does it stay inside the observed Ṗ_b agreement with GR?

Criteria: `FROZEN_CRITERIA.md` + `ASSUMPTION_LEDGER.md` + `LITERATURE_MAP.md` (db3a4913a0, committed alone before any script or
number). Amendments A1, A2 (PRE-RESULT, ff02290692, before any run) and A3 (POST-RESULT, output and reporting only), below.
Launched from X15's "What this does not show": C1 makes the khronon a propagating, superluminal, dispersive scalar, and its
binary-pulsar radiation had not been computed. C8 K7's "no radiative channel" holds only at β = 0.
κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled. No dark-matter particle. Not "theory closed". The only
data are binary-pulsar timing summaries already transcribed in the record; nothing here says the data favour the framework.

## Verdict: C1 PASSES BINARY PULSARS (whole window, both footings, both μ_K), on a named condition

- **Every grid point passes for all four record binaries** (41/41 in each of the four footing × μ_K cells, `window`):
  - canonical: β ∈ [1.9935e-6, 1.0049e-5] at μ_K = 0.1 Mpc⁻¹, and up to 1.1168e-4 at μ_K = 0.03;
  - alt: β ∈ [2.1976e-6, 1.0049e-5] at μ_K = 0.1, and up to 1.1168e-4 at μ_K = 0.03.
- **The double pulsar's extra decay is 7.7e-15 to 2.1e-14 of GR's** (ΔṖ_b = −9.6e-27 to −2.6e-26 s/s, canonical; alt
  7.3e-15 to 1.9e-14). That is 1.2e-10 to 3.3e-10 of its 1σ precision (6.3e-5). The 2σ upper edge is 8.9e-5.
- **The named condition: neutron-star sensitivities.** Weakly gravitating bodies radiate only through the monopole and
  quadrupole channels, which are negligible. The dipole channel is strong (coefficient ∝ 1/(B c_S)). It stays harmless
  only while the stars' sensitivity difference |s₁ − s₂| is below s_crit:
  - 7.2e-7 (double pulsar), 3.4e-6 (B1913+16), 1.3e-5 (J1738+0333) and 4.5e-5 (J0348+0432), at the bottom of the window
    (`s_crit_min_over_window`); s_crit grows with β.
  - Every bracket the record supports sits far below that: σ1 (Foster's weak-field form with this lane's α(k = 1/R_NS))
    gives 1.4e-27 (canonical) / 1.3e-27 (alt); the deliberately generous envelope σ3 (the P hedgehog's self-energy
    fraction G m/(c²L★)) gives 2.8e-15 to 4.4e-15.
  - The counterfactual σX (s = 0.3β, as if the khronon charge scaled with C1's λ) **fails the double pulsar** for
    β ≥ 3.24e-6 (canonical) / 3.47e-6 (alt) at μ_K = 0.1 (29/41 points; 36/41 at μ_K = 0.03). It passes the other three
    binaries everywhere. Barausse 2019 (record transcription) finds sensitivities vanish at α = β_BPS = 0 for any λ, which
    is v3s + C1's situation at the stellar scale (α_eff = η(1/R_NS) ~ 1e-27). No strong-field sensitivity calculation
    exists for v3s + C1, in the record or here.

## The radiated power (step 1; sympy, `D_RES`, `D_FORM`, `X_LIT`)

The linear system is X15's (GR + P sector + switched stiffness + C1, unitary gauge), with the source generalised to
−ρn − Tψ + J·N, plus the TT tensor sector. Units c = 1, K = 4πG, B ≡ β/(2 + 3β), η(k) ≡ 2/(M + ΘL★²k²/2).

- **One radiating scalar, positive energy.** The scalar block has the single root ω_S² = βk²(L★²k² + 2M − 2)/(2(3β + 2)),
  X15's root (S0-3). The vector block has no ω zero (det = −M k²/4). The residue at the pole is rank 1:

      S†RS = K B |Σ|²,     Σ = T + (2/η)ρ − ωJ/(Bk)                      (D-RES; residual 0; K B > 0 for β > 0)

  For a conserved source on shell, Σ = T + ρ (D-ON). The scalar couples to the trace of the stress, to ρ's quadrupole
  only through k², and, in the binary's momentum frame, to the sensitivity mass dipole through 2/η = 1 + ω²/(Bk²).
- **The power formula.** P = (πω/2)∫d³k/(2π)³ K B |Σ|² δ(ω² − ω_S²(k)), from the anti-Hermitian part of the retarded
  response. Through the tensor sector it gives GR's (G/10)ω⁶|Q|² per harmonic to 2.2e-15 (D-GR).
- **Per harmonic** (n_g ≡ d ln ω_S²/d ln k = 4(L★²k² + M − 1)/(L★²k² + 2M − 2), which is 4 on the stiff side; c_S = ω/k_S):

      P_quad = (G B/(30 n_g)) ω⁶|Q|²/c_S⁷
      P_mono = (G B/(4 n_g)) (1 + 1/(3c_S²))² ω⁶|I_kk|²/c_S³
      P_dip  = (G/(3 n_g B)) (1 + B/c_S²)² ω⁴|D|²/c_S,     Ḋ = −μ(s₁ − s₂)v      (D-FORM; residual 0)

- **This is the khronometric binary flux, made dispersive.** With a constant α in place of the P sector (n_g = 2), the
  same machinery gives exactly Yagi et al. 2014's 𝒜₁ − 1/c_t, ℬ₁ and 𝒞 (Eqs. 118, 120–124), and c_s² (all residuals 0;
  `X_LIT`). So v3s + C1's coefficients are exactly (2/n_g) × Yagi's at α = η(k_S), β_BPS = 0, λ = β, c_s = ω/k_S. The
  Einstein-aether (Foster) scalar parts agree in the matching limit c₁₄ = η, c₊ = 0, c₂ = β (w₀² − c_s² = 0).
  - The literature values were read through a summarising fetch and are PROVISIONAL. An exact match of four independent
    coefficient forms is the stronger cross-check.
  - The dipole matches only in the momentum frame. In the Σm v = 0 frame it is off by (1 + B/c_S²)²; that is MUTATE m6,
    and numerically it is ≤ 1.3e-8 (R5).
- **β and η dependence.**
  - c_S² = B(2 − η)/η ≈ 2B/η. So the coefficients scale as B/c_S⁷ ∝ η^{7/2}B^{−5/2} (quadrupole), B/c_S³ ∝ η^{3/2}B^{−1/2}
    (monopole) and 1/(B c_S) ∝ η^{1/2}B^{−3/2} (dipole).
  - At the radiated wavelength η(k_S) is small: 8.9e-10 at the double pulsar's n = 2 harmonic (canonical β_min), up to
    6.7e-9 at β_max(0.03) (R2). That is what suppresses the monopole and quadrupole channels.
  - At fixed ω the exponents are (R4): d ln/d ln β = −0.75, +0.25, −1.25 and d ln/d ln L★ = −3.5, −1.5, −0.5 (quadrupole,
    monopole, dipole). Every coefficient → 0 as L★ → ∞ (D-LIM), and GR + C1 alone has no radiating scalar (its scalar
    determinant is βk⁶/(2K³), with no ω).
  - The limit β → 0⁺ at fixed ω is singular for the dipole and quadrupole. At β = 0 there is no mode (C8). It lies below
    the window and is not scored.
- **Regime.** The radiation is on the stiff, k⁴ side: (L★²k_S²/2)/(10³ max(M − 1, 1)) ≥ 4.4e2 and |n_g − 4| ≤ 4.6e-6
  (D-K4). The mode has no cutoff above ω = 0: with M = 100 the k² → k⁴ crossover is at ω_x ≤ 6.6e-10 rad/s (R7), far below
  every orbital frequency. Multipole validity holds, k_S a(1 + e) ≤ 1.3e-3.

## Step 2: the fractional Ṗ_b shift δ = Ṗ_b(scalar)/Ṗ_b(GR) against the bounds

δ⁺ is the 2σ upper edge, the strictest of the record's transcriptions (FROZEN §2). Each value is the maximum over the
window, M ∈ {1, 100} and brackets σ0–σ3 (the per-binary lines of the `.out`). The R6 rows give the window edges.

| binary | δ⁺ | canonical δ (β_min → β_max 0.03) | alt max δ | dominant channel | s_crit (min) can / alt |
|---|---|---|---|---|---|
| J0737−3039A/B | 8.9e-5 | 7.68e-15 → 2.10e-14 | 1.94e-14 | monopole (e = 0.088) | 7.17e-7 / 7.72e-7 |
| B1913+16 | 1.5e-3 | 3.29e-13 → 8.98e-13 | 8.30e-13 | monopole (e = 0.617) | 3.39e-6 / 3.65e-6 |
| J1738+0333 | 0.166 | 1.21e-17 → 5.93e-19 | 9.40e-18 | quadrupole | 1.26e-5 / 1.36e-5 |
| J0348+0432 | 0.41 | 1.61e-19 → 7.70e-21 | 1.24e-19 | quadrupole | 4.51e-5 / 4.86e-5 |

- δ/σ_1σ ≤ 5.6e-10 for every binary (R6, `delta_over_1sigma_sigma3`).
- Absolute shifts: double pulsar ΔṖ_b = −9.58e-27 to −2.62e-26 s/s; B1913+16 −7.90e-25 to −2.16e-24 s/s.
- The Galactic background changes δ by at most 1.43e-6 relative between M = 1 and M = 100 (R8).
- σ1/σ2/σ3 add nothing visible. The largest sensitivity term is the J0348 σ3 row (1.61e-19 vs 1.57e-19 at σ0).

## Step 0: reproductions (stop rule; all pass)

| check | result |
|---|---|
| **S0-1** X15's own code | A byte-identical copy (sha 2bf28103…) was run in this lane: exit 0, 13/13, verdict "C1 SURVIVES PPN". Its ω² root strings (Θ = 1, 0), α₁(k) and α₂(k) are identical to X15's committed JSON; its windows deviate by 0. Outputs, incl. A22's redirected JSON, are in `step0_reruns/x15/`. |
| **S0-2** X14's own code | Copy run in `step0_reruns/x14/`: exit 0, 24/24, 23 s. β_min = 1.993547e-6 / 2.197554e-6, β_max = 1.004925e-5 (μ_K 0.1) / 1.116754e-4 (0.03); rerun vs committed and this lane's formulas vs rerun both 0.0. |
| **S0-3** this lane's system | Scalar root βk²(L★²k² + 2M − 2)/(2(3β + 2)) (Θ = 1) and βk²(M − 1)/(3β + 2) (Θ = 0), residual 0 against X15's strings. Tensor root ω² = k² with C1 present: c_T = 1. |
| **S0-4** the record's double-pulsar number (C8's own code) | Copy run in `step0_reruns/c8/`: exit 0, 8/8 incl. K7, 75.6 s, 0.29 GB. K7 block vs committed 0.0, worst ratio 3.2190e-14. The ledger's and C8's PSR tables (AST-parsed) agree; the J0737 entry carries "0.999963(63)". This lane's inputs vs the record: P_b ≤ 2.2e-11, m₁ + m₂ ≤ 7.8e-6 (A1). Own K7 recomputation 0.0. |
| **S0-5** Peters–Mathews | −1.247810e-12 (J0737, record −1.247920e-12, 8.8e-5); −2.402573e-12 (B1913, 1.7e-5); −2.746093e-14 (J1738, 8.6e-3, inside +1.5/−1.9); −2.590857e-13 (J0348, 4.2e-3, inside). |

Reported: P3's double-pulsar π–metric mixing ε = 2.012e-9 (read, not rerun).

## Reported only (no verdict weight)

- **R1 GW170817.** c_T = 1 exactly with C1 (K² has no TT part). The scalar at 100 Hz moves at 3.1e4–8.8e4 c. GW170817
  bounds c_T, not this mode. A tensor wave cannot Cherenkov-radiate into a faster scalar.
- **R2 superluminality and causality.**
  - At the double pulsar's n = 2 harmonic the scalar's phase speed is 47–133 c and its group speed 95–266 c (twice the
    phase speed on the k⁴ side). λ_S = 6.3e13–1.8e14 m.
  - Because ω ∝ k², the group speed has no upper bound at large k. This is the same "faster than c, ordered in τ" structure
    as C8's leaf-instantaneous sector: criterion A is already violated there, and criterion B holds.
  - Posed on the khronon's own leaves the mode is well posed, since ω_S² ≥ 0 for every real k when Θ = 1 and M ≥ 1.
  - On a slice tilted by 369 km/s, the boosted dispersion (a quartic in ω′) has complex roots above κ_c = 4.3e-13 m⁻¹
    (canonical β_min) to 5.8e-14 m⁻¹ (β_max 0.03). That is 0.50 × I1's estimate 1/(2√A w) (onset u_c = 0.501 on the
    grid). It is I1's Hadamard pattern.
  - v3s's khronon is hypersurface-orthogonal by construction, so its leaves exist everywhere (unlike v4's twisting
    aether), and ∮∇ln N·dx = 0 rules out closed signal loops.
  - So C1's scalar adds no causality issue beyond C5/C8, provided evolution is posed on the khronon leaves.
- **R3** V_CM/c_S ≤ 2.6e-5 at 369 km/s. The binary's motion through the khronon changes the s = 0 flux only at that
  relative order (ESTIMATE). **R5** the dipole frame factor is ≤ 1.3e-8. **R7, R8** as above.

## Checks (`x16_beta_binary_radiation.out`, `_results.json`)

- **Main run: 17/17 PASS, exit 0.** The checks are S0-1 to S0-5, D-HERM, D-RES, D-ON, D-FORM, ANG, D-GR, X-LIT, D-LIM,
  H-PM, D-K4, P-LIN and P-WAVE.
  - 105 s. Peak RSS 0.104 GB for this process; the C8 copy peaks at 0.29 GB. One thread, nice 15, PYTHONHASHSEED=0.
  - Margins: H-PM ≤ 1.1e-14 (P_GR and ⟨|a|²⟩ vs Peters–Mathews); P-LIN C1 dominance ≥ 1.2e13 and μ_K correction
    ≤ 2.6e-12; P-WAVE δ(D·P)/D·P ≤ 1.6e-7.
- **MUTATE (`X16_MUTATE=1`): exit 1, 9/17, and every required failure bites.**

  | mutation | change | fails |
  |---|---|---|
  | m1 | X15's own `X15_MUTATE=1` | S0-1 (exit 1, 3/13) |
  | m2 | H₀ doubled in this lane's copy of X14's β_max | S0-2 (own vs rerun 3.0) |
  | m3 | C1's sign flipped in the dispersion check | S0-3 (root βk²(…)/(2(3β − 2))) |
  | m4 | J0737's P_b × 1.01 | S0-4 (P_b vs record 1.0e-2), S0-5 (1.7e-2) |
  | m5 | tensor source h_ijT^ij instead of ½h_ijT^ij | D-GR (3.0) |
  | m6 | dipole in the Σm v = 0 frame | X-LIT (dipole residual ∝ 4 − (2 − α)²) |
  | m7 | Kepler's equation skipped | H-PM (B1913 P_GR 0.94) |

  The MUTATE verdict line (UNDECIDED) is the control's output, not physics.

## Amendments and execution history

- **db3a4913a0:** criteria, ledger and literature map, committed alone.
- **A1 (PRE-RESULT, ff02290692).** S0-4's own K7 recomputation now uses the record table's (P_b, M_tot). An
  input-consistency clause (≤ 1e-5) was added, because this lane's mass pairs sum to the record's M_tot only to 3.9e-7 /
  7.8e-6.
- **A2 (PRE-RESULT, ff02290692).** D-GR uses symbolic tensor residues plus the ANG quadrature (1e-10). D-LIM uses symbolic
  M and B.
- **A3 (POST-RESULT, output and reporting only).** After the first (development) main run:
  - the JSON grid rows were pruned to a listed key set;
  - per-binary counts were added to the σX report;
  - R8 (the M = 1 vs 100 sensitivity) was added.

  No check, threshold or scored number changed. The development and scored runs share 28,736 JSON leaves, all equal apart
  from timing. Their `.out` files differ only in timing and the added report lines.

## What this does not show

- **Neutron-star sensitivities are not computed.** The PASS is conditional on |s₁ − s₂| < s_crit (7.2e-7 for the double
  pulsar). σ1–σ3 are brackets: Foster's weak-field form with this lane's α(k), ×3, and an envelope. The counterfactual
  s ∝ β would close the double pulsar above β ≈ 3.2e-6. A strong-field sensitivity calculation for v3s + C1 would settle
  it.
- **Linear, weak-field, leading post-Newtonian order.**
  - The sensitivity-weighted terms (Yagi 𝒜₂, 𝒜₃, ℬ₂, ℬ₃) are bounded with the mapped literature coefficients, not derived.
  - Barausse's V_CM·(s₁ − s₂)² terms are not included. They are ∝ (s₁ − s₂)², so negligible under σ0–σ3.
  - The O(V/c_S) Doppler corrections are estimated, not computed.
- **The Galactic background is an isotropic bracket M ∈ {1, 100}.** The real M_L/M_T anisotropy is not modelled; δ moves by
  ≤ 1.43e-6 across the bracket.
- **Propagation far from the source is not followed.** Beyond a few λ_S, D·P could change sign (the soft side) and the mode
  would change character there. Emission is set within λ_S, where D·P > 0 (P-WAVE).
- **The literature is PROVISIONAL.** Yagi et al.'s coefficients came through a summarising fetch, and Σ_i's definition
  was not read; the exact constant-α match is the stronger check. Pulsar summaries are record transcriptions, not
  re-verified. This is not a timing analysis.
- **X14's and X15's caveats on C1 remain:**
  - the caustic cure is linear and subsonic only;
  - the upper window edge rests on C5's IR-band estimate;
  - the literature ghost warning for this class stands;
  - supersonic galaxy cells (X15 step 3) are not estimable.

## Suggested fixes elsewhere (not edited here)

- **C8 README, K7.** "No radiative channel" holds at β = 0 only. With C1 in X14's window the khronon radiates. δ ≤ 2.1e-14
  for the double pulsar and ≤ 9.0e-13 for B1913+16, provided |s₁ − s₂| < 7e-7 (X16).
- **V3_FULL_PICTURE §3, row "Gravitational waves, binary pulsars".** Replace "with the β completion, scalar radiation is
  not computed, X15" with: "with C1, scalar radiation passes (X16): δ ≤ 2.1e-14 (J0737), 9.0e-13 (B1913); conditional on
  NS sensitivities |s₁ − s₂| < 7e-7; c_T = 1".
- **X15 README, "What this does not show".** The binary-pulsar bullet is now computed in X16.
- **X14 README, C1 row.** Add: binary pulsars pass with the sensitivity condition; c_T = 1 confirmed.
- **I1 README.** Its κ_c ≈ 1/(2√A w) for the tilted-slice onset differs by a factor 2 from X16's boosted quartic (onset at
  0.50 × that value). This is not load-bearing; it may be a convention difference in A or w.
- **CFG291.** Its counterfactual B3 is X16's σX. On the old chassis it failed; in v3s + C1 it fails only the double pulsar,
  above β ≈ 3.2e-6. The open item is the same in both: a strong-field NS sensitivity at small α.

## Files and run

| file | contents |
|---|---|
| `x16_beta_binary_radiation.py` | Parts S0, D, H, W, R. X15's `lagrangian` and X14's window formulas are copied with provenance. X15, X14 and C8 are run as byte-identical copies inside this lane. |
| `x16_beta_binary_radiation.out`, `_results.json` | main run |
| `x16_beta_binary_radiation_MUTATE.out`, `_results_MUTATE.json` | MUTATE run (m1–m7) |
| `step0_reruns/{x15,x14,c8}/`, `step0_reruns_MUTATE/…` | the record scripts' own outputs from S0-1, S0-2, S0-4 |

```
PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/X16_beta_binary_radiation/x16_beta_binary_radiation.py              # exit 0
PYTHONHASHSEED=0 X16_MUTATE=1 OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/X16_beta_binary_radiation/x16_beta_binary_radiation.py  # exit 1 by design
```
