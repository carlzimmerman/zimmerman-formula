# AZ43 — FN6 robustness, lane9

Freeze before computation. Basebca9ca8282. FN6 small/MW engines, their
source dependencies, FN1b validation lines and UX5/X5 priors inspected.
Kappa=1/2 FITTED; not theory closed. This grades FN6's Gaussian form R,
not the native v3s action. Both footings9.3603e-11 and1.1312e-10 are
reported separately. No new data or changed observational tolerances.

## Frozen parameter and cell grids

p=.250,.275,...,.500 (11 values). L_MW=1.00,1.25,...,3.00kpc, plus
1.450,1.475,1.525,1.550kpc (13 distinct widths,143 parameter points).
These grids are robustness brackets, not adjusted after results.
M0=6e10 Msun and each system's mass convention remain FN6's.

For the MW, use the full tensor product around the canonical survivor:

 - sb=48.8,50.5,52.2 Msun/pc²;
 - mbb=2.00e10,2.06e10,2.12e10 Msun;
 - rd=2.6-1/12,2.6,2.6+1/12 kpc;
 - ht=.325,.3375,.350 kpc;
 - hk=.990,1.035,1.080 kpc;
 - fk=.305,.3275,.350;
 - box=BV2,rdk=2.0 fixed as in the original survivor.

There are729 raw cells, filtered by the unchanged RD_TAG and MSTAR_TAG
priors. Upper-edge coordinates are refined inward, never outside the
original parameter range. Preserve a tag for the exact old survivor.
This is a local robustness domain, not the entire original MW prior;
a disappearance in this grid does not exclude all distant cells.
The broader old in-prior1375 cells are not silently substituted for this
new local domain. Report old and new grid counts with their domains.

## Observables and labels

Use FN6's existing engines read-only, and the same T0-T4 observation
definitions and thresholds. T0 is all four UX5 lines (L1,L2a,L2b,L3),
T1 Q2<=5.2e-27s^-2, T2 at least15 of24 dwarfs within2sigma for some
Upsilon in the unchanged41-point[1,3]grid, T3 SURVIVES SPARC (d_rms
<=.005 and |median residual|<=.05), T4 worst planet Z<=2. Retain the
original sample cuts and E1 host field. Report individual failures.

For each footing report the parameter cells passing all five gates,
number of passing MW cells and survival of the old exact cell. WINDOW
means at least one numerically evaluable parameter/cell survives; FAIL
means no survivor in this specified local grid and all decisive gates
are numerically evaluable; UNDECIDED if a numerical uncertainty can
alter that conclusion. "Widens" means new local cells/parameter points
survive, not a measured probability or a larger confidence region.

## Convergence and known answers

Before production reproduce p=.35,L_MW=1.5 from FN6 for both footings:
T1-T4 counts/labels identical; numerical scalar observables relative
difference<=1e-8 at the identical discretization. Reproduce its old MW
survivor at refine1, scalar observable relative difference<=1e-8.
An alternative implementation of a smoothing operator must agree with
the original to1e-10 relative on deterministic nonzero fixtures before
use. This tolerance covers floating-point reduction differences only.

Small-gate numerical pairs: dwarf radial2000/4000; SPARC1500/3000;
Cassini radial/angular quadrature orders doubled; planet outer radial
20000/40000 and angular160/320, orbital256/512. Analytic large-width
formulas are exact in their approximation and retain FN6's numeric
20/50rM validation at the original2% lines. V4 reciprocal identity
<=1e-3 is unchanged. MW refine1/2 with full even angular rank, same
120kpc filter cut and density quadrature. Retain V1(a,b) at the actual
min/max local widths for each parameter point/footing (dv<=.3km/s,
Ou dv<=.5km/s,dK<=.3Msun/pc²).

Convergence lines for grading: MW |dK0|<=1Msun/pc² (inherited FN1b)
and |dvc|<=.3km/s (engine resolution line), no four-line pass flip;
T1/T4 relative difference<=.02 and no pass flip; T2 individual fitted
dispersion change<=.01 relative and no dwarf pass flip; T3 d_rms and
median changes<=.001dex and no label flip. Dwarf1% is below its
measurement uncertainties; SPARC.001dex is one fifth of the narrowest
.005dex grade interval. Rows missing these are unresolved, not rounded
onto the passing side. Preserve coarse and fine outputs. No tolerance
changes after results. Failure of an independent decisive gate may
still rule out a point whose other gate is unresolved.

## Mutation and process

MUTATE changes only the phantom enhancement to zero (nu=1), including
its derivative, and uses separate outputs on the same parameter grid.
The old-anchor reproduction check must fail. Record which physical
gates it defeats; do not assume every observational gate must fail.
Known Newtonian limit must pass. A failed anchor in the deliberately
altered twin does not stop its numerical validation/physical reporting.

Checkpoint per parameter/cell or individual galaxy/dwarf with atomic
replace and hashes. SIGTERM/SIGINT sets a flag and exits75 at a safe
boundary. Resume only identical-input checkpoints. Demonstrate resume
against an uninterrupted small fixture before any queue use. Default
one thread, child memory guard near1GB and bounded batches lasting
minutes. Chunk radial kernels if necessary; validate against originals.
If a job cannot stay light, stop it and record the required queue work;
do not bypass the brief's heavy-work ordering. Preserve old folders.
No downloads, deposits, sends or pushes. All free p,L_MW and baryonic
grid choices are FITTED/bracketed, never inferred action constants.
