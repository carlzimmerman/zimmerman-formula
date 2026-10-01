"""b01: theory-independent kinematics of a static spherical horizon (GR control = p12), and the 'SdS-form' theorem.
(K1) metric ds^2=-N^2 f dt^2+dr^2/f+r^2dOmega^2, f=1-2m(r)/r: G^t_t=-2 m'/r^2 for ANY N (so 'rho_eff := m'/(4 pi r^2)' is a definition valid in every theory).
     horizon: f(r_h)=0 -> f'(r_h)=1/r_h-2 m'(r_h);  kappa_f = N_h f'/2  =>  kappa_f r_h = N_h (1 - 8 pi rho_eff(r_h) r_h^2)/2.
(K2) SdS-form theorem: if a theory's static vacuum solution is f=1-2M/r-Lam_e r^2/3 (N=1) then 1-2 kappa r_h = Lam_e r_h^2 EXACTLY, whatever the theory.
     Hence T=(1/2,8pi) needs Lam_e r_h^2 = 0 and 8 pi at once: impossible; this covers every theory whose vacuum branch is an Einstein space (f(R) const-R branch,
     scalar-tensor/Horndeski/DHOST 'stealth' SdS, Brans-Dicke with no hair, Rastall vacuum, ...).  Only a change of the FORM of f can help.
(K3) with N_h != 1 (N != 1 allowed by the theory) T needs N_h = 1/(1-8 pi) = -0.0414 (negative) for rho_eff=Lambda/8pi: i.e. a sign-flipped/zero lapse at the horizon.
(K4) T lies on a negative-mass cosmological-type horizon even in GR: M=r_h(1-8pi/3)/2<0, f'(r_h)<0, f monotone decreasing so there is NO free-fall point f'(r0)=0:
     the Bousso-Hawking normalisation (1/sqrt f(r0)) is undefined there.
"""
import sympy as sp, sys
ok=[]
def chk(n,c): ok.append(bool(c)); print(("PASS " if c else "FAIL ")+n)
r,rh,Lam,M=sp.symbols('r r_h Lambda M',positive=True)
t,th,ph=sp.symbols('t theta phi')
m=sp.Function('m')(r); N=sp.Function('N')(r)
f=1-2*m/r
g=sp.diag(-N**2*f,1/f,r**2,r**2*sp.sin(th)**2); X=[t,r,th,ph]; gi=g.inv()
Gam=lambda a,b,c: sum(gi[a,d]*(sp.diff(g[d,b],X[c])+sp.diff(g[d,c],X[b])-sp.diff(g[b,c],X[d])) for d in range(4))/2
def Ric(b,c):
    return sp.simplify(sum(sp.diff(Gam(a,b,c),X[a])-sp.diff(Gam(a,b,a),X[c])+sum(Gam(a,a,d)*Gam(d,b,c)-Gam(a,c,d)*Gam(d,b,a) for d in range(4)) for a in range(4)))
R=sp.simplify(sum(gi[i,i]*Ric(i,i) for i in range(4)))
Gtt=sp.simplify(gi[0,0]*(Ric(0,0)-g[0,0]*R/2))
chk("K1 G^t_t = -2 m'/r^2 for arbitrary lapse N(r) (rho_eff := m'/(4 pi r^2) is a definition in any theory)", sp.simplify(Gtt+2*sp.diff(m,r)/r**2)==0)
# control: wrong power fails
chk("K1 control: G^t_t = -m'/r^2 is FALSE", sp.simplify(Gtt+sp.diff(m,r)/r**2)!=0)
# horizon identity with generic rho_eff
rho,Nh=sp.symbols('rho_h N_h',positive=True)
fp_h=1/rh-2*(4*sp.pi*rho*rh**2)/rh   # f'(r_h)=1/r_h-2m'(r_h)/r_h (first draft dropped the 1/r_h; the check caught it)
kap=Nh*fp_h/2
chk("K1 kappa_f r_h = N_h (1-8 pi rho r_h^2)/2", sp.simplify(kap*rh-Nh*(1-8*sp.pi*rho*rh**2)/2)==0)
# GR control: N=1, rho=Lambda/8pi, SdS
fS=1-2*M/r-Lam*r**2/3
Msol=sp.solve(fS.subs(r,rh),M)[0]
kS=sp.simplify((sp.diff(fS,r)/2).subs(M,Msol).subs(r,rh))
chk("K2 SdS: 2 kappa r_h = 1 - Lambda r_h^2 for every M (exact)", sp.simplify(2*kS*rh-(1-Lam*rh**2))==0)
chk("K2 control: 2 kappa r_h = 1 - Lambda r_h^2/3 is FALSE", sp.simplify(2*kS*rh-(1-Lam*rh**2/3))!=0)
# T impossible in SdS form
sol=sp.solve([sp.Eq(2*kS*rh,1),sp.Eq(Lam*rh**2,8*sp.pi)],[Lam],dict=True)
chk("K2 T=(1/2,8 pi) has no solution in SdS form (needs Lambda r_h^2 = 0 and 8 pi)", sol==[])
# K3
Nn=sp.simplify(sp.Rational(1,2)/ ((1-8*sp.pi)/2))
chk("K3 needed N_h = 1/(1-8 pi) = %.5f (negative)"%float(Nn), Nn<0 and abs(float(Nn)+1/(8*float(sp.pi)-1))<1e-12)
# K4: negative mass, monotone f
Mt=Msol.subs(Lam,8*sp.pi/rh**2)
fp=sp.diff(fS,r).subs(M,Mt).subs(Lam,8*sp.pi/rh**2)
rr=sp.symbols('rr',positive=True)
vals=[float(fp.subs({rh:1,r:x})) for x in [0.01,0.1,0.5,1,2,10,100]]
chk("K4 at T: M<0 (M=%.3f r_h) and f'(r)<0 for all sampled r>0 (no free-fall point)"%float(Mt.subs(rh,1)), float(Mt.subs(rh,1))<0 and all(v<0 for v in vals))
# control: ordinary SdS (Lambda r_h^2 <3 , M>0) does have a free-fall point
Mg=Msol.subs(Lam,1.0/rh**2); fpg=sp.diff(fS,r).subs(M,Mg).subs(Lam,1.0/rh**2).subs(rh,1)
chk("K4 control: for Lambda r_h^2=1 (M>0) f' changes sign (free-fall point exists)", float(fpg.subs(r,0.01))>0 and float(fpg.subs(r,10))<0)
print("\n%d/%d"%(sum(ok),len(ok))); sys.exit(0 if all(ok) else 1)
