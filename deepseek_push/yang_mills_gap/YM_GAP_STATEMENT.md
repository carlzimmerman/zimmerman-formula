# YM GAP STATEMENT — the mass gap as the eaten Goldstone of the a0-sector

**Lane:** `deepseek_push/yang_mills_gap/` (2026-09-17) · **Record:** YM00_CAMPAIGN.md
(pre-registered gates), YM01_gap_derivation.py/.out/_results.json (20/20),
lean/YM01_gap.lean (19 theorems, exit 0, zero sorry, axioms ⊆
{propext, Classical.choice, Quot.sound}).

## THE ONE-LINE STATEMENT

Starting from the framework's own action (L5: L = Λ⁴ f(K), the shift-symmetric
scalar with the L2/G031 interpolant f′(K) = μ₂(u), u = |∂φ|/Λ²), the ONLY
structure-preserving way to give the equilibrium sector a gapped gauge field
is to localize the shift — and when you do (D φ = ∂φ − mA, the minimal
Stueckelberg gauging), the B8 gapless Goldstone is eaten and the mass gap is,
EXACTLY and in closed form,

    clean face:   m_A² = μ₂(u)·m²                   (the Stueckelberg truncation)
    exact face:   m_A² = m²·u(u²+3u+4)/(1+u)³       (FULL n=2 potential, 2nd order)
    ratio:        η(u) = (u²+3u+4)/((1+u)(2+u)) ∈ [1,2]   (2 deep → 1 dense)

**The Yang-Mills gap, in this framework, is the eaten Goldstone: a theorem of
the algebra, not a miracle** — and the gap is an EQUILIBRIUM PHENOMENON: it is
exactly zero where the phantom is absent (μ₂(0) = 0: vacuum, Solar System,
beyond the cap) and it follows the phantom's profile inside the halo.

## WHAT IS PROVEN (and how)

| Rung | Statement | Evidence |
|---|---|---|
| A1/A2 | μ₂(u) = u(2+u)/(1+u)² = the RAR face 1−(1+x/2)^−2 at u = x/2 | sympy residual 0 + Lean (mu2_cleared, mu2_deep, kernel_face) |
| B1 | the gauged expansion's mass coefficient = f′(K₀) ⟹ m_A² = μ₂(u₀)m² | sympy residual 0 + Lean (def gap_clean; gap_clean_pos) |
| B2 | exact face m_A² = m²u(u²+3u+4)/(1+u)³ from the FULL potential | sympy residual 0 + Lean (gap_exact_sq) |
| B3/B6 | η(u) ∈ [1,2]; the slope series −1/2 + (9/8)u + O(u²) exact | sympy (coeffs −1/2, 9/8) + Lean (eta_bounds, eta_zero) + numerics on TWO windows (residual 7e-4, 6e-3) |
| C1 | Stueckelberg invariance: the localized shift IS a gauge symmetry | Lean (stueckelberg); no preferred frame at the action level (α₁ = α₂ = 0 by structure, L5) — the G054 kill's boundary registered |
| D1/B5 | the U-MAP coefficient C_f = 1/(2√(8π)) EXACTLY from L1 + the AQUAL lock (M_pl and Λ are the same object; G, a0, ℏ, c all cancel) | sympy symbolic + numeric 1e-7 + Lean (sqrt_pair_8pi, sqrt_pair_8pi_naked, u_map_closed) |
| D2-D5 | the profile: m_A(r)/m_A(8.2 kpc) parameter-free; deep law r^{−1/2} (asymptotic) with the 9/8 correction on the observable window; Proca dispersion ω² = k² + m_A² on every k; vacuum/strong-field/cap closing | sympy + numerics (20/20 gates incl. K1-K5) |
| THE GAP | ω(k) = √(k²+m_A²) ≥ m_A, attained at k = 0; n ≥ 1 excitations cost ≥ m_A (Fock face); m_A > 0 where u > 0 | **Lean: gap_theorem, gap_tight, excitation_gap** |
| G081 link | the certified marginal mode ω² = 0 EXACT IS the gaugeless face; gauging LIFTS it: ω(0)² = m_A² > 0 — "no growing mode, no decay channel" rigidity preserved (a massive vector decays only above 2m_A) | numerics + B8/E02 record |

## THE HONEST VERDICT (registered, never hedged)

1. **The Clay SU(3)/QCD-scale gap is NOT claimed.** The framework has no QCD
   sector (TOE_STATUS.md, dead SM bridge) — this lane proves the framework's
   OWN gap mechanism and its exact scale law, and says so. K5.
2. **The gap is observationally SILENT at framework scales.** Baryons carry no
   shift charge (tree-level decoupling); the dust-dust Yukawa's range at the
   fiducial scale (m = Λ ≈ 2.2 meV) is ~10⁻⁴ m and its strength (m/M_pl)² ≈
   1e-60 of gravity. Silence is reported as silence — never upgraded.
3. **One new constant:** the gauging scale m is the door's price (the
   framework's zero-parameter claim is otherwise untouched: everything else is
   ratios of committed constants). m = Λ is the one-constant fiducial, NOT a
   derived value.
4. **Registered finding (G1b for the follow-up):** the committed constants give
   C_f = 1/(2√(8π)) ≈ 0.10, NOT the 1/2 that would make the field-equation
   argument u coincide with the RAR argument x — the closed sourced-equation
   face (G155, dead) would carry a √(8π)-class a0-shift; the LIVE equilibrium
   reading is unaffected (it never uses the u-map). Whether some committed
   identity absorbs the map is the named open gate.

## THE FALSIFIER RECIPE

The parameter-free PREDICTION: inside the phantom, a massive-vector sector —
if it exists — has the exact spatial law

    m_A(r)/m_A(8.2 kpc) = √( u(r)(u(r)²+3u(r)+4) / (1+u(r))³ )  /  (same at 8.2)

(killable: an observed profile with any other shape; a massless-vector
signature inside the phantom; a gap that fails to close in vacuum / beyond
the cap; a preferred-frame observable, α₁, α₂, that G054's class forbids).

## THE FILES

| File | Content |
|---|---|
| YM00_CAMPAIGN.md | the pre-registered record: door, kill conditions K1-K5, falsifier |
| YM01_gap_derivation.py / .out / _results.json | the derivation lane, 20/20 checks PASS |
| lean/YM01_gap.lean | 19 theorems, exit 0, zero sorry, axioms {propext, Classical.choice, Quot.sound}, incl. THE GAP THEOREM (gap_theorem), its tightness (gap_tight), the Fock face (excitation_gap), the vacuum closing (mu2_zero, vacuum_clean), the monotonicity (profile_mono), the mass faces (gap_exact_sq, gap_exact_pos, gap_clean_pos), the gauge identity (stueckelberg), the efficiency (eta_bounds, eta_zero), and the U-MAP closed form (u_map_closed) |

Lean certifies the mathematics (the premises are the committed lanes' claims —
L5's action, L2's kernel, the minimal gauging — stated in the file header).