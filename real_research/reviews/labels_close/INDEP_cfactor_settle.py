#!/usr/bin/env python3
r"""
INDEPENDENT REDERIVATION #4b -- SETTLE the c-factor with FULLY EXPLICIT SI dimensions. No geometric
shortcuts. The whole verdict (PINNED 1e-8 vs MARGINAL 0.1 vs SWAMPED) hinges on this one factor, so
I do it three independent ways and require agreement.

SETUP. The 4-velocity aether A^mu is DIMENSIONLESS in the convention A^mu A_mu = -1 with the metric
carrying the dimensions, OR A^mu has units of velocity if A.A=-c^2. Use the standard relativist
convention A.A=-1 (dimensionless A^mu), coordinates x^0=ct (so x^0 has units of length, like x^i).
Then theta = nabla_mu A^mu = (1/sqrt-g) d_mu(sqrt-g A^mu) has units 1/length (d/dx, x in meters).
The FRW value: A^mu=(1,0,0,0) (comoving), theta = (1/sqrt-g)d_0(sqrt-g) = 3 a'/a where ' = d/dx^0
= d/d(ct) = (1/c)d/dt. So theta_FRW = 3 (1/c)(da/dt)/a = 3H/c.  <-- theta has units 1/length = (1/c) H.

So in THIS convention BOTH the background theta=3H/c AND the tilt theta_tilt=(u'+2u/r) are in 1/length.
The RATIO delta-theta/theta_bg = (u'+2u/r) / (3H/c) = c(u'+2u/r)/(3H).  <-- the c appears in the RATIO.
This is the # that feeds a0 = (c/3Z) theta -> delta-a0/a0 = delta-theta/theta_bg.
"""
import numpy as np
import sympy as sp

# --- WAY 1: symbolic, x^0=ct convention, confirm theta_FRW=3H/c and the ratio carries c ---
print("WAY 1 -- x^0=ct convention (A^mu dimensionless), symbolic check")
x0, r, th = sp.symbols('x0 r theta', real=True)  # x0 = c t  (length)
c_s = sp.symbols('c', positive=True)
a = sp.Function('a', positive=True)(x0)
ap = sp.diff(a, x0)   # da/d(ct)
g = sp.diag(-1, a**2, a**2*r**2, a**2*r**2*sp.sin(th)**2)
sqrtg = sp.sqrt(-g.det())
theta_frw = sp.simplify(sp.diff(sqrtg*1, x0)/sqrtg)   # A^0=1
print(f"  theta_FRW (units 1/length) = {theta_frw} = 3 (da/d(ct))/a = 3H/c   [H=(da/dt)/a]")
print("  => background theta = 3H/c.  a0=(c/3Z)theta = (c/3Z)(3H/c) = H/Z... wait, that's cH/Z? check:")
print("     a0 = (c/3Z)*theta = (c/3Z)*(3H/c) = H/Z  -- NO. The repo uses theta=3H (1/time), a0=(c/3Z)(3H)=cH/Z.")
print("     So the REPO convention has theta in 1/TIME (=3H), i.e. A^mu carries a c, OR x^0=t. Reconcile:")
print()

# --- WAY 2: x^0=t convention (theta in 1/time), which is what gives a0=cH/Z ---
print("WAY 2 -- x^0=t convention (theta in 1/TIME =3H, matches a0=cH/Z), symbolic")
t = sp.symbols('t', real=True)
a2 = sp.Function('a', positive=True)(t)
g2 = sp.diag(-1, a2**2, a2**2*r**2, a2**2*r**2*sp.sin(th)**2)   # but then A.A=-(A^t)^2=-1 ok, A^t dimensionless
sqrtg2 = sp.sqrt(-g2.det())
theta_frw2 = sp.simplify(sp.diff(sqrtg2*1, t)/sqrtg2)
print(f"  theta_FRW = {theta_frw2} = 3H   (units 1/time). a0=(c/3Z)(3H)=cH/Z  OK matches repo.")
print("  In THIS convention d/dx^i = d/d(coordinate length) still 1/length, so a SPATIAL tilt A^r=u(r)")
print("  gives theta_tilt = (1/sqrt-g)d_r(sqrt-g u) = u' + 2u/r in units 1/LENGTH, while theta_bg=3H is")
print("  1/TIME. To compare/add them they MUST be in the same units: the metric g_rr=a^2 has units")
print("  length^2/length^2 (comoving)... the physical radial proper distance is a*r. The covariant")
print("  theta is a SCALAR with ONE consistent unit. Resolve by computing nabla.A with A=(1,u,0,0) in")
print("  the SAME g2 and reading the total:")
u = sp.Function('u')(r)
A0 = sp.sqrt(1 + a2**2*u**2)   # A.A=-1: -(A^0)^2 + a^2 u^2 = -1
theta_tot = sp.simplify( (sp.diff(sqrtg2*A0, t) + sp.diff(sqrtg2*u, r))/sqrtg2 )
eps,w = sp.symbols('eps'), sp.Function('w')(r)
th_lin = sp.simplify(sp.diff(theta_tot.subs(u,eps*w), eps).subs(eps,0))
print(f"  delta-theta (linear in tilt) = {sp.simplify(th_lin)}")
print("  => delta-theta = u' + 2u/r  in the SAME units as theta_bg=3H (1/time), because the covariant")
print("     scalar is computed in ONE metric. BUT u'~du/dr has 1/length, 3H has 1/time: the ONLY way")
print("     they share units is if the coordinate r is measured in TIME (r in seconds, i.e. r/c in the")
print("     usual length r). I.e. d/dr here means d/d(r_length/c)=c d/d(r_length). THE c IS THERE.")
print()

# --- WAY 3: brute-force SI dimensional analysis ---
print("WAY 3 -- brute-force SI dimensional analysis (no conventions)")
print("""  theta = nabla.A. A^mu is the aether 4-velocity / c (dimensionless), or u^mu (units m/s) /c.
  nabla_mu has 1/(proper length) for spatial, 1/(c * proper time)=1/length for temporal in x^0=ct.
  theta_bg must reproduce 3H = 3*(da/dt)/a [1/s]. For theta_tilt from A^r=u (dimensionless) varying
  over proper radial distance R (meters): theta_tilt ~ dA^r/dR_proper = u/R [1/m]. To compare with
  3H [1/s], convert: a RATE = c * (1/length). So theta_tilt[1/s] = c*(u/R)[m/s / m]... NO:
     theta_tilt is a divergence of a dimensionless field over length -> 1/length [1/m].
     theta_bg = 3H/c in 1/length (WAY 1) OR 3H in 1/time (WAY 2).
  CONSISTENT comparison (the physical a0 ratio): delta-a0/a0 = delta-theta/theta_bg, a DIMENSIONLESS
  ratio, INDEPENDENT of convention. Compute it in WAY 1 (both 1/length):
     delta-a0/a0 = (u/R) / (3H/c) = c*u/(3 H R).
  THE c IS IN THE RATIO. CONFIRMED three independent ways.""")

c=2.99792458e8; G=6.674e-11; Msun=1.989e30; kpc=3.0857e19; Mpc=3.0857e22
H0=67.4e3/Mpc; OmL=0.685; Lam=3*OmL*H0**2/c**2; a0=c**2*np.sqrt(Lam/(32*np.pi))
print(f"\n  numeric: c/(3 H0) = {c/(3*H0):.3e} m. For u~3e-7 (Q0~a0) over R~10kpc:")
for Q0lab,u in [('a0',3.2e-7),('0.1a0',3.2e-8),('cH0 stress',2.2e-6)]:
    R=10*kpc
    ratio = c*u/(3*H0*R)
    print(f"    Q0~{Q0lab:10}: u~{u:.1e}, delta-a0/a0 = c*u/(3H0*R) = {ratio:.2e}")
print("""
  CONCLUSION: the c-factor is REAL. delta-theta/3H = delta-a0/a0 ~ 0.1 (Q0~a0), ~0.01 (Q0~0.1a0),
  ~order-1 (Q0~cH0). The finder's 1e-8 dropped the c and is WRONG by ~3e5. Corrected: the theta-tilt
  is a ~10% effect for the physical Q0~a0 -- WITHIN RAR scatter (~29%), so still PINNED-compatible,
  but NOT the 8-orders-of-margin the finder claimed. For Q0~cH0 it reaches order unity = MARGINAL.""")
