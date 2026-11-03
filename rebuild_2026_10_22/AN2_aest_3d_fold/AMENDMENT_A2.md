# AN2 AMENDMENT A2: corrected AN1 reference, force kernel, rows run for numbers. POST-RESULT, NOT BLIND

Committed alone, before any engine change, before any S1 row. Owner's instruction 2026-11-02: run the rows. Lines of section 8 unchanged. Not blind: AN1 v3 and S0 are read, and so is a 1D diagnostic of KZ (`diag_a2/kz1d.py`).

## 1. Reference column replaced
Section 7's t_ref came from a run with the centre-cell bug and is void. New t_ref, `../AN1_aest_nonlinear_dust/an1_v3_rows.jsonl`, N 1500, strict line (z, t Gyr). AN1 v3 is itself NO VERDICT (K11 missed), so this reference carries that caveat.
| Row | canonical | alt |
|---|---|---|
| 1e12, mu 56.6 | 1.158, 5.277 | 1.158, 5.277 |
| 1e12, mu 0.1 | 0.009, 13.709 | 0.009, 13.708 |
| 1e15, mu 56.6 | 1.342, 4.701 | 1.341, 4.702 |
| 1e15, mu 0.1 | 0.004, 13.783 | 0.005, 13.778 |

1e12 at mu 0.1 now has a fold time, so section 7's no-reference classes lapse: all 16 rows are compared. That fold and the mu 0.1 one at 1e15 are grid-limited at N 1500, and their z moves up to 50 % between settings, so their t moves under 0.1 %; the comparison is in t, as frozen. A row with z_ref < 0.05 can't read LATER by more than 1.05 t_ref unless it doesn't fold by z = 0, because 1.05 t_ref passes t0. Stated before the rows: **at mu 0.1 "NO LATER" is close to "folds at all before z = 0" and says little.**

## 2. What the diagnostic found
KZ reduced to 1D at the same background and step rule. Error in fold t, eta 0.05:
| Mesh force | N 64 | 128 | 256 | 1024 |
|---|---|---|---|---|
| CIC, spectral (frozen engine) | +2.60 % | -3.31 % | -4.95 % | -5.51 % |
| CIC, 2-point | +6.77 % | +0.12 % | -2.04 % | -2.87 % |
| TSC, spectral | +3.54 % | +0.64 % | -0.42 % | -0.95 % |
| TSC, 4-point | +4.20 % | +1.07 % | -0.07 % | -0.65 % |

It reproduces the 3D engine's +2.60 % and -3.31 %. **The error doesn't go to zero with N.** Neighbour spacing at the crest is dq (1 - D/D_c), independent of N, so particle spacing passes below a cell at a fixed time before crossing, at every N, and the force between neighbours is then set by the kernel. Likely reason, not proved. So:
- Section 4's statement, that softening biases the fold toward later, is **wrong for the frozen engine at N >= 96:** the CIC bias is earlier, and larger than I said. The earlier-fold direction is the one the expected label sits on.
- Tet-det fold times on a mesh with one particle per cell carry a kernel-dependent bias at any N. KZ's 5e-3 can't be met at 64^3 by these kernels.

## 3. Engine change
Deposit and force interpolation go to **TSC, gradient stays spectral**. It has the smallest bias near N 128 of the variants that keep L1's gradient, and it was picked on this diagnostic, so that choice is post-result. The hold solver stays, but KC reruns. It costs about 27/8 per deposit and interpolation.

## 4. Status of checks
KZ reruns at 64^3 and KE2 at 96^3, at their frozen lines. **I expect KZ to miss (about +3.5 %).** A miss stands: the lane stays NO VERDICT, numbers only, no label. KG's and KE's reads go on being reported, plus KZ at 128^3 as a read at the rows' own N. Lines aren't loosened.

## 5. Rows run regardless
Section 8 allows rows to be computed for numbers after a failed check, and README's stricter reading is lifted by the owner's instruction. Order otherwise as frozen: KC, KZ, KE2, KR, KM, KT, KB, KE, KG, rows. Section 13's limits stand, including 67.5 CPU min per row: a row over it is checkpointed and reported, not shrunk.

kappa = 1/2 FITTED. Footings never pooled. A gravitating field, never a particle. The cold sector stays retired: nothing here reinstates it. S2 and S3 don't run. No LCDM input. Not theory closed. Nothing here says the data favour the framework.
