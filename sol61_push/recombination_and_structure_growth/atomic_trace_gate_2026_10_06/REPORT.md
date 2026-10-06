# Atomic opacity versus scalar stress trace

Status: analytic conditional result for minimally coupled Jordan matter, not a recombination-history fit or a dark-matter abundance derivation. Base: reviewed source/trace checkpoint3908b938f, with subsequent Claude commits3df87c31a and536e8d160 present. This route does not substitute Claude's new master action for the audited nonminimal action.

## Declared atomic matter model

Four spacetime dimensions; dilute nonrelativistic pure hydrogen, charge neutrality, common kinetic temperature theta=k_B T, ground-state neutral atoms, negligible excited populations and interactions. Let n_b count hydrogen nuclei, x=n_e/n_b=n_p/n_b, and m_0=m_p+m_e in energy units c=1. Neutral atomic mass m_H=m_0-B, with binding B>0. Number of translational particles is (1+x)n_b. Ordinary photon stress has zero trace. Nonideal plasma, helium, excitation, quantum trace anomalies and energy injection are excluded.

Direct addition of rest and ideal translational energies and pressures gives
rho_b=n_b[m_0-(1-x)B+3(1+x)theta/2],
p_b=n_b(1+x)theta,
R_b=rho_b-3p_b=n_b[m_0-(1-x)B-3(1+x)theta/2].
Thus at fixed n_b,theta,
partial_x R_b=n_b[B-3theta/2].
An ionization change |Delta x|<=1 changes the scalar's matter source by at most n_b|B-3theta/2|. For 0<=theta<=B/10 the fractional change relative to the leading baryon rest trace is <=B/m_0. Declared hydrogen illustrative values B=13.6eV,m_0=938.783MeV give1.44868e-8. This is a bound within the declared atomic approximation, not an exact all-matter theorem. Comparing two ionization fractions at fixed temperature isolates the transition: cosmological dilution, cooling and scalar evolution also change R_b over time and are not bounded by this small number.

In particular ionized baryons are already nonrelativistic trace sources: R_b(x=1)=n_b[m_0-3theta]. The trace does NOT turn on when x falls. Emitted freely propagating photons carry energy but not ideal trace; energy transfer alone is not a new dust abundance. A small source change cannot be promoted to a universal small scalar response near a critical instability or over arbitrary time; it only disproves a proposed order-one atomic source switch in this specified matter model.

## Exact local frame dictionary

The audited theory has g_J=A(psi)^2 g_E and all matter minimally coupled to g_J, with fixed Jordan dimensionless atomic couplings. Local Einstein quantities satisfy m_E=A m_J, B_E=A B_J, theta_E=A theta_J, n_E=A^3 n_J. Treat the standard nonrelativistic chemical-equilibrium Saha expression as a declared approximation,
x^2/(1-x)=[m_e theta/(2pi hbar^2)]^(3/2) exp(-B/theta)/n_b,
with a fixed dimensionless degeneracy prefactor suppressed equally in both frames. Its right side is exactly frame invariant: the numerator supplies A^3, canceled by n_E. Its exponential B/theta is invariant. Universal scalar rescaling therefore does not directly change the local equilibrium ionization at fixed dimensionless temperature and density. This says nothing about the cosmological trajectory of those quantities or nonequilibrium populations.

Thomson sigma proportional alpha_EM^2 hbar^2/(m_e^2 c^2) gives sigma_E=A^-2 sigma_J. The collision rate Gamma=n_e sigma c obeys Gamma_E=A Gamma_J. With a_J=A a_E and dt_J=A dt_E,
H_J=(H_E+alpha_m psi_dot_E)/A,
Gamma_J/H_J=Gamma_E/(H_E+alpha_m psi_dot_E).
The scalar may affect the collision-to-expansion ratio via the actual expansion history; an apparent variation of Einstein electron mass alone is not a new physical ionization threshold. Atomic hbar is appropriate in atomic physics; it neither derives nor inserts the classical32pi coefficient.

## Why recombination and growth must be distinguished

In the tight Thomson-coupling approximation, baryons and photons share a bulk velocity, while photons provide pressure. In an adiabatic mixture with negligible baryon thermal pressure the sound speed is c_s^2=1/[3(1+R)], R=3rho_b/(4rho_gamma). This follows from delta rho_b=(3rho_b/4rho_gamma)delta rho_gamma and delta p=delta rho_gamma/3. Recombination reduces n_e and the drag/collision rate, allowing baryons to depart from this pressure-supported mixture. Rest-mass baryons already existed before this release. A separate cold component can supply potential wells before release, but this route does not establish one in the modified theory.

The full atomic history needs population rate equations, Lyman photon transport, escape and two-photon channels, not only equilibrium Saha or Gamma/H. The authenticated Chluba–Thomas paper below supplies that scope warning; no precision visibility or last-scattering redshift is claimed here. Next required calculation: a conserved ordinary baryon/photon action on the actual two-metric cosmological solution, then atomic rate/transport equations and metric-potential transfer. The earlier mirrored trace response cannot be used as an ordinary-only background solution.

## Source check boundary

Primary source: J.Chluba and R.M.Thomas, Towards a complete treatment of the cosmological recombination problem, arXiv1010.3631v3,7Dec2010, checked6Oct2026, https://arxiv.org/html/1010.3631v3. Full HTML inspected introduction and section2.1: free-electron fraction requires atomic populations; accurate recombination involves effective multilevel atoms and radiative transfer. Source supports that transport requirement ONLY. Trace algebra, frame dictionary, sound-speed reduction and finite illustrative atomic parameters above are local derivations/declared approximations, not claimed theorems from this paper. No full source copy retained or global novelty claim. Failed v2 HTML lookup was discovery failure; v3 primary full text succeeded.
