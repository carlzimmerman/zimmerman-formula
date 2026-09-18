# What actually tests the flat law — the ledger (2026-09-18)

The framework's derived law (stage-17, `nbody_2026/stage17_a0z_from_the_action_2026.py`) is a₀² = κ²G(−p_Q) with the vacuum
exactly w = −1: **a₀ is the same at z = 2.5 as today to better than 1%**, and switches off only toward recombination. ΛCDM's
emergent acceleration scale rises instead: +0.09 dex at z = 1, **+0.33 dex at z = 2.5**, +0.73 at z = 5 (Dutton–Macciò 2014
concentration evolution; `L274_a0z_theories_chart.py`, validated against PAPER7's factor 2.1). The two laws differ by nothing at
z = 0, by less than the systematics at z ≈ 1, and by a factor 2 at z ≈ 2.5. Every number below is from a committed lane or a
deposited paper; nothing here is new physics.

## The three requirements of a test

1. **z ≥ 2**, where the predictions are 0.3 dex apart (at z = 1 they are 0.09 dex apart, inside the systematics).
2. **The deep-MOND regime**, g_bar(R_out) ≲ 0.3 a₀, where the Tully–Fisher zero point carries the full a₀ lever; at the
   accelerations of every published high-z sample (0.5–6 a₀) only 7–55% of an a₀ shift reaches the zero point
   (dilution x/(2+x), `prep_2026/highz_tfr_fork/data_ledger.csv`, `L276_data_vs_models_a0z.py`).
3. **A baryonic mass good to ≈ 0.1 dex** (stellar M/L and gas), because the observable is log M_b − 4 log V_f.

Nothing published has all three.

## Tests, ranked

| test | z | regime | what it reaches | status |
|---|---|---|---|---|
| one strongly lensed, rotationally supported galaxy, JWST/NIRSpec IFU + ALMA, deep-MOND BTFR zero point | 2.3–2.9 | deep MOND | 0.00 (flat) vs +0.33 (ΛCDM) at ±0.13 dex: 2.5σ, single object | **pre-registered** in PAPER7 (v3 DOI 10.5281/zenodo.22833314): gate, funnel, statistic frozen; 21 candidate objects on the ledger, none yet passes the rotation, lens-quality and g_bar < 0.3 a₀ gates simultaneously |
| outer-disc CO / [C II] rotation at 2–3 r_M = √(GM_b/a₀) (25–35 kpc for 10¹¹ M☉) in ordinary discs, ALMA / ngVLA | 2–2.5 | outer disc | the same lever; a sample of ~10 at ±0.03 dex in velocity reaches ±0.13 on the zero point | no such sample exists; this is the question for radio observers |
| the lensed-dwarf sample of Jeanneau+26 refit at g_bar < 0.5 a₀ | 1.06 (median) | deep MOND: g_bar/a₀ median 0.16, 76% of the a₀ lever survives | **DONE 2026-07-16** (`prep_2026/jeanneau_refit/`, frozen cuts, adversarially verified; re-run 2026-09-18, identical): N = 61 of 95; Δb = **+0.140 dex**, ±0.070 stat, **±0.272 honest** (coherent gas term ±0.20 dominates: 83% scaling-relation gas). Predictions for this subsample: flat law **0.000 → 0.51σ, compatible**; ALT a₀ ∝ H(z) −0.243 → 1.41σ lean against it (≈1.0–1.3σ after the verified +0.02…+0.11 selection bias); ΛCDM halo term −0.363 (degeneracy not broken, escapes via gas); framework with DESI at face value through the pressure law: −0.05 … −0.11 (0.76 × the z = 1 shift of +0.06/+0.10/+0.14 for Pantheon+/DESY5/Union3, L275) → 0.7–0.9σ, compatible. **Still underpowered**: the band exceeds every separation. Upgrade path: direct gas masses (ALMA CO or dust continuum) for a subset, bringing the coherent term to ≲ 0.10 and B to ≈ 0.15 |
| Euclid galaxy–galaxy lensing RAR around z ≈ 0.5–1 lenses | 0.5–1 | deep MOND at 100s of kpc | a direct a₀, but needs ±0.03 dex and control of the 2-halo term | future; the 2-halo term is the record's known obstacle (L248: inside 1 Mpc the lensing mass is 1.5–8.7× the galaxies' own budget) |

## What already leans flat but cannot decide

McGaugh+24 (no evolution of the BTFR / dark-matter fraction to z ≈ 2.5); Milgrom 2017 (all but excludes a₀ four times larger at
z ≈ 2 and the (1+z)^{3/2} law); the z = 3.25 "Big Wheel" disc (a₀,eff ≈ local); the repository's own KMOS3D and KROSS kinematics.
Each is consistent with the flat line and each sits at accelerations, or carries systematics, that also fit ΛCDM within its errors
(`L276`: every baryonic Tully–Fisher row in the 17-row ledger is within 2σ of every law; the two z = 0.9 baryonic points disagree
with each other by 0.44 dex).

## What does not test it

- **RAR fits on compact star-forming discs at z ≈ 1** (MUSE-DARK III, MIGHTEE-HI): ΛCDM itself predicts an *apparent* a₀ rising
  ×3 by z = 2 from such fits (Mayer+2023), and the measured rise (+0.38 dex at z ≈ 1) sits above every law, including ΛCDM's
  (`real_research/A0Z_MUSE_DARK_III_CONFRONTATION.md` §7 for the method audit: baryonic acceleration is a model output of a
  ΛCDM-halo decomposition with dynamically fitted stellar masses, modelled gas, unbudgeted pressure support).
- **Anything at z < 1 at ±0.1 dex precision** (the laws differ by < 0.1 dex there).
- **DESI and the supernova catalogues** (they measure w(z), not a₀; mapped through the framework's own law at face value they move
  a₀ by +0.01 to +0.06 dex at z = 2.5, `L273`/`L275`).
- **The value of a₀ today** (shared with any constant-a₀ MOND; κ = ½ is fitted, provably underivable in this action class).

## Standing

The flat law is **untested, not unsupported**: one method-dependent tension (MUSE, non-diagnostic), several neutral results,
zero confirmations, zero clean refutations. The Jeanneau refit is done and compatible with the flat law at 0.5σ but underpowered by its gas term; the two things that can be
done now are direct gas masses for that subsample and the search for the lensed rotator; the decisive datum is the pre-registered
measurement. Nothing here derives κ.
