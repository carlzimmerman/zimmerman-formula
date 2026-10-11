# What an orbit selector must produce

2026-10-11. Independent analytic route audit by `torque_selection_audit`, based on
`19d8c776494f0995d5b6b9330dd3ca5065025f5e`. The input
`sol61_push/cold_stream_selection_2026_10_10/REPORT.md` and research contract
were unchanged from that base when inspected. This file contains derivations,
not a completed formation simulation or a proof that cold energy exists.

## 1. The exponential hollow specifies more than tangential bias

Let `mu = G M_b`, `b = r_M`, and consider an exterior, baryon-dominated Kepler
annulus with

\[
\Phi(r)=-\mu/r+\Phi_0+o(1),\qquad r/b\ll1.
\]

The exact exponential target has

\[
M_c(r)=\frac{M_b}{e^{b/r}-1},\qquad
\rho_c(r)\sim\frac{M_b b}{4\pi}r^{-4}e^{-b/r}.
\]

Use a nonnegative spherical, stationary mass distribution function
`f(E,j)`, with specific energy `E` and angular-momentum magnitude `j`.
This is a reduction of the final population, not an assumption that its
nonspherical formation preserves these labels. The exact velocity integral is

\[
\rho(r)=\frac{4\pi}{r^2}\int dE\int_0^{j_{\max}}
\frac{j f(E,j)}{\sqrt{2[E-\Phi(r)]-j^2/r^2}}\,dj,
\quad j_{\max}^2=2r^2[E-\Phi(r)].
\tag{1}
\]

Assume a fixed bounded energy band and uniform small-`j` asymptotics within it.
If `f(E,j) ~ F(E) j^(2n)`, `n > -1`, then positivity and (1) give

\[
\rho(r)\sim
2\pi(2\mu)^{n+1/2}B(n+1,1/2)
\left[\int F(E)dE\right]r^{n-1/2}.
\tag{2}
\]

Thus any nonzero finite algebraic order in this class gives an algebraic
central density. Increasing a finite tangential-anisotropy exponent cannot
produce the stipulated exponential hollow in the asymptotic regime. A radial
delta-function population is outside (2); its nonzero bounded-energy traffic
instead gives the previously derived `r^(-3/2)` density.

Here is a constructive compatible asymptotic family:

\[
\boxed{f(E,j)\sim F(E)j^{-8}\exp[-K/j^2],\qquad K=2\mu b.}
\tag{3}
\]

Set `x=j^2` and `X=2r^2[E-Phi(r)]`. Equation (1) becomes

\[
\rho(r)=\frac{2\pi}{r}\int dE\int_0^X
\frac{f(E,\sqrt{x})}{\sqrt{X-x}}dx.
\]

The substitution `t=K(1/x-1/X)` yields the exact integral identity

\[
\int_0^X\frac{x^{-4}e^{-K/x}}{\sqrt{X-x}}dx
=\frac{e^{-K/X}}{\sqrt K\,X^3}
\int_0^\infty t^{-1/2}e^{-t}(1+Xt/K)^{5/2}dt.
\tag{4}
\]

Consequently the right side is
`sqrt(pi) X^(-3) K^(-1/2) exp(-K/X) [1+O(X/K)]`.
Since

\[
\frac KX=\frac b r-\frac{b(E-\Phi_0)}\mu+o(1),
\]

we obtain

\[
\boxed{\rho(r)\sim
\frac{\pi^{3/2}}{4\mu^3\sqrt K}\,r^{-4}e^{-b/r}
\int F(E)e^{b(E-\Phi_0)/\mu}dE.}
\tag{5}
\]

The target coefficient requires

\[
\int F(E)e^{b(E-\Phi_0)/\mu}dE
=\frac{M_b b\mu^3\sqrt K}{\pi^{5/2}}.
\tag{6}
\]

Equations (3)-(6) construct the required inner asymptotic, but choose both its
exponential scale and amplitude. They do not explain their selection or
guarantee a positive global self-consistent distribution for the full kernel.
Energy distributions without a uniform bounded band, nonspherical final
states, and correlated energy/angular-momentum singularities require separate
analysis. No uniqueness theorem for (3) is claimed.

For a finite baryonic source of radius `r_b`, this is an exterior-annulus
statement requiring `r_b << r << r_M`, not a theorem at the physical origin.
If no such annulus exists, the essential-zero conclusion cannot be imposed by
extrapolating the point-source kernel through the baryons.

## 2. The same condition in measured pericenter traffic

In a spherical potential, the phase-space measure for bound orbits is

\[
dM=8\pi^2jT_r(E,j)f(E,j)\,dj\,dE.
\]

Each orbit makes two crossings of every accessible radius per radial period,
so its unsigned crossing-rate measure is

\[
d\dot M_{\rm unsigned}=16\pi^2j f(E,j)\,dj\,dE.
\tag{7}
\]

Thus (3) is equivalently a per-`j` traffic density proportional to
`j^(-7) exp(-K/j^2)`. For pericenter `p`,

\[
j^2=2p^2[E-\Phi(p)]=2\mu p+2(E-\Phi_0)p^2+o(p^2).
\]

Combining (6) and (7), the target's required leading pericenter traffic is

\[
\boxed{\frac{d\dot M_{\rm unsigned}}{dp}
\sim M_b\sqrt{\frac{2\mu}{\pi}}b^{3/2}
p^{-4}e^{-b/p}.}
\tag{8}
\]

This includes the population's inbound and outbound crossings; it is not net
accretion or a fraction of an unspecified outer supply. It agrees with direct
Abel inversion of the inner Kepler residence kernel. A positive low-pericenter
tail cannot be cancelled by another orbit family.

## 3. A precise torque-to-diffusion test

For an explicitly assumed one-dimensional, orbit-averaged Markov model at
fixed `E`, let `N(E,x) dx` be orbital mass per `x=j^2`. In a Kepler potential
`N=4 pi^2 T_r(E) f`, because the radial period is independent of `j`. Define
the drift `a(x)=lim <Delta x>/Delta t` and variance rate
`D(x)=lim <(Delta x)^2>/Delta t` using the same time convention. The flux is

\[
J_x=aN-\tfrac12\partial_x(DN),\qquad \partial_tN=-\partial_xJ_x.
\]

For the exact candidate stationary, zero-flux population
`N=N_0 x^(-4) exp(-K/x)`,

\[
\boxed{\frac{2a-D'}D=\partial_x\log N
=\frac K{x^2}-\frac4x.}
\tag{9}
\]

Equation (9) is a directly measurable condition on an actual torque process.
For an asymptotic candidate multiplied by a remainder `R(x)`, its right side
also contains `R'(x)/R(x)`. Merely knowing `R(x) -> 1` does not control that
derivative; a derivative bound is needed to retain the displayed orders.
For example, with `D=d x`, the leading required outward drift is
`a ~ d K/(2x)`, followed by `-3d/2`. A regular diffusion with bounded drift
does not have that zero-flux asymptotic. Degenerate diffusion, coherent
resonances, energy-angular-momentum coupling, sustained nonzero flux and
physical removal can change this conclusion; they are not covered by the
one-dimensional closure.

In particular, diffusion in `L_z` along a Jacobi contour cannot simply be
substituted for diffusion in `j` at fixed `E`. An actual rotating-pattern
calculation must first measure the joint transport and decide whether (9) is
an admissible reduction.

Calling low-`j` orbits a loss cone does not empty them. A sink must specify
where their mass, energy and angular momentum go. Without such a sink or an
outward orbital bias, scattering can replenish core-crossing traffic.
Even with a physical loss process, rare large kicks can dominate deeply
depleted populations, as illustrated in the different stellar-capture system
studied by [Weissbein and Sari (2017)](https://arxiv.org/abs/1705.02603).
That paper is a warning to measure kick tails; it is not a transferred theorem
about this cold component.

## 4. A rotating gravitational pattern can lift pericenters, with a price

For a fixed-shape perturbation
`Phi_1(r,theta,phi-theta_p(t))`, with `Omega_p=dot(theta_p)`, Hamilton's
equations give

\[
\dot E=\partial_t\Phi_1=-\Omega_p\partial_\phi\Phi_1
=\Omega_p\dot L_z.
\tag{10}
\]

For constant `Omega_p`, `E_J=E-Omega_p L_z` is conserved; for a changing
pattern speed, `dot(E_J)=-dot(Omega_p)L_z`. A changing pattern amplitude or
spherical background adds explicit work terms. These standard identities are
also derived in section 2.1 of [Dillamore and Sanders (2025)](https://academic.oup.com/mnras/article/542/2/1331/8220894).

To see a constructive direction, take a weak perturbation and use the
instantaneous spherical background's osculating, noncircular pericenter.
Differentiation of `E=Phi_0(p)+j^2/(2p^2)` gives

\[
dp=\frac{dE-(j/p^2)dj}{\Phi_0'(p)-j^2/p^3}.
\tag{11}
\]

The denominator is negative at an inner turning point. For a planar prograde
orbit, `j=L_z`. The background energy is `E_bg=E-Phi_1`, so exactly
`dE_bg=Omega_p dj-dPhi_1` at constant pattern speed. Only for endpoint
comparisons with equal perturbing potential, or a justified secular average
that removes this term, does (10) give

\[
dp=\frac{(\Omega_p-\Omega_{\rm peri})dj}
{\Phi_0'(p)-j^2/p^3},\qquad \Omega_{\rm peri}=j/p^2.
\tag{12}
\]

Therefore a positive torque from a slower rotating pattern raises pericenter:
`dj>0` and `Omega_p<Omega_peri` imply `dp>0`. This is a viable gravitational
exchange direction, not an exclusion. It transfers energy as well as angular
momentum. The omitted `dPhi_1` is generally the same perturbative order as the
torque; weak amplitude alone does not justify dropping it. Instantaneous
pericenter motion requires this term in the numerator of (11). The sign
conclusion is conditional on the stated endpoint or averaging condition.

There are two immediate discriminators:

* A positive `Delta L_z` can initially **reduce** the angular-momentum magnitude
  of retrograde orbits, sending them further inward. Net spin gain alone is
  not evidence of low-`j` depletion. Measure magnitude, inclination and actual
  pericenter traffic.
* For positive constant `Omega_p`, a bound particle with initial `E_i<0`
  cannot gain `Delta L_z >= |E_i|/Omega_p` while remaining bound, when the
  potential is normalized to zero at infinity. Ejection must be counted.

For a planar spherical-background endpoint, a desired avoidance radius `r_*`
can be checked cheaply along the Jacobi line before integration:

\[
E_f=E_i+\Omega_p(j_f-j_i)<0,\qquad
j_f^2>2r_*^2[E_f-\Phi_0(r_*)].
\tag{13}
\]

Together with existence of the final bound orbit, this excludes a crossing at
`r_*`; one must select the outer accessible interval rather than an orbit
entirely inside `r_*`. It is a reachability condition, not a torque rate.

Transfer of baryonic angular momentum to soften a halo is an existing idea:
[Tonini, Lapi and Salucci (2006)](https://arxiv.org/abs/astro-ph/0603051)
constructed a perturbed distribution and compared its required transfer with
a dynamical-friction model. The present question is more specific: whether a
specified mechanism selects (8), including its scale, without imposing it.
No global novelty claim is made.

## 5. A cheap conservative experiment, and what it would establish

There is a cheap analytic control before evolving a whole population. For a
weak planar `m=2` perturbation integrated along a specified unperturbed radial
passage, linearity in the initial bar phase `phi_0` gives

\[
\Delta j_z=U\sin(2\phi_0)+V\cos(2\phi_0),\qquad
J_k=\sqrt{U^2+V^2}.
\]

The coefficients are torque integrals over that passage. For uniform incident
phase and `J_k>0`, the kick density is exactly

\[
P(\Delta j_z)=\frac1{\pi\sqrt{J_k^2-(\Delta j_z)^2}},
\quad |\Delta j_z|<J_k.
\tag{14}
\]

An initially radial packet therefore acquires
`<j_z^2>=J_k^2/2`, while retaining

\[
P(|j_z|<j_*)=\frac2\pi\arcsin(j_*/J_k)
\sim\frac{2j_*}{\pi J_k}.
\]

The mean angular-momentum magnitude grows, but the small-magnitude leakage
remains algebraic. This is a first-order, finite-passage control; the path must
be well defined through a finite baryonic source or over a declared exterior
interval. It does not describe later resonant phase correlations, multiple
passes, self-gravity or a biased incident phase distribution. It shows why the
selector test must measure the tail rather than just a mean torque.

After verifying the above asymptotics, the cheapest physical continuation is
a paired single-passage or few-passage scattering experiment through a
positive-mass rotating baryonic quadrupole. Specify its mass, size, inertia,
rotation and incoming population independently of the target. Include
reciprocal torque rather than holding its pattern speed fixed while silently
extracting unlimited work. A planar rotor prototype has Hamiltonian

\[
H=\frac{L_b^2}{2I_b}
+\sum_i\left[\frac{p_i^2}{2m_i}+m_i\Phi_0(r_i)
+m_i\Phi_1(r_i,\phi_i-\theta_b)\right].
\tag{15}
\]

This finite Hamiltonian conserves total energy and `L_b+sum L_zi`. The
fixed spherical background in this prototype does not supply a full
translationally invariant live galaxy; recoil, three-dimensional orientation
and self-gravity are subsequent obligations. The quadrupole should come from
a specified positive baryonic density, not a freely adjusted unphysical
potential.

Compare phase-matched prograde and retrograde packets, then two declared
orbital mixtures with equal total mass, energy and angular momentum. Measure
the full transition distribution in `(E,j,orientation)`, unsigned core
traffic, ejected mass, bar energy loss and return flux. Check the zero-bar
control and numerical conservation. The initial discriminator is whether
core-avoiding transitions dominate replenishment, particularly in the
retrograde/inclined population; a growing mean `j` is insufficient.

If this works, use its independently measured transition operator in an
orbit-population calculation with physical replenishment and test (8), rather
than fitting stationary orbit weights. This is a route to a selection test,
not a recommendation for a large simulation before checking the sign and
transfer budget. A finite annulus can be tested without claiming the
asymptotic essential zero has been observed numerically.

Finally, collisionless Hamiltonian evolution preserves fine-grained Vlasov
Casimirs `integral C(f) d^3x d^3v` when boundary flux vanishes. This prevents
claiming a universal fine-grained attractor from equal mass, energy and total
angular momentum alone. It **does not** forbid convergence of density or
other coarse observables through phase mixing. The proposed density test is
still meaningful; any claim to erase all orbital information would require
stronger evidence or specified open-system physics.

Neither the asymptotic construction nor the rotor introduces a vacuum
coupling. Even a successful orbit filter would leave abundance and the
`A-M_b-rho_DE` normalization, including `kappa=1/2`, to be selected by the
same completed dynamics.
