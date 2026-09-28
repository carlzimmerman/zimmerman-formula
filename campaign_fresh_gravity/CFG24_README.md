# CFG24 — the cold budget with turned-around associations as the top-level systems

Script: `CFG24_budget_associations.py`, about 5 min.
- Outputs: `.out` and `_results.json`.
- MUTATE control: `_MUTATE.out` and `_MUTATE_results.json`. The linking is switched off, and H0 fails (rc = 1).
- The main run exits 1, because H1 failed, as its declared expectation said it would.

κ = ½ is fitted. Both footings are used.

## Question

CFG23's diagnostics (V4) measured the cold budget's edge against KiDS's own best edge (x_e ≈ 0.62). It costs 40.9–62.0 in χ².

The budget's FG001 grouping (CFG11) owned the phantom at the level of Kourkchi & Tully's groups, whose members lie inside the second-turnaround radius. The framework's switch (T3) acts inside systems that have *turned around*, and FG001 gives the phantom to the outermost such system. So the owner is the turned-around association, one level up. CFG12's standing named this as the untested next step. The phantom is sublinear in the baryons, so owning it higher up can only lower the sum.

## Method

Associations are built from KT2017's groups in the D ≤ 15 Mpc sample, by friends-of-friends in redshift space.
- **Link rule:** two systems join when s_proj² + (ΔV/75)² < r_link(M₁ + M₂)².
- **Link radius:** the self-consistent turnaround radius of the combined system at the edge being tested. That is the law's profile cut at x r_ta, evaluated where its mean density falls to Δ_ta(0) ρ_m.
- **No new constant:** nothing is added beyond the framework's own r_ta.
- **The bias is generous to the budget.** Redshift space compresses infalling pairs, and the law's r_ta exceeds the Local Group's observed zero-velocity radius (CFG20). Both push towards more linking.
- **A still more generous variant** links at the law's untruncated r_ta. It is reported.

The budget is CFG17's exact machinery (exec'd read-only), with CFG11's grouping ratio replaced by the associations' R(x). The KiDS cost is CFG23_diagnostics' V4.

**Revision, disclosed** (made after the MUTATE run, before the main run). The D ≤ 15 Mpc sample, which CFG11, CFG12 and CFG17 all use, contains **the Milky Way's own group**:
- KT2017 group 5064336: the MW, the LMC, the SMC and Sgr dSph.
- It sits at a V/75 distance of 0.12 Mpc. There the MW's integrated K magnitude, seen from inside the Galaxy, becomes M_b = 4.4 × 10¹² M☉, which is 47% of the sample's baryons.

The operative sample drops galaxies whose group V/75 distance is below 1 Mpc; that removes exactly those four. The first-written versions of H0 and H1 are still computed and reported, marked as contaminated.

## Results

**Controls pass.**
- CFG17's committed edges are reproduced exactly.
- With the linking off, this lane's R and edge equal CFG17's to 0.
- The tabulated link radius matches the direct computation to 3e-7.
- The finder conserves the sample: every group lands in one association, and baryons are summed exactly.

**The erratum** (the MW group removed, groups level, CFG17's method):

| row | R(0.31) | edge (committed → corrected) | KiDS cost |
|---|---|---|---|
| canonical P2 | 0.889 → 0.870 | 0.3483 → 0.3542 | 40.9 → 38.6 |
| canonical ν_mono | | 0.3458 → 0.3517 | 47.8 → 45.7 |
| alt P2 | | 0.2998 → 0.3049 | 55.4 → 53.7 |
| alt ν_mono | | 0.2976 → 0.3028 | 62.0 → 59.9 |

**The associations** (operative sample, canonical P2):
- At x = 0.35, 305 groups become 228 associations. 40 of them are multi-group, and those hold 59% of the baryons.
- The largest has 13 groups, 47 galaxies and 11% of the sample's baryons.
- R(0.35) falls from 0.870 (groups) to **0.772**. Without the largest association it would be 0.819. The generous variant gives 0.682.
- **H0 passes:** association ownership lowers the phantom sum.

**The budget edge and KiDS's cost against its own best:**

| row | groups | associations | generous |
|---|---|---|---|
| canonical P2 | 0.354 (38.6) | **0.390 (29.4)** | 0.423 (20.8) |
| canonical ν_mono | 0.352 (45.7) | 0.388 (32.9) | 0.420 (25.1) |
| alt P2 | 0.305 (53.7) | 0.336 (45.4) | 0.374 (31.9) |
| alt ν_mono | 0.303 (59.9) | 0.334 (49.3) | 0.373 (35.3) |

**H1 FAILED**, as declared. The cost falls but stays well above 9:
- 29.4 and 32.9 canonical, which is 5.4–5.7σ;
- 20.8–25.1 even with the generous linking, which is 4.6–5.0σ.

## Standing

**Owning the phantom where the framework's own switch says it belongs relieves the budget by about a quarter of the KiDS cost.** It does not close the gap.

The cold budget still cannot pay for the phantom KiDS sees out to about 0.6 r_ta around isolated lenses: 5.4–5.7σ canonical and 6.7–7.0σ alt, with the linear 2-halo caveat of CFG23. The Milky-Way entry is an erratum for CFG11/12/17. It is small and moves every edge up by about 0.006.

Nothing here says the theory is closed.
