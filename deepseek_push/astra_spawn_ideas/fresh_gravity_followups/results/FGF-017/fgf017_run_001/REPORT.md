# FGF-017 result

Conditional closure is available inside both matched-profile supports. This is a relative eRASS-to-X-COP conversion with an inherited uniform-density-shape assumption, not an observed distance correction or a solution of either cluster.

The unique root is eta* F(C[eta* X+S];a)=C H, and ell_crit=[Me d^(5/2)/(eta* X)]². Q and R have global positive roots; registered M has a unique root throughout both supports by the independent coarse bounds in SUPPORT_ADDENDUM.md.

| Object | Valid d support | Earliest favorable d at ell=1, vacuum | Separate H comparison | Largest favorable ell at d=1 |
|---|---:|---:|---:|---:|
| A644 | [0.022546555, 1.460105202] | 1.1027919144 | 1.0987713667 | 0.6057063460 |
| ZW1215 | [0.023961661, 1.639712760] | 1.3656536194 | 1.3577908394 | 0.3455667269 |

Earliest roots use the alternative normalization and registered M. R remains a distinct branch despite being numerically close here. The full branch-specific favorable thresholds are:

| Object | Footing | History | Q | R | M |
|---|---|---|---:|---:|---:|
| A644 | canonical | vacuum | 1.1489818094 | 1.1244711664 | 1.1244711655 |
| A644 | canonical | H | 1.1447473705 | 1.1205402998 | 1.1205402988 |
| A644 | alternative | vacuum | 1.1260372284 | 1.1027919153 | 1.1027919144 |
| A644 | alternative | H | 1.1218148335 | 1.0987713676 | 1.0987713667 |
| ZW1215 | canonical | vacuum | 1.4511382246 | 1.4043964444 | 1.4043964429 |
| ZW1215 | canonical | H | 1.4427769113 | 1.3966371295 | 1.3966371279 |
| ZW1215 | alternative | vacuum | 1.4093193472 | 1.3656536211 | 1.3656536194 |
| ZW1215 | alternative | H | 1.4008801556 | 1.3577908411 | 1.3577908394 |

For ell>=1, an independently established upper relative-distance bound strictly below 1.0987713667 (A644) or 1.3577908394 (ZW1215), within the stated support, would preserve the earlier p<1 exclusion across all registered branches and the entire favorable box. With vacuum history alone those bounds become 1.1027919144 and 1.3656536194. Equality admits p=1 at the favorable corner. These are conditional sharp thresholds under the adopted interpolation, not distance priors.

At d=1, independently bounded emissivity ratios above 0.6057063460 and 0.3455667269 respectively preserve the all-branch exclusion. Allowing the entire distance support instead raises the sufficient uniform lower emissivity bounds to 6.9734690916 and 2.1611232397 (rounded upward from the computed envelope). The more useful condition is pointwise ell_lower(d)>max_branch ell_crit,favorable(d). No such external bound is inferred from redshift agreement.

The 48 curves contain 34,913 recorded evaluations, including root-solver intermediate values, and 34,608 actual-knot intervals. Analytic slope bounds evaluated in binary64 enclose each interval. The full-support favorable upper bounds coincide with endpoint values; they are not merely sampled maxima. All favorable crossings are unique within their certified monotone cells; there are no unresolved favorable cells. Two ZW1215 central cells, canonical/H/R and canonical/H/M at d=[1.4935830211,1.4968370919], have conservative enclosures straddling ell=1 without an endpoint sign change. No exhaustive central crossing count is claimed there. This ambiguity does not affect the favorable envelope or the earliest favorable thresholds.

All 15 primary controls passed. Maximum nominal relative discrepancy: 5.2847e-14; maximum forward root residual: 4.3854e-14. The main run took 4.00 s. A separate sub-second support control bounded the registered M domain without additional root calculations. Both manifests validate and enforce 120 s wall, 100 s CPU, 1 MiB combined logs and one cooperative numerical-library thread. No memory or CPU-affinity bound is claimed. No failed execution occurred.

Local FITS headers authenticate R500 in kpc and MGAS500 in 10**11 solar masses and the inspected profile units. They do not authenticate the paired angular aperture or a common cosmology. Measured centroid offsets remain approximately 0.3173 and 0.2044 arcmin, and ZW1215 has eRASS z=0.0773 versus X-COP z=0.0766. The raw headers and exact matched rows are preserved in metadata.json. Uniform-density-shape, error-column conventions and the rectangular mass box remain assumptions; the box is not a confidence region.

This result does not rescale both catalogues physically, vary vacuum density with distance, establish instrument independence, replace local density by integrated mass without a shape premise, supply pressure calibration, or validate Q/R/M as a gravity theory. Constant vacuum a=kappa*c*sqrt(G*rho_Lambda) and the separate H history remain separate.

Next discriminating task: authenticate the original eRASS R500 angular aperture and DA convention together with the X-COP distance and centering convention, then test their permitted relative-distance interval against the displayed thresholds. Without that metadata and an independent emissivity bound, the conditional discrepancy cannot be promoted to a cluster exclusion.

Provenance follow-up: immediate post-run manifest validations passed. During finalization the shared source_snapshot.json changed. The final main --root validation therefore correctly fails freshness for that metadata file only; its manifest remains untouched. All scientific code/data inputs and declared outputs still match their pinned hashes, and all applicable current snapshot entries match. The support-run --root validation and main structural validation pass. validation.json preserves the distinction. The first packaging attempt stopped at this freshness assertion and produced no result.json; it was an administrative check, not a failed numerical experiment.

Recovered metadata supplement: handoffs/source_snapshot_before_FGF021.json was independently hashed and exactly matches the executed snapshot SHA256 b1f5f9b3881f91e4c8ac680379940ba468df32da99e0be5ee1823adaaf2575d2. PROVENANCE_RECONCILIATION.json records the explicit historical-path mapping. The original manifest and live snapshot remain unchanged, so the live-path freshness failure is still accurately preserved.
