# Finite-window EFE cannot robustly upper-bound the vacuum moment

Base b40e3aef45d6cccf4c5dfe04e23a1866fb856e3b. This extends Claude p57's actual QUMOND field-equation EFE functional, not its withdrawn algebraic force or orbital likelihood. The original coefficient-selection goal remains open.

## Precise theorem

Let f0=nu0-1 be positive C-infinity on y>0, strictly decreasing, with C0=integral y f0(y)dy finite and 1+f0+y f0'>0. Fix any finite observed acceleration range y<=Yobs, finite external-field bound E>0, tolerance epsilon>0 and desired finite moment Ctarget>C0. There exists another positive C-infinity strictly decreasing response f, with 1+f+y f'>0 and finite moment C=Ctarget, such that:

1. f=f0 exactly for every y<=Yobs;
2. sup over 0<e<=E of |Q2[f](e)-Q2[f0](e)|<epsilon.

The tolerance has the same units as Q2. The same fixed a0 and central rM enter both responses. Consequently these finite-window, finite-precision response data and constitutive inequalities impose no finite upper bound on C in this unrestricted class. Equality below Y means equality of the constitutive function and the corresponding isolated spherical algebraic response there. It does not imply equality of arbitrary finite-radius nonspherical galaxy forces if the global Newtonian field elsewhere exceeds Y: changed phantom sources can contribute nonlocally. No all-orbit likelihood, full covariant action health or relativistic vacuum dictionary is preserved by this theorem. It does not contradict exact ideal-continuum injectivity: the Q2 functions are arbitrarily close, not identical.

## An admissible tail stretch

Choose Y>=max(Yobs,2E), to be increased below. A nondecreasing C-infinity step theta(t), zero for t<=0 and one for t>=1, can be constructed from exp(-1/t); choose its symmetric form theta(t)+theta(1-t)=1. Define

    S_Y(y)=0 for y<=Y,
    S_Y(y)=integral_Y^y theta((s-Y)/Y) ds for y>Y.

Then S>=0, 0<=S'<=1, S''>=0, and S=y-3Y/2 for y>=2Y. Convexity with S(Y)=0 implies y S'-S>=0. For every finite stretch L>=1 put

    T_L(y)=y-(1-1/L)S_Y(y), f_L(y)=f0(T_L(y)).

T_L'=1-(1-1/L)S'>=1/L>0, T_L<=y, T_L>=y/L, and y T_L'<=T_L. Below Y it is the identity; above Y it remains >=Y. Thus f_L stays positive and strictly decreasing, equals f0 below Y, and f_L>=f0. With alpha=y T_L'/T_L in (0,1], its inverse-source derivative is

    1+f_L+y f_L'
      =(1-alpha)(1+f0(T_L))
           +alpha[1+f0(T_L)+T_L f0'(T_L)]>0.

The preserved inequalities are exact, rather than assumed to survive an infinitesimal bump. This construction allows large moment changes.

## Moment range

Since f_L<=f0(y/L), C_L<=L² C0<infinity. C_L is continuous and nondecreasing in L, with C_1=C0. Continuity on a compact L interval follows from domination by y f0(y/Lmax). For L>=2, y in [LY,2LY] is in the affine tail and T_L=y/L+(1-1/L)3Y/2<4Y. Hence

    C_L>=(3/2)L²Y² f0(4Y)->infinity.

The intermediate-value theorem supplies every finite Ctarget>=C0. Each response separately has a finite vacuum moment; the unbounded sequence is not being replaced by an inadmissible infinite-L response.

## Uniform EFE bound

The already independently audited p57 continuum kernel has

    Q2(e)=-(9a0/(4rM)) integral f(y) sqrt(y) F(e/y)dy,
    F(q)=q²/10+O(q⁴) at q=0.

F is analytic on 0<q<1. Therefore B=sup_{0<q<=1/2}|F(q)|/q² is finite, by its removable q=0 limit and compact continuity. We need no numerical estimate of B. Only y>=Y changes, and 0<=f_L-f0<=f0(Y). For every 0<e<=E,

    |Delta Q2(e)|
      <=(9a0/(4rM)) B e² integral_Y^infinity (f_L-f0)y^(-3/2)dy
      <=(9a0/(2rM)) B E² f0(Y)/sqrt(Y).

This upper bound is independent of L. The right side tends to zero as Y tends to infinity; monotonic f0 bounds its numerator even before using finite C0. First choose Y to achieve epsilon, then choose L to achieve Ctarget. Both requirements can therefore be met simultaneously, with every fixed bounded-response measurement unchanged exactly.

The sign and both shell branches of the parent kernel remain important for its complete sum rule, but this deformation only uses e/y<=1/2. It never approaches the shell or discards its branch in the parent theory. An unbounded external-field range, exact data, a prescribed tail scale, or additional action-level restrictions change this conclusion. This theorem does not show arbitrary downward changes in C, nor preserve nonlinear trajectories sampling unbounded accelerations.

## Evidence and physical implication

checks.py verifies the map/source convexity algebra and finite-moment bounds. Its illustrative baseline f0=y^-1/2(1+y)^-5/2 has exact C0=pi/8, deep-MOND leading behavior, and a strictly positive source derivative: the negative term is bounded by 2sqrt(y)/(1+y)^(7/2), whose squared maximum is (2/3)(6/7)^7<1. This baseline is an algebra control, not a fit to Claude's astronomical data. A C2 polynomial ramp is used for finite computational controls; the universal C-infinity theorem instead uses the flat exponential step described above. The proof uses only the stated convexity bounds, shared by both ramps.

This is a sharper robust no-go for inferring the proposed vacuum moment from bounded finite-precision response/inner-quadrupole observations alone. It strengthens the earlier finite-observable null families by establishing arbitrarily large admissible moments while uniformly controlling the entire bounded EFE window. It still does not prove that no independently motivated action or consistency principle can force 32pi. Such a principle must constrain the far tail or the covariant vacuum dictionary, rather than rely only on these data. Full recombination, cold abundance and galaxy source completion remain separate physical obligations.
