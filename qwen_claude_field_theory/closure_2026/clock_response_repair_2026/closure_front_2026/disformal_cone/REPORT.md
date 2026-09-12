# The L215 matter-metric repair has a second gate

Status: **conditional obstruction, not full-theory closure**. Base research
checkpoint `bba135b36`; proposal audited in `bde5bfd2c` and PAPER24 in
`96512fc6e`. This note does not change any coefficient function or action.

## What is varied, and what stays fixed

Keep the Einstein + first-derivative clock/scalar + constant cubic action in
`../principal_gate/REPORT.md`. Replace the matter metric only by

\[
\widetilde g_{\mu\nu}=C g_{\mu\nu}+D n_\mu n_\nu,
\qquad g^{\mu\nu}n_\mu n_\nu=-1,\quad C>0, C-D>0.
\]

The existing independent `../boosted/tensor_cone.py` derives the Einstein
tensor principal action on the homogeneous aligned background, including the
absence of a tensor-kinetic contribution from the constant cubic operator:

\[
S_T^{(2)}=\frac{M^2}{8}\int dt\,d^3x\,a^3
\left[\dot h_{ij}^2-a^{-2}(\partial_kh_{ij})^2\right].
\]

First-derivative scalar terms do not add tensor principal derivatives there.
The calculation is rerun, not presumed to establish arbitrary inhomogeneous
characteristics. Adding a matter metric with no metric derivatives does not
by itself replace this homogeneous gravitational principal action.

Independently vary the transverse Maxwell action
\(S_\gamma=-\tfrac14\int\sqrt{-\widetilde g}\,F_{\mu\nu}F^{\mu\nu}\).
In a local clock-rest orthonormal frame, write \(L=C-D>0\). Direct contraction
and differentiation give

\[
\mathcal L_\gamma^{(2)}=
\frac12\sqrt{\frac C L}\,\dot A_x^2
-\frac12\sqrt{\frac L C}\,(\partial_z A_x)^2,
\quad
\boxed{\frac{c_\gamma^2}{c_T^2}=\frac{C-D}{C}}.
\]

The Euler–Lagrange principal equation therefore has the displayed speed ratio;
the independently inverted physical metric gives the same dispersion relation.
In physical matter units \(c_T^2/c_\gamma^2=C/(C-D)\), not one when \(D\ne0\).
Positive Maxwell kinetic and gradient coefficients follow from the stated
metric domain; metric degeneracy is not a repair.

## Alignment cannot identify distinct cones

For every nonzero tangent vector \(k\) null with respect to \(g\),

\[
\widetilde g(k,k)=D(n\cdot k)^2.
\]

A timelike unit covector has nonzero contraction with a nonzero null vector:
in its rest frame the contraction is \(-k^0\), and the null equation implies
\((k^0)^2=|\mathbf k|^2>0\). Hence the two cones coincide iff \(D=0\).
This is a tensorial statement, unchanged by a boost. Exact rational boost
controls also include **perfect alignment**, which still gives a nonzero norm
when \(D\ne0\). Clock dragging may affect preferred-frame fields but cannot
remove this cone mismatch while retaining the same two principal metrics.

## No-slip and cone equality are incompatible with this shift-only repair

At first order set \(C=1+2c\varphi\), \(D=2d\varphi\). Expand both metric
components separately with a static aligned clock. The result is

\[
\delta\widetilde\Phi=(c-d)\varphi,
\qquad \delta\widetilde\Psi=-c\varphi,
\qquad \delta(c_\gamma^2/c_T^2)=-2d\varphi.
\]

If the original potentials already obey \(\Phi=\Psi\), equal scalar shifts
require \(d=2c\). Common cones through this order require \(d=0\).
Consequently **both conditions force \(c=d=0\)**: no nonzero leading scalar
shift from this matter-metric mechanism. The baseline no-slip and unchanged
tensor-cone assumptions matter. This is not a theorem excluding actions with
different gravitational principal operators or independently derived baseline
anisotropic stress.

For L215, \(c=-1,d=-2\), so

\[
\widetilde\Phi=\Phi+\varphi,\quad
\widetilde\Psi=\Psi+\varphi,\quad
\boxed{c_\gamma^2/c_T^2=1+4\varphi+O(\varphi^2)}.
\]

The quoted metric is only specified to first order: no exact all-order L215
factor is inferred. The exact cone theorem above applies to any specified
nondegenerate \(C,D\). If \(D=0\) only at a particular background point, this
does not guarantee equality along a nontrivial scalar profile.

Thus the L215 **nonzero disformal shift + unchanged tensor-cone shortcut fails
the exact common-cone gate** wherever its hypotheses hold. It has not reduced
the full theory to one clock-alignment number. A quantitative observational
exclusion additionally requires a propagation profile and emission assumptions;
we do not translate this pointwise result into a universal GW170817 bound.

## Known antecedent, not a claimed novel theorem

Bekenstein's TeVeS paper, equations (21)–(24), gives the exact comparison metric
\(C=e^{-2\varphi}\), \(D=-2\sinh(2\varphi)\), whose ratio here is
\(e^{4\varphi}\). Its section VIII also distinguishes the wave cones. This
illustrates the mechanism; it is not a proposed completion of the clock action.
[Bekenstein, arXiv:astro-ph/0403694v6](https://arxiv.org/html/astro-ph/0403694v6).
Disformal photon-coupling constraints following GW170817 were also studied by
[Sakstein and Jain, arXiv:1710.05893v3](https://arxiv.org/abs/1710.05893v3).
Search scope: these two primary sources, checked 2026-09-12, plus the local
L215 and earlier clock-timing/tensor calculations. No global novelty claim.

## Certification scope

`derive_cone.py`: 34 exact symbolic/control checks. `test_cone.py` exercises
Maxwell normalization, unequal-cone and conformal/disformal sign controls; its
initial missing-implementation assertion failed before implementation.
`DisformalCone.lean`: five real-algebra statements, with all hypotheses
explicit. It does **not** formalize Maxwell variation, Lorentz geometry,
gravitational DOF, full PPN, observational inference, or the whole theory.
The first-order no-slip/common-cone implication and the rest-frame null-ray
obstruction are formally proved, not inserted as axioms.
