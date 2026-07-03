#!/usr/bin/env python3
"""
D3 v2 -- STABILITY of the causal amplitude kernel (the make-or-break computation).
EOM form-1: a(t) = -[g_N(r)/mu_fw(Q/a0)] rhat ;  Q^2 = <|a|^2>_w (+ tau_j^2 <|adot|^2>_w)
window w = exponential, timescale tau (exact exponential-integrator update; RK4 orbit step).
ANALYTIC first order in tau (exp window mean-lag = tau):
  Q ~= |a|(t) - tau d|a|/dt  =>  delta_a = a_pw*(mu' tau/(mu a0)) d|a|/dt
  dE/dt|sec = m (mu' tau/(mu a0)) <(d|a|/dt)(a.v)>   -- BOTH legs positive for mu'>0 (MOND sign)
  => retarded amplitude kernel PUMPS eccentric orbits. Numerics below test this + measure f(tau/P).
"""
import numpy as np, sys
a0=9.36e-11; GMsun=1.32712e20; AU=1.495979e11; yr=3.15576e7
def mu_fw(x): x=np.maximum(x,1e-300); return (np.sqrt(1+4*x*x)-1)/(2*x)
def dmu_fw(x): return (1/np.sqrt(1+4*x*x) - (np.sqrt(1+4*x*x)-1)/(2*x*x)/2*0) if False else (4*x/np.sqrt(1+4*x*x)*(2*x)-(np.sqrt(1+4*x*x)-1)*2)/(4*x*x)

def run(GM,r0,e,mtau,tj,nP,dtfrac=3000.,warm=5):
    """orbit with memory; returns apo[], peri[], P_est. mtau=None => pointwise."""
    g0=GM/r0**2; A0=np.sqrt(g0*g0+g0*a0)
    vc=np.sqrt(A0*r0); r=np.array([r0,0.]); v=np.array([0.,vc*np.sqrt(1-e)])
    ya=A0*A0; yj=(A0*vc/r0)**2 if tj>0 else 0.0
    P=2*np.pi*np.sqrt(r0/A0); dt=P/dtfrac
    apos=[]; peris=[]; Aprev=A0
    def Qval(): return np.sqrt(max(ya+tj*tj*yj,1e-90))
    def acc(rv,Q):
        rr=np.linalg.norm(rv); g=GM/rr**2
        A=np.sqrt(g*g+g*a0) if mtau is None else g/mu_fw(Q/a0)
        return -A*rv/rr, A
    rdot_prev=np.dot(r,v)/np.linalg.norm(r)
    for i in range(int(nP*dtfrac)):
        Q=Qval()
        # RK4 with Q frozen over the step (dt<<tau checked by convergence)
        k1a,_=acc(r,Q);                 k1r=v
        k2a,_=acc(r+0.5*dt*k1r,Q);      k2r=v+0.5*dt*k1a
        k3a,_=acc(r+0.5*dt*k2r,Q);      k3r=v+0.5*dt*k2a
        k4a,_=acc(r+dt*k3r,Q);          k4r=v+dt*k3a
        r=r+dt/6*(k1r+2*k2r+2*k3r+k4r); v=v+dt/6*(k1a+2*k2a+2*k3a+k4a)
        _,A=acc(r,Q)
        if mtau is not None:
            ex=np.exp(-dt/mtau)
            ya=A*A+(ya-A*A)*ex
            if tj>0:
                adot=(A-Aprev)/dt; yj=adot*adot+(yj-adot*adot)*ex
        Aprev=A
        rr=np.linalg.norm(r); rdot=np.dot(r,v)/rr
        if rdot_prev>0 and rdot<=0: apos.append(rr)
        if rdot_prev<0 and rdot>=0: peris.append(rr)
        rdot_prev=rdot
    return np.array(apos),np.array(peris),P

def slope_per_orbit(seq,skip):
    if len(seq)<skip+4: return float('nan')
    s=seq[skip:]; n=np.arange(len(s))
    return np.polyfit(n,s,1)[0]/np.mean(s)

print("V2 STABILITY -- WB-class orbit M=1.5Msun r0=5kAU (transition regime, x=g_N/a0=%.2f)"%(1.5*GMsun/(5e3*AU)**2/a0))
GM=1.5*GMsun; r0=5e3*AU
# control floor
ap,pe,P=run(GM,r0,0.5,None,0,30)
print(" pointwise control: apo-slope/orbit=%+.2e peri-slope=%+.2e (integrator floor), P=%.0f kyr"%(
      slope_per_orbit(ap,4),slope_per_orbit(pe,4),P/yr/1e3))
# analytic first-order prediction along pointwise orbit, tau/P=0.03
# dE/orbit ~ m*(mu' tau/(mu a0)) * Int (d|a|/dt)(a.v) dt  -> convert to dapo/apo via dE/E ~ dapo scaling
tauP=0.03; mtau=tauP*P
r=np.array([r0,0.]); g0=GM/r0**2; A0=np.sqrt(g0*g0+g0*a0); vc=np.sqrt(A0*r0)
v=np.array([0.,vc*np.sqrt(0.5)]); dt=P/3000.; W=0.; E0=0.5*np.dot(v,v); Aprev=A0; T=0.
for i in range(int(3000)):
    rr=np.linalg.norm(r); g=GM/rr**2; A=np.sqrt(g*g+g*a0)
    x=A/a0; mu=mu_fw(x); dmu=(4*x/np.sqrt(1+4*x*x)*(2*x)-(np.sqrt(1+4*x*x)-1)*2)/(4*x*x)  # d mu/dx
    avec=-A*r/rr
    dAdt=(A-Aprev)/dt if i>0 else 0.
    W+= (dmu*mtau/(mu*a0))*dAdt*np.dot(avec,v)*dt
    k1r,k1v=v,avec
    rm=r+0.5*dt*k1r; vm=v+0.5*dt*k1v; rrm=np.linalg.norm(rm); gm=GM/rrm**2; Am=np.sqrt(gm*gm+gm*a0)
    r=r+dt*vm; v=v+dt*(-Am*rm/rrm); Aprev=A
vchar2=A0*r0
print(" analytic 1st-order pump (tau/P=0.03): W/orbit / (v_c^2) = %+.2e  (positive => energy INPUT)"%(W/vchar2))
# numeric f(tau/P) curve, amplitude-only (tj=0, worst case) and with jerk tj=tau (C1)
print(" numeric drift (apo-slope/orbit), e=0.5:")
print("   tau/P     amp-only      with-jerk(tj=tau)")
for tauP in [0.01,0.03,0.1,0.3,1.0,3.0,10.0]:
    nP=40 if tauP<=1 else int(20+25*tauP)
    ap1,_,_=run(GM,r0,0.5,tauP*P,0.0,nP)
    ap2,_,_=run(GM,r0,0.5,tauP*P,tauP*P,nP)
    sk=max(5,int(3*tauP)+3)
    print("   %-8.2f  %+.3e    %+.3e"%(tauP,slope_per_orbit(ap1,sk),slope_per_orbit(ap2,sk)))
# convergence check at tau/P=0.1
a_lo,_,_=run(GM,r0,0.5,0.1*P,0.0,40,dtfrac=3000.)
a_hi,_,_=run(GM,r0,0.5,0.1*P,0.0,40,dtfrac=6000.)
print(" convergence tau/P=0.1: dtfrac 3000 -> %+.3e ; 6000 -> %+.3e"%(slope_per_orbit(a_lo,6),slope_per_orbit(a_hi,6)))
# eccentricity dependence at tau/P=0.1
for e in [0.2,0.5,0.8]:
    apx,pex,_=run(GM,r0,e,0.1*P,0.0,40)
    print(" e=%.1f tau/P=0.1: apo %+.3e  peri %+.3e"%(e,slope_per_orbit(apx,6),slope_per_orbit(pex,6)))
# deep-MOND galactic-scale check (dSph-like): x<<1, tau/P=0.01
GMd=GMsun*1e9; r0d=5*3.0857e19
apd,ped,Pd=run(GMd,r0d,0.7,None,0,25)
apd2,ped2,_=run(GMd,r0d,0.7,0.01*Pd,0.0,25)
print(" deep-MOND (x=%.3f) e=0.7: ctrl %+.2e ; tau/P=0.01 %+.2e per orbit"%(GMd/r0d**2/a0,slope_per_orbit(apd,4),slope_per_orbit(apd2,4)))
# high-a danger zone (Oort 300 AU, x=700): tau/P=1
GMo=GMsun; r3=300*AU
apo1,_,Po=run(GMo,r3,0.5,None,0,40,dtfrac=6000.)
apo2,_,_=run(GMo,r3,0.5,1.0*Po,0.0,60,dtfrac=6000.)
apo3,_,_=run(GMo,r3,0.5,1.0*Po,1.0*Po,60,dtfrac=6000.)
print(" Oort 300AU (x=%.0f) e=0.5 P=%.1f kyr: ctrl %+.2e ; tau=P amp %+.2e ; +jerk %+.2e"%(
      GMo/r3**2/a0,Po/yr/1e3,slope_per_orbit(apo1,6),slope_per_orbit(apo2,8),slope_per_orbit(apo3,8)))
# form-2 fork: d/dt[mu(|a|)v]=g pointwise, implicit iteration
def form2run(GM,r0,e,nP,dtfrac=4000.):
    g0=GM/r0**2; A0=np.sqrt(g0*g0+g0*a0); vc=np.sqrt(A0*r0)
    r=np.array([r0,0.]); v=np.array([0.,vc*np.sqrt(1-e)])
    P=2*np.pi*np.sqrt(r0/A0); dt=P/dtfrac
    A=A0; p=mu_fw(A/a0)*v; apos=[]; rdp=1.
    for i in range(int(nP*dtfrac)):
        rr=np.linalg.norm(r); g=GM/rr**2
        p=p+dt*(-g*r/rr)
        vn=v
        for _ in range(8):
            An=np.linalg.norm(vn-v)/dt if i>0 else A
            vn=p/mu_fw(max(An,1e-30)/a0)
        v=vn; r=r+dt*v
        rdot=np.dot(r,v)/np.linalg.norm(r)
        if rdp>0 and rdot<=0: apos.append(np.linalg.norm(r))
        rdp=rdot
    return np.array(apos)
f2=form2run(GM,r0,0.5,25); f2b=form2run(GM,r0,0.5,25,dtfrac=8000.)
print(" form-2 fork (pointwise): apo-slope/orbit %+.2e (dt-check %+.2e)"%(slope_per_orbit(f2,4),slope_per_orbit(f2b,4)))
print("EXIT 0"); sys.exit(0)
