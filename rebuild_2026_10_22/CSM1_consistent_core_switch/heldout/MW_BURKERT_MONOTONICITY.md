# Conditional compact-Burkert monotonicity argument

Fix M>0, outer mass-match radius R>0, and observation radius 0<r<R. Use spherical enclosed halo mass, hence the plane radial contribution is Vh²(r)=G Mh(<r)/r. B(x)=log(1+x²)+2log(1+x)-2 arctan(x), with B'(x)=4x²/[(1+x)(1+x²)]. The implemented mass is pi Sigma r0² B(r/r0), and the outer mass target is M. The untruncated formula at r is valid here because every tested r=R0 is below R200.

Let f(x)=1/[(1+x)(1+x²)], m(x)=integral_0^x t² f(t)dt=B(x)/4, and g(x)=-dlog f/dlog x=x/(1+x)+2x²/(1+x²). Then g is strictly increasing from0 to3. Let h(x)=dlog m/dlog x=x³ f(x)/m(x). Integrating the derivative of t³ f(t) gives

    h(x) = [integral_0^x (3-g(t)) t² f(t)dt] / m(x) > 3-g(x).

Thus dlog h/dlog x = 3-g(x)-h(x)<0. Also h tends to3 at0 and0 at infinity. The outer mass factor F(x)=B(x)/x² therefore increases where h>2 and decreases where h<2, with exactly one maximum xpk where h=2.

The compact mass-match root has x=R/r0>=xpk. At this root M=pi Sigma R² F(x). On the compact branch, increasing Sigma decreases the required F and therefore increases x. For q=r/R in(0,1), the enclosed fraction is H(x)=B(qx)/B(x). Its logarithmic derivative is h(qx)-h(x)>0. Consequently Mh(<r)=M H(x) increases with Sigma on the exact compact branch.

If no mass-match root exists, the implemented saturation convention chooses the r0 that maximizes outer mass, r0=R/xpk. That scale is independent of Sigma, because log Sigma only adds a constant to the maximization objective. Its enclosed mass is proportional to Sigma. At the transition the saturated maximum outer mass equals M, so the two formulae join continuously. The native core floor max(Sigma0, C[Lq(M)]^(5/4) Sigma_coll(M)) is nondecreasing in L>=0. The exact-arithmetic model speed for each fixed baryonic cell is therefore nondecreasing in L, and so is the maximum over the fixed finite box.

Numerical restriction: GD2 uses bounded minimization over r0 in[R*1e-6,R*1e3] and bracketing from R*1e-7 to the maximizing r0. The unique analytic maximizing scale must lie in those bounds, and evaluated compact roots must remain in the bracketing interval. The scalar audit checks these restrictions, radii, saturation state and reconstruction residuals for the evaluated endpoints and registered L cells. Floating minimization/roundoff is not an exact proof certificate. This argument is conditional on the fixed spherical compact-Burkert and saturation conventions; it makes no claim for another halo branch, retuned mass relation or a larger baryonic family.
