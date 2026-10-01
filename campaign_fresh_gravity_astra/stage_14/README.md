# Checkpoint: an explicit continuum gap beyond the first scale turn

2026-09-30, 08:26 UTC pass. Parent: [stage thirteen](../stage_13/README.md).
This is a conditional result for the diagnostic Q scalar-plus-scale wall model.
The physical theory, metric/photon coupling and observational adequacy remain
open. No RAR or registered M stability conclusion is obtained here.

## One specified background, no sampled-orbit certification

In declared dimensionless units set C=cs²=J=S0=tau=sigma=1. The initial data
are B=rho=1, chi=0, chi'=1/10000. The selected full interval ends at D=.01.
All physical source and coupling scales are explicitly restored in the proof;
physical G is absorbed into the density unit, not set to one.

A compact analytic box controls B,rho,g,chi and chi' for the whole interval.
Integrated differential inequalities stay strictly inside every box face,
which excludes a first exit and proves existence through D. Q constitutive
source balance B'=rho and both dynamical field kinetics are retained.

The scale-gradient derivative lies strictly between -.84 and -.09. Its first
zero is between1/8400 and1/900; the same full interval therefore extends at
least2/225 reference lengths beyond that turn. Root's separate certificate
uses a weaker bracket(.0001,.00125) and post-turn extension>.00875; these are
consistent enclosures. No numerical orbit or mesh eigenvalues were used.

## Full continuum energy bound

The original quadratic energy, with zero Dirichlet perturbations, obeys

    Q2 >= (2/5)||u'||² - 9||u||²,
    Q2 >= (3999/10000)||u'||²,
    Q2 >=35991||u||²,
    Mkin <=(11/10)||u||².

Hence the complete generalized longitudinal squared-frequency infimum is at
least359910/11, exceeding32700 in these units. The proof uses coefficient
bounds, explicit Young inequalities and Dirichlet Poincare. It controls the
fluid displacement, scalar potential and scale perturbation together, without
replacing the fields by instantaneous responses or dropping wall compatibility.

For arbitrary fixed reference length Lr and acceleration ar, physical squared
frequency is bounded below by (359910/11) ar/Lr. The chosen couplings are
cs²=ar Lr, J=ar² Lr², S0=ar², tau=1/(ar Lr), sigma=ar Lr. These are illustrative
model choices. The worker additionally gives the equivalent cs=10^6 m/s
parameterization Lr=cs²/ar and symbolic restorations for both a0 values and
separate constant-vacuum/frozen H(z=3) references. Some physical couplings and
background densities change across that family; it is not a common fixed-
parameter observational comparison or actual cosmological evolution.

The certificate remains inside a strong short-domain sufficient regime. It
does not demonstrate stability after that earlier bound fails. Its advance
is a specified continuum gap and a finite post-turn domain, where the earlier
result gave only an unspecified positive margin/extension.

## Evidence, controls and remaining gap

Root supplied the initial candidate box and constants to the author; their
reconstruction is not independent discovery. A separate reviewer audits root's
proof without reading the new worker derivation/code. Exact rational checks
verify the arithmetic; the analytic enclosure and energy argument supply the
continuum implication. Negative controls reject a false A>=1 bound, a
noncertifying larger-domain formula, incorrect Young allocations and omitted
boundary terms outside the stated perturbation domain. None proves a new
physical instability.

- [Root derivation and physical scaling](gap_audit/ROOT_DERIVATION.md)
- [Root rational certificate](gap_audit/run_001/results.json)
- [Independent audit](gap_audit/INDEPENDENT_AUDIT.md)
- [FGF027 reconciliation](../../deepseek_push/astra_spawn_ideas/fresh_gravity_followups/reviews/FGF-027_RECONCILIATION.md)
- [Coordinator receipt](COORDINATOR_VERIFICATION.json)

Mass is conserved under perturbations of each slab, while wall values and
background mass vary across prefix lengths. No free-boundary, nonlinear/3D,
filtered-MONO or metric theorem follows. Actual a=ar exp(chi) still varies,
so the literal constant-vacuum actual-scale interpretation remains unresolved.
Both registered normalizations and distinct reference histories are preserved
without identifying them as the same physical branch.

Next FGF029 tests the recorded pressure-support assumption. A new FGF030 task
asks whether one fixed set of physical couplings, rather than rescaled family
parameters, supports a controlled comparison across the two normalizations
and one declared frozen-H reference. Neither task has been launched here.

Live handoff: 30 tasks, 17 reviewed and 13 ready, none running. Two bounded rational certificates validate. FGF029 next priority; FGF030 fixed-coupling comparison unlaunched. Primary AS228 repair remains with its owner.
