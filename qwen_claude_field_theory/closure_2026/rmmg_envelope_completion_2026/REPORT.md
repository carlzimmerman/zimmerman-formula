# RMMG Hamiltonian-envelope completion (2026-09-10)

This is a new constructive branch, not a deletion of the earlier RMMG
candidate.  It targets the minimal pair's cubic constraint-algebra failure by
replacing the separable Hamiltonian with an algebraic envelope.

## Definition

Let (s=|D u|>0), (S=s^2/2), (p) be the relay momentum, and
(P=p^2/2).  Introduce an auxiliary algebraic field (chi) and define

\[
 {cal H}_{\rm env}(p,s,\chi)=W(\chi)
 +\mu(\chi)\left(S-\frac{\chi^2}{2}\right)
 +\frac{P}{\mu(\chi)},
\]

where

\[
 \mu(\chi)=1-e^{-\chi/a_0},\qquad
 W'(\chi)=\mu(\chi)\chi.
\]

For the required kernel,

\[
 W(\chi)=\frac{a_0^2}{2}\left[y^2+2(1+y)e^{-y}-2\right],
 \quad y=\chi/a_0.
\]

The auxiliary Euler equation factors exactly as

\[
 \partial_\chi{cal H}_{\rm env}
 =\mu'(\chi)\left(S-\frac{\chi^2}{2}
 -\frac{P}{\mu(\chi)^2}\right)=0.
\]

On this algebraic surface the envelope derivatives are

\[
 {cal H}_p=\frac{p}{\mu(\chi)},\qquad
 {cal H}_s=s\mu(\chi),
 \qquad
 {cal H}_p{cal H}_s=p,s.
\]

The last identity is the exact 1+1 principal hypersurface-deformation
coefficient, so the (A'(s)p^3) obstruction of the separable ansatz is absent
without hard-coding a cancellation.  On the relay branch (p=0), the
positive solution is (chi=s), hence

\[
 {cal H}_{\rm env}(0,s,s)=W(s),\qquad
 \partial_s{cal H}_{\rm env}(0,s,s)=\mu(s)s.
\]

The secondary (u)-constraint is therefore

\[
 D_i[\mu(|D u|)D^iu]=4\pi G\rho,
\]

with the exact exponential interpolation.

## Dirac witness

The local relay variables ((u,p,\chi,p_\chi)) have primary constraints

\[
 p=0,\qquad p_\chi=0,
\]

and secondary constraints given by the MOND Gauss equation and the algebraic
\(chi\)-equation.  The executable computes the four-by-four Poisson matrix.
At a nonzero Fourier mode its calculated rank is 4, leaving zero scalar phase
dimension.  At (k=0) the matrix rank drops to 0 and the remaining phase
dimension is reported separately.  The auxiliary Hessian is nonzero on the
local (p=0,chi=s>0) branch and vanishes at the controlled zero-gradient
endpoint, so the rank change is visible rather than hidden.

## Status and limits

**SCALAR-SECTOR-CONSTRUCTIVE-OPEN.**  This is a genuine new live architecture:
it simultaneously derives the exponential static law, removes the minimal
one-pair cubic bracket term, and retains an explicit zero-scalar relay branch.
It is not yet a complete relativistic theory.  The next decisive work is to
embed ({\cal H}_{\rm env}) into the full ADM metric constraint with the
rotated slip relay, then vary a covariant clock/Stueckelberg action.  Only
after that can the full metric HDA, Ward identity, (\Phi/\Psi\), PPN,
FLRW, tensor speed and perturbative stability be certified.

The identities above are checked by `envelope_completion_gate.py` and
kernel-checked in `EnvelopeCompletionFormal.lean`.

The structural obstruction behind the previous minimal-pair failure is also
kernel-checked in `CuscutonClosureFormal.lean`: if the bracket matching
conditions are imposed with a nonzero kinetic coefficient, they force
\(\mu'=0\); the exponential kernel has \(\mu'=e^{-s/a_0}/a_0>0\), so the
canonical propagating branch is inconsistent under those hypotheses.  The
Lean theorem is deliberately conditional on the displayed bracket form; it
is not presented as a universal no-go for every relativistic action.
