# Charge-conserving tether action and its restrictions

Conventions: rationalized (Heaviside) gauge units, c=1 in action formulas. G is
Newton's constant. Restoring hbar,c is explicit in microscopic formulas. This
is a proposed effective action constrained by the adopted acceleration law,
not a derivation of that law or its acceleration scale a0 from nature.

## 1. Inventory and normalization

Use neutral F, positive T of mass m and charge q, negative C of mass epsilon*m
and charge -q, and neutral baryons. A reaction must conserve N_T-N_C. Global
neutrality requires N_T=N_C if no other charged population or boundary flux exists.

At weak field, two T carriers repel with q²/(4pi r²). The old tether energy has
weak-field pair potential +G m²/r. Matching it fixes

    gamma=q/m=sqrt(4pi G),
    alpha_G=q²/(4pi hbar c)=Gm²/(hbar c),
    q_C/m_C=-gamma/epsilon.

The microscopic charge coupling is therefore NOT independent of m. A light
negative population is dynamically more responsive, not innocuous. The total
charged mass per pair is (1+epsilon)m. If the original reservoir ratio eta=5.364
is retained, it refers to total T+C mass, not T mass plus a free extra reservoir.

## 2. Electric action from the fixed spherical function

Define D0=a0/gamma. With D the electric displacement, choose

    h(D)=D0² w(|D|/D0), w(z)=-log(1-z)-z, 0<=z<1.

Its conjugate physical electric field is

    E=partial h/partial D = D/(1-|D|/D0).

The Legendre transform is fixed, not a fitted interpolation:

    ell(E)=D.E-h(D)=D0|E|-D0² log(1+|E|/D0),
    D=partial ell/partial E=E/(1+|E|/D0).

A preferred-frame gauge-invariant candidate has L_field=ell(E)-B²/2,
E=-grad phi-partial_t A and B=curl A, with minimal matter coupling
sum_i[q_i v_i.A-q_i phi] and Newtonian gravity. Its field energy is h(D)+B²/2.
This exhibits gauge and time-translation symmetry, but is NOT asserted to be
a causal Lorentz-invariant theory. The relativistic check in section7 fails for
the simplest single-invariant extension of this electric branch.

Electrostatic variation gives

    div D = rho_q = gamma(rho_T-rho_C/epsilon),
    curl E=0.

In acceleration units d=gamma D and e=gamma E,

    div d=4pi G(rho_T-rho_C/epsilon), e=d/(1-|d|/a0), curl e=0.

In general curl d is NOT zero. This replaces the previous imposed longitudinal
displacement model. The variational 3D field is solved here for finite smooth
manufactured sources. The nonlinear energy is positive/convex, but positivity
alone does not establish a relativistic completion or stability with gravity.

For electrostatics U=integral h(D)=integral[rho_q phi-ell(E)] on a stationary
solution. Differentiating with respect to a smooth source position gives
partial U/partial x_i=integral phi partial rho_q/partial x_i. Equal charges
repel and opposite charges attract in the tested configurations. Scalar-field
source energy is not substituted for this constrained gauge-field Hamiltonian.

## 3. Charge-conserving conversion and energy

For separate complex scalar matter fields, one illustrative gauge-invariant
vertex is lambda F T_dagger C_dagger+h.c., with stabilizing matter interactions
required in a complete action. The two outgoing charges sum to zero. Gauge
invariance fixes the charge relation, not lambda or the neutral-state mass M_F.

If M_F>m+m_C, a free F can decay into T+C, with rest-frame tree-level width

    Gamma=|lambda|²/(16pi M_F) sqrt(Kallen(1,m²/M_F²,m_C²/M_F²)).

Kallen(1,a,b)=(1-a-b)²-4ab. This is for distinguishable scalar daughters and
canonical relativistic normalizations; hbar=c=1. A universal free decay alone
has no galaxy-type selection. If M_F<m+m_C, ionization needs incoming energy;
the inverse needs a photon/third body to carry away excess energy and momentum.
No radiative matrix element is fixed by merely writing the cubic vertex.

For any event the required ledger is

    Delta K + Delta U_g + Delta U_field + Delta(rest/internal energy)
      + Delta E_radiation = 0,
    Delta Q = 0.

The gravitational mass change and countercharge transport cannot be discarded
while claiming exact energy accounting. We do not run invented conversion rates.

To avoid a new gap and vertex, one can try identifying F with a T-C Coulomb
bound state. Then mu=epsilon*m/(1+epsilon),

    B_bind=mu*c²*alpha_G²/2, a_B=hbar/(mu*c*alpha_G).

Those are controlled Coulomb expressions only when the atom lies outside the
nonlinear constituent-core regime. The bound F is neutral; ionizing F creates
the repulsive charged component and its countercharge. This reverses the earlier
identification of recombined atoms with T. There is no new fitted gap here.

Gauss's law and |d|<a0 require every enclosing sphere of a charge m to obey

    Gm/r² < a0, hence r > r_core=sqrt(Gm/a0).

The action does not admit an arbitrarily small classical point-charge source.
Applying the hydrogenic formula at a_B<<r_core is invalid, not a discovery of
strong binding. The scan imposes a_B>10 r_core and alpha_G<.1 before drawing
any Coulomb conclusion. The microscopic structure of the core remains open.

## 4. Countercharge cannot remain a cold, stationary hidden spectator

For a spherical outward field with e>0 and inward gravity g>0,

    a_T=-g+e, a_C=-g-e/epsilon.

Cold stationary T requires e=g, whereas then a_C=-(1+1/epsilon)g<0. Thus both
species cannot be simultaneously cold and static in the same tethered region.
Counterpressure, rotation, transport, escape, or another force must be solved.
This statement does not exclude pressure-supported or rotating equilibria.

For a homogeneous neutral weak-field plasma with equal number densities n,

    omega_p²=n q²(1/m+1/m_C)=4pi G rho_T(1+1/epsilon),
    lambda_D^-2=n q²(1/T_T+1/T_C).

Temperatures here mean k_B*T. The Debye expression assumes a dilute Maxwellian
thermal response; it is not a collisionless irreversible-damping theorem.
The uniform nonlinear mode satisfies Ddot=-J and Jdot=omega_p² E(D), so

    H_mode=J²/(2 omega_p²)+h(D)

is conserved. Our dynamic tests include both species in omega_p, and show
oscillations rather than falsely assigning damping to a conservative mode.

Using the SAME virial proxy in all four mass/radius families,
rho_dark=3 eta Mb/(4pi b³), v0²=G(1+eta)Mb/b,
T_T=T_C=(1+epsilon)m v0²/6, t_dyn=sqrt(b³/[G(1+eta)Mb]), one obtains

    lambda_D/b = (1+epsilon)/6 sqrt((1+eta)/eta),
    omega_p*t_dyn = sqrt(3 eta/[epsilon(1+eta)]).

Mass and radius cancel exactly. This minimal virial screening/response mechanism
does not distinguish the numeric families. A common local bulk rotation also
does not alter the electrostatic relative-mode equations. Full magnetic dynamics,
velocity gradients, evolving distributions and assembly could change outcomes;
they are not represented by this local electrostatic test.

## 5. Countercharge contamination of the acceleration relation

Let r=N_C(<R)/N_T(<R), so countercharge mass is epsilon*r times T mass. For
0<=r<1 and cold spherical T equilibrium, put u=GM_T(<R)/R². Then

    d=(1-r)u, g=g_b+g_F+(1+epsilon*r)u,
    e=g, d=a0*g/(a0+g).

Thus with A=(1+epsilon*r)/(1-r) and S=g_b+g_F,

    S=g-A*a0*g/(a0+g),
    g=[S+a0(A-1)+sqrt((S+a0(A-1))²+4a0*S)]/2.

Local neutrality r=1 cancels the electric monopole and cannot support this
cold repulsive branch. For r>1 its sign reverses. At r=0 the old relation
g=law(S) is recovered; the missing countercharges must be elsewhere, not deleted.

For g_F=0, g0=law(g_b), x=g0/a0>0, t=10^delta, requiring g<=t*g0 gives

    A-1 <= x*(t-1)*(x+1+1/t)/(1+x) = Z,
    r <= Z/(1+epsilon+Z).

At zero tolerance r=0; at small x the allowed enclosed negative-charge fraction
vanishes proportionally to x. This is a cold spherical necessary condition,
not an observed nonspherical disk constraint. Allowing additional free mass
would generally tighten it in this branch. Countercharge pressure or nonstatic
T changes the assumed force balance and must be tested separately.

## 6. Energy needed to move countercharge outside

Even in the weak-field limit, a positive thin shell of charge q_tot at R and
negative shell at L>R store external electric energy

    U_ext=q_tot²/(8pi)*(1/R-1/L).

For q_tot=gamma M_T this is G*M_T²/2*(1/R-1/L). The nonlinear h(D) is at least
D²/2 and increases this field-energy cost for the same displacement. Separating
charge cannot be a free state toggle. Gravity, conversion rest energy, radiation
and countercharge kinetic energy determine whether separation can actually occur.

## 7. Relativistic consistency check of the simplest extension

Take the Lorentz-invariant, single-invariant ansatz L(S), S=(E²-B²)/2, agreeing
with ell(E) on a purely electric background E0>0. Consider a perturbation with
k perpendicular to E0 and electric polarization parallel to E0. Its electric
kinetic coefficient is ell''(E0), while its magnetic gradient coefficient is
L_S=ell'(E0)/E0. The small-amplitude speed therefore satisfies

    v²/c² = [ell'(E0)/E0]/ell''(E0) = 1+E0/D0 > 1.

It has positive electric kinetic coefficient but lies outside the Minkowski
light cone. This fails the usual subluminal-propagation requirement for this
minimal L(S) extension. We have not proved a theorem for all multi-field,
derivative-dependent, medium, or preferred-frame completions. The static action
and numerical energy tests do not cure this problem.

## Evidence and remaining degrees of freedom

The charge magnitude and nonlinear field scale are tied to G,a0,m; the negative
charge is fixed; the electric interpolation is fixed by the target spherical
relation. Remaining inputs are m, epsilon, a microscopic core/completion, and
(unless F is a controlled bound state) its gap and reaction coupling. Initial
distributions, abundance and radiation are physical inputs, not type switches.

General gauge-field conventions: David Tong, original QED lecture notes,
https://www.damtp.cam.ac.uk/user/tong/qft/six.pdf . Dark plasma simulations show
why charged carriers require collective dynamics rather than only binary-rate
estimates: https://arxiv.org/abs/2411.11958 . These sources do not establish our
constitutive law, derivations, observational viability or new numerical results.
