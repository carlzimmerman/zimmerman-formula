# Exact-clock finite-difference refinement (post-result, no original grade changed)

The original six high-precision roots and positive-slope controls pass, but the
1e-4/5e-5 finite-difference pair misses 1e-5 at lambda/H0=100. Original results
and failed label remain in clock_initial; the analytic Jacobian is unaffected.
The smooth characteristic has a cubic correction whose relative derivative
error grows as (lambda*q)^2, so shrinking q is the relevant discriminant.

Freeze a separate diagnostic pair q=1e-5,5e-6 at the same six backgrounds and
half-caustic times, with the same 1e-5 difference threshold. Also require the
fine-pair difference divided by the coarse-pair difference to lie in [.009,.011],
consistent with second-order centered differencing under a tenfold step change.
Do not change roots, scalar history, model, tolerances or original outputs.
Exact-clock global-regularity counterexample is an analytic branch statement;
this numerical refinement corroborates its characteristic-map derivative.
