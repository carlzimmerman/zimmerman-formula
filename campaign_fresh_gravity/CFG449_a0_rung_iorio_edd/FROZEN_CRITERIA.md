# CFG449: growing the gas-dominated a₀ rung via EDD TRGB distances and Iorio+2017 curves. FROZEN before any fitting script exists

Owner chat 10-07 ("swing it all"; data fetches approved for this lane). κ = ½ is FITTED, never derived; both footings are reported (9.3603e-11 / 1.1312e-10 m/s²). No DM particle; the cold mass is still required. Never "theory closed"; the data are not said to favour the framework over ΛCDM.

**Why.** CFG397 (fe7a17fc5) measured a₀ from SPARC gas-dominated points: the 10 ladder-distance galaxies give log a₀ = −9.953 ± 0.071, NOT ESTABLISHED (needs σ ≤ 0.05). CFG442 (dd851292c) added nothing: CF4 gave no TRGB/Cepheid for the 20 non-ladder gas galaxies, and the Oh+2015 route failed the SPARC-overlap control (+0.196 dex).

## Pre-freeze data audit (disclosed; no a₀ and no g_obs vs g_bar was computed)
- **EDD CMDs/TRGB (Anand+2021, AJ 162, 80).** Not on VizieR (no J/AJ/162/80; bibcode search empty). The arXiv source (2104.02649) holds no table. The EDD table display (dsecond.php) is behind a reCAPTCHA; it was NOT bypassed, and EDD's per-galaxy pages are not used as a workaround. **Substitute (a real table):** the Karachentsev LVG catalogue (SAO, updated 2026-07-13) "List of distances" (lvg_table6.dat) + "Catalog" (lvg_table1.dat, positions), which carries per-galaxy TRGB moduli with references, including 2021AJ....162...80A (Anand+2021) and 2016EDD (the EDD CMDs/TRGB database). Its coverage is mainly D ≲ 11 Mpc. I read only its header and first ~25 rows (none of the target galaxies).
- **Iorio+2017.** The arXiv source points to the authors' site; the current Fraternali "downloads" page links `finalrot.zip` (17 `*_onlinetab.txt`, 2016). Columns: R (″, kpc), V_rot, V_AD, V_c (= √(V_rot² + V_AD²)), err, σ, HI surface density Σ_HI (M☉/pc², primary-beam corrected), at a stated distance. **There are no mass models** (no V_gas, no V_star). I viewed one file's header and 9 rows (DDO 53).
- **BIG-SPARC.** Only the IAU S392 proceedings (arXiv 2411.13329, 2024) and a 2025 talk exist. There is no data on arXiv, VizieR or the SPARC site as of 2026-10-07. **Not released.** Nothing to fetch.

## Samples
- **S0 (control).** CFG397's anchor, unchanged: CFG4_common.load_sparc(), Q ≤ 2, ≥ 3 gas-dominated points, f_D ∈ {2, 3, 5}. **C0:** reproduce log a₀ −9.953 and bootstrap σ 0.071 to within 0.002 each.
- **SR (SPARC re-distanced; the EDD route).** CFG397's selection with f_D ∈ {1, 4} (the 20 galaxies), at CFG442's Sesame positions (CFG442/data/sesame_sr.json).
  - Distance rule, in order: CF4 table2 DMtrgb, then CF4 DMceph (nearest CF4 entry within 1′, as CFG442; expected none); then LVG.
  - **LVG match:** the nearest lvg_table1 entry within 1′.
  - **LVG modulus choice:** among that name's lvg_table6 rows with n_DM = TRGB, prefer r_DM = 2021AJ....162...80A, then r_DM containing "EDD", then the most recent year; if there is no TRGB row, a Cep row by the same preference.
  - No other method qualifies (no mem, TF, BS, h, NAM).
  - Rescale with f = D_new/D_SPARC: R → fR; V_gas², V_disk², V_bul² → f × themselves; V_obs and e_V unchanged (CFG397/CFG442).
- **IO (Iorio+2017, new galaxies).** These are the 17 tables, main files only (ddo216b, an alternative model, is not used), minus the SPARC members DDO 50, DDO 87, DDO 126, DDO 154, DDO 168, NGC 2366 and WLM (CFG442's alias list). That leaves 10 candidates: CVn I dwA, DDO 47, 52, 53, 101, 133, 210, 216, NGC 1569, UGC 8508.
  - **V_obs, e_V:** Iorio V_c and err_Vc (asymmetric-drift corrected).
  - **V_gas:** 1.33 Σ_HI, using a razor-thin axisymmetric disc. Σ is linear in R between the tabulated radii, held at Σ(R₁) inside R₁, and zero beyond R_last + ½ΔR. The disc is cut into ≥ 3000 thin rings; Φ_ring = −(2Gm/π) K(k)/(a+R) with k² = 4aR/(a+R)²; V² = R dΦ/dR by central difference, at points off the ring radii.
  - **V_star:** a Freeman exponential thin disc, M* = Oh+2015 table2 MstarSED (Zhang+2012 SED), R_d = Hunter+2012 table1 Rd (V band), both at the Hunter distance. No MstarSED or no Rd means the galaxy is excluded. MstarK (kinematic) is never used, since it is circular.
  - **Distance rule:** CF4 DMtrgb, then DMceph, matched by the Hunter+2012 PGC as in CFG442; else LVG TRGB, then LVG Cep, by position (Oh table1 coordinates, 1′) with the same preference as SR; else excluded.
  - **Rescaling:** f = D_new/D_Iorio for R and V_gas²; f = D_new/D_Hunter for R_d and V_star² (M* ∝ D², R_d ∝ D).
- **K0b (method control for the IO gas integrator).** An exponential Σ sampled at Iorio-like spacing (ΔR = R_d/4, out to 10 R_d) must reproduce the analytic Freeman V² to within 2% (max |ΔV²|/V²) on 0.5–4 R_d. A failure means the IO route is not run (reported).

## Selection and fit (CFG397, unchanged)
- **Gas-dominated point:** V_gas|V_gas| ≥ 0.7 V_bar², where V_bar² = V_gas|V_gas| + 0.5 V_disk² + 0.7 V_bul² (SPARC) or V_gas|V_gas| + V_star² (IO); also V_bar² > 0 and V_obs > 0. A galaxy needs ≥ 3 such points.
- **Fit:** g = V²/R; w = 1/(max(e_V,1)/max(V_obs,1))². One free a₀ minimises Σ w (log g_obs − log[ν_mono(g_bar/a₀) g_bar])², bounded (−10.8, −9.3), xatol 1e-5. Bootstrap over galaxies: 500 draws, seed 7.

## Controls and verdict
- **C2 (IO overlap control).** Take the 7 SPARC-member Iorio galaxies, rescaled to the SPARC distance (Iorio R and V_gas² by D_SPARC/D_Iorio; V_star² and R_d by D_SPARC/D_Hunter). Each galaxy with ≥ 3 gas points in BOTH routes is fitted alone through the IO route and through the SPARC route.
  - **PASS** if EVERY such galaxy has |Δ log a₀| ≤ 0.10 dex, and there are at least 2 of them.
  - The joint-set Δ is also reported, as is any galaxy that sits on a fit bound.
  - **If C2 fails, IO is report-only.**
- **Verdict sample.** S0 + SR + IO if C2 passes; otherwise S0 + SR.
- **K1 (Υ check on the verdict sample).** SPARC Υ_disk goes 0.5 → 0.7 (bulge 1.4Υ); IO M* × 1.4; the point selection stays frozen at baseline. PASS if |Δ log a₀| ≤ 0.05.
- **RUNG ESTABLISHED** if the verdict sample has bootstrap σ ≤ 0.05 dex AND K1 passes. Otherwise NOT ESTABLISHED.
- **Reported:**
  - Δ from each footing and from PAPER43's 8.3e-11, in σ (|Δ| < 2σ = consistent);
  - the shift from CFG397's anchor;
  - D_new/D_SPARC per added SR galaxy;
  - IO-only and all-routes fits (the latter labelled not-the-verdict if C2 failed).
- **Disclosed departures:**
  - distance errors are not propagated (CFG397's statistic);
  - LVG stands in for the captcha-gated EDD table;
  - IO V_gas comes from Σ_HI through my own thin-disc integrator (truncated at the last ring), not the authors' model;
  - IO stars use a V-band R_d and SED M*.
- **MUTATE (`--mutate`).** V_gas → 0 in every route. The selection becomes empty; the script must detect it and exit 1, with outputs carrying the `_MUTATE` suffix.

**Data rules.** Every fetch goes in FETCH_LOG.md (URL, date, bytes, sha256). Files > 5 MB go to campaign_fresh_gravity/_external_data/cfg449/ (git-ignored). Light CPU.
