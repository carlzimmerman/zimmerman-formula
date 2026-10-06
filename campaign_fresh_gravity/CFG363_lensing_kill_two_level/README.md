# CFG363: lensing kill test of the two-level retention picture

Criteria: `FROZEN_CRITERIA.md`, committed alone first in 35b3aa30d. This builds on cold_mass cm11 (9f0c92398, matter only) by adding the framework's own baryon-sourced nu_mono phantom, and by keeping the moved cold mass (mass-conserving envelope of width R_s).

**Frozen verdict: KILLED.** All 24 phantom-ON brackets hit KILL on both CMB lensing (mean ratio 3.3 to 13.7 over L 40-763) and shear.

**But the kill is not specific to the two-level picture.** Robustness checks run after the freeze, and labelled as such:

| variant | CMB-lensing ratio | S8_eff |
|---|---|---|
| EFE-capped phantom, g_e = 0.01 a0, two-level | 2.99 to 3.14 | 1.34 to 1.48 |
| EFE-capped phantom, g_e = 0.03 a0, two-level | 1.92 to 2.04 | 1.09 to 1.24 |
| EFE-capped phantom, **no sorting (r = 1)** | 2.04 to 3.15 | 1.26 to 1.50 |
| halos ANCHORED to observed lensing, moved cold added as extra real mass | **1.27 to 1.37** | 0.85 to 1.01 |

The measured CMB-lensing amplitude agrees with LCDM to ~2-3%.

**Reading.** Real mass is conserved, so the cosmic cold mass (needed by the CMB at z = 1100) has to be somewhere. The phantom is positive extra lensing mass around every baryonic halo. Put the two together and the scaffold over-lenses, whether the cold mass sits in halos (no sorting) or is moved out (two-level). Even the most charitable accounting (halo lensing equal to observation by construction, moved cold diffuse) is 27-37% high in CMB lensing. Escaping needs the moved cold mass smooth on >~ 30-100 Mpc, which cannot be reached kinematically after z ~ 2. This is the same direction as the record's own AUDIT_SIGMA8 (dd14eb3d3: chassis growth too fast; CMB lensing excludes; MOND-blind dark reading 1.45-2.2x). The framework's native growth makes it worse, not better.

The phantom-OFF rows (cm10's literal question, matter only): CMB lensing passes (0.91-1.00), and S8 shifts -3% to -26% depending on R_s. That brackets cm11's -12% to -19%.

**Scope.** This is a halo-model scaffold on a LCDM halo population (colossus planck18). The phantom is spherical, sourced by point-mass baryons and truncated at r_sw or the EFE radius. It is not the framework-native PM calculation (CFG359/CFG361). Controls 4/4. MUTATE (moved mass dropped) fails T0c, rc 1.

Run: `python3 cfg363_lensing_kill.py` (~6 s).

## Scope correction (appended after the run; no number changed)
The frozen model sources lensing **additively** (baryons + cold + phantom). The record calls that the additive reading, "NOT B" (CFG338 reading A; CFG361 criteria). So CFG363 kills the **additive reading** at the lensing level, in parallel with CFG359's additive growth FAIL. It does **not** test candidate B's T5 max / identity bookkeeping (dark mass = max(M_ph, (Omega_c/Omega_b) M_b)) or reading S. The sentence "phantom + conserved cosmic cold mass over-lenses" holds for additive bookkeeping only.
