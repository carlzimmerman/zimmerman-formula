# FINAL-19 (KAPPA_C) FROZEN CRITERIA: derive kappa from the DEEP-FIELD COLUMN, without assuming it (2026-11-11)

TEST lane, quarantined. Relabels nothing, adopts nothing, not registered.
**kappa = 1/2 FITTED; not theory closed.** Footings graded separately, never pooled.

**Committed alone, before any FINAL-19 script exists and before any FINAL-19 number is computed.**

---

## 0. The question, and what is NOT allowed

The record carries two things about the deep field:

* **U1 (universal column).** `Sigma_c = a0 / (2 pi G)` is the same for every galaxy:
  `106.9` (canonical) / `129.2` (alt) Msun/pc^2.
* **U2 (the claim under test).** the law's pressure scale obeys
  `a0^2 / (8 pi G) = rho_Lambda c^2 / (32 pi)` — **at kappa = 1/2**.

U2 is the target. Section 1 below shows (algebra, no numbers) that U2 is *algebraically
equivalent* to `kappa^2 = 1/4`; the lane therefore must **not** use it. What the lane
uses instead is a first-principles column computation in SI: hydrostatic/Jeans equilibrium of
a static, self-gravitating, **cold** halo carrying the law's anisotropic stress, compared
with the column the vacuum's own energy density can support.

**Not allowed anywhere in this lane:** any use of U2; any injected factor of 32*pi; any fit of
kappa to the observed column. All inputs are independent measurements (rotation curves /
BTFR / WALLABY / MIGHTEE for `a0`; Planck for `rho_Lambda`).

---

## 1. The derivation, fixed in advance

Conventions: SI throughout for the numbers; `K = 4 pi G`, `u = g / a0`; **material Cauchy
stress is `sigma = -Pi`** (ELA1 amendment A1), so the pressure that carries weight is
`-Pi_rr` along the radial direction.

### 1.1 The law's static stress (from the record; FINAL-7 crux, verbatim)

```
Pi_ij  = J(g) delta_ij - g_i g_j / (K (1+u)),        K = 4 pi G,  u = g/a0
J(g)   = (a0^2 / K) [ u - ln(1+u) ]
```
Spherical: `Pi_rr = J - g^2/(K(1+u))`, `Pi_tt = Pi_phiphi = J`.
Deep field (`u -> 0`): `J = g^2/(2K) + O(u^3)` hence `Pi_rr = -g^2/(2K)`,
`Pi_tt = +g^2/(2K)`, i.e. **`Pi_rr = -Pi_tt` exactly in the deep field**
(the computed residual `(Pi_rr+Pi_tt)/|Pi_tt|` is `6.6e-3` at `100 r_M`; the leading
behaviour is `2u/3`):
```
|Pi_rr| = |Pi_tt| = P(g) ,     P(g) := g^2 / (8 pi G)      [deep field, exact]
```

### 1.2 Jeans / hydrostatic equilibrium with that anisotropy (EXACT)

Spherical, static, cold:
```
d Pi_rr / dr + (2/r) (Pi_rr - Pi_tt) = - rho_h g                    (J)
```
With `Pi_tt = -Pi_rr` the anisotropy term doubles the "2/r":
```
d Pi_rr / dr + (4/r) Pi_rr = - rho_h g   <=>   (1/r^4) d(r^4 Pi_rr)/dr = - rho_h g   (J2)
```
Poisson (the halo gravitates normally — M5 hypothesis (iii)):
```
rho_h = (1/K) ( dg/dr + 2 g / r )                                      (P)
```
(with `g_N = GM_b/r^2`, `dg_N/dr + 2 g_N/r = 0` outside the baryons.)

**J1 (identity that must PASS).** On any spherical solution of the law's radial relation
`g^2/(g + a0) = g_N`, (J) with the law's `Pi_ij` and `rho_h` from (P) is an *identity*:
the residual is exactly zero at every `u`, not only asymptotically. This is certified
symbolically (`sympy`, exact) **and** in Lean for the deep-field branch. If J1 fails, the
lane's whole footing (that `Pi` is the equilibrium stress) is void and the lane stops.

**J1b (the degeneracy, reported).** The isotropic reading `Pi_ij -> J delta_ij` satisfies (J)
*on the same branch* — because the difference is a radial-radial stress `tau ∝ g_N ∝ r^-2`,
which is annihilated by the spherical Jeans operator. So equilibrium alone does **not**
select the anisotropy; the anisotropy is an input from the covariant theory, and the lane
grades the isotropic variant on the signature gates (M1).

### 1.3 The column the halo can sustain (the derived relation)

In the deep field the law's solution is `g(r) = C / r`, `C = v_inf^2`, `v_inf^4 = G M_b a0`,
so (P) gives `rho_h = C/(K r^2)` and the column above `r` is
```
Sigma(r) = int_r^inf rho_h dr'  =  C/(K r)   =>   g(r) = K * Sigma(r) = 4 pi G Sigma(r)
```
Combined with 1.1:
```
boxed:  |Pi|(r) = 2 pi G Sigma(r)^2            (C1)      [exact on the deep-field branch]
```
i.e. the anisotropic stress needed to hold a column `Sigma` against its own gravity is
`2 pi G Sigma^2`. Inverting: the largest column a cold medium of stress capacity `Pi_max`
can sustain is
```
Sigma_max = sqrt( Pi_max / (2 pi G) )                       (C2)
```

### 1.4 The vacuum's stress capacity (THE load-bearing physical input)

The cold component is the dark energy: energy density `eps_L = rho_Lambda c^2`, pressure
magnitude `|p| = eps_L` (`w = -1`). No equation of the record says how much of that
energy density can be deployed as an **anisotropic** stress, so the lane makes it an explicit,
pre-registered, dimension-free input:
```
Pi_vac := f * eps_L ,     f := 1 (PRE-REGISTERED; the vacuum's own energy density is the ceiling,
                                 the dominant-energy-condition value); f = 1/(8 pi) and f = 1/(32 pi)
                                 are carried as named variants.
```
⟹ `Sigma_vac = sqrt( f eps_L / (2 pi G) )`.
⟹ **master ratio** `R := Sigma_vac / Sigma_c = sqrt(2 pi f) / kappa` (uses only `a0 = kappa c sqrt(G rho_L)`
and `Sigma_c = a0/(2 pi G)`; `G`, `c` and `rho_L` cancel).

**Gate (primary).** The universal column is *sustained* iff `Sigma_c <= Sigma_vac` ⟺ `R >= 1`.
The *saturation demand* `Sigma_c = Sigma_vac` is the inversion the brief asks for.

---

## 2. Fixed inputs (independent measurements; both footings, never pooled)

```
c  = 2.99792458e8 m/s                G  = 6.67430e-11 m^3 kg^-1 s^-2      (CODATA / a0kit)
Mpc = 3.0856775814913673e22 m        Msun = 1.98892e30 kg                    (a0kit)
H0 = 67.4 km/s/Mpc                   Omega_Lambda = 0.685                 (CFG493 footing inputs)
s_L = c H0 sqrt(3 Omega_L /  (8 pi)) = c sqrt(G rho_Lambda)   [canonical footing]
s_C = c H0 sqrt(3        / (8 pi))   = c sqrt(G rho_crit  )   [alt footing]
MEASURED a0 (CFG493 GLS combination):  log10 a0 = -10.1073 +- 0.0985 dex
MEASURED kappa:  canonical 0.4172 +- 0.0946 ;  alt 0.3452 +- 0.0783        (CFG493)
RECORD's footing values (kappa = 1/2 adopted):  a0 = 9.3603e-11 / 1.1312e-10 m/s^2
```
The record's two `a0` footing values are **themselves derived from kappa = 1/2**; the lane
cross-checks its unit arithmetic against them (G1) and then uses only the *measured* `a0` and
*measured* `rho_Lambda` for every graded number.

---

## 3. Pre-registered kills (expected outcome stated before any number)

| # | Kill | Expectation |
|---|---|---|
| **K1** | "`kappa = 1/2` falls out of the deep-field column" | **FIRES.** The demand forces `kappa = sqrt(2 pi f)`; with the DEC ceiling `f = 1` that is `2.5066`, a factor `5.013` from `1/2`. |
| **K2** | "the universal column SATURATES the vacuum's stress budget" | **FIRES.** The column uses `f = kappa^2/(2 pi) ~ 2.8%` of the DEC ceiling, ~150 sigma below saturation. |
| **K3** | the Jeans identity J1 (law's `Pi` + Poisson `rho_h`) | **HOLDS** (exact, all `u`) |
| **K4** | "the column is inside the ceiling" (no dynamical inconsistency) | **HOLDS** on both footings |
| **K5** | "some O(1) geometry convention rescues `R = 1`" | **FIRES.** The convention bracket leaves `R` in `[~6, ~12]` |
| **K6** | the deep-field anisotropy `Pi_rr = -Pi_tt` | **HOLDS**, residual `-> 2u/3` |

Expectation in one line: **the column route does not derive kappa**; it bounds it
(`kappa <= sqrt(2 pi f)`), and the bound is far from the fitted value. The "1/2"
lives in the unforced dilution of the vacuum pressure by a factor `8 pi`
(Einstein's) — the same factor U2 hides.

---

## 4. Gates (each printed with measured value AND threshold, separately)

| Gate | Quantity | Threshold |
|---|---|---|
| G1 | `Sigma_c` from the footing `a0` values vs `106.9 / 129.2` Msun/pc^2 | pass if rel < 1e-3 |
| G2 | **primary** `R = Sigma_vac/Sigma_c` (canonical, then alt) | sustained if `R >= 1` |
| G2b | `|R - 1| / sigma_R` | saturation passes only if <= 3 |
| G3 | `kappa_forced = sqrt(2 pi f)` vs measured `kappa +- sigma` | derivation passes only if pull <= 3 |
| G4 | required `f` for `kappa = 1/2` vs `f = 1` | consistency only if `f = kappa^2/(2 pi)` |
| G5 | `R` over the named column conventions | conclusion robust if `min R >= 2` |
| G6 | SI units / dimensional closure of `Sigma_vac`, `Sigma_c` | pass if both kg m^-2 |
| G7 | `Sigma_vac` and `Sigma_c` are kappa-INJECTIVE: `R` moves with `kappa` | pass if `dR/dkappa != 0` |

Footings are graded separately and the two labels are reported side by side. Nothing is pooled.

---

## 5. MUTATE arms (each must bite; outputs `f19_kappa_C_MUTATE_<arm>.out/.json`)

* **M1 (ISOTROPIC / kinetic).** Drop the `- g_i g_j/(K(1+u))` term, i.e. `Pi_rr = Pi_tt = J`.
  Expect: J1 still passes (the documented degeneracy, J1b) **but** the signature gates fail —
  `Pi_rr/Pi_tt -> +1` instead of `-1`, and `sigma_r^2 = +v_inf^2/2 > 0` (a kinetic medium is
  allowed, i.e. the M5/ELA1 radial-tension reading is lost).
* **M2 (CIRCULAR).** The record's own shortcut: assume U2 and read off `kappa = 1/2`.
  Expect: recovers 1/2 **and fails the INDEPENDENCE gate** (Lean-certified: `U2 <-> kappa^2 = 1/4`).
* **M3 (NEWTON).** `mu = 1`: no phantom, `Pi == 0`, `rho_h == 0`. Expect: (C1) degenerates, `Sigma_max = 0`,
  the demand `Sigma_c = Sigma_vac` fails, `kappa` undefined/0.
* **M4 (GEOMETRY).** Substitute the isotropic plane-parallel slab relation
  `|Pi| = (pi/2) G Sigma^2` for the derived spherical `beta = 2` relation.
  Expect: `R` moves by exactly a factor 2 (to `~12`); the `R = 1` verdict fails harder —
  i.e. the lane's negative conclusion survives the convention change.

An arm that does not bite is reported as a failed arm, not silently dropped.

---

## 6. Reporting

* One headline label per footing, printed as `<LANE> COMPLETE: N/M checks PASS.` with a separate
  per-gate table.
* Every graded number printed with its 1-sigma and its threshold on the same line.
* A closing paragraph naming the single input that would have to move for `kappa = 1/2` to come
  out of the column route, and quantifying the move (factor and sigma).
* The Lean certificate file is compiled and its exit code plus every `#print axioms` line is
  recorded in the lane's `RESULT.md`.
