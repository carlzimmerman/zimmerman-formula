# Spatial nonlinear evolution: result

The expanding reduced action has now been evolved with spatially varying3D fields and independent baryonic and cold particles. The simulations show smooth growth from0.1% seeds and nonlinear density peaks from3% seeds, but no resolved bound-core population or selected core masses. The stronger peaks remain resolution dependent, and the late physical grid cannot resolve the inherited core radius. The core-formation question is therefore unresolved, not answered negatively for the full theory.

## What changed

The prior one-mode restriction was removed. The new runs include exact nonlinear W, spatial chi, reciprocal particle forces, periodic gravity and canonical expansion evolution. Initial fields minimize the action's field energy at the given density, with velocities tangent to that minimum under expansion and the specified matter motion. This is a mathematically motivated low-excitation preparation. It is not a derived primordial state.

## Density growth and refinement

At z10, the maximum cold contrast delta_c=(rho_c-bar rho_c)/bar rho_c is:

| Initial peak contrast | Grid and particles per species | Final peak cold contrast | Final cold RMS contrast |
|---|---:|---:|---:|
| .001 | 8³ | .03679 | .01453 |
| .001 | 12³ | .03736 | .01467 |
| .03 | 8³ | 2.000 | .3750 |
| .03 | 12³ | 2.763 | .4024 |
| .03 | 16³ | 3.270 | .4169 |

Thus the finest strong peak has density4.27 times the mean, not a demonstrated compact remnant. Its peak differs by about18% from12³; the proposed5% spatial-peak criterion fails. Halving the timestep changes the strong8³ peak by only about7.3e-6 fractionally. The spatial resolution, rather than this timestep, controls the uncertain peak height. Baryons reach larger peak contrasts,5.88 at16³, but the pressureless baryon approximation is not a dwarf-galaxy calculation.

No saved state in the nine evolution runs contains a FoF candidate with32 cold particles at the declared link length. This is a finite detector result; it does not establish a general absence of bound objects. No bound mass catalogue or mass partition is available. The final periodic perturbation energy can be negative even in the diffuse .001 runs, demonstrating why its sign alone must not be used as a core detector.

## Resolution is insufficient for a core-mass claim

The16³ run ends with1.44kpc cells. The inherited canonical core radius is0.3215kpc, only0.223 cells. Approximately287 cells per axis would be needed merely to place four cells across that radius in this box at z10. That is a minimal target, not a convergence guarantee, and initial-box size and particle resolution impose further requirements. A mass measured from the present grid would be numerical structure, not an action-selected core mass.

The nominal core mass labels the initial wavelength convention; it is not the box mass. The cold box contains about5.47e8Msun. The particle masses range from1.07e6Msun at8³ to1.33e5Msun at16³. Reporting these discrete masses as remnant selection would be circular.

## Initial conditions are still not cosmologically selected

Earlier-start runs retain the same dust-reference amplitude using delta_i proportional to1/(1+z_i). At fixed8³ resolution, starting at z1100,2200 and4400 gives final peak contrasts .03679,.04155 and .06312. The last change is about52%; the10% preparation-history stability gate fails. These are explicitly different minimum-energy preparation histories in imposed EdS, not a claim about the real radiation-era transfer function.

The field minimizer is unique under the stated finite-dimensional convexity assumptions, but that uniqueness does not choose when the universe attains it, a primordial spectrum, or a physically realized field history. The initial tangent passes a finite-difference step check. Numerical reproducibility of a preparation is distinct from cosmological justification.

## Conservation and observational status

All nine evolution runs reach z10. Their maximum normalized expansion-work residual is1.46e-4; it decreases by approximately four on timestep halving. Separate species mass conservation holds to3.34e-16 in the independent check. The initial force finite-difference test failed at its first step size; reducing the step shows quadratic convergence to3.03e-8 relative error. Both the original failure and refinement are retained.

| Requirement | Current outcome |
|---|---|
| Bound cores | No certified object; inadequate late physical resolution |
| Selected core masses/population | Not established |
| Primordial field conditions | Low-excitation prescription derived; physical initial state unresolved |
| Dwarf fits and rotation curves | No assembled population to test; not certified preserved |
| Cluster distribution/lensing | No derived population or profile |
| Cosmological growth | No new large-scale pass; preceding action benchmark retained95.2–96.2% at k1/Mpc, below its99% target |

The previous growth numbers remain diagnostics of their stated initial conditions, not observational exclusions. The present small-box simulations do not replace that large-scale test. No data refit or full relativistic cosmology was performed.

## Next discriminator

Proceed with refinement that keeps physical core scales resolved, coupled to a physically specified initial field/metric history, before interpreting a mass spectrum. Adaptive refinement must preserve the same variational deposition/force relations and expansion-work accounting across levels. A fixed-grid density peak or chosen compact seed cannot substitute for this test. The full problem remains open; the current artifact provides a tested3D starting point and explicit failed interpretation gates.
