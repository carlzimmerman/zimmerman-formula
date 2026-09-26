# Cluster mergers as a test of the construction (L370–L372)

In the construction, a cluster's baryons fall toward a neighbour with the MOND boost of their shared bound region. Its dark carrier falls with Newtonian gravity alone: whatever feels the boost must also source it (reciprocity, L353), and L361's region kernel reads only a region's own baryons. Mergers are where this split force law shows up in cluster *dynamics* rather than statics. These lanes compute what it does to real mergers, and what the carrier must look like to pass them.

## L370 — boosted infall in cluster mergers

`L370_boosted_infall_mergers.py`: 10/14 checks pass. The load-bearing failures A3, B3 and B6 are recorded. `MUTATE=1` switches the kernel off; A1 and A2 then fail (rc = 1).

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
