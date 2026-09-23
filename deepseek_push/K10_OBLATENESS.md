# K10 — THE OBLATENESS DOOR: windows under a flattened (oblate-spheroid) BLR

**2026-09-23 · moment channel · oblate spheroid · final verdict (all 23 checks pass)**

## The question

J09/J11 derived the emitter windows on the **unit sphere**: central −lnA/E[D] =
(1+q/3)/(1/2+q/4) ∈ **[4/3, 2]** (τ₀-free), volume τ₀-dependent (1.897 at q=0,
τ₀=1, crossing below 4/3 at depth). Real BLRs are flattened. **Does the window
structure survive oblateness?** Transport on the spheroid x²+y²+z²/ε² = 1
(semi-minor axis ε ∈ {1.0, 0.7, 0.5, 0.3}, z flattened), κ = τ₀(1+qr²) with r
the **Euclidean** radius, central + volume-uniform sources, exact quadratic
surface intersection (A-coefficient ux²+uy²+uz²/ε² > 0). Independent
re-implementation of the J02 engine; ε=1.0 is the kill gate.

## Verdict: the window structure is **NOT geometry-stable — it is eps-dependent and inflates**

**Central window (q=0, τ₀=1):**

| ε | A (atom) | E[D] | **W_c = −lnA/E[D]** | vs 2.0 |
|---|---|---|---|---|
| 1.0 | 0.3666 | 0.5016 | **2.0006 ± 0.0061** (sphere: exactly 2) | 0 SE |
| 0.7 | 0.4171 | 0.3877 | **2.2549 ± 0.0073** | **+35 SE above 2** |
| 0.5 | 0.4730 | 0.2944 | **2.5426 ± 0.0087** | **+62 SE above 2** |
| 0.3 | 0.5677 | 0.1859 | **3.0454 ± 0.0119** | **+88 SE above 2** |

The central window leaves [4/3, 2] as soon as ε ≤ 0.7 — **upward**, not down;
E[D] collapses with flattening (0.50 → 0.19) faster than the atom grows.
**A measured ratio > 2 no longer kills central Thomson emission — it reads
oblateness.** J09's "geometry-free law" is sphere-specific.

**Volume window (q=0, τ₀=1):** inflates identically: 1.896 ± 0.007 (ε=1) →
2.156 (0.7) → 2.454 (0.5) → 2.991 ± 0.015 (0.3) — always ABOVE the central
window's sphere value, closing the central-vs-volume discrimination at depth:
at ε=0.3 volume (2.99) sits *above* central-sphere (2.00).

**Volume τ₀-dependence: survives moderate flattening, suppressed at strong:**

| τ₀ | W_v(ε=1.0) | W_v(ε=0.5) | W_v(ε=0.3) |
|---|---|---|---|
| 0.5 | 1.9047 ± 0.0094 | 2.4358 ± 0.0138 | 2.9258 |
| 2.0 | 1.8064 ± 0.0057 | 2.4223 ± 0.0082 | — |
| 3.0 | 1.6865 ± 0.0050 | 2.3542 ± 0.0073 | 3.1462 |
| 5.0 | 1.4649 ± 0.0042 | 2.1710 ± 0.0064 | — |
| 8.0 | **1.2264 ± 0.0036** | 1.9080 ± 0.0055 | 2.9438 |

- ε=1.0: monotone decline **crosses below 4/3 by τ₀=8** (1.226) — J11 confirmed.
- ε=0.5: dependence survives (2.44 → 1.91), but the 4/3-crossing is pushed
  beyond τ₀=8 — **the crossing location is itself eps-dependent**.
- ε=0.3: the decline is killed — window sits in [2.93, 3.15] (hump at τ₀=3;
  atom verified against exact 4-D quadrature at all three points, ≤ 0.5 SE);
  τ₀-amplitude 0.22 vs 0.68 at ε=1.0.

**Central τ₀-freeness also breaks:** at ε=0.3, W_c(τ₀=0.5)=2.9997 vs
W_c(τ₀=3)=3.1590 (8 SE) — the sphere's τ₀-free central law gains τ₀-dependence
under oblateness (weak: ~5% over half a decade).

## The projection-correction table (observer un-flattening)

W_sphere = W_measured / corr(ε), measured at (q=0, τ₀=1), n=4×10⁵:

| ε | corr_c = W_c(ε)/W_c(1) | corr_v = W_v(ε)/W_v(1) |
|---|---|---|
| 1.0 | 1.0000 | 1.0000 |
| 0.7 | 1.1271 ± 0.0050 | 1.1373 ± 0.0063 |
| 0.5 | 1.2709 ± 0.0059 | 1.2940 ± 0.0074 |
| 0.3 | 1.5222 ± 0.0076 | 1.5774 ± 0.0097 |

**Fits:** corr_c(ε) = ε^(−0.347 ± 0.002), corr_v(ε) = ε^(−0.376 ± 0.003)
(least-squares on log-log through the anchor; residual slope scatter 0.002–0.003).
A flattened-ε cloud's measured window must be divided by ~1.27 (ε=0.5) or
~1.52 (ε=0.3) before comparing against the sphere window [4/3, 2].

Thin-limit anchors (exact quadrature): E[chord]_c = 1.000, 0.878, 0.760, 0.589;
E[chord]_v = 0.750, 0.658, 0.570, 0.442 at ε = 1.0, 0.7, 0.5, 0.3. The inflation
is numerator-driven in the thin regime but E[D]/τ₀ also shrinks (0.50 → 0.19
central; 0.34 → 0.13 volume at τ₀=1) — a projection effect on the *residence*
channel, exactly what an observer must un-project.

## Kill conditions (pre-registered) and engine validation

1. **Transport kill:** ε=1.0 must reproduce the sphere exactly — central
   A=e⁻¹ (MC 0.3677, 0.2 SE), E[D]=1/2 (0.5010, 1 SE), W=2.0 (1.997, 0.5 SE);
   volume A vs exact 4-D Gauss–Legendre quadrature (0.5282 vs 0.52725, 1.2 SE)
   and W vs J11 (1.8959 vs 1.8970, 0.2 CE). **PASS — no transport bug.**
2. **Spheroid-transport kill:** atom vs exact quadrature at EVERY ε, both
   sources (QC/QV, 8 checks) — all |MC−quad| ≤ 1.2 SE. **PASS.**
3. **Window claims:** central inflation (3 checks, +35/62/88 SE), volume
   inflation (3 checks, +23/44/68 CE), τ₀-dependence survival (ε=1.0, 0.5),
   eps-dependent crossing location, deep-crossing kill at ε=0.3, central
   τ₀-freeness break — **23/23 PASS.**
4. Nothing killed: the K10 finding is that the *window* is projection-
   sensitive (correctable via the table), not that the engine is wrong.

## Files

`K10_oblate.py` (engine + exact quadratures + checks), `K10_oblate.out`,
`K10_results.json` (full measurements, SEs, fits). No git commit.

## Notes / honesty

- All SEs are MC standard errors (atom binomial, E[D] sample, window by
  first-order propagation); grid values at n=4×10⁵ per (ε, source, τ₀).
- The τ₀=3 hump at ε=0.3 (volume) is machine-verified against the exact
  quadrature atom (0.1 SE) — it is real, not noise.
- The correction table is measured at τ₀=1, q=0; since the central window
  gains (weak) τ₀-dependence at strong flattening, applying the table at very
  different τ₀ carries the quoted ±0.5%–1% plus ~2% τ₀-slope uncertainty at
  ε=0.3 (worst case).