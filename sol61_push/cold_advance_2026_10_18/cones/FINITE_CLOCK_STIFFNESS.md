# Finite clock stiffness: a bounded covariant construction

Date: 2026-10-18 (local session date). Base repository HEAD:
`3c01aa2861bf576f4c2d942251eb9d2f89cae108`; the shared working tree was dirty.
No frozen action, criterion, old result or live run was changed.

**Primary verdict: conditional on a named input.** If an independent positive
clock compressibility is admitted as the explicit operator below, there is a
finite, covariant, two-field effective action with the exact cubic static
response and positive quadratic energy whose local characteristic speeds all
lie inside or on the matter cone on any specified compact nonzero gradient
band. Its required stiffnesses are given by necessary and sufficient
inequalities, not a sample. This adds a model coefficient; the present particle
bridge does not derive it. This is neither a completed gravity theory nor a
matched ultraviolet completion.

The audit of the existing canonical-clock determinant passes at its stated
scope. The construction below is a separate research attempt, self-reviewed by
independent expansion and exact symbolic controls; it does not regrade the old
model or close its ultraviolet matching obligation.

## 1. Claim card and conventions

Use signature (-+++), c=1 and a fixed flat matter metric. Let theta be a genuine
varied shift-symmetric clock, phi the scalar response, and define

    X = -g^{mu nu} partial_mu theta partial_nu theta > 0,
    u^mu = -partial^mu theta / sqrt(X),
    h^{mu nu} = g^{mu nu} + u^mu u^nu,
    y = sqrt(h^{mu nu} partial_mu phi partial_nu phi),
    U = u^mu partial_mu phi.

Consider the explicitly proposed first-derivative covariant Lagrangian

    L = P(X) + A(y) U^2/2 - F(y),
    F(y) = gamma y^3/3,
    A(y) = Z0 + 2 gamma y,
    gamma > 0, Z0 > 0.

The background is theta=omega t, phi=y x, with constant omega>0 and y>0.
Local frozen-coefficient analysis of a smooth static nonconstant y(x) uses the
same principal symbol; it does not establish a self-consistent metric solution.
Set X0=omega^2 and define the two clock coefficients at this background by

    kappa = 2 P_X(X0),
    Delta = 4 X0 P_XX(X0),
    B = kappa + Delta.

This X convention has no factor 1/2. These factors matter when translating to
other P(X) records. kappa is the bare clock spatial coefficient, Delta its
extra temporal coefficient, and B its full temporal coefficient. The canonical
clock in the old calculation has Delta=0. The old adiabatic calculation instead
sets Delta=kappa(1/c_s^2-1), valid only below the integrated amplitude gaps.

The precise proposition is: for the displayed action at each such background,
positive definite quadratic derivative energy and all real characteristic
speeds 0<c^2<=1 for every propagation direction hold if and only if

    kappa > (Z0 + gamma y) y^2 / X0,                         (E)
    Delta >= gamma (Z0 + gamma y) y^3 / (Z0 X0).             (C)

Under the stipulated positive gamma,Z0,y these bounds automatically give B>0.
Strict (C) gives c^2<1. Positive definite energy excludes zero-speed spatial
boundaries. No claim includes y=0, arbitrary backgrounds with U!=0, metric
backreaction, quantum stability, dynamical preservation of the gradient band,
or all frequencies of a microscopic completion.

## 2. Independent covariant expansion

Put theta=omega t+pi and phi=y x+chi. At first order

    U = chi_dot - (y/omega) pi_x.

At second order

    y_field^2 = y^2 + 2 y chi_x + |grad chi|^2
                - (2 y/omega) chi_dot pi_x
                + (y^2/X0) pi_x^2 + O(perturbation^3).

The chi_dot^2 terms cancel inside y_field^2. Derivatives of A(y) first enter
A(y)U^2 at cubic order, since U vanishes on the background. Expanding P(X),
F and A then yields, up to irrelevant background and linear terms,

    L2 = A chi_dot^2/2 + B pi_dot^2/2
         - C_parallel chi_x^2/2 - C_perp |grad_perp chi|^2/2
         - kappa |grad pi|^2/2 + r pi_x^2/2 - d chi_dot pi_x,

    C_parallel = 2 gamma y,
    C_perp = gamma y,
    q = A - C_perp = Z0 + gamma y,
    r = q y^2/X0,
    d = q y/omega.

Thus d^2=q r. Keeping the clock variation is essential: fixing pi=0 would
discard the term that obstructs the common cone in the original ansatz.

For a wave whose unit wave vector makes cosine mu with x, set t=mu^2 in [0,1].
The two-field principal matrix (the off-diagonal sign depends on Fourier
convention and does not change the determinant) is

    M(v,t) = [ A v^2 - C(t),       d mu v ]
             [ d mu v,            B v^2 - E(t) ],
    C(t) = gamma y (1+t),
    E(t) = kappa-r t,
    v = omega_wave/|k|.

Its dispersion polynomial is

    A B z^2 - (A E + B C + d^2 t) z + C E = 0,  z=v^2.

The Hamiltonian in velocities is the sum

    H2 = A chi_dot^2/2 + B pi_dot^2/2
         + C_parallel chi_x^2/2 + C_perp |grad_perp chi|^2/2
         + (kappa-r) pi_x^2/2 + kappa |grad_perp pi|^2/2.

Equivalently the momentum form has (p_chi+d pi_x)^2/(2A) and p_pi^2/(2B).
The mixed term cancels from H2; it cannot compensate E<0. Consequently
positive definite derivative energy is exactly A,B,C_parallel,C_perp>0 and
kappa>r, with the last inequality being the new nontrivial spatial condition.

## 3. Exact 2x2 cone criterion and angular reduction

For any fixed direction with A,B,C,E>0, define

    S=A E+B C+d^2 t,
    p(z)=A B z^2-S z+C E.

Both roots are real and positive, because

    S^2-4 A B C E = (A E-B C)^2
                    +2 d^2 t(A E+B C)+d^4 t^2 >= 0.

The larger root is at least max(C/A,E/B), while the smaller is at most
min(C/A,E/B): substituting either diagonal ratio gives p<=0. Therefore both
roots are <=1 if and only if

    A-C >= 0,
    B-E >= 0,
    (A-C)(B-E)-d^2 t >= 0.                                 (*)

This is also the positive semidefiniteness criterion for M(1,t). In the present
case the determinant at the matter cone simplifies exactly to

    f(t) = Delta (q-gamma y t) - gamma y r t^2.

At t=0, (*) requires Delta>=0. For Delta>=0,

    f'(t) = -gamma y Delta - 2 gamma y r t <= 0.

Thus the radial direction t=1 is exactly the worst direction, not merely one
sample. There A-C=Z0 and

    f(1)=Z0 Delta - gamma y r.

It follows that (E) and (C) are necessary and sufficient for positive quadratic
energy and the stated all-direction speed bound. This proves the proposition.
For matter-timelike covectors v>1 the principal matrix is positive definite;
the same branch of the two-field hyperbolicity cone contains those covectors.
This is local principal-symbol control. It does not supply a global time
function or a nonlinear Einstein-matter Cauchy theorem.

## 4. What is minimally new, and what cannot repair the old clock

The old script's exact radial canonical determinant is recovered at Delta=0:

    f(1) = -gamma (Z0+gamma y) y^3/X0 < 0.

Making kappa arbitrarily large does not change this negative determinant.
A small positive speed excess can tend to zero in a stiff-clock limit without
becoming a nonpositive excess at any finite kappa.

More generally, keep an arbitrary fixed-clock response coefficient A(y), let
C_perp=F'(y)/y>0 and C_parallel=F''(y)>C_perp, and assume A>C_parallel.
Then q=A-C_perp, r=q y^2/X0, and the same calculation gives

    f_radial=(A-C_parallel)Delta-(C_parallel-C_perp)r.

Hence the exact required extra clock temporal stiffness is

    Delta >= (C_parallel-C_perp)(A-C_perp)y^2
             / ((A-C_parallel)X0).

At Delta=0 it is strictly impossible for every finite A in this class.
Increasing only phi's temporal coefficient therefore cannot cure the canonical
clock obstruction. A nonzero temporal margin in the clock itself is required
(or a genuinely different derivative structure). This generalization is an
algebraic statement for the stated separable action, not a no-go for all medium
actions.

A single covariant operator realizes any desired constant Delta at X0:

    P(X)=kappa X/2 + Delta (X-X0)^2/(8 X0).

It changes P_XX(X0) but has zero value and first derivative at X0. It therefore
changes neither the background clock stress/current at X0 nor the static
response action at U=0,X=X0. On that static branch the phi equation remains

    div(gamma |grad phi| grad phi) = prescribed source

for a fixed linear source coupling and sign convention. Its spherical
source-free nonzero-flux solution has |grad phi| proportional to 1/r, as for
the cubic MOND response. The force normalization, attraction/lensing dictionary
and realistic source coupling remain additional inputs. The temporal operator
has not been obtained by integrating out the particle bridge; it is an explicit
new effective coefficient. Coupling it to a full metric requires solving that
same action, rather than transferring the fixed-flat-space result directly.

## 5. Finite-band construction and exact witness

On a prescribed band 0<y<=Y, both right sides below are increasing in y, so
constant coefficients suffice precisely when

    kappa > (Z0+gamma Y)Y^2/X0,
    Delta >= gamma(Z0+gamma Y)Y^3/(Z0 X0).

Uniform positive spatial energy additionally needs y>=y_min>0. At y=0 the
cubic response has zero spatial quadratic coefficient even though A(0)=Z0.
No finite constant kappa can satisfy the first bound at arbitrarily large y;
no finite constant Delta can satisfy the second. This construction is bounded
by design. Choosing an unbounded-gradient stiffness function changes the
action and can generate additional principal mixing that must be rederived.

A fully rational normalized example is

    gamma=Z0=X0=1, kappa=3, Delta=3, 0<y<=1,
    P(X)=3 X/2+3(X-1)^2/8.

Both bounds have margin at y=1: r=2<3 and Delta_min=2<3. At the radial upper
endpoint A=3, B=6, C=2, E=1, d=2, and

    p(z)=18 z^2-19 z+2,
    z_-= (19-sqrt(217))/36,
    z_+= (19+sqrt(217))/36 < 34/36 < 1.

The inequalities above prove the whole band and all angles; these endpoint
roots are an exact independent check. The chosen numbers are a constructive
example, not measured or theoretically selected parameters.

The existing M10 low-energy record already supplies a positive Delta through
its small sound speed. That is why some sampled adiabatic rows pass, and why
this note does not claim discovery of low-energy cone control. The new content
is the angular proof, necessary/sufficient finite-band inequalities, explicit
covariant operator and rational witness, plus the proof that stiffening only
phi cannot repair a canonical clock. A fundamental P(X) temporal operator
would persist at its own effective principal level; whether it is generated
and remains valid above the existing amplitude gaps is a new matching task.

## 6. Relation to the latest vector obstructions

CE-FM-074 shows that the electric vector attachment has a degenerate quadratic
vacuum and a logarithmically divergent unregulated isolated exterior tail.
CE-FM-075 v2 then derives an exact mixed E/B common-cone counterexample for the
specified Maxwell-regulated, single-invariant L(F) extension. Both records were
read, including the v2 row-normalization correction; their latest v2 result,
not the failed original script, is the comparison baseline. Neither record
excludes the two-scalar clock-dependent action studied here, and this note does
not remove their vacuum/exterior obligations or donate their electric force
response to the new scalar model. In particular, a cubic scalar 1/r static
field still needs a boundary/compensation/crossover analysis if a finite
isolated exterior is claimed. No magnetic background is part of this action.

## 7. Dependency and obligation record

Dependencies: [internal definitions of X,u,y,U] -> [quadratic expansion] ->
[Hamiltonian sign + dispersion polynomial] -> [2x2 root criterion] -> [angular
monotonicity] -> [finite-band inequalities] -> [explicit P(X) witness].
The microscopic origin of P_XX and the source/metric dictionary are unchecked
physical inputs, not theorem leaves asserted by citation.

| Obligation | Status | Evidence/limit |
|---|---|---|
| Existing canonical determinant | Passed at stated scope | Independent radial recovery above |
| Covariant reciprocal clock variation | Passed for proposed action | Full expansion in section 2 |
| Quadratic positive energy | Passed under (E),(C) | Explicit Hamiltonian |
| All propagation angles | Passed under (E),(C) | Monotone exact f(t) |
| Static cubic response unchanged | Passed on U=0,X=X0 branch | Added operator vanishes with first derivative |
| Bounded normalized witness | Passed | Rational coefficients and exact roots |
| Uniform vacuum spatial coercivity | Failed for pure cubic | C_perp=gamma y -> 0 |
| Arbitrarily large gradient band, fixed coefficients | Failed | Required kappa~Y^3, Delta~Y^4 |
| Matched microscopic temporal operator | Conditional | Not derived from mediator/host |
| Nonlinear preservation of allowed band | Not addressed | Requires evolution/background solution |
| Metric/lensing/source/cosmology completion | Out of scope | Fixed metric calculation |
| External theorem/source | None used | Elementary derivation, no literature claim |

The cheapest next discriminating check is to choose whether the matched host
actually generates a nonzero P_XX operator that survives at the frequencies
being claimed, then derive its coupled amplitude/clock/response symbol before
integrating amplitudes out. Without that input, the present result is an exact
effective-model construction and a quantified price, not physical closure.

## 8. Verification and provenance

One bounded stdin Python process independently differentiated the displayed
covariant Lagrangian to second order. It checked the quadratic expansion,
angular and radial identities, canonical mutation, angular derivative,
principal polynomial, exact rational-witness polynomial/roots and unchanged
input hashes. All 10 controls passed; Python 3.9.6, SymPy 1.14.0,
macOS-26.5.2-arm64-arm-64bit, runtime 0.56620775 s, exit 0, 30 s SIGALRM cap.
No random inputs, numerical root approximations, arrays or simulations were
used. The mathematical result rests on the displayed proof; the symbolic
calculation cross-checks finite identities. The full executed command is in
this chat's tool record. There is no validated v2 run manifest: only this note
was authorized as a persistent artifact, so no run directory or script was
created. The old historical run was read and audited, not rerun or modified.

Core regeneration command (no file outputs):

```bash
python3 - <<'PY'
import sympy as s
import signal
signal.alarm(30)
e=s.symbols('e', real=True)
w,y,g,Z,k,D=s.symbols('omega y gamma Z0 kappa Delta', positive=True)
pt,px,py,pz,ft,fx,fy,fz=s.symbols('pt px py pz ft fx fy fz', real=True)
X=(w+e*pt)**2-e**2*(px**2+py**2+pz**2)
U=((w+e*pt)*e*ft-e*px*(y+e*fx)-e**2*(py*fy+pz*fz))/s.sqrt(X)
Y2=(y+e*fx)**2+e**2*(fy**2+fz**2-ft**2)+U**2
L=k*X/2+D*(X-w*w)**2/(8*w*w)+(Z+2*g*s.sqrt(Y2))*U**2/2-g*Y2**s.Rational(3,2)/3
L2=s.simplify(s.diff(L,e,2).subs(e,0)/2)
A=Z+2*g*y; q=Z+g*y; r=q*y*y/(w*w); d=q*y/w
expected=A*ft*ft/2+(k+D)*pt*pt/2-g*y*fx*fx-g*y*(fy*fy+fz*fz)/2-k*(px*px+py*py+pz*pz)/2+r*px*px/2-d*ft*px
assert s.simplify(L2-expected)==0
t,v=s.symbols('t v', real=True)
C=g*y*(1+t); E=k-r*t; B=k+D
f=s.factor((A-C)*(B-E)-d*d*t)
assert s.simplify(f-(D*(q-g*y*t)-g*y*r*t*t))==0
assert s.simplify(f.subs(t,1)-(Z*D-g*y*r))==0
assert s.simplify(f.subs({t:1,D:0})+g*y*r)==0
assert s.simplify(s.diff(f,t)+g*y*D+2*g*y*r*t)==0
M=s.Matrix([[A*v*v-C,d*s.sqrt(t)*v],[d*s.sqrt(t)*v,B*v*v-E]])
assert s.simplify(M.det()-(A*B*v**4-(A*E+B*C+d*d*t)*v*v+C*E))==0
p=s.factor(M.det().subs({g:1,Z:1,w:1,k:3,D:3,y:1,t:1}))
assert s.expand(p-(18*v**4-19*v*v+2))==0
for z in [(19-s.sqrt(217))/36,(19+s.sqrt(217))/36]:
    assert s.simplify(p.subs(v*v,z))==0
assert 217<225 and s.Rational(34,36)<1
print('9 exact symbolic/algebraic controls passed')
PY
```

Observed SHA-256 input hashes before and after the check were equal:

| Input (repository relative) | SHA-256 |
|---|---|
| sol61_push/closure_particle_bridge_2026_10_16/dynamical_clock_cones.py | db98509ee4ebe68cf1313feee6bcc630a708f8277952e33cf607b6a12557a912 |
| sol61_push/closure_particle_bridge_2026_10_16/dynamical_clock_cones_contract.json | 9e4f36056c39085657d707d7d7aac790a08a677c2f27f5e8b9532f642311f4d0 |
| sol61_push/closure_particle_bridge_2026_10_16/dynamical_clock_cones_run_001/results.json | 423e1b88d0b7d08f95946950ff53073e0c0ca565a3e27e10bac4de853fbf8bd7 |
| sol61_push/closure_particle_bridge_2026_10_16/mediator_phase_matching_run_002/results.json | e2df12078387b810f130932499ea26936df8a65cce75f23bfa9fcbb84f79ad36 |
| sol61_push/cold_final_mile_2026_10_13/VECTOR_ATTACHMENT_LIMITS_RESULT.txt | a85c054007213c37cbe7a667119f1234edf0522470a9aa133b465cb58ff1dcc1 |
| sol61_push/cold_final_mile_2026_10_13/VECTOR_MIXED_BACKGROUND_RESULT.txt | 0f0e7b0fcc7d5ca62160ef5a4808addd5c60bc9654943baf302b234f2a24c7ef |
| sol61_push/cold_final_mile_2026_10_13/check_vector_mixed_background_v2.py | afb55b804b25f943ff5943595f2a7caedc33eaf9c04d739c1db85ad6503c579f |
| sol61_push/cold_final_mile_2026_10_13/vector_mixed_background_contract_v2.json | fd0aa7c7410e0236e77faf9643e039fae0620c98363e62896194eb593e2fbcb7 |
| sol61_push/cold_final_mile_2026_10_13/vector_attachment_limits_contract.json | 651b439365b81c9033bb722df27c8bd0fecb36891b152ddd8961949f1d30b546 |

Review provenance: separate subagent derivation against the parent's supplied
raw artifacts at the stated HEAD. Existing identities were independently
reconstructed; the new construction and prose are self-reviewed, not an
external certification. No external literature claim is being made.

## 9. Separate continuation using the full-W scalar constitutive function

The general formula in section 4 also admits an explicit scalar response with
the same nonlinear residual function used in the full-W static screening
ODE. This is a separate effective scalar action. It is not an identification
with the original vector polarization, its inertial stock, or its Poisson
normalization.

Write the scalar spatial gradient magnitude as u in this section, to match
the screening function's argument, and choose 0<u<a0. Define

    F(u)=-u^2/2-a0 u-a0^2 log(1-u/a0),
    F'(u)=R(u)=u^2/(a0-u),
    C_perp=F'/u=u/(a0-u),
    C_parallel=F''=u(2a0-u)/(a0-u)^2,
    J=C_parallel-C_perp=a0 u/(a0-u)^2 > 0,
    A(u)=Z0+C_parallel,  Z0>0.

Then q=A-C_perp=Z0+J and r=q u^2/X0. The same covariant action form,
L=P(X)+A(u)(u_clock dot partial phi)^2/2-F(u), gives

    f(t)=Delta(q-J t)-J r t^2,
    f'(t)=-J Delta-2J r t,
    f(1)=Z0 Delta-J r.

Here u_clock denotes the unit timelike vector, while bare u is the scalar
spatial gradient magnitude. Under positive Delta the radial direction is
again the worst direction. Positive quadratic energy and all-direction
matter-cone containment are therefore exactly

    kappa > (Z0+J)u^2/X0,
    Delta >= J(Z0+J)u^2/(Z0 X0).

J increases strictly on (0,a0), since

    J'(u)=a0(a0+u)/(a0-u)^3 > 0.

Thus constant finite coefficients chosen from the upper endpoint work on any
fixed nonzero band u_min<=u<=u_max<a0. There is no uniform finite choice
approaching the wall u=a0: kappa's lower bound diverges as (a0-u_max)^(-2),
and Delta's as (a0-u_max)^(-4). The vacuum spatial degeneracy still remains at
u=0. The added (X-X0)^2 clock operator still leaves this F(u) static branch
unchanged at X=X0,U=0.

This continuation keeps a full-W-like scalar constitutive function, but does
not make the screening mass theorem inapplicable to the original full-W
polarization action. That action has both a polarization equation and a
Poisson flux equation; the new scalar action has a scalar source coupling
that must be specified independently. Transferring the screening force,
carrier mass, attraction/lensing, or finite-stock interpretation would require
a separate derivation. The finite-stock proof audit is recorded separately in
FINITE_STOCK_REVIEW.txt and passes under its own explicit hypotheses.

Validation: a second bounded stdin SymPy process passed six exact identities:
the F primitive, J formula, q formula, angular determinant, radial determinant,
and J' formula. Exit 0, wall time 0.26232225 s, Python 3.9.6/SymPy 1.14.0,
30 s SIGALRM cap; no numerical approximation, random seed or file outputs.
This is a symbolic cross-check of the proof above, not a new empirical result.
The precise full-W primitive and source definitions were cross-checked in the
screening note whose SHA-256 is
`39f99b671342b8b7dc6cfe168e325cd1599fae06e14940b3bf28a1b5e72ce6ed`.
Proofreading self-review covered both new notes: no routine edits or
mathematical-token corrections required; no unresolved prose/notation issues.
