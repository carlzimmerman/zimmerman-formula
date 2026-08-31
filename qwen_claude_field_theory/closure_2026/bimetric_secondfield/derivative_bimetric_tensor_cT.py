#!/usr/bin/env python3
# PERMANENT ARTIFACT (adversarial workflow, independently re-verified). Linearized ghost/c_T gates on the
# MOND-alive (a!=0) directions of the ghost-free-tuned derivative-bimetric subspace. Refs: Ostrogradsky
# instability (Woodard, Scholarpedia 2015) for the box^2 higher-derivative ghost; DC-013 slip-lock; c_T
# GW170817 bound Abbott+ 2017. NOT citing PLB 806 (2020) 135970 (misattributed f(Q) letter).
"""GATE = TENSOR SECTOR + c_T on the a!=0 (MOND-alive) direction u0=1,u1=0 of the ghost-free-tuned
derivative-bimetric subspace. Reuses the EXACT momentum-space Cconn / 5-invariant conventions of
ghost_stuckelberg_helicity0.py and ghost_analysis_a_nonzero_subfamily.py.

L = (1/2)(T4-T5) [linearized-EH GammaGamma kinetic for the relative graviton]  +  lam*Int,
Int = sum cvec[i]*T_i,  cvec = [-u0, -u1/2, -u1/2, u0, u1],  lam ~ a0^2.

TT (spin-2) polarizations transverse to k=(w,0,0,kap) (wave along z):
  CROSS:  eps_12 = eps_21 = h        (rest 0)
  PLUS :  eps_11 = h, eps_22 = -h    (rest 0)   [traceless, transverse]
Both are genuine TT (k_m eps^m_n = 0 since k only has 0,3 comps and eps only 1,2 comps).

Report: (a) sign/health of TT kinetic term (vs pure-EH calibration, which MUST be healthy);
        (b) dispersion relation f(w,kap)=0 and c_T^2 = w^2/kap^2 on-shell; and the fractional shift vs 1.
"""
import sympy as sp

eta = sp.diag(-1,1,1,1); etaI = eta.inv()
k = sp.Matrix(sp.symbols('k0 k1 k2 k3', real=True))
w,kap = sp.symbols('omega kappa', real=True, positive=True)
u0,u1,lam = sp.symbols('u0 u1 lam', real=True)
h = sp.Symbol('h', real=True)

def Cconn(E):
    C=[[[sp.Integer(0)]*4 for _ in range(4)] for _ in range(4)]
    for l in range(4):
     for m in range(4):
      for n in range(4):
       v=sp.Integer(0)
       for s in range(4): v+=etaI[l,s]*(k[m]*E[s,n]+k[n]*E[s,m]-k[s]*E[m,n])
       C[l][m][n]=sp.expand(v/2)
    return C

def invs(C):
    T1=sum(C[a][m][n]*C[b][r][s]*eta[a,b]*etaI[m,r]*etaI[n,s]
           for a in range(4) for b in range(4) for m in range(4) for n in range(4) for r in range(4) for s in range(4))
    P=[sum(etaI[m,n]*C[a][m][n] for m in range(4) for n in range(4)) for a in range(4)]
    T2=sum(eta[a,b]*P[a]*P[b] for a in range(4) for b in range(4))
    V=[sum(C[a][a][mu] for a in range(4)) for mu in range(4)]
    T3=sum(etaI[m,n]*V[m]*V[n] for m in range(4) for n in range(4))
    T4=sum(etaI[m,n]*C[a][m][b]*C[b][n][a] for m in range(4) for n in range(4) for a in range(4) for b in range(4))
    T5=sum(P[a]*V[a] for a in range(4))
    return [sp.expand(x) for x in (T1,T2,T3,T4,T5)]

ksub={k[0]:w,k[1]:0,k[2]:0,k[3]:kap}

def Lagrangian(E, cvec):
    T=invs(Cconn(E))
    EH  = sp.expand(T[3]-T[4])                 # T4 - T5  (linearized-EH GammaGamma)
    Int = sp.expand(sum(cvec[i]*T[i] for i in range(5)))
    return sp.expand(sp.Rational(1,2)*EH + lam*Int), sp.expand(sp.Rational(1,2)*EH), Int

def pol_cross():
    E=sp.zeros(4,4); E[1,2]=h; E[2,1]=h; return E
def pol_plus():
    E=sp.zeros(4,4); E[1,1]=h; E[2,2]=-h; return E

# ghost-free-tuned interaction coefficients
cvec=[-u0, -u1/2, -u1/2, u0, u1]

# sanity: transversality of the chosen polarizations  (k^m eps_mn = eta^{mp} k_p eps_mn)
def check_transverse(E, name):
    res=[sp.expand((sum(etaI[m,p]*k[p]*E[m,n] for m in range(4) for p in range(4))).subs(ksub)) for n in range(4)]
    tr=sp.expand(sum(etaI[m,n]*E[m,n] for m in range(4) for n in range(4)))
    print(f"  {name}: k^m eps_mn =", res, "  trace eta^mn eps_mn =", tr)

print("="*95); print("TRANSVERSALITY / TRACELESS CHECK (k along z)"); print("="*95)
check_transverse(pol_cross(),"CROSS eps_xy")
check_transverse(pol_plus(), "PLUS  eps_xx-eps_yy")

results={}
for name, E in [("CROSS", pol_cross()), ("PLUS", pol_plus())]:
    Ltot, Kin, Intp = Lagrangian(E, cvec)
    Ltot_g = sp.expand(Ltot.subs({u0:1,u1:0}).subs(ksub))   # a!=0 direction
    Kin_g  = sp.expand(Kin.subs(ksub))                       # pure-EH calibration (no cvec dependence)
    Int_g  = sp.expand(Intp.subs({u0:1,u1:0}).subs(ksub))
    # each is c(w,kap)*h^2 ; strip h^2
    f_tot = sp.simplify(Ltot_g/h**2)
    f_kin = sp.simplify(Kin_g/h**2)
    f_int = sp.simplify(Int_g/h**2)
    print("\n"+"="*95); print(f"TT POLARIZATION: {name}   (a!=0 direction u0=1,u1=0)"); print("="*95)
    print("  pure-EH kinetic form   f_kin(w,kap) =", f_kin, "   [ (1/2)(T4-T5) on this TT mode ]")
    print("  interaction form       f_int(w,kap) =", f_int, "   [ Int = T4-T1 on this direction ]")
    print("  TOTAL quadratic form   f_tot(w,kap) =", f_tot)
    # coefficients of w^2 and kap^2
    Aw  = sp.expand(f_tot).coeff(w,2)
    Bk  = sp.expand(f_tot).coeff(kap,2)
    Aw_k= sp.expand(f_kin).coeff(w,2)
    Bk_k= sp.expand(f_kin).coeff(kap,2)
    print(f"  --- pure EH:  coeff w^2 = {Aw_k}, coeff kap^2 = {Bk_k}  => f_kin = {sp.factor(f_kin)}")
    print(f"  --- TOTAL :   coeff w^2 = {Aw},  coeff kap^2 = {Bk}")
    # dispersion relation f_tot = 0  ->  w^2/kap^2
    disp = sp.solve(sp.Eq(f_tot,0), w**2)
    # solve for w^2 in terms of kap^2 and lam
    wsol = sp.solve(sp.Eq(sp.expand(f_tot),0), w)
    # cT^2 = w^2/kap^2 on-shell (physical definition)
    cT2_phys = sp.simplify(-Bk/Aw)      # from A w^2 + B kap^2 = 0 => w^2 = -(B/A)kap^2
    # cT^2 by task's literal wording: coeff(kap^2)/coeff(w^2)
    cT2_ratio = sp.simplify(Bk/Aw)
    print(f"  DISPERSION: f_tot=0  =>  w^2 = {sp.simplify(-Bk/Aw)} * kap^2")
    print(f"  c_T^2 (physical w^2/kap^2 on-shell) = -B/A = {cT2_phys}")
    print(f"  c_T^2 (literal coeff kap^2 / coeff w^2 = B/A) = {cT2_ratio}")
    # health: sign of the total time-kinetic term relative to pure EH
    ratio_kin = sp.simplify(Aw/Aw_k)
    print(f"  HEALTH: coeff(w^2)_total / coeff(w^2)_pureEH = {ratio_kin}  (>0 => same sign as healthy EH)")
    results[name]=dict(Aw=Aw,Bk=Bk,Aw_k=Aw_k,Bk_k=Bk_k,cT2=cT2_phys,ratio_kin=ratio_kin,f_tot=f_tot,f_int=f_int,f_kin=f_kin)

# ---------------- quantitative c_T shift vs GW170817 ----------------
print("\n"+"="*95); print("QUANTITATIVE c_T SHIFT (a!=0 direction)"); print("="*95)
r=results["CROSS"]
cT2=sp.simplify(r["cT2"])
print("  c_T^2(lam) =", cT2)
dev=sp.simplify(cT2-1)
print("  c_T^2 - 1  =", dev, "  (0 => exactly luminal for ALL lam)")
series=sp.series(cT2, lam, 0, 2)
print("  small-lam expansion c_T^2 =", series)
# numeric: lam ~ a0^2 in natural (c=1) units. a0 = cH_Lambda/Z ~ 9.36e-11 m/s^2.
# In geometric units the dimensionless coupling of a 2-derivative correction relative to the EH k^2
# term is (a0^2 * L^2)/c^4-type; the RELEVANT dimensionless number is coeff_int/coeff_EH * (a0-scale)^2.
# Here we simply report the *fractional* shift as an EXACT function of lam and whether it is identically 0.
frac = sp.simplify((cT2-1))
print("  fractional shift (c_T^2-1) as exact function of lam:", frac)
if frac==0:
    print("  => c_T = 1 EXACTLY, independent of lam (a0). No GW170817 tension. PASS on speed.")
else:
    # linear coefficient in lam
    lin=sp.simplify(sp.diff(cT2,lam).subs(lam,0))
    print("  d(c_T^2)/dlam at lam=0 =", lin)
    print("  => c_T shift is O(lam)~O(a0^2); evaluate numerically below.")

print("\n"+"="*95); print("VERDICT INPUTS"); print("="*95)
print("  CROSS: coeff(w^2)_total/coeff(w^2)_EH =", sp.simplify(results['CROSS']['ratio_kin']),
      "  c_T^2 =", sp.simplify(results['CROSS']['cT2']))
print("  PLUS : coeff(w^2)_total/coeff(w^2)_EH =", sp.simplify(results['PLUS']['ratio_kin']),
      "  c_T^2 =", sp.simplify(results['PLUS']['cT2']))
print("  agree across CROSS/PLUS:", sp.simplify(results['CROSS']['cT2']-results['PLUS']['cT2'])==0)
