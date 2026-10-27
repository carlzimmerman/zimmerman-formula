"""Conditional miscibility window and trap tradeoff in the assigned portal model."""
import json,math,sys
from pathlib import Path
import numpy as np
import sympy as s
from scipy.optimize import brentq
shell=json.loads(Path('sol61_push/silica_shell_retention_2026_10_14/run/results.json').read_text())
m=1.;lam=1e-6;delta=2e-9;M=2*m+delta;Delta=delta*(4*m+delta);hc=1.973269804e-7;c=299792458.;n=3e14*hc**3
checks=[]
def ck(name,error,tol):
 assert error<tol,(name,error,tol)
 checks.append(dict(name=name,error=float(error),tolerance=tol))
# Exact rational identities: threshold matching, interval width.
q,d,L,u=s.symbols('q d L u',positive=True)
gs=L/2-u/(4*q);gc=L-u/(4*q)-u/(4*d)
lo=2*L*d;hi=6*L*q*d/(q+2*d)
for name,expr in [('density_eigenvalue',gs+gc-(s.Rational(3,2)*L-u/(2*q)-u/(4*d))),('charge_eigenvalue',gs-gc-(-L/2+u/(4*d))),('interval_width',hi-lo-4*L*d*(q-d)/(q+2*d))]:
 assert s.factor(expr)==0
 checks.append(dict(name=name,exact=True))
rows=[]
for detuning in [2e-9,1e-6,1e-5,.001,.3]:
 mass=2*m+detuning;gap=detuning*(4*m+detuning);lower=2*lam*gap;upper=6*lam*mass**2*gap/(mass**2+2*gap)
 mu=math.sqrt((lower+upper)/2);g_same=lam/(2*m*m)-mu*mu/(4*m*m*mass*mass);g_cross=(lam-mu*mu/(4*mass*mass)-mu*mu/(4*gap))/(m*m)
 U=shell['barrier_eV']*(mu/.002)*(M/mass)**2
 radius=math.pi*hc/math.sqrt(8*m*U)
 assert g_same+g_cross>0 and g_same-g_cross>0
 z=.02*math.sqrt(2*m*U)/hc
 energy=None
 if z>math.pi/2:
  root=brentq(lambda x:x/math.tan(x)+math.sqrt(max(0.,z*z-x*x)),math.pi/2+1e-12,min(z,math.pi)-1e-12,xtol=1e-14)
  ck('spherical_well_matching_'+str(detuning),abs(root/math.tan(root)+math.sqrt(z*z-root*root)),1e-10)
  energy=hc*hc*root*root/(2*m*.02**2)
  assert 0<energy<U
 source_ratio=(mu/.002)*Delta/gap
 rows.append(dict(infinite_exterior_2cm_ground_energy_eV=energy,threshold_plane_wave_source_amplitude_ratio=source_ratio,detuning_eV=detuning,mu_lower_eV=math.sqrt(lower),mu_upper_eV=math.sqrt(upper),selected_mu_eV=mu,density_eigenvalue_eV_minus2=g_same+g_cross,charge_eigenvalue_eV_minus2=g_same-g_cross,scaled_barrier_eV=U,infinite_exterior_s_wave_threshold_radius_m=radius,barrier_over_2cm_threshold=U/(math.pi**2*hc**2/(8*m*.02**2))))
row=rows[0];mu=row['selected_mu_eV'];h=mu/(2*m*math.sqrt(2*M));gs=lam/(2*m*m)-mu*mu/(4*m*m*M*M);gc0=(lam-mu*mu/(4*M*M))/(m*m);gp=gs+gc0
scale=max(delta,h*math.sqrt(n),gp*n)
def eq(n):
 df=lambda f:delta/2-h*math.sqrt(n/2)*(1-3*f)/(2*math.sqrt(f))-gp*n*(1-f)/2
 f=brentq(df,1e-20,1-1e-14,xtol=1e-18)
 A=math.sqrt(n*(1-f)/2);r=-math.sqrt(n*f/2);chem=gp*A*A+h*r
 return A,r,chem,f
A,r,chem,f=eq(n);dchem=(eq(n*1.0001)[2]-eq(n*.9999)[2])/(.0002*n)
assert dchem>0
ck('stationarity',abs((delta-2*chem)*r+h*A*A)/(scale*math.sqrt(n)),1e-12)
def bdg(k):
 LL=np.array([[(2*gs+gc0)*A*A-chem+k*k/(2*m),gc0*A*A,h*A],[gc0*A*A,(2*gs+gc0)*A*A-chem+k*k/(2*m),h*A],[h*A,h*A,delta-2*chem+k*k/(2*M)]])
 BB=np.array([[gs*A*A,gc0*A*A+h*r,0],[gc0*A*A+h*r,gs*A*A,0],[0,0,0.]])
 return np.block([[LL,BB],[-BB,-LL]])
ks=np.sqrt(m*scale)*np.exp(np.linspace(-6,3,301));maximag=0.;maxpair=0.
for k in ks:
 ev=np.linalg.eigvals(bdg(k));maximag=max(maximag,float(max(abs(ev.imag))))
 maxpair=max(maxpair,max(min(abs(z+ev)) for z in ev)/(scale+k*k/m))
ck('bounded_spectrum_imaginary_part_over_scale',maximag/scale,1e-9)
ck('bounded_spectrum_plus_minus',maxpair,1e-10)
# At k small, lowest two positive frequencies are density and charge sound.
k=ks[0];ev=np.sort(np.linalg.eigvals(bdg(k)).real);positive=ev[ev>0];density_speed=math.sqrt(n*dchem/m)
ck('density_sound_derivative',abs(positive[0]/k/density_speed-1),.01)
# Static potential normalization: V=m²X+lambda X²+mu R X+M²R²/2.
quartic_static=lam-mu*mu/(2*M*M);assert quartic_static>0
result=dict(scope='Changed free parameter mu; threshold miscibility and bounded explicit-mediator coherent spectrum, not a created or cosmologically identified substance',rows=rows,selected=dict(total_density_per_m3=3e14,mu_eV=mu,mixing_h_sqrt_n_over_delta=h*math.sqrt(n)/delta,mediator_constituent_fraction=f,chemical_potential_eV=chem,n_dmu_dn_eV=n*dchem,density_sound_speed_m_s=c*density_speed,static_effective_quartic=quartic_static,spectrum_wave_number_count=len(ks),spectrum_log_relative_bounds=[-6,3]),checks=checks,passed=len(checks))
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
