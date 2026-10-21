# Bounded later-catalog check for the near-central SE patch

Checkpoint `ngc5023-full-warp-2026-10-20`, base
`c821a8bccc8a20e107b4c6771d31e02d05aa8b10`; checked20 October 2026.
Classification: **unclear; no matching later isolated-cloud catalog entry
identified in the bounded search**. This is not an absence theorem or a
novelty claim. No new cube fit or flux measurement was performed.

The parent-supplied target is(x,z,u)=(−20,+100,+24.72), with angular
full widths40×40arcsec and velocity full width24.72km/s. It is near
J2000RA13:12:19.1, Dec+44:01:12.7, V_hel429.52km/s. Its box has
x−40..0arcsec,z80..120arcsec,u12.36..37.08km/s. These identify the
query region, rather than a source-derived cloud centroid or mask.

The relevant later catalog is Kamphuis et al.2022,
*HALOGAS: Strong constraints on the neutral gas reservoir and accretion
rate in nearby spiral galaxies*, [A&A668,A182](https://doi.org/10.1051/0004-6361/202140704),
[arXiv2210.09383v1](https://arxiv.org/html/2210.09383v1).
Its §5.1 reports no cloud candidates in NGC5023. AppendixA's source
catalog lists only the target-galaxy row at RA13:12:11.73,
Dec+44:02:18.91, V405.9km/s. The selection requires separated sources:
companions exceed one beam from the target in every channel; clouds use
that separation without an optical counterpart (§3). Connected gas is
counted with the disk (§5.2). The NGC5023 integrated detection limit is
27.5mJy km/s (Table6 in v1; Table7 in the published paper), with a
21.3×14.7arcsec search beam (Table2). These are observational catalog
facts; no accretion-rate or halo assumptions enter this check.

Inference: that catalog cannot establish whether this near-disk patch
was absorbed into the target mask, undetected, or a separate previously
unclassified structure. The supplied HR/LR baseline-subtracted aperture
fluxes17.80/11.39mJy km/s are below27.5mJy km/s, but their apertures,
baseline treatment and extended morphology differ from that selection.
The catalog limit is not a quantitative completeness bound on this
residual. The later catalog uses HALOGAS observations, so its source
classification is not independent confirmation of a HALOGAS residual.

The other directly relevant later HALOGAS study, Marasco et al.2019,
[A&A631,A50](https://doi.org/10.1051/0004-6361/201936338),
[arXiv1909.04048v1 §2.1](https://arxiv.org/html/1909.04048v1), studies
15 intermediate-inclination systems,50°<i<72°. Its Table1 excludes
NGC5023; it supplies no separate cloud identification for this patch.

The2013 source comparison remains as recorded in `KNOWN_EXTENSIONS.md`:
the sky box touches the radial end of feature1's reported projected
extent, but its positive velocity differs from that feature's380km/s
center. For this updated box, the symmetric descriptive FWZI proxy
ends at408km/s, while the box starts at417.16km/s. Neither that proxy
nor the later catalog supplies an exact voxel mask establishing
membership. No later primary source found in the recorded search
identifies the patch at the supplied sky position and velocity.

The supplied older-WHISP uncertainty is too large to provide meaningful
confirmation or refutation at the reported HALOGAS amplitude. This
source-only check does not change that parent result. The defensible
label remains an **unclassified, conditional HALOGAS residual requiring
independent observational confirmation**, with novelty unresolved.

Search scope and input values are retained in `LATER_CLOUD_CHECK.json`.
Primary text evidence is version-pinned to arXivv1 URLs and stored as
web-extraction response capsules in `LATER_CLOUD_CHECK.web_evidence.json`
and `LATER_CLOUD_CHECK.selection_evidence.json`. Their hashes identify
the retained extraction artifacts, **not raw paper/HTML bytes**. Direct
local retrieval failed DNS resolution; publisher HTML returned403
through the web tool, while arXiv's primary HTML was readable. No author
contact, new observational download, source mask or exhaustive citation
index search was attempted.
