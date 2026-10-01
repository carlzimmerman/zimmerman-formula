"""q01: MOND phantom density around a point mass; rho_ph(r*) = rho_Lambda. Lambda held fixed (G rho_Lambda = Lambda/8pi); puzzle: Lambda = 32 pi a0^2."""
import sympy as sp, numpy as np, sys
from common import *
ok=[]
def chk(n,c): ok.append(bool(c)); print(("PASS " if c else "FAIL ")+n)
r,M,a0,G,Lam=sp.symbols('r M a0 G Lambda',positive=True)
# deep MOND: g = sqrt(G M a0)/r ; phantom density = (1/4piG) div(g - g_N) ; away from origin g_N term has zero divergence
g=sp.sqrt(G*M*a0)/r
rho_ph=sp.simplify(sp.diff(r**2*g,r)/r**2/(4*sp.pi*G))
chk("1 rho_ph = sqrt(G M a0)/(4 pi G r^2) (deep MOND, divergence of g)", sp.simplify(rho_ph-sp.sqrt(G*M*a0)/(4*sp.pi*G*r**2))==0)
rhoL=Lam/(8*sp.pi*G)
rs2=sp.solve(sp.Eq(rho_ph,rhoL),r)[0]**2
print("   r*^2 =",sp.simplify(rs2),"  [generic Lambda; pi content: 4pi (Poisson) vs 8pi (Einstein) -> 2 sqrt(G M a0)/Lambda, pi-FREE]")
chk("2 generic (Lambda fixed): r*^2 = 2 sqrt(G M a0)/Lambda (the pis cancel: 4pi in Poisson, 8pi in Lambda=8piG rho)", sp.simplify(rs2-2*sp.sqrt(G*M*a0)/Lam)==0)
pz=sp.simplify(rs2.subs(Lam,32*sp.pi*a0**2/ (1)).subs(G,1)); rM=sp.sqrt(M/a0)
chk("3 puzzle Lambda=32 pi a0^2: r*^2 = r_M r_a0/(16 pi) (r_a0=1/a0)", sp.simplify(pz-rM/(16*sp.pi*a0)).subs(G,1)==0)
# masses: r*=r_M ; r*=r_a0/2  (puzzle substitution, G=c=1)
Msol1=sp.solve(sp.Eq(pz,M/a0),M)[0]; Msol2=sp.solve(sp.Eq(pz,1/(4*a0**2)),M)[0]
print("   r*=r_M     -> M =",Msol1,"  (",sp.simplify(Msol1*a0),"/a0 ;  pi^-2)")
print("   r*=r_a0/2  -> M =",Msol2,"  (",sp.simplify(Msol2*a0),"/a0 ; pi^0 x 1/a0^... )")
chk("4 M(r*=r_M) = 1/(256 pi^2 a0) and M(r*=r_a0/2) = 16 pi^2/a0 (symbolic)", sp.simplify(Msol1-1/(256*sp.pi**2*a0))==0 and sp.simplify(Msol2-16*sp.pi**2/a0)==0)
print("   NOTE both masses are (number) c^4/(G a0): defined BY a0 -> not independent of it (tautological mass).")
# full interpolation check: nu_simple point mass: phantom -> deep formula (numerical)
y=sp.symbols('y',positive=True)
nu=lambda y:(1+sp.sqrt(1+4/y))/2
gN=G*M/r**2
gfull=sp.simplify(nu(gN/a0)*gN)
rho_full=sp.diff(r**2*(gfull-gN),r)/r**2/(4*sp.pi*G)
sub={G:1,M:1,a0:1}
val=float(rho_full.subs(sub).subs(r,1e3)); deep=float(rho_ph.subs(sub).subs(r,1e3))
chk("5 nu_simple phantom -> deep formula at r=1e3 r_M (rel err %.1e)"%abs(val/deep-1), abs(val/deep-1)<1e-3)
# CONTROL (mutation): wrong Poisson factor must break check 1/2
bad=sp.diff(r**2*g,r)/r**2/(2*sp.pi*G)
chk("6 control: 2pi instead of 4pi breaks the pi-cancellation (r*^2 no longer 2sqrt(GMa0)/Lambda)", sp.simplify(sp.solve(sp.Eq(bad,rhoL),r)[0]**2-2*sp.sqrt(G*M*a0)/Lam)!=0)
# --- scan on frozen menu (condition: rho_ph(r_t)=rho_Lambda, Lambda=1):  r_t^2 = 2 sqrt(M a0)
def cond(a,Mv,rn): return np.log(radii(a,Mv)[rn]**2/(2*np.sqrt(Mv*a)))
res=scan(cond); h,nr=hits(res,TARGET); dr=decoy_rate(res)
print("\nscan (i): a0-free mass x radius target -> a0/sqrt(Lambda) roots:")
for mn,rn,rt in res: print("   %-18s %-12s"%(mn,rn),["%.5f"%x for x in rt])
print("   target 1/sqrt(32pi)=%.5f  hits(1%%)=%d of %d roots; decoy hit-rate (random target) = %.3f"%(TARGET,h,nr,dr))
chk("7 scan runs, roots exist for the menu", nr>0)
# positive control: solver recovers a planted value
planted=0.0431
pc=roots_log(lambda a: np.log(a/planted)); chk("8 positive control: planted a0 recovered", len(pc)==1 and abs(pc[0]/planted-1)<1e-6)
chk("9 no menu entry hits the puzzle target within 1%% (hits=%d)"%h, h==0)
# the 'a0-independent mass' question, closed form: M(r*=r_M) =4 a0^3/Lambda^2 generic
Mg=sp.solve(sp.Eq(rs2,M/a0),M)[0].subs(G,1)
print("   generic r*=r_M:  M =",sp.simplify(Mg)," -> equals sqrt(Lambda)^-1 k  iff  a0 =(k/4)^(1/3) sqrtLambda ; needed k for target = %.5f (no natural mass)"%(4*TARGET**3))
chk("10 needed mass coefficient is not in the menu", all(abs(4*TARGET**3/m-1)>0.2 for m in MASSES.values()))
print("\n%d/%d"%(sum(ok),len(ok))); sys.exit(0 if all(ok) else 1)
