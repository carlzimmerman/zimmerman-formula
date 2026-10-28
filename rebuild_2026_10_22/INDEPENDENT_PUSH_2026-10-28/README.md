# Independent push: useful new data and a material equation/code mismatch

Checkpoint **IP28**, 2026-10-28. Base git
`7954d48377463cafcae3e8dbb09454134aef384f`, with existing dirty work preserved.
The requested investigation advanced all named issues. It did **not** derive
kappa or a condensation field equation, and the native ng64 result is pending.

Read the [corrected current theory](CURRENT_THEORY.md) for the equations
actually implemented. The earlier equation page remains historical evidence.

## L and T: the strongest correction

The selected successful model has **mass-dependent core concentration** but
computes its threshold with a **constant concentration level**. They share L,
but are different prescriptions. At L=3.75, canonical log10(T/Msun)=12.23568
for the implemented switch; the X43/background-A EPS core calculation crosses
its floor at 11.22322 under the inherited S9 interpolation/clamp. The isolated
lensing pipeline's coarser collapse interpolation shifts that value slightly.
At 10^12 Msun the core
term is already 1.56478 times the floor while the switch still says no halo.

Thus the written single surface-density rule has not been validated by the
existing calibration passes. This is an equation/code equivalence failure,
not a claim that the recorded implemented-model scores were miscomputed.
The independently coded scalar CLASS/EPS calculation reproduces all six
stored CL3 threshold roots to 1.78e-15 dex.

The compact page also overstated universality: the 5.2715-times-baryons
turnaround budget is a cluster prescription, and BS1's basin flag does not
replace the own-mass flag in every pipeline. The corrected page identifies
BS1's primary versus its reported CL3_L3.75 variant and each prescription's scope.

NL1's primary verdict fixes logT=12.3. Its separately reported linked-T grade
does not veto a primary success. Existing L=4 is a counterexample to the
claimed implication: fixed-T passes, linked-T fails lensing at Delta chi²
=+22.3948. NL1 also applies a canonical-only threshold approximation to alt,
missing its root by about 0.337 dex at the recorded settings. Native L itself
requires an untested transfer of dwarf-scale resolution correction to cluster
mass, and its bootstrap omits reference-ensemble uncertainty.

Nine zooms and the existing NL1 follower were observed live; none was restarted
or duplicated. No completion ETA is inferred. Exact observation times and
conditions are in the [L/T audit](native_l_t/README.md).

## Observations: three barriers became more specific

| Issue | New evidence and implication |
|---|---|
| SLUGGS | Recovered measured gas temperatures for all four targets: M87 1.85, NGC4365 0.44, NGC4374 0.81, NGC5846 0.79 keV. The temperature-data gap is filled. A conditional hydrostatic/Jeans check gives mixed offsets, not a universal cure; aperture coverage and gas-model systematics prevent a clean theory regrade. |
| IC 1613 | A published stellar-tracer inclination is 32±11 degrees. An optimistic rescaling of the entire old tabulated speed would move the canonical residual from -0.593 to -0.299 dex and erase it at 22.06 degrees. But that speed already includes asymmetric drift: the correction is not all proportional to 1/sin(i). These numbers bound a possible correction under a fixed positive drift term; they are not an inclination refit or a pass. Stellar rotation and estimator limitations also prevent treating the old 7.9-sigma figure as complete. |
| X-ray groups | Recovered all 26 CLoGS high-richness rows, including 14 group-scale hot halos. Only NGC4261 supplies an additional eligible hot-halo association under the checked original footprint/membership conditions. It is already labelled FAINT with zero gas mass in HG1/HG2 and lies in a shared sigma bin. The physical control includes known hot gas. Its detected gas reaches 85 kpc at the source distance, or 87.8 kpc at the group's test distance, versus the test radius 619 kpc; gas normalization and selection sensitivity still prevent adding a graded group or changing D. |

Primary sources: [Babyk et al. 2018, arXiv v1](https://arxiv.org/abs/1803.00020v1),
[Taibi et al. 2024, published article](https://doi.org/10.1051/0004-6361/202449468),
and [O'Sullivan et al. 2017, arXiv v2](https://arxiv.org/abs/1708.03555v2).
The [observational report](observations/README.md) contains exact table
locators, distance conversions, aperture diagnostics, match exclusions,
small retained data tables and source hashes. No old grade was overwritten.

## Basin and kappa: scoped obstructions, not invented closure

The turnaround acceleration proposal fails on the inherited Local Group
geometry directly: g_N/a0=0.00582 and simple-law g/a0=0.07926, despite its
canonical basin mass exceeding the switch. A finite-age spherical Newtonian
calculation gives a critical mass 7.94e19 Msun with vacuum, or 1.47e20 without
it, at the inherited 13.821-Gyr age. A dynamically distinct simple-law toy
gives 3.27e19 Msun. These conditional diagnostics support the enormous scale
gap, not one unique threshold or a cosmological completion.

A smooth exterior spherical annulus can change total basin mass across T
while leaving all interior local force information unchanged. That obstructs
a universal force-only local implementation of the basin flag in the stated
Newtonian/AQUAL class. Separately, pressureless Newtonian collapse at fixed
scaled initial profiles has no absolute mass selector. Neither result rules
out nonlocal state, boundary information, mass-dependent formation histories,
or additional microphysics.

The normalization audit distinguishes a field convention from the observable
kappa. Rescaling the field leaves kappa unchanged. Under the specified vacuum
identification, an unconstrained additive constant C gives kappa²=8 pi/C;
choosing C=32 pi merely imposes kappa=1/2. The missing physical matching
principle remains open. See [derivations and numerical evidence](basin_kappa/README.md).

## Alt footing and verification

An independent stored-output recount finds 14/72 canonical combined passes
and 0/72 alt passes across the specified related configuration evaluations.
Alt's SPARC scatter passes; its fitted stellar mass-to-light ratio misses the
frozen calibration interval, and its dwarf failure remains. That licenses
“unsuccessful under the current joint criteria,” not “fails every observable.”
Canonical remains the baseline and alt a separate diagnostic under the
standing rule. [Footing audit and controls](footing_audit/README.md).

All new work is inside this directory. Criteria were written before new
executions and hash pinned; they were not committed because .git is read-only.
The packages retain deterministic checks, deliberate failing mutations,
input/output hashes, commands, model assumptions and execution limitations.
Fresh normal-run checks establish their stated finite assertions; they are
not certificates for the complete astronomical theory.

The next work is ordered by dependency: reconcile the two core/switch
prescriptions before interpreting NL1 as a physical derivation; require an
exact separate-footing linked-T grade after the zooms; build a joint IC1613
HI/stellar comparison; and resolve radial gas support and physical hot-halo
classification before expanding the group statistic. The exact continuation
conditions are in [HANDOFF.md](HANDOFF.md).
