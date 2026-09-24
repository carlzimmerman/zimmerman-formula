# N03 — SMALL ALGEBRAIC SPINE: LEAN VERDICT

**2026-09-23 · lane: fable_independent_2026/lean_2026/N03_small_spine.lean · exit 0 · zero sorry · axioms exactly {propext, Classical.choice, Quot.sound}**

Toolchain: Lean 4.34.0-rc2, `lake env lean N03_small_spine.lean` from
`fable_independent_2026/lean_2026/` (cached mathlib oleans), compile ≈ 5 s,
exit code 0.  Axiom check: unfiltered `#print axioms` for all 26
theorems/lemmas at the end of the file — every line prints
`[propext, Classical.choice, Quot.sound]`, zero `sorryAx`, zero `sorry` in the
proof surface (the only occurrence of the word is the docstring's "zero
`sorry`" statement).  Nothing touches I21–I24 or M01; no git commit.

Pre-certification algebra verified exactly with sympy (this session): kernel
moments, the M05 quadrature values, and the exact polynomial cores of the 2D
reduction — the values below are hand-checked before being stated in Lean, and
the Lean statements were re-checked against the numeric anchors quoted.

Classification legend: **CERTIFIED** = Lean theorem, proof complete, axioms
clean.  **CONJECTURED-WITH-NUMERIC-EVIDENCE** = formally stated in Lean as a
`def : Prop` (compiles, zero axioms), no proof given because the 2D
change-of-variables theorem required is not in this toolchain's mathlib; backed
by the quadrature evidence quoted verbatim.

---

## 1. Thomson-kernel moments (L01, N = 1 sector)  — ALL CERTIFIED

Kernel: `thomsonKernel μ = (3/8)(1+μ²)`, μ ∈ [−1,1], normalized so
∫ p dμ = 1.  The L01 anchor and friends:

| theorem (namespace N03) | statement | status |
|---|---|---|
| `n03KernelNormalized` | `∫₋₁¹ (3/8)(1+μ²) dμ = 1` — the kernel is a probability density | CERTIFIED |
| `n03MeanMu` | `∫₋₁¹ (3/8)(1+μ²)·μ dμ = 0` — E[μ] = 0 (base of the L02 exact fact E[d_j] = 0 for j < N) | CERTIFIED |
| `n03FirstMoment` | `∫₋₁¹ (3/8)(1+μ²)(1−μ) dμ = 1` — E[1−μ] = 1 (base of E[ang] = E[N]) | CERTIFIED |
| `n03SecondMoment` | **`∫₋₁¹ (3/8)(1+μ²)(1−μ)² dμ = 7/5`** — E[(1−μ)²] = 7/5, THE L01 N=1 anchor | CERTIFIED |
| `n03SecondMomentHalf` | `½·∫ … = 7/10` — the literal "½ × the integral" value | CERTIFIED |
| `n03SecondMomentHalfNotSevenFifths` | `½·∫ … ≠ 7/5` — certified REFUTATION of the ½-phrasing (the ½ does not belong; the kernel already sums to 1) | CERTIFIED |
| `n03ChordMuLinearVanishes` | `∫₋₁¹ rμ dμ = 0` — μ-linear chord part integrates to zero | CERTIFIED |
| `n03R1q` | `E[(1−μ)²]·(1/2 + q/4) = (7/5)(1/2 + q/4)` — the r₁(q) coefficient | CERTIFIED |
| `n03L01RatioLead` | `(τ₀·(7/5)(1/2+q/4))/((τ₀(1/2+q/4))·(τ₀(1+q/3))) − 1 = (7/5)/(τ₀(1+q/3)) − 1` for τ₀≠0, (1/2+q/4)≠0, (1+q/3)≠0 — the thin ratio R−1 = (7/5)/[(1+q/3)τ₀] − 1 + O(1) leading term | CERTIFIED |

Answer to the task's check "does ½·∫(3/8)(1+μ²)(1−μ)² dμ = 7/5?": **NO** —
the ½-sealed integral is 7/10 (certified), and the UNSCALED normalized-kernel
expectation integral is exactly 7/5 (certified).  E[(1−μ)²] = 7/5 stands.

## 2. The M05 first-flight moments and the chord substitution  — 1D tails CERTIFIED, 2D statements CONJECTURED

The volume-source moments (M05_FIRST_FLIGHT_MOMENTS.md, Legendre ladder:
ng=1024 → ⟨chord⟩ 0.7500000000003, E[∫r²ds] 0.41666666667, E[∫r⁴ds]
0.25000000000) reduce, after the change of variables (r,μ) ↦ (u,w) =
(rμ, r√(1−μ²)) on the quarter unit disk and the μ-odd integration (certified
piece `n03ChordMuLinearVanishes`), to one-dimensional POLYNOMIAL integrals.
The full 2D moment statements stay CONJECTURED — no 2D change-of-variables
theorem exists for mathlib interval integrals in this toolchain (verified
against the cached oleans: no `integral_pow`, no `integral_id`, no
integrability closure for sums; the FTC route used is
`intervalIntegral.integral_deriv_eq_sub'`).  Everything polynomial is certified:

| theorem (namespace N03) | statement | status |
|---|---|---|
| `n03M05ChordCore` | `∫₀¹ w(1−w²) dw = 1/4` — the chord/r⁴ core | CERTIFIED |
| `n03M05ChordTimesThree` | `3·∫₀¹ w(1−w²) dw = 3/4` — ⟨chord⟩_vol modulo the single 2D step | CERTIFIED |
| `n03M05R2Core` | `∫₀¹ w(1−w²)(1+2w²) dw = 5/12` — E[∫r²ds] core | CERTIFIED |
| `n03M05R4Core` | `∫₀¹ w(1−w²)(1−2w²+4w⁴) dw = 1/4` — E[∫r⁴ds] core | CERTIFIED |
| `chordMomentConjecture : Prop` | `chordMomentVol = 3/4` (formal def, zero axioms) | CONJECTURED-WITH-NUMERIC-EVIDENCE |
| `m05R2Conjecture : Prop` | `m05R2Mom = 5/12` (formal def, zero axioms) | CONJECTURED-WITH-NUMERIC-EVIDENCE |
| `m05R4Conjecture : Prop` | `m05R4Mom = 1/4` (formal def, zero axioms) | CONJECTURED-WITH-NUMERIC-EVIDENCE |

The exact error/blocker: the reduction step `∫∫_{quarter disk} … du dw =
∫₀¹ … dw` requires a 2D substitution theorem for `intervalIntegral`
(change of variables on compact rectangles/quarter disks), which is not in
this build's cached mathlib; no workaround within the allowed toolkit was
found (the μ-inner integral for fixed r is elliptic — √(1−r²+r²μ²) — so no
1D-polynomial route exists).  Quadrature evidence for the conjectures:
M05 ladder quoted above; J11 anchor "⟨chord⟩_vol = 0.750000 exactly"
(quadrature ng=80).

## 3. The Q-decomposition (L02), N = 1 sector  — ALL CERTIFIED

Definitions over an inner product space: `qFull N l u = ∑_{j=0}^{N} ℓ_j (u_j·u_N)`.

| theorem (namespace N03) | statement | status |
|---|---|---|
| `qSplit` | `qFull N l u = ℓ_N·(u_N·u_N) + ∑_{j<N} ℓ_j (u_j·u_N)` — split off the final segment | CERTIFIED |
| `dotSelfUnit` | `‖u‖ = 1 → ⟪u,u⟫ = 1` — unit direction dots itself to 1 | CERTIFIED |
| `qDecomp` | `‖u_N‖ = 1 → qFull N l u = ℓ_N + ∑_{j<N} ℓ_j (u_j·u_N)` — the L02 decomposition | CERTIFIED |
| `qN1` | `qFull 1 l u = ℓ₀·(u₀·u₁) + ℓ₁·(u₁·u₁)` — N=1 algebra, general final direction | CERTIFIED |
| `qN1Unit` | `‖u₁‖ = 1 → qFull 1 l u = ℓ₀·(u₀·u₁) + ℓ₁` — the N=1 headline, two-line algebra | CERTIFIED |

## Summary of counts

- Certificates: **26 Lean theorems/lemmas CERTIFIED**, exit-0 on the single
  file, `#print axioms` clean on every one (exactly
  {propext, Classical.choice, Quot.sound}).
- Conjectures: **3** (`chordMomentConjecture`, `m05R2Conjecture`,
  `m05R4Conjecture`) — CONJECTURED-WITH-NUMERIC-EVIDENCE (formal `def : Prop`,
  zero axioms), the 2D change-of-variables blocker named exactly.
- `sorry` count: 0 (proof-surface grep clean; no `admit`, no `sorryAx` in the
  unfiltered compile log).  Axioms: exactly {propext, Classical.choice,
  Quot.sound} on all 26 printed axiom lines.
- Files: `fable_independent_2026/lean_2026/N03_small_spine.lean` (written),
  `deepseek_push/N03_SMALL_SPINE_VERDICT.md` (this file),
  `deepseek_push/N03_results.json`.  No git commit; I21–I24 and M01 untouched;
  scratch probes `_probe_n03*.lean/.py` removed.  The K04 inversion bijection
  was NOT re-done (already certified as M01).