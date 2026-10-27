# Result and audit of the bounded kinetic route

**Primary verdict: conditional energy-transfer construction; no derived stable
surface-density floor.** The kinetic conservation and entropy statements are
analytical under the regularity and positivity assumptions in DERIVATION.md.
The stopping statements are finite toy-model evidence plus the displayed local
stability calculation. No fundamental cold-field action is supplied.

## What was executed

The pre-run contract is CONTRACT.json. The bounded runner used the exact command
recorded in run_001/manifest.json, with 30 seconds wall time, 20 seconds CPU,
1 MiB output and one numerical-library thread. The run completed, exit 0, and
the manifest validator confirmed current input and output hashes. No random
sampling or halo simulation was used. All 13 declared checks passed.

* Two exact elastic reaction channels preserve mass, three momentum components
  and kinetic energy. Their chosen off-equilibrium occupancies have
  dH/dtau=-2 log(2), strictly negative.
* An exact positive eight-beam example has rho=1/10, u=0,
  Pi=diag(1/5,1/10,1/10), det Pi=1/500, and q=(1/10,0,0).
  With P_star=1 the stress valve is off although heat is transported. This is a
  counterexample to collision-off implying energy-flux-off, not a halo model.
* In the fixed-mass homologous two-zone reduction, hotter-envelope evolution
  reaches s=1 and Sigma/Sigma_star=1 to numerical tolerance.
* A cooler envelope instead reaches s=10, Sigma/Sigma_star=100, at tau=4.0083.
  The calculation stops there; no finite-time singularity was established.
* An initially below-floor core remains at Sigma/Sigma_star=0.81.
* A small positive-capacity envelope equilibrates above the floor, at
  Sigma/Sigma_star=1.44.
* A heat impulse of +0.05 C0 T_star after stopping leaves the core at
  Sigma/Sigma_star=0.9025; the inactive valve never restores it.
* Closed-system energy residuals are below 6.1e-14; the external impulse is
  separately accounted. Entropy production is nonnegative in every trajectory.

The expansion branch therefore demonstrates a possible one-sided stop at an
INSERTED threshold. The other cases invalidate interpreting that example as a
robust two-sided floor or a universal final state.

## Two structural deductions beyond the finite checks

**Passive fixed baths give the wrong restoring sign.** For C_c<0 and a passive
heat flux Q_c=K(T_h-T_c), linearization at T_c=T_h gives
d(delta T_c)/dt=-(K/C_c)delta T_c, which grows. A positive heat-capacity finite
envelope stabilizes thermal equality only if C_h<|C_c|, as section 4 derives.
That stable temperature is set by the total energy. It does not by itself
produce a universal pressure across different core masses and histories.

**An active relaxation operator does not select Burkert.** Its second central
moment obeys

    (d Pi/dt)_coll = -Gamma (Pi-p I),
    (d tr Pi/dt)_coll = 0.

It isotropizes local stress, without changing its trace. In a static no-flow
region that is both locally Maxwellian and in exact kinetic equilibrium, insert
f=rho(2piT)^(-3/2)exp[-v^2/(2T)] into the streaming equation. The cubic velocity
coefficient requires grad T=0; the linear coefficient then requires
grad ln rho=-grad Phi/T. This is the isothermal relation, not an independently
selected Burkert profile. A transport state or a collisionless frozen remnant
can differ, but its profile must be derived separately. The coefficient C_B in
the target P_star cannot be justified by presuming the desired remnant.

## Scope relative to recent lanes

X54/X60 concern rest-energy conversion and vacuum transport. This construction
conserves cold mass and uses internal kinetic/gravitational energy. X57-X64's
retention keys classify which objects keep cold mass; this construction does
not remove the cold halo. Thus their specific exclusions do not dispose of this
operator, and their galaxy-lensing normalization tension remains unresolved.
CFG351 supplies prior art for the rank-sensitive activation variable, not a
microscopic mixing mechanism or a selected pressure.

## Exact remaining obligation

Produce the cold-field interaction that supplies the transport kernel and
derives its pressure dependence. Then show that the total flux, including
ballistic and gravitational work, stops or restores at the same surface density
under different envelope energies, mergers and finite primordial dispersions.
The present effective construction makes those obligations explicit; it does
not meet them by replacing a free beta with the desired Burkert coefficient.

Review provenance: derivations and finite implementation self-audited by the
kinetic-route subagent. The code and results are available for an independent
parent/sibling review. The inherited Burkert pressure coefficient was independently
audited in the preceding task; it is used here conditionally on that profile.
