# Kappa selection: fixed target and checkpoint

Checkpoint: KAPPA-SELECTION-20260921-A, base Git 44f1694720574d9f5a2d46ce6b5e1d215d142627; working tree contains unrelated changes and an active autonomous loop. Existing research and loop configuration are not modified.

Requested goal: derive kappa = a0/s = 1/2 from independently justified particle-free dynamics, with s fixed independently of a0. A proof conditional on choosing a relative coefficient lambda=1 does not finish that goal. Nor does a theorem assuming kappa=1/count and count=2.

Exact family under test: the constrained auxiliary action documented in ../kappa_unit_response_2026_09_20, with lambda>0, s>0, y=g/s>=0, 0<q1,q2<=1, U(q)=q^2/2-2q+log(q)+3/2 and W_lambda=y^2(1-q1*q2)+(U(q1)+U(q2))/lambda^2. The physical action is minus [s^2 W_lambda/(8 pi G)+rho_b Phi]. Existing action variation yields mu_lambda=1-(1+lambda*y)^(-2) and spherical deep matching a0=s/(2 lambda).

Routes and discriminators:

1. Force-law/shape selection: determine whether the entire static action and normalized response distinguish lambda once a0 is supplied. Test exact rescaling, not a finite fit. Success would require an independently known dimensionless shape condition selecting lambda=1. Failure is exact lambda cancellation.
2. Static admissibility: test whether bounded response and positive transverse/longitudinal principal coefficients exclude lambda=2. A valid lambda=2 counterexample defeats selection by these conditions, not every possible covariant completion.
3. Existing count/matching certificates: inspect raw Lean premises and original symbolic assignments. A proof of the count-to-susceptibility implication from independently specified dynamics would close the goal; assuming that implication leaves it open.

If all three fail, report non-entailment under this specified family, preserve a machine-checked counterexample and the exact missing physical input. Do not upgrade this to impossibility across all theories or claim worldwide novelty.
