#!/usr/bin/env python3
from pathlib import Path
import json,math,hashlib,datetime
O=Path(__file__).resolve().parent;R=O.parents[2];L='real_research/cross_thread_review_2026_09_26'
rec=json.loads((O/'full_records.json').read_text()); summary=[]
def compare(x,y,path='',acc=None):
 a=acc if acc is not None else dict(numeric_leaves=0,max_absolute_difference=0.,max_relative_difference=0.,numeric_failures=[],structural_failures=[],string_differences=[],timing_leaves_ignored=0)
 if path.rsplit('/',1)[-1] in {'time','wall_s','production_wall_s','seconds','secs'}:a['timing_leaves_ignored']+=1;return a
 if isinstance(x,dict) and isinstance(y,dict):
  for k in x.keys()|y.keys():
   if k not in x or k not in y:a['structural_failures'].append([path+'/'+k,'missing'])
   else:compare(x[k],y[k],path+'/'+k,a)
 elif isinstance(x,list) and isinstance(y,list):
  if len(x)!=len(y):a['structural_failures'].append([path,'length'])
  else:
   for i,(xx,yy) in enumerate(zip(x,y)):compare(xx,yy,path+'/'+str(i),a)
 elif isinstance(x,bool) or isinstance(y,bool):
  if x!=y:a['structural_failures'].append([path,x,y])
 elif isinstance(x,(float,int)) and isinstance(y,(float,int)):
  a['numeric_leaves']+=1
  if not (math.isfinite(x) and math.isfinite(y)):a['numeric_failures'].append([path,x,y,'nonfinite'])
  else:
   d=abs(x-y);q=d/max(abs(x),abs(y),1e-300);a['max_absolute_difference']=max(a['max_absolute_difference'],d);a['max_relative_difference']=max(a['max_relative_difference'],q)
   if d>1e-9+1e-10*max(abs(x),abs(y)):a['numeric_failures'].append([path,x,y,d])
 elif x!=y:a['string_differences'].append([path,x,y])
 return a
for row in rec['runs']:
 name=row['name'];slug=name.removesuffix('_MUTATE');f=slug+'_results'+('_MUTATE' if row['mutate'] else '')+'.json'
 a=json.loads((O/'mirror'/L/f).read_text());b=json.loads((R/L/f).read_text());check=compare(a,b)
 flags=all(k in b['checks'] and v['ok']==b['checks'][k]['ok'] and v['load_bearing']==b['checks'][k]['load_bearing'] for k,v in a['checks'].items())
 summary.append(dict(name=name,seconds=row['seconds'],returncode=row['returncode'],expected_rc=1 if row['mutate'] else 0,check_flags_match=flags,comparisons=check,scientific_status='matched' if row['returncode']==(1 if row['mutate'] else 0) and flags and not check['numeric_failures'] and not check['structural_failures'] else 'needs review'))
result={'status':'complete' if len(summary)==4 else 'in progress','completed_runs':len(summary),'source_inputs_unchanged':rec.get('input_hashes_after')==rec['input_hashes'],'float_comparison_tolerance':'abs <= 1e-9 + 1e-10 max(abs(values)); check booleans exact; all nonfinite values fail. Diagnostic measured strings separately retained.','runs':summary,'updated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
(O/'NUMERICAL_COMPARISON.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k!='runs'},indent=2));print([(r['name'],r['scientific_status'],r['comparisons']['max_absolute_difference']) for r in summary])
