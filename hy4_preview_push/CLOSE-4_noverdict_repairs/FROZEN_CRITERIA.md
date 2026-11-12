# CLOSE-4 FROZEN CRITERIA: repair the gates that produced NO VERDICT instead of a verdict

Committed alone, before any CLOSE-4 script is run and before any CLOSE-4 number exists.

TEST lane. Relabels nothing, adopts nothing, is not registered. **kappa = 1/2 FITTED; not theory closed.**
Footings canonical (a0 = 9.3603e-11 m/s^2) and alt (1.1312e-10 m/s^2) are graded separately and **never pooled**.
Cold dark energy is a gravitating field component of the sector's own stress-energy — never a particle. Dark mass IS that
sector's stress-energy; stated as the claim, no LCDM hedging.

CLOSE-4 does three repairs, in DOORS.md's priority order. Each repair is pre-registered here **before** the rerun that
reads it. A repair that cannot be completed is recorded as a blocker, never quietly re-labelled.

| # | target | what failed | the repair pre-registered here |
|---|---|---|---|
| 1 | the DES Y3 covariance guard (KL1, KL1R, BX1) | MUTATE MA2 cannot bite on DES Y3 | R1: freeze the KA2 selection sets at the unmutated configuration |
| 2 | DCN1 M3's numerical half (2.1 % against a 5 % line) | the 5 % line is unattainable on the KA4 sphere | R2: a detection test + the absolute line on a u >= 1 testbed |
| 3 | SCS2 / SCS3 / EFN1 (external-field family) | three different convergence clauses, none decisive | R3: ONE rule, RULE-GC, applied to all three |

---

## R1. The DES Y3 covariance guard (KL1, KL1R; inherited by BX1)

### The exact guard, located

- KL1 `FROZEN_CRITERIA.md` (99a42c78ef) section 3, **KA2**: over the published-kept points, with
  `nfrac = diag(N) / diag(G)` (N the shape-noise term, G my Gaussian covariance at the fitted area):
  - (i) on points with `nfrac >= 0.8`, the 16th-to-84th percentile range of `published / mine` lies in [0.85, 1.15];
  - (ii) on points with `nfrac < 0.5`, the median of `published / mine` lies in [0.95, 1.6] and no point is below 0.80;
  - *"If (i) or (ii) has fewer than 5 points it reads NOT EVALUABLE."*
- KL1 section 5, **MA2**: *"KA2 rerun with every n_i halved must FAIL (ii)."*
- KL1 `kl1.py` line 202 (the bite): `bites = bool(k["ii_pass"] is False)`. `ka2()` sets `ii_pass = None` when
  `n_signal < 5` (kl1.py line 65). `None is False` is false, so **NOT EVALUABLE is scored as "does not bite".**

### Why it cannot bite

`n_i` is the *only* thing MA2 changes, and `nfrac` is the *only* thing that defines the (ii) point set. Halving every
`n_i` doubles `N^ij = s_i^2 / n_i`, so `nfrac` rises on every point and points migrate **out of** the (ii) set
(`nfrac < 0.5`) into the (i) set. The mutation therefore destroys the population it is supposed to be measured on.
On DES Y3 the (ii) set collapses from 39 points (unmutated) to 3; 3 < 5, the criteria's own escape clause fires,
`ii_pass` becomes `None`, and the arm cannot fail and so cannot bite. On KiDS-1000 the same halving leaves 15 points,
so the arm bites there. **The guard is a selection artefact of the mutation, not a statement about the covariance.**

### The repair (R1, pre-registered)

**The mutation may change the covariance; it may not change the points on which the tests are evaluated.**

1. Per survey, per footing, at KA2's own configuration (published `n_i`, KA2's fitted area `A_KA2`), compute once:
   - `S_i  = {p : nfrac_p >= 0.8}` (the (i) / noise-dominated set),
   - `S_ii = {p : nfrac_p < 0.5}` (the (ii) / signal-dominated set).
   These two index sets are then **held fixed** for every mutated run of that survey and footing.
2. Mutated run (`ng_scale = 0.5`, i.e. every `n_i` halved): recompute `G'` with `n_i / 2`; refit the area `A'` by the
   frozen rule — the median of `published / G'` over **`S_i`** is 1 (same rule, fixed set, no re-selection);
   then evaluate the (ii) statistic on **`S_ii`**: the median and the minimum of `published / (G' / A')`.
3. **Bite:** the (ii) test must FAIL, i.e. `median not in [0.95, 1.6]` OR `min < 0.80`. `S_ii` is non-empty by
   construction (39 points for DES Y3, 38 for KiDS-1000), so the `n_signal >= 5` escape **cannot** fire and the arm
   is evaluable on both surveys.
4. **Control (must reproduce KA2):** the same machinery run at `ng_scale = 1.0` with the same fixed sets must return
   KA2's own `i_pass = True` and `ii_pass = True`. This is the KA2-reproduction check; if it fails, R1 is void.
5. Reported beside it, unchanged: the re-selected (frozen, point-set-migrating) version, so the record keeps both.

**Scope.** R1 changes the point set only. It changes no physics, no covariance formula, no area rule, no threshold.
It is a post hoc amendment to KL1 and KL1R (the frozen reading is seen) and is labelled as such. BX1 inherits it
through KL1's A2 covariance; BX1's own frozen NO VERDICT does **not** rest on this guard (it rests on its own KA3 and
MB2, both 256^3 simulation gates), so R1 does not by itself move BX1's frozen label. That is recorded, not hidden.

---

## R2. DCN1's M3 numerical half

### The exact clause and why the line is unattainable

- DCN1 `FROZEN_CRITERIA.md` (d603f1703c) section 5, **M3**: *"drop the 1/(1+u) in A1: the sympy check must fail, and
  Gamma_id^2 must disagree with route L on the KA4 sphere by more than 5 %."*
- The mutation replaces `u Phi_nn/(1+u)` by `u Phi_nn`. The relative change it can produce is
  `(2+u) u Phi_nn * [u/(1+u)] / Gamma_id^2`, i.e. it is **capped by `u_max/(1 + u_max)` over the analysis region**.
- On the KA4 sphere the annulus has `u_max = 0.101` (DCN1's stored `u_max_annulus`). The cap is therefore
  `0.101 / 1.101 = 0.0917` of the `u Phi_nn` share of `Gamma_id^2` — and the realised value is 2.13 % against the
  identity's own 0.036 % agreement with route L. **The 5 % line demands more than the testbed's own `u` allows.** It is
  a mis-scaled line, not a failing pipeline: the same run shows the unmutated identity agrees with route L to
  0.036 %, so the mutation is detected at 59x the pipeline's self-error.

### The repair (R2, pre-registered)

**A mutation arm's job is to show the graded number is sensitive to the thing it claims to test. State the line against
what the mutation can produce, and against the pipeline's own error.**

- **R2-a (detection, graded).** On the KA4 sphere analysis annulus (N_R = 108, DCN1's geometry, `rho_0` and `L` of the
  canonical 9.4 thick disc, canonical footing), with `GL` = route L, `Gid` = the A1 identity, `Gmut` = the identity with
  the `1/(1+u)` dropped (all with DCN1's own finite-difference Hessians):
  - `d0 = max_ann |Gid/GL - 1|` (the identity's own agreement with route L),
  - `d1 = max_ann |Gmut/GL - 1|` (the mutated identity's disagreement),
  - `dp = max_ann |Gmut - Gid| / |GL|` (the change the algebra predicts).
  - **BITES iff `d1 >= 10 d0` AND `0.5 dp <= d1 <= 2 dp`.** That is: the mutation moves the number by at least ten
    times the identity's own discretisation error, and by the size the algebra predicts, within a factor of two.
- **R2-b (absolute line on a testbed where it is attainable, graded).** Repeat the same comparison on the KA4 uniform
  sphere with `rho_0` scaled by the first factor in the pre-registered ladder **{1, 3, 10, 30, 100, 300}** for which
  `sup_annulus(u) >= 1.0`. On that testbed the frozen 5 % line is attainable (dropping `1/(1+u)` multiplies the
  `u Phi_nn` term by `1 + u >= 2`), and **M3's numerical half BITES iff `d1 > 0.05`** there. The chosen factor, the
  resulting `sup_annulus(u)`, `d0`, `d1`, `dp` are all reported.
- The sympy half (already biting, cubics 1.6 relative) and M1, M2, M4 are untouched.
- **The frozen 5 % line is not deleted; it is relocated to a testbed where it can be met.** R2-a is the replacement
  line on DCN1's own KA4 sphere; R2-b is the frozen line on a u-O(1) sphere. Both are graded.

**What R2 does and does not do.** R2 repairs a MUTATE arm. A MUTATE arm that does not bite makes the rows it guards
NO VERDICT; M3 guards the A1 identity's numerical use. R2 does not touch KA3, KA4 or KA5, which are the known answers
that carry DCN1's frozen NO VERDICT. **DCN1's lane label does not move under R2.** That is recorded, not hidden.

---

## R3. ONE grid-convergence rule for SCS2 / SCS3 / EFN1

### The rule (RULE-GC), adopted unchanged — not invented here

Taken verbatim from **SCS3's A4 rule** (`fable52_push/SCS3_external_field_stability/`, amendment A4 b34295ebcd,
section 3, "flat clause removed") and **DCN1's section 2** (d603f1703c), which adopted the same rule and validated it
in DCN1's KA3 (12 of 12 sequences to 2.4e-15 on `h = 1/N_R`; `h^-1` and `h^-0.5` Diverging; `1 + h^0.3` not
Converged). CLOSE-4 adds **no** clause to the arithmetic — only the two clauses the three lanes left implicit: the
`n < 3` case and the lane-level combination.

**Input.** A quantity Q measured on a geometric refinement ladder `h_i`, `h_{i+1} = h_i / rho`, `rho = 1.5`
(SCS2, SCS3, EFN1 and DCN1 all use 1.5), `i = 0` coarsest, `n` values.

**Output.** One of `CONVERGED` (with `Q_inf`, `E`, `p`), `DIVERGING`, `NOT CONVERGED`, `NOT EVALUABLE`.

1. **`n < 3` → NOT EVALUABLE.** Two grids cannot separate a slow approach from a divergence. Report the two-grid
   relative change. *(This is SCS2's situation as it landed.)*
2. Finest three `(Qc, Qm, Qf) = (Q_{n-3}, Q_{n-2}, Q_{n-1})`; `d1 = Qm - Qc`, `d2 = Qf - Qm`.
3. **Monotone (`d1 d2 > 0`) and `|d2| < |d1|`:** `p = ln(d1/d2)/ln rho`; `Q_inf = Qf + d2/(rho^p - 1)`;
   `E = 1.25 |d2|/(rho^p - 1)`; if `n >= 4`, `E = max(E, |Q_inf(finest three) - Q_inf(next three)|)`.
4. **Oscillating (`d1 d2 < 0`):** `Q_inf = mean(Qm, Qf)`, `E = max(|d1|, |d2|)`.
5. **`d2 = 0`:** `Q_inf = Qf`, `E = |d1|`.
6. **CONVERGED** iff (p when computed) lies in `[0.5, 6]` **and** `E <= 0.20 |Q_inf|`.
7. **DIVERGING** iff monotone with `|d2| >= |d1|` on the finest three **and**, when `n >= 4`, on the next three.
   When `n = 3` the second check is reported as NOT EVALUABLE and the first alone decides.
8. Otherwise **NOT CONVERGED**.

**Lane-level combination (SCS3's A4 requirement, unchanged):** a family is decided only if **every** background in it
is CONVERGED. Any DIVERGING background makes the family DIVERGING (for a rate: RATE UNBOUNDED). Any NOT CONVERGED
background and no DIVERGING one → the family is NO VERDICT. `n < 3` for the family → NOT EVALUABLE → NO VERDICT.

### Where each lane's ladder comes from

- **SCS2** (`fable52_push/SCS2_static_clock_stability_discs/`): as landed it has **two** resolutions for the axial
  external-field family (R0 = 48x24, R1 = 72x36), so RULE-GC gives NOT EVALUABLE. But **SCS3's AX backgrounds are
  SCS2's exactly** (SCS3 section 1: "Backgrounds are SCS2's exactly", same `scs2_aqual.py`, same solver, same inner
  treatment, same Dirichlet rule), and SCS3's AX files store up to **seven** resolutions (R0-R6) of them. RULE-GC is
  therefore applied to SCS2's two graded KA4 quantities — `frac_neg_over_pos` (the negative-cell charge fraction) and
  `min_dp_offplane` (the minimum G) — on those ladders. This supplies the third resolution SCS2 lacked, from the
  record, with no new physics.

### Correction C1 (recorded after the run, before the ledger was written)

The freeze above said "the seven-point ladder", naming `scs3_maps_AX_A4.json` for both quantities. The run showed that
is wrong for the charge fraction, and the correction is recorded here rather than buried:

- SCS3's **A4 rerun** changed the negative **region**, not the background: on `alt_AX_expo_10.45_0.01` R1 the
  off-plane negative cells go 70 → 110 and `Q_neg_offplane` -1.683e11 → -2.345e11, while `min_dp_offplane` is
  bit-identical.
- Checked against SCS2's own stored `scs2_resolution.json` on all 32 twins: `min_dp_fine`/`min_dp_coarse` match both
  SCS3 files (32/32); **`frac_fine`/`frac_coarse` match only the pre-A4 `scs3_maps_AX.json` (32/32) and the A4 rerun
  (0/32)**.
- Therefore: **SCS2's charge fraction is graded on the pre-A4 ladder (R0-R3); SCS2's minimum G is graded on both the
  pre-A4 ladder (R0-R3) and the A4 ladder (R0-R6).** SCS3's own graded quantities stay on the A4 ladder, which is the
  reading SCS3's A4 amendment grades.
- No clause of RULE-GC changed. Only the file a quantity is read from.

- **SCS3**: the A4 ladder, on SCS3's own graded quantities — route L's `Gamma_L^2`
  (`routeL.L.Gamma2_max_s2`), `Q_neg/Q_pos`, `min_dp_offplane`, the inner radius in `r_e`; route 2's
  `Gamma_2^2 = -lambda_min` from `scs3_route2_AX_A1_R01234_*.json` where it exists.
- **EFN1** (`closure_2026_11_10/EFN1_external_field_nonlinear/`): route D's stop time `tF_efolds` on the
  R2-R3-R4 ladder in `efn1_route_d_main.json` (12 backgrounds) and `efn1_route_d_frozen.json`; route W's `Gamma`,
  `c3`, `c2` from `efn1_route_w.out` / `efn1_route_w_MUTATE.json`.

### What is decided

RULE-GC returns a verdict per quantity per background. CLOSE-4 reports, for each of the three lanes, the count of
backgrounds in each of CONVERGED / DIVERGING / NOT CONVERGED / NOT EVALUABLE and the family-level reading the
combination rule gives. **It does not re-label anything the rule does not decide.** If the rule leaves a family
NO VERDICT, CLOSE-4 says so and names the quantity and the background that blocks it.

---

## 4. What CLOSE-4 may not do

- No new physics, no new simulation, no refit of any lane's model. R3 runs no solver; it reads stored JSON.
- No change to any lane's frozen label that a repaired gate does not itself move. A repaired MUTATE arm that still
  leaves a failed known answer in place leaves the label where it was, and CLOSE-4 says so.
- Footings are never pooled. Every number is reported canonical / alt.
- Nothing here is a verdict on form B.

## 5. Files

- `close4_ma2_fixed.py` → `parts/ma2_fixed.json`, `.out` (R1)
- `close4_m3.py` → `parts/m3_repaired.json`, `.out` (R2)
- `close4_gc.py` → `parts/gc_<lane>.json`, `.out` (R3)
- `NOVERDICT.md` — the ledger of repairs actually executed, written after the runs.
