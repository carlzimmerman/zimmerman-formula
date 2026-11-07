# UA1: SE2's two fragile rows. Coma UDGs drop to NOT A TEST; groups stay NOT EXPLAINED

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. No particle. No LCDM input. Footings graded separately, never pooled.

- Criteria: FROZEN_CRITERIA.md (9b5b06f1d5), committed alone before any script or number.
- Script: ua1.py. It execs se2.py read-only (writes go to a temp dir outside the repo) and reuses SE2's loaders, seeds,
  priors, statistics and label rule. One thread, about 5 s, peak RSS 0.78-0.94 GB (under 1 GB).
- Outputs: ua1.json / ua1.out (main and known answers), ua1_MUTATE.json / ua1_MUTATE.out (MG, MA). Run main first,
  because MUTATE reads ua1.json. Reruns give identical files apart from the peak-RSS line.

## Labels (both footings agree in every graded row)

| Class | canonical | alt | Class label |
|---|---|---|---|
| **groups** (full budget, single widths) | +0.259, 95 % [+0.052, +0.459] -> NOT EXPLAINED | +0.221, 95 % [+0.009, +0.415] -> NOT EXPLAINED | **NOT EXPLAINED** |
| **Coma UDGs** (A1 + A2 + A3 pericentre) | 2 of 9 admissible -> NOT A TEST | 2 of 9 -> NOT A TEST | **NOT A TEST (admissible N < 5)** |
| bright M31 (same cut, 15 of 25) | +0.312 [-0.141, +0.772] EXPLAINED | +0.298 [-0.160, +0.761] EXPLAINED | EXPLAINED |
| MW classical (7 of 8) | no power | no power | NOT A TEST |
| LG field (control, no host term) | no power | no power | NOT A TEST |
| MW ultra-faint (reported only, 29 of 31) | +0.603 [+0.003, +1.215] NOT EXPLAINED | +0.587 [-0.013, +1.197] EXPLAINED | SPLIT (reported only) |
| M31 others (reported only, 5 of 5) | no power | no power | NOT A TEST |

**Reading: one row drops, one stands.** The Coma UDG row drops to NOT A TEST, as expected in the criteria. The groups row
stands as NOT EXPLAINED, also as expected. So the residue does **not** collapse to X-COP + CMB lensing. It is
**X-COP + groups + CMB lensing**. The hot-system step stays on the group-and-cluster scale (about 1e13 to 1e15 Msun),
not the cluster scale alone.

## Groups: what the full budget does

The new knobs, each added alone on top of SE2's budget (reported, canonical / alt, median and 95 %):
- **Non-thermal pressure** (NGC 5044 class), b_nt ~ U[0, 0.20]: +0.280 [+0.113, +0.426] / +0.242 [+0.078, +0.387].
  This raises the step, because the hydrostatic mass reads low.
- **Distance scale** d_f ~ U[1, 0.70/0.674]: +0.221 / +0.184. This lowers the step by about 0.01 dex.
- **Clumping** c_g ~ U[1, 1.1]: +0.220 / +0.183. This lowers it by about 0.01 dex.
- **Cross-catalogue dataset term**, m_G = 0.064 dex: +0.234 [+0.033, +0.419] / +0.196 [-0.004, +0.381]. On its own this
  term reaches 0 on alt.
  - The term is built from 7 groups matched to Eckmiller+2011 (NGC4936, HCG62, NGC1132, IC1633, NGC4325, NGC6338,
    IC1262).
  - log10(M500 L15 / E11) has a mean of +0.042 and an rms of 0.126.
- **Membership / interloper:** NOT APPLICABLE. Lovisari+2015 masses are X-ray hydrostatic, so there is no member-galaxy
  velocity step. Member stars enter through f* only.

Joint result: the medians move **up** against SE2 (+0.232 -> +0.259 canonical, +0.194 -> +0.221 alt). The 95 % intervals
widen but stay clear of 0.

**Checking the fail as hard as a win (none of these decides the label):**
- **The alt margin is thin.** Its 95 % lower edge is +0.009 and P(s <= 0) = 0.021. Canonical is +0.052, with P = 0.007.
- **Doubled widths reach 0:** [-0.122, +0.597] / [-0.170, +0.559]. The criteria froze SINGLE widths before the run (SE2's
  +-1 sigma reading is already the generous one), so this does not change the label.
- **A symmetric non-thermal term reaches 0:** with b_nt ~ U[-0.2, +0.2], CFG34's way of carrying it, the intervals are
  [-0.008, +0.432] / [-0.049, +0.392]. No source on disk gives b_nt < 0 for groups. The frozen sign is physical.
- **MG (inverted sign, b_nt <= 0) bites.** The median drops by 0.088 / 0.087 dex, and the row would read EXPLAINED. The
  groups label depends on the non-thermal sign being physical. It is the most sign-sensitive row in the record.

## Coma UDGs: the pericentre cut

- **No orbit or proper motion exists on disk for any of the 9 UDGs.** So r_p = d_mean/3, the record's no-PM convention
  (X20 A3, UX4 T3, ST1 / SE2), and A3 is evaluated in S1's Coma beta-model field at r_p.
- **tau at d_mean -> tau at d_mean/3:** 0.17-0.33 -> 0.32-0.63. Only J130005.40+275333.0 (0.319) and J130038.63 (0.322)
  pass the 0.375 line. That is 2 of 9, NOT A TEST.
- **The cut is symmetric.** On the dwarf classes the same A3 removes:
  - bright M31: 6 (Andromeda II, IX, XV, XXI, XXIII, Cassiopeia III), leaving 15 of 25, still EXPLAINED;
  - MW classical: Sextans;
  - MW ultra-faint: Grus I.
  - MW ultra-faints use 31 Z2 PM pericentres. No PM pericentre exists on disk for MW classical or M31 systems, so they use
    d/3.
- **MA (inverted admissibility) bites on both footings.** The 7 removed UDGs, graded alone, read NOT EXPLAINED:
  +1.023 [+0.419, +1.644] / +0.977 [+0.354, +1.601]. The 10 bright M31 systems removed by A1 or A3 together show no step
  (+0.023 / +0.011, no power). In the dwarfs the step sits in the systems that are safe at pericentre. In Coma the 7
  pericentre-exposed systems carry the full step; the 2 safe ones are too few to grade.
- **Post-freeze sensitivity (reported only, decides nothing).** The label rests on the d/3 convention, not on a measured
  orbit:
  - admissible N against d_mean/r_p: 1.5 -> 7, 2 -> 6, 2.5 -> 3, 3 -> 2, 4 -> 2, 5 -> 1;
  - the per-UDG break-even d/r_p is 1.23 to 5.82;
  - with pericentres at d/2 or wider, 5 or more UDGs would be graded. Those cells were not computed.
- **What NOT A TEST says.** On the record's orbit convention, the class cannot show that it is in equilibrium, so it
  cannot test the law. It does **not** say that systematics explain the UDG step. SE2's NOT EXPLAINED at the present
  position (+1.12 / +1.08 dex) is unchanged.

## Known answers and MUTATE

| Check | canonical | alt | line |
|---|---|---|---|
| KA0: se2.py exec'd read-only vs committed se2.json (1576 numbers + 337 strings) | 0 numbers differ; 1 string-list leaf differs (Amendment 1) | (both inside) | PASS after Amendment 1 |
| KA-G: new knobs pinned vs SE2's groups posterior | array_equal, summary == se2.json | same | PASS |
| KA-U: A3 off vs SE2's dSph / UDG cells | 6/6 equal | 6/6 | PASS |
| KA-beta: g_beta(d_mean)/a0 vs S1 x_e_dmean | 0.0 (S1's a0) | 0.0 | PASS after Amendment 2 |
| MG: inverted non-thermal sign | median -0.088 | -0.087 | must bite (>= 0.03): **BITES** |
| MA: inverted admissibility, Coma | NOT A TEST -> NOT EXPLAINED (N 7) | same | must bite: **BITES** |

## Disclosed

1. **Amendment 1 (2026-11-07, post-freeze).** KA0 as frozen required every string to be equal. One leaf differs:
   CMB_row/SE1_on_disk, SE2's directory listing of SE1 results. SE1 landed after SE2 ran, so the listing is now
   non-empty. It is record state, not a computed value. KA0 was re-read as "every other leaf equal". All 1576 numbers are
   equal, and SE2's CMB label is unchanged.
2. **Amendment 2 (2026-11-07, post-freeze).** KA-beta as frozen compared against the a0 carried by the SE2/GB1 namespace.
   That is the record's full-precision value (9.360324825e-11 / 1.1312035414e-10), while S1 divided by its rounded a0
   (9.3603e-11 / 1.1312e-10). With the full-precision a0 the difference is 2.8e-6 / 2.7e-6. With S1's a0 it is 0. The A3
   cut uses g_beta directly and no a0, so neither label moves.
3. Both amendments were made after the first main run had printed labels. No label depends on either, and no label
   changed between runs.
4. **The Coma sensitivity table** (N against d/r_p, break-even) was added after the first run. It is reported only.
5. **The Eckmiller+2011 values are a transcription** inside deepseek_push/G125_group_equipartition.py, marked
   UNVERIFIED-in-repo there, so they are PROVISIONAL here. Lovisari's M500 and Eckmiller's M500 are each at their own
   R500.
6. **Not in the groups budget:** T-profile extrapolation (QX30 G3, either sign, not computable); per-point eM (it would
   double count the bootstrap); the XMM vs Chandra T calibration (it has the wrong sign).
7. **Not blind.** SE2, ST1, GB1, S1, QX30, the Lovisari table and the E11 list were read before the freeze.
8. **The data mount for the KiDS loader.** GB1's KiDS loader needs gitignored Brouwer+2021 files that exist only in the
   main checkout. They were linked read-only into the temporary worktree for the run and are not committed.
9. **MW ultra-faint reads SPLIT under the cut.** This row is reported only (as GB1 / SE2), and its 95 % edges are
   +0.003 / -0.013.

Kappa = 1/2 FITTED; not theory closed.
