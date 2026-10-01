"""N2: existence thresholds of MOND-type static spherical fields in a de Sitter static patch.
Units: a0 = 1, H = Z, L = 1/Z, c = G = 1.  Verifies the declared menu hash first."""
import hashlib, sys, numpy as np
from scipy.optimize import brentq
P=F=0
def chk(name,cond):
    global P,F
    P+=bool(cond); F+=(not cond); print(("PASS " if cond else "FAIL ")+name)
h=hashlib.sha256(open('n00_menu_declared.txt','rb').read()).hexdigest()
chk("menu hash matches declared "+h[:12], h==open('n00_menu_declared.sha256').read().split()[0])

# ---- families: S(g)=mu(|g|)g, g signed, domain dom=(gmin,gmax)
def odd(mu): return lambda g: mu(abs(g))*g
def mun(n): return lambda y: y/(1+y**n)**(1/n)
def OR(N): return lambda y: 1-(1+y/N)**(-N)
def rar_S():
    G=lambda s: s/(1-np.exp(-np.sqrt(s)))          # g as function of s>0
    def S(g):
        g=abs(g)
        return brentq(lambda s:G(s)-g,0.1*min(g,g*g),10*max(g,g*g)) if g>0 else 0.0
    return S
FAM={}
FAM['simple']=(odd(mun(1)),(-np.inf,np.inf))
FAM['standard']=(odd(mun(2)),(-np.inf,np.inf))
for n in (1.5,3,4,6): FAM[f'mu_n={n}']=(odd(mun(n)),(-np.inf,np.inf))
FAM['exponential']=(odd(lambda y:1-np.exp(-y)),(-np.inf,np.inf))
FAM['OR N=2']=(odd(OR(2)),(-np.inf,np.inf))
FAM['OR N=3']=(odd(OR(3)),(-np.inf,np.inf))
_r=rar_S(); FAM['RAR']=((lambda g: np.sign(g)*_r(g)),(-np.inf,np.inf))
FAM['DBI-BI']=((lambda g: g/np.sqrt(1-g*g)),(-1,1))
FAM['cubic Gal c=+1']=((lambda g: g+g*g),(-np.inf,np.inf))
FAM['cubic Gal c=-1']=((lambda g: g-g*g),(-np.inf,np.inf))

def fold_info(S,dom):
    """scan signed g; return (monotone?, list of turning points (g,s))"""
    lo=max(dom[0],-1e3)*0.999999 if np.isfinite(dom[0]) else -1e3
    hi=min(dom[1],1e3)*0.999999 if np.isfinite(dom[1]) else 1e3
    # log-symmetric grid
    pos=np.geomspace(1e-6,hi,6000); neg=-np.geomspace(1e-6,-lo,6000)[::-1]
    g=np.concatenate([neg,[0.0],pos]); s=np.array([S(x) for x in g])
    d=np.diff(s)
    tol=1e-9*np.maximum(1,np.abs(s[1:]))
    d=np.where(np.abs(d)<tol,1e-30,d)   # kill root-finder noise
    turn=[(g[i+1],s[i+1]) for i in range(1,len(d)) if d[i-1]*d[i]<0]
    return bool(np.all(d>0)),turn,(s.min(),s.max())

RES={}
print("\n== T1/T2: fold and source range ==")
for k,(S,dom) in FAM.items():
    mono,turn,rng=fold_info(S,dom); RES[k]=(mono,turn,rng)
    print(f"{k:16s} monotone={mono}  turns={[(round(a,4),round(b,4)) for a,b in turn]}")
for k in ['simple','standard','mu_n=1.5','mu_n=3','mu_n=4','mu_n=6','exponential','OR N=2','OR N=3','RAR','DBI-BI']:
    chk(f"{k}: S monotone on signed g (no fold, regular solution for every source s)",RES[k][0])
ga=RES['cubic Gal c=+1'][1]; gb=RES['cubic Gal c=-1'][1]
chk("Galileon c=+1: fold at g=-1/2, s=-1/4 (analytic), repulsive side",len(ga)==1 and abs(ga[0][0]+0.5)<1e-2 and abs(ga[0][1]+0.25)<1e-3)
chk("Galileon c=-1: fold at g=+1/2, s=+1/4 (analytic), attractive side",len(gb)==1 and abs(gb[0][0]-0.5)<1e-2 and abs(gb[0][1]-0.25)<1e-3)
# control: planted non-monotone S must be flagged
Sbad=lambda g: g*(1-0.3*np.exp(-(np.log(abs(g)+1e-9)-0)**2))*1.0 - 0.6*g*np.exp(-g*g)*np.exp(-g*g)*5*np.sign(1)
mono,turn,_=fold_info(lambda g: g-1.0*g/(1+ (g-1.5)**2*1.0)*1.5 ,(-np.inf,np.inf))
chk("CONTROL planted non-monotone S is flagged (would FAIL if detector were blind)",not mono)

print("\n== P1 profile scans: does a regular solution exist for all r in (0,L]?  (a0=1,H=Z,L=1/Z) ==")
def rng_of(k): return RES[k][2]
def exists(k,Z,M,lam_sign=+1,n=4000):
    lo,hi=rng_of(k); Sdom=FAM[k][1]
    L=1/Z; r=np.geomspace(1e-4*L,L,n)
    s=M/r**2-lam_sign*Z**2*r
    # range of S on the signed axis (scan result), DBI and monotone families: full line
    if k=='DBI-BI': ok=np.ones_like(s,bool)
    elif RES[k][0]: ok=np.ones_like(s,bool)
    else: ok=(s>=lo)&(s<=hi) if False else None
    if ok is None:
        t=RES[k][1][0][1]
        if 'c=+1' in k: ok=(s>=t)       # fold at s=-1/4: all s>=-1/4 fine
        else: ok=(s<=t)
    return bool(ok.all()), (None if ok.all() else float(r[~ok][0] if 'c=+1' in k else r[~ok][-1]))
for Z in (0.1,0.25,1,5.7888):
    row=[]
    for k in ('standard','OR N=2','RAR','DBI-BI','cubic Gal c=+1','cubic Gal c=-1'):
        ok,rf=exists(k,Z,0.0); row.append(f"{k}:{'OK' if ok else 'fail@r/L=%.4g'%(rf*Z)}")
    print(f"Z={Z:<7}",'  '.join(row))
# analytic check r_fail/L = 1/(4Z) vacuum, c=+1
ok,rf=exists('cubic Gal c=+1',5.7888,0.0)
chk("Galileon c=+1 vacuum: r_fail/L = 1/(4Z) (to grid)",abs(rf*5.7888-1/(4*5.7888))/(1/(4*5.7888))<2e-3)
chk("Galileon c=+1 vacuum global solution exists iff Z<=1/4 (a0>=4H): Z=0.25 ok, Z=0.26 fails",exists('cubic Gal c=+1',0.2499,0)[0] and not exists('cubic Gal c=+1',0.26,0)[0])
chk("MUTATE: flipping Lambda to attractive removes the c=+1 fold",exists('cubic Gal c=+1',5.7888,0.0,lam_sign=-1)[0])
chk("c=-1 vacuum (repulsive s<0, fold at s=+1/4) never fails; with mass fails at small r, r_fail^2 ~ 4M/a0",exists('cubic Gal c=-1',5.7888,0.0)[0] and not exists('cubic Gal c=-1',5.7888,1e-3)[0])
ok,rf=exists('cubic Gal c=-1',5.7888,1e-3,n=200000)
rr=brentq(lambda r:1e-3/r**2-5.7888**2*r-0.25,1e-4,1.0)
chk("  c=-1 r_fail equals the root of M/r^2 - Z^2 r = 1/4 (%.5g vs %.5g); for Z->0 it is sqrt(4M/a0)"%(rf,rr),abs(rf/rr-1)<2e-3)
for k in ('standard','simple','OR N=2','RAR','DBI-BI'):
    chk(f"{k}: regular solution to the horizon for all tested (Z,M)",all(exists(k,Z,M)[0] for Z in (0.1,1,5.7888,30) for M in (0,1e-6,1e-3,1)))

print("\n== T4: y_h=1  => Z_T4 = S(1) = mu(1);   T9: transition centre (max dln mu/dln y) ==")
T4={};T9={}
for k in ['simple','standard','mu_n=1.5','mu_n=3','mu_n=4','mu_n=6','exponential','OR N=2','OR N=3','RAR']:
    S=FAM[k][0]; T4[k]=S(1.0)
    y=np.geomspace(1e-3,1e3,4001); mu=np.array([S(v)/v for v in y]); dl=np.gradient(np.log(mu),np.log(y))
    interior=bool(np.any(np.diff(dl)[1:-1]>1e-9))   # any rise => interior extremum of dln mu/dln y
    T9[k]=None if not interior else 'interior'
    print(f"{k:12s} Z_T4={T4[k]:.4f}  dlnmu/dlny monotone decreasing 1->0 (T9 transition centre degenerate={not interior})")
    chk("T9 (declared 'transition centre' extremum) is degenerate for all families: extremum sits on the boundary",all(v is None for v in T9.values()))
chk("simple mu(1)=1/2, standard 1/sqrt2 (closed forms)",abs(T4['simple']-.5)<1e-12 and abs(T4['standard']-2**-.5)<1e-12)
print("T6: Z=sqrt3 for M_c=M_Nariai (M_c=L/Z^3, M_N=L/(3sqrt3))")
chk("T6 algebra: sqrt(M/a0)=(M L^2)^(1/3) => M=L/Z^3 ; M_c/M_N=3sqrt3/Z^3=%.4f at Z=5.7888"%(3*3**.5/5.7888**3),abs(3*3**.5/5.7888**3-0.0268)<1e-3)

print("\n== T7 DBI-BI speed limit and T5 observer transition ==")
Zs=np.array([0.1,1,5.7888,100,1e4]); gh=Zs/np.sqrt(1+Zs**2)
print("DBI-BI vacuum horizon field g_h/a0:",np.round(gh,6)," (limit 1, never reached)")
chk("DBI-BI g_h<1 for every Z (no speed-limit breakdown; also no MOND regime: g->a0 = constant force)",np.all(gh<1))
print("T5 r_t/L = 1/sqrt(1+Z^2) at Z=5.7888:",1/np.sqrt(1+5.7888**2))

print("\n== T8 FRW dS attractor, quasi-static perturbation: delta'' + 2H delta' = 4piG rho delta / S'(g) ==")
from scipy.integrate import solve_ivp
def growth(k,y0,Om0=0.3,amax=1e4):
    S=FAM[k][0]; 
    def dS(g): e=1e-6*g; return (S(g+e)-S(g-e))/(2*e)
    def Sinv(s): return brentq(lambda g:S(g)-s,1e-14,1e14)
    # a=1 today, Omega_m(a)=Om0/a^3/(Om0/a^3+1-Om0); y(a)=y0*rho(a)a/(rho0) (physical size ~a)
    def rhs(N,u):
        a=np.exp(N); E2=Om0/a**3+1-Om0; Om=Om0/a**3/E2
        s=y0*a**-2; g=Sinv(s); q=1.5*Om/dS(g)
        d,dp=u; return [dp,-(2+0.5*(-3*Om))*dp+q*d]  # d''(lna)+(2+dlnH/dlna)d'=q d ; dlnH/dlna=-1.5Om
    sol=solve_ivp(rhs,[0,np.log(amax)],[1,0],rtol=1e-8,atol=1e-12,dense_output=True)
    return sol
for k in ('standard','RAR'):
    for y0 in (0.1,10.0):
        sol=growth(k,y0); d1,d2=sol.sol(np.log(1e3))[0],sol.sol(np.log(1e4))[0]
        print(f"{k:9s} y0={y0:<5} delta(a=1e3)={d1:.4g} delta(a=1e4)={d2:.4g}  ratio={d2/d1:.5f}")
        chk(f"{k} y0={y0}: delta tends to a constant in the dS attractor (ratio-1<1e-2)",abs(d2/d1-1)<1e-2)
chk("T8 k-essence fixed point needs P_X=0 (mu=F'=0) at X*>0; every monotone family has mu>0: none",all(T4[k]>0 for k in T4))

print("\n== Decoy control (declared recipe) ==")
rng=np.random.default_rng(32)
targets=np.array([5.7888,5.1962,6.0,6.2832]); fac=np.array([.25,.5,1,2,4])
def hit(v): 
    cand=np.concatenate([fac*v,fac/v]); return np.any(np.abs(cand[:,None]/targets[None,:]-1)<0.10)
vals=list(T4.values())+[np.sqrt(3),0.25,4.0]
actual=[ (n,hit(v)) for n,v in zip(list(T4)+['T6','Gal','Gal4'],vals)]
nh=sum(h for _,h in actual); print("menu values:",np.round(vals,3)); print("hits (within 10% of any target after normalisation factors):",nh,"of",len(vals),[n for n,h in actual if h])
dec=np.array([hit(np.exp(rng.uniform(np.log(0.2),np.log(30)))) for _ in range(20000)])
print("decoy hit rate (log-uniform [0.2,30]):",dec.mean())
chk("decoy hit rate is large (>40%): a hit from this menu is uninformative",dec.mean()>0.40)
chk("MUTATE decoy without normalisation-factor freedom: rate drops (control of the inflation)",np.mean([np.any(np.abs(np.exp(rng.uniform(np.log(.2),np.log(30)))/targets-1)<.1) for _ in range(20000)])<dec.mean())
print(f"\nPASS {P} FAIL {F}"); sys.exit(0 if F==0 else 1)
