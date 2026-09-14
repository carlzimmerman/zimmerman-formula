# G044 — PRE-REGISTRATION (frozen 2026-09-14 18:06 EDT, BEFORE any residual/slope/offset is computed)

Lane: G044, the 438-galaxy unified HI corpus extension (zenodo.20695697, Flynn 2026, v7.0).
Extends G036 (the radial scatter function). Verdicts below are frozen before the data
touching. Every check states measurement and threshold separately. FAILs are findings.

## What was inspected before this registration (declared openly)

Schema inspection ONLY — no residual, slope, offset, or scatter number has been computed:
- Corpus structure: 438 galaxies, `galaxies` list, unified `data` rows (Rad, Vrot/Vobs).
- Survey counts with data: SPARC 175 (Tier 1), THINGS 19 (+15 metadata-only), LITTLE_THINGS 26 (Tier 1), WALLABY 203 (Tier 2).
- Per-ring columns: SPARC carries Vgas/Vdisk/Vbul + errV; THINGS/LITTLE THINGS carry Rad/Vrot/errV ONLY (NO baryon decomposition); WALLABY carries Rad/Vrot/Vdisp ONLY (NO uncertainties, NO masses).
- No stellar-mass metadata exists anywhere in the corpus (key census across all 438 records).
- Bit-identity control: corpus SPARC rows == local SPARC `_rotmod.dat` files on all of
  Rad/Vobs/Vgas/Vdisk/Vbul (max abs diff = 0.0, 175/175 galaxies).
- Crossmatch (structural): 13 THINGS + 3 LITTLE THINGS curves are SPARC galaxies
  (union = 14 unique galaxies; NGC 2366 and DDO 154 appear in both HI surveys).
  gext_vectors.csv matches 175/175 SPARC + 13 THINGS + 3 LT (same 14 galaxies, 16 curves).
  gext_wallaby_237.csv (repo-committed 2M++/MCXC table) matches 203/203 WALLABY.
- e_N axis distributions (structural, no residuals involved):
  gext_vectors cols[4] ("log_eN_noclu"; this is the column G036 actually consumed — its
  printed stats, median 4e-4 / max 0.0048, match noclu, not maxclu; G036's header comment
  mislabeled it): median 3.8e-4, p75 5.4e-4, p90 7.1e-4, max 4.8e-3.
  gext_vectors cols[5] ("log_eN_maxclu"): median 3.3e-3, p75 4.5e-3, max 3.9e-2.
  gext_wallaby_237 eN_maxclu_can936: median 4.2e-3, p75 7.7e-3, p90 2.3e-2, max 0.119.

## Registered sample definitions

- TIER-1 EXTENDED analysis set: all Tier-1 curves that admit a baryon model = 175 SPARC
  (own Vgas/Vdisk/Vbul; M/L disk 0.5, bulge 0.7, the repo's standing convention) + the 16
  crossmatched THINGS/LITTLE THINGS curves (14 unique galaxies; baryon model INHERITED
  from the galaxy's SPARC row, Vb2(r) linearly interpolated onto the HI curve's radii;
  both HI curves of a duplicated galaxy kept — independent measurements, shared model).
  Total: 191 curves / 189 galaxies.
- EXCLUDED (honest scope note): 6 THINGS + 23 LITTLE THINGS curves with no SPARC
  crossmatch — no baryon decomposition exists for them in this corpus; they enter NO
  M_b-dependent test. 45 Tier-1 curves total, 29 excluded.
- TIER 2 (WALLABY, 203): NEVER pooled with Tier 1. No masses -> excluded from ALL
  M_b-dependent tests (RAR residuals, r/r_M, BTFR). No corpus environment metadata ->
  environment from the repo's committed gext_wallaby_237.csv (2M++/MCXC, Chae-convention
  e_N at the canonical a0), 203/203 crossmatched by design.

## Registered verdicts (frozen now)

E1 (ingest integrity): corpus loads with 438 galaxies / 8,963 total rotation points;
  SPARC rows bit-identical to the repo rotmod set; tier labels 175/45/203 intact.
  Threshold: all three counts exact, bit-identity exact.

V1E (the G036 decomposition on the EXTENDED Tier-1 set, BOTH clauses together):
  (a) within-galaxy white-noise floor stays <= 0.06 dex — deep regime (r/r_M > 2),
      per-point residuals after removing each galaxy's own deep-regime mean offset,
      pooled rms; (b) the sag sign persists — mean per-galaxy deep-regime radial slope
      (delta vs log10 r/r_M, >= 3 points, log-span > 0.05 dex) is NEGATIVE with
      binomial p < 0.01 against 50/50.
  Registered expectation: G036 measured the floor at 0.0447 dex (canonical, SPARC-only).
  The 16 added curves carry INHERITED baryon models (different radii, beams, weighting
  than the photometry that fixed the model) — floor inflation on the extended set is the
  live risk this verdict tests. Thresholds: (a) <= 0.060 dex, (b) sign negative AND p < 0.01.

V2E (the environmental EFE split G036 registered as impossible in SPARC alone):
  For every modeled Tier-1 curve with an e_N row: split the sample at the 75th percentile
  of its OWN e_N distribution (not an absolute threshold — the registered 0.5-a0 boundary
  is out of range on every available axis and this is declared, not discovered). Statistic:
  outer-bin (r/r_M > 3) mean residual of the high-e_N half minus the low-e_N half.
  DETECTION requires |offset| > 0.05 dex AND the L240 additive-law sign (strong-field
  galaxies sag LOW, i.e. offset < -0.05 dex). Bootstrap 95% CI reported (2000 resamples,
  resampling galaxies).
  Axes: primary = the G036-consumed column (gext_vectors cols[4], the noclu-values axis;
  G036's own label corrected here); bracket = cols[5] (maxclu). Detection on EITHER axis
  counts, as registered in G036's fallback clause.
  Registered READING (frozen): at these field amplitudes (max e_N 4.8e-3 primary /
  3.9e-2 bracket) the additive law's own predicted shift is ~1e-3–1e-2 dex, an order of
  magnitude BELOW the 0.05-dex detection threshold. A null is the expected architecture-
  consistent outcome. A POSITIVE at this amplitude would NOT be claimed as EFE detection;
  it triggers a confounder audit (inclination/distance/M-L systematics correlate with
  environment) before any claim. The e_N ~ 1 test remains out of this corpus's reach.

V3E (WALLABY cross-check, Tier 2, separate):
  (a) e_N join: 203/203 WALLABY galaxies matched to gext_wallaby_237.csv. Registered
      finding to check: the Tier-2 e_N distribution (median ~4e-3, max ~0.12) still
      leaves the registered 0.5-a0 split OUT OF RANGE — WALLABY DR2 does NOT yet make
      the e_N ~ 1 EFE test possible; the split stays unmet and this is recorded as the
      honest scope state, not spun.
  (b) BTFR on WALLABY: the corpus carries NO stellar-mass or baryon metadata ->
      the M_b-dependent BTFR is NOT RUNNABLE on this corpus (pre-declared scope note).
      What IS delivered: v_flat per galaxy (mean of rings with R >= 0.8 R_out, >= 2
      rings required) + its distribution, and the full 203-row v_flat/e_N join table,
      as the Tier-2 artifact for the future mass-matched cross-check.
  (c) sanity: corpus WALLABY vrot_max vs computed v_flat agreement reported; no
      verdict threshold — descriptive only.

## Artifacts
- glm53_push/G044_corpus_extension.py — the pipeline (G036's exact binning: 0.2-dex
  r/r_M bins from 0.02 to 30, mu_2 bisection s = 2 a0, 200 iterations, both footings).
- glm53_push/G044_corpus_extension.out — full log.
- glm53_push/G044_corpus_extension.json — extended scatter table + EFE split table
  (the paper artifacts) + all verdict measurements.
- glm53_push/data/rotation_curve_corpus_v7.json — the ingested corpus (sha256 a9d668ea…).

Registered before data by the G044 lane per the G041 item-3 action and the repo's
pre-registration discipline (G035/G036 precedent).

## ADDENDUM (post-run, 2026-09-14 18:2x EDT — recorded outcome, nothing amended)

The V2E canonical-footing offset measured -0.0512 dex, crossing the registered
|0.05| threshold (alt footing: -0.0449 dex, below). Per the frozen V2E reading
clause, the confounder audit ran in-script (PART 6) BEFORE any claim:
  A1 the two registered axes select the IDENTICAL high-e_N set (Spearman rho of
     the axes = 0.998) -> one effective test, not two;
  A2 coverage: the high-e_N half reaches LESS far (median max r/r_M 3.99 vs 4.77);
     window-restricted offsets (3,6] and (3,4.5] stay at -0.0517/-0.0505 dex;
  A3 mass: e_N split is mass-orthogonal (rho(log e_N, log M_b) = -0.06); the
     M_b split at its own p75 gives the OPPOSITE sign (+0.070 dex);
  A4 galaxy-level bootstrap, one-sided p(offset >= 0) = 0.114.
Verdict per the frozen protocol: NOT a detection. The standing verdict on the
environmental EFE at sample scale remains NOT ESTABLISHED, consistent with the
architecture's predicted ~1e-3-1e-2 dex shift at these amplitudes. The full
audit numbers are in G044_corpus_extension.json (posthoc_audit).
