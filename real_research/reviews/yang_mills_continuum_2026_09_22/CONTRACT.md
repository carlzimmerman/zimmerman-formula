# Yang–Mills continuum research checkpoint YM-C1

Base: `b73311096299e2f1816be00036ccdb2922bc44d4`.
User objective: solve the Yang–Mills existence and mass-gap problem from the
published fixed-lattice spectral work. This objective is not replaced by a
fixed-spacing theorem, scalar certificate, or conditional continuum statement.

Target: for every compact simple gauge group, construct a nontrivial quantum
Yang–Mills theory on R^4 with the required axioms and positive physical mass
gap. The initial concrete model is pure SU(N), fixed N>=2, in 3+1 dimensions;
an SU(N) result alone does not discharge the all-groups target.

Starting theorem: the I15 proof at this base gives a full-space one-plaquette
comparison at x=g^2>=2 and an open-volume, N-uniform fixed-spacing gap
>=3x/16 for x>=X_d, using Yarotsky's theorem. It does not control x(a)->0
or construct continuum Schwinger functions. Physical energies carry a factor
1/a, in units hbar=c=1.

Proof requires an actual construction and unconditional estimates, including
all limiting maps and a nonzero physical observable sector. Finite numerical
evidence, perturbative beta functions, existence of a finite-volume eigenvalue,
or hypotheses equivalent to the missing gap count only as partial progress.

## Route ownership

- `rg/`: exact renormalization/strong-coupling bridge and source theorem
  dictionary; owner ym_rg_bridge. Test whether available ultraviolet control
  supplies the needed vacuum-subtracted spectral comparison.
- `vacuum/`: ground-state transform and coercivity; owner ym_vacuum.
  Derive a precise weighted Poincare target and test possible curvature or
  comparison shortcuts at weak coupling.
- `continuum/`: continuum spectral transfer and nontriviality; owner
  ym_continuum. Prove the strongest exact transfer lemma and falsify insufficient
  formulations using explicit examples.
- `blocking/`: root agent. Develop and test an exact spectral comparison for
  a proposed block reduction, including eliminated modes and accumulated error.

Subagents may write only their route directory, with sources and exact
obstructions. No publication, commits, or edits to the released paper in this
attempt. Root reconciles the mathematical results and maintains the live
checkpoint. No automatic claim of a breakthrough based on agent agreement.

Next cycle: use the first decisive route results to select and execute a
further implication; preserve both surviving lemmas and failed shortcuts.
