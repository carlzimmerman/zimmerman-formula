# CFG650 FROZEN CRITERIA: the combined "theory v2 candidate" PM engine, native 1024³ shear test of the module combination

Date: 2026-10-12. Committed ALONE, before any CFG650 256³ preview number was seen and before any CFG650 1024³ run.
The engine file `cfg650_pm.py` is committed separately after this file, together with its validation. This file is never edited;
dated disclosures go in the README.

## 0. Disclosure: what was seen before this file was written

- **CFG596's canonical RESULT** (41efda383): candidate B (phantom sourced by all retained baryons) EXCLUDED on raw KiDS-1000
  (Δχ² +68.7, robustness minimum +43.9, T-OWN pass, NZ1 bites); DES Y3 +22.4 NOT DIAGNOSTIC; own boost 1.19 / 1.25 / 1.21 at
  k 0.3 / 0.5 / 1 h/Mpc. No alt verdict (P2 stopped).
- **Module evidence already on record, all seen:**
  - M1: CFG647 (1bf39b8da): no engine bug; pooling across overlapping catchments imports 10% of the z = 0 settled mass (13.5% in
    hosts ≥ 10^13.5); removing the import STATICALLY lowers the own boost to 1.131 / 1.168 / 1.158 (one-sided, no re-evolution).
  - M2: CFG640 criteria 71b2cc1c9 and its 256³ PREVIEW (6b8a3776c): P_grav/P_S0 at z = 0 = 1.055 / 1.103 / 1.099 (G 0.116).
    CFG634: H-CB NOT DECIDED (reservoir-limited). CFG640's 1024³ run has NOT run; CFG636 C1 (census cap) is running, unscored.
  - M3: CFG646 declarations (3c1c5a42f) and its committed-to-disk PM post-process estimate (cfg646_expulsion_pm.out, read):
    DIFF-S P'/P at z = 0 = 0.977 / 0.966 / 0.950 at k 0.3 / 0.5 / 1 on CFG596 P1's own fields (resolution-limited estimate).
  - M4: CFG648 FROZEN CRITERIA only (2e9dffba1); no CFG648 number exists; CFG648 has not written its native PM spec.
  - M5: CFG644 FROZEN CRITERIA only (6a03c0870); no PM spec.
- **Owner/orchestrator correction (applied here):** astra's ΛCDM-dependency audit (`sol61_push/lcdm_dependency_audit_2026_10_12/
  RESULT.txt`, item D) is accepted: CFG636's "growth gate" max|P_F/P_S0 − 1| ≤ 0.10 compares against S0, an unmodified matter run
  on inherited ICs/background; it is a BENCHMARK, not an observational exclusion. In CFG650 it is reported, labelled, and carries
  NO verdict weight (section 5).
- **Settings:** κ = ½ is FITTED. Footings 9.3603e-11 / 1.1312e-10 m s⁻², never pooled. "Cold energy" throughout; its MASS is still
  required; no particle species. Not "theory closed". Nothing here may say the data favour the framework. No ΛCDM or
  standard-MOND yardstick in any verdict.

## 1. Engine and modules (each an independent switch, default OFF = cfg596_pm.py @6323b630f bit for bit)

| switch | module | rule (source of the spec) | status of the spec |
|---|---|---|---|
| `CFG650_M1` | per-host supply | the supply pool is the OWN HOST, not the connected component of overlapping turnaround balls. Every catchment cell belongs to the resolved host with the smallest d/r_ON (periodic distance to the host's peak cell over its r_ON; ties → larger host). q_h = E_h/R_h, the cap q ≤ 1 and the shell draw are per host; zero-sum per host. | FINAL: CFG647 README reproduction plan + `cfg647_audit.membership` rule, verbatim |
| `CFG650_M2` | condensed source | per-particle condensed fraction f_d (float16, irreversible), raised at dynamical census refreshes to f_c,k = 0.10 + (f_ret,k − 0.10) χ_cool,k; the law's MOND input = CIC deposit of f_d; census edge from f_c. | FINAL: `cfg640_pm.py` @6b8a3776c code COPIED (CFG640 criteria 71b2cc1c9) |
| `CFG650_M3` | gas expulsion | the census non-retained baryons e = f_b (1 − f_ret,census(x))(1 + δ) in every catchment cell are removed from the gravitating source and re-placed as each catchment class's e smoothed by a unit Gaussian of σ = that class's r_ON (mass conserved: the k = 0 weight is exactly 1). Particles are not moved (tracers of the total); only the source the potential is solved from changes. f_ret here is ALWAYS the census value (M2 changes only what sources the law, not what the halo retains). | PRIMARY placement FINAL (CFG646 declarations: CFG632 DIFF; grid realisation DIFF-S of cfg646_expulsion_pm.py). CFG646's own native PM spec (its part iii) is NOT committed: CFG650 freezes DIFF-S as written here (TODO in the engine to align; any later CFG646 spec is a separate lane) |
| `CFG650_M4` | phase-mixed gate | each particle carries one byte: bit0 = infalling at the last check (physical radial velocity about its own host < 0, own host by the M1 rule, host bulk momentum = mean momentum of the particles in its own-host cells), bit1 = PHASE-MIXED (bit0 set and now v_r ≥ 0 while in a host: first pericentre passed; irreversible). Checked after every step's kick. Settling is gated by the phase-mixed mass fraction φ = ρ_pm/ρ of each cell: e → φ e and the shell supply is drawn only from φ s_c (1 + δ). First-infall material does not settle and is not drawn. | PLACEHOLDER (CFG648 H-SP criteria 2e9dffba1 state the physics; CFG648's native PM spec is not written). Declared here, frozen |
| `CFG650_M5` | neighbour-bounded edge | — | STUB (CFG644 has no PM spec); the switch raises |
| `CFG650_IC` | IC normalisation | `sigma8` (inherited, default) or `As` (bracket, section 6) | — |

**Structural choices (every one listed; none is a tuned number, none is varied in the verdict):**
S-a M1 partition = smallest d/r_ON (CFG647), not the potential-dominance alternative; catchment cells no host ball covers (FFT
threshold) go to one orphan bucket, counted (must be 0 at 256³ validation, reported). S-b M1 keeps CFG596's edge mask, f_sw, cap
rule and shell definition. S-c M2 = CFG640's K1–K5 choices unchanged. S-d M3 placement width = the class r_ON (DIFF-S); the
expelled mass stays in the particles' dynamics only through the total source (no separate gas tracer); expulsion acts at every
force evaluation on the current catchment state (instantaneous; no ejection time). S-e M4 pericentre = sign change of the physical
radial velocity (v_pec = p H0/a plus the Hubble term H a r, the engine's own background) about the host's peak cell; host labels are
the census-refresh labels (renumbered every 10th call; the bit0 memory is not reset on relabelling); the gate is the continuous
fraction φ, not a threshold; φ is clipped to [0, 1]. S-f all module state is advanced only on dynamical calls (snapshot calls are
measurement only, as in CFG596/640), except that the non-extra snapshots refresh the catchment, f_ret and host labels exactly as
CFG596 does.

## 2. The combination tested at 1024³ (rule declared now, before any CFG650 preview)

**Rule:** the combination = every implemented module (M1–M4) whose standalone lane has NOT committed a FAIL verdict for its
hypothesis. At this freeze: M1 (CFG647: no FAIL, an audit), M2 (CFG634 NOT DECIDED; CFG640 native not run), M3 (CFG646:
estimate, no verdict), M4 (CFG648: no result) → **T1 = M1 + M2 + M3 + M4** (canonical), T2 = the same on the alt footing.
**CFG648 clause:** if CFG648 commits a RESULT whose verdict for H-SP with the condensed-only (H-CB) source is "FAILS" before T1 is
launched, M4 is dropped and **T1x = M1 + M2 + M3** runs instead (T2x for alt). The orchestrator applies this clause when it starts
the waiter (`CFG650_JOB=T1` or `T1x`); no other change of the combination is allowed, whatever the previews show. M5 is excluded
(stub). The 256³ previews (section 4) are reported, never used to choose.

## 3. Production runs (the waiter is created, NOT started by this lane's author)

- T1 (or T1x): RES canonical, L = 100 Mpc/h, N = 1024, NSEED 1024, seed 359, RMIN 0.78125, lean, spill, 14 threads, nice 10, the
  150-step grid and snapshots of CFG596 (z = 1, 0.5, 0 + measurement-only extras). T2 (alt) afterwards. **S0 = CFG596 P0** (shared,
  read only; same seed and box → same-pipeline pair).
- **Start condition (`cfg650_waiter.sh`):** no cfg596_pm.py / cfg636_pm.py / cfg640_pm.py / cfg650_pm.py engine process running, and
  free + inactive memory ≥ 48 GB. Nothing is killed. Queue order versus CFG640 is the orchestrator's decision.
- **Abort rule:** RSS > 52 GB or system swap growth > 4 GB (the modules add ~3.2 GB of per-particle state over CFG596's 40.4 GB peak);
  disk guard as CFG596. Estimated wall time 1–1.5 days (M2 and M4 each add one weighted deposit per force call; M3 adds one FFT pair
  per catchment class per call; M4 adds two particle passes per step).

## 4. Validation (before production; 256³ L100 NSEED 512 RMIN 0.78125, lean, ONE process ≤ 3 GB, nice 10)

- **V-0 (must pass):** all modules OFF must equal CFG596 VLr (`cfg596_work/VLr`) BIT FOR BIT: every stored snapshot quantity of all
  six snapshots, difference exactly 0. Fail → no production.
- **V-2 (must pass):** M2 alone must equal CFG640 VPh (`cfg640_work/VPh`) bit for bit (the copied code is CFG640's).
- **V-C (must pass, each module alone and every combination run):** run completes, finite; mass conservation: settled source
  |src_sum|/e_sum ≤ 1e-5 at z = 1, 0.5, 0; M1 max per-host |Σ src|/E_h ≤ 1e-4 and 0 orphan cells; M3 |Σ(placed − removed)|/Σ removed
  ≤ 1e-5.
- **V-D (reported, not gating):** direction of each module alone at z = 0 relative to V-0: the intended direction is a LOWER settled
  source (e_sum) and a lower P_grav at k 0.3–1 for M1, M2, M4; for M3 a lower P_grav at k ≥ 0.3. A module that moves the other way is
  reported as such (it still enters T1 by the section-2 rule).
- **Preview table (reported only, labelled "PREVIEW 256³, NOT a verdict"):** ΔP_grav/P_S0 at k 0.3 / 0.5 / 1 at z = 0 (S0 = CFG596
  VLs) for: each module alone, M1+M2, M1+M2+M3, all ON.
- **CMB-safety checklist (CFG649):** not committed at this freeze; if committed before the previews finish, run on the previews and
  reported only.

## 5. Statistic, data and verdict (identical to CFG636 89aeaae12 = CFG596 f6c27d401, with the growth gate DEMOTED)

- **Scorer:** `cfg650_native.py` = `cfg640_native.py` (= cfg636_native.py) pointed at T1/T2 (framework) and CFG596 P0 (S0); CFG592's
  library exec'd unchanged.
- **Data:** raw KiDS-1000 and DES Y3 ξ± with their published covariances, n(z), cuts. **Support cut:** a point is kept if ≥ 90% of its
  integrand lies in [k_lo, k_hi], k_hi = πN/(4L) = 8.04 h/Mpc; N_kept < 10 → NOT DIAGNOSTIC.
- **Models:** framework = the run's MEASURED gravitating P(k, z) at z = 0, 0.5, 1 (CFG592 'F' path, B ≡ 1); S0 = P0's particle P.
- **Statistic:** Δχ² = χ²_min(T) − χ²_min(S0) per survey and footing, IA marginalised; positive = framework worse.
- **Robustness set:** widen2, noIA, DESI distances, held. **Classes:** EXCLUDED (Δχ² ≥ 9 and robustness minimum ≥ 9); TENSION (Δχ² ≥ 4);
  CONSISTENT (Δχ² < 4 and robustness maximum < 9); NOT DIAGNOSTIC otherwise, or N_kept < 10, or a failed T-OWN.
- **T-OWN tooth:** unchanged (S0 best-fit mock × B_foot(k) from CFG530's L100 N512 caches must refit to χ²_min ≥ 9).
- **NZ1 MUTATE:** unchanged (source zero → χ²_min(S0) to |Δχ²| ≤ 1e-9); `CFG596_MUTATE=1` run FIRST.
- **CMB-lensing gate:** if CFG649 has committed a RAW-DATA CMB-lensing statistic before T1 is launched, it is executed unchanged on
  T1's measured P_grav(k, z) and its class enters the verdict exactly like a survey class (EXCLUDED counts as EXCLUDED). If CFG649 has
  no committed raw-data form by then, the CMB gate is NOT EVALUATED and the verdict rests on KiDS/DES alone (stated).
- **Benchmark (reported only, NO verdict weight):** G = max_{k ≤ 1} |P_grav,T/P_S0 − 1| at z = 0 (and z = 0.5, 1), the σ8_grav ratio and
  P_grav/P_S0 at k 0.3 / 0.5 / 1, labelled "benchmark vs the inherited-input S0 control, not an observational exclusion".
- **Verdict per footing (raw data only):** FAILS natively if any diagnostic survey (or the CMB gate, when evaluated) is EXCLUDED;
  PASSES the shear side on a footing only if CONSISTENT on at least one diagnostic survey and no survey (or CMB gate) is EXCLUDED or in
  TENSION; a shear-side pass needs both footings. Otherwise TENSION / NOT DIAGNOSTIC as classed. Any pass is conditional on section 7.

## 6. Declared bracket: A_s-normalised ICs (reported only, never verdict-bearing)

`CFG650_IC=As`: the same EH no-wiggle shape and n_s = 0.965, normalised at z_i to the CMB primary amplitude
ln(10¹⁰ A_s) = 3.0448 (record value, XR26 P18; pivot 0.05 Mpc⁻¹) with the growing mode D(a_i) of the engine's own background
normalised to D → a in matter domination (no σ8 at a = 1, no back-scaling from today). Framework-consistent because the switch is off
before structure forms. Runs T1As (the combination) and S0As (its own S0 control), canonical, scored by the same scorer
(Δχ²(T1As − S0As) and each against the data), reported as a bracket after T1. Caveats stated with it: EH no-wiggle transfer, radiation
neglected in D(a_i) (~1.5% at z = 49), A_s itself from a ΛCDM-model fit of the CMB primary spectrum.

## 7. Inherited inputs (the verdict is CONDITIONAL on all of them; astra's audit list, A–C)

h = 0.6736, ω_b = 0.02237, ω_c = 0.1200 (hence Ω_m, f_b and the 5.364 cold/baryon ratio), n_s = 0.965; the σ8 = 0.811 normalisation of
the EH no-wiggle transfer with ΛCDM growth back-scaling to z_i = 49 and the matching IC velocities; the cfg361 Δ_ta(z) turnaround table
(ΛCDM shell ODE); the hard-coded 0.315 / 0.674 in M_ta and the catchment conversions; the census f_ret law and floor (CFG515);
the flat-Λ background E(a) in the engine and in the scorer's distances and lensing kernel; the scorer's Dgrow² continuation of P(k)
above z = 1 and its EH continuation below k_lo; the DESI distance variant's CPL chain; survey nuisance priors and covariances; massless
neutrinos; M2's cooling inputs (Tozzi & Norman Λ(T), μ, n_e/n_H). There is NO HMcode, NO BAHAMAS, NO halo-model mass function in the
verdict. A same-pipeline S0 does not cancel these inputs (astra audit, exact check).

## 8. Outputs

Lane folder: `cfg650_pm.py`, `run_650.py`, `cfg650_validate.py` → `.out/.json`, `cfg650_native.py`, `cfg650_waiter.sh`, `README.md`.
Arrays/logs: `../_external_data/cfg650_work/`. Every quoted number comes from a JSON.
