from pathlib import Path
import argparse,hashlib,json,math
import mpmath as mm
from mpmath import iv,mp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
files=[Path(__file__),HERE/'ROOT_SIGN_CRITERIA.md',HERE/'interval_001/results.json',HERE/'interval_001/manifest.json',HERE.parent/'CSM1_consistent_core_switch/heldout/MW_BURKERT_MONOTONICITY.md'];sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();hashes={str(f.relative_to(ROOT)):sha(f) for f in files};d=json.loads(files[2].read_text());iv.dps=50;mp.dps=80

def B(x,ctx):return ctx.log(1+x*x)+2*ctx.log(1+x)-2*ctx.atan2(x,ctx.mpf(1))
def evaluate(b,scale=1.):
 M,R,S=[iv.mpf(b[k]) for k in ('M','R','Sigma')];lo=iv.mpf(b['r0_lower'])*iv.mpf(scale);hi=iv.mpf(b['r0_upper'])*iv.mpf(scale);xl=R/hi;xh=R/lo;target=M/(iv.pi*S*R*R);fl=B(xl,iv)/(xl*xl)-target;fh=B(xh,iv)/(xh*xh)-target;h=4*xl**3/((1+xl)*(1+xl*xl)*B(xl,iv));finite=all(math.isfinite(float(x)) for q in (fl,fh,h) for x in (q.a,q.b));ok=bool(finite and fl.a>0 and fh.b<0 and h.b<2)
 return ok,dict(lower_x_residual=str(fl),upper_x_residual=str(fh),compact_h=str(h),finite=finite)
rows=[]
for i,b in enumerate(d['root_brackets']):
 ok,rec=evaluate(b);M,R,S=[mp.mpf(b[k]) for k in ('M','R','Sigma')];xl=R/mp.mpf(b['r0_upper']);xh=R/mp.mpf(b['r0_lower']);target=M/(mp.pi*S*R*R);v=[B(x,mp)/(x*x)-target for x in (xl,xh)];rec.update(index=i,certified_signs=ok,high_precision_point_signs=[bool(v[0]>0),bool(v[1]<0)]);rows.append(rec)
q=iv.mpf(1)/iv.mpf(3)*iv.mpf(3);mutation=evaluate(d['root_brackets'][0],1.01)[0]
checks=dict(coverage=len(rows)==124,finite=all(x['finite'] for x in rows),all_directed_signs=all(x['certified_signs'] for x in rows),point_diagnostic=all(all(x['high_precision_point_signs']) for x in rows),rational_containment=bool(q.a<=1 and q.b>=1),mutation_detected=not mutation,inputs_stable=all(sha(ROOT/f)==h for f,h in hashes.items()))
result=dict(checks=checks,rows=rows,input_sha256=hashes,backend=dict(mpmath=mm.__version__,interval_decimal_digits=50,point_decimal_digits=80),certified_scalar_root_brackets=sum(x['certified_signs'] for x in rows),full_model_interval_certified=False,scope='Directed scalar root signs for fixed saved binary64 geometry/column coefficients only; not a model exclusion',remaining_obligations=['Physical coefficient/branch enclosures','Outward mass-vector endpoint and continuum enclosures','Projection and nuisance/covariance coefficient bounds','Signed-dot and final-score bounds'])
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(checks=checks,certified_roots=result['certified_scalar_root_brackets']),indent=2));raise SystemExit(0 if all(checks.values()) else 1)
