# PF01–PF02: what AC2q does and does not determine at a shock

2026-11-06. Base 60263a84e20aaa1c98ba3729708f4171d059a253;
PF01 criteria 57f9b8140d; PF02 criteria 21cb54b10b.
Evidence labels: internal analytic derivation plus symbolic identities and finite
numerical corroboration. Self-review only. No global AC2q failure theorem.

## 1. Correct the question before interpreting AC10

AC10 stops its interior event at J=1e-3 and calls it FOLD. Its auxiliary first-event
reading also uses 1e-3. Neither is J=0. Its RHS sets Pi=0 when J<=0 and continues
sorting labels; that is not a field-theory prescription for a multivalued clock.
The first-event output can inform pre-event compression; later interior behavior
cannot establish a physical post-fold solution. X14 itself estimates native
positive-charge pressure can matter around J~1e-5 at large Mach number. Thus
AC10 does not distinguish a positive-charge true caustic from a pressure shock.
This does not overturn its frozen NO VERDICT or its finite compression results.

Let q=P_x+s^2 denote the leading PN charge, v=-sigma_x, s=background scalar time
slope, and gamma>0. AC10's leading planar equations before breakdown are

    q_t + (q v)_x = 0,
    v_t + (v^2/2 + gamma max(q,0))_x = F,
    F = W_P - Phi_x.

Here W_P is the actual hold-law derivative; replacing it by K M P is an additional
local approximation. A bounded F contributes no delta to the finite-jump
conditions. Dropping F for evolution is a principal-system approximation, not
an exact gravitating AC2q solution. For smooth q>0 these imply

    (q v)_t + (q v^2 + p)_x = q F,   p=gamma q^2/2,
    E_t + [v(E+p)]_x = q v F,       E=q v^2/2+gamma q^2/2.

Multiplication and the chain rule used here are not legitimate across an
unspecified discontinuity. A post-shock scheme must state which equations
hold distributionally and account for the defects in the others.

## 2. Native pressure does not ensure a globally smooth principal system

For F=0, q>0 let c=sqrt(gamma q). Eigenvalues are v±c and Riemann invariants
v±2c. Hold v-2c=-2c0. Then v=2(c-c0) and

    c_t + (3c-2c0)c_x = 0,
    x=a+[3c_init(a)-2c0]t,
    c_x=c_init'(a)/[1+3c_init'(a)t].

For gamma=c0=1 and c_init=1+0.4 sin a, first breaking is t_b=5/6,
with 0.36<=q<=1.96 and |v|<=0.8. Density and velocity stay bounded;
their gradients diverge. This is a shock-forming gradient catastrophe,
not a proof that density goes to infinity or that the label Jacobian is zero.
The units here are local sound-speed units, not units of light speed; these
numbers do not imply a relativistic physical velocity.

This exact example belongs to the source-free leading principal system. It
cannot by itself prove breakdown for the full covariant action: a controlled
short-wavelength limit and an effective-theory validity range are still needed.
A positive pressure replaces some dust crossings by shocks, not by globally
smooth flow. The expanding affine-wave control has no future characteristic
crossing on its local patch. Reversing a periodic sine merely moves its
compressive portion; it would not remove breaking globally.

## 3. Finite positive-charge shocks: an exact PN obstruction

Work in the shock rest frame and write a=q_L>0, b=q_R>0, u=v-S,
j=a u_L=b u_R. Assume bounded sources and no surface charge or stress.
Mass plus the scalar/potential Bernoulli jump gives

    [u^2/2+gamma q]=0,
    j_B^2 = 2 gamma a^2 b^2/(a+b).

Mass plus momentum conservation gives

    [j^2/q+gamma q^2/2]=0,
    j_M^2 = gamma a b(a+b)/2.

Their difference is

    j_M^2-j_B^2 = gamma a b(a-b)^2/[2(a+b)].

It vanishes only for a=b. No nontrivial bounded positive-charge shock can
satisfy all three conditions. More explicitly,

    momentum defect on the Bernoulli branch = gamma(b-a)^3/[2(a+b)],
    Bernoulli defect on the momentum branch = -gamma(b-a)^3/(4ab).

These are exact identities, not numerical errors. Weak shocks hide the mismatch
at cubic order; strong shocks do not. Energy flux is also not automatically
conserved by either continuation. An entropy inequality is a selection rule,
not an accounting of where lost gravitationally coupled stress goes.

## 4. Exact relativistic scalar terms do not cure a defect-free planar corner

This section retains the full flat-space stationary AC2q matter action on the
positive switch branch; it is not the PN expansion above. It proves a necessary
interface obstruction under the stated restrictions, not a global evolution result.

Assume gamma>0 and stationary field profiles P=P(x), phi=s t+psi(x),
with a planar interface stationary in a local inertial frame, no unbounded
metric/tangential gradients, continuous phi and P, bounded one-sided derivatives,
finite W and V, X>0, and no surface stress or unresolved oscillatory defect.
The same-sign nonzero velocities are the usual through-flow case; negative
velocities follow by reflection. Define

    phi=s t+psi(x), v=-psi'/s, y=sqrt(1-v^2), C=1/y,
    n=(C,Cv), e=(Cv,C), P^mu=P e^mu, d=P', B=2X=s^2 y^2.

Here s>0 is the time slope in the interface rest frame, not assumed equal to its
cosmological-frame value. Direct tetrad contraction gives

    D.P = C P',    P.A=P C'.

For continuous P, integrating P C' by parts yields -C P'. With z=C d, the
stationary density, up to a boundary term and continuous -W-V, is

    L(v,d) = -z + B/2 - gamma z^2/2 - gamma z B.

Because W_P and the explicit-phi sources are bounded, the necessary corner
conditions are continuity of L_d, L_v (proportional to scalar current), and
v L_v+d L_d-L (spatial momentum flux). The last condition assumes no localized
stress defect. This is not obtained by assuming conservation through an arbitrary
weak solution; it is explicitly part of the tested physical continuation class.

Set L_d=-A. Then A=C[1+gamma(z+B)]>0 on the on-branch. Eliminate d and use the
partial Legendre transform f=L+A d (continuous W,V drop from jumps):

    epsilon=gamma s^2,
    f(v) = { [A sqrt(1-v^2)-1-epsilon(1-v^2)]^2
              + epsilon(1-v^2) }/(2 gamma).

The remaining two corner conditions require

    f'(v_L)=f'(v_R)=j,
    v_L j-f(v_L)=v_R j-f(v_R).

For 0<v<1,

    f'''(v) = (3v/gamma) {4 epsilon^2
       + A/(1-v^2)^(5/2) [1-epsilon(3-2v^2)(1-v^2)]}.

Since 0<(3-2v^2)(1-v^2)<3, f'''>0 for 0<=epsilon<1/3.
Thus f' is strictly convex. If v_L<v_R and both endpoints equal j,
f'(v)<j strictly between them. Therefore

    [v j-f(v)]_L^R = integral(v_L,v_R) [j-f'(v)] dv > 0.

The momentum-flux equality is impossible. Reflection covers two negative
velocities. Equal velocities imply equal d from L_d and hence no finite jump.
The equality case epsilon=0 is only a formal limiting check because a physical
clock requires s>0; the proof includes positive epsilon.

This excludes the stated defect-free on-branch finite planar shocks even when
the exact canonical scalar and relativistic normalization are retained. It does
not require a Taylor expansion in epsilon. The gamma*s^2~1e-17 values in the
project are far inside this range in their stated frames, but no frame-independent
bound or new solar/galaxy regrade is asserted here.

The argument does NOT establish that the full action forms such a shock from
smooth data. Nor does it exclude a continuous dispersive layer, an oscillatory
weak limit with stress, a dynamically accumulating surface layer, a switch
crossing, or singular gravitational junction terms. Those require their own
solution and conservation analysis. In particular a generic PDE shock is not,
by itself, proof that a fundamental theory is inconsistent.

## 5. What the numerical experiment discriminates

The two source-free finite-volume schemes use respectively conserved variables
(q,v) and (q,m=qv). Both approximate the same smooth equations. Their weak
continuations are different theories of the discontinuity; this experiment
must not be cited as two solutions of one already specified weak Cauchy problem.

Periodic smooth initial data from section 2 were evolved at N=256,512,1024,2048.
At t=0.3<t_b both converge toward the independently inverted characteristic
solution. At t=1.5>t_b, their mean absolute density differences are
0.082162, 0.082479, 0.082521, 0.082548. The mean initial density is 1.08;
thus the finest discrepancy is about 7.64% of that mean. Successive-resolution
errors at N=1024 versus 2048 are 0.001320 and 0.001624 respectively, much smaller
than their difference. This supports persistent prescription dependence, not a
proof of continuum uniqueness for either solver.

The mean-zero spatial primitive of the density differs by 0.236253 at N=2048.
It is the planar Poisson-source diagnostic up to the gravitational coupling;
it is NOT a solved self-consistent gravitational force in these F=0 runs.
Thus the difference is not confined to unresolved peak densities.

Independent symmetric-collision Riemann data q0=gamma=U=1 give:

| continuation | central q | shock speed | missing condition |
|---|---:|---:|---|
| mass + scalar/Bernoulli | 2.2807764064 | 0.7807764064 | momentum defect magnitude 0.3201941016 |
| mass + momentum | 2.1700864866 | 0.8546376797 | Bernoulli defect magnitude 0.1845511931 |

The two shock speeds differ by about 9.46% relative to the first. Numerical
Riemann errors decrease under all four resolutions. The analytic branches
remain distinct independently of the numerical experiment.

## 6. What would change the conclusion

1. A full-action regular evolution could avoid this shock class altogether.
   Show it with a controlled source/metric/clock evolution and an effective-theory
   validity estimate, rather than extrapolating the principal-system example.
2. A derived weak completion could retain an energy/momentum defect carried by
   native unresolved modes or an evolving surface layer. Derive its equations,
   initial data and selection from the action; establish regulator-independent
   observables. A finite-volume entropy rule alone does not do that.
3. A physical extension could add dissipative degrees of freedom, a dispersive
   operator, or another carrier. Each requires stability and empirical rechecks.
   This work does not prove that a new fitted constant is unavoidable.

Current classification: ordinary conservative finite shocks do NOT close AC2q.
The as-used classical/single-clock description needs a justified continuation
or extension before it is a post-break predictive theory. The full covariant
model is not proved globally false; whether its native dynamics provide that
completion remains open.
