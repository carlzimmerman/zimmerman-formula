#!/usr/bin/env python3
r"""
DECISIVE Route-2 calculation -- ACTION-LEVEL variation, NO scaling estimates.

Khronometric MOND with a DYNAMICAL a0 = a0(K),  a0(K)^2 = c^2 K^2 / Z^2.
eps = 0, eta_K = 0.  F(X) = -2 sqrt(X) + 2 ln(1+sqrt(X)),  X = c^4 a_mu a^mu / a0(K)^2.
Restore the khronon Stuckelberg mode  T = t + psi(r).

TARGET:  the khronon Euler-Lagrange SOURCE  S_T(r) = delta S/delta psi |_{psi=0}
for the F-sector (the only sector carrying a0(K)), retaining the FULL X-dependence, and
the quadratic operator W(X).  Outcome A: S_T=0 in vacuum (T=t exact -> Route 2 alive).
Outcome B: S_T != 0 (solve the ODE, report delta K/3H).

CONVENTION: c = 1 in the line element (removes all factor-of-c bookkeeping); X = (g/a0)^2
is exactly the physical ratio; whether S_T VANISHES is convention independent.  In c=1:
   a0^2 = K^2/Z^2 ,   X = Z^2 a_mu a^mu / K^2 .

KEY LIGHT-WEIGHT FACT (DERIVED below): with dT=(1, eps psi',0,0), the khronon norm
   N_phi = sqrt(1/(1+2Phi) - eps^2 psi'^2/a^2)
has its psi-correction at O(eps^2).  So u_mu is EXACTLY LINEAR in eps at the order needed,
and every downstream object (a_mu, K, X) is a short polynomial in eps -> no simplify blowup.

Labels: DERIVED (sympy here) / ASSUMED (background ansatz) / IMPORTED (prior repo result).
"""
import sympy as sp
def head(t): print("\n"+"="*94+f"\n{t}\n"+"="*94)
PASS=[True]
def gate(c,l,d=""):
    print(f"  [{'ok' if c else 'FAIL'}] {l}"+(f"   {d}" if d else "")); PASS[0]=PASS[0] and bool(c); return c

t,r,th,ph = sp.symbols('t r theta phi', real=True)
Z         = sp.symbols('Z', positive=True)
eps       = sp.symbols('epsilon', real=True)
a         = sp.Function('a', positive=True)(t)
Phi       = sp.Function('Phi')(r)
psi       = sp.Function('psi')(r)
Hs        = sp.Symbol('H', positive=True)
X4        = [t,r,th,ph]
sub_adot  = {sp.Derivative(a,t): Hs*a}
lap = lambda f: sp.diff(f,r,2)+2*sp.diff(f,r)/r

head("0 -- geometry, Christoffels, and u_mu(eps) linear in eps  [ASSUMED ansatz / DERIVED]")
N2 = 1+2*Phi
g  = sp.diag(-N2, a**2, a**2*r**2, a**2*r**2*sp.sin(th)**2)
gi = g.inv()
sqrtg = sp.sqrt(-g.det())                              # = sqrt(1+2Phi) a^3 r^2 sin(theta)
# Christoffels (diagonal metric -> fast)
G=[[[sp.Rational(1,2)*sum(gi[l,s]*(sp.diff(g[s,m],X4[k])+sp.diff(g[s,k],X4[m])-sp.diff(g[m,k],X4[s]))
     for s in range(4)) for k in range(4)] for m in range(4)] for l in range(4)]
G=[[[sp.simplify(G[l][m][k]) for k in range(4)] for m in range(4)] for l in range(4)]

# u_mu exactly-linear-in-eps (N_phi correction is O(eps^2)):
Nphi0 = sp.sqrt(1/N2)                                   # = 1/sqrt(1+2Phi)
u_lo = [-1/Nphi0, -eps*sp.diff(psi,r)/Nphi0, 0, 0]      # (u_t, u_r, 0, 0)
u_up = [sp.together(sum(gi[i,j]*u_lo[j] for j in range(4))) for i in range(4)]
print("  u_t =",u_lo[0],"  u_r =",u_lo[1])
print("  u^t =",u_up[0],"  u^r =",u_up[1])

# a_mu = u^nu ( d_nu u_mu - Gamma^l_{nu mu} u_l )   [keep linear in eps]
def lin(e): return sp.expand(e).coeff(eps,0)+eps*sp.expand(e).coeff(eps,1)
a_lo=[]
for mu in range(4):
    s=0
    for nu in range(4):
        s+= u_up[nu]*(sp.diff(u_lo[mu],X4[nu]) - sum(G[l][nu][mu]*u_lo[l] for l in range(4)))
    a_lo.append(lin(s))
a2 = lin(sum(gi[i,j]*a_lo[i]*a_lo[j] for i in range(4) for j in range(4)))
K  = lin(sum(sp.diff(sqrtg*u_up[i],X4[i]) for i in range(4))/sqrtg)

head("1 -- background identities at psi=0  [DERIVED, must match IMPORTED repo results]")
K0  = sp.simplify(K.coeff(eps,0).subs(sub_adot))
K1  = sp.simplify(K.coeff(eps,1).subs(sub_adot))
a20 = sp.simplify(a2.coeff(eps,0))
a21 = sp.simplify(a2.coeff(eps,1))
ar0 = sp.simplify(a_lo[1].coeff(eps,0))
print("  K0    =",K0)
print("  a_r0  =",ar0)
print("  a20   =",a20)
gate(abs(complex((K0-3*Hs/sp.sqrt(1+2*Phi)).subs({Phi:sp.Rational(1,10),Hs:1})))<1e-12,
     "K|0 = 3H/sqrt(1+2Phi)  (IMPORTED isotropy)")
gate(sp.simplify(ar0-sp.diff(Phi,r)/(1+2*Phi))==0,
     "a_r|0 = Phi'/(1+2Phi) = D_r lnN  (a_i=d_iPhi/c^2 phys)")
K1_0 = sp.simplify(K1.subs(Phi,0).doit())
gate(sp.simplify(K1_0+lap(psi)/a**2)==0, "deltaK = -lap(psi)/a^2  (IMPORTED khronon_K B1)")
gate(sp.simplify(a20-sp.diff(Phi,r)**2/(a**2*(1+2*Phi)**2))==0 or
     abs(complex((a20-sp.diff(Phi,r)**2/a**2).subs({Phi:0,sp.Derivative(Phi,r):sp.Rational(3,7),a:1})))<1e-12,
     "a^2|0 = (Phi')^2/(a^2)(1+..)  (weak field)")
print("  STAGE-1", "PASS" if PASS[0] else "FAIL")

head("2 -- F-sector reduced Lagrangian, linear-in-psi piece L1, and the SOURCE S_T(r)")
# X = Z^2 a2 / K^2 ;  X0, X1(linear in psi):
X0 = sp.simplify(Z**2*a20/K0**2)
X1 = sp.simplify(Z**2*(a21/K0**2 - 2*a20*K1/K0**3))     # = X0*(a21/a20 - 2 K1/K0)
srad = sp.sqrt(1+2*Phi)*a**3*r**2                       # radial measure sqrt(-g)/sin(theta)
# rho_F = -srad*(2K^2/Z^2) F(X).  Linear-in-eps (chain rule):
#   L1 = pre0 F'(X0) X1 + pre1 F(X0),  pre0=-srad 2K0^2/Z^2, pre1=-srad 4K0 K1/Z^2
Ff = sp.Function('F')
u_ = sp.Symbol('u_')
F0  = Ff(X0)
Fp  = sp.diff(Ff(u_),u_).subs(u_,X0)                    # F'(X0)  (chain-rules under d/dr)
pre0 = -srad*(2*K0**2/Z**2)
pre1 = -srad*(4*K0*K1/Z**2)
L1 = sp.expand(pre0*Fp*X1 + pre1*F0)

psi1=sp.Derivative(psi,r); psi2=sp.Derivative(psi,r,2)
A = sp.simplify(sp.diff(L1,psi))
B = sp.simplify(sp.diff(L1,psi1))
C = sp.simplify(sp.diff(L1,psi2))
gate(sp.simplify(L1-(A*psi+B*psi1+C*psi2))==0, "L1 = A psi + B psi' + C psi''  (<=2nd order)")

# Euler-Lagrange source (psi-independent inhomogeneous term):
S_T = A - sp.diff(B,r) + sp.diff(C,r,2)

head("3 -- evaluate S_T on an explicit VACUUM solution Phi = -M/r (lap Phi = 0)")
M = sp.symbols('M', positive=True)
Phivac = -M/r
def vac(e):
    e=e.subs({sp.Derivative(Phi,(r,3)):sp.diff(Phivac,r,3),
              sp.Derivative(Phi,(r,2)):sp.diff(Phivac,r,2),
              sp.Derivative(Phi,r):sp.diff(Phivac,r),Phi:Phivac})
    return e
X0v = sp.simplify(vac(X0))
print("  X0(r) =", X0v, "   [= (g/a0)^2, a0=3H/Z, g=M/r^2]")

# joint weak-field/slow expansion: Phi~O(d), H~O(d)  => X0~O(1) held (F kept symbolic).
d = sp.symbols('d', positive=True)
S_T_v = vac(S_T)
# The F,F',F'' of X0 are O(1); scale only the explicit M,H:
S_T_s = S_T_v.subs({M:d*M, Hs:d*Hs})
# X0 is d-independent under this scaling (M/H^2 * ... ), confirm then series:
X0_s  = X0v.subs({M:d*M, Hs:d*Hs})
gate(sp.simplify(sp.diff(X0_s,d))==0, "X0 is invariant under the joint scaling (X0 held O(1))")
ser = sp.series(sp.expand(S_T_s), d, 0, 5)
print("\n  S_T(r) series in d (Phi,H ~ d):")
sp.pprint(ser)
lead = sp.simplify(ser.removeO())
print("\n  Leading S_T(r):")
sp.pprint(sp.simplify(lead))

# Express leading in terms of x=sqrt(X0)=g/a0, to see the a0(K) structure explicitly
is_zero = sp.simplify(lead)==0
print("\n  >>> F-sector SOURCE vanishes in vacuum? ", "YES  => Outcome A" if is_zero else "NO   => Outcome B")

with open("_ST_result.txt","w") as f:
    f.write("X0v="+str(X0v)+"\n\nS_T_v="+str(S_T_v)+"\n\nlead="+str(lead)+"\n")
print("\n  (full S_T written to _ST_result.txt)")
print("\nSTAGE-2/3", "PASS" if PASS[0] else "FAIL")
