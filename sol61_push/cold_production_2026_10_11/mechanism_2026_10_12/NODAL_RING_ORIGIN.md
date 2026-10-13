# A local three-dimensional candidate origin for the cubic response

12 October 2026. Constructive but conditional result: a specified local fermion-band Hamiltonian generates a positive nonanalytic cubic polarization energy. This replaces one assumed interaction in the preceding phenomenological model with a calculated contribution. It does not derive the whole model, identify these fermions with the protected scalar carrier, or establish new physics in nature.

Follow-ups: NODAL_FORCE_LIMITS.md computes two sourced force limits; NODAL_DYNAMICS.md computes the homogeneous retarded response and collective resonance. Their results advance the corresponding uncomputed steps identified below, without completing the nonlinear galaxy or vacuum-normalization problems.

Earlier repository calculations already covered two-dimensional fermions (../../critical_response.py) and a three-dimensional nonlocal k^(3/2) dispersion (../../bulk_cubic_spectrum.py). The present distinction is a three-dimensional Hamiltonian with ordinary first and second spatial derivatives and a ring of low-energy modes. No novelty claim beyond this repository comparison is made.

## Hamiltonian and assumptions

Work in hbar=k_B=1 units. Introduce a four-component fermion with

    H(k,P) = [(kx^2+ky^2-k0^2)/(2 m_*)] Gamma_1
             + v kz Gamma_2 + h sum_j P_j Gamma_(j+2),

where m_*, v, h, k0 are positive. One explicit Hermitian representation is

    Gamma_1 = sigma_x tensor 1,
    Gamma_2 = sigma_z tensor 1,
    Gamma_3 = sigma_y tensor sigma_x,
    Gamma_4 = sigma_y tensor sigma_y,
    Gamma_5 = sigma_y tensor sigma_z.

All five matrices anticommute and square to the identity. The energy bands are

    E_+/- = +/- sqrt(q1^2+q2^2+Delta^2),
    q1=(kx^2+ky^2-k0^2)/(2m_*), q2=v kz, Delta=h|P|.

Each sign has degeneracy N=2 for this representation. At P=0, the bands touch on kz=0, kx^2+ky^2=k0^2. Assume negative bands filled, positive bands empty, zero temperature and chemical potential at the touching energy. These are state assumptions, not consequences of the original carrier.

The Hamiltonian is local as a nonrelativistic differential operator. Its unbounded continuum bands require a regulator or a band completion; it is not a causal relativistic ultraviolet theory. A single ring selects a spatial axis. Its homogeneous potential depends only on |P| because of the internal Clifford structure, but that does not guarantee isotropic spatial response.

Nodal-ring excitations have experimental analogues in ordinary solids: [Liu et al., Phys. Rev. X 8, 031044](https://arxiv.org/abs/1712.03048v3) report photoemission evidence in TiB2. That supports the availability of the band structure as a physical analogy, not its existence in a dark medium. The dark Hamiltonian and coupling above are our explicit hypothesis.

## Calculated cubic coefficient

Choose a circular energy tube q1^2+q2^2 < Lambda^2 with Lambda < k0^2/(2m_*), so the full tube surrounds the ring. Cylindrical momentum integration gives exactly

    d^3k/(2pi)^3 = m_*/(4pi^2 v) dq1 dq2.

The nodal circumference and radial velocity cancel their k0 dependence for this particular quadratic radial dispersion. Define A=N m_*/(2pi v). The change in occupied-band energy is

    V_band(Delta)-V_band(0)
      = -A/3 [(Lambda^2+Delta^2)^(3/2)-Lambda^3-|Delta|^3].

It contains a negative, cutoff-dependent quadratic term -A Lambda Delta^2/2. After subtracting that analytic quadratic contribution, the remaining small-gap expansion is

    V_ren = A |Delta|^3/3 - A Delta^4/(8 Lambda) + ...,
    beta = A h^3 = N m_* h^3/(2pi v) > 0.

Here beta is defined by V_ren=beta |P|^3/3 at leading order. This is the sign needed by the previous convex polarization construction. The result is a controlled low-gap contribution when Delta << Lambda; taking an infinite cutoff is not a claim that the tube approximation holds at all momenta. Modes outside the tube can change analytic coefficients and derivative terms.

The numerical calculation evaluates the subtracted integral using the cancellation-free integrand Delta^4/[2(sqrt(q^2+Delta^2)+q)^2]. For Lambda/Delta=10,100,1000, V_ren/(A Delta^3) is respectively 0.3208541, 0.3320834, 0.3332083, approaching 1/3. Three gap scales reproduce these same dimensionless values. A derivative of the original band formula independently checks the integral.

The quadratic subtraction must not be mistaken for an explanation of criticality. A bare polarization quadratic coefficient is needed, and its renormalized value must still match the value in a|grad phi-P/a|^2/2. No symmetry enforcing that matching has been supplied. The cubic contribution is generated; the critical quadratic relation remains imposed.

## Temperature and occupancy provide a discriminating prediction

For zero chemical potential and finite temperature, in the low-energy tube limit with T, Delta << Lambda, the same zero-temperature subtraction gives

    dV/dDelta = A [Delta^2 + 2 T Delta ln(1+exp(-Delta/T))]
              = 2 A T Delta ln[2 cosh(Delta/(2T))].

Particle and hole excitations both contribute. In the small-gap limit,

    V(Delta)-V(0) = A T ln(2) Delta^2
                    + A Delta^4/(16T) + ... .

The cubic response is rounded into an analytic quadratic response. Numerical Fermi-occupation integrals verify the formula. At Delta/T=1 the restoring derivative is 1.62652 times its zero-temperature value; at 3 it is 1.03239; at 10 it is 1.00000908. These ratios describe the constitutive derivative, not the measured gravitational acceleration at fixed baryonic mass.

At T=0 and nonnegative chemical potential mu, after adding occupied positive-energy states,

    dV/dDelta = A Delta max(Delta,mu).

Thus a nonzero mu also removes the cubic response for Delta<mu. Particle-hole symmetry gives the analogous result for |mu| in this idealized model. A finite occupation shift is not innocuous even if the fermions are cold.

In the previously used local static approximation, D/a=dV/dP. At zero T and mu this gives P proportional to sqrt(D), hence an inverse-radius force outside a spherical source. At fixed nonzero T or |mu|, sufficiently small P instead satisfies P proportional to D, giving an inverse-square response. This predicts a return from the flat-curve scaling at sufficiently large radius, provided gradient terms remain negligible there. It is a conditional observational discriminator, not a fitted transition radius.

If the intermediate-radius solution is P approximately B/r, the expected crossover scales are r_T of order hB/T and r_mu of order hB/|mu|. None is numerically predicted until the medium parameters and state are independently fixed. Retuning the quadratic coefficient separately at each temperature would remove predictivity; even with that subtraction the next analytic quartic term gives a different power law, not the original cubic response.

## Connection to the acceleration coefficient and remaining calculation

If this generated beta is inserted into the preceding scalar-polarization sector while retaining its other assumptions, its asymptotic coefficient becomes

    V_infinity^4/M_b = alpha^3/(4pi a^3 beta)
                     = alpha^3 v/(2 N m_* a^3 h^3).

That is a parameter dictionary, not a parameter-free derivation of G_N a0. The independent vacuum offset still does not fix it. Neither the value kappa=1/2 nor a0 proportional to sqrt(rho_DE) follows.

The accompanying finite-momentum calculation below addresses the static response along the ring axis. General directions and finite-frequency response remain uncomputed. A homogeneous determinant does not establish the positive constant gradient and kinetic coefficients assumed in STABLE_SOURCED_RESPONSE.md. A derivative expansion requires perturbation energies and transverse momentum energies well below Delta. Along P approximately B/r, a representative ratio v/(hB) does not decrease simply by moving outward. These conditions must be checked before transferring the earlier stability argument to this fermionic completion.

Formation of the medium, its energy/particle inventory, protection of the ring and chemical potential, isotropy, critical quadratic matching, coupling to baryons, and cosmological boundary conditions all remain open. The original bosonic carrier does not contain these fermions. This is a concrete new branch of the program, not a relabeling of that carrier as solved.

## Executed spatial-response calculation

At zero temperature and chemical potential, take a homogeneous background gap m=Delta and a perturbation along the ring axis, with energy momentum q=v k_z. Use projectors onto the filled and empty bands to compute the static interband susceptibility. Dividing its Hessian by A, the subtracted integral is

    [K_j(q)-K_j(0)]/A = integral_0^Lambda k dk average_theta {
      -[1+(k^2-q^2/4+m^2(1-2 L))/(E_- E_+)]/(E_-+E_+)
      + (k^2/E^3 if L=1, otherwise 1/E) },

where E_+/-=sqrt(k^2+q^2/4 +/- k q cos(theta)+m^2), E=sqrt(k^2+m^2), and L=1 for a mass perturbation parallel to the background vector, L=0 for a perpendicular one. This follows from the Clifford projector traces, with both occupied-to-empty orientations included. Perturbations of physical P introduce an additional factor h^2.

Direct quadrature agrees with the continuum patch expressions

    [K_parallel(q)-K_parallel(0)]/A
      = (q^2+4m^2)/(2q) atan(q/(2m)) - m,
    [K_perp(q)-K_perp(0)]/A
      = q/2 atan(q/(2m)).

Both are positive for q>0. At q much less than m, they become q^2/(6m) and q^2/(4m), respectively. At m=0 both equal pi |q|/4. The generated static stiffness thus has the stabilizing sign in the tested axial channels, but becomes nonlocal at the gapless point. It is not the same constant gamma used in the earlier radial simulation. The positive local gradient coefficient in the gapped expansion depends on the background and differs between polarization channels.

Eighteen combinations cover m=0,0.1,1; q=0.2,1,3; and both channels. Each is integrated at two cutoffs/resolutions. All 54 positivity, continuum-comparison and refinement checks pass within the declared 0.8% tolerance. The approximation requires max(m,q) much less than the tube cutoff, itself below the ring scale. The cutoff comparison is a finite numerical diagnostic, not an error certificate or proof of the closed forms.

This is useful progress beyond simply guessing a stabilizing term: the fermions supply both the cubic static potential and positive axial spatial response. It also prevents an unjustified shortcut. The old constant-gamma halo profiles cannot be imported unchanged. In a gapless isotropic approximation an operator with symbol |k| acting on a 1/r polarization would scale as 1/r^2, the same radial order as P^2. Consequently such a term can modify the leading mass–force coefficient, not just a small central correction. The actual anisotropic sourced problem and its dynamics remain necessary calculations.

## Reproducibility

nodal_ring_v2.py, nodal_ring_contract_v2.json and nodal_ring_run_v2/ record 63 passing checks: 25 Clifford identities, nine spectra, 18 cutoff-integral/derivative checks, six thermal integrals and five chemical-potential checks. The first run failed serialization of a NumPy boolean; v2 converts check flags to native bools, without changing the physical calculation. The failed attempt is retained. These are mathematical consistency checks, not 63 independent physical observations. The source analogy was checked against the primary article's abstract; no exhaustive literature or novelty search was performed.

nodal_stiffness.py, nodal_stiffness_contract.json and nodal_stiffness_run/ separately record the 54 spatial-response checks. Both successful manifests validate their declared input and output hashes. No galaxy data were fitted or rejected in these calculations.
