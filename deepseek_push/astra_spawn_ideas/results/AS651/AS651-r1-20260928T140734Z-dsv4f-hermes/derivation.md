# AS651 — Four-form metric variation fixes the Legendre vacuum energy? — derivation

**Run:** `AS651-r1-20260928T140734Z-dsv4f-hermes` · **Worker:** deepseek/deepseek-v4-flash-0731 (OpenRouter) via Hermes Agent subagent · **Task SHA-256:** `7c1ad8cc522bdf2f50b1ae87e8e1a6377f7882eb1a063cb74ec35e60c8c37fa6` (verified on disk before execution) · **Started:** 2026-09-28T14:07:34Z · **Finished:** 2026-09-28T14:33:48Z · **Seed:** A03, P0, derivation · **Branch:** explicit coefficient-mechanism diagnostic — k04 four-form promotion (pinned `15c0a7e13eb9b7a5fdb403c8826bd01912d68dc81614609fddb6cd6ed9d32399`, verified against SOURCE_MANIFEST.json). No other branch (Q, RAR, EXP, MU2, MONO) is used for any conclusion; the RAR kernel enters only as the k04 source's own kernel for numeric witnesses, labelled as such.

The seed's mathematics line is `F_μνρσ = q ε_μνρσ, L = P(q)` — a four-form field strength built from a three-form potential, with the MOND scale promoted to the flux. This run executes the five steps in order, runs the negative control (capable of failing), and audits the construction against AS075's obligation B (the shift-free positive vacuum datum equation E* with rank-1 κ-selection).

---

## 0. Result in one paragraph

The four-form promotion **repairs the sign** (B-iii) and **reduces the κ question to one coupling ratio**, but does **not** supply AS075's E*: derived exactly, `ε_vac = q P_q − P = +(Z/2 + b β²) q² > 0` (structural; AS068's negative boundary vacuum is repaired), yet `κ² = a0²/(G ε_vac) = β²/(Z/2 + b β²)` is **independent of the flux amplitude** `q₀` (Lean-certified), and `κ = 1/2` holds **iff** `Z/β² = 8 − 2b = 7.96398921` (K_B = 0; 7.96849056 at K_B = 1/4) — an equivalence with **no equation fixing the ratio** (B-ii fails: `q₀` and `Z/β²` are two adopted reals, zero fixing equations) and **no rank-1 κ-selection** (B-iv fails: the κ-projection is a continuum — Lean-certified injectivity). The negative control — varying q as a metric-independent scalar — forces `P_q = 0 ⇒ q = 0 ⇒ ε_vac = 0`: the four-form (i.e., `∂L/∂F = const` flux conservation) is load-bearing, and the altered premise is violated at the construction's own vacuum-matching flux with residual `9.167504e-05 ≠ 0`. **Verdict: the four-form does not close the E* door; κ = 1/2 remains adopted; the open question becomes "why Z/β² = 8 − 2b" (plus "why q₀ = q_*").** Outcome: counterexample to the constructive (closure) use of the four-form mechanism, with exact derived identities delivered.

---

## 1. Step 1 — source equation, independent variables, boundary conditions, measure

**Source equation (k04 four-form sector).** On a 4D Lorentzian spacetime (signature −+++; the ε-tensor `ε_{0123} = √−g`),

```
S_FF = ∫ √−g P(q) d⁴x,     P(q) = (Z/2) q² + b β² q²
q² = −F_μνρσ F^μνρσ / 24,  F_μνρσ = q ε_μνρσ,   F = dA   (A: three-form potential)
a0² = G β² q²               (scale promotion, k04: a0 = β√G |q|)
b = (2 − K_B) I / (16π),    I = 2∫ z Δ(z) dz    (k01 primitive integral, kernel-dependent)
```

**Independent variables.** The metric `g_μν` and the three-form `A_μνρ` (entering through F = dA). The MOND sector (kernel Δ) supplies `b` as an input structure of k04; it is not varied here.

**Boundary conditions / measure.** Measure `√−g d⁴x`. The flux amplitude is a **boundary/integration datum**: the bulk equation of motion constrains only `∂_μ q = 0` (constancy), never the value `q₀` (step 3). Assumption stated explicitly: one flux sector, no membranes; `q₀ ∈ (0, ∞)` adopted. All of `Z > 0, β > 0, b > 0` (stability and the kernel positivity of k01; `K_B ∈ [0, 1/4]`).

**Additional assumption needed for the displayed target** (κ = 1/2): none is supplied by the sector — the run shows that the specific half requires the *ratio* `Z/β² = 8 − 2b`, which remains unforced (steps 3–5). kappa = 1/2 is the **adopted framework input** throughout, never claimed derived.

---

## 2. Step 2 — T_μν by metric variation (F components held fixed); ε = q P_q − P

**Claim.** Varying `S = ∫√−g P(q)` with respect to `g^μν` *holding the field-strength components `F_μνρσ` fixed* (only the contraction `q² = −F²/24` moves):

```
δS = ∫ √−g · (1/2) g_μν (q P_q − P) δg^μν
T_μν = (P − q P_q) g_μν,     ε_vac := −T⁰₀ = q P_q − P        [Legendre form, Duff–van Nieuwenhuizen / Bousso–Polchinski]
```

**Derivation (with factors, signs, units).**

*Convention check.* With `ε_{0123} = √−g = 1`, `ε^{0123} = −1`; all 24 permutations of `F_μνρσ F^μνρσ` contribute `q²·(±1)·(±1)·∏g` with `∏g = −1` (diagonal chart) ⇒ `F_μνρσ F^μνρσ = −24 q²` (check **L2**, residual < 1e-12). Consequently `δq = (q/2) g_μν δg^μν` and `δ√−g = −(1/2)√−g g_μν δg^μν`; combining,

```
δS = √−g [ P_q · (q/2) − P/2 ] g_μν δg^μν = √−g (1/2) g_μν (q P_q − P) δg^μν.   ✓
```

*Component verification (representative chart).* `g_{11} = 1 + t`, all other components fixed, F components `F_μνρσ = q ε_μνρσ` fixed: exact closed form `S(t) = √(1+t)·P(q/√(1+t)) = 6/√(1+t)` at (q, Z, b, β) = (2,1,1,1). Central FD (double, t = 1e-6): `dS/dt = −2.999999997085` vs theory `−(1/2)(qP_q − P) = −3.000000000000` — PASS (**L3a**, |d| < 1e-8); mpmath 50-digit FD: `−3.000000000001875` (discretization error `f‴t²/6 = +1.875e-12` accounted, threshold 1e-11) — PASS (**L3b**); closed-form agreement to 1e-20 (**L4**); Taylor coefficient `S(t) − (6 − 3t) − (9/4)t² = −1.87484e-12` confirms the linear coefficient is exactly the Legendre energy density (**L4b**). Units: `[ε] = [P] = J/m³ = kg m⁻¹ s⁻²`; `[q] = [a0/√G] = kg^{1/2} m^{-1/2} s^{-1}`; `[Z] = [β] = [b] = 1` (**F1**).

**Legendre identity.** For `P = (Z/2)q² + bβ²q²`: `ε_vac = qP_q − P = (Z/2 + b β²) q²` — symbolic residual 0 (**L1**), and `> 0` for every `q ≠ 0` (**L5**; Lean `legendre_identity`, `vacuum_positive`). **This is the k04 F1 sign reversal, re-derived from the metric variation:** the k01 vacuum term whose sign forced `ρ_vac < 0` enters the *gravitating* energy density with positive sign through the Legendre transform. B-iii (positive vacuum) is **structural — PASSES**. Magnitude is another matter (step 5).

---

## 3. Step 3 — what fixes what: the EOM of the three-form

`∂P/∂F_{μνρσ} = −P_q ε^{μνρσ}/24` (exact: `dq/dF^{abcd} = −F^{abcd}/(24q)`). The EOM ∂_μ[√−g ∂P/∂F_{μνρσ}] = 0, with `√−g ε^{μνρσ}` equal to constant alternating-symbol components, is

```
EOM residual = −(1/24) P_qq · ∂_μ q · [alternating symbol],   P_qq = Z + 2 b β².
```

Residual = 0 **iff** `∂_μ q = 0` (check **L6**, symbolic): the bulk EOM fixes *constancy* of the flux, never its value — `q₀` is an **integration/boundary datum** (the integrated form `∂L/∂F = const`). Constraint accounting of the sector: unknowns {Z, β, q₀, κ}; equations: EOM_A (0 independent relations), Einstein with vacuum energy, framework identity `κ² = a0²/(G ε_vac)` (1 relation) ⇒ **2 real DOF remain free**. step 3 rule obeyed: `Z`, `β`, `b`, `q₀` are kept independent until an equation fixes them; none does.

---

## 4. Step 4 — NEGATIVE CONTROL: vary q as a metric-independent scalar (capable of failing)

**Altered premise.** Drop the three-form structure and treat q as an independent scalar field in `S = ∫√−g P(q)`. Then the EOM is `∂P/∂q = 0`:

```
P_q = (Z + 2 b β²) q = 0   ⇒   q = 0        (Z, b > 0; Lean scalar_variation_kills_vacuum: no q > 0 solution)
⇒ ε_vac(0) = 0             (Lean eps_zero_at_zero)
⇒ κ² = a0²/(G·0) undefined; a0 = β√G |q| = 0  (MOND scale collapses; Newtonian sector).
```

**Exhibited violation with the original equation.** The construction's own vacuum-matching flux at the canonical footing (β = 1, Z = 8 − 2b) is `q_* = a0/√G = 1.145938e-05`. At that point the altered equation has residual

```
P_q(q_*) = (Z + 2 b β²) q_* = 8 q_* = 9.167504e-05 ≠ 0     (N4; N1 symbolic)
```

and the *true* EOM of step 3 is satisfied identically there. **The control fires** (rejects the altered premise): the lost hypotheses are the flux conservation `∂L/∂F = const ≠ 0` and the positivity of the scale; residual ≠ 0, ε = 0 at the altered stationary point (**N3**), B-iii violated at q = 0 (**N2**: only stationary point q = 0). It was capable of failing — a P with a nonzero linear term (`λq`) would have a nonzero stationary point — and k04's quadratic P is shown to have none. (Fixing the premise by adding `λq` is a *changed model* with a new datum `λ`; recorded, not adopted.)

---

## 5. Step 5 — κ structure, E* audit (AS075 B-i…B-iv), witnesses, footings

**Frame relations.** Framework identity `κ² = a0²/(G ε_vac)` with `a0² = G β² q²`:

```
κ² = β²q² / ((Z/2 + b β²) q²) = β² / (Z/2 + b β²)          (q cancels exactly: L7 symbolic, E2 numerics — max |Δ| = 0.0 at 50 digits for q ∈ {0.1,1,10,100}; Lean kappa2_q_independent)
κ = 1/2  ⟺  Z/β² = 8 − 2b                                  (equivalence: Lean kappa_half_iff_ratio)
ρ_vac = ρ_Λ  ⟺  (Z/2 + b β²) q² / c² = 4 β² q² / c²  ⟺  Z/β² = 8 − 2b   (E3: ρ_vac/ρ_Λ − 1 = 0.0 at the tuned ratio)
```

**Kernel witnesses (k04's RAR kernel, same measure).** `Δ(s) = s/expm1(√s)`, truncated at the peak: `s_sat = 2.53963828`, `Δ_sat = 0.64761024`, `I_rar = jsat = 2(sΔ − ∫Δ) = 0.45252490` (dps-50 vs dps-100 refinement residual 1.00e-51 < 1e-40, **L8**). `b = (2−K_B)·jsat/(16π)`: **0.01800539** (K_B = 0), **0.01575472** (K_B = 1/4) ⇒ `Z/β² = 8 − 2b = 7.96398921` / `7.96849056` (k04's 7.96 reproduced). Stiffness bound `min(sΔ − j) = 1.054e-05 ≥ 0` (**L9**); deep limit `sΔ − j → 0⁺` (**L10**, 3.333e-07 < 1e-2).

**E* audit against AS075 obligation B:**

| Property | Status | Evidence |
|---|---|---|
| B-i shift-breaking (pairs with the primitive's additive constant) | **NOT ESTABLISHED** | The pinned construction never couples the primitive's shift C into P(q): b depends on the kernel integral I, not on C. The sector *sidesteps* the AS067 zero mode (vacuum parameterized by q₀ with `∂ε/∂q₀ = (Z + 2bβ²)q₀ ≠ 0`) instead of breaking it through an equation; the coupled-action C-dependence is a precisely named missing input. |
| B-ii no new datum | **FAILS** | Two adopted reals, zero fixing equations: the boundary flux `q₀` and the coupling ratio `Z/β²` (k04 F3 constrains only the environmental a0_loc, not the bare ratio). |
| B-iii positive vacuum `ρ_vac(j₀) = +ρ_Λ` | **PASSES structurally (sign); magnitude = adopted datum** | `ε_vac = +(Z/2 + bβ²)q² > 0` for all q ≠ 0 (Lean). `ρ_vac = ρ_Λ` selects `q₀ = q_* = a0/(β√G)` = 1.145938e-05/β (canonical), 1.380600e-05/β (alternative) — the magnitude is exactly the boundary datum. |
| B-iv rank-1 κ-selection (κ-projection collapses to a point) | **FAILS** | `κ² = 1/(r/2 + b)`, `r = Z/β² ∈ (0, ∞)` ⇒ κ ∈ (0, 1/√b) — a **continuum**; witness grid r ∈ {1,2,4,7.96399,8,16,64} → κ ∈ {1.3894, 0.9911, 0.7040, 0.50000, 0.4989, 0.3532, 0.1767}, all distinct (**E1**); strict monotonicity + injectivity in r are Lean-certified (`kappa_strict_anti`, `kappa_proj_distinct`). Only the tuned ratio lands on 1/2. |

**Footings (κ = 1/2 adopted; never both fixed density and fixed κ).**

| Footing | a0 [m/s²] | ρ_Λ [kg/m³] | ε_Λ [J/m³] | s = 2a0 [m/s²] | q_* (β=1) [kg^{1/2}m^{-1/2}s^{-1}] |
|---|---|---|---|---|---|
| canonical | 9.3619e-11 | 5.8444124540e-27 | 5.2526959597e-10 | 1.872380e-10 | 1.145938e-05 |
| alternative | 1.1279e-10 | 8.4830896196e-27 | 7.6242207273e-10 | 2.255800e-10 | 1.380600e-05 |

`κ_eff` at fixed canonical density (relabel diagnostic, not a fit) = 0.602388404. All κ- and E*-statements are dimensionless and apply to both footings identically (**F1–F4**); only G_N = 6.67430e-11 enters (G_bare/G_cosmo separate symbols; the single-G promotion is k04's own identification, carried as the construction's assumption).

**Limiting cases (same measure):** q → 0⁺ ⇒ ε → 0⁺, a0 → 0 (Newtonian, no vacuum — the q = 0 sector of the *altered* premise); q → ∞ ⇒ ε → ∞ (no preferred flux; the boundary datum carries the size).

---

## 6. Controls (each capable of failing) — summary of actual residuals

| # | Control | Observed | Threshold (pre-set) | Pass |
|---|---|---|---|---|
| C1 | Metric-variation law (FD double / FD mpmath / closed form / Taylor) | −2.999999997085 / −3.000000000001875 / agree 1e-20 / −1.87484e-12 | 1e-8 / 1e-11 / 1e-20 / 1e-10 | ✓✓✓✓ (L3a, L3b, L4, L4b) |
| C2 | Units (F1), sign (L5), normalization ε^{0123} = −1 (L2) | 0 / +6 / −96 | 0 / >0 / −96 | ✓✓✓ |
| C3 | Limiting cases: kernel deep limit, q → 0⁺, q → ∞, F6 stiffness | 3.333e-07; 0⁺; ∞; min 1.054e-05 | <1e-2; —; —; ≥ −1e-12 | ✓✓✓✓ (L9, L10, F3) |
| NC | **Negative control (altered premise)** | P_q(q_*) = 9.167504e-05 ≠ 0; q = 0 only; ε(0) = 0 | ≠ 0; [0]; 0 | **fires** ✓ (N1–N4) |
| E* | q-cancellation (E2), ratio condition (E3), projection continuum (E1) | 0.0; 0.0; 7 distinct κ | <1e-40 / <1e-45 / all distinct | ✓✓✓ |

23/23 checks PASS, exit 0.

---

## 7. Strongest surviving statement (scoped)

In the pinned k04 four-form sector (`S = ∫√−g P(q)`, `P = (Z/2)q² + bβ²q²`, `F = qε`, `a0² = Gβ²q²`), with a single flux and no membranes:

1. **Exact identities (derived):** `T_μν = (P − qP_q)g_μν`; `ε_vac = qP_q − P = +(Z/2 + bβ²)q² > 0` (the AS068 sign obstruction is repaired structurally — B-iii); `κ² = β²/(Z/2 + bβ²)`, independent of the flux amplitude `q₀`; `κ = 1/2 ⟺ Z/β² = 8 − 2b` (equivalence, Lean).
2. **Falsifying witness for the closure use:** the candidate E* (vacuum-datum equation supplied by the four form) does **not** select κ: the κ-projection is a continuum in the ratio `Z/β²` (Lean-certified injectivity, 7-point numeric witness) — B-iv fails; the sector introduces the adopted reals `(q₀, Z/β²)` with no fixing equation — B-ii fails; B-i is not established (the primitive shift C is not coupled in the pinned class). Hence the four-form promotion is **not** an E* in the AS075 sense; **κ = 1/2 remains adopted input** (the framework's stated status is preserved).
3. **Negative control fires:** varying q as a metric-independent scalar forces q = 0 and ε_vac = 0 — the three-form structure (`∂L/∂F = const`) is load-bearing; the altered premise is violated at the construction's own flux (residual 9.167504e-05 ≠ 0).

Domain: 4D Lorentzian, single-flux quadratic-P sector; symbolic statements for all q > 0, Z, b, β > 0; kernel witnesses on the RAR-truncated kernel of k04 (s ∈ [1e-3, 1e4], refinement dps 50 → 100); K_B ∈ {0, 1/4}; both registered footings. No statement about Q, RAR, EXP, MU2-branch or operative filtered-MONO targets; no causality criterion-B statement; no dynamics.

---

## 8. Closure implication and next unresolved implication

**Gate:** Requirement 13 (a0–vacuum relation derive-arm), cell A03 (coefficient mechanism / kappa missing premise). The k04 four-form is the strongest audited sign-repair to date (B-iii) but leaves the E* deficit: **exactly the ratio `Z/β² = 8 − 2b` (one real, codimension-1 condition on two couplings) and the flux magnitude `q₀ = q_*`** — the deficit count of AS075 (one independent real equation E*) is *reduced but not satisfied*: the new precise target is a same-action extension fixing `Z/β²` (or selecting `q₀`), or a no-go for the quadratic-P single-flux class. The four-form's own k04 F2 verdict ("why Z = 8β², still open") is here re-derived from first principles and upgraded to a certified rank statement.

**First missing bridge:** exhibit an equation inside an extended action (same source conventions, healthy DOF, no new species) that fixes `Z/β² = 8 − 2b` or the flux `q₀` — or prove no such equation exists for quadratic-P four-form sectors; simultaneously, the MONO-kernel transfer of `b` (the heat-filtered `h_mono` replacing the RAR Δ) is a registered open step, and the boundary-ensemble origin of `q₀` (membrane/instanton contribution to the 3-form boundary action `δS = ∫ ∂L/∂F ∧ δA`) the candidate mechanism for B-ii.

---

## 9. Reproducibility, bounds, hashes

- `compute_as651.py` → `raw_output.txt` (23/23 PASS, exit 0), `residuals.json`, `err_time.txt`.
- **Bounds (declared and enforced):** `ulimit -t 120` CPU cap on the python process (enforced); single thread via env (`OPENBLAS/OMP/MKL/VECLIB/NUMEXPR_NUM_THREADS = 1`); memory: RLIMIT_AS 512 MB refused by macOS (kernel limitation, same convention as AS067/AS068/AS075 — recorded); measured final run: **wall 0.29 s, max RSS 62.1 MB** (`/usr/bin/time -l`). Bounded single prototype, no refinement beyond the declared dps-100 kernel check.
- **Lean:** `AS651_four_form_legendre_certificates.lean` compiled with `lake env lean` on the compile host only (no files written into `fable_independent_2026/lean_2026`): **8 theorems, compile exit 0, zero `sorry`**; unfiltered `#print axioms` for each = `[propext, Classical.choice, Quot.sound]` (`lean_axioms_out.txt`): legendre_identity, vacuum_positive, eps_zero_at_zero, scalar_variation_kills_vacuum, kappa2_q_independent, kappa_half_iff_ratio, kappa_strict_anti, kappa_proj_distinct.
- Task hash `7c1ad8cc…` and source hash `15c0a7e1…` verified at start against SOURCE_MANIFEST.json; all input/artifact hashes in `result.json`.

## 10. Limitations

- No derivation of κ = 1/2; the E*-no-go is established **only** for the quadratic-P, single-flux, no-membrane class as pinned (k04); a P with a linear term, a two-flux sector, or a coupled C-dependence is a changed model, labelled separately (child C02 direction).
- B-i is reported NOT ESTABLISHED (missing input: the C-coupling of the full coupled action), not proven impossible.
- The MONO-branch analogue (b_mono with the heat filter) is not computed here (child C01); no Q/RAR/EXP/MU2-conclusions; no dynamics, no criterion-B, no empirical claims; numerics at 1e-40…1e-51 and 5e-17…1e-9 (FD) are finite evidence — the exact statements rest on the symbolic identities and the Lean certificate.