# State-preparation checkpoint and continuation

Original goal remains open: derive a microscopic charge/energy-conserving medium
that produces tethered disks and free mass in dwarfs/clusters with common
parameters, preserving acceleration and lensing constraints without labels.
User authorized persistence and pushing findings. This is a substantive checkpoint,
not a declaration that the research program is complete.

Base published checkpoint: fd502a8f56846535ea2126b2ef667b1f1e005fdf on
codex/two-state-mechanism-findings-2026-10-24. Work in this stage only; main checkout
has substantial unrelated work and must not be staged/reset. No active jobs.

## New evidence

- Explicit quadratic gapped preparation, initially m=1,t=.1, ending e=.01,m=0.
  Angular schedule gives diagonal source error0.003937747; linear schedule0.18984.
  Finite hold average1000..2000 gives0.00392653 at1536 modes. Positive work3.097736.
  17 midpoint runs and4 independent ODE/hold checks, all sources pinned.
- Exact blockwise covariance invariant gives a best diagonal error floor:
  .00363943 for gapped initial state,13.0267 for gapless initial state at t=.1.
  Does not constrain interacting entropy transfer or all coherent observables.
- Contact mean-field mass lambda>1: m=(lambda²-1)/(2lambda), derives gap/energy
  but not nodal phase. Field-channel feedback changes chi and characteristic
  field: chi_eff=chi_bare/delta, E_c=Lambda delta²/d, delta=1-lambda.
- Static fit diagnostic can reach.00311341 dex at lambda.3875,chi_eff138.6225,
  tested4001 x points1e-4..1e4. Fitted, not derived; no galaxy or lensing success.
- Autonomous m,pi plus live homogeneous D conserves energy. At I100,T200,
  N128/256 agrees: m_RMS .66631,meanE .0363066 vsreference.01. Energy excess8.122631
  cannot vanish in closed model. Energy error<2e-11 at N256. Other inertias not
  fully mode-converged. No spatial fields/gravity/radiation in this diagnostic.
- Joint local-unit constraints are decisive for the specified interpretation:
  rho ell=K/delta; Lambda=f a0 m_+ ell/delta²;
  m_current,max=hbar c delta²/(f a0 ell²) scalesrho² delta⁴;
  m_Fermi,min=[6pi² hbar³ rho/(nu c³)]^.25/(1+epsilon), nu8.
  Bare disk: upper2.8587e-15 eV, lower.25453 eV; canonical TRK upper9.3062e-20 eV.
  16cases0overlap. Lower density worsens gap. Requires same LOCAL fundamental
  fermionic positive-mass units and nonrel momentum envelope p<=Mc; DOES NOT
  constrain emergent fermions, bosonic units or arbitrary relativistic media.
- Independent vacuum dipole radiation bound uses same q/m and d. Disk zeta.1
  needs m_+>=9.09e-12kg for one transition/10Gyr. Collective emission outside scope.
- Source check on concrete Kitaev alternatives: physical probe matrix elements
  can change flux sector; electric-only perturbations need not linearly gap
  emergent fermions. Checked2D magnetoelectric pocket contribution has wrong
  cubic sign; checked symmetry mass is evenE. No universal3D spin-liquid no-go.

## Run state and files

Seven completed manifests: run_prepare, run_autonomous, run_refine,
run_radiative, run_combined_v2, run_hold, run_figure. One retained failed invocation:
run_combined had wrong output directory. All8 provenance records validate;
failed status is not scientific evidence. VALIDATION.json and AUDIT.md record
scope and checks. Figure checked. Do not change pinned source files without new
runs. README and live findings index can be clarified without altering evidence.

## Prioritized continuation, not an unbounded parameter scan

1. A new microscopic construction must address the simultaneous mass/current
   identification failure. Emergent fermions are a plausible route only after
   deriving physical electric matrix elements, not just their DOS.
2. Cheapest next discriminator: choose a specific3D interacting lattice/continuum
   Hamiltonian and derive its flux-preserving electric operator, symmetry action,
   and leading field dependence. Check positive |E|³ free-energy correction and
   actual spectral weights before investing in galaxy evolution. The literature
   record names tested wrong shortcuts and exact source locators.
3. Derive material rest mass/current inventory and charge compensation separately
   from quasiparticle band parameters. Reusing the failed pair inventory for a
   collective model would erase the key new constraint.
4. Only then build autonomous cooling/transport with propagating energy sinks and
   common microscopic coefficients, reconnecting to live3D gravity. Existing
   controlled protocol is a reachability target, not a physical law to impose.

Untested collective constructions remain open, not exhausted. No generic cooling
coefficient, galaxy-type gate, assumed spectral density or prescribed filling
should be treated as a derived solution.
