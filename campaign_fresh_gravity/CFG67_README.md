# CFG67 — the ΛCDM control for CFG61: is the KiDS colour-split failure specific to B?

- **Criteria:** frozen before any script or ΛCDM prediction existed, in `CFG67_FROZEN_CRITERIA.md` (5f9c56bc8).
- **Script:** `CFG67_lcdm_control_kids_split.py` (about 5 s). It executes CFG61's data, lenses, forward model, projector and K1 bins read-only. Its MUTATE control, which swaps early and late, exits 1 as required.

## Bottom line

**CFG61's failure is specific to B's colour-blind, mass-independent dark mass, not an artefact of the machinery.**
- **Standard halos reproduce the split.** Through exactly the same pipeline, lenses and 1-halo bins, ΛCDM with Mandelbaum+2016's colour-split halo masses fits the early-minus-late difference at χ² 6.5/7 (p = 0.48), with amplitude Â = 0.79 ± 0.48 (1 predicted). **H1 passed.** B's law is at 28.1/7 on the same bins (CFG61's reported χ² row).
- **Even colour-blind ΛCDM reproduces it.** Moster+13 halo masses, which depend on M_* only, give χ² 6.9/7 and Â = 1.36 ± 0.28 (statistical).
- **The mechanism.** At fixed g_bar, ΛCDM's lensing signal grows with lens mass (halo mass rises steeply with M_*), and the early class is more massive. B's law in the deep regime gives the same ΔΣ at fixed g_bar for any mass (CFG61's C4, to 4 × 10⁻⁶), so it cannot make a class difference. That leaves only extra baryons in the early types (CFG61 R4).

## The rest (as run)

- **H2 failed.** "The data prefer ΛCDM's split over a colour-blind prediction at more than 3σ" gave Â/σ_A = 1.64. The ±0.1 dex early-class stellar-mass floor dominates (0.452 against 0.164 statistical), because ΛCDM's predicted split is very sensitive to M_* through the steep stellar-to-halo relation. Without the floor it is 4.8σ.
- **H3 (absolute profiles on K1):** ΛCDM gives early 29.6/7 and late 27.9/7; B's law gives 51.9 and 12.6. Both over-predict the innermost bins. The forward model's point-mass baryons, with no stellar extent, mis-centring or satellites, are shared limits.
- **Reported rows:** the Sérsic replicate gives Â = 0.70 ± 0.17 (χ² 6.5/7). All 15 bins, with no 2-halo term, give Â = 1.20 ± 0.14 (χ² 45.8/15). The M_gal-weighted weight below Mandelbaum's measured range (where halo masses are clamped) is 1.9% for early and 14.9% for late.
- **Controls:** C1 reproduces CFG61's χ²_L = 28.07; in C2, the NFW gives M(<R_200c)/M_200c − 1 = 2 × 10⁻¹⁶ and the projector matches Wright & Brainerd to 2.6 × 10⁻⁵.

## Caveat (frozen up front)

The colour-split relation is calibrated on SDSS lensing, so the headline pass is consistency between SDSS and KiDS under standard halos, not a first-principles prediction. The colour-blind Moster variant is the a-priori version, and it also fits.

κ = ½ and Ω_c h² stay fitted. Nothing here says the theory is closed.

## Data requirements (not in git)

Like CFG61, this script needs local data that git ignores, in `real_research/data/lensing_rar/` (about 17 GB), so **it cannot run from a clean git-archive export**:
- `brouwer2021_rar/Fig-8_*.txt` and the covariance files. These are Brouwer+2021's public release, unpacked from `brouwer2021_rar.tar`; the source and DOI are in `real_research/reviews/lensing_rar/lr_data_acquisition.md`.
- `lr_lenses.npz`, built by `real_research/reviews/lensing_rar/lr_esd_remeasure.py` (`stage_lens`) from the KiDS DR4 bright-sample catalogue in the same directory.
An independent in-place re-run by the equations session reproduced the outputs.
