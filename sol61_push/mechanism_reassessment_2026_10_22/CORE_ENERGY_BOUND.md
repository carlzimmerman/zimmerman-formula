# Persistent cold localization from an energy gap

## Exact claim for the specified model

For every admissible state of the existing isolated spherical cold-medium plus homologous gas model, let total cold and gas masses both be one, gas thermal energy be kappa/B² with kappa=0.3, gas self-energy be -c/B with c=0.6, and total conserved energy be E<-0.3. Assume the cold kinetic, pressure and polarization energies are nonnegative, and use the reciprocal uniform-sphere baryonic potential already implemented. Then complete cold dispersal is impossible along a global energy-conserving evolution. More quantitatively, cold mass inside any fixed R>1/(-E-0.3) has a strictly positive lower bound at every time.

This is a statement about persistent localized mass, not an equilibrium profile, a particular permanently trapped set of particles, or formation from cosmological initial conditions. Global existence of the fluid evolution is assumed, not proved. The theorem also applies to the finite-node hard-wall approximation because reflection preserves the same energy and all weights are positive.

## Proof

The uniform unit-mass baryonic potential satisfies both

    Phi_b(r,B) >= -3/(2B),       Phi_b(r,B) >= -1/r.

For r<B the second inequality is equivalent to (3x-x³)/2<=1 for x=r/B in [0,1]; its derivative is nonnegative and it reaches one at x=1. Outside the sphere equality holds in the second inequality.

Write M_R for cold mass within R. Bound its cross energy using the first inequality and bound the remaining mass using the second. All other cold energies and both kinetic energies can be dropped in a lower bound. Consequently

    E >= kappa/B² - (c+1.5 M_R)/B - (1-M_R)/R
      >= -(c+1.5 M_R)²/(4 kappa) - (1-M_R)/R = F_R(M_R).

The second step is completion of a square in 1/B. For R>1/(-E-0.3), F_R(0)>E. Equivalently the energy inequality requires A M_R²+D M_R+C>=0, where A>0 and C<0 are specified below. The quadratic has exactly one positive root and one negative root, so M_R>=0 must be at least its positive root. This argument does not assume F_R is monotone for every possible negative energy and radius. It is an instantaneous inequality, independent of oscillation phase, timestep, or relaxation.

Explicitly, with A=1.875, D=1.5-1/R, C=0.3+1/R+E<0,

    M_R >= -2 C/[D+sqrt(D²-4 A C)] > 0.

If an asymptotic decomposition into escaping and retained mass exists, take R arbitrarily large after that decomposition. Its retained mass must obey

    M_retained >= [sqrt(-1.2 E)-0.6]/1.5.

The finite-R statement is stronger in one respect: it needs no assumed late-time decomposition. It does not prevent individual particles exchanging between the localized and outer populations.

## Numbers and the fixed-node check

For the 32-shell initial data E=-0.4036304602, the asymptotic lower bound is 0.06397153. Bounds inside R=20 and R=100 are 0.03536890 and 0.05852851. In this discretization a quadrature weight 1/(2N) is held at r=0. It MUST NOT be counted as dynamically retained material. Subtracting its full 0.015625 contribution still leaves mobile-mass bounds 0.01974390 within R=20 and 0.04834653 in an assumed asymptotic decomposition.

For N=64,128,1024, the initial energies are -0.4034142955, -0.4033459412, -0.4033153894. The asymptotic total bounds are 0.06384727, 0.06380797, 0.06379041. At N=128 the mobile bound is 0.03128284 within R=20 and 0.05990172 asymptotically. These numbers are ordinary floating evaluations of the explicit inequality, not interval-certified constants or a proof of continuum convergence. The margin E<-0.3 is much larger than the measured numerical energy errors.

The cold polarization energy used here is positive because at each node it is w sqrt(m)[atanh(sqrt(m)/r)-sqrt(m)/r], with 0<sqrt(m)/r<1. Cold pressure energy is proportional to sum dm²/volume>0. Thus the positivity premise is met by the actual Hamiltonian, rather than borrowed from the different scalar-carrier model.

## What this changes, and what it does not

### Removing the initial discretization entirely

For the exact continuum initial state r(m)=6 m^(1/3), 0<=m<=1, B=3 and zero velocities, the cold density is 1/72. Its pressure energy is 1/14400. The uniform-sphere cross energy is

    -3/(2 R_c)+3 B²/(10 R_c³) = -19/80, with R_c=6.

Adding gas thermal and self energies gives -97/240 before the positive cold terms. Expanding atanh(x)-x with x=m^(1/6)/6 yields the exact initial energy

    E_0 = -97/240 + 1/14400
          + sum_{n=1}^infinity 3/[(2n+1)(n+5)6^(2n+1)].

Each term is positive and the ratio of successive terms is strictly below 1/36. Therefore the first ten terms give a lower energy bound, and adding 36/35 times the eleventh term gives an upper bound. This provides a rational interval of width less than 1.062e-20 around E_0=-0.403314399234023323.

core_energy_exact_run uses exact Fraction arithmetic to verify the energy gap and the following conservative strict bounds from the displayed inequality:

    M(r<20) > 0.03516 at every admissible time;
    M(r<100) > 0.05834 at every admissible time;
    M_retained > 0.06378 if an asymptotic decomposition exists.

There is no fixed central node in these continuum statements. The completed manifest validates; the finite exact arithmetic verifies the stated rational inequalities, while the analytic geometric-series argument supplies their infinite-series justification. This strengthens the earlier finite-grid numerical estimates without proving the global existence or late-time equilibrium of the continuum dynamics.

The energy-gap argument is not restricted to exactly zero initial velocities. With the same initial density profiles, any added total kinetic energy below 0.103314399 leaves E<-0.3 and hence a positive localization bound. For a common initially expanding homologous flow v_c=h r and dot B=h B, the added kinetic energy is (3/10)h²(6²+3²)=13.5h². Thus the sufficient gap persists for 0<=h<approximately 0.08748 in the existing dimensionless units. For example h=.05 gives E approximately -0.3695644 and an asymptotic retained-mass lower bound approximately 0.04396. This is an analytic robustness interval, not a simulated expanding-cloud run or a derived cosmological Hubble rate.

It rules out the possibility that the observed outward shell implies all mobile cold matter will eventually disperse in this closed model. Some localized cold material is required by its energy budget. Converging the solver is still needed to determine how much more survives, its radius/profile, and whether it settles or keeps oscillating.

The result depends critically on fixed gas entropy and the specified positive cold energy. Allowing baryonic radiative cooling changes the baryon-only energy floor; the present proof must then be redone with the radiated energy and changing thermal state. It does not derive the initially cold population. It does not establish a realistic galaxy or a new universal gravitational mechanism.

## Self-review

Primary verdict: **proved as written**, for the explicitly stated model and admissible global evolution. Dependencies are the displayed Hamiltonian, positive weights/volumes, 0<q<1, unit masses, and elementary potential bounds/completing a square. The sign and inequality direction were checked independently by evaluating the M_R=0 limit: gas alone has minimum -0.3, so it cannot realize E=-0.4036. Fixed central quadrature mass was explicitly subtracted. The finite-R conclusion, asymptotic interpretation, and unproved global existence are separated. No external theorem or numerical trajectory is needed for the inequality. This is self-review, not independent replication; no novelty claim is made.
