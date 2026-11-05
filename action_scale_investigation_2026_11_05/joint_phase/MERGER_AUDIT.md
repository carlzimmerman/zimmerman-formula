# Combining induced gravity and vacuum sequestering

Assessment base:4d92d1d95df75f24ce7aeef94118b8b83c4e8fe5.
The previous turn was progress: it derived the shared-condensate matching
formula and its restrictions. This audit addresses its explicit outstanding
dependency: whether the vacuum subtraction from SEQUESTER_RESULT.md can be
imported into INDUCED_RESULT.md. It cannot be imported unchanged.

## Exact scaling check on one combined action

Let d>2 and lambda>0 be global. Suppose, conditionally, that the entire
condensate/polarization theory has a protected metric embedding S_p. Its
induced curvature term, including F(sigma,p), belongs inside S_p. Write

    S = integral sqrt(-g)[C_b R(g)/2-Lambda]
        +S_p[lambda^2 g, fields]
        +Sigma[Lambda/(lambda^d mu^d)].

C_b>=0 is an independent bare Einstein coefficient, not the total induced
gravitational coefficient. The required protected embedding of our specific
polarization model remains unconstructed. This audit grants it to test the
proposed merger, not to claim that grant as a result.

Define hat_g=lambda^2 g and hat_Lambda=Lambda/lambda^d. At finite constant
lambda, the change of variables is invertible. It gives

    S = integral sqrt(-hat_g)
          [C_b lambda^(2-d) R(hat_g)/2-hat_Lambda]
        +S_p[hat_g, fields]+Sigma[hat_Lambda/mu^d].

Consequently the global lambda variation in these variables is

    (2-d) C_b lambda^(1-d) integral sqrt(-hat_g) R(hat_g)/2 = 0.

For nonzero C_b it supplies the zero-integrated-curvature constraint.
For C_b=0 it is identically zero. The pure-induced limit loses this independent
global equation; it is not obtained by cancelling C_b and retaining the
constraint. The other global variation still reads

    integral sqrt(-hat_g)=Sigma'(hat_Lambda/mu^d)/mu^d.

These statements follow by differentiation of the displayed bulk action.
The integrated-curvature expression assumes no additional boundary variation
under the global rescaling. If an Einstein boundary term contributes, its
rescaled variation must accompany the curvature integral. Likewise fixed
physical boundary data can break the global scaling and supply extra input;
they cannot silently be held fixed in two different conformal frames.
No numerical experiment or coefficient scan is needed. Singular lambda
limits, infinite-volume regularizations and additional global variables
require separate treatment. No actual cosmological boundary problem is
claimed solved by the bulk rank calculation.

## What this establishes and what it does not

Losing the curvature constraint does NOT prove that protected matter-loop
vacuum cancellation fails. In particular, eliminating a constant vacuum term
from local field equations is different from predicting the remaining
cosmological constant. A residual constant and a global volume prescription
can remain after such a cancellation.

For example, linear Sigma fixes a total volume through its slope and mu.
That is additional global input, not a derivation of the MOND/vacuum ratio.
More general Sigma changes the volume equation. No particular volume,
function or residual constant is selected here to manufacture the target.
The global equation alone is not a demonstrated solution of the boundary
problem with our condensate and actual matter sources.

Restoring C_b avoids the rank loss but reintroduces an independent
gravitational contribution. The total Planck coefficient is then not solely
the condensate value used in INDUCED_RESULT.md; that matching formula must be
rederived for the changed theory. It is invalid to take the offset removal
from the bare-gravity calculation and the coefficient formula from the
pure-induced calculation and multiply their successes together.

There is also a remaining homogeneous-response issue in the specified
mean-field model: its B h^3 p^3 term vanishes at p=0, as do its first two
variations. The homogeneous equations and global constraints therefore
cannot fix B through that term, while the local cubic response depends on B.
An actual interaction or symmetry connecting the amplitudes, curved quantum
corrections, or an inhomogeneous global calculation would change the problem.
None has been supplied by this merger. No all-completions no-go is claimed.

## Primary-source verification and duplicate screen

[Kaloper and Padilla, arXiv1406.0711v2](https://arxiv.org/html/1406.0711v2),
section7 equations(56)-(63), explicitly distinguishes a nonzero bare Einstein
coefficient from the pure-induced limit. The latter loses the averaged-curvature
condition and leaves an unspecified residual cosmological constant, while the
authors retain protected matter-vacuum cancellation. We preserve that
distinction. Their constant induced coefficient is not a verification of our
field-dependent polarization embedding. The scaling proof above applies
conditionally to a protected S_p containing that embedding.

A bounded search also returned precanonical quantum gravity (2311.05525)
and the de Sitter/gauge MOND proposal (2601.04290). They are already covered
by register rows K175/K216 and K775 respectively. No duplicate computation
was launched. This search is not a claim to exhaust the literature or all
possible new constructions.

## Current research boundary

The joint phase, sequestered phase and induced-gravity calculations are
concrete but conditional. Their missing protections and matching data have
not been fixed. This audit rules out one unjustified merger of their partial
results; it does not deliver the requested positive derivation.

There is currently no identified shared microscopic selector in these models
that determines both the response amplitude and the residual vacuum. A new
action or source-dependent symmetry identity must address that exact step.
Arbitrarily choosing another potential, global function or target boundary
value would repeat the already established freedom. The goal remains open.

Self-review: constant Weyl weights; invertibility of global variable change;
d>2 domain; separate nonzero/zero C_b cases; volume versus curvature constraint;
protected-loop cancellation versus residual prediction; source scope and
unconstructed embedding. No independent review or full constraint-health
claim. This is an analytic/source audit, not a new executable evidence run.
