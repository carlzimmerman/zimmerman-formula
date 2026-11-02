# HF1_hybrid_fermion: FAILS GATE 1 AT 5 OF 6 m, 1 UNDETERMINED. Gates 2 and 3 run as numbers only also fail. Gate 4 not run

**Label.** Gate 1 fails at m 11.8, 11, 9, 7 and, at fixed helium (A2), 5. m 3.74 is UNDETERMINED: its fit didn't converge. So the frozen DEAD AT gate 1 isn't claimed outright, because that label needs every m to fail. Nothing shown favours m 3.74: its unconverged point has plik 9756.6 and S 9497 above the line's minimum. This kills the family on these inputs, not all light fermions, and it isn't a no-go theorem.

Criteria `FROZEN_CRITERIA.md` (56ab302a4d), alone first. `AMENDMENT_A1.md` (4e2a7564c5), before any graded number, with R8 added before the first fit but committed later. `AMENDMENT_A2.md`, post-result. Not blind. The owner's lift of the no-particle rule covers this lane only; running it adopts nothing. kappa = 1/2 FITTED. Footings never pooled. Not theory closed. Nothing here says the data favour the framework.

## Gates against lines
| Gate | Status | Numbers | Line |
|---|---|---|---|
| 1 Early universe, FD | **FAIL 5 of 6, 1 UNDETERMINED** | Best cell m 11.8: plik 1432.4, p 6e-69; BAO 34.6; shear 267.8 of 101 points, sigma8 0.285; S above RF5's minimum +1041.8 | p >= 1e-3 per channel; S <= +25 |
| 2 Clusters, numbers only, m 5 | **FAIL** | X-COP +0.159, rms 0.251. Keys 3 of 15, G-OUT-Mall -18.33 | |mean| <= 0.05, rms <= 0.10; 15 of 15 |
| 3 Galaxies, numbers only, m 5 | **FAIL on groups** | Groups Z -5.90, BELOW LAW. S, tilt, slope, LT pass, canonical | FG1's lines |
| 4 Structure | **NOT RUN** | Frozen: not run when gate 1 fails. No m passed | |
| 5 Acceptance | **NOT RUN** | A1 R7: no surviving m | |

## Gate 1 (`hf1_g1.out`), Fermi-Dirac at the fermion's own temperature
| m eV | omega_f | N_eff | h | plik /605 | BAO /13 | SN | shear /101 | sigma8 | S - 2324.03 | Label |
|---|---|---|---|---|---|---|---|---|---|---|
| 11.8 | 0.13119 | 4.11 | 0.694 | 1432.4 | 34.6 | 1630.4 | 267.8 | 0.285 | +1041.8 | FAIL CMB, BAO, shear, S |
| 11 | 0.13294 | 4.23 | 0.698 | 1599.1 | 40.2 | 1630.5 | 278.5 | 0.267 | +1224.8 | same |
| 9 | 0.13932 | 4.69 | 0.710 | 2216.7 | 57.2 | 1630.8 | 307.6 | 0.221 | +1889.2 | those + A0 |
| 7 | 0.15175 | 5.63 | 0.737 | 3407.2 | 73.0 | 1631.9 | 341.6 | 0.168 | +3130.8 | those + A0 |
| 5, YHe 0.2454 | 0.17486 | 7.94 | 0.805 | 6185.2 | 36.0 | 1630.3 | 380.7 | 0.103 | +5909.2 | FAIL CMB, BAO, shear, S |
| 3.74, YHe 0.2454 | 0.15070 | 8.95 | 0.816 | 9756.6 | 21.4 | 1634.6 | 407.8 | 0.053 | +9496.8 | UNDETERMINED, unconverged, lowTT inf |

For scale, RF5's dust at z_on 1e6 reads plik 581.7. Failure grows steadily as m falls. It isn't on the line's edge at any m: S misses 25 by over 1000 even against the best cell, and the family's own minimum, printed beside it, is 3365.8.

**Reported variant COLD** (degenerate, same f_max, less N_eff), can't move the label: m 11.8 plik 911.5, S +455.1; 11: 1000.9, +557.2; 9: 1369.1, +962.3; 7: 2108.4, +1754.2. All fail. So a colder spectrum helps a lot and doesn't reach the line in these cells. COLD at 5, 3.74 and all of CHI were unfinished at this commit: `run_g1.sh` is still running; `hf1_g1.out` updates.

## Choice of m (R3, `hf1_g23_select.out`)
No m passes both train lines. X-COP train misses everywhere (+0.167 to +0.199), SPARC train passes everywhere. The fallback rule picks **m 5, omega_f 0.17486**. **Read this with care:** m 5 wins by 0.011 dex because its omega_f is highest, which comes from a very poor CMB fit at fixed helium. So m 11.8, omega_f 0.13119, the best CMB cell, runs beside it as a comparator I added (not in R3).

## Gates 2 and 3, numbers only (`hf1_g23_RUN.out`, `hf1_g23_RUN_m11p8.out`)
| Row, canonical (alt) | m 5 | m 11.8 |
|---|---|---|
| X-COP all, mean, rms | +0.159, 0.251 (+0.128, 0.233) FAIL | +0.178, 0.260 (+0.148, 0.240) FAIL |
| train; holdout mean | +0.167; +0.147 | +0.187; +0.167 |
| by x 0.1, 0.2, 0.3, 0.5, 0.7 | +0.407, +0.290, +0.189, +0.023, -0.117 | +0.418, +0.307, +0.210, +0.047, -0.090 |
| Keys, f* 0.034, gas +0.005 | 3 of 15 (2) | 3 of 15 (3) |
| G-OUT-all, G-OUT-Mall, G-OUT-M3 (h 0.672) | -13.83, -17.55, -13.79 | -12.72, -15.97, -12.14 |
| G-MID-T3, G-IN-Mall | -1.67, +0.52 | -1.08, +0.59 |
| DA1 B = 1, n(z), f* 0.0615, gas +0.111 | 3, 3, 3, 3 of 15 | 4, 3, 3, 3 of 15 |
| SPARC rms, Upsilon, tilt | 0.0568, 0.52, +0.03 (0.0582, 0.44, -0.02) | 0.0617, 0.51, +0.03 (0.0668, 0.41, -0.02) |
| SB slope Z; LT | -0.26; -0.025 | -0.33; -0.029 |
| Groups Z | **-5.90** BELOW LAW (-6.56) | **-5.56** (-6.22) |
| M_f/M_b at R_last, V<100, V>200 | 0.0007, 0.057 | 0.0234, 0.104 |
| Dw, five classes | same as the law: UFD +5.22, FAIL | same |
| IC 1613 E | -0.593, Z -7.9, FAIL, expected | same |

- **The shape is wrong, and scaling can't fix it.** X-COP is short by +0.41 at x 0.1 and over by -0.12 at x 0.7. Less fermion would help the outside and hurt the inside. Retention below fair share wasn't run.
- **NU1's sign warning holds, harder.** The fermion overshoots the lensing outskirts by 12 to 18 sigma. This uses a fair-share isothermal profile (A1 R4), an upper bound on infall, so the OUTER size is reading-dependent.
- **What the law can't do, this doesn't do either at this abundance:** the law's K count was 9 of 15 on its own template. Here it's 3 of 15. The templates differ, so that isn't a like-for-like count.
- **Discs are safe, as the idea says.** The cap keeps discs close to the law, which is the one part that works. Groups are the exception: the law alone reads Z +0.31 and the fermion takes them to -5.90.
- **The cap does no work in clusters.** g_f x 16 moves the cap by exactly 16 and leaves X-COP's mean at +0.1586. Fair share sets the mass there, not Pauli.
- **Lensing at offset peaks, PROVISIONAL inputs, no line.** Offsets are by construction of collisionlessness, not a test. Model over published M_lens (<300 kpc), m 5, gas displaced to gas centred: Bullet main 0.99-1.11; Bullet sub 0.49-0.54; MACS J0025 SE 0.47-0.53, NW 0.44-0.50. A2744's row didn't enter: its table name didn't match, not fixed.
- **Milky Way, expected fail, not solved.** The law's cells read K_z +4.7 to +6.6 sigma (READ X5). The cap permits at most 0.04 (m 5) or 1.3 (m 11.8) Msun/pc^2 more. It only adds.
- **DA1's Upsilon windows** pass at both m, canonical and alt. Alt's S fails FG1's window, as the law's does.

## Controls
Gate 1 (`cells_g1/checks.json`): RF5's cell reproduced, chi2 differences 0, shear 103.21; a 2000 eV fermion recovers RF5's dust, d plik 0.002; omega rule within 3e-3; ncdm precision d 0.03 (line 1.0). Twin, omega_b x 1.1: three known answers FAIL, plik off by 386, exit 1, `cells_g1_MUTATE/`.
Gates 2-3 (`hf1_g23_controls.out`): 10 of 10. Tremaine-Gunn closed form, ratio 1.0; solver grid 0.5 %, fair share and cap held; law limit X-COP +0.467, 0.476; SPARC, LT, groups, Dw, SB slope, CRG1's C4 keys all reproduce with the fermion off. MUTATE (`hf1_g23_MUTATE.out`): g_f x 16 gives cap x 16.000000; cap x 300 planted fails gate 3 on Upsilon 0.43, rms 0.0679, so the planted failure is on Upsilon, not rms. PM controls not built: gate 4 not run.

## Liabilities
No production mechanism. No action. Milky Way and IC 1613 stay with the law. The a0 term is absent from linear FRW, stated. A linear channel can't see any boost MOND gives at late times, which matters for shear's sigma8 of 0.1-0.3, though not for plik, the failure at every m.

## Departures and what wasn't verified
- **QUMOND vs AQUAL** coincide in spherical symmetry with this nu: zero by identity, not computed.
- **Spectrum not frozen.** FD is my reading. COLD's trend suggests no spectrum in that family rescues these m, but other non-thermal spectra weren't tried.
- **sigma is the model's** V_max / sqrt 2, a reading. Measured V_flat on SPARC changes little (rms 0.0555, 0.52, +0.03). Clusters weren't bracketed in sigma. A smaller sigma would concentrate mass, and that's the direction the X-COP shape wants, so this is the main open reading in gate 2.
- **m 5 and 3.74 use YHe 0.2454,** not BBN-consistent at these N_eff, and that number is recalled. m 5's omega_b came out 0.02797.
- **m 3.74 unconverged** at RF5's 10 steps. It wasn't retried.
- **Gate 4.** Not run, as frozen. The forest question the audit left open stays open: nothing here tests raw P1D. The queue would also have refused it: 22 GB free against its 30 GB minimum.
- **Harness details.** r_ta is CRG1's, on its native baryon density. MW is a bound, not a solve. DiskMass not graded. Default-setting CLASS rows behind R8 were overwritten in `hf1_g1_prec.json`: only the ladder from tol 1e-5 is kept; R8's "first pass" numbers are from the session, not on disk. The first grade printed EARLY FAIL over the unrun cells, corrected by A2.

kappa = 1/2 FITTED. Not theory closed.
