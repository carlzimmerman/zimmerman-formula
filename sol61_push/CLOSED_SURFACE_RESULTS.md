# Finite curvature supplies a crossover, not a coefficient

This tests a possible physical connection of the surface response to a cosmological length. It does not identify a horizon with material mode support. The model is an untwisted free spin Dirac field on a round sphere, zero temperature and cone neutrality, with a uniform anticommuting internal mass m=yP. A local surface differential operator does not by itself supply a bulk action or vacuum stress.

The primary spectrum input is Abrikosov, [Dirac operator on the Riemann sphere, hep-th/0212134v1](https://arxiv.org/html/hep-th/0212134), Sections 2.1-2.2, equations 24 and 37. On a unit sphere eigenvalues are nonzero integers of either sign, with angular momentum l=|lambda|-1/2. Hence multiplicity per sign is 2|lambda|. Restoring radius R and speed v gives kinetic energies +/-vn/R, n>=1. The intrinsic chirality anticommutes with the spin Dirac operator; a constant chirality times internal mass therefore gives energies +/-sqrt(v^2 n^2/R^2+m^2). No magnetic flux, twist, boundary, or zero-mode sector is included.

## Convergent response with explicit matching

Let nu count Dirac species, equal to the positive-band degeneracy used in the plane calculation. Per area 4pi R^2, subtract the m=0 vacuum energy and the entire quadratic term mode by mode. Then

rho_sub(m)=nu v F(x)/(2pi R^3), x=|m|R/v,

F(x)=sum_{n=1}^infinity [n^2+x^2/2-n sqrt(n^2+x^2)]

    =sum_{n=1}^infinity x^4/[2(sqrt(n^2+x^2)+n)^2].

The second expression is positive and avoids numerical cancellation. This prescription does not determine the finite quadratic counterterm or the absolute vacuum energy; both remain matching inputs.

For |x|<1 the expansion is uniformly summable on compact subintervals, since each n has its nearest square-root singularity at |x|=n and the subtracted terms are bounded by a convergent n^-2 majorant. Thus

F(x)=pi^2 x^4/48 - pi^4 x^6/1440 + O(x^8),

rho_sub(m)=nu pi m^4 R/(96v^3)+O(m^6 R^3/v^5).

There is no cubic at fixed finite R as m tends to zero. The curvature gap is v/R. For x tending to infinity, write each summand as x^2 h(n/x), h(t)=1/[2(sqrt(t^2+1)+t)^2]. The integrable continuous positive decreasing function h has integral 1/3 (substitute t=sinh u). Its Riemann sums give F(x)/x^3 -> 1/3, and recover rho_sub -> nu|m|^3/(6pi v^2). The large-radius and small-mass limits therefore do not commute in the normalized cubic response.

The constitutive consequence is conditional: with the same assumed critical gravitational matching and sheet density as before, the quartic produces b proportional to P^3 rather than P^2 below the crossover P_cross=v/(yR). This is a uniform-response conclusion, not a solved nonuniform galaxy profile. It shows why the infinite-plane deep-field law cannot simply be asserted on finite closed support.

## Bounds and evidence

Taylor inequalities for sqrt(1+u), u>=0, give

x^4/(8n^2)-x^6/(16n^4) <= summand <= x^4/(8n^2).

After N terms, add the leading tail x^4 sum_{n>N} n^-2/8. The result is an upper estimate; its truncation error is at most x^6/(48N^3). The bound excludes floating arithmetic error, which is separate. The run uses N=30000 and x={0.01,0.1,1,10,100,300}. At x=100 the response/planar ratio is about 0.992525; at x=300 it is about 0.997503. Fifteen checks pass, including exact identities, quartic coefficients, the continuum integral and an independent truncated direct sum. These finite checks support the implementation; the expansion and Riemann-sum arguments supply the limit statements.

## Relation to the two radius hypotheses

If R is independently established to be the de Sitter horizon sqrt(3/Lambda), the curvature gap sets P_cross=(v/y)sqrt(Lambda/3). It still depends on the free v/y. Using the desired 32pi relation only as a hypothesis gives P_cross/a0=(v/y)sqrt(32pi/3). This comparison tests whether the proposed cubic regime could exist; it does not derive a0.

If instead R is the density length sqrt(8pi/Lambda), the same conditional comparison gives P_cross/a0=2v/y. The density length is not the geometric de Sitter horizon, as established in HORIZON_8PI_AUDIT.md. A very slow mode can move this finite-size crossover below a chosen observational window, but that does not select the speed, density, coupling or coefficient. The horizon-to-material-support identification remains a new physical assumption requiring dynamics.

SciSpace discovery returned Fischetti, Wallis and Wiseman's 2020 work on Dirac free energies and deformed spheres. Its abstract is not used for these derivations; only the checked primary spectrum above is a source dependency. No full covariant vacuum stress, inhomogeneous polarization determinant, interaction stability, observation fit or 32pi solution is established. The next viable common-scale route must explain the physical support and state while selecting the matching and vacuum sector, rather than treating a radius substitution as their derivation.
