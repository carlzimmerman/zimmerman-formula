#!/usr/bin/env python3
# SUPERSEDED by ghost_stuckelberg_helicity0.py. This naive momentum-space scalar W-matrix is GAUGE-
# CONTAMINATED: the PURE-EH calibration (which MUST be healthy) shows a spurious NEGATIVE W eigenvalue
# (the relative-diff gauge mode), so its eigenvalue signs are NOT reliable ghost indicators. Kept for the
# record; the correct gauge-robust test is the Stuckelberg helicity-0 analysis.
"""DECISIVE linearized ghost analysis of the MOND-alive ghost-free-tuned derivative-bimetric subspace.
Setup: interaction depends only on dh = h - ghat (relative perturbation); the two Einstein-Hilbert terms
give the relative-graviton the linearized-EH (Gamma-Gamma = T4-T5) 2-derivative kinetic operator; the
connection-difference interaction ADDS lambda*(Sum c_i T_i). Around Minkowski, momentum space
dh_mn = eps_mn e^{ikx}, dGamma^l_mn -> C^l_mn = (1/2) eta^{ls}(k_m eps_sn + k_n eps_sm - k_s eps_mn).
DECISIVE QUESTION: on the a!=0 (MOND-producing) directions of the ghost-free 2-D subspace, does the SCALAR
sector propagate a WRONG-SIGN (omega^2) kinetic mode (=> BD ghost, 8 DOF, DEAD) or is the extra scalar
non-dynamical/healthy (=> elliptic AQUAL-like auxiliary, 7 DOF, ALIVE)? Calibrated against pure EH."""
import sympy as sp

eta = sp.diag(-1,1,1,1)
etaI = eta.inv()
k = sp.Matrix(sp.symbols('k0 k1 k2 k3', real=True))
# symmetric perturbation eps_mn
E = sp.zeros(4,4)
es = {}
for a in range(4):
    for b in range(a,4):
        s = sp.Symbol(f'e{a}{b}', real=True); es[(a,b)]=s; E[a,b]=s; E[b,a]=s

def Cconn(E):
    # C^l_mn = (1/2) eta^{ls}(k_m E_sn + k_n E_sm - k_s E_mn)   (indices: l up, m,n down)
    C=[[[sp.Integer(0)]*4 for _ in range(4)] for _ in range(4)]
    for l in range(4):
        for m in range(4):
            for n in range(4):
                val=sp.Integer(0)
                for sgm in range(4):
                    val+= etaI[l,sgm]*(k[m]*E[sgm,n]+k[n]*E[sgm,m]-k[sgm]*E[m,n])
                C[l][m][n]=sp.expand(val/2)
    return C
C=Cconn(E)

def low(vecup):  # lower an index with eta (for contractions we mostly use explicit eta)
    return vecup
# invariants (same 5 as bimond_5invariant_ghostfree_subspace, contracted with eta)
def T1():
    s=sp.Integer(0)
    for a in range(4):
     for b in range(4):
      for m in range(4):
       for n in range(4):
        for r in range(4):
         for sg in range(4):
          s+=C[a][m][n]*C[b][r][sg]*eta[a,b]*etaI[m,r]*etaI[n,sg]
    return sp.expand(s)
def Pvec(a): return sum(etaI[m,n]*C[a][m][n] for m in range(4) for n in range(4))
def T2(): return sp.expand(sum(eta[a,b]*Pvec(a)*Pvec(b) for a in range(4) for b in range(4)))
def Vcov(mu): return sum(C[a][a][mu] for a in range(4))
def T3(): return sp.expand(sum(etaI[m,n]*Vcov(m)*Vcov(n) for m in range(4) for n in range(4)))
def T4():
    s=sp.Integer(0)
    for m in range(4):
     for n in range(4):
      for a in range(4):
       for b in range(4):
        s+=etaI[m,n]*C[a][m][b]*C[b][n][a]
    return sp.expand(s)
def T5(): return sp.expand(sum(Pvec(a)*Vcov(a) for a in range(4)))
T=[T1(),T2(),T3(),T4(),T5()]
print("invariants built.")

# ghost-free 2-D subspace: (c1..c5) = (-u0, -u1/2, -u1/2, u0, u1)
u0,u1,lam = sp.symbols('u0 u1 lam', real=True)
cvec=[-u0, -u1/2, -u1/2, u0, u1]
Int = sp.expand(sum(cvec[i]*T[i] for i in range(5)))
EH  = sp.expand(T[3]-T[4])          # linearized-EH Gamma-Gamma = T4 - T5  (healthy reference)
Ltot = sp.expand(sp.Rational(1,2)*EH + lam*Int)

# ---- restrict to SCALAR sector for k=(w,0,0,kap): rotation-invariant components about z ----
w,kap = sp.symbols('omega kappa', real=True)
A,Bv,Cc,S = sp.symbols('A B C S', real=True)   # eps00=A, eps03=B, eps33=C, eps11=eps22=S
scalar_sub = {es[(0,0)]:A, es[(0,3)]:Bv, es[(3,3)]:Cc, es[(1,1)]:S, es[(2,2)]:S,
              es[(0,1)]:0, es[(0,2)]:0, es[(1,2)]:0, es[(1,3)]:0, es[(2,3)]:0}
ksub={k[0]:w,k[1]:0,k[2]:0,k[3]:kap}

def scalar_form(expr):
    return sp.expand(expr.subs(scalar_sub).subs(ksub))

def analyze(name, L):
    Ls=scalar_form(L)
    fields=[A,Bv,Cc,S]
    # quadratic-form matrix Q (symmetric) in the 4 scalar amplitudes
    Q=sp.zeros(4,4)
    for i in range(4):
        Q[i,i]=sp.diff(Ls,fields[i],2)/2*2   # coefficient of field_i^2 is Q[i,i]/... use Hessian/2
    H=sp.hessian(Ls,fields)                  # Hessian = 2*Q for L=1/2 x^T Q x ; use H directly as the form
    # kinetic matrix W = coefficient of omega^2 in H
    W=sp.Matrix(4,4, lambda i,j: sp.expand(H[i,j]).coeff(w,2))
    # gradient (spatial) matrix at omega=0
    G=sp.Matrix(4,4, lambda i,j: sp.expand(H[i,j]).subs(w,0))
    print(f"\n=== {name} ===")
    print("  omega^2 kinetic matrix W (fields A,B,C,S):")
    sp.pprint(W)
    print("  rank(W) =", W.rank(), "  (# fields with a bare time-kinetic term before constraints)")
    # AUXILIARY REDUCTION: fields with no omega^2 anywhere are auxiliary; integrate them out.
    aux=[i for i in range(4) if all(W[i,j]==0 for j in range(4)) and all(W[j,i]==0 for j in range(4))]
    dyn=[i for i in range(4) if i not in aux]
    print("  auxiliary (no time-kinetic) fields:", [str(fields[i]) for i in aux],
          " dynamical candidates:", [str(fields[i]) for i in dyn])
    return H, fields, aux, dyn

# Calibrate on pure EH (should give NO healthy propagating scalar -> the extra-scalar ghost test baseline)
analyze("PURE EH (lam=0)", sp.Rational(1,2)*EH)

# a=0 (EH-like) direction inside the subspace: from a(c)=-4u0-2u1=0 => u1=-2u0
analyze("a=0 direction (u1=-2u0, lam=1)", (sp.Rational(1,2)*EH + 1*Int).subs({u1:-2*u0, u0:1}))

# a!=0 MOND-alive direction T4-T1  => u0=1,u1=0
H,flds,aux,dyn = analyze("a!=0 MOND-alive T4-T1 (u0=1,u1=0,lam=1)", (sp.Rational(1,2)*EH + 1*Int).subs({u0:1,u1:0}))

# ---- decisive: integrate out auxiliaries, get reduced kinetic matrix for dynamical scalars, check signs ----
print("\n=== DECISIVE: reduce out auxiliaries on the a!=0 direction, signature of the physical scalar kinetic term ===")
Ls = scalar_form((sp.Rational(1,2)*EH + 1*Int).subs({u0:1,u1:0}))
fields=[A,Bv,Cc,S]
# solve EOM for auxiliary fields (linear in them) and substitute back
auxf=[fields[i] for i in aux]; dynf=[fields[i] for i in dyn]
eqs=[sp.diff(Ls,af) for af in auxf]
sol=sp.solve(eqs, auxf, dict=True)
if sol:
    Lred=sp.expand(Ls.subs(sol[0]))
    print("  auxiliaries solved:", {str(k_):sp.simplify(v) for k_,v in sol[0].items()})
else:
    Lred=Ls; print("  (no linear auxiliary solution; using full form)")
Hred=sp.hessian(Lred, dynf) if dynf else sp.Matrix([[0]])
Wred=sp.Matrix(len(dynf),len(dynf), lambda i,j: sp.expand(Hred[i,j]).coeff(w,2)) if dynf else sp.Matrix([[0]])
print("  reduced physical dynamical scalars:", [str(f) for f in dynf])
print("  reduced time-kinetic matrix W_red:"); sp.pprint(Wred)
if dynf:
    ev=list(Wred.eigenvals().keys())
    evs=[sp.simplify(e) for e in ev]
    print("  eigenvalues of W_red:", evs)
    neg=[e for e in evs if (e.is_negative if e.is_number else None)]
    print("  => NEGATIVE (ghost) eigenvalues present?:", any((e.is_number and e<0) for e in evs))
