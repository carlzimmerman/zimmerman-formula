# A positive radial spectrum explains a candidate cold breathing mode

The zero-dispersion fluid limit of the identified medium has positive radial restoring energy. Its lowest computed normal mode has period 7.59059 in the dimensionless units used by the live simulation. The finite-A10000 simulation's dominant peak spacings are approximately 7.1–8.3. This is compatible with a cold collective mode; it is not a quantitative mode identification or a damping mechanism.

## Derivation

Retain the spherical identified medium, fixed Plummer baryons, gamma=.01, total medium mass1 and q=m/r². Set R(q)=q²/(1-q). For the zero-dispersion fluid, continuity and acceleration are

    rho_t + (r² rho u)'/r² = 0,
    u_t + u u' = -mu',
    mu' = gNb - R(q) + gamma rho'.

The equilibrium satisfies mu0'=0 inside its free edge. Let xi be the radial Lagrangian displacement and s=r² rho0 xi. Linearized continuity gives delta m=-s, delta q=-s/r² and delta rho=-s'/r². The acceleration perturbation is

    xi_tt = -R'(q0)s/r² + gamma(s'/r²)'.

Thus s(r,t)=s(r) exp(-i omega t) obeys

    -gamma(s'/r²)' + R'(q0)s/r² = omega² s/(r² rho0).

At a regular center xi=O(r), hence s=O(r³). At the free edge rho0=0, a finite displacement has s=0. We restrict to perturbations with finite quadratic integrals and vanishing integration-by-parts boundary term. This excludes unaccounted boundary flux. The moving edge need not have delta rho=0; no rigid-wall density condition has been imposed.

Multiplication by s and integration gives

    omega² = [integral gamma(s')²/r² dr
                   + integral R'(q0)s²/r² dr]
              / integral s²/(r² rho0) dr.

Here R'(q)=q(2-q)/(1-q)²>0 for 0<q<1. The numerator is positive for nonzero admissible s. Equivalently the linear evolution conserves

    E2 = 1/2 integral [s_t²/(r² rho0)
                       + gamma(s')²/r² + R'(q0)s²/r²] dr.

This proves positivity of this radial quadratic form under the stated boundary and regularity assumptions. It does not prove global nonlinear evolution, a complete singular-endpoint spectral theorem, nonspherical stability, or positivity of a different independent-field parent. Linear normal modes in this conservative problem do not acquire a dissipative decay rate from this operator.

## Numerical eigenproblem

An independently solved continuum cold background has free edge R=1.70504833560. Use centered conservative radial differences with positive face coefficient gamma/r_face² and diagonal weight 1/(r² rho0). Transform the generalized symmetric eigenproblem by the square root of this weight. Compute the first32 eigenpairs at 256,512,1024,2048 interior nodes.

| mode | omega, 2048 nodes | period |
|---|---:|---:|
| 1 | .82776006 | 7.59058769 |
| 2 | 1.04652123 | 6.00387753 |
| 3 | 1.21988059 | 5.15065603 |
| 4 | 1.37911884 | 4.55594191 |
| 5 | 1.53022923 | 4.10604189 |
| 6 | 1.67541944 | 3.75021631 |

The lowest period changes from7.58963 at256 nodes to7.59059 at2048. The first-six frequencies change by less than7e-6 relatively between1024 and2048 nodes. The separately evaluated discrete Rayleigh quotient agrees to better than1e-10 relatively. These checks verify this discretization, not all continuum spectral properties.

A radial dilation has s0 proportional to r³ rho0. Its squared projections in the kinetic inner product onto the first six modes are approximately46.05%,23.18%,11.66%,7.19%,4.55%,2.99%. These are displacement-norm fractions, not energy fractions. Thirty-two modes capture essentially all of that discrete norm. The dilation excites several modes, so beating and nonuniform peak spacing are expected even in the linear limit.

## Comparison and implication

The previously saved finite-A cold runs give prominent peak spacings7.7,8.2,7.2 at256 nodes and7.65,8.25,7.10 at512 nodes. The lowest cold-fluid period is on that scale without fitting a frequency. However, finite A, kinetic anisotropic stress, finite amplitude and particle-mesh errors differ from this exact zero-dispersion model. Those differences prohibit treating the comparison as a successful parameter-free waveform prediction. The earlier failed finite-difference force gate remains recorded and is not erased by the present spectrum checks.

This narrows the mechanism question. A positive restoring force can support a long-lived halo-like configuration while also preserving radial ringing. Stability alone does not select a final state or dissipate the oscillation energy. A proposed completion must derive energy transfer to additional degrees of freedom, or demonstrate genuine kinetic dephasing at the relevant cold occupation, while preserving the desired static law. The independent-field radiation calculation in this folder cannot be imported into the identified-medium theory without a consistent coupling and conservation law.

The bounded audit cold_spectrum_run has4 passing checks and a valid completed manifest; original live trajectories were inputs, not rerun inside the audit. The analytic derivation and interpretation are self-reviewed. Novelty and a full dynamical parent remain unestablished.
