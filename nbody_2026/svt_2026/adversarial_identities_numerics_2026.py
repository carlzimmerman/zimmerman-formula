#!/usr/bin/env python3
"""Independent re-derivation of the load-bearing identities + all quoted numbers."""
import sympy as sp
import numpy as np
from scipy.optimize import minimize_scalar

ok = lambda c, m: print(("[ok]  " if c else "[BAD] ") + m)

# ---------- B1/B2/B3 with EXPLICIT DBI A(Q) (not generic) + generic F ----------
u, LD, M4, kap, G, Q0, Yb = sp.symbols("u LD M4 kappa G Q0 Ybar", positive=True)
F = sp.Function("F")
K = -M4*sp.sqrt(1 - u**2/LD**2)
A = kap**2*G*(-K)
L1 = A*F(Yb/A)/(8*sp.pi*G)
y = sp.Symbol("y", positive=True)

LQQ = sp.diff(L1, u, 2).subs(Yb, y*A).doit()
target = (sp.diff(A, u, 2)*(F(y) - y*sp.Derivative(F(y), y))
          + sp.diff(A, u)**2/A*y**2*sp.Derivative(F(y), y, 2))/(8*sp.pi*G)
ok(sp.simplify(LQQ - target.doit()) == 0, "B1 identity with explicit DBI A(Q)")

LQY = sp.diff(L1, u, Yb).subs(Yb, y*A).doit()
ok(sp.simplify(LQY + (sp.diff(A, u)/A)*y*sp.Derivative(F(y), y, 2).doit()/(8*sp.pi*G)) == 0,
   "B2 L_QY = -(A'/A) y F''/8piG with explicit DBI")
LYY = sp.diff(L1, Yb, 2).subs(Yb, y*A).doit()
ok(sp.simplify(LYY - sp.Derivative(F(y), y, 2).doit()/(8*sp.pi*G*A)) == 0, "B3 L_YY")

# also true L_Y: dL/dY = F'(y)/8piG -- check
LYc = sp.diff(L1, Yb).subs(Yb, y*A).doit()
ok(sp.simplify(LYc - sp.Derivative(F(y), y).doit()/(8*sp.pi*G)) == 0, "L_Y = F'/8piG")

# eps handle
nbar = sp.diff(K, u)
epsc = nbar*Q0/(-K)
ok(sp.simplify(sp.diff(A, u)/A + epsc/Q0) == 0, "B6 A'/A = -eps/Q0")

# ---------- C4 drift ratio, fully explicit ----------
Fpp = sp.Derivative(F(y), y, 2)
Fp = sp.Derivative(F(y), y)
D = 2*sp.sqrt(y*A)*(epsc/Q0)*y*Fpp/(8*sp.pi*G)
GK = sp.diff(K, u, 2)
GG = (2/(8*sp.pi*G))*(Fp + 2*y*Fpp)
ratio = sp.simplify(D**2/(GK*GG) - (kap**2/(4*sp.pi))*(u**2/LD**2)*y**3*Fpp**2/(Fp + 2*y*Fpp))
ok(ratio == 0, "C4 D^2/(G_K G_G) = (kappa^2/4pi) s^2 y^3 F''^2/(F'+2yF'') exact")

# ---------- C1 raw EL sign, my own derivation ----------
t, z, w, k = sp.symbols("t z omega k", real=True)
LQQs, LQYs, LYs, LYYs, ppn = sp.symbols("LQQ LQY LY LYY psip", real=True)
chi = sp.Function("chi")(t, z)
L2 = (sp.Rational(1, 2)*LQQs*sp.diff(chi, t)**2 + 2*LQYs*ppn*sp.diff(chi, t)*sp.diff(chi, z)
      + (LYs + 2*LYYs*ppn**2)*sp.diff(chi, z)**2)
eom = (sp.diff(sp.diff(L2, sp.diff(chi, t)), t) + sp.diff(sp.diff(L2, sp.diff(chi, z)), z))
disp = sp.simplify(sp.expand(eom.subs(chi, sp.exp(sp.I*(k*z - w*t))).doit()
                             / sp.exp(sp.I*(k*z - w*t))))
# my EL: d/dt(dL/dchidot)+d/dz(dL/dchiz) = 0 -> -(LQQ w^2 - 4LQY pp wk + 2(LY+2LYY pp^2)k^2)
ok(sp.simplify(disp + (LQQs*w**2 - 4*LQYs*ppn*w*k + 2*(LYs + 2*LYYs*ppn**2)*k**2)) == 0,
   "C1 raw dispersion: LQQ w^2 - 4LQY pp wk + 2(LY+2LYY pp^2)k^2 = 0; +k^2 sign CONFIRMED "
   "(same-sign kinetic/gradient in L => elliptic in isolation)")

# ---------- Route A closed forms ----------
FA = y - 2 + 2*sp.exp(-sp.sqrt(y))*(1 + sp.sqrt(y))
ok(sp.simplify(sp.diff(FA, y) - (1 - sp.exp(-sp.sqrt(y)))) == 0, "F' = 1-e^{-sqrt y}")
ok(sp.limit(FA, y, 0) == 0, "F(0)=0")
ok(sp.limit(y*sp.diff(FA, y) - FA, y, sp.oo) == 2, "lim (yF'-F) = 2")
BMc = sp.simplify(sp.diff(FA, y) + 2*y*sp.diff(FA, y, 2)
                  - (1 + (sp.sqrt(y) - 1)*sp.exp(-sp.sqrt(y))))
ok(BMc == 0, "F'+2yF'' = 1+(sqrt y -1)e^{-sqrt y}")
# max of y^2 F'': with u=sqrt(y), y^2F'' = u^3 e^{-u}/2, max at u=3 -> 27e^-3/2
ok(abs(27*np.exp(-3)/2 - 0.67206) < 1e-4, "max y^2F'' = 27e^-3/2 = 0.6721 at sqrt(y)=3")

# ---------- fine numerics (denser than the script's 601-point scan) ----------
yg = np.logspace(-4, 4, 2_000_001)
sq = np.sqrt(yg)
Fp_n = 1 - np.exp(-sq)
Fpp_n = np.exp(-sq)/(2*sq)
F_n = yg - 2 + 2*np.exp(-sq)*(1 + sq)
BM = Fp_n + 2*yg*Fpp_n

fdrift = yg**3*Fpp_n**2/BM
i = np.argmax(fdrift)
print(f"  max y^3F''^2/(F'+2yF'') = {fdrift[i]:.6f} at y = {yg[i]:.4f}  (claimed 0.0645 at 3.98)")
nu = 1.8e-4*800
s = nu/np.sqrt(1+nu**2)
asym = 0.5*np.sqrt(s**2*fdrift[i]/(4*np.pi))
print(f"  drift asymmetry at nu_loc=0.144: {asym:.3e}  (claimed 5.2e-3)")

r = eps_committed = 5.1e-4
gf = eps_committed*np.max(yg*Fpp_n/BM)
print(f"  max yF''/BM = {np.max(yg*Fpp_n/BM):.4f} (claimed 0.248); eps*max = {gf:.3e}")

qn = (3*yg**2 - 8*yg + 1)/(1+yg)**4
w = qn < 0
r1, r2 = (8-np.sqrt(52))/6, (8+np.sqrt(52))/6
print(f"  q<0 exact roots: ({r1:.4f}, {r2:.4f})  (claimed (0.13, 2.51) -- upper end is 2.535)")
iq = np.argmin(qn)
print(f"  min q = {qn[iq]:.4f} at y = {yg[iq]:.4f}  (claimed -0.451 at 0.437)")
rat = BM[w]/np.abs(qn[w])
im = np.argmin(rat)
print(f"  min BM/|q| over q<0 window = {rat[im]:.4f} at y = {yg[w][im]:.4f}  (claimed 1.79 at 0.437)")

# saturation values of the two kinetic additions
kk = 0.5
a1 = (kk**2/(8*np.pi))*np.max(yg*Fp_n - F_n)
print(f"  first addition ceiling = kappa^2/4pi = {kk**2/(4*np.pi):.4e} (claimed 1.99e-2)")
c2 = np.max(yg**2*Fpp_n)/(8*np.pi)
print(f"  second addition = (kappa^2/8pi) s^2 y^2F'' K'' <= {c2:.4f} * kappa^2 s^2 K''")
print(f"    -> claimed '0.0067 kappa^2 s^2 K''' but correct coefficient is {c2:.4f};")
print(f"       0.0067 = {c2:.4f} x kappa^2(=0.25) -- i.e. the quoted bound DOUBLE-COUNTS kappa^2 "
      f"(should be 0.0267 kappa^2 s^2 K'', or 0.0067 s^2 K'' at kappa=1/2)")

# deep-MOND / y->0 vanishing
print(f"  y->0: (yF'-F)/K''-ratio {a1:.3e}; yF''(1e-4)={1e-4*np.exp(-0.01)/(2*0.01):.4f}")

# bump entries B11/B12 with explicit A(Q) -- independent
Ab = sp.Symbol("A_b", positive=True)
Bf = (Yb/A)/(1 + Yb/A)**2
L3 = Ab*Bf*u**2
By = y/(1+y)**2
Bp = sp.diff(By, y); Bpp = sp.diff(By, y, 2)
rr = sp.diff(A, u)/A
LQQ3 = sp.simplify(sp.diff(L3, u, 2).subs(Yb, y*A).doit())
tgt3 = Ab*(2*By - 4*u*rr*y*Bp + u**2*(rr**2*(y**2*Bpp + 2*y*Bp) - sp.diff(A, u, 2)/A*y*Bp))
ok(sp.simplify(LQQ3 - tgt3) == 0, "B11 bump L_QQ exact (explicit DBI)")
LQY3 = sp.simplify(sp.diff(L3, u, Yb).subs(Yb, y*A).doit())
tgt4 = Ab*(2*u*Bp/A - u**2*(sp.diff(A, u)/A**2)*(y*Bpp + Bp))
ok(sp.simplify(LQY3 - tgt4) == 0, "B12 bump L_QY exact (explicit DBI)")
ok(sp.simplify(Bp + 2*y*Bpp - (3*y**2 - 8*y + 1)/(1+y)**4) == 0, "D5 q(y) closed form")
