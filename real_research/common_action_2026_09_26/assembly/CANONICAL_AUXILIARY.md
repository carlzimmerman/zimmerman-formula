# A nonperturbative canonical auxiliary result for the common action

This result uses the actual projected exponential carrier in CA4-GNC/CA4-PN.
It is not the separate canonical-z control in REPORT.md. The evolution lane
independently audited its Legendre transform, direct-method proof and scope.

Fix a smooth compact connected three-dimensional leaf without boundary,
its smooth metric h, and a smooth lapse with 0<N_min<=N<=N_max<infinity.
Let cN=1-alpha/2>0, M^2>0, U in H1, and a=D ln N in L2. Fix the carrier's
canonical coordinates and momenta, with

    epsilon0 = sum[Pi_A^2/(2h)] + Wd >= 0, epsilon0 in L1.

Here Pi_A is a spatial density, h is the determinant of the metric, and
Wd=sum|D phi_A|^2/2+V(phi). Finite-energy Cartesian carrier data have this
property for the nonnegative polynomial potentials studied in the transport
lane. Keep all these data fixed while solving for Z; this is one constraint
step, not time evolution of the data.

## Legendre transform before testing the auxiliary

For Ld=exp(z) Kd-exp(-z) Wd, the canonical momentum is
Pi_A=sqrt(h) exp(z) n(phi_A). Its Hamiltonian, apart from the shift term
Pi_A beta^i D_i phi_A which is independent of Z, is

    Hd = N sqrt(h) exp(-z) epsilon0,
    z=Z-<Z>_h.

The spatial gravity terms obey the exact square completion

    alpha|a-DZ|^2+4a.DZ-2|DZ|^2-4cN DZ.DU
      = alpha|a|^2-2cN|DZ-(a-DU)|^2+2cN|a-DU|^2.

The gate and its compensator do not contain Z. Hence, up to terms independent
of Z, the full common action's canonical Hamiltonian is

    H_Z[Z] = integral N dvol_h {
       M^2 cN |DZ-(a-DU)|^2 + exp(-P_h Z) epsilon0 },
    P_h Z=Z-<Z>_h.

This is a positive, strongly convex functional modulo the constant shift.
For bounded smooth variations v its exact second variation is

    2 M^2 cN integral N |Dv|^2
       + integral N exp(-P_h Z) epsilon0 (P_h v)^2.

The second term is nonnegative. The first term is strictly positive for a
nonzero mean-zero v. A putative singularity in a calculation that holds
carrier velocities fixed is therefore not a proof of nonuniqueness of this
canonical constraint. Its independent inputs are momenta, not velocities.

## Existence and uniqueness, including finite-energy data

Work in the mean-zero subspace of H1 and define the functional to be positive
infinity where its exponential integral diverges. It is proper: Z=0 has
finite energy under the stated hypotheses. Write b=a-DU. The pointwise bound

    |DZ-b|^2 >= |DZ|^2/2-|b|^2

and Poincare's inequality bound every minimizing sequence in H1. A subsequence
converges weakly in H1, strongly in L2 and almost everywhere by compactness of
the leaf. The gradient part is weakly lower semicontinuous. Fatou's lemma
applies to the nonnegative exponential term with fixed measurable epsilon0.
The limit therefore attains the minimum and remains mean zero. Strict
convexity of the gradient norm on that subspace gives uniqueness.

The Euler equation exists against bounded smooth tests: multiplying the
integrable exponential term by exp(-t P_h v) is uniformly dominated for
bounded t and v. It is precisely the projected common-action equation

    2 M^2 cN div_N(DZ-a+DU)
      +rho_d-<N rho_d>_h/N=0,
    rho_d=exp(-z) epsilon0.

This proves a unique variational Z constraint solution at fixed canonical
data. It does not assume that the pointwise Hessian is bounded.

## What the result does and does not settle

For fixed epsilon0, geometry and lapse, changing b gives a controlled inverse.
Strong monotonicity and the linear forcing imply

    ||D(Z1-Z2)||_N <= ||b1-b2||_N.

This can be derived from the two minimization inequalities, so it does not
require testing an L1 source against an arbitrary unbounded H1 function.
It controls the auxiliary's dependence on b; it is not a Lipschitz theorem
for arbitrary changes in the carrier energy density. In three dimensions
L1 does not embed in H^{-1}, and no such implication is made.

H1 existence alone supplies neither pointwise bounds on z nor smooth
coefficients for the wave equation. A full coupled continuation theorem
still needs additional regularity, positive bounded lapse, controlled spatial
geometry and foliation, and simultaneous preservation of the U and metric
constraints. Eliminating a convex auxiliary can also subtract a Schur term
from the reduced momentum Hessian; the positivity above is not, by itself,
a proof of the whole reduced Hamiltonian's kinetic positivity.

The explicit Legendre identity, square completion, elementary coercivity and
Hessian lower/strict bounds are certified by five declarations in
CanonicalAuxiliary20260926.lean. The functional-analytic existence argument,
its compactness inputs and the global gravity problem are not formalized by
those five algebraic statements.
