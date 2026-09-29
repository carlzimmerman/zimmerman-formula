# How to build an a0(z) timeline from heterogeneous data, and how to cut the data rigorously

Data-front proposal, 2026-09-29. It is a method note, not a result: no a0 has been fitted anywhere in `data_assembly/`. Calculations belong to the calculation thread; this file
says what the data are, how to chop them, and what to fix before any number is computed. The companion `sample_ledger.csv` records every sample's tracer, velocity and radius
definition, gas basis and pressure-support status, and proposes a tier under the rules below.

## 1. What a timeline can and cannot be
A timeline of a0 against cosmic time is a set of independent estimates, each from one homogeneous piece of data, laid side by side with the competing predictions drawn on the
same axes BEFORE the data are inspected: flat a0 (the framework's law), a0 proportional to H(z) (the rival) and the LCDM-native expectation. Pieces are never pooled across tiers
unless they agree, and a piece with no sensitivity to a0 is shown as uninformative, not as a point.

## 2. Compare through one common observable, not through a0
The quantity that can be compared across tracers is the offset of each object from the LOCAL relation at fixed baryonic acceleration:
Delta = log10(g_obs) - log10(g_RAR,local(g_bar)), where g_RAR,local is the z = 0 relation calibrated on SPARC (the repo already holds SPARC). An a0 ratio is derived from Delta only
where the relation is sensitive to a0. This keeps CO, HI, Halpha and [CII] pieces on one axis and lets each carry its own systematic.

## 3. Cuts declared BEFORE any Delta is computed (pre-registered, hashed, append-only, like the Gaia DR4 pre-registration)
1. **Information cut, by physics not outcome.** For each object compute the sensitivity s = d ln g_obs / d ln a0 at its declared g_bar from the local relation. Objects with s below a declared
   threshold (for example g_bar above 3 a0) carry almost no information and are excluded for that reason. The threshold is written down first.
2. **Rotation support.** Require a stated V/sigma cut (for example V/sigma >= 1) using each sample's own definition; dispersion-dominated objects go to a separate stratum, not into the main one.
3. **Radius.** Require a stated radius per object (tabulated, digitised, or a declared multiple of a tabulated size). Samples with an undefined radius (Tacconi+2013, Ubler+2017) are excluded from the acceleration analysis.
4. **Gas basis is a stratum.** measured cold gas (CO/HI) with a declared conversion bracket; scaling-relation gas; no gas; model-fitted baryons. Each is analysed separately.
5. **Velocity definition is a stratum.** observed rotation velocity; pressure-corrected circular velocity; model circular velocity. Two declared variants, reported side by side.
6. **Quality flags** come from the source and are applied as written (KinType, Rout_Flag, classification, Disk Score); no flag is chosen after seeing its effect.

## 4. Homogenise with declared choices, each with a bracket
- Disc scale radius from R_eff/1.68 (declared), seeing correction ignored or included as a second variant.
- alpha_CO and line ratios: a bracket, never a single value. HI from a declared route.
- Baryon model: exponential disc plus optional bulge, spherical shortcut as a second variant.
- Pressure support: observed V and pressure-corrected V both carried; at KURVS radii the correction can dominate (sigma0 40-155 km/s at 6 disc scale radii), so the two variants must both appear in every result.

## 5. Controls that make the result believable
- **Same-pipeline z = 0 anchor for each sample** (KROSS with matched SAMI, Tiley+2019). A method-localised shift cancels; the MUSE-DARK III rise is reproduced by LCDM simulations for exactly this reason.
- **Mock recovery:** inject a rise and a flat law into mock samples with each sample's selection, resolution and errors; report the sensitivity actually achieved.
- **Mutation controls** as in the repo's other lanes: shuffle redshift labels, shift radii by a stated amount, invert the sign of the trend; each must destroy or reverse a claimed effect.
- **Leave-one-sample-out and tier-by-tier** results; a trend that needs one sample is not a trend.
- **Blind the sign** of the trend until the pipeline and cuts are frozen.

## 6. Building the timeline
1. Bin by cosmic time, with bin edges chosen to equalise INFORMATION (sum of s^2 / sigma^2), not counts.
2. Per bin: Delta with statistical error and a systematic budget from Section 4; convert to an a0 ratio only where s is large enough.
3. Put independent non-galaxy pieces on the same axis as separate rows: the local anchor (z = 0), wide binaries (Gaia DR4, pre-registered), clusters, lensing, and the CMB-era constraint. They are not pooled.
4. Overlay the three predictions fixed in advance; report the likelihood ratio with priors written down beforehand.

## 7. Where the present data stand against these rules (facts from `sample_ledger.csv`)
- Meets radius and rotation-support rules and reaches low acceleration: KURVS-CDFS (Halpha, z 1.2-1.6, velocities at 3 and 6 disc scale radii). It lacks a gas mass and a pressure-support treatment at those radii, so it is Tier B.
- Has measured cold gas and a stated radius: ALPAKA I (19 disks), Amvrosiadis+2025, Lelli+2023. All need a declared conversion factor and, for ALPAKA I, a baryon model; their outermost total accelerations are 2-32 a0, about 10 a0 and above 3-4 a0.
- CRISTAL (z 4.4-5.7) reaches g_bar below a0 only inside a model whose baryon mass is fitted to the same kinematics; Tier C.
- Nothing yet has both a measured gas mass and a low-acceleration outer radius.

## 8. What would move a piece up a tier
Gas mass for KURVS (PHIBSS-type CO or an ALMA follow-up) moves it to A; the COSMOS half of KURVS adds 21 galaxies; gas conversion brackets and R_ext/R_e for ALPAKA I move it to A; a pressure-support-free tracer (HI, or CO with V/sigma > 5) at the KURVS radii would settle the correction.

## Correction (2026-09-29): SPARC `repo_location` in `sample_ledger.csv`
The SPARC row of `sample_ledger.csv` gives `real_research/data/SPARC_table.txt` as its `repo_location`. That file is an HTML 404 page, not data (see `real_research/data/SPARC_table.README.md`). The SPARC anchor's actual files are `real_research/data/SPARC_Lelli2016c.mrt` (Table 1, 175 galaxies) and `real_research/data/sparc_data/*_rotmod.dat` (the rotation curves). The ledger row itself is left unchanged; no script reads that column.
