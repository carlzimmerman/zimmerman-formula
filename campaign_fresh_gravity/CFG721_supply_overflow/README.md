# CFG721: supply overflow (H-OF) and its two-population form (H-OF2). Verdict: BOTH FAIL, every source, every kernel. POST-HOC; every target was already seen

- **Criteria.** `FROZEN_CRITERIA.md` was committed alone in 93d53f734, before any script existed. `ADDENDUM_2026-10-13_HOF2.md` (H-OF2 plus a Bullet-core target, at the orchestrator's request) was committed alone in c5c6894a6, before any H-OF2 number or any H-OF target score existed. Date 2026-10-13.
- **Lane number.** CFG720 was taken (merger stopwatch). CFG721 is the next free number in the owner's reserved block 720–729.
- **Settings.**
  - κ = ½ is FITTED.
  - Footings are canonical 9.3603e-11 / alt 1.1312e-10. Kernels are ν_mono and CFG695's ν_s. Neither footings nor kernels are ever pooled.
  - "Cold energy" is used throughout, and its mass is still required. No particle species is added.
  - Not "theory closed". No ΛCDM or standard-MOND yardstick enters a verdict.
- **Scripts.** Run each from the repository root with `CFG721_MODE=<stage> OMP_NUM_THREADS=1 nice -n 10 python3 -u campaign_fresh_gravity/CFG721_supply_overflow/cfg721.py`. Each runs as one process, under 1.5 GB.
  - The stages are tk, accept, efeds, ladder, erass, hof2 and score. They took about 0.1, 0.2, 1.7, 2.3, 4.6, 0.3 and 0.05 h.
  - Each stage writes a `cfg721_<stage>.log` (gitignored, local only). Work files go to `../_external_data/cfg721_work/` and are not committed; the scripts regenerate them.
  - The score stage writes `cfg721.out` and `cfg721_results.json` (exit 0, 6/6 checks).
  - `cfg721_sparc_posthoc.py` is a POST-HOC, per-galaxy SPARC check. It is not frozen and carries no verdict weight.
- **Machinery.** CFG637 Method A (`cfg637_lib.derive`, unchanged), wrapped as CFG652's `cfg652_model.system`. The supply is 5.364 × the catchment baryons, with catchment = max(M_cond/0.10, M_b/0.90). The overflow is Method A's reservoir.
- **Data.** Read only from disk; nothing was downloaded. The harnesses were reused unchanged except for the mass model. Every number below comes from `cfg721_results.json`.

## D1: the derived threshold M_b,OF

M_b,OF is the mass at which reservoir/supply first reaches 0.01. Values are at z = 0, canonical / alt, and are the same for both kernels.

| condensed fraction f_cond | log M_b,OF (all source) | log M_b,OF (cond source) |
|---|---|---|
| 1 (all condensed; catchment M_b/0.10) | **13.03 / 13.05** | 13.03 / 13.05 |
| 0.5 | — | 13.06 / 13.53 |
| 0.25 | — | 13.54 / 13.61 |
| 0.1 | (no capacity overflow; see note) | 12.11 / 12.54 |
| 0.05 | — | 11.13 / 11.54 |

**Context.**
- At z = 0.3, the f_cond = 1 threshold drops to 12.54 (canonical).
- The analytic deep-regime capacity √(M_src a₀/G)·r_ta crosses the supply at the same place (cap/supply 1.03 at 10^13, 0.85 at 10^13.5).
- The threshold is not monotone in f_cond. The catchment rule switches from M_cond/0.10 to M_b/0.90 at f_cond = 1/9.

**Note on the all-source f_cond = 0.1 cells.** These show a "reservoir" of 0.02–0.09 at 10^9–10^11.5. It vanishes above that mass. It is not overflow:
- the settled target already exceeds the supply (1.01–1.02);
- the edge sits at 0.23–0.25 r_ta;
- R5's edge-to-r_ta shell runs dry (draw shortfall 0.33–0.52).

It is a draw residue, checked directly. The same residue gives the 0.099 at 10^10 in the alt T-K early-type cell.

**At the target masses:**
- **All source:** the overflow is empty everywhere. eRASS1 max 0.013, eFEDS 0, ACCEPT 0, galaxies 0, as in CFG637/656.
- **Cond source:** the overflow is non-zero in groups and clusters. eRASS1 median 0.088 / 0.002 with terciles 0 → 0.09 → 0.22; eFEDS 0.62 / 0.58; ACCEPT 0.34 / 0.28.

## Per-target results (canonical / alt; ν_s within 0.01 of ν_mono everywhere unless stated)

| target | measured | H-OF, all source | H-OF, cond source | rule |
|---|---|---|---|---|
| **T-K** KiDS early/late, matched Ks M_b | +0.280 ± 0.083 | −0.026 / +0.010 (Z 3.7 / 3.3) **FAIL** | −0.034 / −0.034 (Z 3.8) **FAIL** | the galaxy overflow is empty for both types (the hot-halo bracket included), so H-OF stays morphology-blind |
| **T-E** eFEDS 131 groups | stack 44–133 M☉/pc² | χ² 28.7 / 25.2 (p 4e-4 / 1.5e-3); A_out +0.43 / +0.39 dex **FAIL** | χ² 22.8 / 23.2 (p 0.004 / 0.003); A_out +0.16 / +0.17 **FAIL** | = CFG652's (b) / (a) |
| **T-R** eRASS1 318, A = obs/pred | — | MID 1.90 ± 0.12 / 1.74 ± 0.11 (Z 7.7 / 6.9); OUTER 0.96 / 0.87 **FAIL** | MID 1.32 ± 0.10 / 1.69 ± 0.14 (Z 3.3 / 5.1); OUTER 1.27 ± 0.10 / 1.41 ± 0.11 (Z 2.5 / 3.6); INNER 0.45 / 0.60 (overshoot) **FAIL** | |
| T-R2: does H-OF explain s = 0.90 ± 0.21? | 0.90 | s 0.42 / 0.44 (the law gives 0.47): **NO** | s 0.88 / 0.76: **YES by the frozen rule**. But the MID A by gas tercile is 2.66 → 2.01 → 0.81 (data/model): short ×2.7 at low mass and overshooting at high mass, so the model's mass trend is far steeper than the data's | |
| **T-A** ACCEPT 8 | — | MID 1.70 ± 0.36 (Z 1.9), OUTER 1.02 ± 0.25 / MID 1.57, OUTER 0.94: **PASS** (= the plain law, as CFG686) | MID 0.41 ± 0.11 (Z −5.5), OUTER 0.54 ± 0.14 **FAIL** (overshoot ×2) | |
| **T-X** X-COP (CFG637, ν_mono) | — | η 1.820 / 1.679 **FAIL** | η 1.494 / 1.661 **FAIL** (inner band 0.86 / 0.89 passes) | ν_s not run |
| **T-B** Bullet core M(<250)/P16 (addendum; P16 provisional) | 1 | main 0.32 / 0.35, sub 0.17 / 0.18 **FAIL** | main 0.79 / 0.78, sub 0.11 / 0.12 **FAIL** (the sub is input-limited, CFG629) | ν_s not run |
| **T-S** SPARC guard as frozen | 0.100 dex | **FAIL (not verified)**: the worst-case pairing (smallest edge 77 kpc at 10^9 vs the largest R_last 108 kpc) breaks the guard | same | see the post-hoc check |

**Reported bracket (not in the verdict).** In eRASS1, with the condensed mass placed as CFG652's BCG + members instead of co-distributed with the gas (ν_mono, canonical):
- MID 0.94 ± 0.06 and OUTER 1.07 ± 0.09, both within 2σ;
- slope 0.83.

But INNER 0.31 ± 0.05 is a ×3 overshoot. INNER is unused in CFG687 because of failed nulls in CFG686. In the same placement, ACCEPT and eFEDS overshoot. This is the only cell in the lane that fits eRASS1's MID and OUTER bands. It is post-hoc and placement-dependent.

**SPARC, post-hoc per-galaxy check (`cfg721_sparc_posthoc.out`).**
- Each of the 175 galaxies has its own M_b and R_last. Max R_last/r_edge is 0.197 (UGC 00128) and the median is 0.067. The overflow is 0 at every SPARC mass.
- So H-OF changes no SPARC point, and the RAR scatter change is exactly 0 (0.100 dex stays). The frozen guard was too coarse to certify this.
- By the frozen rule T-S stays FAIL (not verified). Physically, SPARC is unchanged.

## H-OF2 (addendum)
- The tethered phantom is capped at mean Σ̄ ≤ a₀/πG = 213.7 / 258.3 M☉/pc², i.e. ν_cap = min(ν, 1 + 1/y). This cap never binds:
  - for ν_s, (ν_s − 1)y < 1 identically (CFG695's saturation is CFG722's wall);
  - for ν_mono it binds only at y > 2.65e5.
- **Verification:** ACCEPT 8 + the T-K pairs + 20 eRASS1, all cells. The maximum |ΔΣ_HOF2/ΔΣ_HOF − 1| = **0.0** and the maximum change in overflow fraction = **0.0**.
- **H-OF2 is numerically H-OF.** H-OF already places the overflow as an untethered collisionless population (G9). H-OF2 therefore takes H-OF's scores and FAILS identically.
- The Bullet core's 4–4.8× capacity is not reached by the free population: the main core reaches 0.79 of P16 at best (cond), and the sub reaches 0.11.

## Verdict (frozen rule; both footings)

| source × kernel | H-OF | H-OF2 |
|---|---|---|
| all × ν_mono | FAILS: T-K, T-E, T-R, T-X, T-S(guard), T-B | identical |
| cond × ν_mono | FAILS: T-K, T-E, T-R, T-A, T-X, T-S(guard), T-B | identical |
| all × ν_s | FAILS: T-K, T-E, T-R; T-X and T-B not run; T-S(guard) | identical |
| cond × ν_s | FAILS: T-K, T-E, T-R, T-A; T-X and T-B not run; T-S(guard) | identical |

## Reading
1. **The all-baryon form never overflows at any target mass.** Its threshold is log M_b ≈ 13.0 only when everything is condensed (catchment ×10). For real clusters (hot-gas-dominated, catchment M_b/0.90) the phantom of all baryons eats the supply out to r_ta, as in CFG637/656. It is the plain law with a supply-edge cut, so it inherits the law's eRASS1 core excess (×1.8–1.9 at 7σ) and the law's √M outer slope (0.42).
2. **The condensed form overflows above a derived threshold and does steepen the cluster mass trend.** Its tercile slope 0.88 matches CFG687's 0.90, which is the only positive here, and M-SHUF bites (0.88 → 0.60). But the switch-on is too abrupt:
   - low-mass eRASS1 clusters stay short ×2.7;
   - massive ones, ACCEPT and eFEDS cores overshoot ×2–3;
   - the outer band falls short (A_OUTER 1.27–1.41), because the condensed phantom is small.
3. **KiDS early/late cannot be reached.** At galaxy masses both types sit far below every threshold, so H-OF is morphology-blind there, like the law.
4. **H-OF2 adds nothing numerically.** The law's own phantom never touches the a₀/πG cap. A real second population is needed only where Σ exceeds the cap (cluster cores), and Method A's free population already is that population. It does not supply enough of the Bullet core.
5. **What survives as a lead (post-hoc, no verdict weight).** The condensed source with a BCG-concentrated placement fits eRASS1's MID and OUTER bands, but it overshoots the cores of the same and of other samples. Any forward test would need a pre-registered placement and threshold.

## MUTATE and controls (6/6)
- **M0** (overflow ×0, phantom uncut ⇒ the plain law) reproduces:
  - CFG687's stored law to 1.6e-15 (band A to 0.0000);
  - CFG686's predictions to 6e-15;
  - CFG652's models to 0.0;
  - CFG652's χ² to 22.8958.
- **M-SHUF** (overflow fraction permuted across clusters, seed 721):
  - cond: s 0.88 → 0.60 (canonical) and 0.76 → 0.54 (alt). **BITES.**
  - all: NOT APPLICABLE (no threshold inside the sample).
  - Ladder: 48 of 56 onset cells are monotone; 0 stay monotone after shuffling.
- **C1:** supply = settled + reservoir to 7e-16 (ladder) and 1e-15 (eRASS1).
- **Disclosed engineering, after the freeze (no rule changed):**
  - cluster projections floor a truncated density so it projects as zero beyond r_ta;
  - the H-OF2 hook (kernel lookup KALL, stage `hof2`) was added after the addendum commit, while later stages were still queued.

κ fitted; cold energy mass required; not theory closed.
