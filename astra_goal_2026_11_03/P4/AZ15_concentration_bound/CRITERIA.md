# AZ15 — non-spherical concentration bound for AZ14

κ = ½ FITTED; not theory closed

Pre-result. ls P4, git log through 7cbe46d34c, rg ellipsoid/anisotropic/Gaussian in AZ14 and ellipsoid-gradient in rebuild criteria checked. AZ14 explicitly leaves arbitrary concentration open. No AZ15 existed. Same positive functional and unspecified FITTED lambda, no extra physical coefficient or new particle. Analytic continuation, not a physical parameter scan.

Let psi=rho^(1/4), M=integral psi^4, J=integral |grad psi|^4, F=256 lambda J. For smooth nonnegative psi with finite M,J and decaying boundary, derive directly by averaging line integrals over a ball:
|psi(x)| <= (3M/(4pi R^3))^(1/4) + 3^(3/4)(4pi)^(-1/4) R^(1/4) J^(1/4).
Choose R=(M/J)^(1/4), not by fitting. Thus rho_max<=C^4 M^(1/4)J^(3/4), C=(3^(1/4)+3^(3/4))/(4pi)^(1/4). Split Newton potential into near/far radii and optimize the bound algebraically to obtain |W|<=K G M^(7/4)(F/lambda)^(1/4), K=3/16*(3^(1/4)+3^(3/4))^(4/3). This is a sufficient non-sharp bound, not an equality or empirical fit. It implies fixed-mass finite-energy configurations cannot have F or rho_max diverge. State all smoothness, isolation, energy conservation, and positive-lambda hypotheses; no claim of global PDE existence or no finite contraction.

Also derive exact affine-Gaussian F=lambda M[(sum Ri^-2)^2+2sum Ri^-4] and W=-GM²/(4sqrt(pi))*integral_0^infty ds/prod(s+Ri²)^(1/2). With rmin=min Ri, F>=3lambda M/rmin^4 and |W|<=GM²/(2sqrt(pi)rmin). These certify no zero-axis finite-energy limit inside that family. They are not a dynamical galaxy simulation.

Structural PASS requires valid derivations of both global energy and affine bounds plus controls. Empirical rows remain NOT EVALUABLE, both footings identical since a0 absent. Known answers: sphere Ri=1 gives F=15lambda M and W=-GM²/(2sqrt(pi)), relative tolerance 1e-10. Independent 3-node Gaussian product quadrature for Ri=(1,2,3), G=M=lambda=1 verifies F formula to 1e-12 and quadrature binding respects bound. Gaussian J=15/256 and rho_max=(2pi)^(-3/2) obey derived global inequalities, margins recorded. Integrable Holder-kernel norm checked by weighted radial quadrature to relative 1e-10. MUTATE reverse lambda sign: Gaussian compression U=-15/R^4-B/R unbounded below and negative curvature, destroys barrier. MUTATE omit psi density transformation factor 256: independent Gaussian F/J oracle differs by >100. No changed physical coefficients. Failed derivation/control -> NO VERDICT. results.json predeclared; quadrature only, no heavy job.
