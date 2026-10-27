import json,argparse
from pathlib import Path
import numpy as np
from scipy.special import roots_laguerre
from scipy.optimize import brentq
from scipy.integrate import solve_ivp
pa=argparse.ArgumentParser();pa.add_argument('--output');args=pa.parse_args();M0=130257985.45037776;ell=.4404221297174536;t0=.012074272908402984;H0=67.4*1000/3.085677581491367e22*(365.25*86400*1e9);Om=.315;gap=.2;d=.125;eps=.1
H=lambda z:H0*np.sqrt(Om*(1+z)**3+1-Om)
age=lambda z:2/(3*H0*np.sqrt(1-Om))*np.arcsinh(np.sqrt((1-Om)/Om)/(1+z)**1.5)
quad_cache={}
def radiate(m,R,omega,n=64):
 if n not in quad_cache:
  u,w=roots_laguerre(n);quad_cache[n]=(u,w)
 u,w=quad_cache[n];s=R*R+2*u[:,None];v=R*R+2*u[None,:];ss=s+v;weight=w[:,None]*w[None,:]
 q=np.sqrt(max(0,omega*omega-gap*gap))
 base=(4*np.pi*m)**2/(2*np.pi)**1.5*ss**(-1.5)*np.exp(-q*q*s*v/(2*ss))
 deriv=-eps*R*R*(3/ss+.5*q*q*(s*s+v*v)/ss**2)
 source=float(np.sum(weight*base*deriv));power=omega*q*source*source/(32*np.pi*np.pi*d) if omega>gap else 0.
 # Gaussian-mixture representation independently diagnoses perturbative field size.
 widths=R*R+2*u;hmax=float(4*np.pi*m*np.sum(w/(2*np.pi*widths)**1.5));rr=np.linspace(0,5*R,301);pp=4*np.pi*m*np.sum(w[None,:]*rr[:,None]/widths[None,:]*np.exp(-rr[:,None]**2/(2*widths[None,:]))/(2*np.pi*widths[None,:])**1.5,axis=1)
 return dict(power=power,source=source,maxP=float(max(pp)),chi_bound=100*hmax*hmax,q=q)
clocks=[]
for factor in [1,2]:
 z=brentq(lambda z:factor*10*H(z)*t0-gap,0,100);clocks.append(dict(frequency_factor=factor,z_open=z,age_Gyr=age(z)))
rows=[]
for z in [0,3,6,10,20,30]:
 for factor in [1,2]:
  omega=factor*10*H(z)*t0
  for M in np.geomspace(1e5,1e11,25):
   m=M/M0;R=(m/(100*(H(z)*t0)**2))**(1/3);r=radiate(m,R,omega);binding=m*m/(2*np.sqrt(np.pi)*R)
   rows.append(dict(z=z,factor=factor,mass_Msun=float(M),R_kpc=R*ell,omega=omega,weak_valid=r['maxP']<.1 and r['chi_bound']<.1,**r,cooling_Gyr=binding/r['power']*t0 if r['power']>0 else None,age_Gyr=age(z)))
checks=[]
def ck(n,b,v):checks.append(dict(name=n,passed=bool(b),value=v))
repeats=[]
for z,M,factor in [(10,1e7,2),(20,1e7,1),(20,1e9,1),(30,1e7,2)]:
 m=M/M0;R=(m/(100*(H(z)*t0)**2))**(1/3);om=factor*10*H(z)*t0;a=radiate(m,R,om,64);b=radiate(m,R,om,128);err=abs(a['power']/b['power']-1) if b['power'] else 0;repeats.append(dict(z=z,M=M,R=R,relative_power=err));ck('quadrature_%s_%s_%s'%(z,M,factor),err<.02,err)
# Fixed geometry/source history reproduces exactly quartic perturbative phase power.
a=radiate(.01,2,.4);b=radiate(.02,2,.4);ck('fixed_geometry_quartic',abs(b['power']/a['power']-16)<1e-10,b['power']/a['power'])
# Exact source Fourier derivative check via independently differenced h-square transform.
u,w=quad_cache[128]
def transform(m,R,q):
 s=R*R+2*u[:,None];v=R*R+2*u[None,:];return np.sum(w[:,None]*w[None,:]*(4*np.pi*m)**2/(2*np.pi)**1.5/(s+v)**1.5*np.exp(-q*q*s*v/(2*(s+v))))
R=2.;om=.4;q=np.sqrt(om*om-gap*gap);dr=1e-4;fd=eps/2*(transform(.01,R*np.exp(dr),q)-transform(.01,R*np.exp(-dr),q))/(2*dr);an=radiate(.01,R,om,128)['source'];ck('breathing_source_derivative',abs(fd/an-1)<1e-6,float(abs(fd/an-1)))
# Prior imposed EdS growth diagnostic, deliberately distinct from the clock cosmology.
fb=1/6.364;fc=1-fb;ellMpc=ell/1000;N0=-np.log(1101)
def growth(z,k):
 nf=-np.log(1+z);ai=np.exp(N0)
 def rhs(N,Y):
  b,bp,c,cp=Y;S=1/(1+(k*ellMpc/np.exp(N))**2) if N<nf else 1
  return [bp,-.5*bp+1.5*(fb*b+fc*c),cp,-.5*cp+1.5*(fb*b+fc*S*c)]
 pre=solve_ivp(rhs,(N0,nf),[ai]*4,rtol=1e-10,atol=1e-13);post=solve_ivp(rhs,(nf,0),pre.y[:,-1],rtol=1e-10,atol=1e-13);return fb*post.y[0,-1]+fc*post.y[2,-1]
growth_rows=[dict(z=z,k=k,retained=growth(z,k)) for z in [clocks[0]['z_open'],clocks[1]['z_open'],20,30,100] for k in [.1,1]]
# Measured losses: no constant-time extrapolation. Available matter remains an independent mass moment.
root=Path(__file__).resolve().parents[1];emp=[]
for b in [1,2,4]:
 r=json.loads((root/f'fragment_radiation_2026_10_22/mass{b}_run/result.json').read_text());emp.append(dict(b=b,loss_fraction=r['rows'][-1]['absorbed']/abs(r['E0']),time_Gyr=18*t0))
long=json.loads((root/'fragment_radiation_2026_10_22/long_run/result.json').read_text());emp.append(dict(b=4,loss_fraction=long['rows'][-1]['absorbed']/abs(long['E0']),time_Gyr=60*t0))
# Same cosmic total cold inventory, different supply spectra: identities, not predictions.
rhocrit=3*(67.4*1000/3.085677581491367e22)**2/(8*np.pi*6.67430e-11)*3.085677581491367e22**3/1.98847e30;rhoc=.265*rhocrit
population=[dict(mass_Msun=M,formed_fraction=F,number_Mpc3=F*rhoc/M) for M in [1e6,1.0952264e7,1e8] for F in [.01,.1,1]]
result=dict(checks=checks,clocks=clocks,rows=rows,repeats=repeats,growth=growth_rows,measured_cooling=emp,population_counterexamples=population,rho_c0=rhoc,clock_age0=age(0))
Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
