"""Conditional AzTEC/C159 forecast, published exponential discs; no new pixels."""
import json, csv, sys, math
from pathlib import Path
import numpy as np
from scipy.special import ive,kve
from scipy.optimize import least_squares
from scipy.ndimage import gaussian_filter
out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=True)
G=4.30091e-6; U=1e6/3.0857e19; A0=9.3603e-11; z=4.5668
a=1/(1+z); ratio=math.sqrt(a**(-3*(1-.838-.62))*math.exp(1.86*(1-a)))
Ms=4.5e10;Mg=1.5e11;rs=.460*1.4/1.678;rg=1.3
def disc(M,rd,R):
 y=np.asarray(R)/(2*rd)
 return 2*G*M/rd*y*y*(ive(0,y)*kve(0,y)-ive(1,y)*kve(1,y))
def speed(b,R,a0):
 n=b/R
 return np.sqrt(.5*(n+np.sqrt(n*n+4*n*a0/U))*R)
def halo(M,c,R):
 # M is the mass normalizing the dark NFW profile, not total baryons+dark mass.
 h=68.56427*np.sqrt(.2976016*(1+z)**3+1-.2976016)/1000
 rv=(G*M/(100*h*h))**(1/3)
 f=lambda x:np.log1p(x)-x/(1+x)
 return G*M*f(R*c/rv)/f(c)/R
R=np.array([1.,2.,3.,5.,7.5,10.]);b=disc(Ms,rs,R)+disc(Mg,rg,R)
F=speed(b,R,A0*ratio);M=speed(b,R,A0)
# Equal-weight fractional curve fit: nuisance degeneracy diagnostic, not fit to data.
rf=np.linspace(1,7.5,27);sf=disc(Ms,rs,rf);gf=disc(Mg,rg,rf);target=speed(sf+gf,rf,A0*ratio)
def fit(kind):
 def pred(p,R):
  s=Ms*10**p[0];g=Mg*10**p[1];bb=disc(s,rs,R)+disc(g,rg,R)
  if kind=='MOND':return speed(bb,R,A0)
  mh=(s+g)*.843/.157*10**p[2]
  return np.sqrt(bb+halo(mh,p[3],R))
 lo=[-.2,-.3]+([0,2] if kind=='NFW' else [])
 hi=[.2,.3]+([2,5] if kind=='NFW' else [])
 fits=[least_squares(lambda p:(pred(p,rf)-target)/target,[s,g]+([.05,3.4] if kind=='NFW' else []),bounds=(lo,hi),max_nfev=3000,gtol=1e-11,ftol=1e-11,xtol=1e-11) for s,g in [(0,0),(.1,-.2),(-.1,-.1)]]
 f=min(fits,key=lambda f:sum(f.fun*f.fun));res=pred(f.x,rf)-target
 return dict(p=f.x.tolist(),mass_factors=(10**f.x[:2]).tolist(),max_residual=float(max(abs(res))),rms=float(np.sqrt(np.mean(res*res))),success=bool(f.success),values=pred(f.x,R).tolist()),pred
fm,pm=fit('MOND');fh,ph=fit('NFW')
rows=[]
for j,r in enumerate(R):
 gap=M[j]-F[j];eps=gap/3
 # One-source-at-a-time uncertainty budgets, not jointly sufficient conditions.
 epsmass=.001
 dvg=(speed(disc(Ms,rs,r)+disc(Mg*(1+epsmass),rg,r),r,A0*ratio)-speed(disc(Ms,rs,r)+disc(Mg*(1-epsmass),rg,r),r,A0*ratio))/(2*epsmass)
 rows.append(dict(R_kpc=r,Newton=float(np.sqrt(b[j])),FDESI=F[j],MOND=M[j],MOND_standard_a012=speed(b,R,1.2e-10)[j],NFW_published=np.sqrt(b[j]+halo(2e12,3.4,r)),MOND_mimic=fm['values'][j],NFW_mimic=fh['values'][j],gap=gap,three_sigma_velocity_budget=eps,inclination_budget_deg=eps/F[j]*np.tan(np.deg2rad(40))*180/np.pi,gas_fractional_budget=eps/dvg))
# Approximate synthetic cube distances: known geometry, Gaussian beam/noise,
# published exponential brightness extrapolated. No uv sampling or covariance fit.
pix=.025;xy=np.arange(-1.8,1.8+pix/2,pix);xx,yy=np.meshgrid(xy,xy);inc=np.deg2rad(40)
rad=np.sqrt(xx*xx+(yy/np.cos(inc))**2);rr=np.maximum(rad*6.70,.01)
cp=np.divide(xx,rad,out=np.zeros_like(rad),where=rad>0)
rd=rg/6.70;bright=4.6/(2*np.pi*rd*rd*np.cos(inc))*np.exp(-rad/rd)
beam=.17937769573198115;vel=np.arange(-700,701,10)
bb=disc(Ms,rs,rr)+disc(Mg,rg,rr)
vs={'FDESI':speed(bb,rr,A0*ratio),'MOND':speed(bb,rr,A0),'MOND_mimic':pm(fm['p'],rr),'NFW_published':np.sqrt(bb+halo(2e12,3.4,rr)),'NFW_mimic':ph(fh['p'],rr)}
sens=[]
for sig in [16.,30.]:
 def cube(kind):
  los=vs[kind]*np.sin(inc)*cp
  cc=bright[None,:,:]*np.exp(-.5*((vel[:,None,None]-los)/sig)**2)/(np.sqrt(2*np.pi)*sig)
  return gaussian_filter(cc,(0,beam/2.35482/pix,beam/2.35482/pix))*1.1331*beam**2
 fc=cube('FDESI')
 for kind in ['MOND','MOND_mimic','NFW_published','NFW_mimic']:
  d=fc-cube(kind)
  for noise in [.686,.8093]:
   den=(noise/1000)**2*1.1331*beam**2/pix**2
   sens.append(dict(model=kind,sigma=sig,noise_mJy10=noise,ideal_distance=float(np.sqrt(np.sum(d*d)/den)),outer_Rgt5_distance=float(np.sqrt(np.sum(d[:,rr>5]**2)/den))))
grid=[]
for mg in [1.2e11,1.5e11,1.8e11]:
 for rdgas in [.9,1.3,1.7]:
  for r in [3,5,7.5]:
   bb=disc(Ms,rs,r)+disc(mg,rdgas,r)
   grid.append(dict(Mgas=mg,Rd_gas=rdgas,R=r,F=float(speed(bb,r,A0*ratio)),M=float(speed(bb,r,A0))))
checks=dict(fits=fm['success'] and fh['success'],ordering=bool(np.all(M>F)),deep_limit=bool(np.all(1-F/M<1-ratio**.25)),disc_point_limit=bool(abs(disc(1e10,1,100)/(G*1e10/100)-1)<.002),newton_limit=bool(np.allclose(speed(b,R,0),np.sqrt(b))))
for name,data in [('predictions.csv',rows),('mass_size_grid.csv',grid),('sensitivity.csv',sens)]:
 with open(out/name,'w') as file:
  w=csv.DictWriter(file,fieldnames=data[0]);w.writeheader();w.writerows(data)
result=dict(ratio=ratio,MOND_mimic=fm,NFW_mimic=fh,checks=checks,rows=rows,sensitivity=sens)
(out/'results.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2));assert all(checks.values())
