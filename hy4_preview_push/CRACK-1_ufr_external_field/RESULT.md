# CRACK-1 RESULT: three readings of the ultra-faint / X-COP pair (2026-11-12)

Criteria 16bc0102de (committed alone, before any script or number) + one disclosed amendment 52d62227df, committed
before this file. Table 441824e854 (DD1's, frozen, unchanged: 3419 points, 626 systems, 16 classes). TEST lane,
quarantined: adopts nothing, relabels nothing, registers nothing. Footings never pooled (canonical a0 9.3603e-11,
alt 1.1312e-10 m/s^2).

## The headline

| reading | predicts UFD (dex) | predicts X-COP (dex) | measured UFD / X-COP | verdict (canonical / alt) |
|---|---|---|---|---|
| **R1 STRIPPING-INVERTED** | **-1.19** (band -1.55 .. -0.30) | **0.00** (-0.30 .. +0.30) | +0.592 / +0.496 | **FAILS THE PAIR / FAILS THE PAIR** |
| **R2 EXTERNAL-FIELD-REGISTERED** | **-1.19** (kappa 0.037 at z_f 8) | **-0.23** (kappa 0.354 at z_f 1) | +0.592 / +0.496 | **FAILS THE PAIR / FAILS THE PAIR** |
| **R3 FELL-IN (at the host's field)** | **-1.15** (band -1.37 .. -0.80) | **0.00** (-0.30 .. +0.30) | +0.592 / +0.496 | **FAILS THE PAIR / FAILS THE PAIR** |

**None of the three survives the pair. Same label on both footings, and the same label under the frozen criteria
line and under the amended one.** All three predict the ultra-faints LOW; the ultra-faints are measured HIGH at
+0.59 (6.1 se canonical, 5.6 se alt). Two of the three predict X-COP at zero; X-COP is measured at +0.50 (22.3 se
canonical, 20.3 se alt).

The sharpest single test is the **differential**: measured d(UFD) - d(X-COP) = **+0.096 +- 0.100** (canonical),
**+0.087 +- 0.101** (alt) — the ultra-faint is, if anything, *above* the cluster. All three readings predict it
*below*, by 0.70 to 1.19 dex. The pair is not two problems; it is one ordering that every one of the three gets
backwards.

## The pair, as the record has it

| | MW ultra-faints (31) | X-COP (7) | CLASH (20, for reference) |
|---|---|---|---|
| LOCO offset, canonical | **+0.5920 +- 0.0977** (6.1 se) | **+0.4955 +- 0.0222** (22.3 se) | +0.5528 +- 0.0232 (23.9 se) |
| LOCO offset, alt | **+0.5520 +- 0.0979** (5.6 se) | **+0.4650 +- 0.0229** (20.3 se) | +0.5237 +- 0.0232 (22.6 se) |
| A->B / B->A, canonical | +0.507 / +0.597 | +0.571 / +0.482 | +0.553 / +0.551 |

A note on the numbers as they were handed to this lane: the "22.5 and 24.0 se" belong to **X-COP (22.3) and CLASH
(23.9)**, not to the two members of the pair. The ultra-faint's own significance is **6.1 se** (canonical) /
**5.6 se** (alt), because its class scatter (se 0.098 dex over 31 systems) is four times X-COP's. The pair is
+0.59 at 6 se and +0.50 at 22 se.

## The three readings, scored

### R1 STRIPPING-INVERTED — a formation-set amount plus tidal stripping

    X_f = X_L(g_bar),  X = X_f f_C,  f_C <= 1 for the hosted family,  f_C = 1 for the unhosted.

- **Predicted, ultra-faints: NEGATIVE, -1.19 dex** with the record's own calibration of what stripping does
  (f_C = 0.038, the tidal dwarfs' value from FRM1), band from the floor (-1.55) to -0.30. Over the whole range the
  channel allows: f_C = 1 gives 0.00, 0.5 gives -0.29, 0.2 gives -0.65, 0.1 gives -0.90, 0.01 gives -1.42. There
  is no value of f_C <= 1 that gives a positive offset — that is the algebra, certified in Lean
  (`strip_lowers`).
- **Measured: +0.592 +- 0.098.** Miss **+0.892 dex from the band's upper edge, 9.1 se** (canonical); +0.852 dex,
  8.7 se (alt). To get there the master equation needs f_C/f_b = **4.08** at a fixed formation field — the host
  would have had to *add* four times the charge, not strip 96 % of it.
- **Predicted, X-COP: 0.00** (nothing to strip; RB1 measures f_ret 1.06-1.10, so no baryon loss either). Measured
  **+0.496 +- 0.022**: miss **+0.196 dex, 8.8 se** (canonical); +0.165 dex, 7.2 se (alt).
- **The inversion inside the hosted family** (reported, and it is the same finding in a second place): R1 requires
  the most-stripped satellites to be the lowest. The measured hosted order is the other way round —
  ultra-faints **+0.592**, Coma UDGs +0.319, M31 dwarfs +0.090, MW bright dwarfs **+0.065**. The ultra-faints are
  0.53 dex *above* the bright dwarfs they are supposed to sit below.
- **FAILS THE PAIR** on both footings, on both grading lines.

### R2 EXTERNAL-FIELD-REGISTERED — the ambient field at assembly sets the normalisation

    X_f = kappa(z_f) X_L(g_amb,f),  kappa = Phi = (1+z_f)^(-3 alpha),  alpha in [0.5, 1],  g_amb,f = g_bar.

- **Predicted, both members: NEGATIVE**, because kappa <= 1 for every z_f >= 0 and every alpha >= 0
  (`kappa_pos_le_one`, `d_of_kappa_le_one_nonpos`). At the pre-registered epochs: ultra-faints (z_f = 8)
  **-1.19 dex** (kappa 0.037, alpha 0.5); X-COP (z_f = 1) **-0.23 dex** (kappa 0.354).
- **The epoch factor, in the terms the lane was asked about.** At z_f ~ 1 the reading supplies
  kappa = **0.354** (alpha 0.5) to **0.125** (alpha 1); the quoted 0.42 is alpha = 0.5 at z_f = 0.78, inside the
  pre-registered range. What the pair *needs* is kappa = **4.08** for the ultra-faints and **4.51** for X-COP
  (canonical; 3.70 and 3.97 on alt) — i.e. **+0.61 and +0.65 dex of enhancement, on the far side of kappa = 1**.
  Supplied and required are on opposite sides of 1: **0.97 dex apart at z_f ~ 1** and **1.06 dex apart at the
  ultra-faints' own epoch** (alpha 0.5), up to 1.65 dex at alpha = 1. The reading's kappa is not too small by a
  factor; it has the wrong sign.
- **Measured: +0.592 / +0.496.** Misses **+1.692 dex (17.3 se)** and **+0.686 dex (30.8 se)** canonical;
  +1.652 (16.9 se) and +0.655 (28.5 se) alt.
- **The ordering is backwards, and that is the structural kill.** kappa is monotone decreasing in z_f
  (`kappa_antitone_z`), so the earlier-forming class must be the lower one: predicted d(UFD) - d(X-COP) =
  **-0.97**. Measured **+0.096 +- 0.100**. Miss **1.07 dex, 10.6 se**. Every corner of the (alpha, z_f) box fails:
  z_f 4/0.3 gives -0.94 / -0.10; z_f 12/2 gives -1.31 / -0.31; alpha = 1 anywhere gives -1.45 to -1.55 for the
  ultra-faints. There is no epoch pair in the box that puts the early class above the late one.
- **FAILS THE PAIR** on both footings. (M3, alpha = 0: the predicted offsets go to exactly 0 and the leg still
  FAILS — the epoch factor is not the only thing wrong; the sign of the whole reading is.)

### R3 FELL-IN — the amount set when the galaxy fell in, at the host's field

    X_f = X_L(g_host(R_f)),  g_host(d) = V_c^2 / d,  V_c = 200 km/s (X1 / RB2's MW host),  d = LVD distance_host.

- The 31 ultra-faints sit at **11.8 to 371.6 kpc** from the Galaxy (median 64.0); the host's field there is
  **3.5e-12 to 1.1e-10 m/s^2** — at the median distance 2.03e-11, i.e. **270 times the satellites' own field**
  (7.5e-14), and across the sample **46 to 1459 times**. Fixing the amount at a field that much stronger can only
  lower the system (`d_stronger_field_lowers`).
- **Predicted, ultra-faints: NEGATIVE, -1.15 dex**, band -1.37 (12 kpc) to -0.80 (372 kpc). **Measured +0.592**:
  miss **+1.392 dex, 14.2 se** (canonical); +1.352, 13.8 se (alt). The amount would have had to be fixed at
  **6.7e-15 m/s^2 — 11 times BELOW the ultra-faints' own field**, not 270 times above it. The reading's field and
  the required field differ by a factor of 3031 (**3.48 dex in field**).
- **The generous edges do not rescue it.** V_c = 180 km/s, the host at 25 % of its present mass at infall, and
  infall at twice the present distance — all three at once — give **-0.72 dex**. Still 1.31 dex below the
  measurement.
- **The within-class prediction fails too.** R3 says satellites that fell in closer sit lower, so d must rise with
  the host distance. Measured rank(log10 d_host, d) over the 31 systems = **-0.215** (p 0.25) — the wrong sign,
  and consistent with zero. This is the same place DG1 found no per-system history signal (rank +0.06), now tested
  against the host distance directly.
- **X-COP: 0.00** (no host, no infall; the reading's only escape is the cluster's ambient field at assembly being
  below its present internal field, which is the reported parameter phi, not part of R3). Measured +0.496:
  miss **+0.196 dex, 8.8 se**.
- **FAILS THE PAIR** on both footings.

## Why the pair is a crux: the shape, measured

LOCO offsets ordered by the class's median field (canonical; alt differs by at most 0.04 dex):

| class | g_bar | d_L | | class | g_bar | d_L |
|---|---|---|---|---|---|---|
| KiDS | 7.4e-14 | +0.137 | | faint rotators | 5.5e-12 | -0.239 |
| **MW ultra-faints** | **7.5e-14** | **+0.592** | | massive spirals | 6.9e-12 | +0.066 |
| M31 dwarfs | 3.2e-13 | +0.090 | | **X-COP** | **2.0e-11** | **+0.496** |
| MW bright dwarfs | 6.3e-13 | +0.065 | | **SPARC** (anchor) | **2.5e-11** | **+0.004** |
| Coma UDGs | 7.0e-13 | +0.319 | | **CLASH** | **3.4e-11** | **+0.553** |
| LG field dwarfs | 1.1e-12 | -0.090 | | RC100 | 1.6e-10 | +0.088 |
| NGC 1052 UDGs | 2.1e-12 | -0.843 | | ATLAS3D | 2.8e-10 | +0.070 |
| groups | 2.2e-12 | +0.161 | | | | |
| tidal dwarfs | 3.6e-12 | -0.687 | | | | |

**Not monotone in the field: 9 direction changes** along the 16 classes. Against the anchor at g_bar ~ a0, the
offset rises **+0.588 dex** to the ultra-faints and **+0.492 / +0.549 dex** to X-COP and CLASH. Any formation map
d = F(v) with v monotone in field or mass is excluded by the two rises alone (`monotone_cannot_be_valley`); and
the two variables on which the ultra-faints and the clusters are *not* on opposite sides of the anchor —
"hosted?" and "gas-poor?" — put the anchor on the same side as one of them. That is the sense in which the pair
kills every monotone formation map, and it is a measurement, not an argument.

## What the pair would need, and what it selects for

Graded by nothing. Per class, the field g_f at which the amount would have to have been fixed to give the measured
offset, as a fraction of the class's own present field, phi = g_f/g_bar (canonical / alt):

| class | d_L | phi | f_C/f_b (R1) | kappa (R2) |
|---|---|---|---|---|
| **MW ultra-faints** | +0.592 | **0.063 / 0.076** | 4.08 | 4.08 |
| **X-COP** | +0.496 | **0.070 / 0.084** | 4.51 | 4.51 |
| CLASH | +0.553 | 0.050 / 0.060 | 5.73 | 5.73 |
| Coma UDGs | +0.319 | 0.219 / 0.265 | 2.19 | 2.19 |
| KiDS | +0.137 | 0.532 / 0.643 | 1.38 | 1.38 |
| ATLAS3D | +0.070 | 0.477 / 0.576 | 1.72 | 1.72 |
| RC100 | +0.088 | 0.440 / 0.531 | 1.84 | 1.84 |
| groups | +0.161 | 0.451 / 0.545 | 1.53 | 1.53 |
| MW bright dwarfs | +0.065 | 0.723 / 0.874 | 1.19 | 1.19 |
| M31 dwarfs | +0.090 | 0.648 / 0.783 | 1.25 | 1.25 |
| **SPARC (anchor)** | +0.004 | **0.845 / 1.021** | 1.11 | 1.11 |
| LG field dwarfs | -0.090 | 1.543 / 1.865 | 0.80 | 0.80 |
| faint rotators | -0.239 | 4.04 / 4.88 | 0.44 | 0.44 |
| tidal dwarfs | -0.687 | 177 / 214 | 0.038 | 0.038 |
| NGC 1052 UDGs | -0.843 | (X ~ 0: no finite field) | 0.009 | 0.009 |

**The two ends of the table agree on one number.** The ultra-faints, X-COP and CLASH — a 10^5 M_sun satellite, a
10^14 M_sun cluster at z 0.06 and a 10^15 M_sun cluster at z 0.2-0.7 — all require the amount to have been fixed
at **g_f ~ g_bar/15** (phi 0.05 to 0.08 on both footings, i.e. the system's radius shrinking by a factor 3.5 to 4.5
afterwards), while the settled discs require phi ~ 1 (no contraction). The pair does not point at stripping, at
the epoch, or at the host: it points at **a contraction factor that is ~15 in field for the smallest and the
largest systems alike and ~1 for discs**. That reading was not pre-registered here and is not graded; it is the
direction the pair leaves open, and it is a statement about the assembly path, not about mass or epoch.

## Known answers and mutations

| check | result |
|---|---|
| KA1 FRM1's LOCO pair reproduced | max deviation 0.0e+00 on both footings: PASS |
| KA2 the readings' neutral algebra (kappa = 1, f_C = 1, g_f = g_bar) | max |d| 0.0e+00: PASS |
| KA3 host distances | 31 / 31 ultra-faints matched in the LVD table, all finite and positive: PASS |
| KA4 synthetic truths | strip: UFD -1.116, R1's leg and G3 HOLD; fell-in: UFD -1.149, R3's leg HOLDS; epoch: UFD -1.194, X-COP -0.225, R2's both legs HOLD. All three: PASS |
| KA5 every system on the law | max |class offset| 0.0e+00, both footings: PASS |
| M1 the 31 ultra-faints stripped of 90 % of the charge | d_L(UFD) = -0.903; R1's UFD leg flips to HOLD: bites |
| M2 the host distances reversed across the ultra-faints | R3's predicted UFD offset -1.149 -> -0.855 (0.294 dex); the within-class rank flips to +0.215: bites |
| M3 alpha = 0 (kappa = 1) | predictions exactly 0; R2's UFD leg still FAILS: bites |
| M4 a0 x 2 | all three labels unchanged, G3's sign unchanged (+0.096 -> +0.065): bites |
| Lean `CRACK-1.lean` | exit 0. 10 theorems, axioms propext, Classical.choice, Quot.sound only |
| Lean `CRACK-1_MUTATE.lean` | exit 1. 14 errors, at least one in each of the 10 false statements; no `sorry` |

## What it means, in plain words

- The formation reading's one algebraic sentence — *an amount fixed at a field weaker than the system's own raises
  it, at a stronger field lowers it* — settles all three readings at once. Stripping, an early epoch and infall
  into a host are all ways of making the fixing field *stronger*; the pair needs it *weaker*, and by the same
  factor (about 15) in a 10^5 M_sun satellite and a 10^15 M_sun cluster.
- The ultra-faint leg is not a close call in any of the three: 9 se, 17 se and 14 se, all with the wrong sign.
  Whatever makes the ultra-faints sit +0.59 high, it is not a transfer, an epoch or a host.
- The X-COP leg is the one FRM1 already failed (+0.496 against a +0.320 baryon-loss ceiling, 77 % of its points
  above a0/g_bar), and none of the three readings adds a channel that reaches it: R1 and R3 give it 0.00 and R2
  gives it -0.23.
- So the honest statement for the record: the pair is a **source** result, not a history result
  (`pair_needs_source` — d > 0 means X_f > X_L(g_bar), more non-baryonic mass than any amount fixed at any field
  plus any transfer can supply). A history can lower a system; it cannot raise these two.

## What this lane does not settle

- z_f is not measured by anything in this table. R2 is graded at pre-registered epochs from the record's assembly
  picture; the whole (alpha, z_f) box was swept and no corner reaches the pair, but a *non-monotone* epoch
  function is not excluded by this lane (it is excluded as a monotone map, which is the reading as stated).
- g_amb,f is not measured for the clusters. phi = 0.070 is what the offset requires; nothing here says what set it.
- The host field uses RB2 / X1's flat-rotation-curve MW (V_c = 200 km/s). The generous edges (V_c 180, a quarter
  of the host's mass, infall at twice the distance) are reported above and fail by the same margin.
- The ultra-faints' class scatter is large (se 0.098 dex, 31 one-point systems) and DD1's systematics apply
  unchanged; the 6.1 se is a class median against that scatter, not a per-system result.

## Files

- `FROZEN_CRITERIA.md`, `AMENDMENT_A1.md`
- `crack1.py`, with `crack1.json` / `crack1.out` and `crack1_MUTATE.json` / `crack1_MUTATE.out`
- `CRACK-1.lean`, `CRACK-1_MUTATE.lean`, `compile.txt`, `compile_MUTATE.txt`
- Reads DD1's frozen table only (`fable52_push/DD1_deduce_from_data/dd1_table.csv`), FRM1's `frm1.json` for KA1,
  and the record's host distances (`real_research/data/dsph/lvd_dwarf_mw.csv`, the file X1 and RB2 used).

## Commit ids

| | shared checkout | origin |
|---|---|---|
| criteria (committed alone, before any script or number) | 16bc0102de | - |
| amendment A1 | 52d62227df | - |
| script, outputs, Lean | 0f9b164d78 | - |
| result (this file, before the ids were filled in) | 2f5168716d | - |
| the whole lane, pushed from a temporary sparse worktree | - | e079ba54e6 |

The freeze requirement — the criteria committed alone, before any CRACK-1 script exists or any CRACK-1 number is
computed — is met on the shared checkout, and the id order there is the record of it. **Collision note:** another
lane working in this repository at the same time swept this folder's in-progress files into an unrelated commit
(089d304ecb, "CRACK-1: external-field reading of the UFR residual...", which carries FINAL7F's files as well as
this lane's). The content it captured was this lane's own and is unchanged; nothing of this lane was lost or
overwritten, and the lane's four commits above are the authoritative record.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
