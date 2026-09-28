# AS087 — Boundary pressure and the claimed half factor

**Run:** `AS087-r1-20260928T1336Z-dsv4f-hermes`
**Seed sha256:** `b09eb2e2fe8bed9c3b29c4bedd7f508f7e35e420085ae6f641104d750c60ebbe` (verified at dispatch)
**Worker:** `deepseek/deepseek-v4-flash-0731` (provider openrouter) — Hermes Agent focused subagent; identity taken from the executing process.
**Branch:** Conditional deep-equilibrium sector; no automatic particle ontology.
**Gate context:** the amended thirteen-item target's equilibrium-sector obligations; historical R ≤ r_M log-well fixtures are NOT a filtered-MONO domain (seed warning reproduced here).
**Sources (pinned, hashes match `SOURCE_MANIFEST.json` at dispatch):** `deepseek_push/G084_maxentropy_law.py` `752999fd…`, `deepseek_push/G091_virial_triad.py` `8164360f…`, `deepseek_push/G233_eos_noscalar.py` `ad89298d…`.

---

## 1. Precise claim, symbol dictionary, boundary conditions, assumptions

**Object under test (the "claimed half factor"):** the coefficient 1/2 in the
conditional deep-equilibrium relation

```
sigma^2 = C/2,     C = sqrt(G_N M_b a0) = v_flat^2   [m^2/s^2]
```

as derived from an explicitly chosen force law and boundary terms for the
truncated singular isothermal phantom on a finite shell.

**Symbol dictionary** (SI throughout; framework contract conventions):

| symbol | meaning | units |
|---|---|---|
| `G_N` | measured Newton coupling `6.67430e-11` (the ONLY coupling used; `G_bare`, `G_cosmo` never invoked — stated, kept separate) | m³ kg⁻¹ s⁻² |
| `M_b` | baryon mass (observed input; MW proxy `6.5e10 M_sun`, G233 row `7.0e10 M_sun`) | kg |
| `a0` | framework scale, canonical `9.3619e-11`, alternative `1.1279e-10`, **kappa = 1/2 adopted as input** | m s⁻² |
| `C` | `sqrt(G_N M_b a0)` = v_flat² | m² s⁻² |
| `r_M` | `sqrt(G_N M_b/a0)` (equipartition radius) | m |
| `A` | profile amplitude `C/(4π G_N)` (from `M_ph(<r_M) = M_b`) | kg m⁻¹ |
| `rho(r)` | phantom density `A/r²` | kg m⁻³ |
| `P(r)` | phantom pressure `sigma² rho(r)` (isothermal barotropic closure, G233) | Pa = kg m⁻¹ s⁻² |
| `sigma²` | 1-D velocity dispersion squared (the EOS coefficient) | m² s⁻² |
| `r_in, R` | shell bounds, `0 < r_in < R`; baryon (point) mass sits at the centre, phantom strictly outside the baryon core | m |
| `M_T` | phantom mass on the shell `4πA(R − r_in)` = `C(R − r_in)/G_N` | kg |
| `T` | kinetic energy `(3/2) M_T sigma²` ⇒ **2T = 3 M_T sigma²** (seed math line) | J |
| `W_self, W_bar` | phantom self-gravity; phantom–baryon pair energy | J |
| `P_R, P_in` | pressures at the outer/inner surfaces, `sigma² rho(R)`, `sigma² rho(r_in)` | Pa |
| `F` | boundary factor `1 + (r_M − r_in) ln(R/r_in)/(R − r_in)` (dimensionless) | — |

**Boundary conditions (the only thing varied in step 2):**

* (B1) fluid-closure surfaces: `P = sigma² rho` at BOTH `r_in` and `R`
  (the truncated phantom is a barotropic fluid whose surface carries the EOS
  pressure — G091 V1d). This is the premise the seed names: "3 P_s V = M sigma²".
* (B0) zero surface pressure on the *same truncated profile* (same `rho`,
  same equilibrium): the negative control.

**Assumptions (declared, per the first-principles obligation):**

1. Static, spherical, single fluid on `[r_in, R]`; no time dependence, no
   particle ontology.
2. Profile `rho = A/r²` (γ = 2) taken from the G084 max-entropy chain at the
   framework virial temperature — **the profile is an input premise of the
   sector, not re-derived here; its own σ²-dependence is the subject of this
   task** (step 2 varies only the boundary condition).
3. Equipartition/source normalization `M_ph(<r_M) = M_b` fixes `A = C/(4πG_N)`
   (G03E as used in G091 V1a). This is a *conclusion-from-normalization*, not
   an independent fit.
4. Baryons: Newtonian point mass `M_b` at the centre; `Phi_b = −G_N M_b/r`
   for `r ≥ r_in` (phantom strictly outside the baryon core). The pair energy
   needs the inner cutoff `r_in > 0` to be finite — **no inner cutoff, no
   finite virial** (G091's honest note, reproduced below).
5. Framework force for the deep exterior: the Q-line/MONO algebraic deep limit
   `g = C/r` (derived there, NOT imposed; see §5).
6. `kappa = 1/2` adopted (task instruction) — the half factor investigated
   here is the *boundary-pressure* coefficient, distinct from kappa.

**Framework inputs (given) vs conclusions (to establish):** inputs — `G_N`,
`M_b`, `a0` (both footings), profile `rho = A/r²`, EOS `P = sigma² rho`,
geometry. Conclusions to establish — the virial energy bookkeeping
(`T`, `W_self`, `W_bar`, boundary term as closed forms), the resulting
`sigma²(C; r_in, R)` and its dependence on the boundary condition.

---

## 2. Derivation of σ² = C/2 from the chosen force and boundary terms

### 2.1 Closed forms (exact integration, signs and units shown)

*Kinetic.* `T = (3/2) M_T sigma²` ⇒
`2T = 3 M_T sigma²` (the seed's first identity, exact by definition of T).

*Self-gravity* (shell theorem integral, phantom mass inside r is
`M_ph(<r) = 4πA (r − r_in)`):

```
W_self = −4π G_N ∫_{r_in}^R rho(r) M_ph(<r) r dr
       = −16π² G_N A² ∫_{r_in}^R (r − r_in)/r dr
       = −16π² G_N A² [ (R − r_in) − r_in ln(R/r_in) ]      [J, negative = bound]
```

*Baryon pair energy* (phantom density × Newtonian point-mass potential):

```
W_bar = ∫ rho Phi_b dV = −4π G_N M_b A ln(R/r_in) = −M_b C ln(R/r_in)
```

(the `C = 4π G_N A` identity is exact: `4πG_N·C/(4πG_N) = C`). Units:
`[M_b C] = kg·m²/s² = J` ✓. Negative (attractive), sign shown.

*Surface term* (fluid closure B1 at both surfaces; the seed's second identity):

```
3 P_R V_R − 3 P_in V_in = 3·(sigma² A/R²)·(4πR³/3) − 3·(sigma² A/r_in²)·(4πr_in³/3)
                        = 4π sigma² A (R − r_in) = sigma² M_T        [J]
```

For the FULL SIS (r_in → 0, `M = 4πAR`): `3 P_s V = sigma² M` exactly
(Lean-certified, T2). The two-surface combination collapsing to `sigma² M_T`
is exact for **any** `r_in < R` — a universal identity.

*Virial theorem of the truncated static fluid* (stationary `d²I/dt² = 0`):

```
2T + W_self + W_bar = 3 P_R V_R − 3 P_in V_in        (B1, fluid closure)
2T + W_self + W_bar = 0                               (B0, zero surface pressure)
```

### 2.2 Solving the virial (only the boundary term differs)

Closure (B1):

```
3 M_T sigma² − 16π²G_N A²[(R−r_in) − r_in ln(R/r_in)] − M_b C ln(R/r_in) = sigma² M_T
```

Insert `A = C/(4πG_N)`, `M_T = C(R−r_in)/G_N`, `G_N M_b = C r_M`
(each step is a coefficient identity):

```
2 sigma² (R − r_in) = C (R − r_in) − C r_in ln(R/r_in) + C r_M ln(R/r_in)
```

**⇒  σ²_closure = (C/2) · F ,   F = 1 + (r_M − r_in)·ln(R/r_in)/(R − r_in)**

Bare (B0) — same profile, same equilibrium, only the boundary condition zeroed:

**⇒  σ²_bare = (C/3) · F**

Both solutions verified **exactly** by sympy. Because the boundary term is the
only σ²-dependent difference, the ratio is exact virial arithmetic:

**σ²_closure / σ²_bare = (3/2) for every shell, every W, every geometry**
(Lean-certified, T1: `3Ms₁+W = Ms₁`, `3Ms₂+W = 0`, `M ≠ 0` ⇒ `s₁ = (3/2)s₂`).

**Answer to step 2's question:** the coefficient is **conditional, not
universal**. Varying ONLY the boundary condition swaps 1/2 ↔ 1/3 with an exact
factor 3/2. The claimed half factor is the surface-pressure term
`3P_sV = sigma² M_T` of the truncated barotropic fluid. `sigma² = C/2` exactly
attains further only when `F = 1`, i.e. `ln(R/r_in) = 0` — the degenerate
shell `R = r_in` — or in the G091 truncation-consistent bookkeeping where the
differential baryon coupling is removed (`r_b = R`). On every non-degenerate
finite shell with a point baryon at the centre, `F > 1` (interior) and the
virial with explicit pair energies demands `sigma² > C/2`.

(cf. G091 V1e's own formula `σ² = (C/2)[1 + ln(R/r_b)/λ]` — the same
structure; this derivation upgrades it to the shell geometry with both
surfaces and the exact factor `(r_M − r_in)/(R − r_in)`.)

### 2.3 The single-counting rule (double-counting control)

The framework's deep potential is `Phi = C ln r` with `C = 4πG_N A` — the
coefficient EQUALS the phantom's own self-potential coefficient. Counting the
log well as an external field AND adding `W_self` counts `C` twice:

- virial double counting ⇒ `σ² = (C/2)[2 − r_in ln(R/r_in)/(R − r_in)]` → `C`
  as `r_in/R → 0` (sympy-exact);
- hydrostatic double counting (force `g = C/r + G_N M_ph(<r)/r²`) forces a
  **position-dependent** `σ²(r) = C − C r_in/(2r)` — a constant-σ² isothermal
  profile is NOT an equilibrium there (control passes; the isothermal C/2
  reading requires single counting).

Single counting (one force per pair) is exercised throughout §2.1–2.2 and in
the deep reading §5, and is exactly what G233's `sigma² = 2πG_N A = C/2`
hydrostatic self-consistency expresses.

---

## 3. Intermediate algebra, signs, units, scale factors — and the limiting regimes

All closed forms and their units are listed in §2.1. Scale-factor audit:

- `C = sqrt(G_N M_b a0)`: `[(m³kg⁻¹s⁻²)(kg)(m s⁻²)]^{1/2} = (m⁴s⁻⁴)^{1/2} = m²/s²` ✓ (velocity²).
- `r_M = sqrt(G_N M_b/a0)`: `[(m³s⁻²)/(m s⁻²)]^{1/2} = (m²)^{1/2} = m` ✓.
- `A = C/(4πG_N)`: `(m²s⁻²)/(m³kg⁻¹s⁻²) = kg/m` ✓; `rho = A/r²` → kg/m³ ✓.
- Boundary term `4π σ² A (R−r_in)`: `(m²s⁻²)(kg/m)(m) = kg m² s⁻² = J` ✓ — same units as `2T`, `W_self`, `W_bar` ✓.
- `F` dimensionless (ratio of lengths × log) ✓. `sigma² ∝ C ∝ sqrt(a0)` ✓.

**Limiting regimes and leading neglected terms:**

1. **Full SIS, `r_in → 0`:** `F = 1 + (r_M/R)·ln(R/r_in)·(1+O(r_in/R))` — the
   virial diverges logarithmically; **no inner cutoff ⇒ no finite virial**
   (G091's honest note reproduced exactly). The shell `W_self` differs from the
   full-SIS closed form `−16π²G A² R` by the factor
   `[1 − ε + ε ln(1/ε)]`, `ε = r_in/R`: at the diagnostics this is
   `1.0361 (ε=0.01)`, `1.1303 (ε=0.1)`, `0.8466 (ε=0.5)` — i.e. relative
   deviations **+3.6 %, +13.0 %, −15.3 %** (leading neglected term quantified;
   this is the finite-boundary correction the seed demands be kept explicit).
2. **Equipartition edge, `R = r_M`:** `F = 1 + ln(r_M/r_in)` — the largest
   diagnostic shells; `F ∈ [1.69, 5.61]` over the mandated fixtures.
3. **Newtonian limit `a0 → 0`:** `C → 0`, `r_M → ∞`, `sigma² = (C/2)F → 0`:
   the equilibrium relations are **deep-sector targets that die with a0**;
   the Newtonian regime is not described by them (stated, not hidden — the
   seed's "distinguish an exact identity from a finite numerical consistency
   check" applies: the a0 → 0 statement is an exact scaling, the shell rows
   are numeric checks).
4. **Degenerate shell `R = r_in`:** `F = 1`, `sigma² = C/2` exactly — the only
   interior boundary configuration attaining the triad value.

---

## 4. Independent checks (different representations, actual residuals)

**(a) Symbolic exactness (sympy):** `σ²_closure ≡ (C/2)F`, `σ²_bare ≡ (C/3)F`,
ratio `≡ 3/2`, full-SIS `3P_sV − σ²M ≡ 0`, `3P_RV_R − 3P_inV_in − σ²M_T ≡ 0` —
all identically zero by `simplify(expr1 − expr2) == 0`.

**(b) Direct quadrature** (log grids 40,001 / 400,001 points) of the DEFINING
integrals `W_self`, `W_bar`, `T`, boundary terms, for all
`r_in/R ∈ {0.01, 0.1, 0.5}` × `R/r_M ∈ {0.62, 1}` × both footings ×
`M_b ∈ {6.5e10, 7.0e10}` — max relative residuals: `|W_self| ≤ 1.9e-10`,
`|W_bar| ≤ 2.2e-9` (first grid) → `≤ 2.2e-10` (final 400,001-pt grid; the
first attempt at 40,001 pts FAILED the pre-set 1e-9 tolerance at 2.2e-9 —
recorded in `failed_attempts`; the integrand ~1/r needs the denser grid),
virial balance `≤ 4.9e-16`, 3/2 ratio `≤ 2.2e-16`, boundary identity
`≤ 2.7e-16`.

**(c) Substitution into the original equation (seed step 4):** the closed form
`s = (C/2)(1 + (r_M − r_in)L/(R − r_in))` is substituted into the virial
equation `2s(R−r_in) = C(R−r_in) − C r_in L + C r_M L` and verified exactly —
Lean-certified **both directions** (T3a substitution, T3b uniqueness,
`R − r_in ≠ 0`).

**(d) Hydrostatic representation:** with the single-counted framework force,
`dP/dr = −rho g`:
- interior log-well fixture, `g = C/r` (single counting incl. self-consistent
  well): `−2σ²A/r³ = −CA/r³` ⇒ **σ² = C/2 at every r** — the local statement
  behind the virial result, consistent with G233's `σ² = 2πG_NA`;
- deep shells: residual `max|dP/dr + ρg|/|dP/dr| ≤ 4.7e-16` on
  40,001-point grids, both footings (algebraic `g = C/r`).

**(e) Lean 4 certificates** (`AS087_half_factor.lean`, compiled
`lake env lean`, Lean 4.34.0-rc2): T1 ratio 3/2, T2 `3P_sV = σ²M`, T3a/T3b
closed-form substitution + uniqueness. `#print axioms` for all four theorems:
**`[propext, Classical.choice, Quot.sound]`** — zero `sorry`, allowed set
exactly.

---

## 5. Deep exterior: where the log well is derived, not imposed

At `r ≫ r_M` the point-source deep field of the operative branch is
`g = √(a0 G_N M_b)/r = C/r` (Q-line deep limit; the MONO continuation agrees
to the filtered-kernel error, below). The local single-counted balance
`dP/dr = −rho·(C/r)` with `rho = A/r²` gives

**σ² = C/2 exactly, every radius of every deep shell** (residual ≤ 4.7e-16).

Mandated deep shells `r_in/r_M ∈ {10, 100}`, `R/r_in ∈ {2, 10}` (both
footings): the same statement holds identically (it is r-independent). For
completeness the virial WITH explicit pair energies on those shells gives
`F = 0.3138–0.7697` i.e. `σ² = 0.157–0.385 C` — the difference between the
readings is precisely which forces are counted (local framework field once vs
self-gravity + pair energy separately); §2.3's single-counting rule applies,
and the total-field reading is the physical one.

**Full-kernel error bound (filtered MONO):** the operative field is
`smooth`ed through `S = exp((ξ²/2)Δ)` with the heat-filter width **ξ unpinned
by the repo** (framework contract defines S without fixing ξ). Smoothing a
monopole `r^{-2}`-type field shifts it at relative order `(ξ/r)²` for
`r ≫ ξ`:

```
|g_MONO(r) − C/r| ≤ (C/r) · c₂ · (ξ/r)² ,   c₂ = O(1) Bessel-width constant,
domain r ≥ r_in ≫ max(r_M, ξ).
```

With ξ unpinned this is a **parametric bound structure, not a number** — an
explicit open dependency (see `next_unresolved_implication`). The algebraic
`C/2` result is exact in the ξ → 0 limit, which is the state of the art the
seed asks to be bounded rather than silently transferred.

---

## 6. Controls (all capable of failing — observed outcomes)

| # | Control | Design | Observed |
|---|---|---|---|
| NC1 | **Zero surface pressure on the same truncated profile, same equilibrium** | same ρ, same W, B0 boundary | `σ²_bare = (2/3) σ²_closure` on every diagnostic shell (exact 3/2, ratio residual ≤ 2.2e-16); the C/2 claim **fails** under B0 ⇒ coefficient conditional **PASS (fires)** |
| NC2 | Double counting (log well + self-gravity) | force `C/r + G M_ph(<r)/r²` | equilibrium not isothermal; `σ²(r) = C − C r_in/(2r)`; virial limit `σ² → C` **PASS (fires)** |
| NC3 | Deep limit | `g = C/r`, deep shells | `σ² = C/2` exact, residual ≤ 4.7e-16 **PASS** |
| NC4 | Newtonian/a0 → 0 limit | exact scaling | `σ² ∝ C → 0`: deep-sector targets die with a0; no Newtonian claim made **PASS (exact identity, distinguished from numeric checks)** |
| NC5 | r_in → 0 (full SIS) | log divergence | `F ~ (r_M/R)ln(1/ε) → ∞`; no finite virial without inner cutoff **PASS** (reproduces G091's honest note) |
| NC6 | Finite-boundary correction | `W_self` shell vs full-SIS form | deviations +3.6/+13.0/−15.3 % at ε = 0.01/0.1/0.5 — quantified, not ignored **PASS** |

12/12 scripted checks PASS on the final run (wall 0.63 s, peak RSS
203.7 MiB, single thread — bounds enforced, see `execution_bounds`).

---

## 7. Diagnostics at the mandated fixtures (both footings)

`F = 1 + (r_M − r_in) ln(R/r_in)/(R − r_in)` and σ (closure reading),
MW proxy `M_b = 6.5e10 M_sun`:

| r_in/R | R/r_M = 0.62 (F) | R/r_M = 1.00 (F) | σ(closure) 0.62 | σ(closure) 1.00 |
|---|---|---|---|---|
| 0.01 | 8.4562 | 5.6052 | 346.6 km/s | 282.2 km/s |
| 0.10 | 4.8707 | 3.3026 | 263.1 km/s | 216.6 km/s |
| 0.50 | 2.5428 | 1.6931 | 190.1 km/s | 155.1 km/s |

(canonical footing; identical F for alt and for `M_b = 7.0e10` — F is
footing-independent in its variables; σ scales as `sqrt(C)`.)
**Reading:** the interior imposed-log-well ansatz virial with explicit pair
energies does NOT deliver `C/2` on any mandated fixture (F > 1.69 everywhere);
`sigma² = C/2` is confined to the consistent-truncation limit — exactly what
the seed's "R ≤ r_M fixtures test the historical imposed-log-well ansatz"
design anticipates. These rows are controls, not a fit.

**Footings** (kappa = 1/2 fixed both; different vacuum densities — they
cannot share both fixed ρ_Lambda and fixed kappa):

| | canonical `a0 = 9.3619e-11` | alt `a0 = 1.1279e-10` |
|---|---|---|
| `rho_Lambda = 4a0²/(G_N c²)` | 5.8444e-27 kg/m³ | 8.4831e-27 kg/m³ (ratio 1.4515 = (a0_alt/a0_can)²) |
| `sigma² = C/2` (MW proxy) | 1.4209e10 (m/s)² | 1.5593e10 (m/s)² |
| σ | 119.20 km/s | 124.89 km/s |
| v_flat, r_M | 168.6 km/s, 9.84 kpc | 176.6 km/s, 8.96 kpc |

kappa back-check `a0/(c·sqrt(G_N rho_Lambda)) = 0.500000` on both footings.

---

## 8. Strongest surviving statement

> **Theorem (conditional, exact).** For the truncated singular isothermal
> phantom `rho = A/r²` (`A = C/(4πG_N)`, equipartition-normalized), with the
> isothermal fluid closure `P = σ²rho` and a central point baryon mass `M_b`,
> on any `0 < r_in < R` (interior `R ≤ r_M` fixtures; deep exterior likewise):
> (i) the exact two-surface virial gives
> `σ² = (C/2)·F` with `F = 1 + (r_M − r_in)ln(R/r_in)/(R − r_in)` and
> `σ² = (C/3)·F` with zero surface pressure on the same profile — the ratio
> **3/2 is exact for every shell** (Lean-certified): the claimed half factor
> is the surface-pressure virial term of the truncated barotropic fluid and is
> **conditional on the boundary condition**, not universal;
> (ii) `σ² = C/2` exactly requires the differential baryon coupling to vanish
> (degenerate shell `R = r_in`, or the G091 truncation-consistent well
> `r_b = R`); on the mandated diagnostics `F = 1.69–8.46` so the interior
> ansatz virial predicts `σ² > C/2`;
> (iii) with single counting (one force per pair), the local balance
> `dP/dr = −ρ·(C/r)` gives `σ² = C/2` exactly at every radius of the deep
> shells `r_in/r_M ∈ {10,100}`, `R/r_in ∈ {2,10}` (residual ≤ 4.7e-16), the
> algebraic deep limit of the operative branch, with the filtered-MONO
> full-kernel error bounded parametrically at `O((ξ/r)²)` in the unpinned
> filter width ξ.

**Domain:** static spherical sector, `0 < r_in < R`, both acceleration
footings, `G_N` only, no particle ontology, no time dependence. **Does NOT
establish:** kappa = 1/2 (adopted), dynamical attainment (G035 kill stands),
the ξ value, or an action-level origin of the coefficient.

---

## 9. First additional implication needed to transfer to the full theory

The C/2 relation is here derived on fluid/virial premises (EOS closure,
equipartition, single counting). The operative gate (amended requirement 1:
exact MOND phenomenology via **filtered ν_mono**, causal by **criterion B**)
needs the **action-level bridge**: solve the full filtered-MONO field equation
`ΔΦ = 4πG_N ρ_b + S*[(ν_mono(|grad S u|/a0) − 1) grad S u]` for a point
source and show (i) its deep-shell equilibrium reproduces `rho = A/r²` and
`σ² = C/2` within the `O((ξ/r)²)` kernel error, and (ii) the truncated-shell
fluid/virial derivation of this task is the same-theory limit of that
solution with `ξ → 0`. Until then, ALL interior R ≤ r_M fixtures remain
historical-ansatz tests (as the seed states), and C/2 is a **conditional
equilibrium-sector target with proven boundary-condition dependence** — not a
transferable constant across branches. No other branch (Q, RAR, MU2, EXP) was
imported to repair anything; MONO appears only as the bounded deep-field
statement of §5.

---

## 10. Reproduction

1. `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 AS087_boundary_pressure.py`
   → prints all tables, writes `residuals.json` (final run: 12/12 PASS,
   0.63 s wall, 203.7 MiB peak RSS).
2. `cd fable_independent_2026/lean_2026 && lake env lean <abs>/AS087_half_factor.lean`
   → 4 theorems, axioms `[propext, Classical.choice, Quot.sound]`, no sorry.
   (Compile host only — nothing written into the Lean workspace.)
3. Raw outputs: `raw_output.txt`, `lean_output.txt`, `time_mem.txt`.
