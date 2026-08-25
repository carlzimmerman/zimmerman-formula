# Final Closure Analysis: Causal Nonlocal Metric Theory with Emergent MOND Interpolation

**Status:** Frozen candidate / linearized closure analysis  
**Purpose:** Consolidate the mathematical construction, resolve the localization-ghost objection, state the causal variational prescription, derive the weak-field constitutive law, and distinguish established results from claims that still require a nonlinear theorem.

---

## 1. Executive statement

The proposed theory is most cleanly defined as a **causal nonlocal metric theory**, rather than as an unrestricted local auxiliary-field theory.

The fundamental physical field is the metric

\[
 g_{\mu\nu}.
\]

A preferred timelike foliation is assigned to the metric by a fixed causal initial-value prescription,

\[
\boxed{g^{\mu\nu}\nabla_\mu T\nabla_\nu T=-1},
\]

and

\[
U_\mu[g]=-\nabla_\mu T[g].
\]

The curvature scalar entering the nonlocal response is

\[
\boxed{J[g]=R_{\mu\nu}[g]U^\mu[g]U^\nu[g]}.\]

The causal response field is not an independent field:

\[
\boxed{\Phi[g]=\Box^{-1}_{\rm ret}J[g]}.\]

Define

\[
\boxed{Z[g]=\frac{4c^4}{a_0^2}\nabla_\mu\Phi[g]\nabla^\mu\Phi[g]}
\]

and choose

\[
\boxed{F'(Z)=\frac12e^{-\sqrt Z/2}}.
\]

With

\[
M[g]=-F(Z[g]),
\]

the action is

\[
\boxed{
S_{\rm phys}[g,\psi]
=
S_m[g,\psi]
+\frac{c^3}{16\pi G}
\int d^4x\sqrt{-g}
\left[
R-2\Lambda-\frac{a_0^2}{c^4}M[g]
\right].
}
\]

The weak-field limit gives

\[
\boxed{\mu(y)=1-e^{-y}},
\qquad y=\frac{|\nabla\Psi|}{a_0}.
\]

The decisive qualification is that the construction does **not** yet amount to a universal nonlinear Hamiltonian theorem proving exactly two degrees of freedom on every background. What has been closed is the auxiliary localization objection, the causal prescription, the linearized physical spectrum around Minkowski spacetime, and the constitutive weak-field limit.

---

# 2. Fundamental causal definition

## 2.1 Metric-defined foliation

Let \(\Sigma_0\) be the initial hypersurface together with a choice of time orientation. Define \(T[g]\) by the timelike eikonal equation

\[
\boxed{g^{\mu\nu}\nabla_\mu T\nabla_\nu T=-1}
\]

with fixed initial data, for example

\[
\boxed{T|_{\Sigma_0}=0}.
\]

The construction is intended on any domain where the associated normal geodesics remain a valid foliation. This qualification matters because caustics can obstruct a single global proper-time function.

Define

\[
\boxed{U_\mu=-\nabla_\mu T}.
\]

Then

\[
U_\mu U^\mu=-1.
\]

Moreover,

\[
U^\nu\nabla_\nu U_\mu
=
\nabla_\mu\left(\frac12 U_\nu U^\nu\right)
=0,
\]

so the congruence is geodesic.

### Important correction

One must **not** additionally impose

\[
\Box T=0
\]

as part of the defining equations. Since

\[
\Box T=-\nabla_\mu U^\mu,
\]

that would impose vanishing expansion and overconstrain the generic geometry. The proper-time/eikonal condition is the appropriate geometric prescription here.

---

# 3. Retarded curvature response

Define the scalar curvature source

\[
\boxed{J[g]=R_{\mu\nu}[g]U^\mu[g]U^\nu[g]}.\]

The auxiliary scalar is then defined by the retarded initial-value problem

\[
\boxed{\Box_g\Phi=J}
\]

with

\[
\boxed{
\Phi|_{\Sigma_0}=0,
\qquad
n^\mu\nabla_\mu\Phi|_{\Sigma_0}=0.
}
\]

Equivalently,

\[
\boxed{\Phi[g]=\Box^{-1}_{\rm ret}J[g]}.\]

This is the actual physical definition. The field \(\Phi\) is a response functional of \(g\), not an independently specifiable phase-space coordinate.

---

# 4. Constitutive sector

Define

\[
\boxed{Z[g]=\frac{4c^4}{a_0^2}\nabla_\mu\Phi[g]\nabla^\mu\Phi[g]}
\]

and choose

\[
\boxed{F'(Z)=\frac12e^{-\sqrt Z/2}}.
\]

The modification is

\[
\boxed{M[g]=-F(Z[g])}.
\]

Thus the complete nonlocal functional is

\[
\boxed{
M[g]
=
-F\!\left[
\frac{4c^4}{a_0^2}
\bigg(\nabla_\mu
\Box^{-1}_{\rm ret}
[R_{\alpha\beta}U^\alpha U^\beta]
\bigg)
\bigg(\nabla^\mu
\Box^{-1}_{\rm ret}
[R_{\rho\sigma}U^\rho U^\sigma]
\bigg)
\right].
}
\]

All appearances of \(T\), \(U\), and \(\Phi\) in this formula are shorthand for their causal response maps from the metric.

---

# 5. Physical action and field equation

The physical action is

\[
\boxed{
S_{\rm phys}
=
S_m[g,\psi]
+
\frac{c^3}{16\pi G}
\int d^4x\sqrt{-g}
\left[
R-2\Lambda-\frac{a_0^2}{c^4}M[g]
\right].
}
\]

The metric equation may be written as

\[
\boxed{
G_{\mu\nu}+\Lambda g_{\mu\nu}
+\frac{a_0^2}{c^4}\mathcal E^{\rm ret}_{\mu\nu}[g]
=
\frac{8\pi G}{c^4}T_{\mu\nu},
}
\]

where

\[
\boxed{
\mathcal E^{\rm ret}_{\mu\nu}[g]
=
-\frac{2}{\sqrt{-g}}
\frac{\delta_{\rm causal}}{\delta g^{\mu\nu}}
\left[\sqrt{-g}\,M[g]\right].
}
\]

The adjective ``causal'' is essential because the functional contains a retarded inverse operator.

---

# 6. Correct variation of the retarded response

For a metric perturbation

\[
h_{\mu\nu}=\delta g_{\mu\nu},
\]

the linearized response obeys

\[
\delta(\Box\Phi)=\delta J.
\]

Therefore

\[
\Box\,\delta\Phi
=
\delta J-(\delta\Box)\Phi,
\]

so the physical solution is

\[
\boxed{
\delta\Phi
=
\Box^{-1}_{\rm ret}
\left[
\delta J-(\delta\Box)\Phi
\right].
}
\]

The perturbation obeys the homogeneous-data prescription

\[
\boxed{
\delta\Phi|_{\Sigma_0}=0,
\qquad
n^\mu\nabla_\mu\delta\Phi|_{\Sigma_0}=0.
}
\]

Hence

\[
\boxed{\delta\Phi_{\rm hom}=0}.
\]

In Green-function form,

\[
\delta\Phi(x)
=
\int d^4x'\,G_{\rm ret}(x,x')
\left[\delta J(x')-(\delta\Box)\Phi(x')\right].
\]

Since

\[
G_{\rm ret}(x,x')=0
\]

unless \(x'\in J^-(x)\), the physical response is causal:

\[
\boxed{\delta\Phi(x)\text{ depends only on the causal past of }x.}
\]

---

# 7. Variation of the metric-defined foliation

The foliation itself is fixed by

\[
g^{\mu\nu}\nabla_\mu T\nabla_\nu T=-1.
\]

Varying gives

\[
\delta g^{\mu\nu}\nabla_\mu T\nabla_\nu T
+
2g^{\mu\nu}\nabla_\mu T\nabla_\nu\delta T
=0.
\]

Since

\[
U_\mu=-\nabla_\mu T,
\]

this becomes

\[
\boxed{
U^\mu\nabla_\mu\delta T
=
-\frac12 h_{\mu\nu}U^\mu U^\nu
}
\]

up to the sign convention chosen for \(h_{\mu\nu}=\delta g_{\mu\nu}\). With the prescribed initial condition

\[
\boxed{\delta T|_{\Sigma_0}=0},
\]

\(\delta T\) is fixed by the metric perturbation. There is no freely specifiable homogeneous scalar datum in \(T\).

Thus

\[
\boxed{T=T[g],\qquad \delta T=\delta T[g;h].}
\]

---

# 8. Localization and the apparent ghost

For variational calculations one may introduce a localized representation with \(\Phi\) and an adjoint \(\lambda\). Schematically,

\[
S_{\rm aux}
\sim
S_m
+\int\sqrt{-g}
\left[
\mathcal L(\Phi)
+\lambda\left(\Box\Phi-J\right)
\right].
\]

After integrations by parts the \(\Phi\)-\(\lambda\) kinetic matrix has the structure

\[
\boxed{
H_{\Phi\lambda}
\propto
\begin{pmatrix}
4&1\\
1&0
\end{pmatrix}
}
\]

with

\[
\boxed{\det H_{\Phi\lambda}=-1}.
\]

An unrestricted local theory using this auxiliary action would therefore possess a negative kinetic direction.

That statement is correct.

The crucial distinction is that the causal theory is **not** the unrestricted local theory.

The physical definition is

\[
\boxed{
\Phi=\Phi[g],
\qquad
\lambda=\lambda[g],
\qquad
T=T[g].
}
\]

There are therefore no arbitrary homogeneous solutions for these variables.

---

# 9. The adjoint field is not a physical field

The adjoint is introduced to evaluate the functional derivative efficiently. Its schematic equation is

\[
\boxed{
\Box\lambda
=
-\frac{8c^4}{a_0^2}
\nabla_\mu\left(F'(Z)\nabla^\mu\Phi\right).
}
\]

The relevant solution is selected by the adjoint Green prescription,

\[
\boxed{
\lambda
=
\Box^{-1}_{\rm adv}
\left[-\frac{8c^4}{a_0^2}
\nabla_\mu(F'(Z)\nabla^\mu\Phi)
\right].
}
\]

The advanced inverse appears in the adjoint calculation because it is the adjoint operator to the retarded inverse under the variational pairing. It does not make the physical response advanced.

The important physical statement is

\[
\boxed{\lambda_{\rm hom}=0}.
\]

Therefore an auxiliary homogeneous combination such as

\[
\chi=\lambda+4\Phi,
\qquad
\Box\chi=0,
\]

is not an independently specifiable physical oscillator.

Hence

\[
\boxed{
\text{an indefinite localization Hessian is not, by itself, a physical ghost theorem for the causal theory.}
}
\]

---

# 10. Linearized spectrum around Minkowski

Take

\[
g_{\mu\nu}=\eta_{\mu\nu}+h_{\mu\nu}
\]

with background

\[
T_0=t,
\qquad
U^\mu_0=(1,0,0,0).
\]

The background curvature vanishes,

\[
R^{(0)}_{\mu\nu}=0,
\]

so the first-order source is

\[
\boxed{J^{(1)}=R^{(1)}_{00}}.
\]

The first-order response is therefore

\[
\boxed{\Box\Phi^{(1)}=R^{(1)}_{00}}
\]

with retarded homogeneous data fixed to zero.

---

# 11. Tensor sector

For a transverse-traceless perturbation

\[
h_{ij}=h^{TT}_{ij},
\]

satisfying

\[
\partial_i h^{TT}_{ij}=0,
\qquad
h^{TT}_{ii}=0,
\]

one has

\[
R^{(1)}_{00}[h^{TT}]=0.
\]

Therefore

\[
\boxed{\Phi^{(1)}_{TT}=0}.
\]

The modification does not generate an additional TT kinetic operator at quadratic order. The tensor action is therefore the Einstein quadratic action,

\[
\boxed{
S^{(2)}_{TT}
=
\frac{c^3}{64\pi G}
\int d^4x
\left[
\frac{1}{c^2}\dot h^{TT}_{ij}\dot h^{TT}_{ij}
-
\partial_k h^{TT}_{ij}\partial_k h^{TT}_{ij}
\right].
}
\]

The resulting dispersion relation is

\[
\boxed{\omega^2=c^2k^2}.
\]

Thus the linearized tensor sector has exactly two polarizations,

\[
\boxed{N_{\rm tensor}=2},
\]

with

\[
\boxed{c_T=c}.
\]

---

# 12. Linearized scalar sector: what can and cannot be concluded

Use the scalar decomposition

\[
ds^2=-(1+2A)dt^2+(1-2B)\delta_{ij}dx^idx^j
\]

for a scalar-sector test.

At first order, since the background curvature vanishes,

\[
J^{(1)}=R^{(1)}_{00}.
\]

With the stated conventions,

\[
R^{(1)}_{00}
=
\nabla^2 A+3\ddot B.
\]

Hence

\[
\boxed{
\Box\Phi^{(1)}
=
\nabla^2A+3\ddot B.
}
\]

For a Fourier mode \(e^{-i\omega t+i\mathbf k\cdot\mathbf x}\),

\[
\Box\rightarrow \omega^2-k^2,
\]

and

\[
R^{(1)}_{00}
=
-k^2A-3\omega^2B.
\]

Therefore

\[
\boxed{
\Phi^{(1)}
=
-\frac{k^2A+3\omega^2B}{\omega^2-k^2}
}
\]

for the retarded response, understood as a Green-function relation rather than as an additional free scalar field.

### Important methodological status

A complete scalar-sector determinant is more delicate than the TT calculation because it depends on the exact gauge choice, all constraint terms, boundary prescriptions, and the precise normalization of the causal variational functional. A scalar determinant should therefore be generated and checked symbolically from the full quadratic action before being promoted to a theorem.

The robust conclusion that does **not** depend on such a shortcut is:

1. \(T\) has no independent initial data under the metric-defined prescription;
2. \(\Phi\) has no independent homogeneous initial data under the retarded prescription;
3. \(\lambda\) is an adjoint response and has no physical homogeneous data;
4. the TT sector has exactly two luminal modes.

Thus the localization fields do not themselves add scalar Cauchy data.

A stronger statement that the **complete nonlinear metric theory has exactly two propagating degrees of freedom on every background** remains a separate theorem and is not asserted here.

---

# 13. Weak-field / quasistatic limit

Take the standard weak-field metric,

\[
g_{00}\simeq-
\left(1+\frac{2\Psi}{c^2}\right).
\]

In the quasistatic regime,

\[
U^\mu\simeq(1,0,0,0),
\]

and

\[
\boxed{
R_{\mu\nu}U^\mu U^\nu
\simeq
\frac{\nabla^2\Psi}{c^2}.
}
\]

Therefore

\[
\nabla^2\Phi
=
\frac{\nabla^2\Psi}{c^2}.
\]

With the prescribed trivial homogeneous solution,

\[
\boxed{\Phi=\frac{\Psi}{c^2}}.
\]

Therefore

\[
Z
=
\frac{4c^4}{a_0^2}
\frac{|\nabla\Psi|^2}{c^4}
=
4\frac{|\nabla\Psi|^2}{a_0^2}.
\]

Define

\[
\boxed{y=\frac{|\nabla\Psi|}{a_0}}.
\]

Then

\[
\boxed{Z=4y^2}.
\]

The constitutive law becomes

\[
F'(4y^2)
=
\frac12e^{-y}.
\]

With the intended weak-field normalization,

\[
\mu(y)=1-2F'(4y^2),
\]

so

\[
\boxed{\mu(y)=1-e^{-y}}.
\]

The modified Poisson equation is therefore

\[
\boxed{
\nabla\cdot
\left[
\left(1-e^{-\frac{|\nabla\Psi|}{a_0}}\right)
\nabla\Psi
\right]
=
4\pi G\rho_b.
}
\]

The two limits are

\[
1-e^{-y}=y+O(y^2),
\qquad y\ll1,
\]

and

\[
1-e^{-y}\rightarrow1,
\qquad y\gg1.
\]

Hence

\[
\boxed{\mu(y)\sim y\quad(y\ll1)}
\]

and

\[
\boxed{\mu(y)\rightarrow1\quad(y\gg1)}.
\]

This is the constitutive closure.

---

# 14. Causality and the advanced adjoint

The physical map is retarded:

\[
\Phi[g](x)=\int d^4x'\,G_{\rm ret}(x,x')J[g](x').
\]

Therefore

\[
G_{\rm ret}(x,x')=0
\]

for spacelike or future-separated \(x'\) relative to \(x\).

The adjoint field may involve

\[
G_{\rm adv}(x,x')
\]

because functional differentiation reverses the direction of the Green operator under the spacetime pairing.

This does not change the causal physical response.

The distinction is

\[
\boxed{
\text{physical propagation: retarded}
}
\]

versus

\[
\boxed{
\text{variational adjoint: advanced}
}
\]

The advanced adjoint is a computational response, not an independently emitted physical signal.

---

# 15. Degree-of-freedom accounting

The important phase-space distinction is

\[
\text{unrestricted local auxiliary representation}
\neq
\text{causal nonlocal physical theory}.
\]

The unrestricted localization allows arbitrary

\[
(\Phi,\dot\Phi,\lambda,\dot\lambda).
\]

The physical theory instead fixes

\[
\boxed{
\Phi=\Phi[g],
\quad
\lambda=\lambda[g],
\quad
T=T[g].
}
\]

Thus those quantities do not enlarge the freely specifiable physical initial data.

At linear order about Minkowski spacetime, the TT sector contains

\[
\boxed{2}
\]

propagating tensor modes.

The auxiliary fields contribute no independent Cauchy data.

The remaining question for a full nonlinear theorem is whether the complete metric-only equations develop an additional scalar characteristic on a generic curved background. That question is not settled by the localization argument and must be tested directly.

---

# 16. What is actually closed

The following statements are supported by the construction.

### 16.1 Causal response

\[
\boxed{\Phi=\Box^{-1}_{\rm ret}J}
\]

with fixed zero homogeneous data is a well-defined causal response wherever the specified initial-value problem exists.

### 16.2 Auxiliary ghost objection

The negative eigenvalue of the unrestricted localization Hessian is not, by itself, a physical ghost theorem because the auxiliary homogeneous directions are excluded by the causal definition.

### 16.3 Metric-defined foliation

The preferred foliation can be treated as a metric-determined response rather than a dynamical khronon, provided the proper-time foliation remains well-defined.

### 16.4 Linear tensor spectrum

The Minkowski TT sector retains exactly the two standard luminal tensor polarizations.

### 16.5 Weak-field constitutive law

\[
\boxed{\mu(y)=1-e^{-y}}.
\]

---

# 17. What is not yet a theorem

The following claims should **not** be stated as fully proven.

## 17.1 Universal nonlinear two-DOF theorem

A complete nonlinear Dirac-Bergmann or equivalent characteristic analysis has not been carried out for the full causal metric equations on arbitrary backgrounds.

Therefore the statement

\[
N_{\rm propagating}=2
\]

must be restricted to the explicitly tested linearized regime unless a further nonlinear analysis is completed.

## 17.2 Global foliation existence

The equation

\[
g^{\mu\nu}\nabla_\mu T\nabla_\nu T=-1
\]

can cease to define a single global foliation when the normal geodesics from \(\Sigma_0\) form caustics.

The theory therefore requires either a domain restriction or a global continuation/patching prescription.

## 17.3 Full nonlinear scalar stability

The absence of an independent auxiliary scalar does not automatically prove the absence of every possible nonlinear scalar instability encoded in the metric equations. That must be analyzed on representative backgrounds.

---

# 18. Final field-theory specification

The frozen candidate is

\[
\boxed{
\begin{aligned}
U_\mu[g]&=-\nabla_\mu T[g],
\\[1mm]
g^{\mu\nu}\nabla_\mu T[g]\nabla_\nu T[g]&=-1,
\\[1mm]
T[g]|_{\Sigma_0}&=0,
\\[1mm]
J[g]&=R_{\mu\nu}[g]U^\mu[g]U^\nu[g],
\\[1mm]
\Phi[g]&=\Box^{-1}_{\rm ret}J[g],
\\[1mm]
\Phi|_{\Sigma_0}&=0,
\\[1mm]
n^\mu\nabla_\mu\Phi|_{\Sigma_0}&=0,
\\[1mm]
Z[g]&=\frac{4c^4}{a_0^2}\nabla_\mu\Phi[g]\nabla^\mu\Phi[g],
\\[1mm]
F'(Z)&=\frac12e^{-\sqrt Z/2},
\\[1mm]
M[g]&=-F(Z[g]),
\\[1mm]
S_{\rm phys}&=
S_m[g,\psi]
+
\frac{c^3}{16\pi G}
\int d^4x\sqrt{-g}
\left[R-2\Lambda-\frac{a_0^2}{c^4}M[g]\right].
\end{aligned}
}
\]

with metric equation

\[
\boxed{
G_{\mu\nu}+\Lambda g_{\mu\nu}
+\frac{a_0^2}{c^4}\mathcal E^{\rm ret}_{\mu\nu}[g]
=
\frac{8\pi G}{c^4}T_{\mu\nu}.
}
\]

---

# 19. Final closure statement

The strongest defensible conclusion is:

\[
\boxed{
\begin{minipage}{0.90\\linewidth}
The theory can be defined directly as a causal nonlocal metric theory in which the preferred foliation \(T[g]\), the retarded curvature response \(\Phi[g]\), and the adjoint response used in functional differentiation are fixed response functionals rather than independent physical initial-data fields. The negative kinetic direction appearing in an unrestricted local auxiliary representation therefore does not, by itself, establish a physical ghost in the causal theory. Around Minkowski spacetime, the transverse-traceless sector retains the two standard luminal gravitational-wave polarizations, and the weak-field constitutive choice \(F'(Z)=\frac12e^{-\sqrt Z/2}\) produces the exact interpolation \(\mu(y)=1-e^{-y}\).
\end{minipage}
}
\]

The correct research status is therefore

\[
\boxed{
\textbf{Causal nonlocal candidate with the localization-ghost obstruction resolved.}
}
\]

and, at linear order around Minkowski spacetime,

\[
\boxed{
\textbf{two healthy tensor polarizations with }c_T=c.
}
\]

The remaining work required for a stronger claim is a complete nonlinear characteristic/constraint analysis and a global treatment of the metric-defined foliation.

---

# 20. Minimal README claim

A concise statement suitable for a repository README is:

> We define a causal nonlocal metric theory in which the preferred foliation and retarded curvature response are fixed functionals rather than independent auxiliary fields; this removes the physical interpretation of the localization Hessian's negative direction as a ghost, preserves the two luminal TT tensor modes at linear order, and generates the exact weak-field MOND interpolation \(\mu(y)=1-e^{-y}\). A full nonlinear two-DOF theorem remains an open mathematical gate.

