# AS006: independent scoped filter audit

Reviewer: actual Astra agent `/root/proof_precision`, 2026-09-27.
Scope: the intake and raw AS006 derivation/result; their hashes are pinned in
`input_verification.json`. No author code, Lean source, numerical output,
external source, or underlying framework specification was audited or run.
This reviews an existing candidate, not a new research seed or theory result.

**Verdict:** the three requested qualifications are necessary. The local
Euclidean vector-Laplacian calculation is correct. It supplies a power-law
heat correction for a fixed toy current under the explicit conditions below;
it does not prove that correction, its remainder, or a solution for the full
filtered MONO system.

## 1. Arbitrary kernels do not supply either asymptotic limit

For positive G,M,a,r, put rM=sqrt(GM/a), x=r/rM and y=B/a=x^(-2).
Substitution proves exactly g/a=x^(-2) psi(x^(-2)) for g=B psi(B/a).
Consequently

    (g/a)/(1/x) = sqrt(y) psi(y),   g/B = psi(y).

The normalized deep limit is 1 iff sqrt(y)psi(y)->1 as y->0; Newtonian
relative recovery is 1 iff psi(y)->1 as y->infinity. Neither follows from
being a function of y alone. The counterexample psi=1 defeats the deep
limit, and psi=2 defeats normalized Newtonian recovery. These examples do
not refute any separately specified registered kernel. A kernel may also
contain dimensionless parameters: x-only dependence removes dimensional
scales, not arbitrary freedom in psi. The fixed branch must be supplied.
Here “deep limit” means asymptotic ratio, not exact equality at finite x.

## 2. A lower floor on xi cannot certify small filter error

Take the report's given inner-argument factor

    H(z)=erf(z) - 2z exp(-z²)/sqrt(pi),   z=r/(sqrt(2)xi).

Direct differentiation gives H'(z)=4z² exp(-z²)/sqrt(pi)>0 for z>0,
with H(0)=0 and H(infinity)=1. At fixed r, increasing xi decreases H.
Thus the relative suppression 1-H grows with xi and tends to 1 as
xi->infinity. A floor xi>=xi_min allows arbitrarily large suppression;
evaluating at the floor gives the smallest suppression in that range.
The quoted tiny errors are not uniform over the stated lower-bounded set.
No observational floor or actual numerical error figure is authenticated here.

An upper bound on xi/r, or a specified fixed small xi, would support an
appropriate quantitative estimate. The exact xi->0 limit is distinct from
a finite scale separation r>>xi. Also xi/rM<<1 is equivalent to xi/r<<1
only with a controlled fixed x=r/rM (in particular x=1); it is not a uniform
equivalence over arbitrary radii. The additional dimensionless parameter
xi/rM remains present at finite nonzero xi.

## 3. Inner and outer filter transfer are different obligations

Write w_t=grad S_t u and j_t=[nu(|w_t|/a)-1]w_t, S_t=exp(t Delta).
The operative equation quoted in AS006 contains S_t^* div j_t. An estimate
for w_t alone does not estimate this entire expression. At minimum it
requires nonlinear response control, the outer operator in its actual
measure/domain, commutation where used, and a field/flux reconstruction.

For a translation-invariant Euclidean heat kernel on all R³ with Lebesgue
measure, S_t is self-adjoint and commutes with derivatives on a suitable
distribution/function domain. This is a conditional mathematical model;
it has not been authenticated as the operative operator with its actual
boundary conditions. In particular componentwise vector heat smoothing
must not be replaced with scalar radial smoothing of its magnitude.

## 4. Independent componentwise vector-Laplacian derivation

Let r=|X|, n=X/r in R³, and J=f(r)n=q(r)X with q=f/r. For each Cartesian
component, the product rule gives

    Delta(q X_i)=X_i(q''+2q'/r)+2 partial_i q
                =X_i(q''+4q'/r).

Substituting q=f/r yields

    Delta(f n)=(f''+2f'/r-2f/r²)n,       r>0.             (1)

For f=C/r, the coefficient is (2-2-2)C/r³, hence

    Delta(C n/r)=-2C n/r³.                               (2)

For f=GM/r² it is (6-4-2)GM/r⁴=0. Both are exact local identities on
any source-free annulus. They are componentwise vector statements: the
scalar identity Delta(1/r)=0 away from zero does not make n/r harmonic.
The Newtonian current is not globally harmonic as a distribution:
GM n/r²=-GM grad(1/r), so its distributional Laplacian is
4pi GM grad(delta_0). Therefore its heat smoothing need not equal itself
away from the origin at positive time.

## 5. What a rigorous small-time expansion requires

For a fixed F in C_c^infinity(R³;R³), differentiating the Gaussian heat
convolution and integrating twice gives

    S_t F = F + t Delta F
              + integral_0^t (t-s) S_s Delta² F ds.

The Gaussian has integral one and is nonnegative, so componentwise

    ||S_t F-F-t Delta F||_infinity
        <= (t²/2) ||Delta² F||_infinity.                 (3)

Thus a second-order remainder here is proved, not inferred from formal
notation. More generally one must specify regularity and a domain on which
the corresponding operations and estimate are justified.

For the *fixed globally defined toy current* J=C X/|X|², the same first
coefficient is rigorously local. Fix a compact annulus K, choose a smooth
compact cutoff chi equal to one on a neighborhood of K and vanishing near
zero, and set F=chi J. Equation (3) applies to F. The difference J-F
vanishes within a positive distance d of K, is locally integrable at zero
(|J|=C/r in dimension three), and is bounded outside a ball. Split its
Gaussian convolution into a fixed ball and its complement. On the first
part use integrability and

    exp(-|X-Y|²/(4t))
       <= exp(-d²/(8t)) exp(-|X-Y|²/(8t));

on the complement use boundedness and the Gaussian integral. This bounds
the tail uniformly on K by A(1+t^(-3/2)) exp(-d²/(8t)), for a finite
K/cutoff-dependent A and 0<t<=t0. It is smaller than every power of t.
Therefore for this fixed toy current, uniformly on K,

    S_t J=J-2t C n/r³+O_K(t²).

At t=xi²/2 the signed radial relative first correction is -xi²/r²;
the remainder is O_K(xi^4) in absolute field units, with dimensional
constants fixed by K and C. This is a small-xi statement on a fixed annulus,
not a uniform large-r theorem or a statement extending to r=0. The analogous
cutoff proof for GM n/r² has zero local first coefficient. Indeed all its
local iterated Laplacians vanish, consistently with nonlocal source tails;
it is not an exactly unchanged globally heat-smoothed current.

None of this proves the same remainder for the operative current j_t:
it changes with t through the inner filter and depends on the actual
nonlinearity, splice and boundary prescription. Reusing (3) for a family
would require uniform local derivative bounds through order four, controlled
tails, and a quantitative expansion of j_t itself. Local leading deep form
j~C n/r alone does not control derivatives of the error. An exponentially
small inner-argument error is not such a proof. Where the actual current is
the phantom response rather than the total response, the subtracted
Newtonian term has zero local Laplacian; this observation still does not
settle the remaining nonlinear or reconstruction steps.

## 6. Critical missing implication and review limits

The first unresolved implication is a justified map from the actual
t-dependent response current, after the actual outer adjoint filter, to the
radial force with the prescribed source and boundaries. Even if the quoted
PDE can be rewritten as div(grad Phi-B-S_t j_t)=0, spherical symmetry on an
annulus leaves an undetermined A/r² radial field. An origin/source condition
is needed to fix A; exterior divergence alone does not exclude an additional
point-source flux. This review does not fix that integration constant.

The correct next assertion to test is whether the full specified filtered
system has a controlled exterior expansion, and what its first correction
is. The coefficient must be derived; exponential suppression should not be
made a success criterion in advance. Neither the toy O(xi²/r²) coefficient
nor the author's inner exponential estimate establishes that full assertion.

One incidental transcription defect is visible in raw result.json's
closure_implication: it equates GM a to 4 kappa² G² M rho_Lambda/c².
This does not follow from its adopted a=kappa c sqrt(G rho_Lambda) and
does not have velocity-to-the-fourth units. Direct substitution gives
GM a=kappa GM c sqrt(G rho_Lambda). No broader audit of the author's
numerical results, Lean certificate, or observational inputs is claimed.

All arguments here are proof-only. No numerical command, CAS calculation,
Lean run, heat-equation solver or new empirical test was performed. Source
hashing and artifact generation are provenance operations. Original files
and the coordinator's intake were not modified.
