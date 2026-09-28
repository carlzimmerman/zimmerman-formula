# AS025 — Dimensional closure of a proposed new coefficient: derivation and audit

**Run:** `run_20260928T000953` · **Task:** `deepseek_push/astra_spawn_ideas/AS025_dimensional_closure_of_a_proposed_new_coefficient.md` (sha256 `770f69cddf23f924179aa8965fa282a55f25a5dc88422f655cd6a1e106cb4ed8`) · **Worker:** deepseek/deepseek-v4-flash-0731 (OpenRouter), Hermes Agent subagent, single-run worker seed · **Outcome:** `supports_scoped_claim`

---

## 1. The precise claim, symbol dictionary, assumptions and scope

**Claim under audit** (task "Mathematics and principal test"; framework base, README key equations; FRAMEWORK_CONTRACT "Mandatory scale and units"):

> The proposed vacuum acceleration scale is the general monomial
>
> **a = A · cᵖ · Gᵍ · ρ_Lʳ  with acceleration dimensions (0, 1, −2)**
>
> in the three inputs (c, G, ρ_L). Its dimensional closure requires: (i) the exponent vector (p, g, r) is uniquely fixed by dimensional analysis to (1, ½, ½) — there is exactly one dimensionally consistent monomial family; (ii) the remaining coefficient **A is dimensionless and is NOT fixed by dimensions** — dimensional analysis alone does not force A = ½; (iii) A is an **independent dimensionless input**: it is not a re-expression of G, c, or ρ_L, no dimensionful combination can absorb it, and on the framework footing A **is** the adopted κ = ½. A is a genuine (if empirically anchored) input, exactly as the repository's record states ("Nothing derives κ").

**Symbol dictionary** (SI throughout; exponent vectors over (M, L, T)):

| symbol | meaning | units | exponent vector | status |
|---|---|---|---|---|
| A | proposed dimensionless coefficient | — | (0,0,0) | audited object; framework identification A = κ = ½ **adopted input** (this task supplies no independent derivation, and its own control shows none can come from dimensions) |
| c | speed of light | m s⁻¹ | (0,1,−1) | fixed exact 299 792 458 m/s |
| G | Newton coupling | m³ kg⁻¹ s⁻² | (−1,3,−2) | measured input 6.67430e-11 (mandated default) |
| ρ_L | vacuum mass density | kg m⁻³ | (1,−3,0) | input (footing-dependent; implied by registered a0 through the audited relation) |
| a0 | MOND acceleration scale | m s⁻² | (0,1,−2) | registered on two footings: **9.3619e-11** and **1.1279e-10** m/s², carried separately |
| M_b | baryonic mass | kg | (1,0,0) | measured input (M_sun for examples) |
| r_M | MOND radius √(G·M_b/a0) | m | (0,1,0) | derived; A-independent in dimensions |
| v_flat | deep flat speed, v_flat⁴ = G·M_b·a0 | m s⁻¹ | (0,1,−1) | derived; ∝ A^{1/4} |

**Framework inputs vs. conclusions established here.** Inputs: A = κ = ½ (adopted), G, c, the two registered a0 footings. Conclusions: (i)–(iii) above — uniqueness of the exponent vector, non-fixation of A by dimensions (with explicit other dimensionally valid A), and the status of A as one independent dimensionless input; plus the footing-ratio theorem and the A-scaling of the derived relatives (r_M dimensionally inert; v_flat⁴ ∝ A; v_flat ∝ A^{1/4}).

**Boundary conditions / domain:** ρ_L > 0, A > 0, c, G > 0 (all physical); theorems certified on the positive domain; boundary case ρ_L → 0 checked numerically (a0 → 0 for any A). Dimensionless witnesses use positive variables only; no observational fit is performed or required by the task.

**Branch discipline:** this is a CORE scale-identity audit (group A01). Q, RAR, MU2, EXP AQUAL and MONO are untouched; no branch translation is made or claimed. The operative filtered-MONO target (amended Requirement 1) and causality criterion B (amended Requirement 7) are not addressed by this seed.

---

## 2. Step 2 — the dimensional exponent equations and their unique solution

Let the monomial a = A·cᵖ·Gᵍ·ρ_Lʳ (A dimensionless) have acceleration dimensions. With base vectors c = (0,1,−1), G = (−1,3,−2), ρ_L = (1,−3,0), the exponent system is

```text
M:  −g + r = 0
L:   p + 3g − 3r = 1
T:  −p − 2g = −2
```

Coefficient matrix and determinant:

```text
      ┌  0  −1   1 ┐
M₃ =  │  1   3  −3 │        det M₃ = −2 ≠ 0   ⇒  unique solution (full rank, no null freedom)
      └ −1  −2   0 ┘
```

Exact solution (Cramer, `fractions.Fraction`): **(p, g, r) = (1, ½, ½)**. Substitution check: (0,1,−1) + ½(−1,3,−2) + ½(1,−3,0) = (0,1,−2) ✓ (m s⁻²). A bounded exhaustive search over all exponent triples in {k/2 : k = −4…4}³ (4913 triples, exact rational arithmetic) finds **exactly one** dimensionally valid family — (1, ½, ½) — so the uniqueness is not an artifact of the linear solve (grid search, `grid_search_unique_family` pass).

**The remaining coefficient A is not fixed by dimensions.** After the system is solved, A multiplies a monomial with the correct exponent vector for **every** A > 0. Dimensional analysis fixes the *shape* (which powers of c, G, ρ_L) and leaves the *coefficient* free:

```text
a(A) = A · c · √(G·ρ_L)     for every A > 0     (dimensionally valid acceleration)
```

**Relation of A's freedom to the adopted κ.** The framework identity is a0 = κ·c·√(G·ρ_L) with κ = ½ adopted. Comparing: **A is exactly the framework κ** — the dimensional closure of the proposed coefficient identifies it as the same dimensionless object, carrying the same freedom, with κ = ½ still an input (consistent with the repository's zero-mode no-go: the action class cannot derive κ either; dimensions certainly cannot). The task's own first-principles obligation is honored: "The adopted one-half normalization is not a derived result unless an independent argument removes its freedom" — no such argument exists here; A = ½ remains adopted, now *proved* to be the only kind of freedom dimensional analysis leaves.

**Independent-input audit (what the task calls "adds an independent input or is a re-expression of existing ones"):** A is an independent dimensionless input. Reasons: (a) the three dimensionful inputs c, G, ρ_L are fully consumed by the exponent system (3 equations, 3 unknowns, det ≠ 0) — no dimensionful combination is left over that could absorb A; (b) A is the unique recoverable parameter of the relation: given a0, c, G, ρ_L the value A = a0/(c·√(G·ρ_L)) is uniquely determined (Lean: `a0_inverse_exact` recovers a0 exactly from the inverted density at fixed A, `a0_unique_multiplier` shows different A give different accelerations); (c) A is *not* a re-expression of an existing input in the sense of a derived combination — it is the one dimensionless degree of freedom the scale identity carries, and the framework's empirical anchors (measurements of κ: 0.551 ± 0.043 distance-free; the L232 parameter-free selection n = 2 ⇒ κ = ½) are data-side constraints on it, not dimensional consequences.

---

## 3. Step 3 — all factors, signs, units; the algebra in full

Every factor of the closed monomial (A > 0, ρ_L > 0):

```text
a(A) = A · c · √(G · ρ_L)
  A      : dimensionless, adopted 1/2, free by dimensions (Section 2)
  c      : (0,1,−1)  — one power of speed
  G      : (−1,3,−2) — one half-power of the Newton coupling
  ρ_L    : (1,−3,0)  — one half-power of the vacuum mass density
  √(G·ρ_L): (0,0,−1) — inverse time (frequency); c lifts it to acceleration
  total  : (0,1,−1) + (0,0,−1) = (0,1,−2) = m s⁻²        ✓
```

All factors positive on the physical domain; no sign branch. No limiting regime is used — the dimensional closure is an exact finite statement; the only "limits" checked are the boundary case ρ_L → 0⁺ (a0 → 0 for every A) and the A-scaling of the deep/Newtonian relatives (below).

**Inversion (closure of the relation).** For ρ_L(a0) := a0²/(A²·G·c²) (the framework density at fixed A),

```text
a0(A, ρ_L(a0)) = A·c·√(G·a0²/(A²·G·c²)) = A·c·(a0/(A·c)) = a0        (exact)
```

i.e. the scale relation is a bijection a0 ↔ ρ_L at fixed A; inverting and re-substituting loses nothing — A is exactly the one remaining degree of freedom (Lean `a0_inverse_exact`).

**Derived relatives, A-dependence (units for ANY A):**

```text
r_M      = √(G·M_b/a0)      : ½[(−1,3,−2) + (1,0,0) − (0,1,−2)] = (0,1,0) = m      ✓  (A-independent in dimension)
v_flat⁴  = G·M_b·a0(A)      : (−1,3,−2) + (1,0,0) + (0,1,−2) = (0,4,−4) = (m/s)⁴   ✓  ∝ A
v_flat   ∝ A^{1/4}          (exact ratio identity, Lean `vflat_ratio_is_fourth_root_A_ratio`)
v_flat⁴  = A·c·G^{3/2}·M_b·√ρ_L   (deep-MOND Tully–Fisher with the coefficient explicit)
```

Numerical A-scaling on the canonical footing (M_b = M_sun): v_flat(A=½) = 333.866 m/s, v_flat(A=1) = 397.036 m/s = 2^{1/4}×333.866 (residual 0 at 60 digits), v_flat(A=0.461 horizon) = 327.095 m/s.

**Both footings, carried separately (mandated).** κ = A = ½ is adopted for both footings, which then require different densities (the relation is ρ ∝ a0² at fixed A):

```text
canonical:      a0 = 9.3619e-11  m/s²  ⟺  ρ_Lambda = 5.844412454e-27  kg/m³
alternative:    a0 = 1.1279e-10  m/s²  ⟺  ρ_total   = 8.483089620e-27  kg/m³
ρ_total/ρ_Lambda = 1.45148716 = (a0_alt/a0_can)²  (exact ratio identity, Lean `footing_density_ratio`)
κ_eff at fixed ρ_Lambda = 0.60238840            (equivalent re-labeling; NOT a third footing)
```

The dimensionless content (A's freedom, the ratio theorem) applies identically to both footings: the footings enter only through the density pair, never through A — e.g. a0(0.551)/a0(0.5) = 1.102 exactly on **both** footings (computed residual 0).

**Exact identity c·√(G·ρ_footing) = 2·a0_footing.** With ρ from the inverted relation at A = ½, the monomial at A = 1 returns exactly twice each registered a0: a(A=1) = 1.87238e-10 m/s² (canonical) and 2.2558e-10 m/s² (alternative) — the "Milgrom prefactor-1" form. This identity is the numerical face of the closed-form algebra in Section 2, not a fit.

---

## 4. Step 4 — independent check in a different representation (bounded, actual residuals)

`compute_AS025_dimensional_closure.py` (mpmath, mp.dps = 60, single thread, `ulimit -t 120` CPU cap actually enforced; wall 0.039 s, RAM trivial) uses **three independent representations**: (a) exact rational Cramer solve; (b) a 4913-cell exhaustive exponent-grid scan (different algorithm, same answer — one hit); (c) direct 60-digit evaluation of the monomial at both footings, plus every derived-relative check. Actual residuals (saved in `residuals.json`; tolerances set before evaluation: 1e-30 relative for all identity checks):

| check | observed | pass |
|---|---|---|
| exact exponent solution | (p,g,r) = (1, ½, ½); det = −2 | ✓ |
| grid scan: # dimensionally valid families | exactly 1 | ✓ |
| monomial reproduces a0_can at A = ½ | rel resid **0.0** (closed form) | ✓ |
| monomial reproduces a0_alt at A = ½ | rel resid **0.0** (closed form) | ✓ |
| c·√(G·ρ_footing) = 2·a0_footing both footings | rel resid 0.0 | ✓ |
| A = 1 ⇒ exactly 2× each footing | rel resid 0.0 | ✓ |
| v_flat(A=1)/v_flat(A=½) = 2^{1/4} | 1.189207115002721 vs 1.189207115002721, resid 0.0 | ✓ |
| a0(0.551)/a0(0.5) = 1.102 on both footings | rel resid 0.0 | ✓ |
| r_M, v_flat⁴ exponent vectors, any A | (0,1,0), (0,4,−4) | ✓ |
| boundary ρ_L → 0 | a0 = 0.0 exactly (A = ½) | ✓ |
| κ_eff = a0_alt/(c·√(G·ρ_Lambda)) | 0.602388404063 ≈ 0.60238840 (to 1e-5) | ✓ |

The residuals are 0.0 because these are closed-form identities evaluated at 60 digits (e.g. A·c·√(G·4a0²/(Gc²)) = 2A·a0 symbolically); the finite-precision arithmetic then returns exact zeros. They are the actual saved values, not booleans, and the exactness claim rests on the Lean certificate (Section 7), not on the numerics.

---

## 5. Step 5 — negative controls (both capable of failing; both executed)

**Control 1 — "dimensional analysis alone forces A = ½" must be refuted with another dimensionally valid A.**

Four explicit witnesses, each with the identical closed exponent vector (1, ½, ½) — i.e. each is a perfectly dimensionally consistent acceleration monomial — and each with A ≠ ½:

| A (dimensionless) | a on canonical footing (m/s²) | a on alternative footing (m/s²) | dimensionally valid |
|---|---|---|---|
| 1 (Milgrom prefactor 1) | 1.87238e-10 | 2.2558e-10 | ✓ |
| 0.461… = √(8π/3)/(2π) (README k03 horizon value) | 8.625284474495188e-11 | 1.039154269836585e-10 | ✓ |
| 0.60238840 (κ_eff at fixed ρ_Lambda) | 1.127899992392e-10 | 1.35886775272e-10 | ✓ |
| 0.551 (README measured distance-free κ) | 1.03168138e-10 | 1.2429458e-10 | ✓ |

The claim "dimensional analysis forces A = ½" **fails** (as it must): the checker's acceptance criterion is the exponent vector, and all four witnesses pass it while disagreeing with ½. The control is non-vacuous because the checker simultaneously **rejects** every wrong exponent triple, e.g. c·√(G·ρ²) → (½, −½, −2), c²·√(G·ρ) → (0,2,−3), √(G·ρ) → (0,0,−1) (frequency, not acceleration), c·G·ρ → (0,1,−3), c²·ρ → (1,−1,−2), G^{1/3}·ρ → (⅔,−2,−⅔) — i.e. no dimensionless multiplier A can repair a wrong exponent vector (A cannot carry dimensions by definition of the proposed coefficient). The verdict would have flipped (false "dimensions fix A") had the checker accepted, say, √(G·ρ) — a control genuinely capable of failing.

**Control 2 — boundary and normalization cases (the deep and Newtonian regimes are scale statements here, not asymptotic laws).**

- Boundary: ρ_L → 0⁺ ⇒ a0(A) → 0 for every A (exact at ρ = 0, computed); ρ_L → ∞ ⇒ a0 → ∞.
- Normalization: A = ½ reproduces both registered footings exactly through the closed monomial (Section 4); A = 1, A = 0.461, A = 0.602, A = 0.551 each produce *different but dimensionally valid* scales — the registered value selects κ = ½ empirically, not dimensionally.
- Deep regime (where it exists as a derived relative): v_flat⁴ = G·M_b·a0(A) is dimensionally closed for every A and scales linearly in A; Newtonian-side relative r_M = √(G·M_b/a0) is dimensionally closed for every A. These are **exact algebraic identities** (Lean-certified ratio and scaling theorems), distinguished explicitly from the finite numerical consistency checks (Section 4).

---

## 6. Negative control on the "independent input" question

Control in A-space: the relation must not silently re-express (κ, ρ_L) in a way that adds or hides a degree of freedom. Exact bijection checks: at fixed A the map ρ_L → a0 is injective (ratio theorem), at fixed a0 the map A → ρ_L is injective (inverse exact), and different A give different accelerations at fixed density (`a0_unique_multiplier`). Counting: the relation a0 = A·c·√(G·ρ_L) has exactly one dimensionless degree of freedom (A) and one dimensionful one given (c, G fixed) — the density ρ_L — matching the framework's (κ, ρ_L) pair. No third coefficient appears; A is not a re-expression of G, c, ρ_L because those three are pinned by the exponent system, and A is not derivable from them.

---

## 7. Lean certificate

`AS025_dimensional_closure_certificates.lean` (self-contained, `import Mathlib`; Mathlib v4.34.0-rc2, lake) certifies **six theorems**:

1. `a0_inverse_exact` — a0(A, c, G, a²/(A²·G·c²)) = a for A, c, G, a > 0: the scale relation closes exactly; A is the sole remaining degree of freedom.
2. `a0_unique_multiplier` — a0(A₁) = a0(A₂) ⇒ A₁ = A₂: A is an observable parameter with distinguishing content; dimensional analysis admits every A > 0.
3. `a0_A_ratio_is_A_ratio` — a0(A₂)/a0(A₁) = A₂/A₁, independent of c, G, ρ: the dimensionless theorem that carries the A-freedom to both footings.
4. `footing_density_ratio` — at fixed A: a0(ρ₂)/a0(ρ₁) = √(ρ₂/ρ₁).
5. `vflat4_ratio_is_A_ratio` — (G·M·a0(A₂))/(G·M·a0(A₁)) = A₂/A₁ (deep law linear in A).
6. `vflat_ratio_is_fourth_root_A_ratio` — v_flat(A₂)/v_flat(A₁) = √√(A₂/A₁) (v_flat ∝ A^{1/4}).

Verification: `cd fable_independent_2026/lean_2026 && lake env lean <abs path>.lean` → **exit 0; zero `sorry`** (grep count 0); unfiltered `#print axioms` of all six theorems reports exactly **`[propext, Classical.choice, Quot.sound]`** — the allowed set. (The dimensional *units* facts are audited in Python's exact rational checker; Lean certifies the real-algebra content.) Proof idioms: `field_simp` (no trailing tactic), `mul_right_cancel₀` (nonzero proof first, equation second — verified against the vendored Mathlib signatures after two API mismatches, see failed_attempts), `Real.sqrt_div`/`Real.sqrt_mul` with the (hx : 0 ≤ x) (y : ℝ) argument order, `Real.sqrt_sq_eq_abs` + `abs_of_pos`.

---

## 8. Strongest surviving statement, and the first implication needed to transfer it

**Strongest supported statement (scoped, CORE branch):** The proposed coefficient's dimensional closure is *consistent and complete in its own terms*: among all monomials in (c, G, ρ_L), exactly one family has acceleration dimensions — a(A) = A·c·√(G·ρ_L) with exponent vector (1, ½, ½) — and within it the coefficient A is a genuine independent dimensionless input, not fixed by dimensions (witnesses A ∈ {1, 0.461, 0.602, 0.551} all dimensionally valid), uniquely recoverable from the scale (bijection), and identical in status to the framework's adopted κ = ½. The claim "dimensional analysis forces A = ½" is refuted; the framework's position that κ = ½ is an input survives this audit strengthened (no hidden dimensional route to ½ exists). Both footings carried separately at A = ½ with densities 5.844412454e-27 and 8.483089620e-27 kg/m³; the dimensionless ratio theorem applies to both. Deep and Newtonian relatives are dimensionally closed for every A (v_flat⁴ ∝ A, v_flat ∝ A^{1/4}, r_M dimension-inert).

**First additional implication needed to transfer to the full theory:** dimensional closure says nothing about *which* physical density ρ_L is (canonical vacuum vs alternative total-density footing — the A01/A03 physical-choice question), and nothing about *why* A = ½ is selected by nature (measurement, not dimensions — the repository's κ-measurement chain and the L232 parameter-free selection supply data-side anchors; a first-principles derivation of κ remains open, consistent with the zero-mode no-go). The operative gate map cell is **Requirement 13** (a0–vacuum relation preserved as input or genuinely derived) with group cells A01 (this audit) — the gate itself stays open (no dynamics supplied here), and no branch (Q, RAR, MU2, EXP, MONO) was imported to repair or extend anything.

---

## 9. Reproducibility

Commands (cwd = repository root unless noted):

- `shasum -a 256 README.md qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md campaign_fresh_gravity_astra/DERIVATIONS.md deepseek_push/astra_spawn_ideas/AS025_dimensional_closure_of_a_proposed_new_coefficient.md` — source reconciliation: all three pinned source hashes match SOURCE_MANIFEST.json exactly (README `91a5fac4…`, FRIED_CHICKEN `98d9149f…`, DERIVATIONS `8da8176e…`); task file hash `770f69cd…` matches the manifest's `task_sha256`.
- `cd deepseek_push/astra_spawn_ideas/results/AS025/run_20260928T000953 && ulimit -t 120; ulimit -v 524288; python3 compute_AS025_dimensional_closure.py > raw_output.txt 2> err.txt` — exit 0; wall 0.039 s (`time`); single thread; mpmath mp.dps = 60. CPU cap enforced via `ulimit -t 120`; memory cap declared 512 MB (trivial scalar arithmetic; no allocation bound needed).
- `cd fable_independent_2026/lean_2026 && lake env lean <abs>/AS025_dimensional_closure_certificates.lean > <abs>/lean_check.out 2>&1` — exit 0; axiom lists in `lean_check.out`.

Artifacts: `derivation.md` (this file), `compute_AS025_dimensional_closure.py`, `raw_output.txt`, `residuals.json`, `err.txt` (empty), `AS025_dimensional_closure_certificates.lean`, `lean_check.out`, `result.json`. Hashes in `result.json` → `artifacts_sha256`.
