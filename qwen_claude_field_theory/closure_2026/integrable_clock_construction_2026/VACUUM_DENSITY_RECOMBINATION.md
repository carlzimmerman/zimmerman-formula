# Carl's question: what was the vacuum density at recombination?

2026-09-08. This note answers Carl's explicit question and separates it
from the construction's evolving clock density. No new discovery is claimed
for the constancy of a cosmological constant.

If vacuum means a constant Lambda, its mass-equivalent density is

    rho_Lambda(z)=Lambda c²/(8 pi G)=rho_Lambda,0.

It is not multiplied by (1+z)^3 or (1+z)^4. Those are the dilution laws for
separately conserved nonrelativistic matter and radiation. Using the
model-dependent Planck base-LambdaCDM reference H0=67.4 km/s/Mpc and
Omega_m=.315, take Omega_Lambda≈.685, neglecting today's tiny radiation
correction for this rounded illustration:

    rho_critical,0=3H0²/(8 pi G),
    rho_Lambda≈5.8450e-27 kg/m³,
    rho_Lambda c²≈5.2532e-10 J/m³.

These are calculated from the reference cosmological fit, not an independent
vacuum measurement made at recombination. Source: [Planck 2018 VI,
published 2020](https://doi.org/10.1051/0004-6361/201833910), abstract and
cosmological-constant discussion. Checked 2026-09-08. No claim is made that
the IC action has derived those parameters.

Carl's proposed relation then gives

    a0=(c/2)sqrt(G rho_Lambda)≈9.3624e-11 m/s²,

the same at recombination and today under this constant-Lambda premise.
Conversely input a0=9.4e-11 gives rho_Lambda=5.8921e-27 kg/m³. Agreement
of these rounded normalizations is not an independent validation or a
derivation of the fitted coefficient 1/2.

For scale only, at reference z=1100 with Omega_r=9.2e-5,

    rho_m≈3.5873e-18 kg/m³,
    rho_r≈1.1535e-18 kg/m³,
    rho_Lambda/rho_total≈1.233e-9.

Thus constant vacuum energy is about one part in 810 million of the total
at that epoch, despite dominating the reference model today. This fraction
uses reference-model matter, including its inferred nonbaryonic component;
it must not be presented as a baryon-only IC cosmology prediction.

If dark energy evolves, there is no unique recombination value without its
equation of state and history. For separately conserved homogeneous dark
energy, rho_DE(z)/rho_DE,0=exp[3 integral_0^z (1+w_DE)/(1+z') dz'].
The acceleration-scale relation by itself does not determine that integral.

## Reproduction

Executed with Python 3.9.6, exit 0:

    python3 -B -c 'import math; G=6.67430e-11;c=299792458.;Mpc=3.085677581491367e22;H=67.4e3/Mpc;rhoc=3*H*H/(8*math.pi*G);rhoL=.685*rhoc;z=1100;rhoM=.315*rhoc*(1+z)**3;rhoR=9.2e-5*rhoc*(1+z)**4;print({"rho_Lambda_kg_m3":rhoL,"energy_J_m3":rhoL*c*c,"a0_relation_density_for_9.4e-11":4*(9.4e-11)**2/(c*c*G),"a0_from_Lambda":c*math.sqrt(G*rhoL)/2,"rho_matter_z1100":rhoM,"rho_radiation_z1100":rhoR,"vacuum_fraction_z1100":rhoL/(rhoL+rhoM+rhoR)})'

The constructive direction being tested is constant vacuum normalization
plus an independently varied, evolving clock. A dust-like clock would
behave gravitationally as an additional matter component; renaming it does
not remove its abundance, lensing, perturbation and conservation obligations.
