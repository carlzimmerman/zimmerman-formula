# QX30 FROZEN CRITERIA: are the hot-system failures partly an artefact of the LCDM-based assumptions in the data?

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. No dark-matter particle. Both footings (canonical a0 = 9.3603e-11,
alt a0 = 1.1312e-10 m/s^2), never pooled. Frozen and committed alone, before any QX30 script exists and before any
re-derived number. Id check: no QX30 directory or commit on origin/main at freeze time (QX28 / QX29 / QX31 are parallel
lanes; their folders are not touched).

## Question (owner, 11-06)

The plain law under-predicts the hot systems at matched variable (QX20 table): X-COP +0.467 / +0.435 dex, Lovisari groups
+0.264 / +0.226 (f* = 0.5), Humphrey+2006 ellipticals +0.210 / +0.189 (Kroupa), Coma UDGs +1.12 / +1.08. Do the
LCDM-based or simulation-calibrated assumptions inside those data products cause part of the miss?

## Record already audited (not redone; carried into the ledger by reference)

- Non-thermal pressure on X-COP: <= 0.03 dex and of the wrong sign (QX2 README). CFG922: hydrostatic bias, clumping,
  radius convention, beta-shape CANNOT remove the eRASS1 core excess (three of wrong sign); ICL NOT TESTABLE there.
- IMF: QX18 (Salpeter -> ellipticals +0.071 / +0.053) and QX26 (Posacki sigma-dependent IMF: X-COP -0.019, groups
  -0.037, ellipticals -0.117 / -0.115).
- MB1: 30 % ICL moves the X-COP member-bound mean to +0.412 (a different model; reported only).
- CFG407: framework-native background in X43's r_ta changes Delta by +0.006-0.007 (model side, not the data's D_A).
- CFG885: KiDS ESDs rescaled to the native background: no class moves (lensing, not hot systems).
- Ellipticals: gas neglected, so the offsets are upper bounds (QX18).
New here: the data-side distance scaling (D_A, h) of every hot sample; the published mass-model columns of X-COP; the
X-COP stellar-mass conventions (Chabrier, no ICL, x0.75 deprojection); clumping and temperature-calibration bounds.

## Data (on disk only; no downloads)

- X-COP: real_research/data/xcop/<cl>/ (hydro_mass M_FORW, M_NFW, M_EIN, M_ISO, M_BUR; fgas MGAS; mstar), the 7
  clusters with stellar files, 35 points at 0.1-0.7 R500, exactly QX2's builder. No n_e(r) or T(r) profiles are on
  disk, so a fresh non-parametric hydrostatic solve is NOT EVALUABLE; M_FORW (Ettori+2019 Sect. 3.1, forward method, no
  assumed mass model) is the record's graded quantity and is the closest on-disk product to it.
- Groups: real_research/data/lovisari2015_groups.tsv via QX5's loader (read-only), f* = 0.5 primary, f* 0 / 1 bracket.
- Ellipticals: real_research/data/humphrey2006_ellipticals.tsv via QX5's (QX16-fixed) loader, Kroupa.
- Coma UDGs: rebuild_2026_10_22/S1_v3_hosted_small/s1_coma_per_galaxy.csv (offsets as QX20 reads them).

## Framework-native background (the only admissible D_A)

Flat, constant rho_DE (flat a0 under the tracking law), as the record defines it (CFG885; QX15):
- Omega_m,nat = 0.3085 (CFG682, BAO + SN, no CMB).
- h_nat = 0.674 on both footings (PRIMARY): QX15 "h is fixed by a0 (0.674)"; the alt footing's a0 = kappa c
  sqrt(G rho_crit) returns h = 0.6740 directly.
- Reported only (never graded): h = sqrt(Omega_DE h^2 / (1 - Omega_m,nat)) from the canonical rho_DE (about 0.671),
  and CFG885's h = 0.70 / 0.73 bracket, because the framework's H0 status is disputed in the record.
- Fiducial backgrounds being replaced: X-COP (H0 70, Omega_m 0.3; Ettori+2019 Sect. 1), Lovisari (H0 70,
  Omega_m 0.27; L15 Sect. 1). Ellipticals: SBF distances (Tonry+2001, no cosmology), except NGC 6482 (LEDA kinematic
  distance, Hubble flow, taken as h70). Coma: d = 100 Mpc class distance at h70 (S1 inputs).
- Ratio f = D_A,nat(z) / D_A,fid(z) per object (numerical comoving integral, radiation neglected).

## Scaling rules (fixed now; at fixed angle and fixed z)

- radius r -> f r.
- hot-gas mass (from emission measure) -> f^(5/2) M_gas.
- stellar mass (from luminosity, D_L = (1+z)^2 D_A) -> f^2 M_*.
- hydrostatic mass M = -r^2 dP/dr / (G mu m_p n_e): with an X-ray spectroscopic T, M -> f M (beta = 1, PRIMARY: inside
  0.7 R500 X-COP's T is XMM spectroscopy, resolved to about 0.9 R500, Ettori+2019 Sect. 2); with an SZ pressure
  (P ~ 1/D_A), M -> f^(1/2) M (beta = 1/2, reported bracket end).
- UDGs (not re-solved): M_dyn ~ sigma^2 R_e -> f; the predicted mass moves by f^p with p in [2, 3] (p = 2 for an
  EFE-dominated, quasi-Newtonian prediction, 3 when the host field ~ 1/D also enters nu); reported as a bracket.

## Admissible corrections (enter the graded "corrected" number)

A correction is admissible only if (i) it is documented in the source paper or computable from the published profiles on
disk, (ii) framework-native (no LCDM parameter, no simulation calibration), (iii) has no free knob. Frozen list:
- C1 (admissible): framework-native D_A with h_nat 0.674, Omega_m,nat 0.3085, beta = 1.
Every other item is classified in ASSUMPTION_LEDGER.md as one of:
- BOUND (documented, no framework-native value; enters only the "all-favourable bound" row): clumping (gas mean instead
  of azimuthal median, sqrt(C) <= 1.1 inside R500, PROVISIONAL); stars without the x0.75 deprojection (x 1/0.75); ICL at
  40 % of total stellar light (x 1/0.6, PROVISIONAL literature upper end); Salpeter instead of Chabrier/Kroupa (x 1.8);
  beta = 1/2; the most favourable published X-COP mass-model column; h = 0.671 (largest native D_A).
- INADMISSIBLE (LCDM / simulation calibrated, or no ground truth): Eckert+2019 non-thermal fraction (uses a universal
  Omega_b/Omega_m), simulation HSE bias (1-b), XMM vs Chandra T calibration, NFW mass-model priors (reported as columns
  only; the graded M_FORW has none).
Each ledger row states the direction of its effect on Delta (+ = model short).

## Grader and lines (read-only reuse)

- X-COP: QX2's builder and gate (qx2.py source executed up to its output block): Delta = log10(M_HSE/M_law), mean and
  rms over 35 points; line |mean| <= 0.05 and rms <= 0.10 (HO1 line, as QX2 / QX12).
- Groups: QX5's loader; class mean over 40 points at f* = 0.5; line as QX5 (f* in [0, 1] bracket must straddle +-0.05).
- Ellipticals: QX5's loader, 2/4/8 Re, Kroupa; line G7 |D| <= 0.15 (QX18).
- UDGs: mean of QX20's UDG offset; shift bracket reported, no line moved.

## Known answers (must pass before any corrected number is read)

- KA1: with f = 1 the X-COP numbers equal QX2 iter 1 (+0.468 / +0.435) to <= 1e-9.
- KA2: with f = 1 groups and ellipticals equal QX20's class means (G, E) to <= 1e-6.
- KA3: comoving distance matches the analytic Einstein-de Sitter form (Omega_m = 1) to <= 1e-6 and astropy (if
  installed) to <= 1e-6 relative.

## Label rule (X-COP; per footing, never pooled)

- ARTEFACT: the admissible corrections (C1) bring X-COP inside the line.
- PARTIAL: they move the mean by >= 0.1 dex but not inside.
- ROBUST: they move it by < 0.1 dex.
The same three words are reported (not as the lane label) for groups and ellipticals against their own lines. The
all-favourable bound row is reported with its own reading ("even with every bound at its favourable end ...") and does
not set the label.

## MUTATE (separate outputs qx30_MUTATE.*), all must bite

- M1 opposite sign: apply C1 with f -> 1/f. The shift must equal minus C1's shift to within 15 % (the scaling is
  near-linear in log f).
- M2 swap back: native background replaced by each source's own fiducial (h 0.70; Omega_m 0.3 / 0.27). Must reproduce the
  original offsets to <= 1e-9 (X-COP) / 1e-6 (groups, ellipticals).
- M3 power plant: h = 0.35 (f about 2). Must move the X-COP mean by >= 0.1 dex, so the pipeline can see an artefact
  when one is planted.

## Limits stated in advance

Statics; published products only; no n_e(r), T(r) on disk (fresh solve NOT EVALUABLE); Bullet not in the QX20 ladder
and not graded here; Humphrey's non-NFW fits not on disk (NOT EVALUABLE beyond the ledger); one thread, < 1 GB.
