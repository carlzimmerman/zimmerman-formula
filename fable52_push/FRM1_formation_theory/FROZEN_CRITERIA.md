# FRM1 FROZEN CRITERIA: the formation reading as a theory (2026-11-11)

TEST lane, quarantined. Adopts nothing, relabels nothing, registers nothing. Footings never pooled (canonical a0
9.3603e-11, alt 1.1312e-10 m/s^2). Committed alone, before any FRM1 script exists or any FRM1 number is computed.
The id FRM1 was checked free (no `fable52_push/FRM*`, no commit subject naming FRM1 or formation_theory).

## Question

HIS1 (`fable52_push/HIS1_history_reading/`, and its blind regrade HIS1R) found that on DD1's frozen 626-system
table the reading
"the non-baryonic mass is real and conserved, its amount set by the law WHEN A SYSTEM FORMED" meets four of five of
DD1's statements, while "the law is a force every system obeys now" scores 1 of 5; HIS1R regraded it with separate
code and got the same label. A reading that survives is not yet a theory. FRM1 turns it into one and asks three
things: **what quantity is set at formation**, **what conserved charge carries it afterwards**, and **what sets the
epoch**. It then grades the resulting theory against DD1's own frozen table, with DD1's own held-out and
leave-one-class-out scoring, and with the fit free (no theory assumed in the fit).

The predictions are written here, with a sign and a rough size for every one of the 16 classes, **before the table is
read**. The lane reports which of them the table confirms and which it contradicts.

## Data

DD1's frozen table, unchanged: `fable52_push/DD1_deduce_from_data/dd1_table.csv` (main rows only; DD1's loaders,
apertures and systematics apply). 3419 points, 626 systems, 16 classes. Per point Y = log10(g_obs/g_bar) =
log10(1 + X), X = M_C(<r)/M_b(<r); per system Y_sys = median of Y over its points, e_sys = median of its finite e_Y.
Per class: off = median of d_sys over the scored systems, se = max(1.2533 x 1.4826 MAD(d_sys)/sqrt(n),
sqrt(sum e_sys^2)/n), se = e_sys for n = 1 (DD1's rule). Splits A / B stratified by class, seed 20261110 (DD1's);
leave-one-class-out as DD1's. The law's value Y_L = log10(1 + X_L(g_bar; a0)),
X_L = (sqrt(1 + 4 a0/g_bar) - 1)/2; the offset d_L = Y - Y_L, per system the median over its points.

## The theory (FRM)

Three objects. Nothing here is fitted; a0 is the footing's, and X_L is DD1's curve.

**Q — what is set at formation.** A system forms when the baryons that define it are assembled into a bound
configuration, at epoch t_f. At that moment it carries non-baryonic mass

    M_C,f = X_L(g_b,f ; a0) * M_b,f ,      X_f = M_C,f / M_b,f = X_L(g_b,f ; a0)

where g_b,f is the baryonic field of the assembled system at formation. So the quantity set at formation is the
**ratio of the non-baryonic mass to the baryonic mass**, fixed by the record's law evaluated at the formation field.

**C — the conserved charge.** The non-baryonic mass M_C is a real, separately conserved charge: for a closed system
dM_C/dt = 0, and it changes only by transport across the system's boundary. A host strips it (f_C < 1); merging and
accretion add it (f_C > 1). The baryonic mass M_b is a second conserved charge with its own transfers: gas expelled
by feedback, ram-pressure stripped, or tidally removed (f_b < 1), gas accreted (f_b > 1). Both are non-negative.
Today

    X = X_f * (f_C / f_b) ,
    d  = Y - Y_L(g_bar) = log10[ (1 + X_L(g_b,f) f_C/f_b) / (1 + X_L(g_bar)) ] .          (master equation)

**E — what sets the epoch.** The formation epoch is the assembly epoch of the system's baryons. The law's scale does
not run with it: a0 = (1/2) c sqrt(G rho_DE) with rho_DE constant (w = -1), so the same a0 fixes the amount at every
epoch. The epoch therefore enters **only** through the field g_b,f at which the amount was fixed, and through the
time available for transfers. For a system that settled and transferred nothing, g_b,f is the field of the
configuration we measure, and it sits on the law today. (A variant in which a0 tracks rho_DE(z) and so is larger at
early epochs is reported, not graded: it moves the early classes up and the late classes not at all, and so cannot
make SPARC and the clusters both right.)

**The three channels, with their signs and sizes** (deep regime, X and X_L >> 1, where X_L ~ sqrt(a0/g)):

    d ~ (1/2) log10( g_bar / g_b,f )  +  log10( f_C / f_b )

- **S, stripping of the charge** (f_C < 1, f_b = 1, g_b,f = g_bar): d = log10 f_C < 0. Losing 90 % of the charge puts
  a system -1.0 dex below the law. It cannot go below the floor d_floor = -Y_L(g_bar), which is X = 0.
- **B, baryon loss** (f_b < 1, f_C = 1; the field falls with the baryons it lost, g_bar = f_b g_b,f):
  d = -(1/2) log10 f_b > 0. Losing 90 % of the baryons puts a system +0.5 dex above; 50 % gives +0.15; 25 % gives
  +0.06. **This is the only channel that raises a system above the law.**
- **A, late baryon accretion or dissipation** (f_b > 1, f_C = 1): d < 0.
- **No transfer and no contraction** (f_C = f_b = 1, g_b,f = g_bar): d = 0. This is the anchor.

Two structural consequences, both testable and both pre-registered:
1. **The floor.** X >= 0 always (both charges are non-negative), so no system can sit below d = -Y_L(g_bar).
2. **No upward channel but baryon loss.** A system above the law must have lost baryons, and the amount of loss is
   determined: solve the master equation for f_b at the measured offset. The lane reports that f_b per class.

## Pre-registered predictions (before the table is read)

Each interval is derived from what the class *is* (its assembly state, its gas, its environment, its aperture), not
from its offset. The three scorings are DD1's A->B, B->A and LOCO; a class must fall in its interval in **all three**
to count. The same intervals are used on both footings (alt shifts d_L by at most 0.04 dex; the bands carry that).

| class | channels the theory licenses for it | predicted d_L (dex) | why |
|---|---|---|---|
| SPARC | none: settled discs, gas inside the aperture | **-0.05 .. +0.05** | the anchor: f_C = f_b = 1, g_b,f = g_bar |
| faint rotators | A: still assembling, gas-dominated, gas beyond the last radius | **-0.35 .. 0.00** | baryons still growing; total-as-enclosed also pushes low |
| tidal dwarfs | S: born out of a parent's debris, no charge of their own | **-0.95 .. -0.30**, and >= floor - 3 se | formed from stripped baryons; nothing to strip afterwards |
| massive spirals | none, mild B | **-0.05 .. +0.20** | settled massive discs; some gas processed into stars |
| ATLAS3D | B: gas-poor early types | **0.00 .. +0.20** | the gas is gone from the aperture; the charge is not |
| RC100 | B: strongly star-forming discs at z 0.6-2.5 | **0.00 .. +0.20** | gas being turned into stars and partly expelled |
| KiDS | none: field galaxies, isolated by selection | **-0.15 .. +0.15** | undisturbed, unhosted |
| groups | B: gas processed, AGN-driven loss | **0.00 .. +0.30** | deep, unhosted, some baryons pushed out |
| X-COP | none, or A | **-0.30 .. +0.30** | deepest unhosted wells, gas measured to be there; no channel in the theory lifts them |
| CLASH | none, or A | **-0.30 .. +0.30** | same |
| MW bright dwarfs | B: hosted, gas lost to the Galaxy | **0.00 .. +0.30** | satellites stripped of gas |
| MW ultra-faints | B: hosted, nearly all gas lost | **+0.30 .. +0.70** | the most gas-stripped: f_b ~ 0.1 gives +0.5 |
| M31 dwarfs | B: hosted by M31 | **0.00 .. +0.30** | satellites stripped of gas |
| LG field dwarfs | none; their g_bar omits their HI, so d_L is biased up | **-0.20 .. +0.30** | unhosted; omitted gas pushes them high |
| Coma UDGs | B: ram-pressure gas loss in the cluster | **+0.10 .. +0.50** | cluster members stripped of gas |
| NGC 1052 UDGs (DF2, DF4) | S: stripped by the host after an early formation | **-1.05 .. -0.30**, and >= floor - 3 se | satellites that lost the charge, not the stars |

**The two the lead names, stated as predictions and not as post-dictions:**
- *systems that formed early and were then stripped sit LOW*: the tidal dwarfs and DF2 / DF4 are predicted at
  **-0.3 to -1.0 dex**, i.e. between the law and X = 0, and much nearer X = 0;
- *hosted systems sit HIGH*: the MW ultra-faints are predicted at **+0.3 to +0.7 dex** (the biggest of any class,
  because they lost the most gas), the Coma UDGs at +0.1 to +0.5, and M31 and the bright MW dwarfs at 0 to +0.3.

**The prediction the theory is expected to fail:** the clusters. An unhosted 10^14-10^15 M_sun well whose hot gas is
measured inside the aperture has no sink for most of its baryons, so f_b cannot be small; at X-COP's field
(a0/g_bar ~ 4.5) the master equation needs **f_b ~ 0.40** (60 % of the baryons inside R500 expelled) to make +0.5
dex. The theory predicts X-COP and CLASH in **-0.30 .. +0.30**. If the table puts them at +0.5, the theory is wrong
there, by the size of the miss, and in the one direction it has no channel for.

## Tests (per footing; each HOLDS / FAILS, F3 three-way, F5 as given)

- **F1 the floor and the stripped.** (a) the number of systems with Y_sys < -3 e_sys is <= 3 (about 0.85 of 626
  expected by chance); (b) no class has median Y < -3 se; (c) each of the 6 tidal dwarfs and each of DF2, DF4 has
  Y_sys >= -3 e_sys and d_L,sys <= +3 e_sys. HOLDS if (a), (b), (c).
- **F2 the two channels the lead names.** (a) the stripped family — tidal dwarfs and NGC 1052 UDGs — has
  median d_L <= -3 se AND median d_L >= d_floor - 3 se, in all three scorings; (b) the hosted, gas-lost family —
  MW bright dwarfs, MW ultra-faints, M31 dwarfs, Coma UDGs — has median d_L >= -3 se in all three scorings, and at
  least three of the four have median d_L >= 0. HOLDS if (a) and (b).
- **F3 the pre-registered sizes.** Count the classes whose offset lies inside its pre-registered interval in all
  three scorings. HOLDS if >= 15 of 16; HOLDS EXCEPT if 13 or 14; FAILS if <= 12. Name every miss and by how much.
- **F4 the free rule, no theory assumed.** DD1's own held-out and leave-one-class-out machinery, DD1's pass line
  (|off| <= 0.10 dex AND |off| <= 3 se) and DD1's scatter line (the rule's class-balanced robust held-out scatter
  must not exceed the class-constant reference, in both splits). The rules the formation reading licenses, each with
  the law's curve as the base and one free binned function F fitted on the training systems only (DD1's node recipe:
  0.2-dex bins on a fixed grid, a bin with at least 5 training points gives a node at the system-weighted medians,
  linear interpolation between nodes, the least-squares line through the three end nodes outside):
  - **N0** Y = Y_L(lgb) (no free parameter; this is the force reading's rule);
  - **N1** Y = Y_L(lgb) + F(dsys) (the epoch / assembly-state proxy: the system's own depth);
  - **N2** Y = Y_L(lgb) + F(zz) (the epoch as observed redshift);
  - **N3** Y = Y_L(lgb) + F(dsys, zz) (both; 0.4 x 0.4 cells, DD1's two-variable recipe).
  F4 HOLDS if at least one of N1, N2, N3 passes DD1's full test (every class passes in A->B, B->A and LOCO, and the
  scatter line holds in both splits). N0's score is reported, not graded. The reference scatter and each rule's
  held-out scatter, failing classes and worst class are reported.
- **F5 the epoch does not rescale the amount.** The transfer-free, unhosted classes — SPARC, KiDS, LG field dwarfs —
  must sit on the law at the footing's a0 with no free parameter: |off| <= 3 se in all three scorings, for all three.
  HOLDS if all three do.

Reported, not graded: the f_b each class would need under the baryon-loss channel alone (solve the master equation
per point at the class's offset); the f_C the stripped classes need; L1's single free a0; the free rules' per-class
offsets; the offset of the transfer-free classes ordered by observed redshift (does the offset track z?).

## Labels (per footing)

- **THE FORMATION THEORY HOLDS**: F1, F2, F3, F4, F5 all HOLD.
- **HOLDS EXCEPT**: F1, F2 and F5 HOLD; F3 and / or F4 fail (named, each with the size of the miss).
- **FAILS**: F1, F2 or F5 fails (the channels themselves are contradicted), or F3 FAILS.
- **NO VERDICT**: a known answer fails.
Beside the label: the count in F3, the misses, and the f_b the misses would need.

## Known answers (must pass, else NO VERDICT)

- KA1 DD1 reproduced: every class's L0 LOCO offset equals DD1's `dd1.json` to 1e-9, both footings (L0 has no fit).
- KA2 synthetic truths, noise free, se from the real errors, on the real points:
  (i) **history truth** (tidal dwarfs and DF2 / DF4 at X = 0; the four hosted classes with f_b = 0.3; the clusters
  and every other class with f_C = f_b = 1): F1, F2, F3 all HOLD and F3 is 16/16;
  (ii) **force truth** (every system on the law, f_C = f_b = 1 everywhere): F2(a) FAILS and F3 is <= 12;
  (iii) **cluster truth** (force truth, but X-COP and CLASH given the baryon-loss channel with f_b = 0.40): F3 is
  16/16 — i.e. the only way the theory accommodates the clusters is 60 % of their baryons leaving the aperture.
- KA3 HIS1's structural numbers reproduced: the count of systems with Y_sys < -3 e_sys is 0, and the tidal dwarfs'
  median d_L = -0.687 +- 0.115 (canonical) to 1e-3.
- KA4 the master equation's two limits, on the real points: (a) with f_b = 1 and f_C planted, the exact offset equals
  log10((1 + X_L f_C)/(1 + X_L)) to 1e-12; (b) with f_C = 1 and f_b planted (g_bar = f_b g_b,f), the exact offset is
  >= 0 for every f_b <= 1 and every point, and equals -(1/2) log10 f_b to within 0.10 dex on every point with
  X_L >= 5.
- KA5 Lean identities numerically: X_L > 0 and X_L <= sqrt(a0/g_bar) on a grid, both footings.

## MUTATE (separate outputs `frm1_MUTATE.*`; each must change its stated outcome, else disclosed)

- M1 every system put on the law (Y := Y_L at its own g_bar, both footings): F2 must FAIL.
- M2 class labels shuffled across systems (seed 20261110; the predictions stay with the class names): F3's count must
  fall below 13.
- M3 the baryon-loss channel applied to the clusters (X-COP and CLASH g_bar x 0.40, their g_obs unchanged): each
  cluster class's offset must rise by >= +0.25 dex and enter its pre-registered interval.
- M4 a0 x 2 (both footings): F5 must FAIL.

## Lean (`FRM1.lean`, with a false twin that must fail to compile)

`XL_pos` (X_L > 0); `XL_le_sqrt` (X_L <= sqrt(a0/g_bar)); `XL_anti` (X_L decreases with the field); `charge_nonneg`
(the transferred charge is non-negative); `strip_lowers` (f_C <= 1, f_b <= 1 lowers X below what formation gave);
`baryon_loss_raises` (f_b <= 1 with g_bar = f_b g_b,f puts X above the law's present demand);
`Y_nonneg` (X >= 0 gives Y >= 0, so the floor is -Y_L).

## Record checked first (quoted, not redone)

- DD1 (origin 91c159b746): NO RULE AMONG THE CANDIDATES; the offsets quoted in this file's prediction table; the
  reference scatter 0.284 dex; P3 (g_bar, system depth) the best full-cover rule at 0.219 dex, failing 12 classes;
  L1's single free a0 at 1.6-1.8 times canonical; X_last medians (X-COP 4.94, groups 9.07, CLASH 7.58, DF2/DF4 0.07).
- HIS1 / HIS1R: HOLDS EXCEPT H3 (faint rotators), H5 no power; force reading 1 / 5; no system below X = 0 beyond 3 e;
  tidal dwarfs d_L -0.687 +- 0.115; DF2 d_L -0.743 (e 0.344), DF4 -0.943 (e 0.349).
- RB1: X-COP last-radius f_ret 1.095 [0.885, 1.259]; at R500 1.057 [1.046, 1.072]; groups 0.597 [0.556, 0.637].
- DG1: the hosted classes' offsets do not follow a predicted per-system history (rank +0.06 in the ultra-faints).

## Disclosures (seen before this file)

- Every DD1 and HIS1 number (their RESULT.md files and outputs), and the record numbers quoted above.
- The DD1 table's column list and the per-class point / system counts (16 classes, 3419 main points, 626 systems).
- No FRM1 number of any kind. No per-class offset has been computed in this lane.
- Hand estimates: F1 HOLDS (HIS1 found no system below X = 0). F2 HOLDS (DD1: the tidal dwarfs -0.61 to -0.87 and
  DF2 / DF4 -0.74 to -0.94 below the law; the hosted classes +0.03 to +0.59 above it). F3: 14 of 16, the two cluster
  classes missing their band by about +0.2 to +0.3 dex. F4 FAILS (DD1 found no candidate holds the splits in any of
  51 seeds; a free function on top of the law inherits that). F5 HOLDS (SPARC on the law; KiDS within its 0.15 se).
  Expected label: **HOLDS EXCEPT** (the clusters), on both footings.

## Operational

One thread, small memory, minutes. `frm1.py` -> `frm1.json` / `frm1.out`; `frm1.py --mutate` ->
`frm1_MUTATE.json` / `frm1_MUTATE.out`. Lean via `lake env lean` in the record's build
(`fable_independent_2026/lean_2026`); `compile.txt` with no home paths. Commit with explicit paths; push by a
temporary sparse worktree.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
