"""b03: Einstein-Gauss-Bonnet / Lovelock horizon equation.
Action (1/16 pi G) int sqrt(-g)[R - 2 Lb + alpha_b L_GB];  alt = (D-3)(D-4) alpha_b ; psi=(1-f)/r^2.
(E1) explicit D=5 and D=6 field equations: G^t_t + Lb + alpha_b H^t_t = -(D-2)/(2 r^{D-2}) d/dr[ r^{D-1}(psi + alt psi^2) ] + Lb  for generic f  (so Boulware-Deser: psi+alt psi^2 = mu/r^{D-1}+lam, lam=2Lb/((D-1)(D-2)));
     in D=4 H_mn == 0 identically (control: why the 4D theory needs the Glavan-Lin D->4 rescaling alpha_b -> alpha/(D-4), alt -> alpha).
(E2) horizon equation (any D):  (2 kappa r_h + 2)(1+2a) = (D-1)(1 + a - lam r_h^2),  a = alt/r_h^2,  kappa = f'(r_h)/2.  Generalised Lovelock: P'(psi_h)(2 kappa r_h+2) = (D-1) r_h^2 (P(psi_h)-lam) ... (checked by sympy).
(E3) T: kappa r_h=1/2 with Lb r_h^2 = 8 pi (D=4 GL): a = -Lb r_h^2/3 = -8 pi/3 (alt <0, alt = -8 pi r_h^2/3);  with Lambda_e: a=-(8pi/3)/(1+(8pi/3)^2).  Contains pi only because T was imposed; alt dimensionful.
(E4) first law: S=int dM/T with T=kappa/2pi, M=(D-2) Omega mu/(16 pi), equals Wald S=(Omega r^{D-2}/4)(1+2(D-2) alt/((D-4) r^2)) (D=5,6); D=4 limit: S = pi r^2 + 4 pi alt ln r (log, not Wald 'A/4(1+alpha...)').
(E5) G_eff at the horizon = G/(1+2a).
"""
import sympy as sp, sys, itertools
ok=[]
def chk(n,c): ok.append(bool(c)); print(("PASS " if c else "FAIL ")+n)
r=sp.symbols('r',positive=True)
def build(D,fexpr):
    """static spherical D-dim metric with unit S^{D-2}; returns G^t_t, H^t_t (Lovelock tensor) as expressions"""
    ang=sp.symbols('x1:%d'%(D-1)); X=[sp.Symbol('t'),r]+list(ang)
    diag=[-fexpr,1/fexpr,r**2]
    s=1
    for i in range(1,D-2):
        s=s*sp.sin(ang[i-1])**2; diag.append(r**2*s)
    g=sp.diag(*diag); gi=sp.diag(*[1/d for d in diag])
    n=D
    Gam=[[[sp.simplify(sum(gi[a,d]*(sp.diff(g[d,b],X[c])+sp.diff(g[d,c],X[b])-sp.diff(g[b,c],X[d])) for d in range(n))/2) for c in range(n)] for b in range(n)] for a in range(n)]
    def Rie(a,b,c,d): # R^a_{bcd}
        return sp.diff(Gam[a][b][d],X[c])-sp.diff(Gam[a][b][c],X[d])+sum(Gam[a][c][e]*Gam[e][b][d]-Gam[a][d][e]*Gam[e][b][c] for e in range(n))
    Rm={}
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(c+1,n):
                    v=sp.simplify(Rie(a,b,c,d)); Rm[(a,b,c,d)]=v; Rm[(a,b,d,c)]=-v
                Rm[(a,b,c,c)]=0
    # all-lower, diagonal metric
    def Rl(a,b,c,d): return g[a,a]*Rm[(a,b,c,d)]
    Ric=sp.zeros(n,n)
    for b in range(n):
        for d in range(n):
            Ric[b,d]=sp.simplify(sum(Rm[(a,b,a,d)] for a in range(n)))
    Rs=sp.simplify(sum(gi[i,i]*Ric[i,i] for i in range(n)))
    Gt=sp.simplify(gi[0,0]*Ric[0,0]-Rs/2)
    # GB tensor H_{mu nu} for mu=nu=0 (diagonal metric -> only diag components needed)
    Ric2=sum(gi[i,i]*gi[j,j]*Ric[i,j]**2 for i in range(n) for j in range(n))
    Riem2=sum(gi[a,a]*gi[b,b]*gi[c,c]*gi[d,d]*Rl(a,b,c,d)**2 for a in range(n) for b in range(n) for c in range(n) for d in range(n) if (a,b,c,d) in Rm or True and a!=b and c!=d) if False else None
    Riem2=0
    for a in range(n):
        for b in range(n):
            if a==b: continue
            for c in range(n):
                for d in range(n):
                    if c==d: continue
                    Riem2+=gi[a,a]*gi[b,b]*gi[c,c]*gi[d,d]*Rl(a,b,c,d)**2
    LGB=sp.simplify(Rs**2-4*Ric2+Riem2)
    mu=0
    t1=Rs*Ric[mu,mu]
    t2=-2*sum(Ric[mu,a]*gi[a,a]*Ric[a,mu] for a in range(n))
    t3=-2*sum(Rl(mu,a,mu,b)*gi[a,a]*gi[b,b]*Ric[a,b] for a in range(n) for b in range(n) if a==b)
    t4=sum(Rl(mu,a,b,c)*Rl(mu,a,b,c)*gi[a,a]*gi[b,b]*gi[c,c] for a in range(n) for b in range(n) for c in range(n) if a!=mu and b!=c and True) 
    Htt=2*(t1+t2+t3+t4)-g[0,0]*LGB/2
    Ht=sp.simplify(gi[0,0]*Htt)
    return Gt,Ht
fF=sp.Function('f')(r)
for D in (4,5,6):
    Gt,Ht=build(D,fF)
    psi=(1-fF)/r**2
    ab=sp.symbols('alpha_b'); Lb=sp.symbols('Lambda_b')
    alt=(D-3)*(D-4)*ab
    claimG=-(D-2)/(2*r**(D-2))*sp.diff(r**(D-1)*psi,r)
    claimH=-(D-2)/(2*r**(D-2))*sp.diff(r**(D-1)*(D-3)*(D-4)*psi**2,r)   # alpha_b * H^t_t
    chk("E1 D=%d: G^t_t = -(D-2)/(2 r^(D-2)) d/dr[r^(D-1) psi]"%D, sp.simplify(Gt-claimG)==0)
    if D==4:
        chk("E1 D=4 control: H^t_t == 0 identically (GB topological)", sp.simplify(Ht)==0)
    else:
        chk("E1 D=%d: H^t_t = -(D-2)(D-3)(D-4)/(2 r^(D-2)) d/dr[r^(D-1) psi^2]"%D, sp.simplify(Ht-claimH)==0)
        chk("E1 D=%d mutation: coefficient (D-3)(D-4) replaced by (D-3)(D-3) is wrong"%D, sp.simplify(Ht-(-(D-2)/(2*r**(D-2))*sp.diff(r**(D-1)*(D-3)*(D-3)*psi**2,r)))!=0)
# E2 horizon equation
def horizon(D):
    a_,lam,rh,k=sp.symbols('a lam r_h kappa')
    alt_=sp.symbols('alt'); mu=sp.symbols('mu')
    psi=lambda f: (1-f)/r**2
    return None
D=sp.symbols('D'); rh,k,lam,alt=sp.symbols('r_h kappa lam alt',positive=True)
fs=sp.Function('f')(r); mu=sp.symbols('mu')
# implicit: P(psi)=mu/r^(D-1)+lam. differentiate: P'(psi) psi' = -(D-1) mu / r^D ; at horizon psi=1/rh^2, psi'=-f'/rh^2-2/rh^3 (f=0)
psih=1/rh**2; psip=-(2*k)/rh**2-2/rh**3
P=lambda s: s+alt*s**2; Pp=lambda s: 1+2*alt*s
mu_h=rh**(D-1)*(P(psih)-lam)
eq=sp.simplify(Pp(psih)*psip+(D-1)*mu_h/rh**D)
aa=alt/rh**2
claim=(2*k*rh+2)*(1+2*aa)-(D-1)*(1+aa-lam*rh**2)
chk("E2 horizon equation (2 kappa r_h+2)(1+2a)=(D-1)(1+a-lam r_h^2) from the Boulware-Deser law", sp.simplify(eq*rh**3+claim)==0)
chk("E2 GR control a=0, D=4: 2 kappa r_h = 1 - Lambda r_h^2 (lam=Lambda/3)", sp.simplify(sp.solve(claim.subs({alt:0,D:4}),k)[0]*2*rh-(1-3*lam*rh**2))==0)
# E2b generalised Lovelock polynomial with cubic term
b3=sp.symbols('b3')
P3=lambda s: s+alt*s**2+b3*s**3; P3p=lambda s: 1+2*alt*s+3*b3*s**2
mu3=rh**(D-1)*(P3(psih)-lam)
eq3=sp.simplify(P3p(psih)*psip+(D-1)*mu3/rh**D)
claim3=(2*k*rh+2)*P3p(psih)-(D-1)*rh**2*(P3(psih)-lam)
chk("E2 generalised Lovelock: P'(psi_h)(2 kappa r_h+2) = (D-1) r_h^2 (P(psi_h)-lam)", sp.simplify(eq3*rh**3+claim3)==0)
# E3 point T, D=4
Lbs=sp.symbols('Lambda_b',positive=True); a=sp.symbols('a')
rel4=((2*k*rh+2)*(1+2*a)-3*(1+a-(Lbs/3)*rh**2)).subs(k,1/(2*rh))
asol=sp.solve(rel4.subs(Lbs,8*sp.pi/rh**2),a)
chk("E3 D=4 GL: T with Lambda_b r_h^2=8 pi  requires a = alt/r_h^2 = -8 pi/3 = %.4f"%float(-8*sp.pi/3), asol==[-8*sp.pi/3])
# dimensional: alt = a r_h^2 = a/(4 a0^2)
He=sp.symbols('He2',positive=True)  # H^2 r_h^2
# Lambda_e = 3 H^2 with H^2 + alt H^4 = Lb/3
Lb_of_Le=lambda Le: Le*(1+a*Le*rh**2/3*(1/rh**2*rh**2))  # with Le in units; use x=Le r_h^2
x=sp.symbols('x')
Lb_x=x*(1+a*x/3)   # Lb r_h^2 as function of x=Le r_h^2 and a=alt/r_h^2
rel4x=(2*(sp.Rational(1,2))+2)*(1+2*a)-3*(1+a-Lb_x/3)
asol2=sp.solve(rel4x.subs(x,8*sp.pi),a)
chk("E3 Lambda_e reading: a = -(8pi/3)/(1+(8pi/3)^2) = %.5f"%float(-(8*sp.pi/3)/(1+(8*sp.pi/3)**2)), len(asol2)==1 and sp.simplify(asol2[0]+(8*sp.pi/3)/(1+(8*sp.pi/3)**2))==0)
# E3b regularity: f real and monotone? D=4: f = 1 + r^2/(2 alt)(1 - sqrt(1+4 alt(2M/r^3+Lb/3)))
import mpmath as mp
def f4(rr,M,alt_,Lb_,sg): return 1+rr**2/(2*alt_)*(1-sg*mp.sqrt(1+4*alt_*(2*M/rr**3+Lb_/3)))
rh_=mp.mpf(1)
def Tcheck(a_,Lb_):
    Mh=(rh_**3)*(1/rh_**2+a_*rh_**2/rh_**4-Lb_/3)/2
    res={}
    for sg in (+1,-1):
        fv=f4(rh_,Mh,a_*rh_**2,Lb_,sg); kap=mp.diff(lambda y:f4(y,Mh,a_*rh_**2,Lb_,sg),rh_)/2
        res[sg]=(fv,kap)
    return Mh,res
a1=-8*mp.pi/3; Mh,res=Tcheck(a1,8*mp.pi)
good=[sg for sg in res if abs(res[sg][0])<1e-12]
chk("E3b Lambda_b reading: f(r_h)=0 only on the branch sg=%s (sg=+1 is the GR-continuous root)"%good, good==[-1])
chk("E3b Lambda_b reading: kappa r_h = 1/2 on that branch (%.6f)"%res[-1][1], abs(res[-1][1]-0.5)<1e-9)
print("   branch factor 1+2a = %.4f <0: G_eff<0 at the horizon, and the solution is the NON-GR branch (no alt->0 limit)"%(1+2*a1))
a2=-(8*mp.pi/3)/(1+(8*mp.pi/3)**2); x_=8*mp.pi; Lb2=x_*(1+a2*x_/3)
Mh2,res2=Tcheck(a2,Lb2)
good2=[sg for sg in res2 if abs(res2[sg][0])<1e-12]
chk("E3b Lambda_e reading: horizon on branch %s, kappa r_h=%.6f"%(good2,res2[good2[0]][1]), len(good2)==1 and abs(res2[good2[0]][1]-0.5)<1e-9)
psiv=[(-1+sg*mp.sqrt(1+4*a2*Lb2/3))/(2*a2) for sg in (1,-1)]
print("   Lambda_e reading: vacuum roots H^2 r_h^2 = %s ; target Lambda_e r_h^2/3 = %.4f ; G_eff(vac)=1+2 a H^2 r_h^2 = %.4f"%([float(p) for p in psiv],8*mp.pi/3,1+2*a2*8*mp.pi/3))
chk("E3b Lambda_e reading: the vacuum with Lambda_e r_h^2=8 pi is the NON-GR root of the quadratic (1+2 alt H^2<0)", abs(psiv[1]-8*mp.pi/3)<1e-9 and 1+2*a2*8*mp.pi/3<0)
# mutation: wrong a must not hit kappa r_h=1/2
a_bad=-4*mp.pi; Mb,rb=Tcheck(a_bad,8*mp.pi)
chk("E3 mutation: a=-4 pi: a horizon exists but kappa r_h != 1/2", any(abs(rb[sg][0])<1e-9 for sg in rb) and all(abs(rb[sg][1]-0.5)>1e-3 for sg in rb if abs(rb[sg][0])<1e-9) )
# E3c single-branch consistency (Lambda_e reading): horizon branch = sign of 1+2a psi_h ; vacuum branch = sign of 1+2a psi_vac (psi in units 1/r_h^2)
hor_branch=1+2*a2; vac_branch=1+2*a2*(8*mp.pi/3)
chk("E3c Lambda_e reading: the unique solution has 1+2a=%.3f (>0, GR-continuous at the horizon) but 1+2a psi_vac=%.3f (<0) -> horizon and the Lambda_e=8pi vacuum sit on DIFFERENT roots: no single-branch solution realises T"%(hor_branch,vac_branch), hor_branch>0 and vac_branch<0)
# control: small coupling a=-0.01 with Lambda_e r^2=3 keeps both positive (same branch)
chk("E3c control: a=-0.01, psi_vac r^2=1: both branch factors positive", 1+2*(-0.01)>0 and 1+2*(-0.01)*1>0)
# E3d Lambda_b reading: where does the solution end? branch point 1+4 alt(2M/r^3+Lb/3)=0
rb_=mp.findroot(lambda y:1+4*a1*rh_**2*(2*Mh/y**3+8*mp.pi/3),(mp.mpf(1),mp.mpf(200)),solver="bisect",tol=1e-12,maxsteps=500)
chk("E3d Lambda_b reading: square-root branch point at r_b = %.4f r_h > r_h (solution exists on 0<r<r_b only, no asymptotic vacuum)"%rb_, rb_>1)

# E4 first law vs Wald in D=5,6 and D=4 log
rS=sp.symbols('r_s',positive=True)
for Dn in (5,6):
    lam_=sp.symbols('lam'); alt_=sp.symbols('alt')
    mu_r=rS**(Dn-1)*(1/rS**2+alt_/rS**4-lam_)
    # kappa from E2: 2 kappa r = (D-1)(1+a-lam r^2)/(1+2a)-2
    aa_=alt_/rS**2
    kap_=((Dn-1)*(1+aa_-lam_*rS**2)/(1+2*aa_)-2)/(2*rS)
    Om=sp.symbols('Omega')
    dS=(Dn-2)*Om/(16*sp.pi)*sp.diff(mu_r,rS)*2*sp.pi/kap_
    S_W=Om*rS**(Dn-2)/4*(1+2*(Dn-2)*alt_/((Dn-4)*rS**2))
    chk("E4 D=%d: dM/T (T=kappa/2pi, M=(D-2)Om mu/16pi) = dS_Wald/dr_h exactly"%Dn, sp.simplify(dS-sp.diff(S_W,rS))==0)
    chk("E4 D=%d mutation: Wald coefficient 2->3 breaks it"%Dn, sp.simplify(dS-sp.diff(Om*rS**(Dn-2)/4*(1+3*(Dn-2)*alt_/((Dn-4)*rS**2)),rS))!=0)
# D=4: first law with alt finite
alt_=sp.symbols('alt'); lam_=sp.symbols('lam')
mu4=rS**3*(1/rS**2+alt_/rS**4-lam_); aa_=alt_/rS**2
kap4=(3*(1+aa_-lam_*rS**2)/(1+2*aa_)-2)/(2*rS)
dS4=sp.simplify((2)*(4*sp.pi)/(16*sp.pi)*sp.diff(mu4,rS)*2*sp.pi/kap4)
dS4s=sp.simplify(dS4)
chk("E4 D=4 GL: dS/dr_h = 2 pi r_h + 4 pi alt/r_h for ALL lam  ( S = pi r^2 + 4 pi alt ln r )", sp.simplify(dS4s-(2*sp.pi*rS+4*sp.pi*alt_/rS))==0)
chk("E4 D=4 mutation: coefficient 4 -> 2 pi alt/r_h breaks", sp.simplify(dS4s-(2*sp.pi*rS+2*sp.pi*alt_/rS))!=0)
# Wald entropy at T: factor (1+4a) for 'S=A/4(1+4 alt/r^2)' naive Wald 2R_h with R_h=2/r^2: show it equals 1-Z^2 -- arithmetic only
Z2=32*sp.pi/3
chk("E5 'Wald factor 1+4a' at T equals 1 - 32 pi/3 = 1 - Z^2: pure arithmetic 4*(8 pi/3) (4=2*R_h r^2 from the sphere, 8pi imposed)", sp.simplify(1+4*(-8*sp.pi/3)-(1-Z2))==0)
# decoy: same pattern for any imposed Lambda r^2 = y
y=sp.symbols('y')
chk("E5 decoy: for any imposed Lambda_b r_h^2=y the same algebra gives 1+4a=1-4y/3 (no special role for 8 pi)", sp.simplify(1+4*(-y/3)-(1-4*y/3))==0)
chk("E5 G_eff at horizon = G/(1+2a): a=-8pi/3 -> G_eff/G = %.4f (negative: repulsive/ghostlike horizon coupling)"%float(1/(1-16*sp.pi/3)), 1/(1-16*sp.pi/3)<0)
print("\n%d/%d"%(sum(ok),len(ok))); sys.exit(0 if all(ok) else 1)
