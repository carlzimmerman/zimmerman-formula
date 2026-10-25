# CCT-006: Sextans survey coverage and the capture gate

The large extended-mass preference survives the tested survey treatment, but the previous 440-million-Msun hard floor does not transfer to this likelihood. Actual-position velocity fits prefer a few hundred million Msun in the tested cold-profile family. Early capture remains energetically conceivable with a much larger gas/cold catchment than the earlier nominal reservoir. Neither permanent capture, the four-galaxy selector, nor stellar survival is demonstrated.

This packet is for the NEW selectively coupled continuous-field candidate in CCT-003. It is not a result for current v3s, AeST or retired SCT-M. Newtonian cold mass is counted once. The cold sector is neutral under the extra baryon-sourced potential Xi by hypothesis.

## Actual coverage test

We downloaded [CDS J/A+A/698/A53](https://doi.org/10.26093/cds/vizier.36980053), retained its metadata and every member row, and fitted conditional velocities at actual measured positions. See SOURCES.md for the exact queries and catalogue/publication discrepancies. The explicit quality subset contains 298 unique stars. Its median circularized radius is 552 pc; 90% are within 1091 pc; 12 are beyond 1500 pc. The maximum is 3629 pc. No missing central spectra were synthesized, and Walker note-field velocities without errors were not treated as new reliable measurements.

The [source survey](https://arxiv.org/html/2504.02787v1) reports uneven coverage and discusses the central gap and membership ambiguity. Our selected catalogue subset is not an exact reproduction of its published sample. Conditional-on-position likelihood avoids uniform spatial weighting only when selection at fixed position/population does not bias the velocity distribution. Published membership already uses velocity information; the documented broad velocity window is modeled with Gaussian truncation, but the full membership/quality selection is not reconstructed.

For each stellar population, the Jeans pressure is computed from

    p_i(r) = r^(-2 beta) integral_r^infinity nu_i(s) g_total(s) s^(2 beta) ds,
    sigma_los,i^2(R) = integral_0^infinity [1-beta R^2/(R^2+z^2)] p_i(sqrt(R^2+z^2)) dz
                      / integral_0^infinity nu_i(sqrt(R^2+z^2)) dz,
    g_total = g_law(baryons) + G Mc r/(r^2+b^2)^(3/2).

Thus observed stars are compared to their local predicted velocity distributions, rather than identifying a selected sample's dispersion with a full infinite-Plummer virial moment. Metallicity errors and a two-population mixture are included. Positions are circularized with catalogue ellipticity; first-order perspective motion is removed. Beta=0 and -0.5 are separate tests, not an anisotropy posterior.

Continuous best fits (rounded; not confidence limits):

| Stellar tracer assumption | Canonical Mc | Canonical cold scale b | Alternate Mc |
|---|---:|---:|---:|
| Full Plummer, isotropic | 425 million Msun | 1.714 kpc | 427 million Msun |
| Full Plummer, tangential beta=-0.5 | 231 million Msun | 1.234 kpc | 229 million Msun |
| Isotropic, smooth 3-kpc stellar taper | 818 million Msun | 2.230 kpc | 848 million Msun |

Reprofiling after removing all 12 stars beyond 1500 pc gives 432/441 million Msun on the two footings. Allowing a fixed 5% uniform-velocity contamination component gives 401/405 million Msun. These are limited sensitivities, not a complete foreground/binary analysis. A taper changes the Jeans pressure needed to support the same inner velocities, so truncating a tracer does not necessarily lower the inferred mass.

For fixed canonical cold masses, with scale and mixture nuisance parameters reprofiled:

| Fixed Mc | 2 Delta negative-log-likelihood, beta=0 | beta=-0.5 |
|---|---:|---:|
| 25 million Msun | 93.22 | 64.88 |
| 50 million Msun | 41.06 | 23.75 |
| 100 million Msun | 13.78 | 5.26 |
| 200 million Msun | 2.71 | 0.11 |
| 400 million Msun | 0.013 | 1.21 |
| 800 million Msun | 1.00 | 4.55 |

No significance level is assigned: fixed radii/metallicity mixture/baryon mass, selected membership and incomplete distribution-function/foreground treatment prevent that interpretation. In particular 200 million is close to the optimum in these tests, so CCT-005's 440-million minimum is not established as a survey-corrected bound. Conversely, the earlier 25-million reservoir is a poor fit in the tested family. The trillion-Msun smooth-profile extrapolations from demanding exact global population moments are not needed by this survey likelihood.

## Capture work and supply

For time-independent linear wave Hamiltonian H, the bound-state spectral projector commutes with H: initially incoming scattering waves cannot acquire bound-state amplitude from a static well alone. This does not prohibit nonlinear self-gravitating collapse with escaping positive-energy waves. That process requires its own mass/energy/spin ledger.

For a changing baryonic potential the cold field has external work

    dEc/dt |_external = integral rho_c partial_t Phi_b dV.

An optimistic scenario contracts a fixed gas mass Mg from scale 5a to a while incoming material is near radius b. In the narrow-packet/trajectory limit the energy decrement is

    |Delta epsilon| = G Mg [1/sqrt(b^2+a^2)-1/sqrt(b^2+25a^2)].

Binding an incoming speed v_infinity needs this decrement to exceed v_infinity^2/2. This is a deliberately favorable timing/radius calculation, not a general capture theorem or an efficiency prediction for a coherent field.

Using the isotropic canonical Sextans profile and a matched-scale 32.9-million-Msun compact Draco target:

| Target | Required cold mass | Minimum catchment baryons at cold/baryon=5.364 and full cold retention | Gas contraction mass to bind v_inf=10 km/s at b |
|---|---:|---:|---:|
| Draco | 32.9 million Msun | 6.12 million Msun | 4.40 million Msun |
| Sextans | 425 million Msun | 79.2 million Msun | 51.7 million Msun |

At 20 km/s the gas-work requirement is four times larger. Sextans' minimum baryon catchment is about 93 times the assumed ~0.847-million-Msun formed stellar mass. That formed mass uses an explicitly approximate surviving fraction 0.59; it is not a measured global Sextans SFH. The primordial cold/baryon ratio is also a hypothesis, not a prediction of this action. Present HI upper limits do not measure the original catchment.

Gas contraction can make the energy temporarily negative. If gas later expands or escapes, it returns positive work to the cold field. Permanent retention therefore needs cold self-binding and/or independently tracked positive-energy wave escape; neither is proved by this work budget. Energy needed to move the gas is not provided by prescribing its scale change.

An energy-and-mass budget does have a nonempty window. For a stationary Plummer cold density, Wself=-3 pi G Mc^2/(32b). Including only the remaining Newtonian stellar potential, the virial energy per cold mass is

    e_bound = -3 pi G Mc/(64b) + <Phi_star,N> + <r g_star,N>/2.

For Sextans it is about -157.7 (km/s)^2. If initially dispersed incoming material has e_in=v_inf^2/2, and outgoing waves have asymptotic e_out=v_group,out^2/2, zero net baryonic work requires

    (1+q) e_in = e_bound + q e_out,
    q = M_out/M_final = (e_in-e_bound)/(e_out-e_in).

The incoming energy of the subsequently escaping mass must be included. At v_inf=10 km/s:

| Outgoing group speed at infinity | Escaped/final mass | Initial cold mass needed | Fits the assumed 200-times-formed baryon catchment? |
|---|---:|---:|---|
| 20 km/s | 1.384 | 1.013 billion Msun | No |
| 30 km/s | 0.519 | 645 million Msun | Yes |
| 50 km/s | 0.173 | 498 million Msun | Yes |

That catchment supplies at most 909 million Msun of cold material under the assumed ratio, giving a minimum outgoing speed about 21.6 km/s for this zero-net-work budget. The 30-km/s case releases about 221 million Msun in waves and retains 425 million; it needs about 120 million Msun of original catchment baryons if all incoming cold material is drawn from that catchment. This is a conservation-compatible candidate, not a capture solution: the field must actually excite the escaping modes, produce the target profile and carry the required spin. Positive net work from gas loss raises the required escaping mass/energy; negative net source work lowers it. The outgoing speed is an asymptotic wave group-speed parameter, not an observed ejecta measurement or an assumed collision.

## Four-dwarf selector: two unresolved possibilities

For the concrete target profiles above and stellar-scale cold profiles matching the single global Fornax/Leo I moments, assume the same initial baryons =200 times formed stellar mass. The necessary cold retention fractions are approximately:

    Draco 0.0315; Sextans 0.467; Fornax 0.00141; Leo I 0.00296.

This is a required selectivity pattern, not a predicted capture history. An initial catchment of only 10 times formed mass cannot supply the Sextans target even with full cold retention. SFH data alone do not determine these initial catchments or fractions. Total formed stellar mass is not itself a strict lower bound on a one-time gas reservoir because recycling is possible; the bookkeeping code does not make that substitution.

Alternatively, equal capture can leave much of the cold material far outside the stars. With retention 0.5 and the same 200-times-formed catchment, matching each single global moment requires approximately:

| Galaxy | Total captured cold mass | Required Plummer envelope scale |
|---|---:|---:|
| Draco | 522 million Msun | 1.01 kpc |
| Fornax | 17.5 billion Msun | 13.5 kpc |
| Leo I | 3.22 billion Msun | 3.32 kpc |

These are algebraic moment constructions, not acceptable dwarf models established by data. They show why central velocities alone do not measure total captured mass. Radial profiles, tides/orbits, cold support/stability and total catchment budgets must accept or reject these extended envelopes. The enlarged Draco envelope also does not establish its required compact central profile. Equal capture and equal concentration must not be conflated.

## Stellar disturbance and spin

We tested a stationary circular-orbit ensemble in the initial baryon-only potential, with 128 orbits per tracer population and a Plummer radial distribution truncated at 6a. This is a controlled response example, not an isotropic fit to the observed velocity catalogue. Add the prescribed target cold profile, either instantaneously or through the exact adiabatic circular mapping L^2=r^3 g(r). Results:

| Galaxy/population | Median radius after adiabatic growth / before | Late median radius after an impulse / before |
|---|---:|---:|
| Draco | 0.525 | 0.694 |
| Sextans compact population | 0.723 | 0.745 |
| Sextans extended population | 0.618 | 0.689 |
| Fornax | 0.896 | 0.906 |
| Leo I | 0.783 | 0.823 |

Slow growth is not undisturbed growth: it preserves circular angular actions while contracting the stars. The impulsive cases also change velocity variance. Initial stellar sizes are unknown, so this does not exclude all late-growth histories; larger birth distributions could evolve toward current sizes. It rejects treating the already-observed stellar structure as unaffected by such growth. Post-impulse orbit-energy errors are below 3e-8 on the recorded scale. This is only the stellar ledger in a prescribed potential, not the total energy of a captured cold field and moving gas.

Spherical gas growth also provides no angular torque: dJz/dt=-integral rho_c partial_phi Phi_b dV=0. Thus it can supply negative work without solving the incoming spin problem. In a spherical wave decomposition, marginal access to a core radius requires

    eta^2 l(l+1) < -2 r_core^2 Phi_Newtonian(r_core),

with the cold field's Newtonian stellar+cold potential, not the extra Xi felt by stars. This barrier is a necessary diagnostic, not a bound-state existence proof. Low-spin initial modes, nonspherical torque, or computed angular-momentum-carrying waves are still required.

## Remaining executable obligations

1. Reconcile the online catalogue counts and metadata caution with the published quality pipeline; add Walker spectra with actual errors, a foreground/binary model, variable anisotropy and photometric-radius covariance. Refit before publishing a lower mass bound.
2. Test pre-stellar gas deepening followed by gas loss in the same self-gravitating cold-field action. It must reproduce the required final mass/profile, show incoming-to-bound mode transfer, pay source work, resolve escaping waves, and export or retain the incoming spin. A static-well scattering run with initially zero bound projection is the null control.
3. Apply the same capture prescription to the four observed stellar histories/catchments and live stellar populations. Fornax/Leo I must either reject capture or retain an observationally acceptable extended envelope. Initial conditions cannot be chosen from the desired final cold masses without labeling the exercise an inverse construction.

Commands (one thread, below 100 MB recorded RSS):

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 sol61_push/cold_survey_capture_2026_10_24/survey.py
    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 sol61_push/cold_survey_capture_2026_10_24/capture.py
    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 sol61_push/cold_survey_capture_2026_10_24/verify.py

Raw data, selected IDs, fit grids, profile likelihood ordinates, hashes and checks remain in this directory. No monitor, heavy run, frozen criteria, publication, chat message or external push was created.
