# AS032 — RAR phantom acceleration maximum: derivation

Run: `run_AS032-r1-20260928T020843Z-dsv4f-hermes`
Task: `deepseek_push/astra_spawn_ideas/AS032_rar_phantom_acceleration_maximum.md`
(SHA-256 `c7ea12d6434d56edb53af4cd42debda6f9ef3776e68220d81cc7b67ea7eb18dc`)
Worker: Hermes subagent (actual model `deepseek/deepseek-v4-flash-0731` via openrouter).
Branch: **RAR only** for conclusions; Q and MU2 derived as comparison landmarks; MONO referenced as comparison only (AS033 owns the splice). Criterion B, September 26 amendment.

---

## 0. Symbol dictionary, branch declarations, boundary conditions

| symbol | meaning | status |
|---|---|---|
| `B = g_N` | Newtonian (baryonic) acceleration, `B > 0` | input, spherical static idealisation |
| `a0` | framework vacuum scale, `a0 = κ c √(G ρ_Λ)`, **κ = 1/2 adopted** | framework input, not derived here |
| `y = B/a0` | dimensionless Newtonian argument, `y > 0` | domain |
| `x = g/a0` | dimensionless total acceleration (MU2 branch only) | domain |
| `t = √y` | square-root variable | change of variable |
| `g` | total radial acceleration | derived per branch |
| `h = g − B` | phantom (excess) acceleration | derived per branch |
| `nu_RAR(y) = 1/(1 − e^{−√y})` | RAR response, `g = B·nu_RAR` (spherical unfiltered) | branch input (framework contract) |
| `h_RAR(y) = y(nu−1) = y/(e^{√y}−1)` | RAR phantom in units of `a0` | derived object of this task |
| `F(t) = (2−t)e^t − 2` | peak-equation LHS | derived |
| `y_p, t_p, h_p` | peak landmark (root of `h' = 0`) and peak value | derived, compared to contract `y_p = 2.53964`, `h_p = 0.647610` |

Branch equations used (framework contract): Q `g² = B² + a0B`; RAR `nu(y) = 1/(1−e^{−√y})`; MU2 `mu2(x) = 1−(1+x/2)^{−2}`, `mu2(x)·g = B`; MONO (comparison only) `h'_mono = max(h'_RAR, δh_p/(y+y_p))`, `δ = 0.05`, `ν_RAR` used up to `y* ≈ 2.3374`. G_N, G_bare, G_cosmo kept separate; only `G_N = 6.67430e-11` enters `B = G_N M_b(<r)/r²`-type contexts and the footing densities.

**Assumptions (all declared):** static spherical algebra `g = B·nu(y)` on the RAR branch (no filter — the filtered field equation is MONO's, out of scope); `κ = 1/2` adopted (framework input); `G, c` fixed SI; two footings `a0 = 9.3619e-11` and `1.1279e-10 m/s²` reported separately.

---

## 1. Precise claim (Step 1)

On the RAR branch with `h(y) = y(nu(y)−1) = y/(e^{√y}−1)`, `y > 0`:

**(C1)** `h` has a unique global maximum on `(0,∞)` at the unique root `t_p = √y_p ∈ (1,2)` of the peak equation `e^{t}(2−t) = 2` (exact form), `y_p = 2.5396382821881653...`, with **exact value law**

  `h_p := h(y_p) = t_p(2−t_p) = √y_p(2−√y_p) = 0.64761023789191486...` (units of `a0`).

**(C2)** concavity at the peak (dimensionless, `h/a0` as function of `y`):

  `h''(y_p) = (1−t_p)(2−t_p)/(2 t_p³) = −0.029802426216689...  (< 0)`.

**(C3)** branch ordering of phantom maxima (all in units of `a0`):
  `max_y h_RAR = 0.64761 > max g-chart`; precisely:

  | branch | phantom max | attained at |
  |---|---|---|
  | RAR | `h_p = √y_p(2−√y_p) = 0.64761024` | finite `y_p = 2.53963828` |
  | Q | `sup h_Q = 1/2` (strict cap, **never attained**; `h_Q < 1/2` for all finite `y`) | `y → ∞` only |
  | MU2 | `1/2` exactly | finite `x = 2` (`g = 2a0`) |

  RAR peak exceeds the Q/MU2 cap by the factor `h_p/(1/2) = 1.29522048`.

**(C4)** boundary behaviour: `h(y) → 0` as `y → 0+` (`h/a0 = √y − y/2 + y^{3/2}/12 + O(y²)`, leading term `√y = √(B/a0)`, i.e. `h ≈ √(a0 B)`) and `h(y) → 0` as `y → ∞` (`h/a0 = y e^{−√y}(1 + e^{−√y} + O(e^{−2√y}))`).

**Framework inputs vs conclusions:** `nu_RAR`, `κ`, `a0`, `G`, `c`, both footings, `δ`, MONO rule = inputs; (C1)–(C4) and the exact identities are conclusions derived from them.

## 2. Derivation of h′ and the peak (Step 2)

With `t = √y` (`y = t²`, `dt/dy = 1/(2t)`, positive for `t > 0`):

```
h(y) = t²/(e^t − 1)                       (exact, no approximation)
dh/dt = [2t(e^t−1) − t²e^t]/(e^t−1)²
      = t·F(t)/(e^t−1)²,   F(t) := (2−t)e^t − 2
h′(y) = (dh/dt)·(dt/dy) = F(t)/(2(e^t−1)²)          (exact closed form)
```

Since `2(e^t−1)² > 0` for `t > 0`, `h′(y) = 0 ⟺ F(t) = 0 ⟺ e^t(2−t) = 2` — **the peak equation in exact form**. Note `t = 0` also solves `F = 0` (boundary solution, `F(0) = 0`), but `y = 0` is not in the open domain and is not a critical point (`h′(0+) = +∞`, §5 control (a)).

**Root isolation (positive nonzero root).** `F′(t) = (1−t)e^t`; so `F` strictly increases on `(0,1)` (F′(t) > 0), `F(1) = e−2 ≈ 0.7183 > 0`, and `F` strictly decreases on `(1,2)` (`F′(t) < 0`), `F(2) = −2 < 0`. By IVT + monotonicity there is **exactly one root `t_p ∈ (1,2)`**; it is the unique root of `F` on `(0,∞)` since `F(t) > 0` on `(0,t_p)` (`F > 0` at `t = 1` and no sign change before) and `< 0` after. `F` signs give `h′ > 0` on `(0,t_p)`, `h′ < 0` on `(t_p,∞)`: unique global max. Numerics (50 digits, mpmath):

```
t_p = 1.5936242600400400923230418758751602417890024248189
y_p = t_p² = 2.5396382821881653249988817897743659023689841775412
```

Contract landmark `y_p = 2.53964`: `|y_p − 2.53964| = 1.72e−6` ✓; AS028's rounded re-derivation `2.539638282` agrees to 1e-9.

## 3. Exact peak value and concavity (Steps 2–3: algebra, signs, units)

At the root, `e^{t_p} = 2/(2−t_p)` (valid since `t_p < 2`), hence `e^{t_p} − 1 = t_p/(2−t_p)`, and therefore **exactly**

```
h_p = t_p²/(e^{t_p}−1) = t_p²·(2−t_p)/t_p = t_p(2−t_p) = √y_p (2 − √y_p).
```

So the maximum is an exact function of the landmark `y_p` — no approximation involved. Numerically `h_p = 0.64761023789191485964720196197595458120902067209651` (agrees with the contract rounded `0.647610` to 2.4e−7 and with AS028's `0.647610238`).

**Second derivative (concavity).** From `h′(y) = F(t)/(2(e^t−1)²)` with `t = t(y)`, `dt/dy = 1/(2t)`, and `F(t_p) = 0`:

```
h″(y_p) = F′(t_p)/(4 t_p (e^{t_p}−1)²) = (1−t_p)(2−t_p)/(2 t_p³)
```

(first attempt at this identity contained a chain-rule slip giving `2t_p⁴` and **failed** the finite-difference control — see `failed_attempt_hpp_formula.json`; corrected form passes). Sign: `t_p ∈ (1,2)` ⇒ `1−t_p < 0`, `2−t_p > 0` ⇒ `h″(y_p) < 0` (genuine maximum); value `h″(y_p) = −0.029802426216689285886344030700488292269603190108711`. Units: `h/a0` is dimensionless in `y`; dimensionally `h″` carries `a0` per unit `y²` (i.e. `h″ ≈ −0.0298 a0`).

## 4. Limiting regimes and leading neglected terms (Step 3)

Using `x/(e^x−1) = Σ B_n x^n/n!` (Bernoulli): `h/a0 = t² Σ B_n t^n/n!`, with `B_0=1, B_1=−1/2, B_2=1/6, B_4=−1/30, B_6=1/42, B_8=−1/30`:

- **Newtonian boundary (y → 0+):**
  `h/a0 = √y − y/2 + y^{3/2}/12 − y²/720 + y^{5/2}/30240 + O(y³)`;
  leading term `√(B/a0)`, i.e. `h ≈ √(a0 B)`; **leading neglected term after `√y` is `−B/2` relative to leading** (ratio `√y/2`). Numerically at `y = 1e−6`: series vs exact agree to `1.39e−15` (5 terms).
- **Trans-Newtonian tail (y → ∞):**
  `h/a0 = y e^{−√y} (1 + e^{−√y} + O(e^{−2√y}))` — faster than any power; numerically at `y = 1e8` the ratio `h/(y e^{−√y}) = 1.0` to 50 digits.
- Both boundaries give `h → 0`; the maximum lies strictly between, at `y_p`.

## 5. Independent checks (Step 4) and negative controls (Step 5)

All residuals are **actual computed values** (no booleans-as-evidence).

**Independent representation checks** (double precision, different algorithms — `AS032_verify.py`):
1. Peak root by **fixed-point iteration** `t_{n+1} = 2 − 2 e^{−t}` (derived from the same peak equation, independent of the mpmath bisection+Newton): residual `F(t_p) = −6.66e−16` ✓.
2. `h_p` by **direct y-space evaluation** `y/expm1(√y)` vs the landmark law `t(2−t)`: differ by `3e−16` ✓.
3. `h′(y_p)` by **five-point numeric differentiation** in y-space at two steps: `7.4e−13` and `−1.0e−11` (≈ 0, consistent with exact `F(t_p) = 0` reported as `0.0` at 50 digits) ✓.
4. `h″(y_p)` by **second central difference** of `h(y)`: `−0.0298017` vs closed form `−0.029802426...` — agree to `2.4e−5` relative, which is the documented fp64 cancellation floor `h(y_p)·eps/(|h″|d²) ≈ 2e−5`; the 50-digit mpmath control (three FD steps `1e−10/1e−12/1e−14` plus the second independent exact form `F′/(4t(e^t−1)²)`) pins `h″ = −0.0298024262166892858863440307...` to `~1e−25` agreement ✓.
5. Grid `y = 10^k`, `k ∈ {−10,…,8}` step `0.1` (181 points): **exactly one sign change** of `h′` (bracket `[2.5, 2.6]` confirmed); grid sup `0.6475987 < h_p` at `y = 10^{0.4}` ✓.

**Negative controls (all capable of failing):**
- **(a) t = 0 boundary solution of the peak equation is NOT the peak:** `F(0) = 0` exactly, so a careless solver is handed a spurious root; rejected because `h′(0+) = +∞` (computed `h′(1e−16) = 4.99999950e7 > 0`) and `(dh/dt)(0) = 1 ≠ 0` — the slope does not vanish at `t = 0`. Classification control: **picked `t = 0` → h(0) = 0 < h_p, fails**.
- **(b) wrong extremum at `t = 1` (where `F′ = 0`, `F` maximal, not a root):** `F(1) = e−2 = 0.7182818 ≠ 0`, `h′(y=1) = 0.1216399 ≠ 0` — rejected; `h(1) = 0.58198 < h_p` — **fails as a maximum**.
- **(c) boundary `t = 2`:** `F(2) = −2`, `h′(4) = −0.0244978 < 0` — not a root; the `e^t = 2/(2−t)` form requires `t < 2`.
- **(d) uniqueness:** `F′ = (1−t)e^t < 0` on `(1,2)` (`F′(1.3) = −1.10`, `F′(1.9) = −6.02`) with `F(1) > 0 > F(2)` ⇒ exactly one positive root; grid count = 1 ✓.
- **(e) THE CONTROL THAT CAUGHT A REAL ERROR:** first-attempt closed form `h″ = (1−t)(2−t)/(2t⁴)` failed the FD control at the 5th significant digit (`−0.0187010` vs FD `−0.0298024`); corrected `2t³` form passes all three FD steps and both independent exact expressions (agreement `4.2e−53`). Preserved: `failed_attempt_hpp_formula.json`.

## 6. Q and MU2 comparisons (derived, same framework)

- **Q** (`g² = B² + a0B` → `g−B = a0 y(√(1+1/y) − 1)`):
  exact rationalized identity `h_Q/a0 = 1/(1 + √(1+1/y))` (certified in Lean, `q_identity`);
  strict monotonicity `(h_Q/a0)′ = (w−1)²/(2w) ≥ 0`, `w = √(1+1/y)`, equality nowhere on `y > 0`;
  **strict cap**: `h_Q(y) < a0/2` for all finite `y`, `sup = a0/2` at `y → ∞` only (certified `q_strict_cap`). No finite peak — the Q branch has no phantom maximum, only an asymptotic cap.
- **MU2** (`mu2(x)·g = B`, `mu2 = 1−(1+x/2)^{−2}` → `h_MU2/a0 = x/(1+x/2)²`):
  exact deficit identity `1/2 − h_MU2/a0 = (1−x/2)²/(2(1+x/2)²) ≥ 0`; `h_MU2 = a0/2` **iff** `x = 2` (certified `mu2_deficit`, `mu2_capped`, `mu2_max_iff`). Finite attained maximum exactly `a0/2`.

**Headline comparison:** `h_p^RAR = 0.64761024 a0 > a0/2 = max h_MU2 = sup h_Q`; the RAR phantom acceleration maximum **exceeds the Q strict cap and the MU2 maximum by 29.5%** (`h_p/(a0/2) = 1.29522048`; excess `h_p − a0/2 = 0.14761024 a0`).

## 7. MONO relationship (comparison only — the operative law)

MONO continues `h_RAR` with `h′_mono = max(h′_RAR, δh_p/(y+y_p))`, `δ = 0.05`, spliced at `y* ≈ 2.3374 < y_p`, i.e. *below* the RAR peak: the RAR maximum is a **comparison landmark** for MONO (it feeds `h_p` and `y_p` into the continuation rule), not the operative law. Consistency check of the landmarks against AS028's rounded splice point: at `y* = 2.337412405`, `h′_RAR(y*) = 0.00663936342199...` vs `δh_p/(y*+y_p) = 0.00663936341274...`, difference `9.25e−12` (i.e. AS028's rounded `y*` obeys the splice equation to its rounding). The exact splice solution is AS033's target; nothing in this task transfers RAR derivative/stability results to MONO (criterion B branch distinctness).

## 8. Dimensional footings (both, separately)

The dimensionless theorem (C1)–(C3) applies identically to both footings; dimensional values scale by `a0`:

| footing | `a0 (m/s²)` | `h_p = 0.6476102379·a0 (m/s²)` | `ρ_Λ = 4a0²/(Gc²) (kg/m³)` |
|---|---|---|---|
| canonical | `9.3619e−11` | `6.0628622861e−11` | `5.8444124540e−27` |
| alternative | `1.1279e−10` | `7.3043958732e−11` | `8.4830896196e−27` |

Both use `κ = 1/2` fixed ⇒ `ρ_Λ` changes: `ρ_alt/ρ_can = (a0_alt/a0_can)² = 1.4514872`. If instead `ρ_Λ` were held fixed, the effective `κ = 0.6023884` (recorded; not used). Φ-peak values are also expressible as accelerations: `h_p,a0` are the phantom acceleration *excess* at the peak field `B_p = a0 y_p` (i.e. at `B = 2.53964 a0`).

## 9. Negative control summary table

| control | method | result |
|---|---|---|
| t=0 boundary root classification | F(0)=0, h′(0+)=+∞, h_t(0)=1 | rejected; not a critical point |
| t=1 (F′–stationary) candidate | F(1)=e−2≠0, h′(1)=0.1216≠0, h(1)<h_p | rejected |
| t=2 endpoint | F(2)=−2, h′(4)<0 | rejected |
| uniqueness | F′<0 on (1,2), F(1)>0>F(2), grid=1 sign change | unique positive peak |
| h_p landmark law | direct eval vs t(2−t) | agree 3e−16 |
| h″(y_p) closed form | FD ×3 steps + 2nd exact form + fp64 stencil | agree 1e−25 (50-digit); 2.4e−5 (fp64 floor) |
| Q cap | certified identity + grid sup (stable form) | `< 1/2` everywhere |
| MU2 max | certified deficit + grid | `= 1/2` iff x=2 |

## 10. Lean certificate

`AS032_rar_phantom_maximum.lean` (in run dir), verified with
`cd fable_independent_2026/lean_2026 && lake env lean <abs>.lean` → **exit 0, zero `sorry`, all nine theorems' axioms ⊆ {propext, Classical.choice, Quot.sound}** (unfiltered `#print axioms` in `lean_check.out`):
`rar_deriv_identity`, `rar_slope_zero_at_peak`, `rar_peak_value` (C1's algebraic core), `peak_equation_iff`, `q_identity`, `q_strict_cap`, `mu2_deficit`, `mu2_capped`, `mu2_max_iff`. The root *location* (IVT + monotonicity) is analytic/numerical, not lean-certified.

## 11. Strongest surviving statement, limitations, next implication

**Strongest statement (scoped):** On the spherical unfiltered RAR branch, the phantom acceleration `h = y/(e^{√y}−1)·a0` has a unique global maximum `h_p = √y_p(2−√y_p)·a0 = 0.64761023789191486·a0` at the unique root `y_p = 2.5396382821881653` of `e^{√y}(2−√y) = 2`; the peak is concave (`h″ = (1−√y_p)(2−√y_p)/(2y_p^{3/2}) = −0.0298024 a0`); and `h_p^RAR > a0/2 = max h_MU2 = sup h_Q` with Q's cap strict-asymptotic and MU2's attained at `g = 2a0`.

**Limitations:** spherical static algebra only; no filter, no field equation, no relativistic content; `κ = 1/2` remains an adopted input; the peak location is certified analytically (IVT+monotonicity) but the exact closed form of `y_p` is transcendental (no elementary expression); RAR conclusions do not transfer to MONO (branch distinctness, criterion B).

**Next unresolved implication:** transfer of the RAR-peak landmark to the operative law is blocked at the splice: the exact solution `y*` of `h′_RAR(y*) = δh_p/(y*+y_p)` (δ = 0.05) and the resulting `h_mono` on `(y*,∞)` — AS033/AS034 territory — plus a proof that the heat-filtered MONO field equation inherits no spurious extremum from the RAR peak.

## 12. Files in this run directory

`AS032_compute.py` (50-digit run, bounded), `raw_output.json`, `AS032_verify.py`, `verify.log`, `AS032_rar_phantom_maximum.lean`, `lean_check.out`, `failed_attempt_hpp_formula.json`, this `derivation.md`, `result.json`.
