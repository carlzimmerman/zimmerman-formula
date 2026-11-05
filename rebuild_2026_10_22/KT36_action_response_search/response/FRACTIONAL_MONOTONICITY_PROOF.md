# Fractional-exponent candidate: p=63/10, every t>=3163/2000

The same proof as MONOTONICITY_PROOF.md applies with the following explicit
generalization. For 2<=p<8, t>=t0>1, z=(y/t)^p and the same simple excess s,

    F(z,t)=d[y nu]/dy=1+exp(-z)[B(s)-p z s],
    B(s)=s^2/(2s+1), B'(s)<1/2.

For z>=1/(2p), F increases with t, so t=t0 is the worst case. For
0<z<=1/(2p), using s<t^(-1/2)z^(-1/(2p))<z^(-1/(2p)),

    F>1-p z^(1-1/(2p))
     >=1-p(2p)^(-3/4)=1-(p/8)^(1/4)>0.

The exponent comparison is valid because p>=2 gives 1-1/(2p)>=3/4,
and z<1. For z>=10, t0>1 implies s<1; as p<8,

    F>1-80 exp(-10)>1-240/1933=1693/1933>0.

The compact interval [1/(2p),10] remains. The exact same rational enclosure
from the p=6 proof is valid with coefficient p in the negative term. Set
p=63/10 exactly and t0=3163/2000 exactly. To enclose z^(1/p)=z^(10/63),
first enclose the positive 63rd root by adjacent decimal rationals and
raise each positive endpoint to the integer power 10. Every root enclosure
is verified by exact integer powers. The square-root, exponential, interval
coverage and positive/negative-term bounds are otherwise unchanged.

`monotonicity_fractional.py` checks every rational interval separately and
retains a uniform positive rational lower bound if successful. Together with
these analytic tails and monotonicity in t, that proves nu>1, nu'<0 and
d[y nu]/dy>0 for every y>0 and t>=1.5815 at p=6.3. The intended exponents
and lower scale in the theorem are exact rationals, not binary floating
approximations. The numerical response code is separately tested by finite
floating controls.

This is constitutive admissibility only, not dynamical or relativistic health
and not an observational pass. This extension needs independent review as
well as the p=6 proof.
