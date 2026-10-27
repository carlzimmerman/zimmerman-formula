# Physical completion: exact deductions and live hypotheses

## 1. Canonical matter kinetic energy fixes a companion force

Let the two mass-normalized matter amplitudes be

    Psi_T=sqrt(rho) sin(theta), Psi_F=sqrt(rho) cos(theta), theta=pi x/2.

With equal constituent masses and no flow phase, direct differentiation gives

    |grad Psi_T|^2+|grad Psi_F|^2
       = |grad sqrt(rho)|^2+rho |grad theta|^2.

Thus a canonical kinetic energy with physical coefficient Q=hbar^2/m^2 gives
both terms, not just the previously tested material stiffness. In the existing
units the mandatory companion is

    E_comp = kappa pi^2/8 integral r^2 rho x'^2 dr,
    mu_rho,comp = kappa pi^2 x'^2/8,
    c_x,comp = -kappa pi^2 div(rho grad x)/4.

The additional species potentials are
`mu_T=mu_rho+(1-q)c_x/(rho q_x)` and
`mu_F=mu_rho-q c_x/(rho q_x)`, with forces minus their radial derivatives.
All endpoint variations are computed directly from the energy. The finite-grid
arithmetic-density edge quadrature used in PC-2 approximates this continuum
identity; it is not the exact discrete two-spinor norm identity.

This canonical wave interpretation is a proposed completion. The stiffness
value was inferred from the earlier successful benchmark, not measured as a
particle mass. The standard scalar-wave quantum-pressure force is documented
in Hui et al., arXiv:1610.08297v2, Section II.2, equations22--26:
[Hui et al., Section II.2](https://arxiv.org/html/1610.08297v2#S2.SS2). Our two-amplitude identity above is
an internal algebraic derivation; that paper does not derive our phase-volume,
binding, response, F equation of state or interaction parameters.

## 2. A continuity obstruction to a matter-only interpretation

Claim: for B>0, `e(rho_T,rho_F)=B rho_T/(rho_T+rho_F)-epsilon rho_T`
on the punctured nonnegative quadrant has no continuous extension to the
vacuum point (0,0).

Proof: on the F axis `(rho_T,rho_F)=(0,t)` the limit as t->0 is0. On the T
axis `(t,0)` it is B. These disagree. In spinor coordinates the same argument
uses `(Psi_T,Psi_F)=(0,sqrt(t))` and `(sqrt(t),0)`, which both tend to zero.
Therefore no continuous local matter-only Hamiltonian density can exactly
produce this energy at vacuum. This is a statement about this interaction,
not a no-go theorem for other finite-radius mechanisms.

The positive volume term requires a carrier that can distinguish its phases
when particles are absent. Introduce an independent real/circular field x,
with q(x)=sin^2(pi x/2), vacuum potential V=B q(x), and a positive vacuum
kinetic energy. Coupling matter by `-epsilon rho q(x)` is a field-dependent
specific particle mass/energy. A positive alignment interaction can lock a
matter internal angle to pi x/2 in an adiabatic limit. These are explicit new
physical assumptions, not deductions from the galaxy law. The earlier model
already used x as an independent variational variable; this interpretation
makes the necessary physical carrier and its missing vacuum gradient explicit.

The simplest static vacuum gradient completion tested here is

    E_vac_grad=(ell_v^2/2) integral r^2 x'^2 dr, ell_v=.01 kpc/rM.

Its fixed-density phase force is `c_x=-ell_v^2 Delta x` and its explicit
fixed-q density derivative is zero. Its mixed species forces follow the same
conversion from (rho,x) derivatives. The original response-weighted stiffness
still participates; it is not replaced. PC-3 checks the prepared branch, not
just the isolated new term. The chosen ell_v is a feasibility input.

## 3. Correct physical coefficient scaling

Use physical mass density `rho_phys=rho_* rho`,
`rho_*=Mb/(4 pi rM^3)=a0/(4 pi G rM)`, and
`E_*=Mb a0 rM`, `rM=sqrt(G Mb/a0)`. Then

    epsilon_dimless = epsilon_phys/(a0 rM),
    B_dimless = 4 pi G B_phys/a0^2,
    kappa = Q/(a0 rM^3),
    K_dimless = K_phys rho_*^(2/3)/(a0 rM),
    ell_dimless = ell_phys/rM.

In particular, keeping the earlier 0.25 kpc material length fixed across
masses would NOT keep the physical canonical kinetic coefficient fixed.
Let lambda=rM/rM0. With common physical coefficients the correct changes are

    epsilon=.3/lambda, B=.001,
    kappa=kappa0/lambda^3,
    material_length=.25 kpc/sqrt(lambda),
    ell_phys=2.12132034 kpc,
    K=30/lambda^(5/3)  [same physical F entropy parameter].

For a separate virial-scaled thermodynamic state, K=30 is kept dimensionless.
That allows physical entropy to differ; it is not a universal coupling fit.
Baryonic templates in this discriminator are homologous with b=3 lambda kpc,
Mb=6e10 lambda^2 Msun. Law windows scale to[1.5 lambda,50 lambda] kpc. Fixed
dark mass ratio5.364 is an assumption of this test, not established for every
observed galaxy. Inherited fixed-physical-window report fields are not used
for cross-mass conclusions.

The response thin-wall coefficient A scales as lambda^-1 for fixed physical
ell. In the large-radius, fixed-enclosed-M approximation, the balance
`B R_dim^2 ~ 2 A M^2/R_dim^3` implies

    R_dim ~ lambda^(-1/5), R_phys ~ rM^(4/5) ~ Mb^(2/5).

That differs from strict homology R_phys proportional to rM. The thin-wall
approximation does not prove the scaling of the fully relaxed system, but it
identifies a genuine universality test rather than silently rescaling couplings.

## 4. Formation and energy accounting

A mass/phase energy minimum does not prove an accessible formation path or
account for its released energy. An all-F baseline must first be in material
balance on a domain large enough that its edge has negligible population.
A positive or negative phase-seed eigenvalue is meaningful only for that
specific baseline, not for an unrelated prepared T density.

PC-3 equilibrates all-F matter but its old664 kpc domain contains a large
edge population; it is a finite-box baseline, not an isolated free halo.
It has a negative phase eigenvalue and a small positive seed lowers its
energy. PC-3 then stops because a diagnostic assumed a boundary larger than
15 kpc. PC-4 fixes that reporting assumption but retains the finite-box
qualification. Neither result can establish unconstrained physical formation.
A larger-domain baseline is required and is pursued separately.

To radiate conversion energy rather than deposit it all in the small F
reservoir, the independent vacuum phase needs a specified time kinetic term,
not just a static potential. A positive Hamiltonian term `Pi^2/(2 I)` supplies
one possible dynamical completion and a scalar energy flux. Its inertia,
propagation, coupling and escape must be derived or tested; simply labeling
missing energy "radiation" is not an energy-conservation calculation. Those
obligations remain open until an explicit dynamical completion is checked.

## 5. Solve carrier and material state independently

PC-10 removes the infinite-locking assumption. Let x be the independent vacuum
carrier, y the matter spin angle coordinate, q_x=sin^2(pi x/2), q_y=sin^2(pi y/2),
and rho_T=rho q_y. In addition to gravity, response W and the F gas, use

    E_phase = integral r^2 [ beta C F(u) s(x)
               + (ell^2 F(u)+ell_v^2) x'^2/2 + B q_x ] dr,
    E_matter = integral r^2 [ kappa |grad sqrt(rho)|^2/2
                + kappa pi^2 rho y'^2/8 - epsilon rho q_y
                + J rho sin^2(pi(y-x)/2) ] dr.

The enclosed T field u is computed from q_y, not q_x. Every density, x and y
variation is retained in the 3n solve. At fixed rho and both angles, write
Xi_x for the phase barrier/response gradient derivative and Psi for the
nonlocal response density potential. The local equations are

    mu_rho = Phi + q_y Psi + (1-q_y)h_F - epsilon q_y
             + J sin^2(pi(y-x)/2) + mu_kappa + kappa pi^2 y'^2/8,
    c_y = rho q_y' (Psi-h_F-epsilon)
          + J rho pi sin(pi(y-x))/2 - kappa pi^2 div(rho grad y)/4,
    c_x = Xi_x + B q_x' - ell_v^2 Delta x
          - J rho pi sin(pi(y-x))/2.

Here q_y' in the conversion term denotes derivative with respect to y, whereas
y' in gradient energy denotes radial derivative. Species chemical potentials
are `mu_T=mu_rho+(1-q_y)c_y/(rho dq_y/dy)` and
`mu_F=mu_rho-q_y c_y/(rho dq_y/dy)`; use direct variations at endpoints.
Carrier force is minus c_x in its field equation, and material radial forces
are minus radial derivatives of the species potentials. This distinction is
necessary: the carrier is not merely a renamed particle fraction at vacuum.

For a general two-component coherent state the alignment energy is

    e_align = (J rho/2)[1 - cos(pi x) cos(pi y)
                          - sin(pi x) sin(pi y) cos(varphi)],

where varphi is the relative matter phase. It is the expectation of a Hermitian
2x2 internal-state Hamiltonian and preserves total particle number. The tested
static slice is varphi=0. Its omitted relative-phase quadratic coefficient is
nonnegative for x,y in[0,1], and common-flow gradient kinetic energy is positive.
This does not supply a collisional normal-component equation of state or a
full time-dependent formation calculation.

J=30 (J/epsilon=100) gives maximum law error0.70975%, R=56.343604 kpc and
maximum angle lag0.002642 rad. PC-16 gives a positive active radial Hessian,
relaxed stiffness4.11305e-4 Eunit/kpc^2 and returns after both +/-1 kpc
independent matter/carrier displacements. J=300 approaches the locked limit
with0.6195% error; J=3 gives1.584%. The coupling is still a phenomenological
physical input, not a derived constant.

## 6. A vacuum condensate can carry energy in a separate angular mode

A local candidate is a complex vacuum order parameter

    Sigma = f s exp(i chi),   s=1+x,
    L_vac = (f^2/2)[(partial s)^2+s^2(partial chi)^2] - V(s).

V and all direct matter couplings depend only on s. A smooth stabilizing
extension outside the occupied amplitude range is needed for a global field
theory; it has not been derived here. Locally around the F vacuum, the old
B sin^2(pi x/2) potential supplies a radial restoring mass. The angular field
chi has no mass potential and no direct particle-state or baryon coupling.
The old response-weighted radial-gradient terms remain and require their own
time-kinetic completion. Treating that inertia as Z/c^2 is an explicit added
assumption in the pulse experiment, not a deduction from static energy.

For one angular Fourier mode of wave number k, the canonical radial/angular
Hamiltonian, in normalized local variables, is

    H = p_s^2/2 + U(s) + p_chi^2/(2s^2) + s^2 k^2 chi^2/2.

It yields

    sdot=p_s,
    pdot_s=-U'(s)+p_chi^2/s^3-s k^2 chi^2,
    chidot=p_chi/s^2,  pdot_chi=-s^2 k^2 chi.

All these terms come from one positive polar-field kinetic energy. Adding a
passive escape term `-gamma p_chi` gives exactly

    dH/dt = -gamma p_chi^2/s^2,
    dE_escaped/dt = gamma p_chi^2/s^2 >=0.

A radial oscillation s=1+a cos(t) makes angular modes near k=1/2 unstable.
PC-17 integrates the monodromy independently, verifies its determinant, and
finds growth exponent0.10116 at a=.2 without leakage and0.09866 at gamma=.005.
The off-resonance k=1.5 case damps instead. PC-13 includes nonlinear backreaction
and closed-system/off-resonance controls. PC-20 extends the same passive escape
calculation, exceeding the derived outer-gas heat-capacity bound without an
external drive. Initial radial energy and a nonzero angular seed are supplied;
the actual collapse-to-radial-energy coupling is NOT thereby established.
PC-22 removes the harmonic approximation using the exact sinusoidal carrier
potential. A nonzero quantum/thermal seed and the physical escape rate still
need a spatial/dynamical derivation. A classical exactly constant chi would
remain constant without such a seed.

For outgoing radiation chi=f(t-r/c)/r, direct differentiation gives

    (partial_t chi)^2/c^2-(partial_r chi)^2
        = -2 f f'/(c r^3)-f^2/r^4.

The leading energy-flux term is proportional to1/r^2, but the source that acts
on the radial modulus starts at1/r^3. For a plane outgoing wave it vanishes
exactly. Thus phase radiation can transport energy with parametrically weaker
modulus forcing, rather than dragging particle conversion along with the
radiative phase. This is asymptotic transparency; finite spherical corrections
must be tested, not discarded.

PC-18/23 use the measured outer density and response field. With fast matter
spin held fixed, the carrier gradient coefficient is

    Z = ell_v^2 + ell^2 F(u),
    M_x^2 = 2 beta C F(u) + (pi^2/2)(B+J rho).

The linear radial response, assuming time inertia Z/c^2, is

    (Z/c^2) delta_x_tt - div(Z grad delta_x) + M_x^2 delta_x
        = ell_v^2 [(partial_t chi)^2/c^2-(partial_r chi)^2].

The packet is a prescribed leading-order angular wave. Source work, passive
absorption and carrier energy are tracked. This checks a necessary transport
component while freezing material degrees during the fast packet; it does not
prove full halo transparency or solve energy-conserving galaxy formation.
The initial two-grid peak changed26%, so those tiny peak values are not quoted
as continuum-accurate predictions. A further refinement is recorded separately.

## 7. Why the massive carrier alone is insufficient

For the illustrative vacuum kinetic length ell_v=.01 kpc, a canonical light-speed
carrier has vacuum decay length0.14235 kpc and quantum energy4.4923e-26 eV. The
binding energy per inferred constituent is4.2295e-30 eV. A transition with only
that binding energy cannot emit one such massive quantum: the ratio is10622.
Allowing such a single-particle emission would require a vacuum decay length
at least1512 kpc, incompatible with assuming a tightly localized carrier in this
simple completion. Collective processes are not ruled out. A massless angular
mode avoids this threshold, which motivates Section6 without proving a unique
microscopic interpretation.

The free-halo all-F baseline in PC-7 is material-equilibrated and clear of the
large domain edge. Its seeded energy relaxation, continued through PC-9/11/12,
reaches the independently prepared equilibrium within2.51e-7 kpc and4.93e-13
Eunit. It releases3.35523 Eunit=1.09287e52 J. These are accepted numerical
relaxations with fixed total mass, not a Hamiltonian time history. Accepted
endpoints do not certify monotonic energy on every interpolating trajectory.

The outer F gravitational escape-energy estimate is0.0765287 Eunit. This is
an upper bound on extra heat absorption because existing internal energy was
not subtracted. If all unexported energy goes there, at least97.7191% must
escape. The radial/angular prototype can export more than this. No calculation
yet couples that export self-consistently to the mass redistribution and local
conversion that released the energy.

## 8. Universality tests and prior exclusions

The naive common physical coefficients fail the homologous high-mass test:
19.02% law error at fixed entropy,8.642% with virial-scaled K, and depleted
transition structure. A reduced B/increased Q common family gives a filled
high-mass case but a6.712% low-mass error and a depleted middle-mass transition.
These are failures of the tested coefficients/closures, not a no-go theorem
for every possible interaction.

Existing real-data supply work is reused rather than rerun:
`rebuild_2026_10_22/ZT6_zstar_sparc_supply/FROZEN_CRITERIA.md` and its results
report28 of175 SPARC systems short under the5.364 no-loss supply, and none short
under the stated baryon-retention census. This uses the record's spherical
Mb=Vbar^2(Rlast)Rlast/G proxy and fixed0.5/0.7 stellar mass-to-light conventions.
It is not an independently derived baryon census or a universal dynamical proof.
PC-14/19 test that larger53.643 supply dynamically in our equilibrium energy;
merely increasing available mass produces a fragmented branch and poor law.
The mass budget alone does not fix the material/phase balance.

The old `campaign_fresh_gravity/CFG122_door4_superfluid` exclusions are also
retained. Its BK phonon force, temperature-slaved two-fluid EOS and DBI
comparisons already failed their declared force-shape, multi-mass, stability
or extra-parameter tests. Our angular mode is proposed only as an energy outlet,
with no direct baryon force; it is not a rebranding of those excluded MOND
phonon mechanisms. The constitutive response W and the F kinetic/thermodynamic
closure still need physical derivations. Keeping K dimensionless by a virial
prescription is a test policy, not a derivation from the galaxy law.

## 9. A targeted phase-purification continuation (PC-25--27)

The multi-mass failure motivates a specific alteration: increase the carrier
barrier, while keeping the leading response-wall tension ell*sqrt(beta) fixed.
This is one common choice for every mass, not a per-galaxy density fit. The
vacuum and material kinetic companions remain, so the *total* surface energy
is not assumed fixed. All variables and the boundary are still free.

A useful exact local stability criterion follows. Inside a uniform T domain,
x=y=1. Let c=pi^2/4 and hold rho fixed. The quadratic phase potential is

    [beta C F(u)-c B] delta_x^2
      + c rho(epsilon-Psi) delta_y^2
      + c J rho(delta_y-delta_x)^2.

All phase-gradient quadratic terms are positive. Thus a sufficient local
fixed-density phase stability condition is

    J+epsilon-Psi >0,
    beta C F(u) > c[B + rho J(Psi-epsilon)/(J+epsilon-Psi)].

This is a condition on a pure-phase background, not proof that the coupled
free-density system reaches that background or stays materially filled. It
shows exactly why increasing the barrier can remove residual F mixing that
spoils the bulk law. The Schur complement retains the finite matter/carrier
alignment rather than assuming equality of their angles.

At the *initial all-F* state both carrier and matter angles vanish and u=0.
The response barrier beta F(u)s(x) is sixth order in small phase amplitudes
because u is second order, F begins at u^2 and s begins at x^2. It contributes
no quadratic seed barrier. Increasing beta therefore need not eliminate the
previously derived dense all-F instability. Once a T response builds, the
same term creates a first-order barrier and can protect pure domains. This
self-induced barrier is distinct from imposing a radial conversion selector.

PC-25--27 use beta40 and ell_phys=0.67082039 kpc, with the original common
physical volume, binding, wave and vacuum coefficients and finite physical
alignment. Virial-scaled K is still an explicit thermodynamic test policy.
The wall mesh is refined adaptively around its current location; this changes
resolution only and does not impose a boundary radius. Multiple crossings,
depleted material or loss of force convergence remain failures of the target.
This route is a conjectured repair of the tested mixing problem until its
actual outcomes are interpreted; the criterion alone is not a solution.

## 10. Exact bulk obstruction for canonical stiffness (PC-28)

There is a construction-specific obstruction stronger than a parameter scan.
Assume a pure T region, no enclosed F source, constant carrier/internal states,
a spherical point baryon source, and no extra bulk force beyond canonical
material stiffness. Work on any open interval away from the source and any
interface. The original exact law fixes

    g0=(1+sqrt(1+4r^2))/(2r^2),  gb=1/r^2,
    M_T=(sqrt(1+4r^2)-1)/2,
    rho_T=2/[r sqrt(1+4r^2)].

Set a=sqrt(rho_T). Direct differentiation gives

    Delta a/a = -(1+24r^2)/[4r^2(1+4r^2)^2],
    mu_kappa' = -kappa(1+12r^2+192r^4)/[4r^3(1+4r^2)^3] <0.

But the material balance equation is `g-W'(u)+mu_kappa'=0`. The exact original
law makes its first two terms cancel, leaving the strictly nonzero expression
above for every r>0 and kappa>0. At r=1 it is exactly-41 kappa/100. Thus this
canonical completion cannot keep the *exact* original law on that pure-core
interval. Interface-localized forces or monopole boundary chemical constants
cannot cancel a spatially varying interior residual. This does not rule out
other bulk operators, mixed phases or observationally small corrections.

A formal first-order interior correction is

    delta g = mu_kappa'[rho_law]/[g0(2+g0)],
    delta g/g0 ~ -3 kappa/(8r^3)  for r>>1.

It is not a uniform expansion through a boundary layer. In the leading flat
bulk rho is proportional to1/r^2, whose square-root is harmonic, so canonical
stiffness becomes small there. The large residuals in purified high-mass trials
occur in the transition/material boundary layer, even when the core phases are
pure. The physical length `(Q/a0)^(1/3)` is0.839 kpc for the inferred coefficient;
it is a dimensional scale, not a general prediction of core radius for every
baryonic profile. PC-28 verifies the displayed identities symbolically.

This identifies a genuine limitation: another localized interface force cannot
make this *particular canonical bulk theory* exactly obey the original law.
A proposed correction must derive a changed bulk constitutive/kinetic law or
accept and test the resulting controlled departures. Adding a penalty that
vanishes on a desired law profile would not be a physical derivation.

## 11. Static data do not identify a unique dynamical completion

For any positive inertia operator I, `H=E_static+Pi^T I^-1 Pi/2` has the same
Pi=0 stationary configurations, while linear frequencies depend on I. Also
adding an angular kinetic energy with an x-independent coefficient gives no
radial/angular exchange, whereas the polar coefficient s(x)^2 in Section6
does. Both additions vanish at chi=constant, Pi_chi=0 and leave the same static
branch. Consequently a static law/force-balance success alone cannot determine
the physical radiation channel, its inertia or rate. A full microscopic or
symmetry-based dynamical action is additional input. This is nonidentifiability
of this inference, not a proof that a physical completion cannot exist.
