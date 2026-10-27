# Baryonic pressure, thermodynamics, and the remaining instability

BP-20261023. The inherited scalar/polarization action, dimensionless units, cold particle forces and imposed Einstein–de Sitter background are retained. This is a preferred-frame reduced cosmological model, not a self-consistent relativistic cosmology.

## Physical gas extension

For a material gas with density rho_b and specific entropy s, add internal energy to the matter action:

 S_b = integral dt integral d^3x A^3 rho_b [|v|^2/2 - u(rho_b,s) - Phi],
 p=rho_b^2 (partial u/partial rho_b)_s.

Mass conservation and material variations give

 D_t v + H v = -grad_x Phi/A - grad_x p/(A rho_b),
 D_t u = -(p/rho_b)(3H+div_x v/A)+q_dot.

For neutral monatomic gas, gamma=5/3, u=k_B T/[mu m_p(gamma-1)], mu=1.22. The local temperature equation is

 D_t T=-(gamma-1)T(3H+div_x v/A)+Gamma_C(T_CMB-T)
         -(gamma-1)mu m_p Lambda_net/(k_B rho_b),

where positive Lambda_net denotes radiative cooling per physical volume. Compton exchange and radiative cooling are open-system source terms, not conservative terms derivable from the matter-only action. A closed action would include radiation and chemistry. Here xe is prescribed, not derived.

With xe defined per total gas particle, use Gamma_C=8.55e-13 xe (1+z)^4 yr^-1, T_CMB=2.725(1+z) K. These are the mean/local thermal equations of Naoz & Barkana (2005), equations5–8, restricted to a uniform radiation bath and fixed residual xe=2e-4. The mean equation is Tbar_dot=-2H Tbar+Gamma_C(T_CMB-Tbar). Initial T=T_CMB at z=1100; a fixed residual ionization at this epoch and imposed EdS are approximations. Neither a recombination calculation nor photon transfer perturbations are included.

## Barotropic preliminary discriminator

Let x=rho_b,com/bar_rho_b,com. The discrete positive relative-energy functional is

 U_b=bar_rho_b,com c_T^2(A) sum_i v_i F_gamma(x_i),
 F_gamma=(x^gamma-gamma x+gamma-1)/(gamma-1),
 F_1=x log x-x+1, c_T^2=k_B Tbar/(mu m_p).

The baryon force differentiates the same deposition-weighted U_b. Its explicit expansion/thermal work is (dlog Tbar/dlog A)U_b. Gamma5/3 approximates isentropic compression relative to the prescribed background; gamma1 is a cooling-efficient thermostatted comparison. These are not exact local Compton thermodynamics. Gas crossing invalidates the smooth-shell interpretation, so these runs stop there. They are superseded for post-shock questions by the hydrodynamic branch below, not erased.

## Conservative gas evolution after crossing

Use comoving gas variables R=A^3 rho_b, J=R v, E=R u+R v^2/2, P=A^3 p. The spherical finite-volume equations are

 Rdot = -div_r(J)/A,
 Jdot = -div_r(Jv+P)/A +2P/(Ar)-HJ-R grad_r Phi/A,
 Edot = -div_r[(E+P)v]/A-H(Rv^2+3P)-J grad_r Phi/A+Q_com.

Cell shell volumes and face areas are exactly the inherited radial quadratures. The geometrical pressure source uses P_i(area_R-area_L)/(A volume_i), giving exact homogeneous pressure balance. A local Lax–Friedrichs/Rusanov flux evolves conservative mass, momentum and total energy; internal energy is recovered by subtracting kinetic energy. Nonpositive density or pressure stops the trial rather than applying a floor. Numerical shock dissipation raises entropy while preserving gas total energy. This is a first-order spatial method: refinement is essential.

For gravity, gas energy work is discretized using face mass flux times the potential difference, so it matches the variation of the discrete gravitational energy under gas transport. The momentum force uses the centered potential gradient. This is not a proof of exact finite-step entropy/gravity consistency; work and positivity checks are required. Gas RK2 half steps surround a cold/field canonical KDK step. The last valid state is preserved if a trial fails. Reflecting boundaries retain field radiation; this is not a cooling-to-infinity calculation.

The diagnostic energy includes cold kinetic, gas total energy, gravitational energy and all inherited positive field terms. For gamma5/3, the gas contribution to dE/dlnA is -2 E_gas; the other terms retain the inherited expansion-work identity. Compton heat is accumulated separately. Thus E-E_initial-integral W dlnA-integral Q_com dt measures numerical imbalance, not radiated binding energy.

## Why pressure does not itself choose a cold-core mass

In the linear, instantaneous-polarization limit with chi=1, P=q J_c delta_c/(1+q^2). Let J_b,c denote the dimensionless gravitational densities and q the physical dimensionless wavenumber. At frozen background the density forcing matrix is

 M = [[J_b-c_s^2 q^2, J_c], [J_b, J_c/(1+q^2)]].

The baryonic pressure is positive but the cold component has no material pressure. For positive densities and q>0,

 det M = -J_c q^2 (J_b+c_s^2)/(1+q^2) <0.

There is still one positive instantaneous eigenvalue. Raising c_s^2 lowers that eigenvalue (differentiate the explicit two-by-two eigenvalue formula), but creates no universal hard cutoff for the pressureless cold component. This is a frozen-background/quasistatic statement, not a proof of collapse in the expanding dynamical-field theory. It explains why adding a gas Jeans scale alone cannot establish a uniquely selected cold remnant mass. Cooling history, accretion, entropy and field binding remain separate requirements.

The linear numerical branch additionally evolves delta_T_dot=(2/3)delta_b_dot-Gamma_C(T_CMB/Tbar)delta_T with negligible photon perturbations, and baryon pressure proportional to delta_b+delta_T. This avoids imposing either barotropic gamma on that linear test. Radiation-era and primordial transfer conditions remain absent.

### Discrete gravity-work correction

The first face-flux gravity-energy implementation matched global potential work but did not match local momentum work. In a collapsing test cell it produced a spurious negative internal-energy derivative and eventually negative temperature. It is rejected for post-shock formation conclusions. `hydro_v2.py` instead uses -J grad Phi/A in the gas energy source, with the same centered gradient used in momentum. Gravity alone then leaves local internal energy unchanged to differential order. The resulting finite-grid potential-work discrepancy is measured in the full expansion-plus-heat residual and checked under refinement; it is not declared exactly zero. No pressure floor was introduced.

The molecular-rich sensitivity adds the GP98 low-density H-H2 cooling source under the explicit choices in COOLING_CONTRACT.md. Its integrated source is net heat, despite the inherited output label `compton_heat`. This branch remains conditional on the imposed molecular fraction.
