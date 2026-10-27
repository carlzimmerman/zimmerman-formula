# CFG407 FROZEN CRITERIA: is the heavy-cluster outer excess real? X43's predicted total mass at R500–R200 vs X-COP hydrostatic masses

Committed alone, with its LEDGER row, before any script exists and before any X43 prediction for an X-COP cluster has been computed. κ = ½ FITTED; footings are never pooled; cold dark energy, never a particle; not theory closed. Nothing here says the data favour the framework. Owner (2026-10-27): "Yes, write frozen criteria for CFG407: X43's predicted outer mass (1-2 R500) vs X-COP hydrostatic masses for the heavy clusters, with the native 5.2715 background as a variant. Check data on disk first." The owner chose ID CFG407, a spare in the 10-06 block 400–409. It is unused in the LEDGER, directories and committed .md files.

## Why
- **X43** (00bc1a7950) fails G-OUT-M3: the heaviest eRASS1 gas tercile's OUTER KiDS shear (1.42–3 Mpc) is under-predicted. Measured/predicted ratio 1.369 / 1.120 = 1.22, Z +2.41.
- **CFG406** (25916e108d) showed this is **not** Eddington selection (it worsens to Z +2.91).
- **NU1 / CFG922** showed that gas beyond the aperture is the wrong sign or has no lever.
- The open question is whether the excess is real mass or a lensing-side effect. X-COP gives an independent measurement for exactly this class: hydrostatic total masses of 12 massive clusters out to R200, from X-ray gas density and SZ + X-ray temperatures, with no lensing and no eRASS1.

## Data on disk (checked 2026-10-27; nothing to download)
`real_research/data/xcop/`, 12 clusters: A85, A644, A1644, A1795, A2029, A2142, A2255, A2319, A3158, A3266, RXC1825, ZW1215. HydraA is in the R500 table but has no profile files, so it is not used.
- `*_hydro_mass.fits` HDU1: RADIUS (kpc, 30–3000), **M_FORW / EM_FORW** (the forward hydrostatic mass, used here). The NFW / Einasto / ISO / Burkert / Hernquist columns are halo-model fits and are **not** used for grading.
- `*_fgas_profile.fits` HDU1: RADIUS in **R/R500** (CFG450 U1), MGAS (+lo / hi), and M_NFW, which is used only for the unit check K3.
- `*_mstar.fits` HDU2: RADIUS (kpc), MSTAR (+lo / hi).
- `xcop_r500_ettori2019.json`: z, R500 (Mpc), M500, R200, M200 (Ettori+2019; h = 0.70, Ω_m = 0.3). R200/R500 is 1.50–1.70.

**The radial range is capped at R200.** X-COP's temperatures, and so M_HSE, are measured to about R200. The 3000 kpc tail of M_FORW is the forward model's extrapolation. The owner's "1–2 R500" therefore becomes **[R500, R200]** for every cluster, since 2 R500 lies beyond the measured range for all 12.

## Prediction (X43 as committed, applied to X-COP clusters)
- **Machinery.** `x43_collapse_core.py` is exec'd up to its final per-footing loop (`for f in FEET:` at line 235), which brings in X43's EM1 + X30 machinery, EPS tables, `sigma_coll`, `sig_core`, `solve_r0`, `B`, `ETA` (c_f = 4, η = 14.83) and `ETA_USE`. No X43 file is written: X43's own output paths are redirected here, as in CFG406.
- **One X-COP cluster, primary recipe (= the recipe X43 uses for the KiDS clusters):**
  - Gas: X30's `gas(Mg500, R500, "P")`, with Mg500 = X-COP MGAS at R/R500 = 1 and R500 from the JSON.
  - Baryons: M_b = gas × 1.20.
  - M_bt = M_b at 3 Mpc.
  - r_ta = `r_ta_com`(M_bt)/(1 + z) and M_fair = 5.364 M_bt, as in X30's `prep`.
  - Σ = `sig_core`(foot, "A_c2b_refit", (M_fair + M_bt)/M☉).
  - r0 = `solve_r0`(M_fair, r_ta, Σ).
  - M_h(<r) = π Σ r0² B(min(r, r_ta)/r0).
  - **M_X43(<r) = M_b(<r) + M_h(<r)**: route E, Newtonian, the same total X43 projects for KiDS.
- **Distances, as X43 does for eRASS1:** X-COP radii and masses are converted from their h70 / Ω_m 0.3 distances to the record's BAO-raw distances. q = [DM(z, h)/(1+z)] / D_A(h70, Ω_m 0.3), with X30's `DM` at both h cells (0.672, 0.686). Scalings: r × q, M_HSE × q, M_gas × q^2.5, M★ × q². q is printed and is expected to be ≈ 1 at z < 0.1.
- **Both footings × both h cells:** four cells, exactly as X43 grades.

## Statistic (graded)
- **Radii:** for each cluster i, five radii r_k = R500 (R200/R500)^(k/4), k = 0…4.
- **Per radius:** Δ_ik = log10[ M_HSE(r_k) / (1 − b) / M_X43(r_k) ]. M_HSE is M_FORW interpolated in log–log.
- **Per cluster:** Δ_i = mean over k.
- **Sample:** Δ̄ = mean over the 12 clusters, with **se = std(Δ_i, ddof 1)/√12**. The cluster-to-cluster scatter carries measurement error, HSE scatter and model scatter.
- **Also reported, not graded:** χ² against EM_FORW, the per-cluster Δ_i and Δ_ik, and Δ at R200 alone.
- **Hydrostatic bias cells:** **b = 0** (raw M_HSE, a **lower bound** on the true mass, since non-thermal pressure only adds support) and **b = 0.3** (CFG432's generous upper bracket). b* = 1 − 10^(Δ̄(b=0)) is the uniform bias at which X43 would match, reported when Δ̄(b=0) < 0.

## Reading (frozen; primary recipe; must hold in all four footing × h cells, else MIXED, with each cell named)
- **EXCESS CONFIRMED:** Δ̄(b = 0) ≥ +2 se. Even the hydrostatic lower bound exceeds X43 in the R500–R200 band. The KiDS heavy-tercile excess is real mass, independent of lensing and eRASS1, and the core law under-supplies heavy-cluster outskirts.
- **X43 OVERPREDICTS:** Δ̄(b = 0.3) ≤ −2 se. X43 exceeds even the maximally bias-corrected mass, so the KiDS excess is not supported by X-COP and points to the lensing side.
- **CONSISTENT:** neither. X43 lies between the raw and the b = 0.3 hydrostatic mass. b* says how much non-thermal support X43 needs. X-COP cannot confirm the KiDS excess at this precision.
- **Reported link (not graded):** KiDS says X43 is short by 0.087 dex (×1.22) in projected ΔΣ at 1.42–3 Mpc for heavy clusters. Δ̄ is printed beside it. The two are not the same quantity (3-D enclosed mass vs projected excess surface density); no conversion is graded.

## Variants (reported; any class change versus primary is flagged in the README's first lines)
- **V-NAT (owner's variant): native background.**
  - Ω_c/Ω_b = 5.2715 replaces 5.364 in M_fair, and Ω_m = 0.2976016, h = 0.6856427, Ω_b = 0.0223081/h² replace X30's OB946 / OC946 / H0_946 in `r_ta_com` (L1 / CFG886, as in P1D1).
  - The collapse table switches to EM1's `B_cfg886_bg` background, **if** K5 confirms it is the same CFG886 fit (h and Ω_m equal to L1's within 1e-4). If K5 fails, V-NAT swaps only the ratio and background constants, keeps "A_c2b_refit" for σ_coll, and says so.
- **V-MEAS: measured X-COP baryons.**
  - Gas: MGAS (fgas file, ×q^2.5) to its last point, continued with X2's "P" shape matched in density at the last point, out to 3 Mpc.
  - Stars: MSTAR (HDU2, ×q²) to its last point, then continued ∝ gas.
  - M_fair and r_ta follow from this M_bt.
- **V-INNER (reported only):** Δ̄ over 0.3–0.7 R500 with the same recipe. This shows whether any outer offset is just a global offset; cores are graded elsewhere (CS1 / CS2).

## Controls (each must pass, or the lane is INVALID)
- **K1 machinery live:** after the exec, X43's `grade_clusters("canonical")` reproduces the committed h0672 `pred` of G-OUT-M3 and G-OUT-all to ≤ 1e-9.
- **K2 rule identity:** for three eRASS1 clusters (index 0, N//2, N−1), the single-cluster function, fed X30's `prep` dict, gives M_h equal to X43's in-loop expression (sig_core → solve_r0 → π Σ r0² B) to ≤ 1e-12 relative.
- **K3 X-COP units:** for all 12 clusters, the fgas file's M_NFW at R/R500 = 1 matches the hydro file's M_NFW at the JSON R500 within 1.5 % (CFG450 U2 reproduced).
- **K4 coverage:** each cluster's MGAS profile reaches ≥ 0.95 R200. A cluster that fails is **reported and kept**, with its band flagged as extrapolated gas. No cluster is dropped.
- **K5 background identity (V-NAT only):** `B_cfg886_bg`'s h and Ω_m equal L1's to 1e-4.
- **MUTATE (rc 1):** the predictions are paired with the X-COP clusters in **reversed** M500 order. The rms of Δ_i must at least double relative to the primary. This shows the prediction tracks each cluster, not just the sample mean.

## Not blind (disclosed)
- Seen before freezing: the R500 / M500 / R200 table for all 13 entries; A2142's column names; A2142's first and last rows (M_FORW at 30 kpc and at 3000 kpc, both outside the band); the CFG432 / CFG656 / CFG450 / CS1 / CS2 headlines (older theories, or cores only); and the KiDS / CFG406 numbers above.
- Not seen: no M_HSE value inside [R500, R200] for any cluster; no X43 prediction for any X-COP cluster.
- **Expectation:** none quantitative. If the KiDS excess is real 3-D mass, Δ̄(b = 0) of about +0.05 to +0.1 dex is plausible. A merger-heavy sample (A2142, A2255, A2319, A3266 are disturbed) could scatter the HSE masses either way. No cluster is excluded for dynamical state.

## Disclosed inherited inputs
- **Primary = X43 as committed.** It includes the Planck ratio 5.364 and X30's OB946 / H0 67.4 in `r_ta_com`, which conflict with the owner's 10-25 rule. V-NAT is the native counterpart, at the owner's request. "A_c2b_refit" is X43's committed EPS background, and c_f = 4 is X43's one external number.
- **X-COP side:** R500 / R200 are Ettori's (h70, ΛCDM ρ_c definitions), used only as radius labels. Distances are converted to BAO-raw as above. M_FORW assumes hydrostatic equilibrium, hence the b bracket.

## Statement-change rule
- Only the X43 entry in LEDGER (and STANDING, if a line exists) may change: the heavy-cluster outer excess is labelled "confirmed by X-COP hydrostatic mass", "not confirmed (CONSISTENT, b* = …)" or "contradicted (X43 OVERPREDICTS)", per the frozen reading.
- No a0 value, no "favours", no change to X43's frozen verdict.

## Compute and files
Single thread (nice), CPU only. About 1–2 min: X43 head exec ~40 s, K1 grading ~20 s, X-COP evaluation in seconds. RSS < 1 GB, no downloads. This is allowed under the small-job rule while the X48 runs are live. Script `cfg407_xcop_outer.py` (`MUTATE=1` for the pairing reversal). Outputs: `cfg407.out`, `cfg407_results.json`, `_MUTATE` siblings, README. Nothing is written outside this directory.
