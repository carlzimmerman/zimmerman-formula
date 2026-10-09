# CFG505 — FROZEN CRITERIA: GALEX UV for the KiDS isolated lenses, rebuilt stellar masses, and the M\*-dependent lensing tests re-scored

**Committed alone, after the GALEX cross-match returned (match statistics only: `cfg505_fetch.*`, `cfg505_match.*`) and before any mass set is built or any lensing quantity is re-scored with it.**

> κ = ½ is FITTED. Both footings (9.3603e-11 and 1.1312e-10) are scored separately and never pooled. a₀ flat. The cold energy's mass is still required; no particle species is added. Nothing here will say the data favour the framework, and nothing says "theory closed".

## 0. What is known before this freeze (disclosure)

- **Owner go (2026-10-08, in chat):** a GALEX positional cross-match of the stack-P lenses, uploading RA/Dec only, via CDS XMatch. Done (`FETCH_LOG.md` in the data dir): GUVcat_AIS (`vizier:II/335/galex_ais`; the approval's "gal_ais" is this table) and GR5 MIS (`vizier:II/312/mis`), 3" radius, 53,296 and 22,940 match rows. Nothing else was fetched.
- **Match statistics (`cfg505_match.out`):** 34.6% of the 181,477 lenses are detected in NUV (MIS used for 22,598); 55.1% are covered non-detections; 10.4% have no coverage. Late class: 57.7% detected; early class: 10.1%. Detections are faint (AIS median NUV 21.9, e 0.32; MIS 22.2, e 0.19). 5σ NUV limits: AIS 21.5, MIS 22.4. Rest-frame NUV − r of detections: late median 2.62, early 3.69; non-detection limits are shallow (median > 2.2 / > 2.7), so **no lens can be shown UV-quiescent (≥ 5) except a handful**. 6.9% of the early class are UV star-forming (detected, NUV − r < 4). FUV and NUV both with e ≤ 0.25: 8,009 late, 538 early. Chance-match rate about 1.6% (AIS) / 0.1% (MIS) of matches. The per-lens total-vs-GAaP r flux scale has median +0.170 dex (the record uses a constant +0.15). Spearman ρ(NUV − r, u − r) over detections = +0.80.
- **Record numbers this lane will move (read before the freeze):** CFG88 / CFG95-MUTATE re-measured early/late split, law at s = 1, K1 (bins 8–14), jackknife covariance: χ² **35.03/7** (canonical), 35.03/7 (alt). CFG95 (own dynamical calibration) 26.7 / 24.8; the uniform differential that the re-measured split wants for p > 0.05 is ≥ 0.225 dex (best ≈ 0.45). CFG261 implied-a₀ scale s\* (K1, Mg weights): late-LO 1.67, late-HI 0.68, early-LO 2.48, early-HI 4.12 (jackknife SD of log s\* 0.105 / 0.180 / 0.053 / 0.044). CFG503: stack-P LCDM + E fails its gate at 1.0–1.4 Mpc.
- **No SPS code or SPS template library is on disk** (no FSPS/BC03/CIGALE/LePhare install), and no download beyond the GALEX match is approved. So the SED method is a published colour–M/L relation (Bell et al. 2003, Table 7, transcribed from the copy on disk, `deepseek_push/G114_data/bell2003b/lf.tex`), with the UV entering through a published UV dust law. **Expected in advance (hand estimate, written now):** Calzetti dust moves a galaxy almost along the g − i / M/L_i relation, so the UV dust correction changes M\* by only about +0.015 × A_FUV dex; the UV is unlikely to move M\* by more than a few hundredths of a dex on average. The larger lever is the method change (Bell+03 vs LePhare). The UV's second lever is the class: 6.9% of the early class are UV star-forming.

## 1. Lens sample
Stack P exactly as CFG377 / CFG413 / CFG502 / CFG503: `lr_lenses.npz` (181,477; typ 0 late / 1 early = rest-frame u − r > 2.0), joined to the KiDS bright sample row by exact coordinates. Patches: `lr_esd_jackknife.npz` (50).

## 2. Mass sets (each lens; M_gal = M\* (1 + f_cold(log M\*)), f_cold = 10^(−0.69 log M\* + 6.63), the record's relation evaluated at the new M\*)
- **M0 (baseline):** LePhare MASS_MED + 0.15 dex (the record's lr_lenses logM).
- **M1 (primary method change, optical colour M/L):** log M\* = −0.152 + 0.518 (g − i) − 0.15 + 0.4 (4.53 − M_i) + 0.15, with g, i = LePhare rest-frame MAG_ABS (GAaP), Bell+03 a_i, b_i for g − i, −0.15 dex the Bell+03 note's diet-Salpeter → Kroupa/Chabrier-like shift, M_sun,i = 4.53 (AB), +0.15 the record's constant fluxscale.
- **M1b (reported):** u − r → M/L_K (a −0.273, b 0.091), M_K,Vega = M_Ks,AB − 1.85, M_sun,K = 3.28. **M1c (reported):** g − r → M/L_r (a −0.306, b 1.097), M_sun,r = 4.65. Same −0.15 and +0.15.
- **M2 (primary UV mass):** M1 with the UV dust correction where the UV measures it: lenses with FUV and NUV both detected with e ≤ 0.25 (same survey record): β = (FUV₀ − NUV₀)/0.4303 − 2 (λ 1528 / 2271 Å; Galactic A_FUV = 8.06, A_NUV = 7.95 E(B − V)); A_FUV = clip(4.43 + 1.99 β, 0, 5) (Meurer+99); E_s = A_FUV / k(0.16 µm), A_g = k(0.477) E_s, A_i = k(0.7625) E_s with the Calzetti (2000) curve (R_V = 4.05); then (g − i)₀ = (g − i) − (A_g − A_i), M_i,0 = M_i − A_i in the M1 formula. All other lenses (low-S/N detections, non-detections, no coverage): A_FUV = 0, i.e. M2 = M1. **Non-detections are not dropped:** they keep M1 and enter every stack.
- **M2i (reported, selection-bias bracket):** as M2, but every covered lens without a measured β (low-S/N detections and covered non-detections) receives its class's median A_FUV of the β-measured lenses (an upper bracket: those are UV-bright).
- **M2_MUT (MUTATE):** the whole per-lens UV record (FUV, NUV, errors, E(B − V), detection and coverage flags) permuted across lenses with a fixed seed (5050), then M2's recipe.

## 3. Data re-staged
`cfg505_stage.py`: CFG110's per-lens estimator verbatim, one pass, the pairs of every lens binned in g_bar = G M_gal / R² for every mass set (M0, M1, M1b, M1c, M2, M2i, M2_MUT). Per-lens sums to the data dir.

## 4. Tests (`cfg505_score.py`), the record's machinery read-only
Model = the L law stack of CFG61 / CFG261 (cell tables of the law, truncation 0.40 r_ta, point baryons, Mg weights; CFG261's cached tables on the 10-node log s grid), with each lens assigned to its cell by the NEW log M\* and weighted by the NEW M_gal.
- **T1, early/late split (headline):** D = ESD_early − ESD_late on K1 (bins 8–14) from the re-staged sums, 50-patch jackknife covariance × Hartlap 41/49; χ²_L of D against the law difference at s = 1 per footing (alt via the canonical tables at log s = log10(1.1312/0.93603) on CFG261's spline). Significance σ_split = two-sided normal equivalent of p(χ², 7).
- **T2, implied a₀ level:** CFG261's estimator (diagonal jackknife weights, fine-grid least squares in log s on K1, jackknife SD of log s\*) for the rows T-late-LO, T-late-HI, T-early-LO, T-early-HI (CFG261's class z-thirds, unchanged by mass), late (all z), early (all z) and ALL. Implied a₀ = s\* × 9.3603e-11; κ_implied = ½ s\* (canonical) and ½ s\* × 0.93603/1.1312 (alt).
- **Reported (no verdict):** (R1) the uniform early-class differential that the split wants (the early lenses' true mass shifted by Δ = 0…0.5 dex in steps of 0.05 in the model, CFG261's `build_cells(shift=Δ)`), per mass set: the Δ range with p > 0.05 and the best Δ; (R2) the UV-class split S-UV: M2 masses, UV star-forming early lenses (detected, NUV − r < 4) moved to the late class; (R3) the CFG503 environment term E (nlz, W10, Moster; restacked per mass set with the new log M\* and M_gal, WW pair weights) added to every class model: split χ² on K1 and on the inner 9 bins (R ≤ 0.445 Mpc = 0.3/h), and the ALL-lens stack χ² (law + E, s = 1, both footings) on the inner 9 and the outer 6 bins, **outer bins reported separately and never in a verdict** (CFG503's LCDM validation fails at 1–1.4 Mpc); (R4) M1b, M1c, M2i through T1 and T2; (R5) the pair-weighted median R per bin per mass set (K1 must stay within 0.3/h Mpc).
- **Mass comparison (reported, before the lensing):** log M\*(set) − log M\*(M0): median offset, robust scatter (1.4826 MAD), slope against u − r, by class, by UV status (β-measured / other detected / covered non-detection / no coverage), and by z third.

## 5. Verdict rules (frozen)
- **V1 (headline, split):** Δσ = σ_split(M2) − σ_split(M0) per footing. **MATERIAL** if |Δσ| ≥ 1.0 on both footings; **PARTIAL** if on one; **NOT MATERIAL** otherwise. The same rule, reported, for the UV-only change σ(M2) − σ(M1) and the method change σ(M1) − σ(M0). **SPLIT CLOSED** if p > 0.01 on both footings with M2; otherwise the split stands.
- **V2 (a₀ level):** per T row and the class rows, Δ log s\* = log s\*(M2) − log s\*(M0); **MATERIAL** if |Δ log s\*| ≥ max(the row's jackknife SD, 0.05 dex). The same, reported, for the UV-only change (M2 vs M1). The early rows' "need" (CFG261: +0.36 / +0.57 dex) is compared with the early-class mean M2 − M0 shift.
- Nothing is pooled across footings; κ stays fitted whatever V2 says (a level is a baryon census times the law, not a measurement of a₀).

## 6. Controls (load-bearing)
- **C1:** the re-staged M0 sums equal `cfg110_perlens.npz` exactly (max |Δ| ≤ 1e-12 relative per non-empty cell).
- **C2:** T1 with M0 reproduces CFG95-MUTATE's re-measured 35.025/7 (canonical) within 0.01, and 35.026 (alt) within 0.05 (alt goes through the spline).
- **C3:** T2 with M0 reproduces CFG261's s\* for the four T rows within 0.005 dex.
- **C4:** M2 with A_FUV ≡ 0 equals M1 exactly; the Bell+03 coefficients printed match the table on disk.
- **C5:** every match row joins one lens (< 1e-6 deg) — passed in `cfg505_match.py` by assertion.

## 7. MUTATE (shuffled UV, `CFG505_MUTATE=1`, separate outputs)
- **MU1:** the shuffle destroys the UV–optical link: |ρ(NUV − r, u − r)| over detections < 0.05 (real +0.80).
- **MU2:** the UV-driven change disappears: for M2_MUT vs M1, |Δσ_split| < 0.3 on both footings and |Δ log s\*| < 0.02 in every T row; and the class structure of the UV correction disappears (the early-minus-late difference of the mean M2_MUT − M1 shift is within 0.005 dex of zero, against the real M2 − M1 value).
- **Pre-declared:** if the real UV-only change (M2 vs M1) is itself below the MU2 thresholds, the MUTATE cannot distinguish it, and it is then uninformative for the headline (as CFG95's); MU1 and C1–C4 remain the machinery checks.

## 8. Limits stated now
No SPS fit (the UV leverage measured here is through the dust law and the class only; an SPS fit with UV could move ages/bursts more). Bell+03 relations are z ≈ 0 SDSS calibrations applied to LePhare rest-frame magnitudes (themselves template K-corrections). β at z 0.1–0.5 samples rest 1090–2060 Å. Meurer's law is a starburst calibration (normal discs lie below it: M2's A_FUV is an upper side). Gas stays on the record's mass-only relation (no sizes on disk for a UV gas estimator). No E in T1/T2 (as CFG95/CFG261); E enters only R3.
