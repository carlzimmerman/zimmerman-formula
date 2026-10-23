import json,sys
from pathlib import Path
import numpy as np
from scipy.interpolate import PchipInterpolator
p=Path(__file__).parent
rows=[]
target=.8228
for stem,order in [('actionh32_64',64),('action16_128',128)]:
 d=np.load(p/(stem+'.npz'));o=d['omega'].reshape(order,order);Q=d['Q'].reshape(order,order)
 critical=[];mixed=[];root_counts=np.zeros(32,dtype=int);bracket_counts=np.zeros(32,dtype=int)
 minimum_resonant_slope=np.full(32,np.inf)
 for j in range(order):
  # E=-Q-u/2; the constant energy offset does not change derivatives or roots.
  e=-Q[j];v=o[j];delta=np.diff(v);interp=PchipInterpolator(e,v)
  indices=np.where(delta[:-1]*delta[1:]<0)[0]+1
  if len(indices):mixed.append(j)
  for k in indices:
   # Quadratic estimate is only a sampled extremum diagnostic, not certification.
   xx=e[k-1:k+2]-e[k];aa,bb,cc=np.polyfit(xx,v[k-1:k+2],2)
   vertex=-bb/(2*aa);inside=bool(xx[0]<=vertex<=xx[-1])
   critical.append(dict(row=j,index=int(k),frequency=float(aa*vertex**2+bb*vertex+cc) if inside else float(v[k]),vertex_inside=inside))
  for n in range(1,33):
   roots=interp.solve(target/n,extrapolate=False)
   roots=roots[np.isfinite(roots)&(roots>e[0])&(roots<e[-1])]
   root_counts[n-1]+=len(roots)
   bracket_counts[n-1]+=np.count_nonzero((v[:-1]-target/n)*(v[1:]-target/n)<0)
   if len(roots):minimum_resonant_slope[n-1]=min(minimum_resonant_slope[n-1],np.min(abs(interp.derivative()(roots))))
 crit=np.array([x['frequency'] for x in critical]);details=[]
 for n in range(1,33):
  distances=abs(n*crit-target)
  details.append(dict(n=n,roots=int(root_counts[n-1]),brackets=int(bracket_counts[n-1]),nearest_sampled_critical_distance=float(min(distances)) if len(distances) else None,critical_frequency_range=[float(n*min(crit)),float(n*max(crit))] if len(crit) else None,minimum_interpolated_resonant_slope=float(minimum_resonant_slope[n-1]) if np.isfinite(minimum_resonant_slope[n-1]) else None))
 rows.append(dict(input=stem,order=order,orbits=order**2,mixed_rows=mixed,critical=critical,omega_range=[float(o.min()),float(o.max())],harmonics=details,root_bracket_agreement=bool(np.array_equal(root_counts,bracket_counts)),finite=bool(np.isfinite(o).all() and np.isfinite(Q).all()),energy_ordered=bool((np.diff(-Q,axis=1)>0).all())))
checks=dict(finite=all(r['finite'] for r in rows),energy_ordered=all(r['energy_ordered'] for r in rows),interpolation_brackets=all(r['root_bracket_agreement'] for r in rows),both_grids_nonmonotone=all(len(r['mixed_rows'])>0 for r in rows))
out=dict(assertion_tested='Stored Gauss energy rows contain frequency reversals at both action resolutions; interior PCHIP roots agree with sign brackets at omega=.8228.',checks=checks,all_pass=all(checks.values()),rows=rows,non_claims=['No endpoint completion','No global support or critical-point completeness','No analytic continuation or pole','Quadratic turning values are diagnostics only'])
Path(sys.argv[1]).write_text(json.dumps(out,indent=2));print(json.dumps({**out,'rows':[{**r,'critical_count':len(r['critical']),'critical':None} for r in rows]},indent=2));sys.exit(0 if out['all_pass'] else 1)
