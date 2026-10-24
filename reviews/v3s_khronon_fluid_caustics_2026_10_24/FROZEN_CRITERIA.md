# v3s self-consistent khronon fluid: does the MW–M31 soft lobe shell-cross? — FROZEN CRITERIA (before any script or number)

Owner's request (2026-10-24): "build a self-consistent axisymmetric khronon-fluid solver for v3s (Lagrangian elements + the
non-local Gauss law div P(grad Xi) = rho_tau + Poisson, switch at D.P = 0) and rerun the MW-M31 caustic test, frozen
criteria first, both footings, mutate, preemptible if heavy." It decides what `reviews/v3s_soft_side_caustics_2026_10_23/`
could not: there, the frozen-field model crossed only through adiabatic halo regions where its premise failed. κ = ½ FITTED.
Canonical a₀ = 9.36e-11 and alt 1.13e-10 m/s², never pooled. No dark-matter particle. Not theory closed.

## 0. Equations (from H4 A1's Lagrangian with the v3s switch, μ_K → 0; derived by hand, re-checked in V1–V3)

Units kpc, Gyr, M☉. Khronon elements carry signed mass (ρ_τ = D·P) and move with

    Dv/Dt = ∇Ψ − ∇φ − γ_L ∇(ρ_τ)₊,
    ∇·[∇Ψ / (1 + |∇Ψ|/a₀)] = 4πG ρ_τ        (Gauss law ∇·P(A) = ρ_τ, A = ∇Ψ, P = A/(4πG(1 + |A|/a₀)))
    ∇²φ = 4πG(ρ_b + ρ_τ),                    γ_L = 2πG L★² (L★ = 24 pc).

- In equilibrium Ψ = φ, which is AQUAL with μ = x/(1+x) exactly (C4). Holding Ψ − φ_τ fixed at its t_i value gives
  the previous lane's frozen-field model.
- Expectation (hand, stated so it cannot steer): in deep MOND the khronon self-force F = A − ∇φ_τ is second order,
  ≈ f|f|/a₀. So lobe elements should behave close to the frozen model, while halo elements (x ≳ 0.2,
  ω = √(4πGρ(M−1)) ~ 2 Gyr⁻¹) respond. No expectation for the verdict.

## 1. Engine (`khronon_fluid.py`)

- Axisymmetric finite-volume grid in (R, z), z along the MW–M31 axis, origin at the barycentre. Box R ∈ [0, 2000],
  z ∈ [−2000, 2000] kpc. Spacing h = 20 kpc (main) and h = 10 kpc (convergence rung).
- Flux-form operators share one discretisation: Poisson (Laplacian factorised once), Gauss law (defect correction
  against that factorisation), and the initial AQUAL solve (Picard with refactorisation, μ floor 1e-6).
- Dirichlet boundaries, fixed in time: the deep-MOND monopole √(G M_b a₀) ln r of the t_i equilibrium. Particles
  within 3 cells of the outer boundary are frozen.
- Baryons are two Plummer spheres (MW 6e10, M31 1e11 M☉, ε = 20 kpc), sampled at cell centres and renormalised to
  their mass. Orbits **O1** (timing-argument Kepler: 780 kpc, −110 km/s, 13.8 Gyr) and **O2** (constant velocity),
  exactly as in the previous lane.
- At t_i ∈ {3, 6, 9} Gyr: AQUAL equilibrium; ρ_τ = (Lφ − 4πGρ_b)/(4πG) with the same operator; one khronon particle per
  cell at the cell centre with mass ρ_τV, at rest.
- Each step: CIC deposit, Poisson, Gauss, cell accelerations, bilinear interpolation to particles, KDK leapfrog,
  dt = 0.02 Gyr (h = 20) / 0.01 Gyr (h = 10).
- Run window t_i → t_end, where r = 300 kpc; continued to r = 150 kpc with no verdict weight.
- Shell crossing: the 3D Jacobian J = (R/R_q) det ∂(R, z)/∂(R_q, z_q) of the particle lattice (central differences)
  reaches J ≤ 0. "Soft" particles are those with ρ_τ(t_i) < 0, excluding frozen ones.
- Preemptible per `compute_queue/JOB_CONTRACT.md`: SIGTERM/SIGINT set a flag; at the next step it writes an atomic
  checkpoint and exits 75. `--resume` continues and exits 0 at once if complete. Rolling checkpoints every 50 steps.
  Runs are direct (one thread, nice 15) while each stays under ~10 min and 1 GB; anything longer goes to the queue.
- Modes: `--mutate` (masses frozen at r(t_i)); `--frozen-F` (F = A − ∇φ_τ held at its t_i field).

## 2. Checks

- **V1 (Gauss law vs analytic, h = 20 and 10).** A Plummer-profile khronon charge, Q(<r) = Q r³/(r² + b²)^(3/2) with
  b = 200 kpc, G Q chosen so max |f| = 0.5 a₀ (strongly nonlinear), both signs, centred on the axis, analytic Dirichlet
  boundary. A = f/(1 − |f|/a₀). PASS iff the max relative error of |∇Ψ| over 2h ≤ r ≤ 1500 kpc is ≤ 3 % at h = 20, and
  error(20)/error(10) ≥ 2.5.
- **V2 (Poisson, h = 20).** Plummer baryon sphere: |∇φ| within 2 % of analytic for r ≥ 3ε.
- **V3 (equilibrium at t_i).** Interior max |acceleration| ≤ 1e-6 × max |∇φ| at every (footing, orbit, t_i).
- **V4 (resume equivalence).** A 40-step segment with SIGTERM after step 17 and `--resume` gives particle positions
  bit-identical to the uninterrupted segment.
- **V5 (MUTATE, static masses, all 12 cases at h = 20).** Max displacement ≤ 1e-3 h and |J − 1| ≤ 1e-3 over the window.
- **V6 (frozen-F mode vs the previous lane).** At h = 20, canonical, O2, t_i ∈ {3, 6, 9}: frozen-F mode crosses, with
  t_sc within ±1 Gyr of the previous lane's 14.44 / 15.43 / 16.44 Gyr (grid forces vs analytic ones).
- **C (verdict, self-consistent mode, both footings, O1 and O2, t_i 3/6/9, h = 20; rung h = 10 for the two cases per
  footing with the smallest soft min J, and for every case that crosses at h = 20).**
  - **SELF-CONSISTENT SHELL CROSSING** iff some case reaches soft J ≤ 0 by t_end at h = 20 *and* its h = 10 run also
    crosses, with t_sc within ±1 Gyr.
  - **NO SHELL CROSSING** iff soft min J > 0.5 in every h = 20 case and every h = 10 rung case.
  - **UNDECIDED** otherwise, with the cases named.
  - Reported with every case: soft min J and when it occurs; the halo response (positive khronon mass within 100 kpc of
    each galaxy at t_end ÷ t_i, and how far the halo's mass centroid follows its galaxy); the frozen-F mode's min J for
    the same case where it was run.

Not tested: stiff-side structure below the grid (L★ ≪ h; γ_L is included but inert at h), non-axisymmetric motions,
the Hubble flow and other Local Group members, a time-dependent outer boundary, BS dust (μ_K → 0), the DBI K.

## AMENDMENT A1 (after the solver tests, BEFORE any production run; `kf_tests.out`)

- **Engine setting changed before any production number:** Gauss-law tolerance 1e-11 → 1e-13 of max |source|. In a 20-step
  smoke test the equilibrium residual was 1.6e-6 relative, at M31's axis core cell; AQUAL had converged to 6.8e-13. The
  V3 threshold (1e-6) is unchanged.
- **V1 FAIL as frozen.** Max error 1.96 % at h = 20 (≤ 3 % ✓), but error(20)/error(10) = 1.88 < 2.5. Diagnosis (scratch,
  disclosed): the worst error is always at the smallest included radius, next to the axis (r ≈ 2.1h), a region that moves
  inward with h. At fixed physical location the scheme converges at second order: the potential error goes
  3.94e-3 → 9.93e-4 → 2.48e-4 (h 20/10/5, ratio 4.0), and the median gradient error 1.07e-3 → 2.7e-4 → 7e-5. The frozen
  metric was badly designed (resolution-dependent region); it stays FAIL.
- **V2 FAIL as frozen.** 11.2 % at h = 20, at the axis cell 70 kpc from a Plummer core that is one cell wide (ε = h;
  sampled M(<60 kpc) is 1.034× analytic). It converges at second order: 2.97 % (h = 10), 0.76 % (h = 5); away from the
  axis 6.4 / 2.0 / 0.61 %.
- **Consequence, stated before production:** soft-lobe forces (200–400 kpc from the galaxies) are accurate to < 1 % at
  h = 20, while halo forces within ~100 kpc of a galaxy carry 5–10 % errors at h = 20 and 2–3 % at h = 10. The frozen
  verdict already requires h = 10 confirmation. **Added now:** if the h = 20 and h = 10 readings of a rung case differ,
  that case is also run at h = 5 (dt 0.005; through the compute queue if over ~10 min), and h = 10/5 decide it.
- V4 PASS (yield exit 75, resume, idempotent re-resume, bit-identical positions).

## AMENDMENT A2 (owner request 2026-10-24, after the main result; PRE-RESULT for O1 at h = 10 and h = 5)

Owner: "run the timing orbit O1 (all t_i, both footings) at h = 10, and h = 5 for its lowest-J case via the queue if heavy,
and report whether O1 stays crossing-free." Same engine (`khronon_fluid.py`, unchanged), self-consistent mode, window to
r = 300 kpc (extended to 150 kpc, no verdict weight). h = 10: dt 0.01 Gyr, all 6 O1 cases. h = 5: dt 0.005 Gyr, the O1
case with the lowest soft min J at h = 10 (ties → canonical), one run per footing; through `compute_queue` if a timing
probe projects more than ~15 min. **Reading:** O1 CROSSING-FREE iff soft min J > 0 by t_end in all six h = 10 runs and in
the h = 5 run(s); O1 CROSSES if any of them reaches J ≤ 0 by t_end (report t_sc, distance to a galaxy, and whether h = 10
and h = 5 agree within ±1 Gyr). Also reported: min J trend with h (20 → 10 → 5). No expectation fixed.
