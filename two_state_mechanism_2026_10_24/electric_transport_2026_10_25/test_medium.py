"""Deterministic necessary-condition tests, not galaxy evolution."""
import argparse, json
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.special import ellipe


def spectrum():
    def shifted(s):
        def f(r):
            if r+s == 0: return 0.
            return -r*2*(r+s)/np.pi*ellipe(4*r*s/(r+s)**2)
        return quad(f,0,1,points=[s],epsabs=2e-13,epsrel=2e-13,limit=300)[0]
    def massive(s): return -((1+s*s)**1.5-s**3)/3
    rows=[]
    for h in [.1,.05,.02,.01,.005,.002]:
        rows.append(dict(h=h,shift_cubic=(shifted(2*h)-4*shifted(h)-1)/(4*h**3),
                         mass_cubic=(massive(2*h)-4*massive(h)-1)/(4*h**3)))
    # Independent Cartesian disk quadrature at s=.2.
    s=.2
    def strip(x):
        z=np.sqrt(max(0,1-x*x)); b=abs(x-s)
        if b < 1e-14: return z*z
        return z*np.sqrt(z*z+b*b)+b*b*np.arcsinh(z/b)
    cart=-quad(strip,-1,1,points=[s],epsabs=2e-12,limit=300)[0]/(2*np.pi)
    return dict(rows=rows,cartesian_vs_elliptic_error=abs(cart-shifted(s)))


def transport(n,a,times):
    # Unit lattice spacing, mu=M=1, K=.25, k=1.
    K=.25
    coords=np.arange(n)-n//2
    X,Y,Z=np.meshgrid(coords,coords,coords,indexing='ij',sparse=True)
    radius2=X*X+Y*Y+Z*Z
    x0=np.exp(-radius2/(2*1.5**2)); core=radius2<=6**2
    f=2*np.pi*np.fft.fftfreq(n)
    d=np.exp(1j*f)-1
    dx=d[:,None,None]
    q2=abs(d[:,None,None])**2+abs(d[None,:,None])**2+abs(d[None,None,:])**2
    A=K; B=-K*a*dx+np.zeros_like(q2); C=q2+K*a*a*abs(dx)**2
    gap=np.sqrt((A-C)**2+4*abs(B)**2)
    lo=np.maximum(0,(A+C-gap)/2); hi=(A+C+gap)/2
    # Matrix functions via spectral projectors; degeneracies handled by limit.
    safe=np.where(gap>1e-13,gap,1)
    plxx=np.where(gap>1e-13,(hi-A)/safe,1)
    plux=np.where(gap>1e-13,-B.conj()/safe,0)
    xhat=np.fft.fftn(x0); rows=[]
    def real(z):
        val=np.fft.ifftn(z)
        assert np.max(abs(val.imag))<2e-12
        return val.real
    for t in times:
        cl=np.cos(np.sqrt(lo)*t); ch=np.cos(np.sqrt(hi)*t)
        sl=-np.sqrt(lo)*np.sin(np.sqrt(lo)*t); sh=-np.sqrt(hi)*np.sin(np.sqrt(hi)*t)
        x=real((ch+(cl-ch)*plxx)*xhat)
        u=real((cl-ch)*plux*xhat)
        vx=real((sh+(sl-sh)*plxx)*xhat)
        vu=real((sl-sh)*plux*xhat)
        du=np.roll(u,-1,axis=0)-u
        density=(vx*vx+vu*vu+K*(x-a*du)**2)/2
        for axis in range(3): density+=(np.roll(u,-1,axis=axis)-u)**2/2
        total=float(density.sum()); ecore=float(density[core].sum())
        rows.append(dict(time=float(t),total=total,core=ecore,outside=total-ecore))
    e0=K/2*float((x0*x0).sum())
    return dict(n=n,coupling=a,initial_energy=e0,
                max_relative_energy_error=max(abs(r['total']/e0-1) for r in rows),
                final_core_fraction=rows[-1]['core']/e0,rows=rows)


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args()
    spec=spectrum()
    runs=[transport(64,a,np.linspace(0,12,25)) for a in [0,.5,1.5]]
    runs.append(transport(96,1.5,[0,6,12]))
    L=np.array([.3,1,3,300.])
    thresholds=np.geomspace(.01,1e5,1001)
    passes=[]
    for exponent in [1,2]:
        cooled=L[None,:]**exponent < thresholds[:,None]
        success=cooled[:,2]&~cooled[:,0]&~cooled[:,1]&~cooled[:,3]
        passes.append(dict(exponent=exponent,threshold_count=len(thresholds),success_count=int(success.sum())))
    result=dict(spectrum=spec,transport=runs,
                box_check_final_core_difference=abs(runs[2]['final_core_fraction']-runs[3]['final_core_fraction']),
                size_only_selection=passes,
                thickness_to_beat_smallest_kpc=float((3/.3**2-2/3**2)**-.5),
                interpretation='Necessary-condition tests only; no galaxy simulation, no tether fraction.')
    assert spec['cartesian_vs_elliptic_error']<1e-9
    assert abs(spec['rows'][-1]['shift_cubic'])<.001
    assert abs(spec['rows'][-1]['mass_cubic']-1/3)<.001
    assert max(r['max_relative_energy_error'] for r in runs)<1e-11
    assert abs(runs[0]['final_core_fraction']-runs[0]['rows'][0]['core']/runs[0]['initial_energy'])<1e-12
    assert result['box_check_final_core_difference']<1e-7
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='transport'},indent=2))
    print([(r['n'],r['coupling'],r['final_core_fraction'],r['max_relative_energy_error']) for r in runs])

if __name__=='__main__': main()
