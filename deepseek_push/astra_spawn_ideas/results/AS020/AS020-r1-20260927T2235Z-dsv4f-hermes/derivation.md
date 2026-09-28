# AS020 — Scale-relation invariance under unit changes: derivation and audit

**Run:** `AS020-r1-20260927T2235Z-dsv4f-hermes` · **Task:** `deepseek_push/astra_spawn_ideas/AS020_scale_relation_invariance_under_unit_changes.md` (sha256 `13f0d383e745164a169daa0f51ed98db0719c5553ca916da96b08dab1149dd58`) · **Worker:** `deepseek/deepseek-v4-flash-0731` via OpenRouter, Hermes Agent subagent (single-seed worker) · **Outcome:** `supports_scoped_claim` · **Branch:** CORE scale identities (A01); Q/RAR/MU2/EXP/MONO untouched.

---

## 1. The precise claim, symbol dictionary, assumptions and scope

**Claim under audit** (framework base; README key equations; FRAMEWORK_CONTRACT *Mandatory scale and units*; FRIED_CHICKEN_SPEC requirement 13):

> The CORE scale cell
>
> **a0 = κ·c·√(G·ρ_Λ),   ρ_Λ = 4a0²/(Gc²),   r_M = √(GM_b/a0),   v_flat⁴ = G·M_b·a0,   C = √(GM_b a0),   σ² = C/2**
>
> is invariant under *consistent* changes of units (one new unit per base dimension, M/L/T): every quantity changes its numerical value, every dimensionless combination is preserved **exactly**, and no formula in the cell secretly depends on the unit choice. The dimensionless ratio **Π := a0/(c·√(G·ρ_Λ))** is the unit-log discriminator: it equals κ = 1/2 in every consistent system, and it *changes by an exact power of the length factor* under every inconsistent conversion (negative controls §5, hybrid galactic convention §6).

**Symbol dictionary** (exponent vectors (M, L, T)):

| symbol | meaning | units | vector | status |
|---|---|---|---|---|
| κ (kappa) | normalisation coefficient | dimensionless | (0,0,0) | **framework input, adopted κ = 1/2** (this task supplies no derivation; README states nothing derives κ) |
| c | speed of light | m s⁻¹ | (0,1,−1) | exact c = 299 792 458 m/s |
| G | Newton coupling | m³ kg⁻¹ s⁻² | (−1,3,−2) | measured input G = 6.67430e-11 (G_N; **G_bare, G_cosmo are separate symbols** not identified here) |
| ρ_Λ | vacuum mass density | kg m⁻³ | (1,−3,0) | derived from a0 via the audited relation below (identity input) |
| a0 | MOND acceleration scale | m s⁻² | (0,1,−2) | registered on two footings (below) |
| M_b | baryonic mass | kg | (1,0,0) | measured input |
| r_M | MOND radius | m | (0,1,0) | derived |
| v_flat | deep flat speed | m s⁻¹ | (0,1,−1) | derived |
| C | v_flat² (deep-law constant) | m² s⁻² | (0,2,−2) | derived |
| σ | isotropic velocity dispersion (σ² = C/2, conditional deep-equilibrium input) | m s⁻¹ | (0,1,−1) | derived/conditional |
| L_u, M_u, T_u | unit ratios (new unit in old units) | — | — | transformation parameters |

**Registered scale footings, kept separate** (mandated): canonical **a0 = 9.3619e-11 m/s²** with ρ_Lambda = 5.844412454021875e-27 kg/m³ and alternative **a0 = 1.1279e-10 m/s²** with ρ_total = 8.483089619559097e-27 kg/m³, both at κ = 1/2. These are **two normalisation hypotheses, not unit variants**: a single fixed (κ, ρ) pair cannot produce both (control B, §5.2). κ_eff = 0.602388404063278 at fixed ρ_Lambda is the equivalent re-labelling, reported not used as a third footing.

**Framework inputs vs conclusions established here.** Inputs: κ = 1/2 (adopted), G = G_N, c, M_sun, the two registered a0 values. Conclusions: (i) the transformation law (§2) and Π-invariance (Theorem 1, Lean-certified); (ii) covariant transformation of r_M, v_flat, C, σ and survival of every relation as an exact identity (Theorems 3–5, 8); (iii) the negative-control verdicts — inconsistent / partial conversions change Π by exactly computable factors (Theorems 6–7 and §5–6 numerics); (iv) the finding that the ubiquitous hybrid galactic convention (kpc, km/s, M_sun) is *not a unit system* and forces explicit (kpc/km)^±1 factors into Π and the deep law (§6). Nothing here derives κ, fixes ρ_Λ physically, or transfers to any interpolation branch.

**Boundary conditions / domain:** L_u, M_u, T_u > 0 (positive unit ratios); G > 0, ρ > 0, c ≠ 0, a0 ≠ 0 where division or √(Gρ) appears (all Lean hypotheses stated exactly in the certificate); M_b ≥ 0 physically. Dimensionless witnesses use positive variables; no observational fit is performed anywhere.

---

## 2. The unit-transformation law and exponent bookkeeping

A quantity q of dimension M^b L^a T^g takes the value q′ = q · L_u^(−a) · M_u^(−b) · T_u^(−g) in the rescaled system. This reproduces exactly the task's template:

```
a0' = a0·T_u²/L_u        (a=1, g=−2)
G'  = G·M_u·T_u²/L_u³    (a=3, b=−1, g=−2)
ρ'  = ρ·L_u³/M_u         (a=−3, b=1)
c'  = c·T_u/L_u          (a=1, g=−1)
M'  = M/M_u              (b=1)
```

**Theorem 1 (Π-invariance, exact):** for any L_u, T_u, M_u > 0, G, ρ > 0, c ≠ 0,

```
a0′ / (c′·√(G′ρ′)) = a0 / (c·√(Gρ))            [AS020.pi_invariant, Lean]
```

The proof is pure exponent cancellation: G′ρ′ = (G·M_u·T_u²/L_u³)·(ρ·L_u³/M_u) = (Gρ)·T_u² (the mass and length ratios cancel identically), so √(G′ρ′) = √(Gρ)·T_u for T_u > 0, and c′·√(G′ρ′) = (c·T_u/L_u)·√(Gρ)·T_u = c·√(Gρ)·T_u²/L_u — the same factor carried by a0′.

**Theorem 2 (the relation survives):** if a0 = κ·c·√(Gρ) then a0′ = κ·c′·√(G′ρ′) **for any real κ** (in particular κ = 1/2 — no unit change can alter the adopted coefficient) — `AS020.a0_relation_preserved`. Since κ is dimensionless, its numerical value is unit-independent by construction; a unit change of the *quantities alone* leaves κ untouched.

**Covariant derived scales (exact, Lean `vflat4_covariant`, `rM2_covariant`, `sigma_sq_preserved`, `rho_norm_covariant`):**

```
v_flat′⁴ = G′M′a0′   = (GM_b a0)·T_u⁴/L_u⁴        ⟹  v_flat′ = v_flat·T_u/L_u
r_M′²   = G′M′/a0′   = (GM_b/a0)·1/L_u²            ⟹  r_M′    = r_M/L_u
C′      = √(G′M′a0′) = C·T_u²/L_u²                 (C = v_flat² = a0·r_M is preserved)
σ′²     = C′/2       given σ² = C/2                (the equilibrium relation is preserved)
ρ_Λ′    = 4a0′²/(G′c′²)  given ρ_Λ = 4a0²/(Gc²)    (normalisation identity survives)
```

All numbers change under a unit change — that is the point; all **relations** survive to full 80-digit precision (§4 residuals).

---

## 3. The SI → kpc–km/s–M_sun conversion, done properly

**Step 1 — consistent rescaling** (kpc, s, M_sun base units): L_u = 1 kpc = 3.085677581491367e19 m, M_u = 1 M_sun = 1.98847e30 kg, T_u = 1 s. In that system (velocities then in kpc/s):

| quantity | SI | kpc–s–M_sun |
|---|---|---|
| a0 (canonical) | 9.3619e-11 m s⁻² | 3.033985e-30 kpc s⁻² |
| c | 299792458 m s⁻¹ | 9.715612e-12 kpc s⁻¹ |
| G | 6.67430e-11 m³ kg⁻¹ s⁻² | 4.517240e-39 kpc³ M_sun⁻¹ s⁻² |
| ρ_Lambda | 5.844412454e-27 kg m⁻³ | 86.35221 M_sun kpc⁻³ |
| Π = a0/(c√(Gρ)) | 0.5 | **0.5** (residual ≤ 2.1e-81) |
|

**Step 2 — re-expression in km/s units** (pure restatement of the same physical values; a factor 1/1000 per length-power, tracked explicitly):

| quantity | value in km/s-kind units |
|---|---|
| a0 (canonical) | 9.3619e-14 km s⁻² (alt: 1.1279e-13) |
| c | 299792.458 km s⁻¹ |
| rho_Lambda | 86.35221 M_sun kpc⁻³ (unchanged: density is kpc-kind) |
| G | **4.301047e-06 kpc (km/s)² M_sun⁻¹** (= 6.67430e-11 × 1.98847e30 / (3.0857e19 · 1e6); the literature value 4.30091e-6 differs only by the older rounded G, M_sun) |

The key rule: **one length unit per base dimension is required in any expression.** G contains L³ and, as conventionally quoted kpc·(km/s)²/M_sun, splits its three length powers across two units (1 kpc + 2 km). Any formula combining this G with km-kind a0 and c is then *not* unit-invariant unless the (kpc/km) power balance closes — see §6, where it does not.

---

## 4. Independent check in a different representation (actual residuals)

80-digit mpmath evaluation of Π and all relations across **nine consistent unit systems** — (m,kg,s), (km,kg,s), (m,g,s), (km,g,s), (m,kg,yr), (km,g,yr), (kpc,s,M_sun), (pc,yr,M_sun), (au,yr,M_sun) — on both footings, plus all derived-scale tests (§2 identities re-evaluated in every system):

- Π = 0.5 in all 18 (footing × system) cells; worst |residual| **2.11e-81** (residuals.json `Pi_*`).
- r_M transforms as L⁻¹: worst residual **1.67e-81**; v_flat⁴/(G′M′a0′) = 1 exactly: residual 0; C = a0·r_M: residual 0; σ² = C/2: worst 2.11e-81; v_flat⁴ matches (GM a0)·T_u⁴/L_u⁴: worst 1.43e-81 (`derived_*`).
- Normalisation identity ρ′ = 4a0′²/(G′c′²) in every system on both footings: worst residual **1.95e-81** (`norm_*`).
- Footing ratio a0_alt/a0_can invariant: residual 0 under m→km and under (pc, yr, M_sun) (`footing_ratio_*`).
- Rounding covariance: the *declared* 5-significant-figure inputs satisfy the identities to the same relative precision in every system (departure bound 2.1e-81 — the rounded pair moves together under conversion; digits 9.3619e-11 ↔ 9.3619e-14 etc. are reproduced, `witnesses`).

These are **exact-identity checks carried at 80 digits**, not finite numerical coincidences: the residuals are machine noise at the working precision, and the same statements are proven exactly in Lean (§8).

Witness values on both footings (M_b = 1 M_sun): r_M = 0.0385860 pc (canonical) / 0.0351541 pc (alt); v_flat = 333.866 m/s / 349.783 m/s; σ = 236.08 m/s / 247.33 m/s; C = 1.114665e5 m²s⁻² / 1.223482e5 m²s⁻²; a0 = 3.0214916e-12 pc yr⁻² / 3.6402230e-12 pc yr⁻²; ρ = 5.84441e-27 kg m⁻³ = 5.84441e-24 g cm⁻³ / 8.48309e-27 kg m⁻³ = 8.48309e-24 g cm⁻³.

---

## 5. Negative controls (both capable of failing — both failed exactly as predicted)

### 5.1 Control A (task-mandated): convert lengths, leave a0 in SI
G, ρ, c converted with L_u = 1000 (m → km), but a0 kept at its SI number 9.3619e-11 (or 1.1279e-10). Result on **both** footings:

```
Π_bad  = a0_SI / (c′ √(G′ρ′)) = 500.0        (predicted failure: κ·L_u/T_u² = 500)
Π_bad/κ = 1000 = L_u exactly (residual vs prediction 2.16e-81 / 0)
```

The dimensionless ratio **fails by exactly the length factor** — this is the discrimination the task's control must detect, and it does. Lean statement: `hybrid_detector` — a0/((c/L_u)·√(G′ρ′)) = L_u·(a0/(c√(Gρ))) exactly, for any L_u ≠ 0.

### 5.2 Control B: the footings cannot share (κ, ρ)
Π evaluated with the alternative a0 over the canonical ρ at κ = 1/2 gives Π = κ_eff = **0.602388404063278 ≠ 0.5** (residual vs κ_eff 0). Equivalently: holding ρ_Lambda fixed forces κ_eff = 0.60239; holding κ = 1/2 forces ρ_total/ρ_Lambda = (a0_alt/a0_can)² = 1.45148716. A single fixed (κ, ρ) pair cannot carry both registered footings — they are separate normalisation hypotheses (cf. AS001).

---

## 6. Finding: the hybrid galactic convention (kpc, km/s, M_sun) is a hidden unit choice

The convention quoted in most galactic-dynamics literature — G in **kpc·(km/s)²/M_sun**, ρ in M_sun/kpc³, a0 and c in km/s-kind units — is **not** a rescaling of the base units (it assigns the length dimension two different units, kpc for G's coordinate power and ρ, km for velocities and accelerations). Consequences, computed at 80 digits on both footings (residuals.json `hybrid_*`):

```
Π_hybrid = a0h/(ch·√(Ghy·ρhy))            = 1.62038964472e-17  = 0.5·(kpc/km)⁻¹   (exponent −1.0, exact)
v_flat⁴ vs G_hy·M_hy·a0_hy                = 3.0856775814913670e16 × v_flat⁴        (exponent +1.0, exact)
```

I.e., any formula written in the hybrid with the numbers as quoted **violates the framework identities by an exact (kpc/km)^±1 = 3.085677581491367e16 factor** unless the explicit factor is inserted (or all three of G's length powers are re-expressed in one unit). The dimensionless ratio Π is the detector: it is dimensionless only in consistent systems; in the hybrid it carries a dimension. The repair is *not* a new formula — it is the same formula in a consistent system, e.g. (km, s, M_sun) with G in km³ M_sun⁻¹ s⁻² (6.67430e-11×1.98847e30/1e9) and ρ in M_sun km⁻³: there Π = 0.5 and v_flat⁴ = GM a0 to ≤ 2.7e-81 (checked, both footings).

This is the concrete answer to the task's "any formula that secretly depends on a unit choice": none of the CORE cell's formulas depends on the unit choice **within consistent systems**; the dependence that exists is (i) the numerical restatement of dimensionful constants (notation: "9.3619e-11" presumes m/s²), and (ii) the hybrid convention, whose numbers are not values in any consistent unit system, and which shifts every relation by computable exact factors.

---

## 7. Deep/Newtonian limits and boundary checks

The CORE scale cell has no interpolation regime of its own, so per the task we check normalisation and boundary cases instead of limits: the identity ρ_Λ = 4a0²/(Gc²) ⇔ a0 = (c/2)√(GρΛ) on both footings in all nine systems (§4, residual ≤ 1.95e-81); the boundary case "both footings coincide" is excluded by construction and replaced by the unit-invariant footing *ratio* a0_alt/a0_can = 1.20483... (residual 0 under two different rescalings); the deep-regime statement of the cell is the v_flat⁴ = GM_b a0 identity itself (§4, residual 0). Limiting-regime behaviour of the *interpolation branches* (Q, RAR, MU2, EXP, MONO) is out of scope: their arguments are already dimensionless ratios (y = B/a0, x = g/a0), and any statement about them needs its own branch proof — **no branch translation is performed or claimed here**.

---

## 8. Machine certificate (Lean 4, mathlib v4.34.0-rc2)

`AS020_scale_relation_invariance_certificates.lean`, verified with `lake env lean` in `fable_independent_2026/lean_2026` (lakefile `mondlean`, pinned mathlib): **8 theorems, zero `sorry`**, every axiom set exactly {propext, Classical.choice, Quot.sound} (checked programmatically — no `sorryAx`):

| theorem | statement | purpose |
|---|---|---|
| `pi_invariant` | Π′ = Π under any consistent rescaling (hypotheses: L_u, T_u, M_u > 0; G, ρ > 0; c ≠ 0) | §2 Theorem 1 |
| `a0_relation_preserved` | a0 = κc√(Gρ) ⟹ a0′ = κc′√(G′ρ′) | §2 Theorem 2 |
| `vflat4_covariant` | G′M′a0′ = (GMa0)·T_u⁴/L_u⁴ | §2 |
| `rM2_covariant` | G′M′/a0′ = (GM/a0)/L_u² | §2 |
| `sigma_sq_preserved` | σ² = C/2 ⟹ (σT_u/L_u)² = (CT_u²/L_u²)/2 | §2 |
| `hybrid_detector` | a0/((c/L_u)√(G′ρ′)) = L_u·a0/(c√(Gρ)) — the negative control is exact | §5.1 |
| `footing_ratio_invariant` | a0t_alt/a0t_can = a0_alt/a0_can | §7 |
| `rho_norm_covariant` | ρ = 4a0²/(Gc²) ⟹ ρ′ = 4a0′²/(G′c′²) | §2 |

## 9. Bounds, commands, environment

Compute script `compute_AS020_unit_invariance.py` (mpmath, 80 digits): **wall time 0.003 s** (enforced limit 120 s via SIGALRM), **max RSS 17.4 MiB** (17 762 KiB; raw macOS bytes 18 186 240), **1 thread** (single-process Python, no threading/pools). Commands recorded in `result.json`. Lean verification: `cd fable_independent_2026/lean_2026 && lake env lean <abs path>` — 8 theorems compiled, axiom check passed (section 8). Source hashes verified against SOURCE_MANIFEST.json: README `91a5fac4…`, FRIED_CHICKEN_SPEC `98d9149f…`, DERIVATIONS `8da8176e…` — all match; no source drift to reconcile.

---

## 10. Strongest surviving statement, limitations, next implication

**Strongest surviving statement.** Let (L_u, M_u, T_u) > 0 be any consistent unit rescaling and q′ the rescaled value of q. Then: (1) Π := a0/(c√(Gρ_Λ)) is exactly invariant, hence a0 = κc√(Gρ_Λ) holds with the **same κ** in every consistent unit system, for both registered footings at κ = 1/2 with their separate densities; (2) r_M, v_flat, C transform covariantly (r_M′ = r_M/L_u, v_flat′ = v_flat·T_u/L_u, C′ = v_flat′², σ′² = C′/2) and the normalisation identity survives; (3) every checked relation holds to ≤ 2.2e-81 in nine unit systems on both footings (80-digit residuals, not booleans); (4) the negative control fails exactly (Π → 500 = κ·L_u) and the hybrid convention shifts Π and the deep law by exactly (kpc/km)^∓1 = 3.0857e16 — the unit-dependence one can actually write down, and it lives in the *convention*, not in any CORE formula. Lean 4 certificates cover the exact algebra of (1)–(4). **Domain:** the algebraic scale cell — no dynamics, no fit, no branch law.

**What this does not establish.** κ = 1/2 remains adopted, not derived (nothing here removes its freedom). ρ_Λ is not identified with a physical density. No interpolation branch (Q, RAR, MU2, EXP, MONO) is touched — the CORE cell's invariance does not transfer derivative, stability or regularity statements. G_N = G_bare = G_cosmo is not claimed: the identities are within one G convention, and a cross-G statement must carry the ratio G_cosmo/G_N (cf. AS014). k_B is declared but never used — no temperature law is in this cell. Rounding at 5 significant figures is a declaration convention, not a unit change; the residuals above use the declared values as given. The σ² = C/2 relation is preserved *given* it holds — its physical derivation (equilibrium formation) remains a separate obligation (FRAMEWORK_CONTRACT: conditional deep-equilibrium input).

**Next unresolved implication.** The invariance here is algebraic and within one G symbol. The first missing bridge to the full theory: **the identification of the G and ρ entering the CORE identities with the measured Newton G_N and a physical vacuum density** — i.e., an argument fixing the (G, ρ_Λ) pair (one equation, ρ_Λ = 4a0²/(G_N c²), one adopted κ), without which the a0–vacuum clause of requirement 13 remains a postulate. Any transfer of the present result to a relativistic action must also derive that the same quantities (G_N, ρ_Λ, κ) enter the field equations with identical unit conventions.

**Suggested follow-up (child proposal, not executed here):** AS020.C01 — *unit-homogeneity audit of published hybrid-convention formulas in this repository*: scan the repository's galactic-unit formulas (e.g., halo/rotation-curve notebooks quoting G = 4.30091e-6 kpc(km/s)²/M_sun) for implicit (kpc/km)-power bookkeeping, using the Π- and v⁴-relations as automatic detectors, and quantify per-formula mismatch factors. This is a distinct task: it changes the object of analysis from the CORE cell (here) to quoted formula transcriptions in a specific convention, with a new failing control (a formula found with a misbalanced kpc/km power). Full child specification: `branches/AS020/AS020.C01.md`.

**Closure implication (gate map).** The named gate is Requirement 13 ("cosmological acceleration-scale relation — preserve or derive"), cell A01/A03/A11. This run certifies the *unit-invariance leg* of the adopted input (a necessary, dimension-level consistency condition on any candidate same-action witness: whatever action realises the cell, its predictions expressed in different unit systems must coincide — guaranteed here at the scale-cell level). The gate itself stays **OPEN**: no dynamics, no derivation of κ, no physical identification of ρ_Λ; closure_candidate = null.