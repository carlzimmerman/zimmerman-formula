# Amount, extent and conservation: exact conditional reduction

## 1. Retention repairs the budget, but must be predicted

Choose one initial patch with baryon mass B_i and cold mass R B_i, R=5.41. In a specified final aperture let B=F_b B_i and C=F_c R B_i. Then

    X_c = C/B = R F_c/F_b.                                           (1)

This is an accounting identity, not a formation law. Fractions are bounded by one only when exchange with material outside the chosen initial patch is excluded. X_c=59.5 requires F_b/F_c=0.09092436975. If F_c<=1, at least 90.91% of the initial baryons lie outside the final baryon inventory, and B_i>=10.99815 B. They need not be a hot gas sphere inside the observed lensing aperture. This corrects the CRUX inference that conservation universally bounds C by 5.41 times *observed* B. It does not invalidate the actual shortfall in a simulation with a fixed initial patch and baryon history.

For scale, the required cold mass at B=10^10 Msun occupies a mean-density-equivalent comoving sphere of radius 1.62013 Mpc at F_c=1, using the stated cosmic cold density. This is not a universal lower bound on catchment radius: an initially overdense patch with contrast delta_i changes it by (1+delta_i)^(−1/3), and incomplete cold retention multiplies it by F_c^(−1/3). The code labels this geometric conversion explicitly.

## 2. Static external-field matching ties amount to environment

For the simple AQUAL kernel, mu=x/(1+x), L=dln(mu)/dln(x)=1/(1+x). The external-field linearized Green function gives the spherical total effective mass enhancement

    F_A(x) = atan(sqrt(L))/(mu sqrt(L)),  x=g_ext/a0,
    y=g_N,ext/a0=x²/(1+x).                                          (2)

This is a flux-defined gravitational monopole, not automatically conserved rest mass. **If** the same final cold mass is identified with its asymptotic effective excess, equations (1) and (2) impose

    F_b/F_c = R/[F_A(x)-1],     R_E/r_M = 1/x.                       (3)

X_c=59.5 means F_A=60.5, not 59.5. It fixes x=0.0131841657256643, y=0.000171560345850140 and R_E=75.84856 r_M. These values are inferred from the target amount, hence cannot be presented as independent predictions of the environment. In the deep limit F_A~pi/(4x), so F_b/F_c~4Rx/pi. The corrected G240 comparison at y=.01273 instead has x=.11937 and asymptotic excess about 6.51247; it is a substantially different environment.

R_E is a transition convention. The two-grid nonlinear solve in `deepseek_corrections` finds total M_eff(R_E)/B about 54.21 at the target field, with cold excess about 53.21. Its asymptote is 60.5. Thus assigning the asymptotic X_c=59.5 inside a sharp boundary at R_E already errs by about 10.6% in the excess. Finite-aperture matching must use the finite solution and the actual lensing operator. A spherical effective mass alone is not a projected lensing prediction for the anisotropic external-field solution.

## 3. The density bridge has a precise obstruction and an escape

Outside a point baryon source, taking a Laplacian of the linearized potential gives

    rho_eff(r,theta) = B L [(3+L)cos²(theta)−(1+L)]
                      /[4 pi mu r³ (1+L sin²(theta))^(5/2)].         (4)

This is negative at the equator for L>0 and its shell angular integral vanishes. It cannot equal a nonnegative cold rest density by itself. The conclusion is about that literal identity; a signed polarization source, or a density *contrast* on a positive cosmological background, is not excluded. At5R_E for the target field, the internal/external field ratio is only about.0405, making the far-field expansion reasonably controlled. For B=10^9,10^10,10^11 Msun the equatorial |rho_eff| is about.651,.206,.065 of the z=0 cosmic cold density used in the calculation, so a positive background can cover the negative contrast there. Negative lobes do not establish a universal cold-field no-go. Near 2R_E the expansion error may be substantial; the perturbation ratio is about.253.

The existing v3 polarization action already allows signed polarization. The remaining question is which conserved charge, stress and metric source obey (1), not whether every effective term must have positive sign. That dictionary must come from one action.

## 4. Environment evolution requires transport

For a finite aperture with boundary velocity v_A and a conserved current j,

    dC/dt = - integral_boundary (j-rho_c v_A) dot n dA.              (5)

In an aperture already sampling the asymptotic plateau, neglecting finite-aperture corrections, imposing C=B[F_A(x)-1] gives

    dln C/dt = dln B/dt + s(x) dln x/dt,
    s(x)=dln[F_A(x)-1]/dln x.                                      (6)

At the target x, s=−1.00118896. An environment weakening as x∝a^(−3/2), with fixed B, demands dlnC/dlna=1.50178344: real inflow or moving-boundary capture, if C is a real mass. A static external-field response supplies no current law or energy budget. A boundary comoving with the cold material has zero right side in (5); then the imposed amount relation can persist only if B and x compensate exactly. The same problem remains if the effective source is a contrast: subtract the background and use the corresponding peculiar continuity equation consistently.

Writing rho_pol=−div P can make a formal continuity identity with j_pol=dot P. That alone does not provide an independent positive carrier, momentum dynamics, stability or a mechanism selecting P. It therefore does not close (5).

## 5. The proxy window gains an additional accretion requirement

To test G242 under its own explicit simplified environment assumptions, impose fixed physical coherence length and fixed geometric/density-contrast coefficient, so x(z)=x(.3)[(1+z)/1.3]^(3/2). A homogeneous density does not itself generate a vector external field; the coefficient must be determined from actual inhomogeneities. Fixing it is an assumption.

At z=2.5 the imposed x=.05824246 gives X_c=13.41557, while z=.3 has X_c=59.5. Retaining G242's fold interpolation, its proxy radius ratio at fixed baryon mass is .608704787. For baryon growth g=B_late/B_early, the radius ratio becomes .608704787 g^(−1/6). To meet the quoted .56 bound requires g>=1.64934741.

Combining that same history with mass matching demands

    C_late/C_early = g (59.5/13.41557) >= 7.31509.                  (7)

If the fractions refer to the same initial reservoir and F_c,late<=1, then F_c,early<=.136704. Thus the mass-plus-radius version requires at least a 7.3-fold increase of cold mass inside the modeled halo under these hypotheses. An already fully retained closed halo cannot satisfy it. An open halo with a large cold reservoir might; a transport solution is needed. No forest likelihood or host-free lensing fit follows from this necessary endpoint condition, and the chosen progenitor mapping is not independently established.

The numbers in this section use the *asymptotic* mass bridge. Substituting a self-consistent finite aperture changes the target and must be redone jointly. Changing coherence-length evolution, density contrast or the environment law changes (7); those are new physical inputs, not automatic escapes supplied by this calculation.

**One-kernel refinement.** G242 used the deep environmental approximation x∝(1+z)^(3/2). We also executed a distinct, exact-simple-kernel scalar proxy: y(z)=y(.3)[(1+z)/1.3]^3 followed by x=(y+sqrt(y²+4y))/2. The scalar relation must still be justified for the actual environment; it is not a general vector-field solution for an arbitrary cosmic web. It gives x_early=.05956050557, X_c,early=13.11721236, fixed-mass radius ratio=.595234416, and g_min=1.44211548. The required cold-mass growth is then **at least 6.54147152**, with F_c,early<=.1528708024 if F_c,late<=1. Both versions fail at fixed baryon mass and require substantial cold inflow. Their numerical difference is why the 7.3-fold condition must not be quoted as a universal bound. The fixed-B instantaneous rate in section 4 becomes dlnC/dlna=1.51161849 at z=.3, since dlnx/dlna=−3(1+x)/(2+x). `constraints_run_001` records the original deep-scaling check; `constraints_run_002` adds this explicitly distinguished refinement.

## 6. A positive equilibrium comparison reaches a different obstruction

We also tested whether the signed AQUAL density obstruction implies that no positive conserved equilibrium could supply the amount and a finite outer scale. It does not. The following explicit comparison family shows why.

Take B>0, r_M=sqrt(GB/a0), any X>0, t=2Xr_M/pi, and

    C(r)=(2XB/pi) atan(r/t),
    rho_c(r)=XB/[2 pi² t r²(1+(r/t)²)].                            (8)

This density is positive, has total mass XB, and has inner behavior C(r)~B r/r_M for r<<t. It approximates a dark-dominated deep-law rotation regime only if max(b,r_M)<<r<<t, an overlap that requires sufficiently large X. Use a finite-central-potential baryon profile B(r)=B r²/(r+b)², b>0; a point baryon combined with the central cold cusp would instead give a logarithmically divergent interaction energy. With the extended baryons, the mass and binding/kinetic energy integrals are finite. The halo's own potential is logarithmically cusped at 0. This is an ideal singular equilibrium diagnostic, not a full galaxy model or a globally Newtonian model down to arbitrarily small r.

The isotropic Jeans pressure p(r)=integral_r^infinity rho_c(s) G[B(s)+C(s)]/s² ds is positive. A stronger phase-space check is possible. Let Psi be the total relative Newtonian potential, gamma=−dlnrho_c/dlnr=2+2u²/(1+u²), u=r/t, and p_M=dln[B(r)+C(r)]/dlnr>=0. Then

    d²rho_c/dPsi² = gamma rho_c r²/[G²(B+C)²]
                   *[gamma−1+p_M−dln(gamma)/dlnr] > 0,

because gamma−1−dln(gamma)/dlnr=(1+3u²+6u^4)/[(1+u²)(1+2u²)]>0. At infinity rho_c∝Psi^4, so (drho_c/dPsi)|0=0. The Eddington inversion therefore has a nonnegative integrand and a positive isotropic distribution for every binding energy>0. The inversion formula and spherical, isotropic assumptions were checked against the [official galpy documentation](https://docs.galpy.org/en/latest/reference/dfeddington.html); the convexity proof here is independent of the package. No galpy code was used. This proves equilibrium existence within the ideal Newtonian phase-space model, not nonlinear stability or formation.

Setting X=F_A(x)−1 merely inserts the desired environmental normalization into this family. It does not derive it. Every X>0 supplies another equilibrium; the same baryons do not select one. The toy contains only about 70% of its mass near R_E in the deep regime and 95% at about 6.35R_E, further illustrating that a transition length is not a settled-mass boundary. It is not an AQUAL solution and has no AQUAL anisotropic lensing prediction.

Finally, ordinary conserved matter with only Newtonian gravitational coupling has no response to a spatially uniform external acceleration in its internal rest frame. In

    partial_t f + v dot grad_x f − (grad Phi_int + g_ext(t)) dot grad_v f=0,

set x=X+q(t), v=V+qdot(t), qddot=−g_ext(t). The external term cancels exactly. Poisson's equation for the internal density is translation invariant. This includes time-dependent uniform external acceleration. Tidal gradients survive, but their length scale depends on the tidal tensor, not merely |g_ext|. Thus a standard collisionless continuation through dust crossing can conserve mass and admit positive equilibria, yet cannot by itself derive the AQUAL external-field radius. To pursue form B with a true uniform-field effect requires a specified additional field/clock coupling that evades this symmetry and survives its own stability tests. No new particle species is proposed by this comparison.

The translation co-moves every internal source, including the baryons, and the internal boundary conditions. Artificially pinning the baryons to an unaccelerated external frame changes this premise. The positive cold distribution in (8) is self-consistent with its own density plus the prescribed extended baryon profile; no baryon distribution function or joint nonlinear stability theorem is claimed. It has infinite spatial support with finite mass and a finite transition scale, not a compact outer edge.

## Current boundary

Equations (1)–(7) are a necessary-condition reduction under stated identifications. Equation (8) and its positive distribution show that finite positive equilibrium mass is not the missing impossibility theorem; the missing work is a predictive coupling and transport/selection law. The corrected DT2 fails before it supplies that law; the exponential PIK gate fails its decoupling health check, and flat gates require an inhomogeneous constrained health analysis. The combined target remains open at those explicit dynamical obligations.
