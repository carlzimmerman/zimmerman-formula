# CQ6_past_first_caustic: FROZEN CRITERIA (committed alone, before any script or number)

κ = ½ FITTED; not theory closed. Launched 2026-11-04 on the owner's go for action-building lanes. Not blind: the author made
the homology estimate in section 2 before freezing. Adopts nothing. No particle; the cold sector stays retired and is not
revived. No data are used, so nothing here can say the data favour the framework.

## 0. Question and record

Requirement row 12 (`rebuild_2026_10_22/REQUIREMENTS_2026-11-01/REQUIREMENTS_LIST.md`) reads "P(X) dust limit only, past the
first caustic no". **With a gradient regulator added, does a 1D collapse of v3s's dust limit go past the first caustic and
settle into a bound phantom profile, without any particle?**

Record read before freezing. No regulated post-caustic run is on record:
- AN1, AN2 (`rebuild_2026_10_22/AN1_aest_nonlinear_dust`, `AN2_aest_3d_fold`): unregulated fold lanes, NO VERDICT.
- X14 (`rebuild_2026_10_22/X14_caustic_completion`): analytic, exact only up to the first crossing; its C1 (β) term
  removes folds only in linear subsonic flow.
- BOLTZ1: the dust limit is L = P(X), K = μ²(Q−1)², μ → ∞; a single-valued φ cannot cross streams.
- AZ14–AZ17 (`astra_goal_2026_11_03/P4/`, read only): the quartic regulator's structural gates (AZ14), a conditional
  concentration bound (AZ15), no C² spherical stationary core (AZ16), and an unconverged static equilibrium (AZ17). None
  evolves a collapse past a caustic.

## 1. Equations (frozen)

- **Dust limit.** Newtonian limit of BOLTZ1's P(X) dust: an irrotational, pressureless, single-stream flow
  (continuity plus Euler; in 1D every flow is irrotational). v3s's finite-μ_K pressure is not included, since the
  question is the μ → ∞ limit; X14 found it inert at the fold scale.
- **Regulator.** AZ14's quartic perspective functional, unchanged:
  F = λ ∫ |∂ₓρ|⁴/ρ³ dx = 256 λ ∫ |∂ₓψ|⁴ dx, with ψ = ρ^¼ (AZ15's form). The equations are continuity and
  D_t v = −∂ₓ(Φ + μ), with μ = δF/δρ = λ[−3(∂ₓρ)⁴/ρ⁴ − ∂ₓ(4(∂ₓρ)³/ρ³)].
  λ > 0 is FITTED and undetermined. The regulator is a nonrelativistic functional with no covariant realization on
  record, so no outcome here completes v3s's action.
- **Geometry.** Planar 1D, periodic box of length L, static background with the background density subtracted in
  Poisson (Φ'' = 4πG(ρ − ρ̄)). Units: L = 1, ρ̄ = 1, 4πGρ̄ = 1 (τ = 1).
- **Footings.** a0 does not enter: there is no a0 in the dust limit or the regulator, and the background is Newtonian.
  Both footings (9.3603e-11 / 1.1312e-10 m/s²) give the same numbers. Nothing is pooled, because nothing depends on a0.

## 2. Discretization, initial conditions and runs

- **Lagrangian sheets.** N equal-mass sheets, m = 1/N, with Lagrangian labels q_i = −1/2 + (i + 1/2)/N.
  - Cell c lies between sheets c and c+1, periodic. Its width is Δ_c, ρ_c = m/Δ_c and ψ_c = ρ_c^¼.
  - F_d = 256 λ Σ_c (ψ_{c+1} − ψ_c)⁴ / s_c³, with s_c = (Δ_c + Δ_{c+1})/2. This is AZ17's discrete form in planar geometry.
  - Gravity is exact for ordered sheets: a_i = ψ_i − ⟨ψ⟩, with displacement ψ_i = x_i − q_i, and
    W = −(m/2) Σ (ψ_i − ⟨ψ⟩)².
  - The discrete Lagrangian is K − F_d − W.
- **Integrator.** Implicit midpoint (symplectic). Each step is solved by Newton's method with a banded Jacobian built by
  complex-step derivatives, plus a backtracking line search that keeps every Δ_c > 0.
  - A step has converged when max|δx| ≤ 1e-12 within 25 iterations.
  - On failure the step is split into 2, 4, …, 64 substeps. Failure at 64 substeps is **BLOW-UP**.
- **Initial conditions.** x_i = q_i − A sin(2π q_i), v = 0, with 2πA = 1/cosh 3. The unregulated Zel'dovich solution
  (static background: ψ = −A cosh t sin kq) first shell-crosses at q = 0 at **t_c = 3 τ exactly**.
- **Times.** The frozen crossing time is t_× ≡ 2π τ: the period of a sheet in a slab of overdensity 1. It is longer
  than the expected core period, so it is conservative.
  - Each run ends at t_end = t_c + 10 t_× = 65.832.
  - The settling window is W5 = [t_end − 5 t_×, t_end] = [34.416, 65.832].
  - Diagnostics are sampled every 0.05 τ.
- **Canonical λ = 1e-8** (box units), chosen before any run. The homology estimate (U = 3λΣ/w⁴ against the infall and
  planar binding energies) puts the regulated core at w ≈ 0.04–0.06 L. That gives ≥ 50 Lagrangian cells across the core
  on the coarsest grid. λ is tied to no galaxy.
- **Runs.**
  - Ladder: N = 256, 512, 1024 at dt = 1e-3.
  - K-dt: N = 512 at dt = 5e-4.
  - MUTATE twin (λ = 0): N = 256, 512, 1024, stopped at the first crossing.
  - Side reading S1: λ = 1e-9 at N = 512 and 1024, numbers only, no label weight.

## 3. Diagnostics

- **Energy and momentum.** E = K + F_d + W; momentum P = Σ m v; mass is exact by construction.
- **Virial ratio.** R_v = (2K + 4F_d + L·G_wrap)/W_v, with W_v = −Σ m x_i(ψ_i − ⟨ψ⟩) and G_wrap = ∂F_d/∂Δ at the wrap
  cell. This is exact: d/dt Σ m x v = 2K + 4F_d + L·G_wrap − W_v, so a static equilibrium has R_v = 1.
- **Profile.**
  - Central density ρ_c = m/Δ at the centre cell.
  - Enclosed-mass widths w_f = x(q = f/2) − x(q = −f/2) for f = 0.25, 0.5, 0.75 and 0.9. w_half = w_0.5.
  - The W5-averaged density at |x| = 0, 0.005, 0.01, 0.02, 0.03, 0.05, 0.075, 0.1, 0.15, 0.2, 0.3, 0.4 and 0.5.
- **Also reported.** min Δ_c, max |∂ₓ ln ρ|, and the number of substeps.

## 4. Lines (frozen)

- **(a) Caustic passed (per grid).** Every Δ_c stays > 0, every value stays finite, and there is no BLOW-UP through
  t_end.
- **(b) Energy (per grid).** max_t |E − E(0)| ≤ 1e-3 · max_t K. Momentum: |P| ≤ 1e-10 at every sample.
- **(c) Virial.** R_v ∈ [0.9, 1.1] at every sample in W5.
- **(d) Stable profile.** (max − min)/(2·mean) of w_half over W5 ≤ 0.10.
- **(e) Converged.** The W5 means of ρ_c, w_0.25, w_0.5, w_0.75, w_0.9 and R_v agree between N 512 and N 1024 within 5 %
  (relative to N 1024). d_fine and d_coarse are the largest such differences for the pairs (512, 1024) and (256, 512).

## 5. Controls (all must pass, else NOT EVALUABLE)

- **K-ZEL (known answer).** With λ = 0, the first crossing time on each grid is within 1 % of t_c = 3.
- **MUTATE (regulator off).** The same λ = 0 runs must fail to pass the caustic, crossing before t_end, on all three grids.
- **K-FD.** On a perturbed N = 64 test state, the analytic regulator force agrees with the complex-step gradient of F_d:
  max|diff|/max|force| ≤ 1e-8.
- **K-hom.** F_d(αΔ) = α⁻⁴ F_d(Δ) to 1e-12 relative, and Σ x_i ∂F_d/∂x_i + 4F_d + L·G_wrap = 0 to 1e-10 relative.
- **K-dt.** At N = 512, dt 5e-4 gives the same outcome for (a), passes (b), and its (e) quantities agree with dt 1e-3
  within 5 %.

## 6. Labels (in this order)

1. **NOT EVALUABLE** if any control in section 5 fails.
2. **ILL-POSED** if:
   - any regulated grid fails (a): blow-up or a regulated crossing; or
   - (e) fails while d_coarse/d_fine < 1.5, which is non-convergence.
3. **NOT EVALUABLE** if:
   - (b) fails on any grid; or
   - (e) fails while d_coarse/d_fine ≥ 1.5, which means resolution-limited.
4. **SETTLES** if (a), (b) and (e) hold and (c) and (d) hold on both N 512 and N 1024.
5. **OSCILLATES WITHOUT SETTLING** if (a), (b) and (e) hold but (c) or (d) fails on N 512 or N 1024.

The label speaks for λ = 1e-8, this amplitude and planar symmetry only. It is not a statement about 3D, about other λ,
or about a covariant completion.

## 7. Compute and files

- Compute: one thread (BLAS threads = 1), `nice -n 10`, under 1 GB. Each run checkpoints every 10,000 steps and on
  SIGTERM, and resumes from its checkpoint.
- Files:
  - `cq6.py` is the script;
  - `cq6_results.json` holds the λ = 1e-8 runs, K-dt, S1 and the K-FD/K-hom checks;
  - `cq6_results_MUTATE.json` holds the λ = 0 runs;
  - `cq6.out` is the run log;
  - `README.md` starts with the headline `# CQ6_past_first_caustic: <RESULT>`.
- Any change after this commit is a dated amendment marked PRE-RESULT or POST-RESULT.

κ = ½ FITTED; not theory closed.
