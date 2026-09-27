# Z6-WAVE BRIEF — conductor tick 2026-09-27 ~14:5x EDT
Doors (all from on-disk registers; none rehash a KILLED door):
1. **LR3** — M01 Lean lane / M-roads roadmap: the M05 first-flight moment triple
   (chord, E∫r², E∫r⁴) + the r⁶ candidate were UNCERTIFIED (M05_FIRST_FLIGHT_MOMENTS.md
   "Registered OPEN"; M01_alg_spine.lean §6 records chord 3/4 as
   CONJECTURED-WITH-NUMERIC-EVIDENCE, blocker "2D change-of-variables not in mathlib").
   Conductor pre-audit this tick (verified numerically + symbolically, re-derived by
   lane R0): the (u,v)=(impact-parameter, depth) reduction makes EVERY moment a pure
   POLYNOMIAL 1D integral: chord = 3/4, E∫r² = 5/12, E∫r⁴ = 17/60, E∫r⁶ = 149/700.
   **M05's I2 table entry (1/4) is a polynomial-coefficient BUG** (their I2 code halves
   the s² and s³ coefficients: (2R²MU²+R²)/3 vs correct (4R²MU²+2R²)/3; R·MU·cord⁴/2
   vs correct R·MU·cord⁴). Their I3 code is correct and its candidate 149/700 is
   CONFIRMED exact. M01's recorded blocker (2D CoV) is BYPASSABLE via two iterated 1D
   substitutions (v=rμ linear; u=√(r²−v²) with r dr = u du).
2. **M05B** — independent audit of the I2 bug + blast radius (fix-forward; M05's
   buggy row stays in history, corrected on top).
3. **MC1** — c₀(q) linearity (M05-I's registered open piece: "the remaining open
   piece is c₀(q) itself").

House rules 1–10 (LOOP_CONDUCTOR.md) bind every lane. No lane touches another's
files. Honest FAILs verbatim. No SE re-tuning. exit 0 only on real passes.

## Pre-registered kill conditions (fixed before any run)
- LR3 gates: G1 = Lean zero-sorry certificates of the four polynomial-value theorems
  (3/4, 5/12, 17/60, 149/700) with axioms ⊆ {propext, Classical.choice, Quot.sound};
  G2 = the reduction lemma ((r,μ) iterated integral = reduced 1D polynomial form)
  discharged in Lean. **exit 0 iff G1 AND G2.** If G2 cannot be discharged, bank G1
  + the conditional form and exit 1 recording the precise blocker (fix-forward of
  M01 §6's status). R0 = lane's own sympy re-derivation must reproduce all four
  rationals; any mismatch = exit 1, no Lean leg.
- M05B gates: R0 = M05's own I2 polynomial under correct-domain quadrature must
  reproduce their table value 1/4 (mechanism identification); R1 = independent
  direct ray-integration MC (midpoint m=256, n=2e6, fresh seeds) for I1/I2/I3 with
  the SE from the MC itself; R2 = lane's own sympy derivation. Verdict
  I2-BUG-CONFIRMED iff R0 ∈ 1/4 ± 1e-6 AND |z(I2_mc − 17/60)| ≤ 3 AND R2 = 17/60.
  **Kill: if R1 confirms 1/4 instead, the conductor's reduction is wrong — record
  I2-CONFIRMED-1/4 verbatim and exit 1** (honest either way).
- MC1 gates: P0 = parse M05_geometric_anchors.out stored c₀ at q ∈ {0,3,10}; fresh
  measurements |z| ≤ 3 at each (parity, loaded not transcribed). M1 = c₀ at
  q ∈ {0,1,3,6,10}, τ₀=1e-3, n=1.5e6, seeds 901–905; weighted LS fit on {0,1,3},
  PREDICT {6,10}. **LINEAR-BANKED iff both |z_pred| ≤ 3; c0-NOT-LINEAR if any
  |z_pred| > 3.** No budget re-tuning; verdict recorded honestly either way.

## Barred (register): SPARC-deep deficit sizing; V04 factorized N=1 route; N01
density-locality; U-band-rule rehash (A-chain CLOSED); Q-closure family search
(QF4 structural, CLOSED); ai_slop/autoresearch_v3; KILLED doors.

## AMENDMENT (conductor, 2026-09-27 14:5x EDT, BEFORE any lane run — appended, original gates above preserved)
LR3's G2 is refined, still before any number exists: G2a = the LINEAR substitution
step (v = rμ, ∫₋₁¹H(r√(1−μ²),rμ)dμ = (1/r)∫₋ᵣ^r H(√(r²−v²),v)dv) certified zero-sorry;
G2b = the full reduction discharge (triangle swap + u=√(r²−v²) substitution). LR3
exits 0 iff G1 AND G2a (real certified components); G2b is attempted and its outcome
recorded verbatim — if discharged the verdict is CERTIFIED-FULL, else
CERTIFIED-G1-G2a-REDUCTION-OPEN with the precise blocker. Rationale: a blind full
discharge of the triangular Fubini + singular-endpoint substitution is a
multi-iteration Lean fight; banking G1 + G2a honestly beats fabricating G2b.

## AMENDMENT 2 (conductor, 2026-09-27 14:5x EDT, still BEFORE any lane run)
LR3 is split: LR3 = R0 + G1 only (polynomial-value certificates; exit 0 iff R0 AND G1);
LR3b = G2a (linear substitution step) + G2b (conditional reduction theorems deriving
chord 3/4, E∫r² 5/12, E∫r⁴ 17/60 from the stated CoV hypothesis, zero-sorry) + the
full-discharge attempt recorded verbatim. LR3b exits 0 iff G2a AND the conditionals;
verdict CERTIFIED-CONDITIONAL-FULL if G2b discharged on top, else CERTIFIED-G2a-CONDITIONAL.
Original amendment-1 exit rule (exit 0 iff G1 AND G2a) is preserved across the split:
the wave banks G1+G2a jointly, on two files, no gate weakened.

## AMENDMENT 3 (conductor, 2026-09-27 ~15:2x EDT, BEFORE the M05B re-run; runs 1-2 preserved verbatim in M05B_r4_bug_audit.out)
R0 outcome (both runs, on disk): M05's committed I2 polynomial under correct-domain
quadrature integrates to 0.1250000001, NOT their table's 0.2500000014 -- the
table's provenance is UNRESOLVED (earlier committed code, not recoverable from the
.py alone). Re-scope: the VALUE correction E[int r^4 ds] = 17/60 rests on R1
(independent direct ray-integration MC, z = +0.20) + R2 (mechanical sympy from the
definition) -- both PASS. M05B exits 0 iff R1 AND R2; R0's outcome (provenance
UNRESOLVED, mechanism-match claim RETRACTED) is recorded verbatim in the verdict.
Amendment note: runs 1-2's verdict string claimed "R0 mechanism match" -- retracted
by this amendment; the corrected verdict string supersedes it in the register.
