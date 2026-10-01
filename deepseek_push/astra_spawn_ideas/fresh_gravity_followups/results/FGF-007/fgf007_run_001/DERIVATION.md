# FGF007: background-relative gradient energy and its zero-field limit

Worker derivation fixed before any stage21 proof/code inspection. Frozen a>0,
Q and RAR considered separately in the inherited preferred-time scalar action;
K=2 is an adopted positive kinetic coefficient. No physical metric is supplied.

## Exact dimensionless objects

Let x=g0/a>0, h=|delta grad phi|/a, r=h/x, and W(g;a)=a² w(g/a).
Write B/a=b(x), so w'=b and the Hessian eigenvalues are b'(x) parallel and
b(x)/x transverse. Q has b=2x²/(sqrt(1+4x²)+1), b'=2x/sqrt(1+4x²).
For RAR use t=sqrt(B/a), f(t)=t²/(1−exp(−t)), x=f(t), b=t². Evaluate the
denominator as −expm1(−t). With d=1−exp(−t),

 f'(t)=t(2d−t exp(−t))/d², b'(x)=2d²/(2d−t exp(−t)).

At t=0 the regular limits are f=0 and f'=1. f is strictly increasing:
2(exp(t)−1)>t for t>0. Also f(t)>=t, so the positive inverse root belongs
to [0,x]; bisection in this bracket is unique. This defines RAR without
substituting Q. A stable positive primitive is

 w_R(x)=integral_0^t s² f'(s) ds.

Q uses either integral b or its inherited exact asinh primitive. All numerical
values below are high-precision floating evaluations, not interval certificates.

For signed parallel perturbations +/-h with 0<=h<=x, subtract the background
linear term and compare

 Delta_parallel_plus =w(x+h)−w(x)−b(x)h,
 Delta_parallel_minus=w(x−h)−w(x)+b(x)h,
 H_parallel=b'(x)h²/2.                               (1)

The negative sign case at r=1 reaches exactly zero gradient and remains a
valid finite energy increment; its path is not uniformly nonzero-background.
For a transverse perturbation, the linear term vanishes and

 Delta_transverse=w(sqrt(x²+h²))−w(x),
 H_transverse=b(x)h²/(2x).                           (2)

Convexity gives positive increments for h>0. Report Delta/H−1 and the
relative error against Delta, |H/Delta−1|, specifying their denominators.
These are field spatial energies only. K=2 changes neither increment but
sets the linear squared-speed ratios to c² as b'/2 and b/(2x).

For RAR the direct increment can avoid subtraction of nearly equal primitives:
if t0=f inverse(x), t1=f inverse(x+/-h), then (1) equals
integral_t0^t1 (s²−t0²) f'(s) ds. Reversing the bounds in the minus case
makes the integral positive. The transverse increment is
integral_t0^t1 s² f'(s) ds, with t1 corresponding to sqrt(x²+h²).
The endpoint-primitive expression independently checks these direct evaluations.

## Remainder scaling

At each fixed x>0, parallel Taylor expansion gives

 Delta_plus/minus=H_parallel +/- b''(x)h³/6+O(h4),
 Delta/H_parallel−1=+/- [x b''(x)/(3b'(x))]r+O(r²).   (3)

For a transverse perturbation the even geometry cancels the cubic term:

 Delta_transverse=H_transverse
                   +(x b'(x)−b(x))h4/(8x³)+O(h6),
 Delta/H_transverse−1=[x b'(x)/b(x)−1]r²/4+O(r4).    (4)

These are local fixed-x expansions; the bounded computations do not certify
uniform error constants over an arbitrary interval. The deep laws give
b_Q=x²+O(x4), b_R=x²+O(x³), hence w=x³/3+o(x³).
For fixed r in [0,1] as x tends to zero, the limiting exact-to-Hessian ratios are

 parallel plus: 1+r/3; parallel minus: 1−r/3,
 transverse: 2[(1+r²)^(3/2)−1]/(3r²).                (5)

The transverse expression tends to1+r²/4+O(r4). Thus making the background
small with a fixed relative perturbation does not make the normalized Hessian
error disappear. In particular r=1 gives parallel relative ratios4/3 and2/3,
and transverse ratio2(2sqrt(2)−1)/3. These follow from cubic energy, not a
sampled PDE evolution or a strong-coupling/ill-posedness theorem.

## Correct order of limits and zero-field control

For fixed nonzero background, sending h to zero yields Delta/H ->1. At exactly
zero background the Hessian vanishes and the linear term is zero, while

 Delta_0(h)=w(h)=h³/3+o(h³).                          (6)

At fixed small absolute h>0, taking x to zero makes Delta tend to w(h)>0
and H tend to zero for plus-parallel or transverse directions. The ratio
Delta/H therefore diverges; taking h to zero first at fixed x gives1.
The failure concerns the normalized approximation and shrinking relative
linearization neighborhood. The raw Delta tends to zero in BOTH iterated
limits as h and x tend to zero, so there is no claim that the raw energy
limits fail to commute. Along h=r x, both Delta and H vanish as x³, but
their ratio retains (5). The exactly zero-background spatial quadratic form
has no positive stiffness; the adopted K=2 time kinetic term is still positive.
Nothing here proves a ghost, nonlinear ill-posedness, global branch failure,
or the behavior of a coupled matter/metric system.

## Bounded computation contract and units

Only x in {.1,.01,.001}, r in {.001,.03,.3,1}, laws Q and RAR, orientations
parallel plus, parallel minus and transverse are evaluated:72 rows. The same
rows are evaluated at60 and90 decimal digits for precision comparison; this
is not an additional physical parameter scan. RAR inversion uses bracketed
bisection until width <=10^(-(digits−8)) times x, and verifies f(t)=x to a
relative tolerance1e-45. Direct and endpoint-primitive increment comparisons
must agree to relative1e-40; precision comparison must agree to1e-40.
Q inverse and primitive derivatives are checked by analytic formulas/integrals.
At each existing x, w(x)/(x³/3) supplies the zero-background cubic diagnostic,
whose exact leading limit is (6). No finite equality with the leading cubic
law at nonzero x is imposed. No random seed is used. Actual resource caps are
120 seconds wall,110 seconds CPU,1 cooperative numerical-library thread and
1 MiB combined log, supplied by the approved runner; no memory/affinity cap
is claimed. Failure or timeout will be preserved rather than treated as a
physical refutation.

Dimensional restoration uses both a=9.3619e-11 and1.1279e-10 m/s²:
g0=a x, gradient amplitude=a h, Delta W=a² Delta and H_W=a² H.
Energy density is Delta W/(4piG), left symbolic in G rather than importing
an empirical unit-conversion value. For the constant-vacuum branch a is
constant. A frozen H-reference comparison uses a=a(0)E(z) with
E²=.315(1+z)^3+.685; at fixed x,r energies scale as E² and the physical
gradients as E. This is not the same fixed physical gradient comparison.
An evolving H prescription has the inherited W_a a_dot/(4piG) work term,
so a frozen-energy comparison does not establish dynamical conservation.
No registered M action, source mass discrepancy, empirical calibration,
filtered-MONO metric/photon result or historical novelty claim is supplied.
