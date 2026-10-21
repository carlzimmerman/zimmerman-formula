# Signed transport from prepared cold-core disturbances

**Finite result:** the prepared K50 and K500 states export energy and Noether charge through r20/r30/r40, with predominantly outward currents at the larger surfaces. K1 does not give a positive monotone control-subtracted loss over the full interval. No weak `gamma K^2` law, spectrum, galaxy escape or four-dwarf efficiency is inferred.

The fresh read-only audit `face_flux_dressed_run_001` completed **1004/1004 checks**, with a valid v2 manifest, numerical runtime1.281 seconds and measured RSS118358016 bytes. It reads100 immutable snapshots (four completed cases, t0:10:240). It does not advance any field. Its 132 predeclared input artifacts have observed unchanged before/after hashes. All four source-evolution manifests also validate. Exact receipts are in `sources_face_flux_dressed.json`.

## Same signed-current kernel, new finite comparison

`face_flux_dressed.py` is a separate copy of frozen `face_flux.py`. The complete `read`, `evaluate` and `ck` function ASTs are identical. Changes are the scope/cadence text, configured time windows and an explicitly labelled K0 control subtraction. Neither equations nor the local-energy allocation changed.

For an oriented interior face i to j,

    F_E = sum_a fac_a Cij (q_ai-q_aj)(v_ai+v_aj),
    F_Q = -2 Cij Im(Psi_i* Psi_j) - 4 Cij Im(X_i* X_j),
    fac = (1,1,1,1,1/2).

The conductances are `Cij=2pi R_face` radially and `2pi R_cell` axially on the equal-spacing cylindrical grid. Apertures use whole cells with `r_cell<R`; energy assigns positive half-links to their endpoints. The original derivation and sign controls are in `FACE_FLUX.md`. Independent ODE differentiation of the local energy/Q agrees with these cut-face currents to at most1.411e-12/1.530e-12 in the normalized instantaneous continuity checks. Recomputed box and r20 inventories also reproduce saved logs within their declared1e-10 relative tolerance. Instantaneous continuity does not guarantee accurate integration at a10-unit output cadence.

All new cases are quasistatic-chi prepared Cauchy states with actual differing Q/E. Nominal K labels a linear coordinate; K500's initial baseline-relative `Delta(E-omega_ref Q)=890.681279`, rather than500. The preparation energy differences are not radiation.

## Whole-interval endpoint inventories

Positive entries mean initial-minus-final inventory inside the indicated aperture. These are measured inventories, rather than an identification with bound mass or quanta.

| Case | r30 E drop | r30 Q drop | r30 E drop minus K0 | r30 Q drop minus K0 |
|---|---:|---:|---:|---:|
| K0 | 1.624102 | 1.272184 | 0 | 0 |
| K1 | 1.473241 | 1.141902 | -0.150861 | -0.130282 |
| K50 | 53.986694 | 50.076444 | 52.362592 | 48.804260 |
| K500 | 3585.009614 | 3144.400358 | 3583.385512 | 3143.128174 |

K0 itself exports about1.6 energy and1.25 charge through each large aperture. Thus zero prescribed quadrupole is not zero transient response. Subtracting K0 compares two different full Cauchy evolutions, with different total Q; the difference is **not automatically modal or radiative power**. A negative difference means the perturbed case loses less inventory than K0, rather than proving physical absorption or the absence of every possible radiation channel.

## Snapshot-integrated currents and measured discrepancies

The following table uses K0-subtracted controls on t0..240. `D` is the endpoint drop difference and `I` is the10-unit trapezoidal current-integral difference. Discrepancies are absolute `|I-D|`, retained even for small or negative signals.

| Case | R | D_E | D_Q | I_E | I_Q | abs E discrepancy | abs Q discrepancy |
|---|---:|---:|---:|---:|---:|---:|---:|
| K1 | 20 | -0.070641 | -0.052110 | -0.138588 | -0.077148 | 0.067946 | 0.025039 |
| K1 | 30 | -0.150861 | -0.130282 | -0.144070 | -0.127909 | 0.006790 | 0.002374 |
| K1 | 40 | -0.166072 | -0.145185 | -0.189083 | -0.145834 | 0.023011 | 0.000650 |
| K50 | 20 | 67.209257 | 63.183085 | 66.990550 | 62.514525 | 0.218707 | 0.668559 |
| K50 | 30 | 52.362592 | 48.804260 | 51.040206 | 48.625592 | 1.322387 | 0.178667 |
| K50 | 40 | 41.006607 | 37.780523 | 42.413989 | 38.096051 | 1.407382 | 0.315528 |
| K500 | 20 | 3811.718385 | 3364.171030 | 4124.495849 | 3415.563337 | 312.777464 | 51.392307 |
| K500 | 30 | 3583.385512 | 3143.128174 | 3446.520783 | 3124.901837 | 136.864729 | 18.226337 |
| K500 | 40 | 3326.683950 | 2892.062997 | 3405.413589 | 2896.206742 | 78.729639 | 4.143745 |

The large cases' outward signs are not just allocation outside an aperture. For un-subtracted K50 at r30, integrated positive/negative E currents are +52.655181/-0.006642; for K500 they are +3449.506228/-1.377112. Aggregate ratios do not identify a free-particle spectrum, and an outgoing surface crossing does not establish permanent escape.

The early impulse is materially undersampled. For K500 at r20, the t0..40 control endpoint E drop is870.233497 but the current integral is1218.186370, an excess347.952873. The later40..120 interval partially cancels this error. Without subtraction, the whole-interval E-current integral exceeds its endpoint drop by314.937316; the remaining control discrepancy is312.777464. The detailed result preserves0..40,40..120,120..180,180..240,0..180,0..240 and120..240 windows separately.

At fixed `omega_ref=.9120838357251844`, the K500 r20 control integral of `F_E-omega_ref F_Q` is1009.215740, whereas the control endpoint decrease of `E-omega_ref Q` is743.312368. The former can appear larger than the initial890.681279 excess simply because of this temporal quadrature error. The endpoint budget does not violate that initial budget. Neither number is automatically energy above an actual-charge stationary core or useful galaxy-centred wind energy.

K1 has small positive late differences at some surfaces (for example r20 E drop0.055876 in180..240), while its whole-interval and larger-surface control differences are negative. Propagation delays, background response and the finite sampling window matter. This comparison does not resolve a universal weak-loss law. No numerical weak-rate claim is made here.

## Scope and next discriminating check

The measured E/Q current signs and endpoint changes establish finite transport in this alternative action. All states have m0 axisymmetry and zero orbital angular momentum. Local fluxes neither supply a galactic torque receiver nor establish the Draco/Sextans versus Fornax/Leo I selector.

The box is finite and reflecting, the new seed trajectories have no independent dx/dt refinement, and the prepared charged configurations are not accepted nonlinear periodic modes. Higher-cadence face currents are needed to resolve the strong early impulse without reconstructing an efficiency from undersampled integrals. Outgoing-state/spectral classification and a controlled actual-charge remnant reference are separate necessary tests before interpreting the transport as a calibrated radiation/capture kernel.
