# SPEC_A — Lean certificates for the NSE campaign (subagent task)

Write THREE Lean files, zero `sorry`, compile exit 0, axioms ⊆ {propext,
Classical.choice, Quot.sound}. Files land in
`/Users/carlzimmerman/new_physics/zimmerman-formula/deepseek_push/navier_stokes_attempt/lean/`.
(NOTE: the folder `lean/` may not exist yet — create it if needed.)

## Environment (already verified working)
- Toolchain: `cd /Users/carlzimmerman/new_physics/zimmerman-formula/fable_independent_2026/lean_2026 && lake env lean /abs/path/to/File.lean`
- Mathlib 4.34.0-rc2 cached. First compile of a file takes minutes — be patient; use `timeout` 600.
- PROBE FIRST, in a throwaway `/tmp/probe.lean`: `#check` every lemma you plan to use.
  Known-working recipes (from this repo's house skill): square-then-sqrt route
  (`Real.sq_sqrt`, `Real.mul_self_sqrt`, `Real.sqrt_mul_self`); `field_simp [h]`
  then `ring`; `nlinarith` needs unwrapped `0 ≤ x` hypotheses; `norm_num` only on
  RATIONAL literals (never scientific notation); `Real.pi` is the only pi name;
  lame `positivity` for `0 < x^2`-class goals; `intervalIntegral.integral_deriv_mul_eq_sub`
  exists if you need integration by parts.
- NO `sorry`, NO `admit`, NO `by_contra` fakes. If a theorem will not close after
  TWO edits: DELETE it and put the blocker statement as a `/-!` comment (named
  blocker, house style). A trimmed file that compiles beats a sorry'd full one.
- End the file with `#print axioms <thm>` for every theorem and READ the output:
  allowed = {propext, Classical.choice, Quot.sound} only; `sorryAx` present = fail.
- Linter: prefix unused variable binders with `_` (or use them).

## File 1: lean/NSE_a0line.lean  (header docstring: "the a0-line two faces, certified algebra; physics scope in the docstring")
Theorems (statements are FINAL — do not weaken; do not change variable orders;
use `noncomputable section` and `open Real` inside a section; `ℝ` = `Real`):

1. `a0cap_sq (x a : ℝ) : (x + a / 2) ^ 2 - (x ^ 2 + a * x) = a ^ 2 / 4 :`
   proof `by ring`.
2. `a0cap_bound (x a : ℝ) (hx : 0 ≤ x) (ha : 0 ≤ a) :
   Real.sqrt (x ^ 2 + a * x) ≤ x + a / 2`
   Recipe: square both sides (both nonnegative): `have h1 : (Real.sqrt (x^2+a*x))^2 ≤ (x + a/2)^2`:
   expand LHS with `Real.sq_sqrt (by nlinarith : 0 ≤ x ^ 2 + a * x)`; use `a0cap_sq`
   and `nlinarith [ha]` for `x^2 + a*x ≤ x^2 + a*x + a^2/4`; then close the square
   inequality with the appropriate `sq_le_sq`-style lemma (probe its exact name —
   maybe `sq_le_sq.mp` direction: `h: a^2 ≤ b^2` with `0 ≤ b` gives `a ≤ b`).
3. `deep_lo (a x : ℝ) (hx : 0 ≤ x) (ha : 0 ≤ a) :
   Real.sqrt (a * x) ≤ Real.sqrt (x ^ 2 + a * x)`
   Recipe: `Real.sqrt_le_sqrt`-class (probe name/signature) with `nlinarith : a*x ≤ x^2 + a*x` (from `0 ≤ x^2`).
4. `deep_hi (a x : ℝ) (ha : 0 < a) (hx : 0 ≤ x) :
   Real.sqrt (x ^ 2 + a * x) ≤ Real.sqrt (a * x) * (1 + x / (2 * a))`
   Recipe: square both sides (both sides ≥ 0). RHS squared: `(Real.sqrt (a*x)*(1+x/(2*a)))^2`
   = `a*x*(1+x/(2*a))^2` via `Real.sq_sqrt (by nlinarith : 0 ≤ a*x)` + `mul_pow`.
   Show `a*x*(1+x/(2*a))^2 ≥ x^2 + a*x` by expanding with `field_simp [ha.ne']` then
   `nlinarith [hx]` (the difference is `x^3/(4a) ≥ 0`). Then square-inequality step
   as in (2). NOTE: keep `(1 + x / (2 * a))` OUTSIDE the sqrt (do not fold into the radicand).
5. `a0line_exact (a x : ℝ) : (Real.sqrt (x ^ 2 + a * x)) ^ 2 = a * x + x ^ 2`
   (statement-level identity; if it needs `0 ≤ x^2+a*x` as an argument, add `(h : 0 ≤ x ^ 2 + a * x)`; adjust the deep_hi proof to provide it via nlinarith from its own hypotheses).
6. `newtonian_face (a g : ℝ) (N : ℝ) (hN : 0 < N) (hg : 0 ≤ g) (hbound : N * a ≤ g) :
   Real.sqrt (g ^ 2 + a * g) ≤ g * (1 + 1 / (2 * N))`
   Recipe: square (both ≥ 0); LHS² `= g^2 + a*g` (Real.sq_sqrt + nlinarith);
   RHS² `= g^2*(1 + 1/(2*N))^2`. Need `g^2*(1+1/(2*N))^2 ≥ g^2 + a*g`:
   from `hbound`: `a ≤ g/N` (division allowed: `g/N ≤ ...`; use `field_simp [hN.ne']` then nlinarith on `N*a ≤ g`).
   Difference = `g^2/N + g^2/(4*N^2) - a*g ≥ 0` (nlinarith once cleared of divisions).
7. `face_1e16 (a g : ℝ) (ha : 0 ≤ a) (hg : 0 ≤ g) (hbound : (10:ℝ)^16 * a ≤ g) :
   Real.sqrt (g ^ 2 + a * g) ≤ g * (1 + 1 / (2 * (10:ℝ)^16))`
   Instantiate (6) with `N := (10:ℝ)^16`; `have hN : 0 < (10:ℝ)^16 := by norm_num`.
8. `window_lower_cleared (eta eta_c : ℝ) (h1 : 0 < eta_c) (h2 : eta_c * 3500 ≤ eta * 203) :
   (3500 / 203 : ℝ) ^ 2 ≤ (eta / eta_c) ^ 2`
   Recipe: from `h2` and `h1`, derive `3500/203 ≤ eta/eta_c` by `field_simp [h1.ne']` →
   `nlinarith`; square both sides (both nonnegative) — probe the right `sq_le_sq`
   direction. (This is the cleared form of: `eta ≥ 7/2` and `eta_c ≤ 203/1000` ⇒ ratio ≥ 3500/203.)
   You MAY also state and prove the composed version:
   `window_ratio (eta eta_c : ℝ) (h1 : 0 < eta_c) (h2 : 7/2 ≤ eta) (h3 : eta_c ≤ 203/1000) :
   (3500 / 203) ^ 2 ≤ (eta / eta_c) ^ 2` — derive `eta_c * 3500 ≤ eta * 203` by `nlinarith`, then reuse.
9. `window_suppression (w : ℝ) (hw : 255 ≤ w) : (1 + w)⁻¹ ≤ 1 / 256`
   Recipe: `have h1 : 0 < 1 + w := by nlinarith`; `field_simp [h1.ne']` then `nlinarith [hw]`.
   Then the composite: `window_exit (eta eta_c : ℝ) (h1 : 0 < eta_c) (h2 : 7/2 ≤ eta)
   (h3 : eta_c ≤ 203/1000) : (1 + (eta / eta_c) ^ 2)⁻¹ ≤ 1 / 256`
   (= S(3.5 floor, eta_c = 0.203-edge): the S-kernel suppression at the window exit is
   ≥ 1 − 1/256 ≈ 99.6%; norm_num on the rational `(3500/203)^2` should confirm `255 ≤ (3500/203)^2`
   — probe whether norm_num closes it, else add a `have hnum : 255 ≤ (3500/203:ℝ)^2 := by norm_num`
   step and compose via `window_ratio` + `window_suppression`.)

## File 2: lean/NSE_vector_core.lean (the sup-argument algebra)
1. `adv_energy_swap (u du : Fin 3 → Fin 3 → ℝ) :
   (∑ i, u i * (∑ j, u j * du j i)) = (∑ j, u j * (∑ i, u i * du j i))`
   Proof: `simp [Finset.sum_mul, Finset.mul_sum, Finset.sum_comm]`-class; `ring` if needed.
   Docstring: pointwise algebraic core of `u·((u·∇)u) = ½(u·∇)|u|²` (the chain-rule
   half is calculus — cited, not certified here).
2. `inner_cross_zero (u v : EuclideanSpace ℝ 3) : ⟪u, u × v⟫ = 0`
   `open scoped RealInnerProductSpace` and `open scoped EuclideanSpace` at the top;
   `×` is crossProduct. Probe: `#check Real.inner_cross_self` — if it exists use it;
   else prove by components: `simp [inner, crossProduct, Finset.sum_mul, Finset.mul_sum]`
   plus `ring`. Docstring: `(ω×u) ⊥ u` — the nondissipative part of the convective term,
   the reason the drag-only mechanism can be capped pointwise.
3. `norm_sq_add_cross (u v : EuclideanSpace ℝ 3) : ⟪u + v, u + v⟫ = ⟪u,u⟫ + 2*⟪u,v⟫ + ⟪v,v⟫`
   (bilinearity; `simp [inner_add_left, inner_add_right, inner_smul_right]`-class — probe
   `inner_add_left`. Docstring: superset-bookkeeping for the sup-estimate.)
   If this one fights you, drop it (delete) — it is NOT load-bearing; (1),(2) are.

## File 3: lean/NSE_barrier.lean (the invariant-set rungs for the sup barrier)
1. `barrier_factor (A c M m : ℝ) (hm2 : m ^ 2 = A / c) : A - c * M ^ 2 = -c * (M - m) * (M + m)`
   Recipe: `rw [← hm2]` on `A`? Better: `linear_combination` or: have `hA : A = c*m^2` by
   `rw [hm2]; field_simp`; then `rw [hA]; ring`.
2. `barrier_eq_at_crossing (A c m : ℝ) (hc : c ≠ 0) (hm2 : m ^ 2 = A / c) : A - c * m ^ 2 = 0`
   (the crossing point feels no upward force). `rw [hm2]; field_simp [hc]`.
3. `barrier_pull_down (A c M m : ℝ) (hc : 0 < c) (hm : 0 ≤ m) (hm2 : m ^ 2 = A / c) (hM : m ≤ M) :
   A - c * M ^ 2 ≤ -c * m * (M - m)`
   Recipe: from (1): `A - c*M^2 = -c*(M-m)*(M+m)`; since `m ≤ M+m` (from `hm`) and `M-m ≥ 0`
   (linarith from hM), `-c*(M-m)*(M+m) ≤ -c*(M-m)*m`; `nlinarith [hc, hM, hm]` on the rearranged
   form. This is the rung: ABOVE the barrier the a-priori sup-derivative is strictly negative.
4. `drag_beats_stretching_never (a C : ℝ) (ha : 0 < a) (hC : 0 < C) :
   ∃ ω : ℝ, Real.sqrt (a / C) < ω ∧ C * ω ^ 3 > a * ω`
   Witness `ω := 1 + a / C`. Show `C*(1+a/C)^3 > a*(1+a/C)` by `nlinarith [ha, hC]`
   (difference = C + 2a + a^2/C + ... positive — expand by `ring` after clearing divisors
   with `field_simp [hC.ne']`); show `√(a/C) < 1 + a/C` via the square-route
   (`(1+a/C)^2 - a/C = 1 + a/C + (a/C)^2 > 0`; `nlinarith`; then sqrt-square inequality).
   Docstring: the stretch-vs-drag COUNT: a drag linear in the norm (the a0-only class)
   cannot dominate the cubic stretching at every level — the canonical reason the
   two-constant drag class cannot close 3D regularity (N02 door).
5. (OPTIONAL, cheap only) If Mathlib's Gronwall (`Mathlib.Analysis.ODE.Gronwall`)
   has a form you can apply in ≤ 2 probes to `E' ≤ -k*E ⇒ E(t) ≤ E(0)`, state and prove
   `barrier_decay`. Otherwise: put the blocker as a `/-!` docstring (named blocker:
   "full ODE comparison certified in N03 lane; algebraic rungs (1)-(4) certified here").

## House rules
- Docstring at top of each file: what is certified (algebra only) and what is physics
  (the a0-line itself is MEASURED — the Lean certifies the mathematics of the law's
  consequences, not that nature obeys it).
- `#print axioms` for each theorem at file end (after `end` of the section).
- Do NOT edit anything else in the repo. No git. No absolute paths inside files.
- Report back: per-file exit code, the `#print axioms` lines, and any theorem you
  deleted with the blocker note. Be honest: a theory that does not compile is a FAIL.
