# CFG952 PRE-REGISTRATION DRAFT: the first 1024³ labelled-domain run (NOT FROZEN; NOT criteria)

This is a draft for the owner and the orchestrator. It freezes nothing. A frozen version must be committed alone, in the
implementation lane, after the 256³ validation gates and before any 1024³ LDT number exists. κ = ½ FITTED. Footings never
pooled. Raw data only. Not "theory closed". A CONSISTENT class never means the data favour the framework.

## 0. What the run can and cannot test (from CFG952's smoke tests)

**Can test.** Labels assigned at turnaround and kept through infall, plus each label's own-domain phantom (no EFE), in place of
class A's global phantom (E4, which carries −0.11 dex in the toy). Merges are blended.

**Cannot test yet.** A momentum-conserving formulation (B): the dipole-preserving positive draw is infeasible in asymmetric
domains and mergers (CFG952 b1, c2). This draft therefore defines **LDT-B0**: labels + own-domain phantom + per-label uniform
draw (`e8`, class A's M1 rule applied per label). Its momentum non-closure is reported, as it is for class A (CFG947 T-M).

**Not covered.** The full LDT test needs CFG950's formulation (A) engine (CFG952 DESIGN §8). That is a later pre-registration.

## 1. Runs

**Engine.** A new lane's copy of the CFG654 engine plus the CFG952 switches, with these settings:
- `LDT=1`, `LDT_LATCH=catch`, `LDT_RDOM=mass`;
- `LDT_OWN=exact3d` (or `hybrid`, chosen from the V-LDT label count before freezing, never after);
- `LDT_SC=own`, `LDT_DRAW=e8`, `LDT_XH=1.0` (the engine's E7);
- `LDT_MERGE_TRIG=tc`, `LDT_MERGE_MODE=blend`, `LDT_RMIN=r0`;
- M2 (condensed f_d) and M3 (expulsion) as in NC1x; M1's per-host pool is replaced by the per-label pool.

**Inputs and settings.**
- native_cmb (CFG654 A1); seed 359; L = 100 Mpc/h; N = NSEED = 1024; lean; spill; 14 threads; nice 10.
- CFG596's 150-step grid and snapshots (z = 1, 0.5, 0, plus the extras).

**Jobs.**
- **NLB0c:** canonical footing (a₀ 9.3603e-11).
- **NLB0a:** alt footing (1.1312e-10).

**Control: NCS0** (existing; native_cmb, same ICs). S0 reads neither the footing nor the source, so no new control run is needed.

**Validation gates before any 1024³ job** (implementation lane; one process ≤ 3 GB at 256³):
- V-R: LDT off, bit for bit equal to the CFG654 engine.
- V-LDT: zero-sum ≤ 1e-10 per label, the label count and size distribution, strays, own-vs-global phantom discretisation, and
  timing / RSS scaling.
- V-RMIN: `r0` vs `r2`, reported.
- V-MEM: 1024³, MAXSTEPS = 3, peak ≤ 47 GB (a heavy job; it needs approval).

## 2. Statistic, data, classes (unchanged from CFG654 FROZEN_CRITERIA + A1)

**Scorer.** CFG654's native scorer with `load_lib("native_cmb")`, scoring the LDT run's gravitating P(k, z) at z = 0, 0.5, 1
against NCS0's particle P. MUTATE first (NZ1, T-OWN), then main.

**Data and fit.** KiDS-1000 and DES Y3, with the published cuts and the support cut; IA marginalised.

**Robustness set.** {widen2, noIA, held, LOC}. DESI is reported only.

**Classes.**

| class | condition |
|---|---|
| EXCLUDED | Δχ² ≥ 9 and robustness min ≥ 9 |
| TENSION | Δχ² ≥ 4 |
| CONSISTENT | Δχ² < 4 and robustness max < 9 |
| NOT DIAGNOSTIC | otherwise, N_kept < 10, or failed T-OWN |

**CMB-lensing gate.** As CFG654 §5. NOT EVALUATED unless a committed raw-data form exists.

## 3. Pre-declared reading (per footing)

| reading | condition |
|---|---|
| HOLDS | CONSISTENT on KiDS and Δχ²(NLB0 − NCS0) ≤ 0 |
| WEAKENED | CONSISTENT and Δχ² > 0 |
| FAILS | EXCLUDED or TENSION on any diagnostic survey, or not CONSISTENT |

**Theory-level reading.**
- Both footings HOLD ⇒ "LDT-B0 (labels + own-domain phantom, momentum-nonconserving draw) keeps the shear side on both footings".
  It stays conditional on CFG654 §6's shared inputs, the empirical census, the effective RMIN M_b,ret ≳ 2e11 M⊙ and the
  non-conservation book.
- Either footing not HOLDS ⇒ "the EFE-free own-domain phantom does not keep class A's shear pass".
- Neither reading is a test of momentum-conserving LDT.

**Reported, no verdict weight.**
- Δχ²(NLB0 − NC1x / NC2x): does the EFE fix move class A's result?
- The benchmark P_grav/P_S0 at k = 0.3 / 0.5 / 1.
- The per-step momentum non-closure.
- Label counts and merger log; the own- vs global-phantom mass per refresh.
- The fraction of collapsed mass in peaks below the effective RMIN.

## 4. Run order and rules

1. Owner approvals (§5).
2. Implementation lane: engine copy and switches; V-R, V-LDT and V-RMIN at 256³.
3. Freeze the criteria (committed alone), including the `exact3d` / `hybrid` choice from V-LDT.
4. V-MEM 1024³ 3-step probe (approval).
5. NLB0c, only when no other 1024³ job (NC2x included) and no heavy server is running.
   - Start rule: free + inactive ≥ 48 GB and free disk ≥ 30 GB.
   - Abort rule: RSS > 52 GB, swap growth > 4 GB, or more than 3 ragged batches.
   - No other lanes beside it.
6. Score NLB0c (MUTATE first).
7. NLB0a under the same rules; score.
8. RESULT, README and LEDGER row.

**Estimated cost.** About 17–18 h per footing if the alive label count stays ≲ 5000 (27 h at 2e4; 47 h worst, every peak a
label). That is 1.5–2 days serial in the expected case. Peak RSS is 43–47 GB with labels on disk.

## 5. Owner approvals needed

1. **Whether to run LDT-B0 at all,** or to wait for CFG950's verdict and a formulation (A) engine. B0 tests only the EFE fix plus
   labels.
2. **Heavy runs.** Two 1024³ jobs (≈ 17–27 h each), plus the V-MEM 3-step probe, serial, with nothing else heavy beside them.
3. **Disk.** About +12 GB transient (labels file, checkpoint copies, S_ℓ spill). The disk start rule is raised to 30 GB.
4. **Theory choices, each a declared cost** (CFG950 / CFG951 may supply canonical ones first):
   - the draw `e8` (momentum non-conserving);
   - merge trigger `tc` and mode `blend`;
   - XH = 1 (engine edge, q = 1, no headroom);
   - RMIN `r0` (law off for M_b,ret ≲ 2e11 M⊙ at 1024³);
   - the own-cold deficit;
   - domain radius from label mass.
5. **Reuse of NCS0** as the control, and of CFG654's frozen scorer unchanged.

κ = ½ FITTED; footings never pooled; cold energy mass required; not theory closed.
