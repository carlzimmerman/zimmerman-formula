# CA4-GNC-P — an explicit perspective-carrier variant

This is a separate action from the frozen exponential CA4-GNC in
`FINAL_ACTION.md`. It retains every gravitational, heat, gate, projector,
centered-trace and ordinary-matter term of equation (4), and makes exactly
the following carrier replacement:

\[
 t=1+z=1+Z-\langle Z\rangle_h>0,\qquad
 {\cal L}_{d,P}=tK_d-\frac{W_d}{t},\qquad
 W_d=\frac12\sum_A|D\varphi_A|^2+V+V_0. \tag{P1}
\]

Here `V` is exactly the five-real-field positive-square potential (1).
For the frozen CA4-GNC-P candidate choose declared `V0>0` and set the bare
Einstein `Lambda=0`, matching `assembly/PERSPECTIVE_REPAIR.md`. Algebraic
no-floor comparisons below are explicitly separate `V0=0` controls; they
do not inherit the positive-floor result by a limit without further work.
The configuration space obeys `t>0` and `<t>_h=1`. The mean
is varied, not imposed as a source subtraction after deriving equations.
There is still one independent physical metric and no new independent
carrier species or propagating gate field. The carrier's nonuniversal
composite lapse is now `N_d=N/t`, with characteristic metric
`g_d=g+(1-t^-2)n n` and carrier speed `1/t` in the preferred frame.

## Exact source and force changes

The physical fixed-h lapse density and the Z source differ:

\[
 \rho_{d,P}=tK_d+W_d/t,\qquad
 \sigma_P=\partial_Z{\cal L}_{d,P}|_{\delta z=\delta Z}
       =K_d+W_d/t^2=\rho_{d,P}/t. \tag{P2}
\]

The notation on the derivative first treats local `z` as independent;
varying the actual projector then gives the exact common-action equation

\[
 2M_P^2c_N\operatorname{div}_N(DZ-a+DU)
       +\sigma_P-\langle N\sigma_P\rangle_h/N=0. \tag{P3}
\]

The U/heat equations, metric momentum and centered-trace terms are
unchanged. In the lapse constraint replace the exponential carrier density
by `rho_d,P`. In all carrier projector stress and clock-mean terms (9)–(10),
replace `rho_d` by `sigma_P`; this is required because those terms arise
from `delta z`, not from the lapse derivative. In particular,

\[
 \Delta T^{ij}_{\rm mean,P}
       =-[\langle N\sigma_P\rangle_h/N]z h^{ij}. \tag{P4}
\]

The five exact field equations (8) have the same potential derivatives
and now use `A=t`, `B=1/t`, `C_P=B h-A n n`. The simultaneous U(1)
Noether current remains conserved, with opposite component-current
exchange proportional to `gamma m_L^2 s/t`. In a fixed flat chart,

\[
 \partial_t\rho_{d,P}+\operatorname{div}F_P
       =-\dot z\,\sigma_P,\qquad
 F_P=-t^{-1}\sum_A\dot\varphi_A D\varphi_A. \tag{P5}
\]

The positive `t` field in these formulas is distinguished from the time
coordinate in `partial_t`; equivalently the latter is `partial_tau` in a
unit-lapse chart. The host supplies the corresponding exchange only when
its constraints and metric/clock equations are included.

At `z=0`, (P1) is canonical and
`Ld,P=Kd-Wd+z(Kd+Wd)+O(z^2)`. It has exactly the same leading
Newtonian reciprocal response (15)–(16) only in the no-floor `V0=0` weak
cold-carrier ordering, or as a controlled approximation when the floor's
susceptibility is negligible at the resolved scales. Subtracting a constant
homogeneous vacuum does not accomplish this: at zero excitations,
`rho=V0/t` and `sigma=V0/t^2`, so
`delta rho=-V0 z`, `delta sigma=-2V0 z` and
`delta(rho-sigma)=V0 z`. The projected source also has a lapse contribution
`+V0 delta ln N` at nonzero modes about a homogeneous unit-lapse state.
Thus the full linear response with the floor must include its changed
constraint vertices; a subhorizon estimate requires a stated small ratio
such as `V0/(M_P^2 k^2)` and a consistent background. Reciprocity follows
from the action but does not fix the old matrix entries. For finite `z`, the
carrier acceleration uses the composite potential `Phi-ln(t)` and the
source is `rho/t`, not `rho`. Consequently exact finite-amplitude density
subtraction is relinquished. No complete PPN force law is inferred from
this first-order agreement or from the changed characteristic metric.

## Canonical joint convexity: what is actually repaired

At fixed spatial metric, field coordinates, their spatial gradients, and
canonical momenta `Pi_A`, let

\[
 \epsilon_0=\sum_A\frac{\Pi_A^2}{2h}+W_d,\qquad
 \Pi_A=\sqrt h\,t\,n(\varphi_A).
\]

The carrier Hamiltonian, apart from the Z-independent shift term, is
`N sqrt(h) epsilon0/t`. With `m=M_P^2 cN>0` and `b=a-DU`, the exact
Z-dependent canonical functional is

\[
 H_{Z,P}=\int N\,d\mathrm{vol}_h
       [m|Dt-b|^2+\epsilon_0/t],\quad\langle t\rangle_h=1. \tag{P6}
\]

This is not obtained by testing a fixed-velocity Lagrangian Hessian.
Write `p_A=Pi_A/sqrt(h)` and hold `Wd` fixed. The local simultaneous
momentum/t second variation is

\[
 \delta^2\left[\frac{\sum_Ap_A^2/2+W_d}{t}\right]
 =\frac1t\sum_A\left(\delta p_A-\frac{p_A}{t}\delta t\right)^2
       +\frac{2W_d}{t^3}(\delta t)^2\ge0. \tag{P7}
\]

The gradient part adds `2m ||D delta t||_N^2`. On the mean-zero tangent
space the gradient term is strict for nonconstant `delta t`. At any fixed
finite-dimensional truncation with positive bounded `t`, eliminating this
positive auxiliary block leaves a positive momentum Schur complement.
This removes the exponential two-cell negative-Hessian mechanism.
An infinite-dimensional uniform kinetic bound requires corresponding
norm/coefficient bounds. This argument fixes the carrier coordinates; it
does not assert that the nonlinear interaction potential is jointly convex
in all carrier field coordinates or that the full constrained gravitational
Hamiltonian is positive.

Root's `../assembly/PERSPECTIVE_REPAIR.md` supplies the stronger static
existence/barrier argument under `V0>0`, smooth bounded data and positive
bounded lapse on a compact connected leaf. Its regularization and minimum
estimate are separate evidence from the elementary identity (P7). The
barrier is a fixed-data constraint result; propagation of its constants in
the coupled gravitational evolution remains open. A positive floor is not
silently supplied by gravitational `Lambda`, because the latter is
Z-independent and does not contribute to `epsilon0/t`.

## Homogeneous vacuum interpretation and remaining price

On the homogeneous inactive FRW branch, `z=0`, `t=1`; (P3) admits nonzero
carrier energy because its source is projected. The field equations are
canonical and the constant floor contributes

\[
 \rho_{V_0}=V_0,\quad P_{V_0}=-V_0,\quad
 \Lambda_{\rm homogeneous,eff}=V_0/M_P^2. \tag{P8}
\]

With homogeneous fields at their zero potential minimum, the floor has
vacuum stress and no excitation abundance. On inhomogeneous leaves its
coupling `-V0/t` also contributes to the auxiliary equation and projector
stress. It is therefore not merely a redundant renaming of the independent
Einstein constant `Lambda`. An extension with an independent nonzero bare
`Lambda` would instead have `Lambda_eff=Lambda+V0/M_P^2`, introducing a
second vacuum input. Its positive value can provide a mathematical
positivity floor for the carrier lapse; the action does not derive its
value, identify it uniquely with observed dark energy, or establish a
cosmological solution with the required abundance.

CA4-GNC-P retains GNC's known changed off-branch force and global gate
interfaces. Exact original global filtered MOND, previous data passes,
global timelike foliation, full Dirac count, arbitrary-background tensor
health and a coupled global Cauchy theorem remain unearned. The improvement
is an explicit common-action carrier coupling with a changed source and a
positive fixed-coordinate canonical block, rather than a claim that the
entire theory is complete.

`perspective_run1/` checks the action-level Legendre, source, energy-exchange
and Hessian identities exactly. These checks do not stand in for the root
functional-analytic proof or the open evolution theorem.
