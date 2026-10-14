# CFG769: what condition do the NGC 1052 debris lack? — own supply (A6) sealed out-of-sample; a stellar compactness switch fails SPARC

**Label: Part 1 C-SIGMA = TENSION as frozen (lenient gas-inclusive Σ leaves only 3 SPARC galaxies; 1/3 requires the boost);
REPORTED stars-only Σ: 29/39 require the boost (median Δχ² +342) ⇒ a stellar-compactness switch is dead in practice. Part 2
C-A6 = SEALED (sha256 6d8d8963…f76b), not scoreable yet. MUTATE bites (exit 1).**

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (c7cf0c857), 2026-10-14. Last ID of block CFG760–769.
- **Script:** `python3 cfg769.py` (seconds) → `cfg769.out`, `cfg769_results.json`, `cfg769_SEALED_predictions.json`.
  `CFG769_MUTATE=1` → `*_MUTATE.*`, exit 1 (V_obs := Newton ⇒ no galaxy requires the boost).
- **Data pulled (owner's go):** Vaz+26 (2610.07467), Keim+26 (2603.15860), Tang+25b (2410.19331) PDFs in
  `_external_data/arxiv_cfg769/` (not committed; sha256 in the criteria). Values read from pdftotext of the PDFs, not summaries.
- **Settings:** κ = ½ FITTED; no-EFE ν_mono; the cold energy's mass is required; no particle species; not "theory closed".

## Part 1: compactness switch (C-SIGMA) on SPARC
Trail: debris Σ_e 8.0 / 9.3 / 18.4, LEDA 42.1 M☉/pc² ⇒ lenient Σ_crit = 14.2.

| set | tested | require the boost (Δχ² ≥ 25), can / alt | with Newton Υ_d ≤ 5 |
|---|---|---|---|
| **lenient Σ (stars Υ 0.7 + half the gas inside R_eff): the verdict** | 3 | 1 / 1 (UGC05918 +82) | 0 |
| stars-only Σ (REPORTED, no verdict weight) | 39 | **29 / 29** (median Δχ² +342 / +319) | 23 / 23 |

- **As frozen: TENSION.** The lenient definition counts half of each galaxy's HI inside R_eff. That lifts almost every
  low-surface-brightness disc above 14.2, so the frozen test barely ran. CamB prefers Newton strongly (Δχ² −320); it is a known
  odd case.
- **Reading (post-hoc, disclosed):** a switch on *stellar* density, the quantity measured for the gas-free trail, is ruled out:
  29 of 39 SPARC discs below the threshold need the boost at ≥ 5σ, and 23 still do with Newton allowed Υ_d up to 5. A switch
  survives only if gas counts toward the threshold. That makes it a different, untested rule, and the trail cannot calibrate it
  because the trail galaxies have no gas.

## Part 2: SEALED predictions of own supply (C-A6)
C-A6 = the framework's rule A6: cold energy settles only from a system's own supply. Debris lost theirs in the collision
(CFG657 channel S) and cannot acquire more (CFG768 A: α_P = 0 under one c_P), so they stay Newtonian forever. The CFG763/764
clocks become the settling rate of a galaxy's own supply, not formation from nothing. That removes CFG768 B's conflict.
Labels from vD+22 (pre-kinematic). CFG655 estimator, no EFE, D = 20 Mpc (17.7–21.7 bracket):

| galaxy | label | log M* | σ_Newton (km/s) | σ_law can / alt | C-A6 predicts |
|---|---|---|---|---|---|
| DF5 (RCP 11) | E | 7.15 | 2.73 (2.62–2.91) | 10.1 / 10.6 | σ_N |
| DF7 (RCP 9) | T | 7.02 | 2.46 | 9.4 / 9.8 | σ_law |
| RCP 16 | E | 6.97 | 3.66 (3.51–3.89) | 9.3 / 9.8 | σ_N |
| RCP 21 | E | 6.78 | 2.06 | 8.2 / 8.6 | σ_N |
| RCP 26 | E | 7.40 | 4.55 (4.37–4.84) | 11.9 / 12.5 | σ_N |
| RCP 28 | E | 6.49 | 1.75 | 6.9 / 7.2 | σ_N |

Plus NGC 5557-E1 (~4 Gyr old TDG): Newtonian band 16–24 km/s, not the law's 28–41 km/s.

**Seal:** sha256(`cfg769_SEALED_predictions.json`) = `6d8d89639d71b53ac00e3d4d3f5ea729b75d2fea40e2f868db7c102834d1f76b`.
Kill rule: any E galaxy measured inconsistent with σ_N at ≥ 3σ and consistent with σ_law fails C-A6 (given its label).

Practical note: σ_N is 2–5 km/s, at or below KCWI's resolution floor (Vaz+26 σ_inst ≈ 12 km/s, measuring 15.8 ± 2). The law
values (7–12 km/s) are resolvable. The decisive form of the test is therefore an **upper limit**: a measured σ ≲ 5 km/s on
any E galaxy supports C-A6, and a clean ~10 km/s fails it.

## LEDA velocity (recorded, C-REST not scored)
LEDA V = 1600.7 ± 1.3 km/s (Vaz+26); DF9 1661 ± 2 (Keim+26). Vaz+26 find LEDA's stellar populations "inconsistent with
membership of the trail as a collision product", which is independent support for its T label (own supply).

## Hand estimate (before the run)
C-SIGMA EXCLUDED. Wrong as frozen (TENSION; the lenient Σ removed the test set). Right in substance for the stellar-density
form (reported).

## Not tested
EFE; SPARC distance/inclination errors; a gas-inclusive switch calibrated on gas-rich systems; what sets a galaxy's own supply.
