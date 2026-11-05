# AC1 extension: fixed-acceleration local response (frozen before numerics)

This is a further analytic discriminator, not an on-shell galaxy or full G0.
Use the same W and potential portal. Hold a positive external acceleration A
fixed, drop spatial stiffness only for this conditional diagnostic, and
eliminate p by W_p=A/K (p and a are acceleration-normalized).
Equivalently differentiate W-p*A/K with respect to p.
Derive U(a;A)=a²/(xi G)+a²/K*[log(1+A/a)-A/a], a>0.
Check its first/second phi derivatives equal the polarization-only Schur
complement at p=a*A/(a+A). No lapse or clock elimination claimed.

Questions: does U have an interior stationary minimum? Does fixed-phi curvature
remain positive as A/a tends to infinity? A failure of off-shell curvature
positivity is not an unstable on-shell mode. If there is a minimum, does its
a value scale with A rather than remain the cosmic normalization?

Derive the stationary equation, uniqueness, and curvature symbolically/with
monotonicity inequalities. Numerical corroboration: beta=1/3,2/3,9/10,
kappa=1/2, G=1, K=4pi, xi=2*kappa²/(1+beta), A=1.
Bracket positive stationary A/a in [1e-6,1e6], 40/80 precision roots, normalized
agreement <1e-25. Test curvature identities at y=.1,1,3 and A/a=1,100,1e4;
40/80 agreement <1e-25. Reverse the source sign as MUTATE and require its
positive-interior stationary solution to disappear. Record a missing bracket
as inconclusive, not no-solution. Both footings are separate dimensional
normalizations; this dimensionless stationary ratio is a0-independent.
No observational PASS transfers. Do not interpret A as screened physical g
without solving the omitted stiffness and metric constraints.
