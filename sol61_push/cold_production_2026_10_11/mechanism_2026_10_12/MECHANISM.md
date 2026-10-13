# Mechanism checkpoint: baryon heat exchange and transport

12 October 2026. Scope: explain the halo selector missing from the prepared-carrier action, not merely improve parameter compatibility. Starting evidence: COLD_ENERGY_EQUATIONS.tex, ELASTIC_STATIONARITY.md, empirical_2026_10_12/RESONANCE_FOLLOWUP.md; neighboring CFG638 read-only. No complete mechanism is established in this checkpoint.

## Why the existing equations do not close the problem

CFG638 evolves toward a supplied rho_ph through a deficit potential and uses a supplied Jeans dispersion in its relaxation operator. Its moment identities can be correct without deriving those destinations. The present microscopic action has no nongravitational baryon vertex; constant vacuum energy supplies no local matter force. Elastic redistribution admits isothermal families whose temperature remains free. Changing the scattering normalization cannot add the missing baryon-dependent selector.

## Concrete mechanism worth testing

Baryons exchange energy with the cold component; transport redistributes that energy and changes its density. This is an existing research route, not a new discovery here. [Famaey, Khoury, Penco and Sharma, arXiv:1912.07626v2](https://arxiv.org/pdf/1912.07626), equations 26–28, propose a specific heating rate per dark mass:

    epsilon_dot = C a0 v rho_b/rho_c,
    Q_c = rho_c epsilon_dot = C a0 v rho_b.

Their transport model additionally assumes ideal-gas behavior and relaxation on roughly a Jeans time. They obtain galaxy scaling behavior under those conditions; the acceleration scale and heating law are assumptions, not consequences of our action. Their profile-based equilibrium analysis is not a proof of our exact repaired kernel or its attractor. This source is adjacent work with a useful mechanism, not independent empirical confirmation of our carrier.

The coupled energy equations must contain +Q_c for the carrier and -Q_c for baryons, plus any explicitly modelled external supply. A fixed baryon bath cannot be treated as a free permanent energy source.

A scaling explanation of the proposed mechanism is useful, but conditional: if transport on a crossing time carries luminosity L=A V^5/G and baryon heating supplies L=B C a0 M_b V, balancing them gives V^4=(BC/A)G M_b a0. Here A and B encode the profile, gradients, and transport. Assuming this luminosity, these constants, and the heating law is not deriving them. In particular, a perfectly isothermal interior has zero Fourier heat flux; its gradients and outer sink must be solved.

## Required microscopic heating law

For particle densities n_c and n_b, binary heating has the schematic form Q_c=n_c n_b <sigma_cb w Delta E_c>. Producing Q_c=C a0 v rho_b therefore requires

    n_c <sigma_cb w Delta E_c> = C m_b a0 v.

This exposes the inverse-density requirement rather than hiding it in a target force. For energy exchange scaling as m_c v² and w proportional to v, the needed cross-section scaling is sigma_cb proportional to 1/(n_c v²), up to mass factors and angular averages. A constant vacuum contact cross section does not supply this. The existing daughter self-scattering is not baryon scattering.

For two zero-drift Maxwell gases, an explicit signed exchange identity is

    Q_c = n_c n_b [mu/(m_c+m_b)] [(T_b-T_c)/s²] <sigma_cb(w) w³>,
    s²=T_c/m_c+T_b/m_b, mu=m_c m_b/(m_c+m_b).

Temperatures are in energy units. This follows by averaging the single-collision energy change -mu V_CM dot w over isotropic outgoing directions (or using the momentum-transfer cross section) and conditioning the Gaussian V_CM on w. It enforces detailed balance and an opposite baryon energy change. Disk rotation introduces drift terms and must be included; this zero-drift expression is not a disk-heating calculation. The sign cannot be stipulated independently of the distributions.

## New necessary-condition checks

### Energy reservoir

For v=V/sqrt(2), a characteristic baryon specific kinetic reservoir V²/2 lasts

    t_b = V/(sqrt(2) C a0)

under continuous heating without replenishment. At a0=9.3603e-11 m/s² and V=200 km/s, t_b=0.479 Gyr for C=0.1 and 4.79 Gyr for C=0.01. At V=50 km/s these fall to 0.120 and 1.20 Gyr. These are budget warnings, not exclusion limits; accretion, feedback, orbital contraction, or a transient heating phase could supply energy, but each needs an explicit budget and dynamical response. Reducing C changes the proposed normalization and cannot be done silently.

### Relaxation rate

For a self-gravitating singular isothermal example, rho_c=V²/(4 pi G r²), single-particle dispersion V/sqrt(2), and mean relative speed sqrt(8/pi)V. At V=200 km/s and S=0.3 cm²/g, the self-collision time at 10 kpc is 6.61 Gyr, versus a crossing time 0.0489 Gyr: a factor 135 apart. At 50 kpc it is about 165 Gyr. The revised carrier therefore does not provide Jeans-time collisional relaxation via this self-scattering channel in these regions. Orbital motion alone is not a derived irreversible heat conductivity. Collective processes or baryon collisions would be additional channels to calculate.

### Trial density-screened scalar

A concrete trial extension uses a scalar chi with homogeneous energy

    E(n,chi)=k n² + a |chi|³/3 + g n chi,   a,g,k>0.

On its negative stationary branch chi=-sqrt(g n/a), the mediator mass squared is 2 sqrt(a g n). A contact Born cross section proportional to mass^(-4) then scales as 1/n, if the dark density dominates screening and the other couplings are fixed. This supplies only the density exponent, not the required velocity dependence or a0. It also introduces a stability problem:

    E_eff(n)=k n² - 2 g^(3/2)n^(3/2)/(3 sqrt(a)),
    d²E_eff/dn²=2k-g^(3/2)/(2 sqrt(a n)),
    d²E_eff/dn² < 0 when n < g³/(16 a k²).

These identities were checked symbolically. The homogeneous mean-field branch has negative compressibility below that density; gradients and finite boundaries may affect unstable wavelengths. A realistic kinetic/thermal pressure adds another term and must be included before a total stability claim. The simple zero-temperature trial is not a viable finished mediator. A mediator mass floor could regulate the dilute limit, but would also remove exact 1/n scaling there. New baryon couplings require laboratory, astrophysical, and cosmological checks.

## Evidence and continuation

check.py, contract.json, and run/ preserve the symbolic and finite numerical audit. This tests necessary ingredients, not a new full kinetic evolution. The proposed heat mechanism is still open; it is not established by its dimensional scaling.

The next discriminating work is to derive a stable, density-dependent baryon coupling with a physical velocity dependence and its signed collision operator, then solve both energy budgets and the transport rate. If those cannot be supplied, the heating mechanism cannot be used to claim a derived halo law. Neither the vacuum relation a0=kappa c sqrt(G rho_DE) nor kappa=1/2 has been derived by this route.
