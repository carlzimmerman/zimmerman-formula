# Moving gas volumes, cooling scales, and what they do not establish

Use the inherited preferred-frame action and imposed EdS background; this is not a new covariant cosmological action. Set y=r^3/3 and gas-shell volume V_j=y_{j+1}-y_j. Mass m_j is fixed, rho_com=m_j/V_j, and physical density is rho_com/A^3. Interior faces have inertia mu_i=(m_{i-1}+m_i)/2, canonical momentum p_i=A^2 rdot_i, and kinetic energy sum(mu_i p_i^2)/(2A^2). End faces are fixed in comoving coordinates. Gamma=5/3 and neutral mean molecular weight=1.22.

## Variational gravity and compatible pressure work
Gas deposition is exact overlap of piecewise-constant density in y with the fixed field grid. Let phi_bar_j be the volume average of the grid potential in a gas shell, and phi_i the grid potential at an interior moving face. The same discrete gravitational energy used for cold particles gives

    dUg/dr_i = r_i^2 [rho_com,L (phi_i-phi_bar,L)
                            + rho_com,R (phi_bar,R-phi_i)].

The gravitational contribution to pdot_i is minus this divided by mu_i. Pressure contributes A^3 r_i^2[(p+q)_L-(p+q)_R]/mu_i. Define theta_j=3H+Vdot_j/V_j, where Vdot is computed from the very same face velocities and areas. Then

    udot_j = -(p_j+q_j)/rho_phys,j * theta_j + heat_j,
    p_j=(gamma-1) rho_phys,j u_j.

The artificial bulk pressure q=2 rho_phys max(-delta v_phys,0)^2 is active only for theta<0. Its peculiar mechanical work cancels the corresponding internal-energy work. Its background term is -3 H A^3 sum(V q); this is included in the expansion-work budget. Gravitational work cancels through the derivative of Ug. The remaining field/cold expansion terms are those of radial_base.py. Thus dE/dt=H W+sum(m heat) in continuous time. RK4 only approximates this identity: all residuals are measured, no global energy correction or temperature floor is applied. The gas force is piecewise smooth at fixed-grid crossings; time refinement remains required.

Cold particles are permitted signed radial coordinates through the origin. The inherited reflected TSC deposition makes the energy even and the force odd. This is the unfolded representation of radial passage, not material leaving the origin or a gas-shell crossing. The old v2 run's cold_boundary stop is a numerical guard, not physical disruption. Signed-orbit equivalence is explicitly checked. Gas faces must remain ordered and positive-volume.

## A cooling scale is not yet a remnant scale
For a prescribed f=nH2/nH, with H-H2 low-density coefficient L0(T) and per-molecule LTE power L_LTE(T), use

    ncrit(T)=L_LTE/L0,
    L_molecule=nH L0/(1+nH/ncrit),
    loss_volume=f nH^2 L0/(1+nH/ncrit).

The source subtracts the same per-molecule power at Tcmb and clips negative net losses. This is an approximate CMB floor, not a level-population/radiative-transfer calculation. The abundance switches on below z100; it is not produced by chemistry. The older low-density cutoff at nH=100 is replaced by the continuous LTE bridge. A conservative study guard nH<=1e7 and T<=10000 remains; crossing it requires new physics, not removal of a guard. Density-dependent dissociation and chemical heating are absent, particularly relevant in the hotter shell regions.

At fixed T, f, composition, neglecting the CMB subtraction and using gas-only free-fall density,

    tcool = [3 kB T/(2 X mu f L0)] (1/nH+1/ncrit),
    tff = sqrt[3 pi X/(32 G mp nH)],
    tcool/tff = C(T,f) [nH^(-1/2)+nH^(1/2)/ncrit].

The ratio has a minimum at nH=ncrit. Below this density, collisions make cooling increasingly competitive; above it, saturation reverses that trend. This is a physical thermal bottleneck absent from a scale-free low-density extrapolation. It is conditional on T and abundance; it neither fixes their histories nor guarantees an equilibrium, fragmentation mass or cold-field remnant.

For example, at T=200K, the adopted fits give ncrit=758/cm3. With f=.001 the minimum tcool/tff is .902 and the gas-only isothermal Jeans estimate is 3276 Msun. With f=.0001 the ratio is 9.02 at the same density. These are analytic cooling diagnostics, NOT simulated core masses. Additional cold gravitating density shortens tff and increases the ratio; varying cold concentration alters the relation. The Jeans estimate uses cs^2=kBT/(mu mp), conventional gas-only Newtonian dispersion, and is not the coupled-field instability threshold.

## Linear growth and observational gates
On the assumed homogeneous thermal history, gas temperature after z100 is below Tcmb. Our clipped molecular loss is zero in a neighborhood of that background, so its linear perturbation is zero there. Artificial viscosity is quadratic in perturbation velocity. Thus these additions do not repair or worsen linear growth at first order within this particular thermal prescription; the previous pressure/mediator growth calculation still applies, including its approximately 4.4% suppression at k=1/Mpc in the quasistatic calculation. This is not a new full-field growth integration or an observational tolerance pass.

In the restricted frozen-background quasistatic limit, the baryon/cold response matrix still has determinant -Jc q^2(Jb+cs^2)/(1+q^2)<0. A pressureless cold-coupled unstable mode persists even with gas pressure. This does not rule out nonlinear selection but prevents identifying a gas Jeans scale with a universal cold cutoff.

No dwarf, rotation-curve, cluster-population, or lensing preservation follows from energy conservation. Those require a converged remnant catalogue and transport history, then matched fits and a metric/lensing completion. The present spherical runs cannot test nonradial fragmentation or select a cosmological abundance. Resolving a moving gas mesh does not resolve the fixed cold/field grid.
