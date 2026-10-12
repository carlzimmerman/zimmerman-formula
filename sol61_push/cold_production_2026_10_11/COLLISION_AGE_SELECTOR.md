# Collision age does not supply the missing universal selector here

## Research decision

A radius defined by one collision per particle over a cosmic age is not a
successful acceleration selector for the detuned carrier in the declared
self-similar halo family. The mismatch follows from scaling, not just a
poorly chosen cross-section normalization. This closes one specific proposed
route; it is not a no-go theorem for the carrier's full halo dynamics.

## Conditional radius calculation

Take a cold-self-gravitating singular isothermal profile over the radii of
interest, with circular speed V:

    rho(r)=V^2/(4 pi G r^2), g_c(r)=V^2/r.

This profile is an analytic test family, not a formed solution of the
production calculation. Use a declared self-similar relative-speed
probability density f(y), y=w/V, and define

    K(V)=integral f(y) [sigma(Vy)/m] Vy dy.

The radius r_1 defined by rho(r_1) K(V) t=1 obeys

    r_1^2=V^2 K(V)t/(4 pi G),
    g_c(r_1)^2=4 pi G V^2/[K(V)t].

For a constant cross section per mass s, K=s V <y>, so the selected
acceleration scales as sqrt(V), rather than remaining constant. More
generally, a universal acceleration at fixed age requires K(V) proportional
to V^2, or a rate-averaged cross section proportional to V.

The detuned carrier instead has the tree cross-section factor

    R(x)=[(1-2x)/(1-x)]^2/[1+(w/(2c))^2],
    x=(w/(2cu))^2.

Throughout 0<=x<1/2 this is positive and strictly decreasing with speed.
For a fixed nonnegative f(y) whose support remains in this range, K(V)/V
therefore decreases as V increases. Consequently

    g_c(V2)/g_c(V1) >= sqrt(V2/V1), V2>V1.

Changing only the constant coupling normalization cannot remove this
speed dependence while staying in that regime.

## Finite detuned example

Use the saved candidate parameters and a Maxwell relative-speed shape,
truncated and renormalized on 0<=y<=6:

    f(y) proportional to sqrt(2/pi) y^2 exp(-y^2/2).

Its mean is 1.59576878. This rate distribution is stipulated; a truncation
is not a proof of a self-consistent global distribution function. The largest
sampled pair x is 0.090125, safely below the amplitude zero and resonance.
Set t=H_Lambda^-1=5.4596174e17 seconds using the earlier declared vacuum
density. The target is a0=(1/2)c sqrt(G rho_Lambda)=9.485696e-11 m/s^2.

| V, km/s | Effective sigma/m, cm^2/g | r_1, kpc | g_c(r_1)/a0 |
| ---: | ---: | ---: | ---: |
| 20 | 0.999911 | 0.9342 | 0.1463 |
| 50 | 0.999444 | 3.6918 | 0.2314 |
| 100 | 0.997773 | 10.4333 | 0.3275 |
| 200 | 0.991069 | 29.4106 | 0.4647 |
| 300 | 0.979821 | 53.7233 | 0.5723 |

The acceleration range is a factor 3.91249, exceeding the analytic minimum
sqrt(15)=3.87298. The required *constant cross-section surrogate at each
separate speed* would rise from 0.02140 to 0.32097 cm^2/g. These numbers are
inverse requirements, not separate tunings that establish the law.

All 14 radius/acceleration/rate consistency checks pass. They verify the
conditional arithmetic, not this mechanism as a dynamical attractor.
`collision_age_selector.py`, its contract, results and validated manifest
preserve the calculation.

## Vacuum scaling and baryonic normalization are additional requirements

At fixed V and microscopic K, setting t proportional to H_Lambda^-1 gives

    g_c(r_1) proportional to rho_Lambda^(1/4),

whereas the requested a0 is proportional to rho_Lambda^(1/2). In this
particular construction, enforcing the target would require

    K(V,rho_Lambda) = 4 pi G V^2/[t a0^2]
                   proportional to V^2 rho_Lambda^(-1/2).

No such vacuum-dependent scattering law is present in the detuned action.
Choosing the age scale alone does not supply it or derive kappa=1/2.

Finally, V_c^4=G M_b g_c follows at a radius where baryonic and cold
accelerations are equal for an enclosed baryonic mass M_b. The collision-age
condition does not identify that equality radius. Baryonic gravity would
also need inclusion in the halo solution; applying a cold-self-gravitating
isothermal approximation at equal gravity is not a controlled derivation.

A successful continuation therefore needs a dynamical baryonic/vacuum
coupling or a demonstrated formation mechanism that evades these particular
scalings. The protected low-pressure carrier remains a candidate substance,
not a completed explanation of the repository's galaxy law.
