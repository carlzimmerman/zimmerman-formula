# XR5 — which force operator? The action's region kernel (L361) vs the PM operator (L377) vs the merger operator (L370)

**Question.** The 2026-09-26 peer review (`peer_review_2026_09_26/dark_sector/REPORT.md`, "Additional bridge";
`NEXT_CALCULATIONS.md` item 1) found that the PM retention runs and the Harvey+2015 merger runs use different phantom
operators, with no error bound tying either to the action. XR5 measures the difference on one controlled test bed.

**Answer in one paragraph.** Inside a cluster region the three operators are the same to a controlled, converged error.
The PM operator (B) matches the action's operator (A) to ≤ 2.2e-3 in the phantom monopole at 0.1–1 Mpc. That covers
merged neighbours, a separated neighbour and merger pairs. A realistic external baryonic field adds ≤ 3.0e-4 (it enters
at second order). For Harvey offsets all operators agree to |Δβ| ≤ 5e-5, and a realistic external field moves β by
≤ 5.5e-4. Where B is **not** A:
- the region outskirts, where B's external-field effect reaches ~1% of the enclosed phantom at 0.003 a0 and 11% at 0.01 a0;
- anything first order in the external field: a net push of the region's baryons of 3.5–4.6 g_e, and a phantom of
  1.3–2.3 g_e felt by baryons outside the region.

Three things matter more than the operator:
- region labelling;
- the edge definition (L370's absolute-density formula vs the contrast);
- a numerical effect. The region's far edge layer, projected along the line of sight, moves a substructure's lensing
  centroid by up to 0.5 kpc (B, C) and 4.1 kpc (A) on staircase meshes. For B and C that is Δβ ≈ 0.009, the size of
  L381's S2 margin.

## The operators, read from the code

| | source of the kernel's field | gate / region | response | felt by |
|---|---|---|---|---|
| **A** L361:16-32 (EL eqs. checked in R0, :86-122) | the region's own baryons, `(lap − M²) w = 4πG f ρ_b`, M² = m²(1−f): screened across the inactive web (Dirichlet as m→∞) | L359's contrast 1.5(ρ − ρ̄_m)/ρ_c (L359:107) | `(lap − M²) P = div[f(ν−1)∇w] + M²w` | in-region baryons (φ + fP) |
| **B** L377:117-127 | ALL baryons on the mesh, `poisson(1.5*Om*(rb - WB)/a)` (:123) | contrast, `1.5*Om_a*(rho-1)*gate > X_C0` (:119-120; p = 2, x_c0 = 2 at :94) | masked `f(ν−1)g` (:124-125), curl-free projection (:126-127), L362's central-difference grad/div (L362:104-108) | ALL baryons (:163-164); carrier Newtonian (:165); trigger reads δ_ph (:176-178) |
| **C** L370:286-307 | each labelled region's own baryons, `grid.field(rb * f)` (:296) | ABSOLUTE density `1.5*rreal/(RHOC0*Ez2) >= x_ceff` (:290; docstring :19 says contrast); only regions containing a given centre (:292) | masked response (:297-299), spectral projection (:301) | in that region only (:302-303); lensing `-div(gph)/4πG` (:304-305) |

Loaded by L371:79-80, L372:252-253, L373:221-249 and AT3:322. The kernel is nu_mono in all three: L340:104-117;
L377:97-114 rebuilds it on a wider table, max deviation 3.6e-12; L370:136-155 is identical.

**Identity checks.** No module was imported and no simulation was run. L377's `phantom()` and L362's `Sim` were compiled
from their source via the AST. L370's head (its definitions, up to the C1 banner) was exec'd exactly as L373 does. On 32³ boxes my (B) and (C) reproduce the originals with 0.0
deviation (I1, I2). With one whole-box region, B and C are the same operator (I3, deviation 0). The two codes'
**discretisations** still differ: L377's central differences against spectral derivatives change the same phantom
potential by 4.2% at 0.75 Mpc/h cells and 1.5% at 0.375 Mpc/h (L377's mesh is 0.39 Mpc/h). Kernel: mine equals L340's
exactly (K1). "nu_mono = nu_RAR below y_p = 2.5396" holds to 3e-9 only below y = 2.337, where the monotone floor takes
over; up to y_p it holds to 1.8e-4 (K2).

## Method

Every configuration is axisymmetric, so the continuum operators are solved on a 2-D (R, z) finite-volume mesh:
- 25 kpc cells within 1.2 Mpc, 100 kpc out to R = 7 and z = −7.5..19.5 Mpc (10 kpc for Harvey);
- geometric growth to a free-space boundary at ~410 Mpc;
- sparse LU;
- each operator is two linear solves plus a pointwise map. The QUMOND form needs no iteration.

Validation against exact solutions:

| check | result |
|---|---|
| S1 spherical QUMOND (ν−1)g_N, all five operators | ≤ 1.4e-3 at 0.25–2 Mpc; 1.2e-2 at 0.1 Mpc (4 cells) |
| S2 Kelvin image for A's Dirichlet w (image = 9–38% of the field) | ≤ 1.0e-2 |
| S3 projection of a uniform field in a ball = F/3 | 0.3304–0.3310 |
| S4 L361 screening transmission, 2 Mpc gap (L361's function and committed JSON) | 1/m = 0.2: 9.53e-5 vs 9.50e-5; 0.3: 3.169e-3 vs 3.167e-3; 0.5: 5.072e-2 vs 5.072e-2 |
| S5 no-gate control (asserted): A (both code paths), B, C coincide | 3.1e-13 |
| R1 convergence, 3 meshes (50/35/25 kpc): change in B−A monopole / push | 3.6e-5 / 4.1e-4 |

**Test bed.** A cluster built with L370's RealHalo recipe: real M200 = 1.2e15 Msun, c = 4, M_b(<1 Mpc) = 6.9e13 Msun,
BCG scale 50 kpc. Perturbations:
- a similar cluster at d = 3, 5 Mpc (one connected region under every gate cell) and at 13 Mpc (separate, except
  z = 0, p = 2);
- a uniform external field g_e/a0 = 0.001, 0.003, 0.01, 0.03, read by B only;
- a merger pair of two M200 = 6e14 halves at 0.5 and 1.0 Mpc;
- L370's Harvey configuration in the toward-main orientation at z = 0.4.

This covers gate cells (1, 2.5) and (2, 2) at z = 0 and 0.4, both a0 footings, and A at m→∞, 1/m = 0.2 and 0.5 Mpc.

**Realistic external field.** The linear-theory baryons-only rms at the lenses is 0.0021 a0 canonical and 0.0017 a0 alt
(L355, via L361's committed R3 JSON). A 1e14 Msun baryonic neighbour at 5 Mpc gives 0.006 a0. The realistic range is
therefore 0.001–0.006 a0; monopole effects scale as g_e², so 3.0e-4 at 0.003 becomes ~1.2e-3 at 0.006.

## Results (max |fractional difference| vs A's Dirichlet limit, all gates and both footings)

| config | op | monopole 0.1–1 Mpc | well depth | M_ph(<0.9 R_e) | worst direction | push | lensing M_2D |
|---|---|---|---|---|---|---|---|
| isolated (= floor) | B, C | 3.0e-8 | 9.4e-6 | 6.5e-4 | 1.7e-4 | 9e-6 | 3.0e-3 |
| neighbour 3 Mpc (merged) | B | 1.5e-3 | 1.2e-3 | 6.9e-4 | 1.6e-2 | 1.4e-2 | 3.2e-3 |
| neighbour 5 Mpc (merged) | B | 2.2e-3 | 3.8e-3 | 6.0e-3 | 2.8e-2 | 3.1e-2 | 2.9e-3 |
| neighbour 13 Mpc (separate; merged at z = 0, p = 2) | B | 2.6e-4 | 2.1e-3 | 1.3e-2 | 4.3e-2 | 3.8e-2 | 3.9e-3 |
| neighbour 13 Mpc | A, 1/m = 0.5 | 2.5e-7 | 7.9e-6 | 5.6e-4 | 5.9e-4 | 2.7e-4 | 1.9e-3 |
| pair 0.5 / 1.0 Mpc | B | 1.7e-5 / 1.7e-4 | 1.2e-5 / 1.0e-4 | 5.3e-4 / 2.2e-4 | 1.0e-3 / 3.8e-3 | 2.9e-4 / 1.9e-3 | 4.4e-3 / 2.7e-3 |
| g_e = 0.001 / 0.003 / 0.01 | B(g_e) − B(0) | 3.3e-5 / 3.0e-4 / 3.3e-3 | 2.2e-4 / 2.0e-3 / 2.1e-2 | 1.1e-3 / 1.0e-2 / 1.1e-1 | 1.3e-2 / 3.8e-2 / 1.3e-1 | 3.5–4.6 g_e | 1.3e-4 / 1.1e-3 / 1.0e-2 |

- C matches B (to ~10%) wherever the relevant baryons share one region: merged neighbours and pairs. For a separated
  neighbour C, like A, does not see it; C's 13 Mpc maxima come from the one cell where the regions merge. A at finite m
  stays within 3e-4 (monopole) of its Dirichlet limit.
- In 72/72 perturbed cases B's phantom at 1 Mpc is weaker than A's. The causes are the EFE, reading separated
  structure, and merged neighbours seen without Dirichlet images.
- The lensing column is floor-limited: the staircase edge layer lies in the line of sight.
- **Gauss.** The net phantom mass over the domain is ≤ 1.4e-13 of M_b for every operator. The phantom enclosed at
  0.9 R_e is 5.7–7.2 × M_b(<0.9 R_e), compensated at the edge.
- **Well depth.** From the centre to 0.9 R_e the carrier's Newtonian depth is 8.1–8.6e6 (km/s)² (v_esc ≈ 4030–4150
  km/s) and identical under all operators. The baryons add a phantom depth of 2.6–3.1e6 (km/s)², on which the operators
  agree to ≤ 1e-5 (isolated), 3.8e-3 (merged) and 2e-3 (g_e = 0.003).
- **B's first-order extras.** The net push is 3.5–4.6 g_e on the baryons within 0.5 Mpc. It displaces them from the
  carrier by only ~0.2 kpc at 0.003 a0 (L370's dx_eq estimator, ρ50 = 1.4e16 Msun/Mpc³). Out-of-region baryons at
  1.25 R_e feel a phantom of 1.3–2.3 g_e. A and C give zero for both.

**Edge definition.** On the same density field, L370's absolute-density formula puts the edge +4.8 to +6.1% further
out than the contrast gate: 5.49 → 5.75 Mpc at z = 0 (p1), 4.26 → 4.46 Mpc at z = 0.4 (p2).
- The shell theorem leaves the interior force unchanged (≤ 5e-6).
- The projected lensing mass changes by up to 1.2e-3 / 2.0e-3 / 3.8e-3 / 5.8e-3 at R = 0.1 / 0.25 / 0.5 / 1 Mpc.
  That is larger than a realistic g_e (1.1e-3). A deep-MOND estimate gives a similar size: ~2.5e-3 at 1 Mpc from
  d ln M_2D,ph/d ln R_e ≈ 0.15 at R/R_e ≈ 0.2, with a phantom fraction of 0.28. The agreement is only within the 3e-3
  lensing floor.
- It can also flip the labelling: at z = 0 (p1) the 13 Mpc neighbour is two regions under the contrast gate and one
  under the absolute gate.
- On L370's painted halos (no cosmic mean) the two gates coincide if the painted profile is read as an overdensity.

**Labelling.** Relabel the same merger pair as two touching regions (split at the midplane) and the phantom pull on
cluster 2 reverses sign: −1.32e5 → +3.5e4 (km/s)²/Mpc, because the split plane's negative edge layer repels. The
operators themselves differ on that pull by ≤ 6.8e-3.

**Harvey (toward main, z = 0.4, both gates, 1e14 and 3e14 substructures, δ_SG = 60 and 120 kpc, both footings).**
Keeping matter within 1.5 Mpc of the substructure excludes the far edge layer. The result is stable at r_s = 1.0 / 1.5 /
2.0 Mpc (2.349 / 2.344 / 2.343 kpc) and at 20 / 15 / 10 kpc cells (2.418 / 2.345 / 2.344).
- Max |Δβ| vs A_D: A(0.2) 1.6e-5, A(0.5) 2.2e-5, C 4.6e-5, C_abs 5.0e-5, B 4.7e-5.
- With an external field in B: ±0.003 a0 gives 5.5e-4 and ±0.01 a0 gives 1.8e-3. The sign follows the field's direction,
  so it averages to zero over orientations.
- **Noise.** With the far layer included, the same 100 kpc centroid wanders by up to 4.13 kpc (A) and 0.52 kpc (B, C)
  between meshes and gates (e.g. A: 0.06–6.47 kpc; C: 2.11–2.86 kpc; true value 2.344). That is a staircase artefact of
  the projected edge layer. The continuum contribution of a smooth shell ~3 Mpc away is < 0.01 kpc.

## Verdict

**(a) Cluster retention in the PM boxes.**
- B is a controlled approximation to A inside ~1 Mpc. The phantom monopole error is ≤ 2e-3 at realistic external fields
  and ≤ 3e-3 up to 0.01 a0.
- For scale, L377's own discretisation (FD vs spectral at its cell size) is 1.5%.
- It is not controlled beyond that. In the outskirts, and in everything first order in the external field (the push,
  the out-of-region phantom), B is a different operator.
- Direction: switching B → A strengthens the phantom slightly (≤ 0.2% at 1 Mpc, ~1% at 0.9 R_e for g_e = 0.003). The
  trigger reads δ_ph, so retention would move marginally lower, far inside the X-COP margin (0.32 vs 0.286). No PM
  run was made; this is a static-field inference.

**(b) Harvey lensing offsets.** B, and equally C, is a controlled approximation to A: |Δβ| ≤ 5e-5, ≤ 5.5e-4 with a
realistic external field and ≤ 2e-3 at 0.01 a0. That is far below σ_β = 0.07 and L381's S2 margin of 0.0086. Switching
operators does not move the Harvey statistic.

**What to fix instead.**
1. Make the edge definition explicit: contrast (as L359/L377) or absolute (L370:290).
2. Watch region-merging thresholds (labelling is discontinuous).
3. In Harvey maps, exclude the region's far edge layer or demonstrate its convergence. On my meshes it moved β for the
   operator the L370-family runs use by up to 0.009.

This is a risk measured on 2-D staircase meshes, not a measurement of L370's 3-D spectral maps; the check there is
cheap.

## Scope and caveats

- Static fields on prescribed densities. No evolution, trigger dynamics or PM run.
- Axisymmetric configurations only; Harvey's "perp" orientation was not computed.
- The external field is uniform; tidal parts enter through the neighbour configurations.
- nu_mono only.
- Lensing = Laplacian of the phantom potential (as L370); the relativistic embedding is not derived.
- The test cluster is one model; region edges at 4.3–6.1 Mpc follow from its profile and the gate.
- Exploratory runs preceded the final script and informed the check tolerances. The checks are consistency asserts,
  not blind predictions.

## Reproduce

From the repository root (single-threaded, ~55 s):

```
python3 real_research/cross_thread_review_2026_09_26/XR5_operator_identity.py > real_research/cross_thread_review_2026_09_26/XR5_operator_identity.out
MUTATE=1 python3 real_research/cross_thread_review_2026_09_26/XR5_operator_identity.py > real_research/cross_thread_review_2026_09_26/XR5_operator_identity_MUTATE.out
```

- Main: 13/13 checks pass, rc = 0.
- MUTATE drops the screening (M² = 0). S4 fails (transmission 1.0 vs 9.5e-5) and X-SCREEN fails (A's response to the
  separated neighbour is 3.2e-2 vs B's 3.8e-2), so rc = 1.
- The script writes nothing but stdout. It reads L340, L361, L362, L370 and L377 sources and L361's results JSON,
  read-only.

Files: `XR5_operator_identity.py`, `XR5_operator_identity.out`, `XR5_operator_identity_MUTATE.out`, `XR5_README.md`.
