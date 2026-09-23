# An exact escape-delay identity and a density-free lag–width band

## Claim and epistemic status

The statements below are proved **within the specified conservative transport
model**. They are not algebraic restatements of an inferred lag. The lag is an
output of a stopping-time problem. An independently measured radius, temperature
and line variance give a band for a separate timing measurement.

This is a standard-physics consequence, not an established discovery of a new
law of nature. Applicability to an actual LRD and global novelty are unproved.
The homogeneous-density restriction on the final band is essential and is
deliberately falsified outside its scope in the supplied simulations.

## Physical model and observables

A stationary, spherical, conservative scattering cloud has outer radius R>0.
Its extinction per unit length kappa(r)=sigma_T*n_e(r) is continuous, bounded
and nonnegative. A central isotropic point source emits photons with the same
line profile in every direction. Photons travel at speed c and scatter with
the unpolarized Thomson angular kernel; in particular E[u'|u]=0. A photon
escapes when it first reaches the outer sphere with an outward direction.
All photons, including unscattered ones, are counted. There is no absorption,
replacement, occultation, bulk flow or time evolution of the cloud.

Let t_exit be its time to escape, r_exit its boundary position, and u_exit its
outgoing direction. For a distant unresolved observer define the excess delay
relative to direct central emission as

    D = t_exit - r_exit dot u_exit/c.

Rotational symmetry makes the all-direction ensemble distribution equivalent
to that seen by each observer. D is nonnegative. The mean delay is d_bar=E[D].
It is the first moment of the normalized photon impulse response, not a
variability baseline, a fitted damping time, or a cross-correlation peak.

## Theorem 1: radial profile, all scattering orders

For every cloud in this model,

\[
\boxed{\displaystyle
\bar D=\frac1c\int_0^R r\,\kappa(r)\,dr
      =\frac{\sigma_T}{c}\int_0^R r\,n_e(r)\,dr.}
\tag{1}
\]

This is not merely the single-scattering approximation. It holds at every
finite optical depth, including multiple backscatterings. Temperature and
frequency redistribution do not enter this spatial statement.

### Proof

For position x and unit direction u, put r=|x| and

    F(r)=2 integral_0^r s kappa(s) ds,
    f(x,u)=F(r)+2 x dot u.

The backward transport generator is

    L f = c u dot grad_x f + c kappa(r)(E[f(x,u')|u]-f(x,u)).

Streaming gives c F'(r)(u dot x/r)+2c. Scattering gives
-2c kappa(r) x dot u, because E[u'|u]=0. Since F'(r)=2r kappa(r),

    L f = 2c.

Initially f=0. At escape, f=F(R)+2R mu_exit, where
mu_exit=x_exit dot u_exit/R lies in [0,1]. Dynkin's stopped-generator identity
therefore gives

    2c E[t_exit] = F(R)+2R E[mu_exit].

Subtract the propagation advance R E[mu_exit]/c to obtain (1).

The stopping argument is justified rather than assumed: bounded kappa gives a
uniform positive probability exp(-2R*kappa_max) of no collision during any
interval 2R/c, which suffices for escape from the sphere. Thus the exit time
has an exponential tail bound and finite moments. f is bounded on the closed
phase-space domain. Apply Dynkin's formula at min(t_exit,t), then dominated
convergence for f and monotone convergence for the time integral. The origin
is harmless because F'(0)=0. This proves the claim for continuous bounded
kappa, including profiles vanishing in subregions.

At kappa=0, D=0 identically, and both sides vanish.

## Theorem 2: eliminate the density for a uniform, isothermal sphere

Now require constant kappa and constant electron temperature T_e>0. Set

    tau=kappa R,    s_e=sqrt(k_B T_e/m_e),
    sigma_sc^2 = sigma_out^2 - sigma_birth^2,
    d = c E[D]/R.

The spectral part uses leading-order, nonrelativistic thermal Doppler shifts,
neglecting recoil and second-order Compton drift. Birth variance is independent
of the electron thermal velocities, and the full emergent line is counted.
Within this approximation the earlier exposure theorem gives

    sigma_sc^2 = 2 s_e^2 E[N].

Constant collision rate also gives E[N]=c kappa E[t_exit]. This is a
compensator identity including the censored final flight, not a substitution
of a fixed number of mean-free-path steps. From Theorem 1 and its boundary term,

    E[D] = tau R/(2c),
    E[N] = tau^2/2 + tau E[mu_exit].

Writing b=E[mu_exit] in [0,1] eliminates tau and n_e:

    sigma_sc^2/s_e^2 = 4d^2 + 4bd.

Consequently

\[
\boxed{\displaystyle
\frac{\sqrt{1+\sigma_{\rm sc}^2/s_e^2}-1}{2}
\;\leq\;\frac{c\bar D}{R}
\;\leq\;\frac{\sigma_{\rm sc}}{2s_e}.}
\tag{2}
\]

No optical depth, electron density or fitted escape factor appears in this
bound. Its endpoints are conservative consequences of 0<=b<=1; no assertion
is made that both endpoints are attainable by a physical Thomson sphere.

There is no circularity: R and T_e can be separately measured; sigma_sc is a
spectral moment. D does not enter their definitions or calibration. A timing
measurement outside (2), with independently established model conditions and
measurement errors, falsifies the model. Deriving R from D and then testing the
same equation would instead be circular and is explicitly disallowed.

If only a conservative upper limit to sigma_sc is available, only the upper
lag bound follows. FWHM is insufficient without a full-profile assumption.
If temperature is variable but bounded below, the upper lag bound survives
using that lower bound, provided density remains uniform. The two-sided band
as written requires isothermality and the actual added variance.

## A density-free variability consequence

For the normalized nonnegative delay kernel H(omega)=E[exp(i omega D)],
|H|>=max(0,1-|omega| E[D]). Therefore (2) implies

\[
\boxed{\displaystyle
|H(2\pi/P)|\geq
\max\left(0,1-\frac{\pi R\sigma_{\rm sc}}{cPs_e}\right).}
\tag{3}
\]

This can constrain additional scattering suppression of a specified intrinsic
line signal. It does not constrain an unknown engine's intrinsic variability,
earlier thermalization, recombination delays, or different continuum paths.

## What cannot be inferred

1. The continuum photospheric radius is not automatically R, the outer radius
   of the scattering region. That identification is a testable physical
   hypothesis, not a Stefan–Boltzmann identity.
2. An LRD's line-forming region need not be a central point source.
3. n_H from a Balmer absorber need not identify any scattering density.
4. Density gradients obey (1), but generally NOT (2). Replacing kappa by an
   average is not legitimate. A simulated kappa(r)=a(1+99 r^2/R^2) explicitly
   violates the uniform lag–width band while passing (1).
5. A static spectrum alone still cannot set a dimensional lag: scaling every
   length by 1/a and density by a leaves the spectrum unchanged. The independent
   radius in (2) supplies the missing physical scale.
6. A null variability measurement does not by itself measure H.

## Illustrative scale, not an observational fit

For R=941 AU, T_e=10,000 K and a full Laplace scattered line with FWHM
2000 km/s, use sigma_sc=W/(sqrt(2) ln 2). Equation (2) gives a narrow interval
of approximately 12–14 days in the source rest frame. Equation (3) retains
more than half the amplitude of a 200-day input signal. The script reports
the precise numbers, and the radius necessary even to permit tenfold
suppression. This example does not claim these inputs describe one measured
LRD scattering cloud.
