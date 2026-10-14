# CFG726: merger memory (H-MM). Verdict: H-MM FAILS (clusters overshoot the outer band; groups unchanged); VOID-as-frozen on 3 controls that do not touch the failing scores. POST-HOC; every target was already seen

- **Criteria.** `FROZEN_CRITERIA.md`, committed alone in 78e51c189 before any script or number. Date 2026-10-13. Lane in the owner chat's block CFG720–729 (CFG726 was free).
- **Settings.** κ = ½ FITTED. Footings canonical 9.3603e-11 / alt 1.1312e-10, never pooled. Kernels ν_s (CFG695, primary) and ν_mono (bracket), never pooled. "Cold energy" throughout; its mass is still required; no particle species. Not "theory closed". No ΛCDM or standard-MOND yardstick in any verdict.
- **Scripts.** `CFG726_MODE=<tk|erass|accept|efeds|score> OMP_NUM_THREADS=1 nice -n 10 python3 -u campaign_fresh_gravity/CFG726_merger_memory/cfg726.py` from the repository root. One process, peak RSS 0.34 GB; no Method A infall run, no PM run; vm_stat checked before each stage (free+inactive 19–28 GB). Stage times 6 s / 14 min / 30 s / 2 min / 1 min. Work files in `../_external_data/cfg726_work/` (not committed). `score` writes `cfg726.out`, `cfg726_results.json`. `cfg726_control_diag.py` (POST-HOC, no verdict weight) locates the failed controls.
- **Data.** Disk only, nothing downloaded. Harnesses reused unchanged except for the H-MM mass term: CFG721 T-K convention, CFG687 per-cluster shear and jackknife, CFG686/ACCEPT gas construction, CFG652 staged eFEDS stack and score code, CFG688's redMaPPer match.

## The derivation

Each bound progenitor carries its tethered cold energy T_i = its own law phantom, cut at its own supply edge (5.364 × m_i/0.10) and its own r_ta. Smooth accretion brings baryons but no halo. Cold energy is conserved and collisionless, so after assembly

**M_HMM(<r) = M_b(<r) + max[ Σ_i T_i(<r), T_rem(<r) ]**

with T_rem the plain law of all remnant baryons. The excess over the law is E = max(0, ΣT_i − T_rem).

- **Deep regime, concentric, all progenitor edges beyond r:** E(<r) = (Σ_i √f_i − 1) × T_rem(<r), with f_i = m_i/M. Smooth accretion enters only through M, so it lowers the excess.
  - N equal pieces: (√N − 1) T_rem.
  - Mass ratio q: (1 + √q)/√(1 + q) − 1.
- **Finite edges:** piece i contributes min(√(G m_i a₀) r/G, S_i).
  - The free memory mass is F = S_tot(1 − 1/√N), which peaks at the progenitor edge (F/T = √N − 1 there).
  - Pieces whose edge lies inside r contribute their whole supply.
- **Numerical check:** at N = 2 the code gives C/T = 1.43–1.45 at 50–100 kpc (√2 = 1.414) and F/T_peak = 0.418 (√2 − 1 = 0.414). The progenitor edges are 174–886 kpc for log M_b 10–11.5.

## Results (frozen rules; canonical / alt; ν_s, with ν_mono within 0.01 everywhere)

| target | measured | H-MM primary | rule |
|---|---|---|---|
| **T-K** KiDS early/late at matched Ks M_b, N_early = 2, N_late = 1 | +0.280 ± 0.083 | +0.115 / +0.116 (Z 1.98 / 1.97) | **PASS**, by 0.003 of the 2σ line (expected; hand estimate disclosed in the criteria) |
| T-K bracket, N = 1 / 2 / 3 / 4 / 5 and q = 1/3 | | −0.027 / +0.115 / +0.200 / +0.262 / +0.310 / +0.102 | N ≥ 3 sits inside 1σ; q = 1/3 fails (Z 2.15) |
| T-K P2 placement (free mass re-placed by Method B; reported) | | N2 +0.031 (Z 3.0), N3 +0.075 | the lift depends on the placement: the free mass spreads out when phase-mixed by energy |
| **T-R** eRASS1 318 | law: MID 1.91 ± 0.12, OUTER 1.01 ± 0.09 | MID 1.54 ± 0.10 / 1.44 ± 0.09 (Z 5.6 / 4.9); OUTER 0.76 ± 0.06 / 0.74 ± 0.06 (Z −3.6 / −4.1) | **FAIL**: the MID excess is only partly filled, and OUTER now overshoots |
| T-R2 outer slope | s = 0.90 ± 0.21 (law 0.47) | s 0.72 / 0.68 | "explains" by the frozen rule. But OUTER A by tercile is 0.57 → 0.82 → 0.81: the low-mass tercile is overshot ×1.75 |
| T-R brackets | | N×0.5: MID 1.82, OUTER 0.82 · N×2: 1.29 / 0.74 · stripped: 1.01 / 0.72 · BCG-half: 1.37 / 0.90 (canonical) | every bracket FAILS. "Stripped" fills MID exactly but overshoots OUTER at 4.6σ |
| **T-A** ACCEPT 8, N_mem 45–93 | law: MID 1.70, OUTER 1.02 | MID 1.03 ± 0.24 / 0.96 ± 0.22; OUTER 0.45 ± 0.11 / 0.43 ± 0.11 (Z −4.8 / −5.2) | **FAIL**: massive clusters overshoot ×2.2 outside 1.2 Mpc (all brackets fail) |
| **T-E** eFEDS 131 | stack 44–133 M☉/pc² | χ² 28.4 / 24.9 (p 4e-4 / 1.6e-3); A_out +0.42 / +0.38 dex | **FAIL**, same as the law (law χ² 28.7 / 25.1). The members' memory raises the stack by ≤ 7.7% (f_cond ≈ 0.03: the members hold little cold energy) |
| T-X X-COP, T-B Bullet | | NOT RUN (machine limit; no X-COP member inventory) | blocks a PASS |
| **T-S** SPARC | RAR rms 0.100 dex | unchanged (identity: discs N = 1) | PASS by construction |
| **T-S2** (declared vulnerability) | | accreted 1% / 3% / 10% in 1% pieces: disc V rises ×1.04 / ×1.12 / ×1.37 at 10–30 kpc (log M_b 10 and 11) | if minor accretion counts, SPARC and the KiDS late types change. The N = 1 rule for discs is declared, not derived |

**Verdict (frozen; both footings; both kernels).** H-MM FAILS on T-R, T-A and T-E. T-K passes at the primary N = 2, on the 2σ line, and only with the memory placement. T-X and T-B were not run.

## MUTATE and controls (10/13 pass; frozen text: "each must hold or the lane is void")

- **Passing controls:**
  - **M-N1** (N = 1 everywhere reproduces the plain law): T-K 8.8e-17, eRASS1 4.2e-15, ACCEPT 5.4e-15, eFEDS 0.0.
  - **M-ADD** in T-K (2.2e-16) and ACCEPT (0.0).
  - **M0 eRASS1:** CFG687's stored law to 1.6e-15, band A 0.0000.
  - **M0 ACCEPT:** CFG686's predictions to 6e-15.
  - The eFEDS score code reproduces CFG652's χ² 22.8958.
  - C-CONS holds on every target.
- **FAIL M-ADD eRASS1.** The additive excess is non-zero (≤ 1.2e5 M☉) only at the first grid node, 1.0 kpc. There the harness's cored gas profile has M_b = 0, while the members' smoothed Hernquist galaxies do not. No ΔΣ bin moves (max relative change 0.0). `cfg726_control_diag.out`.
- **FAIL M-ADD eFEDS.** The cause is a frozen-spec inconsistency: the progenitor rule puts M_bcg in the BCG, while CFG652's baryon profile puts 0.5 M_cond there. All 12 affected groups have M_bcg/M_cond > 0.5. Resetting those groups to the law moves the stack by ≤ 0.7% in two inner bins, so no T-E label moves.
- **FAIL M0 eFEDS (≤ 2% per group).**
  - The analytic cut law differs from CFG652's Method A model (b) by more than 2% in 16 of 131 groups.
  - Group 106 (M_hot 2.5e11) differs by 75% in its inner bins. There, Method A's (b) carries a core reservoir that the analytic cut cannot carry.
  - The next worst group differs by 3.8%.
  - Stack-level agreement is ≤ 0.65% per bin, and the law's χ² (28.7 / 25.1) matches CFG721's (28.7 / 25.2).
- **Scope of the voids.** The verdict stands on clean controls. ACCEPT passes every control and fails at 4.8–5.2σ. eRASS1's only failed control touches no bin, and eRASS1 fails at 3.6–5.6σ. eFEDS fails at the law's own level whatever its baseline.

## Reading

1. **Sub-additivity gives early types roughly the right lift.** The lift is √N − 1 of the law's cold energy inside the progenitors' supply edges (≈ 175–900 kpc). One equal-mass merger reaches the KiDS excess at the 2σ edge, and N ≥ 3 sits well inside it. This rests on keeping the superposed halos where they were. If the free mass is phase-mixed by energy (P2), the lift drops to about 40% (N = 2: +0.058 instead of +0.142 dex). The forward test would be early types split by a measured merger indicator at fixed M_b.
2. **Clusters: the members' memory holds the cluster's whole supply (53.6 M* ≈ 10.7 M_gas), and that is too much at 1–3 Mpc.**
   - It steepens the outer slope (0.47 → 0.72, which "explains" 0.90 by the frozen rule).
   - It overshoots the outer amplitude (eRASS1 OUTER 0.76; ACCEPT 0.45). The overshoot is worst for low-mass eRASS1 clusters and for the massive ACCEPT clusters.
   - The MID excess is still unfilled (1.54).
   - No placement bracket fixes MID and OUTER together. "Stripped" fixes MID but not OUTER.
3. **Groups: no effect.** eFEDS groups are hot-gas dominated (f_cond ≈ 0.03), so the members' memory is a ≤ 8% perturbation, and they fail as the law does.
4. **The N rule is the weak point.** Under H-MM's own logic, small accreted pieces leave memory (T-S2: 3% accreted gives ×1.12 in disc velocity). "Discs N = 1" and "late types N = 1" are therefore declared, not derived. If minor accretion counts, SPARC changes.

κ fitted; cold energy mass required; not theory closed.
