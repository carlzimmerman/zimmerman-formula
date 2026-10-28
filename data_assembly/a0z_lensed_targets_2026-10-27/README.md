# Lensed rotating discs for a self-calibrated a₀ at z ≈ 1.5–2.6: archive target search (2026-10-27)

Owner-approved (2026-10-27): "run the metadata-only target search (MAST JWST IFU/NIRCam + ALMA archive coverage for lensed rotating discs at z 1.5-2.6, M_b ~5e9-2e10, V/sigma >~ 2.5)"; results are pushed as they land. **Metadata and published tables only: no data products downloaded, no law fitted, no a₀ computed.** κ = ½ FITTED; not theory closed.

**Why these galaxies.** A disc measures a₀ on its own only if its curve runs from y = g_bar/a₀ ≳ 3 (inner, fixing its own baryon scale) to y ≲ 0.3 (outer, fixing a₀) (CFG385). y = 0.3 falls at r = √(GM_b/0.3a₀): about 7 kpc for M_b ≈ 10¹⁰ M☉, and about 22 kpc for 10¹¹. Lensing supplies the resolution and the outer surface brightness.

## 1. Inputs (fetched with `../fetch_logged.py`; sha256 in `../FETCH_MANIFEST_2026-10-01.jsonl`)
arXiv e-print TeX tables (`raw/`):
- KLASS I, Mason+2017 (1610.03075)
- KLASS, Girard+2020 (2006.14633)
- OLAS I, Hirtenstein+2019 (1811.11768)
- Leethochawalit+2016 (1509.01279)
- Jones+2010 (0910.4488)
- SN Refsdal host, Di Teodoro+2018 (1801.06546; no parent rows; context)

VizieR and ar5iv are not reachable from this machine, so the TeX tables were parsed directly.

Archive queries (`query_log.jsonl`, every call logged):
- MAST `Observations.query_region` (JWST footprints containing the object, r = 2″).
- ALMA TAP `ivoa.obscore` (footprints containing the object; spectral windows tested for CO(2-1…5-4), [CI](1-0), [CI](2-1) at the object's z).

## 2. Selection (declared in `build_parents.py` before any archive query; not blind to the KLASS-I table)
- **z:** 1.5–2.6. Objects at 1.45–1.5 are kept as "near".
- **Mass:** M_b = M★/(1 − f_gas) with f_gas = 0.5, inside 5 × 10⁹ – 2 × 10¹⁰. A bracket of f_gas 0.3–0.7 counts as "bracket".
- **Rotation:** V/σ ≥ 2.5, or ≥ 2.0 counted as "near", in at least one survey.
- **Exclusions:** mergers flagged by the authors.
- **Definitions differ:** OLAS quotes (ΔV/2)/σ_local, **not inclination-corrected**; KLASS quotes intrinsic V_max (or v_rot)/σ₀. Leethochawalit and Jones give no M★, and all their objects are massive (V_c 129–570 km/s) or have V/σ < 2.

**Parents: 104 rows → 77 unique objects** (merged within 1.5″). **11 unique objects pass** (`parents.csv`, `selected.csv`).

## 3. The 11 candidates, with their archive coverage (`archive_coverage.json`)
| object (all published names) | z | log M★ | μ | V / σ (km/s) by survey | JWST in archive | ALMA cold-gas line coverage |
|---|---|---|---|---|---|---|
| **MACS1149-1501** (KLASS-I / KLASS-2020; the SN Refsdal host spiral) | 1.49 | 9.44 / 9.90 | 12.4 / 5.4 | 227/15, 208/32 | NIRCam deep (1176, 1199, 1208, 2883), NIRISS WFSS, MIRI | **CO(3-2) at 0.36″** (2013.1.00582.S); CO(2-1) 0.82″ (2017.1.00822.S) |
| MACS1149-593 / M1149-00593 | 1.48 | 9.27 / 9.41 | 2.3 / 1.5 | 142/8 (KLASS-I); 79/36 obs (OLAS) | NIRCam deep, NIRISS WFSS | CO(3-2) at 2.0″ only |
| MACS2129-1833 / -37 / M2129-01833 | 2.29 | 9.96 / 10.13 / 9.66 | 1.6 | 306/55 (KLASS-2020); 79/79 obs (OLAS) | none | [CI](1-0) 0.91″ (2025.1.00360.S, **proprietary to 2027-01-07**) |
| MACS2129-1847 / -49 | 1.88 | 9.81 / 9.80 | 1.4 | 243/98 | NIRCam (5594, 6882) | none |
| MACS2129-1539 / -329 | 1.65 | 9.92 / 9.74 | 1.7 | **132/11 (KLASS-I) vs 77/74 (KLASS-2020)** | NIRCam (5594, 6882) | none |
| MACS0416-1321 / -863 | 1.63 | 9.46 / 8.84 | 3.0 | 230/61, 191/38 | NIRCam deep, NIRSpec MSA G235M (10341) | none |
| MACS0416-394 / -880 | 1.63 | 9.93 / 9.73 | 2.2 | 76/32, 62/<34 | NIRCam deep, NIRSpec MSA G235M (10341) | none |
| A2744-1773 | 1.65 | 9.46 | 1.8 | 62/23 | NIRCam deep, NIRSpec MSA G140H/G140M/G235M/G395M (12435, 9645, 12267) | CO(2-1) at 0.71″ (mosaic, 750 s) |
| RXJ2248-1652 | 1.64 | 9.60 | 1.4 | 106/50 | NIRCam (1840) | none |
| A370-03097 | 1.55 | 9.32 | 2.3 | 67/32 obs (OLAS) | NIRCam deep, NIRSpec MSA | CO(3-2) at 1.2″ (161 s) |
| M1149-01802 | 2.16 | 9.70 | 2.4 | 132/55 obs (OLAS) | NIRCam deep, NIRISS WFSS | [CI](2-1) at 0.99″ (cluster continuum, 380 s) |

"obs" means OLAS's uncorrected (ΔV/2)/σ_local; the intrinsic V is higher by 1/sin i.

## 4. What the archive says
1. **No candidate has a JWST NIRSpec IFU observation.** The decisive two-sided outer curve does not exist in any archive. A new IFU programme is needed for every target.
2. **Stellar shapes already exist.** Deep multi-band NIRCam imaging covers 10 of 11, so the rest-frame near-IR profile ingredient is in hand. MACS2129-1833 has none.
3. **Cold-gas kinematics at sub-arcsecond resolution exist for one object only:** the SN Refsdal host (CO(3-2) at 0.36″). MACS2129-1833's [CI] data are proprietary until 2027-01-07. The other line coverages are low resolution or shallow chance coverage in cluster surveys.
4. **NIRSpec MSA spectra** (MACS0416 ×2, A2744-1773, A370-03097) give slit spectra, not 2-D velocity fields. They confirm redshifts and lines only.

## 5. Two warnings before any ranking
- **Surveys disagree on the same galaxies' kinematics.** MACS2129-1539/-329 has V/σ = 12 (KLASS-I) vs 1.0 (KLASS-2020). MACS1149-593 has 142/8 (KLASS-I) vs 79/36 observed (OLAS). Seeing-limited and AO-limited kinematics at this z are not yet reliable enough to pre-select on V/σ. That is the same lesson as arXiv:2507.10544.
- **Rotation speed vs stellar mass (hand arithmetic, not a test).** Under the law, V_flat⁴ = G M_b a₀. V ≈ 210–300 km/s (MACS1149-1501, MACS0416-1321, MACS2129-1847 / -1833) needs M_b ≈ 1.6–7 × 10¹¹ M☉, but the published M★ is 10^9.4–10^10 (lensing-corrected).
  - At M_b ≈ 2 M★, these sit ~1–1.5 dex off the baryonic Tully–Fisher relation. Some of that is the known high-z effect of V_max at small radius / high σ, M★ uncertainty through μ, and unmeasured gas.
  - **These objects are the most informative but the most dangerous.** They need measured gas (CO) and a curve that reaches the deep regime. If M_b really is ~10¹¹, y = 0.3 lies beyond 20 kpc and the self-calibrated test cannot reach it.
  - The dynamically consistent "sweet-spot" objects are those with V ≈ 90–160 km/s: MACS2129-1539 (if KLASS-I is right), RXJ2248-1652, MACS1149-593, M1149-01802 (intrinsic V likely 150+), and A370-03097 / MACS0416-394 at the low end.

## 6. Ranking for a new IFU (+ ALMA) programme (judgement, stated)
1. **MACS1149-1501, the SN Refsdal host.** *(Update 2026-10-27, CFG970: the archival CO(3-2) cube 2013.1.00582.S A1.4 does not detect CO at 1.05 mJy/beam per 2 km/s; CFG970 is INVALID as frozen and cannot decide the gas need. The "existing CO" advantage below no longer holds; a gas mass needs new ALMA time or the other pointings plus a lens model.)* It is a regular spiral, with the highest V/σ, μ ≈ 5–12, deep NIRCam and *existing* 0.36″ CO(3-2). It is the only object where a cold-gas inner curve, a stellar shape and a gas mass can all come from public data today. Caveats: z 1.49 (the H(z) lever is +0.37 dex rather than +0.5), and the V vs M★ tension of §5 must be understood first.
2. **M1149-01802 (z 2.16).** The highest z in the sweet spot, μ 2.4, deep NIRCam. Its V/σ is uncorrected, at 2.4 observed.
3. **MACS2129-1833 (z 2.29).** The highest z, and [CI] arrives 2027-01. No JWST imaging, and the surveys conflict (OLAS V/σ ≈ 1).
4. **RXJ2248-1652, MACS2129-1539, MACS1149-593:** sweet-spot V, but low μ (1.4–2.3) and conflicting kinematics.

## 7. Next steps (each needs the owner's go)
- **Download the public ALMA products for MACS1149-1501** (2013.1.00582.S, CO(3-2) at 0.36″; 2017.1.00822.S). Measure the cold-gas curve and gas mass, and settle the §5 tension for the top candidate. This needs a download (the product sizes are to be checked first).
- **Pre-register the BTFR-consistency check** for the V ≈ 210–300 km/s objects before any gas mass is read.
- **IFU programme:** NIRSpec IFU on ranks 1–3, with the two-sided-coverage and inclination requirements, plus ALMA CO for ranks 2–3.

## Files
`build_parents.py` → `parents.csv`, `selected.csv`. `query_archives.py` → `archive_coverage.json`, `query_log.jsonl`. `raw/` holds the fetched e-prints (logged).

## 8. ALMA product sizes for the SN Refsdal host (DataLink metadata, 2026-10-27; nothing downloaded)
- **2013.1.00582.S** (MOUS uid://A001/X12b/Xa; targeted; band 4; CO(3-2) at z 1.491 = 138.82 GHz inside the 138.35–139.29 GHz narrow-channel window; 0.36″; 1542 s; 0.95 mJy/beam @ 10 km/s; public since 2016-09-24).
  - The pipeline produced one CO(3-2) cube per lensed image, A1.1–A1.4: each `.image.fits` / `.pbcor.fits` is 614.7 MB, plus `.flux.fits.gz` 258 MB. There are matching CS(7-6) cubes, and continuum images of 2.5 MB.
  - Product tarball 11.9 GB; auxiliary 5.9 GB; raw ASDM 3 × ~32 GB.
- **2017.1.00822.S** (MOUS uid://A001/X12c4/X318; band-3 cluster mosaic, 178″ field; CO(2-1) at 92.55 GHz in spw27; 0.82″; 500 s; 1.3 mJy/beam @ 10 km/s).
  - The spw27 cube alone is 15.9 GB; product tarball 96.2 GB. **Not recommended:** shallow chance coverage.
- **Minimal useful download:** the A1.4 CO(3-2) pbcor cube (615 MB), optionally with its beam and continuum (+0.26 GB). All four images come to ~3.5 GB. Disk free at the time was 13 GB.

## 9. Downloaded (owner-approved 2026-10-27): A1.4 pointing of 2013.1.00582.S, outside the repo
Location: `new_physics/_external_data/alma_2013.1.00582.S_A1.4/` (not in git). Fetched with `../fetch_logged.py`; sha256 and sizes are in `../FETCH_MANIFEST_2026-10-01.jsonl`. Every file matched its advertised size; 0.876 GB in total.

| file | size | header check |
|---|---|---|
| `…MACS1149_A1.4_CO_v_0_3_2_image.pbcor.fits` | 614.7 MB | 784² × 250 ch; 0.080″ pixels; beam 0.44″ × 0.35″ (PA −7°); 2.00 km/s channels, 138.703–138.934 GHz; CO(3-2) at z 1.4906 (138.840 GHz) **inside** |
| `…MACS1149_A1.4_CO_v_0_3_2_image.flux.fits.gz` | 258.1 MB | the same grid (primary-beam response) |
| `…calibrated_final_cont_A1.4_image.pbcor.fits` / `.flux.fits.gz` | 2.5 / 1.0 MB | 151 GHz continuum; beam 0.40″ × 0.32″ |

- The KLASS position of MACS1149-1501 lies ~11″ from the pointing centre, inside the 63″ field and the band-4 primary beam.
- **Caveat before any curve:** the cube spans only ±250 km/s around 138.818 GHz, against a published V_max of 208–227 km/s. Clipping at the curve's edges must be checked.
- The fetch-manifest labels came out truncated ("…A1.4-4_image…"); this is cosmetic, and the file names and sha256 are exact.
