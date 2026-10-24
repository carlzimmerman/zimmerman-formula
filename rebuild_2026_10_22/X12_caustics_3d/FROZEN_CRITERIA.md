# X12_caustics_3d: without axial symmetry, does the khronon wake behind a moving Milky Way-mass galaxy still focus, and do the soft-side folds survive an impact parameter? FROZEN CRITERIA

Written and committed (with `ASSUMPTION_LEDGER.md`) before any lane script exists and before any script of this lane has
produced a number. Rules: `rebuild_2026_10_22/BRIEF.md`, `doors_push_2026_10_22/BRIEF.md` + `BRIEF_E_AUDIT.md`. Lane launched
by the coordinator from the open items of X8 and X10 ("the axis collapse and the axis focus may be artefacts of axisymmetry;
non-axisymmetric encounters not run") and the V3_FULL_PICTURE §6 rows "Soft-side caustics in v3s" and "Dynamical state of
moving subsystems". κ = ½ is FITTED. Footings canonical a₀ = 9.3603e-11 m/s² and alt a₀ = 1.1312e-10 m/s², never pooled. No
dark-matter particle. Never "theory closed"; nothing here says the data favour the framework. Small jobs only:
`OMP_NUM_THREADS=1 nice -n 15`, < 1 GB RSS, each run ≤ 30 min (checkpoint/resume), at most two at once; the heavy queue and
every other lane untouched; no downloads.

## 0. What was read before freezing, and the not-blind statement

Read: `rebuild_2026_10_22/BRIEF.md`; X8 (README, FROZEN_CRITERIA + A1–A3, `x8_core.py`); X10 (README, FROZEN_CRITERIA,
ASSUMPTION_LEDGER, `x10_run.py`, `x10_validate.py`, `x10_validate.out`); O1 README §3(ii) (the downstream focal line);
H5 README (A2 Galilean covariance, A5 Danby–Camm); V3_FULL_PICTURE §6.

**Not blind.** I know X8's and X10's results:
- X10 (co-moving start, axisymmetric): O2 soft folds CAUSTIC in t_i 3 and 6 on both footings (t_c at h 20 / 10 / 5:
  canonical t_i 3 16.350 / 15.948 / 15.800, alt t_i 3 16.840 / 15.908 / 15.325; t_i 6 17.97–18.00 / 17.28–17.39 /
  16.65–16.78), t_i 9 folds only at h 5. The events sit 73–240 kpc from MW, at R = 0–73 kpc from the axis; their labels
  start at R_q = 10–120 kpc, z_q ≈ −275 to −410 kpc.
- X10 (b): behind MW the wind focuses onto the axis 76–91 kpc downstream at t_i + 3.9–4.4 Gyr (O2 t_i 3 MW downstream event
  7.49 / 7.32 / 6.90 at h 20 / 10 / 5, canonical); the upstream side drops below 0.5 only after ~11 Gyr; FOCAL LINE
  PRESENT in the two O2 t_i 9 MW cells (window 9.067 Gyr), NOT SINGLED OUT on the longer windows.
- X10 D-ISO (isolated MW-mass, 68.75 km/s, held ball 106 kpc boosted, rest at rest; committed
  `x10_validate_results.json`): downstream event at 4.880 / 4.321 / 3.922 Gyr (canonical, h 20 / 10 / 5) and 4.900 / 4.332 /
  3.928 (alt); upstream minimum over 15.167 Gyr 0.496 / −101 / −186 (first < 0.05 at —, 12.8, 11.3 Gyr), class NOT SINGLED
  OUT.
- Solver statistics of X10's O2 runs: ~7 hold-law iterations per force call, 0.5k–1.6k steps, ω_max 8–15 Gyr⁻¹.

Scoping before this freeze (no physics number of this lane): a single-thread BLAS timing on this machine (a 100 × 100
matrix times 100 × 13950: 1.6 ms) to size the 3D grids. No 3D or 2D evolution was run.

Hand estimates (nothing run):
- **Symmetry.** The encounter with impact parameter b in the x–z plane and both velocities along z is exactly symmetric
  under y → −y. The isolated mass moving along the z axis is symmetric under x → −x and y → −y. Storing y ≥ 0 (and x ≥ 0)
  with mirror (natural) boundary conditions, true particle positions (particles may cross the plane) and a mirror-folded
  deposit is the full-domain problem for mirror-symmetric data; it halves (quarters) the cost. For b > 0 no axial symmetry
  is imposed: the only imposed symmetry is the y-mirror that the encounter has exactly. Round-off would break the mirror in
  a full-domain run only at ~1e-16 × e^(Γt), Γ ≲ 1 Gyr⁻¹ in the deep-MOND lobe, i.e. ≲ 1e-9.
- **Generic caustics.** A cold stream past a point mass focuses on the axis (Danby–Camm; focal distance b²V²/2GM,
  ≈ 95 kpc for MW at 70 km/s and b = 100 kpc). In axisymmetry the focus is a line; under a non-axisymmetric perturbation the
  degenerate line focus unfolds into fold surfaces (a sheet caustic, one collapsing direction) rather than disappearing,
  unless the self-field's restoring force (ω² ≈ 2GM/r³ in the deep halo) prevents the crossing. The diagnostic D-SV (§6)
  separates line foci (two collapsing directions) from sheet folds (one). No expectation for either verdict.
- **Cost.** One particle per unknown node; ~7 hold iterations per step; ~1.3k steps for a 15 Gyr window at ω_max ≈ 13. The
  encounter box at h = 10 kpc in the half domain is ≈ 1.5M nodes (≈ 0.5 GB with float64), ≈ 1 s per step with compiled
  kernels; h = 7.5 or 5 kpc does not fit under 1 GB. Hence the 3D ladder h ∈ {20, 15, 10} kpc (coarser than X10's
  {20, 10, 5}).
- **Why the encounter uses t_i = 3 Gyr.** It is the only O2 epoch whose 2D soft folds occur at every resolution X10 ran
  (h 20 / 10 / 5) well inside the window. t_i 6 folds at h 20 only 0.07–0.1 Gyr before t_end; t_i 9 does not fold at
  h 20 or 10. At 3D resolutions (h ≥ 10) only t_i 3 can serve as an axisymmetric (b = 0) control. This choice uses X10's
  committed numbers and is made before any 3D number.
- **Why the wake window is 9.067 Gyr.** It is the window of X10's two PRESENT cells (O2 t_i 9: 18.067 − 9). The 2D
  isolated-mass upstream side drops below 0.5 only after ~11 Gyr, so this window excludes the held-halo erosion by
  construction (known before freezing; disclosed). The longer-window classes are reported (D-FULL), with no verdict weight.

## 1. The theory (v3s) and its weak-field dynamics (X8 §1, unchanged)

v3s = v3 with the switched stiffness −(γ_L/2)[max(D·P, 0)]². Weak-field PN system, μ_K → 0, no BS dust (X8 §1):

    ∇·[ (1 − μ(|∇Ξ̃|/a₀)) ∇Ξ̃ ] = 4πG ρ_τ        (hold law; μ = x/(1+x); Ξ̃ = Ξ + γ_L ρ₊, ρ₊ = max(ρ_τ, 0))
    ∇²φ_τ = 4πG ρ_τ ,  φ = φ_b + φ_τ               (Poisson)
    ∂_t ρ_τ + ∇·(ρ_τ v_τ) = 0 ,  D v_τ/Dt = ∇(Ξ̃ − φ_τ − φ_b) − γ_L ∇ρ₊

Static equilibrium: AQUAL with φ_b → φ_b + γ_L ρ₊ (X8 A1(e)). γ_L = K L★²/2, K = 4πG, L★ = 21.682 / 22.849 pc. The baryons
are Plummer masses (ε = 20 kpc) on prescribed kinematic orbits; no back-reaction on them (X8, X10).

## 2. Cases (no case is added or removed after any number)

**(W) Wake: an isolated MW-mass galaxy in uniform motion.** M = 6e10 M☉, ε = 20 kpc, moving along +z from the origin at
V = 68.75 km/s (MW's O2 speed). Start (X10 §2, D-ISO): positions and masses are the discrete v3s switched static
equilibrium of the mass at the origin; labels with e(q) = V²/2 − GM/(|q|² + ε²)^½ < 0 (held) start at v = V ẑ, the rest
at rest. Dirichlet data: the spherical AQUAL potential of M about the start position, fixed (X10 D-ISO: the far khronon is
at rest). Window [0, W_a], **W_a = 9.067 Gyr**; the run continues to W_a + 0.1 Gyr for event confirmation only. Both
footings: **2 cases**. Quarter domain (mirrors x = 0, y = 0).

**(E) Encounter: O2-like, with impact parameter b.** MW (6e10 M☉) at (−f₂b, 0, −f₂d(t)), M31 (1e11 M☉) at (f₁b, 0, f₁d(t)),
f₁ = 0.375, f₂ = 0.625, d(t) = r_O2(t) = 780 kpc + 110 km/s · (t₀ − t) (X8's O2 formula); both move along z only (MW at
+68.75, M31 at −41.25 km/s); for b = 0 this is X8/X10's O2 exactly. **t_i = 3 Gyr**; window [t_i, t_end], t_end = 18.067 Gyr
(d = 300 kpc, X8), run to t_end + 0.1. **b ∈ {0, 50, 150} kpc** (0: the axisymmetric control; 50: inside MW's held radius
~107 kpc and at the 2D fold distance from the axis; 150: beyond MW's held radius; both below the separation 300 kpc at
t_end). Start: X8's discrete v3s switched static equilibrium of the two masses at their t_i positions, with X10 §2's
co-moving rule unchanged (labels with e_g < 0 ≤ e_g′ are held by g and start at v = V_g ẑ; common and background labels at
rest; e_g = V_g²/2 − GM_g/(|q − x_g(t_i)|² + ε²)^½). Dirichlet data: the spherical AQUAL potential of M_MW + M_M31 about the
barycentre (the origin), fixed (X8). Both footings: **6 cases**. Half domain (mirror y = 0) for every b, including b = 0.

## 3. Numerical method (3D)

- **Grid.** Tensor product, nodes on every axis. Fine zone uniform spacing h; beyond it the spacings are hq, hq², … with
  **q = 1.25** until the coordinate magnitude reaches ≥ **B_out = 5000 kpc** (measured from the origin: the start position
  for single-mass boxes, the barycentre for E). Outer faces are Dirichlet; mirror planes carry unknown nodes with the
  natural (zero normal flux) condition. **h ∈ {20, 15, 10} kpc**; all fine-zone bounds are multiples of 60 kpc.
  - Box S (single mass, quarter domain, mirrors x = 0, y = 0), fine x, y ∈ [0, 240] kpc and z ∈:
    V-a1 [−240, 240]; V-cm MW [−360, 1440]; V-cm M31 [−360, 1020]; W [−480, 1200].
  - Box E (half domain, mirror y = 0): fine x ∈ [−300, 300], y ∈ [0, 240], z ∈ [−1440, 1260] (MW's held ball over its whole
    track and M31's held ball, radius ≈ 506 kpc, at its start lie inside the fine z range; held material outside the fine
    x, y range moves along z only, where the z spacing is uniform).
- **Discrete fields (variational finite differences; X8 A1(a) with the Q1 element replaced).** For a cell c with spacings
  (Δx, Δy, Δz) and volume V_c, g_c² = ¼ Σ over its four x-edges (δu/Δx)² + the same for y and z. E_c[u] = Σ_c V_c F_c(g_c)
  over the stored cells, and R_c(u)_n = ∂E/∂u_n with F′(g)/g = c: **c = 1** (Poisson; R_1 is exactly the 7-point Laplacian
  times the dual volume, so there is no hourglass mode), **c = μ(g/a₀)** (AQUAL), **c = 1 − μ** (hold law). Equations: hold
  R_{1−μ}(Ξ̃) = −K m; Poisson R_1(φ_τ) = −K m; static AQUAL R_μ(Ξ̃) = R_1(φ_b + γ_L ρ₊). m_n = deposited nodal khronon
  masses, ρ₊,n = max(m_n/V_n, 0) (V_n the dual volume). Every operator is the gradient of a discrete energy, so the particle
  system is Hamiltonian (X8 A1's requirement): −∂U/∂m_n = (Ξ̃ − φ_τ − φ_b − γ_L ρ₊)_n by the envelope theorem.
- **Particles.** One per unknown node, labelled by it. Quadratic B-spline (TSC) shapes in index space (X8 A1(b) in 3D):
  3 × 3 × 3 nodes; on a mirror axis node −1 is folded onto node 1, and a particle at a negative mirrored coordinate deposits
  and interpolates at |coordinate| with that force component's sign flipped (positions are stored unreflected). Particle
  masses are the exact separable deconvolution of the equilibrium nodal masses. Acceleration a_p = ∇ Σ_n (ζ − γ_L ρ₊)_n
  S_n(x_p), ζ = Ξ̃ − φ_τ − φ_b (energy-conserving).
- **Soft set.** A label is soft iff its equilibrium nodal mass m_n < 0 (X8 A1(c)); stiff iff > 0.
- **Initial state (X8 A1(e)).** Discrete AQUAL by Newton–PCG (exact Hessian of E_μ, preconditioned by the diagonally scaled
  fast Laplacian), from the QUMOND-like solve, to relative residual ≤ 1e-12 or stagnation (printed); stiffness outer fixed
  point (φ_b → φ_b + γ_L ρ₊(Ξ̃), ≤ 12 outer iterations, stop at max|ΔΞ̃| ≤ 1e-9 a₀ h_min); m = −R_{1−μ}(Ξ̃)/K; φ_τ boundary
  data Ξ̃_bdy − φ_b,bdy (so ζ ≡ 0 and the start is force-free to solver precision).
- **Solvers.** The separable 7-point operator by fast diagonalisation (dense symmetric eigendecompositions in x and y,
  batched tridiagonal solves in z; exact to round-off). Hold law: X8's Anderson fixed point (depth 5), stop when
  max|ΔΞ̃| ≤ tol a₀ h_min with **tol = 1e-7**, cap 300 iterations (flag F1), warm-started by linear extrapolation.
- **Integrator.** KDK leapfrog, dt = min(dt₀, 0.15/ω_max(t)), dt₀ = min(0.02 Gyr, 0.15/ω_max(t_i)), floor dt₀/50 (flag F4),
  ω_max = max_n [K|ρ_n|((1 + x_n)² − 1)]^½ (X8 A1(g)).
- **The Jacobian.** J(q, t) = det ∂x/∂q by centred differences over the ±1 label neighbours in each direction (mirror
  ghost labels across the planes: the ghost of label (q_x, q_y, q_z) at −q_y is (x, −y, z)). Evaluated every 0.02 Gyr.
- **Validated region.** Labels in the fine zone at least 2 nodes from its outer faces (mirror planes are not outer faces);
  an event counts only if the element's current position (mirrored coordinates by absolute value) is in the fine zone at
  least 2h from its outer faces. **Labels on the z-axis line (x_q = y_q = 0) are excluded from every J statistic** (X8
  A1(d)'s axis exclusion, kept so that the axisymmetric configurations compare like with like; the same line is excluded
  for every b; reported as D-AXIS).
- **Flags.** F1 hold-law cap; F2 max x > 50; F3 a particle leaves the box; F4 the dt floor. Treated as in X8 §5.
- **Implementation.** Hot loops (residual and Hessian kernels, TSC deposit and gather, J, tridiagonal solves) in a C file
  committed with the lane and compiled locally with the system compiler; everything else numpy/scipy. float64 throughout.
  `MallocMediumZone=0`; the sampled physical footprint and ru_maxrss are reported. Checkpoint every 10 min, on SIGTERM and at
  a 27-min wall guard (exit 3); the batch driver resumes.

## 4. Checks (scripts print `ID PASS/FAIL value threshold`; exit 0 iff all PASS)

- **R-X10 (2D reproduced with X10's code).** X10's `x10_validate.py` single-mass driver, copied into this lane with
  provenance and its output redirected here (X8's `x8_core.py` imported read-only), runs D-ISO for MW, both footings,
  h ∈ {20, 10, 5}. PASS iff down_event.t (or both None), down_min.J, up_min.J, up_event.t (or both None), D_EDGE.J and
  D_STIFF.J equal X10's committed `x10_validate_results.json` D_ISO rows within 1e-9·max(1, |value|). The copy adds (output
  only) the §5a statistics over [0, W_a] (the 2D reference for X-ISO).
- **V-a1 (3D static).** M31 (1e11 M☉) at rest at the origin, box S V-a1, both footings, h ∈ {20, 15, 10}, 10 Gyr.
  PASS iff max |J − 1| ≤ 1e-4 and max displacement ≤ 1e-2 kpc over validated labels at every h (X8's line).
- **V-cm (3D Galilean).** One mass with its full switched equilibrium boosted to V (all labels; Dirichlet data follow the
  mass), MW at 68.75 and M31 at 41.25 km/s, canonical footing (X8 V-a2's footing), h ∈ {20, 15, 10}, T = 15.167 Gyr (the
  longest production window, E incl. the tail). Statistic: max over validated labels with 2ε ≤ |q| ≤ 300 kpc of |J − 1|.
  PASS iff ≤ 0.1 at h 15 and at h 10 and the h 10 value ≤ the h 15 value, in both rows (X10's rule on this ladder).
- **X-ISO (3D against 2D, the wake at matched resolution).** Case W in 3D at h = 20 and 10 against R-X10's 2D runs at the
  same h, both footings (4 rows). Row PASS iff both have a downstream event in [0, W_a] (§5a rule) with
  |t_c^3D − t_c^2D| ≤ max(0.5 Gyr, 0.1 t_c^2D) (X10's convergence tolerance reused as the agreement line) and the upstream
  minimum over the window lies on the same side of 0.5 in 2D and 3D. PASS iff all 4 rows pass.
- **X-B0 (3D against 2D, the axisymmetric encounter at matched resolution).** Case E with b = 0 in 3D at h = 20 and 10
  against X10's committed `runs/<foot>_O2_ti3_h<h>.json`, both footings (4 rows). Row PASS iff (i) both have a soft
  threshold event with |t_c^3D − t_c^2D| ≤ max(0.5 Gyr, 0.1 (t_c^2D − t_i)) and (ii) both have an MW downstream wake event
  (X10 §5b, full window) with the same tolerance. PASS iff all 4 rows pass (reported separately as X-B0(i) and X-B0(ii)).
- **N-dt, N-box, N-tol (h = 15).** One at a time: dt₀ and the 0.15 halved; B_out = 2500 kpc (the box-halving check); hold
  tol 1e-8. On two pre-declared cases: (canonical, W) and (canonical, E, b = 150). Two-branch rule (X8 A2 / X10): the
  statistic's event moves by ≤ 0.2 Gyr, or neither base nor variant has an event and the minimum moves by ≤ 0.02; for wake
  cells also the upstream minimum stays on the same side of 0.5. The checks applied: W downstream (N-a, W); E b = 150 MW
  downstream (N-a, E); E b = 150 soft (N-b).
- **MUTATE (`X12_MUTATE=1`): the boost of the wrong sign** (held labels start at −V_g; V-cm boosts −V). It must FAIL V-cm.
  Also run under MUTATE (reported, no pass weight): W at h 20 and 10 with X-ISO evaluated, and E b = 0 at h 20. Outputs keep
  `_MUTATE` in their names.

**Order of work and stop rule.** R-X10 → V-a1 → V-cm → W (h 20, 15, 10) → X-ISO → E b = 0 (h 20, 15, 10) → X-B0. If any of
R-X10, V-a1, V-cm, X-ISO or X-B0 fails, **the 3D solver is not validated against 2D: both verdicts are UNDECIDED (3D NOT
VALIDATED, naming the failed check), the b > 0 runs are not made, and the lane stops.** Otherwise: E b = 50 and 150 at
h 20, 15, 10; then the N-checks; then MUTATE.

## 5. Statistics and frozen verdicts (thresholds X8/X10; no new constant)

### 5a. Wake cells (question a)

A wake cell is (case, galaxy g, footing). For galaxy g at (x_g, 0, z_g(t)) moving with u = sign ż_g, the axis zone is the set
of elements whose current position has R⊥ = ((x − x_g)² + y²)^½ ≤ 30 kpc and lies in the validated fine zone, restricted to
**stiff, non-straddle labels** (X10 §5b). Downstream: (z − z_g)u < 0 with 2ε ≤ |z − z_g| ≤ 1000 kpc on g's outer side (away
from the other galaxy) or ≤ 0.5 d(t) on the inner side (X10; for W: 1000 kpc on both sides). Upstream: (z − z_g)u > 0, same
bounds. Over the wake window [t_i, t_i + W_a] (W: [0, 9.067]; E: [3, 12.067]):
- J_down, J_up = the minimum J over the downstream / upstream zone and samples;
- downstream event: the earliest t_c ≤ t_i + W_a at which some downstream label has J < 0.05 and keeps J < 0.05 at every
  sample in [t_c, t_c + 0.1 Gyr] (zone membership required at t_c only).

Cell class (h_mid = 15, h_fine = 10; h 20 reported for the trend):
- **PRESENT** iff downstream events at both h, J_up > 0.5 at both, |t_c(10) − t_c(15)| ≤ max(0.5 Gyr, 0.1 (t_c(10) − t_i));
- **ABSENT** iff no downstream event at either h, J_down ≥ 0.05 at both, |J_down(10) − J_down(15)| ≤ 0.05;
- **UNDECIDED** otherwise (NOT SINGLED OUT: events at both h with J_up ≤ 0.5 at either; NOT CONVERGED; BREAKDOWN FLAG if
  F1–F4 fires before any event and before the window ends).

**Verdict (a), frozen classes** (verdict cells: MW in E b = 50 and b = 150, both footings: 4 non-axisymmetric cells;
controls: W both footings and MW in E b = 0 both footings):
- **WAKE FOCUS PERSISTS IN 3D** iff R-X10, V-a1, V-cm, X-ISO, X-B0(ii) and the N-a checks PASS, both W cells are PRESENT and
  all 4 verdict cells are PRESENT.
- **WAKE FOCUS REMOVED** iff the same checks PASS and all 4 verdict cells are ABSENT (X-ISO and X-B0(ii) already require the
  axisymmetric 3D configurations to focus as in 2D).
- **UNDECIDED** otherwise, naming the failed check(s) or the cell classes (PARTIAL: n PRESENT, m ABSENT of 4).

### 5b. Soft-side folds (question b)

Per E case, X8 §5 / X10 §5a unchanged: S = minimum J over soft, validated, non-straddle labels and samples in [t_i, t_end];
threshold event = J < 0.05 at every sample in [t_c, t_c + 0.1 Gyr], t_c ≤ t_end; h_mid = 15, h_fine = 10:
- **CAUSTIC** iff events at both h with |t_c(10) − t_c(15)| ≤ max(0.5 Gyr, 0.1 (t_c(10) − t_i));
- **NO-CAUSTIC** iff no event at either h, S(10) ≥ 0.05 and |S(10) − S(15)| ≤ 0.05;
- **UNDECIDED** otherwise (NOT CONVERGED, or BREAKDOWN FLAG as in X8).

**Verdict (b), frozen classes** (verdict cases: b = 50 and 150, both footings: 4; controls: b = 0 both footings):
- **FOLDS PERSIST AT b > 0** iff R-X10, V-a1, V-cm, X-ISO, X-B0(i) and N-b PASS and all 4 verdict cases are CAUSTIC.
- **FOLDS REMOVED AT b > 0** iff the same checks PASS, both b = 0 controls are CAUSTIC and all 4 verdict cases are
  NO-CAUSTIC.
- **UNDECIDED** otherwise, naming the failed check(s) or the case classes (PARTIAL: n CAUSTIC, m NO-CAUSTIC of 4).

No case, cell or window selection after any number; footings never pooled.

## 6. Diagnostics (reported only; no verdict weight)

- **D-SV.** At every threshold event (soft, wake) the singular values σ₁ ≥ σ₂ ≥ σ₃ of ∂x/∂q of the event element at t_c and
  at its J minimum: one small singular value = a sheet fold, two small = a line focus. Also the element's position relative
  to MW (distance, R⊥ from MW's track, height y out of the encounter plane) and to the Newtonian null.
- **D-FULL.** The wake cells over the full E window [3, 18.067] (X10's window), and the soft statistic by t₀ = 13.8 Gyr.
- **D-M31.** The M31 wake cells (E, both footings, all b).
- **D-AXIS.** The excluded z-axis-line labels: minimum J (soft and stiff) and first J < 0.05 time.
- **D-HELD, D-EDGE, D-STIFF, D-FOLLOW, D-GRADED, D-SC** as X10 (held counts and radii; straddle labels' minimum J and first
  fold; stiff minimum; halo-follow ratio; soft labels outside the validated region; flags, max x, hold iterations).
- **D-20.** Whether the per-cell and per-case rules would give the same class with (h 20, h 10) as the pair.
- **D-2D.** R-X10's 2D values over [0, W_a] beside the 3D W values at h 20 and 10.

## 7. What a result can and cannot say

It answers the classical question in X10's model, now in 3D: prescribed straight-line kinematic orbits, Plummer baryons, no
Hubble flow, no other Local Group members, no discs, no dust, μ_K → 0, no back-reaction on the baryons, the X10 co-moving
start (a posed bracket), resolution 10–20 kpc (coarser than X10's 5 kpc). A PERSISTS verdict means the single-stream khronon
of v3s still folds when the axisymmetry is broken by an impact parameter in this model; a REMOVED verdict would mean the 2D
folds needed the symmetry axis. Neither says what happens after a fold (multi-stream flow, a foliation breakdown or new UV
physics), neither covers quantum strong coupling, and neither is a data comparison.

## 8. Compute

`OMP_NUM_THREADS=1 nice -n 15` (plus the single-thread BLAS variables), one thread, < 1 GB RSS per process, each process
≤ 30 min of wall time (checkpoint/resume), at most two at once, none while `compute_queue/heavyq.py status` shows low free
memory. The heavy queue and every other lane are not touched. No downloads.

## AMENDMENT A1 (POST-RESULT: written after R-X10, V-a1 and V-cm were scored; diagnostic only, no verdict weight)

**What has been seen.** R-X10 PASS (all six 2D rows bit-identical to X10's committed values) and V-a1 PASS (max |J − 1|
≤ 3.6e-11 at every h). **V-cm FAILS as frozen:** MW 0.0574 / 0.0552 (h 15 / 10) passes, but M31 gives 0.0819 / 0.0930,
both below 0.1 with h 10 > h 15. By §4's stop rule both verdicts are **UNDECIDED (3D NOT VALIDATED: V-cm)**, the W, E,
b > 0 and N-check runs are not made, and this amendment does not change that.

Seen in the V-cm time series (`runs/vcm_*_canonical_h*.json → series`): at h 10 the error stays ≈ 0.02 until t ≈ 9 Gyr
(M31) and ≈ 11 Gyr (MW), then rises to the final value; F3 fires in the three MW runs at 11.9–12.6 Gyr (boosted labels near
the outer z face leave the 5 Mpc box). A candidate mechanism, not yet tested: V-cm boosts *every* label, so labels that start
in the z-graded zone below the fine zone (spacing hq, hq², …) enter the fine zone behind the statistic region; there the
particle lattice is coarser than the grid and the deposit is lumpy. The production cases do not do this (only held labels,
all starting inside the fine z range, move), but that is an argument, not a test.

**Added diagnostics (declared before they are computed; reported in the README with no verdict weight):**
- **A1-loc.** V-cm M31, canonical, h 15 and h 10, the frozen box, rerun with the label and current position of the
  maximum |J − 1| recorded at each 0.25 Gyr series point (the run must reproduce the frozen numbers exactly).
- **A1-box.** V-cm MW and M31, canonical, h 15 and h 10, with the fine z range extended so that no label from outside it
  comes within 300 kpc of the statistic region during the run: M31 z ∈ [−600, 1260], MW z ∈ [−660, 1680] kpc (x, y, q,
  B_out, statistic and pass line unchanged). Reading: if both masses then give ≤ 0.1 with h 10 ≤ h 15, the frozen failure
  is a property of the V-cm test box (graded-zone labels entering the fine zone), not of the solver in the configurations
  production would use; if not, it is a property of the 3D solver at these resolutions.
- **MUTATE** (§4) is run as frozen on the frozen V-cm box (h 15 and 10, MW and M31) so that the check's discriminating power
  is on record.

Either way the frozen verdicts stay UNDECIDED; a production run would need a new frozen lane (successor) with its own
V-cm box fixed before any production number.

## AMENDMENT A2 (POST-RESULT: written after A1's runs; diagnostic only, no verdict weight)

**What A1 showed.** A1-loc reruns reproduce the frozen V-cm numbers exactly. A1-box (≥ 300 kpc margin from graded-zone
labels) changes nothing material: M31 0.0818 / 0.0929, MW 0.0569 / 0.0529 (h 15 / 10). So A1's candidate mechanism is
**refuted**: the failure is not the test box. The maximum sits on labels 40–60 kpc from the mass (just outside 2ε), mostly on
a mirror plane (x = 0 or y = 0) at h 10 and on the diagonal at h 15, and at h 10 it rises from ≈ 0.02 (t < 9 Gyr) to 0.093 at
the end. The frozen verdicts stay UNDECIDED.

**Added diagnostics (declared before they are computed):**
- **A2-mir.** V-cm M31, canonical, h 10, frozen z range, but the **full domain** in x and y (fine x, y ∈ [−240, 240], graded
  on both sides; no mirror plane). Reading: if max |J − 1| falls below the frozen h 15 value (0.0819), the mirror planes
  drive the h 10 growth.
- **A2-dt.** V-cm M31, canonical, h 10, frozen box, dt₀ and the 0.15 factor halved. Reading: if the late growth disappears
  (max |J − 1| below 0.0819), the time step drives it.
Neither changes any frozen number or verdict.
