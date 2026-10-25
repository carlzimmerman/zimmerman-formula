"""Held-out Draco PM check; complete onset density, no refit."""
import argparse,json,hashlib,csv,time,resource,sys
from pathlib import Path
import numpy as np
from scipy.integrate import cumulative_trapezoid
from numpy.polynomial.legendre import leggauss
P=Path(__file__).resolve().parent;OLD=P.parent/'cold_full_envelope_data_2026_10_25';sys.path.insert(0,str(OLD))
from physics import G,baryon_g,g_cold,project

def projected(R,a,g,beta,kind):
 r=np.geomspace(.001,1e7,8192);nu=(1+(r/a)**2)**(-2.5);pp=-cumulative_trapezoid((nu*g(r)*r**(2*beta))[::-1],r[::-1],initial=0)[::-1]*r**(-2*beta);x,w=leggauss(256);t=(x+1)*np.pi/4;w=w*np.pi/4;z=a*np.tan(t);jac=a/np.cos(t)**2;rr=np.sqrt(R[:,None]**2+z*z);n=(1+(rr/a)**2)**(-2.5);v=np.interp(np.log(rr),np.log(r),pp);factor={'LOS':1-beta*R[:,None]**2/rr**2,'PMR':1-beta+beta*R[:,None]**2/rr**2,'PMT':np.full_like(rr,1-beta)}[kind];return np.sum(w*jac*factor*v,axis=1)/np.sum(w*jac*n,axis=1)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);args=ap.parse_args();out=Path(args.out);out.mkdir(parents=True,exist_ok=True);assert not(out/'result.json').exists();start=time.time();raw=np.loadtxt(OLD/'hst_data/DRACO_BINS.dat');pm=raw[raw[:,6]>0];assert pm.shape==(5,12);expected={'DRACO_BINS.dat':'1e5fd634386465f9d3992cf7f9d4a134','README.txt':'35e33df9bafb2c91bd7ccc52bec2ed47'};assert all(hashlib.md5((OLD/'hst_data'/k).read_bytes()).hexdigest()==v for k,v in expected.items());cat=next(x for x in csv.DictReader(open(P.parents[1]/'real_research/data/dsph/lvd_dwarf_mw.csv')) if x['name']=='Draco');D=float(cat['distance']);a=float(cat['rhalf_sph_physical']);q=1-float(cat['ellipticity']);angle=np.deg2rad(pm[:,7]-float(cat['position_angle']));R=D*1000*np.deg2rad(pm[:,6]/60);Rc=R*np.sqrt(q)*np.sqrt(np.cos(angle)**2+np.sin(angle)**2/q**2);data=json.loads((OLD/'fit_002/result.json').read_text())['datasets']['Draco'];rows=[];errors=[]
 for res in ['base','fine']:
  folder=P/('Draco_'+res+'_v4');meta=json.loads((folder/'result.json').read_text());z=np.load(folder/'field.npz');r=z['r']*meta['units']['R_pc']
  for i,t in enumerate(z['t']):
   if i and t==z['t'][i-1]:continue
   dm=abs(z['u'][i])**2*meta['units']['M_Msun']
   for beta in [-.5,0.]:
    for geom,rr in [('circular_R',R),('LVD_circularized_R',Rc)]:
     g=lambda s:baryon_g(s,data['stellar_mass_Msun'],[a],'canonical')+g_cold(s,r,dm);pred=np.array([np.sqrt(projected(rr,a,g,beta,k))/(4.74047*D) for k in ['PMR','PMT']]).T;obs=pm[:,[8,10]];err=pm[:,[9,11]];rows.append(dict(run=folder.name,t=float(t),beta=beta,geometry=geom,R_pc=rr.tolist(),predicted_masyr=pred.tolist(),observed_masyr=obs.tolist(),errors_masyr=err.tolist(),diagonal_squared_residual=float(np.sum(((pred-obs)/err)**2))));control=project(rr,a,g,beta,nr=8192,nz=256);errors.append(float(np.max(abs(projected(rr,a,g,beta,'LOS')/control-1))))
     if beta==0:assert np.max(abs(pred[:,0]-pred[:,1]))<1e-12
  z.close()
 result=dict(scope='held-out5bins10PMcomponents; spherical fixed observed tracer moment diagnostic; no covariance/axisymmetry/rotation likelihood, no significance or observed-state acceptance',rows=rows,LOS_projection_control_max=max(errors),author_md5_verified=expected,seconds=time.time()-start,peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss);assert max(errors)<1e-12;(out/'result.json').write_text(json.dumps(result,indent=2));print(json.dumps(dict(rows=len(rows),control=max(errors),seconds=result['seconds'])))
if __name__=='__main__':main()
