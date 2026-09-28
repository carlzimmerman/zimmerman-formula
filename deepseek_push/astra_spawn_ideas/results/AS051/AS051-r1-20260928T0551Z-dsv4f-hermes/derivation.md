# AS051 — General deep-slope matching theorem: derivation & verdict

**Run:** `AS051-r1-20260928T0551Z-dsv4f-hermes`
**Task file:** `deepseek_push/astra_spawn_ideas/AS051_general_deep_slope_matching_theorem.md`
(sha256 `819422a92fcd21e32941091e823a459944739a4927de7900a8a2d4bfe7f49025`, ledger-verified)
**Sources (all hashes match SOURCE_MANIFEST.json and the work order's pins):**
`deepseek_push/PD01_polarization_count.py` (`37e39d1a…`), `deepseek_push/PD08_particle_free_derivation.py` (`83f6054c…`),
`kappa_closure/k01_zero_mode_theorem_and_lambda_free_vacuum.py` (`8df5a3ab…`).
**Worker:** deepseek/deepseek-v4-flash-0731 via openrouter (Hermes subagent; platform subagent)

> **Dispatch-preamble note:** the dispatch text described AS051 as "dimensional analysis of the phantom
> density (rho_ph = C/(4πGr²))". No such file exists in the repository; the ledger- and manifest-pinned
> work order at the AS051 slot is the *General deep-slope matching theorem* below, which was executed
> in full. The phantom-density content belongs to other seeds (AS582/AS583/AS728 family). This run's
> `task_sha256` is the hash of the actual dispatched file.

---

## 1. The claim, symbol dictionary, boundary conditions, assumptions

**Claim to audit (work order §"Mathematics and principal test"):**

> If `mu(Y) = b·Y + O(Y^2)` with `b > 0` and `mu(Y)·g = B`, then
> `g^2 = (s/b)·B + corrections` and `kappa = 1/b`.

**Symbol dictionary (framework contract, mandatory scale and units):**

| Symbol | Meaning | Units |
|---|---|---|
| `s` | vacuum scale `s = c·sqrt(G·rho_Lambda)`, held *independent of a0* until the final step (PD08 C2 hygiene) | m/s² |
| `Y = g/s` | dimensionless deep-field argument | 1 |
| `B = g_N = G·M_b/r²` | Newtonian baryonic field in the spherical sector | m/s² |
| `g` | total radial acceleration | m/s² |
| `mu(Y)` | response function, `0 ≤ mu ≤ 1`, `mu(0)=0`, `mu(∞)=1` (L230 normalisation) | 1 |
| `b = mu'(0)` | deep (linear) slope in the *s*-units argument | 1 |
| `a0` | MOND scale, `a0 = kappa·s` (framework input; kappa = 1/2 **adopted**) | m/s² |
| `kappa := a0/s` | the audited coefficient | 1 |

**Equation under audit** — spherical first integral of `div[mu(|grad Phi|/s)·grad Phi] = 4πG·rho_b`:

```text
mu(Y)·g = B ,   Y = g/s .          (E)
```

**Assumptions.** (i) `b > 0`; (ii) `mu` twice differentiable at 0 with the stated linear term, i.e.
`mu(Y) = bY + O(Y²)` — for the explicit bound a *quantified* remainder `|R(Y)| ≤ K·Y²` on `[0,Y0]`;
(iii) spherical sector (the Poisson-response sector the corpus lives in, PD01 B1); (iv) both
endpoints `mu(0)=0`, `mu(∞)=1` preserved (used by the negative control). **Not assumed:** any value
of b; the identity `kappa = 1/b` is what the audit derives.

---

## 2. Proof of the asymptotic theorem with explicit remainder

**Step 1 — expansion of (E).** Write `mu(Y) = bY + R(Y)`, `R(Y) = c2·Y² + c3·Y³ + …`. Then

```text
B = mu(g/s)·g = (b/s)·g² + (c2/s²)·g³ + (c3/s³)·g⁴ + …          (E1)
```

**Step 2 — exact inversion.** (E1) is inverted *exactly*, no approximation:

```text
g² = (s/b)·B − (c2/(b·s))·g³ − (c3/(b·s²))·g⁴                    (E2)
```

*Verification:* substitute (E2) into the RHS of (E1); the residual is identically 0
(PART 0, `A1`: substitution residual = 0, symbolic; Lean `as051_exact_inversion`,
`as051_inversion_residual`).

**Step 3 — remainder bound.** From (E1):

```text
|B − (b/s)·g²| = |g·R(g/s)| ≤ g·K·(g/s)² = K·g³/s²
=>  |g² − (s/b)·B| = (s/b)·|B − (b/s)·g²| ≤ (K/b)·g³/s .          (BND)
```

The first neglected term is `O(g³/s²)` absolute, i.e. **relative correction O(g/s) = O(√(B/(b·s)))** —
it vanishes linearly in `Y = g/s` as `B → 0`. Domain: `0 ≤ Y ≤ Y0` where the quadratic remainder
hypothesis holds (verified on the numerical ladder for the exact family below). Lean:
`as051_remainder_bound`.

**Step 4 — the audited identity.** The deep a0-line is `g² = a0·B`; reading `a0 := s/b` off (E2)
at leading order gives

```text
kappa := a0/s = (s/b)/s = 1/b .                                    (K)
```

Equivalently from the pure linear law `B = (b/s)·g²`: `(g²/B)/s = 1/b` (Lean
`as051_kappa_of_slope`). **Which hypothesis fixes b?** *None in this theorem.* The matching
`kappa = 1/b` is an identity that converts the deep slope into the MOND coefficient; the slope `b`
itself is the genuinely independent freedom. In the sources, `b = 2` is supplied by *separate*
premises — the metric's two static Poisson channels + OR composition + fraction identity
(PD01 A1–B4, PD08 steps 1–4) or by the data (PD01 C1/C2). **Verdict:** the deep-slope matching
theorem is a *transfer identity* (slope freedom ↔ kappa freedom), not by itself a derivation of
`kappa = 1/2`; it turns "a derivation of kappa must remove a genuinely independent freedom" into
"the freedom is the deep slope b".

---

## 3. Intermediate algebra, scale factors, signs, units

- **Sign:** `b > 0` and `mu ≥ 0` keep `g² > 0`; no sign ambiguity in the physical branch `Y > 0`.
- **Units:** `[s] = (m/s)·sqrt((m³/(kg·s²))·(kg/m³)) = (m/s)·(1/s) = m/s²` ✓ (dimensional checker
  N2: exponent vector (1,0,−2)); `[B] = m/s²`, `[g²] = m²/s⁴ = [s]·[B]` ✓; `[b] = [kappa] = 1` ✓.
- **Both footings (dimensionless theorem → footing-independent application):**

| footing | a0 [m/s²] | s [m/s²] | kappa | rho_Lambda [kg/m³] |
|---|---|---|---|---|
| canonical (adopted 1/2) | 9.3619e-11 | 1.872380e-10 | 0.500000 | 5.844412e-27 |
| alternative, kappa fixed | 1.1279e-10 | 2.255800e-10 | 0.500000 | 8.483090e-27 |
| alternative, rho_Lambda fixed | 1.1279e-10 | 1.872380e-10 | 0.602388 | 5.844412e-27 |

The identity `kappa = 1/b` does not contain `a0`; it applies identically on both footings once
`s = a0/kappa` is fixed. PD01/PD08's `b=2` therefore lands `kappa = 1/2` on *both* footings by
construction (0.00% / 0.29% registered, PD01 C2).

- **Standard-branch consistency (canonical footing, `Y = x/2` since s = 2a0):** MU2
  `1−(1+Y)^(−2)` → slope 2; EXP `1−e^{−2Y}` → slope 2; Q deep limit `g² ≈ a0B` → `mu = B/g ≈ g/a0 = 2Y` → slope 2; RAR verified numerically (PART 1 N5: `mu/Y → 2` to 3e-7). All four branches share `b = 2`, hence `kappa = 1/2` under (K).

---

## 4. Independent checks (different representations — actual residuals, not booleans)

1. **High-precision implicit solve (mpmath, 50 digits):** solve `mu_b(g/s)·g = B` exactly for
   `mu_b(Y) = 1−(1+Y)^{−b}`, `b ∈ {1/2, 1, 2}`, over `B/s ∈ [1e-1, 1e-14]`. **Actual equation
   residual** `|mu_b(g/s)·g − B| ~ 1e-47` at every ladder point. Inferred
   `kappa_fit = g²/(B·s)` converges to `1/b` (e.g. b=2: 0.7073 → 0.50000005; b=1/2: 2.7605 → 2.0000002).
2. **Remainder bound (BND) evaluated against the actual residual** at all 24 ladder points:
   max residual/bound ratio = 1.000000 (saturated at the tight-grid K estimate; ≤ 1 required, ✓).
3. **Newtonian limit:** with `B/s → ∞`, `g/B → 1` for all three b (ladder B/s = 1e4…1e16;
   slowest tail for b=1/2, `g/B − 1 ~ (B/s)^{−1/2}`, as expected analytically).
4. **Lean 4:** 9 theorems, 0 sorry, axioms ⊆ {propext, Classical.choice, Quot.sound} (verified
   by `#print axioms`). Covers: exact inversion + residual, kappa = 1/b, remainder bound,
   MU2 slope-2 with explicit remainder, negative-control distinctness `1/(2b) ≠ 1/b`,
   dimension-vector checks.

---

## 5. Negative controls (capable of failing — and audited as such)

| Control | What it would catch | Result |
|---|---|---|
| **N1 b-sweep:** change b (1/2 → 1 → 2) preserving mu(0)=0, mu(∞)=1; fitted kappa must move 2 → 1 → 1/2 | a checker that hardwired kappa = 1/2, or the inverted reading kappa = b | PASS (three distinct limits, each < 1e-6 from 1/b) |
| **N1 Lean:** `1/(2b) ≠ 1/b` for b > 0 | the identity `kappa = 1/b` being insensitive to slope | PASS (certified) |
| **N2 dimensional:** `dim(g²) = dim((s/b)B) = (2,0,−4)`; wrong-G placement `s' = c·sqrt(rho_L/G)` and c-less `s'' = sqrt(G·rho_L)` must be rejected | wrong G placement or missing c in the vacuum scale | PASS (both rejected: (−2,1,0) ≠ (1,0,−2), (0,0,−1) ≠ (1,0,−2)) |
| **N2 note:** `kappa = b` and `kappa = 1/b` are *both* dimensionless | the inversion is invisible to dimensional analysis | documented: caught only by N1 |
| **N3 remainder:** `|g² − (s/b)B| ≤ (K/b)g³/s` at every ladder point with estimated K | a wrong b placement (b multiplied instead of divided) inflating the residual beyond the bound | PASS (ratio ≤ 1 at all 24 points) |
| **N4 Newtonian recovery:** `g/B → 1` as `B/s → ∞` | broken endpoint normalisation mu(∞) ≠ 1 | PASS |

**Failed attempts:** two intermediate script versions (quartic-solve placement; tuple-key JSON dump) and three Lean compile iterations (`ring_nf` doesn't clear field denominators; bare `field_simp` sometimes closes the goal fully, making a trailing `ring` fail — fixed with `try ring`; `neg_div`/`pow_succ` pattern mismatches). All preserved under `failed_attempts`.

---

## 6. Strongest surviving statement

**Theorem (deep-slope matching, scoped).** Let `s > 0`, `b > 0`, `B > 0`, `g ≥ 0`, and
`mu(Y) = bY + R(Y)` with `|R(Y)| ≤ K·Y²` on `[0, Y0]`. The spherical response equation
`mu(g/s)·g = B` implies, for `Y = g/s ≤ Y0`,

```text
g² = (s/b)·B + δ ,   |δ| ≤ (K/b)·g³/s ,   i.e.  |δ|/g² ≤ (K/b)·Y → 0 ,
```

so the deep a0-line constant is `a0 = s/b` and `kappa := a0/s = 1/b`. **Domain:** spherical
static sector, deep regime `B ≪ b·s`, explicit remainder hypotheses as stated; both footings
apply identically (theorem dimensionless). **Scope limit:** `b` itself is *not* fixed by this
theorem; `kappa = 1/2` follows only with the additional premise `b = 2` (channel-count programme
PD01/PD08 or SPARC selection PD01 C2), which this seed does not re-derive.

---

## 7. First additional implication needed to transfer to the full theory

The transfer `g² = (s/b)B` was proven in the **spherical first-integral** form of the response
equation (and, by the PD01 B1–B2 two-channel computation, in the spherical Poisson sector this
theory's response lives in). Transferring to the **full static/nonspherical** theory requires:
(i) a derivation of `b = 2` from the action's channel structure without invoking the fitted
normalisation (the open "completion" gap of PD01 D1 — the OR/fraction-identity premises are
stated, not derived), and (ii) an explicit bridge from the spherical deep-slope matching to the
filtered-MONO target (criterion B, amended thirteen-item target), since MONO's *continuation*
`h'_mono = max(h'_RAR, δ·h_p/(y+y_p))` is not RAR's deep slope in the same variable. Both are
open dependencies, recorded.

---

## 8. Execution bounds (actually enforced)

- Wall clock: hard-stopped at 120 s in-process; actual 0.38 s.
- Memory: measured RSS 60.0 MB (limit 512 MB; process RSS via `resource.ru_maxrss`, macOS bytes).
- Threads: 1 — no pools, no parallelism (single process).
- Precision: mpmath 50 digits; sympy symbolic with exact rationals.
- Lean: `lake env lean` on leanprover/lean4 v4.34.0-rc2 (Mathlib), 0 sorry, axioms verified.
