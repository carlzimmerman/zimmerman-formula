# Handoff contract — the shared interface between the independent lane and the lead

Purpose: the lead agent's recipe adopts OpenAI's *NavierStokesAndEuler* verification architecture —
**independently specified challenges, separately checked submissions**. This file is the second half
of that architecture from this side: challenges stated so the lead can consume them directly, and
results stated so it can rely on them without re-deriving.

Every entry names its script and commit. Nothing here is a claim a check did not survive.

## A. Settled — the lead may rely on these

| # | statement | where | commit |
|---|---|---|---|
| A1 | The lead's IC5/IC6/IC7 algebra reproduces exactly under independent hand rebuild: the boxed obstruction to 18 digits, det(M\*), c₇, the sheared state, the constraint algebra, IC7's leftover. c₇ is genuinely built from action derivatives alone. | `L4_verify_ic7.py`, `L4_VERIFICATION.md` | 0e20cf937 |
| A2 | The local degree-of-freedom count for IC5/6/7 is **3**: two tensors + one healthy khronon (A₀ = 0.46 > 0, DeWitt λ = 1, c_s² = 1/3). IC7 does not remove it. Permitted by I3a **only** as an identified, healthy clock mode. | same | 0e20cf937 |
| A3 | IC7's repair window is |j−1| < 0.074, and on curved backgrounds it detunes the tensor cone: c_T² = 1 − 4c₇R̄₀/c, with 4c₇/c = 0.00857 per unit R̄₀. | same | 0e20cf937 |
| A4 | **The clock's PPN arm passes.** The exponential wall puts Cassini 3.7e4× above the PPN threshold; the preferred-frame coupling there is e^(−5.8e5). Recorded cost: c₁₄ → 0 is also the strong-coupling limit. | `L10_khronon_gate.py` | (this commit) |
| A5 | **Gravitational Cherenkov excludes c_s² = 1/3 by 2.1e14×** (bound 1 − c_s ≤ 2e-15). The exp wall cannot rescue it: the bound is read where \|a\| ~ a₀, the wall acts where \|a\| ≫ a₀. | same | (this commit) |
| A6 | Target region for any clock in this class: c₁₄ ≤ 2.5e-5, c₂ in a thin collar just above c₁₄ about c₂\* = c₁₄/(1−2c₁₄), M ≤ c₁₄. **Lower edge is always Cherenkov ⇒ the khronon must be marginally superluminal.** | same | (this commit) |
| A7 | Cluster residual: **not** an interpolation kernel (2.2–5.1× the galaxy boost at the same acceleration, \|z\| = 13); **not** a fixed-strength finite-range force (BBN, 41×); **not** a screened force in Φ, ρ or M (100% density overlap at 12.8σ, plus a cosmological-ordering argument). | `L2`, `L5`, `L6` | 0e20cf937, aea949c58 |
| A8 | The required cluster source **is** the cosmic dark-to-baryon ratio: 5.73 ± 0.68 against Ω_dm/Ω_b = 5.43, universal to 12%, f_bar = 0.149. | `L7_cosmic_ratio.py` | 9727a5083 |
| A9 | Galaxy-side capture of a cold component, caustics resolved and cap repaired: **0.92–1.45 M_b inside 10 kpc**, still 4–6× the 0.25 the RAR tolerates. Supersedes g04k's 2.58. | `L1_caustics_and_cap.py` | bcd2cb921 |
| A10 | **Method rule.** The algebraic multiplier ν(\|g\|)g has nonzero curl on non-radial fields and unbinds the system within 1 Gyr. Any non-radial MOND infall calculation needs a genuine QUMOND field solve. | same | bcd2cb921 |
| A11 | κ is not fixed by flux quantisation or by any boundary term: split-degeneracy theorem, β → μβ with Z compensating leaves every quantised and geometric quantity invariant while κ → μκ. The target ratio is footing-dependent (7.96 canonical, 5.48 alt). | `L3_flux_quantisation.py` | 0e20cf937 |

| A12 | **No globally admissible point** for the candidate action on either footing (10 gates, 1.2e8 points each, all controls reproduced). The obstruction is **two gates deep** and every minimal incompatible subset contains the clock tachyon G2. Drop G2 and the other nine admit a real region: K_B <= 0.25, c2 ~ c2*(c14), c14 <= 1.18e-5, \|K2\| in [5e4, 5e5], Q0 <= 1 H0, xi >= 0.10/0.15 pc — which predicts gamma_v in (1.0000, 1.0450] / (1.0000, 1.0300], exactly Amendment 11's Arm B ceilings, and whose c14 bound agrees with A6's independently derived one. | `L14_parameter_sweep.py` | (this commit) |
| A13 | The condensate **cannot be the dark sector**: freeing its amplitude to cure the tachyon caps its dark fraction at 2.6e-6, short of Omega_d by 1e5x. Since its background is also what makes the clock tachyonic, **removing it costs nothing and cures the one fatal gate.** The IC-series has already removed it. | same | (this commit) |

| A14 | **The IC-series reduces to MOND.** Its static weak-field limit is `div[mu(|grad Phi|/a0) grad Phi] = 4 pi G_N rho_b` with `mu(y) = 1 - e^(-y)`, at the action's own a0 with coefficient **exactly 1.000000**, `Phi = Psi` (no slip, so lensing and dynamics share one potential to <1e-4 out to 1 Mpc), and the Newtonian limit at the same G that normalises the tensor sector. The lead's own "galactic matching" open item is answered POSITIVELY. | `L11_galactic_limit.py` | a38df5ebe |
| A15 | **sigma = 1 does not remove the IC6 obstruction** — it grows 1.81x to −20.194205022906776 and IC7 is needed 1.78x more strongly on a window half as wide. New closed form, verified against the lead's identity at sigma = 1/3 and numerically at six sigma to <1.7e-40: `S_4'(1;sigma) = e^{5/6}(p_R T - 9)(3p_R + 4)(3p_R - 44)/(216(4T - 27))`, `p_R = 8/3 + 4 a_* sigma`. **Exactly one zero, at sigma\* = 4T/(4T-27) = 1.679 (29.6% superluminal), above IC-4's whole interval (0,1].** `c_T^2 = 1` and the DOF count are sigma-INDEPENDENT identities. | `L15_sigma_one.py` | 9e5b7e838 |
| A16 | **A late-time roll clears the cosmological gates** (BBN, CMB, growth, expansion incl. absolute BAO) while delivering the cluster enhancement — the first mechanism to survive the gate it was proposed against — predicting sigma_8 = 0.845–0.861 with H0 = 68–72. **But it cannot supply the cluster/galaxy contrast**: the two populations are observed at z = 0.0037 and 0.090, so a uniform g(z) gives 0.97 against a required 2.2–5.1. Also: in a consistent scalar-tensor model g **cancels exactly** from the growth source. | `L9_late_transition.py` | bd2acc304 |
| A17 | **The hybrid rescue is unavailable.** Granting LambdaCDM halos, galaxy data no longer require an acceleration scale: variance explained falls 74.0% → −3.5%, scale bounded at <3.3e-13 (3.4 dex below a0), identical across 11 halo rows spanning 2x the real uncertainty; injection control recovers a0 to 0.100 dex. **What survives:** at zero free parameters the fixed-a0 kernel is still tighter than the halo — 0.142 dex vs 0.171, and 0.198 with halo-population scatter. | `L16_hybrid_inverse.py` | 17085a3de |
| A18 | **Hydrostatic bias is not an escape and runs the wrong way.** The b that would rescue the framework is **negative** (−0.82 for the residual, −2.07 for the cluster/galaxy gap) against a measured [0.00, +0.42]; a negative b means sigma^2 < 0 in 12 of 12 clusters. **Self-correction:** L7's "matches cosmic to 5%" is withdrawn (the ratio runs to 9.04 by b = 0.33); the 13–15 sigma residual and 12% universality survive and strengthen. | `L18_hse_bias.py` | c2fed057e |

## B. Open challenges — pass conditions stated in advance

| # | challenge | passes if |
|---|---|---|
| B1 | ~~σ = 1 re-verification~~ **DISCHARGED by L15**: the obstruction does NOT vanish at σ = 1; it grows 1.81× to −20.194205022906776 and IC7 is needed 1.78× more strongly on a window half as wide. Theorem: S₄′(1;σ) has exactly one zero, at σ\* = 4T/(4T−27) = 1.679 (29.6% superluminal), above IC-4's whole admissible interval (0,1]. c_T² = 1 and the DOF count are σ-independent identities. | **CONDITIONAL NOW OPEN:** if L19 finds the Cherenkov bound does not apply to a k-essence clock, σ\* = 1.679 is reachable and IC7 becomes unnecessary |
| B1-old | (original wording) **σ = 1 re-verification.** Cherenkov forces σ from 1/3 to 1 within 4e-15. σ shifts p_R, A_R, B_R, F. | the IC6 obstruction, the IC7 counterterm and the tensor balance all re-derive at σ = 1 |
| B2 | **The mapping.** (c₁₄, c₂, \|K₂\|Q₀²) are not determined by the published IC files; c₁₄ has three readings spanning 0.073–1.333. | the PPN weak-field expansion of the IC action with the auxiliary constraint solved, plus the O(k⁰) mass term of the reduced scalar system |
| B3 | **Galactic matching** (the lead's own open item). | the static weak-field limit yields MOND with the frozen μ(y) = 1 − e^(−y) and a₀ = 9.3619e-11 / 1.1279e-10 |
| B4 | **P7 / A3.** Does the same coefficient control the PPN-visible coupling and the kinetic normalisation? A4's cost note says it may. | an independent finite kinetic normalisation is exhibited in the screened regime |
| B5 | **The clock sector and Ω_d.** A6's region is empty if the clock must carry Ω_d = 0.266 (short by 3.2e4×). | either the clock does not carry Ω_d, or a source that does is exhibited — noting A7/A8 close every mechanism tried |

## C. Standing rules that bind both sides
Both a₀ footings on every dimensional number. Every load-bearing claim is a runnable script with
checks that can fail. Frozen preregistrations and `*_HASH.txt` are untouchable. κ = ½ is fitted.
Nothing is ever "theory closed".

## D. Documentation conflicts found while verifying — for the lead and the user to resolve

| # | conflict | why it matters |
|---|---|---|
| D1 | **The frozen kernel disagrees between two governing documents.** `CRISPY_FRIED_CHICKEN_RECIPE.md` ingredient I1 freezes `mu(y) = 1 - e^(-y)`; `THE_ACTION_2026-09-05.md` section 3 carries `nu_RAR` (swapped 2026-09-06). The lead follows the recipe correctly. L11 shows the IC-series produces the exponential kernel — so it matches I1 and not THE_ACTION. | The two differ by up to 0.073 dex in the transition, and the exponential ceiling is exceeded 5x more often on the bulgeless SPARC control. Any cross-document comparison is currently ill-defined. **One document needs amending; this is the user's call.** |
| D2 | `IC10_LOCAL_CLOCK.md` and `OPTICAL_ALIGNMENT.md` reuse the symbol `sigma` for an unrelated quantity (−1/4), while `sigma` elsewhere is the clock speed parameter of A15. | A symbol collision in the one parameter A15 shows is decisive. Worth renaming before it causes an error. |
| D3 | `hunt_2026/u13_mass_efe_and_domain.py:334` carries the hydrostatic-bias sign backwards relative to `u02:565`; its C3 prose is wrong. | No published number moves (C7 overwrites `B = 0.0` immediately after), so this is a latent trap rather than an error in the record. Flagged, not edited. |
