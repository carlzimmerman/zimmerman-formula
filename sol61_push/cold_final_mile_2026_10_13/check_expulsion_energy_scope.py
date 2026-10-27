"""CE-FM-068: exact shell Hamiltonian/work and stationary rotating controls."""
import json,math,sys,ast
from pathlib import Path
import numpy as np
import sympy as s
p=Path('campaign_fresh_gravity/CFG787_surplus_angular_momentum');rec=json.loads((p/'cfg787_results.json').read_text());mut=json.loads((p/'cfg787_results_MUTATE.json').read_text());checks=[]
def ck(n,v):
 checks.append({'name':n,'pass':bool(v)})
 if not v:raise AssertionError(n)
r,M,c,j,dm=s.symbols('r M c j dm',positive=True)
U=-M/r+c/(3*r**3)+j**2/(2*r**2)
a=-M/r**2+c/r**4+j**2/r**3
ck('exact Hamiltonian acceleration',s.simplify(-s.diff(U,r)-a)==0)
ck('explicit work derivative',s.diff(U,M)==-1/r)
# Radial velocity and rank-fixed shell energy; sorted-rank potential is
# continuous at equal-radius crossings, though force derivatives can jump.
for pp in [1.5,3.]:
 N=4000;mtot=math.sqrt(pp)*49.5;dd=mtot/N;q=(np.arange(N)+.5)/N;rr=.5+q*49.5;mi=.5+dd*np.arange(N)
 ci=mi*mi+mi*dd+dd*dd/3
 cube=((mi+dd)**3-mi**3)/(3*dd)
 ck('finite-shell cubic identity p'+str(pp),np.max(abs(ci-cube)/ci)<1e-11)
 eps=np.random.default_rng(787).uniform(0,1,N);jj=eps*np.sqrt(rr*(pp+mi))
 ap=-pp/rr**2+ci/rr**4;ar=ap+jj**2/rr**3
 ck('angular term adds outward acceleration p'+str(pp),np.all(ar>=ap))
 # A finite-shell stationary rank control with exactly the same dm, CORE,
 # shell labels and total cold mass; larger radii and j are NEW initial data.
 alpha=.8;req=np.sqrt(ci/((1-alpha)*pp));jeq2=alpha*pp*req
 aa=-pp/req**2+ci/req**4+jeq2/req**3
 ck('equilibrated rotating force p'+str(pp),np.max(abs(aa))<1e-13)
 ck('equilibrated radii ordered and outside wall p'+str(pp),np.all(np.diff(req)>0) and req.min()>.5)
 if pp==1.5:source_stats=[]
 source_stats.append({'peak_Mb':pp,'source_fraction_outward_before_loss':float(np.mean(ar>0)),'source_rotation_added_energy':float(np.sum(dd*jj**2/(2*rr**2))),'equilibrium_control_alpha':alpha,'equilibrium_control_min_radius':float(req.min()),'equilibrium_control_max_radius':float(req.max()),'cold_stock_unchanged':mtot,'max_equilibrium_acceleration':float(np.max(abs(aa)))})
# Recompute frozen class from saved snapshots only, no trajectory rerun.
def classify(f):
 if all(x<=.2 for x in f[1:4]):return 'EXPELLED'
 if f[1]>=.5 and f[2]>=.5:return 'RETAINED'
 return 'PARTIAL'
rows=[]
for key,v in rec.items():
 if not isinstance(v,dict) or 'res' not in v:continue
 ck('saved class '+key,classify(v['res']['200']['relic'])==v['cls'])
 pp=float(key.split('|')[0][1:])
 for t,snap in v['res'].items():
  ck('relic normalization '+key+t,np.allclose((np.array(snap['m_over_r'])-1)/(math.sqrt(pp)-1),snap['relic'],rtol=1e-12,atol=1e-12))
 rows.append({'case':key,'frozen_class':v['cls'],'class_if_same_formula_applied_to_2000':classify(v['res']['2000']['relic']),'r5_8_11_at200':v['res']['200']['relic'][1:4],'r5_8_11_at2000':v['res']['2000']['relic'][1:4]})
ck('one partial source case',sum(z['frozen_class']=='PARTIAL' for z in rows)==1)
ck('mutation stored retained',all(v['cls']=='RETAINED' for v in mut.values() if isinstance(v,dict) and 'cls' in v))
# A source-structure observation, NOT a substitute for a missing energy test.
txt=(p/'cfg787.py').read_text();tree=ast.parse(txt);names={n.id for n in ast.walk(tree) if isinstance(n,ast.Name)}
ck('no source energy/work diagnostic names',not ({'energy','work','Etot','E0','K2'} & names))
out={'claim_id':'CE-FM-068','n_checks':len(checks),'all_pass':all(z['pass'] for z in checks),'checks':checks,'initial_state_controls':source_stats,'saved_case_scope':rows,'scope':'Exact force/Hamiltonian and finite-array equilibrium control; no time integration, measured drift, actual escape census or validation of omitted frozen K2. New equilibria change initial radii/angular momenta and are not an original frozen-run replacement.'}
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'checks':len(checks),'all_pass':out['all_pass'],'initial_state_controls':source_stats}))
