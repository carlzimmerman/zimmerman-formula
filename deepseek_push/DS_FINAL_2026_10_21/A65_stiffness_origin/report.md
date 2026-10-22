# A65 — WHERE THE STIFFNESS LENGTH `L*` COMES FROM

Lane A65. `a65_checks.py` (24 checks, 24/24 PASS, exit 0), `a65.out`, `a65_results.json`,
`MUTATE.md` + 5 mutation outputs. SI. Constants: BRIEF §4, `σ_c = 8.33 km/s` (A20 cand. 1,
A37), `σ_th = 8.226 km/s` (10⁴ K, μ = 1.22; A20/A56), `a0_P3 = 1.132e-10` (THEORY P3).
Read first: A20, A37, A33 `MASTER_ACTION.md`, A61; also THEORY §3.3–3.4, BRIEF §1/§4, and
A56 (same identity by an exponent census; this lane adds the four named candidates, the
candidate-by-candidate guard, and the footing/K corollaries).

## 0. PRE-REGISTRATION (written before any number in §2–§5 was computed)

A candidate **counts as a derivation of `L*`** iff all four hold:

- **C1 — window (a).** Derived `L*` lies in `[24, 1000] pc` (the task's window; A20's
  one-sided ceiling is `90 pc` at `f_c -> 1` and `180 pc` at `f_c = 0.25`, reported
  alongside but not used as the admission test).
- **C2 — coefficient (b).** Written `L* = c·X` with `X` a combination of the theory's own
  ingredients, `c ∈ [0.5, 2]` — order 1, not `1e-3` and not `1e3`.
- **C3 — no galactic radius (c).** No `R_core`, `R0.3`, `r_switch`, `R_d`, `r_M`, `V_f` input.
  A measured galactic *density* is not a radius but is flagged: it makes the candidate
  environment-fitted, not a medium constant.
- **C4 — no new constant (d).** Only `{a0, c, G, ρ_Λ, σ_c, baryon sound speed, dark-sector
  density, ħ, m_p}` may enter. A new particle mass is a fit.

A candidate needing `c` outside C2, or a density chosen to land the answer, is **a fit**.
C2 is necessary, not sufficient: a coefficient *inside* the band that is chosen to land the
answer is still a fit. The only admissible coefficient is one fixed by the theory's own
definition of the scale (here, exactly 1 from the acceleration-time length).

## 1. Claim

**The stiffness length is the cold medium's acceleration-time length at `a0`:**

    L* = σ_c²/a0 = (σ_c/c)² L_MOND = (σ_c/c)² ℓ₁/κ .                                      (1)

At A37's closure `κ = 1/2`, `L_MOND = 2 ℓ₁`, so (1) is also `2(σ_c/c)² ℓ₁`; the factor 2 is
the same one that makes `L* = √2 λ_P`.

With `σ_c = 8.33 km/s` and canonical `a0 = 9.36e-11 m/s²`, (1) gives **24.0250 pc**; the
coefficient is **exactly 1** (no 4π, no 2π, no fitted number), it contains **no K** and
**no galactic radius**, and it is the only one of the four named candidates that lands in
`[24, 1000] pc` **without a tuned density or a new constant** (the other in-window readings
are the `10⁻²² kg/m³` Jeans length at 932 pc and the fitted-boson quantum length at 24 pc;
both fail the guard). Candidate (a), the medium's Jeans length, gives **196.2 kpc** at the cosmic
cold density and reaches 24 pc only at `ρ = 1.505e-19 kg/m³ = 90 cm⁻³` — 6.7×10⁷ times the
cosmic cold density, a *measured galactic* density, i.e. a tuned input. Candidate (b),
gradient-vs-potential, returns `L*/√2 = 16.99 pc = λ_P` by construction (circular) or
`λ_J/2 = 98.1 kpc` against the medium's kinetic energy. Candidate (c) in its literal
response-time-equals-dynamical-time reading returns the Jeans length again (196.2 kpc);
only its acceleration reading, `t_cross = t_acc = σ_c/a0`, gives (1). Candidate (d),
quantum pressure vs self-gravity, gives **548.39 kpc** with the theory's own P mass and reaches
24 pc only for a new boson of **1.96×10⁻¹⁶ eV**, which the theory does not contain (P4).

**But the guard bites.** (1) clears the 24 pc floor by 0.1042 % when fed `σ_c = 8.33 km/s` —
and that value is itself the inversion of the 24 pc anchor (A20: `σ_c = √(a0L*)`). The only
*independent* value, the 10⁴ K thermal width `8.226 km/s`, gives **23.429 pc — 2.38 % below
the floor**. On the theory's own P3 footing (`a0 = 1.132e-10`) it gives **19.865 pc — 17 %
below**. So the honest verdict is not "24 pc derived": it is **derived in form, fitted in
normalization** — `L* = σ_c²/a0`, coefficient 1, no tuned coefficient, but the number
`24.0` is the canonical-footing value of a formula whose one external input, `σ_c`, is
fixed by the 24 pc anchor (or, independently, lands 2.38 % below it).

**The K corollary.** (1) contains no `K`. `L*` is therefore **24.025 pc regardless of the
`K = 4πG` vs `8πG` dispute**; what the convention moves is `γ = KL*²/2`, not `L*`. At
`K → 2K`, `√(2γ/K)` returns `L*/√2 = 16.988 pc`, which is `λ_P`, not `L*` (A61 §5). A61's
open question is dissolved from the `σ_c` side: the record's `L*`-anchor is convention-free
because it is anchored to `σ_c²/a0`.

## 2. Task 1 — the scale census

`L* = 24.0250 pc = 7.4133×10¹⁷ m`; ratios are to that number. `L_MOND` is canonical; the
task's `8.0×10²⁶ m` is the **alt** footing (`c²/1.13×10⁻¹⁰ = 7.954×10²⁶ m`), not a third scale.

| scale | formula | value | ratio to `L*` | log₁₀ | O(1)? | exact multiple? |
|---|---|---|---|---|---|---|
| MOND length | `c²/a0` | 9.602×10²⁶ m = 31.118 Gpc | 1.2952×10⁹ | 9.112 | no | **yes**: `(c/σ_c)²` |
| cosmic horizon | `c/H0` | 1.372×10²⁶ m = 4.448 Gpc | 1.8514×10⁸ | 8.267 | no | `(c/σ_c)²a0/(cH0)` |
| de Sitter horizon | `c/H_Λ = √(3/Λ)` | 1.6597653×10²⁶ m = 5.379 Gpc | 2.2389×10⁸ | 8.350 | no | `(c/σ_c)²/Z` |
| vacuum cell | `ℓ₁ = √(8π/Λ)` | 4.804×10²⁶ m = 15.569 Gpc | 6.4803×10⁸ | 8.8116 | no | `(c/σ_c)²κ` |
| Jeans, cold medium | `σ_c/√(4πGρ_c)` | 6.0549×10²¹ m = 196.227 kpc | 8.168×10³ | 3.912 | no | `(c/σ_c)κ√(ρ_Λ/4πρ_c)` |
| Jeans, elastic (P) | `√2πL*` | 3.293×10¹⁸ m = 106.740 pc | 4.442883 | 0.647665 | no | **yes**, construction |
| baryon sound speed | `c_s,b/H0` (10⁴ K, μ=1.22; `c_s,b = 8.226 km/s`) | 3.76599×10²¹ m = 122.0475 kpc | 5080.017 | 3.705865 | no | no |
| baryon thermal (accel.) | `c_s,b²/a0` | 7.2298×10¹⁷ m = 23.429 pc | 0.9752 | −0.0109 | **yes** | `(c_s,b/σ_c)²` |
| inter-particle spacing | `(ρ_c/m_p)^(-1/3)` | 0.904998 m | 1.2208×10⁻¹⁸ | −17.91 | no | no |
| Schwarzschild, 1 M☉ | `2GM☉/c²` | 2954.008 m | 3.9847×10⁻¹⁵ | −14.3996 | no | no |
| atomic (Bohr) | `a₀^Bohr` | 5.29177×10⁻¹¹ m | 7.1382×10⁻²⁹ | −28.1464 | no | no |

**Result (K12/K12b): one of the eleven scales lies in the pre-registered `[0.5, 2]` band —
the thermal baryon acceleration length `c_s,b²/a0 = 23.429 pc = 0.9752 L*`, 2.38 % below the
24 pc floor.** It is the same `σ²/a0` functional as (1) with `c_s,b` in place of `σ_c`, i.e. a
pure number times `L*`; it is the independent input that exposes the normalization, not a
separate derivation. The next nearest is the elastic Jeans length `√2πL* = 106.74 pc` at
`4.44 L*`, a multiple *by construction* because `γ = 2πGL*²`; it cannot select the coefficient.
No vacuum, cosmic, or atomic scale sits near 24 pc; only the medium's own combination can
populate the window (A56 K10–K15b, reproduced here).

## 3. Task 2 — the four candidates

**(a) Jeans length at its own sound speed and density.** `λ_J = σ_c/√(4πGρ_c)` (2). At
`ρ_c = Ω_cρ_crit = 2.2566×10⁻²⁷ kg/m³` (`Ω_c = 5.3643Ω_b`): **196.227 kpc = 8.168×10³ L***.
At `10⁻²² kg/m³`: **932.2 pc** (inside the wide window, but 39× `L*`); at `10⁻²⁰`: 93.2 pc.
To force `λ_J = L*` one needs

    ρ = σ_c²/(4πG L*²) = 1.5054×10⁻¹⁹ kg/m³,  n = 90.00 cm⁻³,  = 6.671×10⁷ ρ_c .           (3)

That is a molecular-cloud density. **NO-GO:** the candidate spans 24 pc–1 kpc over three
decades of *measured galactic* density, and the density that lands 24 pc is itself tuned
(C3-spirit, C4). The `4π` vs `π` convention is a factor `2π` (or `1/(2π)`) and changes nothing.

**(b) Gradient energy vs potential energy.** `(γ/2)(D·P)²` with `P ~ a0/K`, `D ~ 1/L`;
`W(u) = u²/(2K) + O(u³)`, so at `u ~ a0`, `W ~ a0²/(2K)`:

    (γ/2)(a0/KL)² = a0²/(2K)  ⇒  L² = γ/K = L*²/2  ⇒  L = L*/√2 = 16.988 pc = λ_P .       (4)

**Circular**: linear in `L*` because `γ ≡ KL*²/2`; returns `L*/√2` for any `γ` — it is the
P Compton length, not `L*`. Against the
medium's kinetic energy `ρ_cσ_c²` instead, the same balance gives `L = σ_c/(2√(Kρ_c)) =
λ_J/2 = 98.11 kpc`, which fails. **NO-GO in both readings.**

**(c) Response time equals dynamical time.** Two readings, different physics. *Literal*
(`t_res = L/σ_c`, `t_dyn = 1/√(4πGρ_c)`): `L = σ_c t_dyn = λ_J = 196.227 kpc` (K15) — fails.
*Acceleration/crossing* (`t_cross = L/σ_c`, `t_acc = σ_c/a0`):

    L = σ_c t_acc = σ_c²/a0 = 24.0250 pc,   t_acc = 8.8995726×10¹³ s = 2.820 Myr .            (5)

The medium moving at `σ_c` changes its velocity by `σ_c` in the acceleration time
`t_acc = σ_c/a0`; the distance travelled in that time is `L = σ_c t_acc = σ_c²/a0`
(the stopping distance would be half this, `σ_c²/(2a0) = 12.01 pc`, and is not the
quantity used here). That is the length at which the P field's nonlinearity (`u → a0`)
is reached by the cold sector's own kinematics. **Lands, coefficient exactly 1** (K16).
**Naming honesty:** the literal dynamical-time reading of (c) fails; the surviving scale is
the acceleration length, not a gravitational `t_dyn` balance. It is listed under (c) because
it is the only reading of "response time" that uses the theory's own `a0`, not because the
literal candidate survives.

**(d) Quantum pressure vs self-gravity.** For a boson of mass `m` at density `ρ`,
`L_Q = (ħ²/(2m²Gρ))^(1/4)` (6). With the P Compton mass `m_P = ħ/(cλ_P) = 6.7105×10⁻⁶¹ kg`
(A56): **548.39 kpc**, 2.28×10⁴ `L*`. To obtain 24 pc one must choose

    m = ħ/(√(2Gρ_c)L*²) = 3.496×10⁻⁵² kg = 1.961×10⁻¹⁶ eV ,                              (7)

a new ultralight boson. The theory has no dark particle (P4): **a fit, not a derivation**
(C4). At `10⁻²² kg/m³` the required mass is `9.316676×10⁻¹⁹ eV` — the answer moves with density.

| candidate | value | coeff | gal. input? | new const? | C1 | C2 | C3 | C4 | verdict |
|---|---|---|---|---|---|---|---|---|---|
| (a) Jeans, cosmic `ρ_c` | 196.2 kpc | 1 | no | no | ✘ | ✔ | ✔ | ✔ | NO-GO |
| (a) Jeans at `10⁻²²` | 932 pc | 1 | **density** | no | ✔ | ✔ | ✘ | ✔ | fit |
| (b) gradient vs `W` | 16.99 pc | 0.707 | no | no | ✘ | ✔ | ✔ | ✔ | circular (λ_P) |
| (b) gradient vs kinetic | 98.1 kpc | 1 | no | no | ✘ | ✔ | ✔ | ✔ | NO-GO |
| (c) literal `t_dyn` | 196.2 kpc | 1 | no | no | ✘ | ✔ | ✔ | ✔ | NO-GO |
| **(c) acceleration `t_acc`** | **24.025 pc** | **1** | **no** | **no** | **✔** | **✔** | **✔** | **✔** | **PASS** |
| (d) quantum with `m_P` | 548.39 kpc | 1 | no | no | ✘ | ✔ | ✔ | ✔ | NO-GO |
| (d) quantum, fitted `m` | 24.025 pc | 1 | no | **yes** | ✔ | ✔ | ✔ | ✘ | fit |

Exactly one row passes all four (K18); no row was admitted by adjusting a coefficient.

## 4. Task 3 — the guard, applied

**(c-accel) passes C2, C3, C4 exactly**: coefficient `1.000000000000000` (K16), no galactic
radius, only `σ_c` and `a0` as inputs. That is the substantive anti-juggling answer — no
*coefficient* is tuned. **C1 is where it becomes honest**: `24.0250 pc` clears the floor
by 0.1042 %, but (i) `σ_c = 8.33 km/s` is A20's *inversion* of `L* = 24 pc`, so feeding it back
is circular at the 2.38 % level; (ii) the independent thermal width `σ_th = 8.226 km/s` gives
**23.4289 pc, 2.38 % below** the floor (K19); (iii) the footing scan (K20) gives canonical
**24.025** (in), alt **19.900** (out), P3 **19.865** (out) — only one of the theory's three
`a0` values clears it. Strict C1: **passed on the circular input, failed by 2.38 % on the
independent thermal input, failed by 17 % on P3.** The derivation *saturates* the floor; it
does not clear it independently. That is not a tuned coefficient — it is a conditional
normalization. Read strictly against the pre-registration, therefore, **no candidate passes
all four criteria on an independent input**: the only row that passes uses
`σ_c = √(a0 × 24 pc)`, which is the 24 pc anchor inverted. The coefficient is not fitted; the normalization is. The honest label is
`FITTED(σ_c)`, not `DERIVED`. Using A20's weaker `f_c = 0.25` ceiling of 180 pc instead
of 1 kpc does not change the ranking: `24.025 pc` is still the only coefficient-free entry
inside, and the `10⁻²²` Jeans reading at 932 pc is now excluded as well.

## 5. Task 4 — verdict

- **Origin.** `L*` is the cold medium's **acceleration-time length at `a0`** — the distance
  travelled at `σ_c` during `t_acc = σ_c/a0`, the time in which the theory's only acceleration
  changes the velocity by `σ_c`; `L* = σ_c²/a0 = (σ_c/c)²L_MOND`.
- **Number.** **24.025 pc** (canonical, `σ_c = 8.33 km/s`); 23.429 pc (independent thermal
  width); 19.865 pc (P3 footing). The record's "24 pc" is the canonical-footing value.
- **Derived or fitted.** **Derived in form, fitted in normalization.** The formula
  `L* = σ_c²/a0` has coefficient exactly 1 and no tuned coefficient, but the only input
  that lands in the window is `σ_c = 8.33 km/s`, which is the 24 pc anchor inverted; the
  independent thermal width gives 23.429 pc, 2.38 % below the floor. So the number
  `24.025 pc` is a one-parameter fit to the anchor, not a zero-parameter prediction.
  Label: `FITTED(σ_c) / CONDITIONAL(canonical a0 footing)`.
- **The one measurement that would turn it into a derivation.** A **core-independent `σ_c`
  at ~1 %** — the cold phase's line width at 30–100 pc in a face-on low-mass dwarf (Hα IFU
  or 21 cm), or the cold-phase temperature to ~2 % (fixes `μ`, hence `σ_th`). That breaks the
  circularity and makes `L* = σ_c²/a0` a zero-parameter prediction. The second item is the
  footing decision: on P3's `a0 = 1.132×10⁻¹⁰` the same formula predicts 19.9 pc.
- **K corollary.** `L*` has no `K`; the `K = 4πG` vs `8πG` dispute moves `γ`, not `L*`.
  `16.988 pc = L*/√2 = λ_P`, not a second `L*` (K21) — A61's open item closed from here.
  **The prompt's `K` parenthetical is reversed:** it assigns `24.02 pc` to `K = 8πG` and
  `16.99 pc` to `K = 4πG`; A61 §4 proves the opposite (`K = 4πG` -> `24.025 pc`,
  `K = 8πG` -> `16.988 pc = λ_P`). This lane follows A61 and the action's EH normalisation.

## 6. Status

`FITTED(σ_c) / CONDITIONAL(σ_c = 10⁴ K cold phase; canonical a0 footing)` for the number;
`DERIVED` for the form `L* = σ_c²/a0` and the K-independence; `NO-GO` for (a), (b), (d)
as derivations.

## 7. Checks

`a65_checks.py`: 24 checks, deterministic, stdlib only, < 0.1 s, no network, exit 0 iff all
pass. `--mutate {coeff2,jeans_rho,footing_alt,quantum,guard}` each exits 1 (MUTATE.md).

| id | proves | measured | threshold |
|---|---|---|---|
| K1 | `L* = σ_c²/a0` | 24.025012 pc | ± 1e-5 |
| K2 | `L*/L_MOND = σ_c²/c²` | residual 0.0 | < 1e-12 |
| K3 | `L_MOND` both footings | 31.118 / 25.7758 Gpc | 9.602 / 7.954 |
| K4 | `c/H0` ratio | 4.448 Gpc; 1.8514×10⁸ | ± 1e-5 rel |
| K5 | `c/H_Λ` ratio | 5.379 Gpc; 2.2389×10⁸ | ± 1e-5 rel |
| K6 | `ℓ₁` ratio | 15.569 Gpc; 6.4803×10⁸ | ± 1e-5 rel |
| K6b | baryon sound speed | 122.0475 kpc; 5080.02 | ± 1e-6 rel |
| K7 | kinetic Jeans | 196.227 kpc; 8.168×10³ | ± 1e-6 rel |
| K8 | elastic Jeans | 106.740 pc; 4.442883 | exact |
| K9 | spacing | 0.904998 m; 1.2208×10⁻¹⁸ | ± 1e-6 rel |
| K10 | `R_s(1 M☉)` | 2954.008 m; 3.9847×10⁻¹⁵ | ± 1e-6 rel |
| K11 | Bohr ratio | 7.1382×10⁻²⁹ | ± 1e-6 rel |
| K12 | no *independent* O(1) multiple | 0 of 11 | 0 independent |
| K12b | thermal baryon near-miss | 23.4289 pc = 0.9752 `L*`; 2.38 % below 24 pc | 0.9752 `L*`; < 24 pc |
| K13 | (a) required density | 1.5054×10⁻¹⁹ kg/m³; 90.00 cm⁻³ | 6.671×10⁷ ρ_c |
| K14 | (b) both readings | 16.988 pc = 0.707`L*` = `λ_P`; 98.11 kpc | 0.707; `λ_J/2` |
| K15 | (c) literal | 196.227 kpc = `λ_J` | ± 1e-12 |
| K16 | (c) acceleration | 24.025012 pc; coeff 1.000000 | exact |
| K17 | (d) `m_P` / fitted `m` | 548.39 kpc; 1.961×10⁻¹⁶ eV | ± 1e-4 / 1e-5 |
| K18 | guard pass count | 1 (c-accel) | 1 |
| K19 | thermal vs window | 23.4289 pc; 2.38 % low | in / out |
| K20 | footing scan | 24.025 / 19.900 / 19.865 pc | 1 in |
| K21 | K-independence | 0.707106781; 16.9882 pc | exact |
| K22 | A20 polytrope edge (prediction) | 53.3146 pc at 24 pc; 53.370 at `L*` | ± 1e-3 |

## 8. What this does not do

1. **No detection.** A20's null stands: 0/175 SPARC curves reach 24 pc.
2. **It does not derive `σ_c`.** The P sector is velocity-blind (A56 K9, `dθ/dT = 0`); the
   chain terminates at the 10⁴ K cold phase. That is the one external input.
3. **It does not resolve the footing.** Canonical and P3 `a0` differ by 21 % and give
   24.025 vs 19.865 pc; both are reported, neither is chosen.
4. **The density legs are models**, not data: the (a) 932 pc uses a nominal `10⁻²² kg/m³`
   and moves as `ρ^(-1/2)`.
5. **`K = 4πG` is assumed** for the `γ`/`λ_P` conversions; the `L*` result itself does not
   depend on it.

## 9. Next

1. **Measure `σ_c` at 30–100 pc** in a face-on dwarf (1 % line width) — the single
   measurement that converts (1) from conditional to closed.
2. **Settle the footing:** `a0 = σ_c²/L*` with the 24 pc anchor prefers `9.36×10⁻¹¹` over
   P3's `1.132×10⁻¹⁰` by 21 % — a prediction of the canonical footing, or a 21 % error in
   the anchor.
3. **Do not** reach 24 pc with the Jeans length: it needs 90 cm⁻³, a molecular cloud, and
   would make `L*` environment-dependent (A56 R2a, excluded by the action).
4. **Retire 16.99 pc as a value of `L*`**: it is `λ_P`; `L*` has no `K`.