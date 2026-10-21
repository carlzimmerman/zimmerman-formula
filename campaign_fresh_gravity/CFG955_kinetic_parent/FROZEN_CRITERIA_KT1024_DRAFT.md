# DRAFT — NOT FROZEN — NOT CRITERIA. Kinetic-theory (K-T) 1024³ shear run: proposed frozen criteria for a future lane

**Status.** This is a draft written by CFG955 (task 5) for the owner and the orchestrator. It freezes nothing. It is not CFG955's
criteria (those are `FROZEN_CRITERIA.md`, 903cd8f1d) and it is not committed as frozen. A frozen version must be committed alone,
in its own implementation lane, after the 256³ validation gates below and before any 1024³ K-T number exists. Every number in §5
is an estimate from CFG952's NC1x baseline model.

κ = ½ FITTED. Footings never pooled. Raw data only. Cold energy (no particle species). Not "theory closed". A CONSISTENT class
never means the data favour the framework.

## 0. What the run tests and what it does not

**Tests.** Whether the gravitating field of CFG955's kinetic reading K-T reproduces class A's shear pass (T1x / T2x; native NC1x /
NC2x). K-T is cold dust with plain Poisson gravity whose velocities relax, inside each host's own domain, to a local Maxwellian at
the own-domain monopole Jeans temperature T_J. Mass and momentum are conserved per bin; the energy is booked to a reservoir. There
is no phantom field (E4 off), no source S (E6–E8 off) and no RMIN beyond resolution.

**Why a run is needed.** CFG955 found that class A's E6–E8 is K-T's late-time attractor for isolated relaxed hosts, not its τ → 0
limit (L1). The shear passes therefore do not transfer by derivation. They differ in:
- the timing of relaxation (flow-limited, not instantaneous);
- the clip (K-T relaxes native surplus; class A keeps it);
- E4's global phantom (K-T has none);
- RMIN (K-T relaxes hosts down to the mesh);
- collisional mixing of streams inside domains (L6).

**Not tested.** The reservoir's identity (CFG955 L7: a heat bath at T_J; a coherent zero-entropy partner cannot be it), C-ret
(retarded targets) and the selection of τ (no record-derived τ separates clusters from rotators; CFG955 §3).

**Warning from CFG955 (a) — read before approving.** In CFG955's spherical toy, K-T's relaxed law state is not kept:
- every start collapses centrally (69–91% of the dust inside r < 0.5, against the law's 1.2%);
- PH4 (post hoc) finds the thermostatted SIS phantom linearly unstable, with NGC 3198 e-folding in 0.21–0.25 Gyr.

At 98 kpc/h the mesh cannot resolve galaxy-scale collapse, so this run would mostly test the resolution-limited behaviour of the
relaxation, not the theory's small-scale state. The owner should decide whether a run of an unstable theory is informative before
any heavy job.

## 1. Engine (a new lane's copy of the CFG654 engine; nothing in CFG650 / CFG654 is edited)

| switch | content |
|---|---|
| `KT=1` | turns E4 (`f_mond`) and E6–E8 (deficit, edge, zero-sum draw) **off**: the gravitating source is the particles only (+ M3's re-placed gas, unchanged) |
| `KT_DOM` | domains = the engine's resolved peaks (E3 criterion) with latched identity from first detection (`LDT_LATCH=catch` machinery, CFG952); cells to hosts by M1 (smallest d/r_ON) |
| `KT_RMIN=res` | a host is kept iff its own edge r_e ≥ 2 dx (dx = 100/1024 Mpc/h comoving), i.e. M_b ≥ 1.92e10 (canonical) / 2.32e10 M⊙ (alt) (CFG955 L3; 51 / 48 SPARC galaxies lie between this floor and class A's 2.19e11); E3's 14-node r_ON grid is extended down to dx so that such hosts are found. **This replaces RMIN = 0.78125 / effective 1.0471 Mpc/h** |
| `KT_TJ=mono` | per host: monopole of the condensed-baryon deposit (M2's f_d) about the host's condensed-baryon centroid in 64 log bins out to r_ON; phantom M_ph(<r) = r²[g_law(ḡ) − ḡ]/G with ν_mono; supply root r_e from the host's in-domain particle cold mass; T_J(r) = (1/ρ_ph)∫_r^{r_e} ρ_ph g_law dr (zero pressure at r_e) |
| `KT_TAU=T1` | τ = τ_ff/(2α), α = 1, τ_ff = (4πGρ_m)^{−1/2} with ρ_m the bin's total particle density (CFG638's pressure-relaxation time; CFG955 T1) |
| `KT_RELAX` | every step, for particles with r < r_e in their M1 host: resample with probability 1 − exp(−Δt/τ_bin), v_new = ū_S + √T_J(r̄_S)(ξ − ξ̄_S) per (host, bin) subset S, so the subset's momentum is kept exactly (CFG955's toy rule). ΔK is booked to `E_R` per step |
| `KT_SPECIES=whole` | particles carry baryons and cold energy in fixed proportion (E1), so whole particles are relaxed. The baryon share (f_b = 0.157) is relaxed too, a disclosed approximation at the 98 kpc/h cell (galaxies are unresolved). The two-species alternative doubles the particle memory (> 52 GB); it is rejected for 1024³ |
| M2, M3 | as in NC1x (condensed source deposit used only for T_J; M3 expulsion unchanged) |

**Inputs.** native_cmb (CFG654 A1); seed 359; L = 100 Mpc/h; N = NSEED = 1024; lean; spill; 14 threads; nice 10; CFG596's step grid
and snapshots.

**Jobs.** KT1c (canonical a₀ 9.3603e-11), KT1a (alt 1.1312e-10). **Control: NCS0** (existing; native_cmb, same ICs; it reads
neither footing nor source).

## 2. Validation gates (implementation lane; 256³; one process ≤ 3 GB)

| gate | line |
|---|---|
| V-R | `KT=0` is bit-for-bit the CFG654 engine |
| V-MOM | total particle momentum per step: \|ΔP\|/(M v_rms) ≤ 1e-10 with relaxation on (CFG955 planar toy: 1e-13 achieved) |
| V-MASS | particle count exact; M3 placement imbalance ≤ 1e-8 (as CFG650 V-C) |
| V-BOOK | E_kin + W + E_R conserved to the engine's own integrator error with relaxation off (×2) |
| V-PROF | isolated resolved hosts at 256³ that have relaxed (age/τ ≥ 2.3 at r_e/2): stacked gravitating M(<r)/M_law(<r) within 10% over 2–6 dx (law in the spherical-equivalent convention; disc geometry is not resolved) |
| V-RES | the host count and mass function above and below the class-A effective RMIN, reported |
| V-MEM | 1024³, MAXSTEPS = 3, peak RSS ≤ 47 GB (a heavy job; needs approval) |

## 3. Statistic, data, classes (unchanged from CFG654 FROZEN_CRITERIA + A1, as CFG952's draft)

- **Scorer.** CFG654's native scorer with `load_lib("native_cmb")`, on the K-T run's gravitating (particle) P(k, z) at z = 0, 0.5, 1
  against NCS0's. MUTATE first (NZ1, T-OWN), then main.
- **Data.** KiDS-1000 and DES Y3, published cuts plus the support cut; IA marginalised. Robustness set {widen2, noIA, held, LOC};
  DESI reported only.
- **Classes.**

| class | condition |
|---|---|
| EXCLUDED | Δχ² ≥ 9 and robustness min ≥ 9 |
| TENSION | Δχ² ≥ 4 |
| CONSISTENT | Δχ² < 4 and robustness max < 9 |
| NOT DIAGNOSTIC | otherwise, N_kept < 10, or failed T-OWN |

The CMB-lensing gate is as CFG654 §5: NOT EVALUATED unless a committed raw-data form exists.

## 4. Pre-declared readings (per footing)

| reading | condition |
|---|---|
| HOLDS | CONSISTENT on KiDS and Δχ²(KT1 − NCS0) ≤ 0 |
| WEAKENED | CONSISTENT and Δχ² > 0 |
| FAILS | EXCLUDED or TENSION on any diagnostic survey, or not CONSISTENT |

**Theory-level reading.**
- Both footings HOLD ⇒ "the kinetic theory K-T (τ = T1) keeps the shear side on both footings". It remains conditional on:
  - CFG654 §6's shared inputs;
  - the census supply;
  - the reservoir R (CFG955 L7);
  - C-ret;
  - the whole-particle relaxation approximation.
- Either footing not HOLDS ⇒ "class A's shear pass does not transfer to its kinetic parent K-T; the pass rests on class A's
  instantaneous, clipped, global-phantom source".

**Reported, no verdict weight.**
- Δχ²(KT1 − NC1x / NC2x);
- P_grav/P_S0 at k 0.3 / 0.5 / 1;
- the per-step momentum book and E_R (energy to the reservoir per step and cumulative, in units of the box's kinetic energy);
- the relaxed mass fraction R(t) per host mass bin;
- the native-surplus mass that K-T relaxes and class A would keep (the clip difference);
- the host count between the K-T resolution floor and class A's effective RMIN;
- the multi-stream mixing measure (relative kinetic energy removed by relaxation in hosts with two identified streams).

## 5. Cost (estimates from CFG952's NC1x baseline model; not results)

**Baseline.** NC1x: 16.27 h compute (per step: deposit 105 s, forces 193 s, accel 63 s), peak RSS 44.33 GB. One particle pass
t_pass ≈ 105 s; one full 1024³ transform ≈ 2 s; host peaks 32k–63k.

| item | Δ per step | note |
|---|---|---|
| E4 off (11 full-box transforms, `ysq`) | −22 s (−15 to −33) | −4.3 GB resident |
| E6–E8 off (deficit / edge / draw assembly) | −10 to −30 s | the census and peak finding stay (domains, M1) |
| r_ON grid extended to dx (more hosts: est. ×2–4) | +5 to +15 s | host tables are small (64 bins × ≤ 2.5e5 hosts × 8 B ≈ 0.13 GB) |
| relaxation pass: host gather, radius, bin, subset sums | +1 pass (≈ 105 s) | chunked over Lagrangian blocks; per-(host, bin) accumulators ≤ 0.13 GB |
| resampling + velocity write | +0.5–1 pass (50–105 s) | 3 normals per resampled particle (≤ 3.2e9 per step, chunked) |
| **net per step** | **+100 to +185 s** | |

**Per footing.** About 21–25 h of compute per footing if relaxation runs every step (16.27 h × (361 + 100…185)/361). Two footings
take 42–50 h serial, about two days. A census-cadence variant (every 10th force call, E11) would cost about 17 h per footing but
leaves dust collisionless for about 1 Gyr between relaxations at late times. It is reported at 256³ only.

**Memory.** 44.33 − 4.3 + ≤ 1.5 (chunk buffers) + ≤ 0.3 (host tables) ≈ 41–42 GB, within the 47 GB design line and the 52 GB abort
line.

**Disk.** Unchanged plus ≤ 1 GB of logs and E_R and momentum books.

## 6. Run order and rules

1. Owner approvals (§7).
2. Implementation lane: engine copy and switches; V-R, V-MOM, V-MASS, V-BOOK, V-PROF and V-RES at 256³.
3. Freeze the criteria (committed alone), from this draft with any dated changes.
4. V-MEM 1024³ 3-step probe (approval).
5. KT1c, only when no other 1024³ job and no heavy server is running.
   - Start rule: free + inactive ≥ 48 GB and free disk ≥ 20 GB.
   - Abort rule: RSS > 52 GB or swap growth > 4 GB.
   - No other lanes beside it.
6. Score KT1c (MUTATE first).
7. KT1a under the same rules; score.
8. RESULT, README and LEDGER row.

## 7. Owner approvals needed

1. Whether to run K-T at all, given CFG955's class (CONDITIONAL, relation ATTRACTOR) and its unidentified reservoir.
2. Heavy runs: two 1024³ jobs (≈ 21–25 h each) plus the V-MEM probe, serial, nothing heavy beside them.
3. Theory choices, each a declared cost:
   - τ = T1 (CFG638's τ_π; α = 1);
   - whole-particle relaxation;
   - latched domains from the engine's peaks;
   - the monopole own-domain T_J;
   - the supply-root edge from in-domain particle cold mass;
   - no RMIN beyond r_e ≥ 2 dx.
4. Reuse of NCS0 as the control, and of CFG654's frozen scorer unchanged.

κ = ½ FITTED; footings never pooled; cold energy mass required; not theory closed.
