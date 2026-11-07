# Continuous exact gradients do not imply a Kato estimate

This is an explicit transport countertest, NOT an AC2q solution. It strengthens
PF16's test by retaining a continuous potential and an integrable exact
spatial gradient, with no atoms or Cantor derivative at all.

On t>=0, x in the real line, define

    b(x)=sign(x) sqrt(|x|), b(0)=0,
    z(t,x)=max(t-2 sqrt(|x|),0).

The velocity is continuous and locally W1,1, with
b_x=1/(2 sqrt(|x|)) away from zero. The potential is continuous and locally
W1,1 in spacetime, zero at t=0. Writing I(t,x) for the indicator of
0<|x|<t^2/4, its weak derivatives are

    z_t=I,
    W=z_x=-sign(x) I/sqrt(|x|),
    b W=-I.

There are no boundary atoms in Dz because z vanishes continuously at the
moving support boundary and is continuous at zero. Both derivatives are
locally integrable: integral |W(t,x)| dx=2t. Thus

    z_t+b z_x=0,
    partial_t W+partial_x(b W)=0

hold distributionally, the latter by commuting mixed derivatives. For the
initial trace, ||z(t)||L1=t^3/6 and ||W(t)||L1=2t tend to zero. Nevertheless
W is nonzero for t>0. The solution z=0 is another continuous solution for
the same prescribed velocity and same initial data.

Consequently the implication

    continuous BV potential + exact gradient + signed conservative balance
      => homogeneous Kato estimate for |gradient|

is false even when the gradient has no singular measure component. The
countertest can be localized to a periodic circle: retain b on |x|<1,
patch it continuously and with finite variation away from that interval,
and take 0<=t<1 so z is supported in |x|<1/4.

This does NOT prove native nonuniqueness or a need for new physics. Its b is
a prescribed velocity, not an AC2q acoustic speed constrained by the clock,
auxiliary and metric equations. It shows precisely why continuity and the
curl cancellation proved in PF16 cannot alone supply the missing estimate.
Any successful proof must use additional native coupling or admissibility.
