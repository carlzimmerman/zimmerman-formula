# AS034 — Constructing the MONO continuation by integration

**Run:** `AS034_sa3-48c390dc_20260928T020629Z`
**Worker:** Hermes subagent `sa-3-48c390dc` (deepseek/deepseek-v4-flash-0731 via openrouter), dispatched from the reservation in `deepseek_push/astra_spawn_ideas/claims/AS034.json` (state=running, dispatched 2026-09-28T01:58:22Z).
**Branch:** operative filtered MONO only. Q, RAR, MU2, historical EXP remain separate comparison branches; no conclusion below crosses branches.
**Task file SHA-256:** `31d7c3de6a97a1b2ca4a9b2ffdf726b2a5eb36dc4cdbc0aece2221d38421a6cf` (matches claim file). All three pinned sources verified against SOURCE_MANIFEST.json: README `91a5fac4…`, FRIED_CHICKEN_SPEC `98d9149f…`, peer_review README `521d9ac3…` — byte-identical on disk.

---

## 1. Claim, symbols, boundary conditions, assumptions

### Precise claim
Let `y = B/a0 > 0` (dimensionless, `B = g_N` the Newtonian baryonic acceleration, `a0` the framework vacuum scale), and

```text
h_RAR(y) = y (nu_RAR(y) - 1),   nu_RAR(y) = 1/(1 - exp(-sqrt(y))).
```

The operative MONO derivative rule is `h'_mono = max(h'_RAR, P)` with `P(y) = delta*h_p/(y + y_p)`, `delta = 0.05`, `y_p` the unique peak of `h_RAR`, `h_p = h_RAR(y_p)`. Let `y_star` be the unique crossing `h'_RAR(y_star) = P(y_star)`.

**Claim:** on the continuation domain `y > y_star` the max-rule is solved exactly by

```text
h_mono(y) = h_RAR(y_star) + delta*h_p*ln[(y + y_p)/(y_star + y_p)],      (1)
nu_mono(y) = 1 + h_mono(y)/y,                                            (2)
```

i.e. (1) is the antiderivative of `P` fixed by continuity `h_mono(y_star) = h_RAR(y_star)`; the rule is active (never reverts to RAR) on the whole half-line: `h'_mono(y) > h'_RAR(y)` for every `y > y_star`, with equality only at `y = y_star`. The splice is exactly `C^1` and not `C^2`.

### Symbol dictionary
| symbol | meaning | status |
|---|---|---|
| `y` | `B/a0`, dimensionless | dimensionless variable |
| `B = g_N` | Newtonian baryonic acceleration | physical input (not used at fixed value here) |
| `a0 = kappa c sqrt(G rho_Lambda)` | framework vacuum scale | input; `kappa=1/2` **adopted** (not derived), per framework contract |
| `nu_RAR` | `1/(1 - exp(-sqrt(y)))` | framework RAR branch |
| `h_RAR` | `y (nu_RAR - 1) = y/(exp(sqrt(y)) - 1)` | derived from RAR |
| `y_p, h_p` | peak location/value of `h_RAR` | **roots of declared-branch equations, computed** (see §3) |
| `delta` | `0.05` | framework input (dimensionless) |
| `P(y)` | `delta*h_p/(y + y_p)` | the phantom slope rule (max-rule second branch) |
| `y_star` | crossing `h'_RAR = P` | **solved**, not hard-coded (§3) |
| `h_mono, nu_mono` | continuation + response | derived |
| `G, c, rho_Lambda` | constants | framework conventions; `G_N/G_bare/G_cosmo` kept separate (only the measured `G = 6.67430e-11` enters the footing numbers in §7) |

### Boundary conditions and assumptions
1. `y > 0` (physical domain; `y = B/a0` with `B > 0`). At the splice: **value continuity** `h_mono(y_star) = h_RAR(y_star)` — this is the boundary condition that fixes the integration constant, demanded by "joined continuously from the RAR segment" in the framework contract.
2. `delta = 0.05` and `kappa = 1/2` are adopted framework inputs, not derived here.
3. `y_p, h_p, y_star` are real numbers defined by the declared equations; their exact values are transcendental (roots of equations involving `exp`), carried at 50-digit precision numerically. Only the *algebraic identities* among the functions are Lean-certified; the roots are not.
4. Symbolic statement domain for the log: `y + y_p > 0` (automatic on `y > 0` since `y_p > 0`), and `y_star + y_p > 0`.

## 2. Step 1 — Branch equations and derivative of the RAR segment

```text
nu_RAR(y) = 1/(1 - e^{-s}),   s = sqrt(y) > 0
h_RAR(y)  = y (nu_RAR - 1) = y/(e^s - 1)
```
(identity `1 + 1/(e^s - 1) = e^s/(e^s - 1) = 1/(1 - e^{-s})` — checked numerically, residual `≤ 9.3e-48`, control C6.)

Derivative (all scale factors and signs explicit; no limiting regime is used in the main derivation):

```text
d/dy [y/(e^s - 1)] = 1/(e^s - 1) + y * (-1) e^s (e^s - 1)^{-2} * (ds/dy)
    = 1/(e^s - 1) - y e^s / [2 s (e^s - 1)^2],        ds/dy = 1/(2s)
    = [2s(e^s - 1) - y e^s] / [2 s (e^s - 1)^2]  =:  n(s) / [2 (e^s - 1)^2],
n(s) := e^s (2 - s) - 2,   y = s^2.                                                (3)
```

Sign structure (exact, no numerics): `n'(s) = e^s (1 - s)`; `n(0) = 0`, `n(1) = e - 2 > 0`, `n(s) -> -inf` as `s -> inf`. Hence `n` has exactly one root `s_p > 1`: `n > 0` on `(0, s_p)`, `n < 0` on `(s_p, inf)`. The denominator is positive. So `h_RAR` rises strictly to a unique maximum at `y_p = s_p^2`, then falls strictly to 0 as `y -> inf` (since `h_RAR ~ y e^{-sqrt(y)} -> 0`). Also `h'_RAR > 0` on `(0, y_p)`, `h'_RAR = 0` at `y_p`, `h'_RAR < 0` on `(y_p, inf)`.

**Peak (root, not fitted):** `n(s_p) = 0` bracketed on `[1.5, 1.7]` (sign change `+`/`-` verified before bisection), bisection to `1e-48`:

```text
s_p = 1.5936242600400400923230418758751602417890024248186
y_p = 2.5396382821881653249988817897743659023689841775403   (landmark 2.5396 ✓)
h_p = h_RAR(y_p) = 0.64761023789191485964720196197595458120902067209651  (landmark 0.647610 ✓)
h'_RAR(y_p) = 2.6e-50  (peak residual)
```

**Splice (solved, not hard-coded):** the crossing `h'_RAR(y) = P(y)` bracketed on `[2.30, 2.40]` (verified `f(2.30) > 0`, `f(2.40) < 0` before bisection):

```text
y_star = 2.3374124052663294555581233032011988607921527655904   (landmark 2.3374 ✓)
h_RAR(y_star) = 0.64696036932497512497834600819678228815904048678739
h'_RAR(y_star) = P(y_star) = 0.0066393634123774664319402003748430201817060453966319
delta*h_p = 0.032380511894595743
```

Uniqueness of the crossing: on `(1, inf)` for `s`, `n(s)` is strictly decreasing and the denominator strictly increasing, so `h'_RAR` is strictly decreasing on `(y > y_star)`-relevant region `s > 1`; on `(0, y_star)` the difference `D_alt := h'_RAR - P` is strictly positive on the whole sampled log-grid (`min D_alt = 0.01422528` at `y ≈ 1.99526`, 104/104 points positive; fine scan below the splice positive with the only zero at the endpoint `y_star`). The crossing is therefore the **unique** splice of the max-rule on `(0, inf)` (exact on the decreasing arm, numerically bracketed on `(0, y_star)`).

## 3. Step 2 — Integration and the integrated branch

The operative second branch of the max-rule is the slope `P(y) = c/(y + y_p)` with `c := delta*h_p`. Its antiderivative, with the substitution `u = y + y_p`, `du = dy`:

```text
∫ P(y) dy = c ∫ dy/(y + y_p) = c ln(y + y_p) + C.       (4)
```

(The identity `d/dy ln(y + y_p) = 1/(y + y_p)` for `y + y_p > 0` is the Lean-certified antiderivative identity, see §8; no scale factor, sign or unit ambiguity: `c` has the same dimensionless units as `h`; the log argument `y + y_p` is dimensionless.)

**Constant fixed by continuity** at the splice:

```text
h_RAR(y_star) = h_mono(y_star) = c ln(y_star + y_p) + C
   =>  C = h_RAR(y_star) - c ln(y_star + y_p),
```
which reproduces equation (1):

```text
h_mono(y) = h_RAR(y_star) + c ln[(y + y_p)/(y_star + y_p)],   y >= y_star.      (1)
```

**Domain of the rule:** the max-rule selects the phantom branch exactly where `P(y) >= h'_RAR(y)`, i.e. `y >= y_star` (with equality at `y = y_star`). On `y > y_star` the integrated form is used; on `0 < y < y_star` the RAR segment remains operative. Both branches are joined at the crossing by construction of `y_star`, so value and first derivative are continuous at the splice.

**Derivative verification of the closed form (C2):** differentiating (1):

```text
h'_mono(y) = c * (1/(y + y_p))  =  P(y),            (chain rule on ln of the ratio)
```
residual `0.0` at all sampled points `y ∈ {2.5, 3, 10, 100, 1e4, 1e8}` (50-digit arithmetic) — the integrated derivative equals the declared phantom slope exactly (Lean-certified as `mono_deriv_rule`).

**Independent quadrature check (C3):** numerical integration of `P` over `[y_star, y]` with `mp.quad` (50-digit) reproduces `c ln[(y + y_p)/(y_star + y_p)]` at `y = 3, 10, 100, 1e4` with residuals `≤ 8.4e-53`. The fundamental theorem holds on the continuation.

**Exact regularity class at the splice (Step 2 requirement):** `h_mono` is continuous (C1-residual = 0, see below) and its derivative is continuous because `y_star` is the crossing (`h'_RAR(y_star) = P(y_star)`). The second derivative jumps:

```text
h''_mono(y_star+) = -c/(y_star + y_p)^2 = -1.3613480436970371e-3
h''_RAR(y_star)   = -3.6106061598533144e-2    (via mp.diff, independent of hand algebra)
jump: h''_mono(y_star+) - h''_RAR(y_star-) = +3.4744713554836107e-2   (ratio 26.5×)
```
So the splice is exactly `C^1 \ C^2` (a kink in the slope's derivative), and `nu_mono(y) = 1 + h_mono(y)/y` is likewise `C^1 \ C^2` at `y_star`.

## 4. Step 3 — Intermediate algebra, signs, units, limits

All quantities in (1)–(3) are dimensionless (`y, h, nu, delta, c`); no physical unit conversion appears in the derivation. Signs: `c > 0`, `y + y_p > 0`, so `h_mono` is strictly increasing and convex-decreasing-slope on the continuation; `h_RAR` decreases after the peak. No limiting regime is used for the main result; the limits below are checks, with the leading neglected terms:

- **Deep limit `y -> 0+`** (no dynamics here; diagnostic): with `s = sqrt(y)`,
  `h_RAR = s^2/(e^s - 1) = s (1 - s/2 + s^2/12 + O(s^3))`, i.e.
  ```text
  h_RAR(y) = sqrt(y) - y/2 + y^{3/2}/12 + O(y^2).
  ```
  Leading neglected term after `sqrt(y)` is `-y/2` (relative size `sqrt(y)/2`). Numerics: `h_RAR(1e-10)/sqrt(1e-10) = 0.99999500000833…` matching `1 - sqrt(y)/2 + y/12` to `~1e-17`. Hence `nu_RAR ~ 1/sqrt(y)` and the deep law `g^2 = B a0` reproduces (framework identity, on the RAR segment only).
- **Newtonian limit `y -> inf` on the continuation:** `h_mono/y = c ln((y+y_p)/(y_star+y_p))/y -> 0`, so `nu_mono -> 1` and `g -> B` (recovery). Numerics: `nu_mono - 1 = 1.1921232e-8` at `y = 1e8`. Note the phantom itself never decays (`h_mono ~ c ln y`), only its force fraction `h_mono/y` does — an intrinsic property of the declared continuation branch, kept on the MONO branch.

## 5. Step 4 — Independent checks (actual residuals)

| ID | check | method | observed | tolerance set *before* run |
|---|---|---|---|---|
| C1 | splice value continuity | `h_mono(y_star) - h_RAR(y_star)` | `0.0` (50-digit) | `< 1e-40` |
| C2 | derivative identity `h'_mono = P` | analytic derivative of closed form, 6 sample points | `0.0` | `< 1e-40` |
| C3 | fundamental theorem | independent `mp.quad` of `P` vs closed form, 4 endpoints | `≤ 8.4e-53` | `< 1e-45` |
| C6 | representation `h_RAR = y(nu_RAR - 1)` | 181-point grid `y = 10^k`, k = -10..8 step 0.1, + `y = 14.35` | `≤ 9.3e-48` | `< 1e-40` |
| C7a | peak landmark | bracketed root vs 2.5396 | `2.53963828…` | `|· - 2.5396| < 1e-3` |
| C7b | `h_p` landmark | `h_RAR(y_p)` vs 0.647610 | `0.64761024…` | `|· - 0.647610| < 1e-5` |
| C7c | splice landmark | bracketed root vs 2.3374 | `2.33741241…` | `|· - 2.3374| < 1e-3` |
| C7d | 0.0104-dex claim | `max log10(nu_mono/nu_RAR)` over grid **and** dense scan `y ∈ [12,17]` (20001 pts) | `0.01037014956` at `y = 14.35075` | `< 0.0104` |

All pass with wide margins. C3 is a genuinely different representation (quadrature of the slope vs closed-form log).

## 6. Step 5 — Negative controls (capable of failing; each *did* expose the failure mode it targets)

**N1 — omit the integration constant, detect the force jump.** Using `h_zero(y) = c ln[(y+y_p)/(y_star+y_p)]` (correct derivative `P`, constant set to 0) gives `h_zero(y_star) = 0`, while continuity demands `h_RAR(y_star) = 0.64696037`. The force ratio across the splice (on `nu = 1 + h/y`):

```text
g(y_star+)/g(y_star-) = (1 + 0/y_star)/(1 + h_RAR(y_star)/y_star) = 0.78321731,
i.e. a -21.6783 % jump in the total acceleration at the splice.
```
Detected: the integration constant is load-bearing; omitting it produces a discontinuity of the response (`nu` jumps by `h_RAR(y_star)/y_star = 0.2768`). PASS (i.e., control capable of failing and failed as required).

**N2 — switch-back scan of the max-rule (the task's central control).** Define `D(y) := h'_mono(y) - h'_RAR(y) = P(y) - h'_RAR(y)`. The max-rule must never revert to the RAR branch on `(y_star, inf)`:

- Exact on `(y_p, inf)`: `h'_RAR(y) < 0 < P(y)` by the sign structure of §3, so `D > 0` identically — no switching on the whole tail, no numerics needed.
- Numeric on `(y_star, y_p]` and the full continuation: log grid `y_star(1+1e-13) → 1e8` (4001 pts) and linear grids `(y_star, y_p)` and `(y_p, 5)` (1e5 pts each): **0 adjacent-pair sign changes** in every scan; `min D = 8.12e-15` at `y = y_star(1+1e-13)` (approaching the splice, where `D -> 0+` by definition of the crossing); interior minimum `7.03e-8` at `y = 2.3374144`. `D > 0` strictly on the interior; the only zero of `D` on `(0, inf)` is `y_star` itself.
- Complement on the RAR side: `h'_RAR - P > 0` on `(0, y_star)` (min over log grid `0.01422528` at `y ≈ 1.995`; endpoint zero at `y_star` only).

**Conclusion: no premature switch-back anywhere; the splicing point `y_star` is the unique switching point of `max(h'_RAR, P)` on `y > 0`.** If a switch-back had existed, the scan would have found a sign change; the control is genuinely capable of failing (and the C4-omission control did fail in the targeted way).

## 7. Scale footings (mandatory)

The theorem is dimensionless: `h_mono`, `nu_mono`, `y_star`, `y_p`, `h_p`, `delta` are pure numbers; `a0` enters only through the definition of the axis `y = B/a0`. Hence the identical statement applies under both footings; the footing choice merely rescales the physical acceleration axis.

| quantity | canonical | alternative | relation |
|---|---|---|---|
| `a0` [m s^-2] | `9.3619e-11` | `1.1279e-10` | framework |
| `rho_Lambda = 4 a0^2/(G c^2)` [kg m^-3] | `5.8444125e-27` | `8.4830896e-27` | same kappa = 1/2 ⇒ density differs (×1.4512) |
| effective kappa if `rho_Lambda` fixed | `0.5` | `0.602388404` | same density ⇒ kappa differs (×1.2047768) |
| `Lambda = 32 pi a0^2/c^4` [m^-2] | `1.0907998e-52` | `1.5832818e-52` | same-G convention (G_N = G used; G_bare, G_cosmo left separate) |

`kappa = 1/2` is an adopted input, not derived (per framework contract and STANDING: measured 0.465 ± 0.076, consistent with 1/2). No per-object fit of `a0` is made or implied.

## 8. Lean certificate

File: `AS034_certificate.lean` (in this run directory). Command:
`cd /Users/carlzimmerman/new_physics/zimmerman-formula/fable_independent_2026/lean_2026 && lake env lean <abs>/AS034_certificate.lean` — **exit 0**, zero `sorry`.

Theorems (exact algebraic statements only; the transcendental roots `y_star, y_p, h_p` are carried numerically in the Python run, not certified):

| theorem | statement |
|---|---|
| `AS034.antideriv_log` | `deriv (fun y => log(y + yp)) x = 1/(x + yp)` for `0 < x + yp` |
| `AS034.antideriv_ratio` | `deriv (fun y => log((y+yp)/(ys+yp))) x = 1/(x + yp)` for `0 < x + yp, 0 < ys + yp` |
| `AS034.mono_deriv_rule` | `deriv (h_mono c yp ys hRAR_ys) x = c/(x + yp)` (the operative phantom-slope rule) |
| `AS034.mono_continuity_at_splice` | `h_mono c yp ys hRAR_ys ys = hRAR_ys` (integrated-form continuity at the splice) |

**Axioms of all four theorems:** `{propext, Classical.choice, Quot.sound}` — the hard bar is met. (Technical note: statements use Mathlib's `deriv` rather than ad-hoc `HasDerivAt` because the two competing ℝ-over-ℝ normed-module instances make cross-context `HasDerivAt` unification fail; `deriv` is one fixed constant, so the statements are unambiguous.)

## 9. Strongest surviving statement

> **Theorem (scoped, MONO branch only).** Let `c = delta*h_p > 0`, `y_p` the unique maximum of `h_RAR(y) = y/(e^{sqrt(y)} - 1)`, and `y_star` the unique solution of `h'_RAR(y_star) = c/(y_star + y_p)` (numerically `y_star ≈ 2.3374124053`, `y_p ≈ 2.5396382822`, `h_p ≈ 0.6476102379`, all consistent with the framework landmarks `2.3374 / 2.5396 / 0.647610`). Then on `y >= y_star` the max-rule `h'_mono = max(h'_RAR, c/(y+y_p))` is solved by `h_mono(y) = h_RAR(y_star) + c ln[(y+y_p)/(y_star+y_p)]`: the antiderivative of the phantom slope fixed by value-continuity at the splice, with `h'_mono = c/(y+y_p)` (Lean-certified) and strict dominance `h'_mono > h'_RAR` on `(y_star, inf)` — the rule never switches back. The splice is exactly `C^1 \ C^2` (second-derivative jump `+3.4745e-2`). `nu_mono(y) = 1 + h_mono(y)/y` satisfies `nu_mono -> 1` as `y -> inf` (Newtonian recovery) and deviates from `nu_RAR` by at most `0.01037` dex on the tested grid, extremal at `y ≈ 14.35` (consistent with the amended 0.0104-dex claim). The result is dimensionless and applies identically on both `a0` footings; `kappa = 1/2` remains adopted input.

## 10. What this does not establish (limitations)

- Nothing about the **filtered field equation** `Delta Phi = 4pi G rho_b + S* div[(nu_mono(|grad S u|/a0) - 1) grad S u]`, the heat filter `S`, well-posedness, criterion B, or stability — those are separate gates (the C^1 kink's impact on the filtered source is the proposed child C01).
- The "within 0.0104 dex" bound is **numerically supported** on the sampled grid plus a dense scan of `[12, 17]`, not an exact global inequality over `(y_star, inf)` (asymptotics give ratio → 1 at both ends, but a derivative analysis of the extremum was not performed).
- The values `y_p, h_p, y_star` are 50-digit numerical roots (transcendental); their exact closed forms are not asserted. Crossing **uniqueness on (0, y_star)** is numerically bracketed, not a proof.
- The splice `C^1 \ C^2` regularity is for the unfiltered kernel; `nu_mono ∘ |grad S u|/a0` regularity requires composition estimates not attempted here.
- AS033 (splice location, the explicit prerequisite) has **no executed result in `results/` at run time**; this run re-solved the crossing independently as a control rather than importing a reviewed value. AS032 (phantom maximum) likewise had no executed result in `results/`. The `y_p/h_p` values were re-derived here from the declared equations.
- No claim about Q, RAR-as-law, MU2, or historical EXP branches; no closure claim for the thirteen-item target.

## 11. Next unresolved implication and closure position

**Gate:** requirement 1 (operative filtered `nu_mono`), requirement 12 (RAR segment + MONO continuation preserved). This result pins the **constitutive function** of the operative branch: exact integrated form, derivative rule, splice regularity class, no switch-back. The first missing bridge to the full theory: **the regularity and ellipticity of the static filtered operator across the `C^1 \ C^2` splice** — what distributional class the phantom source term `S* div[(nu_mono(|grad S u|/a0) - 1) grad S u]` has when `|grad S u|/a0` crosses `y_star`, and whether the second-order operator keeps a uniform ellipticity ratio across the kink (the coefficient `nu_mono - 1` is continuous but its derivative jumps). Proposed child: `AS034.C01` (spec written to `deepseek_push/astra_spawn_ideas/branches/AS034/AS034.C01.md`, **not dispatched** — no runner available in this wave).

Also explicitly open: exact global bound at 0.0104 dex; the AS033/AS032 reviewed values once those seeds land; criterion B and well-posedness of the filtered equation; the action from which the max-rule is derived (not claimed here).

## 12. Reproducibility

- `AS034_analysis.py` — main computation (grid, roots by bracketed bisection, all controls C1–C8, footings). Run: `python3 AS034_analysis.py`; 4.23 s wall, 20.9 MB peak RSS, 1 thread, mpmath 50 dps. Output: `raw_outputs/analysis.json`, log `raw_outputs/run_stdout.log`.
- `AS034_supplementary.py` — C^2-jump, dense dex scan, RAR-side dominance scan. 0.77 s wall, 18.3 MB RSS. Output: `raw_outputs/supplementary.json`.
- `AS034_certificate.lean` — Lean 4 certificate, 4 theorems, exit 0; `raw_outputs/lean_certificate.out`.
- Enforced bounds: single thread (`OMP/MKL/OPENBLAS/NUMEXPR_NUM_THREADS=1`), declared `<=120 s` wall / `<=512 MB`; actual 4.23 s / 20.9 MB, enforced and recorded in `analysis.json` and `supplementary.json`.
