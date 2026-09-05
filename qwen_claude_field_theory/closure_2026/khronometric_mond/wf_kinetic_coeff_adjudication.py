#!/usr/bin/env python3
"""
wf_kinetic_coeff_adjudication.py

ADJUDICATE the internal contradiction:
  * wf_flanagan_conditions.py / wf_decisive_v2_correct.py :  h_par ~ (1 - W'')  (GHOST for y>1)
  * wf_speeds_and_stability.py                            :  A_par ~  W''/2 > 0 (no ghost)

The second used a HEURISTIC alpha_eff=W''/2 substituted into the flat Minkowski
khronon template.  The first is Flanagan's actual reduction.  We settle it by
directly expanding Flanagan's OWN non-relativistic action (his Eq. 20) to second
order in the khronon pi.

Flanagan Eq (19),(18),(20):
   Xi   = Phi - pidot + (1/2)(grad pi)^2 ,   abar = |grad Xi|
   S_NR = - int dt d3x [ (grad Phi)^2/8piG + rho_m Phi + fbar(abar)/8piG ]
Phi is elliptic/auxiliary (no time derivative) -> it cannot generate pidot^2 terms;
the coefficient of d_i(pidot) d_j(pidot) comes solely from expanding fbar(abar).

Represent the LINEAR-in-pi perturbation of grad(Xi) by explicit symbols:
   d_x(-pidot) = -pxt ,  d_z(-pidot) = -pzt      (pxt=d_x pidot, pzt=d_z pidot)
Background grad Phi = g zhat.  (The (1/2)(grad pi)^2 piece carries no pidot at
linear order, so it does not affect the pidot^2 coefficient.)
"""
import sympy as sp

g = sp.symbols('g', positive=True)
pxt, pzt = sp.symbols('pxt pzt', real=True)     # d_x(pidot), d_z(pidot)
fbp, fbpp = sp.symbols('fbp fbpp', real=True)   # fbar'(g), fbar''(g)
s = sp.symbols('s')                              # order tracker

# grad(Xi) = (0 - s*pxt ,  g - s*pzt)   [linear-in-pi perturbation carries pidot]
gXx = -s*pxt
gXz = g - s*pzt
abar = sp.sqrt(gXx**2 + gXz**2)
dabar = sp.series(abar, s, 0, 3).removeO() - g          # abar - g  to O(s^2)

fbar_quad = fbp*dabar + sp.Rational(1,2)*fbpp*sp.expand(dabar**2)
fbar_quad = sp.expand(sp.series(fbar_quad, s, 0, 3).removeO())
quad = sp.expand(fbar_quad.coeff(s, 2))                 # coefficient of s^2

print("abar - g  (to 2nd order) =", sp.simplify(dabar.subs(s,1)))
print("2nd-order fbar density    =", quad)
c_par  = sp.simplify(quad.coeff(pzt**2))
c_perp = sp.simplify(quad.coeff(pxt**2))
print()
print("coeff of (d_z pidot)^2  [PARALLEL] =", c_par, "  = fbar''/2")
print("coeff of (d_x pidot)^2  [PERP]     =", c_perp, "  = fbar'/(2g) = chibar")
print()
print("S_NR = -(1/8piG) int fbar ;  Flanagan S_2pi=(1/2)int h^ij d_i(pidot)d_j(pidot)")
print("=> (1/2) h_par = -(1/8piG) c_par  => h_par = -(1/4piG)(fbar''/2)   [Eq 32 parallel]")
print("=> (1/2) h_perp= -(1/8piG) c_perp => h_perp= -(1/4piG) chibar      [Eq 32 perp]")
print("   (matches Flanagan Eq (32) EXACTLY, incl. signs)")
print()

# specialize to W: fbar'=2 g (mu-1), fbar''=2(W''-1); mu=1-e^-y, W''=1+(y-1)e^-y
y0 = sp.symbols('y0', positive=True)
mu  = 1 - sp.exp(-y0)
Wpp = 1 + (y0-1)*sp.exp(-y0)
fbpp_W = 2*(Wpp-1)
chib_W = mu-1
print("For Carl's W:  fbar''/2 = W''-1 =", sp.simplify(fbpp_W/2), " ; chibar = mu-1 =", sp.simplify(chib_W))
print("  h_par  ~ -(fbar''/2) = 1 - W'' =", sp.simplify(1-Wpp), "   -> NEGATIVE for y>1  (GHOST)")
print("  h_perp ~ -chibar     = 1 - mu  =", sp.simplify(1-mu),  "   = e^-y > 0  (always healthy)")
print()
print("VERDICT: the khronon TIME-kinetic coefficient of d(pidot)d(pidot) parallel to a")
print("is (1 - W''), NOT W''.  wf_speeds' 'A_par ~ W''/2' mis-used the CONSTITUTIVE")
print("(static force-law / elliptic) Hessian as the kinetic normalization. The genuine")
print("kinetic coeff (1-W'') changes sign at y=1 -> GHOST for a>a0.  Flanagan confirmed.")
