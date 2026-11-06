# QX21: the hot/cold step's origin. NO VERDICT as frozen; every independent channel has the same sign

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Criteria: FROZEN_CRITERIA.md (55374ee57a), committed and pushed
before any script. Script: qx21.py (one thread, seconds). Outputs: qx21.out / qx21.json, and qx21_MUTATE.* for M2.

**Label: NO VERDICT.** The frozen rule needs T1 to read STEP SEEN (at least 3 sigma). The lensing split reads
+0.158 +- 0.064 dex, which is 2.46 sigma, so it falls in "weak". Nothing contradicts the step:

- No channel shows it vanishing.
- The weak-lensing split, which uses no hydrostatic mass, has the same sign and about half the size.
- Pressure-supported cold dwarfs show a step of the same size in one of the two graded classes.
- The record's own second mass method for clusters says correcting hydrostatic bias would make the step larger, not
  smaller.

## T1. KiDS-1000 early/late lensing RAR (Brouwer+2021 Fig. 8; CFG61's K1 bins 8-14)

- **The split:** early types (u-r >= 2.5) sit above late types at the same g_bar in all 7 bins. The per-bin difference
  d runs from +0.07 to +0.31 dex.
- **The amplitude:** D = +0.158 +- 0.040 (stat) +- 0.05 (sys, the early class's M_* +-0.1 dex), giving +- 0.064 in
  total.
  - The law predicts D_law = +0.0002, from CFG61's lens-by-lens law stacks.
  - So D - D_law = +0.158, or 2.46 sigma. That is "weak" by the frozen line (>= 3 sigma needed). On statistical errors
    alone it is 4.0 sigma.
- **Size against QX20's step (+0.35 in g_N): smaller.** It is 0.19 dex below, outside 2 sigma (0.128).
- **M1 (all 128 per-bin early/late swaps):** the 95th percentile is +0.094, and only 0.8% of swaps reach D. The control
  bites, so T1 has the power to see a type step.

## T2. Pressure-supported cold dwarfs (velocity-dispersion masses, no X-ray; LW1 per-system plain-law offsets, no EFE)

| Class | canonical median [95% CI], minus SPARC | alt | Label |
|---|---|---|---|
| bright M31 dSphs (N 25) | +0.227 [+0.106, +0.420], +0.199 | +0.187 [+0.068, +0.382], +0.188 | present, both footings |
| MW classical dSphs (N 8) | +0.245 [-0.022, +0.572], +0.217 | +0.206 [-0.058, +0.532], +0.207 | absent by the line (CI reaches the anchor; N 8) |
| MW ultra-faints (reported) | +0.592, +0.565 | +0.552, +0.553 | present (tides and equilibrium open) |
| LG field dwarfs (reported) | +0.046, +0.019 | +0.007, +0.007 | absent |

- **Overall:** T2 is "mixed" on both footings. Both graded dSph classes sit about +0.2 above SPARC, the same size as the
  X-ray ellipticals' +0.21 / +0.19. The MW classical interval is too wide (N 8) to pass the line. The isolated LG field
  dwarfs show no step.
- **Shuffle:** a sign-flip about SPARC's anchor reaches the observed graded-dSph median in 0.17% of draws.

## T3. Hot-system masses by a second method (read, not recomputed)

- **LF1 (22272b3b32):** KiDS shear on eRASS1 clusters gives about 0.12 dex more mass at fixed gas than X-COP's
  hydrostatic share.
- **RF3:** A2142, the one X-COP cluster with a lensing mass in the record, agrees with its hydrostatic mass.
- **Result: METHOD-SIGN EXCLUDED.** The record's lensing masses are at least the hydrostatic ones. Correcting any
  hydrostatic bias would raise the hot systems' offsets.
- **Caveat:** the two methods are measured on different samples. LF1 itself cannot say which is off.

## Reading (post-data, not the label)

- **Where the step shows up:**
  - with no hydrostatic mass at all (weak lensing, +0.16, smaller than X-COP's step);
  - in cold pressure-supported dwarfs (about +0.2, same as the ellipticals);
  - possibly larger in clusters, if hydrostatic bias is real.
- **Why that matters:** the plain law's miss is not a quirk of X-ray masses. It tracks pressure-supported or early-type
  systems, and it grows from about +0.16-0.2 (early-type galaxies, dSphs) to +0.45 (clusters).
- **The baryonic escape stays open:** CGM hot gas in early types. CFG61 R4 says the law fits the lensing split if early
  types carry 1-1.5 M_gal of extra baryons. That is untested here.
- **What would decide T1:** more KiDS area, or a tighter early-type M_* calibration than +-0.1 dex. The systematic is
  larger than the statistical error.

## Known answers and controls

- **KA1:** CFG61 C1's u-r split chi2 is 119.93 against 119.9 +- 0.5, PASS. The K1 data match CFG61's printed stacks to
  3.7e-4.
- **KA2:** LW1's MW-classical median +0.2445 is reproduced exactly, PASS. In the MUTATE run it fails, as expected,
  because the offsets are Newton there.
- **M1:** bites (above).
- **M2 (Newton, qx21_MUTATE.\*):** every dSph class moves by 1.0-1.5 dex (> 0.3), so it bites.

## Scope

- The KiDS split is colour (early/late) for isolated lenses at log M_* <= 11. The X-ray classes are hotter and more
  massive. The test is the same sign and a comparable size, not identity.
- No action-level mechanism is graded here. This is a statement about where the law misses.

Kappa = 1/2 FITTED; not theory closed.
