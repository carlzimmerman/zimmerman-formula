# GAS1: how lambda_P enters the record's forest code, against each paper's definition

Date: 2026-11-14. Read from the code; nothing was run.

## Verdict first

- Both builds use the same kernel: the density contrast in Fourier space is multiplied by exp(-k^2 lambda^2 / 2). In real
  space that is a Gaussian of standard deviation lambda. The density power is cut by exp(-k^2 lambda^2).
- lambda is comoving, in Mpc/h: 79 comoving kpc is coded as 0.079 x 0.6736 Mpc/h. The "100 proper kpc" bracket is
  coded as 0.100 (1+z) x 0.6736 Mpc/h. Both conversions are right.
- The two builds do not differ from each other in this convention.
- Rorai et al. 2017 (the measured lambda_P, Table S2) use exactly this kernel: a Gaussian of width sigma = lambda_P on
  the smoothed dark-matter density, W(k) = exp(-k^2 lambda_P^2 / 2). Conversion factor 1. No sqrt(2).
- Kulkarni et al. 2015 and Walther et al. 2019 define lambda_P from a fit to the power spectrum of the real-space flux,
  Delta_F^2(k) = A k^n exp(-k^2 lambda^2). The functional form of the cut matches the code's density power cut, but the
  field is the flux, not the density. Two readings of the conversion follow; they differ by a factor 2:
  - Reading 1 (factor 1): Rorai et al. 2017 Section 9.3 compare their density-kernel lambda_P with lambda_P,sim from
    this flux fit in hydrodynamical runs and find "an almost one-to-one relation with a scatter of less than 5%".
  - Reading 2 (factor 1/2): Kulkarni et al. 2015, Figure 14 caption, divide the flux-fit scale by 2 sqrt(2) "for
    consistency" with the linear filtering scale lambda_F, which they define on density contrasts as
    delta_b / delta_m = exp(-k^2 lambda_F^2) (their Eq. 9). The code's lambda is sqrt(2) lambda_F in that convention, so
    the code-equivalent of a flux-fit value would be lambda_ps / 2. On this reading the record's 79 comoving kpc
    (Kulkarni's flux-fit value) corresponds to about 39.5 comoving kpc in the code's convention.
  Reading 1 rests on a computed calibration in the measurement paper; Reading 2 rests on a one-line scaling in a caption
  that is stated without derivation and compares against linear theory. READING.md uses Reading 1 as primary and gives
  Reading 2 beside it.

## Where it is in the code

| build | file | line(s) | what it says |
|---|---|---|---|
| FRZ3R core (imported read-only by FWN1 and FRZ4) | `closure_2026_11_12/FRZ3R_blind_flux_forest_regrade/frz3r_core.py` | `def gas(grid, fk, lam)` | `fk * np.exp(-0.5 * (grid.k * lam) ** 2)`, then inverse FFT, plus 1 |
| FWN1 | `closure_2026_11_13/FWN1_forest_flux_split_f_ceiling/fwn1_run.py` | `LAM0`, `lam_rec`, `ckpc`, `MR_SPECS` | `LAM0 = 0.079 * 0.6736`; `lam_rec(z) = 0.100 * (1 + z) * 0.6736`; measured-range specs 91.4, 113.8, 138.6 comoving kpc; gas from `C.gas` (FRZ3R core) |
| FRZ4 | `closure_2026_11_13/FRZ4_forest_flux_graded/frz4_run.py` | `lam_rec`, `flux_job` | same `lam_rec`; gas from `C.gas` (FRZ3R core) |
| FWN1R (blind build) | `closure_2026_11_14/FWN1R_blind_split_f_ceiling/fwn1r_lib.py` | `def gas(box, fk, lam)`, `LAM0`, `lam_kpc` | own code, same form `np.exp(-0.5 * (box.k * lam) ** 2)`; `LAM0 = 0.079 * 0.6736` |

Grid units are comoving Mpc/h in both builds: `dv_cell` in the FRZ3R core is 100 E(z)/(1+z) times the cell size in km/s,
which holds for a cell size in comoving Mpc/h.

## Other gas parameters in the same code (for the reading)

- gamma enters twice: the optical-depth slope beta = 2 - 0.7 (gamma - 1) (`beta_of`) and the thermal-broadening width
  through T(rho) = T0 rho^(gamma-1).
- T0 enters only through the thermal-broadening width b = 12.85 sqrt(T0 / 1e4 K) km/s (`tau_field`, default
  `T0=1.0e4`). The optical-depth amplitude is retuned to the mean flux each time, so T0's effect on the amplitude is
  absorbed.
- tau_eff enters only as the target mean flux exp(-s tau_eff(z)), s = 0.9, 1.0, 1.1, with tau_eff(z) =
  0.751 ((1+z)/4.5)^2.90 - 0.132. This is Becker et al. 2013 Eq. 5 with their offset C = -0.132 and z0 = 3.5 included
  (SOURCES.md).
- The smoothing is applied to the whole painted density field (halo part and smooth part together), not to a separate
  gas field.

## What this file does not cover

It does not test whether a Gaussian cut on the density reproduces a hydrodynamical gas field; it only compares
definitions as written. FWN2's RESULT.md reports that FWN1R stated lambda_P x 0.5 is below one grid cell of its box.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
