# CFG61 — the KiDS-1000 early/late lensing split against B's law and B's derived rule

- **Criteria:** frozen and committed before any scoring, in `CFG61_FROZEN_CRITERIA.md` (commit d7aecf12b).
- **Script:** `CFG61_kids_colour_split.py` (both footings; about 50 s). Its MUTATE control, which swaps the early and late data, exits 1 as required.
- **Outputs:** `CFG61_kids_colour_split.out` / `_results.json`, and the `_MUTATE` pair.

## Bottom line

**B's derived rule makes no colour-dependent prediction for KiDS's isolated lenses, so it cannot explain the split. The early-minus-late difference rejects B, with or without the rule, at χ² = 28.1 / 7 (p = 2.1 × 10⁻⁴, about 3.7σ) in the isolation-reliable 1-halo bins, on both footings.**

- **Why the rule adds nothing.** With Mandelbaum's measured collapse masses, the rule's red debris switches on only above log M_* ≈ 11.2. The KiDS isolated sample stops at log M_* = 11.0. Its maximal predicted split is 1.2 × 10⁻³ (canonical) and 2.4 × 10⁻⁴ (alt) of the data errors.
- **The frozen amplitude statistic is therefore degenerate** (Â = −1,710 ± 2,580). The frozen H1 was written as "Â/σ_A > 3, *equivalently* χ²_L p < 0.0027". The two forms agree only when the rule predicts a split. **Both are reported, and the coded verdicts are kept as they fell** (see Disclosures).

## Data and model (as frozen)

- **Data:** Brouwer+2021 Fig. 8, released ESD profiles in 15 bins of baryonic acceleration g_bar, for u−r < 2.5 (late) and u−r ≥ 2.5 (early), with the full 30×30 covariance.
- **Lenses:** 181,477 lenses from the repo's reconstruction (`lr_lenses.npz`), used as class proxies.
- **Forward model:** built lens by lens. Each lens contributes at R = √(G M_gal / g_bar). The law is truncated at B's edge (0.4 r_ta, with B's committed r_ta at each lens redshift), and the rule's debris uses CFG36's colour-split collapse masses.
- **Headline range (K1):** the seven bins where both classes' lens-weighted median R is below 0.3 Mpc, from 44 to 286 kpc.

## Results

| Test | Canonical | Alt |
|---|---|---|
| Controls C1–C4 | all pass | |
| **H1, amplitude form** (Â/σ_A > 3) | **fails:** −0.66σ (degenerate) | −2.25σ |
| H1, χ² form (frozen as equivalent) | rejects the law: χ²_L = 28.1/7, p = 2.1e-4 | same |
| **H2 (headline)** (rule accounts for the split) | **fails:** χ²_S = 28.1/7, p = 2.1e-4 | same |
| MUTATE (early/late swapped) | H2 fails; exits 1 | |

**Controls.** The four controls pass. C1 reproduces the committed split from the released files (u−r 119.9/15, Sérsic 69.1/15). C2's projector matches Wright & Brainerd to 3 × 10⁻⁵. C3's lens counts and medians are exact. C4 finds the law's ΔΣ at fixed g_bar mass-independent to 4 × 10⁻⁶, the deep-regime identity that makes the law colour-blind.

**H3 and the reported rows:**
- **H3 (absolute profiles):** late lenses against the law give χ² 12.6/7 (p ≈ 0.08); **early lenses against the law give χ² 51.9/7**. The law sits between the two classes: late types slightly below it, early types well above it.
- **R1, Sérsic replicate:** χ²_L = 20.9/7.
- **R2, Σ_crit⁻² weighting:** χ²_L = 28.1/7, unchanged.
- **R3, class medians:** log M_gal 10.448 (late) and 10.810 (early).
- **R5, all 15 bins** (the 2-halo range included, not modelled): χ²_L = 124/15.
- **R4, the hot gas the law would need:** the law alone fits the difference if early-type lenses carry **at least about 1–1.5 × their stellar plus cold-gas mass** in extra baryons relative to late types (χ² 4.8 and 4.1/7 at f_hot = 1 and 1.5). The gas is treated as a point mass, which maximises its effect per unit mass, so the requirement is a lower bound. This is the one baryonic escape, and it is untested here: CGM hot-gas masses by colour are not on disk.

## Disclosures (kept as they fell)

- **The degenerate amplitude.** The frozen amplitude statistic assumed the rule predicts a split. It does not at these masses (the DEGENERACY row), so Â and σ_A are meaningless here. The script's mechanical reading, "the split does not reject the colour-blind law", follows the amplitude form. It is printed, and then corrected in a labelled "DISCLOSED (post hoc)" line. The H1 χ² form and the DEGENERACY diagnostic were added after the first run, as **reported** rows; the load-bearing verdicts were not changed.
- **Two fixes before the first run**, disclosed here: the mass grid was extended to log M_* = 11.8 so the R4 diagnostic isn't clipped, and a NumPy `trapezoid` fallback was added.
- **Caveats.**
  - `lr_lenses` classes use rest-frame u−r > 2.0, not Brouwer's GAaP u−r ≥ 2.5, and its isolation is the repo's reconstruction (181,477 lenses against Brouwer's 259,383). The class mass distributions are proxies.
  - Lenses below log M_* 10.28 carry the rule's clamped collapse mass (the standing artefact); its effect here is at most 0.02 Msun/pc².
  - Satellite contamination, which is higher for red lenses, is limited by staying inside 0.3 Mpc, Brouwer's isolation-reliable range. It is not modelled.

## Reading

**This is a new failure row for candidate B, next to gate 3.05.** B passes the combined KiDS isolated-lens gate but fails its colour split at about 3.7σ in the 1-halo regime.
- The derived rule was built on the same colour dependence, imported from SDSS lensing, but **it does not act at the masses where KiDS measures the split**. So the rule does not rescue B here.
- A colour-blind dark mass survives only if early-type lenses hold about 1–1.5 × their stellar plus cold mass in additional (hot) baryons.

κ = ½ and Ω_c h² stay fitted. Nothing here says the theory is closed.

## Data requirements (not in git)

This script needs local data that git ignores, in `real_research/data/lensing_rar/` (about 17 GB), so **it cannot run from a clean git-archive export**:
- `brouwer2021_rar/Fig-8_*.txt` and the covariance files. These are Brouwer+2021's public release, unpacked from `brouwer2021_rar.tar`; the source and DOI are in `real_research/reviews/lensing_rar/lr_data_acquisition.md`.
- `lr_lenses.npz`, built by `real_research/reviews/lensing_rar/lr_esd_remeasure.py` (`stage_lens`) from the KiDS DR4 bright-sample catalogue in the same directory.
An independent in-place re-run by the equations session reproduced the outputs.

## What the MUTATE control shows here (added on review)

**CFG61's MUTATE control does not differ from the main run in substance.** Swapping the early and late classes flips the sign of the degenerate amplitude (Â −1709.6 → +1711.5, canonical) and swaps χ²_L and χ²_S (28.07 ↔ 28.10). It changes nothing else, because the law and the rule predict no split (D ≈ 0), and a χ² about a zero prediction is unchanged when the classes are swapped. Both runs exit 1 on the same two checks, so this control cannot tell a working pipeline from a broken one for this lane. The substantive control is CFG67's: through the same machinery, ΛCDM's predicted split moves from χ² 6.5/7 to 124.1/7 when the classes are swapped.


## Corrections from the referee sweep (appended 2026-09-29; no result changed)

A referee sweep re-ran this lane (outputs byte-identical apart from timing). Its wording findings, each re-checked here against `CFG61_kids_colour_split.out`:

- **The 3.7σ in the bottom line is a reported χ² row evaluated after the first run.** The frozen amplitude statistic was degenerate, and H1 and H2 failed as coded (see Disclosures). The bottom line should have said so.
- **The Sérsic replicate is weaker:** χ²_L = 20.9/7, p = 0.0039 (2.9σ), against 28.1/7 (3.7σ) for the u−r split.
- **R4 was overstated** (the R4 bullet and the Reading). The grid printed in the `.out` is below: χ²_L of the difference (7 dof), with the early class's mass multiplied by (1 + f_hot).

| f_hot | 0 | 0.25 | 0.5 | 1 | 1.5 | 2 | 3 | 4 |
|---|---|---|---|---|---|---|---|---|
| χ² / 7 | 28.1 | 18.2 | 10.0 | 4.8 | 4.1 | 10.4 | 26.9 | 58.4 |
| p | 2.1e-4 | 0.011 | 0.19 | 0.68 | 0.77 | 0.17 | 3.5e-4 | 3e-10 |

So the law is acceptable at the 3σ line (p > 0.0027) from f_hot = 0.25 on this grid, and at p > 0.05 from 0.5. The values 1–1.5 are the best fit, not the threshold. **Corrected sentence:** a colour-blind dark mass survives the split if early-type lenses hold at least about 0.25–0.5 × their stellar plus cold mass in extra baryons. That is a lower bound, since the gas is a point mass. The best fit is at 1–1.5×, and f_hot ≥ 3 is rejected again.

- **"Exits 1 as required" (the Script line) says nothing here.** The main run also exits 1, failing the same two checks (H1 and H2). See the MUTATE section above.
