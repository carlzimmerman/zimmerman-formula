# The full picture of the current theory, v3 (2026-10-23)

One document that pulls together the pieces scattered across the record: the action, its field equations, every result as a
statement with its equation, the lane that computed it, and whether it is certified in Lean. Read this first; follow the
lane links for detail.

κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled. No dark-matter particle. The theory is not closed.
Nothing here says the data favour the framework.

**Certification legend.** **LEAN** = a machine-checked theorem (file and name given; `lake env lean <file>` in
`fable_independent_2026/lean_2026/`, axioms exactly propext, Classical.choice, Quot.sound; each file has a `_MUTATE` twin
that must fail). **SYMPY** = a symbolic derivation with a committed script. **NUM** = a numerical lane result, reproduced
by the coordinator. **POSTULATED** = an input, not derived.

---

## 1. The theory in one line

**The action** (C4, C5; Blanchet–Skordis Khronon, arXiv:2404.06584, in its literal healthy form):

    S = (c³/16πG) ∫ √−g [ R − 2 J(Y) + 2 K(Q) ]  −  (γ_L/2) ∫ √−g (D_i P^i)²  +  S_m[g, matter]

- τ is the preferred foliation (the khronon), A_μ its acceleration, and Y = A·A/c⁴. P is an independent spatial covector
  (n·P = 0). No extra curvature term (β = 0) and no P kinetic term (η = 0); η > 0 is ill-posed at β = 0 (C5). The Codex
  review adds a Hořava half mode for DSF-21's η > 0 branch.
- **J = J_x = Λ − 2a₀²[y − ln(1 + y)]**, y = √Y/a₀, so 1 + J′ = y/(1 + y). POSTULATED; it lies outside Blanchet–Skordis's
  admissible class.
- **K(Q) = μ_K²(Q − 1)²** is the Blanchet–Skordis dust sector; BS25 also has a DBI form.
- **The stiffness** γ_L = K L★²/2, L★ ≥ 21.7 / 22.9 pc (outer globulars, D10). POSTULATED; it exists only for Solar-System
  screening.
- **a₀ = κ c √(G ρ_Λ) = c²√(Λ/32π)** at κ = ½. LEAN: `TOE_BEST_ATTEMPT_2026_10_12.a0_lambda_form`, `a0_hubble_form`,
  `Z_bounds`. κ = ½ is FITTED and cannot be derived from the framework's premises. LEAN: `KAPPA_LOGIC_2026_10_20.
  half_not_derivable`, `half_not_derivable_with_data`, `p32_iff` (Λπ(c²/a₀)² = 32π² ⟺ κ² = ¼; re-certified today after a
  one-word toolchain fix).

**Fitted:** κ, L★ (a lower bound only), the dust abundance (an initial condition). **Free:** μ_K, bounded above by
Blanchet–Skordis at μ_K ≤ 14.8 h/Mpc (10 Mpc⁻¹), and by isolated-galaxy lensing at μ_K < 0.1 Mpc⁻¹ (S4).

## 2. The field equations

**Static limit** (S4 §1; BS24 Eq. 35, re-derived from the action in C4 K1 with residual 0):

    ∇·[ μ(|∇ψ|/a₀) ∇ψ ] + μ_K² ψ = 4πG ρ_b ,     μ(x) = x/(1 + x),     φ = ψ   (lensing sees the dynamical potential)

This is AQUAL, not QUMOND (doors E2, C4). With μ_K → 0 and spherical symmetry it gives the a₀-line.

**Weak-field dynamics** (BS24's post-Newtonian system; L1 FROZEN_CRITERIA §1):

    Ξ = φ − σ̇ + |∇σ|²/2                         (the lapse perturbation; khronon acceleration ∇Ξ, Y = |∇Ξ|²/c⁴)
    4πG ρ_τ = −[ ∇·(J_Y ∇Ξ) + μ_K² Ξ ]           (the hold equation; with J_x, J_Y = μ(x) − 1)
    ∇² φ = 4πG (ρ_b + ρ_τ)                        (Poisson, all mass)
    D v_τ/Dt = −∇φ + ∇Ξ ,   D v_b/Dt = −∇φ        (khronon dust and baryons)

**The khronon/dust pair's dispersion** (H4; weak field, first order in background gradients, with self-gravity):

    ω² = ρ_τ [ k²/χ(k) − 4πG ],   χ = k²/(4πG M_θ + γ_L k²) + μ_K²/(4πG),   ρ_τ = D·P + μ_K²(Q̄ − 1)/(4πG)
    at μ_K = 0:   ω² = 4πG ρ_τ (M_θ − 1 + L★² k²/2),   M_θ ∈ [1 + x, (1 + x)²]

## 3. What passes, and why

| statement | equation | evidence |
|---|---|---|
| The law | g_N = g²/(g + a₀), equivalently g² = g_N² + a₀g_N (the a₀-line); deep limit g → √(a₀g_N); Newton recovery g_N ≤ g ≤ g_N + a₀/2 | LEAN: `EQB_S1_rar_landmarks` (slope (2y+1)/(2(y+1)), curvature maximal at g_N = a₀), `TOE_BEST_ATTEMPT.newton_recovery`, `deep_tully_fisher` (v⁴ = GMa₀) |
| The a₀-line is forced | an affine excess with the deep-MOND normalisation forces slope 1 and intercept 0 | LEAN: `EQB_A0LINE_uniqueness.affine_excess_unique` |
| The external field | x μ(x + e) = b ⟺ (x² − b²)(x + e) = bx, with a unique root | LEAN: `EQB_S5_efe_cubic.efe_balance_iff_line`, `efe_root_unique` |
| The leaf problem is well posed | the MOND constraint is strictly convex, so its solution is unique | LEAN: `XC2_wellposedness_certificates.strict_convexity`, `XC5_lapse_convexity_certificates.convex_for_monotone_kernel` |
| The acceleration scale | MeerKAT a₀ is +0.032 dex from SPARC's with the same recipe | NUM: P4 |
| SPARC RAR (conditional) | rms 0.054 / 0.054 dex with one Υ per galaxy and the EFE solved for 109; the χ² line fails (63–64 % acceptable) | NUM: P4 |
| Isolated groups | +0.010 / −0.010 dex | NUM: P4 |
| Solar System (screened) | inside L★ the Sun's field is a hedgehog GM/L★² r̂ with no quadrupole; all 24 Cassini cells pass, by 4.8e7–5.1e9 | NUM: C6. The unscreened law fails Cassini 2.44–5.19× (E2) |
| Gravitational waves, binary pulsars | tensor speed c; at most 3.2e-14 of the double pulsar's precision | NUM: C8, P3 |
| Static black holes, neutron stars | shifts ≤ 2.9e-11; \|ΔR/R\| ≤ 5.3e-28 | NUM: P3 |
| Tidal dwarfs, DF2/DF4 | dust-free in their host, hence Newtonian (§4.3) | NUM: U1, consistent with T3 |
| Isolated Local Group dwarfs | +0.06 / +0.02 ± 0.08 dex | NUM: X1 |

**Why.** The static limit is AQUAL with the simple μ, so wherever a system is isolated and quasi-static, v3 is the
a₀-line, which is certified.

## 4. What fails, and the one mechanism behind most of it

### 4.1 The structural statement (X6, SYMPY; X-D1 to X-D5)

**v3 has one cold field, and it is the same field that carries the law.** For the foliation normal a_μ = D_μ ln N, so the
khronon charge's acceleration relative to free fall is ∇Ξ, the field whose gradient sets Y = |∇Ξ|². Its coupling weight α is
therefore fixed by kinematics at α ≡ 1; it is not a parameter (X-D1). At Q = 1 the khronon is exactly mimetic (geodesic)
dust (X-D2).

LEAN (`V3_PICTURE_2026_10_23`), for static held dust with weight α, (α − 1 + μ(x))x = b:
- `coupling_one_is_law`: α = 1 is exactly the a₀-line b(1 + x) = x².
- `coupling_floor`: α < 1 forces x > (1 − α)/α, an acceleration floor.
- `coupling_newtonian`, `coupling_not_deep`: α > 1 forces x < b/(α − 1), so x < √b once b < (α − 1)²; it is never the deep
  law.

Everything in 4.2–4.5 follows from this one identity and the dust's scale μ_K.

### 4.2 Linear growth: the dust is held only below μ_K

The exact dust kernel (M1, SYMPY) is s(k; f₀) = (μ² − f₀k²)/((1 − f₀)k² + μ²), with f₀ = 1 + J′(0).
LEAN: `kernel_at_zero` (s = 1 at k = 0), `kernel_Jx_pos_le_one`, `kernel_Jx_strictAnti`, `kernel_Jx_le_inv_sq` (for J_x,
s = μ²/(k² + μ²) ≤ μ²/k²: modes above μ are not held), `kernel_anti_f0` (s falls with f₀, so J′(0) = 0 holds less than J_x).

NUM:
- At the Blanchet–Skordis cap, σ₈/σ₈,dust = 0.391 (ODE) and 0.073 (Boltzmann).
- At the μ_K that isolated galaxies allow (0.03–0.1 Mpc⁻¹), it is 0.003–0.005: v3's khronon is radiation-like until
  z ≈ 35–78. Reaching 0.95 needs μ_K 2.4e3–5.7e4 times larger than galaxies allow (X4).
- The nonlinear J_x term does not restore it: L1's 128³ and 256³ rungs give ρ_NL −0.05 (indicative; 384³ running).

### 4.3 Hosted systems: the dust has no weight in a host

X-D5 (SYMPY): for any J, a static host has Ξ = Φ + C, so ∇ψ = 0 across a held system. LEAN: `fall_rate`,
`dusty_unit_lags`. A bound unit of baryons M_b and held dust M_τ > 0 falls at g·M_b/(M_b + M_τ) < g, so it cannot fall with
its host and keep its dust (U1's T3).

NUM: T3 predicts hosted ⇒ Newtonian. Tidal dwarfs and DF2/DF4 agree. Six independent hosted sets disagree at ≥ 5σ: Antlia II
24σ, MW ultra-faints 12.6σ, UMa members 12.6σ, bright M31 dSphs 9.8σ, Crater II 8.7σ, Coma UDGs 5.4σ (X1). Even static AQUAL
+ EFE (no T3) leaves the bright M31 dSphs +0.60 dex and the ultra-faints +1.56 dex high, the same as plain MOND + EFE.
Published MOND's dwarf successes rest on an approximate EFE formula that uses the full stellar mass; the exact solve is
0.19 dex lower (X1 controls).

### 4.4 Clusters: the static dust has the wrong ordering

In spherical symmetry the Khronon static equation is AeST's with μ → μ_K (S4, reproduced to 0.0058). The hydrostatic dust
δρ_K = −μ_K²ψ/(4πG) is attractive inside the well, then oscillates. Its onset sits at r_C ∝ (r_M/μ_K²)^{1/3}, with
r_M ∝ M^{1/2}. LEAN: `onset_exponent` ((M^{1/2})^{1/3} = M^{1/6}), `onset_strictMono`. Lighter systems are hit at smaller
radii, so galaxies are hit before clusters: 0 of 1,804 cells pass (S4).

NUM, the data side (X2):
- The stacked core excess (A_MID 1.68–1.85 / 1.54–1.70) is Z 5–6 on jackknife errors and Z 2.2–2.7 with the cross-shear
  systematics propagated.
- **The lightest third of clusters shows no core excess** (MID 1.02–1.13). The stacked outskirts ratio near 1 is light and
  heavy clusters cancelling (0.5 / 0.76 / 1.3).
- A debris profile that *replaces* the law at cluster scale passes; added to the law it overshoots.

### 4.5 The early universe: the literal dust has no radiation era

The quadratic K carries a stiff partner ρ_s = A a⁻⁶ with A ∝ μ_K⁻². LEAN: `stiff_beats_radiation_iff`
(A a⁻⁶ > R a⁻⁴ ⟺ a² < A/R), `crossing_redshift_linear` (1 + z_× ∝ μ_K), and `record_crossings_consistent`: Q6's own crossings,
z = 1854.4 at 14.8 h/Mpc and 318684 at 2542, obey the linear law to 0.1 %, an independent check of the record. BBN needs
μ_K ≥ 1.84e8 h/Mpc (Q6). BS25's DBI K fixes BBN but not growth (Q7); its large-coefficient door is closed by the Lyman-α
forest (X4).

### 4.6 Escaping through a separate dust is CDM under another name

A dust that weighs in hosts and grows linearly must be a separate field (X6 C1b, a mimetic λ_d constraint field). It
sources the law like baryons, so it double counts in isolated galaxies. It passes growth for f_d ≥ 0.762 and fails isolated
galaxies for every f_d > 0 (NGC 3198 off by 0.145 dex; the SPARC median Υ falls to 0.42 / 0.37). With per-galaxy Υ the RAR
rms barely moves (0.054 → 0.056 / 0.059), so the double count shows up only as Υ dropping below the population-synthesis
window. NUM: X6.

### 4.7 Saddles: the screening term is ill-posed where ρ_τ < 0, and the switched form is not (pointwise)

LEAN:
- `saddle_unbounded`: with ρ_τ < 0 and L★ > 0, −ω² exceeds every bound (Hadamard ill-posed). This is H4's verdict.
- `saddle_no_stiffness`: without γ_L, −ω² does not depend on k (BS's bounded branch: 0.006–0.20 e-folds).
- The switched stiffness −(γ_L/2)[max(D·P, 0)]², which adds no constant, with a non-negative dust density:
  - `switched_bounded_where_negative`: k-independent wherever ρ_τ < 0;
  - `switched_stable_where_positive`: stable wherever ρ_τ ≥ 0 and M ≥ 1;
  - `switched_agrees_where_screened`: identical to v3 wherever D·P ≥ 0, which covers every screened region;
  - `switched_uniform_bound`: −ω² ≤ 4πG|ρ_τ||M − 1| for all k, everywhere.

These are pointwise statements at leading WKB order. Lane X3 is testing the rest: the D·P = 0 interface, the C¹
Lagrangian, convergence under resolution, and whether D·P ≥ 0 wherever C6 and D10 rely on screening. **PENDING.**

### 4.8 The Milky Way disc

The AQUAL extra field around a disc is itself disc-like. The vertical force K_z(1.1 kpc) is 92.3 / 96.9 against 66.4 ± 2.2
on McMillan17 (P4). A light-column, short-disc model inside wide priors passes the χ² line together with v_c(R₀), but still
misses K_z(R₀) by ≥ 4.7σ and fails the full rotation curve (X5). The outer slope is excluded (Z −3.9 to −4.6 across error
models; S3, X5), and this holds for the whole μ-law family. Joint radial-plus-vertical fits fail in the MOND literature too.

## 5. The picture

    v3 = [ law field Ξ, certified a₀-line ]  +  [ screening γ_L ]  +  [ ONE dust = the same field Ξ, scale μ_K ]

1. **The law works where it was built to work:** isolated, quasi-static systems, and the Solar System once screened.
2. **Screening → saddles.** γ_L makes negative-ρ_τ regions Hadamard ill-posed. The switched form removes this pointwise at
   no cost in constants; X3 decides whether it survives the interface.
3. **The single dust → everything else.** Because the dust's coupling is fixed by kinematics (α ≡ 1):
   - it has no weight in hosts (hosted dwarfs fail, at odds with T3's prediction);
   - it is held only below μ_K (growth fails at any μ_K that galaxies allow);
   - its static branch oscillates and hits galaxies before clusters (clusters fail);
   - its literal K has no radiation era.
   Replacing it with a separate dust brings back CDM's double count in galaxies.
4. **Some failures are softer in the data than the record said:**
   - the cluster excess is 2.2–2.7σ with systematics, and absent in light clusters;
   - the dwarf failure depends on class, and isolated dwarfs fit;
   - the Milky Way has a narrow light-disc corner.
5. **Three failures are generic to every MOND-type theory:** clusters, the CMB's third peak (z ≈ 1100 is Newtonian, so a₀
   is inert there), and the Milky Way's joint fit.

**What a completion would need**, read off the mechanisms (X0 §2, X6): a gravitating cold sector that
(i) clusters linearly like dust from z ≈ 1100;
(ii) has weight in hosted systems; and
(iii) contributes nothing extra in isolated galaxies.
That last condition must come from a scale or selector that lies between galaxies and clusters (M2, S4); the record's
μ-pincer theorem rules out pressure for that role. Inside the khronon family (iii) conflicts with (i)–(ii) through α ≡ 1.
No such sector is in the record, and no rule-compatible framework in the literature claims one (X0 §1).

## 6. Still open

| item | what decides it | status |
|---|---|---|
| Switched stiffness at the interface and in the statics | X3 (`rebuild_2026_10_22/X3_switched_stiffness`) | running |
| Nonlinear growth (v3's one dynamical escape) | L1 384³ rung, then the 512³ production | 256³: does not restore growth (indicative); 384³ running |
| Cluster light/heavy split | per-tercile physics; a selector the theory lacks (CFG939) | data result (X2); no mechanism |
| Wide binaries, MW in Gaia DR4 | sealed predictions (C6; S3 `SEALED_V3_MW_DR4.json`) | data 2026-12-02 |
| ALMA U4 / GS4 | sealed, addendum F | data 2026-11-06 / 11-28 |

## 7. Lean index

New today, in `fable_independent_2026/lean_2026/V3_PICTURE_2026_10_23.lean` (23 theorems, 0 sorry, standard axioms only;
the `_MUTATE` twin fails on all four false claims): `saddle_unbounded`, `saddle_no_stiffness`,
`switched_bounded_where_negative`, `switched_stable_where_positive`, `switched_agrees_where_screened`,
`switched_uniform_bound`, `kernel_at_zero`, `kernel_Jx`, `kernel_Jx_pos_le_one`, `kernel_Jx_strictAnti`,
`kernel_Jx_le_inv_sq`, `kernel_anti_f0`, `stiff_beats_radiation_iff`, `crossing_redshift_linear`,
`record_crossings_consistent`, `onset_exponent`, `onset_strictMono`, `coupling_one_is_law`, `coupling_floor`,
`coupling_newtonian`, `coupling_not_deep`, `fall_rate`, `dusty_unit_lags`.

Already in the record, and compiling today:
- `TOE_BEST_ATTEMPT_2026_10_12`: a₀ forms, Z bounds, Newton recovery, deep Tully–Fisher. 13 theorems.
- All seven files in this list were recompiled today: exit 0, no errors, no `sorryAx`.
- `EQB_S1_rar_landmarks`: slopes and curvature.
- `EQB_A0LINE_uniqueness`.
- `EQB_S5_efe_cubic`.
- `XC2_wellposedness_certificates` and `XC5_lapse_convexity_certificates`: leaf convexity and uniqueness.
- `REV_aqual_cone_family`: AQUAL cones.
- `KAPPA_LOGIC_2026_10_20`: κ = ½ not derivable; the 32π equivalence. Its `p32_iff` had failed on the current toolchain with
  a redundant `ring` after `field_simp`, leaving it on `sorryAx`. That was fixed today in both the true file and its MUTATE
  twin; 12 statements are certified, and the twin fails only on its two declared mutations.

Not certified (numerical or data results): every number in §3–§4 marked NUM.
