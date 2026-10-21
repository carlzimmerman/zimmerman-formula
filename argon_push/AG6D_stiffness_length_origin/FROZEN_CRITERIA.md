# AG6D FROZEN CRITERIA: can the stiffness length L* be derived?

Committed alone, before any script exists and before any number is computed by code. Dated 2026-10-20.

## 0. The question and the fixed inputs
The action (PAPER49, DOI 10.5281/zenodo.23501949) carries the stiffness term (γ/2)|∇P|², with γ = K L*²/2 and K = 4πG.
P is the displacement of cold energy: ∂_t P = −j, so ∇·P = ρ_c − ρ̄_c (PAPER49 §1). L* is bounded, not derived:
- floor 24.0 pc canonical / 24.7 pc alt (CFG820, primary sample, 95%);
- ceiling "≳ 1 kpc" (CFG691 grid edge; CFG832 soft edge ~2 kpc).
- CFG821 (dSphs want ≤ 22 pc) is INCONSISTENT and conditional. It is reported, not used as a line.

**Frozen window.**
- Canonical: [24.0 pc, 1000 pc].
- Alt: [24.7 pc, 1000 pc].
- Sensitivity only: the ceiling moved to 2000 pc.

**Constants and inputs.**
- a0 = 9.3603e-11 (canonical) and 1.1312e-10 m/s² (alt). The footings are never pooled; a candidate must land on BOTH.
- CODATA G, c, ħ, m_e, m_p, k_B.
- Ω_c/Ω_b = 5.364.
- h = 0.677 (CFG689 native H0 67.70), Ω_m = 0.31, Ω_r h² = 4.15e-5 (photons plus 3.046 neutrinos, T_CMB 2.7255 K).
- MeV condensate mass m_h = 1 MeV, bracket 0.4–1.7 MeV (ARGON10).
- Record dwarf numbers, copied from the lane READMEs and cited:
  - CFG870: r_c = 104 pc, shape M ∝ r³/(r² + r_c²), ρ0 ≈ 0.58 M☉/pc³;
  - CFG871: UFD best r_c 133 / 139 pc;
  - CFG877 / CFG884: cap radius 237 / 205 pc;
  - CFG884 synthesis: Sextans MP needs ≳ 6e8 M☉ out to ≳ 1.7 kpc (provisional extraction, as flagged there).

κ = ½ is FITTED. No dark-matter particle species is added: the medium is the record's cold energy. Framework-native only;
no ΛCDM mass function or "within X% of ΛCDM" statement enters any verdict.

## 1. Design-stage disclosure (numerology guard)
While designing, I made rough mental estimates with a0 = 1.2e-10 (not a footing value). They are listed so that no later
"hit" is presented as a discovery. The scripts supersede them.
- c²/a0 · 2^−30 ≈ 23 pc.
- ℓ_P^{1/7}(c²/a0)^{6/7} ≈ 38 pc; the n = 8 member ≈ 480 pc.
- σ²/a0 at 10⁴ K neutral gas ≈ 18–24 pc.
- The dwarf core maps to L* ≈ 47–78 pc.
- Screening mass M_eq ∈ [2.5e5, 4.3e8] M☉.
- Cosmic cutoff k ~ 17 Mpc⁻¹ at L* = 24 pc.
- The MeV contact scattering length a_s ~ 4e4 m.
- The Bullet-type bound wants m ≲ 5 meV.

## 2. Part A: the exact identity (mechanism level). Script `ag6d_identity.py`
Claim to test: for longitudinal P (the only part any screening lane has used), the stiffness energy equals the internal
energy of a Γ = 2 (n = 1) polytrope of the cold medium, measured from the cosmic mean:
- e = (γ/2)(ρ_c − ρ̄_c)², so p = (γ/2)ρ_c² at ρ_c ≫ ρ̄_c;
- c_s² = γρ̄ = 2πG L*² ρ̄ (CFG744's c_P relation, recovered);
- the free-medium Jeans wavenumber k_J,phys = √2/L* is independent of density and epoch;
- a free, self-gravitating (Newtonian) clump has the mass-independent radius R_TF = π L*/√2.

| test | PASS line |
|---|---|
| A1 (sympy) | For P = p(r) r̂, the vector Laplacian's radial part equals ∇(∇·P): the residual simplifies to 0 exactly. For a toroidal control P = f(r) sinθ φ̂, ∇·P = 0 while the vector Laplacian is ≠ 0, so the identity is scoped to longitudinal P. |
| A2 (numeric) | For 3 compact-support radial profiles, \|E_grad − E_div\|/E_grad < 1e-6 (the difference is a boundary term). |
| A3 (uniqueness) | For e = Kρ^Γ, the perturbation stiffness γ_eff(ρ̄) = e″(ρ̄) is constant to < 1e-12 over ρ̄ ∈ [1e-30, 1e-18] kg/m³ only for Γ = 2. For Γ ∈ {4/3, 5/3, 3} it varies by > 1 dex. A cubic term (e‴ ≠ 0) breaks exactness at finite δρ. |
| A4 (Lane-Emden) | The n = 1 first zero equals π within 1e-6, and R_TF/L* = π/√2 within 1e-6. For n = 1.5, R ∝ M^−1/3 (slope within 1e-3). |

**MUTATE** (`AG6D_MUTATE=1`): use Γ = 5/3 in place of Γ = 2. The "constant L*" claim must FAIL (L*_eff varies with ρ̄),
and the script exits 1.

Verdict line: IDENTITY HOLDS (longitudinal) if A1–A4 all pass; otherwise IDENTITY FAILS.

## 3. Part B: candidate formulas (each declared before evaluation). Script `ag6d_candidates.py`
Each candidate is evaluated on both footings. Mechanism flags are declared here and are not changed after evaluation:
- F = forced identification of the |∇P|² coefficient;
- R = reading or analogy only;
- X = operator or regime mismatch.

| id | mechanism (flag) | formula for L* | inputs |
|---|---|---|---|
| B1 | {a0, G, c} dimensional theorem (R) | only length c²/a0 (G cannot enter a length without a mass) | a0, c |
| B2 | medium Jeans at the DE density, c_s = c (F via Part A) | c/√(2πGρ_DE) = κc²/(√(2π)a0) | a0, κ |
| B3a | independent light field: P-quantum Compton, √2ħ/(m_P c), m_P c² = ħa0/c (F as field mass) | √2 c²/a0 | a0 |
| B3b | same, m_P c² = ħH_∞ (H_∞ = H0√Ω_Λ, Ω_Λ = 1 − Ω_m) (F) | √2 c/H_∞ | H0 |
| B3c | same, m_P c² = DE scale (ρ_DE ħ³c⁵)^{1/4}, with ρ_DE = a0²/(κ²c²G) (F) | √2 ħc/(m_P c²) | a0, κ |
| B3d | same, m_P = m_h = 1 MeV (F) | √2 ħ/(m_h c) | m_h |
| B4 | BEC contact interaction with a_s = ħ/(m_h c) (F via Part A; Kp = 2πħ²a_s/m³) | √(2ħ³/(G m_h⁴ c)) | m_h |
| B5 | superfluid healing length ħ/(√2 m_h c_s), c_s = 20–220 m/s (CFG744) (X: quantum pressure is O(k⁴), coefficient ∝ 1/ρ) | ħ/(√2 m_h c_s) | m_h |
| B6a | screening-mass reading, L* = √2 r_M(M_x) = √(2GM_x/a0) (R); M_x = baryonic Jeans mass at decoupling, M_J = (4π/3)ρ_b(λ_J/2)³, λ_J = c_s√(π/(Gρ_m)), T = 3000 K, μ = 1.22, z = 1090 | √(2GM_J/a0) | Ω_b h², Ω_m h², T |
| B6b | same, M_x = σ⁴/(Ga0) (bare deep-MOND mass), σ² = k_B T/(μ m_p), T = 10⁴ K, μ = 1.22 (R) | √2 σ²/a0 | a0, T |
| B6c | same, M_x = CFG877 M_cl = 81σ⁴/(4Ga0), σ = 7.53 km/s (R, post hoc) | √(2GM_cl/a0) | a0, σ |
| B7 | isothermal scale height in the wall field, σ²/a0, at T = 10⁴ K, μ = 1.22 (R) | σ²/a0 | a0, T |
| B8 | Part A identity plus the dwarf core as R_TF (F + one post-hoc choice: free cold energy self-gravitates, the class-A hybrid) | (√2/π)·R, with R = 0.7316 r_c/0.60335 (half-central-density match, CFG870 shape vs sinc) | r_c = 104 pc |
| B9 | Part A plus the record's medium wave speed c_P (F) | c_P/√(2πGρ_c) | CIRCULAR: CFG744's c_P was computed from L*. Reported, not scored |
| B10 | size of the two-field MeV condensate compact object (R) | R ≈ 1e8 m (memory, 58674e952) | — |
| B11 | Planck–a0 family ℓ_P^α (c²/a0)^{1−α}, α = 1/n, n = 2..12 (R, numerology) | — | ħ, G, c, a0 |
| B12 | κ-power family κ^n c²/a0, n = 1..60 (R, numerology) | — | κ, a0 |

**Classification per candidate.**
- LAND: the value is inside the window on BOTH footings. MISS otherwise.
- DERIVATION needs all of: LAND; flag F; no post-hoc or fitted input (B6c and B8 are post hoc by construction); and a
  second prediction computed from the same mechanism, not already contradicted by the record.
- CANDIDATE needs LAND, flag F and exactly one post-hoc or free choice, with its second prediction not contradicted.
- NUMEROLOGY: LAND with flag R.
- SCOPED NO-GO: flag X, or flag F with MISS.

**Look-elsewhere menu (generic dimensional combinations).**
- Base lengths: S = {c²/a0, ℓ_P, λ_e, λ_p, λ_1MeV} (Compton lengths ħ/(mc)).
- Every unordered pair (i, j) mixed as ℓ_i^{1−α} ℓ_j^α, for every reduced fraction α = p/q in (0, 1) with q ≤ 8
  (21 values): 10 × 21 = 210 combinations per footing.
- Report N_land / 210 per footing, the landing fraction, and the expected number of chance landings.
- Also report the total count of every dimensionally valid formula evaluated in this lane: B1–B12 members plus the menu.
- Every formula passes through a dimension checker (M, L, T exponents). A dimensionally wrong formula is a script error.

**MUTATE** (`AG6D_MUTATE=1`): inject a dimensionally wrong formula (√(G a0)/c) into the candidate list. The checker must
reject it and the script exits 1. Planted control K-B1: the constant 100 pc must classify as LAND on both footings.

## 4. Part C1: second prediction, the free-medium Jeans cutoff. Script `ag6d_cutoff.py`
If the free medium carries the stiffness (PAPER49's action has no switch on the γ term), its linear growth is:
- δ_c'' + (2 + dlnH/dlna) δ_c' = (3/2) Ω_m(a) [f_c δ_c (1 − (L* k/a)²/2) + f_b δ_b], with ' = d/dln a and k comoving;
- baryons: δ_b = 0 for a < 1/1091, then pressureless with the same gravity term;
- H² = H0²(Ω_m a⁻³ + Ω_r a⁻⁴ + Ω_Λ);
- f_c = 5.364/6.364.

Each mode starts at horizon entry (k = aH/c) with δ_c = 1 and dδ_c/dlna = 1 (sensitivity: 0 and 2). The reference is the
same equation with L* = 0.
- T(k) = δ_m(L*)/δ_m(0) at a = 1/50 (the 1024³ runs start at z = 49).
- Grid: k ∈ [0.05, 200] Mpc⁻¹; L* ∈ {24, 50, 100, 300, 1000} pc.

**Reported.**
- k_1/2(L*), where T = 0.5.
- The half-mode mass M_1/2 = (4π/3) ρ̄_m (π/k_1/2)³.
- L*_IC: the largest L* with T(k_Ny) ≥ 0.9, where k_Ny = π·1024/200 = 16.08 h/Mpc (the 1024³ box, CFG654 `L = 200`),
  found by bisection on [1, 1000] pc.

**Class (conditional on the free medium carrying the stiffness; not scored on data).**
| L*_IC | class |
|---|---|
| ≥ 1000 pc | NO CONFLICT |
| 24 ≤ L*_IC < 1000 pc | NARROWS THE WINDOW to [24, L*_IC] |
| < 24 pc | CONFLICT: the identification plus the globular floor contradicts the CDM-like ICs of the 1024³ shear runs |

**Controls.**
- K1: T(0.05 Mpc⁻¹) within 1e-3 of 1 at L* = 24 pc.
- K2: with f_c = 1, Ω_Λ = 0, no baryons, the growing-mode initial data reproduce the Meszaros D = 1 + 3y/2 within 1e-5.
- MUTATE: γ = 0 (T ≡ 1) must change the class. The script prints it and exits 1 by design.

## 5. Part C2: second prediction, one universal clump radius. Script `ag6d_dwarf_link.py`
Under Part A, free self-bound cold energy (Newtonian self-gravity, the class-A hybrid) has one radius R_TF = πL*/√2 for every
mass. Its σ varies with mass, which is compatible with CFG880's non-universal σ.

**Implied L* values.**
- From CFG870's r_c, by the half-density mapping of B8.
- From CFG871's r_c (133 / 139 pc), by the same mapping.
- From CFG877's cap (237 / 205 pc), taken as R_TF.
- From CFG884 Sextans, taking R_TF ≥ 1.7 kpc, which gives a lower bound.

**Classes.**
- CONSISTENT: all implied L* lie in the window and max/min ≤ 2.
- INCONSISTENT: the Sextans lower bound exceeds the largest group value by more than ×2.
- Otherwise TENSION.

**Supply check (reported).** The TF clump mass M = 4R³ρ0/π at ρ0 = 0.58 M☉/pc³, compared with the catchment stock
53.64 M_b for M_b = 1e5–1e7 M☉.

**MUTATE:** set Sextans' required R equal to the CFG870-implied R. The class must become CONSISTENT; the script exits 1 by design.

## 6. Part D: microphysics scope, reported. In `ag6d_candidates.py`
- For a dilute condensate, Kp = 2πħ²a_s/m³ = πG L*², so a_s/m³ = G L*²/(2ħ²).
- On a mass grid 1e-22 eV – 10 MeV, report at L* = 24 and 1000 pc:
  - a_s;
  - diluteness n a_s³ at ρ = 1 M☉/pc³;
  - σ/m = 8πa_s²/m against 1 cm²/g (Bullet-type scale, PROVISIONAL literature value);
  - the TF condition ħ/(√2 m c_s) < 0.1 L* at ρ = 0.01 M☉/pc³.
- Report the allowed band, and whether 0.4–1.7 MeV is in it.
- True-BEC background (not the record's mean-subtracted form): the redshift where the interaction energy equals the rest
  energy, and ΔN_eff for a radiation-like completion. Reported only.

## 7. Overall verdict rule (frozen)
- **DERIVATION** if at least one candidate meets every DERIVATION condition on both footings.
- **CANDIDATE** otherwise, if at least one meets the CANDIDATE conditions and its second prediction is not contradicted
  (C2 for B8).
- **SCOPED NO-GO** otherwise, if every F/X candidate MISSes, has an operator mismatch, or fails its own second prediction.
  The scope is the pre-declared list only.
- **NOT DIAGNOSTIC** if any control (A1–A4, K-B1, K1, K2) fails.

## 8. Run discipline
- OMP_NUM_THREADS=1, nice -n 10, one process at a time, < 1 GB RSS (measured with /usr/bin/time -l), minutes.
- Start only if free + inactive ≥ 12 GB; a 1024³ run is live.
- No downloads. Web facts are PROVISIONAL.
- Outputs go to `*.out` and `*_results.json`; MUTATE writes `*_MUTATE.*`.
- Results are NOT committed. Never "breakthrough", never "theory closed".
