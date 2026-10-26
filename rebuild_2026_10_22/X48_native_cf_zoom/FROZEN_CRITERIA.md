# X48_native_cf_zoom — FROZEN CRITERIA (committed before any production number; smoke tests are engineering only)

**Question.** X43's rule, Σ_core = max(a₀/(2πG), η(c_f) Σ_coll), needs the formation concentration c_f. It currently
borrows c_f = 4, and the data pin c_f at 4–4.2. Analytic routes fail: X44 (infall timing) gives 1.85, and X45 (peaks plus
spherical collapse) gives none. This lane measures c_f in a collisionless simulation on the record's own background and P(k).

**What the c_f represents (owner/coordinator caution).** The simulation is collisionless dust under Newtonian gravity, with
the background Λ term, on background A (EM1's CLASS refit). That is route E's cold dark energy **without** the a₀ floor
(which binds only below ~10¹² M☉), and **not v3s dynamics**. The measured c_f is c_f for that dynamics.

Standing rules: κ = ½ FITTED. Footings never pooled (the regrade runs both). Cold dark energy is not matter. No ΛCDM
concentration relation. Not "theory closed". Nothing here may say the data favour the framework.

## 1. The runs (`x48_zoom.py`, preemptible per JOB_CONTRACT)

- **Initial conditions.** A Hoffman–Ribak constrained Gaussian field on a periodic grid of side 4 q_M, ng = 38. The
  centre's Gaussian-smoothed height ν and Laplacian −x̄σ₂ are constrained, with x̄ = ⟨x|ν⟩ from BBKS. ν is set so that the
  mean constrained field's enclosed mean inside q_M equals δ_c / D(z_f), where z_f is the Lacey–Cole median formation
  epoch of M (X45 A1's normalisation).
- **Particles.** One per lattice point inside 1.5 q_M (N ≈ 12 150), each carrying one cell of mean density. Zel'dovich
  positions and velocities at z_i = 40, growing mode, f = Ω_m^0.55.
- **Dynamics.** Physical coordinates, an isolated sphere, softened direct summation (Plummer, ε = 0.01 r_f), plus the
  background Λ acceleration. KDK leapfrog with a global adaptive step, dt = 0.2 √(ε/|a|_max), integrated to t(z_f).
- **Grid.** M ∈ {10¹², 10¹³, 10¹⁴} M☉ × seeds {1, 2, 3}: nine runs.
- **Resolution check.** One run at ng = 48 (N ≈ 24 400): M = 10¹⁴, seed 1.
- **Preemption.** Proven on a small size before queueing: SIGTERM → checkpoint → exit 75, and `--resume` is bit-identical
  to an uninterrupted run (smoke log kept).

## 2. The measurement (`x48_analyze.py`, frozen now)

- **Centre:** shrinking spheres from the centre of mass (radius × 0.8 per step), stopping when fewer than 100 particles
  remain.
- **r_vir:** the radius where the mean enclosed density equals 18π² ρ_m(z_f) (physical).
- **Profile:** 24 log bins between r_conv and r_vir, where r_conv = max(3ε, the radius enclosing 200 particles).
  ρ is taken from shell counts. The log slope s(r) uses central differences on the 3-bin running mean of ln ρ.
- **r₋₂:** the first radius going outward where s crosses −2, interpolated in ln r. **c_f = r_vir / r₋₂.** If there is no
  crossing in the converged range, the run is flagged and excluded.
- **Per mass:** c_f(M) = the median over the seeds with a crossing. If fewer than 2 seeds have one, the mass is UNMEASURED.
- **Reported:** an NFW-form one-parameter fit of M(<r) on the same range (the profile form only, no c–M relation), the
  number of particles inside r₋₂, and the resolution-check difference.

## 3. Verdict

- **NATIVE c_f IN WINDOW** if the median c_f at 10¹³ and 10¹⁴ lies in [3.3, 4.6]. That is the window the data pin, from
  X44 and X42's cluster-only calibration.
- **NATIVE c_f BELOW / ABOVE WINDOW** otherwise.
- **UNRESOLVED** if the ng = 48 check changes c_f at 10¹⁴ by more than 20 %, or if any mass is UNMEASURED.
- **Regrade (always run when measured):** X43's script with η(M) = (4/(3B(1))) c_f(M)^{5/4}, interpolated in lg M between
  the measured masses and held flat outside them. The X43 verdict rule applies; the label is NATIVE-CC PASSES / FAILS.

## 4. Checks

- **K0:** the constraint residuals c1, c2 < 1e-10 in every run.
- **K1:** mass is conserved: N × m equals the sphere's mean-density mass (exact by construction).
- **K2:** in every run, momentum drift |Σ m v| / (N m v_rms) < 1e-6 at the end.
- **K3:** the analysis on a synthetic NFW particle sphere (c = 4, N = 12 000, seed 1) recovers c within 15 %.
- **MUTATE (analysis):** the synthetic sphere drawn with c = 8; K3's c = 4 recovery must fail.

## AMENDMENT A1 (2026-10-26; committed alone, after the ng 38 batch, before any ng 48 production number)

The ng 38 batch is UNRESOLVED under §3 (10¹⁴ seed 1: c_f 12.68 → 2.59 at ng 48). This amendment adds an ng 48 grid. It
changes no measurement rule.

- **Runs.** The remaining eight (M, seed) pairs at ng = 48 (N ≈ 24 400), with the same IC, dynamics and integrator as §1.
  Together with the existing 10¹⁴ seed 1 ng 48 run, that gives nine. All run through `compute_queue` (preemptible, one thread).
- **Measurement.** §2 is unchanged and applied to the ng 48 snapshots (`x48_analyze.py`, no code change except to select ng).
- **Verdict.** The §3 window [3.3, 4.6] and the median/UNMEASURED rules are unchanged, with the medians taken at ng 48. The ng 38
  medians are kept as run, and are not graded again.
- **Convergence caveat.** No ng > 48 check is in budget. Whatever the class, it is labelled "at ng 48; convergence beyond ng 48
  not tested". For every pair, the ng 38 → ng 48 shift in c_f is reported. The NFW-form fit stays reported only.
- **Regrade.** The §3 regrade is run on the ng 48 c_f(M), and labelled as above.

κ = ½ FITTED. Not theory closed.
