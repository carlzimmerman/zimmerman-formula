# MB1_member_bound_law: result

Criteria 96fa175118, committed alone before any script. Code with AMENDMENT A1 and the checks: e7240f17a0. kappa = 1/2 FITTED. Footings canonical 9.3603e-11 and alt 1.1312e-10 are reported apart, never pooled. No LCDM input. A description: no action, no field equation, no particle, no fluid. The cold sector stays retired, and nothing here reinstates it. Not theory closed. Nothing here says the data favour the framework.

**Question.** Can the number of bound member galaxies be the second variable that picks out clusters? Each member keeps its own law halo out to r_t, and those halos add as ordinary mass. The extra mass then rides with the galaxies, where the Bullet wants it.

## Verdict: no hit. Every arm is REJECTED by RQ3 on both footings, and every arm fails at least one cluster row of its own label.

| Arm | Footing | Label | Fails | Passes |
|---|---|---|---|---|
| F, tidal r_t | canonical | **SHORT**, factor 16.1 needed in M_x | B23 +0.389, B24 0.397, B25 −2.64, keys 10/15, Bullet (sign wrong, M300 1.20, 0.82) | B1 |
| F | alt | **SHORT**, factor 13.3 | B23 +0.355, B24, B25, keys 8/15, Bullet (sign wrong) | B1 |
| E, external-field r_t | canonical | **SHORT**, factor 114 | B23 +0.453, B24, B25, Bullet (sign wrong, M300 1.11, 0.73) | B1 |
| E | alt | **SHORT**, factor 90 | B23 +0.419, B24, B25, Bullet (sign wrong) | B1 |
| N, r_t = r | canonical | **FAILS** | B24 0.112, keys 5/15, B19, B20 | B23 +0.042, B25, B1, Bullet (M300 3.21, 2.34, dκ +0.079, +0.119) |
| N | alt | **FAILS** | B24 0.104, B1 Z +2.24, keys 5/15, B19, B20 | B23 +0.004, B25, Bullet (M300 3.50, 2.56) |
| K, M_x = K M_star | canonical | **FAILS** (not GALAXY SHAPE WORKS) | keys 7/15, B24 0.140, B25 +4.05 | B23 (fitted, K = 50.0), B1, Bullet (M300 2.84, 2.06) |
| K | alt | **FAILS** | keys 8/15, B24 0.133, B25 +3.66 | B23 (K = 47.8), B1, Bullet |
| KG, control | both | control **bites**: Bullet FAIL, dκ −0.24, −0.56 | Bullet, keys 6/15 | B23, B24 0.093, B25, B1 (K 6.68, 6.43) |

Keys are B4–B18 through RQ3's three cells (g005_f034, g005_f0615, g0_f034), worst of both h and both f*. E's keys weren't in its frozen runs and weren't run. All arms share the law's rows outside clusters (SPARC levels A5–A7, IC 1613, dwarfs, planets C1, and Lovisari groups B2 at the law's own value, among others), so RQ3 reads REJECTED for every arm by construction. Scorecards: `results/mb1_{F,K,KG,N}.out`. Fast rows: `mb1_grade.out`.

## What it says, plainly
- **The galaxies can carry the Bullet's extra mass with the right sign only if each galaxy's law halo reaches 300 kpc unscreened (N), or if the amount is fitted at about 50 times the stars (K).** The law's own readings of a member inside a cluster cut the phantom to 3–4 times the stars (F, its tide) or 0.5–0.9 times (E, its external field). At that size the Bullet's lensing peak stays on the gas, and the sign comes out wrong.
- **On X-COP, the tidal shape fits the scatter only after a fitted boost.** Multiplying F's M_x by 13–16 gives mean 0, rms 0.090–0.092, and B25 passes (`mb1_lambda.out`, reported only). E needs 90–114. N needs 1.01–1.16, and its rms stays at 0.105–0.107, over the 0.10 line.
- **No member-mass shape passes the keys.** N's halo grows about linearly with r, so it over-masses every outer key (G-OUT −3 to −12 σ). K's constant ratio fails 7–8 keys in both directions.
- **The same split as before.** Mass on the galaxies passes the Bullet and fails the keys. The same amount on the gas (KG) passes X-COP fully and fails the Bullet. MB1 gives the Bullet a carrier, but no tested amount of member mass fits the keys too.

## Expectations on record against results
| Expectation (criteria) | Result |
|---|---|
| F short of X-COP by a factor 2–4 (65 %) | Short by 13–16. Right direction, wrong size |
| K needs about 20–30 | K = 50.0, 47.8. Wrong |
| K fails keys (60 %) | 7/15, 8/15. Right |
| Bullet sign right (85 %) | Right in N and K. **Wrong in F and E**: the stellar extra is too small to pull the peak off the gas |
| Bullet mass fails in F (70 %) | M300 1.20, 0.82 against 3.5, 2.3. Right |
| REJECTED in every arm (99 %) | Right |

The hand estimate in the criteria put E about ten times short. Its fitted factor is 90–114.

## Checks
K1 2.2e-16, K2 2.2e-16, K3 +1.96 % (line 2 %), K4a, K4b and K5 all PASS before any graded number (`mb1_checks.out`). The mass-grid check moves the mean by +0.00006 dex. Checks run after the first read:
- **K6 PASS** (`k6.out`, `k6_probe.py`). gb r²/G at r500 equals the harness's own Mb at r500 in all 3912 cluster calls, ratio 1.000000. GE is SI G, r500 runs 0.38–1.67 Mpc, Mb500 4e10–2e14 M☉. The probe's fresh keys run reproduces arm K's key rows line for line.
- **K7 PASS.** The fast grade reruns byte-identical (`mb1_post_checks.out`, cmp exit 0).
- **MUTATE.** On N and K, R·st moved onto the gas loses the Bullet sign on both footings (dκ −0.16 to −0.44), exit 1 by the result (`mb1_post_checks.out`).

## Disclosures, all after the first read
1. **K6 wasn't in `run_mb1.sh`.** It ran after the graded numbers were read. It reads the harness's own Mb from the calling frame, which is the frozen K6 wording, in place of A1 item 7's workaround against X30's table. The first probe crashed on the harness's pre-call, where r500 comes in as an array. That was fixed and the probe rerun.
2. **The first MUTATE proved nothing.** It ran on F, whose Bullet already failed, and its exit code was hard-coded to 1. The exit now comes from the result, and MUTATE was rerun on N and K, the arms whose Bullet passes. F's run stays as `mb1_grade_MUTATE.out`.
3. **N's keys weren't in N's frozen runs.** They were added after the read and can only add failures. N was already FAILS on B24.
4. **The λ fit is post-result.** It is reported because the criteria ask SHORT arms for the factor needed. It is a fitted number, not a rule.
5. **Sensitivities move no label** (F only, `mb1_grade_{a10,a14,icl,base,f03,f085}.out`). X-COP mean canonical: α −1.0 gives +0.397, α −1.4 gives +0.379, 30 % ICL gives +0.412, base law(g_b) gives +0.380. Groups at f 0.3 and 0.85 give B1 Z −0.53 and −0.22.

## Limits
These are the criteria's limits. The model is static. Phantoms sit at their member, so r_t isn't smeared. There are no orbits and no stripping history, and the tide is circular-orbit. The Bullet is QUMOND-type with PROVISIONAL σ (UX6), and for MB1 its γ is 1 at 300 kpc (A1). X-COP is DISPUTED HSE, and keys use HSC 1.7. N departs from the law's field equation on purpose: a bound member reads as a [LABEL], and the harness tag stands.

## Files
`FROZEN_CRITERIA.md`, `AMENDMENT_A1.md`, `mb1_core.py` (the rule), `candidates/` (one module per arm), `mb1_acc.py` (runs RQ3's acceptance.py unedited), `mb1_fast.py` (checks, K fit, fast rows, own Bullet), `mb1_lambda.py`, `k6_probe.py`, `run_mb1.sh`, `run_mb1_post.sh`. The harness's byte copies are `old_gates.py`, `tolerances.json` and `row_marks.json`. The keys caches and the X74 by-products the keys path writes are not committed.
