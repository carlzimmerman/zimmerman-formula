# AmplitudeLaw.lean — Lean 4 + Mathlib certificate

Machine-checks the **algebra** of the amplitude-law / BTFR / virialisation route (cold-collapse
route to the framework's amplitude law). As stated in the file's top doc-comment:

> Lean certifies the mathematics the amplitude law rests on, not that it is a law of nature.

## Theorems certified (10)

| Theorem | Statement (informal) |
|---|---|
| `a0_pos` | `a0 = κ·c·√(G·ρ)` is positive for positive constants. |
| `rM_pos` | The MOND radius `r_M = √(G·M_b/a0)` is positive. |
| `rM_sq` | `r_M² = G·M_b/a0`. |
| `btfr_virial` | `σ² = G·M_b/(2·r_M)` with `r_M = √(G·M_b/a0)` gives `σ⁴ = (G·M_b·a0)/4` — the BTFR up to the virial factor 1/4. |
| `btfr_exponent` | `v⁴ = C·M_b` with `v > 0` gives `v = (C·M_b)^{1/4}` — a 1/4 power law in `M_b`. |
| `profile_slope` | For `ρ(r) = A/r²`, the logarithmic slope `(r/ρ)·dρ/dr = −2` for `r > 0` (the standard form of `d log ρ / d log r`). |
| `monomial_dim_length` | Dimensions as exponent triples `(L,M,T)` with `G=(3,−1,−2)`, `M_b=(0,1,0)`, `a0=(1,0,−2)`: the monomial `G^p M_b^q a0^s` has dimensions of length `(1,0,0)` **iff** `p = q = 1/2`, `s = −1/2`. |
| `mond_length_unique` | Corollary: uniqueness (forward direction). |
| `mond_length_form` | The dimensionally-unique monomial `G^{1/2} M_b^{1/2} a0^{-1/2}` equals `√(G·M_b/a0)` — the MOND radius is the unique length constructible from `G, M_b, a0`. |
| `vc_flat` | For `ρ = A/r²`, `M(<r) = 4π·A·r` gives `v_c² = G·M(<r)/r = 4π·G·A`, constant in `r`. |

Note on §6: over *integer* exponent triples no length monomial exists (the length-squared
monomial is `G^1 M_b^1 a0^{-1}`); the constraint is solved over `ℝ`, where the solution is the
unique point `p = q = 1/2, s = −1/2` — exactly the square-root form.

## Verification status

- **Compile**: exit code `0` (see `../logs/lean_compile.out`)
- **Sorry count**: `0` — `grep -cE '(^|[^`])\bsorry\b([^`]|$)' AmplitudeLaw.lean` → `0`; the word `sorry` appears nowhere in the file.
- **Axioms**: every theorem depends only on `[propext, Classical.choice, Quot.sound]` (verified with `#print axioms`).

## Compile command

```
cd fable_independent_2026/lean_2026
LP=$(for d in .lake/packages/*/.lake/build/lib/lean; do [ -d "$d" ] && printf '%s:' "$(cd "$d" && pwd)"; done)
env LEAN_PATH="${LP%:}" lean ../../kimik3_push/lean/AmplitudeLaw.lean
```

Toolchain: `leanprover/lean4:v4.34.0-rc2` (via elan), with the Mathlib build cached in
`fable_independent_2026/lean_2026/.lake/packages/`.
