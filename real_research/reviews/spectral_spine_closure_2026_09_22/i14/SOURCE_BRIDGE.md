# I14 physical source bridge: the missing identification is substantive

Base checkpoint: `e3af62a453ca6625db8428f6d32957b27a7f1331`.
Read-only source inspection of the four sources I14 originally cited:
`deepseek_push/G155_sourced_eq.py`, `deepseek_push/G081_equilibrium_stability.py`,
`deepseek_push/WAVEBOARD.md` (B8, lines 1609-1622), and
`deepseek_push/THE_THEORY.md` (L5, lines 52-63). Source hashes are pinned in
the computation manifest. This checks those project sources, not an external
literature or novelty search. None of the source files was modified.

**Primary verdict: incomplete, with a failed proposed identification.** The
specified lattice theorem is sound after its quantifiers are corrected. Its
quadratic form has not been derived as the physical fluctuation operator,
and the natural fixed-background radial variation of G155 produces a
different operator. This is not a proof that every possible physical
completion fails; it blocks the cited inference.

## What the sources actually provide

| Source | Actual content | Missing map to I14 |
|---|---|---|
| G155, lines 96-113 | Shift-symmetric scalar f(K), with K=(d phi)^2/(2 Lambda^4), plus candidate matter couplings | No derivation of a bare -kappa^2/r^2 fluctuation term or a positive confinement profile |
| G081, opening and lines 172-191 | Isothermal fluid displacement xi, coupled to a perturbed Newtonian potential; sigma^2=C/2 | Different unknown, norm, dynamics, and boundary conditions from I14's scalar Dirichlet lattice |
| WAVEBOARD B8 | Acoustic dispersion omega=c_s k with c_s^2=C/2, explicitly zero gap | No confined scalar Hessian or derivation of I14's potential |
| THE_THEORY L5 | A frozen scalar kinetic function K-1/(1+K), with a minus-sign K convention | Different f and invariant convention from G155; no comparison or equivalence supplied |

The same symbol kappa appears as a scale ratio in a0, as the isothermal ratio
sigma^2/C, and as I14's formal potential coefficient. Repetition of a numeric
value does not supply a field redefinition or equality of operators.

There is also a directly checkable incompatibility in the quoted actions.
G155 defines, for x=sqrt(K)>0,

    f = x^2 - 2 log(1+x) - 2/(1+x) + 1,
    f_K = mu(x) = x(x+2)/(1+x)^2 -> 0 as x -> 0.

L5 instead writes f(K)=K-1/(1+K), whose derivative at K=0 is 2. The
opposite K convention does not turn a vanishing derivative into a nonzero
one. These functions cannot be used interchangeably as one specified
quadratic action without an additional, explicitly given transformation.

## Direct radial variation of the G155 kinetic function

This is a derivation on a fixed flat spatial background of the gradient
functional. It is not an assertion about the full Lorentzian Hamiltonian,
the time kinetic sign, metric perturbations, or coupled matter constraints.
Those ingredients would be required to decide physical dynamical stability.

Take

    F[phi] = 4 pi int r^2 Lambda^4 f(K) dr,
    K = phi_r^2/(2 Lambda^4),
    phi = phi0 + epsilon eta.

The coefficient of epsilon^2 is

    Q[eta] = 2 pi int r^2 a_r(r) eta_r^2 dr,
    a_r = f_K + 2K f_KK.

The full second variation is 2Q. This follows by inserting
K=K0+epsilon phi0_r eta_r/Lambda^4+epsilon^2 eta_r^2/(2 Lambda^4)
and expanding f to second order. Shift symmetry gives a derivative-only
quadratic expression in the original perturbation eta; a potential can
appear after a weighted field change, but must then be computed from that
weight. It cannot be inserted independently.

For G155's function, differentiation gives exactly

    a_r(x) = mu(x)+x mu'(x)
           = x(x^2+3x+4)/(1+x)^3 > 0,  x>0.

For the trial log background phi0=C log r with C>0, let
ell=C/(sqrt(2) Lambda^2)>0, so x=ell/r. Changing r=e^t gives

    Q/(2 pi) = int w(t) eta_t^2 dt,
    w(t) = r a_r(ell/r)
         = ell (x^2+3x+4)/(1+x)^3.

In the deep regime x->0, w->4 ell, a constant. At leading deep order the
log-coordinate gradient form is proportional to int eta_t^2 dt. It does
not have I14's canonical weight e^t, so dressing by sqrt(r) is not its
natural unit-weight transformation.

For comparison, a canonical radial coefficient a_r=constant gives w
proportional to e^t. Dressing v=sqrt(w) eta then gives

    Q/(2 pi) = int (v_t-s v)^2 dt,
    s=(log w)'/2,

and, for compact support or vanishing boundary values,

    Q/(2 pi) = int [v_t^2+(s^2+s')v^2] dt.

The canonical case has s=1/2 and potential +1/4; a_r proportional to r^-1
has s=0 and potential zero. More generally a_r proportional to r^-p gives
potential (1-p)^2/4. This pins exactly where the Hardy coefficient comes
from and why its physical coefficient cannot be read from a log profile
alone.

For the full G155 interpolant the exact dressing yields

    s(x) = x(x^2+4x+9) / [2(1+x)(x^2+3x+4)],
    V(x) = s(x)^2 - x ds/dx
         = x(x^5+8x^4+42x^3+64x^2+17x-72)
             / [4(1+x)^2(x^2+3x+4)^2].

V tends to zero at x=0 and to 1/4 at x=infinity. It is not a constant
1/4-kappa^2; changing the scale ell shifts the transition along t. Its
negative region does not by itself imply a negative mode: the original
quadratic form is an integral of positive weighted squares. A scalar
potential or a coupled gravitational/matter sector could change this
operator, but must be included and varied explicitly.

## The cited log profile is not an exact solution of the full G155 interpolant

G155 states that phi=C log r exactly solves its source-free radial equation.
Its own displayed mu gives instead

    r^2 mu(x) phi_r = C ell (x+2)/(1+x)^2,
    r d/dr [r^2 mu(x) phi_r] = C ell x(x+3)/(1+x)^3 > 0

for x=ell/r>0. The flux is not constant. In the deep leading approximation
mu(x)=2x the flux becomes the constant 2 C ell, and the log solution is
valid for that approximate equation. The exact full-interpolant equation
requires a different background. The symbolic check reproduces these
identities exactly; this is not based on a floating residual or on a failed
search for a derivation.

A further reason not to import G081 as a spectral certificate is that it
checks local solution families and zero-frequency ODE residuals. Existence
of local solutions for every frequency does not establish the spectrum of
a fixed operator domain satisfying all endpoint conditions. Its claimed
neutral continuum therefore cannot identify the finite Dirichlet operator
in I14. A full re-audit of G081's physical formulation is outside this work.

## What remains to identify a physical coupling

One must choose a single action and invariant convention; solve its actual
background equation (or state a controlled approximation); derive the full
quadratic action including time kinetic terms, matter, gravity, constraints,
and any confinement; specify its Hilbert norm and endpoint domain; then
show that its radial operator reduces to I14's lattice form with a stated
mesh prescription and parameter map. Finally, choosing a unique coupling
requires a physical marginality/saturation condition beyond mere stability.

The existing sources do not complete that chain. In particular, neither the
sharp mathematical threshold nor the factor 1/4 derives a0's kappa=1/2.
Adding positive confinement also moves the model's threshold. These are
specific obstructions to this proposed bridge, not an invitation to assume
it under a new name.

Self-review: direct differentiation, Taylor coefficients, log-coordinate
Jacobian, integration-by-parts sign, asymptotic regimes, and flux derivative
were recomputed. The exact symbolic verification is in verify.py and its
recorded output; no external empirical/source claims are needed for this
algebraic obstruction. Routine proofreading introduced no additional
mathematical changes beyond the explicit new derivations and corrected scope.
