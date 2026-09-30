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

## Reconciliation with the data chat's z > 3.5 list (appended 2026-09-30; the text above is unchanged)

- **Which nine.** The "9 disks that have both" (an SED M★ and dust-based gas) are CRISTAL-02, -03, -07a, -08, -11, -12, -19, -20 and -23b: the primary set's disks with a finite SED M★, f_molgas and fitted M_bary (-09 and -15 are excluded as frozen). The data chat counts **six** with a dust *detection*: 02, 03, 07a, 11, 19, 20. **The three extra are 08, 12 and 23b, whose f_molgas are dust UPPER LIMITS** (the CRISTAL paper's own note lists 01a, 08, 12, 14, 15, 16, 23b and 23c as upper limits, dust continuum below the S/N threshold). The route used their table values as values in M_ind = M★ / (1 − f_molgas). That was wrong for those three, and this README should have said so.
- **Recomputed** (`cfg213_route_detected.py`; its control reproduces the committed n = 9 route medians exactly, max difference 0; MUTATE shifts them by log10 1.5 as it must):

| SED + gas route, α = 3.36, ν_mono, canonical | n | flat | rival |
|---|---|---|---|
| the lane's nine (three upper limits used as values) | 9 | +0.043 [−0.076, +0.377] CONSISTENT | −0.198 [−0.321, +0.107] CONSISTENT |
| the six dust detections only | 6 | +0.117 [−0.060, +0.384] CONSISTENT | −0.144 [−0.319, +0.141] CONSISTENT |
| fit route (the authors' M_bary), the same six | 6 | +0.028 [−0.013, +0.165] CONSISTENT | −0.171 [−0.279, −0.073] DISFAVOURED-under |

  - Both laws are CONSISTENT in all four kernel/footing cells of the detections-only route. On the same six discs the fit route keeps the rival DISFAVOURED-under in all four cells (the flat law is CONSISTENT; P2 canonical is borderline at +0.039 [+0.000, +0.209]). So the route dependence in the bottom line stands on the detections alone, on n = 6 with wide intervals; it is not a separation.
  - **The three upper limits, as one-sided bounds.** An upper limit on the gas is a LOWER bound on δ here, because D = g_obs / g_bar also falls as g_bar rises. CRISTAL-08: δ_flat ≥ +0.377, δ_rival ≥ +0.088; -12: ≥ +0.043, ≥ −0.269; -23b: ≥ −0.437, ≥ −0.536 (ν_mono, canonical). The route factor of 6.09 quoted for CRISTAL-23b in the post hoc block belongs to an upper-limit disc, so it is itself a bound.
- **For any later use of this sample** (CFG219 and the data chat's class A/B split): CRISTAL discs enter as class A only with a dust detection (02, 03, 07a, 11, 19, 20); 08, 12, 15 and 23b enter as one-sided limits, never as values.

## Referee corrections (CFG234, 8222db057; appended 2026-09-30; the text above is unchanged)

CFG234 re-derived this lane independently and reproduces all 96 of its cells (class labels 96 of 96, medians to 1e-9). Its findings on the lane's own text and controls, each checked here against the files:

- **"7 of 10 lie within 0.1 dex" is wrong: it is 6 of 10, and the −0.32 outlier is G4_24078, not G4_20371.** Recomputed directly from `data_assembly/noema3d/noema3d_per_galaxy.csv` (log(M★ + M_gas,CO) − log M_bary,dyn): within 0.1 dex are G4_38065 +0.005, G4_38232 +0.084, G4_20371 +0.018, GN4_24517 +0.078, G4_17555 −0.036 and G4_37375 −0.033; outside are G4_23011 +0.167, GN4_32842 +0.135, **GN4_18574 +0.406** and **G4_24078 −0.317**. The count was copied from the data chat's note into this README (the line "This reproduces the data chat's note: 7 of 10 lie within 0.1 dex") and the outlier's name into `FROZEN_CRITERIA.md` (which names G4_20371, whose offset is +0.018). Neither is used by any number in the lane; the statement that the fitted and SED + CO masses "agree here" stands with the count corrected.
- **C2 is vacuous.** It sets `Dexact = nu1(nu, gb / a0)` and compares it with `nu1(nu, gb / a0)`, i.e. log₁₀(x/x) = 0 by construction (the same construction as CFG216's and CFG217's C1). A non-vacuous replacement, `cfg213_c2_nonvacuous.py`: 400 synthetic galaxies (2 bins × 2 kernels × 2 footings × 2 laws × 5 z × 5 g_bar/a₀) placed exactly on a law through the lane's own input fields (f_DM = 1 − 1/ν, then V_rot or V_c solved from g_bar = (1 − f_DM) V_c,ad²/R_e) and scored by the lane's own `galaxy_rows()` and `deltas()`. Every on-law row returns |δ| ≤ 2.9e-16; scored under the other law, 100% exceed 1e-3; and with the lane's MUTATE injection the control fails as it must (max |δ| 0.176). Outputs `cfg213_c2_nonvacuous.out` and `..._MUTATE.out`. No number in the lane changes.
- **C3 (the vector at R_e against the table) is `load_bearing=False` with a hard-coded True;** it is a reported check and never gated a verdict. **The lane's MUTATE (every D × 1.5)** shifts every median by log₁₀ 1.5 by construction: it verifies that the injected shift propagates through the pipeline, not any significance statement (the same is true of the MUTATE controls of CFG216, CFG217 and CFG220).
