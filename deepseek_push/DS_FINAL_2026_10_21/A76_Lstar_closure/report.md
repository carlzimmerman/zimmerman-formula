# A76 — IS `L*` FITTED, OR DERIVED FROM A MEASURED `σ_c`?

Lane A76. `a76_checks.py` — **35 checks, 35/35 PASS, exit 0** (`a76.out`, `a76_results.json`);
**18 single-input mutations, all exit 1, 35/35 checks killed** (`MUTATE.md` + 18 outputs). SI.
`K = 4πG` (A16/A61), `γ = 2πGL*²`, `ρ_c = 5.364ρ_b`, `a0` footings as named. Read first:
**A65** (form `L* = σ_c²/a0`, coefficient exactly 1, guard C1, the 0.1042 %/2.38 % pair), **A20**
(the `[24,90] pc` window, `R_core = (π/√2)L*`, the 53.31 pc core), **A16** (`c_s = 0.7204 m/s`,
`r_switch ∝ L*`), **A71/A72** (`a0 = 8.544e-11` fit; `a0 = 8.618166e-11` thermal; `9.354746e-11`
at κ = ½), **A11 §15** (where the window's two ends come from).

---

## 0. ANSWER

**The 24 pc floor is not a measurement.** It is the 10⁴ K thermal width pushed through
`L* = σ_c²/a0` and rounded up — `23.4289 → 24.000` pc — and then inverted back to `8.33 km/s`. The
"2.38 % failure" of the independent thermal input is therefore **exactly the rounding of the floor**
(2.3796 %), i.e. the theory compared with itself; it is withdrawn as evidence. No datum on disk
excludes `L* = 23.43 pc` — but no datum measures a 53.31 pc core either, because 53.31 pc is the
prediction at the rounded anchor, and the nearest measured core radius is 150 pc.

> **ERRATUM (2026-10-22, doors push D8):** the 24 pc floor is **not** a rounding of the thermal width. It is CFG820's globular χ² bound (NGC 2419, Pal 4, Pal 14), which A11 cites as `LS_LO = 24 pc # [EXT] CFG820` (`a11_checks.py:49`); the fine-grid roots are 23.641 pc (canonical) and 24.476 pc (alt). A datum does bite the thermal value: at the thermal L* the CFG820 χ² gives **Δχ² = 3.91 (canonical, 23.43 pc; excluded at 95 % by a 0.07 margin) and 5.99 (alt, 19.38 pc)**. The 0.46 % agreement between the thermal width and the floor is a coincidence between a premise and a 95 % bound, not a self-comparison. Separately, A76's `L* = σ_c²/a₀` read as the **free-medium** stiffness is excluded by AG6D's C1 (σ_c ≤ 1.70 / 0.845 km/s canonical, frozen / post hoc; 1.87 / 0.928 alt, against 8.2 km/s at 10⁴ K); it can survive only as a property of the **tethered (bound) state**, which no term in the action yet writes. Original text kept as written. See `doors_push_2026_10_22/D8_Lstar_value/README.md`.

**`σ_c` is not measured anywhere on disk.** 175 SPARC curves and 26 LITTLE THINGS curves carry no
dispersion column; ALFALFA's 21 global profiles have 5.148 km/s channels (62.6 % of `σ_c`) and no
spatial information; the only "independent" value is a *computed* thermal width, `8.226 km/s`, whose
mean molecular weight is unmeasured and moves `L*` by a factor **2.333** (`20.41–47.63 pc`).

**`c_s` cannot be measured separately from `L*`.** `γ ≡ KL*²/2` is a definition, so `(γ, L*)` is one
degree of freedom given `ρ_c`; and every elastic observable is suppressed by `(L*/r)²` — `5.76×10⁻²`
at 100 pc, `5.76×10⁻⁴` at 1 kpc, `5.76×10⁻¹⁰` at 1 Mpc. Only inside ~24 pc is the effect O(1), and
nothing on disk resolves 24 pc. That is the obstruction, and it is structural.

**Verdict: (b) still fitted** — `FITTED(σ_c)`, with the fit now located in `μ` (the cold phase's
ionisation state), not in a coefficient. Under the premise "10⁴ K, μ = 1.22" the number is
**23.43 pc** at canonical `a0` and **25.44 pc** at the thermal `a0` — zero free parameters in the
theory, one unmeasured premise in astrophysics.

---

## 1. The identity: `L*` and `c_s` are one degree of freedom (verified)

With `γ = KL*²/2 = 2πGL*²` and `c_s² = γρ_c`,

    L*² = 2c_s²/(Kρ_c)          ⇔    c_s² = γρ_c,  γ = KL*²/2 .

The residual of `2c_s²/(Kρ_c)/L*² − 1` is **0.0** (K1) at `K = 4πG`; at `K = 8πG` the same identity
fails by exactly a factor 2 (mutation `stiff`). Numerically, with `ρ_c = 2.2565×10⁻²⁷ kg/m³`:

| quantity | value | check |
|---|---|---|
| `c_s(L* = 24.000 pc)` | **0.720398 m/s** (A16: 0.720473; 1.0×10⁻⁴) | K2 |
| `c_s(24.025 pc)` | 0.721148 m/s | — |
| `L*(c_s = 0.7204 m/s)` | **24.0001 pc** | K3 |
| `c_s/c` | 2.40299×10⁻⁹ (A16: 2.4032×10⁻⁹) | K14 |
| `ρ_c` from `5.364327 × 0.02237 × 1.87847×10⁻²⁶` | 2.25416×10⁻²⁷ kg/m³ (0.10 % below the record) | — |

The 0.10 % on `ρ_c` is the difference between `Ω_c = 0.2645` (A11) and the `5.364 × Ω_b` route; it
moves `c_s` by 0.05 % and nothing in this lane depends on it.

**So a measurement of `c_s` is a measurement of `L*`, and vice versa.** There is no second handle:
`d ln c_s/d ln L* = 1` exactly at fixed `ρ_c`. This is the fact that decides Task 3.

---

## 2. TASK 1 — the 24 pc floor is a derived round number, and the 2.38 % is its rounding

> **ERRATUM (2026-10-22, doors push D8):** the 24 pc floor is CFG820's globular χ² bound, not a derived round number; the thermal L* has Δχ² = 3.91 (canonical) / 5.99 (alt) against it, so the statement here does not hold. Full correction in §0 erratum and `doors_push_2026_10_22/D8_Lstar_value/README.md`.

### 2.1 Where the floor comes from, line by line

- **A20 `FROZEN_CRITERIA.md` C3**: "`L* ∈ [24 pc, 1 kpc]` — the record's window (**A11 §15**,
  `σ_c = sqrt(a0 L*)` at the two ends)".
- **A11 §15**: "`24 pc ↔ 8.33 km/s` (within 1 % of the **8.23 km/s thermal value for 10⁴ K gas at
  μ = 1.22**, AG6D B7)" — 8.226 km/s computed here (K4).
- **A20 C4**: the reference observable is `σ_thermal = 8.23 km/s (10⁴ K, μ = 1.22)` (8.226, K4).

So the lower end is the thermal width of 10⁴ K gas, `23.4289 pc`, *rounded to 24.0* and inverted to
`8.33 km/s`. Reproduced here: `(8330)²/9.36×10⁻¹¹ = 24.0250 pc` and the C1 margin is **0.1042 %**
(`c1_margin_frac`). The upper end (`90 pc`) *is* a measurement bound (A20 C5, `R0.3 = 200 pc` of
`IC_10`), one-sided and with no error bar.

**Classification: a derived round number.** Not a hard measurement bound and not a 1σ estimate — the
window's bottom is the theory's own preferred answer, written twice. Nothing on disk measures a 24 pc
scale: 0/175 SPARC curves reach it (floor 80 pc = 3.33×, K26/K27), only 2/26 LITTLE THINGS galaxies
have `r_first < 53 pc` (WLM 10.0008 pc, DDO_210 40.0 pc; K23/K24), and the only core bound is the
one-sided `L* ≤ 90 pc`.

> **ERRATUM (2026-10-22, doors push D8):** the 24 pc floor is CFG820's globular χ² bound, not a derived round number; the thermal L* has Δχ² = 3.91 (canonical) / 5.99 (alt) against it, so the statement here does not hold. Full correction in §0 erratum and `doors_push_2026_10_22/D8_Lstar_value/README.md`.

### 2.2 The 2.38 % is the rounding, to four digits

    1 − 23.4289/24.000 = 0.023796  (K8: 0.023914 from the CODATA route, |Δ| = 1.1×10⁻⁴)

A65's guard passes at **0.1042 %** on `σ_c = 8.33 km/s` (the inversion of 24 pc) and fails at
**2.38 %** on `σ_c = 8.226 km/s` (the same thermal width, not rounded). The difference between the
pass and the fail *is* the rounding of one number. **C1 is not a test of the theory; it is a test of
whether 10⁴ K gas rounds up to 24 pc.**

Two further facts make the guard unusable as a discriminator, both computed:

- its margin is **0.025 pc**, against a footing shift of **2.0512 pc** — the guard's whole decision
  sits **81.9× inside** the theory's own `a0` ambiguity (K10, `8.55 %` from A72);
- on the thermal `a0 = 8.618166×10⁻¹¹` the *same* `σ_th` gives **25.4425 pc**, i.e. **6.0 % above**
  the floor and **57.6×** the margin (K11). C1 flips pass/fail on a footing choice, before any datum.

### 2.3 `R_core` of the 23.4289 pc solution

`R_core = (π/√2)L* = 2.221441469 L*` →

| `L*` (pc) | `R_core` (pc) | note |
|---|---|---|
| 23.4289 (A65, `σ = 8.226` quoted) | **52.046** | the 23.4289 pc solution |
| 23.4261 (CODATA route `√(k_BT/μm_H)`) | 52.0396 | K6 checks this against 52.05 |
| 24.000 (the rounded floor) | **53.3146** | A20 K3, K7 |
| difference at the two `L*` | 1.2687 pc = 2.3796 % | — |

K6 checks 52.0396 against the 52.05 of the task's arithmetic; K7 checks 53.3146 against A20.

### 2.4 The decisive question: is 52.05 inside 1σ of an observed 53.31 pc?

**There is no observed 53.31 pc core.** 53.31 pc is `2.22144 × 24.000`: the theory's own prediction at
the rounded anchor, quoted as such in A16 §7, A20 eq. (4) and A58. The on-disk core-radius census —
LITTLE THINGS `table2.dat`, the pseudo-isothermal core radius `Rc` **with its published `e_Rc`** —
reads:

| fact | value | check |
|---|---|---|
| galaxies | 26 | K19 |
| `Rc` range | 150 – 8400 pc | K20 |
| median fractional error `e_Rc/Rc` | 18.27 % | — |
| best fractional error in the sample | 1.35 % (WLM, 740 ± 10 pc) | — |
| galaxies with `Rc < 53.31 pc` | **0 / 26** | K21 |
| galaxies with `e_Rc/Rc < 5 %` | 5 / 26 (smallest `Rc` among them: DDO_101, 320 ± 10 pc) | — |
| galaxies with HI beam < 53.31 pc | 4 / 26 (beams 20.0 – 51.7 pc; median 156.6 pc, K36) | K22 |
| …their `Rc` | 270 ± 120 (IC_10), 200 ± 40 (IC_1613), 740 ± 10 (WLM), 200 ± 50 (DDO_210) | — |

So the four objects that *could* resolve a 53 pc core all return `Rc ≥ 200 pc`, and the sharpest
core radius on disk (WLM, 1.35 %) is 13.88× the prediction — but `Rc` of a pseudo-isothermal halo is
not the edge of a `Γ = 2` polytrope, so neither number is a like-for-like test.

**The 1σ question therefore has no empirical referent: 52.05 and 53.31 pc are the same theory at
`L* = 23.4289` and `L* = 24.000`.** The precision such a test would need is 1.19 % of 53.31 pc =
**0.634 pc** (K30), i.e. **0.13077″ at 1 Mpc** — 31.5× finer than the best LITTLE THINGS beam (20 pc) and
14.6× finer than the best fractional error achieved for any `Rc < 300 pc` (17.4 %, HARO_29; K31).

**The operative question — does any datum exclude `L* = 23.43 pc`? — is answered NO.** The only
kernel-level bound is one-sided (`L* ≤ 90 pc`). A20's best existing core test (DDO_210's innermost
point, 40 pc, an 11.21 % dip at 0.36σ) separates 23.43 from 24.025 at **0.0061σ per galaxy**, and
**0.031σ** stacked over all 26 dwarfs (K32); 1σ would need **27,254** such galaxies.

> **ERRATUM (2026-10-22, doors push D8):** the 24 pc floor is CFG820's globular χ² bound, not a derived round number; the thermal L* has Δχ² = 3.91 (canonical) / 5.99 (alt) against it, so the statement here does not hold. Full correction in §0 erratum and `doors_push_2026_10_22/D8_Lstar_value/README.md`.

### 2.5 Task 1 result

The floor is soft, the "2.38 % failure" is withdrawn, and **`L* = 23.43 pc` is allowed** — every datum
on disk is consistent with it. But being *allowed* is not being *measured*: the number that lands
there is the same 10⁴ K thermal width that defined the floor, so removing the floor removes a
discrepancy, not a fit.

---

## 3. TASK 2 — `σ_c` is not measured anywhere on disk

### 3.1 Every candidate determination, and its status

| # | source (on disk / quoted) | what it actually is | independent of `L*`? | usable as `σ_c`? |
|---|---|---|---|---|
| 1 | **10⁴ K thermal width** (A11 §15, AG6D B7; formula `√(k_BT/μm_H)`) | a *computed* width, `8.2255 km/s`, from an assumed `T` and `μ` | **yes** (no `L*` in it) | **estimate only** — not a measurement of this component; `μ` unmeasured |
| 2 | observed cold/warm HI range **6–10 km/s** (A20 C4, `[EXT]`, no dataset on disk) | a literature range, no per-galaxy error, no citation on disk | yes | weak: factor 2.8 → `L*` = 12.46–34.62 pc |
| 3 | **ALFALFA** 21 global profiles (`hi_profiles_2026_10_18/*.fits`) | 1024 channels over 24.975586 MHz = **5.148 km/s**/channel; beam 3.3′×3.8′; one spectrum per galaxy, **zero spatial information** | yes | **no** — channel width is 62.6 % of `σ_c` (K28/K29), and `W50 ≈ 2V_rot` is rotation-dominated |
| 4 | **SPARC** 175 `*_rotmod.dat` | columns `Rad, Vobs, errV, Vgas, Vdisk, Vbul, SBdisk, SBbul` — **no dispersion column**; median `errV` = 4.6 km/s = **0.559 σ_c** | yes | **no** — a rotation curve's *error* is half the target width |
| 5 | **LITTLE THINGS** 26 dwarfs (`rotdmbar.dat`, `rotdm.dat`) | scaled rotation curves only; no second-moment cube on disk | yes | **no** |
| 6 | **MIGHTEE-HI DR1** 7 cubes | 79.3 kpc linear resolution (A20 §9) | yes | **no** |
| 7 | cluster gas temperatures | the hot ICM, `T ~ keV` ⇒ `σ ~ 10³ km/s`, 122× the cold width; A18's amplitudes are mass ratios (`R_req = 5.552 ± 0.427`, K33) with no velocity dispersion | yes | **no** — wrong phase |
| 8 | cold-sector share `Ω_c = 5.364 Ω_b` (A9/A11) | a **density** ratio, not a dispersion | yes | **no** — fixes `ρ_c`, which converts `c_s` to `γ`, nothing about `σ_c` |
| 9 | **A65's `8.33 km/s`** | the inversion of `24 pc` | **no** — circular | no |

**Measured determinations of `σ_c`: zero.** Not "few" — none in the datasets this lane opened.

### 3.2 The best independent `σ_c`, with its error

    σ_c = 8.226 km/s,  +3.5 / −0.55 (μ ∈ [1.40, 0.60])  and  ±10 % (T ∈ [0.8, 1.2]×10⁴ K)

The μ band is the dominant term: `σ ∝ μ^(−1/2)`, so `μ = 0.60` (fully ionised) gives 11.729 km/s and
`μ = 1.40` gives 7.679 km/s. That is a factor 1.528 in `σ_c` and **2.333 in `L*`**.

### 3.3 `L* = σ_c²/a0` at the three footings, with errors

| `a0` (m/s²) | `L*` at μ = 1.22, T = 10⁴ K | μ = 0.60 | μ = 1.40 | T = 0.8×10⁴ | T = 1.2×10⁴ |
|---|---|---|---|---|---|
| **9.36×10⁻¹¹** (canonical) | **23.426 pc** | 47.6329 | 20.414 | 18.74 | 28.111 |
| **9.354746×10⁻¹¹** (κ = ½) | **23.439 pc** | 47.6597 | 20.4256 | 18.751 | 28.127 |
| **8.618166×10⁻¹¹** (thermal) | **25.4425 pc** | 51.733 | 22.171 | 20.354 | 30.531 |

Two facts from this table:

1. **The canonical and κ = ½ footings are the same footing** — they differ by 0.013157 pc (K12),
   because `1/7 × cH0 = 9.354746×10⁻¹¹` and BRIEF's `a0 = 9.36×10⁻¹¹` are the same number to 3 s.f.
   The live choice is canonical/κ = ½ vs thermal, `8.55 %`.
2. **`L*` is 23.43 pc with a factor-2.33 systematic and an 8.5 % footing term.** Under reading (a) —
   if `σ_c` were a measurement — the number would be `L* = 23.43 (+24.2 / −3.0) pc` (canonical) or
   `25.44 (+26.3 / −3.3) pc` (thermal). The error bar is not statistical: the formula is exact.

Note the sign flip: at the thermal `a0` the thermal `σ_c` gives **25.44 pc, 6.0 % above the 24 pc
floor**, where at canonical `a0` the same input gives 2.38 % below it. The guard's verdict is decided
by the footing, not by the data.

---

## 4. TASK 3 — the `c_s` route: no observable constrains `γ` alone

### 4.1 The structural statement

    γ = KL*²/2   (definition, not a parameter)      c_s² = γρ_c      ⇒  c_s = √(Kρ_c/2) · L*

Given `ρ_c` from cosmology (`5.364 ρ_b`), `(γ, L*)` is **one** degree of freedom. So "measure `γ`
alone" is not a well-posed request: any measurement of `c_s` *is* a measurement of `L*`, and any
measurement of `L*` *is* a measurement of `c_s`. The elastic sector has one dimensionful parameter and
therefore one observable.

### 4.2 The four probes, each computed

| probe | what it measures | does it contain `γ`? | sensitivity to `γ` at fixed `a0`, `ρ_c` |
|---|---|---|---|
| **(a) cluster pressure / non-thermal support (A18)** | `A_law = 1.9102 ± 0.1186`, `A_newton = 10.17 ± 0.65`, `A_HUT = 1.0109 ± 0.0632` → `λ_req = 2.1207 ± 0.163`, `R_req = 5.552 ± 0.427` | **no** — `F(y) = ½[√(1+4/y)−1]` is a mass ratio; `u = 0.45 ± 0.03` is a *sourcing fraction*, not a velocity | **0** (K33 reproduces `R_req = 5.55177` from the amplitudes alone) |
| **(b) splashback step (A29)** | `r_sp = 1.41 Mpc`, 0.3 % from the model-independent caustic at 1.42 Mpc | **no** — outside `r_sp` the medium is single-stream, `p = 0` *by construction*: the step tests the **sign** of the stress, not its magnitude | **0** — and the cold-medium pressure at `r_sp` is `2.90×10⁻¹⁰` of gravity (`press_rsp`, K17) |
| **(c) RAR knee width** | the law `g_N = g²/(g+a0)` and its knee at `g_N = a0` | **no** — the law contains `a0` only | **exactly 0** (K34: the RAR value at `g_N = a0` is bit-identical for `γ` and `2γ`) |
| **(d) Jeans mass in the dwarf mass function** | `M_J = (4π/3)ρ R_core³`, `R_core ∝ L*` ⇒ `M_J ∝ ρ L*³ ∝ ρ γ^{3/2}` | **yes**, but only as `ρ γ^{3/2}` | **not separable**: one equation, two unknowns (`ρ` at the fragmentation site is not measured). At the cosmic cold density `M_J = 0.021159 M_⊙` (K18) — 8 dex below any dwarf, so the dwarf mass function cannot see it at all |

So (a), (b), (c) are **exactly** `γ`-free, and (d) is degenerate with the density. No probe constrains
`γ` alone.

### 4.3 Why, in one line of numbers

The elastic force is `(L*/r)²` of gravity in every cusp with `1 ≤ n ≤ 2` (A16 eq. 11):

| `r` | 1 pc | 24 pc | 100 pc | 1 kpc | 1 Mpc | 1.41 Mpc |
|---|---|---|---|---|---|---|
| `(L*/r)²` | 576 | 1 | 5.76×10⁻² | **5.76×10⁻⁴** | **5.76×10⁻¹⁰** | **2.90×10⁻¹⁰** |

Cluster observables sit at `10⁻¹⁰`; the RAR region sits at `10⁻⁴`; **only inside `L*` is the effect
O(1)**. The single observable of the elastic sector is the core at 24–53 pc, and §2.4 shows that
nothing on disk resolves it.

### 4.4 The named obstruction

> **The elastic sector of this theory is one-dimensional.** `γ = KL*²/2` is a definition; `c_s` and
> `L*` are the same number in two units. There is no second elastic observable because there is no
> second elastic parameter, and the one elastic observable — the core at 53 pc — lies below the HI
> beam of 22 of the 26 LITTLE THINGS dwarfs and below the innermost reliable radius of every one of
> the 175 SPARC curves. Any claim to have "measured `γ` independently" is either a measurement of
> `L*` (i.e. the core) or an assumption about `μ` (i.e. `σ_c`) — the two things this lane was asked
> to separate.

---

## 5. TASK 4 — verdict

**(b) STILL FITTED.** Not (a): no independent measurement of `σ_c` exists (§3.1: zero). Not (c): `L*`
is not a second scale the theory cannot fix — the theory fixes its *form* and its coefficient
**exactly 1**, and ties it to `c_s` by an exact identity (§1). What is missing is one astrophysical
premise, not a theoretical one.

The precise statement, which is narrower than A65's and harder on it:

- **Coefficient: not fitted.** `L* = σ_c²/a0`, coefficient `1`, no `K`, no galactic
  radius, no new constant (A65 C2–C4, re-verified here through K1–K3).
- **Number: fitted through `μ`.** The best available `σ_c` is a *computed* 10⁴ K thermal width, and
  `L* ∝ 1/μ` moves the answer over `20.41–47.63 pc` (factor 2.33) for the plausible ionisation range.
- **The "2.38 % failure" is withdrawn.** It is the floor's own rounding (2.3796 %), and the floor is a
  derived round number, so `L* = 23.43 pc` is not excluded by anything.
  - **ERRATUM (2026-10-22, doors push D8):** the 24 pc floor is CFG820's globular χ² bound, not a derived round number; the thermal L* has Δχ² = 3.91 (canonical) / 5.99 (alt) against it, so the statement here does not hold. Full correction in §0 erratum and `doors_push_2026_10_22/D8_Lstar_value/README.md`.
- **Under reading (a), if `σ_c` were measured:** `L* = 23.43 (+24.2 / −3.0) pc` at canonical `a0`,
  `25.44 (+26.3 / −3.3) pc` at the thermal `a0`. Both are conditional on "10⁴ K, μ = 1.22".

**What single measurement settles it, and to what precision.** Two questions, two answers:

1. *To make `L*` a prediction rather than an inversion* — measure `σ_c` in the cold phase itself,
   independent of `L*`: an **HI second-moment (velocity-dispersion) map of a face-on low-mass dwarf at
   30–100 pc resolution, `σ_c` to 5 % = 0.411 km/s** (`sigma_for_10pct_L_km_s`). Since `L* ∝ σ_c²`,
   that gives `L*` to 10 % (2.34 pc) — a real prediction, and it breaks the circularity. The 2.5 %
   point (`sigma_for_5pct_L_km_s` = 0.2056 km/s) gives `L*` to 5 %. **Achievable** with ~10²
   independent beams at 5 km/s channels.
2. *To test the coefficient (1 vs 1 + 2 %)* — `σ_c` to **0.5 % = 0.041 km/s**
   (`sigma_for_1pct_L_km_s`), 100× below the 5.148 km/s channel width of every HI dataset on disk.
   **Not achievable.**
3. *To decide 23.43 vs 24.025 pc without `σ_c`* — `R_core` to **1.19 % (0.634 pc, 0.13077″ at 1 Mpc)**
   (K30), 14.6× better than any measured core radius in that size range (K31). Not achievable now;
   it is A20's ngVLA forecast (0.15″ at 4 Mpc = 2.9 pc), which is still 4.6× too coarse for 0.634 pc
   at 4 Mpc.

**The honest bottom line: `L*` is not derived. It is `σ_c²/a0` with the right coefficient and the
wrong input — an input that has never been measured for this component, and that cannot be measured
by any instrument now operating at the precision the claim requires.**

---

## 6. Status

| task | state | one-line reason |
|---|---|---|
| 1 — is the 24 pc floor hard? | **CLOSED-NO-GO** | it is a derived round number (23.4289 → 24.000); the 2.38 % is its rounding (2.3796 %); no datum excludes 23.43 pc, and none measures 53.31 pc |
| 2 — is `σ_c` independently measured? | **CLOSED-NO-GO** | zero measured determinations on disk; best value is a computed 10⁴ K width, `μ`-systematic at factor 2.33 |
| 3 — the `c_s` route | **CLOSED-NO-GO(obstruction)** | `γ ≡ KL*²/2` is one dof with `L*`; every probe is `γ`-free or `ρ`-degenerate; effect is `(L*/r)²`, O(1) only inside 24 pc |
| 4 — verdict | **FITTED(σ_c) / CONDITIONAL(10⁴ K cold phase)** | coefficient 1 is derived; the number is not |

**ERRATUM (2026-10-22, doors push D8):** (task 1 row) the 24 pc floor is CFG820's globular χ² bound, not a derived round number; the thermal L* has Δχ² = 3.91 (canonical) / 5.99 (alt) against it, so the statement here does not hold. Full correction in §0 erratum and `doors_push_2026_10_22/D8_Lstar_value/README.md`.

---

## 7. Checks

`a76_checks.py`: 35 checks, deterministic, stdlib only, ~0.4 s, no network, reads four read-only
datasets, exit 0 iff all pass. 18 mutations, all exit 1, **35/35 checks killed** (`MUTATE.md`).

| id | proves | measured | threshold |
|---|---|---|---|
| K1 | identity `L*² = 2c_s²/(Kρ_c)` exact at `K = 4πG` | ratio 1.0, residual 0.0 | < 1e-12 |
| K2 | `c_s(24 pc)` vs A16 0.720473 m/s | 0.720398 | 5e-4 |
| K3 | `L*(0.7204 m/s)` vs 24.000 pc | 24.0001 | 1e-3 |
| K4 | `σ_th(10⁴ K, μ=1.22)` vs 8.226 km/s | 8.22551 | 1e-4 |
| K5 | `L*_th` from `(T, μ, m_H)` vs A65 23.4289 pc | 23.4261 | 3e-4 |
| K6 | `R_core(L*_th)` vs 52.05 pc | 52.0396 | 1e-3 |
| K7 | `R_core(24.000 pc)` vs A20 53.3146 pc | 53.3146 | 1e-5 |
| K8 | the 2.38 % **is** `1 − 23.4289/24` | 0.023914 | abs 1e-3 |
| K9 | `a0` footing spread vs A72 8.55 % | 0.0854683 | 1e-3 |
| K10 | footing shift / C1 margin | 81.9 | ≥ 50 |
| K11 | `L*(thermal a0) − 24` in units of the margin | 57.62 | ≥ 50 |
| K12 | `|L*(κ=½) − L*(canonical)|` | 0.013157 pc | < 0.02 pc |
| K13 | `L*(μ=1.40)` vs 23.4289 × 1.22/1.40 | 20.4141 | 2e-4 |
| K14 | `c_s/c` vs A16 2.4032e-9 | 2.40299e-9 | 1e-2 |
| K15 | elastic/gravity at 1 kpc vs A16 5.76e-4 | 5.76e-4 | 2e-3 |
| K16 | elastic/gravity at 1 Mpc | 5.76e-10 | < 1e-8 |
| K17 | elastic/gravity at A29 `r_sp` vs 2.90e-10 | 2.8972e-10 | 2e-2 |
| K18 | Jeans mass at `ρ_c`, `R_core(24 pc)` vs A16 0.0212 `M_⊙` | 0.021159 | 5e-3 |
| K19 | LITTLE THINGS census vs A20 26 | 26 | exact |
| K20 | smallest measured `Rc` | 150 pc | exact |
| K21 | galaxies with `Rc < 53.31 pc` | 0 | exact |
| K22 | galaxies with HI beam < 53.31 pc | 4 | exact |
| K23 | innermost LT radius vs A20 10 pc | 10.0008 pc | 2e-4 |
| K24 | LT galaxies with `r_first < 53.31 pc` | 2 | exact |
| K25 | SPARC census vs A20 175 | 175 | exact |
| K26 | SPARC `r_first` floor vs A20 80 pc | 80 pc | exact |
| K27 | SPARC curves inside 24 pc | 0 | exact |
| K28 | ALFALFA channel width | 5.14783 km/s | 1e-3 |
| K29 | channel width / `σ_th` | 0.6258 | 1e-3 |
| K30 | `R_core` 1σ precision needed | 0.6343 pc | 1e-2 |
| K31 | best `e_Rc/Rc` for `Rc < 300 pc` | 0.1739 | 1e-3 |
| K32 | stacked significance of the 2.38 % question (26 dwarfs) | 0.030887σ | 5e-3 |
| K33 | A18 `R_req` from the three amplitudes vs 5.552 | 5.55177 | 1e-3 |
| K34 | RAR unchanged under `γ → 2γ` | 0.0 | abs 0 |
| K36 | median LT HI beam vs A20 156.6 pc | 156.557 | 1e-3 |

(K35 was deleted: `R_core ∝ L*` makes `R_core(√2L*)/R_core(L*) = √2` an algebraic identity that no
single-input mutation can break. `d ln M_J/d ln γ = 3/2` was deleted for the same reason. Both are
reported above as ratios, not as checks — see `MUTATE.md`.)

---

## 8. What this does not do

1. **It does not measure `σ_c`.** It establishes that nothing on disk does. The value 8.226 km/s is a
   computation from `(T, μ)`, and `μ` is the unmeasured quantity.
2. **It does not fit a rotation curve.** The 52.05 vs 53.31 pc comparison is between two theory
   points; a proper `χ²` against WLM/DDO_210 data would require the full baryonic model, inclination
   and beam smearing, and would still be limited by A20's 0.36σ per-galaxy dip.
3. **`Rc` (pseudo-isothermal) is not `R_core` (Γ = 2 polytrope).** The census in §2.4 is used as a
   *resolution and error-bar* benchmark, not as a like-for-like measurement of the theory's core.
   The four beam-resolved objects returning `Rc ≥ 200 pc` is a tension, not an exclusion.
4. **The `μ` range [0.60, 1.40] is a physical bracket, not a measured interval.** It is what the
   factor-2.33 systematic means; a measured ionisation state would replace it.
5. **The 27,254-galaxy figure assumes** A20's per-galaxy dip error (0.36σ at 11.21 %) scales as
   `1/√N` and that the dip is the statistic; a shape fit would do better, but not by the 10² needed.
6. **No new data.** Every file is read-only and in place; no raw data is copied into the lane.

---

## 9. Next

1. **The measurement that closes the circularity**: HI second-moment mapping of a face-on dwarf at
   30–100 pc resolution, `σ_c` to 5 % (0.41 km/s). That is the *only* route to `L*` as a prediction,
   and it needs no new theory.
2. **Do not** re-run SPARC or LITTLE THINGS for this: they have no dispersion column (SPARC) or no
   second-moment cube (LT), so no reanalysis can produce `σ_c`.
3. **Stop quoting the 24 pc floor as a bound.** It is 23.4289 pc rounded up, and the rounding is the
   whole of the "2.38 % failure". If a floor is wanted, state it as the premise it is:
   `CONDITIONAL(cold phase at 10⁴ K, μ = 1.22)`.
4. **Retire the guard C1 as a discriminator** until `a0`'s footing is fixed: its margin (0.025 pc) is
   81.9× inside the footing spread (2.05 pc), so it cannot decide anything before the footing does.

---

## VERDICT (one paragraph)

**VERDICT.** `L*` is **(b) still fitted** — `FITTED(σ_c)` — and the fit is not where A65 said it was. The 24 pc floor is not a measurement: it is the 10⁴ K thermal width pushed through `L* = σ_c²/a0` and rounded up (`23.4289 → 24.000` pc), so the "2.38 % failure" of the independent thermal input is exactly that rounding (`2.3796 %`), a comparison of the theory with itself, and it is withdrawn as evidence; no datum on disk excludes `L* = 23.43 pc`, whose predicted core is `52.046 pc`, and no datum measures `53.31 pc` either, because 53.31 pc is `2.22144 × 24.000`, the theory's own prediction at the rounded anchor — the nearest *measured* core radius is `150 pc` and the sharpest is WLM's `740 ± 10 pc`, so the 1σ test the floor implies would need `0.634 pc` (`1.19 %`, `0.13077″` at 1 Mpc), `14.6×` finer than any core radius measured in that size range and `31.5×` finer than the best LITTLE THINGS beam. Nothing on disk measures `σ_c`: 175 SPARC curves and 26 LITTLE THINGS curves carry no dispersion column, ALFALFA's 21 global profiles have `5.148 km/s` channels (`62.6 %` of `σ_c`) and no spatial information, MIGHTEE resolves `79.3 kpc`, and the cluster amplitudes are mass ratios — so the only "independent" value, `8.226 km/s`, is a *computed* thermal width whose mean molecular weight is unmeasured and moves the answer from `20.414` to `47.6329 pc` (factor `2.333`); at the three footings the number is `23.426 pc` (canonical), `23.439 pc` (κ = ½ — the same footing, `0.013157 pc` apart) and `25.4425 pc` (thermal), each `±` that factor, with the canonical/thermal choice alone worth `8.55 %`. `c_s` cannot be separated from `L*` to fix this: `γ = KL*²/2` is a definition, so `(γ, L*)` is one degree of freedom, and the elastic force is `(L*/r)²` of gravity — `5.76×10⁻²` at 100 pc, `5.76×10⁻⁴` at 1 kpc, `5.76×10⁻¹⁰` at 1 Mpc — so A18's cluster ratios, A29's splashback step and the RAR knee are *exactly* `γ`-free while the Jeans mass constrains only the combination `ρ γ^{3/2}`; the obstruction is that the elastic sector is one-dimensional and its only observable, the core at 53 pc, lies below the beam of 22 of the 26 dwarfs and beyond the innermost reliable radius of all 175 SPARC curves. The coefficient is exonerated (exactly 1, no `K`, no galactic radius, no new constant); the number is not: it is `L* = 23.43 (+24.2 / −3.0) pc` at canonical `a0` if `σ_c` were measured, and what would make it a prediction is an HI second-moment map of a face-on dwarf at 30–100 pc resolution giving `σ_c` to `5 %` (`0.411 km/s`) — achievable; testing the coefficient itself would need `0.5 %` (`0.041 km/s`), a hundred times below the channel width of every HI dataset on disk, and is not achievable.
