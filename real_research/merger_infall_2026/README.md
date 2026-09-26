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
