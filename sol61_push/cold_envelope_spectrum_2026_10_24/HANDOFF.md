# Continue CCT-008

Read RESULT.md and MECHANISM.md. The new result is a constructed supported endpoint, correcting eta=3000's quantum-virial incompatibility with the chosen Draco/Leo I profiles. Common eta=1500 supports all four targets in a stationary density-matrix extension. It is NOT completed coherent formation or current v3/AeST/SCT-M evidence.

Canonical endpoint files: eta1500_refine.json and eta1500_refine_{Draco,Sextans,Fornax,LeoI}.npz. The all-l producer is spectrum_v2.py. Max profile discrepancy <0.35%, same conditional static stellar calibration, Sextans source-spin capacity exceeds its benchmark demand. L<=4 fails the Sextans endpoint reconstruction despite 160 radial modes/l. An even-l-only endpoint also passes the looser 5% criterion; exact old even-m symmetry remains separate.

The spherical mixed-state remnant survives the bounded response test. Sextans dt=.01,T=20 max CDF drift .000932; refined kicked test dt=.005,T=20 drift .0144 and central mass range -6.71..+0.80%. This does NOT test nonspherical stability, pure-field interference or live stars. The time integration conserves mass and energy to the reported finite accuracy, uses fixed baryons and a reflecting outer box, and does not demonstrate cooling/capture.

The next decisive computation is formation into THIS supported endpoint:

1. Use eta=1500 rather than the now-incompatible 3000 benchmark for these target profiles. Preserve earlier failures.
2. Implement a bounded mode-transfer test using the conservative gravitational four-wave coupling in MECHANISM.md; track all vector-J components and positive-energy outgoing waves. Keep statistical closure and coherent-field results separate.
3. Address exact seed symmetries. An all-m spherical ensemble is not automatically reachable from the old even-m coherent seed. Specify justified small nonsymmetric perturbations, or construct a symmetry-compatible nonspherical endpoint. No arbitrary post-collapse population resets.
4. Reach the high-angular support channel, not only stronger l=0 cooling. Do NOT scale CCT-007's dense angular-matrix propagator directly to L=80: it would exceed the memory budget. Use sparse couplings or transforms and validate on the old low-L cases first.
5. Require correct per-dwarf mass profiles, paid capture/source energy, distinct retained supplies and live stellar DF tests. Endpoint fitting does not predict those inventories. The old oversized common source still demands extreme spin/mass rejection for Draco/Fornax/Leo I.

Reproduction (single-threaded, no old files overwritten):

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 sol61_push/cold_envelope_spectrum_2026_10_24/spectrum_v2.py --tag new_refined --eta 1500 --nr 6144 --lmax 80 --nrad 48
    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 sol61_push/cold_envelope_spectrum_2026_10_24/spectrum.py --tag new_even --eta 1500 --nr 6144 --lmax 80 --nrad 48 --parity even
    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 sol61_push/cold_envelope_spectrum_2026_10_24/verify.py
    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 sol61_push/cold_envelope_spectrum_2026_10_24/evolve.py --galaxy Sextans --tag new_kick --dt .005 --T 20 --kick .01

The full all-l reconstruction observed ~993 MB RSS, close to the cap. Prefer the saved states; redesign memory storage before increasing that library. Evolution <100 MB/process. No automation, shared job, remote repository or frozen publication was changed.
