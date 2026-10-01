# FGF035: a coupled static crossing of zero signed Q flux

Proof-only worker derivation, fixed before reading any new root/auditor proof.
This is a local conditional construction in the inherited diagnostic Q action.
No numerical experiment, physical metric, external mechanism or novelty claim.

## 1. Signed equations from the action

Let C=4piG, cs²,J,S0,a_ref be fixed positive physical constants. With
U=S0(cosh(2chi)−1)/4, a=a_ref exp(chi), and the original isothermal fluid,
the static energy per transverse area is

 integral {e(rho)+rho phi+[W(|phi'|;a)+J chi'²/2+U(chi)]/C} dx,
 e(rho)=cs² rho[log(rho/rho_ref)−1], e''=cs²/rho.

For Q, b(s,a)=(sqrt(a²+4s²)−a)/2, W_s=b and
T(s,a)=−a W_a=s b−2W, with W(0,a)=T(0,a)=0.
For s>0, q=T_s=s b_s−b>0 and d=T_chi=2T−s q.
The signed constitutive flux is B=sgn(phi')b(|phi'|,a), continuous at zero.
Variation at fixed endpoint fields and fluid mass gives

 B'=C rho, cs²rho'=−rho phi', J chi''=U'−T(|phi'|,a). (1)

Inverting the actual Q constitutive flux, not a Newtonian source formula,

 g=phi'=sgn(B)sqrt(B²+a|B|).                          (2)

Therefore B=0 is compatible with positive density through B'=C rho>0.
The physical acceleration is −g, so the signs correspond to force toward
the local potential minimum. Spatially varying a is the added responsive
scale assumption; only a_ref, not necessarily actual a, is spatially constant.

## 2. Existence through the crossing using flux as coordinate

Prescribe at x=0 the finite data B=0, rho=rho_*>0, chi=chi_*, w=w_*,
phi=phi_*, where w=chi'. Write a_*=a_ref exp(chi_*)>0. In independent
coordinate B, the exactly transformed equations are

 dx/dB=1/(C rho),       drho/dB=−g/(C cs²),
 dchi/dB=w/(C rho),     dw/dB=[U'(chi)−T(|g|,a)]/(JC rho),
 dphi/dB=g/(C rho).                                  (3)

The absence of rho in the numerator of drho/dB is important; it cancels
against B'=C rho. At B=0 set g=0 continuously. On a small compact state
rectangle with rho bounded below by rho_*/2 and chi,w finite, these right
sides are continuous in B and uniformly locally Lipschitz in all dependent
variables. In particular the only apparent singularity is dependence on the
independent coordinate B, not an unbounded state derivative:

 partial_chi g=sgn(B) a|B|/[2 sqrt(B²+a|B|)]=O(sqrt(|B|)),

extended by zero at B=0, uniformly in the chi rectangle. The state derivative
of T(|g(B,chi)|,a(chi)) is also bounded there (and tends to zero); the inverse
rho factors are smooth. No derivative with respect to B is needed for this
local Lipschitz gate. The x and phi variables introduce no additional state
singularity because the coefficients do not depend on them.

Choose a small symmetric B interval so that the bounded right sides keep the
integral-map image inside this rectangle and the uniform Lipschitz constant
times its length is less than one. Picard iteration of the integral equations
is then a contraction, giving a unique local C1 state solution on both sides
of B=0 with rho>0. This argument also supplies local uniqueness within this
positive-density regular class, not an arbitrary global weak-solution theorem.

Since dx/dB is positive and bounded above/below, x(B) is a local C1 monotone
bijection with C1 inverse B(x). Composition reconstructs all spatial fields
and (1) exactly. There is no assumption that g is differentiable at zero.
The boundaries and total mass on any compact subinterval are induced by this
IVP, not preassigned arbitrarily and not FGF034's fixed-wall response branch.

## 3. Local asymptotics and sharp failure of H2 for phi

Let k_B=C rho_* and k=sqrt(a_* k_B). Continuity in (1) first gives
B(x)=k_B x+o(x), a(x)=a_*+O(x). Equation (2) then gives

 g(x)=k sgn(x)|x|^(1/2)(1+o(1)),
 phi(x)=phi_*+(2k/3)|x|^(3/2)+o(|x|^(3/2)),
 rho(x)=rho_*−[2rho_* k/(3cs²)]|x|^(3/2)+o(|x|^(3/2)). (4)

The density result follows by integrating rho'=−rho g/cs², or equivalently
rho=rho_* exp[−(phi−phi_*)/cs²]. The positive density is maximal at the
crossing, while phi has its local minimum there. No reflection symmetry is
assumed: w_* may be nonzero and higher-order terms may be asymmetric.

For x nonzero, differentiating (2) using B'=C rho and a'=a w gives

 g'=[(2|B|+a)B'+a'B]/[2 sqrt(B²+a|B|)].              (5)

Consequently g'(x)=(k/2)|x|^(−1/2)(1+o(1)) on BOTH sides. This derivative
statement follows from the exact equation, not by differentiating an
uncontrolled little-o term in (4). It is locally Lp for 1<=p<2, but its
square has a positive logarithmically divergent integral. Therefore

 phi in C^(1,1/2) and W^(2,p) for p<2, but phi not in H2

on every interval containing the crossing. Holder statements are local on
a sufficiently small compact two-sided interval. The coefficient asymptotics
exclude any higher Holder exponent for g at the crossing.

Hydrostatic balance gives rho in C^(1,1/2), with
rho''=−(rho'g+rho g')/cs² asymptotic to
−rho_* k |x|^(−1/2)/(2cs²) off zero. Thus rho is also W^(2,p) for p<2
and is not H2 across zero. The signed flux satisfies B'=C rho, hence B is
C^(2,1/2), a much smoother field than g.

For the responsive scale, the Q small-gradient source is
T(s,a)=s³/(3a)+O(s5/a³) at fixed a bounded away from zero. Along (2),

 T(|g(x)|,a(x))=[k³/(3a_*)]|x|^(3/2)(1+o(1)).       (6)

More structurally, as a function of B and a, it is |B|^(3/2) times a smooth
positive function near |B|=0,a=a_*. This composition is C^(1,1/2).
The equation J chi''=U'(chi)−T first makes chi C2, and then bootstrapping
with this source yields chi in C^(3,1/2), w in C^(2,1/2), locally. In
particular chi and w remain finite and the scale gradient energy is bounded.
No need to assume or claim a fourth square-integrable derivative of chi.

## 4. Weak equations, no delta source and finite energy

B is continuous and C1 with derivative C rho on the whole interval. Thus for
compactly supported smooth test zeta,

 −integral B zeta' dx=integral C rho zeta dx.

There is no jump in B and hence no delta-function source at x=0. The integrable
singularity of g' is not the gravitational source: the actual source is B'.
The pressure and scale equations hold with their continuous first/second
derivatives and therefore also distributionally. Continuity of g means phi
has no jump or delta derivative either. A point mass would require different
flux data and is excluded by the finite positive rho_* prescription.

The local field energy obeys
W(|g|;a)=[k³/(3a_*)]|x|^(3/2)(1+o(1)), so is integrable. The scale energy
Jw²/2+U, isothermal internal energy and interaction rho phi are bounded on
small compact intervals. Thus the full static energy per area is finite.
This is integrability, not positivity of the complete self-gravitating energy.
No kinetic instability, global evolution or boundary flux balance in an
unprescribed time-dependent problem is inferred from static existence.

## 5. Full directional Hessian and loss of the standard H1 bound

Choose a fixed small interval around zero, with its induced fields/mass,
and fixed zero perturbation traces xi=psi=eta=0 at its endpoints. Set
r=−(rho xi)'. The mass constraint still has integral r=0 because rho is
positive C1. The original hydrostatic multiplier e'(rho)+phi is constant,
so the inherited full quadratic form, first derived on smooth test triples,
is

 Q0[u]=integral {cs²r²/rho+2r psi
      +[A psi'²−2q_s eta psi'+J eta'²+(U''−d)eta²]/C} dx,
 A=b_s(|g|,a), q_s=sgn(g)q(|g|,a), d=T_chi(|g|,a).  (7)

The signed cross coefficient q_s is required on the negative-gradient side.
Set A=q_s=d=0 at zero where appropriate: W(|g|,a) is C2 as a function of
the signed gradient at zero and has zero gradient Hessian there. All
coefficients in (7) are bounded and continuous, so the form extends
continuously to H1_0 triples. This is a directional second-variation form;
no assertion is needed that the nonlinear energy is twice Frechet
differentiable on every H1 neighborhood with unbounded gradient spikes.

For Q,

 A=2|g|/sqrt(a²+4g²)
   =(2k/a_*)|x|^(1/2)(1+o(1)).                     (8)

In particular A>0 away from the crossing, but it has no positive uniform
lower bound. To test the FULL form's standard product-H1 coercivity it is
legitimate to take an admissible phi-only triple (0,psi,0); (7) then equals
integral A psi'²/C, with no matter or scale term left on this subspace.
This is a test direction, not a deletion of those terms for general triples.

Choose a nonzero smooth f compactly supported in (−1,1), and for small
positive epsilon set psi_epsilon(x)=sqrt(epsilon) f(x/epsilon).
Then integral psi_epsilon'²=integral f'² is fixed and positive, whereas
integral psi_epsilon²=epsilon² integral f². The support lies in the interior
fixed-wall domain. Equation (8) gives

 Q0[0,psi_epsilon,0] <= [sup_(|x|<epsilon) A/C] integral f'²
                        =O(sqrt(epsilon)).           (9)

After any fixed positive reference-unit weighting of the fields and length,
the ratio to the product-H1 norm squared tends to zero. Therefore no positive
constant c0 can satisfy Q0[u]>=c0||u||_H1² on this interval. Every member of
this phi-only sequence nevertheless has strictly positive quadratic energy,
because A>0 almost everywhere and psi' is nonzero on a set of positive
measure. The obstruction is not a negative-energy counterexample.

The positive-gradient H2 seed and the uniform H1 coercivity gates used in
FGF034 both fail here, for explicit independent reasons. This prevents using
that proof unchanged; it does not refute static crossing existence (proved
above), invertibility in every possible weighted space, nonlinear stability,
or a different carefully constructed response theorem. Sign of the full
coupled form and its weighted/dynamical operator domains remain open.
Positive inherited time kinetic coefficients are unchanged, so vanishing
spatial stiffness alone is not evidence of a ghost or PDE ill-posedness.

## 6. Scope, controls and next obligation

The positive-density hypothesis ensures monotonic B as a coordinate; no claim
is made at rho_*=0. Finite chi_* ensures a_*>0. The cancellation in drho/dB,
signed cross term q_s and absence of a flux jump are decisive sign/domain
controls. A Newtonian replacement g'=C rho would erase the square-root cusp
and is a different constitutive problem. Keeping w_* arbitrary tests that no
hidden symmetry or constant-scale assumption supplies the crossing.

Units are physical: B and g accelerations; C rho has inverse-time-squared
units, and k=sqrt(a_* C rho_*) has acceleration divided by sqrt(length)
units. W has acceleration-squared units, and W/C is energy density. Both
reference normalizations9.3619e-11 and1.1279e-10 m/s² can be used independently
as a_ref; the proof only requires positive a_ref. Frozen H choices replace
a_ref by a(0)E(z), E²=.315(1+z)^3+.685, with the other physical constants and
initial data kept explicit. They are separate reference hypotheses, not a
cosmological evolution. An evolving reference needs its energy exchange or
a complete scale reservoir, which is outside this static construction.

A local spatially responsive scale is an additional diagnostic premise and
does not establish the literal constant-vacuum actual-scale identity. RAR
transfer is not proved here, and no registered M action is invented. The
operative filtered MONO, metric/photon/DOF, conserved physical scale sector,
instrument calibration and physical global equilibrium remain unresolved.

The next mathematical obligation, if this diagnostic crossing is retained,
is to specify a justified weighted variational/operator domain and test the
full matter/scale response there. The failed standard-H1 lower bound must
not be silently promoted to spectral or nonlinear instability, nor repaired
by pretending this background belongs to the previous H2 positive-gradient
branch. This pass supplies one local existence/regularity result and one
precise failed applicability gate, not theory closure.
