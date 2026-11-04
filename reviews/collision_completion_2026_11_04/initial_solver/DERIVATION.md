# Positive log-number solve with an absolute rare-cell residual budget

This route changes the nonlinear solver, not the physical collision operator.
It acts on the frozen fast exact-angular 25-group physical-number backend and
the frozen explicit-availability `QuantumState` interface. All numerical
experiments use the actual fresh checkpoint N=.0002999746374639217, its
actual eight orbital phase nodes, and the consistent common mass background.
The inherited scalar/action state and phase background stay fixed during
these collision controls.

## Variables and Jacobian

Write Y_i=nu_i f_i for the physical comoving number. The existing mixed state
stores Z_i=Y_i for a number coordinate, or Z_i=nu_i-Y_i for a fermion hole.
Let s_i=+1 or -1 respectively. The backend supplies C=dY/dtau and its
physical-number Jacobian JY=dC/dY. Thus

    R(Z)=Z-Zold-dtau diag(s) C(Y),
    JZ=d(diag(s) C)/dZ=diag(s) JY diag(s).

For positive Z, use u=log Z. The Newton derivative is

    dR/du=(I-dtau JZ) diag(Z).

`log_number.py` solves the row-scaled system

    diag(1/scale) (I-dtau JZ) diag(Z) delta_u = -R/scale.

Trials are Z_trial=Z exp(alpha delta_u), with a bound on the log correction
and a merit line search. This keeps number and hole coordinates positive
without allowing a nearly empty number coordinate to force a tiny global
positivity step. Fermion coordinate upper bounds are checked before a trial
is evaluated. Coordinate switches above Z/nu=.65 also transform the old
state, preserving the same residual equation. Accepted states are never
clipped. The route requires positive initial represented coordinates; the
declared fresh checkpoint has the previously quantified tiny positive seed.
It is not a solver certificate for an exactly zero, nondifferentiable
fractional-projection boundary.

For nearly empty number coordinates the first Newton guess includes their
positive explicit gain, bounded at .6 nu for fermions. This predictor is
only a guess: it is not accepted as a physical reaction step. A converged
accepted state must satisfy the same conservative backward-Euler residual.

## Error scales and physical interpretation

Number coordinates receive a common absolute merit floor b=1e-14, while
explicit hole coordinates retain their relative scaling. With tol=2e-8,

    scale_i=1e-30 nu_i + b 1_number + max(|Zold_i|,|Z_i|)
            +32 eps dtau gross_i/tol.

Here gross is the nonnegative integrated forward-plus-reverse absolute
reaction measure. The pure floor contribution to the aggregate residual
allowance on the 1000 tested coordinates is tol b 1000=2e-19 numbers.
This is a nonlinear residual budget, not a proof of global trajectory error
or an added physical particle source. Bulk coordinate subtraction and sparse
solves still have a floating-point floor. The actually measured full number
balance L1 reaches 5.55e-16, reported separately rather than hidden by the
small rare-cell budget or called 1e-18 accuracy.

At xi=.02 and visible g*s=106.75, the yield conversion is

    Y_number = number_comoving * 45 xi^3/(2 pi^2 g*s).

The pure floor budget corresponds to about 3.42e-26 yield. The largest
measured full number balance corresponds to 9.47e-23 yield. Both are far below
the 5e-16 comparison gate, whereas collision-time discretization is tested
separately and is much larger. Neither conversion proves that early time
discretization errors contract below the late relic gate.

## Finite results

`run_log001` solves a single dN=5e-5 collision step in six Newton iterations
and 7.97 child seconds. The existing absolute-floor solver took 19 iterations
and roughly 22 seconds. The recorded aggregate charged number and entropy
agree at displayed precision; the baseline did not persist its complete Y
vector, so no bitwise full-vector equality is claimed from that record.
Two half steps require five plus five iterations. All positivity, Pauli,
entropy, local energy, physical balance and rare-budget checks pass.

`run_log002` compares four quarter steps with eight eighth steps over the
same total dN=5e-5. Each step takes three to five iterations. Refinement changes
the charged number by -7.62e-5, U1 number by -.23161%, and U1 mean momentum
by -1.46e-6, all relative. The whole-number L1 difference is 1.295e-4.
The finest U1 yield is 1.26699766e-10. Bounds and increasing entropy hold;
the local collision-energy relative residual remains below 1.70e-17.

The backend's pointwise energy identity is checked independently of the
Newton merit floor. The orbit-averaged particle energy can exchange energy
with the scalar through action covariance, so it is not declared collision
invariant. No scalar/action evolution, Hubble history, continuum limit or
cosmological candidate success follows from these fixed-operator controls.
