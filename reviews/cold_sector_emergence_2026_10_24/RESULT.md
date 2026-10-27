# Cold-sector emergence: checkpoint COLD-20261024-A

Base revision: `f747c7a9730b78f5958ad26fea58f21576add8e3`. Owner: current Codex chat. Date: 2026-10-24.
Original objective remains OPEN: find a conserving, dynamically selecting cold-sector mechanism that recovers the galaxy relation and the dark-energy normalization, without retaining a second full galaxy boost. This checkpoint supplies equilibria and scoped obstructions, not that mechanism. Review provenance: self-review only; no novelty claim. Existing canonical statements are not edited.

## Target contract

Use the headline square-root law `g^2=b^2+a0*b`, not the inequivalent simple-mu law. Work first in spherical weak-field gravity, with nonnegative gravitating cold mass, `g=b+g_c`. The scale relation `a0=kappa*c*sqrt(G*rho_Lambda)` and kappa=1/2 remain hypotheses. A mechanism must predict the cold distribution from dynamics and initial data, track reciprocal energy/momentum exchange, avoid double counting, and address finite halos and cosmology. Selecting initial conditions to be the desired equilibrium is not success.

Nearest earlier work: `campaign_fresh_gravity/CFG44_fluid_target/README.md`, `campaign_fresh_gravity/CFG643_baryon_heat_exchange/README.md`, `rebuild_2026_10_22/X6_dust_coupling/README.md`, and `covariant_push_2026_10_22/V3S_FINAL_VERDICT_2026-10-24.md`. CFG44 already obtains the point-halo Jeans pressure; the result added here is an explicit positive phase-space realization and an all-parameter Plummer positivity certificate. CFG643 closes a particular heating construction under its declared assumptions; it is not a theorem against every possible energy-exchange mechanism.

## R1: a positive collisionless realization exists

### Point baryons: exact analytic result

Set `G=M_b=a0=1`, so radius is in units `sqrt(G*M_b/a0)` and potential in units `sqrt(G*M_b*a0)`. For r>0 define

```
M_c(r) = sqrt(1+r^2)-1
g(r)   = sqrt(1+r^2)/r^2
rho(r) = 1/[4*pi*r*sqrt(1+r^2)]
Phi(r) = asinh(r)-sqrt(1+r^2)/r
P(r)   = 1/(8*pi*r^2)
u(r)   = P/rho = sqrt(1+r^2)/(2*r).
```

Direct differentiation gives `Phi'=g`, `(r^2*g)'=4*pi*r^2*rho` away from the central point mass, and `P'=-rho*g`. Crucially,

```
d rho/d Phi = -(2*r^2+1)/[4*pi*(1+r^2)^2]
d^2 rho/d Phi^2 = r^5/[pi*(1+r^2)^(7/2)] > 0.
```

For specific energy `E=v^2/2+Phi`, define a mass distribution in phase space

```
f(E) = 1/(sqrt(8)*pi^2) * integral_E^infinity rho''(q)/sqrt(q-E) dq.
```

The integrand is positive. It is locally integrable at its lower endpoint and decays at infinity. Thus f(E)>0 for every finite E. The potential covers the full real line.

This is a stationary collisionless solution because E is conserved in the static potential. To prove that it actually reconstructs the source density, substitute into

```
rho_f(Phi) = 4*pi*sqrt(2) integral_Phi^infinity f(E)*sqrt(E-Phi) dE.
```

Positivity permits exchanging the integrations. The inner integral is
`integral_Phi^q sqrt(E-Phi)/sqrt(q-E) dE = pi*(q-Phi)/2`.
Consequently `rho_f=integral_Phi^infinity (q-Phi)*rho''(q)dq=rho(Phi)`; the integration-by-parts boundary terms vanish because rho and q*rho' decay at large positive potential. This is the full analytic implication, rather than a sampling argument.

**Scope:** fixed point baryons, an infinite idealized halo, no Lambda force in the local equations. The halo has divergent total mass. Near the central point its dispersion diverges; it is not a relativistic black-hole solution. No stability theorem is claimed. Indeed sampled f(E) first rises then falls, so a usual monotonic-distribution sufficient stability criterion cannot simply be invoked.

### Extended Plummer baryons: exact positivity certificate

Set `G=a0=Plummer radius=1`; allow any baryonic mass A>0. Write

```
b = A*r/(1+r^2)^(3/2), g=sqrt(b^2+b), g_c=g-b
rho_c = [(g_c)'+2*g_c/r]/(4*pi)
z = r^2/(1+r^2), q = sqrt(b/(1+b)), 0<z,q<1
F0 = A/[4*pi*(1+r^2)^(3/2)]
R = (1-q)*(5-q-3*z+3*z*q)/(2*q)
rho_c = F0*R.
```

All factors in rho_c are positive. Set

```
D = 2*z*(1-z)*partial_z + q*(1-q^2)*(1-3*z)*partial_q/2
A1 = D(R)-3*z*R
B = D(A1)-3*z*A1 - [1+(1-3*z)*(1+q^2)/2]*A1.
```

Since D is d/dlog(r), direct chain rules give
`d^2 rho_c/dPhi^2 = F0*B/(r^2*g^2)`.
The polynomial `p=8*q*B/(1-q)` has the following exact coefficients in the tensor Bernstein basis of degrees (3,5), with rows indexed by the z degree:

```
20    24      144/5   176/5   216/5   48
20    28      174/5   186/5   168/5   32
80    56      172/5   108/5   104/5   16
32    192/5   192/5   128/5   0       0
```

Every basis function is positive in the open unit square; coefficients are nonnegative and not all zero. Hence p>0, B>0 and rho_c''(Phi)>0 for all r,A>0. `plummer_certificate.py` exactly reconstructs the polynomial and cross-checks the density factor against spherical Poisson. The same Abel construction proves a nonnegative isotropic stationary distribution for every positive Plummer mass and scale radius, on accessible energies above the finite central potential. At large radius rho decays as r^-2 and Phi grows logarithmically, so the required outer boundary terms vanish. The central cold density is singular, approximately r^-1/2, even though the baryonic density is cored; no bounded primordial phase-space-density claim is made.

This is an existence result. It is not an attractor or finite-mass result, and Plummer spheres are not galactic discs.

### Checks actually run

The point-halo run checks six exact symbolic identities, positive f at seven energies, and direct velocity-integral reconstruction of rho at r=0.1,1,10. Largest observed reconstruction discrepancy is 6.2e-14; declared acceptance tolerance was 2e-5, and this is floating quadrature, not a precision certificate. A separate finite mass/radius identity was checked at 27 points. All assertions passed.

The extended screen evaluates 17 masses A in [1e-4,1e4] and 1601 radii in [1e-4,1e4]: all 27217 points have positive density, decreasing radial density and positive potential curvature. This finite evidence is superseded for curvature sign by the exact Bernstein certificate. Three bounded-run manifests record code hashes, versions, execution limits and completed status.

## R2: the elementary heat-conduction closure does not maintain this exact halo

For the point solution above, adopt the explicitly assumed positive conductivity `k_h=rho*r*sqrt(u)` and conductive flux `q_r=-k_h*u'`. A constant positive multiplicative conductivity coefficient changes no signs. The outward luminosity is

```
L(r)=4*pi*r^2*q_r=sqrt(2)/[4*sqrt(r)*(1+r^2)^(3/4)]
L'(r)=-sqrt(2)*(4*r^2+1)/[8*r^(3/2)*(1+r^2)^(7/4)] < 0.
```

A steady, static, source-free exterior requires L'=0. A point baryonic source has rho_b=0 at every r>0, so purely local baryon collisions cannot supply the spatially distributed sink required by this L'<0 profile. This refutes **that exact profile + that conductivity + local baryon-only exchange + static equilibrium**. It does not refute finite-range approximate rotation curves, anisotropic/orbit-mediated transport, advective energy flux, a different conductivity or a formation-era interaction that later switches off. Such changes require new dynamics rather than reusing this derivation unchanged.

Source check, 2026-10-24: Famaey–Khoury–Penco, arXiv:1712.01316v2, primary HTML, equations 3.19, 4.1, 5.8 and section 6.3. The paper assumes an interaction normalization and treats baryons as fixed input; its stability check does not establish general formation. Its section 11 toy model is explicitly not phenomenologically viable. Therefore the paper is adjacent prior art, not a verified completion of this framework. https://arxiv.org/html/1712.01316v2

The opposite-sign heating route is also not fresh: CFG643 records energy-budget and formation-sign failures for its native setup. The follow-up primary source arXiv:1912.07626v2 was located, but no complete model reproduction is claimed here. https://arxiv.org/html/1912.07626v2

## R3: mass accounting and dark-energy boundary conditions do not select the scale

For the exact point-baryon law inside a radius R,

```
M_c(R)=M_b*(sqrt(1+a_star*R^2/(G*M_b))-1)
a_star=G*M_c(R)*(M_c(R)+2*M_b)/(M_b*R^2).
```

This makes the missing selection rule explicit. Cold inventory and boundary radius select an effective acceleration unless an additional relation ties them to the vacuum. A number-conserving closed model cannot send two different total cold inventories to the same full density profile. An inner attractor remains possible if an outer reservoir carries the difference; escape and transfer must be accounted for.

A pure cosmological constant has stress `T_Lambda=-rho_Lambda*c^2*g`; equal Lambda on both sides supplies no confining pressure jump. Treating its pressure magnitude as an ordinary positive halo boundary pressure introduces an unprovided interface or coupling.

The ordinary spherical Newtonian Lambda balance is `GM_tot/R^2=Lambda*c^2*R/3`, hence `R^3=3GM_tot/(Lambda*c^2)`. Substitution above in the cold-dominated limit yields `a_star ~ G^(1/3)*(Lambda*c^2/3)^(2/3)*M_c^(4/3)/M_b`, not a universal `c^2*sqrt(Lambda/(32*pi))`. A baryon–halo mass relation is still needed. This is a scaling test, not a cosmological halo-formation calculation. The standard turnaround expression is also stated in Pavlidou–Tomaras, arXiv:1310.1920; the force-balance step used here was derived directly.

## R4: a stable environmental mediator, including the pressure-keyed variant

This is a new candidate tested in this checkpoint, not a model attributed to the cited paper. Use natural units and a canonical scalar chi, with positive constants p,q,M,epsilon and a positive local material quantity X. In the adiabatic, heavy-mediator regime take

```
U(chi,X)=epsilon*exp(-p*chi/M)+X*exp(q*chi/M).
```

It has a stable minimum satisfying

```
p*epsilon*exp(-p*chi/M)=q*X*exp(q*chi/M)
m_chi^2=q*(p+q)*X*exp(q*chi/M)/M^2 > 0.
```

A physical material perturbation delta X couples through the derivative of the same energy, with vertex `q*exp(q*chi/M)*delta X/M`. Dividing this vertex by the mediator mass squared gives exactly

```
vertex_X/m_chi^2 = M*delta X/[(p+q)*X].
```

Thus with a separate constant linear baryon vertex the contact response loses epsilon entirely. Declaring epsilon to be the vacuum energy cannot select the galaxy scale in this response. For X=alpha*rho_c, fixed bare masses and weak mass renormalization, the contact scattering amplitude scales as 1/rho_c and its squared cross section as 1/rho_c^2. Substituting X=canonical kinetic-energy density does not fix the cancellation: the same identity holds, while the vertex must include each mode's actual kinetic energy. It is inconsistent to change the environmental mass while leaving the associated material vertex unchanged.

For p=q=1, eliminating chi gives `U_eff=2*sqrt(epsilon*X)`. If X=alpha*rho_c and a rest term rho_c is retained, the correction is concave:
`d^2 U_eff/d rho_c^2=-sqrt(alpha*epsilon)/(2*rho_c^(3/2))`.
This is an attractive compressibility contribution. It is not by itself a ghost theorem or a general instability theorem: mediator gradients, ordinary velocity dispersion and additional stresses matter. It does mean that a dust-only, local pressure replacement cannot be presumed stable.

### Executed continuation: exponential baryon vertex and the opposite propagation limit

Allow a baryon vertex proportional to `exp(s*chi/M)`, with fixed microscopic coefficients and baryon backreaction small enough that the preceding background remains valid. At fixed external momenta the contact cross section scales as

```
sigma_contact proportional to epsilon^[2s/(p+q)] * X^[-2-2s/(p+q)].
```

Demanding the inverse-X power fixes `s=-(p+q)/2`, and hence gives `sigma_contact proportional to 1/(epsilon*X)`. The required inverse-X dependence and the desired positive square-root vacuum dependence cannot both hold in this class. An adjustable coefficient can match one observed vacuum value, but would not derive the scale relation.

In the opposite momentum-dominated propagator limit, at fixed momentum transfer k and fixed per-mode delta X,

```
sigma_light proportional to epsilon^[2(q+s)/(p+q)] * X^[-2(q+s)/(p+q)] / k^4.
```

Here inverse X requires `q+s=(p+q)/2`, giving vacuum power +1, again not +1/2. These are power-counting obstructions for the stated Born-scattering limits, not full momentum-transfer cross-section calculations or all-mediator no-go theorems. Intermediate propagation, resonances, non-adiabatic response and strong baryon backreaction are untested. They would require checking a changing response across galactic densities, not assuming a single power law.

**Outcome: this stable exponential mediator fails as a normalization mechanism in the two tested propagation regimes, including the naive kinetic-pressure replacement and exponential baryon-vertex continuation.** Its scalar equilibrium is stable, but that does not make the combined cold material a selected galaxy halo.

## Current decision and continuation

The cold-clumping interpretation is mathematically consistent at the level of spherical equilibria. It is not yet dynamically explained. There is a whole family for arbitrary positive a_star; existence supplies no preference for kappa=1/2.

Active missing implication: construct a reciprocal, conserving interaction or formation process that selects the normalization, rather than constraining the density to it. Baryon cooling/heating, ordinary vacuum pressure confinement, pure collisionless relaxation and the tested stable exponential mediator must not be presented as solved selectors. Remaining continuations: (i) a genuinely new nonlocal/orbit-dependent exchange with its energy receiver and reaction on baryons; (ii) a finite-halo kinetic completion and stability analysis; (iii) a cosmological ensemble calculation that predicts the baryon–halo correlation statistically. The latter two are necessary checks, but neither by itself derives a0 from Lambda. Intermediate-regime or non-adiabatic mediators are untested, not excluded; resumption requires specifying the actual interaction, not selecting a desired cross-section by hand. No external jobs were launched.

Self-review: reconstructed the Abel integral and positive-factor signs; retained the infinite-mass, central-cusp and stability limitations. Proofread only the files created in this checkpoint; no canonical mathematical statements were changed. All three bounded-run manifests validated against current file hashes. The R4 cancellation is an analytic calculation, not a simulation of halo formation.

Regeneration commands and exact inputs are in the three contract JSON files and corresponding `run/manifest.json`, `extended_run/manifest.json`, `certificate_run/manifest.json`. Scripts write results to their respective run directories, so use fresh directories or adjust output paths for new runs; do not overwrite the retained evidence.
