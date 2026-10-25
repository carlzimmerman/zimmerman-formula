# CCT-005: data-constrained supply and profile obstruction

The data do not currently establish a cold-core formation mechanism. They sharpen the missing physics: Sextans' two observed populations require an extended gravitational contribution under this candidate, and the earlier assumed cold reservoir is insufficient for that particular equilibrium interpretation. Simply normalizing one common envelope by formed stellar mass badly overboosts Fornax. Initial supply, assembly and stellar survival still require a predictive calculation.

This packet tests the NEW selective two-potential candidate in ../continuous_cold_envelope_2026_10_24/COUPLING_BRIDGE.md, not v3s, SCT-M, or a particle-dark-matter exclusion. Baryonic gravity is the rational spherical law; cold material sources Newtonian gravity once. All dynamical conclusions assume isolated spherical stationary full Plummer tracer moments. Catalogue/global or fitted dispersions are provisionally identified with these moments. Finite survey coverage, binary corrections, membership, tides, an external field, radius uncertainty and joint parameter covariance are not a likelihood here.

## What was actually constrained

The archived Pace LVD snapshot supplies V luminosity, distance, spherical half-light radius and velocity dispersion. Weisz 2014 cumulative SFH fractions and E-MILES Kroupa SSPs give surviving stellar mass and total formed mass, conditional on the measured HST field's SFH shape being globally representative. The field's tabulated TMass is never called a whole-galaxy mass. The catalogued stellar mass convention is not mixed with the SFH mass estimate.

| Galaxy | Primary surviving stellar mass (Msun) | Formed stellar mass (Msun) | Observed sigma (km/s) | Baryon-only sigma, canonical footing | Minimum additional point-like cold mass (Msun) |
|---|---:|---:|---:|---:|---:|
| Draco | 574,273 | 972,697 | 9.55 | 4.41 | 9.68 million |
| Sextans | 447,179 | 762,042 | 7.9 | 4.09 | 15.47 million |
| Fornax | 19,796,200 | 32,587,047 | 12.1 | 10.79 | 14.56 million |
| Leo I | 3,699,170 | 6,010,621 | 9.29 | 7.15 | 5.61 million |

Sextans' row is an 11.5-Gyr, [M/H]=-2.32 burst sensitivity, not a measured global SFH. It is absent from this Weisz table. Both a0 footings and metallicity/old-burst choices are in results.json. The point-like masses minimize total mass for one tracer moment; finite cores require more. They are neither Wolf enclosed masses nor upper mass budgets. The two-population constraint below supersedes the single Sextans moment for that stronger test.

The earlier repository SFH-adjusted age test (CFG827) already found no significant age/excess trend. We reproduce its three relevant M/L values exactly, not that whole statistical study. A galaxy's age alone cannot be used to select its required cold concentration.

## Sextans: test both populations, not just the global dispersion

[Tolstoy et al. 2025, Table 2](https://arxiv.org/html/2504.02787v1) fits a compact metal-rich population (sigma 7.0 +/- 0.4 km/s, elliptical projected radius 0.339 +/- 0.021 degrees) and an extended metal-poor population (10.5 +0.8/-0.7 km/s, 0.62 +/- 0.05 degrees). Their 0.63/0.37 fractions count stars, not mass. We scan the unknown stellar mass split; we do not substitute the number fractions. The paper notes uncertainty in outer membership.

For a Plummer tracer of scale a, extra spherical cold mass contributes

    Delta sigma_i^2 = integral K_i(r) dMc(r),
    K_i(r) = G/(3 a_i) [1+(r/a_i)^2]^(-3/2).

This follows by the scalar virial theorem and exchanging the enclosed-mass and tracer integrals. The baseline is computed from

    g_law = (gN,b + sqrt(gN,b^2+4 a0 gN,b))/2,
    sigma_b,i^2 = a_i integral_0^(pi/2) sin(theta)^3 g_law(a_i tan(theta)) dtheta.

At r=0, K_MP/K_MR=a_MR/a_MP; at large r the ratio tends to (a_MP/a_MR)^2. It increases monotonically. Thus a positive cold distribution producing residual ratio q must have support at or beyond

    t = [q/(a_MR/a_MP)]^(2/3),
    R_min^2 = (t-1)/(a_MR^(-2)-t a_MP^(-2)).

This is a lower bound on the outermost support, not a lower bound on core radius or proof that all the cold mass is outside R_min. A dense component plus an envelope is allowed in this relaxation.

For any c with positive numerator, positivity also gives a continuum mass bound:

    Mc >= (Delta sigma_MP^2 - c Delta sigma_MR^2)
          / max_{r>=0}[K_MP(r)-c K_MR(r)].

The denominator is maximized over zero, infinity, and its single positive stationary radius, analytically. Optimizing c strengthens a valid inequality; it does not fit an observational confidence region. A shell linear program supplies a nearby constructive moment witness on a finite radial grid. Such shells are not asserted to be dynamically stable cold fields.

For central observed sigmas, all 120 combinations (two footings, six stellar populations, five stellar mass fractions, two radius conventions) require:

* cold support extending to at least 1.42–2.66 kpc;
* total cold mass at least 4.44e8–1.53e9 Msun, according to the corresponding continuum bounds.

Across the additional independent sigma-error corners, feasible cases reach a weaker bound of 1.38e8 Msun and 0.859 kpc. Some corners exceed the positive-shell ratio range. These are sensitivity points, not confidence limits or observational rejection probabilities. Population radius and distance errors are recorded but not sampled. Smooth Plummer cold fits to the central sigmas require much larger scales (12.6–97.9 kpc) and masses (3.68e10–7.65e12 Msun); those huge numbers diagnose the restrictive shape and infinite tracer-tail assumptions, not a measured Sextans infall mass. Eight central cases have no Plummer root below 100 kpc although their positive-shell moment relaxation is feasible.

## Supply: replace the assumed reservoir with an explicit unknown

With an assumed primordial cold/baryon ratio Rc=5.364 and cold retention fraction fc,

    Mc <= Rc fc Mb,initial,
    Mb,initial/Mformed >= Mc/(Rc fc Mformed).

This is a bookkeeping hypothesis, not a cosmological derivation of the candidate field abundance. For Sextans the central two-population bounds require initial baryons at least 92–288 times total formed stellar mass even at fc=1; the sigma-corner minimum is about 26. A larger initial reservoir or cold catchment is not excluded by current stellar data. Conversely, present HI upper limits do not measure that original reservoir. The older nominal ~25–27 million Msun cold stocks and the resulting ~1% escape allowance cannot be promoted to observed constraints.

## Four-dwarf control

As an explicit null, hold each successful central Sextans Plummer cold scale fixed in physical pc, and give each other dwarf the same cold mass per unit formed stellar mass. Recompute its own stellar baseline. Across the tested footings and stellar populations:

| Galaxy | Predicted sigma range (km/s) | Observed catalogue sigma |
|---|---:|---:|
| Draco | 4.86–6.21 | 9.55 |
| Fornax | 41.29–65.24 | 12.1 |
| Leo I | 9.48–13.68 | 9.29 |

This null fails: SFH normalization alone underconcentrates Draco and strongly overboosts Fornax. A universal field action does not require a common physical envelope size or capture efficiency, so this is not an all-history no-go. A successful mechanism must predict differences in structure/capture, not assign four normalizations after seeing the target dispersions.

## Assembly and stellar survival obligations

SFHs constrain when stars formed, not the cold spin, gas radius, gas removal rate, or captured cold inventory. Stellar crossing-time proxies a/sigma are 20, 60, 56 and 24 Myr for Draco, Sextans, Fornax and Leo I. The old SFH bins around 10 Gyr are ~1.1 Gyr wide, so they cannot identify the impulsive vs adiabatic gas cycles relevant to these orbits.

[Bettinelli et al. 2018](https://arxiv.org/abs/1801.08145) inferred an early short Sextans burst from its central region. [Piatti 2026](https://arxiv.org/abs/2606.23216) instead proposes spatially extended activity and a merger interpretation, explicitly noting CMD metallicity model dependence. Its inferred inverse gradient is not silently merged with the spectroscopic radial populations. Neither paper measures cold mass or proves the merger/cold-envelope mechanism. A central SFH cannot be assigned to the entire envelope without a spatial test.

The current equilibrium calculations constrain stellar gravity, not time-dependent heating. Earlier CCT-004 gas pulses failed joint retention/stationarity targets and altered tracer sizes; no untouched-stellar-population result is carried forward. Dense structure formed before the stars, or slowly enough for near-adiabatic stellar response, is a candidate condition, not an established history. Slow evolution conserves actions approximately but still changes stellar structure.

Executable next obligations, in order:

1. Fit survey-selected spatial/velocity/metallicity data for Sextans jointly, including radius covariance, membership and finite-aperture moments. Test whether the strong outer-mass requirement survives; full untruncated Plummer moments are a sensitive assumption.
2. Derive cold capture/retention from the same action and an independently constrained initial gas/catchment and orbital model. Use Mb,initial and fc as explicit nuisance parameters; an N-body dark-halo infall estimate from another model is not raw cold supply.
3. Only after that gate, evolve the data-allowed core+envelope histories with live stellar populations, one shared physical eta/a0, source work, boundary energy/spin flux and mass losses. Cold sources Phi once. Require final profiles, population dispersions/sizes and energy/J balance for all four dwarfs, not a global sigma fit.

Run command and hashes are in CONTRACT.md/receipt.json. Maximum recorded RSS is below 100 MB. This is a completed necessary-constraint calculation, not a completed formation theory.
