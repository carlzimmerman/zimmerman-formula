# Spectral bounds preprint, version 1.0

Carl P. Zimmerman, Briar Creek Tech. September 22, 2026.

**From Scalar Certificates to Spectral Bounds: Radial Pulsations, Discrete
Hardy Forms, and SU(N) Lattice Gauge Theory**

DOI: https://doi.org/10.5281/zenodo.22895866

The paper distinguishes analytic/operator proofs, applications of external
theorems, Lean-certified scalar statements, and finite computation evidence.
It does not claim a stellar mass cutoff, physical selection of kappa=1/2,
an explicit numerical many-plaquette coupling threshold, or a continuum
Yang-Mills mass-gap solution.

## Files and licenses

- `real_research/papers/SPECTRAL_BOUNDS_2026.tex`: manuscript source.
- `output/pdf/SPECTRAL_BOUNDS_2026.pdf`: final typeset preprint.
- `output/pdf/SPECTRAL_BOUNDS_2026_supplement.zip`: code and evidence archive.
- `real_research/reviews/spectral_spine_closure_2026_09_22/`: derivations,
  source records, computation contracts, recorded results, and compiler logs.
- `fable_independent_2026/lean_2026/I{13,14,15}_*.lean`: formal scalar results.

The manuscript source and PDF are licensed under Creative Commons
Attribution 4.0 International (https://creativecommons.org/licenses/by/4.0/).
Supplementary repository code and proof materials retain the repository's
GNU Affero General Public License, version 3 or later; see `LICENSE`.
The Zenodo record-level CC BY license describes the manuscript and does
not override these file-specific software terms.

## Reproduce the calculations

Extract the supplement and run from its root, or use the same relative
paths in the Git repository. The computations use Python 3.9.6, NumPy
1.26.2, SciPy 1.11.4, and SymPy 1.14.0. Dependencies may be installed in a
separate virtual environment; no authentication or private input is needed.

```bash
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install numpy==1.26.2 scipy==1.11.4 sympy==1.14.0
mkdir -p reproduced
python3 real_research/reviews/spectral_spine_closure_2026_09_22/i13/radial_bridge.py --output reproduced/i13.json
python3 real_research/reviews/spectral_spine_closure_2026_09_22/i13/symbolic_identities.py reproduced/i13-symbolic.json
python3 real_research/reviews/spectral_spine_closure_2026_09_22/i14/verify.py reproduced/i14.json
python3 real_research/reviews/spectral_spine_closure_2026_09_22/i15/verify.py --output reproduced/i15.json
```

The original results are preserved under the evidence directory. Floating
point values can vary slightly with platform and numerical libraries;
the scripts check declared tolerances. Numerical truncations do not establish
the universal theorems. Original manifests record the working tree and paths
at execution time; `SHA256SUMS` in the archive identifies the actual included
bytes. Historical local paths are provenance, not reproduction prerequisites.

## Check Lean

Install Lean through elan, then use the included pinned toolchain and Lake
manifest. Dependency downloads require network access on first use.

```bash
cd fable_independent_2026/lean_2026
lake exe cache get
lake env lean I13_bhstar_pulsation.lean
lake env lean I14_phantom_vacuum_wall.lean
lake env lean I15_suN_lattice_gap.lean
```

The toolchain is Lean 4.34.0-rc2; Mathlib is pinned by `lake-manifest.json`.
The three files contain 60 theorem declarations in total (23 added in this
revision). Printed dependencies contain only `propext`, `Classical.choice`,
and `Quot.sound`. These checks do not formalize the external operator
theorems or every analytic derivation in the paper.

## Build the paper

From the repository root, with Tectonic installed:

```bash
mkdir -p output/pdf
tectonic --outdir output/pdf real_research/papers/SPECTRAL_BOUNDS_2026.tex
```

The archive contains the source material used in the action comparison and
the cited local reports. Primary external papers are identified by exact
arXiv versions in the manuscript and source records; they are not bundled.
