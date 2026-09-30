# CFG213 — a two-sided a₀ test on DysmalPy disc–halo decompositions: NOEMA3D (z ≈ 1.4) and ALMA-CRISTAL (z ≈ 5)

- **Criteria:** `FROZEN_CRITERIA.md` (03da24231), committed before any number. **κ = ½ FITTED, NOT DERIVED.**
- **Run:** `python3 campaign_fresh_gravity/CFG213_dysmalpy_two_sided/cfg213_two_sided.py`, about 1 s. The main run passes 3/3 checks. `MUTATE=1` (every D × 1.5) passes 4/4: every median δ rises by exactly log₁₀1.5.
- **Post hoc:** `cfg213_posthoc.py` → `cfg213_posthoc.out`, written after the numbers were seen. It is reported only and never a verdict.
- **What is tested.** D = g_obs/g_bar at R_e,disk, taken from the authors' own fits (1/(1 − f_DM)), against ν(g_bar/a₀(z)):
  - flat a₀;
  - the rival a₀ × E(z), about ×2.2 at z ≈ 1.4 and about ×8 at z ≈ 5.
  - The δ reported below is log₁₀(D_obs/D_pred).

## Bottom line

- **z ≈ 5 (ALMA-CRISTAL, 12 disks; CRISTAL-09 and -15 excluded as frozen).**
  - **On the fits' own baryonic masses, the rival is robustly DISFAVOURED-under: it predicts MORE mass discrepancy than the decompositions show.**
    - ν_mono median δ: −0.161 [−0.207, −0.055] canonical and −0.186 alt at the adopted pressure term (α = 3.36).
    - It is −0.27 to −0.30 at the moderate term (α = 1.68).
    - P2 gives −0.11 to −0.25.
    - Every kernel, footing and α cell agrees.
  - **The bare flat law is NOT robust.**
    - It slightly UNDER-predicts at α = 3.36: DISFAVOURED-over in 3 of 4 kernel/footing cells, median +0.04 to +0.08.
    - It is CONSISTENT at α = 1.68.
  - **Under the frozen rule that is a separation (only the rival is robustly disfavoured), labelled ROUTE-DEPENDENT.**
    - With SED M★ plus dust-based gas in place of the fitted M_bary, for the 9 disks that have both, both laws are CONSISTENT.
    - The rival's median is −0.15 to −0.22, but its CI widens to include 0.
- **z ≈ 1.4 (NOEMA3D, 10 galaxies, measured CO gas).**
  - **Both laws are CONSISTENT in every cell, on both mass routes.** No separation.
  - Flat: +0.03 [−0.03, +0.23]. Rival: −0.00 [−0.09, +0.12] (ν_mono, canonical).
  - The fitted and SED + CO masses agree here. This reproduces the data chat's note: 7 of 10 lie within 0.1 dex.

## Post hoc: what drives the route dependence (reported only)

- **(a) Same 9 galaxies, both routes.** On the fit route, the rival stays DISFAVOURED-under in 3 of 4 cells (P2 canonical: −0.107 [−0.220, +0.011]). So cutting the sample from 12 to 9 weakens it only slightly.
- **The swap mostly widens the scatter.** The route factor M_ind/M_fit runs from 0.34 (CRISTAL-19) to **6.09 (CRISTAL-23b)**. The fit gives 23b log M_bary 9.8, against 10.58 from SED + gas. The rival's median becomes MORE negative on the SED + gas route (−0.198 vs −0.155), but noisier.
- **(b) Leave-one-out** (fit route, n = 12 → 11):
  - rival median −0.167 to −0.155;
  - flat median +0.033 to +0.073.
  - No single galaxy carries either.
- **(c) Per-galaxy route factors:**
  - 02: 1.11; 03: 1.15; 07a: 1.11; 20: 1.22; 12: 1.21;
  - 08: 0.61; 11: 0.45; 19: 0.34;
  - 23b: 6.09.

## Also reported

- **CRISTAL at the vector model's outer radii** (the table's R_out, and the outermost data marker; the curves beyond the last marker are extrapolation): the rival is DISFAVOURED-under (−0.28 and −0.26), and flat is CONSISTENT (+0.02 and +0.02).
- **Best-Disk subset (n = 6):** flat DISFAVOURED-over (+0.053 [+0.018, +0.255]); rival CONSISTENT (−0.118 [−0.229, +0.058]).
- **The two excluded disks:**
  - 09: D_obs 1.09, against flat 1.05 and rival 1.42.
  - 15: D_obs 1.21, against flat 1.08 and rival 1.55.
- **Without any pressure term (α = 0, reported only),** both laws over-predict, i.e. are DISFAVOURED-under.
- **C3.** At R_e the vector read matches the table: D ratio median 1.010 [0.93, 1.05]; V_circ ratio 0.997.

## Limitations: read before quoting

- **CRISTAL's M_bary has a Gaussian prior 1 dex wide, fitted jointly with the halo.** This is the MUSE-DARK III situation (CFG198/199). The fit route is the authors' decomposition, and the independent route loses significance through the scatter of the dust-based gas masses (T_d = 50 K single-band).
- **f_DM(R_e) is fitted with a flat prior on [0, 1],** from 1.6 to 5.5 beams at R_out. The statistic uses MAP values without the per-galaxy posterior widths, so the bootstrap over galaxies carries the scatter but not each fit's own uncertainty.
- **The pressure term matters.** The flat law's verdict flips between α = 3.36 and 1.68. The authors adopt 3.36 and note that moderate terms (Dalcanton–Stilp, Kretschmer) are also in use.
- **Scope.** Nothing here says the data favour the framework. The bare flat law is not robustly consistent at z ≈ 5 either, and B's cold component is not modelled.
