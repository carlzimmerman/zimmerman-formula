# CFG960 FROZEN CRITERIA: CFG652's hot-group lensing test with a spectroscopic total-mass census (GAMA G3C + DR4 GKV)

Block CFG960–969 (LEDGER reservation e15fd880c, owner-approved). Follow-up to CFG652 (criteria 11c7906ef, result ef182618d) and
CFG924 (result 8e7374552). CFG924 found that CFG652's label hinges on which groups the photometric census gives a condensed mass.
This lane replaces the photometric census with spectroscopic members and total-flux stellar masses. No new posit, no new model.

Committed ALONE, before any script is written and before any spectroscopic M_cond of any eFEDS group is computed. Date 2026-10-21.
κ = ½ is FITTED. Footings canonical 9.3603e-11 / alt 1.1312e-10 m s⁻², never pooled. "Cold energy"; its mass is required; no
particle species; not "theory closed". Raw data and framework-native models only (CFG652's models, unchanged).

## Seen before this freeze (disclosed)
- **CFG652 and CFG924, every output.** CFG652: BOTH EXCLUDED. CFG924: NOT DIAGNOSTIC (FRAGILE: gas extent), driven by 8 added
  groups. Model (a) is chaotic in its inputs (χ²_a jitter sd 0.28–0.55).
- **The GKV fetch sanity numbers** (`_external_data/gama_dr4_gkv/FETCH_LOG.md`):
  - 73,648 rows; 69,205 with logM* > 5; 58,824 also in G3CGalv10;
  - GKV z minus G3C Z: median 1.26e-3.
- **Footprint counts:** 137 of CFG652's 148 groups have centres in G09; 127 have their 6 R_X annulus inside the box.
- **The eFEDS table's z column (3 decimals) carries no spec/photo flag.**
- No spectroscopic M_cond, and no CFG960 number, has been seen.

## Data (read-only; nothing further downloaded)
- **Groups and lensing:** CFG652's stored `cfg652_inputs.npz` (positions, eFEDS z, R_X, M_hot) and `cfg652_esd.npz` (per-group
  ESD sums; reused unchanged; the lensing z stays the eFEDS z).
- **Spectroscopic galaxies:** `G3CGalv10.csv` (CFG471 fetch; CATAID, RA, Dec, Z, Rpetro, GroupID; NQ ≥ 3, r < 19.8) joined on
  CATAID to `gkv_stellarmass_g09.csv` (DR4 GKV total-flux logM*, owner-approved fetch 2026-10-21). Galaxy z = G3C Z (the z
  GAMA's group finder used). Only galaxies with a finite logM* > 5 are used.
- **G3C groups:** `G3CFoFGroupv10.csv` (variant V3 only).
- **Code** is reused by exec of text slices of committed sources, never imported:
  - CFG652 `cfg652_test.py` preamble + models block + score block verbatim (WORK and the output directory redirected);
  - CFG922 `Census.comp` + `mlim_table` (completeness form), `read_cols` + `load_bright` (K4/K5 only);
  - `cfg652_model.py` (sha256 04352d4e…d60d1, imported from this checkout).

## Census (per group; planar ra·cos(dec) metric and R_X = R500 label as the aperture, both as CFG652)
- **Box:** GAMA G09, 129 < RA < 141, −2 < Dec < 3. A group is in the sample only if its R_X aperture lies wholly inside the box.
  Groups outside are NOT IN G09: M_cond = 0, so excluded by CFG652's post-freeze rule.
- **Spectroscopic anchor.**
  - Candidates: galaxies within 0.5 R_X with |z − z_eF| ≤ 0.05(1 + z_eF), CFG652's window.
  - For each candidate j, count the candidates within ±1500 km/s (rest frame, Δv = c(z_k − z_j)/(1 + z_j)).
  - The peak j* has the highest count; ties go to the higher summed stellar mass.
  - z_grp = median z of the candidates within ±1500 km/s of z_j*.
  - No candidate: NO ANCHOR, M_cond = 0, excluded.
  - The |z_grp − z_eF| distribution is reported.
- **Members:** |Δv| ≤ W = 2000 km/s around z_grp (rest frame).
- **Raw terms:**
  - net = Σ M*(members within R_X) − background;
  - background = Σ M*(members in the 3–6 R_X annulus) × A_ap / (A_ann × f_ann), where f_ann is the in-box fraction of the annulus
    on a fixed polar grid (200 radii × 720 angles, area-weighted);
  - bcg = most massive member within 0.2 R_X (0 if none).
- **Completeness:** M_lim(z) on z nodes 0.03–0.55, step 0.01, is the median logM* of the census galaxies with 19.3 ≤ Rpetro ≤ 19.8
  and |z − node| ≤ 0.02 (≥ 20 galaxies; GAMA's r = 19.8 limit in place of CFG922's KiDS 19.5–20.0). The factors c_cen = exp(x)
  and c_up = 1/erfc(√x), with x = 10^(M_lim − 11), come from CFG922's `Census.comp` (exec'd), evaluated at z_grp.
- **PRIMARY, S-cen:** M_cond = bcg + c_cen · max(net − bcg, 0); M_bcg = bcg.
- **Variants** (x1 cell only; all other groups and steps as primary):
  - **V1, no completeness (c = 1):** M_cond = max(net, bcg), CFG652's form.
  - **V2, upper completeness:** c_up in place of c_cen.
  - **V3, G3C membership.** Members are the G3C galaxies of the matched FoF group (IterCen within 0.5 R_X and |Δv(Zfof, z_grp)| ≤
    W; several matches → largest Nfof) lying within R_X, with no background term; M_cond = bcg + c_cen · max(Σ − bcg, 0).
    Groups without a G3C match keep their primary value.
  - **V4 / V5, window:** W = 1000 / 3000 km/s.

## Models and statistic (unchanged from CFG652 / CFG924)
- **Primary:** CFG652's `models` block verbatim on the S-cen inputs (x1, M_cond × 10^±0.2, gas to 1 / 4 R_X, plus the MUTATE M1
  arrays).
- **Variants:** the identical `cfg652_model` calls, x1 only. Their p02 / m02 / g1 / g4 entries are copies of x1, so variant
  labels are x1 labels only. Model arrays are cached by their exact inputs. Identical inputs reproduce bit for bit (CFG924 K3).
- **Score:** CFG652's `score` block verbatim (8 bins 53–783 kpc, jackknife + Hartlap, χ²_a, χ²_b, the four labels, FRAGILE
  under M_cond ±0.2 or gas extent, footings must agree, the 2-halo tag on any (b) FAVOURED).

## CFG960 decision rule
- **PRIMARY LABEL L:** CFG652's final label on the S-cen inputs.
- **CENSUS-FRAGILE:** any of V1–V5 gives an x1 label different from the primary x1 label on either footing (the variants
  concerned are named).
- **NOISE-SENSITIVE:** any of four model-(a) jitter realizations (M_cond × (1 + k·1e-12), k = 1..4; model (b) unjittered; x1,
  both footings) gives an x1 label different from the primary's.
- **DECISIVE:** L ∈ {(a) FAVOURED, (b) FAVOURED, BOTH EXCLUDED}, without FRAGILE, FOOTING-DEPENDENT, CENSUS-FRAGILE or
  NOISE-SENSITIVE. Otherwise NOT DECISIVE, with every reason listed. CFG652's own forecast put this sample in the hard regime,
  so NOT DIAGNOSTIC / NOT DECISIVE is stated in advance as a likely outcome.
- **Relation to the record:** HOLDS or MOVES against CFG652 (BOTH EXCLUDED) and against CFG924 (NOT DIAGNOSTIC (FRAGILE: gas
  extent)).
- **Reported, no verdict weight:**
  - **F-on-S:** CFG652's stored photometric M_cond and stored model arrays on the groups where both F and S-cen > 0. This
    separates the mass change from the sample change.
  - **S-on-F:** S-cen masses on the same groups.
  - **Census bookkeeping:** groups NOT IN G09, NO ANCHOR, M_cond = 0; median Δlog10 M_cond (S-cen vs F, and vs CFG924 A1c);
    M_lim(z) and c(z) at the group z.
  - CFG652's POSTHOC cut and secondary split under S-cen; A_out values.

## Controls (all must PASS; a failure makes the lane VOID until fixed and disclosed)
- **K1:** sha256 of `gkv_stellarmass_g09.csv` matches its fetch log; both G3C files match CFG471's fetch log.
- **K2:** CFG652's verbatim score on its own stored work files reproduces `cfg652_test_results{,_POSTHOC,_MUTATE}.json`
  (χ² abs < 1e-6, all other numbers abs < 1e-9, labels identical).
- **K3:** `cfg652_model` reproduces the stored arrays (all 22 per group) for the 6 CFG924 K3 groups: max rel < 1e-10.
- **K4:** the CFG960 census engine, fed the unamended KiDS bright sample with CFG652's photometric settings, reproduces CFG652's
  148 stored M_cond and M_bcg: max rel < 1e-9. CFG652's settings are window |z_phot − z_eF| ≤ 0.05(1 + z_eF) around z_eF with
  no anchor step, CFG652's box 122–150 / −7–9, masked = 0, c = 1.
- **K5:** CFG922's `Census.comp` with CFG922's own KiDS M_lim table reproduces the c_cen and c_up stored in `cfg922_census.json`
  for the 318 eRASS1 clusters: max rel < 1e-12.

## MUTATE
- **M-PLANT** (census, before the main models): a planted 1e12 M☉ galaxy at each included group's centre at z_grp gives
  |net′ − net − 1e12| < 1e-9 × 1e12 and bcg′ = max(bcg, 1e12) exactly.
- **M-NULL** (census, before the main models): 300 random positions (seed 960) in the box with their R_X apertures inside it,
  each with an (R_X, z_grp) pair drawn from the included groups. Mean raw net must be consistent with 0 (|mean| < 3 SE); else the
  background term is biased (FAIL).
- **M1** (CFG652's own, verbatim score with MUTATE on the primary): (a) with the hot gas relabelled condensed reproduces (b)'s χ²
  to < 0.01.
- **M-INJ** (end to end, after the main models; fresh model calls, no cache): S-cen M_cond × 10**0.2, the exact float operation
  of CFG652's p02 variant, as an x1 run must reproduce the primary's p02 cell (χ²_a, χ²_b abs < 1e-6; same label) on both
  footings.

## Budget and rules
One process at a time, one core (OMP/BLAS threads 1), nice 10, < 1 GB RSS, beside the live 1024³ job.
- **Run order:** K, then MAIN (census + M-PLANT + M-NULL printed first, then models, variants, scores), then INJ, then JITTER
  (assembles the final qualified label).
- **Time:** about 7 h (≈ 3.8 s per model call).
- **Outputs:** only in this directory and `_external_data/cfg960_work`.
- **Git:** commits with explicit paths; history never rewritten.
