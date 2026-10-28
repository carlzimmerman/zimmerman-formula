# Actual-vacuum layer coercivity: target contract

Checkpoint: YM-LAYER-2026-10-28-C0.
Starting Git revision: 5bb77f83c618cab437a705c7aa19d7fe0b7aead7.
The checkout contains concurrent unrelated work; input file hashes, rather
than subsequent HEAD movement, identify the mathematical sources used.

## User-authorized objective

Try to strengthen the finite-block estimate in the actual Yang–Mills
vacuum to a volume-uniform estimate for a whole elimination layer that
can be used through coarse graining. Track proved statements, conditional
implications, counterexamples and unresolved obligations separately.
This is research authorization, not a request to publish another version.

## Model and conventions

At each fixed finite cubic spatial lattice use

    H = (x/2) sum_l C_l + (b/x) sum_p (1 - ReTr(U_p)/N),
    x = g² > 0, N >= 2, b >= 0, physical spacing a > 0.

The normalized positive ground function is psi, its energy is E0,
mu = psi² dU, and the physical ground-state-transformed form is

    k[f] = (x/(2a)) integral sum_l |grad_l f|² dmu.

The primary nonlinear target is at fixed N, with constants independent
of volume, layer cardinality and ultraviolet cutoff depth. Uniformity in N
is a separate stronger question. Gauge invariance and exact coarse
projections must be specified; coordinate deletion, block averages,
holonomy maps, Gaussian models and scalar analogues are not interchangeable.

For a proposed scale j, P_j must preserve the actual vacuum, Q_j=I-P_j,
and the required estimate is

    k_j[f] >= d_j ||f||² for f in ran Q_j.

For continuum mass-gap use, the same construction must control the exact
generated forms/metrics and give a cutoff- and volume-uniform finite
inverse-gap budget in physical energy units, together with a terminal gap.
Continuum field construction and spectral transfer remain additional claims.

## What counts as progress

An unconditional theorem about the actual nonlinear model in a stated new
regime, an independently audited conditional comparison with explicit and
noncircular inputs, or a worked counterexample eliminating a proposed
inference counts as partial progress. None alone is the full target.
Finite computations certify only their stated algebra or tested range.
No novelty or priority claim follows from this research attempt.

## Existing evidence and excluded shortcuts

The published finite-block theorem is in
../papers/yang_mills_bounds_2026/sections/vacuum.tex.
Its constants deteriorate with the number of eliminated links.
The exact Schur comparison is in the adjacent sections/schur.tex.

Earlier layer work is in
../reviews/yang_mills_continuum_2026_09_22/layer/PROOF.md.
It proves a Gaussian layer estimate but does not identify the nonlinear
vacuum with that Gaussian model. All-background Wilson convexity and
automatic quadratic closure under normalized Schur elimination are false.
Strong-coupling global gaps already imply layer bounds in their known
regime and must not be presented as a new weak-coupling result.

## Active routes

R1 — Conditional variance tensorization: identify sufficient influence
control and try to establish it for the actual vacuum. A fixed-block
density ratio alone is not assumed to tensorize.

R2 — Coarse-form stability: derive comparisons to marginal forms while
retaining the graph metric, and test which elimination operations preserve
the required class. Marginal/Galerkin compression and Schur minimization
will be distinguished explicitly.

R3 — Counterexamples: test whether local conditional gaps force a layer
gap and whether conditional Schur reduction preserves a Markov form.
Analogues are labeled as analogues, not counterexamples to Yang–Mills.

R4 — Quantitative weak-coupling discrimination: check whether available
losses permit a physical multiscale budget; identify additional estimates
required rather than inserting an assumed running coupling as a proof.

Root is the single writer of shared status. Route agents write only their
assigned tensorization/, coarse/, and obstructions/ directories. Candidate
theorems require a separate review of their raw statements and proofs.
