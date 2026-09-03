# Exact exponential MOND: inverse correction and twelve observational channels

## Executive result

The historical hunt kernel
\[
\nu_{\rm RA}(x)={1\over1-e^{-\sqrt{x}}},
\qquad x={g_N\over a_0},
\]
is **not** the inverse of the target law
\[
\mu(y)=1-e^{-y},
\qquad y={g\over a_0}.
\]
The target circular/spherical relation instead requires the unique implicit
inverse
\[
x=y(1-e^{-y}),
\qquad \nu_{\rm exact}(x)={y(x)\over x}.
\]
The Route-A acceleration is high relative to the exact target by 2.445% at
\(x=0.01\), 7.301% at \(x=0.1\), 17.186% at \(x=1\), and 4.415% at
\(x=10\). Therefore a result calculated with `hunt_lib.nu` is not, without a
fresh rerun, a result for the specified exact \(\mu\).

The executable `exact_exponential_mu_2026.py` implements the monotone inverse
without replacing \(y\) by \(\sqrt{x}\), tests it across 22 decades, derives
the low-acceleration series, and records twelve distinct observational
channels. They are not twelve mathematically independent laws: the executable
dependency graph records which channels are derivatives or pipelines. Most
rows require the AQUAL field equation, while lensing additionally needs a
relativistic metric rule. They are not predictions of a closed relativistic
action.

## Exact kernel facts

The action primitive and constitutive eigenvalues are
\[
G(y)=y^2+2(1+y)e^{-y}-2,
\qquad {G'(y)\over2y}=1-e^{-y},
\]
\[
\lambda_\perp=1-e^{-y},
\qquad
\lambda_\parallel=1+(y-1)e^{-y}.
\]
Both eigenvalues are positive for \(y>0\) and vanish at \(y=0\). For
\(0<y\le1\), \(d\lambda_\parallel/dy=(2-y)e^{-y}>0\); for \(y\ge1\),
\(\lambda_\parallel=1+(y-1)e^{-y}\ge1\). This proves uniqueness of the
implicit inverse away from the degenerate endpoint.

Coefficient matching, rather than an assumed deep-MOND ansatz, gives
\[
y(x)=\sqrt{x}+{1\over4}x+{7\over96}x^{3/2}+O(x^2),
\]
so
\[
g=\sqrt{a_0g_N}+{1\over4}g_N
+{7\over96}{g_N^{3/2}\over\sqrt{a_0}}+\cdots.
\]
At high acceleration, \(y=x[1+O(e^{-x})]\).

## Twelve scoped channels

“Exact-kernel” below uses only the implicit force map. “Conditional AQUAL”
also assumes
\[
\nabla\!\cdot[\mu(|\nabla\Phi|/a_0)\nabla\Phi]=4\pi G\rho_b.
\]
“Conditional no slip” additionally assumes the same relativistic action
derives \(\Phi=\Psi\). A dependency such as `2 <- 1` means channel 2 is a
differential consequence of channel 1, not new independent theoretical
content. The distinctions prevent circular phenomenology from being sold as
a full field theory.

| # | Equation / observable | Honest scope | Dependency |
|---:|---|---|---|
| 1 | \(x=y(1-e^{-y}),\ g=a_0y(x)\): resolved RAR | Exact for spherical AQUAL; circular MI only if separately postulated; generic AQUAL discs can have a curl field | base |
| 2 | \(d\ln g/d\ln r=-2/(1+L)\), \(d\ln v_c/d\ln r=(L-1)/[2(1+L)]\): exterior slope | Exterior point mass; for extended spherical mass replace \(-2\) by \(d\ln M/d\ln r-2\) | `2 <- 1` |
| 3 | \(\kappa^2/\Omega^2=(1+3L)/(1+L)\), \(\Delta\varpi=2\pi(\Omega/\kappa-1)\): near-circular precession | Isolated exterior test particle, not a comparable-mass or EFE-dominated orbit | `3 <- 2` |
| 4 | \(\langle v^2\rangle_M=(2/3)\sqrt{GMa_0}[1-\sum_i(m_i/M)^{3/2}]\); \(\sigma_{\rm los}^4=(4/81)GMa_0[1-\sum_i(m_i/M)^{3/2}]^2\) | Deep, isolated, global, spherical, nonrotating virial identity; simple coefficient is the continuum limit | base deep-AQUAL identity |
| 5 | \(\sigma_r^2=[nf_\beta]^{-1}\int_r^\infty nf_\beta g\,ds\): resolved Jeans profile | Generic Jeans pipeline requiring boundary condition, tracer density, anisotropy and LOS projection | `5 <- 1 + dynamics inputs` |
| 6 | \(\partial_i[(\lambda_\perp P^\perp_{ij}+\lambda_\parallel n_in_j)\partial_j\delta\Phi]=4\pi G\delta\rho\): response anisotropy | Linearized AQUAL only at \(y>0\); the operator has rank zero at \(y=0\) | base multidimensional operator |
| 7 | \(\phi=-GM[\mu_e\sqrt{1+L_e}]^{-1}(R_\perp^2+z^2/(1+L_e))^{-1/2}\): EFE Green shape | Uniform \(y_e>0\), internal field \(\ll g_e\); lensing needs a metric completion | `7 <- 6` |
| 8 | \(r_{\rm EFE}\sim\sqrt{GMa_0}/g_e\), \(v_{\rm esc}^2=2\sqrt{GMa_0}[\ln(r_{\rm EFE}/r)+C(\theta;y_e)]\) | Asymptotic matching estimate; \(C\) and escape surface require the full outer BVP | `8 <- 1 + 7` |
| 9 | \(Q_{ij}=Q_2(e_ie_j-\delta_{ij}/3)\), \(|Q_2|=(3/2)(a_0/r_M)|q|\) for \(q=Q_{zz}r_M/a_0\) | Full nonspherical BVP; AQUAL and QUMOND \(q\) are not interchangeable | `9 <- full BVP` |
| 10 | \(\Delta\gamma_t[\rho_1,\rho_2]\not\equiv0\) generically: pair-minus-sum lensing | Proposed nonlinear functional; it vanishes in Newtonian/infinite-separation/trivial limits and needs a specified geometry | `10 <- nonlinear operator + metric` |
| 11 | \(\mathbf g_{\rm lens}=-\nabla(\Phi+\Psi)/2=-\nabla\Phi\); \(\hat\alpha_{\rm deep}(b;R)=4\sqrt{GMa_0}c^{-2}\tan^{-1}(\sqrt{R^2-b^2}/b)\) | Physical no-slip metric; \(2\pi\sqrt{GMa_0}/c^2\) is the \(b/R\to0\) limit | `11 <- 1 + no slip` |
| 12 | \(z_{1\to2}=[\Phi(r_2)-\Phi(r_1)]/c^2=\sqrt{GMa_0}c^{-2}\ln(r_2/r_1)\) | Both radii in the exterior deep pre-EFE region; AQUAL \(\Phi\) must be the physical lapse; no slip is unnecessary | `12 <- 1 + physical lapse` |

These are distinct observational channels, not twelve independent equations.
BTFR, dark
fraction, mass discrepancy, phantom enclosed mass, phantom surface density,
and Bosma-type ratios are deliberately excluded because they are
reparameterizations of row 1. Constant deep-MOND deflection is row 2 plus row
11, not an independent law.

## Strict action fork: modified inertia is outside the stated matter action

For the required action form
\[
S=S_{\rm grav}[g,\ldots]+S_m[g,\psi]
\]
with ordinary matter minimally coupled to one physical metric, separate
diffeomorphism invariance of \(S_m\) gives, on the matter equations,
\[
\nabla_\mu T_m^{\mu\nu}=0.
\]
The point-particle limit is
\[
S_{\rm pp}=-mc\int ds,
\qquad u^\mu\nabla_\mu u^\nu=0,
\]
and hence \(\ddot{\mathbf x}=-\nabla\Phi\) in the weak field. A genuine
modified-inertia equation \(\mu(|\mathbf a|/a_0)\mathbf a=\mathbf g_N\)
requires an acceleration/history-dependent matter action or a nonmetric
force. That relaxes the stated minimal-matter/ordinary-Ward gate.

Therefore the strict fried-chicken target cannot use modified inertia as an
escape hatch. Its exact MOND law must be generated by the gravitational field
equations. Circular data alone still cannot distinguish the two descriptions,
but the action specification can.

## Current empirical interpretation

- Historical Route-A hunts must be labeled Route A, not exact exponential
  \(\mu\). They remain useful tests of that empirical kernel.
- The warning-free exact-target **QUMOND** Cassini integral gives
  (q=0.1658550424134), (Q_2=1.9562\times10^{-26}\,\mathrm{s^{-2}}), or
  3.762 times the Park ceiling on the canonical footing. Recomputing the
  dimensionless external field for the alternate footing gives
  (q=0.1654309216068), (Q_2=2.5802\times10^{-26}\,\mathrm{s^{-2}}), or
  4.962 times the ceiling. Independent split quadrature and a tail bound
  reproduce both. The repository's quoted “AQUAL” factors 4.643/6.125 were a
  calibrated QUMOND rescaling, not a direct nonlinear AQUAL solution. A
  direct finite-volume AQUAL pilot remains adverse near 4.05 times the
  ceiling, but its inner-boundary and fit-window convergence certificate is
  still owed.
- The cleanest live positive measurements are the external-field lensing
  quadrupole, directional rotation-curve dipole, and preregistered wide-binary
  anisotropy. Their exact kernel conventions differ and must not be merged
  without explicit translation.

## Status

**Kernel inverse: CLOSED and executable. Twelve scoped observational channels:
DEFINED with dependencies. Bankable analytic subset: 1, 2, 3, 4, 6, 7 and
the regime-limited parts of 11 and 12. Twelve independent Kepler-grade laws:
not established. Predictions from one fully closed relativistic action: still
OPEN.** Channels 5, 8, 9, and 10 require additional boundary data or an actual
BVP before they yield a number.
