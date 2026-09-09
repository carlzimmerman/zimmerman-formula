# L15 — the IC6 obstruction at σ = 1, the value the physics forces

2026-09-08. Lane L15 of [CHARTER.md](CHARTER.md); discharges open challenge **B1** of
[HANDOFF_CONTRACT.md](HANDOFF_CONTRACT.md).
Script: [L15_sigma_one.py](L15_sigma_one.py) → [L15_sigma_one.out](L15_sigma_one.out).
Exit 2 by design (30 checks, 29 PASS; the single FAIL is the hoped-for outcome, which is false).

Method: nothing under `closure_2026/integrable_clock_construction_2026/` was imported, executed or copied.
The IC5/IC6/IC7 density and curvature coefficient were transcribed by hand into sympy with **σ left symbolic**,
differentiated, and evaluated at 60 digits with mpmath. The mandatory control reproduced L4's confirmed
`S_4'(1) = −11.1407711251147987` at the published parameters *before* σ was moved.

---

## The one-line answer

**The obstruction does not vanish at σ = 1. It persists with the same sign, is 1.81× larger, and IC7's
counterterm is needed 1.78× more strongly. No value of σ in IC-4's own admissible interval (0, 1] would have
removed it — that is a theorem, not a numerical accident. The tensor cone, the DOF count and the absence of a
ghost all survive σ = 1 untouched.**

| quantity | σ = 1/3 (published) | σ = 1 (Cherenkov) |
|---|---:|---:|
| `p_R` | 5.04859346525 | 9.81244706242 |
| `q_R` | −2.89322254947 | −4.67966764841 |
| `A_R` | 2.73988424349 | 5.32523945163 |
| `B_R` | −1.57015908109 | −2.53966728415 |
| `dF/dj` | −2.05478477334 | −4.22559473247 |
| `dJ_T/dj` | −1.89310424406 | −3.89310424406 |
| **`S_4'(1)`** | **−11.1407711251147987** | **−20.194205022906776** |
| `S_4` at `j = 1.007` | −0.0752605165258 | −0.13431570871 |
| growth `λ²/k⁴` at `j = 1.007` | 0.0345698565 | 0.06222544909 |
| `c_7` at `j = 1.007` | 0.00235189114143216 | 0.00419736589718309 |
| IC7 window (`θ=1` edge / `θ=0` edge) | `j` = 1.0736445 / 1.1315852 | 1.0499108 / 1.0855286 |
| `c_T²` | 1 (exact) | 1 (exact, same identity) |
| `A_0` at the witness | 0.461453103619 | 0.461453103619 (identical) |

---

## 1. Where σ enters — I had to determine this from the action

The IC files fix σ = 1/3 and say only *"more generally the calculation covers 0 < σ ≤ 1"* and *"the squared-speed
parameter σ is a construction choice"*. **No published file states σ's downstream role**, so I derived it.
The result is clean and worth recording in the IC series:

> **σ reaches the entire IC5/IC6/IC7 machinery through exactly one channel: `p_R`, hence `F`.**

Checked symbolically (`L15-S1`): `ℓ, T, e, d, α, β, γ, b, a₀², Λ, U, h₀` all have zero σ-derivative. Only
`p_R = 8/3 + 4a_*σ`, `q_R = −1 − 3p_R/8`, `A_R = 3p_R/(16ℓ²)`, `B_R = 3q_R/(16ℓ²)` move, and they reach the
dynamics only through `F = A_R(ξ − 1/4) + B_R(u − 2/3)`, hence through `J_T` and `c = m e^{uξ}J_T`.

Two consequences that make the whole calculation tractable, both proved symbolically (`L15-S5`):

- **`h` restricted to the isotropic slice `τ = 0` is exactly σ-free** — the entire `F`-dependence sits in the
  `τ/J` term. Therefore the witness, the auxiliary constraints `h_ξ = h_u = 0`, their Hessian
  `−[[24,−27],[−27,2T+135/8]]`, `det = 12(4T−27)`, the branch tangent `dq/dj`, **`M12` and `M22`** are all
  σ-independent. At `j = 1.007` the solve returns `ξ = 0.24297809`, `u = 0.66347046` at σ = 1 and σ = 1/3 alike,
  agreeing to 40 digits.
- **Only `M11 = (E/6)(1/J_T − 1)` and `v = (c_ρ/2, D_t c)` carry σ.**

I also re-derived LOCAL_WAVE_REPORT §2 independently (`L15-S2`), which is what licenses reading σ as the squared
sound speed: eliminating `v` from its quadratic Lagrangian gives kinetic coefficient `a_* = 3 − 81/(4T)` exactly
(the `αx/4` and `81ex/(4T²)` terms cancel), source `b(x) = (2/3 + p_R/2)x`, measure-corrected stiffness
`g(x) = (2/3 − p_R/4)x`, and `g = −a_*σx` forces `p_R = 8/3 + 4a_*σ`. `v = 9y/(2T)`, `n = (8T+27)y/(16T)` and the
`q_R` cancellation all reproduce (`L15-S3`).

## 2. The obstruction as a closed function of σ

At the witness `v1 = M11 = 0`, so `S_4(1) = 0` and `S_4'(1) = 4[M11'v2² − 2M12 v1' v2]/M12²` with

    M12 = 2T/9,   M11' = −(e^{1/2}/6) J_T',   J_T' = (9 − p_R T)/(4T − 27),
    v1' = e^{2/3}(p_R T − 9)/(3(4T − 27)),    v2 = e^{1/6} T (3p_R + 4)/54.

Collecting gives

> **S_4'(1; σ) = e^{5/6} (p_R T − 9)(3p_R + 4)(3p_R − 44) / (216 (4T − 27)),   p_R = 8/3 + 4a_*σ.**

This reduces **symbolically** to your boxed identity `−e^{5/6}(5T−27)(8T−27)(8T+27)/(18T²(4T−27))` at σ = 1/3
(`L15-G1`), and it matches the full numerical implicit-function derivative at σ = 1/5, 1/3, 1/2, 9/10, 1, 3/2 to
better than 1e-40 (`L15-G2`). **Suggested for the IC series: this is the σ-general form of your boxed result.**

## 3. Why no admissible σ helps — a theorem, not a number

`S_4'(1;σ)` has **exactly one zero in σ**, at

> **σ_* = 4T/(4T−27) = 3/a_* = 1.67931273219**, i.e. `c_s = 1.2959 c`, **29.6 % superluminal**.

and `σ_* > 1` for **every** `T` in the frozen domain `T > 27/4`. The other two factors are strictly positive for
all σ > 0 (`p_R > 8/3` and `T > 27/4` give `p_R T > 18 > 9`). Hence `S_4'(1;σ) < 0` on the whole of `(0, 1]`
(`L15-R3`). The published factorisation `(5T−27)(8T−27)(8T+27)` obscured this: the sign is really controlled by
`3p_R − 44 < 0`, i.e. by `σ < σ_*`, and IC-4's design interval sits entirely inside that region.

    sigma        p_R          S_4'(1)
    0.05         3.0239557    -5.07339905067
    0.2          4.0958227    -8.21548002461
    0.33333333   5.0485935    -11.1407711251     <- published
    0.5          6.2395569    -14.6420793481
    0.75         8.026002     -18.7290681664
    1.0          9.8124471    -20.1942050229     <- Cherenkov
    1.25         11.598892    -17.6606207073
    1.5          13.385337    -9.75144600916
    1.6793127    14.666667    -6.46e-15          <- sigma_*, 29.6% superluminal
    1.8          15.529071    +8.77397478161

**The sharpest form of the result** (`L15-R3b`): `S_4'` is not monotone. It is most negative at
σ = 0.9806905448 — essentially *at* the Cherenkov-forced value. Of the whole interval IC-4 declares admissible,
the Cherenkov bound selects the point where the obstruction is strongest; σ = 1 sits at 99.94 % of the interval's
worst value. σ = 1/3 was the mildest part of the interval the construction could have been tested on.

The **Cherenkov window is irrelevant to the verdict** (`L15-R2`): `1 − c_s ≤ 2e-15` with `c_s² = σ` gives
`σ ≥ 1 − 4e-15`, over which `S_4'` moves by 4.9e-15 (`dS_4'/dσ = 1.219` at σ = 1). Marginally superluminal does
not help either — reaching `σ_*` needs `c_s = 1.296 c`, which is not "marginal" and is outside IC-4's own
`0 < σ ≤ 1`.

## 4. The other five questions

**Does the frozen domain move?** No (`L15-R4`). `T = −27/16 + 54/(5 ln(9/5))` contains no σ, so `T > 27/4` holds
identically and `det H_qq = 12(4T−27) = 476.952638525` is unchanged to 40 digits. The domain condition in `T` is
untouched; what σ = 1 adds is the *additional* inequality `σ < σ_*`, which is satisfied — and satisfying it is
exactly what makes the obstruction negative.

**Is IC7 still needed?** Yes, and more so (`L15-R6`). `c_7 = −S_4/32` is nonzero and larger at every isotropic
sample: 0.00235189114143216 → 0.00419736589718309 at `j = 1.007` (×1.785). The construction does not simplify.
Two costs get worse:
- **The repair window halves** (`L15-R7`). Because `dJ_T/dj` roughly doubles, `det M` leaves its witness value
  twice as fast: the `θ ≡ 1` plateau ends at `j = 1.0499` instead of 1.0736, and `θ` reaches 0 at `j = 1.0855`
  instead of 1.1316, where the unrepaired `S_4 = −0.9006` (was −0.7341) is restored in full while `η` is still 1.
  L4's "|j−1| < 0.074" becomes **|j−1| < 0.050**.
- **IC7's tensor detuning grows 2.6×** (`L15-R14`). The exact form `c_T,phys² = 1 − 4c_7 R̄₀/c` is unchanged,
  but at the sheared state `4c_7/c` goes from 0.008571 to **0.022593** per unit `R̄₀`.

**Does the tensor sector still give `c_T² = 1`?** Yes, exactly, and for a reason that cannot fail (`L15-R9`).
Re-derived with σ symbolic: `K_T = J_T` and `G_T = J_T` cancel, so `c_T² = 1` **identically in σ**, with the IC5
mutation still returning `J_T`. Cherenkov's tensor arm stays clean at σ = 1.

**Does the DOF count stay 2 tensors + 1 clock?** Yes (`L15-R10`). The count is `(16 − 4 − 6)/2 = 3`, and its two
inputs are both σ-free: the witness Hessian `K = V h_AB` (identical eigenvalues 4.3084046, 40.7253 at both σ) and
LOCAL_WAVE §3's quadratic-Dirac matrix, which **contains no `p_R` at all** — its determinant
`3F²h⁴(4T−27)(8T+x)/(2T) > 0` reproduces symbolically (`L15-S4`). So the scalar sector's constraint rank
(4 second class + 2 first class, 1 physical pair) is σ-independent.

**Ghost?** None, by two independent routes (`L15-R11`). At the witness `A_0 = det M/M22 = −M12²/M22` with both
`M12` and `M22` σ-free, so `A_0 = 0.461453103619` is *exactly* the same at σ = 1; at `j = 1.007` it is 0.463278
(was 0.459336), still positive. Independently, LOCAL_WAVE's reduced scalar kinetic coefficient is
`a_* = 3 − 81/(4T) = 1.786445` with **no σ in it**.

**Is σ = 1 singular or degenerate?** No — it is a regular point (`L15-R12`). Every coefficient that could have
vanished is bounded away from zero at σ = 1: `p_R, q_R, A_R, B_R, a_*, C = 1 + a_*σ = 2.786, det M_* = −13.7501,
M12, M22, det H_qq, J_T(witness) = 1`, and all three factors of the obstruction. The construction's one
degeneracy in σ is the obstruction's own zero at `σ_* = 1.679`. **Luminality does not sit where a coefficient
vanishes here** — which is why the hoped-for simplification does not occur.

## 5. One corrected premise, and one new fact about the branch

I expected `J_T > 0` — IC6's and IC7's stated precondition — to be the thing that fails first at σ = 1. It is
not (`L15-R8`). **The isotropic family itself terminates at a fold of the auxiliary constraint surface at
`j = 1.216488`**, where the real root of `h_ξ = h_u = 0` is lost (`u = 0.5072` there, heading out of `0 < u < 1`).
That fold is σ-independent, for the same reason as everything else on `τ = 0`. `J_T` stays positive all the way
to it at both σ — but its margin at the fold collapses from **0.727 to 0.390**. So `J_T > 0` still holds on the
whole branch at σ = 1, with about half the room. The fold itself is worth noting in IC6: it bounds the isotropic
family the even-sector analysis explores, and it sits only 0.13 beyond IC7's `θ = 0` edge.

## 6. What this lane could NOT compute — named exactly

- **`S4_11(σ = 1)`, the sheared reduced quartic.** IC6_EVEN's `−0.0642323935174161` and IC7's leftover
  `0.0151964888331` are outputs of your *anisotropic* two-mode reduction (`ic6_even_characteristics.py`), which
  this lane does not reproduce and whose σ-dependence is not published in closed form. **The sheared leftover at
  σ = 1 requires re-running that reduction with `p_R = 8/3 + 4a_*σ` at σ = 1.** Same for the antisymmetric mixing
  `N2_21 = 0.000563025148111`. What I *can* report is that the sheared state itself moves (its `τ ≠ 0` makes the
  auxiliary constraints see `F`): `ξ = 0.2427527463 → 0.2393681032`, `u = 0.6635898185 → 0.6620462811`,
  `J_T = 0.9861021597 → 0.9586764466`, `c_7 = 0.002482153 → 0.006344597` (`L15-R13`).
- **The `k²` reduction giving the witness speeds `(σ, 1)`** and IC7's quoted `c_s² = 0.388526918` at `k = 1e5`:
  that needs the background time derivatives `(Ṁ, Ṅ)` of your reduced system. The identification `c_s² = σ` is
  read from LOCAL_WAVE's boxed `z'' + 3z' + σxz = 0` and re-derived here; the finite-`k` correction to it is not.
  Same scope limit as L4.
- Note on notation: `IC10_LOCAL_CLOCK.md` / `OPTICAL_ALIGNMENT.md` use `sigma` for a **different, unrelated**
  quantity (`sigma = −1/4` in the `s8/K8/J8/c8` optical block). Nothing here touches that symbol. A rename in one
  of the two places would prevent a real confusion.

## 7. What this means for the next design equation

IC7's remaining problem was already stated as: find an action-level momentum/curvature modification satisfying
both `N2 = N2ᵀ` and `C4 − B2 A0^{-1} B2ᵀ = 0` on sheared backgrounds. This lane adds three constraints on that
search, all of which are new:

1. **σ is no longer a free dial.** Cherenkov fixes it to 1 within 4e-15. Any future design step that would have
   bought health by tuning σ is unavailable, and the `(0,1]` interval is fully mapped: `S_4'(1;σ) < 0` throughout.
2. **The target has moved 1.81× away**, and IC7 must supply 1.78× more counterterm on a window half as wide,
   while detuning the tensor cone ~2.6× more per unit `R̄₀`. The two conditions are now in sharper competition:
   whatever fixes the sheared mixing must protect `c_T² = 1` against a larger `c_7`.
3. **The one structural positive is genuine and should be leaned on.** `c_T² = 1` is a σ-*identity*, not a tuning;
   `a_*` and `A_0(witness)` are σ-free; the DOF count and constraint rank are σ-free. The healthy khronon and the
   luminal tensor sector are robust to this whole class of parameter motion. Only `M11` and `v` move — which is
   also the precise statement of where a repair has to act.

---

## Verbatim PASS/FAIL

    [PASS] L15-S1  sigma enters through p_R/q_R/A_R/B_R only; 12 constants sigma-free
    [PASS] L15-S2  LOCAL_WAVE reduction re-derived: a_* sigma-free, g = -a_* sigma x forces p_R = 8/3 + 4 a_* sigma
    [PASS] L15-S3  v = 9y/(2T), n = (8T+27)y/(16T), q_R = -1 - 3p_R/8 cancellation
    [PASS] L15-S4  quadratic-Dirac matrix carries no p_R; det = 3F^2h^4(4T-27)(8T+x)/(2T)
    [PASS] L15-S5  h|_{tau=0} sigma-free => witness, Hessian, dq/dj, M12, M22 sigma-free; only M11, v move
    [PASS] L15-C1  witness exact stationary point at both sigma (|h_xi|,|h_u| < 3.11e-60)
    [PASS] L15-C2  auxiliary Hessian identical at both sigma, det = 476.952638525 = 12(4T-27)
    [PASS] L15-C3  dq/dj identical at both sigma, exactly along the null direction chi
    [PASS] L15-C4  the five IC6_EVEN witness coefficients
    [PASS] L15-C5  det(M_star) = -13.750109935689 at both sigma
    [PASS] L15-C6  [MANDATORY CONTROL] S_4'(1)|_{sigma=1/3} = -11.1407711251147987
    [PASS] L15-G1  closed form reduces symbolically to the lead's boxed identity at sigma = 1/3
    [PASS] L15-G2  closed form matches numeric d/dj at sigma = 1/5, 1/3, 1/2, 9/10, 1, 3/2 (< 1.7e-40)
    [PASS] L15-R1  [THE QUESTION] obstruction does NOT vanish: S_4'(1)|_{sigma=1} = -20.194205022906776, 1.81x
    [PASS] L15-R2  verdict uniform across the whole Cherenkov window (swing 4.9e-15)
    [PASS] L15-R3  [THEOREM] one zero at sigma_* = 4T/(4T-27) = 1.679 > 1; S_4' < 0 on all of (0,1]
    [PASS] L15-R3b sigma = 1 is where the obstruction is STRONGEST in the interval (argmax at 0.9807)
    [PASS] L15-R4  frozen domain unchanged; sign really controlled by 3p_R - 44 < 0
    [PASS] L15-R5  isotropic auxiliary solve identical at both sigma to 40 digits at j = 1.007
    [PASS] L15-R6  [SECOND QUESTION] IC7 STILL REQUIRED, c_7 x1.785; no simplification
    [PASS] L15-R7  IC7 repair window halves: |j-1| < 0.074 -> 0.050
    [PASS] L15-R8  branch ends at a sigma-independent FOLD at j = 1.216488, not at J_T = 0; margin 0.727 -> 0.390
    [PASS] L15-R9  [TENSOR] c_T^2 = 1 exactly, sigma-independent identity
    [PASS] L15-R10 [DOF] unchanged: 2 tensor + 1 clock scalar
    [PASS] L15-R11 [GHOST] none; A_0(witness) = 0.461453103619 sigma-free, a_* = 1.786445 sigma-free
    [PASS] L15-R12 [DEGENERACY] sigma = 1 is a REGULAR point; the only degeneracy is sigma_* = 1.679
    [PASS] L15-R13 sheared state moves with sigma; xi, u, J_T, c_7 at sigma = 1 reported
    [PASS] L15-R14 IC7 tensor detuning 4c_7/c: 0.008571 -> 0.022593 per unit Rbar_0
    [PASS] L15-B1  HANDOFF_CONTRACT B1 DISCHARGED: all three re-derive at sigma = 1
    [FAIL] L15-P1  [PROGRAMME REQUIREMENT] "sigma = 1 removes the obstruction, IC7 unnecessary" -- FALSE

29 PASS, 1 designed FAIL, exit 2. The FAIL is the hoped-for outcome, not a reproduction failure; the lead never
asserted that σ = 1 would repair anything.
