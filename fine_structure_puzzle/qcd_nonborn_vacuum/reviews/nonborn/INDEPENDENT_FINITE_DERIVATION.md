# Independent finite-band implementation design

Source: independently authenticated NP arXiv:0712.1294v2 source member
Pol1loop080308.tex, S1pol/S2pol/integraldef1. This design is saved before
opening the worker's check_finite_band.py. Its reported finite values have
been seen, so the computation is a separate implementation, not a blinded
prediction of their numerical values. No worker module will be imported.

Let t=(Q/m_pi)^2, y=x^2, h=1-y, H=sqrt(1+t y). Write the source parameter
integral as J=integral_0^1 dz [1+t(z-h z²)]^-1/2. The source Born amplitudes
fix t_i=S_i, with C0=g_A² M m_pi/(4 pi F²). Direct substitution and algebra
in the full trace -3 S1+h S2 gives C0 times

 Btrace=-3+2H-1/(H+1)
        +(4+t)/(4h+t)[y/(H+1)-1/2]+(2+t/2)J.

This avoids reconstructing S2 with 1/q0² factors. An expression with no
subtraction of two order-one values at small t is obtained from
(H-1)=t y/(H+1) and

 J-1=-t I, I=integral_0^1 dz f/[sqrt(1+t f)(1+sqrt(1+t f))], f=z-h z².

It is

 Btrace=t {1/2+y[2/(H+1)+1/(2(H+1)²)]
   +y[2h+t y/(H+1)]/[(H+1)²(4h+t)]-(2+t/2)I}.

At x=0 this is t[1/2-(2+t/2)I]. At |x|=1 the rational term is
1/(H+1)^3. These formulas are finite at either angular endpoint for t>0.
The angularly integrated soft limit is 9 pi t/32, and its photon ball is
9 pi L4/64. The two amplitudes retain the seagull constant 3/2 from S1.

The independent numerical rule integrates dt directly, uses second-kind
Gauss–Chebyshev nodes/weights for sqrt(1-x²) dx, and integrates the rationalized
parameter integrand with Gauss–Legendre. It does not use the author's
arctangent implementation, angular theta coordinate or singular S2 formula.
Legendre orders 16,32,48 and angular orders 32,64,96 are compared in a bounded
run at 50 digits. All four declared bands are checked against their frozen
source-functional results. This is convergence evidence, not an interval
certificate and not an uncertainty bound for the HB approximation.
