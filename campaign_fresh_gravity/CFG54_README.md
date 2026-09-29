# CFG54 — the pre-registered a₀(z) check on the PHIBSS sample: empty, therefore non-diagnostic

Script: `CFG54_phibss_a0z.py` (about 1 s). Data: `data_assembly/kmos3d_phibss/phibss13_joined.csv` (the data-assembly thread's join of Tacconi+2013 tables 1 and 2; 73 galaxies at z ≈ 1.2 and 2.2). Outputs: `.out`, `_results.json`, and the MUTATE pair. Assigned by the coordinating session; the criteria were frozen in the docstring before the first run. **The main run exits 1 because the feasibility gate H0 failed: this is the declared, valid result.**

## The frozen check

Flat a₀ (branch A) against a₀ E(z) (the H(z)-tracking rival), scored on discs with **g_bar < a₀** where the velocity is measured, with a correlated 0.2-dex mass-scale systematic and 25% velocity errors, and a feasibility gate (N ≥ 5, else the lane is declared non-diagnostic). Sample: rows with a velocity, a radius and a redshift, excluding the six 3σ gas upper limits and the three rows whose quoted f_gas their masses do not reproduce (51 remain). Baryons: an exact Freeman disc of M_* + M_mol with R_d = r_h/1.68. The table does not say where the velocity is measured; I declared r_v = 2.2 R_d = 1.31 r_h (the ledger's convention). **Mismatch stated:** Tacconi+2013's velocities are CO or Hα rotation velocities with their own inclination and pressure corrections; no σ₀ term is applied here.

## Result

**N = 0 of 51.** The lowest g_bar/a₀ at r_v = 1.31 r_h is 1.10 (then 1.11, 1.28; the median is 4.7 and the maximum 114). **No PHIBSS disc is in the regime where a₀ shows at the frozen velocity radius.** H1–H3 are not scored. The lane is non-diagnostic. This agrees with CFG52 (no clean object with g_bar < 0.3 a₀ at z ≥ 1.5) and with the data-assembly thread's warning that most high-z discs are baryon-dominated where measured.

**The MUTATE control is vacuous here.** Selection precedes the velocities, so with H0 failing, H1 and H2 are never scored. The mutated run fails H0 exactly as the main run does. I disclosed this in the docstring after the run.

## Post-hoc sensitivity (reported, added after the main run; not a test)

How many of the 51 would qualify if the velocity were measured farther out: at 1.31 r_h **0**; at 2 r_h **7** (lowest g_bar/a₀ 0.63); at 3 r_h **20** (lowest 0.29); at 4 r_h **31** (lowest 0.16). So **the answer hinges on the radius where Vrot was measured, which the table does not carry.** If Tacconi+2013's velocities come from radii beyond about 2 r_h, a usable sample of 7–20 discs exists. I have not run the test at any such radius, because choosing it after seeing the counts would not be pre-registered.

## What would make it a test

1. The radius at which each Vrot was measured (from the Tacconi+2013 paper's figures or text, or the CO extents), then a fresh pre-registered run with that radius. This needs the paper's source (not in the repo) and would need the owner's approval to fetch.
2. Independent mass calibration at about 0.1 dex: the sample's own systematics (Mmol 50%, M* 30%) already cap the significance near 2.3σ (CFG52's forecast).

Nothing here says the theory is closed.

## Referee corrections (09-28 audit of the lane READMEs against their outputs; appended, the text above is unchanged)
- 'N = 0 of 51' is the canonical footing only (a0 = 9.3603e-11); the alt footing is not scored. Scaling the printed ratios (not re-run) gives about 2 rows below 0.3 a0 at a0 = 1.1312e-10, still below 5, so non-diagnostic holds either way. The 2.3 sigma cap comes from CFG52's generic correlated 0.2-dex floor, not from this sample's own systematics.

## Referee correction (CFG90's independent re-derivation; appended)
- N = 0 of 51 reproduces (lowest g_bar/a0 = 1.097, 1.109, 1.281) but is a knife-edge on an assumed velocity radius: Tacconi+13's Vrot defines no radius; the lowest object is 10% from the threshold and far inside the 0.2-dex mass floor; the N >= 5 gate fails at 1.31 r_h and passes from 2 r_h (N = 7; sweep 0 / 7 / 20 / 31 at 1.31 / 2 / 3 / 4 r_h), and on the alt footing at 1.31 r_h N = 2. 'Non-diagnostic' is a statement about the assumed radius. See CFG90.
