"""q04: domain-wall / slab reading.  sigma_M = a0/(2 pi G); Sigma_L = rho_Lambda R*, R* = 1/(2 a0) (puzzle horizon).  Puzzle: Sigma_L = 4 pi Sigma_M.
Variable held fixed per line is stated.  Newtonian Gauss + exact Israel (symmetric wall in de Sitter)."""
import sympy as sp, numpy as np, sys
ok=[]
def chk(n,c): ok.append(bool(c)); print(("PASS " if c else "FAIL ")+n)
G,a0,sig,Lam,H,z,w,V0,d,eta,lam_,R=sp.symbols('G a0 sigma Lambda H z w V0 delta eta lambda R',positive=True)
# 1 Gauss pillbox: field of a thin wall with tension (energy) sigma, Newtonian: g = 2 pi G sigma each side
chk("1 pillbox: 2 g A = 4 pi G sigma A -> g = 2 pi G sigma ; a0 = 2 pi G sigma_M -> sigma_M = a0/(2 pi G)", sp.simplify(sp.solve(sp.Eq(2*sp.pi*G*sig,a0),sig)[0]-a0/(2*sp.pi*G))==0)
sigM=a0/(2*sp.pi*G); rhoL=4*a0**2/G; Rstar=1/(2*a0)
SigL=rhoL*Rstar
chk("2 puzzle: Sigma_L = rho_Lambda R* = 2 a0/G = 4 pi Sigma_M  (4 pi from 2 pi G in the pillbox vs R*=1/(2a0))", sp.simplify(SigL-2*a0/G)==0 and sp.simplify(SigL/sigM-4*sp.pi)==0)
# 3 Exact Israel: symmetric pure-tension wall in de Sitter: A = -B = 2 pi G sigma ; 1/R^2 = H^2 + A^2
A=2*sp.pi*G*sig; invR2=H**2+A**2
chk("3 Israel: proper acceleration sqrt(1/R^2 - H^2) = 2 pi G sigma for every H (junction A-B=4 pi G sigma, symmetric A=-B)", sp.simplify(sp.sqrt(invR2-H**2)-A)==0)
Z2=32*sp.pi/3
Rw2=sp.simplify((1/invR2).subs({sig:sigM,H:sp.sqrt(32*sp.pi*a0**2/3)}).subs(G,1))
print("   wall with sigma=sigma_M in the puzzle de Sitter: (R a0)^2 =",Rw2,"  = 1/(1+Z^2) = 3/(3+32 pi); R/R* = 2/sqrt(1+Z^2) = %.4f"%float(2*np.sqrt(3/(3+32*np.pi))))
chk("4 wall radius: (R a0)^2 = 3/(3 + 32 pi) (no special value; R != R*)", sp.simplify(Rw2*a0**2-3/(3+32*sp.pi))==0)
# 5 vacuum slab (isotropic vacuum p=-rho) Gauss: div g = -4 pi G (rho+3p) = +8 pi G rho -> surface field of slab thickness w: 4 pi G rho w
gvac=sp.integrate(8*sp.pi*G*rhoL,(z,0,w/2))
w_a0=sp.solve(sp.Eq(gvac,a0),w)[0]
print("   isotropic vacuum slab: surface field = 4 pi G rho w ; = a0 at w = %s = R*/(8 pi)"%sp.simplify(w_a0))
chk("5 w(g=a0) = R*/(8 pi)  [and with ordinary matter 2 pi G Sigma: Sigma=Sigma_M]: R*/w = 8 pi, the same 8 pi as r_H^2 Lambda = 8 pi (restatement)", sp.simplify(w_a0*8*sp.pi-Rstar)==0)
# 6 equilibrium: vacuum has rho+p=0 -> hydrostatic dp/dz = -(rho+p) g = 0 for ANY thickness: no equilibrium thickness
rho_,p_=sp.symbols('rho p')
chk("6 hydrostatic force on vacuum: (rho+p) g = 0 identically -> equilibrium imposes NO thickness (w free)", sp.simplify((rho_+p_).subs(p_,-rho_))==0)
# 7 thick scalar wall (phi^4 kink): sigma = (8/3) V0 delta ; V0 = barrier height identified with rho_Lambda
phi=eta*sp.tanh(z/d); V=lam_/4*(phi**2-eta**2)**2
lam_sol=sp.solve(sp.Eq(d**2,2/(lam_*eta**2)),lam_)[0]
sigma_k=sp.integrate(sp.simplify(sp.diff(phi,z)**2),(z,-sp.oo,sp.oo))
V0k=(lam_*eta**4/4)
ratio=sp.simplify((sigma_k.subs(eta,sp.sqrt(2/(lam_*d**2)))/ (V0k.subs(eta,sp.sqrt(2/(lam_*d**2)))*d)))
print("   kink sigma/(V0 delta) =",ratio)
chk("7 phi^4 kink: sigma = (8/3) V0 delta (profile width delta, V0 barrier height) -- rational, pi-free", sp.simplify(ratio-sp.Rational(8,3))==0)
dk=sp.simplify(sp.solve(sp.Eq(sigM,sp.Rational(8,3)*rhoL*d),d)[0])
print("   sigma_M = (8/3) rho_Lambda delta  ->  delta =",dk,"; R*/delta =",sp.simplify(Rstar/dk)," = Z^2 = 32 pi/3 (pure restatement: it just encodes sigma_M and rho_Lambda, with the width a FREE parameter of the potential)")
chk("8 R*/delta = 32 pi/3 follows from the puzzle (restatement); delta is set by the scalar's (lambda, eta), two parameters vs one condition V0=rho_Lambda -> one free parameter remains", sp.simplify(Rstar/dk-32*sp.pi/3)==0)
# control: tension vs 2 pi -> mutation (pillbox with pi instead of 2pi) breaks check 2's 4 pi
chk("9 control: pillbox with g = 4 pi G sigma (wrong) changes Sigma_L/Sigma_M from 4 pi to 8 pi", sp.simplify(SigL/(a0/(4*sp.pi*G))-8*sp.pi)==0 and sp.simplify(SigL/sigM-4*sp.pi)==0)
# decoy: how often does a random 'Sigma_L/Sigma_M' lie within 1% of a 'natural' pi-multiple {2pi,4pi,8pi,pi,...}?
import random
rng=random.Random(5); menu=[np.pi*k for k in (1,2,4,8,16,0.5,0.25)]
cnt=0
for _ in range(5000):
    t=np.exp(rng.uniform(np.log(1),np.log(50)))
    cnt+= any(abs(t/m-1)<0.01 for m in menu)
print("   decoy rate: a random target in [1,50] lies within 1%% of a pi*{1/4..16} menu value %.3f of the time (4 pi is a menu value by construction of Gauss pillbox, not evidence)"%(cnt/5000))
chk("10 decoy rate computed", cnt>0)
print("\n%d/%d"%(sum(ok),len(ok))); sys.exit(0 if all(ok) else 1)
