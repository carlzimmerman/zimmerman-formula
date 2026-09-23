# M03 — Cluster Evidence Re-Audit (shipped eRASS:3 catalogue): is the evidence right?

**Lane:** `M03_cluster_audit.py` → `M03_cluster_audit.out`, `M03_results.json` (this directory)
**Audited files (untracked on disk, `deepseek_push/G236_eRASS3_data/`):**
`eRASS3_Main_v1.3.fits.gz` (1,975,540 rows × 250 cols), `eRASS3_Hard_v1.2.fits.gz` (15,980 × 111),
`eRASSc3_Main_LS10_Public_27Jul2026.fits.gz` (1,591,243 × 189), `SRG_eROSITA_SDSS_CV_CATALOGUE.fits.gz` (587 × 30).
**Method:** independent re-read of the shipped files only — headers + cheap column slices (`memmap=True`),
never the full 2.3 GB tables. Every number below was measured by this lane; nothing copied from G236 outputs.
**Result:** `M03 COMPLETE: 18/19 checks PASS.` — all 13 G236 gates **RE-VERIFIED**; E1/E2 verdicts registered
honestly as **NOT-TESTABLE-WITH-SHIPPED**; one new strict cross-file check fails on raw counts and is
**RESOLVED** by a DETUID join (duplicate counterpart rows, zero classification flips).

---

## Part 1 — Independent re-verification of the 13/13 G236 gates

| G236 gate | audit status | exact numbers measured here |
|---|---|---|
| C01 hard total = 15,980 | RE-VERIFIED | 15,980 = header NAXIS2 = data length |
| C02 hard EXT = 954 | RE-VERIFIED | EXT_LIKE>0 → 954 (cut sensitivity: EXT_LIKE>10 → 911) |
| C03 hard PS = 15,026 | RE-VERIFIED | 15,026 (= 15,980 − 954, also measured to equality) |
| C12 hard EXT census registry | RE-VERIFIED | 954 hard-band extended sources in hand |
| C04 main 1,911,744 PS + 63,796 EXT | RE-VERIFIED | 1,975,540 rows; EXT_LIKE>0 → 63,796; EXT>0 → 63,796 (two criteria agree); EXT_LIKE>10 → 23,219 (criterion-sensitive) |
| C13 EXT vs PS |b| KS | RE-VERIFIED | D = 0.04598 vs 95% crit 0.00547 → **8.4×**; scipy ks_2samp p = 7.1e-114; frac \|b\|<10°: EXT 0.154 vs PS 0.122 — identical to G236's numbers |
| C05 LS10 ~88% extragalactic | RE-VERIFIED | 1,397,905/1,591,243 = **0.8785** (class_gal_exgal ≥ 1); cross-check Class_STAREX>0 → 0.1243 (stricter codebook, reported for honesty) |
| C06 E1 arithmetic (Δlog10 T_X) | RE-VERIFIED (registration) | framework −0.0000/−0.0000 dex (z=0.5/1); M-RISE +0.1335/+0.2155; (1+z)^1.5 +0.132; σ_bin = 0.076/√150 = 0.0062 → 22σ @ z=0.5 / 35σ @ z=1. Verdict on the physics: PENDING — no T_X in any shipped file |
| C07 E2 constants | RE-VERIFIED (registration) | α=2/3; rms floors 0.076 (local) / 0.100 (z>0.2 falsifier); q = −0.414±0.157 — internally consistent; NOT-TESTABLE-WITH-SHIPPED (below) |
| C08 E3 G187 / C09 E4 G162 / C10 NON-CLAIM / C11 G161 | RE-VERIFIED (registrations) | thresholds registered; all PENDING WG mass products; the 2.4× eRASS1 ratio needs the eRASS1 file (not shipped) |

**New cross-file check (not in G236):** LS10's own `EXT_LIKE` column counts 65,645 EXT rows vs Main's 63,796.
Raw equality **FAILS** (A09). DETUID join (A09b, **PASS**):
all 1,591,243 LS10 rows match Main detections (0 outside, 0 Hard-only), **0/1,591,243 classification flips**,
LS10 holds 130,951 duplicate counterpart rows (1,460,292 unique DETUIDs), of which 1,849 sit on EXT
detections → 65,645 = 63,796 + 1,849 exactly. **Main v1.3's 63,796 EXT census is confirmed twice over;
naive use of LS10 row counts for the EXT census would be wrong.** No G236 claim is touched.

## Part 2 — The named-pain audit: what is ACTUALLY measurable now for E1?

E1 is a virial-temperature null — Δlog10 T_X(z)/T_X(0)|_{M_b} = 0.000 vs M-RISE +0.134 dex @ z=0.5.
**Column census of all four shipped files (header-level, quoted):**
- MAIN/HARD: **zero** columns matching redshift/T_X/M500 patterns out of 250/111 names. Catalogue-only confirmed.
- `SRG_eROSITA_SDSS_CV_CATALOGUE.fits.gz`: a **cataclysmic-variable** cross-validation list (587 CVs
  with CV_TYPE ∈ {AM_CVn, DN, NL, Nova, mCV…}) — not a cluster/redshift product.
- LS10: only `redshift_simbad` (+err) — comment literally "Redshift from Simbad **(not always reliable)**";
  no photometric-z column among the 189 names; `id_bzcat`/`class_jetted` are blazar flags.

**Decisive E1 number cannot be formed**: needs T_X + M500 + z. What the catalogue CAN constrain
(all measured, Part 1 + 3):
1. **Class fractions across the two main catalogues**: Main 63,796/1,975,540 = **3.229% EXT**; Hard
   954/15,980 = **5.970% EXT**; ratio **1.85×** — the hard band is ~1.85× more extended-rich.
2. **Population-split quantified**: KS 8.4× above critical, p=7e-114; plane excess frac |b|<10:
   EXT 0.154 vs PS 0.122.
3. **87.8% extragalactic reproducible from shipped columns** — yes (Part 1 C05), on `class_gal_exgal ≥ 1`.

## Part 3 — z-invariance at catalogue level + E2 testability

**Measurable proxy (raw EXT census sector stability, within eRASS3_Main):**
- |b| sectors: 0-10°: **4.04%** (9,844/243,367); 10-20°: 2.56%; 20-40°: 3.46%; 40-90°: 3.04% → spread **1.49 pp**.
- l sectors (30°): populated only l∈[150,360] (footprint: **l<150° EMPTY — 5 zero-source bins**);
  fractions 2.61–3.81% → spread **1.20 pp**, i.e. longitude-stable at ~1 pp while |b|-dependent.
  → The raw EXT census is NOT sector-invariant (by design: Galactic plane SNR/star-forming contribution).
  This is a catalogue-context statement, **not** a test of E2.
- **E2 pre-registration (rms ≤ 0.076 dex, α=2/3 at 0.2≤z≤1): NOT-TESTABLE-WITH-SHIPPED.**
  Needed to test: per-cluster T_X (or T500), M500, redshift z∈[0.2,1] to fit the α-slope and pooled rms.
  **No shipped column suffices** (census Part 2). Closer: eRASS:3 cluster WG products (T_X, M500, z)
  and/or SDSS DR20 spec-z + X-ray spectral fits.

**Sparse z-candle (only z info in any shipped file):** LS10 `redshift_simbad` → 116,524 rows with z>0
(7.32% of LS10): z∈[0,0.1): 41,726; [0.1,0.3): 12,226; [0.3,0.6): 10,682; [0.6,1.0): 15,774;
[1.0,2.0): 25,561; ≥2: 10,555; blazar-flagged/jetted 1,207. Simbad-curated (AGN/blazar-heavy, biased) —
**not a cluster sample; no E1/E2 verdict can be drawn from it.**

## Part 4 — Verdict table (claim | status | numbers | closer)

| Claim | Audit status | Exact numbers (this audit) | External product that closes it |
|---|---|---|---|
| Hard catalogue 15,980 rows (A&A T2) | RE-VERIFIED | 15,980 (NAXIS2 = data length) | closed; paper Table 2 |
| Hard EXT 954 / PS 15,026 | RE-VERIFIED | EXT_LIKE>0 → 954/15,026 (EXT_LIKE>10 → 911) | closed; paper Table 2 |
| Main 1,911,744 PS + 63,796 EXT | RE-VERIFIED | 1,975,540 rows; EXT_LIKE>0 and EXT>0 both → 63,796 | closed; paper Table 2 |
| EXT vs PS sky populations differ (KS) | RE-VERIFIED | D=0.04598 = 8.4× critical (p=7e-114) | closed; measured from shipped BII |
| LS10 ~88% extragalactic | RE-VERIFIED | 0.8785 (1,397,905/1,591,243) | closed; paper T10, same column semantics |
| Cross-file EXT census (LS10 copy) | RE-VERIFIED (delta resolved) | 65,645 = 63,796 + 1,849 duplicate-EXT rows; 0 flips on 1,591,243 shared rows | closed; Main v1.3 census confirmed twice over |
| E1 Δlog10 T_X = 0.000 (z≤1) virial-T null | NOT-TESTABLE-WITH-SHIPPED | no T_X/M500/z in MAIN/HARD/CV; LS10 only sparse Simbad z; rival amplitudes re-derived (+0.1335/+0.2155 dex, 22/35σ) | eRASS:3 WG products (T_X, M500, z) + SDSS DR20 |
| E2 z-invariance rms ≤ 0.076 dex | NOT-TESTABLE-WITH-SHIPPED | needs T_X(z), M500, α-fit, pooled rms; no shipped column suffices | eRASS:3 WG products + SDSS DR20 |
| G187/G162/G161 eRASS legs | NOT-TESTABLE-WITH-SHIPPED | need M500 (and f_dust) | eRASS:3 WG mass products |
| ~200,000 SDSS DR20 spec-z sources | NOT-TESTABLE-WITH-SHIPPED | no spec-z column in MAIN/HARD; LS10 Simbad-z only | SDSS DR20 cross-match release |
| Tens of thousands of clusters to z>1 | NOT-TESTABLE-WITH-SHIPPED | no cluster z in any shipped file | eRASS:3 WG cluster catalogue |
| eRASS:3 = 2.4× eRASS1 extended | NOT-TESTABLE-WITH-SHIPPED | 63,796 EXT in hand; eRASS1 file not shipped | eRASS1 DR1 catalogue |
| EXT fraction sector stability (audit finding) | MEASURED (context) | |b| 4.04/2.56/3.46/3.04%; l 30° spread 1.20 pp vs |b| 1.49 pp; l<150° empty | n/a |
| EXT/PS class fractions Main vs Hard (audit finding) | MEASURED (context) | Main 3.229% vs Hard 5.970% (ratio 1.85×) | n/a |

**Bottom line:** every headline number the G236 lane carried is right on the shipped files; the E1/E2
verdicts remain PENDING by design, and they cannot be advanced by any shipped column — the register
"NOT-TESTABLE-WITH-SHIPPED" is the honest audit status until the cluster WG products / SDSS DR20 land.
No fabrication; no git commit; all numbers from the shipped files (see `M03_cluster_audit.out`).