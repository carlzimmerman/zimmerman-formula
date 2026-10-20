# ARPACK initialization correction

The original grid_run_001 and natural_run_001 specified no deliberate random
mathematical sampling, but eigs/eigsh were allowed their default starting
vectors. Their initialization was therefore unpinned; the contracts
randomness.used=false did not capture this implementation detail. Old scripts,
contracts, mode caches and manifests are preserved unchanged. Their eigenpair
residuals and finite results remain inspectable; an exact initialized rerun
was not guaranteed.

V2 uses v0_j=cos(.731j)+.3sin(1.17j) at every ARPACK call. New manifests
record the deterministic code and fixed input hashes. New mode caches feed
a new natural-radiation run. No physical coefficient, original pass threshold
or historical result is changed. Additional convergence controls explicitly
match the localized quadrupole under mesh/box changes and check translation
and variational-energy convergence.
