# X8_soft_side_caustics: do v3s soft-side khronon flows form caustics at a moving two-body saddle when the khronon's own field is solved self-consistently? FROZEN CRITERIA

Written and committed (with `ASSUMPTION_LEDGER.md`) before any lane script exists and before any script has produced a
number. Rules: `rebuild_2026_10_22/BRIEF.md`, `doors_push_2026_10_22/BRIEF.md` + `BRIEF_E_AUDIT.md`. Lane launched by the
coordinator from the open row "Soft-side caustics in v3s" of `covariant_push_2026_10_22/V3_FULL_PICTURE.md` §6 and the
review `reviews/v3s_soft_side_caustics_2026_10_23/` (b362f12477). κ = ½ is FITTED. Footings canonical a₀ = 9.3603e-11 m/s²
and alt a₀ = 1.1312e-10 m/s², never pooled. No dark-matter particle. Never "theory closed"; nothing here says the data
favour the framework. Small jobs only: `OMP_NUM_THREADS=1 nice -n 15`, < 1 GB RSS, each run ≤ 30 min (checkpoint/resume).

## 0. What was read before freezing, and the not-blind statement

Read: `rebuild_2026_10_22/BRIEF.md`; `V3_FULL_PICTURE.md` §1, §2, §4.7 and §6; the caustics review (README,
FROZEN_CRITERIA + A1/A2, `caustics.py`, `caustics_validity.py`, `caustics.out`, the results json structure); the
strong-coupling review (README); H4 (README, FROZEN_CRITERIA, ASSUMPTION_LEDGER); X3 (README, FROZEN_CRITERIA §0–§2,
ASSUMPTION_LEDGER); H5 (README); L1 FROZEN_CRITERIA §1 (the weak-field PN system); O1 README (its §3(ii) downstream focal
line), the latter because the coordinator asked for a wake diagnostic (§6 D-WAKE) before this file was written.

**Not blind.** I know the review's numbers: frozen-F test particles shell-cross in 6/12 cases (all O2, earliest
t₀ + 0.64 Gyr about 26 kpc from a galaxy); every crossing passed through an adiabatic halo region; slow-region elements
reach J ≥ 0.35. Hand work before this file (nothing run):
- **Positive-halo frequency.** Inside a Plummer core the deep-MOND phantom has an integrable r^(−1/2) cusp, but
  ω² = Kρ_τ(M_L − 1) stays finite: ω² → (5/3)Kρ_b(0). For M31 (1e11 M☉, ε = 20 kpc) that is ≈ 17 Gyr⁻¹; in the deep-MOND
  halo ω² ∝ r⁻³. So the self-consistent halo is stiff near the galaxies (period ~0.4 Gyr) and soft far out.
- **Hold-law iteration.** Written as ∇²Ξ = Kρ_τ + ∇·(μ∇Ξ), the fixed-point map has Lipschitz constant ≤ max (2x + x²)/(1+x)²
  < 1; x ≲ 0.5–0.7 in the Plummer cores, so a Laplacian-preconditioned iteration converges.
- **Initial-condition mismatch.** The review holds the khronon at v = 0 at t_i while the galaxies already move (~70 km/s
  for MW on O2). A self-consistent halo must catch up; the sloshing amplitude is ~V/ω_loc (≈ 7 kpc where ω ≈ 10 Gyr⁻¹,
  ≳ 70 kpc where ω ≲ 1 Gyr⁻¹). This is part of the review's case definition and is kept (§2); it is reported (D-FOLLOW).
- **Cylindrical CIC.** Linear (bilinear) ring weights in (R, z) misrepresent a radial compression on the first few lattice
  rows next to the axis (relative error ∝ 1/i at row i), so the axis rows converge only at first order in h.
- **Wake geometry.** For a point mass moving at V through cold dust the Danby–Camm focal distance of a ray with impact
  parameter b is b²V²/(2GM): ≈ 95 kpc for MW at 70 km/s and b = 100 kpc. In axisymmetry that focal line is the axis.
- No expectation for the verdict.

## 1. The theory tested (v3s) and its weak-field dynamics

v3s = v3 with the switched stiffness −(γ_L/2)[max(D·P, 0)]² (V3_FULL_PICTURE §1, X3). Weak-field PN system (V3_FULL_PICTURE §2;
L1 FROZEN §1; H4 A1; the switch as in X3 B1-S/B2-S), μ_K → 0, no BS dust (the review's setting; dust ≥ 0 would only fill
the lobe, H4's f = 3 maps):

    Ξ̃ ≡ Ξ + γ_L ρ₊ ,   ρ₊ = max(ρ_τ, 0) = max(D·P, 0)          (no dust: D·P = ρ_τ)
    ∇·[ (1 − μ(|∇Ξ̃|/a₀)) ∇Ξ̃ ] = 4πG ρ_τ                        (hold law / nonlinear Gauss law; μ = x/(1+x))
    ∇²φ = 4πG (ρ_b + ρ_τ)                                        (Poisson, all mass)
    ∂_t ρ_τ + ∇·(ρ_τ v_τ) = 0 ,   v_τ = −∇σ
    D v_τ/Dt = −∇φ + ∇Ξ̃ − γ_L ∇ρ₊                               (khronon Euler; the last term is the switched stiffness)

(The P equation with the switch is ∇Ξ + γ_L∇(D·P)₊ = h(P), so the unstiffened P–field relation holds for Ξ̃; the stiffness
appears as a pressure γ_Lρ₊²/2 acting only where D·P > 0, c² = γ_Lρ_τΘ(ρ_τ), X3 B2-S.) Writing φ = φ_b + φ_τ (φ_b the
baryons' Newtonian potential, φ_τ the khronon's) and χ ≡ Ξ̃ − φ_τ:

    ∇²χ = ∇·[ μ(|∇Ξ̃|/a₀) ∇Ξ̃ ] ,   D v_τ/Dt = ∇(χ − φ_b) − γ_L ∇ρ₊ .

Static equilibrium (v = 0, ρ₊-term aside): Ξ̃ = φ_AQUAL (AQUAL with μ = x/(1+x), the theory's static limit), ρ_τ = the
AQUAL phantom, χ = φ_b. A soft element (ρ_τ < 0) keeps its sign along the flow (continuity), so it never feels γ_L. The
baryons are prescribed point-like Plummer masses on the review's kinematic orbits (§2); the khronon does not act back on
them (as in the review).

γ_L = K L★²/2, K = 4πG, with the v3s floors L★ = 21.682 pc (canonical) / 22.849 pc (alt) (X3 D4). At the kpc scales
resolved here the stiffness force is ~(L★/ℓ)² ≲ 1e-5 of the self-force; it is kept for fidelity, and its size is printed.
X3's sign-consistency knife edge gives a grid rate ~(ρ′γ_L/h)^½ ≲ 1e-3 Gyr⁻¹ at these scales (hand estimate), negligible.

## 2. Cases (the review's, unchanged)

- Baryons: MW 6e10 M☉ and M31 1e11 M☉, Plummer softening ε = 20 kpc, on the z axis about their barycentre: MW at
  z = −(M₂/(M₁+M₂)) r(t), M31 at +(M₁/(M₁+M₂)) r(t).
- Orbits (the review's code, identical formulas): **O1** the Newtonian radial timing-argument Kepler orbit through
  r(t₀) = 780 kpc, ṙ(t₀) = −110 km/s, r(0) = 0, t₀ = 13.8 Gyr; **O2** r(t) = 780 kpc + 110 km/s · (t₀ − t).
- Equilibrium epochs t_i ∈ {3, 6, 9} Gyr: at t_i the khronon is in the discrete AQUAL equilibrium of the two masses at
  r(t_i), with v_τ = 0 everywhere (the review's initial condition).
- Window: [t_i, t_end], t_end the time at which r = 300 kpc (the review's: O1 16.483, O2 18.067 Gyr). Also reported:
  min J by t₀ = 13.8 Gyr and by t_i + 13.8 Gyr (a Hubble time of evolution). Runs continue to t_end + 0.1 Gyr only so
  that a threshold event at t_c ≤ t_end can be confirmed (§5); nothing after t_end enters S.
- Footings: canonical and alt. 6 orbit cases × 2 footings = **12 cases**. No case is added or removed after any number.

## 3. Numerical method (all regulators below are numerical parameters; each is varied in §4)

- **Grid.** Axisymmetric (R, z) node-centred finite volume on a tensor-product grid. Fine zone (uniform spacing h):
  R ∈ [0, R_f], z ∈ [z_lo, z_hi] with r_max = max r(t) over [t_i, t_end],
  R_f = max(500, 0.6 r_max), z_lo = −0.625 r_max − 200, z_hi = 0.375 r_max + 200 (kpc), each rounded outward to a
  multiple of 20 kpc so that the h = 20, 10, 5 kpc lattices are nested. Beyond the fine zone spacings grow geometrically
  by q = 1.08 per cell until the coordinate reaches ≥ B_out = 20 Mpc (in R and in ±z). Resolutions **h ∈ {20, 10, 5} kpc**.
- **Boundary conditions.** Zero flux at R = 0. Dirichlet on R = R_out and z = z_min, z_max: Ξ̃_bdy = the spherical AQUAL
  potential of the total baryon mass about the current baryon centroid (exact g = [g_N + (g_N² + 4g_N a₀)^½]/2,
  integrated in r); φ_τ,bdy = Ξ̃_bdy − φ_b,bdy (φ_b the analytic Plummer potentials at time t); hence χ_bdy = φ_b,bdy.
- **Discrete operators.** Flux-sum form on control volumes (annuli × Δz): face normal gradients from the two nodes, the
  tangential component at a face from the average of the two adjacent nodes' central differences; |∇Ξ̃| at faces sets μ.
  Poisson and the hold law are written as flux sums equal to K × (mass in the control volume). Node gradients (forces) by
  central differences on the non-uniform lattice; ∂_R = 0 on the axis.
- **Initial state.** Solve the discrete AQUAL equation flux-sum[μ(|∇Ξ̃|/a₀)∇Ξ̃] = flux-sum[∇φ_b] (φ_b sampled at the
  nodes) by quasi-Newton (isotropic coefficient (μ + μ_L)/2, μ_L = (2x + x²)/(1+x)², re-factorised each iteration; start
  from the QUMOND-like solve of ∇²Ξ̃ = ∇·[ν(|∇φ_b|/a₀)∇φ_b]) to a relative residual ≤ 1e-11 (or machine stagnation, printed).
  The khronon particle masses are then defined as m = (1/K) × flux-sum[(1 − μ)∇Ξ̃] at each interior node: the discrete
  phantom mass, so the hold law holds exactly for the initial state and χ = φ_b up to the AQUAL residual.
- **Khronon fluid.** One Lagrangian ring particle per interior node, labelled by its initial node q = (R_q, z_q), signed
  mass m(q) (soft ⇔ m < 0), v = 0 at t_i. Each force call: CIC (bilinear in R and z on the non-uniform lattice) deposit of
  the signed masses; Poisson for φ_τ (sparse LU of the Laplacian, factorised once); the hold law for Ξ̃ by
  Anderson-accelerated (depth 5) fixed point Ξ̃ ← L⁻¹[Km + flux-sum(μ∇Ξ̃)] warm-started from the previous call, stopped when
  max|ΔΞ̃|/h ≤ tol·a₀ with **tol = 1e-7** (cap 300 iterations); χ = Ξ̃ − φ_τ; node acceleration ∇(χ − φ_b) − γ_L∇ρ₊ with
  ρ₊ from the node densities; CIC interpolation to the particles. Particles with R < 0 are reflected (axis symmetry).
- **Integrator.** Kick–drift–kick leapfrog, fixed step dt = min(0.02 Gyr, 0.15/ω_max), ω_max = max over nodes of
  [K|ρ_τ|((1+x)² − 1)]^½ in the initial state. ω_max(t)·dt is monitored and printed.
- **The Jacobian.** J(q, t) = (R/R_q) det[∂(R, z)/∂(R_q, z_q)], the 3-D volume ratio of the axisymmetric flow map,
  by centred differences over the ± 1 label neighbours; on the axis J = (R(h)/h)² ∂z/∂z_q (one-sided). Shell crossing ⇔
  J ≤ 0. J is evaluated for every particle every 0.02 Gyr (or every step if dt > 0.02 Gyr).
- **Validated region.** Labels in the fine zone at least 2 nodes from its outer edges (R_f, z_lo, z_hi); a threshold event
  counts only if the element's current position is also inside the fine zone at least 2h from its edges. The same physical
  region at all three h.
- **Strong-coupling / breakdown flags.** (F1) the hold-law iteration does not converge within the cap; (F2) max x on the
  grid exceeds 50 (flux (1 − μ)|∇Ξ̃| ≥ 0.98 a₀, the edge of the hold law's solvability); (F3) particles leave the box.
  Each flag records its first time and location.

## 4. Checks (scripts print `ID PASS/FAIL value threshold`; exit 0 iff all PASS)

- **R0 (the review reproduced, read-only).** The review's `caustics.py` definitions are executed from its source (the part
  before its C0 block, as its own `caustics_validity.py` does; nothing in `reviews/` is written). Its `integrate` for
  (canonical, O2, t_i 3, s 0), (canonical, O2, t_i 3, s 1), (canonical, O1, t_i 3, s 0) and (alt, O2, t_i 9, s 0) must give
  `det_min_to_t_end` within 1e-6 (absolute) and `t_sc` equal within 1e-9 (or both None) of `caustics_results.json`.
- **V-a1 (static equilibrium).** One Plummer mass (M31, 1e11 M☉, ε = 20 kpc) at rest, both footings, h ∈ {20, 10, 5},
  10 Gyr: max |J − 1| ≤ 1e-4 and max particle displacement ≤ 1e-2 kpc. (The AQUAL initial state leaves the stiffness
  force unbalanced at ~(L★/ℓ)² ~ 1e-5 of the self-force, hand estimate, so a few 1e-5 in |J − 1| is physics, not drift.)
- **V-a2 (moving equilibrium, Galilean).** The same mass and its AQUAL khronon both given v = 110 km/s along +z (the
  Dirichlet data follow the mass), canonical footing, h ∈ {20, 10, 5}, 6 Gyr; fine zone R ≤ 500, z ∈ [−400, 1100] kpc.
  The exact solution translates rigidly. PASS iff at h = 10 and h = 5 the maximum over elements with labels in the
  validated region, ≥ 2ε from the mass's initial position and ≤ 300 kpc from it, of |J − 1| is ≤ 0.1. Reported: the same
  inside 2ε, and the comoving displacement.
- **V-b (linear dispersion on both sides of D·P = 0).** Test background in the same code (same grid operators, deposit,
  solvers, integrator, stiffness switch): khronon density ±ρ₀ (Kρ₀ = 0.5 Gyr⁻²) in the cylinder R ≤ 200 kpc, |z| ≤ 200 kpc,
  tapered to 0 by cos² over the next 40 kpc; external field by Dirichlet data Ξ̃_bdy = g₀z with g₀ = a₀ (x₀ ≈ 1); the
  static "baryon" potential is set to φ_ext ≡ χ of the background so the background is exactly stationary. Fine zone
  R ≤ 320, |z| ≤ 320 kpc, h ∈ {8, 4, 2} kpc, graded (q = 1.08) to 3 Mpc. Modes (displacement amplitude 1e-4 λ, λ = 50 kpc,
  k = 2π/λ):
  - **L±** longitudinal (k ∥ field): ξ_z = A sin(kz) for R ≤ 200, |z| ≤ 200; prediction ω² = Kρ̄((1 + x)² − 1 + Θ(ρ̄) L★²k²/2);
  - **T±** transverse (k ⊥ field): ξ_R = A J₁(k R) for R ≤ 200, |z| ≤ 200, with k the first value ≥ 2π/λ at which
    J₁(k·200 kpc) = 0; prediction ω² = Kρ̄(x + Θ(ρ̄) L★²k²/2);
  - with ρ̄ and x the background values at the centre. Measured: the amplitude projected on the mode shape over the
    central region (R ≤ 100, |z| ≤ 100 kpc), fitted by least squares to A cos(ωt) (ρ̄ > 0, window 1.5 predicted periods)
    or A cosh(Γt) (ρ̄ < 0, window 2.5 predicted e-folds).
  - PASS iff at h = 2 kpc |ω_meas/ω_pred − 1| ≤ 0.05 for all four modes. The h = 8 and 4 values are reported.
- **V-c (resolution convergence).** The per-case convergence of §5 (reported per case; it enters the verdict there).
- **N-dt, N-box, N-tol (numerical parameters).** Case (canonical, O2, t_i 3) at h = 10 with, one at a time, dt/2,
  B_out = 10 Mpc, tol = 1e-8. PASS iff each changes the case statistic S (§5) by ≤ 0.02 absolute and, if the case reaches
  the threshold, its first threshold time by ≤ 0.2 Gyr.
- **MUTATE (`X8_MUTATE=1`): frozen F.** The self-consistent update is dropped: the khronon acceleration is
  ∇(χ₀ − φ_b(t)) with χ₀ the t_i solution frozen on the grid (no deposit, no solves; the review's s = 0 model on this
  lane's grid and AQUAL sign map). It must FAIL V-b (no restoring force: ω_meas ≈ 0) and V-a2 (the khronon stays behind).
  Reported in the MUTATE outputs (no pass weight): **MUT-R**, whether the O2 cases at h = 10 reach J ≤ 0 for some soft
  element by t_end on both footings, as the review's frozen-F model did in 6/6 O2 cases; and the frozen-F S for all 12
  cases × 3 resolutions. Outputs keep `_MUTATE` in their names.

## 5. The statistic and the frozen verdict

- **Case statistic S(h)** = the minimum over soft elements (m(q) < 0) of the validated region, and over diagnostic times in
  [t_i, t_end], of J.
- **Threshold event.** An element reaches the caustic threshold at t_c if J < **J_crit = 0.05** at every diagnostic sample in
  [t_c, t_c + 0.1 Gyr] (sustained; this includes J ≤ 0, a fold). t_c(h) = the earliest such time over the case's soft
  validated elements.
- **Per case** (using h_mid = 10 and h_fine = 5 kpc; h = 20 reported for the trend):
  - **CAUSTIC** iff a threshold event occurs at both h = 10 and h = 5 with |t_c(5) − t_c(10)| ≤ max(0.5 Gyr,
    0.1 (t_c(5) − t_i));
  - **NO-CAUSTIC** iff no threshold event at h = 10 or h = 5, S(5) ≥ J_crit, and |S(5) − S(10)| ≤ 0.05;
  - **UNDECIDED** otherwise (named: NOT CONVERGED), or if F1/F2/F3 fires before any threshold event and before t_end
    (named: STRONG-COUPLING / BREAKDOWN FLAG).
- **Overall verdict (frozen classes).**
  - **CAUSTICS FORM** iff R0, V-a1, V-a2, V-b and N-* all PASS and at least one case is CAUSTIC. Reported with the case(s),
    t_c relative to t₀, the element's position relative to the null and the nearer galaxy, and whether t_c < t₀ and
    t_c < t_i + 13.8 Gyr.
  - **NO CAUSTICS TO T_H** iff R0, V-a1, V-a2, V-b and N-* all PASS and all 12 cases are NO-CAUSTIC. (The window [t_i, t_end]
    covers at least a Hubble time of evolution in no case but O2 t_i 3, where it covers 15.07 Gyr; both sub-windows are
    reported.)
  - **UNDECIDED** otherwise, naming the failed validation(s) or the undecided cases.
- No case selection after any number; footings are never pooled (each case is per footing).

## 6. Diagnostics (reported only; no verdict weight)

- **D-WAKE (coordinator request, received before this freeze; frozen here).** For each galaxy and each side of it on the
  axis: the elements (any sign) whose current position has R ≤ 30 kpc and 2ε ≤ |z − z_g| ≤ 1000 kpc on the outer side
  (away from the other galaxy), or 2ε ≤ |z − z_g| ≤ 0.5 r(t) on the inner side. Per case and h: the minimum J over the
  window, its time, position, the element's charge sign, and the galaxy's direction of motion at that time (so "behind"
  = downstream can be read off). This is the Danby–Camm focal line of O1 §3(ii), separate from the saddle soft region.
- **D-STIFF.** The minimum J over positive (stiff-side) elements in the validated region, with time and place.
- **D-GRADED.** The minimum J over soft elements outside the validated region (graded zone or fine-zone rim).
- **D-FOLLOW.** For each galaxy, the mass-weighted mean z-displacement of the positive particles labelled within 50 kpc of
  it, divided by the galaxy's own displacement since t_i, at t₀ and at t_end; and the maximum transverse sloshing.
- **D-SC.** The flags F1–F3 with times; max x(t); ω_max(t)·dt; hold-law iterations per call; the stiffness-to-self-force
  ratio at t_i.
- **D-FROZEN.** The MUTATE (frozen-F) S and first-crossing times, side by side with the self-consistent ones and with the
  review's t_sc.

## 7. What a result can and cannot say

It answers the classical question in the review's model: axisymmetric, prescribed kinematic orbits, Plummer baryons, no
Hubble flow, no other Local Group members, no dust, μ_K → 0, v = 0 initial khronon. It does not test non-axisymmetric
flows, the baryons' response to the khronon, a completion after a fold, or quantum strong coupling (the strong-coupling
review covers that). A CAUSTICS FORM verdict would mean the single-stream khronon of v3s folds in this setting; a NO
CAUSTICS verdict would mean it does not within the window at the resolved scales (≥ 5 kpc), not that no sub-grid fold
exists. Neither is a data comparison.

## 8. Compute

`OMP_NUM_THREADS=1 nice -n 15`, one thread, < 1 GB RSS per process, each run ≤ 30 min with checkpoint/resume (SIGTERM
checkpoint). At most three such processes at once, and none while `compute_queue/heavyq.py status` shows low free memory.
The heavy queue and every other lane are not touched. No downloads.
