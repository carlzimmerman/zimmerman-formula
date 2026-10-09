# CFG534 FROZEN CRITERIA: does the settled cold energy depend on assembly history at fixed stellar mass?

Written 2026-10-09, before any CFG534 script was written or any CFG534 number computed. Inputs inspected so far: the committed
READMEs/JSONs of CFG531, CFG528/528b, CFG505, the AUDIT_SLUGGS per-galaxy JSON keys, the cold_mass cm05/cm09 scripts and outputs,
and the on-disk table headers (lr_lenses.npz, cfg505_uv_table.npz, CFG503 group arrays, sluggs_forbes2017_galaxies.tsv,
SPARC_Lelli2016c.mrt). One structural fact was checked before writing: in the f30 sample the CFG503 (M_gal, z) groups have a median
within-group log M* spread of 0.003 dex, and M_gal - M* does not depend on type at fixed M* (it is a function of M* and z), so a
group is a fixed (M*, z) cell. 655 groups hold both types (25,893 early / 22,074 late lenses). No ε or residual was computed.

Standing settings: a0 = kappa c sqrt(G rho_DE), kappa = 1/2 FITTED. Footings 9.3603e-11 (canonical) and 1.1312e-10 (alt), scored
separately and NEVER pooled. Kernel nu_mono = 1/(1 - exp(-sqrt y)). Candidate B: the law's phantom = settled cold energy,
supply-capped, round, no EFE. The cold energy's mass is still required. Not "theory closed". Nothing downloaded. Compute: nice 10,
<= 4 threads.

## Hypothesis H (owner-approved) and how it is tested
H: the amount of settled cold energy depends on assembly history, not only present baryons. Old / early-type / merger-built /
central systems carry extra settled cold energy beyond the law's phantom; young, gas-rich, star-forming systems sit on the law.
**H is tested only as a sign/correlation prediction at fixed stellar (or baryonic) mass. No amplitude is fitted; nothing rescues a
fit.** The quantity is ε = ΔM(<r)/M_pred(<r) (CFG531's definition) or the equivalent log residual.

## Test 1: KiDS (CFG529/531 machinery, validated f30 environment, LAW_RTA own, constructions A and B)
Machinery: CFG531's `cfg531_kids.py` exec'd read-only up to (not including) its "# ---- base" section (data, groups, LAW_RTA tables
from the CFG531 cache, f30 environment EC30, `comps`, `fit_eps`, bands). Bands K-in (12-14), K-mid (9-11), K-out (6-8), K9 (6-14).

**Mass matching (primary, M-G).** For a comparison of class A against class B: inside each CFG503 (M_gal, z) group g and each radial
bin k, every class-B lens weight (WW and WG) is multiplied by W_A,gk / W_B,gk, where W_X,gk is the summed WW of class X in g, bin k.
Groups that lack either class (in the f30 sample) are dropped from both classes. After this the two classes have identical
stack weights per (group, bin), hence identical stacked model vectors (E and own). The difference vector is Δd = d_A - d_B.
- **Δε** per band = GLS amplitude of the matched own stack o on Δd: Δε = (o^T W Δd)/(o^T W o), σ = (o^T W o)^-1/2,
  W = (C_Δ[band]/hart(n))^-1, C_Δ the 50-patch jackknife covariance of the LOO Δd vectors (same patches for both classes, weights
  held at their full-sample values). o is the Moster-SHMR own stack; the Behroozi own stack is also used and the verdict takes the
  SMALLER Z of the two templates.
- Per-class ε with the matched weights (CFG531's `fit_eps`, its covariance) is reported.
- Comparisons:
  - **1a TYPE:** A = early (typ 1), B = late (typ 0), all f30 lenses.
  - **1b UV:** A = NUV-undetected, B = NUV-detected, f30 lenses with GALEX coverage (CFG505 `det` / `nondet`; `nocov` excluded).
  - 1b-late / 1b-early (reported): the UV split inside each type.
  - 1c (reported): 1a inside each f30 log M* tertile (CFG531's tertile edges).
- **Pass rules (per footing):**
  - 1a PASS: Δε_EL(K9) > 0 with Z >= 3 in both constructions. 1a CONTRADICTS: Z <= -2 in either.
  - 1b SAME SIGN: Δε_UV(K9) > 0 (both constructions); significant if Z >= 3; CONTRADICTS if Z <= -2 in either.
  - "Late on the law" (qualifier, no ladder weight): matched late ε(K9) within 2σ of 0.
- **Amplitude reading (reported):** δ_equiv = 0.10 Δε_EL(K9) / [ε_d0(K9) - ε_d0.10(K9)], with the CFG531 JSON values (the
  uniform M* shift that would produce the same ε change).
- Unmatched early-late (CFG531 (c)) is reproduced as a control (K1) and reported beside the matched value.

## Test 2: SLUGGS ellipticals/lenticulars (small N; consistent/inconsistent only, never a detection)
- Offsets: `AUDIT_SLUGGS_2026-10-03/audit_sluggs_recompute_results.json`, per_galaxy `nu_mono|{footing}`, key `off` (K0 JAM-law
  mass; dex in σ_los, > 0 = excess over the law). N = 17.
- Mass control: Forbes+17 (`sluggs_forbes2017_galaxies.tsv`) log M*.
- History proxies: Env (F 0, G 1, C 2; Forbes+17); central = {4486, 4374, 4365, 5846} (CFG528's four) plus 4649 (cm09's list);
  morphology E = 1 if MType starts with "E" (incl. E/S0), S0 = 0; log L_X/L_B from O'Sullivan+01 (cm05's parsing, upper limits at
  their value; N = 16). Composite H-score = mean of the per-proxy ranks scaled to [0, 1] (proxies available for the galaxy).
- Statistic: partial Spearman ρ(off, proxy | log M*) (rank residuals, as cm09). p (one-sided, positive) from 20,000 permutations
  of the proxy within log M* tertile blocks (sorted by log M*: 6 / 6 / 5), seed 534.
- Reading per proxy: CONSISTENT (ρ > 0), SUPPORTING (ρ > 0 and p < 0.05), INCONSISTENT (ρ < 0 and the negative-tail p < 0.05),
  else NEUTRAL. "Same sign elsewhere" for SLUGGS requires the composite ρ > 0.
- Ages: no per-galaxy stellar-age table is on disk for SLUGGS or ATLAS3D (the ATLAS3D file on disk holds M/L, not ages). Age is
  not tested; the fetch is listed in the README for the owner.

## Test 3: SPARC rotation curves (Hubble type T, gas fraction, surface brightness at fixed baryonic mass)
- Sample: Q <= 2, Inc >= 30 (CFG533's loader). Υ_disk 0.5, Υ_bulge 0.7, gas from rotmod. Law: g = ν_mono(g_bar/a0) g_bar.
- Per point r = log10(g_obs/g_law); per-galaxy weighted mean with w = 1/(σ_p^2 + 0.05^2), σ_p = 2 eV/(V ln10).
  - Δ_in: points with R <= 1.5 R_disk; Δ_out: R >= 3 R_disk; Δ_all: all points. A region needs >= 2 points.
- log M_b = log10(0.5 L36 + 1.33 MHI) (×1e9). f_gas = 1.33 MHI / (0.5 L36 + 1.33 MHI).
- Classes: early T <= 3 (S0-Sb), late T >= 4.
- **Matched difference:** log M_b bins of 0.4 dex from 7.0 to 12.2; in each bin with >= 2 early and >= 2 late galaxies, the
  difference of means; bins combined with inverse-variance weights (variance = s_e^2/n_e + s_l^2/n_l, galaxy scatter). Z = diff/σ.
- Partial Spearman ρ(Δ_out, T | log M_b), ρ(Δ_out, f_gas | log M_b) (H predicts both < 0), ρ(Δ_out, log SBeff | log M_b) (reported).
- Rules (per footing): SAME SIGN if early-late Δ_out > 0; significant if Z >= 2; CONTRADICTS if Z <= -2.

## Test 4: H against "stellar M/L rises with age/mass" (IMF / population)
**What separates them.** An M/L error multiplies the stellar mass: its fractional effect is largest where stars dominate
(r < r_M, ε ≈ f) and falls to ≈ f/2 in the deep-MOND regime. Extra settled cold energy adds mass where the phantom lives: ≈ 0
where stars dominate, growing outward. So **H predicts the history signal in (outer - inner); M/L predicts it in inner at least as
strongly as in outer.**
- **KiDS:** every KiDS band is at r >= 4 r_M (deep MOND), where both an M/L shift and an isothermal extra component scale like the law
  (M ∝ r). KiDS radial shape is therefore declared NOT DISCRIMINATING in advance; Δε_EL per band and the M/L-shift template shape
  (CFG531 tables d0.10 minus d0, ε per band) are reported only.
- **SPARC:** early-late matched (Δ_out - Δ_in) and early-late matched Δ_in (same bins as Test 3).
- **SLUGGS (N = 16, ATLAS3D Salpeter population masses, the same M* for inner and outer):** D_in = -inner_salp (dex excess of the
  JAM mass inside r_1/2 over the law), D_out = 2 off_salp (dex, mass). Partial ρ((D_out - D_in), H-score | log M*) and
  ρ(D_in, H-score | log M*), permutation p as Test 2.
- **Radial pattern favours EXTRA MASS** if (SPARC early-late (Δ_out - Δ_in) Z >= 2, or SLUGGS ρ(D_out - D_in) > 0 with p < 0.05) and
  neither of the two is negative at Z <= -2 / negative-tail p < 0.05.
- **Radial pattern favours M/L** if (SPARC early-late Δ_in Z >= 2 and early-late (Δ_out - Δ_in) <= 0) or (SLUGGS ρ(D_in) > 0 with
  p < 0.05 and ρ(D_out - D_in) <= 0).
- Otherwise radial: NOT DIAGNOSTIC. If both fire: MIXED (treated as NOT DIAGNOSTIC).

## Test 5: MUTATE (CFG534_MUTATE=1, outputs *_MUTATE.*) — every tooth must fire
- **MU1 (KiDS):** type labels, and separately NUV labels, shuffled within each (M_gal, z) group (seed 534). The matched Δε(K9) must
  have |Z| < 2.5 in all four cells (A/B × footing) for both splits. (Unlike CFG531's MU3, the matched estimator compares inside
  groups, so a within-group shuffle must kill it.)
- **MU2 (KiDS method):** mock d_A = d_B,matched + 0.3 o: Δε = 0.300 in every band to 1e-6.
- **MU3 (SPARC):** T shuffled within log M_b bins, 200 seeded shuffles: |mean Z| of the early-late Δ_out < 0.5, both footings.
- **MU4 (SLUGGS):** proxies shuffled within mass blocks, 2,000 shuffles: |mean composite ρ| < 0.1, both footings.
## Controls (must pass)
- K1: unmatched early/late ε(K9) reproduce CFG531's JSON (c) to 1e-6 (A, B, both footings).
- K2: after matching, the two classes' stacked model vectors agree to 1e-10 relative (every band, both SHMRs).
- K3: SPARC ALG weighted rms on Q <= 2 reproduces CFG533's K2 within 0.005 (canonical 0.1117, alt 0.1005 at their footings).
- K4: SLUGGS offsets read equal the AUDIT JSON; N = 17 (16 with L_X; 16 for Test 4).

## Verdict ladder (per footing; applied in this order)
1. **NOT DIAGNOSTIC** if the matched 1a σ(Δε_EL, K9) > 0.30 in either construction.
2. **H NOT SUPPORTED** if 1a fails (Z < 2 in either construction), or any CONTRADICTS fires (1a, 1b, SPARC Δ_out).
3. **M/L-PREFERRED** if the radial pattern favours M/L (Test 4).
4. **H SUPPORTED** if 1a PASS (Z >= 3 both constructions) AND same sign elsewhere (1b, SPARC Δ_out, SLUGGS composite ρ all > 0) AND
   the radial pattern favours EXTRA MASS.
5. **H CONSISTENT-WEAK** otherwise.
Headline: if the footings differ, FOOTING-DEPENDENT with both labels.

## Disclosures policy
Numbers in the README come from the results JSONs. Any change after the first run is dated and disclosed; this text is not edited.
κ = ½ is fitted. The cold energy's mass is still required. Not "theory closed". Nothing here says the data favour the framework.
