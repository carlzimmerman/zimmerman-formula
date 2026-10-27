import csv,json,math,hashlib,subprocess,time,sys
from pathlib import Path
root=Path('/Users/carlzimmerman/new_physics/zimmerman-formula');out=Path(__file__).parent;t=time.time()
files=['campaign_fresh_gravity/CFG821_stiffness_from_dsph/cfg821.py','campaign_fresh_gravity/CFG821_stiffness_from_dsph/FROZEN_CRITERIA.md','campaign_fresh_gravity/CFG821_stiffness_from_dsph/cfg821_results.json','campaign_fresh_gravity/CFG821_stiffness_from_dsph/cfg821_results_MUTATE.json','campaign_fresh_gravity/CFG820_stiffness_from_globulars/cfg820.py','campaign_fresh_gravity/CFG820_stiffness_from_globulars/cfg820_results.json','campaign_fresh_gravity/CFG332_globulars_three_routes/cfg332_globulars_results.json','real_research/data/dsph/lvd_dwarf_mw.csv']
hashes={f:hashlib.sha256((root/f).read_bytes()).hexdigest() for f in files}
G,MS,PC,KPC=6.674e-11,1.989e30,3.0857e16,3.0857e19
xs=[.01,.1,.3,1,3,10,100,1000];ss=[.005,.048,.134,.358,.663,.894,.990,.998999]
def screen(x):
 if x<=xs[0]:return x/2
 if x>=xs[-1]:return 1-1/x
 for i in range(7):
  if xs[i]<=x<=xs[i+1]:return ss[i]+(ss[i+1]-ss[i])*math.log(x/xs[i])/math.log(xs[i+1]/xs[i])
def val(x):
 try:return float(x)
 except (ValueError,TypeError):return None
d=[]
for r in csv.DictReader((root/files[-1]).open()):
 mv,obs,rad=val(r.get('M_V')),val(r.get('vlos_sigma')),val(r.get('rhalf_sph_physical')) or val(r.get('rhalf_physical'))
 if mv is None or obs is None or rad is None or mv> -7.7 or r['name'] in ['LMC','SMC','Sagittarius']:continue
 d.append(dict(name=r['name'],LV=10**(.4*(4.83-mv)),so=obs,eso=val(r.get('vlos_sigma_em')) or .1*obs,rhl=rad,RGC=val(r.get('distance_gc')) or 100))
gc=[g for g in json.loads((root/files[-2]).read_text())['clusters'] if g['name']!='Pal 3']
def pred(g,a,L,ups,efe,mutation=False):
 M=ups*g['LV'];r=4/3*g['rhl']*PC;n=math.sqrt(G*M*MS/(6*r))/1000
 if L is None:return n
 y=G*M*MS/(2*r*r*a)
 if efe:y+=G*6e10*MS/(g['RGC']*KPC)**2/a
 boost=1/(-math.expm1(-math.sqrt(max(y,1e-12))))
 S=1 if L==0 else screen((r/PC)*2*math.sqrt(G*M*MS/a)/PC/L**2)
 if mutation:S=0
 return n*math.sqrt(1+S*(boost-1))
def chi(pop,a,L,ups,efe,mutation=False):return sum(math.log(g['so']/pred(g,a,L,ups,efe,mutation))**2/((g['eso']/g['so'])**2+(math.log(10)*.15/2)**2) for g in pop)
checks=[]
def check(n,b):
 checks.append({'name':n,'pass':bool(b)})
 if not b:raise AssertionError(n)
check('11 dwarfs and 3 globulars',len(d)==11 and len(gc)==3)
source=json.loads((root/files[2]).read_text());grid=[math.exp(math.log(5.75)+j*math.log(3000/5.75)/399) for j in range(400)]
res={}
for foot,a in [('canonical',9.3603e-11),('alt',1.1312e-10)]:
 for efe in [False,True]:
  lab=('law+EFE' if efe else 'isolated law')+'|'+foot
  vals=[chi(d,a,L,2,efe) for L in grid];c0=chi(d,a,0,2,efe);cn=chi(d,a,None,2,efe);cm=min(c0,min(vals));upper=max(L for L,c in zip(grid,vals) if c-cm<=3.84)
  for key,value in [('chi2_unscreened',c0),('chi2_newton',cn),('L95_up',upper)]:check(lab+' '+key,abs(value-source[lab][key])<1e-8)
  # Mutation flat profile must use its OWN attainable minimum.
  flat=[chi(d,a,L,2,efe,True) for L in [5.75,24,3000]]
  check(lab+' zero-screen own profile flat',max(flat)-min(flat)<1e-10)
  # Same conditional proxy, shared L; nuisance values remain group specific.
  fine=[math.exp(math.log(.01)+j*math.log(1e7)/1999) for j in range(2000)]
  gd=[chi(d,a,L,2,efe) for L in fine];gg=[chi(gc,a,L,1.6,True) for L in fine]
  pair=[x+y for x,y in zip(gd,gg)];j=min(range(len(pair)),key=pair.__getitem__)
  rows=[{'name':g['name'],'obs_over_unscreened':g['so']/pred(g,a,0,2,efe),'unscreened_contribution':math.log(g['so']/pred(g,a,0,2,efe))**2/((g['eso']/g['so'])**2+(math.log(10)*.15/2)**2)} for g in d]
  res[lab]={'source_replayed':{'chi2_unscreened':c0,'L95_up':upper},'shared_L_grid_best_pc':fine[j],'joint_chi2':pair[j],'joint_tension_delta_from_separate_minima':pair[j]-min(gd)-min(gg),'dwarf_chi2_at_shared_best':gd[j],'globular_chi2_at_shared_best':gg[j],'top_unscreened_residuals':sorted(rows,key=lambda x:x['unscreened_contribution'],reverse=True)[:4]}
check('input files unchanged',hashes=={f:hashlib.sha256((root/f).read_bytes()).hexdigest() for f in files})
r={'claim_id':'CE-FM-076','status':'completed','checks':checks,'n_checks':len(checks),'results':res,'scope':'Independent stdlib replay of frozen CFG821 proxy and exploratory common-L profile with CFG820 primary; grid not calibrated coverage or physical completion. No original scripts or live experiments run.'}
(out/'results.json').write_text(json.dumps(r,indent=2)+'\n')
m={'claim_id':'CE-FM-076','head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),'command':['python3',str(Path(__file__))],'software':sys.version,'input_sha256':hashes,'input_unchanged':True,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'result_sha256':hashlib.sha256((out/'results.json').read_bytes()).hexdigest(),'seconds':time.time()-t,'bounds':{'frozen_grid_points':400,'exploratory_grid_points':2000,'dwarfs':11,'globulars':3},'limits':'stdlib, sequential small loops; no hard memory cap; not a mathbox v2 runner manifest'}
(out/'execution_receipt.json').write_text(json.dumps(m,indent=2)+'\n')
print(json.dumps({'n_checks':len(checks),'seconds':m['seconds'],'results':res},indent=2))
