# A concrete horizon-to-field transfer attempt, including the tether's reaction

2026-10-14. This is an action-level attempt following the user's instruction to push the missing BH/cold/vacuum interaction. It constructs a local curvature portal, derives reciprocal exchange and both future-horizon conditions, then checks production strength, cold-mass transfer and the unavoidable vacuum dependence of the current tether energy.

**Verdict:** a real horizon-sourced scalar transport mechanism exists in this action class, and a gradient-controlled vacuum field can preserve the local tether law in a solved galactic comparison. No single choice of functions has yet passed production strength, cold dynamics, metric health and cosmological history together. The sub-calculations below use explicitly DIFFERENT potentials and comparisons; their checks cannot be combined into a certificate for one completed theory.

## 1. Specify an actual transfer sector

In natural units, reduced Planck mass MP²=1/(8piG), consider

\[
S_{portal}=\int\sqrt{-g}\left[\frac{M_P^2}{2}R
-\frac12(\nabla\phi)^2-U(\phi)+\alpha\phi\mathcal G\right]d^4x
+S_b[g]+S_c[A_c^2(\phi)g].
\]

Here Gcal is the four-dimensional Gauss–Bonnet invariant, ordinary baryons are minimally coupled, and conserved cold particles have mass mc(phi)=Ac(phi)mc0. This is a new candidate sector, not an action already implied by the repo. U, Ac and alpha must be supplied. A background constant may be placed in U; assuming that constant does not explain its origin. This action does not yet include the unresolved full covariant tether/current parent.

Define beta_c=dlnAc/dphi. Variation gives

\[
\Box\phi-U_{,\phi}=-\alpha\mathcal G+\beta_c\rho_c,
\qquad
a_c^\mu=-\beta_c(g^{\mu\nu}+u_c^\mu u_c^\nu)\nabla_\nu\phi.
\]

The scalar, GB and cold stress divergences are respectively

\[
(-\alpha\mathcal G+\beta_c\rho_c)\nabla_\nu\phi,
\quad+\alpha\mathcal G\nabla_\nu\phi,
\quad-\beta_c\rho_c\nabla_\nu\phi.
\]

They sum to zero. The spatial recoil is present. For a homogeneous cold current, dotrho_c+3Hrho_c=beta_c rho_c dotphi: beta_c dotphi<0 transfers cold rest energy into the field. This conserves particle number, not particle rest mass. If ordinary baryons instead share the same mass function, their fractional transfer is the same and the primordial cold/baryon ratio is retained; that universal conformal variant also requires a physical-frame/atomic-clock analysis. Equal depletion is an interaction choice, not a ratio inferred from H alone.

The curvature portal is established scalar–Gauss–Bonnet physics. [Prabhu–Stein2018](https://arxiv.org/pdf/1805.02668) relates scalar charge to horizon topology and surface gravity. [Glavan–Jaramillo-Garrido2026](https://arxiv.org/html/2605.14132v1) studies the zero-potential cosmological hair and flux in the test-field regime. Neither is a proof of this project's cold carrier or a0. Our normalization alpha phi Gcal is8times the coupling written alpha_paper phi Gcal/8 in the former. No discovery or priority claim is made for those foundations.

## 2. Both FUTURE horizons select a scalar drift

First set Ac constant and approximate Uphi by a local constant slope lambda. On a supplied Schwarzschild–de Sitter background,

\[
f=1-2m/r-r^2/L^2,\quad
\mathcal G=48m^2/r^6+24/L^4
=\frac4{r^2}\frac{d}{dr}[(f-1)f'].
\]

Use phi=q t+psi(r). Its exact test-field equation integrates to

\[
r^2f\psi'=N(r)=C+\lambda r^3/3-4\alpha(f-1)f'.
\]

Let rb and rc be the black-hole and cosmological horizons. Regularity at the future BH horizon uses ingoing v=t+rstar, hence N(rb)=q rb². At the future cosmological horizon it uses outgoing u=t-rstar, hence N(rc)=-q rc². Together,

\[
\boxed{q=
\frac{4\alpha[f'(r_b)-f'(r_c)]
-\lambda(r_c^3-r_b^3)/3}{r_b^2+r_c^2}.}
\]

The drift is fixed once the coupling, slope and supplied geometry are specified. It is not an independently assigned relaxation rate. At lambda=0 a time-independent scalar cannot be regular on both selected future horizons. The outgoing-PG branch discussed in the2026 source has a difference of squared horizon radii; it uses a different chart/branch choice. We explicitly impose the two FUTURE conditions above, rather than treating squared norm regularity as sufficient to select a time orientation. No claim that the source's separate branch is an algebra error is made.

For alpha>0 define

\[
\lambda_*=
\frac{12\alpha[f'(r_b)-f'(r_c)]}{r_c^3-r_b^3}.
\]

For0<lambda<lambda*, q>0 and the local potential grows at rate dotU=lambda q. Maximum growth at fixed geometry occurs at lambda=lambda*/2. A locally rising potential therefore can receive curvature-sourced energy in this comparison. A linear potential is only a local EFT segment; it is not a supplied globally bounded dark-energy potential.

### The total energy ledger includes GB stress

The scalar kinetic flux alone gives r²Tcan^r_t=qN and is insufficient. Directly evaluating the double-dual curvature term gives

\[
T_{GB}^r{}_t=\frac{4\alpha q(f-1)f'}{r^2},
\qquad
\boxed{4\pi r^2T_{total}^r{}_t
=4\pi q(C+\lambda r^3/3).}
\]

Consequently the difference of inward Killing fluxes at the two horizons is exactly

\[
I(r_c)-I(r_b)=4\pi\lambda q(r_c^3-r_b^3)/3,
\]

the potential-energy storage rate in the intervening Killing volume. This is a reciprocal transfer identity from the specified action. Nonzero lambda makes the stress time dependent; a frozen SdS geometry is a transient decoupling comparison, not an exact stationary solution of all metric equations. The horizon length L and coupling alpha remain inputs, and the calculation does not establish m proportional to a³.

## 3. Weak curvature coupling is too small in the assigned population examples

In the approximately Schwarzschild region a hole has scalar charge Qphi=2alpha/m in our normalization. For a dilute population the leading averaged source is Sphi=8pi alpha sum(n_i/m_i). Define each near-hole backreaction parameter epsilon_i=alpha/(MP mi²). If every hole remains in a controlled regime epsilon_i<=epsilon_max, then

\[
S_\phi\le\epsilon_{max}\rho_{BH}/M_P.
\]

For slow homogeneous drift, 3H dotphi approximately equals Sphi-Uphi. Positive potential growth obeys

\[
\dot U=\frac{U_\phi(S_\phi-U_\phi)}{3H}
\le\frac{S_\phi^2}{12H},
\quad
\boxed{\frac{\Delta U_{Hubble}}{\rho_V}
\lesssim\frac{\epsilon_{max}^2\Omega_{BH}^2}{4\Omega_V}.}
\]

At assigned Omega_BH=.001, OmegaV=.7 and epsilon_max=.1, the bound is3.57e-9 per Hubble time. Even assigned Omega_BH=.01 gives3.57e-7. These are disclosed source/weak-coupling diagnostics, not measured BH abundance limits or a theorem about strong/nonlinear regimes. Fast initial motion could supply energy, but then the energy is not derived from this steady BH source. Matter mass transfer adds a different source and must be tested separately.

## 4. An explicit cold-mass portal reproduces the background, at a cost

Next set the GB term to zero in the homogeneous reconstruction, keep baryons minimal, and use the prior conserved MD14 history as a target. This tests whether a canonical cold-transfer action can realize that history; it does NOT derive the history from its potential.

Use MP=Href=1. Write target matter Y(N) and vacuum V(N), so E²=Y+V and target physical matter density is3Y. For a constant0<epsilon<1 choose

\[
\phi_N^2=3\epsilon\Omega_m,\quad
\rho_{matter,actual}=3(1-\epsilon)Y,
\quad U=3V+\tfrac32\epsilon Y.
\]

The scalar's kinetic density is3epsilonY/2. Total density and pressure reproduce the target exactly. Actual minimally coupled baryons are retained; the remaining dust density is assigned to cold particles with Ac(phi) determined by their required comoving mass. The parametric functions Ac(phi(N)) and U(phi(N)) then satisfy the scalar equation exactly. This is inverse design, and the kinetic/dust reallocation must also be accounted for in an early-universe fit.

An EXACT pure-vacuum history with the exact same dust density cannot instead be reproduced by a rolling canonical scalar: Raychaudhuri would require dotphi²=0. The reallocation above is disclosed rather than hidden.

The reconstructed scalar has positive canonical kinetic energy but acquires a cold force. At epsilon=.001:

| Diagnostic | Today | z2 |
|---|---:|---:|
| 1+wphi | .000390 | .01540 |
| MP dlnAc/dphi | -1.077 | -1.618 |
| Short-range unscreened cold–cold scalar force / gravity | 2.32 | 5.24 |
| Effective fixed-number scalar mass²/H² | -74.60 | -211.73 |

The mass is not a positive screening mass. A locally frozen cold/scalar block at z2 and k/H=10 has a growth rate9.44H in this comparison. This is not a full cosmological exclusion: the metric, existing tether restoring stress, and nonlinear evolution are omitted. It does show that fitting H has not supplied a weak harmless transfer field. At epsilon=.1 the local mass becomes positive in these examples, but 1+wphi=.610 at z2. The field is no longer close to pure vacuum there.

This tradeoff has a simple general origin for a canonical conformal portal: finite transfer Q=-beta rho_c dotphi requires either appreciable scalar motion or appreciable coupling. Near w=-1, dotphi becomes small and the required coupling grows. Screening or activation is additional physics to derive, not a word that removes the force. Adding this force to the tether changes carrier equilibrium and must be varied with the original carrier sector.

## 5. The original tether itself exerts a reaction on a dynamical vacuum

This is necessary even if the explicit cold-mass portal is absent. Let K=4piG and u=K|P|. The corrected static full energy is

\[
W_{full}=\frac{-a u-a^2\log(1-u/a)}{K},\quad
W_{rem}=W_{full}-u^2/(2K),\quad a^2=\kappa^2G V.
\]

Here V is physical vacuum energy density in c=1, and the partial variation holds the physical polarization u fixed. FULL and REM have the SAME derivative with respect to V. With x=u/a,

\[
\frac{\partial(V+W)}{\partial V}=1-\eta(x),\qquad
\eta(x)=\frac{\kappa^2}{8\pi}
\left[x+2\log(1-x)+\frac{x}{1-x}\right].
\]

Eta is positive and increasing; its derivative is kappa²x²/[8pi(1-x)²]. At kappa=.5 the source reaction cancels the bare vacuum slope at

\[
x_*=0.990904123653,\qquad 1/x_*=1.00917937077.
\]

The fixed-polarization vacuum curvature is positive. More strongly, the joint residual energy in u,V has positive diagonal curvature and determinant

\[
\det H_{u,V}(V+W_{rem})
=\frac{a^2x^4}{4K^2V^2(1-x)^3}>0.
\]

If BOTH variables freely relax locally in the reduced source energy

\[
E_{local}=V+W_{rem}(u,V)-g_Nu/K,
\]

then the equations are R(u,a)=gN and eta(x)=1. They force x=x* everywhere, yielding

\[
\boxed{g/g_N=1/x_*=1.00917937.}
\]

This is a stable local constant enhancement, not the required square-root galaxy response. The result applies to the freely relaxing, gradient-free, undriven local comparison. It does not exclude a scalar with appreciable gradients, a nonzero driving source, a pinned potential extremum or a global vacuum constraint. Ignoring Wphi while promoting a0 to a dynamical field would miss this reaction entirely.

## 6. A solved way to avoid that local relaxation: gradient control

Test a canonical scalar phi=M sigma, V=Vbackground exp(sigma), with the instantaneous homogeneous scalar equation subtracted. This subtraction is the frozen cosmological background's driving term; it is not a claim of an isolated static exponential vacuum. Retain the full tether reaction and solve its algebraic carrier equilibrium R(u,a)=gN at each radius.

For assigned Plummer baryons of6e10 solar masses, rM=9.452kpc, core=.03rM and outer boundary10rM, the dimensionless radial equation is

\[
\nabla_s^2\sigma=\epsilon_s\left[e^\sigma(1-\eta(x))-1\right],
\quad \epsilon_s=3(M_P/M)^2(H_\Lambda r_M/c)^2,
\quad\sigma'(0)=0,\quad\sigma(10)=0.
\]

The unknown x is solved from the local force law with a=a_background exp(sigma/2). This includes the response of the carrier as the scalar changes.

| M/MP | Max fractional a0 change | Max fractional total-force change |
|---:|---:|---:|
| 1 | **1.18e-13** | **4.17e-14** |
| .01 | 1.18e-9 | 4.17e-10 |
| .001 | 1.18e-7 | 4.17e-8 |

The nonlinear BVP agrees with an independent radial Green-function calculation. An analytic check bounds the Green-operator Lipschitz factor by epsilon_s R_outer² sup|F_sigma|/6. It is1.12e-9 at M=MP and .001124 at M=.001MP, and the |sigma|<=1e-6 domain maps into itself. This supplies a controlled small solution; it is stronger than merely failing to see a change in double precision. The Planck-scale bound on |sigma| is2.351e-13.

Thus a spatially smooth cosmological field can preserve the static response in this assigned patch despite its real reaction term. The boundary value and M are supplied, P stiffness is neglected in this smooth galactic comparison, and neither the GB source nor a cold-mass coupling is included here. This is a surviving local consistency result, not a proof that the same function choices produce the cosmological source history or a healthy full metric/current solution.

## Where this leaves the mechanism

The action-level chain is now explicit enough to reject misleading shortcuts:

1. Curvature can source and transport a scalar, with its drift fixed by horizon regularity and reciprocal GB stress retained. The specified weak population source does not supply the needed growth strength.
2. Cold rest energy can feed that scalar through an actual mass vertex, but the reconstructed near-vacuum examples add significant cold forces and an unstable frozen comparison block. The source history is fitted by inverse design, not predicted.
3. A dynamical a0 field must feel the tether's energy derivative. Free local relaxation changes the force law; a solved gradient-controlled patch avoids that change to high accuracy.

The next genuinely joint candidate must use ONE U, Ac and alpha, include the existing tether variation in the scalar equation, derive a source/activation strength compatible with the cold dynamics, and solve the metric/current constraints. It must also select the cosmological value rather than merely imposing it at the boundary. Those are required simultaneous conditions, not separate successes to add together. Kappa and primordial abundance remain inputs.

Canonical evidence: horizon_run_v1 has141 checks; canonical_run_v1 has115; loading_run_v2 has47; gradient_run_v4 has30, total333. Each manifest validates. Original loading_run_v1 remains a narrower preliminary run. Three gradient refinements exhausted the1e-9 mesh cap; they are retained and explained in GRADIENT_NUMERICS.txt. The canonical gradient result reports successful1e-7/1e-8 tolerances and the independent analytic contraction bound, with no1e-9 convergence claim. No shared experiment, seal, publication or cross-chat message was changed. Algebra and interpretation are self-reviewed, not independent-person replication or a novelty certificate.
