# CFG41 — the massive passive disks: Di Teodoro+2023's 15 HI rotation curves under B's law and cold-mass rule

Script: `CFG41_massive_spirals_hi.py`, about 5 s. Companion: `CFG41_selbias_mc.py` (the selection-bias Monte-Carlo, about 4 min; output `CFG41_selbias_mc.out`).
- Outputs: `.out` and `_results.json`.
- MUTATE control: `_MUTATE.out` and `_MUTATE_results.json`. Observed speeds are multiplied by 0.5, and H1 and H2 both fail.
- The main run exits 1 because **the control C2 failed as declared** (below). H1, H2 and H3 pass.

## Question

CFG37 said the derived rule bites only above log M_* ≈ 11.2 on the red sequence, and that "none is in the repository". Di Teodoro et al. 2023 (MNRAS 518, 6340; arXiv:2207.02906) measured HI rotation curves out to 30–97 kpc for 15 galaxies of log M_* 11.0–11.7, including four S0 / S0a (NGC 1167, NGC 5790, UGC 12591, UGC 12811): the population the rule makes a prediction about.

## Data

- `real_research/data/diteodoro2023_massive_spirals.tsv`: the paper's tables (masses, tabulated v_flat).
- `real_research/data/diteodoro2023_hi_rotation_curves.tsv`: **216 recovered points**. The paper does not tabulate its curves. They were read from the vector coordinates of the atlas figures' plotted points by a delegated agent, calibrated on the axis tick labels, so they are the plotted values (R to about 0.1 kpc, V under 1 km/s). The extraction scripts are in `diteodoro2023_extraction/`.
- `real_research/data/diteodoro2023_morphology.tsv`: RC3 type and WISE W2−W3 (catalogue row queries, not independently re-verified).

## Two things to know before the numbers

**A selection bias that pushes one way.** The sample was selected on HI width (> 300 km/s) and M_* > 10¹¹. Cutting on observed speed keeps upward fluctuations, so the raw offset is biased high. The Monte-Carlo (`CFG41_selbias_mc.py`, choices declared in its docstring) gives +0.067 to +0.085 dex where the mock matches the real sample's mean speed and mass, and +0.003 to +0.154 across its whole grid. The correction used is **B = 0.076 ± 0.030 dex**, subtracted from every offset, with its error in the floor. It leans on the mass function and the width-error model. It cannot be checked on this sample.

**Control C2 failed as declared.** The Lelli+2016 algorithm, run on the recovered points exactly as their paper states it, reproduces the tabulated v_flat within 3 km/s for **10 of 15** galaxies. I had declared 12, from the delegated reader's own report, which I could not reproduce with the same algorithm on the same points. The five misses are 3–12 km/s, inside the quoted errors. Three (NGC 1324, NGC 5790, UGC 02849) are still declining at the last point and the paper's v_flat equals the outermost point. The tolerance is unchanged. The test below does not depend on the algorithm's value: it uses the paper's tabulated v_flat, with a ±25% radius floor.

## Method (declared before the first run)

- The same machinery as CFG40 and CFG37: Mandelbaum's blue and red collapse masses, the conservation form at x_e = 0.40, ν_mono, both footings.
- Baryons: M_* from WISE (Υ = 0.6) plus 1.36 M_HI. Radius: the mean radius of the Lelli-included points. A point mass is the headline (the flat parts lie at 15–97 kpc), with exponential-disc and spherical brackets at R_d = 8 kpc.
- Colour: RC3 type ≤ 0 red, else blue (CFG36's convention).
- Floor: the baryon model, M_* (±0.2 dex), gas (±0.1 dex), radius (±25%) and B's error.
- **H1:** the bare law fits after the correction. **H2 (headline):** B fits (mean over 15) and does not over-predict the four S0/S0a. **H3:** the rule bites (f_ex > 0 in at least 2 of the four).

## Results

| sample | law, raw | law, corrected | B (law + rule), corrected |
|---|---|---|---|
| all 15 | +0.048 | **−0.028 ± 0.066 (−0.43σ)** | **−0.057 ± 0.081 (−0.71σ)** |
| the four S0 / S0a | +0.080 | +0.004 ± 0.071 (+0.05σ) | −0.105 ± 0.131 (−0.80σ) |

- **H1 passed.** After the correction the bare law fits the 15 (canonical; alt −0.045, −0.69σ).
- **H2 passed.** B fits the 15, and the rule does not over-predict the four S0 / S0a at −0.8σ.
- **H3 passed.** The rule bites: f_ex = 0.31 (NGC 1167), 0.31 (NGC 5790), 0.78 (UGC 12591) and 0.49 (UGC 12811). This is the first time the rule adds mass to more than one passive *disk* above log M_* 11.2 that has an HI rotation curve (before: SPARC's UGC 2487; the SLUGGS ellipticals of CFG38 were dispersion-supported).
- **Sensitivity (reported).** WISE colours instead of RC3 type: law −0.028, rule −0.051. Excluding the two galaxies the paper flags as uncertain (NGC 5635, UGC 12591): law −0.038 (−0.60σ), rule −0.066 (−0.81σ).
- **Per galaxy, uncorrected.** The rule puts the four S0 / S0a slightly fast (−0.02 to −0.04 dex), and the law puts them slow (+0.08 on average). The correction turns these into rule −0.105 and law +0.004.

## Independent referee (2026-09-28)

Reproduced: raw law mean +0.048, the algorithm within 3 km/s for 10 of 15. Its selection-bias Monte-Carlo matches the lane's magnitude for matched rows (+0.077). Adding 0.2-dex stellar-mass errors to the mock, which the lane's Monte-Carlo omits, lowers the matched bias to +0.058, so **B is plausibly about 0.02 dex too large and the corrected mean −0.010 rather than −0.028**. H1 passes for any B from 0 to 0.10, so no verdict changes. The bias scales roughly as s_int², which the data do not identify; across the whole grid it runs 0.00–0.15 and the ±0.030 covers only the matched rows. Under B = 0 the CFG40–CFG41 difference is 0.059, not 0.135.

## Standing

**The first massive passive disks with extended HI kinematics are consistent with both the bare law and the derived rule. The test does not decide between them.** The four S0 / S0a error on the rule (0.131 dex) is dominated by the 0.2-dex stellar-mass systematic, because the collapse mass depends steeply on M_*; the law's is 0.071. After the selection correction neither is off by more than 1σ. Nothing here favours the rule over the law.

**It is consistent with CFG40, not in tension.** Ogle's luminosity-selected star-forming super spirals need no selection correction and sit +0.107 ± 0.075 above the law; this sample, after the correction, sits −0.028 ± 0.066 (raw +0.048). The difference, 0.135 ± 0.10, is 1.3σ. Different tracers (Hα maxima at 14–54 kpc against HI flat parts at 15–97 kpc) and selections limit what more can be said.

**UGC 2487 (SPARC's S0) stays a 0.14-dex over-prediction by the rule (CFG36).** The four new S0 / S0a point the same way but weakly: the rule over-predicts them by 10% after the correction (−0.105 ± 0.131, 0.8σ), and by 5–9% before it. They neither confirm nor remove that worry.

Nothing here says the theory is closed.
