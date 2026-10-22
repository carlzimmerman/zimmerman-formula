# A53 — the medium: three candidates, the next-order coefficient, and a discriminator that is not the RAR

Lane A53, `deepseek_push/DS_FINAL_2026_10_21/`. Reads `THEORY.md` §3.5, `A2_medium/report.md`,
`A35_series_parallel/report.md`, `A7_discriminator/report.md`. Inputs: `a0 = 9.36e-11 m s^-2`
(canonical footing, as A2/A35; the theory's own `1.132e-10` scales every absolute acceleration
below and changes no ratio), `c`, `G`, `M_sun` (IAU nominal), `kpc`, `AU`, `yr`, and the P-sector
mass `m/H0 = 2.620985e8`, `lambda_P = 16.971 pc` (THEORY §3.4, A22). Every algebraic statement is
a sympy remainder in `a53_checks.py`; every number is in `a53_results.json`.

## Claim

The three media are **not** three ways of writing one law. They are separated at *leading* order
by the parity of the free energy, and only one of them survives:

1. **The law's deep expansion is not `1 - (1/4)(g_N/a0)`.** Exactly,
   `g = sqrt(a0 g_N)[1 + (1/2)sqrt(g_N/a0) + (1/8)(g_N/a0) + O(y^{3/2})]`. The coefficient of the
   first correction is **+1/2 at half order**; the first *integer*-order coefficient is **+1/8**.
   `-1/4` is not a coefficient of the law, of n=2, or of any of the three media; `+1/4` is the
   coefficient of the *standard* interpolation `mu = x/sqrt(1+x^2)`, with the opposite sign. The
   prompt's number is a mis-transcription, and a check (K2, K2c) shows why it cannot be right: in
   powers of `g_N/a0` alone the coefficient **diverges** as `y^{-1/2}`, so a finite coefficient of
   `y` exists only if the half-power term is kept.
2. **Parity is the static discriminator.** Any medium whose free energy is even in its order
   parameter (`A -> -A`, i.e. `P -> -P` or `E -> -E`) has an **odd** `g_N(g)`, hence no `g^2` term,
   hence a deep limit that is *linear* (BI, or a sub-critical Langevin dielectric) or *cube-root*
   (a critical Langevin dielectric) — never `sqrt(a0 g_N)`. The Langevin dielectric and
   Born–Infeld are both even; the one-sided hard-core lattice is not. This is a statement about
   the exponent, not about a fit.
3. **Capacity/affinity is the number that encodes the medium.** The law needs `C = s = a0`
   (ratio 1). The Langevin dielectric has `C/s = 3` — the factor is `3 chi_0`, fixed by
   `<cos^2 theta> = 1/3` in three dimensions, and *cannot* be tuned to 1 while keeping a
   non-linear deep limit. BI has no capacity at all (`C = infinity`: the response grows linearly
   while the field is capped). The lattice has `C/s = 1`, and `N` occupants per site give
   `C = s = N a0` — the law with `a0 -> N a0`, i.e. `N` is a **modulus**, not a shape parameter.
4. **Only Born–Infeld can produce a maximum acceleration**, because only BI caps the *field*.
   A dielectric caps its *polarisation* and a lattice caps its *occupancy*, but in both cases the
   conjugate field `g = F'(A)` diverges at the cap, so `g` is unbounded — which is what the law
   does. BI's cap is at `E_max`: `1.0 a0` if tied to the MOND scale (excluded by 8.6 decades of
   Solar-System data), or `> 4.23e8 a0` if tied to Mercury's orbit (and then BI is Newtonian
   throughout the MOND regime). Either way BI is excluded.
5. **The dynamics gives a discriminator, but not a measurable one.** The three response functions
   are Debye `1/(1-i omega tau)`, retarded `cos(omega L/c)`, and gapped
   `1/(1-omega^2/(omega_g^2+c^2k^2))`. In the deep regime the fractional shift of the predicted
   `g` at fixed `g_N` is `-(a0/2g) x^2` (dielectric and BI) and `+(a0/2g) x_L^2` (lattice): the
   **sign** separates the lattice from the other two, and the **quadrature part** separates the
   dielectric from both. But the dielectric's shift is bounded by its own drag
   (`t_decay/T = 1/(4 pi x)`: a 1% shift means the orbit dies in 0.8 periods), and the two
   reactive media are bounded by `(v/c)^2`. At the requested frequencies and at the real orbital
   frequencies of wide binaries, galaxies and clusters, **no medium reaches a measurable
   frequency dependence**; the largest number anywhere is the dielectric at its survival limit in
   a cluster, `5.2e-3`, at the edge of the systematic floor.
6. **The action selects the one-sided lattice with luminal, gapped dynamics.** `W(u)` has a
   one-sided pole at `u = a0` (capacity, hard core); the P-sector kinetic term is second order in
   time, so `c_s^2 = 1` and there is **no** first-order (Debye) term; the P mass gives a gap at
   `f_gap = 9.11e-11 Hz`. BI's statics is even, the dielectric's is even and dissipative: neither
   is in the action.

## 1. The expansion the law actually has

With `x = g/a0`, `y = g_N/a0`, `A = g - g_N = a0 x/(1+x)`, `g_N = g^2/(g+a0)`, the exact ratio is

```
g/sqrt(a0 g_N) = x/sqrt(y) = sqrt(1+x)                                   (1)
             = 1 + x/2 - x^2/8 + x^3/16 - ...   (in x)
             = 1 + (1/2) sqrt(y) + (1/8) y + O(y^{3/2})   (in y).        (2)
```

The reversion is exact (K2, sympy, `alpha=1, beta=-1, gamma=1`). Two consequences:

* the first correction is **half-order**, `+1/2 sqrt(y)`;
* the first integer-order coefficient is **+1/8**.

Neither is `-1/4`. The distance from the prompt's value is `0.75` in the half-order coefficient
and `0.375` in the integer-order one (K2). `-1/4` is not a near miss of the right series; it is
the wrong series. If one insists on writing `g = sqrt(a0 g_N)(1 + c y)` with no half-power, then
`c` is not a constant: `(g/sqrt(a0g_N) - 1)/y` takes the values `500.1, 5000.1, 50000.1` at
`y = 1e-6, 1e-8, 1e-10` — it diverges as `y^{-1/2}` (K2c, decade ratio 10.0). A finite `c`
exists only with the half-power term present.

The number `1/4` does live one door down: the *standard* interpolation `mu = x/sqrt(1+x^2)` has
`g/sqrt(a0g_N) = (1+x^2)^{1/4} = 1 + y/4 + ...`, with **+1/4** (K3). The prompt's `-1/4` is that
number with the sign flipped.

### The one-scale theorem, and the next-order coefficient as a fingerprint

Let a medium have a single scale, `A = C f(g/s)`, with `f(0)=0`, `f'(0)=1`, and suppose the deep
limit is to be `sqrt(a0 g_N)`. Expanding `g_N = g - C f(g/s)`:

```
g_N = g (1 - C/s) - (C/2s^2) f''(0) g^2 - (C/6s^3) f'''(0) g^3 + ...        (3)
```

The linear term must vanish, so `C = s` **exactly**; then, in the physical variable
`y = g_N/a0` with `a0 = -2s/f''(0)`,

```
a0 = -2s/f''(0),    c_half = f'''(0)/(3 f''(0)^2),
g = sqrt(a0 g_N)[1 + c_half sqrt(y) + c_one y + ...].                        (4)
```

The law (`f = x/(1+x)`, `f'' = -2`, `f''' = 6`) gives `c_half = 1/2`, `c_one = 1/8`. A
one-parameter family `f_p(x) = [1-(1+x)^{-p}]/p` (p=1 is the law) shows the coefficient is
computable and medium-dependent (K4; `a0/s = 2/(p+1)` differs from 1 for `p != 1`, and the
normalisation matters):

| p | 1 | 2 | 4 | 8 |
|---|---|---|---|---|
| `c_half` (measured) | 0.5000 | 0.4444 | 0.4000 | 0.3704 |
| `(p+2)/(3(p+1))` | 0.5000 | 0.4444 | 0.4000 | 0.3704 |
| `c_one` | 0.1250 | 0.1235 | 0.1200 | 0.1166 |
| `a0/s` | 1.000 | 0.667 | 0.400 | 0.222 |

So "the next-order coefficient" is real and it is a shape fingerprint — but across this family it
moves only between 0.37 and 0.50 (a 15% effect), and A7 has already shown that the RAR shape at
this order is not measurable in SPARC. It is a theoretical label, not a discriminator.

## 2. Candidate (a): a saturating Langevin dielectric

**Free energy.** `N` dipoles of moment `p` at temperature `T` in field `E`, `z = pE/kT`:

```
F = -N kT ln[sinh(z)/z],    P = -dF/dE = N p L(z),   L(z) = coth z - 1/z.     (5)
```

As a function of the order parameter, `F(P) = NkT[zL(z) - ln(sinh z/z)]` with `z = L^{-1}(P/Np)`,
and `dF/dP = (kT/p) z = E` **exactly** (K7). So with `A <-> P`, `g <-> E`:

```
g = g_s L^{-1}(A/A_max),   g_s = kT/p,   A_max = N p,   chi_0 = A_max/(3 g_s).   (6)
```

**Force law.** `g = g_N + A` with `A = A_max L(g/g_s)`, i.e. the implicit

```
g_N = g - A_max L(g/g_s).                                                    (7)
```

**Deep limit.** `L(z) = z/3 - z^3/45 + 2z^5/945 - ...`:

```
g_N = g(1 - chi_0) + A_max g^3/(45 g_s^3) + O(g^5).                          (8)
```

* If `chi_0 < 1`: `g = g_N/(1-chi_0)` — **linear**, no MOND.
* If `chi_0 = 1` exactly (the only critical tuning): `A_max = 3 g_s`, and
  `g_N = (3/5) g^3/a0^2` with `g_s = a0/3` — a **cube root**, `g = (5/3)^{1/3} a0 y^{1/3}`,
  exponent `1/3`, coefficient `0.600000` (K8).
* If `chi_0 > 1`: `g_N < 0` at small `g` — anti-gravity, excluded.

**Capacity/affinity.** `C = A_max`, `s = g_s`, and at criticality `C/s = 3` (K9). The factor is
`3 chi_0 = Np^2/(kT)`: it is the three-dimensional average `<cos^2 theta> = 1/3`, and it is
**not adjustable** once `chi_0 = 1`. The law needs `C/s = 1`.

**Saturated limit.** `L(z) = 1 - 1/z + ...`, so `A = A_max - A_max g_s/g` and

```
g = g_N + a0 - (a0^2/3)/g_N + ...      (law: g_N + a0 - a0^2/g_N + ...)       (9)
```

The constant anomaly matches (`A -> a0`, K10) but the approach coefficient is `-1/3` instead of
`-1`. At `g = a0` the medium transmits `g_N = 0.3284 a0` (its response is `A = 0.6716 a0`),
against the law's `0.5 a0` — a 34% shortfall at the knee.

**No maximum acceleration.** `g = g_s L^{-1}(A/A_max)` diverges logarithmically as
`A -> A_max`; `g_N = g - A -> infinity`. At `g_N = 1e9 a0` the medium gives
`g = 1.000000001e9 a0` (K23). The polarisation cap is at `A = A_max = a0`; 50% of it is reached
at `g = 0.6385 a0`, 90% at `g = 3.30 a0` (K24). There is no cutoff in `g`.

**Verdict on (a): NO-GO.** The deep limit is linear for every `chi_0 != 1` and cube-root at
`chi_0 = 1`; no choice of `(A_max, g_s)` gives `g_N ∝ g^2`, because `L` is odd and the `g^2`
coefficient in (8) is identically zero. It is excluded by the *exponent*, before any data.
Langevin–Debye (permanent plus induced moment) does not help: the induced term adds `alpha E^2/2`
to the free energy, which is even, and the permanent-dipole average is even, so `A(g)` stays odd.
The one dielectric that *does* work is the **mean-field** (Curie–Weiss-like) one,
`A = A_max g/(g+g_s)`, which is exactly the Langmuir isotherm (11) — i.e. it is candidate (c) in
disguise. The distinction this lane draws is between *thermal* (Langevin) and *hard-core*
(mean-field) saturation, and only the second is one-sided.

## 3. Candidate (b): a Born–Infeld medium with a maximum field

**Free energy / constitutive pair.** With `E_max = b` and `D = dL/dE`,

```
L(E) = E_max^2 [1 - sqrt(1 - E^2/E_max^2)],   D = E/sqrt(1 - E^2/E_max^2),
H(D) = E_max^2 [sqrt(1 + D^2/E_max^2) - 1],   E = D/sqrt(1 + D^2/E_max^2).   (10)
```

`dH/dD = E` exactly (K11). The field is capped, `E < E_max`; the induction is not.

**Two orientations, both fatal.**

* *Field = observed acceleration* (`g = E`, `g_N = D`): `g = g_N/sqrt(1+(g_N/E_max)^2)`. Then
  `g < E_max` for all `g_N` — a **hard maximum acceleration** (K13) — and `D > E`, so
  `A = g - g_N < 0`: the medium **screens** where the law enhances. At `g_N = a0` (with
  `E_max = a0`) it gives `g = 0.7071 a0`, `A = -0.2929 a0` against the law's `A = +0.6180 a0`
  (K14). Wrong sign *and* a cutoff. The deep limit is `g = g_N - g_N^3/(2E_max^2) + ...`:
  exponent **1**, cubic term `-(1/2) g_N^3/E_max^2` (K12).
* *Field = baryonic acceleration* (`g_N = E`, `g = D`): `A = D - E > 0` and `g` grows without
  bound, but `g_N < E_max` — a cap on the *baryonic* field — and the anomaly is
  `A ≈ g - E_max -> infinity`: BI has **no constant anomaly**, unlike the law's `A -> a0`
  (K10). It still fails the deep exponent.

**Numbers.** With `E_max = a0` (the only scale the MOND problem offers), the maximum relative
deviation from the law over `g_N/a0 in [1e-3, 10]` is **96.9%** (K15), and the response at
`g_N = a0` has the wrong sign (K14). With `E_max` tied to the Solar System — Mercury's orbital
acceleration `3.96e-2 m/s^2 = 4.23e8 a0` — the cap is at `> 4.23e8 a0` and BI is Newtonian
throughout the entire MOND regime. The natural cap `E_max = a0` is excluded by 8.6 decades of
Solar-System accelerations (K24).

**Verdict on (b): NO-GO, doubly.** Even free energy ⇒ odd `g_N(g)` ⇒ exponent 1, not 1/2. And the
field cap is a maximum acceleration the law does not have: the law's `g -> g_N + a0` is unbounded.

## 4. Candidate (c): a finite-capacity lattice with N states per site

**Free energy.** The one-sided lattice gas of A2, with `u = A` and `K W'(u) = g`:

```
K W(u) = a0^2 [-u/a0 - ln(1 - u/a0)],   W'(u) = a0 u/(a0-u) = g,
W''(u) = a0^2/(a0-u)^2 > 0,   pole at u = a0.                                 (11)
```

`W` is **not** even: it has a pole at `+a0` and is real only for `u < a0`. That one-sidedness is
the whole content (K18).

**N states per site, at most one occupant.** With internal energies `eps_i` and activity
`x_i = exp[beta(mu - eps_i)]`, `X = sum_i x_i`:

```
Z = 1 + X,   theta = X/(1+X).                                                (12)
```

This is **exactly Langmuir for every N and every spectrum** (K16, max deviation 0 over N = 1, 2,
5, 11 with random spectra). `N` is absorbed into the affinity: `X = N x` for degenerate levels,
i.e. `s -> s/N`. It is not a shape parameter.

**N occupants per site.** The isotherm is the BET sum,
`theta = x/(1-x) - (N+1)x^{N+1}/(1-x^{N+1})`, whose expansion is
`theta = x + x^2 + ...` — **convex** at the origin, `f''(0) = +2`. With `C = s` this gives
`g_N = -a0 x^2 + ... < 0`: a negative baryonic field (K17, `-9.98e-7 a0` at `x = 1e-3`).
Multi-occupancy is excluded by positivity, for every `N >= 2`.

**N as a modulus.** Capacity `C = N a0` **and** affinity `s = N a0` reproduce the law exactly
with `a0 -> N a0` (K19, max deviation `2.6e-15` over `g_N/a0 in [1e-3, 1e2]`). Capacity `N a0`
with affinity `a0` gives the linear coefficient `1 - N < 0` (K20): no positive deep limit. So the
only consistent lattice is single-occupancy with `C = s = a0`; any `N` is a relabelling of `a0`,
and since `a0` is fixed by the vacuum (P3), `N = 1`.

**Caps.** `theta = 1/2` at `g = a0`; `theta = 0.9` at `g = 9 a0`; `theta -> 1` as `g -> infinity`,
so `g = a0 theta/(1-theta) -> infinity`. **No maximum acceleration** (K23), and the anomaly
saturates at `a0` exactly as the law requires.

**Verdict on (c): the law, for every N, with N unobservable in the static sector.** The lattice is
the only candidate that reproduces the deep exponent, the knee value `g_N(a0) = a0/2` (K36), and
the saturated anomaly.

### 4.1 The three expansions side by side

| medium | deep limit (in `y = g_N/a0`) | leading power | next-order coefficient | saturated limit |
|---|---|---|---|---|
| law / lattice (N=1) | `sqrt(a0g_N)[1 + (1/2)sqrt(y) + (1/8)y + ...]` | `1/2` | **+1/2** (half order), **+1/8** (integer) | `g_N + a0 - a0^2/g_N` |
| (a) Langevin, `chi_0=1` | `(5/3)^{1/3} a0 y^{1/3}[1 + 0.402 y^{2/3} + ...]` | `1/3` | `+0.402` (at `y^{2/3}`) | `g_N + a0 - (a0^2/3)/g_N` |
| (b) BI, `E_max=a0` | `a0[y - (1/2)y^3 + ...]` | `1` | `-1/2` (at `y^3`) | `g -> E_max` (hard cap) |

The law's second coefficient is **`+1/8` at integer order and `+1/2` at half order**; `-1/4` is not
in this table. The Langevin and BI rows have no `O(y)` term at all: their leading power is not
`1/2`, which is the whole point of the parity theorem.

## 5. The structural difference: what caps what

| medium | capped quantity | `g` at the cap | maximum acceleration? | cap in units of `a0` |
|---|---|---|---|---|
| law (reference) | anomaly `A -> a0` | `g -> infinity` | **no** | anomaly saturates at `g ~ few a0` |
| (a) Langevin dielectric | polarisation `A -> A_max = a0` | `g -> infinity` (log) | **no** | 50% at `0.6385`, 90% at `3.30` |
| (b) Born–Infeld | field `E -> E_max` | `g = E_max` | **yes** | `1.0` (a0-tied) or `> 4.23e8` (Mercury) |
| (c) lattice | occupancy `theta -> 1` | `g -> infinity` (`~a0/(1-theta)`) | **no** | `theta=1/2` at `1.0`, 90% at `9.0` |

The structural rule is: **a cap on the response variable does not cap the conjugate field.** For a
free energy `F(A)` with a finite capacity `A_max`, `g = F'(A)` diverges at `A_max` (log for
Langevin, `1/(A_max-A)` for the lattice), so `g_N = g - A -> infinity`. Only a cap on the *field*
itself — BI's `E < E_max` — produces a maximum acceleration. The theory's law has none:
`g = g_N + a0 - a0^2/g_N + ...` grows without bound. So the dielectric and the lattice are
*allowed* by the cap test, BI is not.

## 6. Dynamics: the response functions, and the time-domain test

### 6.1 The three responses

| medium | equation of motion | normalised response `D(omega)`, `D(0)=1` | `x` |
|---|---|---|---|
| (a) Debye dielectric | `tau_D Adot = A_eq(g) - A` | `1/(1 - i omega tau_D)` | `x_D = omega tau_D` |
| (b) Born–Infeld | retarded field, `k = omega/c` | `cos(omega L/c) = 1 - (v/c)^2/2 + ...` | `x_B = v/c` |
| (c) gapped lattice | `(Box + omega_g^2) phi = J` | `1/(1 - omega^2/(omega_g^2 + c^2 k^2))` | `x_L = (v/c)/sqrt(1+(L/lambda_P)^2)` |

For (c), `omega_g = m c^2/hbar = 2.620985e8 H0 = 5.7248e-10 rad/s`, i.e.
`f_gap = 9.111e-11 Hz`, `lambda_P = c/omega_g = 16.971 pc` (K32). For a system of size `L` the
effective gap is `sqrt(omega_g^2 + c^2/L^2)`; for `L >> lambda_P` it is `omega_g`, for
`L << lambda_P` it is `c/L` and the lattice response *coincides* with BI's at leading order.

### 6.2 The shift of the effective law

Scale the in-phase response by `lambda = Re D(omega)`. Then `g_N = g - lambda A(g)`, and at fixed
`g_N`

```
delta g/g = (lambda - 1) A(g) / [ g (1 - lambda A'(g)) ]                      (13)
         -> -(a0/2g) x_D^2        (dielectric; deep regime)                   (14)
         -> -(a0/2g) x_B^2 / 2    (BI; deep regime)                           (15)
         -> +(a0/2g) x_L^2        (lattice; deep regime)                      (16)
```

The exact form (13) matches the solver to `1e-3` (K34, the residual is the `O(d lambda^2)` term);
the deep reduction (14)–(16) matches to 1.1% at `g = 0.0225 a0` (K34b). Two features matter:

* **The deep-MOND regime amplifies by `a0/2g`.** The medium carries almost all of the field there
  (`A -> g`), so a fractional freeze-out `x^2` of the response becomes a fractional shift
  `(a0/2g)x^2` of the observed acceleration — a factor 22 at `g = 0.0225 a0` (the `1e-15 Hz`
  binary), 6 at `g = 0.083 a0`, 0.6 at `g = 0.82 a0` (the cluster).
* **The sign is a medium fingerprint**: negative for the dielectric and BI (the medium lags, the
  anomaly is reduced), **positive** for the gapped lattice (below its resonance the response is
  enhanced).

**A frozen response adds a linear term, not a uniform `a0` shift.** In the deep limit
`g_N = (1-lambda)g + lambda g^2/a0`; the crossover is at

```
g* = (1-lambda) a0/lambda = x^2 a0                                          (17)
```

exactly (K26). Below `g*` the medium is frozen, the law is Newtonian and MOND is off; the linear
branch lies a further four powers down, `g_N ~ x^4 a0` (K26b: at `g_N = 1e-10 a0`, `x = 0.01`, the
exact solution is `g = 9.90e-7 a0` against the linear prediction `1.00e-6`; at `g_N = 1e-5 a0`,
`x = 0.001`, it is `3.167e-3` against the sqrt-law `3.162e-3`). For the lattice `lambda > 1`, so
the linear term is *negative*: there is no solution below `g_min = |1-lambda|a0/lambda`, a
low-acceleration gap rather than a return to Newton.

### 6.3 The three requested frequencies

The requested frequencies are not orbital frequencies of the named systems; they are the
light-crossing frequencies `c/(2 pi L)` of `155 pc`, `15 kpc` and `1.5 Mpc`. For a circular
Keplerian orbit the orbital frequency is smaller by `v/c`. Mapping each frequency to the radius
whose *true* (MOND) orbital frequency `omega^2 = g(r)/r` equals it, for a `1 M_sun` binary:

| `f` (Hz) | period | `r` | `g_N/a0` | `v/c` | regime |
|---|---|---|---|---|---|
| `1e-11` | 3.17 kyr | 215.8 AU | 1361 | `6.77e-6` | Newtonian |
| `1e-13` | 0.317 Myr | 5088 AU (0.0247 pc) | 2.45 | `1.60e-6` | knee |
| `1e-15` | 31.7 Myr | `3.57e5` AU (1.73 pc) | `4.97e-4` | `1.12e-6` | deep MOND |

(The boost makes the radius *larger* than the Newtonian `(GM/omega^2)^{1/3}`: at fixed `r` the
medium speeds the orbit up, so a slower orbit needs a larger `r`. The factor is 1.09 at the knee
and 3.6 at `1e-15 Hz`, where the system is deep-MOND. The `1e-15 Hz` pair sits at 1.73 pc, the
field's tidal radius: it is bound only in a cluster or at the edge of survival.)

**No stellar-mass system is deep-MOND at `1e-11 Hz`.** The MOND radius of a mass `M` orbits at
`f_M = a0^{3/4}/(2 pi (GM)^{1/4})`; `f_M(2 M_sun) = 3.75e-14 Hz`, `f_M(0.1 M_sun) = 7.94e-14 Hz`,
`f_M(1e11 M_sun) = 7.94e-17 Hz`. Deep MOND at `1e-11 Hz` requires
`M = 7.88e20 kg = 3.96e-10 M_sun` (a Ceres-mass pair at 0.158 AU) — K35. So the requested high
frequencies sit where the medium is a small perturbation, not where it dominates.

Table: `delta g/g` at fixed `g_N`, with the dielectric's `tau` at its **survival limit** (the value
for which the lagged drag removes the orbit in 10 Gyr, §6.4), and the "`x = 1`" column showing what
the dielectric would do if its relaxation time were `1/omega`. The shift in the *effective a0* is
`a0^eff/a0 = (1+delta g/g)^2` at fixed `g_N` (since `g = sqrt(a0^eff g_N)`), i.e. twice the
tabulated number in the deep limit:

| `f` (Hz) | `tau_max` | `x_D` | dielectric (`x=x_max`) | dielectric (`x=1`) | BI | lattice |
|---|---|---|---|---|---|---|
| `1e-11` | `5.47e5 s` (6.3 d) | `3.44e-5` | `-8.7e-13` | `-3.67e-4` | `-1.7e-14` | `+3.3e-14` |
| `1e-13` | `1.69e7 s` (0.54 yr) | `1.06e-5` | `-2.8e-11` | `-1.23e-1` | `-3.2e-13` | `+6.4e-13` |
| `1e-15` | `4.10e10 s` (1.3 kyr) | `2.58e-4` | `-1.5e-6` | `-9.56e-1` | `-1.4e-11` | `+2.8e-11` |

At the requested frequencies every medium is invisible. The `x = 1` column is the warning: a
dielectric slow enough to matter at `1e-15 Hz` would shift `g` by 96% — and §6.4 shows the orbit
is gone in a fraction of a period. Note the dielectric's survival-limited shift *grows* toward
low frequency (`-8.7e-13`, `-2.8e-11`, `-1.5e-6`): the deeper the system, the larger the
amplification `a0/2g`, even though `tau_max` also grows.

### 6.4 The real systems, and the drag theorem

| system | `f` (Hz) | `g_N/a0` | `g/a0` | `v` | `L` | `tau_max` | dielectric | BI | lattice |
|---|---|---|---|---|---|---|---|---|---|
| wide binary, 20 kAU, 2 M_sun | `2.43e-14` | 0.317 | 0.743 | 0.46 km/s | 0.097 pc | 3.8 yr | `-2.8e-10` | `-9.9e-13` | `+2.0e-12` |
| binary, 216 AU, 1 M_sun | `1e-11` | 1361 | 1362 | 2.03 km/s | `1.0e-3` pc | 6.3 d | `-8.7e-13` | `-1.7e-14` | `+3.3e-14` |
| binary, 5088 AU | `1e-13` | 2.45 | 3.21 | 0.48 km/s | 0.0247 pc | 0.54 yr | `-2.8e-11` | `-3.2e-13` | `+6.4e-13` |
| binary, 1.73 pc | `1e-15` | `4.97e-4` | `2.25e-2` | 0.34 km/s | 1.73 pc | 1.3 kyr | `-1.5e-6` | `-1.4e-11` | `+2.8e-11` |
| galaxy, `1e11 M_sun`, 10 kpc | `1.29e-16` | 1.49 | 2.17 | 251 km/s | 10 kpc | `2.4e5` yr | `-1.3e-5` | `-1.2e-7` | `+7.0e-13` |
| cluster, `1e15 M_sun`, 2 Mpc | `5.63e-18` | 0.372 | 0.824 | 2182 km/s | 2 Mpc | `7.3e7` yr | **`-5.2e-3`** | `-2.1e-5` | `+2.9e-15` |

**The drag theorem.** A lagging response does work on the orbit. With phase lag `phi = m omega tau`
(`m = 2` for the quadrupole) and anomaly `A`,

```
P = A v sin(phi),   E = v^2/2   =>   t_decay/T = (g/A)/(4 pi sin phi) -> 1/(4 pi x)   (18)
```

in the deep limit (`g/A -> 1`). The quadrature part is *not* optional for a causal relaxation
response: it is the same pole that produces the real shift. K27 verifies the work integral
(`dE/E = 4 pi sin phi` per orbit, `t/T = 1.5922` at `phi = 0.05`). The consequence is a no-go:

```
|delta g/g| = 1e-2   =>   x = 0.1   =>   t_decay/T = 0.796 < 1                     (19)
```

(K31). **A dissipative medium cannot produce a measurable frequency-dependent `a0` in a surviving
orbit**: the same lag that shifts the real part by `x^2` drains the orbit in `1/(4 pi x)` periods.
The `tau_max` column above is the survival limit; it is what makes the dielectric's numbers so
small. For the 20 kAU binary `tau_max = 3.8 yr`; for the 216 AU binary, 6.3 days; for the cluster
orbit, `7.3e7 yr`.

**The gap is unreachable.** For the gapped lattice the resonance is at
`omega^2 = omega_g^2 + c^2 k^2`, i.e. at orbital speed

```
v_res = L sqrt(omega_g^2 + c^2/L^2) = sqrt(c^2 + omega_g^2 L^2) >= c               (20)
```

for **every** `L` (K28, minimum exactly `1.000000 c` as `L -> 0`). A bound orbit has `v < c`, so
it can never sit on the phonon resonance. The gap therefore *suppresses* the response
(`x_L = (v/c)/sqrt(1+(L/lambda_P)^2)`) rather than enhancing it. For `L << lambda_P` (wide
binaries) `x_L -> x_B` and the lattice and BI are the same order — the lattice 2× larger, since
its coefficient is `+x^2` against BI's `-x^2/2` (1.73 pc row: `+2.8e-11` vs `-1.4e-11`). For
`L >> lambda_P` (galaxies, clusters) the lattice is suppressed by `(lambda_P/L)^2`: a factor
`1.7e-3` at 10 kpc and `8.5e-6` at 2 Mpc, i.e. three to five orders below BI's `(v/c)^2`.

**The ranking.** At real orbital frequencies: dielectric (`5.2e-3`, cluster, survival-limited)
`>>` BI (`2.1e-5`, cluster) `>>` lattice (`2.9e-15`, cluster). At the requested frequencies all
three are below `1e-8`. The largest number anywhere in the table is `5.2e-3` — the dielectric in a
cluster, at the edge of, but below, the ~1% systematic floor of cluster mass profiles.

### 6.5 What the time-domain test can and cannot see

The RAR is a dc measurement: a circular orbit's field is static in the co-rotating frame, so the
static law is blind to `D(omega)`. The frequency-resolved RAR — `g` at fixed `g_N` in systems of
different `omega` and `v` — is the only channel that sees it, and it is a 2D (Re, Im) measurement:

| medium | `Re` shift | `Im` (drag) | scaling |
|---|---|---|---|
| (a) Debye | `-(a0/2g) x_D^2` | `x_D/(1+x_D^2)` | `omega` alone (`tau_D` material) |
| (b) BI | `-(a0/2g)(v/c)^2/2` | 0 at this order | `v/c`, independent of `lambda_P` |
| (c) lattice | `+(a0/2g) x_L^2` | 0 | `(v/c)(lambda_P/L)`, suppressed for `L >> lambda_P` |

So one sign separates (c) from {(a),(b)}; the presence of a quadrature part separates (a) from
{(b),(c)}; and the `L`-scaling separates (b) from (c) — BI's correction is `(v/c)^2` at every
size, the lattice's falls as `(lambda_P/L)^2` for `L > lambda_P`. That is the discriminator the
RAR cannot see. Its predicted magnitude, however, is below every current measurement.

## 7. Verdict

**What the action selects.** The action's potential is

```
W(u) = (a0^2/K)[-u/a0 - ln(1-u/a0)],                                           (21)
```

which is the one-sided lattice free energy (11): a pole at `u = +a0`, no `u = -a0` partner, so
`theta_max = 1` and `C = s = a0`. That is candidate (c), not (a) or (b). The P-sector kinetic term
is `(eta/2) E_iE^i` with `E_i = Pdot_i/N` — **second order in time**, so `c_s^2 = gamma/eta = 1`
and there is no first-order (Debye) term: candidate (a)'s relaxation is not in the action. The
P mass (`m/H0 = 2.620985e8`) makes the collective mode gapped at `f_gap = 9.11e-11 Hz`, the
lattice's phonon gap. So the action selects **the one-sided lattice with luminal, gapped
dynamics** — (c)'s statics with (b)'s light cone and (c)'s gap, and neither (a)'s dissipation nor
(b)'s field cap.

**The one prediction that tells the three apart.** Measure `delta g/g` at fixed `g_N` in systems
of the same `g_N` but different `omega` and `v`. The dielectric moves it **down** with a
quadrature part; BI moves it **down** by `(v/c)^2/2` with no quadrature part and no `L`
dependence; the gapped lattice moves it **up** by `(v/c)^2(lambda_P/L)^2`. The single bit that
separates all three is the **sign of the real shift together with the ratio `Im/Re`**: `(-, ~1/x)`
for the dielectric, `(-, 0)` for BI, `(+, 0)` for the lattice. In practice the predicted
magnitudes are `5e-3` (dielectric, cluster, at its survival limit), `2e-5` (BI, cluster) and
`3e-15` (lattice, cluster), so the runnable version today is a **null**: no frequency dependence
at the `1e-3` level and no anomalous orbital decay. That null selects the gapped luminal lattice
and excludes the Debye dielectric — whose required `tau_D` would have destroyed the orbit
(19) — and it is consistent with BI only because BI is already excluded statically.

**If the action selects none uniquely.** It selects the statics (the one-sided isotherm) and the
kinematics (`c_s = 1`, a gap), but it does **not** fix: (i) the microscopic identity of the two
states; (ii) the origin of `theta_max = 1` (the hard core — the one premise A2 could not derive);
(iii) `N`, the number of internal states, which is a modulus degenerate with `a0` (K19); (iv) the
gap, which is the P mass and therefore the vacuum, not the medium. To select a medium uniquely one
would need either a first-order time derivative in the P sector (which would give Debye and a
measurable, orbit-killing drag) or a hard field cap (which would give BI and a maximum
acceleration). The action has neither. What it has is exactly enough to pick the one-sided
lattice among the three, and no more.

## 8. Status

**DERIVED** (exact, sympy): the law's deep coefficients `+1/2` (half order) and `+1/8` (integer
order), and the non-existence of `-1/4` (K2, K2b, K2c, K3); the one-scale theorem
`a0 = -2s/f''(0)`, `c_half = f'''(0)/(3f''(0)^2)` and the `f_p` family (K4); `dF/dP = E` for
Langevin (K7); the BI Legendre pair (K11); `W'(u) = a0u/(a0-u)` (K18); the parity theorem (K21);
`g* = x^2 a0` (K26); the drag ratio (K27); `v_res >= c` (K28).

**NO-GO**: Langevin dielectric as the law — `C/s = 3`, deep exponent `1/3` at criticality and `1`
otherwise (K8, K9); Born–Infeld — exponent `1`, a hard maximum acceleration, and no constant
anomaly (K12–K15); multi-occupancy lattices — `theta - x = +x^2`, negative `g_N` (K17);
`N != 1` — either a modulus or a negative linear term (K19, K20). Only BI predicts a cutoff
(K23).

**NUMERICAL**: the cap table (K24); the frequency tables (§6.3–6.4, K29, K30, K34, K34b); the
deep-MOND ceiling (K35); the drag bound (K31); the gap frequency (K32).

**CONDITIONAL(action's P sector = a gapped luminal mode)**: the identification of the phonon gap
with the P mass, and of the lattice's collective mode with the P field. The action fixes the
statics and `c_s = 1`; the gap is the vacuum's.

## 9. Checks

`a53_checks.py` prints `<id> PASS|FAIL <measured> <threshold>` per check and ends
`A53 COMPLETE: 40/40 checks PASS.`, exit 0; `a53.out` is the captured run (5 s).

| id | what it proves | measured |
|---|---|---|
| K1 | the five canonical identities (sympy remainders) | 0 |
| K2, K2b, K2c | deep coefficients `+1/2`, `+1/8`; `-1/4` is not a coefficient; the naive coefficient diverges as `y^{-1/2}` | 0.125 |
| K3 | `+1/4` belongs to the standard `mu`, with the opposite sign | 0.250 |
| K4 | one-scale theorem, `c_half = (p+2)/(3(p+1))` for `p = 1,2,4,8` | 0 |
| K5 | identified medium: deep exponent `1/2`, `f''(0) = -2` | 0.50000098 |
| K6 | `g_N/a0 = x^2 - x^3 + ...`; n=2 even; identified medium's `c2=1, c3=-1` | -1 |
| K7 | Langevin `dF/dA = (kT/p) z = g` | 0 |
| K8, K9 | Langevin critical: exponent `1/3`, coefficient `3/5`, next order `0.402`; `C/s = 3` | 0.333333 |
| K10 | saturated anomaly `-> a0`; approach `-1` (law) vs `-1/3` (Langevin) | -0.333333 |
| K11–K15 | BI Legendre pair; exponent 1; cap; screening at `g_N=a0` (`A=-0.293 a0`); 96.9% deviation over SPARC range | 0.968873 |
| K16 | single occupancy = Langmuir for every `N` and every spectrum | 0 |
| K17 | BET `theta - x = +x^2`; `g_N < 0` | `-9.98e-7` |
| K18 | lattice `W'`, `W'' > 0`, pole at `a0` | 0 |
| K19, K20 | `C = s = N a0` is the law with `a0 -> N a0`; `C = N a0, s = a0` gives `1-N` | `2.6e-15` |
| K21, K22 | even `F` ⇒ odd `g_N` ⇒ no `g^2`; identified medium one-sided | `3.556` |
| K23 | `g_N = 1e9 a0`: law/lattice/Langevin unbounded, BI capped at `E_max` | 3 |
| K24 | caps in `a0`: `0.6385/3.30`, `1.0` or `4.23e8`, `1.0/9.0` | 0.638533 |
| K25 | Debye ODE reproduces `chi_0/(1-i omega tau)` | `0.417991` |
| K26, K26b | cutoff `g* = x^2 a0`; exact solve on both sides of it | `6.1e-11` |
| K27 | drag: one orbit removes `4 pi sin(phi)`; `t/T = 1/(4 pi sin phi)` | 1.592213 |
| K28 | `v_res = sqrt(c^2 + omega_g^2 L^2) >= c` for every `L` | 1.000000 |
| K29, K30 | requested frequencies and real systems: no measurable shift | `5.19e-3` |
| K31 | a 1% dissipative shift implies `t_decay/T = 0.796 < 1` | 0.795775 |
| K32 | action: second-order kinetic term, `c_s^2 = 1`, gap `5.7248e-10 rad/s` | `5.72e-10` |
| K33 | Debye `Im/(1-Re) = 1/x`; BI/lattice reactive, opposite signs | 10 |
| K34, K34b | exact amplification law (13); deep reduction (14)–(16) | `1.0e-3`, `1.1e-2` |
| K35 | deep-MOND ceiling; `1e-11 Hz` deep MOND needs `7.9e20 kg` | `3.96e-10 M_sun` |
| K36 | identified medium: `g_N(a0) = a0/2` | 0.5 |

`MUTATE.md`: `--mutate` replaces the identified isotherm by the **even** `tanh` (same `f'(0)=1`,
same capacity, `f''(0)=0`). Five identification checks fail (K5, K6, K16, K22, K36) while the
parity theorem, the cap table and the dynamics survive — the mutation bites exactly the
one-sidedness the lane claims is load-bearing.

## 10. What this does not do

- It does not derive `a0`. `a0` is an input, consumed twice (capacity and affinity) with nothing
  added. The `N`-modulus result (K19) shows that a lattice cannot even *predict* `a0` up to a
  relabelling: only the product `N a0` is observable in the static law.
- It does not derive the hard core `theta_max = 1`. That is A2's premise (P1), and it is the one
  structural input the parity theorem rests on: an even medium cannot give the law.
- The dynamical models are minimal: one relaxation pole (Debye), one light cone (BI), one gapped
  mode (lattice). A real medium could have several poles; the no-go (19) applies to any causal
  single-pole response and the `(v/c)^2` ceiling to any luminal reactive one, but a multi-pole
  medium with a low-frequency reactive resonance below `c/L` is not excluded by these arguments
  (it is, however, not in the action).
- `tau_D` is not predicted. The dielectric's numbers are reported at its survival limit, not at a
  derived value; that is the honest bound, not a prediction.
- The frequency tables use circular Keplerian orbits and `k = 1/L`. Eccentric orbits and the
  quadrupole (`m=2`) change `phi` by a factor 2 (which is inside the `4 pi` of (18)) and do not
  change any conclusion.
- No data were used. The cluster `5.2e-3` is a model number at a survival limit, not a
  measurement, and it is below the current systematic floor.

## 11. Next

1. **The one measurement that would bite**: a frequency-resolved RAR at fixed `g_N`, cluster vs
   field galaxy, at 0.5% systematics. It separates the dielectric (`-5e-3`) from BI (`-2e-5`) from
   the lattice (`+3e-15`); at 1% it is a null that excludes the dielectric.
2. **The static door that is still open**: the next-order coefficient `c_half` is a shape
   fingerprint (table in §1) but A7 showed the shape is not measurable in SPARC. A future sample
   with ~5% systematics at `g_N ~ a0/2` would measure `c_half`, but `p = 1` (0.500) and `p = 2`
   (0.444) differ by only 11% — a factor 10 beyond SPARC's reach, and a different question from
   n=1 vs n=2.
3. **The structural door**: derive `theta_max = 1` from the action (it is the only premise left
   between the lattice and a closed derivation), or find a first-order time derivative in the P
   sector (which would make the dielectric real and the drag a live prediction).
