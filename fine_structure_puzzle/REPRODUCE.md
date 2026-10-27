# Reproducing the launch investigation

Run from `/Users/carlzimmerman/new_physics/zimmerman-formula`. Python and numerical-library versions, bounds and exact arguments are pinned in each current manifest. No package installation or network download is required by these commands in the environment used for this investigation.

The following commands write fresh results to temporary files, preserving the recorded runs:

```sh
python3 fine_structure_puzzle/archive_audit/scope_checks.py
python3 fine_structure_puzzle/normalization_gate/check.py --output /tmp/fsp_normalization_results.json
python3 fine_structure_puzzle/normalization_gate/kernel_regression.py --output /tmp/fsp_kernel_results.json
python3 fine_structure_puzzle/uv_selection/discriminator.py --output /tmp/fsp_uv_matrix_results.json
python3 fine_structure_puzzle/uv_selection/inverse_bvp.py --output /tmp/fsp_uv_inverse_results.json
python3 fine_structure_puzzle/spectral_route/spectral_check.py --output /tmp/fsp_spectral_results.json
```

These reproduce finite assertions within the models, not a derivation of nature's alpha. In particular, the inverse calculation imports the declared phenomenological weak/strong and Yukawa boundaries; the discriminator's calibrated F example is for display only. Do not infer independent measurements or theoretical precision from floating-point agreement.

The negative controls deliberately change a spectral sign or a mixed beta-function coefficient. Their expected exit status is nonzero. Per-route contracts and commands are in `archive_audit/COMMANDS.md`, `normalization_gate/REPRODUCE.md`, `spectral_route/README.md`, `uv_selection/CONTRACT.md` and the numerical run manifests. The fresh review's independent numerical formulation is under `reviews/independent_uv/`.

To check saved provenance, apply the installed mathbox computation validator to each path in CHECKPOINT.json:

```sh
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py PATH_TO_MANIFEST --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

Validation checks file/manifest consistency; it does not prove the physical interpretation. A valid intentionally failed control remains a failed computation. Old failed or superseded runs are retained separately; their original input content may live in archived snapshots while the current script path has changed. Use only the authoritative current paths for current positive evidence.
