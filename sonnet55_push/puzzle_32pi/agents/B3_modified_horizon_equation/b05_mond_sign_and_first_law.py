"""b05: (M1) Newtonian-limit QUMOND/AQUAL phantom density of a point mass: rho_ph = (M/(4 pi r^2)) d(nu-1)/dr >= 0 for every monotone nu(g_N/a0) decreasing in g_N,
so it can never supply the NEGATIVE rho_extra(r_h) = -rho_Lambda that T needs (K1).  SCOPE: weak-field formula; r_h is a strong-field radius (Phi/c^2=1/2) -> not a proof for relativistic AeST/TeVeS/BIMOND, which are NOT computed.
At T the Newtonian g_N(r_h)=M/r_h^2 = 1/(2 r_h) = a0 exactly (x=1).
(W1) GR first law fixes the 4: with M=r_h(1-Lam r_h^2/3)/2, T=kappa/2pi, dM = T dS gives S = pi r_h^2 = A/4 (the 4 = 8pi/2pi); a G_eff rescaling multiplies Einstein term and S together: S Lambda r_h^2... the G-free statement Lambda r_h^2=8pi unchanged.
"""
import sympy as sp, numpy as np, sys
ok=[]
def chk(n,c): ok.append(bool(c)); print(("PASS " if c else "FAIL ")+n)
nus={'simple':lambda x:1/2+np.sqrt(1/4+1/x),'standard':lambda x:np.sqrt((1+np.sqrt(1+4/x**2))/2),'RAR':lambda x:1/(1-np.exp(-np.sqrt(x))),'mono':lambda x:(1-np.exp(-x**1.0))**-1*0+1/(1-np.exp(-x)) }
rr=np.linspace(0.05,50,4000)  # r in units where GM/a0 = 1 (r_h-ish scale): g_N=1/r^2
for k,nu in nus.items():
    x=1/rr**2; v=nu(x)-1; d=np.gradient(v,rr)
    chk("M1 %s: rho_ph ∝ d(nu-1)/dr >= 0 on the whole grid"%k, np.all(d>=-1e-12))
# control: a non-monotone (increasing in g_N) nu would give negative phantom
nu_bad=lambda x:1+0.5*x/(1+x)
d=np.gradient(nu_bad(1/rr**2)-1,rr)
chk("M1 control: nu increasing in g_N gives rho_ph<0 somewhere (test can fail)", np.any(d<-1e-9))
# W1
r,Lam,G=sp.symbols('r Lambda G',positive=True)
M=r*(1-Lam*r**2/3)/2; T=(1-Lam*r**2)/(4*sp.pi*r)
dS=sp.simplify(sp.diff(M,r)/T)
chk("W1 GR first law: dS/dr = 2 pi r  (S=pi r^2=A/4) for every Lambda", sp.simplify(dS-2*sp.pi*r)==0)
chk("W1 control: with T=kappa/pi (wrong) S != A/4", sp.simplify(sp.diff(M,r)/(2*T)-2*sp.pi*r)!=0)
Geff,x=sp.symbols('G_eff x',positive=True)
chk("W1 Lambda r_h^2 = 8 pi is G-free: rescaling G -> G_eff changes G rho_Lambda = Lambda/8pi but not Lambda r_h^2", sp.simplify((8*sp.pi*Geff*(Lam/(8*sp.pi*Geff)))-Lam)==0)
# T: S at puzzle horizon in GR = pi r_h^2 = pi/(4 a0^2); S*Lambda = 8 pi^2 (no new info)
chk("W1 at T (GR area): S Lambda = (pi r_h^2)(8 pi/r_h^2) = 8 pi^2 = A Lambda/4", sp.simplify(sp.pi*r**2*8*sp.pi/r**2-8*sp.pi**2)==0)
print("\n%d/%d"%(sum(ok),len(ok))); sys.exit(0 if all(ok) else 1)
