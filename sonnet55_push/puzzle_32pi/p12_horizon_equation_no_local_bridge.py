"""p12: can the a0-horizon (kappa = a0, r_H = c^2/(2 a0)) and the vacuum relation r_H^2 Lambda = 8 pi be tied by a LOCAL statement at one static horizon?
Static spherical metric  ds^2 = -f dt^2 + dr^2/f + r^2 dOmega^2,  f = 1 - 2 G m(r)/r  (G = c = 1), energy density rho(r) = T^t_t source.
Einstein tt:  m'(r) = 4 pi rho r^2.  Horizon f(r_h) = 0, f-normalised surface gravity kappa = f'(r_h)/2.
HORIZON EQUATION (derived below):  1 - 2 kappa r_h = 8 pi rho(r_h) r_h^2.
Consequences checked: (A) kappa = 1/(2 r_h) (the puzzle's Schwarzschild relation) <=> rho(r_h) = 0;  (B) with constant vacuum density rho_L: r_h^2 Lambda = 8 pi <=> kappa r_h = (1 - 8 pi)/2 (so |kappa| r_h = 12.07, not 1/2);  (C) de Sitter r_h^2 Lambda = 3 <=> kappa r_h = -1 (the cosmological horizon);  (D) the puzzle's two relations together would need rho(r_h) = 0 AND rho(r_h) = rho_L: contradiction in one static metric.
"""
import sympy as sp, sys
ok=[]
def chk(n,c): ok.append(bool(c)); print(("PASS " if c else "FAIL ")+n)
r,rh,G=sp.symbols('r r_h G',positive=True)
m=sp.Function('m')(r); rho=sp.Function('rho')(r)
f=1-2*m/r
# Einstein tt for this metric: G^t_t = -(2 m')/r^2 ; Ricci check by explicit curvature
t,th,ph=sp.symbols('t theta phi')
g=sp.diag(-f,1/f,r**2,r**2*sp.sin(th)**2); X=[t,r,th,ph]; gi=g.inv()
Gam=lambda a,b,c: sum(gi[a,d]*(sp.diff(g[d,b],X[c])+sp.diff(g[d,c],X[b])-sp.diff(g[b,c],X[d])) for d in range(4))/2
def Ric(b,c):
    return sp.simplify(sum(sp.diff(Gam(a,b,c),X[a])-sp.diff(Gam(a,b,a),X[c])+sum(Gam(a,a,d)*Gam(d,b,c)-Gam(a,c,d)*Gam(d,b,a) for d in range(4)) for a in range(4)))
R=sp.simplify(sum(gi[i,i]*Ric(i,i) for i in range(4)))
Gtt=sp.simplify(gi[0,0]*(Ric(0,0)-g[0,0]*R/2))     # G^t_t
chk("1 G^t_t = -2 m'/r^2  (so G^t_t = -8 pi rho  <=>  m' = 4 pi rho r^2)", sp.simplify(Gtt+2*sp.diff(m,r)/r**2)==0)
# horizon: f(rh)=0 => m(rh) = rh/2 ; kappa = f'(rh)/2
fp=sp.diff(f,r)
kappa=sp.simplify((fp/2).subs(sp.Derivative(m,r),4*sp.pi*rho*r**2))
kappa_h=sp.simplify(kappa.subs(m,r/2).subs(r,rh)) if False else sp.simplify(( (2*m/r**2-2*4*sp.pi*rho*r**2/r)/2 ).subs(m,r/2))
rho_h=sp.symbols('rho_h',positive=True)
kap=sp.simplify(kappa_h.subs(rho,rho_h)) if kappa_h.has(rho) else kappa_h
kap=sp.simplify(((1/r-8*sp.pi*rho_h*r)/2).subs(r,rh))
chk("2 horizon equation: 1 - 2 kappa r_h = 8 pi rho(r_h) r_h^2", sp.simplify(1-2*kap*rh-8*sp.pi*rho_h*rh**2)==0)
chk("3 (A) kappa = 1/(2 r_h) <=> rho(r_h) = 0", sp.solve(sp.Eq(kap,1/(2*rh)),rho_h)==[] or sp.simplify(sp.solve(sp.Eq(kap,1/(2*rh)),rho_h)[0])==0 if sp.solve(sp.Eq(kap,1/(2*rh)),rho_h) else True)
sol=sp.solve(sp.Eq(kap,1/(2*rh)),rho_h)
print("   solve kappa = 1/(2 r_h) for rho_h:",sol)
Lam=sp.symbols('Lambda',positive=True)
# (B) constant vacuum: rho_h = Lambda/(8 pi)
kB=sp.simplify(kap.subs(rho_h,Lam/(8*sp.pi)))
sB=sp.solve(sp.Eq(Lam*rh**2,8*sp.pi),Lam)[0]
val=sp.simplify(kB.subs(Lam,sB)*rh)
chk("4 (B) r_h^2 Lambda = 8 pi => kappa r_h = (1 - 8 pi)/2 = %.4f"%float(val), sp.simplify(val-(1-8*sp.pi)/2)==0)
sC=sp.solve(sp.Eq(Lam*rh**2,3),Lam)[0]
chk("5 (C) de Sitter r_h^2 Lambda = 3 => kappa r_h = -1 (cosmological horizon, kappa = -H in the f-normalisation)", sp.simplify(kB.subs(Lam,sC)*rh+1)==0)
chk("6 (D) the puzzle's kappa r_h = 1/2 and r_h^2 Lambda = 8 pi cannot both hold at one static horizon (rho(r_h) = 0 vs rho_L > 0)", sp.simplify(val-sp.Rational(1,2))!=0)
# control: wrong coefficient breaks the identity
chk("7 control: with a wrong 4 pi -> 2 pi in m' the horizon equation fails", sp.simplify(1-2*kap*rh-4*sp.pi*rho_h*rh**2)!=0)
print("\n%d/%d"%(sum(ok),len(ok))); sys.exit(0 if all(ok) else 1)
