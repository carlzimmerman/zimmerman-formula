# CD26-3 accepted evidence and closeout

`python3 real_research/dark_energy_inverse_2026_09_26/verify_evidence.py`
completed successfully. It checked **31 Lean declarations in four files**,
**six accepted bounded-run manifests**, and **12 frozen source snapshots**.
The consulted live gate/clock source hashes also matched at verification.
The machine-readable result is `evidence_summary.json`.

| Route | Accepted calculation | Accepted formal statements |
|---|---|---:|
| Pressure/density reconstruction | `reconstruction/run1`: 21 exact identities, six roundtrips, six synthetic epochs | 6 |
| Scale, horizon and coupling inverse | `scales/run_005`: 34 exact identities plus rank/dimensional and numeric controls | 12 |
| Gate and polar clock inverse | `gates_clock/run1`: 45 exact identities plus 15 bounded/control checks | 4 |
| Positive lapse inverse | `spectral_inverse/run_001`: 30 exact symbolic checks including controls | 9 |
| Illustration | `reconstruction/plot_run2`: synthetic PNG/PDF, visually inspected | — |

The six accepted manifests are the four scientific runs, the illustration
run, and `spectral_inverse/run_lean_001`. The other three Lean files use
explicit compiler records and logs; they are checked separately by the same
consolidation script. Counting only bounded-run manifests would omit those
compiler records.

Every accepted Lean declaration uses only `propext`, `Classical.choice`
and `Quot.sound`. Current source hashes match the accepted compiles; no
`sorry`, `admit`, custom axiom declaration or `sorryAx` appears in those
accepted sources/axiom reports. The reconstruction file has three harmless
linter warnings; the other final compiles are clean. Toolchain: Lean
4.34.0-rc2, mathlib `85e3a25e006c35636f0e53b0e9296caca2685bc0`.

Failed and superseded runs remain visible. Reconstruction's first two Lean
attempts failed elaboration and are excluded; their exact failed sources
are archived. Its first plot was replaced for legend placement. Scale
development required a root-simplification fix, frozen source inputs after
a concurrent note changed, and correction of recorded runtime metadata.
The final scale evidence is `run_005`, not an earlier passing calculation
with stale metadata. Earlier failed scale source revisions were not
separately archived; their retained logs/records do not reconstruct those
source versions. The gate certificate's first successful compile was
superseded only for tactic-style warnings. Per-route evidence documents
record these limits.

Independent review of the reconstruction and synthesis is recorded under
`spectral_inverse/`. The scale investigator independently checked the
pressure/density units, Newton normalization and inverse domains as well.
The root reviewed the four final statement files and their stated physical
scope, inspected the plots, checked report links and checked the recipe diff
for whitespace errors. Mathematical self-review covered the new root
reports and the CD26-3 recipe insertion, not the entire historical recipe.
The synthesis review's missing denominator-domain conditions were added
to the README and recipe; the equations themselves did not change.

These certificates close the stated conditional mathematical calculations.
They do not formally derive the complete action, prove a continuum Cauchy
theorem, identify a microscopic vacuum source, establish observational truth
or settle novelty. No new observational likelihood was fitted. The gravity
theory and its common-action assembly remain **OPEN**.
