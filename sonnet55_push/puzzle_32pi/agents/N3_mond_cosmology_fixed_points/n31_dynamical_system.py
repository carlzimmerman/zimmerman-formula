"""N3-1: exact shell dynamical system with Lambda, point mass M (C1) and Lambda-in-operator (C2). c=1."""
import warnings; warnings.filterwarnings('ignore')
import sympy as sp, numpy as np
from scipy.optimize import brentq
from scipy.integrate import solve_ivp
P=F=0
def chk(name,ok):
    global P,F
    P+=ok; F+=(not ok); print(("PASS " if ok else "FAIL ")+name)
# ---- symbolic
R,GM,a0,H=sp.symbols('R GM a0 H',positive=True)
acc=-sp.sqrt(GM*a0)/R+H**2*R
Rzf=sp.solve(sp.Eq(acc,0),R)
Rzf=[r for r in Rzf if r.is_positive!=False][0]
chk("deep-MOND R_ZF^2 = sqrt(GM a0)/H^2", sp.simplify(Rzf**2-sp.sqrt(GM*a0)/H**2)==0)
lam2=sp.simplify(sp.diff(acc,R).subs(R,Rzf)/H**2)
chk("deep-MOND lambda^2 = 2 H^2", lam2==2)
# dimensions: [GM]=L^3/T^2,[a0]=L/T^2,[H]=1/T
L_,T_=sp.symbols('L T',positive=True)
dim=sp.simplify(((L_**3/T_**2)*(L_/T_**2))**sp.Rational(1,4)*T_)
chk("R_ZF = (GM a0)^(1/4)/H has dimension L",sp.simplify(dim-L_)==0)
Rn=sp.solve(sp.Eq(-GM/R**2+H**2*R,0),R); Rn=[r for r in Rn if r.is_real][0]
chk("Newtonian R_ta^3 = GM/H^2 and lambda^2=3H^2 (control nu=1)",sp.simplify(Rn**3-GM/H**2)==0 and sp.simplify(sp.diff(-GM/R**2+H**2*R,R).subs(R,Rn)/H**2)==3)
# M_c
Mc=a0**3/H**4
chk("deep-MOND valid (x<1) iff GM < a0^3/H^4: x=sqrt(GM H^4/a0^3)",sp.simplify((GM/(a0*Rzf**2))**2-GM*H**4/a0**3)==0)
# ---- numeric general nu
nus={'simple':lambda x:0.5+np.sqrt(0.25+1/x),
     'standard':lambda x:np.sqrt((1+np.sqrt(1+4/x**2))/2),
     'rar_d1':lambda x:1/(1-np.exp(-np.sqrt(x))),
     'delta2':lambda x:(1-np.exp(-x))**-0.5,
     'delta0.5':lambda x:(1-np.exp(-x**0.25))**-2.0}
def fp(nu,gm,a0v=1.0,Hv=1.0):
    f=lambda r: nu(gm/(a0v*r*r))*gm/(r*r)-Hv**2*r
    lo=0.3*min(gm**(1/3),gm**0.25); hi=3*max(gm**(1/3),gm**0.25)
    return brentq(f,lo,hi,xtol=1e-14,rtol=1e-13)
def lam2num(nu,gm,a0v=1.0,Hv=1.0):
    r=fp(nu,gm,a0v,Hv); h=1e-5*r
    g=lambda rr: nu(gm/(a0v*rr*rr))*gm/(rr*rr)
    return (Hv**2-(g(r+h)-g(r-h))/(2*h))
ok=True; lo,hi=9,0; uniq=True
for name,nu in nus.items():
    for gm in 10.0**np.arange(-8,9,0.5):
        r=fp(nu,gm); l=lam2num(nu,gm)
        ok&=(l>0); lo=min(lo,l); hi=max(hi,l)
        # uniqueness: sign changes of force on a fine grid
        rr=np.logspace(np.log10(r)-4,np.log10(r)+4,4000)
        s=np.sign(nu(gm/rr**2)*gm/rr**2-rr); uniq&=(np.sum(np.diff(s)!=0)==1)
chk("S1 unique fixed point, all nu, GM in 1e-8..1e8 (a0=H=1)",uniq)
chk("S2 always unstable: lambda^2>0 for all nu,M (%.4f..%.4f)"%(lo,hi),ok)
chk("S2 lambda^2/H^2 within [2,3]",lo>=2-1e-4 and hi<=3+1e-4)
# deep limit ->2 , Newtonian limit ->3
chk("deep-MOND limit lambda^2->2 (simple nu, GM=1e-16)",abs(lam2num(nus['simple'],1e-16)-2)<1e-3)
chk("Newtonian limit lambda^2->3 (simple nu, GM=1e18)",abs(lam2num(nus['simple'],1e18)-3)<1e-3)
# fixed point formula at deep limit
gm=1e-10; chk("numeric R_ZF matches sqrt(GM a0)^(1/2)/H deep MOND",abs(fp(nus['simple'],gm)/np.sqrt(np.sqrt(gm))-1)<1e-3)
# AQUAL consistency: mu(g/a0) g = g_N with mu=1/nu(x)-type inverse on spherical source
for name,nu in nus.items():
    x=np.logspace(-3,3,50); g=nu(x)*x   # g/a0
    # mu(y) defined by mu(y) y = x ; with y=g/a0 -> mu=x/y=1/nu
    chk("AQUAL spherical algebraic inversion consistent (%s): mu=1/nu in (0,1], monotone"%name,np.all((1/nu(x)<=1)&(1/nu(x)>0)) and np.all(np.diff(g)>0))
# ---- ODE growth rate vs analytic eigenvalue (simple nu, GM=1)
nu=nus['simple']; gm=1.0; r0=fp(nu,gm); l=np.sqrt(lam2num(nu,gm))
def rhs(t,y): return [y[1], -nu(gm/(y[0]**2))*gm/y[0]**2+y[0]]
eps=1e-7*r0
sol=solve_ivp(rhs,[0,6],[r0+eps,0],rtol=1e-12,atol=1e-14,dense_output=True)
t1,t2=3.0,5.0; d1=sol.sol(t1)[0]-r0; d2=sol.sol(t2)[0]-r0
rate=np.log(d2/d1)/(t2-t1)
chk("ODE growth rate %.5f = analytic %.5f"%(rate,l),abs(rate/l-1)<2e-3)
sol=solve_ivp(rhs,[0,6],[r0-eps,0],rtol=1e-12,atol=1e-14,dense_output=True)
chk("inward perturbation collapses (R decreases)",sol.sol(6)[0]<r0-eps)
# ---- mutation: Lambda with wrong sign -> centre, 'always unstable' would be false
# MUTATE: replace the Lambda term H^2 R by a constant outward acceleration (wrong R-dependence): claim lambda^2 in [2,3] must then fail
nu=nus['simple']; gm=1.0; Hc=1.0
r=brentq(lambda rr: nu(gm/rr**2)*gm/rr**2-Hc,1e-8,1e8); h=1e-6
g=lambda rr: nu(gm/rr**2)*gm/rr**2
lm=-(g(r+h)-g(r-h))/(2*h)
chk("MUTATE: constant outward force gives lambda^2=%.3f outside [2,3] (so the [2,3] claim is specific to Lambda ~ R)"%lm, not (2-1e-3<=lm<=3+1e-3))
# MUTATE: attractive Lambda has no zero-force radius
rr=np.logspace(-3,3,300)
chk("MUTATE: attractive Lambda (-H^2 R) has no fixed point",np.all(-nu(1/rr**2)/rr**2-rr<0))
# ---- C2: Lambda inside the MOND operator
gN=lambda r,gm:gm/r**2-r
g2=lambda r,gm:nus['simple'](np.abs(gN(r,gm))/1.0)*gN(r,gm)
gm=1.0; rN=gm**(1/3)
chk("C2 fixed point equals the Newtonian R^3=GM/H^2",abs(g2(rN*(1+1e-12),gm))<1e-5 and abs(g2(rN*(1-1e-12),gm))<1e-5)
# cusp exponent: delta'' ~ +C sign(delta) sqrt|delta|
ds=np.array([1e-8,1e-6,1e-4]); acc2=np.array([-g2(rN+d,gm) for d in ds])  # R''=-g_total
slope=np.polyfit(np.log(ds),np.log(np.abs(acc2)),1)[0]
chk("C2 near-fixed-point force ~ |delta|^0.5 (slope %.3f): non-analytic, no linearisation"%slope,abs(slope-0.5)<0.02)
chk("C2 beyond R_N acceleration is repulsive, inside attractive (still unstable)",(-g2(rN*1.01,gm))>0 and (-g2(rN*0.99,gm))<0)
# ---- MOND turnaround table (isolated point mass, illustration only; SI)
Gs=6.674e-11;Ms=1.989e30;Mpc=3.0857e22;H=0.685**0.5*67.4e3/Mpc;a0v=1.1e-10
for Mm in (1e11,2e12,1e14):
    gm=Gs*Mm*Ms; Rn=(gm/H**2)**(1/3)/Mpc; Rm=(gm*a0v)**0.25/H/Mpc
    print("M=%.0e Msun: Newtonian R_ZF=%.2f Mpc, deep-MOND R_ZF=%.2f Mpc, g_N/a0 at MOND R_ZF=%.2e"%(Mm,Rn,Rm,gm/(Rm*Mpc)**2/a0v))
print("N31 pass=%d fail=%d"%(P,F)); raise SystemExit(0 if F==0 else 1)
