# A conserving multistream kinetic response, and what its stopping valve does

2026-10-27. Bounded route requested by the owner through the root agent. Starting
HEAD e6d278b74755885d9f62106becef5d7b753c512c; the repository is changing concurrently.
This is an effective kinetic construction, not a fundamental field action or a
claim that cold dark energy is a particle species. The unbuilt bridge is a field
theory whose coarse velocity-energy distribution has the stated positive kinetic
description and irreversible mixing limit.

## 1. Exact kinetic construction

Let f(x,v,t)>=0 be mass per spatial and velocity volume, rho=int f dv,
u=int v f/rho, c=v-u, Pi=int cc^T f dv, p=tr(Pi)/3, T=p/rho.
T has units of velocity squared. Define the heat flux q=int c |c|^2 f dv/2.
Assume sufficient decay, positive rho,T, and regularity for integrations by parts.

The self-gravitating equation is

    partial_t f + v.grad_x f - grad(Phi).grad_v f = Q[f],
    Laplacian Phi = 4 pi G rho.

Baryons can be added to Poisson's equation. A prescribed time-dependent baryon
potential then contributes external work int rho partial_t Phi_b dx; it must not
be silently omitted from the ledger.

Choose the explicit relaxation operator

    Q[f] = Gamma[f] (M[f] - f),
    M = rho (2 pi T)^(-3/2) exp[-|v-u|^2/(2T)].

One rate with the intended symmetries and no new dimensional scale is

    J = 27 det(Pi)/(tr Pi)^3,    0 <= J <= 1,
    z = (det Pi)^(1/3)/P_star,
    A(z) = max(z-1,0)/(1+z),
    Gamma = alpha (a0/sqrt(T)) J A(z).

At rank-deficient Pi or T=0 set Gamma=0. alpha is a FREE dimensionless rate
coefficient, even if someone elects alpha=1; the shape of A is also posited. J
vanishes in ideal sheets and filaments. The geometric-pressure threshold is not
an object-boundness detector. The same velocity covariance can occur in unbound
overlapping streams. Tensor positivity and this gate do not establish a field
action or relativistic covariance.

For every nonnegative scalar Gamma[f], even state dependent,

    int (1,v,|v|^2/2) Q dv = (0,0,0).

Its entropy sign is exact. Since log M is a linear combination of the collision
invariants,

    int Q log f dv
      = -Gamma int (f-M)(log f-log M) dv <= 0.

No derivative of Gamma appears: Hdot uses Q at the instantaneous state. Equality
holds if Gamma=0 or f=M. Thus every gate-off state is an additional equilibrium
of the collision operator; the H theorem does not select its density or profile.
For exactly cold delta sheets, the regular-density entropy proof is a limiting
statement, not a finite-entropy theorem about delta distributions.

An alternative explicit elastic binary operator is

    Q_B = (Gamma[f]/rho) int b(|v-v_*|/sqrt(T),omega)
                                  (f' f_*' - f f_*) dv_* domega,

with a nonnegative dimensionless microreversible kernel b,
v+v_*=v'+v_*', and
|v|^2+|v_*|^2=|v'|^2+|v_*'|^2. Its weak form gives the same three invariants and

    int Q_B log f dv
      = -(Gamma/(4 rho)) int b (f'f_*'-ff_*) log[(f'f_*')/(ff_*)] <= 0.

The arbitrary kernel b is additional constitutive input. This formulation does
not derive microscopic stream scattering or a cross section from Lambda.

## 2. Energy-transfer ledger

The kinetic moments obey

    partial_t rho + div(rho u) = 0,
    partial_t(rho u) + div(rho uu + Pi) = -rho grad Phi,
    partial_t K + div(K u + Pi.u + q) = -rho u.grad Phi,
    K = rho |u|^2/2 + 3p/2.

For isolated boundaries, self-gravity supplies

    d/dt [ int K dx + (1/2) int rho Phi dx ] = 0.

The operator converts local anisotropy and non-Maxwellian stream structure into
isotropic random motion while preserving the local kinetic energy. Spatial
transport, represented by q and bulk/stress flux, transfers that energy between
core and envelope. It converts NO rest mass to vacuum energy and makes no claim
to satisfy or evade a bound by doing so. X54/X60's rest-energy-conversion budget
is therefore a different test. Merger drag, cosmological pressure, and halo
transport remain necessary tests for this interaction.

There is a sharp distinction: Gamma=0 does NOT imply q=0. Free streaming is
present in the left-hand side. The executable includes an exact positive beam
distribution with full-rank Pi below P_star and q_x!=0. Therefore a collision
switch is not a no-flux boundary, and does not by itself stop core evolution.

In the short-mean-free-path, slowly varying BGK regime, a gradient expansion
gives the heat-conductivity scale kappa_T=(5/2) p/Gamma for this T convention.
This approximation fails as Gamma->0. Simply replacing a vanishing collision
rate by vanishing Fourier conductivity gets even this local-limit sign wrong.
The ballistic-to-diffusive transition needs a kinetic solve, not that substitution.

## 3. A stronger, explicitly inserted conductivity valve

To test the most favorable macroscopic version, separately POSTULATE

    q = -kappa_0 J A(p/P_star) grad T,    kappa_0 >= 0.

This flux conserves total energy in closed boundaries and produces entropy
kappa_0 J A |grad T|^2/T^2 >=0. It is not derived from the relaxation operator
above. It also leaves Reynolds, bulk and gravitational fluxes present. In an
isotropic, static core, p is maximal at the center and A vanishes everywhere
once p0<=P_star, so this particular imposed conductive channel does turn off.

For a baryon-free isotropic self-gravitating untruncated Burkert profile with
zero pressure at infinity, the independently audited Jeans identity is

    p0 = C_B G Sigma^2,    C_B = 0.8261070360019096.

Hence selecting the target Sigma_star=a0/(2 pi G) REQUIRES inserting

    P_star = C_B a0^2/(4 pi^2 G)
           = 0.005231383918936051 rho_Lambda c^2  [canonical kappa=1/2].

If instead P_star=beta rho_Lambda c^2 is specified independently, the implied
surface density is sqrt(beta rho_Lambda c^2/(C_B G)); beta must have precisely
the value above to hit the stated floor. Neither collision conservation, the H
theorem, nor dimensional analysis fixes beta. The coefficient changes with
profile, anisotropy, baryons and boundary pressure. This is an inserted target,
not a derivation of 1/(2 pi) or of the fitted kappa.

## 4. Negative heat capacity: sign and stopping stability

Consider a self-gravitating, virialized, fixed-mass homologous core, with
negligible surface terms and unchanged dimensionless profile. Writing T=sigma^2,
2K+W=0 gives E_c=-K=-(3/2) M_c T, C_c=dE_c/dT<0. Also R is proportional to 1/T,
Sigma proportional to T^2 and p0 proportional to T^4.

This is a controlled toy reduction, not the exact thermodynamics of a moving,
accreting core boundary. Let C_c=-C0, C_h=b C0>0 and s=T_c/T_star, h=T_h/T_star.
An explicit two-zone conductive exchange is

    ds/dtau = -A(s^4)(h-s),
    dh/dtau = -(1/b) A(s^4)(h-s),
    E_total/(C0 T_star) = -s + b h = constant.

Its total entropy production is proportional to
A(s^4)(h-s)^2/(s h)>=0. The sign has physical consequences:

* Hotter envelope (h>s>1): core GAINS energy, cools, expands, and approaches the
  inserted floor from above if the envelope remains hotter at s=1.
* Cooler envelope (s>max(h,1)): core LOSES energy, heats, contracts, and moves
  AWAY from the floor. The H theorem allows this gravothermal direction.
* s<1: the valve is off; every such state is stationary in this toy. The floor
  is not a two-sided attracting equilibrium. There is no restoration from below.

At thermal equality s=h with the valve on, Delta=s-h satisfies

    dDelta/dtau = A(s^4)(1-1/b) Delta + O(Delta^2).

Equality is stable only for b<1, unstable for b>1, neutral to this order for b=1.
A large envelope acts as the destabilizing bath. A finite envelope can reverse
its temperature ordering, so even the initially expanding branch need not reach
the floor; the energy ledger determines its accessible endpoint.

The valve can be a ONE-SIDED stopping rule for an initially dense, colder core.
It is not an attractor theorem. A heat impulse delivered after stopping raises
E_c, lowers T_c and drives Sigma BELOW the floor. With A=0 there, no restoring
response exists. A merger, accretion episode, tidal work or ballistic flux can
do this without violating total conservation. Conversely, collapse raises p,
reactivates the gate and can initiate contraction again. Any claimed permanent
floor must handle these recurrences explicitly, not only an isolated smooth
expansion trajectory.

## 5. Finite primordial dispersion

For a nonrelativistic freely redshifting homogeneous distribution,
rho~a^-3, T~a^-2, p~a^-5 and J=1 if isotropic. The amplitude gate can therefore
activate at early times for any finite relic dispersion. Unlike H(det Pi), it
does not jump to full strength for arbitrarily small p at fixed epoch.

Activation alone is not an exclusion: elastic mixing conserves density and
energy, and a homogeneous Maxwellian has Q=0 even if Gamma>0. At p>>P_star our
particular rate scales Gamma~a; in matter domination Gamma/H~a^(5/2). One must
calculate perturbations and the pressure/free-streaming scale for the actual
initial T and rate. There is no claim of guaranteed early-universe safety.

## 6. What is new relative to the inspected failures

CFG351 gated a modified-law action; its late inner activation failed the required
turnaround edge. Here activation acts on cold kinetic relaxation. X57-X64 mostly
ask how to remove or convert cold mass while preserving a fundamental law, or
classify which objects retain it. This construction conserves the cold mass and
ordinary gravitational source, and studies internal energy transport instead.
It therefore is not one of their excluded conversion or retention keys. It also
does not solve their data tension: X53's halo-mass normalization remains open.

## 7. Decisive next obligation

A microscopic cold-field interaction must generate a finite transport law and
its stress dependence, including flux across the inactive region. It must either
derive beta and show expansion halts robustly despite accretion, or supply a
restoring energy exchange on both sides with a complete reservoir. The present
calculation supplies a conserving operator and identifies exactly why the most
direct threshold construction falls short. No stable selected core density is
claimed.
