# AS036 — Physical monotonicity versus phantom monotonicity

**Run:** `AS036-r1-20260928T021215Z-dsv4f-hermes`
**Worker:** deepseek/deepseek-v4-flash-0731 (provider: openrouter); Hermes Agent focused subagent (orchestrator claim reservation `sa-5-d75c87dd`)
**Task hash:** `d7262be084e2209ac8a63ed4605fe4277aa62294fcc295070310c36b4796dea9`
**Branch cell:** Separate Q, RAR, MU2, historical EXP, operative MONO (criterion B); `kappa = 1/2` adopted framework input.
**Sources verified:** `README.md` `91a5fac44ffe30db5f8e95247e5f04e913eccd149f2ff8b683c1f05510a6b6ed` ✓; `qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md` `98d9149fcebb3a15a1d01b0142587b7d346b3471b007b52457b17a3bcb5d8e3f` ✓; `real_research/peer_review_2026_09_26/README.md` `521d9ac36a93a27dcd6c995f78743ae9b1de4304095911871d81e6a70f9ecaac` ✓ (all match `SOURCE_MANIFEST.json`).
**Cross-checked landmarks:** `results/AS033/AS033-20260927-r01/landmarks.json` (y_p, h_p, y_star, φ(y_star) agree to 50 digits).

---

## 1. Precise claim, symbol dictionary, boundary conditions, assumptions

Symbols (framework contract §Branch dictionary; `B = g_bar = g_N > 0`, `y = B/a0`, `g` total radial acceleration, `x = g/a0`, units m/s² for g, B, a0; y, x, h, ν dimensionless):

| Symbol | Definition | Status |
|---|---|---|
| `a0` | `kappa*c*sqrt(G*rho_Lambda)`, `kappa = 1/2` | framework input (adopted) |
| `h(y)` | phantom part: `x = y + h(y)`, `h = x − y` | framework input |
| `dg/dB` | `1 + h'(y)` (task math line; derivative w.r.t. B = a0·y) | identity |
| PHYS | physical monotonicity: `dg/dB > 0` all B > 0 (total force strictly invertible) | claim to establish per branch |
| PHAN | phantom monotonicity: `h'(y) > 0` all y > 0 | claim per branch |

Branches (contract): Q `g² = B² + a0B`; RAR `ν = 1/(1−e^{−√y})`, `g = B·ν`; MU2 `μ₂(x) = 1−(1+x/2)^{−2}`, `μ₂(x)·g = B`; EXP (historical, comparison only) `μ = 1−e^{−x}`, `μg = B`; MONO `h'_mono = max(h'_RAR, δh_p/(y+y_p))`, `δ = 0.05`, spliced at `y_star`, `h_mono(y) = h_RAR(y_star) + δh_p·ln((y+y_p)/(y_star+y_p))` on the continuation.

Boundary/domain: `y ∈ (0, ∞)`; each branch normalized to `h(0⁺) → 0` (deep MOND `g² → a0B` as `y→0` checked per branch below); Newtonian limit `dg/dB → 1` where it exists. Both a0 footings (canonical `9.3619e-11`, alternative `1.1279e-10 m/s²`) — every statement below is dimensionless in y, so both footings apply unchanged; SI examples quoted separately per footing (never mixing fixed ρ_Lambda and fixed κ).

**Precise claims (this run establishes):**

1. **(Criterion, exact.)** On ANY kernel of the declared class `x = y + h(y)`: `PHYS ⇔ 1 + h'(y) > 0 ∀y>0 ⇔ h'(y) > −1 ∀y>0`. `PHAN` is the strictly stronger `h'(y) > 0 ∀y>0`.
2. **(Implication, exact.)** `PHAN ⇒ PHYS` on the whole class (indeed `h' > 0 ⇒ dg/dB > 1`). The converse is FALSE. Therefore **no kernel in the declared class can be phantom-monotone and physical-nonmonotone** (impossibility direction), and no such counterexample exists on Q, RAR, MU2, EXP or MONO.
3. **(Branch verdicts.)** Q: PHYS and PHAN, `dg/dB = (2y+1)/(2√(y²+y)) > 1`. MONO: PHAN by construction (`h'_mono ≥ δh_p/(y+y_p) > 0`) hence PHYS with `dg/dB > 1`; C¹ at the splice but **not C²** (jump `−0.0347447136`). RAR: PHYS everywhere (`1 + h'_RAR > 0` exactly) but PHAN fails on `(y_p, ∞)` (`h'_RAR < 0`, confined to `(−1,0)` — max dip `−0.0324`). MU2: PHYS everywhere; PHAN iff `x < 2` iff `y < 3/2` (exact algebraic root). EXP: PHYS everywhere; PHAN iff `x < 1` (exact). Both footings: statements dimensionless.
4. **(Sharpness control.)** `h'(y*) < 0` with `|h'(y*)| < 1` does **not** imply non-invertibility (RAR on `(y_p, ∞)` is the counterexample to that naive claim). Real non-invertibility requires `h' ≤ −1` somewhere; the kernel `h(y) = −y·tanh y` realizes it (`dg/dB < 0` on `[1, ∞)`, exact), with phantom `h' < 0` everywhere.

## 2. Step 2 — invertibility vs phantom monotonicity, RAR vs MONO on their domains

**Total-force invertibility:** `dg/dB = 1 + h'(y)`. Because `h' > 0 ⇒ 1 + h' > 1`, phantom monotonicity is strictly sufficient. The gap between the two concepts is exactly the interval `h' ∈ (−1, 0]`: a decreasing phantom whose slope stays above −1 leaves the total relation strictly increasing.

**RAR:** `h_RAR(y) = y/(e^{√y} − 1)`, with `s = √y`, `t = e^s`:

```
h'_RAR(y) = (2(t−1) − s·t) / (2(t−1)²)                          (closed form)
```

- Sign of `h'`: `2(t−1) − s·t > 0 ⇔ 2(e^s − 1) > s·e^s`. Root `s_p` solves `(2−s_p)e^{s_p} = 2` (transcendental; **bracketed** numerically `s_p = 1.5936242600400400…`, `y_p = s_p² = 2.5396382821881653…`, consistent with the task landmark `y_p ≈ 2.5396` and with AS033 to 50 digits). `h'_RAR > 0` on `(0, y_p)`, `= 0` at `y_p`, `< 0` on `(y_p, ∞)`; `h_RAR(y_p) = h_p = 0.6476102378919148…` (task landmark `0.647610`). Phantom NOT monotone on `(0,∞)`.
- Physical: `1 + h'_RAR = t·(2(t−1) − s)/(2(t−1)²)`, and `2(e^s − 1) > s` for all `s > 0` since `e^s ≥ 1 + s` gives `2(e^s−1) ≥ 2s > s`. Hence **`1 + h'_RAR(y) > 0` for all `y > 0`: RAR is physically monotone everywhere** (`dg/dB ∈ (0, ∞)`, in fact `→ ∞` as `y→0⁺` and `→ 1⁻` as `y→∞`).
- Hence RAR is precisely a branch where **PHYS holds and PHAN fails**, with the phantom dip confined to `(−1, 0)`: grid minimum `h'_RAR = −0.0323805595` at `y ≈ 6.31`; dense scan minimum of `1 + h'_RAR` on `(y_p, 100]`: `0.9675525463` (finite check; the > 0 statement is the exact inequality above).

**MONO (operative):** `h'_mono(y) = max(h'_RAR(y), φ(y))`, `φ(y) = δh_p/(y + y_p)`, `δ = 0.05`:

- `φ(y) > 0` for all `y > 0` (product of positives; Lean-certified `mono_floor_pos`), so `h'_mono ≥ φ > 0` — **PHAN by construction**, with the floor `φ(y)` as the uniform positive margin.
- `1 + h'_mono ≥ 1 + φ(y) > 1` — **PHYS with margin strictly exceeding 1** (Lean `mono_physical_margin`).
- Splice: `y_star = 2.3374124052663294…` solves `h'_RAR(y_star) = φ(y_star) = 0.006639363412377466…` (bisection residual `1.7e-51`; task landmark `2.3374`); `y_star < y_p` so on `(0, y_star)` `h'_mono = h'_RAR > 0` and on `(y_star, ∞)` `h'_mono = φ > 0`. `h_mono` and `h'_mono` continuous at `y_star` by construction (C¹ join), but
- **C² kink:** `h''` jumps by `J2 = h''_RAR(y_star) − φ'(y_star) = −0.0361060616 + 0.0013613480 = −0.0347447136` (magnitude `0.0347447`; matches AS033's printed landmark `0.0347447135548` — AS033's code line `−φ′−h″ = 0.0374674` contradicts its own label; the physically correct jump is the label's value, reproduced here). The splice is C¹ but not C²; smoothing is a declared separate candidate (AS048).
- φ is the operative gate-12 "specified RAR segment and MONO continuation preserved" ingredient: below `y_star` MONO **is** RAR; above it, ν_mono/ν_RAR stays within `max dex = 0.01037` at `y = 14.35` (fine scan over `[10,30]`; FRIED_CHICKEN requirement 1 claims `0.0104 dex` at `y = 14.35` — reproduced), while the *derivatives have opposite signs* there (`h'_RAR(14.35) = −0.02172 < 0`, `h'_mono(14.35) = φ(14.35) = +0.001917 > 0`). **Matching the deep asymptote does not make two kernels equivalent** — RAR and MONO coincide in the deep law yet differ in phantom slope on an open set; Q and RAR share `h ≈ √y` at `y→0` but `h'_RAR − h'_Q → −1/2` there (numerics at `y = 10⁻⁶`: `h'_RAR = 499.50012`, `h'_Q = 499.00075`; exact: `h'_Q = 1/(2√y) + 3√y/4 + O(y^{3/2})`, `h'_RAR = 1/(2√y) − 1/2 + √y/8 + O(y^{3/2})`).

## 3. Step 3 — algebra, scale factors, signs, units, asymptotics

**Q branch.** `h_Q(y) = √(y²+y) − y`; `h'_Q(y) = (2y+1)/(2√(y²+y)) − 1`; `dg/dB = 1 + h'_Q = (2y+1)/(2√(y²+y))`. Sign, exact: `(2y+1) > 2√(y²+y)` since squaring gives `4y²+4y+1 > 4y²+4y` (`1 > 0`); both sides positive for `y > 0`. Hence `dg/dB > 1 > 0` and `h'_Q > 0`: **Q is phantom- and physically-monotone**. Limits and asymptotics (leading neglected terms stated):

```
deep (0 < y < 1):      x(y) = √y + ½ y^{3/2} − ⅛ y^{5/2} + O(y^{7/2})
                       h_Q   = √y + ½ y^{3/2} − ⅛ y^{5/2} − y + O(y^{7/2})
                       leading neglected term:  (1/16) y^{7/2} − (5/128) y^{9/2} + …   (verified: |x − asym| = 3.91e-20 at y = 1e-4 = 5/128·(1e-4)^{9/2})
Newtonian (y > 1):     h_Q = ½ − 1/(8y) + 1/(16y²) + O(y^{-3})
                       dg/dB = 1 + 1/(8y²) + O(y^{-3})   → 1⁺      (verified: |h − asym| = 3.88e-8 at y = 100)
phantom bound:         0 ≤ h_Q(y) < 1/2          (h_Q → 1/2⁻)
```

Units: `dg/dB` dimensionless; `B = a0·y`; `g = a0·(y + h)`. Newtonian recovered as `g = B + ½a0(1 − a0/(8B) + …)`, i.e. `g → g_N + ½a0`, the QUMOND-style constant offset.

**RAR.** Deep expansion of `h_RAR = s²/(e^s − 1) = s − s²/2 + s³/12 − s⁵/720 + O(s⁷)`, `s = √y` (series of `s/(e^s−1)`, converges `|s| < 2π`):

```
deep (0 < y < 1):      h_RAR = √y − y/2 + y^{3/2}/12 − y^{5/2}/720 + O(y^{7/2})
                       x = y + h_RAR = √y + y/2 + y^{3/2}/12 + …   →  g² = a0B + O(B^{3/2})   (deep MOND)
                       leading neglected term: − y^{5/2}/720   (verified: |h − asym| = 3.31e-19 at y = 1e-4 = (1e-2)^7/30240)
Newtonian (√y > 1):    h_RAR = y e^{-√y}(1 + e^{-√y} + O(e^{-2√y}))   (superpolynomial; h_RAR(100) = 0.00454,
                       h_RAR(1e6) → 5.08e-429);  dg/dB = 1 + h' → 1⁻
sign equivalence:      0 < h'_RAR(s) ⇔ 2(e^s − 1) > s e^s           (Lean-certified rar_hprime_pos_iff)
physical monotonicity: 1 + h'_RAR(s) = t(2(t−1) − s)/(2(t−1)²) > 0  ⇔  2(e^s−1) > s         (Lean-certified)
```

**MONO continuation** (`y ≥ y_star`): `h_mono = C + δh_p·ln(y + y_p)` with `C = h_RAR(y_star) − δh_p·ln(y_star + y_p)`, so `dg/dB = 1 + φ(y) = 1 + δh_p/(y+y_p)`; leading neglected term `−δh_p·y_p/(y+y_p)²`; numerics at `y = 10⁸`: `dg/dB − 1 = 3.238051e-10 = δh_p/y·(1 + O(y_p/y))` ✓. `ν_mono/ν_RAR` max `10^{0.01037} − 1 ≈ 2.4%` at `y = 14.35`.

**MU2** (`x`-parametrization; `μ₂(x)·x = y`):

```
y(x) = x(1 − (1+x/2)^{-2});   dy/dx = 1 − (1+x/2)^{-2} + x(1+x/2)^{-3}
dy/dx > 0 ∀x>0   since  (dy/dx)(1+x/2)³ = (1+x/2)³ − (1+x/2) + x = (1+x/2)(x/2)(2+x/2) + x > 0   (exact, Lean)
h_MU2(x) = x(1+x/2)^{-2};   dh/dx = (1 − x/2)(1+x/2)^{-3}
⇒ PHYS everywhere (dx/dy = 1/(dy/dx) > 0);  PHAN ⇔ x < 2 ⇔ y < y(2) = 3/2  (exact algebraic root x = 2, h-peak 1/2)
deep: y = x² − ¾x³ + …   (g² → a0B)   ;   Newtonian: dy/dx → 1 (both verified on grid)
```

**EXP (historical, comparison only):** `y(x) = x(1 − e^{−x})`; `dy/dx = 1 − e^{−x}(1−x) > 0 ∀x>0` (exact: for `x ≥ 1`, `(1−x) ≤ 0`; for `0<x<1`, `e^{−x}(1−x) ≤ 1−x < 1`); `h = xe^{−x}`, `dh/dx = (1−x)e^{−x}`: **PHYS everywhere; PHAN ⇔ x < 1** (exact; `y(1) = 1 − 1/e = 0.6321205588…`, h-peak `1/e`). Historical branch: any transfer to the operative target requires an explicit bridge (none claimed here).

## 4. Step 4 — independent checks (different representations); actual residuals

50-digit (mpmath) evaluation on the mandated grid `y = 10^k`, `k = −10…8`, step 0.1 (181 points; x-grid identical for MU2/EXP). Maximum absolute residuals:

| Check | Representation | Max residual |
|---|---|---|
| Q forward law | `x² − (y²+y)`, `x = y + h_Q` | `2.41e-35` (abs; ill-conditioned cancellation at y=1e8), **relative `2.61e-51`** |
| Q substitution into differentiated law | `2x·dx/dy − (2y+1)` | `1.79e-43` |
| Q closed form vs mp.diff | `h'_Q − d/dy h_Q` | `1.09e-47` |
| RAR representation | `x − y·ν_RAR` | `2.67e-51` |
| RAR closed form vs mp.diff | `h'_RAR − d/dy h_RAR` | `8.76e-47` |
| MONO derivative rule | `h'_mono − max(h'_RAR, φ)` | `0.0` (definitional) |
| MONO value continuity at y_star | both pieces | `0.0` |
| MU2 / EXP forward | `h + y(x) − x` | `1.79e-43` / `1.71e-49` |

Margins (min over grid): `dg/dB_Q − 1 ≥ 1.25e-17` (at y=1e8; exact `~1/(8y²)`); `1 + h'_RAR ≥ 0.9676`; `h'_mono − φ ≡ 0`; `dy/dx|_{MU2} ≥ 2e-10` (at x=1e-10, exact `~2x`); `dy/dx|_{EXP} ≥ 2e-10`. Landmarks reproduced against AS033 to 50 digits: `y_p = 2.5396382821881653249988817897743659023689841775413`, `h_p = 0.64761023789191485964720196197595458120902067209651`, `y_star = 2.3374124052663294555581233032011988607921527655904`, `φ(y_star) = 0.0066393634123774664319402003748430201817060453966306`. C² jump: `h''_RAR(y_star) = −0.0361060615985`, `φ'(y_star) = −0.0013613480437`, `J2 = −0.0347447136` (matches AS033 printed `0.0347447135548`).

**Footings.** `ρ_Λ(canonical a0) = 5.84441245402e-27 kg/m³`, `ρ_Λ(alternative) = 8.48308961956e-27 kg/m³`, ratio `1.4514871574` (κ fixed); `B_star = y_star·a0`: canonical `2.18826212e-10`, alternative `2.63636745e-10 m/s²`; `B_p = y_p·a0`: `2.37758396e-10` / `2.86445802e-10 m/s²`. No per-object a0 fits. All monotonicity results dimensionless ⇒ both footings apply unchanged.

## 5. Step 5 — negative controls (each capable of failing) and strongest surviving statement

**NC1 — declared control (capable of failing, it is the trap named in the task).** *"Declare total-force noninvertibility merely from a negative h′ whose magnitude is below one."* RAR on `(y_p, ∞)` has `h'_RAR < 0` (min `−0.03238` on grid, `|h'| < 1`) but `1 + h'_RAR > 0` everywhere (exact: `2(e^s−1) > s`). **Status: the naive claim FAILS and is rejected** — a negative phantom slope with `|h'| < 1` is *not* evidence of non-invertibility; the sharp criterion is `h' < −1`.

**NC2 — constructive counterexample kernel (capable of failing).** `h(y) = −y·tanh y`: `x = y(1 − tanh y) > 0` for all `y > 0`, `h(0) = 0`; `dg/dB = 1 − tanh y − y·sech²y = 2e^{−2y}(1 + e^{−2y} − 2y)/(1 + e^{−2y})²`. Exact sign: `1 + e^{−2y} − 2y < 0` strictly for `y ≥ 1` (decreasing, `e^{−2} − 1 < 0` at `y = 1`) ⇒ **`dg/dB < 0` on `[1, ∞)`: physical monotonicity genuinely fails**; root bracketed `dg/dB(0.5) = +0.14466`, `dg/dB(0.7) = −0.04869` ⇒ root in `(0.5, 0.7)`. Phantom `h' = −tanh y − y·sech²y < 0` everywhere (phantom decreasing; at `y = 1`: `h' = −1.18157 < −1`). This shows real non-invertibility needs `h' ≤ −1` somewhere — the criterion `h' > −1` is sharp, not merely sufficient.

**NC3 — impossibility direction.** Search for a phantom-monotone + physical-nonmonotone kernel in the declared class: none exists **by the algebraic implication** `h' > 0 ⇒ 1 + h' > 1` (Lean `phantom_implies_physical`). All declared branches consistent: `h'_Q > 0`, `h'_RAR > 0` on `(0, y_p)`, `h'_mono ≥ φ > 0` everywhere.

**NC4 — shared asymptote ≠ equivalent kernel.** RAR and MONO share the deep law (`x = √y + y/2 + …` for `y < y_star`) yet have opposite phantom slopes on `(y_star, ∞)`; Q and RAR share `h ≈ √y` yet `h'_RAR − h'_Q → −1/2 ≠ 0` as `y → 0` (verified numerically at `y = 1e-6`: `499.50012 − 499.00075 = 0.49937`).

**NC5 — exact algebraic sign checks (MU2/EXP, not grid-dependent roots).** `dh/dx|_MU2` at `x = 1.9, 2.0, 2.1`: `+0.0067432, 0, −0.0058037`; `y(2) = 3/2` exactly. `dh/dx|_EXP` at `x = 0.9, 1.0, 1.1`: `+0.040657, 0, −0.033287`; `y(1) = 1 − 1/e` exactly. Both dy/dx positive on entire grid (min `2e-10`).

**Strongest surviving statement.** Let `x = g/a0 = y + h(y)`, `y > 0`. (i) `dg/dB = 1 + h'(y)`; PHYS ⟺ `h'(y) > −1` ∀y; PHAN ⟹ PHYS (sharp: `h' > 0` gives margin `dg/dB > 1`), converse false. (ii) Q: PHYS ∧ PHAN with `dg/dB = (2y+1)/(2√(y²+y)) > 1` (Lean-certified). (iii) MONO (operative): PHAN by construction, PHYS with `dg/dB ≥ 1 + δh_p/(y+y_p) > 1`; C¹, not C² at `y_star` (jump `−0.0347447136`); ν_mono within `0.01037` dex of ν_RAR at `y = 14.35`. (iv) RAR: PHYS on all `y > 0` (exact `2(e^s−1) > s`), PHAN only on `(0, y_p)`. (v) MU2, EXP: PHYS everywhere; PHAN iff `x < 2`, resp. `x < 1` (exact roots). Domain: `y ∈ (0, ∞)` (x ∈ (0,∞)), both a0 footings equally. This is a conditional-lemma collection on the declared branch set — not a closure of any relativistic gate.

## 6. First-principles ledger

- **Framework inputs (adopted):** `a0 = kappa·c·√(Gρ_Λ)` with `kappa = 1/2`; branch equations Q / RAR / MU2 / EXP / MONO (h'_mono max-rule, δ = 0.05); `G = 6.67430e-11`, `c = 299792458` (SI footings only); task landmarks `y_p ≈ 2.5396, y_star ≈ 2.3374, h_p ≈ 0.647610` (reproduced to 50 digits, so no independent input was actually needed).
- **Derived here (all exact unless marked finite-check):** the criterion `h' > −1`; the implication `PHAN ⇒ PHYS` and its sharpness; Q sign identities & asymptotics (leading neglected terms stated); RAR closed-form `h'`, sign equivalence `2(e^s−1) > s·e^s`, physical monotonicity `2(e^s−1) > s`; MONO floor, C¹/C² splice analysis, dex bound (finite scan) ; MU2/EXP exact dy/dx positivity and exact phantom roots `x = 2`, `x = 1`; the `h = −y·tanh y` counterexample (exact sign on `[1, ∞)`).
- **Not derived:** the transcendental root `s_p` (bracketed numerically only); any statement through the heat filter `S`; any statement beyond the declared branch set.

## 7. Closure implication, next unresolved implication, follow-ups

- **Closure implication (gate 1 / gate 12, A02 kernel fidelity):** the operative MONO kernel's local response is strictly monotone (`1 + h'_mono > 1`) on the whole declared domain — a necessary condition for the quasistatic equation `∇²Φ = 4πGρ_b + S*∇·[(ν_mono(|∇Su|/a0) − 1)∇Su]` to define a well-posed inversion of `Φ` given `u` in the same cell. This run only supplies the local/algebraic part; the C² kink (`−0.0347` jump at `y_star`) means second-derivative/regularity results cannot be transferred through it without smoothing (AS048).
- **Next unresolved implication:** monotonicity of the *local* response does not survive the heat filter automatically: show that the map `u ↦ 4πGρ_b + S*∇·[(ν_mono(|∇Su|/a0)−1)∇Su]` is monotone/invertible on its function-space domain (or produce a filtered counterexample). This is the first missing bridge between the algebraic monotonicity proven here and the operative field equation.
- **Suggested follow-up (child spec ready, not dispatched):** `AS036.C01` — "Filtered-response monotonicity for the MONO phantom source": construct the heat-filtered operator and prove/refute a coercive monotonicity estimate on the declared domain; dupe-checked against AS041 (spherical obstruction), AS042 (filter order), AS1116 (Nemytskii map low-field), AS1117 (graph closure) — none state the operator-level monotonicity transfer for the operative S-filtered MONO equation. Pointer: `branches/AS036/` (not created — no runner in this wave).

**Dependencies discovered (newly recorded):** none beyond the stated sources; cross-check dependency on AS033 landmarks (completed, matches).
