# A56 — WHERE `L*` COMES FROM, and a guard that stops constant-juggling

Lane A56. `a56_checks.py` (25 checks, 25/25 PASS, exit 0, 17 s), `a56.out`, `a56_results.json`,
`MUTATE.md` + 5 mutation outputs. SI. Constants: BRIEF §4, plus `sigma_c = 8.33 km/s` (A20 cand. 1)
and `sigma_th = 8.23 km/s` (10⁴ K, μ = 1.22). Inputs read first: THEORY §3.4 and §6, A20, A37, A16, A33.

## Claim

**`L*` is one algebraic object with four spellings, and only the spelling that consumes the cold
medium's velocity dispersion predicts a number.**

    L*^2 := 2 gamma / K  =  2 hbar^2/(m_P^2 c^2)  =  (sigma_c/c)^2 L_MOND  =  (sigma_c/c)^2 ell_1/kappa     (1)

All four agree to `2.2e-16` (K7). Consequences, in order of cost:

1. **`L*` is a definition, not a derivation, inside the action.** A33 row 7 says it: `gamma = K L*^2/2`
   is the definition of `L*`. Every length in the census that lands in A20's window `[24, 90] pc` is a
   multiple of `L*` (K13, K15b).
2. **The Compton reading is off by √2, and fixing that costs luminality.** The P Compton length is
   `lambda_P = sqrt(eta/K) = 16.99 pc` — **29.2 % below A20's floor** (K4). The theory's closure `eta = gamma`
   gives `L* = sqrt(2) lambda_P`, i.e. `L*` is *not* the Compton length; and `(L*/lambda_P)^2 = 2 c_s^2`, so
   identifying `L*` with the Compton length requires `eta = 2 gamma`, hence `c_s^2 = 1/2` and the exact
   luminality of A3/A33 K9 is lost (K2). The two readings are mutually exclusive.
3. **No vacuum combination reaches the window.** An exponent census (`|e| <= 2`) over `{c, hbar, G, a_0, Lambda}`
   gives 6 distinct lengths, none in `[24,90] pc`, the nearest **7.11 dex** away
   (K10); adding the cosmic cold density gives 29 lengths and still nothing, nearest 4.91 dex (K11). The
   nine-decade gap of THEORY §3.3 is not bridged by any vacuum quantity.
4. **Exactly one parameter-free combination lands in the window**: `sigma_c^2/a_0 = 24.025 pc` (K12). It
   contains no free coefficient — only the measured dispersion, `a_0`, and (in the `ell_1` form) `Lambda` and `kappa`.
5. **The guard.** Three readings: R1 action-fixed (`L*` constant), R2a local density (`L* ~ rho_c^-1/2`),
   R2b virial density. R1 gives **0.000 dex** across a dwarf, an MW-like galaxy and a cluster; R2a gives
   **2.06 dex** with a definite sign (57.7 pc / 24.0 pc / 2748 pc); R2b gives 0.014 dex but has no coefficient
   that produces 24 pc — the unique `{G, c, rho_c}` length is **25.0 Gpc**, 8.44 dex high (K16–K20).
6. **The data do not decide between R1 and R2a.** Both dwarf cores sit under A20's bound: 53 pc (27 % of
   `R0.3 = 200 pc`) versus 128 pc (64 %) (K19). What kills R2a is internal: a density-dependent stiffness
   changes the coefficient of `d'` from `gamma` to `gamma + 3 gamma' d`, so the exact first integral
   `g = g_N + u` — the theory's one exact result — is a property of **constant** `gamma` (K8). R2a is a
   different action, not a reading of this one.
7. **`sigma_c` from the identity**: `8.330 km/s` (canonical `a_0`) or `9.153 km/s` (alt). Against the 10⁴ K
   thermal width: **1.012** at μ = 1.22, and `9.153` is the **μ = 1.00** width (9.085 km/s) to 0.7 % (K22, K23).
   So (1) inverts to the cold phase's temperature. `L*` is derived from `sigma_c`; `sigma_c` is atomic physics.

**One sentence.** `L*` is the P field's stiffness length — the distance over which a medium moving at
`sigma_c` coasts against `a_0`, equal to `(sigma_c/c)^2 L_MOND = 24.03 pc` for `sigma_c = 8.33 km/s` — derived
from that dispersion with no free parameter, while the dispersion itself is *not* derived by the theory
(the P sector contains no velocity at all: K9, K15).

## Derivation

### 1. The P sector owns exactly one length

With `K = 4 pi G` (A33 §1.1), `u = K|P|`, `d = D_iP^i`, the gradient sector is
`-(gamma/2)d^2 - (gamma/4)F^2 + (eta/2)E^2`. Two dimensionful coefficients, `eta` and `gamma`, both `[L^2]`.
The static linear response is `gamma grad^2 d - K d = ...`, so its range is

    lambda_P = sqrt(eta/K),        L* = sqrt(2 gamma/K) = sqrt(2 gamma/eta) lambda_P.          (2)

`eta` is free and bounded (`eta >= gamma`); `gamma` is *defined* by `L*`. Hence:
- `eta = gamma` (the one-stiffness closure, THEORY §3.4): `c_s^2 = 1` exactly, `L* = sqrt(2) lambda_P = 24.03 pc`,
  `lambda_P = 16.99 pc`, `m_P = hbar/(c lambda_P) = 6.71e-61 kg`, `m_P/H_0 = 2.618e8` (A22: 2.62e8).
- `eta = 2 gamma` (the only choice making `L*` *the* Compton length): `c_s^2 = 1/2`, `L* = lambda_P`, and exact
  luminality is lost. `(L*/lambda_P)^2 = 2 c_s^2` identically.

So "is `L*` a Compton length?" has the answer: **it is a Compton length up to the factor the action's own
`eta/gamma` freedom supplies (1 to √2), and the theory's luminality picks √2, not 1.** Neither value is a
derivation of the number; both are the same coefficient.
### 2. Task 1 — the census: every combination with dimensions of length

Exponents `{-2,-1,-1/2,0,1/2,1,2}` over the theory's quantities; each entry is a distinct monomial whose
dimension is exactly length (K10–K15b). Representative values, SI:

| combination | value | in `[24,90] pc`? |
|---|---|---|
| `L_MOND = c^2/a_0` ; `ell_1 = sqrt(8 pi/Lambda)` (**the site spacing**) | 31.12 / 15.57 Gpc | no, 11.1 / 10.8 dex |
| `1/sqrt(Lambda)`, `c/H_0`, `r_H`, `a_0/(c^2 Lambda)` | 3.11 / 4.45 / 5.38 Gpc / 310 Mpc | no, ≥ 8.5 dex |
| `l_Pl = sqrt(hbar G/c^3)` | 1.62e-35 m | no |
| `c/sqrt(G rho_c)` (unique `{G,c,rho_c}` length, at the cosmic mean) | 25.03 Gpc | no, 8.44 dex above 90 pc |
| `sigma_c/H_0` | 124 kpc | no, 3.1 dex |
| `c_s^2/a_0` (elastic) | 1.80e-7 pc | no |
| `c_s/H_0` (elastic) | 10.70 pc | no, 0.45 L* |
| `hbar/(m_P c)` = `sqrt(eta/K)` = `lambda_P` | **16.99 pc** | **no — 29.2 % below the floor** |
| `(c_s/c) ell_1` | 37.45 pc | yes, = 1.559 L* |
| `sqrt(gamma/G)` | 60.22 pc | yes, = 2.507 L* |
| `c_s c/a_0` | 74.86 pc | yes, = 3.116 L* |
| `sqrt(2 gamma/K)` = `sqrt2 hbar/(m_P c)` = `sigma_c^2/a_0` = `(sigma_c/c)^2 ell_1/kappa` | **24.025 pc** | yes, the definition |

`c_s = sqrt(gamma rho_c) = 0.7212 m/s` is the P sector's *elastic* speed at the cosmic cold density (A16's
0.720473; 0.1 % from rounding). Two facts decide the census:

- **The site spacing cannot be the stiffness scale.** Every length built from `ell_1 = 15.57 Gpc` alone is
  horizon-scale; it enters `L*` only as `(sigma_c/c)^2 ell_1/kappa` — suppressed by the medium, not the lattice.
- **The window is wider than the coefficient.** `90/24 = 3.75`, and the in-window entries are `L*` times
  `1.000, 1.559, 2.507, 3.116` (K15b). Every O(1) rescaling of `L*` from 1 to 3.1 fits inside the window.
  **A20's window can never select the coefficient** — that is exactly why the derivation has to be an
  identity (1) and not a match to a number.

### 3. The one combination with no free parameter

`L* = (sigma_c/c)^2 ell_1/kappa = (sigma_c/c)^2 L_MOND`. At `kappa = ell_1/L_MOND = 0.500311` (0.06 % from ½,
A37 K10) it returns 24.025 pc; at `kappa = ½` exactly, 24.040 pc. Inputs: `Lambda` (measured), `kappa`
(measured, 0.87σ), `sigma_c` (measured or thermal). **No coefficient of the action appears** — that is the
answer to "which one gives 24–90 pc without a free parameter", and it is (1) again.

### 4. Task 2 — the guard: constant or environment-set?

Three halos under the frozen law, `f_c = F/(1+F)`, `F = (sqrt(1+4/y)-1)/2`, `y = g_N/a_0` (A20's
construction). Dwarf and MW: Hernquist baryons (`M_b = 1e8, a = 0.7 kpc`; `6e10, 1.5 kpc`, A20's frozen
models). Cluster: β-model gas (`M200c = 1.483e14`, `c = 4.5`, A43's stack; `M_bar = 0.13 M200`,
`r_c = 0.15 R500`, A41's cored baryons). Halo mass spans `6.4e8` to `1.48e14 M_sun` = **5.4 decades**
(more than the three asked).

| halo | `M200` | `rho_c(24 pc)` | `f_c` | R1 `L*` | R2a `L*` | R2b `L*` | R1 `R_core` | R2a `R_core` |
|---|---|---|---|---|---|---|---|---|
| dwarf | 6.4e8 | 4.888e-20 | 0.590 | 24.03 pc | **57.7 pc** | 24.03 pc | 53.4 pc | 128.2 pc |
| MW-like | 3.8e11 | 2.822e-19 | 0.0247 | 24.03 pc | **24.0 pc** | 24.03 pc | 53.4 pc | 53.4 pc |
| cluster | 1.48e14 | 2.157e-23 | 0.9935 | 24.03 pc | **2748 pc** | 24.82 pc | 53.4 pc | 6104 pc |
| **spread** | 5.4 dex | 4.1 dex | — | **0.000 dex** | **2.06 dex** | 0.014 dex | 0 | 114× |

- **R1 (action-fixed / Compton).** `gamma` is a constant of the action, so `L*` is a constant of the medium:
  the core radius is **the same in a dwarf, a spiral and a cluster**, and only the *depth* varies with `f_c`
  (A20: 1.21 % MW, 35.8 % dwarf). Sharp, and untested.
- **R2a (local density).** `L* ~ rho_c^-1/2` — bigger where the medium is thinner — normalised so the MW-like
  halo has 24.03 pc (its most generous calibration). Under the frozen law the cold density at 24 pc spans
  only 4.1 dex (the phantom tracks the baryons), so `L*` spans 2.06 dex: **dwarf 57.7 pc, cluster 2.7 kpc**.
  Prediction: cores are a dwarf phenomenon *in radius as well as depth*, and clusters carry a 6 kpc core.
- **R2b (virial density).** All virialized halos share the mean density `200 rho_crit`, so this reading is
  **constant by construction** (0.014 dex), indistinguishable from R1 — but the only `{G, c, rho_c}` length is
  `c/sqrt(G rho_c) = 25.0 Gpc` (K20), so to get 24 pc it must import `L*` itself. R2b is R1 with a free normalization.

**Against A20's measured cores.** A20 measured one thing and bounded another: no core detection anywhere
(0/175 SPARC curves reach 24 pc; the floor is 80 pc = 3.33 L*), and `L* <= 90 pc` from IC_10's turnover
(`R_core <= R0.3 = 200 pc`). R1's dwarf core is 53 pc (27 % of the bound); R2a's is 128 pc (64 %). **Both
survive.** The data show no variation; R1 requires none; R2a requires 2.06 dex but hides 0.9 dex of it
inside the only measured system. The guard therefore does **not** close on data — it closes on the action:
R2a needs `gamma = gamma(rho_c)`, and then the EL equation's `p''` coefficient is `gamma + 3 gamma' d` instead
of `gamma` (K8), so the first integral `g = g_N + u` (A33 §5, residual 0) stops being exact. R2a is not
available without changing the action.

### 5. Task 3 — `sigma_c`, and whether the medium gives it

    L*/L_MOND = sigma_c^2/c^2   (exact, A37 K4)   =>   sigma_c = c sqrt(L*/L_MOND) = sqrt(a_0 L*).      (3)

| footing | `a_0` | `L_MOND` | `sigma_c` | `/8.226 km/s` (μ=1.22) | `/9.085 km/s` (μ=1.00) |
|---|---|---|---|---|---|
| canonical | 9.36e-11 | 9.6021e26 m | **8.330 km/s** | **1.012** | 0.917 |
| alt / P3 | 1.13e-10 | 7.9536e26 m | **9.153 km/s** | 1.113 | **1.007** |

The identity inverts to the 10⁴ K thermal width at **1.2 %** on the canonical footing, and on the theory's
own `a_0 = 1.132e-10` it inverts to the **μ = 1.00** (pure hydrogen) width at **0.7 %**. The 20 % `a_0` gap
(10 % in `sigma_c`, which goes as `sqrt(a_0)`) is entirely the helium mass fraction. That is not a coincidence you can tune: `(3)` fixes `sigma_c` from
`L*` and `a_0` alone, and both footings land on a 10⁴ K hydrogen width.

Does the medium's microphysics give `sigma_c`? **No, and this is provable in one line.** The A2 lattice's
occupancy is `theta = x/(1+x)` with `x = exp[beta(mu+eps)]`, `mu = k_BT ln(g/a_0) - eps`; the temperature
cancels identically, `d theta/dT = 0` (K9), leaving `theta = g/(g+a_0)`. The P sector is **velocity-blind**:
its only content is `a_0` and the response function. A velocity census over `{c, hbar, G, a_0, Lambda}` gives
7 velocities — `c`, `0.0998c`, `(a_0^2/Lambda)^{1/4} = 0.3159c`, and Planck-scale values — the nearest to
`sigma_c` being `0.0998c`, **3.56 dex away** (K15). `sigma_c/c = 2.78e-5` is not a vacuum number.

## Verdict

**`L*` is the stiffness length of the P field — `(sigma_c/c)^2 L_MOND`, the distance over which a medium at
the cold sector's dispersion coasts against `a_0` — derived from `sigma_c` with no free parameter, and
`sigma_c = 8.33 km/s` is the 10⁴ K thermal width of the cold phase, which the P sector does not produce.**

**The pre-registered observation that kills the derivation.** It is a *ratio*, so no absolute calibration
enters: two dwarfs of equal `M_b` whose Hernquist scale radii differ by 2× (central cold densities 2.94×
apart, 4.888e-20 vs 1.661e-20 kg/m³) must have **the same** turnover radius, `r_sw = 18.46 pc` in both,
under R1; R2a predicts 36.01 pc in the second (K21). Measure the turnover in both with `ngVLA` at 0.15″
(2.9 pc at 4 Mpc; 7 % of 18.5 pc = 0.067″):

- **measured ratio in `[0.85, 1.18]`** → constant `L*` survives, R2a dead;
- **outside it** → the derivation above is dead and `L*` is an environment-set length, not a medium constant.

Secondary, same pre-registration: a cold-phase dispersion outside `7.6–9.3 km/s` (`L*` outside `20–30 pc`)
breaks the 10⁴ K identification while leaving (3) intact; a dwarf core beyond 200 pc is already excluded.

## Status

- **Task 1 — DERIVED (the census is exhaustive, the answer is an identity).** One object, four spellings,
  agreeing to 2e-16; the Compton length is 16.99 pc and is *not* `L*` (√2 off, and closing the √2 costs
  `c_s^2 = 1/2`); no vacuum or density combination reaches the window (7.11 / 4.91 dex); the unique
  parameter-free in-window combination is `sigma_c^2/a_0`.
- **Task 2 — DECIDABLE + NO-GO(action-internal).** R1 = 0.000 dex, R2a = 2.06 dex, R2b = 0.014 dex and
  valueless. The data do not separate R1 from R2a (27 % vs 64 % of A20's core bound); R2a is excluded
  inside the theory because `gamma(rho_c)` changes the P equation and destroys the exact law.
- **Task 3 — DERIVED(sigma_c), with `sigma_c` external.** 8.330 / 9.153 km/s vs 8.226 / 9.085 km/s thermal
  (1.012 / 1.007); the P sector is velocity-blind by `d theta/dT = 0`, so the chain terminates at 10⁴ K.
- **Parameter count.** `L*` is one of A33's four finite free parameters and FINAL_THEORY's "one free scale".
  Under this lane it becomes `(sigma_c/c)^2 L_MOND`, so the free list is `(kappa, beta, sigma_c)` — **three**,
  with `L*` traded for one astrophysical temperature. If 10⁴ K is refused as an input, `L*` stays free and
  nothing is gained; that is the honest fork.

## Checks

`a56_checks.py`, 25/25 PASS, exit 0, 17 s, stdlib + numpy + sympy, deterministic, no network.

| id | proves | measured | threshold |
|---|---|---|---|
| K1 | `L*^2 = 2 gamma/K` (definition) | residual 0 | exactly 0 |
| K2 | `L*/lambda_P = sqrt(2gamma/eta)`; `(L*/lambda_P)^2 = 2 c_s^2` | 1.41421 / 1.00000 / 0.70711 | exact |
| K3 | `L* = sqrt2 hbar/(m_P c)`; `m_P/H_0` | residual 0 ; 2.6182e8 | 0 ; 2.62e8 ± 1 % |
| K4 | the Compton length misses the window | 16.988 pc, 29.2 % low | < 24 pc by > 25 % |
| K5 | `L*/L_MOND = sigma_c^2/c^2` | 7.720556e-10 (−9.1124 dex) | exact |
| K6 | `L* = (sigma_c/c)^2 ell_1/kappa_c` | 24.0250 pc (κ=½: 24.0400) | 0 ; 0.06 % |
| K7 | the four spellings agree | spread 2.2e-16 | < 1e-6 |
| K8 | `gamma(rho)` changes the `p''` coefficient | `gamma_0 + 3 gamma_0 m q/rho_0` | nonzero for m≠0 |
| K9 | the lattice is temperature-blind | `d theta/dT = 0` exactly | 0 |
| K10 | vacuum census | 6 lengths, 0 in window, 7.11 dex | 0 ; > 6 dex |
| K11 | + `rho_c` | 29 lengths, 0 in window, 4.91 dex | 0 ; > 4 dex |
| K12 | + `sigma_c` | exactly 1: 24.025 pc | 1 ; 24.025 pc |
| K13 | + `gamma` | 1 entry (60.22 pc); 2 of 3 normalisations in window | straddles the floor |
| K14 | + `m_P` | 0 in window; Compton 16.988 pc | 0 |
| K15 | vacuum velocity census | 7 velocities, nearest 3.56 dex | > 3 dex |
| K15b | the window vs O(1) multiples | 3.75 wide; entries 1.000–3.116 × L* | max < 3.75 ; > 3.0 |
| K16 | R1 across three halos | 24.025 pc each, 0.000 dex | 0.000 dex |
| K17 | R2a across three halos | 57.7 / 24.0 / 2747.8 pc, 2.06 dex | > 1.5 dex |
| K18 | R2b (virial) | 24.03 / 24.03 / 24.82 pc, 0.014 dex | < 0.05 dex |
| K19 | both readings vs A20's core bound | 27 % / 64 % of 200 pc | both < 200 pc |
| K20 | the density route's only length | 25.033 Gpc, 8.44 dex high | > 4 dex |
| K21 | the differential test | `rho` ratio 2.94 → `r_sw` ratio 1.95 | R2a > 1.6 |
| K22 | `sigma_c` from (3), both footings | 8.330 / 9.153 km/s → 1.012 / 1.112 | ± 0.02 |
| K23 | thermal route to `L*` | 8.226 km/s → 23.43 pc (alt 19.40) | 8.23 ± 1 % ; in window |
| K24 | the nine-decade hierarchy | 9.1124 dex; vacuum 7.1 dex away | 9.11 ± 0.01 ; > 6 |

## What this does not do

1. **No detection.** No galaxy on disk resolves 24 pc; A20's null stands. This lane re-derives the number.
2. **The cluster leg is a model, not data.** `rho_c(24 pc)` in a cluster comes from a β-model
   (`M_bar = 0.13 M200`, `r_c = 0.15 R500`); the 2.7 kpc prediction is model-dependent at factor 2. The
   dwarf–MW contrast (2.4×) is robust; the cluster factor (114×) is not.
3. **R2a is not excluded by data**, but by the action (K8). Against a different action with `gamma(rho_c)`,
   R2a is live again and the differential test of §Verdict is the only arbiter.
4. **`f_c` at 24 pc is a model choice** (Hernquist/β-model + frozen law), as in A20; the *ordering*
   (dwarf `f_c` = 0.59 ≫ MW 0.025) and the *sign* of R2a's variation are not.
5. **The 10⁴ K identification is not a theorem.** One astrophysical number inverts (3) to 1.2 % on one
   footing and 0.7 % on the other. A cold phase at 3×10⁴ K triples `L*` and breaks the 90 pc bound — that is
   the falsifiable content, not a derivation. `kappa` likewise stays measured (24.04 vs 24.025 pc).

## Next

1. **Run the differential test.** `ngVLA` 0.15″ on two dwarfs of equal `M_b` and 2× different scale radius;
   the statistic is `r_sw(2)/r_sw(1)`, prediction 1.00 (R1) vs 1.95 (R2a); 7 % radius precision suffices and
   no absolute calibration enters.
2. **Measure `sigma_c` directly.** A face-on dwarf's velocity dispersion at 30–100 pc (Hα or 21 cm) fixes
   `L*` through (3) with no core modelling at all: `L* = sigma_c^2/a_0`. 10 % on `sigma_c` is 20 % on `L*`.
3. **Do not re-derive the Compton reading.** It is 16.99 pc; 24 pc needs the √2 that luminality supplies, so
   any future text writing `L* = hbar/(m_P c)` is off by 41 %.
4. **Retire the window as a derivation tool.** `[24,90] pc` admits every O(1) multiple of `L*` from 1 to 3.1
   (K15b); it can falsify, never derive. The derivation is (1) or nothing.