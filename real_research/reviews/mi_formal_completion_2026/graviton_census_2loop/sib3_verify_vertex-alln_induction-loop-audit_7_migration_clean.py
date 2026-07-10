#!/usr/bin/env python3
"""AUDIT 7 (clean): single-graviton migration k=1..10 (n up to 5), plus a MOVE control:
give the frame a spurious u^x component (break the 'u has no x-slot' structure) and watch
the graviton gradient sin(qx) ESCAPE into the scalar B_n -> proving the x-trapping is the
real protector, not an artifact."""
import sympy as sp, functools, time
print=functools.partial(print,flush=True)
t,x,y,z=sp.symbols('t x y z',real=True)
H=sp.symbols('H',positive=True)
q1,p=sp.symbols('q1 p',real=True)
e1,ep=sp.symbols('e1 ep',real=True)
crd=[t,x,y,z]; nm=['t','x','y','z']
A1=sp.Function('A1')(t);V=sp.Function('V')(t)
mu_x=sp.symbols('mu_x',real=True)  # MOVE knob: spurious u^x = mu_x*ep*V*cos(px)
def trunc(expr):
    expr=sp.series(expr,e1,0,2).removeO()
    expr=sp.series(expr,ep,0,3).removeO()
    return sp.expand(expr)
a=sp.exp(H*t)
h=e1*A1*sp.cos(q1*x)
g=sp.diag(-1,a**2,a**2*(1+h),a**2*(1-h))
gi=g.inv();n=4
G=[[[sp.Integer(0)]*n for _ in range(n)] for _ in range(n)]
for l in range(n):
    for m in range(n):
        for nu in range(n):
            G[l][m][nu]=trunc(sum(gi[l,s]*(sp.diff(g[s,m],crd[nu])+sp.diff(g[s,nu],crd[m])-sp.diff(g[m,nu],crd[s])) for s in range(n))/2)
def run(with_ux):
    uy=ep*V*sp.cos(p*x)
    ux = mu_x*ep*V*sp.cos(p*x) if with_ux else sp.Integer(0)
    u0=sp.symbols('u0d')
    sol=sp.solve(sp.Eq(g[0,0]*u0**2+g[1,1]*ux**2+g[2,2]*uy**2,-1),u0)
    pick=[s for s in sol if sp.simplify(s.subs({e1:0,ep:0})-1)==0]
    u0v=trunc(pick[0])
    u_up=sp.Matrix([u0v,ux,uy,0])
    u_low=sp.Matrix([trunc(sum(g[m,nn]*u_up[nn] for nn in range(4))) for m in range(4)])
    def Dop(w):
        out=[]
        for m in range(n):
            e=0
            for al in range(n):
                e+=u_up[al]*(sp.diff(w[m],crd[al])-sum(G[l][al][m]*w[l] for l in range(n)))
            out.append(trunc(e))
        return sp.Matrix(out)
    v=u_low
    res=[]
    for k in range(1,11):
        v=Dop(v)
        escaped=[nm[m] for m in (0,2,3) if v[m].has(sp.sin(q1*x))]
        if k%2==0:
            B=trunc(sum(u_up[m]*v[m] for m in range(4)))
            seag=sp.expand(B).coeff(e1,1).coeff(ep,2)
            res.append((k, escaped, seag.has(sp.sin(q1*x))))
    return res

print("=== F2-INTACT (u^x=0): does graviton gradient escape x-comp / reach scalar B_n? ===")
for k,esc,inB in run(False):
    print(f"  n={k//2}: sinq escaped to non-x comps={esc} | B_n has sin(qx)?={inB}")
print("\n=== MOVE (u^x = mu_x*ep*V*cos(px), spurious x-slot): should let gradient ESCAPE ===")
for k,esc,inB in run(True):
    print(f"  n={k//2}: sinq escaped to non-x comps={esc} | B_n has sin(qx)?={inB}")
