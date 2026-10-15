import argparse,json,time
from model import *
p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--cache',required=True);p.add_argument('--controls',required=True);p.add_argument('--convention',choices=['native_h','legacy_physical'],default='native_h');p.add_argument('--range',choices=['all','primary'],default='all');p.add_argument('--no-exclusion',action='store_true');p.add_argument('--zero-bias',action='store_true');a=p.parse_args()
if json.loads(Path(a.controls).read_text())['status']!='PASS':raise SystemExit('Projection controls must pass before fitting')
cache=np.load(a.cache);eg=cache['edge_grid'];table=cache['table'];t=time.monotonic()
result=dict(convention=a.convention,range=a.range,excluded=not a.no_exclusion,zero_bias=a.zero_bias,post_data=True,old_K2='FAIL unchanged',models={})
for lab,finite in [('B',False),('D',True)]:
    f=Fitter(eg,table,finite,a.convention,a.range=='primary',not a.no_exclusion,a.zero_bias)
    fit=f.fit();result['models'][lab]=fit
    print(json.dumps(dict(model=lab,chi2=fit['chi2'],p=fit['nominal_p'],logMb=fit['logMb'],biases=fit['biases'],convergence=fit['optimizer_agreement'])),flush=True)
b=result['models']['B'];d=result['models']['D'];result.update(dchi2=d['chi2']-b['chi2'],nominal_empirical_closure=(d['chi2']-b['chi2']<=4 and d['nominal_p']>=.01),all_optimizer_agreement=b['optimizer_agreement'] and d['optimizer_agreement'],elapsed_seconds=time.monotonic()-t)
Path(a.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='models'}))
