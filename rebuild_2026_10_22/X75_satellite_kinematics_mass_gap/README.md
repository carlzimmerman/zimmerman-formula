# X75_satellite_kinematics_mass_gap

**Question.** KiDS lensing (X53, X74_smooth_core_lensing) wants route E's halos 0.30–0.50 dex heavier in M200 than EM1's SPARC relation
gives. Is the halo mass short, or is it a lens stellar-mass or lensing systematic?

**Method.** An independent probe on different data and a different observable: satellite line-of-sight dispersions
around GAMA G09 centrals.
- G3C spectroscopic z and GKV stellar masses, both already on disk.
- 9,049 hosts and 2,087 satellite pairs at 50–300 kpc.
- Graded against the same X53 machinery (smooth core, X73 and X74_smooth_core_lensing) and the isolated law.
- Criteria were frozen before any velocity was read (e7dfee54b9).

## Verdict (frozen rule): KINEMATICS REQUIRE A DIFFERENT MASS, both footings

The data need route E halos **+0.78 dex** heavier than SPARC's M200: more than lensing asked for, and far from zero.

| B21 bin (log M★) | 8.5–10.3 | 10.3–10.6 | 10.6–10.8 | 10.8–11.0 |
|---|---|---|---|---|
| measured σ_sat (pair-weighted), km/s | 72 ± 12 | 114 ± 9 | 151 ± 9 | 188 ± 9 |
| route E at SPARC M200 (canonical) | 41 | 59 | 73 | 85 |
| route E at best common shift | 92 | 126 | 150 | 174 |
| law (isolated, canonical) | 87 | 107 | 120 | 141 |
| per-bin shift needed, dex | +0.55 | +0.68 | +0.80 | +0.88 |

| | canonical | alt |
|---|---|---|
| common Δlog M200 | **+0.79** [+0.75, +0.82] | **+0.78** [+0.74, +0.81] |
| χ², route E at Δ = 0 (4 bins) | 237 | 236 |
| χ², route E at best Δ | 6.7 | 6.7 |
| χ², law (no free parameter) | 39.1 | 29.0 |

**Frozen systematics, reported:** β ±0.3, γ ±0.5, aperture 50–200 kpc, host weighting, the Burkert shape and EM1
background B all give Δ = +0.69 to +0.81. Every one lands in the same class.

## Is it environment? (AMENDMENT A1, post-result, reported only)

The frozen sample is centrals. B21's isolation leaves about 9 pairs in G09, so it is unusable here.
- Restricting to ungrouped or N_fof ≤ 3 hosts, which is biased low because it selects on the tracer, gives:
  - Δ = **+0.63** canonical and +0.62 alt;
  - σ 71 / 99 / 138 / 154 km/s;
  - law χ² 12.8 / 10.4.
- **A2, untruncated halos** (the R200 edge removed): +0.74 frozen sample, +0.58 poor groups.
- The softest combination of every reported knob (poor groups, untruncated, 50–200 kpc) stays near +0.5.

**Environment explains part of the gap (~0.15 dex); the edge explains ~0.05. Neither closes it.**

## Reading

- **Two independent probes now agree on the sign.** Lensing (KiDS, photometric, isolated) and satellite kinematics
  (GAMA, spectroscopic, centrals) both find route E's SPARC-derived halos too light at 50–300 kpc.
  - Lensing: 0.30–0.50 dex short.
  - Kinematics: 0.5–0.8 dex short.
  - The required shift rises with stellar mass (+0.55 → +0.88 per bin). EM1's M200–M_b relation is too shallow as
    well as too low.
- **So the lensing gap is not a lens-M★ artefact.**
  - The kinematics use different stellar masses (GKV ProSpect, not KiDS LePhare) and no lensing.
  - X53 had already noted that ±0.2 dex in M★ moves M200 by ±0.18 dex, which is too little.
- **Route E's galaxy halo masses are the problem.** SPARC rotation curves stop at ~20–50 kpc, and EM1's relation
  extrapolates them to R200. Both outer probes say that extrapolation is far too light.
  - A route E halo-mass rule that does not come from SPARC is needed. A natural candidate is the clusters' own native
    fair-share budget to r_ta. It is untested here.
- **The isolated law does better than SPARC-normalised route E** (χ² 29–39 vs 236, and 10–13 vs 128 in poor groups),
  with no free parameter. It still under-predicts the two highest-mass bins by 20–25 % in the frozen sample.
  - Group potentials and the EFE are not modelled for it.
  - This is not a pass for the law.
  - Nothing here says the data favour the framework.
- κ = ½ FITTED; c_f EXTERNAL; footings never pooled; cold dark energy is a gravitating field component, never a particle;
  not theory closed.

## Checks

- **K1:** a synthetic σ 150 km/s plus floor is recovered at 149.7.
- **K2:** the Jeans projection gives the singular isothermal sphere σ_los within 0.6 %.
- **K3:** mass_H at Δ = 0 equals X53/X74's smooth halo exactly.
- **MUTATE:** shuffled Δv collapses the Gaussian in every bin.
  - **Disclosed fix, made before any real velocity was read:** the first MUTATE run showed that a collapsed fit can
    land in any of three equivalent states (amplitude → 0, σ → fit floor, or σ wider than the ±2000 km/s window, i.e.
    indistinguishable from the flat floor). The frozen check had joined these with "all bins" across the whole set.
    It was corrected to accept any of the three per bin.
- **Velocity errors** are a flat 50 km/s per galaxy, as frozen.
- **Hosts** need GKV masses, so they are in G09 only. G12/G15 masses are not on disk, and fetching them needs approval.
- One thread, peak RSS 0.40 GB, ~3 min per run.

## Files

- `FROZEN_CRITERIA.md`, `AMENDMENT_A1.md` (A1 and A2)
- `x75_satkin.py`
- `x75_satkin{,_A1_nfof3,_MUTATE}.out` and `x75_satkin_results*.json`

Run:

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x75_satkin.py            # X75_MAXNFOF=3 -> A1; X75_MUTATE=1 -> control
