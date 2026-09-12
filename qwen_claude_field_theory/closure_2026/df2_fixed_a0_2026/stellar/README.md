# Spherical stellar profile and isolated Jeans reference

This module supplies a normalized Abel deprojection of a circular Sérsic
profile. It is a spherical approximation to DF2 photometry, not a deprojection
of its observed q=0.85 ellipse. The Sérsic index n=0.6 is a photometric input.
For the physical examples, the adopted circular Re=2.0 kpc and stellar
M=2e8 solar masses at 20 Mpc follow the source conventions recorded in
`../data/SOURCES.md`. The approximate major-axis value 2.2 kpc would give
2.2 sqrt(0.85)=2.03 kpc after circularization; rounding conventions should not
be treated as an independent distance or size measurement. Stellar V-band
M/L=2 is a prior, not fitted here. The fixed global a0 is 9.3619e-11 m/s².

`Sersic(n=.6)` builds the interpolation once. `density(r)` returns density in
M/Re³, `mass(r)` returns enclosed mass in M, `surface_density(R)` returns
surface density in M/Re², and `projected_mass(R)` returns cylindrical mass in
M. Scalars or NumPy arrays are accepted. Lengths are in circular Re.

Writing p=1/n and b=P⁻¹(2n,1/2), where P is the regularized lower incomplete
gamma function, the projected profile is

    Σ(R) = A exp(-b R^p),   A = b^(2n)/(2π n Γ(2n)).

The exact Abel relation is evaluated numerically as

    ρ(r) = (A b p/π) ∫₀∞ (r cosh t)^(p-1)
                            exp[-b(r cosh t)^p] dt.

The central value for n<1 is ρ(0)=A b^n Γ(1-n)/π. The density and enclosed
mass are tabulated on a logarithmic radius grid between 1e-8 and
(80/b)^n. Density beyond the latter is set to zero. The mass integral uses
the antiderivative of a cubic spline for 4πρr³ in log radius and is not
rescaled. The finite central approximation below the first node is negligible
for the integrated observables tested here. The support restriction is
0.5≤n<1; independent analytic validation is at n=0.5 and DF2 validation at n=0.6.

The isolated spherical AQUAL equation integrates to

    g [1-exp(-g)] = η M(<r)/r²,   η = GM/(a0 Re²),

where g is in a0. `spherical_acceleration(g_newtonian)` inverts this monotone
relation. It must not be used by adding an external acceleration to the
right side; a nonzero external field requires the full nonspherical PDE.

For isotropy, constant stellar M/L, equilibrium, and zero outer pressure,
the Jeans equation gives ρσr²(r)=∫ᵣ∞ρ(s)g(s)ds. Projection followed by
integration over a circular aperture gives

    σap² = (4π/3) ∫₀∞ ρ(r)g(r)
             [r³-max(r²-Ra²,0)^(3/2)] dr / Mprojected(<Ra).

The factor in brackets follows by exchanging the Jeans and aperture
integrals: the needed inner antiderivative is one third of this factor.
`aperture_second_moment(profile, eta, aperture, law)` returns σap²/(a0 Re).
`law` is `aqual` or `newtonian`; `aperture=np.inf` is the global moment.
No fitted dispersion coefficient is introduced.

The analytic Newtonian Plummer control has Re=1 and

    σap²/(GM/Re) = (π/32) [1-(1+Ra²)^(-3/2)] / [Ra²/(1+Ra²)],

with global limit π/32. A separate continuous-mass deep-AQUAL control follows
from integrating sqrt(M)dM: the global σlos² tends to (2/9)sqrt(GMa0).

## Reproduction and bounded results

From the repository root:

```sh
python3 -m unittest discover -s qwen_claude_field_theory/closure_2026/df2_fixed_a0_2026/stellar -p test_profile.py -v
python3 qwen_claude_field_theory/closure_2026/df2_fixed_a0_2026/stellar/run_checks.py
```

Five independent checks pass: exact Gaussian n=0.5 density and mass;
n=0.6 total mass and independent line-of-sight reprojection; inverse-law
residual from gN/a0=1e-14 to 1e4; analytic Plummer apertures 0.1, 1, 5, and
global; and the deep-AQUAL global virial limit. The 1025, 2049, and 4097-node
runs agree within 4e-7 km/s for all tabulated dispersions. This is observed
convergence in float64, not a certified interval error bound.

At 20 Mpc, η=0.0744439969865. Results below use the 4097-node run:

| Circular aperture / Re | Newtonian σ (km/s) | Isolated AQUAL σ (km/s) |
| --- | ---: | ---: |
| 0.3 | 8.10973 | 22.09473 |
| 0.5 | 8.04053 | 21.81790 |
| 0.7 | 7.92073 | 21.46279 |
| 1.0 | 7.68904 | 20.88259 |
| 2.0 | 7.04052 | 19.45984 |
| Global | 6.84745 | 19.03973 |

At fixed angular light profile, flux, and M/L, M∝D² and Re∝D, so η is
distance-independent and all these isolated dispersions scale as sqrt(D).
Changing M/L changes η and requires recomputation. These values do not model
the observed flattened tracer, velocity anisotropy, masked and weighted
rectangular KCWI aperture, or the external field. They do not establish a
likelihood, empirical exclusion, or a derivation from the relativistic theory.

Computation-audit and test-driven-development were used to define the finite
contract and independent controls; verification-before-completion was used
for the final command checks.
