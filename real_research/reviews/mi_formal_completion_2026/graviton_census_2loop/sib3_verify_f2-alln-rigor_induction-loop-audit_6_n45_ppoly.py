#!/usr/bin/env python3
r"""Push the FULL graviton-dressed tensor to n=4 AND n=5 with complex phases (lighter than trig),
detecting the p-POLYNOMIAL (spatial cone seed) on the frame kinetic. This is the order range the
lane NEVER reached with the graviton on (setup_1 CAS stopped at n=3; rigor_1 n=8 dropped graviton).
p-poly present at n=4 or 5 with F2 intact => the all-n claim CRACKS => FATAL."""
import sympy as sp, functools, time, importlib.util
print=functools.partial(print, flush=True)
spec=importlib.util.spec_from_file_location('s1','sib3_setup_1_seagull_vertex_generaln.py')
s1=importlib.util.module_from_spec(spec); spec.loader.exec_module(s1)
trunc=s1.trunc; eps=s1.eps; eps2=s1.eps2; p=s1.p; q=s1.q
t,x,y,z=s1.t,s1.x,s1.y,s1.z; crd=[t,x,y,z]; I=sp.I; H=s1.H
a=sp.exp(H*t)
h=eps2*sp.Function('H_TT')(t)*sp.exp(I*q*x)
g=sp.diag(-1,a**2,a**2*(1+h),a**2*(1-h))
G=s1.christoffel(g)
V=sp.Function('V')(t)
uy_up=eps*V*sp.exp(I*p*x)
g00=g[0,0]; gyy=g[2,2]; u0=sp.symbols('u0d')
sol=sp.solve(sp.Eq(g00*u0**2+gyy*uy_up**2,-1),u0)
pick=[s for s in sol if sp.simplify(s.subs({eps:0,eps2:0})-1)==0]
u0v=trunc(pick[0])
u_up=sp.Matrix([u0v,0,uy_up,0])
u_low=sp.Matrix([trunc(sum(g[m,nn]*u_up[nn] for nn in range(4))) for m in range(4)])
def Dop(w):
    out=[]
    for m in range(4):
        e=0
        for al in range(4):
            e+=u_up[al]*(sp.diff(w[m],crd[al]) - sum(G[l][al][m]*w[l] for l in range(4)))
        out.append(trunc(e))
    return sp.Matrix(out)
def vertex(n):
    v=u_low
    for _ in range(2*n):
        v=Dop(v)
    B=trunc(sp.expand(sum(u_up[m]*v[m] for m in range(4))))
    return sp.expand(B.coeff(eps,2).coeff(eps2,2))
def ppoly(c):
    c=sp.expand(c).replace(lambda e: e.func==sp.exp, lambda e: sp.Integer(1))
    return sp.expand(c).has(p)
for n in (4,5):
    t0=time.time()
    c=vertex(n)
    hp=ppoly(c)
    print(f"n={n} (full graviton-dressed tensor, complex phases): p-polynomial on frame kinetic? {hp}  [{'CONE SEED -- FATAL' if hp else 'p-FREE spectator'}]  [{time.time()-t0:.1f}s]")
