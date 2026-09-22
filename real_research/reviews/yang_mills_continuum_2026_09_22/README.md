# Yang–Mills bridge research: current status

**The Yang–Mills existence and mass-gap problem is not solved here.**

The latest attempt is [YM-C3: whole-layer coercivity](layer/PROOF.md).
It proves a volume-uniform discarded-sector bound for a specified covariant
quadratic model. It also gives exact counterexamples to preserving the
quadratic class under normalized quantum Schur elimination and to an
all-background positive Wilson-Hessian comparison. The nonlinear multiscale
estimate remains unproved. See [review and checks](layer/REVIEW.md).

The preceding result is
[YM-C2: actual-vacuum finite-block coercivity](one_shot/PROOF.md).
For a block of m links in the actual finite-lattice interacting vacuum it
derives a positive discarded-sector lower bound independent of the size of
the surrounding lattice. An explicit version is

    d_B >= [x C_F/(2a)] 2^(-2m(N^2-1)) exp[-C_B/x],
    C_B = 4 diam(SU(N)) sqrt(3m b p_B).

Here x=g^2, a is lattice spacing, b is the magnetic coefficient and p_B
counts plaquettes touching the block. The projection is conditional
expectation in the actual ground-state measure, so it preserves the vacuum
and gauge invariance. The proof does not assume an explicit vacuum formula.

This closes the finite-block conditional estimate, but its dependence on
block size does not give a whole-layer bound uniform in volume. Its use
after exact renormalization, the terminal coarse gap/metric and the continuum
field construction also remain unproved. The derivation is self-reviewed,
not a formal proof certificate or independent peer review.

The preceding [YM-C1 report](REPORT.md) contains the exact Schur bridge,
continuum transfer lemmas and counterexamples to insufficient shortcuts.
[CHECKPOINT.json](CHECKPOINT.json) and its hashed files are preserved as the
prior checkpoint. The latest checkpoint is `layer/CHECKPOINT.json`.
The YM-C2 checkpoint remains in `one_shot/CHECKPOINT.json`; its root README
hash refers to the historical version in commit `01b05ecab`, before this
entrypoint update. Its mathematical proof and source files remain unchanged.

The user subsequently authorized committing and pushing both checkpoints;
this supersedes the earlier session's no-commit scope in `CONTRACT.md`.
These are repository research notes. The published preprint and Zenodo
record have not been revised by this attempt.
