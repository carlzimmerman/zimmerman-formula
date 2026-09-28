# AS072 — A normalization theorem with explicit assumptions

**Run:** `AS072-r1-20260928T112622Z-dsv4f-hermes`
**Worker:** deepseek/deepseek-v4-flash-0731 (OpenRouter), Hermes Agent subagent, single-run seed worker
**Task SHA-256:** `127a768e476020e7083d877b1cec4078d9917204b6a523134d36201232e68a79` (verified before execution)
**Branch (declared):** CORE coefficient; conditional MU_n statistical response
**Status:** conditional derivation — 19/19 checks PASS; negative control fired as designed; Lean certificate compiles with axioms ⊆ {propext, Classical.choice, Quot.sound}.

---

## 0. Assignment, verification, sources

The seed asks for *a normalization theorem with explicit assumptions*: state the precise claim behind `kappa = a0/s = 1/2` under the five declared premises, prove the implication chain, remove each premise one at a time with explicit counterexamples at `lambda = 1/2, 1, 2`, and run a negative control capable of failing.

Verified before execution (all match `SOURCE_MANIFEST.json` pins):

| path | sha256 |
|---|---|
| `deepseek_push/astra_spawn_ideas/AS072_a_normalization_theorem_with_explicit_assumptions.md` | `127a768e476020e7083d877b1cec4078d9917204b6a523134d36201232e68a79` |
| `deepseek_push/PD01_polarization_count.py` | `37e39d1abb8dfe74763e59282b6137ed6a6b570215da415d197de72c33e2c74d` |
| `deepseek_push/PD08_particle_free_derivation.py` | `83f6054cdfb1b45834af1ce702b1a040f00ad1625ffc34799ae367bd367f0cfb` |
| `kappa_closure/k01_zero_mode_theorem_and_lambda_free_vacuum.py` | `8df5a3ab5a38d189e0152ab0e54c0fb497056e58373cc0e80db49fca3f35b25c` |
| `FRAMEWORK_CONTRACT.md` / `RESULT_CONTRACT.json` / `SOURCE_MANIFEST.json` | `ca696c7f…` / `621fdad0…` / `fe295b80…` (match records of prior runs) |

## 1. The precise claim, symbol dictionary, boundary conditions, assumptions

**Symbols** (SI throughout): `s = c sqrt(G rho_Lambda)` — the vacuum's own acceleration scale; `Y = g/s` — dimensionless drive; `B = g_N = G M_b / r^2` — Newtonian acceleration of the source; `p_i(Y)` — per-channel engagement; `mu(Y)` — total response; `a0` — the MOND scale; `kappa = a0/s`; `G_N`, `G_bare`, `G_cosmo` kept separate; `rho_Lambda` — vacuum mass density; `c` exact, `G = 6.67430e-11` (CODATA).

**Claim (conditional normalization theorem).** Let

- **A1** `n = 2` channels (carrier count — the metric's static response, PD01-B1/AS056);
- **A2** independent OR composition `mu(Y) = 1 - (1-p1(Y))(1-p2(Y))`;
- **A3** per-channel engagement `p_i(0)=0`, `p_i'(0)=1` (unit slope in s-units), `p_i -> 1` (saturation; the L230 normalization `mu(inf)=1` is implied);
- **A4** measured source coupling: the same measured `G` enters the Poisson flux `4 pi G rho_b` and the vacuum scale `s`;
- **A5** the response scale is fixed by the vacuum, `s = c sqrt(G rho_Lambda)` (measurable vacuum density input).

Then, in the deep regime `Y << 1`, the spherical deep-MOND Gauss law

```
(1/r^2) d/dr [ r^2 mu(g/s) g ] = 4 pi G rho_b      =>      mu(g/s) g r^2 = G M_b
```

together with `mu'(0) = 2` gives

```
g^2  =  (s/2) B (1 - alpha u + O(u^2)),   u = sqrt(B/(2s)) = g_asym/s,
alpha = (c2_1 + c2_2 - 1)/2               (p_i = Y + c2_i Y^2 + O(Y^3)),
```

so at leading order `a0 = s/2` and `kappa := a0/s = 1/2` **exactly**; equivalently
`a0 = (c/2) sqrt(G rho_Lambda)` and `v_flat^4 = G M_b a0` (framework deep law, dimensionless content independent of the completion).

**Framework inputs vs conclusions.** Inputs: `G`, `c`, `rho_Lambda` (measured/defined), premises A1–A5, the L230 normalization `mu(inf)=1`, the statics `div(mu grad) = 4 pi G rho`. Conclusions to be established: `mu'(0) = 2` (from A1–A3), the deep matching `g^2 = (s/2) B (1 + O(g/s))`, `kappa = 1/2`.

## 2. The implication chain to kappa = 1/2

**Step 1 — slope = channel count (product rule through the OR).**
`mu = 1 - prod_i (1-p_i)`; `mu'(0) = sum_i p_i'(0) * prod_{j != i} (1 - p_j(0)) = sum_i p_i'(0)` because `p_j(0) = 0`. With A3 both slopes are 1: `mu'(0) = 2`. Completion-independent: on the generic 2-jet `p_i = Y + c2_i Y^2`, check A1/A3 (sympy) and Lean T1–T3:
`mu(Y) = 2Y + (2 c2 - 1) Y^2 - 2 c2 Y^3 - c2^2 Y^4` (equal channels) — linear coefficient exactly 2.
**Correction record:** PD08's docstring prints the quadratic coefficient as `(2c2+1)`; the true coefficient is `(2c2-1)` (check A2, Lean T1). The origin slope 2 is unaffected and PD08's checks tested only the slope; no later factor may adopt the docstring's sign.

**Step 2 — spherical matching.** Gauss: `r^2 mu(g/s) g = G M_b`, i.e. `Y mu(Y) = B/s`. With `mu = 2Y(1 + alpha Y + O(Y^2))`: `2 Y^2 (1 + alpha Y + ...) = B/s`, so
`Y = u - (alpha/2) u^2 + O(u^3)`, `u = sqrt(B/(2s))`, and

```
g^2 = s^2 Y^2 = (s/2) B ( 1 - alpha u + O(u^2) ),     u = sqrt(B/(2s)).
```

Every scale factor accounted: `[g^2] = m^2/s^4 = [s][B]` (check A8); the `1/2` enters only through the channel count; `s` enters only as the argument's unit and the matching rate (A5 was fixed at the start; `a0` is an output, never an input — the k01 zero-mode hygiene).

**Step 3 — v_flat form.** `v^2 = g r`, deep: `v^4 = g^2 r^2 = (s/2) G M_b = a0 G M_b` ✓ framework deep law (check A7).

**Step 4 — the leading neglected term and its domain.** `alpha = (c2_1+c2_2-1)/2`; relative correction `-alpha u + O(u^2)`, domain `Y << 1` (deep regime). For the corpus member `p = Y/(1+Y)`: `alpha = -3/2`, series `mu = 2Y - 3Y^2 + 4Y^3 - 5Y^4 + 6Y^5 - ...` (check A6, exact).

**Step 5 — Newtonian end.** `p_i -> 1` implies `mu -> 1` ⇒ `g -> B`: an exact limit, not an exact identity at finite `q = B/s` (check D3 measures the rate; see §5).

## 3. What the cited sources actually prove (premise audit)

- **PD01** computes the carrier's static channel count: `G^(1)_00 = 2 lap(Psi)`, `G^(1)_kk = 2 lap(Phi - Psi)` — two independent Poisson operators (B1–B2, symbolic + FD); a scalar/static vector has one channel (B3); hence `kappa in {1/2, 1}` binary under the L230 principle (B4). Its OR-identification is a **declared premise** (D1) — PD01 proves the count, not the composition.
- **PD08** re-derives the chain from a one-field action with `p(0)=0, p'(0)=1, p(inf)=1`; the fraction identity `p'(0)=1` is its **step 3, stated as a premise** ("the L230 principle, backed by the k01 no-go"), and the completion stays empirical (D2). Nothing in PD08 derives `p'(0)=1` from the algebra.
- **k01** proves (K1–K2) that for the candidate action the static equations contain `J` only through `J'` (the normalisation zero mode) — *outcome 3, proven*: with `Lambda` explicit and free, **no equation of that action relates a0 to Lambda**; the Lambda-free repair fails on sign (K3) and by a factor > 200 in size (K4); the `4 pi^4/15` reading needs the branch the bounded-boost theorem forbids (K5), and no coefficient of the action reaches the required ~7.7 (K6).

**Consequence (executed per seed step 2):** the five premises are exactly the premises — every one is load-bearing; the algebra proves the *composition theorem*, none of the five *identifications*. In particular `p_i'(0) = 1` is an **independent premise** (AS053's family `p = lam Y/(1+lam Y)` has the same endpoints and monotonicity for every `lam > 0` but slope `lam`), and `n = 2` is an input (carrier count), not a conclusion.

## 4. Independence audit — remove one premise at a time (explicit counterexamples)

| removed premise | counterexample family | inferred kappa | check |
|---|---|---|---|
| A1 (n = 2) | `mu_n = 1-(1-Y/(1+Y))^n`, n = 1, 3 | `1/n` = 1, 1/3 | B1 PASS |
| A2 (OR) | average `(p+p)/2`; AND `p^2`; real exponent `1-(1-p)^lam` | 1; no MOND sqrt law (`g ~ (B s^2)^{1/3}`); `1/lam` = 2, 1/2 at lam = 1/2, 2 | B2 PASS |
| A3 (p'(0)=1) | `p_lam = lam Y/(1+lam Y)`, lam = 1/2, 1, 2 → slope `2 lam` | `1/(2 lam)` = 1, 1/2, 1/4 | B3 PASS (D4 numeric) |
| A4 (measured G) | source coupling `G_c = xi G_N`, `xi` = 1/2, 1, 2 | `xi/2` = 1/4, 1/2, 1 | B4 PASS |
| A5 (s fixed by vacuum) | `s = xi c sqrt(G rho_Lambda)`, `xi` = 1/2, 1, 2 | `xi/2` = 1/4, 1/2, 1 | B5 PASS |

Diagnostic slopes evaluated at lambda = 1/2, 1, 2 as required; no observational preference used as a mathematical proof anywhere.

## 5. Independent checks (second representation, actual residuals)

mpmath, 60-digit working precision (dps = 60), Newton iteration on `F(y) = y mu(y) - q` with analytic derivative, three completions (corpus `1-1/(1+y)^2`, exponential `1 - e^{-2y}`, tanh `2t - t^2`):

- **D1** deep grid `q = B/s in 10^-2..10^-12`: max `|Y mu(Y) - q| = < 1e-55` (measured; threshold 1e-55). The relative deviation `gamma = g^2/((s/2)B) - 1` is **nonzero** — the a0-line is an asymptote, not an exact identity.
- **D2** `gamma/u -> -alpha = +3/2` (corpus): measured `1.500097`, `1.500010`, `1.500001` at q = 1e-8, 1e-10, 1e-12 (threshold |ratio − 1.5| < 1e-3 at 1e-12). The leading neglected term of Step 2 is reproduced.
- **D3** Newtonian end `q = 1e2, 1e6`: `g/B - 1` matches its asymptote exactly: corpus `1/q^2 - 2/q^3 + O(q^-4)` (measured 9.8020187e-5 vs pred 9.8e-5 at q=1e2; 9.99998e-13 vs 9.99998e-13 at 1e6); exp/tanh exponentially small (`e^{-2q}`/`e^{-4q}`). An exact identity is distinguished from a finite numerical check (seed control 2).
- **D4** origin slopes of the lambda-family by finite difference at h = 1e-24: `2 lam` exact (measured 1.0/2.0/4.0).
- **D5** footings, §7.

## 6. Negative control (specified, capable of failing)

**Claim under test:** "the five assumptions are conclusions of the certified algebra alone" — i.e., dropping/relaxing any premise leaves kappa = 1/2.

**Execution:** each premise's counterexample family is run through the same certified algebra and the inferred kappa is recorded per variant (λ, ξ ∈ {1/2, 1, 2}):

```
A1 (n)         n=1→1,  n=2→1/2,  n=3→1/3            -> load-bearing
A2 (composition) avg→1, OR→1/2, lam=1/2→2           -> load-bearing
A3 (slope)     lam=1/2→1, lam=1→1/2, lam=2→1/4      -> load-bearing
A4 (coupling)  xi=1/2→1/4, xi=1→1/2, xi=2→1         -> load-bearing
A5 (vacuum)    xi=1/2→1/4, xi=1→1/2, xi=2→1         -> load-bearing
```

**Result:** the control **FIRED (PASS as designed)** — every premise's parameter variation changes the inferred kappa; no premise collapses to a single value. The algebra certifies none of the five. It was capable of failing: a redundant premise would leave its variant table constant, forcing withdrawal of the independence claim (check C1). Therefore `kappa = 1/2` is a **conditional** consequence of the five explicit premises — the adopted one-half normalization is not upgraded to an unconditional derivation by this theorem (the seed's warning is honored), but this run *proves the exact content of the normalization step itself*: which premises carry which coefficient.

## 7. Both footings (framework rule)

The theorem is dimensionless: `kappa = 1/2` holds in the s-normalization regardless of the footing's numeric value. Each footing carries kappa = 1/2 with its **own** density (they cannot share both fixed density and fixed kappa):

| footing | a0 [m/s²] | s = 2 a0 [m/s²] | rho_Lambda [kg/m³] | r_M(M_sun) | r_M [kpc] | v_flat(M_sun) [m/s] | eps_L = rho c² [J/m³] | Lambda = 32πa0²/c⁴ [m⁻²] (same-G convention) |
|---|---|---|---|---|---|---|---|---|
| canonical | 9.3619e-11 | 1.87238e-10 | 5.844412454e-27 | 1.190640e15 m | 0.038586 | 333.87 | 5.25270e-10 | 1.09080e-52 |
| alternative | 1.1279e-10 | 2.25580e-10 | 8.483089620e-27 | 1.084744e15 m | 0.035154 | 349.78 | 7.62422e-10 | 1.58328e-52 |

Fixed-density relabeling (alternative a0 on canonical density): `kappa_eff = a0_alt / s_canon = 0.6023884041` — **not** 1/2; recorded as a re-labeling diagnostic (a "second kappa" would contradict A2-A5: `1/kappa_eff = 1.6601` is not the slope of any two-channel OR with unit slopes; see child AS072.C01).

## 8. Branches, gates, and what this run does NOT claim

- **Branch used:** conditional MU_n statistical response (CORE coefficient cell of Requirement 13, the a0–vacuum relation). Q, RAR, MU2, EXP AQUAL, and the operative filtered MONO are distinct laws (**never identified**); no branch translation is performed or claimed. In particular the completed Q-line `g^2 = B^2 + a0 B` shares the deep asymptote but is a different finite law (AS030) — this theorem fixes only the deep slope.
- **The operative target** (amended thirteen-item, filtered MONO, causality criterion B) is **not addressed**; transferring the deep slope to MONO requires the bridge stated in §9.
- No claim that the completion (full shape of mu) is derived — it stays empirical (PD01-D1/PD08-D2); no claim that the action holds of the world; no claim that `kappa=1/2` is an unconditional theorem.

## 9. Strongest surviving statement and the first missing bridge

**Strongest statement (scoped, exact).** *For measurable `G`, `c`, `rho_Lambda`, under premises A1–A5, the deep spherical response satisfies `g^2 = (s/2) B (1 - alpha sqrt(B/(2s)) + O(B/s))` on `Y << 1` — hence `kappa = 1/2` exactly at leading order, `v_flat^4 = G M_b a0`, and each of A1–A5 is necessary: relaxing any one changes the inferred coefficient to the tables of §4. Domain: `Y << 1` (deep), statics, spherical, weak field. The correction's coefficient `alpha` is completion-dependent but the theorem's leading coefficient is not.*

**First missing implication to the full theory:** the operative filtered-MONO branch's deep linear response must be shown to satisfy `mu'_mono(0) = 2` in the vacuum units within the heat-filter domain `S = exp[(xi^2/2) Delta]` (FRAMEWORK_CONTRACT MONO), i.e. a proof that filtering and differentiation commute at the origin for the MONO splice `y_star ≈ 2.3374` construction — or an explicit obstruction. This run proves the MU_n-side statement and stops at that bridge: no branch import is used to repair anything.

## 10. Reproducibility

- Code: `compute_AS072_normalization.py` (single process, 1 thread, deadline checkpoints at 115 s; ran 0.169 s, peak RSS 57.1 MiB; RLIMIT_AS not enforceable on this macOS host — memory measured, not OS-enforced). Raw output: `raw_output.txt`, `err.txt` (empty), `residuals.json` (19 checks, all pass).
- Lean 4 certificate (mathlib 4.34.0-rc2): `AS072_normalization_certificates.lean` — 12 theorems (T1–T10b): ring expansions, HasDerivAt chain rule through the OR (`mu'(0) = 2` completion-independent; `2 lam` for the removal family), the rational lambda-family member `p'(0)=lam`, the truncated matching `b(g/s)g = B => g^2 = sB/b`, `kappa = (s/2)/s = 1/2`, and saturation cleared forms; compiled with `lake env lean` from `fable_independent_2026/lean_2026` (absolute path, host-only compile): **0 errors, 0 sorries, axioms = {propext, Classical.choice, Quot.sound}** (unfiltered `#print axioms`, `lean_check.out`). The certificate covers the algebra of the theorem — not the physical identification of the premises.
- Sources hash-verified against `SOURCE_MANIFEST.json` (table in §0).
