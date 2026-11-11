# HIS1 RESULT: the history reading, on DD1's frozen table (2026-11-10)

Criteria 152ecaf5c4 (committed alone, before any script or number). Data: DD1's frozen table (origin f86496a251),
unchanged. TEST lane, quarantined: adopts nothing, relabels nothing, registers nothing. Footings never pooled. No
amendment. One post hoc addition, reported only: a MUTATE arm and one count, both marked below. Origin ids: see the last
section.

## Label

**HOLDS EXCEPT H3 (fails), H5 (no power) / HOLDS EXCEPT H3 (fails), H5 (no power)** (canonical / alt).

- **The force reading** (every system on the plain law now) **scores 1 of 5** on the same tests, on both footings.
- **No rule** (class labels shuffled) holds 1 of 4. The one that holds is H2, which barely depends on labels.
- **Checks.** Every known answer passes. MUTATE M1, M3 and M4 bite. M2 does not bite as frozen (disclosed below), and a
  post hoc M2b bites. `HIS1.lean` compiles (4 theorems, standard axioms); its false twin fails with 3 errors.

The reading under test: the non-baryonic mass is real and conserved, and its amount was set by the law when a system
formed. Since then a system can only lose non-baryonic mass (stripping), which moves it below the law but never below
X = 0. Or it can lose baryons, which moves it above the law. In short: the data sit where a history allows, with one
class too low for an undisturbed system and no trend inside any class.

| test | required (frozen) | obtained, canonical / alt | history | force reading on the same test |
|---|---|---|---|---|
| H1 tidal dwarfs carry none | median Y within 2 se of 0, and d_L more than 3 se below the law | Y +0.067 +- 0.115 (0.6 se from X = 0); d_L -0.687 / -0.725 +- 0.115 (6.0 / 6.3 se below) | **HOLDS** | F1 fails: the dwarfs are 6 se off the law |
| H2 nothing below X = 0; DF2 / DF4 between Newton and the law | at most 3 systems below X = 0 beyond 3 e; no class below; DF2 and DF4 in [0, law] within 3 e | 0 systems below; no class below; DF2 Y +0.13, d_L -0.74 / -0.78; DF4 Y -0.10, d_L -0.94 / -0.98 (e 0.34-0.35) | **HOLDS** | F2 fails: 12 / 15 systems sit below the law beyond 3 e (DF2 / DF4 alone are within 3 e of it) |
| H3 undisturbed on the law; isolated never below; baryon-losers at or above | SPARC, its gas-rich half and the UNGC-isolated faint rotators within 3 se of the law; isolated sets not below; baryon-losers not below | SPARC +0.004 / -0.023 +- 0.012; gas-rich half +0.026 / -0.010 +- 0.021; **isolated faint rotators -0.278 / -0.315 +- 0.080 (3.5 / 3.9 se below)**; every other set passes | **FAILS** on the faint rotators | F3 fails: off the law are the isolated faint rotators, ATLAS3D, the ultra-faints, the groups and DF2 / DF4 |
| H4 closed systems hold the whole (RB1, no a0) | X-COP's edge X consistent with 5.41; at or below it inside the edge; groups above it | X-COP last radius X 4.94 [4.30, 6.11]; at R500 5.12 (f_ret 1.057 [1.046, 1.072]); groups X 9.07 [8.49, 9.73] | **HOLDS** | F4 fails: X-COP's last points sit +0.15 / +0.12 +- 0.012 dex above the law |
| H5 the offset tracks history | at least one of six Spearman pairs significant (Holm) in the history's direction, none against it | none significant: gas fraction SPARC rho +0.01 / -0.03, faint rotators +0.11; host distance MW bright -0.55 (p 0.08), ultra-faints -0.21, M31 -0.01, Coma UDGs -0.39 | **NO POWER** | F5 passes (the force reading predicts no trend) |

**In plain words.** Four of the five statements the history reading makes are met: the tidal dwarfs at Newton, nothing
below Newton, the closed and open hot systems on the right sides of 5.41, and the hosted and gas-poor classes at or above
the law. The force reading meets one of the five. The history reading misses twice.

- **The isolated faint gas-rich rotators sit about 0.3 dex below the law.** That is beyond errors at the frozen line.
  A system that has lost nothing should not sit there. The miss is not robust to a coherent distance error: if every
  distance were 20 % smaller, it would be 2.3 / 2.7 se.
- **Inside a class, nothing tracks a measured sign of history.** All four host-distance pairs lean against the history's
  direction: closer dwarfs read higher, not lower. None is significant.

## The numbers that carry it

**H1.** The lead's arithmetic is right. For the six tidal dwarfs, X = 0 gives an offset of -0.75 under the law
(canonical); they read -0.69. The record already had this:
- CFG936: -0.690 +- 0.078 below the law, +0.055 +- 0.114 against Newton. It found that zero supply explains them.
- G2: +0.083 +- 0.096 against Newton, reproduced here exactly as KA2.

**H2.**
- No system of the 626 reads below X = 0 beyond three of its own errors, and no class median does.
- DF2 and DF4 sit between Newton and the law, but with errors of 0.34 dex. They are also within 3 e of the law, so the
  force reading's F2 passes them alone.
- The record on how they got there:
  - G2: neither is stripped at its projected distance; that would need a pericentre at or inside 24 / 21 kpc.
  - NH2 (scope: present-day tides at the projected distance, under form B): NGC 1052 cannot hold what today's tides on
    DF4 need. That is TIDES CANNOT REACH under its post hoc reading, NO VERDICT as frozen. DF2 is not decided.
  - A past close passage is not covered by either lane.
- **POST HOC (reported, grades nothing):** with ATLAS3D at Salpeter (DD1's bracket rows), 1 of 187 early types reads
  below X = 0 beyond 3 e. The class median Y is -0.047 +- 0.011, which is 4.3 se below X = 0, and H2(b) forbids that. So
  H2's hold for early types rests on a Chabrier-like IMF.

**H3.**
- **Isolation of the faint rotators.** 13 of the 20 in the table match a UNGC tidal index; 9 of those have Ti1 < 0
  (isolated) and 4 do not (DDO53 +0.8, DDO126 +0.4, AGC229053 +0.1, WLM 0.0). The 7 unmatched are 6 SHIELD AGC
  galaxies and F564-V3.
- **Do the faint rotators' offsets survive their mass-to-light and distance errors?**

| subset | as measured | M_* x 2 | M_* x 0.5 | distances x 0.8 | distances x 1.2 |
|---|---|---|---|---|---|
| all 20 (canonical) | -0.24 (-5.3 se) | -0.32 (-7.3) | -0.20 (-4.7) | -0.14 (-3.2) | -0.32 (-7.1) |
| isolated 9 (canonical) | -0.28 (-3.5) | -0.35 (-4.2) | -0.23 (-3.0) | -0.18 (-2.3) | -0.36 (-4.5) |
| isolated 9 (alt) | -0.32 (-3.9) | -0.39 (-4.6) | -0.27 (-3.5) | -0.22 (-2.7) | -0.40 (-4.9) |

  - Their gas dominates the baryons, so M_* barely matters.
  - A coherent 20 % distance cut brings the isolated nine inside 3 se on both footings. Per-galaxy distance errors are
    already in their se.
- **The rest of H3 holds** (median d_L, canonical):

| set | median d_L |
|---|---|
| KiDS | +0.14 +- 0.11 |
| LG field dwarfs (stars only, an upper bound) | -0.09 +- 0.06 |
| ATLAS3D outside Virgo | +0.08 +- 0.01 |
| MW bright dwarfs | +0.07 +- 0.15 |
| MW ultra-faints | +0.59 +- 0.10 |
| M31 dwarfs | +0.09 +- 0.09 |
| Coma UDGs | +0.32 +- 0.11 |
| groups | +0.16 +- 0.02 |

**H4** is RB1's gate 1, quoted, not redone. One correction to the lead's wording: in X, a system that lost baryons sits
above 5.41, not below it. The groups read X 9.07. "Below" is true of RB1's retention f_ret = 5.41 / X. Inside the edge
X-COP reads 5.12 at R500, below 5.41 beyond errors, and 4.94 at the last radius, consistent with it. That is the
approach from below that the reading asks for. DD1's own X at the outermost point agrees: X-COP 4.94, groups 9.07.

**H5.** None of the six graded pairs is significant, raw or corrected.
- Gas fraction gives nothing in SPARC (rho +0.01) or the faint rotators (+0.11). This was the only pair that could
  separate the history reading from the force reading.
- The host-distance pairs lean the wrong way for stripping: closer dwarfs read higher. Those pairs do not separate
  history from the law with an external field anyway.
- DG1 found the same inside the hosted dwarfs: rank +0.06 against its predicted gas history in the ultra-faints.
- **Reported, not graded:**
  - ATLAS3D galaxies in Virgo read lower than those outside: +0.031 +- 0.016 against +0.081 +- 0.013, Spearman p 0.006.
  - Among the 31 SPARC galaxies with a UNGC tidal index, more disturbed ones read lower: rho -0.37, p 0.04.
  - Both point the way stripping would. Neither was frozen as a test.
  - CLASH's four merging clusters do not differ from the sixteen relaxed ones: +0.56 against +0.55.
  - The LVD age column is empty on disk.

**Controls.**
- The force reading fails F1 to F4 and passes only F5.
- With labels shuffled (seed 7), H1 and H3 fail, H5 has no power, and H2 still holds. H2 is mostly a statement about
  every system, not about classes.

## What earlier lanes already settled, per class

- **Tidal dwarfs.** At Newton: CFG936 and G2. HIS1 adds only that this is the H1 the history reading needs, on DD1's
  table.
- **DF2 / DF4.**
  - At Newton: CFG936.
  - Not stripped at the projected distance: G2.
  - Today's tides cannot reach DF4 under form B: NH2, post hoc reading; DF2 is open.
  - HIS1 adds that both sit between Newton and the law, which the history allows only through a past loss that no lane
    has located.
- **MW ultra-faints and Coma UDGs.**
  - RB2: FAILS HIGH as frozen. DG1: that does not survive the data-side regrade.
  - DG1 also found that counting the gas each dwarf lost brings each class to zero, but per system the residual does not
    follow the predicted history. Its label: HISTORY DOES NOT CLOSE THEM.
  - HIS1 agrees: above the law is allowed for baryon-losers (H3c holds), and nothing inside the class tracks history
    (H5).
- **Groups and clusters.** RB1, quoted as H4.

## What it does not settle

- **It tests consistency with a history, not a mechanism.** It never says how a system would lose non-baryonic mass, or
  why the amount set at formation follows the law.
  - The record's closures stand: COL1 (no route from dust to the static halo), FLD1, LFS1 (a static halo cannot grow),
    and R541 (the 5.41 is an initial condition).
  - Four of the five tests ask only which side of the law a class sits on. Any reading in which the law is a ceiling or
    a floor set long ago passes them.
- **The indicators are incomplete.**
  - Six graded pairs in six classes. No age on disk for the dwarfs.
  - No stripping or tidal index for most systems: UNGC covers only the Local Volume, and none of the clusters.
  - No measured baryon loss for any class, so "above the law by the factor of baryons lost" is untested beyond its sign.
- **Small classes.** Tidal dwarfs n = 6, DF2 / DF4 n = 2 with 0.34 dex errors, isolated faint rotators n = 9, MW bright
  dwarfs n = 11, Coma UDGs n = 11. H1 rests on six systems.
- **IMF.** At Salpeter, the early types read below X = 0 as a class (post hoc count above).
- **Distances.** The faint rotators' H3 failure depends on their distance scale at the 20 % level.
- **The force reading here is the plain law.** The table carries no external field.
  - RB2 notes that an external field would bring DF2 / DF4 down "for free". That could move F2 and F3 for DF2 / DF4
    and the hosted classes. It would not move them for the isolated faint rotators, which have no host field.
  - CFG936 graded the external field FAILS / PARTIAL on these systems.

## What this lane finds in DD1, SHP1 and CLOSURE.md

- **CLOSURE.md, DD1 paragraph.** "The data ... return the law for rotation curves" is SPARC's scope. Not all
  rotation-supported systems on disk sit on the law:
  - the faint gas-rich rotators sit -0.24 to -0.28 (isolated ones included);
  - the tidal dwarfs sit -0.69 (at Newton);
  - RC100 sits +0.09.
- **DD1.** Nothing wrong found. Its "six classes fail every candidate" stands. HIS1 adds that two of those six (tidal
  dwarfs, DF2 / DF4) are fit by X = 0, a value no DD1 candidate could take for one class alone.
- **SHP1.** Nothing wrong found.

## Checks

| check | result |
|---|---|
| KA1 DD1's L0 class offsets | reproduced exactly (deviation 0): PASS |
| KA2 G2's tidal dwarfs | +0.0831 +- 0.0958 equals G2. Table Y vs Lelli's log Mdyn/Mbar within 0.044 dex: PASS |
| KA3 synthetic truths | history truth: H1, H2, H3 HOLD and F1 fails. Force truth: H1 FAILS and F1-F3 pass. Planted gas trend: H5 HOLDS; none: NO POWER. Both footings: PASS |
| KA4 identities | X_L > 0 and X_L <= sqrt(a0/g_bar) on a grid: PASS |
| M1 tidal dwarfs on the law | H1 HOLDS -> FAILS: bites |
| M2 four SPARC galaxies at Y = -0.6 | H2 HOLDS -> HOLDS: **does not bite.** Only 3 of the 4 fall below beyond 3 e (one has e 0.20), and the line allows 3 |
| M2b POST HOC: the same four at Y = -1.0 | H2 -> FAILS (4 below): bites |
| M3 opposite gas trend in SPARC | H5 NO POWER -> FAILS (rho +0.74): bites |
| M4 a0 x 2 | SPARC's d_L -0.102 +- 0.012, H3(a) fails: bites |
| Lean `HIS1.lean` | exit 0. 4 theorems: `XL_pos`, `newton_below`, `XL_le`, `between`. Axioms propext, Classical.choice and Quot.sound only |
| Lean `HIS1_MUTATE.lean` | exit 1. 3 errors, one in each false statement |

**Against the pre-freeze hand estimates.** All held: H1, H2, H4 HOLD, H3 fails on the faint rotators, H5 NO POWER, and
the force reading passes only F5. Not foreseen: the host-distance correlations all lean against the history's sign,
and the faint rotators' failure falls inside 3 se under a 20 % distance cut.

## Files

- `FROZEN_CRITERIA.md`
- `his1.py`, with `his1.json` / `his1.out` and `his1_MUTATE.json` / `his1_MUTATE.out`
- `HIS1.lean`, `HIS1_MUTATE.lean`, `compile.txt`, `compile_MUTATE.txt`

## Commit ids

| | shared checkout | origin |
|---|---|---|
| criteria | 152ecaf5c4 | 0b9421ca2b |
| result | 2ef2d349b3 | c4f8cd2bb3 |

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
