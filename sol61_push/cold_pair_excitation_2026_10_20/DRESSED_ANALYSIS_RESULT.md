# Dressed Cauchy-data comparison: weak, moderate and strong shape excitation

The weak nominal-K1 seed preserves an approximately unit baseline-subtracted quadrupole coordinate for the tested 240 time units and supports a well-predicted finite-window oscillatory component. The K50 and K500 preparations show progressively slower, less coherent coordinate evolution and more outward aperture transport. These are useful finite Cauchy-data distinctions; they do not establish fixed-charge nonlinear normal modes, physical damping rates, or a merger-excitation efficiency.

The new `dressed_analysis_run_001` completed 552/552 declared controls with a valid v2 manifest, measured RSS 129,728,512 bytes and analysis runtime 12.61 seconds. It reads the four completed dressed evolutions only. No field, stationary, eigenvalue or outgoing calculation was added. The mathematical plan was written before their completion; execution waited for the parent's explicit confirmation that all four conservative evolutions were complete and passed their eight frozen controls each.

## Preparation and accounting scope

The data use quasistatic-chi-prepared initial fields/momenta followed by the unchanged conservative five-real-field equations. They are not the earlier undressed seeds with a large nonlinear potential-energy mismatch. However, the dressing is initial preparation, not measured radiation, and neither it nor nominal K fixes the actual charge or makes the state a nonlinear periodic solution.

All projections use the same Q136000 radial reference, omega_ref=0.9120838357251844 and Omega_ref=0.060387406141327836. The primary carrier frame is consistently theta=omega_ref*t, including the charge-two X velocity transformation. Complex K0 coordinates are subtracted **before** squaring. This controls the tested numerical/background anisotropy; it is not an exact nonlinear energy decomposition.

The actual initial fixed-carrier grand differences and conserved charges are:

| Nominal K | Initial total Q | Delta Q from K0 | Initial Delta E - omega_ref Delta Q |
|---|---:|---:|---:|
| 0 | 136190.661351 | 0 | 0 |
| 1 | 136220.487546 | 29.826194 | 0.837048 |
| 50 | 137537.669316 | 1347.007965 | 48.909765 |
| 500 | 149498.216824 | 13307.555473 | 890.681279 |

In particular, nominal K500 is not actual nonlinear grand excess 500. At fixed omega_ref, Delta(E-omega_ref Q) is an exact difference of the supplied global initial states; it is not E-E_stat(Q_actual). No reference at the actual charge was inserted. Frequency differences therefore mix amplitude/state changes with movement along the charge-dependent stationary family.

## Direct numerical health relative to the actual excess

The analysis recomputes maximum observed-time E/Q errors directly from the saved logs. It also evaluates

    D_K(t)=[E_K(t)-E_0(t)]-omega_ref[Q_K(t)-Q_0(t)]

and reports max_t |D_K(t)-D_K(0)|, rather than relying only on the full-energy pass threshold.

| Nominal K | Max relative total-E error | Max absolute global grand error | Max absolute baseline-difference grand drift | Drift / actual initial excess |
|---|---:|---:|---:|---:|
| 0 | 1.8290e-9 | 0.000233405 | 0 | — |
| 1 | 1.7987e-9 | 0.000229583 | 0.000012300 | 1.4694e-5 |
| 50 | 4.1456e-9 | 0.000534318 | 0.000606286 | 1.2396e-5 |
| 500 | 9.3656e-8 | 0.013171676 | 0.013263409 | 1.4891e-5 |

Maximum relative Q errors are below 5.5e-14. This is good finite-run conservation at the sampled diagnostic times. The grid/time/finite-box accuracy of the physical trajectory and a flux measurement remain separate; conservation does not establish mode purity or radiation efficiency.

## Fixed-frame, baseline-subtracted coordinates

The primary difference-coordinate squared is:

| Nominal K | Initial coordinate squared | Range over t=0..240 | Final coordinate squared |
|---|---:|---:|---:|
| 1 | 0.999955 | 0.971561–1.027769 | 1.000004 |
| 50 | 49.999228 | 37.225517–49.999228 | 39.265050 |
| 500 | 500.029252 | 102.916939–500.029252 | 102.916939 |

K0 subtracts identically to zero and is assigned no difference-coordinate frequency. The weak K1 signal persists above that background control. The K50/K500 decrease is a change in a conditional projection: mode conversion, nonstationarity, reference/charge change and transport can all contribute. Calling the decrease radiated mode energy would exceed this experiment.

The full sampled-field mismatch relative to the fixed radial reference reaches about 0.035 at K1, 0.129 at K50 and 0.516 at K500. For the strong seed the ell2 reconstruction-state residual reaches about 0.82. The norms support treating K500 as a strongly nonlinear/mixed Cauchy comparison. They are not themselves energy or bound-stock measurements.

## Train-only harmonic identification with held-out prediction

The predeclared complex basis is 1, exp(+-i Omega t), exp(+-2i Omega t). Training uses only t=20,30,...,180 (17 complex samples); test uses t=190,...,240 (six samples), with **no test refitting or frequency selection**. The training window spans only about 1.54 reference cycles and test about 0.48. Frequencies are tested from 0.03 to 0.09 at step 0.00005; that spacing is not a frequency uncertainty.

For the primary fixed-frame K0-subtracted signals:

| Nominal K | Train-selected base rate | Dominant signed harmonic | Known-Omega train / test residual | Selected-rate train / test residual |
|---|---:|---:|---:|---:|
| 1 | 0.05955 | +1 | 0.03938 / 0.10349 | 0.00295 / 0.00785 |
| 50 | 0.05860 | +1 | 0.08907 / 0.22568 | 0.02162 / 0.05385 |
| 500 | 0.05325 | +1 | 0.36074 / 0.86107 | 0.11989 / 0.17765 |

The weak seed gives the cleanest tested oscillatory component and best test prediction. The stronger states require slower coordinate rates and have larger train/test residuals. Because their total charges differ, these rows do not measure a pure fixed-Q amplitude-frequency relation. They also do not prove a nonlinear eigenmode or an autonomous damping law.

The weak evolved seed already prefers 0.05955, about 1.39% below the fine radial reference's 0.0603874; the raw K0 artifact also has a local fundamental minimum near 0.05945. The radial-to-cylindrical finite-grid/reference bridge therefore contributes a calibration issue even before a strong amplitude is considered. It is appropriate to compare stronger trajectories with this tested weak coarse-grid benchmark, while retaining its finite-grid and charge qualifications. The two-amplitude comparison does not replace spatial/time convergence.

Allowing second harmonics creates genuine identification ambiguity: a mode at Omega_ref can also appear as the second harmonic of Omega_ref/2. The script explicitly fits that known alias, reports signed harmonic powers and up to eight training minima. For raw K0 the selected base is the lower boundary 0.03 with dominant +2, corresponding to an observed coordinate rate 0.06 rather than a physical mode at 0.03. The primary nonzero baseline-subtracted fits listed above select dominant +1. Neither a boundary minimum nor a base rate alone is labeled softening.

The optional independently fitted-phase variant is retained in full, with velocity subtraction still fixed at omega_ref. It is an instantaneous coordinate sensitivity, not a second consistent frozen-frame trajectory. Primary conclusions above use the consistently propagated phase only.

## Core inventories

At t=240, the positive-face fixed-origin aperture diagnostics are:

| Nominal K | Q15 / current total Q | Q20 / current total Q | Q20(t240) / Q20(t0) | E20 / Q20 |
|---|---:|---:|---:|---:|
| 0 | 0.999555 | 0.999984 | 0.999991 | 0.936995 |
| 1 | 0.999552 | 0.999984 | 0.999991 | 0.936996 |
| 50 | 0.998886 | 0.999519 | 0.999532 | 0.937048 |
| 500 | 0.975514 | 0.977438 | 0.977487 | 0.936303 |

The stronger seed transports more charge/energy beyond the core aperture over this finite interval. An aperture boundary does not classify asymptotic escape, and the energy/charge ratio of its inventory is not the energy per escaped quantum. No new cold galactic mass or wind budget follows from these dimensionless charge accounts.

The useful next distinction is now concrete: a weak prepared shape component persists and predicts held-out coordinates well, while moderate/strong preparations have additional state/charge dependence and mixing that weaken a single weak-mode description. A radiation/branching claim still requires conservative outgoing E/Q/J flux and remnant-family accounting, not a projection decrease. These Cauchy preparations do not establish merger amplitudes, physical population rates, galactic orbital-J export, or Draco/Sextans success without Fornax/Leo I overboost.
