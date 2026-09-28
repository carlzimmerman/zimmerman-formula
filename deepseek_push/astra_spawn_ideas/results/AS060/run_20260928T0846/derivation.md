# AS060 — The PD08 quadratic OR expansion: exact coefficient audit

**Run:** `run_20260928T0846` · **Seed:** AS060 (sha256 `5b6caaa70e850d76d649402c9463a07a41746a30c3592297dc33fba3d890ecd5`) · **Branch:** CORE coefficient (A03); conditional MU_n statistical response · **Status:** completed, 20/20 checks PASS, Lean-certified.

## 1. Precise claim, symbol dictionary, boundary conditions, assumptions

**Claim under audit (PD08, lines 54–55 and 213–214):** the two-channel OR composition
μ(Y) = 1 − (1 − p(Y))² is expanded as μ = 2Y + (2c2 + 1)Y² + O(Y³).
**Seed's stated object (AS060, "Mathematics and principal test"):** μ = 2Y + (2c2 − 1)Y² + O(Y³).

**Symbols and units** (all SI):

| symbol | meaning | units |
|---|---|---|
| Y = g/s | dimensionless drive (baryonic acceleration over the vacuum rate) | 1 |
| s = c√(G ρ_L) | the vacuum's own acceleration rate | m s⁻² |
| g = B | baryonic Newtonian acceleration | m s⁻² |
| p(Y) | per-channel engagement, p(0)=0, p′(0)=1 (fraction identity), p(∞)=1 | 1 |
| μ(Y) = g_N/g | response; deep-MOND slope μ′(0) = 2 | 1 |
| c2, c3, … | completion coefficients of p (real, dimensionless) | 1 |
| λ | per-channel linear coefficient in the diagnostic extension p = λY + … | 1 |
| n | channel count (μ_n family), n ≥ 1 integer | 1 |
| κ = a₀/s | framework ratio; **κ = 1/2 ADOPTED as input** | 1 |

s carries acceleration units: [c√(Gρ_L)] = (m/s)·√(m³kg⁻¹s⁻²·kg·m⁻³) = (m/s)·s⁻¹ = m s⁻². ✓

**Framework inputs (adopted, not derived here):** a₀ = κ c √(G ρ_L), κ = 1/2; s = c√(Gρ_L) = 2a₀; Y = g/s.
**Conclusions established:** (i) the exact coefficient of Y² in the OR composition is **2c2 − 1** (not 2c2 + 1); (ii) μ′(0) = 2 for every completion; (iii) the leading κ implication (κ = a₀/s = 1/2 via the deep spherical matching) uses only the slope and is **unaffected** by the discrepancy; (iv) the O(Y²) discrepancy is a prose typo in PD08 — the executable expression computes the correct coefficient; (v) the member engagement p = Y/(1+Y) reproduces the MU_n family exactly (n = 2 is MU2 at Y = g/(2a₀) = x/2).

## 2. The exact second-order term and every occurrence in PD08

**Direct computation** (symbolic, sympy `Poly`; independent Lean `ring` certificate):

μ = 2p − p²,  p = Y + c2Y² + c3Y³:
μ(Y) = 2Y + **(2c2 − 1)**Y² + (2c3 − 2c2)Y³ **− (2c3 + c2²)Y⁴ − 2c2c3Y⁵ − c3²Y⁶** (exact polynomial).

Generic per-channel slope (diagnostic extension p = λY + c2Y²):
μ(Y) = 2λY + (2c2 − λ²)Y² − 2λc2Y³ − c2²Y⁴ (exact).

**Occurrence audit of the coefficient in pinned PD08** (sha256 `83f6054c…0cfb`, matches SOURCE_MANIFEST.json):

| location | occurrence | correct? |
|---|---|---|
| PD08 L54 (STEP 4 text) | μ = 2Y + **(2c2+1)**Y² + … | **NO** — prose typo |
| PD08 L214 (READING) | μ = 2Y + **(2c2+1)**Y² + … | **NO** — prose typo |
| PD08 L97 + L123–125 (executable) | `p = Y + c2*Y**2`; `mu_exp = expand(1-(1-p)**2)` | YES — computes 2Y + (2c2−1)Y² exactly |
| PD01 (both prose and code) | no explicit (2c2±1) coefficient text (grep-verified) | — |

**Does the discrepancy affect the leading κ implication? No.** The deep matching (below) uses only μ′(0) = 2; the Y² coefficient enters nothing that determines a₀. The typo does, however, change finite-Y predictions of the response's quadratic behavior by +2Y² at every c2 (see negative control), so any future test of the *completion* against finite-Y RAR data must use 2c2 − 1.

## 3. Intermediate algebra with scale factors, signs, units

- Chain rule through the OR: μ′(0) = 2·(1 − p(0))·p′(0) = 2·1·1 = 2 — dimensionless, independent of c2, c3 (Lean: `or_slope`).
- **Deep spherical matching** (μ ~ 2g/s, point source): div(μ∇Φ) = 4πGρ ⇒ (1/r²)d/dr[r²·(2g/s)·g] = 4πGρ ⇒ first integral 2g²r²/s = GM ⇒ g² = (s/2)(GM/r²) = (s/2)g_N. Matching the a₀-line g² = a₀g_N ⇒ **a₀ = s/2 ⇒ κ = a₀/s = 1/2** (Lean: `deep_poisson_algebra`, `kappa_half`, `kappa_half_value`). s entered only as the argument's unit; a₀ is the output.
- **Leading neglected term at the deep end:** μ(Y) = 2Y + (2c2−1)Y² + O(Y³) with explicit coefficient (2c2−1); at the corpus member (c2 = −1, c3 = +1) the cubic is +4Y³. Domain |Y| ≪ 1 (g ≪ s).
- **Newtonian limit and boundary cases:** μ(∞) = 1 (saturation), μ(0) = 0 (vacuum normalization) — symbolic limits on the exact member (Lean `member_sq`, `member_pow`; numeric D2).
- **Conditional MU_n statistical response:** the OR composition at the member p = Y/(1+Y) equals μ_n(Y) = 1 − (1+Y)^(−n) **exactly** (symbolic for n ≥ 1; Lean `member_mu_n` for all n ∈ ℕ). Its quadratic coefficient is −n(n+1)/2; at n = 2: −3 = 2·(−1) − 1 ✓ — i.e., MU2 at Y = g/s = g/(2a₀) = x/2 on the adopted footing, matching the framework contract's MU2 cell exactly.

## 4. Independent checks in a different representation (actual residuals)

| check | representation | result |
|---|---|---|
| C1 (Y=0.1, member c2=−1) | mpmath 50-digit closed form vs truncations | true-trunc residual 0.003553719… = 4Y³ − 5Y⁴ + …; text-trunc sits exactly **+2Y² = 0.02** above the true truncation |
| C1b (Y=0.01) | exact tail model | residual 3.950593079e-6 vs 4Y³ − 5Y⁴ = 3.95e-6: difference 5.93e-10 < 7e-10 (residual O(Y⁵), coefficient 6 = 2c3 − … at member) |
| C3 | finite difference of the exact MU2 member at Y=0.1 | FD slope 1.50262755277 vs exact 2(1+Y)⁻³ = 1.5026296018: **relative residual 1.4e-6** |
| deep/Newtonian | symbolic limits on the exact member | μ(∞)=1, μ(0)=0 exactly |
| Lean | 14 theorems, zero sorry | compile exit 0; axioms ⊆ {propext, Classical.choice, Quot.sound} (verified via `#print axioms`) |

## 5. Negative controls (both capable of failing — and they do)

1. **Seed-mandated control (C2):** take the text coefficient 2c2 + 1 at c2 = 0 and compare with the true value at Y = 0.05. Text μ = 0.1025; true μ = 0.0975; **residual = 0.005 = 2Y² exactly**. The control discriminates the typo (if PD08's prose were correct, the residual would be 0); at p = Y the truncated form is exact, so the residual is exactly the coefficient discrepancy.
2. **Coefficient-form sensitivity (C2b):** (2c2+1) − (2c2−1) = 2 for **every** c2 (Lean `neg_control`, ring). This control refuted this script's own preliminary guess that the two forms coincide at c2 = −1/2 (they never coincide: 2c2+1 = 2c2−1 has no real solution). No completion hides the typo.
3. **Diagnostic counterexamples at λ = 1/2, 1, 2 (A3b):** μ′(0) = 2λ ⇒ κ(λ) = 1/(2λ) ∈ {1, 1/2, 1/4}. The seed's warning is confirmed: κ = 1/2 is **not** protected against a non-unit per-channel slope; the premise p′(0) = 1 (fraction identity) is load-bearing. Only the *completion-independence* (freedom from c2, c3, …) is a theorem (Lean `or_slope_lam`, `kappa_lam`).
4. **Mutation sensitivity of the executable:** replacing the true coefficient by the printed one in the run's own code is exactly the C2 control: nonzero residual at c2 = 0.

## 6. Strongest surviving statement

**Theorem (conditional on the OR identification and the fraction identity premises):** for the two-channel OR composition μ = 1 − (1−p)² with p = Y + c2Y² + c3Y³ + O(Y⁴),
μ(Y) = 2Y + (2c2 − 1)Y² + O(Y³),
μ′(0) = 2 for every completion, and the deep spherical matching gives a₀ = s/2, κ = 1/2, on both footings separately (canonical a₀ = 9.3619e-11 m/s², s = 1.87238e-10 m/s², ρ_L = 5.84441e-27 kg/m³; alternative a₀ = 1.1279e-10 m/s², s = 2.2558e-10 m/s², ρ_L = 8.48309e-27 kg/m³ — the alternative footing at fixed κ = 1/2 carries its own density, ratio 1.45148716 = (a₀_alt/a₀_can)²; holding ρ_L fixed instead forces κ_eff = 0.602388). The PD08 prose coefficient (2c2 + 1) is refuted (explicit residual 2Y² > 0 at c2 = 0); the executable expression is correct; the discrepancy does **not** affect the leading κ implication (slope-only dependence).

**First missing implication to transfer to the full theory:** derive (or bound) the per-channel slope λ — equivalently the fraction identity p′(0) = 1 — from the action class. The k01 zero-mode theorem shows the action as written cannot fix it; the diagnostics show κ = 1/(2λ), so any measured κ ≠ 1/2 would read directly onto a violation of this premise, and any independent λ mechanism would set κ. No branch translation to the operative filtered-ν_mono target is claimed (D5); MONO duties are unaffected.

## 7. Footings, bounds, reproducibility

- Script `compute_AS060_or_quadratic.py`: enforced bounds **wall ≤ 120 s** (SIGALRM watchdog), **peak RSS ≤ 512 MB** (ru_maxrss watchdog thread, 0.25 s poll; RLIMIT_AS is refused by macOS — recorded as partial enforcement with the RSS watchdog as the operative mechanism), **1 thread** (no parallel constructs; BLAS/OMP pinned). Actual run: 0.17 s, 20/20 PASS.
- Lean: compiled from the run directory against `fable_independent_2026/lean_2026` (`lake env lean`), exit 0, zero `sorry`; no files written into the lean workspace.
- Checks recorded in `residuals.json` (20 entries, thresholds set before evaluation, measured values are actual numbers); raw transcript in `raw_output.txt`.

## 8. Limitations

- κ = 1/2 remains **adopted input** — this run certifies the internal coefficient algebra of the PD08 argument and its leading implication; it does not derive κ (per STANDING rev. 8–11 and k01's zero-mode theorem, the action class cannot).
- The derivation is conditional on three stated premises: the OR identification over two equal independent channels, the fraction identity p′(0) = 1, and saturation μ(∞) = 1 (PD08 D2 ledger; k01's theorem is the support for the no-second-scale reading, not a proof of p′(0) = 1).
- The static weak-field channel count (PD01 B1) is the physical identification for "two channels"; this run does not re-derive it.
- No finite-Y completion is derived: c2, c3, … remain empirical; the quadratic coefficient's sign convention is fixed here, which matters for any finite-Y kernel comparison.
- No claim transfers to MONO (operative target), RAR, EXP AQUAL or Q; the MU_n response is a conditional comparison branch (framework contract branch dictionary).

## 9. Ready child specification (not dispatched — no spawn mechanism in this worker; orchestrator decision)

**AS060.C01 — "Empirical λ-test of the fraction identity premise"** (parent AS060, run_20260928T0846).
- New claim: IF the OR identification holds, the measured κ reads λ_eff = 1/(2κ_meas) on the deep BTFR/distance-free zero points; using the corpus's committed zero points K_BTF = 0.465 ± 0.076, K_DFR = 0.551 ± 0.043: λ_eff(BTFR) = 1.075 ± 0.176, λ_eff(DFR) = 0.907 ± 0.071 → the fraction identity p′(0) = 1 is consistent at ≤ 1.3σ on these instruments, i.e. the premise is empirically supported but not pinned tighter than the zero-point precision.
- Target equation: κ = 1/(2λ) with the σ-readings; observable: the two committed zero points only (no new data; no per-object fits).
- Controls: same σ-machinery as PD01 C1; a κ = 1 control must fail the λ = 1 expectation; both footings separately.
- **Duplicate check:** closest existing seeds are **AS063** ("Identifiability of n and a per-channel slope") and **AS064** ("Sensitivity of the selected coefficient to channel asymmetry") — the proposed child overlaps their intended identifiability/sensitivity analysis; the substantive difference is the explicit use of the committed zero points to produce a λ-deviation statement with σ. Recommend the orchestrator fold this into AS063/AS064 intake rather than dispatch a duplicate. **Dispatch state: NOT DISPATCHED.**
- Dependency: none beyond committed registers (PD01 C1 constants, STANDING rev. 9 measurements).

*No claims/ files created; no manifest, ledger, contract or task file modified.*