# Fixed 3 kpc reciprocal law: isolated dwarf discriminator

Authorized scope: use the original KT15 sample, Plummer radii, luminosities,
HI masses, Upsilon_V=1..3 on the original 41-point grid, both a0 footings,
and the original two-sigma per-object cut. The new universal length is fixed
at 3 kpc. No dwarf-specific parameter or baryon change is allowed.

This first discriminator is the exact spherical **isolated** form of the
corrected response. It must not inherit KT15's 1D external-field grades or
be described as a complete satellite likelihood. Compare with a plain
isolated control on the same sample, not the historical primary EFE count.

For Plummer density rho and unit-density tracer p=rho/M,

```
g(r)=G M r/(r^2+a^2)^(3/2)+S_ell[A(g_source) rhat] dot rhat,
g_source=G M_enclosed[S_ell rho]/r^2,
A(g)=2g/[sqrt((g/a0)^2+4g/a0)+g/a0],
sigma_los^2=pi G M/(32a)+(4pi/3) integral p(r) r^3 g_ph,out(r) dr.
```

The stable response implementation uses A(g)=sqrt(a0*g) times a rational
factor, including A(0)=0. The displayed expression is understood by continuity
at zero. For z=rs/ell^2, the exact radial vector convolution kernel is

```
K1(r,s)=sqrt(2/pi) s^2/ell^3 exp[-(r-s)^2/(2ell^2)]
        * e^(-z)(z cosh(z)-sinh(z))/z^2.
```

It is derived by the angular integral of mu exp(z mu), not by convolving the
radial scalar acceleration. Small z uses its positive odd-power series;
larger z uses [(z-1)+(z+1)exp(-2z)]/(2z^2). The density kernel K0 replaces
the final factor by (1-exp(-2z))/(2z). Moving K1 onto the virial weight gives
one linear functional, evaluated for every mass without storing a full
matrix or recomputing the outer convolution for every Upsilon.

Independent representation: a normalized Plummer density is an exponential
mixture of centered Gaussians of variance a^2/(2t), with measure exp(-t)dt.
Gaussian convolution adds ell^2 to each variance. Also,
S_ell[x rho_sigma]=(sigma^2/(sigma^2+ell^2)) x rho_sqrt(sigma^2+ell^2).
This gives a distinct positive scalar-quadrature construction of both the
source field and the adjoint virial weight, used for selected checks.

Checks and bounds, fixed before execution:

- All 24 objects at radial n=1000 and 2000, base radius R=80a+16ell.
- Fornax/Sculptor/Leo I additionally at doubled R and mixture quadrature
  orders 128 and 256. No global refined pass-count claim from three objects.
- Density Gaussian variance-addition and mass conservation; vector Gaussian
  identity with fifth-power amplitude; all kernel weights nonnegative.
- Exact Newtonian Plummer sigma^2=piGM/(32a), independently integrated.
- Zero-width plain response, including original isolated count comparison.
- Numerical acceptance: smoothed/input truncated mass discrepancy<1e-3;
  Gaussian/vector Gaussian relative peak errors<1e-3; Newton check<1e-3;
  selected sigma changes under refinement/domain/independent representation
  below .02 km/s. Expose any failure and retain run artifacts.

The omitted outer phantom virial tail has a useful analytic bound. Positivity
gives g_source(s)<=GM/s^2 and A<=sqrt(a0 g_source). The vector convolution's
magnitude is at most the scalar convolution of this upper envelope, namely
sqrt(GMa0) erf(r/(sqrt(2)ell))/r <=sqrt(GMa0)/r. Hence

```
0<=sigma_ph,tail^2 <=sqrt(GMa0)[1-M_Plummer(R)/M]/3.
```

This bounds the uncomputed outer measurement tail, not all numerical errors
or the finite input-density truncation. The recorded convergence checks remain
empirical; no certified observational pass is claimed.

Physical units match the MW solver: G_SI=6.67430e-11, Msun=1.98847e30,
kpc=3.0856775814913673e19m. KT15's rounded G=4.30091e-6 and kpc=3.0857e19
differ negligibly but are disclosed when reproducing its archived controls.
Original files remain read-only. Each new bounded run has a contract and
input/output hash manifest; no randomness is used.
