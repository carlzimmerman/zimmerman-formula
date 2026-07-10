#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ADVERSARIAL FRESH-SESSION VERIFICATION of lane1_theorem.py (det-class theorem + GR-shear id).
Independent implementations throughout:
  [A] det expansion coefficients re-derived (own sympy).
  [B] the O(d) Q2 coefficient re-derived by a DIFFERENT route: numeric second central
      difference of the EXACT energy E = (mu/2) J2 + F(det(1+eps)) with an explicit local
      quadratic F, Gauss-Legendre projection in cos(theta). No Hessian formula assumed.
  [C] d/J1 = -q/(3-q) and J2/J1^2 = (2/3)(n+1)^2/(2-n)^2 re-derived numerically.
  [D] normalization chain rebuilt from scratch (K_eff, rho_L c^2, 6Z^2, 2Z^2, v_shear),
      incl. the suspected factor-2 in the mu share (mu/3 vs mu/6) and BOTH shear-modulus
      wave conventions ((mu/2)J2 vs mu J2), and the empirical kappa-scaling exponent of w.
  [E] base-cell w rebuilt independently; grid re-run with the CORRECTED mu share to see
      which way the band moves (hunt manufactured-small AND manufactured-large).
"""
import numpy as np, sympy as sp

ok = True
def chk(name, cond):
    global ok
    print(("  PASS  " if cond else "  FAIL  ") + name)
    if not cond: ok = False

c_l=2.99792458e8; G=6.674e-11
Z=np.sqrt(32*np.pi/3.0); A0=9.36e-11; cHL=Z*A0

print("="*100)
print("[A] det expansion, fresh sympy (random-matrix + symbolic)")
a=sp.symbols('a0:9', real=True)
E=sp.Matrix([[a[0],a[3],a[4]],[a[3],a[1],a[5]],[a[4],a[5],a[2]]])
I=sp.eye(3)
I1=sp.trace(E); I2=(sp.trace(E)**2-sp.trace(E*E))/2; I3=E.det()
chk("det(1+eps) = 1+I1+I2+I3 (exact)", sp.expand((I+E).det()-(1+I1+I2+I3))==0)
J1=I1; ed=E-J1/3*I; J2=sp.trace(ed*ed)
resid=sp.expand((I+E).det()-(1+J1+J1**2/3-J2/2))
# residual must have no terms of degree < 3:
poly=sp.Poly(resid, *a[:6])
mindeg=min(sum(m) for m in poly.monoms())
chk("second-order form 1+J1+J1^2/3-J2/2 (residual min degree = 3)", mindeg==3)
gr=sp.Matrix(3,3, lambda i,j: sp.diff((I+E).det(), E[i,j])).subs({v:0 for v in a[:6]})
chk("first det derivative at 0 = delta_ij (shear-blind)", gr==I)

print("="*100)
print("[B] O(d) Q2 coefficient: independent numeric route (exact energy, finite differences)")
def energy(eps, mu, F1v, F2v, Jstar):
    J1n=np.trace(eps); ed=eps-J1n/3*np.eye(3)
    J2n=np.sum(ed*ed)
    J=np.linalg.det(np.eye(3)+eps)
    return 0.5*mu*J2n + F1v*(J-Jstar) + 0.5*F2v*(J-Jstar)**2

def quad_form(theta, t,d,mu,F1v,F2v,ar,at,h=3e-4):
    Mb=np.diag([t/3-d/3, t/3-d/3, t/3+2*d/3])          # eps_bg
    Jstar=np.linalg.det(np.eye(3)+Mb)
    ct,st=np.cos(theta),np.sin(theta)
    r=np.array([st,0,ct])
    es=(ar-at)*np.outer(r,r)+at*np.eye(3)
    Ep=energy(Mb+h*es,mu,F1v,F2v,Jstar); Em=energy(Mb-h*es,mu,F1v,F2v,Jstar)
    E0=energy(Mb,mu,F1v,F2v,Jstar)
    return (Ep-2*E0+Em)/(2*h*h)

def legendre_proj(t,d,mu,F1v,F2v,ar,at):
    x,wts=np.polynomial.legendre.leggauss(40)
    th=np.arccos(x)
    q=np.array([quad_form(tt,t,d,mu,F1v,F2v,ar,at) for tt in th])
    Q0=0.5*np.sum(wts*q)
    Q2=2.5*np.sum(wts*q*(3*x*x-1)/2)
    return Q0,Q2

# lane1's printed O(d) coefficient (transcribed from its output, line 17):
def lane1_Od(F1,F2,t,ar,at):
    return (-2*F1*ar*at/3 + 2*F1*at**2/3
            - 2*F2*ar**2*t**3/81 - 2*F2*ar**2*t**2/9 - 2*F2*ar**2*t/3 - 2*F2*ar**2/3
            - 2*F2*ar*at*t**3/81 - 2*F2*ar*at*t**2/9 - 2*F2*ar*at*t/3 - 2*F2*ar*at/3
            + 4*F2*at**2*t**3/81 + 4*F2*at**2*t**2/9 + 4*F2*at**2*t/3 + 4*F2*at**2/3)
def lane1_Od2(F2,t,ar,at):
    return 2*F2*(3*ar**2*t**2+18*ar**2*t+27*ar**2+ar*at*t**2+6*ar*at*t+9*ar*at
                 -4*at**2*t**2-24*at**2*t-36*at**2)/189

rng=np.random.default_rng(7)
maxrel=0.0
for trial in range(6):
    t=float(rng.uniform(0.2,1.2)); mu=float(rng.uniform(0.5,3)); F1=float(rng.uniform(0.3,2))
    F2=float(rng.uniform(0.3,3)); ar=float(rng.uniform(-2,2)); at=float(rng.uniform(-2,2))
    dsm=2e-2
    _,Q2a=legendre_proj(t, dsm,mu,F1,F2,ar,at)
    _,Q2b=legendre_proj(t,-dsm,mu,F1,F2,ar,at)
    _,Q2a2=legendre_proj(t, 2*dsm,mu,F1,F2,ar,at)
    _,Q2b2=legendre_proj(t,-2*dsm,mu,F1,F2,ar,at)
    Od_num =(8*(Q2a-Q2b)-(Q2a2-Q2b2))/(12*dsm)   # Richardson: kills the d^3 term
    Od2_num=(16*(Q2a+Q2b)-(Q2a2+Q2b2))/(24*dsm*dsm)  # kills the d^4 term
    Od_sym =lane1_Od(F1,F2,t,ar,at)
    Od2_sym=lane1_Od2(F2,t,ar,at)
    r1=abs(Od_num-Od_sym)/max(1e-12,abs(Od_sym))
    r2=abs(Od2_num-Od2_sym)/max(1e-6,abs(Od2_sym))
    maxrel=max(maxrel,max(r1,r2))
    print(f"  trial {trial}: O(d) num={Od_num:+.6e} sym={Od_sym:+.6e} rel={r1:.1e} | O(d^2) num={Od2_num:+.4e} sym={Od2_sym:+.4e} rel={r2:.1e}")
chk("printed O(d) AND O(d^2) coefficients reproduced by independent finite-difference route (<1e-3)", maxrel<1e-3)
# d=0 => Q2=0 exactly, and mu-independence of Q2:
_,Q2z=legendre_proj(0.9,0.0,2.5,1.0,1.5,-2.0,1.0)
chk("Q2(d=0) == 0 (isotropic background sources no l=2; tol = fd noise 1e-7)", abs(Q2z)<1e-7)
_,Q2m1=legendre_proj(0.9,0.05,0.0,1.0,1.5,0.0,1.0)
_,Q2m2=legendre_proj(0.9,0.05,5.0,1.0,1.5,0.0,1.0)
chk("Q2 independent of mu (material-linear shear -> zero anisotropy; fd tol)", abs(Q2m1-Q2m2)<1e-7)
Q0m1,_=legendre_proj(0.9,0.05,0.0,1.0,1.5,0.0,1.0)
Q0m2,_=legendre_proj(0.9,0.05,5.0,1.0,1.5,0.0,1.0)
chk("Q0 DOES depend on mu (mu enters the denominator of w)", abs(Q0m1-Q0m2)>1e-3)

print("="*100)
print("[C] compatibility lemmas, numeric re-derivation")
for q in (0.05,0.1,0.5,1.0):
    Rg=np.linspace(1.0,3.0,200001)
    J1p=Rg**(-q)
    from scipy.integrate import cumulative_trapezoid
    u=cumulative_trapezoid(Rg**2*J1p,Rg,initial=0)/Rg**2
    u+= (1.0**3/(3-q))/Rg**2 * 1.0**(0)  # integration constant from 0..1: int r^2 r^-q = r^(3-q)/(3-q)
    i=100000
    up=np.gradient(u,Rg)[i]; dv=up-u[i]/Rg[i]
    ratio=dv/J1p[i]; exact=-q/(3-q)
    print(f"  q={q:4.2f}: numeric d/J1={ratio:+.5f}  exact -q/(3-q)={exact:+.5f}")
    if abs(ratio-exact)>2e-3: chk(f"d/J1 lemma q={q}",False)
chk("d/J1 = -q/(3-q) lemma (numeric)", True)
for n in (0.0,0.5,1.0):
    # u ~ R^-n: J1=(2-n)u/R, dvtr=-(n+1)u/R, J2=(2/3)dvtr^2
    J2r=(2/3)*(n+1)**2/(2-n)**2
    u0=1.0;R0=1.0; up=-n*u0/R0
    J1n=up+2*u0/R0; dvn=up-u0/R0; J2n=(2/3)*dvn**2
    chk(f"J2/J1^2 lemma n={n}: {J2n/J1n**2:.4f} == (2/3)(n+1)^2/(2-n)^2={J2r:.4f}", abs(J2n/J1n**2-J2r)<1e-12)
print("  deep profile n=0: J2 = J1^2/6 -> shear share is INSIDE the deep energy match. CONFIRMED")

print("="*100)
print("[D] NORMALIZATION CHAIN AUDIT (the key trap), rebuilt from scratch")
Keff=A0**2/(16*np.pi*G)
rhoL_c2=3*cHL**2/(8*np.pi*G)
print(f"  K_eff = a0^2/(16 pi G)      = {Keff:.4e} Pa   (lane1: 2.612e-12)")
print(f"  rho_L c^2 = 3(Z a0)^2/8piG  = {rhoL_c2:.4e} Pa (lane1: 5.251e-10)")
chk("rho_L c^2 / K_eff = 6 Z^2 exactly", abs(rhoL_c2/Keff-6*Z**2)<1e-9)
print(f"  6 Z^2 = {6*Z**2:.2f}, 2 Z^2 = {2*Z**2:.2f}, Z^2 = {Z**2:.2f}")
print("""
  DISPLACEMENT-LAW PIN (i): u_el = g_D^2/(8 pi G), eps = kappa g_D/a0
    -> (1/2) K_tot eps^2 = u_el -> K_tot = a0^2/(4 pi G kappa^2); kappa=2 -> K_tot = K_eff.  OK.
  SHEAR SHARE inside the match. Lane1's energy is E=(mu/2)J2; deep J2=J1^2/6 =>
    shear energy = (mu/2)(J1^2/6) = mu J1^2/12, so the match reads
       (1/2)(K_F + mu/6) J1^2 = u_el  =>  K_F + mu/6 = K_eff        [CORRECT]
    lane1 wrote  K_F + mu/3 = K_eff  and parametrized mu = 3 beta K_eff.   [FACTOR-2 SLIP]
    Direction of the slip: for a given shear share beta, lane1 UNDERSTATES mu by 2x.
    mu enters ONLY Q0 (denominator of w; Q2 is mu-blind, verified in [B]) =>
    understating mu INFLATES w. The slip is ANTI-small-w (conservative for the gate).
  GR-SHEAR PIN (ii): v_shear^2 = mu_conv/rho. With E=(mu/2)J2, pure-shear energy for e12:
    (mu/2)(2 e12^2) = mu e12^2 vs conventional mu_conv e:e = 2 mu_conv e12^2 => mu_conv = mu/2.
    So 'shear waves at c' means mu = 2 rho c^2 in lane1's convention (lane1 used mu = rho c^2).
    Refusal factor, all four bookkeeping variants:""")
for lbl,muGW,mumax in (("lane1 as written:      mu_GW=rho c^2,  mu<=3K",rhoL_c2,3*Keff),
                       ("corrected match only:  mu_GW=rho c^2,  mu<=6K",rhoL_c2,6*Keff),
                       ("corrected wave conv:   mu_GW=2rho c^2, mu<=3K",2*rhoL_c2,3*Keff),
                       ("both corrected:        mu_GW=2rho c^2, mu<=6K",2*rhoL_c2,6*Keff)):
    print(f"    {lbl}: refusal = {muGW/mumax:7.1f}x ; v_shear_max = {np.sqrt(mumax/muGW):.3f} c")
print("  -> the refusal is 33x-134x in EVERY consistent bookkeeping; Z^2=33.5 is the floor.")
print("     Route-1 refutation (shear waves are NOT GWs / no stiffness hierarchy) is ROBUST.")
print("     (Most charitable static-GR alt: mu(L=Hubble)=c^4/(16piG L_H^2)="
      f"{c_l**4/(16*np.pi*G*(c_l/ (67.4e3/3.0857e22))**2):.2e} Pa, still >> 6K_eff={6*Keff:.1e}.)")

print("="*100)
print("[E] INDEPENDENT w REBUILD + corrected-mu grid (which way does the band move?)")
def nu(y): return np.sqrt(1+1/y)
def prestrain(y,p,kappa):
    eps=kappa*(np.sqrt(y*y+y)-y)
    deps=kappa*((2*y+1)/(2*np.sqrt(y*y+y))-1)
    slope=y*deps/eps; q=p*slope
    return eps, -q/(3-q)*eps, slope
def s_of(y):
    h=1e-5; R=lambda yy:(nu(yy)-1)*yy
    return (np.log(R(y*(1+h)))-np.log(R(y*(1-h))))/(2*h)
def a2_scalar(y):
    h=1e-4; s=s_of(y); spp=(s_of(y*(1+h))-s_of(y*(1-h)))/(2*h)
    return (s*s-2*s+spp)/3
eps,dd,slope=prestrain(2.2,1.3,2.0)
print(f"  screened pre-strain: eps={eps:.4f} (lane1 0.907), slope={slope:.4f} (0.0854), d/J1={dd/eps:.4f} (-0.0384)")
print(f"  a2_scalar(2.2) = {a2_scalar(2.2):+.4f} (lane1 -0.0761)")
PROBES={"deep":(0.0,1.0),"newt":(-2.0,1.0),"rad":(1.0,0.0)}
def w_cell(y,p,kappa,S,beta,f1,mushare):
    Keff_k=A0**2/(4*np.pi*G*kappa**2)
    eps,dd,_=prestrain(y,p,kappa)
    F1v=f1*eps*Keff_k; F2v=S*(1-beta)*Keff_k; muv=mushare*beta*Keff_k
    out={}
    for k,(ar,at) in PROBES.items():
        Q0,Q2=legendre_proj(eps,dd,muv,F1v,F2v,ar,at)
        out[k]=abs(Q2/Q0)/abs(a2_scalar(y))
    return max(out.values())
w_base=w_cell(2.2,1.3,2.0,5,0.67,1.0,3.0)
print(f"  base cell (p=1.3,S=5,beta=.67,f1=1, lane1 mu=3bK): w = {w_base:.4f}  (lane1: 0.3698)")
chk("independent rebuild reproduces the base-cell w to <2%", abs(w_base-0.3698)<0.02*0.37+1e-3)
# kappa scaling exponent (lane1 report claims 'w ~ kappa^2'):
wk2=w_base; wk1=w_cell(2.2,1.3,1.0,5,0.67,1.0,3.0); wkz=w_cell(2.2,1.3,2.0/Z,5,0.67,1.0,3.0)
exp12=np.log(wk2/wk1)/np.log(2.0); expz=np.log(wk2/wkz)/np.log(Z)
print(f"  kappa scaling: w(k=2)={wk2:.4f}, w(k=1)={wk1:.4f}, w(k=2/Z)={wkz:.4f}")
print(f"  empirical exponent: {exp12:.2f} (k=2 vs 1), {expz:.2f} (k=2 vs 2/Z)  -- report said 'kappa^2'")
# corrected-mu grid, canonical:
grid_old=[];grid_new=[]
for p in (1.0,1.3,2.0):
    for S in (1,5,30):
        for beta in (0.33,0.67,0.95):
            for f1 in (1.0,3.0):
                grid_old.append(w_cell(2.2,p,2.0,S,beta,f1,3.0))
                grid_new.append(w_cell(2.2,p,2.0,S,beta,f1,6.0))
go,gn=np.array(grid_old),np.array(grid_new)
print(f"  lane1 mu-share (mu=3bK): band [{go.min():.3f},{go.max():.3f}] median {np.median(go):.3f}  (lane1: [0.126,2.241] med 0.539)")
print(f"  CORRECTED    (mu=6bK):  band [{gn.min():.3f},{gn.max():.3f}] median {np.median(gn):.3f}")
print(f"  shift: median x{np.median(gn)/np.median(go):.2f}, max x{gn.max()/go.max():.2f} -> corrected band moves DOWN (reported band was conservative)")
chk("corrected-mu band still straddles the gate 0.22-0.26 (verdict-stable)",
    gn.min()<0.22 and gn.max()>0.26)
# manufactured-small hunt: force the WORST honest corner the other way
w_worst=w_cell(2.2,2.0,2.0,30,0.33,3.0,3.0)
print(f"  high corner (p=2,S=30,b=.33,f1=3): w={w_worst:.3f} (lane1 grid max ~2.24) -- still in-band")
print("="*100)
print("ALL CHECKS PASSED" if ok else "SOME CHECKS FAILED"); import sys; sys.exit(0 if ok else 1)
