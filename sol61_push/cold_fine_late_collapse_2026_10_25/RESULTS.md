# CCT021: finer runs through later collapse

The finer original-history Draco and Sextans fields pass the former coarse stopping times while retaining the registered numerical gates. Neither reaches the registered settling window. This is a finite negative formation result for this branch, with explicit remaining resolution and physical-model limitations. It is not a four-dwarf solution or a universal impossibility theorem.

## Final bounded segments

| Quantity | Draco | Sextans |
|---|---:|---:|
| Accepted fine parent T | 1.7323274914 | 1.7223998624 |
| Final T | 3.1083134213 | 3.3798744551 |
| Elapsed collapse time, Myr | 298.571 | 313.660 |
| Registered last window T | 3.10 | 3.35 |
| CDF range / total mass; limit 0.01 | 0.299689 | 0.229101 |
| Reference-sphere mass relative range; limit 0.05 | 0.132015 | 0.140750 |
| Half-mass radius relative range; limit 0.05 | 0.701904 | 0.501046 |
| Maximum relative mass error | 2.1084e-11 | 5.0422e-11 |
| Maximum energy residual / original energy scale | 2.50075e-6 | 2.27201e-6 |
| Maximum residual-phase occupancy; limit 0.05 | 0.0120037 | 0.0147857 |
| Peak measured RSS, bytes | 115212288 | 117260288 |

Both stopped at their new explicit 1800-second segment budgets, not a numerical gate. Neither reached the requested absolute T8 horizon. Both have null birth time, no passive cohorts and null stellar-validity flag. Consequently stellar survival has not been tested. Exact complex fields, original mass/energy references and full birth-test histories survive in the wall-stop checkpoints. There was no renormalization, mesh interpolation, changed physical parameter, manufactured sink or delayed replacement of a previously born stellar population.

All three last-window conditions fail in each dwarf. Sextans' CDF range is declining from its earlier peak, but remains about 23 times the limit. Draco's is about 30 times the limit. Extrapolating either trend into eventual settlement is unsupported.

## Actual-data diagnostics, not evolved stellar velocities

`analysis_001/result.json` keeps 164 complete-profile LOS rows, 76 held-out Draco proper-motion rows and 24 exact-time lineage comparisons. Both source-law footings and beta=-0.5,0 are retained. Sextans' two tracer components are reported separately, without an invented mixture. Survey metadata and author-provided Draco PM files retain their exact hashes.

At the final stored fine state, canonical beta=0:

| Diagnostic | Draco | Sextans |
|---|---:|---:|
| Cold mass inside observed reference radius, Msun | 1.42227e8 | 1.29256e8 |
| Cold total mass, Msun | 5.21755e8 | 4.54576e8 |
| Cold half-mass radius, pc | 2863.62 | 3873.56 |
| Selected-position projected LOS support, km/s | 31.9005 | 18.7480–19.5394 |
| Selected-data constant-dispersion estimate, km/s | 9.70314 | 8.80064 |

These are instantaneous fixed-tracer Jeans moment diagnostics of the complete cold density. They do not measure an evolved stellar population or a formal likelihood significance. They show that retaining considerable cold mass is insufficient: the current inner force remains too large for these tracer diagnostics. A large outer half-mass radius does not erase the inner excess.

Original-history Fornax/Leo I evidence is reconciled in `CONTROL_BRIDGE.md` and `controls_002/result.json`. Finer old controls at T1.25 give 52.8421 and 41.7104 km/s, respectively, against selected-data 12.1355 and 9.03026 km/s. Their finite algorithm and late resolution limitations prevent treating these as converged matched late controls. The alternative vin/V=0.8 branch is not substituted. No four-dwarf acceptance is demonstrated.

## Resolution and physical scope

At the latest independently shared saved times, the coarse/fine CDF differences are 0.0571135 (Draco T2.5) and 0.0472597 (Sextans T3). Unrotated physical-wave L2 differences are 0.916330 and 1.016554; uniform-phase alignment leaves 0.893640 and 0.991530. Exact inherited-prefix matches are reported separately from independent refinement. Conservation and acceptable phase occupancy do not imply late mesh convergence. A finer independent trajectory is still required before quantitative late-wave claims.

The underlying model remains the spherical conservative CCT wave proxy with a fixed supported baryonic source, eta=1500 pc km/s, initial inflow 10 km/s and half the hypothetical catchment supply. It is not a derived Khronon/AeST/v3s action, SCT-M or a collisionless-clump result. Cold self-gravity is supplied once; tracer acceleration adds the baryon-only prescribed law and cold Newtonian force once. The selective coupling still needs a reciprocal action bridge. Spherical symmetry tests no spin export. Finite outer inventories with reflecting boundaries do not demonstrate escaping radiation at infinity.

The sampled fluctuation-binding identity is retained; binding of an averaged smooth density must not replace the average binding of the fluctuating field. No new smooth-envelope energy no-go is claimed.

Source-support clocks at the final reference sphere are descriptive only: Newtonian t_dyn=3.355 Myr (Draco) and 14.038 Myr (Sextans), with pressureless uniform-density reference t_ff=3.727 and 15.593 Myr. The sampled accumulated intervals are about 65.19 and 19.96 local dynamical times. These expose how much fixed gas support is assumed; they are not actual gas-collapse or stellar-birth deadlines. EOS, cooling, support, a cosmological start epoch and gas-to-star dynamics are absent. See `STAR_FORMATION_CONTEXT.md` for primary-source chronology and radial-selection caveats.

## Verification

`audit_001/result.json`: 416 integrity/operator/restart/window checks passed, zero failed; 12 original solver/prolongation unit controls passed. Both real stellar branches are explicitly inactive. The audit validates saved-state provenance and recorded diagnostics, not a replay of nonexistent stellar trajectories or proof of physical convergence. All seven new manifests pass the computation-evidence validator, including the retained, explained `controls_001` alias failure. `controls_002` corrects only that alias and completes. Setup `analysis_preflight_*` and `audit_preflight_*` directories are noncanonical and excluded from these execution counts. Figure pixels were inspected after generation.

Read `NEXT.md` for accepted restart parents, executable continuation instructions and the remaining mechanism obligations.
