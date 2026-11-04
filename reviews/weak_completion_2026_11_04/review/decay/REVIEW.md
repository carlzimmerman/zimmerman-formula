# Independent CC11 decay audit

The audited claim is the leading, fixed-vacuum, massless-external-gaugino
one-loop decay packet at `e=.003`, `x=25.4000254000381`, `mu=2e6 GeV`,
including the two mixed adjoint–chi exits and the allowed octet gaugino pair.
**Primary verdict: computationally verified only in the stated range.**
The inspected derivation, independent critical algebra, and fresh finite controls
support using these as local leading pole rates. No physical normalization or
missing leading two-body channel counterexample was found. This is not a second
independent six-diagram generator, an interval-certified error bound, or a common
cosmological history.

The exact transpose-symmetry selection rule passes as a mathematical implication
of the displayed action and invariant vacuum; its gravity application remains
conditional on preserving that same symmetry.

## Dependencies and obligations

The dependency chain is canonical component action → scalar/Weyl/vector mass
blocks and ordinary vertices → six triangle classes and vanishing relevant tree
leg insertions → finite on-shell form factors → canonical widths and residual
color sums → source branches and separately retained daughter cohorts.
The first two arrows use the frozen component model, whose code was inspected;
the new independent checks reconstruct selected load-bearing leaves rather than
assuming its reported verdict.

| Obligation | Result and scope |
|---|---|
| Six 1PI classes, physical/Goldstone propagators | Passed for the local packet; external source inventory verified separately. |
| Bridge momentum and transverse/longitudinal numerators | Passed by direct Clifford reduction and explicit matrix checks. |
| Conjugate vector index orientation | Passed by interaction-index typing and an external-field phase discriminator. |
| Finite tensor integration | Passed selected scalar and five-denominator moments by different quadratures. |
| UV, gauge, internal-basis and weak-scaling tests | Author finite records inspected and validated; no universal Ward theorem inferred from three gauge values. |
| Goldstino selection and mixed-channel LSZ insertions | Passed under the stated unbroken unitary symmetry. |
| Majorana, mixed-species and octet color normalization | Passed independently. |
| Other leading two-body exits | Passed using representation exclusion as well as thresholds; see correction below. |
| Production daughter number and birth energy | Passed directly from stored momentum cohorts. |
| Evolving parents, inverse transport, secondary partner evolution and full relic history | Not addressed by this local decay calculation. |

## Independent critical derivations

Use metric `+---`, outgoing null `p1,p2`, `s=2 p1.p2`, upper momentum
`kt=k+p1`, lower momentum `kb=k-p2`, and `u=k²,v=2k.p1,w=2k.p2`.
Between the on-shell external spinors, `p1slash` at the left and `p2slash` at
the right vanish. Thus the FFS kinetic chain `ktslash kbslash` gives `u`.
The transverse FFV contraction gives `4 kt.kb`, namely
`4[u+(v-w-s)/2]`. Its longitudinal chain is
`kslash ktslash kbslash kslash`, giving
`(u+v)(u-w)=u²+uv-uw-vw`.

The ordinary scalar-current momenta in the two mixed graphs are
`ds=k+2p1+p2` and `dv=k-p1-2p2` with their respective current orientations.
The bridge fermion momentum is `-k`. Including the scalar-current orientation,
the surviving transverse chains give `u+2v` and `-u+2w`. Contracting the
longitudinal vector momenta gives `u(u+v-s)` and `-u(u-w-s)`. The two-vector
mass-flip chains give `u+v`, `u-w`, and
`u[u+(v-w-s)/2]`. These reproduce all the implemented kinetic polynomials.
Three explicit arbitrary loop four-vectors, without setting internal lines on
shell, reproduce the ten identities within `1.39e-15` scaled error in `run001`.
The sign is fixed by the momentum/current routing, not by fitting the final rate.

For `G=ext† R U`, an external undaggered mass coefficient must transform as
`exp[i(theta_a+theta_b)]` when the external field columns are rephased.
`Y Y` and `G* G*` have that weight; `G G` has the opposite weight.
An explicit complex two-flavor example gives covariance residual `7.85e-17`
for the corrected orientation and `0.9398` for the historical orientation.
Rephasing the actual external columns gives the predicted full amplitude weight
within `6.56e-13`. This independently discriminates the CP-odd vector contribution.
The corrected orientation also matches the index order in Martin's
[exact-version equations 3.2 and 3.6](https://arxiv.org/pdf/hep-ph/0509115v2).
This citation supports the self-energy convention, not the full new triangle
calculation.

The five-denominator tensors were reconstructed by Wick rotation and an SO(4)
angular average, followed by adaptive parameter integration rather than the
source's product Gauss rule. For example, with `t=l_E²` and `u0=-xy s`,
the angular averages are `u0-t` and `u0²-3u0 t+t²` for `u` and `u²`.
Radial beta integrals give the normalization and parameter weights independently.
All eight selected moments at `(s,mt²,mb²,mr²)=(.17,.8,1.1,.7)` agree within
`4.15e-15` relative error.

The messenger normalization was derived in its original charge basis, using
two Weyls, four canonical real scalars, and a hand-written positive Takagi
matrix. The complete coefficients are `A_FFS=B_FFS=0` and
`C_FSS=-2 sqrt(2) g² mu_X lambda² X0`.
An independent one-dimensional logarithmic integral for `C0` reproduces the
finite `arcsin(sqrt(tau))²/tau` form at four values through `s=1.5<4m²`,
within `3.45e-16`. This checks the FSS sign, loop and real-scalar normalization,
and finite momentum dependence. **It does not check a relative FFS/FSS sign**:
the FFS coefficients vanish. The actual-model soft derivative bridge and gauge
cancellation provide separate evidence for the relative diagram signs.

## Goldstones, symmetry and external legs

The gauge-orbit tangent projector was reconstructed directly from `R z`,
without using the scalar zero-mode classification. It agrees with the source
Goldstone projector within `8.66e-13`. The remaining physical zero-scalar space
has rank two and negligible overlap with the Goldstones. Replacing every
zero-scalar mass by `xi mV²` would be wrong; the current source does not do so.

For every retained mixed and octet-pair term, the parameter denominator
`Delta=x mt²+y mb²+(1-x-y)mr²-xy s` was minimized over the entire simplex.
Its interior Hessian is indefinite for positive `s`; its minimum is on an edge,
where only a quadratic or affine minimization remains. At `xi=.5,1,2`, the
smallest minima are `1.49825e-3` for the octet mixed channel,
`1.49982e-3` for the triplet mixed channel, and `5.25064e-6` for the octet pair.
Consequently the accepted terms contain no unobserved cut between quadrature
nodes in this packet.

The transformation `A→A^T,B→B^T,V→-V^T,lambda→-lambda^T,X→X` is unitary;
it does not conjugate the complex background. Cyclicity of the trace preserves
both `Tr(A²)` and `Tr(A²B)`, and the gauge outer automorphism intertwines the
canonical kinetic terms. The diagonal background is fixed. Writing the
fundamental transpose parity as `eta_a`, the parent has parity `eta_a`, its
unbroken gaugino has `-eta_a`, and the `F*` Goldstino is even. The unique
residual invariant for `S_adj lambda_adj G` is `delta_ab`; its product is odd.
This forbids that amplitude, not merely the numerical remainder of one loop.
The actual Cartan parent and gaugino parities pass after transforming into old
field coordinates; the largest parent residual is `8.35e-13`.

The same invariant argument forbids unbroken gaugino–chiral-adjoint mass mixing
and scalar–unbroken-vector mixing. A fixed chi endpoint at the tree parent
vertex vanishes because the unbroken U1 generator annihilates that parent;
the full possible-other-fermion norms are `7.43e-16` and `6.81e-18`.
Every scalar–two-gaugino tree Yukawa block is identically zero. These facts
remove the relevant one-loop external-leg/tree-counterterm contributions to
the mixed channel. Chirality-preserving insertions vanish by the massless
external Dirac equations at this order. A loop Goldstino diagnostic mass on a
constrained background is not a physical Goldstino mass determination.

The first independent run printed two incorrect `parent_C_parity` diagnostics:
it multiplied an old-coordinate C diagonal by mass-coordinate coefficients.
Those two fields were never asserted checks and are explicitly invalid.
The preserved `selection_check.py` and `run002` supersede only those diagnostics
by applying `O` first. No author source or original evidence was repaired.

## Widths and channel coverage

The massless spin sum is `2 s |y|²` for a distinct pair including both
chiralities. The two-body phase space therefore gives `M |y|²/(8 pi)`.
For symmetric `L=-S y_ab lambda_a lambda_b/2+h.c.`, including the identical
particle factor gives `M sum_ordered_ab |y_ab|²/(16 pi)`.
Direct fundamental-generator contraction gives
`sum_bc d_abc²=5/3` for every SU3 parent color. Since `d_811=1/sqrt(3)`,
the pair rate is `5 M |y_11|²/(16 pi)`. There is no additional average over
the already normalized parent component, and no extra factor of eight when
using an existing total octet population.

The finite pole results supported by these checks are:

| Width / mu | S8_0 | S3_0 |
|---|---:|---:|
| mixed adjoint gaugino + chi | 2.859914283e-29 | 2.646097304e-26 |
| adjoint gaugino pair | 4.445295711e-31 | forbidden |
| frozen complete gauge-pair width | 4.631658829e-29 | 3.001424320e-26 |
| sum of leading two-body widths | 7.536026069e-29 | 5.647521625e-26 |

SU2 has no symmetric adjoint cubic invariant. For SU3 the symmetric pair is
the checked d tensor; the antisymmetric f tensor cannot multiply a symmetric
spin-zero Weyl bilinear. The Goldstino exits are forbidden as above.
Other massless gaugino pairs lack the required residual representation.
The massless physical scalars are singlets. A scalar-to-scalar plus one real
massless gauge boson has no nonzero two-body amplitude: the Ward identity and
the two available momenta remove its transverse form factor.

The original sentence saying other massive thresholds are all closed is too
strong. For S3, octet scalar masses `.00264591336` and `.00390369961` and an
octet Weyl mass `.00333793090` lie below the parent `.01010505261`.
Their pair thresholds can be open. Fresh `run003` reconstructs their residual
Casimirs: every massive sub-parent mode is an SU2 singlet, so these pairs cannot
carry an initial triplet. S8 has only massless physical modes strictly below it.
Thus **other representation-allowed massive channels are closed** is the
supported statement. Direct enumeration of all open tree scalar/Weyl pairs
also finds only roundoff vertices (`<=3.26e-17` for FFS and `<=9.68e-21` for SSS).

The [Goodsell–Liebler–Staub v2 inventory, Appendix A.2.3](https://arxiv.org/html/1703.09237v2)
contains the six scalar-to-two-fermion triangle classes, equations A.99–A.110.
Its exact-version PDF header and HTML equations were independently authenticated.
That verifies the inventory and generic coupling structure; it does not certify
the project's whole SU5 insertion or an arbitrary-gauge identity.

## Evidence limits and production handoff

The current four author manifests all validate with status `completed`.
Recorded octet/triplet mixed gauge spreads are `2.64372e-10` / `1.56929e-13`;
the octet-pair gauge spread is `8.51423e-10`. Therefore the derivation's statement
that both mixed amplitudes agree to `2e-12` over all tested xi values overstates
the octet result. The `n24/10→n36/16` quadrature comparisons are smaller; they
are not substitutes for the actual gauge spread. The mass-block rotations,
UV changes, soft bridge, weak e=.001/.003/.01 scaling, numerical coefficient
filters and floating tolerances were inspected. None supplies a rigorous
all-parameter or all-xi error bound.

All nine superseded-source archive mappings reproduce both their declared
hash and the original manifest hash. Historical `decay/run001` is execution
`completed` but has a percent-scale gauge failure; it is rejected physical
evidence. The source did not yet assert that gauge test. Serialization failures
and the later physical-zero/Goldstone mixing failure remain preserved separately.

The source cohorts retain chi, partner gauginos and each direct gauge sector.
Reconstructing every daughter's birth energy from its stored `q/a` and mass
gives total energy per parent within `2.4e-15` of M, and total daughter number
within `5e-15` of two. The mixed chi numbers are `.3794989902` and `.4685413320`;
partner numbers are `.3912964433` and `.4685413320`. The octet's additional pair
branch accounts for the difference. Partner energy is not silently transferred
to chi or to the quoted direct-gauge radiation ledger. The existing propagation
code was read; no new independent cosmological propagation ODE was run here.

The strongest safe handoff is a checked leading local two-body pole packet,
with correct canonical and residual-color normalization, and number/energy
conserving conditional birth cohorts. The first missing full-history implication
is matching these local rates to the evolving actual parent and daughter state,
including inverse/statistical transport and separately evolved hard partners,
with a validated common field/energy history and retained gravity state. The
two older finite-stage yield normalizations remain separate conditional
examples. No new end-to-end cold-matter candidate or exclusion follows.

Review provenance: independent agent, fresh critical derivations and three
bounded runs; shared component inputs are explicitly retained. Scientific runtimes
are `.683/.405/.183 s` (runner wall times `1.594/.686/.369 s`), with measured
peak RSS below 192 MB, wall/CPU caps 240/235 s and one numerical thread.
Exact input hashes, validator observations,
commands, source locators, archive checks and limitations are in
`provenance.json`; the run directories preserve the raw controls and outputs.
