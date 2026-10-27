# Source check before author-packet reading

Checked 2026-10-19. The ignored project literature cache was queried before
fetching. It exists, is ignored by the repository .gitignore, and returned no
hits for the exact identifiers below. Earlier speculative v2 queries for
0802.3409 and 1812.06069 also missed; the arXiv metadata then authenticated
both available preprints as v1. No full source was copied into tracked files.
No source retention was needed: the following exact public versions were read
with the browser. Therefore no retained-source binary hash is asserted.

1. O. Borisenko, S. Voloshyn, V. Chelnokov, *SU(N) polynomial integrals and
   some applications*, arXiv:1812.06069v1 (14 December 2018),
   https://arxiv.org/html/1812.06069v1 . The abstract page authenticates the
   version and authors. Section 2, equations (5), (13)-(21), defines normalized
   polynomial SU(N) Haar integrals and enforces the center-selection condition
   r-s divisible by N. Equations (19)-(21) explicitly admit epsilon tensors.
   Specializing N=3, r=3,s=0 gives the epsilon/6 identity in PRETARGET.md.
   Equation (31) gives integral (Tr U)^3=1 and integral Tr U Tr U*=1 by
   specialization. This verifies the required distinction from a parity rule.
   This source does NOT classify all finite cubical polymers: the geometric
   six-square lower bound in PRETARGET.md is an independent analytic argument.

2. Jesse Carlsson, *Integrals over SU(N)*, arXiv:0802.3409v1 (22 February
   2008), https://arxiv.org/pdf/0802.3409v1 . Abstract metadata and full PDF
   were opened as a primary supplementary identity check. The audit does not
   rely on an unverified theorem number from this source.

3. L. Del Debbio, F. Di Renzo, G. Filaci, *Large-order NSPT for lattice gauge
   theories with fermions: the plaquette in massless QCD*,
   arXiv:1807.09518v2 (15 November 2018),
   https://arxiv.org/html/1807.09518v2 . Section 4.2, equations (31)-(32),
   writes the one-component staggered operator with forward-minus-adjoint
   hopping and the ambient-coordinate phase eta. It also states the flat
   continuum four-taste identification and the Nf/4 rooting convention.
   Application here is RESTRICTED: the graph hopping signs agree locally,
   but its ordinary flat-lattice continuum taste statement is not a theorem
   that the polyhedral K_n operator is a curved physical Dirac discretization.

4. G. Gagliardi, W. Unger, *New dual representation for staggered lattice QCD*,
   Phys. Rev. D 101, 034509 (12 February 2020),
   https://doi.org/10.1103/PhysRevD.101.034509 . Published metadata and abstract
   authenticate the Wilson/staggered strong-coupling context. Full mathematical
   article text was not obtained by the ordinary APS abstract endpoint, and an
   accepted-manuscript endpoint failed. No exact formula is taken from that
   unread body. This source is contextual, not a proof dependency.

Haar pair and triple identities can also be derived without sources: invariance
forces the pair tensor to be c delta delta, and contracting unitarity fixes
c=1/3; invariance forces the triple tensor to c epsilon epsilon, and contracting
det U=1 fixes c=1/6. For Tr U Tr Udagger the pair contraction is 1. Thus source
availability is not load-bearing for those identities.

Source authentication, local extraction, and the stated restricted application
were checked. No broad novelty claim, continuum-limit theorem, all-order
polymer classification, or physical-QCD admission is supported by this search.
