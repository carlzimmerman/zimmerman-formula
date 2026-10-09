# CFG525: the KiDS alt-footing miss of the census edge. Verdict DATA-ISSUE (isolation selection): with strict isolation (f30) the census edge passes on both footings; the miss is carried by the less-isolated lenses. No derived mechanism rescues it, and a fixed physical environment fails the census edge on BOTH footings

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (7f99a4371).
- **Scripts (all exit 0; 7/7 load-bearing checks pass in MUTATE, 5/5 in the main run):**
  - `cfg525_tables.py` builds the per-group node tables. It takes about 1 h with 4 workers and writes to `_external_data/cfg525_work/`, which is not committed.
  - `cfg525_neighbours.py` sums the neighbour baryons inside each lens's turnaround sphere.
  - `cfg525_score.py` scores every row and applies the frozen verdict.
- **MUTATE:** `CFG525_MUTATE=1` writes the `*_MUTATE.*` files. All teeth are detected.
- **Settings:** κ = ½ is FITTED. The footings 9.3603e-11 and 1.1312e-10 are never pooled, and a0 is flat. The data are on disk; nothing was downloaded. The cold energy's MASS is still required (no particle). This is not "theory closed", and nothing here says the data favour the framework.
- **Numbers** below come from `cfg525_score_results.json` and `cfg525_neighbours_results.json`. Pairs are canonical / alt.
- **Statistic:** Δ is the χ² of a row minus the χ² of the best sharp edge at x·r_ta (node x ≥ 0.2), in the same harness, sample and footing. A row passes if Δ ≤ 4.

## The miss, reproduced (K1)
- The census edge in H1 (CFG413's free R^-0.8 two-halo term, 15 bins) gives χ² 12.145 / 18.613.
  - Against CFG413's grid best: **+3.20 / +8.84**.
  - Against this lane's finer node grid (alt best at x = 0.55): +3.20 / +8.97.
- The lens-weighted census edge sits at x = 0.343 / 0.297 of r_ta.

## 1. Data / assumption re-check

| item | result (Δ_H1 canonical / alt) | outcome |
|---|---|---|
| D1 stellar-mass scale, edge only (−0.15 … +0.15 dex) | −0.10: +4.77 / +10.77; +0.10: +2.27 / +7.38; +0.15: +2.01 / +6.83 | no. The edge scales only weakly with mass (x ∝ M^½/r_ta) |
| D2 cold gas, edge only | stars only +4.56 / +10.61; f_cold × 2 +2.30 / +7.46 | no |
| D3 f_ret input | see below | CONFLICTED |
| D4 measured leaked fraction 0.2234 (H3 = CFG503 environment rescaled as in CFG520) | census **+19.45 / +20.50**; inner 9 +2.10 / +1.98 | fails on both footings (see note) |
| D5 two-halo treatment | H2 (trusted 9 bins) +1.03 / +1.03; H4 (E shape, free amplitude) +13.47 / +18.47 | trusted bins cannot place the edge |
| D6 lens redshift | no lens has r_edge ≥ r_ta (0 / 0), and r_edge does not depend on z_l | lens-z errors cannot move the model |
| **D7 isolation: f30 (W = 30 Mpc, 57,265 lenses)** | **−0.24 / +1.00** | **passes on both footings: DATA-ISSUE** |

**D3, the f_ret input.**
- Provenance: CFG416's 0.10 floor is a declared step taken from the cosmic mean in Shull+12 (recalled, PROVISIONAL). It is not a per-object measurement at log M* ≈ 10.6.
- Phase matching: the KiDS M_b is stars plus cold gas, which corresponds to the census "galaxies only" value of 0.07 ± 0.02. At f_ret = 0.07, H1 gives +1.17 / +2.61, a pass on both footings.
- But the Local Group pair has the same baryon definition. On CFG522's committed full statistic it needs a common f_ret of at least about 0.11: z_full,LMC is +4.30 at 0.10, +6.45 at 0.08, and about +7.5 at 0.07 (extrapolated).
- So by the frozen rule D3 is CONFLICTED and cannot carry the verdict.

## 2. Mechanisms (derived, no knob)

**M-i: shared catchments (CFG522's rule).** The census is applied once per catchment, and supply is split by each object's own baryons.
- Derived before scoring: fret_census never decreases with mass. So sharing can only move the edge inward. It cannot rescue KiDS.
- **Photometric neighbours.** Inside the lens turnaround spheres, raw neighbour baryons come to only **0.0044 / 0.0047 M_lens**. At positions displaced by 1° (T3) the same sum is 0.230 / 0.252.
  - The isolation cut has already emptied those spheres, to about 2% of a random sightline.
  - The effect is nil: the upper variant gives +3.22 / +8.95.
- **Leaked satellites** (22.34% of the weight, minimal host): +3.41 / +9.31, worse as derived. The M-i row is therefore +3.41 / +9.31, a FAIL.
- **Forbidden double-counted supply (reported only):** +1.59 / +6.14. It moves toward a pass, still fails alt, and is excluded by derivation.

**M-ii: level or shape?** A uniform multiplier s on the census edge, scored in H1.
- Alt: s_best 2.0 (parabola 2.03). The minimum over s is only +0.28 above best-x, and s = 1 fails. So **alt has a LEVEL (placement) problem, not a shape problem.**
- Canonical: s_best 1.34, +0.76; s = 1 already passes.
- The derived footing ratio of the census edge is x_alt/x_can = (a0_can/a0_alt)^½ · r_ta,can/r_ta,alt = 0.910 × 0.954 = **0.868**. Alt's edge sits further in.
  - The H1 data, through the free template, want the reverse: placed edges alt/can = **1.31**.
  - The census rule fixes the total settled mass, the same on both footings, at 5.364 M_b/f_ret. Alt packs that mass inside a smaller radius.

**M-iii.**
- Partial settling is not derivable here; it is a scope limit.
- Mass scatter is covered by D1.
- Stripping is carried by H3.
- No other derived mechanism was found.

**Post hoc (no verdict weight).** The largest constant f_ret with Δ_H1 ≤ 4 is **0.108 for canonical and 0.078 for alt**. In H3 both footings would need f_ret of about 0.05 (−2.09 / −0.89 there).

## Verdict (frozen order): **DATA-ISSUE**, carried by D7 (f30 isolation)
- The M-i row fails.
- Among the data items, only D7 passes on both footings.
- The NOT-DIAGNOSTIC test is not met: alt H2 is +1.03, but H3's range over x is 32.7.
- Alt census strength: H1 3.0σ; H3 4.5σ.

### How solid the f30 pass is (post hoc, written after the verdict was seen)
- **f30 still discriminates.** Its node χ² spans 25.7 / 27.3 over x = 0.2–1, and its best x is 0.40 on both footings (stack P: 0.50 / 0.55). f_ret = 1 fails f30 by +53 / +62.
- **The pass is robust to dropping bins.** Drop-one-bin gives −0.43..+0.35 / +0.03..+1.97 on f30, against +2.33..+4.42 / +7.24..+10.68 on stack P.
- **f30 brackets the census.** Across f_ret = 0.07–0.12, f30 passes on both footings. At 0.05 it fails (+15.1 / +10.9); at 0.14 it fails on alt (+4.63).
- **The complement carries the miss.** The 124,212 stack-P lenses that fail f30 want x = 0.90, and the census fails there by **+22.0 / +31.4**.
  - The preference for a far-out edge, and so the alt miss, comes from the less-isolated lenses.
  - CFG519 measured more leaked satellites in W10 (0.223) than in f30 (0.169).
- **Plain reading.** The census edge fits the cleanest isolated lenses on both footings. The H1 miss is an environment-contamination effect that the free R^-0.8 template absorbs differently on the two footings.

### What does NOT go away
- **H3**, CFG503's fixed environment with the measured 0.2234 and no free amplitude, fails the census edge on **both** footings (+19.4 / +20.5), with a best x of 0.70.
- So the canonical H1 pass is itself template-dependent.
- H3's own best sharp edge fits poorly in absolute terms (χ² 63 / 45 for 15 bins, against LCDM's 26.1). CFG503's environment was built from ΛCDM halos, and G3 was not re-scored. That the census edge fails a ΛCDM-built environment is reported, not adjudicated.
- An f30 environment (W30 E and stripping) was not built. It is the obvious follow-up.

## Controls and MUTATE
- **Controls, all PASS:**
  - K1: CFG515 a1 reproduced to 0.00000, and a2 inner-9 to 0.00000.
  - K2: interpolated vs direct census, |d| 0.035.
  - K2b: the tabulated fret_census, |d| 1e-9.
  - K3: CFG413 x = 0.5 / 1.0 and f30 x = 0.3 reproduced to 0.00000.
  - K4: CFG520's scaled LCDM χ² 26.1342 reproduced exactly.
  - K5: every lens found in the rebuilt pool at zero separation.
- **MUTATE, all detected:**
  - T1: f_ret = 1 gives +60.48 / +70.57 and reproduces CFG515's M1.
  - T2: f_ret = 0.01 gives +15.56 / +13.67.
  - T3: at displaced positions the excess is −0.0018 ± 0.0022 / −0.0027 ± 0.0024, consistent with zero.

## Dated disclosures (2026-10-09)
- **K2b** (checking the fret_census table) was added beyond the frozen controls.
- **Rows below the node range.** Three rows (D2 stars-only, and the low-x tails) had lens weight ≤ 0.0005 below the node range. These were computed directly per group at the group's weight-mean x; group members share M_gal to 0.01 dex.
- **Biased M-i(a) background.** The frozen annulus (2.5–3.5 Mpc) straddles the 3-Mpc isolation radius. So it contains massive neighbours that the isolation removed from the inner region, and the primary background-subtracted excess comes out negative (−0.145 / −0.159 M_lens).
  - That number is an artefact, clipped to zero, so the primary M-i(a) row equals the census.
  - The raw per-lens sum (the frozen upper variant) is the meaningful bound. The conclusion follows from the derived monotonicity regardless.
- **Fine grid.** The finer node grid finds alt's H1 best at x = 0.55 (9.641) rather than CFG413's 0.50 (9.770). The verdict statistic uses the fine-grid best; the CFG515 comparison is also reported.
- **Post-hoc section.** The f30 node ranges, f30 f_ret rows, drop-one-bin results and complement row were written after the verdict was seen. They carry no verdict weight.
- **f_ret 0.04 row.** It passes alt (+3.57) but fails canonical (+9.04).

## Run
```
nice -n 10 python3 cfg525_tables.py          # ~1 h, 4 workers
nice -n 10 python3 cfg525_neighbours.py ; CFG525_MUTATE=1 nice -n 10 python3 cfg525_neighbours.py
nice -n 10 python3 cfg525_score.py ;      CFG525_MUTATE=1 nice -n 10 python3 cfg525_score.py
```
The inputs are read-only:
- `real_research/data/lensing_rar` (the stack-P lenses, the per-lens weights, the jackknife patches, the f30 flags and the KiDS-bright FITS);
- `_external_data/cfg503_work`;
- the committed JSON of CFG377, CFG413, CFG515, CFG520 and CFG522.
