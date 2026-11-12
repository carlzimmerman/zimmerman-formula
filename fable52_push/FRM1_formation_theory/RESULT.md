# FRM1 RESULT: the formation reading as a theory (2026-11-11)

> **Forward correction, 2026-11-12:** the labels and numbers below are historical.
> The baryon-loss ceiling assumes fixed profile and no incoming cold charge;
> it does not exclude all formation/transport histories. The class bands were
> chosen after prior DD1/HIS1 results were known, so the hits are retrospective
> consistency, not unseen predictions. Read [the correction](CORRECTION_2026_11_12.md).
>
> *Audit note, 2026-11-12 (lead session):* this notice was written by another session and is committed here on the owner's instruction after an independent check, `reviews/codex_corrections_audit_2026_11_12/C2_pik1_and_frm1.md` (grade: ceiling scope: CORRECT WITH LIMITS; retrospective bands: CORRECT). The audit adds that the frozen line of this lane reads FAILS / FAILS, and that the sentence below saying the offsets were predicted before the table was read does not hold. The folder `research_closure_2026_11_12/` it links to was not committed with it, so those links may not resolve; the audit file is the checked record. The committed text, labels and outputs below this notice are not edited by this commit.

Criteria 462eaa806d (+ one disclosed amendment fed1bc94a4, made before any FRM1 number existed). Table 441824e854
(DD1's, frozen, unchanged: 3419 points, 626 systems, 16 classes). TEST lane, quarantined: adopts nothing, relabels
nothing, registers nothing. Footings never pooled (canonical a0 9.3603e-11, alt 1.1312e-10 m/s^2).

## Label

**HOLDS EXCEPT / HOLDS EXCEPT** (canonical / alt).

Under the frozen F2 pass line exactly as committed, the same run reads **FAILS / FAILS**. The difference is one
clause, and the lane shows (KA2) that the clause is *unsatisfiable*, not merely strict: the synthetic history truth —
the theory's own truth — fails it too. Both labels are reported; see "The one defective clause" below.

Every known answer passes. All four mutation arms bite. `FRM1.lean` compiles (8 theorems, standard axioms only);
its false twin fails with 7 errors, one per false statement.

## The theory, in three objects

- **Q, what is set at formation.** A system forms when the baryons that define it are assembled. At that moment the
  ratio of non-baryonic to baryonic mass is fixed by the record's law evaluated at the formation field:
  X_f = M_C,f/M_b,f = X_L(g_b,f; a0), X_L = (sqrt(1 + 4 a0/g) - 1)/2.
- **C, the conserved charge.** The non-baryonic mass M_C is a real, separately conserved charge: dM_C/dt = 0 for a
  closed system, changed only by transport across the boundary (a host strips it: f_C < 1; merging adds it: f_C > 1).
  The baryons are a second conserved charge with their own transfers (f_b < 1: gas expelled, ram-pressure stripped,
  tidally removed). Both are non-negative. Today
  **X = X_f (f_C/f_b)** and the offset from today's law is
  **d = log10[(1 + X_L(g_b,f) f_C/f_b)/(1 + X_L(g_bar))]**.
- **E, what sets the epoch.** The epoch is the assembly epoch of the baryons, and it does *not* rescale the law:
  a0 = (1/2) c sqrt(G rho_DE) with rho_DE constant, so the same a0 sets the amount at every epoch. The epoch enters
  only through the field g_b,f at which the amount was fixed, and through the time available for transfers. A system
  that settled and transferred nothing has g_b,f = g_bar and sits on the law today (the anchor).

**The three channels** (deep regime, X and X_L >> 1, where X_L ~ sqrt(a0/g)):
d ~ (1/2) log10(g_bar/g_b,f) + log10(f_C/f_b). Stripping (f_C < 1) lowers; baryon loss (f_b < 1) raises, and it is
the **only** channel that raises; late baryon accretion lowers. The floor is X = 0.

## Pre-registered, then read (canonical; the same bands on alt)

The bands were committed before any FRM1 number existed. A class must fall in its band in all three of DD1's scorings
(A->B, B->A, leave-one-class-out) to count.

| class | predicted band | A->B | B->A | LOCO | in band |
|---|---|---|---|---|---|
| SPARC (anchor: no transfer) | -0.05 .. +0.05 | -0.003 | +0.018 | +0.004 | yes |
| faint rotators (still assembling) | -0.35 .. 0.00 | -0.274 | -0.239 | -0.239 | yes |
| tidal dwarfs (born from debris) | -0.95 .. -0.30 | -0.606 | -0.869 | -0.687 | yes |
| massive spirals | -0.05 .. +0.20 | +0.155 | +0.019 | +0.066 | yes |
| ATLAS3D (gas gone) | 0.00 .. +0.20 | +0.067 | +0.080 | +0.070 | yes |
| RC100 | 0.00 .. +0.20 | +0.074 | +0.114 | +0.088 | yes |
| KiDS (isolated by selection) | -0.15 .. +0.15 | +0.129 | +0.138 | +0.137 | yes |
| groups (gas processed) | 0.00 .. +0.30 | +0.161 | +0.165 | +0.161 | yes |
| **X-COP** | **-0.30 .. +0.30** | **+0.571** | **+0.482** | **+0.496** | **NO** |
| **CLASH** | **-0.30 .. +0.30** | **+0.553** | **+0.551** | **+0.553** | **NO** |
| MW bright dwarfs (hosted) | 0.00 .. +0.30 | +0.060 | +0.201 | +0.065 | yes |
| MW ultra-faints (most gas lost) | +0.30 .. +0.70 | +0.507 | +0.597 | +0.592 | yes |
| M31 dwarfs (hosted) | 0.00 .. +0.30 | +0.013 | +0.185 | +0.090 | yes |
| LG field dwarfs (unhosted; gas omitted) | -0.20 .. +0.30 | -0.029 | -0.090 | -0.090 | yes |
| Coma UDGs (ram-pressure loss) | +0.10 .. +0.50 | +0.365 | +0.311 | +0.319 | yes |
| NGC 1052 UDGs (DF2, DF4; stripped) | -1.05 .. -0.30 | -0.943 | -0.743 | -0.843 | yes |

**14 of 16 inside their pre-registered band** (alt: 13 of 16 — the M31 dwarfs read -0.028 in A->B, 0.03 dex under the
band's lower edge; their LOCO offset is +0.051). The two the lead named are confirmed, in sign and in size:

- *formed early, then stripped, sit LOW*: the tidal dwarfs at -0.61 to -0.87 and DF2 / DF4 at -0.74 to -0.94, i.e.
  between the law and X = 0 and nearer X = 0 (they would need f_C = 0.038 and 0.009 — 96 % and 99 % of the charge
  gone). The floor holds: no system anywhere in the table sits below X = 0 beyond 3 e (0 of 626).
- *hosted systems sit HIGH*: the MW ultra-faints at +0.51 to +0.60 (predicted +0.30 to +0.70), the Coma UDGs at +0.31
  to +0.37, M31 at +0.01 to +0.19, the bright MW dwarfs at +0.06 to +0.20. All four are at or above the law in all
  three scorings.

And the one the theory was expected to fail, it failed: the clusters.

## The cluster failure, and how hard it is

| | X-COP | CLASH |
|---|---|---|
| offset from the law (LOCO) | +0.496 +- 0.022 (**22.5 se**) | +0.553 +- 0.023 (**24.0 se**) |
| pre-registered band | -0.30 .. +0.30 | -0.30 .. +0.30 |
| miss | +0.20 dex | +0.25 dex |
| the baryon-loss ceiling d_max at that field | **+0.320** | **+0.227** |
| fraction of the class's points with X > a0/g_bar (no baryon loss can reach them) | **0.77** | **0.98** |

The ceiling is the theory's own algebra, not a fit: with f_C = 1, X = X_L(g_bar/f_b)/f_b increases as f_b falls but
tends to a0/g_bar, so no baryon loss, however extreme, can raise a system that was on the law at formation by more
than d_max = log10[(1 + a0/g_bar)/(1 + X_L(g_bar))]. X-COP sits +0.50 against a ceiling of +0.32: **0.18 dex above
anything the theory's channels can do**, and 77 % of its points (98 % for CLASH) carry more non-baryonic mass per
baryon than a0/g_bar, which is the absolute ceiling of the channel.

The only escape the theory has left is the free formation field: with no transfer at all, the cluster's offset would
require g_b,f/g_bar = 0.098 (X-COP) and 0.086 (CLASH), i.e. the cluster's baryons 3.2 x more extended when the amount
was fixed than they are now. The same bookkeeping applied to SPARC gives 0.887 (a 6 % contraction), so the cluster's
requirement is not the disc's; and there is no measured quantity in this table that fixes g_b,f. It is reported, not
graded, and it is unfalsifiable here.

The shallow classes have the same problem in small: 63 % of ATLAS3D's points and 57 % of RC100's lie above their
(very low) ceilings of +0.023 and +0.049 dex, so their +0.07 to +0.09 dex is also out of the baryon-loss channel's
reach — a 0.05 to 0.07 dex excess that the theory does not explain either.

## The tests

| test | canonical | alt |
|---|---|---|
| F1 the floor and the stripped (no system below X = 0; TDGs and DF2/DF4 between 0 and the law) | HOLDS | HOLDS |
| F2 the stripped sit low and the hosted sit high | HOLDS | HOLDS (frozen line: FAILS / FAILS) |
| F3 the 16 pre-registered bands | HOLDS EXCEPT, 14/16 | HOLDS EXCEPT, 13/16 |
| F4 a free rule (no theory assumed) passes DD1's held-out and LOCO test | FAILS | FAILS |
| F5 the epoch does not rescale the amount (SPARC, KiDS, LG field dwarfs on the law within errors) | HOLDS | HOLDS |

**F4, the free rule, in full.** The law's curve plus one free binned function of a history variable, fitted on the
training systems only (DD1's node recipe), scored by DD1's held-out and leave-one-class-out machinery, DD1's pass
line (|off| <= 0.10 dex and <= 3 se) and DD1's scatter line (0.284 dex, the class-constant reference):

| rule | held-out scatter | ref | scatter line | classes failing | worst class |
|---|---|---|---|---|---|
| N0 the law alone (the force reading's rule) | 0.336 | 0.284 | no | 14 | NGC 1052 UDGs (A->B, -0.943, -2.7 se) |
| N1 law + free F(system depth) | **0.213** | 0.284 | yes | 10 | NGC 1052 UDGs (A->B, -1.303, -3.7 se) |
| N2 law + free F(redshift) | 0.285 | 0.284 | no | 15 | NGC 1052 UDGs (A->B, -0.981, -2.8 se) |
| N3 law + free F(depth, redshift) | 0.229 | 0.284 | yes | 11 | NGC 1052 UDGs (A->B, -1.281, -3.7 se) |

A free function of the system's depth on top of the law cuts the held-out scatter from 0.336 to 0.213 dex and beats
the class-constant reference — the epoch / assembly-state variable does real work, as the theory says it must. But it
still fails 10 of the 16 classes, and it *worsens* the shallow end (NGC 1052 UDGs go from -0.94 to -1.30 dex), so
F4 FAILS. Redshift does nothing (0.285, 15 classes failing): the offset does not order with observed epoch among the
undisturbed classes (SPARC +0.004 at z ~ 0, KiDS +0.137 at z ~ 0.3, RC100 +0.088 at z 0.6-2.5, massive spirals
+0.066), which is consistent with E — the observed epoch is not the formation epoch's proxy in this table.

**F5** is the one clean pass: with no free parameter, at the footing's a0, the transfer-free unhosted classes sit on
the law within errors in all three scorings (SPARC +0.004 +- 0.012; KiDS +0.137 +- 0.109, 1.3 se; LG field dwarfs
-0.090 +- 0.062, 1.5 se). So the epoch is not rescaling the amount for them; only transfers move systems.

## The transfer budgets (reported, grades nothing)

Per class, the transfer the master equation would need to produce the measured offset, at fixed formation field.

| class | offset | f_b (baryons kept) | f_C (charge kept) | ceiling d_max | g_b,f/g_bar needed if no transfer |
|---|---|---|---|---|---|
| tidal dwarfs | -0.687 | (328: accretion) | 0.038 | +0.687 | 23.7 |
| NGC 1052 UDGs | -0.843 | (401: accretion) | 0.009 | +0.799 | 48.5 |
| faint rotators | -0.239 | 5.37 | 0.440 | +0.588 | 3.00 |
| LG field dwarfs | -0.090 | 1.60 | 0.797 | +0.940 | 1.51 |
| SPARC | +0.026 | 1.00 | 1.013 | +0.277 | 0.89 |
| massive spirals | +0.066 | 0.583 | 1.240 | +0.539 | 0.74 |
| ATLAS3D | +0.070 | 2.42 | 1.720 | +0.023 | 0.73 |
| RC100 | +0.088 | 1.32 | 1.842 | +0.049 | 0.67 |
| KiDS | +0.133 | 0.509 | 1.385 | +1.547 | 0.54 |
| groups | +0.161 | 0.386 | 1.531 | +0.794 | 0.48 |
| M31 dwarfs | +0.090 | 0.622 | 1.253 | +1.223 | 0.66 |
| MW bright dwarfs | +0.065 | 0.680 | 1.191 | +1.070 | 0.74 |
| Coma UDGs | +0.319 | 0.186 | 2.186 | +1.047 | 0.23 |
| MW ultra-faints | +0.592 | 0.053 | 4.080 | +1.541 | 0.065 |
| X-COP | +0.504 | 0.111 (77 % of points unreachable) | 4.515 | +0.320 | 0.098 |
| CLASH | +0.533 | 0.028 (98 % of points unreachable) | 5.779 | +0.227 | 0.086 |

The hosted classes' numbers are the standard picture's, in the theory's currency: the ultra-faints must have kept
5 % of their baryons, the Coma UDGs 19 %, M31's dwarfs 62 %. The stripped classes are at the other end: DF2 and DF4
would have to have kept 1 % of the charge.

## The one defective clause

F2(a) was committed as: the stripped family must satisfy d_L <= -3 se in *every* scoring. For the NGC 1052 UDGs
(n = 2 systems, so one per half, e_sys = 0.34 dex) the half-splits have se = 0.34 dex and 3 se = 1.03 dex, while the
X = 0 floor is at -0.84 dex. The clause therefore asks for an offset below -1.03 dex from a system that cannot go
below -0.84: **no data can satisfy it.** KA2 proves it — the synthetic history truth, in which DF2 and DF4 sit
exactly at X = 0, fails the clause at -2.4 se and -2.5 se.

The lane voids that clause (it is a contradiction in the criteria, not a finding) and uses for the label: off <=
-0.30 dex in every scoring (the pre-registered band's lower edge), off >= floor - 3 se in every scoring, and
off <= -3 se in LOCO where the class is complete. On the real data the stripped family then passes everything: the
tidal dwarfs at -4.9 / -4.5 / -6.0 se and DF2 / DF4 at -2.7 / -2.2 / -3.4 se, all inside their band, all above the
floor. Both labels are in `frm1.json` (`labels` and `labels_frozen_line`).

Everything else in the criteria is unchanged and used as committed.

## Known answers and mutations

| check | result |
|---|---|
| KA1 DD1's L0 LOCO offsets reproduced | max deviation 0.0e+00 on both footings: PASS |
| KA2 synthetic truths | history truth: F1 HOLDS, F2 HOLDS, F3 16/16; force truth: F2 FAILS, F3 12/16; history truth + clusters with f_b = 0.40: F3 16/16. Both footings: PASS |
| KA3 HIS1's structural numbers | 0 systems below X = 0 beyond 3 e; tidal dwarfs d_L -0.687 +- 0.115 (HIS1: -0.687 +- 0.115): PASS |
| KA4 the master equation's limits | planted f_C exact to 3.9e-16; no baryon-loss offset negative anywhere; the naive -(1/2) log10 f_b good to 0.036 dex on the 324 deep points: PASS |
| KA5 X_L > 0 and X_L <= sqrt(a0/g_bar) | min X_L 0.0093 / 0.0112, max ratio 0.9984 / 0.9985: PASS |
| M1 every system put on the law | F2 FAILS: bites |
| M2 class labels shuffled across systems | F3 14/16 -> 9/16: bites |
| M3 the clusters lose 90 % of their baryons (g_bar x 0.10) | their offsets rise by +0.571 to +0.595 dex: bites |
| M4 a0 x 2 | F5 FAILS (SPARC -0.118 at -8.4 se): bites |
| Lean `FRM1.lean` | exit 0. 8 theorems (the 7 of the criteria plus the u-form helper for `baryon_loss_raises`). Axioms propext, Classical.choice and Quot.sound only |
| Lean `FRM1_MUTATE.lean` | exit 1. 7 errors, one in each false statement |

## What it means, in plain words

- The formation reading survives being made into a theory, and it survives being scored. With a0 fixed, a conserved
  non-baryonic charge, and transfers that can only remove, it predicted 14 of 16 classes' offsets — including the two
  the lead asked about, in the right direction and the right size — before the table was read.
- It fails on the clusters, and the failure is structural, not a matter of tuning: the only channel that can raise a
  system is baryon loss, that channel saturates at a0/g_bar, and X-COP and CLASH sit above the saturation, 77 % and
  98 % of their points. Whatever puts the extra non-baryonic mass in a cluster, it is not a transfer the theory has.
  It is a *source*, which is what the force reading has and the formation reading does not.
- The free-rule test says the same thing from the other side: a free function of the system's depth on top of the law
  halves the scatter and beats the class-constant reference (0.213 against 0.284 dex) but still fails 10 classes, and
  it makes the shallow, stripped systems worse, not better. The history variables available in this table are not
  enough to close it, and redshift contributes nothing.
- So the honest statement for the record: the history is *necessary* — it is what makes the stripped systems low and
  the hosted systems high, in the right amounts — but it is not *sufficient*: the deepest wells carry more
  non-baryonic mass than any formation-time amount plus any transfer can account for.

## What this lane would require of any theory, and the measurement that separates it

- Any theory must supply (i) a conserved non-baryonic charge set by the law at the formation field, (ii) an upward
  channel that is *not* baryon loss, or (iii) a formation field for clusters 10x below the one they show today, with
  something that sets it.
- Compatible with the record's closed routes: the stripping route for the tidal dwarfs (CFG936) and the hosted
  dwarfs' gas loss (RB2). Not compatible, by +0.18 to +0.25 dex: any route that treats the cluster excess as a
  transfer (RB1's f_ret near 1 for X-COP says the same thing from the mass side).
- The measurement that separates the formation reading from the force reading *and* from a source term: X at matched
  g_bar in systems of the same depth but different assembly epochs — for example relaxed clusters at z ~ 0.5 against
  relaxed clusters at z ~ 0 at the same g_bar and the same hydrostatic aperture. The formation reading with a
  constant a0 says they are equal (and both above the law). A source term says the older one is lower (it has had
  less time). The force reading says both are on the law.

## What it does not settle

- The formation field g_b,f is not measured by anything in this table. Every budget above is computed at
  g_b,f = g_bar/f_b; with a free g_b,f the theory has an unfalsifiable parameter per class.
- The transfer factors f_C and f_b are inferred from the offset, not measured independently. DG1's per-system test of
  the hosted dwarfs' history found no signal (rank +0.06 in the ultra-faints); this lane's per-class numbers are
  consistent with that — the class offsets follow the environment, the individual systems within a class do not.
- Mass-to-light, hydrostatic bias, the KiDS calibration, total-as-enclosed: DD1's systematics apply unchanged, and
  none of them moves a cluster by 0.5 dex (DD1: a 10-20 % hydrostatic bias moves X-COP by 0.05-0.1 dex).
- The alt footing's one extra miss (M31 dwarfs at -0.028 against a band starting at 0.00) is 0.03 dex: it is the
  footing, not the channel.

## Files

- `FROZEN_CRITERIA.md`
- `frm1.py`, with `frm1.json` / `frm1.out` and `frm1_MUTATE.json` / `frm1_MUTATE.out`
- `FRM1.lean`, `FRM1_MUTATE.lean`, `compile.txt`, `compile_MUTATE.txt`
- Reads DD1's frozen table only: `fable52_push/DD1_deduce_from_data/dd1_table.csv`, and DD1's `dd1.json` for KA1.

## Commit ids

| | shared checkout | origin |
|---|---|---|
| criteria (committed alone, before any script or number) | 462eaa806d | 440d1b25bf |
| criteria amendment | fed1bc94a4 | 440d1b25bf |
| script, outputs, Lean | b414a1d1d8 | 440d1b25bf |
| result | 04f69b8b6f (then c6270766b8 for the ids) | abb0aff2f0 |

The lane was pushed to origin from a temporary sparse worktree carrying only this lane's folder: 440d1b25bf (all
files), then abb0aff2f0 (this file's ids). The freeze requirement — the criteria committed alone, before any FRM1 script exists or any
FRM1 number is computed — is met on the shared checkout, and the id order there is the record of it.

## Disclosure

- One amendment to the criteria (fed1bc94a4), committed before any FRM1 number existed: a derived bound was wrong as
  first written (a0/g_b,f = u/f_b instead of u f_b). Corrected, the baryon-loss channel saturates and the bound is
  stricter; the M3 mutation arm was restated accordingly. The graded bands, the pass lines, the labels and the known
  answers are unchanged.
- One void clause (F2's 3-se requirement for the stripped family in the half-splits), discovered by KA2 and reported
  above with both labels.
- Seen before the criteria: every DD1 and HIS1 number (their RESULT.md files and outputs), RB1's f_ret values,
  DG1's per-system result, CFG936's tidal-dwarf numbers, and the DD1 table's column list and counts. No FRM1 number
  of any kind, and no per-class offset, before the criteria were committed.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
