# SK1 (spin key): FAIL / FAIL. At fixed M* and g_N, slow rotators sit +0.060 dex above fast rotators, a third of the +0.20 hit line, and dispersion alone carries it

TEST lane, quarantined. kappa = 1/2 FITTED; not theory closed. Adopts nothing. No dark-matter particle. Footings graded
separately, never pooled. No download.

- Criteria: `FROZEN_CRITERIA.md`, committed alone and pushed before any script or number (origin `8fd9c516e3`), unamended.
- Script: `sk1.py` -> `sk1.out` / `sk1.json` (main, exit 0: known answers pass) and `sk1.py --mutate` ->
  `sk1_MUTATE.out` / `sk1_MUTATE.json` (exit 1 by design). One thread, 44 s, peak RSS 0.24 GB. The run is deterministic.
- Post-freeze diagnostics, not graded: `sk1_posthoc.py` -> `sk1_posthoc.out` / `.json` (written after the FAIL, to check it).

## Label

| | canonical (a0 1.2e-10) | alt (a0 1.1e-10) |
|---|---|---|
| **D = slow - fast**, matched (M*_IMF, g_N), dex | **+0.0602 [+0.0369, +0.0811]** | **+0.0601 [+0.0369, +0.0812]** |
| cells / galaxies / slow (slow in matched cells) | 52 / 6056 / 536 (492) | 52 / 6056 / 536 (492) |
| **Label** | **FAIL** (D < +0.10) | **FAIL** (D < +0.10) |

The whole 95 % interval is below the +0.10 FAIL line, on both footings. The two footings agree to 1e-4, because at fixed
g_N the law's prediction is the same for both classes. The a0 value only moves the absolute level: median rho is slow
+0.105 / fast +0.119 (canonical) and +0.112 / +0.128 (alt), at median y = g_N / a0 of 1.64 / 1.79.

**What the FAIL means under the frozen rules:** the rotation selector fails. With it, every selector class in the
catalog has a verdict and none passes. **The selector catalog is closed.**

## Per-bin SHAPE across lambda_Re

Each bin is matched against the fast rotators outside it. Values are dex with 95 % intervals; both footings agree to 1e-3.

| lambda_Re bin | n | D_b | cells |
|---|---|---|---|
| [0.00, 0.10) | 451 | +0.058 [+0.031, +0.081] | 48 |
| [0.10, 0.20) | 470 | +0.034 [+0.014, +0.067] | 66 |
| [0.20, 0.30) | 350 | -0.021 [-0.050, +0.023] | 64 |
| [0.30, 0.45) | 498 | -0.010 [-0.042, +0.013] | 81 |
| [0.45, 0.60) | 807 | +0.005 [-0.013, +0.022] | 122 |
| [0.60, 1.00] | 3480 | -0.003 [-0.019, +0.011] | 142 |

The Spearman correlation of D_b with the bin centre is S = -0.486. A spin key needs S <= -0.6, and both lowest bins need
D_b >= +0.10; they are +0.058 and +0.034. This is not a continuous trend with spin. It is a small step of 0.03-0.06 dex
confined to lambda_Re < 0.2, and it is flat above that. The OLS slope of rho on lambda_Re (with log M* and log g_N as
covariates, beside) is -0.118 / -0.117 dex per unit lambda. That is 0.07 dex across the occupied lambda range.

## Controls (each needs D >= +0.10 to hold; reported because the label is FAIL)

| Control | canonical D [95 %] | alt | reading |
|---|---|---|---|
| (a1) T15 field singletons (542, 68 slow, 13 cells) | +0.051 [-0.023, +0.168] | +0.051 | evaluable; below line |
| (a2) T15 satellites (484, 36 slow, 7 cells) | +0.119 [-0.037, +0.379] | +0.119 | evaluable; interval wide, contains 0 |
| (a) reported: T15 group centrals (162, 30 slow) | +0.056 [-0.084, +0.294] | +0.056 | |
| **(b) matched (M*, Sigma_Re) instead of g_N** | **+0.0096 [-0.003, +0.031]** | +0.0095 | dispersion alone carries the +0.06 |
| (c1) Re_MGE >= 4 arcsec (4401, 443 slow) | +0.053 [+0.028, +0.081] | +0.053 | seeing does not hide a larger step |
| (c2) Eps_MGE < 0.4 both classes (3308) | +0.057 [+0.033, +0.079] | +0.057 | inclination does not either |
| (d) red sequence, u - r >= 2.5 (695, 152 slow) | +0.053 [+0.006, +0.111] | +0.053 | gas-poor subset agrees |

Control (b) is the key one. At fixed M* and fixed Sigma_Re, slow and fast rotators sit on the law together to
+0.010 dex. That is KU2's UNIVERSAL, recovered on SK1's footings and IMF-controlled residual. The +0.06 dex seen at fixed
g_N is the fact that slow rotators of the same mass and size have higher dispersions. That is the dispersion key, which
HX1 already graded NO LADDER. Spin adds nothing beyond it.

## Robustness and disclosed rows

- **Second-best JAM model:** +0.0563 / +0.0562 (FAIL as well).
- **Each JAM model alone (HDU 2-11):** +0.014, +0.025, +0.039, +0.055, **+0.155, +0.181**, +0.047, +0.056, +0.079, +0.077.
  - The HDU 6-7 pair is the stellar-plus-halo pair that KU1 and KU2 flagged. It reads UNDECIDED-sized (+0.155 / +0.181)
    but is the best fit for 0.2 % / 0.6 % of the sample.
  - Chosen-model fractions, HDU 2-11: 0.029, 0.079, 0.103, 0.125, 0.002, 0.006, 0.062, 0.060, 0.190, 0.344.
- **IMF readings (disclosed, not knobs):**
  - Chabrier as stored +0.0747 / +0.0747.
  - Salpeter everywhere +0.0738 / +0.0737.
  - Posacki (primary) +0.0602 / +0.0601.
  - The record's IMF control removes 0.015 dex. FAIL on every IMF reading.
- **Stellar-mass column:** elpetro instead of sersic gives +0.0675 [+0.040, +0.085], FAIL (MUTATE M3).
- **Gas flag:** none. D is 0.04 dex below the line, not within 0.03 of it. Gas omission biases D low by about 0.02 dex
  at most, which cannot reach +0.10.

**Post-freeze verification of the FAIL** (`sk1_posthoc.*`, not graded).
- Every JAM model x every IMF reading (30 readings per footing) spans +0.014 to +0.198.
- None reaches +0.20. Eight reach +0.10: HDU 6-7 on all three IMFs, and HDU 10 on Chabrier and Salpeter.
- The most generous corner of the whole grid is HDU 7 x Salpeter, at +0.198 [+0.157, +0.257].
  - It combines a model the data prefer for 0.6 % of galaxies with the IMF reading the record does not use.
  - Even there the reading is UNDECIDED, not a hit.
- Matched on M* alone (no g_N): +0.047. Unmatched median slow - fast: -0.014 / -0.016.

## Known answers (all PASS)

| Check | result | line |
|---|---|---|
| KA1 ST1/QX26 X-ray elliptical IMF offset (Humphrey 2006 input, record's hosted a0) | +0.093043 / +0.074253 vs +0.093043 / +0.074252 (\|d\| 4.5e-7 / 4.8e-7) | 1e-4 |
| KA2 KU2 replay (its own conventions, ln) | +0.023332 / +0.025383, \|d\| 0 / 2e-17; n 6056, 536 slow, 27 cells | 1e-5 |
| KA3 ATLAS3D III published slow count | 36 of 260 (14 %) | exact |
| KA3 DynPop record count (KU1/KU2 cuts) | 536 slow / 5520 fast | exact |
| KA4 the law's own prediction returns rho = 0 | max 0.0 | 1e-12 |

- **KA1 caveat.** The brief asked for ST1's offset "on the ATLAS3D table". ST1's X-ray elliptical number comes from the
  Humphrey 2006 table, not ATLAS3D, so KA1 replays it on ST1's own input with SK1's alpha(sigma) inside QX26's formula.
- **KA3 caveat.** DynPop's own paper is not on disk, so its published slow fraction could not be read. The DynPop count
  is checked against the record instead.

## MUTATE (`sk1_MUTATE.*`): all bite, both footings

| Twin | canonical | alt | required |
|---|---|---|---|
| M1 lambda_Re shuffled within 0.2 dex M* bins | +0.0122 [-0.016, +0.031] | +0.0122 [-0.016, +0.031] | \|D\| < 0.05, interval contains 0: PASS |
| M2 +0.2 dex planted on slow g_dyn | +0.2602 [+0.237, +0.281], rise +0.2000 | +0.2601, rise +0.2000 | rise 0.20 +- 0.03, excludes 0: PASS |
| M3 elpetro mass column | +0.0675, FAIL | +0.0675, FAIL | label holds: PASS |

The test has the power to see a +0.20 dex spin step. The 95 % half-width is 0.022 dex, and the plant comes back exact.

## ATLAS3D replication row (not graded)

- 258 of 260 ATLAS3D III rows join the FJ table (2 dropped: no FJ row or a missing cell); 187 have qual >= 1, 19 of them slow.
- At the frozen 0.2 x 0.1 dex cells, no cell holds 2 slow and 2 fast, so D is undefined: no power as a replication.
  - The printed bootstrap interval comes from cells that only duplicated galaxies can fill. It is not meaningful.
- Unmatched median slow - fast: -0.053 dex.

## Hand estimates, graded

| HE | estimate | outcome |
|---|---|---|
| HE-a, spin key real at the size the hot rows need | +0.20 to +0.30 | **MISS**: +0.060 |
| HE-b, IMF the whole story: after the IMF control | 0 to +0.05 | **MISS, narrowly**: +0.060 |
| HE-b, IMF the whole story: before the IMF control | +0.05 to +0.10 | **HIT**: Chabrier +0.075 |
| HE-c, control (b) near KU2 | +0.01 | **HIT**: +0.0096 |
| HE-d, label | FAIL both | **HIT** |

## Reading

Measured spin is not a key for the law's residual. At fixed stellar mass and Newtonian acceleration, the slowest rotators
sit only +0.06 dex above fast rotators, the excess is confined to lambda_Re < 0.2 rather than tracking spin, and it
vanishes (+0.010 dex) once Sigma_Re is matched. So it is the dispersion key that HX1 already graded NO LADDER, not a new
selector. The kill stated in advance did not have to be invoked: there is no selector hit to which a second variable could
add the amount. The hot rows need +0.2 to +1.4 dex, and spin supplies at most 0.06 dex at r_h in the IFU sample.

The stated limits stand:
- Sphere-enclosed JAM mass is model output.
- r_h accelerations sit near a0 (y about 1.6-1.8).
- This grades rotation at r_h in MaNGA galaxies at z about 0.03, not in clusters, dSphs or UDGs. Those have no
  integral-field spin on disk.

**Record note for the orchestrator:** the 11-09 pre-read listed rotation as the one selector with no verdict. KU2
(10-22 rebuild) had already graded slow vs fast at matched (M*, Sigma_Re) on this same file as UNIVERSAL (+0.01 dex).
SK1 confirms that reading at matched g_N and adds the spin-binned shape.
