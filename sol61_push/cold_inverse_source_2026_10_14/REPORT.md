# An explicit geometric source and a regulated local matter model

2026-10-14. CIS-001/002/003.
Base 6ed48b14bf28a573b375818b4754206bb77b4f5c; nearest source checkpoint
[CWS-001/004](../cold_wall_source_2026_10_14/REPORT.md).

**Outcome:** an explicit generally covariant four-field action supports the
prescribed geometry and satisfies all its matter equations. A separate
source-preserving regulator and strain interactions give a positive frozen
matter Hamiltonian, with a uniform finite-band group-speed bound below c.
The full coupled gravity/interface/launch problem is unresolved. This is an
inverse-designed mathematical candidate, not a discovery of cold particles,
an independent prediction of the bubble, or a working engine.

## 1. Exact source action

Use signature -+++, c=hbar=1 and reduced Planck mass Mp. Introduce four
scalar fields Phi^A with invertible gradients. They are material-coordinate
fields, with dimensions of length; Phi0 is a clock and PhiI label positions.
For a smooth target metric g*, define functions on their field space by

\[
 H_{AB}(\Phi)=M_p^2R_{AB}[g_*](\Phi),\qquad
 S_0=\int\sqrt{-g}\left[\frac{M_p^2}{2}R
 -\frac12H_{AB}(\Phi)g^{\mu\nu}\partial_\mu\Phi^A
 \partial_\nu\Phi^B\right].
\]

H has dimensions of energy density. All coefficients are specified functions
of scalar fields, so the action is covariant under spacetime coordinate
changes. It explicitly encodes the target curvature in those functions.

At Phi^A=x^A and g=g*,

\[
 T_{\mu\nu}=H_{\mu\nu}
 -\frac12g_{\mu\nu}g^{AB}H_{AB}=M_p^2G_{\mu\nu}[g_*].
\]

Thus all Einstein equations hold, not only the energy-density equation.
The four scalar Euler-Lagrange equations are

\[
 E_A=\frac1{\sqrt{-g}}\partial_\mu
 [\sqrt{-g}H_{AB}g^{\mu\nu}\partial_\nu\Phi^B]
 -\frac12\partial_AH_{BC}\,g^{\mu\nu}
 \partial_\mu\Phi^B\partial_\nu\Phi^C=0.
\]

On this background they follow from the contracted Bianchi identity, with
the invertible field map converting stress conservation into the four
equations. The computation independently evaluates every E_A directly for
arbitrary static b(x,y,z), as well as all ten Einstein components.

The target used here is

\[
 ds_*^2=-dt^2+dx^2+dy^2+[dz+b(r)dt]^2,\quad b=V(1-f(r)).
\]

It is the previous constant-speed bubble in its moving coordinate system.
To avoid differentiability problems of the old C2 quintic at interfaces,
take a C-infinity compact transition: f=1 for r<=R/2, f=0 for r>=R, and
f=1-s(u) between, where u=2r/R-1,
s(u)=eta(u)/[eta(u)+eta(1-u)] and eta(u)=exp(-1/u) for u>0, zero otherwise.
No old profile input or evidence is altered. The symbolic construction uses
an arbitrary smooth b, not a numerical approximation to this transition.

This inverse construction is formal source realization. It makes no claim
that measured matter has these coefficients or that preparing the fields
is possible. The chosen speed is a parameter of the target; acceleration,
launch and net momentum generation have not been derived.

## 2. The source carries momentum, but its bare kinetic form is unacceptable

For n=partial_t-b partial_z and ez=partial_z,

\[
 T(n,e_z)=H_{0z}-bH_{zz}=M_p^2G(n,e_z).
\]

The clock/material coupling supplies the previously missing signed momentum
stress. It is not a positive dust component with an assigned velocity.
One may also form the identically conserved material-label current
J^mu=epsilon^{mu nu alpha beta} partial_nu Phi1 partial_alpha Phi2
partial_beta Phi3. Its divergence vanishes by commuting derivatives. For the
target, J=(1,0,0,0), with norm -1+b^2. It is timelike when |b|<1, including
0<=V<1 and 0<=f<=1. This counts material labels, not known particles or
baryon number. No superluminal material-current interpretation is claimed.

The bare action is not a viable ordinary medium. In the normal frame,

\[
 H_{nn}+H_{zz}=M_p^2(R_{nn}+R_{zz})
 =-M_p^2(b_x^2+b_y^2)<0
\]

where the transverse gradient is nonzero. Its frozen scalar time-kinetic
form has a negative direction. The planar constant-shear control gives
H/h=diag(-1,1,0,-1), h=Mp^2 s^2/2>0. Its uncoupled matter action contains
negative kinetic sectors; merely supplying an exact stress is insufficient.

## 3. Strain interactions preserve the source but have a precise limitation

Define B^{AB}=g^{mu nu}partial_mu PhiA partial_nu PhiB and
DeltaB^{AB}=B^{AB}-g_*^{AB}(Phi). Quadratic terms in DeltaB vanish along
with their first variations on the target. They change the perturbations
without changing any background field equation.

Use the target coframe theta0=dt, theta1=dx, theta2=dy,
theta3=dz+b dt, expressed as functions on field space. The framed strains
S^{ab}=theta^a_A theta^b_B DeltaB^{AB} have frozen principal variations

\[
 S^{00}=-2\dot\pi^0,\quad
 S^{0i}=-\dot\pi^i+\partial_i\pi^0,\quad
 S^{ij}=\partial_i\pi^j+\partial_j\pi^i.
\]

For arbitrary regular quadratic strain coefficients, restrict to clock/z
disturbances. If Kzz is the time-kinetic coefficient of piz and G0z is the
spatial-energy coefficient of partial_z pi0, direct expansion gives

\[
 K_{zz}+G_{0z}=H_{zz}+H_{00}.
\]

It is negative for the directed bubble in this frame. Hence ordinary
first-derivative strain interactions cannot make both forms positive here.
The conclusion is about this Hamiltonian criterion. It is not an assertion
that every indefinite-energy system has imaginary frequencies. The run
includes a real-root mixed-derivative control u^2-4u+1=0 to distinguish them.

For the planar benchmark the same obstruction exists in every timelike
frame: H(u,u)/h=-(1+uy^2+2uz^2)<0 and the Lorentz trace of H/h is 1.
The sum of its spatial diagonal entries in any such frame is therefore
1+H(u,u)/h<=0. At least one spatial direction still has
H(u,u)+H(e,e)<0. This argument is specific to that benchmark.

Indefinite Hamiltonians and stability in general Lorentz-breaking theories
need careful distinctions; [Dubovsky et al., hep-th/0512260v2, section 3.1](https://arxiv.org/pdf/hep-th/0512260v2)
provides relevant exceptions. No universal NEC/stability theorem is imported
from that paper or claimed here.

## 4. A separate projected-clock-curvature term removes the local obstruction

Define the unit clock normal U_mu=-partial_mu Phi0/sqrt[-(dPhi0)^2],
P^{mu nu}=g^{mu nu}+U^mu U^nu, and

\[
 Q=P^{\mu\nu}\nabla_\mu\nabla_\nu\Phi^0,\qquad
 L_Q=-\frac{hD}{2}[Q-Q_*(\Phi)]^2,\quad D>0.
\]

On the target Q*=b_z. The difference and its first variations vanish there,
so this term also preserves the exact solution of all background equations.
With the metric frozen, its highest-derivative scalar variation is Delta pi0;
it contributes -hD(Delta pi0)^2/2 to the local matter action. Unlike the
strain-only repair, this term adds positive fourth-order spatial energy to
the clock without the same linked material time-kinetic penalty.

Metric variations also enter Q, including metric time derivatives. The
frozen-matter calculation does not establish degeneracy, absence of extra
modes, or stability of the full gravity/clock system. No covariant ultraviolet
completion or physical cutoff is asserted.

## 5. Explicit strain coefficients for arbitrary bounded source H

This is an algebraic construction, not a fitted set of constants. In the
target normal frame choose a constant h>0 bounding the Euclidean operator
norm of H. A smooth finite target has a finite bound. Write
Ht=H00/h, a_i=H0i/h, Hs_ij=Hij/h; then |Ht|, norm(a), norm(Hs)<=1.
Set Kc=10^12, L=100, mu=2, B=L I-Hs. Add, in units of h,

\[
\begin{split}
 L_{\rm strain}/h={}&(K_c-H_t)(S^{00})^2/8
 +\tfrac12 S_0^T B S_0-\tfrac12 S^{00}(a\cdot S_0)\\
 &-\tfrac\mu4\sum_{ij}(S^{ij})^2
 +\sum_i a_i\left[\sum_j S^{0j}S^{ij}
 -\tfrac12 S^{0i}\operatorname{tr}S\right].
\end{split}
\]

Here trS sums spatial entries only. Every term is at least quadratic in
zero-background strains. The large assigned hierarchy has not been shown
radiatively stable, natural, physically accessible or within a microscopic EFT.

The exact frozen quadratic matrices, with h factored out, become

\[
 K=\operatorname{diag}(K_c,L,L,L),\qquad
 G_{00}=Dk^4+(H_t-L)k^2+k^TH_s k,
\]
\[
 G_{0i}=0,\qquad G_{\rm sp}=k^2(H_s+2I)+2kk^T.
\]

Mixed time/spatial terms are retained. After normalizing K to I, their
symmetric symbol W is

\[
 W_{00}=2a\cdot k/K_c,\quad
 W_{\rm sp}=-2a\cdot k\,I/L,\quad
 W_{0\rm sp}=-(Bk)^T/\sqrt{K_cL}.
\]

For 103<=q=Dk^2<=10^5, the normalized G has strictly positive blocks:
Gclock>=k^2/Kc, Gsp>=k^2/L. The Legendre Hamiltonian is

\[
 H_2=\tfrac12(p-M\nabla\pi)^TK^{-1}(p-M\nabla\pi)
 +\tfrac12\pi^TG(k)\pi.
\]

It is positive for these frozen modes. This statement includes the mixed
terms rather than discarding their effect on the momentum.

## 6. All-direction finite-band group-speed proof

In canonically normalized variables the wave equation is
[omega^2 I-omega W(k)-G(k)]v=0. Let X=sqrt(G), the positive matrix square
root. The real symmetric matrix

\[
 A(k)=\begin{pmatrix}W&X\\X&0\end{pmatrix}
\]

has its eight frequencies as eigenvalues. Thus they are real. For any unit
direction m, a differentiable eigenfrequency satisfies
|partial_m omega|<=norm(partial_m A); the same Lipschitz bound controls
branches through degeneracies.

The source-norm assumptions give

\[
 \|\partial_m W\|\le2/K_c+2/L+101/\sqrt{K_cL}.
\]

For the spatial block, norm(partial_m Gsp)<=10|k|/L and
lambda_min(sqrt(Gsp))>=|k|/sqrt(L). Differentiating X^2=G and using its
Sylvester integral solution
partial_m X=integral_0^infinity exp(-tX)(partial_m G)exp(-tX)dt gives
norm(partial_m sqrt(Gsp))<=5/sqrt(L)=0.5.

For the clock block, the quadratic anisotropy matrix
(L-Ht)I-Hs has eigenvalues between 98 and 102. Therefore

\[
 |\partial_m\sqrt{G_{00}}|
 \le\frac{2q_{\max}-98}{\sqrt{K_c}\sqrt{q_{\min}-102}}
 =0.199902.
\]

Using the larger square-root block bound gives the uniform result

\[
 \boxed{|v_g|/c\le0.520010100002<1}
\]

throughout the specified band, for every direction and every source matrix
with the stated norm bound. This is a local finite-band wavepacket group
velocity bound with the metric frozen. It is not an ultraviolet front speed,
a full characteristic-cone theorem, or a global causal/stability certificate.

The specialized planar run independently checks 18 direction/momentum cases
using Hermitian spectra, square-root derivatives and the original quadratic
wave pencil. Their largest computed group speed is 0.2211673. The uniform
claim relies on the norm proof, not that finite table. The arbitrary-H
coefficients and mixed symbols are separately checked as exact polynomials.

## 7. What would turn this into a physical mechanism

The source is now specified by an action, not an unspecified exotic Tmunu.
The conditional mechanical sequence is: prepare the four-field material
state; its clock/material stresses support the geometry; strain interactions
give positive local time kinetic energy; the projected clock-curvature term
regulates the remaining spatial energy over a defined band.

The following implications remain unproved:

1. **Actual medium:** no microscopic carrier, state-preparation process or
   measured coupling produces this engineered action. It is not identified
   with the chi/S neutron portal or the reciprocal tether medium.
2. **Long wavelengths and boundaries:** the infinite-space action still has
   problematic modes below the band. No finite interface has been derived
   to remove them. An imposed mode restriction is not a physical wall.
3. **Full gravity:** varying the metric in LQ changes the coupled constraint
   and kinetic equations. The calculation here freezes those fluctuations.
4. **Finite wall:** gradients of the inhomogeneous coefficients, interface
   modes and low-frequency evolution can defeat local frozen stability.
5. **Control and conservation:** a prepared constant-speed solution is not
   a launch, steering, acceleration or finite-hardware momentum budget. The
   target also omits a massive craft and fuel; adding their stress requires
   solving a different combined source and geometry.
6. **Conversion:** adding baryon/light production changes Tmunu. No derived
   coupling currently routes that reaction's energy into this medium while
   keeping the combined source solution. Baryon-number transfer remains a
   separate conditional mechanism.

These are required physical steps. The exact inverse solution and its
regulated local matter band provide a concrete model to test against them;
they do not establish a feasible drive or immunity of surrounding baryons.

Evidence: 69 assertions across three completed bounded runs, retained inputs,
validated manifests and self-review. No independent agent or novelty claim.
