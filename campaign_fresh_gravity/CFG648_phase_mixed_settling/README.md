# CFG648: phase-mixed settling (H-SP). Verdict: FAILS for both sources. B fails T2 canonical, T3 and T4b. H-CB fails T2, T3 headline and T4b alt. H-SP is not inert: it cuts the growth-proxy excess (context) by 35–39% for B, and it gets the sign of the KiDS age split right but only part of the size

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone in 2e9dffba1 before any CFG648 code or number. Date 2026-10-12.
- **Settings:**
  - κ = ½ is FITTED.
  - Footings: canonical 9.3603e-11 and alt 1.1312e-10 (the CFG543 group path keeps 9.36e-11 / 1.13e-10). They are never pooled.
  - "Cold energy" throughout. Its mass is required. No particle species.
  - Not "theory closed".
  - No ΛCDM or standard-MOND yardstick enters a verdict. T6 (halo model) and the EPS route are CONTEXT ONLY.
- **Scripts.** Run from the repository root with `OMP_NUM_THREADS=1 nice -n 10`. One process, about 150 MB. No PM, no download.
  - **`cfg648_lib.py`**: `InfallSP`, a subclass of CFG637's self-similar infall solver, imported read-only. With H-SP off it runs CFG637's code path unchanged. With H-SP on it adds:
    - pericentre and first-apocentre tracking per shell;
    - r_sp, taken as the outermost caustic of shells past pericentre, using its running maximum;
    - a live settling cut;
    - a draw only from phase-mixed shells;
    - Γ over the last Δln a = 0.4;
    - an ESD projector.
  - **`cfg648_derive.py`** (5.1 h). Runs D1, the brackets, C2/C3, the EPS context route (D2), and per-system runs for all gate systems:
    - 63 groups, 12 X-COP clusters, Bullet BASE/B1/B2/B3;
    - KiDS lens masses, the CFG556 masses, 175 SPARC galaxies.
    - It writes `cfg648_derive.out`, `cfg648_derive_results.json` and `cfg648_profiles.npz` (not committed; this script regenerates it).
    - `CFG648_MUTATE=1` runs M-ta and M-Γ.
  - **`cfg648_gates.py`** (20 s). Runs T1–T6 using CFG634's, CFG487's, CFG556's and CFG634-halo committed source, executed from text. There is one RSP patch per function: cut the settled phantom at the derived settled edge and add the derived reservoir. `CFG648_MUTATE=1` runs M-ta.
  - **`PM_SPEC.md`**: the native PM specification. Written, not run.
- Every number below comes from the JSONs. "can / alt" means canonical / alt.

## The derivation: r_sp/r_ta vs Γ (D1, framework solver, flat background, G9)

All rows are canonical. Alt is in the JSON and differs by ≤ 0.02 in s.

| ε (seed) | Γ = dlnM_ta/dlna | galaxy s | group s | cluster (A1795) s, B / H-CB | galaxy settled/B | cluster B settled/B |
|---|---|---|---|---|---|---|
| 0.3 | 1.36 | 0.223 | 0.248 | 0.255 / 0.278 | 0.352 | 0.369 |
| 0.5 | 0.81 | 0.304 | 0.336 | 0.322 / 0.325 | 0.531 | 0.538 |
| 0.75 | 0.54 | 0.353 | 0.435 | 0.370 / 0.421 | 0.652 | 0.658 |
| **1 (primary)** | **0.40** | **0.394** | **0.460** | **0.403 / 0.446** | **0.728** | **0.731** |
| 1.5 | 0.26 | 0.424 | 0.487 | 0.436 / 0.480 | 0.809 | 0.813 |
| 2.5 | 0.16 | 0.454 | 0.513 | 0.462 / 0.479 | 0.868 | 0.874 |

- **Prediction (a) holds in the framework's own dynamics.** r_sp/r_ta falls monotonically with Γ at every scale. Spearman ρ is −1.00 everywhere except the H-CB cluster, at −0.94. Label: TREND at every mass and footing.
- **Is there a mass trend at fixed ε?** It is weak. At ε = 1, s is 0.38–0.46 from 1e11 to 1e15 M☉/h (T6 runs).
  - Any mass dependence of Γ must come from the seed. The CFG557 EPS seed (CONTEXT) gives Γ = 0.48 for the galaxy, 0.49 for the group, 0.60 at 1e13, 0.84 at 1e14 and 1.28 at 1e15.
  - With that seed, s falls to 0.27–0.29 for 1e15 halos, so massive systems settle 0.23–0.38 of B's amount.
- **Does r_sp bind against B's supply edge at ε = 1?** It BINDS for the galaxy (0.39 vs 0.42), the group (0.46 vs 0.53) and the H-CB cluster (0.45 vs 1.36). It DOES NOT BIND for the B cluster (0.40 vs 0.35).
- **What actually limits settling is the phase-mixed supply, not r_sp itself.**
  - Under H-SP only cold energy on shells past pericentre can settle.
  - At ε = 1, 26–27% of the catchment cold energy is still on first infall, so R2's edge moves to where the phantom has used up the phase-mixed supply: x_set = 0.31 (galaxy), 0.40 (group), 0.27 (B cluster).
  - Settled mass is 0.73 of B's at every scale for the B source. The freed 27% stays as unsettled first-infall cold energy beyond r_sp.
  - So the reservoir is exactly the first-infall material, and none of it lies inside r_sp. SPARC sees zero reservoir inside R_last (T1).
- **Gate systems at ε = 1** (s / x_set / settled÷B):

| systems | source | s | x_set | settled÷B |
|---|---|---|---|---|
| groups | B | 0.40–0.47 | 0.37–0.46 | 0.37–0.73 |
| X-COP | B | 0.40–0.41 | 0.25–0.31 | 0.73 |
| X-COP | H-CB | 0.40–0.45 | 0.40–0.45 | 0.39–0.44 |
| Bullet (Γ 0.60 at z 0.296) | B | 0.36–0.37 | 0.21–0.31 | 0.67–0.69 |

## Per-test table (PRIMARY: ε = 1, derived settled edge; can / alt)

| test | candidate B source | H-CB source | CFG637 RD for reference (B / H-CB) |
|---|---|---|---|
| **T1 SPARC rms** | 0.10033 / 0.10127, Δ 0.00000: **PASS**. No r_set inside the data (min r_set/R_last 3.5); reservoir inside R_last 0 | = B (SPARC source identical) | 0.1003 / 0.1013 |
| **T2 Tian groups** | −0.070 (Z −2.97) BELOW / −0.046 (Z −1.80) CLOSES: **FAIL** | −0.076 (Z −3.28) / −0.058 (Z −2.37), BELOW both: **FAIL** | +0.060 / +0.066 CLOSES |
| **T3 X-COP headline η** | 1.784 ± 0.067 / 1.627 ± 0.061: **FAIL** | 1.342 ± 0.049 / 1.363 ± 0.052: **FAIL** | 1.820 / 1.679; 1.494 / 1.661 |
| T3 inner band 200–420 kpc | 3.163 / 2.927 FAIL | **0.812 / 0.815 PASS** | 3.163 / 2.927; 0.859 / 0.889 |
| **T4b Bullet B1 Δκ (z) main / sub** | +0.020 (−3.42) / +0.002 (−2.28) can; +0.023 (−3.39) / +0.006 (−2.23) alt: **FAIL** | +0.347 (+0.44) / +0.071 (−1.40) **PASS** can; +0.288 (−0.26) / +0.009 (−2.19) **TENSION** alt | FAIL / TENSION |
| T4 other variants (H-CB) | B: FAIL everywhere | BASE PASS / PASS; B2 PASS / TENSION; B3 PASS / TENSION | |
| T4c main M(<250)/P16 (PROVISIONAL) | 0.33 / 0.35 | 0.83 / 0.81 | 0.32 / 0.35; 0.79 / 0.78 |
| T4 merger statement | Phase-mixing time (pericentre → first apocentre, B1 main) is 2.68 Gyr, longer than the scored window t − t_peri 0.1–0.6 Gyr (CFG623). **H-SP predicts no new settling during the passage, α_eff = 0, with no constant**: the only value CFG623 allows | same | |
| **T5 KiDS isolated lenses** δ_in (K-in, ESD_HSP/ESD_B − 1) | p5 / p50 / p95: +0.058 / +0.068 / +0.025 can; +0.053 / −0.009 / +0.031 alt. **UNCHANGED (= record FAIL)**: the sign is right (more inner signal) but it is not ≥ +0.05 at every mass | = B (lens source = stars + cold gas) | record FAIL |
| T5 age split (prediction c) | A_HSP,max = log10 ESD_K9(Γ 0.16)/ESD_K9(Γ 1.36) = +0.099 / +0.095, against the observed +0.166 ± 0.071 (CFG700). **SIGN MATCHES (old > young), SIZE PARTIAL**: even the most extreme Γ contrast the solver spans gives 0.6 of the observed amplitude | same | |
| **T6 growth proxy (CONTEXT)** R(k=1) | 1.716 → **1.437** / 1.885 → **1.572**: **REDUCES** (excess cut 39% / 35%; σ8 ratio 1.040 → 1.022). Bracket with the derived reservoir shape: 1.442 / 1.560, REDUCES. Literal frozen row "r_sp only" (no phase-mixed supply edge): 1.719 / 1.887, UNCHANGED | base 0.593 / 0.676 is already a deficit; H-SP 0.574 / 0.626: **DEFICIT**; reservoir-shape bracket 1.261 / 1.270 (UNCHANGED) | |

## Verdict (frozen rule)

- **Candidate B: FAILS** T2 groups (canonical over-corrects to −0.07, Z −3.0), T3 X-COP headline and T4b Bullet.
  - It is not inert. Groups move by 0.13 dex and the context excess falls by 35–39%. T1 is untouched.
  - The cuts that thin the 0.2–0.5 r_ta settled shell also strip group-scale mass that T2 needed. Clusters stay short, because the freed supply lies on first infall beyond R200.
- **H-CB: FAILS** T2 (both footings BELOW) and T4b (alt TENSION, sub z −2.19).
  - T3: the headline still FAILS at 1.34–1.36. The inner band passes (0.81).
  - The Bullet improves on CFG637 (canonical main and sub both pass for B1, BASE, B2 and B3).
  - T6 is a deficit (context; the H-CB base already was one).
- **The EPS (context) route was run through the derivation only, not through the gates.** Whether it would add "ACCRETION-HISTORY-DEPENDENT" is therefore not established.
  - Direction: it raises cluster Γ to 0.8–1.3 and cuts cluster settled mass to 0.23–0.47 of B's. That would push X-COP and the Bullet B source further down, and cannot turn a FAIL into a PASS (frozen rule).
- **How H-SP differs from CFG598** (the finite-age front, which did not fix growth). CFG598 changes when the law's profile fills. H-SP removes where it can fill: at every age, the first-infall 27% never settles. That is why H-SP cuts the k = 1 context excess by about 37%, where CFG598 left it in place. It is also why the same cut over-corrects groups.

**Predictions (a)–(e) against the record.**
- (a) The Γ trend is derived. ✓
- (b) "Settled mass farther out in isolated lenses" is structurally impossible (S1: verified, settled H-SP ≤ B at every r in every run). The small inner ESD gain is a projection effect (less settled mass at 0.3–0.4 r_ta lowers the local Σ(R) more than the mean inside R), not an outward edge.
- (c) The age-split sign is right; the size is at most 0.6 of observed.
- (d) Mergers: α_eff = 0 is predicted knob-free. ✓
- (e) Cluster cores mixed and outskirts infalling: the H-CB inner band passes, but R200 is still short (as CFG637 H-CB).

## Checks and MUTATE

- **M-ta derive PASS.** H-SP off reproduces `cfg637_lib.derive` to exactly 0 (galaxy, group, A1795 H-CB).
- **M-ta gates PASS** (6/6), each to 0:
  - CFG637's RD branch with CFG637's own profiles reproduces CFG637's JSON: T2, T3 headline / σ / inner, T4 all variants.
  - H-SP off reproduces CFG624's T1 rms.
  - H-SP off reproduces CFG556's primary R(k).
  - Disclosed: the "construction with edge → 10 r_ta" check returns early (r_e,HSP ≥ r_e), so it only re-tests the unmodified path and is not an independent test of the H-SP construction.
- **M-Γ PASS.** With EPS seeds reversed across the T6 masses, the slope ds/dΓ_own changes from −0.110 to +0.183 (can) and +0.178 (alt). Against the Γ actually used it stays −0.211 / −0.208, so Γ drives s, not mass.
- **C1 PASS:** supply = drawn + reservoir, worst 1.4e-15. **S1 PASS:** max excess 0.
- **C2 PASS:** N 3200 changes s by 0.010 / 0.002 / 0.012.
- **C1b reported FAIL:** the transient drawn > target reaches 3.8% in the apo-bracket group and four H-CB X-COP runs. Gravitating settled mass is capped at the target, so up to 3.8% of the settled amount is briefly not gravitating; the final states are consistent.
- **C3 (reported):** no-core benchmark with Λ background, s = 0.472 at Γ = 0.41.
- **Brackets at ε = 1** (apo caustic / R5lit draw): s 0.37–0.47, settled/B 0.67–0.81 (B source). They do not change the reading; R5lit settles slightly more because it draws first-infall material.

**Post-freeze disclosures.**
1. **Scattering guard.** Shells past pericentre that sit beyond their own turnaround radius are left out of the caustic statistic.
   - In galaxies this removes 3 shells ejected to 15–21× their turnaround radius, and the caustic is unchanged.
   - In groups, many inner shells drift to 1.02–1.5× their turnaround radius as the self-similar core expands (a CFG637 inherited convention). The guard then lowers s by at most about 4%: NGC4151 0.457 guarded, vs about 0.475 if mild drifters are kept; the 99th percentile is 0.464.
   - Per-run counts reach 1433 of 1600 (a maximum over time; median 133).
2. **R2 under H-SP.** The supply available for settling is taken as the phase-mixed cold energy, so the edge is truncated inside-out. CFG637's uniform fset scaling would scale the phantom by about 0.73 at every radius and break the law.
   - As a result the gates cut at the derived settled edge r_set = min(r_sp, phase-mixed supply edge), not at r_sp alone. Cutting at r_sp alone would double-count the freed supply.
   - The literal frozen T6 row "s(M) = r_sp only" is reported and reads UNCHANGED for B. That alone shows the effect comes from the phase-mixed supply, not from the caustic position.

## Comparison with CFG644 (neighbour-bounded edge, reported)

CFG644 found that H-NB barely bites:
- KiDS isolated lenses 0%;
- SPARC 0 real bites;
- groups +0.008 dex;
- shear excess removed 0.00%.

H-SP bites everywhere a catchment is still accreting: groups −0.13 dex, the T6 context excess −35–39%. Both lanes can only move settled edges inward (S1). The difference is that H-SP's limit comes from the system's own orbital state (the first-infall share of its supply), which is large (≈ 27% at Γ 0.4) for every isolated system. Neither repairs clusters.

Inherited and labelled:
- CFG637's solver conventions: seed slope ε, angular-momentum bracket q 0.1, self-similar core growth, sphericity;
- CFG634's per-scale supply conventions;
- CFG556's halo ingredients (T6);
- CFG557's EPS history (context).
