#!/usr/bin/env python3
"""
D3 v4 -- retarded-vs-advanced certification of the eccentric-orbit pump.
Two-pass: (1) integrate POINTWISE orbit, store A(t)=|a|(t) on a fine grid.
(2) build Q_ret(t) (exp window over PAST of stored A) and Q_adv(t) (exp window over
FUTURE of stored A); re-integrate full dynamics with mu_fw(Q_pre(t)/a0) prescribed.
Same integrator, same grid: any scheme bias is common mode; a sign flip ret->adv
certifies the pump as pure retardation physics. First order in tau/P: exact +/- symmetry.
"""
import numpy as np, sys
a0=9.36e-11; GMsun=1.32712e20; AU=1.495979e11; yr=3.15576e7
def mu_fw(x): x=np.maximum(x,1e-300); return (np.sqrt(1+4*x*x)-1)/(2*x)
GM=1.5*GMsun; r0=5e3*AU
g0=GM/r0**2; A0=np.sqrt(g0*g0+g0*a0); vc=np.sqrt(A0*r0); P=2*np.pi*np.sqrt(r0/A0)
NPER=8; DTF=4000; dt=P/DTF; N=int(NPER*DTF)
# pass 1: pointwise
r=np.array([r0,0.]); v=np.array([0.,vc*np.sqrt(0.5)]); Astore=np.zeros(N)
def accP(rv):
    rr=np.linalg.norm(rv); g=GM/rr**2; return -np.sqrt(g*g+g*a0)*rv/rr
R=[r.copy()]; V=[v.copy()]
for i in range(N):
    k1=accP(r); k1r=v
    k2=accP(r+0.5*dt*k1r); k2r=v+0.5*dt*k1
    k3=accP(r+0.5*dt*k2r); k3r=v+0.5*dt*k2
    k4=accP(r+dt*k3r); k4r=v+dt*k3
    r=r+dt/6*(k1r+2*k2r+2*k3r+k4r); v=v+dt/6*(k1+2*k2+2*k3+k4)
    rr=np.linalg.norm(r); g=GM/rr**2; Astore[i]=np.sqrt(g*g+g*a0)
tau=0.01*P; al=np.exp(-dt/tau)
A2=Astore**2
Qr=np.zeros(N); Qa=np.zeros(N)
acc_=A2[0]
for i in range(N): acc_=A2[i]+(acc_-A2[i])*al; Qr[i]=acc_
acc_=A2[-1]
for i in range(N-1,-1,-1): acc_=A2[i]+(acc_-A2[i])*al; Qa[i]=acc_
Qr=np.sqrt(Qr); Qa=np.sqrt(Qa)
def rerun(Qpre):
    r=np.array([r0,0.]); v=np.array([0.,vc*np.sqrt(0.5)])
    apos=[]; rdp=1.
    for i in range(N):
        Q=Qpre[i]
        def acc(rv):
            rr=np.linalg.norm(rv); g=GM/rr**2; return -(g/mu_fw(Q/a0))*rv/rr
        k1=acc(r); k1r=v
        k2=acc(r+0.5*dt*k1r); k2r=v+0.5*dt*k1
        k3=acc(r+0.5*dt*k2r); k3r=v+0.5*dt*k2
        k4=acc(r+dt*k3r); k4r=v+dt*k3
        r=r+dt/6*(k1r+2*k2r+2*k3r+k4r); v=v+dt/6*(k1+2*k2+2*k3+k4)
        rdot=np.dot(r,v)/np.linalg.norm(r)
        if rdp>0 and rdot<=0: apos.append(np.linalg.norm(r))
        rdp=rdot
    return np.array(apos)
def sl(seq,skip=2):
    if len(seq)<skip+3: return float('nan')
    s=seq[skip:]; return np.polyfit(np.arange(len(s)),s,1)[0]/np.mean(s)
apr=rerun(Qr); apa=rerun(Qa); app=rerun(Astore)  # Astore = zero-lag control
print("WB 5kAU e=0.5 tau/P=0.01, prescribed-timeline (first-order-in-backreaction):")
print("  zero-lag control : %+.3e /orbit"%sl(app))
print("  RETARDED window  : %+.3e /orbit"%sl(apr))
print("  ADVANCED window  : %+.3e /orbit"%sl(apa))
print("  ratio adv/ret = %+.3f  (physical retardation pump => ~ -1)"%(sl(apa)/sl(apr)))
print("EXIT 0"); sys.exit(0)
