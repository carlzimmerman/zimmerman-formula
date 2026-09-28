# FGF-017 scoped acceptance: conditional distance/emissivity thresholds

Result SHA256 `4cea2c2c5d9cbbde81cacd2092265404daabd1459d1810bc6f614c49fcec35ac`.
Coordinator read the raw derivation, compute.py, support addendum and report.
Required fields and every scientific input/output hash match. The one live
metadata exception and exact historical replacement are stated below.

Independently, at fixed r=d Re and eta=m/X, h(eta)=eta F(C[eta X+S];a)/(C H)
has derivative (F+eta C X F_B)/(C H)>0. This gives the unique positive root
for Q/R; M additionally requires its registered positive domain. Substitution
gives ell_crit=[Me d^(5/2)/(eta* X)]² and the indicated ordering in ell.
Coordinator also checked the logarithmic derivative and slope enclosures.
Those arguments are conditional on the declared interpolation and uniform
density-shape relation, not measurements of local density.

A separate bounded run in
`campaign_fresh_gravity_astra/stage_06/distance_audit/run_001/` parsed the
original six FITS profiles and reproduced 64 Q/R nominal/crossing checks.
It used positive roots of Q's quartic and direct eta-bisection for R, sharing
neither the author's force implementation nor its log-root solver. Maximum
relative difference was 1.71e-13. eRASS matched masses were taken from the
returned metadata, whose matching was previously audited in FGF-012.
This is not an independent M implementation or a full-envelope recomputation.

Accept the finite outputs with their binary64 scope: 48 branch/corner curves,
unique positive roots, and reported slope-enclosed favorable thresholds.
Constant-vacuum earliest favorable ell=1 distances are 1.1027919144 (A644)
and 1.3656536194 (ZW1215). The separate H comparison gives 1.0987713667 and
1.3577908394. These earliest cases use alternative normalization and M;
R is independently distinct and numerically close. Both central unresolved
ZW1215 cells remain recorded. The support-wide enclosures use analytic slope
bounds evaluated without directed rounding; they are not machine interval
certificates or statistical confidence bounds.

No distance change has been measured here. The result demonstrates why valid
interpolation support alone cannot supply an observational exclusion: closing
values exist inside that support. Authentic angular apertures, common distance
and centering conventions, emissivity bounds, pressure calibration and the
shape premise remain required. The rectangular error box has no asserted
joint coverage or independence. Filtered-MONO field/metric closure is absent.

## Explicit provenance reconciliation

After the original successful run, the coordinator appended FGF-021 sources
to live source_snapshot.json. The original main manifest is preserved and
correctly fails a later live-path freshness check for that metadata file.
All actual code/data inputs and outputs still match. The exact executed
snapshot was reconstructed, hashed, and saved at
`handoffs/source_snapshot_before_FGF021.json`, with SHA256
`b1f5f9b3881f91e4c8ac680379940ba468df32da99e0be5ee1823adaaf2575d2`.
The worker's PROVENANCE_RECONCILIATION.json pins that explicit mapping; no
manifest was rewritten and no science was rerun to hide the metadata change.
Support-run and independent-root-check manifests validate against current
inputs. Future dispatches must freeze live coordinator metadata before hashing
it as an execution input, or omit it when it is not a scientific dependency.
