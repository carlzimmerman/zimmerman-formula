# Cold energy: common-action advance and completion boundary

20 October 2026. Exploratory research, **original full theory OPEN**.
Base `dce2a2e3d`; the shared CE-FM-093 checkpoint and frozen/publication files
are unchanged. This packet supplies an explicit alternative common **matter**
action and new calculations. It does not adopt a replacement canonical action.

The new result is a classical action containing a near-threshold charge-2
production source, a charge-1 carrier and the neutral mediator that permits
self-bound fragments. An exact polynomial certificate gives a uniform
`E >= 0.85 m |Q|` floor in isolated flat space. Full three-field stationary
solutions retain a positive candidate merger gap, and the homogeneous phase
has a nonzero zero-pressure state with positive local compressibility.
Production, binding and a finite energy floor can therefore coexist in this
specified altered matter model. The original stronger bound, its benchmark
scattering and its pressure results do not transfer.

It remains necessary to derive real exported energy/J/charge, a population and
formation history, the observed dwarf profiles, and any additional gravity law
from the same model. A stationary energy difference is not a cooling rate.

## 1. What is meant by cold energy

Here it means massive positive-energy fields whose bulk motion can be slow,
so the dilute material energy is dominated by rest energy. It is not a new
unlimited energy supply. Rest energy, binding energy, heat and gravitational
potential energy must be distinguished. A dense self-bound phase can have zero
equilibrium pressure while retaining a substantial sound speed; that is not
the dilute cold-gas equation of state.

Use natural units hbar=c=m=1 in the new matter calculations. Physical masses,
field normalization, abundances and coupling renormalization have not been
identified with observed particles. Named astronomical quantities below retain
their indicated units and assumptions.

## 2. The original protected carrier is not ARGON

Let I=|Psi|^2, X have charge 2 and Psi charge 1. With Delta=MX^2-4m^2>0,

    V_protected = m^2 I + 4m^2 |X|^2
       + |sqrt(Delta) X + (g/sqrt(Delta)) Psi^2|^2
       + lambda_rep I^2,             lambda_rep >= 0.

Writing lambda=g^2/Delta+lambda_rep gives

    V_protected = m^2 I + MX^2 |X|^2
                  + g(X* Psi^2 + X Psi*^2) + lambda I^2.

For decaying or periodic classical fields, square completion proves
`E >= m |Q|`. The synchronized, localized, nongravitating stationary class
has no ordinary subthreshold Q-ball under this potential: its fixed-frequency
functional is nonnegative and spatial scaling forces the trivial state.
Gravity, finite-density periodic condensates and release of pre-existing
`E-m|Q|` are outside that exclusion. See [carrier audit](CARRIER_ACTION_AUDIT.md).

ARGON instead uses

    V_ARGON = I + 1.99 I^2 + 200 chi I + U(chi),
    U(chi) = 10000 chi^2/2 - 100 chi^3/8 + chi^4/4.

Its real neutral mediator changes the energy bound. Eliminating a slowly
varying neutral field at low I produces attraction. Calling chi the old X
would change its charge, kinetic normalization, equation and interactions.

## 3. Explicit alternative common matter action

The following is a concrete candidate extension, not a derived cosmic theory:

    V = m^2 I + MX^2 |X|^2 + g(X* Psi^2 + X Psi*^2)
          + lambda I^2 + a chi I + U(chi),
    U(chi) = Mchi^2 chi^2/2 - Mchi chi^3/8 + chi^4/4.

Parameters in the performed calculations:

    m=1, MX^2=4.0016, g=0.002168, Mchi=100, a=200,
    lambda=1.99+g^2/MX^2 = 1.9900011745861654.

These choices are exploratory and motivated by the earlier branch. The small
g is borrowed from a prior production benchmark; lambda and the mediator are
not predictions. The protected-family remainder would be
`lambda_rep=lambda-g^2/(MX^2-4)=1.9870635345861651`, radically different from
the old scattering benchmark. Setting **a=0** decouples the neutral sector and
recovers a member of the protected family. Taking g to zero **along the declared
family lambda(g)=1.99+g^2/MX^2** leaves exact ARGON plus a decoupled X. Holding
the performed lambda fixed instead leaves a slightly different ARGON quartic.
Simply imposing chi=0 at a!=0 is not a consistent truncation:
the daughter density sources chi immediately.

A minimal gravitational embedding, with metric signature (-+++), is

    S = integral sqrt(-gmetric) [ (R-2 Lambda)/(16 pi G)
          - grad_mu Psi* grad^mu Psi - grad_mu X* grad^mu X
          - (grad chi)^2/2 - V ] d^4x + S_b[gmetric,baryons].

The curvature convention is fixed by `G_mu_nu+Lambda g_mu_nu=8 pi G T_mu_nu`.
This is ordinary minimally coupled scalar matter in GR. It specifies a
possible metric coupling and counts its real mass once. It does **not**
derive the repository's additional polarization law. Adding that law requires
a new explicit coupled action and a fresh source/stress calculation.

With Box_+=dt^2-laplacian, the flat matter equations are

    (Box_+ + m^2) Psi + 2 lambda |Psi|^2 Psi
             + 2g X Psi* + a chi Psi = 0,
    (Box_+ + MX^2) X + g Psi^2 = 0,
    Box_+ chi + Mchi^2 chi - 3 Mchi chi^2/8 + chi^3 + a|Psi|^2 = 0.

They determine reciprocal source response. There is no externally prescribed
friction, cooling bath, density target or per-dwarf switch in this action.

## 4. Conserved books and exact classical protection

Choose the ARGON positive-charge convention (Psi proportional to exp(+i omega t)):

    q = 2 Im(Psi* dt Psi) + 4 Im(X* dt X),
    j = -2 Im(Psi* grad Psi) - 4 Im(X* grad X),
    dt q + div j = 0.

The flat Hamiltonian density and energy flux are

    e = |dt Psi|^2 + |grad Psi|^2 + |dt X|^2 + |grad X|^2
           + [(dt chi)^2+|grad chi|^2]/2 + V,
    S_E = -2 Re(dt Psi* grad Psi + dt X* grad X) - dt chi grad chi,
    dt e + div S_E = 0.

Momentum density equals S_E in these units. With the canonical symmetric
stress, `J=integral x cross S_E d^3x`; angular flux through a surface is
`integral x cross (T dot n) dA`. Net orbital transport and intrinsic remnant
spin must be recorded separately. In curved space the conserved statement is
covariant stress-energy conservation; flat E is not an invariant global energy
in an arbitrary evolving spacetime. Galaxy-scale gravitational work and field
energy must be included, with appropriate asymptotic/boundary conditions.

For mu=17/20, complete the charge-2 potential square:

    V - mu^2(I+4|X|^2)
      = (MX^2-4mu^2)|X+g Psi^2/(MX^2-4mu^2)|^2
          + delta I + A_mu I^2 + a chi I + U(chi),
    delta=1-mu^2=111/400,
    A_mu=lambda-g^2/(MX^2-4mu^2)>0.

For chi>=0 all remaining terms are nonnegative. For chi=-t<0, the quadratic
in I is nonnegative if either at<=delta or

    F(t)=4 A_mu U(-t)-(at-delta)^2 >= 0.

Here `t0=delta/a=111/80000`. The exact rational quartic F is positive at t0
and has **zero Sturm roots on [t0,infinity)**. Its signs are [+,+,+,-,-] at
t0 and [+,+,+,+,-] at positive infinity. Thus the potential inequality holds
at every classical field amplitude, not just sampled profiles. Completing
time-derivative squares gives `E >= mu |Q|` under the stated flat boundary
conditions. This does not prove a renormalized quantum bound, gravitational
stability or `E>=m|Q|`. Full coefficients are in run_001 and independently
reconstructed in the carrier audit.

## 5. Production in the same action

A prepared circular source X=A exp(i MX t), Psi=chi=0 is a homogeneous
solution. At first order in daughter perturbations the added neutral mediator
has no source, since its source is a|Psi|^2. The daughter linear equation is

    ddot Psi_p + (p^2+m^2) Psi_p + 2g A exp(i MX t) Psi*_{-p}=0.

After removing half the source phase, the growth condition is

    |p^2 - m^2 u_star^2| < 2 |g A|,
    MX=2m sqrt(1+u_star^2), u_star=.02.

The free two-body kinematics are p_star=m u_star and
v_star=u_star/sqrt(1+u_star^2). These linear relations follow for this action;
finite depletion, neutral production, daughter heating, seeding and the
nonlinear final yield must be recalculated. Exactly zero classical daughter
fields stay zero. A prepared source population or quantum initial state and
an abundance/epoch mechanism are still required.

## 6. Binding and a saturated dense phase

For low I and slowly varying neutral fields,

    chi = -(a/Mchi^2) I + O(I^2),
    V_eff,neutral = I + [lambda-a^2/(2Mchi^2)] I^2
                       + a^3 I^3/(8Mchi^5) + O(I^4).

The coefficients here are approximately -0.0099988254 and +0.0001. The
attractive quadratic in I favors concentration; positive higher-density
terms can saturate it. This expansion alone is not trusted at a dense core
or near the charge-2 resonance; the actual tests retain X and chi.

For homogeneous rotating fields Psi=sqrt(I) exp(i omega t),
X=b exp(2i omega t), chi=h, eliminate b exactly:

    D=MX^2-4omega^2, b=-g I/D, A(omega)=lambda-g^2/D,
    Omega=(1-omega^2)I+A(omega)I^2+a h I+U(h),
    0=1-omega^2+2A I+a h,   0=U'(h)+a I,
    P=-Omega, q=2omega(I+4b^2), e=omega q-P.

The nonzero zero-pressure solution is

    I=49.00650744, h=-0.97646151, b=-0.10747018,
    omega=e/q=0.86789830, q=85.14552, e=73.89765.

The local amplitude Hessian is positive. On the neighboring stationary branch
`dP/domega=q` and the adiabatic long-wavelength sound formula
`cs^2=q/[omega dq/domega]` gives **0.2479230**. Finite differences check the
implicit derivatives. This supplies a local compressible dense-phase candidate,
not a global phase diagram, full perturbation-stability proof, dilute-vacuum
coolant or cosmological cold-sound-speed result.

The original run_002 omitted a h I from Omega and failed. Its code/output are
retained with status failed. run_003 corrects that term and adds independent
full-potential and field-derivative controls; no physical threshold changed.

## 7. Full stationary fragments and merger energy

For radial Psi=f exp(i omega t), X=b exp(2i omega t), chi=h:

    f''+2f'/r = [1-omega^2+2lambda f^2+a h+2g b] f,
    b''+2b'/r = (MX^2-4omega^2)b+g f^2,
    h''+2h'/r = Mchi^2 h-3 Mchi h^2/8+h^3+a f^2,
    Q=8pi omega integral r^2(f^2+4b^2)dr,
    E=4pi integral r^2[omega^2(f^2+4b^2)+f'^2+b'^2+h'^2/2+V]dr.

The new action's candidate branch, L=60 and tolerance1e-7:

| Q | omega | E | E/Q | charge fraction in X |
|---:|---:|---:|---:|---:|
| 80000 | .9217883883 | 76151.177234 | .9518897154 | .00106960 |
| 160000 | .9095170227 | 149323.629586 | .9332726849 | .00105631 |

    2 E_stat(80000)-E_stat(160000)=2978.724881,
    gap / [2 E_stat(80000)] = 0.0195579700.

The comparison changes L=40 to60 and tolerance1e-5 to1e-7; energies agree
within 1.3e-11 relative. Integrated charge, virial
`Tgrad+3V-3Trot=0`, tails and finite-difference dE/dQ=omega independently
check the normalization. This is finite collocation evidence for a stationary
branch, not a continuum error theorem, uniqueness, a ground state, nonlinear
stability or a dynamically measured merger. The gap can remain as excitation
or spin unless a real outgoing channel is established.

## 8. Cooling, charge loss and angular momentum

The three-field matter sector has no massless vacuum carrier. Its minimal GR
embedding also has metric/gravitational-wave modes, whose emission is a
separate uncomputed channel. Around the matter vacuum, freely propagating
Psi, X and chi have thresholds 1, sqrt(4.0016) and100.
For a rotating remnant, a charge-q positive-frequency sideband opens when

    Omega_rot >= mass - q omega,

and its opposite-charge branch opens at mass+q omega. A static evanescent X
admixture is not coolant. Coherent propagating angular modes obey Jdot/Edot
=m_azimuth/nu_lab, with sign and charge measured separately; their excitation
and escape rates require a calculation. Internal sound can carry energy inside
a dense phase, but below-threshold sound does not automatically propagate into
vacuum. Neutral chi radiation and charged particle/antiparticle emission are
possible at adequate frequencies; their thresholds do not prove an all-rate no-go.
See [flux audit](ASYMPTOTIC_FLUX_AUDIT.md).

For a pair with initial total Q_i, remnant charge Q_r and escaping charge Q_e:

    Q_i=Q_r+Q_e,
    E_i=E_remnant(Q_r,J_r,excitations)+E_escape+E_other,
    J_i=J_orbit,rem+J_spin,rem+J_escape+J_other.

At small positive charge loss q_e, E_stat(Q_i-q_e)=E_stat(Q_i)-omega q_e+...
Free positive-charge emission costs at least m q_e in energy. Therefore the
fixed-Q gap must pay `(m-omega)q_e` as well as outgoing kinetic energy; the
old fixed-Q gap cannot be spent while silently keeping the old charge profile.
This is a necessary ledger, not a predicted loss fraction.

Intact nonlinear daughter fragments are a separate outgoing channel. Their
energies may obey E_stat(q)<m q, so the free-wave bound E_escape>=m|Q_escape|
must **not** be applied to every bound fragment or ejecta ensemble. A merger
must identify which charge leaves as free waves, bound fragments, or both.
The mass gaps constrain linear radiation; they do not exclude slow transport
of pre-existing composite objects.

An actual outward angular-momentum mechanism could be shear transport from
conservative fragment interactions. In an approximately spherical rotating
fluid with measured positive isotropic dynamic shear viscosity eta and angular
velocity Omega_g(r), the viscous part of its outward torque flux would be

    F_J = -(8pi/3) eta r^4 dOmega_g/dr,
    d(heating power)/dr = -F_J dOmega_g/dr >= 0.

The total angular flux also includes advection and any field stresses. These
equations explain how differential rotation can move J outward while heating
the receiver. They do not supply eta or the sign of an actual galaxy's shear.
In a rarefied/coagulating fragment gas a local viscosity closure may fail;
then the measured differential collision kernel and its stress must be used.
An independently conserved action prevents invented cooling, but does not
guarantee a useful rate or a receiver capable of surviving that heat.

## 9. Gravity law: separate required choice

The audited polarization candidate has K=4piG, u_vec=KP, u=|u_vec|<a0:

    W_full=[-a0 u-a0^2 ln(1-u/a0)]/K,
    W_rem=W_full-u^2/(2K),
    L_pol=-|grad Phi-KP|^2/(2K)-rho_b Phi-W_rem
                       -gamma|grad P|^2/2, gamma=K Lstar^2/2,
    div(grad Phi-KP)=K rho_b,
    grad Phi-KP=[u^2/(a0-u)] uhat-gamma laplacian P.

In the spherical negligible-stiffness limit,

    g_Nb=u^2/(a0-u), g=g_Nb+u, g_Nb=g^2/(g+a0),
    g_deep=sqrt(a0 g_Nb), V_flat^4=G M_b a0.

KW'_full=a0 u/(a0-u) and KW'_rem=u^2/(a0-u) are different quantities.
Using full W in the completed square double counts the critical quadratic.
The exponential interpolation used in Class A is also different from this
simple interpolation outside their common leading deep limit.

If div P is identified with the cold density perturbation, the critical
quadratic cancels its ordinary quadratic self-gravity. If the new real carrier
is instead independent matter, it changes the source equation. Adding a halo
mass, polarization discrepancy and a law-boosted clump formula without a new
variation is not a consistent unification. The new GR matter action above
chooses real mass and has not added this P action. The choice remains explicit.
See [gravity action audit](GRAVITY_ACTION_AUDIT.md).

The relation `a0=kappa c sqrt(G rho_DE)` with kappa=1/2 is still fitted.
For mass-equivalent rho_DE it implies a0^2=Lambda c^4/(32pi); this rewriting
does not derive the coefficient, vacuum scale, abundance or carrier coupling.
The single Newtonian polarization potential does not predict the full lensing
metric. Minimal GR predicts lensing from its actual stress, but does not prove
the observed profiles or recover an extra polarization force.

## 10. Astronomical gates that remain open

The reference four-dwarf budgets are not repaired by an attractive microscopic
phase. At the prior canonical B0/G1/C endpoint Sextans has free stock
25.3958 million solar masses and only .2910 million in the escaping receiver.
That endpoint needs receiver speed about128km/s. Its old-energy J capacity at
the core is only4.856% of the required value; the stationary-shell last-torque
radius is about13.485kpc. Ideal binding-powered capacity is possible, but an
isotropic wind carries only about.55% of the angular momentum in the earlier
common-budget example. Directed recoil or a measured outward torque is needed.

Independent forward projection also exposed the profile/observable gate:
the reference Sextans C-profile cannot reach a whole-population7.9km/s with
the allowed stock (all-stock ceiling6.93581km/s). Its core-only equivalent
mass is33.913 million solar masses, also a lower bound on total free stock
within that fixed-C-plus-outer-shell family. This is conditional on interpreting
the catalogue dispersion as that global moment, not an arbitrary-profile or
observational exclusion. Fornax and LeoI's old global upper guards do not
guarantee their projected-aperture likelihoods. Member selection, profile and
stock must be settled before treating an old energetic endpoint as a fit.

No per-galaxy hidden coupling, processing fraction or spin is chosen here.
A common microscopic kernel and independent assembly/environment histories
must select the different surviving cores, with stellar heating and return
flow included.

Claude's finalized CFG928 conditionally revives a fragile P2 static galaxy
score after IMF-corrected red lenses and withholding clusters. It does not
derive capture, exported flux or the four SFH-based endpoint budgets. Newly
frozen CFG930/932 investigate energy-limited settling; no result is assumed
from their criteria. CFG932's representative set omits Sextans and LeoI, so
even a later window pass will require a separate four-dwarf calculation.

## 11. Executable completion sequence

1. **Stability and flux, same action.** Linearize the full three-field equations
   about the resolved isolated branch. Check radial and nonradial modes and
   compute outgoing sideband transmission. Then use matched pair evolutions
   over relative phase, velocity and impact parameter, including translation/
   boost controls. Extract E,Q,p and vector orbital/intrinsic J at multiple
   radii, and show convergence at the small orbital-energy scale. No heavy
   job is launched by this packet.
2. **Measure a kernel rather than insert a selector.** Determine elastic,
   capture, merger, fission and emission branches with their remnant states.
   Convolve them with declared phase-space distributions; derive stress, heat,
   charge loss and escape without assuming a positive outward torque. Test
   whether the fitted P2 velocity scale arises, rather than inserting it.
3. **Close real inventory and observables.** Derive source preparation and
   production/abundance; resolve stellar selection and stock-compatible dwarf
   profiles. Evolve the same kernel for Draco, Sextans, Fornax and LeoI,
   including gravity, tides, stellar heating and finite outer receivers.
4. **Choose and derive the force architecture.** Either predict observed
   gravitational profiles with the real-matter GR action, or construct a
   reciprocal carrier–polarization/metric action and rederive its sources,
   stable excitations, lenses and cosmological perturbations. Preserve the
   exact FULL/REM dictionary and forbid inferred-mass double counting.
5. **Normalization and independent tests.** Derive or openly calibrate m,
   abundance, couplings, a0 and kappa. Test released predictions and withheld
   data under their actual selection/uncertainty model. None of steps1–4
   converts a fitted normalization into a derived one.

`NEXT_TEST.json` records the first unresolved implication and a precise flux
test. Run commands, hashes and scopes are in the adjacent contracts and source
receipts. run_001 has43 passed controls; corrected run_003 has19. Both are
completed v2 evidence records, peak RSS below187MB. The failed17-control
run_002 remains failed. Numerical counts are implementation evidence, not
independent physical confirmations. This is a substantive common-action
checkpoint; it is not the completed cold-energy theory.
