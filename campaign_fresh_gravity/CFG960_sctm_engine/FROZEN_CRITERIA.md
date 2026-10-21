# CFG960 FROZEN CRITERIA: the SCT-M structure-formation engine (design and ≤ 128³ validation)

Committed ALONE, before any CFG960 script, engine file or number exists. Date 2026-10-21. Block CFG960–969 (LEDGER reservation
606c4c754). This file freezes the PM realisation of CFG953's SCT-M and its validation gates. The 1024³ shear test is pre-registered
separately in `FROZEN_CRITERIA_1024.md`, committed alone after the validation below and before any 1024³ job. This lane starts no
1024³ job.

**Settings.** κ = ½ FITTED. Footings canonical a₀ = 9.3603e-11 and alt 1.1312e-10 m/s², run and scored separately, never pooled.
Cold energy is the framework's own component: its mass is required, no particle species. Framework-native inputs and raw data only:
no HMcode, BAHAMAS, ΛCDM mass function or other ΛCDM nonlinear yardstick enters any verdict. Not "theory closed" whatever the
outcome; nothing here can say the data favour the framework. Any change after this commit is a dated, labelled amendment.

## 0. Question and what was read

**Question.** The class-A engine (theory-v2: CFG650 M1 + M2 + M3 with the E-rules, E8 relocation) passes raw KiDS-1000 on both
footings with native inputs (NC1x −10.08, NC2x −9.39; CFG909: class ROBUST, size amplitude-driven). That engine has no physical
parent (CFG947: no exact non-local parent; CFG955: E8 is not the τ → 0 limit of any locally mass-conserving kinetic theory).
CFG953's SCT-M is a galaxy-scale-consistent theory (CONDITIONAL: C-E, C-DF; open C-MR, C-c; clusters FAIL in CFG954). Does SCT-M,
growing structure itself, still pass raw KiDS? A pass gives the shear result a parent; a fail means the pass depends on the
parentless rules.

**Read before freezing (design stage, not blind to the record).** LEDGER rows CFG650, CFG654-A2/A3, CFG909, CFG947, CFG953–955,
CFG960 reservation; CFG654 README, FROZEN_CRITERIA + A1/A2/A3, its engine, launcher, scorer and validation script (Read tool only);
CFG953 README, DERIVATION, FROZEN_CRITERIA; CFG954 README; CFG955 `FROZEN_CRITERIA_KT1024_DRAFT.md` (cost baseline);
`_external_data/overnight_chain/chain7b.sh`; the NC1x / NC2x / NCS0 run JSONs (runtime, peak RSS). No SCT-M PM number exists at
any resolution.

## 1. Engine: `cfg960_sctm_pm.py` = the CFG654 engine + an SCT-M source sector

- The CFG654 engine file (sha256 7058f4333b8d4597…31c6, the version that ran NCS0 / NC1x / NC2x) is IMPORTED read-only by a path
  assembled in code, its sha256 asserted at start. Nothing in CFG650 / CFG654 is edited. Reused unchanged: native_cmb inputs and
  background (A1), ICs (`initial_conditions_lean`), step grid (150 steps), CIC deposit and interpolation, FFT mesh, the finder
  (`cover_peaks`), the census catchments and M3 (`cover_balls`, `expel_m3`), `fcond_of`, `nu_mono`, `a0_code` (FLAT branch, as
  NC1x / NC2x), P(k) and gravitating-field measurement (`measure_pk`, `grav_field`), snapshots (zi, z1, x0.7548, z0.5, x0.2562, z0).
- Off: E4 (the global QUMOND phantom), E6–E8 (deficit, edge, zero-sum draw), the tidal switch, M1's supply pool, M4.
- The run JSON keeps the engine's structure (`snap[...]["k", "P", "P_grav", ...]`, `foot`, `np`, `L`, `cfg654_inputs`), so the
  frozen CFG654 scorer reads it.

### 1.1 SCT-M rules as realised in the PM code

| id | rule (CFG953 source) | PM realisation |
|---|---|---|
| S1 | R0/R2 gravitating density ρ_b + ρ_c,unl + Σσ_q | ρ_g = Σ_i w_i m_p W_CIC(x − x_i) + Σ_q σ_q + M3's re-placement; w_i = 1 for unlabelled and pending particles, w_i = f_b for converted particles (their cold share 1 − f_b is inert). Poisson exactly as S0: φ_k = −1.5 Ω_m δ_g,k / (a k²) |
| S2 | R1 domain birth at first turnaround, no RMIN, labels latched | at each census refresh (every 10th force call from the first, the engine's census cadence): peaks = `cover_peaks` on the all-particle CIC density (E3: top-hat mean ≥ Δ_ta(z) ρ̄_m about a mesh peak; native Δ_ta table; radii geomspace(dx, 8, 14) Mpc/h); every peak with r_ON ≥ dx is used. Cells of the union of balls (radius r_ON) are partitioned by CFG647's rule (smallest d/r_ON, ties to the larger r_ON). For peak h: T_h = particles whose NGP cell h owns, U_h = the unlabelled ones. If U_h > T_h/2, a new domain is born at h and all U_h particles take its label as PENDING. Otherwise h belongs to the domain holding the most labelled particles in h's cells, and its unlabelled particles convert into that domain at once (R1: matter entering q's turnaround region joins q) |
| S3 | R4 birth ramped over τ_conv = free-fall time at turnaround | pending particle i of domain q converts at t_b,q + u_i τ_q; u_i ∈ [0, 1) = splitmix64 hash of the particle's global index (random order, as CFG953's toy); τ_q = (π/2) (a_b³ / (Ω_m Δ_ta(z_b)))^½ / H0; cosmic time from the native E(a). Due conversions are executed at every step |
| S4 | R4 conversion algebra | M_c += (1 − f_b) m_p; X_q → mass-weighted mean (minimal image); P_q += (1 − f_b) m_p v_i, v_i the code momentum at the leapfrog half step (the time level of P_q); the particle's weight w_i → f_b |
| S5 | R3 own baryons (the M2 condensed source = retained baryons) | every particle labelled q (pending or converted; labels resolved to the merge root) carries own retained baryons f_b f_d,i m_p. f_d is M2's float16 condensed fraction, raised at each refresh (irreversible max) to `fcond_of(r_ON,h, Δ_ta, a)` of the partition peak owning the particle's NGP cell (M2's phase law, CFG640 cooling, census floor 0.10, no RMIN) |
| S6 | R3 SCT-M monopole body, cut at the supply root | every step, each live domain with M_c > 0: M_b,q(<r) about X_q from 48 log radial bins (edges dx/16 … L/2, plus an inner bin from 0 and an overflow bin), linear in r³ inside a bin; y(r) = G M_b(<r)/(a r)²/a₀ in the engine's units; M_σ(<r) = min{(ν_mono(y) − 1) M_b(<r), M_c}; r_e = supply root (bisection, relative tolerance 1e-10). Fallbacks (counted, reported): no root before L/2 → remainder in a last shell at L/2; M_b = 0 → point mass |
| S7 | painting | r_e ≤ dx/2: one point (X_q, M_c). Otherwise n_r = ⌈2 r_e/dx⌉ equal-width shells; shell mass ΔM_σ at the mid radius r̄ on an antipodal-symmetric set (Fibonacci hemisphere + antipodes) of n_a = max(6, 2⌈8π r̄²/dx²⌉) directions, shell k rotated by k × the golden angle; CIC deposit of the points with the particles' CIC. The point set carries mass M_c and centroid X_q exactly |
| S8 | R4 M_c V̇ = ∫σ g | F_q = Σ_points w_p g(x_p), g the same CIC-interpolated mesh acceleration the particles receive; V_q and X_q advance with the particles' KDK factors |
| S9 | R7 merges (bound fraction < ½ or baryon-centroid coalescence; inelastic) | at each refresh, after births and accretion: per domain the own-baryon centroid X_b and velocity V_b (f_d-weighted), the own-baryon half-mass radius r_h about X_b, and the bound fraction f_bound = own retained baryon share with ½\|v − V_b\|² + Φ < 0 (v physical, Hubble flow included; Φ the spherical potential about X_b of the domain's own gravitating particle mass, converted f_b and pending 1, plus its body profile M_σ, taken about X_b). host(p) = the domain of the largest-r_ON peak, not p's own, whose ball contains X_b,p. For (p, host(p)) with s / l the smaller / larger by own retained baryons: merge s into l iff f_bound,s < ½ or \|X_b,s − X_b,l\| ≤ r_h,l. Mass, centroid and momentum add; pending particles keep their times and convert into the root; no blend (CFG953's primary toy run) |
| S10 | R1 in situ | a peak with a labelled majority creates no domain and no body; its matter keeps its label |
| S11 | R2 labelled dust inert | converted particles still move geodesically (they carry the baryons); their cold share sources nothing |
| S12 | M3 unchanged | census catchments (`cover_balls`, RMIN 0.78125 Mpc/h), e_k = f_b (1 − f_ret,census,k)(1 + δ_all), Gaussian re-placement with σ = r_ON,k, applied to the gravitating source (`expel_m3` on the all-particle density; its increment is added to δ_g) |
| S13 | R5, R6, R8 | spin S_q and E_int are bookkeeping charges with no NR gravitational effect: not tracked. Retardation: NR limit (instantaneous), as every engine run. Bodies are never stripped; no dynamical-friction term beyond what the PM field gives |

### 1.2 Where SCT-M is underspecified for a PM code (declared choices)

| # | gap | choice |
|---|---|---|
| U1 | domains below the mesh (CFG953: peaks at L* = 24 pc) | domain floor r_ON ≥ dx (the finder's smallest radius): ≈ 2e9 h⁻¹ M☉ of turnaround mass at 1024³, ≈ 1e12 h⁻¹ M☉ at 128³. Sub-floor systems are not domains; their dust stays gravitating until it enters a resolved turnaround region, then converts there (S2). The 128³ preview is therefore not representative of 1024³ |
| U2 | "matter density" for the turnaround test | all particles, including inert labelled dust (it is matter; the test is kinematic) |
| U3 | which domain a re-found peak belongs to; in-situ test | the labelled-majority rule of S2 / S10 |
| U4 | conversion cadence | ramp conversions every step (S3); region entry at refreshes (every 10 force calls, as the census) |
| U5 | "own baryons" | M2's condensed (retained) baryons of the domain's labelled particles (S5), as the task fixes |
| U6 | rigid sphere on a mesh | quadrature points + CIC (S7); a body with r_e ≤ dx/2 is a CIC point mass |
| U7 | body overlap | linear superposition, no exclusion (members add as Newtonian mass, CFG953 §4) |
| U8 | stripping | none (CFG953 cost 7); the body follows M_b,q(<r) of all its own baryons, wherever they are |
| U9 | R7 details | host via turnaround balls, bound fraction as S9, no blend |
| U10 | species | single-species particles carry f_b baryons and 1 − f_b cold energy and co-move (collisionless baryons, as in every engine run); a converted particle's baryons keep gravitating at weight f_b |
| U11 | kernel | ν_mono (the engine's kernel and NC1x / NC2x's; CFG953's secondary kernel, same law structure) |
| U12 | M3 and momentum | M3 moves source mass without moving particles, so the momentum book is exact only with M3 off. M3 is kept unchanged (as the task fixes) and its momentum effect is reported |
| U13 | the census supply | M_c is the converted particle cold mass (no census N enters S6); N enters only through f_d's census targets |

## 2. Validation (≤ 128³; every gate decided from committed JSON)

**Jobs** (L = 100 Mpc/h, N = NSEED = 128, seed 359, RMIN 0.78125, native_cmb, lean, no spill, ONE thread, nice 10, one process at
a time, in-script RSS guard 1 GB):

| job | content |
|---|---|
| VS0 | the CFG654 engine's own S0 at 128³ (reference control) |
| VK | SCT engine, conversion OFF (births, pending labels, f_d, merges all active; no particle ever converts), M3 OFF |
| VC | SCT on, M3 OFF, canonical (conservation run) |
| VSC | SCT on, M3 on, canonical (= SC1x at 128³) |
| VSA | SCT on, M3 on, alt (= SC2x at 128³) |
| VMU | VSC with a planted wrong body mass: painted body mass × 0.5 (MUTATE) |
| LAW | static isolated host on a 128³ mesh: box 6.4 Mpc/h (M_b = 1e12 h⁻¹ M☉, M_c = 20 M_b, deep regime) and 0.64 Mpc/h (M_b = 1e12, M_c = 2 M_b, y ≈ 0.1–3), Plummer baryons, both footings, z = 0; the engine's own profile, body, CIC, Poisson and interpolation functions |
| SCOREK | the CFG960 scorer wrapper re-scores the stored NC1x and NC2x vs NCS0 |

**Gates (all must pass before `FROZEN_CRITERIA_1024.md` is frozen; a failure is reported, not hidden):**

| gate | line |
|---|---|
| V-K | VK vs VS0: P and P_grav at every snapshot and k identical to ≤ 1e-6 relative (expected 0: same deposit and Poisson path) |
| V-IC | VSC / VSA / VC zi particle P(k) equal VS0's bit for bit (same ICs) |
| V-MASS | VC, VSC, VSA, every step: \|Σ_i w_i + Σ_q M_c − N\|/N ≤ 1e-12; \|Σ painted − Σ M_c\|/N ≤ 1e-10; \|mean δ_g\| ≤ 1e-5 |
| V-MOM | VC (M3 off): max over steps of \|P_book − P_book,0\|/P_scale ≤ 1e-5 per component, P_book = Σ_i w_i m_p v_i + Σ_q M_c V_q, P_scale = Σ_i w_i m_p\|v_i\| + Σ_q M_c\|V_q\|; event algebra (conversions, merges) exact to ≤ 1e-12 P_scale in every SCT run. VSC / VSA: reported only (U12) |
| V-N1 (n = 1) | VSC and VSA: P_grav / P_VS0 within 3% in the two lowest k shells at z = 1, 0.5, 0; and VSC's fundamental-mode P_grav growth from z_i over the native D² within 5% at z = 1, 0.5, 0 (CFG654 V-N2 form) |
| V-LAW | LAW, each box and footing: radial g (64 directions per radius) against g_law(r) = ν_mono(y) ḡ_own (r < r_e) and Kepler with M_b + M_c (r > r_e), each minus the periodic background term (1.5 Ω_m/a²) μ_tot r/(3L³): median \|g/g_exp − 1\| ≤ 0.02 and max ≤ 0.05 over 4 dx ≤ r ≤ 0.85 r_e; median ≤ 0.02 over 1.3 r_e ≤ r ≤ min(2.5 r_e, 0.4 L). K: with the body off, the same test against the baryons' Newtonian field passes the same lines |
| V-MUT | VMU vs VSC: \|P_grav,MU/P_grav,VSC − 1\| ≥ 0.01 at each of k = 0.3, 0.5, 1 h/Mpc (z = 0), and the mass monitor flags \|Σ painted − Σ M_c\|/N ≥ 1e-3. Separate outputs; exit 1 when both bite, 2 otherwise |
| V-SCORE | SCOREK reproduces `cfg654_native_results_NC1x.json` / `_NC2x.json` (χ²_S0, χ²_F, Δχ², robustness, DESI, class, benchmark) and the stored MUTATE T-OWN / NZ1 to ≤ 1e-9 |
| V-MEM | every validation process peaks below 1 GB RSS |

**Reported, no gate:** the 128³ PREVIEW P_grav,VSC/P_VS0 and P_grav,VSA/P_VS0 at k = 0.3, 0.5, 1 (z = 0; also z = 0.5, 1), labelled
"PREVIEW, NOT A VERDICT" (128³ cannot decide anything: the domain floor is ≈ 1e12 h⁻¹ M☉ and k = 1 is at the support limit); VC
vs VSC (the M3 effect); per snapshot: live domains, births, merges, in-situ peaks, converted / pending / labelled mass fractions,
r_e in dx (median, max), bodies painted as points, fallbacks, f_d mean, the mass and momentum books; per-stage runtime and peak RSS,
used for the 1024³ cost estimate.

## 3. Scorer for the 1024³ test (frozen here, used unchanged by `FROZEN_CRITERIA_1024.md`)

`cfg960_score.py` imports the frozen CFG654 scorer (`load_lib`, `build`, `klass`, `CMB_GATE`) by path and copies its production
control flow verbatim, changing only file locations (framework run from `_external_data/cfg960_work/<JOB>/`, control
NCS0 from `_external_data/cfg654_work/NCS0/`, outputs in this folder). Statistic, data, covariances, n(z), published and support
cuts, nuisances, IA marginalisation, robustness set {widen2, noIA, held, LOC}, DESI reported only, T-OWN and NZ1 (MUTATE first),
classes and benchmark are CFG654's (FROZEN_CRITERIA + A1). V-SCORE certifies the identity.

## 4. Compute and repository rules

- Validation: OMP_NUM_THREADS=1, `nice -n 10`, one process at a time, in-script RSS guard 1 GB; numpy / scipy only; no downloads.
- No repo-wide grep or find; no running process touched; no file of another lane edited; LEDGER and THEORY_CANONICAL untouched.
- Separate outputs per job and per mode (`_MUTATE`); every quoted number comes from a committed JSON.
- Outputs: `cfg960_validate.{out,json}`, per-job run JSONs copied from `_external_data/cfg960_work/<JOB>/` into `runs_128/`,
  `cfg960_law.{out,json}`, `cfg960_scorek.{out,json}`.
- The 1024³ jobs SC1x / SC2x are defined in a NEW runner (`run_960.py`) and a gate script; never by editing CFG654's launcher. They
  are not started by this lane.

κ = ½ FITTED; footings never pooled; cold energy mass required; no particle species; not theory closed.
