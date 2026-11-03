# RS1_required_source: NO SOURCE FORM. The required source doesn't collapse on any one variable; 3.5e9 source forms tried, none within a factor of 2 of every line. X-COP and the ultra-faint dwarfs are the wall

Criteria `FROZEN_CRITERIA.md` (2c0a6f6f70), committed alone. Scripts `rs1_rows.py`, `rs1_map.py`, `rs1_search.py`, `rs1_hf.py`, `run_arms.sh`. Outputs `rs1_map.out/.json`, `rs1_hf.out/.json`, `runs/arm_*.json`. MUTATE: `rs1_map_MUTATE.*`, `runs/arm_canonical_U50_mutate.json`. κ = ½ FITTED. A family result within this grammar and these caps, not a no-go theorem. Not theory closed. Nothing here says the data favour the framework.

## Part 1, what the law needs added (`rs1_map.out`), M_x = (g_obs^2/(g_obs + a0) - g_b) r^2/G
Canonical, Υ 0.5/0.7:

| Class | n | M_x/M_b 16/50/84 % | Share M_x < 0 | Tag |
|---|---|---|---|---|
| SPARC | 3166 | −0.34 / +0.05 / +0.68 | 0.45 | |
| LITTLE THINGS | 20 | −0.53 / −0.09 / +2.83 | 0.50 | |
| Groups | 63 | −0.78 / +0.22 / +2.77 | 0.48 | ASSUMED-GAS |
| X-COP | 35 | +2.83 / **+4.42** / +5.71 | 0.00 | HSE |
| Lensing, R ≤ 0.3 Mpc | 28 | +0.00 / +0.55 / +1.29 | 0.14 | SIS, PROVISIONAL |
| Dwarfs | 82 | −0.09 / +3.34 / +35 | 0.18 | gas 0 |

- **Discs:** the requirement is centred on zero and half the rows are negative. At the low Υ reading SPARC rises to median +0.25, 31 % negative. Alt: −0.04, 54 % negative.
- **Clusters:** X-COP needs 4.4 times its baryons under HSE, and every row positive. Correlated with gas (+0.93) and stars (+0.95) alike, so the data can't tell which it follows.
- **Milky Way and IC 1613,** read from the record's rows, not inverted: IC 1613 needs negative (A10 −0.59 dex, Z −3.9). RQ3's A15 reads K 70.1 against 66.4, Z +0.9, on its R form; the record's X5 cells read +4.7 to +6.6σ high. A positive source can't lower either.
- **Collapse test:** no variable collapses it on any footing or reading. The best, y_g = g_gas/a0, leaves 0.59-0.63 dex against a line of 0.20, against a shuffled null of 0.63-0.68. A worst class sits 0.35-0.39 dex off any monotone curve. Phase density Q = ρ_x/σ³, descriptive and partly circular, leaves 0.53-0.60. Only rows with M_x > 0 enter, so noise in discs contributes.

## Part 2, the search (`runs/`)
6,000-member pool of 24,348 at level 2, all 6,000 run in every arm; 8.64e8 forms per arm (four bases, all pairs, four ops, both orders of − and /), four arms plus a shuffled control. **Stage 1 hits: 0 in every arm. Control: 0.** Holdouts and keys have no survivor to run on, and near misses don't go to Stage 2 under these criteria.

Best score (largest value/line across gates; 1 passes):
| Arm | Best | Form | Over line |
|---|---|---|---|
| canonical Υ 0.5 | 2.29 | M_bt (x/π² + f² √y_g) | X 2.1, S 2.3, LT 2.1, G 1.7, UFD 1.6 |
| canonical low | 2.12 | M_bt log1p(0.5/y_s) / ((1+π)(1+f)) | X 2.0, S 2.1, LT 2.0, UFD 2.1 |
| alt Υ 0.5 | 2.35 | M_bt (1/(1+y_g/ell) + f²/(1+x)) | X 2.3, S 2.2, LT 1.4, UFD 2.2 |
| alt low | 2.15 | M_bt /(1+f x) / (π² √y_s) | X 2.1, S 2.2, LT 1.8 |
| **shuffled control** | 2.97 | | |

The law itself scores 9.4 (X-COP), with UFD 3.5 and everything else near or inside its line on canonical Υ 0.5.

**Dropping one gate,** on the 1 % sample of pool members evaluated in full:
- Without X-COP the best form reads 0.97, so it passes everything else (canonical Υ 0.5). The law nearly does too, except UFD.
- Without dwarfs, 1.09-1.19: it misses by little.
- Without any other gate, about 1.9 to 2.5.

So the two places nothing in this grammar reconciles are **clusters under HSE and the ultra-faint dwarfs, against discs at the same time.** Real arms beat the shuffled control (2.1-2.35 against 2.97), so the leaves carry some signal; none of it reaches a line.

## Part 3, HF1's open reading as a map (`rs1_hf.out`)
X-COP on HF1's R4, σ × s (0.3-1) and fair share × r (0.2-1), m 5 and 11.8 eV, both footings. **No cell clears** |mean| ≤ 0.05, rms ≤ 0.10. Best rms 0.173-0.176 at s 0.85, r 0.6: mean near 0, but the radial tilt stays: +0.25 at x 0.1, −0.21 at x 0.7. Lowering σ further makes the outer excess worse. HF1's main open reading doesn't rescue clusters; its label doesn't move.

## Checks
- K1 T = 0: X-COP +0.4675, 0.4763; LT −0.0252; UFD Z +5.217, all as the record (pass).
- K2 inversion round trip below 1e-10.
- K3 planted M_b π x, with 0.01 dex noise: recovered within 21 pool members, as `M_b*(1.0*(x*pi))` and equivalents. The weak point: 340 forms passed there, so the gates don't single out a form; they only exclude.
- K4 shuffled: 0 hits, best 2.97.
- K5 Part 3 at s 1, r 1: +0.1585 and +0.1782 against HF1's +0.159, +0.178.
- MUTATE a0 × 2 fails K1, exit 1. Lines × 1e-6 on the planted mock: 0 hits.

## Departures and limits
- Groups and lensing use this lane's own estimators (Wolf 3σ²/r12; SIS 4GΔΣ, R ≤ 0.3 Mpc, gas share assumed 0.2), not CRG1's or BF3's paths. Groups at f 0.3 and 0.6 give the same M_x because only the split changes.
- Dwarfs and groups have no measured gas: leaves using y_g read 0 there, which forces forms with y_g/… to fail on dwarfs.
- Drop-one gate table is from a 1 % sample of pool members; the top-50 list is from all forms past the X-COP precut (|mean| ≤ 0.30, rms ≤ 0.35), so forms bad on X-COP and good elsewhere are seen only through the sample.
- Part 3 ran while the two search processes ran, so three processes for a few minutes, above the criteria's two.
- Cluster keys weren't run: no Stage 1 survivor.
- Grammar capped at level 2 and 6,000 members; deeper forms untried.

## Against the record
SL2's ratio, GS4 and LF1 on gas, NU1 on ordinary mass, MG1 on peaks and DW2 on processes stand. This adds: inverted row by row, the source the law needs is zero-centred in discs, ~4.4 M_b in X-COP and scattered over two decades in dwarfs; no single baryonic or system variable organises it; and BF1-BF3's near misses don't come from a missing source form at this depth.
