# Extension to a regular nonconstant native potential: candidate audit leaf

The constant-V subfamily suffices for an existence-of-breakdown result within
the action family, but not automatically for a specifically selected rolling
potential. Here is the explicit local extension, with constant gamma,Khold,M
and V(phi)>0, a0(phi)^2=xi G V(phi) of sufficient C2 regularity on a clock interval.
Assume positive lower bounds and bounded parameter derivatives on that interval.
Let W=W(P,phi); subscripts P,phi hold the other variable fixed.

H=r²/2-V(phi)-W(P,phi)+(Ar-1-gamma r²)²/(2gamma).
The quantities h=H_r,R=H_rr,c²=h/(rR) are unchanged and independent of phi.
The clock coordinate is tau=phi, so n(phi)=r and e(phi)=0 exactly.
Put Zpot=V_phi+W_phi. The scalar rate becomes
 F=n(r)=-(hK+r²D_r u+W_P v+2BJ+Zpot)/R,
with S=F+r c²K. The spatial inverse before substituting F is now
 e(u)=W_PP v/r-W_P F/r³+W_P K/r²+W_Pphi/r,
 e(v)=D_r F/r+(r/gamma)u-2Ev+K(D-2PE)/r+2PB(a+E)/r.
The extra term in e(u) follows from n(W_P)=r W_PP v+r W_Pphi.

For rho=rh-H, rho_phi=Zpot, hence
 n(rho)=rR F+r²D_r(ru)+W_P(rv)+r Zpot
       =-(rho+p)K-2(rho+p_perp)B.
The spatial pressure identity is unchanged because e(phi)=0. Thus every
residual equation in RESIDUAL_PROPAGATION.md retains its form with the new
Vrate=F/r and new inverse; the extra W_Pphi term cancels in n(CA).
No explicit phi derivative enters e(Vrate) since clock slices have e(phi)=0.

The inverse matrix is unchanged; only bounded inhomogeneous sources change.
Coercivity and the Lp/parameter estimates therefore persist. The promoted
source is now explicitly clock-time dependent, locally Lipschitz in its state
and with bounded time dependence. The uniform approximation, difference and
continuation estimates have additional bounded coefficients only. No new
principal derivative is introduced.

The Riemann sources retain their exact formulas with the new S. The curvature
and metric-wave formulas retain their form with the new algebraic rho,p,p_perp.
Spatial differentiation of S adds Zpot_P=W_Pphi, with bounded/Lipschitz local
constitutive factors. The covariant TV and weighted Riccati estimates retain
bounded/linear-gradient remainders. Fixed-width-independent compact estimates
hold on a sufficiently short clock interval inside the chosen potential range.
The initial auxiliary and ADM constraints depend only on values of V,a0 at
phi0; their width-independent construction is unchanged.

Therefore, subject to verifying these explicit signs and source regularity,
the local theory and short-time packet-breakdown result extend to a regular
positive rolling potential, including any selected native potential satisfying
these local bounds. This is not an assertion about a potential zero, a pole,
a nonsmooth potential, or a time-dependent gamma not treated here.
