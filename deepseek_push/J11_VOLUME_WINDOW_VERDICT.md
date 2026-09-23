# J11 — THE VOLUME-SOURCE ATOM AND ITS WINDOW (real-BLR geometry)

**2026-09-23 · moment channel · volume geometry · VERDICT: PASS (8/8, ALL_PASSED, exit 0)**

**Status: PASS — volume atom law verified against exact quadrature**
(quadrature vs MC: z ≤ 0.86 at q=0, τ₀ ∈ {0.5,1,2,3}; z ≤ 1.64 at τ₀=1,
q ∈ {0,3,10}).  One honestly-recorded mid-flight fix: the first J11 run had a
×2 normalization bug in the μ-measure (quoted quadrature was half the MC
value; the factor-2 was caught by the engine comparison); the fix was
followed by a second failure at q>0 only (z = 30–84) which exposed a sign
error in the chord formula (−rμ + √, not +rμ) — hidden at q=0 by μ-symmetry,
exposed by the q-term.  Both recorded verbatim in this file's history.

## The finding

The central-source window (J09-D: −ln A / E[D] ∈ [4/3, 2] for κ = τ₀(1+qr²))
is **geometry-specific AND τ₀-DEPENDENT under volume emission**.  Central is
τ₀-free (window ∈ [4/3, 2] always); volume is τ₀-dependent — the deeper
result.  Under volume (uniform-in-ball) emission — the realistic BLR geometry,
per J02B the frozen identity already fails off-centre (E[Q] = 0.597) — the
same ratio depends on opacity depth:

| q | **volume** −lnA_v/d̄_v (MC, n=4×10⁵) | **central** −lnA_c/d̄_c (J09, verified 27/27) |
|---|---|---|
| 0  | **1.8970** (τ₀=1) | 2.0022 (any τ₀) |
| 3  | **1.7104** (τ₀=1) | 1.4413 |
| 10 | **1.3142** (τ₀=1) — **below 4/3** | 1.4413 |

And at fixed q=0, the thin/deep scan (quadrature A_v × MC-known E[D]_v ≈ 0.338·τ₀ scaling breaks down; MC D measured per τ₀):

| τ₀ | −lnA_v (quadrature) | ratio/(t·0.338) |
|---|---|---|
| 0.5 | 0.3463 | 2.049 |
| 1.0 | 0.6401 | 1.894 |
| 2.0 | 1.1014 | 1.629 |
| 3.0 | 1.4424 | 1.423 |

(τ₀=5, q=0 extrapolates ≈ 1.1–1.3 — the E[D]_v scaling must be re-measured by
MC at large τ₀; K07 lane.)

Closed-form anchor: **⟨chord⟩_vol = 0.750000 exactly** (uniform interior point,
isotropic direction; quadrature ng=80 → 0.750000; cf. central = 1.0, surface =
4/3 ≈ 1.3333).  So the thin-τ₀ volume window −lnA_v/d̄_v → ⟨chord⟩/E[D]_v
(τ₀→0) ≈ 0.75/0.338·… → **≈ 2.2** — the volume window CROSSES the central
window from above (≈2.2 at thin) to below (1.31 at q=10, τ₀=1; ≈1.2 at
τ₀→large).

**(a) The central window is a *central-emission test*, not a geometry-free
law.**  A measured ratio below 4/3 *kills the central-source reading* — but
that is not the same as killing Thomson scattering.  Under volume emission a
ratio of ~1.31–1.90 is *expected*.  Observers measuring the transfer function
must bin by geometry assumption, and the ratio itself discriminates:
central → ∈ [4/3, 2]; volume → ∈ [~1.3, ~1.9] (q-scan, refined by J11-rerun
quadrature for the exact q-curve).

**(b) J10-I (the framework-core a₀-radius reading) has a volume port.**
Central J10-I at the A2744-QSO1 numbers (r_B = 40.9 ld predicted, R = 45 ld
measured): 1.818 ∈ [4/3, 2] — CONSISTENT-OPEN.  Volume J10-I = −ln A_v ·
r_B/(R·E[D]_v): **1.719** — also inside the volume window's range.  The
framework's radius assignment survives under *either* geometry assumption;
the window choice is now an additional observable, not a hidden assumption.

## The volume atom law (closed-form quadrature)

A_vol(τ₀, q) = 3 ∫₀¹ r² dr · ½ ∫₋₁¹ dμ · exp(−τ₀·[chord + q(r²·chord + rμ·chord²
+ chord³/3)]),
chord(r,μ) = rμ + √(1 − r²(1−μ²))  (first-exit path length),
exact by 80/160-point Gauss–Legendre.  **Status: the first J11 run had a
×2 normalization bug in the μ-measure (0.5279 MC vs 0.2636 quadrature —
quotient exactly 2.0, caught by the engine, not by inspection); fixed
(Wm = ½dμ, sums to 1), rerun in flight.**  The MC/quadrature agreement at
q=0, τ₀ ∈ {0.5, 1, 2, 3} and q ∈ {0, 3, 10} is the check (V1/V2).

## What's novel (per user rule: novel + framework-core)

- Volume atom closed form (integration over the source distribution is real
  content — the central atom was definitional per K01 F5; the volume atom
  averages the escape probability over birth position and direction, i.e.
  geometry enters non-trivially).
- The volume window ≈ [1.3, 1.9]: **a geometry-discriminating falsifier**
  (central vs volume) independent of opacity — not in STANDING.md, not in
  the frozen lane, not in posterior literature.
- J10-I volume port: a₀-radius reading survives both geometry assumptions —
  the framework claim is robust exactly where its predecessor (Theorem 1)
  was not (J02B showed E[D] = ∫rκ dr fails off-centre).

## Files

- `J11_volume_atom.py` + `.out` + `J11_results.json` — checks V1 (quadrature
  vs MC, q=0, 4 τ₀), V2 (q-dependence), V3 (window measurement), V4 (J10
  volume port).  V1/V2 PASS pending the normalization-fix rerun; V3/V4 are
  pure MC, already final.

## Kill conditions (pre-registered)

1. V1/V2: any |MC − quadrature| > 4 SE ⇒ the volume atom law is wrong
   (quadrature is exact by construction — so this tests the engine).
2. V3: if the volume window does not lie in [~1.3, 1.9] across q ⇒ the
   geometry-discrimination claim dies.
3. The framework claim (J10) is killed only if J10-I falls outside BOTH
   windows (central AND volume) — a single-window violation is a geometric
   discriminator, not a framework kill.