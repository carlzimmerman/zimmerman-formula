#!/usr/bin/env python3
"""
D3 v3 -- pump-sign diagnostics (bulletproofing the Fifth-Theorem candidate).
Tests: (1) retarded exp-window vs first-order lag (Q=A-tau dA/dt) vs first-order LEAD
(Q=A+tau dA/dt, 'advanced'): physical retardation pump must FLIP SIGN under lead;
integrator dissipation would not flip. (2) dt-convergence. (3) escape bookkeeping.
"""
import numpy as np, sys
a0=9.36e-11; GMsun=1.32712e20; AU=1.495979e11; yr=3.15576e7; kpc=3.0857e19
def mu_fw(x): x=np.maximum(x,1e-300); return (np.sqrt(1+4*x*x)-1)/(2*x)

def run(GM,r0,e,mode,tau,nP,dtfrac=3000.):
    g0=GM/r0**2; A0=np.sqrt(g0*g0+g0*a0); vc=np.sqrt(A0*r0)
    r=np.array([r0,0.]); v=np.array([0.,vc*np.sqrt(1-e)])
    P=2*np.pi*np.sqrt(r0/A0); dt=P/dtfrac; ya=A0*A0; Aprev=A0; dAdt=0.
    apos=[]; rdp=np.dot(r,v)/r0; esc=None
    for i in range(int(nP*dtfrac)):
        if mode=="ctrl": Q=None
        elif mode=="exp": Q=np.sqrt(max(ya,1e-90))
        elif mode=="lag1": Q=max(Aprev-tau*dAdt,1e-30)
        elif mode=="lead1": Q=max(Aprev+tau*dAdt,1e-30)
        def acc(rv):
            rr=np.linalg.norm(rv); g=GM/rr**2
            A=np.sqrt(g*g+g*a0) if Q is None else g/mu_fw(Q/a0)
            return -A*rv/rr
        k1=acc(r); k1r=v
        k2=acc(r+0.5*dt*k1r); k2r=v+0.5*dt*k1
        k3=acc(r+0.5*dt*k2r); k3r=v+0.5*dt*k2
        k4=acc(r+dt*k3r); k4r=v+dt*k3
        r=r+dt/6*(k1r+2*k2r+2*k3r+k4r); v=v+dt/6*(k1+2*k2+2*k3+k4)
        rr=np.linalg.norm(r); g=GM/rr**2
        A=np.sqrt(g*g+g*a0) if Q is None else g/mu_fw(Q/a0)
        dAdt=(A-Aprev)/dt; Aprev=A
        ya=A*A+(ya-A*A)*np.exp(-dt/tau) if tau>0 else A*A
        rdot=np.dot(r,v)/rr
        if rdp>0 and rdot<=0: apos.append(rr)
        rdp=rdot
        if rr>8*r0 and esc is None: esc=i/dtfrac; break
    return np.array(apos),esc

def sl(seq,skip=4):
    if len(seq)<skip+4: return float('nan')
    s=seq[skip:]; return np.polyfit(np.arange(len(s)),s,1)[0]/np.mean(s)

GM=1.5*GMsun; r0=5e3*AU
g0=GM/r0**2; A0=np.sqrt(g0*g0+g0*a0); P=2*np.pi*np.sqrt(r0/A0)
print("WB 5kAU e=0.5, tau/P=0.01 -- sign diagnostic (apo-slope/orbit):")
for mode in ["ctrl","exp","lag1","lead1"]:
    ap,esc=run(GM,r0,0.5,mode,0.01*P,30)
    ap2,esc2=run(GM,r0,0.5,mode,0.01*P,30,dtfrac=8000.)
    print("  %-6s dt=P/3000: %+.3e   dt=P/8000: %+.3e %s"%(mode,sl(ap),sl(ap2),
          "" if esc is None else "(ESCAPED at %.1f P)"%esc))
ap,esc=run(GM,r0,0.5,"exp",0.1*P,40)
print("  exp tau/P=0.1: slope %+.3e ; escape: %s"%(sl(ap), "UNBOUND at %.1f P"%esc if esc else "bound"))
# deep-MOND dSph lead test
GMd=GMsun*1e9; r0d=5*kpc; g0d=GMd/r0d**2; A0d=np.sqrt(g0d*g0d+g0d*a0); Pd=2*np.pi*np.sqrt(r0d/A0d)
for mode in ["exp","lead1"]:
    apd,escd=run(GMd,r0d,0.7,mode,0.01*Pd,25)
    print("deep-MOND e=0.7 tau/P=0.01 %-5s: %+.3e %s"%(mode,sl(apd),"(ESC %.1fP)"%escd if escd else ""))
# kill arithmetic
print("\nKILL ARITHMETIC (pump coeff c: drift/orbit = c*(tau/P), measured c~8.7 (WB x=3.8), c~46 (deep):")
for nm,Pyr,c,age,budget in [("WB 2kAU (x=24)",73e3,3.0,5e9,0.1),("WB 5kAU (x=3.8)",272e3,8.7,5e9,0.1),
                            ("dSph (deep)",3e8,46.,1e10,0.3)]:
    taumax=budget*Pyr**2/(c*age)
    print("  %-16s P=%.0e yr: tau_max = %.2e yr  (vs Saturn floor C1 4.4e3 yr / C2 1.4e2 yr)"%(nm,Pyr,taumax))
print("EXIT 0"); sys.exit(0)
