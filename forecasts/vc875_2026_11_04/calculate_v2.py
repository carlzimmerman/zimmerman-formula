"""VC875 finite forecast using public cube morphology and literature mass branches."""
import csv,json,math,sys,subprocess
from pathlib import Path
import numpy as np
from scipy.special import ive,kve
from scipy.optimize import least_squares
from scipy.ndimage import gaussian_filter
here=Path(__file__).resolve().parent;out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=True)
subprocess.run([sys.executable,str(here/'measure.py'),str(out/'measurement')],check=True)
m=json.loads((out/'measurement/measurement.json').read_text())
G=4.30091e-6;U=1e6/3.0857e19;A0=9.3603e-11;z=m['z'];a=1/(1+z)
r=math.sqrt(a**(-3*(1-.838-.62))*math.exp(1.86*(1-a)))
def disc(M,re,R):
 rd=re/1.678;y=np.asarray(R)/(2*rd)
 return 2*G*M/rd*y*y*(ive(0,y)*kve(0,y)-ive(1,y)*kve(1,y))
def speed(vb,R,a0):
 gn=vb/R;return np.sqrt(.5*(gn+np.sqrt(gn*gn+4*gn*a0/U))*R)
def halo(lm,R):
 # Dutton-Maccio mean c200 relation; total-equivalent mass, .843 dark amplitude.
 c=10**(.520+(.905-.520)*np.exp(-.617*z**1.21)+(-.101+.026*z)*(lm+np.log10(.671)-12))
 hz=68.56427*np.sqrt(.2976016*(1+z)**3+1-.2976016)/1000
 rv=(G*10**lm/(100*hz*hz))**(1/3);f=lambda x:np.log1p(x)-x/(1+x)
 return .843*G*10**lm*f(R*c/rv)/f(c)/R
Ms=10**9.94;Mg=31*m['L_CII_aperture'];rs=1.4;rg=m['fit_Re_kpc']
R=np.array([1.28,2.,3.,3.84,5.,6.,8.]);vs=disc(Ms,rs,R);vg=disc(Mg,rg,R);vb=vs+vg
vf=speed(vb,R,A0*r);vm=speed(vb,R,A0)
rows=[]
for j,rr in enumerate(R):
 rows.append(dict(R_kpc=rr,V_Newton=float(np.sqrt(vb[j])),V_FDESI=vf[j],V_MOND=vm[j],V_MOND_a012=speed(vb,R,1.2e-10)[j],delta_kms=vm[j]-vf[j],NFW_logM12=np.sqrt(vb[j]+halo(12,R)[j])))
grid=[]
for logms in [9.68,9.94,9.97,10.2]:
 for res in [.93,1.4,2.0]:
  for reg in [3.0,rg,4.6]:
   for alpha in [15.5,31.,62.]:
    vbar=disc(10**logms,res,R)+disc(alpha*m['L_CII_aperture'],reg,R)
    v1=speed(vbar,R,A0*r);v2=speed(vbar,R,A0)
    for j,rr in enumerate(R):grid.append(dict(logMs=logms,Re_star=res,Re_gas=reg,alpha_CII=alpha,R=rr,V_FDESI=v1[j],V_MOND=v2[j]))
Rf=np.linspace(1,8,15);sf=disc(Ms,rs,Rf);gf=disc(Mg,rg,Rf);target=speed(sf+gf,Rf,A0*r)
def fit(halomode):
 def predict(p,R=Rf,s=sf,g=gf):
  vbar=s*10**p[0]+g*10**p[1]
  if not halomode:return speed(vbar,R,A0)
  lm=math.log10((Ms*10**p[0]+Mg*10**p[1])/.157)+p[2]
  return np.sqrt(vbar+halo(lm,R))
 lo=[-.2,-.3]+([0] if halomode else []);hi=[.2,.3]+([2] if halomode else [])
 fs=[least_squares(lambda p:(predict(p)-target)/target,[s,g]+([.1] if halomode else []),bounds=(lo,hi),max_nfev=2000,gtol=1e-10,xtol=1e-10,ftol=1e-10) for s,g in [(0,0),(-.1,-.1),(.1,-.2)]]
 f=min(fs,key=lambda f:sum(f.fun**2));vv=predict(f.x,R,vs,vg)
 return dict(parameters=f.x.tolist(),success=bool(f.success),max_residual_kms=float(max(abs(predict(f.x)-target))),rms_residual_kms=float(np.sqrt(np.mean((predict(f.x)-target)**2))),predicted_at_rows=vv.tolist(),halo_logM200=(math.log10((Ms*10**f.x[0]+Mg*10**f.x[1])/.157)+f.x[2]) if halomode else None)
fm=fit(False);fh=fit(True)
for j,row in enumerate(rows):row['MOND_mass_adjusted']=fm['predicted_at_rows'][j];row['NFW_mass_adjusted']=fh['predicted_at_rows'][j]
for name,rr in [('predictions.csv',rows),('mass_size_grid.csv',grid)]:
 with open(out/name,'w') as f:w=csv.DictWriter(f,fieldnames=rr[0]);w.writeheader();w.writerows(rr)
# Ideal model-cube separability. All geometry, flux and dispersion fixed; no imaging filtering.
# Correlated pixels represented by one independent sample per Gaussian beam area.
# This is an approximate Asimov S/N, not an injection-calibrated significance.
pix=.025;xy=np.arange(-2,2+pix/2,pix);xx,yy=np.meshgrid(xy,xy);inc=np.deg2rad(50);pa=np.deg2rad(147)
major=xx*np.sin(pa)+yy*np.cos(pa);minor=xx*np.cos(pa)-yy*np.sin(pa)
rad=np.sqrt(major**2+(minor/np.cos(inc))**2);rp=np.maximum(rad*m['kpc_per_arcsec'],.01)
cosphi=np.divide(major,rad,out=np.zeros_like(rad),where=rad>0)
rd=rg/1.678/m['kpc_per_arcsec'];brightness=m['flux_apertures_Jykms']['1.5']/(2*np.pi*rd**2*np.cos(inc))*np.exp(-rad/rd)
sv=disc(Ms,rs,rp);gv=disc(Mg,rg,rp);freqvel=np.arange(-500,501,10)
def model(kind,beam,sigma):
 if kind=='F':vc=speed(sv+gv,rp,A0*r)
 elif kind=='MOND':vc=speed(sv+gv,rp,A0)
 else:vc=speed(sv*10**fm['parameters'][0]+gv*10**fm['parameters'][1],rp,A0)
 los=vc*np.sin(inc)*cosphi
 cube=brightness[None,:,:]*np.exp(-.5*((freqvel[:,None,None]-los)/sigma)**2)/(np.sqrt(2*np.pi)*sigma)
 cube=gaussian_filter(cube,(0,beam/2.35482/pix,beam/2.35482/pix))*1.1331*beam**2
 return cube
sens=[]
for sig in [30.,60.]:
 for beam,noise,label in [(.0445692,.5893627,'new_native_best_SPW'),(.0445692,.7367477,'new_native_other_SPW'),(math.sqrt(np.prod(m['beam_arcsec'])),m['noise_mJybeam_10kms'],'existing_compact_measured'),(.15,.3,'hypothetical_taper_NOT_verified')]:
  fc=model('F',beam,sig);den=(noise/1000)**2*1.1331*beam**2/pix**2
  sigsame=math.sqrt(np.sum((fc-model('MOND',beam,sig))**2)/den)
  sigfit=math.sqrt(np.sum((fc-model('fit',beam,sig))**2)/den)
  sens.append(dict(label=label,beam=beam,noise_mJy10=noise,dispersion_kms=sig,ideal_fixed_mass_model_distance=sigsame,ideal_adjusted_mass_model_distance=sigfit))
checks=dict(grid_count=len(grid)==4*3*3*3*7,fit_convergence=fm['success'] and fh['success'],positive_separation=bool(np.all(vm>vf)),ceiling=bool(np.all(1-vf/vm<=1-r**.25+1e-12)),point_mass_limit=bool(abs(disc(1e10,2,200)/(G*1e10/200)-1)<.002))
summary=dict(a0_ratio=r,nominal=dict(logMstar=9.94,Mgas=Mg,Re_star_proxy_kpc=rs,Re_gas_fit_kpc=rg,alpha_CII=31),MOND_mimic=fm,NFW_mimic=fh,sensitivity=sens,checks=checks)
(out/'results.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2));assert all(checks.values())
