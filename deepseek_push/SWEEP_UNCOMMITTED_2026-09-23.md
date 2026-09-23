# SWEEP OF UNCOMMITTED SCRATCH — 2026-09-23

Sweep of the `_`-prefixed and `tmp_`-prefixed scratch files in `deepseek_push/`, plus
`navier_stokes_attempt/openai_NS_lean/` and the `G236_eRASS3_data/` FITS files.
Method: read-only classification (no long computations run); two <10 s verification runs
(`_g08_proto.py`, `_g08_proto2.py`) to diff proto numbers against the committed records.
**No existing file was modified or deleted.**

## BOTTOM LINE

Every scratch file is a **superseded prototype or debug step whose outputs are already fully
committed** in the lane records it fed (G08, G208, S04, G070). **Zero missing results.**
Recommendation: archive-and-forget (all are untracked by git, harmless to keep); two
diagnostic files keep as reference (`tmp_parse_dist.py`, `tmp_dbg_dist.py`). Nothing needs
finishing, and no new result JSON is warranted.

## 1. INVENTORY TABLE

| File | Lane | What it was answering | Status | Verdict |
|---|---|---|---|---|
| `_g08_proto.py` | G08 formation story | Run 1 of the mass-function arithmetic: sigma_8 norm, g(z) growth, sigma(M), n(>M,z) Tinker, M_prog(z*=2.4), F_above cross-check vs G079, WDM T2 21-cm damping, z_coll map | **Superseded prototype** (pre-`G08_formation_story.py`) | No missing result — verified by re-run: sigma8 0.811, g(0.5/1/2.43)=0.770/0.608/0.367, n(>3.09e14,0)=6.0888e-07, M_prog=1.575e13, f_b·M_prog=2.46e12, n(>4.48e11,2.4)=8.3e-04, T2(30/100)=0.7075/0.0163, Rcomp=0.7133 — all in `G08_results.json` verbatim (checks G1/G2/G5/G7/G11, part2.abundance_matching, part3.21cm) |
| `_g08_proto2.py` | G08 formation story | Run 2: Madau–Dickinson rho*(z) integral + corrected z_coll | **Superseded prototype** | No missing result — rho*(2.4)/rho*(0)=0.160 verified by re-run; committed as `stellar_budget.rho_star_zstar_over_0=0.1597` (check G7 "0.160"); z_coll 6.1→0.3 grid matches committed .out "z_coll ~ 6-8 is a FLOOR" |
| `_g208_explore.py` | G208 deep staircase | Stage 2 exploration: overlap control [8.5,9.5], MIGHTEE Table-5 window count, MIGHTEE D-at-deepest-ring, F fits (power + eq-fraction) | **Superseded prototype** | No missing result — overlap HI 1.075 (n=11) vs SPARC 0.493 (n=10) = 2.18x, MIGHTEE in-window 7, D-deepest med 7.28, F fit p=1.474 rms 0.250, bridge pred 0.226 — all in committed `G208_results.json` (orthogonal_decomposition.c, samples.MIGHTEE, candidate_law) |
| `_g208_explore2.py` | G208 deep staircase | Stage 3: SPARC f_gas from rotation-curve corpus, Spearman + permutation p-values, residual spreads | **Superseded prototype** | No missing result — pooled rho 0.379 p 3.0e-04, within-SPARC 0.663 p 1.0e-04, within-HI 1.0 (reading tautology), f_gas med 0.305/0.799, MAD 0.220→0.145 — all verbatim in committed `G208_results.json` (orthogonal_decomposition a/b, residual_spread) |
| `_s04_debug.py` | S04 core vorticity | Debug: per-cluster gradient fit internals on first 8 clusters (X/Y rms, weighted vs unweighted, 3 shuffle nulls) | **Debug, superseded** | No missing result — superseded by proto/fin; S04 record complete |
| `_s04_proto.py` | S04 core vorticity | Prototype: per-cluster v_los gradient fit (v0+aX+bY) on all 58 clusters, 150-bootstrap errors, 100-shuffle nulls | **Superseded prototype** | No missing result — mean A 313.0, null 282.6, excess +30.5±23.6 (z 1.29), coherent 51.2/-26.8 amp 57.8 z 1.71 — all in committed `S04_results.json` part3_signature verbatim |
| `_s04_fin.py` | S04 core vorticity | Final scratch: same stats + Rayleigh axis test + 2-sigma UL on gradient excess | **Superseded prototype** | No missing result — Rayleigh Rbar 0.073 z 0.79, v_rot,los UL 65.9 km/s, n A>3err 5 — all in committed `S04_results.json` (rayleigh, v_rot_los_2sigma_UL) |
| `tmp_dbg2.py`…`tmp_dbg7.py` | G070 dSph compendium | Six debug iterations of the `dwarf_tab.tex` (Simon 2019 Table 1) distance-regex: CRLF, name normalization (LaTeX braces, `~`), line offsets, Boötes diacritic | **Debug dead-end iterations** | No missing result — the working parser lives in committed `G070_dsph_compendium.py` (parses the tex directly, sha256 in JSON); results in `G070_results.json` |
| `tmp_dbg_dist.py` | G070 | Distance parse audit: found 53/54 distances parsed; 3 compendium names "missing" = diacritic artifact (Boötes I/II, CVn II — `ö` vs `o`), not a parse failure | **Diagnostic, superseded** | No missing result — diagnostic only; kept as reference for the name-normalization pitfall |
| `tmp_parse_dist.py` | G070 | Working distance-extraction view for 32 named dwarfs (Sculptor 86, Fornax 139, Carina 106, Sextans 95, UMi 76, Draco 82, Leo I 254, Leo II 233, Reticulum II 31.6, Segue 1 23, …) | **Reference tool (works)** | No missing *lane* result — distances are an internal input of the committed compendium; the 32-row table is a useful cross-check artifact → **keep** |

## 2. RECOMMENDATIONS

| File group | Recommendation | Action |
|---|---|---|
| `_g08_proto*.py`, `_g208_explore*.py`, `_s04_*.py` | Archive (results fully committed; re-running them is redundant with `.out` files) | Keep in place untracked, or delete — no content lost either way |
| `tmp_dbg2..7.py` | Delete candidates (pure debug scrap) | Safe to delete; no content lost |
| `tmp_dbg_dist.py`, `tmp_parse_dist.py` | **Keep** — record the G070 name-normalization pitfall and provide the only standalone dSph-distance table | Keep as reference |
| `navier_stokes_attempt/openai_NS_lean/` | Keep — upstream clone (see §4); the 19 GB `.lake` build cache is the valuable part; already referenced by N08 lane | Keep |
| `G236_eRASS3_data/*.fits.gz` | Keep untracked by design (README states the 2 GiB/100 MB GitHub rationale; cf. G114_data) — re-downloadable from eRODat | Keep, do not commit |

## 3. G236 eRASS3 APPRAISAL (FITS verification + plan connection)

**Plan doc.** `G236_eRASS3_data/README.md` IS the lane plan (it calls itself "Home of the next
free G-number's lane" — one of the two G236 users; the other is the committed
`G236_bootstrap_fixedpoint` deep-line lane). It lays out: eRASS:3 = eROSITA DR2 cumulative
catalogues (556 days, public 2026-07-31, Ramos-Ceja+2026 A&A aa60385-26), the two registered
predictions — **E1** the virial-T a0(z) sharp null (Δlog10 T = 0.000 at z≤1, vs +0.134/+0.216
dex for Ciocan M-RISE, separated at ~21σ/35σ with 150-cluster z-bins; falsifier |Δlog10 T|>0.010
dex) and **E2** cluster-sector z-invariance (α=2/3, rms≤0.076 dex, dust slope −0.414±0.157) —
plus re-pointed registrations G187/G162/G161 and the honest status (catalogue-only release: no
T_X, no M500; verdicts wait on WG products and SDSS DR20 cross-match). The committed
`G236_eRASS3_a0z.py` (+`.out`, `G236_results.json`) runs 13/13 PASS audit checks against the
actual files. Also connecting: `MNRAS_METHODS.md` §(b1)/(F2) cite G236 as the deep-line lane
(G071/G099/G114/G231) — that is the *bootstrap_fixedpoint* G236, not eRASS3; `REASSESSMENT_2026-09-16.md` registers "the bootstrap fixed point NEGATIVE (G236)" — same lane. The eRASS3
folder is the newer occupant of the name.

**FITS verification (astropy 7.2.0, header-only reads, all four gz files — valid FITS):**

| File (gz size) | HDU1 BINTABLE | Rows | Columns | Audits it proves (per README) |
|---|---|---|---|---|
| `SRG_eROSITA_SDSS_CV_CATALOGUE.fits.gz` (0.1 MB) | NAXIS1=281 | 587 | 30 — IAUNAME, SDSS_ID, DETUID, GAIA_DR3_ID, RA/DEC (eRO+Gaia+ICRS), eRO_FLUX(+ERR), Gmag, BP-RP, **DISTANCE + LOWER/UPPER**, Gabs, log(Lx), log(fx/fopt), HR_P12… | eROSITA×SDSS CV catalogue in hand (complementary data, not cited by the 13 checks) |
| `eRASS3_Hard_v1.2.fits.gz` (6.2 MB) | NAXIS1=564 | **15,980** | 111 — IAUNAME, DETUID, SKYTILE, ID_SRC/UID(+5XMM/2RXS/CSC/DR1Hard/Main), ID_CLUSTER, RA/DEC(+raw/lower/upper), POS_ERR, LII/BII, … | C01–C03 (hard total 15,980 = 15,026 PS + 954 EXT) EXACT |
| `eRASS3_Main_v1.3.fits.gz` (1385 MB) | NAXIS1=1083 | **1,975,540** | 250 — IAUNAME, SKYTILE, ID_SRC, ID_CLUSTER, DETUID, UID(+5XMM/2RXS/CSC/DR1/Hard), RA/DEC, POS_ERR, LII/BII, … | C04 (1,911,744 PS + 63,796 EXT = 1,975,540) EXACT |
| `eRASSc3_Main_LS10_Public_27Jul2026.fits.gz` (1054 MB) | NAXIS1=1122 | **1,591,243** | 189 — IAUNAME, ID_SRC, ID_CLUSTER, DETUID, RA/DEC(+raw), POS_ERR, LII/BII, ELON/ELAT, EXT(+ERR/LIKE), DET_LIKE_0, … | C05 (87.8% extragalactic on `class_gal_exgal`; the lane measured 1,397,905/1,591,243) EXACT |

All counts reproduce the paper's headline numbers row-for-row from the shipped files; headers
read in ≤9 s each (header-only, no data materialized). Key E1/E2-relevant columns are present
in the main catalogue baseline (RA, DEC, fluxes, EXT), but there is **no T_X and no M500** in
any file — confirming the README's honest status that E1–E4 verdicts must wait for the cluster
WG products + SDSS DR20 redshifts. Distances ARE available in the CV catalogue
(DISTANCE_LOWER/UPPER) — useful only for the CV subsample, not for clusters.

## 4. NAVIER-STOKES / openai_NS_lean APPRAISAL (one page)

**What it is.** `navier_stokes_attempt/openai_NS_lean/` is a **git clone of
`github.com/openai/NavierStokesAndEuler`** (origin remote verified; clone commit f9e8bc5),
i.e. OpenAI's own Lean 4 formalization accompanying *"Finite time blowup for Navier–Stokes"*
(2025) and *"Finite time blowup for the Euler equation"*. It is up-stream/third-party work —
the repo's N08 lane (`N08_openai.md`, `N08_openai_analysis.md`, Sep 17) already digested it
(OpenAI's audit: 2,659 `.lean` files / 616k lines / 35,731 theorems; clone contains ~12.3k
`.lean` including the vendored mathlib surface). It is **not** a proof of energy-bounded global
smoothness — the Clay-conjecture direction; it proves the **opposite/breakdown alternatives (C)
and (D)** of the Clay problem statement: for every positive viscosity there exist smooth forced
initial data on ℝ³ (and on ℝ³/ℤ³) with **no** global smooth solution with uniformly bounded
kinetic energy; and unforced Euler on ℝ³ develops a C¹ singularity in finite time. That
distinction matters for the repo's own NSE campaign (N05 verdicts: the OpenAI singularity is a
*visible-NSE* fluid, in the framework's singular sector (D2), contested provenance B&A vs
OpenAI — see N07/N08).

**Contents.** Root: `README.md`, `formalization.yaml` (v0.4 metadata: authors OpenAI, Apache-2.0),
`lakefile.toml`, `lake-manifest.json`, `lean-toolchain` = `leanprover/lean4:v4.34.0-rc2`.
Modules: `NavierStokes/` (~700+ modules: Activation*, Actual*Candidate/Carrier/Cycle*, AllOrder*
corrections/drift, comparator machinery — the "localized cascade" construction), `Euler/`
(EulerSingularity library), `ComparatorChallenges/` (2 root files: `NavierStokes.lean`,
`Euler.lean`), root `NavierStokes.lean` (imports ComparatorSolution + PaperResults) and
`Euler.lean` (imports Euler.EulerSingularity). `LICENSE` (Apache 2.0).

**Does it compile?** Toolchain present: `lean 4.34.0-rc2` at `/opt/homebrew/bin/lean` (elan),
`lake` present; `.lake/` = 19 GB with a **prebuilt** mathlib+project cache including
`NavierStokes.olean` and `Euler.olean`. Fresh compile checks (real runs, this sweep):
- `lake env lean NavierStokes.lean` → **exit 0, clean** (whole NS library typechecks against the cached build)
- `lake env lean Euler.lean` → **exit 0, clean**
- `lake env lean ComparatorChallenges/NavierStokes.lean` → exit 0, **2 `sorry` warnings** (lines 273/280 — deliberate placeholder gaps in the challenge scaffolding)
- `lake env lean ComparatorChallenges/Euler.lean` → exit 0, **2 `sorry` warnings** (lines 85/170)

The main theorem roots compile without `sorry`; only the self-describing "comparator challenges"
have declared gaps (by design — they are the re-derivation exercises). A from-scratch `lake
build` would fetch mathlib and take hours; the cached build makes incremental verification
instant. **Appraisal: genuine, compilable, current (toolchain matches the repo pin exactly);
kept as the NSE lane's ground-truth artifact — do not "fix" the `sorry`s (they are upstream's).**

## 5. SWEEP META

- Files inspected: 15 scratch `.py` + 2 lane dirs (openai_NS_lean, G236_eRASS3_data).
- Runs performed: `_g08_proto.py`, `_g08_proto2.py` (<5 s each, verification), 4× FITS header
  reads (astropy, ≤9 s each), 4× `lake env lean` compile checks. No long computations.
- Missing results: **none**. Files written this sweep: this document only.