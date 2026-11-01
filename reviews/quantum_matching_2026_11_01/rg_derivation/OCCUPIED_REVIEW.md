# Independent review: finite occupied phase-current matching

1 November 2026. Reviewer: `/root/independent_math_transport`. **Verdict:
correct only with the stated rigid phase-current, partial finite matching,
small-heavy-shift and local thermodynamic/IR restrictions.** The calculable
finite occupied relaxation and Legendre ledger pass. A complete physical
pressure no-go is not established.

The review reconstructed the source/Hessian and thermodynamic identities
from the rotating raw SU(5) action, then inspected
`matter_coupling/OCCUPIED_DERIVATION.md`, `occupied_matching.py`, the frozen
contract and `run_occupied/`. It also inspected the full-matrix normal
tadpole implementation in `rg_threshold/relaxation.py`. No occupied
calculation was rerun. Exact reviewed hashes and current-input manifest
validation are retained in `OCCUPIED_REVIEW_INPUTS.json`.

## 1. Actual rotating fields and heavy elimination

The selected classical R-phase convention rotates X and B by their common
phase θ and leaves A unrotated. For A=i aD, B=bD exp(iθ), X=X exp(iθ),
Tr D²=30, the angular kinetic coefficient is

    F0=X²+30b².

Here θ is arg X; the original R-angle has a factor two relative to this
convention. The classical potential at fixed X is

    (f−15ha²)²+(15/2)λ²a⁴+30a²(hX−λb)².

On the tree valley its constrained a,b Hessian is
Haa=120fh, Hbb=60λ²a², Hab=0. At fixed phase frequency ω the rotating
grand potential is U−ω²F0. Its linear normal sources are therefore

    J_a=CW_a,       J_b=CW_b−ω²60b0.

Minimizing the quadratic heavy energy gives exactly the retained subset

    Ω=U_RG−ω²F_RG−(1/2)[CW_a²/Haa+(CW_b−ω²60b0)²/Hbb].

Expanding once gives

    V=U_RG−(CW_a²/Haa+CW_b²/Hbb)/2,
    F=F_RG−CW_b(60b0)/Hbb,
    J=(60b0)²/Hbb,
    Ω=V−Fω²−Jω⁴/2.

Thus vacuum relaxation, the geometric angular correction and the quartic
occupied term are the same elimination. The code includes them once. It
does not add δU or δF a second time or discard the quartic source-square.
The a,b coordinates are fixed-X fiber coordinates; their Hessian factors
are consistent with the raw kinetic normalization and do not assert that
b itself is a canonical normal coordinate orthogonal to flat T.

The full-matrix tadpoles differentiate all scalar, Weyl/gaugino-mixing and
vector matrices. Their first spectral derivative h'(m²)=2m²[ln(m²/Q²)−1]
extends to zero at m²=0. The finite first derivative at gauge Goldstone
zeros does not require evaluating a real stable CW potential at neighboring
negative off-shell masses. It does not validate arbitrary higher off-shell
derivatives there. The matrix-directional and CP-odd controls in the saved
tadpole record check the implemented first derivatives.

The retained square is a definite finite two-loop-order *subset* in a fixed
gauge/subtraction convention. Its off-shell normal gradients and resulting
isolated relaxation piece can depend on that convention. Genuine finite
two-loop graphs and direct one-loop derivative/kinetic graphs remain
necessary for a matched physical result.

## 2. Stationary branch and Legendre transform

Let q=ω² and s=ln(X_reference/X_ref). With derivatives at fixed ω,

    Ω_s=V_s−F_s q−J_s q²/2,
    q=2V_s/[F_s+√(F_s²+2J_sV_s)]

selects the connected small-frequency branch when the discriminant and
denominator have the stated positive continuation. The reviewed finite
branch has positive q. It is not a classification of all roots or phases.

Direct differentiation independently yields

    n=−Ω_ω=2ω(F+Jq),
    C=−Ω_ωω=2F+6Jq,
    M=Ω_sω=−2ω(F_s+J_s q),
    N=Ω_ss=V_ss−F_ss q−J_ss q²/2.

At fixed charge n, ε=Ω+ωn and ∂_sω=M/C. Hence the constrained radial
Hessian is

    D=∂²_s ε|n=N+M²/C.

Along Ω_s=0, ds/dω=−M/N and dn/dω=C+M²/N=CD/N. Therefore

    dP/dε=n/[ω dn/dω]=nN/(ωCD).

For positive C,D,n,ω, the local sound/compressibility sign changes at
N=0, with the limiting interpretation of the divergent branch susceptibility.
It is not the fixed-charge radial D=0 condition. This is the appropriate
condition for this occupied phase state, rather than the old waterbag
U_ss−3U_s condition.

Keeping the same vacuum subtraction throughout gives

    P_ex=Fq+Jq²/2−V+Vvac,
    ε_ex=Fq+3Jq²/2+V−Vvac.

The code retains the 3/2 quartic coefficient in energy. Along the stationary
branch dP/dω=n and dε/dω=ω dn/dω. Its independent finite P(n) check uses
dP/dln n=c_IR² nω, which follows directly from these identities.

No uncomputed radial kinetic coefficient is used to turn D into a physical
oscillation frequency. The result concerns local thermodynamic and leading
IR response of this declared partial effective action. Its actual finite-
wavelength range requires the matched derivative terms and treatment of
the retained light fields.

## 3. What the finite numerical record establishes

At ε=.03, central matching scale and the declared reference branch, all
three five-point log-field stencils h=.01,.005,.0025 pass the frozen checks.
The nearly constant RG baseline U is retained in mpmath arithmetic while
the finite normal tadpoles are float64. The code appropriately uses finite
stencils for those tadpoles, rather than infinitesimal mp.diff through a
float64 function/cache.

The last two boundary ratios are 1.2126320815026 and 1.2126320804647; the
corresponding vacuum-subtracted w values are .61566951886 and .61566951721.
This supports reporting approximately 1.21263208 and .61567. It is not a
rigorous error interval or evidence of a monotone asymptotic stencil order.
The residual negative N at the numerical root is tiny compared with the
off-boundary values and should be read as a root residual, not a resolved
physical negative sign exactly at that root.

All sampled C and D values are positive. At X/X_min=1.2 the native state
still has c_IR²≈+.07257 and w≈.63651; at 1.3 it has c_IR²≈−.58161. Thus the
old waterbag's negative witness at 1.2 must not be imported into this phase
state. The phase state has its own later pressure boundary. Its w near
that boundary remains far from cold dust within this partial matching.

The direct P(n) finite-difference relative discrepancy is about 1.40×10⁻⁶,
below the declared 10⁻⁴ check. Maximum retained heavy displacement is
2.29×10⁻⁶ relative, below its 1% gate. The record contains 448 normal
evaluations, three field stencils and five declared branch samples each;
these are bounded numerical checks, not a new halo evolution or global
phase classification.

## 4. Optional light reservoir and coldness bound

For an *assumed free equilibrated* zero-temperature reservoir of twelve
unbroken Weyl gauginos, q_θ=1/2. Its grand potential is
−12(ω/2)⁴/(24π²)=−ω⁴/(32π²), equivalent to J_light=1/(16π²).
Because it is X independent it adds no J_s or J_ss, so the same stationary
q(X) and N boundary remain. It changes n,C,D and the excess pressure/energy
ledger. In the tested case its energy fraction is about 1.53×10⁻¹⁹, so it
does not change the displayed w digits. Equilibration, abundance, gauge
interactions and confinement are not derived. The Goldstino is correctly
not included as another free charged reservoir without its current map.

The separate two-derivative coldness inequality also passes as stated:
with F>0, a=F_s/F>0 and nonnegative native N along a connected branch,
q_s=N/(aF)≥0. Thus ΔU=∫q dF≤q(F−Fvac). With E_phase=Fq,

    w_ex=(E_phase−ΔU)/(E_phase+ΔU)≥Fvac/(2F−Fvac).

For canonical F∝X² this gives 1/[2(X/X_min)²−1]. This conditional
integral argument does not directly apply to the quartic Ω above, a
disconnected phase branch or an unknown fully matched kinetic action.

## 5. Remaining physical implications

The earned result is a conserving occupied-state elimination and its own
pressure/energy/charge ledger, including a previously omitted quartic
source term. It is stronger than attaching the old comparator portal to a
vacuum potential. The finite calculation still omits genuine finite two-loop
vacuum diagrams, direct finite derivative/two-point thresholds, quantum
transverse stability, gauge/IR/resummation, current anomaly/lifetime and a
selected cosmological occupation. These limitations prevent a full physical
no-go or halo prediction. The actual eigenmode-gas rest-source calculation
is a separate state problem and was not independently re-audited here.
