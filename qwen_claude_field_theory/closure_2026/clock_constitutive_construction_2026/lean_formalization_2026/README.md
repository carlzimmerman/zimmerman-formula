# Lean formalization boundary

`ClockConstitutiveGate.lean` is an intended kernel-checkable Lean/Mathlib core for the
identities already derived by the executable symbolic gates. It proves the
exponential constitutive law, positivity of the transverse and longitudinal
principal eigenvalues for `y > 0`, the factorization of the flat linear
equation determinant, and the exact witness `c_clk^2 = 18/509`.

Run from the repository root:

```sh
cd qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026
lake exe cache get ClockConstitutiveGate.lean
lake build ClockConstitutiveGate
python3 -B run_lean_gate.py
```

The project layout follows the reproducible Lake/cache pattern used by
OpenAI's public Navier--Stokes and Euler Lean certificates: pin the compiler
and Mathlib revision, fetch the dependency closure, build a declared library
target, and expose a machine-readable formalization status. The inspiration
is methodological, not a claim that the gravity result is comparable in
scope. See <https://github.com/openai/NavierStokesAndEuler>.

The runner returns status `COMPILED` only when the local Lean toolchain checks
the file. In the present host the toolchain is installed, but the Mathlib
build hits macOS `file table overflow` while materializing the dependency
closure; the recorded result is therefore `LEAN_COMPILE_FAILED`, not a proof
pass. That environment failure is separate from the physics status. The
unformalized gates remain the nonlinear metric-dependent York/Hodge variation,
complete Dirac closure, boosted PPN, FLRW perturbations, and the controlled
`y -> 0` limit.
