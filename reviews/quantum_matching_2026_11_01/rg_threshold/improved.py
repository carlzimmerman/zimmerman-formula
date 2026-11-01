"""Reduced RG/complete-one-loop-threshold interface; finite two-loop matching omitted.

evaluate(X0,e,eta,scheme) exposes U,F in the original reference X0 coordinate.
The native angular coefficient F is its RG wavefunction part, not a matched
finite kinetic threshold. `rg2log` adds reduced-CS-determined scale logs around
the central field-dependent matching scale; its finite two-loop remainder is
unknown and is NOT fitted or declared zero in the physical theory.
"""
import sys
from pathlib import Path
import mpmath as mp
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'reviews/three_priorities_2026_11_01/spectrum_pressure'))
from pressure_scan import cw as cw_f1

def gammas(h,l,g,order=2):
    L=16*mp.pi**2
    one=[12*h*h,h*h+mp.mpf(21)/10*l*l-10*g*g,mp.mpf(21)/20*l*l-10*g*g]
    two=[-24*h**4-mp.mpf(252)/5*h*h*l*l+240*g*g*h*h,
         -13*h**4-mp.mpf(21)/5*h*h*l*l-mp.mpf(1323)/200*l**4+21*g*g*l*l+50*g**4,
         -mp.mpf(21)/10*h*h*l*l-mp.mpf(441)/100*l**4+mp.mpf(21)/2*g*g*l*l+50*g**4]
    return [one[i]/L+(two[i]/L**2 if order==2 else 0) for i in range(3)]

def beta(c,order=2):
    h,l,g,f=c;gx,ga,gb=gammas(h,l,g,order);L=16*mp.pi**2
    return [h*(gx+2*ga),l*(gb+2*ga),-5*g**3/L+(g**3*(150*g*g-10*h*h-mp.mpf(63)/2*l*l)/L**2 if order==2 else 0),f*gx]

def flow(e,t,steps=32,order=2):
    e=mp.mpf(e);y=[e,e,mp.sqrt(mp.mpf(29)/200)*e,mp.mpf(1),mp.mpf(0),mp.mpf(0)]
    dt=t/steps
    def rhs(z):
        h,l,g,f=z[:4];gx,ga,gb=gammas(h,l,g,order);ge=(l*l*gx+30*h*h*gb)/(l*l+30*h*h)
        return beta(z[:4],order)+[-gx,-ge]
    def add(z,w,a):return [v+a*u for v,u in zip(z,w)]
    for _ in range(steps):
        k1=rhs(y);k2=rhs(add(y,k1,dt/2));k3=rhs(add(y,k2,dt/2));k4=rhs(add(y,k3,dt))
        y=[v+dt*(a+2*b+2*c+d)/6 for v,a,b,c,d in zip(y,k1,k2,k3,k4)]
    return y

def tree(c):
    h,l,g,f=c;return f*f*l*l/(l*l+30*h*h)

def C1(c):
    h,l,g,f=c;return 6*f*f*h*h*l*l*(29*l*l-200*g*g)/(l*l+30*h*h)**2/(32*mp.pi**2)

def C2(c):
    h,l,g,f=c
    total=gammas(h,l,g,2);one=gammas(h,l,g,1)
    gx,ga,gb=[a-b for a,b in zip(total,one)]
    return 2*tree(c)*(l*l*gx+30*h*h*gb)/(l*l+30*h*h)

def threshold(X,c,Q):
    h,l,g,f=c
    # All mass squares scale with f; the singlet threshold cancels exactly.
    val=f*f*cw_f1(X/mp.sqrt(f),h,l,g)
    return val-mp.log(Q/mp.sqrt(f))*C1(c)

def reduced_D1_threshold(X,c,Q):
    b=beta(c,1);gx=gammas(*c[:3],order=1)[0]
    return mp.diff(lambda z:threshold(X*(1-z*gx),[v+z*w for v,w in zip(c,b)],Q),0)

def D1C1(c):
    b=beta(c,1)
    return mp.diff(lambda z:C1([v+z*w for v,w in zip(c,b)]),0)

def evaluate(X0,e,eta=1,scheme='rg2log',steps=32,details=False):
    X0,e,eta=map(mp.mpf,(X0,e,eta));c0=[e,e,mp.sqrt(mp.mpf(29)/200)*e,mp.mpf(1)]
    D0=31*e*e;cc=e/31;Qm=mp.sqrt(cc+(e*X0)**2)
    if scheme=='fixed':
        out={'U':tree(c0)+threshold(X0,c0,mp.mpf(1)),'F':D0/e**2*X0**2,
             'Q':mp.mpf(1),'Qm':Qm,'U2log':mp.mpf(0),'field_transport_error':mp.mpf(0),
             'couplings':c0,'X_running':X0,'T_running':mp.sqrt(D0)/e*X0}
        return out
    if scheme not in ('rg1','rg2','rg2log'):raise ValueError(scheme)
    Q=eta*Qm;t=mp.log(Q);order=1 if scheme=='rg1' else 2
    vals=flow(e,t,steps,order);c=vals[:4];X=X0*mp.exp(vals[4]);h,l,g,f=c
    T=mp.sqrt(l*l+30*h*h)/l*X
    implied_T=mp.sqrt(D0)/e*X0*mp.exp(vals[5])
    correction=mp.mpf(0)
    if scheme=='rg2log' and eta!=1:
        delta=mp.log(eta)
        correction=-delta*(reduced_D1_threshold(X,c,Qm)+C2(c))+delta**2*D1C1(c)/2
    out={'U':tree(c)+threshold(X,c,Q)+correction,'F':T*T,'Q':Q,'Qm':Qm,'U2log':correction,
         'field_transport_error':T/implied_T-1,'couplings':c,'X_running':X,'T_running':T,
         'critical_ratio_drift':g*g/(mp.mpf(29)/200*l*l)-1}
    return out

def profile(X0,e,eta=1,scheme='rg2log',steps=32):
    """Return U,Us,Uss,F,a,a' using direct mpmath reference-log derivatives."""
    out=evaluate(X0,e,eta,scheme,steps)
    U=lambda s:evaluate(mp.mpf(X0)*mp.exp(s),e,eta,scheme,steps)['U']
    LF=lambda s:mp.log(evaluate(mp.mpf(X0)*mp.exp(s),e,eta,scheme,steps)['F'])
    out.update(U_s=mp.diff(U,0),U_ss=mp.diff(U,0,2),a=mp.diff(LF,0),a_prime=mp.diff(LF,0,2))
    return out
