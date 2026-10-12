# Retuning the crossover cannot greatly reduce the coherent sound distance

Status: optimization within the specific softened EOS family, at fixed
illustrative halo support. This is not a bound over arbitrary interactions
or a cosmological observational exclusion.

## Hold the halo requirement fixed

For the family c_s^2=H_sound x/(1+x^2)^(3/2), let
x_h=rho_h/rho_cross. Require c_s(rho_h)=c_h, with the previously chosen
rho_h=1e-21 kg/m^3 and c_h=200 km/s. Vary the crossover and adjust the
strength consistently:

    rho_cross=rho_h/x_h,
    H_sound=c_h^2(1+x_h^2)^(3/2)/x_h.

This is a parameter-family test, not a derivation of the halo requirement.
Changing only the crossover while silently changing the halo support would
not address the same problem.

## An analytic minimum in a matter-only background

With H=H_m a^-3/2, H_m=sqrt(8 pi G rho_m,0/3), integrate the comoving
sound distance over a from zero to infinity as an analytic control. For
x=(rho_m,0/rho_cross)a^-3,

    r_sound = [sqrt(H_sound)/(6H_m)]
       (rho_m,0/rho_cross)^(1/6) B(1/6,7/12).

The integral follows by substituting x and using
integral_0^infinity x^(-2/3)(1+x^2)^(-3/4) dx=B(1/6,7/12)/2.
After imposing the fixed halo support, the only x_h dependence is

    r_sound proportional to (1+x_h^2)^(3/4) x_h^(-1/3).

It diverges as x_h tends to zero or infinity and has its unique minimum at

    x_h=sqrt(2/7)=0.5345224838.

Moving the crossover far earlier or later therefore does not monotonically
remove the integrated pressure effect while retaining this halo support.
The necessary strength adjustment competes with the shift in epoch.

This matter-only infinite history is not the actual cosmic history. It
is a tractable control that identifies the tradeoff and a global minimum
within that specified idealization.

## Declared radiation/matter/vacuum background

Using the same finite history a=0.001 to 1 and background densities as
PORTAL_COSMOLOGY.md, direct quadrature and optimization over
0.05<=x_h<=4 give

    optimum x_h=0.5353375686,
    minimum comoving sound distance=1.110990639 Mpc.

The original x_h=1 choice gave 1.254584987 Mpc. Thus retuning improves the
sound distance by only about 11.45% in this search. The analytic matter-only
minimum is 1.138306966 Mpc, close to the finite-background optimum. The
finite-history numerical search is not a certified global optimization
over all positive x_h, though its interior minimum agrees closely with
the analytic control. The searched strengths remain small relative to
rest energy; no relativistic large-pressure extrapolation is used here.

Sound distance is a diagnostic, not a power-spectrum likelihood or a
one-to-one measure of final growth. No retuned transfer function or
observational exclusion is asserted. The calculation does establish that
this simple retuning does not reduce the characteristic pressure travel
scale by orders of magnitude while keeping the chosen halo support.

## Verification and research decision

portal_retuning.py checks the analytic optimum against numerical
minimization, the beta integral against independent quadrature, the original
sound distance, refined finite-background quadrature, and the fixed halo
speed throughout the sampled family. All 11 checks pass; the manifest
validates provenance. The interpretation is self-reviewed.

Together with the composition-independent local force identity, this
narrows two simple ways of trying to save the density-only portal: changing
the source fraction does not eliminate its total-density force, and moving
its crossover within the tested family yields only a modest sound-distance
reduction. The candidate still needs a derived state-dependent response
or a different mechanism. Neither this optimization nor the earlier
stability/production results completes the repo's cold-energy construction.
