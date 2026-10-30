# GH5_tsz_desi_centrals: FROZEN CRITERIA (committed alone, before any y-map pixel is read around DESI lenses)

**Question.** GH3 and GH4 left the hot-gas extent NOT DECIDED on 88k KiDS isolated lenses (Δχ² ≈ 4). GH4's README said
this "needs a deeper measurement". DESI DR1 BGS spectroscopic galaxies, already on disk, give ~2.5× more MW-mass lenses
in the ACT strip. **Does gas around MW-mass centrals extend past R_vir?**

## Data (nothing new fetched)

- **Maps:** ACT DR6.02 NILC y strips as GH3/GH4. PRIMARY CIB-deprojected; reported standard ILC.
- **Lenses:** `desi_dr1_bgs/BGS_BRIGHT_full_HPmapcut.dat.fits` with ZWARN = 0, DELTACHI2 > 40, joined on TARGETID to
  `desi_dr1_cigale/IronPhysProp_v1.2.fits` (main/bright) for LOGM and LOGSFR.
- **Mass and redshift cut:** LOGM 10.6–11.0, z > 0.1, −35.9° < Dec < 3.9°. LOGM is converted to native as GH3 (h 0.704
  WMAP7 → 0.679).
- **Validity:** ±40′ stamp finite and non-zero, and 20 R_vir inside 39′.
- **Catalogue-only counts seen before this freeze** (no y read): 313,094 lenses; 219,374 centrals.

## Tiers (neighbours: any matched BGS galaxy, spec-z, |Δv| < 2000 km/s, native D_A)

- **PRIMARY, "central":** no more massive neighbour within 1 Mpc projected. This is close to the kind of sample Zhang's
  gas was measured on (their CEN fraction is 68 %).
- **"clean":** no more massive neighbour within 3 Mpc. This suppresses the two-halo tSZ, which is dominated by heavier
  neighbours, by selection rather than by a template. GH4's template failed its smoothness premise and is not reused.
- **"iso3":** no neighbour with M★ > 0.1 M★,lens within 3 Mpc (B21-like, ~33k).
- **Completeness:** "central" restricted to COMP_TILE > 0.8 is reported, since missed fibres leak satellites in.
- **Dust split:** "central" split at LOGSFR − LOGM = −11 (passive vs star-forming) is reported. Passive lenses carry less
  CIB, so a positive y there is the cleanest.

## Measurement and predictions (as GH4)

- **Stack:** annuli x = [0, .5, 1, 1.8, 3, 5, 8, 12, 20]; per-lens compensation by the [12, 20) mean; 3 randoms per lens in
  the ±0.5° box; 50 equal-count RA jackknife patches, Hartlap-corrected.
- **Gas:** Zhang MW-mass gas (β 0.43, r_c 6 kpc, M_hot(<R_vir) = 1.84 M★, 0.22 keV, μ_e 1.14), cut at k = 1, 1.8, 3,
  beam-convolved, averaged over (z, lm) cells, compensated. A = 1. χ² on 7 points. No free parameter.

## Verdict (frozen; PRIMARY = CIB-deprojected, central)

- **EXTENDED GAS PREFERRED:** χ²(k=3) < χ²(k=1) − 4 and p(k=3) > 0.01.
- **MEASURED EXTENT PREFERRED:** χ²(k=1) < χ²(k=3) − 4 and p(k=1) > 0.01.
- **NEITHER FITS:** p < 0.01 for all k.
- **NOT DECIDED:** otherwise.
- **Two-halo flag:** an EXTENDED verdict is labelled **TWO-HALO SUSPECT** if the "clean" tier's free amplitude at k = 3 lies
  below the central tier's by more than 2σ (σ = jackknife error of the clean-minus-central difference) or if the clean
  tier's own class is not EXTENDED.
- **Dust flag:** any verdict is labelled **CIB-SENSITIVE** if the standard map's class differs.

**Reported:** free A per k, all tiers, both maps, the uncompensated profile.

**Interpretation lock.**
- tSZ measures pressure, n·T. Weak signal does not exclude cool gas at 1–3 R_vir, and route E needs mass, not pressure. So
  MEASURED EXTENT would exclude hot extended gas at 0.22 keV, not the gas route E needs.
- EXTENDED is a necessary condition only: GH2 found the law fits KiDS better than route E at any extent.
- This sample differs from GH2's KiDS lenses; centrals are less isolated.

## Checks

- **K1:** β = 2/3 projection closed form within 1e-4.
- **K2:** this script's stack, run on the KiDS bins 3–4 lenses with GH4's seed, reproduces GH4's committed compensated Y on
  the same map within 1e-6 relative.
- **K3:** pixel geometry vs WCS within 0.01 px.
- **K4:** the central fraction of the mass-selected sample lies in 0.6–0.8 (Zhang's CEN 0.68).
- **MUTATE:** random positions as lenses give a compensated null (p > 0.01).

**Scope.** Stellar masses are CIGALE, not Zhang's; a mass offset scales the model and is absorbed only in free A. DESI
fibre incompleteness leaks satellites into every tier. κ = ½ FITTED; c_f EXTERNAL; cold dark energy is a gravitating field
component, never a particle; not theory closed; nothing here says the data favour the framework. One thread, nice 15, RSS
< 3 GB.
