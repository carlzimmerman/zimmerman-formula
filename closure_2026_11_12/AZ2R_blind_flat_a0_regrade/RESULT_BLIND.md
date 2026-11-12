# AZ2R RESULT (BLIND, before opening AZ2's RESULT.md, script or outputs)

## Label (headline cell T2 = BAO + Pantheon+ shape, Om 0.30)

- **Canonical (a0 9.3603e-11): FLAT HOLDS / EXPANSION-MODEL DEPENDENT.**
- **Alt (a0 1.1312e-10): FLAT HOLDS / EXPANSION-MODEL DEPENDENT.**

Headline numbers: a0(2.33)/a0(0) = sqrt X(2.33) = 1.320 (canonical) / 1.322 (alt), X5 = 1.742 / 1.747; D_band 1.76 / 1.79
(minimum at the band edge X5 = 1.21); D_rival 361.8 / 361.3. Absolute a0(2.33) at the best fit: 1.236e-10 / 1.495e-10 m/s^2.
The flag is set because T2 at Om 0.25 and Om 0.35 are both FLAT FAILS (D_band 71 and 15). A FLAT HOLDS is not a pass for the
theory: constant dark energy (LCDM) gives the same sqrt X = 1; nothing here separates the framework from LCDM, and this is not a
kinematic a0 measurement at z 2.33.

## Per cell (Delta chi^2 from the lowest chi^2 found at that Om; canonical / alt)

| cell | h | sqrt X(2.33) best | D_band | D_rival (X5 rival) | label | X5 95 % (coarse grid) |
|---|---|---|---|---|---|---|
| T1 Om 0.25 | 0.644 / 0.778 | 1.965 / 1.966 | 3.21 / 3.22 | 7.1 / 7.1 (9.99) | FLAT HOLDS | [1.0, 4.36] / [1.25, 4.37] |
| T1 Om 0.30 | 0.667 / 0.806 | 1.195 / 1.197 | 0.01 / 0.01 | 13.6 / 13.6 (11.79) | FLAT HOLDS | [<= -1, >= 4] |
| T1 Om 0.35 | 0.692 / 0.836 | 0 (X5 -1.38) | 1.00 / 0.99 | 19.8 / 19.7 (13.58) | FLAT HOLDS | [-1.88, 3.25] |
| T2 Om 0.25 | as T1 | 2.026 / 2.028 | 71.3 / 71.6 | 169 / 169 | FLAT FAILS | [3.5, 4.61] |
| **T2 Om 0.30** | as T1 | **1.320 / 1.322** | **1.76 / 1.79** | **361.8 / 361.3** | **FLAT HOLDS** | [1.0, 2.5] |
| T2 Om 0.35 | as T1 | 0 (X5 -0.99) | 15.2 / 15.1 | 569 / 569 | FLAT FAILS | [-1.49, -0.25] |
| T1 Om free (reported only) | Or at Om 0.30's h | 0 (Om 0.45 ceiling, X5 -8.5) | 0.11 / 0.11 | 4.6 / 4.6 | no label | - |
| T2 Om free (reported only) | same | 1.918 (Om 0.260) | 0.04 / 0.04 | 97.8 / 97.5 | no label | - |

Every cell has the same label in both footings; the footing moves sqrt X(2.33) by <= 0.002 (<= 0.2 %). At T2 Om 0.35 the
whole 95 % interval has X5 < 0 (negative dark energy density at z 2.33): FLAT FAILS there means the fit wants rho_DE(2.33) < 0.
The rival (a0 proportional to H(z)) is excluded in every fixed-Om cell (D_rival >= 7.1); the T reading (sqrt X ~ 0.2) is not graded.

## Validation (all pass; grading proceeds)

- V1 = KA1 (CFG681's original Lya pair, h 0.68): T1 Delta chi^2 7.408 (target 7.41 +- 0.10), T2 12.080 (12.08), T3 AP chi^2 5.976
  (5.98 +- 0.05); fixed-Om sqrt X(2.33) T1 1.929 / 1.140 / 0 (1.93 / 1.14 / 0.00), T2 1.974 / 1.235 / 0 (1.97 / 1.24 / 0.00). PASS.
- V2 = KA2 flat injection (Om 0.30, own X = 1 model, new-pair errors): D_band 1e-13, best sqrt X(2.33) 1.000, both footings. PASS.
- V3 = KA3: |profile min - free fit| <= 6e-9 in every cell, both footings, mutated runs too (the profile is continuous: Brent
  inside the band plus the free fit's own X5 on the grid, so the coarse-grid gap AZ2's amendments describe does not arise). PASS.
- Mutation (new D_H/r_d 8.600 -> 8.270, -5 sigma): T2 Om 0.30 sqrt X 1.320 -> 1.789 (+0.47; alt 1.322 -> 1.790), D_band
  1.76 -> 22.15 (+20.4; alt 1.79 -> 22.27); mutated headline FLAT FAILS / EXPANSION-MODEL DEPENDENT both footings. BITES.

## Scripts and outputs (this folder)

`azr.py` (own code; modes KA1, canonical, alt, canonical_MUTATE, alt_MUTATE); outputs `azr_<mode>.json/.out`. Deterministic:
fixed starts (six 5-node starts, three Om starts), Nelder-Mead -> Powell -> Nelder-Mead, profile warm starts in a fixed order,
OMP/OPENBLAS/MKL/VECLIB threads = 1, `nice -n 19`. Run with `-W ignore::RuntimeWarning` (macOS Accelerate emits spurious matmul
warnings; chi^2 values checked finite and equal to CFG681's X = 1 values 10.67 / 1400.39 / 1456.84 / 47.38).

## Shared with AZ2 (not independent)

The data: DESI DR2 BAO table as typed in CFG681's script, Pantheon+ STAT+SYS files and cuts, CFG681's model definition and
SN distance convention; the new Lya pair 39.32 +- 0.33 / 8.600 +- 0.066, r +0.225 (arXiv 2607.27410 Eq. 26, PROVISIONAL, read
2026-11-12 from https://arxiv.org/html/2607.27410v3); the frozen criteria and labels. Independent: the fit code and optimizer.
Blindness caveat (READING.md): AZ2's amendment files, which I was allowed to read, already quoted AZ2's headline numbers.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
