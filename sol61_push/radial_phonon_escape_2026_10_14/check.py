"""On-shell radial phonon transitions to finite-shell continuum scattering states."""
import json,math,sys
from pathlib import Path
import numpy as np
from scipy.special import spherical_jn as j,spherical_yn as y
from scipy.optimize import brentq
from numpy.polynomial.legendre import leggauss
modes=json.loads(Path('sol61_push/shell_radial_noise_2026_10_14/run/results.json').read_text())
poles=json.loads(Path('sol61_push/stable_window_retention_2026_10_14/run/retention.json').read_text())
sources=json.loads(Path('sol61_push/stable_window_retention_2026_10_14/run/source.json').read_text())
hc=1.973269804e-7;hbe=6.582119569e-16;ev=1.602176634e-19;hb=hbe*ev;kb=1.380649e-23;T=300.;alpha=1-2*(3750/6000)**2;checks=[]
quadratures={N:leggauss(N) for N in [384,768]}
def ck(name,e,t):
 assert e<t,(name,e,t)
 checks.append(dict(name=name,error=float(e),tolerance=t))
def stress(fun,z):return fun(1,z,derivative=True)+2*alpha*fun(1,z)/z
cases=[]
for case in modes['cases']:
 label=case['candidate'];a=case['radius_m'];b=case['outer_radius_m'];pole=[p for p in poles['rows'] if p['candidate']==label][-1];U=pole['barrier_eV'];source=next(s for s in sources['rows'] if s['candidate']==label)
 z0=a/hc*math.sqrt(2*U);z=brentq(lambda z:z/math.tan(z)+math.sqrt(z0*z0-z*z),math.pi/2+1e-12,min(z0,math.pi)-1e-12);decay=math.sqrt(z0*z0-z*z)/a
 norm=.5-math.sin(2*z)/(4*z)+math.sin(z)**2/(2*decay*a);E0=hc*hc*z*z/(2*a*a)
 def initial(r):return math.sin(z)/math.sqrt(a*norm)*np.exp(-decay*(np.asarray(r)-a))
 def final_state(E):
  # Regular u=sin(kr) inside, continuous u,u' at a and b.
  k=math.sqrt(2*E)/hc;ua=math.sin(k*a);upa=k*math.cos(k*a);p=math.sqrt(2*abs(E-U))/hc
  def raw(r):
   s=np.asarray(r)-a
   if E>U:return ua*np.cos(p*s)+upa/p*np.sin(p*s),-ua*p*np.sin(p*s)+upa*np.cos(p*s)
   return ua*np.cosh(p*s)+upa/p*np.sinh(p*s),ua*p*np.sinh(p*s)+upa*np.cosh(p*s)
  ub,upb=raw(b);amp=math.hypot(float(ub),float(upb)/k)
  # Continuum normalization integral u_E u_E' dr=delta(E-E'), E in eV.
  normalization=math.sqrt(2/(math.pi*hc*hc*k))/amp
  return lambda r:tuple(normalization*t for t in raw(r)),normalization,k,ua,upa
 rows=[]
 for im,mode in enumerate(case['modes']):
  q=mode['q'];om=2*math.pi*mode['frequency_Hz'];quantum=hbe*om;nb=1/math.expm1(quantum*ev/(kb*T));xzp2=hb/(2*mode['effective_mass_kg']*om)
  A=stress(y,q*a/b);B=-stress(j,q*a/b);sc=math.hypot(A,B);A/=sc;B/=sc
  def f(r):return A*j(1,q*np.asarray(r)/b)+B*y(1,q*np.asarray(r)/b)
  def fp(r):return q/b*(A*j(1,q*np.asarray(r)/b,derivative=True)+B*y(1,q*np.asarray(r)/b,derivative=True))
  for sign,kind,occupation in [(1,'absorption',nb),(-1,'emission',nb+1)]:
   E=E0+sign*quantum
   if E<=0:continue
   final,fac,k,ua,upa=final_state(E)
   u0,up0=final(a);ck(label+'_'+str(im)+'_'+kind+'_inner_matching',max(abs(u0-fac*ua),abs(up0-fac*upa)/k)/max(abs(fac),1e-300),1e-12)
   def coupling(N):
    x,w=quadratures[N];r=a+(x+1)*(b-a)/2;w=w*(b-a)/2;u,up=final(r);ui=initial(r)
    parts=U*np.dot(w,ui*(up-(decay+2/r)*u)*f(r))
    direct=-U*(np.dot(w,u*ui*(fp(r)+2*f(r)/r))+final(a)[0]*initial(a)*f(a)-final(b)[0]*initial(b)*f(b))
    return parts,direct
   coarse,direct=coupling(384);C,_=coupling(768)
   ck(label+'_'+str(im)+'_'+kind+'_quadrature',abs(coarse-C)/max(abs(C),1e-100),1e-7)
   ck(label+'_'+str(im)+'_'+kind+'_surface_bulk',abs(coarse-direct)/max(abs(C),1e-100),1e-7)
   rate=2*math.pi/hbe*xzp2*occupation*C*C
   rows.append(dict(mode=im+1,channel=kind,final_energy_eV=E,phonon_energy_eV=quantum,final_above_barrier=E>U,continuum_matrix_element_sqrt_eV_per_m=float(C),escape_rate_per_s=float(rate)))
 sums={str(N):sum(r['escape_rate_per_s'] for r in rows if r['mode']<=N) for N in [10,20,40]}
 cases.append(dict(candidate=label,initial_reference_energy_eV=E0,rows=rows,partial_escape_sums_per_s=sums,absorption_sum_per_s=sum(r['escape_rate_per_s'] for r in rows if r['channel']=='absorption'),emission_sum_per_s=sum(r['escape_rate_per_s'] for r in rows if r['channel']=='emission'),resolved_escape_to_drive_ratio=sums['40']/source['pair_drive_per_s'],resolved_escape_to_tunneling_ratio=sums['40']*pole['lifetime_s']))
result=dict(scope='First forty radial shell phonons, on-shell Golden-rule absorption/emission from reference quasi-bound orbital to energy-normalized finite-shell l=0 continuum; no other angular modes or finite-linewidth integral',cases=cases,checks=checks,passed=len(checks))
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(passed=len(checks),cases=[{k:v for k,v in x.items() if k!='rows'} for x in cases]),indent=2))
