# CFG549 FROZEN CRITERIA: what the framework predicts, measures and leaves free for the dark-energy density ρ_DE(z)

Written 2026-10-09, before any script for this lane exists and before any number in it is computed. Committed alone.

**Owner request:** "figure out how to predict the dark energy density evolution."
**Owner requirement (relayed the same day, folded in before this file was committed):** the framework's predictions for ρ_DE(z) must be
derived INDEPENDENTLY, with no DESI, DES or supernova input. DESI DR2 and DES enter only afterwards, as a frozen test. Where no independent
prediction exists beyond the settling trickle, say so plainly. Nothing is tuned to DESI.

Standing: κ = ½ is FITTED (two footings, canonical 9.3603e-11 and alt 1.1312e-10 m s⁻², never pooled). The cold energy's mass is required;
its amount (Ω_c/Ω_b = 5.364) is an input. Not "theory closed". Never "the data favour the framework". No downloads. nice -n 10, ≤ 2 threads.

## 0. Labels

Every route and every model gets one label:
- **PREDICTION**: ρ_DE(z) (or w(z)) follows with no free function and no dark-energy data.
- **MEASUREMENT**: data turn into ρ_DE(z) through the law; the framework supplies the mapping, not the answer.
- **FREE**: the framework allows a function or constant that nothing in it fixes.

Each record model of dark-energy dynamics also gets a provenance label:
- **DERIVED**: no dark-energy data used to build it.
- **USES DE DATA**: DESI, DES or SN data enter its construction.
- **RESTATEMENT**: a free constant or function carries the content.
- **NO DE DYNAMICS**: it assumes Λ and says nothing about ρ_DE(z).

## 1. Independence firewall (frozen)

1. The prediction script (`cfg549_predict.py`) must not open any file under `_external_data/desi_dr2_chains`, any DES file, or any SN
   file. It writes `cfg549_predictions.json`, and its SHA-256 goes to `PREDICTIONS_HASH.txt` before the test script runs.
2. Allowed prediction inputs:
   - κ, fitted to galaxies (CFG541 JSON settings: κ = 0.5, both footings);
   - the cosmic cold amount and f_b (CFG541 JSON: cold_per_b, f_b);
   - E_sink per unit settled mass for the MW-like, group-like and cluster-like systems (CFG541 JSON `one_d`);
   - the settled-fraction anchor 0.162 (CFG506 `cfg506_diag_results.json`, D1, 512³);
   - H0 and Ω_m from CFG541's JSON settings (h = 0.674, Ω_m = 0.3134), and the primordial amplitude and tilt from Planck 2018
     (ln 10¹⁰A_s = 3.044, n_s = 0.9649) for the linear power spectrum through CAMB. **These are CMB numbers; they are unavoidable for a
     collapse history and are declared as such.** No BAO, SN or lensing-survey number enters.
3. The test script (`cfg549_test.py`) reads `cfg549_predictions.json` and checks its hash before opening the DESI chains.

## 2. Routes

### R1 SETTLING SOURCE (expected label: PREDICTION)

dρ_DE/dt + 3H(ρ_DE + p_DE) = Q_settle(t). The sink is modelled as a vacuum-like component (w_s = −1). This is the maximal accumulation:
any w_s > −1 dilutes the deposit.

- Settled energy per comoving volume U(z) = ρ_c0 ∫_{M_min} e(M) dF/dlnM dlnM. F is the Sheth–Tormen collapsed fraction (δ_c = 1.686,
  top-hat, CAMB linear P(k) at the §1 parameters; the record's growth is CDM-like, CFG508/CFG424-460). e(M) = E_sink/M per unit settled
  cold mass, interpolated in log e vs log M_tot through CFG541's three systems, where M_tot = M_b (1 + M_cat/M_b). Beyond the end points
  it is extrapolated with e ∝ M^{1/2} (V_f² under the BTFR). M_min = 1e8 M☉ primary; 1e6 and 1e10 reported.
- Physical source: Q c² = a⁻³ dU/dt. Then Δρ_DE(a) = ∫ Q dt, 1 + w_eff(z) = −Q / (3H ρ_DE), and Δρ_DE(0)/ρ_DE(0).
- Branch A: the Sheth–Tormen F as is. Branch B: F rescaled so that F(z = 0) = 0.162 (CFG506). Reported separately, never pooled.
  Footings are reported separately.
- CPL projection: least-squares fit of ln[ρ_DE,eff(z)/ρ_DE,eff(0)] on z ∈ [0, 2.5] (51 points) to CPL, where ρ_DE,eff = ρ_tot − ρ_m0 a⁻³.

### R2 THE LAW AS A DARK-ENERGY PROBE (expected label: MEASUREMENT)

a0(z)/a0(0) = √(ρ_DE(z)/ρ_DE(0)), independent of κ. Galaxies alone (rotation curves, lensing RAR) are the framework's own channel for
dark-energy evolution, independent of DESI.

- σ(log10 ρ ratio) = 2 σ(log10 a0 ratio).
- Benchmark (comparison only, not input): the DESI DR2 68% half-width of log10 ρ_DE(z)/ρ_DE(0) per chain at z = 0.5, 1, 2, 2.5 (CPL,
  30% burn-in, as CFG511). The required a0-ratio precision to rival it = half that width.
- Calibration wall (CFG256/CFG240): σ(log a0) ≥ 3σ_obj/√N. N per z-bin needed to reach the required precision at σ_obj = 0.1 and 0.2 dex.
- CFG571's sealed predictions translated to ρ_DE: the gas-mass response to the a0 ratio is read from CFG571 JSON (sep_flat against the
  F-DESI/F-flat a0 ratios at z = 1.6; sep_RH against R-H/F-DESI). With a 0.15 dex sample systematic floor, the implied σ(log a0 ratio)
  and σ(log ρ_DE ratio) are reported.
- The CFG511 fork (a0 ∝ √ρ_DE vs a0 ∝ √(−p_DE)): state which observable separates them. Under the framework's own prediction (R1/R3) and
  under DESI (test stage), give the separation size at z = 1, 2.5.

### R3 CLOSURE ROUTES (expected: each FORCES / BOUNDS / RESTATEMENT / NO RELATION)

Derive or rule out, with sympy where useful:
- (a) total dark-sector energy conservation cold ↔ DE, including the cosmic cold amount;
- (b) the supply cap and reservoir cap (CFG364/365);
- (c) the switch / vacuum gate (DE1–DE13);
- (d) a0 consistency across epochs with the settled-profile equilibrium (class A is one-sided: CFG541 open item 5);
- (e) PAPER42's zero-field energy, Λc⁴/a0² = ½∫(ν − 1) d(y²), evaluated for the framework kernel ν_mono;
- (f) CFG542's partner-field principle, read-only at the end. If it gives Q, write the ODE; if it is not landed, say so.

### Record models of dark-energy dynamics (tested the same way)

| model | expected provenance |
|---|---|
| M-Λ: a0 a constant of the Lagrangian / PAPER42 fixed kernel ⇒ w = −1 | DERIVED |
| M-R1: Λ + settling trickle (R1) | DERIVED |
| M-C4: CFG360 C4, vacuum → cold at Γ = a0(t)/c = κ√(Gρ_DE(t)) (zero new constants) | DERIVED; re-run here independently |
| CFG507 M1 running vacuum ν 3H²/8πG | RESTATEMENT (ν free) |
| CFG511 O1 elastic vacuum (Q1b relaxing tension, Q1c √(−p) fork) | USES DE DATA (w(z) is an input) |
| DE1–DE13 gate lanes | NO DE DYNAMICS (Λ assumed) |
| CFG368 F1–F4 cold ↔ vacuum flows | USES DE DATA (Γ fitted to DESI) |
| PAPER42 | DERIVED (w = −1 if a0 constant) |

M-C4 set-up (frozen): ρ_vac' = −Γρ_vac, ρ_c gains the same energy, Γ = a0,foot(t)/c with a0,foot(t) = a0,foot √(ρ_vac(t)/ρ_vac,0);
ω_c fixed at its early (CMB) value, h = 0.674, flat; ρ_vac,0 set by closure (iterated). θ* is not refit (provisional, as CFG368/CFG507).
Projected to CPL as in R1.

### R4 CONSISTENCY (test stage only)

With the DESI DR2 chains, a0(z)/a0(0) = √(ρ_DE(z)/ρ_DE(0)) per sample. Compared with the record's a0(z) constraints:
- KiDS lens-z split (CFG255 stage B JSON): A = +0.060 ± 0.038 dex between z = 0.2045 and 0.3996. The DESI-tracking amplitude is
  A_FLAT + (A_RIVAL − A_FLAT) × Δlog a0,DESI / Δlog a0,RIVAL, linear in the a0 change (declared approximation).
- CFG547 test (a) DESI-tracking verdict (from its JSON).
- the ±0.15 dex inner calibration band of the high-z points (CHART_a0z).
- Rule: TENSION if |Z| ≥ 2 against any constraint; otherwise NO TENSION. DIAGNOSTIC if |DESI-tracking − flat| ≥ 2σ of the constraint.

## 3. The frozen DESI/DES test (written before any prediction is computed)

- Data: DESI DR2 w0wa chains on disk: cmb, pantheonplus, union3, desy5 (the DES input is the DES-Y5 SN chain; no DES 3×2pt is on disk).
  30% burn-in, weights as CFG511. Gaussian approximation: weighted mean μ and covariance C of (w0, wa) per chain.
- Statistic: d² = (p − μ)ᵀ C⁻¹ (p − μ) for each model's CPL point p. Also d²_Λ for (−1, 0).
- Verdict per model:
  - **EXCLUDED** if d² ≥ 11.83 (3σ, 2 dof) in all three SN chains;
  - **TENSION** if d² ≥ 6.18 (2σ) in all three SN chains and not excluded;
  - **CONSISTENT** otherwise.
  The cmb-only chain is reported, not scored.
- **Distinguishable from Λ by DESI** if |d² − d²_Λ| ≥ 1 in at least one SN chain.
- **Observable ever** (generous declared floor for any foreseeable background survey): max over z ≤ 2.5 of |1 + w_eff| ≥ 1e-3.

## 4. Controls

- K1: Sheth–Tormen F(M_min = 1e-6 M☉ equivalent, z = 0) ≥ 0.95 (normalisation).
- K2: CAMB σ8 at the §1 parameters within 0.811 ± 0.015.
- K3: Branch A Δρ_DE(0)/ρ_DE(0) ≤ CFG541's cosmic ceiling 2.24e-6 (JSON S.ii.cosmic_drho_over_rho), both footings.
- K4 (test stage): the chain read reproduces CFG511's a0(2.5)/a0(0) medians 0.827 / 0.782 / 0.798 (± 0.01).
- K5: sympy gives ½∫(ν_mono − 1) d(y²) = 2π⁴/15 exactly.
- K6: the CPL projection of an exact Λ returns (−1, 0) to 1e-6.
- K7: the prediction JSON's hash matches `PREDICTIONS_HASH.txt` before the chains are opened.

## 5. MUTATE (`CFG549_MUTATE=1`, separate outputs)

- MU1: Q_settle × 1e6 (Branch A, canonical). Must be detected: |d² − d²_Λ| ≥ 9 in every SN chain, or EXCLUDED.
- MU2: κ ∈ {0.42, 0.5, 0.55}: a0(z)/a0(0) at z = 0.5, 1, 2, 2.5 identical to ≤ 1e-12. (κ-ratio invariance.)
- MU3: e(M) ≡ 0 ⇒ Δρ_DE ≡ 0 exactly (null).
A MUTATE that fails is reported as a failure and not repaired.

## 6. Verdict format

The framework PREDICTS (what, with numbers) / only MEASURES (what, with required precision) / leaves FREE (what). One-line answer to "can
the framework predict ρ_DE(z)?". If no independent prediction exists beyond the settling trickle, that is the answer, stated plainly.
PREDICTION.md summarises, with one figure: ρ_DE(z) for Λ, the DESI band, the settling-induced curve (scaled to be visible, the scale
stated), M-C4, and the a0(z)/a0(0) ↔ ρ_DE(z) mapping with the sealed-prediction precisions marked.
