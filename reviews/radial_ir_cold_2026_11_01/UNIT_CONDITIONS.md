# Units, density and survival conditions

Restore mu=sqrt(f), measured in GeV. A dimensionless mass mhat and width
Gammahat computed at f=1 correspond to m=mu mhat and Gamma=mu Gammahat.
The lifetime in seconds is hbar_GeV_s/(mu Gammahat). Taking mu=1 without
restoring units cannot establish a cosmological lifetime.

For the leading radiatively lifted radial mode at the inherited minimum,
vhat=zmin/sqrt(e) and mhat=c_m e^(3/2). Its compulsory phase-pair decay is

    Gamma_radial->aa = m^3/(64 pi v^2),
    Gammahat_aa = c_m^3/(64 pi zmin^2) e^(11/2).

This follows from the canonical polar action: sigma=sqrt(2)delta R,
pi=sqrt(2)v theta, and L_int=sigma(partial pi)^2/(sqrt(2)v).
It is a partial width and supplies a necessary upper bound on survival.
Other decays and stimulated/coherent processes are checked separately.

For harmonic oscillations with alpha=delta R_amplitude/v,

    rho_osc=m^2 v^2 alpha^2,
    mu_min_density=[rho/(alpha_max^2 mhat^2 vhat^2)]^(1/4),
    mu_max_lifetime=hbar/(t_required Gammahat_aa).

A nonempty interval only passes these necessary density and spontaneous
decay conditions; it does not solve Floquet growth, production or gravity.
At fixed scaled field, mu_min_density scales as e^(-1/2), whereas the
phase-width mu_max scales as e^(-11/2). Smaller e can therefore open a
conditional interval even if the .01/.03 examples fail.

The residual-U1 gaugino is a separate candidate once its radiative mass is
included. For a Majorana mode with two spin states and a distribution
supported at |p|<=m v_max, Pauli exclusion implies

    n <= 2(m v_max)^3/(6 pi^2),
    m >= [6 pi^2 rho/(2 v_max^3)]^(1/4).

This is a stated compact-support bound, not a universal observed halo mass
limit. A cold nonthermal distribution remains an initial-state hypothesis.
The Goldstino low-energy partial width is supplied and source-checked by
the particle route; a rate alone does not select that distribution.

Vacuum normalization is material. If the raw V0=mu^4/31 is required to
equal a specified dark-energy density, mu is fixed. Then harmonic radial
energy satisfies rho_osc/V0=31 alpha^2 mhat^2 vhat^2, parametrically small
as e^2 for weak e and small alpha. A free-mu interval obtained by allowing
an independent vacuum offset does not prove this raw-vacuum identification
works. Both variants are kept in the output.

Numerical benchmarks are explicitly inputs: 13.8 Gyr survival, density
0.3 GeV/cm^3 and velocity cap .001 for a halo example, and a denser/slower
example 10 GeV/cm^3 with cap .0001. No observational fit is made. Unit
constants use NIST CODATA 2022. H0=67.4 km/s/Mpc and Omega_Lambda=.685
are a Planck-2018 base-LambdaCDM benchmark, not a claim about a latest fit.
The cosmological comparison conditionally assumes standard Einstein gravity;
the project has not derived that gravitational completion.
