# L1_khronon_pm: a Khronon-native particle-mesh engine for v3, validated at small scale

## Verdict: RUNNABLE NOW

- **The engine is built and validated.** The validation passes 6/6. KB passes only on its post-result statistic (AMENDMENT A2).
  **KB as frozen FAILED** (0.0345 / 0.0356 against 0.02). That failure is printed on every run, and its cause is stated below.
- **Indicative 128³ result (not a verdict).** v3's full nonlinear J_x term does **not** restore growth at μ_K = 14.8 h/Mpc
  in any of the three initial-condition sets. Where it acts at all (z ≈ 200, x up to 20), it **lowers** σ₈.
- **Production has not been run.** This session's permission system blocked enqueueing the 512³ jobs. The coordinator will
  enqueue them with the owner's go-ahead. The exact commands are in **ENQUEUE** below.
- **Reading sentence for every production result (A4, from Q6).** Literal v3's quadratic K has no radiation era: the stiff
  a⁻⁶ partner beats radiation before z = 1854 at μ_K = 14.8, and BBN needs μ_K ≥ 1.84×10⁸ h/Mpc. So every L1 result
  belongs to **"v3 on a dust background with a yet-unspecified early K"**, not to the literal theory.

κ = ½ is FITTED. The footings (canonical 9.3603e-11, alt 1.1312e-10 m/s²) are never pooled. There is no dark-matter particle:
the cold sector is BS K(Q) dust ("cold energy"). Not "theory closed". Nothing here says the data favour the framework.

## 1. What the engine is (FROZEN_CRITERIA §1)

F3 §6 writes v3's field equation in its static form, ∇·[μ(|∇ψ|/a₀)∇ψ] + μ_K²ψ = 4πG(ρ_b + δρ_K). The engine runs the
native **dynamical** form: BS24's post-Newtonian system, as transcribed in BSK1 (`real_research/bs_khronon_2026/`).
- **Metric potential.** ∇²Φ = 4πG(ρ_b + ρ_τ), sourced by all mass.
- **Hold equation.** ∇·[(1 − μ(x))∇Ξ] − μ_K²Ξ = 4πGρ_τ, with J = J_x, μ = x/(1+x) and x = |∇Ξ|/a₀.
- **Forces.** Baryons are kicked by −∇Φ. The khronon (K(Q) dust) particles are kicked by −∇(Φ − Ξ).

**Why this form.**
- Its static limit is exactly F3 §6's AQUAL equation. The K sector is already inside it, as the phantom.
- Read literally, F3 §6 counts the K(Q) sector twice: once as the μ_K² term and once more as a separate source with its
  own pressure.
- Its linearisation on FRW is F3's BSK2 kernel (J_x) and F3's Jeans kernel (J = GR).

**What the engine does not contain.** No settling, relocation, catchment or f_ret rule. No QUMOND phantom. No ν_mono.

**Solver and modes.**
- The hold equation is solved by an iterative FFT fixed point with Anderson mixing, to a relative tolerance of 1e-6.
  Every call converged in every run here.
- Modes: KX (v3), LIN (J_Y ≡ −1, the linearised theory), GRJ (J = GR at finite μ_K), S0 (dust control).

**Engineering.**
- The engine is preemptible: SIGTERM or SIGINT leads to a checkpoint at the next step and an exit (75 under heavyq).
- Checkpoints roll every 10 steps. `--resume` is bit-identical and exits 0 at once when the run is DONE.
- Writes are atomic: fsync, then `os.replace`.

## 2. Validation (`l1_khronon_pm.py`: 6/6 PASS; MUTATE 2/5, exit 1)

| check | result | line |
|---|---|---|
| K0: reproduce F3 K4 | BSK2 0.39080, Jeans 0.12055 (F3's own) | 1e-3 |
| X0: pre-flight | flag raised (below) | computed |
| KA: GR limit vs the copied CFG596 S0 engine, 64³ | max\|ΔP/P\| 8.7e-5 at z = 0; σ₈ 0.8499 = 0.8499 | 0.02 |
| KB: linear growth vs ODE, 64³, ε = 0.01 (A2 statistic) | ≤ 1.2e-3 | 0.02 |
| KB-frozen (bin-mean ODE) | **FAIL** 0.0345 / 0.0356, printed, not counted | 0.02 |
| KC: static point mass, 128³ | AQUAL vs law 3.4e-4 / 3.5e-4. PN equilibrium: baryon 3.7e-4 / 4.1e-4; khronon net force 5.9e-3 / 7.9e-3 (can/alt) | 0.01 |
| KR: SIGTERM mid-run, then `--resume` | exit 0 after 0.3 s; bit-identical sha256 and P(k) | bit-identical |

- **MUTATE** (no khronon in Poisson; no hold; standard μ plus a swapped hold) fails KA, KB and KC.
- **KB, why the frozen line fails** (A2, post-result):
  - in the lowest bins, the frozen line evaluates the ODE at the bin-mean k, while the estimator weights modes by
    |δ(z_i)|². Put through the same estimator, the deviation is 3e-4;
  - near the grid scale, the PM's own force deficit (S0's PM/ODE growth falls to 0.83) does not cancel against the
    weakly coupled khronon. Calibrating that deficit on the S0 run alone removes it.
- **KC cross-check.** An independent Anderson AQUAL solve agrees with the projection solver to 4.6e-5 in every shell.
- **Reported only.** The Jeans (GRJ) mode is not validated above k ≈ 0.6 h/Mpc: its oscillation phases are not
  reproduced. Production does not use it.
- **Memory.** The validation peaked at 2.27 GB RSS (disclosed in A2; the owner had lifted the 1 GB limit).
- **Engine copy.** `ref_cfg596_pm.py` is a verbatim copy of CFG596's engine (sha256 1c207fa5…).

## 3. X0: the J_x nonlinearity is strong **before** z_i (`l1_khronon_pm_results.json` X0)

The linear rms of the hold-field argument, x = |∇Ξ|/a₀, along F3's BSK2 solution (k ≤ 4 h/Mpc):

| z | canonical | alt |
|---|---|---|
| ≈ 1000 | 11.2 | 9.3 |
| 199 | 0.78 | 0.65 |
| 49 | 0.049 | 0.041 |
| 0 | 3e-6 | 2e-6 |

- **So the nonlinear term acts mainly before z ≈ 200.** That is earlier than the frozen z_i = 49, so the frozen rule added
  the z_i = 199 runs.
- **The quadratic-K background stops being dust there.** Q̄ − 1 is 1.5e-3 at z = 199 (w = 7.6e-4) and 0.19 at z ≈ 1000
  (w = 0.087). At F3's a = 1e-4 start it is 191 (w = 0.99, stiff).
- **No run here covers z ≈ 1000 → 200.**
- **The direction is set by the PN structure** (BSK1 M4, record). Where x > 0, the hold's response is ω² ∝ k²f_θ − μ_K²
  with f_θ = μ + xμ′ > 0. That adds Jeans-like support, so it cannot add attraction.

## 4. Indicative 128³ set (`l1_indicative.py`, `l1_lob.py`; not a verdict)

Setup: L = 100 Mpc/h, model B (CFG886 background), μ_K = 14.8 h/Mpc, the same phases throughout, σ₈ at z = 0.

| ICs | S0 | LIN | KX canonical | KX alt | linear (box) | ρ_NL |
|---|---|---|---|---|---|---|
| F3 ODE (from a = 1e-3), z_i = 49 | 0.8733 | 0.3212 | 0.3211 | 0.3212 | 0.3112 | −0.0002 / −0.0002 |
| F3 ODE, z_i = 199 | 0.8746 | 0.3207 | **0.2915** | — | 0.3112 | **−0.053** |
| Q6 LOB transfer, z_i = 199 (A4) | 0.8746 | 0.0155 | 0.0155 | — | 0.0156 | −0.0000 |

- **Linear infinite-volume σ₈ on model B.** BSK2 ODE: 0.324 (F3's 0.32). Q6 LOB: 0.0616 (R_B 0.0754 on model B; Q6 got
  0.073 at its own parameters).
- **Reading (frozen bands): "does not restore growth at 128³"** for every set.
  - With z_i = 199, KX ends 9 % below LIN: x reaches 20 near z ≈ 200, which stiffens the khronon.
  - In the LOB set, 95 % of σ₈² sits at k < 0.063 h/Mpc, below this box's fundamental mode. That is why the box σ₈ is
    0.0155 while the infinite-volume value is 0.062.
- **Checks.** I1–I4 PASS. **I5 FAILS as frozen**: peak RSS 1.64 GB against < 1 GB; the peak footprint was 0.27 GB (macOS
  keeps freed pages resident). MUTATE breaks I1 and I2.
- **LOB check.** K-LOB1: the DUST normaliser vs classy, 1.8e-4. K-LOB3: δ_τ recomputed independently is exact; MUTATE
  breaks it. I-LOB PASS.
- **Indicative, not a verdict. The frozen production run decides.**

## 5. Scorer (`l1_score.py`)

- **It reproduces the record first.** CFG596 canonical through this code path gives KiDS S0 144.26, F 212.99, Δχ² +68.73,
  EXCLUDED, exactly the record's.
- **Checks.** S0–S3 PASS. MUTATE breaks S3.
- **At 128³ L100** (k_hi = 1.0 h/Mpc) no KiDS point keeps 90 % support, so the indicative pairs are NOT DIAGNOSTIC.

## 6. Pre-result notes for the production (no change to the frozen plan)

- **Power at 512³ L100.** With k_hi = 4.0 h/Mpc, KiDS keeps **27 of 225** points; CFG596 kept 104 at k_hi = 8. DES keeps 40.
  The score is diagnostic (N ≥ 10) but weaker.
- **LOB cells.** Their transfer is ≤ 3 % of dust at k ≥ 0.063 h/Mpc and 1e-3–1e-4 at k ≥ 0.3. The CFG592 node construction
  fills k < k_lo with an EH shape matched at k_lo. For these cells that underestimates power at k < k_lo, so their KiDS
  Δχ² is a lower bound on the misfit (the predicted shear is too small).
- **Memory.**
  - Declared estimate (`khronon_pm.py estimate --N 512`): 30.4 GB. The est_gb is 35 (×1.15).
  - The measured 128³ peak footprint (0.27 GB, KX z_i = 199) scales to about 17 GB.
  - The calibration job measures the real peak first. 1024³ is excluded: the particles alone need 51.5 GB.
- **Time.** At 128³ on one thread a run takes 4–8 min. At 512³ on 8 threads, expect very roughly 1.5–4 h per cell, so about
  2 days for all 20 cells. The calibration job measures the per-step time.
- **Scoring after the runs.** `OMP_NUM_THREADS=1 nice -n 15 python3 l1_score.py --dir work/prod`, then the same with
  `L1_MUTATE=1`.
- **Halo profiles.** The coordinator's request (A3 item 5, reported only) is written into each z = 0 snapshot (`halos`).

## ENQUEUE (for the coordinator; this lane does not enqueue)

All jobs follow `compute_queue/JOB_CONTRACT.md`:
- SIGTERM or SIGINT → checkpoint → exit 75;
- `resume_cmd` exits 0 at once if DONE exists, continues from the checkpoint if there is one, and otherwise starts fresh;
- rolling checkpoints every 10 steps; atomic writes;
- the done-file is written only when the run completes.

Frozen order: the calibration job first, then the 14 frozen cells (A3), then the 6 LOB-IC cells (A4).

```bash
# Run from the repository root.  1) the calibration job; 2) the 14 frozen cells (A3 order); 3) the 6 LOB-IC cells (A4).
python3 compute_queue/heavyq.py add --id L1_calib_512 --cwd rebuild_2026_10_22/L1_khronon_pm \
  --cmd "python3 khronon_pm.py run --mode KX --foot canonical --muK 14.8 --N 512 --L 100 --zi 199 --nseed 512 --threads 8 --tag calib_KX_can_512_zi199 --maxsteps 3" \
  --resume-cmd "python3 khronon_pm.py run --mode KX --foot canonical --muK 14.8 --N 512 --L 100 --zi 199 --nseed 512 --threads 8 --tag calib_KX_can_512_zi199 --maxsteps 3 --resume" \
  --est-gb 36 --threads 8 --priority 200 --env L1_WORK=work/calib \
  --done-file work/calib/calib_KX_can_512_zi199/CALIB_DONE \
  --note "L1 A3: 3-step 512^3 KX footprint/timing calibration; outputs not used"

python3 compute_queue/heavyq.py add --id L1_S0_zi199 --cwd rebuild_2026_10_22/L1_khronon_pm \
  --cmd "python3 khronon_pm.py run --mode S0 --foot canonical --muK 14.8 --N 512 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic ode --tag S0_zi199" \
  --resume-cmd "python3 khronon_pm.py run --mode S0 --foot canonical --muK 14.8 --N 512 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic ode --tag S0_zi199 --resume" \
  --est-gb 35 --threads 8 --priority 120 --env L1_WORK=work/prod --done-file work/prod/S0_zi199/DONE

python3 compute_queue/heavyq.py add --id L1_LIN_mu14p8_zi199 --cwd rebuild_2026_10_22/L1_khronon_pm \
  --cmd "python3 khronon_pm.py run --mode LIN --foot canonical --muK 14.8 --N 512 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic ode --tag LIN_mu14p8_zi199" \
  --resume-cmd "python3 khronon_pm.py run --mode LIN --foot canonical --muK 14.8 --N 512 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic ode --tag LIN_mu14p8_zi199 --resume" \
  --est-gb 35 --threads 8 --priority 119 --env L1_WORK=work/prod --done-file work/prod/LIN_mu14p8_zi199/DONE

python3 compute_queue/heavyq.py add --id L1_KX_can_mu14p8_zi199 --cwd rebuild_2026_10_22/L1_khronon_pm \
  --cmd "python3 khronon_pm.py run --mode KX --foot canonical --muK 14.8 --N 512 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic ode --tag KX_can_mu14p8_zi199" \
  --resume-cmd "python3 khronon_pm.py run --mode KX --foot canonical --muK 14.8 --N 512 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic ode --tag KX_can_mu14p8_zi199 --resume" \
  --est-gb 35 --threads 8 --priority 118 --env L1_WORK=work/prod --done-file work/prod/KX_can_mu14p8_zi199/DONE

python3 compute_queue/heavyq.py add --id L1_KX_alt_mu14p8_zi199 --cwd rebuild_2026_10_22/L1_khronon_pm \
  --cmd "python3 khronon_pm.py run --mode KX --foot alt --muK 14.8 --N 512 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic ode --tag KX_alt_mu14p8_zi199" \
  --resume-cmd "python3 khronon_pm.py run --mode KX --foot alt --muK 14.8 --N 512 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic ode --tag KX_alt_mu14p8_zi199 --resume" \
  --est-gb 35 --threads 8 --priority 117 --env L1_WORK=work/prod --done-file work/prod/KX_alt_mu14p8_zi199/DONE

python3 compute_queue/heavyq.py add --id L1_S0_zi49 --cwd rebuild_2026_10_22/L1_khronon_pm \
  --cmd "python3 khronon_pm.py run --mode S0 --foot canonical --muK 14.8 --N 512 --L 100 --zi 49 --nseed 512 --threads 8 --halos --ic ode --tag S0_zi49" \
  --resume-cmd "python3 khronon_pm.py run --mode S0 --foot canonical --muK 14.8 --N 512 --L 100 --zi 49 --nseed 512 --threads 8 --halos --ic ode --tag S0_zi49 --resume" \
  --est-gb 35 --threads 8 --priority 116 --env L1_WORK=work/prod --done-file work/prod/S0_zi49/DONE

python3 compute_queue/heavyq.py add --id L1_LIN_mu14p8_zi49 --cwd rebuild_2026_10_22/L1_khronon_pm \
  --cmd "python3 khronon_pm.py run --mode LIN --foot canonical --muK 14.8 --N 512 --L 100 --zi 49 --nseed 512 --threads 8 --halos --ic ode --tag LIN_mu14p8_zi49" \
  --resume-cmd "python3 khronon_pm.py run --mode LIN --foot canonical --muK 14.8 --N 512 --L 100 --zi 49 --nseed 512 --threads 8 --halos --ic ode --tag LIN_mu14p8_zi49 --resume" \
  --est-gb 35 --threads 8 --priority 115 --env L1_WORK=work/prod --done-file work/prod/LIN_mu14p8_zi49/DONE

python3 compute_queue/heavyq.py add --id L1_KX_can_mu14p8_zi49 --cwd rebuild_2026_10_22/L1_khronon_pm \
  --cmd "python3 khronon_pm.py run --mode KX --foot canonical --muK 14.8 --N 512 --L 100 --zi 49 --nseed 512 --threads 8 --halos --ic ode --tag KX_can_mu14p8_zi49" \
  --resume-cmd "python3 khronon_pm.py run --mode KX --foot canonical --muK 14.8 --N 512 --L 100 --zi 49 --nseed 512 --threads 8 --halos --ic ode --tag KX_can_mu14p8_zi49 --resume" \
  --est-gb 35 --threads 8 --priority 114 --env L1_WORK=work/prod --done-file work/prod/KX_can_mu14p8_zi49/DONE

python3 compute_queue/heavyq.py add --id L1_KX_alt_mu14p8_zi49 --cwd rebuild_2026_10_22/L1_khronon_pm \
  --cmd "python3 khronon_pm.py run --mode KX --foot alt --muK 14.8 --N 512 --L 100 --zi 49 --nseed 512 --threads 8 --halos --ic ode --tag KX_alt_mu14p8_zi49" \
  --resume-cmd "python3 khronon_pm.py run --mode KX --foot alt --muK 14.8 --N 512 --L 100 --zi 49 --nseed 512 --threads 8 --halos --ic ode --tag KX_alt_mu14p8_zi49 --resume" \
  --est-gb 35 --threads 8 --priority 113 --env L1_WORK=work/prod --done-file work/prod/KX_alt_mu14p8_zi49/DONE

python3 compute_queue/heavyq.py add --id L1_LIN_mu400_zi49 --cwd rebuild_2026_10_22/L1_khronon_pm \
  --cmd "python3 khronon_pm.py run --mode LIN --foot canonical --muK 400 --N 512 --L 100 --zi 49 --nseed 512 --threads 8 --halos --ic ode --tag LIN_mu400_zi49" \
  --resume-cmd "python3 khronon_pm.py run --mode LIN --foot canonical --muK 400 --N 512 --L 100 --zi 49 --nseed 512 --threads 8 --halos --ic ode --tag LIN_mu400_zi49 --resume" \
  --est-gb 35 --threads 8 --priority 112 --env L1_WORK=work/prod --done-file work/prod/LIN_mu400_zi49/DONE

python3 compute_queue/heavyq.py add --id L1_KX_can_mu400_zi49 --cwd rebuild_2026_10_22/L1_khronon_pm \
  --cmd "python3 khronon_pm.py run --mode KX --foot canonical --muK 400 --N 512 --L 100 --zi 49 --nseed 512 --threads 8 --halos --ic ode --tag KX_can_mu400_zi49" \
  --resume-cmd "python3 khronon_pm.py run --mode KX --foot canonical --muK 400 --N 512 --L 100 --zi 49 --nseed 512 --threads 8 --halos --ic ode --tag KX_can_mu400_zi49 --resume" \
  --est-gb 35 --threads 8 --priority 111 --env L1_WORK=work/prod --done-file work/prod/KX_can_mu400_zi49/DONE

python3 compute_queue/heavyq.py add --id L1_KX_alt_mu400_zi49 --cwd rebuild_2026_10_22/L1_khronon_pm \
  --cmd "python3 khronon_pm.py run --mode KX --foot alt --muK 400 --N 512 --L 100 --zi 49 --nseed 512 --threads 8 --halos --ic ode --tag KX_alt_mu400_zi49" \
  --resume-cmd "python3 khronon_pm.py run --mode KX --foot alt --muK 400 --N 512 --L 100 --zi 49 --nseed 512 --threads 8 --halos --ic ode --tag KX_alt_mu400_zi49 --resume" \
  --est-gb 35 --threads 8 --priority 110 --env L1_WORK=work/prod --done-file work/prod/KX_alt_mu400_zi49/DONE

python3 compute_queue/heavyq.py add --id L1_LIN_mu400_zi199 --cwd rebuild_2026_10_22/L1_khronon_pm \
  --cmd "python3 khronon_pm.py run --mode LIN --foot canonical --muK 400 --N 512 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic ode --tag LIN_mu400_zi199" \
  --resume-cmd "python3 khronon_pm.py run --mode LIN --foot canonical --muK 400 --N 512 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic ode --tag LIN_mu400_zi199 --resume" \
  --est-gb 35 --threads 8 --priority 109 --env L1_WORK=work/prod --done-file work/prod/LIN_mu400_zi199/DONE

python3 compute_queue/heavyq.py add --id L1_KX_can_mu400_zi199 --cwd rebuild_2026_10_22/L1_khronon_pm \
  --cmd "python3 khronon_pm.py run --mode KX --foot canonical --muK 400 --N 512 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic ode --tag KX_can_mu400_zi199" \
  --resume-cmd "python3 khronon_pm.py run --mode KX --foot canonical --muK 400 --N 512 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic ode --tag KX_can_mu400_zi199 --resume" \
  --est-gb 35 --threads 8 --priority 108 --env L1_WORK=work/prod --done-file work/prod/KX_can_mu400_zi199/DONE

python3 compute_queue/heavyq.py add --id L1_KX_alt_mu400_zi199 --cwd rebuild_2026_10_22/L1_khronon_pm \
  --cmd "python3 khronon_pm.py run --mode KX --foot alt --muK 400 --N 512 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic ode --tag KX_alt_mu400_zi199" \
  --resume-cmd "python3 khronon_pm.py run --mode KX --foot alt --muK 400 --N 512 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic ode --tag KX_alt_mu400_zi199 --resume" \
  --est-gb 35 --threads 8 --priority 107 --env L1_WORK=work/prod --done-file work/prod/KX_alt_mu400_zi199/DONE

python3 compute_queue/heavyq.py add --id L1_LIN_mu14p8_zi199_LOB --cwd rebuild_2026_10_22/L1_khronon_pm \
  --cmd "python3 khronon_pm.py run --mode LIN --foot canonical --muK 14.8 --N 512 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic lob --tag LIN_mu14p8_zi199_LOB" \
  --resume-cmd "python3 khronon_pm.py run --mode LIN --foot canonical --muK 14.8 --N 512 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic lob --tag LIN_mu14p8_zi199_LOB --resume" \
  --est-gb 35 --threads 8 --priority 106 --env L1_WORK=work/prod --done-file work/prod/LIN_mu14p8_zi199_LOB/DONE

python3 compute_queue/heavyq.py add --id L1_KX_can_mu14p8_zi199_LOB --cwd rebuild_2026_10_22/L1_khronon_pm \
  --cmd "python3 khronon_pm.py run --mode KX --foot canonical --muK 14.8 --N 512 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic lob --tag KX_can_mu14p8_zi199_LOB" \
  --resume-cmd "python3 khronon_pm.py run --mode KX --foot canonical --muK 14.8 --N 512 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic lob --tag KX_can_mu14p8_zi199_LOB --resume" \
  --est-gb 35 --threads 8 --priority 105 --env L1_WORK=work/prod --done-file work/prod/KX_can_mu14p8_zi199_LOB/DONE

python3 compute_queue/heavyq.py add --id L1_KX_alt_mu14p8_zi199_LOB --cwd rebuild_2026_10_22/L1_khronon_pm \
  --cmd "python3 khronon_pm.py run --mode KX --foot alt --muK 14.8 --N 512 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic lob --tag KX_alt_mu14p8_zi199_LOB" \
  --resume-cmd "python3 khronon_pm.py run --mode KX --foot alt --muK 14.8 --N 512 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic lob --tag KX_alt_mu14p8_zi199_LOB --resume" \
  --est-gb 35 --threads 8 --priority 104 --env L1_WORK=work/prod --done-file work/prod/KX_alt_mu14p8_zi199_LOB/DONE

python3 compute_queue/heavyq.py add --id L1_LIN_mu400_zi199_LOB --cwd rebuild_2026_10_22/L1_khronon_pm \
  --cmd "python3 khronon_pm.py run --mode LIN --foot canonical --muK 400 --N 512 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic lob --tag LIN_mu400_zi199_LOB" \
  --resume-cmd "python3 khronon_pm.py run --mode LIN --foot canonical --muK 400 --N 512 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic lob --tag LIN_mu400_zi199_LOB --resume" \
  --est-gb 35 --threads 8 --priority 103 --env L1_WORK=work/prod --done-file work/prod/LIN_mu400_zi199_LOB/DONE

python3 compute_queue/heavyq.py add --id L1_KX_can_mu400_zi199_LOB --cwd rebuild_2026_10_22/L1_khronon_pm \
  --cmd "python3 khronon_pm.py run --mode KX --foot canonical --muK 400 --N 512 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic lob --tag KX_can_mu400_zi199_LOB" \
  --resume-cmd "python3 khronon_pm.py run --mode KX --foot canonical --muK 400 --N 512 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic lob --tag KX_can_mu400_zi199_LOB --resume" \
  --est-gb 35 --threads 8 --priority 102 --env L1_WORK=work/prod --done-file work/prod/KX_can_mu400_zi199_LOB/DONE

python3 compute_queue/heavyq.py add --id L1_KX_alt_mu400_zi199_LOB --cwd rebuild_2026_10_22/L1_khronon_pm \
  --cmd "python3 khronon_pm.py run --mode KX --foot alt --muK 400 --N 512 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic lob --tag KX_alt_mu400_zi199_LOB" \
  --resume-cmd "python3 khronon_pm.py run --mode KX --foot alt --muK 400 --N 512 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic lob --tag KX_alt_mu400_zi199_LOB --resume" \
  --est-gb 35 --threads 8 --priority 101 --env L1_WORK=work/prod --done-file work/prod/KX_alt_mu400_zi199_LOB/DONE
```



## ENQUEUE-A5 (resolution ladder, AMENDMENT A5; for the coordinator, this lane does not enqueue)

The rungs run at priorities 300–310, above the 512³ calibration (200), so they run first. They are reported as convergence
only, never pooled with the 512³ cells.

**est_gb.** It is 1.2 × the measured peak footprint (3-step KX at z_i = 199, 8 threads):
- 128³: 0.539 GB measured → est 0.65;
- 256³: 2.727 GB measured → est 3.3;
- 384³: 8.66 GB, extrapolated from 0.226 GB + 149 B per cell → est 10.4. Its calibration was skipped because the two-point
  scaling is clean.

**Caches.** The NSEED-512 white-noise caches and the model-B CLASS spectrum are already in `work/prod`.

**Fix.** The 256³ calibration found a fork-related pocketfft failure at > 1 thread. It is fixed, and SIGTERM → resume is
bit-identical at 8 threads.

```bash
# A5 resolution ladder (run from the repository root). mu_K 14.8, z_i 199, L 100, NSEED 512 (phases shared with the 512^3 cells).

python3 compute_queue/heavyq.py add --id L1_A5_S0_N256_zi199 --cwd rebuild_2026_10_22/L1_khronon_pm \
  --cmd "python3 khronon_pm.py run --mode S0 --foot canonical --muK 14.8 --N 256 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic ode --tag A5_S0_N256_zi199" \
  --resume-cmd "python3 khronon_pm.py run --mode S0 --foot canonical --muK 14.8 --N 256 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic ode --tag A5_S0_N256_zi199 --resume" \
  --est-gb 3.3 --threads 8 --priority 310 --env L1_WORK=work/prod --done-file work/prod/A5_S0_N256_zi199/DONE

python3 compute_queue/heavyq.py add --id L1_A5_LIN_N256_zi199 --cwd rebuild_2026_10_22/L1_khronon_pm \
  --cmd "python3 khronon_pm.py run --mode LIN --foot canonical --muK 14.8 --N 256 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic ode --tag A5_LIN_N256_zi199" \
  --resume-cmd "python3 khronon_pm.py run --mode LIN --foot canonical --muK 14.8 --N 256 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic ode --tag A5_LIN_N256_zi199 --resume" \
  --est-gb 3.3 --threads 8 --priority 309 --env L1_WORK=work/prod --done-file work/prod/A5_LIN_N256_zi199/DONE

python3 compute_queue/heavyq.py add --id L1_A5_KX_can_N256_zi199 --cwd rebuild_2026_10_22/L1_khronon_pm \
  --cmd "python3 khronon_pm.py run --mode KX --foot canonical --muK 14.8 --N 256 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic ode --tag A5_KX_can_N256_zi199" \
  --resume-cmd "python3 khronon_pm.py run --mode KX --foot canonical --muK 14.8 --N 256 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic ode --tag A5_KX_can_N256_zi199 --resume" \
  --est-gb 3.3 --threads 8 --priority 308 --env L1_WORK=work/prod --done-file work/prod/A5_KX_can_N256_zi199/DONE

python3 compute_queue/heavyq.py add --id L1_A5_KX_alt_N256_zi199 --cwd rebuild_2026_10_22/L1_khronon_pm \
  --cmd "python3 khronon_pm.py run --mode KX --foot alt --muK 14.8 --N 256 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic ode --tag A5_KX_alt_N256_zi199" \
  --resume-cmd "python3 khronon_pm.py run --mode KX --foot alt --muK 14.8 --N 256 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic ode --tag A5_KX_alt_N256_zi199 --resume" \
  --est-gb 3.3 --threads 8 --priority 307 --env L1_WORK=work/prod --done-file work/prod/A5_KX_alt_N256_zi199/DONE

python3 compute_queue/heavyq.py add --id L1_A5_S0_N384_zi199 --cwd rebuild_2026_10_22/L1_khronon_pm \
  --cmd "python3 khronon_pm.py run --mode S0 --foot canonical --muK 14.8 --N 384 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic ode --tag A5_S0_N384_zi199" \
  --resume-cmd "python3 khronon_pm.py run --mode S0 --foot canonical --muK 14.8 --N 384 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic ode --tag A5_S0_N384_zi199 --resume" \
  --est-gb 10.4 --threads 8 --priority 306 --env L1_WORK=work/prod --done-file work/prod/A5_S0_N384_zi199/DONE

python3 compute_queue/heavyq.py add --id L1_A5_LIN_N384_zi199 --cwd rebuild_2026_10_22/L1_khronon_pm \
  --cmd "python3 khronon_pm.py run --mode LIN --foot canonical --muK 14.8 --N 384 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic ode --tag A5_LIN_N384_zi199" \
  --resume-cmd "python3 khronon_pm.py run --mode LIN --foot canonical --muK 14.8 --N 384 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic ode --tag A5_LIN_N384_zi199 --resume" \
  --est-gb 10.4 --threads 8 --priority 305 --env L1_WORK=work/prod --done-file work/prod/A5_LIN_N384_zi199/DONE

python3 compute_queue/heavyq.py add --id L1_A5_KX_can_N384_zi199 --cwd rebuild_2026_10_22/L1_khronon_pm \
  --cmd "python3 khronon_pm.py run --mode KX --foot canonical --muK 14.8 --N 384 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic ode --tag A5_KX_can_N384_zi199" \
  --resume-cmd "python3 khronon_pm.py run --mode KX --foot canonical --muK 14.8 --N 384 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic ode --tag A5_KX_can_N384_zi199 --resume" \
  --est-gb 10.4 --threads 8 --priority 304 --env L1_WORK=work/prod --done-file work/prod/A5_KX_can_N384_zi199/DONE

python3 compute_queue/heavyq.py add --id L1_A5_KX_alt_N384_zi199 --cwd rebuild_2026_10_22/L1_khronon_pm \
  --cmd "python3 khronon_pm.py run --mode KX --foot alt --muK 14.8 --N 384 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic ode --tag A5_KX_alt_N384_zi199" \
  --resume-cmd "python3 khronon_pm.py run --mode KX --foot alt --muK 14.8 --N 384 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic ode --tag A5_KX_alt_N384_zi199 --resume" \
  --est-gb 10.4 --threads 8 --priority 303 --env L1_WORK=work/prod --done-file work/prod/A5_KX_alt_N384_zi199/DONE

python3 compute_queue/heavyq.py add --id L1_A5_LIN_N384_zi199_LOB --cwd rebuild_2026_10_22/L1_khronon_pm \
  --cmd "python3 khronon_pm.py run --mode LIN --foot canonical --muK 14.8 --N 384 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic lob --tag A5_LIN_N384_zi199_LOB" \
  --resume-cmd "python3 khronon_pm.py run --mode LIN --foot canonical --muK 14.8 --N 384 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic lob --tag A5_LIN_N384_zi199_LOB --resume" \
  --est-gb 10.4 --threads 8 --priority 302 --env L1_WORK=work/prod --done-file work/prod/A5_LIN_N384_zi199_LOB/DONE

python3 compute_queue/heavyq.py add --id L1_A5_KX_can_N384_zi199_LOB --cwd rebuild_2026_10_22/L1_khronon_pm \
  --cmd "python3 khronon_pm.py run --mode KX --foot canonical --muK 14.8 --N 384 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic lob --tag A5_KX_can_N384_zi199_LOB" \
  --resume-cmd "python3 khronon_pm.py run --mode KX --foot canonical --muK 14.8 --N 384 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic lob --tag A5_KX_can_N384_zi199_LOB --resume" \
  --est-gb 10.4 --threads 8 --priority 301 --env L1_WORK=work/prod --done-file work/prod/A5_KX_can_N384_zi199_LOB/DONE

python3 compute_queue/heavyq.py add --id L1_A5_S0_N128_zi199 --cwd rebuild_2026_10_22/L1_khronon_pm \
  --cmd "python3 khronon_pm.py run --mode S0 --foot canonical --muK 14.8 --N 128 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic ode --tag A5_S0_N128_zi199" \
  --resume-cmd "python3 khronon_pm.py run --mode S0 --foot canonical --muK 14.8 --N 128 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic ode --tag A5_S0_N128_zi199 --resume" \
  --est-gb 0.65 --threads 8 --priority 300 --env L1_WORK=work/prod --done-file work/prod/A5_S0_N128_zi199/DONE

python3 compute_queue/heavyq.py add --id L1_A5_LIN_N128_zi199 --cwd rebuild_2026_10_22/L1_khronon_pm \
  --cmd "python3 khronon_pm.py run --mode LIN --foot canonical --muK 14.8 --N 128 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic ode --tag A5_LIN_N128_zi199" \
  --resume-cmd "python3 khronon_pm.py run --mode LIN --foot canonical --muK 14.8 --N 128 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic ode --tag A5_LIN_N128_zi199 --resume" \
  --est-gb 0.65 --threads 8 --priority 300 --env L1_WORK=work/prod --done-file work/prod/A5_LIN_N128_zi199/DONE

python3 compute_queue/heavyq.py add --id L1_A5_KX_can_N128_zi199 --cwd rebuild_2026_10_22/L1_khronon_pm \
  --cmd "python3 khronon_pm.py run --mode KX --foot canonical --muK 14.8 --N 128 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic ode --tag A5_KX_can_N128_zi199" \
  --resume-cmd "python3 khronon_pm.py run --mode KX --foot canonical --muK 14.8 --N 128 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic ode --tag A5_KX_can_N128_zi199 --resume" \
  --est-gb 0.65 --threads 8 --priority 300 --env L1_WORK=work/prod --done-file work/prod/A5_KX_can_N128_zi199/DONE

python3 compute_queue/heavyq.py add --id L1_A5_KX_alt_N128_zi199 --cwd rebuild_2026_10_22/L1_khronon_pm \
  --cmd "python3 khronon_pm.py run --mode KX --foot alt --muK 14.8 --N 128 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic ode --tag A5_KX_alt_N128_zi199" \
  --resume-cmd "python3 khronon_pm.py run --mode KX --foot alt --muK 14.8 --N 128 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic ode --tag A5_KX_alt_N128_zi199 --resume" \
  --est-gb 0.65 --threads 8 --priority 300 --env L1_WORK=work/prod --done-file work/prod/A5_KX_alt_N128_zi199/DONE
```


## ENQUEUE-A6 (DBI-IC set, AMENDMENT A6; for the coordinator, this lane does not enqueue)

The owner's question: where was the cold energy at BBN, and how does it form galaxies from there? The ICs at z_i = 199 come
from Q7's validated DBI CLASS, the only BBN-viable early completion of v3 on record. It is run read-only, with BS's
published sets only:
- the cap, μ_K = 14.8 h/Mpc with λ_D = 30;
- BS24 P1, μ⁻¹ = 223 kpc (6.54029 h/Mpc at model B's h) with λ_D = 30.

Q7's fitted λ_D,95 door is not used.

**Linear check on model B** (the DUST normaliser equals classy; reported). DBI σ₈ is 0.2509 (cap-λ30) and 0.2200 (P1), so
R_B = 0.307 and 0.269. Q7 found 0.295 and 0.259 at its own parameters.

**Engine.** No change is needed (A6 item 3). At z_i = 199 the DBI background differs from dust by ≤ 3.9e-3 in ρ̄ and w, and
its late hold mass differs from μ_K by ≤ 1.8e-2 in M². Both fall as a⁻³, and they are declared, not fitted.

**Satellite split** (pre-result clarification of A6 item 5). A galaxy-mass halo's hosts are the other, more massive
cluster-class or top50 halos.
- satellite = the nearest host lies 1–3 Mpc (physical) away;
- field = no host within 3 Mpc.

**est_gb.** The measured 3-step DBI KX peak footprint at 256³ is 2.770 GB (A5's ODE KX was 2.727), so est = 3.4. 384³ is
extrapolated with A5's scaling to 8.80 GB, so est = 10.6. Calibration: 256³ DBI KX took about 14 s/step at 8 threads, with
16–26 hold iterations.

**Order.** Priorities 299–290, after the A5 ladder and before the 512³ calibration. The DBI tables are pre-built in
`work/prod`.

```bash
# A6 DBI-IC set (run from the repository root). BS's published sets only: cap mu_K 14.8 h/Mpc + lambda_D 30; P1 223 kpc (6.54029 h/Mpc) + lambda_D 30.
# Controls: A5's S0 cells at the same N (L1_A5_S0_N256_zi199, L1_A5_S0_N384_zi199). DBI tables are pre-built in work/prod.

python3 compute_queue/heavyq.py add --id L1_A6_LIN_dbi_cap30_N256_zi199 --cwd rebuild_2026_10_22/L1_khronon_pm \
  --cmd "python3 khronon_pm.py run --mode LIN --foot canonical --muK 14.8 --N 256 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic dbi --lamD 30 --tag A6_LIN_dbi_cap30_N256_zi199" \
  --resume-cmd "python3 khronon_pm.py run --mode LIN --foot canonical --muK 14.8 --N 256 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic dbi --lamD 30 --tag A6_LIN_dbi_cap30_N256_zi199 --resume" \
  --est-gb 3.4 --threads 8 --priority 299 --env L1_WORK=work/prod --done-file work/prod/A6_LIN_dbi_cap30_N256_zi199/DONE

python3 compute_queue/heavyq.py add --id L1_A6_KX_can_dbi_cap30_N256_zi199 --cwd rebuild_2026_10_22/L1_khronon_pm \
  --cmd "python3 khronon_pm.py run --mode KX --foot canonical --muK 14.8 --N 256 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic dbi --lamD 30 --tag A6_KX_can_dbi_cap30_N256_zi199" \
  --resume-cmd "python3 khronon_pm.py run --mode KX --foot canonical --muK 14.8 --N 256 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic dbi --lamD 30 --tag A6_KX_can_dbi_cap30_N256_zi199 --resume" \
  --est-gb 3.4 --threads 8 --priority 298 --env L1_WORK=work/prod --done-file work/prod/A6_KX_can_dbi_cap30_N256_zi199/DONE

python3 compute_queue/heavyq.py add --id L1_A6_KX_alt_dbi_cap30_N256_zi199 --cwd rebuild_2026_10_22/L1_khronon_pm \
  --cmd "python3 khronon_pm.py run --mode KX --foot alt --muK 14.8 --N 256 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic dbi --lamD 30 --tag A6_KX_alt_dbi_cap30_N256_zi199" \
  --resume-cmd "python3 khronon_pm.py run --mode KX --foot alt --muK 14.8 --N 256 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic dbi --lamD 30 --tag A6_KX_alt_dbi_cap30_N256_zi199 --resume" \
  --est-gb 3.4 --threads 8 --priority 297 --env L1_WORK=work/prod --done-file work/prod/A6_KX_alt_dbi_cap30_N256_zi199/DONE

python3 compute_queue/heavyq.py add --id L1_A6_LIN_dbi_P1_N256_zi199 --cwd rebuild_2026_10_22/L1_khronon_pm \
  --cmd "python3 khronon_pm.py run --mode LIN --foot canonical --muK 6.54029 --N 256 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic dbi --lamD 30 --tag A6_LIN_dbi_P1_N256_zi199" \
  --resume-cmd "python3 khronon_pm.py run --mode LIN --foot canonical --muK 6.54029 --N 256 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic dbi --lamD 30 --tag A6_LIN_dbi_P1_N256_zi199 --resume" \
  --est-gb 3.4 --threads 8 --priority 296 --env L1_WORK=work/prod --done-file work/prod/A6_LIN_dbi_P1_N256_zi199/DONE

python3 compute_queue/heavyq.py add --id L1_A6_KX_can_dbi_P1_N256_zi199 --cwd rebuild_2026_10_22/L1_khronon_pm \
  --cmd "python3 khronon_pm.py run --mode KX --foot canonical --muK 6.54029 --N 256 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic dbi --lamD 30 --tag A6_KX_can_dbi_P1_N256_zi199" \
  --resume-cmd "python3 khronon_pm.py run --mode KX --foot canonical --muK 6.54029 --N 256 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic dbi --lamD 30 --tag A6_KX_can_dbi_P1_N256_zi199 --resume" \
  --est-gb 3.4 --threads 8 --priority 295 --env L1_WORK=work/prod --done-file work/prod/A6_KX_can_dbi_P1_N256_zi199/DONE

python3 compute_queue/heavyq.py add --id L1_A6_KX_alt_dbi_P1_N256_zi199 --cwd rebuild_2026_10_22/L1_khronon_pm \
  --cmd "python3 khronon_pm.py run --mode KX --foot alt --muK 6.54029 --N 256 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic dbi --lamD 30 --tag A6_KX_alt_dbi_P1_N256_zi199" \
  --resume-cmd "python3 khronon_pm.py run --mode KX --foot alt --muK 6.54029 --N 256 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic dbi --lamD 30 --tag A6_KX_alt_dbi_P1_N256_zi199 --resume" \
  --est-gb 3.4 --threads 8 --priority 294 --env L1_WORK=work/prod --done-file work/prod/A6_KX_alt_dbi_P1_N256_zi199/DONE

python3 compute_queue/heavyq.py add --id L1_A6_LIN_dbi_cap30_N384_zi199 --cwd rebuild_2026_10_22/L1_khronon_pm \
  --cmd "python3 khronon_pm.py run --mode LIN --foot canonical --muK 14.8 --N 384 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic dbi --lamD 30 --tag A6_LIN_dbi_cap30_N384_zi199" \
  --resume-cmd "python3 khronon_pm.py run --mode LIN --foot canonical --muK 14.8 --N 384 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic dbi --lamD 30 --tag A6_LIN_dbi_cap30_N384_zi199 --resume" \
  --est-gb 10.6 --threads 8 --priority 293 --env L1_WORK=work/prod --done-file work/prod/A6_LIN_dbi_cap30_N384_zi199/DONE

python3 compute_queue/heavyq.py add --id L1_A6_KX_can_dbi_cap30_N384_zi199 --cwd rebuild_2026_10_22/L1_khronon_pm \
  --cmd "python3 khronon_pm.py run --mode KX --foot canonical --muK 14.8 --N 384 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic dbi --lamD 30 --tag A6_KX_can_dbi_cap30_N384_zi199" \
  --resume-cmd "python3 khronon_pm.py run --mode KX --foot canonical --muK 14.8 --N 384 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic dbi --lamD 30 --tag A6_KX_can_dbi_cap30_N384_zi199 --resume" \
  --est-gb 10.6 --threads 8 --priority 292 --env L1_WORK=work/prod --done-file work/prod/A6_KX_can_dbi_cap30_N384_zi199/DONE

python3 compute_queue/heavyq.py add --id L1_A6_KX_alt_dbi_cap30_N384_zi199 --cwd rebuild_2026_10_22/L1_khronon_pm \
  --cmd "python3 khronon_pm.py run --mode KX --foot alt --muK 14.8 --N 384 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic dbi --lamD 30 --tag A6_KX_alt_dbi_cap30_N384_zi199" \
  --resume-cmd "python3 khronon_pm.py run --mode KX --foot alt --muK 14.8 --N 384 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic dbi --lamD 30 --tag A6_KX_alt_dbi_cap30_N384_zi199 --resume" \
  --est-gb 10.6 --threads 8 --priority 291 --env L1_WORK=work/prod --done-file work/prod/A6_KX_alt_dbi_cap30_N384_zi199/DONE

python3 compute_queue/heavyq.py add --id L1_A6_LIN_dbi_P1_N384_zi199 --cwd rebuild_2026_10_22/L1_khronon_pm \
  --cmd "python3 khronon_pm.py run --mode LIN --foot canonical --muK 6.54029 --N 384 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic dbi --lamD 30 --tag A6_LIN_dbi_P1_N384_zi199" \
  --resume-cmd "python3 khronon_pm.py run --mode LIN --foot canonical --muK 6.54029 --N 384 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic dbi --lamD 30 --tag A6_LIN_dbi_P1_N384_zi199 --resume" \
  --est-gb 10.6 --threads 8 --priority 290 --env L1_WORK=work/prod --done-file work/prod/A6_LIN_dbi_P1_N384_zi199/DONE

python3 compute_queue/heavyq.py add --id L1_A6_KX_can_dbi_P1_N384_zi199 --cwd rebuild_2026_10_22/L1_khronon_pm \
  --cmd "python3 khronon_pm.py run --mode KX --foot canonical --muK 6.54029 --N 384 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic dbi --lamD 30 --tag A6_KX_can_dbi_P1_N384_zi199" \
  --resume-cmd "python3 khronon_pm.py run --mode KX --foot canonical --muK 6.54029 --N 384 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic dbi --lamD 30 --tag A6_KX_can_dbi_P1_N384_zi199 --resume" \
  --est-gb 10.6 --threads 8 --priority 290 --env L1_WORK=work/prod --done-file work/prod/A6_KX_can_dbi_P1_N384_zi199/DONE

python3 compute_queue/heavyq.py add --id L1_A6_KX_alt_dbi_P1_N384_zi199 --cwd rebuild_2026_10_22/L1_khronon_pm \
  --cmd "python3 khronon_pm.py run --mode KX --foot alt --muK 6.54029 --N 384 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic dbi --lamD 30 --tag A6_KX_alt_dbi_P1_N384_zi199" \
  --resume-cmd "python3 khronon_pm.py run --mode KX --foot alt --muK 6.54029 --N 384 --L 100 --zi 199 --nseed 512 --threads 8 --halos --ic dbi --lamD 30 --tag A6_KX_alt_dbi_P1_N384_zi199 --resume" \
  --est-gb 10.6 --threads 8 --priority 290 --env L1_WORK=work/prod --done-file work/prod/A6_KX_alt_dbi_P1_N384_zi199/DONE
```


## A7, the "early release" test: no cells (`l1_x0dust.py`; A7)

- **Dust-limit spectrum, hold off:** x_rms crosses 1 at **z_x = 153 (canonical) / 174 (alt)**. Before that, x_rms is 51 at
  z = 3000 and 14 at z = 1000.
- **DBI (cap, λ_D 30) on its own spectrum:** z_x = 242 / 264. M²/μ² is 3.2e4 at z = 3000, 3.9 at z = 1000 and 1.0 by z = 199.
- **The coordinator's rule (z_x ≳ 300) is not met, so no A7 cell is queued.**

**The premise is also inverted, shown exactly (XD3).** Larger x raises f = μ + xμ′, and the khronon's net self-force
kernel (m² − fk²)/((1 − f)k² + m²) falls monotonically, to the Jeans form as x → ∞. Early strong fields stiffen the khronon;
they do not release it. That matches the 128³ z_i = 199 run, where KX ended 9 % below LIN.

## A5 ladder, rung by rung (convergence only; no verdict)

Scored as each rung lands, by the owner's request ("score L1 when it lands"). `l1_ladder.py` reads only completed cells and
uses the frozen §4 definitions; the A5 reading bands carry the word "indicative". The KiDS score uses the frozen
`l1_score.py` on that rung's cells only (a link directory under `work/`, label `_A5_N<N>`). MUTATE (S0 normaliser replaced by
LIN) makes L4 FAIL, as required.

| rung | σ₈,PM S0 / LIN / KX-can / KX-alt | ρ_NL can / alt | indicative reading | KiDS (`l1_score.py`) | checks |
|---|---|---|---|---|---|
| 256³ | 0.820 / 0.285 / 0.254 / 0.260 | −0.058 / −0.047 | does not restore growth (KX sits below LIN) | NOT DIAGNOSTIC: N_kept 0 at k_hi 2.0 h/Mpc; the scorer's own S0 reproduces CFG596 (+68.73) | 4/4; MUTATE L4 FAIL |
| 384³ | 0.821 / 0.286 / 0.254 / 0.261 | −0.059 / −0.047 | does not restore growth (KX below LIN); converged with 256³ to ≤ 0.0005 in ρ_NL | NOT DIAGNOSTIC: N_kept 0 even at k_hi 3.0 h/Mpc; only the 512³ production can be scored against KiDS | 4/4; MUTATE L4 FAIL |
| 384³ LOB-IC (Q6's Boltzmann state at z_i 199; control S0-384) | LIN 0.01347 / KX-can 0.01345 (S0 0.821) | −0.0000 (−1.7e-5) | from the Boltzmann linear state the khronon barely grows (σ₈ ≈ 1.6 % of the dust limit) and the nonlinear term does nothing (amplitudes stay linear) | not scored (amplitude far below the KiDS range) | in the 4/4 run; L1 now counts the 2 LOB cells (10/10 converged); peak RSS 14.1 / 18.7 GB under the queue |
| 128³ (NSEED 512) | 0.816 / 0.283 / 0.253 / 0.259 | −0.057 / −0.045 | does not restore growth; ladder 128 → 256 → 384 converges monotonically (−0.0565 → −0.0583 → −0.0588 / −0.0452 → −0.0467 → −0.0470) | not scored (k_hi 1.0 h/Mpc) | 4/4 (14/14 cells converged); MUTATE L4 FAIL |

**Ladder complete (A5).** Every rung, at every resolution and from both IC families, says the nonlinear J_x term does not restore growth; the frozen 512³ production run gives the verdict and is the only rung KiDS can score.

KX halos at 256³ (reported only, resolution-limited: cell 0.57 Mpc): 4 / 7 galaxy-class halos, median dust/baryon in
0.3–1 Mpc 4.16 / 4.20 against the cosmic 5.27. At 384³ (cell 0.38 Mpc): 20 / 35 galaxy-class halos (3 / 5 satellites at 1–3 Mpc from a
larger host), median dust/baryon 4.06 / 4.08. Scoring note (CFG963, e96c21a87): the L1 engine carries no gas expulsion
(FROZEN_CRITERIA L76), and its KiDS score is KX against its own S0, feedback-matched by construction. If L1 is ever
compared with NCS0 / theory-v2 numbers, use CFG963's score_vs_feedback_control. Reading sentence (A4): every L1 result belongs to "v3 on a dust background
with a yet-unspecified early K", not to the literal theory.

## A6 DBI-IC set, as it lands (reported only; no verdict weight)

Read by `l1_a6.py`, using the frozen A6 item-5 statistics. The control is A5's S0 at the same N. MUTATE (S0 replaced by the
set's LIN cell) makes A4 FAIL, as required.

| set @ N | σ₈ LIN (fraction of S0) / KX-can / KX-alt | ρ_NL can / alt | P/P_S0 at k ≈ 0.1 / 0.3 / 1 h/Mpc (LIN) | halos | reading |
|---|---|---|---|---|---|
| cap30 @ 256³ (λ_D 30) | 0.201 (0.245) / 0.185 / 0.188 | −0.026 / −0.021 | 0.17 / 0.020 / 0.0017 | none in any cell | does not restore growth |
| P1 @ 256³ (λ_D 30) | 0.177 (0.216) / 0.112 / 0.127 | −0.102 / −0.078 | 0.13 / 0.016 / 0.0015 | none in any cell | deepens the deficit |
| cap30, P1 @ 384³ | queued | | | | |

From BS25's BBN-viable DBI state, v3's own nonlinear dynamics form no galaxy-mass halo in a 100 Mpc/h box, so the satellite
vs field question (A6 item 5) has no halos to answer it at 256³. The linear deficit (0.22–0.25 of the dust limit) matches
Q7's R_B 0.26–0.32. 6/6 cells converged.


## A5 + A6 results (queue runs, scored 2026-10-25; reported only, never pooled, not a verdict)

Scored by `l1_ladder.py` (→ `l1_ladder.out`, `_results.json`) and by the frozen scorer `l1_score.py --label _A5A6`. Setup:
μ_K 14.8 (P1: 6.54029) h/Mpc, z_i = 199, L100, NSEED 512, σ₈ at z = 0.

| IC / rung | S0 | LIN | KX-can (ρ_NL) | KX-alt (ρ_NL) |
|---|---|---|---|---|
| F3-ODE, 128³ | 0.8159 | 0.2828 | 0.2527 (−0.057) | 0.2587 (−0.045) |
| F3-ODE, 256³ | 0.8203 | 0.2853 | 0.2540 (−0.058) | 0.2603 (−0.047) |
| F3-ODE, 384³ | 0.8210 | 0.2858 | 0.2543 (−0.059) | 0.2606 (−0.047) |
| LOB, 384³ | 0.8210 | 0.0135 | 0.0135 (−0.000) | — |
| DBI cap-λ30, 256³ / 384³ | 0.820 / 0.821 | 0.2010 / 0.2013 | 0.1848 / 0.1850 (−0.026) | 0.1879 / 0.1882 (−0.021) |
| DBI P1, 256³ / 384³ | 0.820 / 0.821 | 0.1771 / 0.1774 | 0.1118 / 0.1117 (**−0.102**) | 0.1268 / 0.1269 (−0.078) |

**KX is not LIN.**
- Every KX run's state hash and σ₈ differ from its LIN: KX/LIN is 0.89–0.92 (ODE), 0.92–0.94 (DBI cap) and 0.63–0.72 (DBI P1).
- Every hold call converged. The largest per-call iteration count is 26–102, and the largest x is 6–115.
- The earlier "identical numbers" read must have compared LIN with LIN (or S0) fields. The hashes in `l1_ladder_results.json`
  settle it.

**Reading (frozen bands, indicative).**
- Every cell "does not restore growth". DBI P1 KX-can "deepens the deficit" (ρ_NL = −0.10).
- **Resolution trend.** ρ_NL is flat from 128 to 384, within 0.002. The nonlinear J_x term's effect is set before halo
  cores matter: x is large at z ~ 200 and in the strongest wells. That effect is to stiffen the khronon, as XD3 predicts.
- **DBI vs its LIN.** The BBN-consistent DBI ICs start below the ODE ones: LIN/S0 is 0.245 (cap) and 0.216 (P1), against
  0.348 for the ODE ICs. KX then lowers σ₈ further, by 7–8 % (cap) and 28–37 % (P1).

**KiDS.** At N ≤ 384 (k_hi ≤ 3 h/Mpc) no KiDS point keeps 90 % support, so every pair is NOT DIAGNOSTIC (scorer 4/4 checks,
CFG596 reproduced). The frozen 512³ cells are still the shear test.

**Halos (z = 0; a 384³ cell is 0.38 Mpc).** No cell reaches 1e14 M_⊙: the cluster class is empty except in S0, whose
dust-to-baryon ratio is the cosmic 5.27 by construction.
- **ODE ICs, KX-can 384³:** 20 galaxy-mass halos. Dust/baryon is 4.11 in 0.3–1 Mpc and 4.73 in 1–3 Mpc. Satellites
  (n = 3): 4.27 / 4.62. Field (n = 17): 4.09 / 4.76.
- **LIN 384³:** 165 halos. Satellites (n = 26): 4.33 / 4.73. Field (n = 139): 4.14 / 4.85.
- So the khronon is **under**-represented in halo cores relative to cosmic (×0.78–0.82 in 0.3–1 Mpc). Satellites are only
  ~3 % richer than field halos.
- **DBI and LOB cells form no halo** above the 20×-mean peak threshold (σ₈ ≤ 0.20), so they have no halo report.
- **The owner's question gets a "no" at this resolution:** v3's own dynamics from BBN-consistent ICs puts no extra cold
  energy into satellites or cores, and in fact less than cosmic. Every result here is "v3 on a dust background with a
  yet-unspecified early K" (A4), except the DBI cells, whose early K is BS25's.

## Files and commits

**Criteria and amendments**, each committed before the results it governs:
- `FROZEN_CRITERIA.md` (062b199c77), committed alone first;
- A1 (ea9baeddca, pre-result);
- A2 (0bac03ce31, post-result: the KA script bug and KB as above);
- A3 (0bac03ce31, pre-result for the indicative set and production);
- A4 (9948b6a5f0, pre-result: Q6 sentence and LOB-IC).

**Engine and checks:**
- `khronon_pm.py`, the engine. Validation in `l1_khronon_pm.py` → `.out` and `_results.json`; the `_MUTATE` and `_RUN1`
  files are kept.
- `l1_indicative.py`, `l1_lob.py` and `l1_score.py`, each with `_MUTATE` outputs. The scorer's machinery test is labelled
  `_indicative128`.

**Runs.** Every run: `OMP_NUM_THREADS=1 nice -n 15`, one thread, at most 128³ (A1). `work/` is scratch and is not committed.

## What this does not show

- It does not show v3's nonlinear growth or its KiDS score at production resolution. Only the frozen 512³ cells decide those.
- No run covers z ≈ 1000 → 200, where x ≫ 1. Literal v3 has no valid early history there (Q6).
- The khronon is represented by collisionless particles, so it can multistream after shell crossing. BS's khronon is
  single-stream.
- The galactic law and the EFE are not tested. L★ is far below the cell.
