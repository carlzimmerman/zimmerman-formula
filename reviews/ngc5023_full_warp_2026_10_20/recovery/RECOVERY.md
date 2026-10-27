# Recovered author baseline and digitized preferred disk

Checked20October2026. Scope: `ngc5023-full-warp-2026-10-20`, base
`c821a8bccc8a20e107b4c6771d31e02d05aa8b10`. Only this recovery directory
was written. No author code was executed and no dependency installed.

## Actual author model recovered, with a material version distinction

A fresh recovery path inspected the lead author's public repositories
rather than repeating the earlier article/archive-only search. The exact
GitHub tree commit for [PeterKamphuis/pyHIARD](https://github.com/PeterKamphuis/pyHIARD)
is `9688d31c7ae0c857039d19b8f0a52f205c8b655c`. Its
`pyHIARD/Resources/Cubes/NGC_5023/NGC_5023.def` is retained as
`pyHIARD_NGC_5023.def`. The companion `NGC_5023.py` downloads the actual
HALOGAS-HR cube and explicitly attributes this model to Kamphuis2013.
The file's source blob SHA is `4d9216967f5ffbf95f1e05419c1b3fed370d6855`.

**This is an authentic author-provided baseline model, not the preferred
asymmetric warp/spiral model.** It identifies itself as `BaseModel-hr`, has
two azimuth-restricted half disks, constant inclinations, different rotation
and brightness profiles per half, and no supplied Gaussian arms or lag.
The preferred source instead requires side-dependent inclination warp,
shared rotation/SBR and two added arm disks. The retrieved file cannot
silently replace that model. It is a useful independent renderer benchmark
and source-defined alternative.

The public file history has two returned revisions:2021-12-17
`d662219c5f5250e18f10e073266bc8340670d94a` and2023-11-03
`8fd948f3556b759aa01fd057dc8f72f3889090fc`. Both were retrieved and both
contain two half disks without supplied arms/lag. Metadata/byte hashes
and history coverage are in `AUTHOR_REPOSITORY_SEARCH.json`,
`AUTHOR_MODEL_ACQUISITION.json` and `AUTHOR_HISTORY_SEARCH.json`.
Author repositories FAT, pyFAT-astro, Disk_Simulations and TRM_errors
were also checked by recursive filenames; no object-name match was found.
That is a filename scope, not an exhaustive content/history/nonpublic search.
No exact preferred `.def` or preferred model cube was recovered.

Literal baseline details, also parsed in `author_baseline_parameters.json`:

* `NDISKS=2`, `NUR=20`, `RADI=0,19,...,361arcsec`.
* First half: `AZ1P` defaults0, `AZ1W=180`; second: `AZ1P_2=180`,
  `AZ1W_2=180`. They are approaching and receding halves respectively.
* `INCL=88.1009deg`, `INCL_2=87.7361deg`; `Z0=Z0_2=10.5415arcsec`.
* `LTYPE=LTYPE_2=3` (normalized exponential), `CONDISP=10km/s`.
  No SDIS or DVRO values are supplied, so documented defaults are0.
* Both centers: RA198.049316deg,Dec44.0380178deg. Systemic velocities
  404.823 and406.228km/s differ between the halves.
* The restoring beam19.1036x13.4223arcsec,BPA0.383774966deg agrees
  with the current HALOGAS-HR release header to its printed precision.
* SBR is face-on Jy km/s arcsec², not projected intensity per beam.

The literal file and its companion are evidence, not instructions to run
their shell operations, install software or change the original data.

## Preferred Figure12 profiles reconstructed graphically

The existing exact arXiv1306.5312v1 source PNG was copied byte for byte as
`figure12_source.png` (2237x2591 native pixels). It has20 visible radial
nodes over0..6arcmin. All coordinate readings use native pixels, not
the UI's resized display. Black dashed means approachingSW; red solid
means recedingNE. Rotation and face-on SBR are equal between the halves.

The runnable digitizer explicitly records the marker centers, printed tick
calibrations and affine transforms. Its primary result is
`digitization_run002/ring_profiles.json`; its completed v2 manifest validates
with current source hashes. `digitization_overlay.png` shows every chosen
marker position over the source graph for inspection.

Conservative graphical halfwidths are2pixels radially and5pixels vertically:

| Quantity | Graphical interval halfwidth |
|---|---:|
| Radius |0.448arcsec|
| Inclination |0.213deg|
| PA |0.109deg|
| Rotation speed |0.506km/s|
| SBR |5.32e-6Jy km/s arcsec²|

These cover line width, colored/black marker overlap, axis and endpoint
reading. They are not Gaussian uncertainties or independent per-ring
errors. Ring-center/edge/support/interpolation alternatives are additional
structural uncertainty. In particular the exact author baseline grid
0..361arcsec is a distinct source version; a graphical marker-spacing
check is consistent with the preferred plot0..360arcsec. The two must not
be silently equated. Interpolating the plotted values to either plausible
grid and changing the final half-cell support is a legitimate declared
reconstruction sensitivity, not hidden graphical precision.

The exact Table4 central PA28deg and inclination88.5deg can supersede
subpixel raster jitter in the inner tied rings. The digitizer retains its
literal measurements so that this choice remains visible.

Checks all pass:20 ordered nodes, central PA/inclination consistent with
Table4 within the graphical envelopes, outer rotation consistent with the
reported87.6+/-5km/s and nonnegative brightness. Integrating the digitized
face-on column at the paper's6.6Mpc gives4.7387e8Msun, within the published
disk4.8+/-0.26e8Msun. Direct right-axis SBR integration gives46.2565Jy km/s.
This is a useful independent normalization check. The nearby-galaxy distance
enters only this source-mass check; the angular renderer need not assume it.

The first bounded run failed only because NumPy boolean check values were
not JSON serializable. Its source is archived as
`digitize_rings_v1_failed.py`, and the failed run is preserved. The new
run casts those checks to Python bool; no physical calculation was changed.
Do not treat the historical failed manifest as current-input evidence.

## Required forward conventions

Primary code-author [TiRiFiC geometry documentation](https://gigjozsa.github.io/tirific/model_geometry.html)
is retained/hashed separately. It establishes angular radial nodes and
default linear interpolation; exponential `LTYPE=3` means
`exp(-abs(z)/Z0)/(2Z0)`. PA is measured from North toward the receding
major axis. Azimuth origin for arm phases/wedges is the **approaching**
major axis, with the documented counterclockwise convention. Gaussian
arm width GAkD is in spatial arcsec, not angular degrees; GAkP is degrees.
The coordinate system has axes North,East,toward the observer, so positive
intrinsic LOS velocity decreases the observed recession velocity.

These docs are current primary software documentation, not a hash-pinned
2013 binary manual. Preserve that version qualification when claiming an
exact reproduction. Published Table4 one-parameter visual deviation ranges
remain separate from graphical error, and neither supplies a joint
parameter posterior or covariance matrix.
