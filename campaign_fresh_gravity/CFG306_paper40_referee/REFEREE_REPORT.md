# CFG306: referee report on PAPER40, "The MOND Acceleration Scale from MeerKAT: 47 Deep-Regime HI Discs in MIGHTEE-HI COSMOS" (draft v1.0, commit 00d6c89ae)

*A hostile referee's report. The diagnostics behind it are this lane's own scripts. They are post hoc, were not frozen, and are not an a₀ measurement. κ = ½ is FITTED. Nothing here says the data favour any law. The cold mass is still required. Both footings (9.3603 × 10⁻¹¹ and 1.1312 × 10⁻¹⁰ m s⁻²) are quoted throughout.*

## Recommendation: MAJOR REVISION. Do not deposit v1.0.

The reproduction is clean. Every lane script and the paper's figure script re-run from a `git archive` mirror. Every results JSON and CSV comes out byte-identical, and the figures are identical apart from their creation dates. The audit gives 306 of 306 at HEAD.

The physics has one critical error and four major gaps.
- **The critical error.** The catalogue's W50 values are rest-frame widths, and the catalogue paper itself shows this. The chain divides them by (1 + z) again. This error alone moves the headline from 1.05 to 1.31 × 10⁻¹⁰ m s⁻², which is above both footings on the catalogue flux scale.
- **The major gaps.**
  - The flux-scale range is built on a reading that has no physical basis.
  - The SPARC control is presented as calibrating a chain whose velocity side it never tests.
  - The kernel dependence at y ≈ 0.03 (+0.08 dex) is missing from the systematics.
  - The S/N cut moves a₀ by 0.07 dex, and the paper does not report it.
- **Prior art.** The fifth major finding (M5) is that the MIGHTEE resolved work is misdescribed.

The paper does many things right:
- frozen criteria;
- the fails that are disclosed are kept;
- the controls are reproducible;
- no "data favour" language;
- κ = ½ is called fitted;
- the cold mass is kept;
- it states plainly that it is not an a₀(z) test.

After the frame fix, the honest bottom line is roughly this. On the catalogue scale a₀ is about 1.3 × 10⁻¹⁰. On the single-dish scale (gas only) it is about 0.9–1.06 × 10⁻¹⁰. Width corrections lower it by up to 0.1 dex, and the choice of kernel raises it by up to 0.08 dex. The result cannot separate the footings.

## Findings

Severity counts: **1 CRITICAL, 5 MAJOR, 12 MINOR, 9 NIT.**

### CRITICAL

**C1. The catalogue W50 is already rest-frame, so dividing by (1 + z) biases a₀ low by 0.098 dex.** Locations: §3 (the chain), abstract, Table 1, Fig. 1, §5 "velocity frame", §6, Conclusions.
- **Evidence** (`cfg306_velocity_frame.py`, F1). The catalogue paper (MM26, arXiv:2605.28731, Appendix D; the local PDF re-read with pdftotext) prints each example's W50 both in km s⁻¹ and in 26.126 kHz channels.
  - For all five examples, the km s⁻¹ per channel equals c·Δν/ν_obs to +0.07%. That is the rest-frame width, and the constant 0.07% is c = 3 × 10⁵ km s⁻¹.
  - The observed-frame conversion c·Δν·ν₀/ν² misses by −1.6% to −8.3%, growing with z: −8.3% at z = 0.0907.
  - The text agrees: the channel velocity width is "calculated for the given redshift", 5.5 km s⁻¹ at z = 0.
  - Four of the five example W50 values equal the catalogue values to rounding.
- **Supporting, not decisive.** CFG302's raw rest-frame widths show no z-trend in their ratio to the catalogue. The clipped Theil–Sen slope on log(1 + z) is +0.29, with a 95% range of −1.05 to +1.42. The observed-frame reading predicts −1, which sits at the edge. CFG302's "+0.003 vs −0.022 dex" cannot decide the frame, because the 5% method offset happens to equal (1 + z) at the median z.
- **Where the error came from.** The (1 + z) step comes from CFG260/CFG281. There the ALFALFA and BUDHIES widths are observed-frame: H18 applies no cosmological correction. The step was carried over to a catalogue whose widths are rest-frame.
- **Consequences** (`cfg306_physics_checks.py`, P1).
  - On the catalogue flux scale, a₀ = **1.311 × 10⁻¹⁰** (own bootstrap: 68% 1.27–1.42, 95% 1.24–1.66). That is +0.146 dex from canonical, +0.064 dex from alt and +0.038 dex from SPARC's 1.20, with κ = **0.70 / 0.58**.
  - Both footings fall outside the 95% statistical interval. The recipe half-width recomputed at k = 0 is 0.128 dex (δ 0.098, M\* 0.069, D_HI 0.026, H₀ 0.036). So on the catalogue scale the canonical footing is 0.018 dex outside it, and the alternative footing is inside. This is a fail on the catalogue scale, kept as a fail; M1 is what removes it.
  - The W3 − W1 drift changes sign, from −0.057 to +0.022 dex, so the "same sign as CFG281" remark (§4) is withdrawn.
  - CC1 and CC3 pass under both frames. A 0.1 dex shift is invisible to the controls (see M2).
- **Fix.** Make k = 0 the primary and recompute every downstream number, figure and κ. Keep k = 1 only as a disclosed variant. If the authors want to keep k = 1, they must show that the catalogue's columns differ from the appendix conversion, for example in writing from the catalogue team.

### MAJOR

**M1. The flux-scale range "0.6–1.05 × 10⁻¹⁰, catalogue value at the top" is not fair, and the abstract weights it wrongly.** Locations: abstract, §5 "What the flux scale does", Table 2 rows 1–5, Fig. 1 open markers, §6 bullet 4, Conclusions.
- **(a) The lower end has no physical basis.** The 0.60 comes from raising *all* baryons by 0.195 dex. An HI flux-scale error cannot change the BAGPIPES stellar masses, so only the gas-only reading is a flux-scale systematic. That reading gives 7.50 × 10⁻¹¹ at k = 1, and **9.01 × 10⁻¹¹** at k = 0 (P3).
- **(b) The 47 discs lie largely outside the calibrating pairs** (`cfg306_flux_scale.py`, S1–S2).
  - The 15 code-1 pairs have median z 0.028, against 0.065 for the 47.
  - Their SNR_3D is 18.7, against 12.4.
  - Their θ_HI is 66″, against 40″.
  - Only 30% of the 47 lie inside the pairs' z range, and only 7 of the 47 have a pair.
  - R_cat becomes less negative toward the 47's properties. In the code-1 pairs, Spearman(R_cat, log SNR) is −0.62 (p 0.01). Linear trends extrapolate to R_cat ≈ −0.115 (in SNR) and −0.087 (in z) at the 47's medians.
  - CFG304's own z ≥ 0.02 subsets give −0.137 (N 19) and −0.120 (clean).
  - So for the 47, the offset is −0.09 to −0.20 dex, not −0.195.
- **(c) The direction of the offset is robust.**
  - SPARC's own M_HI sit **+0.053 dex above ALFALFA's**, at the same distance, for 35 SPARC × ALFALFA galaxies (P6). So the catalogue is about 0.25 dex below the HI scale of CC2's own calibrator. ALFALFA is not the high outlier.
  - Confusion would need about 500 times the mean cosmic HI density of *uncatalogued* HI in a 3.5′ × ±300 km s⁻¹ beam (S3). MIGHTEE is far deeper than ALFALFA, so this is implausible.
  - MeerKAT's 29 m shortest baseline recovers scales of about 25′, far larger than θ_HI of 25–110″. Missing short spacings are therefore excluded.
  - The catalogue paper's flux method is a plausible cause, though not demonstrated: an iterated 3σ moment-0 mask on a 15.5″ cube, with the moment map built over the channels "within the measured width". The paper validated it only on sources injected after imaging, and it shows no single-dish comparison.
- **Fix.** Drop the all-baryon reading as a flux-scale systematic, or label it as a stellar-plus-HI scaling that has nothing to do with the flux. Quote the gas-only range at k = 0: **0.90–1.06 × 10⁻¹⁰** for R from −0.195 to −0.120, or 0.90–1.13 × 10⁻¹⁰ including the extrapolated −0.087. On present evidence the catalogue-scale value is the *least* consistent with the chain's own SPARC calibration, not "the top of a range". Recast the abstract around the range, not around one value.

**M2. CC2 does not validate the chain's velocity side or its flux scale. "A chain calibrated on SPARC" (§6) over-claims, and the §6 bullet-4 inference is a non sequitur.**
- **What CC2 actually tests.** CC2 uses V_flat. It does not use W50, the optical sin i, the frame or δ. It also uses SPARC's own M_HI, which sit at or above the ALFALFA scale. So it tests the baryon recipe only, as §3 says, and cannot "not show" a MeerKAT flux offset.
- **A width-side test** (P6), on 22 SPARC × ALFALFA galaxies with Q ≤ 2, i ≥ 30° and code 1.
  - W50/(2 sin i) exceeds V_flat by **+0.026 dex** (68% +0.022 to +0.032). For V_flat < 160 km s⁻¹ the excess is +0.014 dex. With δ = 11 it is −0.018 dex, so δ ≈ 5 km s⁻¹ removes the offset at MIGHTEE-like masses, which lowers a₀ by about 0.05 dex.
  - The CC2 recipe run with W50 instead of V_flat gives s\* **+0.18 dex** higher at δ = 0, and +0.07 dex higher at δ = 11.
- **CC1 has no power at the level that matters.** Its ±0.15 dex tolerance cannot calibrate at the 0.08 dex that separates the footings. It passes at both k = 1 and k = 0.
- **Fix.**
  - Call CC2 a baryon-side closure everywhere.
  - Calibrate W50 against V_flat with Lelli et al. (2019, MNRAS 484, 3267), which gives exactly these relations, or with the SPARC × ALFALFA overlap.
  - Treat δ as two-sided around an empirical value.
  - Delete "an offset that the chain's SPARC closure does not show".

**M3. The kernel dependence of a₀ at y ≈ 0.03 is a missing systematic of +0.08 dex, as large as the footing separation (0.082 dex).** Locations: §3 estimator, Table 2, "framework-native" (abstract, §1).
- **The spread** (P2). With the same chain at k = 1:
  - ν_mono, which is the MLS16 exponential here, gives 1.046 × 10⁻¹⁰;
  - the "simple" kernel gives 1.043;
  - the "standard" n = 2 kernel gives 1.234;
  - the **framework's own closed form √(1 + 1/y)** gives **1.216**;
  - the δ-family at V26's best δ = 4.1 gives 1.251.
  - At k = 0 the same kernels give 1.31 to 1.53.
- **Why.** The exponential and simple forms carry the +½ term (ν ≈ y^−½ + ½), which the others lack. That term is the whole of the +0.078 dex "kernel factor".
- **What is robust.** Against CC2 run with the same kernel, the MIGHTEE offset is stable: −0.066 to −0.086 dex at k = 1, +0.001 to +0.032 dex at k = 0. So the comparison with SPARC holds up, but the comparison with the footings does not.
- **External corroboration.** V26 shows the same effect on MIGHTEE data: 1.50 with MLS16 against 1.86 ± 0.06 with the δ-family.
- **Fix.**
  - Add a kernel row to Table 2.
  - State which kernel the footings (and κ = ½) are defined with.
  - Stop calling the chain "framework-native", or report the closed-form result alongside.

**M4. Selection: the frozen SNR_3D ≥ 8 cut moves a₀ by 0.07 dex, and the per-galaxy residuals trend with the sample's properties.** Locations: §2 cut, §5 "Mass matching and sample size", Table 2.
- **The cut** (P4). It removes 23 of 70 discs. Those 23 alone give a₀ = 1.72 × 10⁻¹⁰, and all 70 give 1.23 × 10⁻¹⁰, which is +0.07 dex.
  - At fixed flux the catalogue's SNR_3D scales as W50^−0.50 over the 70. The cut therefore favours narrow lines (low V), which biases a₀ low among the survivors.
  - Equally, low-S/N fluxes or widths may be biased.
  - Either way, the effect belongs in Table 2.
- **Residual trends.** The per-galaxy log s\* correlates with W50 (ρ +0.60), with gas fraction (ρ −0.45, p 0.002) and with log M\* (ρ +0.34, p 0.02).
- **Slope.** The BTFR inverse slope is 3.50 (68% 3.17–3.88). For comparison, P21's W50 slope is 3.66 and V26's is 3.72. With a slope below 4, the median V⁴/M_b depends on the sample's mass distribution, and so does any comparison with SPARC or between windows.
- **The stellar-mass claim.** "The stellar mass hardly matters" (§4) rests on a median difference of −0.023 dex, which the gas-fraction trend contradicts.
- **Fix.**
  - Report the a₀ dependence on the S/N threshold.
  - Fit the residual jointly in z and log M_HI, or log M_b, instead of the bins that failed.
  - Discuss HI-flux selection in the BTFR. V26 shows that the forward-versus-inverse choice moves their evolution signal from 8.7σ to 3.4σ.

**M5. Prior art is misdescribed or missing.** Locations: §1 "MeerKAT", §4 "Against other determinations", references. All checked on the arXiv API, Crossref and the V26 source on disk.
- **(a) V26's kernel.** V26's fiducial 1.50 ± 0.05 uses the *same* MLS16 exponential function (main.tex l.526–540), not "its own kernel". Its δ-family fit gives 1.86 ± 0.06 (l.631), and its Sérsic route gives 1.48 ± 0.04.
- **(b) V25's value.** V25's a₀ = 1.69 ± 0.13 (19 COSMOS galaxies) is not quoted.
- **(c) Redshift evolution.** V25 reported "tentative evidence for redshift evolution". V26 finds a **formal 5.0σ increase of a₀ with z when SPARC anchors z ≈ 0**, which they attribute to sample selection; MIGHTEE + LADUMA alone give a₁ = −1.6 ± 2.3. The paper's "no significant redshift evolution" leaves this out, and it bears directly on the framework's distinctive constant-a₀(z) prediction.
- **(d) V26's flux scale and overlap.** V26's HI comes from 3D Barolo on the 12″ DR1 cubes with a 3σ mask, so it carries MeerKAT's interferometric flux scale. The paper says it has not checked; the answer is in V26 §2–3. At most 28 of V26's 130 galaxies are in COSMOS.
- **(e) Missing references.**
  - Lelli et al. 2019, on W50 against V_flat;
  - Papastergis, Adams & van der Hulst 2016 (A&A 593, A39): gas-dominated ALFALFA W50 BTFR, slope 3.75, with a profile-shape dependence;
  - McGaugh 2012, the BTFR normalisation;
  - the standard width corrections: Verheijen & Sancisi 2001 for turbulence, Springob et al. 2005 for instrumental broadening;
  - P21's W50 slope 3.66 (abstract).
- **(f) SPARC's systematic.** SPARC's g† is 1.20 ± 0.02 (stat) ± 0.24 (sys) [MLS16]. "Consistent with SPARC (−0.060 dex)" should carry the 0.08 dex systematic.

### MINOR

- **m1. CC1's second reference is not calibrated.** CFG281 is itself **NOT CALIBRATED**, by its own README. It also uses δ = 9 km s⁻¹, observed-frame ALFALFA widths and the isotropic sin 60°, so it is not the same recipe as CFG301. §3 should say so.
- **m2. The bootstrap interval of a median of 47 is lumpy.** The committed 68% runs −0.014 / +0.039 dex. A different seed gives a lower edge of 0.992 rather than 1.012. The robust per-galaxy scatter (0.199 dex) implies ±0.036 dex. Quote the bootstrap SD (0.035 dex) or a symmetric robust error.
- **m3. Molecular gas is omitted and absent from Table 2.** Adding M_H2 = 0.1 or 0.3 M_HI lowers a₀ by 0.027 or 0.070 dex (P7). CFG281 carried this row.
- **m4. The H₀ convention.** The footings use H₀ = 67.4, so quote the H₀-consistent value against them: 0.962 × 10⁻¹⁰ at k = 1, **1.208 × 10⁻¹⁰** at k = 0 (κ 0.645 / 0.534). Quoting the H₀ = 70 value against a 67.4 footing biases the comparison by +0.036 dex.
- **m5. The beam range (§5) is wrong.** "74.2–77.3″" is copied from CFG302's README. The lane's output gives valid-channel beams of 62.2–77.3″ (median 75.9″) and per-sub-cube medians of 74.7–77.3″. The audit checks this row against the README, not the output (number_trace N39).
- **m6. "+0.000 dex (scatter 0.037)" for catalogue/ALFALFA widths (§5).** The median sits on an exact integer tie: 3 of 23 pairs have identical W50. Give the 68% range (−0.025 to 0.000) and the −0.012 dex expected under the rest-frame reading. Like CFG302, it does not decide the frame.
- **m7. The geometry.**
  - The next-order kernel term depends on the effective radius that W50 samples. That is HI-weighted and usually smaller than R_HI, so D_HI ± 0.15 dex may understate the R knob.
  - Say that g_bar uses the total M_b, which is an asymptotic approximation, not the mass enclosed at R.
  - The size relation is "not re-checked against W16" (§3). A web-search snippet gives W16's relation as (0.506 ± 0.003) log M_HI − (3.293 ± 0.009), which matches; this is provisional, so check it against the paper and say so.
- **m8. The calibration wording.** "Four calibration controls pass" (abstract) should say that CC1 and CC3 are evaluable only on unmatched windows, as the disclosures concede.
- **m9. Inclinations.** The residual shows no trend with inclination (ρ −0.06) or axis ratio (ρ +0.07); say so. Mention optical-versus-HI inclinations and seeing for the smallest discs.
- **m10. "So the velocity side of the chain stands" (§5, CFG302 paragraph).** CFG302 confirms the catalogue's W50 *measurement*. It does not confirm the W50 → V conversion: frame, δ, W50 versus V_flat.
- **m11. Audit robustness.**
  - The tex check is a substring match within a block, and 7 literals are 4 characters or fewer.
  - README-sourced rows can disagree with script outputs, as m5 shows.
  - The PDF is not checked against the tex. I checked 27 sampled numbers, and all are present.
- **m12. Internal lane labels.** CFG260, CFG279, CFG281 and so on are cited as if they were sources. A reader outside the programme needs each claim stated with its public data, or a repository pointer per number.

### NIT

- **n1. The abstract is 333 words**, against MNRAS's 250 limit, and dense. A version of 247 words is given below.
- **n2. Byline and metadata.**
  - The byline says "The authors", but the Zenodo creator field carries the owner's name and affiliation. This matches the 39 earlier `*.zenodo.json` files, and the deposit needs a creator, so it is the owner's call.
  - No e-mail address or home-directory path appears in the paper's files, the PDF text, or any of the 75 committed files of the paper and the three lanes.
- **n3. The title over-promises.** Suggested: "A width-chain estimate of the MOND acceleration scale from MIGHTEE-HI COSMOS, with its flux-scale, line-width and kernel systematics".
- **n4. Figures.** Fig. 1 shows the all-baryon reading (A), which is not a flux systematic; add the k = 0 point and the gas-only k = 0 band. Fig. 2's V should become W50/(2 sin i) at k = 0.
- **n5. Format.** Single column, 7 pages, all fonts embedded, vector figures. That is fine for Zenodo. MNRAS would need its own class.
- **n6. Script provenance.** The committed CFG301 `.out` files for stages A, SELFTEST, CC2 and M5 were written by a script whose docstring later gained one line (DRYRUN). The re-run results are identical, but the script is not byte-identical to the one that wrote them.
- **n7. A lane README slip.** CFG304's README prints 4.99 for reading A's 68% lower end; the JSON gives 4.985, so the paper's 4.98 is right.
- **n8. A catalogue-paper oddity.** Its example 1 (J100404.9+014303) prints W50 237.9 km s⁻¹, while the catalogue lists 223. The frame inference does not depend on it; ask the authors if they are contacted.
- **n9. One reference lacks an arXiv check.** MS08 is cited for the α = ½ member; Crossref confirms the record (ApJ 678, 131), but the family's form was not checked on arXiv here.

## Proposed abstract (247 words)

> The programme ties MOND's acceleration scale to the vacuum, a₀ = κc√(Gρ_Λ), with κ = ½ fitted, not derived; its footings are 9.36×10⁻¹¹ (ρ_Λ) and 1.13×10⁻¹⁰ m s⁻² (ρ_crit). We apply a width chain, frozen before any width was read, to the public MeerKAT MIGHTEE-HI COSMOS catalogue: V comes from the rest-frame W50 and optical inclination, the baryons are 1.33 M_HI + M⋆ at half the HI diameter, and a median-residual estimator with the exponential (McGaugh et al.) kernel returns a₀. Forty-seven golden discs at 0.027 ≤ z ≤ 0.093 survive, all at g_bar/a₀ ≤ 0.084 and 37 gas-dominated. On the catalogue's flux scale the pooled value is a₀ = 1.31×10⁻¹⁰ m s⁻² (statistical ±0.035 dex), above both footings (κ = 0.70 or 0.58). Three systematics dominate. Arecibo single-dish fluxes exceed the catalogue's by 0.12–0.20 dex for 15–23 overlapping, brighter and nearer galaxies; if this applies to our discs' HI, a₀ falls to 0.90–1.06×10⁻¹⁰. Line-width corrections (turbulence; W50 versus flat rotation speed) lower a₀ by up to 0.1 dex. At these accelerations a₀ depends on the kernel: forms without the exponential's next-order term raise it by 0.08 dex. A SPARC closure tests the baryon recipe (+0.008 dex) but neither the width side nor the MeerKAT flux scale. The result is consistent with SPARC and, on the single-dish scale, with both footings; it cannot separate them, nor, at z ≤ 0.093, test the constant a₀(z) the framework predicts. The cold mass (Ω_c h² ≈ 0.12) is still required.

*Every number in this abstract is a CFG306 referee recomputation (`cfg306_physics_checks.py`). The revision must regenerate each one from committed lane scripts, frozen where the record requires it, before it is printed.*

## Over-claim sweep (item 5)

Sentences that imply more than "consistent with both footings on the catalogue scale; an upper value; not an a₀(z) test":
1. Abstract and §6: "four calibration controls pass" and "a chain calibrated on SPARC". The velocity side and the flux scale are not calibrated (M2).
2. Abstract and §1: "framework-native width chain". The kernel is MLS16's, not the framework's closed form (M3).
3. §6 bullet 4: "an offset that the chain's SPARC closure (CC2) does not show". This is a non sequitur, and it leans against the flux correction (M2).
4. §5: "so the velocity side of the chain stands" (m10).
5. §4: "so the stellar mass hardly matters" (M4).
6. Abstract and Conclusions: "the catalogue value at the top" and "0.6–1.05". The frame and the all-baryon reading are wrong (C1, M1).
7. Abstract: the velocity frame "could add +0.098 dex". The cited catalogue paper settles this (C1).

What the paper gets right: no sentence says the data favour the framework; κ = ½ is called fitted; both footings are given; the cold mass is kept; "not an a₀(z) test" is stated clearly.

## References checked (arXiv API and Crossref, 2026-10-02; abstracts only, no downloads)

| ref | checked | result |
|---|---|---|
| D23 Desmond 2023 | arXiv 2303.11314 + journal ref | a₀ = 1.19 ± 0.04 ± 0.09; MNRAS 526, 3342: OK |
| MLS16 | arXiv 1609.05917 | 2693 points, 153 galaxies; PRL 117, 201101: OK (paper omits g†'s ±0.24 sys) |
| P21 Ponomareva+ | arXiv 2109.04992 + Crossref | 67 galaxies, 0 ≤ z ≤ 0.081; MNRAS 508, 1195: OK; W50 slope 3.66 not quoted |
| R22 Rajohnson+ | arXiv 2203.06149 + Crossref | 204 galaxies, slope 0.501, intercept −3.252; MNRAS 512, 2697: OK |
| W16 Wang+ | arXiv 1605.01489 + Crossref | MNRAS 460, 2143: OK; coefficients 0.506 / −3.293 by web snippet only (provisional) |
| V25 Vărăşteanu+ | arXiv 2504.20857 + Crossref | 19 galaxies to z = 0.08; MNRAS 541, 2366: OK; its a₀ = 1.69 ± 0.13 and its evolution hint are omitted |
| V26 | arXiv 2608.03576 + source on disk | 1.50 ± 0.05, MLS16 kernel; δ-family 1.86; SPARC-anchored 5.0σ evolution: misdescribed (M5) |
| MM26 | arXiv 2605.28731 + Crossref | MNRAS 550, stag1091 (2026): OK; channel 26.126 kHz, rest-frame widths (C1) |
| H18 Haynes+ | arXiv 1805.11499 | DOI 10.3847/1538-4357/aac956: OK |
| MS08 | Crossref 10.1086/529119 | ApJ 678, 131: OK |
| Lelli+ 2019; Papastergis+ 2016 | arXiv 1901.05966; 1602.09087 | missing from the paper (M5e) |

Files: `README.md` (what was run), `number_trace.csv` (60 numbers; 59 match; N39 does not), `uncovered_numbers.csv`, and the helper scripts with their `.out` and `_results.json`.
