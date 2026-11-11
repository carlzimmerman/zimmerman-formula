# HIS1R READING: how this regrade reads HIS1's frozen criteria (2026-11-10)

TEST lane, quarantined. Adopts nothing, relabels nothing, registers nothing. Footings never pooled (canonical a0
9.3603e-11, alt 1.1312e-10 m/s^2). This note is committed ALONE, before any HIS1R script exists and before any HIS1R
number is computed. The id HIS1R was checked free with `ls -d` only.

Inputs: `fable52_push/HIS1_history_reading/FROZEN_CRITERIA.md` (criteria commit as on disk), DD1's frozen table
`fable52_push/DD1_deduce_from_data/dd1_table.csv`, DD1's `FROZEN_CRITERIA.md` and `dd1_table.py` (column meaning and
build), the indicator source files the criteria name, and RB1's RESULT.md (for H4, which the criteria quote from RB1).

## Exposures before this note (stated in full; the grade below is NOT clean-blind)

1. **HIS1's result was in the context this session started with.** The session context attached automatically at
   start (the repository's recent commit subjects) carried HIS1's result commit messages. Seen before any reading was
   chosen: HIS1's label "HOLDS EXCEPT H3 (fails), H5 (no power)" on both footings; tidal dwarfs Y +0.067 +- 0.115 at
   6.0 / 6.3 se below the law; H3 failing on the UNGC-isolated faint rotators at -0.278 / -0.315 +- 0.080 (3.5 / 3.9 se;
   2.3 / 2.7 se under a 20 % distance cut); X-COP edge X 4.94 [4.30, 6.11], R500 5.12, groups 9.07; force reading 1 / 5
   (only F5); shuffled labels 1 / 4; 626 systems; M2 "does not bite"; ATLAS3D at Salpeter class median X < 0 at 4.3 se.
   This was not looked up; it arrived with the session. It cannot be unseen. Every reading below is chosen from the
   criteria's text; where the text admits two readings, both are graded and the label's dependence is reported.
2. The owner's auto-memory index was loaded into the session context at start (summaries of other lanes; nothing in
   it states HIS1's numbers beyond the commit subjects above).
3. To find the keys KA1 needs, the KEY STRUCTURE of DD1's `dd1.json` was listed (no values printed). The key names
   show which classes DD1's L0 fails (faint rotators, tidal dwarfs, massive spirals, ATLAS3D, KiDS, groups, X-COP,
   CLASH, MW ultra-faints, Coma UDGs, NGC 1052 UDGs, RC100, MW bright dwarfs, M31 dwarfs). No DD1 value was seen.
4. The criteria file itself quotes DD1 and record numbers and the criteria author's hand estimates.
5. While choosing the name-match reading: which of the 20 faint rotators have a UNGC name match (13 match, 7 do not:
   the six AGC galaxies other than AGC229053, and F564v3). No Ti1 value was printed.

Nothing else from HIS1's folder, `CLOSURE.md`, `README.md`, DD1's RESULT.md or DD1's outputs was opened. The sibling
notes `HIS1_handover.md` and `DD1_handover.md` in the shared notes folder were not opened.

## Table and per-system quantities

- Main rows only: `bracket == ''` (3419 points, 16 classes, 626 systems by a structure count; the `atlas_salp` and
  `kids_hot` brackets are reported only). A system is the pair (class, sys): WLM appears in two classes and is two
  systems.
- Per point: Y = lgo - lgb; X_L = (sqrt(1 + 4 a0 / g_bar) - 1) / 2; Y_L = log10(1 + X_L); d_L = Y - Y_L.
- Per system: Y_sys = median of Y over its points; d_L,sys = median of d_L over its points; e_sys = median of its
  finite eY (DD1's rule). A point with g_obs <= 0 (KiDS) keeps Y = d_L = -inf; the median keeps it (DD1: "medians
  handle it"). ALT-INF: drop those points before the median.
- Class (or subset) statistic: the median over its systems of the quantity being tested; se = max(1.2533 x 1.4826 x
  MAD / sqrt(n), sqrt(sum e_sys^2) / n) for n >= 2, with MAD = median |v - median(v)| of the SAME quantity whose
  median is taken; se = e_sys for n = 1. The same e_sys is used for Y and for d_L (DD1's rule: a0 carries no error).
  ALT-ERR: for d_L, e_d = sqrt(max(eY^2 - e_lgb^2, 0) + (1 + s)^2 e_lgb^2) per point, s = dY_L / dlgb (the law term
  absorbs part of the g_bar error); e_sys then the median of e_d.
- "x se" thresholds are read as offsets in units of that se: "median d_L < -3 se" means median < -3 x se.
  Inequalities are used exactly as written (strict where written strict).

## Indicators (read from the files the criteria name)

- SPARC f_g = 1.33 MHI / (0.5 L36 + 1.33 MHI), from `SPARC_Lelli2016c.mrt` (L36 and MHI columns), the 149 galaxies in
  the table, matched by file name.
- Faint rotators f_g = 1 - 10^(logMstar - logMbary), McQuinn t1, by name.
- Ti1 (UNGC, `ungc_karachentsev2013.tsv`): name match after upper-casing and keeping only letters and digits, with the
  criteria's aliases (DDO99 -> DDO099, DDO53 -> DDO053, SextansA/B -> SexA/B) and no others. A system with no match,
  or a blank Ti1, has no Ti1. "Isolated by UNGC" = Ti1 < 0 (strict; Ti1 = 0.0 is not isolated).
  ALT-ISO1: Ti1 <= 0. ALT-ISO2: faint rotators with no UNGC Ti1 counted as isolated (not shown to have a host).
- LVD (`dsph/lvd_dwarf_*.csv`, by `name`): MW bright and MW ultra-faints use `distance_host`; M31 dwarfs use
  `distance_host`, else `distance_m31`. Missing -> the system leaves that pair. `age` reported.
- Coma UDGs `dmean_kpc` (Freundlich+22), by name. ATLAS3D `Virgo` flag, by name; "outside Virgo" = flag 0 (a missing
  flag is not outside). CLASH high-magnification flag = the four clusters under "High Magnification" in Umetsu+16
  table 1. Tidal dwarfs D_p and (M_atom + M_mol) / M_bar from Lelli+15's csv. Massive spirals f_g = M_gas / (M_* +
  M_gas) from Di Teodoro+23 (logMs_W1, logMgas). LG field dwarfs mass_HI (LVD) and Ti1 (UNGC). All "reported" items:
  Spearman rho and p printed, never graded.

## Tests (per footing; Y-only clauses are the same on both)

- **H1** (tidal dwarfs, 6 systems): |median Y_sys| <= 2 se(Y) AND median d_L,sys < -3 se(d_L). HOLDS iff both.
- **H2** (a) count over all 626 systems of Y_sys < -3 e_sys; holds iff <= 3. (b) every one of the 16 classes has median
  Y_sys >= -3 se (classes only, not subsets). (c) DF2 and DF4 each: Y_sys >= -3 e_sys and d_L,sys <= +3 e_sys. HOLDS
  iff (a), (b), (c). ATLAS3D at Salpeter (bracket) reported for (a) and (b), not graded.
- **H3** (a) |median d_L| <= 3 se for: SPARC (149); SPARC with f_g >= 0.5; faint rotators with Ti1 < 0.
  ALT-HALF: SPARC's gas-rich half = f_g above the SPARC median f_g. (b) median d_L >= -3 se for SPARC, KiDS (4 bins),
  LG field dwarfs, faint rotators with Ti1 < 0, ATLAS3D with Virgo = 0. (c) median d_L >= -3 se for MW bright, MW
  ultra-faints, M31 dwarfs, Coma UDGs, groups. HOLDS iff (a), (b), (c). An empty set counts as not failing and is
  named. Reported: the faint rotators' isolated fraction (of all 20 and of those with a Ti1); the isolated set's and
  the whole class's offset with M_* x 2 and x 0.5 (g_bar from M_bar + (k - 1) M_*, M_* and M_bar from McQuinn t1) and
  with distances x 0.8 and x 1.2 coherent (g_bar fixed, g_obs x 1/f, so d_L shifts by -log10 f; e unchanged).
- **H4** quoted from RB1's RESULT.md, no a0: X-COP last-radius f_ret 95 % interval contains 1; X-COP at R500 f_ret >= 1;
  groups' f_ret upper bound < 1. HOLDS iff all three. Beside it, from the table: class median X = 10^Y - 1 at each
  system's `last` point (X-COP, groups, every class), with the se rule applied to X.
- **H5** Spearman rho (average ranks for ties) of d_L,sys with the indicator for G1 SPARC f_g (-), G2 faint rotators
  f_g (-), G3 MW bright distance_host (+), G4 MW ultra-faints distance_host (+), G5 M31 dwarfs (+), G6 Coma UDGs dmean
  (+). Systems with a missing indicator leave the pair. p two-sided from scipy's `spearmanr` (t approximation); a pair
  with n < 3 or an undefined rho has p = 1. Holm step-down over the six at 0.05. HOLDS iff at least one Holm-rejected
  pair has rho with the history sign and none has the opposite sign; FAILS iff any Holm-rejected pair has the opposite
  sign; NO POWER iff none is rejected. ALT-P: permutation p (20000 relabellings, seed 11) in place of the t approximation.

## Controls

- **Force reading**, five items: F1 tidal dwarfs |median d_L| <= 2 se. F2 count of d_L,sys < -3 e_sys over all 626
  systems <= 3, AND DF2, DF4 each |d_L,sys| <= 3 e_sys. F3 |median d_L| <= 3 se for every H3 set ((a), (b), (c) lists);
  "every hosted class" is read as the (c) list, already inside. ALT-HOST: F3 also takes tidal dwarfs and NGC 1052
  UDGs. F4 X-COP's `last` points: class median d_L within 3 se of 0. F5 no G pair Holm-rejected. Score = passes of 5.
- **No rule**: systems in table order of first appearance; class labels permuted by
  `numpy.random.default_rng(7).permutation(626)` (system i takes the label of system perm[i]); every indicator, the
  Virgo flag, Ti1 and the DF2 / DF4 identity of the H2 (c) clause travel with their systems: H2 (c) is applied to the
  systems carrying the "NGC 1052 UDGs" label; a subset defined by an indicator takes the systems in the labelled class
  that carry that indicator. H1, H2, H3, H5 re-run; reported as how many of 4 hold. ALT-RNG:
  `numpy.random.RandomState(7).permutation`. Also reported: the count's distribution over seeds 1..200.

## Labels (per footing), as the criteria state them

THE HISTORY READING HOLDS ON EVERY TEST (H1-H5 HOLD); HOLDS EXCEPT (at most one FAILS, others HOLD or NO POWER; named);
FAILS (two or more FAIL); NO VERDICT (a known answer fails). "By how much" = the failing clause's offset in dex and se.

## Known answers

- KA1: per class, the median of d_L,sys over all its systems vs `dd1.json` `runs/<footing>/L0/LOCO/<class>/off`, to
  1e-9, both footings. The code prints only the largest absolute difference and the pass flag; no DD1 value is printed.
- KA2: inverse-variance mean of log10(Mdyn_over_Mbar) with e = e_Mdyn_over_Mbar / (ratio ln 10) from Lelli+15's csv vs
  +0.083 +- 0.096 to 1e-3 (ALT: log10(M_dyn / M_bar) with errors from e_M_dyn and e_M_bar, reported). The table's six Y
  vs log10(M_dyn_1e8 / M_bar_1e8) within 0.05 dex each.
- KA3 synthetic, noise free, Y replaced at every real point, se from the real errors: (i) tidal dwarfs, DF2, DF4 at
  Y = 0; MW bright, MW ultra-faints, M31 dwarfs, Coma UDGs at Y_L + 0.3 ("hosted"); every other system at Y_L:
  H1, H2, H3 HOLD and F1 fails (ALT: groups also +0.3). (ii) every point at Y_L: H1 FAILS; F1, F2, F3 pass. (iii) (ii)
  plus d_L -= 0.3 (f_g - class median f_g) at every point of SPARC and the faint rotators: H5 HOLDS; (ii) alone: H5
  NO POWER.
- KA4: X_L > 0 and X_L <= sqrt(a0 / g_bar) on a grid of g_bar 1e-15..1e-6 m/s^2, both footings.
- A known-answer failure gives NO VERDICT for that footing.

## MUTATE (separate outputs `his1r_MUTATE.*`)

M1 tidal dwarfs set to Y = Y_L at each point: H1 FAILS. M2 the first four SPARC systems in table order set to Y = -0.6 at
every point: H2 FAILS (each one's e_sys printed). M3 d_L += 0.5 (f_g - median f_g) at every SPARC point: H5 FAILS.
M4 a0 x 2: H3 (a) fails for SPARC. An M that does not change its outcome is disclosed, not repaired.

## Checks of HIS1R's own (beyond the criteria)

Row, class and system counts. Planted signals per statistic, each graded: H1 (tidal dwarfs at Y = 0 / at the law / at
Y = +0.4); H2 (a) 3 vs 4 planted systems at Y = -5 e_sys; H2 (b) one class moved to median -4 se; H2 (c) DF2 at
-4 e_sys, DF4 at d_L +4 e_sys; H3 a set moved to -4 se and to +4 se; H5 a planted trend with the history sign and with
the opposite sign, in each G pair alone; F4 X-COP last points on the law vs +0.5 dex. Shuffles that should destroy
each signal: indicators permuted within the class (H5 planted trend -> NO POWER in most seeds); class labels permuted
(H1's planted pattern and each H3 set's planted shift should no longer appear in their class); X-COP last-point d_L
permuted with other classes' last points (F4). H2 (a) is a count over all systems with no label to permute; its check is
the 3 vs 4 threshold.

## Not done

No Lean file: KA4 is checked numerically, which is what the criteria require of a known answer. HIS1's Lean theorems
are algebra and do not enter any label.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
