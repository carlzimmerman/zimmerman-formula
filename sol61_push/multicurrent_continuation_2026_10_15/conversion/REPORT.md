# Conservation theorem for local tether-to-free conversion

2026-10-15. Base HEAD: `5c06d239febe644b9f485477b4c2f93390a23b3e`.
This is a new conditional extension and obstruction theorem, not an edit of the
frozen canonical model. Analytical self-review; no empirical score, microscopic
identification, large simulation, or independent referee is claimed.

**Verdict: incomplete, with the smallest missing implication now isolated.**
A nontrivial local conversion to a gravity-only neutral species cannot preserve
both the old one-species mass polarization and the gauge-parent charge
dictionary with only the tethered and free populations. A conservative local
reaction action and transport extension does exist after charged stocks are
counted. Its Gauss source follows all charged stocks, rather than the tethered
label alone. It does not derive canonical S4's permanent, one-way, retained
untethering.

The source records are the immutable package inputs `CANONICAL_2026-10-14.md`
(S2-S4), `OPEN_ITEMS_RESULT.txt` (B), `RTM_REPORT.md` (1-4), and
`PORTAL_REPORT.md` (1, 3-6, 8). They preserve the actual source text at this HEAD.
No external factual claim is needed below. Particle masses are repository
inputs, not newly authenticated constants.

## 1. Pin the objects before equating them

Work locally with signature -+++, c=1. For each massive material species a,
N_a^mu is its future-directed timelike number current, m_a>0 its rest mass,
q_a its dark gauge charge, and nu_ar its signed products-minus-reactants
coefficient in reaction r. Massless radiation is counted separately, with
m=0, when present in a reaction or total stress tensor.

    nabla_mu N_a^mu = sum_r nu_ar R_r.
    M^mu = sum_a m_a N_a^mu,       Q^mu = sum_a q_a N_a^mu.

M is a rest-mass current. It is not the total relativistic energy current.
Photons have m=0 but carry stress and energy. Bound-state masses already
include binding energy. If sum_a m_a nu_ar is nonzero, rest mass has a source;
total energy-momentum can still be conserved with the listed products.

There are two distinct spatial polarization dictionaries:

* Canonical mass displacement P_t: div P_t=rho_t-rhobar_t and
  partial_t P_t=-j_t in the source-free model. rho_t and j_t are tethered
  REST-MASS density and flux.
* Gauge displacement D: div D=rho_Q in a patch containing every charged
  species and any actual compensator. With zeta=sqrt(4 pi G), put
  P_Q=D/zeta. Then div P_Q=rho_Q/zeta. The static RTM identification with
  mass requires rho_Q=zeta rho_M. A reference background requires an actual
  compensating charge/current or an explicitly subtracted-background
  approximation; a constant reference density is not itself that stock.

For independent species currents, Q^mu=zeta M^mu for EVERY admissible mixture
if and only if q_a=zeta m_a for every included species. Proof: sufficiency is
termwise; necessity follows by varying one independent species current at a
time. Equality in one specially arranged mixture is a weaker state-dependent
condition. Neutral positive-mass free species violate the structural identity.

Even with equal q/m, the exact gauge evolution is

    partial_t P_Q = -j_Q/zeta + curl H/zeta,

where H is the constitutive magnetic field, with charge orientation chosen to
give the Gauss convention above. The canonical equation without a solenoidal
term is a longitudinal/electrostatic reduction, or requires curl H=0. Gauge
charge conservation fixes its divergence; it does not delete transverse modes.
Thus neither a different frame nor a curl freedom repairs a source with
nonzero divergence.

## 2. Exact reaction and polarization compatibility theorem

For local reaction rates R_r that can vary independently:

1. Gauge charge is conserved iff sum_a q_a nu_ar=0 for each active r.
2. The sum of species rest masses is conserved iff sum_a m_a nu_ar=0.
3. Any other additive charge b is conserved iff b dot nu_r=0.
4. A closed reciprocal kinetic reaction conserves four-momentum iff every
   included event satisfies sum_in p_a^mu=sum_out p_a^mu. In a material
   quasiparticle description the energies and momenta must come from the SAME
   varied total Hamiltonian, including medium/binding terms.

The first three conclusions follow directly by weighting the continuity
equations. The fourth follows by weighting the collision integral by p^mu;
its event delta function annihilates the sum. Conversely, a reaction with a
nonzero weighted stoichiometric sum changes that additive quantity wherever
its independent rate is nonzero. This is a statement about the declared
species and reactions, not about unlisted sinks.

For the particular nonrelativistic same-mass transfer

    partial_t rho_t+div j_t=-S,
    partial_t rho_f+div j_f= S,

differentiating the two proposed P_t identities gives

    div(partial_t P_t+j_t)=-S-partial_t rhobar_t.                  (1)

Thus retaining partial_t P_t=-j_t is possible iff S=-partial_t rhobar_t
pointwise. With spatially uniform rhobar_t, only spatially uniform S can
satisfy this, and with fixed rhobar_t it forces S=0. On a torus a correction
C_t in partial_t P_t=-j_t+C_t must obey

    partial_t rhobar_t=-<S>,       div C_t=-(S-<S>).               (2)

On a closed bounded domain the corresponding condition is
integral_boundary C_t.n=-integral(S+partial_t rhobar_t).
Equation (2) fixes only the divergence. A Poisson gradient is a constraint
solution, not a local causal action or a derived conversion law.

There is a constructive source-free identity for the TOTAL mass:
choose div P_total=rho_t+rho_f-rhobar_total initially and evolve
partial_t P_total=-(j_t+j_f); total continuity preserves the constraint.
Decompositions P_total=P_t+P_f require opposite conversion corrections
C_t and -C_t (and consistent separate reference densities). This total-mass
identity is exact kinematics. It does not show that a constitutive tether
depending on P_t can depend instead on P_total without changing the force law.

An alternative local bookkeeping field is the accumulated converted density
rho_conv=integral_initial^t S dt. Then rho_t+rho_conv and j_t are conserved,
so an ordinary displacement can represent that pair. rho_conv is a memory
stock, not the actual surviving tethered mass; equating its polarization to
the physical field retains the converted charge/mass in the field source.
It cannot justify deleting tether energy.

## 3. The precise two-population obstruction

For a single t->f reaction with one incoming t and k outgoing f,

    nu=(-1,k),   m_t=k m_f,   q_t=k q_f

are the necessary rest-mass and charge conditions. If q_t=zeta m_t>0 and
free f is neutral, the charge condition fails for every k. If only two
populations and no partner stock exist, this neutral conversion is impossible
in a gauge-invariant local action with conserved dark charge.

For one-to-one equal-mass relabeling, conservation instead requires q_f=q_t.
Minimal charge coupling then acts on f too. A label change alone does not
remove its force; the charge polarization tracks t+f. Nonminimal screening,
a changed medium response, confining bound states, or a charged receiver could
change that conclusion, but each adds physical dynamics and its energy/stress.
The conclusion is restricted to this declared local gauge construction; it is
not a no-go theorem for every nongauge phenomenological tether.

The integral version is especially simple: in a closed domain a one-sign
nonzero initial gauge charge cannot become entirely neutral matter without
charged remnants, an opposite-charge inventory, or charge flux through the
boundary. The issue is not cured by choosing a mass frame.

## 4. A conservative, local four-stock action witness

Introduce a counted neutral receiver R0 and a charged receiver R+:

| species | mass | dark charge | reaction coefficient |
|---|---:|---:|---:|
| t | m | q | -1 |
| f | m | 0 | +1 |
| R0 | M | 0 | -1 |
| R+ | M | q | +1 |

The reaction is t+R0 <-> f+R+. It exactly conserves total rest mass,
dark charge, the number N_t+N_f, and the receiver number N_R0+N_R+.
Both incoming stocks are indispensable. It transfers the gauge charge while
allowing asymptotic neutral f quanta to move under ordinary gravity between
collisions, if all constitutive arguments also exclude f.
There is no mass gain from a relabeling: R0 was already gravitating, and R+
still gravitates afterward.

One classical local action on a finite-density timelike-current domain is

    S = S_EH + S_other + integral sqrt(-g) [
          L_medium(F,U_*,n_*) - sum_a epsilon_a(n_a)
          + sum_a N_a^mu(partial_mu theta_a+q_a A_mu)
          - V(Xi) ] d4x,
    Xi=-theta_t+theta_f-theta_R0+theta_R+,
    n_a=sqrt(-N_a.N_a),   V(Xi)=g[1-cos(Xi)],   g>=0.            (3)

For a concrete constitutive member set U_*=U_Q, n_*=sqrt(-Q.Q)/q, and

    L_medium=Le(E_U)-beta(E_U,n_*) B_U^2/2,
    Le(E)=D0 E-D0^2 log(1+E/D0),   D0=a0/zeta.

E_U and B_U are measured by the varied U_Q. Any fixed smooth beta defines
the conservation calculation; a positive constant already gives an explicit
member. The static pure-electric Le is the RTM tether function. A constant
beta is NOT claimed to meet RTM's cone criterion; selecting and proving a
healthy multi-current response remains a separate obligation.

All N_a, phases, A and metric are varied. This is an irrotational-fluid
witness, sufficient for the current/reaction theorem; no arbitrary vortical
or collisionless distribution is thereby derived. The sign of q/A is chosen
consistently with the RTM Gauss orientation. Under A->A+d lambda,
theta_a->theta_a-q_a lambda, Xi is invariant because q dot nu=0.
Phase variation yields

    nabla.N_a = nu_a R,       R=-V'(Xi).

This proves a genuinely local, gauge-invariant reaction source exists with
the required additive conservation laws. Metric and gauge variation of the
whole action give reciprocal stress exchange and on-shell covariant
conservation of the total material/field stress. A global energy requires
appropriate time-translation and boundary assumptions; wherever that Noether
energy is defined it includes V, the complete medium and particle energy,
with gravity handled consistently in the chosen approximation. Charge
transfer has no unexplained deletion of a P_t energy term: the gauge field
responds to Q=q(N_t+N_R+) throughout.

Equation (3) is coherent reversible conversion and R has either sign. It is
not a prescribed positive Boltzmann reaction rate, a proof of stability, or a
microscopic particle identification. For a contact-scattering witness use
four complex scalar fields with positive masses m,m,M,M, charges q,0,0,q,
standard kinetic terms and the Hermitian interaction

    L_int = -[lambda phi_f^* phi_R+^* phi_t phi_R0 + h.c.].      (4)

This quartic is gauge invariant. A stable polynomial potential can be chosen:
add (|lambda|/2) sum_a |phi_a|^4, since
2 |product phi_a| <= (1/2) sum_a |phi_a|^4 by AM-GM.
The global phase symmetries conserve the two species-pair numbers; the
weighted sum m(N_t+N_f)+M(N_R0+N_R+) is the rest-mass invariant in its
declared particle-only 2->2 kinetic sector. The full relativistic scalar
theory also has antiparticles; pair production is outside this rest-mass
invariant sector. Local four-momentum conservation permits ordinary
2->2 scattering. For example m=M=1, incoming momenta (+3/4,0,0) and
(-3/4,0,0), outgoing (0,+3/4,0) and (0,-3/4,0), have all four energies
5/4, nonzero phase space, and exactly matching total four-momenta. The
interaction has a nonzero tree contact matrix element when lambda!=0.
For particles exactly at rest and degenerate mass sums, phase space closes;
this witness does not assert spontaneous conversion of perfectly cold dust.

The fluid witness (3) and particle witness (4) are alternatives, not two
copies of the same carrier added to one stress tensor. A proposed kinetic
realization must actually match its interaction and constitutive medium.

The critical dictionary has a decisive cost. Set q=zeta m. If M=m, all
charged stocks retain the same critical ratio and

    Q/zeta = m(N_t+N_R+).

That CHARGED rest mass is conserved even during reaction. Charge conversion
therefore does not locally deplete the Gauss source: it replaces t charge
with R+ charge. To weaken a halo field, R+ must leave or be redistributed by
solved transport, with its charge/current, mass, field energy and reaction
partner included. If M!=m, the charged receiver has q/M!=zeta and the
one-species critical force cancellation no longer applies to it. Choosing
a small M does not avoid that additional dynamics.

## 5. Reciprocal kinetic transport and exact energy accounting

For a dilute on-shell reaction with phase-space occupations f_a, a local
2<->2 collision factor contains

    W delta4(p_t+p_R0-p_f-p_R+) [
      f_t f_R0 (1+eta_f f_f)(1+eta_R+ f_R+)
      - f_f f_R+ (1+eta_t f_t)(1+eta_R0 f_R0) ],               (5)

with W>=0 from the SAME Hermitian interaction; eta=+1,-1,0 for Bose,
Fermi, classical conventions. Integrating this event kernel into C_a gives
sum_a q_a integral C_a=0, sum_a m_a integral C_a=0, and
sum_a integral p_a^mu C_a=0. The proof is the weighted stoichiometry and
delta function, not a fitted rate. Occupations and measure factors need their
usual consistent species normalizations; no numerical cross section is used.

In a reciprocal material action the single-particle energy must instead be
the full functional derivative epsilon_a=delta H_total/delta f_a. The exact
collision energy condition is sum_in epsilon=sum_out epsilon. Using only
bare masses/free energies while deleting constitutive P_t energy does not
meet that condition. Reaction momentum and energy then enter species moment
equations as sources whose sums vanish; field/material stresses and gravity
carry their own reciprocal exchange. This is the conservative transport
contract, not a claim that (5) with bare free energies already implements all
RTM density/current dependence.

Permanent no-recapture and a positive-only R do not follow from (3)-(5).
The Hermitian conjugate supplies the inverse channel. Escape of R+, absence
of reverse collision partners, dissipation into counted radiation, or a
derived barrier can suppress reverse events in an open subsystem, but each
requires dynamics and an energy/entropy budget. An unbinding sign criterion
alone specifies none of these.

## 6. What the actual neutron portal conserves

Use the source's actual assumed masses, in MeV:

    m_n=939.56542194, m_chi=m_n-0.5, m_S=1,
    m_p=938.27208943, m_d=1875.612945.

Charges are q_chi=q_S=q, q_antiS=-q; neutron, proton and deuteron are dark
neutral. The portal is y S^dagger nbar P_L chi+h.c. It supplies the following
charge-conserving reactions, with exact rest-mass changes per forward event:

| reaction | sum_out m - sum_in m (MeV) | counted charge stock |
|---|---:|---|
| chi+gamma -> n+S | +1.5 | emitted S |
| chi+antiS -> n+gamma | -0.5 | consumed antiS |
| chi+p -> d+S | -0.72456637 | emitted S |

All rows conserve dark charge and generalized baryon number. Their total
four-momentum is conserved by on-shell reaction kinematics; their sums of
REST masses are not. Photon activation spends energy; recombination and
nuclear capture release it into the listed products. Exact gravity must
include those energies, binding and field stress. The same-mass t/f source
equations cannot be copied literally into this portal model.

If chi has q/m_chi=zeta, emitted S has q/m_S=(m_chi/m_S) zeta,
about 939.0654 zeta in this example. Treating it as the same critical dust
medium is an error. The scalar is a major charge carrier despite its small
rest-mass fraction. Recombination needs an actual antiS stock and can screen
the old field; opposite stocks cannot be subtracted from the dynamics.
This report does not reauthenticate the source's external particle limits
or rerun its amplitudes. The exact arithmetic checks only its displayed
mass/charge bookkeeping.

## 7. Mass frame, charge frame, and neutral force freedom

U_M=M/sqrt(-M.M) exists for positive-mass future timelike material currents.
The charge frame U_Q=Q/sqrt(-Q.Q) exists only when Q is nonzero timelike.
Equal-sign charged future timelike currents guarantee this locally; opposing
charges can produce Q=0 or spacelike Q while M remains timelike. For example
equal proper densities with N_+=(gamma,gamma v,0,0) and
N_-=(gamma,-gamma v,0,0) give Q=(0,2q gamma v,0,0). Thus a conserved charge
current does not automatically supply a valid material frame.

Choosing U_M in L_medium makes neutral f participate in its constitutive
variation. For species a,

    delta U_M^mu = [delta^mu_nu+U_M^mu U_M_nu]
                    m_a delta N_a^nu / sqrt(-M.M).

Unless partial L_medium/partial U_M and relevant cross derivatives vanish,
this is a non-gravitational force/inertia contribution for f even when q_f=0.
On a common rest, pure-electric background some first variations vanish,
but reciprocal perturbative mixing remains; RTM itself exhibits it. Calling
that neutral species gravity-only for arbitrary motion is not justified.

A frame built only from charged stocks, or an independent material support
current, can exclude direct neutral participation only if the OTHER medium
arguments (including n_*) also exclude f. The frame must still be varied
and stay timelike/nonzero, and the support stock must be counted. In the
four-stock witness, U_Q can serve on its nonzero finite-density domain and
f is absent from it. In opposite-charge recombination the charge frame can
fail as stocks cancel or deplete. None of these choices inherits the
single-current RTM wave/cone certificate: extra relative-current and reaction
modes require their own quadratic action and admissible-domain check.

## 8. Dependency and obligation record

| obligation | status | reason |
|---|---|---|
| Exact old P_t identities with nonuniform local S | failed | equation (1) |
| Two-species neutral f with conserved q_t>0 | failed | q dot nu!=0 |
| Conservative reaction/current extension | passed, conditional model | (3)-(5), counted stocks |
| Rest-mass identity for actual neutron portal | failed as stated | exact mass defects above |
| Full energy/charge/momentum bookkeeping contract | passed | varied total action and collision invariants |
| Critical q/m for emitted S | failed | actual mass mismatch |
| Permanent one-way unbinding/no capture | not established | inverse reaction and stock transport unresolved |
| Neutral f gravity-only with total mass frame | conditional/usually failed | constitutive current variation |
| Multi-current health and finite-density exit | not established | new modes and possible frame failure |
| Bound retained remnant/core profiles or fits | out of scope | requires live distributions and potentials |

The universal parts are direct algebraic and variational proofs above. The
small exact calculation checks their implemented normalization and specific
mass/charge examples; it does not prove physical existence or a uniform
causality theorem. The sources, code, arithmetic domain, cap, versions, hashes
and actual exit status are pinned by `contract.json` and `run_v4/manifest.json`.

**First unresolved implication:** derive a selective interaction and receiver/
opposite-charge transport history which depletes the halo's actual charged
source, suppresses the inverse process, and deposits an occupied neutral
distribution bound by the changing TOTAL potential, while its entire
multi-current action stays on a healthy finite-density domain. A local
positive tether-frame energy flag does not supply this implication. The
four-stock action demonstrates conservative possibility after enlarging the
inventory; it cannot be promoted to S4 or an observational closure without
that derivation.
