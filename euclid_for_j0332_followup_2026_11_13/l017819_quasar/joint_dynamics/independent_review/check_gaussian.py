"""Independent flattenedGaussian tracer in harmonicpotential benchmark.
Exact analytic Jeansmoments and independent Hermite projected apertureintegral.
"""
import sys,json,argparse
from pathlib import Path
sys.dont_write_bytecode=True
import numpy as np
from scipy.stats import ncx2
B=Path(__file__).resolve().parent;sys.path.insert(0,str(B.parent))
from axisymmetric_jeans_v2 import JeansMoments

def main(output):
 out=Path(output);out.mkdir(parents=True,exist_ok=True);sR=1.;sz=.6;wr=2.;wz=3.;V=wz*wz*sz*sz
 density=lambda R,z:np.exp(-.5*((R/sR)**2+(z/sz)**2))/((2*np.pi)**1.5*sR*sR*sz)
 force=lambda R,z:(wr*wr*R,wz*wz*z)
 model=JeansMoments(density,force,1.,nodes=440,extent=300.)
 rr=np.geomspace(.03,2,25);zz=np.geomspace(.01,1.5,25);R,z=np.meshgrid(rr,zz,indexing='ij');m=model.evaluate(R,z);bs=np.array([.8,1,1.2]);point=[]
 for b in bs:
  exact=b*V+(wr*wr-b*V/sR**2)*R*R;est=b*m[...,1]+m[...,2];point.append({'b':float(b),'vertical_max_relative_error':float(np.max(abs(m[...,0]/V-1))),'azimuthal_max_relative_error':float(np.max(abs(est/exact-1)))})
 # Orthogonal 2DGaussian expectations: no sharedLOS or polar quadrature.
 gx,gw=np.polynomial.hermite.hermgauss(100);records=[]
 for inc,offset in [(0.,(.2,-.1)),(45.,(.2,-.1)),(90.,(.2,-.1)),(90.,(-.2,.1))]:
  si=np.sin(np.deg2rad(inc));co=np.cos(np.deg2rad(inc));sv=np.sqrt(sR*sR*co*co+sz*sz*si*si);u=np.sqrt(2)*sR*gx[:,None];v=np.sqrt(2)*sv*gx[None,:];dist2=(u-offset[0])**2+(v-offset[1])**2;weight=gw[:,None]*gw[None,:]/np.pi*ncx2.cdf((1/.25)**2,2,dist2/.25**2);den=weight.sum();um=(weight*u).sum()/den;u2=(weight*u*u).sum()/den
  a=model.aperture(1.,.25,offset=offset,inclination=inc,bs=bs,nrad=200,nphi=64,nlos=160);exactsecond=[];exactfirst=[]
  for b in bs:
   C=wr*wr-b*V/sR**2;exactsecond.append(V*(si*si*b+co*co)+C*si*si*u2);exactfirst.append(np.sqrt(C)*si*um)
  err=np.array(a['raw_second_moment_kms2'])/exactsecond-1;firsterr=np.array(a['satoh_k1_mean_kms'])-exactfirst
  rec={'inclination':inc,'offset':list(offset),'code':a,'exact_light_fraction':float(den),'exact_second_moment':list(map(float,exactsecond)),'exact_mean':list(map(float,exactfirst)),'relative_light_error':float(a['light_fraction']/den-1),'relative_second_error':err.tolist(),'absolute_first_error':firsterr.tolist()};records.append(rec)
 assert max(x['vertical_max_relative_error'] for x in point)<.01
 assert max(x['azimuthal_max_relative_error'] for x in point)<.015
 assert max(abs(x['relative_light_error']) for x in records)<.003
 assert max(abs(v) for x in records for v in x['relative_second_error'])<.01
 assert max(abs(v) for x in records for v in x['absolute_first_error'])<.003
 # Reader/schema audit only, not independentfieldsolvervalidation.
 fields=[]
 for tag in ['run_03','run_04']:
  f=B.parents[1]/'aqual_host/run_01'/tag/'best_field_refined.npz';d=np.load(f);light=d['light'];shape=(len(d['xc']),len(d['tc']));assert d['gr'].shape==shape and d['gt'].shape==shape;assert np.all(np.diff(d['xc'])>0) and np.all(np.diff(d['tc'])>0)
  fields.append({'path':str(f),'logmass':float(d['logmass']),'light':light.tolist(),'zl':float(d['zl']),'zs':float(d['zs']),'a0':float(d['a0']),'shape':list(shape),'gr_gt_finite':bool(np.all(np.isfinite(d['gr'])) and np.all(np.isfinite(d['gt']))),'stored_q_is_projected_and_edgeon_intrinsic':float(light[4])})
 result={'assertion_tested':'FlattenedGaussian/harmonic exactJeans plus independentHermite aperturecontrol','fixture':{'sR':sR,'sz':sz,'omegaR':wr,'omegaz':wz,'V':V},'point_checks':point,'aperture_checks':records,'field_schema_checks':fields,'non_claims':['Not actualhighnAQUALnumericalconvergence or physicalDFvalidation','SeeingGaussian andfibergeometryassumed','No observationaltheoryverdict']};(out/'result.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);main(p.parse_args().output)
