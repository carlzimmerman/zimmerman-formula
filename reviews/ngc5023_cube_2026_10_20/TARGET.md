# NGC5023 raw HI symmetry test

Checkpoint `ngc5023-cube-2026-10-20`, assessment base
`be8fc76cb0e207b88710f130abf2aa937f0895a5`.
Parent `reviews/ugc08286_profile_2026_10_20/CHECKPOINT.json`.

User authorizes actual-cube analysis without LambdaCDM or the project's
acceleration law, centering/beam/mask/warp controls, and independent-data
replication where available. This is an exploratory object-specific search,
not a blind preregistration, theory closure or a guaranteed new discovery.

Primary observable: point-inversion residual of the HI emission cube,
`D(x,z,u)=I(x,z,u)-I(-x,-z,-u)`, with `u=v-v_sys`. For a centrally symmetric
source with antisymmetric line-of-sight velocity and symmetric instrument
response it vanishes. Spatial sky angles and observed velocities suffice;
no distance, halo, acceleration law or stellar M/L enters this observable.
Moment diagnostics and vertical/radial bins are summaries, not additional
independent detections. A symmetric extra mass is inside this null.

Before interpreting a residual, check data identity and WCS/velocity
convention; compare independent positional/systemic centering and allowed
perturbations; propagate actual beam and channel resolution, finite/paired
support, negative emission and blank-region correlations. Use common mirrored
masks, include fixed apertures and more than one emission threshold. Spatial
pixels and adjacent channels must not be counted as independent measurements.
HR/LR HALOGAS products share observations and provide only resolution and
processing controls. A centrally symmetric warp is inside the null; asymmetric
warp/spiral/emissivity and tracer motion remain ordinary explanations.

Freeze any candidate statistic/region before looking at independent data.
Seek a separate telescope/observation and verify actual data provenance,
coverage, angular/spectral response and sensitivity. Replication means the
same observable after matched responses and declared support; another image
of the same visibilities or an integrated flux is insufficient. Preserve
an unavailable/underpowered independent check explicitly rather than claiming
either confirmation or absence. Known published HI structure is not novel.

Work only inside this new packet, plus the designated live pointer after
reconciliation. Earlier packets, original datasets, campaigns, publications,
owner jobs and Git state are immutable. No process inspection or job control.
Acquire public data with explicit source URLs/byte hashes/checksums and byte
bounds. No installs. Bounded single-thread analysis runs, minutes per run,
nominal memory below 1 GB. macOS memory/affinity hard limits are unavailable
and must not be claimed enforced; use supported wall/CPU/log/thread settings.

Outcome criteria: report the measured residual and its sensitivity across
controls; distinguish a noise/processing feature, ordinary known structure,
a robust unexplained candidate and actual independent replication. A finite
anomaly is not evidence of a specific gravity law or physical memory unless
an independently derived distinguishing prediction is supplied.
