"""Rank of the lapse VELOCITY-Hessian d^2L/d(Ndot)^2 for generic linear M=sum c_i T_i, and the true
constant-coefficient velocity-free locus. This is the object that governs the PRIMARY lapse constraint."""
import sympy as sp
t = sp.Symbol('t')
Ng, Nf, ag, af = (sp.Function('N_g')(t), sp.Function('N_f')(t), sp.Function('a_g')(t), sp.Function('a_f')(t))
X = [t, sp.Symbol('x'), sp.Symbol('y'), sp.Symbol('z')]
def metric(N,a): return sp.diag(-N**2, a**2, a**2, a**2)
g=metric(Ng,ag); gi=g.inv(); gh=metric(Nf,af); ghi=gh.inv()
def chris(gm,gmi):
    G=[[[sp.Integer(0)]*4 for _ in range(4)] for _ in range(4)]
    for l in range(4):
     for m in range(4):
      for n in range(4):
       s=sp.Integer(0)
       for si in range(4): s+=gmi[l,si]*(sp.diff(gm[si,m],X[n])+sp.diff(gm[si,n],X[m])-sp.diff(gm[m,n],X[si]))
       G[l][m][n]=s/2
    return G
Gg=chris(g,gi); Gf=chris(gh,ghi)
C=[[[sp.simplify(Gg[l][m][n]-Gf[l][m][n]) for n in range(4)] for m in range(4)] for l in range(4)]
def T_full():
    s=0
    for a in range(4):
     for b in range(4):
      for m in range(4):
       for n in range(4):
        for r in range(4):
         for sg in range(4): s+=C[a][m][n]*C[b][r][sg]*g[a,b]*gi[m,r]*gi[n,sg]
    return s
def P(a): return sum(gi[m,n]*C[a][m][n] for m in range(4) for n in range(4))
def T_P(): return sum(g[a,b]*P(a)*P(b) for a in range(4) for b in range(4))
def V(mu): return sum(C[a][a][mu] for a in range(4))
def T_V(): return sum(gi[m,n]*V(m)*V(n) for m in range(4) for n in range(4))
def T_R():
    s=0
    for m in range(4):
     for n in range(4):
      for a in range(4):
       for b in range(4): s+=gi[m,n]*C[a][m][b]*C[b][n][a]
    return s
T1,T2,T3,T4=map(sp.expand,(T_full(),T_P(),T_V(),T_R()))
dNg,dNf=sp.symbols('dNg dNf',real=True)
c1,c2,c3,c4=sp.symbols('c1 c2 c3 c4',real=True)
M=sp.expand((c1*T1+c2*T2+c3*T3+c4*T4).subs({sp.Derivative(Ng,t):dNg,sp.Derivative(Nf,t):dNf}))
# velocity Hessian (only the interaction; measure factor is >0 and does not change the RANK/nullvector)
Hgg=sp.simplify(sp.diff(M,dNg,dNg)); Hgf=sp.simplify(sp.diff(M,dNg,dNf)); Hff=sp.simplify(sp.diff(M,dNf,dNf))
H=sp.Matrix([[Hgg,Hgf],[Hgf,Hff]])
print("velocity-Hessian H (lapses) =")
sp.pprint(H)
print("det H =", sp.simplify(H.det()))
S=sp.symbols('S'); Hs=H.subs(c1,S-c2-c3-c4)  # S = sum c_i
print("=> H is proportional to (c1+c2+c3+c4); det H =", sp.simplify(H.det()))
print("rank of H for generic sum!=0: ", H.subs({c1:1,c2:0,c3:0,c4:0,Ng:sp.Symbol('n'),Nf:sp.Symbol('m')}).rank())
# null vector of H
nv = H.nullspace()
print("null vector(s) of H:", [sp.simplify(v.T) for v in nv])

# --- constant-coefficient FULLY velocity-free locus: kill EVERY dNg,dNf term identically ---
dag,daf=sp.symbols('dag daf',real=True)  # dummies for a-dot
ng,nf,Ag,Af=sp.symbols('ng nf Ag Af',positive=True)
rep={sp.Derivative(ag,t):dag, sp.Derivative(af,t):daf, Ng:ng,Nf:nf,ag:Ag,af:Af}
Md=sp.expand(M.subs(rep))
# clear denominators
Md=sp.together(Md); num,den=sp.fraction(Md); num=sp.expand(num)
# require coefficient of every monomial containing dNg or dNf to vanish, for constant c_i
pol=sp.Poly(num,dNg,dNf,ng,nf,Ag,Af,dag,daf)
conds=[]
for mon,co in pol.terms():
    if mon[0]>0 or mon[1]>0:   # power of dNg or dNf > 0  => velocity-carrying
        conds.append(co)
conds=list(set(conds))
sol=sp.solve(conds,[c1,c2,c3,c4],dict=True)
print("\nCONSTANT-COEFFICIENT velocity-free locus (kills ALL Ndot terms):", sol)
