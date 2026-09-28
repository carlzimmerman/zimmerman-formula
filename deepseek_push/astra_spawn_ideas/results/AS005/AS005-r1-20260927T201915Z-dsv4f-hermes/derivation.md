# AS005 — Horizon normalization and Z: derivation

**Task:** `deepseek_push/astra_spawn_ideas/AS005_horizon_normalization_and_z.md`
**Branch:** CORE scale identities (branches remain labelled; κ = 1/2 adopted, NOT derived here)
**Primary evidence dir:** `deepseek_push/astra_spawn_ideas/results/AS005/AS005-r1-20260927T201915Z-dsv4f-hermes/`

---

## 1. Precise claim, symbol dictionary, assumptions

### Claim under test

```
H_L = c*sqrt(Lambda_eff/3);  R_dS = c/H_L;
Z_H = c*H_L/a0 = sqrt[(32*pi/3)*(G_E/G_N)],
reducing to sqrt(32*pi/3) when the Einstein and measured couplings coincide;
Z_H is not the spatial auxiliary Z.
```

### Symbol dictionary (SI unless noted)

| symbol | meaning | status |
|---|---|---|
| `a0` | vacuum acceleration scale (m/s²) | framework input on two footings |
| `κ` | normalization in `a0 = κ c sqrt(G_N ρ_Λ)` | **adopted κ = 1/2; not derived in this task** |
| `G_N` | measured/scale Newton coupling, 6.67430e-11 m³ kg⁻¹ s⁻² | default constant |
| `G_E` | Einstein coupling entering the vacuum curvature | carried as ratio `G_E/G_N`; set equal for the reduction |
| `c` | 299792458 m/s | default constant |
| `ρ_Λ` | vacuum mass density (kg/m³) | derived: `ρ_Λ = a0²/(κ² c² G_N) = 4 a0²/(G_N c²)` at κ=1/2 |
| `Λ_eff` | vacuum curvature (m⁻²) | derived: `Λ_eff = 8π G_E ρ_Λ/c² = 32π (G_E/G_N) a0²/c⁴` at κ=1/2 |
| `H_L` | Lambda-only Hubble rate (s⁻¹) | derived: `c sqrt(Λ_eff/3)`; framework ρ_Λ, **NOT** H0, **NOT** the critical-density rate |
| `R_dS` | de Sitter radius (m) | derived: `c/H_L` |
| `Z_H` | dimensionless horizon normalization | derived: `c H_L/a0` |
| `Z` ("spatial auxiliary") | k04 four-form stiffness `Z_q` (κ=½ ⟺ Z_q/β² = 7.96) / auxiliary vector W (L52) | **distinct object; no identification with Z_H** |
| `H0` | 67.4 km/s/Mpc = 2.18428524109e-18 s⁻¹ | **NOTED for comparison only; not used in H_L** |

### Assumptions and boundary conditions

1. `a0 = κ c sqrt(G_N ρ_Λ)` with **κ = 1/2 adopted as framework input** (task does not derive it; a derived κ would be a separate claim. STANDING rev-11 and kappa_closure/k01–k04 record that the present action class does not fix κ).
2. All variables positive: `κ, c, G_E, G_N, ρ_Λ > 0`. Dimensionless witnesses use positive variables; **no observational fit is requested or performed**.
3. `G_E` and `G_N` are separate symbols until a relation is derived; the numerics evaluate the actions at `G_E = G_N` (the task's reduction case) and carry the ratio symbolically everywhere else.
4. `H_L` uses the framework `ρ_Λ` (derived from a0 and G_N), **not** H0, **not** a critical-density `H_Λ`; the distinction is enforced in every formula and tested by the negative control (Sec. 6).
5. Both acceleration footings are carried separately: canonical `a0 = 9.3619e-11` and alternative `a0 = 1.1279e-10 m/s²`, with κ = 1/2 fixed on both → the two footings have **different** `ρ_Λ` (they never share both fixed density and fixed κ).

### Framework inputs vs conclusions

- **Inputs:** κ = 1/2; G_N, c (default constants); a0 on two footings; H0 only as noted reference.
- **Derived (this task):** ρ_Λ, Λ_eff, H_L, R_dS, Z_H, and the identity `κ Z_H = sqrt(8π G_E/(3G_N))`.

---

## 2. Derivation of the equalities

Start from the adopted scale relation and the vacuum-curvature definition:

```
a0       = κ c sqrt(G_N ρ_Λ)              (framework input, κ = 1/2)
Λ_eff    = 8π G_E ρ_Λ / c²                (vacuum curvature with Einstein coupling G_E)
H_L      = c sqrt(Λ_eff / 3)              (Lambda-only rate)
R_dS     = c / H_L
Z_H      = c H_L / a0
```

**Step 1 — ρ_Λ from a0.** Squaring the scale relation:

```
a0² = κ² c² G_N ρ_Λ   ⇒   ρ_Λ = a0² / (κ² c² G_N)   = 4 a0²/(G_N c²) at κ = 1/2.
```
Units: [a0²] = m²/s⁴, [κ²c²G_N] = m⁵/(kg s⁴) ⇒ [ρ_Λ] = kg/m³. ✓

**Step 2 — Λ_eff from a0.**

```
Λ_eff = 8π G_E ρ_Λ / c²
      = 8π G_E a0² / (κ² c⁴ G_N)
      = (8π/κ²) (G_E/G_N) a0² / c⁴
      = 32π (G_E/G_N) a0² / c⁴            at κ = 1/2.
```
Units: [a0²/c⁴] = 1/m² ✓ (the framework-contract Lambda `32π a0²/c⁴` is recovered **when G_E = G_N**; the ratio is carried explicitly otherwise).

**Step 3 — H_L.**

```
H_L² = c² Λ_eff/3 = 8π G_E ρ_Λ/3
H_L  = sqrt(8π G_E ρ_Λ / 3) = (a0/(κ c)) sqrt(8π G_E / (3 G_N)).
```
Units: [G_E ρ_Λ] = s⁻² ⇒ [H_L] = s⁻¹ ✓.

**Step 4 — R_dS.**

```
R_dS = c/H_L = (κ c²/a0) sqrt(3 G_N/(8π G_E)).
```
Units: [c²/a0] = m ✓. At κ = 1/2 and G_E = G_N: `R_dS = (c²/(2 a0)) sqrt(3/(8π))`.

**Step 5 — Z_H and the general identity.**

```
Z_H = c H_L/a0 = sqrt(8π G_E/(3 G_N)) / κ.
```
Equivalently — the **one-dimensional constraint**:

```
κ · Z_H = sqrt(8π G_E / (3 G_N)).
```

**Step 6 — reduction at κ = 1/2, G_E = G_N.**

```
Z_H = 2 sqrt(8π/3) = sqrt(32π/3) = 5.7888100364661412749...
```
This is *exactly* the task's stated reduction. Because the claim is dimensionless, **the same closed form applies to both acceleration footings** (a0 cancels in `c H_L/a0`); the two footings differ only in the dimensional orbit (ρ_Λ, Λ_eff, H_L, R_dS).

### Is Z an independent explanation?  No.

`Z_H` is a pure function of the input pair `(κ, G_E/G_N)`. It carries no degree of freedom of its own: given κ and the coupling ratio, `Z_H` is fixed; conversely the constraint `κ Z_H = sqrt(8π G_E/(3 G_N))` means "fitting" Z_H separately from κ is redundant — Z_H is κ (and G_E/G_N) restated. This matches the standing record: STANDING.md rev-11 (2026-09-26): *"Z = √(32π/3) = 5.7888 is κ restated"*; `RECIPE_BRANCH_R2_PROPOSAL_2026-09-26.md`: *"§1's Numbers line says 'Z~21 FITTED'. On the record's definition Z ≡ cH_Λ/a₀ ... κ = ½, Z = √(32π/3) = 5.7888. The '~21' was an error corrected on the record on 09-16."*

### Z_H is not the spatial auxiliary Z

The sources' four-form promotion (README k04; `kappa_closure/k04`; `L40_RIGIDITY`) uses a stiffness `Z_q` with `P(q) = Z_q q²/2` and `κ = ½ ⟺ Z_q/β² = 7.96` (L40: 7.964); `RECIPE_BRANCH_R2_PROPOSAL` states explicitly: *"Z_q = the four-form's stiffness, k04's P(q) = Z_q q²/2 — not the framework's Z = 5.7888"*. The auxiliary construction L52 pushes J onto a spatial auxiliary vector W. **No equality between Z_H and any of these symbols is asserted or derivable; Z_H ≈ 5.789 vs Z_q/β² ≈ 7.96 are numerically distinct and conceptually different objects.** This task makes no identification.

---

## 3. Intermediate algebra shown; signs, units, domain, limiting regime

All steps above are exact algebraic identities for **all positive** `κ, c, G_E, G_N, ρ_Λ` — there is no limiting regime and no truncation: the "leading neglected term" is identically zero on this domain. The domain of the identity is `κ > 0`, `G_E > 0`, `G_N > 0`, `ρ_Λ > 0`, `c > 0`. Boundary behavior (checked numerically, Sec. 6): κ → 0⁺ ⇒ Z_H → ∞; ρ_Λ → 0⁺ ⇒ H_L → 0 and R_dS → ∞ (flat-space limit, no horizon); G_E → 0⁺ ⇒ Z_H → 0.

---

## 4. Independent check in a different representation (actual residuals)

| check | observed | reference | residual | pass |
|---|---|---|---|---|
| C1 Z_H canonical (route a0→ρ→Λ→H_L→Z_H, 50 digits) | 5.7888100364661412749 | 5.7888100364661412749 | 1.07e-50 | ✓ |
| C1 Z_H alternative (same route) | 5.7888100364661412749 | 5.7888100364661412749 | 1.07e-50 | ✓ |
| C1 κ·Z_H both footings | 2.8944050182330706375 | sqrt(8π/3) | 5.35e-51 | ✓ |
| C2 closed form at κ=1/2, G_E=G_N | sqrt(32π/3) | 5.7888100364661412749 | 0 (exact) | ✓ |
| C3 R_dS·H_L = c (both footings) | 299792458.0 | c | 0 | ✓ |
| C3 R_dS = sqrt(3/Λ_eff) (both footings) | 1.6584e26 / 1.3765e26 m | same | 0 | ✓ |
| C6 independent route vs closed form | 5.7888100364661412749 | 5.7888100364661412749 | 1.07e-50 | ✓ |
| S1 symbolic (sympy) Z_H − sqrt(8πG_E/(3G_N))/κ | 0 | 0 | exact | ✓ |
| S2 symbolic Λ_eff − 8π G_E a0²/(κ² G_N c⁴) | 0 | 0 | exact | ✓ |
| S3 symbolic at κ=1/2: Λ_eff − 32π G_E a0²/(G_N c⁴) | 0 | 0 | exact | ✓ |

Symbolic result (sympy, all symbols positive): `Z_H = 2√6 √π √G_E / (3 √G_N κ) ≡ √(8π G_E/(3 G_N))/κ`, difference **identically 0** — an exact identity, not a finite numerical coincidence. The 50-digit mpmath cross-route residual (C6) is 1.07e-50.

**Lean 4 certificate** (`AS005_horizon_Z_certificates.lean`, 10 theorems, self-contained, imports Mathlib only):
`z_sq` (master squared identity), `kappa_mul_z` (the redundant constraint), `z_explicit`, `z_sq_half`, `z_sq_half_GE_GN`, `z_half_value` (Z_H = sqrt(32π/3)), `z_half_value_ratio` (Z_H = sqrt(32π G_E/(3 G_N))), `rds_sqrt3` (R_dS = sqrt(3/Λ_eff)), `lambda_eff_from_a0`, `rho_from_a0_half` (ρ = 4a0²/(G c²)).
Verification: `cd fable_independent_2026/lean_2026 && lake env lean <abs>/AS005_horizon_Z_certificates.lean` → exit 0, zero `sorry`, axioms for every theorem ⊆ {propext, Classical.choice, Quot.sound} (unfiltered `#print axioms` in `lean_axioms_out.txt`).

---

## 5. Negative control (specified; capable of failing)

**Control A — Z_H and κ treated as independent fitted constants ⇒ redundant constraint.**
The derived identity is `κ Z_H = sqrt(8π G_E/(3G_N))` (at G_E=G_N: `κ Z_H = sqrt(8π/3) = 2.89440501823`). Scanning κ ∈ {0.1, 0.25, 0.5, 0.75, 1, 2, 4} with `Z_H = sqrt(8π/3)/κ`: product residual **0.0** at 50 digits (C4, max deviation 0). Treating both as free fit constants therefore cannot be identified — the pair is constrained to a one-dimensional curve. The control is *capable of failing*: a claimed `Z ≈ 21` (the historical §1 error) would force `κ = sqrt(8π/3)/21 = 0.137828810392`, contradicting the adopted κ = 1/2; the constraint is what makes the "~21" claim detectably wrong. Recorded consistently in STANDING rev-11 and RECIPE_BRANCH_R2 (error corrected 09-16).

**Control B — deep/Newtonian limiting regimes / normalization and boundary cases.**
Z_H is a pure vacuum ratio with no baryonic-field dependence, so no deep/Newtonian regime exists for it; per the task text we check normalization and boundary cases instead:
- dimensionless normalization: `c·H_L` and `a0` both have units m/s², so `Z_H` is dimensionless; identical on both footings (verified, C1).
- boundary: κ=1/2, G_E=G_N → `sqrt(32π/3)` (exact); κ→0⁺ → Z_H→∞; ρ_Λ→0⁺ → H_L→0, R_dS→∞ (no horizon); G_E→0⁺ → Z_H→0 (no vacuum curvature).
- exact identity vs finite consistency check distinguished: the identity is an algebraic theorem (sympy diff 0; Lean-certified); the 50-digit residuals are confirming witnesses only.

**Control C (additional, must be capable of failing — it does).**
Replace H_L by the measured H0 = 67.4 km/s/Mpc in the same expression:
- `c·H0/a0_can = 6.99465110072` ≠ `sqrt(32π/3) = 5.78881003647` (difference 1.2058411);
- `κ·(c·H0/a0_can) − sqrt(8π/3) = 0.60292053` ≠ 0.
The claimed identity is specific to the framework Lambda rate and **fails** for H0 or any critical-density rate; it is not a tautology about arbitrary Hubble-type rates. Implied Ω_Λ by the framework density at the noted H0 is reported as a comparison only (canonical `(H_L/H0)² = 0.68493046`; alternative `0.99416777`) — no observational fit is made.

Control C is complemented by the k03 horizon variant: `κ_k03 = sqrt(8π/3)/(2π) = 0.460658865962` ⇒ `Z_H = 2π` exactly (C5c residual 0). The famous "2π" horizon coefficient and "sqrt(32π/3)" are the *same* constraint curve `κ·Z = sqrt(8π/3)` evaluated at two different adopted κ values — precisely the redundancy the control exposes.

---

## 6. R_dS on both footings (no mixing of cosmological inputs)

| quantity | canonical a0 = 9.3619e-11 | alternative a0 = 1.1279e-10 |
|---|---|---|
| ρ_Λ (kg/m³) | 5.84441245402e-27 | 8.48308961956e-27 |
| Λ_eff (m⁻²), G_E=G_N | 1.09079976328e-52 | 1.5832818477e-52 |
| H_L (s⁻¹) | 1.80772595288e-18 | 2.17790630348e-18 |
| **R_dS (m)** | **1.65839549696e+26** | **1.37651678367e+26** |
| R_dS (Gpc) | 5.37449378027 | 4.4609870841 |
| Z_H (dimensionless) | 5.78881003647 | 5.78881003647 |
| (H_L/H0)² = Ω_Λ,fw (comparison only) | 0.68493046 | 0.99416777 |

Every R_dS uses only the framework ρ_Λ (derived from the a0 of that footing, G_N, c) and G_E — H0, Ω_Λ and critical density enter **nowhere** in R_dS. For reference only: c/H0 = 1.37249683494e26 m (4.448 Gpc), H_sqrt(ρ_crit) = H0 by definition of ρ_crit.

**Footing bookkeeping (contract requirement).** κ = 1/2 held fixed on both footings ⇒ the alternative footing has a different density: `ρ_alt/ρ_can = (a0_alt/a0_can)² = 1.4514871574`. If instead ρ_Λ were held fixed at the canonical value, alternative a0 would imply `κ_eff = 0.602388404063`; if ρ_Λ were held at the alternative value, canonical a0 would imply `κ_eff = 0.415014628956`. The two footings never share both fixed vacuum density and fixed κ. The dimensionless result (Z_H) applies identically to both footings.

---

## 7. Strongest surviving statement, and next implication

**Surviving statement (exact, both footings, all positive variables):**
> In the CORE cell `a0 = κ c sqrt(G_N ρ_Λ)` (κ = 1/2 adopted), `Λ_eff = 8π G_E ρ_Λ/c²`, `H_L = c sqrt(Λ_eff/3)`, the horizon normalization `Z_H = c H_L/a0` obeys `κ Z_H = sqrt(8π G_E/(3 G_N))` exactly; at κ = 1/2 with G_E = G_N, `Z_H = sqrt(32π/3) = 5.78881003646614` on both acceleration footings, and `R_dS = c/H_L` = 1.6584e26 m (5.3745 Gpc, canonical) / 1.3765e26 m (4.4610 Gpc, alternative). Z_H is κ restated — a derived dimensionless ratio, not an independent fitted constant and not the four-form/auxiliary Z; the identity fails when H_L is replaced by H0 or any critical-density rate.

**Next unresolved implication for transfer to the full theory:** the *value* κ = 1/2 (equivalently any fixed Z_H) remains an adopted input: nothing in the CORE scale identities or the horizon form derives it. The closure gate affected is requirement 13 ("framework a0–vacuum relation preserved as input or genuinely derived") — the operative status is **input mode, internally consistent**; the missing bridge is an action-level derivation of κ (or of G_E/G_N) in a common-action cell, which kappa_closure/k01–k04 record as an open freedom (normalization zero mode; four-form leaves Z/β² free). No branch is imported to repair anything: the result is an exact identity, not a failed computation.

---

## 8. Reproducibility

- `as005_horizon_z.py` — bounded prototype: wall **0.077 s** (enforced limit 120 s), **1 thread**, memory peak ≈ 63 MB (ru_maxrss 63029248 bytes; limit 512 MB), mpmath 50 digits, sympy exact. Outputs: `raw_output.txt`.
- `as005_footings_complement.py` — footing bookkeeping (κ_eff under fixed density, which-H ledger). Outputs: `footings_complement.json`.
- `AS005_horizon_Z_certificates.lean` — Lean 4 certificates; `lean_axioms_out.txt` (exit 0, axioms ⊆ {propext, Classical.choice, Quot.sound}, zero sorry).
- Commands:
  - `python3 <run>/as005_horizon_z.py > <run>/raw_output.txt 2> <run>/time_bounds.txt`
  - `python3 <run>/as005_footings_complement.py > <run>/footings_complement.json 2>&1`
  - `cd fable_independent_2026/lean_2026 && lake env lean <abs>/AS005_horizon_Z_certificates.lean > <run>/lean_axioms_out.txt 2>&1` (exit 0)
- All source hashes verified against SOURCE_MANIFEST.json (README.md `91a5fac4...`, FRIED_CHICKEN_SPEC.md `98d9149f...`, DERIVATIONS.md `8da8176e...`; task sha256 `9dc8de250d0493ea3740238258278dbed5013d0aad009073bfd21b8f3bc21280`).

### Limitations

- κ = 1/2 remains an adopted input; this task proves the *identity structure and its redundancy*, not the value of κ, G_E/G_N, or any observational prediction (no fit performed).
- Numeric witnesses are 50-digit confirmations of an exact identity; the identity is the theorem, not the numbers.
- R_dS is an algebraic de Sitter radius of the framework vacuum; horizon/geodesic semantics under the full candidate action (criterion B, carrier/clock sector) are outside this CORE identity task.
- Ω_Λ,fw entries are framed strictly as comparisons at the noted H0 and are not fitted or claimed as measurements.