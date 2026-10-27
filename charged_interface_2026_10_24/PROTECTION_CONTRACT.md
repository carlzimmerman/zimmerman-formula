# CI-2: suppress interface fragmentation with the existing mixing barrier

CI-1 stores charge in multiple outer interfaces, often loses the core. This
is a failed tested regime, not a conserved-T construction. The old beta20
is not a measured constant. Increase the existing positive mixing barrier to
beta100,1000 while keeping the same law-preserving endpoints and all forces.
Large-disk template, k1,10,100, two starts, n128:12 minima. This tests whether
energetic metastability suppresses fragmentation, not a data-calibrated fit.
Independent T potential must use the actual beta, not a hardcoded20.
Any apparent pass needs grid/regularization and nonlinear phase/charge checks.
