# CFG486: CFG352's caustic edge re-scored with a free two-halo amplitude. REVIVED on the frozen rule, but stack-dependent, and the revival needs an implausibly large "two-halo" term

**This lane qualifies CFG352. CFG352 is not edited.** CFG352's KiDS kill of the second-caustic edge (+169 / +163) was scored with the two-halo amplitude fixed at zero. It should no longer be quoted as a clean kill. The revival found here should not be quoted as a pass either: it holds only with CFG377's free R^-0.8 template.

Criteria: `FROZEN_CRITERIA.md`, committed alone first (02ef5356e). Script: `cfg486_rescore.py`, about 70 s on one thread at nice 15. On-disk data only; no downloads.

## Bottom line
- **By the frozen rule the edge is REVIVED.** On CFG413's floor (CFG377 primary stack, free R^-0.8 two-halo amplitude), the edge at 0.232 r_ta fits *better* than the law out to r_ta: Δχ² −7.76 (canonical) / −1.12 (alt). The fitted A is 1.57 / 1.43, inside CFG413's range × 1.5.
- **It is stack-dependent, which the frozen rule makes the headline.** Freeing the two-halo amplitude on CFG352's own scorer (FP1/L355, Brouwer+21 Fig-3, 4 mass bins) cuts the penalty from +178 to +56 / +54. The edge is still killed there. The two heaviest mass bins push A to 2.2–2.3, above the record's bias-like ceiling of 2.
- **The A that stack P needs is too large for a two-halo term** (R6 flag, reported). Compared with linear-theory two-halo lensing, the fitted template implies an effective bias of 2.0–2.2 at 2.2 Mpc, rising to 10–11 at 0.6 Mpc. At 1 Mpc it carries 72% / 67% of the model.
- **POST-HOC (not frozen):** on the same stack P, with a free amplitude on the *linear* two-halo shape instead of R^-0.8, the edge is killed again: +22.0 / +15.0, with bias ≈ 3.
- **What this means:**
  - CFG413 said the +169 "follows from the missing two-halo term, not from the data". That is only partly right. The missing amplitude explains about two-thirds of the penalty on CFG352's scorer (+178 → +56).
  - Whether the rest goes away depends entirely on the shape assumed for the two-halo term, and neither stack fixes that shape.
  - The edge's status is **template-dependent, not settled**. Settling it needs a two-halo model for isolated lenses fixed independently of these fits, for example from mocks with the isolation cut. CFG413 already named this need.

## χ² tables (both footings, never pooled)

**Stack P: CFG413's floor, the verdict stack.** 181,477 lenses; 15 g_bar bins; 50-patch jackknife; Hartlap 0.6735. Two-halo amplitude free.

| x (r_on / r_ta) | χ² can | A can | χ² alt | A alt | Δχ² vs x = 1 (can / alt) |
|---|---|---|---|---|---|
| 0.232 (edge) | 16.74 | 1.568 | 22.33 | 1.432 | **−7.76 / −1.12** |
| 0.359 (first caustic) | 10.84 | 1.388 | 13.62 | 1.241 | −13.66 / −9.82 |
| 1.0 (law to r_ta) | 24.50 | 1.120 | 23.45 | 0.953 | 0 |
| 0.232, A = 0 | 441.78 | 0 | 376.96 | 0 | +200.5 / +196.5 |

- **A range (frozen):** CFG413 found 1.12–1.57 (canonical) and 0.95–1.44 (alt). × 1.5 gives [0.75, 2.36] and [0.64, 2.16]. Both fits on both footings are inside.
- **R1, the 9 bins Brouwer+21 trust (R ≤ 0.3/h = 0.445 Mpc; Hartlap 0.7959):**
  - Edge vs x = 1: χ² 5.735 vs 6.563 (canonical) and 6.463 vs 7.552 (alt), so Δχ² −0.83 / −1.09. A is 1.27 / 1.05.
  - Even with A = 0 the edge is not penalised there: −6.9 / −8.2.
  - The trusted bins cannot tell the edge from the law to r_ta. All the discriminating power sits in the 6 outer bins (0.59–2.17 Mpc).
- **R3, drop-one-bin, Δχ²_edge:**
  - Canonical: −9.44 to +3.91 (no drop exceeds 4).
  - Alt: −2.75 to **+8.28**. Two drops exceed 4; the worst removes the 1.82 Mpc bin.
  - So the alt-footing revival is fragile.
- **R5, CFG352's own r_ta definition on stack P** (`r_bound`, z_l = 0.25; its median is 2.8% larger than `r_ta_law`): Δχ²_edge −10.17 / −3.76. Same outcome.

**Stack F: CFG352's own scorer** (FP1/L355; Brouwer+21 Fig-3; 4 mass bins × 15 radii; published covariance; linear two-halo shape, A ≥ 0 per mass bin).

| Amax | law χ² | x = 1.0 | x = 0.359 | x = 0.232 | Δχ²_edge (0.232 vs 1.0) | A per mass bin at 0.232 |
|---|---|---|---|---|---|---|
| 0 (CFG352) | 162.61 / 154.76 | 153.43 / 145.46 | 231.41 / 220.08 | 331.89 / 318.22 | **+178.46 / +172.76** | 0 |
| 2 (L355 ceiling) | 159.60 / 152.32 | 149.32 / 142.88 | 159.33 / 151.80 | 206.28 / 199.52 | +56.95 / +56.63 | [0.82, 1.09, 2.0, 2.0] / [0.83, 1.12, 2.0, 2.0] |
| ∞ (free) | 159.60 / 152.32 | 149.32 / 142.88 | 159.33 / 151.80 | 205.38 / 196.87 | **+56.06 / +53.99** | [0.82, 1.09, 2.28, 2.22] / [0.83, 1.12, 2.32, 2.27] |

- With Amax = 0, the edge row against the untruncated law is CFG352's committed +169.28 / +163.46.
- At x = 1.0, the free fit needs almost no two-halo term: A per mass bin is [0.09, 0, 0.5, 0.16] (canonical) and [0.03, 0, 0.58, 0] (alt).
- The first caustic with A free sits +10.0 / +8.9 above x = 1 on this stack.

**R6 (reported): the effective bias b_eff = A · template / linear two-halo ESD**, using FP1's linear-theory two-halo (bias 1, z_l = 0.25), stacked identically.
- **Edge fit:** 2.19 / 2.00 at 2.17 Mpc, 3.7 / 3.4 at 1.38 Mpc, 11.1 / 10.1 at 0.59 Mpc.
- **x = 1 fit:** 1.56 / 1.33 at 2.17 Mpc, 7.9 / 6.7 at 0.59 Mpc.
- **Flagged:** b_eff > 2 in every outer bin of the edge fit.
- **Caveat:** one lens redshift, and linear theory. Non-linear clustering raises the true two-halo term at R < 1 Mpc, so the inner-bin values overstate the excess. The 1.4–2.2 Mpc bins are the cleanest comparison.

**POST-HOC PH2 (not in the frozen criteria): stack P with the linear two-halo shape** (bias free):
- χ² is 207.2 at x = 0.232 (b 2.99) and 185.2 at x = 1 (b 1.46), canonical; 156.9 (b 2.90) and 141.9 (b 1.21), alt.
- Δχ²_edge is **+22.0 / +15.0, STILL KILLED**. The first caustic gives −14.7 / −18.5. The trusted 9 bins give −4.4 / −3.2.
- Both χ² levels are poor: the outer KiDS signal is better described by R^-0.8 than by linear theory.

## Controls
- **C1 PASS: CFG352 reproduced.** Stack F with Amax = 0 matches CFG352's law χ² and its row Δχ² (1.0, 0.359, 0.232) to 2e-5. The MUTATE run also matches the 0.05 row.
- **C2 PASS: CFG413 reproduced.** Stack P matches CFG413's committed x = 0.23 and x = 1.0 χ², free and A = 0, to 1e-5.
- **C3 PASS:** 181,477 lenses and 15 bins.
- **R1 setup PASS:** 9 trusted bins.
- **R6 setup FAIL, kept.** The script exits rc 1 because of it.
  - The linear two-halo ESD rebuilt on a wide grid differs from FP1's ESD2h by 3.1% at 0.049 Mpc, against a 2% tolerance.
  - The cause, diagnosed post-hoc (PH1): FP1 starts its Σ integral at 0.02 Mpc with a constant-Σ core. With the same inner edge the two agree to 2.4e-4. At R ≥ 0.445 Mpc, where the flag is decided, they agree to 6.5e-5.
  - The tolerance and range were mis-specified. The flag does not change.
- **MUTATE (`CFG486_MUTATE=1`): DETECTED.** An edge at 0.05 r_ta on stack P with free A gives Δχ² +39.77 / +51.14 (A 2.24 / 2.18), STILL KILLED. This reproduces CFG413's MUTATE.

## Standing rules
- κ = ½ is fitted.
- The footings 9.3603e-11 and 1.1312e-10 are scored separately.
- The cold mass is still required, and no particle species is added.
- This is not an a0 measurement, and nothing here says the data favour the framework.

## Run
```
nice -n 15 python3 campaign_fresh_gravity/CFG486_caustic_edge_rescore/cfg486_rescore.py                    # rc 1 (R6 setup check FAIL, kept)
CFG486_MUTATE=1 nice -n 15 python3 campaign_fresh_gravity/CFG486_caustic_edge_rescore/cfg486_rescore.py    # MUTATE DETECTED
```
Inputs (read-only):
- `real_research/data/lensing_rar/`: CFG377's per-lens files and the Brouwer+21 Fig-3 tables;
- FP1's KiDS slice;
- `cfg100_lib`;
- the committed CFG352, CFG413 and CFG4_switch JSONs.

Outputs: `cfg486_rescore{,_MUTATE}.out` and `cfg486_rescore{,_MUTATE}_results.json`.
