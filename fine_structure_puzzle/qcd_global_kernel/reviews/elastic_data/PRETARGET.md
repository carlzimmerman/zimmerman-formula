# Independent pretarget, before opening author implementation/results

From supplied B(z), put t=z², d=1+t, r=sqrt(d)-z and E=GE, M=GM.
Sachs convention: F1=(E+t M)/d, F2=(M-E)/d; hence A=(E²+t M²)/d.
Then B=a E²+b E M+c M² with
 a=r+z(2-t)/(2d²), b=3zt/d², c=-2tr+zt(2t-1)/(2d²).
This follows by direct expansion: 3F1²-A=[(2-t)E²+6tEM+t(2t-1)M²]/d²,
and dA-3tM²=E²-2tM².
At each fixed z, derivatives are B_E=2aE+bM and B_M=bE+2cM.

For finite nodes z_0<...<z_(n-1), the trapezoid functional is
T=C sum_i w_i B_i, with endpoint weights half the adjacent spacing
and interior weights w_i=(z_(i+1)-z_(i-1))/2. C denotes a separately
specified external normalization. This quadrature is in z, not Q²;
Q=sqrt(Q²), z=Q/(2m). No endpoint at zero is implied.
The sensitivities are g_(E,i)=C w_i B_E and g_(M,i)=C w_i B_M.
For fixed marginal standard deviations σ_j and any PSD covariance Σ,
|Σ_jk|≤σ_jσ_k by Cauchy-Schwarz, so the first-order propagated
standard deviation obeys sqrt(gᵀΣg)≤sum_j |g_j|σ_j.
The bound is sharp among arbitrary PSD matrices with those diagonal
entries, via Σ_jk=sign(g_j)sign(g_k)σ_jσ_k. It is only a covariance
ceiling for linear propagation, not a reconstructed covariance or
nonlinear distributional error bound. With independent variables the
standard deviation would be sqrt(sum_j(g_jσ_j)²), a separate assumption.
The finite point functional alone does not determine missing tails,
subtraction functions, proton electromagnetic self-energy, or alpha.
