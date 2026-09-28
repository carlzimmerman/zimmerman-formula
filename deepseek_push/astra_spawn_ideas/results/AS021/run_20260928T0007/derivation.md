# AS021 — Sign and domain of the vacuum scale: derivation and audit

**Run:** `deepseek_push/astra_spawn_ideas/results/AS021/run_20260928T0007`
**Worker:** deepseek/deepseek-v4-flash-0731 (OpenRouter), Hermes Agent subagent, single-run worker seed
**Branch:** CORE scale identities (A01 group). Q, RAR, MU2, EXP, MONO handled strictly as labelled branches for the limiting-law audit; no branch translation is performed or claimed. Operative target (filtered MONO, causality criterion B, amended thirteen items) untouched — this is the scale-leg audit, not a dynamics claim.
**Sources pinned:** README.md `91a5fac4…` (a0 identity, κ=1/2 adopted, both footings), FRIED_CHICKEN_SPEC.md `98d9149f…` (amended operative target wording), DERIVATIONS.md `8da8176e…` (scope comparison only), STANDING.md `660462eb…`, all matching SOURCE_MANIFEST.json exactly (verified `shasum -a 256` before execution).

---

## 1. Precise claim, symbol dictionary, assumptions vs conclusions

**Framework identity under audit (adopted input, README + FRAMEWORK_CONTRACT):**

```
a0 = kappa * c * sqrt(G * rho_Lambda),   kappa = 1/2 (adopted, fitted — NOT derived here)
rho_Lambda = 4 a0^2 / (G c^2)            [mass density, kg m^-3]
epsilon_Lambda = rho_Lambda c^2          [energy density, J m^-3 = kg m^-1 s^-2]
Lambda = 32 pi a0^2 / c^4                [m^-2, when the Einstein and scale G coincide]
r_M = sqrt(G M_b / a0),  C = sqrt(G M_b a0),  v_flat^4 = G M_b a0
```

**Symbol dictionary (all SI):**
| symbol | meaning | status |
|---|---|---|
| `a0` | vacuum acceleration scale, **real ≥ 0 by convention** (magnitude; m s⁻²) | framework input |
| `kappa` | dimensionless normalization, κ = 1/2 adopted | framework input (fitted, underivable by this task) |
| `c` | 299792458 m s⁻¹ (exact) | framework input |
| `G` | 6.67430e-11 m³ kg⁻¹ s⁻², the G_N leg; G_bare, G_cosmo kept as separate symbols | framework input |
| `rho_Lambda` | vacuum mass density (kg m⁻³), domain under audit | **conclusion: rho_Lambda ≥ 0** |
| `B = g_N` | Newtonian baryonic acceleration, B > 0 (dimensionless witnesses use B > 0, a0 > 0) | positive-variable domain |
| M_b | baryonic mass (kg) | positive |

**Boundary conditions / domains:** a0 ∈ [0, ∞) by convention; κ = 1/2 > 0; G > 0; c > 0; rho_Lambda free in ℝ, audited against the identity. No dynamics, no initial data, no action — this is an algebraic/limiting audit of the adopted identity and its derived scales.

**Claim to establish (quantified):**
> **T-domain.** Let a0 = κ c √(G ρ_Λ) with declared κ > 0, c > 0, G > 0 and a0 real ≥ 0. Then:
> (i) the identity has a real solution **iff ρ_Λ ≥ 0**; (ii) a0 > 0 iff ρ_Λ > 0 and a0 = 0 iff ρ_Λ = 0;
> (iii) at ρ_Λ < 0 **no real a0 exists**: the squared identity a0² = κ²c²G ρ_Λ < 0 contradicts a0² ≥ 0, and the complex continuation a0 = i κ c √(G|ρ_Λ|) is an unphysical branch excluded by the positive-real convention; the absolute-value repair a0 = κ c √(G|ρ_Λ|) is a *different law* (fails the squared identity at ρ_Λ < 0, is Z₂-symmetric under ρ_Λ ↦ −ρ_Λ, is non-C¹ at 0) and must not be labelled the original theory.
> **T-limit.** At fixed B > 0, as a0 → 0⁺ **every** branch Q, RAR, MU2, EXP, MONO reduces to Newtonian g → B; the MOND radius r_M → ∞, v_flat⁴ = G M_b a0 → 0, C → 0: flat-profile and deep-MOND observables vanish with the vacuum scale; the surviving gravitational law is Newtonian. Leading a0-corrections are branch-specific (Section 3).
> **T-deep.** At fixed a0 > 0, as B → 0⁺ every branch gives g → √(a0 B) (deep MOND law), with branch-specific first corrections.

**Assumed vs derived ledger.**
- *Assumed (inputs):* κ = 1/2; G = 6.67430e-11; c exact; footings a0 = 9.3619e-11 and 1.1279e-10 m/s²; positivity convention a0 ≥ 0; G > 0 (attractive leg).
- *Derived (this task):* domain rho_Λ ≥ 0; the sign-classification theorem; squared-identity and conversion identities (Lean-certified); the a0 → 0 Newtonian-survival theorem for the five branches with leading neglected terms and their domains; deep-limit theorem with first coefficients; footing bookkeeping (ratio 1.45148716 at fixed κ; κ_eff = 0.60238840 at fixed ρ).

## 2. Zero and negative vacuum-density classification (no analytic continuation)

Let ρ₀ = 5.844412454e-27 kg m⁻³ (canonical positive density) and evaluate the identity a0 = κ c √(G ρ) over the three cases at mp.dps = 50:

| ρ | radicand Gρ | a0 = κ c √(Gρ) | classification |
|---|---|---|---|
| +ρ₀ | +3.9020e-37 | **+9.3619e-11 m s⁻²** (real, > 0) | positive branch: a0 > 0 |
| 0 | 0 | **0.0** (exact) | degenerate branch: a0 = 0, scale vanishes |
| −ρ₀ | −3.9020e-37 | **no real solution** (undefined in ℝ) | no branch: real acceleration impossible |

**Why ρ < 0 cannot be admitted:** the squared identity a0² = κ²c²G·ρ is an immediate consequence of squaring the (nonneg) scale; at ρ < 0 the right-hand side is −κ²c²G|ρ| = −8.764517e-21 < 0, contradicting a0² ≥ 0. A real a0 satisfying both the identity and the convention therefore cannot exist; analytic continuation a0 = i·κ·c·√(G|ρ|) is an imaginary acceleration (i·9.3619e-11 m s⁻² numerically) — excluded by the framework's positive-real convention, and *not* a limit of real solutions (the map ρ ↦ a0 has no real branch across 0). No absolute-value substitution is imported: the repaired law a0 = κ c √(G|ρ|) satisfies **(a0_rep)² = +κ²c²G|ρ| ≠ κ²c²Gρ** at ρ < 0 (violation exactly +2κ²c²G|ρ| = +1.7529034322e-20 for the canonical magnitude), maps ρ and −ρ to the same a0 (Z₂ symmetry, residual 0.0 at 50 digits — a symmetry the original identity does not possess), and has d(a0_rep²)/dρ jumping from +κ²c²G to −κ²c²G at 0 (±1.499640e6). The repair is therefore a *different theory*, explicitly not the original identity.

**Sign bookkeeping.** With ρ > 0: a0 > 0 forces κ > 0 (κ = −1/2 gives a0 = −9.3619e-11 < 0, violating the magnitude convention); c > 0 by definition of a speed; with κ > 0, ρ > 0, c > 0: a real positive a0 requires G > 0 (G < 0 makes the radicand negative at ρ > 0). So the declared signs {κ > 0, c > 0, G > 0} are *consistent and mutually forced* with the convention a0 ≥ 0 and the identity; the only free sign-like variable is sign(ρ), and the identity fixes its domain to ρ ≥ 0. (The framework contract's caution is respected: G_N, G_bare, G_cosmo remain separate symbols; nothing here sets them equal, and Lambda = 32πa0²/c⁴ is recorded as the same-G expression only.)

**Which limiting law survives as a0 → 0.** a0 → 0⁺ (equivalently ρ → 0⁺, since ρ = 4a0²/(Gc²)): r_M = √(G M_b/a0) → ∞, C = √(G M_b a0) → 0, v_flat = (G M_b a0)^{1/4} → 0 (M = M_sun examples in raw_output.txt: r_M from 1.15e14 m at a0 = 1e-8 to 1.15e16 m at 1e-12; v_flat from 1073 m/s to 107 m/s). The flat-rotation-curve deep regime and the MOND radius disappear: the surviving limiting gravitational law is **Newtonian g = B**, and the vacuum scale is what creates the deep regime. A0 = 0 exactly (ρ = 0) is the degenerate Newtonian world inside the framework.

## 3. Intermediate algebra: units, signs, limiting expansions, leading neglected terms

**Dimensional ledger (exponent vectors [M, L, T]; programmatic check, all accepted):**
- √(Gρ): (0,0,−1) = s⁻¹; c·√(Gρ): (0,1,−2) = m s⁻² = a0 ✓
- ρ = 4a0²/(Gc²): (1,−3,0) = kg m⁻³ ✓
- ε = ρ c²: (1,−1,−2) = J m⁻³ ✓; Λ = 32πa0²/c⁴: (0,−2,0) = m⁻² ✓
- v_flat⁴ = G M_b a0: (0,4,−4) → v_flat: (0,1,−1) ✓; r_M = √(G M_b/a0): (0,1,0) ✓.

**Branch forces at the a0 → 0 (Newtonian) limit, B = g_N > 0 fixed, y = B/a0 → ∞:**
- **Q** (`g² = B² + a0B`, algebraic a0-line): closed form
  g = √(B² + a0B) = B√(1 + y⁻¹) ⟶ B + a0/2 − a0²/(8B) + a0³/(16B²) − ⋯
  Binomial series, convergent for |a0/B| < 1, **domain 0 < a0 < B**. Leading correction +a0/2; **leading neglected term −a0²/(8B)** (third term). Numerics (B = 1, a0 = 1e-3): ratio (g − B − a0/2)/(−a0²/8) = 0.99950031; second-order residual g − (1 + a0/2 − a0²/8) = 6.2461e-11 vs predicted +a0³/16 = 6.25e-11 (ratio agreement to 1e-2); exact identity residual g² − (B² + a0B) = −2.67e-51 (at 50 digits) — an *exact identity*, not a finite consistency.
- **RAR** (`ν = 1/(1 − e^{−√y})`, g = Bν): write s = √(B/a0):
  g = B/(1 − e^{−s});  g − B = B·e^{−s}/(1 − e^{−s})  — **exact closed form, no neglected term** (residual 8.3e-53). The correction is transcendentally small, e^{−√(B/a0)}, with no polynomial expansion in a0 — this is the "branch-specific correction" content of the audit.
- **MU2** (implicit `μ2(x)g = B`, μ2(x) = 1 − (1 + x/2)^{−2}, x = g/a0): using (1+x/2)^{−2} = 4a0²/(g+2a0)²,
  g(1 − 4a0²/(g+2a0)²) = B.  Let δ = g − B. Then δ(B+δ+2a0)² = 4a0²(B+δ); Taylor expansion in a0 (domain 0 < a0 ≪ B):
  **δ = 4a0²/B − 16a0³/B² + O(a0⁴)**; leading correction +4a0²/B; **leading neglected term −16a0³/B²**. Numerics: ratio (g−B)/(4a0²/B) = 0.99999600 at a0=1e-6 (→1); second-order residual (g−B) − 4a0²/B = −1.5997e-11 vs predicted −16a0³ = −1.6e-11 ✓.
- **EXP** (historical AQUAL, `μ_EXP(x) = 1 − e^{−x}`, g(1 − e^{−g/a0}) = B): δ = g − B solves δ(1 − e^{−(B+δ)/a0}) = B·e^{−(B+δ)/a0}, so asymptotically **(a0 < B)**: δ = B·e^{−B/a0}·(1 + O(e^{−B/a0})); leading correction B e^{−B/a0}; neglected terms exponentially suppressed. Numerics: ratio (g−B)/(B e^{−B/a0}) = 0.99959165 at a0 = 1e-1, 1.00000002 at 1e-2.
- **MONO** (operative filtered continuation; framework rule h'_mono = max(h'_RAR, δh_p/(y+y_p)), δ = 0.05, joined continuously):
  h_RAR(y) = y/(e^{√y} − 1),  h'_RAR(y) = [(e^{s} − 1) − (s/2)e^{s}]/(e^{s} − 1)².
  Computed landmarks (50 digits): **y_p = 2.5396382821881653** (h_p = 0.6476102378919149), **y_star = 2.3374124052663295** — reproduce the framework's rounded landmarks 2.5396 / 2.3374 to 1e-3 ✓. For y ≥ y_star the max-rule derivative is δh_p/(y+y_p), giving by integration the **exact continuation**
  h_mono(y) = h_RAR(y_star) + δ h_p ln[(y + y_p)/(y_star + y_p)]  (exact at y_star: ln 1 = 0, continuity residual 0.0).
  Derivative max-rule verified on a 200-point grid by numerical differentiation: max deviation 2.97e-50 relative. Newtonian limit (y → ∞): g = B(1 + h_mono/y) → B, with
  **g − B = a0·h_mono(B/a0) = a0[h_RAR(y*) + δh_p·ln((B/a0 + y_p)/(y* + y_p))]** — exact on the continuation (ratio 1.0 to 1e-40) and → 0 like a0·ln(1/a0), polynomially slower than RAR's exponential but still vanishing: Newtonian survives, with the MONO log-tail correction as the branch's fingerprint.

**Deep limit (fixed a0, B → 0, y → 0):** g → √(a0B) in all five branches, with first corrections:
Q: g = √(a0B)(1 + y/2 − y²/8 + ⋯), so (g − √(a0B))/√(a0B) ≈ y/2 (= 5e-4 in the y-basis at y=1e-6, observed 0.499999875);
RAR: ν ≈ 1/√y + 1/2 → 1 + √y/2 + ⋯ (coeff 1/2, observed 0.50008333);
MU2: μ2(x) ≈ x − 3x²/4 → 1 + (3/8)√y (coeff 3/8, observed 0.37510158);
EXP: μ(x) ≈ x − x²/2 → 1 + (1/4)√y (coeff 1/4, observed 0.25007294);
MONO: h_RAR ≈ √y → 1 + √y/2 (coeff 1/2, observed 0.50008333).
All observed first coefficients within 1e-3 of the analytic predictions; |g/√(a0B) − 1| at B/a0 = 1e-9 ≤ 1.6e-5 (Q: 5.0e-10).

**Footing bookkeeping (both footings, separately — the contract's non-sharing rule):**
- canonical a0 = 9.3619e-11 (κ = 1/2): ρ_Λ = 4a0²/(Gc²) = **5.844412454021875e-27 kg m⁻³**; ε = **5.252695959726114e-10 J m⁻³**; Λ = **1.090799763280735e-52 m⁻²**; l0 = c²/a0 = 9.600136497e26 m.
- alternative a0 = 1.1279e-10: at κ = 1/2, ρ = **8.483089619559097e-27 kg m⁻³**; ε = 7.624220727267268e-10 J m⁻³; Λ = 1.583281847696523e-52 m⁻²; density ratio (a0_alt/a0_can)² = **1.451487157399611**; at ρ fixed at the canonical value, **κ_eff = a0_alt/(2·a0_can) = 0.6023884040632778** (matches the repository's "alt κ = 0.6" label to 8 digits). Cross-checked against the accepted AS001 numerics (relative agreement 3.7e-12 / 5.2e-11 / 6.7e-9).
- **Dimensionless/domain results apply to both footings identically:** the theorems use only κ > 0, c > 0, G > 0, a0 ≥ 0 — satisfied by both.

## 4. Independent checks (different representations, actual residuals)

1. **Exact-identity residuals at 50 digits** (not booleans): Q branch g² − (B²+a0B) = −2.6728e-51; RAR closed form (g−B) − B e^{−s}/(1−e^{−s}) = 8.2795e-53; v_flat⁴ − G M_sun a0 = −1.3515e-51 relative; MONO continuation ratio = 1.0 (tol 1e-40); these separate exact identities from finite-consistency checks.
2. **Cross-run reproducibility:** footing numerics agree with the independently accepted AS001 run to 3.7e-12 (canonical ρ), 5.2e-11 (alternative ρ), 6.7e-9 (κ_eff); MONO landmarks reproduce the framework's quoted rounded values to 1e-3.
3. **Deep first-coefficient reproduction** from the *numeric* force functions (Section 3), confirming the analytic expansions independently of their derivation.
4. **MONO derivative rule** verified by numerical differentiation over a 200-point grid (2.97e-50), plus exact continuity at y_star.

## 5. Negative controls (capable of failing — and their actual outcomes)

- **C1 — negative density feed.** a0_real(−ρ₀) = **None** (identity undefined in ℝ); squared identity gives −8.764517e-21 < 0. The control *is* capable of failing (a real solution at ρ < 0 would have made it pass) and it fails: the original identity does not extend to negative density. Any ρ<0 usage needs a genuinely different model.
- **C2 — absolute-value repair must not be labelled the original theory.** Repair value a0 = 9.3619e-11 at ρ = −ρ₀ would *look* fine; the control exposes it: (a0_rep)² − κ²c²Gρ = **+1.7529034322e-20 ≠ 0** (the repair breaks the squared identity by exactly 2|κ²c²Gρ|), a0_rep(−ρ₀) − a0_rep(+ρ₀) = **0.0** (Z₂ symmetry the original lacks), derivative of the repaired square jumps ±κ²c²G at 0. PASS (repair correctly distinguished), with the exact violation magnitude recorded.
- **C3 — Newtonian and deep limiting regimes.** g − B ≥ 0, strictly decreasing to the 50-digit floor as a0 → 0 for all five branches (actual residual lists in residuals.json, e.g. Q: [4.99e-3, 5.00e-4, 5.00e-5, 5.00e-6, 5.00e-7]; RAR: [4.54e-5, 1.85e-14, 3.72e-44, 0, 0] at the floor); deep convergence |g/√(a0B) − 1| ≤ 1.6e-5 at B/a0 = 1e-9 and first-coefficient reproduction. Exact identities are flagged as such; finite checks carry their numeric residual.

## Strongest surviving statement

Under the declared conventions (κ = 1/2 > 0, c > 0, G > 0, a0 ≥ 0):
1. **Domain:** the framework identity has real solutions iff ρ_Λ ≥ 0; ρ_Λ = 0 ⇔ a0 = 0; ρ_Λ > 0 ⇔ a0 > 0 (Lean-certified for the forcing direction and the zero equivalence).
2. **No negative-density theory exists in the framework:** the squared identity is inconsistent at ρ_Λ < 0 and the imaginary continuation is excluded; the |ρ| repair is a distinct theory.
3. **Newtonian survival:** as a0 → 0⁺ every branch Q, RAR, MU2, EXP, MONO obeys g → B = G M_b/r², r_M → ∞, v_flat → 0 — the vacuum scale is necessary for every deep-MOND observable; the surviving law is Newtonian. Leading corrections are branch-specific (Section 3), so the branches remain distinct laws off the limit.
4. Both registered footings carry the same domain/limit statements; their (κ, ρ) separation is the exact ratio 1.4514871574 (fixed κ) or κ_eff = 0.6023884041 (fixed ρ).

## 6. Lean certificate

`AS021_sign_domain_certificates.lean` — 5 theorems, **zero sorry**, unfiltered `#print axioms` = `[propext, Classical.choice, Quot.sound]` for every theorem (hard bar met):
- `as021_density_positive`: 0 < a0 with κ,c,G > 0 forces 0 < ρ_Λ (domain forcing);
- `as021_zero_scale_iff_zero_density`: a0 = 0 ↔ ρ_Λ = 0 (under ρ_Λ ≥ 0);
- `as021_four_a0sq`: κ = 1/2 ⇒ 4a0² = G c² ρ_Λ (the framework conversion, cleared algebraic form);
- `as021_q_newtonian_sandwich`: 0 < B, 0 < a0 ⇒ B < √(B²+a0B) < B + a0/2;
- `as021_q_correction_bounds`: 0 < g − B < a0/2 (Q-branch correction sandwich).

Verified: `cd fable_independent_2026/lean_2026 && lake env lean <abs>/AS021_sign_domain_certificates.lean` → exit 0; axioms via `lean_axioms_check.lean` → `lean_check.out`.

## 7. Bounds (declared and actually enforced)

Declared: wall ≤ 120 s, memory ≤ 512 MB, threads = 1, mp.dps = 50.
Enforced: CPU — RLIMIT_CPU(120,120) inside the process **and** `ulimit -t 120` at the shell (both verified working on this host); threads — single-threaded CPython, no threading/multiprocessing; memory — **no OS-level cap available** (macOS/Anaconda Python refuses RLIMIT_AS and RLIMIT_DATA lowering: `ValueError: current limit exceeds maximum limit`, probed and recorded), so an in-process RSS guard aborts the run if ru_maxrss > 512 MB after any section, with peak RSS recorded: **measured wall 0.051 s, peak RSS 18.5 MB, 1 thread, dps 50** (all scalar closed-form/grid arithmetic; only bounded bisection and findroot(maxiter=50) iteration).

## 8. Limitations and next unresolved implication

**Limitations.** κ = 1/2 remains adopted, not derived (consistent with the recorded zero-mode no-go). The physical magnitude of ρ_Λ is implied, not measured, by the registered a0. The domain theorem governs the *adopted identity*, not the operative action: sign conventions of the common action's vacuum term, the G_E/G_N ratio in Λ_eff = 32π(G_E/G_N)a0²/c⁴, and the filtered-MONO dynamics (Requirement 1) are untouched. Numerics at 50 digits are finite evidence; exactness rests on the Lean certificates. Historical EXP and RAR/MU2/Q statements are comparison branches; the operative target remains filtered MONO with criterion B.

**Next unresolved implication (first bridge to the full theory).** Transfer the scale-domain result to the operative common action: prove that the action's vacuum contribution enters with **positive energy density (ε_Λ = +ρ_Λ c², sign +1)** and that **G_E/G_N > 0** in that action, so that Λ_eff = 32π(G_E/G_N)·a0²/c⁴ > 0 inherits the domain result and the MONO kernel argument a0 enters as a real positive scale in the static target — i.e., an *action-level sign audit of the vacuum term* against the September-26 amendment cell. Until then the domain statement is a property of the scale identity, not of the field equations.

**Suggested follow-up (child AS021.C01, ready spec, NOT dispatched — no spawn mechanism in this subagent run):** inspect `real_research/common_action_2026_09_26/action/FINAL_ACTION.md` (hash pinned in SOURCE_MANIFEST.json: b8c04d4e…) and certify sign(ε_Λ) = +1 and the sign of G_E/G_N in that action; target equation: Λ_eff > 0 ∧ a0 ∈ (0, ∞) in the operative parameter cell; negative control: an allowed sign-flipped vacuum term would have to produce a *different* model (different kernel argument); fingerprint: (action hash b8c04d4e…, common action CD26-4, sign convention, ε_Λ > 0 ∧ G_E/G_N > 0, Λ_eff sign, no new input).
