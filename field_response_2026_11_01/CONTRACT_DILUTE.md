# Frozen A3: dilute-parent controls and material-core response

Written before the new control implementation or execution. The root
authorizes baseline central depths `psi_c={.2,.4,.6}` at `epsilon=.01`
to discriminate concentration-dependent behavior from a statement about
the entire chosen parent. No observed galaxy data or fitted response enters.

Use the unchanged frozen PN28 baseline module and unchanged static-response
solver. `B,k,C_s` and the canonical waterbag level stay fixed; all three
states have the same epsilon, but their dark masses may differ. Each forced
path preserves its own initial dark mass exactly through the established
outer derivative condition. Retain the same diagnostic Plummer families:

    weak_diffuse: final mb/M=.05, a/R0=.5;
    strong_compact: final mb/M=.20, a/R0=.1.

The original unforced total matter radius R0 fixes a. Run fractions `j/40`
for `j=0,...,40` independently for both families at all three baselines:
exactly 246 records including explicitly unattempted fractions after a
failure. Seed only from the previous passing state in that same family.
No alternative guess, new step size, forcing change or extra scan is allowed.
All original main solve tolerances, node budgets, mass/scalar/stress/virial/
source-sign tests and failure handling remain unchanged. This pass adds no
domain/tolerance scan and makes no stronger numerical certification claim.

Besides the existing density-defined quarter-core column, report two
material-core observables at every passing state. Let rq0 be the initial
quarter-density radius and Mc0=integral_0^rq0 n0(r) r^2 dr. Compute

    enclosed_core_mass_ratio=integral_0^min(rq0,R) n(r) r^2 dr / Mc0,
    material_core_radius_ratio=r(Mc0)/rq0,

where `r(Mc0)` solves `integral_0^r n(t)t^2 dt=Mc0` in the current state.
Both integrations concern dark matter alone, retaining the same original
core mass, not a newly selected density threshold. Independently compare
quadrature mass to `-r^2 psi'(r)-m_b(r)` at rq0 and r(Mc0), using the
original relative mass tolerance `2e-5`. Zero forcing must recover both
ratios within `5e-5`. This checks material-core contraction/expansion without
confusing a changed central density threshold with motion of the same mass.

Store all numeric state records and 400-point profiles only at fractions
`0,.25,.5,.75,1`, plus the last successful state before any failed family.
Run one numerical thread, wall cap 300 s, CPU cap 240 s, target RSS below
1 GB; do not claim unsupported macOS memory/affinity enforcement. Outputs
remain in a new run directory. Command:

    python3 field_response_2026_11_01/static_dilute.py NEW_RUN/result.json

The static experiment supplies conditional equilibria and response metrics.
It does not itself prove fluid or kinetic stability, physical accessibility,
formation, a universal column, B/V selection or an observational fit. The
root's independently contracted energy screens are separate obligations.
Failure of a continuation remains numerical inconclusiveness, not a no-go.
