# A60 — the Solar System's P configuration: the Sun embedded in the Galaxy

**Lane:** A60_solar_p_config · **Date:** 2026-10-21 · **Base:** `DS_FINAL_2026_10_21/BRIEF.md`,
`A22_ppn_frames/report.md`, `A36_galactic_alpha1/report.md`, `THEORY.md` §2–§3
**Script:** `a60_checks.py` (20/20 PASS, exit 0) · **Output:** `a60.out` · **Data:** `a60_results.json`
**Action:** the frozen round-2 ADM action verbatim (A22 §D1); `c = 1`, signature `(-+++)`, `K = 4 pi G`,
`gamma = K L*^2/2`, `L* = 24 pc`, `a0 = 9.36e-11 m/s^2` (canonical footing) unless stated.
`K = 4 pi G` is the unique EH normalisation (A61 K1); BRIEF.md's "`K = 8 pi G`" is a factor-2 mislabel
of the same symbol, and every P-sector formula here is in the `K = 4 pi G` normalisation in which
`gamma = K L*^2/2` is calibrated. A61 fixes `L* = 24.025 pc`; the 0.1 % shift is immaterial to every
number below (`alpha_1 ∝ L*^{-2}`).

## Claim

The Sun's P field is **not** the isolated hedgehog. It is the galactic background plus a small,
exactly computable perturbation:

> **P = P̄(galactic, `u = 0.566 a0`, pointing away from the Galactic Centre) + π (solar hedgehog,
> `u = GM/L*^2 = 2.42e-16 m/s^2 = 2.59e-6 a0`, radial, constant to 1 pc).**
> The nonlinearity is controlled by `eps_2 = u_sun/u_gal = 4.57e-6`: the amplitude composition fails
> only at `O(eps_2^2) = 2.1e-11`, and the full nonlinear solve moves the profile by `< 9e-7`.
> There is **no crossover radius in u**: the solar contribution is 4.6e-6 of
> the galactic one at 1 AU and 4.3e-6 at 1 pc. The dynamical crossover (`g_sun = g_gal`) is at
> `6.97e3 AU = 0.0338 pc`.

The consequence for the preferred-frame parameter:

> **`|alpha_1(1 AU)| = 1.63e-13` on the embedded background, against `1.63e-13` for the isolated Sun
> — a shift of 4.9e-8 relative (8e-21 absolute).** The Solar System gate (`|alpha_1| < 1e-4`)
> survives the embedding by **6.1e8**, and A22's isolated-Sun solution was adequate for `alpha_1`.
> A36's K12 "factor 2.19e5 mismatch" is the expansion's small parameter, not a contradiction.

At the Pioneer distances the theory predicts **no observable preferred-frame anomaly**: the largest
signal is `(2 to 4) w^2 a_P = 7e-22` to `1.5e-21 m/s^2`, about `1e11` below the Pioneer thermal-recoil
residual `1.33e-10 m/s^2`. The theory's own constant sunward anomaly `a_P = 2.42e-16 m/s^2` is
`2.8e-7` of the Pioneer anomaly — the right shape, six and a half decades too small.

**Status: `CLOSED-DERIVED` for the configuration (two-scale expansion, controlled to 11 % at 1 pc and
1e-17 at 1 AU); `PASS` for the Solar System gate at every measured radius.** One scope statement is
load-bearing and is stated in §5: the theory has no asymptotic PPN limit, so `alpha_1` is a *running*
coefficient, and it reaches `1e-4` at `0.12 pc = 2.5e4 AU` — the Oort cloud, not the planetary system.

---

## 1. The two-scale problem

### 1.1 The exact static equation

Varying the action with respect to `P_i` (static, `E = 0`, `F = 0`) gives

  (1)  `gamma lap(P_i) + d_i ln N - K W'(u) P_i/|P| = 0`,   `u = K|P|`,   `K W'(u) = u/(1-u/a0)`.

`K4` verifies that `p = GM/(2 gamma)` solves this exactly for a point mass, and that the only other
homogeneous solutions are `r` and `1/r^2` (so the regular, decaying solution is unique). `K1`
verifies `W'`, `W'' = 1/(K(1-u/a0)^2)` and the inverse `u = a0 g/(g+a0)` identically.

### 1.2 The ansatz and the three small parameters

Write `P(x) = Pbar(X) + pi(x)` with `X = x/R_gal`, `R_gal = 8 kpc`, and `x` the local coordinate.
Because `d_x = d_x|_X + R_gal^{-1} d_X`, the equation splits into an outer problem on `X` and an
inner problem on `x`. Three dimensionless parameters control the split:

| parameter | definition | value at 1 AU | value at 1 pc | controls |
|---|---|---|---|---|
| `eps_1` | `r/R_gal` | 6.1e-10 | 1.25e-4 | scale separation |
| `eps_2` | `u_sun/u_gal` | 4.57e-6 | 4.30e-6 | **the nonlinearity** |
| `eps_3` | `m^2/(gamma k^2) = (r/ell)^2` | 1.9e-13 | 0.008–0.018 | the background's effect on the response |

The frozen-background error is not `eps_1` alone but `eps_bg(r) = (r/R_gal)(g_gal/g_sun(r))`:
`1.2e-17` at 1 AU, `1.1e-4` at 0.1 pc, `0.11` at 1 pc, and it reaches 1 at

  (2)  `r* = (GM R_gal/g_gal)^{1/3} = 2.09 pc`   (K5).

So the expansion is excellent out to 0.1 pc, 11 % at 1 pc, and fails at 2 pc. That is the honest
domain of the calculation, and it covers everything the lane was asked for.

### 1.3 The outer solution (input, A36's Milky Way)

A Hernquist galaxy with `M_bar = 6e10 Msun`, `a = 3 kpc`, the canonical law `g = (g_N/2)(1+sqrt(1+4a0/g_N))`:

| quantity | value |
|---|---|
| `g_N(8 kpc)` | `6.913e-11 m/s^2` |
| `g(8 kpc)` | `1.221e-10 m/s^2 = 1.3047 a0` |
| `ubar = g - g_N` | `5.299e-11 m/s^2 = 0.56611 a0` |
| `pbar = ubar/K` | `6.318e-2 kg/m^2` |

`K3` verifies the background is on-shell (`K W'(ubar) = g_gal` to 1e-14) and inside the cap.
The background's masses are `m_L^2 = K/(1-ubar/a0)^2 = 4.455e-9` and `m_T^2 = K/(1-ubar/a0) = 1.933e-9`,
i.e. screening lengths `ell_L = 7.36 pc` and `ell_T = 11.18 pc`. **These are the only way the Galaxy
enters the Solar System problem.**

The direction: `P` is anti-parallel to the gravitational field (`K W'(u) Phat = grad ln N = -g`), so
`Pbar` points **away from the Galactic Centre**. The solar hedgehog also points away from the Sun
(`pi_r > 0`). Both have positive charge, `psi = div P > 0`, and both gravitate.

### 1.4 The inner solution: exact

Linearising (1) about `Pbar` (`K6`, symbolic residual 0 and finite-difference agreement 1.7e-8) gives

  (3)  `gamma lap(pi) - m_L^2 (e.pi) e - m_T^2 pi_perp = -grad(delta ln N_sun)`,

with `e = Phat_bar` and `delta ln N_sun = -GM/r`. For the isotropic mass `m` the exact solution is

  (4)  **`pi_r(r) = p0 f(r/ell)`,  `f(x) = 2[1 - e^{-x}(1+x)]/x^2`,  `p0 = GM/(2 gamma)`,  `ell = 1/m`,**

  `f(0) = 1`, `f = 1 - 2x/3 + x^2/4 - ...`, `f -> 2/x^2`. `K7` verifies (4) solves (3) identically
  (symbolic residual 0), and `K8` verifies it against an independent `solve_bvp` integration to
  `2.3e-10` over `0.01–30 pc`. The same `K8` runs the **full nonlinear** equation (no linearisation
  in `pi`): the nonlinear solution differs from (4) by at most `8.8e-7` anywhere — that is the
  measured size of the superposition failure.

**Why superposition is legitimate here, quantitatively.** The equation's only nonlinearity is
`K W'(u)`. Expanding about the background,

  `K W'(u) Phat = K W'(ubar) e + m_L^2 (e.pi) e + m_T^2 pi_perp + O(pi^2/pbar)`.

The first term is the outer solution (already solved), the next two are the linear operator (3), and
the remainder is of order `eps_2^2` relative to the linear term. There is no other nonlinearity in
(1). So the two-scale solution is the linear response plus a correction of relative order
`eps_2^2 = 2.1e-11`, and the exact nonlinear solve (K8) confirms `<= 8.8e-7` in the profile.

**Why the solar amplitude is `GM/L*^2` and not `a0`.** At `r << ell` the mass term is negligible and
(3) reduces to `gamma lap(pi) = -grad(delta ln N)`, whose regular solution is the constant-magnitude
hedgehog. In numbers: `gamma lap(pi) = 2 gamma p/r^2 = u L*^2/r^2`, which must balance `g_sun = GM/r^2`,
so `u = GM/L*^2`. This is exactly A22's result, and it is *forced* by gradient balance, not chosen.
A36's K12 computed the gradient cost of the alternative (`u = a0`): `2 gamma u/(K r^2) = 2.29e3 m/s^2`
at 1 AU, `3.9e5` times `g_sun` — which is the proof that the field cannot be slaved, not a proof that
no configuration exists (K11). The measured gradient-balance residual of (4) is `8.5e-9`.

### 1.5 The charge, and the metric response

  (5)  `psi(r) = div(pi) = (p0/ell)[f'(x) + 2f(x)/x] = 2 p0/r` at small `x` (A22's `GM/(gamma r)`),

  (6)  `Phi_P(r) = K int_0^r pi ds = u0 ell I(x)`,  `I(x) = 2 - 2e^{-x} - 2(1-e^{-x}(1+x))/x`,

  `I(0) = 0`, `I(inf) = 2`, `dI/dx = f` (K7). At 1 AU, `Phi_P = (GM/L*^2) r` to `1.4e-7` (K16): **A22's
  `a_P` is unchanged by the embedding**, because `div` is linear and the solar charge is untouched by
  the background.

---

## 2. The field: `u(r)` from 1 AU to 1 pc, and the crossovers

`u(xhat) = K|Pbar + pi| = ubar + u0 f(r/ell) cos(psi) + O(u0^2/ubar)`, where `psi` is the angle between
`xhat` and the direction away from the Galactic Centre. The table:

| `r` [AU] | `r` [pc] | `u_sun/a0` | `u_sun/u_gal` | `u/a0` (max) | `u/a0` (min) |
|---|---|---|---|---|---|
| 1 | 4.85e-6 | 2.5860e-6 | 4.568e-6 | 0.566109 | 0.566103 |
| 10 | 4.85e-5 | 2.5860e-6 | 4.568e-6 | 0.566109 | 0.566103 |
| 100 | 4.85e-4 | 2.5859e-6 | 4.568e-6 | 0.566109 | 0.566103 |
| 1e3 | 4.85e-3 | 2.5852e-6 | 4.567e-6 | 0.566109 | 0.566103 |
| 2.06e3 (=0.01 pc) | 0.01 | 2.5844e-6 | 4.565e-6 | 0.566109 | 0.566103 |
| 1e4 | 4.85e-2 | 2.5785e-6 | 4.555e-6 | 0.566109 | 0.566103 |
| 2.06e4 (=0.1 pc) | 0.1 | 2.5706e-6 | 4.541e-6 | 0.566109 | 0.566103 |
| 2.06e5 (=1 pc) | 1.0 | 2.4368e-6 | 4.305e-6 | 0.566108 | 0.566104 |

Three facts:

1. **`u_sun` is constant to 6 % over five decades.** The `-2x/3` term in `f` is the whole radial
   dependence; there is no `1/r` monopole because the hedgehog's charge `2p0/r` is not a localized
   charge — the total flux grows with `r`, which is why the constant solution is the regular one.
2. **The Galaxy dominates everywhere.** `u_sun/u_gal` runs from `4.57e-6` to `4.30e-6` — a factor 1.06
   across the entire range. **There is no crossover radius in `u`.** The quantity that measures the
   field is `u = K|P|`, and the solar contribution never comes within five orders of magnitude of the
   galactic one, let alone matching it.
3. **`u_total` is `0.566 a0` to +-4.6 ppm**, and the angular variation is a dipole of relative amplitude
   `4.57e-6` aligned with the Galactic Centre direction (max looking away from the GC). In
   acceleration units that dipole is `5.6e-16 m/s^2` — unobservable.

**The crossover that does exist** is dynamical, and there are four ways to define it:

| definition | radius |
|---|---|
| `g_sun = g_gal` (the solar gradient term equals the galactic one) | `6.97e3 AU = 0.0338 pc` |
| solar charge density `2p0/r` = galactic charge density `psi_gal = 3.99e-22 kg/m^3` | `9.66e3 AU = 0.047 pc` |
| the perturbation's own screening length `ell_T` / `ell_L` | 11.18 / 7.36 pc |
| the two-scale expansion breaks (`eps_bg = 1`) | 2.09 pc |

Beyond `6.97e3 AU` the *gradient* of the total field is the Galaxy's, but the *magnitude* is still
`0.566 a0 + 2.4e-6 a0`. The solar field is a small, radially ordered perturbation on a large, slowly
varying background: it never becomes the field.

---

## 3. `alpha_1` on the embedded background

### 3.1 The formula

With `g_00 = -1 - 2Phi` and the `w^2` foliation lapse `ln N = Phi(1+2w^2)` (A22 K6, A36 K2), the P
source is multiplied by `(1+2w^2)`. Solving the linearised system gives the charge potential
`delta Phi(w^2) = 2 w^2 Phi_P` and therefore

  (7)  **`alpha_1(r) = -4 Phi_P(r)/(GM/r) = -4 (r/L*)^2 I(r/ell)/(r/ell)` ,**

i.e. `-4(r/L*)^2` for `r << ell`, with `ell` set by the **galactic** background (`ell_T = 11.18 pc`).
The minus sign is the `g_00 = -1-2Phi` convention (A22's matching `alpha_1 = P_iso + S/2`); A36's
convention `alpha_1 = 2 delta Phi/(w^2 U)` gives `+4(r/L*)^2`. **The magnitude is convention-independent
and is what the bound constrains.**

Three routes agree at 1 AU (K12):

| route | `|alpha_1(1 AU)|` |
|---|---|
| closed form (7), `I/x = 1 - 1.4e-7` | `1.632252e-13` |
| exact `Phi_P` from the ODE profile + Poisson integral | `1.632252e-13` (rel. `1.4e-7`) |
| `4(r/L*)^2` (the `x -> 0` limit) | `1.632252e-13` |

### 3.2 How much it moves

  (8)  `alpha_1(1 AU)|_embedded = -1.6322519e-13`,  `alpha_1(1 AU)|_isolated = -1.6322520e-13`,

a relative shift of **`4.9e-8`** (absolute `8.1e-21`). The reason is structural: at 1 AU the response
is gradient-dominated, `gamma k^2/m^2 = (ell/r)^2 = 5.3e12`, so the mass term — the only place the
background enters — is 13 orders below the gradient term. The background changes the screening length
(`11.18 pc` vs `16.97 pc`), which changes the `-2x/3` correction to `f`, hence a `5e-8` relative shift.
**The embedding does not move `alpha_1`.**

### 3.3 A36's K11: reproduced and diagnosed

A36's K11 reports `alpha_1(1 AU) = 5.44e-14`. Reproduced exactly (K14): their expression is
`2u'/(D-u')` with `u' = r^2/L*^2` and `D = 1 + (L*/r)^2 u'/2 = 1.5`, which gives `5.4408e-14`. Two
slips sit inside it, both in the safe direction:

| step | value | comment |
|---|---|---|
| A36 K11 as printed (`2u'/(D-u')`) | `5.44e-14` | prefactor is 2, but their own eq. (2.5) has 4 |
| their own prefactor (`4u'/(D-u')`) | `1.09e-13` | `x2` |
| their formula with the correct mass (`(1-u/a0)^2 = 1`, not `u' = r^2/L*^2`) | `3.26e-13` | `x3` |
| exact point source (7) | `1.63e-13` | the `k = 1/r` proxy overestimates by 2 |

The second slip is the interesting one: A36's `D` uses `u' = du/dg` as if it were `(1-u/a0)^2`. On a
*slaved* background those coincide; on the hedgehog they do not — the hedgehog has `u/a0 = 2.6e-6`,
so `(1-u/a0)^2 = 1` while `du/dg = r^2/L*^2 = 4e-14`. The mass term is a property of the background
*value*, not of the derivative along the solution family. Net: **K11 understates `|alpha_1|` by 3x**,
which is harmless — it is still nine orders below the bound — but it should not be quoted as the
theory's number.

### 3.4 The gate

  (9)  `|alpha_1(1 AU)| / 1e-4 = 1.63e-9`,  i.e. **6.13e8 below the bound** (K15).

`alpha_2 = 0` is unchanged: `w` enters only as `|w|^2`, and the anisotropy is in `k.Pbar` (the external
field), not in `w` (A22 K6, A36 K6). `beta_PPN = 1` is unchanged: the background contributes a constant
`u` and a constant stress, with no `1/r^4` source; the `O(rho^2)` exponent argument of A22 D7 is local.
Both are arguments, not recomputations, and are labelled as such.

**The one scope statement.** `alpha_1(r)` is a *running* coefficient, `4(r/L*)^2`, because the P charge
potential grows linearly in `r` — this theory has no asymptotic PPN limit. The running value reaches
`1e-4` at

  (10)  `r = (L*/2) sqrt(1e-4) = 0.12 pc = 2.475e4 AU`   (K15),

and `|alpha_1| = 1` at `14.6 pc` — where the metric correction is still only `w^2|alpha_1| = 1.5e-6`,
so what fails there is the PPN *description* (a constant `alpha_1`), not the weak field. The running
values:

| `r` | 1 AU | 20 AU | 70 AU | 160 AU | 0.01 pc | 0.1 pc | 1 pc |
|---|---|---|---|---|---|---|---|
| `|alpha_1|` | 1.63e-13 | 6.53e-11 | 8.00e-10 | 4.18e-9 | 6.94e-7 | 6.92e-5 | 6.74e-3 |

Every radius at which the solar field has been probed — 1 AU (LLR),
20–70 AU (Pioneer), 160 AU (Voyager) — is deep inside the safe region: `4.2e-9` at 160 AU.

---

## 4. The Pioneer region (20–70 AU)

The task's `1e-9`–`1e-10 m/s^2` is the Pioneer-anomaly scale (`8.74e-10`), not `g_sun` (`1.5e-5` at
20 AU, `1.2e-6` at 70 AU). The relevant question is whether the near-`a0` acceleration puts the P field
on its slaved branch. It does not: the gradient-to-mass ratio is `(L*/r)^2 (1-ubar/a0)/2 = 1.3e10` at
20 AU and `1.1e9` at 70 AU (K18). The solar perturbation stays at `u = 2.59e-6 a0`; the total field
is the galactic `0.566 a0`.

| quantity | 20 AU | 70 AU |
|---|---|---|
| `alpha_1` (eq. 7) | `6.53e-11` | `8.00e-10` |
| preferred-frame acceleration `alpha_1 w^2 g_sun` (r-independent) | `1.47e-21` | `1.47e-21` |
| `a_P = GM/L*^2` (constant, sunward) | `2.42e-16` | `2.42e-16` |
| `2w^2 a_P` | `7.3e-22` | `7.3e-22` |

With `w = 369 km/s`, `w^2 = 1.515e-6`. Comparisons:

* **Against the Pioneer anomaly:** `a_P/a_Pioneer = 2.77e-7`. The theory predicts the Pioneer anomaly's
  *shape* — a constant, sunward acceleration — with the wrong size by 6.6 decades.
* **Against the thermal-recoil residual:** the thermal model of Turyshev et al. (2012) accounts for
  `a_P = (8.74 ± 1.33)e-10 m/s^2` and leaves no significant residual; the `1sigma` scale is
  `1.33e-10 m/s^2`. The P-sector preferred-frame signal is `7.3e-22` to `1.5e-21 m/s^2` (the `2w^2`
  modulation of `a_P`, and the equivalent `alpha_1 w^2 g_sun = 4 w^2 a_P`), a factor **`9e10` to
  `1.8e11` below it** (K17).
* **Against the galactic field's own `w^2` modulation:** `2w^2 g_gal = 3.7e-16 m/s^2`, but that is a
  common-mode rescaling of the galactic acceleration (identical for the Sun, Earth and spacecraft) and
  its tidal part across the Solar System is `~2e-27 m/s^2`. Not an anomaly.

**Answer: no.** The theory predicts no preferred-frame anomaly in the outer Solar System at a level
Pioneer could have seen. The largest term is `1.5e-21 m/s^2`; the data's residual scale is `1e-10`;
the gap is eleven orders. Pioneer does not test this sector, in either direction.

---

## 5. Verdict

**Is the Sun's P configuration established? Yes**, in the two-scale expansion — the first explicit
solution of the Sun-in-the-Galaxy problem in this campaign. The field is

  `P = Pbar(u = 0.566 a0, away from the GC) + pi(u = 2.59e-6 a0, radial, ell = 7.4–11.2 pc)`,

with controlled errors: `1e-17` at 1 AU (background variation), `2.1e-11` (amplitude composition)
and `<= 8.8e-7` (the full nonlinear solve, largest at the outer end of the 0.01-30 pc grid), and
`11 %` at 1 pc (the frozen-background expansion). A36's K12 is resolved: the "2.19e5 mismatch" is
the ratio `u_gal/u_sun`, i.e. the small parameter that makes the embedding a perturbation. The
configuration exists, is regular at the origin, respects the cap (`u = 0.566 a0`, 43 % below `a0`), and
has the correct gradient balance (residual `8.5e-9`).

**Does the Solar System gate survive the embedding? Yes.** The number that decides:

> **`|alpha_1(1 AU)| = 1.63e-13`, against the bound `1e-4` — a margin of 6.1e8 — and the embedding
> moves it by `4.9e-8` relative. `u_sun/u_gal = 4.57e-6` is the small parameter that makes this
> statement controlled.**

Two honest qualifications, neither of which changes the verdict at any measured radius:

1. `alpha_1(r) = 4(r/L*)^2` **runs**. It reaches `1e-4` at `0.12 pc` (2.5e4 AU) and `1` at `14.6 pc`.
   The theory has no asymptotic PPN limit; the gate is a statement about the radii where `alpha_1` is
   measured, and there it passes by 8–9 orders.
2. The gate's `alpha_2` and `beta` legs are argued, not recomputed (§3.4). The background contributes
   no `(w.nhat)^2` structure and no `1/r^4` source, so neither moves at the order that matters.

---

## 6. What this does not do

- **Not a 3-D nonlinear solve with the anisotropic masses.** The masses `m_L != m_T` make the
  linearised operator anisotropic; I solve the isotropic problem and bound the anisotropy by
  `|m_L^2 - m_T^2| r^2 = 6 (r/L*)^2`, i.e. `1e-12` at 1 AU and `1e-2` at 1 pc. The reported numbers
  are the `m_T` (larger-`ell`, conservative) values; `m_L` shifts them by 3 % at 1 pc and nothing at
  1 AU.
- **Not a real galactic field.** The background is a spherical Hernquist model; a real MW has a bar,
  spiral arms and a non-radial field at the Sun. Those change the dipole's *orientation* and add a
  tidal term, not its magnitude: the field varies on 8 kpc, the Solar System is 1e-8–1e-4 of that.
- **No time dependence.** The Sun moves at ~220 km/s through the Galaxy, so the background changes on
  ~40 Myr; the P field's response time is `ell/c ~ 30 yr`, so the adiabatic approximation is excellent,
  but it is an approximation and is not checked here.
- **`alpha_2` and `beta_PPN` are not recomputed** on the embedded background (§3.4).
- **The matching convention for `alpha_1` is imported** (A22 D1, Foster–Jacobson); the sign differs
  between A22's and A36's conventions and is stated explicitly in (7).
- **`a0` and `L*` are inputs.** `alpha_1 ∝ L*^{-2}`: at `L* = 40 pc` it is `5.9e-14`, at `90 pc`
  `1.2e-14` — the verdict strengthens. The `a0` footing moves `u_gal/a0` (0.566 canonical, 0.468
  theory) and `u_sun/u_gal` (4.57e-6 vs 4.01e-6), and leaves `alpha_1(1 AU)` unchanged, because
  `alpha_1` depends on `r/L*` only.

---

## 7. Checks (`a60_checks.py`, 20/20 PASS, exit 0)

| id | what it proves | measured |
|---|---|---|
| K1 | `W'`, `W''`, and the exact inverse `u = a0 g/(g+a0)` | residuals 0,0,0 |
| K2 | `K = 4 pi G`, `gamma = K L*^2/2`, `u0 = GM/L*^2` | `2.4205e-16` |
| K3 | the galactic background is on-shell and inside the cap | `K W'(ubar)/g - 1 < 1e-14` |
| K4 | the hedgehog solves the exact ODE; `r`, `r^-2` are the only homogeneous modes | 0 |
| K5 | the two-scale error `eps_bg(r)`, and the breakdown radius | `0.11` at 1 pc; `r* = 2.09 pc` |
| K6 | the linearised operator: only `m_L`, `m_T` survive (symbolic + FD) | 0 ; `1.7e-8` |
| K7 | the closed-form profile solves the massive equation; `dI/dx = f` | 0, 0 |
| K8 | independent BVP reproduces it; the full nonlinear solve moves it by | `2.3e-10` ; `8.8e-7` |
| K9 | `u_sun/u_gal` and its spread over 1 AU–1 pc | `4.57e-6`, factor 1.06 |
| K10 | the three crossovers; **no** u-crossover | `6.97e3 AU`, `9.66e3 AU` |
| K11 | gradient balance residual; the cost of `u = a0` | `8.5e-9` ; `3.9e5 g_sun` |
| K12 | `alpha_1(1 AU)` by three routes | `1.6323e-13` |
| K13 | embedded vs isolated `alpha_1` | `4.9e-8` rel. |
| K14 | A36's K11 reproduced and diagnosed | `5.44e-14` → `1.63e-13`, x3 |
| K15 | the gate margin; the `1e-4` crossing radius | `6.13e8` ; `0.12 pc` |
| K16 | A22's `a_P` unchanged by the embedding | `1.4e-7` rel. |
| K17 | Pioneer: ratios and residual comparison | `2.8e-7` ; `9e10`–`1.8e11` |
| K18 | the slaved branch is inaccessible at 20–70 AU | `1.1e9` |
| K19 | the cap: `u_total/a0` | `0.5661` |
| K20 | the verdict, assembled | established ; survives |

Mutation (`--mutate`), each breaking at least one check and exiting 1: `flat_background` (K3, K9, K10,
K20), `slaved_sun` (K9, K10, K20), `eps_r_only` (K5), `alpha1_k0` (K12, K20), `alpha1_prefactor2`
(K12, K20), `pioneer_visible` (K17, K20). Records in `MUTATE.md`.

**Cross-checks against the source lanes** (read-only): A22's `a22_checks.py` 13/13 PASS at read time;
its K7 (`alpha_1` measure `8.16e-14` at 1 AU) is A22's convention, half of the exact `4(r/L*)^2`, and
its K13 verifies the hedgehog + charge-potential chain by FFT — the same chain used here. A36's
`a36_checks.py` 13/13 PASS; its K11 is reproduced to five digits and its K12 mismatch is the
`eps_2` of this lane.

---

## 8. Next

1. **The 2-D anisotropic solve.** Replace the isotropic mass by `m_L`/`m_T` on a `(r, theta)` grid;
   expected to move the 1 pc numbers by 3 % and nothing at 1 AU, but it is the one approximation left
   in the inner problem.
2. **A real galactic field.** Use a barred MW potential evaluated at the Sun; the dipole's orientation
   and the tidal term are the only changes.
3. **The moving Sun.** `dPbar/dt` from the Sun's orbit. The adiabatic argument is comfortable (the
   field responds on `ell/c ~ 30 yr`, the orbit is 40 Myr), but the size of the induced `E_i` needs
   the `E^2` normalization fixed first: with `P_i` in `kg/m^2`, `E_i = Pdot_i/N` has units
   `kg/(m^2 s)` and `eta E^2` is not an energy density unless `eta` carries an extra `c^-2`-like
   factor. The printed action does not fix this, and it is not needed for the static results above.
4. **The Oort-cloud boundary.** `alpha_1 = 1e-4` at 0.12 pc and `1` at 14.6 pc is a prediction for
   the outer Oort cloud, where no ranging exists. It is also the theory's cleanest statement that it
   is not a PPN theory.