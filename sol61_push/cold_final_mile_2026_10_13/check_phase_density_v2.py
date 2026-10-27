"""CE-FM-003 corrected bounded phase-density necessary preparation; not an existence test."""
import json,sys
from pathlib import Path
import numpy as np

C=.3*(3/(4*np.pi))**(2/3)
checks=[]
def check(name,condition,detail):
    checks.append(dict(name=name,passed=bool(condition),detail=detail))
    if not condition:raise AssertionError(name)

# Orthogonal explicit packed velocity ball: rho=4pi F v_*^3/3, K_density=2pi F v_*^5/5.
for rho in (.01,1.,100.):
    for F in (.01,1.,100.):
        vmax=(3*rho/(4*np.pi*F))**(1/3)
        direct=2*np.pi*F*vmax**5/5
        bound=C*F**(-2/3)*rho**(5/3)
        check(f'packed ball equality rho={rho} F={F}',abs(direct/bound-1)<1e-13,float(direct/bound-1))

def integrals(R,k,n):
    z,w=np.polynomial.legendre.leggauss(n)
    t=(z+1)*R**(1/3)/2;r=t**3
    drdt=3*t*t
    weight=w*R**(1/3)/2*drdt
    root=np.sqrt(1+4*r*r)
    # Cancellation-free m0 and u0; important in the central quadrature cells.
    m0=2*r*r/(root+1);u0=2/(root+1)
    dm0=2*r/root
    rho0=1/(2*np.pi*r*root)
    integral_rho=float(np.sum(weight*4*np.pi*r*r*(k*rho0)**(5/3)))
    # Virial K=.5 int dm r [gN-R(ku0)].
    # Stable difference: 1-k^2(1-u)/(1-ku)=(1-k)[1+k-ku]/[1-ku].
    delta=(1-k)*(1+k-k*u0)/(1-k*u0)
    K=float(.5*k*np.sum(weight*dm0*delta/r))
    F_required=(C*integral_rho/K)**1.5
    return dict(R=R,k=k,rho_power_integral=integral_rho,virial_K=K,F_required=F_required)

rows=[]
for R in (10.,50.):
    previous=0.
    for k in (.5,.8,.9,.95,.99):
        a=integrals(R,k,128);b=integrals(R,k,256);d=integrals(R,k,512)
        err=max(abs(b[key]/d[key]-1) for key in ('rho_power_integral','virial_K','F_required'))
        check(f'quadrature resolution R={R} k={k}',err<1e-7,err)
        check(f'positive budget R={R} k={k}',d['virial_K']>0,d['virial_K'])
        check(f'monotonic required phase density R={R} k={k}',d['F_required']>previous,d['F_required'])
        previous=d['F_required'];rows.append(d)
    near=[integrals(R,k,512) for k in (.9999,.99999)]
    ratio=near[1]['F_required']/near[0]['F_required']
    # Cusp: K~(pi/2)*sqrt(1-k), hence F_required~(1-k)^(-3/4).
    check(f'cusp phase-density asymptotic R={R}',abs(ratio/(10**.75)-1)<.03,ratio)
    asymptotic=np.pi/2*np.sqrt(1-near[1]['k'])
    check(f'cusp virial leading coefficient R={R}',abs(near[1]['virial_K']/asymptotic-1)<.02,near[1]['virial_K']/asymptotic)

result=dict(checks=checks,rows=rows,coefficient=C,
            domain='G=a0=Mb=1; spherical stationary no-boundary-stress pure tethered profile M=kM0 within finite R; bounded mass phase density',
            conclusion='Necessary F lower bounds only; no stationary distribution existence, formation, observational inference or condensate constraint.')
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
