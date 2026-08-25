# QWEN FINAL CLOSURE ATTACK

You are not being asked for a plausibility argument. You are being asked to either construct or falsify a fully specified Hamiltonian minimally modified gravity model whose physical gravitational sector has exactly two local propagating tensor degrees of freedom and whose static weak-field lapse equation is exactly the MOND modified Poisson equation with

mu(y) = 1 - exp(-y).

This is the final attack. Do not declare success unless every algebraic gate below is explicitly checked.

## Literature constraints

Use these as structural references, not as permission to copy an unverified result:

1. Yao, Oliosi, Gao, Mukohyama, "Minimally modified gravity with auxiliary constraints formalism", Phys. Rev. D 107, 104052 (2023), arXiv:2302.02090.
2. Sangtawee, De Felice, Karwan, "Minimally modified gravity with Laplacian auxiliary constraints and an inflationary realization", arXiv:2607.26031 (submitted 28 July 2026).
3. Yao, Oliosi, Gao, Mukohyama, "Minimally modified gravity with an auxiliary constraint: a Hamiltonian construction", Phys. Rev. D 103, 024032 (2021).

The 2023 four-auxiliary-constraint construction uses a total Hamiltonian of the form

H_T = integral d^3x [ H_scr + mu_I S^I + N^i H_i + lambda^i pi_i ],

with spatial-diffeomorphism constraints and four scalar second-class auxiliary constraints. The 2026 Laplacian version replaces direct multiplier coupling by (D^2 mu_I)(Q^I-P^I), so inhomogeneous constraints survive while homogeneous multiplier zero modes drop out.

## Target theory architecture

Use ADM variables

N, N^i, gamma_ij, pi_N, pi_i, pi^ij.

Let

q := (1/6) ln det(gamma_ij)

be the local volume/conformal scalar and let

p := pi / sqrt(gamma),   pi := gamma_ij pi^ij

be its canonical momentum density up to an irrelevant fixed normalization. Track the exact Poisson-bracket normalization rather than hiding it.

Keep the six first-class spatial-diffeomorphism constraints (pi_i, H_i).

Use four scalar auxiliary constraints:

S_4 := pi_N ≈ 0,

S_1 := C_M ≈ 0,

S_2 := Delta q ≈ 0,

S_3 := Delta p ≈ 0,

where Delta := D_i D^i and C_M is the nonlinear MOND elliptic constraint

C_M := D_i [ c^2 mu(y) D^i ln N ] - 4 pi G rho_m,

y := (c^2/a_0) sqrt(D_i ln N D^i ln N),

mu(y) := 1 - exp(-y).

For vacuum rho_m=0. For matter, define rho_m as the normal-frame matter energy density in the same ADM split and do not silently assume a 4D Hamiltonian constraint survives.

The canonical Hamiltonian density should be taken to be the GR tensor Hamiltonian plus matter,

H_can = H_GR[N,N^i,gamma,pi] + H_matter[N,N^i,gamma,matter],

but the lapse is NOT treated as a first-class refoliation multiplier. The total phase-space Hamiltonian is

H_T = H_can + int d^3x [ lambda_N S_4 + mu_1 S_1 + mu_2 S_2 + mu_3 S_3 + lambda^i pi_i + N^i H_i ].

The purpose of S_1 is to replace the scalar/lapse constraint sector by the MOND elliptic equation, while S_2 and S_3 eliminate the remaining inhomogeneous scalar metric pair. The Laplacian leaves homogeneous modes available for cosmological background dynamics.

## Required calculations

### Gate 1: Constitutive primitive

Derive a local spatial constitutive density whose lapse variation gives C_M in the weak-field quasistatic limit.

Starting from

y = c^2 |D ln N| / a_0,

show that the primitive can be chosen as

G(y) = y^2 + 2(1+y)e^{-y} - 2,

so that

G'(y)/(2y) = 1 - e^{-y}.

Check every factor of c and a_0.

### Gate 2: Newtonian limit

Set

N = 1 + Psi/c^2 + O(Psi^2/c^4),

D_i ln N = D_i Psi/c^2 + O(Psi^2),

y = |grad Psi|/a_0 + O(Psi/c^2).

Derive explicitly

C_M = 0

=>

D_i[ (1-e^{-|grad Psi|/a_0}) D^i Psi ] = 4 pi G rho_b

with no missing sign or factor.

### Gate 3: Exact four-constraint Dirac matrix

Define

Phi_A = (S_4,S_1,S_2,S_3).

Compute

Delta_AB(x,y) = {Phi_A(x),Phi_B(y)}

including differential operators and smearing by test functions.

You must show the structure

Delta ~
[[0, L_N, 0, 0],
 [-L_N^T, *, *, *],
 [0, *, 0, K],
 [0, *, -K^T, *]],

where

L_N := delta C_M / delta N

is the Frechet derivative of the MOND elliptic operator and

K := {Delta q, Delta p}.

Do NOT replace differential operators by numbers without stating the boundary conditions.

### Gate 4: Ellipticity / rank

Linearize C_M under N -> N + delta N.

With u_i := D_i ln N and y = c^2 |u|/a_0, derive the principal symbol

sigma(L_N)(k) = - c^2 k_i A^i_j k^j / N + lower-order terms,

with

A^i_j = mu(y) delta^i_j + y mu'(y) uhat^i uhat_j.

For mu(y)=1-e^{-y}, prove

mu(y)>0,

mu(y)+y mu'(y)>0

for every y>0.

State clearly that the operator is generically elliptic for nonzero acceleration, while the exact zero-acceleration point is a degenerate branch that needs separate treatment.

### Gate 5: Laplacian scalar pair

Compute the Poisson bracket of

S_2 = Delta q,
S_3 = Delta p.

For a nonzero spatial Fourier mode show

{S_2(k), S_3(-k)} = C_q k^4

with the exact normalization C_q determined from your definition of q and p.

Show this is nonzero for k != 0.

### Gate 6: Full rank

Use the Pfaffian/determinant of the 4x4 antisymmetric Dirac matrix.

Show that, on the generic branch,

det Delta = [L_N K]^2

up to the exact transpose/sign/operator ordering.

Therefore the four scalar auxiliary constraints are second class for k != 0 whenever L_N is elliptic/invertible and K is invertible.

Do not claim a global rank theorem if there are zero modes or degenerate-gradient points. State the exact domain.

### Gate 7: DOF count

Start from the full ADM phase space including lapse/shift.

Explicitly count:

- six first-class spatial-diffeomorphism constraints (pi_i, H_i), removing 12 phase-space dimensions;
- four independent second-class scalar auxiliary constraints, removing 4 phase-space dimensions.

Demonstrate that the remaining gravitational phase space has 4 dimensions per spatial point, i.e.

N_DOF = 2.

Explain why S_2 and S_3 eliminate the inhomogeneous scalar pair while the tensor TT pair is untouched.

### Gate 8: Constraint preservation

Compute

dot S_A = {S_A,H_T}.

Show that, because the 4x4 Dirac matrix is invertible on the generic nonzero-k branch, preservation of S_A determines the four multipliers (lambda_N,mu_1,mu_2,mu_3) rather than generating additional constraints.

This step is mandatory. A primary second-class rank calculation without consistency is not enough.

### Gate 9: Tensor sector

Expand the Hamiltonian around Minkowski or the chosen homogeneous background in TT variables.

Verify that the scalar constraints do not constrain h_ij^TT or pi_TT^ij.

Compute the quadratic tensor action/dispersion relation.

Require

Q_T > 0,

c_T^2 > 0,

and, if possible, c_T^2 = 1.

If c_T != 1 for the candidate Hamiltonian, record it as an additional phenomenological defect rather than hiding it.

### Gate 10: Matter coupling

Do not assume the matter equations remain standard just because the constraints are second class.

Derive the coupled matter equations and verify spatial-diffeomorphism covariance and consistency of the modified scalar constraint with the matter continuity equation.

If the simple choice C_M uses rho_m but the full Hamiltonian coupling is inconsistent, modify C_M or H_can and show the repair explicitly.

### Gate 11: Action/Lagrangian reconstruction

Attempt a Legendre transform back to a phase-space/Lagrangian formulation.

If a local Lagrangian exists, write it explicitly.

If only a Hamiltonian definition is clean, state that the final theory is a Hamiltonian MMG theory and do NOT falsely advertise it as a manifestly 4D generally covariant local action.

### Gate 12: Falsification

The following failures are automatic rejection:

1. an extra scalar pole;
2. a vanishing Dirac determinant on the generic branch;
3. a hidden tertiary constraint changing the count;
4. ghost/gradient instability in the tensor sector;
5. failure to reproduce the MOND modified Poisson equation;
6. matter-inconsistency;
7. unexplained dependence on an arbitrary homogeneous multiplier;
8. claiming global closure despite degenerate zero modes.

## Required symbolic tools

Use SymPy for exact algebra.
Use Fourier-space symbolic matrices for the linearized constraint algebra.
Use functional-derivative notation for field operators, with explicit integration by parts and boundary assumptions.
Create runnable scripts in a scripts/ directory.
Every claimed identity must have a symbolic check.

## Required final output

Produce:

1. FINAL_STATUS.md
2. CLOSURE_CANDIDATE.md
3. scripts/01_constitutive.py
4. scripts/02_newtonian_limit.py
5. scripts/03_dirac_matrix.py
6. scripts/04_rank_and_ellipticity.py
7. scripts/05_dof_count.py
8. scripts/06_constraint_preservation.py
9. scripts/07_tensor_sector.py
10. scripts/08_matter_consistency.py
11. scripts/09_legendre_check.py
12. run_all.sh

FINAL_STATUS.md must begin with exactly one of:

CLOSED
CONDITIONALLY_CLOSED
FAILED

and must explain why.

Do not use the phrase "two DOF" unless the Dirac count, rank condition, and preservation equations have all been explicitly checked.
Do not call a Hamiltonian construction 4D covariant unless that has actually been proven.
Do not use the previous retarded Phi/adjoint localization as a hidden dynamical field.
Do not replace an unresolved equation with a placeholder.
If the construction fails, produce the explicit no-go algebra and identify the minimal modification needed.
