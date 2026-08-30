#!/usr/bin/env python3
"""v2 -- fixes two things in wf_tunedsubspace_mond_nr.py:
   (1) BACKGROUND-INDEPENDENT lapse tuning: the c_i are CONSTANTS in the action, so lapse-velocity-freedom
       must hold for GENERIC FRW backgrounds (treat N_g,N_f,a_g,a_f,a_g',a_f' as independent). A tuning that
       only removes the ghost on ONE fine-tuned background does not remove the ghost.
   (2) adds the 5th quadratic invariant  T5 = PV = P^a V_a  (mixed P-trace . V-trace), so the GR / non-
       metricity-scalar direction is correctly L_EH(GammaGamma) = T4 - T5 (NOT T4-T2).
   Then the DECISIVE checks:
     Q1 does a NONZERO MOND acceleration scalar |grad dPhi|^2 survive on the ghost-free (lapse-free) subspace?
     Q2 does the subspace collapse to the single GR / non-metricity 'Q' line (=> ghat frozen, f(Q), DC-013)?
     Q3 how does the surviving static-NR quad form compare to the HEALTHY linearized-Einstein (Lichnerowicz)
        kinetic form for the relative graviton dh -- i.e. is the surviving scalar sector the ghost-free one?"""
import sympy as sp

X=[sp.Symbol('t'),sp.Symbol('x'),sp.Symbol('y'),sp.Symbol('z')]; t=X[0]

def christoffel(gm,gmi):
    G=[[[sp.Integer(0)]*4 for _ in range(4)] for _ in range(4)]
    for l in range(4):
     for m in range(4):
      for n in range(4):
       s=sp.Integer(0)
       for si in range(4):
        s+=gmi[l,si]*(sp.diff(gm[si,m],X[n])+sp.diff(gm[si,n],X[m])-sp.diff(gm[m,n],X[si]))
       G[l][m][n]=sp.expand(s/2)
    return G
def Cdiff(g,gi,gh,ghi):
    Gg=christoffel(g,gi); Gf=christoffel(gh,ghi)
    return [[[sp.expand(Gg[l][m][n]-Gf[l][m][n]) for n in range(4)] for m in range(4)] for l in range(4)]
def invariants(C,g,gi):
    def T1():
        s=sp.Integer(0)
        for a in range(4):
         for b in range(4):
          for m in range(4):
           for n in range(4):
            for r in range(4):
             for sg in range(4):
              s+=C[a][m][n]*C[b][r][sg]*g[a,b]*gi[m,r]*gi[n,sg]
        return sp.expand(s)
    def Pvec(a): return sum(gi[m,n]*C[a][m][n] for m in range(4) for n in range(4))
    def T2(): return sp.expand(sum(g[a,b]*Pvec(a)*Pvec(b) for a in range(4) for b in range(4)))
    def Vcov(mu): return sum(C[a][a][mu] for a in range(4))
    def T3(): return sp.expand(sum(gi[m,n]*Vcov(m)*Vcov(n) for m in range(4) for n in range(4)))
    def T4():
        s=sp.Integer(0)
        for m in range(4):
         for n in range(4):
          for a in range(4):
           for b in range(4):
            s+=gi[m,n]*C[a][m][b]*C[b][n][a]
        return sp.expand(s)
    def T5():  # PV = P^a V_a  (natural contraction, no metric needed: upper a with lower a)
        return sp.expand(sum(Pvec(a)*Vcov(a) for a in range(4)))
    return [T1(),T2(),T3(),T4(),T5()]

cs=list(sp.symbols('c1 c2 c3 c4 c5'))

# ================= PART 1 : background-INDEPENDENT lapse-velocity-free tuning =================
print("="*95); print("PART 1  background-INDEPENDENT lapse-velocity-free tuning (c_i are action constants)"); print("="*95)
Ng,Nf,ag,af=(sp.Function('N_g')(t),sp.Function('N_f')(t),sp.Function('a_g')(t),sp.Function('a_f')(t))
def frw(N,a): return sp.diag(-N**2,a**2,a**2,a**2)
g1=frw(Ng,ag); C1=Cdiff(g1,g1.inv(),frw(Nf,af),frw(Nf,af).inv())
Tf=invariants(C1,g1,g1.inv())
dNg,dNf=sp.symbols('dNg dNf')
subsV={sp.Derivative(Ng,t):dNg,sp.Derivative(Nf,t):dNf}
comb=sp.expand(sum(cs[i]*Tf[i] for i in range(5)).subs(subsV))
p=sp.Poly(comb,dNg,dNf)
# independent-background symbols
Ngs,Nfs,ags,afs,dags,dafs=sp.symbols('Ngs Nfs ags afs dags dafs',positive=True)
bgsub={Ng:Ngs,Nf:Nfs,ag:ags,af:afs,sp.Derivative(ag,t):dags,sp.Derivative(af,t):dafs}
lapse_conditions=[]
for (i,j),coef in p.terms():
    if i+j>0:
        lapse_conditions.append(sp.together(coef.subs(bgsub)))
# each condition must vanish as an identity in the independent background symbols -> collect numerator coeffs
lin_eqs=set()
bgvars=[Ngs,Nfs,ags,afs,dags,dafs]
for cond in lapse_conditions:
    num,den=sp.fraction(cond)
    num=sp.expand(num)
    pol=sp.Poly(num,*bgvars)
    for coef in pol.coeffs():
        ce=sp.expand(coef)
        if ce!=0: lin_eqs.add(ce)
lin_eqs=list(lin_eqs)
print(f"# independent linear conditions on (c1..c5) from background-independent lapse-freedom: {len(lin_eqs)}")
Jac=sp.Matrix([[sp.diff(e,ci) for ci in cs] for e in lin_eqs])
rank=Jac.rank(); ns=Jac.nullspace()
print(f"rank = {rank}  =>  ghost-free (lapse-free) subspace dimension = {5-rank}")
print("nullspace basis (lapse-velocity-free combinations of (c1,c2,c3,c4,c5)):")
for v in ns: print("   ", list(v.T))

# ================= PART 2 : static NR quadratic forms (a,b,x) for all 5 invariants =================
print("\n"+"="*95); print("PART 2  static NR weak field: (a=|grad dPhi|^2, b=|grad dPsi|^2, x=cross) for T1..T5"); print("="*95)
eps=sp.Symbol('eps')
Phi=sp.Function('Phi')(X[1]);Psi=sp.Function('Psi')(X[1]);Phh=sp.Function('Phih')(X[1]);Psh=sp.Function('Psih')(X[1])
def wf(P_,Q_): return sp.diag(-(1+2*eps*P_),1-2*eps*Q_,1-2*eps*Q_,1-2*eps*Q_)
g2=wf(Phi,Psi);gh2=wf(Phh,Psh)
C2=Cdiff(g2,g2.inv(),gh2,gh2.inv())
Tn=invariants(C2,g2,g2.inv())
dPhi=sp.diff(Phi,X[1]);dPsi=sp.diff(Psi,X[1]);dPhh=sp.diff(Phh,X[1]);dPsh=sp.diff(Psh,X[1])
gPhi,gPsi=sp.symbols('gPhi gPsi')
def quad(Tv):
    Ts=sp.series(Tv,eps,0,3).removeO().coeff(eps,2)
    Ts=sp.expand(Ts.subs({dPhh:dPhi-gPhi,dPsh:dPsi-gPsi}))
    return Ts
A=[];B=[];Cx=[]
for i,Tv in enumerate(Tn):
    q=quad(Tv)
    ai=sp.simplify(q.coeff(gPhi,2)); bi=sp.simplify(q.coeff(gPsi,2)); xi=sp.simplify(q.coeff(gPhi,1).coeff(gPsi,1))
    A.append(ai);B.append(bi);Cx.append(xi)
    print(f"   T{i+1}: a={ai}  b={bi}  x={xi}   (form: {q})")
aC=sp.expand(sum(cs[i]*A[i] for i in range(5)))
bC=sp.expand(sum(cs[i]*B[i] for i in range(5)))
xC=sp.expand(sum(cs[i]*Cx[i] for i in range(5)))
print(f"\n general: a(c)={aC}   b(c)={bC}   x(c)={xC}")

# ================= PART 3 : decisive checks =================
print("\n"+"="*95); print("PART 3  DECISIVE"); print("="*95)
us=sp.symbols('u0:%d'%len(ns))
cvec=sp.zeros(5,1)
for k,v in enumerate(ns): cvec+=us[k]*v
csub={cs[i]:sp.simplify(cvec[i]) for i in range(5)}
print("ghost-free subspace general element (c1..c5) =",[sp.simplify(cvec[i]) for i in range(5)])
aLF=sp.simplify(aC.subs(csub));bLF=sp.simplify(bC.subs(csub));xLF=sp.simplify(xC.subs(csub))
print(f"\n[Q1] MOND accel coeff on ghost-free subspace: a = {aLF}")
print(f"     lensing coeff:                            b = {bLF}")
print(f"     cross coeff:                              x = {xLF}")
mond_alive = sp.simplify(aLF)!=0
print(f"     => nonzero MOND acceleration scalar survives the ghost-free tuning? {mond_alive}")

# GR / non-metricity direction = T4 - T5  (EH GammaGamma Lagrangian)
QGR=sp.Matrix([0,0,0,1,-1])
aQ=sp.simplify(sum(QGR[i]*A[i] for i in range(5)))
bQ=sp.simplify(sum(QGR[i]*B[i] for i in range(5)))
xQ=sp.simplify(sum(QGR[i]*Cx[i] for i in range(5)))
Msp=sp.Matrix.hstack(*ns)
inspace=(sp.Matrix.hstack(Msp,QGR).rank()==Msp.rank())
print(f"\n[Q2] GR/non-metricity 'Q' direction = T4 - T5 = (0,0,0,1,-1); its static-NR form a={aQ} b={bQ} x={xQ}")
print(f"     is the GR/Q direction INSIDE the ghost-free subspace? {inspace}")
print(f"     does the ghost-free subspace COLLAPSE to exactly that 1 line (=> ghat frozen=f(Q)=DC-013)? "
      f"{inspace and len(ns)==1}")

# healthy comparison: linearized Einstein / Lichnerowicz kinetic form for the RELATIVE symmetric tensor dh.
# For a symmetric tensor field h_mn the ghost-free (Fierz-Pauli/EH) 2-derivative Lagrangian, in the same
# static-NR (h00=2dPhi, hij=-2dPsi delta) parametrization, has a KNOWN scalar-sector quad form. Compute it by
# taking g=eta+eps*dh, ghat=eta (so C=Gamma(dh)) and evaluating the GR GammaGamma scalar (=T4-T5): that IS
# the linearized-EH kinetic scalar for dh. Its (a,b,x) is the 'healthy' reference.
print(f"\n[Q3] HEALTHY reference = linearized-EH (T4-T5) scalar-sector form: a={aQ} b={bQ} x={xQ}")
if mond_alive:
    print(f"     ghost-free-subspace form (per unit MOND coeff): "
          f"(a,b,x)/a = (1, {sp.simplify(bLF/aLF)}, {sp.simplify(xLF/aLF)})")
    if aQ!=0:
        print(f"     healthy-EH form (per unit a):                    "
              f"(a,b,x)/a = (1, {sp.simplify(bQ/aQ)}, {sp.simplify(xQ/aQ)})")
    print("     (match => the surviving relative-scalar sector is the ghost-free EH kinetic structure AND")
    print("      MOND-producing; mismatch => the surviving form differs from EH => extra scalar to price.)")

print("\n"+"="*95); print("SUMMARY (v2, background-independent, 5-invariant basis)"); print("="*95)
print(f"  ghost-free (lapse-free, bg-indep) subspace dim : {5-rank}")
print(f"  nonzero MOND acceleration scalar survives      : {mond_alive}")
print(f"  collapses to single GR/f(Q) line (ghat frozen) : {inspace and len(ns)==1}")
