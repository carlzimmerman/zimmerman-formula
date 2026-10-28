# HO1_xcop_hotgas_heldout: the frozen CL2 picture FAILS both held-out tests, on both footings

**Provenance.**
- Criteria and ledger: `FROZEN_CRITERIA.md` and `ASSUMPTION_LEDGER.md`, committed alone in 95341eda1a before any script or
  number.
- `AMENDMENTS.md` A1 (af70a0b593) was committed alone before the rerun. It fixes a check definition (K2) and a label. No
  number or class changed.

**Run conventions.**
- κ = ½ is FITTED.
- The two footings are scored separately and never pooled. Canonical is the primary.
- Route E. Cold dark energy is a gravitating w ≈ 0 field component, never a particle.
- Not "theory closed". Nothing here says the data favour the framework or ΛCDM.

**What was tested.** The CL2 picture, implemented by executing CL2's own source at its passing point (S9 shape, L = 4,
T = 12.3, GS1 measured cluster budget):
- the switch at M200 10^12.3 or satellite;
- the galaxy law on baryons below the switch;
- route-E Burkert halos above it, with Σ = max(a₀/2πG, η(M) Σ_coll(M));
- c_f(M) = 4 c_nat(M)/c_nat(10^14);
- the native fair-share cluster budget to the turnaround radius, with gas slope 2.777 beyond R500.

It was graded on two data sets that no calibrating lane graded. Nothing was refit.

## Step 0 (stop rule): all reproduced exactly (max |d| = 0)

| part | what was reproduced |
|---|---|
| S0-CL2 | CL2's S9 L4 T12.3 X43 grade (SPARC, groups Z +1.99, all 2×15 cluster keys), re-run in this lane |
| S0-CS2 | CS2's X-COP grader: CS2 law −0.151 / 0.205; OS1 −0.075 / 0.124 (canonical) and −0.035 / 0.092 (alt) |
| S0-HG2 | HG2: D −0.294 [−0.511, −0.076], power 0.448, 188 supported groups |

## Result

| line (frozen rule) | canonical (primary) | alt |
|---|---|---|
| (a) X-COP, 35 points: PASS iff \|mean Δ\| ≤ 0.05 and rms ≤ 0.10 | mean **−0.002**, rms **0.126** → **FAIL (rms)** | mean −0.002, rms 0.126 → FAIL (rms) |
| (b) HG2: PASS iff the picture's D lies in the measured 95% [−0.511, −0.076] | D_pred **+0.229** → **FAIL (ABOVE)** | +0.201 → FAIL (ABOVE) |
| **lane** | **CL2 PICTURE FAILS** (X-COP, HG2) | **CL2 PICTURE FAILS** (X-COP, HG2) |

The footings agree.

### (a) X-COP

With no hydrostatic mass used anywhere in the prediction, the native fair-share budget gets the **average** pull inside
0.7 R500 right: mean Δ is −0.002 dex. Per cluster, the means run from −0.056 to +0.094.

The **shape** is wrong. Δ by radius:

| radius | Δ (dex) |
|---|---|
| 0.1 R500 | +0.19 |
| 0.2 R500 | +0.03 |
| 0.3 R500 | −0.03 |
| 0.5 R500 | −0.08 |
| 0.7 R500 | −0.12 |

So the picture gives too little pull in the cores and too much towards R500:
- At R500, the predicted halo mass alone is 1.27–1.47 × M_HSE in 6 of the 7 clusters (ZW1215: 0.97).
- The Burkert cores at Σ ≈ 630–770 M☉ pc⁻², with r₀ ≈ 290–410 kpc, are too flat in the centre.

The outer excess is the same size as a typical hydrostatic mass bias (10–30%). That is **not** tested here, and it is not
claimed as an explanation. The inner deficit is not addressed by it at all.

**Context.** CS2's HSE-normalised comparators:
- OS1: rms 0.124 on canonical, also a FAIL; 0.092 on alt, a PASS;
- the CS2 law: rms 0.205.

The CL2 picture is the first with no mass normalisation, and it lands at rms 0.126.

### (b) HG2 hot-gas groups

- **Measured.** At matched σ, X-bright groups sit 0.29 dex **below** X-faint groups against the blue-lens reference.
- **Predicted.** The picture predicts +0.23: the opposite sign, and outside the interval.
- **Mechanism.**
  - Counting the eRASS1 gas mass in M_b,tot puts **all 14 X-bright groups above the switch** (halo, route E).
  - Only 30% of the X-faint groups are above it. The rest get the law on baryons.
  - So at fixed σ the picture gives the bright arm extra pull that the data do not show.
- **Reported variant.** With M★ only in M_b,tot, 71% of the bright groups are still above the switch, and D_pred = +0.03.
  That is still above the interval's upper end, −0.076.
- **Reported only.** HG2's statistic on the residual against the picture: D_res = −0.53 [−0.74, −0.38]. HG2's power rule
  (0.448) makes that UNDERPOWERED, as disclosed before the run. The per-arm median residuals are +0.30 (BRIGHT) and +0.30
  (FAINT) on canonical: both arms sit 0.3 dex above the picture's pull at HG1's radius.

## Reading

- On X-COP, the picture's cluster budget is right on average but wrong in shape: the cores are too shallow and the
  outskirts too heavy.
- On groups, a mass switch that counts hot gas sends X-bright groups the wrong way. Within this framework's own picture, a
  detected hot atmosphere at fixed σ should not come with a halo that the X-faint groups lack.
- Both are new failures for the frozen CL2 picture, outside the data it was tuned on. They are information, not a closed
  door: the switch criterion and the core profile are the named suspects.

## Checks: 9/9 normal run

| check | result |
|---|---|
| K4 | c_f table |
| S0-CL2, S0-CS2, S0-HG2 | all reproduced exactly |
| K5 | X-COP rows equal the matched-clumping targets |
| K1 | switch: 0 branch violations |
| K2 | budget start independence 3.9e-8 (A1) |
| K3 | halo mass identities |
| K6 | 0.69 GB, one thread |

**Rerun.** The second normal run gives a byte-identical results JSON.

**MUTATE** (`HO1_MUTATE=1`, CL2's flag and shape inverted, HG2 target × 1.01): S0-CL2, K1 and S0-HG2 all fail (4228
branch violations). The teeth bite; exit 1.

`ho1_k2_diagnostic.py` (post-run, not graded) shows the first-run K2 miss was a check artefact. Shifting the budget by its
size moves the X-COP grade by ≤ 1e-4 dex.

## Files and run

- `ho1_heldout.py`
- `ho1_heldout.out`, `ho1_heldout_results.json`, and their `_MUTATE` twins
- `x62_x43copy_on_shpS9_L4_T12.3_B*`: the CL2 reproduction
- `ho1_k2_diagnostic.*`
- the `x62_x30_machinery.log` is local only

Run (about 2 min each, one thread, 0.69 GB):

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 ho1_heldout.py               # exit 0, 9/9
    HO1_MUTATE=1 PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 ho1_heldout.py  # exit 1 = teeth bite
