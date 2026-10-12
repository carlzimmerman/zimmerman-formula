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
ns.update(math=math,EPS=.01)
selected(ROOT/'campaign_fresh_gravity/CFG544_settling_kinetic_consistency/cfg544.py',['phi_b_grid'],ns)
def selfenergy(r,M,eps):
    n=len(r);dm=M/n;q=(np.arange(n)+.5)/n;ss=np.sqrt(r*r+eps*eps)
    W=-M*M*np.mean(q/ss)
    outside=np.cumsum((dm/ss)[::-1])[::-1]-.5*dm/ss
    phi=-M*q/ss-outside
    return float(W),float(.5*dm*phi.sum())
u=(np.arange(262144)+.5)/262144
w,_=selfenergy(u**(1/3),1.,0.)
ck('uniform Newtonian sphere',abs(w+.6)<1e-5)
ck('MUTATE doubled self energy',abs(2*w+.6)>1e-5)
r=2.;h=1e-5;ep=.01
potential=lambda x:-1/math.sqrt(max(x,.5)**2+ep*ep)
a=-(potential(r+h)-potential(r-h))/(2*h);exact=-r/(r*r+ep*ep)**1.5
ck('symmetric pair force',abs(a/exact-1)<1e-5)
ck('MUTATE repulsive sign',-a>0 and exact<0)
rows=[]
for name,c in cells.items():
    mp=lambda r:ns['Mph_enc'](c,r);mb=lambda r:ns['Mb_enc'](c,r)
    m0=float(mp(np.array([.001]))[0]);M=float(mp(np.array([1.]))[0])-m0
    rg=np.geomspace(.001,1,20001);mg=mp(rg)-m0
    rb,pb=ns['phi_b_grid'](c);computations=[]
    for n in (131072,262144):
        q=(np.arange(n)+.5)/n;rt=np.interp(q*M,mg,rg)
        g=(mb(rt)+M*q)*rt/(rt*rt+.01**2)**1.5
        Wc,W2=selfenergy(rt,M,.01);Wb=M*np.mean(np.interp(rt,rb,pb));I=M*np.mean(rt*g)
        ck(name+str(n)+' self potential factor',abs(Wc-W2)<1e-8*max(1,abs(Wc)))
        Emax=Wc+Wb+.5*I
        state={'n':n,'M':M,'M_over_Mcat':M/c['Mcat'],'Wcc':Wc,'Wcb':Wb,'virial':I,'Emax':Emax}
        for ic in ('B','C'):
            rr=np.maximum(c['rta']*q**(1/3),.001*1.01) if ic=='B' else rt
            wi,wii=selfenergy(rr,M,.01);wb=M*np.mean(np.interp(rr,rb,pb));Ei=wi+wb+.00375*M
            state[ic]={'Einitial':float(Ei),'required_export_lower_bound_signed_over_M':float((Ei-Emax)/M)}
        computations.append(state)
    changes={ic:abs(computations[1][ic]['required_export_lower_bound_signed_over_M']-computations[0][ic]['required_export_lower_bound_signed_over_M']) for ic in ('B','C')}
    for ic in ('B','C'):ck(name+ic+' refinement',changes[ic]<1e-5)
    rows.append({'cell':name,'refinement_change':changes,'coarse':computations[0],'fine':computations[1]})
result={'checks':checks,'rows':rows,'pass':all(x['pass'] for x in checks)}
(OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print('checks',sum(x['pass'] for x in checks),len(checks));print([(r['cell'],r['fine']['B'],r['fine']['C']) for r in rows])
sys.exit(0 if result['pass'] else 1)
