# TP01-SC: paired contraction weakens spin ranking; the conditional SPARC repair fails normalization

The nine existing LC1 pairs do not establish an additional predictive spin response. Initial core strength predicts final core strength out of sample within these nine seeds; adding spin worsens that prediction. Under a deliberately idealized perfect inverse-spin association with galaxy brightness, the measured joint scatter and response can flatten SPARC's brightness residual, but drive the median stellar mass-to-light ratio to 0.40 on both backgrounds, below the frozen 0.50 floor. This is a failed conditional repair, not an exclusion of arbitrary baryonic dynamics or all possible spin maps.

Checkpoint base `0fe706856e8a897a9ab350be4931dbf36416ada4`. The actual shared tree was dirty/active. [FROZEN_CONTRACT.md](FROZEN_CONTRACT.md) and [CAPACITY_CONTRACT.md](CAPACITY_CONTRACT.md) precede their respective runs. No old inputs were modified, no production simulation or download was run, and nothing was staged or committed. κ remains fitted. No claim of theory closure or empirical preference follows.

## What was measured directly

[measure_pairs.py](measure_pairs.py) independently reduces seed 1–9 pre-disc X48 snapshots and the matching LC1/ZN1 z=0 pairs. N, particle mass, seed, grid, softening, initial metadata and disc-axis alignment agree. It reconstructs every stored LC1 f_Q and R_live, and every matching HS1 spin/concentration, exactly at float64 precision. The actual same-epoch identity is S_disc(z=0) = R_live(z=0) S_no_disc(z=0); a z_f S was not multiplied by a z=0 response.

Median initial Bullock spin is 0.011688, pre-disc NFW-fit concentration 7.75, f_Q 0.871707 and R_live 2.154310. S is X77's smooth-core fit to a cumulative profile, not evidence that collapse produced a physical smooth core. Raw S units are solar masses per Mpc squared. Across seeds, log10 S scatter is 0.1371 dex before the disc, 0.09934 in the no-disc z=0 branch and 0.07813 in the disc z=0 branch. Thus contraction narrows, rather than amplifies, the available core-strength scatter in this finite ensemble.

Exact two-sided permutation tests enumerate all 362,880 permutations for each predeclared association. Holm adjustment covers these six diagnostics only; p-values describe the exchangeable finite-seed null, not uncertainty in a cosmological galaxy population.

| Association | Spearman rho | Exact p | Holm p | Leave-one-seed-out rho range |
|---|---:|---:|---:|---:|
| f_Q, initial spin | -0.200 | 0.6134 | 1.000 | -0.476 to -0.048 |
| f_Q, initial concentration | +0.767 | 0.02139 | 0.1283 | +0.667 to +0.810 |
| Initial S, initial spin | -0.500 | 0.1777 | 0.8883 | -0.738 to -0.286 |
| No-disc z=0 S, initial spin | -0.450 | 0.2298 | 0.9193 | -0.643 to -0.262 |
| Disc z=0 S, initial spin | -0.283 | 0.4630 | 1.000 | -0.524 to +0.024 |
| f_Q, no-disc z=0 S | -0.183 | 0.6436 | 1.000 | -0.381 to +0.167 |

Contraction therefore weakens the measured S–spin rank relation. A strong-looking concentration association is not a new response law: it has nine points, corrected p=0.128, and modest held-out prediction skill.

Prediction skill is 1 minus leave-one-out squared error divided by leave-one-out intercept-only squared error, with a separate intercept fitted on the eight training seeds. Negative skill loses to that baseline.

| Predicted quantity | Predictors | Held-out skill | Held-out RMSE |
|---|---|---:|---:|
| log10 final S | log10 initial S | 0.8414 | 0.03300 dex |
| log10 final S | log10 initial spin | -0.0520 | 0.08499 dex |
| log10 final S | log10 initial concentration | 0.5886 | 0.05315 dex |
| log10 final S | log10 initial S and spin | 0.7827 | 0.03863 dex |
| log10 final S | log10 initial S and concentration | 0.7382 | 0.04240 dex |
| f_Q | log10 initial spin | -0.1291 | 0.16644 |
| f_Q | log10 initial concentration | 0.1021 | 0.14842 |
| f_Q | log10 initial spin and concentration | -0.1852 | 0.17052 |

These calculations measure predictive associations among existing seeds. They do not fit a galaxy-to-halo spin map.

## Conditional forward continuation on the current NR2 baseline

[forward_capacity.py](forward_capacity.py) reads the fixed NR1 cache directly and rebases the low-mass eta interpolation to completed NR2 medians. The original NR1 Upsilon is reproduced exactly, rms to 1.4e-17. NR2 Upsilon is reproduced exactly, rms to 4.81e-7. NR2 still has its reported seed uncertainty; this continuation uses its medians only.

This transfers **relative smooth-core-fit scatter and f_Q from the actual LC1 pairs onto N's smooth-core halo prescription**, with N's mass mapping. It is not OP3's native cumulative-profile calculation. Applying a one-mass, one-disc response to all galaxy masses/profile shapes is an explicit extra homology assumption. The spherical shell equation is solved at each final radius:

    r_i M_0(r_i)(1+F) = r_f [M_b(r_f) + M_0(r_i)].

The direct solver was compared to the legacy shell interpolation on three preselected galaxies at Upsilon 0.50; the maximum relative mass difference from 1,200 shells was 0.267%, within the frozen 0.5% line. No compact-root saturation occurred. This validates the limited numerical realization, not spherical contraction as a galaxy model.

All nine actual (S_no_disc/median S_no_disc, f_Q) pairs are preserved. The ensemble-mean force makes no brightness association. The perfect inverse-spin scenario assigns low-spin seed pairs to brighter galaxy quantile bins; this is stipulated and deliberately idealized, not observed galaxy spins or an optimized upper bound over every association. The same assignments are used on both backgrounds. No scatter amplitude, response strength or rank coefficient was fitted.

| Conditional N prescription | Median Upsilon A / B | rms A / B | Brightness slope b, A | Original Upsilon line |
|---|---|---|---|---|
| NR2, no response/scatter | 0.75 / 0.76 | 0.06902 / 0.07010 | -0.1720 ± 0.0623 | Pass; tilted |
| Median measured response, no scatter | 0.39 / 0.39 | 0.06476 / 0.06555 | -0.0742 ± 0.0651 | **Fail low** |
| Paired ensemble-mean force | 0.39 / 0.40 | 0.06411 / 0.06485 | -0.0737 ± 0.0647 | **Fail low** |
| Paired perfect inverse-spin association | 0.40 / 0.40 | 0.06891 / 0.06985 | -0.0011 ± 0.0634 | **Fail low** |
| Same ranked scatter, response off | 0.77 / 0.78 | 0.06960 / 0.07085 | -0.0888 ± 0.0588 | Conditional pass |
| Same ranks, f_Q cyclically permuted | 0.40 / 0.40 | 0.06796 / 0.06890 | +0.0034 ± 0.0623 | **Fail low** |

All brightness statistics use HS1's original 47-galaxy selection and fixed Upsilon=0.50 at 2 Rd. The baseline slope differs from historical HS1 because this is NR2's revised N halo, not HS1's older eta table. All rms values above are the original 175-curve weighted acceleration statistic; brightness slopes use velocity residuals. They are distinct diagnostics. The existing fit masks are retained and residuals use max(g,1e-300). No nonpositive model acceleration occurred inside any fit mask in either background or any model; per-galaxy counts are recorded. HS1's sqrt(max(g R,0)) safeguard applies to some ungraded cells.

The useful distinction is now explicit: artificial ranking without contraction can pass these chosen aggregate gates, but restoring the measured gravity-only response breaks normalization. Flattening the slope alone is insufficient. Preserving the measured covariance does not remove that conflict in these scenarios. A cyclic permutation changes the brightness mean by 0.00516, confirming the paired information is being used, while retaining the normalization failure. Neither the inverse-spin assignment nor its cyclic control is a physical model selection exercise.

## Evidence, failures and review status

- [run_002/results.json](run_002/results.json), [manifest](run_002/manifest.json): primary direct measurements, exact permutation tests and predictions. Completed; manifest validation passed. About 15 s and 117 MB maximum RSS.
- [run_004/results.json](run_004/results.json), [manifest](run_004/manifest.json): NR2-rebased conditional forward scenarios. Completed; manifest validation passed. 10.6 s and 113 MB maximum RSS.
- [per_seed.csv](per_seed.csv), [per_galaxy.csv](per_galaxy.csv): readable projections of the hashed JSON evidence. Complete per-radius Q/QB and all model/bin summaries remain in JSON.
- Run 001 failed the rigid-motion control because a discrete virial-boundary particle changed aperture membership under rounding; [A1](AMENDMENT_A1.md) retains the failure and repairs the invariant using identical particle identities. The repaired invariant has relative error 2.1e-15. The archived [original source](measure_pairs_run001.py) matches run 001's recorded SHA exactly.
- Run 003 finished its calculations but failed NumPy-bool JSON serialization; [A2](AMENDMENT_A2.md) documents the repair. Its [original source](forward_capacity_run003.py), manifest and logs remain. No scientific result JSON was produced for that run.
- Input hashes before/after are unchanged for the successful runs. Validation records execution/provenance, not a physical theorem. Critical calculations are self-reviewed; fresh cross-review is coordinated separately.

## Remaining implication and continuation

The route remains open as a physical question, but these nine isolated, low-spin, same-mass spheres with artificial steady discs do not supply the missing galaxy spin/size retention law. Concentration's modest f_Q prediction gain is a lead for an independently specified response calculation; adding spin to it failed held-out prediction here. Initial S already carries most of the predictive information for final fitted S. Testing a different mass, cosmological torques, baryonic assembly history or actual dissipation would require new physical inputs/runs outside this checkpoint. No independent response suppression or scatter strength has been introduced to obtain a pass.
