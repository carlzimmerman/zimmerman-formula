# A24 — the wide-binary contradiction: does the framework's own law predict 1.51 or 1.18?

**Lane A24**, `DS_FINAL_2026_10_21`. Deliverables: `report.md`, `a24_checks.py`, `a24.out`, `a24_results.json`, `MUTATE.md`.

---

## Claim

**The framework's law predicts 1.18, not 1.51.** The law `g_N = g²/(g + a₀)` relates the observed and
baryonic accelerations *at a point*; at a wide binary its argument `g_N` is the binary's own field
**plus the Galaxy's**. Evaluating the same law with the Galactic field deleted gives γ_v = 1.51 at
20 kAU; evaluating it with the field present gives **γ_v = 1.1771–1.1933** across the four
kernel/inversion combinations (1.1811 in the registration's own) — every one within **0.012**, i.e.
0.6 σ_fit, of the Arm A band top 1.1814. The EFE is therefore **not** something the
law lacks: ν has no `g_ext` argument, but neither does AQUAL's μ, and AQUAL is the textbook EFE
theory — the law *is* AQUAL with `μ(x) = x/(1+x)` (exact, eq. 2 below). "No EFE" is a choice of what
one puts into `g_bar`, not a property of ν. **The document in error is the October record (Zenodo
23251278), in its wide-binary sentence. The September registration stands and must not be amended
numerically.** The October number is also outside the framework's own pre-registered scoreable range
(1.51 > 1.23 = "no hypothesis verdict permitted"), so it could never have been scored as a framework
confirmation even if it were right.

---

## Derivation

### 1. The law, and the exact identity that settles the "EFE-free" claim

With `y ≡ g_N/a₀`, `x ≡ g/a₀`, the frozen law `g_N = g²/(g + a₀)` inverts to

  (1)  `g = (g_N/2)(1 + √(1 + 4a₀/g_N))`,  `ν(y) = ½(1 + √(1 + 4/y))`,  `ν → 1 + 1/y` (y≫1),  `ν → y^-1/2` (y≪1).

Solving (1) for `g_N` gives `y = x²/(x + 1)`, hence

  (2)  **`μ(x) ≡ y/x = x/(1 + x)`  exactly.**

Eq. (2) is the argument in one line. The framework's law *is* the AQUAL law with `μ(x) = x/(1+x)`.
AQUAL has an EFE **because the external field enters the argument of the nonlinearity**. `μ` is a
function of one variable and AQUAL still has an EFE. So "ν is a function of `g_bar` only" does **not**
imply "no EFE"; it says only that there is no *separate* `g_ext` slot. Whether an EFE exists is decided
by whether `g_bar` at the system is the local total field (EFE present) or the system's own field with
the external part subtracted (EFE absent, non-local).

**Proposition (implicit EFE).** Let `g = ν(|g_b|/a₀) g_b` with ν differentiable and not constant, and
let `g_b = g_e + g_i`, `|g_i| ≪ |g_e|`. Then
`δg = [ν(y_e) I + y_e ν'(y_e) ê êᵀ] g_i`, which equals `ν(y_i) g_i` only if `y_e = y_i`. The internal
dynamics of a bound system therefore changes at O(1) when it is placed in an external field — for any
ν, including one with a single argument. The only escape is to define `g_b` as the system's own field,
i.e. to remove `g_e` by hand, which is not a local functional of the mass distribution.

*Modified inertia is the exception, and it is not available here.* An MI law has no local field
equation, so "the boost of a binary in the Galaxy" is not a functional of the instantaneous field; but
the framework's operative arm is modified gravity (Arm A is its AQUAL quasi-static solve) and its
ontology is a local medium with `div P = ρ − ρ̄`. Under MI the framework would owe a different,
non-local calculation — and 1.51 is not it either, since 1.51 is the isolated algebraic value.

For this binary: `y_i = 0.3169` at 20 kAU, `y_e = 1.1571` (from `x_ext = 1.8`, §3), so
`ν(y_i)/ν(y_e) = 1.5078`. **The Galaxy suppresses the acceleration boost by 1.51× (1.23× in γ_v).**

### 2. Task 1 — the exact integral, and the no-EFE numbers

The two-body relative acceleration is computed from the QUMOND form of (1):

  (3)  `∇²Φ_N = 4πGρ`,   `∇²Φ = ∇·[ν(|∇Φ_N|/a₀) ∇Φ_N]`,
  (4)  `g = g_N + g_ph`,  `g_ph(r) = −(1/4π) ∫ d³x′ ∇′·[(ν−1) g_N](x′) (r − x′)/|r − x′|³`.

With the stars on the z-axis at `z₁ = −r₀/2`, `z₂ = +r₀/2`, in units `G = a₀ = M_tot = 1`
(`r₀ = √(M_tot/y_tot)`), and `S ≡ −ν′(y)(∇|g_N|·g_N)`, the axisymmetric quadrature evaluated is

  (5)  `a_ph,z(z*) = −½ ∫∫ S(ρ,z) (z* − z) ρ [ρ² + (z* − z)²]^(−3/2) dρ dz`,
  (6)  `a_rel = GM_tot/r₀² + [a_ph,z(z₁) − a_ph,z(z₂)]`,  `γ_v = √(a_rel/a_N)`,  `a_N = GM_tot/r₀²`.

Grid: `n_ρ = 480`, `n_z = 960`, log-spaced `10⁻³r₀` to `3×10³r₀`. The `q → 0` control returns
`ν(y) − 1` to 3.4% (K3), which is the check that (4)–(6) are the right object.

**Assumption about the internal acceleration of each star (stated, because it is where the answer
could hide).** Three readings exist; only one is live.

- *(a) Surface self-field.* A solar-type star has `g_self = GM/R² = 274.27 m/s² = 2.93×10¹² a₀`. If ν
  were evaluated on the total field at each stellar surface, `ν − 1 = 3.4×10⁻¹³` and
  `γ_v − 1 = 1.7×10⁻¹³` — **no boost at all**. Excluded: it would switch MOND off inside every galaxy,
  since every star there sits in its own deep field. It is not a suppression of the binary boost; it
  is a refutation of the law.
- *(b) Total-mass composition.* Each star a point test mass in the other's field,
  `a_rel = ν(y_tot) a_N`. This is PAPER44's recipe (`γ_v = √ν`) and it is an **overestimate**.
- *(c) Exact two-body composition.* Eqs. (5)–(6). Nonlinear superposition reduces the excess by
  `f₂ ≡ ε_exact/ε_totmass = 0.721` at 20 kAU (`0.668` at 10 kAU). The deep-MOND closed form
  (`a_ex = 0.781` for q = 1) is the `y→0` limit of the same factor. **(c) is the live reading.**

Numbers (1.0 + 1.0 M☉, circular orbit, `v² = a_rel s`):

| s [kAU] | y_tot (can) | **canonical** total-mass | **canonical** exact (c) | alt total-mass | alt exact (c) |
|---|---|---|---|---|---|
| 10 | 1.26744 | 1.2326 | **1.1605** | 1.2636 | 1.1848 |
| 20 | 0.31686 | 1.5315 | **1.4037** | 1.5859 | 1.4493 |

**With no external field the law predicts 1.53 (20 kAU) in the total-mass convention and 1.40 in the
exact one** — both far above Arm A. The composition suppression is real but worth only 0.128 in γ_v
(20 kAU); it cannot take 1.51 to 1.18.

### 3. Task 2 — the EFE, imposed inside the same law

The external field enters (5) only through `y = |g₁ + g₂ + g_ext|/a₀`. Nothing else changes: same law,
same integral, same code. With the standard local field `x_ext = 1.8 a₀` (observed; its Newtonian
counterpart from (1) is `y_ext = 1.1571`), field **along** the separation (`θ = 0`, the maximal
orientation):

| s [kAU] | EFE-blind exact | **EFE-present exact** | `√ν(y_ext)` (parallel bound) | `√⟨B⟩` (orientation average) |
|---|---|---|---|---|
| 10 | 1.1605 | **1.100** (1.107 canonical) | 1.2472 | 1.2005 |
| 20 | 1.4037 | **1.181** (1.193 canonical) | 1.2472 | 1.2005 |

**1.1811 at 20 kAU against the registered Arm A top 1.1814 — 0.0003.** The four kernel/inversion
combinations span 1.1771–1.1933 (`y_ext` from the canonical or the RAR closure × RAR or canonical
kernel), i.e. the band top ±0.012. With the repo's own closed-loop `x_ext = 1.8996` the computation
gives 1.1732; with the alt footing (`x_ext = 1.5764`) 1.2094 against Arm A-alt's 1.1917–1.2267. Two
independent routes to the registered band, one of them the exact quadrature.

*The framework's law vs AQUAL.* Both are (1)–(2). At the saturated order the EFE tensor is
`B_par = ν(y_e) = 1.5556`, `B_perp = ν(y_e)/√(1+L₀) = 1.3841`, `L₀ = −d ln ν/d ln y = 0.2632` — exactly
what the repo's full nonlinear AQUAL solve uses (its V3 check), and exactly what the quadrature
reproduces (`√1.5556 = 1.2472`, the parallel bound). The QUMOND-vs-AQUAL difference is second order:
the repo's own two solvers agree to **0.005** at the recovered-γ̂ level and **0.016** profile-level
(PREREG Amendment 10 note), and that is the largest honest estimate of the fork. So

  `Δγ = 1.5315 − 1.1811 = 0.350 = 12.7 σ_tot`  vs  `Δγ(QUMOND − AQUAL) ≤ 0.019 = 0.7 σ_tot`  → **18×**.

**Answer to task 2: "no EFE" is a choice of solver, not a property of the law.** The solver fork is
18× smaller than the EFE effect and cannot produce it. The consequence runs opposite to the EFE-free
claim: the Galaxy *does* suppress the boost, by `ν(y_ext)/ν(y_int) = 1.5078` in acceleration.

*Declared sensitivity.* Read as the **Newtonian** external field (`y_ext = 1.8`), the 20 kAU number is
1.1359 (RAR) / 1.1515 (canonical), below Arm A; Amendment 4b's closure inversion of the **observed**
field is operative, so 1.1571 / 1.2445 are used.

### 4. Task 3 — which document is wrong, and what the corrected arm reads

**The October record is wrong; the registration is right.** The chain, one choice at a time at 20 kAU:

| step | γ_v | Δ |
|---|---|---|
| the paper's recipe: quadrature law, 1.5 M☉, total mass, **no EFE** | 1.5107 | — |
| kernel → canonical ν at 1.5 M☉ | 1.6160 | +0.1053 |
| mass → 2.0 M☉ | 1.5315 | −0.0845 |
| composition → exact two-body | 1.4037 | −0.1278 |
| **impose the Galactic field** | **1.1933** | **−0.2104** |

Kernel and mass nearly cancel (+0.105 / −0.085); composition costs 0.128; **the EFE costs 0.210, the
single largest step.** And 1.51 is *exactly* the paper's recipe (K2 reproduces 1.0104 / 1.0601 /
1.1969 / 1.5107 at 2 / 5 / 10 / 20 kAU against 1.01 / 1.06 / 1.20 / 1.51) — so the October number is
not a mistake in arithmetic, it is a correct computation of a different theory.

Three reasons that theory is not the framework's:

1. It has no completion. PAPER44 says of the EFE-blind sector: "No covariant theory with this property
   exists yet."
2. The law *is* a completion — AQUAL with `μ = x/(1+x)` — and that completion has the EFE.
3. Its number is unscoreable: γ̂ > 1.23 is the guard zone, "no hypothesis verdict permitted", and the
   *registered* no-EFE benchmark 1.33 already sits there (CFG943: 100% of MOND-benchmark mocks land in
   it). A 1.51 detection would read "contamination-dominated or EFE-shape failure", never confirmation.

**Corrected text for Zenodo 23251278** (its wide-binary sentence; the same sentence appears in
PAPER44's abstract and §5):

> "Wide binaries are predicted at γ_v = 1.1614–1.1814 (canonical) / 1.1917–1.2267 (alt) — the
> registered Arm A, which includes the Galactic external field — or at γ_v ≤ 1.045 for the screened
> covariant candidate (Arm B). The values 1.20 at 10 kAU and 1.51 at 20 kAU are the predictions of an
> **EFE-blind** MOND sector, which this paper argues the data prefer but for which no covariant theory
> exists; they are not the framework's registered prediction and must not be reported as one."

**Corrected arm:** no numerical change. Arm A stays 1.1614–1.1814 / 1.1917–1.2267; what is needed is a
*declarative* amendment — Arm A presumes the local (EFE-present) reading, and the EFE-blind alternative
(1.33 pooled; 1.20 / 1.51 per bin) is the benchmark the guard zone already uses. Adopting EFE-blindness
instead would cost the covariant parent and the ability to score DR4 in the same stroke.

### 5. Task 4 — the decisive measurement

  `Δγ(20 kAU) = 1.51 − 1.1814 = 0.3286`  →  **11.9 σ_tot** at the frozen resolution (σ_tot = 0.0276),
  `Δγ(20 kAU) = 1.4037 − 1.1933 = 0.2104` →  **7.6 σ_tot** like-for-like (same composition, EFE on/off),
  `Δγ(10 kAU) = 1.1969 − 1.1814 = 0.0155` →  **0.6 σ_tot**: the two documents agree at 10 kAU.

- **Bin: 18–22 kAU** (the 20 kAU bin). At the frozen `N = 30,000` log-uniform over 2–30 kAU it holds
  **2,223 pairs**; σ_fit = 0.0699, σ_tot = 0.0726, so the separation there is **4.5 σ** — the repo's own
  4.2σ forecast, met.
  - **ERRATUM (2026-10-22, doors push D2):** the 18–22 kAU bin holds **~208 pairs at N = 30,000** on the DR3 frozen-cut occupancy (43 of 6,210 pairs, 0.69 %), not 2,223 (log-uniform 7.41 % is 10.7× too many; the pipeline's own mock gives 3.73 %, 1,119 pairs). The bin alone then separates 1.18 from 1.0 at only 0.8–2.6σ, so one bin does not decide; the registered whole-catalogue γ̂ does (5.0–5.9σ canonical) only if the contamination systematic σ_sys < 0.054 (alt 0.064). See `doors_push_2026_10_22/D2_wide_binary_fork/README.md`.
- **Pairs for exactly 4.2σ:** `σ_tot = 0.3286/4.2 = 0.0782`, `σ_fit = 0.0757`, **N = 1,893 pairs** in
  that bin. The like-for-like difference would need **5,134** pairs (N_cat ≈ 69,280).
- **The 10 kAU bin can never decide.** `Δγ = 0.0536` like-for-like against the irreducible
  σ_sys = 0.020 caps it at **2.7 σ at infinite N**. Any DR4 claim about this contradiction must come
  from ≥ 18 kAU.

**The contradiction is invisible at 10 kAU and decisive at 20 kAU**: the October paper's 1.20 at 10 kAU is consistent with Arm A; only its 1.51 at 20 kAU is excluded.

---

## Status

**DERIVED** for the central result: the law is AQUAL with `μ = x/(1+x)` (exact, eq. 2), so the EFE is
implicit and unavoidable in the local reading (proposition, §1), and imposing it inside the law
reproduces the registered arm (1.181 vs 1.1814; 1.193 canonical, 0.6 σ_fit).

**NUMERICAL** for the quadrature values (§2, §3), controlled at `q→0` to 3.4% and by the deep-limit
closed form.

**CONDITIONAL(premise)** on three declared items: (i) the composition factor `f₂` is measured in the
RAR kernel — the only kernel whose point-mass phantom quadrature is regular — and transferred to the
canonical law multiplicatively; (ii) the EFE numbers are `θ = 0` (maximal orientation), so the
orientation-averaged single-star bound is lower (1.2005 vs 1.2472); (iii) the 2,223-pair bin occupancy
assumes log-uniform separations over 2–30 kAU.

---

## Checks (`a24_checks.py`, 10/10 PASS, exit 0)

| id | what it proves | value |
|---|---|---|
| K1 | law ⇔ ν ⇔ AQUAL `μ = x/(1+x)`, exact | 2.2e-16 / 1.1e-16 |
| K2 | the October 1.20 / 1.51 are reproduced, so their recipe is identified | max dev 0.0031 |
| K3 | the phantom quadrature's `q→0` limit returns `ν−1` | 3.4% |
| K4 | no-EFE canonical: 1.5315 total-mass / 1.4037 exact at 20 kAU | pass |
| K5 | EFE-present: 1.1811 (RAR) / 1.1933 (canonical) / 1.1732 (repo x_ext) vs Arm A top 1.1814 | pass |
| K6 | EFE effect is 18× the solver fork | 0.350 vs 0.019 |
| K7 | 1.51 and the 1.33 no-EFE benchmark both sit in the guard zone | pass |
| K8 | 20 kAU bin: 2,223 pairs, 4.5σ, 1,893 needed for 4.2σ; 10 kAU caps at 2.7σ | pass |
| K9 | kernel systematic of the arm (canonical vs RAR) | 0.0216 = 1.1 σ_fit |
| K10 | surface-self-field reading gives γ−1 = 1.7e-13 (excluded); live suppression `f₂ = 0.721` | pass |

`--mutate` drops the external field from K5: γ returns to 1.3980 and K5 fails (exit 1) — teeth on exactly the quantity the lane is about; see `MUTATE.md`.

---

## What this does not do

- **It does not re-derive the registered band.** It reproduces the band's *top* (1.1811 / 1.1933 vs
  1.1814), not its construction (population MC + frozen estimator + the `f_tm` grade). The floor 1.1614
  is a composition/estimator effect this lane does not rebuild.
- **It does not solve the EFE-present exact two-body problem in AQUAL.** The quadrature is QUMOND; the
  AQUAL/QUMOND fork is taken from the repo's own two-solver comparison (0.005–0.016), not recomputed.
  That solve is the repo's declared unlock and remains open.
- **It does not decide whether the framework should adopt EFE-blindness.** It prices the choice: no
  parent, no scoreable DR4 prediction. **It does not touch data**; no measurement is made or re-analysed.
- **It flags but does not resolve the kernel conflict** (A5 tension 1): Arm A was computed with
  `ν_RAR`, the BRIEF's canonical law is `ν = ½(1+√(1+4/y))`. The shift is 0.0216 (1.1 σ_fit) and does
  not move the verdict, but the two kernels cannot both be "the" law.

## Next

1. File the correction to Zenodo 23251278 (text in §4) — one sentence, no numbers move.
2. Add the declarative amendment to `PREREGISTRATION_DR4.md`: Arm A presumes the local EFE-present reading; the EFE-blind alternative is the 1.33 benchmark already used for the guard zone.
3. On DR4 day, score the 18–22 kAU bin separately; it is the only bin that can decide this and needs
   ≥ 1,893 clean pairs. If the framework wants 1.51, the owed object is a covariant EFE-free completion.
