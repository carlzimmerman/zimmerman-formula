# CN1_contraction_on_cold_share: CONTRACTION BREAKS SPARC on FC1's rule, with no softening on the grid that repairs it. FC1's pass requires zero net cold response from L★ galaxies to clusters, and the known responses point the wrong way

Criteria: `FROZEN_CRITERIA.md` (38a6fb863e), committed alone before any script or number. Scripts `cn1_x74.py`, `cn1_run.py`, `cn1_bins.py`. Outputs `cn1.out`, `cn1_results.json`, `cn1_bins.*`. Post-result, reported only: `cn1_energy.py`, `cn1b_run.py`, `cn1c_run.py` and their outputs.

## Frozen grade (f★ 0.034, median η, canonical primary)
**LABEL, both footings: CONTRACTION BREAKS (SPARC line); R_SPARC NONE ON GRID; R_CL 1.0, REACHABLE.**

| R (softening before contraction) | SPARC Υ can. (A/B) | SPARC Υ alt | G-IN-Mall | G-MID-T3 | cluster fails |
|---|---|---|---|---|---|
| 1.00 | 0.31 / 0.31 | 0.30 / 0.30 | −1.30 | −1.00 | none |
| 0.80 | 0.33 / 0.33 | 0.30 / 0.30 | −0.76 | −0.31 | none |
| 0.60 | 0.36 / 0.36 | 0.33 / 0.34 | −0.17 | +0.58 | none |
| 0.50 | 0.39 / 0.39 | 0.36 / 0.37 | +0.14 | +1.13 | none |
| 0.40 | 0.44 / 0.44 | 0.37 / 0.37 | +0.47 | +1.79 | G-MID-T3 UNDER |
| 0.30 | 0.48 / 0.47 | 0.40 / 0.40 | +0.81 | +2.59 | G-MID-T3, G-MID-b UNDER |

Gnedin at R 1: Υ 0.34 / 0.35 (canonical), clusters pass. Groups are not contracted, as X39. Rms: 0.0728 at R 1, about 0.064 at R 0.55–0.7.

**By V_flat (LS1's bins), canonical, Υ / ΔV at Υ 0.50:**
| R | 100–150 (4/23 active) | 150–200 (25/25) | 200–250 (18/18) | 250–400 (10/10) |
|---|---|---|---|---|
| 1.0 | 0.71 / −5.6 | 0.30 / +39.2 | 0.34 / +33.2 | 0.46 / +11.0 |
| 0.8 | 0.71 / −5.6 | 0.30 / +32.7 | 0.39 / +24.8 | 0.49 / +2.7 |
| 0.6 | 0.74 / −6.1 | 0.34 / +24.3 | 0.42 / +13.8 | 0.54 / −6.8 |
| 0.4 | 0.74 / −10.2 | 0.41 / +11.6 | 0.48 / −1.2 | 0.59 / −18.7 |
| 0.3 | 0.74 / −10.2 | 0.47 / +4.3 | 0.56 / −10.9 | 0.65 / −26.0 |

Softening needed before contraction falls with mass: R ≈ 0.3 at 150–200, 0.4 at 200–250, 0.8 at 250–400, none in clusters. No single R works, and below R ≈ 0.45 clusters fail.

## Reported: energy to undo the contraction
At Υ 0.50, as a fraction of each galaxy's SN energy (BE1's budget): median **0.094** [0.055, 0.122], max 0.157; by bin 0.043 / 0.070 / 0.100 / 0.125. Below 1, so not excluded by the budget. But CM1's gravity-only channel at measured gas delivers about 0.3 % of E_SN into the cold fluid (0.4 % of a lift that costs 76 % of E_SN), about **30× short**; CM2/CM3's reach needs coupling ≈ 1 and rare bursts, and even those were measured without a disc to fight.

## Reported: clusters
**CN1b, Blumenthal + BCG on clusters, none on SPARC.** f★ 0.034 canonical: Υ 0.51 / 0.50, groups +1.62, G-IN-Mall −1.30, G-MID-T3 −1.00, G-OUT-M3 −0.98, G-OUT-all −1.37, nothing failing. p16 passes, p84 fails only the SPARC line (0.49). f★ 0.0615: median and p16 pass, worst −1.54. In clusters the hot gas is less concentrated than the cold fluid, so Blumenthal expands the cold fluid.

**That was a selective application, and its sign is doubtful.** It applies the response where it helps and drops it where it hurts. And Blumenthal has no energy exchange. Non-radiative hydrodynamic runs that start from the same dust-plus-gas situation report the opposite sign: dark matter concentration higher by about 10 %, with gas gaining energy at the collisionless component's expense ([Rasia+04](https://arxiv.org/abs/astro-ph/0309405), [Lin+06](https://arxiv.org/abs/astro-ph/0607555)). These were read from search excerpts of ΛCDM-background runs, so they are physics context, not inputs, and are provisional.

**CN1c, how much net response can clusters take?** No contraction; collapse-branch cluster S × R_c:

| R_c | f★ | G-IN-Mall | G-MID-T3 | keys over 2 |
|---|---|---|---|---|
| 0.90 | 0.034 | −1.61 | −1.35 | none |
| 0.95 | 0.034 | −1.78 | −1.54 | none |
| 1.00 (= FC1) | 0.034 | −1.95 | −1.71 | none |
| 1.05 | 0.034 | −2.11 | −1.88 | G-IN-Mall |
| **1.126 (c +10 %, η ∝ c^(5/4))** | **0.034** | **−2.35** | **−2.12** | **G-IN-Mall, G-MID-T3** |
| 1.00 | 0.0615 | −2.00 | −1.93 | G-IN-Mall |
| 1.126 | 0.0615 | −2.42 | −2.35 | G-IN-Mall, G-MID-T3 |

So FC1's clusters have room for **no more than about +1.5 % in S**. If the hydro sign holds at the cited size, the cluster pass is lost.

## The job this states
FC1's edge assumes the cold fluid does not respond to baryons at all. CN1 shows that to be load-bearing at both ends: the galaxy end breaks by a large margin under contraction, the cluster end breaks under a small net contraction. The rule needs **net response R ≈ 1, within about +1.5 % on the high side in clusters and well below contraction in galaxies.** No calculation in this record produces that.

## Checks
K1 (contraction off reproduces FC1, 0.0), K2 (identity 7.2e-15, closed form 1.3e-8), K3 (BCG 190), MUTATE ((1 − F) fails K2's closed form at 0.333): PASS. CN1c: R_c 1 reproduces FC1's four cluster keys at both f★, both footings, |d| 0 (run by hand after the run, because the in-script check had a wrong file name and was skipped).

**Disclosures.** First launch stopped at `NameError REPO`, before any number. X39's closed form was rewritten for the K2 test range. A first CN1b temp-folder path was wrong and was fixed before a run. Cluster η is ng 48 until A4.

## What this does not show
- Blumenthal is a limit: slow, circular, no feedback. Real settling may be weaker. Gnedin, also calibrated, still fails on SPARC.
- The R comparison assumes softening acts before contraction, at reach measured without a disc. Neither is shown.
- A required R does not derive that R.
- The floor-branch decision (no contraction there) was stated before any number but it is a modelling decision, and it creates a jump at the branch crossing.

κ = ½ FITTED. Footings never pooled. Cold dark energy is a gravitating field component, never a particle. Not theory closed. Nothing here says the data favour the framework.
