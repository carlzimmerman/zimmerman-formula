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
    res=linprog(np.r_[np.zeros(A.shape[1]),1.],A_ub=vstack([hstack([A,one]),hstack([-A,one])]),b_ub=np.r_[b,-b],A_eq=csr_matrix(np.r_[np.ones(A.shape[1]),0.][None,:]),b_eq=[1.],bounds=(0,None),method='highs',options={'time_limit':3.,'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9})
    if res.status!=0:return {'status':int(res.status),'message':res.message}
    y=res.x[:-1];err=float(np.max(np.abs(A@y-b)))
    return {'status':0,'t':float(res.x[-1]),'residual':err,'mass':float(y.sum()),'feasible':bool(err<=1e-6 and abs(y.sum()-1)<=1e-6),'y':y}
def public(d):return {k:v for k,v in d.items() if k!='y'}
from scipy.integrate import quad,solve_ivp
from numpy.polynomial.legendre import leggauss
RIN=.001
RAD=np.geomspace(RIN,1,25)[1:]
def wall(phi,ra,j,radii,n=256):
    ra=np.asarray(ra);j=np.asarray(j)
    speed_wall=2*(phi(ra)-phi(np.full_like(ra,RIN)))-j*j*(1/RIN**2-1/ra**2)
    if np.any(speed_wall<=0):raise ValueError('not a wall-impact orbit')
    nodes,weights=leggauss(n); nodes=(nodes+1)/2;weights=weights/2
    def integ(lo):
        u=1-(1-lo[:,None])*(1-nodes)**2
        r=ra[:,None]-(ra[:,None]-RIN)*u*u
        v2=2*(phi(ra)[:,None]-phi(r))-j[:,None]**2*(1/r**2-1/ra[:,None]**2)
        if np.any(v2<=0):raise ValueError('nonpositive interior radial speed')
        values=2*(ra[:,None]-RIN)*u/np.sqrt(v2)
        return np.sum(values*weights*2*(1-lo[:,None])*(1-nodes),axis=1)
    half=integ(np.zeros(len(ra)))
    columns=[]
    for radius in radii:
        lo=np.sqrt(np.maximum((ra-radius)/(ra-RIN),0))
        columns.append(integ(lo)/half)
    return 2*half,np.array(columns)
# independent analytic/ODE validation in harmonic field.
ph=lambda r:np.asarray(r)**2/2
validation=[]
for ra in (.1,.5,1.):
    jc=math.sqrt(2*(ph(ra)-ph(RIN))/(1/RIN**2-1/ra**2))
    for frac in (0.,.5,.9):
        j=frac*jc;ts=[]
        for n in (128,256):
            tr,pp=wall(ph,np.array([ra]),np.array([j]),np.array([ra/2,ra]),n);ts.append(float(tr[0]))
        E=ph(ra)+j*j/(2*ra**2)
        # independent r-space adaptive quadrature (integrable outer endpoint).
        tq=2*quad(lambda r:1/math.sqrt(2*(E-ph(r))-j*j/r**2),RIN,ra,epsabs=1e-10,epsrel=1e-9)[0]
        ck(f'harmonic {ra} {frac} quadrature',abs(ts[1]/tq-1)<1e-5)
        ck(f'harmonic {ra} {frac} refinement',abs(ts[1]/ts[0]-1)<1e-5)
        ck(f'harmonic {ra} {frac} normalization',abs(pp[-1,0]-1)<1e-10)
        if frac==0:
            exact=2*math.acos(RIN/ra)
            ck(f'harmonic {ra} analytic',abs(ts[1]/exact-1)<1e-5)
            ck(f'MUTATE double period {ra}',abs(2*ts[1]/exact-1)>1e-5)
        validation.append({'ra':ra,'fraction':frac,'period':ts[1],'quad':tq})
ra=.5;j=.5*RIN*ra
def ode(t,y):return [y[1],j*j/y[0]**3-y[0]]
def hit(t,y):return y[0]-RIN
hit.terminal=True;hit.direction=-1
first=solve_ivp(ode,(0,4),[ra,0],events=hit,rtol=1e-10,atol=1e-12,method='DOP853')
def apo(t,y):return y[1]
apo.terminal=True;apo.direction=-1
ret=solve_ivp(ode,(0,4),[RIN,-first.y_events[0][0,1]],events=apo,rtol=1e-10,atol=1e-12,method='DOP853')
tr,_=wall(ph,np.array([ra]),np.array([j]),[ra]);direct=first.t_events[0][0]+ret.t_events[0][0]
ck('direct reflected period',abs(direct/tr[0]-1)<1e-5)
try:wall(ph,np.array([.5]),np.array([.01]),[.5]);rejected=False
except ValueError:rejected=True
ck('MUTATE forbidden wall orbit',rejected)
for name,c in cells.items():
    mb=lambda r:ns['Mb_enc'](c,r);mp=lambda r:ns['Mph_enc'](c,r)
    m0=float(mp(np.array([RIN]))[0]);mass=float(mp(np.array([1.]))[0])-m0
    def g(r):
        r=np.asarray(r);mc=np.where(r<1,mp(np.minimum(r,1))-m0,mass)
        return (mb(r)+mc)*r/(r*r+.01**2)**1.5
    edges=np.r_[0,np.geomspace(1e-4,2*math.sqrt(float(g(np.array([1.]))[0])),15),np.inf]
    initial={};qerr={};rg=np.geomspace(RIN,1,20001);mg=mp(rg)-m0
    for ic in ('B','C'):
        vals=[]
        for nq in (1048576,2097152):
            u=(np.arange(nq)+.5)/nq
            rr=np.maximum(c['rta']*u**(1/3),RIN*1.01) if ic=='B' else np.interp(u*mass,mg,rg)
            cdf=np.array([np.mean(-np.expm1(-edge**2/(2*.05**2*rr**2))) for edge in edges]);vals.append(np.diff(cdf))
        initial[ic]=vals[-1];qerr[ic]=float(np.max(abs(vals[1]-vals[0])))
        ck(name+ic+' quadrature',qerr[ic]<=1e-7)
    for nb in (24,48):
        F=lib.Field(g,RIN,1);L=lib.Library(F,RIN,1,nb=nb,sub=2)
        target=(mp(RAD)-m0)/mass
        A=np.cumsum(L.P,axis=1)[:,np.arange(nb//24-1,nb,nb//24)].T
        u=np.linspace(math.log(RIN),0,2*nb+1);ar=np.exp((u[1:]+u[:-1])/2)
        ra=np.repeat(ar,24);frac=np.tile(np.linspace(0,.999,24),len(ar))
        jc=np.sqrt(2*(F.phi(ra)-F.phi(np.full_like(ra,RIN)))/(1/RIN**2-1/ra**2));jl=jc*frac
        period,W=wall(F.phi,ra,jl,RAD)
        ck(name+str(nb)+' wall normalization',np.max(abs(W[-1]-1))<1e-10)
        ck(name+str(nb)+' wall finite',np.all(np.isfinite(W)) and np.all(np.isfinite(period)))
        ck(name+str(nb)+' cumulative order',np.min(np.diff(W,axis=0))>-1e-10)
        for mode in ('natural','augmented'):
            jall=L.L if mode=='natural' else np.r_[L.L,jl]
            Ar=A if mode=='natural' else np.hstack([A,W])
            ji=np.searchsorted(edges,jall,side='right')-1
            J=np.zeros((len(edges)-1,len(jall)));J[ji,np.arange(len(jall))]=1
            Aj=np.vstack([Ar,J]);witness=np.ones(len(jall))/len(jall)
            bw=np.einsum('ij,j->i',Aj,witness,optimize=False)
            ctrl=fit(Aj,bw);ck(name+str(nb)+mode+' witness',ctrl.get('residual',1)<1e-7)
            imp=np.zeros(J.shape[0]);imp[-1]=1;mut=fit(Aj,np.r_[target,imp]);ck(name+str(nb)+mode+' impossible',mut.get('t',0)>1e-3)
            den=fit(Ar,target)
            for ic in ('B','C'):
                b=np.r_[target,initial[ic]];res=fit(Aj,b)
                tag=f'{name}_{nb}_{mode}_{ic}'
                if res.get('feasible'):np.savez_compressed(OUT/(tag+'.npz'),matrix=Aj,target=b,weights=res['y'],j=jall)
                rows.append({'cell':name,'nb':nb,'mode':mode,'ic':ic,'quadrature_error':qerr[ic],'density_only':public(den),'joint':public(res)})
        print(name,nb,flush=True)
result={'rows':rows,'checks':checks,'validation':validation,'pass':all(x['pass'] for x in checks)}
(OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print('checks',sum(x['pass'] for x in checks),'/',len(checks))
sys.exit(0 if result['pass'] else 1)
