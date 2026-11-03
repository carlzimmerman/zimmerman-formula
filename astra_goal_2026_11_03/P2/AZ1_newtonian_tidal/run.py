"""Bounded AZ1 necessary-gate experiment; run from repository root."""
import hashlib, json, math, platform, subprocess, time
from pathlib import Path
import numpy as np
import scipy
from scipy.special import erf
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
start=time.time()
inputs=[HERE/'CRITERIA.md',Path(__file__).resolve()]
sha=lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
before={str(p.relative_to(ROOT)):sha(p) for p in inputs}
def quad(a0,nr,nm,null=False):
    eta=2.32e-10/a0
    u=np.linspace(math.log(1e-7),math.log(1e5),nr); r=np.exp(u); x=r/0.5
    g=np.empty_like(r); small=x<1e-3
    g[small]=math.sqrt(2/math.pi)/3*r[small]/0.5**3
    g[~small]=(erf(x[~small]/math.sqrt(2))-math.sqrt(2/math.pi)*x[~small]*np.exp(-x[~small]**2/2))/r[~small]**2
    mu,w=np.polynomial.legendre.leggauss(nm); m=mu[None,:]; g=g[:,None]
    y=np.sqrt(eta**2+g*g+2*eta*g*m)
    A=np.zeros_like(y) if null else np.sqrt(0.25+1/y)-0.5
    q=abs(1.5*float(np.trapz((A*(eta*(3*m-5*m**3)+g*(1-3*m*m)))@w/r,u)))
    rM=math.sqrt(6.6743e-11*1.98892e30/a0)
    Q=1.5*a0/rM*q
    return {'q':q,'Q2':Q,'ratio':Q/5.2e-27}
res={'disclaimer':'κ = ½ FITTED; not theory closed','assertion_tested':'point-mass Newtonian tidal reconstruction and inherited quadrature Cassini necessary gate','free_parameters':[{'name':'kappa','value':0.5,'status':'FITTED'}],'footings':{}}
for foot,a0,ref in [('canonical',9.3603e-11,0.4806),('alt',1.1312e-10,1.057)]:
    errors=[]; mutations=[]
    for GM in [1.,8.]:
        for r in [0.25,1.,4.]:
            t=math.sqrt(6)*GM/r**3; d=3*t/r; est=27/math.sqrt(6)*t**4/d**3
            errors += [abs(est/GM-1),abs(math.sqrt(est/a0)/math.sqrt(GM/a0)-1)]
            mutations.append(abs(2*est/GM-1))
    low=quad(a0,4000,80); high=quad(a0,8000,160); null=quad(a0,4000,80,True)
    checks={'mass_xi_identity':max(errors)<=1e-12,'mutate_bites':min(mutations)>1e-12,'null':null['q']<=1e-14,'record_reproduction':abs(high['ratio']-ref)<=0.005,'convergence':abs(high['ratio']-low['ratio'])<=0.002}
    res['footings'][foot]={'a0':a0,'coarse':low,'fine':high,'margin':1-high['ratio'],'identity_max_error':max(errors),'mutate_min_error':min(mutations),'null':null,'checks':checks,'label':('PASS' if high['ratio']<=1 else 'FAIL') if all(checks.values()) else 'NO VERDICT','scope':'Cassini necessary gate only; MW/dwarfs/SPARC NOT EVALUABLE (not run)'}
res['label']='FAIL' if all(all(v['checks'].values()) for v in res['footings'].values()) and any(v['label']=='FAIL' for v in res['footings'].values()) else 'NO VERDICT'
out=HERE/'results.json';out.write_text(json.dumps(res,indent=2)+'\n')
manifest={'schema_version':2,'claim_id':'AZ1','repository':{'commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'dirty':True},'command':['python3','astra_goal_2026_11_03/P2/AZ1_newtonian_tidal/run.py'],'environment':{'software':[{'name':'Python','version':platform.python_version()},{'name':'numpy','version':np.__version__},{'name':'scipy','version':scipy.__version__}],'hardware':platform.machine()},'mathematics':{'assertion_tested':res['assertion_tested'],'coefficient_domain':'IEEE float64','conventions':'SI; radial integral in r/rM','inputs':list(before),'bounds':{'nr':[4000,8000],'nmu':[80,160],'r':[1e-7,1e5]},'non_claims':['No full field solve','No observational score beyond Cassini quadrature']},'randomness':{'used':False,'generator':'','seed':None},'run':{'started_at':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime(start)),'runtime_seconds':time.time()-start,'exit_status':0,'status':'completed','resource_limits':{'memory_bytes':None,'cpu_seconds':None,'max_cores':None,'max_threads':1}},'outputs':[{'path':str(out.relative_to(ROOT)),'sha256':sha(out),'kind':'result'}],'checks':[{'name':foot+' '+k,'passed':v} for foot,d in res['footings'].items() for k,v in d['checks'].items()],'result':res['label'],'residual_risks':['inherited quadrature approximation; no independent Cassini field solution'],'input_artifacts':[{'path':p,'sha256':h,'sha256_after':sha(ROOT/p)} for p,h in before.items()],'declared_results':[str(out.relative_to(ROOT))]}
(HERE/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(res,indent=2))
