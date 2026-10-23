# W1_pmedium_3d_scaleup: does the 3D P-medium core peak converge, and is it bound? FROZEN CRITERIA

Written and committed before the lane's engine exists and before any lane number. Rules: `rebuild_2026_10_22/BRIEF.md`
(rules 1, 2, 4, 6 apply; rule 5's compute line is replaced, for this lane only, by the coordinator's instruction: runs
of at most 10 min and < 2 GB run directly with `OMP_NUM_THREADS=1 nice -n 15`; anything longer goes through
`compute_queue/` under `compute_queue/JOB_CONTRACT.md`, and this lane never enqueues itself). κ = ½ is FITTED. a₀ enters
this lane only through the unit system (t₀ = √(ℓ₀/a₀), M₀ = a₀ℓ₀²/G), so every ladder number is produced on both footings,
canonical a₀ = 9.3603e-11 m/s² and alt a₀ = 1.1312e-10 m/s², and never pooled. No dark-matter particle. Never "theory
closed"; nothing here says the data favour the framework (no data are used). The assumption ledger is
`ASSUMPTION_LEDGER.md` (committed with this file).

## 0. Request, what was read, not-blind statement

Request (coordinator, paraphrased): reproduce the parallel lane `sol61_push/spatial_expansion_2026_10_23/` (SE-20261023)
exactly; port its discretized action to a faster, preemptible engine gated against its code at 8³/12³/16³ with a MUTATE
that breaks the gate; run weak (.001) and strong (.03) seeds at 32³, 64³ and, if the footprint allows, 128³ with the same
initial-state prescription; measure the strong-seed peak δ_c(z = 10) and the core mass in a fixed physical aperture; give a
convergence verdict and an isolated binding certificate under a frozen reading rule; queue long runs (ENQUEUE block only).
**Nothing in `sol61_push/` is edited, moved or deleted.** Files needed are copied into this lane with sha256 provenance.

Read before freezing: SE-20261023 `HANDOFF.md`, `DERIVATION.md`, `RESULT.md`, `AUDIT.md`, `CONTRACT.md`, `SOURCES.md`,
`CHECKPOINT.sha256` (all entries verified OK), `model.py`, `run.py`, `run_v2.py`, `check.py`, `force_check.py`,
`summarize.py`, every run `manifest.json`, `check/`, `force/`, `summary/result.json`; the inherited
`sol61_push/fragment_radiation_2026_10_22/model.py` (sha256 1c4b10bb…7e83a62eb2b4ffc519627082, the TSC/lattice operators);
`sol61_push/radiating_collapse_2026_10_22/CONTRACT.md` line 8 and `RESULT.md` line 9 (unit system: ℓ₀ = .4404221297174536
kpc, a₀ = 9.3603e-11 m/s², canonical fitted mass .0840813 M₀); `compute_queue/JOB_CONTRACT.md`, `compute_queue/README.md`;
`rebuild_2026_10_22/V1_density_screen/FROZEN_CRITERIA.md` (format; footing values).

**Not blind.** I have read SE-20261023's recorded numbers (they are the reproduction targets): z = 10 peak cold contrast
.03679 / .03736 (weak 8³/12³), 2.000 / 2.763 / 3.270 (strong 8³/12³/16³), max work residual 1.46e-4, step counts 1712 /
2275 / 2874, the check values (mass 3.33e-16, expansion partial 4.83e-11, tangents 6.54e-7 / 1.26e-5, null force 5.17e-26,
force-step table). One plumbing test was run in scratch (not a lane number): NumPy 1.26.2's `np.sum(a, axis=1)` on an
(N, 27, 3) array accumulates sequentially over the 27 stencil entries, so a C gather in that order can be bit-identical.
Expectation, stated so it cannot steer anything: a cell-maximum δ_c of a collapsing peak rises with resolution by
construction (the cell shrinks), so I expect the cell-peak statistic not to converge and the aperture mass to converge
better; I have no expectation for the sign or stability of the binding energy. No threshold below was chosen after seeing
any lane number.

## 1. Reproduction (R): run their code, unchanged, at their sizes and seeds

- Copy, byte for byte, `model.py`, `run_v2.py`, `check.py`, `force_check.py`, `summarize.py`, `CONTRACT.md` of SE-20261023
  to `repro/spatial_expansion_2026_10_23/` and the parent `fragment_radiation_2026_10_22/model.py` to
  `repro/fragment_radiation_2026_10_22/model.py` (the relative import `parents[1]/fragment_radiation_2026_10_22/model.py`
  then resolves inside this lane). `PROVENANCE.json` records the sha256 of every source file read and of every copy; the
  copies must hash equal to the sources.
- Interpreter: `/usr/bin/python3` (Python 3.9.6, NumPy 1.26.2, SciPy 1.11.4), the environment their manifests record.
- Runs, with their exact command lines: base (8³, .001), space (12³, .001), time (8³, .001, cfl .3), strong (8³, .03),
  strong_space (12³, .03), strong_fine (16³, .03), strong_time (8³, .03, cfl .3), early (8³, amp .0005002271694684235,
  z_i 2200), earlier (8³, amp .0002501704158145876, z_i 4400); then `check.py`, `force_check.py`, `summarize.py`.
- **R-PASS** iff every reproduced `result.json` is byte-identical (sha256) to the recorded one. **R-PASS (numeric)** iff not
  byte-identical but every numeric leaf (rows, residuals, final positions and momenta, checks, gates) agrees to relative
  1e-9 (absolute floor 1e-15 × the leaf's largest magnitude in its array) and every integer and boolean leaf is equal.
  **R-FAIL** otherwise: then the lane stops, reports why, and makes no port or ladder claim.

## 2. Port (P): engine and gate

Engine `engine/pmedium3d.py` + `engine/tsc_kernels.c` implements the same discretized action and integrator as
SE-20261023 `model.py` (Model, fields, evaluate, evolve), with only these changes, each of which must leave arithmetic
unchanged or be covered by the gate:
1. TSC deposition and the TSC force gather run in C (compiled with `-O2 -ffp-contract=off`, no fast-math), with the same
   weight formulas, the same particle-major and 27-offset order of accumulation as `np.bincount`, and the same sequential
   27-term sum as `np.sum(axis=1)`. Threads: deposition splits the grid into x-slabs (each cell still accumulates in particle
   order), the gather splits particles; both are independent of the thread count by construction.
2. The second `evaluate` per step in SE-20261023 (`state`, same positions and fields as `mid`) is not repeated: forces are
   computed once, and the energy, work and diagnostics are evaluated with the fully kicked momenta, exactly as `state`.
3. Checkpoint/resume (§2.4), atomic writes, extra diagnostics (§4, §6) at snapshot times, and a footing switch (§3).
   Diagnostics read the state; they never feed back into it.

FFT, field operators, minimizer, drift integrals, timestep rule, guards and diagnostic rows stay NumPy/SciPy code identical
in expression order to SE-20261023.

**2.1 Gate G-P1 (trajectory equivalence).** Configurations: canonical footing, z_i 1100, z_end 10, cfl .6, n ∈ {8, 12, 16},
amp ∈ {.001, .03} (six runs). The engine (threads 1, and threads 4 for the three strong runs) and SE-20261023 `evolve`
(imported from the `repro/` copy, same interpreter, same process) are compared:
(a) equal step count and stop reason;
(b) final cold positions: max |Δx| ≤ 1e-9 dx (dx the comoving cell); final cold momenta: max |Δπ| ≤ 1e-9 max|π|;
(c) every diagnostic row: equal `step`, `max_members`, `groups_ge32`; relative difference ≤ 1e-9 in `z`,
`contrast_c_max`, `contrast_b_max`, `rms_c`, `Pmax`, `chi_min`, `chi_max`, `cell_kpc`, `core_radius_cells`; |Δ energy| ≤
1e-9 × `energy_scale`; |Δ work_error| ≤ 1e-9;
(d) |Δ max_work_error| ≤ 1e-9; initial residuals relative difference ≤ 1e-9.
**G-P1 PASS** iff (a)–(d) hold for all runs; the README states whether the agreement is bit-identical.

**2.2 MUTATE G-P2.** `--mutate drop_h_cold` removes the medium force h from the cold-particle force (cold particles feel Φ
only). Running G-P1 with the mutated engine at n = 8 (both amps) must FAIL (b) or (c). If it passes, the gate is void and
reported as such.

**2.3 Thread and resume equivalence G-P3.** At 16³ strong canonical: (i) threads 1 vs threads 4 give bit-identical final
state arrays and rows; (ii) a run sent SIGTERM near mid-run exits 75 after writing a checkpoint, and `--resume` completes it;
its final state `.npz` arrays and its result rows (excluding wall-clock fields) are bit-identical to the uninterrupted run;
(iii) `--resume` on a completed run exits 0 at once without changing its outputs. The same three are repeated at 32³ strong
canonical before any 64³/128³ job is listed for the queue.

**2.4 Job contract.** SIGTERM/SIGINT set a flag; at the next step boundary the engine writes a checkpoint (tmp file, flush,
fsync, `os.replace`) and exits 75. Rolling checkpoints every 600 s of wall time. `--resume`: exit 0 if the result is
complete; else continue from the newest complete checkpoint; else start fresh. Every output (result JSON, final-state
`.npz`, checkpoint) is written atomically and named by job (n, amp, footing, mode); mutation writes separate outputs.
Footprint is measured (`/usr/bin/time -l` peak memory footprint) at 32³ and 64³ and scaled linearly in n³ (plus the
measured constant) for 128³; `--est-gb` = 1.2 × the scaled peak; threads ≤ 8; priority 250–259; `--done-file` = the
result JSON.

## 3. Ladder (L)

- Seeds: amp ∈ {.001, .03}; resolutions n ∈ {32, 64, 128} (particles per species = cells = n³); both footings; z_i 1100,
  z_end 10, cfl .6. Alt-footing runs also at n ∈ {8, 12, 16} (the canonical 8/12/16 runs are the gate runs), so that each
  footing has its own complete ladder.
- Alt footing: ℓ₀ fixed; t₀ → t₀ √(9.3603e-11 / 1.1312e-10); M₀ → M₀ × 1.1312e-10 / 9.3603e-11; everything else
  identical (H₀ 67.4, Ω_m .315, f_b = 1/6.364, nominal mass label 1.0952264e7 M☉ that sets the box, reference radius
  .3214846542759978 kpc, η, α, b, d). The canonical footing uses SE-20261023's literal constants.
- Initial state: SE-20261023's instantaneous minimum (L-BFGS-B, ftol 1e-14, gtol 1e-9, Helmholtz start), tangent velocities
  with ε = 1e-4. `maxiter` = 1000 for n ≤ 16 (identical to theirs) and 20000 for n ≥ 32 (solver budget only; the minimizer
  is the same mathematical object). Its residual gate is theirs: < 1e-5. A run failing it is reported INIT-FAIL and is not
  used for any verdict until a fix-forward amendment.
- Direct runs: every n ≤ 32 run; a 64³ run only if a cost probe (the 64³ initial state plus 200 steps at one thread,
  extrapolated to the full step count of the timestep rule) projects ≤ 10 min and its footprint is < 2 GB; everything else
  goes to the ENQUEUE block.

## 4. Measurements (at z = 10 unless stated)

- **Peak δ_c**: SE-20261023's `contrast_c_max` (maximum over cells of the TSC cold contrast) in the final row.
- **Centre**: start at the centre of the first cell (C order) of maximum TSC cold density; iterate x_c ← x_c + mean of the
  minimum-image offsets of the cold particles within R₁ = 1.44 kpc (physical) of x_c, until the shift is < 1e-10 dx or 50
  iterations. The same centre is used for every aperture at that snapshot.
- **Apertures** (fixed physical radii): R ∈ {0.3214846542759978, 1.44, 2.88} kpc. Report M_c(<R), M_b(<R) in M☉ (footing's
  M₀) and δ_ap = M_c(<R)/(ρ̄_c 4πR³/3) − 1. An aperture is **resolved** at a grid iff R ≥ 4 physical cells there at z = 10
  (R = 2.88 kpc: n ≥ 32; R = 1.44 kpc: n ≥ 64; R = 0.3215 kpc: n ≥ 287, i.e. never in this lane).

## 5. Convergence rule (per seed, per footing, never pooled)

For a quantity Q measured on the ladder, let n₁ < n₂ be the two finest grids completed (a grid counts as completed only
with R-PASS/G-P1 PASS in force and its own checks passing: endpoint reached, initial residual < 1e-5, max work residual <
1e-2).
- Peak δ_c: **CONVERGED** iff |Q(n₂)/Q(n₁) − 1| ≤ 0.05 (SE-20261023's own 5% spatial-peak criterion); else **NOT
  CONVERGED**.
- Aperture mass M_c(<R): **CONVERGED** iff R is resolved at n₁ and |Q(n₂)/Q(n₁) − 1| ≤ 0.05; **NOT CONVERGED** iff R is
  resolved at n₁ and the change exceeds 0.05; **UNRESOLVED** if R is not resolved at n₁.
- With three grids n₀ < n₁ < n₂, the observed order p = log₂(|Q₁ − Q₀| / |Q₂ − Q₁|) (for ratio-2 steps) is reported as a
  diagnostic only.
- Every verdict carries **PROVISIONAL** while the 128³ runs of that seed and footing are queued and not completed.

## 6. Binding certificate (isolated matter-plus-field energy of the core region)

At snapshot targets ln A_k = ln A_end − 1 + 0.1 k, k = 0 … 10 (the first step boundary at or after each target; k = 10 is the
final state), for apertures R = 1.44 and 2.88 kpc about the §4 centre:
- K = Σ ½ m_i |u_i − u_cm|², over cold and baryon particles within R, with physical velocity
  u_i = H A Δx_i + π_i/A (Δx_i the minimum-image comoving offset from the centre, π = A² ẋ) and u_cm the mass-weighted mean.
- U = −Σ_{i<j} m_i m_j / √(A²|Δx_ij|² + ε²), G = 1 in code units, ε = A dx (one physical cell), full particle masses
  (isolated: no periodic images, no background subtraction).
- E_field = Σ over cells whose centres lie within R of: ½vol(ηQ² + bV²)/A³ + A³vol W(|P|) + ½αA³vol(χ−1)² +
  ½dA³vol|∇χ/A|² + ½A³vol e h (SE-20261023's energy densities; staggered P, Q components are attributed to their cell index).
  All five are non-negative perturbation energies about the homogeneous vacuum P = 0, χ = 1, h = 0.
- **E_iso = K + U + E_field.** Diagnostics reported, not gating: the virial ratio 2K/|U|; the matter-only K + U; a cold-only
  version; the Hamiltonian-form region energy E_H(R) = T_m + T_f + U_g + U_W + U_χ + U_∇ + U_e restricted to the region
  (U_g(R) = ½A³vol Σ_cells δρΦ, peculiar T_m) and its region expansion work W_A(R) (SE-20261023's formula restricted),
  with the trapezoid ∫W_A(R) d ln A over the window, so that E_H(R) − ∫W_A d ln A can be read against the region's flux
  (the region is open, so no balance is expected).

**Reading rule.** At one grid, for one aperture: NEGATIVE iff E_iso < 0 at all 11 snapshots; STABLE iff
max_k |E_iso,k − E_iso,10| ≤ 0.25 |E_iso,10|; **BOUND at that grid** iff NEGATIVE ∧ STABLE ∧ the aperture is resolved
(§4). Per seed and footing:
- **BOUND-CERTIFIED** iff BOUND at both of the two finest completed grids at which the aperture is resolved and their
  E_iso,10 agree to 25%;
- **NOT CERTIFIED** iff NEGATIVE or STABLE fails at the finest completed grid at which the aperture is resolved;
- **UNDECIDED** otherwise (e.g. one resolved grid only, or the finest two disagree).
Primary aperture: 1.44 kpc where resolved (n ≥ 64); 2.88 kpc otherwise. Both are always reported.

**Certificate self-test C-S1.** The unperturbed lattice (amp = 0) with pure Hubble flow at A = 1, n = 32, aperture of
comoving radius box/4: EdS is critical, so a uniform Hubble sphere has K + U = 0 analytically; PASS iff |K + U| ≤ 0.10 K
(lattice discreteness and softening). **MUTATE C-S1m:** dropping the Hubble term from u_i must FAIL C-S1.

## 7. What this lane does not do

No new parameter, no change to η, α, b, d, the seeds, z_i, the box, the timestep rule or the guards; no knob scan; no data
comparison; no population or mass-function claim; a peak or a BOUND verdict is a statement about this discretized reduced
action with this quiet seed in an imposed EdS box, not about dwarf galaxies or observations. Amendments are fix-forward,
committed before the numbers they affect, and leave this file's lines unchanged.
