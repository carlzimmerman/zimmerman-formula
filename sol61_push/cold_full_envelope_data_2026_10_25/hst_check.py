import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import argparse,datetime,hashlib,json,math,pathlib,resource,time
import numpy as np
from scipy.integrate import cumulative_trapezoid
from numpy.polynomial.legendre import leggauss
from physics import G,project,baryon_g,plummer_g,g_cold
from core_floor import cut_profile
from fit_v2 import profiles
from data import CATS,P,ROOT

def projected(R,a,g,beta,kind):
 r=np.geomspace(.001,1e7,8192);nu=(1+(r/a)**2)**(-2.5);pp=-cumulative_trapezoid((nu*g(r)*r**(2*beta))[::-1],r[::-1],initial=0)[::-1]*r**(-2*beta)
 x,w=leggauss(256);t=(x+1)*np.pi/4;w=w*np.pi/4;z=a*np.tan(t);jac=a/np.cos(t)**2;rr=np.sqrt(R[:,None]**2+z*z);n=(1+(rr/a)**2)**(-2.5);p=np.interp(np.log(rr),np.log(r),pp)
 factor={'LOS':1-beta*R[:,None]**2/rr**2,'PMR':1-beta+beta*R[:,None]**2/rr**2,'PMT':np.full_like(rr,1-beta)}[kind]
 return np.sum(w*jac*factor*p,axis=1)/np.sum(w*jac*n,axis=1)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);args=ap.parse_args();dest=pathlib.Path(args.out);dest.mkdir(exist_ok=True,parents=True);assert not (dest/'result.json').exists();files=[P/f for f in ['hst_check.py','HST_CONTRACT.md','physics.py','data.py','fit_v2.py','core_floor.py','fit_002/result.json','core_001/result.json','core_fraction_001/result.json','hst_data/DRACO_BINS.dat','hst_data/README.txt']];snap='sol61_push/cold_core_binding_2026_10_25/late_runs/late_dt005';files.extend([ROOT/(snap+'.json'),ROOT/(snap+'.npz'),ROOT/'sol61_push/cold_resolved_pulse_2026_10_25/runs/draco_joint_s05.npz',ROOT/'real_research/data/dsph/lvd_dwarf_mw.csv',ROOT/'sol61_push/cold_data_constraints_2026_10_24/results.json']);hashes=lambda:{str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files};before=hashes();start=time.time()
 expected={'DRACO_BINS.dat':'1e5fd634386465f9d3992cf7f9d4a134','README.txt':'35e33df9bafb2c91bd7ccc52bec2ed47'};md5={n:hashlib.md5((P/'hst_data'/n).read_bytes()).hexdigest() for n in expected};assert md5==expected
 raw=np.loadtxt(P/'hst_data/DRACO_BINS.dat');pm=raw[raw[:,6]>0];assert pm.shape==(5,12);cat=CATS['Draco'];D=float(cat['distance']);a=float(cat['rhalf_sph_physical']);angle=np.deg2rad(pm[:,7]-float(cat['position_angle']));q=1-float(cat['ellipticity']);R=D*1000*np.deg2rad(pm[:,6]/60);Rc=R*np.sqrt(q)*np.sqrt(np.cos(angle)**2+np.sin(angle)**2/q**2)
 fit=json.loads((P/'fit_002/result.json').read_text());cf=json.loads((P/'core_fraction_001/result.json').read_text());co=json.loads((P/'core_001/result.json').read_text());ms=fit['datasets']['Draco']['stellar_mass_Msun'];r,dm,_=cut_profile('Draco');late=next(x for x in profiles('Draco') if x['tag']=='Draco_fine_late');rows=[];controls=[]
 for beta in [-.5,0.]:
  fitrow=next(x for x in fit['rows'] if x['name']=='Draco' and x['footing']=='canonical' and x['beta']==beta);gridrow=next(x for x in cf['rows'] if x['name']=='Draco' and x['footing']=='canonical' and x['beta']==beta);best=min(gridrow['grid'],key=lambda x:x['nll']);full=next(x for x in co['rows'] if x['name']=='Draco' and x['footing']=='canonical' and x['beta']==beta)['core_plus_envelope'][1]
  models=[('free_Plummer',fitrow['free_Plummer'],None),('half_supply_Plummer',fitrow['fixed_supply_envelopes'][1],None),('best_grid_cut_plus_extended',best,best['coefficient']),('full_cut_plus_extended',full,1.)]
  for geometry,rr in [('circular_R',R),('LVD_circularized_R',Rc)]:
   for tag,model,c in models+[('resolved_full_Draco',None,None)]:
    def g(rad):
     cold=g_cold(rad,late['r'],late['dm']) if model is None else plummer_g(rad,model['cold_mass_Msun'],model['scale_pc'])+(0 if c is None else c*g_cold(rad,r,dm))
     return baryon_g(rad,ms,[a],'canonical')+cold
    pred=np.array([np.sqrt(projected(rr,a,g,beta,k))/(4.74047*D) for k in ['PMR','PMT']]).T;obs=pm[:,[8,10]];err=pm[:,[9,11]];res=(pred-obs)/err
    rows.append(dict(beta=beta,geometry=geometry,model=tag,R_pc=rr.tolist(),predicted_masyr=pred.tolist(),observed_masyr=obs.tolist(),errors_masyr=err.tolist(),standardized_residual=res.tolist(),sum_squared_residual=float(np.sum(res**2))))
    los=projected(rr,a,g,beta,'LOS');direct=project(rr,a,g,beta,nr=8192,nz=256);controls.append(float(np.max(abs(los/direct-1))))
    if beta==0:assert np.max(abs(pred[:,0]-pred[:,1]))<1e-12
 result=dict(scope='held-out five-bin PM diagnostic, no covariance or axisymmetric/rotation likelihood, no significance',rows=rows,LOS_projection_control_max=max(controls),download=dict(record='https://zenodo.org/records/11111113',files_md5=md5,md5_matches_published=True,utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),inputs_before=before,inputs_after=hashes(),seconds=time.time()-start,peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss);assert max(controls)<1e-12 and before==result['inputs_after'];(dest/'result.json').write_text(json.dumps(result,indent=2)+'\n')
 for z in rows:print(z['beta'],z['geometry'],z['model'],round(z['sum_squared_residual'],3))
if __name__=='__main__':main()
