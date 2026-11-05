# Same refinement at the second prescribed normalization

The b=.1 cases passed the frozen320-to640 low3 ladder at0.879% and1.024%.
Their160-cell rows reproduced the original exactly. The b=.3 cases remain
unconverged in the original run. Apply exactly the same160,320,640 refinement
to those two already-prescribed cases, without changing physics, backgrounds,
boundaries, quadrature or tolerance. This completes the original four-case
diagnostic and tests whether this limited stability gate could select b.

Only the case subset differs from spectrum_refine.py. Keep its120/180-second
bounded single-core resource policy, the original2% convergence criterion,
and all failed original records. No coefficient prediction or broad stability
claim is permitted. The160-cell repeat must again match its original row.
