# Current production derivation and interpretation

3 November2026. This file supersedes the interpretation prose of the frozen
CONTROL_DERIVATION*.md run inputs. Numerical histories remain immutable. The
working approximation is a cold radial mother, dilute vacuum decay kernels,
collisionless neutral photinos, Einstein expansion, and no SM portal. Arbitrary
nonabelian energy redistribution is permitted in the **energy inequality**;
it must preserve the stipulated dilute mother decay law for the birth-quantile
inequality. A fully redistributed nonabelian collision solution was not computed.

## Source and particle kernels

The initial mother is specified at visible T=20MeV and zero physical momentum.
Its comoving number is fitted to the target pre-decay photino rest density
.265rho_c. This is an input population; no process creating that mother has
been derived. The separate H=m_sigma harmonic misalignment test is a genuinely
different primordial source hypothesis.

For canonical T radius R, the actual TP04 finite-F mass derivative gives
y_sigma,i=(dlnm_i/dlnR)m_i/(sqrt2 R). Multiplicities are8,3,1. Widths are
d_i y_sigma,i² m_sigma beta_i³/(16pi) and, for the leading phase-law coupling
y_a,i=m_i/(sqrt2R), d_i y_a,i² ma beta_i/(16pi). The canonical gravity-modified
phase-pair cubic is (m_sigma²-ma²)/(sqrt2R), hence

    Gamma_sigma_aa=m_sigma³/(64piR²)
        *(1-ma²/m_sigma²)²*sqrt(1-4ma²/m_sigma²).

Actual finite-action stationary masses/current data are imported from the
canonical and protected workers. The protected scalar-to-Goldstino cubic is
not certified by its photino dipole projection. The code therefore treats
m_scalar^5/(32pi Fmatter²) as a Ward estimate and tests factors0 and1000.
The protected GG daughter is the leading uneaten zeta, not the physical
gravitino. Its very small total energy branching makes this large uncertainty
irrelevant to the warmness conclusion. Exact mixed neutral/SUGRA scalar cubics
remain uncomputed. The unmatched phase anomaly coefficient diagnostic is not
a rigorous inclusive upper bound; no precision claim depends on it.

## Actual transport

For x=ln a, the solver evolves dN_sigma/dt=-Gamma_sigma N_sigma and momentum
bins q=a p. Phase cohorts evolve dN_a(q)/dt=-Gamma_a ma/E_a N_a(q). Their
daughter energies in the cosmic frame are E_a/2 plus or minus
p_a sqrt(1-4m_i²/ma²)cos(theta)/2. Gauss-Legendre angular integration and
positive deposition on log-q bins generate the actual gaugino distributions.
Each daughter redshifts freely afterward. Einstein H includes all mother,
phase, daughter and hidden-radiation energy, the visible bath, baryons and
Lambda. No final FD occupation is imposed.

The visible thermodynamic approximation uses exact equilibrium electron
integrals, photons and three instantaneously decoupled neutrinos. It conserves
visible comoving entropy; no dark energy transfer to SM is assumed. Residual
U1 photons are dark photons, not identified with observed electromagnetic
photons. The hidden nonabelian entropy cannot be inferred without its collision
operator. Two endpoint calculations retain companions or convert their energy
immediately to hidden radiation. They are exploratory budgets, not proved
brackets on every physical momentum/expansion history.

The neutral mean travel is the actual occupation-weighted integral
N_chi(final)^-1 integral dt/a sum_q N_chi(q,t) p/E. Lambda_FS=1kpc and
DeltaNeff=.3 are comparison gates, not likelihoods or structure transfer
functions. Radiation is reported as3P/rho_one_neutrino at the stated epoch;
unwanted nonrelativistic companion mass is reported separately.

The numerical source approximation neglects individual photino decays during
transport and reports the actual current partial lifetime separately. This
is accurate at the quoted e=.003 points to much better than1% of particle
number. At the boundary control it is a stable-transport approximation plus
the necessary Ward-survival>=.99 gate. Refitting the exact surviving abundance
would require more mothers and strengthen its energy cost. Final survivors
are biased toward later, larger-q births because their elapsed proper decay
time is smaller. The late-travel lower bound is consequently conservative.
The dark photon/Goldstino decay products stay in total hidden stress energy.

## Threshold corner without guessing an annihilation rate

Let K=rho_hidden a^4, including every dark daughter and mother. For averaged
0<=w<=1/3, dK/dln a=(rho_hidden-3P_hidden)a^4>=0. At recombination a_r=1/1101
we generously allow10% extra dark matter plus pressure-equivalent DeltaNeff=.3:

    K_r<=Kmax=1.1rho_chi,0 a_r+.3rho_nu,0.

For any massive particle E-m<=p²/E, so3P bounds kinetic energy in this budget.
All nonabelian annihilation energy remains included. A source entirely emitted
before a_r obeys K_r>=N_sigma m_sigma<a_decay>; for the exponential source
the calculation explicitly truncates this lower integral at a_r.

The visible photon/electron/neutrino EOS has rho_SM a^4 nondecreasing. Thus
Cmin=sqrt[rho_SM(a_i)a_i^4/(3Mp²)] at the stipulated20MeV start gives
H>=Cmin/a² throughout. Every exponential birth quantile u=Gamma t obeys
a_birth>=sqrt(2Cmin u/Gamma), after conservatively dropping a_i². The maximum
hidden energy allowed at recombination gives, before recombination,

    H<=sqrt[(rho_SM+Kmax/a^4+rho_b+rho_L)/(3Mp²)].

The actual numerical integral t_min of1/Hupper bounds elapsed proper source
time from below. Set U_min=Gamma t_min. The finite-recombination energy bound is

    K_r>=N_sigma m_sigma sqrt(pi Cmin/(2Gamma))
                    *gammainc(3/2,U_min).

Future decays are omitted. In dilute vacuum-width kinetics N_sigma is at
least rho_chi,0/(2Bchi mchi). This yield statement is **not** asserted for an
arbitrarily Pauli-blocked companion plasma: blocking the other channels could
increase eventual Bchi. Actual direct-stream source occupation is checked
for every8/3/1 channel. At the tested budget boundary, all source streams have
f<.01 after a region accounting for less than8.1e-8 of mothers. Redistribution
into a nonabelian bath remains a named kinetic limitation.

After recombination, positive pressure gives
rho_hidden(a)<=Kmax/(a_r a³). The **upper** H in the travel denominator is
therefore sqrt[(rho_SM+rho_b+rho_L+Kmax/(a_r a³))/(3Mp²)]. The lower birth
quantiles supply lower q, and integration of their velocities against that
upper H gives a lower travel bound. Travel starts at recombination, after
production has completed up to the explicitly bounded exp(-U_min) tail.
No travel is assigned before particle birth. The subtracted tail uses1e5Mpc,
larger than the full post-recombination relativistic path even with only
Omega_b=.05 in the H lower bound.

The5940-point physical-ratio grid and one evaluated energy/survival boundary
are finite controls, not a proof of a global minimum over all gravity models.
The physical ratio can be tuned as input; a lower-order gaugino mass does not
certify a fixed-t threshold below its unknown counterterm precision.

## Other source actually tested

Universal graviton-mediated SM scattering is a distinct existing-action source.
Tang/Wu1708.05138v2 equations3.7,3.15 and TableI give, after explicit conversion
to a Majorana final species, sigma(gamma gamma->chi chi)=s/(640pi Mp^4).
The photon MB source is3 T^8/(20pi^5 Mp^4). Its independent Bessel integral
control is integral z^6 K1(z)dz=384. Initial identical-particle and final-number
factors are included. For4 real Higgs,45 Weyl fermions and12 gauge generators,
the direct-source MB coefficient is[4/80+45(3/80)+12(3/20)]/pi^5. Quantum
bosonic/fermionic initial distributions multiply these terms by zeta(4)^2 and
[(7/8)zeta(4)]^2 respectively. The direct freeze-in yield is integrated in
constant-g radiation with an explicitly stated reheat temperature.

At TR<=.01Mp this direct source is insufficient. The entire hidden heavy
spectrum would also be gravitationally produced at such temperatures, and its
later cascade/thermal vacuum history has not been computed. This direct-source
test does not rule out every gravitational or hidden reheating scenario.

Primary sources authenticated by arXiv PDF reads: Hasenkamp/Kersten1212.4160v2
(13February2014), Hall et al0911.1120v2 (8December2009), and Tang/Wu1708.05138v2
(26October2017). No observational limits from those historical papers were
adopted as current. Local source/input bytes are pinned in v2 manifests.
