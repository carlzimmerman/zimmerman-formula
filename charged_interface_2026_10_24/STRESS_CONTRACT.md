# CI-8: general kinetic stress necessary condition and phase recovery

For a stationary spherical species define radial kinetic pressure P_r>=0
and one-component tangential pressure P_t>=0 (streaming included).
The radial momentum equation is (r^2 P_r)' = -r^2 rho g_eff + 2r P_t.
With P_r(R)=0, it gives

P_r(r) = r^-2 integral_r^R [s^2 rho g_eff - 2s P_t] ds
       <= r^-2 integral_r^R s^2 rho g_eff ds = U(r).

Thus any U<0 excludes all such nonnegative kinetic stresses for this
prescribed density and calculated force, not just an isotropic closure.
It does not exclude extra confining boundary traction, a different density,
time dependence, or extra material stresses absent from the tested action.
All interface energetic forces are already included in g_eff=g0+dmu/dr.
The T population at R is numerically zero; no imposed T boundary pressure.

Evaluate U on the four CI-7 states without dropping small populations.
Check n128/256/512 and delta1e-5/1e-6. Also displace the last state by
plus/minus .2 kpc and minimize the same energy with all phase cells free.
Return under minimization is a local energetic basin test, not formation
or real-time recovery. A finite stationary Hessian is not continuum proof.
