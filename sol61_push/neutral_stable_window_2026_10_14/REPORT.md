# A conditional miscible parameter window, with a trapping tradeoff

The prior density obstruction applies to the assigned strong mediator coupling.
It is not a no-go for every parameter of the same Lagrangian. The earlier choice
mu^2=lambda M^2 was explicitly illustrative, not fixed by symmetry or data.
Varying mu independently opens a dilute coherent window in which BOTH density
and charge interactions are repulsive. This supplies a candidate continuation
without inventing an additional interaction. It does not identify a physical
particle, a complete apparatus, or the repo's cosmological cold component.

## Match both channels before changing the coupling

Use L_int=-lambda|phi|^4-mu R|phi|^2, carrier mass m, mediator mass M>2m.
Let Delta=M^2-4m^2>0. The existing tree amplitudes in
../ev_resonance_reciprocity_2026_10_14/REPORT.md give at zero relative momentum

    gs = [lambda/2 - mu^2/(4M^2)]/m^2,
    gc = [lambda - mu^2/(4M^2) - mu^2/(4Delta)]/m^2.

The threshold potential uses the off-shell propagator. A constant on-shell
width is not inserted into a zero-kinetic-energy conservative contact coefficient;
this is leading tree matching, not a loop-resummed scattering calculation.
The identical and distinguishable channel normalization differs, as in the
preceding repository matching. The interaction Hessian for the two occupations
has eigenvalues

    g_density = [3lambda/2 - mu^2/(2M^2) - mu^2/(4Delta)]/m^2,
    g_charge  = [-lambda/2 + mu^2/(4Delta)]/m^2.

Demanding both positive gives the OPEN interval

    2lambda Delta < mu^2 < 6lambda M^2 Delta/(M^2+2Delta).

Its width is 4lambda Delta (M^2-Delta)/(M^2+2Delta)>0 because
M^2-Delta=4m^2. Merely making mu arbitrarily small would fail: at mu=0 the
charge eigenvalue is negative and the uniform mixture favors demixing.
This is why testing density compressibility alone is insufficient.

These are dilute, low-frequency contact criteria. They do not establish
finite-density stability when elimination of the mediator is uncontrolled.

## Test one candidate with the mediator retained

Keep m=1 eV, lambda=1e-6, delta=M-2m=2e-9 eV. The allowed threshold interval is

    1.264911064e-7 eV < mu < 2.190890226e-7 eV.

Choose the midpoint in mu^2: mu=1.788854380e-7 eV. Both threshold eigenvalues
are approximately 5e-7 eV^-2. This coupling is about 11,180 times smaller than
the former 0.002 eV assignment.

At the illustrative density 3e14 constituents/m^3, solve the same fixed-number
three-field equilibrium as before, using h=mu/(2m sqrt(2M)) and the uneliminated
nonresonant couplings. The result is

    h sqrt(n)/delta = 0.03394887,
    mediator constituent fraction = 0.000576262,
    chemical potential = 5.75268e-13 eV,
    n dmu/dn = 5.74274e-13 eV > 0,
    density sound speed = 227.185 m/s.

The explicit six-component Bogoliubov spectrum has zero computed imaginary
parts on 301 logarithmically spaced wave numbers with
k/sqrt(m*scale) from exp(-6) to exp(3). Its small-k density branch agrees with
the thermodynamic derivative within 0.27%; finite-k curvature is retained.
The near-threshold rotating-wave matching differs from the exact threshold
coefficient by higher-order detuning/rest-mass terms. At this delta those are
tiny; no full relativistic loop or all-wave-number stability proof is claimed.
The static underlying potential also has positive completed-square quartic
lambda-mu^2/(2M^2)=9.99999996e-7, a separate boundedness check.

This candidate avoids the previously exhibited bulk coherent instability in
the tested regime. Its 227 m/s sound speed is not support for a 200 km/s halo.
Mode populations, halo selection and the dark-energy connection remain missing.

## The same change weakens the trap

Holding the photon coupling fixed, scale the previous Coulomb-only material
barrier as U=U_ref (mu/0.002) (M_ref/M)^2. This retains the same approximate
nuclear response, not a measured full silica scalar response. For a spherical
cavity of radius a surrounded by an INFINITE exterior of potential U, the first
s-wave bound level exists only when

    a > pi hbar c / sqrt(8mU).

This follows from k cot(ka)=-kappa as E approaches U from below, where ka=pi/2.
It is not an infinite-height hard wall. An actual finite shell has escape to
exterior vacuum and needs a separate resonance lifetime calculation.

| Detuning, eV | Selected mu, eV | Modeled barrier, eV | Minimum ideal radius |
|---|---:|---:|---:|
| 2e-9 | 1.78885e-7 | 2.55567e-12 | 13.710 cm |
| 1e-6 | 4.00000e-6 | 5.71464e-11 | 2.899 cm |
| 1e-5 | 1.26490e-5 | 1.80710e-10 | 1.630 cm |
| 1e-3 | 1.26412e-4 | 1.80420e-9 | 0.516 cm |
| 0.3 | 1.97264e-3 | 2.13099e-8 | 0.150 cm |

Each row selects the midpoint of its threshold mu^2 interval. Only the first
row received the explicit finite-density spectrum calculation. For the first
row, the 2 cm cavity has no sub-barrier bound level even with an infinitely
thick exterior. Larger radius is necessary but not sufficient for useful storage.

The 1e-5 eV detuning row recovers an ideal 2 cm ground level at
1.668448086e-10 eV, below the barrier 1.807100734e-10 eV. It is close to escape;
no earlier 5 mm or 10 mm shell lifetime may be reused.
At pair threshold, the plane-wave virtual production coefficient scales as
mu*g_photon/Delta. Its ratio to the original assigned benchmark is 1.26490e-6
for this row. This is an amplitude coefficient, NOT a probability or a calculated
trapped-mode Rabi rate. Spatial overlaps, finite pair energy, noise, optical
buildup and losses must be recomputed before quoting a preparation time.

## Evidence and next decision

Ten checks pass: three exact rational identities, three spherical matching
residuals, explicit-mediator stationarity, bounded-spectrum imaginary part and
plus/minus symmetry, and the low-k thermodynamic comparison. Positivity and
sub-barrier energy assertions additionally constrain the reported rows.
contract.json and run/manifest.json record this bounded calculation.
No new Lean theorem is claimed for this package.

The useful next comparison is between the larger near-resonant cavity and the
2 cm, more-detuned candidate, using actual finite-shell resonances and source
matrix elements. It must include the positive pair interaction, which removes
the old attractive blockade parameters. Retention and creation cannot be imported
independently from the old benchmark. This is a conditional alternative parameter
family, not empirical evidence or a completed cold-energy creation mechanism.
