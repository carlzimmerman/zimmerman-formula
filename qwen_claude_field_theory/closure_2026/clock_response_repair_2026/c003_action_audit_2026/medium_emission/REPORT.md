# Necessary clock-medium emission gate

Verdict: **kinematics alone is incomplete as a realization of the requested process**. Within the specified fixed-mass nonrelativistic model, release-free emission has a speed threshold and strictly *cools* the tracer. Positive internal release permits emission from cold comoving matter. At nonzero initial speed, a fixed release and fixed recoil cannot have isotropic recoil directions. A slower positive-energy mode can reduce the required internal-energy budget; this is not a construction of a classical clock interaction or a new particle-DM model.

## Contract and direct derivation

Work in the local preferred frame. The tracer has stipulated fixed inertial mass `m>0`, initial velocity vector `v`, final velocity `v-p/m`, and loses internal energy `Delta>=0`. The outgoing medium excitation is assumed to carry conserved momentum vector `p` and positive energy `c_s |p|`, with `c_s>0`. This energy-momentum assignment itself needs to be justified by the eventual field action; a mode's wavevector is not automatically the complete physical momentum of a medium.

Let `q=|p|>0`, `w=q/m`, `v=|v|`, `mu=cos(theta)`, and `d=Delta/m`. Momentum conservation is built into the final velocity. The nonrelativistic energy equation is

\[
 \tfrac12m v^2+U=\tfrac12m|\mathbf v-\mathbf p/m|^2+(U-\Delta)+c_s q.
\]

Expanding gives the exact identity *within this Hamiltonian approximation*

\[
 d=c_s w-vw\mu+\tfrac12w^2,\qquad
 {\Delta K\over m}=\tfrac12w^2-vw\mu=d-c_s w.
\]

For `v>0`, the necessary angular support for a specified positive recoil is

\[
 \mu={c_s+w/2-d/w\over v},\qquad
 \left|c_s+w/2-d/w\right|\le v.
\]

These are support equations, not a differential emission rate. A supported event may have zero amplitude. A spherical ensemble of initial velocities may yield rotationally symmetric ensemble emission while each particle has strongly direction-dependent recoil; that does not establish isotropic kicks conditional on its initial velocity.

## Zero internal release

For `d=0`,

\[
 \mu={c_s+w/2\over v}>0,\qquad
 0<w\le2(v-c_s),\qquad v>c_s,
 \qquad \Delta K=-mc_s w<0.
\]

Cold comoving flow cannot radiate a nonzero positive-energy excitation. A local speed threshold is available, but it selects relative speed, not virialization or halo membership. Fast coherent flow can also satisfy it. Every allowed event removes kinetic energy; the recoil is correlated with the velocity. The positive term `w^2/2` in the expansion does not make the complete change positive because its cross term is constrained by energy conservation.

For a fixed 650 km/s recoil, the threshold is stronger than merely `v>c_s`: `v>=c_s+325 km/s`. The limiting equality is a collinear supported event, with phase-space measure/rate undetermined. Values `c_s=300` and `537 km/s` therefore require respectively `v>=625` and `862 km/s`. Values `c_s=1` and `10 km/s` give `326` and `335 km/s`. These are parameter examples only, not empirical sound-speed or forest constraints. Generic sufficiently small recoils start above `c_s` itself and could occur in any flow with that relative speed if the interaction permits them.

Thus the release-free variant provides a cold kinematic cutoff but reverses the desired heating sign. This conditional obstruction is robust and formalized in Lean.

## Positive release

For `d>0` and `v=0`, the unsquared energy equation has a positive solution

\[
 w=\sqrt{c_s^2+2d}-c_s>0.
\]

More generally, every direction `mu in [-1,1]` admits a positive root if recoil magnitude can vary:

\[
 w(\mu)=v\mu-c_s+\sqrt{(c_s-v\mu)^2+2d}>0.
\]

Its kinetic effect is `m(d-c_s w)`, which can be heating or drag depending on the event. Internal release therefore removes the purely kinematic cold protection. A coupling, selection rule, state-preparation mechanism, or energy reservoir that switches off on the cold state would have to establish that protection dynamically.

For fixed `d` and fixed `w>0` at `v>0`, only one `mu` is allowed. In particular, forward and backward emission would require releases differing by `2vw`, and cannot both use the same release. Full conditional angular isotropy is impossible under those fixed quantities. This is not an obstruction to isotropy of a population after averaging over its initial velocity directions.

One useful explicit case is `d=c_s w+w^2/2`. It gives `Delta K/m=w^2/2>0` and the requested fixed recoil at rest, but also permits cold emission. For moving tracers, fixed `d,w` require `mu=0`: the recoil lies in the transverse plane, not on the full sphere. Thus positive heating itself is possible; the missing conjunction is positive fixed-magnitude *isotropic* heating together with cold shutoff.

Allowing direction-dependent release `d(mu)=c_s w+w^2/2-vw mu` can support a fixed recoil over the sphere if a reservoir can provide those transitions. Requiring `d>=0` for every direction further demands `v<=c_s+w/2`. For higher initial speeds, some directions require internal-energy absorption instead of release. These are new reservoir/interaction obligations, not consequences of the dispersion law.

## Energy budget and finite reservoir

The following examples choose the cold fixed-650 release `d=c_s*650+650^2/2`. The heating fraction is `650^2/(2c^2)=2.35047324e-6`; the rest is energy carried into the clock mode. Using `c=299792.458 km/s`:

| `c_s`, km/s | Required `Delta/(mc^2)` | Mean reservoir fraction for illustrative `n=2.3077948724637416` |
|---:|---:|---:|
| 1 | 2.35770547e-6 | 5.44110059e-6 |
| 10 | 2.42279550e-6 | 5.59131503e-6 |
| 300 | 4.52014085e-6 | 1.04315579e-5 |
| 537 | 6.23417826e-6 | 1.43872046e-5 |

The `300–537` and `<=10` values are stipulated parameter illustrations, not derived bands or observational certificates. The mean merely multiplies a supplied count mean by a fixed event cost; no Poisson law or emission rate is inferred here. Compared with an ordinary massless relativistic isolated decay, the slow mode can make the energy cost quadratic in the tracer velocities, of order `(c_s/c)(w/c)+(w/c)^2/2`. That repairs the *size of a possible supplied reservoir budget*, not the missing dynamics.

Bookkeeping is exact in the stipulated model:

\[
 U_N=U_0-\sum_{j=1}^N\Delta_j,\qquad
 K_N-K_0=\sum_{j=1}^N(\Delta_j-c_s q_j),\qquad
 U_N+K_N+\sum_{j=1}^Nc_s q_j=U_0+K_0.
\]

A nonnegative finite reservoir requires `sum Delta_j <= U_0`. For a fixed positive release it permits at most `floor(U_0/Delta)` emissions without pumping; it cannot implement an untruncated Poisson count for all histories. Release-free events instead use the kinetic reservoir and reduce the speed, potentially below the emission threshold in one event. These identities do not include reabsorption, forces, or time-varying `c_s`; such exchanges must be added if present.

The inertial mass is held fixed because that was the requested nonrelativistic Hamiltonian. In a fully relativistic completion, depletion of internal energy changes inertial/rest mass and introduces corrections; the displayed `Delta/(mc^2)` is a budget estimate, not an exact relativistic two-body mass formula.

## Exact missing action-level input

An eventual classical clock-plus-matter action must identify a positive-energy propagating medium mode with the stated dispersion, the complete conserved stress tensor, and an interaction that produces a calculated momentum-transfer spectrum. To recover the proposed phenomenology, it must additionally provide a physical internal-energy or background reservoir, show why the transition amplitude vanishes for cold single-stream matter, derive a rate tied to the desired state, and produce the required angular and magnitude statistics. None follows from `omega=c_s |p|` alone. A force correlation derived by integrating out existing classical field modes is one possible object to calculate; it must include the compensating energy/momentum transfer and any drag, rather than imposing a noise kernel by hand.

Primary conclusion: **the slower-dispersion escape remains open only with extra dynamical input**. Release-free kinematics is incompatible with positive heating. Positive release allows heating but does not kinematically enforce cold shutoff, and constant release plus fixed recoil excludes conditional isotropy at nonzero speed. No theorem here rules out all interacting classical clock actions.

## Evidence and source boundary

Used computation-audit/proof-audit for the contract and conservation checks, with conservative proofread-math self-review. No external theorem is invoked: all relations are direct expansions of the explicitly supplied nonrelativistic energy and momentum equations. No web source or empirical statement is needed or claimed.

`audit.py` checks four exact symbolic identities, four cold constructions, and a 45-point exact radical grid for positive-release support, then invokes existing Lean. `MediumEmission.lean` proves six algebraic lemmas: energy partition, release-free drag, the strict small-recoil threshold, positive release required at rest, incompatibility of both opposite directions at fixed release/recoil, and complete reservoir bookkeeping. All six compiled on the first run, exit 0, with only standard `propext`, `Classical.choice`, and `Quot.sound`; no user axioms or `sorryAx`.

The version-2 manifests record actual commands, input/output hashes, software, Git dirty state, execution time, and exit 0. `run_001` is the original computation; `run_002` is the current-input rerun after correcting a source comment from 50-digit to 30-digit display. The mathematics was unchanged. The existing raw Lean path and LEAN_PATH are captured in `results.json`; no dependencies were installed. No failed scientific run occurred in this bounded calculation. The original recoil subtree was not modified. The exact command and hash record are in `RUNS.md`.
