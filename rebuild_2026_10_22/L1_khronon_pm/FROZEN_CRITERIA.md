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
