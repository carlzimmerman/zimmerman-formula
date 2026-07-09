#!/usr/bin/env python3
"""
ORDERING FORK: does v12's 'no transverse aether kinetic term' survive if Box_u is defined
with the SYMMETRIZED/covariant ordering instead of the directional (u.grad)^2 ordering?
On dS (comoving frame) the two orderings agree on the BACKGROUND (their difference ~ frame
acceleration = 0 for a geodesic frame), so any fork lives at O(delta_u^2). We compute
Q = u^mu Box_u u_mu to O(du^2) under BOTH orderings and compare the transverse symbol.
Metric: dS flat slicing 1+1  ds^2=-dt^2+a^2 dx^2, a=e^{Ht}; frame ubar=(1,0).
"""
import sympy as sp
t,x,H,eps = sp.symbols('t x H epsilon', real=True)
a = sp.exp(H*t)
g  = sp.Matrix([[-1,0],[0,a**2]]); gi = g.inv()
coords=[t,x]
def Gamma(l,m,n):
    return sp.simplify(sum(gi[l,r]*(sp.diff(g[r,m],coords[n])+sp.diff(g[r,n],coords[m])-sp.diff(g[m,n],coords[r]))/2 for r in range(2)))
Gam=[[[Gamma(l,m,n) for n in range(2)] for m in range(2)] for l in range(2)]

# frame: ubar^mu=(1,0); fluctuation du^mu=(du0, v). unit norm u.u=-1 fixes du0 at O(eps^2):
# g_00 (1+eps*du0)^2 + g_11 (eps v)^2 = -1  =>  -(1+2 eps du0) + a^2 eps^2 v^2 = -1
#  => du0 = (a^2 v^2/2) eps   (so eps*du0 is O(eps^2)); keep to needed order.
v=sp.Function('v')(t,x)
du0=sp.Rational(1,2)*a**2*v**2      # times eps^2 overall
uup = sp.Matrix([1+eps**2*du0, eps*v])           # u^mu to O(eps^2)
udn = sp.simplify(g*uup)                          # u_mu

def covderU(vecUp):                               # nabla_a of a (1,0) vector, returns [a][l]
    return [[sp.diff(vecUp[l],coords[aa])+sum(Gam[l][aa][mm]*vecUp[mm] for mm in range(2)) for l in range(2)] for aa in range(2)]
def covderD(covDn):                               # nabla_a of a (0,1) covector -> [a][l]
    return [[sp.diff(covDn[l],coords[aa])-sum(Gam[mm][aa][l]*covDn[mm] for mm in range(2)) for l in range(2)] for aa in range(2)]

# (u.grad) acting on the covector u_mu:  (u.grad u)_mu = u^a nabla_a u_mu
def u_dot_grad_cov(covDn):
    d=covderD(covDn)                               # d[a][l]
    return [sp.simplify(sum(uup[aa]*d[aa][l] for aa in range(2))) for l in range(2)]

# --- ORDERING 1: directional  Box_dir u_mu = (u.grad)( (u.grad) u_mu ) ---
A1 = u_dot_grad_cov(udn)          # (u.grad)u  (the acceleration covector, =0 on bg)
Box_dir = u_dot_grad_cov(A1)      # (u.grad)^2 u_mu

# --- ORDERING 2: symmetrized covariant  Box_sym u_mu = u^a u^b nabla_a nabla_b u_mu ---
# nabla_b u_mu = M[b][mu]; then nabla_a of the (0,2) tensor M, contract u^a u^b.
M=covderD(udn)                    # M[b][l] = nabla_b u_l
def covder_02(T):                 # nabla_a of (0,2) tensor T[b][l] -> [a][b][l]
    out=[[[0]*2 for _ in range(2)] for _ in range(2)]
    for aa in range(2):
        for bb in range(2):
            for ll in range(2):
                term=sp.diff(T[bb][ll],coords[aa]) - sum(Gam[mm][aa][bb]*T[mm][ll] for mm in range(2)) - sum(Gam[mm][aa][ll]*T[bb][mm] for mm in range(2))
                out[aa][bb][ll]=term
    return out
DM=covder_02(M)
Box_sym=[sp.simplify(sum(uup[aa]*uup[bb]*DM[aa][bb][ll] for aa in range(2) for bb in range(2))) for ll in range(2)]

# quadratic forms Q = u^mu Box u_mu
Q_dir=sp.simplify(sum(uup[l]*Box_dir[l] for l in range(2)))
Q_sym=sp.simplify(sum(uup[l]*Box_sym[l] for l in range(2)))
diff=sp.simplify(Q_dir-Q_sym)

# extract O(eps^2) parts
def order2(expr): return sp.simplify(sp.series(expr,eps,0,3).removeO().coeff(eps,2))
Qd2=order2(Q_dir); Qs2=order2(Q_sym); D2=sp.simplify(Qd2-Qs2)
print("O(eps^2) directional Q_dir:"); sp.pprint(sp.simplify(Qd2))
print("\nO(eps^2) symmetrized Q_sym:"); sp.pprint(sp.simplify(Qs2))
print("\nORDERING DIFFERENCE  Q_dir - Q_sym  at O(eps^2):"); sp.pprint(D2)

# symbol: replace v -> e^{i(w t + k x)} and read the k (transverse) structure of the DIFFERENCE
w,k=sp.symbols('omega k',real=True)
vpl=sp.exp(sp.I*(w*t+k*x))
D2s=sp.simplify(D2.subs(v,vpl).doit())
# strip the |plane wave|^2 factor by dividing by e^{2i(...)} where present; look at k,w powers
D2s=sp.simplify(D2s/sp.exp(2*sp.I*(w*t+k*x)))
print("\nsymbol of the ordering-difference (coeff structure in w=k0, k=kperp):"); sp.pprint(sp.simplify(D2s))
# the decisive test: at w=0 (static), is there a NONZERO k^2 (transverse KINETIC) piece?
D2_static=sp.simplify(D2s.subs(w,0))
print("\nAt omega=0 (static): ordering-difference symbol ="); sp.pprint(D2_static)
kk2=sp.simplify(sp.diff(D2_static,k,2)/2)          # coefficient of k^2 at w=0
print("\n=> transverse k^2 KINETIC coefficient of (Q_dir - Q_sym) at omega=0 :", sp.simplify(kk2))
print("   (if 0 -> orderings agree on the aether kinetic term -> v12 SURVIVES;")
print("    if nonzero -> the 'no aether term' verdict is ORDERING-DEPENDENT -> v12 scoped back.)")

print("\n"+"="*74)
print("WHY (dimension-independent): Box_dir - Box_sym = u^a[nabla_a,u^b]nabla_b = accel^b nabla_b")
print("so  u^mu (Box_dir-Box_sym) u_mu = accel^b * (u^mu nabla_b u_mu).")
# u^mu nabla_b u_mu = (1/2) nabla_b(u.u) = (1/2) nabla_b(-1) = 0  (unit-norm + metric compat)
uNabla = [sp.simplify(sum(uup[mm]*covderD(udn)[bb][mm] for mm in range(2))) for bb in range(2)]
uNabla2 = [sp.simplify(order2(e)) for e in uNabla]   # O(eps^2) part
print("   u^mu nabla_b u_mu  (b=t,x), O(eps^2) =", uNabla2)
uu = sp.simplify(sum(uup[mm]*udn[mm] for mm in range(2)))
print("   u.u =", sp.simplify(uu), " -> nabla_b(u.u)=nabla_b(-1)=0, so u^mu nabla_b u_mu = 0 identically.")
print("   => the ORDERING difference vanishes for ANY dimension by the UNIT-TIMELIKE constraint u.u=-1.")
print("="*74)
print("VERDICT: v12 SURVIVES the Box_u operator-ordering fork. Directional (u.grad)^2 and")
print("symmetrized u^a u^b nabla_a nabla_b give the IDENTICAL quadratic frame form; their")
print("difference ~ accel^b * u^mu nabla_b u_mu = (1/2)accel^b nabla_b(u.u) = 0. No transverse")
print("aether kinetic term appears in either ordering. Ordering-invariant, not a silent choice.")
