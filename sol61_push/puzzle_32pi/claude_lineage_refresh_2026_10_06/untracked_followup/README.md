# Followup: untracked products and dirty log comparison

This separate record closes the explicitly requested untracked-source inventory within the same two authorized directories. It preserves the original lineage snapshot unchanged.

At pinned HEAD `f2c6144f842b9d56b61781d7399e598a1328a726`, `git ls-files --others --exclude-standard -- sonnet55_push/puzzle_32pi campaign_fresh_gravity` returns245 files, all under campaign_fresh_gravity. No untracked candidate scientific source/report/criteria file was found: counts for .py,.md,.lean,.json,.toml,.yaml/.yml,.tex,.c/.cpp/.h,.jl,.r and .ipynb are zero. Ignored files are excluded by this exact command; this is not an inventory of every hidden/ignored product or every Claude workspace.

| Group | Count | Inspected evidence and classification |
|---|---:|---|
| CFG158_infall_referee/cfg158_sims |236|59 each of .final.bin,.rgrid.bin,.samples.bin,.times.bin; numeric binary byte samples; total74,864,264 bytes. Generated simulation products, not new source code.|
| CFG122_door4_superfluid |3|NumPy .npz archives, including two MUTATE variants; each central directory contains1226 .npy members, with named numerical arrays such as bestS, reactS and cs_ratio_min.|
| CFG193_g7_speed_referee |5|NumPy .npz curve archives, including three MUTATE variants and U2; each contains six .npy members named names,C,N,fD,D,eD.|
| cfg109_posthoc.out |1|156-byte failed-launch message: Python could not open cfg109_posthoc.py. No successful result or source file is supplied by this log.|

Archive central directories were read without loading arrays or executing code. INVENTORY.json records every current untracked path, size and128-byte header hash; it records archive member counts/suffix counts/catalog hashes and bounded samples. Header hashes are explicitly not whole-binary hashes. This inspection neither validates the numbers in those products nor identifies their generation time, author or authenticated scientific antecedents. It provides no claim that the old campaign topics lacked source work; it only finds no NEW source/report file in this currently untracked set.

## Three tracked dirty CFG4 outputs

Each current log was read in full and compared byte-for-byte with its pinned committed version. All three are exact committed prefixes:

| Log | Current / committed lines | Added lines | Removed lines |
|---|---:|---:|---:|
| CFG4_clusters.out |56 /101|0|45|
| CFG4_galaxy_law.out |47 /141|0|94|
| CFG4_galaxy_law_MUTATE.out |49 /143|0|94|

Their last tracked file commit is3409d12da0325a661168298e4049dcf2502e6d22. The current cluster prefix stops before its law/results section; the galaxy prefixes stop after the SPARC setup count. The normal and MUTATE headers remain distinguishable. There is no newly added measurement, conclusion or full final result to audit in these dirty bytes. They are unverified partial output evidence, not scientific source changes. Why those files are truncated, whether a process is active, and when they were generated are not inferred.

The inherited headers explicitly call kappa=1/2 FITTED; they do not contain a newly derived32pi or cutoff normalization. Existing committed conclusions were not rerun or newly accepted from their labels. No author files were modified, no source simulation or astronomical fetch was executed, and no commit was made.

## Result and reproduction

No newer source antecedent impacting the retained p57/CFG355 kernel/growth claims was discovered by this exact followup inventory. The observed additions are simulation/cache/log products, with a missing-file launch error and truncated legacy logs. That conclusion is limited to the nonignored untracked set and three named tracked dirty outputs; it is not a statement about all Claude activity or the scientific validity of their generating programs.

Reproduce from the repository root with `/usr/bin/python3 sol61_push/puzzle_32pi/claude_lineage_refresh_2026_10_06/untracked_followup/inventory.py`. It performs read-only scoped Git/metadata/archive-directory operations and writes only its owned INVENTORY.json. The original SOURCE_UPDATE.json remains hash `ae0dc1aa8798620f2b3fd674e5ef21741a7f393c0c56d8639d448f4177e2a74b`. Current followup inventory hash `cb36a76d3a3a8f30069705761ba08a554c763c468b17212ec867eb8f73daac91`; script hash `3680fbf28c2abd4dfc4c2036fd86c7e190484f78e4e3207a1f82c86d5c3b0734`. Head at the end was `f2c6144f842b9d56b61781d7399e598a1328a726`.
