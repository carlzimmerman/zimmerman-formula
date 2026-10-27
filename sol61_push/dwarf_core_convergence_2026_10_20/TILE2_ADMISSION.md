# Tile2 backend: bounded admission, 20 October 2026

`tile2_gravity.mm` / `tile2_gravity.py` are a distinct ABI5 implementation and
binary. They retain full three-dimensional, ordered off-diagonal Plummer pairs
and exact raw three-component coordinate encoding. Pair displacements and
interactions are FP32. Four independent FP32 partial chains are reduced in a
balanced tree within each128-source tile, then merged into DS accumulators.
Safe Metal math and explicit distance FMA are used; this is a separately
declared empirical precision budget, not the DS1e-11 reference budget.

Use `TILE2_GRAVITY_LIBRARY=<absolute directory>/tile2_build_run_001/tile2_gravity.dylib`
and `from tile2_gravity import gravity, backend_metadata`. `gravity(x,m,eps)`
returns acceleration, total self-potential energy and per-particle potential.
`run_refined.py --backend tile2` and `launch_refined.py` freeze the correct
source, binary and reference closure. Root review is required before any new
production is launched by this subagent.

The6 unit cases pass, including the exact anisotropic513-particle torque case
and Gaussian32768 maximum-error case that failed tile v1. The v1 benchmark
remains a valid **failed** record at `tile_benchmark_run_001/manifest.json`;
its sources and results were preserved.

The completed `tile2_benchmark_run_001` passes all10 measured cases with
unchanged gates: forceL2<5e-7, per-particle relative max<2e-6, phi/U<5e-7,
and normalized net force/torque<1e-8. Cases include random anisotropic unequal
masses, a2pc remnant with a distant first tail and large coordinate offsets,
two actual evolved states, and the prepared262144-cold/294912-total dwarf.
For that actual dwarf: median1.514s, forceL2=3.89e-8, maximum=6.30e-7,
phi=5.49e-8, U=3.77e-8, torque=1.70e-11; one full DS reference took8.932s.
Gaussian262144 took0.956s,3.74x faster than the contemporaneous mixed baseline.
Other GPU users were not stopped; timings do not certify isolated throughput.

`initial_reference_old8k/` contains an exact byte-copy of the saved original
DS-normalized8k initial file and derived loader metadata. No initial sampling,
force calculation or velocity renormalization was performed. Its relative
phase-space SHA256 is
`b090c6ff60cf3917cd2e992a0836e948e0e1af7fa03bfaa76c061e3e002cd8b9`.

`run_tile2_admission8k_iso_dt05_1Gyr` completed in66.3s with the same initial
arrays, eps10pc,h25pc,dt0.5Myr, physical parameters and CTMC seed as the original
`run_pilot_gpu8k_iso`. Ten evolved full CPU/DS comparisons all passed; worst
forceL2=6.83e-8 and maximum=9.17e-7. Maximum total-energy defect was4.114e-4
of initial internal binding, normalized vector-J defect8.23e-11 and momentum
defect9.57e-10. These pass the declared bounded admission gates.

`tile2_admission_comparison_001` records descriptive trapezoidal time averages
over800–1000Myr. Mean M300 differs by+0.711% and M100 by+0.505%; all density
bins with boundaries within250–2000pc differ by at most5.603%. All radii are
retained in the JSON. Events differ254 versus236, so a shared seed does not
keep the diverging CTMC trajectories coupled. Snapshot time variation is not
independent sampling error.

The build, benchmark, initial import, trajectory and comparison manifests all
validate against the project root. This supplies bounded backend admission.
It does not establish an inner flat core, higher-N density convergence, host
remnant convergence, later10Gyr accuracy or resolution below250pc. Production
still needs independent timestep, force-softening/support and physical
resolution controls with this separately declared arithmetic budget.
