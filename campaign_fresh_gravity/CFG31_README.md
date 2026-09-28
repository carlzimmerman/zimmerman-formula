# CFG31 — the Coma ultra-diffuse galaxies under candidate B

Script: `CFG31_coma_udgs_under_b.py`, under a second.
- Outputs: `.out` and `_results.json`.
- MUTATE control: `_MUTATE.out` and `_MUTATE_results.json`. Every dispersion is doubled, and the headline H1 fails (4.7 / 4.5σ, rc = 1).
- The main run passes 11 of 11 checks and exits 0.

κ = ½ is fitted. Both footings are used.

## Question

The failures summary carried the Coma UDGs as liability B2. Eleven galaxies (Freundlich+2022; dispersions from Chilingarian+2019, and from van Dokkum+ for DF44 and DFX1) sit +1.16 / +1.11 dex in acceleration above the framework's external-field prediction. That is 4.9 / 4.7σ with L23's systematic floor (`fable_independent_2026/L23_udg_verify.py`).

That prediction applied Coma's external field. Candidate B does not. Under FG001's ownership rule a UDG that fell into Coma is *accreted*, and an accreted system obeys the *isolated* law of its *infall* baryons. CFG18 applied the same rule to the Local Group's satellites, where it removed the M31 tension.

**This is a re-scoring under B's own rule, not a blind test.** L23 had already computed the stars-only isolated offset (+0.397 / +0.357 dex). The infall-gas number and the recomputed systematic floor were new.

## Method (declared before the first run)

- **Data and estimator:** L23's, exec'd read-only (r_1/2 = 4R_e/3; g_obs = 3σ²/r_1/2; g_bar = G(M_b/2)/r_1/2²; L23's errors and inverse-variance weighting). This is FG001's own convention for accreted systems.
- **B's prediction:** the isolated law, no external field, kernel ν_mono (P2 reported).
- **Infall baryons:** M_* plus the infall gas. Each galaxy's gas-to-star ratio is drawn from its 5 nearest members of CFG18's calibration set (42 LVD field dwarfs) in log M_*, over 2000 realisations. HI non-detections count as zero (the headline) or at their upper limit (reported).
- **The systematic floor, recomputed for the isolated law** from L23's entries by re-running the pipeline:
  - stellar M/L: 0.078. This is half the 0.148 of the external-field reading, because in deep MOND the prediction scales as √M.
  - aperture and anisotropy: 0.120.
  - the instrumental term: 0.052.
  - the estimator: 0.047.
  - distance: 0.021.
  - The Coma mass model and 3-D position do not apply without an external field.
  - The floor is **0.161 dex**, against 0.227 for the external-field reading.

## Results

**Controls.**
- C1: L23's committed isolated offsets are reproduced (+0.3965 / +0.3573).
- C2: CFG18's calibration set is rebuilt exactly (42 dwarfs, 32 detections, log M_* 4.98–9.65). The UDGs (log M_* 7.70–8.59) lie inside it.

**Hypotheses.** Offsets are in dex of acceleration.

| | canonical | alt | verdict |
|---|---|---|---|
| H1 (headline): B's isolated law, infall baryons | **+0.234 ± 0.176 → 1.3σ** | **+0.195 ± 0.176 → 1.1σ** | PASS |
| H2: DF44 alone (Keck/KCWI) | +0.162 ± 0.237 → 0.7σ | +0.123 → 0.5σ | PASS |
| H3: UDGs vs CFG18's M31 dwarfs (dex in σ) | +0.117 ± 0.088 vs +0.078 ± 0.048 → 0.4σ | 0.4σ | PASS: one accreted class |

**Reported rows** (canonical / alt).

| row | result |
|---|---|
| R1 stars only (the current baryons) | +0.397 → **2.3σ** / +0.357 → 2.1σ |
| R2 non-detections at their limits | unchanged: every calibration dwarf near the UDGs' masses is an HI detection |
| R3 the P2 kernel | +0.257 / +0.217 |
| R4 the Milgrom-1994 virial estimator | +0.286 / +0.245 |
| R5 the Keck pair vs the Chilingarian nine | +0.165 ± 0.116 vs +0.261 ± 0.073 |
| R6 the common gas-to-star ratio that would null the offset | 4.5 / 3.7, against calibration dwarfs at 0.26–3.92 |
| R7 the external-field rival (L23) | +1.159 → **4.9σ** / +1.112 → 4.7σ |

## Standing

**The 4.9σ Coma liability belongs to the external-field reading, not to candidate B.** Under B's ownership rule the eleven UDGs sit at +0.23 / +0.19 dex (1.3 / 1.1σ). DF44, the best-measured one, sits at 0.7σ. The UDGs agree with the M31 satellites under the same rule, so the rule treats cluster-accreted and group-accreted systems as one class.

What carries the result:
- **Dropping the external field does most of the work:** 4.9σ becomes 2.3σ with stars alone.
- **The infall gas does the rest** (2.3σ becomes 1.3σ). That gas is drawn from ordinary field dwarfs of the same stellar mass, not from UDG progenitors. Field UDGs may be more or less gas-rich.

**Caveat.** This pass is exactly as strong as B's ownership rule. B says a cluster member's internal dynamics ignore the cluster's field, which is a strong-equivalence-principle choice other data constrain:
- Chae's wide-binary external-field signal costs B 1.7–2.2σ (CFG8).
- Gaia DR4 tests the rule directly: under it, wide binaries are exactly Newtonian.

The UDGs are consistent with the rule; they do not prove it.

Nothing here says the theory is closed.
