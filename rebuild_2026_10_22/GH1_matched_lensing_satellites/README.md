# GH1_matched_lensing_satellites

**Question.** KiDS lensing of isolated lenses wants route E's M200 +0.30–0.50 dex above EM1's SPARC relation. GAMA
satellites around G09 centrals want +0.78 (X75). In X78 no baryon budget fit both, in any gravity model. Is the gap the
**sample** (isolated vs centrals) or the **method** (lensing vs satellite dynamics)?
- **Test:** measure KiDS-1000 lensing around **exactly X75's 9,049 G09 centrals**, over the satellites' own aperture
  (50–300 kpc), and fit the same model.
- Criteria were frozen before any shear was read (45f918f379).

## Verdict: PROBES DISAGREE ON MATCHED HOSTS (lensing lighter), both footings

| | canonical | alt |
|---|---|---|
| **Δ_lens** (common log M200 shift, 50–300 kpc, 4 bins, jackknife + Hartlap) | **+0.17** [+0.05, +0.28] | +0.16 [+0.04, +0.26] |
| Δ_sat on the same hosts (X75, frozen) | +0.79 ± 0.03 | +0.78 ± 0.04 |
| χ² (20 pts): route E at best / at Δ = 0 / law (no parameter) | 24.8 / 26.5 / 28.3 | 24.8 / 26.3 / 28.7 |

**Reported:**
- Δ_lens per bin: +0.32 / −0.22 / +0.55 / +0.24.
- At 50–200 kpc: +0.21. Boost-corrected: +0.16.
- Cross-shear null: χ² 16.7 / 20 (p 0.67).

## What it means

- **The 0.3–0.6 dex gap is a method systematic of the satellite measurement, not a sample difference.**
  - On the same hosts and radii, lensing wants +0.17 ± 0.12 and satellites want +0.79 ± 0.03, more than 4σ apart.
  - Lensing on G09 centrals is consistent within ~1.5σ with KiDS isolated-lens lensing (X53 A1: +0.35 inner).
  - So lensing tells one story across both samples; the satellites are the outlier.
- **Likely causes, in X75's set-up (not tested here):**
  - Pair weighting is dominated by satellite-rich hosts, i.e. high-mass-scatter group centrals.
  - The Gaussian + flat-floor fit can absorb correlated (infalling / 2-halo) interlopers as dispersion.
  - Velocity bias and non-equilibrium.
  - X75's poor-group amendment already moved Δ by −0.15. A full correction would need e.g. a host-weighted, mock-
    calibrated interloper model.
- **Consequences for the lanes that leaned on satellites:**
  - **X75**'s "+0.78 dex" should not be used as the halo-mass need.
  - **X76**'s satellite need (×10^1.24) is overstated. Its lensing need (×10^0.85–0.90 on fair share) stands.
  - **X78_cgm_closure_regrade**'s failure was on the satellite line. With lensing alone, CGM-closure halos gave the
    best route E lensing yet (b3–4 χ² 141 vs SPARC 385), though still behind the law with F2 gas (95).
  - **X77_cgm_budget**'s lensing need (~2.8 R_vir, ≈ Zhang's closure radius) is now the relevant one.
- **What lensing says about route E on these hosts:** SPARC halos at Δ = 0 are already acceptable at 50–300 kpc
  (χ² 26.5 / 20), with a mild preference for +0.17. The law (no parameter) is about as acceptable (28.3).
  - At this S/N, 50–300 kpc lensing of G09 centrals does not separate the law from route E.
  - X53's isolated-lens preference for the law came from larger radii and the normalisation over all bins.
- κ = ½ FITTED; c_f EXTERNAL; footings never pooled; cold dark energy is a gravitating field component, never a particle;
  not theory closed; nothing here says the data favour the framework.

## Limits (disclosed)

- **Photo-z dilution.** Point Z_B > z_l + 0.2, with no n(z) and no m-correction (|m| ≈ 1–2 %), biases ΔΣ low by
  perhaps 5–10 %, i.e. ~0.05–0.1 dex in Δ. It cannot close a 0.6 dex gap.
- **Covariance.** With 30 jackknife patches for 20 points, the Hartlap factor is 0.276, so the errors are conservative
  (inflated about 1.9×).
- **S/N.** The signal is modest, roughly 4–6σ total at 50–300 kpc, and the per-bin shifts are noisy.
- **No two-halo term.** It is negligible inside 300 kpc for these masses; the 300–3000 kpc residual is not graded.

## Checks (3/3; MUTATE run separately)

- **K1:** the estimator reproduces CFG652's committed eFEDS-group stack exactly (max rel diff 0).
- **K2:** the host sample equals X75's (hosts [3651, 2411, 1690, 1297], pairs [318, 468, 574, 727]).
- **K3:** the model at Δ = 0 equals X75/X53's smooth halo.
- **MUTATE** (sources rotated 45°):
  - the rotated ΔΣ is consistent with zero (p 0.67);
  - the Δ fit hits the grid floor (−0.50).
- **Disclosed fix:** the first MUTATE run stopped at a missing LGRID name (X75 defines it in a later section). The same
  grid was added locally before any real shear was read.
- Peak RSS 0.72 GB; ~2.5 min per run.

## Files

- `FROZEN_CRITERIA.md`
- `gh1_matched.py`
- `gh1{,_MUTATE}.out` and `gh1_results{,_MUTATE}.json`
- per-host stacks: `_external_data/gh1_work/gh1_esd{,_MUTATE}.npz` (21 MB each, not committed; reproducible)

Run:

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 gh1_matched.py      # GH1_MUTATE=1 -> rotated control
