"""Conditional spherical equilibrium virial screen; NOT evolved stellar heating."""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import json,pathlib,numpy as np
from scipy.integrate import simpson
P=pathlib.Path(__file__).resolve().parent;ROOT=P.parents[1];G=.00430091;a0=9.3603e-11*3.085677581491367e10
models={m['name'].lower().replace(' ',''):m for m in json.loads((ROOT/'sol61_push/cold_survey_capture_2026_10_24/capture_results.json').read_text())['models']};rows=[];xx=np.geomspace(1e-5,1e4,20001);refs=dict(draco=11.615430e6,sextans=8.623096e6,fornax=17.476462e6,leoi=6.737626e6)
for jf in sorted((P/'runs').glob('*_v[23]_*.json')):
 m=json.loads(jf.read_text());name=m['parameters']['galaxy'];obs=models[name];units=m['physical'];R=units['Runit_pc'];V2=units['Vunit_kms']**2;d=np.load(jf.with_suffix('.npz'));cdf=d['physical_CDF'];rr=d['physical_CDF_r'];t=d['times'];massunit=units['Munit_Msun'];stellar=obs['stellar_mass'];gn=G*stellar/R**2*xx/(1+xx*xx)**1.5;gb=.5*(gn+np.sqrt(gn*gn+4*a0*gn));vb=R*simpson(xx**3/(1+xx*xx)**2.5*gb,x=xx);states=[]
 for k in [0,len(t)-1]:
  cc=np.interp(xx,rr,cdf[k],left=0,right=m['history'][k]['M']);sigcold=V2*simpson(xx/(1+xx*xx)**2.5*cc,x=xx);aperture=float(np.interp(1,rr,cdf[k])*massunit);states.append(dict(t=float(t[k]),aperture_Msun=aperture,aperture_over_conditional_reference=aperture/refs[name],sigma_equilibrium_global_kms=float(np.sqrt(vb+sigcold)),sigma_baryons_only_kms=float(np.sqrt(vb))))
 rows.append(dict(tag=m['parameters']['tag'],galaxy=name,states=states,status=m['status'],scope='spherical Plummer tracer global virial screen in instantaneous field; baryon-only Xi once plus Newtonian cold once; not actual heating or likelihood, Sextans two-tracer survey not re-fitted'))
(P/'kinematic_screen.json').write_text(json.dumps(rows,indent=2)+'\n')
for row in rows:print(row['tag'],row['states'])
