# HLF1 AMENDMENT A1 (2026-11-11; post hoc; committed alone, before any Part A row or any Part B number exists)

Criteria 123947b9dc. Adopts nothing. Footings never pooled.

**Timing, disclosed.** `hlf1_halos.py` has run, and so has its MUTATE file. I have seen: KA-A1 PASS (M_lo = 1e13 Msun/h),
the own counts and r_j in 7 bins up to M_hi = 5.62e14, the own bias in 4 bins (all used), KA-A2 (reported) and KA-A4 PASS,
MA2 (199 against 455: bites) and MA1 (160 against 455: does not bite). No halo-model ratio, f_res, C4, C5 or forest number has
been computed.

**What failed as frozen.** MA1 asked that the z = 0 grid with its cells permuted give at most 10 % of the own count above
M_lo. It gives 160 against 455 (35 %). The arm was mis-specified by me: a permutation keeps every cell's mass, the densest
cell holds 7623 cell masses (3.96e13 Msun/h), and the finder accepts any cell above about 1,500 cell masses as a halo of
M200m >= 1e13 on its own. So a permuted field still holds "halos" between 1e13 and about 4e13 that are single cells. **As
frozen, Part A is NO VERDICT on both footings** (a mutation arm does not bite), and RESULT.md will say so first.

**MA1, restated (chosen before the permuted mass distribution is looked at).** The same permuted grid must give at most
10 % of the own count above 5e13 Msun/h, the first mass above the densest single cell, where an object needs more than one
cell. `hlf1_ma1_check.py` writes `hlf1_ma1_check.json` / `.out` (the permuted catalogue's counts above 1e13, 2e13, 5e13 and
1e14 are reported beside it).

**What the restated arm does not repair.** Below about 4e13 the finder cannot tell a halo from one dense cell. In the run
those cells are halo cores, but the planted known answer used smooth profiles only. RESULT.md reports, beside the Part A
label, the rows with the own list applied only from 5e13 up (inherited below), as a reported bracket.

**Nothing else changes.** No known answer, line, label rule, bin, bias rule or Part B item is altered. Both readings of
Part A (as frozen: NO VERDICT; under A1: the frozen label rules with MA1 restated) are reported.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
