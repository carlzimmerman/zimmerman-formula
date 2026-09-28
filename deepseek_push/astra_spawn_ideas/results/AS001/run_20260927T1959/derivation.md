# AS001 — Mass-density versus energy-density normalization: derivation and audit

**Run:** `run_20260927T1959` · **Task:** deepseek_push/astra_spawn_ideas/AS001_mass_density_versus_energy_density_normalization.md (sha256 `9067b7b97049e3ab58421790e9dcce67bd561de5fd3eded8920ea230583bc751`) · **Worker:** deepseek/deepseek-v4-flash-0731 (OpenRouter), Hermes subagent · **Outcome:** `supports_scoped_claim`

---

## 1. The precise claim, symbol dictionary, assumptions and scope

**Claim under audit (framework base, README key equations; FRAMEWORK_CONTRACT, "Mandatory scale and units"):**

> The vacuum acceleration scale given by the mass-density normalization and the energy-density normalization are the *same function* of the vacuum density: for every ρ_L > 0,
>
> **a0(ρ_L) = κ·c·√(G·ρ_L) ≡ κ·√(G·ε_L),   ε_L := ρ_L·c²**
>
> — identically, with no approximation and no new fitted input introduced by the change of variable. Consequently every derived quantity that is a function of a0 — r_M = √(GM_b/a0), v_flat⁴ = G·M_b·a0 — takes numerically identical values through either representation.

**Symbol dictionary** (SI throughout):

| symbol | meaning | units | exponent vector (M, L, T) | status |
|---|---|---|---|---|
| κ (kappa) | normalization coefficient | dimensionless | (0,0,0) | **framework input, adopted** κ = 1/2 ("adopted unless this task supplies an independent derivation" — this task does not; the README's stand that nothing derives κ is consistent with this audit) |
| c | speed of light | m s⁻¹ | (0,1,−1) | fixed exact c = 299 792 458 m/s |
| G | Newton coupling | m³ kg⁻¹ s⁻² | (−1,3,−2) | measured input G = 6.67430e-11 (mandated default) |
| ρ_L | vacuum **mass** density | kg m⁻³ | (1,−3,0) | measured/derived input (from a0 via the audited relation below) |
| ε_L | vacuum **energy** density | J m⁻³ = kg m⁻¹ s⁻² | (1,−1,−2) | derived here: ε_L := ρ_L·c² |
| a0 | MOND acceleration scale | m s⁻² | (0,1,−2) | registered values on two footings (below) |
| M_b | baryonic mass | kg | (1,0,0) | measured input |
| r_M | MOND radius | m | (0,1,0) | derived |
| v_flat | deep flat rotation speed | m s⁻¹ | (0,1,−1) | derived |

**Registered scale footings, carried separately throughout** (mandated): canonical a0 = **9.3619e-11 m/s²** and alternative a0 = **1.1279e-10 m/s²**. Per contract, these cannot simultaneously share a fixed ρ_Lambda and a fixed κ. Here κ = 1/2 is adopted for **both** footings; they then carry **different** densities (Section 6). The alternative interpretation — ρ_Lambda held fixed, κ_eff = 0.60238840 — is an equivalent re-labeling, reported but not used as a third footing.

**Framework inputs vs. conclusions established here:** inputs — κ = 1/2 (adopted), G, c, the two registered a0 values; conclusions — (i) dimensional consistency of both normalizations, (ii) exact algebraic equivalence of the two representations, (iii) representation-invariance of r_M and v_flat⁴, (iv) the dimensionless footing-ratio identity, (v) the negative-control verdicts. Nothing here derives κ, fixes the physical value of ρ_Lambda, or identifies which physical density the vacuum is (all remain framework inputs; see Section 8).

**Boundary conditions / domain:** ρ_L ∈ (0, ∞) for the physical statement; the identity and all theorems hold on the closed domain ρ_L ≥ 0 (κ, c, G ≥ 0) — verified symbolically in Lean (Section 7). κ > 0 for the ratio theorem (division). No observational fit is performed and none is required.

---

## 2. Exponent vectors (M, L, T) and the reversible conversion table

Dimensional base vectors: G = (−1,3,−2), c = (0,1,−1), ρ_L = (1,−3,0), ε_L = (1,−1,−2), M_b = (1,0,0), κ = (0,0,0).

| expression | exponent vector | dimension | verdict |
|---|---|---|---|
| √(G·ρ_L) | (0,0,−2) → √ → (0,0,−1) | s⁻¹ (frequency) | not an acceleration today |
| **κ·c·√(G·ρ_L)** | (0,1,−1)+(0,0,−1) = **(0,1,−2)** | m s⁻² | ✓ acceleration |
| ε_L = ρ_L·c² | (1,−3,0)+(0,2,−2) = (1,−1,−2) | kg m⁻¹ s⁻² = J m⁻³ | ✓ energy density |
| G·ε_L | (−1,3,−2)+(1,−1,−2) = (0,2,−4) | m² s⁻⁴ | — |
| **κ·√(G·ε_L)** | (0,2,−4) → √ → **(0,1,−2)** | m s⁻² | ✓ acceleration |
| **r_M = √(G·M_b/a0)** | ((−1,3,−2)+(1,0,0)−(0,1,−2)) → √ = (0,1,0) | m | ✓ |
| **v_flat⁴ = G·M_b·a0** | (−1,3,−2)+(1,0,0)+(0,1,−2) = (0,4,−4) | m⁴ s⁻⁴ = (m s⁻¹)⁴ | ✓ |

**Reversible conversion table** (exact bijections; the framework's vacuum term in either convention):

| from | to | rule |
|---|---|---|
| ρ_L (kg m⁻³) | ε_L (J m⁻³) | ε_L = ρ_L·c² (exact; c is defined exactly) |
| ε_L (J m⁻³) | ρ_L (kg m⁻³) | ρ_L = ε_L/c² (exact) |
| a0(mass form) | a0(energy form) | a0 = κ·c·√(G·ρ_L) = κ·√(G·(ρ_L·c²)) (exact identity, Section 3) |
| a0 | ρ_L | ρ_L = 4·a0²/(G·c²) at κ = 1/2 (framework identity, verified numerically to 1e-61) |
| a0 | Λ | Λ = 32π·a0²/c⁴ m⁻² (context; not re-derived here) |

**Where exactly does c disappear?** In the mass-density form c appears as an explicit prefactor. In the energy-density form the density carries c² (ε_L = ρ_L·c²) and √ extracts exactly one power of c: √(G·ε_L) = √(G·ρ_L·c²) = c·√(G·ρ_L). The one explicit c of the mass form IS the one implicit power of c extracted from the re-scaled density in the energy form. Nothing is lost or gained — the disappearances are exact bookkeeping of the units bijection, not physics.

---

## 3. The algebra (all steps, scales, signs, units)

Let ρ_L > 0, κ ≥ 0, c ≥ 0, G ≥ 0. Since c² ≥ 0 and G·ρ_L ≥ 0:

```text
κ·c·√(G·ρ_L)
  = κ·√(c²)·√(G·ρ_L)                 [c = √(c²) for c ≥ 0]
  = κ·√(c²·G·ρ_L)                     [√(x)·√(y) = √(x·y) for x,y ≥ 0]
  = κ·√(G·(ρ_L·c²))                   [commutativity of reals]
  = κ·√(G·ε_L)                        [definition ε_L := ρ_L·c², in J/m³]
```

Every factor: κ (dimensionless, adopted 1/2), c (s⁻¹→m s⁻¹ prefactor chain), G (m³ kg⁻¹ s⁻²), ρ_L (kg m⁻³), ε_L (kg m⁻¹ s⁻²). All factors positive in the physical domain, so no sign branch arises; at ρ_L = 0 the identity holds with both sides zero.

**Leading neglected term and limiting regime:** none — this is an **exact algebraic identity** for all ρ_L ≥ 0, not an asymptotic statement. There is no approximation error. The only finite-numerics error is the decimal representation of the registered a0 values themselves (5 significant digits on both footings), which sets the implied ρ_L values to ~10 significant digits; the identity itself holds at the symbol level (Lean-certified, Section 7) and at 60-digit precision to ~1e-61 relative (Section 4).

**Derived consequences (exact functions of a0):**

```text
r_M        = √(G·M_b/a0)          -> identical through either a0 representation
v_flat⁴    = G·M_b·a0             -> identical through either a0 representation
v_flat/…   = (G·M_b·a0)^(1/4)     = √(√(G·M_b·a0))  (fourth root, nonneg domain)
```

**Footing ratio (dimensionless, applies to both footings):** for fixed κ, c, G and two positive densities,

```text
a0(ρ₂)/a0(ρ₁) = [κ·c·√(G·ρ₂)]/[κ·c·√(G·ρ₁)] = √(ρ₂/ρ₁)
```

so the ratio of the two registered a0 values is pure density-ratio: (a0_alt/a0_can)² = ρ_total/ρ_Lambda (verified to 2.1e-61, Section 4). This is how the single dimensionless theorem applies to both footings: it is κ-, c-, G-independent, and the footings enter only through their density pair.

---

## 4. Independent check: different representation, bounded high-precision computation

`compute_AS001_dimensional_audit.py` (mpmath, **60 digits**, single thread, CPU-capped at 120 s by `ulimit -t 120`; actual wall 0.0006 s, memory trivial) evaluates every quantity **twice**: once through the mass-density form, once through the energy-density form, from independently written expressions. Actual residuals (relative):

| check | canonical | alternative |
|---|---|---|
| a0 reconstructed (mass form) | 9.3619000000e-11 | 1.1279000000e-10 |
| a0 reconstructed (energy form) | 9.3619000000e-11 | 1.1279000000e-10 |
| rel resid mass-form vs registered | 9.6729e-62 | 8.0288e-62 |
| rel resid energy-form vs registered | 0.0 | 0.0 |
| **rel resid mass − energy** | **9.6729e-62** | **8.0288e-62** |
| implied ρ (kg m⁻³) | 5.844412454e-27 | 8.483089620e-27 |
| implied ε (J m⁻³) | 5.252695960e-10 | 7.624220727e-10 |
| identity over grid ρ ∈ [1e-33, 1e-12] kg/m³ | worst 1.4966e-61 (at ρ = 1e-23) | — |
| boundary ρ → 0 | 0.0 / 0.0 | 0.0 / 0.0 |

Prediction invariance (M_b = M_sun = 1.98847e30 kg):

| derived quantity | canonical | alternative |
|---|---|---|
| r_M (both forms, m) | 1.190639769e15 | 1.084743572e15 — rel resid ≤ 8.074e-62 |
| v_flat (both forms, m/s) | 333.866 | 349.783 — rel resid ≤ 1.193e-61 |
| v_flat⁴ − G·M_b·a0 (m⁴ s⁻⁴) | −1.34e-51 (60-digit zero) | +2.67e-51 (60-digit zero) |

These are residuals of a finite-precision evaluation of an exact identity — they are the actual saved values (`residuals.json`), not booleans. Tolerances were set **before** evaluation: 1e-30 relative for every identity check (the 60-digit arithmetic sits ~30 orders inside that bar).

**Context-only cross-check (not evidence; not part of the claim):** ρ_Lambda implied by canonical a0 equals Ω_Λ·ρ_crit computed with the README k03-block context values (H₀ = 67.4 km/s/Mpc, Ω_Λ = 0.685) to 1.02e-4 relative — a 0.01% bookkeeping consistency of the framework's own conventions.

---

## 5. Negative controls (both capable of failing — and they do fail on the wrong forms)

A symbolic dimensional checker (exponent vectors over M, L, T) was given the unit map G, c, ρ, ε, M and evaluated seven candidate forms. It must accept the two correct forms (non-vacuity) and reject every rho↔epsilon substitution made without a coefficient change:

| test | candidate | vector | checker | expected |
|---|---|---|---|---|
| 1a CORRECT | κ·c·√(G·ρ) | (0,1,−2) | accept | accept ✓ |
| 1b CORRECT | κ·√(G·ε) | (0,1,−2) | accept | accept ✓ |
| 2a **NEG** | κ·c·√(G·ε) — c **retained**, ε substituted | (0,2,−3) | **reject** | reject ✓ |
| 2b **NEG** | κ·√(G·ρ) — c dropped | (0,0,−1) | **reject** | reject ✓ |
| 2c **NEG** | κ·c²·√(G·ρ) — extra c | (0,2,−3) | **reject** | reject ✓ |
| 2d **NEG** | κ·√(G·ε)·c² — c back in energy form | (0,3,−4) | **reject** | reject ✓ |
| 2e **NEG** | κ·c·√(G·ε) — ε mislabelled with mass-density dimensions | (0,2,−3) | **reject** | reject ✓ |
| 2e′ (non-vacuity) | κ·c·√(G·ρ) at ρ's own dimensions | (0,1,−2) | accept | accept ✓ |

Tests 2a–2e are exactly the required negative control ("replace ρ_L with ε_L without changing the coefficient and require the dimensional checker to reject it"): the checker is non-vacuous (1a/1b/2e′ accepted) and rejects all five mis-substitutions. The verdict would have flipped (false PASS) had ε_L shared ρ_L's exponent vector — i.e., the control is capable of failing and did not.

**Second control — deep/Newtonian limits and boundary cases.** The audited object is the scale normalization itself; the deep law v_flat⁴ = G·M_b·a0 and the MOND radius r_M are its derived relatives. Limits: ρ_L → 0⁺ ⇒ a0 → 0⁺, r_M → ∞, v_flat → 0 (exact zeros at ρ_L = 0, computed); ρ_L → ∞ ⇒ a0 → ∞. Normalization boundary case: κ = 1/2 reproduced identically by both forms on both footings (residuals ≤ 9.7e-62). These are exact identities (algebraic), and the numerical checks are finite consistency checks with saved residuals — the two are distinguished explicitly in Section 4.

---

## 6. Both footings carried separately — what the contract's non-sharing rule means here

κ = 1/2 is adopted for **both** registered footings. They then require **different** densities — the relation is a0² = κ²G c² ρ/4, so ρ ∝ a0² at fixed κ:

```text
a0_alt/a0_can              = 1.204776808
(a0_alt/a0_can)²           = 1.45148716
ρ_total/ρ_Lambda           = 1.45148716      (identical to the squared ratio, to 2.1e-61)
κ_eff if ρ_Lambda fixed    = 0.60238840      (re-labeling; not a third footing)
```

No single (κ, ρ) pair produces both a0 values: holding ρ_Lambda fixed forces κ_eff = 0.602 ≠ 1/2; holding κ = 1/2 forces ρ_total = 1.4515·ρ_Lambda. Both statements are recorded; the audited identity itself is a dimensionless-free statement valid on either footing, with its footing application given by the ratio identity of Section 3.

---

## 7. Lean certificate

`AS001_normalization_certificates.lean` (self-contained; `import Mathlib` only; Mathlib v4.34.0-rc2, lake) certifies four theorems:

1. `a0_energy_density_form` — κ·c·√(G·ρ) = κ·√(G·(ρ·c²)) for κ,c,G,ρ ≥ 0 (the identity).
2. `a0_footing_ratio_is_sqrt_density_ratio` — a0(ρ₂)/a0(ρ₁) = √(ρ₂/ρ₁) for κ,c,G,ρ₁,ρ₂ > 0.
3. `r_M_representation_invariant` — √(G·M/a0) equal through both representations.
4. `vflat4_representation_invariant` — √√(G·M·a0) equal through both representations.

Verification: `cd fable_independent_2026/lean_2026 && lake env lean <abs path>` → **exit 0, zero `sorry`** (grep count 0), and the unfiltered `#print axioms` of all four theorems reports exactly **`[propext, Classical.choice, Quot.sound]`** — the allowed set. Proof style: `rw [mul_pow, Real.sq_sqrt …]`, `Real.sqrt_sq_eq_abs` + `abs_of_nonneg`, `field_simp`, `Real.sqrt_div` — the exact Mathlib v4.34 lemma signatures were located in the vendored sources (`Mathlib/Analysis/Real/Sqrt.lean`, lines 91/178/189/378) after two API-signature mismatches on first compile (see failed_attempts).

---

## 8. What this result does and does not establish

**Established (scoped claim):** the mass-density and energy-density normalizations of the framework scale are the same exact function of the vacuum density; changing variables ρ_L ↔ ε_L = ρ_L·c² introduces **zero** additional coefficient or statistical freedom; all derived scale relatives (r_M, v_flat⁴) are representation-invariant; both footings are internally consistent and mutually exclusive in (κ, ρ) — all dimensionally checked, numerically verified to ~1e-61, and algebraically certified in Lean.

**Not established, explicitly:**
- κ = 1/2 is NOT derived (adopted input; consistent with the recorded zero-mode no-go for deriving it from the action class).
- The magnitude of ρ_Lambda is an input implied by the registered a0 (through the inverse of the audited relation); no cosmological measurement is inverted here.
- The *physical* identification "the galactic scale is set by the dark-energy density" is not derived: this audit certifies the normalization's well-formedness only. Which density (canonical ρ_Lambda vs alternative ρ_total, i.e. the footing choice) is a physical hypothesis, and the a0(z) law from the pressure promotion remains a postulate (STANDING: stage-17 promotion).
- No dynamical branch (Q, RAR, MU2, EXP AQUAL, MONO) was touched, altered, or imported; this is a CORE scale-identity result only. In particular it is not a derivation of the operative filtered-MONO target — Requirement 1 stays untouched.
- Numerical agreement at 1e-61 is finite evidence for an exact identity; the identity itself is the Lean-certified statement.

**Contribution to closure (Requirement 13 / ORCHESTRATOR gate map A01, A03, A11):** the framework's scale–vacuum relation may be retained as input under the spec; this run certifies that input's dimensional consistency and representation equivalence (a necessary leg of gate 13), and supplies the prerequisite normalization audit on which the A03 critical-density closure and A11 cosmological-coupling tasks can build. The gate itself remains open — nothing here supplies dynamics.

---

## 9. Reproducibility

Commands (cwd = repository root unless noted):
- `shasum -a 256 <task> <contracts> <sources>` — source-integrity reconciliation: all three pinned source hashes match SOURCE_MANIFEST.json exactly (README `91a5fac4…`, FRIED_CHICKEN `98d9149f…`, DERIVATIONS `8da8176e…`; STANDING `660462eb…` also matches the manifest entry). Task file hash `9067b7b9…`.
- `cd deepseek_push/astra_spawn_ideas/results/AS001/run_20260927T1959 && ulimit -t 120 && python3 compute_AS001_dimensional_audit.py > raw_output.txt 2> err.txt` — CPU bound actually enforced by `ulimit -t 120`; wall 0.0006 s; single thread; mpmath dps = 60; output + residuals written in place.
- `cd fable_independent_2026/lean_2026 && lake env lean <abs>/AS001_normalization_certificates.lean > <abs>/lean_check.out 2>&1` — exit 0; axiom lists in lean_check.out.

Artifacts: `derivation.md` (this file), `compute_AS001_dimensional_audit.py`, `raw_output.txt`, `residuals.json`, `err.txt` (stderr: one deprecation warning, non-fatal), `AS001_normalization_certificates.lean`, `lean_check.out`, `result.json`. Hashes in `result.json` → `artifacts_sha256`.