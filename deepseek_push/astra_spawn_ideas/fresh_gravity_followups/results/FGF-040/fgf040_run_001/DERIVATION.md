# FGF040: force-product failure and a candidate conservative momentum system

Proof-only independent worker derivation, frozen before new root/reviewer text.
The action is the inherited preferred-time Q matter/phi/chi model, with fixed
positive C=4piG, tau=K/c², sigma=J/v_chi², J,cs²,S0 and fixed a_ref. This is
an evolution-domain audit, not a nonlinear existence or physical metric theorem.

## 1. The energy class does not define the separate force density

Fix the same wall interval I=(-d,d), background rho>0, phi0,chi0 and mass M.
Select one fixed length0<L<d/4. Define a normalized nonnegative density shape

 q(x)=(1/(3L))(x/L)^(-2/3) for0<x<L, and0 elsewhere,
 integral_I q=1,
 n=(rho+M q)/2.                                      (1)

This has mass M and is positive almost everywhere. Its relative isothermal
entropy is finite: near0 the singular contribution is bounded by a constant
times x^(-2/3)(1+|log x|), which is integrable; away from0 it is bounded or
has finite jumps. Background rho is bounded above/below, so changing from
absolute entropy to entropy relative to rho causes no divergence.

Take one fixed acceleration amplitude a_p=a_ref>0 and define

 p(x)=a_p[(x/L)^(-2/5) 1_(0,L)(x)−(5/3)1_(2L,3L)(x)],
 psi(x)=integral_-d^x p(s)ds.                        (2)

The two integrals cancel, so psi has zero outer traces and is supported in
[0,3L]. It is continuous, absolutely continuous and H1: its derivative is p
and integral p²=a_p² L(5+25/9)=70 a_p² L/9<infinity. Its supremum is at most
5a_p L/3. Set chi=chi0 (eta=0), matter velocity v=0, and instantaneous field
velocities phi_t=chi_t=0, with phi=phi0+psi. Scale cap and endpoint fields are
unchanged and kinetic energy is zero.

Every exact energy component is finite. Q obeys0<=W(|G|,a)<=G²/2, so G=phi_x
in L2 gives finite field action. The inherited scale gradient/potential remain
finite. The fluid entropy was checked above and the interaction n phi is L1
since phi is bounded and n has fixed finite mass. This is an admissible energy
comparison state, not a static equilibrium or a constructed nonlinear solution.

On0<x<L the actual crossing background g0=phi0' is positive, so

 n phi_x >= (M/(6L))(x/L)^(-2/3)
                          a_p(x/L)^(-2/5)
           =(M a_p/(6L))(x/L)^(-16/15).             (3)

Its integral diverges on every neighborhood of0. The product is nonnegative
there, so no principal-value cancellation represents it as an ordinary L1
force. It does not define a distribution by integration against a nonnegative
test function equal to1 near0. A renormalized extension would be an additional
choice, not supplied by the energy class.

This is an exact mass-preserving counterexample to the implication
finite entropy + finite action => n phi_x in L1_loc. It does not refute
nonlinear evolution on all stronger domains or in all other weak formulations.
The field is dynamical: its source equation is B_x=C n+tau phi_tt, with
B=sgn(phi_x)b(|phi_x|,a). Imposing B_x=C n on arbitrary comparison data would
incorrectly discard potential dynamics. We neither impose that static
constraint on (1)-(2) nor assert a future trajectory for these data.

## 2. Smooth full equations and the combined momentum identity

Let n,v,phi,chi temporarily be smooth, with n>0 where primitive fluid equations
are used; the conservative expressions below use j=n v. Let

 g=phi_x, a=a_ref exp chi, B=sgn(g)b(|g|,a),
 T=-a W_a, p_m=cs² n, U=S0[cosh(2chi)−1]/4.

The inherited smooth equations are

 n_t+j_x=0,
 j_t+(j²/n+cs² n)_x=−n g,
 tau phi_tt−B_x=−C n,
 sigma chi_tt−J chi_xx+U'=T.                         (4)

At vacuum, the kinetic convention later is j=0 when n=0, with j²/n=0 there;
this does not create a smooth primitive velocity equation at vacuum.

Define field momentum density and stress

 P_f=−[tau phi_t g+sigma chi_t chi_x]/C,
 Pi_f=[tau phi_t²/2+sigma chi_t²/2+B g−W
                              +J chi_x²/2−U]/C.     (5)

Direct differentiation gives the phi contribution
(B_x−tau phi_tt)g/C+T chi_x/C, because
partial_x W=B phi_xx−T chi_x. The scale contribution is
(−sigma chi_tt+J chi_xx−U')chi_x/C=−T chi_x/C.
Thus the scale exchange terms cancel and

 (P_f)_t+(Pi_f)_x=n g.

Adding the smooth matter equation cancels the force BEFORE any weak limit:

 P_t+Pi_x=0,
 P=j−[tau phi_t phi_x+sigma chi_t chi_x]/C,
 Pi=j²/n+cs² n
      +[tau phi_t²/2+sigma chi_t²/2+B phi_x−W
                                +J chi_x²/2−U]/C.  (6)

All signs, both kinetic stresses and the scale-gradient/potential terms are
retained. The interaction n phi belongs in the energy but does not appear
as an extra term in (6); its mechanical force has canceled against the field
momentum exchange by the actual equations. This is a 1D preferred-frame
momentum identity, not a covariant gravitational stress tensor.

For smooth fields the global relation is

 d/dt integral_I P dx=−[Pi]_left^right.              (7)

Fixed field wall values imply phi_t=chi_t=0 there, and impermeable fluid
walls imply v=0. They do NOT generally make Pi vanish: pressure, B g−W,
scale-gradient stress and U can transfer momentum to the walls. Zero energy
flux at fixed walls must not be confused with zero momentum traction.
Global momentum conservation needs the actual endpoint traction balance.

## 3. Integrability of the combined quantities at a finite-energy time slice

Assume n>=0, integral n=M, finite entropy, phi and chi in their affine H1
wall classes, |chi−chi0|<=1/4, phi_t,chi_t in L2 and integral j²/n finite
with j=0 on vacuum. Then

 ||j||_1<=sqrt(M)*sqrt(integral j²/n),
 ||phi_t phi_x||_1<=||phi_t||_2||phi_x||_2,
 ||chi_t chi_x||_1<=||chi_t||_2||chi_x||_2.

Therefore P is L1. Every term in Pi is L1: j²/n,n and kinetic squares are
controlled; |B|<=|g| gives0<=B g<=g²;0<=W<=g²/2; chi_x² is integrable,
and U is bounded under the scale cap on this finite interval. No n g product
is required. These bounds apply even to the counterexample (1)-(2), where
separate force integrability fails. Finite fluxes alone do not assert that
this state solves the conservation law.

The other candidate equations also have meaningful coefficients. B is L2.
For Q, q(s,a)=T_s=a b/(2b+a)<=a/2 and T(0,a)=0, so
0<=T(s,a)<=a s/2. With a bounded by the scale cap, T is L2, and U'(chi)
is bounded. The density source n is L1. These are coefficient bounds, not
license to multiply the resulting distributions by rough field derivatives.

## 4. What is needed in spacetime

Pointwise-in-time finiteness alone does not give spacetime integrability. A
sufficient local-in-time assumption on each compact time slab is that n has
fixed mass, the fields have the stated weak derivatives and traces, and

 integral dt integral dx [j²/n+phi_t²+phi_x²+chi_t²+chi_x²+U(chi)]<infinity,

together with a uniform finite scale cap or another explicit bound on a and
U' sufficient for the field source. These assumptions imply P,Pi in L1 of
that spacetime slab by time-space Cauchy-Schwarz and fixed mass. One convenient
stronger version is local uniform-in-time bounds on those spatial integrals.
Measurability and compatibility of phi_t,chi_t with distributional time
derivatives are required; assigning unrelated kinetic variables is not enough.

There is a useful conditional way to obtain the component bounds on this
finite wall interval, without presuming that signed total energy is itself
a sum of nonnegative terms. Suppose total energy has a uniform upper bound,
mass is M, a<=a_max uniformly and the fixed left potential value is phi_L.
The exact raw energy is

 E=K+integral[e(n)+n phi+(W+J chi_x²/2+U)/C],
 K=integral[j²/(2n)+(tau phi_t²+sigma chi_t²)/(2C)].

From Q, W>=g²/4−a_max²/4. Also
phi>=−|phi_L|−sqrt(ell)||g||_2, so
integral n phi>=−M|phi_L|−M sqrt(ell)||g||_2.
The elementary inequality
M sqrt(ell)||g||_2<=||g||_2²/(8C)+2C M²ell yields

 E>=K+||g||_2²/(8C)+J||chi_x||_2²/(2C)
                             +integral U/C+integral e(n)−C0,
 C0=M|phi_L|+a_max²ell/(4C)+2C M²ell.                (8)

Since e(n)>=−cs²rho_ref pointwise, an upper bound for E controls every
nonnegative component on the right and the positive part of e as well.
Thus a postulated uniform energy bound plus uniform scale cap and mass supplies
the preceding spacetime bounds. This is an algebraic estimate, not a proof
that a weak trajectory conserves or dissipates energy. The cap may be obtained
only under the already-explicit conditional premises of FGF039; no existence
or cap preservation is inferred from writing (8).

## 5. A meaningful candidate weak system and its non-equivalence gap

Under those spacetime bounds, one MAY PROPOSE a weak system consisting of mass,
the two original field equations and combined momentum. For compactly supported
smooth spacetime tests zeta in the open slab the identities are

 integral(n zeta_t+j zeta_x)=0,
 integral[−tau phi_t zeta_t+B zeta_x+C n zeta]=0,
 integral[−sigma chi_t zeta_t+J chi_x zeta_x+(U'−T)zeta]=0,
 integral(P zeta_t+Pi zeta_x)=0.                     (9)

Each integral is well-defined by the stated bounds. These equations retain
the signed Q constitutive law and dynamic source term. Choosing (9) as a weak
solution definition is an EXPLICIT new formulation choice at low regularity.

For smooth solutions it is equivalent to the separate matter momentum
equation in (4), because the field identity can be differentiated and
subtracted. At the energy regularity above this equivalence is NOT established:
ng need not be L1, and deriving the field momentum identity separately would
multiply weak field equations by g or chi_x, which is unjustified. Therefore
(9) must not be described as a theorem repairing an undefined product while
preserving the original weak dynamics. Additional product/renormalization
regularity, or a carefully selected limiting definition, remains to be proved.
Even bounded finite-energy sequences need not pass their quadratic momentum
fluxes to the weak limit without compactness; possible defect terms have not
been ruled out. Cancellation is justified in the smooth algebra (6) first,
not by multiplying undefined distributions after a limit.

There is no solution existence, uniqueness, energy equality/inequality,
stability or convergence theorem in this pass. Meaningful equations and finite
fluxes are prerequisites, not solutions.

## 6. Initial and wall traces are separate obligations

For tests supported in the interior, (9) needs no pointwise wall evaluation.
The imposed field Dirichlet values are meaningful as H1 spatial traces for
almost every time. But L2 gradients and field velocities, or L1 j,Pi, do not
automatically have the wall traces appearing in (7). Impermeable matter walls
need a specified normal trace of j (or an appropriately imposed weak boundary
mass condition); total mass is retained explicitly here. Testing momentum up
to the wall requires actual traction traces of Pi with enough time
integrability, or a separately specified normal-trace framework. One cannot
set Pi to zero merely because the potential and scale values are fixed.

Initial momentum also needs an appropriate weak trace or a prescribed initial
term in the weak formulation; L1 slice bounds alone do not justify identifying
it with a pointwise value at t=0. Stronger regularity can supply the usual
traces, but has not been proved from the energy class. The same issue applies
to temporal traces used for field and mass initial conditions. These are
explicit well-posed-definition obligations, not claimed consequences.

## 7. Scope and physical bookkeeping

All state and stress expressions retain their physical units. q in (1) has
inverse-length units; M q is volume density. a_p is acceleration and psi has
potential units. P is momentum density and Pi momentum flux/pressure; division
by C converts the field terms correctly. Density entropy, interaction and
kinetic energies have been checked component by component.

Both positive a_ref choices9.3619e-11 and1.1279e-10 m/s² give separate
backgrounds and valid counterexamples. Constant-vacuum and frozen-H comparisons
are distinct from an evolving reference. A spatially uniform prescribed
reference a_ref(t) would not by itself add an explicit spatial force to the
smooth translation identity, but it changes energy exchange and cannot inherit
the assumed energy bounds/conservation without reservoir accounting. No
cosmological evolution is derived here. Responsive local scale remains an
added diagnostic premise.

Q only is treated; no RAR/M transfer, physical V, filtered-MONO, metric/photon/
DOF completion, instrument calibration, imported mechanism or historical
novelty is claimed. The precise outcomes are a force-product counterexample,
a full smooth conservative identity, and the integrability/trace conditions
under which a candidate weak formulation can be written. Weak equivalence and
actual evolution remain distinct unresolved questions.
