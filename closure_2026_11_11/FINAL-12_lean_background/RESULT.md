# FINAL-12 (LEAN-BACKGROUND) — result

**Verdict: compiled, exit 0, 30 theorems, zero `sorry`, axioms ⊆ {propext, Classical.choice, Quot.sound}.**

Artifacts (this lane, all new):

* `FINAL12_background_conservation.lean` — the certificate (namespace `FINAL12`, 30 theorems).
* `FINAL12_background_conservation.out` — the compile log: warnings only (unused-tactic/unused-simp lints),
  `EXIT=0`, and the 30 `#print axioms` lines (every one reads
  `[propext, Classical.choice, Quot.sound]`; no `sorryAx`).
* `f12_sym.py` scratch precheck: every identity below was verified symbolically in sympy before it was
  written as a Lean statement.

Compile command (reproduce from the repo root; the project's cached Mathlib is reused via `LEAN_PATH`):

```bash
cd fable_independent_2026/lean_2026
LP=$(for d in .lake/build/lib/lean .lake/packages/*/.lake/build/lib/lean; do [ -d "$d" ] && printf '%s:' "$(cd "$d" && pwd)"; done)
env LEAN_PATH="${LP%:}" lean ../closure_2026_11_11/FINAL-12_lean_background/FINAL12_background_conservation.lean
```

## Statement-by-statement: what is certified, and where it differs from the lane target

1. **FRW EOS** — `frw_eos_quadratic` (the exact quadratic `w = x/(2+x)` at `xbar(a) = I0/(2 mu^2 a^3)` is
   `w0/(w0+a^3)`, `w0 = I0/(4 mu^2)`), `wFRW_lt_half_iff` (`w < 1/2 ⟺ a^3 > w0`), `wFRW_strictly_decreasing`,
   `wFRW_tendsto_zero` (ε–A form, witness `A = w0/eps + 2`). Supporting: `Vquad_deriv`, `quad_background`,
   `one_lt_cube`. **All three requested properties hold exactly as stated, with I0 > 0, mu > 0, a > 0.**
2. **Coldness / sound speed** — `cs2_quadratic` (`n/n' = x`, epoch-independent), `cad2_quadratic`
   (exact `dp/dρ = x/(1+x) = (Qbar-1)/Qbar`), `eos_quadratic` (exact `w = (Qbar-1)/(Qbar+1)`),
   `quad_cs_minus_w` (`c_ad^2 - w = x/((1+x)(2+x))`); exponential: `cs2_exponential` (`n/n' = x_T` exactly,
   at every epoch), `cad2_exponential` (`x_T/Q`), `eos_exponential` (`x_T/(Q - x_T)`),
   `exp_w_minus_cs2` (`w - c_ad^2 = x_T^2/(Q(Q-x_T))`).
   **CORRECTIONS (both are DT2 §5's findings, now machine-checked):**
   - the target's `w = Qbar - 1` is **false**; the exact equation of state is `w = (Qbar-1)/(Qbar+1)` and the
     exact adiabatic speed is `(Qbar-1)/Qbar`. DT1's `c_s^2 = x` is the leading order of the latter.
   - the exponential term is **not exactly isothermal**: `n/n' = x_T` is exact as a ratio, but the adiabatic
     speed is `x_T/Q` and the equation of state is `x_T/(Q - x_T)`; both keep their Q-dependence.
   - consistency check: the target's own item (1), `w = w0/(w0 + a^3)`, follows from the exact
     `w = x/(2+x)`, not from `w = x` (which would give a pure `a^-3` law). Item (1) is therefore consistent
     with the exact w and inconsistent with `w = Qbar - 1`.
3. **Jeans wavenumber** — `kJ2_quadratic` / `kJ2_quadratic_value`: `k_J^2 = mu^2 (1 + xbar/2)(1 + xbar)`
   `= mu^2 + mu^2 xbar(3+xbar)/2`, and `kJ2_quadratic_gt_mu2`: strictly **larger** than `mu^2` for every
   `xbar > 0`. So `k_J^2 = mu^2` (constant) is only the dust limit `xbar -> 0`, not an identity along the
   background. `kJ2_exponential` / `kJ2_exponential_ratio`: `k_J^2 = Q(Q - x_T) n'(xbar)` with
   `n'(xbar) = nbar/x_T` — density-dependent, as the target says, up to the factor `Q(Q - x_T) ≈ 1`.
4. **Trade-off** — `tradeoff_two_point` (the two-point estimate `k^2 (x_b - x_a) <= n(x_b) - n(x_a)`,
   proved from monotonicity of `y ↦ n y - k^2 y`, i.e. the mean value theorem),
   `tradeoff_span` (`x_b - x_a <= (n_b - n_a)/k^2` after dividing by `k^2 > 0`), and
   `tradeoff_cap_conflict` (the well-cap contradiction). **Formalized in the discrete two-point form the
   lane permits; the integral/FTC version (`∫ n' = n_b - n_a`) is NOT formalized** and is stated as such in
   the file header. Monotonicity beyond `x_b` is an explicit premise (DT2's stated extra hypothesis),
   not a conclusion.
5. **Budget exhaustion** — `budgetX_identity` (`X(1+X) = x^2`), `budgetX_nonneg`, `budget_char`
   (X is the UNIQUE non-negative root, so the branch convention is immaterial),
   `budget_exhaustion_iff` (`X(x) = R_b ⟺ x = sqrt(R_b(1+R_b))` for `x ≥ 0`, `R_b > 0`),
   `budget_exhaustion_at_xb`. `X` is defined as the non-negative branch of `X(1+X) = x^2`
   (the lane gives only the inverse relation, so the branch is fixed by definition and proved unique).

## Scope (repeated for the record)

Lean certifies the algebra and real analysis above, over the stated hypotheses. It does not certify that
any of these relations is a law of nature, that the khronon/Zimmerman action is the correct action, or
that the numerical values of `I0, mu, x_T, R_b` are the ones realised in the universe. Every identification
of a symbol with a physical quantity is an imported assumption, not a conclusion of this file.
