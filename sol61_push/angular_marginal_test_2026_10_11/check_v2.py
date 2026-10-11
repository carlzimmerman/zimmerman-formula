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
for name,c in cells.items():
    mb=lambda r:ns['Mb_enc'](c,r)
    mp=lambda r:ns['Mph_enc'](c,r)
    m0=float(mp(np.array([.001]))[0]);mass=float(mp(np.array([1.]))[0])-m0
    def g(r):
        r=np.asarray(r); mc=np.where(r<1,mp(np.minimum(r,1))-m0,mass)
        return (mb(r)+mc)*r/(r*r+.01**2)**1.5
    edges=np.r_[0,np.geomspace(1e-4,2*math.sqrt(float(g(np.array([1.]))[0])),15),np.inf]
    initial={}; qerr={}
    rg=np.geomspace(.001,1,20001); mg=mp(rg)-m0
    for ic in ('B','C'):
        vals=[]
        for nq in (8192,16384):
            u=(np.arange(nq)+.5)/nq
            rr=np.maximum(c['rta']*u**(1/3),.001*1.01) if ic=='B' else np.interp(u*mass,mg,rg)
            cdf=-np.expm1(-edges[:,None]**2/(2*.05**2*rr[None,:]**2));vals.append(np.diff(cdf.mean(axis=1)))
        initial[ic]=vals[-1];qerr[ic]=float(np.max(abs(vals[1]-vals[0])))
        ck(name+ic+' quadrature',qerr[ic]<=1e-5)
    for nb in (24,48):
        F=lib.Field(g,.001,1);L=lib.Library(F,.001,1,nb=nb,sub=2)
        target=np.diff(mp(np.exp(L.ub)))/mass
        A=L.P.T; ji=np.searchsorted(edges,L.L,side='right')-1
        J=np.zeros((len(edges)-1,len(L.L)));J[ji,np.arange(len(L.L))]=1
        ck(name+str(nb)+' partition',np.max(abs(L.P.sum(axis=1)-1))<1e-10)
        witness=L.w/L.w.sum();Aj=np.vstack([A,J]);bw=np.einsum("ij,j->i",Aj,witness,optimize=False)
        ck(name+str(nb)+" finite witness",np.all(np.isfinite(bw)))
        ctrl=fit(Aj,bw);ck(name+str(nb)+' witness',ctrl.get('residual',1)<1e-7)
        den=fit(A,target)
        impossible=np.zeros(J.shape[0]);impossible[-1]=1
        ck(name+str(nb)+' empty bin',not np.any(J[-1]))
        mut=fit(Aj,np.r_[target,impossible]);ck(name+str(nb)+' MUTATE impossible',mut.get('t',0)>1e-3)
        # Dropping J must allow the known witness density, regardless of impossible j target.
        drop=fit(A,bw[:nb]);ck(name+str(nb)+' MUTATE dropped constraint',drop.get('residual',1)<1e-7)
        for ic in ('B','C'):
            fitj=fit(Aj,np.r_[target,initial[ic]])
            rows.append({'cell':name,'nb':nb,'ic':ic,'quadrature_error':qerr[ic],'target_mass_over_Mcat':mass/c['Mcat'],'density_only':public(den),'joint':public(fitj)})
        print(name,nb,public(den),[public(fit(Aj,np.r_[target,initial[ic]])) for ic in ()],flush=True)
result={'rows':rows,'checks':checks,'pass':all(x['pass'] for x in checks),'scope':'Finite orbit library; not continuum proof; initial benchmark distributions not cosmological derivations.'}
(OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print('checks',sum(x['pass'] for x in checks),'/',len(checks));print([(r['cell'],r['nb'],r['ic'],r['joint'].get('t')) for r in rows])
sys.exit(0 if result['pass'] else 1)
