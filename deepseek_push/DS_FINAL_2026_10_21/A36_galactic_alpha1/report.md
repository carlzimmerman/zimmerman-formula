# A36 — the galactic-regime `alpha_1`

**Lane:** A36_galactic_alpha1 · **Date:** 2026-10-21 · **Base:** `DS_FINAL_2026_10_21/BRIEF.md`,
`FINAL_THEORY.md` §3, `A22_ppn_frames/report.md`, `A12_slip_theorem/report.md`
**Script:** `a36_checks.py` (13/13 PASS, exit 0) · **Output:** `a36.out` · **Data:** `a36_results.json`
**Action:** the frozen round-2 ADM action, verbatim; `c = 1`, signature `(-+++)`, `K = 4 pi G`.

## Claim

For `r >> lambda = L*/sqrt2 = 16.97 pc` the P field is **MOND-slaved**: `|P| = u/K` with
`u = a0 g/(g+a0) ~ a0`, and the background carries a nonzero `Pbar(r)` whose direction is the
baryonic field's. On that background the preferred-frame parameter is **not zero**:

> **`alpha_1(r) = 4 u' / (D - u')`, with `u' = du/dg = a0^2/(g+a0)^2`,
> `D = 1 + (k L*)^2 u'/2`, and `alpha_2 = 0`.**

Evaluated on a Milky-Way-like baryonic field, `r = 1 ... 30 kpc`:

| `r` (kpc) | 1 | 2 | 3 | 5 | 8 | 12 | 20 | 30 |
|---|---|---|---|---|---|---|---|---|
| `g/a0` | 6.45 | 4.39 | 3.25 | 2.07 | 1.30 | 0.86 | 0.50 | 0.33 |
| `u/a0` | 0.866 | 0.814 | 0.765 | 0.674 | 0.566 | 0.462 | 0.335 | 0.248 |
| `u'` | 0.0180 | 0.0344 | 0.0554 | 0.1060 | 0.1883 | 0.2892 | 0.4420 | 0.5650 |
| **`alpha_1` (a)** | **0.073** | **0.143** | **0.235** | **0.475** | **0.928** | **1.628** | **3.169** | **5.194** |
| `alpha_1` (b) | 0.537 | 0.742 | 0.942 | 1.303 | 1.736 | 2.151 | 2.659 | 3.007 |
| `alpha_1` (c) | 0.046 | 0.068 | 0.091 | 0.142 | 0.219 | 0.316 | 0.477 | 0.629 |

Three independent routes — (a) linear response to a test source, (b) `4 x` phantom share,
(c) the galaxy as its own source — span **0.046 to 5.2**. Every entry is `2.66` to `4.72`
decades above `|alpha_1| < 1e-4`. **The galactic-regime `alpha_1` is O(1), not `< 1e-4`.**

The mechanism is the operator A22 identified as the residual frame dependence and then dropped:
the clock `P^i D_i ln N`. It carries **no** `N^i`, so it cannot mix `g_0i` with `delta P_i`
directly — but its source is the foliation lapse, which carries `w^2(Phi+Psi)` identically. At
galactic radii the P charge **is** a finite fraction of the baryonic density, so a `(1+2w^2)`
rescaling of that charge rescales the `1/r` potential: `alpha_1 != 0`. In the hedgehog regime the
charge is `GM/(gamma r)`, whose potential is *linear* in `r`, and A22's zero is recovered as the
`k L* -> infinity` limit (`alpha_1 -> 8/(k L*)^2`).

**Status: `NO-GO(exclusion)`** — the gate does not close, and the framework's structural claim
`alpha_1 = alpha_2 = 0` is false in the MOND regime. Scope and the one caveat that matters are
in §5 and §6; they do not move the number.

## 1. The quadratic action about the galactic background (task 1)

Background (static, spherical, `c = 1`): `Nbar`, `hbar_ij = fbar delta_ij`, `Pbar_i` with
`u = K|Pbar|`, `K W'(u) = g = |D ln Nbar|`, hence `u = a0 g/(g+a0)`, `Phat = ghat`,
`|Pbar| = u/K`. Perturbations: `N = Nbar(1+phi)`, shift `N^i`, `h_ij = hbar_ij + delta h_ij`,
`P_i = Pbar_i + pi_i`. To quadratic order, keeping the shift,

```
L2 = [EH quadratic] + (1/4K)[K_ij K^ij - (1+beta) theta^2]_2
   + pi^i D_i ln Nbar + Pbar^i D_i phi - (1/2) K^2 W'' (Phat.pi)^2
   - (1/2)(K W'/p)|pi_perp|^2 + (eta/2) E_i E^i
   - (gamma/2)(D.pi)^2 - (gamma/4) F_ij F^ij,     E_i = (d_t P_i - N^j D_j P_i - P_j D_i N^j)/N.
```

**Operator inventory (K1, exact).** Which operators mix `h_0i` (i.e. `N^i`) with `delta P_i`, and
which can produce an `O(w^2 eps)` source at all:

| operator | contains `N^i`? | `N^i x delta P_i` mixing | `O(w^2 eps)` piece |
|---|---|---|---|
| clock `P^i D_i ln N` | **no** | no | **yes**: `w^2 Pbar.grad(Phi+Psi)` |
| `W(u)` via `h^{ij}` | **no** | no | only a `Phi` tadpole (no `1/r`) |
| `(eta/2) E_iE^i` | **yes** | **yes**, coeff. `eta d_j Pbar_i d_t Pbar^i` | no: `E = 0` statically, so `E^2 = O(w^2 eps^2)` |
| `-(gamma/2)(D.P)^2` | **no** | no | no |
| `-(gamma/4) F_ijF^ij` | **no** | no | no |
| gravity `theta^2`, `K_ijK^ij` | yes | no (no `pi`) | no: `theta = O(w eps)` |

**Exactly one** operator mixes the shift with `delta P_i` (`E^2`), and it is *not* the one that
produces `alpha_1`: statically `E_i = 0` at O(1), so its mixing enters only at `O(w^2 eps^2)`.
`(D.P)^2` has no `N^i`; `W`'s `h^{ij}` dependence gives the anisotropic stress `prop Pbar_iPbar_j`
and the `pi`-mass, but no shift coupling. The operator that does the work is the clock — through
its **source**, not through a shift mixing.

## 2. `alpha_1` from the definition (task 2)

### 2.1 The kinematic identity (exact, K2)

Source at rest, foliation moving at `-w`: `T = t + w.x`, so `N` is the foliation lapse
`N = (-g^{mu nu} d_mu T d_nu T)^{-1/2}`. Expanding the exact expression to `O(eps)` and `O(w^2)`:

```
ln N = Phi - w.B + w^2 (1/2 + Phi + Psi) + O(eps^2),      residual exactly 0 (K2).     (2.1)
```

With `Psi = Phi` (A12's slip theorem) this is a **uniform rescaling of the lapse gradient**:

```
D_i ln N = (1 + 2 w^2) D_i Phi + O(w^2 eps^2).                                       (2.2)
```

This is A22's own `K6` (`ln N_T = Phi + w.B + w^2(Phi+Psi)`), re-derived from the exact lapse, not
a new assumption. `K3` shows the only other `O(w^2)` correction to the clock,
`h^{ij}P_j = ... + w^i (w.Pbar)`, multiplies `grad(Phi)` by a *constant* `(w.Pbar)` and is a total
derivative in the action. `grad(Pbar)` enters only at `O(L*/r) ~ 1e-3`; the leading formula is local.

### 2.2 The charge response (K4, K5)

The clock source `S = Pbar.D ln N` is therefore `S0(1+2w^2)`: **the P equation's source is
multiplied by `(1+2w^2)`.** Linearising about `Pbar` (`Phat = z`, `m_L = K^2W''`, `m_T = KW'/p`,
`delta psi = i k.pi`):

```
A = k_i G_ij k_j = k_perp^2/(m_T + gamma k^2) + k_z^2/(m_L + gamma k^2),
delta psi = - A (delta Phi + 2 w^2 delta Phi).                                       (2.3)
```

The lapse equation at `O(eps)` is A22's exact `lap^2 Psi = K(psi+rho)`, i.e.
`-k^2 delta Phi = K(delta rho + delta psi)`; nothing is added at `O(w^2 eps)`, because every other
P operator is either `O(w^2 eps^2)` (`E^2`, `theta^2`) or a `Phi`-tadpole without a `1/r` (`W`).
Solving, and using `g_00 = -1-2Phi`:

```
delta Phi(w^2)/delta Phi(0) = 2 A K/(k^2 - A K) = 2 u'/(D - u'),
D = 1 + (k L*)^2 u'/2,   u' = 1/(K W'') = a0^2/(g+a0)^2,                             (2.4)
alpha_1 = 2 delta Phi/(w^2 Phi) = 4 u'/(D - u'),        alpha_2 = 0.                  (2.5)
```

`K5` verifies (2.4) symbolically (residual 0) with `gamma = K L*^2/2`. The factor 4 is `2 x 2`:
one 2 from the `(1+2w^2)` source rescaling, one 2 from `g_00 = -1-2Phi`. `alpha_2 = 0` because `w`
enters only as `|w|^2`; the anisotropy in (2.3) is in `k.Pbar` (the external field), not in `w`.

### 2.3 Why A22 got zero, and where the zero stops

A22's `D5-D6` is exactly (2.1)-(2.3): "the rescaling multiplies the charge,
`psi(w) = (1+2w^2) psi_0`". Their zero comes from the next step: in the hedgehog regime
`psi = GM/(gamma r)`, so its potential is **linear** in `r` (`Phi_c = (GM/L*^2) r`), and rescaling
a linear potential gives a `w^2 r` term — not a `w^2 U` term. In the MOND regime the charge is
instead a finite fraction of the baryonic density (`div P = rho - rhobar`, BRIEF §1), so its
potential **is** the `1/r` potential and the same rescaling gives `w^2 U` with an O(1) coefficient.
The transition is the `k L*` factor in `D`: `alpha_1 -> 8/(k L*)^2` for `k L* >> 1` (`K7`, A22's
zero) and `alpha_1 -> 4u'/(1-u')` for `k L* -> 0` (a galaxy).

## 3. Numbers on a Milky-Way background (task 3)

Model: `M_bar = 6e10 Msun`, Hernquist `a = 3 kpc`; `g_N = G M(<r)/r^2`, then the framework's law
`g = (g_N/2)(1+sqrt(1+4a0/g_N))`, `u = g - g_N`, `u' = a0^2/(g+a0)^2`; `a0 = 9.36e-11 m/s^2`,
`L* = 24 pc`, `lambda = 16.97 pc`.

| `r` (kpc) | `g_N` | `g` | `g/a0` | `u/a0` | `u'` | `alpha_1`(a) | `alpha_1`(b) | `alpha_1`(c) | `/1e-4` (a) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 5.23e-10 | 6.04e-10 | 6.45 | 0.866 | 0.0180 | 0.073 | 0.537 | 0.046 | 734 |
| 2 | 3.35e-10 | 4.11e-10 | 4.39 | 0.814 | 0.0344 | 0.143 | 0.742 | 0.068 | 1426 |
| 3 | 2.32e-10 | 3.04e-10 | 3.25 | 0.765 | 0.0554 | 0.235 | 0.942 | 0.091 | 2348 |
| 5 | 1.31e-10 | 1.94e-10 | 2.07 | 0.674 | 0.1060 | 0.475 | 1.303 | 0.142 | 4745 |
| 8 | 6.91e-11 | 1.22e-10 | 1.30 | 0.566 | 0.1883 | 0.928 | 1.736 | 0.219 | 9277 |
| 12 | 3.72e-11 | 8.04e-11 | 0.86 | 0.462 | 0.2892 | 1.628 | 2.151 | 0.316 | 16278 |
| 20 | 1.58e-11 | 4.72e-11 | 0.50 | 0.335 | 0.4420 | 3.169 | 2.659 | 0.477 | 31689 |
| 30 | 7.68e-12 | 3.09e-11 | 0.33 | 0.248 | 0.5650 | 5.194 | 3.007 | 0.629 | 51945 |

**(a)** is (2.5), the linear response to a test source (the task's definition: the coefficient of
the `w^2 U` term after the constraint is solved). **(b)** is the independent share argument
`alpha_1 = 4 f_ph`, `f_ph = u/g` — no derivative of `u`, no `k`-response; agrees with (a) to within
a factor 7.3 (`K14`). **(c)** is the galaxy as its own source: the boost multiplies `g` by
`(1+2w^2)`, so `u -> u + 2w^2 g u'`, the charge becomes `psi + 2w^2 (1/K)(1/r^2) d_r(r^2 g u')`,
and the lapse equation integrates once to `d(delta Phi)/dr = 2 w^2 g u'`, i.e.
`alpha_1(r) = 4 <u'>_g` (`g`-weighted mean). Route (c) has `grad Pbar` exactly, needs no local
approximation, and is the most conservative of the three.

The spread `0.046 ... 5.2` is the honest O(1) uncertainty. The floor of all three routes is
`0.046` at 1 kpc; the one-parameter estimate `4u'` alone is `0.072` at 1 kpc (`K10`). Nothing in
the galactic range approaches `1e-4`.

**Solar system (`K11`).** For an AU-scale source the hedgehog branch gives
`u' = r^2/(2 lambda^2)`, `D - u' = 1.5`, hence `alpha_1(1 AU) = 5.44e-14` — A22's zero is
recovered as the short-wavelength limit. The formula is the same; only `k L*` differs.

---

## 4. THE DECISION (task 4)

> **`|alpha_1| = 0.046` to `5.19` over `r = 1 ... 30 kpc`, i.e. O(1) everywhere in the galactic
> regime. It exceeds `|alpha_1| < 1e-4` by `2.66` to `4.72` orders of magnitude. Under the
> criterion set for this lane, the theory is EXCLUDED.**
>
> Largest controlled value (`u' <= 0.19`): `alpha_1 = 0.93` at 8 kpc; largest reported: `5.19` at
> 30 kpc (extrapolated). Smallest: `0.046` at 1 kpc — still `460x` the bound.

The exclusion does **not** rest on a marginal number, a coefficient choice, or a sign, but on a
structural fact: at galactic radii the P charge is a finite fraction of the baryonic density, so
the `(1+2w^2)` rescaling of the clock source — exact, and already in A22's `K6`/`D5` — rescales a
`1/r` potential. No coefficient in `[0.046, 5.2]` is `< 1e-4`, and no route gives less without
contradicting `div P = rho - rhobar`.

**What the exclusion is and is not (stated, not softened).** The `|alpha_1| < 1e-4` bound is
measured in the solar system, and the solar-system value of this same formula is `5.4e-14`: LLR
itself does not see the effect. What is excluded is the framework's *claim*, repeated in
`FINAL_THEORY.md` §3/§8 and in A22's status line, that `alpha_1 = alpha_2 = 0` is a structural
property of the theory. It is not: `alpha_1` is **scale-dependent**, varying by 13 orders of
magnitude between an AU-scale source and a kpc-scale one. A "PPN parameter" with that behaviour is
not a PPN parameter, and the theory has no PPN limit in the MOND regime — the regime that is its
whole observational case. That is the failure, and it is not repairable by tuning: `alpha_1` is
fixed by `u(g)` and by the `(1+2w^2)` identity, neither of which is free.

---

## 5. Status

**`NO-GO(exclusion)`** for the gate. `CLOSED-DERIVED` for the two ingredients that carry it: (2.1)
(the lapse's `w^2(Phi+Psi)`, exact) and (2.3)-(2.5) (the constrained response, exact in the slaved
gradient expansion at galactic scales, `(kL*)^2u'/2 <= 5.2e-6`, K13).
`CONDITIONAL` on one approximation: the coefficient uses the linearised response about a locally
uniform background, so its O(1) value carries the three-route spread (a factor 7 at worst); every
route is `> 460x` the bound, so the verdict is invariant.

## 6. What this does not do

- **Not a full nonlinear PPN computation.** The `O(w^2 eps)` analysis is complete for the operators
  in the action (K1), but the coupled metric + khronon + P system is not solved nonlinearly at
  `O(w^2)`. The khronon perturbation does not appear in the `O(w^2 eps)` source list; if it
  entered, it would enter at the same `(1+2w^2)` order — the coefficient could move, not the order.
- **The deep-MOND end is an extrapolation.** (2.5) has a `1/(1-u')` denominator; for `u' > 0.3`
  (`r >~ 12 kpc`) the linear response is uncontrolled and the 20-30 kpc entries should be read as
  "`> 1`". The 1-8 kpc entries (`u' <= 0.19`) are controlled.
- **`grad Pbar` is only partly included.** Route (c) has it exactly (spherical `Phat = rhat`);
  routes (a)/(b) are local. The `O(L*/r) <= 3e-3` corrections cannot move the answer.
- **The solar-system P configuration is not established (K12, an independent problem).** A22's
  hedgehog is the *isolated* Sun (`u = 2.59e-6 a0`); the galactic field at the Sun is `u = 0.566 a0`,
  a factor `2.19e5` larger. A static, divergence-free, cap-respecting P field following the Sun's
  radial direction would need `2 gamma u/(K r^2)`, which at 1 AU with `u ~ a0` is `~2e3 m/s^2`
  against `g_sun = 5.9e-3 m/s^2`. So A22's zero is an isolated-source statement, not one about the
  real solar system. The galactic numbers above use the galactic solution and are unaffected.
- **`L*` and `a0` are inputs.** `u'` depends on `a0` and `g`, `D` on `L*`. `L*` enters only the
  `k L*` crossover (negligible in the galactic range); the alt footing `1.13e-10` shifts `u'` by `O(20 %)`
  and leaves the verdict unchanged.

## 7. Checks (`a36_checks.py`, 13/13 PASS, exit 0)

K1 operator inventory (1 of 5 mixes `N^i` with `pi`: `E^2` only) · K2 `ln N` residual 0 ·
K3 `w^i(w.Pbar)` residual [0,0,0] · K4 propagator exact · K5 `2u'/(D-u')` residual 0 ·
K6 `S = 0` · K7 limits `0, 0, 4u'/(1-u')` · K8 min `|alpha_1| = 0.0734` (1 kpc) ·
K9 max `5.194` (30 kpc) · K10 conservative `4u' = 0.0720` · K11 `alpha_1(1 AU) = 5.44e-14` ·
K12 mismatch `2.19e5` · K13 `(kL*)^2u'/2 <= 5.2e-6` · K14 ratio in [0.58, 7.32].

Mutation (`--mutate`): dropping the `(1+2w^2)` rescaling of the clock source makes `alpha_1 = 0`
and breaks K7, K8, K9 — the check has teeth (`MUTATE.md`).

## 8. Next

1. **Nonlinear `O(w^2)` solve** of the coupled (metric, khronon, P) system on the spherical galactic
   solution, to replace the three-route bracket by one number — the only way the coefficient moves,
   and it cannot move it below `1e-4`.
2. **The solar-system P configuration.** Solve the static P equation for the Sun inside the galactic
   field (`g_gal = 1.30 a0` at 8 kpc); if no regular solution exists, the framework has no
   solar-system sector at all, independent of `alpha_1`.
3. **Observational consequence.** `alpha_1 ~ 0.05-0.6` at galactic scales predicts a CMB-frame
   modulation of galaxy MOND fields at the `alpha_1 v^2/c^2 ~ 2e-7` to `3e-6` level (with
   `v = 369 km/s`), below any present measurement. The theory therefore dies here by principle,
   not by data — a distinction that must be stated wherever the framework quotes "`alpha_1 = 0`".
