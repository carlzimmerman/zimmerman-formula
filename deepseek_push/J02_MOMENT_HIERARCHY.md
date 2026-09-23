# J02 — EVEN-MOMENT HIERARCHY + THE VOLUME-SOURCE FACE
**2026-09-23 · moment channel, continued from J01**
Files: `J02_moment_hierarchy.py` · `J02_moment_hierarchy.out` (exit 0, **15/15**) · `J02_results.json`

**Scope (kept):** same stationary Thomson-sphere model as J01 and the frozen
lane. A closed-form identity inside the model — not an observational JWST
confirmation, not a new law of nature; the significance is that the moment
hierarchy is now *proven exact at all orders* and the source-geometry limit of
the frozen Theorem 1 is now *exactly located*.

---

## THEOREM A — the even-moment hierarchy (new; any source)

J01's conditional-Gaussian lemma stated that V := v | trajectory is Gaussian
with variance exactly 2·ang. The moment structure of a Gaussian is closed:

> **E[D v^{2m}] = (2m−1)!!·2^m·E[D·ang^m]**   (m ≥ 1, every scattering order)

Verified on the independent solver (n = 10⁶, ±SE):

| source | m=1: E[Dv²] = 2·E[D·ang] | m=2: E[Dv⁴] = 12·E[D·ang²] | m=3: E[Dv⁶] = 120·E[D·ang³] |
|---|---|---|---|
| central | 3.7254 vs 3.7142 (0.30%) | 122.04 vs 121.57 (0.38%) | 8502 vs 8762 (3.1%) |
| **volume** | 2.2634 vs 2.2598 (0.16%) | 68.60 vs 68.24 (0.53%) | 4834 vs 4672 (3.5%) |

(ratios 1.003 / 1.004 / 0.970 and 1.002 / 1.005 / 1.035; the m=3 spread is the
MC tail of v⁶, within the pre-registered tolerance.) **The hierarchy survives
the source change exactly** — Gaussianity is a property of the kick chain, not
of the emission.

## THEOREM B — the volume-source face of Theorem 1 (new)

The frozen identity E[D] = ∫₀¹ rκ(r) dr holds for the **central** source (its
proof starts at x₀ = 0). For volume-uniform emission, the generator identity
Lf = 2c with f = F(r)+2x·u, F′(r) = 2rκ(r) gives, **exactly**:

> E[τ]_vol = ∫₀¹ rκ dr + R·E[μ_exit] − ½·E[F(r₀)],   r₀ ~ 3r² (volume-uniform)
> E[D]_vol = E[τ]_vol − E[Q],   Q := (x_τ−x₀)·u_τ = Σⱼ ℓⱼ(uⱼ·u_final)

Q is a new, retained path functional — the residence–direction coupling. For
κ = τ₀ uniform (R = c = 1): E[F(r₀)] = 3τ₀/5, so
**E[τ]_vol = τ₀/2 + E[μ_exit] − 3τ₀/10**.

Numbers (independent solver; E[μ_exit] measured by a dedicated escape-face
estimator, n = 1.5×10⁵):

| quantity | measured | exact/prediction |
|---|---|---|
| E[D]_central | 0.4989 | ½ ···· (B1, re-benchmark ✓) |
| E[D]_volume | **0.3376** | ≠ ½ (B2: the identity does **not** port; >8 SE) |
| E[τ]_volume | 0.93465 | Dynkin: ½ + 0.73527 − 0.3 = 0.93527 ✓ (B3) |
| E[Q] | 0.59715 | E[τ]_vol − E[D]_vol = 0.59706 ✓ (B4; bookkeeping exact to 7e-16) |

So the *reason* the frozen identity fails off-centre is now itemised: the
volume starting position injects ½E[F(r₀)] into the mean residence and the Q
coupling into the delay. **The mixed hierarchy (Theorem A) is untouched** — its
E[D·ang^m] simply uses these corrected means.

## Corollary — the closure fails at every order (the target's retained term)

The two-moment closure ratio, using only marginal moments:

> R_m = E[Dv^{2m}] / ((2m−1)!!·2^m·E[D]·E[ang^m])

is measured (central, uniform, n = 10⁶):

| m | R_m |
|---|---|
| 1 | 2.635 |
| 2 | 3.574 |
| 3 | 4.563 |

R_m ≠ 1 at every order and **grows with m**: no finite set of marginal moments
closes the mixed moments; the pathwise angular correlation Cov(D, ang^m) is
load-bearing at all orders. This is the quantitative form of the target's
"matched pair matches only two moments" warning, now extended to the full
hierarchy.

## Robustness and honest edges

- q-clouds κ = τ₀(1+qr²), q = 3, 10: hierarchy at m = 1, 2 **passes** (D-checks).
- Independent solver discipline as J01 (exact optical-depth bisection, own
  geometry arithmetic, no null-collision thinning); calibration vs the frozen
  `transport.py` held from J01 (≤0.8%).
- Not claimed: any observational content; the volume computation is a
  *model-internal* face of a standard transport statement (the generator
  identity is textbook; the exact compensation and the Q term are the lane's
  addition, and the closure growth R_1→R_2→R_3 is the lane's measurement).
- The m = 3 numbers carry MC tail risk; the identity is exact, the *evidence*
  is the m = 1, 2 concordance plus the closed Gaussian moment argument.