# Independent review of initial-state loading and prepared-seed comparisons

**Verdict: computationally verified only in the stated finite range.** The loader changes initialization only. Its replay controls and the quasistatic neutral-field preparation pass the checks described below. The four prepared Cauchy evolutions are conservative finite experiments, not accepted nonlinear normal modes, physical cooling histories or a four-dwarf mechanism. This review performed no field advancement or repeated elliptic solve.

Exact reviewed bytes, manifest statuses and numerical checks are pinned in `sources_review_seed.json`. The separate new transport analysis is in `DRESSED_FACE_FLUX_RESULT.md`.

## 1. Loader and test-first evidence

The seed C source has only three changes relative to frozen `pair_axisym_v2.c`: a strict t0 input helper, allowance for its extra argument, and a `snapshot` initialization branch. Independently reversing those three changes reproduces the entire v2 source exactly. Force equations, Laplacian, boundary treatment, potential, diagnostic allocation and kick-drift-kick code are unchanged. The legacy profile is still read before initialization; it is pinned as an input but its Q80000 table does not replace the supplied Q136000-reference Cauchy fields.

The helper requires the exact CEPAIR1 magic, dimensions and grid spacing, time zero, ten complete finite binary64 field/velocity planes and no trailing byte. This is a native-format initial-data interface, rather than a general restart or cross-endian serializer.

The red run has a valid manifest recording **failed**, exit 1, and no result JSON. Its old binary rejects the extra argument before accepting a seed. That is the intended interface failure; it is not a physical counterexample. The green run has a valid completed manifest and 18 passing checks. Independently compared both static and moving replay snapshots at t0 and t5 and their full diagnostic logs byte for byte. All are exact. The seven malformed fixtures produce the expected header/nonfinite/truncated/trailing rejection messages. This proves the tested replay behavior, rather than every possible input or future compiler optimization.

Build receipts match current source/binary hashes. `METADATA_CORRECTION.md/json` separately preserve a historical compiler annotation error in 18 old records; no frozen record was overwritten. New seed contracts use the compiler string from the seed build receipt.

## 2. Why the undressed seeds were unsuitable weak-mode controls

The raw constructor embeds a prescribed linear Y20 coordinate with amplitude `A=sqrt(K_nom)` into the full action. Accurate recovery of that coordinate does not make its nonlinear Hamiltonian excess equal to `K_nom`. Independently expanding the saved states' exact finite-volume energy and charge gives

    Q(A) = 136190.6613513635
           + 3.361410175648 A + 26.464784111980 A^2,

    Delta(E-omega_ref Q)
         = -0.112739759171 A + 0.952905934176 A^2
           -0.004674506463 A^3 + 0.201558973671 A^4,
    omega_ref = 0.9120838357251844.

Independent polynomial evaluation reproduces the saved raw E/Q within 1e-7 absolute. At nominal K50, the quadratic contribution is 47.6453 while the quartic contribution is 503.8974; total grand excess is 549.09285. At K500 those contributions are 476.453 and 50389.743, with total 50811.41288. Both are quartic-dominated undressed perturbations. Their accurate linear projection does not justify weak-rate extrapolation. These raw high-amplitude states were not used for the new field evolutions.

## 3. Restricted validity of quasistatic chi preparation

For fixed charged fields, the neutral configuration energy is

    H_chi,config = sum_i w_i [ -chi_i Lap(chi)_i/2
                              + U(chi_i) + a chi_i |Psi_i|^2 ],
    U = M^2 chi^2/2 - M chi^3/8 + chi^4/4.

Its stationary equation is `-Lap chi + U'(chi) = -a |Psi|^2`. The real Hessian satisfies

    U''(chi) = 3(chi-M/8)^2 + 61 M^2/64 > 0.

The weighted finite-volume minus-Laplacian is positive with the stated Dirichlet faces and regular axis. The finite configuration energy is therefore strongly convex and coercive, giving a unique minimizer for each fixed charged configuration. Differentiating that stationary equation gives the instantaneous tangent equation

    (-Lap + U''(chi)) chi_dot = -a I_dot,
    I_dot = 2 Re(Psi* Psi_dot).

This tangent solve is well-posed; it does not replace the full dynamical chi equation during subsequent evolution. Configuration minimization is not automatically minimization of the full energy after selecting a nonzero tangent velocity. The saved full kinetic-plus-configuration energy is therefore the relevant check. Here I_dot is essentially zero at the selected phase and full energy decreases in the actual four preparations.

The completed preparation has a valid manifest, 56 passing checks and measured RSS 212713472 bytes. Independently verified all eight charged field/momentum planes **bit for bit**, including the explicitly interpolated K1 state. Independently recomputed the full finite-volume energy and Q: E agrees within 5.9e-11 absolute and Q exactly with the saved diagnostics. Static residual maxima are at most 5.619e-9; tangent residual maxima at most 8.428e-14. The saved residuals are independently reproduced. The energy-gradient directional controls agree to better than 5e-10 relative. Reported small contraction factors concern this tested iteration region; no global convergence claim for arbitrary initial guesses follows.

| Nominal coordinate K | Actual Q | Prepared full E | Delta(E-omega_ref Q), versus prepared K0 |
|---|---:|---:|---:|
| 0 | 136190.661351 | 127610.616682 | 0 |
| 1 | 136220.487546 | 127638.657719 | 0.837047562 |
| 50 | 137537.669316 | 128888.110639 | 48.909765342 |
| 500 | 149498.216824 | 140638.904201 | 890.681279154 |

At K50 and K500, full energies are respectively 500.183089 and 49920.731599 below the raw preparations. Those are differences between initial data, **not measured emitted energy**. The actual grand excess is still not forced to the nominal coordinate. K500 also retains a large charge shift and nonlinear deformation; the preparation does not turn it into a weak normal mode. Charged fields receive no DC or stationary-branch correction.

## 4. Completed evolution health checks and design limits

All four completed v2 evolution manifests validate with current hashes; each has 8 passing declared checks. Each loads the prepared t0 snapshot exactly and uses Nr188, Nz480, dx0.75, dt0.005, T240, snapshot cadence10 with unchanged full equations. Maximum relative E changes for K0/K1/K50/K500 are respectively 1.829e-9, 1.799e-9, 4.146e-9 and 9.366e-8. Multiplying by initial E gives absolute drift maxima about 0.000233, 0.000230, 0.000534 and 0.013172. Maximum relative Q changes are below 5.5e-14. Solver RSS is about 17.2 MB. The loose predeclared global-energy bound is a health check; these actual observed errors are the stronger finite evidence.

The actual Q values differ between amplitudes, and even K0's sampled charge differs from nominal Q136000. Thus frequency changes can mix amplitude response, stationary-branch charge dependence and grid/reference mismatch. The exact diagnostic Delta(E-omega_ref Q) is not automatically `E-E_stationary(Q_actual)`. K0 coordinate subtraction is useful control information, not a proof that the residual coordinate or current is modal energy/radiation.

The box has radial boundary141 and axial boundaries +/-180, with reflecting zero-Dirichlet faces. T240 is finite and does not certify permanent escape. Initial profiles extend to radius60 with small tails; a blanket claim that every aperture/time lies before all possible boundary returns is unjustified. The specific slow Psi second-harmonic reference packet has much later travel times, but broadband transients must not be assigned that speed without spectral evidence. New prepared seeds lack their own spatial/timestep convergence comparison; old pair controls do not supply that error bound.

At the reference Omega0.0603874, cadence10 gives about10.4 samples per oscillation and5.2 per second harmonic. It undersamples the lab carrier near0.912, so known-carrier demodulation is essential. A 20..180 fit covers only about1.54 reference cycles and a190..240 holdout about0.48 cycle. Such tests can identify finite-window components; they do not by themselves establish an eigenfrequency, damping coefficient or uncertainty interval.

These are axisymmetric m0 states with zero orbital angular momentum. Neither a prepared isolated state nor a flux through a small control surface proves galactic energy/torque transfer, capture, physical unit normalization, survival or protection of Fornax/Leo I.
