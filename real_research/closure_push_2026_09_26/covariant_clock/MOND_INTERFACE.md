# The polar clock inside the same exact-MOND action

**Result:** the healthy charged amplitude can be coupled covariantly to the
same phase that defines the MOND foliation, but the minimal combined action
acquires an independent, nonconstant metric source. Its density response is
strictly nonzero on the stable charged branch. A homogeneous vacuum subtraction
does not recover baryon-only AQUAL. The original covariant homogeneous result
remains valid for its stated Einstein–polar action; it is not silently promoted
to a solution of every added clock interaction.

**Checkpoint scope:** the F_C/AQUAL operator below is the explicit candidate
assigned before the shared specification changed in external commit
`9092fc0fd02b904e87c708971335cd63adb18151`. The operative target now uses filtered
nu_mono and criterion B, allowing well-posed leafwise instantaneous channels.
No AQUAL calculation or metric-cone exclusion is used here to reject that
amended target. The polar density variation is independent of which MOND
operator is added; an unchanged additive polar sector would also contribute
extra metric source terms to a baryon-only nu_mono construction. Whether a
different common action cancels them remains an action-specific question.

## Explicit common action and Newton normalization

Keep one physical metric and define
n_mu=-partial_mu T/sqrt(-(partial T)^2), a_mu=n^nu nabla_nu n_mu. Add

\[
S=\int\sqrt{-g}\,d^4x\left\{
\frac{M_b^2}{2}[\mathcal R+F_C(a)]-\rho_\Lambda
-\frac12(\partial R)^2-\frac12R^2(\partial T)^2-V(R)\right\}+S_b,
\quad M_b^2=(8\pi G_{\rm bare})^{-1},
\]
\[
x=|a|/a_0,\qquad
F_C=2(1-C)a_0^2x^2+4Ca_0^2[1-(1+x)e^{-x}],\quad C>0.
\]

This is the normalization used in the parallel Newton-normalization route.
On its bare weak-static branch, eliminating the spatial potential with its
source-free stress equation gives

\[
-2a_0^2x^2+F_C=-2Ca_0^2\mathcal A(x),\qquad
\mathcal A=x^2+2(1+x)e^{-x}-2,
\]

so mu(x)=1-exp(-x) and the measured coupling is GN=Gbare/C. We rederive this
primitive in the interface script; its normalization does not cancel any
additional matter density. An added term proportional to K^2 vanishes,
together with its first variation, on this exactly static K=0 branch, so it
does not change the source obstruction below. The full dynamical count and
health of the combined F_C action are not inherited from the bare polar action.

There is nevertheless an exact shared homogeneous branch: on aligned FRW,
a_mu=0, F_C(0)=0, and its first derivative with respect to a_mu vanishes.
Thus adding this F_C term alone contributes neither background stress nor a
background clock equation. The homogeneous equations and charge-barrier
theorem in RESULT.md extend to this minimal common action with Mpl replaced
by Mb. This is a background statement; the second variation changes the
clock/metric perturbations. A K^2 term or an environmental gate would require
its own homogeneous variation before making the same extension.

Here, **X=-(partial T)^2/2**. This is half the X used in section 7 of RESULT.md.
We also write q=2X to keep the translation explicit.

## Exact static radial and lapse equations

For ds^2=-N(x)^2 dt^2+h_ij(x)dx^i dx^j, T=Omega t with Omega!=0,

\[
q=\Omega^2/N^2=2X,\quad a_i=D_i\ln N,\qquad
S_{\rm polar,static}=\int dt\,dV_h\left[
\frac{\Omega^2R^2}{2N}-N\left(\frac12(DR)^2+V\right)\right].
\]

The radial equation is exactly

\[
\boxed{\Delta_N R+qR-V'(R)=0},\qquad
\Delta_N=N^{-1}D_i(ND^i).
\]

F_C has no direct R dependence. A constant nonzero R would require
V'(R)/R=Omega^2/N(x)^2, which is impossible for varying N and fixed Omega.
Thus a constant charged amplitude cannot simply be carried unchanged into a
nontrivial static gravitational potential.

At fixed h,R,T, the additional lapse density is exactly

\[
\boxed{\rho_c=-\frac1{\sqrt h}\frac{\delta S_{\rm polar}}{\delta N}
=\frac12qR^2+\frac12(DR)^2+V(R).}
\]

The vacuum adds rhoLambda separately. In a static ADM reduction, the complete
lapse equation has the necessary term

\[
\frac{M_b^2}{2}\left[\mathcal R^{(3)}+F_C-
\operatorname{div}_N\left(\frac{\partial F_C}{\partial a}\right)\right]
=\rho_b+\rho_c+\rho_\Lambda,
\quad
\frac{\partial F_C}{\partial a_i}=4[1-C\mu(x)]a^i.
\]

This equation is a necessary common-action field equation, not a full static
solution. In particular, the spatial metric variation also sees clock
pressure and radial-gradient stresses. It is inconsistent to retain rho_c
while borrowing the bare source-free spatial equation to impose no slip.

## Radial gradients retained: the density cannot disappear at finite k

Use a constant circular reference patch R=R0>0, q=q0>0, V'=q0 R0 and
mu_r^2=V''-q0>0. This defines the local static response; it is not a claimed
global Minkowski Einstein solution with positive homogeneous density.
For nu=delta ln N, delta q=-2q0 nu and r=delta R, the linear radial equation is

\[
(\Delta-\mu_r^2)r=2q_0R_0\nu,\qquad
r_k=-\frac{2q_0R_0}{k^2+\mu_r^2}\nu_k.
\]

The perturbation of (DR)^2 starts at second order on this reference patch.
Since V'=q0 R0, the exact first-order density response is

\[
\boxed{\displaystyle
\delta\rho_{c,k}=-\mathcal S(k)\nu_k,\qquad
\mathcal S(k)=R_0^2q_0\left[1+\frac{4q_0}{k^2+\mu_r^2}\right]>0.}
\]

It approaches R0^2 q0>0 at high k; the amplitude's gradient stiffness reduces
its response but does not remove the direct phase contribution. Static
radial boundary conditions can add homogeneous solutions to the elliptic
equation; they cannot cancel this forced multiplier for all lapse profiles.
A constant vacuum shift changes the zero-mode background density, not S(k).

Pressure is equally relevant. On the circular reference patch,

\[
\delta p_c=-R_0^2q_0\nu,\qquad
\delta(\rho_c+3p_c)_k=-4R_0^2q_0
\left[1+\frac{q_0}{k^2+\mu_r^2}\right]\nu_k.
\]

For weak static scalar metric potentials phi,psi and an isotropic source at
the retained order, the Einstein kinetic density is
M_b^2[(grad psi)^2-2 grad phi.grad psi], and source variation is
-rho delta phi-3p delta psi. Consequently the spatial equation gives
Delta(phi-psi)=3p/(2M_b^2). Together with the lapse equation it gives the
leading trace-reduced source rho+3p in the AQUAL equation, with GN=Gbare/C.
For nonrelativistic matter, p is negligible and this reduces to rho. This
weak-field comparison requires the usual local-background subtraction and
does not replace the full curved/static tensor equations. In either version,
the charged clock contributes a nonzero response; neither its pressure nor
its density can be silently discarded.

## Controlled Thomas–Fermi limit and cancellation obstruction

For V=m0^2 R^2/2+lambda R^4/4, m0^2>=0, lambda>0, dropping radial gradients
is an approximation requiring |Delta_N R| small relative to the radial
restoring terms. On its active branch q>m0^2,

\[
R_*^2=\frac{q-m_0^2}{\lambda}=\frac{2X-m_0^2}{\lambda},\qquad
P(X)=\frac{(2X-m_0^2)^2}{4\lambda}.
\]
\[
\rho_c=2XP_X-P=\frac{(2X-m_0^2)(6X+m_0^2)}{4\lambda},\qquad
\frac{d\rho_c}{d\ln N}=-\frac{2X(6X-m_0^2)}{\lambda}
=-\frac{q(3q-m_0^2)}{\lambda}<0.
\]

This is exactly the k=0 limit of the gradient-retaining susceptibility. It is
not a free choice of a cosmological density: Omega, amplitude boundary data,
and the conserved charge come from the independent clock/matter initial data.
Nor is this calculation a particle interpretation or an imposed abundance.

The cancellation problem has a short general formulation. For any regular
first-derivative phase action P(X) on a timelike branch, define

\[
A=P_X+2XP_{XX},\qquad B=P_X.
\]

Healthy phase time kinetics and positive spatial gradient energy require
A>0 and B>0. But

\[
\frac{d\rho}{dX}=A>0,\quad
\frac{d(\rho+3p)}{dX}=A+3B>0,\quad \delta X=-2X\nu.
\]

Therefore neither density nor active trace can be independent of N on an
open interval while retaining both health conditions in this P(X) class.
An exact constant-density solution is P=b sqrt(X)+c, for which A=0. An exact
constant-active-trace solution is P=-b/X+c, for which A=-3B. These are not
healthy replacements with the same propagating phase mode. A constant
counterterm has no effect on A or B. A compensating X-dependent action must
be counted in the total A and B; cancellation cannot be assessed by its
background stress alone. This is a scoped obstruction for the stated minimal
addition and first-derivative effective phase class, not a theorem excluding
all constrained multi-field or higher-derivative constructions.

## Active versus inactive branches: an open constructive alternative

The algebraic radial potential is V(R)-qR^2/2. For the positive-mass quartic,
its stable inactive minimum is R=0 when q<m0^2; its active minimum has R>0
when q>m0^2. The inactive branch has no polar charge stress if V(0)=0, so it
can remove this particular static source locally. It also removes the
canonical phase kinetic coefficient R^2 and the active gyroscopic mapping.
At q=m0^2 the radial restoring gap closes and the Thomas–Fermi approximation
cannot certify the transition. If T is literally the phase of a complex
field, that phase is undefined at R=0. If T is instead an independently
fundamental MOND clock, its dynamics there must be supplied and tested by
the F_C sector; this is a different interpretation with explicit obligations.

A second possibility is an explicitly varied smooth environmental gate
h multiplying the polar action, with h identically zero on a galactic
plateau. On such an open plateau, h and its gate derivatives can vanish,
removing the polar stress. The canonical polar kinetic block then also
degenerates, and the healthy active-branch completion does not transfer
unchanged. Where h varies, its metric/clock variations give additional
transition stress and equations. Even if h were independent of T, the
homogeneous conserved charge would be a^3 h R^2 Tdot, not a^3 R^2 Tdot;
its energy contains J^2/(2a^6 h R^2). A finite-energy homogeneous solution
with fixed nonzero J cannot simply reach h=0 at bounded a and R.
For a gate depending on the normalized clock geometry, the phase current
itself gains the corresponding gate contributions and must be rederived.

Thus a spatially inactive galactic branch is a candidate to construct,
not a forbidden option. It requires an actual dynamic transition, charge
transport or constraint mechanism, metric-source calculation, and a new
global clock argument. The homogeneous charge-barrier theorem in RESULT.md
cannot be inherited across a zero kinetic coefficient or phase node.

## Verification and exact remaining implication

`check_mond_interface.py` and `interface_contract.json` define a new bounded
run in `interface_run1/`. **20 checks passed**: 18 exact symbolic identities,
a grouped nonlinear finite-graph central-difference check, and a negative
control. The 32-node weighted cycle varies both lapse-dependent node mass
and edge conductance, solves the nonlinear radial equation, and computes its
variational lapse density including the radial-gradient contribution.
At the finest step, the radial-response error is 5.93e-11 and the density
response error is 1.15e-9; residuals are below 1.35e-13. Freezing the amplitude
instead misses 1.8186 of the density susceptibility in that declared example.
The manifest validator accepted the input and result hashes. The finite graph
uses a prescribed lapse and is not a full metric solution or an empirical fit.

The source provenance record distinguishes the action normalization examined
in the parallel route, the earlier gyroscopic target, the independently
derived formulas, and the limited primary literature comparison.
`PushClock20260926.lean` compiled successfully with Lean 4.34.0-rc2 and the
existing Mathlib revision in 32.3966 s. Its three conditional lemmas prove
positive susceptibility, a nonzero response for a nonzero lapse perturbation,
and A+3B>0 from A,B>0. They use only the standard propext, Classical.choice,
and Quot.sound axioms. Source and log hashes were independently checked
against `../ic27_bridge/clock_lean_record.json`; the compiler log is
`../ic27_bridge/clock_lean_final.log`. These are scalar algebra bridges after
the physical formula is supplied, not a formal derivation of the action,
constraints, PDE, or field count.

The remaining common-action implication is now quantitative: remove or
account for S(k) and the pressure response using an explicit action while
preserving the allowed field content, causal response, MOND law, and clock
domain. A positive vacuum density alone does not perform that cancellation.
