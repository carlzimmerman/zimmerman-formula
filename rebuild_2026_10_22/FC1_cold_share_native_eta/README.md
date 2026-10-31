# FC1_cold_share_native_eta: converting the zooms' total-matter surface density to the cold share takes route E from FAIL to the edge, with no knob. Frozen label F★-DEPENDENT (canonical), cluster masses ng 48

Criteria: `FROZEN_CRITERIA.md` (061b2e2a1a), committed alone before any script or number. Scripts `fc1_grade.py`, `fc1_x74.py`, `fc1_down.py`. Outputs `fc1.out`, `fc1_results.json`, `fc1_ls1.out`, `x79_rule/`.

## The bookkeeping point
X48's zooms evolve **all of Ω_m** as collisionless dust (`x48_zoom.py`: `rhom = Om * 2.775e11 * h ** 2`; "each lattice point carries one cell of mean density"). X43's Σ_coll uses the same total density. So η Σ_coll(M) is the surface density of total matter in a halo of total mass M.

The grader used that number for the **cold** halo alone and added the baryons on top: `q["GB"] + Mh` on SPARC, `pp["Mb"] + Mh` on clusters, with `solve_r0(pp["Mfair"], pp["rta"], s)`. The cold share is f_c = R_nat/(1 + R_nat) = 0.8405. No earlier lane in this line applied it. Applying it keeps the zoom's r₀ exactly (K2), which the old call did not.

## Frozen grade (canonical; X74's grader; both h cells; cluster masses ng 48)
η used at 10¹² / 10¹³ / 10¹⁴: 21.80 / 14.85 / 14.22, from CE1's 25.94 / 17.67 / 16.91.

| f★, CE1 η point | SPARC Υ (bg A/B) | groups Z | G-IN-Mall (h 0.672/0.686) | G-MID-T3 | result |
|---|---|---|---|---|---|
| 0.034, median | 0.51 / 0.50 | +1.62 | −1.95 / −1.64 | −1.71 / −1.13 | **PASS** |
| 0.034, p16 | 0.52 / 0.52 | +1.67 | −1.70 / −1.44 | −1.45 / −0.89 | PASS |
| 0.034, p84 | 0.49 / 0.49 | +1.55 | −2.23 / −1.88 | −2.00 / −1.40 | FAIL (SPARC line, G-IN-Mall) |
| 0.0615, median | 0.51 / 0.50 | +1.62 | **−2.004** / −1.69 | −1.93 / −1.34 | **FAIL by 0.004 in Z** (G-IN-Mall) |
| 0.0615, p16 | 0.52 / 0.52 | +1.67 | −1.75 / −1.48 | −1.66 / −1.09 | PASS |
| 0.0615, p84 | 0.49 / 0.49 | +1.55 | −2.29 / −1.93 | −2.23 / −1.62 | FAIL (SPARC line, G-MID-T3, G-IN-Mall) |

**Label: F★-DEPENDENT** as frozen (median passes at one f★ only). For comparison, CE1 without the factor: Υ 0.48, G-MID-T3 −2.30, G-IN-Mall −2.55, failing at both f★ and all three η points.

**Alt: COLD-SHARE FAIL**, on the SPARC line (Υ 0.44), which X78 traces to the law, not to route E. Its cluster and group numbers equal canonical's.

**Read it as the edge, not a pass.** The result sits on the G-IN-Mall line, and the SPARC line is at 0.50 on background B. A4 replaces the ng 48 cluster masses; `watch_A4_then_FC1.sh` reruns this grade when CE1's A4 tables exist, and A4's label stands if it differs.

## What it changes in the record
- **External c_f = 4 is no longer the only way to reach the grader's window.** The η values here come from the zooms and the native Ω_c/Ω_b alone.
- **The mass-independent softening the lanes were hunting for (R 0.81–0.85 at every mass) has a plain source at the level of the factor.** It is not a physical softening. SN (CM1–3, SH1), black-hole (CL4, CL5, BH1) and gas-cycle channels are not needed to reach this edge. They are not excluded either.
- It is **post-hoc in origin**, as the criteria state: I found it after seeing the required R. The protection is that there is nothing to tune.

## Reported, not graded
**S only** (no mass-argument conversion): same labels at each f★; Υ 0.51 / 0.51.

**By V_flat (canonical, `fc1_ls1.out`), ΔV at Υ 0.50, 2–4 R_d:**

| V_flat | n | c_f 4 | converged η | this rule | law | rule S vs ET1 S_need at Υ 0.50 |
|---|---|---|---|---|---|---|
| 20–60 | 13 | +3.7 | +3.7 | +3.7 | +2.4 | 107 vs 69 [52, 85] outside (floor; ET1's M200 caveat) |
| 60–100 | 35 | +2.9 | +2.9 | +2.9 | −2.0 | 107 vs 103 [81, 124] inside |
| 100–150 | 23 | −6.4 | −5.6 | −6.4 | −6.8 | 107 vs 143 [118, 200] outside |
| 150–200 | 25 | −12.6 | +1.3 | −3.8 | +5.2 | 136 vs 150 [98, 190] inside |
| 200–250 | 18 | −34.7 | −7.8 | **−16.2** | −12.5 | 156 vs 215 [137, 272] inside |
| 250–400 | 10 | −65.5 | −51.0 | −56.7 | −40.0 | 161 vs 412 [182, 596] outside (every model short) |

The L★ deficit is about half of c_f 4's and close to the law's on the same statistic. It is not removed. Below 150 km/s the floor still disagrees with S_need as in ET1.

**Milky Way (`x79_rule/`):** FEASIBLE (WIDE PRIORS ONLY) on the MW box, 8 all-four cells at R_d 1.93–2.27 kpc. In-prior best v_c 211.4 at R_d 2.60; McMillan 202.9, against Eilers 229.1 ± 4.6. This is the same class as SH1 at R 0.817. The Milky Way is **not** fixed.

**KiDS isolated, X53 harness (`x79_rule/`):** Δχ²(H2H − L2H) +434 canonical, +464 alt, class LAW. S hardly touches R > 100 kpc, so this rule does not move lensing. See BL1 and SI1.

## Checks
K1 (factor 1 reproduces CE1: SPARC, cluster predictions, both footings, |d| 0), K2 (`solve_r0` scale identity 7e-15), K3 (S/Σ_coll at the nodes 21.802 / 14.849 / 14.217 equal f_c × table), K4 (f_c 0.84055; background A's 1 − f_b 0.84387, background B's 0.84055; K4 passes at ≤ 0.01), MUTATE (factor 0.5: Υ 0.51 → 0.56, G-IN-Mall prediction 4.72 → 3.03): all PASS.

Disclosures: the first launch stopped at a code error (`BGS["fb"]`) before any grade existed. The first downstream launch could have moved files in a shared folder; it was killed before it did and the move now filters by name.

## What this does not show
- The baryons are dust in the zooms. Hot extended gas would let the cold fluid expand further. Condensing baryons contract it, and X39's full Blumenthal contraction breaks SPARC. **Contraction is the largest assumption left untested on this rule.** It pushes the wrong way, and a softening channel would then be needed again at galaxy scale.
- The zoom η values are converged by extrapolating each halo's NFW fit (X81), and f_c is applied on top.
- The floor is still by hand. Nothing here derives κ. Nothing here says the data favour the framework.

κ = ½ FITTED. Footings never pooled. Cold dark energy is a gravitating field component, never a particle. Not theory closed.
