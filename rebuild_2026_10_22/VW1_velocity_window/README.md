# VW1_velocity_window: WINDOW EMPTY on the canonical footing, post-result and resting on the Υ floor of 0.50

Criteria `FROZEN_CRITERIA.md` (c7c964581d), `AMENDMENT_A1.md`, post-result. Not blind. κ = ½ FITTED. A family result on these inputs, not a no-go theorem. Adopts nothing. Not theory closed. Nothing here says the data favour the framework.

## Question
Is there any velocity today v0 at which a light fermion passes both HF1's SPARC line and gate 1, for any m, on a Fermi-Dirac shape?

## Gate 1 against v0 (`vw1_b.out`), line unchanged
| v0 km/s | plik | shear | σ8 | S − S_min (line 25) | Read |
|---|---|---|---|---|---|
| 0.25 | 581.9 | 103.2 | 0.821 | 0.3 | PASS |
| 0.5 | 582.1 | 103.8 | 0.810 | 1.1 | PASS |
| 1 | 583.4 | 106.7 | 0.776 | 5.5 | PASS |
| 2 | 588.6 | 117.8 | 0.692 | 22.3 | PASS |
| 4 | 624.5 | 149.1 | 0.550 | 91.8 | FAIL S |
| 8 | 848.5 | 208.6 | 0.393 | 386.8 | FAIL CMB, shear, S |

So the upper edge lies in [2, 4). HF1's thermal cells, about 14 km/s at 11.8 eV, sit far beyond it. The fail in HF1 is the velocity, not the need for a particle as such. P(k, z = 0) at v0 2 is half the v0 0.25 cell's at k 0.27 h/Mpc, which is well below the forest's scales. That is a warning only; no forest verdict here.

## SPARC against m (`vw1_a2.out`), canonical; v0 at omega_f 0.13
| m eV | v0 | rms | Υ | tilt | M_f/M_b at R_last | Read |
|---|---|---|---|---|---|---|
| 3.74 | 62.9 | 0.0548 | 0.52 | +0.03 | 0.001 | PASS |
| 7 | 27.3 | 0.0578 | 0.51 | +0.04 | 0.005 | PASS |
| 11 | 14.9 | 0.0606 | 0.51 | +0.03 | 0.029 | PASS |
| 20 | 6.72 | 0.0634 | 0.45 | +0.02 | 0.149 | FAIL Υ |
| 50 | 1.98 | 0.0645 | 0.41 | −0.15 | 0.423 | FAIL Υ |
| 300 | 0.18 | 0.0646 | 0.40 | −0.15 | 0.424 | FAIL Υ |

v_min lies between 6.72 and 14.9 km/s, above gate 1's edge below 4. The gap is at least a factor of about 1.7, after the small omega_f correction. On alt every m fails Υ, including where the fermion is negligible, because the law alone reads 0.44 there, so alt doesn't separate anything.

## How firm this is
- **It rests on one line.** Only Υ >= 0.50 closes the window. rms and tilt pass or sit at the edge everywhere (tilt −0.15 is at the line). By eye from the tables, not run, a floor near 0.41 to 0.43 would open it. DA1 already found the Υ window soft. So the honest statement is: at v0 <= 2 km/s the fermion costs about 0.10 in Υ, and the window needs discs that light.
- **R4 flatters the slow end.** R4 has no contraction. A slow species falling in would put more mass in discs than this, so the Υ cost above is a lower estimate, and LC1's measured response says it would.
- **Post-result.** The frozen disc requirement misread RM2 (see A1), and its replacement was chosen after seeing that. m grid coarse.
- **Controls.** K_hf1_cell reproduces HF1's plik within 0.0002. K_m_indep gives d exactly 0: the equations scale, so it checks my parameter mapping and little else. K_integral and K_planted pass. MUTATE wasn't run on A2 or B, and Stage A's frozen MUTATE wasn't run either: a departure, stated.
- **Shape.** Fermi-Dirac only in B. HF1's V-cold cells land consistently (σ8 0.374 at m 11.8, S − S_min 455).

## What it says
This is the old conflict in a new form. Slow enough for the early universe means enough mass in discs to push Υ below the floor. No m, on this shape, avoids that on the record's Υ window.
