# A concentrated Q packet: small weak residuals, nonzero flux defect

2026-09-30 22:31 UTC pass. Root proof frozen before new author/reviewer proof
or formula previews. Task041 proposes a localized traveling packet; this proof
specifies its scaling and checks each residual. Pure analytic construction,
no numerical run or imported mechanism. All background/physical coefficients
are the same reviewed fixed-reference Q model, with C=4piG and tau>0.

## Packet and domain

Let rho,phi0,chi0 be the static crossing on fixed interval I. Put g0=phi0_x,
a(x)=a_ref exp chi0, B0=B(g0,a). Choose a closed time slab [0,T] and trajectory
X(t)=x0+v t wholly inside a compact regular subinterval on ONE side of the
crossing, with a fixed positive distance to its ends and both physical walls.
Here v=1/sqrt(tau)>0, derived from the actual potential inertia and Q's
large-gradient coefficient, not identified with a metric light speed. Such a
T>0 is possible for any finite positive tau. Fix physical L>0, potential unit
Phi>0 and a nonconstant real F in C_c^infinity((-1,1)). For dimensionless
0<epsilon sufficiently small define

psi_e=Phi sqrt(epsilon) F((x-X(t))/(L epsilon)),
h_e=partial_x psi_e=(Phi/L)epsilon^(-1/2)F',
phi_e=phi0+psi_e, u_e=partial_t phi_e=-v h_e,
n_e=rho, j_e=0, chi_e=chi0, w_e=0.                         (1)

All actual field walls, matter mass and impermeability are preserved, scale
cap is exact, and the packet never touches the background cusp. The background
retains its inherited crossing regularity; perturbations are smooth and the
full fields are smooth on the packet's support. No global C2 claim about the
background cusp is needed. These are approximate states, not exact solutions.

Let A0=(Phi²/L)int F'^2>0. Uniformly in t,
int h_e²=A0, int |h_e|=O(sqrt(epsilon)),
||psi_e||infinity=O(sqrt(epsilon)), ||psi_e||2=O(epsilon).
The spacetime tube supporting the packet has measure O(epsilon). Thus h_e and
u_e converge weakly in L2 to0: pairing with any fixed L2 test is bounded by
a fixed L2 norm times the test's L2 mass on that shrinking tube. The latter
tends to zero. Potentials converge uniformly to phi0; density and scale are
unchanged. For any continuous compactly supported test zeta,

int h_e² zeta dxdt -> A0 int_0^T zeta(t,X(t))dt.            (2)

This follows by x=X(t)+L epsilon y and uniform continuity/dominated bounds on
compact sets. The same formula holds at each fixed time. Denote this moving
measure by A0 delta_X, with time Lebesgue measure understood.

## Exact Q bounds and residuals of every equation

Write B(g,a)=sgn(g)b(|g|,a), W_s=b and T=-W_chi. Global Q bounds are

|B(g,a)-g|<=a/2, |B(g,a)|<=|g|,
|W(|g|,a)-g²/2|<=a|g|/2,
S(g,a)=B(g,a)g-W(|g|,a), |S-g²/2|<=a|g|,
|T(|g+h|,a)-T(|g|,a)|<=a|h|/2.                            (3)

The first follows directly from b=(sqrt(a²+4s²)-a)/2; integration gives the
W bound. The S bound follows by adding s(b-s) and the W error. The T bound
uses 0<=T_s=a b/sqrt(a²+4s²)<=a/2 and evenness in signed g. All are global;
no deep-MOND expansion is used at the packet's growing gradients.

Define e_B=B(g0+h_e,a)-B0-h_e. It vanishes outside the packet tube and obeys
|e_B|<=a, hence ||e_B||_(L_infinity_t L2_x)=O(sqrt(epsilon)).
Using tau v²=1 and the exact background source B0_x=C rho, the field residual
is exactly

R_phi=tau phi_e,tt-partial_x B(g0+h_e,a)+C rho
      =-partial_x e_B.                                   (4)

For every spatial H1_0 test its pairing is bounded by ||e_B||2||test_x||2.
Thus R_phi tends to zero in L_infinity_t H^(-1)_x at the stated rate. This
does not say its pointwise or L1 norm tends to zero. Also B_e-B0=h_e+e_B,
so B_e converges weakly in L2 to B0.

Continuity residual is exactly zero. The conservative separate matter momentum
residual is

R_m=partial_t j_e+partial_x(j_e²/n_e+cs²n_e)+n_e phi_e,x
   =rho h_e,

by background hydrostatic balance, and is O(sqrt(epsilon)) in L1 spacetime,
even uniformly in spatial L1 at each time. Products exist here since rho is
bounded; this construction is distinct from FGF040's singular-density example.
The scale residual is

R_chi=sigma chi_e,tt-J chi_e,xx+U'(chi_e)-T(|g0+h_e|,a)
     =T(|g0|,a)-T(|g0+h_e|,a),                            (5)

which is O(sqrt(epsilon)) in L1 by (3). No vanishing L2 scale-residual bound
is asserted. Kinematic time/space derivative compatibilities hold exactly.
All residuals are for the actual coupled Q equations, not a Newtonian surrogate.

## Full momentum and energy, including their residuals

The FGF040 combined density/stress are
P=j-(tau u g+sigma w chi_x)/C,
Pi=j²/n+cs²n+[B g-W+tau u²/2+sigma w²/2+J chi_x²/2-U]/C.
The background has P0=0 and partial_x Pi0=0. For (1),

P_e=h_e²/(C v)+rP_e,
Pi_e=Pi0+h_e²/C+rPi_e,                                   (6)

where rP_e=tau v g0 h_e/C has L1 spacetime norm O(sqrt(epsilon)). For the
stress, tau u_e²/2=h_e²/2; compare S(g0+h_e)-S(g0) with
h_e²/2+g0 h_e using (3). On the tube the remaining error is bounded by a
constant times |h_e|+1, so ||rPi_e||1=O(sqrt(epsilon)). These bounds are uniform
in time on the selected compact trajectory region and include zeros of F'.

The leading terms cancel EXACTLY in the combined residual since
partial_t h_e²+v partial_x h_e²=0. Thus

partial_t P_e+partial_x Pi_e=partial_t rP_e+partial_x rPi_e.

For every compact spacetime test zeta the residual pairing is bounded by
O(sqrt(epsilon)) (||zeta_t||infinity+||zeta_x||infinity).
This is an explicit weak residual norm, not an L1 bound on the derivative.
No unjustified multiplication of R_phi by the unbounded packet gradient is
used to infer this: the combined residual was checked directly from its flux.

Let mathcalH be the FULL energy density, including n phi and both field kinetic
terms. Direct use of (3), bounded background and rho psi_e gives

mathcalH_e-mathcalH0=h_e²/C+rH_e,
||rH_e||_(L_infinity_t L1_x)=O(sqrt(epsilon)).              (7)

Indeed kinetic and large-gradient W each supply h_e²/(2C). The background
cross terms have L1 size O(sqrt(epsilon)), and the density interaction has
size O(epsilon^(3/2)). All other terms are unchanged. No density-potential
term is omitted. For this zero-current, static-scale ansatz the exact smooth
energy flux expression is Q_e=-B_e u_e/C=v B_e h_e/C. It obeys
Q_e=v h_e²/C+rQ_e, ||rQ_e||1=O(sqrt(epsilon)), because
B_e=B0+h_e+e_B with B0,e_B bounded. Thus the energy-balance residual also
tends to zero against compact C1 tests, by direct cancellation of the same
transported leading square. This checks an approximate balance; it does not
promote the approximants to exactly conservative solutions.

Equations (2),(6),(7) give the measure limits

P_e -> (A0/(C v))delta_X,
Pi_e -> Pi0+(A0/C)delta_X,
mathcalH_e -> mathcalH0+(A0/C)delta_X,
Q_e -> (v A0/C)delta_X.                                  (8)

Their singular parts obey the transport balances. The ordinary limiting
fields are simply the original static background, whose computed P and
excess energy vanish. Therefore these nonlinear flux/energy limits are NOT
identified by inserting the weak field limits into their formulas. The limit
background still solves its equations; this example is not a failure of that
fact. It refutes identification of nonlinear fluxes/energy from these energy
bounds and weak-residual topologies alone.

## Initial data and a vanishing-energy control

At t=0 the measure in (8) is already nonzero, at X(0)=x0. Integrated exact
total excess is A0/C+O(sqrt(epsilon)), uniformly on [0,T]. Initial phi values
converge uniformly, but gradients and velocities do not converge strongly in
L2, and initial energies do not converge to the background energy. There is
NO energy creation from zero-energy data and no counterexample here to
strong-initial-data convergence, exact-solution uniqueness or stability.

Multiplying psi_e by any positive amplitude b_e->0 gives
||h_e||2=b_e sqrt(A0), ||u_e||2=v b_e sqrt(A0). All packet defect weights
become b_e² A0 and vanish. The small remainder bounds also vanish, and the
initial/total energies now converge to the background. This is an explicit
control, not an exponent scan. Strong convergence of the energy-carrying
variables distinguishes it from the nonzero-defect sequence.

## Sufficient identification conditions, not consequences of the PDE

One transparent sufficient condition on a finite spacetime slab is strong
L2 convergence of each g,u,chi_x,chi_t, together with uniformly bounded chi
converging uniformly, and strong L2 convergence of both r=sqrt(n) and
z=j/sqrt(n). Use z=0 on vacuum for each state AND assume the limiting z=0
where limiting r=0. This last vacuum compatibility is not automatic from
strong convergence: otherwise a kinetic defect can survive on vacuum.
Then n=r², j=rz and j²/n=z² converge in L1 by Cauchy-Schwarz. Field quadratic
products also converge in L1. The Q bounds |partial_g B|<=1 and
|partial_a B|<=1/2 make B converge strongly in L2 when a converges uniformly.
Consequently B g converges in L1. For W, the gradient difference is bounded
by (|g1|+|g2|)|g1-g2|, while |W_a|=T/a<=|g|/2 bounds the scale-parameter
change. These give L1 convergence of W. Bounded uniform chi convergence also
gives convergence of U and U'. Thus all combined momentum coefficients are
identified in L1, ruling out the momentum/stress defects above.

For energy DENSITY additionally require L1 convergence of e(n), since density
L1 convergence alone does not identify n log n. Bounded potentials converging
uniformly then identify n phi as well. Entropy convergence can be supplied by
convergence in measure plus uniform integrability of entropy densities, using
truncation into bounded values and uniformly small tails. Likewise convergence
in measure of energy-carrying derivatives plus uniform integrability of their
squares yields strong L2 by truncating tails and integrating the bounded
remainder. Uniform integrability WITHOUT convergence in measure does not
exclude oscillatory defects. None of these compactness conditions follows
just from bounded total energy or vanishing residuals in (4)-(6).

The general matter ENERGY FLUX needs further velocity/enthalpy product control;
its identification is not asserted from the above sufficient momentum/energy-
density conditions. For the explicit packet j=0 it vanishes and the direct
flux check already made is valid. Weak force-product equivalence and boundary/
initial traces remain distinct from these sufficient interior compactness gates.

All calculations retain the actual Q MOND constitutive law and potential
inertia. Both a0=9.3619e-11 and1.1279e-10 m/s² specify separate positive
backgrounds; constant-vacuum reference, frozen a0 E(z) with
E²=.315(1+z)^3+.685, and evolving-H cases stay distinct. This is fixed-reference
work with an added locally responsive scale, not a physical reservoir or
cosmology. No RAR/M/filtered-MONO, metric/photon/DOF, calibrated observation,
imported mechanism, historical novelty or physical theory closure follows.
