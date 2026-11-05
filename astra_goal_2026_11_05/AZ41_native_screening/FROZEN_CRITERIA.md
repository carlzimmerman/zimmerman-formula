# AZ41 — native nonlinear-stiffness mechanism screen, lane7

Frozen before computation, base3587c8eacc. Kappa=1/2 FITTED; not theory
closed. FN6 README/scripts/criteria, CT2 and M1 were inspected. Do not
repeat M1's closed standard Galileon route or transfer its exponent to
the Gaussian operator. No external theorem or paper is a proof input.

## Target and limits

A successful candidate must derive the screening response from its own
covariant equations, possess a regular FRW endpoint, retain the galactic
law, and be checked on T0-T4, Q2 and tensor speed. Mere agreement with
FN6's p window is insufficient. NO VERDICT if these are unresolved.
An early failed regularity/response prerequisite must be reported before
using the five observational engines; no inherited observational PASS.

Test a native family replacing only v3s's switched quadratic stiffness
by Fbar(d)=lambda*d^q/q for d>0, zero for d<=0, where p=K P,
d=D.p and Fbar=K F. Lambda has the units implied by q; it is free.
Keep Wbar=a[-p-a log(1-p/a)] and the other v3s terms unchanged.
Require Fbar(0)=Fbar'(0)=0 and Fbar''>0 on d>0. For positive lambda this
requires q>1; q=1 is a boundary term away from the switch and is excluded.
No claim of global novelty. This is a constitutive-family screen, not a
new adopted action or a fit of q.

## Own radial equation and asymptotic scales

Derive variation of -Fbar(div p), including its sign. In a spherical,
static, zero-charge, mu_K=0 reduction, g=g_b+p and the P equation gives

    g_b=p²/(a-p)-d_r Fbar'(d), d=p'+2p/r.

On the unscreened deep-MOND solution p=a*rM/r, rM=sqrt(GM/a),
evaluate R=|d_r Fbar'(d)|/g_b. Define the diagnostic crossover by R=1.
Derive its mass exponent p_mass=(q-3)/(4q-6), and its r dependence.
For q=2, lambda=Lstar²/2, verify R=Lstar²/(rM*r). This operational
equality radius is Lstar²/rM, not a claim that all definitions of a
screened core have this coefficient. Derive the unscreened high-field
limit p~a,d~2a/r separately; do not use a deep-MOND formula inside rM.
At q=3/2 there is no radial crossover in the deep-MOND approximation.

Show that an inward-growing deep-MOND stiffness correction requires
q>3/2. Its exponent is less than1/4, so cannot equal FN6's0.30-0.45.
Solve for q at target exponents3/10,1/3,2/5,9/20, with no coefficient
tuning. Test the zero-d endpoint of those formal powers even if lambda's
sign is chosen to make Fbar'' positive. Divergence at zero rejects them.
This is only an asymptotic obstruction: a finite-radius crossover or
non-power function is not excluded. No full nonlinear solution is claimed.

## Operator-transfer test

Linearize the radial/longitudinal response at a frozen isotropic
background with Wbar_pp=M>1 and Fbar''=gamma_eff>=0. Derive
delta g/delta g_b=1+1/(M-1+gamma_eff*k²).
FN6's reciprocal Gaussian response at a fixed external-field derivative
is1+C exp(-L²k²). Matching the zero-wavenumber enhancement and k²
coefficient fixes C and L; compare k^4 coefficients. Require exact
equality before treating Gaussian engine grades as grades of this local
constitutive action. An operator mismatch is not an observational failure.

## Controls, numerics and output

Known answers: the q=2 quadratic variation, zero stiffness, zero
wavenumber response, and the exact q=2 ratio above. Use symbolic
identities for the exponents, endpoint limits and transfer mismatch.
Independent40/80-digit evaluations on q=2,3,4; r/rM=10,100,1000;
normalized coefficient lambda*a^(q-2)*rM^(-q)=1 and both a0 footings.
These are dimensionless coefficient fixtures, not a normalization fit.
For the transfer compare k=0,.1,1,10 at M=2,gamma_eff=1, with a
normalized40/80-digit difference<=1e-30. Numerical agreement corroborates
the algebra and is not a PDE convergence claim.

MUTATE drops one power of r from the radial derivative while retaining
the original definitions/known answers; the dimensional radial-ratio
identity and q=2 control must fail. Separate output. No failed line may
be widened. Main PASS checks mean verified derivation, not mechanism PASS.

If no candidate clears regularity and operator-transfer prerequisites,
state T0-T4 and Q2 NOT EVALUABLE for a new mechanism, and full c_T
UNDECIDED, with the missing own-equation solvers explicitly identified.
Do not rerun FN6 at an invented length and call that a mechanism test.
Lane7 remains NO VERDICT on the requested complete covariant mechanism.
