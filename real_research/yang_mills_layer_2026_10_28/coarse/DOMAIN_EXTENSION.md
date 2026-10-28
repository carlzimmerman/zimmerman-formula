# A bounded minimizing graph at every fixed compact coordinate split

Date: 2026-10-28. Candidate by the root investigator, extending the scope
of `PROOF.md` without changing its audited statements. No novelty claim.
This is a finite-volume analytic result, not a uniform weak-coupling bound.

## Theorem and constants

Let X,Y be compact connected boundaryless Riemannian manifolds with product
metric, and let dmu=rho(x,y) dx dy be a smooth strictly positive probability
density. Let nu be its Y marginal, P conditional expectation onto Y, and
Q=I-P. The form is

    e[f]=t integral (|grad_X f|²+|grad_Y f|²) dmu, t>0,
    Dom(e)=H¹(X×Y).

Suppose the conditional X-gradient Poincare constant is uniformly at least
lambda>0. At a fixed compact split this follows already from positivity
and compactness; the published Yang–Mills bound supplies an explicit value.
Put

    sigma=grad_Y log rho−grad_Y log nu,
    S0=sup |sigma|,
    S1=sup |div_Y sigma+<sigma,grad_Y log rho>|.

These two numbers are finite at each fixed lattice, but are NOT estimated
uniformly in volume, exterior configuration families or weak coupling here.

The energy-minimizing lift subject to Pf=u has the form J u=u−C u, where
C extends to a bounded map from L²(nu) to Q H¹(X×Y). In particular

    ||C||_(L²(nu)→L²(mu)) <= S0/sqrt(lambda)+S1/lambda.       (D1)

Also C1=0. The Schur form s[u]=e[J u] is closed with domain H¹(Y), and
the exact form decomposition is

    e[p+q]=s[p]+e[q+C p],
    Dom(e)={p+q: p in H¹(Y), q+C p in Q H¹(X×Y)}.           (D2)

Thus G=I+C* C is a bounded, positive, boundedly invertible operator and
the normalized coarse form k[z]=s[G^(-1/2)z] on G^(1/2)H¹(Y) is closed.
The published closed-form Schur gap comparison applies to this split.

## Proof

Smooth positivity on a fixed compact product implies equivalence of weighted
and unweighted Sobolev norms. P maps H¹ to H¹, by differentiating the
conditional integral; hence QH¹ is a closed form subspace. The conditional
Poincare inequality gives e[q]>=t lambda ||q||² for q in QH¹, so e is an
inner product making QH¹ complete.

For smooth q with Pq=0, differentiating that zero conditional mean gives

    P grad_Y q=−P(q sigma).

For smooth u depending only on Y, the mixed form therefore satisfies

    b(u,q)=e(u,q)
      =−t integral <grad_Y u,sigma> conjugate(q) dmu
      = t integral u [<sigma,grad_Y conjugate(q)>
            +(div_Y sigma+<sigma,grad_Y log rho>)conjugate(q)] dmu. (D3)

The last identity is integration by parts in Y with x held fixed; there
is no boundary term. It proves

    |b(u,q)| <= sqrt(t)(S0+S1/sqrt(lambda)) ||u|| sqrt(e[q]). (D4)

Indeed ||grad_Y q||<=sqrt(e[q]/t) and
||q||<=sqrt(e[q]/(t lambda)); the L² norm of u in the product is exactly
its marginal norm. By density D3 defines the same mixed form for u in H¹,
q in QH¹, and D4 extends it continuously to all u in L²(nu).

Riesz representation in the Hilbert space (QH¹,e) gives a unique C u with

    e(C u,q)=b(u,q) for every q in QH¹.

Its energy norm is at most the right-hand coefficient in D4 times ||u||.
Applying the discarded Poincare inequality proves D1, and also boundedness
L²→H¹ (with fixed-graph norm equivalence). For u in H¹, the first variation
of e[u−C u] along QH¹ vanishes, so J u is exactly the constrained minimizer.
For u=1 the mixed form vanishes, proving C1=0.

The one-step comparison in `PROOF.md`, equations (3)–(4), applies with a
finite score covariance bound M<=S0. It gives

    (1+S0²/lambda)^(-1) e_Y <= s <= e_Y,

so s is a closed form on H¹(Y). Energy orthogonality of Jp and QH¹ proves
the identity D2. Its domain equality follows in both directions from the
H¹ boundedness of P and C: if f is in H¹ then p=Pf and q=f-p are in H¹;
conversely p in H¹ and q+Cp in QH¹ imply f=p+q in H¹. Normalization by the
bounded invertible G^(1/2) preserves closedness with the stated transported
domain. This checks exactly the hypotheses of the published closed-form
extension, rather than multiplying unchecked unbounded operators.

## Actual vacuum and repeated coordinate constraints

For the actual finite SU(N) Wilson-link vacuum, rho=psi² is smooth and
strictly positive. All assumptions above hold for any fixed coordinate
split. Thus boundedness of the original minimizing graph is unconditional
at fixed finite volume and fixed x>0. No such conclusion is asserted for
nonlinear holonomy fibers without a separate argument.

For nested retained coordinate sets Z_i, let E_i be the original conditional
expectation onto Z_i and J_i the direct-original minimizing lift under
E_i f=u. Apply the theorem with X equal to all deleted coordinates. Each
J_i is bounded on its coordinate L² space, and its correction
C_tot,i=inclusion−J_i maps L² into H¹ of the original product.

The intermediate minimizing lift is j_i=E_i J_(i+1). Uniqueness and the
tower property imply J_i j_i=J_(i+1). Its correction is

    C_i=inclusion−j_i=E_i C_tot,i+1.

Since E_i is H¹ bounded at the fixed graph, C_i maps L² into H¹(Z_i).
The unnormalized intermediate closed form s_i has domain H¹(Z_i), by the
direct-original one-step comparison, so the same square completion has
its exact form domain at each unnormalized coordinate stage.

This verifies boundedness of all these finite-sequence graph maps. It does
not establish volume-uniform bounds for them, a favorable accumulated
metric, or every domain detail for the transported orthogonal subspaces
in the normalized iteration of `PROOF.md` §2. That last identification is
retained under its stated domain hypotheses until checked separately.

## Limit of the result

The abstract boundary-trace counterexample in `PROOF.md` §5 remains valid:
an energy-weighted estimate alone does not imply boundedness. The present
argument uses the additional smooth product diffusion structure and the
first-order cancellation D3. S0 and S1 may grow badly with the number of
coordinates or as x decreases. The quantitative physical layer and
continuum questions therefore remain open.
