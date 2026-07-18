# Membership / Phase-Space Inventory Lane

**Scout:** cluster-EFE sigma-spread "nearest bite" (MaNGA/SAMI diffuse-dwarf reanalysis, D(zone) = <ln(sigma_int/sigma_bary)>_zone − <>_ancient at fixed deprojected caustic-a_ext bin, Rhee+2017 infall zones, MG = 0 theorem).

**My charge:** is Rhee-zone infall tagging + caustic a_ext binning *available* for the nearby (z<0.1) clusters that host the IFU carriers, and does DESI DR1 BGS meaningfully deepen membership vs the SDSS-era catalogs?

**Bottom line:** The membership/phase-space side is **not the bottleneck** — it is abundant, mature, and DESI DR1 BGS deepens it ~9.5×. The bottleneck is the **IFU diffuse-carrier count**. Stacking both public IFU surveys (MaNGA + SAMI cluster) yields only **~150–200 diffuse tagged members**, ~1.7–3× short of the 300–500 target → **NO-GO / underpowered** for a standalone 2–3σ exploratory test on public data *today*. Honest both ways: this is a real, statistics-driven no-go, not a manufactured deficit — the physics observable is clean (MG = 0 theorem-grade), the *data* is not yet there.

---

## (1) Phase-space tagging + caustic infrastructure — READY

Rhee zones need per-galaxy `(R_proj/R200, |Δv_los|/σ_cl)`; caustic a_ext needs a per-cluster caustic mass/accel profile `M(<r)` traced by enough spectroscopic members. Both are public for hundreds of z<0.1 clusters:

| Catalog | Clusters | z | Members | Provides |
|---|---|---|---|---|
| **GalWCat19** (Abdullah+2020, ApJS 246:2, SDSS-DR13) | 1800 | 0.01–0.20 | 34,471 | σ_cl, M & R at Δ=500/200/100/5.5 → caustic-ready + Rhee coords |
| Yang+2007/2012 SDSS groups | >400k grp | 0.01–0.20 | >600k | halo mass, R180, membership |
| redMaPPer SDSS (Rykoff+2014) | 26,000 | 0.08–0.55 | >1e6 photo | λ→M200; mostly *above* the IFU z-range |
| HeCS / HeCS-omnibus (Rines+2013,2016) | 58 | 0.02–0.30 | >20,000 | dedicated caustic mass profiles |
| **SAMI cluster survey** (Owers+2017, MNRAS 468:1824) | 8 | 0.029–0.058 | 2,899 | σ200, R200, caustic+virial mass — tailored to the IFU footprint |

The SAMI cluster survey is the cleanest anchor: 8 low-z clusters (A85, A119, A168, A2399, A3880, A4038, EDCC442, APMCC0917), 2,899 confirmed members, caustic masses already published, and it *is* the IFU footprint. GalWCat19 + HeCS extend caustic-grade profiles to hundreds more.

**Verdict:** phase-space coords + caustic a_ext profiles are already public. This side does not limit the test.

## (2) DESI DR1 BGS — does it deepen membership? YES

- Density **854 deg⁻²**, >5.5M reliable redshifts (Hahn+2023; DR1). BGS BRIGHT r<19.5 (z_med≈0.20), FAINT color-selected 19.5<r<20.175.
- vs SDSS Legacy main spectroscopy (~90 deg⁻², r<17.77) → **~9.5× more spectroscopic members per cluster**.
- BGS FAINT reaches **75–85% completeness for −15.5<Mr<−14.8 at the Coma redshift** — i.e. into the dwarf regime; DESI EDR already had 3,292 spectra within ~4σ of Coma.

DESI DR1 sharpens the **caustic denominator** (cleaner a_ext profiles) and tags fainter members. But it delivers redshifts, **not resolved IFU σ maps** — so it improves the tagging/binning, not the carrier count. Genuinely useful, not the fix.

## (3) IFU carrier overlap — the binding constraint

Diffuse deep-MOND carriers: σ_star ~ 20–70 km/s (a_in < ~1.5 a0); L* and bright ellipticals (σ>100) are adiabatic-dead and carry ~none. Both public IFU surveys are stellar-mass-limited, which cuts exactly these carriers:

- **MaNGA DR17:** 10,059 galaxies, ~flat in log M* for logM>9.0, floor ~5e8. Instrumental LSF ~70 km/s (1σ); DAP stellar σ reliable only above ~half the LSF (~45 km/s) at typical S/N — the *lower half of the carrier band is marginal*. Cluster-member dwarfs are rarer than field dwarfs.
- **SAMI cluster:** 906 IFU galaxies in the 8 clusters, but M* floor **logM>9.5** (higher than MaNGA) hits the deep-MOND dwarfs even harder; higher spectral resolution (R~4500) helps σ reliability.

Transparent overlap arithmetic (`inventory_membership.py`, prove-by-moving):

```
MaNGA:  10059 × f_cluster 0.10 × f_diffuse 0.18 × f_sigma_reliable 0.50 × f_taggable 0.85 ≈ 77
SAMI:     906 × f_cluster 1.00 × f_diffuse 0.15 × f_sigma_reliable 0.70 × f_taggable 1.00 ≈ 95
STACK ≈ 172 diffuse tagged members   vs target 300–500  → ~1.7× short → NO-GO
```

Signal magnitude (framework-committed E10, τ_mem=203 Gyr): ~0.3–1.5% ABSOLUTE / ~4–9.5% RELATIONAL D(zone). Per-galaxy σ error at σ~20–70 km/s is ~5–15%, so beating it down to see a ~few-% relational swing needs *hundreds* of carriers. ~150–200 does not clear it.

## What is needed (named)

- A dedicated **dwarf-IFU cluster survey** pushing the M* floor to logM~8, OR
- A **MaNGA + SAMI + Hector** stack with a low-σ-reliability re-reduction (recover σ<45 km/s), OR
- **ELT/HARMONI**-class resolved kinematics of cluster dwarfs.

The tagging/caustic scaffolding (GalWCat19 + HeCS + SAMI-Owers + DESI DR1 BGS) is ready and slots straight in the moment the diffuse-carrier IFU sample exists.

---

*Data-availability go/no-go only. Not a physics claim. No "proves". Estimate from published catalog metadata; no real cross-match performed.*

### Sources
- MaNGA DR17 sample / σ floor: sdss4.org/dr17/manga (DAP); MaNGA morphology DR17 (arXiv:2510.12792, 10,059 gals); LSF-to-subpercent (arXiv:2011... Law+2021).
- SAMI cluster: Owers+2017 MNRAS 468:1824 (arXiv:1703.00997) — 8 clusters, 2,899 members, logM>9.5 floor.
- GalWCat19: Abdullah+2020 ApJS 246:2 (arXiv:1907.05061) — 1800 clusters, 34,471 members.
- Rhee+2017 phase-space zones: ApJ 843:128 (10.3847/1538-4357/aa6d6c).
- DESI BGS: Hahn+2023 AJ (arXiv:2208.08512), DR1 854 deg⁻² / >5.5M z; Coma-faint completeness from DESI cluster-membership work.
- HeCS: Rines+2013 (ApJ 767:15) / HeCS-omnibus Rines+2016.
