# FGF037: nonlinear Q energy is not controlled by the weighted linear topology

Proof-only worker derivation, fixed before viewing new root/auditor proof.
Keep one reviewed short FGF036 crossing and its physical interval, density,
scale, mass and wall values. We use phi-only tests: density and scale remain
unchanged, so their positivity, mass and energies are not approximation issues.

## 1. Exact action and its large-gradient growth

Let C=4piG>0, g=phi0', a(x)=a_ref exp(chi0(x)), and let a be bounded above
and below by positive constants on the fixed compact interval. The background
has signed flux B=sgn(g)b(|g|,a), B'=C rho, with rho positive. For Q,

 b(s,a)=(sqrt(a²+4s²)−a)/2, W(s,a)=integral_0^s b(t,a)dt.

Since 2s<=sqrt(a²+4s²)<=2s+a for s>=0,

 s−a/2<=b(s,a)<=s,
 s²/2−as/2<=W(s,a)<=s²/2,
 W(s,a)>=s²/4−a²/4.                                 (1)

These inequalities hold globally, including where the lower bound is negative;
W itself is nonnegative. They imply the uniform large-gradient asymptotic
W(s,a)=s²/2+O(a_max s) when a ranges over the fixed bounded interval.
For a measurable spatial gradient G on a finite interval,

 integral W(|G|,a)<infinity iff G is in L2.           (2)

The upper bound proves sufficiency. The last lower bound proves necessity
by s²<=4W+a_max². This uses the exact Q high-gradient law, not the deep cubic
truncation applied beyond its range.

For a fixed-wall potential perturbation psi, the full static energy change
with unchanged rho,chi is

 E[phi0+psi]−E[phi0]
  =integral rho psi+(1/C)integral[W(|g+psi'|,a)−W(|g|,a)].

Every weighted-domain psi is continuous and absolutely continuous, with psi'
in L1, so rho psi and B psi' are integrable. B is C1 and psi vanishes at the
outer endpoints. The integrated equilibrium linear term cancels EXACTLY:

 integral B psi'=-integral B' psi=−C integral rho psi.

Consequently the correct energy change, possibly positive infinite, is

 D[psi]=(1/C)integral[W(|g+psi'|,a)−W(|g|,a)−B psi']. (3)

Convexity gives a nonnegative pointwise integrand. The matter interaction is
not dropped, and no infinite linear subtraction is concealed in (3). The
source is B', not g': the integrable cusp in g' is not substituted for density.
Scale/fluid internal/gradient terms cancel because those fields are unchanged.

## 2. A genuine singular member of the completed linear domain

Recall A=b_s(|g|,a)~a_A sqrt(|x|), a_A>0, and
s(x)=integral_left^x 1/A, whose finite total length is S. The weighted phi
space V_A is equivalent to H1_0(0,S) under psi(x)=v(s(x)), with

 integral A psi'² dx=integral v_s² ds.

Choose one smooth v compactly supported in (0,S), with v_s a fixed nonzero
constant in a neighborhood of the center coordinate s0. Its units are those
of potential; a fixed reference amplitude may be multiplied into v. Then
psi is a legitimate zero-outer-trace weighted-domain direction, continuous
across the center, and

 psi'(x)~[v_s(s0)/a_A]|x|^(−1/2).                   (4)

The weighted integral is finite, but integral psi'² diverges logarithmically.
For every nonzero dimensionless amplitude epsilon, the new gradient
G=g+epsilon psi' is not in L2, since g is bounded and L2. By (2), its exact
field energy is infinite. All interaction and linear subtraction terms remain
finite as established above, so D[epsilon psi]=+infinity for epsilon nonzero.
Yet ||epsilon psi||_VA tends to zero as epsilon tends to zero.

Thus no open weighted-form neighborhood of the background is a finite-energy
domain for the exact action. The singular direction alone does not establish
impossibility of nonlinear evolution on a stronger domain. Nor does a
quadratic finite directional form imply that the exact nonlinear functional
has finite second directional derivatives along this singular direction:
here it has infinite energy for every nonzero amplitude. FGF036 constructs
a closed extension of the linear form, not that stronger nonlinear assertion.

## 3. One smooth concentration family with full dimensional restoration

The failure is not only an artifact of admitting singular test functions.
Choose fixed positive reference length L_ref and potential amplitude Psi_ref.
Let f(y)=exp[−1/(1−y²)] for |y|<1 and0 outside: one fixed smooth nonzero
compact bump. Its derivative has positive squared integral. Let delta>0 be
dimensionless and sufficiently small that its support fits inside the fixed
crossing interval. Choose ONE exponent beta=3/8 and define

 psi_delta(x)=Psi_ref delta^(3/8) f(x/(L_ref delta)),
 p_delta=psi_delta'= (Psi_ref/L_ref)delta^(−5/8)
                                      f'(x/(L_ref delta)). (5)

These are smooth phi-only fixed-wall perturbations. Fluid density, mass and
scale stay exactly equal to the background. The exponent satisfies
1/4<beta<1/2, giving vanishing weighted gradient energy but growing physical
L2 gradient energy. This is a single discriminating family, not an exponent
scan. The potential amplitude tends to zero uniformly despite increasing
pointwise gradients.

Let J0=integral_-1^1 f'²>0 and JA=integral_-1^1 sqrt(|y|) f'²>0.
Using the actual coefficient A(x)~a_A sqrt(|x|),

 integral p_delta² dx=(Psi_ref²/L_ref)J0 delta^(−1/4),
 integral A p_delta² dx~(a_A Psi_ref²/sqrt(L_ref))JA delta^(1/4),
 integral psi_delta² dx=Psi_ref² L_ref delta^(7/4) integral f². (6)

The coefficient asymptotic can be substituted under the fixed rescaled
integral because A(x)/sqrt(|x|) tends to a_A and is uniformly bounded near
zero. The point y=0 has no adverse contribution. Thus psi_delta tends to0
in V_A (with any fixed dimensional norm weights), but its physical L2 gradient
norm diverges like delta^(−1/8). Its gradient supremum grows like
(Psi_ref/L_ref)delta^(−5/8) max|f'|.

On this phi-only subspace the full quadratic form is Q[0,psi,0]=integral
A psi'²/C, so the quadratic Taylor ENERGY is H[psi]=Q[0,psi,0]/2. Therefore

 H[psi_delta]~[a_A Psi_ref² JA/(2C sqrt(L_ref))]delta^(1/4)->0. (7)

To determine the EXACT energy, (1) gives uniformly

 |W(|g+p_delta|,a)−(g+p_delta)²/2|
                                      <=a_max|g+p_delta|/2.

Only the bump support contributes to (3). On that support the background has
g=O(delta^(1/2)), B=O(delta), and W(|g|,a)=O(delta^(3/2)).
The integrated bounds are

 integral|p_delta|=O(delta^(3/8)),
 integral|g p_delta|=O(delta^(7/8)),
 integral|B p_delta|=O(delta^(11/8)),
 integral g²=O(delta²), integral W(|g|,a)=O(delta^(5/2)).

The integrated large-gradient error is at most O(delta^(3/8))+O(delta^(3/2)).
Every displayed error vanishes; the leading unweighted gradient-square term
diverges. Hence the exact full energy difference is

 D[psi_delta]~[Psi_ref² J0/(2C L_ref)]delta^(−1/4)->+infinity. (8)

This proof does not assume that g+p is uniformly large at each bump point:
the global bounds (1) control the zeroes of f' as well. Equation (3) already
accounts for the interaction rho psi and its exact equilibrium cancellation.
Each individual smooth bump has finite exact energy; it is the sequence of
energies which diverges as its weighted distance to the background vanishes.

## 4. Precise failed continuity and Taylor implications

Equations (6)-(8) prove that even the restriction of the exact finite-energy
functional to smooth fixed-wall phi perturbations is not continuous at the
background in the completed weighted-form topology. They also rule out a
uniform quadratic upper control D[psi]<=constant||psi||_VA² near zero.
For the claimed quadratic approximation the normalized remainder obeys

 (D[psi_delta]−H[psi_delta])/||psi_delta||_VA² ->+infinity, (9)

since numerator is of order delta^(−1/4) and denominator of order delta^(1/4).
Equivalently D/H grows as a positive constant times delta^(−1/2). In particular
there is no little-o quadratic Taylor remainder in this topology, and no
bounded uniform quadratic remainder controlling all sufficiently small
weighted perturbations.

This does not contradict the valid second variation along any FIXED smooth
bounded-gradient direction when its scalar amplitude tends to zero. The
concentrating directions change with delta, and the exact constitutive energy
enters its large-gradient quadratic regime even while their weighted norms
vanish. A fixed-gradient-amplitude or stronger nonlinear bound would change
the question. Neither a negative energy direction nor a growing time mode
has been found: the exact increments here are positive.

## 5. Necessary stronger finite-energy domain and surviving linear theorem

At fixed bounded positive scale, on this finite interval, finite field energy
requires g+psi' in L2. Since g is L2 and the weighted perturbations are already
bounded continuous, within V_A this means exactly psi in ordinary H1_0.
It is therefore a necessary stronger phi domain for interpreting exact finite
nonlinear energy, not a sufficient theorem for nonlinear evolution.
For this fixed-density/fixed-scale slice, exact energy is continuous in the
strong H1 topology: b(s,a)<=s implies

 |W(|G1|,a)−W(|G2|,a)|
                     <=(|G1|+|G2|)|G1−G2|,

whose integral is controlled by Cauchy-Schwarz when gradients converge in L2;
the interaction is continuous by the same fixed-density bounds. No claim of
twice-Frechet differentiability on all H1 neighborhoods or of a well-posed
nonlinear matter/scale system follows merely from this observation.

FGF036's positive closed weighted quadratic form, compact inverse, transmission
conditions and conserved LINEAR energy evolution remain mathematically valid
on their stated spaces. Their extension includes directions with no finite
nonlinear action at nonzero amplitude, and even smooth finite-energy directions
lack uniform nonlinear control in that topology. Thus that linear theorem
cannot by itself establish nonlinear stability, nonlinear Cauchy well-posedness
or a nonlinear fixed-wall parameter-response result. The present gate is closed
by explicit counterexamples; repeating weighted positivity does not repair it.

## 6. Units, branch distinctions and stopping scope

Psi_ref has potential units L²/T², L_ref has length units, and delta is
dimensionless. p and g are accelerations, A dimensionless, a_A has inverse
square-root-length units. D and H above are energy per transverse area because
W/C is energy density. Formulae keep the same physical reference units and
coefficients as delta varies, so no coupling rescaling hides the concentration.

Both a_ref=9.3619e-11 and1.1279e-10 m/s² remain separate positive hypotheses;
a=a_ref exp(chi0) is bounded on each chosen crossing. The proof applies to each
without equating their backgrounds. Constant-vacuum, frozen a(0)E(z) and actual
evolving-H prescriptions are distinct; an evolving reference retains the
missing reservoir/exchange obligation. Responsive local scale is an added
diagnostic premise and not a literal scale-vacuum identity derivation.

Q only is treated. RAR transfer and registered M action are not inferred.
No physical V, imported mechanism, historical novelty, filtered MONO,
metric/photon/DOF or empirical closure is supplied. The exact failed implication
is weighted linear control => nonlinear energy control. Further work requires
a separately justified nonlinear/physical target and stronger domain, not a
parameter scan or a ghost/instability conclusion from these counterexamples.
