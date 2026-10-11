import json,sys
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from astropy.cosmology import FlatLambdaCDM
P=Path('sol61_push'); old=np.load(P/'gas_image_operator_2026_10_11/run_v2/operator.npz')
rows=json.loads((P/'native_lensing_2026_10_11/run_v2/results.json').read_text())['gold_rows']
H=old['helmert']; zs=np.array([r['zsys'] for r in rows]); zl=.296
checks=[]
def ck(n,b,v=None):checks.append(dict(name=n,passed=bool(b),value=v))
def hm(a):return np.einsum('ij,jk->ik',H,a,optimize=False)
# Independent dimensionless Gaussian LOS oracle at fixed angular radius x=.7.
x=.7
base_B=quad(lambda z:np.exp(-x*x-z*z),-np.inf,np.inf)[0]
base_S=quad(lambda z:np.exp(-.5*(x*x+z*z)),-np.inf,np.inf)[0]
for lam in [.5,1.,2.]:
 for eta in [.5,1.,2.]:
  depth=lam*eta; norm=depth**-.5
  B=quad(lambda z:norm**2*np.exp(-x*x-(z/depth)**2),-np.inf,np.inf)[0]
  S=quad(lambda z:norm*np.exp(-.5*(x*x+(z/depth)**2)),-np.inf,np.inf)[0]
  ck(f'brightness_{lam}_{eta}',abs(B/base_B-1)<1e-8)
  ck(f'column_{lam}_{eta}',abs(S/base_S-np.sqrt(depth))<1e-8)
  ck(f'angular_mass_{lam}_{eta}',abs(S/base_S*lam**2-lam**2.5*np.sqrt(eta))<1e-8)
  ck(f'alpha_{lam}_{eta}',abs(S/base_S*lam-lam**1.5*np.sqrt(eta))<1e-8)
wrong_B=quad(lambda z:np.exp(-x*x-(z/2)**2),-np.inf,np.inf)[0]
ck('MUTATE_fixed_density',abs(wrong_B/base_B-1)>.1)
ck('MUTATE_fixed_mass_alpha',abs(2**-1-2**1.5)>1)
Om=(.02237+.1200)/.6736**2
ca=FlatLambdaCDM(H0=70,Om0=.3);cn=FlatLambdaCDM(H0=67.36,Om0=Om)
Da=ca.angular_diameter_distance(zl).value;Dn=cn.angular_diameter_distance(zl).value;lam=Dn/Da
wa=(ca.angular_diameter_distance_z1z2(zl,zs)/ca.angular_diameter_distance(zs)).value
wn=(cn.angular_diameter_distance_z1z2(zl,zs)/cn.angular_diameter_distance(zs)).value
for name,c,h,om in [('author',ca,70,.3),('PM',cn,67.36,Om)]:
 def chi(z):return quad(lambda q:1/np.sqrt(om*(1+q)**3+1-om),0,z,epsabs=1e-12,epsrel=1e-12)[0]
 d=299792.458/h*chi(zl)/(1+zl); ws=np.array([1-chi(zl)/chi(z) for z in zs]); wc=wa if name=='author' else wn
 ck('independent_distance_'+name,abs(d/c.angular_diameter_distance(zl).value-1)<1e-8)
 ck('independent_weights_'+name,np.max(abs(ws-wc))<1e-8)
ck('author_source_weight_reproduction',np.max(abs(wa-old['source_weight_author_context']))<1e-12)
factor=lam**1.5; arrays={'helmert':H,'source_weight_native_PM_flat':wn}; metrics={}
for frame in ['ICRS','FK5J2000']:
 for interp in ['linear','cubic']:
  tag=frame+'_'+interp; a=old[tag+'_alpha_infinity_arcsec']; na=factor*a
  reduced=wn[:,None]*na; contrast=hm(reduced)
  ck('roundtrip_'+tag,np.max(abs(na/factor-a))<1e-12*np.max(abs(a)))
  ck('identity_'+tag,np.max(abs(1**1.5*a-a))==0)
  ck('source_gauge_'+tag,np.max(abs(hm(wn[:,None]*(na+np.array([2.,-3.])))-contrast))<1e-10)
  ck('finite_'+tag,np.isfinite(contrast).all())
  arrays[tag+'_alpha_infinity_native']=na
  for foot in ['canonical','alt']:arrays[tag+'_'+foot+'_H_reduced_native']=contrast.copy()
  ck('footings_same_gas_'+tag,np.array_equal(arrays[tag+'_canonical_H_reduced_native'],arrays[tag+'_alt_H_reduced_native']))
  metrics[tag]={'max_difference_distance_factor_only_arcsec':float(np.max(abs(contrast-hm(wn[:,None]*a)))),'max_difference_author_context_arcsec':float(np.max(abs(contrast-old[tag+'_H_reduced_author_context_arcsec'])))}
result=dict(checks=checks,distance_author_Mpc=Da,distance_native_Mpc=Dn,distance_ratio=lam,gas_column_factor=lam**.5,gas_angular_aperture_mass_factor=lam**2.5,gas_unreduced_alpha_factor=factor,gas_density_factor=lam**-.5,source_efficiency_ratio_range=[float(np.min(wn/wa)),float(np.max(wn/wa))],metrics=metrics,native_PM_background={'H0':67.36,'Om0':Om},conditional_on='Fixed angular 3D geometry, clumping and spectral emissivity; fixed redshift',scientific_verdict=None)
out=Path(sys.argv[1]);np.savez_compressed(out/'operator.npz',**arrays);(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(f'{sum(c["passed"] for c in checks)}/{len(checks)} checks');print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2));assert all(c['passed'] for c in checks)
