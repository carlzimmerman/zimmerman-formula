# Moving-source response with the produced radial spectrum

The finite radial width of the saved detuned production spectrum does not
remove the moving-source response in a frozen, free-evolving Gaussian
ensemble. At elapsed response time 200 its linear forced response is
1.250259, compared with 1.256696 for the ideal monochromatic shell. Values
above one flag breakdown of undepleted forcing; they are not physical
conversion fractions.

## Surrogate and derivation

Use the daughter occupations saved at production x=200 in
`detuned_bogoliubov_run/results.json`. Reset the moving source to zero and
let daughters evolve with their free envelope phases, with no daughter
backreaction, quartic phase shift, source remnant or expansion. This is a
new response clock, not an extension of the production trajectory. It
retains the produced radial number spectrum but does not assert that the
actual state's unequal-time correlations are free.

For radii q,r in units p/(m u), define ell=L_a(q)+L_a(r). Uniform relative
angle mu gives source momentum Q^2=q^2+r^2+2qr mu and mismatch

    delta = L_b(Q)-ell.

The endpoints and angular density are

    delta_- = L_b(|q-r|)-ell,
    delta_+ = L_b(q+r)-ell,
    probability density = a+b delta,
    a = epsilon (R+epsilon ell)/(2u^2 q r),
    b = epsilon^2/(2u^2 q r).

The forced kernel is the integral of
(a+b delta) 4 sin^2(delta t/2)/delta^2 over these endpoints. Its primitives
are the same sine/cosine integral expressions in
[DETUNED_MOVING_RESPONSE.md](DETUNED_MOVING_RESPONSE.md), evaluated at both
signed endpoints. The implemented small-argument series avoid cancellation.
For radial charge fractions f_i, the connected source response is
2 sum_ij f_i f_j K(q_i,q_j,t). The factor two is from Gaussian normal Wick
contractions. A coherent anomalous mean source is separate.

## Results

| Elapsed response time | Produced-spectrum forced response |
| ---: | ---: |
| 1 | 0.00627068079 |
| 10 | 0.06254540015 |
| 30 | 0.18756877050 |
| 100 | 0.62514771364 |
| 200 | 1.25025936811 |

The 512- and 1024-radius inputs agree to 8.44e-7 or better over these times.
The wider-band 1536-radius input differs from the 1024-radius result by
less than 1.7e-11. Independent direct angular quadrature, angular density
normalization, kernel positivity, radial refinement and bandwidth comparisons
all pass: 21 checks. The run manifest validates against current inputs.

About half the radial pair weight permits an interior angular resonance.
The sharp-indicator asymptotic-slope diagnostic is less well converged than
the smooth finite-time response: it ranges from 0.0062118 to 0.0062321 across
these grids. No high-precision asymptotic-rate claim is made. The finite-time
values above are the tested quantities.

## Consequences for the research route

Radial width alone is not a supported justification for dropping moving
sources. The next dynamical calculation must retain either their response
with the actual unequal-time production correlations or a coupled evolving
source population. Simply evolving homogeneous Gaussian production longer
cannot decide spatial survival.

A changing daughter fraction is also not identical to loss of coldness.
The classical positive-square identity E-mQ>=0 constrains gradient and
rotating-frame energy for the combined two-field system, including moving
sources. At the detuned circular-source initial condition the excess fraction
is about 5e-5. The repulsive quartic remains nonnegative in that identity.
This statement is conditional on a classical state with that measured E,Q,
fixed-box boundary assumptions and smooth evolution. A renormalized quantum
bound and a justified quantum-to-classical matching have not been proved.
It cannot be used to silently certify the quantum production state's later
stress or its galaxy-scale behavior.

Thus a viable target may be a cold two-field mixture rather than almost pure
daughters, but that would still need its transport, halo stress and the
repository's acceleration law derived. No completion claim follows here.

Evidence: `detuned_radial_response.py`, its contract, and
`detuned_radial_response_run/results.json` and `manifest.json`.
