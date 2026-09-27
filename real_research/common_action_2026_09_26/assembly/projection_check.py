"""Exact finite-volume first variations of the foliation mean projection."""
import argparse,json
from pathlib import Path
import sympy as s

ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
n=3
weights=s.symbols('w0:3',positive=True)
lapses=s.symbols('N0:3',positive=True)
Z=s.symbols('Z0:3',real=True)
K=s.symbols('K0:3',nonnegative=True)
W=s.symbols('W0:3',nonnegative=True)
volume=sum(weights);mean=sum(w*z for w,z in zip(weights,Z))/volume
z=[v-mean for v in Z]
lag=[s.exp(z[i])*K[i]/lapses[i]**2-s.exp(-z[i])*W[i] for i in range(n)]
rho=[s.exp(z[i])*K[i]/lapses[i]**2+s.exp(-z[i])*W[i] for i in range(n)]
action=sum(weights[i]*lapses[i]*lag[i] for i in range(n))
source_mean=sum(weights[i]*lapses[i]*rho[i] for i in range(n))/volume
checks={}
def exact(name,expr):
    value=s.simplify(expr)
    assert value==0,(name,value)
    checks[name]={'passed':True,'residual':str(value)}
exact('weighted_zero_mean',sum(weights[i]*z[i] for i in range(n)))
for i in range(n):
    exact(f'projected_Z_source_{i}',s.diff(action,Z[i])-weights[i]*(lapses[i]*rho[i]-source_mean))
    exact(f'unchanged_lapse_density_{i}',-s.diff(action,lapses[i])-weights[i]*rho[i])
    exact(f'volume_stress_correction_{i}',s.diff(action,weights[i])-lapses[i]*lag[i]+source_mean*z[i])
    exact(f'mean_volume_derivative_{i}',s.diff(mean,weights[i])-z[i]/volume)
exact('integrated_Z_source_identity',sum(s.diff(action,v) for v in Z))
offset=s.symbols('offset',real=True)
for i in range(n):
    exact(f'global_shift_invariance_{i}',z[i].subs({q:q+offset for q in Z},simultaneous=True)-z[i])
out={'passed':True,'checks':checks,
     'scope':'Three-cell exact variation; continuum formulas follow by the same weighted-integral differentiation',
     'physical_identity':'z=Z-<Z>_h; source rho-<N rho>_h/N; lapse density unchanged; extra isotropic pressure -<N rho>_h z/N',
     'non_claims':['No full metric-clock variation from a three-cell model','No coupled PDE theorem','No observational pass']}
Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'exact_checks':len(checks),'passed':True}))
