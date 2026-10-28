# DS1_hot_displacement: a hot atmosphere displacing the halo does NOT fix the group sign (both footings)

Criteria: `FROZEN_CRITERIA.md` (456bf76c7c, committed alone, before any script or number); no amendment.
Machinery: HO1's committed script (91cc5c3bd4), executed read-only up to its grade block.

κ = ½ FITTED. Footings never pooled. Cold dark energy is a gravitating w ≈ 0 field component, not matter and not a
particle. Not "theory closed". Nothing here says the data favour the framework.

## Verdict (frozen)

| | canonical (primary) | alt |
|---|---|---|
| **PRIMARY** (X-ray-bright groups on the law, hot gas counted) | **HOT DISPLACEMENT FAILS**: HG2 D_pred **+0.187**, ABOVE [−0.511, −0.076] | **FAILS**: D_pred +0.198, ABOVE |
| base picture (HO1(b), Step 0) | D_pred +0.229 | +0.201 |
| **UNIVERSAL** (clusters on the law too) | **DISPLACEMENT NEEDS A SCOPE**: 6 cluster cells fail; median pred/meas 0.26 | 10 cells fail; 0.22 |

The cluster numbers are CL2's committed law-only run (`x62_x43copy_law_a2`).

**The base lines (C)** are untouched by the PRIMARY scope, so BS1's committed grade stands. The BS1 rerun identity is
recorded below.

## The finding

**Even with every group on the law, the sign is wrong:**
- D_pred is +0.137 (canonical) / +0.136 (alt).
- Arm medians of prediction minus reference: BRIGHT +0.075, FAINT −0.089 (canonical).

So **no rule of the form g_pred = F(g_bar) can give HG2's negative D.** That covers the law, a halo, or a halo
displaced. Once the eRASS1 hot gas is counted, the BRIGHT groups sit at high g_bar, where any such rule predicts *more*
pull than the reference. The data show *less*.

The sign therefore says one of two things:
- (i) at fixed σ, X-ray-bright groups pull **less than the law on their counted baryons**, which no extra-mass mechanism
  can produce; or
- (ii) the counted hot gas is too high, or the σ-based g_obs too low, for the BRIGHT groups.

HG2's own caveat already flagged (ii): gas-to-star ratios of 8–14 in the σ 80–160 km/s bins are high for groups, and a
cluster-calibrated eRASS1 Mgas500 or the β-model may overstate group gas.

**Reading.** HG2's sign is a constraint on the *data model* (the group hot-gas masses) before it is a constraint on
the mechanism. The next step is a gas-mass audit of the 14 BRIGHT groups, not another halo rule. That reading is stated
here, not graded.

## Checks: 5/5

- **K0 (both footings):** the base D_pred reproduces HO1(b), +0.2293 / +0.2011.
- **K1 (both footings):** BRIGHT is the law on baryons and FAINT is the base branch, to 1e-12.
- **K2:** peak RSS 0.67 GB, one thread.
- **Rerun:** the results JSON is byte-identical (sha256 `2bb58bf5…5868`).
- **MUTATE twin** (`DS1_MUTATE=1`, BRIGHT/FAINT swapped in the branch): K1 fails on both footings, checks 3/5, exit 1.

**K0's other clause** (the all-law D against HG2's −0.059) is reported, not reproduced. HG2's −0.059 is a *measured* D
with the BRIGHT gas removed from g_bar. The all-law value here is a *predicted* D, so the two are different quantities.
This is stated as the criteria allow.

## Disclosed

- The UNIVERSAL cluster grade reads CL2's committed law-only run. It was not recomputed with the GS1 measured-gas
  baryons, so it is reported as a bound: the law alone gives a quarter of the cluster lensing.
- `x62_*` files are machinery outputs of the read-only CL2 namespace, written into this folder.
