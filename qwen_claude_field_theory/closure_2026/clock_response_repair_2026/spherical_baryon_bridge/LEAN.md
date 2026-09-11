# Exact sourced constraint algebra

Base checkpoint: `776cc413d`. The complete relativistic MOND objective remains
open. `SourceSchur.lean` proves five finite-dimensional real-algebra statements
for the quadratic polynomial used in `source.py`; it does not formalize the
variation of general relativity or certify the full theory.

For arbitrary real coefficients at a fixed time and nonzero Fourier
wavenumber, the polynomial is

    L = A0 v²/2 + J z v + B0 u v + D z²/2 + E z u + C0 u²/2
        + fz z + fv0 v + fu0 u.

Here `v=udot`. The names `B0,C0` in this algebra are the raw mixed and field
coefficients, not the background clock kinetic coefficient also called B0 in
other calculation files. The physical constraint reduction requires `D != 0`.

The Lean file checks that `z=-(J v+E u+fz)/D` satisfies the displayed linear
constraint and that its exact substitution gives

    Lred = (A0-J²/D) v²/2 + (B0-J E/D) u v + (C0-E²/D) u²/2
           + (fv0-J fz/D) v + (fu0-E fz/D) u - fz²/(2D).

The velocity-increment identity also checks the momentum coefficient:

    Lred(u,v+dv)-Lred(u,v) = p dv + (A0-J²/D) dv²/2,
    p = (A0-J²/D) v + (B0-J E/D) u + fv0-J fz/D.

Consequently common physical initial data `u=v=0` require
`p=fv0-J fz/D`. A final lemma shows that these data do not have zero momentum
when this velocity-source coefficient is nonzero. The source-dependent
canonical offset follows from the same initial field and velocity; it is not
an independently chosen scalar charge for each source.

Theorems and scope:

| Theorem | Exact conclusion |
| --- | --- |
| `constraint_residual` | The solved constraint has zero residual for `D != 0`. |
| `sourced_schur_identity` | All six reduced coefficients, including the constant, follow by substitution for `D != 0`. |
| `velocity_increment` | The linear velocity-increment coefficient is the displayed momentum. |
| `zero_physical_data_momentum` | Zero initial field and velocity give the velocity-source momentum shift. |
| `zero_physical_data_not_zero_momentum` | A nonzero shift excludes zero momentum for those same physical data. |

The last three are polynomial identities even with Lean's totalized real
division, but that does not extend the original physical elimination through
`D=0`. The singular branch needs its original, unreduced constraint equations.

## Executed verification

Working directory:

    /Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026

Actual command:

    lake env lean /Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/clock_response_repair_2026/spherical_baryon_bridge/SourceSchur.lean

Final exit status: **0**. All five `#print axioms` outputs contain only
`propext`, `Classical.choice`, and `Quot.sound`; there are no `sorry` statements
or added physics axioms. Two development compilations exited 1 for Lean
declaration syntax: real division needed a noncomputable section, then that
section needed its own closing `end`. No mathematical statement changed to
address those compiler errors.

The connection from the covariant action to the coefficients remains the
separate symbolic calculation in `source.py`; this Lean file accepts arbitrary
real coefficients and proves their algebraic reduction. It does not establish
the nonlinear constraint count, a globally invertible spatial operator,
well-posed evolution, a galactic force law, or a MOND scale.

Mathbox proof-audit checked the coefficient normalization and excluded branch.
Mathbox proofread-math self-review covered both new files; no local notation,
typographical, or mathematical-token correction was needed after that review.
