#!/usr/bin/env python3
r"""
VERIFY (adversarial, independent) -- LANE K planetary kernel calc.
Re-derives from scratch, with NO import from laneK, the two load-bearing claims the tasking
names: (V1) the a0/2 landmine arithmetic and its per-planet exclusion; (V2) that the constant
sunward a0/2 is a GENUINE non-absorbable secular residual, NOT a piece that hides in a GM
rescaling ("DC-into-GM absorption"). Plus independent re-checks of (V3) the cut boundary
values / pure-phase claim, (V4) the secular-drift orbital-mechanics factor, (V5) that the
first-moment (constitutive) closure REPRODUCES the a0/2 tail while a bound orbit's operator
spectrum cannot feed the positive kernel argument. Both footings. Exit 0 iff all pass.
"""
import numpy as np, sympy as sp
from scipy.integrate import solve_ivp
np.seterr(all="ignore")
OK=True
def ck(n,c):
    global OK; print(f"   [{'PASS' if c else 'FAIL'}] {n}");  OK = OK and c

C=2.99792458e8; GMsun=1.32712440018e20; YR=3.15576e7
A0=dict(canon=9.362e-11, alt=1.130e-10)
# per-planet CONSTANT-radial-accel bounds [m/s^2] (laneR from Fienga-Minazzoli 2024 Table 10)
DGB={"Mercury":4.6e-14,"Venus":8.0e-14,"Earth":8.7e-15,"Mars":1.4e-15,"Jupiter":5.6e-13,"Saturn":7.0e-15}
R  ={"Mercury":5.7909e10,"Venus":1.08209e11,"Earth":1.49598e11,"Mars":2.27939e11,"Jupiter":7.7857e11,"Saturn":1.43353e12}

print("# V1  a0/2 landmine arithmetic + per-planet exclusion (independent)")
for f,a0 in A0.items():
    dg=a0/2
    exc={p:dg/DGB[p] for p in DGB}
    print(f"   {f}: a0/2 = {dg:.3e} m/s^2 ; excl Mercury {exc['Mercury']:.0f}x  Mars {exc['Mars']:.0f}x  Saturn {exc['Saturn']:.0f}x")
    ck(f"{f}: a0/2 = a0/2 (trivial) and Mars excl in [3e4,4.2e4]", 3.0e4 < exc['Mars'] < 4.2e4)
    ck(f"{f}: every planet excludes a0/2 by >80x", all(v>80 for v in exc.values()))

print("# V2  is the constant sunward a0/2 absorbable into a GM rescaling?  (the DC-absorption test)")
# A constant radial A adds to g=GM/r^2. Absorb into GM_eff(r)=GM + A r^2 -> the required FRACTIONAL
# GM shift is A r^2/GM, which must be r-INDEPENDENT for a genuine absorption. Show it is not.
for f,a0 in A0.items():
    A=a0/2
    frac={p: A*R[p]**2/GMsun for p in R}
    spread=max(frac.values())/min(frac.values())
    print(f"   {f}: fractional GM shift A r^2/GM  Mercury {frac['Mercury']:.2e}  Saturn {frac['Saturn']:.2e}  spread {spread:.0f}x")
    # if it were absorbable the spread would be ~1; it is ~(r_Sat/r_Merc)^2
    ck(f"{f}: required GM shift is r-DEPENDENT (spread = (r_max/r_min)^2, not 1) -> NOT GM-absorbable",
       abs(spread - (R['Saturn']/R['Mercury'])**2) < 1.0)
# Independent: a constant radial accel produces a NONZERO secular perihelion precession (Gauss),
# so it is observable, not a coordinate/GM artifact. Toy: integrate Kepler + constant sunward A,
# measure apsidal precession rate; confirm != 0 and scales linearly in A.
def peri_rate(A, GM=1.0, r0=1.0, e=0.2, norbit=300):
    # start at perihelion of an e-orbit
    a=r0/(1-e); rp=a*(1-e); vp=np.sqrt(GM*(1+e)/(a*(1-e)))
    def rhs(t,y):
        x,yy,vx,vy=y; r=np.hypot(x,yy)
        gx,gy=-GM*x/r**3 - A*x/r, -GM*yy/r**3 - A*yy/r   # extra CONSTANT sunward A
        return [vx,vy,gx,gy]
    T=2*np.pi/np.sqrt(GM/a**3)
    sol=solve_ivp(rhs,[0,norbit*T],[rp,0,0,vp],rtol=1e-11,atol=1e-13,dense_output=True)
    tt=np.linspace(0,norbit*T,200000); Y=sol.sol(tt)
    r=np.hypot(Y[0],Y[1]); 
    # Laplace-Runge-Lenz direction ~ perihelion longitude; track via angle at min-r passages
    # simpler: eccentricity vector e_vec = (v x L)/GM - r_hat
    vx,vy=Y[2],Y[3]; x,yy=Y[0],Y[1]
    L=x*vy-yy*vx
    ex=(vy*L)/GM - x/r; ey=(-vx*L)/GM - yy/r
    ang=np.unwrap(np.arctan2(ey,ex))
    return np.polyfit(tt,ang,1)[0]   # dvarpi/dt
r1=peri_rate(1e-3); r2=peri_rate(2e-3); r0=peri_rate(0.0)
print(f"   perihelion precession: A=0 -> {r0:+.2e},  A=1e-3 -> {r1:+.2e},  A=2e-3 -> {r2:+.2e} (code units)")
ck("constant sunward A gives NONZERO secular perihelion precession (=> observable, not GM-absorbable)",
   abs(r1)>1e-6)
ck("precession scales ~linearly in A (2e-3 ~ 2x the 1e-3 rate, <5%)", abs((r2-r0)/(r1-r0) - 2) < 0.05)

print("# V3  cut boundary values: pure phase |K|=1, ReK=sqrt(1-1/4W^2), ImK=1/2W (independent sympy+numeric)")
W=sp.symbols('W',positive=True)
zc=-W**2  # argument on the cut fed by a real harmonic omega, W=c omega/a0
Kdef=(sp.sqrt(1+4*zc)-1)/(2*sp.sqrt(zc))  # principal; sqrt(neg) -> i branch
# numeric boundary value K(-W^2 + i0):
Kf=sp.lambdify(sp.symbols('z'),(sp.sqrt(1+4*sp.symbols('z'))-1)/(2*sp.sqrt(sp.symbols('z'))),"numpy")
maxe=0.0
for wv in [0.6,1.0,3.7,55.0,6e5]:
    k=complex(Kf(-wv**2+1e-30j))
    maxe=max(maxe, abs(abs(k)**2-1), abs(k.real-np.sqrt(1-1/(4*wv**2))), abs(k.imag-1/(2*wv)))
print(f"   max deviation over W in [0.6, 6e5] from (|K|^2=1, Re=sqrt(1-1/4W^2), Im=1/2W): {maxe:.2e}")
ck("pure-phase cut identities hold numerically to <1e-9", maxe<1e-9)

print("# V4  secular-drift orbital-mechanics factor d ln r/dt = 2 omega (f_t/g_N) (independent ODE)")
def dlnr(eps,norbit=200,fit0=20,GM=1.0,r0=1.0):
    om0=np.sqrt(GM/r0**3)
    def rhs(t,y):
        x,yy,vx,vy=y; r=np.hypot(x,yy); gN=GM/r**2; v=np.hypot(vx,vy)
        return [vx,vy,-GM*x/r**3+eps*gN*vx/v,-GM*yy/r**3+eps*gN*vy/v]
    T=2*np.pi/om0
    s=solve_ivp(rhs,[0,norbit*T],[r0,0,0,np.sqrt(GM/r0)],rtol=1e-11,atol=1e-13,dense_output=True)
    tt=np.linspace(fit0*T,norbit*T,8000)
    return np.polyfit(tt,np.log(np.hypot(*s.sol(tt)[:2])),1)[0],om0
b,_=dlnr(0.0); p,om0=dlnr(1e-6)
print(f"   eps=1e-6: (measured-baseline)/pred = {(p-b)/(2e-6*om0):.4f}")
ck("orbital-mechanics factor recovered to <1% in linear regime", abs((p-b)/(2e-6*om0)-1)<0.01)
# => with ImK=1/2W=a0/(2c omega) in place of eps: d ln r/dt = 2 omega a0/(2c omega) = a0/c
for f,a0 in A0.items():
    print(f"   {f}: a0/c = {a0/C:.3e}/s = {a0/C*YR:.3e}/yr  vs MESSENGER Gdot/G 4e-14/yr -> x{(a0/C*YR)/4e-14:.0f}")
    ck(f"{f}: drift a0/c exceeds MESSENGER Gdot/G by >200x", (a0/C*YR)/4e-14 > 200)

print("# V5  first-moment (constitutive) closure REPRODUCES the a0/2 tail; bound orbit spectrum cannot")
# constitutive: k = mu(|a|/a0), nu = 1/mu; anomaly = (nu-1) g_bar ; deep-Newton nu-1 -> a0/(2 g_bar)
def mu(x): return (np.sqrt(1+4*x*x)-1)/(2*x)     # mu(x)=K(x^2)
for f,a0 in A0.items():
    gN=GMsun/R['Saturn']**2; y=gN/a0
    nu=1.0/mu(y); anom=(nu-1)*gN
    print(f"   {f} Saturn: y={y:.2e}  (nu-1)g_bar = {anom:.3e}  vs a0/2 = {a0/2:.3e}  ratio {anom/(a0/2):.4f}")
    ck(f"{f}: constitutive anomaly -> a0/2 to <0.1% (the tail IS reproduced by the first-moment closure)",
       abs(anom/(a0/2)-1)<1e-3)
# operator/spectral side: a circular orbit feeds Box_u only eigenvalues {0, -(gamma omega)^2} <= 0;
# the tail lives at z=+(a/a0)^2 > 0 -> unreachable. Symbolic witness:
tau,om,bet=sp.symbols('tau omega beta',positive=True); g=1/sp.sqrt(1-bet**2)
uc=sp.Matrix([g,g*bet*sp.cos(g*om*tau),g*bet*sp.sin(g*om*tau),0])
Bu=sp.diff(uc,tau,2)
ck("circular u: Box_u eigenvalue on spatial part = -(gamma omega)^2 < 0 (no positive argument fed)",
   sp.simplify(Bu[1]/uc[1] + (g*om)**2)==0)
ck("circular u: Box_u u_time = 0 (DC sector; K(0)=0)", sp.simplify(Bu[0])==0)

print("="*90)
print(f" VERIFY RESULT: {'ALL PASS' if OK else 'A CHECK FAILED'}")
print("="*90)
import sys; sys.exit(0 if OK else 1)
