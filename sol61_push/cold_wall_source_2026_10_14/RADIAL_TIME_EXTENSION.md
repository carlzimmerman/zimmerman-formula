# CWS-004: time dependence alone does not remove the radial momentum obstruction

Analytic extension of REPORT section2. Same stationary constant-speed bubble
metric and source action Mp^2 A(phi)R/2+P(phi,X). Permit phi=phi(t,r) and
A=A(t,r), positive and regular. No added normal-spatial momentum source.
Use a true flat cabin with b=b'=0 at r0>0. Claim: the necessary radial
momentum equation still forces b identically zero. This is not a statement
about higher-derivative scalar theories, vector currents or other metrics.

For the metric ds2=-dt2+dx2+dy2+(dz+b(x,y,z)dt)^2, n=(1,0,0,-b).
The contracted connection is

\[
 n^a\Gamma^t_{az}=n^a\Gamma^z_{az}=0,\qquad
 n^a\Gamma^x_{az}=-b_x/2,\quad
 n^a\Gamma^y_{az}=-b_y/2.
\]

Consequently, for any scalar A(t,x,y,z),

\[
 (\nabla\nabla A)_{nz}=A_{tz}-bA_{zz}
 +(b_x A_x+b_y A_y)/2.
\]

At z=0, radial symmetry gives A_tz=0, A_zz=A_r/r and
phi_z=0, even when phi_t is nonzero. Therefore T^P(n,ez)=0 and the necessary
equation is exactly

\[
 A(t,r)(b''+b'/r)+(b'-2b/r)A_r(t,r)=0.
\]

For every fixed t, positivity and regularity of A give the same nonsingular
homogeneous radial ODE as before. Zero initial b,b' force b=0 on the connected
interval. Time dependence of a radial first-derivative scalar alone does
not provide the missing directed stress. Nonradial phase structure, an
additional momentum carrier or different derivative/curvature operators are
still distinct possibilities requiring their own full field equations.

Review status: self-reviewed analytic proof, with the contracted connection
and arbitrary time-dependent Hessian verified in a separate bounded run.
Earlier canonical static-source inputs and outputs are preserved unchanged.
