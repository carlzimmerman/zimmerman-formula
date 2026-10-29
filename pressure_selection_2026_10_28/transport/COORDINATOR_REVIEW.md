# Coordinator reconstruction of the transport calculation

Reviewer `/root`, 2026-10-28. This is a separate derivation of the critical
identities and scope, not a blind fresh-session review. The author had shared
the route's result before this written review. No formal certificate is claimed.

The stated instantaneous compatibility conclusions are correct as written.
From (3/2)Dp+(5/2)p theta+div q=Q and D rho=-rho theta,
the fixed-EOS coefficient is C=5p-3rho P'. Integrating the regular radial
divergence gives q=-integral(C theta r²dr)/(2r²), with the sign and factor
in the report. The excluded inverse-square integration constant would indeed
be a point source.

Differentiating T=p/rho and using p'=-rho g, p_rho=A/rho, gives
T'=(p/A-1)g. Thus a center with p>A is a temperature minimum, while pure
compression with C>0 requires outward flux. The MC27 offset 2/3 and
x_c<=1/4 put every relevant center strictly in that regime. The threshold
x=exp(-1/3) and its second derivative are correct. At this interior maximum,
finite Fourier conductivity supplies zero flux but the integrated trace
condition requires a nonzero flux for either sign of uniform theta.

With direct exchange, Q=C theta/2+div q. Its volume integral yields
L_Q=|theta| integral(C dV)/2 -4pi r²q under compression. Inserting q=-kappa T'
reproduces the positive conductive term in equation (18). At a smooth center,
div q=-4piG kappa_c rho_c(p_c/A-1), confirming (17). The integrated bound
is not a pointwise bound at arbitrary r; the report correctly separates them.

For the extra full-EOS assumption, the exterior has rho P'=3p/2, so C=p/2.
Inside, C-p/2=(9/2)p-3A>=0. Therefore p/2<=C<5p on matter, and K=3 integral(p dV)/2
gives exactly |theta|K/6<=L_Q<5|theta|K/3. The vacuum-edge argument is valid
with its explicit zero-boundary-flux assumption. Escape populations and a
changed exterior closure remain outside it.

No algebra correction was needed. The claim is instantaneous and conditional
on isotropic stress, the specified fixed EOS and flow, and the asserted
Fourier law. It does not prove a dynamic invariant manifold, exclude nonlocal
transport, or select A. The numerical record was inspected separately; its
finite examples supplement these analytic arguments. Exact reviewed artifact
hash is recorded in the coordinator's final verification file.
