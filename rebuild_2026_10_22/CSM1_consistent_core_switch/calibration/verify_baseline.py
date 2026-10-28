import json,pathlib,hashlib
D=pathlib.Path(__file__).resolve().parent;R=D.parents[2];B=R/'rebuild_2026_10_22';j=json.load(open(D/'run_002/results.json'));tests={};inputs={}
def load(p):inputs[str(p)]=hashlib.sha256(p.read_bytes()).hexdigest();return json.loads(p.read_text())
def flat(d,p=''):
 if isinstance(d,dict):return {a:b for k,v in d.items() for a,b in flat(v,p+'/'+k).items()}
 if isinstance(d,list):return {a:b for k,v in enumerate(d) for a,b in flat(v,p+f'/{k}').items()}
 return {p:d}
for name,old in [('x43','x62_x43copy_on_shpS9_L3.75_TF12.2357:12.5739_B_results.json'),('x53','x62_x53copy_on_shpS9_L3.75_TF12.2357:12.5739_results.json')]:
 ref=load(B/'CL3_one_number'/old)['footings'];act=j['baseline'][name]['result'];act=act[0]['footings'] if name=='x43' else {f:act[f] for f in ('canonical','alt')};A,C=flat(act),flat(ref);samekeys=set(A)==set(C);errors=[]
 for k in A.keys()&C.keys():
  a,b=A[k],C[k]
  if isinstance(a,(float,int)) and not isinstance(a,bool) and isinstance(b,(float,int)) and not isinstance(b,bool):
   if abs(a-b)>1e-6:errors.append((k,a,b))
  elif a!=b:errors.append((k,a,b))
 tests[name]=dict(same_keys=samekeys,n_leaves=len(C),n_different=len(errors),max_abs_numeric_diff=max([abs(A[k]-C[k]) for k in A.keys()&C.keys() if isinstance(A[k],(float,int)) and isinstance(C[k],(float,int))]+[0]),differences=errors[:5])
p=D/'baseline_full_comparison.json';p.write_text(json.dumps(dict(tests=tests,input_hashes=inputs),indent=2)+'\n');print(json.dumps(tests,indent=2))
