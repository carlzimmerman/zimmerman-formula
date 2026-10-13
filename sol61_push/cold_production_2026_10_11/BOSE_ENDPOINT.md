# Conditional Bose equilibrium resolves one production endpoint concern

2026-10-11. The preceding stationarity audit made progress by distinguishing
near-isothermal galaxy interiors from the non-isothermal cluster target. This
turn addresses an earlier independent gap: moving-source conversion can undo
the homogeneous Gaussian production endpoint. It need not undo coldness.

**Constructive result:** at the candidate's initial charge and excess-energy
densities, an ideal nonrelativistic Bose mixture in chemical equilibrium has
97.314% of its conserved charge in a daughter condensate. Its pressure/total
energy is 3.2600e-5. A conditional adiabatic equilibrium expansion leaves a
98.1545% daughter condensate after the thermal source population disappears.
This is a thermodynamic endpoint candidate, not evidence that equilibration
actually occurs or that the repo's halos form.

## Ensemble and assumptions

Use the parameters recorded in `nr_quantum_bound_run/results.json`:

    m = 193.5248917183 eV, M = 387.0691354420 eV,
    delta = M-2m = 0.01935200538 eV,
    rho_initial = 9715106.1903 eV^4.

Units hbar=c=k_B=1. Daughter charge is 1 and source charge is 2. Starting from
zero-momentum sources gives conserved charge density and excess-energy density

    n_Q = 2 rho_initial/M = 50198.29948 eV^3,
    d_initial = (delta/2)n_Q = 485.7188809 eV^4.

The ideal approximation drops the interaction energy but retains the reaction
chi <-> phi+phi as a chemical-equilibrium condition. The species are not
assigned separately conserved particle numbers. Chemical potentials relative
to mQ are mu_phi=mu and mu_chi=2mu. On the ideal daughter-condensed branch mu=0,
so the source has occupation 1/[exp((p²/(2M)+delta)/T)-1]. Source condensation
does not occur on this branch because delta>0. Antiparticles, relativistic
corrections, gravitational inhomogeneity and external heat exchange are omitted.
The maximum temperature is T/m=0.003486; the approximation is nonrelativistic
but not an exact relativistic calculation.

For either species define

    N_j(T,alpha) = (2 m_j T)^(3/2)/(2 pi²)
                    integral_0^infinity x²/[exp(x²+alpha)-1] dx,
    K_j(T,alpha) = T (2 m_j T)^(3/2)/(2 pi²)
                    integral_0^infinity x^4/[exp(x²+alpha)-1] dx.

Use alpha_phi=0 and alpha_chi=delta/T. Then

    n_cond = n_Q - N_phi - 2 N_chi,
    d(T) = K_phi+K_chi+delta N_chi,
    P(T) = (2/3)(K_phi+K_chi).

Solve d(T)=d_initial and verify n_cond>0. This is the self-consistency test for
the assumed condensed branch, not an imposed condensate fraction.

## Endpoint and expansion

The energy constraint gives T=0.674710845 eV. At this point:

- Daughter condensate charge fraction: 0.97314218.
- Thermal source charge fraction: 0.02192769.
- Thermal daughter charge fraction: 0.00493013.
- P/(m n_Q+d): 3.2599966e-5.

The thermal cloud can be much faster than the condensate; small total pressure
does not bound every individual particle velocity. The thermal source fraction
is also much larger than the 1.80684e-7 transient homogeneous Gaussian remnant.
The two results concern different assumed states and do not contradict each
other. Neither is a derived halo-era source abundance.

For homogeneous, reversible adiabatic expansion with continued equilibrium,
charge and entropy in a comoving volume are fixed. Because mu=0, the entropy
density is S=(d+P)/T. Solve S(T(a))=S(T_initial)/a³ and n_Q(a)=n_Q(initial)/a³:

| Expansion a/a_initial | T (eV) | Daughter condensate charge fraction | Thermal source charge fraction | P/total energy |
| --- | ---: | ---: | ---: | ---: |
| 1 | 0.674711 | 0.973142 | 0.0219277 | 3.2600e-5 |
| 2 | 0.175302 | 0.976740 | 0.0180365 | 8.2236e-6 |
| 10 | 0.0114780 | 0.984352 | 0.00470910 | 4.6789e-7 |
| 100 | 1.62662e-4 | 0.981545 | 8.58e-54 | 7.9654e-9 |
| 1000 | 1.62662e-6 | 0.981545 | negligible | 7.9654e-11 |
| 1e6 | 1.62662e-12 | 0.981545 | negligible | 7.9654e-17 |

The condensate fraction need not be monotone while source excitations disappear.
Once the source gas is negligible, T scales as a^-2 and the ideal condensate
fraction is constant. This is NOT a cosmological prediction: expansion can
outpace reaction or kinetic equilibration, and the actual initial entropy
requires a dynamical production history. Ideal zero-condensate-energy results
are not replacements for the interacting quantum stress bound.

## Size of the omitted interactions

The positive-square NR Hamiltonian gives k_eff=k-c²/delta=1.927748626e-13 eV^-2.
Using the calculated initial condensate density, a leading static mean-field
estimate gives

    mu_MF = 2 k_eff n_cond = 1.8834e-8 eV,
    mu_MF/T = 2.79e-8, mu_MF/delta = 9.73e-7,
    k_eff n_cond²/d_initial = 9.47e-7.

A source amplitude slaved to a uniform daughter condensate, b=-c n_cond/delta,
would contribute charge fraction 2|b|²/n_Q about 9.47e-7. This is a coherent
interaction dressing, distinct from the tabulated thermal source gas. Thus
"negligible thermal source" must not be read as exactly zero source field in
the interacting theory. These small energy scales motivate the ideal endpoint
approximation. They do not prove its interacting phase diagram, excitation
spectrum, renormalization or relaxation time. Corrections to the condensate
charge fraction and chemical potential have not been solved self-consistently.

## Evidence and what remains

`bose_endpoint.py` solves the energy and six entropy constraints and checks
positive remaining condensate charge. Thermal integrals are audited against
zeta-function values for gapless daughters and an independent 20,000-term
fugacity series for sources at the initial temperature. All 18 finite checks
pass. Integrals stop at sqrt(kinetic energy/T)=30, where omitted tails are
exponentially negligible; this is numerical evidence, not a rigorous interval
bound. `bose_endpoint_run/manifest.json` validates recorded provenance.

The calculation supplies a coherent alternative to requiring the first
homogeneous conversion episode to remain permanently complete: reactions may
redistribute population while the energy and charge allow a predominantly
condensed, cold endpoint. The [quantum pressure bound](NR_QUANTUM_PRESSURE.md)
continues to be the stronger non-equilibrium statement within its regulator.

The next decisive production calculation is the approach rate to this endpoint
with stimulated conversion, condensate growth and scattering represented
consistently. A classical Maxwellian collision rate alone cannot certify Bose
condensation or chemical equilibration. The daughter field, its source,
initial abundance, halo temperature and profile selection are still candidate
physics, not experimentally identified matter or a closed theory.
