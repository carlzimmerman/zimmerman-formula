# CFG559: a kinetically supported settled profile. Verdict: DOES NOT resolve the growth / KiDS conflict (both footings)

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (8485002fc). Date: 2026-10-10.
- **Scripts** (all `nice -n 10`, ≤ 4 processes, 1 thread each; no PM, no downloads):
  - `cfg559_toy.py` (task 1, about 2 h on a shared machine): the CFG544 toy, imported unchanged, run per halo. Writes `cfg559_toy.out`, `cfg559_toy_results.json`. `CFG559_MUTATE=1` runs the σ ×2 cells (`_MUTATE`).
  - `cfg559_lib.py`: Δm(x) interpolation from the toy JSON.
  - `cfg559_tests.py`: halo model, groups, MW, LG. `CFG559_MUTATE=1` → MK0 + MK2 (exit 1 = all teeth bite).
  - `cfg559_kids.py`: KiDS f30. `CFG559_MUTATE=1` → MK0 + MK2 (exit 1). Tables cached outside git in `_external_data/cfg559_work/`.
- **Settings:** κ = ½ is FITTED. Footings 9.3603e-11 / 1.1312e-10, never pooled. ν_mono, candidate B, G9, no EFE. The cold energy's MASS is still required; no particle species. Not "theory closed"; nothing here says the data favour the framework.
- All numbers come from the `*_results*.json` files. Pairs are canonical / alt.

## 1. How the kinetic profile is posed (task 1)

- **What the cold energy feels.** G9: baryons + all settled cold energy (real mass); the phantom never enters Φ. In candidate B the settled cold energy IS the phantom, so the self-consistent requirement is ρ_c = ρ_ph wherever the supply holds it. FIX-2's two-sided drift enforces that; its Ornstein–Uhlenbeck relaxation toward the isotropic Jeans dispersion of the *current* density in the *current* real-mass field supplies the kinetic support (CFG554 route (b)). The isotropic target is POSITED (CFG554; CFG558, finished meanwhile, labels it ISOTROPY CHOSEN and keeps FIX-2 as the working candidate).
- **Solve.** Direct, per halo, no scaling assumption: CFG544's spherical N-body toy (N = 30000), FIX-2, IC-B (cold infall from r_ta), α = 1, 10 Gyr, point-mass baryons M_b = f_ret f_b M_ta, settled mass M_set = s_c*(1 − f_b)M_ta with s_c* = CFG557's α-free finite-age ceiling (primary) or 1 (declared variant), sharp edge r_* = r_M/ln(1 + M_b/M_set), r_ta from CFG556. Grid: log M_ta 11–15 in steps of 0.5, both footings.
- **Output.** Δm(x) = m_kin − m_sharp (cumulative settled-mass fraction vs x = r/r_*, averaged over the last 1 Gyr). In every test, the source lane's sharp settled profile gets + M_set Δm(r/r_e). Nothing else changes.
- **Controls:** C5 reproduces CFG544's FIX-2 IC-B end states exactly (Δ = 0, MW_can and cluster_can). C6 m_sharp(1) = 1 to 4e-16. C7 mass exact everywhere. All 36 cells pass CFG544's gate (steady, |D|, |log X| ≤ 0.1). KK0 passes.

**The profile (primary, canonical; alt within ~0.03):**

| log M_ta | s_c* | r_*/r_ta | kinetic r_99/r_* | ln(r_99/r_99,sharp) | r_99/r_ta | Δm(0.3) | Δm(0.5) | Δm(1) | β |
|---|---|---|---|---|---|---|---|---|---|
| 11 | 0.798 | 0.190 | 1.32 | +0.29 | 0.25 | +0.009 | +0.015 | −0.098 | 0.08 |
| 12 | 0.770 | 0.271 | 1.30 | +0.27 | 0.35 | +0.010 | +0.019 | −0.094 | 0.09 |
| 13 | 0.702 | 0.206 | 1.36 | +0.32 | 0.28 | +0.003 | +0.005 | −0.118 | 0.15 |
| 14 | 0.616 | 0.192 | 1.68 | +0.53 | 0.32 | −0.013 | −0.024 | −0.181 | 0.30 |
| 15 | 0.501 | 0.211 | 2.03 | +0.72 | 0.43 | −0.013 | −0.043 | −0.236 | 0.37 |

- The edge softens outward by +26% to +72% in r_99 (CFG544/554's +25–55% range, larger in the point-mass-dominated cluster cells). 10–24% of the settled mass moves beyond r_*.
- **Inside 0.5 r_* almost nothing moves** (|Δm| ≤ 0.04). The kinetic tail comes from the outer shell, just inside the edge. That is why the mass at ~0.2–0.3 r_ta barely drops.

## 2. Tests (primary supply)

| test | rule | canonical | alt |
|---|---|---|---|
| (i) growth, CFG556 halo model | max\|R−1\| ≤ 0.10 and σ8 within 5% | **FAIL**: E +0.290 at k 0.99 (sharp +0.382), σ8 1.0139 | **FAIL**: E +0.375 (sharp +0.458), σ8 1.0175 |
| (ii) KiDS f30 | p > 0.01 in A and B | **FAIL**: χ² 57.77 (p 6.1e-7) / 63.97 (p 5.2e-8); sharp 59.13 / 66.04 | **FAIL**: 48.80 (p 1.9e-5) / 53.61 (p 3.0e-6); sharp 50.44 / 55.50 |
| (iii) groups, CFG543 P2 | \|Z\| < 2 | **FAIL** (marginal): +0.0771, Z +2.05 (sharp +0.0732, Z 1.97) | **PASS**: +0.0637, Z +1.68 |
| (iv) MW inside 30 kpc | \|ΔV_c\| ≤ 5.4 km/s, \|ΔΣ\| ≤ 5.8 | **PASS**: ΔV_c ≤ +0.97 ± 2.05 km/s; ΔΣ_dark(R0) +0.25 ± 0.81 | **PASS**: ≤ +1.94 ± 2.16; +0.02 ± 0.85 |
| (v) LG timing, CFG522 | \|z_full\| < 2 | **PASS**: −0.43 (sharp −0.42) | **PASS**: −0.41 |

- **(i) Growth.** R(k = 1) goes from 1.385 / 1.462 to 1.292 / 1.378, about a quarter of the remaining excess. Ratio form +0.225 / +0.290. Drivers at k = 1: log M_ta 14–15 gives +0.226 / +0.271. M_F/M_L at 0.3 r_ta is still 1.28–1.31 at log M_ta 13–14 (canonical). The effective edge r_99/r_ta becomes 0.28–0.43. The concentrated part (0.1–0.3 r_ta) is the drift-held law profile inside the edge, which kinetic support does not touch.
- **(ii) KiDS.** The median effective edge x_99 moves from 0.196 to 0.256 (canonical) and from 0.169 to 0.224 (alt). KiDS prefers 0.45–0.50. χ² drops by only 1.4–2.1; the outer-6 χ² does not move (33.58 vs 33.63). The small gain is in the inner 9 bins (−1.0 / −1.4). Δ vs the best sharp node is still +17.2 / +13.0 (canonical A / B).
- **(iii) Groups.** The Tian+26 groups' edges sit at only 1.5–5 Re (median 2.5 Re) in the P2 configuration, so the tracer samples the region just inside the edge. That is where the kinetic tail takes its mass from (Δm(1) ≈ −0.12, many times the Poisson error ~0.002). The predicted σ therefore drops, and the canonical P2 mean rises past the line, from Z 1.97 to 2.05. This is a real effect of the redistribution, not noise. It is marginal.
- **(iv) MW.** The edge moves from 389 to a kinetic r_99 of 502 kpc (canonical) and from 351 to 459 kpc (alt). Every shift inside 30 kpc is within one Poisson σ of the toy. The CFG553 sealed predictions are not changed.
- **(v) LG.** M_eff(<780 kpc) is unchanged (5.367e12 / 5.388e12): the tail stays inside 780 kpc (r_99 296/409 kpc). The strict radial z_meas is +3.06 / +3.13.

**Declared variant: full turnaround supply + kinetic (reported, no verdict).**
- Growth E +0.600 / +0.750 (CFG556 sharp +0.715 / +0.883).
- KiDS χ² A/B 43.32 / 50.87 (p 1.4e-4 / 8.7e-6) canonical and 34.49 / 40.04 (p 2.9e-3 / 4.5e-4) alt. That is a large improvement (outer-6 33.6 → 23.3), and B canonical reaches the best sharp node (Δ −0.15). It still fails p > 0.01.
- Groups +0.0597 Z 1.63 / +0.0444 Z 1.21; LG z_full −0.11 / −0.10.
- So with the full supply, kinetic support moves KiDS a long way toward the data, but growth is then 6–7× over the bar.

## 3. Overall (frozen rule)

- **canonical: DOES NOT** (growth FAIL, KiDS FAIL; groups FAIL marginally; MW PASS; LG PASS).
- **alt: DOES NOT** (growth FAIL, KiDS FAIL; groups, MW, LG PASS).
- The kinetic profile does move both growth (E −0.09 / −0.08) and KiDS (χ² −1.4 to −2.1) toward the data, but by far too little.
- **Plain reading.** Kinetic support spreads only the outer ~10–25% of the settled mass, just inside the edge. The excess that drives growth sits at 0.1–0.3 r_ta, held to the law's profile by the drift. KiDS needs settled mass out to ~0.45–0.5 r_ta, and only a larger supply does that (variant), which brings growth back. **The conflict is between the law's own isothermal profile inside the edge (growth) and the edge position (KiDS). An equilibrium velocity part does not decouple them.**

## 4. MUTATE (all teeth bite; both MUTATE scripts exit 1)

- **MK0, kinetic support off (Δm ≡ 0):**
  - halo model R(k) and σ8 equal CFG557's TESTED exactly (max |ΔR| 0, |Δσ8| 0);
  - groups +0.073187 / +0.059170 (= CFG557);
  - MW edge 389.3195 / 351.3893 kpc (= CFG557);
  - LG z_full −0.423437 / −0.407716 (= CFG557);
  - KiDS χ² from CFG557's cached tables through this scorer: max |d| 0.
  - Reported: the kinetic code path with Δm = 0 vs the source path, 20 random groups: max relative table difference 9.4e-16.
- **MK2, σ ×2 (OU target ×4):**
  - r_99/r_* is larger than σ ×1 in all 18 cells (2.6–4.4 r_*). All 18 are not steady at 10 Gyr (still expanding, log X +0.30 to +0.37), as expected for an overheated target.
  - Halo-model E falls to −0.000 / −0.000, with D −0.210 / −0.111. R(k = 1) is 0.787 on canonical, past the data side (< 0.90).
  - KiDS median x_99 0.526 / 0.468 (σ ×1 0.256 / 0.224), past KiDS's preferred 0.45–0.50. χ² 175.6 / 192.7 and 161.9 / 178.4: inner-9 bins starved (95 / 87).
  - So over-spreading overshoots both tests. The direction is right; the amount at σ ×1 is what the equilibrium gives.

## 5. Disclosures (dated 2026-10-10)

- **Toy limits** (inherited from CFG544/554): spherical; static point-mass baryons (the halo model's extended baryons enter only through the source lane's sharp profile, onto which Δm is added); α = 1 (O(1) FREE; CFG558: not α-robust); a 0.05 V_f seed; overfill not handled (CFG554/558). The z = 0 Δm table is applied to the KiDS lenses at z 0.1–0.5 at their own census M_ta.
- **The toy age is 10 Gyr** (CFG554's bench end state), not 13.8 Gyr. All primary cells are steady over the last 2 Gyr, so this is not expected to matter.
- **Mutate scale.** "σ ×2" was implemented as the OU σ² target ×4. This is stronger than CFG544's MT (σ² ×2).
- **Group mechanism** (post-run diagnostic, no verdict use): the P2 edge radii are 1.5–5.0 Re (median 2.5), computed from the CFG543 configuration with s_c*. The inner Δm at x ≤ 0.05 is positive (+0.001 to +0.007, 5–10 Poisson σ). It is outweighed by the edge-region deficit that the tracer samples.
- **MW Poisson errors** use N = 30000 and the interpolated m_kin. The ΔΣ_dark estimate is a shell average over 6–10.5 kpc.
- **Spurious FP warnings** ("divide by zero in matmul") are printed by the CFG556 code under Accelerate. They are the same flags CFG522 documents and do not affect results (MK0 reproduces CFG557 exactly).
- **Machine sharing.** The toy wall time was slowed by another lane running concurrently; this does not affect results.

Commits: criteria 8485002fc; results in the commit that adds this README.
