# Compiler metadata correction — no frozen records replaced

2026-10-20, scoped to `sol61_push/cold_pair_excitation_2026_10_20`.

Nine contracts and their nine run manifests declare `Ccompiler: Apple clang17.0.0`. That annotation was a metadata assumption and conflicts with the recorded toolchain: the original `build_receipt.json` and the later `build_receipt_seed.json` both report **Apple clang version 21.0.0 (clang-2100.1.1.101)**. The original preflight contract/manifest already record 21.0.0 correctly.

This correction preserves all old contracts/manifests, sources, binaries and outputs. It does not rerun a field calculation, replace hashes, alter an equation, repair a physical discrepancy or change a finite numerical result. Exact source and binary identities remain the pinned SHA-256 values. `METADATA_CORRECTION.json` lists all 18 affected files with full hashes and the build evidence.

Affected paths, relative to the packet directory:

| Case | Frozen contract | Frozen manifest |
|---|---|---|
| preflight_v2 | `preflight_v2_contract.json` | `preflight_v2_run_001/manifest.json` |
| isolated_static | `isolated_static_contract.json` | `isolated_static_run_001/manifest.json` |
| isolated_moving | `isolated_moving_contract.json` | `isolated_moving_run_001/manifest.json` |
| pair_inphase | `pair_inphase_contract.json` | `pair_inphase_run_001/manifest.json` |
| pair_antiphase | `pair_antiphase_contract.json` | `pair_antiphase_run_001/manifest.json` |
| pair_dt_half | `pair_dt_half_contract.json` | `pair_dt_half_run_001/manifest.json` |
| pair_dx_fine | `pair_dx_fine_contract.json` | `pair_dx_fine_run_001/manifest.json` |
| pair_separation | `pair_separation_contract.json` | `pair_separation_run_001/manifest.json` |
| pair_faster | `pair_faster_contract.json` | `pair_faster_run_001/manifest.json` |

The v2 build receipt records its compile argv and source/binary hashes but does **not** contain its own compiler-version observation. Consequently, the observed 21.0.0 toolchain is directly documented for the original and seed builds; a fully independent reconstruction of v2's exact historical compiler version is not supplied by its versionless receipt alone. The frozen 17.0.0 annotation must not be used as verified historical build evidence.

The seed-evolution launcher now reads the exact compiler string from the pinned seed build receipt before freezing new contracts. Previously frozen metadata remains visible together with this correction.
