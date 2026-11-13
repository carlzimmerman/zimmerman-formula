# JNT1 RESULT: the regime-split joint on data

**NO VERDICT / JOINT COMPLETE ON POWERED ROWS [1.25, 2] (canonical / alt), as frozen.**
Canonical: the required twin TW-H (halo halved) does not bite on row S, so row S has NO POWER and the label is NO VERDICT.
Reading, not graded: the reference layout at the record's halo mass fails the 9 SPARC curves above v_stiff on shape
(outer minus inner -0.087 dex, 4.1 se). That fail holds at every mass-to-light ratio in the bracket. Half that halo fits.
Alt: row S has only 2 galaxies, so NO POWER. The hit rests on G4 alone, plus TRIVIAL and law-equal rows. It is a HIT, not a
pass. It awaits a blind re-grade. The family is post hoc three times over, and both constants stay fitted.
TEST lane. Criteria 00292e1430 (alone, before any script or number); scripts and outputs b5731fd9a5; no amendment.
Footings never pooled. Cold dark energy is a gravitating field component; no particle.

## The whole joint in one table (CARRIED = quoted from the committed file, not recomputed)

| row | power | f 0.75 | f 1.00 | f 1.25 | f 1.5 | f 2 | f 3 |
|---|---|---|---|---|---|---|---|
| **S** SPARC curves above v_stiff (this lane), can / alt | can: twin-limited; alt: none | NO POWER / NO POWER (f-independent) | same | same | same | same | same |
| G1 forest, matter level (SRJ2, CARRIED) | TRIVIAL | holds | holds | holds | not run | holds (0.42 / 0.58) | not run; SRF1 / SRF1R flux reading (ungraded) allows to f ~ 3 |
| Clusters, groups (SRJ2, CARRIED) | TRIVIAL (joint = reference) | holds, FRAGILE (R500) | same | same | same | same | same |
| G2 RC100 (SRJ2 coverage; SRJ3, SRJ4 data, CARRIED) | coverage only; data NO POWER | coverage FAILS (31 / 22 discs) | same | same | same | same | same |
| G4 KiDS by type, early z (SRJ2 joint, CARRIED) | powered | FAIL (+2.142 / +2.172) | FAIL (+2.012 / +2.037) | PASS (+1.843 / +1.852) | joint not run; SRH1 no-split PASS (+1.58 / +1.62), NOT JOINT | PASS (+1.420 / +1.142) | not run (SRH1 f inf PASS) |
| SPARC below v_stiff (this lane) | powered (law's PD1 line holds) | law-equal | law-equal | law-equal | law-equal | law-equal | law-equal |

On SPARC below v_stiff, every last radius sits inside f x R_fold for f >= 0.410 (PD1 M_b; 166 / 173 galaxies) or f >=
0.467 (FLD1 M_b, all 175), on both footings. So these galaxies are the law's at every f in the grid.

## Row S in detail (fixed Upsilon disc 0.50 / bulge 0.70, all points to the last radius)

Statistic: residual log10(V_obs^2 / V_mod^2) = log10(g_obs / g_mod), weighted by (V / eV)^2. This is PD1's and QX8's
residual. Class line from DD1, as SRJ3 used it: |median| <= 0.10 and <= 3 se. S3: rms_ref <= rms_law + 0.02.

| canonical (n 9, 249 points) | reference | law + T, same galaxies |
|---|---|---|
| S1 offset (median d_i), se | -0.028, 0.041: holds | -0.009, 0.042: holds |
| S2 shape, outer minus inner half, se | **-0.087, 0.021: FAILS (4.1 se)** | -0.037, 0.013: holds |
| S3 pooled rms (mean) | **0.1265 (-0.046): FAILS** against 0.1265, by 3e-5 | 0.1065 (+0.024) |
| word | **REFERENCE FAILS** (S2, S3) | fits the same lines |

- **Members (KA4 = srj2_rc.json):** ESO563-G021, NGC0801, NGC2955, NGC5371, NGC6195, UGC02487, UGC02885, UGC09133,
  UGC11455. FLD1-M_b subset: NGC6195, UGC02487, UGC02885. All 9 have a negative reference shape (-0.025 to -0.169). The
  reference over-predicts the outer curve relative to the inner one, because the NFW cold mass keeps rising outward
  while the curves stay flat. Worst cases: NGC0801 (-0.169), NGC5371 (-0.146), UGC09133 (-0.121, 68 points to 108 kpc).
- **Twins (canonical):** TW-N (no cold component): off +0.271, shape +0.196, FAILS, bites. TW-D (2 X): off -0.093, shape
  -0.142, rms 0.188, FAILS, bites. **TW-H (X / 2): off -0.006, shape -0.030, rms 0.1073, REFERENCE FITS, does not bite.**
  The gate can see the halo mass: double fails, half fits, record fails. But the frozen rule says a non-biting twin
  means NO POWER. That word stands.
- **Mass-to-light bracket (canonical, reference word unchanged, so not FRAGILE):**
  - U 0.35: off +0.031, shape -0.143. FAILS (S2). The law fails too (off +0.105).
  - U 0.65: off -0.120, shape -0.044. FAILS (S1, S3). The law fits.
  - QX8 per-galaxy fit: off -0.018, shape -0.074, rms 0.105 against the law's 0.052. FAILS (S2, S3). The law fails S2
    alone (-0.028 against 3 se of 0.026).
- **Other conventions (reported):** with SRJ2's convention (reference + T), the shape is -0.105 and the rms 0.127. The law
  without T gives shape -0.031 and rms 0.104.
- **Alt (n 2: UGC02487, UGC02885; NO POWER by n < 5):** reference off +0.043, shape -0.100, rms 0.117. The law + T gives
  off +0.097, shape -0.056, rms 0.150. Twins are not applicable.
- **Known answers:**
  - KA1 PASS: 175 galaxies; the law at fixed U 0.50 gives 0.1124 / +0.0504 (no T) and 0.1181 / +0.0594 (T) on canonical,
    0.1029 / +0.0239 on alt, equal to QX8.
  - KA2 PASS: SRJ2's reported reference reading is 0.06396 / 0.05593.
  - KA3 PASS: SRJ3's zC 400569 d is -0.0061041. Alt: 22 / 22 discs are reproduced.
  - KA4 PASS.

## What is TRIVIAL, what has no power, what was not addressed

- **TRIVIAL:** the forest at matter level, clusters and groups. The joint hands these back to the reference, so it
  predicts nothing new there.
- **NO POWER:**
  - Row S on alt (2 galaxies).
  - Row S on canonical as frozen (TW-H).
  - G2's data rows (SRJ3, SRJ4).
  - G2 itself is a coverage line, not data.
- **SRH1R:** found that G4 cannot see f (lensing passes at f 0.05 and at f 0). So the alt window [1.25, 2] is set by
  one gate that cannot weigh f.
- **Not computed:** the joint at f 1.5 and 3 for G1 and G4.
- **Not addressed:**
  - the weak-lensing amplitude;
  - hosted dwarfs;
  - the Milky Way rows;
  - the two fitted constants (kappa, share 5.41);
  - why v_stiff should switch the layout, and the halo's X (56 to 59, unbracketed). A smaller X moves the boundary and
    the membership.

## Estimate against the outcome

My estimate before any number:
- canonical off +0.05 to +0.09: **wrong** (-0.028);
- shape within 0.05: **wrong** (-0.087);
- P(NO VERDICT via TW-H / TW-D) 0.30: TW-H did not bite;
- alt NO POWER: right;
- alt hit [1.25, 2]: right.

## What the joint is, and what closes

As frozen, nothing closes on canonical. The ungraded canonical reading is plain. Above v_stiff, the joint's own reference
halo (X M_b with X about 59) is too heavy in the outer parts of the most massive SPARC discs: all 9 curves fall below it
outward. A halo about half as massive fits them, as well as the law does. So the regime-split joint in SRJ2's form, with
FRZ1's halo mass for galaxies above v_stiff, does not survive the full rotation curves on canonical. Keeping the family
needs a third choice, a lighter reference halo for those galaxies, and that choice would be fitted. On alt the same two
galaxies show the same shape, but two galaxies carry no power. The alt hit is the rule "law inside 1.25 to 2 R_fold of
galaxies with v_vir <= 288.1 km/s, cold-dust layout elsewhere". It rests on KiDS early-type lensing that cannot see f.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
