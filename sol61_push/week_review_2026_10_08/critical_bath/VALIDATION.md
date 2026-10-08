# Verification and checkpoint CB1

October 8, 2026. Base a51caafcab1b0f62c9a744fef62cab4d1703714a. Owner: this Sol61 chat. Scope: this new folder only; no Astra work orders, physical target requirements or shared claims ledger were changed.

## Computation

81 baseline checks pass. The boundary mutation fails 40 checks; the omitted energy-Jacobian mutation fails 31. All three stderr files are empty, and all three manifests validate, including input and output hashes.

The baseline compares coordinate-space Bessel quadrature with the analytic transform for nu=.2, 1/3 and .45, including both domains. It checks the Gamma density, normalization, Euclidean correlation to t=1e6, resolvent against log-energy quadrature, the regular-domain susceptibility against its Green-kernel result, finite-source roots, mixed-boundary exponents, and the radial-potential dictionary. The rational -5/36 identity and identity-shift invariance are also checked.

For nu=1/3:

| Quantity | Value |
|---|---:|
| Analytic asymptotic A=Gamma(1/3)^(3/4) | 2.0939777466514693 |
| epsilon/D^(3/2), D=1e-8 | 2.0937527506843616 |
| Ratio to A | 0.9998925509273117 |
| Regular-domain chi=(2^(2/3)-1)/(1/3) | 1.7622031559045988 |
| Regular epsilon/D^2, D=1e-8 | 1.7621912906394839 |
| Dimensionless a_toy at eta=1 | 9.86567130781102 |

None of these numbers is a measured acceleration or a prediction of k.

The log-energy quadratures use [-90,35]; the finite lower cutoff is material to the last few digits of the nu=.2 susceptibility (error about 5.9e-8, inside its specified relative 2e-8 tolerance). This tolerance was set before execution. Gaussian coordinate quadratures stop at r=20. These bounds are numerical limitations, not limits used to prove the analytic formulas. No random sampling or claimed formal proof was used.

The positive-square form and its natural boundary condition were derived after these runs and self-reviewed analytically. They are not counted among the 81 numerical checks. The checks establish finite implementation consistency; neither they nor manifest validation are an independent proof audit.

## Reproduce

Python 3.9.6, NumPy 1.26.2 and SciPy 1.11.4. The scientific script is checks.py and its contract is contract.json. Actual commands, versions, input hashes, repository dirty state, limits, logs and output hashes are retained in runs/*/manifest.json.

Use the installed mathbox computation-audit scripts/run_experiment.py with the repository as --root, this folder's contract.json and checks.py as --contract and --input, a NEW --output directory and --result path, and --timeout 60 --max-output-bytes 100000 --max-threads 1, followed by:

    -- python3 sol61_push/week_review_2026_10_08/critical_bath/checks.py --output NEW_RESULTS_PATH --mutate none

Controls use --mutate boundary or --mutate jacobian and are expected to exit 1. Preserve the existing runs.

## Source review

The primary published inverse-square paper was read at its domain definition and homogeneous spectral diagonalization, translating its Bessel prefactor to ordinary J. The real m=-nu case used here is self-adjoint; the paper's general complex-parameter statements must not be mistaken for self-adjoint results. Lin–Yin equations (3.1)–(3.4) were checked in arXiv:1402.0055v2. Source locators and cached-byte hashes are in source_manifest.json; raw copies remain in the ignored project research cache.

The new work uses established Bessel and rank-one spectral machinery. The bounded novelty claim is only that this is a new route relative to the threshold folders reviewed in this project. No exhaustive literature novelty claim or new OpenAI theorem is asserted.

## Live research decisions

1. Constructive bath route: advanced from an assumed spectral density to an explicit operator, source, and positive energy form. The next unresolved implication is selection of s=1/6 and exclusion/control of the allowed boundary energy from the microscopic theory.
2. BFSS route: open. The primary leading free-channel reduction does not supply this Bessel index. Full operator-weighted scattering, effective interactions and domain matching remain uncomputed. It is not declared impossible.
3. Exact MONO completion: the single bounded-source mechanism cannot reproduce the unbounded logarithmic excess tail globally. That specific realization is insufficient; extending it requires an explicitly justified new ingredient.
4. Vacuum coefficient: open. A same-action gravitational vacuum normalization is needed; the subtracted response is invariant under an identity energy shift.

Next bounded discriminator: obtain an actual effective radial interaction and domain from a proposed microscopic action, and compare against Delta V=[1/9-(l+7/2)^2]/r^2 and b/a=0. A candidate failing this may still realize the threshold exponent through another channel; merely renaming a free channel does not meet this test.
