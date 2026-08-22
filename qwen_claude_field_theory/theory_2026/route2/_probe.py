import sympy as sp, time
t,r,th,ph=sp.symbols('t r theta phi',real=True)
Z=sp.symbols('Z',positive=True); eps=sp.symbols('epsilon',real=True)
a=sp.Function('a',positive=True)(t); Phi=sp.Function('Phi')(r); psi=sp.Function('psi')(r)
X4=[t,r,th,ph]
N2=1+2*Phi
g=sp.diag(-N2,a**2,a**2*r**2,a**2*r**2*sp.sin(th)**2); gi=g.inv(); sqrtg=sp.sqrt(-g.det())
T=t+eps*psi; dT=[sp.diff(T,X4[i]) for i in range(4)]
normsq=sum(gi[i,j]*dT[i]*dT[j] for i in range(4) for j in range(4))
Nphi=sp.sqrt(-normsq)
u_lo=[sp.simplify(-dT[i]/Nphi) for i in range(4)]
u_up=[sp.simplify(sum(gi[i,j]*u_lo[j] for j in range(4))) for i in range(4)]
def chris(g,gi,X):
    n=4;G=[[[0]*n for _ in range(n)] for _ in range(n)]
    for l in range(n):
        for m in range(n):
            for k in range(n):
                G[l][m][k]=sp.Rational(1,2)*sum(gi[l,s]*(sp.diff(g[s,m],X[k])+sp.diff(g[s,k],X[m])-sp.diff(g[m,k],X[s])) for s in range(n))
    return G
Gam=chris(g,gi,X4)
nab=[[sp.diff(u_lo[mu],X4[nu])-sum(Gam[l][nu][mu]*u_lo[l] for l in range(4)) for mu in range(4)] for nu in range(4)]
a_lo=[sum(u_up[nu]*nab[nu][mu] for nu in range(4)) for mu in range(4)]
t0=time.time()
a2=sum(gi[i,j]*a_lo[i]*a_lo[j] for i in range(4) for j in range(4))
print("a2 built", time.time()-t0)
t0=time.time()
a21=sp.diff(a2,eps).subs(eps,0)
print("a21 diff", time.time()-t0)
t0=time.time()
# leading weak-field: series in a formal smallness lam scaling Phi->lam Phi and adot->lam*H*a
lam,H=sp.symbols('lambda H',positive=True)
a21s=a21.subs(sp.Derivative(a,t),H*a)
a21s=a21s.subs(Phi,lam*Phi).rewrite(sp.Pow)
a21_lead=sp.series(a21s,lam,0,2).removeO()
print("a21 lead", time.time()-t0)
sp.pprint(sp.simplify(a21_lead))
