# CFG951 AMENDMENT A1: POST HOC (2026-10-21, after the first full MAIN run). Reported only; no class changes

**When.** Written after the first full MAIN run, whose outputs are kept unchanged as `cfg951_RUN1_toyartefact.out` and
`cfg951_results_RUN1_toyartefact.json`. It is therefore post hoc. Nothing in `FROZEN_CRITERIA.md` (a29366301) is edited.

## What was found
In the (d) merger toy, the frozen rule takes τ₁ (label 1's medium tidal tensor at the secondary's centre) from label 1's iterated C2
medium in monopole form. In that form the off-centre secondary (its baryons and its retained medium) enters label 1's spherically
averaged source as a shell at r ≈ d. This raises label 1's local medium density toward its enclosed mean, so
|τ₁(d)| = (√6/3)·4πG|ρ₁(d) − ρ̄₁(<d)| dips toward zero. The secondary's L2 domain then jumps to its cap: for q = 1 (canonical),
r_dom ≈ 170 kpc at d ≈ 260 kpc rises to ≈ 1480 kpc (the cap, r_ta,2) near d ≈ 100 kpc, and falls back to ≈ 150 kpc at d ≈ 70 kpc.

This is an artefact of smearing a single off-centre source into a spherical shell. It is not present in the cluster runs (the host
is sourced by a smooth member population), the Bullet (isolated progenitors' own media, as CFG916) or the UDGs (the β-model field).

## What is added (reported, no class weight)
The same toy is also run with τ₁ from label 1's **isolated** medium. This is CFG945's own L2 convention and the one this lane uses for
the Bullet. With it, r_dom(d) is smooth (r_dom = d for q = 1). The frozen metric, the M1 instantaneous jump and the fixed-configuration
diagnostic are all reported for both τ₁ forms.

A scratch probe made before this file (outside the repository; not a result) showed the isolated-τ₁ toy also far above the 5% line.
The rerun from the final script is the record.

## What is not changed
- **The (d) class** is graded on the frozen τ₁ exactly as frozen. If the isolated-τ₁ variant gave a different class, the README
  would say that (d) is artefact-dependent. It does not hide either number.
- Every other test, class rule and K / MUTATE item.

## Also disclosed here (implementation-stage changes made before the full run)
- **(d) metric.** The first smoke implementation of (d) graded a label-induced change accumulated at fixed configuration, which is not
  the frozen metric. Before any full-data run it was replaced by the frozen metric (the change of E_v = M_v/M_GP − 1 over windows of
  one t_dyn). The fixed-configuration number is kept as a labelled post-hoc diagnostic. The toy does not depend on the cluster sample,
  so the 4-cluster smoke run showed real toy numbers under both metrics.
- **Bullet stellar trigger.** After the smoke run showed the coalescence trigger r_dom ≤ r_½,b firing at the present separation (the
  record's progenitor baryons are cluster-extended, r_½,b ≈ 531 kpc), a diagnostic with the sub's stellar half-mass radius was added.
  It is reported only (POST HOC, no weight).
- **Smoke runs** (`CFG951_NMAX=4`) wrote only outside the repository (`../_external_data/cfg951_work/`).

**Reruns.** COMPUTE, K, MUTATE and MAIN are rerun from the final `cfg951.py`. The COMPUTE arrays are checked against the first run's
arrays.

κ = ½ FITTED; footings never pooled; not theory closed.
