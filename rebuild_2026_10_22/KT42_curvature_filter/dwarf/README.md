# KT42: curvature-only filtering does not repair the tested Draco diagnostic

With the full action variation retained, Draco at fixed Upsilon=2 and auxiliary external-field eta=.01 has negative scalar virial for every sampled Gaussian width through **0.3 kpc**, on both unchanged acceleration footings. At 1 kpc the virial becomes positive, but its trace-averaged dispersion is only **3.0693 / 3.0729 km/s**, below the unchanged two-sigma lower comparison line **6.7 km/s**. None of the nine sampled widths clears that orientation-averaged screen.

This is a finite diagnostic of the specified response and fixed Plummer profile, not a continuous-width no-go or an assignment of Draco's actual external environment. A negative W/(3M) is the stronger result: the imposed profile cannot have stationary scalar virial balance with nonnegative kinetic energy in this imposed field. A positive trace value alone does not prove an anisotropic equilibrium or observed line-of-sight fit.

| Gaussian width a [kpc] | Draco V canonical [(km/s)^2] | Draco V alternate [(km/s)^2] |
|---:|---:|---:|
| 0 | -19.33829216 | -26.83431052 |
| 0.0001 | -19.33829386 | -26.83431270 |
| 0.001 | -19.33846216 | -26.83452856 |
| 0.003 | -19.33982161 | -26.83627184 |
| 0.01 | -19.35520631 | -26.85597029 |
| 0.03 | -19.48423908 | -27.01876751 |
| 0.1 | -20.18320079 | -27.58950102 |
| 0.3 | -3.23715815 | -3.87816867 |
| 1 | 9.42034774 | 9.44262814 |

The mechanism is not simple monotonic damping. Small filtering initially makes the negative curvature term stronger. At a=.1 kpc the canonical decomposition is V=1.08196158+6.35973843−27.62490080=−20.18320079. At a=1 kpc it is 1.08196158+8.43661526−.09822910=9.42034774: large filtering nearly removes the negative curvature stress, but the remaining response supplies too little scalar support for the unchanged comparison line.

Fornax at fixed Upsilon=3 is the declared size control. Its scalar virial stays positive; the original orientation-averaged two-sigma screen is met at a=.3 and 1 kpc on both footings. At a=0, sigma=9.4007/9.6024 km/s; at .3, 9.9309/10.1785; at 1, 12.9333/13.3959. This difference confirms that the calculation is not a construction forcing every object to fail. It does not rescue Draco or grade the full dwarf population.

## Action and numerical evidence

`DERIVATION.md` gives the full action and source. Only the Hessian argument is filtered: g remains unfiltered, Hbar=T_a Hess psi, E=g²R(x+[ell²Hbar:Hbar/a0²]^p), p=9/8, ell=3 kpc. The return term is −partial_i partial_j(T_a* Bbar)_ij. The virial pairs Bbar with T_a delta H; replacing it with the unfiltered delta H changes the declared finite-domain controls by **7.25 to 16.57 (km/s)^2** at a=.3 kpc.

The Plummer density is an exact exponential mixture of Gaussian densities, so convolution adds a² to each component variance. Differentiating the filtered potential gives the filtered Cartesian Hessian; no independent smoothing of spherical-basis components is used. Fixed-source-mass homology differentiates the source scale at fixed physical a, retaining the additional filter-scale term.

The predeclared three radial/angular/mixture/domain settings agree within **1.68e-05 (km/s)^2** for every 36-case row. Analytic unfiltered Hessian/homology controls agree to 3.4e-15 scaled error. The energy finite-difference check, formed from energy values independently of A/B, has maximum relative error **7.88e-9**. Zero-filter signed virials reproduce KT40 to below **1e-10 (km/s)^2**. These are observed numerical checks, not interval-certified continuum error bounds.

The bounded run completed in 13.15 seconds with one numerical-library thread, a 1200-second wall cap, 1100-second CPU cap and 1 MiB log cap. No memory or CPU-affinity cap is claimed. `run_001/manifest.json` records exact argv, software versions, dirty working tree, input hashes before/after and result hashes. Validation returned `valid evidence record (run status: completed)`. No earlier file was modified.

Outcome: **implementation and finite assertion verified in the stated range, conditional on numerical quadrature**. A code-independent derivation review of this new branch is still desirable; the controls do not certify relativistic or dynamical health.

## Reproduction

Use `contract.json` and every `execution_artifacts` entry as repeated `--input` arguments to the installed mathbox bounded runner. Use a fresh output directory and invoke `python3 -B rebuild_2026_10_22/KT42_curvature_filter/dwarf/calculate.py --output FRESH/results.json`. The exact executed argv is in the manifest. Validate with:

    python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py rebuild_2026_10_22/KT42_curvature_filter/dwarf/run_001/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
