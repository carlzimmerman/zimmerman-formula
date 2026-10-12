# CFG647: engineering audit of the settled cold-energy accounting in the CFG596 engine (crowded regions). Verdict: NO BUG; the per-component pooling RULE is a real crowding effect (about 10% of the settled mass at z = 0), but it does not by itself explain the KiDS exclusion

- **Date:** 2026-10-12. Criteria: `FROZEN_CRITERIA.md`, commit 2e1ea8c58, committed alone before any code or measurement.
- **Settings:** κ = ½ is FITTED. Canonical footing only: P1 is the only finished RES run. The cold energy's MASS is still required; no particle species. Not "theory closed".
- **Read only:** `cfg596_pm.py` (freeze 6323b630f) is imported unchanged; `cfg527_pm.py` is read only. Stored P1 outputs are read only. No simulation was run, and the running CFG636/CFG640/CFG625 jobs were not touched.
- **Scripts:**
  - `cfg647_audit.py` → `cfg647_audit.out/.json` (frozen measurements);
  - `cfg647_posthoc.py` → `cfg647_posthoc.out/.json` (POST-FREEZE, reported, never gating).

## How the settled source is built (cfg596_pm.py lines 615–795, identical to cfg527_pm.py 366–470)

1. **Hosts.**
   - Peaks are local maxima of δ with δ ≥ 3(τ − ε).
   - r_ON = the largest R on the 14-point grid whose top-hat mean is ≥ Δ_ta (`cover_peaks`).
   - Resolved hosts have r_ON ≥ RMIN.
2. **Masks** (`cover_balls`, each one a UNION of balls, so a cell is either in or out):
   - catchment = balls of radius r_ON;
   - census edge = balls of radius x_supply·r_ON. At z = 0, x = 0.28–0.45, so the edge sits at 0.28–0.45 r_ta, which is where CFG556 places the excess.
   - f_ret is painted per ball, and the largest host wins.
3. **Excess** (lines 710–716): e = f_sw·edge·max(s_ph − s_c(1+δ), 0)·catch.
   - s_ph is the phantom source of the retained baryons f_ret(1+δ).
   - s_c = 1.5Ω_m(1−f_b)/a is the particles' own cold share.
   - So inside the edge, the gravitating cold density is topped up to the phantom. The particles there are not removed.
4. **Supply** (lines 724–758):
   - Components come from `catch_labels`: periodic 6-connected components of the union catchment, one label per cell.
   - shell = catch ∧ ¬edge.
   - Per component, E_C = Σe and R_C = Σ_shell s_c(1+δ), both summed by `np.bincount` over unique cells. q_C = E_C/R_C.
   - If q_C > 1, e → e/q_C and q_C → 1.
   - comp = q_C·s_c(1+δ) on the shell.
5. **Assembly** (lines 763–795):
   - src = e − comp, which is zero-sum per component.
   - φ_k = −(1.5Ω_m/a)δ_k/k² − src_k/k².
   - The settled source therefore REDISTRIBUTES the particles' mass: it adds to the edge what it removes from the shell of the same component. It is not added on top.

This matches the CFG518/524/527 spec text exactly. Overlapping turnaround balls MERGE into one component, and that component has ONE supply.

## Frozen results

| check | z = 1 | z = 0.5 | z = 0 | rule | outcome |
|---|---|---|---|---|---|
| M1 stored \|src_sum\|/e_sum (1024³, every snapshot) | 1.5e-11 | 1.2e-11 | 6.3e-12 (max 2.7e-11) | ≤ 1e-5 | mass conserved |
| C0 instrumented copy vs unmodified `forces` (256³) | Δφ_k = 0 | 0 | 0 | ≤ 1e-5 | **PASS (bit-exact)** |
| B1 Σ_C R_C vs unique shell | 0 | 0 | 0 | ≤ 1e-5 | no per-ball supply |
| B2 Σ_C E_C vs unique e | 0 | 0 | 0 | ≤ 1e-5 | no per-ball demand |
| B3 max per-component \|Σ src\|/E_C | 3.2e-8 | 1.5e-8 | 2.1e-8 | ≤ 1e-4 | zero-sum |
| B4 delivered/R_C max; comp in edge; e in shell; e outside catch | 1+3e-9; 0; 0; 0 | same | same | | no over-delivery |
| naive per-ball shell sum / unique (what a per-ball bug would give) | 1.92 | 2.14 | 2.09 | | engine uses unique: no |
| C2 representativeness: overdraw 256³ vs 1024³ | | | 0.41 vs 0.91 (q_max 1.86 vs 6.32) | within ×1.5 | **FAIL** |

**Verdict on H1–H4 (B1–B5): NO BUG.**
- The engine counts each cell once.
- It never delivers more than a component's shell supply.
- It draws nothing inside the edge.
- It conserves mass to 1e-11 of the settled amount at 1024³.

**Overlap (V1, 256³ recomputation on the stored P1 density):**
- 50–54% of catchment volume lies in ≥ 2 turnaround balls, and 33–35% in ≥ 3. For the edge the figure is 31–44%.
- 90–95% of the settled excess sits in multiply-covered cells.
- At z = 0, 462 of 1618 occupied components hold ≥ 2 hosts, and the largest holds 242 hosts. At z = 1 the largest holds 1023 hosts and 19% of the catchment volume.
- On the stored 1024³ settled field, 92–99% of the settled mass lies in multi-host components (post-hoc).

**Mass budget (V2, z = 0, 256³ recomputation; mass in units of the mean total density per cell):**

| quantity | ratio |
|---|---|
| delivered settled mass / box mass | 0.094 |
| delivered / shell cold mass | 0.45 |
| delivered / (Ω_c/Ω_b × retained baryons in the catchments) | 0.37 |

No excess over either ceiling.

**Pooling (V3, frozen):** the own-host counterfactual gives G = 1.49 / 1.45 / 1.39 at z = 1 / 0.5 / 0. The gain sits in massive hosts (×1.5–1.7, against ×1.0–1.3 for low-mass hosts).
- By the frozen rule this is **RESOLUTION-LIMITED, not used**: C2 failed. The 256³ block-mean field caps in 41% of catchment mass, against 91% in the run.
- V4 static P(k) from the 256³ recomputation is likewise not used. Its own boost is 1.36 at k = 0.3, against 1.20 stored.

## Post-freeze diagnostics (`cfg647_posthoc.py`; NOT in the criteria, reported only)

**C1 re-read.**
- The frozen C1 expected "ONE component" from the engine's `nc`. The engine returned nc = 2 for two overlapping balls.
- Cause: `catch_labels` builds its graph on n + 1 nodes, including the background label 0, so `nc` = occupied components + 1. The OCCUPIED count is 1.
- Effects:
  - The background index carries E = R = 0, so the dynamics are unaffected.
  - Every stored `n_catch` is one too high (cosmetic).
- The frozen 1e-9 tolerance on R_C was also mis-set. The shell weight is float32, and the observed 3.0e-8 equals the float32 rounding of s_c.
- The overlap itself was counted once: naive − unique = 47 cells, which is exactly the overlapping shell cells.

**Pooling measured on the STORED 1024³ settled field** (s = dgrav − dpart, block means; own-host partition on 256³ catchments). For each host, the settled mass it received is compared with all the cold mass in its own shell. Settled mass beyond that must have been pooled from neighbours.

| | z = 1 | z = 0.5 | z = 0 |
|---|---|---|---|
| imported beyond own shell, all hosts (T_shell) | 28% | 17% | **10%** |
| same, hosts with log M_ta ≥ 13.5 | 36% | 26% | **13.5%** |
| same, lighter hosts | 21% | 5% | 0.4% |
| beyond the host's whole own catchment cold mass (T_all) | 1e-4 | 2e-4 | 2e-4 |

**Rough static P(k) effect** at z = 0, frozen particles, capping each host at its own shell (`static_import_removed`):

| k (h/Mpc) | own boost, stored | own boost, import removed |
|---|---|---|
| 0.3 | 1.198 | 1.131 |
| 0.5 | 1.253 | 1.168 |
| 1 | 1.205 | 1.158 |

This is one-sided. Hosts that export supply could gain under an own-host rule, and there is no re-evolution.

## Inherited inconsistencies (in cfg527 too; not bugs by B5; not crowding double counts)

- **Off-by-one `n_catch`.** Described above.
- **Snapshot diag calls refresh catch and f_ret, but not the edge mask** (cfg596 lines 646–653; cfg527 386–391). After the z = 1 and z = 0.5 snapshots, 11 of the 151 force calls use a catchment that is newer than their edge mask, until the next 10-call refresh. Two things limit the effect:
  - e is masked by catch;
  - the staleness is within the spec's own refresh interval.

## Reading

- **There is no engine bug that double-counts settled source in crowded regions.**
- **The THEORY's rule, applied as specified, is non-local:** one cap per connected component of overlapping turnaround balls. A dominant host draws its neighbours' shells, through chains of up to hundreds of hosts.
  - At z = 0, about 10% of the settled mass (13.5% in hosts ≥ 10^13.5) exceeds the receiving host's own shell supply. At z = 1 the figure is 28%.
  - The rule never takes more than the pooled shells hold.
- **Removing that import statically lowers the own boost from 1.20–1.25 to 1.13–1.17 at k 0.3–1.** That accounts for roughly a third of the excess, so the CFG596 EXCLUDED verdict does not hinge on pooling.
- **A per-host supply rule would be a theory change, not a fix.** It would need its own frozen criteria and a native PM run. Reproduction plan:
  - copy cfg596_pm.py;
  - replace the component labels with the own-host partition (smallest d/r_ON);
  - run 512³ L100 against S0 at a matched seed;
  - score with `cfg596_native.py` unchanged.

## Disclosures

- **What was read before freezing:** the code, astra's notes and the P1 JSON scalars (stated in the criteria).
- **The frozen C1 failed as literally written.** The cause is a test mis-specification (background node, float32 tolerance), shown in the post-hoc re-read.
- **The frozen C2 failed,** so the frozen pooling numbers are not used. The stored-field pooling numbers are post-freeze.
- **Memory over the frozen limit.**
  - `cfg647_audit.py`: peak footprint 1.27 GB, but ru_maxrss 3.09 GB. The allocator release had been disabled in that run.
  - `cfg647_posthoc.py`: footprint 1.16 GB, ru_maxrss 2.41 GB.
  - Both exceed the 2 GB RSS limit; free + inactive memory was ≥ 16 GB throughout.
- **The 256³ host partition and edge are approximations** to the 1024³ ones. 99.6–99.9% of the stored positive settled mass falls inside the 256³ catchments.
- κ = ½ fitted; cold energy mass required; no particle species; not theory closed.
