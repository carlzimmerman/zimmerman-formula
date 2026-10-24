# v3s soft side: do khronon flows shell-cross in finite time in a moving saddle (MW–M31)? — FROZEN CRITERIA

Owner's request (2026-10-23): "test whether v3s soft-side khronon flows form caustics or shell-crossing in finite time in
moving saddles (e.g. MW-M31 approach), frozen criteria first, both footings, mutate." Follows
`reviews/v3s_soft_side_strong_coupling_2026_10_23/` (quantum loops: benign) — this is the classical question it left open.
κ = ½ FITTED; canonical a₀ = 9.36e-11 / alt 1.13e-10 m/s², never pooled. No dark-matter particle. Not theory closed.
Small job, one thread, nice 15. Written before any script or number.

## 0. Dynamics (derived by hand before freezing; checked in the script where stated)

v3s PN equations (H4 A1 with the switch): continuity ∂_tρ_τ + ∇·(ρ_τ v) = 0, v = −∇σ; Gauss law ∇·P(A) = ρ_τ with
A = ∇Ξ = ∇φ + Dv/Dt (N1 of the soft-side lane); Poisson ∇²φ = K(ρ_b + ρ_τ). Hence **Dv/Dt = F[ρ_τ] + g_b**, with
F = A − ∇φ_τ a functional of the khronon density alone and g_b = −∇φ_b the baryons' Newtonian field. Static AQUAL
equilibrium has A₀ = ∇φ, so **F₀ = −g_b(t_i) exactly**. To first order in the displacement ξ, an element obeys
`ẍ = Δg_b(x, t) + (self term)`, `Δg_b(x, t) ≡ g_b(x, t) − g_b(x, t_i)`: a test particle in the *difference* field, plus
the WKB self term −K(M−1)(ρ_τ ξ)_L. On the soft side (ρ_τ < 0) that self term is growth at
Γ² = K|ρ_τ|(M − 1). Continuity carries the density sign with the element (ρ_τ = ρ_τ₀(q)/J), so **a soft element stays
soft and never gets γ_L pressure**. A shell crossing there (J = det ∂x/∂q → 0) is a gradient catastrophe of σ, i.e. the
khronon foliation folds, with no pressure to regularise it. Hand estimate: deformation ~ ΔT_b t²/2 ≈ 0.2–1 over a Hubble
time, so borderline. No expectation for the verdict.

## 1. Model inputs (all stated now)

- Baryons: MW 6e10 M☉, M31 1e11 M☉ (H4's S1 inputs, illustrative), point masses with Plummer softening 20 kpc, on the
  MW–M31 axis about their barycentre.
- Orbit (separation r(t)): **O1** the Newtonian radial timing-argument Kepler orbit through r(t₀) = 780 kpc,
  ṙ(t₀) = −110 km/s, r(0) = 0, t₀ = 13.8 Gyr (kinematics only; its effective mass is a fitted orbit parameter, not
  baryons). **O2** a constant-velocity bracket, r(t) = 780 kpc + 110 km/s · (t₀ − t).
- Equilibrium epochs t_i ∈ {3, 6, 9} Gyr: the khronon is held (v = 0, F = −g_b(t_i)) at t_i, then forced.
- Window: t_i → t_end, where r(t_end) = 300 kpc (pre-merger). Also reported (no verdict weight) to r = 150 kpc.
- Soft region at t_i: elements on a grid in the plane containing the axis, x_null(t_i) ± 400 kpc along the axis
  × 0–400 kpc transverse, 10 kpc spacing. An element is kept if the QUMOND phantom density
  ρ_ph = −∇·[(ν − 1)g_N]/(4πG) < 0 there (ν for μ = x/(1+x)). This is a proxy for H4's AQUAL sign map, disclosed. Its
  x = |ν g_N|/a₀ and ρ_ph set M_L = (1+x)² and Γ.
- Integration (per element): x(t), ẋ(t) and the deformation D = ∂ξ/∂q with D̈ = −ΔT_b(x, t)(I + D) + s·Γ²D and
  ẍ = Δg_b(x, t) + s·Γ²(x − q), where ΔT_b = ∇∇φ_b(t) − ∇∇φ_b(t_i). Self-term brackets: **s = 0** (pure test
  particles in the difference field) and **s = 1** (isotropic soft-side growth at Γ² = K|ρ_ph|(M_L − 1), the
  fastest rate). Shell crossing ⇔ det(I + D) ≤ 0.

## 2. Checks (`caustics.py`; `--mutate` freezes the masses at r(t_i))

- **C0 (solver).** Constant compressive tidal field (ΔT = τ diag(1, 1, −2), s = 0): det(I + D) along the compressive
  axis reaches 0 at t = π/(2√τ) to relative 1e-6; time-reversal returns the start to 1e-9.
- **C1 (orbit).** O1 reproduces r(t₀) = 780 kpc and ṙ(t₀) = −110 km/s to 1e-9 relative. Report its effective mass,
  apocentre time and t_end for O1/O2.
- **C2 (soft region).** At every t_i and footing the soft region is non-empty and contains the axis null. Report its
  element count and size.
- **C3 (verdict, both footings, O1 and O2, all t_i, s = 0 and s = 1).** For each case, the minimum over soft elements
  of det(I + D) in [t_i, t_end] and the earliest crossing time t_sc. **Frozen reading:**
  - **SHELL-CROSSES** iff, for some (footing, orbit, t_i), *both* self-term brackets reach det ≤ 0 by t_end. Then report
    the earliest t_sc relative to t₀, where it happens (distance to the nearer galaxy), and the fraction of soft
    elements crossed by t₀ and by t_end. Sub-reading: t_sc < t₀ ⇒ "already crossed in the Local Group's past, given
    equilibrium at t_i".
  - **NO SHELL CROSSING** iff min det > 0.5 in every case.
  - **UNDECIDED** otherwise, with the cases named.
- **MUTATE (static masses).** Δg_b ≡ 0, so min det must be ≥ 0.999 for s = 0 in every case. That checks that only the
  approach drives the result; s = 1 with D(t_i) = 0 also stays at det = 1.

Not tested: the stiff side (γ_L pressure p = γ_Lρ²/2 may regularise positive-density caustics — not computed), the full
nonlinear 3D self-consistent F[ρ_τ] (only its WKB linear form), the cosmological environment (Hubble flow, other Local
Group members), the actual AQUAL sign map (QUMOND proxy), BS dust (μ_K → 0), and any completion that would follow a
crossing.

## AMENDMENT A1 (after run 1 crashed, BEFORE any verdict; run 1 kept as `caustics_RUN1_crash.out`)

Run 1 printed C1 PASS, C0 PASS and two C3 lines (canonical, O1, t_i 3, n_soft 28, det_min 0.377 / 0.336), then crashed
on an empty soft region. Diagnosis (scratch, disclosed):
1. **Code defect: wrong null.** `null_x` bracketed from 1e-3 kpc off each mass and found the trivial zero of g_x inside
   MW's Plummer core: T there was isotropic (GM/ε³ = 56 Gyr⁻²), not traceless. So run 1's two C3 lines describe a
   region behind MW, not the saddle; they are void. Fix: bracket [p₁ + 3ε, p₂ − 3ε]. At the real null, T is traceless
   (−0.0119, +0.0060, +0.0060 Gyr⁻² at r = 988 kpc), and the finite-difference phantom matches the deep-MOND analytic
   form −√a₀ gᵀTg/(8πG|g|^(5/2)) (−1.60e4 vs −1.68e4 M☉/kpc³ at 5 kpc off-axis, converging with the step size).
2. **C2's wording was a wrong expectation.** Near the null the phantom is positive along the axis and negative
   transverse. The soft region is a transverse lobe (±40–110 kpc along the axis, 250 to > 400 kpc across) whose
   boundary passes through the null. C2 ("contains the axis null") is kept as frozen and will be reported as it comes
   out; it does not gate C3.
3. In O2 the lobe reaches the box edge at 400 kpc transverse. Elements beyond are not tracked (disclosed truncation;
   frozen box unchanged).
Nothing in C3's thresholds, brackets or reading changes.

## AMENDMENT A2 (POST-RESULT; the frozen reading stands as computed; a validity diagnostic is added before it is run)

Run 2 (`caustics.out`): C0, C1 PASS; C2 FAIL (wording, A1); **C3 frozen reading SHELL-CROSSES**. 6/12 cases cross in
both brackets, all of them O2, identical on both footings. The earliest is t₀ + 0.64 Gyr, about 25 kpc from a galaxy.
O1 crosses only for t_i = 3 Gyr with s = 1 (t₀ + 1.46 Gyr, 254 kpc from a galaxy); its s = 0 runs reach min det +0.0000
(t_i 3) and +0.0005 (t_i 9) by t_end, and all O1 runs go negative by r = 150 kpc. MUTATE: det = 1.000000 in all 24
runs (PASS).

**Concern, raised before the diagnostic is computed:** the model keeps the khronon's own field F frozen apart from its
local WKB response. Near a galaxy, the positive phantom halo responds at ω_loc = √(4πG ρ_ph (M − 1)) ≫ 1/Gyr. It should
then follow the galaxy adiabatically, carrying F along and cancelling Δg_b there. The model is invalid in such
regions. Diagnostic (reported only, no verdict change), for every element that crosses, or reaches det < 0.1, by t_end:
at the crossing time t_c, take the element's current position, the current QUMOND equilibrium phantom ρ_eq and x
there, ω_loc² = 4πG ρ_eq (M_L − 1) with M_L = (1+x)², and the forcing time T_f = r/|ṙ| at t_c. Classify the crossing
as **ADIABATIC-REGION (model invalid)** if ρ_eq > 0 and ω_loc T_f ≥ 1, and as **SLOW-REGION (model valid)**
otherwise. Report the counts per case, the minimum det among elements whose whole track stays SLOW-REGION up to t_end,
and its time.
