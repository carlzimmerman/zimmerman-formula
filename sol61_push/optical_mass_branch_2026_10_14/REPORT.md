# An eV-mass branch permits optical creation, with a transport bottleneck

2026-10-14. Base checkpoint: fbbdfab6a7c8bbc22f9763d215b940a901123cc1.

This is a materially different conditional preparation route: produce a light
neutral mediator coherently using optical fields, then let it decay into cold
carrier pairs. An assigned finite Gaussian source gives approximately 276
mediators/s, but neither a Maxwell-realizable source with that exact envelope,
an empirically admissible parameter set, nor carrier capture has been supplied.
It is a new benchmark branch, not an improvement to the fixed 1 MeV benchmark.

## Why revisit the mass

The repository's cold_field_identity and microscopic_carrier studies considered
eV-scale carriers; they did not establish a unique particle mass. The recent
source studies instead assigned m=1 MeV. That choice required MeV photons.
The earlier coherent_optical_drive calculation drove a low-energy excitation
of a preexisting dense condensate and therefore did not prepare the carriers
from an initially empty dark sector.

Here choose m=1 eV and a distinct neutral scalar R with M_R=2m+2e-9 eV. The
interaction is the same form as the later source branch,

    L_int = -mu R |phi|^2 - g R F_munu F^munu/4,

but choose g=1e-20/eV. This value is an assigned parameter, not a measured or
certified allowed coupling. No claim carries the muon-only MeV model's limited
constraint checks over to a 2 eV mediator. Stellar transport, short-range forces,
cosmology, photon searches, self-scattering, loop matching and mass-gap stability
must be checked in this branch. The eV mass is motivated by an existing repo
alternative, not derived from a fit here. Neither branch is identified with
observed dark matter by this computation.

R decays into phi and anti-phi. The preparation creates zero net global charge
and does not automatically produce a single-sign condensate or the halo state
required by the gravity research.

## Coherent source from light, without a seed condensate

For two equal counterpropagating, parallel-polarized ideal waves, the prior
Maxwell identity gives a spatially uniform oscillatory part of F^2 at twice
the photon frequency. With each beam's cycle-averaged energy density u, the
linear R source has oscillatory amplitude 2g u. Write

    R = [alpha(x,t) exp(-i M_R t) + conjugate]/sqrt(2M_R).

In the undepleted, rotating-wave, nonrelativistic mediator approximation,

    i d alpha/dt = -laplacian(alpha)/(2M_R) + F(x) exp(-i epsilon t),
    F0 = g u/sqrt(2M_R),
    2 omega_photon = M_R + epsilon.

This is a source for the neutral mediator itself; it contains no assumed
carrier density. It can create a coherent state even when the mean occupation
is below one. The dark sector is initially empty.

To calculate finite spatial formation, prescribe the effective envelope

    F(x,y,z)=F0 exp[-(x^2+y^2)/(2 L_t^2)-z^2/(2 L_z^2)],
    L_t=1 mm, L_z=1 m.

The amplitude F0 corresponds to peak intensity 1e12 W/m^2 in EACH beam.
This is a high assigned intensity, not an apparatus recommendation or a
verified available source. The Gaussian envelope is an effective-source
idealization. The plane-wave normalization does not prove that this arbitrary
three-dimensional envelope is an exact Maxwell solution. Counterpropagating
focused modes, diffraction, Gouy phases, finite optical boundaries, losses and
pump coherence must be solved to replace that assumption. The isotropic 1 mm
case below is only a normalization control; it is not claimed as a continuous
optical beam geometry.

## Finite source instead of homogeneous accumulation

Use the symmetric Fourier transform with factor (2pi)^(-3/2). Then

    F_tilde(k)=F0 L_t^2 L_z
               exp[-(L_t^2 k_perp^2+L_z^2 k_z^2)/2].

The asymptotic emission rate into the free mediator continuum is

    Ndot_R = 2pi integral d^3k |F_tilde(k)|^2
                  delta(epsilon-k^2/(2M_R)).

Let k0=sqrt(2M_R epsilon), u=k_z/k0, and

    A_k = 2pi exp(-L_t^2 k0^2)
          integral_{-1}^{1} exp[-k0^2(L_z^2-L_t^2)u^2] du.

The evaluated natural-unit rate is

    Ndot_R = 2pi M_R k0 F0^2 L_t^4 L_z^2 A_k.

Divide by hbar in eV seconds to obtain mediators/s. For L_z=L_t=L,
this reduces to 8pi^2 M_R k0 F0^2 L^6 exp(-L^2 k0^2).
There is no volume-wide t^2 population extrapolation: produced modes propagate
out of the source. The global emission rate and local stored inventory differ.

Choose k0=1/(sqrt(2)L_t), the isotropic Gaussian rate's maximum. This is a
convenient choice, NOT a claimed optimum of the elongated source. It gives

    k0 = 1.3953124595e-4 eV,
    epsilon = 4.8672421492e-9 eV,
    mediator speed = 2.0915e4 m/s,
    isotropic source control = 0.2200 mediators/s,
    elongated source = 275.7504 mediators/s.

The increase comes from the assigned longer coherent interaction region, not
an unrestricted collective target enhancement. The pump supplies the mediator
rest energy. At this rate the emitted mediator power is approximately 8.84e-17 W;
small extracted power does not establish a feasible optical geometry.

## Finite-duration cross-check

For an additional temporal amplitude exp[-t^2/(2 tau^2)], the free-field
population after the pulse is exactly, within the reduced linear model,

    N_R = 2pi tau^2 integral d^3k |F_tilde(k)|^2
                    exp[-tau^2(k^2/(2M_R)-epsilon)^2].

Divide by the squared-drive duration sqrt(pi) tau. For tau*epsilon=10,30,100,
the resulting rate divided by the stationary shell result is respectively
1.0006252, 1.00006945, 1.00000625. The corresponding durations are 1.35,4.06,
13.52 microseconds. This checks the continuum normalization and finite-time
limit independently of substituting a delta function from the outset.

This pulse control neglects decay during pumping. It is directly applicable
to the weaker-width example below; the stronger-width case would need a damped
pulse treatment for an accurate finite-pulse surviving population. The reported
stationary production estimate also neglects finite-width line smearing;
Gamma_phi/epsilon is about 3.7e-4 even in the stronger example. No certified
error bound on this approximation is claimed.

## The daughters meet the assigned cold cut, but escape matters

For exact mediator mass M_R and momentum k0, the daughter's laboratory kinetic
energy extrema are

    K_min,max = sqrt(M_R^2+k0^2)/2 - m
                minus/plus (k0/M_R) sqrt(M_R^2/4-m^2).

A 70-decimal calculation gives 3.1361e-10 through 6.5536e-9 eV. Thus all decay
angles of this monochromatic on-shell source satisfy K<=1e-8 eV for each
daughter. This statement does not assert the same for every finite-pulse tail.
The absolute kinetic-energy cut is retained to compare with prior packages;
at a different mass it corresponds to a different velocity and temperature
interpretation. It is not evidence of trapping or condensation.

For the carrier potential lambda_rep |phi|^4, choose mu^2=lambda_rep M_R^2.
The previous square-completion condition then leaves a positive residual
quartic lambda_rep/2. This is sufficient classical potential stability in the
stated source sector, not a full quantum or empirical certificate. At leading
order beta=sqrt(delta/m),

    Gamma_phi = mu^2 beta/(16pi M_R),
    Gamma_gamma = g^2 M_R^3/(64pi),
    mean flight distance = (k0/M_R)c hbar/(Gamma_phi+Gamma_gamma).

| Assigned lambda_rep | mu (eV) | Rest lifetime | Mean mediator flight | Decay probability in first 1 mm |
|---|---:|---:|---:|---:|
| 1e-6 | 0.002 | 0.370 ms | 7.74 m | 1.292e-4 |
| 1e-15 | 6.325e-8 | 4.28 days | 7.74e9 m | 1.293e-13 |

These quartics are diagnostic choices, NOT experimentally allowed points.
In particular, an eV carrier with strong self-interaction cannot inherit the
MeV benchmark's astrophysical interpretation without a separate analysis.
The resulting stationary production times decay probability is approximately
0.0356 or 3.56e-11 pairs/s in the first 1 mm of trajectory after creation.
That is a path-length diagnostic, not an integrated detector-volume prediction
for this extended source. Branching to carriers is effectively one in both
examples. Eventual decays far from the source do not establish a laboratory
inventory; the long-lived case also needs a finite operation-time treatment.

## What has changed and what has not

The very small MeV target yields do not by themselves exclude an optical
production branch at an independently allowed lower mass. This calculation
supplies an explicit empty-sector source, its finite spatial momentum
selection, a nonzero creation rate, cold daughter kinematics, and a transport
calculation under declared assumptions. It does not rely on a preexisting
condensate to manufacture that same condensate.

The original goal is still unresolved. The central outstanding obligations are:

1. Replace the effective Gaussian source by specified Maxwell modes with the
   same coherent normalization and calculate their actual emitted spectrum.
2. Check this new mass/coupling branch against appropriate constraints and
   radiative mass-gap stability; no old one-observable admission transfers.
3. Produce and capture the daughters within one geometry, including finite
   operation time, transport, reciprocal reactions and carrier self-interaction.
4. Establish the connection of this carrier to the repo's claimed cosmological
   cold component, rather than identifying them solely by terminology.

The next executable calculation is the first: counterpropagating paraxial
Gaussian modes with their actual longitudinal overlap and phase. It will test
whether the new source normalization survives the arbitrary-envelope removal.

## Evidence and formal status

Nine bounded checks cover isotropic reduction, three angular integrals,
Parseval normalization, finite-pulse convergence, high-precision daughter
energy conservation, and both positive residual quartics. run/manifest.json
pins the code, results and three source reports. These are self-reviewed
mathematical checks of a proposed model, not observations.

No new Lean certification of the optical field or scattering calculation is
claimed. The prior stable_source_completion certificate covers its stated
polynomial condition; the new finite-source and transport derivations remain
analytical and numerically checked, not fully formalized.

Reproduce:

    python3 sol61_push/optical_mass_branch_2026_10_14/check.py /tmp/optical_mass_results.json
