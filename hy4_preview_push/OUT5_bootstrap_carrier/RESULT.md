# OUT-5 (BOOTSTRAP CARRIER) RESULT — the carrier evades T4 and LFS1 exactly, and is killed by the same constant it needs

Criteria `FROZEN_CRITERIA.md`, committed alone before any OUT-5 script or number.
TEST lane, quarantined: adopts nothing, relabels nothing, registers nothing.
Footings graded separately, never pooled. Cold dark energy is a **gravitating field
component**, never a particle. **kappa = 1/2 FITTED; not theory closed.**

---

## LABEL

| | canonical | alt |
|---|---|---|
| **lane label** | **BOOTSTRAP KILLED (FRW/HALO + PAYMENT)** | the same (every graded ratio is footing-independent in the deep regime; G9) |

The construction works and is exact. The carrier is killed by **two** load-bearing gates,
and both failures are the *same* number: the one constant the sector must carry, `mu_K`,
cannot be cold enough for the CMB and small enough for a galaxy halo at once; and the
charge it constitutes has to be paid for, and nothing in the record can pay.

**In one line:** the halo's charge can be made where it is needed — the pinning identity
is exact, T4 and LFS1 do not apply to it, and the law comes out exactly with the charge
counted once — but making it costs a rest-mass density of 3e4 to 7e6 Msun/kpc^3 against a
payer that has 86, and the sector that carries the CMB's cold dust carries, in the same
halo, 19 to 7.2e3 times the density the law needs.

---

## (a) The carrier, as an action

Action (A) is QX17 section 0, `c = 1`, `K = 4 pi G`.

| # | term | mark |
|---|---|---|
| 1 | `[R - 2 Lambda] / (4K)` | **FROM (A)** |
| 2 | `+ mu_K^2 (Q - 1)^2 / (2K)` | **FROM (A)** |
| 3 | `+ P^m A_m - W(K\|P\|)` | **FROM (A)** |
| 4 | `- gamma_L F(Pi)` | **FROM (A)** |
| 5 | `+ lambda n^m P_m` | **FROM (A)** |
| 6 | `+ S_m[g; baryons]` | **FROM (A)** |
| 7 | `- rho_c c^2` (a worldscalar; **no kinetic term**) | **NEW** |
| 8 | `+ zeta ( rho_c - N(rho_b, g, partial_s g) )` (the **pinning**) | **NEW** |
| 9 | `- (1/2) m_zeta^2 zeta^2` (multiplier regulator) | **NEW** |

`N := [(1-mu)/mu] rho_b + [mu' g /(4 pi G mu)] partial_s g`, `mu = mu(g/a0)`,
`partial_s g` the derivative along the inward field direction.

New ingredients beyond (A): one field, one multiplier, one regulator mass. No new mass
scale, no new particle, no new gauge symmetry. Term 8 is a **constraint on a new
variable**, not a rescaling of the P-sector — so **VCC1's C-III factor-(1+eps) double
count cannot arise** (G3, structural).

## (b) The Newtonian limit reproduces the law exactly, counted once

**G1 (exact).** Let `mu(u)` be any kernel and `g(r)` any field, and define

    rho_b := (1/4 pi G)(1/r^2) d_r[ r^2 mu g ]      (the law)
    rho_c := (1/4 pi G)(1/r^2) d_r[ r^2 (1-mu) g ]  (the carrier)

Then, from the product rule and Gauss's law alone,

    rho_c = [(1-mu)/mu] rho_b + [mu' g /(4 pi G mu)] partial_s g .

The right-hand side is **local**: `rho_b`, `g` and `partial_s g` at one point, no integral.
So the halo's density is a *constitutive function of the field*, not a divergence.
**sympy residual exactly 0** for a generic `mu(g/a0)` and a generic `g(r)`, on both kernels:
- law S (`mu = u/(1+u)`): `rho_c = (a0/g) rho_b + [a0/(4 pi G (g+a0))] partial_s g`
- law B, **the a0-line** (`mu = (sqrt(1+4u^2)-1)/(2u)`): the same form with its own coefficients.

**G2 (exact).** `M_c(<R) = [(1-mu(R))/mu(R)] M_b` gives, on each kernel's own field,
`X_S(x) = (sqrt(1+4x^2)-1)/2` (AMT1's demand) and `X_B(x) = sqrt(1+x^2) - 1` (the
a0-line's own demand), both residual 0 (the B case via the exact denesting
`x^8+6x^6+13x^4+12x^2+4 = (x^4+3x^2+2)^2`, verified residual 0, plus a 60-digit numeric
check at 8 radii, max diff 6.2e-61).

**Kernel sensitivity (so no conclusion here is a kernel artefact).** At FLD1's KiDS radii
`X_B/X_S` = 0.919 (x = 5.89), 0.988 (41.98), 0.992 (60.00), 0.995 (98.32). Both `~ x`.

## (c) The FRW limit is cold dust — and this is what kills it

**G6 PASS.** The carrier is the FRW cold component, so it carries `mu_K`. With
`w(a) = w0/(w0+a^3)`, `w0 = I0/(4 mu_K^2)`, `I0 = 4.037e-8 Mpc^-2` (KD1 B1a / MK1 row 1),
`w(1/3401) <= 0.01` needs **`mu_K >= 198.256 /Mpc`** (MK1 KA7: 198.254 / 198.245; KA2
reproduces to 1e-6).

**G7 FAIL — and this is the first kill.** In a static halo the same sector contributes
`delta rho_K = mu_K^2 |Phi| / (4 pi G)` (V3 §4.4). Setting it equal to the pinned density
gives a matching scale with **no `M_b`, no `a0`, no kernel** (KA5, exact):

    mu_K^match(r) = 1 / ( r sqrt( ln(R_max/r) ) )

| r (kpc) | 10 | 30 | 100 | 272 | 389 | 637 |
|---|---|---|---|---|---|---|
| `mu_K^match` /Mpc | 62.50 | 19.77 | 6.81 | 3.26 | 2.67 | **2.35** |
| `rho_K(198.26)/rho_pin` | 19.0 | 125 | 906 | 3.79e3 | 5.62e3 | **7.19e3** |

A 26.6x radial spread, and **3.2x to 84x below the CMB line** at every radius. Equivalently,
at the CMB's `mu_K` the sector's own halo density exceeds the law's by 19x (10 kpc) to
7.19e3x (637 kpc), with the wrong profile (`∝ Phi`, logarithmic, not `∝ partial_s g ~ 1/r^2`).
**Worst `|rho_K/rho_pin - 1| = 7.192e+03`** against a line of 0.10 — FAIL by 7.2e4.
`R_max` is the weakest input: moving it 300 -> 3000 kpc changes `mu_K^match`(100 kpc) by
1.76x (9.85 -> 5.60), which cannot close a 3.2x-to-84x gap.

## (d) The charge is not bounded by T4, and LFS1 does not freeze it

**G4 PASS.** T4 is a statement about the **clock's polarization charge** `D_m[(1+gamma_L Pi_+)P^m]/Q`
on a ball whose boundary free-falls. The carrier's charge is `rho_c`, a **distinct variable
with its own current**; and the pinning is keyed to `g`, which does **not** vanish where the
clock free-falls (`P = 0` there, `g != 0`). T4's boundary premise has no purchase on it.

**G5 PASS.** LFS1 A1 measures the allowed/demanded flux ratio at **-5.0e-6 to -1e-8** (it
runs the wrong way: as `M_b` grows the lapse deepens and the flux *drains*). The carrier's
charge moves at `d ln C/dt = d ln M_b/dt`, ratio **+1**. LFS1's A1 is turned from FAIL to
PASS by **2e5 to 1e8**.

## (e) kappa: reported, with an error bar — and proved NOT derivable here

    a0 = kappa c sqrt(G rho_Lam),  rho_Lam = Omega_L rho_crit  (Omega_L 0.685, H0 67.4)

| | value |
|---|---|
| kappa, canonical footing | **0.4999** |
| kappa, alt footing | **0.6041** |
| measured, distance-free fit | **0.551 +/- 0.043** |
| measured, BTFR | 0.465 +/- 0.076 |

**DERIVED: NO.** And the reason is exact (G2/H4, residual 0): as `u -> 0`,
`(1-mu)/mu -> a0/g` and `mu' g/mu -> 1`, so outside the baryons

    rho_c = partial_s g / (4 pi G) ,

which **contains no a0 at all**. Under `a0 -> lambda a0` with `g` held fixed the halo
density is invariant (`OUT5.kappa_is_a_flat_direction`, Lean, standard axioms). So no
halo observable of this carrier fixes kappa: it is a flat direction here, exactly as
FINAL-16 found it to be a flat direction of the formation physics. This is the sixth lane
to report KAPPA NOT DERIVED.

## (f) The kill, pre-registered and fired

`FROZEN_CRITERIA.md` §4 froze the gates and §3 stated the four expected kills with their
hand numbers, before any script. What fired:

| kill | pre-registered (§3) | computed | fires |
|---|---|---|---|
| **K1 FRW/halo `mu_K` fork** | 46.6 / 6.59 /Mpc at 10 / 100 kpc; 4.3x–85x below the line | 62.5 / 6.81 /Mpc; 3.2x–84x below | **YES (G7)** |
| **K2 payment wall** | local 4.0e4–1.2e1; integrated 1164–29.5 | local **6.63e4**; integrated **1.38e5** | **YES (G8)** |
| K3 positivity (spherical) | negative in voids | **0 negative points** in 64 halo rows and 4 extended profiles | **no** |
| K4 Bullet | reported, not graded | in tension | reported |

**K2 in detail** (`rho_Lam = 86.4 Msun/kpc^3`; line `<= 0.10`):

| payer | available | required | short by |
|---|---|---|---|
| the vacuum, locally | 86.4 Msun/kpc^3 | 3.46e4 (100 kpc) to 3.29e6 (10 kpc) | **4.0e2 to 3.8e4** |
| the vacuum, integrated over the halo | 1.27e-2 of `M_c c^2` (389 kpc) | 1 | 78.8 |
| the halo's own binding energy | `U/(M_c c^2) = 1.03e-7` | 1 | **1e7** |
| the clock's polarization `J/c^2` | 3.845e-3 Msun/kpc^3 (100 kpc) | 3.46e4 | **9e6** |

## (g) Lean

`OUT5.lean` — **14 theorems, exit 0, 0 errors, 0 warnings, 0 sorry**, `#print axioms`:
`[propext, Classical.choice, Quot.sound]` only (`axioms.txt`, 14/14 lines identical).
Certified: the two pinning coefficients (T1, T2), the a0-free gradient coefficient and the
flat direction (T3, T9), law S and law B as quadratics (T4, T5), `1/mu_B` (T5'),
`mu_K^match` and its uniqueness (T6, T6'), the FRW dust line `w <= 1/100 => 99 w0 <= a^3`
(T7) and the resulting `mu_K^2 >= 99 I0/(4 a^3)` (T8), and the pinning itself.
`OUT5_MUTATE.lean` — **7 false statements, 7 failures, exit 1** (`compile_MUTATE.txt`).

## Mutation arms

| arm | what it does | bites |
|---|---|---|
| MU1 | drop the pinning's gradient term | **G1 residual becomes `-a0 g'/(4 pi G (a0+g))` (non-zero); KA4 fails**; label -> CONSTRUCTION FAILS. G2 correctly does not move — the enclosed-mass statement follows from the flux alone |
| MU2 | use the *source* route `F = u^2` instead of the pinning | source spreads **5.623x** across the four masses (VCC1's V5e: 5.62); the pinning spreads **1.000** |
| MU3 | halve `mu_K` to 99.12/Mpc | G6 flips PASS -> FAIL (`w(1/3401) = 3.88e-2`, 3.88x the line) |
| MU4 | `rho_Lam -> 10 rho_Lam` | G8 improves by **exactly 10x** (6.631e4 -> 6.631e3); no other gate moves |
| MU5 | flip the sign of `partial_s g` | G10 flips PASS -> FAIL, **64 negative-density points**; label gains POSITIVITY |

## Known answers

All PASS. `sqrt(M_sun a0/G)` = 25914.5 / 28488.4 Msun/kpc (LFS1 KA4: 25914.5);
`mu_K` at `w(1/3401) = 0.01` = 198.256 /Mpc (MK1 KA7: 198.254 / 198.245);
`r_M` = 1.934 / 6.478 / 8.639 / 10.876 kpc canonical (FLD1: 1.934 / 6.479 / 8.640 / 10.877);
the deep pinning converges to `(1/4 pi r^2) dM_c/dr` as **1/(8 x^2)** (rel 1.25e-5 at x = 100);
`mu_K^match` carries no `M_b`, no `a0`, no kernel.

---

## (h) What it predicts that is not yet measured

1. **`rho_c = |partial_s g| / (4 pi G)` in the deep regime** — a parameter-free, a0-free,
   kernel-independent relation between a rotation curve's *slope* and the dark density at
   the same radius. Nothing on disk tests it: it needs a galaxy with a measured rotation
   curve and an independent lensing mass profile over the same radii. It is the cheapest
   discriminator between a constituted halo and any particle halo, and it has no free
   parameter to fit.
2. **The halo follows the baryons in real time, not on a dynamical time.** A constituted
   halo is made by the field, so if the baryons are redistributed the lensing mass inside a
   fixed radius moves with them — with **no inflow** to account for it. In a dissociative
   merger the lensing mass should therefore track the **dominant** baryon component (the
   intracluster gas, ~85–90 % of the baryons), not the galaxies. The Bullet's lensing peaks
   sit on the galaxies: **already in tension** (inputs PROVISIONAL, reported not graded).
   A stacked lensing measurement on interacting pairs is the clean test.
3. **Dark mass growth without any carrier bulk velocity.** The carrier has no kinetic term
   (term 7), so `dM_c/dt` at fixed radius is not accompanied by an inflow. Any measurement
   that ties halo growth to a velocity field (e.g. a kinematic Sunyaev–Zel'dovich or
   gas-infall proxy) would separate this from every advective carrier at once.
4. **Non-spherical negative density.** Spherical symmetry with `rho_b >= 0` gives
   `rho_c >= 0` everywhere (checked on 4 profiles). The non-spherical case is **not
   checked**; a *real component* with negative energy density wherever the field decreases
   inward is the sharpest place to kill the component reading, and void lensing is the
   instrument.

---

## What this lane does not cover

- **The covariant completion of terms 7–9 is not derived.** The pinning is specified and
  graded at Newtonian order; `N(rho_b, g, partial_s g)` is the Newtonian form of the
  invariant. This is a disclosed gap, not a result, and it is the first thing a successor
  lane should close or kill.
- The pinning is graded where it holds. What the carrier does outside the static region,
  behind a fold, or in a non-spherical geometry is not computed.
- `w(a)` is KD1's background line, not a CMB likelihood (MK1's own caveat). No Boltzmann
  solve; no nonlinear time-dependent solve.
- The potential's zero `R_max = 1 Mpc` is the weakest input; bracketed 300–3000 kpc above.
- G9 (footing-independence) **FAILS as frozen** (line 1e-6; worst 2.9e-3 at x = 15.4).
  Diagnosed, not amended: the residual is the finite-x correction to the asymptotic closed
  form, it falls with x, and G9 is not load-bearing. The asymptotic statement is exact.
- The Solar System gate passes and should not be used: 9.69e-14 Msun inside Saturn's orbit
  against a 1e-10 bound. A diffuse source is invisible locally (VCC1 said the same).

## Files

`FROZEN_CRITERIA.md`; `out5_sym.py/.out/.json`, `out5_num.py/.out/.json`,
`out5_grade.py/.out/.json` (+ `_MUTATE_MU1..MU5` twins); `OUT5.lean`,
`OUT5_MUTATE.lean`, `compile.txt`, `compile_MUTATE.txt`, `axioms.txt`.
Re-run: `python3 out5_sym.py && python3 out5_num.py && python3 out5_grade.py`
(with `OUT5_MUTATE=MU1|MU2|MU3|MU4|MU5`, then `python3 out5_grade.py _MUTATE_MU<n>`), and
`cd fable_independent_2026/lean_2026 && lake env lean ../../hy4_preview_push/OUT5_bootstrap_carrier/OUT5.lean`.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
