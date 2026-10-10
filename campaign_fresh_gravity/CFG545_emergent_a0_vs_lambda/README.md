# CFG545: does ΛCDM's emergent RAR scale track Λ? Estimate s = d ln a₀/d ln Λ ≈ −0.01 to +0.16 against the owner's 0.5. As frozen: NOT DIAGNOSTIC (the primary variant misses "coincidence-like" by 0.011). Overall: TEST NEEDS NEW SIMULATIONS

The setup:
- Criteria were committed first, alone: **58aa36f22**.
- Script: `cfg545_lambda_scaling.py` (~5 min, niced, ≤ 2 threads). MUTATE: `--mutate` (~45 s).
- κ = ½ is FITTED. Footings 9.36e-11 / 1.13e-10 are never pooled. Cold energy mass is still required and no dark-matter particle is added.
- ΛCDM is the comparator. Nothing here says the data favour the framework, and the theory is not closed.

**The question.**
- The owner's picture (cold energy clumps first, galaxies form inside, a₀ = κ c √(G ρ_DE)) predicts **s = 0.5**.
- In ΛCDM, the emergent scale (CFG477: 9.7e-11 with DC14 cores) is set by galaxy formation and halo structure. It should depend on Λ only through how Λ alters halo formation.

## 1. Census (dated 10-09)
Sources are arXiv abstracts via the export API (CC0) and WebFetch summaries, which are **PROVISIONAL**. Only the Magneticum number was read from the paper text.

**(a) ΛCDM simulations that measure an emergent RAR / a₀, and what sets it in their own words:**

| work | a₀ / g† | what sets it (authors' explanation) |
|---|---|---|
| Keller & Wadsley 2017 (MUGS2, 32 discs) | matches SPARC's (abstract gives no number) | "dissipative collapse of baryons"; Mayer+23 cite a decline of a₀ toward z = 0 in MUGS2 |
| Ludlow+17 (EAGLE variants) | g† present; feedback variants move galaxies *along* the relation | galaxy formation in CDM halos |
| Navarro+17 | a₀ and a_min | self-similar CDM halo acceleration profiles (broad central maximum bracketed by a_min, a₀ over the disc-hosting mass range), plus the halo-mass and size scalings of any successful galaxy-formation model |
| Dutton+19 (NIHAO, 89 galaxies) | RAR scatter 0.079 dex (abstract gives no g†) | ΛCDM galaxy formation |
| Paranjape & Sheth 2021 | — | quasi-adiabatic relaxation of CDM around baryons, plus feedback |
| Grudić+20 (FIRE context) | g† ≈ ⟨ṗ/m★⟩ ≈ 1e-8 cm s⁻² ~ 0.1 G m_p/σ_T (= 1.68e-10 m s⁻²) | stellar-feedback momentum per unit stellar mass. **Contains no cosmological parameter: s = 0 by construction** |
| Mayer+23 (Magneticum) | **1.12e-10 m s⁻² at z ≈ 0.1**; rises ×≈3 to z = 2 | the different distributions of dark matter and baryons; they cite Grudić's surface-density threshold |
| record: CFG477 | 9.69e-11 (DC14 cores on SPARC baryons) | SHMR + concentration + DC14 response |

**(b) Simulations with varied Λ.**
- **Barnes+18** (EAGLE, 25 cMpc, Λ = 0, 0.01, 0.1, 1, 3, 10, 30, 100, 300 Λ₀) holds baryon and CDM mass per photon fixed and uses identical initial conditions. It measured collapse fraction, mass and baryon accretion, star-formation efficiency and metals.
- **Salcido+18** (EAGLE 50 cMpc, ΛCDM vs Einstein–de Sitter) measured the cosmic SFR, stellar mass density, GSMF and sSFR.
- Sudoh+17 (a semi-analytic anthropic test) was located but not read.
- **None of these, as summarised, measured rotation curves, circular-velocity profiles, the RAR, a characteristic acceleration, halo concentrations or galaxy sizes.**
- So no published s exists. The summariser readings are provisional and the PDFs were not text-verified.
- Dolag+04 (dark-energy w-models, N-body only): concentration tracks the linear growth factor at collapse, c₀ → c₀ D₊(z_coll)/D₊,ΛCDM(z_coll). This was used as a model variant.

## 2. ΛCDM estimate of s
**Model** (frozen):
- CFG477's machinery, exec'd unedited, seed 77, 200 realisations per λ. Only its c(M) is multiplied by c_λ/c₁.
- What varies: ρ_Λ only. Physical ω_m, ω_b and the early amplitude are fixed, as in Barnes+18.
- Linear theory: D(a) and EH98 no-wiggle σ(M).
- Concentration from the Ludlow+16 collapsed-mass model (ρ_crit or ρ_m form) or the Dolag+04 growth scaling.
- Observed at a = 1 (P) or at fixed age (T).
- **SHMR, DC14 response and galaxy sizes are held fixed** (declared; this is the main limitation).

| variant | s at Λ₀ | span slope 0.1–10 Λ₀ | a₀(10 Λ₀)/a₀(Λ₀) |
|---|---|---|---|
| **L16-crit / a = 1 (primary)** | **+0.161** | +0.178 | 1.87 (owner: 3.16) |
| L16-m / a = 1 | +0.105 | +0.114 | |
| D04 / a = 1 | −0.014 | −0.024 | |
| L16-crit / fixed age | +0.096 | +0.139 | |
| L16-m / fixed age | +0.051 | (λ = 100 has no L16 solution; skipped, disclosed) | |
| D04 / fixed age | −0.014 (the D04 rule has no observation-epoch term) | −0.024 | |
| analytic proxy g₋₂ = G M₋₂/r₋₂² (L16-crit, a = 1) | +0.089 (10¹¹ M_⊙), +0.107 (10¹² M_⊙) | | |
| **owner's picture** | **0.5** | 0.5 | 3.16 |

**What the frozen rule gives.**
- max |s| = 0.161 > 0.15, and the primary 0.161 < 0.35, so the label is **NOT DIAGNOSTIC** as frozen.
- The primary misses "coincidence-like" by 0.011. Every variant lies between −0.014 and +0.161, at most a third of the owner's 0.5.

**Why ΛCDM's s is positive.** At fixed physical matter density and fixed early amplitude, a larger Λ halts growth sooner. A halo of given mass seen today is then a rarer, earlier-formed and denser object, so its concentration goes up: c ratio 1.06 at 2 Λ₀ and 1.33 at 10 Λ₀ for 10¹² M_⊙. That raises the inner halo acceleration, and with it the fitted a₀. The sign matches the owner's prediction and the size is ≲ ⅓ of it.

**Stellar-feedback explanation (Grudić+20).** Here g† is microphysical and s = 0 exactly.

**Precision needed** (two runs at Λ₀ and 10 Λ₀, separating 0.5 from the primary 0.161 at 3σ): per-run error in ln a₀ < 0.184 (0.080 dex). Hydro RAR fits reach this easily (Magneticum quotes ±0.04 on 1.12).

## 3. Time domain (the observable version, no new data)
At fixed Λ (w = −1), the owner's picture predicts a **flat** a₀(z). For DESI-like evolving dark energy it predicts √ρ_DE(z), ≈ 0.8 at z = 2.5 (record).

Feedback-ΛCDM's emergent scale rises:
- CFG565 (committed JSON): g†(z)/g†(0) = 1.20 (1.02–1.90) at z = 1, **2.82 (1.52–8.20) at z = 2**, 4.88 (2.01–9.70) at z = 2.5.
- Mayer+23 (Magneticum): ×≈3 by z = 2.
- Keller & Wadsley's MUGS2 trend has the same sign (as cited by Mayer+23).

So ΛCDM predicts a drift of roughly +0.3 to +0.5 dex by z ≈ 2, opposite in sign to the owner's picture.

**Caveat (CFG566):** through the record's existing high-z estimators, which use near-Newtonian points in compact discs, the drift shrinks to ~0.17 dex. Their power is ≤ 0.06, so it is **not yet observable with data on disk**. It needs discs measured out to low g_bar, with measured gas.

## 4. Verdict
**TEST NEEDS NEW SIMULATIONS.** No published varied-Λ run measured an acceleration scale. The analytic ΛCDM estimate (s ≤ 0.16) is NOT DIAGNOSTIC by the frozen threshold, but it lies well below the owner's 0.5 in every variant.

**What would decide it.** Rerun a Barnes+18-style suite at Λ₀ and 10 Λ₀ (ideally plus 0.3 and 3 Λ₀), with these properties:
- **Resolution:** discs resolved down to g_bar ~ 1e-12 m s⁻². That means zooms or a ≥ 25 cMpc box at EAGLE/FIRE/NIHAO resolution, with the same initial conditions and the same subgrid feedback.
- **Measurement:** the RAR (g_obs vs g_bar from V_c and baryon profiles) for central discs at z = 0. Fit a₀ with the same ν function. Also report c(M), the SHMR and the sizes.
- **Verdict:** ln[a₀(10Λ₀)/a₀(Λ₀)] / ln 10 against 0.5. The per-run precision needed is 0.08 dex.

Note that standard ΛCDM simulations can only measure ΛCDM's s. The owner's picture needs its own simulation, with cold energy and a₀ tied to ρ_DE, to be confronted in the same way. The *observable* discriminator remains a₀(z) at z ≈ 2.

**Downloads that would help (owner's go needed; none made):**
- The Barnes+18 / Salcido+18 varied-Λ EAGLE snapshots, if public: these would let the RAR be measured directly on the existing runs. Availability and size are unknown (EAGLE public releases cover the reference runs; the varied-Λ runs have not been seen on the public database). Ask the authors.
- The Barnes+18 and Salcido+18 full-text PDFs (~2–5 MB each, arXiv 1801.08781 / 1710.06861), to verify the census readings beyond the summariser.

## Controls
- K1 PASS: λ = 1 reproduces CFG477's median a₀ 9.6864e-11 exactly.
- K2 PASS: D(a) = a for λ = 0.
- K3 PASS: the concentration ratio is 1 at λ = 1.
- K4 PASS: L16-crit gives c(10¹²) = 8.20 against Dutton–Macciò 8.33.
- K-null PASS: s = 0 with λ held fixed.
- **MUTATE:** with the owner's law injected (a₀ = 9.36e-11 √λ), the same estimator recovers **s = 0.499** (exit 1, bite detected). The estimator can see a √Λ scaling. In the MUTATE output K1 reads "FAIL"; that is expected, because the halo is replaced by the law.

## Scope
- SHMR, DC14 response and sizes are held fixed with Λ (supported only by Barnes+18's small change in star-formation efficiency for λ ≲ 10, a summariser reading).
- One halo-mass convention: a fixed physical aperture at 200 ρ_ref.
- Ludlow+16's C = 650 and f = 0.02 are taken at their ΛCDM calibration.
- Radiation is ignored.
- The census of what each paper measured is provisional (abstracts and summaries).

One line (ledger): CFG545: ΛCDM's emergent RAR scale vs Λ (CFG477 machinery, c from Ludlow+16/Dolag+04, SHMR/DC14/sizes fixed). s = d ln a₀/d ln Λ = −0.014 to +0.161 (primary +0.161) vs the owner's 0.5. As frozen, NOT DIAGNOSTIC (0.011 over the 0.15 line). No published varied-Λ run measured an acceleration scale, so TEST NEEDS NEW SIMULATIONS. MUTATE recovers an injected 0.5 as 0.499. The time-domain discriminator stays CFG565's rising g†(z) (×2.8 at z = 2) against a flat a₀.
