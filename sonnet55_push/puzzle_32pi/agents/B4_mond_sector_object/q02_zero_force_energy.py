"""q02: zero-force radius of deep-MOND attraction vs Lambda repulsion, and the energy-equality threshold. Lambda held fixed; H^2 = Lambda/3."""
import sympy as sp, numpy as np, mpmath as mp, sys
from common import *
ok=[]
def chk(n,c): ok.append(bool(c)); print(("PASS " if c else "FAIL ")+n)
r,M,a0,G,Lam=sp.symbols('r M a0 G Lambda',positive=True)
H2=Lam/3
gM=sp.sqrt(G*M*a0)/r
rZF2=sp.solve(sp.Eq(gM,H2*r),r)[0]**2
rs2=2*sp.sqrt(G*M*a0)/Lam                       # from q01 (rho_ph = rho_Lambda)
print("   r_ZF^2 =",sp.simplify(rZF2)," ; r*^2 =",rs2)
chk("1 r_ZF^2 = 3 sqrt(G M a0)/Lambda", sp.simplify(rZF2-3*sp.sqrt(G*M*a0)/Lam)==0)
chk("2 STRUCTURAL: r_ZF^2/r*^2 = 3/2 exactly for every M, a0, Lambda (pi-free; same units fixed)", sp.simplify(rZF2/rs2-sp.Rational(3,2))==0)
chk("3 ... equivalently rho_ph=rho_Lambda <=> g = (3/2) H^2 r (div g = Lambda/2 at r*, g/r in deep MOND)", sp.simplify((gM/r).subs(r,sp.sqrt(rs2))-Lam/2)==0)
# puzzle substitution
pz=sp.simplify(rZF2.subs(Lam,32*sp.pi*a0**2).subs(G,1))
chk("4 puzzle: r_ZF^2 = 3 r_M r_a0/(32 pi)", sp.simplify(pz-3*sp.sqrt(M/a0)/(32*sp.pi*a0))==0)
# scan ZF = r_t on frozen menu
def condZF(a,Mv,rn): return np.log(radii(a,Mv)[rn]**2/(3*np.sqrt(Mv*a)))
res=scan(condZF); h,nr=hits(res,TARGET); dr=decoy_rate(res,seed=2)
print("\nscan (ii) zero-force radius = r_t -> a0/sqrt(Lambda):")
for mn,rn,rt in res: print("   %-18s %-12s"%(mn,rn),["%.5f"%x for x in rt])
print("   hits(1%%)=%d of %d ; decoy rate = %.3f"%(h,nr,dr))
chk("5 no hit on the target (ZF scan)", h==0)
# identity check between scans: ZF roots relate to r* roots? (3/2) -> verify via independent numeric
a_t=0.3; Mv=1.0
rzf=np.sqrt(3*np.sqrt(Mv*a_t)); gnum=np.sqrt(Mv*a_t)/rzf; chk("6 numeric: at r_ZF, g = H^2 r (H^2=1/3)", abs(gnum-rzf/3)<1e-12)
# energy equality: deep-MOND potential has a log -> reference r0 required.  Phi_M = sqrt(GMa0) ln(r/r0);  Lambda: -(1/2)H^2 r^2 -> equality of magnitudes
# a0 r_M ln x = (Lambda/6) r_M^2 x^2 , x = r/r0 with r0=r_M ; solutions exist iff lam <= 1/(2e), lam = Lambda r_M/(6 a0)
lam_max=1/(2*np.e)
chk("7 ln x = lam x^2 has a real root iff lam <= 1/(2e) (max of ln x/x^2 at x=sqrt e) -- reference r0=r_M", abs(max(np.log(x)/x**2 for x in np.linspace(1.0001,5,100000))-lam_max)<1e-6)
# threshold mass: lam=1/(2e): Lambda r_M/(6a0) = 1/(2e) -> r_M = 3 a0/(e Lambda) -> M_thr = a0 r_M^2 = 9 a0^3/(e^2 Lambda^2)
Mthr=lambda a: 9*a**3/(np.e**2)
def condE(a,Mv,rn): return np.log(Mthr(a)/Mv) if rn=="2GM" else np.nan   # one condition per mass: M = M_thr(a0)
resE=[]
for mn,Mv in MASSES.items():
    resE.append((mn,"M=M_thr",roots_log(lambda a: np.log(Mthr(a)/Mv))))
print("\nenergy-equality threshold M_thr = 9 a0^3/(e^2 Lambda^2) [reference r0=r_M: REFERENCE-DEPENDENT] set equal to menu mass:")
for mn,_,rt in resE: print("   %-18s a0/sqrtL ="%mn,["%.5f"%x for x in rt])
h2,_=hits(resE,TARGET); dr2=decoy_rate(resE,seed=3)
print("   hits=%d ; decoy rate=%.3f  (pi content: none from the threshold; e^2 from the log reference; the log potential has no absolute zero)"%(h2,dr2))
chk("8 energy-equality: no menu hit", h2==0)
# control: reference choice changes the threshold (shows it is convention): r0 = 2 r_M
def thr_M(s_ref):   # numeric threshold mass (a0=1,Lambda=1) for reference r0 = s_ref r_M: lam = s_ref r_M/6 <= 1/(2e)
    rM=(1/(2*np.e))*6/s_ref; return rM**2
chk("9 control: threshold mass changes by 4x when the arbitrary reference is doubled (M_thr ~ 1/s^2): %.4f vs %.4f"%(thr_M(1),thr_M(2)), abs(thr_M(1)/thr_M(2)-4)<1e-12)
print("\n%d/%d"%(sum(ok),len(ok))); sys.exit(0 if all(ok) else 1)
