# EUC1 (ECLIPSE SATURATION CEILING): RESULT

2026-11-12. Criteria 898cefb457 (committed alone, before any script or number).

## Verdict: NO VERDICT / NO VERDICT (canonical / alt)

With every source placed at infinity, 15.6 % [14.3, 16.8] (canonical) and 13.9 % [12.7, 15.1] (alt) of Euclid's 3,192
grade-A, successfully modelled strong lenses need more than 1.78 × their catalogued Salpeter stellar mass for law S to
make them. That is above the 10 % contamination floor and below the 25 % line, so the frozen word is NO VERDICT on both
footings. No robustness run moves the word. All instrument checks pass. The mutation twin exits 1.

The test is one-sided. This is not a pass of the lensing gate and not a kill. It says where Euclid's lenses sit: **at
the ceiling.** The median lens needs exactly the law's full supply when its source is infinitely far away
(`b_med` = −0.019 canonical, −0.044 alt), and more than the law can give for any realistic source.

κ = ½ FITTED. Footings never pooled. No outcome here favours the framework.

## 1. The numbers (sample P, N = 3,192, source at infinity)

`b` = log₁₀ of the factor by which the catalogued Salpeter stellar mass must be multiplied. It is a lower bound on the
true requirement. `f₂₅` = fraction with b > 0.25 dex.

| Law, footing | f₂₅ [95 %] | f₀ [95 %] | b_med [95 %] | Word |
|---|---|---|---|---|
| S, canonical | 0.156 [0.143, 0.168] | 0.472 [0.455, 0.489] | −0.019 [−0.030, −0.009] | NO VERDICT |
| S, alt | 0.139 [0.127, 0.151] | 0.436 [0.419, 0.453] | −0.044 [−0.055, −0.033] | NO VERDICT |
| B, canonical | 0.200 [0.187, 0.214] | 0.556 [0.539, 0.572] | +0.033 [+0.023, +0.044] | NO VERDICT |
| B, alt | 0.183 [0.171, 0.198] | 0.524 [0.507, 0.541] | +0.015 [+0.004, +0.025] | NO VERDICT |

Sample medians: z_l = 0.660, θ_E = 0.897″, θ_e = 0.878″, n = 5.34, log M★ = 11.42, R_E = 6.22 kpc, R_e = 5.93 kpc.
Σ_cr,∞ = 1,363 M☉ pc⁻²; stars inside R_E = 1,056 M☉ pc⁻²; the law's cold pull inside R_E = 445 (canonical) / 510 (alt)
M☉ pc⁻², about a third of what the lens needs.

10 of the 3,202 rows of the base cut were removed for inputs outside the frozen ranges, before any statistic.

## 2. Instrument checks (all pass)

| Check | Result |
|---|---|
| K1 point mass / SIS | 1.3e-11 / 7.6e-6 |
| K2 A55 on SLACS, median R_E,pred/R_E,obs | 0.8852 (target 0.885 ± 0.005) |
| K3 A70 on SLACS, boost taking the median to 1 | 1.1738 (target 1.174 ± 0.02) |
| K4 twin projection, 20 lenses | max 3.3e-6 |
| K6 H₀ → 70 | b_med moves +0.0189, predicted +0.0186 |
| MUTATE newton (a₀ → 0) | f₂₅ 0.156 → 0.332 and 0.139 → 0.332; exit 1 |

**K5, the cost of having no source redshift (SLACS, law S).** At the true source redshifts SLACS needs
`b_med` = +0.082 (canonical) / +0.070 (alt). With the sources moved to infinity the same lenses read −0.144 / −0.163.
Dropping the source redshift hides 0.20 dex. On the same source-free footing Euclid's lenses read −0.019 / −0.044:
**0.12 dex higher than SLACS.**

**Deviation from the criteria, disclosed.** §3 expected Σ_cr at z_s = 1100 to be within 1 % of its limit. Over P the
largest difference from z_s = 10⁵ is 1.8 %. The frozen choice (z_s = 1100) was kept. It makes the lower bound at most
0.01 dex too high in b for the highest-redshift lenses, far inside every threshold.

## 3. Conditional readings (never the verdict)

| Reading | f₂₅, law S canonical | f₂₅, law S alt | b_med canonical / alt | Would-be word |
|---|---|---|---|---|
| R3: every source at z_s = 3 | 0.320 [0.305, 0.336] | 0.296 [0.281, 0.312] | +0.146 / +0.125 | CEILING BROKEN |
| R2: every source at z_s = max(2, z_l + 0.5) | 0.466 [0.450, 0.483] | 0.435 [0.418, 0.452] | +0.232 / +0.213 | CEILING BROKEN |

If Euclid's sources lie where lensed sources usually do, the median lens needs 1.3–1.7 × Salpeter, against 1.17 ×
for SLACS at its measured source redshifts. The ECLIPSE paper reports DESI-vetted source redshifts between 0.3 and 2.7.
These readings are conditional on the source distribution and are not the verdict.

## 4. Robustness (law S, source at infinity; f₂₅ canonical / alt)

| Run | f₂₅ | Word |
|---|---|---|
| 1 R_e × 0.80 | 0.126 / 0.107 | NO VERDICT |
| 2 n = 4 for all | 0.188 / 0.169 | NO VERDICT |
| 3 SIE Einstein radius | 0.167 / 0.147 | NO VERDICT |
| 4a z_l < 1.0 (N = 2,747) | 0.163 / 0.145 | NO VERDICT |
| 4b the 39 DESI-redshift deflectors, at spec-z | 0.179 / 0.154 | NO VERDICT (N = 39) |
| 5 θ_E ≤ 2.5″ | 0.151 / 0.134 | NO VERDICT |
| 7 sample S, grades A+B (N = 6,173) | 0.164 / 0.145 | NO VERDICT |
| 8 r_max = 300 kpc | 0.160 / 0.145 | NO VERDICT |
| 6 Monte Carlo of the catalogued errors, 200 draws | mean 0.198 / 0.178, sd 0.005 / 0.004 | (spread only) |

Run 1 alt is the closest to a threshold: its upper bound is 0.118, against the 0.10 line for HOLDS.

## 5. Map (exploratory; no verdict)

Law S, source at infinity. `ΔΣ_min` is the smallest extra mean surface density the lens needs inside R_E beyond the
law's supply (alt footing); negative means the law has room.

| Split | Where the excess sits |
|---|---|
| θ_E | f₂₅ rises from 0.03 (< 0.6″) to 0.31 (1.3–1.7″), 0.62 (1.7–2.5″), 0.90 (> 2.5″, N = 20). ΔΣ_min rises from −741 to +369, +604, +895 M☉ pc⁻². |
| θ_E/θ_e | f₂₅ = 0.34 below 0.5 (N = 562), 0.06 between 1.5 and 5. |
| Sérsic n | f₂₅ = 0.05 for n < 4, 0.18 for 6–8, 0.32 for 8–10. |
| z_l | b_med falls from +0.11 (z_l < 0.3) to −0.17 (z_l > 1.2). Expected from geometry: a source at fixed redshift costs more at higher z_l. |
| log M★ | Lowest at 11.2–11.6 (b_med ≈ −0.07 to −0.09 alt). Rises to +0.41 below 10.6 (N = 21) and +0.15 above 12.0 (N = 11). |
| SP1's switch, log M★ = 11.21 | Median b is 0.07 dex *lower* above the switch than below. No step up. SP1 is a weak-lensing prediction of a retired sector and is not graded here. |
| Disc deflectors (N = 228) | b_med = −0.154 (alt), against −0.034 for the rest. |

The excess is concentrated in wide-separation lenses, in lenses whose light is far more extended than their Einstein
radius, and in very high Sérsic index fits. All three mark group-scale or brightest-group galaxies. It does not appear
as a step in stellar mass.

## 6. Post hoc readings (after the frozen run was seen; `euc1_posthoc.py`; not the verdict)

**A1, the break redshift.** Placing every source at one redshift z_s, the lower 95 % bound of f₂₅ reaches 0.25 at
**z_s\* = 4.34 (canonical) and 3.58 (alt)**. If Euclid's lensed sources typically lie below z ≈ 3.6–4.3, the ceiling
breaks. f₂₅ at z_s = 2 / 2.5 / 3 / 4 / 6 / 10: canonical 0.47 / 0.37 / 0.32 / 0.28 / 0.23 / 0.20;
alt 0.44 / 0.35 / 0.30 / 0.25 / 0.20 / 0.18.

**A2, noise.** Adding the catalogued errors a second time raises f₂₅ from 0.156 to 0.198 (canonical) and 0.139 to
0.178 (alt). To first order the noise-free value at infinity is 0.115 / 0.099: at the contamination floor. With the
source at infinity the sample does not break the ceiling; the question is entirely the source redshifts.

**A3, discs against the rest.** 228 disc deflectors matched one-to-one in (log M★, z_l) to other lenses: the others
need **+0.120 [+0.069, +0.158] dex** more boost than the discs (both footings). This has the sign and size of QX26's
early-type step in weak lensing (+0.158 ± 0.064 dex). The catalogue applies one Salpeter IMF to both classes. An IMF
difference of 0.12 dex between discs and spheroids, half the usual Chabrier–Salpeter gap, absorbs it. So it is the same
unresolved early-type excess seen through a second probe, and it is degenerate with the IMF in exactly the way A70
found.

## 7. What this means for the framework

1. **Nothing here confirms a registered prediction, and nothing here kills the law.** The strict test has no verdict
   because the catalogue has no source redshifts and infinity is a very generous place to put a source (0.20 dex of
   slack on SLACS).
2. **The law's saturating cold pull does real work in these lenses.** It supplies 445–510 M☉ pc⁻² inside R_E, a third
   of the lensing mass. Switch it off and a third of the lenses break the ceiling even at infinite source distance
   (the mutation twin). The cold pull is the right order of magnitude; it is short in amplitude.
3. **The shortfall is the two already on the books, not a new one.** (a) Amplitude: A55/A70's "needs more than
   Salpeter", which Euclid raises from 1.17 × (SLACS) to 1.3–1.7 × conditional on sources at z_s = 3–2. (b) The
   group-scale residual: the excess grows with Einstein radius and sits in extended, high-n, wide-separation systems.
   There is no step at SP1's switch mass and no excess in discs.
4. **Euclid's lenses read 0.12 dex above SLACS on the same source-free footing, and need more than SLACS at true
   source redshifts unless their sources typically lie beyond z ≈ 5.** The two samples lose different amounts when the
   source is dropped: SLACS 0.20 dex (measured), Euclid 0.25 dex if its sources sit near z_s = 2 and 0.09 dex at
   z_s = 6 (A1). Euclid's median reaches SLACS's +0.082 / +0.070 only at a common z_s ≈ 5.3 / 4.8. In a theory where
   lensing mass is a function of the baryons alone, a selection that prefers large Einstein radii cannot raise the
   lensing mass at fixed stars. Only three things can: a different stellar-mass scale between the two catalogues,
   selection on stellar-mass errors, or baryons outside the lens galaxy (group gas and neighbours). Prospector masses
   run high, not low, so the first works against the law. This is the sharpest thing the release says about the law
   today, and it is an argument conditional on the sources, not a measured gate.
5. **What any extra cold component would have to look like here.** If the group-scale lenses are real and their
   sources are not at extreme redshift, the gravitating density beyond the law's equilibrium must add at least
   +370 to +900 M☉ pc⁻² of mean surface density inside 10–20 kpc for θ_E > 1.3″, rising with aperture, and nothing for
   θ_E < 1″. That is a centrally concentrated, group-hosted component, not a per-galaxy halo keyed to stellar mass.

## 8. Prospective gate EUC1-F (frozen here; before any row-level ECLIPSE source redshift is public)

Written after EUC1's numbers and before any per-lens source redshift for this catalogue exists in public (Storfer et
al. is in preparation; 4MOST 4SLSLS follows). When row-level source redshifts are released for lenses in sample P:

- statistic: `b_med` at the true source redshifts, law S, per footing, 95 % bootstrap interval, N ≥ 10 required;
- **LENS GATE HOLDS** if the upper bound ≤ 0.15 (the law makes Euclid's lenses with at most 1.41 × Salpeter);
- **LENS GATE FAILS** if the lower bound ≥ 0.25;
- otherwise NO VERDICT.

Reference points on the record: SLACS reads +0.082 / +0.070; EUC1's conditional readings read +0.146 / +0.125 (z_s = 3)
and +0.232 / +0.213 (z_s ≈ 2). The same script computes it: pass the source redshift in place of `ZS_INF`.

## 9. Other registered predictions against DR1-Foundation (status only; nothing regraded here)

| Prediction | Where | Status against the November release |
|---|---|---|
| SP1 / SP2 sealed lensing steps | `rebuild_2026_10_22/SP1_*`, `SP2_*` | Need calibrated shear (June 2027). The seals' inequality direction conflict stands unrepaired. |
| PR-F4 lens-redshift split | `closure_2026_11_11/FINAL4_growth_history` | Needs calibrated shear. |
| GATE1 / A-7 isolated-lens RAR to 1 Mpc | `predictions_2026/PREDICTIONS_LEDGER_2026-09-02.md` | Needs calibrated shear. |
| η = Φ/Ψ = 1 | TC2-01 / P2; G041 | Needs shear and clustering. |
| D2 cluster kink | `prep_2026/cluster_kink_spec` | Retired (signal identically zero). |
| Saturated deflection α∞ = 2π√(GMa₀)/c² | `real_research/MASTER_PREDICTIONS.md` | This lane is its finite-radius, projected form. NO VERDICT. |
| Morphology-blind lensing excess | CFG668/669, QX26 | A3 above: the early-type step reappears in strong lensing at +0.120 dex, IMF-degenerate. |
| G118 close-pair excess | `deepseek_push/G118_merger_registry.md` | Gradeable with Euclid photo-z pairs and a ΛCDM mock control. Not run. |
| a₀(z) flat below z = 3 | SWEEP3 S3-20 | Not gradeable: needs source redshifts or kinematics. |
| Dwarf / ultra-faint predictions | PREDICTIONS_100 #53, #63–66; CRACK-1 | Euclid's 15 resolved systems carry no velocities. Not gradeable. |
| High-z abundance | C-3, S3-R7 | The repo registers none ("structurally silent"). |

No registered prediction has been confirmed by DR1-Foundation, and none has been newly falsified by it.

## 10. Files

`euc1.py` (frozen run), `euc1.out`, `euc1_results.json`, `euc1_per_lens.csv` (3,192 lenses),
`euc1_MUTATE_newton.out` / `_results.json` (exit 1), `euc1_posthoc.py`, `euc1_posthoc.out`, `euc1_posthoc_results.json`.

Commits (local / origin): criteria 898cefb457 / dcc8e51300; artifacts 5926a21305 / 2fb58b62e3; result 3ed302a34c /
a1f5178885.

Data are not in the repository: ECLIPSE archive, DOI 10.5281/zenodo.19654904; the two CSV files are hash-checked by the
script on every run.

    python3 -I euc1.py --data-dir <dir with eclipse_dr1_catalogue_key_v20261103.csv and ECLIPSE_object_catalogue.csv>

## 9. Dated note (2026-11-12, evening): the SLACS reference numbers are on a different mass convention

Found by lane EUC12 (`../EUC12_common_mass_scale/`, another session) and checked here through this lane's own code
(`euc1_slacs_convention.py`, `.out`). **No frozen threshold changes; EUC1's word and EUC1-F's lines (0.15, 0.25) are
untouched** (they came from stellar-mass systematics, not from SLACS).

- **The two conventions.** Every SLACS number above takes a SLACS stellar mass as Auger's Salpeter fraction inside the
  Einstein radius × the Einstein mass ÷ the n = 4 light fraction inside R_E (convention F). Euclid's lenses are graded
  with the catalogue's total stellar mass. The like-for-like SLACS mass is Auger's total Salpeter mass (convention T).
  F is a median 0.0375 dex above T; the size and sign follow the radius used in the light fraction (with the I-band
  radius instead of the V-band one, F is 0.049 dex below T).
- **SLACS under law S, both conventions** (canonical / alt):

| | F (as written above) | T (like Euclid's) |
|---|---|---|
| Lensing b at the true source redshifts | +0.082 / +0.070 | **+0.121 [+0.082, +0.159] / +0.109 [+0.071, +0.144]** |
| Lensing b with the source at infinity | −0.144 / −0.163 | −0.108 / −0.129 |
| Dynamics b (published dispersions) | +0.091 / +0.085 | +0.132 / +0.123 |

- **What moves in this file.** "Euclid's lenses read 0.12 dex above SLACS on the same source-free footing" becomes
  0.09 dex. "Euclid's median reaches SLACS's only at a common z_s ≈ 5.3 / 4.8" becomes z_s ≈ 3.6 / 3.4. The reference
  point "SLACS reads +0.082 / +0.070" in §8 should be read as +0.121 / +0.109 when it is set beside a Euclid number.
- **What it means.** On one convention SLACS needs about 1.3 × Salpeter under law S, not 1.2 ×, and Euclid's lenses
  sit closer to SLACS than this file said. SLACS's own interval now straddles EUC1-F's 0.15 line on the canonical
  footing (upper bound +0.159) and stays under it on the alt footing (+0.144).
- **Not checked.** Which radius Auger's fraction was computed with; the T numbers have no independent re-grade beyond
  EUC12's.
