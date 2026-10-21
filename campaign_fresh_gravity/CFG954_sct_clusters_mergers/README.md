# CFG954: clusters and mergers under the source-changing non-local theory (SCT)

**Lane label: SCT CLUSTERS FAIL.** All three rules are INCONSISTENT on both footings:
- **R1 (absorption)** removes merger memory, but the core deficit stays and it destroys satellites' own laws.
- **R2 (persistence)** and **R3 (hybrid)** keep satellites, but memory, the core deficit and merger continuity fail.

Own-baryon sourcing does remove the failure that killed LDT (CFG951's inter-label amplification). Persistence gives eRASS1 A_OUTER
0.87 / 0.79, against LDT's 0.56 / 0.50 and H-MM's 0.76 / 0.74. It still does not pass on the alt footing.

**Settings and provenance.**
- **Criteria:** `FROZEN_CRITERIA.md` **68a43b4ff**, committed alone before any script or number.
- **A1** `AMENDMENT_A1_implementation.md` **1c9c15630** (implementation stage, after 4-cluster smoke runs written outside the
  repository, before any full-data run; committed alone). The R1 toy momentum check uses the exact supply root. A convergence
  figure for r ≥ 10 kpc is reported only.
- **A2** `AMENDMENT_A2_post_hoc_cfg953.md` (POST HOC). CFG953's frozen SCT specification read against this lane; no class of R1–R3
  changes.
- **Block and label:** CFG950–959. HYPOTHESIS TEST, POST HOC (every target was read before freezing), zero new constants.
- κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 never pooled. Cold energy; no particle species. Framework-native inputs only.
- Not "theory closed". Nothing here says the data favour the framework.

## The SCT statement used (criteria §1–2)
- **Chassis (CFG947).** G = 8πG(T_b + T_c + 𝒮). The dust is untethered. 𝒮 = Σ_q 𝒮_q, each conserved, retarded and sourced by its
  domain's own baryons only; nothing cross-sources.
- **Zero-sum per domain** forces an edge at the supply root (A(<r) = min(T_law, S)). Weights are constant and carried by matter
  between events.
- **Domains** are bounded by the gravitational King r_J at pericentre. SCT has no medium tidal tensor, so L2 is not used.
- **Supplies (CFG652 P2 branch).** The members' supplies add up to the cluster's (Σ_i S_i = S_tot, exact in 652/652 cases).
- **Rules:**
  - R1: absorb a member when r_J < its own supply edge; the host is recomputed from its total own-domain baryons.
  - R2: members keep 𝒮_q inside r_J; the host is the law of the gas.
  - R3: absorb beyond r_J, persist inside it.
- **Cold-dust placement:** P-S primary (the halo is 𝒮-carried); P-I bracket (bound dust halos survive absorption as Newtonian
  dust).

## Results (canonical / alt; ν_s; eRASS1 318 with CFG687's jackknife, ACCEPT 8 with bootstrap)

### (a) Memory (OUTER), core (MID), (b) ACCEPT and (c) slope

| profile | eRASS1 A_MID (Z) | eRASS1 A_OUTER (Z) | s (obs 0.896 ± 0.209) | ACCEPT A_OUTER (Z), reported |
|---|---|---|---|---|
| plain law (= CFG687, K3) | 1.907 (+7.66) / 1.751 (+6.91) | 1.011 ± 0.087 (+0.13) / 0.926 ± 0.079 (−0.93) | 0.466 / 0.464 | 1.019 (+0.08) / 0.941 (−0.25) |
| **R1 [P-S]** (f_abs = 1.000) | **1.889 (+7.60) / 1.729 (+6.82)** | **0.950 ± 0.083 (−0.60) / 0.863 ± 0.075 (−1.83)** | 0.420 / 0.442 | 0.974 (−0.10) / 0.897 (−0.43) |
| R1 [P-I] (dust-held halos) | 1.630 (+6.26) / 1.488 (+5.30) | 0.816 ± 0.071 (−2.60) / 0.748 ± 0.065 (−3.90) | 0.502 / 0.533 | 0.799 (−0.92) / 0.731 (−1.35) |
| **R2** | **1.723 (+6.80) / 1.575 (+5.91)** | **0.868 ± 0.075 (−1.75) / 0.793 ± 0.069 (−3.02)** | 0.487 / 0.518 | 0.832 (−0.74) / 0.763 (−1.13) |
| **R3** | **1.710 (+6.73) / 1.563 (+5.83)** | **0.863 ± 0.075 (−1.84) / 0.788 ± 0.068 (−3.11)** | 0.488 / 0.519 | 0.828 (−0.75) / 0.760 (−1.15) |
| bracket present-epoch r_J: R1 / R2 / R3 | — | 0.964 / 0.836 / 0.833 (can); 0.877 / 0.773 / 0.771 (alt) | — | — |
| bracket uncut host law: R1 / R2 / R3 | — | 1.011 / 0.909 / 0.904 (can); 0.926 / 0.832 / 0.827 (alt) | — | — |
| never absorb, MU-NA (ii) (= CFG953's spec, A2) | 1.559 (+5.68) / 1.470 (+5.06) | 0.771 (−3.48) / 0.762 (−3.68) | 0.809 / 0.816 | 0.447 (−4.88) / 0.428 (−5.26) |
| for reference: CFG726 H-MM (K2) / CFG951 LDT M3 (K1) | — | 0.765 / 0.744 · 0.556 / 0.496 | — | 0.449 / 0.430 · 0.616 / 0.557 |
| reading N: native dust + clip, with members | 1.110 ± 0.070 (+1.58) / 1.103 ± 0.069 (+1.49) | 0.782 ± 0.069 (−3.18) / 0.755 ± 0.066 (−3.71) | 0.629 / 0.656 | (no B0 ACCEPT grade) |

**Diagnostics** (medians over eRASS1):
- R1 absorbs every member node (median pericentre r_J 178 kpc, against member edges ≈ 1 Mpc).
- R2 and R3 keep C_J ≈ 9.3 / 10.2 M* (canonical / alt; C/M_b at 1 Mpc ≈ 1.06 / 1.17). The host keeps 81–83% of the supply; its
  forced edge sits at ≈ 2.4–2.9 Mpc.

**What the numbers say.**
- **(a1) memory: CONDITIONAL for every row.**
  - R1 [P-S] is the capped law (no memory), but its P-I bracket shows memory.
  - R2 / R3 pass canonical and fail alt (Z ≈ −3.0 / −3.1). The present-epoch bracket fails both footings.
  - SCT's forced edge removes the projected mass beyond the edge from Σ(R), which raises the model's outer ΔΣ. That lowers A_OUTER
    by 0.04–0.06 (uncut vs capped), so the edge works against the memory budget, not for it.
- **(a2) core: INCONSISTENT for every row, Z_MID +5.3 to +7.6.** No rule moves cold mass into the core; the memberships only add
  co-distributed mass, so MID and OUTER drop together.
- **(c) slope.** R1 is CONDITIONAL (s 0.42 / 0.44, 2.2 s_err low). R2 and R3 are CONSISTENT, because memory steepens s. The
  binning dependence (CFG688, NOT SETTLED) applies.

### (d) The Bullet (CFG599 progenitors; pericentre not in the record)
- The sub's King r_J at 720 kpc is 304 / 306 kpc (K5), against its edge rt = 991 kpc. r_J < rt at every d_p ∈ (0, 720] kpc.
- **R1 [P-S]: INCONSISTENT for every d_p.** The sub is absorbed whatever the pericentre, and its 𝒮 is recomputed onto the main.
  - Reported, no weight: a non-spherical recompute that keeps the galaxies' own share would give φ = 0.62.
- **R1 [P-I], R2, R3: UNDERDETERMINED (by input).** φ_J ≤ φ_lin,H (0.039 / 0.041) for d_p ≥ 324 / 319 kpc; φ_J ≥ 0.9 for
  d_p ≤ 19 kpc.

### (e) Continuity (merger toy, m₁ = 1e11, q = 1, 1/3, 1/10): INCONSISTENT for every row

| row | J (max \|ΔE\| per dynamical time), can / alt | what drives it |
|---|---|---|
| R1 [P-S] | 0.65 / 0.68 (q 1), 0.78 / 0.80, 0.87 / 0.88 | absorption fires at d = 970 / 811 / 552 kpc (can), when r_J falls below the secondary's 674 / 391 / 217 kpc edge, and the secondary's interior loses its phantom at once (E₂ jump). About centre 1, E₁ ≡ 0 |
| R1 [P-I] | 0.29 / 0.29, 0.16 / 0.17, 0.076 / 0.077 | dust-held memory about centre 1 |
| R2 | 0.39 / 0.39, 0.18 / 0.18, 0.080 / 0.080 | persistence never merges. The stripped secondary's stars source nothing, so the remnant ends below the law: E₁(200 kpc) = −0.26 / −0.12 / −0.04 |
| R3 | 0.22 / 0.22, 0.097 / 0.097, 0.047 / 0.047 | sub-additive transient while the secondary sits inside R (q = 1/10 passes; q ≥ 1/3 fails) |

- Reported, no weight: a global recompute would give the absorbed secondary an EFE of −0.9% to −15% at 5–20 kpc instead of erasing
  its phantom.

### (f) Momentum of the absorption step (T-M identity)
- **R1: CONDITIONAL.**
  - The primary monopole recompute at the trigger conserves momentum exactly. The whole domain is comoving with zero net charge, and
    the recompute is spherical. On the exact-root member the residual is 2e-16 / 9e-17; the inherited harness-grid residual of
    0.9% / 1.1% is reported only (A1).
  - The declared bracket is a global recompute that keeps satellites' phantoms. It leaves an uncompensated charge riding with the
    member, ΔP_s/P = 2.7 / 3.1 (cluster median) and 29 (toy).
- **R2: CONSISTENT.** No event, constant carried weights.
- **R3: INCONSISTENT under P-S.**
  - The stripped shells are moved into the static host while the bound part keeps net charge Q_in = h(<r_J). That gives
    ΔP_s/P = 10.1 / 11.1 (cluster median) and 58 (toy).
  - It is zero only if the bound halo is dust (P-I).
- **Mass:** the supply bookkeeping holds in every cluster (S_host/S_tot ≥ 0.08, never negative).

### (g) Coma UDGs (9 admitted; CFG948 inputs)
- **R1 absorbs them.** r_J < r_e for 7/9 (canonical) and 4/9 (alt) at the 3D distances, and 9/9 at the projected distances.
  r_J/r_e ≈ 0.7–1.3, so this is marginal at the 3D distances.
- With the absorbed UDGs' own phantom recomputed away, R1 [P-S] predicts ⟨E⟩ = −1.85 / −1.09 ln against the observed
  +0.76 / +0.67: **z +5.75 / +3.87, INCONSISTENT.**
- **Rules that keep the own phantom inside r_J** (r_J/r12 ≥ 4.45): ⟨E⟩ = +0.026 ln, z +1.61 / +1.42 (statistics only 2.80 / 2.46).
  NOT DIAGNOSTIC. They neither explain the above-law excess nor are excluded by it.
- **So absorption does remove their phantom, and that is excluded.** The global-source variant is excluded too (MU-GS:
  −2.13 ln, z +6.4 / +6.2).

### The CFG949 combination: is "SCT for galaxies, untethered for clusters" what R1 gives?
**No.**
- **R1 gives the law, not CFG949's reading.** The absorbed 𝒮 has zero net mass (zero-sum), so it cannot "become dust". R1
  recomputes it into the host's law of total baryons, which is the capped law: core Z +7.6 / +6.8.
- **The only route inside the SCT chassis is the clip** (ρ_s = max(ρ_ph − ρ_c, 0)). Wherever untethered native dust is denser than
  the phantom, gravity is Newtonian.
- **Reading N** (CFG949's B0 native debris plus the clip, members' dust conserved) **fixes the core but overshoots the outskirts.**
  A_MID is 1.110 / 1.103 (Z +1.6 / +1.5), but A_OUTER is 0.78 / 0.76 (Z −3.2 / −3.7). The clip adds the phantom wherever it
  exceeds the dust, on top of B0's own dust.
- **No selector is derived; the split is a CHOICE.**
  - Under the same native rule, native dust exceeds the phantom at 20–50 kpc in M_b ≥ 1e10 galaxies: up to 1.30× / 1.18× at
    NGC 3198 mass (dwarfs at 1e9 stay below, ≤ 0.76).
  - In the median-Mgas cluster, dust exceeds the phantom over only 41% / 31% of the MID band.
  - So neither side of the frozen selector criterion holds.

## Classes

| row | (a1) memory | (a2) core | (c) slope | (d) Bullet | (e) continuity | (f) momentum | (g) UDGs | class |
|---|---|---|---|---|---|---|---|---|
| R1 [P-S] | CONDITIONAL | INCONSISTENT | CONDITIONAL | INCONSISTENT | INCONSISTENT | CONDITIONAL | INCONSISTENT | **INCONSISTENT** |
| R1 [P-I] | CONDITIONAL | INCONSISTENT | CONDITIONAL | UNDERDETERMINED | INCONSISTENT | CONDITIONAL | NOT DIAGNOSTIC | **INCONSISTENT** |
| R2 | CONDITIONAL | INCONSISTENT | CONSISTENT | UNDERDETERMINED | INCONSISTENT | CONSISTENT | NOT DIAGNOSTIC | **INCONSISTENT** |
| R3 [P-S] | CONDITIONAL | INCONSISTENT | CONSISTENT | UNDERDETERMINED | INCONSISTENT | INCONSISTENT | NOT DIAGNOSTIC | **INCONSISTENT** |
| R3 [P-I] | CONDITIONAL | INCONSISTENT | CONSISTENT | UNDERDETERMINED | INCONSISTENT | CONSISTENT | NOT DIAGNOSTIC | **INCONSISTENT** |

- **Per rule:** R1 INCONSISTENT, R2 INCONSISTENT, R3 INCONSISTENT.
- **Overall: SCT CLUSTERS FAIL.**
- Reported, no weight in the overall: reading N gives (a1) INCONSISTENT, (a2) CONSISTENT, (c) CONSISTENT, with the selector a CHOICE.
  CFG953's own specification (A2) gives (a1) INCONSISTENT and (a2) INCONSISTENT.

## What this means
1. **Own-baryon sourcing fixes CFG951's specific failure, not merger memory itself.** Members' bound phantoms still add
   co-distributed mass, and the alt footing still fails OUTER. CFG953's whole-body rule sits at H-MM's level (0.77 / 0.76).
2. **Absorption trades memory for satellites.** Any criterion loose enough to absorb cluster members (domains truncated below their
   edges) also absorbs the Coma UDGs and the Bullet sub, and erases a merging galaxy's interior law 0.5–1 Mpc before coalescence.
   Gravitational r_J is small next to SCT's supply edges (≈ 54 r_M), so truncation below the edge is the rule, not the exception.
3. **The core deficit is untouched by every bookkeeping of the law.** It closes only with untethered dust denser than the phantom,
   which needs a cluster/galaxy selector SCT does not derive, and in clip form that reading overshoots the outskirts.
4. **Merger continuity is generic.** Two own-domain laws against one law of the combined baryons differ by O(√2 − 1) in the deep
   regime. Every rule here changes that faster than 5% per dynamical time.

## Controls
- **K: 8/8 pass** (`cfg954_K.out`; every reproduced value exact to 0.0, except the alt law at 1.9e-16).
  - **K1** CFG951's persistence failure: M3 eRASS1 OUTER 0.5562 ± 0.0476 (Z −9.32) / 0.4960 (Z −11.86), ACCEPT 0.6164 / 0.5565,
    X-OD 0.8144 / 0.7455. M3 recomputed with CFG951's `run_ldt` on 6 eRASS1 and 8 ACCEPT clusters equals the stored arrays (0.0).
  - **K2** CFG726 H-MM: 0.7645 (Z −3.63) / 0.7444 (Z −4.05), ACCEPT 0.4485 / 0.4300; recomputed = stored.
  - **K3** CFG687: A_MID 1.9102 ± 0.1186, A_OUTER 1.0118 ± 0.0869, s 0.466; alt law; ν_s law arrays = CFG726's.
  - **K4** CFG949 primary corner: 1.0109 ± 0.0632 / 1.0469 ± 0.0888, s 0.6615.
  - **K5** CFG916 King r_J: Bullet 303.76 / 305.94 kpc; eRASS1 pericentre median 178.046 / 178.704 kpc.
  - **K6** CFG948 z_up 1.6334 / 1.4350; β-model g_host(1 Mpc) 8.8065e-11.
  - **K-W** convolution 3.8e-15 / 7.3e-15.
  - **K-S** Σ_i S_i = S_tot to 4.4e-16, P2 branch in 652/652.
- **MUTATE: all teeth bite and the control holds** (`cfg954_MUTATE.out`).
  - **MU-NA, "never absorb":** the H-MM form reproduces CFG726 exactly and fails OUTER. SCT's own never-absorb form also fails:
    0.771 (Z −3.48) / 0.762 (Z −3.68).
  - **MU-GS, "a global source":** CFG947's 36 T-X EFE values exact (−0.730 … −0.102 dex). The UDGs under a global source reproduce
    CFG951's M1-inf: −2.131 / −2.137 ln, z +6.36 / +6.18.
  - **MU-0:** C = 0 with no cap through the SCT runner gives the plain law to 6.1e-15.

## Disclosures
- **Non-convergence (frozen rule applied).**
  - R1 [P-S] did not reach 1e-4 in 8 iterations for 173 / 215 clusters, and R1 [P-I] for 161 / 204; R2 for 3 / 8, R3 for 3 / 5.
  - The cause is a 2-cycle at the innermost radii, where the cored harness gas has M_b ≈ 0 and a member node at the centre has no
    tidal radius (A1). The largest change for r ≥ 10 kpc is 4.4e-2.
  - The largest change of any band amplitude between the last two iterations is 3.8e-5 (`T_R_prev_iteration`), so no class is
    UNDERDETERMINED.
- **Smoke runs and A1.** Smoke runs (`CFG954_NMAX=4`) wrote only to `../_external_data/cfg954_work/`. Their sample-independent
  numbers (Bullet, toy, UDGs, selector) were seen before the full run and are disclosed in A1.
- **Implementation choices within the frozen text:**
  - the absorbed and stripped stars are placed with the members (gas-co-distributed, node-averaged weights);
  - a member node with no finite tidal radius persists whole under R1;
  - the UDG edge's r_ta cap uses z = 0.0231 (it never binds);
  - reading N takes baryons and cold from CFG949's B0 arrays, and members from this lane's eRASS1 gas;
  - the Bullet sub's edge is its rt (the record's progenitor truncation);
  - in the toy, label 2's stripped active mass joins label 1's supply (its cap never binds at R ≤ 200 kpc).
- **CFG953.** Its specification froze while this lane ran and differs on two points (whole bodies kept; labelled dust inert). The
  consequences are in A2: CFG953's clusters are this lane's MU-NA (ii) row, at H-MM-level memory. No R1–R3 class changes.
- **Compute.** One process at a time, one core, nice 10, RSS guard 0.9 GB. COMPUTE took 725 s at a peak of 0.66 GB; K / MUTATE /
  MAIN each ran under 0.6 GB in under 10 s. No 1024³ job was seen running at the start. Nothing was downloaded. No other lane, LEDGER,
  THEORY_CANONICAL file, sol61_push/ or campaign_fresh_gravity_astra/ was edited; CFG953 was read only.

## Files and re-run (from this directory, one at a time, `OMP_NUM_THREADS=1 nice -n 10`)

| file | how it is made |
|---|---|
| `cfg954.py` | the script |
| `cfg954_COMPUTE.out` | `CFG954_STAGE=COMPUTE python3 cfg954.py` (progress only; work arrays in `../_external_data/cfg954_work/` from the repository root, not committed) |
| `cfg954_K.out`, `cfg954_results_K.json` | `CFG954_STAGE=K python3 cfg954.py` |
| `cfg954_MUTATE.out`, `cfg954_results_MUTATE.json` | `CFG954_MUTATE=1 python3 cfg954.py` |
| `cfg954.out`, `cfg954_results.json` | `python3 cfg954.py` |

Read-only inputs:
- CFG726 and CFG951 work arrays and λ;
- CFG687's per-cluster npz;
- CFG686 data / results;
- the results and caches of CFG726, 687, 916, 915, 947, 948, 949 and 951;
- CFG654 native tables (through CFG951's copy of CFG949's R930);
- the Coma UDG table.

κ = ½ FITTED; footings never pooled; cold energy mass required; no particle species; not theory closed.
