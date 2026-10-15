# Independent audit of the subcritical stiff-core branch

VC3-STIFF-AUDIT-001, 15 October 2026. Independent reconstruction of the
existence and radial-energy argument, with read-only inspection of the frozen
proof, amendment and computation. This audit is the reviewer's only edit here.
It is another agent's derivation in the same model/tool environment, not
external peer review or a formal proof certificate.

**Verdict: correct as a qualitative sufficiently-small theorem for the stated
new hybrid continuum model, with the amendment's parameter, chemical and
free-boundary qualifications.** This is an actual dynamical two-species branch,
not the earlier held-source equilibrium. Its subcritical charge and stiffer
charged EOS are changed inputs. The listed finite numerical example is not
interval-certified and is not a quantified member supplied by the analytic
existence theorem.

## 1. Exact audited revisions

| Artifact | SHA256 |
|---|---|
| `PROOF.md` | `4cc70fb29778cfd3ec9e2c14fc2e9c5ef561e18074e10787bd8ba9aeeab177fb` |
| `AMENDMENT.md` | `b927f0f7d0d1fb7523c8efabc62824f4e9aae2521368da0b8773dfb19d2a423c` |
| `check_stiff_core.py` | `ae19ac8832fc5cd1aaa692c72702d61792691f8e7b1b24b344764f4132a8522e` |
| `run_v2/manifest.json` | `733e2b1aff433aa84e31f97f0405c7e33a5e84a3f8d5dd918e7c19b52969f716` |

The v2 manifest validates against actual input/output bytes. Its authoritative
software correction is explicitly recorded. No new simulation or enlargement
of the numerical sample was necessary for this audit.

## 2. Normalize the claim before using the sample

Fix `0<alpha=b_q^2<1`, charged functional EOS `P_c=K rho_c^2` and neutral
functional EOS `P_s=K_s rho_s^(6/5)`. Each member has separately conserved
charged and neutral currents and its own fixed constants. The family varies
the chosen constants/central density through the displayed dimensionless
parameters. It does not vary all parameters independently while silently
holding a single pair `(K,K_s)` fixed.

Poisson gravity sources the two rest densities. Gauge/internal energy and
relativistic stresses are not added to that source. The material frame is
varied with both currents. At a static co-moving electric state its first
variation vanishes, so the displayed coupled hydrostatic/Gauss equations
follow. The neutral chemical potential normalization makes its specific
enthalpy equal to `-Phi`, giving the finite-mass n=5 tail equation.

The assertion is: for each fixed alpha there exists a sufficiently small
positive parameter neighborhood containing actual matched equilibria, and a
smaller neighborhood where the radial form is positive. It does not give an
explicit smallness threshold or certify that the computed `alpha=.5,
delta=10^-6,eta=.001` point lies in that rigorous neighborhood.

## 3. Actual finite-mass exterior, not an assigned tail

With enclosed total mass m_R at radius R, direct integration of the exterior
Poisson and neutral hydrostatic equations gives the integral map (2). After
scaling to z=t/R and psi=(m_R/R)Z, the coefficient is exactly
`2mu=delta*m_R^4/R^2`. It is not a missing or extra factor two.

For `1/z<=Z<=C/z`, the map's weighted excess is bounded by `mu*C^5` and
its derivative norm by `5mu*C^4`. The self-map and contraction conditions
in the proof therefore suffice. The total exterior mass increment is
between `mu*m_R` and `mu*C^5*m_R`. The first iterate is independently
obtained as

\[
 Z_1=(1+\mu)/z-\mu/(3z^3),
\]

which agrees with both the edge and asymptotic-mass controls in the code.
The positive n=5 tail has finite rest mass and potential zero at infinity.

C1 parameter dependence is also justified. The normalized operator acts on
the fixed weighted space, has uniformly invertible `I-DT` by its convergent
Neumann series, and has a bounded quadratic remainder because `Z^3 dZ^2`
has the same inverse-fifth-power decay. Restoring m_R/R and mu is smooth.
At delta=0 one may work with a local open positive-function ball, or use the
one-sided positive-delta differentiability actually needed by the scalar
contraction. An unproved infinite-domain shooting theorem is not being
substituted for this construction.

## 4. Interior and moving charged radius really match this exterior

At the auxiliary base, `k=sqrt(1-alpha)`, the independently checked solution
has `theta=sin(kt)/(kt)`, first zero `R0=pi/k`, charged mass `pi/k^3`, and
`psi=(1+theta)/k^2`. Its zero slope is `-k/pi`, strictly nonzero.

Near the center `m_a=O(t^3)` removes the apparent `1/t^2` singularities.
The field ratio x is O(eta*t), with a strict margin from its pole. The
integral equations consequently give local parameter-dependent solutions;
ordinary continuation on a compact interval away from zero reaches the
transverse core zero. Positivity on earlier compact subintervals and the
nonzero edge slope ensure this remains the first zero. The radius and
enclosed masses are C1; their values have not been frozen at the base.

At delta=eta=0 the interior theta and masses are independent of psi_c. The
interior potential at its edge is `psi_c-1/k^2`, while the exterior value
is `m_R/R=1/k^2`. Thus the true mismatch is

\[
 F(\psi_c,0,0)=\psi_c-2/k^2,\qquad F_{\psi_c}=1.
\]

The proof's scalar contraction follows from C1 continuity and this nonzero
derivative. It adjusts the actual central potential and the actual radius
simultaneously with the neutral exterior. The two potential values match,
and their derivatives both equal `-m_R/R^2`; there is no hidden surface mass
or externally imposed pressure. This is the required existence implication.

The zero-neutral base is only an auxiliary ODE limit: its missing exterior
material frame is not declared a physical vacuum action. Every asserted
positive-delta member has positive neutral density at every finite radius.

## 5. Full radial form and its constrained free-boundary domain

For charged/neutral mass tangents u,v, the internal Hessians, Poisson Green
energy and Gauss electric Hessian give the displayed equation (5). The
electric coefficient `(1-x)^-2>=1` cancels at least alpha of the charged
self-gravity. Both the neutral/core gravitational cross term and the
nonlinear electric Hessian are retained.

Core mass conservation gives `u=0` outside its edge. Work first with regular
mass-preserving displacements of finite inertia and the zero-density,
zero-pressure charged edge, then take their finite-energy form closure.
The charged tangent has `u(0)=u(L)=0`. For z=u/r,

\[
 \int_0^L u'^2/r^2
 =\int_0^L[z'^2+2z^2/r^2]
 \ge(\pi^2+2)L^{-2}\int_0^L z^2.
\]

The integration-by-parts boundary term vanishes in this domain. The
Dirichlet bound follows from the explicit completed square in the proof;
`2/r^2>=2/L^2` supplies the other term. This correctly gives the strictly
positive base margin `kappa=2/pi^2` and, by actual-radius continuity, a
nearby core margin. It does not rely on a finite homology matrix.

The amendment's chemical qualification is essential. The charged first
integral is a constant lambda_c that need not be zero. The Hessian is that
of `E-lambda_c*M_c` on independently mass-conserving paths; the second-order
path terms proportional to lambda_c cancel. At the base the dimensionless
constant is -1. A zero charged surface density and pressure leave no extra
quadratic surface work on the declared form domain. This is not a general
nonlinear physical-vacuum free-boundary theorem.

For the neutral fluid, the positive Newton kernel and weighted square
inequality give

\[
 G\int v^2/r^2\le5\sup_r[(-\Phi_s)/(-\Phi)]U_s=q_sU_s.
\]

This is the actual neutral self-potential. On the interior, its central
potential is O(delta) while the core potential has a positive uniform lower
bound. In the exterior, total neutral mass is O(delta) by the contraction,
and `-Phi_s(r)<=G*M_s/r`, whereas `-Phi_c=G*M_c/r`. Therefore q_s tends to
zero uniformly, not just at each radius separately. The gravitational cross
term is at most `2sqrt(G*q_s*I_u*U_s)`. The resulting two-variable form is
strictly positive exactly under the proof's sufficient Schur conditions.
Their base limits have q_s=0 and kappa=2/pi^2, so they hold for a sufficiently
small positive matched subbranch.

This proves a positive radial density/Gauss form in its compressibility/core
norms and positive conserved comparison energy for suitable linear solutions.
The noncompact neutral tail does not supply a uniform inertial frequency gap.
No full spectral-domain, free-boundary PDE or all-angular theorem is inferred.

## 6. Principal gate and finite numerical evidence are separate claims

For these actual EOSs, the effective inertias are exactly
`rho_c*c^2` and `rho_s*c^2+24P_s/5`. The harmonic current-frame formula then
gives `h_* >= (rho_c+rho_s)c^2`. The field normalization in equation (10)
checks directly. For a fixed positive-delta member its spatial coefficient
vanishes at the center, stays finite at the charged edge, and decays at
infinity; choosing epsilon sufficiently small therefore supplies the local
gate. This choice is allowed by the displayed reparameterization of K,
rho_* and K_s. It is a family of chosen continuum inputs. It is not an
automatic gate for a low-density sequence at one arbitrarily fixed EOS pair.

The bounded run has 15 exact reduction checks and DOP853 shooting at outer
radii 100,200,400. The base benchmark and changing outer radius are useful
implementation controls. The analytic first-Picard tail error is conditional
on its supplied ODE state; it does not bound the non-interval ODE error or
prove the reported sample's Schur margin. The central start is nonzero and
uses a truncated regular-center series; the sample field maximum is sampled,
not uniform. The labels in the output correctly preserve these limits.

No new numerical experiment was needed to establish the uniform implications
in sections 3--5. They are analytic reductions and estimates, with exact
base constants checked by the existing bounded run.

## 7. Exact remaining implication

This is an actual finite-mass, self-consistent, dynamical charged/neutral
equilibrium branch with positive radial density/Gauss energy in a specified
Newtonian rest-mass-gravity model. It changes the critical charge ratio and
the soft inverse EOS that failed earlier. The result must not be substituted
into the old critical-charge galaxy law.

The charged free-boundary evolution, all nonradial/gauge sectors, magnetic
backgrounds, tail/vacuum action, microscopic EOS and species selection,
production and abundance, full metric constraints, formation and observational
predictions remain separate obligations. The fixed-core sharp-interface
control is a different model and cannot be spliced onto this branch without
solving a new coupled equilibrium and energy problem.
