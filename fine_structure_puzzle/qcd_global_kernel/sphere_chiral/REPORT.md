# A calculated global sphere contribution

The one-loop pion sector now has a direct global round-S4 answer, with
every scalar harmonic included. This goes beyond FSP-007's flat trace
two-point function. It does not calculate the complete QCD numerator,
proton denominator, R(alpha), or alpha itself.

For one real scalar pion, z=M²/H² and ξ=0 at leading chiral order,

    ρdec(H)=3H⁴ z I0(z)/(32π²),
    Iξ(z)=(z+12ξ-2)/6 [ψ(3/2+ν)+ψ(3/2-ν)-log z]
                +2/9-2ξ-(29/90-4ξ+12ξ²)/z,
    ν²=9/4-z-12ξ.

DERIVATION.md also gives an absolutely convergent spectral sum and the
global W from which this one-point response follows by fixed-parameter
metric differentiation. The common decoupling prescription subtracts
local heat terms through R²; no radius-dependent or alpha-target fit
is made.

The new homogeneous low-curvature result is

    ρdec=37H⁶/(2016π²M²)+O(H⁸/M⁴)

per real minimal pion. With one neutral and two real charged modes,

    ρ_pi,mass=37H⁶/(2016π²)
       [1/M²+2/(M²+2e²C/F²)]+O(H⁸).

M,F,C remain unfitted matching inputs. This determines a real global
contribution and its conditional charge dependence. Its linear-H
coefficient is zero at fixed positive mass, uniformly for the stated
bounded charge neighborhood. This is a result for this controlled
one-loop sector, not a no-go theorem about full QCD.

The independent electromagnetic curvature constant k15 contributes
through ξcharged=-2e²k15. Its isolated derivative, along with the mass
effect, is calculated in (13). Photon loops, strong curvature matching,
interacting pions, heavier QCD states and nonperturbative global QCD
remain absent. A local R³ matching term can change the total H⁶
coefficient; the displayed coefficient is the defined pion matter
contribution and its leading inverse-mass chiral behavior.

The execution evidence includes independent heat/spectral comparisons,
fixed-parameter metric differentiation, W reconstruction, a radius grid,
and finite charge-mass scenarios. The massive constant mode is retained.
The massless Gaussian zero mode is singular and is not used to infer a
physical chiral-limit sphere response. Reproduce with REPRODUCE.md;
contract.json and run_001/manifest.json define the exact tested domain.
