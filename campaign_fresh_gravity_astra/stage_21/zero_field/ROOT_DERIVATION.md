# Zero-background limit: exact energy versus its quadratic approximation

Root proof fixed before reading any new author/auditor formulas, code or
results. All statements concern the inherited unfiltered scalar Q/RAR
constitutive energy with fixed positive a and K=2. No transfer to filtered
MONO, responsive matter stability or metric theory is assumed.

## Exact object and normalization

For background gradient G with g=|G|>0 and perturbation h, set

 D(G,h)=W(|G+h|;a)-W(g;a)-b(g;a) Ghat dot h,
 H2(G,h)=[b'(g) h_parallel²+(b(g)/g)|h_perp|²]/2.

D is the energy increment with its linear term subtracted; H2 is the
quadratic Taylor energy, not the Hessian itself. W is convex, so D>=0.
Physical field-energy increments are these values divided by C=4piG.
Set x=g/a, y=|h|/a and epsilon=y/x. Constitutive homogeneity gives
b=a bbar(x), W=a² w(x). Keep physical-gradient and dimensionless ratios
separate; holding x fixed across normalizations changes physical g.

For Q, bbar=(sqrt(1+4x²)-1)/2, equivalently 2x²/(sqrt(1+4x²)+1),
w=x sqrt(1+4x²)/4+asinh(2x)/8-x/2.
For RAR, introduce t=sqrt(B/a), x=f(t)=t²/(1-exp(-t)), bbar=t²,
and w(x)=integral_0^t s² f'(s)ds. The inverse branch is unique for t>=0;
f'(t)>0 for t>0. Both representations follow directly from the registered
radial laws. RAR is not replaced by Q or the registered M law.

For parallel signed h/a=s epsilon x, s=+1 or-1, define u=|1+s epsilon|x.
For the task's0<epsilon<=1,

 D/a²=w(u)-w(x)-s epsilon x bbar(x),
 H2/a²=bbar'(x) epsilon²x²/2.

For transverse h, u=x sqrt(1+epsilon²),

 D/a²=w(u)-w(x), H2/a²=bbar(x) epsilon²x/2.

Near small amplitudes direct subtraction can lose digits. Quadrature of
b or of the Hessian along the segment gives independent stable evaluation.
Precision agreement is a numerical check, not a rigorous interval bound.

## Leading energy and relative remainders

Expanding the defining Q inverse gives

 bbar_Q=x²-x⁴+O(x⁶), w_Q=x³/3-x⁵/5+O(x⁷).

For RAR, expanding its defining exponential gives
f(t)=t+t²/2+t³/12+O(t⁵). Inverting yields
t=x-x²/2+5x³/12+O(x⁴), hence

 bbar_R=x²-x³+13x⁴/12+O(x⁵),
 w_R=x³/3-x⁴/4+13x⁵/60+O(x⁶).

These local analytic expansions follow at t=0 from f'(0)=1. They do not
assert that the finite task points are exactly in the cubic theory.
At exactly G=0 and |h|/a small,

 D(0,h)=W(|h|)=|h|³/(3a)+higher order,
 H2(0,h)=0.

The leading spatial energy is cubic. Its vector Hessian at zero is zero,
although W remains strictly convex; strict convexity is not a positive
quadratic lower bound there.

Let theta be the angle between G and h. For fixed epsilon>0 and x->0,
D/(a²x³) tends to

 [(1+2epsilon cos(theta)+epsilon²)^(3/2)-1-3epsilon cos(theta)]/3,

whereas H2/(a²x³) tends to epsilon²[1+cos²(theta)]/2. Thus for parallel
same-direction and opposite-direction perturbations with epsilon<=1,

 D/H2 -> 1+epsilon/3 and 1-epsilon/3, respectively.              (1)

For transverse perturbations,

 D/H2 -> 2[(1+epsilon²)^(3/2)-1]/(3epsilon²)
       =1+epsilon²/4+O(epsilon⁴).                             (2)

For example epsilon=1 gives4/3 and2/3 in (1), and
2(2sqrt(2)-1)/3 in (2). Shrinking the background while keeping its relative
perturbation fixed does not remove those fractional errors. For fixed
nonzero epsilon, corrections to these deep ratios are O(x²) for Q and
O(x) for RAR. The coefficients and finite task values still need computation.

At any fixed g>0, the ordinary local expansions are

 (D-H2)/H2 = [g b''(g)/(3b'(g))] s epsilon+O(epsilon²)

for parallel signed perturbations, and

 (D-H2)/H2 = [(g b'(g)-b(g))/(4b(g))] epsilon²+O(epsilon⁴)

for transverse perturbations. The transverse odd term vanishes by symmetry.
The coefficient limits are1/3 and1/4, agreeing with (1),(2).
This is a gradient-amplitude criterion |h|/g small, not merely a potential
amplitude criterion or a requirement |h|/a small. For a Fourier perturbation,
|h| is its gradient amplitude, involving its wave number.

## What actually fails to commute

To make a precise statement take same-direction gradients and use independent
positive absolute amplitudes g and d=|h|. Define Qratio(g,d)=D(g,d)/H2(g,d)
only for g,d>0. For fixed g>0, d->0 gives Qratio->1. Thus

 lim_(g->0+) lim_(d->0+) Qratio(g,d)=1.

For fixed d>0, g->0 gives D->W(d)>0 while
H2=b'(g)d²/2~g d²/a->0. Therefore

 lim_(d->0+) lim_(g->0+) Qratio(g,d)=+infinity

in the extended-real sense. The ratio is undefined exactly at g=0, not a
finite observable there. This is a nonuniform relative approximation, not
noncommuting raw energies: BOTH iterated raw D limits are zero, and both
raw H2 limits are zero. Taking x and epsilon as the independent variables
instead describes different paths and must not be confused with these
absolute-amplitude iterated limits. The fixed-epsilon paths (1),(2) are an
additional explicit diagnostic of the nonuniformity.

## Kinetics and physical interpretation

For fixed K=2>0, the inherited scalar time kinetic term stays positive.
At a nonzero uniform background, c_parallel²/c²=b'(g)/2 and
c_perp²/c²=b(g)/(2g). Both vanish proportionally to g/a as g->0:
c_parallel/c~sqrt(g/a), c_perp/c~sqrt(g/(2a)). Loss of positive spatial
quadratic stiffness at zero is not a negative time kinetic term, a ghost,
a nonlinear ill-posedness theorem or an instability calculation for matter.
It is not a proof of continuation of FGF034 through its excluded zero-gradient
set. Source inference, if made, must still use the chosen constitutive flux.

Both a=9.3619e-11 and1.1279e-10 m/s² have the same dimensionless test, with
physical g=a x, h=a x epsilon and energy density a²(D/a²)/(4piG).
Constant-vacuum a is one branch. Frozen H references a=a0 E(z) change these
physical factors while leaving dimensionless formulas intact; evolving H
requires the already recorded reference work and is not simulated here.
No density/discrepancy, observational calibration, physical metric/photon or
full-theory closure result follows, and no historical novelty is asserted.
