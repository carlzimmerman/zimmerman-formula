# Backfill spec — the contract every replacement idea must meet

Written 2026-08-17. Any idea that replaces one moved to `ALREADY_TRIED.md` must satisfy
**all** of this. So must any new idea added later.

## The seven elements

| | element |
|---|---|
| **N1** | `a0 = kappa c sqrt(G rho_Lambda) = c^2 sqrt(Lambda/32 pi)` = 9.3619e-11 canonical / 1.1279e-10 alt; `kappa = 1/2` FITTED, measured 0.529 ± 0.034 |
| **N2** | **The promotion**: `a0^2(Q) = kappa^2 G (-K(Q))` — the MOND scale *is* the dark sector's pressure, so **a0 is a field** |
| **N3** | **The β=1 DBI brane**: `K(Q) = -M^4 sqrt(1-(Q-Q_0)^2/Lambda_D^2)`, `M^4 = rho_Lambda c^2`. Has a **WALL** at `|Q-Q_0| = Lambda_D` where `-K -> 0`, hence `a0 -> 0` |
| **N4** | **The derived a0(z)**: `a0(nu)/a0(0) = [(1+nu_0^2)/(1+nu^2)]^(1/4)`, `nu = nu_0 rho/rho_0`. Locally makes a0 track charge density. `nu_0 <= 2.36e-6` |
| **N5** | **The a0-line**: `g_obs^2 = g_bar^2 + a0 g_bar`, `U = sqrt(y^2+y)-y`, saturating at 1/2 |
| **N6** | **Legality**: single-valued `F(Y,Q)` requires `U(y)` strictly increasing. Family `J_Y = v/(1-v/s)`, `U -> s`. **`s = 1/2` is NOT the a0-line** (U(2): 0.369 vs 0.449) |
| **N7** | `Q_0` pinned 0.0024–0.0146 Mpc⁻¹; `Lambda_D/Q_0` bounded by growth and the Ly-α forest |

## The six criteria

1. **C1 — ≥2 of N1–N7, three where the physics allows.** Mandatory `USES:` field naming them.
   The idea must *require* those elements: if it would still make sense for generic MOND,
   it fails.
2. **C2 — Unique.** No two ideas produce the same computation, across all 500.
3. **C3 — Dimensionally sound.** Every comparison between commensurable quantities; units
   stated where not obvious.
4. **C4 — Physically plausible.** May *test* whether the framework violates a law; may not
   *assume* a violation as its mechanism.
5. **C5 — High impact if true.** Mandatory `IMPACT:` field, ≤12 words, naming the roadblock
   it moves or the discriminator it produces.
6. **C6 — Not already tried.** No collision with `RETRACTIONS.md`, `STANDING.md`, the qwen
   ledger/harvest, or a committed script. If related prior work exists, cite it in `DO:` so
   the worker starts from it.

## Explicitness — the part that decides whether a 27B model succeeds

Every `DO:` must be executable **without judgement calls**. Concretely:

- Name the **file to read** and, where it matters, the function or table inside it.
- Give the **formula to evaluate**, not a description of it.
- Give the **numeric range to scan** (e.g. "s ∈ {0.02, 0.05, 0.1, 0.2, 0.5, 1, 2}"), not
  "a range of s".
- Give the **tolerance or threshold** that decides PASS, as a number.
- Say **which a0 footing** (both, unless stated).
- If a fit is needed, say **what is fitted and what is held fixed**.
- If the answer is likely partial, say `PARTIAL EXPECTED:` and name the sub-result that
  still counts as delivered.

A `DO:` that says "investigate whether X" is rejected. A `DO:` that says "evaluate
`U(y) = s sqrt(y)/(s+sqrt y)` at y = 6.3e7 for s in {…}, compare with 1.27e-5, report the
ratio" is accepted.

## The four seeded angles — expand these first

These are the combinations the corpus has **not** taken. Backfill should draw heavily on
them before inventing elsewhere.

### S1 — a0 as a dynamical field with its own equation of motion (N2+N3+N4)

The promotion makes a0 a field; the DBI gives it a ceiling; the derived law gives it a
source. The corpus has only ever treated a0 as *a number that happens to vary*. Nobody has
written its equation of motion. Ideas: derive `box a0` from the Q-equation; what are its
boundary conditions at a halo edge; does it have wave solutions and at what speed; is there
an a0-wave the CMB or a merger could excite; what sets its correlation length; does a0
lag the density it tracks, and by how much; what happens to a0 across a shock.

### S2 — dark energy is inhomogeneous in this theory (N1+N2)

`a0 = kappa c sqrt(G rho_Lambda)` holds *at the minimum*, but `P` is a field, so locally
`rho_Lambda -> P(x)/c^2`. **The same equation that ties a0 to dark energy says dark energy
is not homogeneous** — it is suppressed wherever the charge is dense. This is a direct
consequence of two committed lines and appears nowhere in the corpus. Ideas: compute the
fractional dark-energy deficit inside a cluster, a galaxy, the solar system; does it show
up in the ISW effect; in void expansion rates; in supernova distances through voids versus
walls; does it shift `w(z)` inferred from an inhomogeneous universe; is the Hubble tension
sensitive to it; what is the volume-averaged `<P>` versus the `rho_Lambda` that Planck
fits.

### S3 — the wall is a surface in spacetime (N3+N7)

`|Q-Q_0| = Lambda_D` is a locus, not an abstraction, and with `Q_0` pinned it has a
location. Ideas: where is the wall for the Sun, the Milky Way, a cluster, at both edges of
the pinned `Q_0` band; is any real object past it; what happens dynamically at the wall
(phase boundary, caustic, discontinuity in a0); is the wall crossed during collapse and
does that halt it; is there a shell where a0 = 0 inside a halo and would it be visible in
a rotation curve; does the wall have a surface tension or energy.

### S4 — legality re-derived with a0 as a field (N5+N6, and this one is load-bearing)

The monotonicity requirement — the origin of the 233× obstruction — was derived treating
a0 as a **constant**. If a0 is a field, `y = g_bar/a0(rho)` is not a fixed variable and
`U(y)` is not a fixed curve. **The central obstruction may have been derived under an
assumption the framework itself contradicts.** Ideas: redo the single-valuedness argument
with `a0 = a0(rho)`; is the correct condition monotonicity in `y` or in `g_bar`; does the
kinetic-matrix positivity condition change; is there a legal coupled system whose *apparent*
U is non-monotone; does the saturation theorem survive; and if it does not, what replaces
the 233× number.

**S4 is the highest-value item in this file.** If it holds, the framework's central
roadblock dissolves. If it fails, the roadblock is confirmed at a deeper level than before.
Either outcome is worth a paper.
