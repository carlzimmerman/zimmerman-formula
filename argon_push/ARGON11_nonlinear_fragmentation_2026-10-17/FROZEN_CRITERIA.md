# ARGON11 — nonlinear fragmentation of astra's coherent charged state (3+1D). FROZEN CRITERIA

2026-10-17. Committed alone, before any scored run. Lives in `argon_push/` (my folder); no file of astra's is edited. Task: astra's NEXT #1
("nonlinear weakly coupled charged fragmentation") and the open point of ARGON10 F2/F3 (lump size and charge were a linear-scale ESTIMATE).
κ = ½ FITTED; footings never pooled; "cold energy"; its mass is required; not "theory closed"; no ΛCDM / standard-MOND yardstick in any verdict.

**Model (astra's CPB-UV potential, unchanged).** m_h = 1 units. L = −|∂Ψ|² − ½(∂χ)² − V, V = I + L_q I² + aχI + U(χ), I = |Ψ|²,
U = M²χ²/2 − (M/8)χ³ + χ⁴/4, L_q = 2 − 1/M, a = 2M, M = 100. EOM: Ψ̈ = ∇²Ψ − (1 + 2L_q I + aχ)Ψ; χ̈ = ∇²χ − U′(χ) − aI.
Charge density n = 2 Im(Ψ*Ψ̇); coexistence phase (ARGON10): I* = 48.989, ω*² = 0.753423, n* = 2ω*I* = 85.1.
Weak route (ε): the classical dynamics in rescaled fields is identical (Ψ = ψ/√ε), lumps keep their shape and Q → Q/ε. It is not re-run; it is applied analytically exactly as in ARGON10 F2.

**Solver.** `frag3d.c` (this folder; sha256 of the committed file is recorded in the result): periodic cube, 4th-order Laplacian, kick–drift–kick velocity Verlet, double precision, dt = 0.01.
Pilot (N = 32, s = 0.5, ε = 1e-3, t = 150) was run before freezing only to test the code: charge drift 0, energy drift 9e-6, late-linear growth 0.070 versus the allowed-mode prediction 0.074.
The K2 fit window below was chosen after that pilot (early times are a non-exponential transient); no other threshold was set from it.

**Initial state.** Ψ = √I₀(1 + εζ), ζ complex white Gaussian per site (re, im each variance ½), Ψ̇ = iωΨ, χ = χ₀ (U′(χ₀) + aI₀ = 0), χ̇ = 0, ω² = 1 + 2L_qI₀ + aχ₀, I₀ = sI*.
This coherent charged state is an INPUT (astra: "coherent charged initial state INPUT, not neutral gas"); the noise amplitude ε is an INPUT.

## Runs (all on the machine, single thread each, `nice -n 10`, ≤ 0.3 GB each; none starts or continues while a 1024³ run is live)
| id | s | N | dx | L_box | seed | ε | t_end | note |
|---|---|---|---|---|---|---|---|---|
| R1 | 0.1 | 96 | 1.0 | 96 | 1 | 1e-4 | 700 | primary |
| R2 | 0.1 | 96 | 1.0 | 96 | 2 | 1e-4 | 700 | seed |
| R3 | 0.1 | 128 | 0.75 | 96 | 1 | 1e-4 | 700 | resolution |
| R4 | 0.5 | 96 | 1.0 | 96 | 1 | 1e-4 | 500 | second density |
| R5 | 0.1 | 64 | 1.0 | 64 | 1 | 1e-4 | 700 | MUTATE M5: L_q = 2 + 1/M (net quartic repulsive) |
| R6 | 0.1 | 64 | 1.0 | 64 | 1 | 1e-4 | 700 | amplitude pair |
| R7 | 0.1 | 64 | 1.0 | 64 | 1 | 1e-6 | 800 | amplitude pair |
| R8 | 0.1 | 128 | 1.0 | 128 | 3 | 1e-4 | 700 | box size |
Snapshots (I, n, local energy) every 25 time units; log every 2.5. Snapshots stay outside the repo (`_external_data/argon11_work/`); only analysis outputs are committed.

## Gates
**K1 conservation (every scored run).** |ΔQ/Q₀| ≤ 1e-6 and |ΔE/E₀| ≤ 1e-3 to t_end (E = the discrete Hamiltonian; Q = Σ n dV).
**K2 linear stage (R1–R4, R6, R7, R8).** γ_meas = ½ d ln⟨|Ψ−⟨Ψ⟩|²⟩/dt fitted over ⟨|Ψ−⟨Ψ⟩|²⟩/I₀ ∈ [1e-4, 1e-2]. γ_pred = max over allowed discrete modes |k| = (2π/L_box)√(j₁²+j₂²+j₃²) of ARGON10's F1 curve (interpolated). **PASS** iff |γ_meas/γ_pred − 1| ≤ 0.10.
**Lump identification (analysis, periodic).** Core = connected set of cells with I > 0.5 I* (face-connected, wrapped). A *lump* = a core with charge in the core ≥ 1e3. Each cell within 4 cells of a core and with I > 0.05 I* is assigned to the nearest core (periodic distance); Q_f, E_f are integrals of n and the local energy density over a lump's assigned cells; R_eff = (3V_core/4π)^{1/3}; n_in = (charge in core)/V_core; the halo-radius variant R_0.1 uses cells with I > 0.1I* connected to the core.
Hard-sphere σ = 4πR², m_f = m_h Q_f (as in ARGON10 F2), so S ≡ (σ/m)m_h³ = 4πR²/Q_f (primary R = R_eff; bracket R_0.1). Conversion to cm²/g and the CFG725 classes (BELOW < 0.105, LOW-EDGE 0.105–0.82, ABOVE-LOW 0.82–10, EXCLUDED > 10) exactly as in ARGON10 F2, at ε ∈ {1, 1e-3, 1e-6}, m_h = 1 MeV.
**Epochs.** t_A = first snapshot at which ≥ 50 % of the total charge lies in cores; t_end = last snapshot.

## Readings
**K3 FRAGMENTS** (R1, R2, R3, R4 each): at t_A there are ≥ 3 lumps, median |n_in/n* − 1| ≤ 0.25, and median E_f/Q_f < 1 (bound against free quanta of mass m_h per unit charge). Otherwise **NO STABLE FRAGMENTS** with the reason printed. Reported but not gated: E_f/Q_f against ω*, N_lump(t), Q_med(t), S(t), lump shapes (core V vs bounding extents).
**K4 F2 estimate (R1, R4 at t_A).** r_Q = Q_med/Q_est, r_S = S_med/S_F2 with Q_est, S_F2 = 1.001e5, 5.385e-3 (s = 0.1) and 2.572e5, 3.932e-3 (s = 0.5) from ARGON10 F2. **SURVIVES** iff 1/3 ≤ r_Q ≤ 3 and 1/3 ≤ r_S ≤ 3; otherwise **REVISED** (the measured Q_med, R_eff, S and their CFG725 class replace the estimate). The same table is also reported at t_end (coarsened).
**K5 convergence.** CONVERGED iff all hold between R1 and R3 (resolution) and between R1 and R2 (seed): t_A within 10 %; N_lump(t_A) within 30 %; Q_med(t_A) within 30 %; S_med(t_A) within 30 %. R8 vs R1 (box) is reported on the same four numbers. Otherwise **NOT CONVERGED**; then every number is quoted as a range over runs and K4 is read on the range.
**K6 amplitude (R6, R7; informative).** Q_med(t_A) within a factor 1.5 between ε = 1e-4 and 1e-6.
**K7 coarsening (informative).** Q_med(t) and N_lump(t) from t_A to t_end, with the S at t_end. The box is periodic and has no expansion: coarsening here is an upper bound on merging, not a prediction.
**K8 energy bookkeeping (informative).** f_rad = 1 − ΣE_f/E_tot at t_A and t_end; f_max = 1 − ω*Q_tot/E_tot (all charge in lumps at E/Q = ω*); Q_out = Q_tot − ΣQ_f. Not a coldness claim: no spectrum of the non-lump energy is computed.

**MUTATE M5 (R5).** With L_q = 2 + 1/M, F1's curve has no growth for s = 0.1. **Bites** iff R5 gives no lump (t_A undefined by t_end) and K2 is not applicable (γ_pred ≤ 1e-10); otherwise **DOES NOT BITE**, reported, not rescued.

## Conduct and scope
Scripts: `argon11_run.py` (launcher; checks no 1024³ run is live and runs a watchdog that stops the job if one appears; jobs resume from checkpoints), `argon11_analyze.py` (reads logs/snapshots, prints every gate), `REPORT.md`, `HANDOFF_TO_ASTRA.md`.
Not claimed: a prediction of the real lump spectrum (no expansion, no thermal or quantum seed, one coupling M = 100, one box family); stability of lumps beyond t_end; any statement about the gas of free quanta (collisionless in the weak route); anything about observations. Failures and non-convergence are reported as such.
