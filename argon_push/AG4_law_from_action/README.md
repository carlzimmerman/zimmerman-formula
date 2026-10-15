# AG4_law_from_action — lane record

**Date:** 2026-10-15 · **Track:** argon (interactive session) · **Status: LANDED —
BRANCH (a) CONFIRMED: the unique static rest state of the frozen S2 action IS the
canonical law ḡ = g²/(g+a₀); the quadratic a₀-line is the half-capacity (n=2) variant —
a different theory. Lean 12/12 certified. exit 1 = G4 FAILED-as-frozen on record
(structural threshold miscalibration; physics bound ≤1.09% recorded loud).**

Adjudicates the repo's law-form split (AG3 handoff §2/§4) theory-internally: jet
Euler–Lagrange of L = −|∇Φ−KP|²/(2K) − ρ_bΦ − W_rem(u) − (γ/2)|∇P|² with
K W_rem′ = u²/(a₀−u) gives, at rest, ḡ = u²/(a₀−u) with u = K|P| = g_ph — equivalent to
the canonical law; capacity family u²+nḡu=a₀ḡ gives the quadratic exactly at n=2.
PAPER49 ν=100.50125 and Σ̄_max=214 M⊙/pc² anchors reproduced; ARGON02 P1 phantom mass
(s−1)/2 and density profile derived from the action; deep sandwich u ∈ [√(a₀ḡ)−ḡ/2, √(a₀ḡ)].

## Files

- `FROZEN_CRITERIA.md` (93e579ec1) + `FROZEN_CRITERIA_AMENDMENT_A.md` (c80cdb5fd) —
  both committed ALONE before the first run. AMD-A: G4 tiered bound (uniform <1% at
  10r_s miscalibrated for the L*~r_M corner) + G1 strengthened to explicit W_rem
  antiderivative + jet-total-derivative EL.
- `ag4_derive.py` / `.out` / `_results.json` — MAIN (exit 1: G4 failed-as-frozen, all
  other gates PASS; branch (a)). `MUTATE=1` → `_MUTATE.out/_MUTATE_results.json`
  (M1–M3 as designed).
- `AG4_law_from_action.lean` / `.out` — 12 theorems (T1 eom_bridge, T2/T3 law⇔rest-state,
  T4 uniqueness, T5 tether bound, T6 explicit root, T7 capacity family + T7_n2_quadratic
  + T7_n2_not_canonical, T8 ARGON02 phantom mass, T9b root form, T9 deep sandwich);
  exit 0; axioms ⊆ {propext, Classical.choice, Quot.sound} for all; zero proof-term sorry.
- `IDEA.md` — brief-format write-up. `HANDOFF_TO_CONDUCTOR.md` — register proposals,
  the law-form owner decision, erratum proposals, AG4b/AG4c spawn proposals.

## Reproduce

    python3 ag4_derive.py                      # MAIN (exit 1 = G4 on record; branch a)
    MUTATE=1 python3 ag4_derive.py             # mutations
    cd ../../fable_independent_2026/lean_2026 && \
      lake env lean ../../argon_push/AG4_law_from_action/AG4_law_from_action.lean

## Honest notes

- G4's frozen thresholds sat at the corners' structural asymptote (ratio → (L*/r_M)² as
  x→0): FAILED as frozen, NOT re-adjudicated post-run. Calibration lesson #2 today.
- The sympy subs-cascade trap (RHS containing the substituted symbol) broke four checks
  in the first run; fixed via subtract-relation form (check implementation, gates
  untouched — AG1 precedent).
- The SPARC preference for n=2 (AG3 diagnostic, 0.042 dex) is registered as the open
  empirical counterweight with a pre-registered resolution path (AG4b: Υ-marginalized
  re-analysis), NOT absorbed silently.
