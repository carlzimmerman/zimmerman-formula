# Constitutive monotonicity: cutoff p=6, every t>=3/2

Claim: for every y>0 and t>=3/2, the explicitly defined response

    nu(y)=1+s(y) exp[-(y/t)^6],
    s(y)=(sqrt(1+4/y)-1)/2,

has nu>1, nu'<0 and d[y nu(y)]/dy>0. This is a constitutive statement only;
it is not a theorem of dynamical stability, relativistic health or data fit.

The first two claims follow from s>0,s'<0 and a decreasing positive
exponential. Put z=(y/t)^6, so y=t z^(1/6). Since s(s+1)=1/y,

    y s'=-s(s+1)/(2s+1),
    F(z,t):=d[y nu]/dy=1+exp(-z)[B(s)-6 z s],
    B(s)=s^2/(2s+1).

Also B'(s)=2s(s+1)/(2s+1)^2<1/2. At fixed z, s is strictly decreasing
in t. For z>=1/12, B'(s)-6z<0, so F is increasing in t. It therefore
suffices in this region to treat the single exact value t=3/2.

For 0<z<=1/12, the inequality s<1/sqrt(y) and t>=3/2>1 give

    F>1-6 z s>1-6 z^(11/12)
      >=1-6 (1/12)^(3/4)>0.

Here z^(11/12)<=z^(3/4) on (0,1), and 12^3=1728>6^4=1296 proves
6(1/12)^(3/4)<1. No numerical sampling is used for this tail.

For z>=10 at t=3/2, s<1 and z exp(-z) is decreasing. Thus

    F>1-60 exp(-10)>1-180/1933=1753/1933>0.

The exact exponential bound uses
exp(10)>1+10+10^2/2+10^3/6+10^4/24=1933/3. By the monotonicity in t
already established, this tail estimate also covers every t>=3/2.

It remains to verify the compact interval z in[1/12,10] at t=3/2. The
companion script uses only Python integers and fractions, not floating-point
square roots or exponentials. Divide the interval into consecutive closed
intervals of length 1/500, with the final interval shortened. There are
exactly 4,959 intervals and their union is the required interval.

For an interval [a,b], s(z) is decreasing, so certified rational enclosures
s_-(b)<=s(z)<=s_+(a) follow from adjacent decimal-rational bounds for the
positive sixth and square roots, whose powers are explicitly checked.
Because B is increasing, its minimum on that interval is bounded by B(s_-(b)).
For N=128 and 0<=x<=10,

    (1-x/N)^N <= exp(-x) <= (1+x/N)^(-N).

These follow from log(1-v)<=-v and log(1+v)<=v for their stated domains.
Let L(b) be the left bound and U(x) the right bound. Let m=1 when [a,b]
contains 1, m=b when b<1, and m=a when a>1. The function x exp(-x) is
maximal at m on [a,b]. Consequently

    F(z,3/2) >= 1+L(b) B(s_-(b))-6 m U(m) s_+(a).

Every quantity on the right is rational and evaluated exactly. The run
checks strict positivity separately on every interval and retains the exact
minimum fraction and its interval. Combined with the analytic reductions
above, a successful run proves the stated constitutive claim for all y>0
and all t>=3/2. The resulting positive bound need not approximate the true
minimum sharply.

This is an exact finite certificate supporting an analytic reduction, with
the usual dependency on correct integer arithmetic and the audited script.
It is separate from floating-point tests of the response implementation.
An independent proof/code review is still appropriate before promotion.
