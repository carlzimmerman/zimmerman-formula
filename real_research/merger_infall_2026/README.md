# Cluster mergers as a test of the construction (L370–L373, L392)

In the construction, a cluster's baryons fall toward a neighbour with the MOND boost of their shared bound region. Its dark carrier falls with Newtonian gravity alone: whatever feels the boost must also source it (reciprocity, L353), and L361's region kernel reads only a region's own baryons. Mergers are where this split force law shows up in cluster *dynamics* rather than statics. These lanes compute what it does to real mergers, and what the carrier must look like to pass them.

## L370 — boosted infall in cluster mergers

`L370_boosted_infall_mergers.py`: 11/14 checks pass. The load-bearing failures A3, B3 and B6 are recorded. `MUTATE=1` switches the kernel off; A1 and A2 then fail (rc = 1).

**Machinery.**
- A periodic-FFT QUMOND solver with L361's region labelling: each bound region's phantom is sourced by its own baryons, and baryons feel it while the carrier does not.
- Its controls:
  - it reproduces Milgrom's exact deep-MOND two-body force (ratio 0.985);
  - an Ewald image correction is exact on Gaussian blobs (1.0000 at 4 and 8 Mpc);
  - an isolated cluster reproduces its 1-D lensing mass, and its phantom is Gauss-cancelled at the region's edge.
- The construction's clusters are real halos (carrier + gas + stars), solved so that real + phantom gives the observed lensing M200.
- ΛCDM uses the same components with all mass real. With the kernel off, the construction's intact variant is therefore identical to ΛCDM, which the MUTATE run confirms.

**(A) El Gordo, on Asencio, Banik & Kroupa's own yardstick** (Kim+2021 lensing: M200 = 2.13e15 M☉, ratio 1.52, z = 0.87).
- About 40% of El Gordo's lensing mass is phantom. Its real halos are 0.56–0.62 of the lensing mass.
- At the same lensing mass the pair pulls together at 60–90% of ΛCDM's rate. The carrier, which is most of the inertia, feels only the real mass's Newtonian pull, and so does everything else until the two bound regions merge (4–6 Mpc).
- To collide the way ΛCDM's pair does, the construction needs v~ = 2.09–2.29 against ΛCDM's 1.44 (at 2500 km/s). That is faster than any pair among the Jubilee simulation's 1000 most massive (the largest is ~1.69).
- Scoring: Asencio+2023's Fig. 1 (digitized) plus the z = 1 mass function of Asencio+2021.
  - With a linear tail: χ = 4.5–5.0 against ΛCDM's 5.10, so Δχ = −0.58 to −0.12.
  - With the tail continued as a Gaussian: Δχ = −0.46 to +0.01.
- **El Gordo comes out slightly easier than in ΛCDM.** The reason is that lensing overweighs the real clusters, not faster infall: the clusters actually fall together *slower*. The record's "El Gordo: natural (faster growth + boost)" is therefore right in sign for this construction but wrong in reason.
- The pre-declared neutral band (A3, |Δχ| < 0.5) is exceeded on the easing side; this is recorded. Beyond Jubilee's range the tail is an extrapolation.

**(B) Harvey et al. 2015 (72 collisions): where the lensing peak sits when a substructure's gas is knocked loose.**
- The measured quantity is β = δSI/δSG = −0.04 ± 0.07.
- Eight configurations: 1e14 or 3e14 substructures, 400 kpc from a 1e15 cluster at z = 0.4, gas displaced 60 or 120 kpc.
- Three estimators: iterated centroids in 100 kpc and 150 kpc apertures, and a projected-NFW fit (the analogue of Harvey's Lenstool fits).

Population-mean excess β, in σ from Harvey's mean:

| carrier in the substructure | 100 kpc | 150 kpc | NFW fit |
|---|---|---|---|
| intact | +0.7 | +1.1 | +0.9 |
| uniformly depleted to 0.55 | +0.8 | +1.3 | +1.3 |
| L357 cleared, x_v0 2000 (core decayed) | +2.5 | +4.0 | +1.7 |
| L357 cap, x_v0 1000 (core decayed) | +1.9 | +2.7 | +3.0 |

- **The core-decayed carriers are disfavoured at 1.7–4σ.** The MUTATE run shows this failure survives with the kernel off. It comes from the hollowed core, not from the boost. It is the Bullet-cluster logic: with no collisionless mass at the galaxies, the lensing peak follows the displaced gas.
- The boost's own pull on the peak is small: +0.03 to +0.06 in β for an intact carrier.
- **Design constraint: the carrier must keep collisionless mass in group and cluster cores.**

**Scope (2026-09-26).** L370's region mask is computed on the absolute density, (3/2)ρ/ρ_crit(z) ≥ x_c0 E(z)^(2p). Its docstring said the mean was subtracted; the correction is now in the docstring. L352, L377 and DE1 do subtract the mean: at z = 0.4 the two gates differ by 0.84 in x̃. Every L370 number, and every lane that reuses its solver, uses the absolute mask at L370's cell (p = 1, x_c0 = 1.5). This operator difference is open item 1 of the 2026-09-26 peer review.

## L371 — the Harvey test on L366's slow-kick carrier

`L371_harvey_slow_kick_carrier.py`: C1 reproduces L370's intact carrier to 1e-4. H1–H3 fail and are recorded; H4 is reported. `MUTATE=1` sets the retention to 1, so every shape becomes the intact carrier and passes (the inverted control, rc = 0).

**Input.** L366's carrier retention at 650 km/s (z = 0, within 1 Mpc/h): 0.18 for 1e14 M☉ substructures, 0.40 for 3e14 M☉, and 0.75 for the 1e15 M☉ main cluster. L366's 0.39 Mpc/h mesh does not resolve how that carrier sits inside a core, so three shapes bracket it:
- the original cusp, scaled down (optimistic);
- phase-mixed daughters kicked at 650 km/s (L321's machinery);
- recaptured, marginally bound daughters (pessimistic).

Population-mean excess β, in σ from Harvey's mean:

| shape of the retained carrier | 100 kpc | 150 kpc | NFW fit |
|---|---|---|---|
| cusp, L366 median retention | +1.0 | +1.8 | +2.1 |
| heated daughters, median | +1.1 | +2.0 | +2.5 |
| recaptured daughters, median | +1.9 | +3.5 | +5.4 |
| cusp, each bin's maximum retention (0.26 / 0.73 / 0.80) | +0.9 | +1.6 | +1.7 |

- **L366's slow-kick carrier fails Harvey at 2.1–5.4σ on the Lenstool-like fit.** Only the most favourable retention L366 allows passes.
- The reason is that its group cores keep too little collisionless mass: carrier-to-baryons inside 150 kpc is 1.4–3.7, against about 10 for an intact halo. Its trigger fires early, so galaxies lose their carrier before groups assemble from them.

**Scope (2026-09-26).** Harvey here runs at L370's cell (p = 1, x_c0 = 1.5; absolute-density mask; canonical footing). The retentions come from L366's mesh, which carries no phantom.

## L372 — a carrier that passes Harvey and X-COP together

`L372_gated_slow_kick_carrier.py`: 4/4 checks pass. `MUTATE=1` switches the uniform channel off; W1 then fails (X-COP overshoots) and rc = 1.

**Part 1: the pincer.** L357's vacuum-gated trigger with a finite kick (p = 2; cleared x_v0 2000 and cap x_v0 1000; v_k from 600 to 3000 km/s):

| kick | forest | S₈ | X-COP (canonical/alt) | galaxies | KiDS | Harvey (NFW fit) |
|---|---|---|---|---|---|---|
| 750 km/s | pass | 0.836 | 1.38/1.44 (fails) | pass | pass | +0.044 (pass) |
| 3000 km/s | pass | 0.772 | 1.08/1.13 (pass) | pass | pass | +0.129 (fails) |

- Slow kicks pass everything except X-COP: massive clusters recapture their daughters.
- Fast kicks pass X-COP but empty group cores.
- Escape depends monotonically on potential depth, so no single kick strips massive clusters to X-COP's ceiling while leaving group cores intact.

**Part 2: the two-channel carrier that passes.** The carrier has two decay modes:
- **U**, spatially uniform: L319's rate law Γ ∝ [Ω_Λ(a)/Ω_Λ,0]², with fast daughters at 3000 km/s. It depletes every host by nearly the same fraction and keeps its cusp. Its partial retention in the deepest cluster core is computed, not assumed (0.77 of the carrier stays inside R500 at f_U(0) = 0.25).
- **G**, L357's vacuum-gated density trigger with a slow kick (750–1050 km/s): galaxies lose their daughters, while groups and clusters recapture theirs.

At **f_U(0) = 0.25**, all three G kicks (750, 900, 1050 km/s) pass every gate on the record's alternative threshold set:

| gate | result |
|---|---|
| forest | T² ≥ 0.9976 |
| S₈ | 0.750–0.755 with every decayed particle at 3000 km/s (the conservative bound); 0.821–0.831 at v_G |
| X-COP | 1.19–1.21 / 1.24–1.26, passing after the 6% non-thermal correction |
| galaxies | +0.022 dex |
| KiDS | −24 / −17 |
| Harvey (100 kpc / 150 kpc / fit) | +0.019 / +0.050 / +0.048 up to +0.030 / +0.070 / +0.062; core carrier-to-baryons 5.7–7.9 |

Other rows of the grid:
- f_U(0) = 0.20 leaves X-COP too heavy on the alt footing (1.28–1.30).
- f_U(0) ≥ 0.30 drops the conservative S₈ below 0.748.

**Limits.**
- The strict threshold set fails on X-COP (1.24–1.26 on the alt footing) and on the conservative S₈ bound. The true S₈ lies between the two free-streaming bounds, 0.75 and 0.83.
- Retention is the static, full-depth, phase-mixed kind of L357/L321, not an assembly history. L366's PM machinery with both modes is the next check.
- The two modes are combined multiplicatively (a stated approximation).
- Harvey is scored on the canonical footing, with eight configurations standing in for the 72 substructures.
- High-z galaxies keep their carrier, as for every vacuum-gated carrier (L357's flagship shift).

**Scope (2026-09-26, cross-lane review XR1).** The combined verdict joins two kernel setups:
- KiDS is scored through L357 → L355, which has **no switch** (the kernel acts everywhere).
- Harvey runs at L370's p = 1, x_c0 = 1.5 cell, with the absolute-density mask and the canonical footing only.

This is a scope gap, not a known failure: L360 finds a switched p = 1, x_c0 = 1.5 construction with a carrier passes KiDS. A same-cell re-score is pending, for example at p = 1, x_c0 = 2.5 with the switched KiDS of L360/L390. Until then, quote L372 with this scope.

## L373 — the two-mode carrier in the particle-mesh box (scope: the p = 2, x_c0 = 2 cell)

`L373_two_mode_carrier_pm.py`: 5/6 checks pass, rc = 1 (3/4 before the edge-layer re-score added C3 and W2). The pre-declared hypothesis, that L372's window survives real assembly, is falsified. The MUTATE run (mode U off) was not made: by the lane's rule it runs only if R1 passes.

**Scope.** The box is L377's full construction at its switch cell, p = 2, x_c0 = 2:
- DE1 (c8bb50813) finds this cell fails the flat-a₀ flagship on the canonical footing.
- The particle-mesh track has moved to p = 1, x_c0 = 2.5 (L388). The verdict here holds for p = 2 only.

**Construction.** L372's two modes are put into L377's mesh, pooled over L369's three realisations:
- **U:** a uniform late decay at 3000 km/s.
- **G:** the vacuum-gated trigger at the mesh's x_c = 5, the record's mesh proxy. The mesh cannot resolve L372's x_v0 = 1000–2000.

**Pooled gates:**

| cell (f_U(0), v_G) | S₈ | forest | X-COP retention (floor 0.286) | shear |
|---|---|---|---|---|
| 0.20, 900 | 0.922 | 0.000 | 0.180 (under) | ok |
| **0.25, 750** | **0.939** | 0.000 | **0.337** | ok |
| 0.25, 900 | 0.917 | 0.000 | 0.175 (under) | ok |
| 0.25, 1050 | 0.892 (fails) | 0.000 | 0.087 (under) | ok |
| 0.30, 900 | 0.912 | 0.000 | 0.176 (under) | ok |

- **Decay in the mesh.** The mesh's G mode decays 65–70% of all the carrier by z = 0; mode U accounts for 12–18%. That is far more than L372's static G.
- **Clusters.** They keep too little carrier except at the slowest kick.
- **High redshift.** Clearing at z = 2 is 1.00 on both measures, as the vacuum gate is designed to leave high-z halos alone.

**Harvey on the one cell passing X-COP** (0.25, 750 km/s):
- Retention measured at z = 0.4 is 0.26 for 5e13–1e14 and 0.62 for 1.5e14–3e14 Msun/h.
- No halo reaches 3e14 at z = 0.4 in the three boxes, so the main cluster takes the 1.5e14–3e14 bin's 0.62.

| shape | excess β (100 kpc / 150 kpc / NFW fit) |
|---|---|
| intact carrier (matched control) | +0.006 / +0.040 / +0.027 |
| S1, the scaled cusp | +0.024 / +0.073 / +0.076 (passes) |
| S2, phase-mixed daughters | +0.040 / +0.092 / **+0.116 (fails; limit +0.10, i.e. 2.2σ from Harvey's −0.04 ± 0.07)** |

- The failure comes from the depleted group cores, as in L371: carrier-to-baryons inside 150 kpc is 2.7 (1e14) and 6.0 (3e14). It does not come from the kernel, since the intact control sits at +0.027.
- The miss is marginal: one shape, one estimator, 0.016 over the line.

**Controls.**
- **C1:** the LCDM run reproduces L366's σ₈ exactly.
- **C2:** the Harvey stage uses the mesh's own cell, p2_x2.0.

**Edge-layer check (added after the first result; reported, not gated).** XR5 found that the projected far edge layer of a switched region can move a substructure centroid. The Harvey maps were re-scored from the checkpoint with the line of sight also capped at ±3 and ±1.5 Mpc:
- **W2:** the betas move by at most 0.0006; the S2 fit is +0.116 on the full projection and +0.116 at both caps.
- **C3:** the full-projection betas reproduce the committed numbers exactly (0 difference over 9 numbers).
- The verdict is unchanged, so the S2 miss is not an edge-layer artefact.

**Correction.** The first run's Harvey stage had inherited L370's default cell (p = 1, x_c0 = 1.5), the same defect that withdrew L381. It was caught by a peer session and stopped before any Harvey number. The mesh runs were kept: 27,921 s, logged in `L373_two_mode_carrier_pm_mesh_stage.out`. Harvey was then re-scored from the checkpoint on the matched cell.

**Operators.** The mesh (L377: the Newtonian field of all baryons, response masked, background-subtracted gate) and the Harvey stage (L370/L361: each region's own baryons, absolute-density mask) use different phantom operators. Both are recorded in `results.json`. The cross-thread review XR5 finds Harvey operator-independent to |Δβ| ≤ 5e-5, with ≤ 1.8e-3 under a ±0.01 a₀ external field. It also flags a line-of-sight edge-layer effect of up to Δβ ≈ 0.009 on 2-D meshes. That is below this cell's 0.016 S2 margin, but the 3-D check (projection depth capped) has not yet been run.

**Limits.**
- The p = 2 cell only.
- The G trigger is the mesh proxy.
- Three 100 Mpc/h boxes, with no halo ≥ 3e14 at z = 0.4.
- Harvey is scored on the canonical footing, with eight configurations standing in for Harvey's 72 collisions.

## L392 — L372's two-mode carrier re-scored same-cell at the linear gate, each switch branch on its own

`L392_l372_linear_gate_branches.py`: 7/9 checks pass, rc = 1. The pre-declared hypothesis holds on the curvature branch and fails on the matter branch. `MUTATE=1` (an intact carrier) fails every cell, flipping the curvature pass.

**Why.** L372's committed window joined two kernel setups (see its scope note, 8850550c4):
- KiDS was scored switch-free, through L355.
- Harvey was scored at L370's p = 1, x_c0 = 1.5 cell, on the canonical footing only.

The construction now sits at the linear gate p = 1, x_c0 = 2.5. The switch variable has two readings, which are never pooled:
- **Matter:** the matter density (baryons + carrier), background-subtracted.
- **Curvature:** matter + the untruncated (switch-everywhere) phantom, background-subtracted. This is how L352 and DE1 set the edge. L395's "onbranch" cell iterates the masked phantom instead, which is not identical.

**Method.** Only the switch-dependent gates are re-scored. Forest, S₈, X-COP and galaxies are switch-free in L372 and are read from its committed results.
- **KiDS:** L372's own carrier templates go on L360's switched fit at x_c,eff(0.25) = 3.25. Each branch sets the edge from the lens's own matter: L375's baryons (Hernquist + NFW-shaped CGM) plus the retained carrier.
- **Harvey:** L372's harvey(), with the branch's mask in both the 1-D lensing-mass root and the 3-D phantom map, using L370's region operator.

**Controls, all exact:**
- **C1:** L372's templates rebuilt here reproduce its switch-free KiDS to 6e-14; the data radii and hosts agree.
- **C2:** L360's switched fit is reproduced exactly.
- **C3:** L372's committed Harvey numbers are reproduced exactly at its own cell.
- **C4:** x_c,eff(0.4) = 3.868 = 2.5 E(0.4)².

| branch | lens matter beyond r200 | KiDS Δχ² (canonical / alt, all three kicks) | Harvey NFW-fit β (canonical; 750 / 900 / 1050) | verdict |
|---|---|---|---|---|
| matter | cut at r200 | +322 / +332 (edges 0.15–0.34 Mpc) | +0.047 / +0.056 / +0.062 | fails KiDS |
| matter | continued as NFW | +118 / +128 (edges 0.35–0.88 Mpc) | same | fails KiDS |
| curvature | cut at r200 | −41 / −34 | +0.046 / +0.055 / +0.062 | **passes every gate** |
| curvature | continued as NFW | −60 / −55 (edges 0.81–1.36 Mpc) | same | **passes every gate** |
| L360's own edge rule | — | −41 / −34 | — | (reference) |

On the alternative footing at 900 km/s, Harvey gives +0.063 (matter) and +0.062 (curvature); both pass.

**Reading.**
- **On the curvature switch, L372's window survives same-cell at the linear gate.** All three kicks pass KiDS comfortably, pass Harvey (canonical, and the alternative footing at the central kick), and keep their committed switch-free gates.
- **On the matter-only switch, it fails KiDS.** With the carrier cleared from galaxies, the switched region around an isolated lens ends at 0.35–0.9 Mpc, depending on how the lens's matter continues beyond r200. KiDS needs the MOND-like signal further out.
- Harvey passes on both branches; the branch barely moves β.

**The convention split.** The two outer-matter conventions were split after the first main run. With the templates cut at r200, the matter-branch edge sat exactly at r200, a truncation artefact. Both conventions are reported, never pooled.

**Limits.**
- σ = 0 only (L370's operator). V0 finds σ physical, but the cross-thread review XR5 (H1) finds the action's σ = 1 operator and L370's give the same Harvey centroid to |Δβ| ≤ 0.002 (toward-main geometry, far edge layer excluded). That is far inside these margins (0.04–0.05 below the line). XR5's 4.1 kpc far-edge-layer shift is a staircase-mesh numerical effect, not a σ effect, and L373's 3-D check bounds that layer at |Δβ| ≤ 0.0006. The first version of this note misread it as Δβ ≈ 0.03–0.07. XR5 does not cover the perpendicular orientation.
- The switch-free gates are L372's static ones, not re-derived.
- No 2-halo matter enters the matter branch's switch variable; Brouwer's lenses are isolated.
- The ESD keeps L352's point-mass baryons; only the switch reads the resolved baryons.

