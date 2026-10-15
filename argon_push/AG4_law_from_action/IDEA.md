# AG4 — The rest-state law from the frozen S2 action (law-form adjudication)

**Open item addressed:** AG3 HANDOFF_TO_CONDUCTOR §4 (pre-registered branches a/b/c):
which interpolation is the unique static rest state of the frozen action? This is the
theory-internal arbiter of the repo's law-form split — canonical `ḡ = g²/(g+a₀)`
(THEORY_CANONICAL S2 L21; PAPER49; ARGON02) vs quadratic a₀-line `g²−ḡ² = a₀ḡ`
(G071-tested; user-profile program statement; AG3 K2 bands).

## Idea

PAPER49's claim is that the law IS the medium's unique static rest state — a theory-
internal fact, not a fit. So derive it. S2 action:

    L = −|∇Φ − KP|²/(2K) − ρ_bΦ − W_rem(u) − (γ/2)|∇P|²,  K = 4πG, u = K|P|,
    K W_rem′(u) = u²/(a₀ − u),  γ = K L*²/2

Jet Euler–Lagrange (sympy, G1) on the spherical static ansatz: δL/δΦ ⇒ ∇·A = 4πGρ_b with
A ≡ ∇Φ−KP (baryon-only field; point mass ⇒ |A| = ḡ = GM_b/r² by Gauss — declared premise);
δL/δP ⇒ A − (u²/(a₀−u))P̂ + γ∇²P = 0. At rest (γ=0, P ∥ A): ḡ = u²/(a₀−u), and ∇Φ = A+KP
gives g = ḡ + u — the tether variable u IS the phantom acceleration g_ph. Everything else
is algebra, and all of it is Lean-certified.

## Results — BRANCH (a) CONFIRMED

- **G1 (variational):** both field equations derived from the explicit W_rem antiderivative
  (n-family; at n=1 the ArgonClues-certified a₀²(−ln(1−u/a₀)−u/a₀−u²/(2a₀²))); EL residuals
  identically zero.
- **G2 (rest state = canonical law):** ḡ(a₀−u) = u² ⇔ u²+ḡu = a₀ḡ ⇔ (g = ḡ+u) g² = ḡ(g+a₀)
  — EXACTLY the canonical S2 law. Explicit root u = (√(ḡ²+4a₀ḡ)−ḡ)/2 ∈ (0,a₀), unique.
  **PAPER49 anchors reproduced exactly:** ν(ḡ=10⁻⁴a₀) = 100.50125 vs cited 100.5;
  **ARGON02 P1 derived from the action:** M_ph/M_b = (√(1+4x²)−1)/2 and
  ρ_ph = M_b/(2πr_M²r√(1+4x²)) — exact; deep limit u/√(a₀ḡ) → 1 ⇒ shared A/r² asymptote,
  C = √(GM_ba₀), σ² = C/2 chain (GF2/AG1) untouched.
- **G3 (capacity family = the split):** K W_rem′ = u²/(a₀−nu) ⇒ u²+nḡu = a₀ḡ ⇒
  g²−ḡ² = a₀ḡ+(2−n)ḡu. **n=1 ⇒ canonical; n=2 ⇒ the quadratic a₀-line EXACTLY.** The two
  repo law lines differ by ONE structural number: the tether capacity (a₀ vs a₀/2).
  Certified anti-tautology: the n=2 rest state satisfies the canonical law only if ḡu = 0.
  Capacity falsifier (frozen before any data pull): Σ̄_max = a₀/(πG) ≈ 214 M⊙/pc² (n=1,
  PAPER49's own anchor) vs ≈ 107 (n=2) — a measured lensing/edge-on sheet with
  Σ_ph ∈ (107, 214] excludes the quadratic capacity.
- **G4 (γ reduction): FAILED as frozen — kept failed on record.** Structural: the ratio
  |γ∇²P|/(u²/(a₀−u)) → (L*/r_M)² as x→0, and the frozen corner thresholds (1e-6 / 1%)
  sit at the corners' own asymptotes (3.6e-5 for 5.75pc/1kpc; 1.09% for 1kpc/10kpc).
  Physics unaffected: the γ=0 reduction holds at O((L*/r_M)²) — ≤1.09% in EVERY corner,
  ≤0.004% at the fiducial L*=5.75 pc floor; interior belongs to the argon_clues
  stiffened-tether lane (untouched). Calibration lesson #2 of the day (after AG3 K2b):
  freeze thresholds away from structural asymptotes.
- **G5 (Lean):** AG4_law_from_action.lean — **12/12 theorems, exit 0, zero proof-term
  sorry, axioms ⊆ {propext, Classical.choice, Quot.sound} for all** (T1 bridge, T2/T3
  law⇔rest-state, T4 uniqueness, T5 tether bound, T6 explicit root, T7 capacity family
  + n=2 instance + non-canonicity, T8 ARGON02 phantom mass, T9/T9b deep sandwich + root
  form). Statements sympy-prechecked before typing (G5-pre all OK); signatures grep-
  verified against the cached Mathlib (sqrt_le_iff conjunct order, pos_of_mul_pos_right).
- **Mutations as designed:** M1 capacity-2 ⇒ quadratic, NOT canonical; M2 canonical g_ph
  in the n=2 equation ⇒ residual ḡu ≠ 0; M3 positive control ⇒ residual 0.

## Kill test (of this lane's conclusion)

The derivation is void only if the frozen S2 action text is superseded (asserted verbatim
at runtime, kill test 3) or the declared premises fail: (i) Gauss for A — unassailable for
the static point source; (ii) P ∥ A at rest — could fail for rotating/non-equilibrium
configurations (not the rest state claim); (iii) γ=0 outside the screening core — G4
bounds this at ≤1.09% even for the extreme L* bound. **The empirical counterweight, stated
loud:** SPARC rotation mildly prefers the n=2 form (AG3 diagnostic: paired velocity rms
0.178 vs 0.220 dex; crossings +0.06 vs +0.49; γ cannot explain it — 10⁻⁹ at fiducial L*).
A ~16–25% Υ_disk overestimation (plausible: SPARC Υ's were fit with halo models that can
absorb phantom) fully absorbs the canonical-law gap. If a Υ-marginalized re-analysis still
prefers n=2 at ≥3σ, either the rest-state claim or the capacity needs revisiting — that
re-analysis is the pre-registered next empirical step (AG4b proposal), NOT a silent
re-derivation of the action.

## Two strongest objections

1. **"The data prefer the quadratic — theory should follow data."** The framework's claim
   (PAPER49) is that the law is DERIVED (rest state of the medium), not fitted; a 0.042-dex
   preference within a known circularity (Υ fitted from the same curves) does not overturn
   an exact derivation. But the preference is registered, quantified, and given a
   pre-registered resolution path (AG4b), not buried.
2. **"Your derivation assumes the spherical static ansatz and γ=0 — the real medium may
   rest elsewhere."** γ=0 is bounded numerically (G4) at ≤1.09% worst-case outside the
   screening core, and the core is the stiffened-tether lane's domain (certified there).
   Uniqueness is certified for the ansatz (T4); full 3-D uniqueness of the rest state is
   an open analysis problem — flagged, not claimed.

## Consequences

1. **Canonical law vindicated from the frozen action; PAPER49's rest-state claim upgraded
   from assertion to derivation (algebra Lean-certified).** S2 L21 stands.
2. **The quadratic a₀-line is a DIFFERENT theory** (half-capacity tether), not a
   transcription variant of the canonical: the user-profile program statement
   (`g_obs²−g_bar² = a₀g_bar`) and G071's validated test refer to that variant. Conductor
   must route: either the profile shorthand is corrected, or (if Carl holds the a₀-line as
   THE law) the S2 action's W_rem needs a dated v2 with capacity a₀/2 — and then PAPER49's
   ν=100.5 and Σ̄=214 anchors must change (they are n=1 numbers). This is a physics
   decision for the owner, not a lane.
3. **PAPER49/S2 mislabel:** both call ḡ=g²/(g+a₀) the "simple interpolating function";
   the algebra + ν=100.5 pin standard μ=x/(1+x). Dated-erratum proposal (label only).
4. **AG3 reinterpretation (no verdict change):** AG3 K2 bands used the quadratic
   prediction; the frozen K2b FAIL and the +0.493 canonical crossing offset both stand as
   registered; measured widths and verdict S are law-agnostic.
5. **New frozen falsifier:** Σ_ph ∈ (107, 214] M⊙/pc² in any well-measured sheet kills
   n=2 (AG4c census proposal).

**Files:** FROZEN_CRITERIA.md (93e579ec1) + AMENDMENT_A (c80cdb5fd), both pre-run ·
ag4_derive.py/.out/_results.json (MAIN, exit 1 = G4 FAILED-as-frozen on record) ·
_MUTATE.out/_results.json · AG4_law_from_action.lean/.out (12/12, axioms clean) ·
IDEA.md · README.md · HANDOFF_TO_CONDUCTOR.md.
