# AS054 — Channel-composition nonuniqueness: derivation

**Run:** `run_20260928T0803` · **Task file hash:** `7b2c007adcd8ba72edd386411a5c1529236e5e6b44882c2bb86f12fb60aa6726` (verified at start)
**Branch cell:** CORE coefficient; conditional MU_n statistical response algebra. No Q/RAR/MU2/EXP/MONO branch translation is performed; the operative thirteen-item target (filtered MONO, criterion B) is never touched.
**Compute:** `compute_AS054_channel_composition.py` (18/18 checks, bounded: 0.34 s wall, 57.9 MiB peak RSS, 1 thread — see §7).
**Certificate:** `AS054_channel_composition_certificates.lean` — compiles; all ten theorems depend only on `{propext, Classical.choice, Quot.sound}` (see `lean_check.out`).

---

## 1. Objects, boundary conditions, assumptions (step 1)

Framework base (adopted inputs, not derived here): `a0 = kappa*c*sqrt(G*rho_Lambda)` with **kappa = 1/2 ADOPTED**; mass density `rho_Lambda`; `s = c*sqrt(G*rho_L)`, `Y = g/s`; `r_M = sqrt(G*M_b/a0)`; `v_flat^4 = G*M_b*a0`. Constants: `G = 6.67430e-11 m^3 kg^-1 s^-2`, `c = 299792458 m/s`, `M_sun = 1.98847e30 kg`, `pc = 3.085677581491367e16 m`. `G_N`, `G_bare`, `G_cosmo` are separate symbols; no relation between them is used or derived here.

**Per-channel engagement** `p(Y)` (drive `Y = g/s` dimensionless): `p : [0,oo) -> [0,1]` with

- BC1 `p(0) = 0` (zero drive, zero engagement — the action's frozen vacuum),
- BC2 `p'(0) = 1` (the **s-units fraction identity**: engagement fraction = drive fraction; no second scale exists in the one-scale action — k01 zero-mode theorem, cited),
- BC3 `p(Y) -> 1` as `Y -> oo` (channel saturation),
- BC4 `p' > 0` on `(0,oo)` (monotone engagement).

**Compositions** (the object of the task): over two channels with engagement `p`,
`mu_OR = 1 - (1-p)^2` (OR: response engaged if at least one channel engages; PD01/PD08's family) and `mu_avg = (p+p)/2 = p` (equal-weight average of the two channel responses). `mu_lam = 1 - (1-p)^lam`, `lam > 0`, the real-exponent family of the same OR form.

**Assumptions (stated as premises, not derived here):**
- A-OR: the response is the OR composition (PD01 D1's OR-identification; PD08 Step 4's chain rule).
- A-eq-slope: every channel obeys BC1–BC3 with unit slope (PD08 Steps 1–3).
- The carrier identification (the linearized metric's *two* static Poisson channels, PD01 B1, computed to 2e-14) is cited as context for the physical count; no claim about it is made or needed by the algebra below.

**Claim under test (the control claim C0):** *"saturation alone (µ(∞) = 1 under BC1–BC3) uniquely selects the OR response."*

**Boundary conditions:** `Y in (0,oo)`; symbolic `n >= 1`; diagnostic slopes `lam in {1/2, 1, 2}` per the task. Both footings separately (canonical `a0 = 9.3619e-11`, alternative `a0 = 1.1279e-10 m/s^2`); the two footings cannot share both a fixed `rho_Lambda` and a fixed kappa.

## 2. Positivity, monotonicity, exact separation (step 2)

For every completion in the class (verified symbolically for the three corpus members `p = y/(1+y)`, `p = 1-exp(-y)`, `p = tanh(y)`, and generically by algebra):

1. **Separation is exact and completion-independent.** `mu_OR - mu_avg = p - p^2 = p(1-p)` identically (S2.1: sympy residual 0 for all three completions). Under BC2–BC4, `0 < p(Y) < 1` for `Y in (0,oo)`, hence `mu_OR(Y) > mu_avg(Y)` pointwise on the whole deep/intermediate domain; the two compositions are different functions for *every* completion (they coincide only at `Y = 0` and in the limit `Y -> oo`).
2. **Monotonicity:** with BC4 both compositions are strictly increasing (`mu_OR' = 2p'(1-p) > 0`, `mu_avg' = p' > 0`). Positivity: `mu_OR, mu_avg in (0,1)`.
3. **Both saturate:** `mu_OR(oo) = mu_avg(oo) = 1` for every completion (S2.3, exact limits).

**Physical principle that would distinguish the compositions:** the deep-MOND zero point — the slope `µ'(0)` maps to `kappa = 1/µ'(0)` through the a0-line (section 3), so the measured `kappa` band (PD01 C1's instruments, cited as measurements, not used as proof) distinguishes the count class {1, 2}. No registered principle distinguishes the two compositions *within* a fixed slope class (e.g., the shape/completion); that distinguisher is **open** (section 8).

## 3. Intermediate algebra with scale factors, signs, units (step 3)

### 3.1 Origin slopes and the generic 2-jet

Generic completion jet `p(Y) = Y + c2 Y^2 + O(Y^3)` (c2 = unknown completion coefficient; PD08 Step 4's c2):

```
mu_OR  = 2Y + (2c2-1)Y^2 - 2c2 Y^3 - c2^2 Y^4                       (exact expansion)
mu_avg = Y + c2 Y^2
mu_lam = lam*Y + (c2*lam - lam*(lam-1)/2) Y^2 + O(Y^3)              (real exponent)
mu_OR - mu_avg = Y + (c2-1)Y^2 - 2c2 Y^3 - c2^2 Y^4
```

(Clarification of the record: the quadratic coefficient of `mu_OR` on this jet is `(2c2 - 1)`, not `(2c2 + 1)`; the *linear* coefficient 2 is c2-independent — that is the content of PD01 A1's completion-independence.) The Lean theorem `or_slope_jet` certifies the exact identity; `slope_gap_jet` the gap identity. **The linear coefficients 2 and 1 are independent of the completion; the shape is not.**

### 3.2 The L230 chain with units (the a0-line, kappa = 1/lam)

Deep-MOND Poisson equation with the truncated response `mu ~ lam*Y = lam*g/s`, spherical point source, all quantities positive (radial acceleration magnitudes; no sign ambiguity in this truncated identity):

```
(1/r^2) d/dr [ r^2 mu(Y) g ] = 4 pi G rho_b            [m/s^2 · 1/m^2 · m^2 = m/s^2 ✓]
   =>  lam*(g/s)*g = G M_b/r^2 = g_N
   =>  g^2 = (s/lam) g_N
```

Matching the deep a0-line `g^2 = a0 g_N`:  `a0 = s/lam`,  `kappa = a0/s = 1/lam`.  Units: `[g^2] = m^2/s^4 = [s]*[g_N]` ✓. Substitution residual: identically 0 (symbolic; numeric 0.0 to 60 digits at all sampled radii). Therefore:

- `lam = 2` ⇔ `kappa = 1/2` (the framework footing), `lam = 1` ⇔ `kappa = 1` (PD01's scalar count), `lam = 1/2` ⇔ `kappa = 2`.

### 3.3 Leading neglected term and its domain

For the corpus completion `p = Y/(1+Y)`:

```
mu_lam - lam*Y = -(lam*(lam+1)/2) Y^2 + (lam*(lam+1)*(lam+2)/6) Y^3 + O(Y^4)
```

For generic `p = Y + c2 Y^2 + ...`: `mu_lam - lam*Y = (lam*c2 - lam*(lam-1)/2) Y^2 + O(Y^3)` — the coefficient is completion-dependent at second order. **Domain of the lambda-line matching:** `Y << 1` with relative error `|(mu_lam - lam Y)/(lam Y)| = |c2 - (lam-1)/2|·Y + O(Y^2)`; the a0-line is an *asymptotic* statement of the truncated equation, exact only at `Y -> 0`.

## 4. Independent checks (step 4; different representations, actual residuals)

All thresholds pre-set before evaluation. mpmath at 60 digits.

| Check | What was done | Measured | Threshold | Verdict |
|---|---|---|---|---|
| S4.1 | `(mu(h)-mu(0))/h` at `h=1e-24`, 3 completions × {OR, avg}: direct numerical differentiation vs exact slopes 2, 1 | max rel. residual **1.50e-24** | 1e-18 | PASS |
| S4.2a | `1 - mu(Y)` at `Y = 1e6, 1e60`, both compositions × 3 completions: saturation residual | max **1.24e-60** at 1e60 | 1e-40 | PASS |
| S4.2b | saturation-rate ratio `(1-mu(2Y))/(1-mu(Y))`: corpus 0.250000 (algebraic 1/Y² tail), exp 1.125e-07, tanh 1.266e-14 (exponential tails) | as listed | <1e-2 | PASS |
| S4.3 | `mu_OR - mu_avg` vs `p(1-p)` at `Y = 0.3, 1, 3` × 3 completions | max **4.67e-61** | 1e-40 | PASS |
| S4.4 | both footings separately at 60 digits: κ_can = 0.5 exactly, κ_alt = 0.5 exactly; fixed-ρ relabeling κ_eff = 0.6023884041 → λ_eff = 1.6600585 (non-integer) | as listed | exact + 1e-6 | PASS |
| S4.5 | deep a0-line: at r = 50–1000 kpc, M_b = 1e11 M_sun (Y in [6e-3, 0.122], r_M ≈ 3.9 kpc), full OR-response solution vs λ-line: relative deviation **9.78e-2 → 4.59e-3**, truncated identity residual 0 to 60 digits | as listed | < 0.2, <1e-40 | PASS |
| S4.6 | unequal-channel OR witness `1-(1-p)(1-q)`, q = tanh: slope 2, saturates, but `mu_uneq - mu_OR = 1.308e-01` at Y = 1 | 1.308e-01 | >1e-3 | PASS |

Domain statement: all symbolic identities hold for `Y in (0,oo)`, `lam > 0`, `c2 in R`, `n >= 1`; numerical grids above; pc-scale radius points (Y >> 1) were explicitly rejected as outside the a0-line domain.

## 5. Negative controls (step 5; capable of failing)

**NC1 — "saturation alone uniquely selects the OR response": REFUTED.** The control is capable of failing (if `mu_avg` did not saturate, the claim would survive) and it fires: `mu_avg` *does* saturate at 1 for every completion (S2.3) yet is not the OR response (S2.1–S2.2: `mu_OR - mu_avg = p(1-p) ≠ 0` on `(0,oo)`, slopes 2 vs 1). `mu_avg = (p+p)/2` is the explicit counterexample. The OR identification is therefore a **genuinely independent input** (PD01 D1 raised to an explicit condition), exactly as the task's principle states.

**NC2 — saturation + slope determine only the real exponent, not a count.** The family `mu_lam = 1-(1-p)^lam` realizes every diagnostic slope with saturation: at `lam = 1/2` (κ = 2; no integer-channel realization exists), `lam = 1` (κ = 1; `mu_avg ≡ mu_1 = 1-(1-p)^1` — the average-of-two and the one-channel OR are the *same function*, an exact degeneracy), `lam = 2` (κ = 1/2; the framework footing, reproduced also by any two unit-slope channels, equal or not — S4.6). Numerics: max residual 1.50e-24 (threshold 1e-18/1e-40). The fixed-ρ relabeling λ_eff = 1.6601 is a further non-integer diagnostic: the algebra cannot prefer the integer readings.

## 6. Strongest surviving statement

**Theorem (nonuniqueness classification).** Let `p` satisfy BC1–BC4. Then:

(a) **Saturation does not select the composition:** both `mu_OR` and `mu_avg` satisfy `mu(0)=0`, `mu(oo)=1`, and the constraint set {BC1–BC3} admits infinitely many unrelated compositions (verified: `mu_OR - mu_avg = p(1-p) > 0` on `(0,oo)`, exact and completion-independent).

(b) **Saturation + slope select only the real exponent:** the pair (µ(∞) = 1, µ'(0) = λ) fixes `lam = lambda` and `kappa = 1/lambda` via the L230 chain — but every λ in (0,∞) is realized by a saturating composition (µ_λ and, for λ = 2, by unequal-channel ORs, S4.6). In particular λ = 2 does not imply "two equal channels": it implies an OR-2 class with a free shape and, without A-OR, any saturating composition of slope 2.

(c) **The count is an input, not an output of the algebra:** `kappa = 1/2` (λ = 2) is the framework's adopted coefficient; it survives as *derived* only under the conjunction {A-OR, A-eq-slope, carrier count = 2 (PD01 B1)}. This adds one explicitly unlisted premise (A-OR, and its equal-channel reading) to PD01/PD08's chain: the "OR-exclusion by normalization" argument (PD01 A3) excludes only the *sum* of channel-shares, not the average or any other saturating composition.

**Lean-certified component identities** (zero sorry; axioms ⊆ {propext, Classical.choice, Quot.sound}): exact separation `or_avg_difference` + strict positivity `or_avg_separated`; completion-independent jets `or_slope_jet` (coefficient 2), `avg_slope_jet` (coefficient 1), `slope_gap_jet`, `unequal_or_slope_jet`; saturation of both compositions in ε-M form `sat_avg_cleared`, `sat_or_cleared` (cleared polynomial form, equivalent to `|1-µ| < ε` given `1+Y > 0`); fractional member `frac_family_sq`, `frac_family_pos`.

## 7. Execution bounds (actually enforced)

- **Wall time:** deadline checkpoints at every section; measured **0.34 s** (declared ≤120 s). Enforced.
- **Memory:** RLIMIT_AS = 512 MiB attempted — **not effective on this host** (macOS; `setrlimit` raised "current limit exceeds maximum limit"; a 900 MiB probe allocation succeeded, proving non-enforcement). The measured compute peak RSS is **57.9 MiB** — the *observed* usage, well under the declared target. Honest record: wall time and thread count are the hard-enforced bounds; memory is declared + measured, not OS-enforced.
- **Threads:** 1 (single process, pure sympy/mpmath, no threading/process primitives). Enforced by construction.
- Lean compiles are outside the 120 s prototype bound (they are the certificate step).

## 8. What this result does and does not establish

**Does:** refutes the saturation-uniqueness claim with an explicit counterexample (µ_avg) and an exact classification (saturation+slope ⇒ real exponent only); restates PD01 A1–A4's core algebra with two explicit premises (A-OR, A-eq-slope) and shows the OR-identification cannot be *derived* from the normalization — it must be supplied or obtained from the carrier structure; produces actual residuals (60-digit) for every identity; certifies the algebra in Lean.

**Does not:** does not derive the OR identification, the equal-engagement premise, or the completion shape from the action; does not touch the operative filtered MONO branch or criterion B (branch isolation respected); makes no empirical claim (PD01 C1/C2's data are cited only as the physical-identification context); does not transfer to nonspherical fields (the L230 chain is spherical deep-asymptotic); the two Poincaré channels of PD01 B1 are not rederived here (source cited, hash-verified).

## 9. First additional implication needed to transfer to the full theory

To transfer the coefficient to the operative target (requirement 13's a0–vacuum cell, filtered-MONO gate): the **equal-engagement premise for the metric's two static Poincaré channels must be derived from the action (or refuted with a no-go)**. PD01 B1 counts the two channels; nothing in the counted-algebra forces their per-channel responses to coincide beyond the universal unit slope at the origin (which ± the OR form already fixes λ = 2). Concretely: prove or disprove that the 00-sector load (2 ΔΨ) and the spatial-trace load (2 Δ(Φ−Ψ)) of the linearized metric imply identical response functions at *finite* Y — i.e., whether unequal-channel ORs (µ_uneq family, this run S4.6) are excluded by the static sector's equations. An explicit negative would leave the full response shape and the completion freedom as the residual empirical input; a positive would close PD08's chain at the shape level.

## 10. Both footings

The composition theorem is dimensionless; its application to both footings: canonical footing `a0 = 9.3619e-11 m/s²` ⇔ `rho_Lambda = 5.844412454e-27 kg/m³`, `s = 1.87238e-10 m/s²`, λ = 2, κ = 1/2 (exact); alternative footing `a0 = 1.1279e-10 m/s²` ⇔ `rho_alt = 8.483089620e-27 kg/m³`, `s_alt = 2.2558e-10 m/s²`, λ = 2, κ = 1/2 (exact). The two footings cannot share fixed density and fixed kappa: holding ρ_Lambda fixed forces κ_eff = 0.6023884041 (λ_eff = 1.6601, non-integer diagnostic — a re-labeling, not a measurement), in agreement with AS001's recorded κ_eff.

## 11. Sources inspected (hash-verified against SOURCE_MANIFEST.json)

| Source | Pinned/actual SHA-256 | Status |
|---|---|---|
| `deepseek_push/PD01_polarization_count.py` | `37e39d1abb8dfe74763e59282b6137ed6a6b570215da415d197de72c33e2c74d` | match |
| `deepseek_push/PD08_particle_free_derivation.py` | `83f6054cdfb1b45834af1ce702b1a040f00ad1625ffc34799ae367bd367f0cfb` | match |
| `kappa_closure/k01_zero_mode_theorem_and_lambda_free_vacuum.py` | `8df5a3ab5a38d189e0152ab0e54c0fb497056e58373cc0e80db49fca3f35b25c` | match |

The k01 outcome (no second scale in the action; normalisation zero mode for the action as written) is used only to support BC2's status as the one-scale fraction identity; kappa = 1/2 remains ADOPTED in this run (as the task mandates) and is not claimed derived here.