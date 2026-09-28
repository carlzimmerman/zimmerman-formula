# AS045 — Newtonian-tail ordering of the three kernels (REDO, authoritative run)

**Run:** `AS045-newtonian-tail-r2-20260928T082400Z-dsv4f-hermes`
**Seed:** `deepseek_push/astra_spawn_ideas/AS045_newtonian_tail_ordering_of_the_three_kernels.md`
**Seed SHA-256 (verified before computation):** `2f7f4fa561e1625a234f4210e10c8bcd64a8d98f869d88b553e094f45187372f`
**This run supersedes** the previous subperseed run `AS045-heatdom-r1-20260928T051523Z-dsv4f-hermes/` (executed a different seed text; preserved, unmodified).
**Worker:** deepseek/deepseek-v4-flash-0731 via openrouter (Hermes subagent) · **Platform:** subagent
**Bounds actually enforced:** wall 2.52 s (declared ≤ 120 s), peak RSS 19.9 MiB (declared ≤ 512 MB), 1 thread (env caps; pure-python mpmath). `RLIMIT_CPU=(120,121)` set in-process; `RLIMIT_AS` not settable on this macOS build (recorded; RSS measured instead).

---

## 1. Sources and pinned hashes (all verified before computation)

| Source | SHA-256 | Match |
|---|---|---|
| `README.md` | `91a5fac44ffe30db5f8e95247e5f04e913eccd149f2ff8b683c1f05510a6b6ed` | ✓ manifest pin |
| `qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md` | `98d9149fcebb3a15a1d01b0142587b7d346b3471b007b52457b17a3bcb5d8e3f` | ✓ manifest pin |
| `real_research/peer_review_2026_09_26/README.md` | `521d9ac36a93a27dcd6c995f78743ae9b1de4304095911871d81e6a70f9ecaac` | ✓ manifest pin |
| Seed (this task) | `2f7f4fa5…372f` | ✓ (recorded as `task_sha256`) |

Operative target per the 2026-09-26 amendment: **filtered ν_mono**; causality criterion **B**; historical EXP is a comparison branch only. This seed's claim concerns the **kernel-level** (response-level) Newtonian tails; no field-level or causality claim is made here.

## 2. Symbol dictionary, branch equations, framework inputs vs. conclusions

Dimensionless variables: `y = B/a0 = g_N/a0 > 0` (baryonic/Newtonian field in units of the acceleration scale), `x = g/a0` (total acceleration). Symbols: `B = g_bar = g_N > 0`, `g` total radial acceleration, `ν = g/B` (inverse-interpolation factor), `μ = B/g` (interpolation factor). Units: `a0, B, g` in m/s²; `g − B` absolute anomaly in m/s².

Framework **inputs** (adopted, NOT derived here — stated explicitly per the framework contract):

- `a0 = κ c √(G ρ_Lambda)`, **κ = 1/2 adopted** (no independent derivation supplied by this task);
- `ρ_Lambda = 4 a0²/(G c²)` (rearrangement of the same relation, κ = 1/2);
- branch equations from the branch dictionary (FRAMEWORK_CONTRACT §"Branch dictionary"):
  - **Q:** `g² = B² + a0 B`  ⟹  `ν_Q(y) = √(1 + 1/y)` (radial algebraic relation);
  - **RAR:** `ν_RAR(y) = 1/(1 − e^{−√y})`, spherical unfiltered `g = B ν_RAR(y)`;
  - **MU2:** `μ2(x) = 1 − (1 + x/2)^{−2}`, `μ2(x)·g = B`  ⟹  `y = x·μ2(x)`, `ν_MU2 = x/y`;
  - **EXP** (historical, comparison only): `μ_EXP(x) = 1 − e^{−x}`, `y = x(1 − e^{−x})`, `ν_EXP = x/y`;
  - **MONO** (operative): `h_RAR(y) = y(ν_RAR(y)−1)`, `h′_mono = max(h′_RAR, δ h_p/(y+y_p))`, `δ = 0.05`, spline at `y*`; on the continuation `h_mono(y) = h_RAR(y*) + δ h_p ln((y+y_p)/(y*+y_p))`, `ν_mono = 1 + h_mono/y`;
- measured constants: `G = 6.67430e-11 m³ kg⁻¹ s⁻²`, `c = 299792458 m/s`, `M_sun = 1.98847e30 kg`, `pc = 3.085677581491367e16 m`; two footings `a0 = 9.3619e-11 m/s²` (canonical) and `1.1279e-10 m/s²` (alternative) — **κ = 1/2 fixed in both, so ρ_Lambda differs** (ratio `(1.1279e-10/9.3619e-11)² = 1.4514872`).

Conclusions to be established (this run): the large-`y` asymptotics of `ν−1`, the fate of the absolute anomaly `B(ν−1) = a0·y(ν−1)`, their strict ranking and crossing points, and the recovery radii — all **kernel-level**, on `y > 0`.

### 2.1 First-principles obligation and dependency inventory
The derivation starts from the declared branch equations (inputs 1) and derives (2) expansions, closed forms, rankings, crossings and footings. No new law, no fitted parameter, no new particle species. `κ = 1/2` and `δ = 0.05` remain supplied inputs; `y_p`, `y*`, `h_p`, `h*` are *derived* values (bracketed roots of stated equations, not inputs). The branch dictionary itself is the amended requirement-1/12 definition — an adopted constitutive input, not derived here.

## 3. Step 1 — precise claim, boundaries, assumptions

**Claim under test (seed):** *"Q, RAR and MU2 each give ν−1 with different large-y asymptotics"*, in the sense that a constitutive response, its inverse, and its field equation must agree on their declared branch, and matching one asymptote does not make two kernels equivalent.

**Precise quantified statement (this run establishes):**  On `y ∈ (0, ∞)`, as `y → ∞`:

| Branch | relative anomaly `ν − 1` | absolute anomaly `(g−B)/a0 = y(ν−1)` |
|---|---|---|
| MONO (operative) | `[h* + δ h_p ln((y+y_p)/(y*+y_p))]/y` = `(δ h_p ln y)/y·(1+o(1))` | `h* + δ h_p ln((y+y_p)/(y*+y_p))` → **+∞** (logarithmic, unbounded) |
| Q | `1/(2y) − 1/(8y²) + 1/(16y³) − 5/(128y⁴) + 7/(256y⁵) − …` | `1/2 − 1/(8y) + 1/(16y²) + …` → **a0/2** (nonzero limit) |
| MU2 | `4/y² − 16/y³ + 32/y⁴ + 64/y⁵ − 832/y⁶ + …` | `4/y − 16/y² + 32/y³ + …` → **0** (power law) |
| RAR | `e^{−√y} + e^{−2√y} + e^{−3√y} + …` | `y e^{−√y} + O(y e^{−2√y})` → **0** (exponential in √y) |
| EXP (comparison) | `e^{−y}(1 + O(y e^{−y}))` | `y e^{−y}(1 + O(y e^{−y}))` → **0** (exponential in y) |

Boundary conditions / domain assumptions: `y = B/a0 > 0`; all branches are evaluated at their declared argument (`y` for Q/RAR/MONO; `x = g/a0` with `y = x μ(x)` for MU2/EXP — the Newtonian variable of those two responses is defined implicitly by their own constitutive relation, so `ν−1` is quoted as a function of the *Newtonian* `y` after inversion). No field equation, no filter action, no Cauchy data are needed for the kernel-level statement.

## 4. Step 2 — derivation of the leading anomalies and their symbolic ranking

### 4.1 Q branch
`ν_Q(y) = √(1 + 1/y)`. Binomial series with `w = 1/y`:

`(1+w)^{1/2} = 1 + w/2 − w²/8 + w³/16 − 5w⁴/128 + 7w⁵/256 − …`  ⟹

**`ν_Q − 1 = 1/(2y) − 1/(8y²) + 1/(16y³) − 5/(128y⁴) + O(y⁻⁵)`**
**`(g−B)/a0 = y(ν_Q−1) = 1/2 − 1/(8y) + 1/(16y²) − 5/(128y³) + O(y⁻⁴)`.**

Leading neglected term: `−1/(8y²)` (relative; `−1/(4y)` in `2y(ν−1)`); domain `y ≫ 1`. Rationalization identity (exact, certified in Lean):

`y(√(1+1/y) − 1) = 1/(√(1+1/y) + 1)`  ⟹  **`y(ν_Q−1) ≤ 1/2` for all `y > 0`** — the absolute anomaly never decays below half of `a0`; it saturates at **a0/2** from below (the "a0/2 offset"). Two-sided bound (certified in Lean, `y ≥ 1`): `1/2 − 1/(8y) ≤ y(ν_Q−1) ≤ 1/2`.

Inverse consistency (response–inverse agreement): `g² = B² + a0B` inverted gives `B = (√(a0² + 4g²) − a0)/2`, i.e. `B/g = √(1 + (a0/2g)²) − a0/(2g) = 1 − a0/(2g) + O((a0/g)²)`; the inverse's deviation is `~ a0/(2g) = 1/(2x)` — the same `1/y`-class tail in the inverse variable, consistent with the response (no branch contradiction).

### 4.2 RAR branch
`ν_RAR(y) = 1/(1 − u)`, `u = e^{−√y} < 1` for `y > 0`. Geometric series:

**`ν_RAR − 1 = u/(1 − u) = u + u² + u³ + … = e^{−√y} + e^{−2√y} + e^{−3√y} + …`**
**`(g−B)/a0 = y e^{−√y}(1 + O(e^{−√y}))`.**

Leading neglected term: `e^{−2√y}`; domain `y ≫ 1`. The exact identity `(ν−1)(1 − u) = u` is machine-verified over the full grid (residual 1.3e-51). Inverse: `B = g/ν_RAR(y(B))` — same function, analytic; the tail in the inverse variable is `e^{−√x}`-class: consistent.

### 4.3 MU2 branch (implicit response: `μ2(x)·g = B`)
Exact algebra first. With `q = (1 + x/2)^{−2}`: `μ2 = 1 − q`, `y = x μ2`, `x − y = x·q`, so

**`ν_MU2 − 1 = (x − y)/y = q/(1 − q) = 4/(x² + 4x) = 4/(x(x+4))`**  — *exact closed form, pure algebra, certified in Lean.*

(Verified in sympy: `closed_form_residual = 0`.) Inverting `y = x − 4x/(x+2)²` near infinity (`x = y + 4/y − 16/y² + 32/y³ − 128/y⁴ + …`, symbolic reversion cross-checked):

**`ν_MU2 − 1 = 4/y² − 16/y³ + 32/y⁴ + 64/y⁵ − 832/y⁶ + …`**
**`(g−B)/a0 = 4/y − 16/y² + 32/y³ + …`**

Leading neglected term: `−16/y³` (relative); domain `y ≫ 1`. Sign check: `q > 0`, `1 − q > 0` for `x > 0` (μ2 strictly between 0 and 1), all coefficients of the anomalies positive at leading order. Units: `y(ν−1)` dimensionless; multiplication by `a0` restores m/s². Also `y'(x) = 1 − 4(2−x)/(x+2)³ > 0` on the sample box (secant min 1.199e-3 > 0) → unique inversion x(y), hence a genuine function `ν_MU2(y)`.

Inverse consistency: the MU2 relation is symmetric by construction (`B = g μ2(g/a0)` is the defining equation); the response and inverse are the same algebraic curve — branch-agreement holds by definition; the *tail* ordering in the Newtonian variable is what distinguishes it from Q and RAR.

### 4.4 EXP branch (historical, comparison only)
`μ_EXP(x) = 1 − e^{−x}`, `y = x(1 − e^{−x})`, `x − y = x e^{−x}`:
**`ν_EXP − 1 = x e^{−x}/y = e^{−y}(1 + O(y e^{−y}))`**, `(g−B)/a0 = y e^{−y}(1 + O(y e^{−y}))`. Checked at `y ∈ {20, 30, 40}`: `e^y(ν−1) = 0.9999999608, 0.9999999999973, 1 − 1.7e-16` with the predicted bound `|e^y(ν−1) − 1| ≤ 2.2 y e^{−y}` satisfied at every point. Note `e^{−y}` vs RAR's `e^{−√y}` — a *different* exponential rate, so even the two exponential kernels are not tail-equivalent.

### 4.5 MONO branch (operative)
Landmarks (bracketed roots, residual ~1e-47, not grid inspection): peak of `h_RAR` solves `e^{−t} = 1 − t/2`, `t = √y`:

`y_p = 2.5396382821881653`, `h_p = h_RAR(y_p) = 0.6476102378919149`, `h* = h_RAR(y*) = 0.6469603693249751`, splice `y* = 2.3374124052663295` (crossing of `h′_RAR` with `δ h_p/(y+y_p)`; spec landmarks 2.5396 / 2.3374 reproduced). Splice continuity: `|h_mono(y*) − h_RAR(y*)| = 0` (exact) and `|h′_RAR(y*) − δh_p/(y*+y_p)| = 2.0e-47`.

Continuation (closed form, exact for `y ≥ y*`):
**`h_mono(y) = h* + δ h_p ln((y+y_p)/(y*+y_p))`**, `ν_mono − 1 = h_mono(y)/y`, `(g−B)/a0 = h_mono(y)`.

- **Absolute anomaly is unbounded:** `(g−B) = a0·(h* + δ h_p ln((y+y_p)/(y*+y_p))) → +∞` as `y → ∞` (logarithmic growth). Numerically at `y = 10^8`: `y(ν−1) = 1.192123204` (vs. Q's 0.5). The structural identity is exact (residual 0.0 over the whole tail grid).
- **Relative anomaly:** `ν_mono − 1 ~ (δ h_p ln y)/y` — decays, but *slower* than every other branch's relative tail.
- **MONO > Q for ALL `y ≥ y*` (proof, not numerics):** `y(ν_Q − 1) = 1/(√(1+1/y)+1) ≤ 1/2` (exact, certified in Lean), while `y(ν_mono − 1) = h* + δh_p·ln(…) ≥ h* = 0.64696 > 0.5`. Minimum observed ratio `(ν_mono−1)/(ν_Q−1)` over the tail grid = 1.38336. **No crossing exists.**
- Defining-ODE check on the continuation (finite differences vs. `δ h_p/(y+y_p)` at `y ∈ {10, 100, 10⁵, 10⁸}`): relative residuals 2.1e-19 … 3.3e-19 — the continuation obeys its own derivative rule, not the RAR derivative (the two differ: RAR's `h′` dives below the phantom floor at `y*`).

Branch fidelity of MONO vs RAR (amended requirement-1 landmark): `max_y |log10 ν_mono − log10 ν_RAR| = 0.0103701` (spec quote 0.0104; rounds consistently) attained at `y = 14.3507` (spec 14.35) ✓.

### 4.6 Ranking, crossings, recovery radii

Relative tails (`ν−1`), asymptotically `y → ∞`:

**MONO `(δ h_p ln y)/y`  >  Q `1/(2y)`  >  MU2 `4/y²`  >  RAR `e^{−√y}`  >  EXP `e^{−y}`** — each with a *distinct* leading rate.

Absolute anomalies (`B(ν−1)`): **MONO → +∞·a0** (log), **Q → a0/2** (constant), **MU2 → 4a0/y**, **RAR → a0 y e^{−√y}**, **EXP → a0 y e^{−y}` (both → 0).

Exact crossing points of the *relative* curves (bracketed roots of the exact functions):
- **Q = MU2 at y = 3 exactly (closed form):** `x = 2√3` solves `x·μ2(x) = 3` (since `μ2(2√3) = √3/2`), and `ν_Q(3) = √(4/3) = 2/√3 = ν_MU2(3)` — certified in Lean (`q_mu2_coincidence_y3`), numeric agreement to 1e-40 in check C16. RAR does not share the point (`ν_RAR(3) = 1.2149505`, gap 0.0602 from 2/√3).
- **MU2 = RAR at y = 32.5348974602.** For `10 ≤ y < 32.53` the RAR tail *exceeds* MU2's (min ratio 0.6172 on [10, 1e8]); on the ordering window `[50, 1e8]` the strict hierarchy holds (min ratios: Q/MU2 6.7505, MU2/RAR 1.7446, RAR/EXP 4.92e18, MONO/Q 1.3834).
- **MONO = Q: none on `[y*, ∞)`** (proof in §4.5).

"1%-Newton-deviation radii" `y_{1%}` (`ν−1 = 0.01`) and the recovery radius in units of the MOND radius (`r = r_M/√y`, since `y = r_M²/r²`):

| branch | `y_{1%}` | `r_{1%}/r_M` |
|---|---|---|
| MONO | 73.594 | 0.117 |
| Q | 49.751 | 0.142 |
| MU2 | 17.921 | 0.236 |
| RAR | 21.299 | 0.217 |
| EXP | 4.569 | 0.468 |

The operative MONO branch is the **last** to return to Newton at fixed radius — 1.7× farther in (in `r/r_M`) than RAR at the 1% level, and its absolute anomaly does not return at all.

## 5. Step 3 — intermediate algebra, scale factors, signs, units (completed)

Everything above carries explicit powers/signs; units: every `ν−1` is dimensionless; `y(ν−1)` dimensionless; `a0·y(ν−1)` in m/s² is the physical absolute anomaly; `a0 = κ c √(G ρ_Lambda)` only ever enters through the ratio `y = B/a0` → **the entire kernel-level statement is a0-free and G-free** (pure dimensionless mathematics), and both footings apply by the rescaling `y = B/a0` with the respective adopted `a0` (see §8). No integration was needed at kernel level; the two limiting regimes used are `y → 0` (deep) and `y → ∞` (Newtonian), each with its derived leading neglected term and domain, stated above.

## 6. Step 4 — independent checks in a different representation (actual residuals)

All at mpmath dps 50, grid `y = 10^k`, `k = −10.0 … 8.0 step 0.1` (181 points), cancellation-free evaluation forms:

- **IC1 (Q, substitution into the original equation):** max over grid of `|x² − y² − y|` with `x = y·ν_Q` = **2.4e-35** (absolute; at `x² ~ 1e16` this is relative 2.4e-51 — dps-50 rounding scale). Pass (tolerance 1e-30).
- **IC2 (MU2, inversion identity):** max `|y − x·μ2(x)|` after bisection re-solve = **2.3e-38**; consistency `|ν_grid − (x/y − 1)|` = **0.0**.
- **IC3 (RAR, series identity):** max `|(ν−1)(1 − e^{−√y}) − e^{−√y}|` = **1.3e-51**.
- **IC4 (MONO, defining ODE by finite differences):** relative residuals 2.1e-19, 3.2e-19, 3.3e-19, 3.3e-19 at `y = 10, 100, 1e5, 1e8`.
- **IC5 (EXP tail convergence):** `e^y(ν−1)` = 0.9999999608 (y=20), 0.9999999999973 (y=30), 1−1.7e-16 (y=40); bounds `2.2y·e^{−y}` satisfied.
- **IC6 (peak condition):** `|e^{−t} − (1 − t/2)|` at the bracketed `t = √y_p` = **9.9e-47**.
- **IC7 (symbolic series, sympy):** `ν_MU2−1` closed form residual 0; series `4v² − 16v³ + 32v⁴ + 64v⁵ − 832v⁶ + …` in `v = 1/y` by formal-series Newton reversion — consistent with the numeric coefficient extraction at `y = 10^8` (`y²(ν−1) = 3.9999998400000032` = `4 − 16/y + 32/y²` exactly at dps 50).

Distinction exact-identity vs finite-consistency: IC1/IC3/IC6 and the MONO structural identity + splice continuity are exact identities evaluated numerically (residuals at rounding scale, flagged `exact_identity`); IC2/IC4/IC5 are finite numerical consistency checks (flags set accordingly in `result.json`).

## 7. Step 5 — controls capable of failing

**Regime controls (must pass):**
- **C1 deep (five branches):** `g²/(a0B) = y·ν² → 1` (shared deep asymptote `g² = a0B`, i.e. `v_flat⁴ = G M_b a0`) with the *derived* leading corrections — Q: `+y`; RAR/MONO: `+√y`; MU2: `+(3/4)√y`; EXP: `+(1/2)√y` — slope checks on `k ∈ [−10, −4]`: Q 1.0000, others 0.50019–0.50021 (within 5%), magnitude ratios dev/lead < 2 at `y = 10^{-2}`. Pass.
- **C2–C8 Newtonian regime (five branches):** asymptotic coefficient ratios at `y = 10^8` match the expansions: `2y(ν_Q−1) = 1 − 1/(4y) + 1/(8y²)` EXACT (0.9999999975000000125 both sides); `y²(ν_MU2−1) = 4 − 16/y + 32/y²`; `e^{√y}(ν_RAR−1) = 1 + e^{−√y}`; MONO structural residual 0.0; EXP bounds pass. Pass.
- **C9/C10 landmarks and MONO–RAR dex** (2.53964/2.33741; 0.0103701 @ 14.3507): pass.
- **C11–C16 ordering window, crossings, normalization cases, triple point, recovery radii:** pass.

**Negative controls (must FAIL — they do):**
- **NC1 (seed-specified):** *"Compare only ν−1 while forgetting its multiplication by B"* — test: "relative tails decay ⇒ absolute tails decay". At `y = 10^8` all five relative anomalies are tiny (`ν−1` from 6.5e-43429449 to 1.2e-8), but the absolute anomalies per branch are: Q **0.4999999987·a0** (≠ 0 — control fires), MONO **1.192123204·a0** (growing — fires), MU2 4.0e-8·a0 (decays), RAR ~1.1e-4335·a0, EXP ~6.5e-43429449·a0. Conclusion "all absolute anomalies vanish in the Newtonian tail" is **false**; the control is capable of failing (it would pass only if Q's absolute anomaly also decayed) and it fails exactly where the trap predicts.
- **NC2 (branch fidelity):** *"matching one asymptote makes kernels equivalent"* — test: "shared deep limit ⇒ same kernel" would require `|ν_a − ν_b| ≈ 0` everywhere; max pairwise gap over the whole grid is **0.4999958** (Q vs RAR in the deep corner) while C1 shows all five share `g² = a0B`. Inference rejected.

## 8. Both footings (κ = 1/2 fixed in both — vacuum density differs)

The dimensionless theorem is footing-independent (`y = B/a0`). Dimensional examples (κ = 1/2 adopted in **both**; `ρ_Lambda` therefore differs by factor 1.4514872 between footings — the two footings do **not** share both a fixed vacuum density and a fixed κ):

| quantity | canonical `a0 = 9.3619e-11 m/s²` | alternative `a0 = 1.1279e-10 m/s²` |
|---|---|---|
| ρ_Lambda = 4a0²/(Gc²) | 5.844412454e-27 kg/m³ | 8.48308962e-27 kg/m³ |
| ε_Lambda = ρ_Lambda c² | 5.2526960e-10 J/m³ | 7.6242207e-10 J/m³ |
| Λ = 32πa0²/c⁴ | 1.0907998e-52 m⁻² | 1.5832818e-52 m⁻² |
| r_M(Sun) = √(GM_sun/a0) | 1.190639769e15 m = 0.038586 pc | 1.084743572e15 m = 0.035154 pc |
| v_flat(Sun)⁴ = GM_sun·a0 → v_flat | 333.87 m/s | 349.78 m/s |
| Q absolute anomaly at y = 10³ | 4.679780347e-11 m/s² | 5.638090829e-11 m/s² |
| MU2 absolute anomaly at y = 10³ | 3.729810977e-13 m/s² | 4.493589764e-13 m/s² |
| RAR absolute anomaly at y = 10³ | 1.728887e-21 m/s² | 2.082923e-21 m/s² |
| EXP absolute anomaly at y = 10³ | 4.752062e-442 m/s² | 5.725174e-442 m/s² |
| MONO absolute anomaly at y = 10³ | 7.671243034e-11 m/s² | 9.242135697e-11 m/s² |

At `y = 10^3` the operative MONO absolute anomaly is already **1.64× the Q offset** and the RAR anomaly is 4.4×10^10 smaller — the tails differ by eleven orders of magnitude between branches at the same Newtonian field.

## 9. Strongest surviving statement, closure implication, next implication

**Strongest statement (kernel level, both footings, y = B/a0 > 0):** Q, RAR, MU2, EXP and the operative MONO each produce a *distinct* Newtonian-tail law: relative tails `(δh_p ln y)/y ≫ 1/(2y) ≫ 4/y² ≫ e^{−√y} ≫ e^{−y}`, absolute fates `{+∞·a0, a0/2, 0, 0, 0}`, with Q=MU2 crossing exactly at y = 3 (closed form, Lean-certified), MU2=RAR at 32.5349, and MONO strictly above Q on `[y*, ∞)` (proved). Matching the shared deep asymptote `g² = a0B` therefore identifies no kernel; matching one tail coefficient identifies none either (Q's `1/(2y)` class is shared by no other branch; MU2's power `4/y²` is unique; RAR's `e^{−√y}` is unique vs EXP's `e^{−y}`).

**Closure implication (named gate):** requirement **1 (operative filtered MONO kernel) → Newtonian-recovery gate (requirement 10)**. Kernel-level implication: any same-action candidate carrying the operative MONO continuation carries an absolute anomaly `a0(h* + δh_p·ln((y+y_p)/(y*+y_p)))` that **grows without bound** with `y = B/a0` — i.e. MONO's phantom does not vanish in the strong-field interior, in sharp contrast with RAR. Transfer to requirement 10 (Solar-System-level Newton recovery, measured G) is **not** licensed by this result: the seed's instruction "avoid transferring a local acceleration estimate into a Cassini quadrupole verdict" applies — the missing bridge is the action of the heat filter `S` on the divergence structure (`∇²Φ = 4πGρ_b + S*∇·[(ν_mono−1)∇Su]`) and the spatial realization of the log growth, which this kernel-level identity does not determine.

**Next unresolved implication:** the kernel-level logarithmic absolute anomaly of the operative MONO branch must be raised through `S` and the divergence operator to the *static field equation* level; until that is computed, no claim about the Solar-System/EPE gate of MONO (nor any RAR↔MONO transfer) can be made. (This is the exact first missing bridge.)

## 10. Lean 4 certificate

File: `as045_newtonian_tail_certificate.lean` (self-contained; compiled from `fable_independent_2026/lean_2026` as compile host only — verified: **no files written into `lean_2026/`**; `lake env lean <abs path>` exit 0, ~3.7 s).

Certified declarations (all over ℝ, dimensionless):
1. `q_rationalized` — rationalization identity `y(√(1+1/y)−1) = 1/(√(1+1/y)+1)`, `y > 0`;
2. `q_tail_bounds` — two-sided tail bound `1/2 − 1/(8y) ≤ y(√(1+1/y)−1) ≤ 1/2`, `y ≥ 1` (the upper constant 1/2 = the a0/2 offset);
3. `mu2_pos` — `μ2(x) > 0` for `x > 0`;
4. `mu2_nu_minus_one_closed_form` — `(x − x·μ2(x))/(x·μ2(x)) = 4/(x(x+4))` for `x > 0` (exact closed form of the MU2 relative anomaly);
5. `mu2_tail_bound_by_y` — `ν−1 ≤ 4/y²`, `y = x·μ2(x)` (power-law tail in the Newtonian variable);
6. `q_mu2_coincidence_y3` — `x·μ2(x) = 3` at `x = 2√3` and `√(1+1/3) = 2/√3` (the exact Q=MU2 tail coincidence at `y = 3`).

**Axiom check (`#print axioms`, unfiltered):** every declaration depends on exactly `[propext, Classical.choice, Quot.sound]` — **zero `sorryAx`**. Hard bar met. (Formal statements carry no physical constants; they certify the dimensionless algebra behind the Q and MU2 tails. House traps applied: `field_simp` closure handling, ℤ-exponent typing for `^(-2)`, explicit ℤ for the MU2 power.)

## 11. Runtime, bounds, artifacts

- Script `as045_newtonian_tail.py`: wall **2.52 s** (`/usr/bin/time`; script-reported `wall_s` 2.5094891), peak RSS **19.9 MiB** (`ru_maxrss` 19,841,024 B; `/usr/bin/time` max RSS 19,939,328 B), 1 thread (env caps OPENBLAS/OMP/MKL/NUMEXPR=1; pure-python mpmath). `RLIMIT_CPU=(120,121)` enforced in-process; `RLIMIT_AS` unsupported on this macOS ("current limit exceeds maximum limit") — recorded, RSS measured instead. All far inside declared bounds (≤120 s, ≤512 MB, 1 thread).
- Checks: **32 total → 30 pass, 2 negative controls fail as designed** (NC1, NC2); every pass/fail with observed value and preset tolerance.
- Grid: `y = 10^k`, `k = −10.0 … 8.0 step 0.1` (181 pts), dps 50; roots bracketed (bisection residual ≤ 2e-47), crossings bracketed (residual ~1e-40), never grid inspection.
- Artifacts (all hashes in `result.json`): `seed_as_dispatched.md` (byte-identical seed copy, hash matches the pinned task hash), `as045_newtonian_tail.py/.out/.time`, `sympy_series_check.py/.out`, `as045_newtonian_tail_certificate.lean/.out`, `derivation.md`, `result.json`.
- Failed attempts (this run; causes recorded): (1) first script execution exited 1 — cancellation underflow of the naive `1/(1−e^{−√y}) − 1` at `y = 10^8` (u at the 4344th digit) and of `x/y − 1` for EXP; fixed with exact cancellation-free forms `u/(1−u)` and `x·e^{−x}/y`; (2) two preset-tolerance/reporting defects found in review of the first full output (C2 expected-series string; C11 ordering window straddling the MU2=RAR crossing), corrected and re-run; (3) multiple Lean elaboration iterations (ℕ-vs-ℤ power typing, `field_simp` closure discipline) resolved before the final clean compile. No failed artifacts preserved separately (same evolving files; final versions authoritative).
- Old subperseed run `AS045-heatdom-r1-20260928T051523Z-dsv4f-hermes/` preserved and untouched (its heat-filter subject matter is a *different* task under the same ID; the orchestrator should keep both on record).

## 12. Child proposals (ready specifications; NOT dispatched — no runner in this session)

1. **AS045.C01** — "Newton-recovery gate for operative MONO through the heat filter". New target: compute the static, field-level `|g − B|` profile of the filtered MONO equation `∇²Φ = 4πGρ_b + S*∇·[(ν_mono−1)∇Su]` for a compact spherical baryonic source with the actual filter domain results (S-boundedness/adjoint conventions from AS043/AS045-r1 artifacts), and locate the smallest `y_gate` with `|g−B|/B ≤ 10^{-4}` plus the implied bound at 1 AU. Why AS045 does not answer it: kernel-level `y(ν−1) = h* + δh_p ln(…)` has no spatial realization; the S-action and divergence structure are not part of this result. Controls: cancellation-free numerics, filter-domain handoff, negative control "RAR exp-tail ⇒ MONO recovery" (must fail). Dependencies: S-domain result (AS043 family; preserved AS045-heatdom-r1 artifacts as handoff), failure of the naive transfer demonstrated in §7 NC1.
2. **AS045.C02** — "MONO tail vs. requirement-10 measured-G gate (EPE/Cassini multipole, no local-transfer shortcut)". New target: derive the first non-Newtonian multipole of the operative MONO field equation (not the Q-branch estimate) and compare against the committed Solar-System gates, honoring the seed's warning that a local acceleration estimate must not become a Cassini quadrupole verdict. Controls: matched forward solve at ξ → 0 vs. committed quadrupole (repository f26 conventions), signed chargebook of the log tail. Dependencies: AS045.C01 output.

Duplicate screening: manifest/registry check performed; no existing AS task targets the MONO Newton-recovery gate or MONO quadrupole (closest: AS035 high-field recovery of MONO — kernel-level, superseded scope-wise by this run's exact closed form; AS026/AS029/AS031 inversions — different objects).

## 13. Honest limitations

- Kernel-level only: no heat filter action, no field equation, no spacetime/PPN statement, no causality criterion-B statement (these are explicitly NOT established; the operative MONO's field-level health was not touched).
- Finite grid is evidence, not proof: asymptotics are symbolic (series, closed forms — hence not grid-dependent); the numeric checks confirm coefficients; ordering beyond bracketed crossings relies on the proven distinct leading rates. `MONO > Q` on `[y*, ∞)` is proved, `Q > MU2` for `y > 3` beyond the exact coincidence has a *proved exact crossing point* plus distinct leading rates (the tail dominance `1/(2y) > 4/y² ⟺ y > 8` is elementary).
- The a0/2 Q offset and the MONO log growth are *local* statements; transferred to no observable (per seed instruction).
- `κ = 1/2` and `δ = 0.05` remain adopted inputs; `y_p`, `y*`, `h_p`, `h*` are derived. `G_N/G_bare/G_cosmo` are not separated further because no dimensional identity beyond the footings was needed; both footings given.
- The `0.0104 dex` spec quote is reproduced as 0.0103701 (rounds to 0.0104; argmax 14.3507 vs 14.35) — a 3e-5 discrepancy from the quoted value, consistent with rounding in the amendment; flagged, not "fixed".