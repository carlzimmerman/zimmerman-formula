# CFG960 FROZEN CRITERIA 1024: the pre-registered 1024³ native-input shear test of SCT-M

Committed ALONE. It follows the 128³ validation (FROZEN_CRITERIA.md 6fc440225; A1 1e5ebf105; A2 fbfc2bcf5; A3 8ddc764b2; A4 887e5dbd1;
validation outputs 32ccc6ffe) and comes before any 1024³ CFG960 job. This file is never edited; later changes are dated, labelled
amendments. **This lane starts no 1024³ job. The orchestrator starts it under the overnight gate after review.**

**Settings.** κ = ½ FITTED. Footings canonical a₀ = 9.3603e-11 and alt 1.1312e-10 m/s², run and scored separately, never pooled.
Cold energy mass required; no particle species. Raw data and framework-native inputs only: no HMcode, BAHAMAS, ΛCDM mass function or
other ΛCDM nonlinear yardstick enters the verdict. Not "theory closed" whatever happens; a CONSISTENT class never means the data
favour the framework.

## 0. The question, and what was seen before this file

**Question.**
- The class-A engine (theory-v2: CFG650 M1 + M2 + M3 with the E-rules) passes raw KiDS-1000 on both footings with native inputs:
  NC1x −10.08 (canonical), NC2x −9.39 (alt); CFG909 finds the class ROBUST but the size amplitude-driven.
- That engine has no physical parent (CFG947, CFG955).
- SCT-M (CFG953, CONDITIONAL on galaxy scales; clusters FAIL in CFG954) is a theory with a conserved, galaxy-consistent parent.
- Does SCT-M, growing its own structure from the same native initial conditions, still pass?
  - A pass gives the shear result a parent.
  - A fail means the pass depends on class A's parentless rules: the global QUMOND phantom E4, the E8 relocation, RMIN.

**Seen before this file (disclosed).**
- All 128³ validation numbers (cfg960_validate.out), including the PREVIEW, which is NOT A VERDICT:

  | footing | P_grav/P_S0 at k = 0.3 / 0.5 / 1, z = 0 |
  |---|---|
  | canonical | 0.959 / 0.881 / 0.628 |
  | alt | 0.965 / 0.902 / 0.679 |

- A2's diagnosis of that preview. Cluster bodies at 128³ are more extended than the resolution-limited dust halos. M2's condensed
  own-baryon fraction sits at the census floor 0.10 at every resolved mass, so N = M_c/M_b ≈ 54 even for clusters.
- The gate record:
  - every gate passes except V-N1's growth sub-line, which fails as frozen (A2);
  - SCT-M grows like dust to ≤ 0.4%, and plain dust shows the same ≈ 5% baseline;
  - V-MUT bites.
- The stored NC1x / NC2x / NCS0 run JSONs and their scores.
- No SCT-M number at any resolution above 128³ exists.

## 1. Engine, inputs and files (sha256; a VOID condition, §4)

| file | sha256 | role |
|---|---|---|
| `cfg960_sctm_pm.py` | 3ede8034050de3cb3753e4819041320f898583236a68597f3a1f613e51247cc5 | SCT-M engine (S1–S13, U1–U13, A3/A4 hybrid painting) |
| CFG654 engine (imported read-only; asserted by the engine) | 7058f4333b8d45970af932f889ba00aa1e67372cd2f04f21d2df1da471f631c6 | ICs, background, mesh, finder, M2 census, M3, measurement |
| `run_960.py` | c3de055174a8fe7e7fb381af22b5beb6cf4ff01fee42d4ae610571d92e526106 | launcher: guards, work folders by job |
| `chain960.sh` | bb8538b1cdb870aeefe8c7f9bd44657ab50c566e7d24f2797f2080ccfcec73e2 | gate and resume chain (modelled on chain7b) |
| `cfg960_score.py` | b45b148b3e3f4f0a6b6061e6f00270bf82244370f47bd37b929e89779e216fbe | the frozen CFG654 scorer, wrapped; V-SCORE reproduced NC1x / NC2x exactly |
| CFG654 scorer (imported read-only; asserted) | e5e3da3bf442e1b91797c19e232e828d996c4b1c2d91753ebfc42d0ffc79e67f | statistic, data, cuts, classes |

**Inputs.** These are exactly NC1x / NC2x's: native_cmb (CFG654 A1), L = 100 Mpc/h, N = NSEED = 1024, seed 359, lean mode, CFG596's
150-step grid and snapshots (zi, z1, x0.7548, z0.5, x0.2562, z0), FLAT a₀ branch, kernel ν_mono, RMIN 0.78125 Mpc/h for M3's census
catchments only. The SCT-M domain floor is r_ON ≥ dx = 0.0977 Mpc/h (U1; ≈ 2e9 h⁻¹ M☉ of turnaround mass).

**Environment.** 14 threads; spill on; nice 10; `MallocSpaceEfficient=1` (A1; arithmetic unaffected); in-script RSS guard 52 GB.

## 2. Jobs (`run_960.py`; outputs in `_external_data/cfg960_work/<JOB>/`)

| job | content |
|---|---|
| **SC1x** | SCT-M, M3 unchanged, conversion on, **canonical** footing |
| **SC2x** | the same on the **alt** footing |
| control | **NCS0** (CFG654, existing): the native_cmb S0 on the same ICs. S0 never reads the footing, so one control serves both footings, as for NC1x / NC2x |

Order: SC1x, its score (MUTATE first), SC2x, its score (MUTATE first): `chain960.sh`.

**Start command** (the orchestrator, after review, under the overnight gate; from the repository root):

    cd campaign_fresh_gravity/CFG960_sctm_engine && nohup bash chain960.sh > ../../../_external_data/cfg960_work/chain960_nohup.log 2>&1 &

## 3. Start, abort, resume; cost

- **Start (gate).**
  - No heavy job running: CFG6xx engines, CFG650 / 654 launchers, CFG596, CFG960's own engine or launcher, or an Ollama llama-server.
  - Free + inactive memory ≥ 46 GB (as chain7b).
  - Free disk ≥ 45 GB.
  - Light single-core lanes do not block.
- **Abort (unchanged from CFG654):** RSS > 52 GB or swap growth > 4 GB (run_960.py); disk guard 3 GB.
- **Resume.** The engine writes a rolling checkpoint (particles, f_d, labels, domain table) after every step whose next force call
  refreshes the census. On a non-zero exit with a checkpoint present, `chain960.sh` restarts the job after the gate, up to 3 times
  per job. Labels and domains are in the checkpoint, so the resume is a bit-identical continuation, as in CFG654. Each resume is
  logged and disclosed.
- **Cost estimate per footing.** These are estimates, not results.
  - **Basis.** The NC1x / NCS0 timings at 1024³: deposit 105 s per step, accel 63 s, NCS0 7.9 h in all. The 128³ per-stage timings
    (cfg960_validate.json) are scaled by particle number for the particle passes and by mesh size for the FFT work.
  - **Per step:**

    | item | seconds per step |
    |---|---|
    | all-particle deposit | ≈ 105 |
    | converted-particle deposit | 30–60 |
    | label I/O | 10–20 |
    | conversion and profile passes | 20–40 |
    | refresh passes (finder, partition, births, merges), amortised | 30–60 |
    | bodies | 5–20 |
    | M3 | 40–60 |
    | Poisson | 4 |
    | accel | ≈ 70 |
    | **total** | **≈ 320–440** |

  - **Run.** 150 steps, plus about 1.2 h of snapshots and about 0.5 h of checkpoints, gives **about 18–30 h per footing** (central
    ≈ 22 h), in line with the engine's 20–40 h envelope. Two footings in series take about 1.5–2.5 days.
  - **Peak memory: about 43–47 GB per footing.** NCS0 peaked at 41.4 GB and NC1x / NC2x at 44.3 / 44.8 GB. SCT-M adds f_d (2.1 GB,
    as M2 in NC1x), the census transients (as NC1x), per-chunk pass buffers (≈ 0.5–1 GB), domain and profile tables (≤ 0.5 GB) and
    body arrays (≲ 0.3 GB after A3/A4). Labels live on disk (4.3 GB file).
  - **Disk.** Checkpoint ≈ 32.3 GB, label file 4.3 GB, spill temporaries, and 6 snapshot block files of about 0.12 GB each.

## 4. VOID conditions (any one ⇒ no verdict for that footing; reported; a rerun needs a new dated amendment)

| id | condition |
|---|---|
| V1 | `engine_sha256` in the run JSON ≠ 3ede8034…7cc5, or the CFG654 engine assertion fails |
| V2 | zi particle P(k) differs from NCS0's zi P(k) by more than 1e-6 relative at any k (same ICs; measurement-level last-bit effects allowed) |
| V3 | a snapshot of the six is missing, or a step is not finite |
| V4 | any step has \|Σ w + Σ M_c − N\|/N > 1e-10, \|Σ painted − Σ M_c\|/N > 1e-8, or event-algebra momentum residual > 1e-10 P_scale |

## 5. Statistic and data (CFG654 FROZEN_CRITERIA §5 + A1, unchanged; `cfg960_score.py`)

- **Run order.**
  1. `CFG596_MUTATE=1 python3 cfg960_score.py --score SC1x` runs first: NZ1 and the T-OWN tooth.
  2. Then without MUTATE. SC2x the same.
- **Model and data.**
  - Framework = SC's measured gravitating P(k, z) at z = 0, 0.5 and 1; control = NCS0's particle P(k, z).
  - Native scorer `load_lib("native_cmb")`.
  - Raw KiDS-1000 and DES Y3 with their published cuts and the support cut (≥ 90% of the integrand in [k_lo, π N/(4L)]; N_kept < 10
    ⇒ NOT DIAGNOSTIC); IA marginalised.
- **Robustness set:** {widen2, noIA, held, LOC}. DESI-chain distances are reported only.
- **Classes:**

  | class | condition |
  |---|---|
  | EXCLUDED | Δχ² ≥ 9 and robustness minimum ≥ 9 |
  | TENSION | Δχ² ≥ 4 |
  | CONSISTENT | Δχ² < 4 and robustness maximum < 9 |
  | NOT DIAGNOSTIC | otherwise, N_kept < 10, or failed T-OWN |

- **Δχ²** = χ²_min(SC) − χ²_min(NCS0) per survey; positive means the framework is worse.
- **CMB-lensing gate:** NOT EVALUATED in this verdict, as CFG654.

## 6. Pre-declared readings

**Per footing (SC1x canonical, SC2x alt):**

| reading | condition |
|---|---|
| **PASS** | KiDS-1000 is CONSISTENT **and** Δχ²_KiDS(SC − NCS0) ≤ 0, **and** no diagnostic survey is EXCLUDED or TENSION |
| WEAKENED | KiDS CONSISTENT, none EXCLUDED or TENSION, but Δχ²_KiDS > 0 |
| FAILS | anything else: KiDS TENSION, EXCLUDED or NOT DIAGNOSTIC, or a diagnostic DES EXCLUDED or TENSION |

**Theory level. SCT-M passes the shear side iff both footings are CONSISTENT with Δχ² ≤ 0 vs NCS0, i.e. SC1x PASS and SC2x PASS.**

- **Both PASS ⇒** "The native shear pass gains a parent. SCT-M is CFG953's galaxy-scale-consistent source-changing theory:
  CONDITIONAL on C-E and C-DF, with C-MR and C-c open and clusters failing in CFG954. Growing its own structure from the
  framework's native initial conditions, it passes raw KiDS-1000 on both footings."
  - It stays conditional on CFG654 §6's shared inputs, this lane's declared PM choices (U1–U13, A3/A4) and A2's U5 sensitivity.
  - It is a CONSISTENT class, not a preference.
- **Anything else ⇒** "The class-A shear pass depends on its parentless rules (E4's global phantom, E8's relocation, RMIN): SCT-M, a
  theory with a consistent galaxy-scale parent, does not reproduce it." The failing footing(s) and the class are stated.
  - WEAKENED on either footing counts as not passing.

Whichever happens is reported. No job, setting, statistic or data cut is added after this commit.

## 7. Reported, no verdict weight

- Absolute χ²_min and p per survey.
- Δχ²(SC1x − NC1x) and Δχ²(SC2x − NC2x) = χ²_F(SC) − χ²_F(NC), from the score JSONs (same control).
- The benchmark P_grav/P_S0 at k 0.3 / 0.5 / 1 and z = 0, 0.5, 1.
- SCT diagnostics per snapshot:
  - live domains, births, merges (bound / coalescence), labelled-majority peaks;
  - converted / pending / labelled mass fractions;
  - r_e in dx; inner points and outer nodes; fallbacks and caps;
  - the mass book, the momentum drift (M3 on, U12) and runtime per stage.
- If the orchestrator runs them separately: CFG909's amplitude sensitivity and CFG917's CMB-lensing statistic, as sensitivities.

## 8. What remains shared or conditional (stated with any verdict)

- **CFG654 §6:**
  - the Planck TT,TE,EE+lowE column from a base-ΛCDM chain;
  - H0 from θ*;
  - massless ν;
  - the empirical f_ret census and floor;
  - M2's cooling inputs;
  - survey nuisances and covariances;
  - the CFG530 boost of the T-OWN tooth;
  - seed 359.
- **SCT-M's own conditions** (CFG953): C-E, C-DF, C-MR, C-c. Clusters FAIL (CFG954).
- **This lane's PM choices U1–U13 and A3/A4:**
  - domain floor r_ON ≥ dx;
  - majority-rule domain assignment;
  - own baryons = M2's condensed fraction, at the floor 0.10, giving N ≈ 54 at all masses (A2);
  - no stripping; no blend;
  - spin and E_int not tracked;
  - M3's momentum effect.
- **V-N1's growth sub-line failed as frozen (A2).** SCT-M's large-scale growth equals dust's to ≤ 0.4%.

κ = ½ FITTED; footings never pooled; cold energy mass required; no particle species; not theory closed.
