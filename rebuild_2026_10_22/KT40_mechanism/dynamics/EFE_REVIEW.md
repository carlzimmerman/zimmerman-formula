# Independent review of the fixed-uniform-field scalar virial

Verdict: the variational identity and homology sign are **proved as written**
under the stated centered-source, fixed external boundary gradient and
boundary-decay assumptions. The negative virial assertion is **computationally
verified in the recorded finite range**, not at every possible external field.
Reviewer: mechanism_dynamics, separate from the EFE implementer. Inputs and
raw sign/sum checks are pinned in EFE_REVIEW.json.

Starting directly from the energy, use size expansion rather than the
author's compression convention: rho_lambda(r)=lambda^-3 rho(r/lambda),
psi_self,lambda=lambda^-1 psi_self(r/lambda). Then

    d rho/d ln lambda=-div(rho r),
    d g_self/d ln lambda=-(2g_self+r.partial_r g_self),
    d H_self/d ln lambda=-(3H_self+r.partial_r H_self).

The full first variation delta U=integral Phi delta rho gives
dU/d ln lambda=+integral rho r.grad Phi=+W. Meanwhile
U_ph=-(1/8piG) integral [f(e+g,H)-f(e,0)-2A_ext.g],
with f=E-g.g, yields

    W_ph=(1/4piG) integral [(A-A_ext).(2g+r.partial_r g)
                           +B:(3H+r.partial_r H)].

This agrees with the author's sign after reversing the homology parameter.
There is no missing derivative of e: the auxiliary boundary gradient is
held fixed. The uniform *physical* external acceleration contributes zero
because integral rho r=0. Its tangent subtraction has zero angular-integrated
virial, while making the energy remainder absolutely integrable before
angular integration. A constant potential likewise drops out at fixed mass.

For the spherical self field, the radial/tangential Hessian eigenvalues are
g' and g/r. Contracting the full Frobenius tensor gives exactly

    sigma_ph²=(1/6GM) integral r² dr dmu [
      (A_r-A_ext mu)(2g+r g')
      +D g'(3g'+r g'')+2D(g/r)(2g/r+g')].

The two tangential components account for the explicit factor 2. The
Newtonian term is positive pi GM/(32a). Independently, angular averaging
the field equation gives the regular monopole force

    <g_ph,r>=<A_r>-partial_r<D g'>-2<D(g'-g/r)>/r.

Angular-divergence terms integrate to zero; the regular origin gives no
central point-mass integration constant. This is the force form used by
the separate monopole check and confirms the same Hessian sign.

I rechecked all raw three-grid sums of Newtonian+A+B, all stored signs and
the independent monopole signs. All 1,312 distinct configurations at the
four nonzero sampled eta values have W/(3M)<0 on all three grids. The
isolated eta=0 configurations have positive total variance. Source/energy
and monopole numerical checks pass in their original manifests.

For an isolated finite system in a prescribed constant external field,
stationary scalar virial balance requires 2K=W. With positive-mass tracers,
K>=0 regardless of velocity anisotropy. Thus a genuinely negative W excludes
a stationary equilibrium of the *fixed density/tracer profile under these
assumptions*. It cannot be repaired by choosing a different line-of-sight
projection or a positive anisotropic dispersion tensor.

It does not by itself exclude different density shapes, time-dependent or
tidally affected objects, or all possible environments. In particular eta
means the auxiliary Newtonian gradient e/a0; the physical uniform external
acceleration is nu(eta)e. Values eta=.1,.3,1,3 have not been identified with
the actual fields of the named satellites. That environmental mapping or
a lower-eta continuation is necessary before treating this finite sign
result as an observational rejection of those satellites.
