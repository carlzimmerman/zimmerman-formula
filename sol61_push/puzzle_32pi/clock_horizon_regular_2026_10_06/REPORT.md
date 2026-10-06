# A smooth Killing horizon is not an eigenvalue condition for this clock action

The source-generated clock calculation raises a specific new question: can regular crossing of its cosmological Killing horizon select A/H? In the stated stationary normalized-clock action, the answer is no if the requirement is only local smooth horizon crossing. Its exact vacuum radial equations remain a regular ODE at F=0. A global source/cosmology boundary-value condition could still restrict parameters; this local theorem neither proves nor rules out that different condition.

## Action and dimensionally correct normalization

Take d=n+1, n>=3, Einstein coefficient M/2, M>0, N,B>0, H>0. Use the stationary areal metric

`ds^2=-N^2 dt^2+B^2(dr+Vdt)^2+r^2 dOmega_(n-1)^2`, `F=N^2-B^2V^2`.

Set `C=M(n-1)/2`, `lambda_n=(n-1)/[2(n-2)]`, `b=2c/(nH)`, `Veff=n(n-1)MH^2/2`, and signed clock gradient `g=N'/(NB)`. Away from g=0 the even response can be treated as a smooth function Q(g). Per unit solid angle the boundary-reduced vacuum radial action is

`L=C[(n-2)N r^(n-3)(B+1/B)+2N' r^(n-2)/B-r^(n-2)V^2(B'/N+BN'/N^2)]`

`+N B r^(n-1)[2c lnN-Veff+M lambda_n Q(g)]-b B r^(n-1)V N'/N`.

This is the same general-dimensional action used in the center audit, with its flow boundary term removed explicitly. Its response normalization is not held to the four-dimensional value1 in other dimensions. M has mass dimension n-1; c,Veff have dimension n+1, b dimension n, and g,A,H dimension1. No hbar appears.

## Exact principal determinant

Vary before imposing F=0. Let E_V,E_B,E_N be the Euler derivatives. Regard `(B',V',N'')` as the derivative unknowns, with `(r,N,B,V,N')` fixed. E_V contains neither V' nor N'', E_B contains no N'', and their relevant coefficients are

`partial E_V/partial B'=-M(n-1)r^(n-2)V/N`,

`partial E_B/partial V'=+M(n-1)r^(n-2)V/N`,

`partial E_N/partial N''=-M lambda_n r^(n-1)Q_gg/(NB)`.

The last coefficient follows from the actual derivative `-(M lambda_n r^(n-1)Q_g)'`; the EH and braid terms do not supply a lapse second derivative. Thus the determinant of rows `(E_V,E_B,E_N)` and columns `(B',V',N'')` is

`D=M^3(n-1)^2 lambda_n r^(3n-5)V^2 Q_gg/(N^3 B)`.

At a finite Killing horizon r_h>0, F=0 implies V^2=N^2/B^2 and V!=0, so

`D_h=M^3(n-1)^2 lambda_n r_h^(3n-5)Q_gg/(N B^3)`.

It is nonzero whenever Q_gg!=0. There is no factor of F and no 1/F singularity in these vacuum equations. The static-fluid sources contain 1/F, but the source is absent at the cosmological horizon in this question. A static fluid continuing through its Killing horizon would be a different, singular-source premise.

The metric determinant of the t-r block is `-N^2 B^2`, also nonzero at F=0; this flowing chart is regular there. The unitary scalar X=q^2/(2N^2) is finite for finite positive N. Once the ODE derivatives and smooth response are finite, curvature and clock derivatives are finite locally. On a smooth interval the usual local first-order ODE existence theorem supplies a local crossing solution from horizon data. A simple horizon additionally needs F'!=0, an open inequality rather than an equality fixing A/H. This is local ODE existence, not a global cosmological solution or a positive physical kinetic proof.

## An explicit four-dimensional local family

For n=3 put M=H=N_h=B_h=1, eta=.5, c=1.5, b=1, r_h=1 and V_h=-1. Use the actual detuned P2 response `Q=(1-epsilon)g^2-2W(|g|;A)`, epsilon=.01, A>0, and choose N'_h=.01 A. These are freely specified regular horizon data, not an imposed numerical coefficient. Here g/A=.01 and Q_gg is positive and independent of A.

Define the response Legendre combination `J=Q-g Q_g=2[g W_g-W]-(1-epsilon)g^2`. Solving the actual E_V,E_B equations at the horizon gives

`B'_h=-N'_h/2`, `V'_h=-1-(3/2)N'_h+J/2`,

and therefore `F'_h=-2+J`.

Since `W_g=sqrt(g^2+A^2/4)-A/2<=g^2/A` and `g W_g-W=integral_0^g s W_gg(s) ds<=2g^3/(3A)`,

`J<=g^2[4g/(3A)-(1-epsilon)]<0` at g/A=.01.

Hence F'_h<-2 and the horizon is simple for **every positive A**. The remaining lapse equation uniquely fixes a finite N''_h because its coefficient Q_gg is nonzero. A/H varies across this entire local family. The crossing has positive response curvature in this example, but a full constrained health test remains separate. No claim is made that every member matches a regular central source or the selected global vacuum.

The local family also has a varying finite Killing surface gravity, `abs(F'_h)/(2N_h B_h)`, so local regularity does not even remove the nonlinear response dependence of that observable. Identifying A with measured a0 still requires the source/force dictionary of a globally completed branch.

## Scope and evidence

This result does not repeat a Schwarzschild-de Sitter area balance: it checks the actual non-geodesic logKGB response equations at their flowing-clock horizon. It excludes a new proposed selector based solely on eliminating a vacuum horizon singularity, because no such singularity is present when Q_gg!=0. Response-rank zeros, zero shift, an extra boundary condition, quantum state regularity, a changed action or nonvacuum horizon matter can change the premises and require a separate calculation.

The script derives the general-dimensional derivative matrix directly from the radial action using a polynomial response prototype, with arbitrary symbolic n, then verifies finite actual P2 horizon data. The generic Q_gg chain-rule proof above supplies the extension beyond the prototype. Mutation controls incorrectly insert F into the determinant or ignore the response contribution to the lapse derivative. Tests corroborate this analytic theorem and are not a global integration. The original coefficient goal remains open.
