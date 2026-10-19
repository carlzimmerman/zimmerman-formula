# CFG854 FROZEN CRITERIA: symbolic regression (PySR) for the satellite-dwarf extra mass from baryonic inputs, tested blind across hosts (before any script)

**Why.** Every framework mechanism examined fails to produce the faint-dwarf excess (CFG822–853); CFG853 found the sharpest clue:
fainter dwarfs need MORE absolute extra mass at fixed radius and dispersion. A compact empirical law for the extra mass, found by
symbolic regression (the AI-Feynman family of methods; PySR 1.5.9, offline) and VALIDATED out of sample, would tell a mechanism
what to produce. Fitting a single number is numerology (CFG642); here the target varies across 25 systems and is tested blind.

## Data (all committed)
- Dwarfs with an excess (Δ > 0.05 dex): CFG844's 25 (CFG828 Δ, Υ_SFH from CFG827).
- Target y = log10(M_extra(<r_1/2)/M_⊙), M_extra = g_law(10^Δ − 1) r_1/2²/G (as CFG842/844). σ enters ONLY the target.
- Inputs (baryonic / stellar only): x1 = log10 M★, x2 = log10 r_1/2 [kpc], x3 = [Fe/H] (LVD `metallicity`), x4 = τ90 [Gyr]
  (CFG824/Weisz). Dwarfs missing x3 or x4 are dropped (listed).
- **Split A:** train = MW satellites, test = M31 satellites + field dwarfs. **Split B:** train = M31 + field, test = MW.

## Models
- PySR: binary + − × ÷, unary none, maxsize 12, niterations 60, populations 15, serial, deterministic, random_state 854;
  model_selection "best" (PySR's accuracy–complexity score). Constants fitted on the training set only.
- Baselines (training-set fits): B0 constant (train mean); B1 linear y = a + b x1 + c x2 (least squares).

## Classes
- **GENERALISING LAW** if in BOTH splits the PySR test RMSE ≤ 0.8 × min(B0, B1) test RMSE.
- **LINEAR SUFFICES** if B1 beats B0 by ≥ 20% on test in both splits but PySR does not meet the GENERALISING bar.
- **NO GENERALISING STRUCTURE** otherwise.
- Report the selected formulas (sympy form), train/test RMSE, and the Pareto front's top 3 per split.

## Controls
- K1 (power): replace y by y_syn = 7 + 0.5 (x2 + 0.5) − 0.3 (x1 − 6) + N(0, 0.1) (seed 854) → PySR test RMSE must be ≤ 0.2 in both splits.
- MUTATE (separate output): y shuffled within each training set → PySR must NOT reach GENERALISING LAW.

κ = ½ fitted; cold energy mass required; not theory closed. A GENERALISING LAW is an empirical regularity, not a mechanism.
