# CFG800 ADDENDUM (2026-10-18): the "Binary Emergent Gravity" rival, registered for Gaia DR4 before DR4 exists

**Status.** Written 2026-10-18, before Gaia DR4 (ESA planned date 2026-12-02) and before any DR4 data are read. It only adds: `FROZEN_CRITERIA.md`
(aa71ca510), the CFG740 sealed predictions, CFG825's `FROZEN_CRITERIA.md` (lane dir `CFG816_dr4_r_statistic_scoring`, d9eed26eb) and the DR4
preregistration are not touched, and no threshold, cut or class moves. It registers one more comparison number for the R statistic, with its
translation fixed now. κ = ½ is fitted, not derived; not theory closed.

## 1. Source, and what it does and does not contain
- **Record:** Zenodo 10.5281/zenodo.20544019, "Binary Emergent Gravity Applied to Wide Binary Stars: Predictions for Gaia DR3/DR4 and the
  Gravitational Boost", single author, published 2026-06-04, CC BY 4.0, no peer review indicated. Read 2026-10-18 from the record page and the
  Zenodo records API (the description text exactly as deposited).
- **The one attached file** (`BEG_Article2_Final-V1.md.pdf`, 8 pages, md5 `0bb0fcf8c4212e49b7b51fd7e2dade93`, matching the record's checksum) is
  **not the wide-binary paper.** It is the companion "Paper II" on the non-perturbative ("deep Zone II") regime: algebraic identities, an
  entropic sound speed c/√3, and a Sirius A/B drift velocity. It contains **no wide-binary prediction, no 1.077, no derivation of it and no
  uncertainty**; wide binaries appear only in its acknowledgements. (Its Appendix E uses a0 = 6.548×10⁻¹⁰ m s⁻², not 1.2×10⁻¹⁰.)
- **So the prediction registered here rests on the record's abstract alone.** Its derivation is not in the deposit and cannot be checked.

## 2. The prediction (record abstract)
- **Observable:** a gravitational boost γ_g = G_eff/G_N, i.e. an acceleration ratio at fixed mass and separation.
- **Number:** ≈ 1.077, "γ_g = G_eff/G_N ≈ 1.077, constant across all separations" (record abstract). **No uncertainty is given.**
- **Domain:** binary separations 500–30,000 AU, g_N ≈ 0.05–500 a0. **No separation dependence**: the abstract contrasts this with MOND, which
  gives no effect where g_N > a0, and attributes the boost to an entropic cross-term, not a change of the radial potential.
- **Its own discriminator:** Γ at g_N > 10 a0 with σ_Γ < 0.005, needing about 600 pairs with 3D velocities (it says Gaia DR4 can supply them).
  It reports agreement with Chae (2025) Bayesian-orbit results at < 2σ (not checked here).
- In velocity terms: v ∝ √(G M / r), so a uniform G_eff/G_N = 1.077 is a uniform velocity factor √1.077 = **1.0378**.

## 3. Translation into CFG825's R statistic
R = median ṽ over pairs with x = r_sky/r_M > 1 (s ≤ 50 kAU) ÷ median ṽ over pairs with x < 0.3 (CFG825 `FROZEN_CRITERIA.md` §1).
**Recipe, the same as for the registered MOND 1.15/1.20:** R_model = (velocity factor in the outer regime) ÷ (velocity factor in the inner
regime). For MOND the inner factor is ≈ 1 (Newtonian at high g), so R equals the outer velocity boost (Chae & Yoon's 1.15–1.20). CFG825 §1
states the consequence for any factor that does not depend on separation: it multiplies both medians alike and **cancels in R**.

**R_BEG = √1.077 / √1.077 = 1.000 exactly.**

Assumptions, stated:
- **A1.** γ_g is an acceleration ratio, so the velocity factor is √γ_g (the abstract defines γ_g = G_eff/G_N). Under the translation the reading
  does not matter: any uniform factor cancels.
- **A2.** "Constant across all separations" covers both R regimes. With R's a0 = 1.2×10⁻¹⁰, x < 0.3 is g_N ≳ 7–11 a0 (de-projected or
  not), inside BEG's stated 0.05–500 a0. The registered DR3 catalogue spans 2–30 kAU, inside BEG's stated 0.5–30 kAU. Pairs at 30–50 kAU (the
  frozen numerator cap) lie outside BEG's stated domain. The exact comparison is the frozen `r_sky ≤ 30 kAU` branch; on the primary, the boost
  is assumed to stay constant out to 50 kAU.
- **A3.** Γ in the record's discriminator is taken in the Chae convention, Γ = log10 √γ_g (the record does not define it). BEG then gives
  Γ = 0.0161, which is 3.2 × its stated σ_Γ = 0.005.

## 4. Distances in units of σ_R
σ_R values: DR3 **0.1775** (CFG825 C4, N = 348). Expected DR4 **0.0276** at the prereg's frozen N = 30,000 (σ_fit 0.019 ⊕ σ_sys 0.02; CFG825 C3
table; the prereg rounds it to 0.028). Floor **0.020** (σ_sys alone; no DR4 sample goes below it).

| registered number | R | (R − R_BEG)/σ_R at DR3 0.1775 | at DR4 0.0276 | at the floor 0.020 |
|---|---|---|---|---|
| Newton / Arm C | 1.000 | 0.00 | 0.00 | 0.00 |
| framework, CFG740 stiffness (R − 1 ≤ 3.2e-4 at ≤ 30 kAU) | ≤ 1.0003 | ≤ 0.002 | ≤ 0.01 | ≤ 0.02 |
| MOND 1.15 | 1.15 | 0.85 | 5.44 | 7.50 |
| Arm A canonical floor | 1.1614 | 0.91 | 5.85 | 8.07 |
| Arm A alt floor | 1.1917 | 1.08 | 6.95 | 9.58 |
| MOND 1.20 | 1.20 | 1.13 | 7.25 | 10.0 |

The CFG740 row uses the sealed envelope γ_v − 1 = 1.4e-6 / 8.9e-6 / 3.2e-4 at 2 / 5 / 30 kAU (inner regime ≈ 1e-6, outer ≤ 3.2e-4).
The DR3 C4 value R = 0.973 ± 0.178 sits 0.15 σ_R from R_BEG, the same as from Newton.

## 5. Can DR4 separate BEG from the framework?
- **Under the frozen R rule: no, at any N.** R_BEG and the framework's R differ by ≤ 3.2e-4, against a σ_R floor of 0.020 (a ≥ 60× gap). BEG
  and CFG740 receive the same label from the same data (KILLED, CONSISTENT or UNDECIDED). BEG is separated from Arm A and from standard MOND
  exactly as Newton is (5.4–7.3 σ_R at N = 30,000).
- **Stated against interest: the frozen rule is blind to a uniform boost.** CFG740's sealed envelope is an absolute velocity boost, and its
  falsifier reads "γ_v ≥ 1.01 at s ≤ 50 kAU". BEG's uniform excess γ_v − 1 = 0.038 is 3.8× the falsifier's 0.01 and about 120× the sealed 30-kAU envelope (3.2e-4). If an absolute
  boost of that size were established, it would contradict CFG740. The frozen DR4 rule measures γ_v relative to the inner regime (it must,
  because Cookson et al. fit a free normalization), so it cannot see such a boost. This addendum records the blind spot; it does not change the
  rule.
- **Where the contrast lives: the absolute normalization at high acceleration.** That is BEG's own discriminator (Γ at g_N > 10 a0). BEG gives
  Γ = 0.0161 (A3). CFG740 gives Γ ≲ 4e-6 at ≤ 5 kAU, as does Newton. At BEG's σ_Γ = 0.005 that is a 3.2σ separation, but it is degenerate with
  two effects. (i) ṽ depends only on the product G·M, so a 7.7% boost is identical to every total mass being 7.7% low (0.032 dex). (ii)
  Undetected close companions raise ṽ in the same direction (CFG825 §0). A 3σ absolute test therefore needs the mass scale, including hidden
  companions, known to ≲ 2.5% per sample. **No frozen file registers such a test.** Adding one needs its own criteria, committed alone before
  DR4; this addendum does not do that.

## 6. Sensitivity: readings that are NOT the record's stated prediction
For orientation only, if a boost were confined to the outer regime (contrary to "constant across all separations"):
- Acceleration reading, outer velocity factor √1.077: R = 1.0378. That is 0.21 σ_R from Newton at DR3, 1.37 at DR4 (0.0276) and 1.89 at the
  floor. KILLED would need σ_R ≤ 0.0126, below the floor, so the label is UNDECIDED at any N.
- Velocity reading, 1.077 as a velocity factor: R = 1.077. That is 0.43 / 2.79 / 3.85 σ_R from Newton at DR3, DR4 and the floor.
Neither reading is registered as BEG's prediction. The registered R-equivalent is **1.000** (§3).

## 7. Not claimed
No measurement and no score of BEG against data. The arithmetic is in this file (σ_R values from CFG825's committed outputs). Nothing here says
the data favour the framework, BEG or Newton. A Newtonian R from DR4 would leave BEG, Newton and CFG740 tied on this statistic.
