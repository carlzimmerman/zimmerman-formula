# Adversarial self-review of MP01

Primary verdict for a mechanism completing the framework: **incomplete, with
the smallest missing implication being matching the new parent to the actual
regular two-state/carrier action and its coefficients**. Review provenance:
same-author self-review, not an independent agent or external referee.

Scoped claim reviewed: the action in DERIVATION.md generates the stated
density-weighted current and kinetic companion at low frequency; its specified
homogeneous pure-component longitudinal Hamiltonian is positive and has the
stated causal principal cone. The sphere response obeys the given passive
outgoing identity. These conditional claims are proved as written by the local
algebra; their finite implementations have the checks recorded below.

Dependency graph: current constraint -> source identity; exact internal-field
equation -> low-frequency expansion; displacement/continuity -> quadratic
action -> Legendre squares -> spectrum/principal cone. Separately, radial
Helmholtz equation -> regular/outgoing matching -> susceptibility -> flux
identity -> selected coupled-mode poles. No cited external theorem carries a
proof step. No simulation supplies a universal stability theorem.

| Obligation | Finding |
|---|---|
|Signs and shift charge|Passed; metric(-,+,+,+), Box sign and reciprocal source reconstructed from variation.|
|Conserved-current cancellation|Passed only with constant coupling and conserved current; conversion explicitly changes premise.|
|Density/phase expansion|Passed for uniform rest background and longitudinal perturbations; not a general vortical action.|
|Canonical energy|Passed at quadratic order; all squares retained, including the h^2 n^2 b^2 term in Hamiltonian coordinates.|
|Dispersion|Passed; exact determinant checked independently against canonical6x6 evolution.|
|Causal condition|Passed for the homogeneous principal symbol; ghost freedom and subluminality distinguished.|
|Boundary cases|A=1 is uncoupled in the low theory; c_s=0 has a zero mode; neither treated as strictly positive sound.|
|Uniform-density range|Conditional; the inequality must hold at every occupied density, not just a reference point.|
|Static forces|Changed at finite M. Exact inherited static preservation is not claimed.|
|Derivative expansion|Conditional on frequencies/gradients below M and appropriate heavy-field initial data.|
|Finite sphere|Passed as fixed-body linear response; a sharp A interface is not the parent's solved density/mediator boundary.|
|Damping poles|Finite numerical evidence with half-step continuation and alternative susceptibility; not all poles.|
|Two-state full health|Not addressed; source identity is insufficient.|
|Microscopic coefficients, kappa, observational fit|Not addressed.|
|Global galaxy formation|Not addressed by these new calculations; original goal remains open.|

## Failed runs preserved

run_001 failed because its determinant residual normalized by already-cancelled
factors. At cs^2=.001,D=.999,h=2,k=100, the exact luminal root was represented
as omega=99.99999999999999. The raw polynomial residual1.82e-7 was misleading;
the frequency-matrix residual was1.14e-14. check_parent_checked.py changes to
coefficient-scale backward error and also checks the original matrix. No
physical equation or parameter was changed. The original source and manifest
are retained unchanged.

run_escape failed because the independent quadrature accidentally evaluated
sin(x) instead of sin(x*r). Boundary matching and passivity agreed already;
the quadrature disagreed strongly, localizing the error. The checked script
fixes only that argument. Original script and failed manifest are retained.

Successful run_checked, run_escape_checked, run_poles and run_pole_refinement
were executed with bounded wall/CPU time and one numerical thread. Their v2
manifests passed validation against current inputs. Zero exit is not a proof
of the overall mechanism. All experiments have finite, specified coverage.

## Attribution and source scope

Density-dependent derivative scalar-fluid interactions are established model
classes, not claimed as a new general idea. The official arXiv abstract for
Kase and Tsujikawa, *Scalar-field dark energy nonminimally and kinetically
coupled to dark matter*,1910.02699v2 (13 March2020), explicitly lists
f2(n,phi,X)J^mu partial_mu phi. The official abstract for Boehmer, Tamanini and
Wright, *Interacting quintessence from a variational approach Part II:
derivative couplings*,1502.04030v2 (3 June2015), describes the variational
scalar-fluid construction. Checked26 October2026:
https://arxiv.org/abs/1910.02699v2 and https://arxiv.org/abs/1502.04030v2.
Only metadata/abstract attribution was checked; their detailed stability
theorems were not imported. Overlap: partial or adjacent result only for this
specific tracking construction. No novelty claim or exhaustive literature
search is made. No papers were downloaded into this packet.

Math proofreading: reviewed this phase's prose, displays, symbols and links.
The letter v in DERIVATION.md is explicitly squared speed; c_s^2 is stored as
cs in numerical code. No mathematical-token changes to frozen derivations.
No manuscript or inherited scientific record was edited.
