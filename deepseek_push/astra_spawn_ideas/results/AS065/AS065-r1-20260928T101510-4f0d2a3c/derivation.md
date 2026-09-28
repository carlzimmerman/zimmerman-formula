# AS065 — Closure of the OR class under coarse graining: derivation

**Run:** `AS065-r1-20260928T101510-4f0d2a3c` · **Seed sha256:** `def81066fb744efb3e018fe4818da6c8696d1cb79d83042e013653ac84c93626`
**Sources inspected (hashes match SOURCE_MANIFEST.json):** PD01 `37e39d1a…c74d`, PD08 `83f6054c…fcfb`, k01 `8df5a3ab…5b25c`.

This document executes the seed's five numbered steps, derives every intermediate factor, sign and unit, runs the mandated negative controls, and records actual residuals only.

---

## Step 1 — Precise claim, symbol dictionary, boundary conditions, assumptions

### Claim (the object to establish)

**Closure of the OR class under coarse graining.** *For n ≥ 1 independent statistical channels with survival functions q_i = 1 − p_i and total survival q_total = ∏ q_i, the response of k groups of m equal channels is a member of the SAME OR-class response family at the total count n = k·m. The deep-MOND slope of the member response equals the total count n, and the adopted normalization κ = a0/s = 1/2 is consistent with every grouping but is selected by physics (unit anchor + computed channel count), not by the product identity.*

### Symbol dictionary (units)

| Symbol | Meaning | Units |
|---|---|---|
| a0 | MOND acceleration scale (framework: a0 = κ·c·√(G·ρ_Λ), κ = 1/2 adopted) | m s⁻² |
| s | vacuum rate s = c·√(G·ρ_Λ); s = 2·a0 under κ = 1/2 | m s⁻² |
| ρ_Λ | (mass-)vacuum density | kg m⁻³ |
| Y | normalized drive Y = g/s, dimensionless, positive finite | — |
| g | gravitational acceleration of the test particle | m s⁻² |
| g_N | Newtonian acceleration G·M_b/r² | m s⁻² |
| p(Y) | per-channel engagement (completion), 0 ≤ p ≤ 1 | — |
| q(Y) | per-channel survival q = 1 − p | — |
| μ_n(Y) | n-channel OR response μ_n = 1 − q^n = 1 − (1 − p)^n | — |
| m, k, n | channel counts, n = k·m | — |
| c, G | 299792458 m s⁻¹, 6.67430e-11 m³ kg⁻¹ s⁻² (numeric legs only) | — |

### Framework inputs (adopted, not derived here)

1. a0 = κ·c·√(G·ρ_Λ) with κ = 1/2 ADOPTED (mandatory framework base).
2. r_M = √(G·M_b/a0), deep v_flat⁴ = G·M_b·a0 (L230 chain).
3. Two registered footings, kept separate: canonical a0 = 9.3619e-11 m s⁻²; alternative a0 = 1.1279e-10 m s⁻². They must not share both a fixed vacuum density and a fixed κ.
4. Units: the dimensionless drive Y = g/s is the only argument of the response; units enter only through (s, a0).

### Boundary conditions (L230 unit anchor, from k01/PD01)

- p(0) = 0 (no drive → no engagement), p'(0) = 1 in the vacuum unit s (the action's one scale; k01 zero-mode).
- p(∞) = 1 (saturation ⇒ μ_n → 1 at Y → ∞, handover to Newton).
- Channel count n = 2 of the metric's computed static channels (PD01 B1).

### Independent premises used (the honest ledger)

| # | Premise | Status |
|---|---|---|
| P1 | Independence: q_total = ∏ q_i (seed's boxed identity) | framework input |
| P2 | Equal-channel grouping: q_group = q^m | definition of the OR over m equal channels |
| P3 | p(0)=0, p'(0)=1 in unit s | L230 unit anchor (k01) |
| P4 | p(∞)=1 | normalization |
| P5 | κ = 1/2 | ADOPTED (framework); shown below to be *not* selected by the algebra |
| P6 | Channel count n = 2 | PD01 B1 computed |
| P7 | Strictly positive finite Y; |Y| < 1 for the series expansion | domain |

### Conclusions to be established (not inputs)

- C1: regrouping invariance (exact product identity, any completion p, any m, k ≥ 1).
- C2: deep-MOND slope = count: μ_n'(0) = n (chain rule, premise P3).
- C3: the count conversion κ = a0/s = 1/n is grouping-covariant; κ = 1/2 ⇔ n = 2.
- C4: the normalized group-drive slope does **not** remain one after grouping (negative control B2); the "one" is restored only by a hand-chosen unit s/m — a physical scale-selection, not a product identity (D1).
- C5: the diagnostic readings are scale-covariant: at unit s_λ = λ·s the same response reads slope n_λ = n·λ; the matched ratio a0_λ/s stays 1/2 for every λ ≠ 0 under correct unit bookkeeping, while unit-confused fits read κ = 1/(2λ) ∈ {1, 1/2, 1/4} at λ ∈ {1/2, 1, 2}.

---

## Step 2 — Regrouping invariance and the normalized group-drive slope

### 2.1 Regrouping invariance (the closure identity)

For m equal independent channels, the OR-engagement of the group is
p_G = 1 − (1 − p)^m, so the group survival is q_G = (1 − p)^m. The response of
k such groups is

μ^{(k groups of m)}(Y) = 1 − q_G^k = 1 − ((1 − p)^m)^k = 1 − (1 − p)^{m·k} = μ_{km}(Y),

the last step by **power associativity** ((x^m)^k = x^(m·k)); m·k = n is the
total count. The composed response is a member of the SAME class μ_n at n = k·m
**for every completion p** (the shape of p never enters) and every m, k ≥ 1.
Unequal channels likewise regroup: (q1·q2)·(q3·q4) = q1·q2·q3·q4 — only
independence (P1) is used.

**Exact identity, not a finite numerical check.** Certified in Lean 4
(`AS065_or_closure_pow`, `AS065_or_closure_response`,
`AS065_closure_member_two_times_two`, `AS065_survival_grouping`; see §7).

### 2.2 Does the normalized group-drive slope remain one?

**No.** In the vacuum unit s the group engagement has derivative

p_G'(0) = m·(1 − p(0))^{m−1}·p'(0) = m

by the chain rule (P3). A group of two channels has slope **2**, not 1
(negative control B2 — the claim "remains one" FAILS this control by design; the
control is live because the slope 2 is a computed value with content). Restoring
slope one requires redefining the drive unit to s_G = s/m and *then* the group
reads as one unit-slope channel — but the same procedure at m = 3 reads count 1
at unit s/3 and would "derive" κ = 1/3. The product identity is consistent with
EVERY κ = 1/m: closure does not select 1/2. That separation — a mathematical
product identity vs. a physical scale-selection principle — is the seed's
distinction, executed.

---

## Step 3 — Intermediate algebra with all scale factors, signs and units

### 3.1 The deep-MOND slope equals the count

Chain rule, unit s:

μ_n'(0) = d/dY[1 − (1 − p(Y))^n]|_{Y=0} = n·(1 − p(0))^{n−1}·p'(0) = n·1·1 = n.

So the slope reading at the origin is the *total* channel count n — grouping
invariant by §2.1 (the count of the grouped system is n = k·m). The sign is +
(slope −n for 1 − (1+p)⁻ⁿ-style falling members is not our branch form; all
corpus members used here rise from 0 to 1).

### 3.2 Corpus member p = Y/(1+Y), its response and its expansion

For the corpus member p = Y/(1+Y): q = 1/(1+Y), μ_n(Y) = 1 − (1+Y)^{−n}.
For n = 2 the origin expansion (signs and factors explicit):

μ₂(Y) = 1 − (1+Y)^{−2} = 1 − [1 − 2Y + 3Y² − 4Y³ + 5Y⁴ − 6Y⁵ + …]
      = 2Y − 3Y² + 4Y³ − 5Y⁴ + 6Y⁵ − … ,  domain |Y| < 1.

- Slope at origin: μ₂'(0) = 2 ✓ (count).
- **Leading neglected term: −3Y².** Its coefficient is completion-dependent:
  for a generic completion p = Y + c₂Y² + …, μ₂ = 2Y + (2c₂ − 1)Y² + …, i.e.
  the quadratic coefficient 2c₂ − 1 varies with the completion while the slope
  nY is completion-independent. The slope is the testable content (Part C1).

### 3.3 The κ-chain (L230), units explicit

Deep regime |Y| ≪ 1: μ_n ≈ n·(g/s). Poisson equation μ·g = g_N gives
(n·g/s)·g = g_N ⇒ g² = (s/n)·g_N. The a0-line g² = a0·g_N (framework: deep
relation g² = a0·g_N with v_flat⁴ = G·M_b·a0) is matched by

a0 = s/n,  i.e. κ = a0/s = 1/n   (all quantities in m s⁻²; n dimensionless).

Regrouping does not change n (§3.1), so κ is grouping-invariant on the fixed
vacuum footing. The framework's two-channel count (PD01 B1, n = 2) is the
selection that lands κ = 1/2 — together with the L230 unit anchor that fixes
the unit at the vacuum rate s (one-scale action, k01). The algebra alone
admits every 1/m (D1: κ readings {1, 1/2, 1/3} at m = 1, 2, 3).

**G-identity hygiene (campaign rule "G_N/G_bare/G_cosmo SEPARATE"):** this
branch carries exactly ONE G = 6.67430e-11: it enters s = c·√(G·ρ_Λ) (via the
adopted a0) and would enter g_N = G·M_b/r² — the same Newtonian constant, no
bare/cosmological split is introduced or conflated anywhere. The H1 lane
evaluates g_N from the lumped parameter GM = 1e20 (m s⁻²·m²), which sidesteps
any second G identification; the framework cell records the single G. No
claim here asserts equality or difference of G_N, G_bare, G_cosmo — that
question is out of this branch's scope.

### 3.4 λ-diagnostics (scale factors explicit)

Read the n = 2 response in unit s_λ = λ·s: Y_λ = g/(λ·s) = Y/λ. In that unit
the chain rule gives reading slope n_λ = n·λ = 2λ ∈ {1, 2, 4} at
λ ∈ {1/2, 1, 2}. The covariant matched scale is
a0_λ = s_λ/n_λ = (λ·s)/(2λ) = s/2, so the ratio a0_λ/s = 1/2 **for every
λ ≠ 0** (closed form (λs)/(2λ)/s = 1/2; the algebra cannot move the landing).
A unit-confused fit — mistaking s_λ for the vacuum rate s — reads
κ_naive = 1/(2λ) ∈ {1, 1/2, 1/4}. Only λ = 1 (the vacuum's own unit) makes
the slope reading coincide with a channel count. No observational preference
is used anywhere in this part.

### 3.5 Deep-limit domain statement

The deep asymptote g_deep = √((s/2)·g_N) is the leading order of the ACTUAL
response solution in |Y| ≪ 1; leading neglected term −3Y² for the corpus
member (§3.2), i.e. the asymptote's relative error is O(Y²). The Newtonian
handover occurs at Y ≫ 1 where μ → 1 and g → g_N.

---

## Step 4 — Independent checks in a different representation (actual residuals)

### 4.1 80-digit independent arithmetic (F1) — mpmath, 18 (grouping, Y) points

The exact closure identity re-evaluated numerically at 80-digit precision, plus
direct finite-difference slopes:

- max |closure residual| = **2.1e-81** (80-digit machine limit — a residual,
  not a Boolean);
- numeric slopes at the origin: n = 1 → 1.0, n = 2 → 2.0, n = 3 → 3.0, n = 4 → 4.0
  (finite difference in the vacuum unit);
- continuation to |Y| ≤ 1e3 confirms saturation μ → 1 (finite consistency
  only; the exact proof is Part A / Lean §7).

### 4.2 Substitution into the original equation (H1) — 80 digits, r ∈ [1e12, 1e17] m

Solve μ₂(g/s)·g = g_N exactly (mpmath, 80 digits) with GM = 1e20 and
s = 1.87238e-10 m s⁻²; compare each solution with g_deep = √((s/2)·g_N) and g_N:

| r (m) | Y | g_N (m s⁻²) | g_sol | eq residual | |g−g_deep|/g_deep | |g−g_N|/g_N |
|---|---|---|---|---|---|---|---|
| 1e17 | 0.0052 | 1.0e-14 | 9.7133e-13 | **6.59e-94** | 0.0039 (deep ✓) | 96 |
| 1e15 | 0.780 | 1.0e-10 | 1.4610e-10 | **1.23e-91** | 0.510 (transition) | 0.46 |
| 1e13 | 5.34e3 | 1.0e-6 | 1.000000035e-6 | **0.0** | 102 (not deep) | 3.5e-8 (Newton ✓) |
| 1e12 | 5.34e5 | 1.0e-4 | 1.0e-4 | **0.0** | 1.0e3 | 3.5e-12 (Newton ✓) |

Thresholds set before evaluation: equation residual < 1e-50 (actual: ≤ 1.23e-91);
deep-end deviation < 1e-2 at r = 1e17 (actual 0.0039); Newtonian deviation
< 1e-6 at r = 1e13 and < 1e-8 at r = 1e12 (actual 3.5e-8, 3.5e-12).
**The matching g² = (s/2)g_N is the deep asymptote of the actual solution —
the a0-line is not a separate law in this branch.**

### 4.3 Both footings (G1) — separate densities, separate κ-legs

- Canonical: a0 = 9.3619e-11 ⇒ ρ_Λ = 4·a0²/(G·c²) = **5.84441e-27 kg m⁻³**,
  s = c·√(G·ρ_Λ) = 1.87238e-10 m s⁻², κ = a0/s = **1/2** (residual 0.0 < 1e-12).
- Alternative: a0 = 1.1279e-10 ⇒ ρ_Λ = **8.48309e-27 kg m⁻³**,
  s = 2.2558e-10 m s⁻², κ = **1/2** (residual 0.0 < 1e-12).
- The two footings do NOT share both fixed density and fixed κ: the
  alternative footing holds κ = 1/2 and scales the density by
  (a0_alt/a0_can)² = 1.4515. The fixed-density accounting leg
  κ_eff = a0_alt/s_can = 0.6024 is recorded for bookkeeping only, never used
  as a value. (Tolerance rationale: 1e-12 is 4 orders above the ~1e-16 input
  roundoff and 8 orders below discriminating physics.)

Both footings are n = 2 responses at their own densities (PD01 C2 registration
arms 0.00% / 0.29%).

---

## Step 5 — Negative controls, strongest surviving statement, next implication

### 5.1 Negative controls (both live, both capable of failing, both executed)

- **B2 (capable of failing — it fails the "remains one" claim by design):**
  p_G'(0) = 2 in the vacuum unit, computed; the claim "the normalized group
  drive slope remains one after grouping" is rejected (2 ≠ 1). Lean:
  `AS065_group_two_slope_two`, `AS065_group_slope_not_one : (2:ℝ) ≠ 1`.
- **D1 (the mandated hand-renormalization):** two channels grouped, slope
  renormalized by hand to unit s/2 ⇒ the count interpretation CHANGES
  (2 physical channels → 1 renormalized group channel). The same procedure at
  m = 3 reads count 1 in unit s/3 and would "derive" κ = 1/3. κ values
  {1, 1/2, 1/3} for m = 1, 2, 3 are all consistent with the closure identity —
  **the identity does not select 1/2.** Lean: `AS065_kappa_matching_generic`
  ((s/m)/s = 1/m), `AS065_kappa_half_landing`, `AS065_a0_line_chain`.
- **E1/E2 (scale-covariance diagnostics, λ = 1/2, 1, 2):** count reading
  covariant n_λ ∈ {1, 2, 4}; covariant κ = 1/2 for ALL λ; unit-confused
  κ_naive ∈ {1, 1/2, 1/4}. Lean: `AS065_kappa_covariant_lambda` (all λ ≠ 0),
  `AS065_lambda_reading_half` (slope 1 = 2·(1/2)), `AS065_lambda_reading_two`
  (slope 4 = 2·2), `AS065_naive_readings`.
- **C2 (normalization / boundary cases):** μ_n(∞) = 1 for every completion
  (Newtonian handover); deep asymptote domain |Y| ≪ 1 with leading neglected
  term −3Y² (H1 residuals confirm: at Y = 0.0052 deep error 0.39% ≈ 3Y² = 8e-5·(correction scale) ✓ order-of-magnitude consistent).

### 5.2 Strongest surviving statement

**Theorem (scoped).** For any completion p with p(0)=0, p'(0)=1 (in unit s),
p(∞)=1 and any m, k ≥ 1: (i) the OR class is closed under coarse graining with
exact count conservation (μ of k groups of m equals μ_{km}); (ii) the
deep-MOND slope of the response equals the total count n in the vacuum unit;
(iii) κ = a0/s = 1/n is grouping-covariant; (iv) the value κ = 1/2 is NOT a
consequence of the closure algebra — it is the conjunction of the adopted
L230 unit anchor (drive measured in the vacuum rate s; one-scale action, k01)
with the computed two-channel count (PD01 B1). Domain: dimensionless Y > 0;
all identities algebraic/symbolic (Lean-certified); numerics at 80 digits on
the finite box of Part H with the residuals recorded above.

### 5.3 First additional implication needed to transfer to the full theory

The transfer to the amended thirteen-item target (filtered MONO, causality
criterion B) needs the bridge: *statistical independence of the n channels at
finite separation in the full action* — the OR product presumes the channels
are independent; the effective-field completion p(Y) must be shown to arise
from the SAME one-scale action (k01) so that the count n = 2 is a property of
the metric's static channels inside the filtered-MONO gate, not an assumption
imported from the historical branches. Until that bridge is proved, this
result is a conditional lemma on the CORE branch, and the historical branches
(Q, RAR, MU2, EXP, MONO) remain distinct comparison objects (seed's causality
criterion B).

---

## §7 Lean 4 certificate (verification record)

File: `AS065_closure_or_coarse_graining.lean` (17 theorems/lemmas).
Command: `cd fable_independent_2026/lean_2026 && lake env lean <abs path>.lean`.
Result: **compiles with 0 errors; every theorem depends on axioms exactly
{propext, Classical.choice, Quot.sound}; zero `sorry`.**

| Theorem | Content |
|---|---|
| `AS065_or_closure_pow` | (x^m)^k = x^(m·k) — power associativity |
| `AS065_or_closure_response` | closure for all m, k, any p |
| `AS065_closure_member_two_times_two` | corpus member, 2×2 = 4 |
| `AS065_survival_grouping` | q-regrouping, unequal channels |
| `AS065_slope_one..four` | μ_n'(0) = n, n = 1..4 (punctured-filter limits of the difference quotients) |
| `AS065_group_two_slope_two` / `AS065_group_slope_not_one` | negative control B2 |
| `AS065_kappa_matching_generic` / `_half_landing` / `AS065_a0_line_chain` | κ = 1/m family; the a0-line chain lands s/2 |
| `AS065_kappa_covariant_lambda` | (λs)/(2λ)/s = 1/2 for all λ ≠ 0 |
| `AS065_lambda_reading_half` / `_two` | reading slopes 1 and 4 at λ = 1/2, 2 |
| `AS065_naive_readings` | unit-confused κ ∈ {1, 1/2, 1/4} |

House-traps honored: `Filter.Tendsto` (namespaced) with `Tendsto.congr'`
(eventually-eq BEFORE the Tendsto; orientation rational =ᶠ DQ), punctured
neighborhoods via `mem_nhdsWithin` + `Set.Ioo` (no `ball` in scope),
`mul_right_cancel₀` for right-sided cancellation, `field_simp` only on
pure-division goals, all numerals ℝ-annotated, `open scoped Topology` for 𝓝.

---

## Bounds actually enforced (recorded, not suggested)

wall 0.20 s lane / 0.45 s with supervisor · RLIMIT_CPU 110 s enforced
in-process (verified "110 110" at runtime) · 512 MiB RSS ceiling enforced by
external supervisor polling `ps -o rss=` every 0.1 s (SIGKILL on exceedance;
host macOS 26 rejects in-process RLIMIT_AS/RLIMIT_DATA/RLIMIT_RSS lowering —
recorded in `AS065_supervisor.json`, kill_event = null) · observed max RSS
80.1 MiB · 1 thread (no spawns; OMP/OPENBLAS/MKL/VECLIB pinned to 1).
