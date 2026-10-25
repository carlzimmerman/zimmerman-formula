# Eliminate the Coulomb microscopic mass analytically

This extends the finite applicability scan without changing its inputs/results.
Assume the charge normalization and displacement cap in ACTION.md, mass ratio
epsilon in [1e-4,1], and the controlled Coulomb condition a_B>=k*r_core with k=10.
No claim is made for unknown constituent-core interactions outside this regime.

Using mu=epsilon*m/(1+epsilon),

    a_B/r_core = hbar² sqrt(a0) (1+epsilon)
                  / [G^(3/2) epsilon m^(7/2)].

Consequently

    m <= m_max(epsilon)
      = [hbar² sqrt(a0) (1+epsilon)/(k G^(3/2) epsilon)]^(2/7).

For the equal-temperature virial proxy in ACTION.md,

    B_bind/T = 3 epsilon/(1+epsilon)² * alpha_G²*c²/v0².

At fixed epsilon this grows as m^4, so substitute m_max for an upper bound.
Its epsilon-dependent factor becomes epsilon^(-1/7)*(1+epsilon)^(-6/7).
The logarithmic derivative is -1/(7epsilon)-6/[7(1+epsilon)]<0. Thus the maximum
over the ENTIRE stated continuous mass-ratio interval occurs at epsilon=1e-4.
This is an analytic reduction, not an inference from the 1,717-point grid.
Imposing alpha_G<.1 can only lower this upper bound; it is satisfied at the
maximizing endpoint used by the calculation.

The resulting bound compares the Coulomb binding energy with specified virial
temperatures. It does not by itself establish ionization rates, equilibrium,
cosmological survival or population fractions. It shows that there is no virial
thermal binding threshold available from this controlled Coulomb branch in the
stated domain. A strongly bound neutral F would require additional core physics
or interactions, with parameters not fixed by the present action.

The factor k=10 is a declared conservative applicability margin, not a fundamental
constant. The bound scales as k^(-8/7); changing it to1 does not remove the many
orders of magnitude gap. Neither criterion proves the full constituent structure
is known; these are necessary consistency checks for using the Coulomb formula.

Self-review: algebraic bound conditional on the chosen field law, force
normalization, Coulomb regime, mass-ratio interval and virial proxy. It is not a
universal exclusion of charge-conserving mechanisms.
