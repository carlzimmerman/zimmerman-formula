# FSP-N reproduction

From repository root:

```sh
python3 fine_structure_puzzle/normalization_gate/check.py --output /tmp/fsp_normalization_results.json
python3 fine_structure_puzzle/normalization_gate/kernel_regression.py --output /tmp/fsp_kernel_results.json
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py fine_structure_puzzle/normalization_gate/run_001/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

The saved run uses Python 3.9.6 and SymPy 1.14.0. It passed; its v2 manifest has observed input hashes before and after execution, command, resource limits, output hashes and dirty Git state. Exact symbolic algebra and 72 charged-source fixtures check the two-dimensional formula; the proof in CLAIM.md supplies the finite-rank argument. The code's symbolic assumptions are a>0, b>0, c>0, m^2>0. Positive definiteness additionally requires ac>b^2, as stated in the claim; rational identities are checked algebraically away from their denominator zeros. The proof and exact benchmarks cover the relevant positive-definite domain. No empirical alpha value is used.

The code checks a symbolic shear as a concrete basis-covariance identity, not all GL(r,R) transformations by enumeration. N1's algebra covers general invertible transformations. The counterfamily's fixed trace and determinant in two dimensions fix both eigenvalues. Rotating K while holding charges and Higgs fixed changes the theory; transforming all of them together leaves the observable unchanged.

`kernel_run_001/manifest.json` records two additional exact 3x3 examples with a rank-two massless kernel. This was added after independent review found an overbroad introductory sentence: K^-1 is the residue only when all fields are massless. The corrected general formula uses the projected inverse. The original successful 2x2 computation remains unchanged; its input hash is still current.
