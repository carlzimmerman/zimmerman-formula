# CFG36 — the conservation rule with measured, colour-split collapse masses

Script: `CFG36_colour_split_collapse.py`, a few seconds.
- Outputs: `.out` and `_results.json`.
- MUTATE control: `_MUTATE.out` and `_MUTATE_results.json`. The colours are swapped, and H2 fails (rc = 1).
- The main run exits 1: H1 and H2 both failed. That is reported as run.

## Question

CFG35's derived conservation rule closed the X-ray ellipticals but broke the massive SPARC spirals. It used a colour-blind stellar-to-halo relation that puts every log M_* ≈ 11.4 galaxy in a ~10¹⁴ M☉ collapse.

Weak lensing measures the collapse mass by colour. Mandelbaum+2016 (MNRAS 457, 3200, Table 3) is now transcribed with provenance to `real_research/data/mandelbaum2016_lbg_halo_mass.tsv`, from the arXiv source (3.6 MB, fetched with the owner's approval). Passive centrals sit in 3–7× heavier halos than star-forming ones at the same stellar mass.

## Method

This is CFG35's machinery exec'd read-only, with one change: the collapse mass is Mandelbaum's ⟨M_200m⟩ converted to M_200c on the same NFW.
- The ellipticals take the red relation.
- SPARC late types take the blue relation, and its S0s the red.

**Disclosed change before the main run.** Clamping the table at its low end gave dwarfs the collapse mass of a 10¹⁰-star galaxy. H2 is therefore evaluated only over the table's measured range (log M_* ≥ 10.0, 61 SPARC galaxies). CFG35's colour-blind relation already gave every dwarf f_ex = 0.

## Results

- **C1, C2 (controls):** the table (14 rows; red − blue = 0.56 dex at log M_* 11.3) and the 200m → 200c conversion (3e-15) check out.
- **H1 failed, narrowly: the ellipticals half-close.**
  - The red relation gives collapse masses of 2–6 × 10¹³, about 4× below the colour-blind ones, so the leftover fraction is 0.35–0.67.
  - The mean offset goes from +0.28 under the law to **+0.125 ± 0.120 dex (1.04σ canonical, 1.03σ alt)**, against the declared "better than 1σ".
- **H2 failed on one galaxy: every late-type spiral is clean.**
  - f_ex = 0 in 98% of the 61. Among them are UGC 2885, NGC 6195, UGC 11455 and ESO563-G021, which CFG35 broke.
  - The single failure is **UGC 2487, an S0** (T = 0, log M_* 11.5). Given the red relation, its leftover would raise v_c at R_HI by **+0.14 dex**, but its rotation curve follows the law.
- **R1:** at the +1σ halo masses the picture is the same (98%, +0.146). Across the edge window the ellipticals sit at +0.10 to +0.15.

## Standing

The measured colour split moves B's conflict rather than removing it:
- **Massive star-forming spirals are safe.** Their measured collapse masses are small enough for the law's phantom to use all their cold fluid.
- **Massive passive galaxies get real extra mass.** It closes about half of the X-ray ellipticals' gap.
- **The price is passive disks.** A passive galaxy with a measured rotation curve (UGC 2487) should rotate faster than the law at large radii, and it does not.

**What decides it** is a sample of passive (S0 or early-type) disks with extended rotation curves or HI kinematics. Under the conservation rule they must deviate from the law at large radii by roughly the amount their colour's collapse mass implies. SPARC has only one. Nothing here says the theory is closed.
