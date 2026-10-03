# CFG307 — FROZEN CRITERIA: stress test of ALESS 122.1's implied a₀ (the one class-M galaxy on the a₀(z) chart with a root)

> **Owner request: "stress test it" (ALESS 122.1).** A declared grid of the inputs the record and the source papers already hold; no knob scan, no fitting, no download. **κ = ½ is FITTED. FLAT a₀(z) is the framework's distinctive law; a₀ ∝ H(z) is the rival; ΛCDM has no a₀.** Framework-native inputs only: no halo-fit quantity enters a cell. The implied a₀ is descriptive, not a verdict; one galaxy is not a measurement of a₀(z). No sentence of this lane may say the data favour a law.

Written 2026-10-02 and committed BEFORE any g_obs, g_bar, D, s★ or interval of any new cell is computed.

## 0. What was seen before this freeze (stated first)
- **CFG229 (read in full: README, criteria + Addendum 1, `cfg229_score.py`, `a0implied.py`, the committed points, inputs and results JSON):** ALESS 122.1 at z = 2.024, R = 2 r_e = 10.630 kpc, V_circ(2 r_e) = 533 ± 37 km/s, σ = 157, g_bar = 4.533e-10, y = 4.84, D = 1.911, δ_FLAT = +0.226; **s★ = 8.82** (log₁₀ 0.945356), MC rooted-draw quantiles of log₁₀ s★ (2.5/16/50/84/97.5 %) = 0.1801 / 0.6227 / 0.9249 / 1.1575 / 1.3549 (68 % 4.20–14.37, 95 % 1.51–22.64), **no-root fraction 0.0103**; lever −2.0; the printed corners (gas ±0.03/±0.093: 9.74/7.93/11.8/6.16; stars ±1σ/±0.30: 10.6/6.58/11.2/5.49; joint outer 15.1/3.72) and variants (R_e × 1.5 14.2, ÷ 1.5 7.92, stars at 2 R_e 10.9, spherical 14.7, no He 13.2, P2 12.8; α = 1.68 / 3.36 → 13 / 17.9, **withdrawn as double-counted** by CFG229's Addendum of 2026-10-01). The six siblings' committed D (0.20–0.46, all NO ROOT, all BAND-DEPENDENT on the floor) and their MC no-root fractions (0.87–1.00).
- **CFG229's Addendum (CFG267 finding F2):** Amvrosiadis+ V_circ already contains the drift term; the rotation-only V ≈ √(533² − 3.36 × 157²) ≈ 449 km/s and "D would fall to about 1.35 … s★ would fall (not computed)".
- **CFG274** (the eight other Amvrosiadis discs: 7 of 8 NO ROOT; 075.1 s★ 6.9, ill-conditioned; its M5 cross-check of CFG229's ALESS 122.1 failed at 1.2e-6 because it re-derived the inputs; this lane reads CFG229's own input CSVs instead). **CFG228** (STANDING: the pressure convention alone moves ALPINE6 from no root to s★ 4.3). **CFG227/CFG237** (the S1 group; the offset sits in the SED stellar mass: JOINT / NOT DECIDABLE). **CFG140/141/303** (the LCDM-free pressure family P0 none, P1 Burkert constant-σ 2σ²R/R_d, P2 the same with the measured outer σ, P3 fixed scale height σ²R/R_d − R dσ²/dR; P4 Kretschmer+21 is LCDM-MODEL, VELA-calibrated). STANDING entries for CFG229/267/274.
- **Source papers on disk (read, not downloaded):** Amvrosiadis+ (arXiv 2312.08959 TeX, sha256 cc3b1226…; in the external data directory beside the repo, `../_external_data/arxiv_src/2312.08959/main.tex`): eq. 8 V_circ(r) = √(V_rot²(r) + 1.68 σ² (r/r_e)) for a constant σ and a radius-independent thick-disc height; V_rot(r) = V_max[1 − arctan(r/r_t)/(r/r_t)] (r_t not tabulated); ALESS 122.1 row r_e 0.62 (+0.07/−0.08)″, i = 55 (+8/−6)°, V_max 564 (+44/−17), σ 157 (+19/−18), V_circ(2 r_e) 533 ± 37; the text quotes Calistro Rivera+18's image-plane fit of the same data, V_max = 564 ± 8 and **σ = 129 ± 1 km/s**; the paper's α_CO = 0.92 is derived from M_dyn with an assumed f_DM = 0.25 (a halo assumption, so excluded below); the parent-table gas 11.30 ± 0.09 is Calistro Rivera+18's (footnote γ; its conversion is not on disk). A commented-out older row (V_circ 547 ± 39) exists in the TeX and is NOT a published value: not used. **Dunne+22** (arXiv 2208.01622 TeX, sha256 1616c847…; and the CDS tables already in the repo): Table "single tracer only" (incl. He): **SMGs α850 = 7.3 ± 0.1 × 10¹² W Hz⁻¹ M☉⁻¹, α_CO = 3.8 ± 0.1, α_CI = 16.2 ± 0.4**; all seven galaxies carry Dunne's SMG flag = 1. ALESS122: logLCO (CO(1–0)) 11.110 ± 0.067, JCorr 0, logL850 24.052 ± 0.049, no [CI]; opt_ad aCO = 1.406 (the other five CO galaxies 2.64–4.70), κ_H 3361.5, logMH2 11.258 ± 0.104.
- **Arithmetic done before the freeze:** the hand estimates of §8 (by hand, Bessel values from tables, the RAR shape as a stand-in), and **ν_mono evaluated at seven y values only** (0.549, 1.8, 4.843, 6, 8, 10.64, 18.6 → 1.911, 1.354, 1.136, 1.111, 1.084, 1.064, 1.037) to sharpen the hand estimates. No g_bar, g_obs, D or s★ of any new cell was computed by code.

## 1. The question
Does ALESS 122.1's implied a₀ (s★ = 8.82, above FLAT s = 1 and above H(z) s = E(2.024) = 3.0652) survive every declared, record-held choice of its inputs, or does it depend on one? And is it the outlier of a calibration the six class-M siblings share?

## 2. Machinery (CFG229's, unchanged)
- g_bar: one thin exponential disc (Freeman) carrying stars + gas with R_d = R_e/1.678, R_e = the CO r_e (5.31500 kpc), CFG229's `gdisc`; g_obs = V²/R; D = g_obs/g_bar.
- s★: CFG229's `a0implied.implied` (CFG223's estimator, bisection on log₁₀ s ∈ [−3, 3]) with ν_mono and the canonical a₀ = 9.3603e-11; implied a₀ = s★ × 9.3603e-11 m/s². **NO ROOT** = no s in [10⁻³, 10³] (D at the Newtonian floor); a root above the bracket is a LIMIT (counted as a root above every law).
- Inputs read from CFG229's committed `cfg229_inputs_static.csv` / `cfg229_inputs_kin.csv` (not re-derived; this is the CFG274-M5 lesson).
- **Statistical interval per cell (CFG229's convention, PRIMARY):** 10,000 MC draws with CFG229's random stream replayed exactly (seed 230, the seven galaxies in CFG229's order, so ALESS 122.1's draws are bit-identical): velocity split-normal (533 +37/−37), the source's stellar 1σ, the gas statistical error; percentiles 2.5/16/50/84/97.5 of log₁₀ s★ over the ROOTED draws, the no-root fraction beside; fewer than 21 rooted draws → interval undefined. **Common random numbers:** every cell reuses the same standard deviates; a cell's velocity draws are V_cell × (V_draw/533), its baryon draws use its own statistical error times the same deviates. **SECONDARY convention (beside):** the same percentiles over ALL draws with no-root draws placed at s → 0 (−∞) and bracket-limit draws at +∞. σ_int (0.15 dex) is NOT in either interval (as CFG229).

## 3. The grid for ALESS 122.1 (full factorial; every level from the record or a source paper on disk)
**(a) pressure / asymmetric drift** (5 levels). V_rot(2 r_e) is reconstructed by inverting the source's eq. 8: V_rot² = 533² − 1.68 σ² × 2 (≈ 449 km/s); the term T(R) is then added back:
| level | T(R) | origin |
|---|---|---|
| P0 | 0 (rotation only) | CFG140/141/303 P0 |
| C168 | 1.68 σ² (constant) | CFG229's α = 1.68 family, now applied to V_rot once |
| **EQ8 (committed)** | 1.68 σ² (R/r_e) | Amvrosiadis eq. 8 = the published V_circ at 2 r_e; ≡ CFG141 P3 for a constant σ (σ²R/R_d = 1.678 σ² R/R_e, 0.1 % from 1.68) and ≡ FS+18's constant 3.36 σ² at 2 r_e, so those are not separate levels |
| P1 | 3.36 σ² (R/r_e) | Burkert+10 / CFG140 P1 = CFG141 P2 with the source's (only) σ |
| MSIG | 1.68 σ_m² (R/r_e), σ_m = 129 km/s | the measured-σ variant: the committed form with the other measured dispersion of the same data (Calistro Rivera+18, quoted by the source) |
P4 (Kretschmer+21) is excluded (LCDM-MODEL). σ is not inclination-dependent.

**(b) gas** (6 levels; all as M_mol including He; [CI] has no ALESS122 measurement, so no [CI] level):
| level | M_gas | origin; statistical error |
|---|---|---|
| **G0 (committed)** | 1.36 × 10^11.258 | Dunne+22 opt_ad; ±0.104 |
| CO1 | 3.8 × L′_CO | Dunne+22 single-tracer, SMG row; ⊕ of 0.067 and the α error |
| DU1 | L′₈₅₀ / 7.3e12 | Dunne+22 single-tracer dust, SMG row; ⊕ of 0.049 and the α error |
| A08 | 0.8 × L′_CO | record ULIRG convention (CFG272/283/285); ±0.067 |
| A36 | 3.6 × L′_CO | record convention (CFG285 ADF22 M_mol); ±0.067 |
| A436 | 4.36 × L′_CO | record Galactic convention incl. He (CFG227/280/283); ±0.067 |
L′_CO = Dunne's CO(1–0) luminosity 10^11.110 (JCorr 0). Beside, never in the decision: Dunne's luminosity-dependent single-tracer fits (log α_CO = −0.062 log L′ + 1.25; log α850 = 0.052 log L850 + 11.60), the parent-table gas 11.30 (conversion not on disk), and Amvrosiadis's α_CO 0.92 (halo-anchored; shown only to say what it would do).

**(c) stellar mass** (3 levels): MAGPHYS 10^10.890 and ± its stated 0.21 dex. No other SED for ALESS 122.1 is on disk. CFG229's declared ±0.30 dex band is reported beside only.

**(d) inclination** (3 levels): 55° (committed), 49° and 63° (∓ the stated errors); V_rot scales by sin 55°/sin i, T(R) does not. No alternative geometry for ALESS 122.1 is on disk.

**(e) radius** (2 levels): 2 r_e (committed) and r_e. At r_e, V_rot(r_e) comes from the source's arctan law with r_t solved so that V_rot(2 r_e) equals the reconstructed value with V_max = 564 (r_t is not tabulated; mixing posterior summaries is an approximation, disclosed). g_bar at r_e from the same disc.

**N = 5 × 6 × 3 × 3 × 2 = 540 cells.** The committed cell is (EQ8, G0, M* nominal, 55°, 2 r_e).

## 4. Per cell (CSV `cfg307_grid.csv`)
V, R, g_obs, g_bar, y, D, s★ (or NO ROOT / LIMIT), log₁₀ s★, the lever λ = d log₁₀ s★/d(baryon dex) (CFG223 definition), the 68 % and 95 % intervals (primary and secondary), the MC no-root fraction, and for FLAT (log s = 0) and H(z) (log s = log₁₀ 3.0652): **inside the 95 % interval / excluded above (q2.5 above the law) / excluded below (q97.5 below the law)**; the alt-footing versions (FLAT at s = 1.2086, H(z) at 3.0652 × 1.2086); the P2-kernel nominal s★.

## 5. Decision rule (frozen; primary convention, canonical footing, all 540 cells)
Fractions over N: f_FLAT,excl = #(root and q2.5 > FLAT)/N; f_H,excl = #(root and q2.5 > H(z))/N; f_FLAT,in = #(root and FLAT inside the 95 % interval)/N (a rooted cell with an undefined interval counts as FLAT inside); f_noroot = #(no nominal root)/N.
1. **"NOT ROBUST"** if f_FLAT,in ≥ 0.25 or f_noroot ≥ 0.25 (checked first);
2. else **"ROBUSTLY ABOVE BOTH"** if f_FLAT,excl ≥ 0.80 and f_H,excl ≥ 0.50;
3. else **"MIXED"**.
Beside (printed, not gating): the same rule under the secondary convention, on the alt footing, on the 2 r_e-only subgrid (270 cells; the r_e level rests on the r_t reconstruction), and on the one-axis-at-a-time set (the committed cell plus every single-axis change, 15 cells).

**Which axis moves s★ most (frozen):** the one-axis-at-a-time range of log₁₀ s★ about the committed cell; an axis with a NO-ROOT level ranks above any finite range (it removes the root); ties by the spread across levels of the full-grid root fraction. The full-grid per-level root fraction, FLAT-excluded fraction and median rooted log₁₀ s★ are printed for every axis.

## 6. Controls that can fail
- **C1** the committed cell reproduces CFG229: log₁₀ s★ and the five MC quantiles and the no-root fraction equal `cfg229_score_results.json` to 1e-12 (bit-level replay).
- **C1b** the replayed stream reproduces CFG229's committed MC for all seven galaxies (no-root fractions and quantiles, to 1e-12).
- **C2 loader:** the eq.-8 coefficient 1.68, σ_m = 129, V_max 564, V_circ 533, σ 157, i 55 (+8/−6) parsed from the Amvrosiadis TeX; the SMG single-tracer row 7.3 / 3.8 / 16.2 parsed from Dunne's TeX; Dunne's ALESS122 rows equal the repo CSVs.
- **C3** the reconstruction: EQ8 at 2 r_e gives back 533 km/s and the arctan law with the solved r_t gives back V_rot(2 r_e), both to 1e-9.
- **C4 independent inversion:** every rooted cell's s★ equals a brentq inversion of ν_mono(y/s) = D to 1e-6 dex.
- **C5 independent g_bar path:** the Hankel-transform disc force equals the closed form at both radii to 1e-4.
- **C6 directions over the grid:** at fixed other levels, D rises P0 < C168 ≤ EQ8 < P1 (at 2 r_e; C168 = EQ8 at r_e), falls with more gas and with more stars, and rises as the inclination falls.
- **C7 bookkeeping:** for every cell exactly one of {no root, FLAT excluded above, FLAT inside, FLAT excluded below} holds, and the four fractions sum to 1.
- **C8 siblings' committed cells** reproduce CFG229's committed D to 1e-9.
- **MUTATE (`MUTATE=1`, separate outputs `*_MUTATE*`): V × 0.7 in every cell of every galaxy.** In every cell the mutated s★ must equal the independent inversion at D × 0.49 (root exactly where the inversion has one; to 1e-6 dex), and every cell that keeps a root must have a smaller s★ than in the main run. The main-run controls C1/C1b/C8 are expected to fail under MUTATE and are not run there.
- The script ends with "N/M checks pass".

## 7. Sibling check (the same grid on ALPAKA 15/18/19/20/22 and BX610, each galaxy's own record)
- (a) pressure: the same five forms with each galaxy's σ (ALPAKA: σ_ext; MSIG uses ALPAKA's σ_m, which equals σ_ext except for ALPAKA 18; BX610: σ₀, no second σ, so MSIG is omitted); the committed level is P0 for ALPAKA (V_ext not pressure-corrected) and P1 at R_e for BX610 (FS+18 Eq. 1, 3.36 σ₀²).
- (b) gas: Dunne-optimised (committed table) + each single tracer Dunne tabulates for that galaxy (CO, [CI], dust; SMG row) + α_CO 0.8 / 3.6 / 4.36 × L′_CO where L′_CO exists; BX610 also its other Dunne tables (ad, xa, xd), as CFG229 used them.
- (c) M*: committed ± the source's 1σ. (d) inclination: committed ± its error (ALPAKA i_used ± e, clipped 5–85°; BX610 from sin i = 0.86 (−0.12/+0.08)) and, for ALPAKA, the other of (i_HST, i_ALMA). (e) radius: committed, and R_e for ALPAKA 15/18/19/22 by linear interpolation of the digitised rotation curve (ALPAKA 20's R_e lies beyond its last ring and BX610 has only R_e: one level).
- Reported: per sibling, the number and fraction of cells with a root, the cells that root, the largest D; MC intervals for rooted cells (shifted CFG229 inclination draws for ALPAKA). **"Gains a root" = at least one cell with a nominal root.**
- **Common-calibration outlier test:** for each recipe shared across galaxies (pressure P0/C168/EQ8/P1 × gas G0, DU1 for all seven; CO1, A08, A36, A436 for the six with L′_CO), at each galaxy's committed M*, inclination and radius: log₁₀ D of all seven, ALESS 122.1's rank and its gap to the largest sibling; Dunne's per-galaxy optimised α_CO and κ_H printed beside.

## 8. Hand estimates (frozen; scored by code; misses kept)
- **H1** C1 reproduces CFG229 exactly (0.95).
- **H2** pressure, one axis at a time: P0 s★ ≈ 2.7 (2.2–3.3), C168 ≈ 5.4 (4.5–6.5), P1 ≈ 17.9 (15–21), MSIG ≈ 6.5 (5.5–7.5) (0.8).
- **H3** gas: A436 NO ROOT (0.75); CO1 s★ 1.0–1.6 or NO ROOT (0.7); A36 1.4–2.2 (0.7); DU1 ≈ 15.7 (13–19) (0.8); A08 ≈ 22.7 (18–28) (0.8).
- **H4** M* ± 0.21: 6.6 and 10.6 (each ± 0.3) (0.95).
- **H5** inclination 49° → ≈ 12.4 (10.5–14.5); 63° → ≈ 6.2 (5.3–7.2) (0.8).
- **H6** at r_e (committed otherwise) D lies in 0.93–1.12 and s★ < 1.5 or NO ROOT (0.7).
- **H7** the dominant axis is the gas (a NO-ROOT level and > 1 dex among rooted levels) (0.75); the radius is second (0.55).
- **H8** the decision is NOT ROBUST (0.85), with f_noroot ≥ 0.25 (0.75) and f_FLAT,in ≥ 0.25 (0.65).
- **H9** f_FLAT,excl in 0.15–0.35 (0.6); f_H,excl in 0.04–0.18 (0.6); f_noroot in 0.30–0.55 (0.65).
- **H10** the 2 r_e-only subgrid is also NOT ROBUST (0.7).
- **H11** 3 or 4 of the 6 siblings gain a root in at least one cell (0.55); ALPAKA 15 and 20 gain none (0.7); ALPAKA 18 gains one through i_used − 1σ (0.8); every sibling's rooted-cell fraction is below 0.15 (0.6).
- **H12** ALESS 122.1 has the largest D of the seven in every common recipe (0.85), with a median gap ≥ 0.3 dex to the largest sibling (0.7).
- **H13** MUTATE: the committed cell loses its root (D ≈ 0.94) (0.95); fewer than 20 % of the 540 cells keep a root (0.6).
- **H14** the secondary convention gives the same decision (0.85); under it the committed cell's 95 % lower bound on s★ lies in 1.0–1.3 (0.5).

## 9. Wording and limits (written before the run)
"Stress test of one galaxy; descriptive; the implied a₀ is not a measurement of a₀(z)." No "favours", "prefers", "disfavours" or "confirms". A NO-ROOT cell is a statement about baryons against dynamics, never about a₀. Limits: one galaxy; one thin disc for stars and gas with the CO r_e; the velocity is the authors' model output; V_rot and r_t are reconstructed from posterior summaries; σ is held fixed in the MC; the full factorial treats every declared level as equally plausible (the fractions describe the record's spread of choices, not a probability); σ_int is not in the intervals; the record's α_CO conventions carry no stated error.
