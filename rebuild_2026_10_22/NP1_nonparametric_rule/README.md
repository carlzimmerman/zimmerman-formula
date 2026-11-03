# NP1_nonparametric_rule: a flexible leaf function fitted on BF1/SY1's train set passes gates 1-5 in both arms. RQ3 rejects it in both. L3 reads NO SMOOTH RULE IN LEAF SPACE, carried by IC 1613 and by the Υ rows. L5 reads SMOOTH RULE EXISTS IN REACH, but only by 0.002 on the hull line

Criteria `FROZEN_CRITERIA.md` (bc346de43e), committed alone. `AMENDMENT_A1.md` (d8439a56e1), pre-result, committed alone. Scripts:
- `np1_core.py`: data, the Gaussian process, gates 1-4, hull.
- `np1.py`: modes `controls`, `real`, `oracle`.
- `np1_cand.py`, `np1_stage3.py`: RQ3 run unedited.
- `np1_post.py`: **POST-RESULT**.

Outputs are `np1_<mode>.{json,out}`, `rules/*.npz` (the frozen rules), and `results/np1_<mode>_<arm>.{json,out}` (RQ3 cards). Run with `PYTHONHASHSEED=0 nice -n 10 python3 -I np1.py <mode>`, one thread, RSS 0.6 GB, about 40 minutes in all.

**Not blind.** κ = ½ FITTED. No cold component, no particle; the cold sector stays retired, and nothing here reinstates it. Not theory closed. Nothing here says the data favour the framework. A pass is a description of data, not a theory.

## What was done
- **Rule:** log10 B = log10(g_obs / law(g_b, a0)), fitted as a Gaussian-process posterior mean. Prior mean 0, the plain law. ARD squared-exponential kernel, class noise.
- **Leaves:** L3 (log y, log ell, f) and L5 (+ s, asinh D), SY1's formulas.
- **Fit:** on BF1's train set only (odd SPARC, X-COP 0/2/4/6). Lengths by type-II maximum likelihood, then a length multiplier λ by 4-fold grouped cross-validation on train. Frozen per footing.
- **Grading:** BF1/SY1's gates 1-5 and RQ3_acceptance_v2, unchanged.
- **Oracle:** the same hyperparameters refit on train plus every holdout point row. It is a diagnostic: it sees the holdouts.

## Train fit and gates 1-5: train-only frozen rule

| Arm, footing | λ | G1 X-COP train | G2 SPARC train (line) | G3 SPARC even (line) | G3 X-COP unseen | G4 LT | G5 A1 / A2 / A3 |
|---|---|---|---|---|---|---|---|
| L3 canonical | 4 | +0.007 / 0.057 | 0.134 (0.175) | 0.179 (0.195), med +0.020 | +0.003 / 0.035 | +0.002 | 0.052 / 0.50 / 0.02 |
| L3 alt | 4 | +0.007 / 0.057 | 0.134 (0.177) | 0.179 (0.196), med +0.020 | +0.002 / 0.035 | −0.001 | 0.052 / 0.50 / 0.02 |
| L5 canonical | 4 | +0.005 / 0.055 | 0.120 (0.175) | 0.184 (0.195), med +0.022 | +0.005 / 0.031 | +0.016 | 0.056 / 0.50 / 0.01 |
| L5 alt | 4 | +0.005 / 0.055 | 0.120 (0.177) | 0.184 (0.196), med +0.022 | +0.004 / 0.031 | +0.012 | 0.056 / 0.50 / 0.01 |

**Every cell passes gates 1-5.** On the record, this is the first class-blind rule to hold X-COP's unseen clusters (+0.003 dex) while passing discs and LITTLE THINGS. Neither BF1's 2e9 forms nor its near-miss family managed that. It isn't underfit: train rms is 0.12-0.13 against the law's 0.167.

Caveats:
- **λ sits at the top of the CV grid (4)**, so train asks for the smoothest rule offered.
- **G5's median Υ reads exactly 0.50.** The rule learned B at Υ = 0.5, so the FG1 path returns 0.5. G5 is weak for this class.

**Partial dependence (L3, canonical): the shape target for BF1/SY1.** Values are log B over the train sample.

| Leaf | Range | Change in log B |
|---|---|---|
| log y | −1.6 to +0.7 | +0.085 to −0.10 |
| log ell | −8.0 to −6.7 | −0.15 to +0.05, then flat |
| f | 0 to 0.6 | +0.095 to −0.06 |

L5 adds a rising s term, −0.02 at s = −2 to +0.13 at s = +0.9; D is flat. X-COP's +0.47 sits in its own corner of leaf space, which CX1 found has no neighbour. The rule carries it without touching discs.

## Stage 3 (RQ3, unedited): REJECTED in every cell

| Cell | FAIL | PASS | NOT COMPUTABLE |
|---|---|---|---|
| L3 canonical | 11 | 30 | 54 |
| L3 alt | 15 | 26 | 54 |
| L5 canonical | 10 | 31 | 54 |
| L5 alt | 13 | 28 | 54 |

| Row | L3 canonical Z | Note |
|---|---|---|
| A10 IC 1613 | −5.08 (v −0.76) | law −3.94: the rule lifts the f = 0, low-y corner and makes IC 1613 worse |
| A30 lensing | +8.45 | law +9.27 |
| A5 / A6 / A7 Υ estimator rows | +4.1 / +6.0 / −2.3 | law fails these too |
| A23b | −3.6 | |
| Keys B7, B9, B14, B16 | +2.1, −3.0, −2.1, −2.1 | B19 and B20 pass |
| C1 planets | +16492 | by construction: prior mean is the law, AMENDMENT_A1 |

- **Alt adds** A20, A25 and keys B10, B11.
- **L5** has the same pattern, plus A24 and A25 (A30 +12.4); A7 and B7 pass.
- **B23-B25 X-COP pass** in every cell (mean +0.005, rms 0.049).
- **Dwarf rows A11-A13 read NOT COMPUTABLE in every cell.** POST-RESULT `np1_post.out` shows why: g is not monotone in g_b on 30-34 of 50 dwarf rows and about 10 % of SPARC points. A13's field difference then goes negative. **The frozen rule isn't an admissible law in the dwarf corner:** more baryons can mean less gravity there.

## Oracle (train + every holdout point row, frozen hyperparameters)
- **Point lines it fits:**
  - G3 SPARC 0.150-0.160, X-COP +0.002, LT +0.02-0.03.
  - CX1's groups, lensing, Dw-UFD (L3) and Dw (L5) to |z| < 1.
  - Dw at L3 is still +0.12 (z 6.9).
- **IC 1613 is not fitted at the frozen smoothness:** −0.63 (L3), −0.59 (L5).
  - At λ/4, L3 gives −0.30 (z −4.2) and L5 gives −0.13 (z −1.9).
- **RQ3 still rejects the oracle:** A10, A30, A5-A7 and most outer keys fail. Its G5 fails (median Υ 0.49).
  - **A30 isn't fixed by fitting CX1's lensing rows,** because RQ3's ΔΣ forward model isn't CX1's g = 4GΔΣ conversion. So the lensing failure is partly an estimator mismatch, not only data.

## Verdicts (frozen rules plus AMENDMENT_A1; per arm and footing)

| Arm | Canonical | Alt | Carried by |
|---|---|---|---|
| **L3** | **NO SMOOTH RULE IN LEAF SPACE** | **NO SMOOTH RULE IN LEAF SPACE** | A10 IC 1613 (in hull, reach 0.2, oracle fails); A5, A6, A7 (SPARC 93 % in hull, oracle fails) |
| **L5** | **SMOOTH RULE EXISTS IN REACH** | **SMOOTH RULE EXISTS IN REACH** | every failing line is out of reach: SPARC 89.8 % in hull, below the 0.90 line; IC 1613 out of the 4-D hull (s = −2 stand-in) |

### How much each label carries (POST-RESULT, `np1_post.out`; no label changes)
- **L5's label is on a knife edge.** Its SPARC in-hull fraction is 0.898 against the frozen line of 0.90. At a line of 0.85, A5 and A6 become in-hull failures the oracle also fails, and L5 would read NO SMOOTH RULE.
- **L5 escapes IC 1613 only through SY1's s = −2 stand-in.** A2 records that stand-in as false for a half-light radius.
- **A5-A7 can't move by construction.** BF1's train targets are built at a fixed Υ of 0.5, so no rule fitted to them can shift the Υ the FG1 path infers. With A5-A7 set aside, L3's no-go rests on **IC 1613 alone**: one system, two rows, inclination DISPUTED in RQ3.
  - The L3 oracle at λ/4 still misses it by 0.30 dex.
  - CX1 found the IC 1613-SPARC contact goes through one galaxy, F583-1.
- **Reading.**
  - The smooth function does what no closed form in BF1/SY1 did: it holds the X-COP holdout and discs together. So the X-COP wall isn't a leaf-space no-go.
  - What stops it is a short list of individual systems and estimators: IC 1613, RQ3's lensing forward model, and the Υ rows. Some are in reach of train, some only by stand-in. Plus non-monotone g in the dwarf corner, which an admissible law can't have.
  - Taken together this is not closure for the class. L3's no-go stands at the train-chosen smoothness and rests on one disputed galaxy. L5's pass is within 0.002 of the hull line and leans on a stand-in leaf.

## Controls, run and read before the real fit (`np1_controls.out`)

| Control | Result | Verdict |
|---|---|---|
| Known answer | X-COP +0.4675 (35 rows), LT −0.0252 | exact |
| Planted (1 + f) log1p(1/y), noise-free | gates 3-4 rms 0.000 | recovered, every cell |
| Planted, at SPARC's errors | G3 0.128 against 0.195 | recovered, every cell |
| Planted class boost ±0.25 dex | G3 0.284-0.291 against 0.195 | fails, as it must |
| MUTATE (log B permuted over train) | X-COP holdout +0.45-0.46 | bites, every cell |

There was one more check, a plumbing smoke before any result: a rule with α = 0 reproduced RQ3's law card row for row.

## Departures, all disclosed
1. **AMENDMENT_A1, pre-result.**
   - L5's hull is taken on 4 coordinates.
   - The label SMOOTH RULE EXISTS IN REACH was added, because C1 fails for every rule whose prior is the law.
2. **Per-footing refit** (frozen in the criteria), unlike SY1 A2.4.
3. **λ = 4 at the grid's edge** in every cell. The grid was frozen and isn't extended here.
4. **A11-A13 are NOT COMPUTABLE** through the rule's non-monotone g, not through a missing input. Groups (B1), the Milky Way and Bullet are NOT COMPUTABLE because gas or r is NaN, as frozen.
5. **Oracle extra rows come from CX1.** Groups use f = 0.45 ± 0.15 ASSUMED. Lensing is PROVISIONAL with diagonal errors.
6. **RQ3 stage-3 logs are gitignored,** because they print local paths. The JSON and .out cards are committed. `np1_post.py` is POST-RESULT and changes no label.

κ = ½ FITTED. Not theory closed.
