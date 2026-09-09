# L65 — the wake/memory architecture: a causal kernel DOES have a variational origin, and it is the bookkeeping for a hidden sector

2026-09-09. Lane L65 of [CHARTER.md](CHARTER.md), answering **door 6** of
`qwen_claude_field_theory/closure_2026/TEN_OPEN_DOORS_2026-09-09.md`.
Script: [L65_memory_kernel.py](L65_memory_kernel.py) → [L65_memory_kernel.out](L65_memory_kernel.out).
**37 checks, 28 PASS / 9 FAIL — every FAIL is a marked `[GATE]`, i.e. a requirement the architecture does
not meet. 0 non-gate failures: all controls and all structural checks pass.**

Method: nothing under `closure_2026/`, nothing of the lead's, and nothing of L39's script was imported,
executed or copied. All curvature is computed from the metric in sympy inside this file; all numerics are
built here. Eleven controls guard the lane, including three that reproduce L39's central results
independently and three that reproduce published Dirac counts.

---

## The verdict, first

> **A variational principle that produces a genuinely causal kernel EXISTS.** It is the doubled-field
> (in-in / Schwinger–Keldysh, or classically Galley) construction, and it meets the lead's stated pass
> condition — the causal kernel comes **out** of the variation, it is not prescribed afterwards. That is a
> real advance on L39, which reported only that the single-field variation symmetrises.
>
> **But the memory is bookkeeping, not a fundamental structure.** A bath is constructed here whose
> retarded propagator *is* the kernel; the retarded prescription is then a **choice of state** for that
> bath. The trichotomy is exhaustive: a memory kernel is local, or the retarded propagator of a healthy
> hidden sector, or of ghosts. There is no fourth option.
>
> **And it does not escape the lensing lock.** A memory kernel is a function of `□`, so it sits in the
> frame-free one-parameter transverse family; that family is identified here with the linearised Einstein
> tensor of a *pure conformal perturbation*, and a conformal factor cannot bend light.
>
> **Outcome (b) of the lane's three: a variational causal formulation exists, at the price of hidden
> dynamical states** — an oscillator continuum per space point for a branch-cut kernel, a ghost for a
> rational one.

L39's finding is **not weakened**. The retarded reading really does give `N_grav = 2`, and the localised
counting rule really is unreliable (`C4b`, reproduced exactly). What L65 adds is that the 2 is the count of
the *effective* description, that the causal variational principle exists but is the doubling whose second
field is the very `±½` pair L31 flagged, and that the architecture is caught by the lock it was hoped to
evade.

---

## 1. Controls — L39's three results, reproduced independently

| control | L39 | L65, computed here | result |
|---|---|---|---|
| **C1** Dirac count, ADM general relativity | 2 | `(12 − 2·4)/2 = 2` | ✔ |
| **C2** GR + one minimally coupled scalar | 3 | `(14 − 8)/2 = 3` | ✔ |
| **C3** Einstein-aether | 5 | `(18 − 8)/2 = 5` | ✔ |
| **C4** GR's conformal mode vs its graviton | `+½` / `−6` | `+1/2` (TT) / `−6` (conformal) | **exact match** |
| **C5** retarded restriction preserved by the dynamics | `0.000e+00` | `0.000e+00` | **exact match** |
| **C6** does variation give the causal kernel? | `0.50` from `G_ret`, `0.00` from the average | `0.5000` / `0.0000` | **exact match** |

**C4** is L39's decisive control and it is reproduced from the metric, with the integration by parts done
by period-averaging a plane wave rather than by hand:

    L^(2) unreduced, TT h_11 = -h_22 = chi(t,z)   : -2 chi chi_tt + 2 chi chi_zz - (3/2) chi_t^2 + (3/2) chi_z^2
    L^(2) unreduced, conformal g = (1+2 phi(t)) eta : -6 phi_t^2
    reduced: TT coefficient of (d_t chi)^2 = +1/2 ;  conformal coefficient of (d_t phi)^2 = -6

So "a negative kinetic eigenvalue means a propagating ghost" would give **general relativity** a ghost. It
is a false inference, exactly as L39 said.

**C5 gains a control L39 did not print, and it matters.** The retarded solution restarted from its own
slice data reproduces itself to `0.000e+00` — but so does a solution *with* a homogeneous piece (also
`0.000e+00`), while the two differ from each other by `0.48`. **Restart-invariance is therefore not what
singles retardation out.** What C5 establishes is *where* the condition is imposed — once, at the initial
surface — not that the dynamics prefer it. The real content is `C5c`: two source histories identical for
`t ≥ 8` give `|j_A − j_B| = 2.9e-63` on the slice at `t = 16` but `|ξ_A − ξ_B| = 2.96`. The retarded
condition is not a function on the instantaneous slice, so Dirac's algorithm is structurally blind to it.

**C6 is reproduced in L39's own normalisation.** The varied kernel sits at exactly `0.5000` of the way
along the segment `G_ret → G_adv` and `0.0000` from their average. (In the `‖G_ret‖` normalisation the same
fact reads `0.70`; that number is discretisation-dependent and the segment position is not.)

### C6c — the obstruction, sharpened past L39, and this is what actually closes route 1

L39's A4 argument is about kernels of **quadratic** nonlocal actions. MOND needs a **nonlinear** kernel
(see §3, M1), which that argument does not reach. The general statement is the Helmholtz/Poincaré
condition: *a field equation arises from some action if and only if its linearisation is symmetric*. The
obstruction is then measurable directly, with no action to guess:

| equation | `‖J − Jᵀ‖ / ‖J‖` |
|---|---|
| intended **linear** causal equation `D f + G_ret f` | **0.703** |
| intended **nonlinear** causal equation `D f + G_ret f³` | **0.873** |
| CONTROL, time-symmetrised `D f + ½(G_ret + G_adv) f` | `0.0e+00` |
| CONTROL, an operator that really is `δS/δf` (numerical Hessian of a quartic *nonlocal* functional built on the **same** causal kernel) | `0.0e+00` |

Both controls sit at zero, so the estimator can tell the two cases apart. **No single-field action —
local or nonlocal, linear or nonlinear — yields a causal kernel.**

---

## 2. The routes to a causal kernel from a variational principle, enumerated

| route | causal from variation? | memory fundamental or bookkeeping? |
|---|---|---|
| **1** single-field action, local or nonlocal, any order | **NO** — C6c, an obstruction of 0.70–0.87 | — |
| **2** doubled fields: in-in / Schwinger–Keldysh, Galley's classical version | **YES** — V1, distance `0.0000` from `G_ret` | bookkeeping (V2 + PART B) |
| **3** integrating out a genuine dynamical sector | **YES**, trivially | **fundamentally bookkeeping** — the kernel *is* the sector's retarded propagator |
| **4** open-system / dissipative (Rayleigh function, GKSL) | not an action for the system alone | route 3 with the environment already traced out; adds no new possibility |

**V1, the constructive result.** Vary `S[a,b] = aᵀ G_ret b`:

    delta S / delta a  ->  kernel at distance 0.0000 from G_ret   (EXACTLY retarded)
    delta S / delta b  ->  kernel at distance 0.0000 from G_adv   (EXACTLY advanced)

Causality is not *created* by the doubling; it is **distributed** — one causal equation and one anti-causal
one — and the physical limit then keeps the causal half.

**V2, the identification that ties the lane together.** Compute the kinetic matrix of `S[q₊] − S[q₋]` in
the Keldysh basis `q± = q_cl ± q_q/2`:

    L_kin = q_cl_dot * q_q_dot     =>     K = [[0, 1/2], [1/2, 0]] ,  eigenvalues ∓1/2 ,  det K = -1/4

This is **identically** the off-diagonal pair L31 flagged as a ghost and L39 defused. It cuts both ways.
It *exonerates* the `±½` — a field/response-field pair always has an off-diagonal kinetic form, which is
precisely why C4b's false inference matters. But it also means **the causal variational principle and the
localised nonlocal action are the same object in two notations**, so whatever the localised reading counts,
the causal variational principle also has.

**V3.** The physical limit `a = 0` (`q₁ = q₂`) has exactly the structure of C5/C5c: an invariant
submanifold, imposed once on the initial surface, invisible to Dirac's algorithm. Route 2 therefore
*relocates* L39's cost — from "not variational" to "variational, with a second field and a prescription" —
it does not remove it.

---

## 3. Memory ⟺ hidden states. The whole question, and it is decided

**H1 — an explicit bath whose retarded propagator IS the kernel.** Caldeira–Leggett with a counterterm,
`N = 600` oscillators, Ohmic `J(ω) = η ω e^{−ω/ω_c}`. Integrating out oscillators started at rest gives
*exactly* `q̈ + ω₀²q + ∫₀^t γ(t−s) q̇(s) ds = 0` with `γ(τ) = Σ (c_n²/ω_n²) cos(ω_n τ)`. Integrated
independently against the memory equation:

| `dt` | max relative difference (full bath vs memory equation) |
|---|---|
| 0.004 | 2.9e-03 |
| 0.002 | 1.5e-03 |
| 0.001 | 7.3e-04 |
| 0.0005 | 3.7e-04 |

First-order convergence of the convolution quadrature: the residual is discretisation, not physics.

**H2 — and therefore the retarded prescription is a choice of STATE.** Give the same bath nonzero initial
data and the observable trajectory changes by up to **118%**. "No homogeneous piece" is a statement about
what state the hidden sector is in, not about whether it exists.

**H3–H5 — the trichotomy, and it is exhaustive.**
- Causality is a *spectral* statement: the causal kernel `e^{−s/τ}/τ` satisfies Kramers–Kronig to
  `6.1e-04` relative error, while the time-symmetric kernel `e^{−|s|/τ}/(2τ)` **fails it outright**
  (predicted `Re = 0`, true `Re = 0.67`). So a causal kernel *has* a spectral density.
- If that density vanishes, the sine transform of `K` vanishes; the sine transform is injective (discrete
  rank 400 of 400, condition number 1.0000), so `K(s) = 0` for `s > 0` and `K` is a contact term — a
  **local** operator, with a local theory's mode count and Ostrogradsky problem.
- If it is non-negative, the kernel is the retarded propagator of a positive-norm sector: H1 builds it.
- If it takes either sign, some of those oscillators carry negative norm.

**H6 — the finite case is a ghost.** `D(s) = −s + k² + g²M²/(M² − s)`, `s = ω²`, has poles at
`s = 0.4189` and `0.9312` with residues of `1/D` equal to `−1.13434` and `+0.13434` — **opposite signs**.
A rational (finite-state) memory kernel is the Pais–Uhlenbeck/Lee–Wick situation and is not ghost-free.

**`[GATE] H7` — FAIL. The memory is bookkeeping for hidden degrees of freedom.** Every branch of the
trichotomy either has states or is local. There is no exception.

---

## 4. The physics test: can a memory kernel produce a *static* MOND modification at all?

Rotation curves and the solar system are **both static**, so the memory integral has run to its asymptote
and the response is the kernel's zero-frequency limit. This is the sharpest internal check available and
it comes before any phenomenology. Four requirements fall out, and three of them fail on data.

**`[GATE] M1` — FAIL. A linear memory kernel is excluded by the data.** A linear response
`Φ = ∫K ρ` obeys superposition, so `g_obs ∝ g_bar` with slope 1. SPARC, deep regime:

| footing | points (`g_bar < a₀/10`) | `d log g_obs / d log g_bar` |
|---|---|---|
| canonical (9.3619e-11) | 846 | **0.504 ± 0.027** |
| alt (1.1279e-10) | 977 | **0.528 ± 0.023** |

20σ from the linear-response value. **The memory kernel must be nonlinear in the field**, which is why
C6c's extension past the bilinear argument was necessary.

**`[GATE] M2` — FAIL. A purely temporal kernel cannot separate two static systems.** `K(t − t')` at
`ω = 0` applies one number `K̃(0) = ∫₀^∞ K(s) ds` to *every* static configuration. The data demand
`g_obs/g_bar = 3.48` (canonical) / `3.39` (alt) in galaxy outskirts and `1 + 10⁻⁵` at Saturn's orbit
(`g = 6.5e-05 m s⁻²`; the bound used is deliberately loose — ephemerides do far better). Separation of
2e+05 in units of that loose bound. **The kernel must be a function of the full `□`, not of time alone.**

**`[GATE] M3` — FAIL. Then the transition is a LENGTH, and it is not the MOND length.** In the static
limit `□ → −∇²`, so `F(□) → F(k²)` and the on/off transition is at a wavelength.

| footing | `c²/a₀` | ÷ galactic radius (median 9.0 kpc) | ÷ solar-system radius (9.54 AU) |
|---|---|---|---|
| canonical | 9.6001e+26 m = 31112 Mpc = **6.99 c/H₀** | 3.47e+06 | 6.73e+14 |
| alt | 7.9684e+26 m = 25824 Mpc = **5.81 c/H₀** | 2.88e+06 | 5.58e+14 |

A kernel whose only scale is `a₀` has its transition **outside the observable universe** — seven Hubble
radii — and galaxies and the solar system sit on the *same* side of it. The discriminating length is a
**new free parameter**, not `a₀`. (It is the same length this repository's own f30/f33 line calls `ξ` and
calibrates at 0.03–0.15 pc. That is a consistency, not a rescue: it means `a₀` is inserted, not derived.)

**`[GATE] M4` — FAIL. The static limit has not been reached.** The retarded prescription needs a preferred
initial surface (L39) and cosmology supplies one. With `τ = c/a₀`:

| footing | `τ` | `t₀/τ` | accumulated response today | `a₀_eff(z=1)/a₀_eff(0)` | `a₀_eff(z=5)/a₀_eff(0)` |
|---|---|---|---|---|---|
| canonical | 101.5 Gyr | 0.136 | **12.7%** | 0.440 | 0.090 |
| alt | 84.2 Gyr | 0.164 | **15.1%** | 0.444 | 0.091 |

(`t(z=0) = 13.80`, `t(z=1) = 5.85`, `t(z=5) = 1.17` Gyr, flat ΛCDM `Ω_m = 0.315`.) So `a₀_eff` would still
be rising roughly linearly in cosmic time — **56% lower at `z = 1` than today**. The repository's own
recorded standing (stage-17 derived law) is **flat to < 1% for `z ≤ 5`**, and the MUSE front records `a₀`
**rising with redshift**. The memory transient has the wrong *magnitude* against one and the wrong **sign**
against the other. Both quoted as standing; neither re-derived in this lane.

**M5 (PASS).** The requirements are now explicit, which is the constructive part of PART C: **nonlinear in
the field; nonlocal in space as well as time; carrying a transition length that is not `c²/a₀`; and with a
temporal tail short enough to have converged.** No kernel meets M3 and M4 with `a₀` as its only scale.

---

## 5. The lensing lock — a memory kernel is a function of `□`, and it is caught

**X1 (PASS).** Transverse symmetric operators, counted by an explicit SVD solve at five random momenta:

| available background structures | transverse solutions |
|---|---|
| `{η^{μν}, k^μk^ν}` — **no preferred vector** | **1** |
| adding a unit timelike `ū` | **2** |

Reproduces L39. The single frame-free structure is `B(□)(∂^μ∂^ν − η^{μν}□)`, and **`B` may contain `□⁻¹`
or any memory kernel** — nonlocality buys nothing.

**X2 (PASS).** For `ds² = −(1+2Ψ)dt² + (1+2Φ)δ_ij dx^i dx^j`, computed from the metric here:
`R⁽¹⁾ = −2∇²Ψ − 4∇²Φ` and `R_00⁽¹⁾ = ∇²Ψ`. Both coefficients of `R⁽¹⁾` are nonzero, so the ratio is locked
at **1 : 2** and cannot be chosen.

**X3 (PASS) — the identity that makes the mechanism unmistakable, and it is one step past L39.** The
unique frame-free transverse structure is, up to a factor, the **linearised Einstein tensor of a pure
conformal perturbation**:

    G^(1)[h = 2 sigma eta]  =  2 ( eta_{mu nu} Box sigma  -  d_mu d_nu sigma )      [verified symbolically]

So every frame-free addition to the field equations is, at linear order, **a conformal redefinition of the
metric**.

**X4 (PASS).** And a conformal factor cannot bend light: from the Christoffels of `Ω²g`,
`Γ̃^a_{bc}k^bk^c − Γ^a_{bc}k^bk^c − 2k^a(k·∂lnΩ) = 0` for null `k` — a reparametrisation, nothing more.

**`[GATE] X5` — FAIL. A frame-free memory kernel does NOT escape the lock.** X1 → X3 → X4 is a chain, not
an enumeration: the deflection stays at the GR-with-baryons-only value while dynamics demand **3.39–3.48×**
in SPARC outskirts (computed here) and **~6.8×** in clusters (repository standing, g04a, quoted). Escaping
requires adjoining a unit timelike `u` — X1's second structure — which is exactly the preferred-frame
object the programme's single-metric pincer already constrains, and exactly what DEFW 2011 and
Deffayet–Woodard 2026 were forced to add.

---

## 6. The mode count, and all independent initial data

**E1 (PASS).** Rank of the map (hidden-sector initial data) → (observable trajectory), for a bath of 30
oscillators: **58 independent directions out of 60**, against the one observable's own 2. (The shortfall
from 60 is numerical — the weakest-coupled oscillators at the edge of the spectral density — not
structural.) For a branch-cut kernel rather than 30 poles this is a **continuum per space point**.

**E2 (PASS) — the count, per reading, with the price attached:**

| reading | `N_grav` | free initial data on the slice | price |
|---|---|---|---|
| (a) retarded / physical-limit prescription | **2** | graviton 2 × 2 = 4 functions | not a constraint (C5c); needs a preferred initial surface; by H2 it is a **choice of state** for the hidden sector |
| (b) the causal **variational** formulation (V1–V2) | **2 + 2** | + `(a, ȧ)` / `(q_q, q̇_q)` | the second field is exactly the `±½` off-diagonal pair |
| (c) the localised nonlocal action | 2 + n_aux (**6** for the published DEFW MOND model) | + `2 n_aux` | L39's C6, not recomputed here |
| (d) the honest count once H1–H6 are admitted | 2 + the hidden sector's | + the whole bath | a **continuum** per space point for a branch-cut kernel, a **ghost** for a rational one |

**`[GATE] E3` — FAIL.** The architecture delivers `N_grav = 2` in reading (a) exactly as L39 found — and
**that remains more than any local construction in this programme has managed** — but the 2 is bought by
fixing the state of a sector whose initial data is measured at rank 58. **The two-mode claim survives as a
statement about the classical effective theory and fails as a statement about the states.**

---

## 7. Answers to the lane's questions, in order

| question | answer |
|---|---|
| Does any enumerated formulation give a genuinely causal kernel from a variational principle? | **YES** — the doubled-field (in-in / Galley) route, V1, distance `0.0000` from `G_ret`. It is the *only* one: C6c closes every single-field action, nonlinear and nonlocal included. |
| Is the memory fundamental or bookkeeping for hidden states? | **Bookkeeping**, with no exception (H1/H2/H4/H6, trichotomy exhaustive). |
| Can a memory kernel produce a static MOND modification at all? | Only if it is nonlinear (M1), spatially as well as temporally nonlocal (M2), and carries a transition length that is **not** `c²/a₀` (M3) with a tail short enough to have converged (M4). `a₀` is then an input. |
| Does it escape the lensing lock? | **NO** (X5). Caught by a mechanism: `□`-kernel → unique transverse structure → conformal shift → zero extra deflection. |
| Mode count? | **2** under the retarded prescription; **2 + 2** in the causal variational formulation; **6** localised for the published DEFW model; **2 + a continuum per space point** honestly. |
| Full initial-data content? | 4 graviton functions **plus** the hidden sector's — rank 58 of 60 measured for a 30-oscillator bath, a continuum for a branch-cut kernel. |

---

## 8. What survives of the owner's intuition, and what does not

The paddle picture is **the correct picture of what a retarded kernel is**, and that is exactly the point.
Water keeps pushing the paddle because the water is *there*, carrying energy and its own degrees of
freedom. The analogy does not license ignoring the medium; computed out, it **insists** on one. That is
not a dismissal of the intuition — it is the intuition taken literally and followed to its consequence,
and the consequence is a hidden sector with initial data.

Stated plainly and without inflation: **a suggestive analogy is not evidence**, and the lead is right about
that. Equally, this lane is not a reason to retire the idea's one real achievement — L39's `N_grav = 2` in
the retarded reading, reproduced here, remains the only two-mode result this programme has, and the
localised counting rule really is unreliable.

---

## 9. What this changes in the programme's standing record

- **Door 6's pass condition is half met and half failed, and the halves are now separable.** "Test whether
  variation produces the intended causal kernel rather than its time-symmetric counterpart" — it **can**,
  by doubling (V1). "Compute the spectrum and all independent initial data before claiming that memory
  carries no additional modes" — done, and memory **does** carry them (E1, E3).
- **L39's A4 should be upgraded, not corrected.** The single-field obstruction is not merely that a
  quadratic nonlocal action symmetrises; by the Helmholtz condition **no** action, of any order, yields a
  causal kernel (C6c: obstruction 0.70 linear, 0.87 nonlinear, both controls at zero). This matters
  specifically because MOND needs a nonlinear kernel (M1), which the bilinear argument never covered.
- **L31's `±½` gets a name.** It is the Keldysh doubling (V2: `K = [[0,½],[½,0]]` identically). That
  explains *why* L39's C5 defusal was right, and simultaneously why the doubling is not an escape.
- **The lensing lock gets a mechanism in one line.** Frame-free addition = conformal shift = no deflection
  (X3 + X4), which is a strictly stronger statement than L39's operator count and reaches the same place.
- **A new, sharp, internal argument against any `□`-based MOND kernel, independent of memory.** M3: the
  MOND length is `6.99 c/H₀` (canonical) / `5.81 c/H₀` (alt), so a kernel whose only scale is `a₀`
  transitions outside the observable universe. Any construction in this programme that discriminates by
  `□` rather than by acceleration inherits this and must supply a second length.
- **Nothing here contradicts the lead's IC-series.** The metric sector being exactly Einstein with
  `N_grav = 2` and one separately counted healthy clock remains what the lensing lock predicts, and door 6
  does not supply an alternative to it.

## 10. What is NOT claimed

1. That the in-in/Galley doubling is original — it is standard, and it is used here because door 6 asked
   for exactly it.
2. That the specific bath of H1 is *the* hidden sector of any gravitational memory theory. It is an
   existence construction: it shows the kernel *can* be a bath's propagator, and H4/H6 show it must be
   something of that kind. The identification of the actual states in a gravitational case is not made.
3. That the M4 transient argument excludes memory outright. It assumes the memory time is `c/a₀`, which
   follows only if `a₀` is the kernel's scale; M3 already shows that if `a₀` is *not* the kernel's scale,
   the scale is a free parameter. The two failures are alternatives, and either one is sufficient.
4. That the `a₀(z)` comparison in M4 is re-derived here. The stage-17 derived law and the MUSE result are
   quoted from the repository's standing record.
5. That door 6 is "closed". It is closed **on the gates run here**, which are the ones the door itself
   names. A memory architecture built on a unit timelike `u` is not excluded by X5 — it is thrown back
   onto the preferred-frame constraints the programme already runs, where it must be tested separately.
