"""Fixed-history profile tests and exact-action external-field diagnostic."""
from pathlib import Path
import json
pdir=Path(__file__).resolve().parent
source=(pdir/'assembly.py').read_text().split('rows=[]')[0]
source=source.replace('def run(T,n,dt):','def run(T,n,dt,mass,core):')
source=source.replace('r<8,np.exp(-r*r/8)','r<4*core,np.exp(-r*r/(2*core*core))')
source=source.replace('rho/=np.dot(rho,vol)','rho*=mass/np.dot(rho,vol)')
env={'__file__':str(pdir/'assembly.py')};exec(compile(source,str(pdir/'assembly.py'),'exec'),env)
np=env['np'];run=env['run'];check=env['check'];checks=env['checks'];rows=[]
for mass,core in ((.1,2),(1,1),(1,4),(10,2)):
    pair=[run(320,2048,.04,mass,core),run(320,4096,.02,mass,core)]
    for r in pair:r.update(mass=mass,core=core)
    rows.extend(pair)
    pred=np.interp(pair[0]['r'],pair[1]['r'],pair[1]['force'])
    check('profile refinement '+str((mass,core)),np.linalg.norm(pred-np.array(pair[0]['force']))/np.linalg.norm(pair[0]['target']),.03)
# Response of the actual interpolated inverse-deficit constitutive model.
pt=env['pt'];bt=env['bt'];gt=pt+bt
bn=1e-8;giso=bn+np.interp(bn,bt,pt);external=[]
for ge in (.01,.1,1.):
    j=np.clip(np.searchsorted(gt,ge)-1,0,len(gt)-2)
    be=float(np.interp(ge,gt,bt));bp=float((bt[j+1]-bt[j])/(gt[j+1]-gt[j]));mu=be/ge
    axial=bn/mu;equatorial=bn/np.sqrt(mu*bp)
    check('external perturbation small '+str(ge),max(axial,equatorial)/ge,.001)
    checks.append(dict(name='elliptic '+str(ge),passed=bool(mu>0 and bp>0),value=min(mu,bp)))
    external.append(dict(ge=ge,mu=mu,Bprime=bp,bn=bn,g_isolated=float(giso),g_parallel=float(axial),g_equatorial=float(equatorial),parallel_fraction=float(axial/giso),equatorial_fraction=float(equatorial/giso)))
out=dict(rows=rows,external=external,checks=checks,all_checks_pass=all(c['passed'] for c in checks))
(pdir/'profile_audit_run/results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(checks=checks,external=external,profiles=[dict(mass=r['mass'],core=r['core'],N=r['N'],formation=r['formation'],late_max=max(s['error'] for s in r['samples'] if s['time']>=560),final_error=r['samples'][-1]['error']) for r in rows]),indent=2))
assert out['all_checks_pass']
