# Exact warm kinetic realization of the algebraic law, with a boundary obstruction

A positive anisotropic collisionless distribution reproduces the full zero-stiffness identified-medium algebraic-law density, despite nonzero velocity dispersion. Its stress divergence vanishes because radial and tangential stresses balance. Thus the previous isotropic pressure tradeoff is not a universal obstruction to warm equilibria.

However, this exact construction has infinite mass, nonzero inward/outward streaming, and nonvanishing surface stress. It is not an isolated finite halo, a stable attractor, or a derived formation/selection mechanism. It provides an explicit kinetic target for a finite-boundary construction and exposes what that construction must supply.

## Native law and density

Work in the identified-medium branch of CFG939, with a point baryonic mass, gamma=0, negligible background density, and K=4piG. Define rM²=GMb/a0, a=rM/2, and C=a0 rM/K. The law is

    u²/(a0-u)=GMb/r²,
    u=2a0/[1+sqrt(1+4r²/rM²)].

With P=u/K radially outward and divP=rho, direct differentiation gives the full profile

    rho(r)=C/[r sqrt(r²+a²)].

This is not merely a deep-acceleration approximation. On the law, the medium's effective acceleration -gNb+R(u) is zero. Therefore its collisionless characteristics are straight lines at constant velocity in this formal branch. Ordinary baryons do not follow this zero-force medium equation.

## A positive stationary distribution

For any chosen speed v0>0 let b=|r cross v|/v0 be the impact parameter on the support v=v0. Define the velocity-space mass distribution

    f(r,v)=C a/[2pi² v0² b(b²+a²)] delta(|v|-v0).

It is nonnegative and depends only on constants of the force-free trajectories. It therefore solves the stationary collisionless equation away from the point centre in the distributional sense. The b=0 singularity is integrable in velocity solid angle for every r>0; it does not define a smooth phase-space density. The spatial density has a1/r central cusp, appropriate to this point-source gamma=0 limit. It must not be confused with the finite-stiffness central regularization calculated earlier.

The density integral reduces to

    rho=4pi v0²/r integral_0^r b F(b)/sqrt(r²-b²) db,
    F(b)=C a/[2pi² v0² b(b²+a²)].

Using b=r sin(theta) gives exactly C/[r sqrt(r²+a²)]. Thus this is an explicit positive distribution, not only a formal solution of the Jeans moment equation. It was constructed from the target density; its formation is not derived.

Let S=sqrt(r²+a²). The mean velocity is zero by symmetry, while

    sigma_r²=v0² S/(S+a),
    sigma_t,total²=v0² a/(S+a),
    beta_anisotropy=1-sigma_t,total²/(2 sigma_r²)
                   =1-a/(2S).

Here beta_anisotropy is the conventional velocity anisotropy, not A33's gravitational kinetic parameter beta. It increases from1/2 near the centre to1 at large radius. The total mean-square speed is v0².

These moments obey exactly

    d(rho sigma_r²)/dr
      +rho(2sigma_r²-sigma_t,total²)/r=0.

The isotropic constant-dispersion pressure term in MEDIUM_INERTIA_RESULT.md omitted this anisotropic cancellation by assumption. Its scoped result remains valid, but cannot be extended to all distributions.

The speed v0 is arbitrary. Positive normalized mixtures of these monoenergetic distributions retain the same density and replace v0² by its mixture average in the stresses. Hence even this equilibrium family does not select a temperature, dispersion, kinetic history or unique distribution.

## The finite-halo limitation is essential

The enclosed cold mass is

    M(<r)=4pi C [sqrt(r²+a²)-a],

which grows linearly at large radius. Inward and outward particles balance in net current, but each population crosses every large sphere. This formal all-space equilibrium is not a finite isolated object.

For a stationary zero-force system, integrating div Pi=0 against position gives the virial boundary identity. In this example,

    4pi r³ Pi_rr(r)=v0² M(<r).

Both sides grow linearly; the boundary stress cannot be discarded. More generally, a finite stationary zero-force system with vanishing virial surface term has integral Tr(Pi)dV=0, forcing zero kinetic energy for a nonnegative distribution. Thus a warm finite realization must have a confining force in a transition region, a surface stress/particle supply, or time dependence. Simply cutting this density off creates an unbalanced boundary and is not a solution.

An effective-potential rise outside a flat interior could in principle turn bound trajectories around, as the earlier CFG939 discussion of a finite basin suggests. But that potential must be generated self-consistently by the same field and matter equations; no reflecting wall or arbitrary cutoff was added here. Finite gamma, extended baryons, cosmological matching and nonspherical perturbations also require new calculations.

## What is new in this checkpoint and what is not

The useful result is the explicit positive impact-parameter distribution and its stress balance for the native full law, together with its boundary limitation. It provides a counterexample to any unqualified assertion that nonzero dispersion necessarily changes that law in the identified branch. This construction is not claimed to be globally novel; inverse distribution-function methods and anisotropic equilibria are established methods.

No stability calculation has been done. In particular, a highly radial distribution cannot be declared stable merely because its Jeans equation is satisfied. No phase-mixing rate, occupation probability or formation basin has been derived. Shell crossing still does not generate the free S4 population under the unchanged identity, as CFG939 already establishes.

The next substantive target is a self-consistent finite transition and a positive bound distribution on it, followed by stability and formation tests. The calculation leaves kappa, the cold sourcing fraction and observational viability open.

## Verification

anisotropic_run/manifest.json validates; ten checks pass. These cover the native law/density, moment relations, anisotropic Jeans balance, quadrature at five radii, positivity, enclosed mass, infinite-mass asymptotic and virial boundary identity. Direct quadrature agrees with the analytic moments to better than2.2e-14 relative for the tested a=0.5,C=v0=1. Removing tangential stress fails Jeans balance, total-speed and anisotropy checks (seven of ten pass), as intended. The boundary check was added after construction and is disclosed in ANISOTROPIC_CONTRACT.md. Mathematical interpretation is self-reviewed, not independently certified.
