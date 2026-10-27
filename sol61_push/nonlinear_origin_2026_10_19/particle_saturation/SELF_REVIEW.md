# Self-review and computation interpretation

Reviewed scope: the complete new PARTICLE_SATURATION.md and final
check_two_mode.py, contract.json, source_pins.json and run_004 results.
This is a self-review, not an independent peer audit. New arguments are
derived here; external theorems are not asserted on an unverified citation.
An ensuing independent occupied-landscape peer review identified one local
restriction now corrected in the note: with fixed finite H0,D and a simple
dmax, A=0 implies exact polarization once that common eigenvector is ground;
it does not leave a higher-order virtual-mixing correction. No computation
or parameter changed in that correction.

## Claim and dependency audit

The safe claim is conditional exact finite-dimensional response in the stated
Gaussian Galerkin subspace of the matched daughter Hamiltonian with a rigid,
freely translating host. Original action/matching are pinned parent inputs;
the host density, rigid shape, stock N and state preparation are declared
inputs. The note does not turn the variational trial subspace into exact
continuum low modes.

The dependency chain is: original matched NR action -> relative-coordinate
kinetic and full positive-mass source -> analytic spatial integrals ->
fixed-N symmetric tensor projection -> spectral/thermal response ->
finite-matrix perturbation at a simple largest source eigenvalue. Each
analytic implication is written explicitly. Numerical checks cover only
the ten declared matrices and two independent tensor-source benchmarks.

Checks reconstructed by hand during review:

- Eliminating the total COM gives T_rel=sum p_i²/(2m)+(sum p_i)²/(2Mb);
  consequently the cross-pair mass-polarization kernel is p_i.p_j/Mb.
- The host characteristic form factor is exp(-B²k²/4)cos(ka). Its recoil
  survives the heavy-host limit because Mb alpha tends to m.
- Differentiating the symmetric tensor power selects exactly one scalar
  source factor, with no extra N or factorial normalization. N=1,2 tensor
  products provide a separate numerical check.
- The contact density term is2W nL nR, pair hopping W/2, and the density
  assisted term is T(N-1) hopping in each fixed-N sector. The full tensor
  and independently expanded matrix agree.
- Ground energy -Edmax+h00-A/E yields P=dmax-A/E², with A>=0; the
  coherent minimization and noninteracting exact response agree on this
  power. Nonzero A and a simple top source eigenvalue are explicit hypotheses.
- The k=0 source is an unprojected COM operator identity, not evidence
  supplied by the code's zero return. That tautological test was removed.
- Ground/thermal spectral weights, measurement probabilities and actual
  independent host counts are different objects; the manuscript does not
  count the same N particles once per transition.

## Computation-audit outcome

Outcome: implementation and finite assertion verified in the stated range,
conditional on float64/complex128 tolerances and NumPy/SciPy eigensolvers.
The source has an independent tensor implementation for N=1,2; the contact
has an independent fixed-N closed expansion for every N; noninteracting
response, parity, Hermiticity, Kubo derivatives and analytic asymptotics
provide orthogonal controls. No interval/eigenvalue error certificate,
complete continuum spectrum or resource-truncated negative result is claimed.

run_004 status is completed, all88 checks pass, and manifest validation
against the current project input bytes succeeds. Resource contract:
45s wall,30s process CPU,1 conventional numerical-library thread,
131072 log bytes; no hard address-space or affinity restriction. The
exploratory run_001 failure and later revisions are retained and described
honestly; only run_004 is the current input-hash evidence.

## Mathematical proofreading self-review

Proofread: the complete new note and its equations(1)-(29).
- Routine edits: checked definition order, source signs, matrix conventions,
  contact factors, repeated B versus B0 names, display references and table units.
- Mathematical-token changes during proofreading: none. The independent
  contact check was an implementation-audit addition, not a proofreading repair.
- Unresolved issues: no uniquely forced typographic issue remains; physical
  and continuum obligations are explicitly open in section9.
- Validation: current runner manifest and all88 numerical checks pass.
- Coverage: this lane's new files only; no parent manuscript or action was edited.

No source/action/manuscript, global navigation, history, queue, heavy job,
publication or external chat was changed by this lane.
