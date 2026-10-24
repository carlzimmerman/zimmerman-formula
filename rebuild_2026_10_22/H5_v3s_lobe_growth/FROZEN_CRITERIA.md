# H5_v3s_lobe_growth: do v3s's D·P < 0 lobes produce harmful growth? FROZEN CRITERIA

Written and committed (with `ASSUMPTION_LEDGER.md`) before the lane script exists and before any script has produced a
number. Rules: `rebuild_2026_10_22/BRIEF.md`, `doors_push_2026_10_22/BRIEF.md` + `BRIEF_E_AUDIT.md`. κ = ½ is FITTED.
Footings canonical a₀ = 9.3603e-11 m/s² and alt a₀ = 1.1312e-10 m/s² (9.36e-11 / 1.13e-10 inside reused H4 code), never
pooled. No dark-matter particle. Never "theory closed"; nothing here says the data favour the framework. Small compute only
(`OMP_NUM_THREADS=1 nice -n 15`, < 1 GB, minutes); a heavy run is live and is not touched. No downloads. X3, H4, V1, S1,
U1, D10 files are read (and code imported or copied) read-only.

## 0. What was read before freezing, and the not-blind statement

Read: X3 (README, D4_maps json rows, script: `SW`, `g_mw`, `s_gal`, `task_D4maps`, constants); H4 (README, script Part D
`region_stats`/`rates`, json `efolds`/`regions`/`meta`); L1 FROZEN_CRITERIA §1 (the PN system); U1 README (T3, part (b),
A2) and both CSVs' headers; S1 README and `s1_per_system.csv` header; D10 `d10_solver.py` and the json cluster inputs;
V3_FULL_PICTURE §4.7 (the preliminary 15–86 e-folds / N ≲ 0.1 statement).

**Not blind.** Hand work done before this file (nothing run):
- **Euler/continuity.** From H4 A1's Lagrangian, the σ equation is continuity for the khronon charge ρ_τ = D·P − μ_K²Ξ/K
  with v_τ = −∇σ, and the Bernoulli definition of Ξ gives Dv_τ/Dt = −∇(φ − Ξ) (L1 §1).
- **Galilean boost.** σ′ = σ + V·x′ + V²t/2 leaves Ξ invariant and gives v′ = v − V. So the static branch (σ = −Ct,
  Ξ = φ + C, v_τ = 0) holds in exactly one frame, the khronon's rest frame (U1 part (b)).
- **Steady linear response in the system frame** (uniform host background ρ̄ > 0, host field along n, stiffness on since
  ρ̄ > 0): δρ_τ(k) = δρ_m(k) / [M(k̂) − 1 + Θ L★²k²/2 − (k·V)²/(Kρ̄)], M(k̂)⁻¹ = cos²/M_L + sin²/M_T. At V = 0 this is
  D10 Route F's screened kernel; for (k·V)² ≫ Kρ̄(M − 1) it is −Kρ̄ δρ_m/(k·V)², the cold-flow wake (first order only on
  the source's line; off the line the perturbation is second order).
- **Sign invariance.** Along v_τ, ρ_τ(X, t) = ρ_τ(X, 0)/J(X, t). A fluid element that enters with ρ_τ > 0 cannot reach
  ρ_τ < 0 before a caustic. Cold flow past a point mass (Danby–Camm form, b the impact parameter, R = r sin θ):
  ρ/ρ∞ = b²/[R(2b − R)] = u²/(2u − 1) ≥ 1 with u = b/R. So host khronon flowing through a lobe region is never rarefied.
- **Orders of magnitude (hand, not thresholds).** NGC 2419's deepest lobe cell (3.3e-3 M☉/pc³, x_e 0.10) has bounded rate
  ~2e-16 s⁻¹ (86 per T_H, as the preliminary). With ℓ ~ 1 kpc and V ~ 150 km/s, N ~ 0.04. The linear crossover speed
  V_* = ℓ√(Kρ̄(M − 1))/2π is ~0.2–1 km/s at kpc scales for ρ̄ ~ 1e-4 M☉/pc³. U1's capture radius 2GM_b/V² is ~0.25 pc for
  NGC 2419 at 167 km/s. A pure radial orbit at apocentre gives ~1 e-fold in the deepest cell (residence √(2ℓ/g_e) each
  way); I have not computed it on the maps.
- **Data gap found before freezing.** No globular-cluster 3-D velocities are on disk (Baumgardt's `combined_table.txt`
  and BH2018 CDS tables have none; no Vasiliev & Baumgardt 2021 / LVD GC table). See §2(a): PROXY speeds plus a
  speed-independent envelope.

## 1. Part A: the khronon velocity relative to a moving system's lobe (sympy; all residuals must be identically 0)

- **A1 (EL equations).** H4 A1's PN Lagrangian with the switched stiffness written as a generic F(∇·P):
  L = −|∇φ|²/2K − ρ_mφ − Ξ∇·P − W(K|P|) − (γ_L/2)F(∇·P) + μ_K²Ξ²/2K, Ξ = φ − σ̇ + |∇σ|²/2 (1D and 2D, sympy
  `euler_equations`). PASS iff the σ equation equals ∂_tρ_τ + ∇·(ρ_τ v_τ) with ρ_τ = ∇·P − μ_K²Ξ/K, v_τ = −∇σ; the φ
  equation equals ∇²φ = K(ρ_m + ρ_τ); and ∇ of the Ξ definition equals D_t v_τ = −∇(φ − Ξ). Residuals 0.
- **A2 (frame).** With x = x′ + Vt, σ′ = σ + V·x′ + V²t/2: PASS iff Ξ′ − Ξ ≡ 0 and v′ − (v − V) ≡ 0 (2D, generic σ).
  The static branch in the khronon frame becomes v′ = −V in a frame moving at V.
- **A3 (steady linear response in the system frame).** Fourier system in 2D (k at angle α to the host field n, V at angle
  β): continuity, Euler, Poisson with a baryon source δρ_m, the P equation with the anisotropic Hessian
  K⁻¹[M_L nn + M_T(1 − nn)] and stiffness γ_LΘ, and ρ_τ = ∇·P (μ_K = 0). Solved by sympy for δρ_τ, δv, δΞ, δφ. PASS iff
  (i) δρ_τ equals the §0 formula (residual 0); (ii) at V = 0 it equals D10 Route F's kernel m/(1 − m + κ²m/2) (κ = kL★,
  m = 1/M) times δρ_m (residual 0); (iii) its V → ∞ limit is −Kρ̄δρ_m/(k·V)² and δv → k δψ/(k·V) with δψ → −Kδρ_m/k²
  (the baryons' Newtonian potential) (residual 0).
- **A4 (sign invariance).** For a generic smooth 2D Lagrangian map x(X, t), ρ = ρ₀(X)/det(∂x/∂X) satisfies continuity
  (Jacobi's formula; sympy residual 0).
- **A5 (flow through the lobe, nonlinear).** The Danby–Camm field (hyperbolic orbits about a point mass, impact parameter
  b(r, θ) = [R + √(R² + 4r(GM/V²)(1 + cos θ))]/2, θ from the downstream axis) with ρ/ρ∞ = b²/[R(2b − R)] satisfies steady
  continuity: max |∇·(ρv)| / (ρ∞V/r) ≤ 1e-9 at 200 random points (sympy derivatives evaluated numerically), and
  ρ/ρ∞ − 1 = (b − R)²/[R(2b − R)] ≥ 0 (sympy identity). A numerical Lagrangian integration (cold test particles, point
  mass, Jacobian from neighbouring trajectories) agrees with the formula to ≤ 1e-3 at ≥ 20 test points with min ρ/ρ∞ ≥ 1.
  The same integration in the Plummer potential of NGC 2419 is reported (not gated) at lobe radii.

**The derived statement (reported with the numbers):** beyond the capture radius r_cap = 2GM_b/V² (U1, LIT) and for
V ≫ V_*, the lobe pattern (a function of the system's baryons and the host field direction) moves with the system; the
khronon fluid stays in the host frame, with velocity relative to the system −V + δv, |V + δv|² = V² + 2GM_b/r along each
streamline. A fluid element's residence time in the lobe is its path length / V.

## 2. Part B: lobe e-folds

**Rates.** H4's `rates()` copied verbatim: bounded-branch rate Γ = √(4πG|ρ_τ|((1 + x)² − 1)) (M_L, the upper end), plus
H4's other columns. Local Γ_loc on each lobe cell uses the cell's own |ρ_τ| and local x = |v|/a₀ from the solution.

**B0 (reproduce the record first).**
- B0a: H4 row `S1_MW-M31|canonical|e0|L*21.7`: recompute `median` and `max` with the copied `rates()` from H4's json region
  stats and H4's T = min(T_H, ℓ/v). PASS iff every field matches H4's json to ≤ 1e-12 relative.
- B0b: X3 D4 maps: with D10's solver (imported read-only) and X3's `SW`, `g_mw`, `s_gal` (copied), recompute
  `min_total_Msun_pc3` for the 4 clusters × 2 footings at the D10 central floor. PASS iff ≤ 1e-6 relative to X3's json.
- B0c: S1 host field: S1's `g_host` (copied with S1's constants) at d_host, E_mid, reproduces S1's `x_e_mid` for the 32 MW
  satellites, both footings, ≤ 1e-9 relative. (X3's `g_mw` uses D10's rounded constants; its agreement is reported.) The
  satellite maps use S1's `x_e_mid`, `y_plummer`, `rh_pc` as given.

**Maps.** v3s static maps from X3's switched operator (`SW`, switched = True, s_g = the host's phantom at the system's
galactocentric distance, D10 grid `Grid2D(nper=24, Nt=16)`); total ρ_τ = (D + s_g)·a₀/(4πG a). The unswitched map is
solved first (warm start) and its lobe statistics are reported alongside. Lobe = cells with total ρ_τ < 0. Cell volume
2π a³ Δ(r³)/3 Δ(cos θ).
- (a) **Outer globulars:** NGC 2419, Pal 3, Pal 4, Pal 14 (D10 inputs; Υ_V = 1.6; E_mid MW), L★ ∈ {D10 central floor, 24,
  90} pc, both footings (as X3 D4_maps).
- (b) **MW satellites:** the 32 MW systems of S1 with U1's LVD-3D speeds (S1's y, a = r_h, x_e_mid; d_host for s_g),
  L★ ∈ {D10 central floor, 90} pc, both footings. M31 satellites and Leo T (PROXY speeds) are not in this class.

**Statistics per system × footing × L★ (lobe non-empty):**
- ℓ = V_neg^⅓; volume-weighted median |ρ_τ| and x; deepest cell |ρ_τ| and its x; r-range and θ of the deepest cell.
- **N_TH** = Γ_deep · T_H (co-moving for a Hubble time; reproduces the preliminary 15–86 as a reported line).
- **N_ℓ** = Γ_med · min(T_H, ℓ/V) and Γ_deep · min(T_H, ℓ/V) (H4's lifetime convention).
- **N_path(V)** = max over straight paths of (1/V)∫Γ_loc ds. Paths: directions at 0°, 30°, 60°, 90° to the host field;
  for each, a 61 × 61 grid of offsets over ±1.05 r_max of the lobe in the plane ⟂ the path; 4000 samples per path;
  Γ_loc bilinear in (ln r, θ). Validated (B2) on a uniform-Γ sphere: max path integral = 2R·Γ to ≤ 1 %.
- **V_crit** = max path ∫Γ_loc ds (the speed below which N_path ≥ 1).
- **N_apo** (radial orbit at apocentre; relative displacement s = g_e t²/2 along the host field, both signs, the system
  momentarily at rest): N_apo = max over paths ∥ n and turning points s₀ of (4/√(2g_e)) ∫₀^∞ Γ_loc(s₀ ± u²) du, g_e = x_e a₀.
  Validated (B3) on a uniform-Γ slab of length L with the turning point at its edge: analytic 2Γ√(2L/g_e), ≤ 1 %.
- **Pile-up bound** n_enc = 2 T_H/T_orb, T_orb = 2π d_host/V; N_cum = N_path · n_enc (an upper bound: every passage is
  assumed to re-cross the same fluid element; between crossings the element sits at ρ_τ > 0, where modes oscillate).
- **Flow state** (A5 at the record speed): min and max of ρ_τ/ρ̄_host over the lobe cells (×16 azimuths) for V ∥ n and
  V ⟂ n, point mass M_b, ψ = φ_N; max |δv| = √(V² + 2GM_b/r_in) − V; r_cap = 2GM_b/V² against the lobe's inner radius;
  V_* = ℓ√(K ρ̄_host (M_L − 1))/2π at the lobe's median x.

**Speeds.**
- (b) satellites: U1's `V_kms` with `V_src = LVD-3D` (RAW proper motions + v_los, U1's Galactocentric frame).
- (a) globulars: **MISSING on disk** (needed: 3-D Galactocentric velocities, e.g. Vasiliev & Baumgardt 2021 or Baumgardt's
  orbit table). Used instead: V_c = √(g_mw(R_GC)·R_GC) of D10's MW model (E_mid) — PROXY — and the speed-independent
  envelope: V_apo,10 = V_c √(2 ln 10/99) (apocentre of a flat-curve orbit with r_a/r_p = 10) and the pure radial apocentre
  (class c).

## 3. Verdict rules (frozen)

Per class, each footing separately; the class verdict is the worse footing's. Two layers are always both reported:

**Layer P (pattern granted — conservative).** The static v3s lobe density is granted to the fluid that crosses it.
- **BENIGN**: max over the class of N_path(V) < 1 **and** max N_cum < 1 at the L★ floor (24 / 90 reported). For (a), also
  max V_crit < V_apo,10 (so no bound orbit with r_a/r_p ≤ 10 can reach N_path ≥ 1 at any phase).
- **BOUNDED-BUT-LARGE**: some system has N_path ≥ 1 or N_cum ≥ 1 at the record speed (finite: bounded branch).
- **UNDETERMINED**: the verdict needs data not on disk (for (a): BENIGN fails only through V_crit ≥ V_apo,10, i.e. the
  missing speeds decide), or needs nonlinear saturation physics.

**Layer D (dynamics — the derived flow state).** If A1–A5 pass and, at the record speed, r_cap < the lobe's inner radius
and min ρ_τ/ρ̄_host ≥ 1 over the lobe for every system in the class, the lobe region holds host khronon with D·P > 0 (stiff
side, ω² ≥ 0): "**NO NEGATIVE LOBE IN THE FLOW STATE**". Otherwise "layer D not established".

**(c) worst case.** (c1) N_apo per system (pure radial orbit, both classes). (c2) co-moving for T_H: N_TH (posited).
Verdict: BENIGN if max N_apo < 1 and no system has r_cap ≥ r_lobe,in (no co-moving lobe allowed by v3's capture law);
BOUNDED-BUT-LARGE if max N_apo ≥ 1 or a co-moving lobe is allowed; each with layer D's reachability statement (A4: negative
charge cannot be produced from ρ_τ > 0 initial data). If the reading needs the end state of a would-be lobe (vacuum vs
flow), the README says so plainly: that is nonlinear physics not computed here.

## 4. Checks (exit 0 iff all pass) and mutation

A1, A2, A3, A4, A5, B0a, B0b, B0c, B1 (every solve converged: residual ≤ 1e-8; no lobe statistic non-finite), B2 (uniform
sphere path test ≤ 1 %), B3 (slab apocentre test ≤ 1 %).

`H5_MUTATE=1` (outputs `*_MUTATE.*`): A2 uses σ′ = σ + V·x′ (no V²t/2); A3 drops the Doppler term (k·V → 0 in the
continuity/Euler pair); A5's numerical integration uses a repulsive mass. A2, A3 and A5 must FAIL (exit 1). The maps and
statistics are not rerun in the mutated mode.

## 5. Not in scope

No time evolution of a would-be lobe, no 2D/3D nonlinear khronon simulation, no caustic physics, no re-scoring of D10,
satellites or any tile. Consequences for other lanes (e.g. a moving system's static EFE solution) are reported as readings
only.
