# CFG114 — does the SLUGGS deficit survive GC slopes and orbits varied together? FROZEN CRITERIA

Written 2026-09-29, before any number of this lane was computed. Nothing below may change after a result is seen; any later deviation goes in the README as a disclosed departure.

## Why

Two declared ranges have each been tested alone:
- **CFG111** (6e1b04092): the GC density slopes. With every published γ_i shifted by −0.4 to +0.4, the law's deficit spans 2.3–4.7σ at β = 0.
- **CFG113** (1db2d3a69): the GC orbits. With β from −0.5 to +0.5 at the published γ_i, the minimum is 3.4σ (alt 2.9σ).

The mass–anisotropy degeneracy is joint. Lower slopes and radial orbits both raise the predicted dispersion when γ < 3, so the corner where both are favourable is the real test of whether the deficit is robust.

## The box (declared; both ranges were fixed in earlier frozen files)

- **Slope shifts:** every γ_i + δ, with δ ∈ {−0.4, −0.2, 0, +0.2, +0.4}. These are CFG111's R2 brackets.
- **Orbits:** constant β ∈ {−0.5, −0.25, 0, +0.25, +0.5}, CFG113's bracket.
- **Cells:** 25 on each footing.
- **Held fixed:** CFG55's JAM-calibrated masses, CFG55's 16 galaxies and CFG113's machinery. It is CFG111's pipeline, with β passed to h50's `sigma_r2` and `sigma_los`.

## Checks

- **C1 CONTROL:** the box's edges reproduce the committed lanes exactly (1e-9):
  - the cell (δ = 0, β = 0) reproduces CFG111's law and rule means;
  - the cells (δ, β = 0) reproduce CFG111's committed R2 (canonical);
  - the cells (δ = 0, β) reproduce CFG113's committed R1 for the bracket, both footings.
- **H1 [HEADLINE; MUTATE must fail]:** the law's JAM-calibrated SLUGGS deficit exceeds 2σ in every cell of the box, on both footings. The minimum over the box is the quantity tested.

## Reported rows

- **R1:** the full box of the law's σ on both footings, with the cell where it is smallest.
- **R2:** the rule's box on both footings, and the cells where |z| ≥ 2.
- **R3:** the number of cells, out of 25, where the law exceeds 2σ, on each footing.
- **R4:** at the law's most favourable corner, the law with SLUGGS's population masses, and with the four centrals excluded.

## MUTATE

MUTATE=1 removes the deficit and keeps the scatter. On each footing, every galaxy's observed outer dispersions are multiplied by 10^(−D). D is the law's mean offset in the box cell where the law's σ is smallest, computed in the same run from the unmodified data. So H1 must fail and the script must exit 1.

If the main run's H1 also fails, both runs fail the same check. The control is then uninformative for H1, and the README will say so.

## Readings (declared)

- **H1 PASS:** the law's SLUGGS deficit survives the mass–anisotropy degeneracy across both declared ranges together.
- **H1 FAIL:** at the favourable corner of the two ranges the deficit falls below 2σ. The SLUGGS failure of the law is then not robust to the joint degeneracy. R3 says how much of the box still shows it.
- **The rule** is reported (R2). No verdict on the rule rests on this lane.
- **Caveats:** constant β only; one β for red and blue GCs; a coherent γ shift for all galaxies.

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model, or that the theory is closed.
