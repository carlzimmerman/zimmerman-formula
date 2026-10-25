# Can the vacuum select the cold reservoir?

**The requested parameter-free reservoir has not been derived.** This continuation tests three distinct production routes instead of assigning a new abundance or velocity. It obtains a quantitative failure for the late-vacuum thermal route, an explicit gravitational-production calculation showing dependence on expansion history, and an exact energy-transfer constraint. A new microscopic/cosmological completion remains necessary; these results do not exclude every possible completion.

The current CCT selective action is the one in `sol61_push/continuous_cold_envelope_2026_10_24/COUPLING_BRIDGE.md`. It is nonrelativistic, has no derived covariant parent or production term, and leaves eta=1500 pc km/s imposed. The checks below do not turn eta, a0 or the vacuum energy into predictions. They do not inherit fits from the separate literal v3s program.

## 1. What the source-free theory actually predicts

The established continuity law fixes global cold inventory from initial data. In a homogeneous collisionless FLRW extension, physical momentum p obeys

    partial_t f - H p dot partial_p f = 0,
    f(p,t) = f_initial[a(t)p/a_initial].

It predicts dilution and redshifting: n proportional to a^-3 and nonrelativistic velocity dispersion proportional to a^-1. It does not choose the initial function f_initial. This kinetic description is conditional on an incoherent/quasiclassical regime; a coherent wave instead requires its initial amplitude and phase. Neither is selected by the existing action.

Normal quantization of a number-conserving nonrelativistic Hamiltonian does not change this. Terms with equal numbers of creation and annihilation operators preserve the empty state, including time-dependent gravitational one-body potentials and normal-ordered self-gravity. Relativistic pair creation is a genuinely different possibility; conserved charge there need not equal conserved particle number. Route 3 below treats that distinction explicitly rather than applying the nonrelativistic norm argument outside its domain.

## 2. Route A: a late de Sitter temperature is not a viable reservoir selector

### Conditional dictionary and thermal calculation

To make a definite test, suppose a conventional canonically quantized scalar completion identifies

    m = hbar/eta = 1.27810e-21 eV/c².

This identification is an additional interpretation of the classical field, not an established ontology of the framework. A medium with a different quantum normalization or dispersion needs a separate calculation.

Use the de Sitter temperature relation

    k_B T_dS = hbar H_Lambda/(2 pi).

[Gibbons & Hawking (1977)](https://doi.org/10.1103/PhysRevD.15.2738) is the original horizon-thermodynamics source. This temperature does **not** by itself establish a real homogeneous gas of particles. As an extra, deliberately explicit assumption, test what an ideal nonrelativistic bosonic gas at that temperature would supply.

For one degree of freedom with zero total chemical potential, the dilute result is

    rho_th = m [m k_B T/(2 pi hbar²)]^(3/2) exp[-mc²/(k_B T)],
    mc²/(k_B T_dS) = 2 pi c²/(eta H_Lambda),
    sigma_1D² = k_B T_dS/m = eta H_Lambda/(2 pi).

H_Lambda=1.8e-18 s^-1 is an explicitly external reference scale, not a fitted value or a deduction from a0. At this scale:

- T_dS = 2.18819e-30 K;
- sigma_1D = 0.115151 km/s;
- the Boltzmann exponent is 6.77808e12;
- log10(rho_th/rho_Lambda) is approximately -2.94368e12, where rho_Lambda=3H_Lambda²/(8 pi G) is a mass density.

No exponentiation of this enormous suppression is used numerically. H_Lambda=1e-18 and 3e-18 s^-1 give the same qualitative result; all three values are reference sensitivities, not measurements used to optimize the conclusion.

### Allowing a chemical potential does not remove the normalization problem

For an ideal number-conserving Bose gas, total chemical potential obeys mu<=mc². The largest thermal excited-state number occurs at mu=mc²:

    n_exc,max = zeta(3/2) [m k_B T/(2 pi hbar²)]^(3/2).

At the middle reference scale,

    rho_exc,max / rho_Lambda = 10^(-92.9981).

This is a maximum for the *thermal excited states of the stipulated ideal gas*, not a bound on an arbitrary cold classical field. A condensate can carry much greater density, but its particle number is additional conserved inventory. At saturation the temperature and chemical potential do not fix that condensate occupation. Assuming that occupation equals the required reservoir would insert the answer.

The tiny thermal velocity also does not provide the proposed galaxy/cluster speed filter: in the impulsive capture control, wells with escape speeds far above this dispersion both admit almost the entire speed distribution. This is only an energy-criterion statement; it is not a claim that a static galaxy captures an unbound passing particle without losing energy.

### Symmetry makes the distinction sharper

For a de Sitter-invariant state and covariant renormalization, a separately invariant stress expectation must have the form <T_mu_nu>=C g_mu_nu. It has the vacuum equation of state, not that of a finite-density pressureless reservoir. A preferred cold rest frame or a non-equilibrium relic state breaks this premise. Thus horizon thermality and vacuum fluctuations cannot simply be counted again as a classical dust source. This statement is scoped to exact de Sitter invariance, not the actual time-dependent matter-filled Universe.

**Disposition:** the stipulated late-vacuum ideal-gas selector fails. Alternative quantum normalizations, interactions, non-equilibrium production and early cosmology remain outside this result.

## 3. Route B: compute gravitational production rather than assume a distribution

### A concrete relativistic control

Consider a free scalar on spatially flat FLRW with metric a(s)²(-ds²+dx²), in units hbar=c=1. For curvature convention R=6a''/a³, rescale chi=a phi:

    chi_k'' + [k²+a²m²+(6 xi-1)a''/a] chi_k = 0.

The standard mode/Bogoliubov formulation and its cosmological inputs are described by [Kolb & Long, sections III and VI](https://arxiv.org/html/2312.09042v2). The calculation here is an independently checked smooth-background example, not one of their relic-density fits.

Fix xi=1/6 and m=1, and prescribe

    a²(s) = 5/2 + (3/2) tanh(s/tau).

All cases have the same mass, coupling, initial scale factor 1, final scale factor 2, and asymptotic positive-frequency in-vacuum. Only the transition duration tau changes. The background is prescribed; we have not produced a stress source realizing it self-consistently or a covariant selective MOND completion. In particular, this asymptotically static control is not our Universe and is not asserted to have a late de Sitter vacuum.

Let wi=sqrt(k²+1), wo=sqrt(k²+4). The produced occupation is

    |beta_k|² = sinh²[pi tau (wo-wi)/2]
               / {sinh(pi tau wi) sinh(pi tau wo)}.

For completeness this follows by putting z=(1+tanh(s/tau))/2 and

    chi = z^alpha (1-z)^beta F(A,B;C;z),
    alpha=-i tau wi/2, beta=+i tau wo/2,
    A=alpha+beta, B=1+alpha+beta, C=1+2alpha.

The hypergeometric connection coefficient of the outgoing negative-frequency term is Gamma(C)Gamma(2 beta)/[Gamma(A)Gamma(B)], with normalization sqrt(wo/wi). Taking its squared modulus gives the displayed occupation. Direct ODE integration independently checks nine modes; the formula is not accepted merely because it was coded twice.

### Both normalization and velocity spectrum change

Per scalar degree of freedom,

    a_out³ n_out = (1/2 pi²) integral dk k² |beta_k|²,
    <v²>/c² = integral dk k² |beta_k|² k²/(k²+4)
              / integral dk k² |beta_k|².

| tau (in m^-1 units) | Comoving number (in m³ units) | Final rms speed/c |
|---:|---:|---:|
| 0.1 | 0.00776942 | 0.714261 |
| 0.5 | 0.000410000 | 0.482882 |
| 2.0 | 5.70466e-9 | 0.253384 |

The abundance ratio between the first and last controls is **1.36194 million**. Their normalized velocity spectra differ too. These are newly produced relativistic populations in a dimensionless control, not present-day cold velocities; later expansion would redshift them, with additional dependence on that expansion.

No coupling or final mass has been varied to obtain this difference. Hence even choosing a conventional initial vacuum and fixing the curvature coupling does not remove the production-history input. A late vacuum scale alone specifies neither this history nor the redshift to the present. This demonstrates the missing input explicitly; it does not prove that a future unified theory cannot fix the whole history.

Direct ODE occupation errors are at most about 4.52e-11 in the nine tested modes. Wronskian drift is below 7.2e-10. The weakest-production high-k mode is extremely small; it is reported but no large relative-precision conclusion is needed there. Integrating to k=30 versus 60 changes the reported number by at most 1.47e-8 relatively and passes the velocity-moment check. These are finite-domain checks, not a complete primordial spectrum calculation.

**Disposition:** gravitational production remains a viable physical route, but a reservoir prediction requires the covariant action, expansion history, vacuum prescription and subsequent transport. The present CCT theory supplies none of that full selection. A universal late attractor that erases these differences is not tested here; it would need a specified number-changing/redistributing dynamics.

## 4. Route C: can stable vacuum conversion select a universal fraction?

Use homogeneous energy densities epsilon_v and epsilon_c (not mass densities), a pressureless cold component, and vacuum pressure p_v=-epsilon_v. If Q is energy transferred from vacuum to cold, total conservation gives

    dot epsilon_c + 3 H epsilon_c = Q,
    dot epsilon_v = -Q.

An exactly constant positive vacuum has Q=0 in this two-component system. It cannot continuously replenish a homogeneous cold reservoir against expansion without a further energy supplier, a changed equation of state or time dependence. This does not exclude existing bound clusters, which are not homogeneous comoving dust, nor an earlier production episode followed by a stable vacuum.

For a proposed positive constant ratio r=epsilon_c/epsilon_v, imposing dot r=0 yields the necessary relation

    Q = 3 H r epsilon_v/(1+r),
    d ln epsilon_v/d ln a = -3r/(1+r),
    w_eff = -1/(1+r).

Every r>0 requires an evolving vacuum. The algebra permits a continuum of r; it supplies no particular value. Declaring Q=3 alpha H epsilon_v just selects r=alpha/(1-alpha) when 0<alpha<1, moving the missing abundance into alpha unless a microscopic theory derives it. The three finite balance checks confirm the identities, not the stability or existence of an attractor for a specified Q.

Even an independently fixed Q is insufficient to determine velocities. In a kinetic completion with source S(p,t), the homogeneous solution schematically is

    f(p,t) = f_initial[a(t)p/a_initial]
             + integral_initial^t dt' S[p a(t)/a(t'),t'].

The energy integral of S fixes Q; its number integral and momentum dependence separately determine abundance and speeds. For number-changing production a source can also include loss/stimulation terms, so this expression applies when S is the specified net source along characteristics. A microscopic source kernel is required, not merely an energy-transfer scalar.

**Disposition:** continuous conversion out of an exactly stable homogeneous vacuum fails under these two-fluid assumptions. Transient decay, an evolving dark component, early production and extra interactions remain open extensions, each requiring an action and initial-state prescription. A constant-ratio ansatz is not a derivation of r.

## 5. What this does to the cluster/galaxy requirement

The earlier rapid-assembly result requires sufficient inventory outside the galaxy-tested apertures and a common physical distribution that clusters retain without excessive extra enclosed gravity in galaxies. Its spherical allowance remains

    M_c(<r) <= delta(r) r² g_law(r)/G.

No value of delta is selected here; it must be inferred with the galaxy likelihood. A final reservoir also requires its spatial correlations with baryons, not just a mean number and one rms speed. None of the three routes has supplied a distribution that can honestly be propagated into a successful cluster/galaxy prediction:

- Late-vacuum ideal thermal excitations are negligible; a large condensate reintroduces inventory.
- Gravitational creation can generate a spectrum, but the tested spectrum and normalization change with expansion history even at fixed couplings and in-vacuum.
- Vacuum conversion needs a derived source kernel and cannot be sustained by an exactly constant vacuum in the stated closed two-fluid model.

This reduces the viable target to **a non-equilibrium cosmological production mechanism with a derived expansion/state prescription and momentum-resolved source**, or a substantively different completion. It is stronger than choosing a cold/baryon ratio, a temperature or a capture efficiency. It is not yet that mechanism, and a new large cluster simulation with assigned reservoir inputs would not close the gap.

## 6. Evidence, limitations and continuation handoff

`FROZEN_CRITERIA.md` fixes the routes and finite tests before execution. `check.py` and `contract.json` reproduce the thermal comparisons, nine oscillator integrations, three integrated spectra and three energy-balance checks. `run/manifest.json` records input/output hashes and the completed bounded run. `mutation/manifest.json` records the expected failure when the thermal temperature loses its 2pi factor. Both records are hash-validated. Analytic statements have self-review only, not independent referee certification.

External-source scope: the Gibbons-Hawking temperature is standard horizon thermodynamics, not authorization to substitute a material gas. The original publication's metadata was accessible but its full-text endpoint rejected access; the temperature is independently corroborated by the displayed equation in [Melia (2021)](https://doi.org/10.1140/epjc/s10052-021-09028-5), without adopting that paper's cosmology. The Kolb-Long review was inspected for its scalar mode formulation and dependence on gravitational/inflationary inputs. All tabulated numbers are our calculations. The solvable tanh example, gas interpretation and two-fluid restrictions are explicitly stated assumptions.

Resumption conditions: derive a covariant production term and cosmological background from the same candidate action, with a state prescription independent of halo fits; then calculate number, momentum spectrum and spatial correlations, redshift them, and apply the existing mass/energy ledgers and galaxy likelihood. Early scalar self-interactions or a vacuum transition remain untested possible extensions; they cannot be evaluated as predictions until their potential, couplings and state are fixed. The original first-principles goal remains OPEN. Do not promote this checkpoint, an imposed eta, or a selected transition duration to theory closure.
