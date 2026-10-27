# Published extensions and the newly selected residual boxes

Checkpoint `ngc5023-full-warp-2026-10-20`, base
`c821a8bccc8a20e107b4c6771d31e02d05aa8b10`. Source-only check on
20 October 2026. The candidate coordinates were supplied by the parent
analysis. No new cube measurement, model fit or independent-data result
was used for this note.

The strongest supplied box, centered at(x,z,u)=
(−220arcsec,−60arcsec,−49.44km/s), overlaps an already published
low-velocity, high-altitude extension region. Excluding the three
Table2 feature boxes does **not** place this box outside all known HI
structure. The two supplied positive-u guarded boxes are spatially near
the published feature1 region, but their velocity offsets prevent a
secure feature1 identification from the source alone.

## Primary-source locators and coordinate registration

Source: Kamphuis et al. (2013),
[arXiv1306.5312v1](https://arxiv.org/abs/1306.5312v1), published as
[MNRAS434,2069](https://doi.org/10.1093/mnras/stt1153).
The immutable retained TeX is
`reviews/ngc5023_cube_2026_10_20/warp/Kamphuis_2013.tex`, SHA256
`2323426866bdb41e15fed1a528847befeb446e1a334eb412b7d72cf3b007f600`.
Locators below use that exact TeX's line numbers and figure labels.

The paper's positive major offset is toward the approaching SW side
(§3.5, line290); its positive minor offset is NW, while negative is SE
(§2.2.1, line127; Figure9 caption, lines284–287). The analysis uses
positive x toward NE and positive z toward SE. Thus

`x_analysis = −major_paper`, `z_analysis = −minor_paper`,
`u_analysis = V_hel −404.8km/s`.

The current sampling code independently confirms the last convention by
sampling at `U+404.8+dv` in `cube_analysis.py`. No distance or cosmology
is involved in this registration. The source's approaching/receding
velocity sign is also visible directly in Figures6/7: positive-major
rows lie below systemic velocity; negative-major rows lie above it.

## The top box is in the previously discussed extension family

At §3.4, line264, the authors distinguish an extended low-projected-
velocity component from both the simple lag model and the three Table2
localized features. They identify it in the positive-major PV cuts near
1.7,2.9 and4.2arcmin, at positive minor offsets0.4–1.3arcmin and
velocities25–75km/s from systemic on the approaching side. They also
describe weaker counterparts in negative-major cuts near−1.7 and−2.9
arcmin, on the negative-minor side, at0–60km/s from systemic.

In analysis coordinates the first family has z approximately−78 to−24
arcsec and u approximately−75 to−25km/s, at sampled major positions
x approximately−102,−174,−252arcsec. The plot labels are more exactly
1.67,2.92,4.17arcmin, so these rounded prose positions must not be
mistaken for exact mask boundaries. Figures6/7 show the corresponding
data contours; blue dashed boxes mark some representative extensions.
The absence of a dashed box in every row is not an absence of emission.

For the supplied40×40arcsec×24.72km/s top box:

| Quantity | Analysis footprint | Paper-frame footprint |
|---|---|---|
| Major position | x=−240 to−200arcsec | +200 to+240arcsec = +3.333 to+4.000arcmin |
| Minor position | z=−80 to−40arcsec | +40 to+80arcsec |
| Velocity | u=−61.80 to−37.08km/s | V_hel=343.00 to367.72km/s |

Its minor/velocity footprint substantially overlaps the explicit prose
ranges; the last2arcsec in minor position extend beyond their rounded
78arcsec upper value. Its major footprint lies between the2.92 and4.17
arcmin sampled cuts. The prose alone does not establish a continuously
filled three-dimensional rectangle between those cuts.

Figure9 supplies a more direct check without inventing that rectangle:
its **top-left data panel, labeled minor offset+50arcsec**, contains
published emission contours over positive major offsets approximately
3.3–4.0arcmin at velocities in the343–368km/s range. That nominal slice
falls inside the new box's minor footprint. The corresponding top-right
panel is the published preferred spiral model. This is qualitative
coordinate overlap with previously plotted emission, not a digitized
flux or exact voxel-membership claim: the caption does not specify the
complete PV extraction kernel or supply a source cube mask.

The authors subsequently state that the partial-disk model reproduces
the SW extensions (§3.5, line290), and that the preferred spiral model
reproduces the low-velocity/high-altitude extensions substantially better
(§3.6, lines311–312), with its line-of-sight warp crucial to the
improvement. These statements identify a known morphology; they do not
guarantee that either the exact published model or our reconstruction
has zero residual in this box. A newly measured amplitude mismatch there
is still a mismatch in a known structure region, not by itself discovery
of previously unnoticed HI.

## Guarded positive-u spots: proximity is not secure identification

The source §2.2.1, line127, places feature1 at paper major+25 to+100
arcsec and minor approximately−75arcsec. Table2, lines174–179, gives
its center(+72,−80)arcsec, V0=380km/s, FWZI56km/s. In the analysis
frame this is a spatial region x approximately−100 to−25arcsec,
z approximately+75arcsec, with center(−72,+80)arcsec and u0=−24.8km/s.
The FWZI is a descriptive width, not a recovered exact spectral mask;
using V0±FWZI/2 as a symmetric proxy gives V=352–408km/s, or
u=−52.8 to+3.2km/s.

| Supplied guarded center | Spatial relation to feature1 | Spectral relation |
|---|---|---|
| (x,z,u)=(−60,+100,+61.8) | A40arcsec box spans x−80..−40,z80..120: adjacent to the source feature's radial range and roughly25arcsec above its quoted minor location | Center V=466.6km/s,86.6km/s from feature1's center. With24.72km/s full width its V range454.24–478.96km/s lies well beyond the symmetric FWZI proxy. |
| (x,z,u)=(−20,+100,+30.9) | A40arcsec box spans x−40..0,z80..120 and overlaps only the end of the quoted radial interval | Center V=435.7km/s,55.7km/s from feature1's center. Its V range is423.34–448.06km/s for24.72km/s width, or417.16–454.24km/s for37.08km/s width. Neither proxy overlaps352–408km/s. |

The second spectral width was not specified with the supplied candidate;
both declared search widths are therefore shown. The source's rounded
positions and FWZI do not define strict support boundaries, and the
features blend into the disk. Spatial beam wings can connect neighboring
sky regions, particularly with the source LR beam36×33arcsec, but
spatial convolution alone cannot account for the substantial velocity
displacements. The source does not justify declaring either guarded
spot to be feature1 merely because it lies near its sky projection.

Features2/3 have V0=444km/s, which is closer to these positive-u spots,
but their analysis centers are(+112,+92) and(+120,−76)arcsec. Their
major-axis separations from the supplied spots are132–180arcsec. The
source provides no footprint demonstrating that they extend across
those distances. Similarly, the §3.4 weaker positive-u extension family
is on the **positive-x** side, not at these negative-x centers. Neither
proximity argument establishes known-feature membership; neither lack
of a catalog match establishes novelty.

## Consequence for masking and claims

The present three-Table2-feature exclusion should be called that exact
thing. The top candidate can be outside it and still overlap the
separately published warp/spiral/lag extensions. A broader source-based
extension sensitivity exclusion may cover the quoted ranges, with
explicit spatial/bin/beam and channel guards. Filling the major interval
between sampled cuts would be an analyst conservative footprint, not a
recovered author mask. Its point-inverted partner can be included to
preserve the analysis symmetry, with the same qualification.

Because the top residual has already been inspected, any such added
source-based mask is a **post-selection known-structure check**; it
cannot create a fresh blind significance test. Preserve the original
result and report the new classification rather than silently replacing
the original mask. The guarded spots remain source-unclassified until
their actual spectral/spatial coherence and controls are established.
Older-data recurrence would address observational reproducibility with
the campaign's stated reuse; it would not by itself establish a new
physical effect or remove ordinary-model nonidentifiability.

## Retained figure provenance

Figures6,7,9 were extracted byte-for-byte from the already retained
arXiv v1 source archive, SHA256
`5ac7d289936d4ec75041a23093b009a79901f9e1423c8351c9f0321c05525181`.
They are saved here as `extension_figure6.ps`, `extension_figure7.ps`,
`extension_figure9.ps`. Ghostscript10.02.1 rendered the local PS files
with `-dSAFER -dBATCH -dNOPAUSE -dEPSCrop -sDEVICE=png16m -r160`.
All three PNGs were visually inspected. This creates only source-image
derivatives; it is not a new physical computation or observed-data fit.

| Artifact | SHA256 |
|---|---|
| `extension_figure6.ps` | `cfb7191fc8c06287e4bc2a1dac6eb176cc4de037663bb4d316975eff73cccfab` |
| `extension_figure7.ps` | `e62c7c79f3b9eb113953e4a300ec132fff6aeef1c1ff9d00f2028a3ea8c1ed24` |
| `extension_figure9.ps` | `85b84e6b1d98c0209d313d146128f2f1e2315a8e88a1cb62709db84152b015f8` |
| `extension_figure6.png` | `e10095ee6a9a7a6746ece974294957b68561976107aba67dd7552200226eb007` |
| `extension_figure7.png` | `1f9d281faee71fa4707dda692c41fff3a403f7a7660c2946fc2c01e5ebbf6db9` |
| `extension_figure9.png` | `d3290e72f8a4b97758db2ef4fbf4aa8a430caeee2a6c4af5fa9c94678becf0e3` |
