# QX23 iter_1 frozen criteria: is the law's hot/cold step keyed on cold gas (A), or a baryon gap (B)?

Frozen before any script exists. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Footings never pooled:
canonical a0 = 9.3603e-11, alt a0 = 1.1312e-10 m/s^2.

## Context (from the record, not new numbers)
- QX20: plain-law offset step. Hot systems sit +0.32-0.37 dex above SPARC at equal M_b, g_N, depth, r/r_M and f_gas (f_gas
  counted hot gas).
- QX21: KiDS early-type lenses sit +0.158 +- 0.064 above late types.
- QX22: the step is not keyed on kinematic support. Post-data reading: LG gas-poor dwarfs +0.13, gas-rich -0.03 (types
  provisional).
- SPARC is gas-rich by selection.

Readings:
- (A) The missing boost is keyed on cold-gas content.
- (B) Gas-poor systems carry uncounted baryons.

## Data (all on disk; nothing downloaded)
- SPARC: real_research/data/SPARC_Lelli2016c.mrt (MHI, L36) and sparc_data/*_rotmod.dat. QX5's loader is used read-only:
  Q <= 2, Inc >= 30, eV/V <= 0.1, disk Upsilon 0.5, bulge 0.7. This is QX20's SPARC anchor sample.
- LG dwarfs:
  - plain-law offsets per system from rebuild_2026_10_22/LW1_law_scorecard/lw1_dwarfs.json (per_system.plain; stars-only
    baryons, as LW1 froze them);
  - HI masses from real_research/data/dsph/mcconnachie2012_dsph.csv (M.HI, 1e6 Msun) and lvd_dwarf_*.csv (mass_HI,
    mass_stellar), matched by name.
- MaNGA: HI-MaNGA is NOT on disk. T3 is NOT RUN; a download request goes to NEEDS_OWNER.md.

## Tests
**T1 (graded) SPARC, cold-gas fraction at fixed g_bar.**
- Galaxy f_HI = 1.33 M_HI / (1.33 M_HI + 0.5 L36).
- Points are binned in log10(g_bar/a0), bin width 0.5 dex.
- In each bin, take each galaxy's mean plain-law residual. D1 is the bin-count-weighted mean, over bins holding at least 3
  galaxies of each kind, of mean(f_HI < 0.10) minus mean(f_HI > 0.30). Units are dex.
- sigma_D1^2 = stat^2 + Upsilon^2:
  - stat: bootstrap over galaxies, 2000 draws, seed 20261108;
  - Upsilon: the larger |D1 shift| when the disk Upsilon is 0.4 or 0.6 (bulge 1.4 x disk).
- Predictions under A use S = QX20's step for the footing (V4_gN step: +0.35 canonical, +0.35 alt; read from qx20.json):
  - M-step: boost S for f_HI < 0.10, else 0. D1_pred = S.
  - M-lin: boost S (1 - f_HI/0.30) for f_HI < 0.30, else 0. D1_pred is computed on the actual sample.
- T1 labels:
  - **A KILLED in SPARC's range** if D1 < D1_pred - 3 sigma for both mappings, on both footings.
  - **A SUPPORTED** if D1 > 3 sigma and |D1 - D1_pred| <= 2 sigma for at least one mapping, on both footings.
  - Otherwise **NO VERDICT**.
- A kill covers only the f_HI range SPARC samples. A threshold below SPARC's gas-poorest galaxies is not excluded by T1.
- Also reported, not graded: the partial Spearman of galaxy residual (bin mean removed) against log f_HI.

**T2 (graded) LG dwarfs with measured HI.**
- Classes:
  - gas-poor: M_HI/M* < 0.1, or no HI listed in either catalogue;
  - gas-rich: M_HI/M* > 1.
- D2 = median(plain, gas-poor) - median(plain, gas-rich), on LW1's "LG field" class (primary). Satellites are confounded by
  host fields and stripping, so they are reported only.
- sigma_D2 by bootstrap, 5000 draws. The stars-only baryons are LW1's frozen choice. Also reported: a bracket with all HI
  counted inside the half-light sphere, which can only raise D2.
- Labels:
  - A SUPPORTED-DW: D2 > 3 sigma;
  - A DISFAVOURED-DW: D2 < 2 sigma and D2 < S - 3 sigma;
  - otherwise NO VERDICT.
- Systems that match in neither catalogue are listed and dropped.

**T3** MaNGA HI-detected against gas-poor: NOT RUN (data not on disk).

**T4 (graded by argument and numbers) reading B, the uncounted-baryon factor.**
- For each class (ellipticals, groups, X-COP, bright M31 dSphs, MW classical dSphs, LG gas-poor field dwarfs), compute the
  factor k by which counted baryons must be multiplied to null the class's mean offset Delta at its median y = g_N/a0:
  glaw(k gN) = 10^Delta glaw(gN). For dwarfs, use deep-MOND k = 10^(2 Delta) when y is not available.
- B is ALLOWED for a class when k - 1 is at most an on-record or stated observational ceiling on uncounted baryons in that
  class. Ceilings are fixed here:
  - ellipticals: hot gas inside 8 Re <= 0.2 M* (generous; X-ray gas fractions of massive ellipticals are of order 1-10 %
    inside a few Re);
  - groups and X-COP: hot gas already counted, uncounted <= 0.3 of M_b;
  - dSphs and gas-poor dwarfs: <= 0.1 M* (no hot gas; HI and X-ray non-detections).
- B is EXCLUDED for a class if k - 1 > 2 x ceiling. Otherwise it is MARGINAL.
- The ceilings are stated literature-level bounds, not graded data.

## Overall label
- **COLD-GAS KEY SUPPORTED:** T1 A SUPPORTED, or T2 A SUPPORTED-DW with T1 not A KILLED.
- **BARYON-GAP SUPPORTED:** B ALLOWED for every class in T4.
- **NEITHER:** T1 A KILLED (in SPARC's range) and B EXCLUDED for at least one class, including a dwarf class.
- Otherwise **NO VERDICT**.

## Controls (separate outputs, qx23_MUTATE.*)
- **M1 shuffle:** f_HI shuffled across galaxies (seed 7). |D1| <= 2 sigma required on both footings, or T1 has a built-in
  bias.
- **M2 power:** +0.20 dex planted into the f_HI < 0.10 galaxies' residuals. D1 must rise by 0.20 +- 0.05. Otherwise T1 has
  no power and no T1 label stands.
- **M3 Newton:** reported as a baseline (the SPARC anchor must move by > 0.2 dex).

## Known answers
- KA1: the SPARC mean residual of the loaded sample reproduces QX20's sparc_mean to 1e-6 on each footing.
- KA2: the LW1 LG-field gas-poor and gas-rich medians reproduce QX22's T4 numbers (+0.134 / -0.027 canonical) to 1e-6, when
  QX22's provisional lists are used.

Kappa = 1/2 FITTED; not theory closed.
