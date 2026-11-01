# Independent review of the kinetic quadrupole discretization

Reviewer: `/root/core_gap_check`, 2026-11-01. Scope: the definitions and
implementation read in `response.py`, `orbits.py`, and `background.py`,
compared with `THEORY.md`. No numerical computation was run for this review.
Execution manifests must identify the exact implementation revision used.

**Analytic verdict:** the action-shell measure, orientation factor, scalar
and current operators, real-quadrupole energy/work normalization, and angular
momentum normalization are consistent with the declared fast-scalar kinetic
model. No missing driven `l=2` parity sector was found. This verdict is
conditional on numerical orbit, Gram, resolution and work-ledger checks;
it is not evidence that those checks have passed.

One concrete interface fault was found and reported immediately: the read
version of `response.py` requested orbit diagnostic keys `rp`, `ra`,
`energy_error`, `period_relative_error`, and `advance_relative_error`, whereas
the read `orbits.py` supplied `r_pericenter`, `r_apocenter`,
`invariant_residual`, `dense_period_relative_error`, and
`dense_angle_relative_error`. A mapping or consistent provider aliases are
required before execution. This is not a physical ambiguity.

## 1. Canonical action-shell measure

The dimensionless background Hamiltonian is
`h_0=A(r)p^2/2-psi(r)`, with the occupied energy surface at zero and
`A=exp(-2s)`. Its density level is
`f_*=3/[4pi 2^(3/2)]`. In canonical spherical actions use radial action
`J_r`, total angular momentum `L`, and signed component `L_z`.
The phase-space volume is

```text
d^3x d^3p = dJ_r dL dL_z d^3theta,
partial h_0/partial J_r = Omega_r,
-L <= L_z <= L.
```

Integrating the energy delta function over `J_r`, the angles over their
periods, and `L_z` over its allowed range gives

```text
dmu_shell(L) = (2pi)^3 f_* [2L/Omega_r(L)] dL.
```

This is the implementation's `mw` before orientation reduction. It is not
an arbitrary orbit weighting. An independent local momentum integration
gives

```text
S(r) = integral f_* delta(h_0) d^3p = (3/2)n(r)/psi(r),
integral dmu_shell = 4pi integral_0^R r^2 S(r) dr.
```

The code's shell-measure comparison therefore has the correct `4pi` and
frequency factors. The exactly radial and circular endpoints have zero
measure under the continuous `L` integral, but near-endpoint behavior still
requires quadrature refinement.

The orbit variables use
`phi=theta_phi+dphi(theta_r)`. Consequently a degree-`k` planar angular
factor has Fourier frequencies `nu=n Omega_r+k Omega_phi`. The periodic
factor to Fourier transform is `exp[i k dphi(theta_r)]`, not the full
precessing physical azimuth. The read implementation uses the former.

## 2. Orientation factor and planar harmonics

For a laboratory harmonic `Y_2m`, rotate each orbit to its own equatorial
plane. The rotated harmonic is a linear combination of the five planar
components, with unitary rotation coefficients. Uniform orbit-plane and
in-plane orientations give

```text
average_orientation D_(m,k)* D_(m,k') = delta_(k,k')/5.
```

This follows from rotational invariance: the average matrix is proportional
to the identity on the five-dimensional harmonic space, and its trace is
one by unitarity. It is independent of laboratory `m`; thus the same response
normalization applies to `Y_20` and `Y_22` on an isotropic spherical state.

On the equatorial orbit plane,

```text
Y_20(pi/2,phi)  = -sqrt[5/(16pi)],
Y_2,+2(pi/2,phi)= sqrt[15/(32pi)] exp(2i phi),
Y_2,-2(pi/2,phi)= sqrt[15/(32pi)] exp(-2i phi),
Y_2,+1(pi/2,phi)=Y_2,-1(pi/2,phi)=0.
```

The code's square-root weight `sqrt(mw/5)` and these three amplitudes are
therefore correct. A useful exact consistency check is

```text
( |Y_20|^2+|Y_22|^2+|Y_2,-2|^2 )/5 = 1/(4pi).
```

Combined with the action-shell measure, this gives the local scalar Gram
matrix `integral r^2 S(r)u_i(r)u_j(r) dr` for harmonics normalized by
`integral |Y_2m|^2 dOmega=1`. There is no additional factor of five, two,
or `4pi` to insert into the response matrices.

## 3. Current components and parity

The even-parity vector basis is

```text
W = W_r(r)Y_2m e_r + W_t(r)grad_Omega Y_2m.
```

Its contraction with momentum along the equatorial orbit is

```text
p.W = [p_r W_r+i k p_phi W_t]Y_2k.
```

This is exactly the implementation's current feature. Both radial and
poloidal tangential currents are retained. The angular norm is

```text
integral W_i*.W_j dOmega = W_ri* W_rj+6 W_ti* W_tj,
```

because the angular-gradient norm is `l(l+1)=6` at `l=2`. This establishes
the factor six in both the current stiffness and direct current Gram checks.

There is a separate toroidal current basis
`W_o e_r cross grad_Omega Y_2m`. Its momentum contraction has opposite
phase-space parity from scalar/poloidal `l=2` forcing. In the orbital plane
it occupies the complementary odd planar `k=+/-1` sector: the relevant
polar derivatives can be nonzero even where the scalar harmonic vanishes.
The spherical background and reciprocal current kernel preserve parity, so
that sector is not driven by the stated scalar quadrupole from zero initial
perturbation. Excluding it is consistent with this forced calculation;
it would not be consistent with a claim to have tested every nonradial
kinetic perturbation or arbitrary axial forcing.

The leading current radial functions in the code have ratio
`W_r:W_t=2:1` and scale as `r`. They represent the regular gradient of
`r^2Y_2m`. The independent higher radial and tangential functions start at
`r^3`, retaining regularity while enlarging the polar current space.

For `gamma=(1-A)/n`, the positive current kernel is represented variationally
through

```text
C_ij = integral r^2 gamma^(-1)(W_ri W_rj+6W_ti W_tj) dr.
```

The implementation uses `gamma^(-1)=n/[-expm1(-2s)]`, the correct stable
evaluation on this positive-scalar background. The local shell momentum
moment is `(n/A)delta_ij`, yielding the direct current Gram matrix used in
the implementation. Scalar-current direct cross-Grams vanish by oddness
in momentum. These are useful tests of the current vertex and phase weights.

## 4. Gravity and scalar stiffness, including their tails

For radial field basis functions `u_i=(r/R)^2 P_i(2(r/R)^2-1)`, each
`u_i(R)=1`. The gravity matrix is

```text
G_ij = integral_0^R [r^2 u_i' u_j'+6u_i u_j] dr +3R.
```

The constant matrix term is the exact exterior energy of the decaying
quadrupole `r^(-3)`. Poisson therefore contributes the negative feedback
`-B_g^dagger G^(-1)B_g`.

In `rho_* h_*` energy units the scalar coefficients are

```text
kappa_s=(6/5)epsilon,
c(r)=(18/5)exp(3s)+(12/5)npsi,
A_s=-kappa_s Delta_2+c,
source=2psi n_1.
```

The read code's `1.2epsilon`, `3.6exp(3s)+2.4npsi`, and `2psi u_i`
source features match these expressions. Scalar feedback is negative:
`-B_s^dagger A_s^(-1)B_s`.

The scalar exterior has `n=0` but retains the nonzero background tail.
For its decaying radial solution let `y=S'/S`. The equation is

```text
y' = 6/r^2+3exp(3s_0(r))/epsilon-2y/r-y^2.
```

At the remote outer boundary `L`, the constant-vacuum decaying `k_2`
solution supplies `y(L)=-b_2(L)`, with `b_2` from `THEORY.md`.
Integrating this Riccati equation backward to `R` incorporates the scalar
background tail between `R` and `L`. Its boundary stiffness at the matter
edge is

```text
tail_stiffness = -kappa_s R^2 y(R).
```

This is positive for the decaying solution and is added to every scalar
matrix entry because `u_i(R)=1`. The code's Riccati sign and coefficient
are correct. Its only exterior approximation is the remote constant-vacuum
condition at `L`; its insignificance still needs domain/tail checks.

## 5. Feature conjugation and the finite Hamiltonian

Let `a_i,nu` be the orbit Fourier coefficient of a test feature. The moment
map is `B_i,nu=sqrt(weight) a_i,nu*`, while an external feature's source
column is `b_nu=sqrt(weight) a_ext,nu`. The code's conjugation choices
implement this distinction. In particular, the core-restricted feature is
returned as a source column and later used as an adjoint observable; its
different apparent conjugation from the moment rows is consistent.

After solving the positive field/current Gram matrices, the kernel is

```text
H=I-V_g^dagger V_g-V_s^dagger V_s+V_j^dagger V_j.
```

The low-rank construction of `H^(1/2)` is consistent with this expression
when `H` is positive and the discarded Gram eigenvalues are numerically
negligible. Its cutoff and positive minimum must be treated as numerical
claims requiring refinement. An indefinite `H` is outside this square-root
solver's execution path; it is not a physical proof of kinetic growth.

With `x=H^(1/2)z`, the homogeneous generator becomes
`H^(1/2)Omega H^(1/2)`, a Hermitian matrix. The transformed source is
`H^(1/2)Omega b`, as implemented. The observable is
`b^dagger H^(-1/2)x`. The Lanczos projection preserves its projected
Hermitian dynamics, but agreement with the full finite system still requires
Krylov/residual checks. The physical work and angular-momentum ledgers are
additional checks rather than consequences that may be assumed in advance.

## 6. Real rotating quadrupole: factors of two and four

The physical laboratory perturbation is
`Re[F(t)U(r)Y_22(theta,phi)]`, with standard complex `Y_22` normalization.
Only one complex `m=2` sector is explicitly stored; its conjugate represents
the real physical field. Angular integration of a squared real field gives
one half the corresponding complex norm. Consequently

```text
E_2 = (1/4) z^dagger H z = (1/4)||H^(1/2)z||^2,
q_ext = b^dagger z,
P_ext = (1/2)Re[q_ext* F_dot],
T_z = (m/2)Im[q_ext* F],        m=2.
```

These agree with the code's `.25` energy, `.5` work, and unit torque factor.
The interaction energy is `(1/2)Re[q_ext*F]`; it vanishes at both ends of
the sine-squared pulse. Therefore integrated external work equals final
quadratic energy if the finite equation is solved accurately.

On the active, nonzero-frequency subspace the canonical second-order angular
momentum is

```text
L_z,2 = (m/4) sum_nu |z_nu|^2/nu.
```

The denominator is signed. This is the rotation generator of the linear
phase-space perturbation: under the Poisson operator `-iOmega`, this
quadratic functional generates `z_dot=-imz`. Differentiating it using
`z_dot=-iOmega(H z+bF)` gives precisely
`L_z,2_dot=(m/2)Im[(b^dagger z)*F]`, because `z^dagger H z` is real.
The implementation's `.5 sum |z|^2/nu` is therefore correct at `m=2`.
It is not the first-order spatial integral of `x cross j_1`, which vanishes
for a pure quadrupole. Zero-frequency orbit amplitudes must remain frozen
and cannot be divided by `nu`.

For a fixed rotating pattern speed `Omega_p`, write
`F=A(t)exp(-im Omega_p t)`. Then

```text
P_ext = Omega_p T_z + (1/2)Re[q_ext* A_dot exp(-im Omega_p t)].
```

The code's separate envelope-work term makes this identity explicit. It is
an independent accounting check on sign and pattern-frequency conventions.

## 7. Local work, interpretation and remaining numerical obligations

The observable restricted by `r<core_radius` gives work supplied by the
external source at positions in that original-material-core region. It is
not the energy retained there: kinetic transport and gravitational/scalar
energy exchange cross that boundary. Its ratio to total work can therefore
be negative or exceed one without violating conservation. It must not be
called a retained heat fraction, a heating efficiency, or a measured change
of core binding energy.

Likewise, decay of a coherent quadrupole after the pulse can indicate phase
mixing within the resolved orbit distribution, but a finite conservative
system has recurrences. No irreversible thermalization or scalar radiation
is represented by this fast-scalar calculation.

Numerical obligations remain: correct provider interfaces; orbit invariants
and near-endpoint quadrature; action/local shell-measure agreement; scalar
and current feature Gram agreement including cross blocks; harmonic and
radial-basis refinement; weighted Hermiticity and treatment of discarded
small Gram eigenvalues; Krylov convergence; both work-energy and
torque-angular-momentum ledgers; and the remote scalar-tail approximation.
The omitted axial parity sector is outside the specified forcing problem,
not a missing component of its driven polar response.
