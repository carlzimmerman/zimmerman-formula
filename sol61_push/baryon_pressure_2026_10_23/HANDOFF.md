# BP-20261023 continuation handoff

Base checkpoint: PR-20261023; repository revision5f6a308756f29ae9f6ec633b4b79ac378f897e98 at start, dirty shared tree. Own write scope is this directory only. No commit, push or external message. The full goal remains open.

Read RESULT.md, DERIVATION.md, AUDIT.md, SOURCES.md. The current numerical model is `hydro_v2.py` (nonradiative ideal gas plus local Compton heat), with `hydro_cooling.py` a separately labeled prescribed-H2 sensitivity. `hydro.py` is the retained failed local-energy implementation. `gas.py`/`evolve.py` are preliminary barotropic shells, stopped at gas crossing; do not resume them as shock hydrodynamics.

Accepted finite result at z=10: pressure/shock heating reduces the previous pressureless fixed-aperture cold mass from434k to358k solar masses in the512-cell equal-seed run. Doubling resolution changes this aperture mass1.04%, but raises cold peak840->1980 and changes baryonic aperture mass10.6%. Core center remains unresolved. Time halving agrees; energy error halves spatially, not temporally. Absolute energy defect is comparable to the candidate Newtonian binding energy, so binding is not certified.

Cold aperture masses with initially smooth baryons are37.6k (same cold seed) or64.4k (first-order total-matter displacement matched). Half seed radius gives56.9k. No universal mass selection. These are single deterministic spherical seeds, not a population.

Cooling fH2=1e-3, imposed below z=100, reduces central gas temperature629->562 K at z=10 with almost unchanged0.32 kpc mass. Atz9.527, with acceptable global residual~.00104, it givesTmax823 K rather than1817 K; aperture mass grows to548k in both. Nonradiativez8 work error.01086 fails. Cooling continuation stopsnear z=8.920 at its low-density fit boundary, also with failed work error.0267. Do not promote either late endpoint to a stable remnant.

Structural result: in the frozen-background quasistatic linear limit detM=-Jc q²(Jb+cs²)/(1+q²)<0. Gas pressure slows the cold-coupled unstable mode but does not introduce a hard cold-mass cutoff. This is restricted, not a nonlinear or cosmological no-go theorem.

Full dynamical linear thermal campaign timed out300s and has no usable result. Quasistatic replacement is explicitly approximate; retained growth at k1/Mpc is.95565 with or without the small gas-pressure correction. Existing growth deficit unresolved. Dwarf/rotation/cluster/lensing fits were not run or certified.

Next work must address the demonstrated bottlenecks, rather than rerun the same coarse model: (1) a locally positivity-preserving gravity/gas discretization with energy error far below candidate binding energy through cooled infall; (2) higher spatial and nonradial resolution with a full-action binding and escaping-energy diagnostic; (3) a chemical/recombination network with density-dependent H2 cooling and a physically derived baryon/photon/field initial history; (4) only then a population and joint growth/galaxy/cluster tests. The late cooling run explicitly requires a cooling treatment beyond the low-density fit, not a relaxed guard. No parameter retuning or successful remnant catalogue exists.

Reproduction commands, bounds, inputs and outputs are recorded in each manifest. Use new output directories and preserve failed/timeout records. Validation status and final hashes are in VALIDATION.txt and CHECKPOINT.sha256. All dispatched runs have completed or timed out; none is intentionally left running. Self-review only, no independent full solver. The figure is illustrative postprocessing, not independent evidence.
