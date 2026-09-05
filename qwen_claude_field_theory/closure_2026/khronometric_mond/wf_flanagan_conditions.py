#!/usr/bin/env python3
"""
wf_flanagan_conditions.py

Translate Flanagan (arXiv:2302.14846) khronon-stability conditions into the
MOND mu-function language, and then into Carl's W(y) primitive, and locate the
ghost for Carl's specific candidate.

Flanagan's setup (BM = Blanchet-Marsat khronometric MOND), action Eq (3):
    S = (c^3/16 pi G) int sqrt(-g)[ R - 2 f(a) ] + S_m
with a = |acceleration of foliation normal|.  Rescaled fbar(abar), abar = physical accel.

Khronon quadratic action, Eq (42):
    S_2pi = (1/2) int [ h^{ij} d_i(dpi_dot) d_j(dpi_dot) - rho_T0 (grad dpi)^2 ]
Kinetic tensor, Eq (32):
    h^{ij} = -(1/4piG)[ chibar (delta^{ij}-nhat^i nhat^j) + (fbar''/2) nhat^i nhat^j ]
    chibar = fbar'(abar)/(2 abar).
No-ghost Eq (43):  fbar' <= 0 ,  fbar'' <= 0.
rho_T0>=0 (grad-stability), Eq (53):  fbar''<=0 , abar fbar'' - fbar' >= 0.
COMBINED, Eq (54):   f'(a) <= a f''(a) <= 0.

MOND Poisson (Eq 26):  div[(1+chibar(ab)) grad Phi] = 4 pi G rho  =>  mu(a) = 1 + chibar
                       = 1 + fbar'/(2a).   (footnote 8: varpi(a)=a mu(a/a0))

We work with y = a/a0, mu = mu(y), primes on mu are d/dy.  a = a0 y.
"""
import sympy as sp

y = sp.symbols('y', positive=True)
a0 = sp.symbols('a0', positive=True)

# ---- generic mu(y): express Flanagan's f' , f'' in terms of mu -------------
mu = sp.Function('mu')(y)

# chibar = mu - 1  ; f'(a) = 2 a chibar = 2 a (mu-1),  a = a0*y
fprime = 2*a0*y*(mu - 1)                      # f'(a) as a function of y
# f''(a) = d f'/da = (1/a0) d/dy [f'(a)]
fpp = sp.diff(fprime, y)/a0
fpp = sp.simplify(fpp)
print("f'(a)  in mu-language        :", sp.simplify(fprime))
print("f''(a) in mu-language        :", fpp)   # expect 2*((mu-1)+y*mu')

# Flanagan Eq (54) pieces:
#   (C1) f' <= 0                      <=> mu <= 1
#   (C2) f'' <= 0                     <=> (mu-1)+y mu' <= 0  <=> y mu' + mu <= 1
#   (C3) a f'' - f' >= 0             <=> ?
cond3 = sp.simplify(a0*y*fpp - fprime)
print("a f'' - f'  in mu-language   :", cond3, "   (>=0 required)")   # expect 2 a0 y^2 mu'
print()

# ---- Now the KEY identification with Carl's W:  mu = W'/y  =>  W' = y*mu ----
# => W'' = d(y mu)/dy = mu + y mu'.  So Flanagan f'' = 2*(W'' - 1).
Wpp_sym = mu + y*sp.diff(mu, y)
print("W''(y) = mu + y mu'          :", Wpp_sym)
print("Check f'' == 2*(W''-1)       :", sp.simplify(fpp - 2*(Wpp_sym - 1)) == 0)
print("=> Flanagan no-ghost f''<=0  <=>  W''(y) <= 1")
print("=> Flanagan grad-stab (C3)   <=>  mu'(y) >= 0   (since a f''-f' = 2 a0 y^2 mu')")
print("="*70)

# ---- Carl's exact primitive ------------------------------------------------
# W(y) = (1/2)y^2 + (1+y)e^{-y} - 1
W = sp.Rational(1,2)*y**2 + (1+y)*sp.exp(-y) - 1
Wp = sp.simplify(sp.diff(W, y))
Wpp = sp.simplify(sp.diff(W, y, 2))
muC = sp.simplify(Wp/y)
print("Carl W(y)      :", W)
print("Carl W'(y)     :", Wp, "   (= y(1-e^-y))")
print("Carl W''(y)    :", Wpp, "   (= 1+(y-1)e^-y)")
print("Carl mu=W'/y   :", muC, "   (= 1-e^-y)")
print()

# no-ghost longitudinal kinetic coefficient (proportional to) 1 - W''  (>0 healthy)
kin_long = sp.simplify(1 - Wpp)
print("Longitudinal khronon kinetic coeff  ~ (1-W'') =", kin_long)
print("   (Flanagan h_par = (1-W'')/(4 pi G);  <0  => GHOST)")

# solve where W'' = 1 (ghost onset)
onset = sp.solve(sp.Eq(Wpp, 1), y)
print("W''(y)=1 at y =", onset, "  => ghost boundary at y=1  (a = a0)")

# grad-stability: mu' >= 0 ?
muCp = sp.simplify(sp.diff(muC, y))
print("Carl mu'(y)    :", muCp, "  (= e^-y > 0 : grad-stability C3 ALWAYS ok)")
print()

# tabulate the kinetic coefficient and worst ghost
print("  y      W''(y)     1-W''(y)   [<0 => longitudinal ghost]")
import math
for yv in [0.1,0.3,0.5,0.8,1.0,1.5,2.0,3.0,5.0,10.0]:
    wpp = 1 + (yv-1)*math.exp(-yv)
    print(f" {yv:5.2f}  {wpp:9.5f}  {1-wpp:9.5f}")
# worst (most negative) point:
ycrit = sp.solve(sp.diff(kin_long, y), y)
print("extremum of (1-W'') at y =", [sp.nsimplify(s) for s in ycrit if s.is_real],
      "-> most-ghostly y=2, 1-W''=", float(1-(1+(2-1)*math.exp(-2))))
print("as y->inf, W''->1^+ so (1-W'')->0^- (vanishing residual ghost)")
