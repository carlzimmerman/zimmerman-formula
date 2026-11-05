# Accepted evidence and preserved failures

Final recorded state: **17 valid bounded-run manifests**,14 completed and3
failed. The installed computation-audit validator was run with the project
root so current input and output hashes were checked, not merely JSON shape.
`finish_001` validates the preceding16 records; its own manifest was then
validated separately. Zero exit/provenance validity is not a theorem proof.

| Evidence | Main check |
|---|---|
| mw/checks_003 | full finite energy derivative, weighted heat adjoint, zero-width reproduction, analytic Gaussian benchmark, response reciprocity |
| mw/scan_001, heat_refine_001, refine_001, domain_001 |48 fixed-witness evaluations with separated heat-step, spatial and domain comparisons |
| pass_population/run_001 |52 historical primary-pass cells at3 widths;156 outward-force witnesses,468 potential-difference signs,6 known-answer replays |
| dwarf/run_001 |36 physical rows,3 quadrature/domain settings, filtered-Plummer identity, fixed-filter energy derivative, zero-width benchmarks |
| solar/run_002, verify_001 |40 width/footing cases; full-adjoint energy, Cartesian Green contraction, finite-source exterior checks, adaptive crossing comparison |
| endpoint/run_002 |24 symbolic/finite checks, including controls detecting wrong signs/omitted terms |
| planets/run_001, controls_001 |16 full-A+B planet rows, exact eccentric-orbit averages, two independent B integrals, actual-model Newtonian null and omitted-return control |
| verification_001 |13 preceding manifests; independent grading of48 MW rows,7152 profilepoints,156 population rows,18 main Solar ratios,36 dwarf rows |
| finish_001 |16 preceding manifests; independent grading of16 supplementary planet rows and supplementary controls |

Failed records remain valid records of failure, with immutable inputs:

- mw/checks_002: m16 heat approximation missed the declared Gaussian accuracy
  gate. New m32/64/128 checks meet the same gate; the physical law and cuts
  were unchanged. checks_001 was a rejected launcher request before execution
  and has a retained contract but no manifest.
- endpoint/run_001: symbolic simplification did not cancel equivalent
  radical/power factors. A separately pinned v2 uses exact cancellation
  before the same identity test.
- solar/run_001: NumPy boolean JSON serialization failed after calculation.
  A separately pinned v2 serializes correctly; independent controls follow.

The numerical gates are prospective and unchanged. Root independently
recomputed saved grades using the original comparison data. Independent
reviewers reconstructed the energy variation, orbital/Green factors,
filtered-Plummer homology and the counterterm implications. They did not
claim blind review or independently rerun every solver.

Important interpretation boundaries remain in README and the audit reports:
finite samples versus all widths,52 historical passes versus1375 new-action
cells, uniform external field versus full Galactic curvature, supplementary
monopole ephemeris screens versus a refitted likelihood, and bounded growth
versus stability. No error estimate is advertised as an interval certificate.

The standard scientific figure was generated from accepted saved data by
`plot_results.py`, rendered to PNG/PDF and visually inspected. It shows finite
samples with connecting lines explicitly identified as guides. Root prose and
equations were self-reviewed for signs, units and consistency with the data.
