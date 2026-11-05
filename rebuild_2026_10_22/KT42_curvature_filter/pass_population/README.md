# Every historical primary-pass cell retains the outward-force defect

**All52 original KT39 primary-pass baryon cells have outward vertical acceleration at R=12 kpc,z=.3 kpc at each of the three tested filter widths.** This includes a=.0001 kpc, the small width identified as Solar-passing in the companion calculation. Every one of the156 signed-force evaluations is negative, with the same sign in all468 finite differences of the potential.

The historical selection is frozen at32 canonical and20 alternate cells from the KT39 production scan; it was independently reconstructed from the stored primary flags and matched to the published pass-index lists before this run. At the requested refinement3,31 canonical and19 alternate cells retain all four original primary cuts at each width. **Zero** retain the primary cuts and a restoring force at the tested point.

| Footing | a [kpc] | Outward / selected | Current primary passes | Range of partial_z Phi [(km/s)^2/kpc] |
|---|---:|---:|---:|---:|
| canonical | 0 | 32/32 | 31 | -1050.794019 to -547.720261 |
| canonical | 0.0001 | 32/32 | 31 | -1050.792328 to -547.718630 |
| canonical | 0.001 | 32/32 | 31 | -1050.627146 to -547.559329 |
| alt | 0 | 20/20 | 19 | -1136.734904 to -774.205619 |
| alt | 0.0001 | 20/20 | 19 | -1136.733359 to -774.204004 |
| alt | 0.001 | 20/20 | 19 | -1136.584376 to -774.043051 |

The largest change from the unfiltered force over this entire selected population is only **0.001824 (km/s)^2/kpc** at a=.0001 kpc, and **0.180580** at a=.001 kpc. The least outward canonical cell is index1366; the least outward alternate cell is1259 at all three widths. Thus the earlier two-witness result is not caused by choosing unusually bad primary-pass witnesses.

The acceleration is −grad Phi, so negative partial_z Phi above the midplane means acceleration away from the plane. Together with the fixed decreasing gas profiles, it gives the same local positive-compressibility hydrostatic obstruction identified in KT40. The primary observational cuts alone do not test that local sign.

## What was computed

The code imports the existing KT42 `mw/filtered_model.py` read-only, using p=9/8,ell=3kpc, widths0,.0001,.001kpc, refinement3,32 backward-Euler heat steps, rmin=.005kpc and the unchanged outer domain. It evaluates the complete finite action with Hbar=H_h T_h psi and the weighted transpose of that composite, then recomputes the original primary cuts from the observables. The baryon density of each selected cell is solved literally; no surrogate or interpolation between baryon models is used.

All six combinations of the two previously computed witnesses and three widths replay their primary scores exactly and reproduce their force to at most1.4e-16 relative. The selection/row-count audit finds156 expected unique combinations,156 recorded and no duplicates. `VERIFICATION.json` records this independent bookkeeping review; it is not an independent physics solver.

`run_001/manifest.json` validates with run status `completed`; runtime was **173.26 seconds**. The predeclared wall/CPU/log caps were1200s/1100s/1MiB, with one numerical-library thread. All pinned inputs were unchanged. No memory or CPU-affinity cap is claimed.

## Scope and prior work

`KNOWN_SOURCES.md` and `novelty_search.json` document the gap: KT40 force/hydro scripts explicitly evaluate only canonical1368 and alternate1287. This new calculation tests all52 historical primary-pass cells at the declared small widths. The general nonlocal-action novelty audit remains in KT41/nonlocal.

**This is not a full1375-cell scan of the new filtered action, not an all-baryon or continuous-width theorem, and not an independently converged continuum calculation for all52 cells.** Individual primary passes shift slightly from refinement2 to3: canonical index1344 and alternate index1290 each lose one primary cut. The force defect is nevertheless present in every selected cell, including all50 that still pass. Companion witness refinements support those witnesses; they must not be relabeled as population-wide convergence.

Outcome: the finite selected-population assertion is verified at the declared numerical resolution. The local-force failure persists throughout the already-found original primary-pass population at the sampled small filter widths.

## Reproduction

Use `contract.json`, all listed `execution_artifacts`, a fresh output directory and the installed bounded runner. The executed program is `python3 -B rebuild_2026_10_22/KT42_curvature_filter/pass_population/calculate.py --output FRESH/results.json`; the complete argv is retained in the manifest. Validate with:

    python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py rebuild_2026_10_22/KT42_curvature_filter/pass_population/run_001/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
