# CFG497 FROZEN CRITERIA: does a binding-energy selection rule, with a threshold NOT set by S, select S × M_b of cold?

Written and committed alone, before any script or number of this lane. κ = ½ is FITTED. Both footings (a₀ = 9.3603e-11 and
1.1312e-10 m/s²) are scored separately and never pooled. No dark-matter particle is added: the cold fluid ("cold energy")
still needs its mass, and its cosmic amount S = Ω_c/Ω_b = 5.364 is an input. This is not "theory closed".

## The question

PAPER45 v2.1's growth fix rests on the supply postulate: each galaxy settles S × its ORIGINAL baryons of cold (edge
5.8498 r_M). CFG461, 462, 488, 490 and 494 did not derive it. CFG494 left one open route: in CFG118's secondary-infall model
the MOST-BOUND S M_b of cold at the dissipation time t_d is 97–100% Lagrangian partner material, because binding energy keeps
Lagrangian order. But S was inserted as the threshold.

Here: is there a selection rule "settle the cold whose specific binding energy at t_d is below E_thr" with E_thr set by
something other than S, that selects S M_b,orig without inserting it?

## Model (offline numerics; no downloads)

- H-N: CFG118's point-core secondary infall in Planck18 ΛCDM (core = the galaxy's original baryons M_b, present from z = 100;
  cold shells at Ω_c ρ_crit; other baryons smooth). The worker is a COPY of CFG488's `cfg488_infall.py` in this folder
  (CFG118's `shellcore.c` compiled read-only to a temp dir), changed only so that S and the core mass are arguments.
  N = 20,000 shells, q = r_peri/r_ta ∈ {0.05, 0.1, 0.2} (the record bracket), one run per q at M_sim = 1e10 M☉.
- Self-similarity: H-N is Newtonian with no a₀, so radii scale as M^(1/3), velocities as M^(1/3), energies as M^(2/3), times
  unchanged. Thresholds that carry a₀ break this; they are evaluated per mass by rescaling the run (r_phys = r_sim (M_b/M_sim)^(1/3)).
- t_d = 2 t_ta(k_b), the first collapse of the outermost partner shell (CFG494; z = 3.51). Positions at t_d and t_d(1 + 1e-6);
  v by finite difference (CFG494's method); j² from the integrator.
- Specific energy E = v²/2 + j²/(2r²) + Φ(r), Φ = core + shells (each shell's own half, CFG494) + smooth-baryon and Λ
  background terms Ω_b H₀² r²/(4a³) − Ω_Λ H₀² r²/2. "Apocentre inside r_x" means E < Φ(r_x).
- Selected mass M_sel = cold mass with E < E_thr; ratio s_sel = M_sel / M_b,orig. Purity Π_sel = partner fraction of the
  selected cold (labels as CFG494).
- Cells: M_b = 1e9, 10^10.5, 10^11.5 M☉ × 2 footings × 3 q.

## Candidate thresholds (declared now, before any selected mass is computed; all scored, none dropped)

Class A: a₀-free (self-similar: the same s_sel at every mass and on both footings, by construction).
- **A1 VIR200**: E < Φ(R_200(t_d)), R_200 = mean enclosed (core + cold) density 200 ρ_crit(t_d). The 200 is a convention.
- **A2 VIRTH**: E < Φ(R_ta(t_d)/2), the top-hat virial radius of the shell turning around at t_d.
- **A3 CATCH**: E < Φ(R_ta(t_d)), bound inside the current turnaround radius (anchor; CFG494's LP-H/inf at t_d was 1.57 S M_b by sphere).
- **A4 CORE-BOUND**: v²/2 + j²/(2r²) − G M_core/r < 0, bound to the baryons' own gravity (the "baryons' own binding energy"
  reading). Reads the baryon field apart from the total: species split.

Class B: carries a₀ (the law's own scales).
- **B1 Y1-FIELD**: r_x = the outermost radius where the TOTAL infall field g(r, t_d) = ν(1) a₀ (the law's total field at y = 1;
  ν_mono(1) = 1.582); E < Φ(r_x).
- **B2 A0-FIELD**: as B1 with g = a₀.
- **B3 Y1-RM**: r_x = r_M = √(G M_b/a₀) (the baryons' own Newtonian field = a₀); E < Φ(r_M). Species split.
- **B4 LAW-TA**: r_x = the law's own turnaround radius (cfg100 `r_ta_law(M_b, a₀, z_d)`), the law's turnaround in energy space.
- **B5 VF-SPEED**: r_x = the outermost radius where the infall circular speed √(G M(<r)/r) = V_f = (G M_b a₀)^(1/4). Species split (M_b).
- **B6 LYNDEN-BELL**: degeneracy threshold of violent relaxation. For a cold fluid the fine-grained phase-space density is
  unbounded unless a quantum mass is supplied; with no particle this threshold is NOT FORMULABLE and scores FAIL. (Declared so
  it is not silently dropped.)

Restatement controls (reported; not candidates):
- **R1 BARYON-E**: E < E(k_b, t_d), the energy of the outermost dissipated-baryon shell (reads the label).
- **R2 TOP-S**: the most-bound S M_b (S inserted; CFG494's energy rank).

## Criteria

**(M) Match.** s_sel ∈ [4.828, 5.900] (5.364 ± 10%) in every cell: 3 masses × 2 footings × 3 q, with Π_sel ≥ 0.9. A match at
one mass, one footing or one q only FAILS (tuning).

**(T) MUTATE tracking — the frozen requirement is TRACK.** `CFG497_MUTATE=1` sets Ω_c/Ω_b = 2 × 5.364 = 10.728 at fixed Ω_m
in the initial conditions (CFG488's convention: shell density Ω_c and the smooth baryons change; core = M_b,orig unchanged;
the partner becomes the innermost 10.728 M_b of cold). A genuine derivation must select s_sel ∈ [9.655, 11.80] (10.728 ± 10%)
in every cell with Π_sel ≥ 0.9.
- Why TRACK: the postulate is "the cosmic share", settled = (Ω_c/Ω_b) M_b for whatever Ω_c/Ω_b; the edge and the growth fix
  depend on f_b through it (CFG488's f_b-test). A rule that reads binding order selects the partner set, and the partner set
  doubles. A rule that gives 5.364 at the true S but not 10.728 at 2S matches a number, not the share: COINCIDENCE, FAIL.
- Expectation written now: the infall dynamics feel S only through Ω_c (+8.5% under MUTATE), so S-free thresholds should barely
  move; only R1/R2 should track.

**(iii) G9.** PASS iff E_thr is a functional of the TOTAL gravitational field/potential and the parcel's own orbit only, with
a₀ (and the committed kernel) the only constants: no baryon labels, no separate baryon field or M_b, no S or f_b.
- A4, B3, B5 read M_b or the baryon field separately: G9 FAIL (species split, CFG462's F-H class). B4 reads M_b through the
  law's ν(g_N[b]) before anything has settled: G9 FAIL. R1 reads the label: FAIL. A1–A3, B1, B2: PASS by construction.
- Epoch: t_d is inherited from CFG494 and is keyed to the partner boundary shell, i.e. to the label. Reported: s_sel at
  t_ta(k_b) and at z = 2. If a candidate passes (M) at t_d but moves by more than 10% at both other epochs, it is
  "epoch-keyed" and can at most be DERIVES-COND.

**(iv) Constants.** Counted per candidate: A1 1 conventional number (200); A2 1 structural number (½, virial); A3 0; B1 0
(the kernel's ν(1)); B2 0; others listed. A threshold containing S or f_b is a RESTATEMENT and FAILS.

**Bonus (scored per candidate, not needed for DERIVES):**
- (i) Clusters: settled = min(ν_cl − 1, s_sel(M_cl)) by free inside-out fill; u = 1 − settled / x_T15 (CFG453 cluster medians,
  b = 0 and 0.3) inside [0.433, 0.628] canonical / [0.368, 0.584] alt (the record range recomputed from CFG453 as CFG494).
  For class-B candidates M_cl,b = 1e14 M☉ (RECALLED, U), with 10^13.5–10^14.5 reported.
- (ii) Edge: x_edge from the point-host ν_mono phantom holding s_sel(M) M_b; KiDS lensing-weighted median x_edge/r_ta over
  CFG413's lens groups (CFG488/494 grouping) in [0.3, 0.5] on both footings; CFG485 R8 early-type χ² ≤ 12.59 on both
  footings. s_sel(M) on a grid log M = 8.0–12.5 (class B), interpolated in log.
- Note written now: a candidate that passes (M) settles S M_b, so its edge is 5.85 r_M and it inherits the postulate's
  lensing misses (KiDS 0.038, early-type χ² 30.5 / 38.1). (ii) can pass only for a candidate that fails (M).

**Lane verdict.**
- **DERIVES** iff one candidate passes (M) AND (T) AND (iii), with no S or f_b in its threshold (DERIVES-COND if epoch-keyed).
- Otherwise **NOT DERIVED**, with the candidate table; a candidate passing (M) but failing (T) is labelled COINCIDENCE.

## Controls (exit 0 of the main run iff all pass)

- K1: H-N reproduces CFG494/CFG118: M_ta/M_b = 23.632 ± 1%, r_ta0 = 507.94 kpc ± 1%, partner = S M_b to 1e-9, z_d = 3.51 ± 0.02.
- K2: CFG494's energy-rank purity (its Φ, no background terms) reproduced: 0.9721 / 0.9779 / 0.9996 ± 0.01.
- K3: x_e = 1/ln(1 + 1/S) = 5.8498 and the ν_mono point phantom there equals S M_b to 1e-6.
- K4: KiDS median at 5.8498 r_M reproduced: 0.0377 / 0.0327 ± 0.001.
- K5: CFG485 R8 early-type χ² at 5.8498 r_M reproduced: 30.5 / 38.1 ± 0.5.
- K6: self-similarity: a direct q = 0.1 run with the core at 1e9 M☉ gives the rescaled B2 and A1 s_sel within 2%.

## MUTATE (`CFG497_MUTATE=1`, writes *_MUTATE.*)

As in (T). Teeth: R1 and R2 (which read the label / insert S) must move to 10.728 ± 5% — this shows the mutation reaches the
selection machinery, so a non-moving candidate is a real non-track. Exit 1 iff the teeth are detected.

## Outputs

`cfg497_infall.py` (copied worker), `cfg497_binding.py`, `cfg497.out`, `cfg497_MUTATE.out`, `cfg497_results.json`,
`cfg497_results_MUTATE.json`, plain `README.md`. Committed locally; not pushed.
