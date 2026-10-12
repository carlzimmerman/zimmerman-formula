"""Finite nonlinear vacuum packet test; no fitted dissipation."""
import os
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[name]='1'
import ast,json
from pathlib import Path
import numpy as np
from scipy.optimize import brentq
HERE=Path(__file__).resolve().parent
SRC=HERE.parents[1]/'campaign_fresh_gravity/CFG596_lean_pm_1024/cfg596_pm.py'
tree=ast.parse(SRC.read_text()); names={'Y_P','H_P','DELTA','LYG','YG','DH_MONO','H_MONO'}
nodes=[n for n in tree.body if (isinstance(n,ast.FunctionDef) and n.name in {'h_rar','dh_rar','nu_mono'}) or
       (isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in names for t in n.targets))]
env={'np':np,'brentq':brentq}; exec(compile(ast.Module(body=nodes,type_ignores=[]),str(SRC),'exec'),env)
pt=np.r_[0.,env['H_MONO']]; bt=np.r_[0.,env['YG']]
sl=np.diff(bt)/np.diff(pt)
wt=np.r_[0.,np.cumsum(.5*(bt[1:]+bt[:-1])*np.diff(pt))]
def potential(p):
    v=abs(p); j=np.clip(np.searchsorted(pt,v)-1,0,len(pt)-2); z=v-pt[j]
    return wt[j]+bt[j]*z+.5*sl[j]*z*z
def force(p):
    if np.max(abs(p))>=pt[-1]: raise ValueError('table support exceeded')
    return np.sign(p)*np.interp(abs(p),pt,bt)

def run(amp,n,dt,linear=False):
    dx=512./n; x=(np.arange(n)-n/2)*dx; k=2*np.pi*np.fft.rfftfreq(n,dx); k[-1]=0
    def D(u): return np.fft.irfft(1j*k*np.fft.rfft(u),n=n)
    phi=amp*8*np.exp(.5)*np.exp(-x*x/(2*8.**2)); p=D(phi)
    q0=p.copy(); v=np.zeros(n); w=v.copy()
    def accel(phi,p):
        diff=D(phi)-p
        return D(diff),diff-(0 if linear else force(p))
    def energy(phi,p,v,w):
        return .5*(v*v+w*w+(D(phi)-p)**2)+(0 if linear else potential(p))
    e0=float(np.sum(energy(phi,p,v,w))*dx); ap,aq=accel(phi,p); rows=[]
    steps=round(300/dt)
    for s in range(steps+1):
        if s%round(10/dt)==0 or s==steps or s==0:
            e=energy(phi,p,v,w); total=float(e.sum()*dx)
            rows.append(dict(time=s*dt,relative_energy_drift=(total/e0-1 if e0 else total),
                central_fraction=(float(e[abs(x)<24].sum()*dx/e0) if e0 else None),
                gradient_change=float(np.linalg.norm(D(phi)-q0)/np.linalg.norm(q0))))
        if s==steps:break
        v+=.5*dt*ap; w+=.5*dt*aq
        phi+=dt*v; p+=dt*w
        ap,aq=accel(phi,p)
        v+=.5*dt*ap; w+=.5*dt*aq
    return dict(amplitude=amp,N=n,dt=dt,linear=linear,initial_energy=e0,
                max_energy_error=max(abs(r['relative_energy_drift']) for r in rows),samples=rows)

rows=[]; checks=[]
for amp in (.01,.03,.1):
    pair=[run(amp,512,.15),run(amp,1024,.075)]; rows.extend(pair)
    for r in pair:
        checks.append(dict(name='energy '+str((amp,r['N'])),value=r['max_energy_error'],passed=r['max_energy_error']<.002))
    diff=abs(pair[0]['samples'][-1]['central_fraction']-pair[1]['samples'][-1]['central_fraction'])
    checks.append(dict(name='resolution '+str(amp),value=diff,passed=diff<.03))
control=run(.1,512,.15,True)
err=control['samples'][-1]['gradient_change']
checks.append(dict(name='linear null control',value=err,passed=err<1e-8))
out=dict(rows=rows,control=control,checks=checks,all_checks_pass=all(c['passed'] for c in checks))
(HERE/'nonlinear_run/results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(checks=checks,final=[dict(amplitude=r['amplitude'],N=r['N'],**r['samples'][-1]) for r in rows]),indent=2))
assert out['all_checks_pass']
