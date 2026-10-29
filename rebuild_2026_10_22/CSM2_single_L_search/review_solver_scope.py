"""Independent90-digit selected normalized roots and complete trace integrity."""
from pathlib import Path
import hashlib,json,math,resource,signal
import numpy as np
import mpmath as mp
resource.setrlimit(resource.RLIMIT_CPU,(120,120));signal.alarm(150)
p=Path(__file__).resolve().parent;r=p.parents[1];run=p/'solver_scope_001';paths=[Path(__file__),run/'results.json',run/'scope_inventory.json',run/'extracted_original_definitions.py.txt',p/'source_audit_scipy_1_14_1/SOURCE.json',p/'SOLVER_SCOPE_CRITERIA.md'];sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();hashes={str(f.relative_to(r)):sha(f) for f in paths};d=json.loads(paths[1].read_text());rows=d['records'];scope=json.loads(paths[2].read_text());nodes=sorted(set(row['node'] for row in rows));chosen=[nodes[0],nodes[len(nodes)//2],nodes[-1]];checks={};mp.mp.dps=90;B=lambda x:mp.log1p(x*x)+2*mp.log1p(x)-2*mp.atan(x);M=lambda v:mp.mpf(float(v));points=[]
for row in rows:
 if row['node'] not in chosen:continue
 R,Sigma,mass=map(M,[row['R'],row['Sigma'],row['M']]);target=mass/(mp.pi*Sigma*R**2);a,b=mp.mpf(1),mp.mpf(1e7)
 for _ in range(280):
  c=(a+b)/2
  if B(c)/c**2>target:a=c
  else:b=c
 x=(a+b)/2;oldlo,oldhi=map(mp.mpf,row['reference_x_bracket']);assert oldlo<=x<=oldhi;ref=R/x;error=abs(M(row['brent']['root'])-mp.log(ref));assert abs(float(error)-row['log_root_error'])<=1e-28;points.append(dict(node=row['node'],L=row['L'],reference_r0=str(ref),log_root_error=str(error)))
checks['nine_independent_roots']=len(points)==9;checks['coverage']=len(rows)==186 and len(nodes)==62 and sorted(set(row['L'] for row in rows))==[3.75,3.7505,3.751];checks['callback_counts']=all(row['brent']['function_calls']==len(row['brent']['trace']) and row['peak']['nfev']==len(row['peak']['trace']) for row in rows);checks['finite_callbacks']=all(math.isfinite(value) for row in rows for st in ['peak','brent'] for pair in row[st]['trace'] for value in pair);checks['zero_count']=sum(row['returned_callback']==0 for row in rows)==d['zero_callback_cases']==147;checks['observed_tolerance_count']=sum(row['exceeds_nominal_tolerance'] for row in rows)==d['nominal_tolerance_exceedances']==0;checks['scope_open']=scope['law_comparator'].startswith('Fixed numerical') and 'Analytic comparator all127 positive nodes if changing comparator scope' in scope['open'];checks['original_controls']=all(d['checks'].values());finger=json.loads(paths[4].read_text())['binary_fingerprints'];checks['observed_binaries_unchanged']=all(sha(Path(f))==h for f,h in finger.items());checks['source_hashes']=all(sha(r/f)==h for f,h in hashes.items());result=dict(checks=checks,selected_nodes=chosen,points=points,all_samples_within_nominal_tolerance=d['nominal_tolerance_exceedances']==0,nonclaim='Finite trace and source-scope audit, not uniform libm/solver continuum certificate',input_sha256=hashes);(p/'solver_scope_review.json').write_text(json.dumps(result,indent=2)+'\n');print('checks',len(checks),all(checks.values()),'selected',chosen);assert all(checks.values())
