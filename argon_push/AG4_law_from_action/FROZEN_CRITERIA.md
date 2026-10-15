# AG4 — FROZEN CRITERIA (committed ALONE, before any derivation run)

**Lane:** `argon_push/AG4_law_from_action/` · **Date:** 2026-10-15 · **Track:** argon (interactive)
**Question (AG3 handoff §4, pre-registered branches a/b/c):** Which interpolation is the unique
static rest state of the frozen S2 action?

    L = −|∇Φ − K P|²/(2K) − ρ_b Φ − W_rem(u) − (γ/2)|∇P|²,   K = 4πG,  u = K|P|,
    K W_rem′(u) = u²/(a₀ − u),   γ = K L*²/2

This is theory-internal adjudication of the repo's law-form split (AG3 handoff §2):
canonical `ḡ = g²/(g+a₀)` (THEORY_CANONICAL S2 L21; PAPER49 ν=100.5; ARGON02) vs quadratic
`g² − ḡ² = a₀ḡ` (G071-tested; user-profile a₀-line; AG3 K2 bands).

## Pre-registered branches (unchanged from AG3 HANDOFF §4)

- **(a)** rest state = canonical/standard-μ ⇒ canonical stands; the quadratic's better SPARC fit
  (Δ = −0.042 dex paired) becomes an anomaly to explain (Υ bias ~8% absorbs quadratic residual;
  ~16–25% would be needed for canonical — recorded, not adjudicated here).
- **(b)** rest state = quadratic ⇒ THEORY_CANONICAL S2 L21 + PAPER49 get a dated v2 erratum
  (append-only), ARGON02 P2/P3 re-derive (r_e 5.843 → 6.285 r_M).
- **(c)** neither/both-in-limits ⇒ report exactly as falls.

**Hand-derivation sketch (to be machine-verified, NOT assumed):** δL/δΦ ⇒ ∇·A = 4πGρ_b with
A ≡ ∇Φ−KP (A is baryon-only; spherical point mass ⇒ |A| = ḡ = GM_b/r² by Gauss). δL/δP at
γ=0 ⇒ A = (u²/(a₀−u))P̂ with u = K|P|; ∇Φ = A+KP ⇒ g = ḡ + u (u = g_ph). Then
ḡ = u²/(a₀−u) ⇔ u² + ḡu = a₀ḡ ⇔ (with g = ḡ+u) g² = ḡ(g+a₀) — the canonical S2 law.
Branch (a) is the expected reading; the script must VERIFY the variational step honestly — if
the functional derivatives do not reproduce this, branch (c).

## Gates (all pre-registered; exit 0 iff G1–G5 pass and mutations behave as designed)

- **G1 (variational derivation):** sympy functional derivatives of the spherical static ansatz
  reproduce BOTH field equations exactly: ∇·A = 4πGρ_b and A − (u²/(a₀−u))P̂ + γ∇²P = 0
  (residual identically zero after substitution). Physics premise stated in headers: A's Coulomb
  form for a point baryon mass (Gauss) and P̂ ∥ Â at rest — NOT certified, declared.
- **G2 (rest state = canonical law):** closed form u(ḡ) = (√(ḡ²+4a₀ḡ)−ḡ)/2 on (0,a₀);
  g = ḡ+u satisfies ḡ(g+a₀) = g² identically; PAPER49 anchor |ν(ḡ=10⁻⁴a₀) − 100.5| < 0.01;
  ARGON02 P1 phantom mass M_ph/M_b = (√(1+4x²)−1)/2 exact from u (x = r/r_M); deep asymptote:
  u/√(a₀ḡ) → 1 and ρ_ph → M_b/(4πr_M r²) (A/r² with 4πGA = √(GM_ba₀)/1 = C — GF2/AG1 chain).
- **G3 (capacity family = the law-form split):** for KW_rem′ = u²/(a₀−nu): rest state
  u² + nḡu = a₀ḡ; n=1 ⇒ canonical (g² = ḡ(g+a₀)); n=2 ⇒ quadratic (g²−ḡ² = a₀ḡ) EXACTLY.
  Tether bounds: n=1 ⇒ g_ph < a₀ (Σ̄_max = a₀/(πG) ≈ 214 M⊙/pc², PAPER49's anchor number);
  n=2 ⇒ g_ph < a₀/2 (≈ 107 in the same convention). Capacity is THE structural number
  separating the two repo laws; new falsifier recorded (see Kill test 2).
- **G4 (γ reduction bound):** numeric ratio |γ∇²P|/(u²/(a₀−u)) with u = exact rest-state
  profile: < 1% for r ≥ 10 r_s, r_s = L*²/r_M (argon_clues screening radius), for
  L* ∈ {5.75 pc, 1 kpc} and r_M ∈ {1, 10} kpc; ratio diverges below r_s (stiffened-tether
  inner regime, already certified in ArgonClues.lean — AG4 must NOT touch the interior claim).
- **G5 (Lean certificate):** AG4_law_from_action.lean compiles exit 0, zero proof-term sorry,
  `#print axioms` ⊆ {propext, Classical.choice, Quot.sound} for every headline theorem.
  Theorem list (statements hand-derived above and sympy-prechecked in the SAME session before
  typing, per lean-math-certification discipline):
    T1 eom_bridge: ḡ(a₀−u) = u² ↔ u² + ḡu = a₀ḡ (polynomial, unconditional)
    T2 rest_state_to_law: u²+ḡu=a₀ḡ, g=ḡ+u ⇒ g² = ḡ(g+a₀)
    T3 law_to_rest_state: g²=ḡ(g+a₀), u=g−ḡ ⇒ u²+ḡu=a₀ḡ
    T4 rest_state_unique: u₁,u₂>0 both solving ⇒ u₁=u₂
    T5 tether_bound: u>0, ḡ>0, rest state ⇒ u<a₀
    T6 explicit_root: u₀=(√D−ḡ)/2, D=ḡ²+4a₀ḡ ⇒ u₀>0 ∧ rest state
    T7 capacity_family: u²+nḡu=a₀ḡ, g=ḡ+u ⇒ g²−ḡ² = a₀ḡ+(2−n)ḡu; corollaries n=1, n=2
    T8 phantom_mass: s²=1+4x² ⇒ u=a₀(s−1)/(2x²), ḡ=a₀/x² solve rest state ∧ x²u/a₀=(s−1)/2
    T9 deep_sandwich: √(a₀ḡ)−ḡ/2 ≤ (√(a₀ḡ+ḡ²/4)−ḡ/2) ≤ √(a₀ḡ)
  Overlap with ArgonClues.lean (nu_quadratic, gate_solves, Wrem_deriv) is COMPLEMENTARY:
  those certify the law's internal identities; AG4 certifies action-rest-state ⇔ law bridge
  and the capacity family. No theorem restated verbatim.

## Mutations (MUTATE=1; as-designed = all three fire)

- **M1:** capacity 2a₀ in W_rem′ ⇒ derived law must become the QUADRATIC (else algebra bug).
- **M2:** canonical-law g_ph substituted into the n=2 rest-state equation ⇒ residual = ḡ·g_ph ≠ 0
  symbolically (canonical is NOT the half-capacity rest state).
- **M3 (positive control):** canonical g_ph into the frozen n=1 EOM ⇒ residual exactly 0.

## Kill tests (of AG4's conclusion)

1. A sympy-checked variational error (G1 residual ≠ 0 for the frozen W_rem′) kills the branch-(a)
   reading immediately — report (c), do not patch the action.
2. Observational capacity falsifier (NEW, from G3): a well-measured lensing/edge-on sheet with
   phantom surface density Σ_ph ∈ (a₀/(2πG), a₀/(πG)] ≈ (107, 214] M⊙/pc² would exclude the
   n=2 (quadratic) capacity and confirm canonical; all measured sheets saturating below 107
   is consistent with both (no discrimination). Recipe: max-Σ_ph census over strong-lensing
   arcs + edge-on disk warps; number + range frozen here BEFORE any data pull.
3. The whole adjudication is void if THEORY_CANONICAL S2's action is superseded by a dated v2 —
   check the file's mtime/commit lineage at run time (script asserts the S2 line verbatim).

## Data/code provenance

a₀ read at runtime from `deepseek_push/G081_results.json`; S2 action text asserted verbatim
from `campaign_fresh_gravity/THEORY_CANONICAL_2026-10-14.md` (read-only); PAPER49 anchor
(ν=100.5 at g_N=10⁻⁴a₀) from `qwen_claude_field_theory/papers_2026/PAPER49_...tex` L37;
ARGON02 M_c from `argon_push/ARGON02_settled_halo_esd_2026-10-15/settled_halo_esd_results.json`.
No ledger/register touched; proposals to conductor only. Files outside argon_push/ untouched.
