# Focused proof audit and final self-review

Claim: for the stated homogeneous canonical potential, any prescribed absolutely
continuous density d(t)>8 on a compact time interval, and a solution on |q|<pi,
E_final <= E_initial exp(integral max(d',0)/(d-8) dt). Finite instantaneous
jumps obey the corresponding ratio bound. E is the excitation defined in REPORT.
Verdict: **proved as written**, within the explicitly stated homogeneous domain.
This is self-review of REPORT.md section 5 at the pre-commit checkpoint based
on 0dbe9d1421, not independent certification or proof of the physical goal.

Dependencies: canonical homogeneous equation -> work identity; exact polynomial
factorization -> E >= (d-8)(A-1) >=0; sign of d' -> differential inequality;
integrating that inequality -> exponential bound. No external source theorem
beyond elementary differential inequalities is a load-bearing leaf.

Obligations:
- Passed: x=sec(q/2)>=1 on the physical branch; coefficient polynomial positive.
- Passed: kinetic energy is nonnegative and must be included in E.
- Passed: for d'<0, E'<=0; replacing d' by its positive part gives an upper bound.
- Passed: zero E is preserved by uniqueness; the proof need not divide by E.
- Passed: d is bounded away from 8 on a compact continuous-density interval.
- Passed: at a jump q,p are unchanged, Delta E=Delta d(A-1); the same ratio
  bound follows algebraically for upward jumps and energy decreases downward.
- Out of scope: a crossing of d=8, energy flux, quantum fluctuations, matter or
  metric backreaction, and contracting geometry. They are not excluded routes.

The quarter-cycle linear control saturates the per-rise factor in its
small-amplitude limit; the full nonlinear inequality does not assert repeated
saturation. Source amplitudes and phases are controls, not selected parameters.

Computation review: exact algebra checked by bounds.py; normal run validates,
mutation fails specifically at the independently integrated energy ledger.
ODE tolerance repeats and monodromy determinant checks pass in the declared
range. No continuum spatial simulation or observational covariance is claimed.

Mathematical proofreading: reviewed the complete new REPORT.md; no routine or
mathematical-token changes required. The separate galaxy bound is explicitly
restricted to the earlier spherical selective bookkeeping, not conflated with
a validated Palatini prediction.

Remaining gap: a physical coupled system must predict seed, source history,
energy supply and retention, then satisfy galaxy constraints. The strongest
safe result is a possible externally driven amplification mechanism with an
exact work bound, plus an insufficient internal redistribution budget under
the recorded assumptions. Next discriminating check: derive the density-source
spectrum from a specified, independently justified matter-field initial state.
