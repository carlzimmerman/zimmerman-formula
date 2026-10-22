# A59 — is the theory actually excluded by `alpha_1`?

**Lane:** A59_alpha1_observable · **Date:** 2026-10-21 · **Base:** `DS_FINAL_2026_10_21/BRIEF.md`,
`A36_galactic_alpha1/report.md`, `A22_ppn_frames/report.md`, `A12_slip_theorem/report.md`
**Script:** `a59_checks.py` (22/22 PASS, exit 0) · **Output:** `a59.out` · **Data:** `a59_results.json`
**Action:** the frozen round-2 action, verbatim; `c = 1` in the algebra, `K = 4 pi G`; `a0 = 9.36e-11 m/s^2`,
`L* = 24 pc`, `lambda = 16.97 pc`, `w_CMB = 369.82 km/s` (`(w/c)^2 = 1.5217e-6`).

---

## Claim

**A36's coefficient is right and its verdict is wrong.**

`alpha_1` is a *coefficient*, not an observable. In the PPN sector the `alpha_1` Lagrangian is
**bilinear in velocities** (Shao & Wex 2012, eq. 7),

```
L_a1 = -alpha_1 (G m1 m2 / r) (v1.v2) / (2 c^2),      v1, v2 = ABSOLUTE velocities
     = -alpha_1 (G m1 m2 / r) [ V^2 + ((m2-m1)/M) V.u - (m1 m2/M^2) u^2 ] / (2c^2),
```

`V` = barycentric velocity w.r.t. the preferred frame, `u` = relative velocity. There is **no
velocity-independent term** (K7, exact). Every `alpha_1` observable is therefore

> **`O = alpha_1 x (v/c)^2 x (a dynamical quantity)`, with `v` in `{V, u}`.**

The bound `|alpha_1| < 1e-4` is a bound on the coefficient *as measured in the environment of the
measurement*. In this theory that coefficient is a response function of two variables — the local
acceleration `g` and the coherence scale `r_s` of the field being tested (A36 eq. 2.5):

```
alpha_1(g, r_s) = 4 u' / (D - u'),   u' = a0^2/(g+a0)^2,   D = 1 + (L*/r_s)^2 u'/2.
```

It is screened by *both*: `alpha_1 -> 4(a0/g)^2` at high acceleration and `alpha_1 -> 8(r_s/L*)^2`
for a source small compared with `L*`. It spans **46 decades** (K5). The environments where the
bound is measured are at `g/a0 = 6.3e7` (LLR) and `1e9-1e12` (binary pulsars), where this same formula
gives `1.1e-13` and `8.4e-24` — i.e. **8.9 and 18.6 decades inside their own bounds**.

> **Status: `SURVIVES(alpha_1)`. The theory is not excluded by any `alpha_1` measurement.**
> **A36's verdict is over-scoped by ~13 decades** (it compares the galactic value 0.93 with a bound
> obtained at `g/a0 = 6e7`, where the theory gives 1.1e-13).
>
> **What A36 does establish, and this lane confirms: the claim `alpha_1 = alpha_2 = 0` is false in
> the galactic regime.** `alpha_1 = 0.046 ... 5.19` for `r = 1 ... 30 kpc` (K1/K2 reproduce A36's
> tables from its own formula). That claim must be retired; the theory survives its retirement.

---

## 1. The observable signature of `alpha_1` (task 1)

### 1.1 Why everything carries `(v/c)^2` — the bilinearity theorem (K7, K8)

`L_a1` is quadratic in velocities. Expanding `v1 = V + (m2/M)u`, `v2 = V - (m1/M)u` gives exactly
three pieces and nothing else:

| piece | coefficient | what it does |
|---|---|---|
| `V^2` | `-alpha_1/2 (Gm1m2/r)/c^2` | uniform rescaling of `G` by `(1 + alpha_1 V^2/2)` — **not observable** (absorbed into masses) |
| `V.u` | `-alpha_1/2 (Gm1m2/r)(m2-m1)/(M c^2)` | velocity-dependent force at the orbital frequency — **the polarisation** |
| `u^2` | `+alpha_1/2 (Gm1m2/r)(m1m2/M^2)/c^2` | an effective `gamma`-like shift of the two-body binding |

No term without a velocity. A theory whose `alpha_1` were observable at zeroth order in velocity
would not have `alpha_1` as its PPN parameter. This is the structural reason the bound cannot be
transferred from one environment to another: the bound is on `alpha_1`, the measurement is on
`alpha_1 (v/c)^2`, and `(v/c)^2` is environment-specific.

### 1.2 Preferred-frame acceleration (K8, exact)

Euler–Lagrange of `L_a1` in the test-body limit gives, in closed form,

```
delta a = (alpha_1/2)(G M/c^2) [ V rdot - (V^2 + V.u) rhat ] / r^2
        = (alpha_1/2)(V^2/c^2) g      [isotropic; a G-rescaling, absorbed into the masses]
        + (alpha_1/2)(V.u/c^2) g      [velocity-dependent, along g]
        + (alpha_1/2)(V rdot/c^2) g rhat/(GM/r^2)   [velocity-dependent, transverse].
```

So the "preferred-frame acceleration" is `delta a / g = (alpha_1/2)(V/c)^2` plus the two
velocity-dependent terms of relative size `(alpha_1/2)(V.v/c^2)`. With `V = 369 km/s` and
`v = 220 km/s` (a galactic disk), the isotropic piece is `7.6e-7 alpha_1` and the velocity-dependent
pieces `9.1e-10 alpha_1`.

### 1.3 Nordtvedt-type polarisation of an orbit (K7, K8; Shao & Wex 2012)

The `V.u` piece is a forcing at the orbital frequency, so it does not average away: it drives a
**fixed forced eccentricity** whose direction is set by the preferred frame,

```
e_F = kappa alpha_1 (Delta m / M) (V/c)(v_orb/c) nhat,   nhat || w x L,   kappa = O(1)
```

(`kappa = 1/2` for a circular orbit in the quadrupole estimate; the direction is perpendicular to
both the orbital angular momentum and `w`). This is the "orbit polarisation": the eccentricity
vector is the vector sum of a freely precessing `e_R` and the fixed `e_F`, so the observable is a
secular change of the projected semi-major axis, `xdot ~ e_F x n_b` (pulsars) or a sidereal/annual
range modulation (LLR). Numerically, for PSR J1738+0333 (`Delta m/M = 0.78`, `(V/c)(v/c) = 1.29e-6`),
`e_F = 5.0e-7 alpha_1`.

*The other Nordtvedt channel.* In the standard PPN bookkeeping `alpha_1` also enters the Nordtvedt
parameter linearly, `eta_N = 4beta - gamma - 3 - (10/3)xi - alpha_1 + (2/3)alpha_2 - ...`. That
reading carries no `(v/c)^2` and is therefore the *most damaging* possible interpretation for the
theory. It is tested in K21: with `alpha_1(LLR) = 1.1e-13`, `eta_N = 1.1e-13` against the MESSENGER
bound `|eta_N| < 7.2e-5` — **8.8 decades inside**. The theory passes that channel too, so the
verdict does not depend on which reading is correct.

### 1.4 Anisotropic correction to a rotation curve (K9)

For a star moving at `v(r)` inside a galaxy whose bulk velocity w.r.t. the preferred frame is `W`,

```
|W + v|^2/c^2 =  W^2/c^2        (monopole: delta g/g = (alpha_1/2)(W/c)^2)
              + 2 W.v/c^2       (dipole:   delta g/g = alpha_1 (W.v)/c^2)
              + v^2/c^2         (radial:   delta g/g = (alpha_1/2)(v/c)^2).
```

- The **monopole** is *exactly* degenerate with the mass: `g -> g(1+eps)` is `M -> M(1+eps)` (K9,
  residual 0). It is not an observable of a single system. It becomes observable only as a
  **sky-direction variation** between systems with different `W`, with amplitude
  `Delta(alpha_1 W^2/2c^2) ~ alpha_1 x 4.5e-6` — the distinctive prediction of §4.
- The **dipole** is the genuinely anisotropic term: an `m = 1` pattern in the disk aligned with the
  projection of `W` (the CMB dipole), of amplitude `alpha_1 (W v/c^2) = 9.1e-10 alpha_1`.
- The **radial** term is a shape correction `delta v/v = (alpha_1/4)(v/c)^2` = `1.3e-7 alpha_1` at
  220 km/s.

At 8 kpc (`alpha_1 = 0.93`): `delta v/v = 1.25e-7`, i.e. **2.7 cm/s on a 220 km/s rotation curve.**

### 1.5 The two screens (K3-K6)

| limit | `alpha_1` | where |
|---|---|---|
| `k L* -> 0`, `u' -> 1` | `4u'/(1-u')` (max `-> infinity` as `u' -> 1`) | galaxies, clusters (`r_s >> L*`, `g ~ a0`) |
| `k L* >> 1` | `8/(kL*)^2 = 8(r_s/L*)^2` | any source smaller than `L*` (solar system, binaries) |
| `u' -> 0` (`g >> a0`) | `4(a0/g)^2` | neutron stars, solar system, Earth |

`alpha_1 = 1` at `g = 1.236 a0`; `alpha_1 = 1e-4` at `g = 199.0 a0 = 1.863e-8 m/s^2` (K4).

---

## 2. Every environment with a real bound (task 2)

Margins are `log10(precision / alpha_1-signature)`; for coefficient rows the "precision" is the
published bound on `alpha_1` itself. `[DISK]` = number verified on disk (`DOOR11_LITERATURE`,
`BOUNDS.md`); `[LIT]` = literature value used with its source named; `[ASSUMED]` = no published
bound exists, an optimistic precision is used and flagged.

| environment | `g/a0` | `u'` | **`alpha_1` (theory)** | observable | theory prediction | precision | **margin** | src |
|---|---|---|---|---|---|---|---|---|
| NS surface (1.4 M, 12 km) | 1.4e22 | 5.3e-45 | **2.1e-44** | pulsar `alpha-hat_1` | — | 2.1e-5 | **39.0 dex** | `[DISK]` Liu 2020 |
| PSR J1738+0333 | 6.9e11 | 2.1e-24 | **8.4e-24** | `xdot` / `alpha-hat_1` | `e_F = 5.0e-7 alpha_1` | 3.5e-5 | **18.6 dex** | `[DISK]` Shao–Wex 2012 |
| wide pulsar binary (100 d) | 3.7e8 | 7.2e-18 | **2.9e-17** | timing | — | 1e-3 `[ASSUMED]` | **13.5 dex** | — |
| **Earth–Moon (LLR)** | 6.3e7 | 4.1e-14 | **1.1e-13** | orbit polarisation, `delta r` | `delta r = 6.4e-11 m` | 9e-5 (bound ↔ 5.3 cm) | **8.9 dex** | `[DISK]` Müller 2005 |
| wide binary 18.8 AU | 1.8e5 | 3.1e-11 | **6.0e-11** | relative accel. | `1.7e-18` | 1.2e-2 | **15.9 dex** | `[ASSUMED]` A24 band |
| wide binary 20 kAU | 0.158 | 0.745 | **1.31e-4** | relative accel. | `1.1e-13` (dipole) | 1.2e-2 | **11.0 dex** | `[ASSUMED]` A24 band |
| **outer SS 7000 AU** | 1.29 | 0.190 | **1.6e-5** | `delta a` | `1.5e-21 m/s^2` | **none exists** | **n/a** | — |
| **rotation curve 8 kpc** | 1.30 | 0.188 | **0.93** | `delta v/v` | `1.25e-7` (`2.7 cm/s`) | 1e-2 | **4.1 dex** | `[ASSUMED]` |
| **cluster (Coma-like)** | 0.346 | 0.552 | **4.92** | `delta M/M` | `2.7e-5` | 1e-2 | **2.6 dex** | `[ASSUMED]` |

Notes on the entries.

- **LLR.** The task's `2.4e7 a0` is the Earth's field at the Moon (`2.88e7 a0` computed); the Sun's
  field at 1 AU is `6.34e7 a0`. Both give `alpha_1 <= 1.1e-13`. Two branches of A36's own formula
  are computed: slaved (`u' = (a0/g)^2`, `alpha_1 = 1.0e-15`) and hedgehog (`u' = r^2/2lambda^2`,
  `alpha_1 = 1.09e-13`); the table quotes the **larger**, i.e. the conservative one.
  `delta r = r alpha_1 (w/c)^2 = 6.4e-11 m` against 2 cm ranging. The 9e-5 bound itself corresponds
  to `r x 9e-5 x (w/c)^2 = 5.3 cm` — within a factor 2.6 of the ranging precision (K17). **The
  published bound *is* a `(w/c)^2`-suppressed measurement of the coefficient.**
- **Pulsars.** `g` at the companion from the pulsar: `G M_p/a^2 = 64.7 m/s^2 = 6.9e11 a0`
  (the task's `1e9-1e11` bracket is the same regime for wider systems; `[ASSUMED]` 100 d row gives
  `3.7e8`). `alpha_1 = 4(a0/g)^2 = 8.4e-24`, so `e_F = 5.0e-7 x 8.4e-24 = 4e-30` and the induced
  `xdot` is ~`1e-35 s/s` against a `5e-16 s/s` measurement.
- **Wide binaries.** The task's pair "(20 kAU, `g = 1.8e5 a0`)" is internally inconsistent: for a
  1 Msun binary `1.8e5 a0` occurs at **18.8 AU**, while at 20 kAU `g = 0.158 a0` (K12). Both are
  tabulated. At 20 kAU the deep-MOND limit is exact: `alpha_1 = 8(r_s/L*)^2 = 1.31e-4` — **the
  closest any real environment comes to the 1e-4 line** (1.3x above it), and its observable
  signature is `1.1e-13`. Note that a wide binary is *not* an `O(1)`-`alpha_1` environment: at
  20 kAU the source is 250x smaller than `L*`, and the `(kL*)^2` screen suppresses it to the line.
- **Outer solar system.** 7000 AU is just inside the Sun's MOND radius (`r_MOND = sqrt(GM/a0) =
  7960 AU`, `g = 1.29 a0`), but `alpha_1 = 8(r_s/L*)^2 = 1.6e-5`, and the predicted anomaly is
  `1.5e-21 m/s^2` (with the CMB velocity) — no experiment exists there. Voyager 1 at 165 AU has
  `g = 2328 a0` and `alpha_1 = 8.8e-9`.
- **Clusters.** Observed `v_c = 1000 km/s` at `r = 1 Mpc` gives `g = 0.346 a0` — the deepest MOND
  environment with data — hence the **largest `alpha_1` in nature, 4.9**. This is also the
  extrapolated end of A36's formula (`u' = 0.55 > 0.3`); the conservative route (c) of A36 gives
  `alpha_1 = 0.63` there instead, which changes the margin only from 2.6 to 3.5 dex.

---

## 3. The decisive question (task 3)

> **Is there ANY environment where `alpha_1` is `O(0.1-5)` AND a precision test exists?**
>
> # No.

Two environments have `alpha_1 >= 0.1`, and neither has a test (K16):

| environment | `alpha_1` | signature | best precision | margin | what would be needed |
|---|---|---|---|---|---|
| cluster (Coma-like) | **4.92** | `2.7e-5` (`delta M/M`) | 1e-2 | **2.6 dex short** | 1e-5 relative masses |
| rotation curve 8 kpc | **0.93** | `1.25e-7` (`delta v/v`) | 1e-2 | **4.1 dex short** | 1e-7 relative velocities |

The reason is structural, not accidental: `alpha_1 = O(1)` requires `g <= 5.4 a0` (for `r_s >= L*`),
and in any bound system with `g <= 5.4 a0` the velocities are non-relativistic by construction. The
largest velocities in such systems are cluster dispersions, `1000-2500 km/s`, so `(v/c)^2 <= 7e-5`
and

```
max signature = alpha_1 (v/c)^2/2 <= 5 x 7e-5/2 = 1.7e-4      (the extreme: alpha_1 = 5, 2500 km/s),
realistic                          = 2.7e-5                  (cluster row of the table),
```

while the best relative-acceleration precision available in that regime is `~1e-2` (rotation curves,
cluster masses, wide binaries). **Two to four decades of margin for the systems that exist, and
never better than 1.8 decades even for the most extreme combination physics allows.** The only
environment with enough relative precision to see `alpha_1 x (v/c)^2` at the `1e-4` level is LLR
(`delta r/r ~ 5e-11`), and there `alpha_1 = 1.1e-13` — 8.9 decades inside the bound.

The task's premise is confirmed with numbers: the bound is satisfied *exactly where it is measured*
(`alpha_1 = 1.1e-13` at LLR, `8.4e-24` at PSR J1738+0333) while the galactic-regime value is `O(1)`
— and the galactic value is unobservable because `(v/c)^2 <= 1e-5` there.

---

## 4. The upside: environment-dependent `alpha_1` is a parameter-free prediction (task 4)

### 4.1 Where `alpha_1` crosses `1e-4` (K6)

The `1e-4` line is a **locus**, not an acceleration:

```
alpha_1 = 1e-4  at  g* = 199 a0 = 1.863e-8 m/s^2      for any source larger than ~1 pc,
                at  g* = 96 a0  = 9.0e-9 m/s^2       for a 20 kAU wide binary,
                and NEVER                           for a source smaller than 17.5 kAU,
                                                    where max alpha_1 = 8(r_s/L*)^2 < 1e-4.
```

The systems where `g = 199 a0` occurs:

| system | radius where `g = 199 a0` |
|---|---|
| Sun (1 Msun) | **564 AU** |
| 2 Msun binary | **798 AU** (a Gaia wide binary) |
| MW-like galaxy (1e11 Msun) | **0.87 kpc** from the centre |
| any field coherent on `>= L* = 24 pc` | `g = 1.86e-8 m/s^2` |

### 4.2 The one observation

> **A CMB-dipole-correlated modulation of the effective acceleration scale**, of amplitude
> `Delta a_eff/a_eff = alpha_1 Delta(W^2)/2c^2 = 2e-6` between systems on opposite sides of the sky.
> It must switch off at `g > 2e-8 m/s^2` (199 a0) — inside 564 AU of the Sun, 0.87 kpc of a
> MW-like galaxy, 800 AU of a solar-mass binary — and reach its full `O(1)` value only for fields
> coherent on `>= 24 pc` at `g <= a0`.

This is distinctive because the direction is fixed (the CMB dipole, `(l,b) = (264.0, 48.3) deg`), the
amplitude is fixed (`alpha_1` is not free), and the *sign* of the acceleration-dependence is fixed
(positive, turning on below 199 a0). No constant-`alpha_1` theory makes a direction-dependent
acceleration scale; a MOND completion that does would have to reproduce the same `(a0/g)^2` screen.

**Can existing data see it? No.**

| channel | prediction | best existing | short by |
|---|---|---|---|
| TF/RAR zero-point dipole vs CMB direction | `2e-6` | CF4 TF dipole `0.063 +- 0.016 mag` = 6 % `[DISK]` | **4.5 dex** |
| cluster mass vs sky direction | `2.7e-5` | ~1 % masses | 2.6 dex |
| rotation-curve dipole (m=1, CMB-aligned) | `8.4e-7` | ~1 % per point | 4.1 dex |
| wide-binary knee at 17.5 kAU | `1e-13` | 1.2e-2 | 11 dex |

The claimed 25-37 % `a0` dipole of Zhou et al. 2017 / Chang et al. 2018 is **five decades too large**
to be this effect and points ~94-103 deg from the CMB dipole; it is not this prediction and this
prediction is not that claim.

---

## 5. Audit of A36

### 5.1 What stands (verified here)

- The formula `alpha_1 = 4u'/(D-u')` and the galactic numbers `0.046 ... 5.19`: **reproduced**
  from A36's own code (K1: max relative difference `4.9e-3` on route (a), `3.6e-4` on route (b);
  K2: `1.1e-2` on route (c); all consistent with A36 quoting 3 decimals).
- The structural finding that the clock term's `(1+2w^2)` source rescaling rescales a `1/r`
  potential in the MOND regime, so `alpha_1 != 0`: **stands**. `alpha_1 = alpha_2 = 0` is not a
  property of this theory in the MOND regime.
- `alpha_2 = 0`: consistent with the bilinearity (w enters only as `|w|^2`).

### 5.2 What does not stand

1. **The scope of the verdict.** A36 compares `alpha_1(k = 1/kpc, g = 1.3 a0) = 0.93` with a bound
   on `alpha_1` obtained at `(k = 1/AU, g = 6.3e7 a0)`, where the same formula gives `1.1e-13`. The
   ratio is `8.5e12` (**12.9 decades**). "2.66-4.72 decades above the bound" should read
   **"8.9-18.6 decades below the bound"** in the two environments where the bound exists.
2. **Its own §8 contradicts its §4.** A36 §8 item 3 states that `alpha_1 ~ 0.05-0.6` predicts a
   `2e-7` to `3e-6` modulation, "below any present measurement", and that "the theory therefore
   dies here by principle, not by data". A `(v/c)^2`-suppressed, unmeasurable coefficient is not an
   exclusion; it is an untested prediction. Recomputing A36's own conservative route gives
   `7.0e-8 ... 9.6e-7` — a factor 2-3 below its quoted range (K19).
3. **An arithmetic slip, not load-bearing.** A36's K11 quotes `alpha_1(1 AU) = 5.44e-14`, but its
   headline formula (factor 4, not 2) gives `1.09e-13` (K18: ratio exactly 2.00). Both are far
   below `1e-4`; the number in §6 of A36 ("5.4e-14") should read `1.1e-13`.
4. **The K12 caveat does not threaten the LLR pass.** A36's K12 notes that the solar-system P
   configuration is not established (galactic background `u = 0.566 a0` vs isolated-Sun hedgehog
   `u = 2.6e-6 a0`). K22 closes this for the `alpha_1` question: at 1 AU, `alpha_1 = 4u'/(1 +
   (L*/AU)^2 u'/2 - u')` is **maximised at `u' -> 1`**, giving `8/(kL*)^2 = 3.3e-13` — for *any*
   `u'`, i.e. for any solar-system P configuration. The LLR pass does not depend on the open problem.

### 5.3 The correct statement of A36's result

> `alpha_1` is not a PPN parameter in the MOND regime: it is a response function spanning 46
> decades, `2e-44` at a neutron-star surface to `5.2` at 30 kpc. **The claim `alpha_1 = 0` is
> refuted.** Every measurement of `alpha_1` is made where the theory gives `<= 1.1e-13`, so **no
> measurement excludes the theory**; and no environment with `alpha_1 >= 0.1` has a test, so none
> can. The theory is *unfalsified by `alpha_1`* and *newly predicted* to have a
> velocity- and acceleration-dependent preferred-frame response.

---

## 6. Status

**`SURVIVES(alpha_1)`** — the theory is not excluded. **`OVER-SCOPED`** — A36's `NO-GO(exclusion)`
label is withdrawn as an exclusion of the theory; it is retained only as an exclusion of the
*claim* `alpha_1 = alpha_2 = 0`, which this lane confirms is false.

`CLOSED-DERIVED` for: the bilinearity of the `alpha_1` sector (K7), the closed-form
preferred-frame acceleration (K8), the monopole degeneracy (K9), the `1e-4` locus (K6) and the
`8/(kL*)^2` ceiling at 1 AU (K22). `CONDITIONAL` on A36's linearised `alpha_1(k,g)` (factor-7
spread in the galactic value, uncontrolled for `u' > 0.3`) — but every conclusion here is
insensitive to that spread: the O(1) environments stay O(1) (route (c) gives 0.63 at a cluster
instead of 4.9) and the verdict moves by < 1 decade.

---

## 7. Checks (`a59_checks.py`, 22/22 PASS, exit 0)

| id | what it proves | measured |
|---|---|---|
| K1 | A36 route (a)/(b) tables reproduced | `4.9e-3`, `3.6e-4` |
| K2 | A36 route (c) reproduced | `1.1e-2` |
| K3 | limits: `4u'/(1-u')`, `0`, `0`, `8/(kL*)^2` | residual 0 |
| K4 | `alpha_1 = 1` at 1.236 a0; `1e-4` at 199.0 a0 | exact |
| K5 | `alpha_1(g)` monotone; 46-decade span | `True`, 45.7 |
| K6 | the `1e-4` locus: 199 a0 / 96 a0 / 17.5 kAU | 199.0, 95.8, 17502 |
| K7 | `alpha_1` Lagrangian is bilinear: 0 velocity-independent terms | residual 0 |
| K8 | closed-form preferred-frame acceleration | residual 0 |
| K9 | monopole piece exactly degenerate with mass | residual 0 |
| K10 | LLR: `6.4e-11 m` predicted vs `5.3 cm` at the bound | 8.9 dex |
| K11 | pulsars: 18.6 / 13.5 dex inside | PASS |
| K12 | wide binary 20 kAU: `8(r/L*)^2 = 1.31e-4` | ratio 1.000 |
| K13 | outer SS 7000 AU: `alpha_1 = 1.6e-5`, `delta a = 1.5e-21` | no test |
| K14 | rotation: `delta v/v = 1.25e-7`, 4.1 dex short | 4.08 |
| K15 | cluster: `alpha_1 = 4.92`, 2.6 dex short | 2.56 |
| K16 | **no** environment with `alpha_1 >= 0.1` and a test | count 0 |
| K17 | published bounds are `(v/c)^2` measurements: 9e-5 ↔ 5.3 cm | factor 2.6 |
| K18 | A36 K11 uses factor 2 where its formula has 4 | ratio 2.00 |
| K19 | A36 §8's own modulation `2e-7..3e-6` recomputed `7e-8..9.6e-7` | within 3x |
| K20 | verdict logic: O(1) coefficient, satisfied bounds, no test | True/True/True |
| K21 | `eta_N` channel without `(v/c)^2`: 8.8 dex inside MESSENGER | 8.8 |
| K22 | `alpha_1(1 AU) <= 8/(kL*)^2 = 3.3e-13` for ANY P configuration | 3.26e-13 |

Mutations (`MUTATE.md`): `--mutate freeze` (freeze `alpha_1` at its 8 kpc value in every environment
— A36's implicit assumption) breaks K10, K11, K12, K13, K16, K20 and **reproduces A36's exclusion**
(LLR would predict 543 m against 5.3 cm). `--mutate nolstar` (drop the coherence factor) breaks K12,
K13. Both exit 1.

---

## 8. What this does not do

- **No nonlinear `O(w^2)` solve.** Every number uses A36's linearised `alpha_1(k,g)`; the galactic
  value carries a factor-7 three-route spread. The verdict is invariant to it, but the individual
  galactic numbers are not.
- **No independent derivation of the `alpha_1` Lagrangian.** K7/K8 use the standard PPN `alpha_1`
  term (bilinear in absolute velocities), which A22's matching convention reproduces. If the theory's
  `alpha_1` were to enter some observable *not* through that term, the counting would change — but
  then the coefficient would not be `alpha_1`.
- **The `u' -> 1` end is an extrapolation** (clusters `u' = 0.55`, 30 kpc `u' = 0.57`); A36's own
  caveat applies. The conservative route (c) leaves the cluster at `alpha_1 = 0.63`, margin 3.5 dex.
- **No strong-field `alpha-hat_1` computation.** The pulsar bounds are on the hatted parameter; the
  theory's P field is deeper in the screened regime inside a neutron star, so `alpha-hat_1 <= alpha_1`
  is the likely direction, but it is not computed.
- **The solar-system P configuration remains open** (A36 K12). K22 shows the *`alpha_1`* conclusion
  is independent of it; other observables (`a_P`, the kernel anomaly) are not.
- **No cosmological `alpha_1`.** On FRW the P field has no VEV (A22 D8), so there is no `alpha_1`
  sector in the background and the CMB is not a bound system against which `(v/c)^2` can be counted.
- **No survey for other theories with environment-dependent `alpha_1`.** The prediction is
  parameter-free and falsifiable; "no other theory makes it" is not established here.

---

## 9. Next

1. **The sky-direction test at 2e-6.** Fit a CMB-dipole-aligned modulation of the RAR/BTFR
   normalisation on SPARC + CF4 with the amplitude free. The prediction is a *fixed-direction*,
   *fixed-amplitude* (`2e-6`) signal that must vanish for galaxies whose `g > 200 a0`. Existing
   directional claims (25-37 %) are 5 decades too large and misaligned, so the measurement is a
   clean null-test of this prediction, not a confirmation of theirs.
2. **The knee at 17.5 kAU.** Stack Gaia wide binaries in separation bins around 10-30 kAU and look
   for the `(r/L*)^2` turn-on of an orbit-polarisation signal. Requires ~1e-5 relative acceleration;
   present precision is 1e-2, so this is a Gaia-DR5/ELT-era test.
3. **Nonlinear `O(w^2)` solve** to replace the three-route bracket by one number (A36 §8 item 1) —
   the only way the galactic `alpha_1` moves, and it cannot move the verdict.
4. **Correct `FINAL_THEORY.md` §3/§8 and A22's status line** to: *"`alpha_1 = alpha_2 = 0` holds for
   `r << lambda`; in the MOND regime `alpha_1 = 4u'/(D-u')` is O(1) but every observable is
   `(v/c)^2`-suppressed and no measurement constrains it. A36's `EXCLUDED` is withdrawn."*