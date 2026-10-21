# A16 — the cutoff chain and the edge prediction

Lane A16. Script `a16_checks.py`, output `a16.out`, numbers `a16_results.json`, mutations `MUTATE.md`. SI.

## Claim

One `L*` does generate three lengths, and A11's arithmetic is right: at `L* = 24 pc` they are **106.63 pc**
(Jeans), **82.35 kpc** (free streaming) and **1.0205 Mpc** (half mode), a spread of **3.98 dex**. But the chain
is not a chain — it is three *different* functionals of one parameter, with exponents `1`, `1/2` and `0.6118`,
and **no `(L*, rho_c, sigma)` tuple makes them coincide anywhere in the window**: the pairwise crossings sit at
`L* = 14.315 Mpc`, at `L* = 4.44e11 pc` and nowhere, and the smallest achievable spread inside `[24 pc, 1 kpc]`
is **3.357 dex**. The system is rank 2 in three unknowns — `rho_c` is an exact null direction because the
`Gamma = 2` polytrope has a **density-independent** Jeans wavenumber — so it is over-determined by one, and by
two once `sigma^2 = a0 L*` is imposed. The edge is not testable on SPARC: `r_e/r_M = 22.79 … 54.14`, **0 of 175
curves reach `r_e`**, closest approach **20.74 %** (`UGC09133`) — the expected null, but not a vacuous one,
since the same statistic requires `N > 10.118` and **excludes the fitted `N = 8.296` at three curves**. Three
results. **(i)** The pressure switch-off is a **length, not a density**: for any cusp `rho ∝ r^-n` with
`1 <= n <= 2` the pressure/gravity ratio is `(L*/r)^2`, so `r_switch = L* = 24.02 pc` in an MW-like halo, `3.3x`
inside the innermost SPARC point — no density threshold anywhere and no conflict with the RAR. **(ii)** The
Jeans mass there is `M_J = 3.654 V_f^2 L*/G = 2.039e4 (V_f/km/s)^2 Msun`, i.e. **5.565e8 Msun inside 53.31 pc**
for the MW — an ultra-compact dwarf / massive nuclear star cluster. **(iii)** A11 §14's superluminality is a
`c^2` unit slip: `c_s = 0.720473 m/s = 2.4032e-9 c` at cosmic mean, not `0.72 c`; `c_s = c` needs
`L* = 9.99 Gpc` or `rho = 5.7738e9 Msun/pc^3`. The `Gamma = 2` pressure is subluminal everywhere in a galaxy, so the
causality motive for switching it off does not exist.

## Derivation

`gamma = K L*^2/2` with `K = 4 pi G` (AG6D `FROZEN_CRITERIA.md` §0, the stiffness lane's own convention), so
`gamma = 2 pi G L*^2`; `P` is the displacement with `div P = rho_c - rhobar_c`, `e` its internal energy density,
`rho_c` the cold-sector density, `sigma_c` its dispersion.

### 1. Equation of state, and length 1 (K1–K3)

    e = (gamma/2)(rho_c - rhobar_c)^2
    p = rho_c de/drho_c - e = (gamma/2)(rho_c^2 - rhobar_c^2)                     (1)
    c_s^2 = dp/drho_c = gamma rho_c = 2 pi G L*^2 rho_c                            (2)
    omega^2 = c_s^2 k^2 - 4 pi G rho_c = 4 pi G rho_c [ (L* k)^2/2 - 1 ]           (3)
    k_J = sqrt(2)/L*,     lam_J = 2 pi/k_J = sqrt(2) pi L* = 4.443 L*              (4)

K1: (2) is exact (sympy residual `0`); this is AG6D Part A's `Gamma = 2` polytrope, nothing added. K2:
`d ln k_J/d ln rho_c = 0` **identically** — the `rho_c` in `c_s^2` cancels the one in the Jeans frequency. That
cancellation makes `L*` one length instead of a density-dependent one, and makes `rho_c` a null direction of
everything below. K3: `lam_J = 106.6292 pc` at 24 pc, `4442.8829 pc` at 1 kpc.

### 2. Length 2 — free streaming (K4, K5)

`L*` is a velocity-squared over `a0`, so the dispersion is fixed rather than free:

    sigma_c = sqrt(a0 L*)  ->  8.3257 km/s at 24 pc,  53.7419 km/s at 1 kpc          (5)
    lam_FS = 2 sigma_c/(3 H0) = 82.3502 kpc  and  531.568 kpc                        (6)

(6) is the comoving distance a *fluid* element coasts in one EdS Hubble time. `sigma_c` is a sound speed set by
`L*`, not a decaying relic velocity, so `2/(3H0)` is the right coefficient.

### 3. Length 3 — half mode (K6, K7)

The pressure enters the linear growth as `-(c_s^2 k^2/a^2) delta_c`; with `c_s^2 = 2 pi G L*^2 rhobar_c` and
gravity `4 pi G rhobar_m`,

    (c_s^2 k^2/a^2)/(4 pi G rhobar_m) = f_c (L* k/a)^2/2,   f_c = Omega_c/Omega_m      (7)

— again **no local density**, only the cosmic ratio. Integrating AG6D §4 (baryons, `Lambda`, horizon-entry ICs,
`T = delta_m(L*)/delta_m(0)` at `z = 49`) reproduces the record's half mode (K6):

| `L*` (pc) | 24 | 50 | 100 | 300 | 1000 |
|---|---|---|---|---|---|
| `k_1/2` (Mpc^-1) | 0.97995 | 0.61584 | 0.40306 | 0.20407 | 0.10011 |
| `1/k_1/2` (Mpc) | 1.02046 | 1.62380 | 2.48102 | 4.90035 | 9.98910 |

`k_1/2 = 0.9695 (L*/24 pc)^-0.6118 Mpc^-1` (max residual 5.6e-3 dex); `M_1/2 = 5.442e12 Msun` at 24 pc. The
`0.6118` is the whole problem: it is neither 1 nor 1/2.

### 4. The system: rank, crossings, no solution (K9–K11)

    lam_J(x)   = sqrt(2) pi L*        depends on L* only
    lam_FS(x)  = 2 sigma/(3 H0)       depends on sigma only
    lam_1/2(x) = 1/k_1/2(L*)          depends on L* only                            (8)

The Jacobian is `[[dL,0,0],[0,0,dsigma],[dL',0,0]]`: **rank 2 of 3** (K9), `rho_c` an exact null direction by
(3) and (7). So the system is *over-determined by one*, and by two once the velocity-window link
`sigma = sqrt(a0 L*)` (5) is imposed. Exactly one tuple reproduces the three quoted lengths, the one they were
computed at: `L* = 24 pc`, `sigma = 8.3257 km/s`, `rho_c = 2.25697e-27 kg/m^3 = 3.3347e-8 Msun/pc^3` — the
`rho_c` component is unconstrained (it enters only `M_J` and `c_s`). So, solving it as a system:

- **as a prediction** it is consistent and rigid: `L*` fixes all three with zero freedom.
- **as a fit** there is no solution for a *single* cutoff. The pairwise equalities are

      lam_J = lam_FS   <=>  L* = 2 a0/(9 pi^2 H0^2) = 14.315 Mpc        (analytic, K10)
      lam_J = lam_1/2  <=>  L* = 4.44e11 pc                             (8-dex extrapolation)
      lam_FS = lam_1/2 <=>  no crossing: the ratio is 0.07984 at 24 pc and
                            0.05261 at 1 kpc, monotone, always < 1                 (9)

  all outside `[24 pc, 1 kpc]` by `1.4e4` and more, so `lam_J < lam_FS < lam_1/2` is **rigid**.
- **the best case**: `log10(lam_1/2/lam_J)` decreases monotonically in `L*`, so its minimum on the window is at
  the ceiling, **3.357 dex at `L* = 1 kpc`** (K11) — a factor 2274. No `L*` makes the three one scale.

The obstruction is structural: **the three lengths carry three different powers of `L*`** (1, 1/2, 0.6118) — the
Jeans length is fixed by the polytrope's density-free `k_J`, the free-streaming length is `sqrt(a0 L*)/H0`, and
the half mode is set by *when* a mode turns Jeans-unstable relative to horizon entry. One cutoff needs equal
exponents; none are equal.

### 5. The edge on SPARC (K12–K17)

`r_e = r_M sqrt(N(N+1))`, `r_M = sqrt(G M_b/a0)` (A11 eq. 7). `N = 5.364327/f_ret` with `f_ret` the CFG416 table
evaluated at the **turnaround** mass, `M_b = f_ret f_b M_ta/h` inverted per galaxy (K12 reproduces A11's
`N = 53.643, 44.125, 14.917, 8.296, 5.960` to 2.1e-15). Sample: 175 `rotmod` curves, 3391 points,
`M_b(<r_max) = 5.03e7 … 3.64e11 Msun`, `Upsilon_d = 0.5`, `G_bar = (V_gas^2 + Upsilon V_disk^2 + 1.4 Upsilon
V_bul^2)/r`.

| quantity | value |
|---|---|
| census `N`; predicted `r_e/r_M` | `22.30 … 53.64`; `22.79 … 54.14` |
| curves reaching `r_e` | **0 / 175** |
| closest approach `max(r_max/r_e)` | **0.2074** (`UGC09133`) |
| `N` required by the data, `max N_min` | **10.118** (`D564-8`) |

Because `r_e >= sqrt(2) r_M` for any `N >= 1`, a curve can only violate by extending *beyond* `r_e`, which yields
a **lower** bound on `N`; the census sits 2–5x above it, so `0/175` is indeed **no constraint** on the census
reading. The statistic is not vacuous — scanning `N`:

| `N` | 1 | 2 | 3 | 5 | **8.296** | **10.12** | 20 | 53.64 |
|---|---|---|---|---|---|---|---|---|
| `r_e/r_M` | 1.414 | 2.449 | 3.464 | 5.477 | 8.782 | 10.608 | 20.494 | 54.141 |
| curves beyond `r_e` | 166 | 147 | 117 | 38 | **3** | **0** | 0 | 0 |

So SPARC **excludes `N <= 10.118`** and excludes the fitted `N = 8.296` at three curves (`D564-8` 1.2077x,
`NGC3741` 1.1855x, `UGC00128` 1.0816x beyond their edges). Caveats: `M_b(<r_max)` is enclosed, not total; inflating it by
**1.33x** clears the `N = 8.296` violation, so *that* exclusion is marginal while the census null (0/175 at
`N >= 22.79`) is not. At `Upsilon_d = 0.7` the bound moves to `N > 9.829` (−2.9 %). The test that would bite — a
Keplerian turnover at `50–500 kpc` — is outside SPARC (A11 §Next).

### 6. The switch-off: a length, not a density (K8, K18, K19)

The motive has to be checked first. `c_s^2 = 2 pi G L*^2 rho_c` in SI at `rho_c = Omega_c rho_crit` and
`L* = 24 pc` is **0.519081 m^2/s^2**, i.e. `c_s = 0.720473 m/s = 2.4032e-9 c` (K8). A11 §14 reports that number
as `0.5191` in units of `c^2` and concludes `c_s = 0.72 c`; the `33.311 pc` at which it says `c_s = c` is in
fact the `L*` at which `c_s = 1 m/s`, and `c_s = c` needs `L* = 9.9865e9 pc = 9.99 Gpc`. The reverse reading —
the density at which `c_s = c` for `L* = 24 pc` — is `3.9078e-10 kg/m^3 = 5.7738e9 Msun/pc^3`, a white-dwarf
core density. At a galactic `0.01 Msun/pc^3`, `c_s = 394.54 m/s = 1.32e-6 c`. **The `Gamma = 2` pressure is
subluminal by 6–9 dex everywhere a galaxy exists**; the causality switch-off is not needed, and A11 §14's no-go
and its `L* <= 0.0608 pc` galactic ceiling are artefacts of the slip.

What *does* switch is the pressure force against gravity. With `p = (gamma/2) rho_c^2`,

    (1/rho_c) dp/dr / g = 2 pi G L*^2 |d ln rho_c/dr| / g                          (10)

and for `rho_c ∝ r^-n`, `M = 4 pi rho_c r^3/(3-n)`, `g = 4 pi G rho_c r/(3-n)`:

    R_press(r) = [n(3-n)/2] (L*/r)^2 = (L*/r)^2 for n = 1 (NFW cusp) and n = 2      (11)

so `r_switch = L* sqrt(n(3-n)/2)`, i.e. `L*` to `1.06 L*` for every cusp with `1 <= n <= 2`, and *zero* for a
core. This is a **gradient threshold of one length, `L*`** — there is no density threshold, because `k_J` is
density-free. For an MW-like halo (`M_200 = 1e12 Msun`, `c = 10`, `r_200 = 211.6 kpc`, `r_s = 21.16 kpc`) the
numerical root of (10) is `r_switch = 24.018 pc` (`1.0008 L*`, K18) at `rho_c = 4.9609 Msun/pc^3`.

RAR region: the innermost SPARC point is `r = 0.080 kpc = 3.3 L*`, where (11) gives `R_press <= 0.0900`; at
1 kpc `R_press = 6.09e-4` (`5.76e-4` analytic, K19). **The switch is 3.3x inside the innermost datum, the pressure
is < 9 % of gravity at the worst point and < 0.1 % beyond 1 kpc** — no conflict with the RAR.

### 7. One new number: the Jeans mass at the switch (K20, K21)

`R_TF = lam_J/2 = pi L*/sqrt(2) = 53.3146 pc`, mass-independent. `M_J = (4 pi/3) rho_c R_TF^3`, so with the
law's own flat-curve profile `rho_c = V_f^2/(4 pi G r^2)` at `r = r_switch = L*`:

    M_J(r_switch) = (pi^3/(6 sqrt2)) V_f^2 L*/G = 3.654 V_f^2 L*/G
                  = 2.039e4 (V_f/km/s)^2 Msun                                      (12)

For `V_f = 165.2 km/s`: **`M_J = 5.565e8 Msun` inside 53.31 pc** (half-mass radius `32.34 pc`, mean density
`876.6 Msun/pc^3`) — the **ultra-compact dwarf / massive nuclear star cluster** class, the `(M, r_eff)` locus of
M59-UCD3-like objects. The NFW reading of the same halo (lower inner density, 4.9609 `Msun/pc^3`) gives
`3.149e6 Msun`, a globular cluster: the *class* spans GC-to-UCD and the mass is fixed only to ~2 dex by the
inner profile. The coefficient 3.654 is exact.

`M_J ∝ rho_c` **exactly** (K21) because `lam_J` is density-free: `d ln M_J/d ln rho_c = 1.000000`, against
`-1/2` for a standard Jeans mass. This inverts the fragmentation hierarchy — denser regions make *bigger* clumps
— and is the sharpest single consequence of the `Gamma = 2` identification. At the cosmic mean density (12)
gives `M_J = 0.0212 Msun`, and at the (unphysical) `c_s = c` density `3.665e15 Msun`; neither is an object class,
which is another way to see the switch must be the gradient one.

## Status

- **Task 1 — NO-GO(obstruction), with DERIVED sub-results.** (2), (4), (6) and §3 are exact or reproduced (§3 to
  1e-4 of AG6D's `0.980`); rank 2 of 3 with `rho_c` null (K9); no `L*` makes the three coincide (K10, K11;
  minimum spread 3.357 dex at `L* = 1 kpc`). *The obstruction is the three different `L*` exponents (1, 1/2,
  0.6118).* A tuple reproducing the quoted triple exists and is unique — `(24 pc, 3.3347e-8 Msun/pc^3,
  8.3257 km/s)` — but it is a point on the model's own curve, not a solution of a joint fit.
- **Task 2 — NUMERICAL / null.** `r_e/r_M = 22.79 … 54.14`; **0/175** reach it, closest `0.2074` (`UGC09133`).
  No constraint on the census `N`, but the sample requires `N > 10.118` and excludes the fitted `N = 8.296` at
  3 curves, fragile at 1.33x in `M_b`.
- **Task 3 — DERIVED, and CORRECTION of A11 §14.** The switch is `r = L*` (a gradient threshold), `24.018 pc`
  for an MW-like NFW halo at `4.9609 Msun/pc^3`; `R_press <= 0.09` at the innermost SPARC point, `6.09e-4` at
  1 kpc. The superluminality that motivated it does not exist (`c_s = 0.720473 m/s`).
- **Task 4 — DERIVED.** `M_J(r_switch) = 3.654 V_f^2 L*/G = 2.039e4 (V_f/km/s)^2 Msun`: **5.565e8 Msun in
  53.31 pc** for the MW — ultra-compact dwarf / nuclear star cluster; `M_J ∝ rho_c` exactly.

## Checks

`a16_checks.py`: 21 checks, deterministic, stdlib + numpy/scipy/sympy, 1.0 s, no network, exit 0 iff all pass.

| id | proves | measured | threshold |
|---|---|---|---|
| K1 | (2) `c_s^2 = dp/drho` is exactly `2 pi G L*^2 rho` (sympy) | 0 | exactly 0 |
| K2 | `d ln k_J/d ln rho = 0` for `Gamma=2` (1/6 for 5/3) | 0 | 0 |
| K3 | `lam_J = sqrt2 pi L*` at both window ends | 106.6292, 4442.8829 pc | 1e-6 |
| K4, K5 | `sigma = sqrt(a0 L*)`; `lam_FS = 2 sigma/(3H0)` | 8.3257/53.7419 km/s; 82.3502/531.568 kpc | 1e-3 |
| K6 | the growth ODE reproduces AG6D `k_1/2(24 pc)` | 0.97995 | 0.980 to 1 % |
| K7 | the motive's 3.98 dex | 3.9809 dex | 3.98 ± 0.02 |
| K8 | **`c_s/c` at cosmic mean** | 2.4032e-9 | < 1e-6 |
| K9 | Jacobian rank, `rho_c` null | 2 of 3 | 2 |
| K10 | crossings outside the window; `FS/half < 1` | 14.315 Mpc, 4.44e11 pc, 0.0798 | > 1 Mpc; < 0.1 |
| K11 | minimum spread over the window | 3.3568 dex | > 3.0 dex |
| K12 | census inversion reproduces A11's five `N` | 2.1e-15 | < 1e-3 |
| K13 | SPARC sample | 175 curves / 3391 points | 175 / 3391 |
| K14 | fraction reaching `r_e`, closest approach | 0.000 / 0.2074 | 0 / < 0.5 |
| K15 | `max N_min` required by the data | 10.118 | 5 … 20 |
| K16 | curves beyond `r_e(N = 8.296)` | 3 / 175, worst 1.208x | 3 |
| K17 | `M_b` inflation that clears that violation | 1.327x | 1.3 … 1.7 |
| K18 | `r_switch` in an MW-like NFW halo | 24.018 pc | 24 pc to 1 % |
| K19 | innermost SPARC radius vs `r_switch`, `R_press` there | 0.080 kpc (3.3 L*), 0.0900 | > 3 L*; < 0.10 |
| K20 | `M_J(r_switch)`, `R_TF`, `r_eff` | 5.565e8 Msun, 53.31, 32.34 pc | 1e8…1e9; 53.31 |
| K21 | `d ln M_J/d ln rho` | 1.000000 | exactly 1 |

## What this does not do

1. **It does not derive `L*`** and does not narrow `[24 pc, 1 kpc]`; it does not fix `N` either — the census `N`
   is inherited from CFG416, §5 shows the edge test cannot see it at SPARC radii, so `N > 10.118` is a floor.
2. **`k_1/2` is cosmology- and IC-dependent**: AG6D's IC-slope sensitivity is `0.665–1.050 Mpc^-1` at 24 pc
   (factor 1.58); I reproduce their fiducial (`h = 0.677`, `Omega_m = 0.31`, slope 1). The 3.98 dex is robust.
3. **The free-streaming length is an O(1) convention** (`2/(3H0)`, EdS, constant dispersion); a decaying relic
   changes the coefficient, not the ordering. **`M_b(<r_max)` is enclosed, not total**, so `r_M` is low by
   10–20 % and `N_min` is an upper bound — the `N = 8.296` exclusion is fragile (1.33x in `M_b` clears it).
4. **`c_s` and the switch use `K = 4 pi G`** (AG6D). With BRIEF §1's `K = 8 pi G`, `c_s^2` doubles and
   `lam_J = 2 pi L*` instead of `sqrt2 pi L*` (+41 %); `r_switch` moves to `sqrt2 L*` and `M_J` halves. The
   conclusion (subluminal, `r_switch ~ L*`, no RAR conflict) is unchanged; the numbers are not.
5. **§7's `M_J` uses the law's own flat-curve profile**; NFW gives `3.149e6 Msun`, so the class is GC-to-UCD. The
   coefficient in (12) is exact; the density is a model choice, and the edge is untested beyond `5 r_M`.

## Next

1. **The half-mode reading is a self-consistency problem, not a data problem.** `M_1/2 = 5.442e12 Msun` at 24 pc
   is 15x the largest baryonic mass in the SPARC sample whose curves define `a0` — a `Gamma = 2` cold sector
   carrying the stiffness erases the objects it is calibrated on. Either the stiffness misses the free medium
   (AG6D's escape: switch on below `z ~ 3.7e3`), or `L*` is not a medium property.
2. **Retract A11 §14 and its dependants** (`c_s = 0.72 c`, the `0.91` of the window being superluminal, the
   `394x` galactic ceiling). Corrected, the `Gamma = 2` pressure passes every causality test and A11's Task-2
   no-go loses its second leg; its barotropic and contact-term arguments (§16 there) stand alone.
3. **The measurement that decides §5 is unchanged and is not SPARC**: a Keplerian turnover at `50–500 kpc`, or
   the Local Group zero-velocity surface, read as `N = (r_t/r_M) - 1/2`. The floor `N > 10.118` puts the turnover
   beyond `10.6 r_M` — `100.25 kpc` for a `6e10 Msun` galaxy (`r_M = 9.4526 kpc`), A11's target with a one-sided
   bound now attached.
