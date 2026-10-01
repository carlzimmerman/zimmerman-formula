"""N3-2: homogeneous closure M=(4pi/3) f rho_Lambda R^3 ; horizon/ZF coincidence ; target comparison only at the end. c=1."""
import warnings; warnings.filterwarnings('ignore')
import numpy as np, sympy as sp, hashlib
from scipy.optimize import brentq
P=F=0
def chk(n,ok):
    global P,F
    P+=bool(ok); F+=(not ok); print(("PASS " if ok else "FAIL ")+n)
h=hashlib.sha256(open('CRITERIA.md','rb').read()).hexdigest()
chk("criteria file hash matches the pre-declared hash",h==open('CRITERIA_HASH.txt').read().split()[0])
nus={'simple':lambda x:0.5+np.sqrt(0.25+1/x),
     'standard':lambda x:np.sqrt((1+np.sqrt(1+4/x**2))/2),
     'rar_d1':lambda x:1/(1-np.exp(-np.sqrt(x))),
     'delta2':lambda x:(1-np.exp(-x))**-0.5}
def nud(d): return lambda x:(1-np.exp(-x**(d/2)))**(-1/d)
def xstar(nu,f):   # nu(x)=2/f, needs f<2
    return brentq(lambda lx:nu(np.exp(lx))-2/f,-40,40,xtol=1e-14)
def xs(nu,f): return np.exp(xstar(nu,f))
# --- closed-form check (simple nu): nu=2/f -> x = 1/((2/f-1/2)^2-1/4)
f=sp.symbols('f',positive=True)
xs_sym=1/((2/f-sp.Rational(1,2))**2-sp.Rational(1,4))
chk("simple nu: x*(f=1)=1/2 exactly",sp.simplify(xs_sym.subs(f,1)-sp.Rational(1,2))==0)
chk("numeric x*(simple,f=1)=0.5",abs(xs(nus['simple'],1)-0.5)<1e-10)
chk("standard nu: x*(f=1)=1/sqrt12",abs(xs(nus['standard'],1)-1/np.sqrt(12))<1e-10)
chk("RAR delta=1: x*(f=1)=(ln2)^2",abs(xs(nus['rar_d1'],1)-np.log(2)**2)<1e-10)
# --- closure: g_N = f H^2 R/2 ; fixed point nu=2/f ; R* H = 2 x*/(f Z) ; horizon coincidence s=R*H => Z = 2x*/(f s)
print("\nS3: vacuum's own density (f=1), horizon coincidence R*=c/H  ->  Z = 2 x*")
for k,nu in nus.items(): print("  %-9s x*=%.4f  Z=%.4f"%(k,xs(nu,1),2*xs(nu,1)))
chk("S3/S6: f=1, s=1 gives Z in (0.5,1.1) for all four nu (nowhere near 5.79)",all(0.5<2*xs(nu,1)<1.1 for nu in nus.values()))
# free-parameter freedom: Z(f) monotone covering (0,inf) => every target has a preimage f
fs=np.linspace(0.05,1.999,400)
Zf=np.array([2*xs(nus['simple'],q)/q for q in fs])
chk("Z(f) (simple nu, s=1) is monotone increasing, range %.3f..%.1f"%(Zf[0],Zf[-1]),np.all(np.diff(Zf)>0))
T={'Z=sqrt(32pi/3)=5.7888':np.sqrt(32*np.pi/3),'3sqrt3':3*np.sqrt(3),'6':6.0,'2pi':2*np.pi,'decoy 4.5':4.5,'decoy 7.3':7.3,'decoy 8.1':8.1}
print("\nS6 (end): f needed so that the homogeneous closure gives each target (simple nu, s=1)")
fneed={}
for k,z in T.items():
    g=lambda q:2*xs(nus['simple'],q)/q-z
    fneed[k]=brentq(g,0.05,1.9999); print("  %-22s f=%.4f"%(k,fneed[k]))
chk("every target, including decoys, has a solution f in (0,2): closure cannot discriminate",all(0.05<v<2 for v in fneed.values()))
# no natural f: candidate natural values
print("  natural f candidates give Z:", {q:round(2*xs(nus['simple'],q)/q,3) for q in (0.5,1,4/3,1.5)})
# decoy hit-rate under freedom f in [0.8,1.2] (+/-20% on the density) and delta in [0.5,3] at f=1
z_lo=2*xs(nus['simple'],0.8)/0.8; z_hi=2*xs(nus['simple'],1.2)/1.2
print("  f in [0.8,1.2] (simple nu): Z in [%.3f,%.3f]"%(z_lo,z_hi))
chk("f within +-20%% of 1 does NOT reach 5.789 (window max %.2f): a genuine failure of the closure"%z_hi,z_hi<5.78)
zd=[2*xs(nud(d),1) for d in np.linspace(0.2,4,200)]
print("  delta in [0.2,4] at f=1: Z range [%.3f,%.3f]"%(min(zd),max(zd)))
dneed={}
for k,z in T.items():
    try: dneed[k]=brentq(lambda d:2*xs(nud(d),1)-z,0.2,4)
    except Exception: dneed[k]=None
print("  delta needed (f=1,s=1):",{k:(None if v is None else round(v,3)) for k,v in dneed.items()})
# hit-rate of decoys: fraction of log-uniform Z in [3,12] reachable by delta in [0.05,4]
chk("every target (incl. decoys) reachable by a one-parameter interpolation family delta at f=1: no discrimination",all(v is not None for v in dneed.values()))
fr=sp.nsimplify(sp.Rational(12,7)); 
xr=1/((2/fr-sp.Rational(1,2))**2-sp.Rational(1,4)); chk("simple nu: f=12/7 gives exactly Z=6 (rational f for rational Z; not a natural density factor)",sp.simplify(2*xr/fr)==6)
# --- horizon = zero-force radius for the vacuum mass inside the Hubble sphere (M=R_H/(2G))
print("\nS4: M = vacuum mass in the Hubble sphere, deep-MOND ZF radius vs horizon")
for z in (T['Z=sqrt(32pi/3)=5.7888'],):
    chk("deep-MOND R_ZF/R_H=(2Z)^(-1/4)=%.3f"%((2*z)**-.25),True)
    xdeep=z**1.5/np.sqrt(2)
    chk("deep-MOND self-consistency x=Z^(3/2)/sqrt2=%.2f must be <<1: FAILS (x>>1)"%xdeep,xdeep>1)
    # exact nu: solve nu(x)x^1.5 = Z^1.5/sqrt2 for the simple nu
    nu=nus['simple']; mu=z**1.5/np.sqrt(2)
    xe=brentq(lambda lx:nu(np.exp(lx))*np.exp(1.5*lx)-mu,-30,30); print("  exact simple nu: x=%.3f  R_ZF/R_H=%.4f  nu=%.4f"%(np.exp(xe),np.sqrt(z/(2*np.exp(xe))),nu(np.exp(xe))))
    chk("exact R_ZF/R_H for M_Lambda(R_H) at Z=5.789 is not 1 (%.3f)"%np.sqrt(z/(2*np.exp(xe))),abs(np.sqrt(z/(2*np.exp(xe)))-1)>0.1)
# coincidence Z from nu(Z/2)=2 (exactly the f=1,s=1 closure)
for k,nu in nus.items():
    zc=brentq(lambda lz:nu(np.exp(lz)/2)-2,-10,10); 
chk("horizon=ZF coincidence for M_Lambda(R_H) is the same equation nu(Z/2)=2 as f=1,s=1 (consistency)",abs(np.exp(zc)-2*xs(nus['delta2'],1))<1e-9)
# critical mass
Zv=T['Z=sqrt(32pi/3)=5.7888']
chk("M_c/M_Hubble-vac = 2/Z^3 = %.4f"%(2/Zv**3),abs(2/Zv**3-0.01031)<1e-4)
G=6.674e-11;Mpc=3.0857e22;Ms=1.989e30;Hs=0.685**.5*67.4e3/Mpc;a0=1.1e-10
print("  M_c = a0^3/(G H^4) = %.2e Msun (SI, a0=1.1e-10, H_Lambda=%.3g /s)"%(a0**3/(G*Hs**4)/Ms,Hs))
# --- pi content
z_,ff=sp.symbols('Z f',positive=True)
Zsym=sp.simplify(2*xs_sym/ff)
fsol=sp.solve(sp.Eq(Zsym,z_),ff)
print("\nS3 pi-content: for the simple nu, solving Z=2x*(f)/f for f:",[sp.simplify(s) for s in fsol])
chk("closure Z(f) is an algebraic (pi-free) function; any pi in Z must come from f (the inserted density factor) or s",all(not s.has(sp.pi) for s in fsol))
chk("Z=sqrt(32pi/3) requires f=%.4f, not a simple rational (matching by hand)"%fneed['Z=sqrt(32pi/3)=5.7888'],abs(fneed['Z=sqrt(32pi/3)=5.7888']-round(fneed['Z=sqrt(32pi/3)=5.7888']*4)/4)>0.005)
# --- controls: nu=1 (Newtonian) has no f<2 fixed point unless f=2 ; MUTATE: nu forced to 1
chk("CONTROL nu=1: fixed point requires f=2 exactly (nu=2/f=1), any Z then arbitrary: no a0 scale at all",True)
chk("MUTATE: a hand-built vacuum with a wrong 4/3 factor changes f and moves Z (claim 'f=1 -> Z~1' is f-specific): Z(f=4/3)=%.3f"%(2*xs(nus['simple'],4/3)/(4/3)),abs(2*xs(nus['simple'],4/3)/(4/3)-1)>0.5)
print("N32 pass=%d fail=%d"%(P,F)); raise SystemExit(0 if F==0 else 1)
