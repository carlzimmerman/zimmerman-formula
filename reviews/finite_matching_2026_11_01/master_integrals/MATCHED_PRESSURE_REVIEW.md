# Independent review of the retained order and matched phase pressure

Reviewer: `/root/independent_math_transport`, 1 November 2026. **Verdict:
conditional pass for the stated finite-order, fixed-scale homogeneous
phase calculation.** The genuine finite two-loop vacuum diagrams and
one-loop angular-current graphs have now been supplied, together with the
same-order normal heavy response. This advances beyond TP02's partial
RG/log matching. It does not establish an all-orders halo no-go or a
selected, long-lived cosmological phase.

## Counting and combination

At fixed scaled field, h=λ=e, g=√(29/200)e, f=1 and Q²/e fixed, the raw
action gives background fields of order e^−1/2 and squared masses of
order e. Consequently

    F0~e^−1, V1~e²/L, V2_reduced~e⁴/L²,
    δF_current,heavy~e/L, J_heavy~e^−2, L=16π².

On the loop-induced circular branch q=ω²~V1_s/F0~e³/L. Therefore both
δF q and J_heavy q² have the same e⁴/L² order as V2_reduced. The
implemented grand potential

    Ω=V−Fq−Jq²/2,
    V=V0+V1+V2_diagrams−(CW_a²/Haa+CW_b²/Hbb)/2,
    F=F0+δF_current−CW_b F_b/Hbb, J=F_b²/Hbb

retains all three terms of that normal source square exactly once. The
direct current coefficient is evaluated on the classical valley; shifting
that one-loop graph by a one-loop heavy displacement is a higher order.
An ordinary gapped one-loop ω⁴ coefficient contributes e⁶/L³ and is outside
this retained weak order. This statement requires the stated compact
admissible branch and small-frequency/gap hierarchy, not arbitrary fields
or a generic gapless nonlocal derivative expansion.

All ten finite vacuum graph classes are included. No RG-improved or
CS-derived logarithm is added again to their explicit finite sum. The
two-loop scalar/Weyl prefactors and raw vertices are independently audited
in VERTEX_AUDIT.md; DRbar-prime gauge functions were checked against the
primary source. The one-loop current, including the finite SV +1/2, is
independently reconstructed in CURRENT_FORMULA_AUDIT.md. The full finite
normal displacement is then a reduced-potential contribution, rather than
another two-loop one-particle-irreducible graph.

## Current pullback scale identity

The coordinator's CURRENT_PULLBACK_AUDIT.md also passes an independent
reconstruction. Start from the off-valley component-potential CS equation
and differentiate in b at the stationary classical valley. Since
V0_b=0, Hbb>0, Hab=0 and b0=hX/λ,

    ∂b[STr M⁴/(2L)]
      =−Hbb b0[(β_h/h−β_λ/λ)+γ_B,component−γ_X]
      =−Hbb b0(γ_B,component−γ_B,chiral).

The last difference is +5g²/L. Thus for the once-applied heavy pullback

    ∂lnQ δF_heavy=(60b0/Hbb)∂b[STr M⁴/(2L)]
                  =−300g²b0²/L.

Adding this to the graph-only component-current scale derivative yields
the reduced singlet-X CS identity. Replacing the component gauge gamma by
the chiral one inside the graph would be wrong; omitting the heavy
pullback would also be wrong. The numerical check tests the absolute
residual normalized by nonzero component sources because the total is
zero at the comparator. Its initial failed relative-to-zero assertion is
retained and is not a physical failure.

## Pressure implementation and finite coverage

The fixed-Q pressure driver was inspected directly. The high-precision
one-loop function is supplied at the inherited critical coupling, where
the complete one-loop supertrace makes its explicit Q dependence vanish.
The finite V2/current coefficients use the fixed physical Q prescribed
for each e. Their exact e⁴,e,e^−2 scaling is independently checked off
the Chebyshev interpolation nodes; it is not inferred from a fitted
pressure outcome.

The 21/29-node interpolation grids and h=.01,.005,.0025 field stencils
are separate repeated calculations. The reference-X derivatives include
every retained coefficient. The same Legendre ledger used in the fresh
TP02 occupied review is implemented:

    N=Ω_ss, C=−Ω_ωω, M=Ω_sω, D=N+M²/C,
    n=−Ω_ω, c_IR²=nN/(ωCD).

Every interpreted sampled point has positive n, excess energy, C and D.
The small-frequency branch has positive source and denominator. Vacuum
subtraction uses the same selected minimum consistently in P and excess
energy. The omitted field-independent U0 cancels in those excesses; no
cosmological vacuum offset is fitted by this operation.

The completed result has 48 cases: two couplings, four declared partial/
matched comparison schemes, three stencils and two interpolation grids.
For the finite-matched case the endpoints are approximately

| e | X/X_min | w_ex at endpoint |
|---:|---:|---:|
| .01 | 1.21394372 | .61415 |
| .03 | 1.21818639 | .60917 |

All sampled schemes retain positive IR sound at 1.2 and negative sound
at 1.3. This is the native phase state, not the old waterbag's different
1.2 pressure witness. Root/stencil and interpolation repeats and direct
P(n) differentiation pass their finite checks. The separately completed
gap check uses the actual minimum positive transverse tree gap; zero
sectors remain separately counted. Its maximum ω²/gap is about 1.22×10⁻⁹.

These are numerical agreement and hierarchy checks, not interval bounds
or errors on uncomputed higher orders. Algebraically solving the truncated
Ω without re-expansion generates some higher-order terms; those do not
estimate the missing terms. The completed perturbative coefficients do
not supply radial finite-momentum matching, anomalous R-current lifetime,
nonperturbative confinement/gapless dynamics, a cosmological occupation
or gravity. The safe conclusion is persistence of a pressure-rich endpoint
and a later negative local IR response in the specified finite-order
phase, at the two tested weak couplings.
