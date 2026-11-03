# BF3_all_gates_first: JOINT FORM, ABSOLUTE at Stage 1 on both footings, one form, **NOT ABOVE CONTROL** (scrambled clusters give 7-33 times more joint hits per expression), and it **fails the holdouts**: keys 11/15 and 8/15, TDG, Milky Way, IC 1613. Gate 0 holds only at exactly f = 0. The Bullet isn't computable here and is the expected kill.

Criteria `FROZEN_CRITERIA.md` (b25ab0a57d), committed alone first. `AMENDMENT_A1.md`, compute only, written after timing shards. `AMENDMENT_A2.md`, post-result: cheap joint hits were seen on 6 shards before it. **Not blind**: BF2's failures set these gates. A description at best: no action, no field equation, no fitted float. kappa = 1/2 FITTED. Footings canonical and alt are graded apart, never pooled. The cold sector stays retired and nothing here reinstates it. Not theory closed. Nothing here says the data favour the framework.

## Read this first
- **The question has an answer inside this grammar: yes, at Stage 1, and it means little.** H = 1 + f [(1 + pi) y + 1/2 - c/(f +- ell)], wrapper W3, c = 1/3 or 1/pi, so four spellings of one form. In plain words: law x (2/3 + f/2 + (1 + pi) g_gas/a0). It's UX3's gas term again, with the constant offset written as -c f/(f + ell). Exact, both footings: lensing chi^2_sys 72.8-74.8 (line 77.2; the law reads 83.2 canonical, 96.2 alt), groups |Z| <= 1.6 at f 0.3, 0.6, 0.85, SPARC rms 0.079-0.083 (law 0.054), U 0.57-0.59, X-COP **+0.22 dex short** at Z +1.8. It passes X only because the frozen line, 2 sigma with 0.12 dex of hydrostatic systematic, allows about 0.24 dex. **No form holds X-strict with the other gates on both footings except one (F5), and that one fails L-abs on alt.**
- **NOT ABOVE CONTROL.** Like-for-like, same 105 shards, 6.1e8 expressions per arm, Family A canonical. Joint passes per 1e6 tried, estimated from S on sampled candidates: real rows 16.9, scrambled C1 557, C2 119, C3 566. With L-abs: 4.2 real against 85, 6.3, 67. X passes per 1e6: 42k real, 62k-121k scrambled. **Shuffling which cluster row gets which y, f, ell makes joint passes more common, not rarer.** So the gates as frozen don't pin a physical relation between the leaves and the cluster deficit: a mean lift of about 0.2 dex on X-COP, applied any way, passes.
- **Gate 0 is passed by a singular limit.** At exactly f = 0, H = 1. With a trace of gas H is about 0.67 on a disc for f >> ell (f 1e-6 at 5 kpc: 0.60-0.73), and at Saturn f = 1e-6 gives H = 3.5, f = 1e-3 gives 2,860 (`bf3_fzero.json`). Same kind of protection as BF2's P7, which had H(f -> 0) = 0.64. **The Sun is gas physically; f = 0 is a labelling choice.** At f = 1, Saturn's anomaly is 1.8e2 m/s^2, Z 1.9e16. The law itself fails unscreened Cassini (PAPER58, RQ3 C1 Z 1.65e4), so gate 0 only ever asked for the law's standing.

## Stage 2, holdouts, RQ3 unchanged, lines |Z| <= 2. `results/`, `bf3_holdout.out`
| Form | Footing | Keys | Keys failing, Z | A23a TDG chi^2 (line 12.6) | A9 LT | A10 IC 1613 | A18 DiskMass | A16 MW, f 0.05 | A30 cov-only | Label |
|---|---|---|---|---|---|---|---|---|---|---|
| a0 law | can | 10/15 | MID-T3 +4.86, M3 +4.76 | 10.8 PASS | PASS | -3.94 | PASS | FEASIBLE IN PRIORS | 154 | reference |
| F1, F2: c = 1/3 | can | **11/15** | MID-T3 +3.39, MID-b +2.69, OUT-all -2.56, M3 +2.16 | **38.6 FAIL** | PASS -0.08 | **-4.09** | PASS 1.21 | **V+K ONLY, FAIL** | 232 | joint, fails holdouts |
| | alt | **8/15** | OUT-all -3.17, MID-T3 +3.11, ... | 39.4 FAIL | PASS | -4.33 | PASS | FAIL | 182 | |
| F3, F4: c = 1/pi | can | 10/15 | MID-T3 +3.34, OUT-all -2.66 ... | FAIL | PASS | FAIL | PASS | FAIL | ~225 | joint, fails holdouts |
| F5, E: log1p(y/ell)(0.6 - 1/(1+f) + y), the X-strict one | can | **7/15** | OUT-all -5.08, Mall -5.04 ... | 83.0 FAIL | **-2.03 FAIL** | -4.39 | PASS | FAIL | 365 | L-abs fails alt; A3 tilt Z +8.4 |
| | alt | 6/15 | | 84.4 | FAIL | FAIL | PASS | INFEASIBLE at f 0.15 | 292 | |

Also failing for F1-F4 as for the law: A5, A6, A12, A13, A23b, A24, A26a, B2, B24 (rms 0.24), B25. Lensing passes only under the frozen systematic: cov-only chi^2 is 232 against the law's 154, so **the added 12.5 % correlated amplitude term is what lets it through.** That term is mine and PROVISIONAL. Gas scaled x 0.5 and x 0.25 in the lens model makes cov-only worse, 309 and 355. **Bullet: NOT COMPUTABLE,** because UX6's map has ell = 0, where these forms are singular. Expected kill, stated before the run: any local present-gas form puts its boost where f is highest, on the gas (UX6, MG1, BF2). Groups and Milky Way have no gas on file; they're at assumed f, reported beside.

**HOLDS HOLDOUTS: none.**

## Stage 1, exact, both footings. `bf3_final.out`
| Arm | Expressions | Coverage | Distinct joints, exact on top 300 | Joint on both footings: L-law, L-abs, X-strict |
|---|---|---|---|---|
| A canonical | 5.67e9 | 935 of 1,043 shards, 2 h budget | 214 L-law, 128 L-abs canonical | 52, 0, 0 |
| B canonical | 6.11e9 | complete; 3.6e6 pass gate 0 numerically | 17, 1 | 1, 0, 0 |
| E canonical (level-3 pool, 80,000) | 1.36e9 | 57 of 3,200 shards, 1 h | 212, 162 | 106, 0, 1 |
| A alt | 6.13e8 | 10 % of jobs | 76, 16 | 32, **4**, 0 |
| B alt | 6.13e8 | 10 % | 1, 0 | 1, 0, 0 |
| C: BF1 L4 snapshot | 6,272 hits, sha256 9eb8e496... | 137 pass gate 0 | 0 joint | best: L 82.1, G f.3 -1.47 |

Funnel on a 0.1 % sample of Family A canonical, frozen order: 3.91e6 tried; gate 0, 3.69e6; L-law, 1.22e6; +G, 1.18e6; +X, 21,006; with L-abs: 298,284, 277,976, **31**. **So lensing and groups are easy for protected forms; L-abs plus X is the narrow part, and S cut the 25,000 L-abs candidates seen in A to about 16,000 by sampling.** Precut losses on the sample (K5): 0 in every arm.

### Near misses, best per gate combination (canonical; alt in the file), exact numbers, labelled NEAR MISS
| Passes | Form | Fails |
|---|---|---|
| X, L-abs, G, S except X-strict (E) | W2 `log1p(y/ell) (0.6 - (1/(1+f) - y))` | X-strict; L-abs on alt (chi^2 within the L-law line there) |
| X, L-abs, S | W3 `pi^2 log1p(y) - (1/pi)/(ell - f)` | G at -2.8 on all three f |
| X, G, L-law | W1 `(y f/sqrt(ell)) / ((f + 2) + pi y)` | S (rms 0.197, U 0.30), lensing 151 |
| X, L-abs, G (B) | W3 `(f + 1 - sqrt f) + 2 pi y f`, H itself | S on alt, X-strict |

Family (b)'s cut-off forms show up as X-alone bests that fail lensing at chi^2 300-600 and groups at Z +6 to +8, as BF2 found.

## Checks
K1 exact path reproduces RQ3 for the law: A30 154.149 and 124.996, B23 +0.4675 and +0.4345, A1, A2, B1, each within 1e-3 (`bf3_k1.out`, 26 PASS). K2 BF2's P3, P7, P8 A30, X-COP and S reproduce. K3 cheap against exact: lensing lower bound within 1 % below chi^2 400 (max ratio 1.010), worse above (1.17), outside any line. **K3 groups FAILS its 0.01 dex criterion on wild forms: median 0.007, max 0.13 canonical and 2.3 alt.** The cheap G slack was 0.045 dex, so a few joint forms could be lost there. K4 planted H = 1 + f sqrt(y)/(1+y), W2: recovered at zero distance (`bf3_k4.json`). K5 above. **MUTATE twin:** H x 1.5 breaks K1 (26 FAIL lines, exit 1) and K4 (planted lost, exit 1). **Rerun:** three r10 shards byte-identical.

## Errors and limits, disclosed
- **Amendments post-result.** A1 after timing; A2 after cheap joint hits were seen. Real A canonical isn't exhaustive (90 % of shards), E covers 2 %, alt and C1 cover 10 % of jobs. A form passing only on alt outside that 10 % would be missed.
- Lensing's systematic term (0.125, fully correlated) is my PROVISIONAL reading of stellar-mass, shear and redshift systematics; it moves the law from 154 to 83 and the joint form from 232 to 73. **With RQ3's cov-only A30, nothing here passes lensing, the law included.**
- A30's two-halo template carries fixed background numbers inherited from CRG1, RQ3; b = 0 changes the joint form's chi^2_sys by 0.1-0.2.
- Groups have no gas on file; f is assumed. f = 0.85 is reported, not gated.
- S was sampled: up to 20,000 L-abs candidates and 10,000 others per arm; counts are estimates. Exact regrade was on the top 300 distinct per arm.
- First final reads crashed twice on non-finite exact models (lens, then a group's log); guards added that return a failure, and the read was rerun in full. The first partial output is kept as `bf3_final_firstpass_crashedC.out`.
- The planted precut first used the real targets (stale copy). Fixed before K4 passed; not used by any real arm.
- Compute: nice 19, at most 4 workers, private memory under 1 GB per process; load on the machine was 50-90 throughout.

## Expectation against result
JOINT ABSOLUTE on a footing 3 %, both 2 %: **happened, both,** but only through X's 0.24 dex allowance, lensing's added systematic, and the f -> 0 singularity. LAW'S LENSING on both 8 %: happened, 192 distinct. Law passes L-abs under the systematic, 25 %: no, 83.2. Holds holdouts 10 %: no. Real above control by 3, 50 %: **no, below.**

kappa = 1/2 FITTED. Not theory closed.
