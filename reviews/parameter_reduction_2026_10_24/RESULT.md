# Parameter reduction in the preferred-frame MOND truncation

## Status and scope

The seven displayed EFT coefficients reduce to six physical combinations by an exact field redefinition, then to four on the requested exact deep-MOND surface. The second step is a force-law requirement, not a symmetry derivation. No microscopic amplitude or stable positive gravitational vacuum has been selected. This is a finite-truncation audit, not a count of all parameters in a UV completion.

Campaign status: kappa = 1/2 is FITTED. CFG493 kappa_Lambda = 0.417 +/- 0.095 and kappa_crit = 0.345 +/- 0.078 are separate footings, unused in the computation. No numerical target, fit, scan or second parameter-free observational prediction is claimed. Frozen criteria commit: 4a154a00e7.

## 1. Remove a genuine redundancy

Use c = hbar = 1 and the action from the preceding preferred-frame analysis:

\[
\mathcal L=\frac K2\dot\phi^2-\frac D2(\Delta\phi)^2-a|\nabla\phi|-\frac b2|\nabla\phi|^2-\frac\gamma3|\nabla\phi|^3-q\rho_b\phi-V.
\]

K,D,gamma are positive; q is nonzero and can be made positive by reversing phi. The linear-gradient term is retained because the preceding formal loop calculation generated it. This operator list is not quantum closed.

Set chi = sqrt(K) phi. The six canonical coefficients are

\[
d=D/K,\quad \alpha=a/\sqrt K,\quad\beta=b/K,\quad
\lambda=\gamma/K^{3/2},\quad g=q/\sqrt K,\quad V.
\]

Their exponent map has rank six; its unique continuous kernel is the field-normalization direction. Thus K is not a seventh independent physical input in this truncation. Setting a second canonical coupling to unity would impose a physical restriction, not remove another normalization freedom. Physical units are fixed using the gravitational coupling.

## 2. Impose the requested asymptote, visibly

For s = |grad chi| > 0, the spatial energy is E(s) = alpha s + beta s^2/2 + lambda s^3/3. The static equation is

\[
\nabla\!\cdot[(\alpha/s+\beta+\lambda s)\nabla\chi]-d\Delta^2\chi=g\rho_b.
\]

An isolated spherical cubic-dominated solution has s proportional to 1/r. The alpha and beta contributions to its integrated radial flux grow as r^2 and r, whereas the cubic contribution is constant. Consequently the exact deep-MOND asymptote in this truncation requires alpha = beta = 0. This leaves d, lambda, g, V: four physical coefficients. It does not explain why the two vanished coefficients remain zero under quantum corrections. For a finite MOND interval the appropriate restrictions are instead

\[
|\alpha|/(\lambda s^2)\ll1,\qquad |\beta|/(\lambda s)\ll1.
\]

No numerical bounds follow without specifying the interval and allowed deviations. The asymptotic statement is within the static approximation, not a claim about arbitrarily large radii in a cosmological spacetime.

The spatial Hessian eigenvalues on a nonzero constant-gradient background are

\[
E''(s)=\beta+2\lambda s,\qquad E'(s)/s=\alpha/s+\beta+\lambda s.
\]

Their positivity gives necessary local gradient-health inequalities. On the exact MOND surface both are positive for lambda > 0 and s > 0. The canonical time kinetic term is positive and d > 0 supplies a positive high-momentum k^4 contribution in this scalar model. These facts do not establish gravitational, aether, vacuum or all-orders stability. At s = 0 the two-derivative spatial Hessian degenerates. V > 0 specifies an energy sign, not a stable vacuum solution.

## 3. Isolate what actually controls the desired prediction

With reduced Planck mass defined by 8 pi G = M_Pl^(-2), define

\[
u=gM_{\rm Pl},\quad v=\lambda M_{\rm Pl}^2,\quad
w=dM_{\rm Pl}^2,\quad e=V/M_{\rm Pl}^4.
\]

All four quantities are dimensionless and physically independent in the displayed model. For the same g sourcing the scalar and coupling its force to baryons, cubic dominance gives

\[
a_\phi=g s,\quad \lambda r^2s^2=gm/(4\pi),\quad
 a_\phi^2=a_0Gm/r^2,
\]
\[
\frac{a_0}{M_{\rm Pl}}=\frac{2u^3}{v},\qquad
\kappa\equiv\frac{a_0}{\sqrt{GV}}
=2\sqrt{8\pi}\frac{u^3}{v\sqrt e}.
\]

This matching is conditional on the stated source/force identification and scalar-dominated deep-MOND regime. It is not a new derivation of the amplitude.

The target depends only on R = u^3/(v sqrt(e)); w does not enter its leading coefficient. Its sensitivity is

\[
d\ln\kappa=3d\ln u-d\ln v-\tfrac12d\ln e.
\]

This sharpens the microscopic task: it is unnecessary to fix every coupling separately if a symmetry or dynamics fixes R across all admissible microscopic choices. Merely imposing this tangent relation leaves the value of R arbitrary. Predicting the absolute vacuum scale as well additionally requires selecting e. A measured V must not be used upstream and then described as a predicted vacuum.

## 4. The fourth derivative has a distinct, testable role

It cannot be discarded as a field normalization. For chi = A log(r/r_ref) in n spatial dimensions,

\[
\Delta\chi=A(n-2)/r^2,\qquad
\Delta^2\chi=2A(n-2)(4-n)/r^4.
\]

The integrated fourth-derivative flux is 2d A(n-2)r^(n-4). In three dimensions the cubic flux is lambda A^2 and the extra flux is 2d A/r. With

\[
A=\sqrt{gm/(4\pi\lambda)},\qquad r_D=\frac{2d}{\lambda A},
\]

the ratio of extra to cubic flux on this profile is r_D/r, and r_D scales as m^(-1/2) for fixed coefficients. Thus a controlled cubic regime also needs r_D/r much smaller than one, together with control of omitted operators. This is a residual evaluated on the uncorrected profile, not a solved boundary-value problem or an exact transition radius. Its subleading large-radius behavior cannot cancel the growing alpha and beta fluxes.

## Reduction ledger

| Step | Result | Logical status |
|---|---|---|
| Quotient field normalization | Seven coefficients to six | Exact equivalence within the displayed action |
| Require exact cubic deep-MOND limit | Six to four | Conditional target restriction; protection unresolved |
| Require local health | Positive kinetic and spatial-Hessian domains | Inequalities, not amplitude selection |
| Project onto leading MOND/vacuum ratio | Only R enters kappa | Observable dependence, not another elimination of physical parameters |
| Bound fourth-derivative corrections | r_D/r must be small in the MOND regime | Conditional bound; no numerical data used |

The useful next filter is therefore precise: any proposed completion must preserve alpha = beta = 0, constrain R rather than a removable normalization, and select a healthy positive vacuum scale if it claims an absolute prediction. Extra fields remain possible but bring their own couplings and matching obligations; the four-parameter count cannot be exported to them without redoing the quotient.

## Evidence and limits

Baseline symbolic checks: 22/22 pass. The separate mutation keeps q fixed while rescaling the field; 20/22 pass and the canonical baryon-coupling and force-invariance checks fail as intended, with nonzero process exit. These are algebraic checks, not independent peer review or a UV existence proof. The script uses positive symbols for the generic rank calculation; the zero-coefficient surface is treated separately in the argument above.

Parents: [finite-shell radiative test](../lifshitz_radiative_protection_2026_10_24/RESULT.md), [scalar-vector source audit](../aest_joint_matching_2026_10_24/RESULT.md), and [supersymmetric matching audit](../susy_lifshitz_matching_2026_10_24/RESULT.md). No external theorem is needed for the new algebraic reductions.
