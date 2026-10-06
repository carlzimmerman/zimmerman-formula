# Real transfer initialization and a sourced relative-velocity null test

The new advance is a source-closed test using actual CLASS density **and velocity** transfers, rather than selected toy modes. It confirms the initial-velocity nuisance, separates three restricted source templates across scales and epochs, and quantifies the numerical accuracy needed before proposing a cold-wave inference. It does not derive a cold mass, observational detection, or 32pi.

## What was actually computed

The existing local L183 CLASS extension reports v3.3.4. Its MOND patch is disabled with `mond_a0=0`; the inspected source guards the extra force behind `mond_a0>0`. No installation, rebuilding, or peer-file writes occurred. Newtonian-gauge CLASS-format `d_b,d_cdm,t_b,t_cdm,t_g,phi,psi` were obtained at 601 log-a-spaced epochs z99→19, on 124 CLASS wavenumbers extending to k10/Mpc. The thermodynamics table supplies baryon sound speed and Thomson opacity; background densities supply 4rho_gamma/(3rho_b). Exact local binary, wrapper, source and Python-executable hashes are in `sources.json`. This authenticates the used artifacts; it is not a reproducible fresh build of upstream CLASS or an independent Boltzmann solver.

Baseline inputs are h=.6736, omega_b=.02237, omega_cdm=.1200, N_ur=3.046, no massive neutrinos, no perturbed recombination, and default standard reionization. The tested interval z≥19 avoids its late-time application. This is a declared benchmark, not the exact Planck massive-neutrino baseline. Perturbation integration tolerance is 1e-9, sampling stepsize .02, thermo tolerance1e-8. The pressure closure is CLASS's ordinary Ma–Bertschinger adiabatic sound-speed approximation, not a perturbative temperature/recombination calculation.

## Exact dictionary and integral diagnostic

Primes in the following equations denote conformal time, dots cosmic time. Set c=1 with lengths Mpc, H in Mpc^-1, theta in Mpc^-1, and physical sound speeds expressed as fractions of c. CLASS k is returned in h/Mpc and multiplied by h once. For pressureless baryon/cold continuity with common metric,

    Delta = delta_b - delta_c
    Delta' = -(theta_b-theta_c)
    U = a² dot Delta = -a(theta_b-theta_c).

Subtracting Euler equations gives

    dot U = -k²(Psi_b-Psi_c) - c_b² k² delta_b
            + c_c² k² delta_c - Gamma_b(theta_gamma-theta_b),
    Gamma_b = [4rho_gamma/(3rho_b)] kappa',
    dt = da/(aH).

The conformal drag coefficient appears directly in dot U: factors of a cancel when differentiating −a Delta-theta. This sign and normalization match [Ma & Bertschinger, eq67](https://arxiv.org/html/astro-ph/9506072v1). The local source's baryon/CDM Euler equations independently match. A common gravitational force cancels even in a radiation-plus-vacuum background; no EdS approximation is needed for this cancellation within these continuity/Euler assumptions.

Define source-subtracted epoch residual

    N(k,a) = [U(a)-U(a_i)-integral(S_gas+S_drag)dt] / norm(k),
    norm(k) = a_i² H_i delta_m(k,a_i),
    delta_m = f_b delta_b + f_c delta_c.

This removes the arbitrary inherited U(a_i) rather than setting it to zero. All transfers and norm scale together with a mode's primordial curvature amplitude; the ratio cancels that common nonzero amplitude. It does not remove independent isocurvature amplitudes, incoherent modes, transfer/tracer biases, or observational cosmic variance.

At z99 the actual U/norm at k(.01,.03,.1,.3,1,3,8)/Mpc is approximately (−.01629,−.06217,−.03801,−.03917,−.03893,−.03890,−.03916). These inherited values dwarf the sourced change. At k8 the measured DeltaU/norm is −.00217889, comprising gas −.00209435 and photon drag −.0000845317. At k.01 pressure is only −3.62e-9 while drag remains −8.20e-5. Residual drag therefore cannot simply be discarded after recombination.

The acoustic-state growing projection uses **both** density and velocity:

    delta_m,N = -theta_m/(aH) + 3 phi_N,
    A_at_i = (3delta_m+2delta_m,N)/5,
    B_at_i = 2(delta_m-delta_m,N)/5.

These exactly reconstruct the instantaneous EdS state dictionary, delta_m=A_at_i+B_at_i. In the real radiation/vacuum CLASS baseline these are not invariant growing/decaying dynamical amplitudes. Density-only initialization delta_m,N=delta_m errs by up to13.68% in the tested initial logarithmic derivative; the projection error has the corresponding 2/5 factor. Raw projected initial states and relative density/velocity are saved, not chosen by hand.

## New wave diagnostic and unavoidable degeneracies

For the nonrelativistic subhorizon free-wave regime, c_c²=ell² k²/(4a²), ell=ħc/(m_eV Mpc_metres), so

    S_wave = ell² k⁴ delta_c/(4a²).

This is the late-time regime of [Hu, Barkana & Gruzinov eq7](https://arxiv.org/html/astro-ph/0003365v2); it requires a≫k ell/2. The same primary paper authenticates the previously provisional CFG345 cutoff formula eq8-9; that cutoff fit is **not** used to generate these baseline transfers.

In exact EdS, H=H_E a^(-3/2), delta_c=D(k)a and q=ell² k⁴/4,

    DeltaU = 2qD/H_E (sqrt(a)-sqrt(a_i)),
    Delta_source = 2qD/H_E² [ln(a/a_i)-2(1-sqrt(a_i/a))].

The growing relative fraction is proportional to ln(a)/a asymptotically, while U grows as sqrt(a). Thermally decoupled gas c_b²=v0²/a² with delta_b=D_b a has the identical time kernels, replacing qD by −v0²k²D_b. Time dependence alone cannot distinguish them. Multiple scales discriminate k² from k⁴ only with a common scale-independent thermal coefficient and constrained initial density ratios. Constant differential potential gives DeltaU proportional to a^(3/2), but a potential decaying as a^-1 matches the wave's time kernel.

More strongly, an arbitrary differential potential

    Psi_b-Psi_c = -ell² k² delta_c/(4a²)

reproduces the wave forcing identically for every k and epoch. This is an algebraic observational degeneracy, not a demonstrated healthy covariant competing action. Nor is k⁴ unique to free waves: a positive effective fluid gradient energy rho kappa |grad_physical delta|²/2 yields c_eff²=kappa k²/a² and the same linear k⁴ restoring term. Additional stress/action assumptions are necessary for microscopic identity. These degeneracies are explicit negative controls.

## Quantitative scope and next observable model

Born source integrals use the actual **CDM reference** delta_c, holding its z99 state fixed. They forecast an incremental post-z99 pressure source, not a self-consistent massive-wave transfer from the primordial radiation era. This distinction is especially important at m1e-22eV near its primordial cutoff. The stiffness/H² is below.026 at k8,z99 for that mass; this is a necessary late-interval Born check, not proof that the common CDM initial state is physically generated by that mass. The larger mass benchmarks have smaller late and early pressure effects, but their abundance/initial-state history remains a separate calculation.

At k8/Mpc, z99→19, the normalized incremental wave sources are:

| benchmark mass eV | DeltaU_wave/norm | max wave stiffness/H² |
|---|---:|---:|
| 1e-22 | .064748 | .02568 |
| 2e-20 | 1.6187e-6 | 6.4203e-7 |
| 2e-19 | 1.6187e-8 | 6.4203e-9 |

The latter two are illustrative masses used in earlier small-scale work, not an endorsement of its empirical bounds. At k1 the m2e-20 increment is only3.95e-10. No32pi coefficient enters these sources. Any claimed connection requires the **same** action to predict mass/stress and its coupling to baryons/metric and vacuum normalization.

A concrete next forecast uses N(k,a_j), seven k values and three late epochs, with columns: W from the integrated wave source; G from gas-temperature-normalization error; Q from a constant differential potential proportional to initial phi(k). Projecting out independent U_i per mode is built into epoch differences. The three unit-length column singular values are (1.50473,.85351,.08547): the restricted model is invertible, albeit correlated. Synthetic coefficients (.7,−.2,.4) are recovered. At a single k the EdS gas and wave columns are exactly collinear.

For an explicitly hypothetical covariance C, let P project out gas/gate and any added nuisance columns. Then F_alphaalpha=W^T C^-1 P W, alpha=(1e-22eV/m)². With equal independent normalized noise sigma_N on the 21 cells, ||P W||=.00936845 and sigma_alpha=sigma_N/.00936845. An **assumed**, not achieved, sigma_N=1e-6 gives sigma_alpha1.0674e-4; alpha at m2e-20 is2.5e-5. Thus even this toy noise model does not supply a strong detection at that mass. No instrumental sensitivity is asserted, and realistic epoch/mode covariances must replace independent-cell noise.

Observation requires baryon density/velocity tracers and a metric/matter reconstruction. For example, neutral-gas/21cm density plus redshift-space velocity information could constrain baryonic transfer, while lensing/metric data constrain matter **within a specified gravitational action**. Inferring delta_c=(delta_m−f_b delta_b)/f_c and theta_c requires that action's metric equations, bias and thermal/ionization response; lensing alone does not directly measure cold density. This is a concrete forecast input model, not an available measured cold transfer. Arbitrary differential-gate templates or arbitrary scale-dependent gas stress destroy identifiability even with noiseless data.

## Validation, failed routes and handoff

The default CLASS integration tolerance1e-5 produces a maximum null residual7.78e-5, failing the1e-6 bound. Its standard-runner record is retained as `runs/default_precision_negative/` with statusfailed; manifest validity authenticates a failed calculation, not a success. Tightened tolerance1e-9 gives4.0606e-8; tolerance1e-10 gives2.6725e-8. Attempting1e-11 hit CLASS's minimum-step error and was abandoned, not counted as validation.

At fixed1e-9 tolerance, changing301→601 epochs changes the gas integral by at most9.2654e-10 and drag integral1.0959e-9 normalized units; U is identical on common epochs. The null maxima4.1436e-8 vs4.0606e-8 show quadrature is not the dominant residual. The m2e-20 wave source changes by only2.42e-15 between1e-9 and1e-10 solver tolerances. These are numerical consistency/sensitivity checks, never survey noise or a certified physical accuracy bound.

The finite checks cover Euler-source closure, actual-velocity state reconstruction, EdS primitive derivative, restricted design rank/coefficient recovery, exact single-k time degeneracy, false signal from omitted initial U, primordial-amplitude cancellation, and exact arbitrary-force mimicry. All three positive standard-runner manifests validate; the negative manifest also validates its failed status. `convergence.json` records the independent comparison and root-kernel review input hashes. `REVIEW_ROOT_KERNEL.md` independently reconstructs root's analytic kernel.

The remaining arrow is an observation/transfer model with constrained baryon stress and differential gravity and controlled cold reconstruction. This experiment advances the discriminator and rejects numerical/initial-state shortcuts; it does not identify cold microphysics or close the common-action/vacuum-normalization problem.
