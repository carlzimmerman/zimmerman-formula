# Coordinator independent review: shared-scalar and QCD bridges

Parent FSP-001; work package FSP-002. The coordinator derived the equations below from the displayed candidate definitions and inspected the final scalar checker and QCD v2 checker. This is same-team independent algebra, not a new full-QCD, curved-space or quantum-gravity calculation. Input hashes are pinned in REVIEW_INPUTS.json.

## QCD cosmological matching

For the stated natural-unit candidate epsilon=c_H H Lambda^3, Friedmann H^2=(8 pi G/3)epsilon implies H=(8 pi G/3)c_H Lambda^3 on the nonzero de Sitter branch. In SI units, with m_Lambda=Lambda_energy/c^2,

`H = (8 pi/3) c_H G m_Lambda^3 c/hbar^2`.

Combining with the framework's same-epoch de Sitter relation a_M=kappa c sqrt(3/(8 pi)) H gives

`a_M hbar^2/(G c^2 m_p^3) = kappa sqrt(8 pi/3) c_H/C_p^3`,

where C_p=m_p/m_Lambda. Both sides are dimensionless and the numerical factors agree. This is conditional on the linear cosmological term, its sign/coefficient, the vacuum subtraction/matching and the de Sitter solution. The paper's extension from its hyperbolic calculation to physical QCD in de Sitter is not a result established by this algebra. The current cosmic epoch cannot simply replace the asymptotic solution when the vacuum evolves.

The pure-QCD trace identity is not the entire physical QCD+QED trace identity; the latter contains electromagnetic anomalous terms. The final QCD report distinguishes that limit and its subsequent electromagnetic matching model.

## Electromagnetic-sensitive local matching

Take the declared leading functions H=d q Lambda^2(1+v alpha) and m_p=(C0+c_gamma alpha)Lambda+c_q q. Direct differentiation gives

`det d(H,m_p)/d(Lambda,q) = -d Lambda^2 (1+v alpha) D`,

`D=C0+c_gamma alpha-2 c_q q/Lambda`.

On the regular domain specified by the report, holding H fixed gives delta q=-q[2 delta Lambda/Lambda+v delta alpha/(1+v alpha)]. Substituting into delta m_p=0 with delta alpha=1 gives exactly its displayed delta Lambda and null tangent. This is an actual local curve by the implicit-function theorem, not just a formal kernel vector at a singular constraint.

The physical expanding branch additionally requires 1+v alpha>0 and positive proton mass, as distinct from the weaker nonvanishing condition sufficient for the algebraic implicit-function theorem. These signs must persist within the admitted local neighborhood.

With q independently fixed, the remaining determinant is

`d q Lambda^2 [2 c_gamma-C0 v+c_gamma v alpha]`.

It is not identically zero, so the theory **can in principle constrain alpha** after its matching functions are calculated and q is independently known. An independent measured quark-mass input is legitimate for this conditional correlation test; it need not first be derived from the same framework. The result is local identification under a nonzero determinant, not a global uniqueness or actual precision claim. It vanishes in the exact zero-EM-response limit, as required.

QCD v2 explicitly includes the electron threshold in inverse alpha0 as `2(log M-log m_e)/(3 pi)`. Its derivative at fixed physical boundary is `-2/(3 pi)`; the earlier partial formula's fixed remainder could not be used to vary m_e consistently. The v2 matrix's first two rows remain dependent, while the independent EM integration constant and electron-mass output bring total rank three. This is a restricted product-gauge one-loop diagnostic, not full SM running across the electroweak region.

The coordinator also independently derived the final constrained-sensitivity qualification before reading the agent's new note. With p=log C_p, h=log c_H, P=sum_i partial p/partial log(mhat_i/Lambda), Q=sum_i partial h/partial log(mhat_i/Lambda), and alpha partials taken with these ratios fixed, preserving physical quark masses and proton mass gives d log Lambda/d log alpha=-p_alpha/(1-P). Consequently S_constrained=h_alpha-(3-Q)p_alpha/(1-P). This agrees with CONSTRAINED_SENSITIVITY.md on its regular branch 1-P!=0. Rescaling Lambda by a positive s(alpha) sends C_p to C_p/s and c_H to c_H/s^3; both their ratio and its derivative along this specified physical constraint path are invariant. The agent's explicit transformed derivatives agree by cancellation of the d log s/d log alpha terms. This is hand algebra, not an additional executed experiment.

## Shared-scalar stationary point and finite family

Use the scalar candidate B(x)=B_*+beta x^2/2, Lambda=M_U exp(-aB), m_N=C_N Lambda, m_e=y M_U exp(-pB), and alpha=1/(4 pi k_gamma B). At x=0 the first B derivative vanishes. Differentiating the proposed potential U(B)-C Lambda^4+n_N m_N+n_e m_e gives

`V_xx(0)=beta[U_B+4aC Lambda_*^4-a n_N m_N*-p n_e m_e*]`.

The signs follow respectively from d(-C Lambda^4)/dB=+4aC Lambda^4 and dm/dB<0. Thus negative QCD vacuum energy and positive nonrelativistic matter prefer opposite extrema of B in this specified matched model. The absolute QCD vacuum sign/value and compensating U are model data here. Canceling the value of the potential does not cancel its B derivative. No empirical fifth-force exclusion follows at a common extremum with all linear couplings zero.

For fixed M=m_N, R=a_H m_N, and vacuum density, the stated family M_U(t)=M exp(at)/C_N, y(t)=C_N exp[-(a-p)t]/[R/(4 pi k_gamma t)-1] preserves M and R for every admitted t. It also preserves Lambda(x)=M exp(-a beta x^2/2)/C_N and the QCD part of its scalar profile. The electron mass varies, as the report explicitly states; this is not a family preserving every laboratory observation. At fixed R and an independently known electron/nucleon mass ratio, alpha is already determined by the atomic measurement identity.

In the report's coordinates the three-row constraint matrix has minor -1/(1+r), with r=m_e/m_N>0. Its displayed null vector indeed annihilates all three rows and changes log alpha by -1/B_*. Adding a fixed physical M_U gives determinant a/(1+r)>0. This proves that the remaining freedom is an actual physical-threshold/Yukawa freedom in the candidate, not an arbitrary change of renormalization scale within one matched theory. It also proves the stated conditional exception: an independent threshold and complete common-gauge matching can remove this particular defect. They have not been supplied by the frozen framework.

Finally, for V=rho0+A exp(-px)-C Lambda0^4 exp(-4ax), stationarity gives pX=4aY, so V_xx=p(p-4a)X and V-rho0=(1-p/(4a))X. The formula for x* has the correct sign. The positive-curvature branch p>4a lies below the offset, and p=4a gives no isolated stationary point. A physically admissible scalar/gauge-domain restriction must still be imposed when applying the root.

## Verdict and next decision

The reviewed algebra is **proved under the stated candidate hypotheses**. The physical alpha prediction is **conditional on uncomputed matching/selection inputs**, not achieved. The QCD route supplies a specific potentially measurable ratio and a positive identifiability control; the scalar route supplies a conditional mass-to-coupling mechanism and an explicit surviving family. Neither should be summarized as a theorem that a baryon/vacuum link is impossible.

The next physical calculation is to derive the QCD cosmological response coefficient and its EM dependence with independently fixed quark-mass inputs, or to supply the common physical gauge threshold/functions from one microscopic theory. A new fit of those unknowns to alpha would consume the proposed prediction.
