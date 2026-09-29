# CFG57 gas sources: extraction record

These are the hot-gas numbers for the pre-registered CFG57 test (`campaign_fresh_gravity/CFG57_FROZEN_CRITERIA.md`). They are read from the two sources that the frozen file names. This directory holds data extraction only: it fits no model and computes no prediction or galaxy-dynamics offset.

The sources are in `raw/`, which is git-ignored. Each script checks its source's sha256 before it runs.

| file | what |
|---|---|
| `raw/lakhchaura2018_1806.00455.pdf` | Lakhchaura et al. 2018, MNRAS 481, 4472, arXiv:1806.00455v2. sha256 `706f479c…3b88b0` |
| `raw/fukazawa2006_astro-ph_0509521.tar.gz` | Fukazawa et al. 2006, ApJ 636, 698, arXiv:astro-ph/0509521 (LaTeX source). sha256 `68f6999d…5e5ec4` |
| `extract_lakhchaura.py` → `lakhchaura2018_ne_profiles.tsv`, `extract_lakhchaura.out` | the Fig. A.2 digitisation, the Table 1 distances and validations V1–V4 |
| `transcribe_fukazawa.py` → `fukazawa2006_table4.tsv`, `transcribe_fukazawa.out` | Table 4 (all 53 rows) with the Table 1 distances |

To reproduce, run `python3 transcribe_fukazawa.py`, then `python3 extract_lakhchaura.py`. The first script writes the TSV that the second one's V4 row reads. Both scripts are deterministic and run in about 4 s. Tested with PyMuPDF 1.27.2 and numpy 1.26.

---

## Source 1: Lakhchaura et al. 2018, Appendix Figure A.2

**What was extracted.** Figure A.2 ("Deprojected density profiles of the individual galaxies") is vector graphics. The four panels used here are:
- NGC 4374, NGC 4486 and NGC 4649 on PDF page 21;
- NGC 5846 on PDF page 22.

From each panel the script takes every plotted point and both of its error bars. No point or bar went unrecovered, and none of the four panels has a hidden (clipped) marker.

| galaxy | D (Table 1) | points | plotted r (kpc) | shell edges (kpc) | n (cm⁻³) |
|---|---|---|---|---|---|
| NGC 4486 | 16.56 Mpc | 25 | 0.788 – 29.51 | 0.079 – 30.38 | 0.163 → 0.0108 |
| NGC 5846 | 27.13 Mpc | 23 | 0.777 – 35.63 | 0 – 36.69 | 0.156 → 0.00229 |
| NGC 4374 | 16.68 Mpc | 12 | 0.406 – 18.37 | 0.162 – 19.26 | 0.248 → 0.00171 |
| NGC 4649 | 16.55 Mpc | 20 | 0.158 – 20.81 | 0 – 23.57 | 0.781 → 0.00171 |

There are 80 rows in all.

Spot values, taking the point nearest 10 kpc in each panel (r in kpc, n in cm⁻³):
- NGC 4486: (10.008, 0.029556)
- NGC 5846: (9.6429, 0.015207)
- NGC 4374: (10.29, 0.0034604)
- NGC 4649: (10.563, 0.006002)

**Which quantity the figure plots.** The y axis is `n`, the total particle density n = nₑ + nᵢ, as defined in the paper's §2.2.5 and eq. 1. It is not nₑ.

The TSV gives both. The `n_*` columns are the values as plotted. The `ne_*` columns are 0.53 × n, which is the paper's own conversion for a fully ionised plasma at 1/3 solar abundance ("nₑ = 0.53n").

V2 below confirms this reading from the paper's own entropy figure. Had the plotted n been nₑ, K would be off by a factor of 1.527.

The paper's mass density is ρ = 0.62 mₚ n (footnote 4), which equals 1.170 mₚ nₑ. CFG57 freezes μₑ = 1.155, which is 1.3% lower.

**The other columns.**
- `r_kpc` is the plotted radius. It is the linear mid-point of the deprojection shell, (r_in + r_out)/2, verified to better than 1e-5 dex.
- `r_in_kpc` and `r_out_kpc` are the ends of the x error bar, which are the shell edges. The shells are contiguous to machine precision, and the paper assumes constant n and T within each shell.
- `r_in = 0` means the innermost bar runs to the edge of the figure canvas, so that shell starts at the centre. This is the case for NGC 5846 and NGC 4649.
- NGC 4486's innermost shell starts at 0.079 kpc (2 ACIS pixels) and NGC 4374's at 0.162 kpc (2.0″). These gaps are presumably the central point-source exclusion, although §2.2.2 gives that as 3 pixels (1.476″).
- `*_lo` and `*_hi` are the ends of the y error bar as drawn. The paper does not state their confidence level.

**How the extraction works** (the `diteodoro2023_extraction` precedent, done with PyMuPDF on the vector data):
1. **Which panel owns what.** matplotlib draws each axes completely before the next: its white background, then its data, ticks and labels. The script assigns every vector path and text span to the axes whose background was drawn last before it (PDF drawing order, `seqno`). This is what stops panels that share an edge from leaking ticks, labels or points into one another. A galaxy's panel is the axes that drew its name.
2. **Axis calibration.** Tick labels are read from the text layer together with their font sizes: the base "10" is large, the exponent small, and a minus sign is a small filled bar. Each label is paired with its own tick mark, and log10(value) is fitted linearly against the tick coordinate.
3. **Panels without their own labels.** These share their axes with a labelled panel. The script uses that panel's calibration only after checking that the unlabelled panel's own tick marks sit at exactly the same places (mismatch 0.0 pt).
4. **Points.** A point is the centre of its filled marker. Its x and y error bars are the stroked lines of the same colour passing through that centre. Every point has exactly one of each, and no bar is left unused.

**Calibration residuals** (all ticks, every panel):
- x: at most 4.5e-7 dex, over 3 labelled ticks (10⁰, 10¹, 10²);
- y: at most 6.0e-7 dex, over 4 labelled ticks (10⁻³ to 10⁰).

Both are listed per panel in the TSV header.

**Digitisation error: stated as 0.001 dex per coordinate (r and n).** This is conservative. The internal budget is below 4e-5 dex:
- calibration residuals below 1e-6 dex;
- vector coordinates exact to about 1e-3 pt, which is 2e-5 dex in r and 3e-5 dex in n;
- marker centre and error-bar crossing agree to within 1.2e-4 pt.

The validation checks below agree with this at the 1e-5 level.

**Distance.** `D_Mpc_paper` comes from Table 1 (PDF page 3), the NED "mean redshift-independent distance". The paper's eq. 1 names an angular-diameter distance D_A, and it assumes H₀ = 70, so the script checks which distance was actually used to turn arcsec into kpc:
- Of the 49 panels, 15 have a finite innermost shell edge.
- With the Table 1 D, 14 of those 15 edges come out as a whole number of ACIS pixels to better than 0.01 px (2, 3, 4 or 6 px). The 15th, NGC 4374, comes out at 2.000″.
- With the H₀ = 70 redshift distance, none do; the median offset from a whole pixel is 0.29 px.

So the kpc radii were made at the Table 1 D. That the densities (eq. 1) used the same D is an assumption, since both come from the same pipeline; nothing in the figures can test it directly.

**Validation.** C2 asks for a number printed in the paper and reproduced within 10%. The paper prints no per-galaxy density, gas mass or radius anywhere: its Table 1 has z, D, kT, L_X and the like, and its other tables hold sample statistics, jet powers and the observation log. So, as the task allowed, the method is validated on a figure whose plotted values are printed, and the density scale is then checked against the paper's own other figures.

- **V1: the same machinery on Fig. 1, against printed values.** This is the C2 fallback. Fig. 1 is in the main text, not the appendix; no appendix figure has printed counterparts.
  - Fig. 1 plots L_X and M_gas against T_X within 10 kpc, and T_X and L_X are both printed in Table 1.
  - For all four galaxies, the digitised T_X and L_X equal the printed values. The largest deviation is 8e-8 in kT and 6e-7 in L_X, far inside the 10% criterion. **PASS.**
  - Across all 49 galaxies, 47 round to the printed values. The other two are differences between the paper's table and its figure, not digitisation errors:
    - NGC 777: kT printed 0.62, plotted 0.90;
    - NGC 1132: L_X printed 0.17, plotted 0.16.
- **V2: identities between the appendix figures, shell by shell.** Figs. A.1 (kT, linear axis), A.3 (K) and A.4 (P) were digitised independently with the same code, and the shells were matched by radius: 79 of the 80 appear in all four figures. The 80th is NGC 4649's innermost shell, whose pressure point lies above the A.4 frame and is clipped there.
  - P / (n kT) = 0.99864 ± 0.00001 for every shell. This equals 1.6/1.602177: the paper used 1 keV = 1.6e-9 erg.
  - K / (kT (0.53 n)^(-2/3)) = 1.00000 ± 0.00001.

  The digitised densities are therefore consistent with the paper's independently plotted P, K and kT to about 1e-5. V2 also shows that n is the total density.
- **V3: gas mass, against the paper's own M_gas(10 kpc) in Fig. 1.** Each galaxy's M_gas point is identified by its position in the drawing order. By x alone it would be ambiguous: NGC 4374 and NGC 4636 are both "NE" at kT = 0.68.
  - Summing the digitised shells with μ = 0.62, up to and including the shell that contains 10 kpc, reproduces the plotted M_gas to a ratio of 1.0023 for all four galaxies.
  - This scheme was found after two others fell 7–18% short: cutting the shells at 10 kpc, and log–log integration through the plotted points. All three are in the log.
  - So Fig. 1's "M_gas (10 kpc)" is the gas inside the outer edge of that shell (10.3–11.4 kpc).
- **V4: comparison with the other source.** This is not a digitisation check. It compares Lakhchaura's nₑ at 10 kpc (0.53 n, moved to Fukazawa's D with r ∝ D and nₑ ∝ D^-1/2) with Fukazawa's Table 4:
  - NGC 5846: 0.96
  - NGC 4649: 1.29
  - NGC 4374: 2.91
  - NGC 4486: not in Fukazawa.

  V1–V3 are exact, so the NGC 4374 factor comes from the papers themselves, not from the extraction. One possibility is how each paper treats the surrounding Virgo emission:
  - Fukazawa set R_max small wherever there is flat outer emission. For NGC 4374 it fits a single β component (n_β = 1) out to R_max = 15.4 kpc.
  - Lakhchaura uses blank-sky backgrounds and warns (§2.2.3) that the outer annuli may contain group or cluster gas.

  This is untested.

**Caveats for the use CFG57 makes of these profiles:**
- **The outermost point rises in three of the four profiles.** The last shell sits above the trend:
  - NGC 4486: ×1.99 the previous point;
  - NGC 5846: ×1.50;
  - NGC 4374: ×2.27;
  - NGC 4649: flat (×0.99).

  This is the usual outermost-shell deprojection effect, and §2.2.3 warns about exactly this contamination. The points are kept as plotted, not edited. The frozen rule "extrapolate with the power-law slope of the outermost three points" will pick up these upturns. How to handle that is CFG57's call, and any departure from the frozen rule must be disclosed.
- **Metallicity.** The paper froze each galaxy's metallicity at its 10 kpc value. §2.2.5 says a metallicity underestimated by a factor 2 overestimates n by about 1.35×. Footnote 2 reports that freeing the metallicity lowered the densities by less than 10% in the two galaxies tested.
- **Size of the error bars.** The relative half-width of the drawn y bars, lowest to highest over each galaxy's points:
  - NGC 4486: 0.1–0.6%;
  - NGC 4649: 0.6–4.5%;
  - NGC 5846: 1–12%;
  - NGC 4374: 2–50%, the largest at r = 16.5 kpc.

  Many bars are hidden under the marker in the published figure but are recovered from the vector data. They are the paper's statistical errors only.

---

## Source 2: Fukazawa et al. 2006, Table 4 and Table 1

**What was transcribed.** The script parses `ms.tex` inside the tarball, which has 1626 lines. It writes all 53 rows of Table 4 (`table:results`, caption line 1492, data lines 1506–1558):
- n_β;
- R_max in kpc, with a lower-limit flag where the table prints ">";
- nₑ at 10 kpc, in units of 1e-3 cm⁻³;
- the EXG/CXG/VCXG type;
- kT_i and kT_o;
- M/L_B;
- n_depro.

It also joins the distance D from Table 1 (`tab:sample-chandra`, caption line 1309, data lines 1322–1375). Every row records its line number in the `.tex`.

The script checks that the source has exactly five deluxetables, in the order sample-chandra, sample-newton, spec, results, nfwcmp, and no other table environment. That makes `table:results` Table 4.

**Conventions.**
- The paper assumes H₀ = 70 km s⁻¹ Mpc⁻¹ (line 261).
- D comes from Table 1, which takes it from O'Sullivan et al. 2001 and NED. Most of the Virgo galaxies are placed at 15.9 Mpc, and lines 686–689 note that NGC 4697 is at 15.1 Mpc.
- nₑ,10kpc is "the hot gas electron density at 10 kpc". It comes from the β-model fit to the 0.5–1.5 keV surface brightness (§3.2), which ignores how the emissivity depends on temperature.
- No per-galaxy error is given. The text says the fits are good to better than 10% and that local structure "gives 10% error to the hot gas density".

| galaxy | D (Mpc) | n_β | R_max (kpc) | nₑ(10 kpc) (1e-3 cm⁻³) | type |
|---|---|---|---|---|---|
| NGC 5846 | 22.9 | 2 | >44.18 | 7.17 | EXG |
| NGC 4374 | 15.9 | 1 | 15.43 | 0.63 | CXG |
| NGC 4649 | 15.9 | 1 | >30.70 | 2.57 | EXG |
| NGC 4365 | 15.9 | 3 | 30.70 | 0.82 | CXG |
| NGC 4494 | 21.3 | 1 | 5.05 | — (none) | VCXG |
| NGC 3607 | 19.8 | 2 | 28.55 | 1.37 | CXG |
| NGC 4697 | 15.1 | 1 | >29.20 | 0.88 | CXG |

**NGC 4494 has no nₑ(10 kpc).** Its emission stops at R_max = 5.05 kpc, so source 2 cannot normalise a β model at 10 kpc for it. NGC 4486 is not in this paper.

**Spot check and consistency checks:**
- **Spot check.** A second route through the raw `.tex` lines (a regex, not the table parser) re-reads all seven CFG57 rows, and they agree. Example: NGC 5846, line 1553 `… 2 & 9 & $>$44.18 & 6.70 & 7.17 & EXG`, and line 1370 D = 22.9.
- **Classification rule.** The paper's rule (EXG if nₑ,10 > 2e-3, CXG if below) holds for every row.
- **Joint check of D and R_max.** All 21 ACIS-S lower limits give R_max/D = 396.7–399.2″, a single field-edge angle to within the rounding of D to 0.1 Mpc. The 3 ACIS-I lower limits lie at 713–737″, the larger ACIS-I field.
