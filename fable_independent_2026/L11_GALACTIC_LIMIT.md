# L11 — does the IC-series have a MOND limit?

2026-09-08. Script `L11_galactic_limit.py`, output `L11_galactic_limit.out`. 18 PASS, 3 FAIL.
Nothing under `integrable_clock_construction_2026/` was edited, imported or rerun; the lead's
files were read, and every equation below was re-derived here with sympy.

## Answer

**Yes.** The static weak-field limit of the IC-series is a genuine AQUAL-type MOND theory:

    div[ mu(|grad Phi|/a0) grad Phi ] = 4 pi G_N rho_b,    mu(y) = 1 - e^(-y),    y = |grad Phi|/a0,
    G_N = 1/(8 pi m),    Phi = Psi (no slip),    deep-MOND  g = sqrt(g_N a0)  with coefficient exactly 1.

- **Acceleration scale.** Exactly the `a0` in the action's `a0^2 U(u^2)` term — the numerical coefficient
  the theory attaches to it is `1.000000`, not 2, 1/2 or 2π. Setting that constant to 9.3619e-11
  (canonical) or 1.1279e-10 m/s² (alt) reproduces the programme's scale exactly. `a0` is an **input**,
  which the rules permit; the content of the check is the coefficient, and it is right.
- **Interpolation function.** `mu(y) = 1 - e^(-y)` — the lead's own PATH_FORWARD target, and the
  framework's **exponential carrier**: the kernel the programme carried until 2026-09-06 and then
  swapped for ν_RAR. It is **not** ν_RAR.
- **Newtonian limit.** `mu -> 1` at high acceleration, with `G_N = 1/(8 pi m)` — the same `m` that
  normalises `R4` and the tensor sector, so `G_dyn = G_lens = G_tensor` on the static plateau.

## How it comes out

`U(c) = (1-c)[ln²(1-c) - 2ln(1-c) + 2] - 2` has `U'(c) = -ln²(1-c)` exactly. That one identity is the
whole mechanism: varying `u` in `(m/2)[2(1-u²)a·a - 2a0²U(u²)]` gives `|a|² = a0² ln²(1-u²)`, i.e.
`u² = 1 - exp(-|a|/a0)` — **exact** on the static branch, with the covariant leaf norm, no weak-field
step. In static GR the lapse-gradient square *cancels* (verified: `sqrt(-g)R4 = 2A_s(|∇Ψ|² - 2∇Φ·∇Ψ)`
up to a total derivative), so the entire `|∇Φ|²` coefficient is `-u²`, and `mu = u²`. `U` was designed
to be this primitive, so the kernel is built in, not predicted.

## The transfer chain, checked rather than quoted (A6)

The reduction above is IC1's static sector. That it is also **IC10's** was verified here:
- IC10's added block is entirely `∝ eta`, and `eta ≡ 0` with all derivatives for `r ≤ 0.707`, while a
  static configuration has `p = 0`, i.e. `r = 0` — so the block is absent on a *neighbourhood*.
- IC5's static Hamiltonian (barred curvature `-(m/2)Ve^{uξ}R̄` plus its `G` term at `eta = 0`) is
  **exactly** IC1's `(m/2)[R³ + 2(1-u²)a·a]`: the difference is a null Lagrangian in all three fields
  (a pure spatial divergence — the one the lead declares).
- IC4's extra term is quadratic in `Q = K - 3W`, which vanishes identically in time on a static
  configuration, so it contributes nothing to any first variation.

## What the limit drops, and by how much (B4)

At the construction's own `kappa/m = 1.0127 a0²` (the IC1/IC4 witness relation), the dropped
clock/vacuum sources total `0.483 a0²`. Out to 1 Mpc: dropped/retained `≤ 1.9e-5`, spurious
acceleration `≤ 2.5e-3 a0`, slip `|Φ-Ψ|/|Φ| ≤ 6.5e-6`. The ordering the lead assumes is therefore
satisfied by seven orders of magnitude on galaxy scales — it is not smuggled in. It breaks only at
`L ~ c²/a0`.

## The two things that FAIL

**B2b — the kernel is not the carried one.** `mu = 1 - e^(-y)` versus ν_RAR differ by up to **0.073 dex**
in the transition (at `s = g_N/a0 ≈ 1.7`); they agree in both asymptotic limits. On the bounded-boost
ceiling — the one parameter-free discriminator — the IC-series' ceiling is `a0/e = 0.368 a0` against
ν_RAR's `0.648 a0`. On the bulgeless SPARC control (143 galaxies, 1475 points beyond 2 kpc, fixed
Υ_d = 0.5): **16.3% / 10.5%** of points exceed the IC ceiling at >3σ (canonical/alt) against
**3.1% / 1.8%** for ν_RAR — a factor 5.2, the same ordering the programme's own controlled test g03w
finds (7.3%/3.5% vs 1.2%/0.6%; my counts run ~2.5× higher for *both* kernels, so the cut/Υ difference
is common-mode). The IC kernel would need `a0` 2.4–2.9× larger to bring its violations to 1%; ν_RAR
needs 1.4–1.7×. *Direction stated:* this test is one-sided and Υ-sensitive, and the programme's own
global comparison with `a0` and Υ profiled (f25/g03l) finds exponential-vs-RAR **undecided**. So this
disfavours the kernel the IC-series produces; it does not exclude it.

**B5 — the far-field boundary condition on `u` is not determined by the published files.**
This is the precise missing input. The static (`eta = 0`) branch fixes `u` pointwise from the local
field, so `u -> 0` as `|a| -> 0` — the isolated-MOND boundary condition the deep-MOND asymptotics above
assume. The expanding (`eta = 1`) plateau fixes `u` from `P_w = 0` instead: IC10's own solution has
`u = 0.492, 0.537, 0.570` and the IC4/IC5 witness `u = 2/3`. A galaxy sits in `eta = 0`, the cosmology
in `eta = 1`, and the transition between them is exactly IC10's own "What remains" item 1 — not varied.
**The stakes are quantified:** if `u` must approach its cosmological value at large `r`, the static law
reads that as a universal external field `g_ext = 0.28–0.59 a0`, and 27% (canonical) / 38% (alt) of the
bulgeless SPARC points beyond 2 kpc sit below even the smallest of those. That is the acceleration
range where flat rotation curves live. Nothing in the published files fixes this either way — the
missing piece is the varied `eta`-transition together with the galactic/cosmological matching of `u`.

## Two flagged diagnostics (informational, not scored)

1. **`a0` vs the expansion rate on the one exhibited branch.** With IC10's own `m = h0 = 1, kappa = 6`,
   the witness relation gives `a0 = 2.434 h0` while IC10's solution has `H_phys = 0.72–0.81 h0`, so
   `a0/(cH) = 3.0–3.4` against the observed `0.143` (canonical) / `0.172` (alt) — **19–22× off**.
   `Lambda` and `kappa` are free off that branch, so this is a property of the exhibited solution, not
   a theorem; the lead already labels it "not a viable cosmology".
2. **`G_cos` vs `G_local`.** The Planck mass is `m` at `eta = 0` and `m* = m e^(-1/6)` on IC10's
   `eta = 1` plateau — a ratio `e^(1/6) = 1.181`. Whether that is a real 18% shift (BBN allows ~10–20%)
   depends on the conformal factor `e^(2w)` matter carries and on the transition; it cannot be settled
   from the published files.

## Verdict

The IC-series, as published, **is** a candidate host for this framework's galaxy phenomenology: its
static weak-field limit is MOND, at the action's own `a0` with coefficient 1, with one potential
(so lensing and dynamics agree) and the measured `G`, and the terms the limit drops are negligible by
seven orders of magnitude on galactic scales. Two named liabilities stand and are scored separately,
not hidden inside that verdict: the kernel it produces is the framework's *superseded* exponential
carrier, and the boundary condition that decides whether an isolated galaxy actually reaches the
deep-MOND regime is not determined by anything published.
