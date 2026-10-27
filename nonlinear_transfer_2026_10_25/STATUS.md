# NT checkpoint: actual nonlinear transfer, preservation, incomplete formation

Full freely evolving density, complex T/F fields, independent carrier momentum
and reciprocal scalar waves were implemented. The strongest verified runs use
the exact physical response, stable evaluation of the unchanged energy, a
force-finished benchmark, and an absorber outside all material cells.

This phase establishes a nonlinear transfer channel and local preservation
tests. It does NOT establish formation from a free all-F reservoir, or full
relaxation after infall. No real-galaxy data fit or population claim is made.

## New mathematical and numerical pieces

* ACTION_CANONICAL.md derives the gauge-transformed positive Hamiltonian,
  actual conversion source, all density forces, finite carrier momentum and
  the energy/shift-charge identities.
* The density-dependent carrier inertia adds a material force that is retained
  explicitly. Its independent derivative and scalar-source sign are audited.
* A stable series evaluates the same W=-log(1-u)-u at small u. On actual outer
  nodes, 80-digit comparison gives 2.18e-16 relative error, versus 1.17e-5 for
  direct subtraction. This resolves an energy-noise floor and improves static
  preparation. Positive-form kinetic/alignment energies remove other avoidable
  cancellations. No new physics is fitted by these changes.
* The exact complex-edge benchmark is Newton force-finished: density KKT
  3.07e-7, projected gradient 5.71e-10. The active radial constrained Hessian
  is positive, and the independently relaxed boundary force is

      F_R=-k delta_R, k=0.00041127513 Eunit/kpc².

  Density and both real phase fields relax in this stiffness. It is conditional
  on the stated active radial space, not a global formation theorem.

## Joint nonlinear tests

The physical_boundary_plus/minus runs perturb the material boundary by
approximately +/-0.5 kpc, then release all dynamic fields. Both complete
100 Myr with no imposed radius or density curve. Final results:

| Initial displacement | Boundary (kpc) | Law error | Density rebound | Outer T fraction |
|---|---:|---:|---:|---:|
| +0.5 kpc | 56.4972 | 0.70796% | 1.0000 | 1.03e-7 |
| -0.5 kpc | 56.6945 | 0.70493% | 1.00481 | 5.24e-8 |

The reference radius is about 56.3437 kpc. Both initially return toward it;
their nonlinear oscillations and final offsets are reported rather than
called complete settling. Escaped energies are 1.29479e-4 and 3.01573e-4
Eunit. Maximum total energy errors are 9.44e-9 and 5.05e-8 Eunit. These tests
support finite restoring response and preservation for these disturbances;
they do not establish an arbitrary-size basin or formation from all F.

For a true material infall test, independently dilate initial radii in the
core by 20%, leaving the distant reservoir fixed, then evolve all variables.
The density is never constrained to follow that dilation afterward.
physical_infall and flux_infall complete 30 Myr. Halving dt and changing the
wave spacing/domain give:

| Test | Work into field | Net energy through 500 kpc | Law error | Density rebound |
|---|---:|---:|---:|---:|
| dt=.005 Myr | 3.2888455e-4 | 3.1295362e-4 | 17.3293242% | 1.9711311 |
| dt=.0025 Myr | 3.2887066e-4 | 3.1293756e-4 | 17.3293244% | 1.9711313 |
| wave h=1 kpc, domain=12 Mpc | 3.2888301e-4 | 3.1294928e-4 | 17.3293243% | 1.9711348 |

Energies are Eunit. The far-flux ledger closes below 1.83e-17 Eunit. The fine
time run has total energy error 2.09e-7 Eunit, less than 0.07% of far flux.
The zero-coupling control emits zero scalar energy and has nearly the same
law residual and trough. Thus nonlinear transfer is real in the implemented
model, but is insufficient to restore this disturbed galaxy within the tested
window. A 30 Myr window is not a proof of failure at every later time.

Far-zone flux is distinguished from near-field storage and absorber energy.
Absorbers at different radii record different arrival times; the comparison
uses the same 500-kpc sphere, not uncorrected sponge losses.

## Formation and long-time limits

All-F seeds undergo conversion and generate waves, but the tested full runs
produce small, multiply crossed converted structures rather than the final
law. Finite-carrier long-time integration encounters unresolved fast motion;
partial runs remain labelled partial or numerical failures. The independent
zero-carrier-inertia comparison reaches the physical cap at about 69.89 Myr
for the dilated data, with law error 17.16% and density rebound 3.80. It is
not a finite-carrier solution or a universal no-go.

Early split-step adiabatic pilots, noisy tail-energy runs, an insufficient
absorber, and an inherited line-search continuation were isolated as
development evidence. They are not merged with the physical verification
rows above. CONTRACT_ERRATUM.md records an inherited conventions sentence.
All original scripts/contracts/results remain immutable.

The exact gap in the present operator is unchanged: if div(j_T)=0 it supplies
no direct bulk source. Gravity can feed the conversion channel indirectly
through relative currents, carrier motion and stresses, but the actual tested
transfer is weak. The next candidate is a higher-order density-weighted T
current; see compression_current_2026_10_25/TARGET.md. This is an explicitly
changed dynamical interaction, not a derived consequence of the formula.
