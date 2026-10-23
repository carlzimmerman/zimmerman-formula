# Full spectrum and the cold-abundance test

The computed gravitational source does not supply enough material for the existing MeV benchmark in the tested cosmology. This is a conditional, quantitative failure of that production regime, not an exclusion of all inflationary histories or the full interacting action.

## Physical background and quantum state

Replace the earlier asymptotically static tanh example by

    a=exp(N), H=H_inf/(1+a²), epsilon=-d ln H/dN=2a²/(1+a²).

This smoothly connects de Sitter expansion to radiation-like expansion. It obeys the flat Friedmann equations for an effective fluid with rho=3 M_Pl² H² and w=-1+2 epsilon/3, ranging from -1 to 1/3. It does not specify an inflaton or derive reheating from the carrier action. Equating its asymptotic radiation energy to a thermal bath with g*=g*s=106.75 is an explicit additional assumption.

Use H_inf=m_Phi=1, xi=0 and M/m=2 sqrt(1+0.02²), the mass ratio of the existing near-threshold benchmark. Each complex field begins in a positive-frequency adiabatic vacuum deep inside the horizon, with no occupied X source. The linear mode equation is

    u_NN+(1-epsilon)u_N+
      [k²/(aH)²+(mass/H)²-(2-epsilon)]u=0.

The cubic and quartic interactions do not enter this linearization. Their effect on the produced state has not been simulated. This is a free spectator calculation on the declared geometry, not a complete nonlinear production solution.

## Spectrum and checks

physical_spectrum_wkb2_v2_run samples k/m from 1e-5 to 10 on 121 and 241 logarithmic points for both species. The two runs start with k/(aH) at least 50 and 100, end at H/m=.01 and .005, and use rtol=2e-10 and 2e-11. The initial/final particle bases include second adiabatic-order corrections. The lower-order basis produced a spurious UV tail in the much smaller X population; this motivated the correction rather than accepting the apparent tail as physical.

For omega=sqrt(k²+mass² a²), the corrected frequency is

    W=omega+[-a''/a - omega''/(2 omega)
                         +3 omega'^2/(4 omega²)]/(2 omega).

The basis mode has derivative (-iW-W'/(2W))u. Projection onto its conjugate gives beta. Both particle and antiparticle are counted:

    a³ n = (1/pi²) integral k³ |beta_k|² d ln k.

At the finer setting:

| Species | a³ n / m³ | rms speed at H/m=.005 |
|---|---:|---:|
|Phi, both charges|0.00380974030|0.0193564 c|
|X, both charges|0.00000638154|0.0229132 c|

The comoving number changes by about 7e-8 fractionally for Phi and 1.3e-5 for X between the two setups. The maximum absolute Wronskian residual for highly occupied infrared Phi modes is 2.7e-5; X remains below 1.1e-9. All four declared checks pass and the completed manifest validates. Two earlier runs failed JSON serialization after calculating their modes; those failed records are preserved and do not supply the final spectrum artifact.

No finite grid literally integrates every momentum. The k>=5 contribution is below 1e-8 of the number in these corrected runs. The infrared asymptotic slope is k³ n_k proportional to k^(3-2 sqrt(9/4-m²/H_inf²)); for Phi the exponent is 0.763932 and the first sampled intervals agree. Extrapolating that asymptote below k=1e-5 gives an omitted number approximately 0.000367 of the computed Phi number. This is a stated analytic tail estimate, not an additional integrated domain. It is negligible compared with the abundance shortfall.

This source is not a collisionless rearrangement of the earlier warm distribution. Quantum production can generate very large infrared mode occupations from the vacuum, so the warm-population phase-space ceiling is not an applicable production bound. Large occupation in a small momentum volume nevertheless does not imply a large total abundance; the k³-weighted integral is decisive. The scalar occupation has not been mapped to the distinct identified-medium distribution used by the collapse model.

## Does it give enough cold material?

Map to m=1 MeV, the existing benchmark, and assume asymptotic radiation thermalization and subsequent conserved visible entropy. The asymptotic comoving temperature is

    a T = [90/(pi² g*)]^(1/4) sqrt(M_Pl H_inf),
    a³ s = (2 pi²/45) g*s (a T)³.

Using the reduced Planck mass 2.435e18 GeV, the effective daughter yield, even if every produced X eventually gives two daughters, is

    Y = (n_Phi+2 n_X)/s approximately 4.30e-36.

The finite-time code's unextrapolated values are 4.365e-36 and 4.332e-36; their small difference is mostly the residual departure of H a² from its radiation asymptote. Correcting with the exact factor (1-H/H_inf)^(3/2) gives the asymptotic value above.

For comparison, the conventional dark-matter target mY approximately 4.37e-10 GeV requires Y approximately 4.37e-7 at m=1 MeV. The result is therefore approximately 9.84e-30 of that target: roughly 29 orders of magnitude too small. The target is a standard-cosmology benchmark, not an independently derived requirement of the unidentified polarization medium. Constants and the abundance conversion are documented by the [PDG astrophysical constants](https://pdg.lbl.gov/2025/reviews/rpp2025-rev-astrophysical-constants.pdf) and [PDG dark-matter review](https://pdg.lbl.gov/2023/reviews/rpp2022-rev-dark-matter.pdf).

The directly produced Phi particles are already nonrelativistic at the endpoint and would redshift further if decoupled. For example, extrapolating their rms momentum through entropy-conserving expansion to a photon temperature of 0.8 eV gives a speed of order 3e-18 c. That is a conditional redshift estimate, not a computed matter transfer function, and it excludes later interaction heating and X-decay recoil. The decisive failure here is abundance, not an inability to become cold.

At fixed H_inf/m and fixed dimensionless couplings, Y scales as m^(3/2), so the abundance fraction scales as m^(5/2). Merely rescaling this result would reach the conventional abundance near m approximately 4e8 GeV. That is a radically different mass regime and does not preserve the MeV scattering benchmark or establish the carrier-to-medium mapping. It is not a prediction that the theory chooses that mass.

## Higher inflation scale: a specific nonlinear gate

A potentially larger source is the inflationary fluctuation of a light X field. In the free, effectively massless approximation over N_e e-folds,

    <|X|²> approximately H_inf² N_e/(4 pi²).

This follows by integrating the vacuum fluctuation power per logarithmic horizon-exit interval; it is an ensemble variance with zero mean charge, not a freely inserted charged source. If this displacement survived until H approximately M and then behaved as a noninteracting massive condensate, one would estimate n_X approximately M <|X|²>. Taking N_e=60 and the same radiation history, meeting the abundance through two-daughter conversion would require rms |X| approximately 1.66e10 GeV, or H_inf approximately 1.34e10 GeV.

That estimate cannot be imported into the dilute decay calculation. Expanding the actual carrier action around a background X gives real-Phi quadratic eigenvalues

    m² + 2 g |X|,       m² - 2 g |X|.

For g=2168 eV and m=1 MeV, the second is negative above |X|=m²/(2g)=0.23063 GeV. The putative abundance-producing displacement exceeds that threshold by 7.2e10. Restricting the free-condensate estimate below the threshold yields at most about 1.94e-22 of the target abundance under the same onset assumptions. These estimates diagnose loss of validity; they are not a nonlinear abundance prediction or a universal bound on the interacting theory.

The remaining source route is therefore concrete: inflationary fluctuations of X followed by nonlinear conversion through the existing g X* Phi² vertex, with quartic backreaction and expansion. The instantaneous negative mass eigenvalue identifies a possible conversion channel, but Hubble friction and a nonzero Phi background can delay or block it. It does not establish the final temperature or abundance. Trilinear tachyonic production is established physics ([Dufaux et al., hep-ph/0602144](https://arxiv.org/abs/hep-ph/0602144)); no novelty is claimed. The unresolved calculation is whether this particular positive-square action leaves the required cold neutral population after that nonlinear stage, rather than heating or depleting it. A prepared low-density X decay is not an adequate substitute.

There is a further protection gap: the vacuum source has zero net conserved U(1) charge. The carrier bound E>=m|Q| becomes only E>=0 for the total neutral stock. The earlier bound on small excess energy in a single positive-charge nonrelativistic sector cannot be transferred to this state. Opposite-charge sectors and number-changing processes must be retained when assessing heating. This does not prove that the output is hot; it removes an unjustified guarantee that it is cold.
