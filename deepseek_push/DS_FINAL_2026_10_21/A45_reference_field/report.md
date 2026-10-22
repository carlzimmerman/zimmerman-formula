# A45 — WHAT IS `g_N` IN COSMOLOGY? The reference-field fork, decided at the P equation

**Lane:** A45_reference_field · **Date:** 2026-10-21 · **Base:** `A33_master_action/MASTER_ACTION.md`
(eq. P), `A22_ppn_frames/report.md` (D4, D8), `A40_growth/report.md` (the fork), `THEORY.md`.
**Script:** `a45_checks.py` (25/25 PASS, exit 0, <40 s) · **Output:** `a45.out` · **Data:** `a45_results.json`
· **Mutations:** 5, each exit 1, in `MUTATE.md`.

## Claim

Go back to the P equation and linearise it about FRW + a scalar perturbation. Three things follow, and they
decide the fork.

1. **The coefficient on `grad(delta Phi)` is exactly 1/K.** For a pure-gradient mode the two gradient
   operators of (P) — the `-(gamma/2)(D_iP^i)^2` and `-(gamma/4)F_ijF^ij` terms — cancel identically into
   a single `gamma lap^2(delta P_i)` (K5). The P sector is therefore an **elliptic constraint**, not a
   propagating field, with stiffness `gamma = K L*^2/2`; the linear response is
   `delta P_i = (1/K) d_i(delta Phi) / (1 + (k lambda_P)^2)` with `lambda_P = L*/sqrt2 = 17.0 pc`.
   At `k = 0.1 h/Mpc`, `(k lambda_P)^2 = 1.31e-12` and the kinetic term is `(eta/K)H^2 = 1.5e-17`: **the
   coefficient is 1 to twelve digits.**
2. **The charge it carries is a copy of the Poisson source, not an independent one.** `delta d = D.delta P =
   lap^2(delta Phi)/K`, so eliminating `psi = d` between A22's exact linearised system (4)+(6) gives
   `Phi = -K rho (K + gamma k^2)/(gamma k^4)`, i.e. **`G_eff/G = 1 + 1/(k lambda_P)^2 = 7.6e11`** at
   0.1 h/Mpc — a `k^-4` runaway. **The linear order of the action has no finite solution.** This is the
   "zero-field `k^2` runaway" A40 cites (FP22 B0–B4), now with its coefficient.
3. **The reason is algebraic and does not depend on the perturbation.** In the variable `u = K|P|` the law is
   `g_N = u^2/(a_0(1-u/a_0))` — **quadratic** in the P field (K3), with `nu = a_0/u` (K2) and a **square-root**
   inverse `u = sqrt(a_0 g_N)` (K4). There is no regime in which the response is `1 + O(field)`: at high field
   it is `1 + (a_0/g_N)^2`, at low field `sqrt(a_0/g_N)`; the two ends do not meet in a linear term. So the
   modification is **inert at linear order** in the only operational sense — it admits no linear field — and
   its first nonzero effect is `O(g_N/a_0) = 0.21 %` at the 8 h⁻¹ Mpc peak, i.e. second order in `delta` (K9b).

Consequently **neither branch of A40's fork is a linearisation of the action.** Branch (b) is the *resummation*
of the exact law (the `sqrt` branch) applied where the law's derivation does not hold, and it is excluded
(`sigma8 = 2.267`, 2.8× the observed amplitude, ×8868 clusters at 10¹⁵ M☉). Branch (a) is a posit: **no term of
A33 §1 contains an `H`** — `cH` is a background quantity, not an operand the action names — so `g_ref = cH` is imported, and it happens to land on the right answer to 0.2 %
for a reason that has nothing to do with `cH` (see §5). What survives is the filtered/environmental reading,
whose filter scale **does not exist in the linear field** (max `g_R = 0.0021 a_0`, shortfall 479×) and is
`R(a_0) = 2 sigma^2/a_0 = 1.4–52 kpc` in the nonlinear field, i.e. `k(a_0) = 29–1037 h/Mpc` — two to four
decades above every linear scale. Hence: **growth is GR on the theory's own background, `sigma8 = 0.760`,
`f sigma8` ΛCDM-shaped**, `chi^2 = 14.78/8` against `7.34/8` for the ΛCDM control. The theory has a growth
prediction, and it is a *background* prediction (`f(0) = 0.452` vs `0.528`), not an `a_0` prediction. The
`delta_c` that would fake Planck's `sigma8` is **0.677**, a factor 2.5 below the collapse threshold — so the
"bound systems only" reading is consistent with the data but cannot produce 0.832 without a tuned threshold
in the quasi-linear regime.

## 1. The algebra: the law is quadratic, and its inverse is a square root

`c = 1`; `K = 4 pi G`; `W(u) = (a_0^2/K)[-u/a_0 - ln(1-u/a_0)]`; `g = KW'(u) = u/(1-u/a_0)`;
`g_N = g - u` (A33 §5's first integral). Eliminating `u`:

```
g_N = g^2/(g+a_0) = u^2/(a_0(1-u/a_0)),      nu = g/g_N = a_0/u                        (1)
g_N = u^2/a_0 + u^3/a_0^2 + ...   (dg_N/du|_0 = 0,  d^2g_N/du^2|_0 = 2/a_0)             (2)
u   = [sqrt(g_N)sqrt(4a_0+g_N) - g_N]/2 = sqrt(a_0 g_N) (1 - sqrt(g_N/a_0)/2 + ...)      (3)
```

(K1–K4, sympy exact.) Eq. (2) is the fact the record has not used: **a first-order perturbation of P produces
a second-order `g_N`.** The consequence is stronger than "the effect is small": at the order where linear
growth is defined, the modification **is absent**. Eq. (3) is the other face of it: the inverse is a Puiseux
series in `g_N^{1/2}`, so `nu = sqrt(a_0/g_N)` has a branch point at zero field and no Taylor expansion
exists. `nu` runs from 1 at infinite field to ∞ at zero field with no linear term at either end:

```
high field (eps = a0/g_N):   dg/dg_N = 1 + eps^2 + O(eps^3)     [A40 K6]
low  field (eps = g_N/a0):   nu      = eps^{-1/2}(1 + ...)      [a square root]
```

## 2. The P equation at linear order (task 1)

FRW (`N = 1`, `N^i = 0`, `h_ij = a^2 delta_ij`, `P = 0`) plus `N = 1 + Phi`, `h_ij = a^2(1-2Psi)delta_ij`,
`P_i = delta P_i`. The linearised (P) is, term by term,

```
d_i(delta Phi)                                     [clock: D_i ln N at O(delta)]
+ gamma[ d_i(D.delta P) + lap^2(delta P_i) - d_i(D.delta P) ]   [(D.P)^2 + F^2]
+ eta(d_t^2 + 3H d_t) delta P_i                    [kinetic, E_i = d_t delta P_i at P = 0]
= K delta P_i                                      [mass: KW'(u)/u -> 1, times the K of u = K|P|]
```

**K5:** the two gradient brackets cancel *identically* for a gradient mode (`F_ij = 0`), leaving
`gamma lap^2(delta P_i)`. This is the term A33 §7.4 records as mis-transcribed in A3, and here it is
load-bearing: it is why the P sector is a constraint rather than a propagating scalar.
**K6:** in Fourier, `delta P_i = d_i(delta Phi) * K/(K + gamma k^2)`, so

> **the coefficient multiplying `grad(delta Phi)` is `1/K`, i.e. 1 in the action's `K = 1` units, with a
> relative correction `(k lambda_P)^2 = 1.31e-12` at `k = 0.1 h/Mpc` (and `1.5e-17` from the kinetic term).**

**K7:** the charge `delta d = -k^2 Phi/(K + gamma k^2)` is a copy of the Poisson source with coefficient
`1/K`. Substituting into the lapse equation (A22 (4), `lap^2 Psi = K(psi + rho)`) and using `Phi = Psi`
(no anisotropic stress, A22 F2):

```
-k^2 Phi = K rho - K k^2 Phi/(K + gamma k^2)   =>   Phi = -K rho (K + gamma k^2)/(gamma k^4)
G_eff/G = (-k^2 Phi)/(K rho) = 1 + K/(gamma k^2) = 1 + 1/(k lambda_P)^2                  (4)
```

At `k = 0.1 h/Mpc` that is **7.6e11**; at 0.2 h/Mpc, 1.9e11. The potential runs away as `k^-4`. **The
linearised system is not a truncation of any solution** — the same conclusion A22's (7)
(`lap^2 psi = -(K/gamma) rho`, exact) implies once `gamma k^2/K -> 0`. The result is robust to the one
approximation made: if the Hubble-drag term in the lapse equation breaks the cancellation, the residual is
`O(H^2/k^2) = 1.5e-5` at 0.1 h/Mpc and `G_eff/G ~ 7e4` instead of `∞` — still not a growth equation, and
still five orders above anything that could be mistaken for a 1 % effect.

**K8:** equivalently, `u/g = 1 - (k lambda_P)^2` and `g_N/g = (k lambda_P)^2`: the linearised P sector sits
*at the deep-MOND endpoint*, not near GR. Combining `g_N = g(k lambda_P)^2` with the law
`g_N = u^2/a_0 ~ g^2/a_0` leaves exactly one admissible field, `g = a_0 (k lambda_P)^2 = 1.5e-22 m/s^2` —
zero. That is the "zero field" in the record's name for this failure.

**K9:** and the linear solution is not the `delta -> 0` limit of the exact solution. The exact small-source
solution has `u = sqrt(a_0 g_N)`, which at the 8 h⁻¹ Mpc field (`g_N = 0.0020 a_0`) is **22.5× the
Newtonian field** and scales as `delta^{1/2}`, not `delta`. The two branches are separated by a singular map
at `delta = 0`; "the modification is a small perturbation of GR" is not a statement this action can make.

**K9b (the size of the first nonzero effect).** Because `g_N = u^2/a_0 + ...`, the P sector's contribution to
the potential is second order, `(grad delta Phi)^2/a_0`, i.e. a fraction `g_N/a_0 = 0.21 %` of the first-order
Newtonian field at the 8 h⁻¹ Mpc peak (0.18 % at 100 Mpc). That is the whole `a_0` imprint on linear growth:
below every quoted error bar (`Delta sigma8 < 0.2 %`).

**Convention, stated.** The printed (P) is dimensionally consistent only in units `K = 1` (its clock term
`P^i D_i ln N` is a density if `[P] = kg/m^2`, while the RHS `(KW'/u)P_i` then carries `[P]`); A33's K1/K2
variations are done in those units. Restoring `K`, the mass term is `K delta P_i` — the normalisation that
A22's `m^2 = K/eta` and `u = K|P|` being an acceleration both require — and the ratio `u/g = 1` that gives
(4) is independent of `K`. Nor does the divergence depend on the coefficient's value: any **nonzero** clock
coupling `c` gives `G_eff/G = 1 + c/(k lambda_P)^2 -> ∞`, and `c = 0` is not available — it would remove the
clock term and with it the law (A33 K5 derives the coefficient to be exactly 1). The defect is bookkeeping,
not structural, but it should be fixed before (P) is used at second order.

## 3. The three readings, and what each one is

Same law, same background, three closures. `sigma8` is `0.811 * D(1)/0.78856` (A40's anchor);
`G_eff/G` is at `z = 0`.

| reading | what `g_N` is | `G_eff/G` | `sigma8(0)` | `chi^2(f sigma8)/8` | status |
|---|---|---|---|---|---|
| **(a) cosmic `cH`** | the only background acceleration the theory has | 1.0140 | **0.7619** | 14.21 | **posit** — no `H` in the action |
| **(b) own rms field** | `(4 pi G/3) rho_m sigma8(z) R_8` | 11.75 | **2.267** | — | **excluded**, 2.8× in sigma8, ×8868 clusters |
| **inert / filtered** | nothing at linear order; the field where `u ~ a_0` | **1.0000** | **0.7602** | 14.78 | the action's linear order (§2) |

K11 and K12 reproduce A40's 0.7619 and 2.267 exactly, so the three numbers are on one integrator (K10 checks
it against the exact integral growing mode on *both* backgrounds: 0.788559 and 0.739201). The `chi^2` for
branch (a) is identical to A40's 14.21; my ΛCDM control is 7.34 where A40 quotes 7.85, a 0.5 difference from
their use of the branch-S shape for the control's `sigma8(z)` — the `Delta chi^2` is +7.4 here, +6.4 there.

**What (b) is, precisely.** It is not "the law linearised"; it is the exact law *resummed* and applied
pointwise to the perturbation's own field. K1–K9 show that this resummation is the only way to get a finite
`nu > 1` out of the algebra, and that it is the wrong branch for a linear mode: it requires `u = sqrt(a_0 g_N)`,
which is 22× the Newtonian field. So (b) is a statement about what happens if the law is applied where it was
not derived — and the data say no.

**What (a) is, precisely.** `cH(z)` is `6.6 a_0` at `z = 0`, so `G_eff/G = 1.014`: a 1.4 % scale-free boost.
It gives the right `sigma8` because the *background* already suppresses growth by 6 %, not because `cH` is the
right operand. Nothing in the action singles out `cH`; the coincidence is that any reference field of order
`a_0`–`10 a_0` gives `G_eff` within a few per cent of 1.

## 4. Task 2 — the bound-system reading, and the `delta_c` it needs

The law is a **static-spherical first integral**: A33 §5 obtains it by differentiating (L) and substituting
(P-sph), with `g_N = GM_src/r^2` and the asymptotically flat boundary condition `u -> 0`, `g -> g_N`. Its
hypotheses are static, spherical, isolated, and `u ~ a_0`. A linear cosmological perturbation satisfies none
of them: it is not static, not spherical, not isolated, and its field is `0.002 a_0`. That is the physical
argument for inertness, and it is independent of §2's algebra — the two agree.

Made quantitative: `G_eff = 1` while `delta_8(a) < delta_c`, and the full pointwise response
`RESP(g_8/a_0)` above it, with `g_8 = (1/2) Omega_m H^2 delta_8 R_8` (the 8 h⁻¹ Mpc sphere). The ODE is then
nonlinear; `sigma8` is its fixed point.

| `delta_c` | 0 | 0.2 | 0.4 | 0.6 | 0.8 | 1.0 | 1.686 | 4.0 |
|---|---|---|---|---|---|---|---|---|
| `sigma8(0)` | 3.346 | 2.618 | 1.665 | 0.988 | 0.7602 | 0.7602 | **0.7602** | 0.7602 |

**`delta_c(sigma8 = 0.832) = 0.677`** (K14, K15). Compare:

* `delta = 0.76` — what the 8 h⁻¹ Mpc sphere actually reaches at `z = 0`;
* `delta = 1` — the nonlinear scale;
* `delta = 1.686` — spherical collapse.

So the required threshold is **0.40 × the collapse threshold** and *below* the nonlinear scale. Two readings
of that number:

1. **The bound-system reading is consistent but empty.** At `delta_c = 1.686` the `sigma8` mode never crosses
   the threshold, `sigma8 = 0.7602` exactly (K16), 6.3 % below Planck. The reading says "the modification is
   a nonlinear-scale effect"; that is allowed, and it predicts nothing beyond the background.
2. **It cannot reach Planck without tuning.** To get 0.832 the modification must switch on at `delta ~ 0.7`,
   i.e. in the quasi-linear regime where there is no bound system yet and the static-spherical derivation does
   not apply. That is a one-parameter fit, not a prediction.

Note also that `delta_c -> 0` gives 3.346, *not* A40's 2.267: `RESP ~ delta^{-1/2}` diverges as `delta -> 0`
and the 8 h⁻¹ Mpc mode starts from zero. A40's 2.267 uses the nonzero rms field and is the finite member of
the same family.

## 5. Task 3 — the filtered field

`g_R = (1/2) Omega_m H^2 sigma(R) R` is the rms acceleration at the surface of a top-hat of radius `R`
(only the contrast sources `Phi` in cosmology; the mean is in the expansion). `sigma(R)` is EH98 no-wiggle,
`n_s = 0.965`, normalised to `sigma8 = 0.811`; its `k_NL = 0.224 h/Mpc` is the standard Planck value, which
calibrates the shape (K17).

**The filter scale does not exist in the linear field.** Over `R in [1 kpc, 10 Gpc]`,

```
max_R g_R = 2.36e-13 m/s^2 = 0.0021 a_0   at R = 21.5 Mpc        (K18)
```

— a **shortfall of 479×**, and the function is almost flat past the turnover (`sigma(R) R` is nearly
scale-invariant), so there is no `R` anywhere in the linear universe at which "the mean smoothed field equals
`a_0`". **`a_0` is not a cosmic acceleration.**

Two consequences, and they are the substance of task 3:

* **If one forces the filter on the linear field anyway**, `G_eff/G` runs over `11.5–291` for
  `R in [1 kpc, 10 Gpc]` (K19) and the growth is branch (b): `sigma8 = 2.267`. Smoothing a linear mode does
  not reduce its field — a 15 kpc filter applied to a 100 Mpc mode returns the mode's own field — so **the
  filter changes nothing at linear scales.** This kills the naive "environmental rescue" of linear growth.
* **The only place the smoothed field reaches `a_0` is inside haloes.** `R(a_0) = 2 sigma^2/a_0` for an
  isothermal profile: **1.4 kpc (50 km/s), 5.7 kpc (100), 12.9 kpc (150), 22.9 kpc (200), 51.5 kpc (300)**
  (K20), i.e. `k(a_0) = 29–1037 h/Mpc` — two to four decades above every linear scale (`k <~ 0.2 h/Mpc`).
  There the response at `a_0` is `RESP(1) = 1.174`, a 17 % boost — but that is the **RAR**, the internal
  dynamics of a galaxy, not growth.

This is exactly how the programme already uses the law: the PM engine `CFG960`'s `Law.mph` evaluates
`y = C_y M_b(<r)/r^2` at the local radius (`campaign_fresh_gravity/CFG960_sctm_engine/cfg960_sctm_pm.py`
L250–256) — an object-by-object, nonlinear smoothing, with no cosmic `R(a_0)` anywhere. The environmental
reading, implemented honestly, therefore **is** the inert reading.

**The filter alone is not enough, and that must be said.** K19 shows that evaluating the law at the smoothed
linear field gives `G_eff ~ 12`, not 1: smoothing a 100 Mpc mode at 13 kpc returns the mode's own
`0.002 a_0`. What gives inertness is the filter **together with** the law's domain of validity — the operand
`g_N` is defined only where there is a system whose field it is, i.e. inside a bound object. That is a mask,
and the mask is the part the action does not derive (see §6). With mask + filter:

**The answer task 3 asks for:** `G_eff = 1` on all linear scales, and

```
sigma8(0) = 0.7602          f sigma8:  z=0: 0.3438   z=0.5: 0.4186   z=1: 0.4023
                                      z=1.5: 0.3594  z=2: 0.3162
f(z)      = 0.4522, 0.6950, 0.8332, 0.9041, 0.9413       sigma8(z) = 0.760, 0.602, 0.483, 0.398, 0.336
```

`chi^2(f sigma8) = 14.78/8` vs `7.34/8` for the ΛCDM control (Δχ² = +7.4 at equal parameters, all pulls but
one negative: the theory grows too slowly). `S8 = sigma8 sqrt(Omega_m/0.3) = 0.7806` with the Lagrangian
`Omega_m = 0.3163` (KiDS-1000 0.759 ± 0.021 → +1.03σ; Planck 0.832 → −3.9σ).

## 6. Verdict

**The action does not support a linear modification, and that is a derivation, not a failure to find one.**

* `delta P_i = (1/K) d_i(delta Phi)` with coefficient 1 to `1e-12`; the charge it carries is a copy of the
  Poisson source; eliminating it gives `G_eff/G = 1 + 1/(k lambda_P)^2 -> ∞`, a `k^-4` runaway. This is
  A40's own caveat ("not a strict linearisation of the action; the strict system is degenerate and
  ill-posed") turned into an equation with a coefficient.
* The algebra explains it: `g_N = u^2/(a_0(1-u/a_0))` is quadratic in the P field and its inverse is a square
  root, so there is no linear term to perturb. The modification enters at second order, at `0.2 %` — and if
  resummed it is the `sqrt(a_0 g_N)` branch, which is 22× the Newtonian field and excluded.

**Which reading does the action support?** The one in which the law acts only where it was derived — in bound
systems, at the field's own `a_0` scale. That is the **filtered/environmental reading in its only consistent
form**: `R(a_0) = 1.4–52 kpc`, `k(a_0) = 29–1037 h/Mpc`, no linear effect. It is not a derivation *of the
filter* — nothing in A33 §1 selects `R(a_0)`, and that must be said plainly — but it is the unique completion
that survives both the action's own linear order and the data. Branch (a) is numerically right and has no
action-level origin; branch (b) is the resummed law and is excluded.

**What `sigma8` does it predict? `0.7602`** on the literal `beta = 0` background (`H(0) = 77.33 km/s/Mpc`,
`Omega_m(a=1) = 0.2403`), i.e. **6.3 % below Planck-2018's 0.811** and 0.22 % below A40's branch (a). On the
flat background the same calculation is ΛCDM to the digit (`sigma8 = 0.811`), so the *distinct* prediction is
the literal background's; the flat reading predicts nothing new.

**The discriminating observable.** Not `sigma8` — the amplitude is degenerate between (a), the inert and the
filtered readings (0.762 / 0.760 / 0.760) and the differences are inside Planck's own `Lambda`CDM-fit bar.
Three observables do discriminate, in order of sharpness:

1. **The scale dependence of growth at fixed `z`.** Branch (b) is *blue*: `G_eff(0.05 h/Mpc)/G_eff(0.2 h/Mpc)
   = 0.630` (60 % more boost on 5 h⁻¹ Mpc than on 20), so `f sigma8` and `P(k)` acquire a measurable tilt over
   `k = 0.05–0.3 h/Mpc`. The filtered and inert readings are **exactly scale-free** (ratio 1.000) — the `17 pc`
   stiffness is `1e-12` of any linear scale. A detection of any `k`-dependence in `f sigma8` at the ≥10 % level
   at one `z` decides the fork; a null at that level excludes (b) and confirms the rest. This is the one
   observation that separates *all three* readings at once, and it needs no new theory prior.
2. **The cluster mass function at `z ~ 1`.** `sigma8 = 2.267` vs `0.760` changes
   `exp(-delta_c^2/2sigma(M)^2)` at `10^15 M_sun` by a factor **8868** (K23). Cluster counts alone exclude (b)
   independently of any growth-rate measurement.
3. **The nonlinear step at `k ~ 1/R(a_0) = 30–1000 h/Mpc`.** The `a_0` response (17 % at `a_0`) is real but
   lives entirely inside haloes: it shows up in the *nonlinear* `P(k)`, in halo profiles, and in the
   environment-dependence of the RAR — not in `f sigma8`. A reading in which the modification acts at linear
   scales would put a step at `k ~ 0.01–0.1 h/Mpc` instead; the two are separated by three decades.

And the background, not `a_0`, is what makes the surviving prediction testable: `f(0) = 0.452` against
ΛCDM's `0.528` is a **14 %** difference, at DESI DR2's 1–2 % precision a 7–14σ discriminant with no free
parameters (K24).

## Status

**`DERIVED`:** the coefficient `1/K`; the exact cancellation of the gradient operators into `gamma lap^2`;
`G_eff/G = 1 + 1/(k lambda_P)^2`; `g_N = u^2/(a_0(1-u/a_0))` and the square-root inverse; `sigma8(b) = 2.267`
excluded; `delta_c(0.832) = 0.677`; `max_R g_R = 0.0021 a_0`; `R(a_0) = 1.4–52 kpc`.
**`CHOSEN (not derived)`:** the restriction of the law's domain to bound systems, i.e. the identification of
the filtered reading with "the modification lives at `k >~ 1/R(a_0)`". Nothing in the action forces it; what
the action does force is that **no** reading with a linear `G_eff > 1` is available, which is why the choice is
between a domain restriction and a `2.98×` `sigma8` failure.
**`NUMERICAL`:** `sigma8 = 0.7602`, the `f sigma8` table, `chi^2 = 14.78/8`, the threshold scan, the filter
scales.

## Checks (`a45_checks.py`, 25/25 PASS, exit 0, <40 s)

| id | what it proves | measured |
|---|---|---|
| K1 | `g_N = g^2/(g+a_0) = u^2/(a_0(1-u/a_0))` | residual `0`, `0` |
| K2 | `nu = g/g_N = a_0/u` exactly | residual `0` |
| K3 | **`g_N` has no linear term in `u`**: `dg_N/du|_0 = 0`, `d^2/du^2|_0 = 2/a_0` | `0`, `2/a_0`, series `u^2(a_0+u)/a_0^2` |
| K4 | the inverse is a square root: `u^2/(a_0 g_N) -> 1`, `nu' ~ g_N^{-1/2}` | Puiseux, no Taylor series |
| K5 | `(D.P)^2` + `F^2` = `gamma lap^2(dP_i)` for a gradient mode | `[0,0,0]` |
| K6 | **coefficient on `grad(delta Phi)` is 1/K to 1e-12** | `(k lambda_P)^2 = 1.31e-12`; `(eta/K)H^2 = 1.5e-17` |
| K7 | eliminating `psi` gives `G_eff/G = 1 + 1/(k lambda_P)^2` | `7.64e11` at 0.1 h/Mpc; `-> ∞` |
| K8 | the linear branch is the deep-MOND endpoint: `g_N/g = (k lambda_P)^2`, `g -> 1.5e-22 m/s^2` | `1.31e-12` |
| K9 | the linear solution is not the `delta -> 0` limit | `u_exact/u_lin = 22.5` |
| K9b | the first nonzero effect is second order, `O(g_N/a_0) = 0.21 %` | `0.0020` / `0.0018` |
| K10 | integrator = exact growing mode on both backgrounds | `0.788559`, `0.739201` |
| K11 | branch (a) `cH` reproduces A40 | `0.7619` |
| K12 | branch (b) rms reproduces A40 | `2.267`, `G_eff = 11.75` |
| K13 | adopted branch is `G_eff = 1` | `0.7602`, `f(0) = 0.45224` |
| K14 | threshold scan monotone, root exists | `delta_c(0.832) = 0.677` |
| K15 | **that `delta_c` is below the nonlinear scale** | `0.677`; `0.40 × 1.686` |
| K16 | at `delta_c = 1.686` the modification never fires | `0.7602` vs `0.7602` |
| K17 | transfer shape: `k_NL`, `sigma(R)` | `0.224 h/Mpc`; `3.53`, `0.932`, `0.0717` |
| K18 | **no linear scale reaches `a_0`** | max `0.0021 a_0` at 21.5 Mpc; 479× short |
| K19 | the filter on the *linear* field gives `G_eff = 11.5–291` | `sigma8 -> 2.27` |
| K20 | `R(a_0)` exists only nonlinearly | `1.4–52 kpc`; `k(a_0) = 29–1037 h/Mpc` |
| K21 | filtered = inert | `0.7602` |
| K22 | branch (b) is blue, filtered is not | `0.630` vs `1.000` |
| K23 | cluster-count discriminator | `×8868` |
| K24 | background discriminator vs ΛCDM | `f(0)` −14.4 %; `sigma8` −6.3 % |

Mutations (`--mutate`), each changing a **term or a reading**, each breaking a check and exiting 1:
`pointwise` (K13, K21), `cH` (K13, K21), `quad` (K12), `nocut` (K15), `gamma_pc` (K6, K8) — see `MUTATE.md`.
`gamma_pc` is the sharpest: reading the 17 pc stiffness as 17 Mpc gives `(k lambda_P)^2 = 1.31` and the
coefficient drops from 1.000 to 0.433 — the "coefficient = 1" claim is load-bearing on the P scale being 17 pc.

## What this does not do

- **It does not derive the filter.** Nothing in A33 §1 selects `R(a_0)`; §6 says so. What is derived is that
  the alternatives fail: (b) on data, (a) on provenance, and any linear `G_eff` on the algebra.
- **No second-order perturbation theory.** K9b estimates the `O(delta^2)` correction's *size* (`0.2 %`) but
  does not integrate it. That is the only place the `a_0` effect lives in linear cosmology, and it is the
  natural next computation. It also needs the (P) bookkeeping defect fixed (§2, convention).
- **The `sigma8` anchor is A40's assumption**: same `A_s` ⇒ same `sigma8` at `z ~ 10`. With `H(0) = 77.3`,
  `Omega_m h^2 = 0.189` against Planck's 0.143, so the transfer function would actually differ; not computed.
  This is a systematic on the 0.760, probably of the same order as the 6 % offset it is being compared to.
- **No scale-dependent `P(k)` integration, no CMB, no halo model, no shear likelihood.** `f sigma8` are
  ΛCDM-fiducial: a 1.147× `H(0)` shifts the AP conversion by a few per cent, not corrected (A40's caveat).
- **The `delta_c` scan uses one smoothing scale** (`R_8`) and one mapping `delta -> g_N`; other choices move
  `delta_c` by O(1). The qualitative statement (it must be quasi-linear, `delta_c < 1`) is robust because the
  `sigma8` mode reaches only 0.76 today.
- **The cold-sector fork is untouched** (A40 §5): `M_src = M_b + M_c` contradicts the baryon-only SPARC fits
  by 2.52×. Growth is degenerate between those branches (0.19 %), so nothing here depends on it.

## Next

1. **Second-order perturbation theory with the P sector.** The `(grad delta Phi)^2/a_0` term is the theory's
   only linear-cosmology signature; compute its effect on `P(k)` at `k = 0.05–0.3 h/Mpc` and check that it is
   really `0.2 %` and not, e.g., `O(1)` through a cumulative graviton-exchange effect.
2. **The nonlinear step.** `P(k)` at `k = 1–100 h/Mpc` with the law switched on at `R(a_0)` (a PM run, or the
   CFG960 engine with the growth box). That is where the theory differs from ΛCDM at *all*; `sigma8` does not
   see it.
3. **Fix (P)'s dimensional bookkeeping** (clock term / `K` normalisation) before any second-order use.
4. **Re-anchor `sigma8` with the theory's own `Omega_m h^2`**, which is the dominant systematic on the 0.760.
5. **A `k`-split `f sigma8` measurement** (e.g. bispectrum-assisted RSD at `z < 0.6`) is the observation that
   would settle (b) vs filtered without any new theory input.

## Reproduce

```bash
cd deepseek_push/DS_FINAL_2026_10_21/A45_reference_field
python3 a45_checks.py | tee a45.out          # 25/25, exit 0; writes a45_results.json
for m in pointwise cH quad nocut gamma_pc; do
  python3 a45_checks.py --mutate $m > a45_MUTATE_$m.out 2>&1; echo "$m $?"   # each exit 1
done
```

`a45_results.json` carries every number quoted here: `algebra`, `linear_order` (coefficient, `G_eff`,
`g_consistent`), `growth` (three branches + the `f sigma8` rows), `delta_c` (the scan and the root), `filter`
(`sigma(R)`, `max g_R`, `R(a_0)`, `k(a_0)`), `discriminators`, `verdict`, `checks`. No network, no fits, no
free parameters beyond the two the record already carries (`a_0`, `L*`).
