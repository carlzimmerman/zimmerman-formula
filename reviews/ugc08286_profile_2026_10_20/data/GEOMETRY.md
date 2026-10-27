# UGC08286 input and geometry authentication

Checked 2026-10-20. This lane authenticates the published inputs and the assumptions needed by a disk forward model. It does not fit the rotation curve. Original datasets and scripts were read without execution or mutation. All files written by this lane are in this `data/` directory.

## Decision for the inversion

Use the 17 inclination-corrected `SBdisk` values in `UGC08286_rotmod.dat` for a conditional radial-light reconstruction, with declared interpolation, inner continuation, outer continuation and resolution controls. Use the published exponential vertical law, nominal height **0.2021477434 kpc**, for the stellar component. A forward calculation must first reproduce the published `Vdisk` template to stated accuracy; no fitted normalization may hide a failure of that control.

The full 65-point 3.6-micron photometry was recovered, but its downloadable values are **projected**. The exact transformation that SPARC applied to this edge-on galaxy is not specified in these files or in the authenticated main-paper text. Therefore a fully sampled intrinsic radial light profile has **not** been independently authenticated. An Abel inversion of the `.dens` profile is not justified: it is not a measured vertically integrated strip. This limits the geometric interpretation of any stellar-gradient result.

## Primary ASCII inputs and matching copies

The [SPARC primary index](https://astroweb.case.edu/SPARC/) distinguishes three products: raw on-sky photometry; bulge/disk decompositions uncorrected for inclination; and mass models with inclination-corrected stellar profiles. The index identifies the master paper and original curve references. Downloaded on 2026-10-20:

| Saved file | Primary URL or archive member | Contents |
|---|---|---|
| `SPARC_Lelli2016c.mrt` | [Table 1](https://astroweb.case.edu/SPARC/SPARC_Lelli2016c.mrt) | Full published sample table and reference dictionary |
| `MassModels_Lelli2016c.mrt` | [Table 2](https://astroweb.case.edu/SPARC/MassModels_Lelli2016c.mrt) | Full published mass-model table, including column notes |
| `UGC08286_rotmod.dat` | `UGC08286_rotmod.dat` in [Rotmod_LTG.zip](https://astroweb.case.edu/SPARC/Rotmod_LTG.zip) | All 17 rotation/mass-model points, eight numeric columns |
| `UGC08286.sfb` | `UGC08286.sfb` in [sfb_LTG.zip](https://astroweb.case.edu/SPARC/sfb_LTG.zip) | All 65 on-sky photometric points; radius arcsec, surface brightness mag/arcsec², inclusion flag, quoted error |
| `UGC08286.dens` | `UGC08286.dens` in [BulgeDiskDec_LTG.zip](https://astroweb.case.edu/SPARC/BulgeDiskDec_LTG.zip) | Same 65 radii in kpc and projected luminosity surface density; zero bulge |

`REMOTE_ACQUISITION.json` pins archive hashes, member hashes, URLs and response headers. Archives were read in memory; only the relevant ASCII member was retained. `MANIFEST.json` pins every retained ASCII input. The remote rotation file is byte-identical to all three existing copies:

- `real_research/data/sparc_data/UGC08286_rotmod.dat`;
- sibling `hali_flow/sparc_data/UGC08286_rotmod.dat`;
- sibling `zimmerman-formula 2/sparc_data/UGC08286_rotmod.dat`.

All four copies are 850 bytes, SHA-256 `8d22e60665ae11d1c8d510cf69ca88e7c132d39490bfb1e259b3972406bac0b6`. Remote Table 1 is byte-identical to the local table, SHA-256 `5aa0501f6b0d881fa579030e315e7b5b6ef561a5bd3a07472f9929c7e5728243`. Independently selecting the 17 UGC08286 rows from remote Table 2 gives exactly the same eight numbers as `rotmod`, at every row, with assumed distance 6.5 Mpc.

## Object and catalog parameters

UGC08286 = NGC5023 = PGC045849 is independently listed by the primary [Updated Nearby Galaxy Catalog object entry](https://www.sao.ru/lv/lvgdb/object.php?id=344&name=NGC5023). The existing local Sesame alias match agrees. The catalog's present distance is a separate value, not a replacement of the frozen SPARC distance.

The exact SPARC Table 1 row is:

```text
UGC08286 6 6.50 0.21 2 90.0 3.0 1.255 0.018 2.25 39.52 1.05 1488.78 0.642 8.07 82.4 2.3 1 Sw09,Sw02
```

| Quantity | Value at the frozen SPARC footing |
|---|---|
| Hubble type | 6 = Scd |
| Distance | 6.50 ± 0.21 Mpc |
| Distance method | 2 = tip of the red giant branch |
| Kinematic inclination | 90.0 ± 3.0 degrees |
| Total [3.6] luminosity | (1.255 ± 0.018) × 10⁹ Lsun |
| Effective radius | 2.25 kpc |
| Mean effective surface brightness | 39.52 Lsun/pc² |
| Outer exponential disk scale length | 1.05 kpc |
| Tabulated extrapolated central disk SB | 1488.78 Lsun/pc²; not an admissible intrinsic normalization here |
| HI mass | 0.642 × 10⁹ Msun |
| HI radius at 1 Msun/pc² | 8.07 kpc |
| Flat speed | 82.4 ± 2.3 km/s |
| SPARC quality | Q = 1 |
| Original HI references | Sw09, Sw02 |

The raw curve covers **0.47–8.04 kpc**, with all **17** points retained. The photometric grid covers **0.02048–9.17183 kpc**, corresponding to 0.65–291.05 arcsec at 6.5 Mpc. All 65 supplied inclusion flags equal one. No bulge is present in any product.

## Geometry, signs and units

[Lelli, McGaugh & Schombert, AJ 152:157 (2016)](https://astroweb.case.edu/ssm/papers/AJv152n157.pdf), DOI [10.3847/0004-6256/152/6/157](https://doi.org/10.3847/0004-6256/152/6/157), published 2016-11-11, §3.3, is the authenticated journal version; arXiv:1606.09251v1 was also checked. It specifies an exponential stellar vertical density and the empirical rule `h[kpc] = 0.196 (Rd[kpc])^0.633`, with no edge-on exception stated. Thus the model uses `rho(R,z) = Upsilon(R) I(R) exp(-abs(z)/h)/(2h)`. This height is an adopted relation, not a direct measured height for NGC5023. The observed radial light profile is continued exponentially beyond its measured extent unless truncated. Gas is represented by a thin disk, with helium included by multiplying HI mass by 1.33; molecular gas is omitted. Stellar templates use M/L = 1. The signed velocity convention is equation (2).

In particular, define inward radial acceleration as positive. At each supplied radius,

```text
g_gas = Vgas * abs(Vgas) / R,
g_star = Upsilon * Vdisk² / R,
g_bar = g_gas + g_star.
```

Use km/s and kpc with conversion `1 (km/s)²/kpc = 10⁶/3.0856775814913673e19 m/s²`; AG4g/h instead used the rounded kpc conversion `3.0857e19 m`. The first three gas terms are outward: signed squared speeds **−14.8225, −1.9044 and −0.3969 (km/s)²**. Negative `Vgas` is not negative mass; exterior gas can pull outward across a central depression. Squaring away this sign changes the inherited baseline. The gas velocity template already includes helium and must not be multiplied by 1.33 again.

The `CFG4_common.load_sparc()` input path is exactly `real_research/data/sparc_data`, and the metadata path is `real_research/data/SPARC_Lelli2016c.mrt`. It reads only the first six rotation columns into the loader; our copied ASCII preserves the light columns as well. The owner's code was inspected, not run.

## The projected-light mismatch

The `.sfb` and `.dens` grids agree under the catalog distance, and obey `mu + 2.5 log10(Sigma_projected) = 24.81207507` to their printed precision. Their relation is a unit conversion, not deprojection. By comparison the rotation file has already corrected surface densities, e.g. **82.49 Lsun/pc² at 0.47 kpc**, while the projected profile there is approximately **555 Lsun/pc²** under linear interpolation.

Integrating `2pi R Sigma_projected` over the supplied 65 radii by a trapezoid yields **8.454857965 × 10⁹ Lsun**, far above the tabulated total **1.255 × 10⁹ Lsun**. Their ratio **0.1484354** is only a diagnostic of a substantial projection correction. It is not an authenticated inclination, deprojection operator or fitted scale factor. It must not be adopted to force a rotation-template match. The central extrapolated Table 1 SB combined with a pure exponential would similarly imply about **1.03 × 10¹⁰ Lsun**; that inappropriate combination is excluded.

The journal paper §3.1 describes a narrow circular sector about the semimajor axes for thin edge-on photometry. It does not supply this object's sector aperture, vertical light integral, ellipse-ratio sequence, correction algorithm or intrinsic deprojection. Therefore neither multiplying the full profile by `cos(90°)` nor applying an Abel inverse to this one-dimensional sector profile is supported. The corrected 17 points are valid published model inputs, but are not proof that line-of-sight mixing has been uniquely removed.

## Original observation and errors

`Sw09` is **Swaters, Sancisi, van Albada & van der Hulst, A&A 493, 871–892 (2009)**, *The rotation curves shapes of late-type dwarf galaxies*, DOI [10.1051/0004-6361:200810516](https://doi.org/10.1051/0004-6361:200810516); inspected [arXiv:0901.4222v1](https://arxiv.org/pdf/0901.4222v1), §§3.1–3.4, Table 2 and §5. It states that 15-arcsec sampling of 30-arcsec HI data makes adjacent points dependent. Edge-on curves use line-profile envelope tracing with an assumed 8 km/s gas dispersion. The method can be biased by a central gas hole or ring. UGC8286 has original quality 2, inclination 90°, and HI/Halpha disagreement near the curve turnover. The source excluded edge-on objects from its own shape analysis; its quality flag differs from SPARC's.

`Sw02` is **Swaters, van Albada, van der Hulst & Sancisi, A&A 390, 829–861 (2002)**, *The Westerbork HI survey of spiral and irregular galaxies. I. HI imaging of late-type dwarf galaxies*, DOI [10.1051/0004-6361:20011755](https://doi.org/10.1051/0004-6361:20011755), [published primary PDF](https://www.aanda.org/articles/aa/pdf/2002/30/aah3074.pdf). Its bibliographic identity and role as the HI surface-density source were authenticated; its plotted radial HI profile has not been digitized or independently reconstructed here. The supplied SPARC signed gas-force template is retained.

Table 2's own notes identify `errV` as a random uncertainty from noncircular motions and/or kinematic asymmetries and explicitly omit inclination systematics. The quoted errors are **2.00–3.47 km/s**. No covariance matrix, beam response matrix or component-velocity uncertainty array is supplied. Therefore row-wise intervals and diagonal propagation are conditional error summaries; they cannot justify an independent-17-point chi-square likelihood. Likewise the photometric errors share sky estimation and do not provide a radial covariance matrix.

For fixed geometry, first-order propagation is `sigma_gobs = 2 Vobs errV/R`. Coherent distance/inclination alternatives should be applied as coherent changes, not additional independent point noise. The original edge-on construction and turnover mismatch remain material systematic limitations even though SPARC assigns Q1.

## Distance and inclination transformations

Under a **homologous** distance change `lambda = D_new/6.5 Mpc`, angularly corresponding radii and vertical height scale by `lambda`, luminosities/masses by `lambda²`, surface density is unchanged, and squared baryonic template speeds scale by `lambda`. Hence baryonic acceleration is invariant while `g_obs` scales as `lambda^(-1)`. If the empirical height rule is instead re-applied at each distance, `h` scales as `lambda^0.633`, so the dimensionless thickness changes and the velocity-template homology is only approximate. State which convention is used.

At fixed observed line-of-sight velocity, `Vobs_new = Vobs_SPARC sin(i_SPARC)/sin(i_new)`. Near 90°, this kinematic correction is second order: moving to 87° raises V by only 0.137%. This does not establish the stellar photometric correction; a line-of-sight light deprojection has a different geometry and cannot use the kinematic `cos(90°)`.

## Relation to the inherited AG4h result

AG4g supplies AG4h's data. Its radius/positivity cuts retain every UGC08286 point: positive observed speed, positive radius and baryonic acceleration at both ends of its M/L grid, finite observed acceleration, at least five retained rows. It does **not** impose an `errV/V < 0.1` cut here. AG4g/h use signed gas, a fixed 0.05-dex comparison floor, and `2 errV/(ln(10) Vobs)` with a 1 km/s error clip, which is inactive for this galaxy. Their floor is inherited bookkeeping and is not a measured covariance or a new noise term for this inversion.

For comparison only, the owner's saved AG4h record reports UGC08286 pull +3.70, `dchi2 = 15.8620044077`, coherent offset 0.1805487152 dex, and prior-free constant M/L 1.6179683; root's separate implementation must reproduce it. The saved CF4 cross-match gives 5.915616 Mpc versus SPARC 6.5 Mpc. Both catalog distances should remain labeled; their agreement does not authenticate photometric deprojection or remove HI systematics.

## Verification and source-status record

Run `python3 data/verify_inputs.py` from this packet or with its absolute path. It only reads inputs, emits JSON and exits nonzero on a mismatch. `INPUT_VERIFICATION.json` records the run. SHA-256 hashes are identity/provenance checks, not a physical validation of deprojection.

- **Verified:** exact ASCII identity, all 17 mass-model rows, complete 65-point projected photometry, alias, table parameters, signed gas convention, published generic vertical model, original observation/error caveats.
- **Conditional:** a 17-point corrected-light reconstruction and nonlocal stellar-gradient kernel, contingent on explicit continuation controls and forward-template agreement.
- **Unverified:** the fully sampled intrinsic stellar light profile and its edge-on deprojection, object-specific stellar height measurement, gas mass-profile reconstruction from original HI data, full radial observational covariance.
- **Retention:** public authoritative ASCII data only; no full copyrighted paper text/PDF was copied into this packet. No novelty search or claim was made. Literature checks authenticated sources and extracted the cited definitions/assumptions; no `.mathbox` source evidence was written.
