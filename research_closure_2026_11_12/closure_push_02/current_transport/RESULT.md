# CP02 current transport: derived, closed at leading NR order, and executed

**The gated clock has an explicit conserved current and a closed leading
Newtonian evolution system. Its global charge normalization remains an initial
condition. A regular stationary positive-charge configuration cannot evade the
static equations by adding an irrotational closed clock flow.** These are
concrete results for the specified action, not a declaration of theory closure.

The full derivation and scope conditions are in[DERIVATION.md](DERIVATION.md).
Observed HEAD was `2207a1df48348f01ca1084d4add5d214c55d0e7e`. Only this new
`current_transport` directory was edited; originals are preserved and hashed.

## Exact current

For `H(Q,Pi)=F(Q)S(Pi/Pic)`, define

    B=1+Gamma'(Pi)-H_Pi,    b=B/Q,
    rho_Q=H_Q+div(BP)/Q.

Direct variation of the constrained QX17 action gives

    div J=0,      J^mu=rho_Q n^mu-lambda P^mu/Q,
    Q D_mu b=W_P,mu,      lambda=Q n.partial b.

Hence `J=rho_Q n-P(n.partial b)`. Pure transport along the clock flow is exact
only if `P(n.partial b)=0`. The gate changes the current in two places:
`H_Q=F'S` and the `-H_Pi` contribution inside B.

The direct unconstrained jet variation was evaluated after imposing tangent
test fields in flat1+1 on three nontrivial configurations. Clock residuals are
at most7.53e-37; polarization residuals at most1.51e-36. Three omission mutants
fail on every witness, with errors .0092–.0106 (gate-Pi), .0072–.248 (leaf flux),
and .0665–.0833 (ungated H_Q). The general identity is derived analytically;
these finite jet checks are adversarial confirmation, not a dimensional proof.

## Closed leading evolution and actual dynamical test

Under the explicit regular Newtonian ordering in DERIVATION section2,
`x=Q-1=dot(sigma)-Phi-|grad(sigma)|^2/2`, `v=-grad(sigma)`, and

    n=H_Q+Pi,                     Pi=divP,
    dot n+div(nv)=0,
    dot v+(v.grad)v=-grad(Phi+x),
    Delta Phi=K(rho_b+n),
    grad[x+H_Pi-Gamma']+W_P=0.

For `F=Cx^2`, `x=(n-Pi)/(2C S)`. The polarization constraint is solved from
the stationary internal energy

    e=(n-Pi)^2/(4C S)+W+Gamma.

This closes evolution given initial charge/velocity, sources, and boundary
conditions on a regular elliptic branch. It does not advect bare rho_d by
assumption. Positive n is preserved by smooth transport; Pi may be signed.
The exact polarization drift is one Newtonian order higher **only when**
`H_Pi,Gamma'=O(v^2)` with controlled derivatives. The approximation is not
uniform in arbitrarily small Pic or singular gate derivatives.

The executable benchmark uses the actual QX17 convex W and a nonconstant gate
`S=exp(-Pi/10)`, C=500, K=.01, a0=.1, gamma=0 in dimensionless units. It solves
the nonlinear polarization constraint at every RK4 stage and evolves a smooth
nonuniform density and velocity. Periodic Poisson subtracts the mean charge:
this prescribed compatibility background is the usual periodic/Jeans
subtraction, not an on-shell static homogeneous cosmology. The tested finite
wavenumber range is not a UV-health theorem for this gate.

| Check | Accepted result |
|---|---:|
| N=64 nonlinear maximum density change | .05840208 |
| global charge absolute drift | 1.78e-15 |
| nonlinear polarization residual | 1.77e-13 |
| moving-boundary charge ledger error | 3.11e-15 |
| error when boundary motion is omitted | .12614249 |
| N=32/64 density difference on common grid/times | 1.6423e-8 |
| maximum clock offset / potential | .001116 / .001075 |
| maximum absolute H_Pi | 6.211e-5 |
| largest K|P|/a0 | .001168 |

Numerical conservation to roundoff is conservation of the **leading** equations;
it does not remove the higher-order physical error in that reduction. Each
production computation took less than.5s; every runner capped CPU at55s and
wall time at60s. Raw density, velocity, charge, energy and flux-ledger
trajectories are retained.

The linear response was independently derived from the Hamiltonian Hessian.
With `A=H_QQ`, `b=H_QPi`, `D=H_PiPi-Gamma''`, `c=1+b`, `w=W_PP`,

    omega^2=n0[k^2(w-Dk^2)/(Aw+(c^2-AD)k^2)-K].

For the ungated QX17 P=0 branch this reduces to
`omega^2=-n0 A K^2/(AK+k^2)`. The gated benchmark's k=1 growth rate is
**.0952626122560 per dimensionless time unit**. The actual nonlinear integrator
reproduces its small-amplitude growing solution to8.50e-12 relative amplitude
error. This checks the coupled charge, polarization and gravitational dynamics,
not merely a conservation bookkeeping identity.

## What crosses an EFE aperture, and what is selected

At leading order a spherical moving aperture obeys

    M_dot=4pi R^2 n(R)[R_dot-v_r(R)].

The exact equation uses the density and drift flux of the covariant current.
If `R=R_E=sqrt(GM_b/a0)/x_e`, then
`R_dot/R=.5 M_b_dot/M_b-.5 a0_dot/a0-x_e_dot/x_e`.
Demanding `M=M_b(F_A(x_e)-1)` imposes the concrete flux condition

    4pi R_E^2 n(R_E)(R_E_dot-v_r)
       = M_b_dot(F_A-1)+M_b F_A' x_e_dot.

A static mass enhancement supplies neither n(R_E) nor v_r(R_E). The transport
system can calculate them from initial and boundary data; the identity itself
does not set them to the desired capacity. In the executed benchmark the moving
interval charge changes2.2338560782 ->2.3931917639 while total charge stays2pi.
Both boundary sweep and material transport are included and independently checked.

Global normalization has an exact answer. Homogeneous FRW gives
`a^3 H_Q(Q,0)=I`, hence `Q=1+I/[2C S(0)a^3]`. **I is a free conserved initial
charge for fixed action coefficients.** The gate supplies no source or
relaxation selecting it. The mean-charge1 and1.3 numerical examples retain
their distinct totals2pi and2.6pi, illustrating this fact; because their
periodic compatibility backgrounds differ, the analytical FRW family is the
proof, not that numerical comparison. This does not exclude conditional local
capacities after a cosmological inventory and assembly history are specified.

## Stationary flowing-clock workaround

For stationary leading NR transport with n>0, single-valued sigma, and no normal
boundary charge flux, multiplying `div(n grad sigma)=0` by sigma gives
`integral n|grad sigma|^2=0`. Therefore v=0. On an infinite domain the weighted
boundary term must vanish; total net flux zero alone is insufficient.

There is also an exact spherical result. For a static metric and stationary
clock `tau=t+psi(r)`,

    J^r=n^r[H_Q+(B/Q)Pi].

A regular origin sets the conserved radial flux to zero. Any **nonzero**
coefficient therefore forces n^r=0. A negative nonzero coefficient does not
evade this conclusion. A smooth nonzero clock flow with zero current requires
the coefficient to vanish on an open flowing region, or a change to the
regularity, boundary-flux, or stationarity assumptions. Positive rho_Q alone
does not prove positive coefficient; that distinction is retained explicitly.

Thus the simple regular closed stationary flow does not rescue a failed static
halo branch. Time dependence, open accretion/central flux, singular or
post-caustic behavior, and a zero-coefficient branch remain distinct problems;
none is established as a successful halo by this calculation.

## Evidence and reproduction

- exact_run: five exact-current/polarization and mutation checks, completed.
- nr32, nr64, charge_family, linear32: four bounded evolution runs, completed.
- symbolic_run: fourteen exact derivative/Hessian/mutation and cross-run checks,
  completed.
- static_flux_run: eight exact factor/energy-identity/scope checks, completed.

All seven v2 manifests validate against their current inputs. Commands, software
versions, observed source hashes and output hashes are retained in the manifests,
[run_commands.txt](run_commands.txt),[sources.json](sources.json),
[verification.json](verification.json), and[artifact_hashes.json](artifact_hashes.json).
Use fresh output directories to reproduce; frozen source files were not changed.

**Assessment:** exact current derived and adversarially checked; leading
Newtonian closure derived and nontrivially executed within its stated scaling;
global charge nonselection established; simplest regular stationary-flow
workaround excluded under explicit hypotheses. Full relativistic health,
time-dependent environmental halo formation, and the observed normalization
are not certified by these results.
