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

## B. Open challenges — pass conditions stated in advance

| # | challenge | passes if |
|---|---|---|
| B1 | **σ = 1 re-verification.** Cherenkov forces σ from 1/3 to 1 within 4e-15. σ shifts p_R, A_R, B_R, F. | the IC6 obstruction, the IC7 counterterm and the tensor balance all re-derive at σ = 1 |
| B2 | **The mapping.** (c₁₄, c₂, \|K₂\|Q₀²) are not determined by the published IC files; c₁₄ has three readings spanning 0.073–1.333. | the PPN weak-field expansion of the IC action with the auxiliary constraint solved, plus the O(k⁰) mass term of the reduced scalar system |
| B3 | **Galactic matching** (the lead's own open item). | the static weak-field limit yields MOND with the frozen μ(y) = 1 − e^(−y) and a₀ = 9.3619e-11 / 1.1279e-10 |
| B4 | **P7 / A3.** Does the same coefficient control the PPN-visible coupling and the kinetic normalisation? A4's cost note says it may. | an independent finite kinetic normalisation is exhibited in the screened regime |
| B5 | **The clock sector and Ω_d.** A6's region is empty if the clock must carry Ω_d = 0.266 (short by 3.2e4×). | either the clock does not carry Ω_d, or a source that does is exhibited — noting A7/A8 close every mechanism tried |

## C. Standing rules that bind both sides
Both a₀ footings on every dimensional number. Every load-bearing claim is a runnable script with
checks that can fail. Frozen preregistrations and `*_HASH.txt` are untouchable. κ = ½ is fitted.
Nothing is ever "theory closed".
