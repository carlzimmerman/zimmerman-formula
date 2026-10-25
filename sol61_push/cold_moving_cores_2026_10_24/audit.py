"""Audit saved finite computations; this command does not rerun their dynamics."""
import pathlib,json,hashlib,sys,platform,resource,numpy as np,scipy
P=pathlib.Path(__file__).resolve().parent;ROOT=P.parents[1];out=pathlib.Path(sys.argv[1]);records=[];pins=0
for f in list((P/'runs').glob('*.json'))+[P/'analysis.json']:
 q=json.loads(f.read_text());aa=q.get('source_hashes_before',q.get('inputs_before'));bb=q.get('source_hashes_after',q.get('inputs_after'))
 if aa is not None:
  assert aa==bb,(f,'before/after')
  for path,sha in aa.items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==sha,(f,path);pins+=1
for tag in ['draco','sextans']:
 a=json.loads((P/'runs'/f'{tag}_track.json').read_text());b=json.loads((P/'runs'/f'{tag}_momentum.json').read_text());fa=np.load(P/'runs'/f'{tag}_track_fields.npz');fb=np.load(P/'runs'/f'{tag}_momentum_fields.npz');field_difference=float(np.linalg.norm(fa['final']-fb['final'])/np.linalg.norm(fa['final']));assert field_difference<1e-12;assert a['source_hashes_before']==a['source_hashes_after'];h=a['history'][-1];assert abs(h['M_residual'])<1e-8 and abs(h['E_residual'])<.01 and abs(h['J_residual'])<.01
 mom=json.loads((P/'runs'/f'{tag}_momentum_momentum.json').read_text());mh=mom['history'];tr=json.loads((P/'runs'/f'{tag}_track_tracking.json').read_text());assert abs(mh[0]['Pz_code']-tr['history'][0]['global_P_code'][2])<1e-12
 st=json.loads((P/'runs'/f'{tag}_track_stars_advected.json').read_text());diff=[]
 for control in [False,'advected']:
  x=next(z for z in st['results'] if z['dt']==.02 and z['static_cold']==control)['history'][-1];y=next(z for z in st['results'] if z['dt']==.01 and z['static_cold']==control)['history'][-1];diff.append(abs(x['r50_pc']/y['r50_pc']-1));assert diff[-1]<1e-4
 residual=mh[-1]['remaining_plus_sink_minus_initial_code'];records.append(dict(galaxy=tag,tracking_and_momentum_final_field_relative_difference=field_difference,M_E_J_gates_pass=True,star_r50_dt_refinement_max_relative_difference=max(diff),Pz_nonabsorber_residual_code=residual,Pz_nonabsorber_residual_fraction_of_initial_net_Pz=residual/mh[0]['Pz_code'],Pz_residual_equivalent_remnant_bulk_kms=residual/h['M']*a['physical']['Vunit_kms'],linear_momentum_conservation_verified=False))
checks=json.loads((P/'checks_result.json').read_text());assert checks['full_multipole_gradient_max_absolute_error']<1e-7
out.write_text(json.dumps(dict(status='finite records reconciled; formation/profile and linear momentum closure NOT established',audited_pin_instances=pins,results=records,force_checks=checks,software=dict(Python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__),peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,nonclaims=['No rerun of cold or stellar dynamics by this audit','No observational stellar DF fit','No matched Fornax/Leo I formation controls','No full theory or current-v3 bridge']),indent=2)+'\n');print(out)
