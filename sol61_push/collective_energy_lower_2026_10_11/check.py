import os
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','MKL_NUM_THREADS'): os.environ[k]='1'
import ast,json,math,sys,importlib.util
from pathlib import Path
import numpy as np
from scipy.optimize import brentq,linprog
from scipy.sparse import csr_matrix,vstack,hstack
ROOT=Path.cwd(); OUT=Path(sys.argv[1]);OUT.mkdir(exist_ok=True,parents=True)
P626=ROOT/'campaign_fresh_gravity/CFG626_kernel_recheck_anisotropic_target'
def selected(path,names,ns):
    tree=ast.parse(path.read_text()); nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
    assert {n.name for n in nodes}==set(names)
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(path),'exec'),ns)
ns={'np':np};selected(P626/'cfg626.py',['h_rar','dh_rar','nu_m1_mono'],ns)
yp=brentq(lambda y:float(ns['dh_rar'](y)),1,5);hp=float(ns['h_rar'](yp));yg=10**np.linspace(-12,12,240001)
dh=np.maximum(ns['dh_rar'](yg),.05*hp/(yg+yp));hm=float(ns['h_rar'](yg[0]))+np.r_[0,np.cumsum(.5*(dh[1:]+dh[:-1])*np.diff(yg))]
ns.update(LYG=np.log10(yg),H_MONO=hm,nu_m1=ns['nu_m1_mono'])
selected(ROOT/'campaign_fresh_gravity/CFG544_settling_kinetic_consistency/cfg544.py',['Mb_enc','Mph_enc'],ns)
spec=importlib.util.spec_from_file_location('lib',ROOT/'campaign_fresh_gravity/CFG620_anisotropic_velocity_target/cfg620_lib.py');lib=importlib.util.module_from_spec(spec);spec.loader.exec_module(lib)
cells=json.loads((P626/'cfg626_results_mono.json').read_text())['cells']
checks=[]; rows=[]
def ck(name,ok):
    checks.append({'name':name,'pass':bool(ok)})
def fit(A,b):
    A=csr_matrix(A); one=csr_matrix(-np.ones((len(b),1)))
    res=linprog(np.r_[np.zeros(A.shape[1]),1.],A_ub=vstack([hstack([A,one]),hstack([-A,one])]),b_ub=np.r_[b,-b],bounds=(0,None),method='highs',options={'time_limit':3.,'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9})
    if res.status!=0:return {'status':int(res.status),'message':res.message}
    y=res.x[:-1];err=float(np.max(np.abs(A@y-b)))
    return {'status':0,'t':float(res.x[-1]),'residual':err,'mass':float(y.sum()),'feasible':bool(err<=1e-6 and abs(y.sum()-1)<=1e-6),'y':y}
def public(d):return {k:v for k,v in d.items() if k!='y'}
from scipy.integrate import quad
import sympy as sp
r=sp.symbols('r',positive=True);p=sp.Function('p')(r);pt=sp.Function('pt')(r);rho=sp.Function('rho')(r);g0=sp.Function('g')(r)
identity=sp.expand(r**3*(sp.diff(p,r)+(2*p-pt)/r+rho*g0)-sp.diff(r**3*p,r)+(p+pt)*r**2-rho*g0*r**3)
ck('symbolic Jeans boundary',identity==0)
r0=.2;R=1.;dp=.5*(R*R-r0*r0);I=4*math.pi*(R**5-r0**5)/5
K=6*math.pi*((R**2/2)*(R**3-r0**3)/3-(R**5-r0**5)/10)
B=4*math.pi*r0**3*dp
ck('harmonic kinetic interval',I/2-B<=K<=I/2)
ck('harmonic exact boundary',abs(2*K-I+B)<1e-12)
ck('MUTATE pressure sign',abs(2*K-I-B)>1e-5)
v2=R**2-r0**2
ck('radial saturation',abs(v2-2*dp)<1e-12)
ck('MUTATE speed factor',abs(v2-dp)>1e-5)
prior=json.loads((ROOT/'sol61_push/collective_energy_gate_2026_10_11/run/results.json').read_text())
rows=[]
for old in prior['rows']:
    name=old['cell'];c=cells[name];v=old['fine'];M=v['M'];ri=.001
    mp=lambda x:ns['Mph_enc'](c,np.asarray(x));mb=lambda x:ns['Mb_enc'](c,np.asarray(x))
    m0=float(mp(ri))
    def gf(x):return (mb(x)+mp(x)-m0)*x/(x*x+.01**2)**1.5
    dp,err=quad(lambda x:float(gf(x)),ri,1,epsabs=1e-10,epsrel=1e-10,limit=500)
    grid=np.geomspace(ri,1,32769);trap=float(np.trapz(gf(grid),grid))
    ck(name+' potential quadrature',abs(dp-trap)<=1e-5*max(1,abs(dp)))
    deriv=[]
    for frac in (1e-4,5e-5):
        h=ri*frac;deriv.append(float((-3*mp(ri)+4*mp(ri+h)-mp(ri+2*h))/(2*h)))
    ck(name+' derivative refinement',abs(deriv[1]-deriv[0])<=1e-4*max(abs(deriv[1]),1e-20))
    bound=ri*deriv[1]*dp;Klo=max(0,v['virial']/2-bound);Elo=v['Wcc']+v['Wcb']+Klo
    rows.append({'cell':name,'potential_drop':dp,'Mprime_inner':deriv[1],'inner_pressure_K_bound':bound,'Klower_over_M':Klo/M,'Kupper_over_M':v['virial']/(2*M),'signed_import_over_M':{ic:(Elo-v[ic]['Einitial'])/M for ic in ('B','C')}})
result={'checks':checks,'rows':rows,'pass':all(x['pass'] for x in checks)}
(OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));sys.exit(0 if result['pass'] else 1)
