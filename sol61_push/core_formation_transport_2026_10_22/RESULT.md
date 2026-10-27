# Core formation and transport: binding favours growth, not a selected mass

CFT-20261022; base6502ef90a995619f6c40ccaa340ca52be52c251d. Continuation of moving_core_population_2026_10_22. The requested joint mechanism is **not established**. This checkpoint derives a new obstruction to passive mass selection and tests a possible gravitational transport route, with energy conservation and baryonic response retained.

The strongest result is an action-level inequality: **the energy per unit mass decreases along a differentiable stationary passive-core mass branch.** The action can support a radius at fixed inventory without choosing a preferred inventory. A dwarf-sized core can merge into a more tightly bound double-mass core; neither a fixed-mass radius nor the earlier fitted population is a mechanism that stops that growth. Gravitational transport has the right qualitative scale dependence to distinguish some dwarf outskirts from galaxies and clusters, but its controlled approximation does not reach the central dwarf regime and its heating cannot be omitted.

These conclusions are self-reviewed. Lensing, empirical law-plus-core tests, and the imposed cosmological history retain the predecessor's stated limitations.

## 1. Binding and mass selection derived from the action

Consider isolated finite-mass, static pure cold matter in the passive X=0 branch. Require fields to decay, chi->chi0, and all displayed energies and integration-by-parts boundary terms to be well defined. Include the optional positive polarization and scalar gradient energies. Let

    U = Newtonian gravitational self-energy (<0),
    V = integral e²/(2chi),
    Z = integral mu_phase²(chi-chi0)²/2,
    J = integral Dchi |grad chi|²/2,
    T = integral gamma |grad P|²/2,
    B = integral W,  D = integral w W_w,
    W=(a0²/K)[-w-ln(1-w)],  w=K|P|/a0<1,
    E=U+V+Z+J+T+B,  H=chi0 integral h², h=e/chi.

Fixed-mass homology rho(r)->t³rho(tr), P(r)->t²P(tr), chi(r)->chi(tr) is an admissible variation. Stationarity gives the virial identity

    U+3V-3Z-J+3T+2D-3B=0.

Cold chemical equilibrium and the field equation, integrated over the full interior **and exterior**, give

    mu_c M = 2U+2V+D+2T.

Multiplying the passive scalar equation by chi-chi0 and integrating gives

    V=2J+2Z+H/2.

Consequently,

    E = -2J-H-2T+4B-2D < 0,
    mu_c M-E = -4J-2Z-H-2T+2B-D < 0.

For the logarithmic W, 2W-wW_w vanishes at w=0 and has derivative proportional to -w²/(1-w)², so D>2B for a nontrivial polarization profile. All other displayed contributions have the required nonnegative sign. The inequalities are conditional on stationary solutions with the stated boundaries; they do not assert that such solutions exist for every mass or gradient coefficient.

Along a differentiable stationary branch with couplings fixed, dE/dM=mu_c. Therefore

    d(E/M)/dM = (mu_c M-E)/M² < 0.

There is no interior minimum of binding energy per mass that could select a preferred core mass on that branch. Positive gradient energies do not reverse this inequality. If masses M and2M belong to the same connected increasing-mass branch, E(2M)<2E(M): merger binding can be released, provided the material and an energy-export channel are available. This is **not** a prediction of a merger rate, nor a claim that cold mass appears without supply.

For fixed chi and zero gradient terms, the same homology can have positive second derivative at fixed M: the W expansion is a sum of positive terms t^(2n-3)w^n/n, n>=2, and mismatch energy scales as t³. Thus a positive restoring response of radius at fixed mass is compatible with the absence of a preferred mass. A full stability spectrum remains unproved.

Scope matters. Baryonic confinement, driven X fields, angular momentum, mass/energy fluxes or nonstationary histories add terms to these identities. They are possible ways to alter the conclusion, not effects already included in this passive theorem. A branch endpoint or maximum supported mass can depend on the free phase parameters; it is not automatically a formed mass spectrum or the empirically fitted dwarf mass.

### Numerical energy audit and an actual merger comparison

Twelve matched pure-cold cores (s0=.03,.1,.3,1,3,10; lambda0,1) satisfy the virial and chemical identities, with maximal relative residual below5e-8. Energies include the vacuum polarization/mismatch tail. Finite differences independently reproduce dE/dM=mu_c. The deliberate omission of exterior field energy is a separate failure control.

For the canonical fitted dwarf core:

| quantity | progenitor | equal-mass merger remnant |
|---|---:|---:|
| material mass | 1.095e7 solar masses | 2.190e7 solar masses |
| cold edge | 321.5pc | 384.3pc |
| central dimensionless h | .148204 | .238131 |
| E/M in units a0 ell0 | -.028323 | -.053262 |

The remnant was solved at **twice the mass**, not twice the central amplitude. Two progenitors at rest and infinitely separated release1.382e45J if they settle into that remnant with the same total mass. This is31.725(km/s)² per unit initial total mass. Incoming orbital kinetic energy must also be exported to obtain a static remnant. If mass is ejected, the final mass/energy bookkeeping changes; no ejection fraction was supplied.

## 2. What would actually capture or move a core?

The action's far-field pair interaction is Newtonian in the beta~1 limit. A core in a specified light, collisionless Maxwellian background therefore has the usual gravitational-wake reduction,

    a_df = -4piG² m rho lnLambda F(X) vhat/v²,
    F(X)=erf(X)-2X exp(-X²)/sqrt(pi), X=v/(sqrt(2)sigma).

This imports a **bath hypothesis**, not a new fundamental dissipative vertex. It does not establish that the cold fluid is such a bath. Hot gas requires its own pressure-dependent wake response. Equal-mass cores require both drift and diffusion; applying friction alone to all of them would create an artificial cooling mechanism. The fluctuation/drag relationship is explicit in [Chandrasekhar's original treatment](https://blackholes.tecnico.ulisboa.pt/gritting/pdf/astrophysics/Chandrasekhar_Dynamical_Friction.pdf). [Ostriker's comparison, equations12 and16](https://arxiv.org/pdf/astro-ph/9810324), distinguishes collisionless and gaseous wakes and their energy transfer. Exact source/applicability checks are in LITERATURE.md.

For a light-particle singular isothermal bath with circular speed Vc and sigma=Vc/sqrt2,

    dr/dt = -Gm lnLambda F(1)/(Vc r), F(1)=.427593.

The familiar constant-log scale is t~1.1693 Vc r²/(Gm lnLambda). To avoid claiming arrival at the centre from a formula that ceases to apply, the calculation instead uses bmin=max(2r_core,Gm/Vc²), a radius-dependent logarithm, and stops at

    r_stop=max(3bmin,10Gm/Vc²).

These are declared conservative scale-separation and small-perturbation requirements, not sharp physical boundaries.

| Vc | starting radius | result within the declared regime |
|---:|---:|---|
| 10km/s | 1kpc | not in controlled regime |
| 20km/s | 1kpc | not in controlled regime |
| 30km/s | 3kpc | 2.87Gyr to1.93kpc; central phase unresolved |
| 200km/s | 10kpc | 210Gyr to1.93kpc |
| 1000km/s | 500kpc | about994,000Gyr to1.93kpc |

The examples optimistically assign the supporting halo density to the light bath. If only a fraction contributes to the wake, drag is weaker. They show a potentially useful scale separation, not predicted orbital histories. A dense early phase, a gaseous wake or another background can change the rates, but must be derived and constrained separately.

The inherited ten-object MW calibration has full-core/half-light dynamical-mass ratios0.116--10.76. None lies in the declared<=.1 weak-perturber regime at its half-light radius. This is an audit of treating the whole extended core as a point perturber, **not** a rejection of its static enclosed-mass fit. Finite core size also matters. The nonlinear central problem cannot be solved by extrapolating the small-perturbation drag formula.

### Reciprocal stellar heating cannot be removed from the sinking calculation

For an illustrative circular path from3r_half to r_core in a flat Vc=sqrt3 sigma potential, the orbital energy transfer is

    DeltaE = m Vc² ln(3r_half/r_core),
    DeltaE / K_stars = (2m/Mstar) ln(3r_half/r_core),
    K_stars=1.5 Mstar sigma².

The path exists for nine of the ten inherited objects; the remaining one is already smaller than the assumed endpoint. Ratios range2.39 (Fornax) to340 (LeoIV), with Draco33.5 and UrsaMinor48.4. To keep stellar kinetic changes below a declared10%, the stellar deposition fraction would have to be below4.2% down to0.029%, respectively. These are energy-response budgets, not disruption thresholds or a likelihood. If a stellar wake supplies the drag, its reaction energy cannot simply be discarded. Another sink—diffuse cold matter, escaping material, gas cooling or field radiation—needs an actual transport calculation.

## 3. Capture can distinguish low and high speeds, but still does not select mass

At first contact of two equal cores, the point-gravity escape speed is17.12km/s. The minimum fraction of their contact orbital kinetic energy that must be removed to make a bound pair is

    f_loss >= v_infinity²/(v_infinity²+v_escape²).

For20km/s encounters this is about58%; at1000km/s it exceeds99.97%. A merger to a static remnant must additionally export the released internal binding energy. This helps explain why geometric overlaps cannot be equated with mergers: the prior cluster overlap interval of order26Myr is not a capture time. The action still needs to determine inelastic energy transfer, excitation, ejection and radiation in an encounter.

The same distinction prevents imposing a drag-only evolution on a monodisperse population. Equal-mass diffusion counteracts drag in thermal equilibrium; there is no automatic massive-versus-light segregation among identical cores. An order-of-magnitude pure-gravity finite-N relaxation scale for the fitted~20-million-core cluster is about53,000Gyr. It will not choose the profile by ordinary two-body thermalization over a cosmic age. This does **not** exclude collisionless assembly or violent relaxation in a changing potential; those depend on initial conditions and cannot be replaced by the relaxation estimate.

## 4. Does the action provide the required energy-export channel?

In fixed-chi vacuum, linearizing about P=0 gives

    eta omega_T²=K,
    eta omega_L²=K+A k², A=1/chi0.

With no polarization gradient term, transverse oscillators have no spatial group velocity; the longitudinal propagating channel has gap omega0=sqrt(K/eta) and asymptotic speed cL=sqrt(A/eta). Positive added gradient stiffness changes propagation but does not remove the k0 gap.

At eta rho_scale=.0163643, the predecessor's permissive99%-retention all-core benchmark limit, the fixed-chi numbers are

    omega0=.6474/Myr, cL=278.8km/s,
    core Omega_dyn=.03850/Myr=.0595 omega0.

A20km/s passage has characteristic frequency v/r_core about.0983 omega0. A monochromatic linear perturbation at that frequency cannot carry outgoing longitudinal vacuum radiation. This obstructs assuming efficient *slow, linear* polarization-wave cooling. It does not prove zero radiation from a finite collision pulse: high-frequency tails, nonlinear excitations, scalar/mediator channels and cold-matter ejection are not computed here.

The same permissive eta makes1000km/s cluster motion faster than cL, so the previously used slow, adiabatic core-motion ansatz needs another check. Requiring cL>=1000km/s would demand eta rho_scale<=.0012721 and would raise the gap further. There is no algebraic contradiction with the growth bound—eta can be smaller—but its value and the capture response are not derived. Efficient damping cannot be introduced as a free drag term without its reciprocal energy flow and effect on formation/growth.

## 5. A merger changes the fits, but one merger is not automatically excluded

The actual doubled-mass remnant was substituted into the earlier **phenomenological** law-plus-core comparison without refitting any data. It remains a sensitivity calculation, not a solution of the nonlinear baryon/field problem and not a claim that every dwarf merges once.

| canonical statistic | progenitor | double-mass remnant |
|---|---:|---:|
| MW calibration RMS ln dispersion residual | .2156 | .2427 |
| M31/field17 mean ln residual | +.0551 +/- .0542 | -.0594 +/- .0518 |
| literature-sigma UFD21 mean ln residual | +.0923 +/- .1157 | -.0214 +/- .1229 |
| SPARC rotating dwarfs56 mean dex residual | +.0267 +/- .0220 | +.0223 +/- .0219 |

One mass doubling is not decisively excluded by these coarse summaries. This is useful: the empirical mass fit is not a sharply measured universal mass. It also means observations do not supply the missing microscopic stopping rule. Repeated mergers, occupations and baryonic heating still require a derived history.

The polarization inertial coefficient changes from.184347 to.197531 in (Mi-m)/m=coefficient*eta rho_scale. At the same illustrative eta and a conditional diffuse-to-core conversion at z10, retained growth changes from .996464 to .996248 at k=.1/Mpc, and .952756 to .952550 at k=1/Mpc. The merger-induced correction here is small; the earlier diffuse growth loss remains dominant. Even the beta1 late-conversion limit retained only .955659 at k1. No formation/transport mechanism has been shown to repair that loss, and no full FRW or CMB test follows from this imposed history.

### Sample-label correction

Auditing the inherited calibration identities found LeoIV and CanesVenaticiII among its ten MW objects. Older descriptions calling all ten 'classical dwarfs' were inaccurate. The numerical selection and fits are unchanged; the report now calls it the inherited MW calibration sample. The21-object literature-sigma UFD comparison is explicitly disjoint from that calibration, so this wording correction does not uncover calibration/test overlap.

## 6. What remains viable

The new result is stronger than “formation parameters are missing”: the passive stationary binding energy itself does not contain a preferred finite core mass. It favours more binding per mass on larger-mass branches, including the explicitly solved merger. A viable formation model therefore needs a **dynamical arrest or inventory mechanism**, not merely the existence of a static core.

Gravitational transport remains a plausible part of environmental sorting: slow, light-background interactions can act more rapidly in some dwarf outskirts than in massive galaxies/clusters. It has not delivered the needed central occupation, halt mass or cluster profile. The centre is nonlinear; the identity of the receiving bath and its heating matter; equal-mass diffusion cannot be dropped; and low-frequency radiation is not automatically available.

The next meaningful route must change a named missing piece: derive a driven or angular-momentum-supported arrest from the reciprocal action; or specify admissible initial data and field coefficients and compute nonlinear collapse/encounters with outgoing energy and momentum. A fitted central mass, a friction coefficient chosen by object class, or a collisionless equilibrium profile would bypass rather than solve these requirements. Within the passive binding plus generic gravitational-drag construction tested here, no derived common selector has been obtained.
