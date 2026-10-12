"""Nonlinear sourced radial field, conservative staggered discretisation."""
import os
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[name]='1'
import ast,json
from pathlib import Path
import numpy as np
from scipy.optimize import brentq
HERE=Path(__file__).resolve().parent
SRC=HERE.parents[1]/'campaign_fresh_gravity/CFG596_lean_pm_1024/cfg596_pm.py'
names={'Y_P','H_P','DELTA','LYG','YG','DH_MONO','H_MONO'}
nodes=[n for n in ast.parse(SRC.read_text()).body if (isinstance(n,ast.FunctionDef) and n.name in {'h_rar','dh_rar','nu_mono'}) or (isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in names for t in n.targets))]
env={'np':np,'brentq':brentq};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(SRC),'exec'),env)
pt=np.r_[0.,env['H_MONO']];bt=np.r_[0.,env['YG']]
sl=np.diff(bt)/np.diff(pt);wt=np.r_[0.,np.cumsum(.5*(bt[1:]+bt[:-1])*np.diff(pt))]
def W(p):
    z=abs(p);j=np.clip(np.searchsorted(pt,z)-1,0,len(pt)-2);d=z-pt[j]
    return wt[j]+bt[j]*d+.5*sl[j]*d*d
def b(p):return np.sign(p)*np.interp(abs(p),pt,bt)
checks=[]
def check(name,val,tol):checks.append(dict(name=name,value=float(val),tolerance=tol,passed=bool(abs(val)<=tol)))
def run(R,n,dt):
    dr=R/n;rf=np.arange(n+1)*dr;r=(rf[:-1]+rf[1:])/2
    vol=(rf[1:]**3-rf[:-1]**3)/3
    length=np.full(n,dr);length[-1]=dr/2
    area=rf[1:]**2;fw=area*length
    rho=np.where(r<8,np.exp(-r*r/8),0);rho/=np.dot(rho,vol)
    b0=np.cumsum(rho*vol)/area;p0=np.interp(b0,bt,pt);g0=b0+p0
    phi0=-np.cumsum((g0*length)[::-1])[::-1]
    def grad(phi):return (np.r_[phi[1:],0]-phi)/length
    def div(f):return np.diff(np.r_[0,area*f])/vol
    def acc(phi,p):
        q=grad(phi);return div(q-p)-rho,q-p-b(p)
    def energy(phi,p,v,w):
        q=grad(phi)
        return float(np.dot(.5*v*v+rho*phi,vol)+np.dot(.5*w*w+.5*(q-p)**2+W(p),fw))
    ar,ap=acc(phi0,p0)
    check('static residual '+str((R,n)),max(np.max(abs(ar)),np.max(abs(ap))),1e-7)
    check('no-source zero RHS '+str((R,n)),max(np.max(abs(div(np.zeros(n)))),np.max(abs(b(np.zeros(n))))),1e-14)
    norm=abs(energy(phi0,p0,np.zeros(n),np.zeros(n)))
    phi=np.zeros(n);p=phi.copy();v=phi.copy();w=phi.copy();af,ap=acc(phi,p)
    sel=(rf[1:]>=2)&(rf[1:]<=20);samples=[];maxe=0
    for step in range(round(160/dt)+1):
        if step%round(10/dt)==0:
            q=grad(phi);err=float(np.sqrt(np.mean(((q[sel]-g0[sel])/g0[sel])**2)))
            e=energy(phi,p,v,w)/norm;maxe=max(maxe,abs(e))
            samples.append(dict(time=step*dt,force_rms_fractional_error=err,min_force=float(q[sel].min()),energy_error=e))
        if step==round(160/dt):break
        v+=dt*.5*af;w+=dt*.5*ap;phi+=dt*v;p+=dt*w
        af,ap=acc(phi,p);v+=dt*.5*af;w+=dt*.5*ap
    check('energy '+str((R,n)),maxe,.002)
    return dict(R=R,N=n,dt=dt,samples=samples,formation=all(s['force_rms_fractional_error']<=.1 and s['min_force']>=0 for s in samples if s['time']>=120),r=rf[1:][sel].tolist(),force=grad(phi)[sel].tolist(),target=g0[sel].tolist())
rows=[run(128,512,.04),run(128,1024,.02),run(256,1024,.04)]
base=np.array(rows[0]['force']);target=np.array(rows[0]['target'])
for label,other in [('refinement',rows[1]),('box',rows[2])]:
    pred=np.interp(rows[0]['r'],other['r'],other['force'])
    check(label+' force',np.linalg.norm(pred-base)/np.linalg.norm(target),.03)
out=dict(rows=rows,checks=checks,all_checks_pass=all(c['passed'] for c in checks))
(HERE/'spherical_run/results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(checks=checks,summaries=[dict(R=r['R'],N=r['N'],formation=r['formation'],late=[s for s in r['samples'] if s['time']>=120]) for r in rows]),indent=2))
assert out['all_checks_pass']
