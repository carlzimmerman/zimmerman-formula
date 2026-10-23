# X1_seedfree_abundance: evolve the high-H quantum state through bath formation and compute the cold abundance with no seed. FROZEN CRITERIA

Written and committed before any lane script exists and before any lane number. Rules: `rebuild_2026_10_22/BRIEF.md`,
`doors_push_2026_10_22/BRIEF.md` (+ `BRIEF_E_AUDIT.md`). κ = ½ is FITTED (it does not enter this lane). No dark-matter
particle is added: the fields are the record's scalar carrier (Φ, X) of the cold-energy sector, unchanged. Never
"theory closed"; nothing here says the data favour the framework. The assumption ledger is `ASSUMPTION_LEDGER.md`,
committed with this file. Later changes are append-only AMENDMENT sections marked PRE-RESULT or POST-RESULT.

## 0. Request, what was read, and the not-blind statement

Owner's request (verbatim): "Find a scalable way to evolve the actual high-H quantum state through bath formation,
retaining coherence and non-Gaussian correlations. Include reactions and inverses and calculate the cold abundance
without assuming a seed."

Read before freezing (read-only, never edited): `sol61_push/mechanism_reassessment_2026_10_22/`
QUANTUM_CORRELATION_CONTINUATION.md, STOCHASTIC_SOURCE_RESULT.md, NONLINEAR_QUANTUM_SOLVER_RESULT.md,
PERSISTENT_STATE_AND_OVERLAP_RESULT.md, BATH_FORMATION_REACTION_RESULT.md, EMPTY_STATE_OBSTRUCTION.md,
QUANTUM_CONVERSION_RESULT.md (4→2 amplitude, C), NONLINEAR_FRAGMENTATION_RESULT.md, LATE_CONVERSION_RESULT.md,
PRODUCTION_SPECTRUM_RESULT.md; scripts `stochastic_source.py`, `quantum_fock_solver.py`, `quantum_wavefunction.py`,
`audit_quantum_wavefunction.py`, `run_quantum_fock_benchmark.py`, `production_scalings.py`, `highH_annihilation_gate.py`;
run outputs `stochastic_source_run/results.json`, `production_scalings_run/results.json`,
`bath_assisted_conversion_run/results.json`; `compute_queue/JOB_CONTRACT.md`. Anything copied is copied into this lane
with its sha256 in `PROVENANCE.json`.

**Not blind.** Before this file, by hand only (nothing run, no lane code exists):
1. Scale ordering from the action. During inflation λ|Φ|²/H² ≈ 0.009, so Φ is light; after inflation it starts to roll
   when its quartic curvature passes H, i.e. at H ≈ √λ|Φ| ≈ 0.1 H_inf, a few H_inf⁻¹ after the end of inflation, not
   at H ~ 10 m as the lane brief assumed. X (mass M, no quartic) starts at H ≈ M, at a ≈ √(H_inf/M) ≈ 2.6e6
   (Codex also finds 2.59e6). In conformal units the cubic/quartic force ratio grows ∝ a² from ~1e-14; the
   radiation-era quartic sector is conformal (a″ = 0 kills the ξ term), so ξ enters only through the inflationary state
   and any non-radiation era.
2. Near X onset the thermal-like Hartree mass² of the Φ bath and the X-induced splitting 2g|X| are of the same order for
   this benchmark (their ratio is H_inf-independent at onset: ∝ g/(λ^{3/2}M) ≈ 1); the tachyonic window therefore opens
   near X onset, at a hierarchy √(2g|X|)/M ~ 1e5 that no lattice can resolve.
3. Codex chose H_inf = 1.3445e10 GeV so that a free X condensate gives about the target yield, so the free-condensate
   ceiling sits near 0.12 at the primary input by construction; prompt thermalization of the dark sector at X onset
   followed by cannibal freeze-out gives a far smaller yield. A light spectator (ξ = 0) gives order-one isocurvature
   (Codex: P_S ≈ 2/N_pre). I expect: the abundance at ξ = 0 is bracketed widely and decided by the X-onset epoch;
   the isocurvature gate fails at ξ = 0; ξ = 1/6 is negligible.
These estimates set no threshold below. Every reported number comes from the committed scripts.

## 1. Action, units and declared inputs

V = m²|Φ|² + M²|X|² + g(X*Φ² + XΦ*²) + λ|Φ|⁴, canonical complex fields, charges 1 and 2, m = 0.001 GeV,
M = 2m√(1+0.02²), g = 2.168e-6 GeV, λ = 0.00881292. Nothing in the action is changed, rescaled or fitted.

Inputs the action does not fix (declared, never fitted to 0.12):
- H_inf: primary 1.3445177278709404e10 GeV (Codex's value, itself chosen by a free-condensate abundance estimate; it is
  NOT an independent input and proximity of any result to 0.12 there is not a prediction).
- N_e: e-folds of light-field noise accumulation, primary 60 (Codex).
- Reheating: primary "instant" = radiation era from the end of inflation, a = 1 + H_inf η, visible g* = g*s = 106.75 at
  that time; variants T_rh with a w = 0 era from the end of inflation to H(T_rh).
- ξ (curvature coupling of both fields): primary 0, control 1/6.
- The patch: the coarse field values of our patch are one draw of the stochastic distribution; results are given for
  the median patch with the 10–90 % patch range.
- Visible-sector g*(T), g*s(T): a declared smoothed step table (ASSUMPTION_LEDGER A14).

Input map grid (frozen): H_inf ∈ {1e8, 1e9, 1e10, 1.3445e10, 1e11, 1e12, 1e13} GeV × T_rh ∈ {instant, 1e12, 1e9, 1e6} GeV
(only T_rh below the instant value) × ξ ∈ {0, 1/6}. N_e = 60 throughout, with the scaling of the ceiling closure stated
for N_e = 30 and 120.

## 2. Method (frozen): epochs, and what carries coherence and correlations through each

**E0 — inflation (stochastic + Gaussian in-box modes).**
- R0: rerun Codex's Langevin algorithm (`stochastic_source.py` logic, same seed 20261022, same 4096 patches, dN = .02/.01)
  and reproduce ⟨|Φ|²⟩/H² = 0.972195 and ⟨|X|²⟩/H² = 1.54258 (fine run).
- Box zero mode: the same Langevin drift with noise for N_e − N_box e-folds and drift only for the last
  N_box = ln(1/k_min) e-folds (k_min = 2π/L in units of a_e H_inf), seed 2026102301, dN = .01, 4096 patches. Its conformal
  velocity is the slow-roll attractor of the same drift (not zero by fiat). The global U(1) is rotated to make Φ₀ real.
- In-box modes (all lattice k ≠ 0): the de Sitter Bunch–Davies state at the end of inflation with constant-background
  effective masses m_L² = 3λf₀², m_T² = λf₀² for Φ and 0 for X (Codex's Hankel prescription), mode functions
  v_k = (√π/2)e^{iπ(ν/2+1/4)}H_ν⁽¹⁾(k), v′_k at η = −1, lattice dispersion k → k_lat. They are sampled as Wigner
  Gaussians (half-quanta included): this is the actual quantum state of the light fields, with no inserted seed, and
  it smoothly contains both the superhorizon stochastic amplitudes (k < 1) and the vacuum (k > 1).

**E1 — truncated Wigner (TW) lattice, τ = 0 → τ_h.** Conformal fields φ = aΦ/H_inf, x = aX/H_inf, conformal time
τ = H_inf η, comoving momenta in units of a_e H_inf, a = 1 + τ (instant reheating). Full nonlinear equations of the action:
- φ″ = ∇²φ − [m̂²a² − (1−6ξ)a″/a]φ − 2ĝ a x φ* − 2λ(|φ|² − 2c)φ,
- x″ = ∇²x − [M̂²a² − (1−6ξ)a″/a]x − ĝ a φ²,
  with m̂ = m/H_inf etc. The −2c term is the Weyl symbol of normal ordering with respect to the massless conformal lattice
  vacuum, c = V⁻¹Σ_{populated k≠0} 1/(2ω_k); this is the exact TW counterpart of the normal-ordered Hamiltonian used by
  Codex's Fock solver.
- 7-point Laplacian, velocity-Verlet (kick–drift–kick), dt = dx/20, periodic box L = 78.54 (k_min = 0.08).
- Coherence (the zero mode / condensate) and all connected correlations are carried by the fields themselves; every
  reaction of the action and its inverse is implicit, with classical Bose enhancement.
- Variants: TW_full (half-quanta in every k ≠ 0), TW_kc (half-quanta only for k_lat ≤ 2), CSA (populate k_lat < 1 only);
  ξ = 1/6 control (conformal vacuum state, no coarse field). Prototype N = 32, 48, 64 to τ_end = 2000; production
  N = 64 (ensemble, long), 128, 256 through the queue.

**Validation of TW against Codex's exact reduced Hamiltonians (before using E1 numbers).**
- V0: my zero-momentum Fock builder vs Codex's `Model` (with p = 1e3 so only k = 0 modes fit under the energy cut):
  Hamiltonian matrices identical to 1e-12 at energy cut 12, number cut 8, charge 2.
- V1: one-cell wavefunction (Codex's `CellWavefunction`, n = 32, length 12): (a) Codex's one-X-excitation state, TW with
  signed Wigner weights, t ∈ [0, 2]; (b) coherent Φ state with ⟨N_Φ⟩ = 1 and 2, t ∈ [0, 50].
- V2: 12-oscillator Fock model (Codex's `Model`, energy cut 12, number cut 8, V = 100): the absorption benchmark
  X⁺Φ⁺Φ⁻ → Φ⁺(±p), TW with signed product Wigner weights, t ∈ [0, 10000].
- V3 (the occupation sweep): zero-momentum four-mode Fock model (both charges of Φ and X, all normal-ordered terms of the
  action, Galerkin), exact sparse evolution vs TW, at fixed classical density ν = n/V ∈ {2, 8},
  n ∈ {1, 2, 4, 8, 16, 32}, window t ∈ [0, 500] m⁻¹. Scenario A: X coherent (neutral, linear), Φ vacuum.
  Scenario B: Φ coherent (neutral, linear), X vacuum. Observables: O1 = ⟨N_X⟩/n, O2 = ⟨N_Φ⟩/n, O3 = coherent fraction
  of the driven species |⟨a⟩|²/⟨a†a⟩ summed over charges, O4 = Var(N_X)/n and Var(N_Φ)/n, O5 = κ₄/κ₂² and
  O6 = κ₃/κ₂^{3/2} of the driven species' real quadrature. Errors: e_O(n) = max_t |O_TW − O_exact| (absolute).
  TW uses 20000 trajectories (sampling error reported). n* (the validity occupation) = the smallest n with
  max(e_O1..O4) < 0.05 and max(e_O5, e_O6) < 0.10 for both ν; n*_10 = the same with 0.10/0.20.

**Hand-over E1 → E2.** n_k from TW with the isotropic Hartree reference ω_k² = k_lat² + m_H², m_H² = 4λ(⟨|φ|²⟩ − c).
τ_h(H1) = first output time at which modes with n_k < n* carry more than half of the non-vacuum fluctuation energy AND the
Φ coherent fraction f₀ = |φ̄|²/⟨|φ|²⟩ is below 0.05; H2 = the same with one quarter. If neither is reached by τ_end, E2
starts at τ_end as a CONDITIONAL case (the residual zero-mode energy is added to the bath with energy conserved) and is
labelled so.

**E2 — momentum-resolved quantum Boltzmann, τ_h → τ_on.** Isotropic Φ± (charge-symmetric), 2↔2 elastic with
|M|² = (4λ)² for Φ⁺Φ⁺ and Φ⁺Φ⁻ (effective S|M|² = 24λ²), full Bose factors f₃f₄(1+f₁)(1+f₂) − f₁f₂(1+f₃)(1+f₄),
self-consistent Hartree mass m_H² = 4λ∫f/E, exact isotropic angular reduction (piecewise-linear D-function), number and
energy conserved by projection. X stays a homogeneous coherent zero mode (free ODE; the cubic back-reaction is a
diagnostic). Number-changing channels in E2 (X ↔ ΦΦ in-medium threshold, X + Φ + Φ̄ ↔ ΦΦ with the condensate, 2↔4) are
evaluated as rate/H diagnostics and included dynamically only if any exceeds 0.01. Overlap test: a classical-statistics
Boltzmann started from the TW spectrum at τ_end − 0.25τ_end must reproduce the TW energy spectrum at τ_end to an L1
relative difference < 0.15 on the populated band. Hand-over sensitivity: E2 outputs at τ_on (m_H²/T_eff², number relative to
thermal at equal energy, the tachyonic-window ratio r = 2ĝa²|X̂₀|/m_H²) from H1 vs H2 (or two start times if CONDITIONAL).

**E3 — X onset (τ_on: H = M).** The coherent X–bath dynamics at the physical hierarchy cannot be resolved; three frozen
closures, each fed into E4 identically:
- L (prompt): at τ_on all dark energy (X condensate + Φ bath) thermalizes with μ = 0. Earliest possible dark
  thermalization (X is frozen by Hubble friction before τ_on).
- K (kinetic): the X condensate is a population of X quanta at rest (n_X = ρ_X/M by the free-X adiabatic invariant)
  interacting only through the perturbative reactions of E4 with in-medium kinematic blocking; the Φ bath from E2.
- C (ceiling): the X condensate never interacts; Y_C = 2n_X/s + the Φ bath's own E4 relic.
The dissipation actually realised in E3 is NOT computed here; if 0.12 lies inside [Ω_L, Ω_C] the verdict at that input
is UNDETERMINED, never "consistent".

**E4 — freeze-out network.** Dark sector in kinetic equilibrium (BE thermodynamics, Hartree Φ mass), energy conserved,
reactions with Δ(N_Φ, N_X): r1 X ↔ ΦΦ (+2, −1), vacuum width g²β/(8πM), in-medium β_eff; r2 XX̄ ↔ ΦΦ̄ (+2, −2),
σv = √(1−m²/M²)g⁴/(2πM⁶) (Codex threshold); r3 XΦΦ̄ ↔ ΦΦ (0, −1), Codex's D(T) table (MB, T/m = 0.01–2; D₀ below);
r4 4→2 (−2, 0), C = 1.0181045670e14 GeV⁻⁸; inverses by detailed balance with the chemical potentials. The crossed channel
XΦ̄Φ̄ → ΦΦ̄ has an uncomputed RIS-subtracted kernel: primary ×0, sensitivity ×1 of D, stated as uncomputed. For
T_d > m/3 chemical equilibrium (μ = 0) is imposed when C n³/H > 100. Output: Y = (n_Φ + 2n_X)/s at T_vis = 1 MeV
after freeze-out, Ω_c h² = 2.744e5 · Y · (m/1e-3 GeV).

**Isocurvature.** P_S = Σ_fields (∂ln Y/∂ln|F|)²(H_inf/2π)²/(f₁² + f₂²)|_canonical, with ∂ln Y/∂ln|F| from the closure
chain by ±1 % finite differences at the median patch; gate P_S < 8.3e-11 (β_iso < 0.038, P_R = 2.1e-9, uncorrelated).

**ξ = 1/6 control.** No light spectator: Y from the exact linear Bogoliubov production of both species on the declared
history (analytic exp(−πk²/(mH_inf)) for instant reheating; numerical for T_rh variants), then E4.

## 3. Checks (lane script `x1_seedfree_abundance.py`, one line each, exit 0 iff all pass)

- K1 R0 reproduction: |Δ⟨|Φ|²⟩/H²| and |Δ⟨|X|²⟩/H²| < 1e-6 vs Codex's stored fine values.
- K2 V0 builder identity: max |ΔH| < 1e-12.
- K3 exact solvers internal: norm drift < 1e-8 and energy drift < 1e-6 (relative) in every V1/V3 exact run.
- K4 TW approaches exact: for each scenario and ν, max error at n = 32 < max error at n = 1.
- K5 free limit: with g = λ = 0, TW ⟨N⟩(t) matches exact within 4 sampling standard errors.
- K6 lattice energy: |E(τ) − E(0) − W(τ)|/E_phys(0) < 1e-4 in every prototype run.
- K7 lattice charge: |ΔQ| < 1e-10 · Σ|q| scale.
- K8 resume: SIGTERM at a step, then `--resume`: final arrays byte-identical to the uninterrupted run (exit 75 then 0).
- K9 time step: Φ coherent fraction at τ = 500 differs < 0.02 between dt and dt/2 (32³).
- K10 Boltzmann: BE(μ=0) input gives |C|/(rate scale) < 1e-6; number and energy conserved < 1e-6 over the E2 run.
- K11 overlap: classical Boltzmann vs TW spectrum L1 < 0.15 (as defined above).
- K12 E4 network: with all rates ×1e3 the abundance tracks equilibrium within 1 % until T_d = m/30; with rates ×0 W is
  conserved to 1e-8.
- K13 free X: numerical late n_X a³ vs the exact Bessel solution < 1e-4.
- K14 conformal control: numerical Bogoliubov vs exp(−πk²/(mH_inf)) number < 1 %.
- MUTATE (`--mutate`): the TW occupation estimator omits the symmetric-ordering −½ per mode; K5 must FAIL. Outputs go to
  `*_MUTATE.out` / `*_results_MUTATE.json`.

## 4. Physics verdict legs (reported, not counted as numerical checks)

- G1 "any input region gives 0.12": per grid point BELOW (Ω_C < 0.12: no seed-free route at this input whatever E3
  does), ABOVE (Ω_L > 0.12: overproduction whatever E3 does), or BRACKETS (Ω_L ≤ 0.12 ≤ Ω_C: 0.12 is reachable only for
  one specific, uncomputed E3 dissipation; reported as UNDETERMINED, never as a match). Ω_K is reported but never decides G1.
- G2 isocurvature: PASS/FAIL per closure and grid point.
- G3 coherence and non-Gaussianity through bath formation (E1): f₀(τ) for Φ and X, Φ energy-proxy zero-mode fraction,
  spatial κ₃/κ₂^{3/2}, κ₄/κ₂² of Re/Im δφ and g₄ = ⟨|δφ|⁴⟩/(2⟨|δφ|²⟩²) − 1, with TW_full/TW_kc/CSA spread.
- G4 TW validity window: n*, n*_10 and the error-vs-n table.
- Final word (README first line): SCOPED NO-GO if every ξ = 0 point fails G2 and every ξ = 1/6 point is BELOW;
  CRISP FINDING if some grid point is not BELOW on G1 and PASSES G2; otherwise UNDETERMINED with the deciding epoch named.

## 5. Compute and repo rules

Local runs: `OMP_NUM_THREADS=1 nice -n 15`, < 2 GB, ≤ 10 min each. Lattice production goes through `compute_queue`
(JOB_CONTRACT: SIGTERM → checkpoint → exit 75, `--resume` byte-identical, atomic writes, declared footprint); the README
carries an ENQUEUE block with exact `heavyq.py add` commands (est-gb = measured × 1.2, ≤ 8 threads, priority 240–249,
resume-cmd, done-file). This lane does not enqueue. Commits are pathspec-limited to this directory; never push; no personal
names or home paths; `sol61_push/` is read-only.

## AMENDMENT A1 (PRE-RESULT, before any V1–V3 number; R0 has run and passed bit-identically)

Feasibility, found while sizing V3 by hand: scenario A (X coherent, Φ vacuum) produces single-mode-squeezed Φ⁺ and Φ⁻
whose number tails fall only as tanh(r)ⁿ, so the full four-mode basis needs ~10⁶–10⁷ states for n ≥ 8 at ν = 8 over
t = 500; exact sparse evolution of that size does not fit the ≤ 10 min / < 2 GB rule. Change (method only, no threshold
moved):
1. V3 exact runs use the full normal-ordered Hamiltonian wherever the basis (edge probability < 1e-7 over the window) has
   ≤ 3e5 states, and the W-conserving (rotating-wave) projection H_RWA of the same Hamiltonian (keep the monomials with
   ΔW = 0, W = N_Φ + 2N_X) for every n. H_RWA is block-diagonal in (W, Q) and exactly solvable at all n ≤ 32.
2. TW is run with the classical Weyl symbol of the same Hamiltonian in each case (full H: Strang with exact harmonic part;
   H_RWA: RK4 in the rotating frame). The validity occupation n* is computed from the RWA pairs (exact-RWA vs TW-RWA) at
   all n; wherever full pairs exist, their errors must agree with the RWA-pair errors within a factor 2, else the full-pair
   errors govern at those n and the disagreement is reported.
3. V2 is unchanged; its exact P_abs ≈ 1.3e-9 (Codex) is far below any TW sampling floor at ≤ 1e6 trajectories, so V2 is
   expected to report "unresolvable at n ~ 1" with the floor stated.

## AMENDMENT A2 (PRE-RESULT for the E1 prototype; no threshold changed)

Plumbing runs made while building the lattice engine (not results, disclosed): 16³ to τ = 100; 32³ to τ = 200 and three
32³ runs to τ = 600 for the resume test; 64³ to τ = 100. Seen: Φ coherent fraction 0.90 at τ = 0 falling to ≈ 0.2–0.8
(oscillating) by τ = 200–500 at 32³; energy residual 1.1e-4 (32³) and 4.5e-4 (64³); charge drift ≤ 2e-13.
1. K8 is evaluated on the evolved state: sha256 of (φ, π_φ, x, π_x) byte-identical after SIGTERM → 75 → `--resume`
   (shown: stop-after-steps twice and a real SIGTERM, all three equal to the uninterrupted run). The FFT-based spectral
   diagnostics carry 1-ulp jitter (seen even between two fresh runs; numpy pocketfft alignment), so diagnostics are
   compared with a stated tolerance of 1e-12 relative. This is the lane's resume tolerance under JOB_CONTRACT §3.
2. K6 stays as frozen (dt = dx/20, residual < 1e-4 of E_phys(0)). With dt fixed at dx/20 the Verlet oscillation of the TW
   vacuum-noise energy at the cutoff is a fixed fraction of a vacuum energy that grows ∝ N⁴ relative to E_phys, so K6 can
   FAIL at 64³ without any secular drift. Added diagnostics (reported, not checks): the same residual for CSA (no UV
   noise) and for dt/2.
3. scipy's expm_multiply leaked ~80 MB per call here; the one V3 point B ν=8 n=8 (full) peaked at 4.36 GB before this was
   found (rule breach, disclosed). The exact propagator is now a shifted Taylor series (agrees with expm_multiply to 8e-13),
   and all full-H V3 points are recomputed with it.

## AMENDMENT A3 (POST-RESULT for the closure-L and closure-C values at the primary point and for the partial V3 table, which
## were seen while building; PRE-RESULT for closure K, E2, the input map, the isocurvature legs and the final V3 table)

Seen before this amendment (disclosed): Y_L ≈ 3.9e-14 (Ω_L ≈ 1.07e-8) and Ω_C = 0.167 at the primary point; Ω(ξ = 1/6)
≈ 6e-30; the V3 scenario-B rows and A rows for ν = 8, n ≤ 4; the E1 prototype diagnostics (A2). No threshold moves.
1. V3 metric (unchanged): with max-over-time absolute errors, O5/O6 are dominated by instants where κ₄/κ₂² ≈ 10 (thin,
   phase-aligned quadrature distributions); the frozen n* is reported as computed (it may not exist for n ≤ 32). Added
   diagnostic only: the median-over-time errors and an occupation-only validity occupation (O1–O4), labelled as such.
2. Hand-over f₀ = trailing 100-τ mean of |φ̄|²/(⟨|φ|²⟩ − c): the instantaneous value passes through zero twice per
   zero-mode oscillation. If the frozen n* does not exist the criterion is unreachable and E2 is CONDITIONAL.
3. Boltzmann numerics: f(p₄) interpolated in energy through ln(1 + 1/f) (classical: 1/f), and C[f] − C[f_eq] with f_eq
   the grid BE (or Rayleigh–Jeans) state of equal number and energy (raw equilibrium residual 3 % / 1.3 % at Np = 96/192).
4. r3 above T = 2m (the frozen text did not say): Monte-Carlo average of Codex's complete tree amplitude (x1_dmc.py,
   validated against Codex's MB table to ≤ 0.74 %), BE statistics and Hartree masses; thermal X for the network, X at rest
   for the condensate (closure K). Codex's last-interval power law (slope −3.39) is a reported sensitivity. Thermal widths
   are not included; Γ_Φ ≈ 2M at onset would lower the X-at-rest rate by an O(1) factor there.
5. Closure K numerics: if the per-X absorption rate of the condensate Γ/H > 10 at onset, the cold X are absorbed at onset
   (stiff limit): energy M per X into the bath, N_Φ unchanged (r3 stoichiometry), no thermal X; the network then runs.
6. E4 thermodynamics: Bose sums with scaled Bessel functions, Hartree Φ mass from the μ = 0 table; LSODA in log variables
   (rtol 1e-6). Added sensitivities (not frozen): 4→2 off above T = m ("relcut"), crossed channel ×1, D power law.
7. ξ = 1/6: the conformal mode starts in its vacuum at x ≈ 0 (a ≈ 0 in the scaled variable), a half-line problem; the
   full-line exp(−πk²/(mH)) named in K14 is not its exact answer (half/full = 0.371), so K14 FAILS as frozen; the control
   value reported is the numerical half-line one. Production during a w = 0 era (H_rh < 10 m_s) is not evaluated.
