# JWST archive recon (JADES DR4/DR5 · COSMOS-Web · CEERS · MAST) — the decisive test is not in there, and exactly why

*C. Zimmerman, 2026-06-06. Tasked to swarm the JWST deep fields for the framework's decisive measurement (a deep-MOND,
g≪a₀, rotation curve at z≳2). Three agents queried MAST LIVE (astroquery 0.4.11 works here) + the data-release
literature. Convergent, honest verdict: the data are public and accessible, but the **acceleration regime is wrong** —
JWST resolves the compact, high-surface-density INNER regions (high g), not the low-acceleration outskirts the test
needs. The archives cannot decide a₀(z); a purpose-built lensed-dwarf campaign can. This hardens the standing
conclusion with actual archive verification.*

## What's actually there, and how to get it (verified astroquery)

- **JADES DR4** (spectroscopy, public ~Oct 2025; arXiv:2510.01033/34): **5,190 NIRSpec spectra**, 3,297 robust spec-z
  (396 at z>5.7), PRISM + 3 gratings + **2,654 G395H (R~2700)**. Products: 1D/2D spectra, line-flux + redshift
  catalogs. **No kinematics, no rotation curves, no velocity-dispersion/dynamical-mass catalog.**
- **JADES DR5** (imaging, public Jan 2026; arXiv:2601.15954/56): NIRCam mosaics (35 filters) + photometric catalog
  (>45k sources) + stellar-population (mass/SFR) catalog. **Photometry/SED only.**
- **COSMOS-Web** (GO 1727): **imaging only — 0 spectra** (628 NIRCam + 164 MIRI). Public catalog = **COSMOS2025**
  (Shuntov/Weaver 2025, arXiv:2506.03243), >700k sources, photo-z/mass/morphology. **No kinematics.**
- **CEERS** (ERS 1345): 5,441 NIRSpec/MSA + 8 NIRCam grism + imaging; photometric catalog Cox+2025 (87k). Spectra are
  *integrated* (redshifts, line widths), **not resolved deep-MOND rotation curves.**
- **The "low-z measurements" in these fields** come from *overlapping ground/HST* data, not the JWST catalogs:
  **LEGA-C** (VLT, ~3k dynamical masses at z~0.6–1.0 in COSMOS), **KMOS³D / 3D-HST** (Tully-Fisher 0.9<z<2.3 across
  COSMOS+EGS+GOODS). That low-z baseline is a real anchor — but it's the same regime-limited kinematics we already used.

Verified working queries (executed live against MAST):
```python
from astroquery.mast import Observations
Observations.query_criteria(provenance_name="JADES", instrument_name="NIRSpec")   # 15,060 NIRSpec products
Observations.query_criteria(obs_collection='JWST', proposal_id='1727')            # COSMOS-Web: 792 obs, all image
Observations.query_criteria(obs_collection='JWST', proposal_id='1345')            # CEERS: 5,564 obs (MSA+grism+img)
# field-overlap spectra from OTHER programs (EGS box) -> 28,051 spectra (RUBIES, etc.)
Observations.query_criteria(obs_collection='JWST', dataproduct_type='spectrum',
    instrument_name=['NIRSPEC/MSA','NIRCAM/GRISM'], s_ra=[214.5,215.3], s_dec=[52.6,53.1])
```
(Photometric catalogs — COSMOS2025, CEERS-Cox, JADES — download from cosmos2025.iap.fr / ceers.github.io / the JADES
HLSP DOI 10.17909/8tdj-8n28, not via `query_criteria`.)

## The decisive fact: the acceleration regime is wrong

To measure a₀(z=2)'s ~14% shift you need **g_bar/a₀ ≲ 0.3** (where the shift becomes a >5% observable). Every confirmed
z≥2 JWST/ALMA kinematic system is far above that:

| system | z | g/a₀ | usable? |
|---|---|---|---|
| **Cosmic Grapes** (lensed, RXCJ0600-z6) | 6.07 | **~1.0–1.1** | **borderline — the single best case, but only AT the boundary** |
| FRESCO/JADES/CONGRESS "geko" disks (Danhaive 2025, N=213) | 3.9–6.5 | ~3–4 | no (high-acc, dispersion-dominated, v/σ~1–2) |
| JADES NIRSpec IFU (de Graaff 2024, N=6) | 5.5–7.4 | ~1.5–5.7 | no |
| Big Wheel / Wolfe Disk / REBELS-25 / SPT0418 | 3.25–7.3 | 2.4–5.0 | no (massive disks → a₀ overestimate) |
| genuinely low-g rotators (Patrício; z=1.87 SFG) | 0.6–1.9 | 0.2–0.7 | no — **z<2** (below threshold) |

**Honest count of usable deep-MOND (g/a₀≲0.3), z≥2 systems with V+R+M_bar: ZERO** (Cosmic Grapes at ~1.0 is the lone
boundary object, and at 1 R_e it's already ~2.1; its <1 value needs extrapolating mass to radii where none is
measured). Everything low-g is z<2; everything z≥2 is high-g — because JWST resolves the bright compact cores, and
beam-smearing + dispersion support bias the outskirts. This is the physical, not pipeline, reason the test isn't in the
archive.

## Bonus: a flawed prior analysis confirmed dead
The pre-existing `ai_slop/research/z2_mond_predictions/jades_kinematic_comparison.py` is methodologically invalid:
(i) applies a deep-MOND scaling to g≈1.5–6 a₀ systems (wrong regime); (ii) uses the **a₀=a₀·E(z) ρ_total scaling** — the
known cH₀-vs-cH_Λ bug — giving a₀(z=6)≈1.1e-9 (×10 too big), then "wins" against a strawman; (iii) compares σ to σ while
ignoring the larger V_rot; (iv) M_star-only baryons (gas is ~10×). It correctly belongs in `ai_slop/` (unverified);
not salvageable as an a₀(z) test.

## What WOULD deliver the measurement (proposal-grade spec)
A clean deep-MOND a₀(z≳2) point requires **deliberately targeting low-mass, low-surface-brightness LENSED dwarfs**
(M*~10⁸·⁵–10⁹·⁵) behind high-magnification cluster caustics (μ≳10–30: UNCOVER/A2744, MACS J0600/RXCJ0600, SMACS 0723,
GLASS, Sunburst/Sunrise) and resolving their **outer** kinematics to ≥2–3 R_e (the flat part, where g drops below a₀):
- **Instrument:** JWST NIRSpec IFU (Hα/[OIII], z≈2–3.5) or ALMA [CII] (z≈4–7), with forward-modeled beam-smearing +
  pressure-support correction (³DBarolo / GalPaK³D through the lens model).
- **Sample:** ~10–20 such lensed dwarfs for a statistically meaningful a₀(z=2–3) point — a dedicated campaign (each is a
  deep integration; the Cosmic Grapes alone absorbed >100 hr ALMA+JWST). **Not an archival reanalysis.**

## Verdict
The JWST deep-field archives (JADES/COSMOS-Web/CEERS, fully public, queryable here via astroquery) give **abundance,
masses, sizes, and spec-z** — strong for structure/abundance science, and a regime-limited high-z BTFR *consistency*
point at best. They do **not** contain a deep-MOND z≥2 kinematic system, and cannot, because JWST resolves the
high-acceleration cores. The framework's decisive test is **not reachable from existing/archival data** — it requires a
purpose-built lensed-dwarf IFU campaign reaching g≪a₀ at z≳2. This is the same wall the open-doors scan hit, now
confirmed by direct archive query: the measurement that would decide `a₀∝√ρ_DE` vs constant does not yet exist.

**Sources:** JADES DR4 [2510.01033], DR5 [2601.15956]; de Graaff 2024 [2308.09742]; COSMOS2025 [2506.03243]; CEERS-Cox
[2510.08743]; Danhaive "dawn of disks" [2503.21863]; Cosmic Grapes [2402.18543]; Big Wheel (Nat. Astron. 2025);
beam-smearing systematics [2311.05832, 2509.18328].
