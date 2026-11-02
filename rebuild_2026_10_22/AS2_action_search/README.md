# AS2_action_search: EMPTY FOR THIS GRAMMAR. Tier A 0 of 717; 25 reach G6 and all fail it, because a screen and a dust cost more than the frozen budget. With the budget relaxed by one, 15 rows have no FAIL and none is clean

**Method, plainly.** This is enumeration against analytic gates, because an action has no data table to regress on. No data were graded. An empty result holds for this grammar only and isn't a no-go theorem. A row that passes needs a hand derivation, outside review and data grading.

The brief called this AS1; `AS1_outer_slope` holds that id. Criteria `FROZEN_CRITERIA.md` (102c3e16bf, alone first, not blind), `AMENDMENTS.md` A1-A3. kappa = 1/2 FITTED. Footings canonical 9.3603e-11, alt 1.1312e-10 m/s^2, never pooled. No dark matter particle. The cold sector stays retired and nothing here reinstates it. Not theory closed. Nothing here says the data favour the framework. Credit: AeST (Skordis, Zlosnik), Khronon (Blanchet, Skordis), BIMOND, QUMOND (Milgrom), TeVeS (Bekenstein), Einstein-aether (Jacobson, Mattingly; PPN formulas Foster, Jacobson, from memory, PROVISIONAL, and the engine reproduces them).

## Counts
Space: 8668 templates (Tier A 3732, Tier B 4936) x 2,500,000 distinct functions (cap hit at size 9, partway) x 10 coefficients = 2.17e11 (Tier A 9.33e10). Before any function, 2887 templates exit: 1928 source on a flat direction, 942 carrier unsourced, 16 carrier not rank one, 1 mimetic. 67 static forms remain.

Rows are template x distinct law function, after G1. "Not FAIL" counts ND as alive; no row reaches G3 with PASS except the two below.

| Not FAIL through | Tier A | Tier B |
|---|---|---|
| G1 static law | 717 | 915 |
| G2 c_T, gamma | 548 | 690 |
| G3 health | 438 | 466 |
| G4 Q2 | 212 | 267 |
| G4p planets | 43 | 78 |
| G5 preferred frame | 25 | 46 |
| G6 dust, growth | **0** | 43 |
| G7 well-posed | 0 | **15** |
| PASS every gate | **0** | **0** |

Raw G1 passes before merging equal functions: 63,232 Tier A, 76,232 Tier B. **G3 is ND on all 15 and on every Tier A row with fewer than two FAILs:** the frozen analysis finds zero-speed roots and can't fix their sign. G3 PASS occurs in 2 rows, both conformal, both failing gamma at 1.98.

## Why Tier A is empty
It's a budget result, not a physics theorem. Planets need a screen, and every screen in the grammar costs the one extra scale (the law's own tail is 1.1e4-8.1e4 x the bounds). Dust then needs a second scale (K(Q)) or a third field (separate P(X)), and both are over the frozen cap. Tying mu to 1/L stays in budget, but puts the static mass term at about 22 pc, where the record (S4, C1) has it breaking the law; that is an argument, not a run row.

## Closest rows
| Tier | Row | Fails | Numbers |
|---|---|---|---|
| A | KhP + (D.P)^2, no cold term (3 rows) | G6: no dust; G3 ND | alpha_1, alpha_2 0; planets 0.21 of Mars's bound at the L* floor |
| A | SKh + (D.V)^2, no cold term (6 rows) | G6: no dust; G3 ND; G4 [EST] | same |
| A | Bare law on Kh, SKh, SAe, Ae or BIMOND, 20 rows, one FAIL | G4p | up to 8.1e4 x bound |
| B | KhP + (D.P)^2 + K(Q), which is v3 | G6, cap 14.8 vs need 411 h/Mpc [REC M1] | reproduces the record |
| B | KhP + (D.P)^2 + separate dust (3), UX1's K8 | no FAIL; G3 ND | double counts, capture 0.76 vs 0.20 / 0.03 [REC X22] |
| B | SKh + (D.V)^2 + separate dust (6) | no FAIL; G3 ND; G4 [EST] | same double count |
| B | SKh + (D.V)^2 + K(Q) on the scalar (6) | no FAIL; G3, G6 ND; G4 [EST] | see below |

Nearest function off the law at G1: 0.019 dex at worst, f = y/(1/y + sqrt(log(3/2))). It isn't the law.

**So only a separate dust passes G6 with the screen present, and only by relaxing the cap.** I report that as a result. It reinstates nothing, and it carries the v3s double-count objection unchanged.

## The one new corner, and why it isn't a lead yet
A khronon plus a scalar, with (D^2 chi)^2. The vector is untwisted, so the I1 ill-posedness doesn't apply. C1 set it aside because it isn't AQUAL off symmetry; the static form is g = g_N + grad psi, BIMOND's two-field form, with Q2 at 0.03-0.11 of the Hees line even unscreened. That reshapes one trilemma horn: "untwisted fails growth" is a statement about K(Q) on the khronon itself (M1). K(Q) on a separate scalar over the khronon is not on record. I named this corner in the criteria as my expected closest, so this isn't a blind find.

**The independent reduction does not confirm its growth.** `as2_indep.py` shares no code with the engine:
- Agrees: exact static expansion gives g = g_N + h, gamma = 1 and the exact law; tensor wave untouched; no propagating scalar without charge; spherical stiff ODE returns the law at r >> L (0.61801 vs 0.61803) and sits at about half the hedgehog inside L for the Sun's ratio (1.2e-6 vs 2.4e-6, inside its factor-2 tolerance).
- **I3b FAILS.** ADM block with a dust charge n: omega^2 = n^2 (mu^2 - k^2) / [8 mu^2 (F + NF + L^2 k^2 - n) + 4 NF^2 k^2 + ...], order n^2, stable below mu. H1 found Gamma^2(k -> 0) = 4 pi G rho, order n, for AeST. Their scalar sectors should match, since a longitudinal aether is a gradient. I didn't resolve this. My block drops FRW terms by a Jeans swindle (with them kept the order is unchanged) and H1's route differs, so either could be at fault. G6 stays ND. As it stands this row has no shown growth.

Also unexamined for it: FRW background beyond dust at Q -> 1, C7's runaway (attributed there to a vector pair this row lacks, unproven), H4's negative-charge instability, a Q2 solve with stiffness (bound a0/L only), and the L* floor, which comes from D10's AQUAL equation, not this one. Off-spherical differences from AQUAL need data grading.

## G5 finding: two branches
- A slowly moving source excites the zero-speed pair, and Phi falls to the bare Newtonian value, so moving-branch alpha_1 = alpha_2 = 0 in AeST-form rows. This is H5's and O1's velocity screening in the linear solve.
- Dividing by the static potential reproduces the record exactly: alpha_1 = -2(K_B+2) at J_Y = 1 (-4.000000, -5.000000; KA4d, e). So N7 is the static branch at J_Y = 1.
- On the capped law at the Sun, static alpha_1 is about -1e-7 at K_B = 0 and -4 K_B otherwise. So K_B = 1/2 fails G5 and K_B = 0 doesn't: this answers N7's named solar-profile residual for the capped form only. Which branch applies depends on the source speed against that pair's, which frozen analysis doesn't fix. G5 requires both.

## Failed checks and limits
`as2_run` 17/17 at the end, rerun byte-identical; `as2_indep` 8/9 (I3b), rerun identical. MUTATE: engine KAs and KA1 fail, exit 1; `as2_indep` MUTATE fails I1a, I1b, I3b.
- **RUN1 failed 5 known-answer checks** (`as2_run_RUN1.log`), all faults in the checks, fixed after seeing counts (A3). The counts didn't change.
- **A rerun comparison passed falsely once:** a crash left stale outputs, so `cmp` matched old files. I caught it from the unchanged failures, removed outputs before running and repeated.
- **Independent I1b and I3 first failed** on my errors: coefficient -1 instead of -2 (fixed), K(Q) normalisation (fixed). I3b's remaining failure stands.
- **Five BIMOND rows show `sympy_ok` false.** The routine misses them; a separate check gives f = 1 - y - u - log(1-y) and residual under 3e-17. They fail G4p anyway.
- **Debugging order.** Gate labels of the known-answer rows and one SKh row were seen before A2, with a placeholder Q2. A2 changed G5's definition after that.
- **Compute breach.** The grammar build peaked at 4.76 GB, over the 4 GB rule, once. One thread, nice 19; BF1, UX7, AF1 and AR1 untouched. The run takes minutes, so no queue was needed.

**Limits of the gates.**
- G3 is leading WKB on frozen backgrounds, so it can't see Jeans terms. ND on nearly everything means health isn't decided here; C5, H3 and H4 are the record's reading.
- G4 and G6 carry [REC] or [EST] where marked, and G7's twist rule is I1's result, not a new solve. G6 labels and the Q2-form choice are assigned by rule from content, not derived per row.
- G5's alpha_2 readout is calibrated on Einstein-aether (beta = -2 - alpha_1/2 + alpha_2) and extended to the other contents without proof. It ignores F'' and mu.
- Grammar gaps: no SX row at all (QUMOND's h = y/4 needs a constant it lacks), BIMOND at a = 1/2 only, one law function per action, cap partway through size 9. KA5's mock is injected labels, so it tests the tally only.

## Reproduce
`python3 as2_grammar.py 2500000 9` (npz gitignored), `as2_q2.py`, `as2_run.py`, `as2_indep.py`, all `OMP_NUM_THREADS=1 nice -n 19 python3 -W ignore`; twin `AS2_MUTATE=1`. Numbers in `as2_run.out`, `.json`, `as2_indep.out`, `as2_q2.json`. Solver imported read only from UX1.

No deposit. PAPER67, the ledger, the outside summary and other lanes untouched. kappa = 1/2 FITTED. Not theory closed.
