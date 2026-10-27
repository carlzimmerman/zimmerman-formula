# Q010_kappa_referee — lane record

**Date:** 2026-10-15 · **Track:** qwen38 (closure track) · **Status: LANDED — VERDICT:
UPHELD-QUALIFIED.** All gates PASS (MAIN exit 0, MUTATE exit 0, Lean exit 0, 10/10
theorems, zero sorry, axioms ⊆ {propext, Classical.choice, Quot.sound}).

Referee of the pending GF2 register-upgrade ("κ=½: DERIVED as the closure coefficient"),
opened on the owner request: *the nature of cold energy and dark energy without any
assumptions.* Frozen criteria committed alone pre-run (0eb0b4d078).

## Verdict (pre-registered vocabulary)

**UPHELD-QUALIFIED**, exact reading:

> κ = ½: **DERIVED as the closure coefficient of the dynamical face** — three independent
> routes: GF2 closure algebra (γ=2 forced by Poisson on the log branch; σ²=C/2 forced by
> hydrostatics; re-derived independently here, J1/J2), Q001 constitutive EOS (Lean),
> Q007 amplitude identity (Lean). **Germ face tied by the exact κ=1/n web** (J3 re-derived;
> underdetermined by ONE integer — GF1 V2, 0/6 pins). **Cross-face identification =
> rung 5** (equilibrium identification "halo=phantom, coefficient 1" — THEORY.md L64,
> POSTULATED-CARRIED) + the triad line (HORIZON-BTFR L58, IDENTIFICATION-CARRIED,
> "fitted" → now derived on the dynamical leg). **Value anchored empirically at 0.06%:**
> n_germ = 2.000102 ± 0.017235, three channels (germ tie, SPARC slope 155 curves,
> BTFR b=1.004±0.011) + GF1's registered lockstep falsifier (>3σ split kills).

**The single door to UPHELD-FULL:** derive rung 5 from S2 + a relativistic completion
(canonical §3 open item). M3 mutation demonstrates the qualification is load-bearing:
drop the identification and the verdict degrades to IDENTIFIED, as pre-registered.

## Gate results

- **J1 PASS** — ∇²(C ln r) = C/r² exact; ρ = C/(4πG)r⁻² forced; σ² = C/2; κ_dyn = ½.
  Registered controls reproduced: σ(6.5e10) = 119.21 km/s (119.2), σ(1e11) = 132.76 (132.76).
- **J2 PASS** — γ=2 unique: defect identically zero at γ=2 (C tied), non-identical otherwise;
  two-point Poisson argument 2^(−γ)=1/4 solved uniquely by γ=2 (strict monotonicity).
  Form-vs-content note: GF2's printed closed form −4πGA(2−γ)r^(1−γ) is a flux-tied
  grouping; the iff CONTENT is what was verified and is what the lemma claims.
- **J3 PASS** — web identities exact (κ=a₀/s=1/n; Z²=n²·8π/3; Ω_Λ; boundary); numeric
  battery at registers: germ ratio 4.000406, Z 5.789104, cH₀/a₀ 6.994651 — all reproduced.
- **J4 PASS** — nine junction links, every citation verified VERBATIM at runtime
  (rung 5, rung 4 status, triad line, G002 chassis, GF1 H2 tie-honesty, GF2 border 3,
  Q007 Lean, Q001 Lean, Q007 py-traceback lane-state fact). No link silently promoted;
  no ½ import found in the closure premises (GF2's 0/4 ledger stands).
- **J5 PASS** — NEW relations, zero new assumptions: capacity–DE Σ̄_max = a₀/(πG) =
  κc√(ρ_DE/G)/π (exact; κ=½ ⇒ 213.8 M⊙/pc² = PAPER49's anchor; half-capacity ⇒ 106.9);
  zero-mode shift invariance exact (deriv(f+c)=deriv f; f(0) moves 1:1).
- **J5-pre PASS** — all Lean statements sympy-prechecked before typing.
- **J6 PASS** — lean/Q010_kappa_closure.lean: L1/L2 log-branch derivatives (the
  "textbook" facts GF2 left as prose), L3 Laplacian, L4 Poisson coefficient, L5
  hydrostatic forcing σ²=C/2, L6 two-point uniqueness γ=2 (log-injectivity), L7 germ
  identity, L8 capacity–DE cleared, L9 shift invariance, L10 κ=1/γ mutation backbone.
- **J7 PASS** — M1 γ=2.1: defect ≠ 0, κ=0.4762 = GF2's registered MUTATE value (2.38%
  off ½, cross-lane control); M2 n=3: Z=8.68 vs 5.79, boundary 10.49 vs 6.99 — web is a
  point, not a basin; M3: rung-5 removal degrades verdict to IDENTIFIED as designed.

## Assumption ledger (owner deliverable, full table in q010_results.json + MAIN .out)

Cold energy: medium postulates (S2/S3) POSTULATED · rest state=law, capacity u<a₀,
uniqueness, cored halo DERIVED+LEAN (AG4/T8) · γ=2+σ²=C/2 self-source DERIVED (this lane) ·
supply 5.364 MEASURED · attractor NUMERIC · native mass 2.24 meV DERIVED-from-constants ·
aether-like (massive-particle reading DEAD 26×) · S4 second population POSTULATED (tension) ·
Ω_c/Ω_b DERIVATION OPEN · L* BOUNDED-not-derived.
Dark energy: local invisibility (C₀) THEOREM · cosmic tracking MEASURED · tie EMPIRICAL
(0.06%) · zero mode DEAD (|c|<0.02, shift-invariance Lean L9) · w=−1 DERIVED-IN-CHASSIS
(G002) not from S2 · a₀(z) SEALED (ALMA 11-06/28) · S5 optional branch FRB-bounded.
Bridge: κ_dyn=½ DERIVED×3 (2 Lean) · κ_germ=1/n exact algebra · JUNCTION = rung-5
POSTULATED-CARRIED · n=2 theory+data (2.000102±0.017235) · transport exponent-only.

## Conductor proposals (append-only; nothing outside qwen38_push/ touched)

1. Register line for κ=½: replace "MEASURED, not derived" (canonical S1 L13) reading with
   the UPHELD-QUALIFIED verdict text above, DATED, citing this lane + 5b173a046 + Q001/Q007.
2. GF2 "pending referee" → "refereed UPHELD-QUALIFIED (Q010, 2026-10-15)".
3. Open door registration: **rung-5 derivation from S2 + relativistic completion** = the
   remaining step to an unqualified κ=½ derivation (joins §3's relativistic-completion item).
4. New falsifier on the books (from AG4, re-anchored here): Σ_ph ∈ (107, 214] M⊙/pc² in
   any well-measured sheet excludes the half-capacity (n=2-law) variant — L8 Lean-certified.

## Files

FROZEN_CRITERIA.md (0eb0b4d078, pre-run) · q010_referee.py · q010_referee.out /
q010_results.json (MAIN, exit 0) · q010_referee_MUTATE.out / q010_results_MUTATE.json
(exit 0) · ../lean/Q010_kappa_closure.lean / .out (exit 0) · README.md (this file).

## Reproduce

    python3 q010_referee.py            # MAIN  (exit 0)
    MUTATE=1 python3 q010_referee.py   # J7    (exit 0)
    cd ../../fable_independent_2026/lean_2026 && \
      lake env lean ../../qwen38_push/lean/Q010_kappa_closure.lean   # exit 0
