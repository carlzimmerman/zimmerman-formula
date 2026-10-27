# Moving compact cores: collective dynamics derived; abundance not selected

MCP-20261022, base Git 3d82af0a7eb241322237e1ca1257fc9debddd372. Continues compact_surplus_2026_10_22 without changing its records or unrelated work. The original joint target remains open.

**An extended population can substantially improve the cluster shape, but the present theory does not predict its abundance or spatial distribution.** Its dilute, slow-motion limit is a kinetic gravitating population with extra field inertia. A positive equilibrium family exists and can fit the middle cluster bins without the central-core overshoot. The successful cluster interpretation replaces the cluster dark component; adding the same fitted population to the full empirical law overshoots outer lensing. Dwarf central occupation, formation/merger rates and the environment dependence needed to retain the galaxy law remain missing.

The most important correction is cosmological: present-size dwarf cores cannot form a dilute all-core population at recombination. A late conversion is geometrically possible, but does not restore growth lost in the earlier diffuse phase. All lensing statements retain the predecessor's additional equal-metric-potential assumption. Review is self-review, not independent certification.

## 1. Deriving the motion, without discarding reciprocal field inertia

Take a spherical static cold core with conserved material mass m, translate its profiles by q(t), and put material velocity equal to V=q_dot. In the local passive, X=0 branch, P_dot=-V.grad P and chi_dot=-V.grad chi. Spherical angular integration gives the leading collective-coordinate Lagrangian

    L_core = Mi V²/2 - E_internal - m Phi_external(q) + tidal/overlap corrections,
    Mi = m + (eta/3) integral |grad P|² d³x
           + (Mchi/3) integral |grad chi|² d³x.

Thus, for fixed internal state,

    q_ddot = -beta grad Phi_external,    beta=m/Mi <= 1.

The long-range gravitational source is m in this Newtonian action, not Mi. The preferred-frame time-derivative terms make Galilean point-particle inertia an assumption that must be tested. This reduction assumes slow translation/deformation, stable cores, weak tidal variation and separations large enough that field overlap is negligible. It is not a proof that the cusp/edge-jump core has a stable moving continuation. In an occupied surrounding medium the vacuum isolation approximation must also be rederived.

For the canonical dwarf-fitted fixed-chi core, write P=(a0/K)w(x) rhat, x=r/ell0 and m=M0 mhat. Numerical integration including the exterior gives

    J = integral_0^infinity [x² w'²+2w²] dx = .0465003931,
    mhat=.0840813319,
    (Mi-m)/m = .184346878 (eta rho_scale),
    rho_scale=a0/(4piG ell0).

The integral is finite despite the integrable central cusp. Extending the outer cutoff and tightening tolerance changes J by about3e-9 relatively. The coefficient eta is still an unselected action parameter. A passive variable chi adds further positive inertia.

## 2. What the kinetic equation can and cannot determine

For separated noninteracting surviving cores with a specified mass spectrum, the leading number distribution f_m obeys

    partial_t f_m + v.grad_x f_m - beta(m) gradPhi.grad_v f_m = 0,
    laplacian Phi = 4piG [rho_b + integral m f_m d³v dm].

This is a conditional collisionless reduction, not a derivation of negligible collisions. A formation/merger/evaporation calculation would instead produce source and collision terms and transfer mass to/from the diffuse phase. Those terms have not been supplied or computed for this action. They are not permission to add new cold mass to an already counted law component.

The phase-space flow has zero divergence, so, under decaying/no-flux boundaries, each integral C(f_m) d³x d³v is conserved for any differentiable C. In particular, particle number is an initial datum. The familiar Hamiltonian kinetic invariants are discussed in [Ye & Morrison, Action principles for the Vlasov equation](https://web2.ph.utexas.edu/~morrison/92PFB771_morrison.pdf); here the conservation also follows directly by integrating the displayed equation.

For a monodisperse population with collapsed fraction F(a),

    n_physical(a) = F(a) rho_c,0 / [m a³].

This is the abundance constraint, not a predicted F or m. The density illustration and imposed EdS growth histories below are separate benchmarks, not a single self-consistent cosmology. With illustrative inputs Omega_c=.25 and H0=70km/s/Mpc, rho_c,0=3.3997e10 solar masses/Mpc³. Taking the inherited *fitted* m=1.095e7 solar masses gives n0=3104.8 F0/Mpc³; F0=1 implies a mean spacing68.55kpc. Lensing of a smooth population measures the mass moment integral m f_m, not number or mass spectrum separately. Different core masses and abundances can give the same mean lensing profile.

There is also no finite fastest-growing fragmentation scale in the inherited quasistatic, cold-only smooth limit:

    s_growth²=4piG rho_c/[1+k²ell0²],
    d/dk [1/(1+k²ell0²)] = -2k ell0²/(1+k²ell0²)² < 0.

This does not exclude nonlinear fragmentation with specified initial fluctuations and field dynamics. It does rule out claiming that this linear response alone selects the dwarf core mass.

### An explicit distribution, and a counterexample to unique selection

In the isolated, self-gravitating, common-beta limit a positive Plummer equilibrium is

    rho_pop(r)=3M b²/[4pi(r²+b²)^(5/2)],
    Phi=-GM/sqrt(r²+b²),
    f_mass(E)=24sqrt(2)b²/[7pi³ beta^5 G^5 M^4] (-E)^(7/2),
    E=v²/2+beta Phi<0; f=0 otherwise,
    sigma_r²=beta GM/[6sqrt(r²+b²)].

Velocity integration, Poisson and Jeans checks verify the normalization and force balance. M and b are inputs. This is a distribution of core centres, not the density inside each core. Adding baryons changes the self-consistent distribution function, so using this density as a cluster lensing template is a necessary shape test, not a solved baryon+core equilibrium. A primary discussion of this collisionless family appears in [Polyachenko & Shukhman](https://link.springer.com/article/10.1134/S1063772923110082); our normalization was checked directly.

For beta=1 the isolated Plummer energy is E_total=-3piGM²/(64b). Knowing the assembly energy could determine b *within this chosen family*, but mass and energy do not select the family. An explicit positive isotropic n=3 polytropic distribution f proportional to (E_cut-E)^(3/2) supplies a counterexample: in G=M=1 units, the same total energy as a b=1 Plummer sphere yields a finite outer radius16/pi=5.092958, whereas the Plummer sphere has a nonzero infinite tail. The Lane-Emden calculation gives xi_edge=6.896849, mass2.018236 and independently integrated U=-1.5GM²/R. Both states have identical M,E and different spatial distributions. No universal equilibrium profile follows from those conserved moments alone.

## 3. Cluster lensing: extended populations improve shape, with a crucial distinction

For the Plummer population, in the conditional weak-lensing metric,

    M_cyl(<R)=M R²/(R²+b²),
    Sigma=M b²/[pi(R²+b²)²],
    DeltaSigma=M R²/[pi(R²+b²)²].

At cluster radii the321.5pc internal core size is negligible. Unlike a single central mass, the extended population need not produce a large inner R^-2 excess.

The cached318-object CFG687 sample and canonical baseline were retained. Two parameters were fitted using only the three MID bins; INNER and OUTER were held out. Two prescriptions were tried: common M,b; and M=q M_gas, b=t R500. The fit metric uses stacked inverse-variance weights, not a new calibrated covariance likelihood. Thirty RA jackknife deletions refit the parameters. A is observed/model band amplitude.

| baseline and prescription | median M, solar masses | median b | INNER A | OUTER A |
|---|---:|---:|---:|---:|
| Newtonian baryons + common population | 2.181e14 | .5805Mpc | 1.834 +/- .438 | 1.085 +/- .149 |
| Newtonian baryons + gas/R500-scaled population | 2.160e14 | .5298Mpc | 1.651 +/- .405 | 1.038 +/- .147 |
| full empirical law + common extra population | 9.670e13 | .4913Mpc | 1.390 +/- .319 | .740 +/- .073 |
| full empirical law + gas/R500-scaled extra population | 9.359e13 | .4408Mpc | 1.305 +/- .320 | .732 +/- .074 |

All four fits lie away from parameter bounds and have MID amplitudes near1. The Newtonian-baryon baseline plus population removes the earlier central overshoot and is not clearly rejected by these coarse held-out band summaries, although it underpredicts INNER on average. It behaves as an ordinary extended gravitating dark component. Adding a population while retaining the entire empirical law instead overpredicts OUTER by about35--37%; the descriptive jackknife residual scores are -3.56 and -3.64. This is not a full-covariance exclusion of all possible distributions.

The gas/R500 Newtonian fit requires q=18.612 and t=.6753. Its population mass *inside* R500 is about10.6 M_gas; its total mass extends beyond R500. Comparing this to the adopted cosmic cold/baryon ratio requires the actual baryon inventory and depletion/assembly history. A cluster gas mass within an aperture is not the cosmic baryon mass, so this is an inventory requirement, not an automatic cosmic-budget exclusion.

At the inherited fitted dwarf core mass, the preferred Newtonian/common population contains approximately19.9 million cores. This number is conditional on that core mass. Neither the fitted M,b nor a decision to retain the law in galaxies but replace its cluster dark component has been derived from the action.

## 4. Dwarf fits and rotation curves are not automatically preserved

The earlier central dwarf core and its successful phenomenological summary statistics remain unchanged as an isolated calculation. A population model must explain why dwarfs have such a central core rather than merely allow one to be inserted.

For illustration, the Newtonian/common cluster fit has central mean population density2.662e-4 solar masses/pc³. Extending *that density* locally to a galaxy would add only3.70e4 solar masses inside321.5pc, and1.115e9 solar masses inside10kpc. The latter raises a200km/s gravitational baseline by only0.60%. Thus a diffuse population can have a small mean effect on those existing fits. This illustration assumes the same density; no galaxy profile was derived or fitted here, and the reciprocal baryonic mediator correction is still required.

But the expected number of dwarf-sized cores inside321.5pc at that density is only.00338. If centres were independently sampled, the chance of even one would be0.34%. This is **not** a predicted dwarf probability: it shows that transferring a diffuse density does not supply the central occupation assumed in the dwarf fits. Biased formation, sinking, capture or a central-plus-satellite rule requires additional dynamics. Likewise, a small mean rotation-force correction is not a test of granular stellar heating or orbital scattering.

As a declared heating scale only, distant Newtonian encounters with m=1.095e7 solar masses, local population density .01solar masses/pc³, relative speed200km/s and impact parameters2r_core..2kpc give total squared-velocity diffusion about295(km/s)²/Gyr. This uses8piG²m rho ln(bmax/bmin)/V, excludes penetrating field encounters and is not an observational exclusion. Actual local abundance and an appropriate stellar-orbit calculation are needed before asserting rotation/disc preservation.

## 5. Population validity: dilute does not mean interaction-free

For the Newtonian/common cluster fit, the central filling fraction N(r_core/b)^3 is .00338. The maximal radial stretching tide in a self-Plummer potential divided by Gm/r_core³ is only6.85e-4, a favorable necessary tidal comparison (not a complete survival proof).

Nevertheless the geometric core-overlap interval near its centre is about26Myr at the beta=1 self-Plummer velocity scale. It is about50Myr for the law-plus-common-population fit. The relative speed estimate uses4sigma/sqrt(pi), a Maxwell approximation at the self-Plummer dispersion. These are encounter/overlap times, not merger or destruction times. Extended field cores may pass through, deform, exchange energy or radiate; a collision kernel has to determine which. It would be unjustified either to declare them destroyed on26Myr or to assume collisionless evolution for billions of years without checking. Cluster baryons and beta change the actual velocities; the quoted estimates isolate the population's self-gravitating scale.

The past spin/survival and baryon-selection work already left initial shapes/spins, capture, transport rates and the matter-state selector unresolved. This population construction does not supply those missing inputs by relabelling the cores as particles.

## 6. Cosmological growth: inertia, formation time and packing

In an imposed EdS background, if all cold mass is already in pressureless cores, the derived two-component diagnostic is

    delta_b''+.5delta_b' = 1.5(f_b delta_b+f_c delta_core),
    delta_core''+.5delta_core' = 1.5 beta(f_b delta_b+f_c delta_core),
    f_b=1/6.364, f_c=1-f_b, prime=d/dln a.

The growing exponent is [-.5+sqrt(.25+6(f_b+f_c beta))]/2. Integrating from z1100 with the same dust initial density/velocity gives:

| beta | retained total amplitude at a=1 |
|---:|---:|
| 1 | 1 |
| .999 | .996665 |
| .99 | .967094 |
| .9 | .711515 |

For99% retention in this idealized full-duration limit, beta>=.996992, or (Mi-m)/m<=.0030167. For the fitted core's polarization profile this requires eta rho_scale<=.0163643 if scalar inertia is absent. This is a conditional bound on an unselected parameter, not its derivation.

An illustrative pressure-moment term with physical sigma=sigma0/a produces additional suppression. At beta1 and k=1/Mpc, sigma0=.1 and1km/s give .999244 and .926631 retention. A collisionless transfer function requires the actual momentum distribution; this moment closure is not that solution. Cluster virial speeds are not primordial cosmic dispersion and were not substituted for it.

### The all-core-from-recombination history is not physically available for these fixed-size cores

With F0=1, fixed m and fixed321.5pc radius, the present mean filling is4.321e-7; at z1100 it would be577. The dilute approximation fails long before that: filling reaches1 at z131.3 and .01 at z27.5. The .01 value is a declared illustration of diluteness, not a fundamental threshold. Evolving core radii/fractions can change the bound but requires a different formation history.

I therefore ran24 two-phase diagnostics: the inherited diffuse compliance equations first, then complete homogeneous conversion to cores at z10,30,100, with beta1 or.997 and either continuous velocity or cold momentum-conserving velocity rescaling. Conversion conserves density; neither prescription inserts extra perturbations. The transition itself remains a conditional matching rule, not an action-derived formation event. z100 is already crowded; z30 is marginal by the illustrative1% criterion.

For the dilute z10 case with continuous velocity:

| beta after formation | k=.1/Mpc | k=1/Mpc |
|---:|---:|---:|
| 1 | .999500 | .955659 |
| .997 | .996472 | .952764 |

Late core formation **does not undo the roughly4.4% small-scale amplitude loss already accumulated in the diffuse phase** at the inherited ell0. Even the beta1 z100 counterfactual gives only .956056 at k1/Mpc. Momentum-conserving matching is recorded separately in the raw output. No full expansion/radiation/CMB calculation is claimed: the preferred-frame Newtonian action does not yet derive a self-consistent FRW parent.

Core granularity also needs a formation model. Uncompensated Poisson centres would have cold-density shot power P=F m/rho_c,0, but local mass-conserving rearrangement gives P=F m/rho_c,0 [1-W(k R_L)]². A top-hat compensation has1-W~(kR_L)²/10, so power is proportional to k^4 at long wavelength. It is incorrect to impose uncompensated shot noise as an unavoidable exclusion without specifying formation.

## 7. What has been established and what remains

Established at this checkpoint: the conditional collective inertia and kinetic equations; an explicit positive spatial/velocity distribution; a concrete nonselection witness even at fixed mass and energy; improved extended cluster-template fits; quantitative occupancy, packing and encounter requirements; and the two-phase growth limitation.

Not established: an action-selected mass spectrum or collapsed fraction; a predicted phase-space distribution; stable moving cores and their collision/formation kernel; a central dwarf occupation mechanism; one baryonic/field solution that retains galaxy rotation laws while producing the cluster population; or relativistic cosmology and lensing.

The strongest surviving route is **a formed, extended cold-core population whose environment and assembly history are computed**, not an arbitrarily added cluster mass profile. The next discriminating calculation must specify the missing inertias/initial state and derive core formation plus core-core/baryon transport from this same action, with mass/energy/momentum accounting. Without those inputs the requested abundance/distribution has multiple physically distinct allowed answers, as the explicit equilibrium counterexample demonstrates. Fitting another profile cannot resolve that nonselection.
