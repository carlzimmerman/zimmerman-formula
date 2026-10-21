# CFG951: mergers and clusters under the labelled-domain theory (LDT)

**Lane label: LDT MERGERS FAIL.** Every merge variant is INCONSISTENT, on both footings:
- **M1** fails (a), (c) and (d).
- **M2** fails (a) and (d).
- **M3** fails (a) and (d).

What does it is LDT's own core, not the choice of merge rule:
- Labels give restored inter-label gravity: every mass outside a label is a Newtonian source for that label's law.
- L2 tidal re-latching sets how much of each label survives.

In clusters no member ever coalesces at pericentre (fraction ≈ 2e-8), so M1 ≡ M2 ≡ M3 there.

**Settings and provenance.**
- **Criteria:** `FROZEN_CRITERIA.md`, a29366301, committed alone before any script or number.
- **Amendment A1:** `AMENDMENT_A1_post_hoc.md`, POST HOC, written after the first MAIN run. It adds a reported, ungraded variant of
  the (d) toy, and changes no class.
- **Block and label:** CFG950–959. HYPOTHESIS TEST, POST HOC (every target was read before freezing), zero new constants.
- κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 never pooled. Cold energy; no particle species. Framework-native inputs only.
- Not "theory closed". Nothing here says the data favour the framework.
- CFG950 (the formal LDT specification) had not appeared when this lane froze. The working LDT statement below is this lane's own, and
  is taken from CFG945 H1 and CFG947 N1 / M-R.

## The LDT statement used (criteria §1)
- **C1 labels.** Every collapsed object carries a label. Its medium is tethered only to its own χ_q (CFG945 H1).
- **C2 label equilibrium.** R(u_q) = |g_N + Σ_{p≠q} g_p|: all baryons and every other label's medium are Newtonian sources of label
  q's law (CFG945 [H1_two_label_equilibrium], (e); CFG941 R2). Monopole form: **M_tot = S ν(S)**, with S the mass outside label q.
  - Bracket X-OD: CFG947's own-domain phantom, with no cross-sourcing.
- **C3 L2 re-latch.** The label with the dominant medium tidal tensor |τ| = (√6/3)|u′ − u/r| takes each element (CFG945).
  Re-latching is irreversible, so a member keeps its medium inside r_dom at pericentre.
- **C4 static relaxation** (as CFG916 LR-c).
- **C5** CFG726 / CFG916 harness conventions.
- **Coalescence trigger:** r_dom ≤ r_½,b (bound fraction < ½; CFG947 M-R).

**The merge variants:**
- **M1:** instant relabel at the trigger.
- **M2:** linear blend over one t_dyn; identical to M1 for static cluster scoring.
- **M3:** labels persist until L2 disruption.

**The key consequence.** A surviving member keeps its medium inside its L2 domain:
- medians at pericentre: r_dom 238 / 234 kpc; retained medium ≈ 13–14 M* per cluster; C/M_b ≈ 1.51 / 1.64 at 1 Mpc;
- under C2 that medium is a source of the host label's law, so M_host = (M_b + C) ν((M_b + C)/…);
- the outer lensing mass therefore rises by about √(1 + C/M_b). The criteria's disclosed hand estimate was A_OUTER ≈ 0.6–0.7.

## Results (canonical / alt; ν_s)

### (a) Merger memory and (b) the cluster core
eRASS1: 318 clusters, CFG687 stack, 30-patch jackknife. ACCEPT: 8 clusters, bootstrap 1000.

| model | eRASS1 A_MID (Z) | eRASS1 A_OUTER (Z) | ACCEPT A_OUTER (Z) |
|---|---|---|---|
| plain law (single label; = the global phantom, MU-GP) | 1.907 ± 0.118 (+7.66) / 1.751 ± 0.109 (+6.91) | 1.011 ± 0.087 (+0.13) / 0.926 ± 0.079 (−0.93) | 1.019 (+0.08) / 0.941 (−0.25) |
| labels never merge, shared target (= CFG726 H-MM, MU-NM) | 1.536 (+5.56) / 1.440 (+4.87) | 0.765 ± 0.065 (−3.63) / 0.744 ± 0.063 (−4.05) | 0.448 (−4.83) / 0.430 (−5.19) |
| labels never merge, under C2 (MU-NM) | 0.632 / 0.567 | 0.281 (−29.9) / 0.259 (−33.4) | 0.269 (−10.9) / 0.247 (−12.3) |
| **LDT, M1 = M2 = M3** (L2 at pericentre, C2) | **1.213 ± 0.075 (+2.85) / 1.089 ± 0.067 (+1.32)** | **0.556 ± 0.048 (−9.32) / 0.496 ± 0.043 (−11.86)** | **0.616 ± 0.162 (−2.37) / 0.557 ± 0.147 (−3.02)** |
| bracket: present epoch | 1.138 (+1.96) / 1.020 (+0.32) | 0.502 (−11.6) / 0.447 (−14.4) | 0.574 (−2.90) / 0.519 (−3.63) |
| bracket: King r_J (CFG916) | 1.373 (+4.40) / 1.235 (+3.07) | 0.646 (−6.40) / 0.576 (−8.58) | 0.703 (−1.52) / 0.635 (−2.07) |
| bracket: ICM-sourced member halos | 0.953 (−0.80) / 0.884 (−2.09) | 0.472 (−13.2) / 0.426 (−16.0) | 0.339 (−6.96) / 0.320 (−7.67) |
| bracket: X-OD coupling (CFG947) | 1.585 (+5.95) / 1.454 (+5.04) | 0.814 (−2.66) / 0.746 (−3.99) | 0.743 (−1.32) / 0.684 (−1.75) |
| report only: supply-capped law / LDT | 1.888 / 1.729 · 1.163 / 1.034 | 0.950 / 0.863 · 0.555 / 0.520 | 1.013 / 0.932 · 0.598 / 0.544 |

**(a) INCONSISTENT for every variant, robust.** Every bracket fails OUTER on eRASS1, X-OD included. LDT reproduces CFG726's merger
memory and makes it worse: 0.56 / 0.50 against H-MM's 0.76 / 0.74. In H-MM the members' halos only replace the host law where they
exceed it; in LDT they also source it.

**(b) CONDITIONAL on reading T, which LDT implies.**
- The footings disagree: canonical Z +2.85, alt +1.32. The brackets are mixed: present epoch CONSISTENT, King and X-OD INCONSISTENT,
  ICM CONDITIONAL.
- **The MID drop is bought with the OUTER overshoot.** It is the same sourcing in the same profile. MID/OUTER is 2.18 / 2.20,
  against the law's 1.89, so the shape gets worse.
- No LDT reading fixes MID and OUTER together.

**Reading U ("LDT + an untethered-cluster selector"; not LDT).**
- CFG949 B0 (K3, exact): MID 1.011 ± 0.063, OUTER 1.047 ± 0.089.
- With labelled members truncated at King r_J in the untethered host (median 90 / 94 kpc), taking 14% / 16% of the supply:
  MID 1.114 ± 0.070 (Z +1.63) / 1.132 ± 0.071 (+1.85), OUTER 1.065 (+0.71) / 1.067 (+0.74). This is consistent on eRASS1.
- With full-halo members: MID 1.56 / 1.47, OUTER 0.77 / 0.76 (memory).
- LDT seeds a label and gates its tether on wherever the medium is settled, so it implies reading T. U needs a selector LDT does not
  have (CFG939). Even under U, every variant still fails (d).

### (c) The Bullet (CFG599 progenitors, CFG916 / CFG915 inputs)
- The sub's L2 domain at 720 kpc is 489 / 484 kpc (CFG916's King r_J: 304 / 306, reproduced exactly).
- **M3: UNDERDETERMINED (by input).**
  - The re-latched core fraction φ is ≤ φ_lin,H (0.039 / 0.041), i.e. CONSISTENT, only for pericentres d_p ≥ 151 / 150 kpc.
  - φ ≥ 0.9, i.e. INCONSISTENT, for d_p ≤ 27 / 26 kpc. The domain falls inside the 200 kpc core below d ≈ 158 kpc.
  - The record has no measured pericentre. Report only: the head-on model's minimum separation (21.5 / 9.5 kpc) gives φ 0.95 / 0.997.
- **M1: INCONSISTENT.**
  - The trigger r_dom ≤ r_½,b fires already at 720 kpc, because the record's progenitor baryons are cluster-extended
    (r_½,b = 531 kpc). The sub loses its label, so its lensing would not follow its galaxies.
  - Post hoc, no weight: with the stellar half-mass radius (466 kpc) the trigger fires below 671 / 681 kpc, i.e. at any plausible
    pericentre.
- **M2: UNDERDETERMINED** (bracket [M3, M1]).

### (d) Continuity (merger toy, m₁ = 1e11, q = 1, 1/3, 1/10)
- **FAIL for every variant**, with the frozen metric (change of the label-induced part E = M/M_GP − 1 over one remnant t_dyn).
  - J per t_dyn: 2.21 / 1.82 / 1.16 (canonical, q = 1 / 1/3 / 1/10) and 2.34 / 1.96 / 1.25 (alt), identical for M1, M2 and M3.
  - The M1 instantaneous relabel jump alone is 0.18–0.27.
  - Post hoc, fixed-configuration (relabel-only) J: 0.81–1.22.
- **Amendment A1 (post hoc, no class weight).** The frozen τ₁ has a shell-smearing artefact: r_dom spikes to its cap near
  d ≈ 100 kpc (r_dom/d up to 14.6). With τ₁ from label 1's isolated medium, r_dom(d) is smooth (r_dom = d for q = 1) and J is
  still 1.53 / 1.17 / 0.70 (canonical) and 1.63 / 1.25 / 0.75 (alt). The instant jump is 0.17–0.27, and J at R = 20 kpc is
  0.088–0.318. The artefact inflated J by about 1.4–1.7×; it did not create the failure.
- **Cause.** Two labels close together are strongly super-additive: the companion's labelled halo sources the primary's law, and L2
  strips it within about one t_dyn of coalescence. M1 and M2 cannot help, because the change happens before their trigger
  (d ≈ 16–37 kpc).

### (e) Satellites accreted onto clusters (9 Coma UDGs; CFG948)
- **LDT keeps every UDG's label.** min r_dom / r12 is 6.2 / 6.5 at the 3D distances, even with the host's total-field τ as an upper
  bound. No UDG is relabelled.
- **Inter-label sourcing raises the ceiling** by ⟨ΔE⟩ = +0.054 ln (max +0.086; with projected distances +0.26). This is an upper bound:
  it counts all host matter inside r12.
  - LDT ceiling: +0.072 ln, against observed +0.760 / +0.669.
  - z (with systematics) 1.51 / 1.32; statistics only 2.63 / 2.28 (CFG948: 1.63 / 1.43).
- **Class: NOT DIAGNOSTIC** for every variant. LDT barely changes the ceiling.
- **The global phantom** (bracket M1-inf, labels lost at infall) would give an EFE prediction of −2.13 ln, z +6.4 / +6.2: excluded
  (report only).

### Reported
- **KiDS early types.** In every variant, coalesced remnants end single-label, so H-MM's √N − 1 lift is absent. They sit at the law's
  −0.027 against +0.280 ± 0.083 (Z 3.70, CFG726's N = 1 cell).

## Classes

| variant | (a) memory | (b) core | (c) Bullet | (d) continuity | (e) UDGs | class |
|---|---|---|---|---|---|---|
| M1 | INCONSISTENT | CONDITIONAL | INCONSISTENT | INCONSISTENT | NOT DIAGNOSTIC | **INCONSISTENT** |
| M2 | INCONSISTENT | CONDITIONAL | UNDERDETERMINED | INCONSISTENT | NOT DIAGNOSTIC | **INCONSISTENT** |
| M3 | INCONSISTENT | CONDITIONAL | UNDERDETERMINED | INCONSISTENT | NOT DIAGNOSTIC | **INCONSISTENT** |

**Overall: LDT MERGERS FAIL.** The selector reading U is reported only; it is INCONSISTENT for every variant, through (d).

## What this means for LDT (for CFG950)
1. **C2 is the problem in multi-label systems.** Restored gravity between labels is what CFG945 needed for distinct collapsed objects.
   But in the deep regime a label's medium is ≫ its baryons, so a companion's or member's retained medium sources its neighbour's law
   by √(1 + C/M_b). Clusters overshoot their outer shear ×1.8–2.0. Galaxy pairs jump by O(1) per t_dyn as L2 strips the companion.
   The same term would act on any galaxy with labelled companions inside its halo; that is not tested here.
2. **The merge rule is not the lever.** L2 does nearly all the relabelling, before any coalescence trigger. To pass, LDT would need
   C2 to be weaker than full Newtonian sourcing between labels, which is the X-OD direction. X-OD still fails eRASS1 OUTER
   (−2.66 / −3.99), and dropping cross-sourcing contradicts CFG945's (e).
3. **Clusters.** Tethered LDT does not fix the core (only by overshooting OUTER). The untethered reading needs a selector LDT lacks.

## Controls
- **K: 9 / 9 pass** (`cfg951_K.out`).
  - **K1:** CFG726's H-MM failure numbers, both footings, to 0.0: eRASS1 OUTER 0.7645 ± 0.0648 (Z −3.63) / 0.7444 (−4.05), ACCEPT
    0.4485 / 0.4300. The recomputed arrays equal the stored ones to 0.0.
  - **K2:** CFG687 A_MID / A_OUTER 1.9102 ± 0.1186 / 1.0118 ± 0.0869 (canonical) and 1.7536 / 0.9265 (alt), exact. ν_s 1.9068 / 1.7510.
  - **K3:** CFG949's primary corner 1.0109 ± 0.0632 / 1.0469 ± 0.0888, s 0.6615, exact.
  - **K4:** CFG945's 18 L2 radii to 7.4e-10.
  - **K5:** CFG916 Bullet r_J 303.76 / 305.94 kpc and the eRASS1 King median 178.046 / 178.704 kpc, exact.
  - **K6:** CFG948 z_up 1.6334 / 1.4350.
  - **K-W:** the matrix convolution equals CFG916 / CFG726's to 7.3e-15.
- **MUTATE: all teeth bite, all controls hold** (`cfg951_MUTATE.out`, exit 0).
  - **MU-NM "labels never merge":** reproduces CFG726 exactly and fails OUTER, both under the shared target and under C2.
  - **MU-GP "the global phantom":** reproduces CFG947's T-X class-A EFE, all 36 values exact (−0.730…−0.102 dex). For clusters it is
    the plain law.
  - **MU-0:** C = 0 through the runner gives the law exactly.

## Disclosures
- **Run 1 kept.** The first MAIN run is `cfg951_RUN1_toyartefact.*`. Its graded numbers equal the final run's; the final run adds the
  A1 block. COMPUTE, K, MUTATE and MAIN were then rerun from the final script; the rerun COMPUTE arrays are identical to run 1's
  (56 arrays, max |diff| 0.0).
- **Implementation-stage changes** (all in A1):
  - The (d) metric was corrected to the frozen one before the full run.
  - The Bullet stellar-trigger diagnostic (post hoc).
  - Smoke runs wrote only outside the repository.
- **Non-convergence (frozen rule applied).**
  - 11 / 19 clusters (M3 primary) and 44 / 46 (present) did not reach 1e-4 within 8 iterations, with max change 6e-3 / 8e-4. The
    previous iteration's A agrees to 4 decimals.
  - The ICM bracket 2-cycles in 302 / 305 clusters. Its class is the same on both iterations.
  - No class is UNDERDETERMINED by this rule.
- **Implementation choices within the frozen text:**
  - a COMPUTE stage, which writes work arrays to `../_external_data/cfg951_work/`, not committed;
  - the ν_e kernel for the UDG estimator (CFG933 / 948's own);
  - UDG medium partially lost if r_dom < r12 (never triggered);
  - Bullet τ with G = 1 (it cancels);
  - the toy's infall speed √(G(M₁ + M₂)(<d)/d);
  - M2 blends the trigger-time content;
  - X-OD counts coalesced members' stars as host-domain baryons (none coalesce).
- **Compute.** One process at a time, one core, nice 10, RSS guard 0.9 GB. COMPUTE peak 0.66 GB in 806 s (first run 0.64 GB, 809 s); K /
  MUTATE / MAIN each under 0.25 GB in under 30 s. Run beside the live 1024³ job. Nothing downloaded; no other lane, LEDGER or THEORY_CANONICAL file edited.

## Files and re-run (from this directory, one at a time, `OMP_NUM_THREADS=1 nice -n 10`)

| file | how it is made |
|---|---|
| `cfg951.py` | the script; final sha256 670f05e172dcc375… |
| `cfg951_COMPUTE.out` | `CFG951_STAGE=COMPUTE python3 cfg951.py` (progress only) |
| `cfg951_K.out`, `cfg951_results_K.json` | `CFG951_STAGE=K python3 cfg951.py` |
| `cfg951_MUTATE.out`, `cfg951_results_MUTATE.json` | `CFG951_MUTATE=1 python3 cfg951.py` |
| `cfg951.out`, `cfg951_results.json` | `python3 cfg951.py` |
| `cfg951_RUN1_toyartefact.*` | first MAIN run, kept |

Read-only inputs:
- CFG726 work arrays and λ;
- CFG687's per-cluster npz;
- CFG686 data / results;
- the results and caches of CFG916, 915, 945, 947, 948 and 949;
- CFG654 native tables (through the R930 copy);
- the Coma UDG table.

κ = ½ FITTED; footings never pooled; cold energy mass required; no particle species; not theory closed.
