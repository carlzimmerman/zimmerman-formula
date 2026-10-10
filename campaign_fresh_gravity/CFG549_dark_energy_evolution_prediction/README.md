# CFG549: predicting the dark-energy density evolution

The summary and the figure are in `PREDICTION.md`.

**Bottom line.** Built only from its own ingredients, the framework predicts ρ_DE(z) = Λ plus a settling trickle of 2e-7 to 8.5e-7
(|1 + w| ≤ 1.6e-7, phantom side). That trickle can never be observed. Real evolution is FREE in the framework. It can be MEASURED by
galaxies through a₀(z)/a₀(0) = √(ρ_DE ratio), and κ cancels in that ratio.

κ = ½ is fitted. The cold energy's mass is required. This is not "theory closed".

## Files and runs
- `FROZEN_CRITERIA.md` was committed alone first in 19032746a. It includes the owner's independence requirement (no DESI, DES or SN in
  any prediction), which was folded in before that commit.
- `cfg549_predict.py` is stage 1, with no DE data. It writes:
  - `cfg549_predict.out` and `cfg549_predictions.json`;
  - `PREDICTIONS_HASH.txt`, the SHA-256 of the predictions JSON, written before stage 2 ran.
  - Run time ~6 s with nice -n 10 and 2 threads. Exit 0, 8/8 checks pass (K1, K2, K3 ×2, K5, K6, MU2, MU3).
- `cfg549_test.py` is stage 2. It verifies the hash (K7) and only then opens the DESI DR2 chains (cmb, +Pantheon+, +Union3, +DESY5). It
  writes `cfg549_test.out`, `cfg549_results.json` and `cfg549_prediction.png`. Exit 0; K4 and K7 pass.
- `CFG549_MUTATE=1` writes `*_MUTATE.*` for both stages. Exit 0.
  - MU1: Q × 10⁶ is EXCLUDED by DESI (d² − d²_Λ = +65 / +98 / +77 / +88): DETECTED.
  - MU2: κ ∈ {0.42, 0.5, 0.55} leaves a₀(z)/a₀(0) unchanged (max deviation 3e-16).
  - MU3: e(M) = 0 gives Δρ = 0 exactly.
- Inputs, all already on disk; nothing was downloaded:
  - CFG541 JSON (κ, footings, f_b, cold/b, Ω_m, h, E_sink and ΔW per settled mass);
  - CFG506 JSON (settled fraction 0.162);
  - CFG493 JSON (fitted κ);
  - CAMB with Planck 2018 A_s and n_s. These are declared CMB inputs, and so are h and Ω_m.
  - Test stage only: the DESI DR2 chains, plus CFG571, CFG255 stage B, CFG547 and CFG542 JSON (read-only).
  - DES enters only through the DESI+DES-Y5 SN chain. No DES 3×2pt data is on disk.

## Results per route

| route | label | numbers |
|---|---|---|
| R1 settling source | **PREDICTION** | Δρ_DE/ρ_DE(0) is 7.1e-7 / 2.0e-7 (canonical A / B) and 8.5e-7 / 2.4e-7 (alt), all below CFG541's 2.24e-6 ceiling (K3). M_min = 1e6–1e10 M☉ moves A by ≤ 7%. 1 + w(0) is −5.3e-8 (can A), and max \|1 + w\| at z ≤ 2.5 is 1.3e-7. CPL is (w₀ + 1, w_a) = (−6.4e-7, +3.2e-6) on the frozen projection and (−9.8e-8, −1.0e-7) on the H-fit. Observable ever: NO |
| frozen DESI test of the derived prediction | — | identical to Λ (d² − d²_Λ = 0.00). d² = 9.43 / 9.22 / 14.44 / 18.79 (cmb / PP / U3 / DY5) → **TENSION**. Not excluded (PP 9.22 < 11.83) |
| R2 galaxies as the probe | **MEASUREMENT** | Matching DESI+DESY5 on ρ_DE needs σ(log a₀ ratio) = 0.007 / 0.012 / 0.030 / 0.040 dex at z = 0.5 / 1 / 2 / 2.5. At the CFG256 wall that is N ≈ 1730 / 640 / 97 / 56 discs per bin at 0.1 dex per disc. CFG571 KURVS translates to σ(log ρ ratio) ≥ 0.42–0.92 dex at z ≈ 1.6. The fork √ρ vs √(−p) separates by 0 under the framework's own prediction and by +0.09 to +0.17 dex at z = 2.5 under the DESI SN chains; it needs galaxy a₀(z) plus an independent H(z) |
| R3a dark-sector energy conservation | FORCES ONLY THE TRICKLE | sympy: one equation, two unknown functions. With w = −1, ρ_DE = C₁ + ∫Q dt, and C₁ is FREE |
| R3b supply and reservoir caps | NO RELATION | a galaxy-level inequality that needs f_ret; no ρ̇_DE |
| R3c switch / gate (DE1–DE13) | NO RELATION / NO DE DYNAMICS | Λ background assumed; DE7 found the gate ill-posed as an action term |
| R3d settled-profile consistency | BOUNDS (ratchet) | It never binds under the framework's own prediction. Under DESI, local galaxies would read a₀ of the past maximum: +0.016 to +0.038 dex in the SN chains, i.e. κ_fit high by 4–9% |
| R3e PAPER42 zero-field energy with ν_mono | DERIVED, coefficient FAILS | ½∫(ν_mono − 1) d(y²) = 2π⁴/15 (sympy plus quadrature, K5). The implied κ = 1.391 against 0.417 ± 0.095 (+10.3σ). It agrees with the record's kappa_closure K5 class result |
| R3f CFG542 partner field | Q DERIVED, w(z) FREE | Its results landed during this lane (read-only; they appear uncommitted). Q = ρ_c α τ_ff ∇ψ·∇Φ takes the whole ΔW, up to 3.65 × E_sink, so R1 scales to ≤ 2.6e-6 (max \|1 + w\| ≤ 4.9e-7). The partner's w(z) is an input, α is FREE, and a canonical partner is singular at w = −1. No ODE closes ρ_DE(z) |
| R4 consistency | NO DESI-SPECIFIC TENSION; NOT DIAGNOSTIC | KiDS split: Z = +1.49 to +1.52 in the SN chains, both footings (cmb-only +1.44). DESI-tracking max \|Δlog a₀\| at z ≤ 2.5 is 0.08–0.11 dex (medians), inside the 0.15 dex band. The frozen rule reads TENSION through CFG547's native route O2 (Z 2.08–2.09), which flat a₀ also fails (Z −2.3): the calibration wall |
| M-C4 (CFG360 C4 re-run, Γ = a₀/c) | DERIVED (posited rate) | (w₀, w_a) = (−0.961, −0.038) canonical and (−0.954, −0.044) alt. TENSION, with d² 10.04 / 8.10 / 12.76 / 14.32. The cold energy gains 9.8% by today |

## Disclosures (dated 2026-10-09/10; frozen text not edited)
1. **The frozen CPL projection is undefined for M-C4.** ρ_DE,eff = ρ_tot − ρ_m0 a⁻³ crosses zero at z ≥ 2.08 (canonical) and ≥ 1.91 (alt),
   because the cold energy gains energy late. M-C4 is therefore projected post-freeze by fitting a flat-CPL H(z) (Ω_m free, H0 fixed) on
   z ∈ [0, 2.5]; the maximum residual is 6e-5. R1 is reported on both projections. Its verdict is the same on either, because R1 is
   indistinguishable from Λ.
2. **The R3f block was added to the test script after the first test run.** CFG542's results appeared while this lane was working. It is
   a report only and changes no verdict.
3. **KiDS A** is now read from CFG255's JSON (`A_data` = 0.0595). The first test run used the README's rounded 0.060 (Z +1.53 → +1.50).
   Both test modes were re-run.
4. **M-C4 is CFG360's posit.** The rate Γ = a₀/c is not derived from an action, θ* was not refit (as in CFG368/CFG507), and its
   vacuum → cold direction is opposite to CFG541's required cold → DE sink. It is reported as a record model, not as the framework's law.
5. **Gaussian approximation.** The DESI test uses a Gaussian (w₀, w_a) approximation for each chain. d²_Λ reproduces CFG368's ΛCDM
   values (9.43 / 9.22 / 14.44 / 18.79).
