# EUC10 (PUBLISHED SOURCE REDSHIFTS): FROZEN CRITERIA

Committed alone, before any script of this lane exists, before any literature table or NED row at a lens position is
fetched for matching, and before any matched redshift or graded number is seen. 2026-11-12.

κ = ½ FITTED; not theory closed. Footings 9.3603e-11 (canonical) / 1.132e-10 (alt) m/s², graded separately, never
pooled. One-sided: no outcome is a pass of the theory; a favourable reading awaits an independent re-grade. Adopts
nothing.

## 0. Question

Euclid DR1's ECLIPSE catalogue has no lensed-source redshifts. EUC1 froze gate EUC1-F (`../EUC1_eclipse_saturation_ceiling/RESULT.md`
§8) and EUC5 sealed forecast EUC5-F (`../EUC5_dynamical_boost/RESULT.md` §3c) for the day source redshifts exist. This
lane collects spectroscopic lensed-source redshifts **already published by others** for systems in the ECLIPSE
catalogue and grades both exactly as frozen. Neither gate is redesigned here.

## 1. Lens list (frozen; read-only)

`_external_data/euclid_dr1_eclipse/ECLIPSE_object_catalogue.csv` (all 26,662 rows, any grade) and
`eclipse_dr1_catalogue_key_v20261103.csv`, hash-checked by EUC1's `load()`. Samples P and S are EUC1's `select()`
(P: grade A + model success + final sample + no large-system warning + valid inputs, N = 3,192; S: the same with
grades A+B, N = 6,173). EUC1's machinery is imported, not rewritten (`euc1.py`: `load`, `select`, `build`, `run_b`,
`stats`, `FOOT`, `EUCLID`).

## 2. Sources of published redshifts (frozen list; one paced stream per service, ≥ 1 s apart, generic User-Agent,
stop on HTTP 429; no personal detail in any request)

Not queried at all: IRSA, ESA Euclid TAP, NOIRLab SPARCL (in use by other lanes). CDS Strasbourg (VizieR TAP,
SIMBAD) returned "page unavailable" / timeouts on 2026-11-12 before freezing; VizieR is used through the CfA mirror
(`vizier.cfa.harvard.edu`, ASU tsv). If SIMBAD returns during the lane it is queried as route R1b below; if not, that
is reported as not done.

- **R1 NED TAP** (`ned.ipac.caltech.edu/tap/sync`, table `NEDTAP.objdir`): every one of the 26,662 ECLIPSE positions,
  10″ cones, batched 60 cones per query with OR'd `CONTAINS`. Columns: prefname, prefphytype, ra, dec, z, zflag,
  z_bibcode.
- **R1b SIMBAD TAP** (only if reachable): same positions and radius, objects of type gravitationally lensed image
  (`LI`, `LeI`, `LeQ`, `gLe`, `gLS` or the equivalent otype labels) with a redshift.
- **R2 VizieR (CfA mirror)**: for each catalogue below that exists, the table metadata is read and, if a column holds
  a spectroscopic source redshift, the full table is downloaded. Fixed list: SL2S J/ApJ/777/97; SuGOHI II
  J/ApJ/867/107, V J/MNRAS/495/1291, VIII J/PASJ/74/1209; SQLS J/AJ/143/119; Lemon+2023 J/MNRAS/520/3305;
  DES bright arcs J/ApJS/259/27; Diehl+2017 J/ApJS/232/15; Rojas+2022 J/A+A/668/A73; Jacobs+2019 J/ApJS/243/17 and
  J/MNRAS/484/5330; Huang+2021 J/ApJ/909/27; Cañameras+2020 J/A+A/644/A163; Shu+2022 J/A+A/662/A4; Petrillo+2019
  J/MNRAS/484/3879; Cañameras+2021 J/A+A/653/L6; SGAS J/ApJS/247/12; plus a `-meta` probe of the J/ identifier implied
  by every other `earliest_publication_bibcode` in the ECLIPSE catalogue (44 distinct values) and of Gaia GraL /
  lensed-quasar compilations found by the same probe.
- **R3 primary literature tables** (arXiv e-print source, LaTeX tables as published; for the Euclid DR1 paper the PDF
  from `pubs.euclid-ec.org`, text extracted locally, not through a summarising fetch): AGEL DR1 (Tran+2022,
  arXiv 2205.05307); AGEL DR2 (Barone+2025, 2503.08041); AGEL environments (2602.11068) and AGEL double source planes
  (2509.15012) if they carry redshift tables; DESI Strong Lens Foundry II (2509.18089), III (2509.18086), IV
  (2509.18078); HSC lenses confirmed with DESI I (2505.16158); DESI-253.2534+26.8843 (2307.12470); Euclid Q1 Strong
  Lensing Discovery Engine A (2503.15324); eBOSS spectroscopic lens candidates (Talbot+2021, 2007.09006); MaNGA
  spectroscopic lens candidates (Talbot+2022, 2206.09902); Gaia GraL X catalogue (2603.12810); Lensed quasars in
  Gaia II, III, IV (1803.07601, 1810.04480, 2206.07714); DES meets Gaia (1711.03971); Gaia GraL VI (2012.10051);
  Bergamini et al., Euclid DR1 NISP spectroscopy of gravitational arcs (`pubs.euclid-ec.org/public/dr1/bergamini.pdf`,
  Table 1).
- Any further source found while reading the above (a cited follow-up table) may be added only before the
  cross-match is run, and is listed in the RESULT as "added during collection".

Fetched data: `_external_data/euc10_published_source_z/` with `MANIFEST.txt` (URL or query, bytes, sha256, date,
licence). Never added to git. Cap 200 MB.

## 3. Purity rule (frozen)

A redshift counts only if **a publication identifies it as the spectroscopic redshift of the lensed background
source of that system**. Recorded per entry: paper, table, row (or NED object name and z_bibcode), the paper's quality
flag, match separation.

- Photometric source redshifts never count; neither do redshifts the paper marks tentative, uncertain, "?" or below its
  own secure class (each paper's secure class is recorded as read from its table notes).
- NED (R1): an object counts if `zflag` begins with `S` (spectroscopic) **and** its type is `G_Lens` or `Q_Lens`
  (NED's own identification as a lensed image). A spectroscopic NED redshift on an object not so typed, more than 0.1
  above the lens redshift, is a **pointer** only: it counts if its `z_bibcode` paper (or another publication) identifies
  it as the lensed source; read from a summarising fetch it is **PROVISIONAL** (§6).
- A source redshift must exceed the lens redshift the publication gives (or the DESI deflector redshift, or the
  ECLIPSE photo-z if neither) by more than 0.05; otherwise it is the deflector and is discarded.
- Several sources in one system: the paper's primary (first-listed / brightest-arc) source; if the paper does not
  say, the lowest secure source redshift. Reported both ways if they differ by more than 0.1.
- Conflicts: two secure values for one system differing by more than 0.02 → the lens is excluded and listed.
- A value used in a gate must come from a machine-readable table (VizieR, NED, a LaTeX/PDF table of the publication
  read locally) **or** be confirmed in two independent places. Otherwise the lens is PROVISIONAL and each gate is
  reported with and without the PROVISIONAL lenses (the word is the one without).

## 4. Match (frozen)

- Literature tables and VizieR rows giving a lens / system position: matched to `RA_obj, DEC_obj` within **5″**;
  nearest ECLIPSE row wins; ties reported.
- NED objects (image positions): within **10″** of `RA_obj, DEC_obj`.
- Positions only as names: decoded; if the name's precision is coarser than 2″ (e.g. `JHHMM±DDMM`), the match is
  accepted only if exactly one ECLIPSE row of any grade lies inside the name's precision box, and is PROVISIONAL.
- **Null (shifted positions).** Every match is repeated with every ECLIPSE position moved +0.3° in declination (NED: a
  second full set of cones at the moved positions). Accepted source redshifts at moved positions must be
  ≤ max(2, 10 % of the real count). If the null fails, the lane is NOT EVALUABLE.

## 5. Statistic and words (frozen; copied from the gates, not changed)

b_i = log₁₀ of the Salpeter stellar-mass boost law S needs for lens i at its true source redshift: EUC1's `run_b`
with `z_s` in place of `ZS_INF`; lens redshift = ECLIPSE `eclipse_median_phz` (EUC1's model, §3 of its criteria);
lenses with `z_l ≥ z_s − 0.2` are dropped and counted (EUC1's conditional-reading rule, as EUC3 used it). Bootstrap
2,000 resamples, seed 20261112 (EUC1's `stats`).

- **EUC1-F** (sample P, law S, per footing, N ≥ 10 else **NOT EVALUABLE**): **LENS GATE HOLDS** if the upper 95 %
  bound of b_med ≤ 0.15; **LENS GATE FAILS** if the lower bound ≥ 0.25; otherwise **NO VERDICT**.
- **EUC5-F** (sample S, law S, per footing, per class of `eclipse_effective_einstein_radius`; N ≥ 10 per class else
  that class **NOT GRADED**): bands canonical / alt: θ_E < 1.0″: −0.19 to +0.22 / −0.19 to +0.21; 1.0–1.3″: −0.05 to
  +0.30 / −0.06 to +0.34; ≥ 1.3″: +0.03 to +0.32 / +0.03 to +0.31. **LENSING EQUALS DYNAMICS** if the class median's
  95 % interval overlaps the band; **LENSING EXCEEDS DYNAMICS** if its lower bound is above the band; **LENSING BELOW
  DYNAMICS** if its upper bound is below.

**Readings (labelled, not gates):** b_med on sample S; on all matched lenses with valid EUC1 inputs; the same at the
DESI deflector redshift where present (stellar mass rescaled by D_L², as EUC1 robustness 4b; guard z_l < z_s − 0.05);
law B beside law S. Matched lenses against P: medians of θ_E, z_l, log M★, Sérsic n, θ_E/θ_e, with a statement of what
the selection does to the reading.

## 6. Known answers and checks (frozen; a failure of KA1, KA2, MUT or NULL makes the lane NOT EVALUABLE)

- **KA1** SLACS `real_research/data/slacs_auger2009_lenses.tsv` through EUC1's K5 path: b_med at true z_s
  = +0.082 / +0.070, to 0.003.
- **KA2** L015763 at z_s = 1.3657, DESI deflector redshift with mass rescaled (EUC3's K2 path): b = +0.231 / +0.215 to
  0.002 (1.70 × / 1.64 × Salpeter).
- **KA3** If Bergamini et al. Table 1 (or any table) is fetched, the cross-match must return z_s ≈ 1.366 for
  EUCL-DR1-L015763. If no fetched table contains it, the RESULT says so in its first paragraph.
- **KA4** EUC1 reproduced: N(P) = 3,192, source-free b_med −0.019 / −0.044 to 0.001.
- **MUT** `EUC10_MUTATE=newton` (a₀ → 10⁻³⁰): b_med on the matched P lenses (or all matched, if P has none) must rise
  on both footings and the script must exit 1. Outputs under a separate name.
- **NULL** §4.

## 7. Part B: population reading (NOT A GATE; never called EUC1-F)

For each imaging-selected lens sample collected with spectroscopic source redshifts and N ≥ 20 secure systems with
lens and source redshift (expected: AGEL DR1+DR2 as one survey, DESI SLF II, HSC/DESI I, SL2S; lensed-quasar and
spectroscopically selected samples are excluded), separately:

- If ≥ 80 % of its rows give θ_E, match on (z_l, log θ_E) with scales 0.1 and 0.1 dex; else on z_l alone (labelled).
- For each lens of P: the k = 10 nearest systems of that sample in the scaled space; draw one at random; keep its z_s
  if z_s > z_l(P lens) + 0.2, else redraw (≤ 20 tries, else that lens is dropped from the realisation).
- 200 realisations, seed 20261112; per realisation b_med (law S) per footing; report the median and 2.5–97.5 % range
  per sample and footing. The **bracket** is the lowest to highest per-sample median.
- Limits stated in the RESULT: ground-based selection (brighter, wider arcs), the spectroscopic redshift desert
  (1.5 ≲ z ≲ 2.5 under-represented for optical spectra), different depth from Euclid, z_l matched only through the
  photo-z of P.

Reference points on the record (orientation only): EUC1 conditional b_med +0.146 / +0.125 at z_s = 3 and +0.232 /
+0.213 at z_s ≈ 2; SLACS +0.082 / +0.070.

## 8. Disclosure: seen before freezing

- This lane's brief, including the lead's **unverified hand estimate**: row-level overlap 5–30 lenses; b_med at true
  source redshifts between +0.2 and +0.3; likeliest words NOT EVALUABLE or NO VERDICT. Not used for any choice above
  except that N ≥ 10 and the bands are copied from the gates.
- EUC1, EUC2, EUC3 and EUC5 RESULT files (all numbers there, including EUC3's void readings +0.251 / +0.236 on 18 P
  systems), EUC1's code, the ECLIPSE README, and the release review's note that Bergamini et al. give
  z_s = 1.366 ± 0.008 for PS1J1821+7130 and that the ECLIPSE paper has 20 DESI lens/source pairs without row-level
  linkage.
- Distribution of `earliest_publication_bibcode` (642 rows with a bibcode, 44 distinct).
- Service probes: NED TAP schema; NED cones at three famous lenses outside ECLIPSE (Q2237+0305, Cosmic Horseshoe,
  SDSS J1004+4112) to learn NED's type codes (`G_Lens`, `Q_Lens`; the Horseshoe source is typed `G`, so typing is
  incomplete); one batched NED query of 60 random ECLIPSE positions **moved +0.5° in Dec** (timing test; first rows
  only, no lens-typed object); and **one NED cone at EUCL-DR1-L015763's own position (3″ radius), which returned a single
  WISE galaxy with no redshift**: so NED does not carry the published 1.366 within 3″. That is the only real-position
  look made.
- VizieR `-meta` probes of the identifiers in §2 (which exist on the mirror; no table rows read); arXiv API title
  searches (titles and identifiers only).
