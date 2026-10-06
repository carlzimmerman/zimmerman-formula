# Independent root derivation review

Reviewed the frozen vector/weighted compatibility report and actual constraints from base c1449c08768f6ea7553ea0ecbc7c6653f4651bb8. This does not certify a nonlinear solution or classify all spectra.

The tracefree ADM extrinsic square for a transverse plane displacement has two equal off-diagonal entries W_x/2, so KijKij gives W_x²/2 and the trace gives zero. Summing two opposite half-amplitude sectors gives the reported relative coefficient Ka³/4. Interaction acceleration at quadratic order depends only on the relative lapse gradient; no transverse kinetic correction is available in the unchanged action. The shift equation therefore enforces W=0 for nonzero wave number, allowing only divergence-free relative shifts from the quadratic flat direction.

For one eigenvalue, the original clock current becomes -3H div(nu grad nu)-k² V.grad nu. A nonzero real eigenfunction has a nonzero extremum on the compact torus. There the second term vanishes for every smooth V, while the first is +3Hk²nu². The distinct admitted flat-data powers cannot remove this term on an open time interval. This argument does not constrain singular vector fields or a different action.

For general smooth f, writing w=Delta f and u=(-Delta)^-1f gives the repair equation V.grad w=(H/a)div(f grad f-2w grad u). Periodic weak divergence freedom implies its integral against any smooth G(w) is zero, by using an antiderivative as test function. This is only necessary. For f=cos x+alpha cos 2x, I independently extracted the constant Laurent coefficient of w²R using cos x=(z+z^-1)/2 and sin x=(z-z^-1)/(2i). It is -3(64alpha^4+40alpha²+1)/4, so the full period integral is -3pi(64alpha^4+40alpha²+1)/2. Every real alpha fails the necessary condition, including genuine two-shell data. The exact polynomial carries the uniform conclusion; a symbolic spot check corroborated it but is not a general spectral search.

Disposition: these stated smooth eigenshell and explicit weak two-shell obstructions survive the independent derivation. No arbitrary multishell theorem follows from their negative integral, and no healthy or positive cold mode has been derived.
