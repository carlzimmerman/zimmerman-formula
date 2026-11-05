"""Conditional NFW concentration-prior sensitivity, not a LCDM likelihood.
Uses original forecast definitions through AST selection without running that experiment.
M200 here is total-equivalent DM-only simulation mass; dark amplitude is (1-fb).
"""
import ast, json, math, sys
from pathlib import Path
import numpy as np
from scipy.optimize import least_squares

here=Path(__file__).resolve().parent
out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=True)
tree=ast.parse((here/'forecast.py').read_text())
allowed={'G','U','H0','OM','A0','W0','WA'}
nodes=[n for n in tree.body if isinstance(n,(ast.Import,ast.ImportFrom,ast.FunctionDef)) or
       isinstance(n,ast.Assign) and all(isinstance(t,ast.Name) and t.id in allowed for t in n.targets)]
ns={};exec(compile(ast.Module(body=nodes,type_ignores=[]),'forecast definitions','exec'),ns)
disc,speed,nfw,ratio= [ns[k] for k in ['disc','speed','nfw','ratio']]
inputs=json.loads((here/'inputs.json').read_text())
profiles=json.loads((here/'run01/profile_fits.json').read_text())
fb=.157
def logc(lm,z):
    a=.520+(.905-.520)*math.exp(-.617*z**1.21)
    b=-.101+.026*z
    return a+b*(lm+math.log10(.671)-12)
records=[]
for p in profiles:
    d=inputs[p['target']];z=d['z'];R=np.array(p['radii']);Ms=10**d['logMs']
    L=d.get('Lp10') or ns['lp'](d['F32'],z)*d['R31'];Mg=p['alpha']*L
    vs=disc(Ms,p['Re_star'],R);vg=disc(Mg,p['Re_gas'],R)
    vt=speed(vs+vg,R,ns['A0']*ratio(z))
    for width in [0.,.22]:
        lower=math.log10((Ms*10**(-.2)+Mg*10**(-.3))/fb)
        def pred(x):
            c=10**(logc(x[2],z)+(x[3] if width else 0))
            return np.sqrt(vs*10**x[0]+vg*10**x[1]+(1-fb)*nfw(x[2],c,z,R))
        def res(x):
            penalty=max(0,math.log10((Ms*10**x[0]+Mg*10**x[1])/fb)-x[2])*10
            return np.r_[(pred(x)-vt)/vt,penalty]
        lo=[-.2,-.3,lower]+([-width] if width else [])
        hi=[.2,.3,14.]+([width] if width else [])
        fits=[]
        for lm in [12.,12.5,13.]:
            x=[-.1,-.1,max(lower+.01,lm)]+([0.] if width else [])
            fits.append(least_squares(res,x,bounds=(lo,hi),xtol=1e-11,ftol=1e-11,gtol=1e-11,max_nfev=1000))
        f=min(fits,key=lambda x:sum(x.fun**2));err=(pred(f.x)-vt)/vt
        budget=10**f.x[2] >= (Ms*10**f.x[0]+Mg*10**f.x[1])/fb*(1-1e-4)
        records.append(dict(target=p['target'],Re_star=p['Re_star'],Re_gas=p['Re_gas'],alpha=p['alpha'],concentration_width_dex=width,parameters=f.x.tolist(),c200=10**(logc(f.x[2],z)+(f.x[3] if width else 0)),rms_fraction=float(np.sqrt(np.mean(err**2))),max_fraction=float(max(abs(err))),success=bool(f.success),budget_ok=bool(budget)))
summary={name:{str(w):max(r['max_fraction'] for r in records if r['target']==name and r['concentration_width_dex']==w) for w in [0.,.22]} for name in inputs}
checks=dict(coverage=len(records)==72,convergence=all(r['success'] for r in records),baryon_budget=all(r['budget_ok'] for r in records),relation_z0=abs(logc(12-math.log10(.671),0)-.905)<1e-12)
(out/'halo_fits.json').write_text(json.dumps(records,indent=2))
(out/'summary.json').write_text(json.dumps(dict(max_point_residual_by_target=summary,checks=checks),indent=2))
print(json.dumps(dict(summary=summary,checks=checks),indent=2));assert all(checks.values())
