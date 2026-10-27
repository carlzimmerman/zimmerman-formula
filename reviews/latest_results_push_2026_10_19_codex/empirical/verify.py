import ast,hashlib,json,math,pathlib,numpy as np
P=pathlib.Path(__file__).resolve().parent
# Extract only our saved deterministic fit functions; do not execute main output code.
t=ast.parse((P/'discriminate.py').read_text());nodes=[n for n in t.body if isinstance(n,ast.FunctionDef) and n.name in ('golden','fit_predict')]
ns={'math':math,'np':np};exec(compile(ast.Module(body=nodes,type_ignores=[]),'<audited-fit-functions>','exec'),ns)
fit=ns['fit_predict'];checks={}
for model,param in [('additive',25.),('multiplicative',3.)]:
 rows=[{'sl2':x,'so':math.sqrt(x+param if model=='additive' else x*param)} for x in (1.,4.,9.,25.,100.)]
 result,_=fit(rows,rows,model);assert abs(result['parameter']-param)<2e-6 and result['rmse_log_sigma']<2e-9
 checks[model+'_synthetic_recovery']=result
R=json.loads((P/'run/result.json').read_text());grid_checks=[]
for foot in ('canonical','alt'):
 rows=R['footings'][foot]['rows']
 for lab,sub in [('all',rows),('low_g',[r for r in rows if r['lgbar']<-11.9]),('mw',[r for r in rows if r['host']=='mw']),('m31',[r for r in rows if r['host']=='m_031']),('mw_low',[r for r in rows if r['host']=='mw'and r['lgbar']<-11.9]),('m31_low',[r for r in rows if r['host']=='m_031'and r['lgbar']<-11.9])]:
  sol,_=fit(sub,sub,'additive');A=sol['parameter'];sl2=np.array([r['sl2'] for r in sub]);yo=np.log10([r['so'] for r in sub]);grid=np.expm1(np.linspace(0,math.log1p(10*max(r['so']**2 for r in sub)),10001));obj=np.mean((yo[None,:]-.5*np.log10(sl2[None,:]+grid[:,None]))**2,axis=1)
  loss=sol['rmse_log_sigma']**2;assert loss<=obj.min()+1e-13
  grid_checks.append({'foot':foot,'subset':lab,'A':A,'loss':loss,'minimum_grid_loss':float(obj.min())})
checks['all_additive_minima_beat_10001_point_grid']=grid_checks
src=json.loads((P/'source_provenance.json').read_text());base=pathlib.Path(src['original_root']);observed={f:hashlib.sha256((base/f).read_bytes()).hexdigest() for f in src['sha256']};checks['original_source_hashes_unchanged']=(observed==src['sha256']);assert checks['original_source_hashes_unchanged']
checks['original_source_hashes_observed_after']=observed
(P/'verify_run/result.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps(checks,indent=2))
