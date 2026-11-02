# BF2_near_miss_family: FROZEN CRITERIA (committed alone, before any BF2 script or number)

Owner's standing go, 2026-11-02. Question: does BF1's L4 near-miss family, a boost rising with gas share and cut off when f/y is large, survive everything we can compute?

**Not blind.** Read before this: BF1's criteria, README, `bf1.py`, `bf1_near.py`, its interim printout (3,918 scored hits, 0 Stage 1, best W3 form rms 0.184 against line 0.1747), RQ3's README, `acceptance.py`, tolerances, UX6's README and script, MG1's README and criteria. The forms are already seen, and they came out of about 1.7e11 tries. No BF2 number exists yet. Nothing here touches BF1's process or changes its gates; BF1's NO HIT at Stage 1 stands whatever happens here. Description at best: no action, no field equation. **The highest label any form can take in this lane is NEAR MISS, and a second implementation is owed before anything beyond it.** kappa = 1/2 FITTED. Footings canonical 9.3603e-11, alt 1.1312e-10, reported apart, never pooled. No cold component, no particle; the cold sector stays retired and nothing here reinstates it. Not theory closed. Nothing here says the data favour the framework. PAPER67, ledger and outside summary untouched.

## Snapshot
`chunks/real_L4/hits.jsonl` and `names.json` read-only. The first complete N lines at the moment of the scan, N and SHA-256 recorded. Lines added later are not in this lane.

## Step 1, families
Parse each hit. Collapse any subtree without y or ell to F (contains f) or C (constants only); merge F op F, F op C to F. Sort commutative arguments. The resulting string plus the wrapper is the family signature. Representative: fewest nodes, then lexical. Report count, H at f = 0, and the plain meaning of the largest families. H(f=0) = 1 identically, or not, is a recorded split.

## Step 2, SPARC
Two statistics, side by side, on every hit: BF1's fixed Upsilon pointwise rms on train and holdout, and FG1's free Upsilon path through CRG1's `fit` and `tilt`, the law as reference. f is recomputed at each Upsilon. For the representatives chosen below, and the law: rms and Upsilon by V_flat bin and by gas-share tercile, worst galaxies, Upsilon median, tilt, surface-brightness slope (RQ3 A4), LITTLE THINGS (RQ3 A9), and the minimum of g/g_b.

## Choosing what goes to RQ3. Rule fixed now, applied on the snapshot
Score S, canonical: the largest of rms/0.110, |U - 0.65|/0.15, |tilt|/0.15, |LT|/0.10, |X-COP all 7 mean|/0.05, X-COP all 7 rms/0.10. S <= 1 passes those six lines. These lines are RQ3's and FG1's and aren't moved.
- **P1:** BF1's interim best, W3 `(sq(((f+2.0)/inv1p(f)))*inv1p(((f+pi)+(f/y))))`.
- **P2:** lowest S over all hits.
- **P3:** lowest S among hits with H(f=0) = 1 at all y, so stars-only systems read the law.
- **P4:** representative of the largest family, if not already one of these.
P2 and P3 are chosen using all of SPARC and all of X-COP, so **those rows are not out of sample for P2, P3.** Keys, Bullet, dwarfs, groups and the rest are unseen for selection.

## Step 3, RQ3
`RQ3_acceptance_v2/acceptance.py` read-only, loaded unchanged except that outputs go to this lane and its tolerances, marks and gates are read from RQ3's directory; the substitutions are listed in the script. Both footings, 15 keys, X-COP all 7. Tolerances are RQ3's `tolerances.json`, line |Z| <= 2, unmoved. Rows RQ3 can't compute for a gas-reading g stay NOT COMPUTABLE. Reported beside, never in place: groups and Milky Way at stated assumed f, since neither has gas on file.

## Step 4, Bullet and mergers. Three readings of f, because f has no field definition, all mine
- **Fa, local field share:** |g_gas|/|g_b| at the point, clipped to [0, 1], through RQ3's B28, UX6's map.
- **Fb, enclosed share about each BCG:** UX6's N1 structure, the law locally plus a radial term law(g_t) (H - 1) per group, f = M_gas(<r)/M_b(<r), y = g_t/a0. **Fb2:** same with gas restored on its BCG, UX6's N2.
- **Fc, local density share:** rho_gas/(rho_gas + rho_stars). Doesn't reduce to BF1's f in a concentric cluster; reported.
Graded with UX6's `observe`, sigma values as UX6's (PROVISIONAL on position and mass). UX6's labels: DEAD if every cell fails position or sign; ALIVE if all pass; WOUNDED, MIXED otherwise. MG1's pair model for its usable rows where the form computes: dkappa sign against its observed labels, its verdict rule unmoved, PROVISIONAL inputs.

## Step 5, Saturn
RQ3's C1 with its real errors, plus H at Saturn and Z = anomaly / sigma, with f = 0 taken as stated. **The Sun is gas physically; f = 0 is a labelling choice,** said in the README, and f = 1 is reported as well.

## Step 6, control
BF1's L3 counts as recorded. At L4, on the real run's own closure list, one thread: a frozen random sample of completed jobs, seed 20261102, as many as finish in a budget of 2 hours of wall time. Arms on identical jobs: **real rerun**, which must reproduce `hits.jsonl` exactly on those jobs, **control** with BF1's control scramble, **two more permutations**, seeds 1, 2. Report hits per arm, 95 % bootstrap over jobs on the ratio, and how many hits per arm reach fixed-Upsilon rms <= 0.20, and pass unseen X-COP, |mean| <= 0.05, rms <= 0.10. **Limits:** scrambled arms reuse the real closure list, whereas a true control would dedupe its own, and the sample is short of 1.7e11. If real isn't above the control's mean by a factor of 3 with the bootstrap's lower bound above 1, **"NOT ABOVE CONTROL" goes in the title.**

## Labels, per form and footing
- **NEAR MISS, DISCS AND CLUSTERS:** passes A1, A2, A3, A4, A9, B23, B24 and at least 14 of 15 keys.
- **X-COP ONLY:** B23, B24 pass, A1 or A2 fails.
- **BROKEN:** X-COP fails too.
Separately, and it doesn't soften any label: Bullet label per reading, C1 PASS or FAIL, RQ3 overall.
Family verdict: the best label any form holds on both footings, with Bullet and planets stated beside it.

## Checks, verify a fail as hard as a win
K1 RQ3 through my loader reproduces `results/law.json` labels and values. K2 H = 1 candidate from my generator equals the law, RQ3 rows same. K3 my flat free-Upsilon fit equals CRG1's `fit` on the law and UX3's term, 1e-9 on rms. K4 BF1's interim numbers for P1 reproduce to 1e-3, and H = 1 on X-COP gives +0.4675. K5 Bullet, k-free H = 1 gives UX6's LAW row, and my Fa map with UX3's H = 1 + k f y gives UX6's L1 row to 1e-3 (since f y = g_gas/a0 when unclipped). K6 control real arm reproduces hits exactly. K7 RSS under 4 GB.
**MUTATE twin, must fail:** H x 1.5 in the generator breaks K2, K3 is fed the mutated law, K4 and K5 break, control's real arm no longer matches; separate outputs, exit 1. **Rerun byte-identical** for scan, Bullet and control's sample; RQ3 rerun on P1 with cached keys.

## Expectation, mine, on record
Free Upsilon lifts some forms over the rms line: 60 %. Upsilon median out of 0.50-0.80 for the boosted forms: 70 %, since H above 1 at low f lowers Upsilon as UX3 did. Any form NEAR MISS, DISCS AND CLUSTERS on a footing: 12 %; on both: 5 %. Keys at least 14 of 15 on canonical for P1: 25 %. Bullet DEAD in every reading: 85 %. C1 FAIL for every form, the law's failure included: 97 %. Real above control by 3: 40 %.

## Compute
One thread, nice 19, under 4 GB. BF1 and AR1 processes untouched. Lane directory only; `git commit -- <dir>`; no push.
