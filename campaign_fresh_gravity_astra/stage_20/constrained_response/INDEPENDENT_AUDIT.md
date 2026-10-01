# Independent audit: fixed-mass and fixed-wall local response

Reviewer: /root/pressure_extrema. **Accepted as a conditional local theorem.**
No correction to the displayed argument is required. I read the fixed
ROOT_DERIVATION.md and independently checked its functional maps, variational
signs and boundary terms. I did not read the new author or metric_intake
files, and performed no numerical computation.

The root proof discloses that an author route preview arrived after its
reasoning but before its filesystem freeze. This audit preserves that
chronology: the root artifact must not be described as fully informationally
isolated. My review is root-only, not a second independently constructed seed
or a verification of the author's new proof.

## Density and displacement variables

The normalized exponential is the unique positive hydrostatic density for
the prescribed phi and total mass. Differentiating its normalizing integral
gives exactly

    r_psi=-rho(psi-<psi>_rho)/cs²,

whose integral is zero. The weighted average is indispensable. The seed must
have precisely the chosen mass M and prescribed endpoint values; merely
being an equilibrium of some other initial-value problem would not suffice.

For a regular rho bounded above and away from zero with bounded derivative,
xi->-(rho xi)' is bounded H1_0 to zero-integral L2. Its stated inverse is
well defined and bounded: the integral of r is H1, division by rho preserves
H1, and the right trace vanishes exactly when integral r=0. This proves the
linear isomorphism. It does not assume that a general H1 displacement induces
a nonlinear positive diffeomorphism, which the proof correctly avoids.

Completing the density square is exact. The cross term produced on expansion
is 2r(psi-<psi>_rho), equal in the integral to2r psi because integral r=0.
The minimizing density is r_psi and corresponds to an admissible zero-trace
xi by the isomorphism. Substitution into the full coercive Q0 leaves a
coercive bound on both field H1 norms. The negative weighted variance in
Q_red is therefore correctly retained rather than discarded.

This is static minimization used to find an equilibrium derivative. It
neither removes the fluid kinetic degree of freedom from dynamics nor
changes the Dirichlet field domain.

## Nonlinear map and seed inverse

In one dimension H2 embeds into C1 on the compact interval. Uniform seed
positivity of phi0' is thus preserved on an open H2 neighborhood, while
rho_phi stays positive and normalized. On such a bounded neighborhood,
composition by the smooth functions b, T and exp is continuously
differentiable in the required Sobolev norms. In particular

    (b(phi',a))'=b_g phi''+b_chi chi'

is L2. Its variations consist of bounded coefficient variations multiplied
by L2 second derivatives, or bounded coefficients multiplied by L2 second
derivative variations. The H1 multiplication and H2-to-C1 estimates provide
operator-norm continuity. The asserted F:H2^2 to L2^2 C1 mapping is valid
locally; making the same positivity claim on all H1 would not be valid.

Differentiation gives the displayed D. In the first component the sign is
-[A psi'-q eta]'/C+r_psi; the second is
(-J eta''+m eta-q psi')/C. Weak integration against zero-trace tests yields
the symmetric two-field form, including the negative normalized-density
variance. Its coercivity follows from the full-form assumption as above.

Every L2 right side is a bounded functional on H1_0^2. Completeness of the
equivalent coercive form norm gives its unique weak solution and H1 estimate.
At the smooth seed, the second equation gives eta'' in L2. The first gives
(A psi'-q eta)' in L2, so that flux is H1. With seed A uniformly positive
and A,q having bounded first derivatives, division by A makes psi' H1.
This supplies the H2 estimate and proves the bounded inverse Y->L2^2.

The coefficient smoothness used for this explicit inverse is a **seed**
property. Nearby solutions are initially only H2, but their derivatives
remain invertible by small operator-norm perturbation of the seed inverse.
The proof does not require silently upgrading every nearby coefficient to
W1,infinity to repeat the regularity argument there.

## Local branch and persistence of coercivity

The fixed-inverse update has derivative zero at the seed. On a sufficiently
small closed Y-ball it is a uniform contraction, and the parameter-dependent
center error can be made smaller than the remaining ball margin. This
justifies the ball-invariance and convergence assertions. The continuous
parameter derivatives give local Lipschitz dependence; subtracting neighboring
equations and using their C1 remainder and uniformly bounded inverses yields

    y_lambda=-(D_y F)^-1 partial_lambda F.

Continuity of this expression proves C1 dependence. Uniqueness is local in
the selected neighborhood. The normalized density and zero perturbation
traces preserve mass and both wall values exactly; positivity follows after
shrinking the interval.

The coefficients of the full form vary continuously in the form norm:
phi', chi and the necessary rho, rho' coefficients are controlled in the
appropriate uniform norms by this one-dimensional H2 neighborhood. A small
form perturbation preserves the seed coercive lower bound in the fixed
reference norms. No global continuation or computable parameter radius is
provided. In particular, existence near one seed does not prove that this
same constrained branch reaches the alternative a0 or a distant frozen-H
reference, nor that two separately constructed seeds lie on it.

## Response sign and restoring margin

At fixed fields, b_lambda=-q and T_lambda=S. The weak partial-lambda term
in F1 is integral q' test_phi/C, which becomes
-integral q test_phi'/C because the test trace vanishes. F2 contributes
-integral S test_chi/C. Their sum is exactly ell, with the stated sign.

The density minimizer obeys
cs² r_lambda/rho+psi_lambda=constant, so its density tangent equation
vanishes against every zero-integral density test. Combining this with
the two differentiated field equations gives the unreduced full identity

    a0(u_lambda,v)=-ell[v].

Coercivity supplies uniqueness, hence u_lambda=-z rather than+z. The direct
chain rule for R gives integral(q psi_lambda'+S eta_lambda+S)/C. Substituting
the definition of ell and u_lambda=-z yields

    R'=integral S/C+beta.

There is no general positivity assertion for R' without control of S.
At a separately established autonomous equilibrium V'=R, the restoring
margin is indeed Delta=V''-R'. This does not construct V, produce its
intersection, or prove a fold/nonlinear conclusion when Delta vanishes.

## Boundary and mass controls

Allowing mass to change adds (rho/M) M_lambda to r_psi. Its nonzero integral
prevents the stated displacement inverse from having two zero traces unless
M_lambda=0. Moving field endpoints similarly places their derivatives
outside the homogeneous form domain. A trace lifting contributes
-a0(w_b,test) to the response equation, so the homogeneous remainder is
generally not-z. These are substantive changes of the problem.

For the static density/field energy, direct variation gives the density
coefficient e'(rho)+phi=mu_c, spatially constant by hydrostatic balance.
The phi bulk variation cancels rho phi_lambda using b'=C rho; the chi bulk
variation vanishes by its static equation. Explicit reference dependence
contributes -R. The remaining terms are exactly

    dE_stat/dlambda
      =-R+mu_c M_lambda+[b phi_lambda+J chi' chi_lambda]_0^d/C.

Both boundary signs are positive before evaluating the upper-minus-lower
bracket. This check confirms why individually equilibrated members of a
left-IVP family need not satisfy the constrained susceptibility formula.

## Qualifications and acceptance boundary

No internal analytic gap was found under the specified smooth positive seed,
matched mass/wall values, inherited Q action and coercive full-form hypothesis.
The proof does not independently construct such a seed or verify coercivity
for an arbitrary chosen equilibrium; those are explicit antecedents. It
does not claim a uniform neighborhood over all reference hypotheses.

This remains a fixed-domain diagnostic Q response theorem. It supplies no
physical V, measured source discrepancy, local covariant reservoir,
metric/photon sector, literal scale-vacuum identity, evolving H history,
RAR/M action or operative filtered-MONO transfer. Both a0 hypotheses remain
separate and no empirical or full-theory closure is established.
