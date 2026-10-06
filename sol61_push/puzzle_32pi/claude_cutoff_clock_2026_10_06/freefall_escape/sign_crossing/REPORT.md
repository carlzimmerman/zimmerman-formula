# Isolated clock-gradient zero: a regular local crossing with a restrictive flow condition

This addresses the actual missing local branch connection: negative signed clock gradient in the inner freefall escape, positive gradient in the outer MOND candidate. It proves pointwise admissibility criteria and constructs a bounded local vacuum crossing. It does not construct a globally matched source/cosmological solution or a regular center. Prior scientific inputs are unchanged.

## 1. An isolated zero is not a geodesic interval

Use n=3, signature−+++, the same logarithmic KGB plus fixed-A cutoff response, η=c/(3K_EH*²)∈(0,1), and signed a=N'/(NB). At a=0, the even response has U=U_a=0 but U_aa=2. Its current is
j_response=K_E V(r²U_a)'/(qBr²).
Thus at an isolated zero it contributes2K_EV a'/(qB). It is incorrect to omit this derivative and impose clock expansion3H*. That condition applies to an interval with a≡0, for which a'=0 as well. The geodesic-interval lemma remains valid.

In vacuum with V≠0 the exact momentum equation gives B'=0 at the zero. The zero-current/lapse equation then fixes
κ:=a'=BηH*[3H*+(V'+2V/r)/N]
=BηH*[3H*−θ],
θ=−(V'+2V/r)/N.
Consequently the desired negative-inner/positive-outer crossing has κ>0 exactly when θ<3H*. U_aa=2 keeps the stationary derivative determinant nonzero at this point. There is no critical rank loss or inverse-kernel singularity at a=0.

## 2. Exact pointwise radial, metric, and mass conditions

Put w=−V/(H*rN)>0 for the outward-flowing clock, D=(1−B^−2)/(H*²r²). The actual vacuum potential remains K−ρ_v=K_EH*²[−3+6η ln N]. The radial equation determines
V'=N H*/(2w)[D+w²−3+6η ln N],
θ/H*=[3w²+3−6η ln N−D]/(2w),
κ=BηH*²[D+6η ln N−3(w−1)²]/(2w).
These are exact values at the zero, not an asymptotic force identification. Define χ=F/(N²B²)=B^−2−H*²r²w²>0 and cosmological-background-subtracted Misner–Sharp mass
m_MS=r/2[1−χ−H*²r²].
Then
κ>0 iff 2m_MS/(H*²r³)+6η ln N>4w²−6w+2.
The physical proper stationary-observer force is
 g0=[m_MS/r²−H*²r(1−3η ln N)]/√χ.
Attraction requires m_MS>H*²r³(1−3η ln N), independently of assuming a=gphysical. F>0, N>0 and B>0 are additional patch conditions.

For μ=m_MS/(H*²r³), the permitted positive crossing-flow interval is between the roots
w_±=[3±√(1+8μ+24η ln N)]/4,
when real; retain only positive w and the χ>0 interval. In a mass-dominated weak-lapse region μ≫1, w_+≈√(μ/2)+3/4. Freefall has w_ff≈√(2μ), twice as large at leading order. Thus the desired clock-gradient zero cannot lie arbitrarily close to the nearly geodesic freefall data in that regime: the flow must slow to approximately half that speed or less at the crossing. This is a necessary local transition condition, not a universal nonexistence result. The outer MOND-like w≈η can satisfy it.

An admissible weak-field example uses H*=1,η=.5,A=1,T=128.9153707043,r0=.001,N0=.99999,w0=.5,m_MS=1e−8. Choose B0 from B0^−2=1−H*²r0²[2μ+1−w0²] and V0=−H*r0N0w0. It has positive F, attractive g0≈.009, and κ≈10>0. m_MS here is local geometric data, not an asserted baryonic mass; no target coefficient was fitted.

## 3. Conserved static-fluid source version

For a perfect fluid stationary along the metric Killing vector, let proper density and isotropic pressure be ρ,p. Its ADM quantities are
E=N²(ρ+p)/F−p,
P_r=p+B²V²(ρ+p)/F,
δS_m/δV=NB³r²V(ρ+p)/F.
The sourced momentum equation at a=0 gives B'/B=r(ρ+p)/(2K_Eχ), so setting B'=0 inside matter would be incorrect. The source terms cancel identically in the stationary current/Euler identity: static Killing matter has zero mixed radial energy flux and does not inject scalar shift charge.

Retaining the density/boost terms in the radial equation and θ gives the exact simplifications
κ=BηH*²[D+6η ln N−3(w−1)²+p/(K_EH*²)]/(2w),
g0=[m_MS/r²−H*²r(1−3η ln N)+rp/(2K_E)]/√χ.
Density and the boosted-pressure piece cancel out of these pointwise formulas; proper pressure remains. Positive pressure can assist the crossing. It is not a freely prescribed force: conservation requires p'=−(ρ+p)F'/(2F), together with an equation of state/source solution. No fluid interior was constructed here.

## 4. Local Taylor solution through the vacuum zero

Let δ=r−r0 and κ>0 as fixed above. On the regular nonzero-V vacuum patch,
a=κδ+O(δ²),
N=N0+(N0B0κ/2)δ²+O(δ³),
B=B0+(B''0/2)δ²+O(δ³),
V=V0+V'0δ+(V''0/2)δ²+O(δ³),
B''0=−B0²κ(1−η/w0),
N''0=N0B0κ,
V''0=N0N''0/(V0B0²)+V0N''0/N0+ηH*r0N''0−2V'0/r0−(V'0)²/V0−N0²(K−ρ_v)/(K_EV0).
The V'' expression follows by differentiating the exact radial equation; response-pressure first derivative vanishes at the zero. The coefficients determine a local lapse minimum with the required clock-gradient signs.

The action contains |a|³ near zero. It is C², not generically C³ there. The signed ODE has a continuous locally Lipschitz vector field because U_aa(0)=2, so ordinary local existence/uniqueness holds in the regular patch, but higher Taylor coefficients should be interpreted one-sided. For κ>0 the leading response gives the one-sided jump a''_+−a''_−=4κ²/A. This is a regularity issue, not the cutoff's distinct U_aa=0 critical surface. The local metric remains sufficiently differentiable for the displayed field equations.

The bounded DOP853 calculation integrates the exact stationary momentum/radial/current system from the example in both directions to r0±1e−6, with actual inverse-cutoff response and no imposed acceleration law. Current reduction is equivalent to the lapse equation on this nonzero-V patch by the authenticated Euler identity. It verifies a<0 inward, a>0 outward, F>0 and positive clock Hessian, checks the point slope and Taylor coefficients, and refines tolerances. A tiny neighborhood is all that is claimed. V and metric data have not been matched to a source or a cosmological boundary.

## 5. Missing implication and evidence

The crossing is locally allowed and does not require encountering the cutoff critical magnitude~13A. Yet the flow bound shows it is not a perturbation of freefall at that point in a mass-dominated exterior. A full transition must solve the coupled radial flow/metric equations, then connect to both asymptotic branches and a conserved source. The zero-point conditions do not fix A/H*: A first enters beyond these leading point/Taylor coefficients. Local mass data are not sufficient to calibrate a baryonic mass or Newton coupling.

checks.py independently reconstructs the vacuum and sourced point formulas, source-current cancellation, Taylor coefficients, admissible/counterexample data and exact short two-sided IVP. Negative controls omit U_a' at the isolated zero, classify freefall-oriented data as the desired crossing, or mis-sign the pressure source. Fresh bounded manifests pin all input revisions. This is a local branch-connection advance, not a global theory completion, full finite-gradient stability result or32π selector.
