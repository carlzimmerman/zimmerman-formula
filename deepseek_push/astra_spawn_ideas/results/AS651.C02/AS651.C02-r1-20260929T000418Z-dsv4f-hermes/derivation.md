# AS651.C02 — Boundary ensemble for the three-form flux: origin of q₀? — derivation

**Run:** `AS651.C02-r1-20260929T000418Z-dsv4f-hermes` · **Worker:** deepseek/deepseek-v4-flash-0731 (OpenRouter) via Hermes Agent subagent · **Task SHA-256:** `9af24b0982839d405c5e28d771090661968fff53fd37e2ca82520eada7bdd4dd` (verified on disk before execution) · **Started:** 2026-09-29T00:04:18Z · **Finished:** 2026-09-29T00:10:xxZ (final artifact pass) · **Parent:** AS651 `AS651-r1-20260928T140734Z-dsv4f-hermes` (provisional). Branch: k04 four-form promotion only (pinned `15c0a7e1…`, verified against SOURCE_MANIFEST.json); Q/RAR/EXP/MU2/MONO branches not used. κ = 1/2 is **adopted input**, never claimed derived.

---

## 0. Result in one paragraph

The boundary ensemble **can** select the flux amplitude `q₀` — the Stokes boundary term `δS = ∫∂L/∂F ∧ δA` reduces on the box prototype to the linear boundary law `Π₀ = (Z+2bβ²)q₀` (50-digit-verified; Lean `boundary_law_iff`) — but the ensemble **cannot select κ or the ratio `Z/β²`**: (i) `κ² = β²/(Z/2+bβ²)` is invariant on *every* nonzero flux (Lean `kappa_proj_ensemble_blind`; numeric residual 0.0 over a μ-continuum), so any q₀-selection is **κ-blind**; (ii) the unadorned (zero-new-datum) Gibbs / discharge ensemble selects `q → 0⁺` or the lowest spectral level, **not** `q_*` — the mode weight ratio `W(q_*)/W(0) = e⁻¹ = 0.3679 ≠ 1` (fires; Lean `unadorned_weight_fires`, `eps_strict_mono`); (iii) matching the target requires tuning the ensemble's own datum `Π₀* = (Z+2bβ²)q_* = 8β²q_* = 9.16750431446e-05` kg^{1/2}m^{-1/2}s^{-1} (canonical, β=1) — the adopted real **relocates** `q₀ → Π₀` (or `Δq`, or `μ`), and the B-ii ledger stays at **2 adopted reals {r, Π₀}, zero fixing equations** (the ε-matching `ε_vac = ε_Λ` is q₀-free: `r = 8−2b` for every selected q₀). The alternative changed model `P + λq` relocates `q₀ → λ` with `κ²` λ-independent (Lean `lambda_kappa_blind`). The negative control: the fine-grained membrane is **genuinely boundary-localized** (bulk Einstein residual 0.000e+00, support-disjoint), while the *same* ensemble coarse-grained as a fluid leaks `ρ_w/ε_Λ = 0.0781 ≠ 0` per wall at natural density — the control fires on the fluid representation; the static sector is untouched (dS/dC = 0) and the membrane DOF count is healthy (1 transverse scalar per wall, kinetic `+σ/2 > 0`). **Verdict: no self-consistent (datum-free) boundary ensemble exists on the pinned cell that selects `q₀ = q_*` or the ratio; the boundary-ensemble route leaves κ in a continuum — documented no-go for the κ-datum, with the q₀-origin answered as relocation, not mechanism.** κ = 1/2 remains adopted; `r = Z/β² = 8−2b` remains the single unforced real.

---

## 1. Step 1 — the boundary term δS = ∫ ∂L/∂F ∧ δA (density/coframe form, box prototype)

**Pinned sector** (identical to parent AS651, k04): `S = ∫√−g P(q) d⁴x`, `P(q) = (Z/2)q² + bβ²q²`, `F = dA` (three-form potential), `F_μνρσ = q ε_μνρσ`, `q² = −F²/24`, `a0² = Gβ²q²`, `P_q = (Z+2bβ²)q`, `b = (2−K_B)·j_sat/(16π)` (K_B ∈ {0, 1/4} → b = 0.018005393544499 / 0.015754718757862, parent literals).

**Boundary variation.** Varying A: `δS = ∫_M δF ∧ ∂L/∂F = ∫_M d(δA) ∧ Π` with `Π := ∂L/∂F`; Stokes gives

```
δS = ∫_Σ Π ∧ δA  −  ∫_M δA ∧ dΠ        (Σ = ∂M)
bulk: dΠ = 0  ⟺  ∂_μ q = 0            (parent AS651 L6; AS658: q = const, zero DOF)
boundary: δS|_Σ = ∫_Σ Π ∧ δA           (the flux datum q₀ is fixed here, or not at all)
```

**Box prototype (exact reduction).** M = [0,1]⁴, Minkowski diag(−1,1,1,1), `A = A₀₁₂(z) dt∧dx∧dy`, `φ(z) = A₀₁₂(z)`, so `F₀₁₂₃ = φ′(z)` is the only component and `q = |φ′|` (chain rule over the full 24-ordering sum, check **S1b**). With the linear profile `φ(z) = v·z` (q₀ = v):

```
S(v) = (Z/2 + bβ²) v²  ⇒  ∂S/∂v = (Z + 2bβ²) v = P_q(q₀) =: Π₀
```

**BOUNDARY LAW (pinned):** `Π₀ = (Z + 2bβ²) q₀` — the boundary conjugate of the flux is the ensemble's handle on q₀; invertible on β, Z > 0 (Lean `boundary_law_iff`, `selection_injective`). Verified: 80-digit central FD `∂S/∂v = 9.167504314458642…e-05` vs theory, residual **1.49e-62** (S1a); chain-rule coefficient `dq/dF₀₁₂₃ = F₀₁₂₃/q = +1`, residual **9.33e-58** (S1b). Tuned target: at `r* = 8−2b` the stiffness is `Z+2bβ² = 8β²`, so the datum that selects q_* is `Π₀* = 8β²q_* = 9.16750431446e-05` (canonical, β = 1) and `1.10447965865e-04` (alternative) kg^{1/2}m^{-1/2}s^{-1} (S1c; note: the parent's N4 "violation residual 9.167504e-05" is *exactly this boundary datum* — the rerun links the two results). Units: [Π₀] = [P_q] = [q] = kg^{1/2}m^{-1/2}s^{-1}.

**Note on the parent's covariant formula.** The parent's `∂P/∂F_{μνρσ} = −P_q ε^{μνρσ}/24` is a component convention tied to the 24-ordering contraction; the reduced boundary coefficient on a single-component profile follows from the full alternating-sum chain rule and is the `P_q` quoted above — checked numerically (S1b) rather than asserted.

---

## 2. Step 2 — dependence of q₀ on the ensemble parameters

**2a. Linear law, continuum in the datum.** `q₀(Π₀) = Π₀/(Z+2bβ²)` is a bijection (roundtrip residual 0.0 at 80 digits over Π₀ ∈ {1e-8, 9.17e-5, 1e-3, 1e3}, **S2a**; Lean `selection_injective`): no quantization emerges from the pinned action alone — the ensemble's selected flux spans a continuum in its own datum.

**2b. κ-blindness of any selection.** For the chemical-potential family `q₀(μ) = μ/(V(Z+2bβ²))`, μ ∈ [1e-9, 1] sweeps q₀ over four decades while `κ²(q₀) = β²q₀²/((Z/2+bβ²)q₀²)` is *identical* — max |Δκ²| = **0.0** (80 digits, **S2b**; Lean `kappa_proj_ensemble_blind`: κ²(q₁) = κ²(q₂) for **all** q₁, q₂ ≠ 0). **The ensemble's selected value drops out of κ² identically.**

**2c. Unadorned Gibbs ensemble (pure action weight, zero new data).** Weight `W(q) = exp(−V·ε_vac(q)/T)`, T chosen at the sector's own energy scale (T = ε_Λ·V). `ε_vac = (Z/2+bβ²)q²` is strictly increasing in q > 0 (min dε/dq = 9.17e-37 > 0 on the probe grid, **S2c**; Lean `eps_strict_mono`, `half_flux_lower_energy`): `W` strictly decreases, `W(q_*)/W(0) = e⁻¹ = 0.36787944 ≠ 1` — **the unadorned ensemble's mode sits at q → 0⁺, not at q_*** (fires, **S2c′**; Lean `unadorned_weight_fires`). W(q)/W(q_*) = {0.7788, 0.3679, 0.01832, 3.72e-44} at q = {q_*/2, q_*, 2q_*, 10q_*}.

**2d. Discharge chain (Bousso–Polchinski-type, single flux).** Levels `q_n = n·Δq` (n ≥ 0) with the detailed-balance weight exp(−V ε(q_n)/T): the mode is the **lowest level n = 0** (S2d) — the single-flux discharge chain runs to the bottom of the spectrum, exactly the BP single-flux statement (the dense-discretuum *statistical* selection of a small Λ is a many-flux property, outside this single-flux pin). Reproducing q_* would require the spectrum to *land* on it: `Δq = q_*/m` — a new datum.

**2e. r-blindness.** Fix the ensemble datum Π₀ = Π₀*. The boundary law then holds at **every** r ∈ {1, 2, 4, 7.96398921, 8, 16, 64} with residual **0.0** (S2e): the ensemble supplies **zero equations constraining r**; κ(r) = {1.38942, 0.99112, 0.70395, 0.50000, 0.49888, 0.35316, 0.17673} — the parent's continuum, unchanged (AS138.C01's continuum theorem: the ensemble adds no new constraint to it).

---

## 3. Step 3 — setting the ensemble to q_* at κ = 1/2: B-ii ledger

Unknowns {r = Z/β², q₀, Π₀}. Equations available:

```
boundary law            Π₀ = (Z+2bβ²) q₀        (1 equation: fixes q₀ as a function of (r, Π₀))
ε-matching  ε_vac = ε_Λ  ⟺  (r/2+b) q₀² = 4β²q₀²  ⟺  r = 8 − 2b        (q₀ CANCELS)
κ-target    κ = 1/2      ⟺  r = 8 − 2b                                   (same condition; adopted, not derived)
```

The ε-matching/κ-condition is **q₀-free** (S3: under fixed Π₀, q₀(r) varies 8.84885e-05 → 1.43162e-06 across the r-grid, yet the matching condition is r = 8−2b for every one of them):

- The ensemble's equation set is **disjoint** from the ratio condition: any ensemble that fixes q₀ leaves r exactly as free as before; any construction fixing r does so without the ensemble.
- Setting Π₀ = Π₀* = 8β²q_* reproduces q₀ = q_* at the tuned ratio — but Π₀* is **one more adopted real**: the ledger is {r, Π₀} = 2 adopted reals, 0 fixing equations, **identical structure** to the parent's {q₀, r}: the boundary ensemble **relocates the flux datum without reducing the deficit** (Lean `tuned_datum`: Π₀* = 8β²q_* exactly).
- DOF count: the three-form contributes 0 propagating DOF (parent AS658); membranes contribute 1 healthy transverse scalar per wall (S4d, kinetic +σ/2), non-gravitational; the two gravitational DOF are untouched (wall action is first-order in the metric, δ-like stress). The a-priori *statistical* variant has zero new DOF but the measure itself is the adopted datum. Either reading: deficit conserved.

---

## 4. Step 4 — NEGATIVE CONTROL: does the ensemble leak into the bulk Einstein equations? (capable of failing — it fires on the fluid representation)

Wall action `S_w = −σ∫_Σ √−h d³x` at t = t_b on a Friedmann slice; T^w_{μν} distributional.

| Repr. | Regulator/geometry | Bulk residual (dimensionless, canonical footing) | Verdict |
|---|---|---|---|
| **S4a fine-grained** | Gaussian width ε = ℓ_H/1000 (ℓ_H = c/H₀ = 1.373e26 m, H₀ = 2.184e-18 s⁻¹); bulk window [t_b+ℓ_H/20, t_b+3ℓ_H/20] (50ε away) | **0.000e+00** (support-disjoint; exact) | boundary-localized ✓ |
| **S4b coarse-grained ('fluid')** | same wall, ε = ℓ_H/2 (fat-wall fluid representation); same bulk window | **0.0781 ≠ 0** per wall at natural density σ₀ = ε_Λ·ℓ_H | **fires**: the fluid representation leaks ρ_w/ε_Λ into the Friedmann RHS |

The control has content: the *same* pinned ensemble is boundary-invisible in the fine-grained representation and bulk-visible in the fluid representation — "genuinely boundary-localized" is a representation-dependent, checkable property, and it fails as soon as one coarse-grains. Wall-gas fractions at one wall per Hubble volume: ρ_w/ε_Λ = 1.0000 (canonical), 0.6889 (alternative) (**S4e**) — an O(1) background shift if represented as fluid. Statics: `∂S_ens/∂C = 0` identically — the primitive shift C never couples; B-i status unchanged (not established, not damaged) (**S4c**). Health: transverse-scalar kinetic coefficient +σ/2 with expansion `√(1+s²) = 1 + s²/2 − s⁴/8 + s⁶/16 + …` verified to the s⁶ tail (residual 3.91e-26 = 5s⁸/128; **S4d**).

---

## 5. Step 5 — alternative changed model: topological mass term λq (B-ii relocation audit)

`P(q) → P(q) + λq` (the spec's failure-repair branch, labelled changed model):

```
P_q = (Z + 2bβ²) q + λ = 0  ⇒  q* = −λ/(Z + 2bβ²)          (unique; residual 0 exact, S5a)
ε_vac = qP_q − P = (Z/2 + bβ²) q²                          (λ cancels: Legendre identity, Lean lambda_eps_equals_eps)
κ²(q*) = β²/(Z/2 + bβ²)                                     (λ-independent: Lean lambda_kappa_blind; numeric 0.25 for all λ)
ε_vac(q*) = (Z/2+bβ²)λ²/(Z+2bβ²)² = 4.0e-10 J/m³-scale > 0  (S5c)
```

The linear term gives the altered premise a nonzero stationary point (parent N4's "would have..."), but **B-ii merely relocates**: the free reals become {r, λ} — the λ-datum replaces the q₀-datum, κ is untouched, the deficit is conserved at 2 adopted reals / 0 equations. The spec's question "does B-ii merely relocate?" is answered **yes — shown exactly, with the κ-continuum witness unchanged** (Lean: `lambda_stationary_point`, `lambda_eps_equals_eps`, `lambda_kappa_blind`).

---

## 6. Controls — summary of actual residuals (each capable of failing)

| # | Control | Observed | Threshold (pre-set) | Pass |
|---|---|---|---|---|
| S1a | boundary law ∂S/∂v = P_q(q₀), 80-digit FD h=1e-30 | 1.49e-62 | < 1e-50 | ✓ |
| S1b | chain rule dq/dF₀₁₂₃ = F₀₁₂₃/q = +1 | 9.33e-58 | < 1e-50 | ✓ |
| S1c | tuned datum Π₀* = 8β²q_* rerun vs parent N4 | 9.16750431446e-05, |Δ| < 7e-16 | < 1e-15 | ✓ |
| S2a | boundary map bijection (roundtrip) | 0.0 | 0 | ✓ |
| S2b | κ² invariant under μ-continuum selection | 0.0 (80 digits) | 0 | ✓ |
| S2c | dε/dq > 0 on grid (Gibbs decreasing) | 9.17e-37 | > 0 | ✓ |
| S2c′ | **mode fires: W(q_*)/W(0) = e⁻¹ ≠ 1** | 0.36787944 | ≠ 1 | ✓ fires |
| S2d | discharge chain mode at lowest level | n = 0 | n = 0 | ✓ |
| S2e | r-blindness: ens-law residual for r ∈ 7-pt grid | 0.0; 7 distinct κ | 0; distinct | ✓ |
| S3 | ε-match q₀-free: r = 8−2b for every selected q₀ | 8.85e-05 → 1.43e-06 q₀ sweep | exact | ✓ |
| S4a | **fine-grained bulk Einstein residual = 0** | 0.000e+00 | 0 (support) | ✓ |
| S4b | **coarse-grained leak ≠ 0 (fires)** | 0.0781 | > 1e-3 | ✓ fires |
| S4c | statics: dS_ens/dC = 0 | 0.0 | 0 | ✓ |
| S4d | membrane kinetic +σ/2, s⁶ tail match | 3.91e-26 | < 1e-24 | ✓ |
| S4e | wall-gas fraction σ₀/(ε_Λℓ_H): 1.0000 / 0.6889 | 1.0 / 0.689 | — | ✓ |
| S5a | λ-model: P_q(q*) = 0 exact; ε λ-free | 0 / 0 (sympy) | 0 | ✓ |
| S5b | κ²(λ) independent over λ-grid | 0.25 for all | constant | ✓ |
| S5c | ε(q*) > 0 | 4.0e-10 | > 0 | ✓ |
| F1–F3 | footings, κ_eff relabel, r* reruns | 1.145938039e-05 / 1.380599573e-05; 0.6023884041; 7.96398921291 / 7.96849056248 | exact | ✓ |

21/21 PASS, exit 0. Lean: **12 theorems, compile exit 0, zero sorry, axioms ⊆ {propext, Classical.choice, Quot.sound}** for every theorem (`lean_axioms_out.txt`): boundary_law_iff, selection_injective, kappaSq_of_q, kappa_proj_ensemble_blind, eps_strict_mono, gibbs_weight_strict_dec, half_flux_lower_energy, unadorned_weight_fires, lambda_eps_equals_eps, lambda_stationary_point, lambda_kappa_blind, tuned_datum.

---

## 7. Strongest surviving statement (scoped)

**No-go statement (domain: pinned k04 single-flux class + boundary membrane sector, 4D Lorentzian).** Let the ensemble be any equilibrium selection that is a function of the boundary conjugate Π₀ (or chemical potential μ / membrane charge step Δq) and the action couplings {Z, β, b}, on the box/Friedmann prototype of Section 1. Then:

1. **Selection possible, κ blind:** the ensemble fixes `q₀ = Π₀/(Z+2bβ²)` (linear bijection, certified), but `κ² = β²/(Z/2+bβ²)` is constant on all nonzero fluxes (Lean) — the ensemble leaves κ and r = Z/β² in the parent's continuum (7-point witness; disjoint equation sets, Section 3).
2. **No datum-free self-consistent ensemble reproduces q_*:** the unadorned Gibbs weight is strictly decreasing in q (Lean) and its mode is q → 0⁺ / lowest spectral level — `W(q_*)/W(0) = e⁻¹ ≠ 1` fires; reproducing q_* requires tuning Π₀* = 8β²q_* (or Δq = q_*/m, or μ = V(Z+2bβ²)q_*) — an adopted real **relocating** q₀, deficit conserved at {r, Π₀}, 0 equations (B-ii).
3. **The λq repair relocates, does not close:** q* = −λ/(Z+2bβ²), ε_vac and κ² λ-independent (Lean); free reals {r, λ}, 0 equations.
4. **Negative control:** fine-grained ensemble is truly boundary-localized (bulk Einstein residual 0.0); coarse-grained fluid of the same ensemble leaks ρ_w/ε_Λ = 0.0781 per wall at natural density (fires); statics untouched (∂S_ens/∂C = 0); membrane DOF healthy (1 transverse scalar/wall, +σ/2); two gravitational DOF unaffected.

Hence: **there is no self-consistent boundary ensemble on the pinned cell selecting the κ-datum; q₀'s origin is relocation-to-Π₀, not mechanism; κ = 1/2 remains adopted and r = Z/β² = 8−2b remains fixed by no equation** (consistent with AS138.C01's symmetry-continuum theorem, AS651's B-ii/B-iv failure, AS658's bulk-constancy, AS669's volume-blindness — none of the surviving mechanisms closes the ratio).

---

## 8. Closure implication and next unresolved implication

**Gate:** Requirement 13 (a0–vacuum derive-arm), cell A03; AS075 obligation B (E* equation). This run closes the *boundary-ensemble* candidate as a κ-selection mechanism: the equation set of any boundary ensemble is disjoint from the ratio condition, and the q₀-datum relocates into ensemble data. The surviving routes for the single ratio `Z/β² = 8−2b`, unchanged by this run:

- **AS651.C01** (MONO-kernel transfer of b — changes the number 8−2b, does not fix the mechanism);
- **AS075.C01** E*-search cell (an equation *inside* an extended same-action class that fixes the ratio — e.g., a two-flux sector whose cross-coupling quantizes r, or a derivative/self-coupling of Z and β; must be a same-source convention, healthy counted DOF, no new species);
- **prove the class no-go** for quadratic-P four-form sectors (the failure modes are now fully catalogued: symmetries AS138.C01, bulk AS651, volume AS669, boundary ensemble — this run).

**First missing bridge:** exhibit any gauge-invariant equation depending on Z and β *separately* (not merely through `(Z/2+bβ²)q²` and `β²q²`): the disjointness argument of Section 3 shows the ratio condition `r = 8−2b` is invisible to every equation of the pinned boundary-ensemble family; the next mechanism must couple the couplings themselves.

---

## 9. Reproducibility, bounds, hashes

- `compute_as651_c02.py` → `raw_output.txt` (21/21 PASS, exit 0), `residuals.json`, `err_time.txt`.
- **Bounds (declared and enforced):** `ulimit -t 120` CPU cap on the python process (enforced); single thread via env (`OPENBLAS/OMP/MKL/VECLIB/NUMEXPR_NUM_THREADS = 1`); memory: RLIMIT_AS 512 MB refused by macOS (kernel limitation, same convention as AS067/AS068/AS075/AS651 — recorded); measured final run: **wall 0.28 s, max RSS 63,815,680 bytes (60.9 MiB)** (`/usr/bin/time -l`). Bounded single prototype; no refinement beyond the declared 80-digit arithmetic.
- **Lean:** `AS651C02_boundary_ensemble_certificates.lean` compiled with `lake env lean` from `fable_independent_2026/lean_2026` (compile host only; no files written into lean_2026): **12 theorems, compile exit 0, zero `sorry`**; unfiltered `#print axioms` for each = `[propext, Classical.choice, Quot.sound]` (`lean_compile_out.txt`, `lean_axioms_out.txt`).
- Task hash `9af24b09…` verified at start; k04 source hash `15c0a7e1…` verified against SOURCE_MANIFEST.json; all input/artifact hashes in `result.json`.

## 10. Limitations

- The boundary ensemble is implemented on a 1D box / Friedmann-slice prototype with a Gaussian regulator for the localization check (exact by support, but a thin-shell/topology-aware treatment of Σ is not attempted); no computation of instanton nucleation *rates* (the discharge hierarchy is argued structurally via the Gibbs weight, not via a computed bounce action); the Bousso–Polchinski *many-flux* landscape (which can statistically select small |Λ| among many fluxes) is outside this single-flux pin and is not computed — note it selects flux *levels*, never the coupling ratio.
- No statement about MONO-kernel b_mono (child C01), no dynamics, no criterion-B statement, no Q/RAR/EXP/MU2 conclusions; the fine-grained localization holds for the wall action class tested (−σ∫√−h), not for arbitrary boundary terms.
- κ = 1/2 and the ratio condition remain adopted/unforced; the no-go is established for the boundary-ensemble family of Section 2 (selections built from Π₀/membrane data and the pinned couplings) — a future mechanism coupling Z and β directly is labelled, not excluded.