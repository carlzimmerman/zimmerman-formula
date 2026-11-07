# KX1: QX10's KiDS kill of the late-heated window, re-graded with a joint systematic budget at 100-300 kpc

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. TEST lane (cold dark energy; no particle). Footings never pooled.
- Criteria: FROZEN_CRITERIA.md (db8ffafa83), committed alone before any script or number.
- Grader: kx1.py -> kx1.json / kx1.out; kx1.py --mutate -> kx1_MUTATE.* (M1, the window at 4x sector mass).
  One thread, 23 s, peak RSS 0.19 GB. Nothing downloaded.

## Label (frozen rule): NO VERDICT on both footings. The reading under it: the kill HOLDS wherever the window has power, and no cell softens

The frozen controls require M1 (window at 4x mass) to read KILL HOLDS for every cell. It does for C1, C2 and C4, but
not for C3. C3's core already fills r_ta and evaporates the excess (QX10: it keeps 44 / 50 %), so 4x the captured mass
leaves the retained halo, and W_b, unchanged (0.036-0.069 dex). That gap is in the control's design, not in the data.
It is disclosed, and it fixes the frozen label at NO VERDICT.

| Cell | canonical | alt |
|---|---|---|
| C1 (2.61 Mpc, p 4.25) | NO POWER by the power rule (W >= 2 sigma_tot in 1/4 bins); z > 2 in 1/4 | NO POWER by the power rule (1/4); **z > 2 in 4/4** |
| C2 (1.47, 3.5) | **KILL HOLDS** (z > 2 in 4/4) | **KILL HOLDS** (4/4) |
| C3 (8.25, 5.625) | NO POWER (W 0.04-0.05 dex) | NO POWER (W 0.04-0.05) |
| C4 (2.15, 3.75) | **KILL HOLDS** (z > 2 in 2/4) | **KILL HOLDS** (4/4) |

**No cell reads KILL SOFTENS on either footing.** The cells with power (C2, C4, and C1 at 4x) are killed.
C3 is not killed at 100-300 kpc. Its QX10 G6 fail (-0.153) came from radii beyond 300 kpc. With the full budget at
all radii it reads z <= 1.9 / 2.3, and NO POWER. C3 is the cell that QX10 reported at X-COP +0.32 / 0.36 rms (CE1's gate).

## Per bin (canonical, C2 shown; every cell and footing is in kx1.out)

E_b is the posterior excess of the data over the law after the central corrections (kSZ gas P1, two-halo at b_cap/2).
W_b is the window's excess over the law. The line is E_b + 2 sigma_tot: the largest window excess the data allow.

| Bin (log M*, r kpc) | raw data - law (no gas, no 2h) | E_b (posterior) | sigma_tot | line | W_b C1 / C2 / C3 / C4 | z C2 |
|---|---|---|---|---|---|---|
| 1 (9.4, 122-285) | +0.029 | -0.207 | 0.127 | +0.047 | 0.185 / 0.204 / 0.036 / 0.194 | +3.23 |
| 2 (10.45, 131-231) | +0.196 | +0.022 | 0.100 | +0.221 | 0.168 / 0.221 / 0.041 / 0.190 | +2.00 |
| 3 (10.7, 131-232) | +0.150 | +0.006 | 0.096 | +0.197 | 0.169 / 0.237 / 0.039 / 0.196 | +2.42 |
| 4 (10.9, 125-292) | +0.182 | +0.053 | 0.091 | +0.236 | 0.190 / 0.243 / 0.051 / 0.210 | +2.08 |

On alt the posterior excesses are -0.249 / -0.019 / -0.034 / +0.013, and the lines are 0.007 / 0.181 / 0.158 / 0.196.

**The line the budget implies is 0.05-0.24 dex (canonical) and 0.00-0.20 (alt), not QX10's flat 0.05.** The window's
0.17-0.25 dex sits at or above it in most bins. The joint budget loosens QX10's line, but not by enough.

Budget per bin (window, canonical C2, dex):
- stat 0.027-0.077
- stellar-mass shift 0.080-0.095. This is the largest term.
- kSZ gas range 0.014-0.023
- isolation 0.027
- two-halo 0.002-0.009
- calibration 0.006

## Why the hot gas does not rescue the window

The deduction expected the hot-gas systematic to absorb the excess. It does absorb it, but for the law:
- Raw data sit 0.15-0.20 dex above the law in bins 2-4. That is Brouwer's excess.
- Every kSZ-normalised CW6 profile (P1-P6, B1-B5) moves that excess to -0.05 to +0.08 dex. Gas measured by the kSZ
  supplies the 100-300 kpc excess on its own.
- The same gas sits under the window too. The window then adds its 4.2 M_b halo on top and over-predicts.
- Without gas, the window still over-predicts bins 2-4 (raw W 0.27-0.35 against raw excess 0.15-0.20).
- The two-halo term is negligible inside 300 kpc (b_cap/2 T2H is about 1 % of the ESD).

## Known answers and controls

- KA1: QX10's G6 shifts for all 8 cell-footings, and its baselines, recomputed through qx10_i2.py's own grade_cell:
  max |d| 0. PASS.
- KA2: the CW6 gas interpolator at grid nodes, |d| 0. PASS.
- KA3: sector 0 gives W = 0 exactly. PASS.
- M2 (the law itself): z_law +1.50 / -0.21 / -0.06 / -0.62 (canonical) and +1.80 / +0.18 / +0.36 / -0.16 (alt). PASS.
- M1 (window x4): KILL HOLDS for C1, C2 and C4 on both footings (4/4 bins). It reads NO POWER for C3, as explained
  above, and so **DOES NOT BITE** -> frozen NO VERDICT.

## Reported readings

- **Projected ESD** (model g_obs = 4 G Delta Sigma of the 3D effective mass, instead of QX10's local estimator): W
  C1 0.13-0.19, C2 0.23-0.26, C4 0.18-0.21, C3 0.01-0.03 dex. Projection does not save C1, C2 or C4.
- **All radii** (QX10's range, same budget): every cell reads NO POWER by the power rule. C2 still has z 2.0-2.8 in
  every bin.

## Checked as hard as a pass (where the reading is fragile)

1. **Bin 1 (log M* 9.4) uses CW6's log M* 10.0 gas row**, a frozen extrapolation. It pulls E_1 to -0.21. Every cell's
   z_1 is above 3 there.
   - Without bin 1, C2 still holds on both footings (canonical z 2.00, 2.42, 2.08; the first is 2.0008).
   - C4 canonical would read SOFTENS (z 1.74 / 2.12 / 1.79). C4 alt still holds (2.19 / 2.60 / 2.29).
   - So canonical C4's hold rests on the extrapolated bin.
2. **The power rule makes C1 NO POWER even where z > 2 in 4/4** (alt). That is because W_b < 2 sigma_tot. The rule was
   frozen and is applied as written.
3. **The sector is solved around QX10's stellar point-mass host.** Gas is not counted in the captured mass
   (f_cap R M_b) or in the host potential. Counting it would make the halo heavier and tighter, so this choice is
   generous to the window.
4. **The isolation term is derived:** CFG96's sigma_A20 times the fraction of the signal a 0.18 dex split can move
   (0.027 dex). CFG96 tested the early/late split, not the total signal.

## One sentence

With a joint budget drawn from the record (kSZ gas, two-halo, isolation, stellar-mass shifts, calibration), the
isolated-lens data at 100-300 kpc sit on the law (posterior excess -0.25 to +0.05 dex), because the kSZ-measured hot
gas itself explains Brouwer's raw excess. The late-heated window's 0.17-0.25 dex halo stays above the implied line in
every cell with power, and no cell softens. The frozen label is NO VERDICT only because the 4x MUTATE cannot bite on
the evaporating cell C3, which KiDS cannot see at 100-300 kpc.

Kappa = 1/2 FITTED; not theory closed.
