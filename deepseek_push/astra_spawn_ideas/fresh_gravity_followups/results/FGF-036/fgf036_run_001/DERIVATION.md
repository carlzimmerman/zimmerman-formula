# FGF036: a weighted coupled linear energy across the Q crossing

Proof-only independent worker derivation, fixed before reading new root/auditor
work. This continues the actual local crossing of FGF035 with the same physical
coefficients and central data. It neither changes the constitutive law nor
repairs the established failure of standard product-H1 coercivity.

## 1. Background and exact form

Restrict one FGF035 solution to I_h=(-h,h), of length ell=2h, within its local
existence interval. Its endpoint fields and mass are induced separately at each
h; at each selected interval perturbations fix those endpoint fields and mass.
This is not a fixed-mass family as h changes. Keep C=4piG, cs²,J>0 and the
positive time coefficients tau=K/c², sigma=J/v_chi² fixed. Let

 A=b_s(|g|,a), q_s=sgn(g)(|g|A−|B|), S=T_chi, m=U''−S.

The ancestry proves rho positive C1, A~a_A sqrt(|x|) with a_A>0,
q_s=O(x), S=O(|x|^(3/2)), and smooth coefficients off the center. In particular
A>0 away from zero, A is bounded, and 1/A is integrable across zero. Write
rho_min,max for its positive extrema, Qh=sup(q_s²/A), Mh=sup max(−m,0),
with the quotient set to0 at the center. Qh=O(h^(3/2)) and Mh stays bounded.

The FULL directional quadratic form is

 Q[u]=integral {cs² d²/rho+2d psi
      +[A psi'²−2q_s eta psi'+J eta'²+m eta²]/C} dx,
 d=−(rho xi)', u=(xi,psi,eta).                         (1)

Matter and scale are not removed from this form. The kinetic Hilbert norm is

 N[u]=integral[rho xi²+(tau psi²+sigma eta²)/C] dx.    (2)

The intended outer traces are xi=psi=eta=0. No independent wall or prescribed
flux condition is inserted at x=0. Norm equivalences use fixed positive
reference units for length and each field; inequalities comparing Q to N have
inverse-time-squared units, retained below.

## 2. Weighted space, completion, density and center traces

Put I_A=integral_Ih 1/A dx, finite and O(sqrt(h)). Define V_A as the real
absolutely continuous functions psi on the closed interval with zero outer
traces and integral A psi'²<infinity. Absolute continuity is in physical x,
not merely separate continuity on the two punctured halves. The equivalent
norm is integral(A psi'²+psi²), with fixed unit weights if required.
For x<y, weighted Cauchy-Schwarz gives

 |psi(y)−psi(x)|² <= (integral_x^y A psi'²)(integral_x^y 1/A),
 ||psi||_L2² <= ell I_A integral A psi'².             (3)

Hence finite derivative energy and one fixed outer trace determine a single
continuous center value; a jump is not admissible. To justify that this is the
actual completion, rather than an arbitrary extra condition, introduce

 s(x)=integral_-h^x 1/A(t)dt, 0<=s<=I_A.

It is strictly increasing and absolutely continuous; its inverse X(s) is
Lipschitz because X_s=A(X) is bounded (and vanishes only at the single center).
Under v(s)=psi(X(s)), change of variables gives

 integral A psi'² dx=integral_0^I_A v_s² ds,
 integral psi² dx=integral_0^I_A v² A(X(s))ds.         (4)

The transformation identifies V_A with H1_0(0,I_A), with equivalent complete
norms: the ordinary derivative norm controls v by its endpoint Poincare
bound; (3) controls physical L2, while the energy is identical. Conversely
v in H1_0 reconstructs an absolutely continuous psi since its x derivative
v_s(s(x))/A(x) has finite L1 norm by Cauchy-Schwarz and integral1/A<infinity.
Thus the space is complete and the outer/center traces are intrinsic.

Smooth compactly supported functions of x are dense. To see the potentially
nontrivial center step, first approximate v by smooth compactly supported
functions in s. For such a smooth v, replace it in a shrinking s-neighborhood
of the center s0 by a function constant v(s0) near s0, using
v_delta(s)=v(s0)+cutoff((s−s0)/delta)(v(s)−v(s0)).
Use cutoff0 near0 and1 outside a fixed bounded window. For sufficiently small
delta the alteration is interior and the result still equals v near the
outer endpoints. The derivative alteration is uniformly bounded and supported
on O(delta), so it tends to zero in H1. Pulling this modified v back to x gives
a smooth function off the center, and a constant near the center, hence a smooth
compactly supported physical-x function. This proves density in V_A. Standard
piecewise-linear approximation followed by local smoothing proves the ordinary
H1_0 density used in the first step without requiring a weighted density theorem.

For energy-bounded sets, (3) gives a common modulus of continuity because the
integral of1/A is uniformly absolutely continuous; near zero it gives a Holder
1/4 bound. It also gives a uniform bound from the outer trace. On finite grids
extract convergent subsequences of point values, then use this common modulus
to make them uniformly Cauchy. Thus V_A embeds compactly into continuous
functions, and in particular into L2. This proof does not invoke a uniform
lower bound on A. The full form domain is

 V=H1_0(I_h) for xi, times V_A for psi, times H1_0(I_h) for eta. (5)

It is complete, has dense smooth test triples, and embeds compactly in the
kinetic space H defined by (2). Ordinary H1 components have their usual
square-root modulus, obtained by the unweighted version of (3). Dense smooth
triples also make V dense in H.

## 3. A sufficient full coupled positivity bound

Set

 E_d=integral cs² d²/rho, E_p=integral A psi'²/C,
 E_eta=integral J eta'²/C.

For the fluid coupling, elementary 2ab<=a²/2+2b² and (3) imply

 2|integral d psi| <= E_d/2 + (2rho_max/cs²)||psi||_2²
                       <=E_d/2+alpha E_p,
 alpha=2C rho_max ell I_A/cs².                       (6)

For the mixed scalar-scale term,

 (2/C)|integral q_s eta psi'|
       <=E_p/2+(2/C)integral(q_s²/A)eta²
       <=E_p/2+(2Qh ell²/J)E_eta.                    (7)

Here ||eta||_2²<=ell²||eta'||_2² is sufficient; no sharp Poincare constant is
needed. The negative part of m contributes at worst (Mh ell²/J)E_eta.
Combining all terms of (1) gives

 Q>=E_d/2+(1/2−alpha)E_p+(1−beta)E_eta,
 beta=ell²(2Qh+Mh)/J.                               (8)

Along the SAME central solution shortened symmetrically, alpha=O(h^(3/2))
and beta tends to0 (at worst O(h²)); rho extrema remain bounded and positive.
Therefore for all sufficiently small positive h one can require

 alpha<=1/4, beta<=1/2,
 Q>=E_d/2+E_p/4+E_eta/2.                            (9)

This is a theorem about an induced short patch, with no numerical or physical
length chosen and no potential coefficients tuned. It includes every fluid,
phi and scale cross term, rather than proving positivity only on a subspace.

The right side controls the norm of V. Indeed d has zero integral, and
xi(x)=−rho(x)^(-1)integral_-h^x d gives
||xi||_2<=ell||d||_2/rho_min and
||xi'||_2<=(||d||_2+||rho'||infinity||xi||_2)/rho_min.
Conversely H1 xi controls d because rho,rho' are bounded. The weighted
phi control is (3), and eta uses the ordinary endpoint inequality. Upper
bounds follow by the same mixed-term estimates and bounded m. Hence Q is
an equivalent Hilbert norm on V, with its symmetric polarization a(u,v).
Completeness of V proves that this positive quadratic form is closed.
The accepted noncoercivity in ordinary H1 triples is unchanged: V has a
weaker phi derivative norm and includes functions outside ordinary H1.

For an explicit symbolic bound relative to kinetic norm, the same estimates
show

 N<=[rho_max² ell²/(cs² rho_min²)] E_d
                       +tau ell I_A E_p+(sigma ell²/J) E_eta.

Under (9), define

 T_h²=max{2rho_max² ell²/(cs² rho_min²),
                         4tau ell I_A, 2sigma ell²/J}.

Then Q>=N/T_h²>0 for nonzero u. Each entry in this maximum has time-squared
units. This is a symbolic sufficient gap, not a computed physical frequency.

## 4. The actual operator and transmission conditions

Define L by u in D(L) if u in V and there is f in H with

 a(u,v)=<f,v>_H for all v in V; set Lu=f.             (10)

Let H_f=cs²d/rho+psi and F=A psi'−q_s eta. The differential expression is

 (Lu)_xi=H_f',
 tau (Lu)_psi=C d−F',
 sigma (Lu)_eta=−J eta''+m eta−q_s psi'.             (11)

These are distributional equations on the WHOLE interval, not separate
operators with a wall at zero. Since q_s/sqrt(A) is bounded, q_s psi' is L2
for every u in V. Also F is L2 since A is bounded. It follows that the exact
operator domain is

 D(L)={u in V: H_f in H1, F in H1, eta in H2}.        (12)

Necessity follows from (11) with f in H, using positive bounded kinetic
weights and the preceding L2 controls. Conversely these conditions make all
expressions (11) L2. Integration by parts first on the dense smooth tests,
then continuity in the V norm, gives (10), proving sufficiency. Integration
against the weighted psi derivative is legitimate: F/sqrt(A) is L2 and
psi' is L1, while approximation or the global H1/AC identity fixes the same
boundary expression. The fixed outer traces make those endpoint terms vanish.

Thus center transmission includes continuity of xi,psi,eta from V, and
continuity of H_f, F and J eta' from (12). The fluxes are derived from weak
source equations, not imposed independently. A jump in one of these would
produce a delta distribution unmatched by an H right-hand side. There is
no requirement F(0)=0. Although A(0)=q_s(0)=0, psi' may diverge like1/A;
its limiting product F can be nonzero because integral1/A is finite.

There is an explicit admissible operator-domain control for this last point.
Choose v(s) smooth and compactly supported, with nonzero constant derivative
near s0, and put psi=v(s(x)), eta=0. Then A psi'=v_s(s(x)) is constant near
the center and H1 on the whole interval. Set

 c=M_h^(-1)integral rho psi, d=rho(c−psi)/cs²,
 xi=−rho^(-1)integral_-h^x d, M_h=integral rho.

Its mass perturbation is zero, xi has zero outer traces and is H1, and H_f=c
is constant. Thus this full triple belongs to D(L), while F(0)=v_s(s0) is
nonzero. q_s psi' remains L2. A reflecting center boundary would wrongly
exclude this legitimate state. It would change the physical problem.

## 5. Compact inverse, spectrum and linear energy evolution

Here are the special functional-analytic steps used rather than an unsupported
appeal from positivity to a spectral conclusion. For f in H, the functional
v -> <f,v>_H is continuous on the complete Hilbert space (V,a). Representing
it in that inner product, equivalently minimizing Q[v]/2−<f,v>_H, gives a
unique u=T f in V and a bound ||Tf||_V<=constant||f||_H. The minimization can
be obtained from a bounded minimizing sequence, weak Hilbert convergence and
weak lower semicontinuity of the norm; uniqueness follows from strict
convexity. Thus T:H->H is compact by the compact embedding already proved.
Moreover <f,Tg>_H=a(Tf,Tg)=<Tf,g>_H and
<f,Tf>_H=Q[Tf]>0 for f nonzero. If Tf=0 then f is orthogonal to dense V,
hence zero; T is injective and has dense range by symmetry.

For completeness, the compact positive operator has an orthonormal eigenbasis
by the following construction. Maximize <Tf,f> over the H unit sphere. A
maximizing sequence has a weakly convergent subsequence and, by compactness,
strongly convergent T images, so its positive supremum is attained on a unit
vector. Variation yields an eigenvector with this largest positive eigenvalue.
Repeat on its orthogonal complement, invariant under symmetry. The resulting
positive eigenvalues theta_n tend to zero: otherwise their orthonormal
vectors would have T images separated by a fixed distance, contradicting
compactness. If the orthogonal complement of the constructed vectors were
nonzero, positivity/injectivity would give a positive Rayleigh value there,
contradicting theta_n->0 and maximality at each step. Thus the eigenvectors
are complete. The separable L2 Hilbert space and ordinary bounded-sequence
weak extraction are sufficient for this argument; no continuum spectral
approximation is involved.

L=T inverse on its range is consequently the diagonal positive self-adjoint
operator with eigenvalues lambda_n=1/theta_n, tending to infinity, counted
with multiplicity. Its domain has sum lambda_n²|u_n|² finite. The form domain
has sum lambda_n|u_n|² finite: eigenvectors are orthogonal also in a, and any
V vector a-orthogonal to all of them is H-orthogonal to the complete H basis,
hence zero, giving completeness also in the form norm. These statements
prove self-adjointness and compact inverse for the actual domain (12).
The symbolic bound above gives lambda_n>=1/T_h²>0. This is a linear
longitudinal wall-system spectrum, not a physically calibrated mode claim.

For initial displacement u0 in V and velocity v0 in H, set in this eigenbasis

 u_n(t)=u0_n cos(sqrt(lambda_n)t)
               +v0_n sin(sqrt(lambda_n)t)/sqrt(lambda_n).

Termwise oscillator conservation and square-summable energy tails give
u in C(R;V), u_t in C(R;H), with u_tt+Lu=0 weakly in V dual and conserved
energy [Q[u]+N[u_t]]/2. Uniqueness follows by taking each eigencomponent.
If u0 is in D(L) and v0 in V, the same weighted sums give strong evolution
C(R;D(L)) intersect C1(R;V) intersect C2(R;H). No spectral sweep was used.
This earns well-posed linear energy evolution in the declared spaces; it is
not nonlinear Cauchy well-posedness, nonlinear stability, or the earlier
H2 fixed-wall parameter-response theorem.

## 6. Physical and logical scope

The construction uses both registered positive a_ref values9.3619e-11 and
1.1279e-10 m/s² as separate hypotheses. Each yields its own actual background
and sufficiently short allowed patch; no shared measured length is inferred.
Constant-vacuum, frozen a(0)E(z) comparisons and evolving-H scale are distinct.
The last would require the missing exchange/reservoir treatment. Spatially
responsive a=a_ref exp(chi) remains an added diagnostic assumption and does
not establish the literal pointwise scale-vacuum identity.

Signed source balance is always B'=C rho with Q flux. No Newtonian missing
mass is substituted. RAR transfer is open and no registered M action is
invented. No physical V is fitted. The operative filtered MONO, physical
metric/photon/DOF, conserved physical scale sector and instrument calibration
remain separate unresolved obligations. No empirical or global-theory closure.

Failed shortcut preserved: ordinary H1 coercivity cannot be recovered by this
argument; its localized counterexample remains valid. Also, treating the
center as two independent walls would discard continuous weighted states and
the nonzero-flux control above. What is established is a positive closed
weighted coupled form and its linear operator on sufficiently short induced
patches of the same crossing. A nonlinear or fixed-constraint parameter
response through the cusp needs its own nonlinear map/domain theorem.
