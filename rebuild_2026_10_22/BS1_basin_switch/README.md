# BS1_basin_switch: the CL2 switch keyed on the gravitational basin

## Provenance

- **Criteria:** `FROZEN_CRITERIA.md` (aabf665e07, committed alone).
- **Amendments:** `AMENDMENTS.md` A1–A11 (efc77e8136, committed alone, before the script and before any BS1 number).
- **Harnesses:** executed read-only as text copies.
  - CL2 (b57ed8751f) / CL3 (47625a9db2): X43, X53 and X51.
  - HO2 (MW: GD2's X5 box, GD1's McMillan point).
  - HO3 (S1–S3 rules).
  - CFG548 (UNGC frame and selection) and CFG522 (MW/M31/M33/LMC baryons).
  - The record's `match_kt2017_host` on Kourkchi & Tully 2017.
- **Run:** `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I bs1_basin_switch.py`

**Run conventions.**
- κ = ½ FITTED. Footings 9.3603e-11 (canonical, primary) and 1.1312e-10 m/s² (alt) are never pooled.
- Cold dark energy is a gravitating w ≈ 0 field component, not matter and not a particle. ΛCDM appears only as the rival;
  no ΛCDM number enters a rule.
- **The basin is a posit:** nonlocal, with no action written.
- Not "theory closed". Nothing here says the data favour the framework.

## Verdict (frozen rule)

| footing | verdict | A calibration kept | B MW fixed | C field holds |
|---|---|---|---|---|
| **canonical (primary)** | **BASIN SWITCH RESOLVES THE MW CONTRADICTION** (field dwarfs fail S3; \|Z\| ≥ 2: IC 1613 −7.62) | yes | yes | **no** |
| alt (reported) | BASIN SWITCH FAILS: SPARC line, dwarfs MW ultra-faint (OVER, Z −2.77), field dwarfs (S3) | no (CL2's known alt lines) | yes | no |

**Reading.** Keyed on the basin, the switch removes the mass contradiction:
- The Milky Way gets a cold dark energy halo through the Local Group, and every calibration line still passes on
  canonical.
- It does not fix the field dwarfs one by one. IC 1613 was already 6.8σ below the law (stated in advance); with the LG
  halo it falls to 7.6σ below.
- Leo T and Phoenix, which sat above the law in HO3, become consistent.

The pass rests on a thin margin and on wide MW priors:
- **LG margin:** log M_basin = 12.39 against T = 12.3. The big four alone give 12.37 and the summed-baryon variant 12.35.
- **MW priors:** the box is feasible only under wide priors (the short disc, R_d 1.93), not in the priors.

## The Local Group basin (rule a)

- **R0_data:** CFG548's frame (f31 = 2/3) and frozen selection (N = 27; it reproduces CFG548's committed sample).
  - The straight-line fit gives V_r = 89.0 km/s/Mpc × (R − R0), rms 42.1 km/s.
  - **R0_data = 794.7 ± 151.5 kpc** (bootstrap of 400, seed 20261027).
  - This is model-free, not CFG548's model-based 830 kpc.
- **Membership:** 70 UNGC rows lie inside R0_data.
  - 69 carry a mass; And XXX has no KLum and is skipped, so the mass is a lower bound.
  - MW, M31, M33 and the LMC are all inside.
- **Mass:**
  - log M_basin = **12.3925**, against 12.3, so the LG takes **route E**.
  - Own log M200 (EM1 A relation, CFG522 baryons): MW 11.880, M31 12.151, M33 11.093, LMC 10.709. The big four sum to
    12.371.
- **Satellites:** their flag is recovered (rule f). It is unchanged from CL2, so HO3's satellite grade is carried. The
  re-run gives the same EXCESS SCATTER (S1, S2, S3) as HO3.

| field dwarf | R (kpc) | in LG at R0 − 1σ (643) | at R0 (795) | at R0 + 1σ (946) |
|---|---|---|---|---|
| Pegasus dIrr | 415 | yes | yes | yes |
| IC 1613 | 467 | yes | yes | yes |
| Cetus | 620 | yes | yes | yes |
| Phoenix | 659 | no | yes | yes |
| NGC 6822 | 707 | no | yes | yes |
| Leo T | 754 | no | yes | yes |
| WLM | 818 | no | no | yes |
| Aquarius | 961 | no | no | no |
| Leo A | 1023 | no | no | no |
| Tucana | 1150 | no | no | no |
| Sagittarius dIrr | 1184 | no | no | no |
| UGC 4879 | 1331 | no | no | no |
| Antlia B | not in UNGC (A5: alone) | no | no | no |

Placing Antlia B at NGC 3109's position (R ≈ 1.3 Mpc) changes nothing.

## SPARC basins (rule b) and the galaxies whose flag changed

- **Inputs:**
  - 175 galaxies. 165 have a position (the record's merged NED/SIMBAD file) and 126 have cz.
  - **KT2017 matches: 104.** Of these, 63 sit in groups with Nm ≥ 2.
  - Two of those groups have no Dist and keep their CL2 flag (A3): DDO064 and UGC03546.
  - No SPARC galaxy lies inside R0_data. UGCA444 (WLM) is at 818 kpc.
- **Result:** 13 galaxies change from law to route E, the same set in bg A and bg B.
- **Route-E count:** 22 of 175, against CL2's 9.

| galaxy | own log M200 (bg A) | log M_basin | KT2017 group (Nm) |
|---|---|---|---|
| NGC3917 | 11.297 | 12.520 | 37617 (24) |
| NGC3992 | 12.199 | 12.598 | 37617 (24) |
| NGC4088 | 11.909 | 12.436 | 38795 (17) |
| NGC4100 | 11.656 | 12.405 | 38795 (17) |
| NGC4157 | 11.904 | 12.427 | 38795 (17) |
| NGC5033 | 11.942 | 12.321 | 45749 (20) |
| NGC5907 | 12.137 | 12.395 | 54470 (7) |
| NGC5985 | 12.151 | 12.674 | 55674 (11) |
| UGC02953 | 12.211 | 12.552 | 14508 (15) |
| UGC06917 | 10.987 | 12.394 | 38795 (17) |
| UGC06923 | 10.641 | 12.525 | 37617 (24) |
| UGC06930 | 11.129 | 12.403 | 38795 (17) |
| UGC06983 | 11.017 | 12.526 | 37617 (24) |

Most of these are Ursa Major galaxies, which KT2017 splits into groups 37617 and 38795.

## Tables: canonical primary, alt reported

**(A) Calibration.** Only SPARC and the dwarf classes can move. Groups, clusters and lensing are unchanged by
construction and equal CL2 exactly.

| line | CL2 canonical | **BS1 canonical** | BS1 alt |
|---|---|---|---|
| SPARC bg A rms / U / line | 0.0559 / 0.53 / pass | **0.0569 / 0.53 / pass** | 0.0565 / 0.46 / FAIL |
| SPARC bg B rms / U / line | 0.0563 / 0.53 / pass | **0.0573 / 0.53 / pass** | 0.0569 / 0.46 / FAIL |
| groups Z | +1.99 | +1.99 | +1.98 |
| clusters (15 keys), G-OUT-all Z | all pass, −1.93 | all pass, −1.93 | all pass, −1.93 |
| dwarfs MW ultra-faint | −0.218 (Z −1.91) | −0.218 (Z −1.91) | −0.316 (Z −2.77) FAIL |
| dwarfs bright M31 / M31 others / MW classical | Z −0.73 / +0.09 / +0.24 | same | Z −0.87 / −0.10 / −0.42 |
| dwarfs LG field | (CL2: law) | +0.001 (Z +0.01) | −0.036 (Z −0.59) |
| lensing ENV2H−L2H / ENV2H−H2H | +0.0 / −429.0 | +0.0 / −429.0 | +0.0 / −458.2 |

The alt failures are CL2's own alt lines, unchanged.

**(B) Milky Way (held out).** HO2's X5 box with GD2's lines; the branch comes from the LG basin, so all 175 cells take
route E.

| | canonical | alt |
|---|---|---|
| class | FEASIBLE (WIDE PRIORS ONLY) | FEASIBLE (WIDE PRIORS ONLY) |
| cells passing L1 + L2a + L2b | **13** | 13 |
| cells passing all four | 3 (Σ_b 47.1, R_d 1.93, M_bb 1.88 to 2.12e10) | 3 |
| best cell | V_c 233.5, K_z 68.8, χ²_Kz 29.6, χ²_Ou 48.0 | same |
| McMillan point | route E: V_c 200.1 (z −6.2), K_z 67.2 (z +0.4); L1 fails, L2a and L2b pass | same |

For comparison, CL2 (HO2) gives INFEASIBLE with 0 cells and a McMillan K_z of 92.9 (z +12.0).

**(C) LG field dwarfs (held out, HO3's rules).**

| | canonical | alt |
|---|---|---|
| S1 (\|Z\| ≥ 2 count) | 1 (p 0.45) PASS | 1 PASS |
| S2 (median \|Z\|) | 0.76 ≤ 1.24 PASS | 1.01 ≤ 1.24 PASS |
| S3 (worst object) | **IC 1613 Z −7.62, p 3.4e-13 FAIL** | IC 1613 Z −8.44 FAIL |
| **Leo T** (halo) | −0.130 ± 0.154 (Z −0.85) CONSISTENT; HO3 law +0.414 (Z +2.69) | Z −1.26 CONSISTENT |
| **Phoenix** (halo) | +0.130 ± 0.074 (Z +1.75) CONSISTENT; HO3 law +0.405 (Z +5.47) | Z +1.13 CONSISTENT |
| **IC 1613** (halo) | −0.603 ± 0.079 (Z −7.62) BELOW PICTURE; HO3 law −0.535 (Z −6.75) | Z −8.44 BELOW |

## Verifying the failure, and the pass

- **IC 1613 (the C failure).**
  - At R = 467 kpc it is inside R0_data in every variant.
  - It was already 6.75σ below the picture on the law branch (HO3, stated in the criteria). Adding the route-E halo can
    only raise g_pred.
  - S3 fails in every reported variant. The failure is not produced by the basin rule; the rule cannot remove it.
- **The MW pass (B).**
  - It is HO2's MUTATE twin, now reached by the frozen rule rather than by inversion. The writer knew it in advance
    (disclosed in the criteria).
  - It holds only under wide priors. The McMillan point itself still fails L1 (V_c 200).
- **The calibration pass (A).**
  - The 13 switched SPARC galaxies raise the pooled rms by 0.001 dex and leave the median U at 0.53, so the line passes.
  - Every other line equals CL2 to 1e-6.

## Reported variants (not graded)

| variant | LG log M_basin (route E?) | SPARC flags changed | canonical | alt |
|---|---|---|---|---|
| **CL3 one number** (L 3.75, T 12.2357 / 12.5739; lensing carried from CL3) | 12.3925 (canonical yes, **alt no**) | 19 | RESOLVES (all lines pass; MW V+K ONLY, 10 cells) | FAILS: SPARC line, dwarfs MW ultra-faint (UNDER, Z +4.87), M31 others (Z +2.12), MW INFEASIBLE, field S3 |
| Υ_K 0.5 | 12.3906 (yes) | 12 | RESOLVES | FAILS (known alt lines + field S3) |
| Υ_K 0.8 | 12.4013 (yes) | 20 | RESOLVES | same |
| summed-baryon M_basin | 12.3457 (yes) | 12 | RESOLVES | same |
| literal all-Ks self term (A2) | 12.3925 (yes) | 12 | RESOLVES | same |
| groups without Dist take the SPARC distance | 12.3925 (yes) | 13 | RESOLVES | same |
| R0_data − 1σ (643 kpc) | 12.3918 (yes) | 13 | RESOLVES (field \|Z\| ≥ 2: IC 1613, Phoenix +5.47, Leo T +2.69 back on the law) | same |
| R0_data + 1σ (946 kpc) | 12.3927 (yes) | 14 (+ UGCA444/WLM) | RESOLVES | same |
| Antlia B at NGC 3109 | 12.3925 (yes) | 13 | RESOLVES (C as primary) | same |

- **Canonical:** the canonical verdict is the same in every variant.
- **CL3 variant, alt:** the LG falls below its alt threshold 12.574, so the satellites go to the law and the
  ultra-faints come out UNDER.

## Checks: 6/6

- **K0a:** with every basin set to the system alone (satellites keep CL2's clause), every leaf of CL2's committed S9 L4
  grade matches on both footings to 1e-6, and the fail lists are exact.
- **K0b:** HO3's 13 field residuals are reproduced: E to 1e-6, Leo T and Phoenix Z to 1e-6, and the S1–S3 outcomes.
- **K0c:** HO2's MW result is reproduced: INFEASIBLE with identical line counts, McMillan K_z 92.9 (z +12.0), and GD2/GD1
  step 0.
- **K1:** every system's branch equals its basin flag on independent recomputation: 0 violations in 25,096 decisions,
  own M200 deviation 0.
- **K2:** R0_data comes from CFG548's committed selection and the frozen seed; the 104 KT2017 matches are stated.
- **K3:** peak RSS 0.70 GB per process, one thread.
- **Rerun:** the second full run's results JSON is byte-identical (`cmp`). The `.out` differs only in its timing stamps.
- **MUTATE** (`BS1_MUTATE=1`, separate `_MUTATE` outputs): the basin flags are inverted at their source.
  - K0a, K0b and K0c fail, and K1 records 25,096 violations in 25,096 decisions.
  - The run exits 1, with checks 2/6.
  - Its verdict is FAILS on both footings: satellites UNDER (MW ultra-faint Z +5.22), MW INFEASIBLE, field S1 and S3.
- **Shared log:** `bs1_x30_machinery.log` carries no MUTATE tag (X43's own naming), so the twin overwrote it. It is a
  machinery log only.

## Disclosures

- **The basin is a posit:** nonlocal, with no action. KT2017's grouping uses its own luminosity-based radii (a borrowed
  algorithm); only its membership is used, never its masses.
- **Lower bounds:**
  - Members fainter than Ks 11.75 are missed, so M_basin is a lower bound.
  - KT2017 L_K uses M_K,⊙ = 3.28 with no extinction correction.
  - The F2 cold-gas relation is used only in its lens range (A1).
- **Unchanged by construction** (stated in advance):
  - KiDS isolated lenses, groups, clusters and SLUGGS.
  - HO1's hot-gas sign failure and HO2(a)'s SLUGGS failure stand.
- **Held out, but not blind:** the writer knew HO2's MUTATE MW result and HO3's field residuals. The rule was fixed from
  the geometry, so weight B and C accordingly.
- **Amendments** A1–A11 are in `AMENDMENTS.md`.
- **Crash fix:** the first full run crashed when a variant label containing "/" was used in an output filename. The fix
  changed only how filenames are built, not any rule. The results above come from the complete runs after it.

## Files

- `bs1_basin_switch.py`
- `bs1_basin_switch.out` and `bs1_basin_switch_results.json`
- The `_MUTATE` twins of the above
- The per-run copy outputs: `bs1_x43copy_*`, `bs1_x51copy_*`, `bs1_x53copy_*` and `bs1_x30_machinery*.log`
