# VB1_vacuum_boundary: FROZEN CRITERIA (2026-10-31, before any run)

**Question.** Argon's door D2 (`../ARGON_REPLY_2026-10-31_EVENING_SCORED.md`): the zooms are isolated Lagrangian spheres of radius RS = 1.5 q_M in a vacuum (`x48_fast.py --rs`, default 1.5; ZN1 limit 5). Mass that would arrive at 1.4–2.1 R₂₀₀ by z = 0 from Lagrangian radii beyond 1.5 q_M is absent. Is the × 1.4 shortfall of the native profile in the OUTER shear band (G-OUT-M3, 2.18–3.17 R500) a boundary artefact?

**Owner rule.** Native inputs only; nothing fitted; one gate; lines fixed here; MUTATE twin; κ = ½ FITTED; cold dark energy is a gravitating field component, never a particle; not theory closed; nothing here says the data favour the framework.

## Design
- Two runs, same seed, same mesh, same particle mass, same softening, same background: **A** RS 1.5 (control), **B** RS 2.0. RS 2.0 is the largest radius the IC grid allows (periodic side 4 q_M, so the sphere must stay inside half the side). Argon asked for 2.25; 2.0 is the ceiling without changing the grid, and that change would alter the constrained field. Disclosed.
- Mass 1e14 M☉, seed 1, **ng 48** (so B's particle count, about 2.4 × A's, matches an ng 64 run's cost). Collapse to z_f with `x48_fast.py`, continued to z = 0 with `zn1_continue.py` unchanged.
- Measured on both at z = 0, same code path as ZN1/ZN3 (`zn1_measure.py` or its ZN3 copy, read-only): M(< r) in physical kpc, R₂₀₀, M₂₀₀, the projected ΔΣ in the OUTER band 2.18–3.17 R500 and M(< 0.7 R500), each on the lensing sample's R500 convention as ZN3 used it.
- **Statistic:** f_out = ΔΣ_B/ΔΣ_A in 2.18–3.17 R500; f_in = M_B(< 0.7 R500)/M_A(< 0.7 R500). Both runs' R500 taken from run A, so the aperture is the same physical radius.

## Gate: G3g, G-OUT-M3 (one template, X-COP's and the measured gas scales both reported, class on the measured scale)
- **PASS (BOUNDARY MATTERS):** f_out ≥ 1.28 and |f_in − 1| ≤ 0.04.
- **FAIL (NOT A BOUNDARY ARTEFACT):** f_out < 1.15.
- **MIXED:** 1.15 ≤ f_out < 1.28, or f_out ≥ 1.28 with |f_in − 1| > 0.04 (the inner profile moved too, so the key's gain is not from the boundary alone). Reported as MIXED, no pass.
- Post-result, reported not graded: ZN3's 15 keys with run B's shape at 1e14 in place of run A's, on both gas scales.

## Predictions on record
- Argon: f_out 1.18–1.24, G-OUT-M3 from about +3.8 to about +2.4. Asked, not yet given: f_in.
- This session: f_out below Argon's, 1.05–1.15 (ZN1's tail-closure shell at rest moved the keys by |ΔZ| ≤ 0.01; a stream of infalling shells does more than a shell at rest, but the band at 1.4–2.1 R₂₀₀ at z = 0 is fed mostly by shells inside 1.5 q_M on this background); f_in within 2 %.

## Checks before any grade
- K1: run A at RS 1.5 ng 48 reproduces X48's ng 48 seed-1 1e14 η and c at z_f to 1e-6 when given the same seed and flags (same code; if X48's ng 48 run is not on disk, K1 is replaced by an engine identity check against ZN1's K1).
- K2: particle mass equal in A and B to 1e-12 (meta `mpart`).
- K3: softening equal (zn1_continue asserts it).
- K4: run B's sphere holds (2.0/1.5)³ = 2.370 × run A's particles, ± 3 % (grid discreteness).
- MUTATE: run B measured with run A's R500 shifted by × 1.5: f_out must change by more than 10 % (the statistic sees the aperture), else the lane stops.

## Cost and scheduling
About the cost of one ng 64 zoom to z = 0 for B plus a cheap A. **Does not start while ZN4 or the 1e12 ng 80 seeds are live** (`run_vb1.sh` waits for their done files and for free load). Preemptible: checkpoints on SIGTERM, `--resume`.

## What a pass breaks
More mass inside r_ta from the extended sphere, if the budget is not renormalised, pushes G-MID-T3 toward OVER (Argon: about −0.35 in Z) and changes M_fair at r_ta against the zoom's holding (ZN1: 3.4 against 2.2 M₂₀₀). A pass here is a statement about the zoom's boundary, not a cluster pass: ZN3's keys would need regrading on the measured gas scale, where G-OUT-M3 is +4.35.

## Not done here
No new data. No change to the force kernel, the softening, the background or the constrained field beyond RS. No tail slope, no r₀ multiplier (closed, GX1/NZ1). A4's and ZN3's shapes are not re-derived.
