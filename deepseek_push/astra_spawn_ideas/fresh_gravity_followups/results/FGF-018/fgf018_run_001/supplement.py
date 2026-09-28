from pathlib import Path
from fractions import Fraction
import sys,json,math,argparse
import numpy as np
from astropy.io import fits
ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);O=ap.parse_args().out;O.mkdir(parents=True,exist_ok=True);R=Path.cwd();DATA=R/'real_research/data/xcop'
N=['A1795','A2029','A2142','A2319','A644','A85','ZW1215'];rows=[];critical=[]
for n in N:
 for kind,ex,key,lo,hi,error in [('fgas_profile',1,'MGAS','MGAS_LO','MGAS_HI',True),('hydro_mass',1,'M_FORW','EM_FORW','EM_FORW',True),('mstar',2,'MSTAR','MSTAR_LO','MSTAR_HI',False)]:
  with fits.open(DATA/n/(n+'_'+kind+'.fits')) as h:
   t=h[ex];unit=t.columns['RADIUS'].unit;scale=1 if unit=='kpc' else (1000 if unit=='Mpc' else float(t.header['R500']));r=np.asarray(t.data['RADIUS'],float)*scale;m=np.asarray(t.data[key],float);a=np.asarray(t.data[lo],float);b=np.asarray(t.data[hi],float);L,U=(m-a,m+b) if error else (a,b)
  start=max(0,int(np.searchsorted(r,100,side='right'))-1);stop=min(len(r)-1,int(np.searchsorted(r,1000,side='left')))
  pref=np.maximum.accumulate(L);future=np.minimum.accumulate(U[::-1])[::-1];glob=bool(np.all(pref<=future));lp=np.maximum.accumulate(L[start:stop+1]);uf=np.minimum.accumulate(U[start:stop+1][::-1])[::-1];local=bool(np.all(lp<=uf));bad=None
  if not glob:
   gap=L[:,None]-U[None,:];gap[np.tril_indices(len(r),-1)]=-np.inf;i,j=np.unravel_index(np.argmax(gap),gap.shape)
   assert i<=j and L[i]>U[j]
   bad=dict(indices_zero_based=[int(i),int(j)],radii_kpc=[float(r[i]),float(r[j])],earlier_lower_msun=float(L[i]),later_upper_msun=float(U[j]),gap_msun=float(L[i]-U[j]),both_outside_tested_range=bool(r[i]>1000 and r[j]>1000))
  rows.append(dict(name=n,profile=kind,global_monotone_feasible=glob,interpolation_support_knots=[start,stop],support_radii_kpc=[float(r[start]),float(r[stop])],tested_domain_monotone_feasible=local,largest_global_violation=bad))
  if kind=='fgas_profile':
   for i in range(len(r)-1):
    if r[i]>=1000 or r[i+1]<=100:continue
    q=r[i+1]/r[i];lam=(m[i+1]-q*m[i])/(a[i+1]+q*b[i]);x=m[i]+lam*b[i];y=m[i+1]-lam*a[i+1];res=y/(q*x)-1
    assert lam>1 and x>0 and y>0 and abs(res)<1e-14
    critical.append(dict(name=n,interval_index=i,r1_kpc=float(r[i]),r2_kpc=float(r[i+1]),error_multiplier_at_box_slope_one=float(lam),endpoint_masses_msun=[float(x),float(y)],crossing_residual=float(res)))
# Synthetic rational witness satisfies a full four-knot mass box and strict monotonicity.
r=list(map(Fraction,[1,2,4,8]));L=list(map(Fraction,[1,2,3,6]));U=list(map(Fraction,[2,4,8,10]));m=list(map(Fraction,[1,3,4,8]))
assert all(l<=v<=u for l,v,u in zip(L,m,U)) and all(m[i]<m[i+1] for i in range(3)) and m[2]/m[1]<r[2]/r[1]
synthetic=dict(radii=[str(v) for v in r],lower=[str(v) for v in L],upper=[str(v) for v in U],witness=[str(v) for v in m],target_mass_ratio=str(m[2]/m[1]),target_radius_ratio=str(r[2]/r[1]),conclusion='Positive globally increasing mass within all boxes; target 0<s<1; only local sign certificate removed, not a steady-flow solution.')
summary=dict(all_21_profiles_monotone_feasible_on_tested_interpolation_support=all(x['tested_domain_monotone_feasible'] for x in rows),global_infeasible=[x for x in rows if not x['global_monotone_feasible']],gas_error_multiplier_minima={n:min(x['error_multiplier_at_box_slope_one'] for x in critical if x['name']==n) for n in N},synthetic_exact_witness=synthetic,maximum_crossing_residual=max(abs(x['crossing_residual']) for x in critical))
assert summary['all_21_profiles_monotone_feasible_on_tested_interpolation_support']
for name,obj in [('monotone_support_audit.json',rows),('slope_error_margins.json',critical),('checks.json',summary)]: (O/name).write_text(json.dumps(obj,indent=2)+'\n')
print(json.dumps(summary,indent=2))
