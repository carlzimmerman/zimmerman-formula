# PF08: full coupled formation, avoidance, singular selection

Base d7aba1da7f; original scientific target unchanged. No arbitrary global
attempt quota; individual numerical jobs bounded at120s with preserved restarts.

R1 numerical formation/avoidance: replace dense constraint matrices with the
same Jacobian applied through FFT derivatives and preconditioned GMRES. Verify
Jacobian-vector finite differences, dense-versus-FFT constraints/RHS on smooth
states, homogeneous benchmark, and endpoint agreement at n31/127. No change
to the action, initial family, momentum reconstruction, padding or physical
admissibility. Then refine n255,511,1023,2047,4095 only as needed to resolve
late evolution. Evaluation grids2n+1, with selected larger-padding controls.
Timestep scales inversely with n and is halved for temporal comparisons.
Preserve strict raw momentum1e-7, reconstructed momentum, domain and multifield
tail1e-3 stops. Do not call any numerical stop physical breakdown. For an actual
formation inference require converging prebreak fields and gradients plus
controlled event localization, or a separate full-action theorem.

R2 structural formation: derive genuine nonlinearity from the exact auxiliary
principal system, with A held fixed in state derivatives. Then attack the
nonlocal finite-K/polarization and metric transfer, explicitly bounding the
terms needed by a Riccati/characteristic comparison. A frozen or decoupled
simple wave remains partial progress unless that transfer is supplied.

R3 singular selection: distinguish a selected native limit from two different
regularized theories, undefined weak products or freely assigned surface data.
A uniqueness/nonuniqueness claim must identify a fixed admissible solution
class and the same incoming native data. Search the auxiliary structure for an
intrinsic selection rule; restricted no-layer results remain dependencies.
No viscosity, surface stress, or additional state is adopted by default.

Numerical fixture remains the dimensionless PF07 constant-V case. It is not
an astrophysical-footing prediction. Tests of alternate scales require a new
recorded range. Success/failure of a finite computation is not a universal
classification of every solution to the action.
