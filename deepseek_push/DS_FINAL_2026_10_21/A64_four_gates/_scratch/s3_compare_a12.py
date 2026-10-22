import numpy as np
G=6.67430e-11; C=2.99792458e8; MSUN=1.98892e30; PC=3.0856775814913673e16
K=4*np.pi*G/C**2; A0=9.36e-11; A0g=A0/C**2
MBAR=5e10*MSUN; AH=3e3*PC
def gN(r): return G*(MBAR*r**2/(r+AH)**2)/r**2
def mond(gn): return 0.5*gn*(1+np.sqrt(1+4*A0/gn))

def run(Pi_kind, coef, rmax_pc, npts=20000):
    rr=np.geomspace(1e-3*PC, rmax_pc*PC, npts)
    gn=gN(rr); g=mond(gn); u=g-gn
    ug=u/C**2; gg=g/C**2; x=ug/A0g
    if Pi_kind=='exact':    Pi = ug**2/(K*(1-x))          # A3 Pi = uW'
    elif Pi_kind=='a12':    Pi = ug*gg/K                  # A12 code: u*g/K
    elif Pi_kind=='a3W':    Pi = ug**2/K                  # quadratic W approx
    integ=Pi/rr
    seg=0.5*(integ[1:]+integ[:-1])*np.diff(rr)
    outer=np.concatenate([np.cumsum(seg[::-1])[::-1],[0.0]])
    fp=-coef*K*rr*outer
    segf=0.5*(np.abs(fp)[1:]+np.abs(fp)[:-1])*np.diff(rr)
    fabs=np.concatenate([np.cumsum(segf[::-1])[::-1],[0.0]])
    out=[]
    for rk in (10.,100.):
        j=int(np.argmin(abs(rr-rk*1e3*PC)))
        Psi=g[j]*rk*1e3*PC/C**2
        out.append((rk,abs(fabs[j])/Psi, abs(fp[j])/gg[j], Psi, -x[j]))
    return out
for kind in ('exact','a12','a3W'):
    for coef in (2.0,3.0):
        print(kind,coef)
        for row in run(kind,coef,3e6):
            print("   r=%5.0f kpc  |Phi-Psi|/Psi=%.3e   |f'|/g=%.3e  Psi=%.3e u/a0=%.3f"%row)
print()
print("cutoff sensitivity (exact, 2K):")
for rm in (0.3e6,1e6,3e6,10e6,100e6):
    rows=run('exact',2.0,rm)
    print("  rmax=%8.1f Mpc  r=10kpc: %.3e   r=100kpc: %.3e"%(rm/1e6,rows[0][1],rows[1][1]))