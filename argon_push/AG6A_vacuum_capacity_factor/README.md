# AG6A: vacuum capacity factor. **SCOPED NO-GO** (scale side): no capacity of the vacuum fixes κ; κ = ½ stays FITTED

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (199ba297e), before any script or number.
- **Run:** `OMP_NUM_THREADS=1 nice -n 10 python3 ag6a.py > ag6a.out`: under 1 s, about 100 MB peak, exit 0, **26/26**.
  `AG6A_MUTATE=1 ... > ag6a_MUTATE.out`: exit 1, **19/26**. Every mutation bites:
  - Mu1 flips the two horizon checks;
  - Mu2 flips the equipartition bound and the no-hit check;
  - Mu3 flips the exact-½ check;
  - Mu4 flips the dataset-spread and crossing checks.
  Both runs went beside the live 1024³ job.
- **Scope:** scale only. Which law shape (n) a saturating medium gives belongs to AG6B (dbcaeba9e). Nothing here scores SPARC.
- **Settings:** κ = ½ FITTED; Z ≡ κ, Z = 2√(8π/3) = 5.788810; footings 9.3603e-11 and 1.1312e-10, never pooled; no
  dark-matter particle; not theory closed. Units c = 1, H = H_Λ, a₀ = κ√(Gρ_Λ), H² = (8π/3)Gρ_Λ.

## The argument in one paragraph
Taken on its own, the vacuum has no capacity that sets a₀.
1. **Horizon capacity.** For an eternally accelerated observer in dS₄, the causal horizon is the same bifurcation sphere,
   area 4πL², at every acceleration (embedding computation, M1.2). Acceleration consumes no horizon entropy. The only local
   datum that depends on a is the KMS/Tolman temperature √(a² + H²)/2π (M1.3).
2. **Thermal capacity.** Build an inertia law from the bath energy along the orbit, F(a) = f(A) − f(H), with a Newtonian
   limit. Its deep scale is exactly a₀ = 2cH/f′(T_GH) (B.1).
   - A bath of harmonic modes obeys f′ ≤ 1 (equipartition: Einstein and Debye functions ≤ 1, B.3). So a₀ ≥ 2cH_Λ and
     κ ≥ 2√(8π/3) = 5.79.
   - Milgrom's 1999 value is therefore the **floor** of this class, and quantum modes push a₀ up, away from the framework.
   - κ = ½ would need a bath heat capacity of 2Z = 11.58 times the classical value at T_GH. The whole MOND transition would
     also have to sit within 1.5% of T_GH (0.37% for the n = 2 rest scale).
3. **Holographic capacities.** Five horizon-type entries were checked: BH cells, Padmanabhan's degrees of freedom, the CKN
   vacuum ball, the Bekenstein patch and Compton dipoles.
   - All of them read H, so κ² = rational × π^(±1), never ¼.
   - The closest, k03's √(2/(3π)) = 0.461, lies in the data band but is not ½.
4. **Enthalpy capacity.** The vacuum's own inertial density ρ + p is exactly zero for Λ.
   - For DESI's evolving dark energy, a capacity √(G(ρ + p)) gives κ_eff(0) = √(1 + w₀) = 0.40–0.76, depending on the
     dataset.
   - It vanishes where w crosses −1, at z = 0.35–0.50, so it cannot be the framework's a₀.

**Net:** a capacity can explain *that* the polarization saturates. It cannot explain *where*. The ½ still needs the
dark-energy density coupled through bare G with coefficient ¼, the record's open target (CFG263/264, p61 PREMISE A).
No capacity principle supplies it.

## Results
| mechanism (field) | what was computed | κ it gives | verdict |
|---|---|---|---|
| M1 horizon-information capacity (QFT in curved space, holography) | A_h(a) = 4πL² exactly, dA_h/da = 0; T = √(a²+H²)/2π | none (no scale) | SCOPED NO-GO, geometric |
| M1b thermal (KMS/Tolman) capacity (statistical mechanics) | a₀ = 2cH/f′(T_GH); f′ ≤ 1 for harmonic baths; thermal moments (A^k − H^k)^{1/k}: deep MOND only at k = 1 | ≥ 5.79 (classical 5.79; one mode at ω = H 78.2; Debye 1D/3D 11.4/23.9) | SCOPED NO-GO; the floor is new |
| M2 holographic/Bekenstein polarization capacity | 5 entries × n = 1, 2; ħ and G cancel in all | 1.447, 2.894, 5.789 (BH cells, CKN, Bekenstein, Padmanabhan); 0.461/0.921 (Compton dipole) | SCOPED NO-GO (π-grade); 1/10 in band |
| M3 enthalpy capacity (fluids, cosmology) | Λ: 0. DESI rows: κ_eff = √(1+w₀) = 0.762 / 0.402 / 0.577 / 0.498 (CMB / +Pan+ / +U3 / +DESY5); z_× = 0.50 / 0.35 / 0.44 / 0.41 | dataset-dependent | SCOPED NO-GO |

**Key numbers** (all from `ag6a_results.json`):
- **Factor.** Milgrom's κ = 2√(8π/3) = 5.788810, numerically equal to Z.
  - The ratio to κ = ½ is 2Z = 11.5776 = √(8π/3) × 4: the Friedmann conversion (forced) times a rational 4 (open).
  - In SI, Milgrom's 2cH_Λ = 1.084e-9 sits +1.06 dex above the canonical a₀, and +0.97 dex above AG4f's n = 2 SPARC a₀.
- **Required slope.** f′(T_GH) = 11.5776.
- **Temperature windows.** δ₁ = 0.014811 at a = a₀; δ₂ = 0.003723 at a = a₀/2.
- **Escapes.** A Schottky escape needs ≥ 24.1 two-level systems per classical degree of freedom, with gaps tied to T_GH
  (≥ 2 free choices).
- **M3 spread.** The four κ_eff(0) values span 0.359; only 1 of 4 lies within 1σ of ½. χ² about ½ is 6.66, illustrative only
  because the rows share DESI + CMB.
  - The other declared normalisations (ball, Friedmann, Jeans) give 0.82–2.70.
  - At z = 0.2, M3 predicts a₀(0.2)/a₀(0) = 0.62–0.79. The framework's √ρ_DE law gives 1.03–1.13.

## Second prediction
**None survives, because no mechanism passes.** What each would have predicted, for the record:
- **Thermal class:** the n = 2 hyperbola, with a₀ ≥ 2cH_Λ. Excluded by the record (equation book: 15.6σ).
- **M3:** a₀ falls by 20–40% by z = 0.2 and reaches zero at z ≈ 0.4. That is a sharp discriminant from the framework.
  - In-repo a₀ at z ≈ 0.2–0.5 is not calibrated (CFG260/281 BUDHIES; CFG255: a KiDS lens-z split is not possible).
  - So against data it is **NOT DIAGNOSTIC**. Theoretically it is excluded anyway: a₀² < 0 beyond z_×.

## What is new against the record
- **New.**
  - **(a) The capacity is a-independent.** The accelerated observer's causal horizon in dS₄ has area 4πL² for every a. This
    closes "acceleration consumes horizon entropy" routes. By the same causal structure (reasoned, not computed here), it
    holds for any worldline confined to one static patch.
  - **(b) The slope theorem and the equipartition floor.** a₀ = 2cH/f′(T_GH), and f′ ≤ 1 for harmonic baths, so Milgrom's
    1999 coefficient is a lower bound on a₀ in this class, not merely one point. The record already had the related results:
    agentYY found the modular free energy monotone, and X3 showed selection conditions give algebraic K. This lane adds the
    inequality and the exact heat-capacity ratio (2Z) a thermal route would need.
  - **(c) The required-bath diagnostic.**
    - What it shows: for either framework law, the bath's C/C_classical would have to be ≈ 2Z at T_GH, fall roughly like
      (T − T_GH)^(−1/2) above δ ≈ 0.015, and reach 1 at T ≫ T_GH. The local slope reaches −0.37 (n = 1) and −0.43 (n = 2)
      in the short window.
    - In words: a bath tuned to be critical at T_GH, with a₀ as its free rounding scale.
    - Status: post-freeze, a diagnostic and not a gate.
  - **(d) The enthalpy capacity on the DESI DR2 rows,** including the DESY5 near-hit (0.498). Its two problems: it is one row
    of four, and it needs the bare-G normalisation (the other three declared q give 0.82–2.70).
- **Reproduced as controls.**
  - CFG47: κ_match = √(8π/3)/n.
  - Equation book / F1: Milgrom's a₀ = 2cH_Λ, a factor 2Z away.
  - X2: ρ + p = 0.
  - k03: 0.4607.
  - The footing value 9.3603e-11.
- **Not new.**
  - The π-grade obstruction: p59 one-π Lean, X3 structural reason, CFG263's rule.
  - The bare-G open target (p61, CFG263/264).
  - That dielectric saturation is only an analogy (CFG695).

## Caveats
- **M1 scope.** M1 covers eternal Killing orbits. Finite-lifetime causal diamonds have areas that depend on the duration, not
  on a; they were not computed.
- **M1b scope.** M1b assumes inertia comes from the bath energy. I did not compute free-energy or entropy functionals. My
  expectation, not computed here, is that they lack the linear large-T behaviour the Newtonian limit needs. Non-harmonic
  baths escape the bound only by inserting a scale at T_GH (B.5, B.6).
- **M2 menu.** M2 is a menu written with the target known. Its 1/10 in-band rate is reported, not used as evidence.
- **M3 inputs.**
  - The DESI DR2 numbers are p13b's recorded read of arXiv:2503.14738 Table 5 (37b55b149). I did not re-read them.
  - The errors are marginal σ(w₀) only, and the CPL form is assumed.
  - q = 1 is a choice.
- **Post-freeze additions, both reported and not gates:** B.6, and the SI footing check (G-record canonical).
- **First run (kept as `ag6a_firstrun_B3a_numerics.out`, 24/25).** B.3a failed on a numerical artefact. The form
  x²e⁻ˣ/(1 − e⁻ˣ)² loses about 1e-10 to cancellation at x = 1e-6 and printed a grid maximum of 1 + 9e-11. The analytic
  identity (y/sinh y)² and its limit passed in that same run. The fix computes the stable form; the gate was not changed.
- **Sources.** No web page or paper was read in this lane; every external number is quoted from committed repo files.

## Files
- `FROZEN_CRITERIA.md` (199ba297e).
- `ag6a.py`.
- `ag6a.out`, `ag6a_results.json`.
- `ag6a_MUTATE.out`, `ag6a_results_MUTATE.json`.
- `ag6a_firstrun_B3a_numerics.out`.
- This README. Nothing beyond the criteria is committed by this lane.

κ = ½ FITTED; not theory closed.
