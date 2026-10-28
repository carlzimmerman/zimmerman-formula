# CSM1: consistent mass-dependent core and switch

Checkpoint CSM1, base git2c6b17d683c1a69a1c95754c255de1cc6f79800a,
with pre-existing dirty files preserved. This contract precedes new grades.
User explicitly authorizes correcting the mismatch, rerunning the model and
pursuing whether previous passes survive without another fitted number.
Criteria are hash pinned before computation, not committed (.git read-only).

## Target and permitted correction

For S9, let q(M)=c_nat(M)/c_nat(1e14), with the existing linear-in-logM
interpolation and exterior clamp. Define

    U_f,tag(M;L) = [4/(3 B(1))] [L q(M)]^(5/4) Sigma_coll,tag(M),
    Sigma_core(M) = max(Sigma0_f, U_f,tag(M;L)),
    candidate_halo(M) iff U_f,tag(M;L) > Sigma0_f,
    Sigma0_f = a0_f/(2 pi G), B(1)=3 ln2-pi/2.

The switch must use the SAME function as its corresponding halo core, including
background, units and numerical representation. No constant-eta(L) threshold,
canonical-only T interpolation, or independent free T is allowed. Diagnostic
roots may be reported, but the direct inequality governs each actual decision.
Each scorer retains its current collapse-column representation (X43 exact EPS,
X53/HO2 tabulated interpolation); interpolation differences must be disclosed.
No blanket claim of exactly identical cross-pipeline roots.

Preserve BS1 basin membership and primary mass definition: LG is the sum of
member inferred M200 values, NOT the summed-baryon variant. SPARC, MW and dwarf
flags use the corresponding parent-column function at basin mass (own-mass
fallback for ungrouped systems). Cluster/group/isolated-lens flags retain their
own system mass where that is what the previous pipeline used. Core amplitudes
still use own mass. X51's separate cooled-dwarf profile remains its prior
construction; no universal Burkert dwarf equation is introduced.

All mass relations, backgrounds, SPS priors, cluster GS1 gas budget, GC/dwarf
estimators, covariances, profile radii and scoring cuts remain fixed. Kappa=1/2
is FITTED. Both footings are separate throughout. Basin selection is a posit.
No new physical constant, concentration shape parameter, profile radius,
normalization, gas model, halo budget or screening parameter is fitted.

## Primary finite experiment

Evaluate the previously registered L values3.75,3.9,4.0, on both footings.
The prior success to compare is the calibrated CL3 picture plus BS1's basin
extension, with L3.75 reported separately from BS1's L4/T12.3 primary.
Before corrected interpretations, reproduce appropriate old scorer controls
from actual machinery: old CL3 L3.75 own-mass SPARC/groups/clusters/lensing;
BS1 primary or its L3.75 reported-variant basin assignments and MW/dwarfs.
Failure to reproduce an affected subsystem stops its scientific verdict.

Recompute SPARC on both backgrounds,63 Tian groups,15 cluster keys in both h
cells, KiDS isolated-lens scores, five LG dwarf classes, MW box/McMillan and
field dwarf diagnostics where computationally applicable. No new kT, IC1613
inclination or group-label repair is folded into this correction. Known heldout
failures remain separately visible, even if calibration lines pass.

Frozen scoring is inherited, never loosened: SPARC rms<=0.110 and median
Upsilon in[0.50,0.80], group and dwarf class criteria, all cluster keys |Z|<=2,
and both KiDS comparisons as defined in the old grade. MW feasibility and field
S1-S3 are additionally reported with their existing criteria.

## One predeclared sole-L rescue discriminator

If none of the primary L cells passes all calibration lines, permit ONE
exploratory challenge at Lcrit solving U_canonical,A(10^12.3;L)=Sigma0.
The target12.3 is the old CL2 midpoint, fixed before CSM1 results. This is a
refit of the existing single L using old empirical information; it is not a
blind prediction or an independently adjustable T. Apply its L to every core
and every branch on both footings and regrade. Do not scan T, shape or other
constants. Failure of four tested levels alone is not a theorem excluding allL.
Scalar monotonic bounds may establish stronger restricted conclusions only
with assumptions checked on the corrected scorer.

## Checks, evidence and stopping conditions

- Record every branch's selected mass and column/floor comparison; independent
  checks must find no disagreement with the actual core-function selector.
- Baseline reproduction, hand/scalar witnesses around the crossover, units,
  input hashes and finite domain are checked before claiming a new result.
- A deliberate flag/critical-integral mutation must fail a meaningful check;
  scientific failure is distinct from an implementation/environment failure.
- Retain full scores, signs, passing/failing line lists, commands, environment,
  runtime/RSS, exact input/output hashes and manifested run status.
- Run single-threaded, nice15 if supported, <1GB per process where feasible,
  bounded minutes per scorer. No PM simulation, downloads, job duplication,
  alteration of NL1 or changes to historical lane outputs. Unsupported macOS
  RLIMIT_AS is not requested; observed RSS and time/thread bounds are recorded.

Owners: calibration/ (SPARC/groups/clusters/lensing), heldout/ (MW/dwarfs),
feasibility/ (independent scalar bounds/review), coordinator (this directory's
synthesis and reconciliation). Each writes only its assigned scope.
