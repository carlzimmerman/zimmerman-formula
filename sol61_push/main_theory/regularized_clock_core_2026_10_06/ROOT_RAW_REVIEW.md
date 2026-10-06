# Root raw review of the detuned conserved core

Reviewed the actual radial action, source definitions, core.py and recorded core_200k_b output rather than taking completion status as evidence of a source match. The positive result is a finite same-state source/vacuum integration in the changed epsilon=.01 action. It is not a normalized cosmological boundary-value solution, stability proof or coefficient selector.

## Independent initialization derivation

The report initially leaves its higher center initialization coefficients uncertified. They can be independently recovered from the displayed exact stationary equations. Set M=N0=H=1 and positive n2, expand `N=1+n2 r^2+n3 r^3`, `B=1+b2 r^2+b3 r^3`, `V=xr+y2 r^2`, and `Q=(1-epsilon)a^2-2a^3/(3A)+O(a^5)`. The conserved constant-density fluid has no linear r correction to its proper pressure, so it contributes no order-r^3 term to lapse/radial Euler densities.

The radial Euler order-r^3 coefficient is `2b3-6n3+8xy2=0`, hence `b3=3n3-4xy2`. The acceleration derivative has expansion

`Q_signedprime=4(1-epsilon)n2 r+[6(1-epsilon)n3-8n2^2/A]r^2+O(r^3)`.

The lapse coefficient at order r^3 is therefore

`8b3+8xy2+8eta y2-24(1-epsilon)n3+32n2^2/A=0`.

Substitution gives exactly the first initialization equation, `3epsilon n3+(eta-3x)y2=-4n2^2/A`. Finally the stripped sourced momentum equation at order r^3 gives

`3x(b3+n3)+2 C y2+3eta n3=0`, `C=b2+n2-(rho0+p0)/4`,

and hence `3(4x+eta)n3+(-12x^2+2C)y2=0`. Both equations and the b3 formula agree with core.py. These are independent analytical coefficient checks; they do not certify the numerical remainder at its finite starting radius or convergence of a complete series. The |a|^3 response permits such radial higher terms and need not be analytic as a Cartesian field to every order.

## Physical force and matching bookkeeping

For q^2=B^2 r^2 w^2 and t=lnr, the exact Killing force used for the interior is

`[k(1-q^2)-q^2(dlnB/dt+1+dlnw/dt)]/[r B sqrt(1-q^2)]`.

It follows directly from `F'=2N^2[k(1-q^2)-q^2(dlnB/dt+1+dlnw/dt)]/r` and `g_phys=F'/(2NB sqrtF)`. The code implements this expression, rather than assuming physical force equals clock acceleration. Its pressure is the exact conserved-fluid identity `(rho0+p0)/sqrtF-rho0` for N0=1. The event sets proper pressure to zero; it then passes the same four field values to the vacuum integrator and does not prescribe an independent mass or clock charge. A finite density jump at zero pressure changes field derivatives but introduces no pressure surface shell in this stationary second-order system. Smooth-source matching remains a separate test.

The exterior's named weak_massflux and MOND_ratio use a leading weak metric force, not a second exact mass theorem or observational fit. Their report labels this approximation correctly. The two tolerances, phase caps and finite sampled sign/force checks support a bounded constructive result. They do not certify every point, measure G_N, or establish the full perturbation matrix.

## Remaining boundary and health obligations

The central normalization is fixed to1, while outer N is not imposed to1. A finite endpoint at .342 of r_cos is insufficient for a cosmological asymptotic claim. The formal high-clock negative-kinetic sector lies outside the sampled low-clock segment; positive sampled Qaa cannot prove absence of other dynamical instabilities. Epsilon and A/H remain free inputs. A new source-generated outer shooting investigation is required with its own frozen inputs and evidence.
