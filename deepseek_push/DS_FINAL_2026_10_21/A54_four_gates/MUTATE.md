# A54 — mutations

Seven dials. Each changes **one** structure of the action (a coefficient, a term, or a sign) and each breaks at
least one check and exits 1. Reproduce any of them with

```bash
python3 a54_checks.py --mutate <name>
```

`none` is the canonical run: 34/34 PASS, exit 0 (`a54.out`, `a54_results.json`).

| mutation | what it changes | checks broken | measured | why that is the right failure |
|---|---|---|---|---|
| `clock2` | clock coefficient `1 → 2` | **L5**, **G9** | `q_scale − 1 = 1.0`; `min dg/dg_N = −77.72` | the charge becomes `2D·P`, so `g_N = g − 2u` and `dg_N/dg = 1 − 2u'` goes **negative** for `u' > ½`: the response folds. This is A33 K5's "any ξ ≠ 1 deforms the law" in canonical form. |
| `drop_clock` | clock coefficient `1 → 0` | **L5** | `q_scale − 1 = −1.0` | no charge at all: `g_N = g`, no MOND, and the P sector decouples from the lapse. Note `G9` still passes — with `g_N = g`, `dg/dg_N = 1 ≥ 1` — which is correct: dropping the clock does not destabilise the response, it deletes it. |
| `wquad` | `W(u)` log `→ u²/2K` | **H1**, **H2**, **H3**, **H7** | `W(0.999) = 0.499` (no cap divergence); `W(g)` residual `g²(a₀²−(a₀+g)²)/(2K(a₀+g)²)`; `dg/du − K/(1−x)² = a₀²/(a₀−u)² − 1` | the quadratic potential is convex and bounded but gives the **wrong law**: the log form is what makes `g_N = g²/(g+a₀)` exact (A33 K3b). H1's coercivity fails too: no cap. |
| `eta_neg` | `η → −γ` | **H5**, **H6**, **G10** | `1/η = −4.35e−27`; `min ω_T² = −1.0e60`; `min Q₀ = −3.27e104`; `c_s² = −1` | a ghost in the P kinetic term and a gradient instability in the same stroke: `ω² < 0` for every `k`. |
| `gamma_neg` | `γ → −γ` | **H6**, **G10** | `c_s² = −1`, `min ω₀² = −1.0e60` | negative gradient energy: the front speed squared is negative, the mode is unstable at every wavelength. |
| `beta_neg` | `β → −0.25` | **H6** | `min Q₀ = −5.96e9` | **the sharpest one**: `Q₀ = (2+3β)/(Kβ) + ηk²/K²` changes sign with `β`, so the fifth mode (the mixed conformal/`P`-longitudinal scalar) becomes a ghost. This is why `β > 0` is load-bearing and not decorative (§2.3). |
| `ricciP` | adds `ξR_ijP^iP^j`, `ξ = 10¹⁸` | **G1b** | `Δc_T² = 2ξ(L_*a₀/c²)² = 1.19` | a P–curvature coupling puts two derivatives of `h` into the TT action. `ξ = 10¹⁸` is dialled for visibility; at `ξ = 1` the shift is `1.19×10⁻¹⁸`, i.e. the absence of this operator is what makes `c_T² = 1` **exact** rather than approximate. |

## What each mutation establishes

* `clock2` / `drop_clock`: **(S2)** — the unit coefficient of the clock is not a convention. It fixes the charge
  `D·P`, hence the first integral `g_N = g − u`, hence `dg/dg_N = 1/(1−u')`. Any other coefficient either folds
  the response (`ξ = 2`) or deletes it (`ξ = 0`).
* `wquad`: **(S1)+(S2)** are not enough for gate (iv); the *shape* of `W` matters. Convexity alone
  (`W'' > 0`) gives `dg/dg_N > 1`, but only the log form gives `g_N = g²/(g+a₀)` and the exact coefficient
  `1 + a₀²/(g²+2a₀g)`.
* `eta_neg` / `gamma_neg` / `beta_neg`: the three positivity conditions `η > 0`, `γ > 0`, `β > 0` are exactly
  the three kinetic coefficients `η/2`, `γ/2`, `Q₀`. There is no ghost-free window with any of them negative.
* `ricciP`: **(S3)** — no P–curvature coupling — is the *only* premise gate (ii) needs; `β` does not enter it.

## Not mutated (and why)

* `β = 0`: not a small perturbation but a **rank-degenerate point** (`Q₀` diverges, the shift equation becomes a
  constraint — round-2's "the `β = 0` branch must be treated separately"). A mutation to `β = 0` would crash the
  `Q₀` arithmetic rather than fail a check honestly, so it is excluded from the dial set and discussed in
  §2.3 instead.
* `β = −2/3`: the Legendre map degenerates (`2+3β = 0`, L8). Same reason: it is a different theory, not a
  perturbation of this one.
* `η = 0`: `π_P = 0` becomes primary and the DOF count changes. L4/L7 catch it structurally; the dial would
  produce a division by zero in H5.
