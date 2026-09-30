# Neutrality is a separate condition for the surface cubic

This calculation extends SLOW_WALL_RESULTS.md. It does not supply the missing vacuum stress or select 32pi.

For a free uniform two-dimensional Dirac branch at zero temperature, let m=y|p|, tangential speed v, positive-band degeneracy nu, and chemical potential zeta>=0 relative to the cone. After the previously assumed analytic vacuum subtraction,

Omega_vac(m) = nu m^3/(6pi v^2).

When m<zeta, occupied positive-energy states contribute

Delta Omega = -nu/(2pi v^2) integral_m^zeta E(zeta-E) dE.

Consequently the exact grand potential is

Omega(m,zeta) = -nu zeta^3/(12pi v^2) + nu zeta m^2/(4pi v^2), for m<zeta;

Omega(m,zeta) = nu m^3/(6pi v^2), for m>=zeta.

The potential and its first mass derivative agree at the threshold. The number density for the occupied branch is nu(zeta^2-m^2)/(4pi v^2). Negative chemical potential gives the corresponding hole result with |zeta|. Thus every fixed nonzero filling scale removes the cubic term in the asymptotic small-p regime. A crossover occurs at |p|=|zeta|/y. Analytic quadratic counterterms remain separate inputs; removing that quadratic term by matching would still not restore the cubic in this regime. These statements concern a free band and its specified equilibrium ensemble, not a general interacting determinant.

## What a candidate symmetry does and does not protect

Take Gamma_x=sigma_x tensor I, Gamma_y=sigma_y tensor I and M_i=sigma_z tensor sigma_i, as in the prior four-band surface Hamiltonian. The antiunitary Theta=(sigma_y tensor sigma_y)K has Theta^2=+1. It flips the kinetic matrices and preserves the three M_i. For a time-even polarization p, it therefore permits y p_i M_i while excluding the internal-rotation singlet gap sigma_z tensor I.

This is an explicit algebraic way to remove the previously identified singlet-gap permission, conditional on the state and microscopic action respecting this time reversal. A directed stream need not respect it. Theta preserves the identity, so it does not enforce zero chemical potential or half filling. An overall identity energy shift can be absorbed together with the chemical potential at fixed charge; its permission alone does not demonstrate physical doping. The required condition is that the equilibrium chemical potential sits at the cone, and the symmetry above does not select that condition.

A canonical momentum-independent particle-hole antiunitary C leaving p unchanged would require C Gamma_{x,y} C^-1=+Gamma_{x,y} and C M_i C^-1=-M_i, from C H(k,p) C^-1=-H(-k,p). But Gamma_x Gamma_y M_1 M_2 M_3=-I is real. Those five transformation rules would change its sign, whereas conjugation of -I cannot do so. This excludes that specified C in this quartet. It does not exclude doubled representations, particle-hole actions transforming p, or more general momentum-dependent constructions. A spectral particle-hole constraint must also be distinguished from an implemented physical charge-conjugation symmetry.

## Evidence and next decision

The bounded run in runs/surface_neutrality contains 16 passing checks: exact symbolic occupation integration and matching/density identities, exact matrix actions and central product, and five independent radial-momentum quadratures. The central-product proof above supplies the inference; a passing matrix check alone does not establish a universal classification. No external theorem or novelty claim is used.

The next viable surface route must select both a protected gapless state and cone neutrality. A doubled model may permit additional symmetries, but compensated electron and hole pockets can have zero total charge while retaining nonzero filling relative to each cone. Neutrality of total charge alone is therefore insufficient. Separately, the positive-tension wall stress obstruction, quadratic critical matching, absolute vacuum constant and unselected couplings remain. This is a constraint on a prospective common action, not a completed connection between a0 and Lambda.
