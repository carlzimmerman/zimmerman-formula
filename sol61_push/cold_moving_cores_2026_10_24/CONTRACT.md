# CCT-010 moving-core finite diagnostic

Resume the exact source-free escape-pulse CCT-009 final fields at t120; run to t130 with identical field grid, eta, angular cuts and dt. Track continuous nearest potential well, finite radius-one cold control-volume centroid, wave-current momentum and intrinsic angular momentum. A tracked aperture is not a Lagrangian material label. Compare centroid displacement/current velocity before identifying material transport. Save full potential coefficients every .5 code time for inertial stellar probes.

New stellar probes are passive, initialized around the chosen tracked cold aperture with its current velocity, and propagated in full nonspherical cold potential. Rigid stellar self-gravity/Xi follows probe COM; cold backreaction, self-consistent nonspherical Xi, host and real stellar DF are absent. Neither stellar safety nor a stable four-dwarf solution can pass from these probes alone. Shared G source counted once, no added cold force.

Controls: angular quadrature refinement for core moment integrals; analytic spherical potential gradient against finite differences and point-mass force; timestep refinement of stars; cold M/E/J inherited and recorded. Source hashes must match before/after. At most 1 GB RSS, single-threaded, no heavy shared jobs or old packets changed. New audit is exploratory; old criteria/failures retained. Fornax/Leo I unmatched pulse production remains an unresolved conjunction, not a pass.

Commands (from repo root):
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 sol61_push/cold_moving_cores_2026_10_24/evolve.py --galaxy Draco --tag draco_track --resume draco_escape_long --nr 768 --lmax 12 --mmax 4 --T 130 --dt .02 --gas none
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 sol61_push/cold_moving_cores_2026_10_24/evolve.py --galaxy Sextans --tag sextans_track --resume sextans_escape_long --nr 1024 --lmax 16 --mmax 4 --T 130 --dt .02 --gas none
