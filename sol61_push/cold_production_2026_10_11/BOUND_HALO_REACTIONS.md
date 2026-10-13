# Initial resonant reactions in a finite bound halo

Status: a finite collisionless equilibrium replaces the homogeneous bath for
an initial-rate test. Source production is centrally concentrated, and newly
formed sources obey an explicit orbital-binding bound. This is not a halo
evolution simulation or a derivation of the selected halo profile.

## A declared equilibrium, not the target profile

Choose a Plummer potential and daughter density,

    Phi(r)=-G Mh/sqrt(r^2+b^2),
    rho(r)=3 Mh/(4 pi b^3) (1+r^2/b^2)^(-5/2).

The bound isotropic phase-space distribution is proportional to
[-(v^2/2+Phi)]^(7/2) below escape and zero above it. The potential/density
pair is given in [Bovy's galactic-dynamics text, spherical potentials](https://galaxiesbook.org/chapters/I-01.-Gravitation_4-Examples-of-spherical-potentials.html);
the distribution's energy dependence is also documented in the author's
[galpy Plummer DF implementation](https://docs.galpy.org/en/stable/reference/dfplummer.html).
Here its normalization is computed directly from the stipulated daughter
number density, rather than importing a mass/number convention from a library.

Since the distribution is a function of the conserved orbital energy, it
solves the collisionless stationary equation in this potential. It does not
solve the full reaction kinetic equation: source production initially has a
nonzero collision term. No baryons are included.

Take central density 1e-21 kg/m^3 and central one-dimensional dispersion
200 km/s. The isotropic moment relation sigma_r^2=-Phi/6 gives

    b^2=9 sigma_0^2/(2 pi G rho_0),
    Mh=6 sigma_0^2 b/G.

Thus b=30.027 kpc, Mh=1.6755e12 solar masses and the central escape speed
is 692.82 km/s. These define an illustrative test halo. They are neither
measurements nor predictions of the creation mechanism.

## Local occupation and production rate

Let v*=u c=299.792458 km/s and e=p^2/(2m^2u^2), as in COUPLED_KINETICS.md.
At radius r define esc=-Phi/v*^2. Then

    f(e,r)=Ar (1-e/esc)^(7/2),  0<=e<esc,
    Ar = n(r)/[w0 sqrt(2) esc^(3/2) B(3/2,9/2)],
    w0=(m u)^3/(2 pi^2).

This integrates to n(r)=rho(r)/m in natural units. Its mean e is esc/4,
which independently recovers sigma_r^2=-Phi/6.

With no sources initially, the reaction gain is proportional to f1 f2.
The earlier invariant measure gives

    Rchi(r)=K0 integral_allowed de1 de2 f(e1,r)f(e2,r),
    K0=g^2 m^2 u^4/(16 pi^3).

Here Rchi is source number production per physical volume and time in
natural units. The local fraction of daughter charge converted per unit time
is initially 2Rchi/n. The global initial rate is its daughter-mass-weighted
radial integral; it is not a constant conversion rate for later evolution.

For quadrature use q=sqrt(ec-1), ec=e1+e2, and

    e1=ec/2+z, e2=ec/2-z,
    |z|<=min(q,esc-ec/2).

Splitting at q=sqrt(2esc)-1 resolves the switch between the angular and
escape boundaries. This avoids the midpoint angular mask used by the earlier
energy-grid evolution. Radial and nested energy quadratures are each tested
at orders 24,48,96.

## Orbital binding and the reaction region

On resonance, the parent relative speed is 2v*. The source velocity is the
parents' mean velocity at retained NR order. Its specific orbital energy is

    epsilon_chi=(epsilon_1+epsilon_2)/2-v*^2/2.

Both parents are bound, so epsilon_chi<-v*^2/2. A newly formed source is
therefore bound more deeply than its parents' average; it cannot escape
immediately. The kinematic condition for any two bound parents to reach the
resonance is v_escape(r)>v*, or esc>1/2. At equality the available phase
space shrinks to zero.

For this Plummer example the active region ends at

    r_active/b=sqrt[(2 esc_0)^2-1]=5.24626,
    r_active=157.53 kpc.

In a fixed potential, the same energy inequality bounds a newly born source's
apocenter by r_active even if its angular momentum is zero. This is a
kinematic bound for collisionless motion of that source, not proof that
later scattering or decay preserves its individual orbital energy.

The selected scale here is an escape **velocity** fixed by the mass splitting.
It is not a derivation of a universal acceleration or a vacuum-density scale.

## Initial-rate results

The initial global source-charge production rate is 0.1770035 per Gyr,
normalized to total initial daughter charge. The central local rate is
1.188862 per Gyr. Approximately 90.581% of all initial source production
occurs inside b, which contains only 35.36% of the initial Plummer mass.
Thus the reaction preferentially operates in the central, denser region.
These are initial derivatives; they must not be extrapolated as linear yields
once the populations or gravitational potential change.

| Radius r/b | Initial local charge-conversion rate, Gyr^-1 |
|---|---:|
| 0 | 1.18886 |
| 0.5 | 0.61973 |
| 1 | 0.13726 |
| 2 | 0.0030993 |
| 4 | 7.01e-8 |
| Beyond 5.24626 | 0 |

A counterfactual isotropic spontaneous decay of each new source at its birth
position also has a simple escape geometry. Daughter energies are

    e_out=ec/2 +/- sqrt(ec-1) cos(theta).

At most one daughter can escape because ec<2esc. The fraction of isotropic
orientations with an escape is max[0,1-(esc-ec/2)/sqrt(ec-1)]. Weighting by
initial source births gives 0.0049371, or about 0.494 percent.
This is **not an evaporation fraction or rate**: actual sources move before
decaying; Bose factors change the angular rates; inverse reactions and
source depletion must be evolved. Large forward and reverse stimulated
rates also cancel in the net collision term, so a comparison of gross decay
probabilities alone would not determine secular escape.

## Evidence and remaining evolution

All 351 checks pass, including normalization, velocity moments, finite total
mass, source binding and quadrature refinement. The last two quadrature
orders agree in the global initial rate to better than 1e-13 relatively;
this is a numerical convergence diagnostic, not a certified accuracy claim.
`bound_halo_reactions.py` and `bound_halo_reactions_run/manifest.json` record
the calculation; the manifest validates. Interpretation is self-reviewed.

This establishes a centrally biased conversion channel in a bound test
system. It does not yet determine orbit-averaged source density, heat export,
contraction, a final mixed-species equilibrium or the response of gravity.
The Plummer shape was chosen to make those questions concrete, not produced
by the microscopic action. The repo's halo profile, baryonic scaling and
vacuum-dependent acceleration remain unresolved.
