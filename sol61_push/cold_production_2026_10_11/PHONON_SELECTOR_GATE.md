# Gate for reusing the protected carrier as a phonon force mediator

## Decision

The protected detuned carrier does not directly supply a MOND-like phonon
force. Its coherent low-density phase action is quadratic in the chemical
potential variable, its illustrative halo is not an equilibrium condensate
under the ideal-gas screen, and the usual linear baryon-phase source would
break the charge conservation used in the coldness proof. These are gates
on this proposed reuse, not a general exclusion of superfluid dark matter.

## Primary-source comparison

Berezhiani and Khoury's [Theory of Dark Matter Superfluidity, v2](https://arxiv.org/html/1507.01019v2),
section 1.3, equations (4)-(6), uses a phase action P(X), postulates an
X sqrt(|X|) form, and introduces a coupling proportional to theta rho_b.
The paper explicitly describes that coupling as breaking the global U(1).
These ingredients are different from the positive quartic carrier here;
the paper does not derive them from our action or establish our vacuum
normalization. Search scope: this primary paper and its companion abstract/
PDF were located; the cited equations were read in the v2 HTML. No broad
literature-completeness or novelty claim is made.

The following carrier derivation and compatibility tests are independent
calculations for the repo's candidate.

## Coherent saddle derived from the same NR Hamiltonian

For constant daughter density n and a real source amplitude b at their
energy-minimizing relative phase, introduce chemical potential mu conjugate
to Q. The grand-potential density is

    Omega = (delta-2mu)b^2 + 2c b n + k n^2 - mu n.

For delta-2mu>0, minimization over b gives

    b=-c n/(delta-2mu),
    Omega=k_eff(mu)n^2-mu n,
    k_eff(mu)=k-c^2/(delta-2mu).

On the dilute coherent branch with 0<mu<delta(1-r^2)/2 and r^2=c^2/(delta k),
k_eff>0. Hence

    n=mu/[2k_eff(mu)], P(mu)=mu^2/[4k_eff(mu)].

Differentiation includes the source population:

    dP/dmu=n+2b^2.

Thus the source cannot be dropped when relating the pressure derivative
to conserved charge. At mu much smaller than delta,

    P(mu)=mu^2/[4(k-c^2/delta)] + higher powers of mu/delta.

At leading order in the low-gradient, common-phase expansion this becomes
P(X) proportional to X^2 on X>0. Common-phase Galilean kinematics use source
mass 2m at this order; corrections of order delta/m and derivative/gap
ratios are not being used to infer a new branch. With positive effective
quartic and the density constraint n>=0, maximizing nX-k_eff(0)n^2 gives
P=0 for X<=0. Continuing X^2 to negative X would give a negative density
P_X, not a physical condensate of this Hamiltonian.

For orientation only, a formal gradient-dominated P(X) proportional to
|X|^nu coupled linearly to baryons would have radial flux proportional to
r^2 |theta'|^(2nu-1). Outside a spherical baryonic source this implies
|theta'| proportional to M_b^[1/(2nu-1)] r^[-2/(2nu-1)]. A 1/r force requires
nu=3/2, not 2. The actual positive-density branch above does not even
justify the negative-X continuation needed for that formal comparison.
A sextic term, alternative phase or extra field would change the model
and would require a new stability and protection analysis.

## Condensation screen for the detuned halo benchmark

Assume, only for this screen, a single thermal daughter population with
rho=1e-21 kg/m^3 and one-dimensional velocity dispersion sigma=200 km/s.
With k_B T=m sigma^2,

    lambda_T=sqrt(2 pi) hbar/(m sigma),
    degeneracy=(rho/m) lambda_T^3.

For m=193.5249 eV, lambda_T=3.83116e-6 m and degeneracy=0.000162999,
well below zeta(3/2)=2.612375. At fixed density this ideal-gas threshold
would require sigma<=7.93256 km/s; at fixed density and dispersion it would
require m<=17.1998 eV. This is not a proof against a colder coherent
subcomponent, a different density or nonequilibrium condensation. It does
mean a halo-wide superfluid cannot be assumed from cosmological coldness
alone for these parameters.

## Charge conservation cannot be transferred through a new coupling

Take L=P(X)-alpha theta rho_b. Define the phase current by
j^mu=partial L/partial(partial_mu theta). Its Euler-Lagrange equation is

    partial_mu j^mu = -alpha rho_b.

In a closed boundary with no current flux this gives dQ/dt=-alpha M_b.
The sign changes if the coupling convention changes; nonconservation does
not. Thus the earlier conserved-Q proof for D=H-mQ cannot be carried over
unchanged, and the full Hamiltonian now includes a different interaction.
A compensating reservoir or an exact conserved combination would have to
be specified and audited.

The simplest shift-preserving coupling partial_mu theta J_b^mu does not
solve this automatically: for a conserved prescribed baryon current it is
a boundary term after integration by parts and supplies no bulk force.
Other derivative or density couplings are not ruled out by this observation.

## Evidence and remaining route

`phonon_selector_gate.py` verifies the coherent-saddle charge derivative,
low-density exponent and the condensation arithmetic. All seven checks
pass; its contract, results and validated manifest are in
`phonon_selector_gate_run`. The Noether and radial-scaling statements above
are analytic derivations, not claims decided by those seven numerical tests.

A useful next route must preserve an audited energy/charge budget while
introducing a derived baryonic response and vacuum scale, or explicitly
replace the protection mechanism and prove another. Calling this same
carrier a superfluid or adding a MOND phase action by hand does not finish
the repository's requested construction.
