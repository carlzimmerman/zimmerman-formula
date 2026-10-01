"""b02: f(R) and Rastall.
(F1) f(R) = R - 2 L + a R^2 + b R^3: constant-curvature branch R=R0 solves R f' = 2 f (4D trace eq) i.e. -R0+4L+b R0^3=0; SdS with Lambda_e=R0/4 solves the full field eqs
     F R_mn - f g_mn/2 = 0 (checked on the explicit SdS metric).  Hence the horizon relation is the GR one with Lambda_e (K2): T excluded. Lambda_e != Lambda_b once b != 0.
     G_eff = G/F(R0), Wald S = F(R0) A/4G (c_W = F).
(F2) general static f(R) (non-constant R): at a regular horizon the tt equation gives  F R^t_t - f/2 + (B'_h/2) F'_h = 0 with F'_h = F_RR R'_h the horizon value of a free
     radial derivative (global/regularity data, not a theory constant).  So the horizon equation acquires one free number F'_h.
(R1) Rastall G_mn + k l R g_mn = 8 pi T_mn with a vacuum fluid T_mn=-rho g_mn: Lambda_e = 8 pi rho/(1-4 k l): the vacuum energy is renormalised by a free dimensionless factor;
     vacuum Rastall (T=0) = GR + Lambda as integration constant (R=const).
"""
import sympy as sp, sys
ok=[]
def chk(n,c): ok.append(bool(c)); print(("PASS " if c else "FAIL ")+n)
r=sp.symbols('r',positive=True); t,th,ph=sp.symbols('t theta phi'); X=[t,r,th,ph]
M,Le,L,a,b=sp.symbols('M Lambda_e Lambda_b a b')
def geom(g):
    gi=g.inv()
    Gam=lambda i,j,k: sum(gi[i,d]*(sp.diff(g[d,j],X[k])+sp.diff(g[d,k],X[j])-sp.diff(g[j,k],X[d])) for d in range(4))/2
    def Ric(j,k):
        return sp.simplify(sum(sp.diff(Gam(i,j,k),X[i])-sp.diff(Gam(i,j,i),X[k])+sum(Gam(i,i,d)*Gam(d,j,k)-Gam(i,k,d)*Gam(d,j,i) for d in range(4)) for i in range(4)))
    Rm=sp.Matrix(4,4,lambda i,j:Ric(i,j)); Rs=sp.simplify(sum(gi[i,j]*Rm[i,j] for i in range(4) for j in range(4)))
    return gi,Gam,Rm,Rs
fS=1-2*M/r-Le*r**2/3
g=sp.diag(-fS,1/fS,r**2,r**2*sp.sin(th)**2)
gi,Gam,Rm,Rs=geom(g)
chk("F1 SdS Ricci scalar = 4 Lambda_e, R_mn = Lambda_e g_mn", sp.simplify(Rs-4*Le)==0 and sp.simplify(Rm-Le*g)==sp.zeros(4,4))
R=sp.symbols('R')
fR=R-2*L+a*R**2+b*R**3
trace=sp.expand(R*sp.diff(fR,R)-2*fR)
chk("F1 trace eq R f'-2f = -R+4 Lambda_b + b R^3", sp.expand(trace-(-R+4*L+b*R**3))==0)
R0=sp.symbols('R0')
F0=sp.diff(fR,R).subs(R,R0)
# full eq on SdS with Lambda_e=R0/4 : F R_mn - f g/2 = (F R0/4 - f/2) g = (R0 f'-2f)/4 g =0 on the branch
E=sp.simplify((F0*Rm-fR.subs(R,R0)*g/2).subs(Le,R0/4))
chk("F1 field eqs F R_mn - f g/2 vanish on SdS(Lambda_e=R0/4) iff trace eq holds", sp.simplify(E-((R0*F0-2*fR.subs(R,R0))/4)*g.subs(Le,R0/4))==sp.zeros(4,4))
# numeric branch: b=0.3,L=1 -> Lambda_e != Lambda_b
sols=[s for s in sp.Poly(-R+4*0.1+0.3*R**3,R).nroots() if abs(sp.im(s))<1e-12 and sp.re(s)>0]
chk("F1 with b=0.3, Lambda_b=0.1: Lambda_e=R0/4 differs from Lambda_b (%s)"%[float(sp.re(s)/4) for s in sols], any(abs(float(sp.re(s)/4)-0.1)>1e-3 for s in sols))
chk("F1 control: b=0 gives Lambda_e = Lambda_b (R0=4 Lambda_b) for any a", sp.simplify(trace.subs(b,0).subs(R,4*L))==0)
# horizon relation on that branch is K2
rh=sp.symbols('r_h',positive=True)
Ms=sp.solve(fS.subs(r,rh),M)[0]
chk("F1 kappa_f: 2 kappa r_h = 1 - Lambda_e r_h^2 (theory independent)", sp.simplify(2*(sp.diff(fS,r)/2).subs(M,Ms).subs(r,rh)*rh-(1-Le*rh**2))==0)
# F2 general static f(R): horizon tt eq, with free F'_h
A=sp.Function('N')(r); B=sp.Function('B')(r); Ff=sp.Function('F')(r); P=sp.Function('P')(r)
gg=sp.diag(-A**2*B,1/B,r**2,r**2*sp.sin(th)**2)
gi2,Gam2,Rm2,Rs2=geom(gg)
def hess(i,j): return sp.diff(Ff,X[i],X[j])-sum(Gam2(k,i,j)*sp.diff(Ff,X[k]) for k in range(4))
box=sp.simplify(sum(gi2[i,i]*hess(i,i) for i in range(4)))
Ett=sp.simplify(Ff*gi2[0,0]*Rm2[0,0]-P/2+box-gi2[0,0]*hess(0,0))
Err=sp.simplify(Ff*gi2[1,1]*Rm2[1,1]-P/2+box-gi2[1,1]*hess(1,1))
Ethth=sp.simplify(Ff*gi2[2,2]*Rm2[2,2]-P/2+box-gi2[2,2]*hess(2,2))
# near horizon: B=0 at r_h; impose B(rh)=0
Bh=sp.Symbol('Bp'); Fh=sp.Symbol('Fp')
tt_h=sp.simplify(Ett.subs(B,0) ) if False else None
sub=lambda e: sp.simplify(e.subs({sp.Derivative(B,(r,2)):sp.Symbol('Bpp'),sp.Derivative(B,r):Bh}).subs(B,0))
# evaluate by series: set B=Bh*(r-rh)+..., N=N0+N1(r-rh)
x=sp.symbols('x')
B1,B2,N0,N1,F0s,F1s,F2s,P0=sp.symbols('B1 B2 N0 N1 F0 F1 F2 P0')
Bs=B1*x+B2*x**2; Ns=N0+N1*x; Fs=F0s+F1s*x+F2s*x**2/2; Ps=P0
def atH(e):
    e2=e.subs({A:Ns.subs(x,r-rh),B:Bs.subs(x,r-rh),Ff:Fs.subs(x,r-rh),P:Ps}).doit()
    return sp.simplify(sp.limit(sp.simplify(e2),r,rh))
tt0=atH(Ett); rr0=atH(Err)
print("   tt at horizon:",tt0); print("   rr at horizon:",rr0)
chk("F2 tt and rr equations agree at the horizon (regularity)", sp.simplify(tt0-rr0)==0)
# solve for kappa_f = N0 B1/2: tt: F0 * (-B1 N1/N0 ...) ; express 1-2kappa r form
kap=sp.symbols('kappa')
rel=sp.simplify(tt0)
print("   horizon relation:",sp.simplify(rel))
chk("F2 the horizon relation contains the free horizon value F1=F'(r_h) (not a constant of the theory)", rel.has(F1s))
# GR limit: F0=1,F1=0,F2=0, P=R-2L -> must reproduce 1-2 kappa r = Lambda r^2 type relation for N=1,N1=0
Rh_expr=atH(Rs2)
print("   R at horizon:",Rh_expr)
GRrel=sp.simplify(rel.subs({F0s:1,F1s:0,F2s:0,N0:1,N1:0,P0:Rh_expr-2*L}).subs({N0:1,N1:0,F0s:1,F1s:0,F2s:0}))
GRrel=sp.simplify(GRrel.subs({N0:1,N1:0}))
print("   GR limit (P0=R_h-2Lambda):",GRrel)
chk("F2 GR control: horizon relation reduces exactly to B1 r_h = 1 - Lambda r_h^2 (= K2)", sp.simplify(GRrel-(B1/rh-1/rh**2+L))==0)
chk("F2 mutation: with a wrong P0=R_h-L the GR limit is NOT the K2 relation", sp.simplify(sp.simplify(rel.subs({F0s:1,F1s:0,F2s:0,N0:1,N1:0,P0:Rh_expr-L}))-(B1/rh-1/rh**2+L))!=0)
# closed form: eliminate B2 using R_h; N1 cancels
Rh_s,fh=sp.symbols('R_h f_h')
B2sol=sp.solve(sp.Eq(Rh_expr,Rh_s),B2)[0]
relc=sp.simplify(rel.subs(B2,B2sol).subs(P0,fh))
target=F0s*B1/rh+B1*F1s/2+F0s*Rh_s/2-F0s/rh**2-fh/2
chk("F2 closed form (N1 and B2 drop out): F_h(1-B1 r_h) = (r_h^2/2)(F_h R_h - f(R_h)) + B1 r_h^2 F'_h/2 with B1=2 kappa_f/N_h", sp.simplify(relc+target)==0 or sp.simplify(relc-target)==0 or sp.simplify(sp.expand(relc)+sp.expand(target))==0)
chk("F2 closed form control: dropping the F'_h term breaks it unless F'_h=0", sp.simplify(sp.simplify(relc)-(-(target-B1*F1s/2)))!=0)
# Rastall
kl,rho=sp.symbols('kl rho')
Gs=sp.symbols('G_s'); 
# trace of G + kl R g = 8 pi T with T_mn=-rho g: -R+4 kl R = -32 pi rho
RR=sp.Symbol('RR'); Rr=sp.solve(sp.Eq(-RR+4*kl*RR,-32*sp.pi*rho),RR)[0]
Lamr=sp.simplify(-(-8*sp.pi*rho-kl*Rr))   # G_mn = -Lambda_e g_mn  with  -Lambda_e = -8 pi rho - kl R
chk("R1 Rastall vacuum fluid: Lambda_e = 8 pi rho/(1-4 kl)", sp.simplify(Lamr-8*sp.pi*rho/(1-4*kl))==0)
chk("R1 control: kl=0 gives GR Lambda=8 pi rho", sp.simplify(Lamr.subs(kl,0)-8*sp.pi*rho)==0)
# Rastall vacuum: SdS with R=4 Lambda_e solves G_mn + kl R g=0 iff Lambda_e (1-4kl)... G=-Le g so -Le + kl*4Le =0 => (4kl-1)Le=0
chk("R1 Rastall T=0: SdS requires (4 kl-1) Lambda_e=0 -> Lambda_e arbitrary only at kl=1/4 (else Lambda_e=0)", sp.simplify((-Le+4*kl*Le).subs(kl,sp.Rational(1,4)))==0 and sp.simplify((-Le+4*kl*Le).subs(kl,0))!=0)
print("\n%d/%d"%(sum(ok),len(ok))); sys.exit(0 if all(ok) else 1)
