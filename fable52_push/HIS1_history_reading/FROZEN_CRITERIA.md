# HIS1 FROZEN CRITERIA: the history reading, on DD1's frozen table (2026-11-10)

TEST lane, quarantined. Adopts nothing, relabels nothing, registers nothing. Footings never pooled (canonical a0
9.3603e-11, alt 1.1312e-10 m/s^2). Committed alone, before any HIS1 script exists or any HIS1 number is computed. The id
HIS1 was checked free (no folder, no commit subject).

## Question

DD1 (origin 91c159b746) found no single rule. Its breakers go both ways. The lead asks whether that pattern is what a
history allows. The reading under test (form B read with a history): the non-baryonic mass is real and conserved, its
amount was set by the law when a system formed, and since then a system can only (i) lose non-baryonic mass (stripping),
which moves it below the law, never below X = 0, or (ii) lose baryons, which moves it above the law. Against it: the
force reading (every system obeys the law now) and no rule (class labels shuffled). This tests consistency with a
history. It is not a mechanism.

## Data

DD1's frozen table, unchanged: `fable52_push/DD1_deduce_from_data/dd1_table.csv` (main rows; DD1's loaders and
systematics apply). Per system: Y_sys = median of Y = log10(g_obs/g_bar) over its points, e_sys = median of its e_Y
(DD1's rule). The law's value Y_L = log10(1 + X_L(g_bar; a0)); the offset d_L = Y - Y_L, per system the median.
Class statistics follow DD1: median over systems, se = max(1.2533 x 1.4826 MAD / sqrt(n), sqrt(sum e^2) / n), n = 1:
e_sys.

History indicators, read from the source files DD1 cites (stated here before any correlation is computed):

| class | indicator | source | use |
|---|---|---|---|
| SPARC | gas fraction f_g = 1.33 MHI / (0.5 L36 + 1.33 MHI) | SPARC_Lelli2016c.mrt | graded G1 (sign -) |
| SPARC | UNGC tidal index Ti1, Local Volume subset (name match) | ungc_karachentsev2013.tsv | reported |
| faint rotators | f_g = 1 - 10^(logMstar - logMbary) | McQuinn t1 | graded G2 (sign -) |
| faint rotators | Ti1 (name match; aliases DDO99 -> DDO099, DDO53 -> DDO053, SextansA/B -> SexA/B) | UNGC | isolation for H3 |
| tidal dwarfs | projected host distance D_p, gas share (M_atom + M_mol)/M_bar | Lelli+15 csv | reported (n = 6) |
| massive spirals | f_g = M_gas / (M_* + M_gas) | Di Teodoro+23 | reported |
| ATLAS3D | Virgo flag | atlas3d table | reported |
| CLASH | high-magnification (merger) flag | Umetsu+16 table 1 | reported |
| MW bright, MW ultra-faints | distance_host (LVD) | LVD | graded G3, G4 (sign +) |
| M31 dwarfs | distance_host, else distance_m31 (LVD) | LVD | graded G5 (sign +) |
| MW, M31 dwarfs | age (LVD) | LVD | reported |
| LG field dwarfs | mass_HI, Ti1 | LVD, UNGC | reported (their g_bar omits the gas, so d_L is biased up with gas: not graded) |
| Coma UDGs | dmean (3D mean cluster-centric distance) | Freundlich+22 | graded G6 (sign +) |
| groups | none usable (Mgas/M500 is Y itself) | | |
| KiDS, RC100, X-COP, NGC 1052 UDGs | none in the table (n = 2 for DF2/DF4) | | |

Signs from the history reading: gas-poor systems lost baryons, so d_L falls with gas fraction (-); systems closer to a
host were stripped more of their extended non-baryonic mass, so d_L rises with host distance (+). Note: the law with an
external field also predicts d_L rising with host distance (relative to the plain law), so G3 to G6 do not separate
history from the law with its external field; only G1 and G2 do. The plain-law force reading predicts no trend.

## Tests and pass lines (per footing where a0 enters)

- **H1, systems made of baryons alone carry none.** Tidal dwarfs: |median Y| <= 2 se (consistent with X = 0) AND
  median d_L < -3 se (away from the law). Both required.
- **H2, nothing below X = 0; stripped systems between X = 0 and the law.**
  (a) Count of systems with Y_sys < -3 e_sys must be <= 3 (by chance about 0.85 of 626 are expected; P(>= 4) about
  0.01). (b) No class with median Y < -3 se. (c) DF2 and DF4 each: Y_sys >= -3 e_sys and d_L,sys <= +3 e_sys.
  HOLDS if (a), (b), (c) hold.
- **H3, undisturbed systems on the law; none isolated below it; baryon-losers at or above it.**
  (a) on the law, |median d_L| <= 3 se, for: SPARC; SPARC's gas-rich half (f_g >= 0.5); faint rotators with Ti1 < 0
  (isolated by UNGC). (b) no isolated set below: median d_L >= -3 se for SPARC, KiDS (isolated by selection), LG field
  dwarfs (stars-only g_bar: an upper bound on their d_L), faint rotators with Ti1 < 0, ATLAS3D outside Virgo.
  (c) baryon-losers at or above: median d_L >= -3 se for MW bright dwarfs, MW ultra-faints, M31 dwarfs, Coma UDGs,
  groups. HOLDS if (a), (b), (c) hold. Reported: the faint rotators' isolated fraction, and their offset with M_* x 2 and
  x 0.5 and with distances x 0.8 and x 1.2 (coherent).
- **H4, closed systems hold the whole (quoted from RB1, not redone; no a0).** In X: a closed system's X at its edge
  approaches R = 5.41 from below; a system that lost baryons has X above R. (The lead's wording "groups below it" holds
  for RB1's retention f_ret = R / X; in X a baryon loss puts a system above R.) HOLDS if RB1 gives: X-COP's last-radius
  class f_ret 95 % interval contains 1; X-COP at R500 f_ret >= 1 (X at or below R inside the edge); groups' f_ret
  95 % upper bound < 1 (X above R). DD1's X_last medians are reported beside it.
- **H5, the offset tracks a sign of history.** Spearman rank correlation of d_L,sys with the indicator for G1 to G6,
  Holm-corrected over the six at 0.05 (two-sided). HOLDS if at least one pair is significant with the history sign and
  none is significant against it. FAILS if any is significant against it. NO POWER if none is significant.

Outcomes per test: HOLDS / FAILS / NO POWER (H5 only).

## Controls (same tests)

- **Force reading** (every system on the plain law now; the table carries no external field, so none is used; RB2's
  external-field statements are quoted). Its predictions on the same tests: F1 tidal dwarfs |median d_L| <= 2 se;
  F2 count of systems with d_L,sys < -3 e_sys <= 3, and DF2 / DF4 |d_L,sys| <= 3 e_sys; F3 every H3 set and every
  hosted class with |median d_L| <= 3 se; F4 X-COP's X at its last points equals the law's X there (class median d_L at
  the last points within 3 se of 0); F5 no G pair significant. Reported as passes out of five.
- **No rule** (class labels shuffled across systems, seed 7; indicators travel with their systems): H1 to H3 and H5
  re-run; reported as how many hold.

## Labels (per footing)

- **THE HISTORY READING HOLDS ON EVERY TEST**: H1 to H5 all HOLD.
- **HOLDS EXCEPT**: no more than one test FAILS (named, with by how much), others HOLD or NO POWER (named).
- **FAILS**: two or more tests FAIL (named, by how much).
- **NO VERDICT**: a known answer fails.
Beside the label: the force reading's score out of five, and the shuffled control's.

## Known answers (must pass)

- KA1: DD1 reproduced: every class's L0 offset over all systems equals DD1's leave-one-class-out L0 offset in `dd1.json`
  to 1e-9 (L0 has no fit), both footings.
- KA2: the record's tidal-dwarf numbers: the inverse-variance mean of log10(Mdyn/Mbar) from Lelli+15's own columns equals
  G2's +0.083 +- 0.096 to 1e-3; DD1's table Y for the six equals log10(Mdyn/Mbar) within 0.05 dex each.
- KA3: synthetic truths, noise free, se from the real errors: (i) history truth (tidal dwarfs and DF2 / DF4 at Y = 0,
  every other system on the law, hosted classes +0.3 dex): H1, H2, H3 HOLD and F1 fails; (ii) force truth (every system
  on the law): H1 FAILS and F1, F2, F3 pass; (iii) a planted gas-fraction trend d_L -= 0.3 (f_g - median) in SPARC and
  the faint rotators on the force truth: H5 HOLDS; on the force truth without it: H5 NO POWER.
- KA4: Lean identities numerically: X_L > 0 and X_L <= sqrt(a0 / g_bar) on a grid, both footings.

## MUTATE (separate outputs `his1_MUTATE.*`; each must change its stated outcome, else disclosed)

- M1 tidal dwarfs put on the law (Y = Y_L): H1 FAILS.
- M2 four SPARC galaxies moved to Y = -0.6 dex: H2 FAILS.
- M3 the opposite gas trend planted in SPARC (d_L += 0.5 (f_g - median)): H5 FAILS.
- M4 a0 x 2: H3 (a) fails for SPARC.

## Lean (`HIS1.lean`, with a false twin that must fail)

XL_pos (X_L > 0: Newton lies below the law at every g_bar); XL_le (X_L <= sqrt(a0/g_bar)); between (0 <= X <= X_L
gives 0 <= log(1 + X) <= log(1 + X_L)).

## Record checked first (quoted, not redone)

- Tidal dwarfs: CFG936 (6 Lelli+15 TDGs at -0.690 +- 0.078 / -0.728 +- 0.079 dex below the law; at Newton +0.055 +-
  0.114; the "zero supply" route explains them); G2 (B1: +0.083 +- 0.096 against Newton, NO BREAKAGE).
- DF2 / DF4: CFG936 (at Newton, +0.021 +- 0.539 ln); G2 (B2: not stripped at the projected distance under baryons plus
  the law; would need a pericentre <= 24 / 21 kpc); NH2 (under form B, NGC 1052 cannot hold the mass that today's tides
  on DF4 need: TIDES CANNOT REACH under its post hoc reading A1, NO VERDICT as frozen; DF2 NOT DECIDED; scope: present
  tides at the projected distance, not a past pericentre).
- MW ultra-faints and Coma UDGs: RB2 (B FAILS HIGH for the ultra-faints and bright M31; Coma CONSISTENT on the
  systematics budget); DG1 (the two FAILS HIGH do not survive the data-side regrade; counting each dwarf's lost gas
  brings every class to zero, but per system the residual does not follow the predicted history: rank +0.06 in the
  ultra-faints, +0.12 in bright M31, -0.04 at fixed stellar mass: HISTORY DOES NOT CLOSE THEM).
- Groups and clusters: RB1 (f_ret 0.597 [0.556, 0.637] groups; X-COP last radius 1.095 [0.885, 1.259]; at R500 1.057
  [1.046, 1.072]).

## Disclosures (seen before this file)

- Every DD1 number (its RESULT.md and outputs), and the record numbers quoted above.
- While matching names to UNGC: the tidal index of a few galaxies (SexA -0.8, SexB -0.8, DDO099 -0.8, DDO053 +0.8, HolmII
  +0.7, and the first rows of the file). No indicator was set against any offset.
- Hand estimates: H1 HOLDS (DD1: tidal dwarfs' median Y 0.07, 0.6-0.9 dex below the law). H2 HOLDS unless some early
  types read below X = 0 at Chabrier. H3 FAILS on the faint rotators if most are isolated (DD1: -0.24 to -0.27, about 5
  se), otherwise it rests on the isolated subset. H4 HOLDS (RB1). H5 NO POWER (DG1: no per-system signal; SHP1: no mass
  trend in SPARC). Expected label: HOLDS EXCEPT H3 (faint rotators), H5 no power. Force reading: fails F1, F2 (DF2 /
  DF4), F3 (hosted classes above), F4; passes F5.

## Operational

One thread, minutes. `his1.py` -> `his1.json` / `his1.out`; `--mutate` -> `his1_MUTATE.*`. Lean via `lake env lean`;
`compile.txt` with no home paths. Explicit-path commits; push by a temporary sparse worktree.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
