# TK08 fixed occupation and actual kinetic obstruction

## State, mass and source

Take e=h=lambda=.003, g=sqrt(29/200)e, mu=sqrt(f), and x=X/mu.
On the rigid valley a=sqrt(2/(31e)), b=x. The broken signed Weyl matrix is

    M(x)=[[ex/2,-ea/2,5ga],[-ea/2,0,5gx],[5ga,5gx,0]].

The middle signed eigenvalue is zero at x=0 and positive for x>0 in the
tested domain 0<x<=200. Its twelvefold multiplicity gives 24 spin degrees,
equivalently six Dirac components transforming as (3,2) and conjugate.
Residual GUT-normalized U1 charge squared is 5/12, independently checked
in the full 73-Weyl component model. Mass mixing does not remove this charge.

At the origin the zero vector is proportional to (0,-5ga,-ea/2). Its
gaugino probability is .064516129, and

    m_x(0)=2(5g)(5ga)(ea/2)/[(5ga)^2+(ea/2)^2]
          =.002806451612903225.

Here m denotes the dimensionless eigenmass in mu units. At x=5,10,25,
m=.01088545,.01764745,.03874730. The derivative approaches e/2 at large x;
using eX or a constant slope would distort the intermediate force.

Assume f(q)=1/(exp(q/Tc)+1), with comoving occupation preserved and physical
momentum scale Tc proportional to a_FRW^-1. This is a stated initial
distribution, not a reheating or thermalization result. For gspin=24,

    rho=24/(2pi^2) integral dp p^2 f(p) sqrt(p^2+m_phys^2),
    rho_X=24/(2pi^2) integral dp p^2 f(p) m_phys m_phys,X/E,
    P=24/(6pi^2) integral dp p^4 f(p)/E.

The physical energy and force are positive for x>0. The field equation is
62 Xddot+186H Xdot+V_X+rho_X=0. Its energy loss is precisely the source
gain: rho_dot+3H(rho+P)=rho_X Xdot. In the nonrelativistic limit the force
is n m_phys,X, with no Boltzmann suppression. A field-independent origin
energy subtraction is allowed in a plotted potential, but all particle
energy must remain in cosmological bookkeeping. This energy functional and
its nonrelativistic restoring force agree with Kofman et al., Eq.(2.10);
their particle-creation initial state is not imported here [S1].

At m<<Tc, rho(X)-rho(0)=24 m_phys^2 Tc^2/48+..., so the origin curvature
is 24 m_X(0)^2 Tc^2/24. Thus a frozen distribution does not by itself evade
the equilibrium origin instability. The useful effect occurs away from
the origin. The frozen-only curvature cancellation occurs at Tc/mu
.005120597; retaining other equilibrium species changes the full profile.

## Finite stationary and dynamical controls

`run_stationary_002` uses exact neutral tree SUGRA plus the complete rigid
one-loop CW potential. Local finite two-loop fits are not extrapolated.
Tc/mu spans .0001--.01 and x spans 0--200. Both the frozen-only potential
and a diagnostic hybrid retaining all other species in ideal equilibrium
have finite-X minima through the equilibrium gap. At Tc/mu
.004,.003,.002,.001,.00064, the canonical frozen-only minima are
x = 3.4770,5.7499,8.7884,14.7851,18.7293. Protected minima are
3.4754,5.7472,8.7799,14.7198,18.5066. These are numerical stationary
minima in the tested domain, not a phase-transition or complete-history
theorem. The hybrid closure is not a consistent kinetic solution.

`run_roll_001` integrates the homogeneous frozen-only system, with chosen
initial x equal to the equilibrium origin spinodal, zero initial velocity,
and initial xi=Tc/T_SM=.02. The visible g*=106.75 bath expands explicitly;
other massive hidden species are omitted. For 250 origin-roll times,

| embedding | initial x | largest x | H/origin-roll rate | fractional cooling |
|---|---:|---:|---:|---:|
| canonical | .2689499 | 2.9048930 | 2.27649e-8 | 5.69117e-6 |
| protected | .1844426 | 2.9318131 | 7.58582e-7 | 1.89592e-4 |

Two integration tolerances agree on the maximum excursion within 1.2e-7.
The energy plus integrated Hubble loss drifts by less than 2.1e-9 of the
initial particle energy. The origin-roll rate is approximately
1.825e-6 mu, much faster than H. This run establishes a bounded first
collisionless excursion. It does not span the Hubble cooling interval to
outer-vacuum reappearance; assigning it that meaning would be incorrect.

## Actual interactions and why equilibrium is not automatic

`neutral_rates.py` projects both superpotential Y and gauge Yukawa vertices
onto the twelve charged light eigenstates. `branching.py` independently
adapts the entire scalar and Takagi fermion bases to residual U1 charge
squared. Their light-pair partial widths agree within 1e-9 relative.

For L_int=-1/2 y_ij S psi_i psi_j+h.c., the real-scalar equal-mass width is

    Gamma=M/(16pi) sqrt(1-4r)
      sum_ij [abs(y_ij)^2(1-2r)-2 Re(y_ij^2)r], r=m^2/M^2.

The ordered Weyl sum includes the correct identical-Majorana factor; an
off-diagonal Dirac pair appears twice and gives y^2 M/(8pi) when massless.
Physical scalar pair widths use the ordered cubic sum divided by 32pi M.
The twelve charged Goldstone zero modes are excluded; neutral collective
zeros remain physical. Loop/gravity shifts to these heavy masses and widths
are outside the leading tree kinetic accuracy.

At x=0, sixteen SU3 B real scalars have M=.02782433mu and individual
Gamma(S->light charged pair)=3.48786786e-10mu. Six SU2 B real scalars have
M=.04173650mu and individual width 7.84770269e-10mu. Two heavier singlet
modes also couple. If the parents are kept in zero-chemical-potential
equilibrium, gamma_D=M^2 Tc Gamma K1(M/Tc)/(2pi^2). At Tc/mu=.00466 the
loss normalization 2 sum gamma_D/n_light is 7.48206e-6 GeV canonical and
2.49623e-4 GeV protected: Gamma/H=330.66 and 9.91. It is only 7.53e-6 of
the origin-roll rate. This detailed-balance normalization uses Boltzmann
parents and unblocked decay widths; small quantum-statistical corrections
do not make it a precision collision operator. Most importantly, the parent
chemical potential cannot simply be set to zero without following its exits.

The dominant SU3 B neutral scalar exit is S_B3->S_A3+R, with individual
width 2.71193650e-10mu, where R is massless at tree order and
M_A3=.02199707mu. `run_cascade_002` then finds

    Gamma(S_A3 -> charged scalar + conjugate)=6.10159051e-10mu,
    each charged daughter mass=.00695608mu.

All tree scalar/fermion neutral exits of this SU3 octet are numerical zero
(below 1e-39 mu). Broken-vector final states are closed by mass; unbroken
vector final states have no vev-induced tree coupling for this lightest
SU3 scalar. Loop-mediated radiation exits remain uncomputed. Thus this
apparently neutral branch returns to charged carriers promptly, rather
than establishing irreversible annihilation. At displaced x additional
neutral fermion/scalar branches open, and their subsequent cascades must
also be followed. The total widths and all immediate scalar daughters are
serialized; no cascade is silently renamed radiation.

Direct U1 annihilation to two massless U1 photons has the existing-charge
nonrelativistic cross section sigma v=pi alpha_Y^2/m^2,
alpha_Y=g^2(5/12)/(4pi). It follows by crossing/detailed balance from the
Breit-Wheeler cross section [S2]. This channel is included only where
m/Tc>3. It is not an upper bound on nonabelian, scalar-resonant or other
annihilation processes.

## Nonthermal scalar resonances on the conditional branch

An equilibrium massive-FD population must not replace the actual assumed
frozen f0(p). For a neutral scalar with mass M>2m, isotropy and the two-body
decay phase space give the exact unblocked inverse production integral

    gamma_inv=Gamma(S->LL) M/(2pi^2)
       integral dP P^2/E_S [1/2 integral_-1^1 dc f0(p1)f0(p2)],
    E1,2=E_S/2 +/- P sqrt(1-4m^2/M^2)c/2,
    p1,2=sqrt(E1,2^2-m^2).

With Boltzmann distributions exp(-E_i/T), the angular product reduces to
exp(-E_S/T) and recovers gamma_D exactly. The numerical MB limit agrees
within 4.3e-12 relative, and 64/128-node repeats within 1e-5 on the tested
curve. We set parent occupation to zero and count every produced parent as
irreversibly absorbed: this deliberately overstates loss for this set of
on-shell scalar channels. For f0<=1/2, adding a real parent population does
not increase net forward loss after its inverse decay is included.

| Tc/mu | canonical maximum loss/H | protected maximum loss/H |
|---:|---:|---:|
| .004 | 1927.1 | 57.71 |
| .003 | 4931.9 | 147.33 |
| .002 | 8.91e-8 | 2.67e-9 |
| .001 | 8.14e-18 | 2.12e-19 |
| .00064 | 1.02e-24 | 9.81e-27 |

These rates use the frozen-only stationary x(Tc) with its number held fixed.
They show that early resonances can matter over a Hubble interval, while
the same on-shell channels are strongly suppressed after x increases.
They do not bound all annihilation, prove the population is depleted,
or allow one to evolve abundance while leaving the restoring force fixed.

## Coldness, charged relic and first missing calculation

The assumed conserved occupation becomes kinetically cold when m/Tc>>1;
the table reaches 46 near Tc/mu=.00064. These particles are heavy charged
messengers, not the light neutral photino. With xi=.02 and g_SM=106.75,
the undepleted initial charged yield is 3.74544e-7 per visible entropy.
The root full charge classification finds that the outer-vacuum lightest
charged particle is instead a scalar (23.2 TeV canonical or 688 TeV protected).
The light fermion can decay into this stable charged companion. Exact
signed U1 charge does not conserve particle-plus-antiparticle number;
annihilation could remove pairs, and must be calculated.

One further finite force-budget control at Tc/mu=.002 uses the leading
T0+other-species-equilibrium force. It is outward at all 1151 tested points
0<=x<=200. For each charged species, a particle exerts at most
abs(dm_phys/dX), since m/E<=1. The fermion bound is the operator norm of
the signed mass-matrix derivative; the physical scalar bound is
norm(H_X)/(2m_min), with the charged Goldstone excluded; the vector
derivative is explicit. These deliberately conservative pointwise bounds
give a necessary additional charged yield for any stationary trap in this
prescribed family. The smallest grid values are 1.16183e-10 canonical and
5.13655e-11 protected, both at the x=200 endpoint. Using the explicit
comparison rho_DM/s=.44e-9 GeV and a 10% charged rest-density allowance,
the corresponding relic yield gates are 1.89607e-15 and 6.39858e-17.
The necessary supporting population exceeds these gates by 6.13e4 and
8.03e5. This finite-grid/prescribed-force tension is not a global bound
beyond x=200 or an exclusion of support from frozen neutral daughters,
nonstationary capture or later all-channel annihilation.

No final photino abundance or free-streaming prediction has been derived.
The first missing coupled calculation is f_charged(p,t), charged scalar
populations, neutral resonances/cascades and the field X(t), including
their source energy and changing force during the early .004--.003mu
window. The late frozen resonance suppression makes that early window
decisive. A second missing leaf is the actual irreversible neutral/radiation
exit of each cascade, rather than its first neutral daughter. This is a
conditional first-roll/force success and an unresolved production history,
not a solution of the combined DE/cold-matter objective.

## Sources and provenance

[S1] Kofman et al., *Beauty is Attractive*, hep-th/0403001v2, Eq.(2.10),
explicit occupation-weighted energy and nonrelativistic restoring force;
the following discussion stresses the separate annihilation/decay obligation:
https://arxiv.org/pdf/hep-th/0403001 . Accessed 2026-11-04. Model-specific
masses, FD assumption, mode count and integration are derived here.

[S2] Esnault et al., *Electron-positron pair production in the collision of
real photon beams with wide energy distributions*, arXiv:2103.09099,
Eq.(2), used solely for the crossed tree QED channel:
https://arxiv.org/pdf/2103.09099 . Original primary calculation:
Breit and Wheeler, Phys.Rev.46,1087 (1934),
https://doi.org/10.1103/PhysRev.46.1087 . Accessed 2026-11-04.

Each contract JSON contains the exact input closure and software versions;
each run manifest contains argv, limits and before/after hashes. Successful
records are stationary002, rates001, branching002, roll001, audit001,
cascade002, nonthermal002 and force_budget001. The original failed sources are retained
byte-for-byte under `inputs_historical/`, with SHA-matched archive mapping.
