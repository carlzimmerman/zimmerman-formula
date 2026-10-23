# Q6_v3_class FROZEN CRITERIA (2026-10-23): v3's own linear CMB and P(k) from a Khronon variant of C7's patched CLASS

Written and committed alone, before any script or number of this lane. Rules: `rebuild_2026_10_22/BRIEF.md`,
`covariant_push_2026_10_22/BRIEF.md`, `doors_push_2026_10_22/BRIEF.md`, `BRIEF_E_AUDIT.md`. κ = ½ FITTED. Footings
9.3603e-11 / 1.1312e-10 m/s², never pooled (neither enters: see D0). No dark-matter particle: the cold sector is the
Blanchet–Skordis K(Q) dust ("cold energy"). Never "theory closed". Never "the data favour the framework".
**Compute:** CFG960 (1024³) is running and is not touched. Every process: `OMP_NUM_THREADS=1 nice -n 19`, one thread,
< 1 GB RSS; CLASS runs strictly one at a time; builds `make -j1`. No downloads.

## 0. The question

v3 (`covariant_push_2026_10_22/THEORY_V3_DRAFT.md` §1) is the Blanchet–Skordis Khronon in literal form: metric g,
khronon τ, J = J_x (μ = x/(1+x) static limit), BS K(Q) dust with mass μ_K, plus γ_L. F3 found, with a Jeans-swindle /
sub-horizon ODE (not a Boltzmann code), that J_x′(0) = −1 removes the linear Newtonian term on FRW and that linear σ₈ is
0.03–0.32 at BS's cap μ_K ≤ 14.8 h/Mpc. This lane (1) derives v3's linear perturbation equations on FRW from the action,
(2) builds a Khronon variant of C7's patched CLASS by swapping C7's two isolated functions, validates it, (3) computes
v3's native TT/TE/EE/φφ, P(k), σ₈, S₈ on a μ_K grid and fits them to plik-lite + low-ℓ, and (4) compares with F3.

**Stated before any number (an analytic reading of records already committed, not a result of this lane):** C4 K7 gives
the quadratic-K background Q̄ − 1 = ε ≡ I₀/(2μ_K²a³), 8πGρ̄_K = I₀/a³ + I₀²/(4μ_K²a⁶), w = ε/(2+ε). The a⁻⁶ ("stiff")
partner is the one `fable_independent_2026/L137_aest_dust_stiff_correction.out` found BBN-fatal for AeST's quadratic K,
and C4 README L111 says the quadratic K is stiff early. At μ_K in this lane's grid the stiff term may exceed radiation
before recombination or BBN; CLASS refuses to start unless Ω_r(a_ini) is within 1e-4 of 1 (`background.c` L2302).
The lane therefore defines two models (§3) and scores the literal background separately (step B).

## 1. External inputs (cited)

- **BS24** = arXiv:2404.06584 (JCAP 11 (2024) 040): action S = (1/16πG)∫√−g[R − 2J(Y) + 2K(Q)] + S_m (Eq. 6),
  Q = √(−g^{μν}∂_μτ∂_ντ), n_μ = −∂_μτ/Q, A_μ = n^ν∇_νn_μ, Y = A·A (Eqs. 1–5, c = 1), K = μ²(Q−1)² (Eq. 7), cap
  μ⁻¹ ≫ 100 kpc (Eq. 39). **Not on disk**: transcribed by C4 via WebFetch (PROVISIONAL), self-consistency checked in
  C4 K1/K7 and BSK1. This lane re-derives everything it uses from the quoted action and does not use any BS24 equation
  beyond Eqs. 1–7 and 39. If a step would need BS24's text (e.g. BS's own FRW perturbation equations), the README says so.
- **J_x** = Λ − 2a₀²[y − ln(1+y)], y = √Y/a₀ (C4 K2: 1 + J_x′ = y/(1+y), J_x′(0) = −1).
- **C7** (`covariant_push_2026_10_22/C7_aest_class/`): `aest.patch`, `c7_make_patch.py` (the two isolated functions
  `background_aest_K()` and `perturbations_aest_rhs()`), `PROVENANCE.md` (pristine CLASS v3.3.4 under
  `../_external_data/class_public_v3.3.4_2026_10_22/`), validation thresholds, C2 likelihood loader and Gauss–Newton
  fitter (`c7_native.py`), ΛCDM refit (χ² 1003.48).
- **C2** (`covariant_push_2026_10_22/C2_aest_cosmology/c2b_native_cmb.py`): numpy plik-lite TTTEEE + low-ℓ TT + low-ℓ EE,
  executed read-only (the block between its "likelihoods" and "CLASS emulation" markers), τ prior.
- **F3** (`rebuild_2026_10_22/F3_growth_audit/`): K4 sub-horizon two-fluid ODE (`growth_ratio`, BSK2 kernel
  s = a²μ²/(k² + a²μ²), Jeans kernel 1 − k²/(a²μ²)), its numbers at μ_K = 14.80 h/Mpc on background A (BSK2 0.391 /
  0.203 at a_i = 1e-3 / 1e-4; Jeans 0.121 / 0.036), μ_min 361–2542 h/Mpc.
- **L1_khronon_pm FROZEN_CRITERIA §1** (parallel lane, read only): BS24's PN system as transcribed in BSK1
  (hold equation, Ξ, khronon Euler force −∇(Φ − Ξ)); used only as a cross-reference for check D5.

## 2. Assumption ledger (classes: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / ΛCDM-PROCESSED / STANDARD-MOND-MACHINERY / POSITED)

| ingredient | this lane's choice | class | source |
|---|---|---|---|
| action | BS24 Eq. 6 with J = J_x, K = μ_K²(Q−1)² | FRAMEWORK-NATIVE (v3's parent; J_x POSTULATED, outside BS's class); BS24 text PROVISIONAL (WebFetch) | C4, THEORY_V3 §1 |
| J at linear order | only J(0) = Λ and j₁ ≡ J′(0) enter the second-order action (Y = O(ε²) on FRW); v3: j₁ = −1; control j₁ = 0 | DERIVED (D0) | C4 K2 |
| a₀ | enters J_x first at O(Y^{3/2}): **absent at linear order** on FRW | DERIVED (D0) | C4 K2 |
| γ_L stiffness | not in the patch. At γ_L = 0 the covector P is the Legendre dual of J (C4 K3), so its linear effect is already the j₁ term; γ_L adds corrections of relative order (kL★)² ≤ (10 Mpc⁻¹ × 90 pc)² ≈ 8e-7 at the largest k used (an estimate, stated); P̄ = 0 on FRW | FRAMEWORK-NATIVE, neglected at linear order (POSITED reading, stated) | C4 K3/§5, I1 |
| J(0) = Λ | moved to CLASS's Ω_Λ (a constant in the Lagrangian has δT = 0) | DERIVED | C7 P-Λ |
| G_cosmo/G_N | 1 (Y ≡ 0 on FRW, so J does not touch the Friedmann equation; G_N = G in the strong-field regime where J′ → 0) | DERIVED (D1) | C4 K7 |
| μ_K | grid fixed in physical units (constant of the action): {14.8, 50, 150, 361, 1000, 2542} h/Mpc × h_ref, h_ref = 0.67552 (C7 ΛCDM refit) ⇒ {9.998, 33.78, 101.3, 243.9, 675.5, 1717} Mpc⁻¹; 14.8 h/Mpc = BS24 Eq. 39 edge (μ⁻¹ = 100 kpc), 361 / 2542 = F3's μ_min | EXTERNAL premise (BS24 Eq. 39) + F3 numbers; not fitted | F3 K4/K5 |
| dust abundance ω_K (I₀) | fitted with the six standard parameters | FITTED (initial condition) | C2, C4 K7 |
| A_s, n_s, ω_b, θ_s, τ_reio | fitted; start at C7's ΛCDM refit | FRAMEWORK-NATIVE form (GR + dust limit, C7 V1) with values from plik-lite | C7 |
| neutrinos | massless, N_ur = 3.044 | standard (as C7 P-ν) | — |
| BBN He table, recombination (CLASS defaults) | standard nuclear/atomic physics as coded in CLASS | external standard physics (as C7) | — |
| plik-lite + low-ℓ TT/EE (C2 numpy) | data | SURVEY-CALIBRATION (Planck-reduced bandpowers; plik-lite's foreground marginalisation was done on ΛCDM-like spectra: ΛCDM-PROCESSED to that extent) | C2 |
| τ prior | C2's low-ℓ scan | SURVEY-CALIBRATION | C2 |
| CDM species | ω_cdm = 1e-8, inert (fixes CLASS's synchronous gauge) | numerical (C7 P-CDM) | C7 |
| comparison model | ΛCDM refit with the pristine binary, same likelihood, optimiser and precision | same-pipeline control | C7 |
| F3's ODE (comparison only) | sub-horizon, baryons Newtonian from a_i, GR dust background | POSITED start (F3's) | F3 |
| STANDARD-MOND-MACHINERY | none (no QUMOND, no EFE recipe, no a₀) | — | — |

## 3. Models

- **LIT (literal v3):** quadratic K exactly, Q̄ = 1 + I₀/(2μ_K²a³), j₁ = −1. Background and perturbations exact in ε.
- **LO (v3 at leading order in ε = Q̄ − 1):** the literal equations expanded to leading order in ε in every coefficient
  (background exactly dust, ρ̄_K = I₀/(8πGa³); perturbations keep K″ = 2μ_K² and j₁ = −1). This is the regime in which
  BS24 use their K (Q − 1 ≪ 1) and the model F3/BSK2/L1 analysed. LO equals LIT wherever ε ≪ 1 (late times); where
  ε ≳ 1 (early times at small μ_K) LO is **not** the literal theory, and the README says so for every LO number.
  LO is POSTULATED as a reading (no new constant): it drops the a⁻⁶ background term and all O(ε) corrections.
- **DUST:** exact dust limit K″ → ∞ (μ_K → ∞ at fixed I₀), any j₁; the CDM control.
- Implementation: `aest_K_type` 0 = DUST, 3 = LIT, 4 = LO; `aest_K2` = μ_K² (Mpc⁻²); `aest_Q0` = 1 (Q is dimensionless
  in the Khronon); `aest_lambda_c` carries j₁ = J′(0) (the C7 parameter is unused by the Khronon and is re-labelled in
  the swapped functions; default 0); `aest_K_B` = 1 and `aest_g` = 1 (unused / derived g = 1). This keeps every edit
  inside the two swapped functions.

## 4. Step D: derivation (sympy, `q6_derive.py`; one line per check; exit 0 iff all pass)

Setup as C7: conformal time, perturbations depend on (η, x); metric h₀₀, h₀ₓ, hₓₓ, h_yy = h_zz; khronon
τ = τ̄(η) + ε·ϑ(η, x), τ̄′ = aQ̄. Extra-sector Lagrangian √−g[−2j₁Y + 2K(Q)] to second order in ε; Euler–Lagrange
equations; T^{μν} from the metric variations; CLASS variables δ, θ, δp, σ.

- **D0** Y⁽⁰⁾ = Y⁽¹⁾ = 0 on FRW, so the second-order action contains J only through J(0), J′(0); and the series of J_x
  about Y = 0 has a₀ first at Y^{3/2}. PASS = both exact. (This is the statement "a₀ absent at linear order".)
- **D1** background: 8πGρ̄ = Q̄K′ − K, 8πGp̄ = K, (a³K′)′ = 0 from the τ equation; no J contribution. PASS = residuals 0.
- **D2** structure: the sector's anisotropic stress σ (PASS = 0, or its form is exported and the patch must source it;
  if nonzero this is an AMENDMENT before any build); compact gauge-general forms of δρ, (ρ+p)θ, δp in terms of
  gauge-invariant combinations (exact). The khronon congruence's acceleration potential Ξ = Ψ − π′ − ℋπ (π = ϑ/τ̄′,
  Ψ = h₀₀/2) is checked to be gauge-invariant and to equal A_x/∂ₓ at linear order.
- **D3** gauge map: the synchronous system plus the standard fluid map (δ_N = δ_S − 3ℋ(1+w)α_C, θ_N = θ_S + k²α_C)
  equals the Newtonian system exactly (sympy residual 0), for LIT (general K) and for LO.
- **D4** conservation: ∇_μT^{μν} = 0 at linear order on the shell of the τ equation, both gauges (residual 0).
- **D5** quasi-static sub-horizon limit (link to F3/BSK2/L1): in Newtonian gauge, k ≫ ℋ, time derivatives of Ξ
  neglected against k²Ξ, LO: the khronon's net self-force kernel equals BSK2's s = a²μ_K²/(k² + a²μ_K²) for j₁ = −1 and
  the Jeans kernel 1 − k²/(a²μ_K²) for j₁ = 0. PASS = both exact.
- **D6** dust limit: K″ → ∞ at fixed I₀ gives CDM's equations exactly (δp = 0, σ = 0, θ′ = −ℋθ + metric), for j₁ = 0 and
  j₁ = −1. PASS = exact.
- **D7** Minkowski (a = 1, Q̄ = 1, K′ = K = 0): the τ mode has ω = 0 at linear order (BS24's "non-propagating" mode).
  PASS = exact. (A consistency check of the transcription.)
- **IC1–IC3** adiabatic initial conditions, synchronous gauge, radiation era, leading order in kτ (as C7): IC1 the series
  solves the LO system with residual at least one order above each equation's leading term; IC2 DUST gives CDM's IC;
  IC3 the Newtonian IC from the D3 map solves the Newtonian LO system at the same order. **IC_C7:** C7's IC block
  (already in the patch, not edited) applied with the LO background (w = c_a² = 0 there) satisfies IC1's criterion for
  the LO system. If IC_C7 fails, the IC block must be edited too (an AMENDMENT, stated as an edit outside the two
  functions).
- **MUTATE** (`Q6_MUTATE=1`, outputs `*_MUTATE.*`): the exported LO δp/ρ uses j₁ → −j₁ inside the J term; D5 must FAIL.

The implementation evolves the khronon sector's total (δ, θ) in C7's slots 0, 1 with the exact fluid equations and the
derived δp/ρ (and σ if D2 requires it); C7's slots 2, 3 are used only if D2 shows (δ, θ) do not determine δp, in which
case they carry gauge-invariant auxiliaries (AMENDMENT before any build). LIT uses the exact (general-K) system, LO the
LO system, DUST the CDM limit.

## 5. Step P: the patch (`q6_make_patch.py` → `khronon.patch`)

Pristine CLASS v3.3.4 copy + C7's `aest.patch` (applied with `patch -p1`, must apply cleanly) + **only the bodies of
`background_aest_K()` and `perturbations_aest_rhs()` replaced** (exact-anchor edits, each matching once). The diff
pristine → Khronon tree is written to `khronon.patch`; a MUTATE tree (`--mutate`: the sign of the metric-source term
θ + metric_continuity in the khronon δ′, as C7's V4) gives `khronon_MUTATE.patch`. Builds under
`../_external_data/class_khronon_build_2026_10_23/` (`class_khronon/`, `class_khronon_mutate/`), `make -j1 class`.
C7's `class_vanilla/class` is the pristine reference binary (its tree equals pristine: re-checked by the validator).

## 6. Step V: validation (`q6_validate.py`; thresholds are C7's)

Spectra: lensed TT, TE, EE, φφ for 2 ≤ ℓ ≤ 2500; linear P(k, z = 0) for 1e-4 ≤ k ≤ 1 Mpc⁻¹. Relative difference
|ΔX/X|; TE: |ΔTE|/√(TT·EE). Planck-2018-like parameters as C7's V1.

- **V0** patched code, sector off, vs pristine: bit-identical (extra check, not frozen in C7 either).
- **V1 dust limit (the task's (a)):** DUST with j₁ = 0 (μ_K → ∞ with J′(0) → 0), ω_K = ω_c − 1e-8, ω_cdm = 1e-8, vs pristine
  ω_cdm = ω_c, `tol_perturbations_integration = 1e-7`, in **both** gauges: every spectrum ≤ 1e-4; 100θ_s and r_drag
  ≤ 1e-6. Reported beside it (not gated): DUST with j₁ = −1; LO at μ_K = 1e6 h/Mpc with j₁ = 0 and j₁ = −1.
- **V2 convergence:** LO, μ_K = 361 h/Mpc, j₁ = −1: default vs C7's high precision; PASS ≤ max(2e-3, 2 × vanilla's change).
- **V3 gauge consistency (the task's (b)):** synchronous vs Newtonian, TT/TE/EE/φφ and P(k): LO at μ_K = 361 and at
  14.8 h/Mpc, j₁ = −1; PASS ≤ max(1e-3, 3 × vanilla's own gauge difference) for C_ℓ, and the same rule for P(k).
- **V5 IC attractor:** LO μ_K = 361, start times × 0.5: change ≤ vanilla's change + 1e-4.
- **V4 MUTATE (the task's (c)):** `Q6_MUTATE=1` uses the MUTATE binary; it must break V1 (or V3); `*_MUTATE.*`.
- **"Native prediction ready"** iff V1, V2, V3, V5 pass and MUTATE breaks V1 or V3.

## 7. Step B: the literal background (`q6_native.py`, before any spectrum)

For LIT at each grid μ_K, with I₀ from ω_K = 0.12063 (C7 ΛCDM refit ω_dm) and h = 0.67552, Ω_r with N_eff = 3.044:
z_stiff (ε = 1, i.e. w = 1/3); the redshift where the a⁻⁶ term equals radiation; ρ_K/ρ_r and the radiation-equivalent
ΔN_eff,equiv = ρ_K/ρ_{1ν} at T = 1 MeV and T = 0.07 MeV; ε and ρ_stiff/ρ_dust at recombination (z = 1090);
μ_K,BBN = the smallest μ_K with ΔN_eff,equiv(T = 1 MeV) ≤ 0.5 (a conservative BBN-era line, external); and whether the
Khronon CLASS binary starts a LIT run at the ΛCDM-refit parameters (its own radiation-domination test).
- **Reading (frozen):** LIT is **"NO RADIATION ERA (BBN-EXCLUDED)"** at a grid μ_K if ΔN_eff,equiv(1 MeV) > 0.5, and
  **"VIABLE BACKGROUND"** otherwise. If CLASS refuses a LIT run, no LIT spectrum exists at that μ_K and the step-N
  spectra are LO only.

## 8. Step N: native spectra and fits (`q6_native.py`; only if "native prediction ready")

- Runs (C7 A2 high precision, P_k_max = 10 h/Mpc, lensed C_ℓ to ℓ = 2508): pristine ΛCDM and DUST at C7's ΛCDM refit
  parameters; LO (j₁ = −1) at every grid μ_K at the same parameters (ω_K = ω_dm). LIT attempted at every grid μ_K (step B).
- Reported per run: χ² parts (C2 likelihood, A_planck = C7's), σ₈, S₈ = σ₈(Ω_m/0.3)^½, H₀, P/P_DUST at k = 0.1, 0.3, 1,
  3, 10 h/Mpc, max |ΔC_ℓ/C_ℓ| vs DUST, and **R_B(μ_K) = σ₈(LO, μ_K)/σ₈(DUST)**.
- Fits: C7's Gauss–Newton (A3: plik-lite residuals + A_planck prior + τ prior, 4 iterations, halving line search),
  start at C7's ΛCDM refit, ≤ 150 CLASS runs per model; free ω_b, ω_K (FITTED), 100θ_s, ln10¹⁰A_s, n_s, τ, A_planck.
  ΛCDM refit with the pristine binary the same way. Models fitted: LO at every grid μ_K. Reported: Δχ² vs the ΛCDM
  refit, H₀, σ₈, Ω_m, S₈. **Numbers only, no χ² verdict.**
- A model is RUNAWAY (C7 A4 rule) if at the fixed parameters its χ² is non-finite or max P/P_DUST > 10 over the tabulated
  k; RUNAWAY models are reported, not fitted.

## 9. Step C: comparison with F3 (the task's question 4)

- **K0 (reproduce first):** this lane's copy of F3's `growth_ratio` reproduces F3 K4 at μ_K = 14.79771 h/Mpc on
  background A (BSK2 0.39080 / 0.20313 at a_i = 1e-3 / 1e-4) to ≤ 1e-3 relative; and the pristine binary at C7's ΛCDM
  refit gives χ² within 2 of 1003.48.
- R_F3(μ_K) at this lane's fixed parameters (BSK2 kernel, a_i = 1e-3 and 1e-4) on the grid, beside R_B(μ_K).
- **Reading at the BS cap (μ_K = 14.8 h/Mpc), frozen:**
  - **CONFIRMED** if R_B ≤ R_F3(a_i = 1e-3) (the Boltzmann suppression is at least F3's optimistic one);
  - **CONFIRMED, WEAKER** if R_F3(a_i = 1e-3) < R_B < 0.95;
  - **NOT CONFIRMED** if R_B ≥ 0.95.
- μ_min,B: the μ_K at which R_B = 0.95, by log-log interpolation on the grid (if bracketed; else "beyond the grid"),
  beside F3's 361–2542 h/Mpc and BS's cap 14.8 h/Mpc.
- The reading is about LO (F3's model). The literal theory's status is step B's reading. Both appear in the README.

## 10. Files, rules, verdict word

Scripts `q6_derive.py`, `q6_make_patch.py`, `q6_validate.py`, `q6_native.py`, each writing `<name>.out`,
`<name>_results.json` and `*_MUTATE.*` under `Q6_MUTATE=1`; each prints `K… PASS/FAIL value threshold` lines and ends
`<NAME> COMPLETE: N/M checks PASS.` (exit 0 iff all pass). README verdict first (one of CRISP FINDING, RUNNABLE NOW,
DATA-GATED, SCOPED NO-GO, NOTHING NEW). CLASS source is not committed (only `khronon.patch`, scripts, outputs). Commit
only this lane's paths; never push. Any change to this file is an append-only AMENDMENT marked pre- or post-result.

## AMENDMENT A1 (PRE-RESULT, 2026-10-23; written after a 0.3 s sympy prototype of the kinematics in the scratchpad that printed only A_μ⁽⁰⁾ = 0 and the symbolic form of A_x⁽¹⁾ = ∂ₓ(Ψ − π′ − ℋπ), and before any script of this lane, any check line or any number)

1. **LO, precisely.** LO is the fluid with background w = 0, c_a² = 0 (ρ̄_K = I₀/(8πGa³)) and δp/ρ̄ = c²_{s,LO}·δ_rest,
   δ_rest = δ + 3ℋθ/k² (gauge-invariant when w = 0), where c²_{s,LO} is the leading-order-in-ε value of the rest-frame
   sound speed that D2 derives (with K″ = 2μ_K², Q̄ → 1). The exact fluid conservation equations are used, including
   the −3ℋ δp/ρ̄ term of the continuity equation (it is O(ε) without a k² factor; it is kept so that LO conserves its own
   T^{μν} exactly and is exactly gauge-covariant). D3 and D4 are checked for LO as well as for the exact system.
2. **IC_C7, precisely.** If the series solution of the LO system has θ's leading coefficient proportional to I₀ (the
   khronon charge, i.e. O(ωτ) in CLASS's radiation-era expansion, where CDM has θ = 0 exactly), then C7's IC block
   (θ = 0, δ = ¾δ_γ when w = c_a² = 0) is correct at zeroth order in ωτ. **IC_C7 PASS** iff C7's δ equals the series'
   leading δ exactly AND the series' leading θ vanishes as I₀ → 0. The O(ωτ_ini) remainder is then tested numerically by
   V5 (start × 0.5), at C7's threshold; if V5 fails, the IC block is edited (a further amendment).
3. **Slots 2, 3.** If D2 shows δp is fixed by (δ, θ) alone, C7's slots 2, 3 (E, χ) are dormant: their IC from C7's block
   is ∝ c_a² (zero for LO and DUST) and the swapped function sets their derivatives to 0.
4. **V1c with j₁ = 0 (reported, not gated):** at j₁ = 0 the LO rest-frame sound speed is K′/K″ = I₀/(2μ_K²a³), which exceeds
   1 at early times for any finite μ_K (LO is not the literal theory there). That run is attempted with a 600 s limit and
   reported as it ends (completed / failed / timed out).

## AMENDMENT A2 (POST-RESULT for step D's derivation lines, PRE-RESULT for everything else: written after `q6_derive.py` printed D0–D9 PASS and its LO initial-condition series failed to solve; before any CLASS build, spectrum, χ² or validation number)

What step D showed: the v3 khronon sector is exactly a fluid (no shear) whose rest-frame sound speed is
c_s² = Q̄K′/(Q̄²K″ − 2j₁k²/a²) (D2_fluid). The frozen LO uses its Q̄ → 1 value c²_{s,LO} = K′/(K″ − 2j₁k²/a²), which for
j₁ = −1 is bounded by K′/K″ = ε = I₀/(2μ_K²a³) and so **exceeds 1 wherever ε > 1** — at CLASS's initial times for every grid
μ_K (ε ≫ 1 there). With X = δ_rest the fluid equations give X′ = −θ − h′/2 + 3(ℋ′ − ℋ²)θ/k² (independent of c_s²) and
θ′ = −ℋθ + k²c_s²X, i.e. a super-horizon mode of frequency ω² = 3(ℋ² − ℋ′)c_s² (6c_s²ℋ² in radiation), ≫ ℋ² when c_s² ≫ 1:
the frozen LO has a superluminal, stiff mode exactly where it is not the literal theory, and its regular solution is not
a power series in τ (why the IC series failed). Changes, fixed now:

1. **Frozen LO is not run** (its derivation checks D3, D4_LO, D5, D8 stay). The run model replacing it is **LOB**:
   background exactly dust (w = c_a² = 0, ρ̄_K = I₀/(8πGa³); the a⁻⁶ partner and all O(ε) background terms dropped, as
   F3's background), perturbations with the **literal** rest-frame sound speed c_s² = Q̄K′/(Q̄²K″ − 2j₁k²/a²) with the
   exact quadratic-K Q̄ = 1 + I₀/(2μ_K²a³) and K″ = 2μ_K². It is the fluid {w = 0, c_s²(k, τ)} with exact conservation
   (gauge-covariant by the D4_LO argument, which holds for any c_s²); c_s² ≤ ε/(1+ε) < 1 (subluminal, no stiff mode);
   LOB = LO to O(ε) where ε ≪ 1 (D8). LOB is "literal v3's perturbations on F3's dust background"; its only departure
   from LIT is the dropped O(ε) background, which step B scores separately. Implementation: `aest_K_type` 4 = LOB.
   Every "LO" in §§6, 8, 9 (validation runs, native runs, fits, the step-C reading) reads "LOB".
2. **IC edit outside the two functions (the §4 fallback).** C7's IC lines assume c_s² = c_a² = w (true for AeST's
   k-essence, false here). The khronon IC is replaced by CLASS's own fluid formula (1004.5509, as for `fld`) with w from
   the background and c_s² = c_s²(k, τ_ini) obtained from the swapped `perturbations_aest_rhs()` (its δp/ρ at δ = 1, θ = 0):
   δ = ¾δ_γ(1+w)(4 − 3c_s²)/(4 − 6w + 3c_s²), θ = −k(kτ)³c_s²/(4(4 − 6w + 3c_s²))·curvature_ini·s2², E = χ = 0. This one block
   and the two functions are the only differences from `aest.patch`.
3. **Step-D IC checks re-pointed:** IC1 (the constant-c_s² w = 0 series solves the LOB system), IC2 (c_s² = 0 gives CDM's IC),
   IC3 (Newtonian IC via the D3 map), IC_fld (the coded formula equals the series). IC_C7 is printed as a reported line
   (it is expected to fail for c_s² ≠ 0; its failure is what triggers this fallback), not counted. Added D10: c_s² of LOB
   ≤ ε/(1+ε) < 1 and c²_{s,LO} → ε at k → 0 (exact), with the super-horizon frequency identity above.
4. Nothing else changes (thresholds, readings, grid, fits, MUTATE).

## AMENDMENT A3 (POST-RESULT: written after `q6_validate.py` ran in both modes and after scratch diagnostics; before any step-B, step-N or step-C number)

**What happened.** V_prov, V0, V1 (both gauges; DUST with j₁ = 0 and, reported, j₁ = −1, ≤ 4e-6) PASS; MUTATE breaks V1
and V3 as required. The frozen **V2, V3 (both μ_K) and V5 FAIL**, and the frozen "native prediction ready" flag is False.
These lines stay in the record. Scratch diagnostics (not scored; disclosed in the README):
- LOB's matter transfer function passes through a node at k ≈ 0.5–1 Mpc⁻¹ (P/P_ΛCDM down to 3.4e-6 at μ_K = 361 h/Mpc;
  to 1e-8 at 14.8 h/Mpc). V2's 45 % P(k) change comes from interpolating log P across the two precisions' different k
  grids through that node; on the **same** k grid default and high precision agree to ≤ 1.2e-3 for every k ≤ 1 Mpc⁻¹
  (≤ 1.1e-4 for k ≤ 0.5).
- V3's P(k) and φφ mismatches sit where the model's own spectrum is 1e-3 to 1e-8 of ΛCDM's (φφ: ℓ = 2500, φφ_LOB/φφ_ΛCDM =
  1.7e-6; in units of the ΛCDM spectrum the gauge gap is 2.3e-5). TT/TE/EE gauge gaps are ≤ 8.5e-5 (vanilla's own ≤ 8.1e-5).
- V5's TT change sits at ℓ ≈ 9–14, is identical at high precision, and shrinks ≈ 3.8× per halving of the start time
  (5.25e-4 for ×1 → ×0.5; 1.38e-4 for ×0.5 → ×0.25): an initial-condition truncation error ∝ τ_ini², converging.

**Supplementary gates (fixed now; the frozen ones are still printed):**
- **V2b** same-grid convergence: LOB, μ_K = 361 h/Mpc, j₁ = −1, default precision with `k_per_decade_for_pk = 20` vs C7's high
  precision (same k grid); metric |ΔX|/X_ΛCDM (X_ΛCDM = pristine ΛCDM at the same parameters and precision) for TT, TE
  (normalised by √(TT·EE)_ΛCDM), EE, φφ, P(k); PASS ≤ max(2e-3, 2 × vanilla's change).
- **V3b** gauge consistency in units of the ΛCDM spectrum: the frozen V3 pairs, metric |ΔX|/X_ΛCDM; PASS ≤ max(1e-3, 3 × vanilla).
- **V5b** attractor at the native start time: every step-N run (ΛCDM and Khronon alike) uses
  `start_small_k_at_tau_c_over_tau_h` and `start_large_k_at_tau_h_over_tau_k` × 0.25; V5b compares × 0.25 with × 0.125 for
  LOB 361 h/Mpc (relative C_ℓ, P(k) in units of ΛCDM); PASS ≤ vanilla's own change + 1e-4.
- MUTATE must break V1 or V3b. **"Native prediction ready (A3)"** iff V1, V2b, V3b, V5b pass and MUTATE breaks V1 or V3b.
  The README states that the frozen gates failed and that the native numbers rest on the A3 gates.
- Step N: C7's high precision (A2 of C7) plus the × 0.25 start, for ΛCDM and Khronon runs alike. Nothing else changes.
