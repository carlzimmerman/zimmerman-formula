# CT09 charged microphysics

Checkpoint: base Git `285353a57bc1c21662c5565830bbc97ac5b0f7f9`;
actual executed source hashes are in each fresh v2 manifest and `SOURCE_PINS.json`.
Only this package was written. Earlier TP06/TK08 science is read-only ancestry.

The charged population has genuine microscopic exits, but the combined vacuum,
charged-relic and photino history remains unresolved. A neutral first daughter
alone is insufficient evidence of pair loss. Conversely, the displaced cascade
and a late charged-scalar resonance really can remove charged pairs. Neither
result establishes removal of the energy into radiation.

## Charges and populations

The residual U1 charge has q^2=5/12 on broken components, which form (3,2)
and its conjugate. `network.py` adapts every exactly degenerate scalar and
Takagi block to Q^2 before using vertices. It finds 36 physical charged real
scalars, 36 charged Weyls, and excludes the twelve charged scalar Goldstones.
The initially light charged fermion branch has 12 Weyls, or 24 spin degrees.
At x>0 the lowest charged scalar branch has 12 real degrees, or one complex
(3,2) multiplet; its origin degeneracy is 24 real degrees.

Let n count particles plus antiparticles. The conserved quantity is signed
charge. A single charged fermion converting to a charged scalar and one neutral
gaugino leaves one carrier. A neutral scalar inverse decay consumes two
carriers, but its decay/cascade may return zero, two, or more carriers.
For a one-way, empty-daughter decay network define N_i as the mean terminal
charged-carrier number. Stable charged states have N=1, stable neutral states
N=0, and N_i=sum Br(i->jk)(N_j+N_k). Thus an initial neutral inverse parent
has signed pair-loss fraction eta_i=1-N_i/2. Negative eta describes pair
multiplication. This is a one-way branching statistic, not a thermal collision
operator: inverse processes and nonzero daughter occupations must subsequently
be followed.

## Tree widths and the changing lightest carrier

All masses below are in mu units, x=X/mu, e=h=lambda=.003,
g=sqrt(29/200)e, a=sqrt(2/(31e)). The light fermion is the middle signed
eigenvalue of the broken 3x3 matrix pinned in TK08. The lowest charged scalar
branch obeys

    m_C(x) = e/2 sqrt(x^2 + 2/(31e)),
    dm_C/dx = e x/[2 sqrt(x^2+2/(31e))].

The exact tree Hessian agrees with this formula at every tested point. The
fermion/scalar ordering changes at x=3.83742513487 (independent photino package).

For L=-y_ij S psi_i psi_j/2+h.c., the real-parent scalar width is the TK08
ordered Weyl expression. For unequal masses z_i=m_i/M, r_i=z_i^2,

    Gamma(S->FF) = M/(16pi) sum_ij sqrt(lambda(1,r_i,r_j))
       [ |y_ij|^2(1-r_i-r_j) - 2 Re(y_ij^2) z_i z_j ].

The ordered sum includes the identical-Majorana factor. The physical scalar
pair width is sum_ij C_aij^2 sqrt(lambda)/(32pi M), excluding charged
Goldstones. A spin-averaged Majorana fermion parent has

    Gamma(F_i->F_j S_a) = M_i/(16pi) sqrt(lambda(1,r_j,r_a))
       [ |y_ija|^2(1+r_j-r_a) + 2 Re(y_ija^2) sqrt(r_j) ].

These formulas follow directly from the two-body phase-space integral and
spin sum. They also reproduce the prior charged-pair scalar widths. Degenerate
charged Majorana components are averaged, so this gives the charged Dirac
particle width without assigning an unphysical signed charge to one Takagi
column.

| x | m_F | m_C | mean Gamma(F->C+neutral F)/mu |
|---:|---:|---:|---:|
| 0 | 0 | .00695608344 | 0 |
| 3 | .00747601960 | .00828475086 | 0 |
| 5 | .01088545043 | .01022922757 | 9.58205747e-12 |
| 7.5 | .01433828522 | .01322685136 | 2.07188951e-11 |
| 10 | .01764744887 | .01653442157 | 1.72027568e-11 |
| 20 | .03153029976 | .03079589415 | 4.38133150e-12 |
| 30 | .04605013153 | .04553446054 | 1.49815128e-12 |

Each of these fermion decays leaves one terminal charged carrier in this tree
network. The rate includes the tree Goldstino in addition to the twelve raw
unbroken gauginos. The photino package separates the raw U1/SU2/SU3 rates;
their ratio is 1:1.8:3.2. The difference of about .1--1% from this table is
the Goldstino channel, not extra photino production. Physical longitudinal
gravitino interpretation requires the gravity equivalence regime.

## Displaced cascades and daughter force

`run_network001` computes all SSS and FFS decay chains at thirteen points.
At x=0 the important SU3 B scalar first produces A3+R, and A3 returns charged
carriers; the low-parent cascade is not irreversible loss. At x=3 the lowest
open octet parent instead has

    M=.01939155277, Gamma_LL=1.52972513e-10,
    Gamma_total=6.64121410e-10, N_charged=1.85731566.

It deposits .07134217 tree-stable massive neutral A3 particles per parent,
plus massless neutral daughters. Thus eta=.07134217: actual charged pair
loss occurs already here. At x=3 this low parent and all its daughters are
below vector thresholds; its SSS/FFS tree accounting is complete. Higher
parents can have scalar+broken-vector exits, which are omitted from the broad
network. Their numerical branching fractions must therefore retain the
SSS/FFS-only qualification. Unbroken-vector tree radiation from these vev
scalars vanishes because each unbroken generator annihilates the vev.

The A3 mass decreases with x. At x=3 it is .01452276 and its slope is about
-.0022546. The preceding parent therefore deposits mean massive-neutral rest
energy .00103608543 mu and mean neutral NR force -.000160849612 per parent.
The negative slope favors motion to larger x. Calling this energy radiation
would erase a physically relevant force. `run_endpoint002` serializes every
terminal daughter index, mean number, mass and mass slope, plus charged and
neutral rest-energy/NR-force sums. Actual force is (m/E) times the tabulated
NR force, so the table is not a daughter momentum distribution.

## Gauge annihilation, normalization and long-range scope

At zero relative velocity the gauge-boson annihilation color factor of a
Dirac (3,2) particle is

    C = 1/(4 d^2) sum_AB Tr[{T_A,T_B}^dagger {T_A,T_B}], d=6.

For common g and q_Y^2=5/12 the separate rational contributions are

| final generators | C contribution |
|---|---:|
| SU3,SU3 | 7/54 |
| SU2,SU2 | 1/32 |
| U1,U1 | 25/864 |
| SU3,SU2 | 1/3 |
| SU3,U1 | 5/27 |
| SU2,U1 | 5/48 |

Their sum is exactly 13/16. The physical particle-antiparticle pair cross
sections, averaged over all six gauge components, are

    sigma_pair v(F Fbar -> all unbroken VV) = 13 g^4/(256pi m_F^2),
    sigma_pair v(C Cbar -> all unbroken VV) = 13 g^4/(128pi m_C^2).

The scalar coefficient is twice the spin-averaged fermion coefficient. For
the total particle-plus-antiparticle density,

    n_dot + 3H n = -sigma_pair v n^2/2

when inverse creation is neglected. Thus the coefficient often called an
effective cosmological cross section is sigma_pair/2. The modern scalar
triplet benchmark is 7g^4/(216pi m^2) for a physical pair; the v3 paper [S1]
lists half this value in its all-particle cosmological convention. Mixed
gauge channels matter: the full coefficient is 702/25=28.08 times the
gauge-averaged pure U1 channel. None of these is an upper bound on scalar,
fermion, resonance or bound-state channels.

For isotropic independent frozen FD momenta, angular averaging gives
<1/|p-q|>=1/max(p,q). Consequently

    <1/v_rel> = (m/Tc) C_FD, C_FD=.29473891402637836.

The strongest attractive gauge Coulomb potential has
alpha_max=(4/3+3/4+5/12)g^2/(4pi)=2.59621500919e-7. For these s-wave gauge
annihilation channels only, the elementary inequality

    S(z)=2pi z/(1-exp(-2pi z)) <= 1+2pi z, z>=0,

yields sigma_0[1+2pi alpha_max(m/Tc)C_FD] as a conservative average. Repulsive
representation channels only lower this gauge result. This is not a
model-wide upper bound. It retains the 1/v growth even after velocities
redshift far below alpha; ignoring Sommerfeld at late times is unjustified.

All two tree-zero neutral real scalar modes were included in a separate
long-range exchange norm bound. With physical cubic matrices C_a restricted
to the light charged scalar block,

    alpha_scalar <= sum_a ||C_a||_op^2/(16pi m_C^2).

The bound is 8.52e-10,1.55e-9,2.38e-9,2.74e-9,2.79e-9,2.82e-9 at
x=3,5,10,20,25,30. It is about 1.1% of alpha_max near the outer packet.
It concerns only tree-massless exchange; finite-range scalar resonances
remain separate. [S2] supplies Coulomb Sommerfeld and Abelian radiative
capture formulas; [S3] shows why nonabelian capture requires its actual
transition algebra. Replacing alpha by alpha_max in an Abelian capture
formula is not a proved nonabelian capture bound. The coordinator owns the
RD/MD loss integral; this package supplies its normalized microscopic inputs.

## Charged-scalar resonance missed by a fermion-only selection

The neutral singlet mass M=sqrt(2e)=.0774596669241 persists while the charged
scalar remains lighter than the fermion. It has nonzero C Cbar residue even
after the F Fbar channel closes. The exact tree threshold is

    x_pole=sqrt(60/(31e))=25.4000254000381,
    m_C(x_pole)=M/2=.0387298334621.

At the fixed protected radius x=24.8 the detuning M-2m_C=.00177011423mu.
It falls to 2.951214e-6mu at x=25.3990254. `run_scalar002` computes all
physical neutral-to-lowest-C-pair cubic widths, including parents closed
to light fermion pairs. Its diagnostic f_C=2/(exp(p/Tc)+1) on twelve real
scalar states preserves the original 24-spin charged number; this shape is
an assumption, not the derived fermion-decay daughter distribution.

The inverse integral is the TK08 exact two-body production integral with
the scalar occupations inserted. A 96/192-node repeat agrees within
3.88e-6; its MB limit is independently checked. At x=25.3990254,Tc=.0005mu,
the diagonal empty-daughter net-loss diagnostic is about 7.44e3 H for the
protected packet. At x=24.8 it is about 1.26e-7 H. These values show why a
near-pole history must be examined. They are not final depletion factors.

There are FOUR exactly degenerate singlet real modes. Individual branching
fractions in an arbitrary mass basis are not physical when their widths
overlap. Therefore `run_scalar002`'s per-basis net-loss factors are explicitly
diagnostic. The total absorbing inverse production, proportional to the
trace of the C-pair production matrix, is basis invariant. A coherent
calculation is required for a physical narrow-pole loss rate.

## Coherent pole calculation

`run_pole002` computes the complete leading-tree absorptive matrix at the
pole. All massive-vector exits are kinematically closed; unbroken-vector
tree exits vanish. All charged two-body exits are closed at exact threshold,
including the heavier fermion branch. Every allowed tree daughter and its
cascade remains neutral. The result removes charged pairs, while depositing
both massive neutral adjoints and massless neutral states.

Let C_aij be the cubic coupling of singlet a to the twelve real light
charged states and define

    G_ab=sum_ij C_aij C_bij/12^2,
    Gamma_C(s)=12^2 G beta_C(s)/(32pi sqrt(s)),
    D(s)=[(s-M^2)I+i M (Gamma_other+Gamma_C(s))]^-1.

The physical-pair, six-component averaged inclusive neutral-exit cross
section, in the narrow near-threshold tree packet, is

    sigma_pair v = 2/m_C Tr[G D Gamma_other D^dagger].

This follows by integrating the decay final states, whose absorptive tensor
is 2sqrt(s)Gamma_other, with incoming flux 4E^2. At E=m_C it reduces to

    sigma_pair v(0)=2/(m_C M^2) Tr[G Gamma_other^-1].

The measured dimensionless width eigenvalues are

    Gamma_other/mu=(1.305574536,1.335771063,2.428356032,2.500655228)e-9.

The effective production residue is 2TrG=9.14754162331e-9 mu^2. The
normalized commutator of G and Gamma is .0016888, so independent diagonal
Breit-Wigner curves would not be exact. The matrix result is

    sigma_pair v(0)=15741.99983725 mu^-2,
    sigma_pair v(0)<=30151.28622873 mu^-2

where the latter follows from replacing Gamma_other^-1 by the inverse
smallest width eigenvalue. It is an upper bound for this pole packet,
not for all annihilation channels. A fixed orthogonal basis rotation
reproduces the matrix cross section to floating precision. The complete
4x4 matrices and the velocity curve are serialized for the coordinator's
late-time integration. The coordinator supplied a sharper uniform matrix
inequality, independently checked here. With Gamma_tot=Gamma_other+Gamma_C
positive and any Hermitian detuning/mixing matrix H, whitening by Gamma_tot
gives

    D Gamma_other D^dagger <= D Gamma_tot D^dagger
      <= Gamma_tot^-1/M^2 <= Gamma_other^-1/M^2.

Positivity of G bounds the entire fixed-pole-packet curve by
15741.99983725 mu^-2, with equality at H=0,Gamma_C=0. This controls coherent
detuning and velocity for the fixed leading-tree matrices, not other
channels or arbitrary coupling changes. The finite peak does not by itself
prove a relic floor; expansion history, mass evolution and other channels
still matter.

`run_medium001` splits the width into SSS and FFS matrices. The bosonic
SSS matrix is strictly positive definite, with eigenvalues/mu

    (5.151330594e-11,1.426686436e-10,1.818089153e-9,1.884197191e-9).

There is no production overlap with a bosonic-width null space. Turning
off every FFS decay channel gives the uniform fixed-pole bound

    sigma_pair v <= 2/(m_C M^2) Tr[G Gamma_SSS^-1]
                 =97360.19095551 mu^-2.

It is 6.185 times the vacuum-width result. Ordinary final-boson stimulation
cannot reduce the vacuum SSS width. This bound permits arbitrary positive
Pauli suppression of FFS widths; it is not a theorem about a general
nonequilibrium retarded self energy with gain. Inverse neutral processes
still belong in an actual collision history.

The relative width is O(2e-8), comparable to weak one-loop mass shifts
e^2/(16pi^2)=5.7e-8. A physical resonance must be retuned after computing
the pole-mass shift; tree x_pole is not a precision gravity tuning claim.

## Direct charged-fermion exchange into gaugino pairs

The separate process C Cbar->lambda_alpha lambda_beta, with alpha,beta
among all twelve raw unbroken gauginos, both removes charged pairs and
can produce photinos. Its daughters have energy of order m_C, not the
small F-to-C decay mass splitting. The direct one-photino-per-fermion
conversion branching ratio therefore cannot bound all photino sources.

For this direct t/u contribution a generous finite coefficient bound is
available without evaluating every interference term. The Casimir sum is
C_total=4/3+3/4+5/12=5/2. Completeness of all charged fermions gives, for
each normalized complex charged scalar particle, the total vertex norm
over the twelve gauginos and both chiralities

    L=sum |Y|^2=2 g^2 C_total=5g^2.

The six complex charge eigenstates constructed from the real light scalar
subspace give this value independently at six x points in `run_tchannel002`.
On the stable scalar branch each internal charged fermion has M_I>=m_C.
For equal-mass incoming scalars and massless outgoing gauginos, both
external particles have CM energy E. The t/u exchange momentum has q0=0,
and the Euclidean spinor-operator norm is exactly

    ||(qslash+M_I)/(q^2-M_I^2)||=1/sqrt(|q|^2+M_I^2)<=1/m_C.

This uses anti-Hermiticity of spatial Dirac matrices; explicit matrices
provide a numerical control. External massless spinors have norm sqrt(2E).
For each fixed final-helicity assignment, Cauchy-Schwarz over the internal
fermions bounds either diagram's final-flavor Frobenius norm by 2EL/m_C.
Adding t and u with the triangle inequality, then conservatively allowing
four helicity assignments, yields sum|A|^2<=64E^2L^2/m_C^2. The two-body
phase space and Moller flux give

    sigma_pair v_M <= sum|A|^2/(32pi E^2)
                   <= 50g^4/(pi m_C^2)
                   = (6400/13) sigma_gauge,scalar.

The factor6400/13=492.3076923 is deliberately loose: ignoring identical
Majorana final-state factors only increases the bound. It is uniform in
CM velocity in the massless-gaugino approximation, and contains no possible
spacelike internal pole. At the singlet radius it is 1.80696565e-8 mu^-2,
far below the coherent singlet-pole peak. This is a bare tree t/u bound,
not a bound on a scalar s-channel pole, heavy neutral fermions, Goldstino
channels, or all Coulomb partial waves. An NR short-distance s-wave
Coulomb enhancement can be treated separately; a full gaugino daughter
distribution and exact interference cross section were not computed.

## Weak-regime scaling and next obligations

At fixed ratios h/e=lambda/e=1,g/e=sqrt(29/200), changing e while keeping
sqrt(e)x fixed gives m proportional to sqrt(e), Yukawa proportional to e,
cubic proportional to e^(3/2), and widths proportional to e^(5/2). This
follows by rescaling the valley fields in the exact component model.
`run_controls001` checks e=.001,.003,.01: the pole mass divided by sqrt(e)
is .70710678119 and the width trace divided by e^(5/2) is
.01535724155419 at all three points. The pole peak scales as 1/e at fixed
mu, while its velocity width scales as e. These are microscopic scaling
relations; mu and initial abundances need not stay fixed in gravity
families. No conclusion for the entire weak regime follows from one packet.

Remaining physical leaves are: a coupled source/daughter distribution with
neutral occupation forces; the remaining charged-scalar finite-range
annihilation channels and exact gaugino-pair momentum source beyond its
conservative direct-exchange bound; nonabelian bound-state formation;
loop radiative exits of the neutral
adjoints; scalar/fermion/vector channels omitted from the broad cascade;
and any gravity retuning/pole corrections needed for a late resonance.
These routes are open, not exhausted. A scalar resonance or neutral stable
daughter does not by itself solve the photino abundance or coldness problem.

Primary-source checks are recorded in `SOURCES.md`. No external source was
used to replace the model-specific component vertices.
