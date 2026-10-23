# Research results publication

Start with [RESULT.md](RESULT.md) and [PERSISTENT_STATE_AND_OVERLAP_RESULT.md](PERSISTENT_STATE_AND_OVERLAP_RESULT.md).

The repository includes source, contracts, result tables, original validation manifests, reports, plots, and smaller numerical artifacts. Raw `.bin` simulation checkpoints, compiled executables/libraries, and individual data artifacts larger than 20 MiB remain local. `LOCAL_ARTIFACT_INVENTORY.json` records their paths, sizes, and SHA-256 hashes. Nothing was deleted locally.

Original manifests describe the original full local runs; they have not been rewritten to imply that omitted inputs are present in this checkout. Rebuild executables and regenerate omitted source/checkpoint inputs using the corresponding scripts before rerunning dependent computations or validating all input hashes on a fresh clone. Compiled binary hashes may differ across toolchains.

Bath formation and surviving cold abundance remain uncomputed. Single-cell quantum propagation checks and classical high-H continuation are distinct experiments and do not establish a cold formation mechanism.
