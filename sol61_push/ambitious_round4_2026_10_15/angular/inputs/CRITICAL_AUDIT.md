# Independent audit of the joined critical two-fluid Maxwell-interface body

15 October 2026. Independent reconstruction by the dynamic-core agent, not the author of this joined model. Verdict: **proved within the explicitly defined Newtonian rest-mass-gravity/current-kinetic model, for its static equilibrium and full radial comparison energy**. This is a same-team mathematical audit, not external peer review, formal verification, or completion of the original physical theory.

The important advance is a single joined construction: ordinary neutral baryons and actual critically charged dark matter both gravitate and move; no central body is held, no third neutral stock is added, and a counted moving wall joins the occupied region to Maxwell vacuum. The positive radial form is derived for this combined system, rather than inferred by adding separate fixed-core, local-cone and wall results.

Audited frozen revisions:

- `PROOF.md`: `ec4f77a2adbf9a8f35c400103b4ab82cd872c3ef2c78c0c7b5a251ba21ebbbc3`.
- `check_critical_interface.py`: `605b7afaf32efa927fe6c19db235b8536ee353e81c3a2ab089617e8f20ada7d3`.
- `run_v1/results.json`: `ec96750a7a0b01339986d18ac6ac6452779b39e2611e6c155850e42a0c141c97`.
- `run_v1/manifest.json`: `ba934652fe566962fe3f5c1c20ab64a1b8beabc0e5ad4dbea26ad73fe1cf3eba`.

The recorded 37 exact checks and their implementation were inspected. The Mathbox validator, run with the repository root, confirms current input/output hashes. The infinite-dimensional conclusions below rest on the reconstructed contraction and inequalities; neither the manifest nor the check count substitutes for them.

## Static equations count both actual masses and the actual charge

The first varied dark-frame constitutive term vanishes on the co-moving pure-electric background, and the first beta B^2 terms vanish. With the dark current supplying the frame and ordinary baryons excluded from it, the chosen action therefore gives the displayed hydrostatic comparison equations. At critical charge zeta^2=4piG, Gauss D=zeta m_c/(4pi r^2) implies zeta E=Gm_c/[r^2(1-x)]. Thus cold material feels the actual baryon gravity plus the residual nonlinear self-electric repulsion. The latter has the outward sign in the cold enthalpy map. No source has been replaced by a fictitious neutral mass or frozen central charge.

The two species have fixed functional EOSs P_a=K_a rho_a^2. Their central densities and normalization relation are explicit inputs. The given f is a central-density input; the total mass ratio is an output and is not an exact cosmological prediction. This body is confined predominantly by the selected wall pressure, not a pressureless galactic halo.

## The two-fluid finite-ball fixed point exists

In the relative enthalpy box 0.99 w_a0<=w_a<=w_a0, each mass is bounded between the corresponding uniform-density lower and upper balls. Hence x< f/7500<1/1000. The strict inequality 0.99>f X/(1-X) bounds the cold inward force below by a positive multiple of r; this is needed for the cold map to stay below its central value despite the outward nonlinear self-electric correction.

Direct integration gives the stated upper enthalpy drops 8G(1+f)/3 and 8G/3. Both fit strictly within the chosen box. For perturbations, integrating the relative density bound gives |delta m_a(s)|<=4pi rho_a0 s^3 ||delta w||/3. The cold nonlinear mass derivative is (1-x)^-2-1, not (1-x)^-2 alone; this verifies the stated cancellation and Lipschitz bound. The two row constants are bounded by 1/4023000 and 28020101/111526611750000, both below 10^-6. The common contraction therefore supplies an actual unique regular hydrostatic two-fluid solution on the whole ball, with both densities strictly positive at the edge. No floating ODE profile is used to establish this solution.

## The wall root and global Maxwell matching are reciprocal

The wall rest mass is m_w=4pi sigma R^2/c^2. At conserved M_b and M_c, spherical symmetry makes its interaction exactly -G m_w(M_b+M_c)/R, independent of either interior density shape. Its shell self-energy is -Gm_w^2/(2R). Differentiating these together with the area rest energy reproduces all three wall-load terms in (9). Since m_w scales as area, treating it as fixed during differentiation would be wrong; the proof includes that variation.

At fixed conserved cold charge, D_b is proportional to R^-2. The electric energy jump satisfies Delta H_D=E-D, so its boundary derivative is -2D_b(E_b-D_b)/R. The summed material pressure therefore balances the electric jump and the complete wall load. The selected sigma is the weak positive root calculated from the **actual fixed-point boundary pressures**, then held fixed during perturbations. The upper test value 51P0R/100 crosses the load while the wall quadratic is still increasing, so this is a genuine tension root, not an assigned-pressure reservoir.

Normal D is continuous, which means no independent Gauss surface charge is introduced. A discontinuity of normal E is the specified constitutive phase jump; it is not an uncounted free charge stock. The exterior is the Maxwell action itself and requires no material U. The finite positive interior densities avoid the failed smooth zero-density taper premise, but this is accomplished by a new wall/phase input, not by repairing that old taper in place.

## Independent derivation of the full radial operator

Let g_b=g and g_c=g-zeta E. For either species, the pressure and advected-background-density terms reduce to

\[
 -\delta P_a'-g_a\delta\rho_a
 =(2P_a d_a)'+\rho_a(2g_a/r-g_a')\xi_a.
\]

Use the actual variations delta g=-4piG(rho_b xi_b+rho_c xi_c), delta D=-zeta rho_c xi_c and delta E=H''delta D. The background identities g'=4piG(rho_b+rho_c)-2g/r and E'=H''(zeta rho_c-2D/r) then give

\[
 F_b=(2P_b d_b)'+4\rho_b g\xi_b/r
                  -4\pi G\rho_b\rho_c(\xi_b-\xi_c),
\]

\[
 F_c=(2P_c d_c)'+4\rho_c g\xi_c/r
                  -4\pi G\rho_b\rho_c(\xi_c-\xi_b)
                  -2\zeta\rho_c(E+H''D)\xi_c/r.
\]

This agrees exactly with the frozen operator. In particular, the background density force is required; dropping it would leave a false local electric or gravitational term. Summing against the two displacements yields the positive relative-gravity square with coefficient 4piG and the positive electric restoring term with coefficient 2zeta. Both species' gravity is varied. There is no use of the earlier held-source positivity theorem.

At the common material edge, xi_b(R)=xi_c(R)=xi_R. The cold Gauss trace is

\[
 \Delta D=\delta D+\xi_R D'
          =-\zeta\rho_c\xi_c+\xi_R(\zeta\rho_c-2D/R)
          =-2D_b\xi_R/R.
\]

This is the fixed-total-charge variation required in the wall load. It also handles the Eulerian surface distribution from moving a finite-density cold edge. The correct wall equation sums the two Lagrangian pressures, -[2P_b d_b+2P_c d_c], and includes the positive wall acceleration term sigma ddot xi_R/c^2. Integrating the two bulk equations with this boundary equation gives exactly Q and I in (13)--(14). No additional independent surface-charge or wall/fluid density-cross curvature is missing under the separately conserved masses and common impermeable boundary.

The wall/matter gravitational energy depends only on the two conserved totals and R, so its remaining shape work is already in P_ext'. Its interior spatially constant potential adds no bulk force gradient. Both chemical constants can be nonzero; their path terms cancel on the separately conserved masses. Unlike the preceding compact zero-density construction, the Eulerian enclosed-mass tangents do **not** vanish separately at the fixed background R. The proof correctly uses material displacements and the summed moving-wall condition instead of importing the old Dirichlet mass-variable bound.

## Uniform radial coercivity and the assigned witness

For J_a=integral d_a^2r^2, regularity gives r^2xi_a=integral_0^r s^2d_a ds. Cauchy-Schwarz followed by reversing the integration order yields integral xi_a^2r^2<=R^2J_a/6. The two equal endpoint displacements give the stronger common trace xi_R^2<=(J_b+J_c)/(6R). These hold on the full radial form closure, not just homology trials.

Bounding g by Omega^2r and discarding only positive bulk coupling/electric terms and the positive wall cross-gravity derivative yields the coefficient C_a in (15). The exact rational lower values inspected in the output are

\[
 C_b>0.562129808590777\ldots>14/25,\qquad
 C_c>0.456994421124252\ldots>9/20.
\]

The current inertia is H_a/c^2=rho_a+2P_a/c^2. Including that value and the wall inertia, the recorded cap is 2793796681551/3125000000000 times J_b+J_c. The corresponding conservative Rayleigh lower bound is 468750000000/931265560517>1/2. Thus the positive form controls the actual declared radial inertia, including relative fluid motion and the moving boundary. The old bare-rho inertia convention is not silently mixed into this result.

The occupied dark-current EOS has H_c(1-s_c^2)=rho_c c^2. Its strict positive density lower bound and x<1/1000 give the stated very large local principal gate margin. The occupied-center magnetic coefficient comes from the pinned smooth patch; outside is Maxwell. This local pure-electric bulk check is distinct from the radial finite-radius energy proof and does not establish arbitrary magnetic or nonspherical boundary health.

## Limits of the accepted result

“Global” means the specified center/interior/common wall/Maxwell exterior configuration is solved and its finite stocks and spherical energy exchanges are counted. There is no held source. Impermeability conserves both matter stocks and critical charge; the wall receives the pressure and phase work. No independent monopole electromagnetic radiation mode is lost in the Gauss reduction. Nonspherical gauge radiation, capillary/interface modes and charge-carrying wall dynamics require further equations and analysis.

Newtonian gravity here couples to the conserved laboratory rest-density and wall rest mass, while fluid quadratic kinetics retain the inherited current enthalpy. This is the declared hybrid comparison, not minimal coupling of the full stress tensor to an Einstein metric. Internal/gauge/kinetic gravitational sources, relativistic tension gravitation and metric junction terms are not covertly included. The area wall is a chosen effective carrier with no derived microphysics, formation, tension selection or permeability mechanism.

The accepted theorem is therefore a joined, no-held-source, critical-charge **radial Newtonian control** with actual equilibrium and a true Maxwell exterior. It does not derive the EOSs, abundance, wall production, original galactic algebraic law, lensing, cosmology, empirical success, nonlinear free-boundary well-posedness or full covariant theory health. Those limits are explicitly maintained in the frozen proof. No amendment is requested.
