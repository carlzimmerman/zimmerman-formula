# SNe -> rho_DE  vs  framework galaxy-side prediction -- SETUP

**Goal.** Extract the dark-energy *density* rho_DE from Type Ia supernovae (the
standard LCDM extraction) and test it against the framework's **galaxy-side**
prediction rho_DE = 4 a0^2 / (G c^2). Sarkar attacks the SNe leg; an *independent*
galaxy-side rho_DE that agrees would be a cross-corroboration, a discrepancy a
tension in the framework's canonical footing.

## The honest physics (not blurred)

The framework does **not** modify the cosmological background. a0 = cH_Lambda/Z =
c^2 sqrt(Lambda/32pi) modifies galaxy **inertia**, not expansion; Lambda is a
genuine constant, so H(z) and mu(z) are **standard LCDM**. There is **no**
framework-native SNe formula (banked: MI linear cosmology is dead / LCDM-degenerate).
So "rho_DE from SNe" *is* the standard extraction; the framework contributes only
the galaxy-side cross-check.

## (1) SNe-side extraction (standard)

- Pantheon+ (Brout+2022), SNe-only flat-LCDM: **Omega_m = 0.334 +/- 0.018** =>
  **Omega_Lambda = 0.666 +/- 0.018**. (q0 = Om/2 - OL = -0.499, accelerating.)
- SNe constrain the **shape** (Omega_Lambda via q0). The **absolute** density
  rho_DE = Omega_Lambda * 3 H0^2/(8 pi G) needs **H0** (SNe alone are M_B-H0
  degenerate). Carry H0 explicitly:

| H0 (km/s/Mpc) | rho_crit (kg/m^3) | rho_DE(SNe) (kg/m^3) |
|---|---|---|
| 67.4 (Planck) | 8.533e-27 | **5.683e-27 +/- 1.5e-28** |
| 73.0 (SH0ES)  | 1.001e-26 | **6.666e-27 +/- 1.8e-28** |

The H0 lever alone moves rho_DE by (73.0/67.4)^2 = **1.17x**. The +/- is from
Omega_Lambda only; the H0 choice is a **separate axis** (shape-vs-absolute).

## (2) Galaxy-side prediction  rho_DE = 4 a0^2 / (G c^2)

From Lambda = 32pi a0^2/c^4, rho_Lambda = Lambda c^2/(8 pi G) = 4 a0^2/(G c^2).

| a0 footing | a0 (m/s^2) | rho_DE (kg/m^3) |
|---|---|---|
| canonical (cH_Lambda/Z) **[CIRCULAR]** | 9.355e-11 | 5.836e-27 |
| alt (rho_total/cH0) | 1.131e-10 | 8.523e-27 |
| **measured GLS gas-dom** (Lambda-blind) | 1.181e-10 +/- 1.90e-11 (16%) | **9.308e-27 +/- 3.0e-27** |
| measured median variant | 9.726e-11 | 6.307e-27 |

Measured a0 reused from the banked a0-line
(`prep_2026/a0_line/fire_slope_results.json`, `budget_gas`). rho ~ a0^2 =>
sigma_ln(rho) = 2 sigma_ln(a0) = 0.322.

## (3) Cross-check + the circularity (the crux)

ratio = rho_DE(galaxy) / rho_DE(SNe); t = ln(ratio)/sigma_ln(combined).

| a0 footing | vs 67.4 | vs 73.0 |
|---|---|---|
| canonical | 1.03x (circular) | 0.88x (circular) |
| alt | 1.50x | 1.28x |
| **measured GLS** | **1.64x (+1.53 sigma)** | **1.40x (+1.03 sigma)** |
| measured median | 1.11x | 0.95x |

**The circularity (do NOT manufacture agreement).** Canonical a0 was *defined* as
cH_Lambda/Z from a **cosmological (Planck) Lambda**, so rho_DE(canonical) *is* the
Planck rho_Lambda by construction. Matching it to the SNe rho_DE (1.03x) only
re-checks Planck-vs-SNe Lambda -- **algebra run backwards, not a test**. The
**genuine** test uses the **measured** a0 (SPARC rotation-curve dynamics alone, no
Lambda input): GLS gas-dom lands **~1.4-1.6x** the SNe rho_DE (within ~1-1.5 sigma),
the median variant **~0.9-1.1x** (<~0.3 sigma).

**Sarkar relevance.** The measured-a0 galaxy density is genuinely independent of the
SNe leg. The honest spread (~1x-1.6x) is *consistent* with the SNe rho_DE, **not a
clean confirmation**; it neither manufactures agreement nor a null.

## Files
- `setup.py` (exit 0) -- computes all of the above.
- `setup_results.json` -- hand-off for the compute lane.

## Credits
Milgrom (a0 kernel; nu = sqrt(1+1/y) is Milgrom 1999 PLA 253:273 Eq 9 -- the
framework's distinctive content is the cH_Lambda/Z coefficient); Perlmutter/Riess/
Schmidt (accelerating-universe discovery); Brout+2022 / Scolnic (Pantheon+);
Sarkar (the SNe-leg critique). Background is LCDM; rho_DE-from-SNe is standard;
the framework adds the galaxy cross-check only. No 'proves'.
