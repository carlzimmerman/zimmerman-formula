"""Diagnostics of the two already-fitted discs; no likelihood or stability calculation."""
import sys,json,pathlib,hashlib
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.interpolate import RegularGridInterpolator
ROOT=pathlib.Path(__file__).resolve().parents[2]; SRC=ROOT/'rebuild_2026_10_22/S3_v3_mw_seals'
sys.path.insert(0,str(SRC));import s3_mw as M
fits=json.loads((ROOT/'reviews/dr4_flexible_halo_2026_10_26/run_v3/results.json').read_text())['fits']
R=8.122;zs=np.array([.1,.3,.5,1.1,2.,3.]);points=np.column_stack([np.full(len(zs),R),zs]);out={'R_kpc':R,'z_kpc':zs.tolist(),'scope':'diagnostics of existing fits; no observational likelihood or stable distribution function','rows':[]}
mw=M.MW(M.GRID_FINE,tag='fine');g=mw.g
sample=lambda arr:RegularGridInterpolator((g.Rc,g.zc),arr)(points)
for f in fits:
 if f['model']!='halo_plus_disc' or not f['stellar_nuisance']:continue
 foot=f['footing'];rho_s,rs,m,a,b=f['physical_parameters'];s=f['stellar_scale']
 def disc_density(z):
  h=np.sqrt(z*z+b*b)
  return b*b*m/(4*np.pi)*(a*R*R+(a+3*h)*(a+h)**2)/((R*R+(a+h)**2)**2.5*h**3)
 def halo_density(z):
  r=np.sqrt(R*R+z*z);x=r/rs;return rho_s/(x*(1+x)**2)
 def disc_forces(r,z):
  h=np.sqrt(z*z+b*b);d=(r*r+(a+h)**2)**1.5
  return np.array([M.G*m*r/d,M.G*m*(a+h)*z/(h*d)])
 def halo_forces(r,z):
  rad=np.sqrt(r*r+z*z);x=rad/rs;mass=4*np.pi*rho_s*rs**3*(np.log1p(x)-x/(1+x))
  return M.G*mass*np.array([r,z])/rad**3
 col=2*quad(disc_density,0,np.inf,epsrel=1e-10)[0]
 half=brentq(lambda z:2*quad(disc_density,0,z)[0]/col-.5,.001,5.)
 # Independent finite-difference Poisson check for the analytic MN density.
 eps=1e-4;errs=[]
 for z in zs:
  dfr=(disc_forces(R+eps,z)[0]-disc_forces(R-eps,z)[0])/(2*eps)
  dfz=(disc_forces(R,z+eps)[1]-disc_forces(R,z-eps)[1])/(2*eps)
  lap=dfr+disc_forces(R,z)[0]/R+dfz
  errs.append(abs(lap/(4*np.pi*M.G*disc_density(z))-1))
 assert max(errs)<1e-6
 pn,pb=mw.phiN(s);dr,dz=g.cell_derivs(pn,pb)
 modelFz=sample(dz)+np.array([disc_forces(R,z)[1]+halo_forces(R,z)[1] for z in zs])
 key=f'fine|{foot}|s1.000000|eN0.000000|';path=SRC/'_cache_final'/('mw_'+hashlib.sha1(key.encode()).hexdigest()[:16]+'.npz')
 with np.load(path,allow_pickle=False) as dat:
  vr,vz=g.cell_derivs(dat['Phi'],{k:dat['PB_'+k] for k in ('R','B','T')})
 bary0=float((s*M.rho_stars(R,0.)+M.rho_gas(R,0.))/1e9)
 darkcol=2*quad(lambda z:disc_density(z)+halo_density(z),0,1.1)[0]/1e6
 barycol=2*quad(lambda z:s*M.rho_stars(R,z)+M.rho_gas(R,z),0,1.1)[0]/1e6
 row=dict(footing=foot,disc_half_column_height_kpc=half,disc_midplane_density=disc_density(0)/1e9,halo_midplane_density=halo_density(0)/1e9,dark_midplane_density=(disc_density(0)+halo_density(0))/1e9,baryon_midplane_density=bary0,total_midplane_density=bary0+(disc_density(0)+halo_density(0))/1e9,disc_to_halo_midplane_ratio=disc_density(0)/halo_density(0),dark_column_1p1=darkcol,baryon_column_1p1=barycol,total_column_1p1=darkcol+barycol,model_Kz_over_2piG=(modelFz/(2*np.pi*M.G)/1e6).tolist(),v3_Kz_over_2piG=(sample(vz)/(2*np.pi*M.G)/1e6).tolist(),MN_poisson_check=max(errs))
 out['rows'].append(row);print(json.dumps(row),flush=True)
(ROOT/sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n')
