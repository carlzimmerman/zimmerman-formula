# L1_khronon_pm FROZEN CRITERIA (2026-10-23): a Khronon-native particle-mesh engine for v3 (F3 README §6), built and validated at small scale only

Written and committed alone, before any script or number of this lane. Rules: `rebuild_2026_10_22/BRIEF.md`,
`covariant_push_2026_10_22/BRIEF.md`, `doors_push_2026_10_22/BRIEF.md`, `BRIEF_E_AUDIT.md`. κ = ½ FITTED. Footings
a₀ = 9.3603e-11 (canonical) / 1.1312e-10 m/s² (alt), never pooled. No dark-matter particle: the cold sector is the
Blanchet–Skordis K(Q) dust ("cold energy"), represented by particles that carry the khronon's hold force. Never "theory
closed". Never "the data favour the framework". **Compute:** CFG960 (1024³) is running and is not touched or duplicated.
Every run of this lane: `OMP_NUM_THREADS=1 nice -n 15`, one thread, < 1 GB RSS, nothing larger than 128³. No downloads.

## 0. The question and why

The trilemma (`covariant_push_2026_10_22/THEORY_V3_DRAFT.md` §1b; F3, I1, C7): v3 (Khronon + J_x + K(Q) dust + γ_L)
fails LINEAR growth (F3 K1/K4: J_x′(0) = −1; inside BS24's cap μ_K ≤ 14.8 h/Mpc linear σ₈ is 0.03–0.32). The one undecided
escape is nonlinear: does v3's full J_x (its deep-MOND Y^{3/2} term and beyond) change structure growth at μ_K inside BS's
window? Only a native nonlinear simulation decides. This lane **builds and validates** that engine at 32³–128³, reports one
**indicative** 128³ number, and **freezes** the production run. The indicative number is not a verdict. The production
run decides.

## 1. The engine's equations (what "Khronon-native" means here)

F3 §6 writes the field equation in its static form, ∇·[μ(|∇ψ|/a₀)∇ψ] + μ_K²ψ = 4πG(ρ_b + δρ_K), μ = x/(1+x). That is
BS24 Eq. 35 (C4 K1). Its native **dynamical** form is BS24's post-Newtonian system (eqs. 19, 25, 27, 29, 30), as transcribed
and checked in the record (`real_research/bs_khronon_2026/BSK1_moving_source_gate.py` L15–21, M2–M4, M7):

- Ξ = φ − σ̇ + |∇σ|²/2 (unitary-gauge lapse perturbation; the khronon congruence's acceleration is ∇Ξ, Y = |∇Ξ|²/c⁴);
- 4πGρ_τ = −[∇·(J_Y ∇Ξ) + μ_K² Ξ] (the hold equation; with J_x, J_Y = μ(x) − 1 = −1/(1+x), x = |∇Ξ|/a₀);
- ∇²φ = 4πG(ρ_b + ρ_τ) (Poisson for the metric potential, all mass);
- v_τ = −∇σ, ∂_tρ_τ + ∇·(ρ_τ v_τ) = 0, hence Dv_τ/Dt = −∇φ + ∇Ξ (the khronon's Euler equation);
- baryons: Dv_b/Dt = −∇φ.

Static limit (σ = 0, so Ξ = φ): subtracting the hold equation from Poisson gives ∇·[μ(x)∇φ] + μ_K²φ = 4πGρ_b, i.e. F3 §6's
equation with the K(Q) sector already inside it (ρ_τ is the phantom). **Writing δρ_K on the right of F3 §6's equation as
well, and giving the K fluid a separate pressure, would count the K(Q) sector twice** (its μ_K² term *is* its pressure:
BSX3 I1, μ_eff² = k_J²(1 + c_ad²)). The engine therefore implements the PN system, not the literal two-source form. This
is a reading of F3 §6, recorded here before any number, not a new posit.

Comoving form used by the engine (code units: x in Mpc/h, time 1/H₀, velocity 100 km/s; Φ, Ξ in (100 km/s)²):
- ∇²Φ = (3/2)(Ω_m/a) δ_m, δ_m = f_b δ_b + f_τ δ_τ;
- ∇·[(1 − μ(x))∇Ξ] − a²μ_K² Ξ = (3/2)(Ω_τ/a) δ_τ, with x = |∇Ξ| / (a · a₀/ACC_UNIT), ACC_UNIT = 10¹⁰ h / Mpc m s⁻²;
- baryon particles kicked by −∇Φ; khronon particles by −∇(Φ − Ξ).

Linearisation on FRW (x → 0): Ξ_k = −(3/2)(Ω_τ/a)δ_τ/(k² + a²μ_K²), so the khronon's own-gravity kernel is
s = a²μ_K²/(k² + a²μ_K²): **F3's BSK2 kernel** (and BSK1 M7). With J ≡ GR (J_Y ≡ 0): Ξ = −(3/2)(Ω_τ/a)δ_τ/(a²μ_K²),
s = 1 − k²/(a²μ_K²): **F3's Jeans kernel**. With J ≡ GR and μ_K → ∞: Ξ → 0, ordinary dust (ΛCDM-like control).

**Modes of the engine** (one code path, a switch on the hold):
- `KX` — v3: full J_x hold, solved nonlinearly (below);
- `LIN` — linearised v3: J_Y ≡ −1 exactly (Ξ = −S/(k² + a²μ_K²)); the linear theory carried by nonlinear gravity;
- `GRJ` — J ≡ GR at finite μ_K (Jeans kernel; Ξ = −S/(a²μ_K²));
- `S0` — J ≡ GR, μ_K = ∞ (Ξ ≡ 0), dust-limit ICs: the control.

**Nonlinear solver (KX).** Spectral (FFT) gradients/divergence on the periodic mesh, Nyquist planes zeroed. Fixed-point form
(∇² − a²μ_K²)Ξ = S + ∇·[μ(x)∇Ξ], accelerated by Anderson mixing (depth 5), warm-started from the previous step. Converged when
‖Ξ_{n+1} − Ξ_n‖₂/‖Ξ_{n+1}‖₂ ≤ 1e-6 (cap 400 iterations). Every force call records iterations, final residual, x_rms and
x_max. A call that does not converge is recorded; any non-converged call makes that run INVALID (reported, not rescued).

**Integrator.** Kick–drift–kick in a (kick ∫da/(a²E), drift ∫da/(a³E)), CFG596's step grid (150 steps, z_i = 49; the z_i = 199
variant prepends 60 equal-ln a steps from a = 1/200 to 1/50). CIC deposit and interpolation, no force deconvolution (as CFG596).
Particles: N_p = N_mesh per species, both species on the same lattice (cell centres).

## 2. Assumption ledger (classes: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / ΛCDM-PROCESSED / STANDARD-MOND-MACHINERY / POSITED)

| ingredient | engine choice | class | source |
|---|---|---|---|
| field equations | BS24 PN system (§1), J = J_x, K = μ_K²(Q−1)² | FRAMEWORK-NATIVE (J_x POSTULATED, outside BS's class, C4); BS24 equations external, transcribed via WebFetch, not on disk (PROVISIONAL), self-consistency checked in BSK1 M2–M4 and C4 K1 | BSK1 L15–21; C4 README §Source |
| cosmological (comoving, mean-subtracted) form | standard Newtonian-cosmology substitution; k_J → aμ_K (Q̄ → 1) | DERIVED (F3 K1(ii) A1); valid while Q̄ − 1 ≪ 1 (checked in X0) | F3 K1 |
| hold argument x | |∇Ξ| (khronon congruence acceleration), physical, a₀ constant in time | FRAMEWORK-NATIVE (v3's J has a constant a₀); κ = ½ FITTED | BSX1; C4 K2 |
| μ_K | 14.8 h/Mpc (BS24 Eq. 39 edge, F3) for validation and the indicative run; 14.8 and 400 for production | EXTERNAL premise (BS24 Eq. 39); μ_K is absent from the v3 parameter table (F3 §7); not fitted here | F3 K4/K5, §6 |
| background | flat, Ω_m = 0.2976016, h = 0.6856427 (CFG886 GR fit, BAO + BBN, no CMB), Ω_b = ω_b/h² with ω_b = 0.0223081 (C2 c2b refit), radiation Ω_r = 4.18e-5/h² (as F3's solver), Λ fills; K sector treated as w = 0 | FRAMEWORK-NATIVE in the dust limit (C2); ω_b from a plik-lite refit (SURVEY-CALIBRATION inside); w = 0 checked in X0 | F3 K2 model B |
| linear spectrum at z = 0 (dust limit) | vanilla CLASS 3.3.4 at model B with C2 c2b A_s, n_s, τ | FRAMEWORK-NATIVE in the dust limit (C7 V1, F3 ledger) | F3 K2 |
| per-species IC transfer | F3's two-fluid sub-horizon ODE (baryons feel all mass; khronon own-gravity kernel per mode) from a_start = 1e-3 with δ_b = δ_τ ∝ a (F3's optimistic start), evolved to z_i; δ_s and f_s = dlnδ_s/dlna per k | POSITED start condition (F3's; ignores the baryon acoustic lag at recombination and the khronon's earlier history); the kernel is FRAMEWORK-NATIVE (§1 linearisation) | F3 `growth_ratio` |
| IC phases | CFG596 white-noise recipe, seed 359, NSEED = 256 for N ≤ 256 (production N = 512: NSEED = 512, in place) | pipeline choice (random phases) | `cfg596_pm.py` `initial_conditions_*` |
| IC displacement | Zel'dovich per species, momentum a²E f_s(k) ψ_s | standard; exact at linear order | — |
| baryons | collisionless particles, no pressure | POSITED (standard PM approximation; baryon Jeans scale ≫ k_Nyq at z < 49) | — |
| khronon | collisionless particles carrying the hold force | POSITED beyond shell crossing (BS's khronon flow is single-stream, v = −∇σ); F3 §6 allows particles | F3 §6 |
| settling, relocation, catchments, f_ret, switches | **absent** | — | — |
| QUMOND phantom, ν_mono, EFE recipe | **absent** (the phantom arises dynamically as ρ_τ) | — | — |
| γ_L stiffness (L★) | absent: L★ ≤ 90 pc is ≥ 10³× below the cell | FRAMEWORK-NATIVE, irrelevant at cell scale (F3 §3) | D10, F3 |
| gate (a) reference | CFG596 lean engine, verbatim copy, S0, MODE = exact, its EH ICs and Planck-2018 background | ΛCDM-PROCESSED; used **only** as a numerical reference for the GR limit, never in a verdict | `CFG596_lean_pm_1024/cfg596_pm.py` |
| production KiDS likelihood | CFG592 library exec'd unchanged (as F3 K0, CFG596): ξ± RAW; covariance, SOM n(z), Δz, m, NLA IA SURVEY-CALIBRATION; projection background and EH/D(z) edges ΛCDM-PROCESSED; plus the native model-B projection variant (F3 K3) | as listed | F3 ledger 1b |

## 3. Checks of the validation script `l1_khronon_pm.py` (one line per check; exit 0 iff all pass)

- **K0 (reproduce the record's linear numbers first).** This lane's copy of F3's ODE on F3's background A reproduces F3 K4
  `bsk2_ai0.001` at μ = 14.79771 h/Mpc (σ₈ ratio 0.39080) and `jeans_ai0.001` (0.12055) to ≤ 1e-3 relative.
- **X0 (pre-flight, reported).** On model B, with the BSK2 kernel from a_start = 1e-3: the linear rms hold-field argument
  x_rms,lin(a) = rms |∇Ξ|/(a a₀) (Ξ from the linear δ_τ(k, a) of the dust-limit CLASS spectrum, k ≤ 4 h/Mpc, also k ≤ 16)
  at a = 1e-3, 5e-3, 0.02, 0.1, 0.5, 1 on both footings; and Q̄ − 1 and w of the quadratic-K background at z_i = 49 and 199
  (Q̄ − 1 = I₀/(2μ_K²a³), I₀ = 3H₀²Ω_τ/c², C4 K7). PASS = computed. **Flag rule (frozen):** if x_rms,lin > 0.1 anywhere in
  [1e-3, a_i = 0.02] on either footing, the J_x nonlinearity is active before z_i and the linear ICs miss it; the indicative
  set then adds the z_i = 199 variant (LIN and KX canonical), and the production plan uses both z_i.
- **KA (gate a: GR limit).** Engine in mode GRJ with μ_K = 10⁶ h/Mpc (Ξ → 0 along the GRJ code path), both species given
  CFG596's exact-mode ICs at 64³, L = 100 Mpc/h, CFG596's background (Ω_m 0.3153, no radiation) and step grid, against the
  copied CFG596 S0 engine on the same ICs. PASS iff max over bins k ≤ k_Nyq/2 of |P_engine/P_CFG596 − 1| ≤ 0.02 at z = 0
  (z = 1 and 0.5 reported).
- **KB (gate b: linear growth = F3's linear prediction at the same μ_K).** Mode KX (full J_x, nonlinear solver on),
  μ_K = 14.8 h/Mpc, canonical footing, IC amplitude × ε = 0.01 (δ and x both linear), 64³, L = 25 Mpc/h, model B; and the S0
  run on the same phases and ε. Growth per bin from z_i, by cross-correlation of the total-matter mesh field:
  G(k, z) = Σ Re[δ(z) δ*(z_i)] / Σ |δ(z_i)|². Statistic R = G_KX/G_S0, compared with the ODE's R_ODE at the bin-mean k.
  PASS iff max over bins k_f ≤ k ≤ k_Nyq/4 of |R/R_ODE − 1| ≤ 0.02 at z = 3 and at z = 0. Reported, not gated: G_S0/G_ODE,dust
  (the PM's own resolution bias); the same statistic for mode GRJ against the Jeans-kernel ODE; and the tooth size
  max|R_ODE − 1| over the same bins.
- **KC (gate c: static point mass).** 128³ box, L = 0.32 Mpc/h, a = 1, μ_K = 0 (BS24 Eq. 39: μ_K⁻¹ ≫ galaxy), baryon mass
  10¹¹ M_⊙/h as a Plummer sphere of scale 2 cells, both footings.
  - (c1) the engine's AQUAL solver (iterative FFT: alternating curl-free projection, μ = x/(1+x)) vs the law
    g = ν(g_N/a₀) g_N, ν(y) = (1 + √(1 + 4/y))/2, applied to the box's own Newtonian field; shell-averaged radial fields in
    10 log shells r ∈ [3 cells, L/8]. PASS iff max |g/g_law − 1| ≤ 0.01.
  - (c2) the engine's equilibrium: with ρ_τ set to the phantom of the (c1) solution, the engine's force routine (Poisson for
    all mass; hold equation by the KX solver **started from Ξ = 0**) must return a baryon field equal to the law and a
    force-free khronon. PASS iff, on the same shells, max |g_b/g_law − 1| ≤ 0.01 and max |∇(Φ − Ξ)|/|∇Φ| ≤ 0.01.
    (The Poisson half of (c2) is an identity of the spectral operators, said so here; the hold half is the test.)
- **KD (gate d: mutate).** `L1_MUTATE=1`, outputs `*_MUTATE.out` / `*_results_MUTATE.json`: KA drops the khronon from the
  Poisson source; KB removes the hold (Ξ ≡ 0 in KX); KC uses μ = x/√(1+x²) in (c1) and (1 − μ) → μ in the hold of (c2).
  KA, KB and KC must all FAIL (exit 1). K0 and X0 are unchanged.

## 4. The indicative 128³ set (`l1_indicative.py`; not a verdict)

L = 100 Mpc/h, 128³ mesh, 128³ particles per species, model B, z_i = 49, same phases for all runs, μ_K = 14.8 h/Mpc:
`S0` (dust-limit ICs), `LIN` (BSK2 ICs, linear hold), `KX-can`, `KX-alt` (BSK2 ICs, full J_x hold). If X0 flags: also
`LIN-199` and `KX-can-199`.

Statistics (frozen definitions):
- σ₈,PM = total-matter σ₈ at z = 0 from the particles on the mesh (CFG596 `measure_pk` definition: CIC-deconvolved,
  top-hat 8 Mpc/h, sum over mesh modes);
- σ₈,lin,box = the linear prediction for the same realisation and modes (IC field × ODE growth to z = 0);
- σ₈,lin,∞ = F3-style infinite-volume linear σ₈ on model B at the same μ_K (CLASS P(k) × ODE transfer²);
- restoration fraction ρ_NL = (σ₈[KX] − σ₈[LIN]) / (σ₈[S0] − σ₈[LIN]), per footing.

Checks: I1 every run completes with every force call converged; I2 S0 sanity σ₈,PM/σ₈,lin,box ∈ [0.98, 1.15];
I3 LIN sanity σ₈,PM/σ₈,lin,box ∈ [0.98, 1.30]; I4 ρ_NL computed and finite on both footings; I5 peak RSS < 1 GB.
MUTATE (`L1_MUTATE=1`, at 32³ only): the hold solver capped at 1 iteration (I1 must FAIL) and S0 without the khronon in
Poisson (I2 must FAIL).

**Reading (indicative only, frozen):** ρ_NL ≥ 0.5 "the nonlinear J_x term restores most of the linear deficit at 128³";
0.1 ≤ ρ_NL < 0.5 "partial"; |ρ_NL| < 0.1 "does not restore growth at 128³"; ρ_NL ≤ −0.1 "deepens the deficit". Whatever
the reading, the sentence "indicative, not a verdict; the frozen production run decides" goes with it.

## 5. The production plan (frozen; NOT run now; scheduled after CFG960 finishes)

- **When:** only after `cfg960_sctm_pm.py` / `chain960.sh` have exited (no CFG960 process in `ps`), and only with the owner's
  go-ahead for a run above 128³.
- **Runs:** 512³ mesh, 512³ particles per species, L = 100 Mpc/h, model B, NSEED = 512 (in place), z_i = 49 (plus z_i = 199
  if X0 flags), modes S0 ×1, LIN ×2 (μ_K = 14.8, 400 h/Mpc), KX ×4 (μ_K = 14.8, 400 × canonical, alt). Snapshots z = 1, 0.5,
  0 (total-matter and per-species P(k)); force-call diagnostics as in §1.
- **Command (per run, from the repository root):**
  `cd rebuild_2026_10_22/L1_khronon_pm && OMP_NUM_THREADS=4 nice -n 10 python3 khronon_pm.py run --mode KX --foot canonical --muK 14.8 --N 512 --L 100 --zi 49 --nseed 512 --threads 4`
  (and the same with `--mode S0|LIN|KX`, `--muK 14.8|400`, `--foot canonical|alt`).
- **Memory:** estimated in the README from the measured 64³/128³ peak RSS (bytes per particle and per mesh cell), and a run
  is not started unless free + inactive memory exceeds 1.5× that estimate.
- **Scoring:** KiDS-1000 ξ± with the CFG592 library exec'd unchanged and CFG596's node construction (P at z = 0, 0.5, 1;
  k_lo = first bin, k_hi = πN/(4L); support ≥ 90 %), Δχ²(KX − S0) per μ_K and footing, CFG596's classes
  (EXCLUDED / TENSION / CONSISTENT / NOT DIAGNOSTIC); both on the library's projection background and on model B (F3 K3 style).
  Also σ₈(z = 0), S₈ on model B, and ρ_NL per μ_K and footing.
- **What the production decides:** whether v3's full J_x restores growth at μ_K = 14.8 (ρ_NL and σ₈ against the S0
  control), and whether either μ_K is CONSISTENT with raw KiDS against S0. At μ_K = 400 the hold leaves the 512³ mesh by
  a ≈ 0.04, so that run tests mainly the IC-carried linear suppression plus nonlinear gravity; this is stated in advance.

## 6. What a result of this lane can and cannot say

- Gates pass/fail are engine statements, not physics verdicts.
- The indicative 128³ number is not a verdict on v3's growth (box 100 Mpc/h, 128³, one realisation). Its only use is to say
  whether the nonlinear term moves σ₈ at all, and in which direction.
- Physics outside the engine (pre-z_i history beyond the linear ICs; quadratic-K background before z ≈ 200 at μ_K = 14.8;
  khronon multistreaming) is listed in the README as a limitation, with the X0 numbers.

## AMENDMENT A1 (PRE-RESULT, 2026-10-23, before any script or number; coordinator instructions relaying the owner)

Reason: the owner stopped CFG960 to free memory for v3 work (ledger 89fbefe1c0), and asked that heavy runs be preemptible.
Nothing in §1–§4 (equations, gates, thresholds, indicative set, readings) changes. Changes:

1. **Compute for the validation and indicative runs** stays as frozen (≤ 128³, one thread, < 1 GB, nice 15).
2. **Production is run in this lane, after KA, KB, KC (and KR below) pass**, no longer "not run now". §5's runs, box,
   scoring and readings are unchanged. Launch conditions replacing §5 "When" and the per-run command's thread/nice settings:
   - size: the largest N ∈ {512, 1024} whose **declared** peak memory (engine `--estimate`, calibrated on the measured
     64³/128³ peaks) is ≤ 45 GB; 1024³ is used only if it fits;
   - `nohup`, `nice -n 5`, up to 8 threads (scipy.fft workers and numexpr; particle chunks in a thread pool);
   - hard abort (exit 3, no output written) if system swap use grows by > 4 GB over its value at start or the process RSS
     exceeds 52 GB (the CFG960 rule); a crash or abort resumes from the latest checkpoint;
   - if `compute_queue/heavyq.py` exists when production is ready, the runs are enqueued with `python3 compute_queue/heavyq.py add ...`
     instead of launched directly; otherwise launched directly with the SIGTERM handler in place;
   - run order: S0, LIN-14.8, KX-can-14.8, KX-alt-14.8, LIN-400, KX-can-400, KX-alt-400 (one heavy job at a time).
3. **Preemptible engine.** On SIGTERM the engine finishes the current step, writes a checkpoint at that safe point (after
   the drift) and exits 0 (target ≤ 300 s at 512³). `--resume` continues from the latest checkpoint. Checkpoints are also
   written every 10 steps. Checkpoint and result files are written atomically (temporary file + `os.replace`). The run JSON
   declares the peak-memory estimate before the first step.
4. **New validation check KR (resume).** 64³, L = 25 Mpc/h, mode KX, μ_K = 14.8, canonical, full amplitude, model B, one
   thread: an uninterrupted run vs a run that receives a real SIGTERM mid-run (after step ≥ 40 is reported), exits, and is
   resumed with `--resume`. PASS iff the interrupted process exits with code 0 within 300 s of the signal, a checkpoint
   exists, and the resumed run's final particle state and z = 0 P(k) are **bit-identical** to the uninterrupted run's
   (sha256 of the state arrays equal). If bit-identity fails, the measured max |ΔP/P| is reported and KR FAILS (no
   tolerance is set after the fact). KR is not mutated (it is an engineering check); MUTATE still must fail KA, KB, KC.

## AMENDMENT A2 (POST-RESULT, 2026-10-23, after validation RUN1; RUN1 kept as `l1_khronon_pm_RUN1.out` / `_results_RUN1.json`)

RUN1: K0 PASS, X0 PASS (flag raised), KA FAIL, KB FAIL, KC PASS, KR PASS (4/6). Peak RSS 2.27 GB.

1. **KA: a script bug, not a gate result.** The script added an unfrozen sanity condition (k-bin centres equal to 1e-9
   absolute). CFG596 builds k in float32, so its bin centres differ by ~1e-7 relative and the line printed FAIL although the
   frozen statistic was max|P/P_CFG596 − 1| = 8.7e-5 (threshold 0.02). The sanity condition is now 1e-5 relative. The
   frozen statistic and threshold are unchanged.
2. **KB FAILED as frozen** (max|R/R_ODE − 1| = 0.0345 at a = 0.253 and 0.0356 at z = 0, threshold 0.02). Diagnosis (post-result):
   - lowest two bins (k = 0.32, 0.56): the frozen line evaluates the ODE at the bin-mean k, while the estimator weights each
     mode by |δ(z_i)|². Pushing the linear prediction through the same estimator gives deviations 0.0003 / 0.0011;
   - bins k ≳ 1 h/Mpc: the PM's own force deficit near the grid scale (S0's PM/ODE growth falls from 0.997 to 0.83 over the
     bins) does not cancel in R, because the suppressed khronon couples more weakly than dust. Fitting one PM coupling g per
     bin on the **S0 run alone** (dust ODE) and reusing it for KX brings these bins to ≤ 0.007.
   **Re-scored statistic KB-A2 (post-result):** max over the same bins and epochs of |G_KX,PM / G_KX,A2 − 1| ≤ 0.02 (threshold
   unchanged), where G_KX,A2 is the linear (ODE) prediction per mode, weighted per mode by wt·|δ_lin(k, z_i)|²·W_CIC(k)²
   (the estimator's own weights), with the coupling g_j fitted on S0's PM growth in bin j. The frozen line is still
   printed as `KB-frozen` and stays FAIL. The same A2 statistic for GRJ (Jeans kernel) is reported, not gated (its
   transfer oscillates in k, so the frozen bin-mean comparison is meaningless for it).
   What KB-A2 does not show: that the PM is accurate near its grid scale. It shows that the hold term reproduces the linear
   theory once the PM's own deficit, common to KX and S0, is calibrated on S0. The production statistic compares KX with
   S0 on the same mesh, so that deficit enters both arms.
3. **KC (reported addition):** the c1 projection iteration stalls at a 2.5 % iterate change (grid-scale aliasing; the
   residual at k < k_Nyq/2 is ≤ 1e-3). An independent Anderson AQUAL solve (the KX solver with coefficient 1 − μ in the
   divergence, i.e. ∇²Φ = S + ∇·[(1 − μ)∇Φ]) converges to 8e-10 at 128³ and agrees with it in every shell to 4.6e-5. It is
   printed as a reported line. The gate is unchanged.
4. **Memory disclosure:** RUN1 peaked at 2.27 GB RSS, above the frozen 1 GB guideline (KC at 128³ and the CFG596 reference's
   256³ white noise). The owner had lifted the memory restriction (A1) before the run.

## AMENDMENT A3 (PRE-RESULT for the indicative set and production, 2026-10-23, before any indicative or production number)

1. **X0 raised the flag** (x_hold,rms,lin = 0.78 / 0.65 at z = 199, 11.2 / 9.3 at z ≈ 1000, canonical / alt; 0.049 / 0.041
   at z = 49). The z_i = 199 variant is therefore mandatory (frozen rule). The quadratic-K background has Q̄ − 1 = 1.5e-3
   (w = 7.6e-4) at z = 199 and 0.19 (w = 0.087) at z ≈ 1000, so the engine cannot start earlier than z ≈ 200 at μ_K = 14.8.
   The epoch z ≈ 1000 → 199, where x ≫ 1, is not simulated by any run here. That is a stated limitation.
2. **Indicative set** adds `S0-199` (control for the z_i = 199 pair). ρ_NL,199 = (σ₈[KX-199] − σ₈[LIN-199]) /
   (σ₈[S0-199] − σ₈[LIN-199]).
3. **Production = both z_i for every mode**, 14 runs at 512³ (1024³ is excluded: particles alone need 51.5 GB). Order:
   S0-199, LIN-14.8-199, KX-can-14.8-199, KX-alt-14.8-199, S0-49, LIN-14.8-49, KX-can-14.8-49, KX-alt-14.8-49,
   LIN-400-49, KX-can-400-49, KX-alt-400-49, LIN-400-199, KX-can-400-199, KX-alt-400-199.
4. **Queue.** `compute_queue/heavyq.py` exists, so each run is a queue job:
   `heavyq add --id L1_<tag> --cmd "<run>" --resume-cmd "<run> --resume" --est-gb E --threads 8 --done-file work/<tag>/DONE`,
   with priorities in the order above. Under the queue, the engine exits with `$HEAVYQ_YIELD_EXIT` (75) after its SIGTERM
   checkpoint (0 otherwise, as validated by KR). It writes `work/<tag>/DONE` only on completion. E = 1.15 × the measured peak
   of a 3-step 512³ KX z_i = 199 calibration run (its outputs are not used).
5. **Halo profiles (coordinator request; reported only, no verdict weight)**, at z = 0 in every production run:
   - centres: local maxima (3³ cells, periodic) of the total-mass CIC density smoothed with a Gaussian of σ = 1 cell,
     above 20× the mean;
   - M₁ = total mass within 1 Mpc (physical);
   - greedy exclusion within 1 Mpc, most massive first;
   - classes by M₁: cluster ≥ 1e14 M_⊙, group 1e13–1e14, galaxy 1e12–1e13; if fewer than 10 clusters, also "top50" (the 50
     largest M₁);
   - per class: stacked mean ρ_b, ρ_τ in shells with edges 0.1, 0.2, 0.3, 0.5, 0.7, 1, 1.5, 2, 3 Mpc (physical);
   - dust-to-baryon mass ratio in 0.3–1 Mpc and in 1–3 Mpc (stacked, and the median over halos), against the cosmic Ω_τ/Ω_b.
   Caveat stated in advance: the 512³ cell is 0.285 Mpc (physical) and the PM softening is 1–2 cells, so the 0.3–1 Mpc
   annulus is resolution-limited.
6. **Production scorer `l1_score.py`.** CFG596's flow, with the CFG592 library exec'd unchanged:
   - nodes z = 0, 0.5, 1 of the total-matter particle P(k); k_lo = first bin, k_hi = πN/(4L); support ≥ 0.9;
   - fits with and without IA; robust variants widen2, DESI and noIA (CFG596's "held" variant has no analogue: omitted);
   - `klass` as in CFG592;
   - KX vs S0 at the same z_i; LIN vs S0 reported;
   - T-OWN tooth: inject the run's own P_KX/P_S0 at z = 0 into an S0 mock, and require χ²_min ≥ 9 for "diagnostic", as CFG596;
   - plus the model-B projection variant (F3 K3 style), reported. KiDS is the frozen survey; DES is reported.

## AMENDMENT A4 (PRE-RESULT for production and for a 128³ LOB check, 2026-10-23; after the indicative set, before any production number or any LOB-IC run)

Reason: Q6_v3_class (`rebuild_2026_10_22/Q6_v3_class/README.md`) landed, relayed by the coordinator.
1. **Reading sentence, added to every production reading.** Literal v3's quadratic K has no radiation era: the stiff a⁻⁶ partner
   beats radiation before z = 1854 at μ_K = 14.8, and BBN needs μ_K ≥ 1.84×10⁸ h/Mpc (Q6 §4). So every L1 production result
   belongs to "v3 on a dust background with a yet-unspecified early K", not to the literal theory.
2. **The frozen ICs overstate the linear state.** The frozen LIN/KX ICs come from F3's BSK2 ODE started at a = 1e-3 with
   δ_b = δ_τ ∝ a (§2 ledger, POSITED start). Q6's full Boltzmann LOB model (dust background, literal perturbations, from early
   times) gives R_B = 0.073 at the cap, against the ODE's 0.391. The frozen cells stay unchanged and are reported.
3. **New variant "LOB-IC"** (fix-forward). Same engine, mode, box, phases and step grid as the z_i = 199 cells. Only the
   per-species linear state at z_i = 199 changes:
   - Q6's validated Khronon CLASS binary (`class_khronon`, sha256 3ccb50b2..., PROVENANCE.md), run read-only with Q6's HIGH
     and START×0.25 precision settings, at model B: h, ω_b, A_s, n_s, τ as §2; ω_cdm = 1e-8 and ω_aest = Ω_τh² − 1e-8 (Q6's
     convention); LOB (`aest_K_type` 4, `aest_lambda_c` −1, `aest_K2` = (μ_K h)² Mpc⁻²). A DUST run (`aest_K_type` 0) at the
     same parameters is the normaliser. Outputs mTk at z = 0, 195, 199, 203, synchronous gauge, written to this lane's
     `work/` (not to `_external_data`).
   - δ_b = d_b. δ_τ = (Ω_m d_m − Ω_b d_b − Ω_cdm d_cdm)/Ω_τ from the total-matter transfer, which includes the khronon in the
     patch (aest.patch L518–520).
   - R_s(k) = δ_s^LOB(k, z_i)/d_m^DUST(k, 0). dδ_s/dln a is the central difference between z = 195 and 203. The momentum is
     built from dδ/dln a (as the engine does).
   - T_m(z = 0) for σ₈,lin,box is d_m^LOB(k, 0)/d_m^DUST(k, 0).
   - The sub-horizon N-body reading of synchronous-gauge δ at z = 199 is accurate to O((aH/k)²) ≤ 2e-3 at the box's k_f.
4. **LOB-IC production cells**, appended after the frozen 14 (lower priority; the frozen cells stay unchanged):
   LIN-LOB-14.8-199, KX-can-LOB-14.8-199, KX-alt-LOB-14.8-199, then LIN-LOB-400-199, KX-can-LOB-400-199, KX-alt-LOB-400-199.
   The control is the frozen S0-199. They are scored and read exactly as the frozen cells (same ρ_NL, the same scorer). Both
   IC families are reported, never pooled.
5. **128³ LOB check (indicative, `l1_lob.py`)**: LIN-LOB-199 and KX-can-LOB-199 at the indicative settings, plus K-LOB1, the
   DUST normaliser against this lane's vanilla classy P(k) at z = 0 (|P_DUST/P_classy − 1| ≤ 1e-3 for k ≤ 7 h/Mpc), and
   K-LOB2, which reports the LOB linear σ₈ (z = 0, infinite volume) against Q6's R_B = 0.073 (at Q6's own parameters; it is
   reported, not gated, because the parameters differ). ρ_NL,LOB = (σ₈[KX-LOB] − σ₈[LIN-LOB])/(σ₈[S0-199] − σ₈[LIN-LOB]), with
   the frozen reading bands. MUTATE: δ_τ taken from d_b (the khronon's own transfer dropped) must FAIL K-LOB3, the check that
   the IC's khronon δ equals the CLASS-derived one to 1e-6.

## AMENDMENT A5 (PRE-RESULT, 2026-10-23: a resolution ladder that fits now; before any ladder run)

Reason (coordinator): the 512³ cells cannot start yet (free + inactive memory is about 35 GB, and the queue needs 44 GB), and
halo cores, where x > 1, are unresolved at 128³.
1. **Ladder cells.** μ_K = 14.8 h/Mpc, z_i = 199, F3-ODE ICs, L = 100 Mpc/h, model B, `--halos`.
   - **NSEED = 512 at every N**, so the rungs share phases with the frozen 512³ cells. The 128³ indicative set used
     NSEED = 256, so it is not a rung. The ladder adds a 128³ NSEED-512 rung instead.
   - Rungs: N = 128, 256 and 384, each with S0, LIN, KX-can and KX-alt. Plus LOB-IC LIN and KX-can at 384, with S0-384 as
     their control.
   - The frozen 512³ cells (A3, A4) are unchanged.
2. **Statistics per rung** (definitions as §4 / A3 / A4):
   - σ₈,PM(z = 0), total and per species;
   - ρ_NL per footing;
   - halo profiles (reported);
   - the KiDS score from `l1_score.py --dir work/prod` wherever N_kept ≥ 10. k_hi = πN/(4L) is 1.0, 2.0 and 3.0 h/Mpc at
     128, 256 and 384.
   The trend 128 → 256 → 384 (→ 512) is **reported as convergence only**: no verdict, never pooled with the 512³ cells. The
   frozen reading bands for ρ_NL are quoted per rung with the word "indicative".
3. **est_gb, measured** (3-step KX-can, z_i = 199, 8 threads; peak phys_footprint from `/usr/bin/time -l`):
   - 128³: 0.539 GB; 256³: 2.727 GB.
   - Two-point fit: 0.226 GB + 149 B per cell. The constant is the interpreter baseline, and 149 B per cell sits below the
     declared formula's 224 B.
   - 384³ extrapolates to 8.66 GB, so **the 384³ calibration is skipped**. The formula's upper bound there is 13.0 GB.
   - 512³ extrapolates to 20.2 GB; the queued est of 35 is unchanged.
   - est_gb = 1.2 × measured or extrapolated peak: 0.65 / 3.3 / 10.4 GB. The KX value is used for every cell at a given N.
   - The NSEED-512 white-noise caches for N = 128, 256 and 384 are pre-generated in `work/prod`. That step peaks at 2.20 GB
     for about 1 s and was done here. So the queued ladder jobs never run the 512³ noise transform.
4. **Engineering fix, found by the 256³ calibration.** The guard thread probed swap through `subprocess` (a fork) every 2 s.
   pocketfft shuts down its worker pool around a fork, so with workers > 1 a transform could fail ("Work item submitted after
   shutdown"). The swap probe now uses `sysctlbyname` through ctypes, with no fork. Numerics are unchanged; validation used
   one thread.
   - Re-checked at 8 threads (64³, KX, z_i = 199): SIGTERM → exit 75 in 0.3 s → `--resume` gives a sha256 and P(k)
     bit-identical to the uninterrupted run.
