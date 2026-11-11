# PAR1 AMENDMENT A1 (POST HOC, committed alone, before par1_grade.py exists or any label is computed)

Criteria 51522963e0. This amendment is post hoc: it was written after `par1_spec.py` printed S8's series.

## What changes

S8 (T-SHK) as frozen states the energy-flux jump of a barotropic jump that conserves charge and momentum as
"-(m/12) P''(tau) (Delta tau)^3 + O(Delta tau^4)". The sign is wrong. The series (sympy) gives

    [energy flux] / m = +(1/12) P''(tau) (Delta tau)^3 + (1/24) P'''(tau) (Delta tau)^4 + ...

exactly +(1/12) b Delta^3 for a quadratic P(tau) (hand check in RESULT.md). With Delta tau < 0 (a compressive jump) and
P''(tau) > 0 the jump is negative: mechanical energy is lost. That is Landau-Lifshitz's weak-shock result
(T Delta s = -(1/12) P''(tau) (Delta tau)^3 > 0), so the corrected sign is the physical one. The frozen "-" was a sign
slip in writing the statement.

## What does not change

The statement S8 is used for: the jump's energy defect is nonzero wherever P''(tau) != 0, so no single-valued
variational field (whose weak solutions must conserve charge, momentum and energy together) continues through it.
That conclusion holds with either sign. MU2 (P''(tau) = 0) still must give zero, and does.

## Reading

- As frozen, S8's residual line fails (residual b/6), so B-Ts cannot be called EMPTY as frozen.
- Under A1, S8's residual is 0 and B-Ts is graded by the frozen rule otherwise unchanged.
- Both readings are reported; the label under A1 is marked post hoc.

Also disclosed (not a criteria change): two reporting bugs fixed before grading, neither feeding a frozen line:
`S8_coeff_D3_residual` compared against a symbol with different assumptions (printed "b/12 - b/12" instead of 0), and
S15's "2 pi bracket" divided where it should multiply (the bracket makes coherence stricter, so the gap grows by 2 pi).

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
