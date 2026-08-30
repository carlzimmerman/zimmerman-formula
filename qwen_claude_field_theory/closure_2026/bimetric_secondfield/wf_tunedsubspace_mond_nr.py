#!/usr/bin/env python3
"""DECISIVE: does the lapse-velocity-FREE (ghost-free at minisuperspace) tuned subspace of extended-BIMOND
STILL reproduce the MOND acceleration scalar in the NR/weak-field static limit -- or does the same tuning
that removes the ghost annihilate the MOND term / force ghat->Minkowski (constrained f(Q))?

Basis of quadratic invariants of C^a_mn = Gamma(g)-Gamma(ghat)  (SAME as committed bimond_bd_audit_steps123.py):
  T1 = C^a_mn C^b_rs g_ab g^mr g^ns          (full)
  T2 = g_ab P^a P^b,      P^a = g^mn C^a_mn  (P-trace)
  T3 = g^mn V_m V_n,      V_m = C^a_am        (V-trace)
  T4 = g^mn C^a_mb C^b_na                     (Ricci-type; Milgrom's Upsilon kind)

STRATEGY
  Part 1 (TIME sector, FRW minisuperspace): the lapse-velocity-free tuning conditions L1,L2 on (c1..c4).
  Part 2 (STATIC SPATIAL sector, NR weak field g=eta+h(x), ghat=eta+hhat(x)): C is linear in the RELATIVE
         perturbation dh=h-hhat, so each T_i is a rot-invariant quadratic form in (grad dPhi, grad dPsi)
         with dPhi=Phi-Phihat, dPsi=Psi-Psihat.  Read off the coefficients:
             a_i = coeff of |grad dPhi|^2   (the MOND ACCELERATION scalar),
             b_i = coeff of |grad dPsi|^2   (the LENSING/spatial scalar),
             x_i = coeff of grad dPhi . grad dPsi.
  Part 3 (DECISIVE): impose {L1=0,L2=0}; ask whether a(c)=sum c_i a_i is generically NONZERO on that subspace
         (MOND survives), and inspect the lensing structure (Phi=Psi?) and whether the subspace collapses to
         the single 'non-metricity Q / GR' direction (=> ghat frozen => DC-013 single-metric class => DEAD)."""

import sympy as sp

X = [sp.Symbol('t'), sp.Symbol('x'), sp.Symbol('y'), sp.Symbol('z')]
t = X[0]

def christoffel(gm, gmi):
    G=[[[sp.Integer(0)]*4 for _ in range(4)] for _ in range(4)]
    for l in range(4):
        for m in range(4):
            for n in range(4):
                s=sp.Integer(0)
                for si in range(4):
                    s+= gmi[l,si]*(sp.diff(gm[si,m],X[n])+sp.diff(gm[si,n],X[m])-sp.diff(gm[m,n],X[si]))
                G[l][m][n]=sp.expand(s/2)
    return G

def Cdiff(g, gi, gh, ghi):
    Gg=christoffel(g,gi); Gf=christoffel(gh,ghi)
    return [[[sp.expand(Gg[l][m][n]-Gf[l][m][n]) for n in range(4)] for m in range(4)] for l in range(4)]

# ---- the four invariants, contracted with the g-metric (physical metric), as in the committed script ----
def invariants(C, g, gi):
    def T1():
        s=sp.Integer(0)
        for a in range(4):
         for b in range(4):
          for m in range(4):
           for n in range(4):
            for r in range(4):
             for sg in range(4):
              s+= C[a][m][n]*C[b][r][sg]*g[a,b]*gi[m,r]*gi[n,sg]
        return sp.expand(s)
    def P(a): return sum(gi[m,n]*C[a][m][n] for m in range(4) for n in range(4))
    def T2(): return sp.expand(sum(g[a,b]*P(a)*P(b) for a in range(4) for b in range(4)))
    def V(mu): return sum(C[a][a][mu] for a in range(4))
    def T3(): return sp.expand(sum(gi[m,n]*V(m)*V(n) for m in range(4) for n in range(4)))
    def T4():
        s=sp.Integer(0)
        for m in range(4):
         for n in range(4):
          for a in range(4):
           for b in range(4):
            s+= gi[m,n]*C[a][m][b]*C[b][n][a]
        return sp.expand(s)
    return [T1(),T2(),T3(),T4()]

c1,c2,c3,c4 = sp.symbols('c1 c2 c3 c4')
cs=[c1,c2,c3,c4]

# ==========================================================================================================
# PART 1 -- TIME SECTOR (FRW minisuperspace): lapse-velocity-free tuning conditions
# ==========================================================================================================
print("="*95)
print("PART 1  TIME SECTOR (two-FRW minisuperspace): lapse-velocity-free (ghost-free) tuning conditions")
print("="*95)
Ng,Nf,ag,af = (sp.Function('N_g')(t),sp.Function('N_f')(t),sp.Function('a_g')(t),sp.Function('a_f')(t))
def frw(N,a): return sp.diag(-N**2,a**2,a**2,a**2)
g1=frw(Ng,ag); gi1=g1.inv(); gh1=frw(Nf,af); ghi1=gh1.inv()
C1=Cdiff(g1,gi1,gh1,ghi1)
T_frw=invariants(C1,g1,gi1)
dNg,dNf=sp.symbols('dNg dNf')
subsV={sp.Derivative(Ng,t):dNg, sp.Derivative(Nf,t):dNf}
comb=sp.expand(sum(cs[i]*T_frw[i] for i in range(4)).subs(subsV))
# collect ALL lapse-velocity-dependent pieces: coeff of dNg^2, dNf^2, dNg*dNf, dNg^1, dNf^1
p=sp.Poly(comb,dNg,dNf)
lapse_terms={}
for (i,j),coef in p.terms():
    if i+j>0:
        lapse_terms[(i,j)]=sp.simplify(coef)
print("lapse-velocity monomials present in c.T (must all vanish for lapse to stay a multiplier):")
conds=[]
for k,v in lapse_terms.items():
    print(f"   dNg^{k[0]} dNf^{k[1]} :  {v}")
    conds.append(v)
sol_lapse=sp.solve(conds,cs,dict=True)
print("\nSOLVE {all lapse-velocity coeffs = 0} for (c1,c2,c3,c4):")
print("   ->", sol_lapse)
# Extract explicit linear conditions L1,L2 (rank of the condition set)
Mrows=[]
for v in conds:
    Mrows.append([sp.expand(v).coeff(ci) if sp.Poly(sp.expand(v),*cs).is_zero==False else 0 for ci in cs])
Mmat=sp.Matrix([[sp.diff(v,ci) for ci in cs] for v in conds])   # linear in c => Jacobian gives the rows
Mmat=sp.Matrix([[sp.simplify(e) for e in row] for row in Mmat.tolist()])
print("\ncondition matrix rows (coeff of c1..c4 in each lapse condition):")
sp.pprint(Mmat)
rank=Mmat.rank()
ns=Mmat.nullspace()
print(f"rank of lapse-free condition matrix = {rank}  =>  ghost-free subspace dimension = {4-rank}")
print("nullspace basis (each vector = a lapse-velocity-free combination of (c1,c2,c3,c4)):")
for v in ns: sp.pprint(v.T)

# ==========================================================================================================
# PART 2 -- STATIC SPATIAL SECTOR (NR weak field): the MOND acceleration + lensing quadratic forms
# ==========================================================================================================
print("\n"+"="*95)
print("PART 2  STATIC NR WEAK FIELD: g=eta+h(x), ghat=eta+hhat(x)  =>  C linear in dh=h-hhat")
print("        1D static field (Phi,Psi,Phihat,Psihat depend on x); recovers the full isotropic quad form")
print("="*95)
eps=sp.Symbol('eps')
Phi=sp.Function('Phi')(X[1]); Psi=sp.Function('Psi')(X[1])
Phh=sp.Function('Phih')(X[1]); Psh=sp.Function('Psih')(X[1])
def wf(Phi_,Psi_):
    return sp.diag(-(1+2*eps*Phi_), 1-2*eps*Psi_, 1-2*eps*Psi_, 1-2*eps*Psi_)
g2=wf(Phi,Psi); gh2=wf(Phh,Psh)
# metric inverses to O(eps) (series) -- use exact inverse then series later
gi2=g2.inv(); ghi2=gh2.inv()
C2=Cdiff(g2,gi2,gh2,ghi2)
T_nr=invariants(C2,g2,gi2)
# leading quadratic-in-eps part: since C ~ O(eps), T ~ O(eps^2). Take coeff of eps^2.
dPhi=sp.diff(Phi,X[1]); dPsi=sp.diff(Psi,X[1]); dPhh=sp.diff(Phh,X[1]); dPsh=sp.diff(Psh,X[1])
# relative-potential derivative symbols
gPhi,gPsi=sp.symbols('gPhi gPsi')   # grad dPhi , grad dPsi   (dPhi_rel = Phi-Phihat)
def leadquad(Tv):
    Ts=sp.series(Tv,eps,0,3).removeO()
    Ts=Ts.coeff(eps,2)
    # substitute derivatives -> relative combos:  Phi'-Phih' = gPhi ,  Psi'-Psih' = gPsi
    # do it by expressing everything in (Phi'-Phih') and (Psi'-Psih'): replace Phih'->Phi'-gPhi etc.
    Ts=Ts.subs({dPhh:dPhi-gPhi, dPsh:dPsi-gPsi})
    Ts=sp.expand(Ts)
    # now Ts should depend ONLY on gPhi,gPsi (C depends only on dh) -- verify no residual Phi',Psi'
    return sp.simplify(Ts)
coeffs=[]
print("leading O(eps^2) static-NR value of each invariant, in terms of grad(dPhi)=gPhi, grad(dPsi)=gPsi:")
for i,Tv in enumerate(T_nr):
    q=leadquad(Tv)
    resid=q.has(dPhi) or q.has(dPsi)
    a_i=sp.simplify(q.coeff(gPhi,2))         # |grad dPhi|^2
    b_i=sp.simplify(q.coeff(gPsi,2))         # |grad dPsi|^2
    x_i=sp.simplify(q.coeff(gPhi,1).coeff(gPsi,1))  # cross
    coeffs.append((a_i,b_i,x_i))
    print(f"   T{i+1}: {q}")
    print(f"        a(|grad dPhi|^2)={a_i}   b(|grad dPsi|^2)={b_i}   x(cross)={x_i}   depends-only-on-dh:{not resid}")

a=[c[0] for c in coeffs]; b=[c[1] for c in coeffs]; xx=[c[2] for c in coeffs]
aC=sp.expand(sum(cs[i]*a[i] for i in range(4)))   # MOND acceleration coeff of the general combination
bC=sp.expand(sum(cs[i]*b[i] for i in range(4)))
xC=sp.expand(sum(cs[i]*xx[i] for i in range(4)))
print("\ngeneral combination c.T static-NR quadratic form:")
print("   MOND accel coeff  a(c) =", aC)
print("   lensing   coeff   b(c) =", bC)
print("   cross     coeff   x(c) =", xC)

# ==========================================================================================================
# PART 3 -- DECISIVE: is MOND alive on the lapse-free subspace? lensing? ghat frozen?
# ==========================================================================================================
print("\n"+"="*95)
print("PART 3  DECISIVE CHECK")
print("="*95)
# parameterize the lapse-free subspace by the nullspace basis
params=sp.symbols('u0:%d'%len(ns))
cvec=sp.zeros(4,1)
for k,v in enumerate(ns):
    cvec+= params[k]*v
csub={cs[i]:sp.simplify(cvec[i]) for i in range(4)}
print("lapse-free (ghost-free) subspace, general element (c1..c4) =")
for i in range(4): print(f"     c{i+1} =", sp.simplify(cvec[i]))
aLF=sp.simplify(aC.subs(csub)); bLF=sp.simplify(bC.subs(csub)); xLF=sp.simplify(xC.subs(csub))
print("\nON the lapse-free subspace:")
print("   MOND acceleration coeff a =", aLF)
print("   lensing coeff           b =", bLF)
print("   cross coeff             x =", xLF)
mond_alive = not (sp.simplify(aLF)==0)
print(f"\n[Q1] does the ghost-free tuning leave a NONZERO MOND acceleration scalar |grad dPhi|^2 ?  {mond_alive}")

# lensing structure: for the PHYSICAL metric g, MOND lensing wants the interaction to feed Phi_g and Psi_g
# equally. The interaction quadratic form ratio b/a (and cross) tells whether the spatial (lensing) response
# matches the temporal (dynamics) response. eta=1 (Phi=Psi) iff the induced source structure is symmetric.
if mond_alive:
    ratio=sp.simplify(bLF/aLF)
    print(f"[Q2] lensing/dynamics quadratic-form ratio  b/a = {ratio}   cross/a = {sp.simplify(xLF/aLF)}")
    print("     (b/a and cross encode how strongly the SAME interaction sources the spatial potential dPsi")
    print("      relative to the acceleration dPhi; the Phi=Psi lensing then follows from the coupled g/ghat")
    print("      EOMs -- a nonzero symmetric (a,b,x) form is the pre-req, an all-zero-a form is fatal.)")

# ghat-frozen test: does the surviving subspace collapse to the SINGLE 'GR/non-metricity Q' direction?
# The GR (linearized-R-equivalent) 'Gamma-Gamma' Lagrangian is  L_GG = g^mn(Gamma^a_mb Gamma^b_na - Gamma^a_mn Gamma^b_ab)
# = T4 - T2  in this basis (Ricci-type minus P-trace).  If lapse-free subspace == span{this one vector} => ghat
# is pure-gauge (f(Q), single metric) => DC-013 class => DEAD.  If it is a HIGHER-dim space containing genuinely
# bimetric MOND directions, ghat stays dynamical.
QGR=sp.Matrix([0,-1,0,1])   # T4 - T2  (the GR/non-metricity-scalar direction)
print("\n[Q3] does the lapse-free subspace COLLAPSE to only the GR/non-metricity 'Q' direction (T4 - T2)?")
print(f"     lapse-free subspace dim = {len(ns)} ; GR/Q direction = (c1,c2,c3,c4)=(0,-1,0,1)")
# is QGR in the lapse-free subspace? and is the subspace exactly 1-dim?
inspace=False
if len(ns)>=1:
    Msp=sp.Matrix.hstack(*ns)
    aug=sp.Matrix.hstack(Msp,QGR)
    inspace = (aug.rank()==Msp.rank())
print(f"     GR/Q direction lies in lapse-free subspace? {inspace}")
print(f"     lapse-free subspace is EXACTLY the 1-dim GR/Q line (=> ghat frozen, f(Q), DEAD)? "
      f"{inspace and len(ns)==1}")
# MOND coeff of the pure GR/Q direction (should vanish: GR has no MOND scalar)
aQ=sp.simplify(sum(QGR[i]*a[i] for i in range(4)))
print(f"     MOND accel coeff of the pure GR/Q direction a(Q) = {aQ}  (0 => GR alone gives no MOND, as expected)")

print("\n"+"="*95)
print("SUMMARY")
print("="*95)
print(f"  lapse-free (ghost-free minisuperspace) subspace dimension : {4-rank}")
print(f"  MOND acceleration scalar survives on that subspace        : {mond_alive}")
print(f"  subspace collapses to single-metric GR/f(Q) line          : {inspace and len(ns)==1}")
