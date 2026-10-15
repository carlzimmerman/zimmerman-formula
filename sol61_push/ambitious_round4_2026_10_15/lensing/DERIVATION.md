# Projection and finite-source identities

Let x=R/rM, v=sqrt(1+4x²), m=1/v². In units Mb/rM²,
the infinite exact-law point-source surface density and cylindrical excess mass are

    Sigma_ex(x) = K(m)/(pi*v),
    M_ex,cyl(<x)/Mb = [v E(m)-1]/2,
    DeltaSigma_total = [v E(m)+1]/(2*pi*x²)-K(m)/(pi*v).

Here K and E use the parameter convention of SciPy's complete elliptic
integrals. They follow by substituting line-of-sight t=x*sinh(u), and
integrating x Sigma using d[v E(1/v²)]/dv=K(1/v²).
The point-source excess spherical mass is [sqrt(1+4s²)-1]/2.
At finite e, Sigma_ex=F(arccos(x/e)|m)/(pi*v) for x<e,
zero outside. The finite cylindrical mass is total stock minus spherical
caps, integrated after s=x*cosh(u). For x>=e the full total ESD is exactly
(1+5.364*N)/(pi*x²). Tests compare this implementation with independent
direct-density LOS and spherical-shell quadrature.

The independent environmental real-space transform uses

    xi(r) = (2*pi²)^-1 int k² P(k) sinc(kr) dk,
    DeltaSigma(R)/rho = 4/R² int_0^R r² xi(r) dr
        -2 int_0^infinity xi(sqrt(R²+t²))
                  [R/(sqrt(R²+t²)+t)]² dt.

Combining the cylinder and surface terms before LOS integration makes
the tail decay faster and avoids a missing inner cylinder. For exclusion e,
the first integral begins at e when e<R and is zero otherwise; the second
begins at sqrt(e²-R²) when e>R. Substitution t=R*sinh(u) makes its weight
R*cosh(u)*exp(-2u). Dense finite-band power is transformed by DST-I,
xi interpolated on a uniform fine radial grid, and r²xi integrated by a
cubic spline antiderivative. This is checked against independent
Hankel rho/(2*pi) int k P(k) J2(kR) dk, with exactly the same band,
smoothing and physical-unit conversion. No sigma8 renormalization occurs.

For Plummer baryons b(s)=s³/(s²+u²)^(3/2), the same spherical law gives

    m_ex(s)=[sqrt(b(s)²+4*s²*b(s))-b(s)]/2,
    rho_ex = m_ex'(s)/(4*pi*s²).

The implemented analytic derivative is

    m_ex' = [(2*b*b'+8*s*b+4*s²*b')/(2*sqrt(b²+4*s²*b))-b']/2.

Solve m_ex(e)=5.364*N at every trial source mass and radius; the new edge
also excludes the environment. Project excess by the same shell geometry.
The exact Plummer baryon ESD is Mb*R²/[pi*(R²+rb²)²]. The four-size
diagnostic changes both baryons and excess, so it is reciprocal at the
level of this spherical acceleration law. It does not establish a common
covariant action, formation, energy budget or isolation-selected cross-power.
