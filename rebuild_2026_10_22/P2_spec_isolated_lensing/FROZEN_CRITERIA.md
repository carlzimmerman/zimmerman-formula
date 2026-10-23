# P2_spec_isolated_lensing: FROZEN CRITERIA (committed alone with the ledger, before any script, shear read or model number)

Brief: the coordinator's P2 task, `rebuild_2026_10_22/BRIEF.md` (failure 2), `doors_push_2026_10_22/BRIEF.md` and
`BRIEF_E_AUDIT.md`. F2 (`rebuild_2026_10_22/F2_outer_lensing/`, incl. AMENDMENT_A1) is the parent lane.
κ = ½ FITTED. Footings canonical a₀ = 9.3603e-11, alt 1.1312e-10 m/s², scored separately, never pooled.
No dark-matter particle. Never "theory closed". Never "the data favour the framework".
Ledger: `ASSUMPTION_LEDGER.md` (committed with this file).

## 0. Question

F2 found outer (0.4–3 Mpc) isolated-galaxy lensing UNDECIDABLE: the photo-z "isolated" sample leaks hosts, a wider
host veto opens an isolation hole beyond 1.1 Mpc, and the external field (EFE) makes v3's outer prediction 4.5–12× too
small while B21's sample tolerates only y_e ≲ 3e-5. P2 builds the largest spectroscopically isolated lens sample on disk
that overlaps KiDS-1000 shear, measures ΔΣ(R) to 3 Mpc with its covariance, and scores v3
(`covariant_push_2026_10_22/THEORY_V3_DRAFT.md`: AQUAL μ = x/(1+x), screened by L★, with an EFE) with
(a) zero external field and (b) the external field implied by the spectroscopic catalogue itself.

## 1. Inventory (done before this file; catalogue counts only, no shear read, no model evaluated)

| catalogue on disk | overlap with KiDS-1000 shear | used? |
|---|---|---|
| GAMA DR4 G3CGalv10 (CFG471 logged fetch, sha256 051950e1…f9; `campaign_fresh_gravity/_external_data/cfg471/G3CGalv10.csv`) | G09 58,839 + G12 63,198 + G15 62,044 = 184,081 spec-z, r < 19.8 (99.7 % in KiDS source cells); G02 (20,029) is outside KiDS; G23 absent | **YES — the sample and the environment catalogue** |
| GAMA DR4 GKV stellar masses (`../_external_data/gama_dr4_gkv/` outside the repo, G09 only, 73,648) | G09 only | cross-check of lens masses only (reported) |
| GAMA GalaxiesClassifiedv01 (CFG563) | subset of G3C | no (adds nothing to G3C redshifts) |
| 2MRS (`real_research/data/2mrs_catalog.csv`, 44,599) | 1,030 in KiDS source cells (783 at 3000 < cz < 15000) | no: ≲ 10 % S/N gain for a 2–3° aperture per lens, K-band masses not poolable with LePhare |
| DESI DR1 BGS_BRIGHT (CFG316 fetch; staged `cfg316_lenses.npz`) | 165,796 good-z rows in the KiDS footprint; 55,561 inside the GAMA boxes, 110,235 outside | no: CFG316 showed DR1 fibre incompleteness (median 70 unobserved BGS targets within 3 Mpc per lens) prevents a complete veto; inside GAMA it is shallower (r < 19.5) than GAMA |
| SDSS / BOSS spectroscopic galaxies | none on disk | — |
| 6dFGS FP (Campbell+14) / ALFALFA–SDSS (Durbala+20) | 849 / 1,124 in KiDS cells | no: selected subsamples (early types / HI), not complete environment catalogues |

Pre-freeze feasibility counts (GAMA, z > 0.02, no proxy margin; disclosed because they chose the rule below):
a complete B21-style veto (no neighbour above 0.1 M★,lens within 3 Mpc) is possible for only **29** GAMA lenses in total
(a 0.1 M★ neighbour is fainter than r = 19.8 at almost every lens redshift). A complete **host veto** (f = 1) gives
≈ 4,015 lenses at R_iso = 3 Mpc and ≈ 12,562 at R_iso = 1 Mpc. f = 0.5 / 0.3 give 338 / 48 at 3 Mpc.

## 2. Lens samples (frozen)

- **Parent:** G3CGalv10 in the GAMA boxes G09 RA [129, 141] Dec [−2, 3]; G12 RA [174, 186] Dec [−3, 2];
  G15 RA [211.5, 223.5] Dec [−2, 3] (deg). Redshift = G3C `Z`.
- **Masses (h70 catalogue units):** KiDS-bright LePhare `MASS_MED` + 0.15 dex (record convention, F2 ledger B1) of the
  nearest KiDS-bright object within 1.5″, valid when `MASS_MED` > 0; rescaled from the LePhare redshift to the spec-z by
  + 2 log₁₀[D_L(z_spec)/D_L(z_LePhare)] (flat Ω_m 0.3, h 0.7, the catalogue's fiducial). Galaxies without a valid LePhare
  mass get a proxy lM = c(z) − 0.4 r_petro + 2 log₁₀ D_L(z), c(z) = median over valid galaxies in 0.01-wide z bins;
  proxy masses carry δ = 0.30 dex (their scatter against LePhare, measured on the catalogue).
- **Lens cuts:** 0.05 < z < 0.50; 8.5 ≤ lM70 < 11.0; valid LePhare mass; KiDS-bright `masked` = 0.
- **Completeness:** lM70,lens ≥ M_lim95(z), the 95th percentile, among valid-mass G3C galaxies in the lens's 0.01 z bin,
  of lM70 − 0.4 (19.8 − r_petro) (the mass each galaxy would have at the flux limit); empty bins linearly interpolated.
- **Isolation (host veto, f = 1):** no G3C galaxy j ≠ lens with projected physical separation < R_iso (native distances,
  at the lens z), |Δv| = c |z_j − z_l|/(1 + z_l) < 1000 km/s, and lM70_j + δ_j ≥ lM70,lens (δ_j = 0 for LePhare, 0.30
  for proxy masses).
- **Edge:** the lens's projected distance to every box edge ≥ R_iso.
- **S3 (primary, the verdict):** R_iso = 3.0 Mpc. **S1 (secondary, reported):** R_iso = 1.0 Mpc. S3 ⊂ S1.

## 3. How the isolation hole is handled (frozen)

- **Iso-random points.** Draw a lens from the sample (with replacement), place it at a uniform random position in a
  uniformly chosen GAMA box (uniform in RA and sin Dec), keep it only if it meets the same edge margin and the same veto
  with that lens's (z, lM70). I3 for S3: 4 N_S3 points; I1 for S1: 2 N_S1 points (cap 200 N attempts).
  **Plain randoms R:** lens drawn from S1, uniform position with edge ≥ 1 Mpc, no veto; 3 N_S1 points. Fixed seeds.
- **Primary data vector:** Δ(R) = ΔΣ_L(R) − ΔΣ_I(R). The iso-random stack is the lensing of the vetoed environment
  (the hole and everything common to it) with no central galaxy; subtracting it removes both from the data.
- **Model side:** m(R) = T_own(R) + [T_nbr(L) − T_nbr(I)](R) (section 5): the lens's own v3 profile plus the v3 lensing
  of the catalogued neighbours that sit around real lenses beyond what sits around iso-random points.
- Reported, not verdict lines: raw L − R against T_own + T_nbr(L) − T_nbr(R); the environment-only stack I − R against
  T_nbr(I) − T_nbr(R); Δ against T_own alone.

## 4. Estimator (own code; F2's amplitude estimator re-implemented exactly)

- Sources: KiDS-1000 SOM-gold via F1's reader cache (passed as argv; 21,262,011 rows, finite, w > 0, Z_B ≤ 1.2).
  For each centre: Z_B > z_c + 0.2; flat-sky offsets (Δα cos δ_c, Δδ); physical R = θ D_A(z_c);
  15 log bins 0.03–3.0 Mpc; e_t = −(e1 cos 2φ − e2 sin 2φ) (record/F1 sign); Σ_crit⁻¹ = (4πG/c²) D_l (1 − χ_l/χ_s) at
  the source Z_B; native flat Ω_m 0.3085, h 0.679 (F2 H1/H2). Per centre and bin: WG = Σ w Σ_crit⁻¹ e_t,
  WW = Σ w Σ_crit⁻², the cross analogue, N. ΔΣ = (ΣWG/ΣWW)/(1+K), 1+K = 0.9853 (F2 ledger C2).
- Patches: 36 (1° RA slices of the three boxes, by centre RA). Delete-one jackknife, paired across L, I, R; the 15 × 15
  covariance of Δ is reported.
- Ranges (bin centres): in 0.03 < R ≤ 0.31; **O1 0.4 < R < 1.1** (4 bins); **O2 1.1 < R ≤ 3.0** (3 bins).
- Amplitude (F2 Track B): w = m/var (jackknife variance of the data vector), A = Σ w d / Σ w m over the range, σ_A from
  the jackknife replicates of A (the model's replicate uses the same deleted patch).

## 5. Model (v3, F2's T_central inventory; no fitted amplitude, bias, profile or halo model)

- Field equation AQUAL, μ = x/(1+x); lensing sees Φ; orientation-averaged M_eff (F2's solver `f2_aqual.py`, imported
  read-only). Screening (L★ ≥ 21.7 pc) is irrelevant at R ≥ 30 kpc (stated). BS24's μ_K² ψ static term is not included
  (deferred, as in S2 and N0's R6). No dust term (v3 predicts no galaxy-bound dust profile; F2).
- Baryons per galaxy: M★ (above, native: + 2 log₁₀(0.70/h) + 2 log₁₀ q_DA as F2); cold gas log f_cold = −0.69 lM70 + 6.63;
  hot CGM 0.5 M★ (uniform 100-kpc sphere for the lens; a point for neighbours).
- **T_own:** per lens, F2's profile (isolated AQUAL of the extended baryons × the point-mass EFE ratio C(r; y_e)),
  area-averaged over each R bin, stacked with each lens's WW. EFE solutions on the grid
  y_e ∈ {0, 1e-6, 3e-6, 1e-5, 3e-5, 1e-4, 3e-4, 1e-3, 3e-3, 1e-2}, interpolated in log y_e.
- **T_nbr(c):** for every G3C galaxy j ≠ c with projected d < 6 Mpc (physical at z_c) and |Δv| < 1000 km/s, the exact
  bin-averaged tangential ΔΣ about c of j's v3 profile, from ⟨ΔΣ_t⟩ = M_c(<R)/(πR²) − Σ_ring(R) (M_c = j's projected
  mass inside the centre's circle); summed over j (linear superposition: exact in the EFE-linearised regime, an upper
  estimate at y_e → 0, where AQUAL's far field grows as √ΣM).
- **Case (a):** y_e = 0 for the lens and every neighbour.
- **Case (b):** each galaxy's y_e = |g_N|/a₀ (footing), g_N = Newtonian vector field at its position of all other G3C
  galaxies' baryons M_b,j / C_b(z_j) with 3D physical separation 1.0–10 Mpc (redshift-space positions from RA, Dec, z;
  native comoving distance / (1 + z_i)). Galaxies within 1 Mpc belong to the lens's own system (T_nbr), not its
  external field. C_b(z) = ρ_b(lM70 ≥ M_lim95(z)) / ρ_b(lM70 ≥ 8.0) from the catalogue's own 1/V_max baryonic mass
  function (0.02 < z < 0.30, V_max from r_lim = 19.8 without k-correction). x_e from μ(x_e) x_e = y_e (F2).
- Reported brackets of (b), not verdict lines: no 1/C_b (lower); R_f 5 / 20 Mpc; projected-slab estimator; all cosmic
  baryons tracing the galaxies (× Ω_b ρ_crit / ρ_b,gal, Ω_b h² = 0.0224); matter tracing (× (1 + 5.364), ΛCDM-processed,
  flagged).
- **Scan (reported):** one uniform y_e for every galaxy, on the grid → y_allow = the largest grid value with
  A_O1 ≤ 1 + 2σ and A_O2 ≤ 1 + 2σ ("the field the data allow").

## 6. Lines and verdict (per footing; F2's classes)

"short" A − 1 > 3σ_A; "over" 1 − A > 3σ_A; "consistent" |A − 1| ≤ 2σ_A; else "between".
Decisiveness S = max over O1, O2 of |A_ba − 1| / σ_A,a, A_ba = Σ w m_b / Σ w m_a with case (a)'s weights.
On S3 (Δ vs m):
1. S < 3 → **UNDECIDABLE (N too small)**; N_needed = N_S3 (3/S)².
2. else (b) consistent in O1 and O2 → **v3 PASSES (catalogue EFE)**.
3. else (a) consistent in O1 and O2 → **v3 FAILS (EFE tension)**; report y_allow against the lenses' median catalogue
   y_e (central and lower bracket).
4. else (a) short in O1 or O2 → **v3 FAILS (short even at zero external field)**.
5. else (b) over in O1 or O2 → **v3 FAILS (overshoots even with the catalogue EFE)**.
6. else **UNDECIDABLE (between)**.
Lane verdict = the canonical verdict if both footings agree, else UNDECIDABLE (footing split). Robustness tags
(reported): the class recomputed with raw L − R, without T_nbr, with the lower-bracket field, and on S1.
One-at-a-time (reported, T_own only, T_nbr held): f_hot 0 / 1; M★ ± 0.2 dex; h 0.672 / 0.686; Σ_crit ± 3 %.
A cure must be a named ingredient or a measured sample property; nothing is fitted.

## 7. Checks (`p2_spec_isolated_lensing.py`; one line each; exit 0 iff all pass; `--mutate` writes `*_MUTATE.*`)

- **K0a** my estimator, run with F1's conventions on F1's first 30 clusters, reproduces F1's per-cluster raw ΔΣ and
  weight (`f1_meas.pkl` in the cache dir, h070) to ≤ 1e-6 relative. Absent pickle → N/A, not PASS.
- **K0b** with the record's conventions (CFG110: Ω_m 0.3, h 0.70, g_bar bins), the first 2,000 record lenses inside the
  GAMA boxes give ΣWW/ΣWW_rec ∈ [0.90, 1.000001] and a median stacked-ΔΣ ratio (bins with S/N > 3) in [0.95, 1.05]
  (the cache lacks Z_B = 1.20 sources, so equality is not expected).
- **K1** AQUAL solver: y_e = 1e-6 reproduces the isolated law to ≤ 1e-3 at s ≤ 10; far field ≤ 2 % (F2's K1).
- **K2** projection: point mass and SIS vs analytic ≤ 1e-3; my offset machinery at d → 0 equals the centred bin average
  ≤ 1e-3; offset point mass vs the analytic bin formula ≤ 1e-3; a uniform sheet of identical neighbours
  (y_e = 1e-4 profile) gives |ΔΣ_t| ≤ 1e-2 of one centred neighbour in every bin.
- **K3** S3 ⊂ S1; a brute-force re-veto (no tree) of 200 S3 lenses and 200 I3 points finds 0 violations.
- **K4** cross-shear null of Δ: χ² over 15 bins with the jackknife diagonal, p ≥ 0.001.
- **K5** GAMA completeness: KiDS-bright galaxies (masked = 0, r < 19.5) inside the boxes matched to G3C within 1.5″ ≥ 0.90.
- **MUTATE:** cross shear in place of tangential everywhere → K0a and K0b must FAIL (exit 1).
Compute: `OMP_NUM_THREADS=1 nice -n 15`, < 1 GB RSS, minutes; measurement cache in a scratch work dir (argv); no
downloads; no PM simulation.

## 8. What each outcome means

PASS (b): v3 with the field its own environment implies reproduces spectroscopically isolated outer lensing.
FAIL (EFE tension): the outer signal needs a field below y_allow, while the catalogue's baryons alone imply more.
FAIL (short / overshoot): the outer signal sits outside v3's range for any field in [0, catalogue].
UNDECIDABLE (N): the sample cannot separate (a) from (b); N_needed lenses would.
