# L25 — the universal external field: does the eta-matching force one, and would galaxies survive it?

2026-09-08. Script `L25_universal_efe.py`, output `L25_universal_efe.out`. **10 PASS, 7 FAIL.**
Nothing under `integrable_clock_construction_2026/` was edited, imported or rerun; the lead's files
were read, and every equation below was re-derived here with sympy.

This closes L11's B5, the one input its galactic-limit reduction left undetermined.

---

## The short version

**Part 1 — what the eta-transition gives.** The far-field `u` for an isolated galaxy tends to **0**
— not to the cosmological value, and not to something in between — throughout the `eta = 0` region,
and the `eta = 0` region extends **at least 32×** beyond the last measured rotation-curve point.
The reason is structural, not numerical: on `eta = 0` the auxiliary field `u` appears in the static
Lagrangian **with no derivatives at all**, so its Euler-Lagrange equation is algebraic and it cannot
carry a far-field boundary condition of any kind. There is nothing for the cosmological value to be
imposed *through*.

**Part 2 — would rotation curves survive if it did.** **No.** A universal `g_ext = 0.28 a0` caps the
boost at `nu = 4.09`, turns the median outer rotation-curve slope from `+0.110` to `-0.040` against
an observed `+0.046`, takes the fraction of declining outer curves from 8% to 41% against 16%
observed, and degrades the profiled-Upsilon fit by `Delta chi2 = 796` with errors *already* inflated
to `chi2/dof = 1`.

**The deliverable — the hard upper bound on a universal external field from SPARC rotation curves:**

```
    g_ext <= 0.207 a0 (canonical) / 0.196 a0 (alt)     at the framework's own a0 (+- 0.1 dex)
    g_ext <= 0.207 a0            / 0.205 a0            with a global a0 refit of up to +- 0.5 dex
```

The smallest value the lead's exhibited cosmological solutions offer, **0.277 a0**, exceeds that by
1.34–1.42×. The values **IC11's own varied transition actually produces**, 0.490–0.587 a0, exceed it
by 2.4–2.9×, at `Delta chi2 = 4296–6898` (66–83 sigma) with a0 fully profiled.

**So: the eta-matching is not a loose end. It is a live kill switch, and the thing that keeps it from
firing is E2.**

---

## Part 1, in detail

### E1 — what `eta` is a function of (PASS)

IC5 defines the activation by `r = -N p /(3 m h0)` with `p = h_{mu nu} P^{mu nu}` — the **trace of
the metric momentum**. `eta` is therefore a function of the **local expansion rate and of nothing
else**: no `Phi`, no `|a|`, no `rho`, no position. Verified verbatim against `IC5_ACTION.md`, and by
evaluating the published smooth switch: `eta` and its first two derivatives are **identically zero**
(0.000e+00, not "small") for `r^2 <= 1/2`, and `1 - eta` is identically zero on `|r^2 - 1| <= 1/4`.
A quasi-static region therefore sits at `eta = 0` on a *neighbourhood*.

### E2 — `u` carries no boundary condition on `eta = 0` (PASS, PASS, PASS)

Three steps, all re-derived here rather than inherited from L11:

- **E2a.** The conformal 3-curvature identity `e^(-2w) Rbar = R3 + 4 Lap_h w - 2|Dw|^2` for
  `hbar = e^(-2w) h`, derived for a general spherically symmetric leaf. Exact zero residual.
- **E2b.** IC5's static gradient block `m[2 u xi a.Du + xi^2 |Du|^2]` combines with the
  barred-curvature difference into an **exact null Lagrangian** — all three Euler-Lagrange residuals
  (in `Phi`, `Psi`, `u`) vanish identically. So the `eta = 0` sector is IC1's.
- **E2c.** In IC1's static density `u` appears with **no derivatives**: `dL/du' = 0`, `dL/du'' = 0`.
  The `u` equation reduces to `a.a = a0^2 ln^2(1-u^2)`, i.e. `u^2 = 1 - e^(-|a|/a0)` pointwise.

**A field with no derivatives in its own Euler-Lagrange equation admits no boundary datum.** That is
the whole answer to part 1's first half. The question "does far-field `u` go to 0 or to `u_cosmo`?"
is malformed inside `eta = 0`: `u` is slaved to the local field, and the local field goes to zero.

### E3 — where the eta boundary actually is (PASS)

`eta` can leave 0 only where `r^2 > 1/2`. Calibrating `r` against the lead's own solutions
(IC11_CLOCK_PRESSURE's table gives `r/H_physical = 0.981–1.350`) and taking the **largest** ratio —
conservative, because it makes `eta` leave 0 earliest — `eta = 0` is guaranteed wherever
`H_local <= 0.524 h0`.

Two independent, deliberately conservative criteria over 141 SPARC galaxies (2734 points):

| criterion | min | median | max |
|---|---:|---:|---:|
| `R(Hubble-velocity crossing) / R_last` | **31.6** | 117.9 | 550.9 |
| `R(Lambda zero-gravity) / R_last` | **38.1** | 135.1 | 552.2 |

`R_last` runs 1.1–108 kpc; both criteria put the earliest possible eta boundary at 0.3–3 Mpc.

*Direction stated:* this is a **kinematic estimate** of the local expansion rate around a bound
object, not a solution of the IC field equations in the transition region. That is exactly what E4
names as missing.

### E4 — what is still missing (FAIL)

**L11's B5 is partly superseded: IC11 HAS now varied the transition.** But only on a *homogeneous*
background — a 501-point continuation in the trace momentum `rho` from the IC10 plateau through the
switch boundary, giving `u = 0.622175` (n=200), `0.625545` (n=220), `0.666132` (n=500). Those are
the cosmological `u` values continued **in time**; no radius appears anywhere in that calculation.
And that trial **fails a necessary scalar kinetic condition**, `aUV < 0` from n = 205 onward.

**The missing input, named exactly:** a solution of the full phase equations for a **bound mass**
embedded in the expanding plateau, with `eta` varying in **space** (not in the homogeneous momentum),
so that `r(x)^2` crosses 1/2 at some radius and `u` is continued across it. Nothing published
attempts that, and the only transition action that has been varied is unhealthy.

---

## Part 2, in detail

### Controls (all PASS)

- **C0.** The construction's own kernel `mu(y) = 1 - e^(-y)`: solver residual `3.4e-16`, deep-MOND
  coefficient `1.00000025` at `s = 1e-12`, Newtonian ratio `1.00000000`.
- **C1.** At `g_ext = 0` the pipeline reproduces the radial acceleration relation: scatter
  **0.140 dex** on both footings against the published ~0.11–0.13 at fixed Upsilon, median offset
  `+0.076 / +0.048` dex. The small excess is expected — no distance or inclination marginalisation,
  `eV/V < 0.10` in place of SPARC's Q/i cuts, and the kernel is the exponential carrier whose too-low
  ceiling is L11's B2b, showing up here as the positive offset.
- **C2.** The external-field implementation reproduces **seven** published numbers of this repository
  at their stated parameters (`aqual_efe_full_solve_2026.py` PART A, `stage64_efe_two_body_exact_2026.py`
  PART B; `x_ext = 1.9`, Route A kernel), all to `< 5e-3`:

  | quantity | this file | recorded |
  |---|---:|---:|
  | `y_extN` | 1.28969 | 1.28903 |
  | `B_par = nu(y_extN)` | 1.47322 | 1.47342 / 1.4732 |
  | `dx/dy` | 1.07736 | 1.07749 |
  | `B_perp = nu/sqrt(1+L0)` | 1.25984 | 1.2598 |
  | `sqrt(nu)` canonical / alt | 1.21376 / 1.25911 | 1.2139 / 1.2592 |
  | MI orientation average | 1.15813 | 1.1582 |

### What an external field does to *this* kernel

| `u_cosmo` | `y_ext` | `nu_ext = 1/mu` | `L0` | `B_par` | `B_perp` | `<B>` | source |
|---:|---:|---:|---:|---:|---:|---:|---|
| 0.492193 | 0.2774 | 4.128 | 0.868 | 4.128 | 3.021 | 3.390 | IC10 S=0.10 |
| 0.536585 | 0.3396 | 3.473 | 0.840 | 3.473 | 2.561 | 2.865 | IC10 S=0.15 |
| 0.570419 | 0.3936 | 3.073 | 0.816 | 3.073 | 2.281 | 2.545 | IC10 S=0.20 |
| 0.622175 | 0.4896 | 2.583 | 0.775 | 2.583 | 1.939 | 2.154 | **IC11 transition n=200** |
| 0.666667 | 0.5878 | 2.250 | 0.735 | 2.250 | 1.708 | 1.889 | IC4/IC5 witness |
| 0.666132 | 0.5865 | 2.254 | 0.735 | 2.254 | 1.711 | 1.892 | **IC11 transition n=500** |

**Conservatism declared:** the isotropic (quadrature) composition used throughout gives the boost
`B_par`, the *larger* eigenvalue, while the orientation average is 1.218× smaller. Every number here
therefore **understates** the damage, and the bound below is an upper bound on the bound. The
colinear composition, quoted alongside every `Delta chi2`, is 3–4× more damaging still.

### F1 / F2 — flat rotation curves do not survive (both FAIL)

Outer log slope `beta = dlnV/dlnr` over `r >= 0.6 R_last`, canonical footing:

| | median `beta` | % declining (`beta < -0.10`) | % flat (`\|beta\| < 0.10`) |
|---|---:|---:|---:|
| observed | **+0.046** | **16.3** | **43.3** |
| `g_ext = 0` | +0.110 | 7.8 | 41.1 |
| `g_ext = 0.28 a0` | **-0.040** | **41.1** | 24.8 |
| `g_ext = 0.59 a0` | **-0.141** | **52.5** | 23.4 |

RAR damage (canonical): scatter `0.140 -> 0.150 -> 0.191` dex, zero point `+0.076 -> +0.119 -> +0.186` dex.

Profiled-Upsilon fit, errors inflated to `chi2/dof = 1` (so `Delta chi2 = 9` is a genuine 3 sigma):

| | canonical | alt | colinear composition (canonical) |
|---|---:|---:|---:|
| `g_ext = 0.28 a0` | **+796 (28.2 s)** | +506 (22.5 s) | +3465 |
| `g_ext = 0.59 a0` | **+5683 (75.4 s)** | +6239 (79.0 s) | +9305 |

### F3 — the hard upper bound (F3a, F3b, F3c all FAIL)

Four constructions. Each bound is the upper edge of the `Delta chi2 = 9` region measured from the
**minimum of the profiled curve**, not from `x = 0`.

| construction | canonical | alt | profiled minimum at |
|---|---:|---:|---|
| (a) framework's own a0, Upsilon profiled | 0.120 | 0.160 | x = 0.100 / 0.150 |
| (b') a0 profiled ±0.1 dex (the real footing spread is 0.081 dex) | 0.165 | 0.188 | x = 0.150 / 0.175, a0 +0.10 dex |
| (b) a0 profiled ±0.5 dex (adversarial) | 0.205 | 0.205 | x = 0.200, a0 +0.30 / +0.20 dex |
| (c) fit-free: median outer slope within 3 s.e. of observed | 0.207 | 0.196 | — |
| **HARD BOUND (weakest)** | **0.207** | **0.196** | at framework a0 ±0.1 dex |
| **HARD BOUND (adversarial a0)** | **0.207** | **0.205** | with ±0.5 dex of a0 |

Every `u` the lead's own solutions exhibit, against that bound:

| `u_cosmo` | `g_ext/a0` | `Delta chi2` a0 fixed (can/alt) | `Delta chi2` a0 profiled ±0.5 dex (can/alt) |
|---:|---:|---|---|
| 0.492193 | 0.2774 | +809 / +773 (28 / 28 s) | +535 / +606 (23 / 25 s) |
| 0.536585 | 0.3396 | +1549 / +1630 (39 / 40 s) | +1418 / +1568 (38 / 40 s) |
| 0.570419 | 0.3936 | +2329 / +2565 (48 / 51 s) | +2398 / +2644 (49 / 51 s) |
| **0.622175** | **0.4896** | +3951 / +4437 (63 / 67 s) | **+4296 / +4725 (66 / 69 s)** |
| 0.666667 | 0.5878 | +5682 / +6489 (75 / 81 s) | +6304 / +6925 (79 / 83 s) |
| **0.666132** | **0.5865** | +5659 / +6461 (75 / 80 s) | **+6278 / +6898 (79 / 83 s)** |

The a0 degeneracy is real but **bounded**: absorbing `g_ext = 0.28 a0` costs a0 `+0.26 dex`
(a factor 1.8, 3× the gap between the programme's two footings), and a full ±0.5 dex of a0 freedom
moves the chi2 bound only from 0.120/0.160 to 0.205/0.205 a0. It does not open enough room.

### F5 — one result that runs the other way, reported at face value (FAIL)

The profiled fit does **not** peak at `g_ext = 0`. SPARC mildly **prefers** `g_ext ~ 0.10–0.20 a0`
for this kernel, and the two-parameter family `{exponential carrier, g_ext}` with a0 refitted beats
even the programme's carried `nu_RAR` with no external field, by `Delta chi2 = 367` (canonical) /
`420` (alt):

| model (canonical) | chi2 |
|---|---:|
| exponential carrier, footing a0, no EFE | 3144.8 |
| exponential carrier, a0 refit, no EFE | 2815.1 |
| **exponential carrier, a0 refit + best g_ext (0.200 a0)** | **2081.3** |
| nu_RAR (carried kernel), footing a0, no EFE | 2501.2 |
| nu_RAR, a0 refit, no EFE | 2448.3 |

This is an **interpolation-function statement** (two parameters against one), not a detection of a
universal field — and real galaxies do sit in ~0.01–0.1 a0 of large-scale-structure field anyway.
It does not rescue 0.277 a0. But it does mean that **a small universal floor, below ~0.2 a0, would
cost the construction nothing at all** — which is worth knowing if the spatial transition turns out
to leave a residual `u` rather than exactly zero.

---

## What the lead should do with this

1. **The one calculation that closes it.** Solve the full phase equations for a bound mass embedded
   in the expanding plateau with `eta` varying in **space**, and confirm `r(x)^2 < 1/2` throughout
   the rotation-curve region. E1–E3 say this should come out cleanly — `eta`'s argument is the
   expansion rate, and the expansion rate around a galaxy is far below `0.52 h0` out to Mpc scales —
   but it has not been done, and until it is, the construction has an unchecked path to a 28–83 sigma
   failure on rotation curves.

2. **A cheaper sufficient version.** Do not solve for `u(x)` at all: show that any admissible `eta`
   profile keeps the effective `g_ext` below **0.196 a0** inside `R_last`. That is the whole content
   of the constraint, and it is a one-inequality target.

3. **Do not treat the homogeneous continuation as the matching.** IC11's 501-point run varies `eta`
   in the momentum, which is a cosmological history, not a galactic boundary. Its `u = 0.622–0.666`
   are exactly the values SPARC excludes at 66–83 sigma if they ever reach a galaxy. If the spatial
   transition is written in terms of the same continuation, that is the number to watch.

4. **The a0 side-constraint.** If any residual universal field survives the matching, the theory can
   partly absorb it by raising a0 — but by at most ~0.2 dex before the outer-slope test bites
   independently, and any such shift has to be re-checked against every a0-calibrated result in the
   corpus (BTFR zero point, the two footings, the DR4 registration).

---

## Scope and limits, stated

- The rotation-curve response is the standard **algebraic** AQUAL EFE,
  `mu(|g_int + g_ext|/a0) g_int = g_N`, in the isotropic composition. Its `g_int -> 0` limit is the
  exact AQUAL linear-response eigenvalue `B_par` (validated in C2), i.e. the larger one — so it
  understates the damage by 1.218×. A full nonlinear disc-in-external-field PDE solve would tighten
  the bound, not loosen it.
- Upsilon is profiled per galaxy under a 0.11 dex lognormal prior (`Upsilon_bul = 1.4 Upsilon_disk`);
  errors are inflated to `chi2/dof = 1` before any `Delta chi2` is read; a global a0 rescaling is
  profiled as a nuisance. No distance or inclination marginalisation — that is the one remaining
  freedom, and it is a per-galaxy nuisance that cannot generate a coherent shape change of this size.
- E3's transition radius is a kinematic estimate of the local expansion rate, not an IC solution.
- Both a0 footings throughout: 9.3619e-11 / 1.1279e-10 m/s^2.
