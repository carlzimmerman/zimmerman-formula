"""Prescribed source assembly with explicit external work accounting."""
from pathlib import Path
import json
pdir=Path(__file__).resolve().parent
prefix=(pdir/'spherical.py').read_text().split('def run(R,n,dt):')[0]
env={'__file__':str(pdir/'spherical.py')};exec(compile(prefix,str(pdir/'spherical.py'),'exec'),env)
np=env['np'];pt=env['pt'];bt=env['bt'];W=env['W'];b=env['b'];check=env['check'];checks=env['checks']
def run(T,n,dt):
    R=512.;dr=R/n;rf=np.arange(n+1)*dr;r=(rf[:-1]+rf[1:])/2
    vol=(rf[1:]**3-rf[:-1]**3)/3;length=np.full(n,dr);length[-1]=dr/2
    area=rf[1:]**2;fw=area*length
    rho=np.where(r<8,np.exp(-r*r/8),0);rho/=np.dot(rho,vol)
    b0=np.cumsum(rho*vol)/area;p0=np.interp(b0,bt,pt);g0=b0+p0
    phi0=-np.cumsum((g0*length)[::-1])[::-1]
    def grad(phi):return (np.r_[phi[1:],0]-phi)/length
    def div(f):return np.diff(np.r_[0,area*f])/vol
    def ramp(t):
        u=min(1.,max(0.,t/T));return u*u*(3-2*u),6*u*(1-u)/T
    def acc(phi,p,t):
        diff=grad(phi)-p;return div(diff)-ramp(t)[0]*rho,diff-b(p)
    def energy(phi,p,v,w,t):return float(np.dot(.5*v*v+ramp(t)[0]*rho*phi,vol)+np.dot(.5*w*w+.5*(grad(phi)-p)**2+W(p),fw))
    zero=np.zeros(n);norm=abs(energy(phi0,p0,zero,zero,T));af,ap=acc(phi0,p0,T)
    check('static '+str((T,n)),max(np.max(abs(af)),np.max(abs(ap))),1e-7)
    phi=zero.copy();p=zero.copy();v=zero.copy();w=zero.copy();af,ap=acc(phi,p,0)
    work=0.;power=0.;sel=(rf[1:]>=2)&(rf[1:]<=20);samples=[];maxe=0.;end=T+320
    for step in range(round(end/dt)+1):
        t=step*dt
        if step%round(10/dt)==0:
            q=grad(phi);err=float(np.sqrt(np.mean(((q[sel]-g0[sel])/g0[sel])**2)))
            residual=(energy(phi,p,v,w,t)-work)/norm;maxe=max(maxe,abs(residual))
            samples.append(dict(time=t,error=err,min_force=float(q[sel].min()),energy_work_residual=residual,source_work=work))
        if step==round(end/dt):break
        v+=dt*.5*af;w+=dt*.5*ap;phi+=dt*v;p+=dt*w
        af,ap=acc(phi,p,t+dt);v+=dt*.5*af;w+=dt*.5*ap
        newpower=ramp(t+dt)[1]*float(np.dot(rho*phi,vol));work+=.5*dt*(power+newpower);power=newpower
    check('energy-work '+str((T,n)),maxe,.002)
    return dict(T=T,N=n,dt=dt,end=end,samples=samples,formation=all(s['error']<=.1 and s['min_force']>=0 for s in samples if s['time']>=end-80),r=rf[1:][sel].tolist(),force=grad(phi)[sel].tolist(),target=g0[sel].tolist())
rows=[]
for T in (40,160,320):
    pair=[run(T,2048,.04),run(T,4096,.02)];rows.extend(pair)
    pred=np.interp(pair[0]['r'],pair[1]['r'],pair[1]['force'])
    check('refinement '+str(T),np.linalg.norm(pred-np.array(pair[0]['force']))/np.linalg.norm(pair[0]['target']),.03)
out=dict(rows=rows,checks=checks,all_checks_pass=all(c['passed'] for c in checks))
(pdir/'assembly_run/results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(checks=checks,summary=[dict(T=r['T'],N=r['N'],formation=r['formation'],late_error_min=min(s['error'] for s in r['samples'] if s['time']>=r['end']-80),late_error_max=max(s['error'] for s in r['samples'] if s['time']>=r['end']-80),final=r['samples'][-1]) for r in rows]),indent=2))
assert out['all_checks_pass']
