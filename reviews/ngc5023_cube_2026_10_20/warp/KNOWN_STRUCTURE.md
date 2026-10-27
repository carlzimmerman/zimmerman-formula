# NGC5023: source-based ordinary-structure controls

Checked 20 October 2026 (user timezone). This is a source check for
`ngc5023-cube-2026-10-20`, assessment base
`be8fc76cb0e207b88710f130abf2aa937f0895a5`. Earlier packets are unchanged.
No cube was analyzed by this source-only work package.

## Authenticated primary source and coordinates

Kamphuis et al., *HALOGAS observations of NGC 5023 and UGC 2082:
modelling of non-cylindrically symmetric gas distributions in edge-on
galaxies*, MNRAS434,2069–2093 (2013), DOI
[10.1093/mnras/stt1153](https://doi.org/10.1093/mnras/stt1153).
Exact retrieved source is [arXiv1306.5312v1](https://arxiv.org/src/1306.5312v1),
SHA256 `5ac7d289936d4ec75041a23093b009a79901f9e1423c8351c9f0321c05525181`.
The archive has TeX/BibTeX and22 PostScript figures, with no TiRiFiC `.def`,
radial parameter table or model cube. This matches the earlier packet's
version pin. `ACQUISITION.json` records bounded acquisition and all members.

Table1 and Table4 give the fitted HI center as J2000 RA13h12m11.83s,
Dec+44°02′16.9″. Table4 gives systemic velocity404.8±4km/s, central
PA28.0±1°, inclination88.5±1.3°. **The literal RA uncertainty is±4.3s of
time**, not±4.3arcsec. The retrieved v1 TeX and the publisher's indexed
Table4 both print seconds of time. At the center declination this is
±46.37arcsec east/west. The Dec uncertainty is±6arcsec. This surprisingly
large RA range should be bracketed as a literal source stress control;
silently treating it as4.3arcsec would modify the source. No erratum or
alternative clarified unit was recovered. These bounds are not a joint
Gaussian covariance: Section3.6 varies one parameter at a time until clear
model/data disagreement and averages the maximum upper/lower deviations.

The official SIMBAD identifier record independently gives an **optical
catalog position**, ICRS/epochJ2000 RA13h12m11.8036148808s,
Dec+44°02′17.328663600″, with reference2020yCat.1350....0G. It differs from
the HI center by about−0.284arcsec east and+0.429arcsec north. The record
is retained and hashed. Its astrometric precision is not an uncertainty on
the galaxy's physical/dynamical center. SIMBAD lists optical radial
velocity407km/s with separate provenance; do not substitute it for the HI
systemic velocity without frame/definition correspondence.

Section2.1 gives69 final NGC5023 channels, offline Hanning smoothing and
4.12km/s stated velocity resolution. It gives the paper's HR beam19×13arcsec
and LR36×33arcsec. The actual release FITS headers take precedence for the
downloaded cube's precise beam, grid, velocity convention and noise. HR/LR
are different imaging products of the same WSRT observations.

## Already known localized features: essential exclusions/overlays

Section2.2.1, Table2 and Figure1 identify three extended HI features. They
are explicitly separated from global disk fitting in the original paper.
The source's rotated-frame major offset is positive toward the
approaching SW side (Section3.5); positive minor offset is NW and negative
minor offset SE. Register this sign convention against the actual sky
coordinates before applying an aperture. If a new analysis uses positive
major offset toward NE, negate the table's major offsets.

| Published feature | Major offset (arcsec) | Minor offset (arcsec) | Central observed velocity (km/s) | FWZI (km/s) |
|---|---:|---:|---:|---:|
|1|+72|−80|380|56|
|2|−112|−92|444|40|
|3|−120|+76|444|52|

The prose gives feature1's radial extent as+25 to+100arcsec, and feature2's
as−150 to−50arcsec, at minor offsets approximately−75arcsec. Feature3 is
opposite feature2 on the NW side. Individual masses were not recovered
because the features blend into the disk. The quoted centers/FWZI are
descriptors, not exact source-mask boundaries or confidence ellipses.
A published-feature exclusion should remove the chosen regions **and
their point-inverted counterparts** so that the mask itself does not break
the null. A beam-sized and a deliberately broader version of that exclusion
are reasonable declared sensitivity controls, not new independent data.

These features already cause strong observed/model differences. Section3.1
says the mismatch near major offset−100arcsec and high-altitude secondary
vertical profile are due to features2/3. They disappear in a central
20arcsec-wide strip or when regions with model residual above50% are
excluded. That latter cut is data/model-dependent and must not be presented
as a blind or independently calibrated mask.

Section3.4 also identifies low-projected-velocity high-altitude extensions
at major offsets+1.7,+2.9,+4.2arcmin and minor offsets+0.4 to+1.3arcmin,
25–75km/s from systemic; weaker counterparts occur at−1.7,−2.9arcmin,
minor offsets−0.4 to−1.3arcmin and0–60km/s from systemic. These structures
are reproduced substantially better by the spiral+warp models. Therefore
a cube residual in these locations is not automatically a new object.

## What the actual warp control must address

Section3.6 and Figure12 show the preferred main disk has equal rotation
and surface-brightness profiles on the two sides, but **different PA and
inclination profiles** outside the inner shared geometry. Figure12 is
retained in original PostScript and rendered PNG. Visual reading shows
PAnear28° centrally and a greater outer PA change on the receding NE side;
the outermost values are roughly34° versus30.6°. Inclinations fall from
88.5° centrally to roughly82° in the outer disk. These are visual
descriptions only, not recovered numeric ring parameters; no forward model
should treat them as an exact20-ring solution. The source PostScript is a
raster-image wrapper, so exact plotted numerical arrays were not recovered
by parsing vector paths.

The paper fits20 rings per disk and ties the inner ten rings in PA and
inclination. Section3.5 describes the inner radius partition as175arcsec.
The arms have different radial amplitudes/phases/widths and one different
height. Section3.6 finds a lag of−9.4±3.8km/s/kpc with arms and line-of-sight
warp; removing the warp pushes the lag toward−14.5km/s/kpc. Symmetric
classical models prefer−14.9±2.7km/s/kpc (Table3). This is an explicit
projection/emissivity degeneracy already demonstrated on these data.

A centered, fully point-symmetric tilted-ring warp remains inside the
cube-inversion null, even with radius-dependent PA/inclination. Its
nonzero residual cannot be invoked by the word “warp” alone. But the
published **side-dependent** warp plus nonidentical arms does not satisfy
that symmetry and is a live ordinary explanation. Varying one global PA
does not test that model: point inversion commutes with coordinate
rotation, so the full inversion residual is rotation-invariant. Global PA
changes can affect apertures/binned decomposition, not eliminate this
source-class issue. A projected inner175arcsec cut helps assess the outer
disk, but outer-ring gas projects inward along the line of sight; it is
not a strictly warp-free volume selection.

**Full asymmetric warp/spiral subtraction remains unavailable in this
source-only package.** The actual fitted model/covariance would need an
authenticated parameter product or an explicitly uncertain reconstruction;
its hundreds of fitted nuisance parameters cannot silently be invented.

## Later overlap: global asymmetry is already measured

Reynolds, Westmeier, Staveley-Smith, Chauhan and Lagos (2020), *HI
Asymmetries in LVHIS,VIVA and HALOGAS Galaxies*, MNRAS493,5089;
[arXiv2002.11857v1](https://arxiv.org/abs/2002.11857v1). Exact v1 source
archive SHA256 `1b69cc02494080837a49992c51713f26e4d3dbe29775b70e9da7ba4ac393a8d7`.
`REYNOLDS_ACQUISITION.json` pins it; the official CDS catalog
[J/MNRAS/493/5089](https://cdsarc.cds.unistra.fr/ftp/J/MNRAS/493/5089/)
pins the full electronic TableA3, including NGC5023, in
`SUPPLEMENTARY_ACQUISITION.json`.

The NGC5023 row gives `A_spec=.066`, `A_flux=1.03`, `A_peak=1.06`,
bias-corrected `A_map=.05`, inner first-harmonic mean`.05`, and
`A_vel=.012`. No object-specific errors accompany these values in the
electronic table. Its unrelated mass/environment columns are not used
here. These are published measurements on the low-resolution HALOGAS
observations, **not independent replication**.

Sections3.1.4,3.2.1,3.2.3 define the exact relevant overlap:

- `A_spec = sum|S−S_flip|/sum|S|`, flipped about the flux-weighted mean
  systemic velocity.
- `A_map = [sum|M0−rot180(M0)|−sum|B−rot180(B)|]/[2sum|M0|]`, centered
  on the flux COM. The bias image uses the same SoFiA source mask on a
  cube region without HI emission.
- `A_vel` uses a weighted median absolute deviation of the summed moment1
  map and its180°rotation, scaled by the95th percentile of the difference
  velocity map. It is independent of a constant systemic velocity.

They used SoFiAv1.2.1 smooth+clip with3.5σ, minimum merging sizes5pixels
in spatial and spectral dimensions, reliability>.7. Their low-resolution
cube description says5arcsec pixels, whereas the actual release used in
the new test has its own header grid. Exact numeric agreement with a
new statistic/center/mask/release is therefore not guaranteed. Their
moment0 definition also includes a factor2 that some global cube
asymmetry definitions omit.

This means a few-percent **global** flipped spectrum,180°moment-map or
velocity-map residual is already studied for this exact galaxy. A
spatial/channel-local residual with controls can add information, but
neither the general symmetry method nor the existence of asymmetry is a
new discovery. Their cosmological mock-catalog environment corrections
are separate from the raw observed asymmetry definitions and are not
needed or imported here.

Deg et al. (2023), *Measuring Galaxy Asymmetries in3D*,
[arXiv2306.02839v1](https://arxiv.org/html/2306.02839v1), explicitly defines
the same full-cube point-inversion pairing in Section2.2. Its global3D
method is **known verbatim**, not merely adjacent prior art. It also
recommends symmetrizing masks. Section2.3, Eqs12–20, uses the ratio of
squared differences to squared sums and subtracts the estimated noise
contribution from both. That treatment avoids the low-SNR overcorrection
of a simple absolute-residual blank subtraction. The paper's uniform-noise
shortcut cannot automatically supply errors for correlated/interpolated
data. The versioned response hash and exact locators are recorded in
`DEG2023_SOURCE.json`; no raw HTML was retained. A localized residual not
already explained or previously reported is a separate empirical question.

## Status

Source identity, literal central parameters, known-feature positions,
global-asymmetry table values and method overlap verified in the cited
versions. Actual asymmetric ring model not recovered. Novelty classification:
known after translation for projected/global symmetry statistics and known
verbatim for the global3D cube statistic; partial or adjacent result for a
fully localized, controlled cube-inversion map.
No global search completeness, new signal, gravity inference or memory
identification follows from this source check.
