# X19_selector_rank_test: does one physical variable order the record's "extra cold mass" pattern?

Criteria: `FROZEN_CRITERIA.md` + `ASSUMPTION_LEDGER.md` (8960ea2285, committed alone first); `AMENDMENT_A1.md` (0fc9bade54,
pre-result: K4's reference value); `AMENDMENT_A2.md` (post-result: step-0 check code only). κ = ½ FITTED. Footings
9.3603e-11 / 1.1312e-10 m s⁻², never pooled. No dark-matter particle. Not "theory closed". Nothing here says the data
favour the framework. Every number is in `x19_selector_rank_test.out`, `_results.json` or `x19_classes.csv`.

## Verdict: NO LOW-DIMENSIONAL SELECTOR (both footings)

No single variable separates the classes that need extra from those that need none, and no axis-aligned pair does either.
This holds on both footings under the primary reading (baseline B_iso, Z labels, 16–84 % intervals). It also holds for every
reported variant: the v3s EFE baseline, the brief's literal labels, strict min–max intervals and h = 0.686. No V* exists.

**Decisive labels** (Z ≥ 2 EXTRA, Z < 1 NONE; both footings unless noted):
- **EXTRA:** clusters T2 and T3, MW ultra-faints, bright M31 dSphs, M31 others, and the cosmic background (by
  requirement).
- **NONE:** SPARC small and large, groups, cluster T1, the MW disc, the isolated LG dwarfs, Crater II, UMa members, TDGs,
  DF2/DF4, and Antlia II (alt only).
- **AMBIGUOUS (do not constrain):** MW classical, Coma UDGs, and Antlia II (canonical, Z 1.11).

**The labels depend on the baseline, and this is the main finding beside the verdict.**
- Against the isolated law (the successor's no-EFE baseline), Crater II needs *less* than the law: −0.443 / −0.478 dex.
- On the same baseline Antlia II needs about none (+0.060 / +0.024), and the Coma UDGs are only 1.64 / 1.45σ above.
- Their large hosted "excess" is the v3s EFE's: +0.49, +1.01 and +1.12 dex against B_EFE.

## Class table (canonical; class medians; E in dex of g over the isolated law, Z in brackets)

| class | E_iso (Z) | label | E_EFE | M_b [M☉] | σ [km/s] | ρ_b [M☉/pc³] | x | e | \|Φ\|/c² | kT [keV] | N_orb | ρ_env | H |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SPARC small | −0.046 (−1.71) | NONE | −0.05 | 1.0e9 | 45 | 1.4e-3 | 0.046 | 0.052 | 7.7e-9 | 0 | 24 | 3.9e-8 | 0 |
| SPARC large | −0.047 (−3.06) | NONE | −0.05 | 2.8e10 | 110 | 6.9e-4 | 0.085 | 0.046 | 6.9e-8 | 0 | 15 | 3.9e-8 | 0 |
| Groups (63) | +0.020 (+0.31) | NONE | +0.02 | 5.7e11 | 140 | 4.8e-7 | 0.0048 | N/A | 5.2e-8 | N/A | 1.1 | 3.9e-8 | 0 |
| Clusters T1 | +0.040 (+0.29) | NONE | +0.04 | 4.0e12 | 450 | 5.1e-6 | 0.018 | 0.0022 (band) | 9.8e-7 | 1.3 | 3.2 | 3.9e-8 | 0 |
| Clusters T2 | +0.268 (+2.29) | EXTRA | +0.27 | 1.4e13 | 510 | 1.3e-5 | 0.043 | 0.0022 (band) | 2.6e-6 | 1.6 | 3.6 | 3.9e-8 | 0 |
| Clusters T3 | +0.264 (+4.83) | EXTRA | +0.26 | 3.5e13 | 630 | 2.3e-5 | 0.079 | 0.0022 (band) | 5.0e-6 | 2.5 | 4.5 | 3.9e-8 | 0 |
| MW disc | −0.143 (−9.93) | NONE | −0.14 | 6.6e10 | 160 | 0.026 | 1.3 | 0.016 | 3.9e-7 | 0 | 63 | 3.2e-6 | 0 |
| LG field (13) | +0.055 (+0.68) | NONE | +0.06 | 8.9e6 | 9.3 | 5.4e-3 | 0.012 | 0.011 | 4.0e-9 | 0 | 71 | 1.9e-6 | 0 |
| MW classical (8) | +0.277 (+1.87) | AMBIG | +0.34 | 1.0e6 | 9.0 | 5.0e-3 | 0.014 | 0.099 | 2.8e-8 | 0 | 110 | 1.6e-4 | 1 |
| MW ultra-faint (31) | +0.625 (+5.62) | EXTRA | +1.35 | 8.5e3 | 3.7 | 1.3e-3 | 8.0e-4 | 0.15 | 4.1e-8 | 0 | 170 | 3.8e-4 | 1 |
| bright M31 (25) | +0.249 (+2.70) | EXTRA | +0.58 | 7.4e5 | 7.8 | 1.3e-3 | 3.4e-3 | 0.079 | 2.9e-8 | 0 | 58 | 8.0e-5 | 1 |
| M31 others (5) | +0.644 (+2.28) | EXTRA | +0.99 | 6.2e4 | 7.1 | 2.4e-3 | 2.2e-3 | 0.11 | 4.1e-8 | 0 | 150 | 1.6e-4 | 1 |
| Crater II | −0.443 (−3.31) | NONE | +0.49 | 3.2e5 | 2.3 | 1.4e-5 | 1.2e-4 | 0.083 | 2.4e-8 | 0 | 6.5 | 1.2e-4 | 1 |
| Antlia II | +0.060 (+1.11) | AMBIG | +1.01 | 1.3e6 | 6.0 | 5.0e-6 | 1.0e-4 | 0.077 | 2.2e-8 | 0 | 7.3 | 9.8e-5 | 1 |
| Coma UDGs (9) | +0.325 (+1.64) | AMBIG | +1.12 | 6.2e7 | 22 | 4.5e-4 | 7.5e-3 | 0.85 | 1.4e-5 | 0 | 32 | 1.2e-4 | 1 |
| UMa members (28) | −0.063 (−2.28) | NONE | −0.06 | 1.7e10 | 97 | 1.6e-3 | 0.13 | 0.047 | 7.4e-8 | 0 | 24 | N/A | 1 |
| TDGs (6) | −0.691 (−6.80) | NONE | −0.59 | 7.6e8 | 17 | 1.3e-3 | 0.038 | 0.19 | 7.2e-8 | 0 | 0.3 | 5.0e-4 | 1 |
| DF2/DF4 | −0.843 (−4.04) | NONE | −0.72 | 1.8e8 | 7.4 | 1.6e-3 | 0.023 | 0.16 | 9.2e-8 | 0 | 8.2 | 2.5e-4 | 1 |
| Cosmic background | +0.804 (req.) | EXTRA | +0.80 | N/A | N/A | 6.1e-9 … 8.2 | 0 … 15.6 | 0 | N/A | 2.6e-7 | 0 | 3.9e-8 … 52 | 0 |

- **Table conventions.**
  - f_hot is 0.83 for the clusters, 0 for every galaxy-scale row, and N/A for the groups.
  - f_b (reported only) is in the CSV.
  - The alt rows, with their 16–84 % ranges, are in `x19_classes.csv`.
  - Alt labels are the same except Antlia II, which is NONE on alt (Z 0.44).
- **Sources of E.** P4 for SPARC, groups, the MW disc, TDGs and DF2/DF4; X7 CAL for the cluster terciles; X1 for the LG
  dwarfs; S1 for Coma; U1 for UMa. JSON keys are in `FROZEN_CRITERIA.md` §2 and are printed per row in the `.out`.

## Which V fail, and on which classes (primary; both footings identical in class)

| V | result | fewest offenders at the best threshold |
|---|---|---|
| M_b | FAILS | MW ultra-faints, bright M31, M31 others (extra at both ends of the mass range). Background not placeable |
| σ (and T_vir) | FAILS | cluster T1, ultra-faints, bright M31, M31 others |
| ρ_b | FAILS | T2, T3, ultra-faints, bright M31, M31 others, background |
| x = g_N/a₀ | FAILS | T2, T3, ultra-faints, bright M31, M31 others, background (whose band 0 … 15.6 spans every bound system) |
| e (host field) | FAILS (INCOMPLETE: groups' field not on disk) | ultra-faints, bright M31, M31 others, T1 |
| \|Φ\|/c² | FAILS (J1's result, reproduced in kind) | ultra-faints, bright M31, M31 others |
| f_hot | FAILS (INCOMPLETE) | T1, ultra-faints, bright M31, M31 others, background |
| kT | FAILS (INCOMPLETE; eRASS1 KT exists for 29 / 39 / 38 of 109 / 108 / 109 clusters) | T1, ultra-faints, bright M31, M31 others |
| N_orb | FAILS | LG field, T2, T3, bright M31, background |
| ρ_env | FAILS (INCOMPLETE: UMa) | canonical: Crater II, TDGs, DF2/DF4, T2, T3, background; alt: T2, T3, ultra-faints, bright M31, M31 others, background |
| H (hosted) | FAILS | T2, T3, ultra-faints, bright M31, M31 others, background |
| f_b, O (reported only) | FAIL | f_b: T2, T3, bright M31, M31 others (canonical); O: T2, T3, ultra-faints, bright M31, M31 others, background |

**The structure behind the failure.**
- **At galaxy scale the offenders are always the same three hosted-dwarf classes.** Every variable that splits cluster T1
  from T2/T3 (M_b, |Φ|) puts the ultra-faints, bright M31 and M31 others on the no-extra side.
- **Every variable that singles out hosted dwarfs** (H, e, ρ_env, low x) also takes in hosted systems that need nothing:
  Crater II, TDGs, DF2/DF4 and UMa members. It also misses the clusters and the background.
- **At fixed host field, compact hosted dwarfs need extra and diffuse ones do not.** The ultra-faints have x ≈ 8e-4;
  Crater II and Antlia II have x ≈ 1e-4. That is the EFE's signature, read against a baseline without an EFE.

**The cluster-only ordering is not a selector.**
- M_b and |Φ|/c² order T1 below T2 and T3, with best thresholds M_b ≈ 8.4e12 M☉ and |Φ|/c² ≈ 1.7e-6.
- For M_b this gap is partly by construction, because the terciles are cut on MGAS500.
- X7 itself classes the mass trend of A_MID as UNDECIDED: a step improves χ² by only 4.2–4.6, against a line of 9. Its
  quintiles are not monotone (A_MID 1.45 / 1.24 / 1.82 / 1.38 / 2.19, canonical h 0.672).
- σ and kT do not split T1 from T2.

## Two-variable search (frozen: run because every single V failed)

**No pair separates on either footing.** The nearest miss, on both footings, is **(M_b, |Φ|/c²)**, with one offender:
- The rule is "extra iff M_b < 10^5.45 ≈ 2.8e5 M☉ OR |Φ|/c² > 10^−5.77 ≈ 1.7e-6".
- The offender is **bright M31**: its 16–84 % mass range, 2.4e5–5.7e6 M☉, straddles the cut.
- The cut also sits only 0.06 dex below Crater II's 3.2e5 M☉.
- The cosmic background is not placeable on either variable.

The next pairs have two offenders each:
- (M_b, N_orb): bright M31 and LG field.
- (M_b, σ): bright M31 and T1.
- (M_b, e), (M_b, kT) and (M_b, f_hot): bright M31 and T1, and incomplete because the groups have no value.
- (Φ, N_orb): bright M31 and LG field.

Adding the reported-only O or f_b does not produce a separating pair.

**Reported, B_EFE baseline.**
- Here every hosted dwarf class needs extra, including Crater II, Antlia II and Coma.
- The nearest pair is again (M_b, |Φ|), with M_b < 1.4e8 M☉ OR |Φ|/c² > 1.7e-6. Its one offender is the **isolated LG
  dwarfs**.
- (x, e) and (x, kT) miss only cluster T1, but are incomplete because the groups have no value.
- So under the v3s baseline the pattern needs a third ingredient: hosted (H = 1) and small, or deep. TDGs and DF2/DF4 are
  excluded only because they are heavier than 1.4e8 M☉, not by any variable that names their origin.

## Step 2: action-level mechanisms in the record (reported only)

No V separates, so there is no selector to match to an action. For the near-miss variables:
- **Potential.** J1 (Part A, sympy) shows Φ enters the v3/v4 actions only at post-Newtonian order (≤ 4e-6) and through
  H2's hydrostatic dust. An a₀(Φ) would be a postulate (+1 function, +1 constant), and J1 found it fails.
- **Mass and energy.**
  - CFG930 (energy-limited settling, one constant ε; LEDGER:690) was CONTRADICTED on both footings.
  - CFG921's five one-constant selectors (LEDGER:681) failed on both footings.
  - CFG914's density threshold (LEDGER:670) found NO COMMON ORDERING, which this lane reproduces in kind for ρ_b.
- **Capture and ownership.** Z★'s R2 uses CFG939's capture criterion (relative speed vs baryonic escape speed; Z1
  `DESIGN.md` §2). It is non-variational and was not a candidate here. U1 shows it makes hosted satellites dust-free, which
  moves them the wrong way.
- **Supply radius.** Z★'s crossing mass, M_× = 2.7e13 / 4.7e13 M☉ (200ρ_c), is the only mass scale between galaxies and
  clusters that the record derives (Z1 `DESIGN.md`:86). It is a supply-radius effect, and it gives no core excess at
  X2's tercile medians (ZT2B: PROFILE-LIMITED).
- **Status of any successful (M_b, Φ)-type rule.** It would be new physics: two thresholds, so +2 constants, with no action.
- **What it would predict out of sample.** Fossil and ordinary groups of equal mass and depth would need the same extra.
  Bullet-type offsets would follow the deepest potential, not the hosted state.
- **What the near miss would need first.** It would need the bright M31 dSphs to split at about 3e5 M☉. Their own scatter,
  χ²/N 10.8 in X1, does not support that.

## Checks: 6/6 PASS (exit 0, 1.1 s, 0.12 GB, one thread)

| check | result |
|---|---|
| K0 | every row's E/Z equals the printed README/.out value (0 mismatches, both footings; A2) |
| K1 | 9/9 independent recomputations: TDG / DF2-DF4 isolated-law means to 1.2e-4; terciles n 109/108/109 and medians 3.305e12 / 1.1668e13 / 2.9232e13; SPARC split 68/107; UMa 28. Reported (A2): X1 plain vs bootstrap medians differ by up to 0.133 dex (M31 others); no label changes |
| K2 | oracle 10^−E_raw separates on both footings (positive control) |
| K3 | synthetic tables: SEPARATES / FAILS / SEPARATES, NOT GRADED |
| K4 | law round trip 2.2e-16; σ(1 keV) 399.6 km/s (A1); β-model identity |
| K5 | 0.118 GB |

**MUTATE** (`X19_MUTATE=1`) swaps E/s/Z between the ultra-faints and the LG field dwarfs, and between T1 and T3. **K0 FAILS**
(12 mismatches) and **K2 FAILS** (the oracle no longer separates on either footing), as required. Result: 4/6, exit 1;
verdict UNDECIDED (stop rule). Outputs `*_MUTATE.*`.

## What this does not show

- **Only axis-aligned thresholds on catalogue variables were tested.** A selector built from a derived combination (for
  example CFG939's V_rel/v_esc, or a history variable) is not excluded.
- **V is read at each class's measurement radius.** The intervals are 16–84 % of members. Single systems (Crater II,
  Antlia II, the MW) and DF2/DF4 (N = 2) are points or min–max.
- **The cluster rows carry assumptions.** They use F1's β-model and f★ = 0.20. Their e is X2's band, and their N_orb uses
  13.8 Gyr (an upper bound). KT is available for only about a third of them.
- **f_hot = 0 outside clusters is "by catalogue".** A hot CGM is not in the record's baryon inventories.
- **The labels are at 1–3σ for several hosted classes.** Bright M31 (Z 2.70 / 2.34) and M31 others (2.28 / 2.07) are EXTRA
  only narrowly. If they dropped to AMBIGUOUS, M_b would still fail on the ultra-faints.
- **Not blind.** The E values were read while writing the criteria (ledger). Amendment A2 fixed check code after the first
  run. The rank-test numbers are identical with and without it.

## Suggested next step

There is no single selector to build an action around. The data ask for at least three ingredients:
- something that makes compact hosted dwarfs heavy but not diffuse or tidal ones;
- something that switches on between 4e12 and 1e13 M☉ of cluster baryons (T1 vs T2);
- a cosmic dust from z ≈ 1100.

The cheapest decisive test is a **per-system rank test inside the hosted dwarfs**, on X1's 89 systems against B_iso and
B_EFE, with CFG939's V_rel/v_esc,bar and x/e as the frozen candidates. This would settle whether the dwarf side has any
one-variable ordering at all before the cluster side is joined to it. In parallel, the cluster split should be retested
with the full eRASS1 KT subsample (106 clusters with KT) binned by KT rather than MGAS500, to remove the by-construction
part of the mass ordering.

## Files and commits

- `FROZEN_CRITERIA.md` and `ASSUMPTION_LEDGER.md` (8960ea2285); `AMENDMENT_A1.md` (0fc9bade54); `AMENDMENT_A2.md`
  (result commit).
- The script `x19_selector_rank_test.py`, with its outputs `x19_selector_rank_test.out`, `_results.json` and
  `x19_classes.csv`, plus the matching `*_MUTATE.*` files.
- Run: `OMP_NUM_THREADS=1 PYTHONHASHSEED=0 nice -n 15 python3 x19_selector_rank_test.py` (and with `X19_MUTATE=1`).
- No downloads. Inputs are read-only from P4, X1, S1, U1, X7, X2, CFG657, CFG695, SPARC, Chae's environments, Tian+26 and
  eRASS1.
