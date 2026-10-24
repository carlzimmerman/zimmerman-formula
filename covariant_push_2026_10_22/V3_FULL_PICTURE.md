# The full picture of the current theory, v3s (2026-10-23)

**v3s = v3 with the switched stiffness −(γ_L/2)[max(D·P, 0)]², adopted by the owner on 2026-10-23** (§4.7, lane X3). It equals v3 wherever D·P ≥ 0, so the v3 results below carry over except where a solve has D·P < 0 lobes; there X3's globular re-solve moved L★ by +0.006 %.

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
| Gravitational waves, binary pulsars | tensor speed c; at most 3.2e-14 of the double pulsar's precision (no scalar channel at β = 0; with the β completion, X16: δṖ_b ≤ 2.1e-14 for J0737, provided the neutron-star sensitivity difference |s₁ − s₂| < 7e-7, which is bracketed but not computed in strong field) | NUM: C8, P3 |
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
- The nonlinear J_x term does not restore it. L1's A5 ladder gives ρ_NL −0.057 / −0.045 (128³), −0.058 / −0.047 (256³)
  and −0.059 / −0.047 (384³): monotonically converged, with KX below LIN. This is indicative; the 512³ production decides, and it is the
  only rung KiDS can score. Starting instead from Q6's Boltzmann state (LOB-IC, 384³), σ₈ is only 0.0135, about 1.6 % of the dust limit,
  and the nonlinear term changes nothing (ρ_NL ≈ 0).

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
- The stacked core excess (A_MID 1.68–1.85 / 1.54–1.70) is Z 4.5–5.5 on statistical errors. With the cross-shear
  systematic calibrated it is **Z 2.4–2.9, MARGINAL** (X7). The offset is 2.2–2.5σ against 200 rotated-source realisations,
  of unidentified origin; it is not PSF leakage. If it is a pure B-mode, the statistical Z stands.
  **X11 (reproduced) shows the offset behaves like noise, so the statistical Z 4.5–5.5 stands.** X11 also found the excess
  depends on source size (small sources A_MID 1.10–1.24, large 1.86–2.11).
  **X13 (reproduced) shows that size dependence is an artefact of the split, not of the clusters.** The lensfit scalelength
  acts as a major-axis length, so shear stretches it: a cut on it sends tangentially aligned sources to the large half and
  radially aligned ones to the small half. Evidence:
  - splitting on a shear-invariant circularised size removes most of it (ratio 1.13–1.17 ± 0.15, against 1.69–1.71);
  - 181,477 galaxy lenses show the same split ratio (1.47 ± 0.19);
  - random points give a null.
  The selection-corrected A_MID is 1.66 / 1.70 (canonical) and 1.52 / 1.56 (alt), **Z 4.1–5.0**, close to the all-source
  values. "Small sources are consistent with the law" was the suppressed half. Caveat: the response's size is not pinned
  (the first-order prediction overshoots the measured ratios by 0.9–2.4σ), and no image simulations are on disk.
- **The lightest third of clusters shows no core excess** (MID 1.02–1.13). The stacked outskirts ratio near 1 is light and
  heavy clusters cancelling (0.5 / 0.76 / 1.3).
- A debris profile that *replaces* the law at cluster scale passes; added to the law it overshoots.
- MOG/STVG with its published universal parameters fails this stack the other way (no core excess, outskirts too high)
  and fails SPARC (rms 0.136 against the law's 0.054). X9.

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

**The constraint algebra is not the problem** (Codex review, `reviews/v3_constraint_algebra_2026_10_23/`, d2d14f8326):
- v3's algebra closes uniformly with 3 DOF: no tertiary constraint, 8 second-class constraints, rank 4 on every background
  tested.
- In H4's ρ_τ < 0 regions γ_L|ρ| ≤ 2.9e-12, so the rank does not change there.
- The ill-posedness is therefore the scalar's own dynamics, and a cure has to change those dynamics. The switched stiffness
  does exactly that.

These are pointwise statements at leading WKB order. **Lane X3 tested the rest. Frozen verdict: WELL-POSED + STATICS
UNCHANGED** (`rebuild_2026_10_22/X3_switched_stiffness`, 8aeba82a87 / 31febd3b70; 13/13 checks; the MUTATE run, with the
switch removed, fails 6 of 12; coordinator rerun: main run identical; the D10 E_lo bracket regenerated from scratch matches 9,384 numbers to 1e-9).
- **Nonlinear, 1D.** The khronon pair is exactly a barotropic Euler fluid with c² = γ_L(D·P + ρ_d)Θ(D·P). That is ≥ 0 for
  every state when ρ_d ≥ 0; v3 as written has c² = −γ_L s_n. Any smoothing of the switch gives c² ≈ −0.058 εγ_L < 0, so the
  switch must be exact: it adds no new scale. SYMPY.
- **The interface.** The leaf functional stays convex ((s₊)² is C¹ and convex), so the leaf problem stays uniquely solvable.
  It becomes a free-boundary (obstacle-type) problem with Φ ∈ C¹, P continuous, and s₊ = ∂ₙs₊ = 0 on the stiff side. If v3's
  solution has D·P ≥ 0 everywhere, it is the switched solution.
- **Slab without WKB.** The growth rate converges under resolution doubling (finest ratio 1.0000; Γ → 1.22474 against the
  localised 1.224745), where v3 diverges (2.03). The rigorous bound held at every level.
- **Statics unchanged:**
  - Cassini: the Galactic phantom keeps D·P > 0 within 1 kpc of the Sun, with a margin ≥ 1.8e4.
  - Outer globulars: their external-field lobes do have D·P < 0 (180–1555 pc). The full switched re-solve (11,250 solves,
    0 unconverged) moves the L★ floor to 21.682 / 22.849 pc (+0.006 %).
  - P3: all 60 rows have D·P > 0.
- **Qualifiers:**
  1. The dust must be ≥ −D·P inside stiff regions, which holds in the μ_K range S4 allows.
  2. At zero dust the interface is a knife edge, so numerics must be sign-consistent.
  3. H4's bounded growth remains at saddles (0.006–0.20 e-folds median). **The v3s lobes around outer globulars and satellites are RESOLVED BENIGN** (H5, `rebuild_2026_10_22/H5_v3s_lobe_growth`, 2cde8548ed / 568a6b6709, 11/11, rerun identical):
     - the PN system is Galilean-covariant, so the lobe pattern rides with the moving system while the host khronon streams through, spending 1–25 Myr in a lobe;
     - the khronon charge's sign is carried along with the flow, so the stream keeps D·P ≈ ρ̄_host > 0 there, which is the stiff side, with nothing to grow;
     - granted the static lobe anyway, N ≤ 0.048 (globulars), ≤ 0.013 (satellites) and ≤ 0.46 (pure radial orbit at apocentre).
  4. The D·P < 0 side's strong coupling: RESOLVED BENIGN (review `reviews/v3s_soft_side_strong_coupling_2026_10_23/`, d27e01f42e, 5/5): the soft-side khronon is a dispersionless fluid, ω² = Kρ_τ(M − 1); 'Λ = 0' came from putting c_π = 0 (the k → ∞ limit) into the relativistic scaling. With c_π(k) = ω/k, the strong-coupling length across all 320 H4 region values is 57 m–54 km, so the soft-side EFT holds on astrophysical scales. Open: classical nonlinearity of real khronon flows, ε_cl = k|v|/ω, possibly O(1) in Mpc bulk flows.
- **Not shown:** 2D/3D time evolution; a well-posedness proof for the moving interface.

So the saddle failure has a zero-constant cure. **v3 with the switched stiffness ("v3s")** keeps every v3 pass and removes
H4's ill-posedness.

### 4.8 The Milky Way disc

The AQUAL extra field around a disc is itself disc-like. The vertical force K_z(1.1 kpc) is 92.3 / 96.9 against 66.4 ± 2.2
on McMillan17 (P4). A light-column, short-disc model inside wide priors passes the χ² line together with v_c(R₀), but still
misses K_z(R₀) by ≥ 4.7σ and fails the full rotation curve (X5). The outer slope is excluded (Z −3.9 to −4.6 across error
models; S3, X5), and this holds for the whole μ-law family. Joint radial-plus-vertical fits fail in the MOND literature too.

## 5. The picture

    v3 = [ law field Ξ, certified a₀-line ]  +  [ screening γ_L ]  +  [ ONE dust = the same field Ξ, scale μ_K ]

1. **The law works where it was built to work:** isolated, quasi-static systems, and the Solar System once screened.
2. **Screening → saddles: cured.** γ_L makes negative-ρ_τ regions Hadamard ill-posed. The switched form
   −(γ_L/2)[max(D·P, 0)]² removes this at no cost in constants. It is certified pointwise in Lean, and lane X3 checked it
   nonlinearly in 1D, in a slab without WKB, at the interface (still uniquely solvable) and in every screened static result
   (unchanged). The qualifiers are in §4.7.
3. **The single dust → everything else.** Because the dust's coupling is fixed by kinematics (α ≡ 1):
   - it has no weight in hosts (hosted dwarfs fail, at odds with T3's prediction);
   - it is held only below μ_K (growth fails at any μ_K that galaxies allow);
   - its static branch oscillates and hits galaxies before clusters (clusters fail);
   - its literal K has no radiation era.
   Replacing it with a separate dust brings back CDM's double count in galaxies.
4. **Some failures are softer in the data than the record said:**
   - the cluster excess is absent in light clusters. (Its overall significance is not softer: after X11 and X13 it stands
     at Z 4.1–5.5; X7's calibrated 2.4–2.9 assumed the cross-shear offset was a systematic, and X11 found it is noise);
   - the dwarf failure depends on class, and isolated dwarfs fit;
   - the Milky Way has a narrow light-disc corner.
5. **Three failures are generic to every MOND-type theory:** clusters, the CMB's third peak (z ≈ 1100 is Newtonian, so a₀
   is inert there), and the Milky Way's joint fit.
6. **The single-stream khronon forms caustics generically** (X14, analytic: any stream crossing a sheet folds at
   w/(KΣ_b)). Removing them needs a new constant; of nine classes only the β term survives, in a narrow window. It
   passes preferred-frame PPN (X15) and binary pulsars (X16, on a neutron-star sensitivity condition). But it works only
   for motion slower than the khronon's new sound speed, it is no galaxy/cluster selector (X17), and in linear theory it
   makes small-scale growth overshoot (X17; whether nonlinear saturation or the forest decides is open).

**What a completion would need**, read off the mechanisms (X0 §2, X6): a gravitating cold sector that
(i) clusters linearly like dust from z ≈ 1100;
(ii) has weight in hosted systems; and
(iii) contributes nothing extra in isolated galaxies.
That last condition must come from a scale or selector that lies between galaxies and clusters (M2, S4); the record's
μ-pincer theorem rules out pressure for that role. That covers density-keyed pressure; the β completion's
acceleration-keyed sound speed lies outside it, but has no effect in statics (X17). Inside the khronon family (iii) conflicts with (i)–(ii) through α ≡ 1.
No such sector is in the record, and no rule-compatible framework in the literature claims one (X0 §1).

## 6. Still open

| item | what decides it | status |
|---|---|---|
| Switched stiffness at the interface and in the statics | X3 (`rebuild_2026_10_22/X3_switched_stiffness`) | **WELL-POSED + STATICS UNCHANGED** (qualifiers in §4.7); 2D/3D evolution and the moving-interface proof remain open |
| Nonlinear growth (v3's one dynamical escape) | L1 512³ production | ladder converged at 256³ / 384³: does not restore growth (ρ_NL ≈ −0.05, indicative); LOB-IC 384³: σ₈ 0.0135, ρ_NL ≈ 0; the 512³ cells are queued |
| Dynamical state of moving subsystems | H5 A2–A5; lane O1 (H4/V1 coordinator) | **OPEN.** In the literal single-stream reading, a system moving at V through its host's held khronon is not in the static branch: outside r_cap = 2GM_b/V² (the Sun ≈ 0.03 AU, globulars ≤ 0.25 pc) its interior sees ψ → φ_N. This is the dynamical form of U1's T3 (hosted ⇒ Newtonian). It questions the static AQUAL solutions (D10, S1, X1_hosted_recount) as the dynamical state of hosted systems. O1 result (`rebuild_2026_10_22/O1_ownership_action`, ecbb964b0e, rerun identical):
  - **ownership cannot come from a local action** in the v3s family: a held host's phantom makes a satellite's held dust
    hover, ε = 1;
  - **literal v3 with γ_L removed** (velocity screening only) passes Cassini (estimate), the outer globulars (Newton within
    Δχ² 2.47 in all 18 D10 cells), the TDGs/DF2 and the isolated RAR, and fails the satellites and UDGs;
  - **but every moving mass focuses the khronon wind into a line behind it** that a single-stream khronon cannot pass
    (a caustic; γ_L does not fix it, Mach ≈ 300). X10 confirms the wake line behind a moving Milky Way-mass galaxy at
    t_i + 3.9–4.4 Gyr, converged, so velocity screening carries the caustic problem with it.
  - **X15 (linear, analytic):** at β = 0 a moving source does not carry its hedgehog. For any k·w ≠ 0 the linear
    solution is GR with the bare G, and the limits β → 0⁺ and w → 0 do not commute. This is H5's velocity screening at
    linear order. So A22's a_P = GM/L★² and C8 K8's (w·n̂)² anisotropy hold only for a Sun at rest in the khronon frame;
    Cassini passes either way. The β term restores the carried hedgehog for motion slower than c_A |
| Soft-side caustics in v3s | review `reviews/v3s_soft_side_caustics_2026_10_23/` (b362f12477); X8, X10, X12, X14 | **CAUSTICS GENERIC (X14, analytic); no caustic-free completion without a new constant (only β survives).** History: the review left it open, not established and not excluded. A soft khronon element is a test particle in the difference field Δg_b plus a WKB self term, and its density sign is carried with it, so it never gets γ_L pressure. The frozen reading shell-crosses in 6 of 12 cases (constant-velocity orbit, ~26 kpc from a galaxy, earliest t₀ + 0.64 Gyr), but every crossing element passes through an adiabatic halo region where the frozen-F premise fails. Elements that stay in the valid region never cross (deepest J = 0.35). Deciding it needs a self-consistent khronon-fluid code: Lagrangian flow plus the nonlinear Gauss law ∇·P(∇Ξ) = ρ_τ, axisymmetric **X8** (`rebuild_2026_10_22/X8_soft_side_caustics`, 43eedad42a / 72515e7e75; coordinator rerun of the decisive runs identical) built the self-consistent axisymmetric solver. Frozen verdict **UNDECIDED**: halving the time step moves one fold by 0.221 Gyr against the 0.2 line.
  - All six O2 cases fold on both footings, converged, at t₀ + 0.4 to 2.7 Gyr (none before today). O1 t_i 9 does not fold; four O1 cases are unconverged.
  - The mechanism is an axis collapse (a hoop factor of 0.022), which may be specific to axisymmetry.
  - Self-consistency does not remove the crossing.
  - O1's wake line cannot be separated from the transient caused by starting the khronon at rest.
  - **X10** (`rebuild_2026_10_22/X10_caustics_comoving`, 8a67b46dd7 / c13d9a15a6; decisive cells reproduced) added a
    co-moving start: each galaxy's held khronon is Galilean-boosted with it.
    - **The folds are not a start artefact.** Four of the six O2 cases fold, converged on both footings, 1.1–2.0 Gyr later
      than in X8 and all after t₀. They are mostly in-plane, at the front of the Milky Way's held halo. X8's dt sensitivity
      is gone (0.006 Gyr). Verdict UNDECIDED (PARTIAL): t_i 9 is not converged.
    - **The wake is real in this model.** Behind the Milky Way the khronon wind focuses onto the axis 76–91 kpc downstream at
      t_i + 3.9–4.4 Gyr, converged and the same on both footings. The upstream side folds only after ~11 Gyr. On the t_i 3
      orbit this happens before today.
  - **Reading.** In the axisymmetric model v3s's single-stream khronon develops caustics within a few Gyr behind moving
    galaxies. What that means for the foliation (multi-stream flow, a global-time breakdown, or new UV physics) is not
    decided. Still open: non-axisymmetric encounters, a smooth irrotational co-moving start, and back-reaction on the
    baryons. X12 (3D) failed its own Galilean check, so the stop rule held and there is no 3D result. A single moving mass in
    a cold stream is axisymmetric in 3D too, so the wake is generic focusing; the question is now a caustic-free completion
    (X14).
  - **X14** (`rebuild_2026_10_22/X14_caustic_completion`, 68bf6e379d / c23149c508; rerun reproduced) answers both questions
    analytically from v3s's own PN equations.
    - **(i) Caustics are generic.** In the planar reduction a zero-charge stream crossing any sheet of surface density Σ_b
      folds at τ_f = w/(KΣ_b), for every speed w. Soft (ρ_τ < 0) elements fold for every initial datum. Stiff elements fold
      outright or by phase mixing. v3s's own terms act too late: the stiffness is a nonlinear pressure that meets the stream
      at Mach ≥ 311 / 280, and K(Q) is inert at the fold scale (q_K ≤ 0.017 at μ_K = 0.1 Mpc⁻¹).
    - **(ii) Every caustic-free completion needs a new constant.** Of nine frozen classes only C1 survives: a K²/(□φ)²
      term, the record's β. Its window is β ∈ [2.0e-6, 1.0e-5] at μ_K = 0.1 Mpc⁻¹. It removes the fold only in linear,
      subsonic flow; X15 (below) checked its preferred-frame PPN. The complex-scalar (Madelung)
      completion needs ρ_τ ≥ 0 and is singular where ρ_τ crosses zero. Adhesion adds no constant but is non-variational, and
      with sign-indefinite charge a sticky merger creates energy.
    - **New structural fact.** The PN hold flux is capped, |KP| < a₀: under the simple μ the phantom acceleration
      g − g_N = a₀x/(1+x) never reaches a₀. Its inverse 𝒰(y) = a₀y/(a₀ − |y|) has 𝒰′ = (1+x)². Negative enclosed charge
      therefore collapses within a free-fall time.
    - The coordinator checked the cap identity, τ_f, the C9 energy gain and β_max by hand.
  - **X15** (`rebuild_2026_10_22/X15_c1_preferred_frame`, 87867a70a4 / 1dabb58f50; rerun identical): **C1 SURVIVES PPN**.
    - In the screened branch, with η(k) = 2/(1 + L★²k²/2), α₁ = −4η and α₂ = η(η(1+2β) − β)/(β(2 − η)). These match
      Blas–Pujolàs–Sibiryakov's khronometric formulas with α_BPS = η, β_BPS = 0, λ_BPS = β; the coordinator checked
      that symbolically.
    - At PPN order (r ≪ L★) α₁ = α₂ = 0 for every β > 0. The residuals at 30 AU, ≤ 3.6e-10 and ≤ 2.3e-11, are set by L★,
      not β, against bounds 1e-4 and 2.4e-7. The whole X14 window survives on both footings.
    - **The open condition is galaxy dynamics.** C1 makes the khronon a propagating scalar with sound speed c_A,
      160–770 km/s at the top of the μ_K = 0.1 window, and its cure needs motion slower than c_A.
      - Subsonic galaxies shift by ≤ 0.04 dex.
      - At CMB-dipole speeds galaxy outskirts are supersonic (Mach up to 2.3) and not estimable.
      - At μ_K = 0.03 the window reaches 1.1e-4 and 369 km/s stays subsonic (Mach ≤ 0.69).
      - The khronon's rest frame relative to galaxies is not fixed by the record.
    - Not computed in X15: binary-pulsar scalar radiation (now X16, below), neutron-star sensitivities, and 2PN.
  - **X16** (`rebuild_2026_10_22/X16_beta_binary_radiation`, db3a4913a0 / ff02290692 / 4799209bf5; rerun identical):
    **C1 PASSES BINARY PULSARS, on one condition.**
    - There is one radiating scalar, with positive energy. Fed through the tensor sector, the same flux formula
      reproduces GR's quadrupole to 2.2e-15. In the matching limit it equals Yagi et al. 2014's khronometric flux at
      α = η(k_S), λ = β (PROVISIONAL).
    - δṖ_b/Ṗ_b over the window: J0737 ≤ 2.1e-14, B1913 ≤ 9.0e-13, J1738 ≤ 1.2e-17, J0348 ≤ 1.6e-19 (41/41 points
      in every cell).
    - The condition: the dipole channel is strong, so the stars' sensitivity difference must stay below 7.2e-7
      (J0737) to 4.5e-5. The weak-field estimate gives s ≈ 1e-27 and a generous envelope gives ≤ 4.4e-15. No
      strong-field sensitivity calculation exists for v3s + C1.
    - The scalar moves at 47–133 c at the double pulsar. The tensor speed is exactly c.
  - **X17** (`rebuild_2026_10_22/X17_beta_sound_selector`, 348993ca40 / 3d8f8c6a0c; rerun identical): **C1's sound speed
    is no galaxy/cluster selector (WRONG SIGN).**
    - **Inert in statics, at all orders.** K = 0 on static slices, and β enters the PN charge equation only through a
      term that vanishes on held and boosted-held khronon. So static cluster lensing, isolated galaxies and S4's
      ordering are unchanged.
    - **The speed is set by acceleration, not density.** c_A² ∝ B c² x, where x = |∇Ξ|/a₀. So C1 is outside the
      μ-pincer's scope. Internal Mach v_c/c_A = √(r/r_β) with r_β = Bc²/a₀ (31–1737 kpc), whatever the mass.
      eRASS1-mass cluster cores have c_A 209–482 km/s at β_max(0.1), not X15's 449–1032.
    - **Motion effects are too small and ordered the wrong way.** They lower heavy-cluster cores or are largest in the
      lightest clusters, and none reaches a quarter of the excess.
    - **New problem for C1: growth.** c_A = 0 on the cosmic background, so there is no Jeans suppression. Instead C1
      amplifies the khronon's response to baryon wells at large k, with growth rate ∝ k^{1/2}. In X4's linear ODE every
      window cell overshoots at k ≳ 1–3 h/Mpc. At β_min σ₈ is 0.19–0.22 of dust, yet P(k = 3) is 300–470× dust; at
      β_max(0.1) σ₈ is 9.97× dust. So wherever σ₈ would match dust, small-scale power is far above it. Nonlinear
      saturation and the Lyman-α forest are not yet computed. |
| Cluster light/heavy split | per-tercile physics; a selector the theory lacks (CFG939) | data result (X2); no mechanism. The β completion's sound speed is not that selector (X17: inert in statics, wrong mass ordering in motion) |
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
