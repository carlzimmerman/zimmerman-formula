# Stellar masses of the Roman-Oliveira z~4.4 [CII] discs: BRI1335-0417, SGP38326-1, SGP38326-2 (literature look-up, 2026-10-01/02)

Data gathering only. No acceleration, a0, rotation-curve or gravity quantity was computed. The only arithmetic in the CSV is (i) log10 of two quoted linear masses
(1.7e10 -> 10.23, 2.4e10 -> 10.38) and (ii) err_lo = value - lower bound, err_hi = upper bound - value for the Ma+2019 rows (CDS gives 16th/50th/84th percentiles).
Every number below was read in a source during this task; where a value was read through a web summariser instead of a TeX file it is flagged ("WEB-READ").

Files: `ro23_stellar_masses.csv` (24 rows, 14 columns, parsed back with Python's csv module) and this README. Nothing else was edited by hand or committed; the fetch helper itself appended rows to the existing fetch log and manifest (section 7).

## 1. Bottom line

| target | SED-based stellar mass found | dynamical stellar mass (not SED) | verdict |
|---|---|---|---|
| BRI1335-0417 | log M* = 12.05 (+0.30/-0.65), TRICEPS I (Lelli+2026, Table 1), AGN included in the fit | 10.4 +/-0.1, RO24 Table 4 (baryon fraction fixed) | **No constrained SED mass.** The only SED numbers (12.05; Tsukui+2023 stellar-template ~1e12, which the authors reject as AGN-dominated) exceed every dynamical mass found in the literature (section 5). |
| SGP38326-1 | 11.04 (+0.27/-0.36) TRICEPS I; 11.52 (+0.27/-0.31) Ma+2019 (MAGPHYS, Chabrier, WEB-READ) | 11.0 +/-0.2, RO24 | Two SED values 0.48 dex apart; TRICEPS agrees with RO24 within 0.04 dex. |
| SGP38326-2 | 11.39 (+0.21/-0.22) TRICEPS I; 11.27 (+0.27/-0.33) Ma+2019 (WEB-READ) | 10.3 (+0.4/-0.6), RO24 | SED values agree with each other but sit ~1.0-1.1 dex above RO24. |

Roman-Oliveira et al. 2023 (RO23, arXiv:2302.03049) state **no** stellar mass for any of the three. Roman-Oliveira, Rizzo & Fraternali 2024 (RO24, arXiv:2403.00904, A&A 687, A35) do state masses, but
they are **dynamical** (rotation-curve decomposition with a Sersic stellar component, an NFW halo and a CO gas disc), not SED masses; RO24 say they had "no prior estimate of the stellar masses"
(aanda.tex line 273) and that the sample "not (yet) been observed with" JWST and the reddest HST band is rest-frame far-UV (line 292). Because the RO24 masses are fitted to the same [CII] rotation curves,
they are not independent of the kinematics (relevant for any use of them as independent baryon masses).
No source gives a numerical stellar-mass **upper limit** for any of the three targets (see section 4).

## 2. Primary SED sources and exactly what they print

**TRICEPS I** - Lelli, Lin, Zhang et al. 2026, arXiv:2609.30375v1 (posted 2026-09-24; arXiv comments: "Version addressing the reviewer's report"; no journal reference listed). Table 1 (TRICEPS_I.tex lines 120-155),
column log(M*), tablefoot: stellar mass and SFR "from SED fitting (from Paper II)". Paper II (Marasco et al., "submitted") is **not on arXiv** (checked the arXiv API and the astro-ph.GA new listing of 2026-09-28), so
the SED code, templates, SFH, photometric deblending and **IMF are not available** (TRICEPS I does not state an IMF). Photometry: ALMA + JWST (NIRCam/MIRI, program GO 3954, PI Lelli) + HST. Sect. 2.2 (line 172): the AGN
contribution is included in the SED fits, giving ~0.5 dex uncertainties on M* for QSOs.
Printed: BRI1335 (QSO) 12.05 (+0.30/-0.65), log SFR 3.24 (+0.90/-0.90); SGP38326-1 (SMG) 11.04 (+0.27/-0.36), log SFR 2.52 (+0.28/-0.26); SGP38326-2 (SMG) 11.39 (+0.21/-0.22), log SFR 2.44 (+0.56/-0.35).
Not lensed; lensed sources were excluded from the sample. SGP38326-1/-2 are interacting (dust bridge, common [CII] envelope; Sect. 4.3).

**Ma et al. 2019** - ApJS 244, 30, arXiv:1908.08043 ("Spitzer catalog of Herschel-selected ultrared DSFGs"). SGP38326 appears as HATLAS J000306.9-330248 = **SGP-196076**, z_spec = 4.425, "Lensed? No" (Table 3), with ALMA-resolved
components a, b, c (870 um: 17.58, 7.90, 1.33 mJy). MAGPHYS+photo-z (z fixed), Chabrier 2003 IMF (Sect. 1), BC03, delayed-tau SFH, no AGN term. IRAC 3.6/4.5 um photometry (Table 4): a = 5.94+/-3.11 / 5.93+/-1.81 uJy;
b = 6.72+/-2.08 / 4.24+/-1.57 uJy; c = <6.24 / <6.34 uJy. SPIRE de-blended with XID+ using the ALMA positions; SCUBA-2 split by the ALMA flux ratios.
The per-source physical parameters exist only as the online machine-readable Table 5 (CDS J/ApJS/244/30/table5), **not in the arXiv TeX**. WEB-READ via the CfA VizieR mirror (HTML) in four queries with identical numbers
(last read 2026-10-02T02:41:05Z): logM* a = 11.52 (16th-84th: 11.21-11.79), b = 11.27 (10.94-11.54), c = 10.72 (10.36-11.06); logsSFR/logSFR in the same rows are mutually consistent with these masses
(e.g. a: 11.52 - 8.47 = 3.05). The CDS mirror at cds.unistra.fr refused automated access ("Access Denied"), so a file-level check against the CDS table was not possible within the approved scope.
Mapping a = SGP38326-1, b = SGP38326-2, c = SGP38326-3 is my inference from the 870 um fluxes versus Oteo+2016 (SMG1 16.3, SMG2 7.3 mJy); the paper itself does not use the SGP38326-n names.

**Tsukui, Wisnioski, Krumholz & Battisti 2023** - MNRAS 523, 4654, arXiv:2302.07272 (BRI1335-0417 only). STARDUST (Kokorev+2021) UV-to-FIR fit = QSO template + AGN-heated dust + cold dust; no stellar component in the adopted fit.
Sect. 4.2.2 (mnras_template.tex lines 389-393): a variant with a stellar template in place of the QSO template is worse by chi2 = 536 (16 dof) and gives an estimated stellar mass of ~10^12 Msun that "easily exceeds the dynamical mass";
they conclude the UV-optical SED is AGN-dominated (HST/STIS image consistent with the PSF). This is a rejected diagnostic, not a measurement. Photometry in Table A1 (Pan-STARRS1 grizy, VISTA Y, 2MASS JHKs, WISE W1/W2, Spitzer IRAC/MIPS,
Herschel PACS/SPIRE, ALMA, IRAM, VLA). They also revise the SFR to 1.5-1.8e3 Msun/yr (AGN fraction 0.53-0.67; Table 3) versus 5040 +/-1300 in Wagg+2014.

## 3. Dynamical (non-SED) numbers, for the brackets you asked for

* RO24 Table 4 (aanda.tex lines 509-528): BRI1335-0417 10.4 (+0.1/-0.1) [f_bar fixed at 0.187; R_eff,* 2.3 kpc, n 6.9; log M_gas 9.8]; SGP38326-1 11.0 (+0.2/-0.2) [log M_gas 11.3]; SGP38326-2 10.3 (+0.4/-0.6) [log M_gas 11.1];
  J081740 10.6 (+0.2/-0.2). Priors: log M* uniform 9-12 (Table 2). Appendix C.2 (lines 993-1020), BRI1335-0417 only: 1.7e10 Msun with i free (prefers 50 deg), 2.4e10 Msun with c200 free; enclosed total mass
  4.2e9 Msun (0.5 kpc ring) and 2.5e10 Msun (4.6 kpc ring) at i=42 deg; simple CO gas estimate 2.92e10 Msun (lowest CO(2-1), alpha_CO 0.8, r21 0.5), "no room" for stars or halo in that comparison.
  Note the text calls 1.7e10 "47% lower" than the fiducial, whereas 1.7e10 vs 10^10.4 is ~32% lower.
* Bacchini et al. 2024 (arXiv:2405.00103, A&A accepted), Table 1: log M* = 10.42 / 11.09 / 10.34 for BRI1335-0417 / SGP38326-1 / SGP38326-2 (J81740 10.58), explicitly "taken from" the RO24 mass models - a two-decimal copy, not independent.
* Tsukui & Iguchi 2021 (Science 372, 1201; arXiv:2108.02206; the arXiv file is the submitted manuscript PDF, page 6): BRI1335-0417 compact structure (R_e < 1.3 kpc, 95%) 5.2e9-3.0e10 Msun, disc 4.9 (+1.7/-2.5)e10 Msun; M_BH ~6e9 Msun (cited).
* Tsukui et al. 2024 (arXiv:2308.14798, MNRAS 527, 8941), Sect. 3.3: disc/gas fraction > 0.73+/-0.07 within 4.0 kpc, v_total = 200+/-10 km/s; says the optical emission is dominated by a quasar (citing Tsukui+2023).
* Riechers et al. 2008 (arXiv:0808.3774, ApJ 686, L9), Sect. 4: M_dyn = 1.0e11 sin^-2(i) Msun if bound; total molecular mass 9.2e10; M_BH 6e9 (Shields+2006); merger-like, disturbed structure.
* Oteo et al. 2016 (arXiv:1601.07549, ApJ 827, 34), Sect. 3.6: SGP38326 SMG1 M_dyn ~5e10 Msun from a disc+halo fit (v_c ~300 km/s, i ~65 deg, uncertain by >= 2); virial estimates SMG1 ~3.6e11, SMG2 ~2.3e11 Msun (disc correction ~1.5x lower).
  Different resolution and geometry from RO23/RO24 (V_rot,max 562 km/s for SGP38326-1 in RO23): do not mix. Oteo+2016 print **no stellar mass**; "no near-IR counterpart in the VIKING survey" (5-sigma 23.1 mag Z to 21.2 mag Ks) is the only near-IR statement.

## 4. NOT FOUND (stated plainly)

* **BRI1335-0417: no published SED stellar mass that its authors regard as constrained.** (Only TRICEPS I's AGN-included 12.05 and the rejected ~1e12 diagnostic.)
* **No numerical stellar-mass upper limit** for any of the three targets in any paper read (Oteo+2016 gives VIKING magnitude limits only; Tsukui+2024 bounds the non-gas mass fraction, not M*).
* **SGP38326-1/-2: no SED stellar mass before 2019 in the papers read**; Oteo+2016 and Fudamoto+2017 (NOEMA/ALMA scans; Table "compare", row SGP-196076: M_H2 = 2.7e11 Msun) contain none. (A web-search snippet claimed "stellar mass of 2.7e11" for SGP-196076; that is the H2 gas mass column. Ignored.)
* **RO23: no stellar mass for any of the three** (only AzTEC 1, outside this scope, gets ~1e11 Msun quoted from an SED fit by Yun+2015; J081740 needs "an estimate of the stellar mass").
* **TRICEPS Paper II** (SED code, IMF, photometry details) not available. Papers III-V of the series were also not found on arXiv.
* No lensing magnification is involved: all three are unlensed (Oteo+2016 argue this for SGP38326; Ma+2019 "Lensed? No"; Lu+2018 call BRI 1335-0417 an "unlensed QSO"; RO23, RO24 and TRICEPS exclude lensed sources).
* Not read in detail: Ivison+2016 (abstract only; ApJ 832, 78), Toft+2014 (arXiv:1401.1510), Wagg+2010 abstract only, Oteo+2017, any non-arXiv text. Valentino+2020 (arXiv:1909.10540) HTML checked: no mention of the targets.
  The A&A (aanda.org, HTTP 403) and MNRAS/ApJ final versions were not read; RO24 and RO23 values are from the arXiv v1 TeX (neither has a v2; the arXiv HTML page of RO24, web-summarised, gave the same Table 4 values as the TeX).

## 5. Conflicts between values (all differences in dex, simple subtraction of the printed values)

* BRI1335-0417: TRICEPS SED 12.05 vs RO24 dynamical 10.4: 1.65 dex. 12.05 is also above Riechers+2008 (1.0e11/sin^2 i), Tsukui & Iguchi (compact 5.2e9-3.0e10 + disc 4.9e10) and RO24's enclosed 2.5e10. TRICEPS I itself flags ~0.5 dex QSO uncertainties.
* SGP38326-2: TRICEPS 11.39 and Ma+2019 11.27 versus RO24 10.3 (differences 1.09 and 0.97 dex). SGP38326-1: TRICEPS 11.04 vs RO24 11.0 (0.04) but Ma+2019 11.52 (0.48 above TRICEPS).
* Ordering: TRICEPS has -2 more massive than -1 (11.39 vs 11.04) although -2 is the fainter source (I_[CII] 4.3 vs 16.6 Jy km/s; I_160um 7.3 vs 17.5 mJy); Ma+2019 and RO24 have -1 > -2; Oteo+2016 (cited by RO24) say -1 is ~2.5x more massive in gas.
* IMF: Ma+2019 Chabrier; TRICEPS unspecified; RO24 dynamical (Chabrier only for SFRs). No IMF rescaling was applied to any value.
* SFR (context, same tables): BRI1335-0417 5100 +/-1500 Msun/yr in RO23 Table 2 (ref. Lu+2018; RO23 note the Wagg+2014 SED estimate may be AGN-biased) versus 1700 (+500/-400) in Tsukui+2023 and log SFR 3.24 in TRICEPS. SGP38326-1/-2: RO23/Oteo+2016 IR-based ~1830/~882 (Chabrier; log 3.26/2.95) versus TRICEPS SED log SFR 2.52/2.44.

## 6. Which papers Roman-Oliveira et al. cite for these sources

* RO23 (MNRAS 521, 1045; main.tex lines 204-240): **BRI1335-0417** - Irwin+1991 (APM selection), Guilloteau+1997 (CO 5-4), Wagg+2010 (APEX [CII]), Wagg+2014 (SED SFR ~5000), Lu+2017/Lu+2018 (CO 7-6 SFR; Table 2 ref 2), Jones+2016 (gas mass; Table 2 ref 3), Tsukui & Iguchi 2021 ([CII] kinematics, spiral/bulge).
  **SGP38326** - Oteo+2016 (CO, SFR, gas masses; Table 2 ref 5), Valentino+2020 and Toft+2014 (progenitors of massive ellipticals). AzTEC 1 - Yun+2015 (SED stellar mass ~1e11); J081740 - Neeleman+2017/2020.
* RO24 (aanda.tex lines 131-176): sample - Wagg+2014 (BRI1335-0417), Oteo+2016 (SGP38326), Neeleman+2019 (J081740); gas - Wagg+2014, Jones+2016, Oteo+2016, Neeleman+2020, Fudamoto+2017 (SGP38326 CO(4-3), MNRAS 472, 2028);
  SFR - Lu+2018, Wagg+2014 (BRI1335 ~5000), Tsukui+2023 (BRI1335 1700, AGN removed), Oteo+2016, Neeleman+2020; Tsukui & Iguchi 2021 (compact bulge) and Tsukui+2024 (bar).
  Neither cites an SED stellar mass for the three targets; RO24 state that no prior stellar-mass estimate existed for the sample.

## 7. Downloads made for this task (all via data_assembly/fetch_logged.py; arXiv e-print only; destination <repo-parent>/_external_data/arxiv_src/<id>.tar.gz plus an extracted folder)

Total 69,570,376 bytes (69.6 MB) of the 200 MB allowance; largest file 12.2 MB (cap 50 MB). The helper appended these rows to `FETCH_LOG_2026-10-01.md` and `FETCH_MANIFEST_2026-10-01.jsonl` (not edited by hand).

| arXiv id | role | bytes | sha256 |
|---|---|---|---|
| 2403.00904 | RO24 | 9,777,728 | 63707003994d2ef40dac42605ba917434d44fd6d3b0952abea4a9b01f04039a1 |
| 2302.07272 | Tsukui+2023 | 6,533,311 | 3102ac6a05445e43811d379e1c62f9f22a4583651de6f8db7ebaa51dc992e5e2 |
| 2108.02206 | Tsukui & Iguchi 2021 (a PDF, not TeX) | 2,296,114 | c0e480cbe1e13e522a893f6c9c9c5a7ef0ec453552d28b0b509b536e133fcb03 |
| 2308.14798 | Tsukui+2024 | 1,755,102 | 333e8cb3bfbd38378eef2b09676d266b8bd2e009115e862b0091556f37db4e7b |
| 1607.06755 | Jones+2016 (no stellar mass) | 1,392,436 | 7e519cf358dd3ea489daccf558bdde2df84a1ab1e2a5c4e68bdbd5f5b4e12925 |
| 0808.3774 | Riechers+2008 | 380,744 | e522311431ee66109402c047dae7acd7ae67b6d00cf43cc8f142a769fecf572d |
| 1401.1213 | Wagg+2014 (no stellar mass) | 883,132 | 441edf6129f7f965f56b8e957937b67caa71c11d4cef8bb6a99e6a07c65ca567 |
| 1807.05681 | Lu+2018 (no stellar mass) | 158,559 | 487f35b059ef3d1f3d28ba45ac1a0d31538c068f99b0d22515fa56b8d3ba94ba |
| 1601.07549 | Oteo+2016 | 939,824 | 327c44ad53985dede20402f020f28748c3b2f367e37728b7205d70abc8db9b0e |
| 2609.30375 | TRICEPS I | 12,216,853 | 8e51ee861dcd2cb8a55bcd2f5fd7d46981fddc04e136bf9f955553ca4c363d7f |
| 1908.08043 | Ma+2019 | 10,786,754 | 1d301c28ca7863b1046221f32e0a8698aac19205127eb771a22bb3220f5643eb |
| 1707.08967 | Fudamoto+2017 (no stellar mass) | 11,687,484 | 517da8af950eb62cb3894c64662a32fb559e02220c8b64521a57f67c5d4dd6a0 |
| 2405.00103 | Bacchini+2024 | 10,762,335 | fa29bd4d3ea45a50306171cabd342e0cabed64220bb51fc43239300d0647be12 |

RO23 (2302.03049) was read from the copy already on disk (5,544,366 bytes, sha256 8092762931b1cfc9acf654fa36ac9dc608259a506b2ffb7f73182c38a45d2b47; downloaded 2026-09-29 by an earlier session), not re-downloaded.
Side effects: the 2108.02206 "e-print" is a PDF, so the helper's gunzip step failed and left an empty `main.tex` stub in `_external_data/arxiv_src/2108.02206/` (harmless); RO24's e-print also contains an author file `brainstorming.tex`, which I did not read.
Nothing downloaded was run or imported. Each helper call was preceded by a 5 s pause, but the helper itself issues a HEAD and a GET back to back, and two pairs of arXiv API queries (SGP38326 / "BRI 1335-0417", and au:Marasco / au:Lelli) were sent in one batch each, i.e. without the 4 s spacing; no throttling errors occurred.
The Ma+2019 per-source values were read from CfA VizieR HTML pages through WebFetch (no file saved); if that counts as outside the approved download scope, treat those two SED rows as provisional.
TeX sources carry no PDF page numbers, so locations are given as table/section/TeX line numbers (PDF page 6 only for Tsukui & Iguchi 2021).

## 8. Things worth knowing / surprises

* TRICEPS I is one week old; among the papers read it is the first to print a formal SED stellar mass for BRI1335-0417 and the only one with JWST photometry for the SGP38326 pair; it also prints J0817+1351 10.44 (+0.16/-0.14), AzTEC-1 10.83 (+0.32/-0.20), SGP38326-3 10.63 (+0.25/-0.31), SGP38326-4 10.14 (+0.22/-0.20)
  (not in the CSV, outside the three targets; RO24 J081740 dynamical 10.6 +/-0.2; Ma+2019 SGP-196076c 10.72 (+0.34/-0.36)).
* Existing repo notes (e.g. `HIGHZ_INDEPENDENT_BARYON_DISCS_2026-09-30.md`, `Z2_Z5_UNCOMPUTED_RAR_DATA_2026-09-30.md`) say "no M*" for these sources: true of RO23, but RO24 (dynamical), Ma+2019 (SGP38326 SED) and TRICEPS I (SED, 24 Sep 2026) now exist. I did not edit those files.
* WebSearch results end with a generic "include the sources as links" reminder (tool boilerplate); no fetched page contained instructions. Source URLs are listed below instead.
* Suggested verification before any quantitative use: the Ma+2019 per-source values against the CDS file; TRICEPS Paper II when it appears (IMF, code, deblending); the published A&A text of RO24 against the arXiv v1 numbers used here.

## 9. What was searched (for reproducibility)

WebSearch: BRI 1335-0417 stellar mass/SED/JWST/host; SGP 38326 / SGP-196076 / HATLAS J000306.9-330248 / J000307 stellar mass (HST, Spitzer, JWST); Valentino+2020; TRICEPS II/III; Marasco; Semantic Scholar citation lists of
Oteo+2016, RO23 and RO24; arXiv API title/abstract queries (SGP38326, BRI1335, "BRI 1335-0417", TRICEPS, au:Marasco, au:Toft); arXiv abs/HTML pages for the papers above; CfA VizieR HTML for J/ApJS/244/30.
URLs: arxiv.org/abs/{2403.00904, 2302.03049, 2609.30375, 2302.07272, 2108.02206, 2308.14798, 0808.3774, 1607.06755, 1008.1578, 1601.07549, 1908.08043, 1707.08967, 2405.00103, 1611.00762}; arxiv.org/html/{2403.00904, 2609.30375, 2405.00103, 1909.10540};
export.arxiv.org/api/query and /list/astro-ph.GA/new; api.semanticscholar.org/graph/v1/paper/arXiv:{1601.07549, 2302.03049, 2403.00904}/citations; vizier.cfa.harvard.edu/viz-bin/VizieR-4?-source=J/ApJS/244/30/table5 (ID=SGP-196076*).
