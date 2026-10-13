# Conservative source conversion operator for the coupled kinetic stage

2026-10-11. The previous turn made progress by evaluating condensate gain on
a fixed spectrum, while identifying faster moving-source dynamics as a reason
not to extrapolate it. This turn implements the conversion operator that must
evolve that spectrum. It is an operator audit, not a production simulation.

## Isotropic nonrelativistic kinematics

For the leading NR kinetic masses m and 2m, let delta=M-2m be the positive
source rest-energy gap and e_b=P²/(4m) the source kinetic energy. Its daughters
have energies

    e_1=(delta+e_b)/2 + sqrt(delta e_b) cos(theta),
    e_2=delta+e_b-e_1.

An isotropic source decay is uniform in e_1 on this interval. Equivalently,
a daughter pair can form a source if

    e_b=e_1+e_2-delta >= 0,
    |e_1+e_2-2delta| <= 2 sqrt(e_1 e_2).

This describes genuine moving-source recoil. The approximation replaces M
by 2m in the kinetic mass only; the finite rest gap is retained. Relativistic
kinematic corrections, coherent source amplitudes and medium shifts are not
included. Vacuum decay rate Gamma_0 is inherited from the candidate; it can
multiply the dimensionless audited operator once a resolved evolution is used.

## Discrete reaction construction

Choose h=delta/D, daughter energies e_i=i h and source kinetic energies e_k=k h.
Retain only physically allowed triplets with i+j=D+k. A reaction extent J
changes particle densities by

    dn_i=+J, dn_j=+J, dn_bk=-J.

If i=j, that daughter's density receives 2J. Every reaction therefore conserves
charge n_a+2n_b and excess energy sum(e_i n_ai)+sum((delta+e_k)n_bk), without
an after-step correction or cancellation between unrelated reactions.

For each source energy, unordered daughter pairs have normalized angular
quadrature weights w_ijk. Off-diagonal pairs count both daughter-label orders;
diagonal pairs count once. With source density-of-states weight g_bk,

    J_ijk = Gamma_0 g_bk w_ijk [f_bk(1+f_i)(1+f_j)
                                   -(1+f_bk)f_i f_j].

The weights sum to one for every retained source mode, so an empty daughter
bath gives the inherited vacuum decay rate. Angular endpoint quadrature
errors remain at finite h; normalization does not remove those shape errors.
For the audited maximum kinetic energy 8delta, the allowed daughter interval
lies within the retained range. Zero-energy condensate modes are not included
in this operator and must be represented separately in a full calculation.

A Bose equilibrium with daughter chemical potential mu and source chemical
potential 2mu satisfies detailed balance reaction by reaction. This follows
from e_i+e_j=delta+e_k, not from forcing the numerical solution toward a
specified temperature or profile. If X and Y are the forward and inverse
Bose products, each reaction contributes a nonnegative entropy production
Gamma_0 g_bk w_ijk (X-Y) ln(X/Y). The code checks this against the independent
entropy gradient sum[ln(1+1/f) dn/dt].

## Finite audit

`source_collision_operator.py` builds three grids and applies the operator to
specified thermal controls and a positive, nonthermal test distribution:

| D | Retained reactions | Maximum equilibrium residual | Relative charge derivative error | Relative energy derivative error |
| --- | ---: | ---: | ---: | ---: |
| 8 | 990 | 1.25e-15 | 0 | 8.28e-18 |
| 16 | 3912 | 1.25e-15 | 4.47e-16 | 1.40e-17 |
| 32 | 15553 | 1.30e-15 | 4.28e-16 | 6.69e-17 |

The daughter-energy mean for a source with e_b=delta/2 is 0.75delta on all
three grids. Its variance approaches the continuum value delta²/6: 0.15625,
0.171875 and 0.164714 in delta² units. The error is not monotone in sign, but
its magnitude decreases across these grids. Entropy production is positive
for the nonequilibrium control and agrees with the independent gradient.
All 25 finite checks pass. The run manifest validates recorded provenance.
The structural per-reaction conservation and detailed balance apply to this
construction at any admissible grid; the sampled angular accuracy does not
prove uniform convergence or the correctness of a future time integrator.

## Why these audit grids are not an initial-production evolution

The current candidate has delta/(m epsilon)=999.975. Its produced energy band
has structure on the m epsilon scale, about a thousand times narrower than
the gap. Newly accessible source recoil energies can be on that same small
scale. D=8,16,32 cannot resolve this band or its near-zero source recoils.
Replacing it with one occupied coarse bin could artificially forbid or alter
inverse conversion. Such a run would not answer the physical question even
if conservation and solver tests passed.

At the other end, the conditional equilibrium has T about 35delta, demanding
a much wider energy domain than the initial narrow shell. A uniformly fine
grid covering both scales would be needlessly large and potentially obscure
the initial coherent-to-kinetic approximation. The coupled calculation needs
a resolved treatment of the narrow source/daughter band and a broader thermal
energy domain, with transfer between them audited for conservation and Bose
balance. A finite-grid equilibrium must not be mistaken for the previously
computed continuum Bose endpoint.

The remaining implementation is to couple this source operator to daughter
redistribution and separate condensate variables, with an appropriate energy
representation and a justified treatment of initial correlations. No evolved
spectrum, condensation fraction or halo result is claimed by this audit.
