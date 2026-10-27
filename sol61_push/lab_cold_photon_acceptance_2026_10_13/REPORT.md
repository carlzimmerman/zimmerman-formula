# A narrow pair resonance does not ensure laboratory-cold output

2026-10-13. Base checkpoint: 55f48b1fb1fed4a4001a2364f90c183e5a6ee9a6.
This returns to the fixed-coupling photon production route, avoiding the
artificial switch in the preceding surrogate. It adds laboratory momentum
acceptance and a finite-bandwidth rate. The specified continuous-beam benchmark
is quantitatively ineffective; this is not a no-go theorem for all sources.

## Model and the separate laboratory requirement

Retain the hypothetical reduced muon-loop pole from
../ordinary_lepton_source_2026_10_13: m=1 MeV, M=2m+delta,
delta=2e-9 eV, and equal vacuum partial widths
Gamma_gamma=Gamma_phi=3.41884037e-13 eV. These are assumed particle parameters,
not measurements. Use independent unpolarized incoming photons and isotropic
scalar decay. No new coupling or controllable switch is added.

For a pole at rest, each daughter has Kstar=delta/2=1e-9 eV. For source total
momentum P and decay angle u=cos(theta*) relative to its boost, exact kinematics
gives

    K_plus/minus = sqrt(M^2+P^2)/2 - m +/- (P/M) sqrt(M^2/4-m^2) u.

In the nonrelativistic final-state regime this becomes

    K_plus/minus = Kstar + P^2/(8m) +/- P sqrt(2m Kstar)/(2m) u.

The common boost is not removed by requiring the pair invariant mass to lie on
the pole. To quantify this, choose Kcut=1e-8 eV as a diagnostic upper bound
on EACH daughter's laboratory kinetic energy. It is not a surviving material
wall height from the earlier excluded charged-messenger model.

Let r=sqrt(2m Kstar), R=sqrt(2m Kcut), and q=P/2. Both daughters pass if

    r^2+q^2+2rq |u| <= R^2.

For isotropic decay, u is uniform on [-1,1], so the accepted fraction at fixed P is

    A(P)=1,                                  P<=2(R-r),
        =(R^2-r^2-P^2/4)/(P r),               2(R-r)<P<2sqrt(R^2-r^2),
        =0,                                  P>=2sqrt(R^2-r^2).

Numerically the first boundary is 0.193400 eV and the final boundary is
0.268328 eV, in c=1 momentum units. A high-precision exact Lorentz check over
16 representative momentum/angle points gives a maximum nonrelativistic
energy error of about 1.03e-22 eV. This checks the chosen low-momentum regime,
not arbitrary boosts.

An independent geometric check integrates A over total momentum. The result is
eight times the intersection volume of two radius-R spheres separated by 2r:

    integral d^3P A(P)=16pi/3 (2R+r)(R-r)^2=0.0513213 eV^3.

## Beam phase-space assumptions

For nearly opposing photons, to leading order

    P_parallel ~= E1-E2,
    P_transverse ~= m psi,

where psi is the two-component net angular mismatch. Assume each beam's
energy has independent Gaussian RMS sigma_E=5000 eV about the required
central energy. Then the energy sum and difference each have RMS
sqrt(2)*sigma_E, and are independent. Assume each component of psi is also
independent Gaussian, with RMS sigma_psi, independent of energy.

Integrate A(|P|) against the resulting anisotropic Gaussian, with longitudinal
RMS sqrt(2)*sigma_E and transverse component RMS m*sigma_psi. The result is
conditional on these independent errors. Real Compton beams have energy-angle
correlations; this calculation does not replace their measured joint
distribution. Selecting a narrow invariant mass does not by itself select a
narrow energy difference. The tiny boost-dependent shift in the energy sum is
neglected relative to the broad assumed spectrum in this leading approximation.

| Net angular component RMS (rad) | Both daughters below Kcut |
|---:|---:|
| 0 | 2.5783e-5 |
| 1e-8 | 2.5733e-5 |
| 1e-7 | 1.9452e-5 |
| 1e-6 | 4.5576e-7 |
| 1e-5 | 4.6078e-9 |
| 1e-3 | 4.6083e-13 |

These are production-energy acceptance fractions, not trapping probabilities.
The zero-angle case isolates the energy-imbalance obstruction. In the broad
three-dimensional momentum limit, the fraction approaches the accepted
momentum volume times the Gaussian density at zero; that independent
asymptotic check is included.

## Bandwidth and luminosity

In the leading constant-width narrow-pole approximation, the integrated area is

    I_sigma = pi Gamma_gamma sigma_peak = 6.56934e-38 m^2 eV,
    sigma_peak=2pi (hbar c)^2/M^2.

This uses equal partial widths, hence energy half-width Gamma_gamma. The
bandwidth-averaged pole cross section for sigma_sum=sqrt(2)*sigma_E is

    sigma_bar ~= I_sigma/[sqrt(2pi)*sigma_sum] = 3.70635e-42 m^2.

The prior threshold-resonance package supplies the isolated-pole normalization.
Here the running daughter width and off-resonant continuum are not integrated
over the full broad spectrum. These numbers describe the leading narrow-pole
contribution, not a certified total scattering rate. Gamma_gamma/delta is
about 1.7e-4, so the constant-width approximation is local to the pole;
numerical quadrature precision is not an error bound on omitted physics.

Choose, explicitly as an assumed continuous-beam benchmark, F1=F2=1e8
photons/s, common area A=1 mm^2 and overlap length ell=2 mm. For opposing
uniform beams the luminosity is

    L_CW=2 ell F1 F2/(A c)=1.33426e11 m^-2 s^-1.

The leading pole rate before the cold cut is then only

    rate_all=4.94522e-31 pairs/s.

After the cut it is 1.27503e-35 pairs/s even at zero angular mismatch,
2.25383e-37 pairs/s at sigma_psi=1e-6, and 2.27867e-39 pairs/s at 1e-5.
For this assumed geometry, spectrum and constant particle parameters, there is
no useful source. Rate scaling is proportional to F1*F2*ell/A for continuous
uniform beams. Pulsed beams require the actual space-time overlap integral;
using average fluxes alone can miss a bunching enhancement. No universal
bound on all pulse structures or all photon sources is claimed.

## Empirical source context, checked 2026-10-13

The official [HIgammaS beam table, May 2020 v2.5](https://tunl.duke.edu/sites/tunl.duke.edu/files/documents/HIGSBeamParameters.pdf)
labels its values flux-performance projections. For 1-2 MeV it lists total
flux 1e8-4e8 photons/s and collimated flux 6e6-2.4e7 at 5% FWHM. Higher
resolution trades away flux. The current [2026 user call](https://tunl.duke.edu/higs-pac-2026)
advertises roughly 2-110 MeV availability. The older table therefore does not
establish an available pair of opposing 1 MeV beams for this calculation.

The official [ELI-GBS specifications](https://www.eli-np.ro/gsd_second.php)
describe implementation as underway and specify 1-19.5 MeV, bandwidth no
greater than 0.5% FWHM, peak spectral density at least 5000 photons/(s eV),
and divergence no greater than 1.5e-4 rad FWHM. These are specifications, not
a measured joint energy-angle distribution or a demonstration of the required
two-beam collision. We do not substitute FWHM for RMS or combine separately
quoted total flux and bandwidth as if they established the modeled spectrum.

The F=1e8/s and sigma_E=5000 eV calculation is an illustrative assumption,
not a forecast for either facility. Facility numbers are context for replacing
the earlier wholly stipulated megawatt ultranarrow beams; they are not evidence
for R or phi. No contact with either facility was made.

## Verification and next research decision

Eleven checks pass: accepted momentum volume against sphere-intersection
geometry, exact Lorentz control, independent pole-area integral, six probability
range checks, broad-distribution asymptotics and the sampled angular-spread
ordering. Acceptance.lean checks the exact real-algebra equivalence of requiring
both a+b and a-b to lie below a limit versus requiring a+|b| to do so. It does
not certify beam assumptions, integrals, particle existence or a device.

The physical source decision changes: the specified two-dilute-photon-beam
benchmark is not worth pursuing as a manufacturing scheme. Changing this
conclusion requires an explicit luminosity/spectral-density improvement or a
different production channel, with its own laboratory momentum acceptance.
Replacing one dilute beam by an ordinary target is a distinct untested route;
it must supply the scalar production matrix element, recoil and cold acceptance,
not merely assume that a target fixes the momentum problem. Confinement and
empirical admissibility of the new particles remain open.

Reproduce:

    python3 sol61_push/lab_cold_photon_acceptance_2026_10_13/check.py /tmp/lab_cold_acceptance_results.json

The original manufacturing goal remains unresolved. This checkpoint rejects
one stated source benchmark and isolates its two independent losses: tiny
resonant spectral overlap and insufficient laboratory momentum cancellation.
