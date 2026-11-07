# GL3 RESULT: the web-line side re-read with the Limber kernel corrected. Most labels HOLD; five numbers and two lanes' labels MOVE (reported, pending owner)

Criteria: FROZEN_CRITERIA.md. It was committed locally as 96f207f4ce before any run. Because the push was slow, it
reached origin as 76b04675b7 after the runs had started (disclosure 1). The gate is GL2 CONFIRMED (d0c3692fc6), so the
moves below are reported. **Nothing is rewritten:** the owner decides. Adopts nothing. Kappa = 1/2 FITTED; not theory
closed. Both footings graded, never pooled.

## Method

- Every lane's own script was run unchanged in a scratch sandbox:
  - closure_2026_11_06 and closure_2026_11_07 come from origin/main via `git archive`;
  - data is symlinked from the checkout;
  - the builder is `gl3_sandbox.sh`.
- The sandbox copy of QX3 iter2's `limber_ratio` carries one environment switch (`gl3_iter2_kernel_switch.patch`):
  - **old**: as committed;
  - **new**: the weight multiplied by chi^4, which restores the k^-4 of the lensing potential;
  - **k2**: the MUTATE, chi^2.
- `gl3_compare.py` compares every numeric leaf of each lane's JSON against the committed file. It writes
  `gl3_compare.json`. Run logs are in `logs/*.txt` (machine paths stripped).

## Checks

- **KA (gating): PASS for all 16 outputs.** The old kernel reproduces every leaf of every committed JSON: the largest
  relative difference is 4.5e-16, over about 24,800 leaves.
- **MUTATE (gating): BITES.** On SV5 iter_1 the S(L) values are:

  | L | old | new | k2 |
  |---|---|---|---|
  | 30 | 74.87 | 41.63 | 68.63 |
  | 100 | 74.79 | 32.42 | 58.59 |
  | 400 | 74.60 | 26.65 | 48.44 |

  k2 differs from both old and new by much more than 1e-2. It also gives different labels, for example SV5 iter_3
  H-native reads NO-GO under k2 and WINDOW-CONDITIONAL under new.
- **LD1 (S10), static check: unaffected.** D1 uses CLASS's lensed C_L^phiphi (`X_of` -> `raw_cl`). LD1 imports the
  iter2 library but never calls `limber_ratio`.

## Per statistic (old -> corrected; canonical / alt)

| id | lane | statistic | old | corrected | k2 | label |
|---|---|---|---|---|---|---|
| S1 | SV5 iter_1 | W1 web amplitude r (line 1.072) | 74.74 / 89.36 | 32.53 / 38.66 | 57.63 / 68.80 | **HOLDS** (W1 FAIL) |
| S1 | SV5 iter_1 | W2 shape dchi2 (line 4) | 0.019 / 0.019, PASS | 33.5 / 34.1, FAIL | 18.8 / 19.0 | **MOVES** (PASS -> FAIL; NO-GO FOR CLASS W HOLDS) |
| S1 | SV5 iter_2 | every leaf | | unchanged (0 of 180) | | **HOLDS** |
| S1t | SV5 T0.2 | latest z at which a Jeans length of 30 / 100 / 1000 Mpc may switch on | none / none / none | 2.0 / 1.5 / 0.75 | | **MOVES** (late stiffening now tolerated) |
| S1t | SV5 iter_3 H-flat | M* dchi2 | 543.6 | 740.4 | 203.7 | **HOLDS** (NO-GO FOR CLASS) |
| S1t | SV5 iter_3 H-native (a0 tracks rho_DE, CFG689) | M* / K-mono dchi2 | 876.7 / 541.7, FAIL | 0.016 / 0.52 | 6.45 / 10.1, NO-GO | **MOVES: FAIL -> WINDOW-CONDITIONAL** |
| S1t | SV5 iter_3 H-CPL (reported only) | M* / K-mono dchi2 | 780.7 / 359.7, FAIL | 0.036 / 0.52 | 16.5 / 14.3 | **MOVES: FAIL -> WINDOW-CONDITIONAL** (reported row) |
| S2 | WL1 | q_pop vs 0.0354 (r_pop = (1+q)^2 vs 1.072) | 0.936 / 1.079 | identical | identical | **HOLDS**, kernel-free (only the KA reference to SV5's r moves) |
| S3 | OQ1 | F_web,max (web row YES iff < 1); S1 | 0.00481 / 0.00435; DEAD | 0.00798 / 0.00720; DEAD | 0.00563 / 0.00508 | **HOLDS** |
| S3 | OQ2 | label; F_web,max; SEPARATED | NO VERDICT; 0.00481 / 0.00435 | NO VERDICT; 0.00798 / 0.00720 | | **HOLDS** |
| S4 | NA1 I5 | W1 r, readings A and B | 72.2-89.4 | 27.4-38.7 | 50.5-68.8 | **HOLDS** (FAIL) |
| S5 | FA2 C1 | web r | 74.74 / 89.36 | 32.53 / 38.66 | | **HOLDS** (FAIL) |
| S5 | FA2 C2 | L_max (largest L2 with r <= 1.072) | 0.3 / 0.3 Mpc | 1.0 / 1.0 Mpc | 0.3 / 0.3 | number **MOVES**; label **HOLDS**: KiDS at 1 Mpc is -0.074 / -0.074 against 0.05, still FAIL |
| S6 | FA3 I1 | W1 r at tau_gal | 75.39 / 78.77 | 19.12 / 18.75 | 51.13 / 52.51 | **HOLDS** (FAIL); I1 / I3 / I4 labels unchanged. The reported (ungraded) scan's longest tau now passes W1 (r 1.044) |
| S7 | EW2 iter_2 | mu_w (smallest mu passing W1) vs mu_h 0.063 | 10 / 10 (gap x160) | 0.63 / 1.0 (gap x10 / x16) | | number **MOVES**; label **HOLDS** (NO-GO FOR CLASS A_mu; window still empty); W2 flips PASS -> FAIL on the law rows |
| S8 | QX27 | G6b dchi2 over n 3.5-8 | 231-1059, FAIL | 108-340, FAIL | 23-114 | **HOLDS** (G6c is kernel-free and FAILS) |
| S8 | QX28 | G6b dchi2 | 140.1 / 70.0, FAIL | 0.006 / 0.004, PASS | 0.42 / 0.30 | **MOVES** (G6b FAIL -> PASS); G6 **HOLDS** FAIL through the kernel-free G6a |
| S8 | QX28 | largest K passing growth vs galaxies' K_min (1.58e-6 / 1e-6) | 1e-7 | 1e-6 | 1e-6 | number **MOVES** (alt now meets K_min; G6a still FAILS) |
| S8 | QX29 | medium dchi2 | 0.0 PASS (A-web CONDITIONAL) | 0.0 | | **HOLDS** (only the controls move) |
| S9 | QX31 B / C / D | gap; label | 2.5 dex; ROBUST x3 | 0.9 dex; ROBUST x3 | 1.5 dex | **HOLDS** (its "reproduce the record" flags read False by construction, because the record used the old kernel) |
| S10 | LD1 | D1 CMB-lensing chi^2 | 46.3 / 53.0 | not kernel-dependent | | **HOLDS** |

## Reading

- **Every web row HOLDS.** NA1, FA2 C1, FA3, OQ1/OQ2, EW2 and SV5 W1 still fail the 1.072 line, by a factor of 18-39
  instead of 72-89. WL1 is kernel-free.
- The 0.0354 line is the 1.072 amplitude line, mapped by r_pop = (1 + q)^2. The 1.072 line comes from the PR4 amplitude
  error sigma_A, not from the kernel, so it stands.
- **What moves is late suppression.** With the k^-4 restored, PR4's shape at L <= 400 is nearly blind to suppression at
  k >~ 0.3 /Mpc at low z. This is GL1's finding, seen here in the following:
  - SV5 T0.2 now tolerates late Jeans lengths of 30-1000 Mpc below z 0.75-2;
  - QX28's G6b passes;
  - SV5 iter_3's a0(z)-tied history reads **WINDOW-CONDITIONAL** in place of FAIL;
  - FA2's web cut-off loosens to 1 Mpc;
  - EW2's gap shrinks to x10-16.
- **The moves do not open a door on their own.** SV5 iter_3 is a growth and CMB-lensing gate only:
  - WINDOW-CONDITIONAL there means a history passes T1 and K-mono, with the window still to be met;
  - every cluster, group and KiDS row of the record stays as graded;
  - CE2 failed the late-heated window on X-COP, the groups and the Bullet, and those gates are kernel-free;
  - QX28 still fails G6a.
- The corrected kernel is stricter in one place: SV5 W2. The law on the web now also fails the shape test.

## Consequence for PAPER70 v1.1 (reported, not rewritten)

The erratum line should give these corrected values:
- the web r values: NA1 72-86 -> 27-39, FA3 75.4 / 78.8 -> 19.1 / 18.8;
- EW2's window: mu >= 10 -> mu >= 0.63 / 1.0, gap x160 -> x10 / x16;
- OQ2's F_web,max: 0.00481 / 0.00435 -> 0.00798 / 0.00720;
- FA2's L_max: 0.3 -> 1.0 Mpc.

All of these labels HOLD. The label moves pending the owner are SV5 iter_1 W2, SV5 T0.2, SV5 iter_3 H-native / H-CPL,
and QX28 G6b.

## Disclosures

1. The criteria commit (96f207f4ce) was made before any run. Its push to origin (76b04675b7) landed after the first
   runs, because a worktree push was slow.
2. In the new and k2 sandboxes, WL1's and FA2's own known-answer checks pin SV5's committed r (74.74 / 89.36). Under
   the corrected kernel those checks stop the scripts by design ("KA FAIL: stop"). In those two sandboxes the pinned
   constants were set to the same-kernel SV5 value: 32.5 / 38.7 for new, 57.6 / 68.8 for k2. No other line was
   edited, and the old sandbox is unedited.
3. OQ2 reads OQ1's oq1.json. The first OQ2 run ran in parallel with OQ1 and without its stage flags. It was rerun
   (--stage0, then --main) after OQ1 finished, and only that rerun is reported.
4. The "pristine" reference tree also carries the kernel switch, which defaults to old. It was never run, so its JSONs
   are the committed files byte for byte.
5. Peak RSS was at most 1.64 GB (EW2 iter_2). No 1024^3 run was live.

Adopts nothing. Kappa = 1/2 FITTED; not theory closed.
