#!/usr/bin/env python3
"""Pressure with polarization subtraction; scalar coefficient cap on fixed target."""
import argparse,importlib.util,json,math
from pathlib import Path
import numpy as np
from scipy.integrate import simpson,cumulative_trapezoid
from scipy.optimize import brentq
base=Path('research_closure_2026_11_12/closure_push_02/static_gate')
spec=importlib.util.spec_from_file_location('physical_annulus',base/'check_physical_annulus.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
sol,benchmark=mod.run(198.25,4.,tol=5e-7)
assert benchmark['accepted_finite_annulus']
rM=benchmark['rM_Mpc'];ell=benchmark['ell'];d=benchmark['d'];Lstar=ell*rM
C_LIGHT=299792458.;a=9.3603e-11/C_LIGHT**2*3.0857e22;eps=a*rM
x=np.geomspace(1,60,12001);r=rM*x;f,y,p,Z=sol.sol(x);yp=sol.sol(x,1);Zprime=yp[3]/rM
phi=eps*f;N=np.exp(phi);Q=np.exp(-phi);qoff=np.expm1(-phi);A=a*y
KPi=a/rM*Z;KPi_prime=a/rM*Zprime;KPic=a*d/rM;u=KPi/KPic
S,Sp,Spp=mod.gate(u)
assert np.min(u)>4 and np.max(p)<1 and np.min(p)>0
mu=198.25;Cgeo=mu*mu/2;delta=1/(mu*mu)
Qmax=float(np.max(Q));xmax=Qmax-1
LQ2=xmax*xmax/(Qmax*(-math.log1p(-delta)))*(1+1e-9)
t=qoff*qoff/(LQ2*Q);expmt=np.exp(-t)
KB_over_Q=Cgeo*LQ2*(-np.expm1(-t));KB=Q*KB_over_Q
KM=float(Cgeo*LQ2*(-math.expm1(-xmax*xmax/(LQ2*Qmax))))
Imin=3*math.exp(-2/3);zcomb=S-u*Sp
KrhoH=Cgeo*np.expm1(-2*phi)*(-np.expm1(-t)+S*expmt)
KR=Cgeo*qoff*qoff-KB
KpH=KR+KB*zcomb+Q*KM*(Imin-zcomb)
KWB=a*a*(-p-np.log1p(-p));KPWp=a*a*p*p/(1-p)
KPA=a*a*p*y
Kstiff_active=2*Lstar*Lstar*KPi*KPi/2
# T is the residual after removing the exact constant QPi boundary slope.
Tgate=(KM-KB_over_Q)*Sp/KPic
Qprime=-Q*A
KBoverQ_prime=Cgeo*expmt*(1-1/(Q*Q))*Qprime
Tgate_prime=-KBoverQ_prime*Sp/KPic+(KM-KB_over_Q)*Spp*KPi_prime/(KPic*KPic)
Tgamma=N*Lstar*Lstar*KPi/2
Tgamma_prime=N*Lstar*Lstar*(KPi_prime+A*KPi)/2
constitutive=A+(Tgate_prime+Tgamma_prime)/N-a*p/(1-p)
normalization=a*rM*rM
flux=r*r*N*a*(y-p)
flux_delta=float((flux[-1]-flux[0])/normalization)
source_without_lambda=KrhoH+3*KpH+2*(KPWp-KWB)+Kstiff_active-KPA
pressure_mass=float(simpson(r*r*N*3*KpH,x=r)/normalization)
clock_energy_mass=float(simpson(r*r*N*KrhoH,x=r)/normalization)
field_work_mass=float(simpson(r*r*N*(2*(KPWp-KWB)+Kstiff_active-KPA),x=r)/normalization)
volweighted=float(simpson(r*r*N,x=r)/normalization)
rows=[]
for Lam in [0.,1e-7,1.1e-7]:
 mass=float(simpson(r*r*N*(source_without_lambda-Lam),x=r)/normalization)
 rows.append({'Lambda_Mpc_inverse2':Lam,'required_polarized_flux_change_baryon_units':mass,'target_polarized_flux_change_baryon_units':flux_delta,'equation_residual_baryon_units':mass-flux_delta})
# Independently reconstruct spatial weak potential from the normal-energy equation.
Krho=KPi+KrhoH+KWB+Lstar*Lstar*KPi*KPi/4
spatial_flux=r[0]*r[0]*A[0]+cumulative_trapezoid(r*r*Krho,r,initial=0)
psiprime=spatial_flux/(r*r)
psi=-r[-1]*psiprime[-1]-np.flip(cumulative_trapezoid(np.flip(psiprime),-np.flip(r),initial=0))
quiet={'definition':'Explicit minimum-moment rectangular-band Gamma on accepted strongly-off annulus; target substitution, not repaired-action BVP','baseline_BVP':benchmark,'mu_Mpc_inverse':mu,'Qmax':Qmax,'LQ_squared':LQ2,'K_Bband':KM,'energy_fraction_max':float(np.max(-np.expm1(-t)+S*expmt)),'delta':delta,'minimum_u':float(np.min(u)),'max_gate_residual_potential':float(np.max(np.abs(Tgate))),'max_gate_force_shift_fraction':float(np.max(np.abs(Tgate_prime/(N*A)))),'max_full_constitutive_residual_over_force':float(np.max(np.abs(constitutive/A))),'max_original_stiffness_force_fraction':float(np.max(np.abs(Tgamma_prime/(N*A)))),'target_polarized_flux_change_baryon_units':flux_delta,'pressure_mass_baryon_units':pressure_mass,'clock_energy_mass_baryon_units':clock_energy_mass,'remaining_field_work_mass_baryon_units':field_work_mass,'Lambda_exactly_canceling_integrated_residual_Mpc_inverse2':(pressure_mass+clock_energy_mass+field_work_mass-flux_delta)/volweighted,'max_abs_reconstructed_spatial_potential':float(np.max(np.abs(psi))),'lambda_rows':rows}
assert quiet['max_full_constitutive_residual_over_force']<1e-7
assert quiet['max_gate_force_shift_fraction']<1e-15
# Separate deformation-independent raw lapse bound, using the fixed original target.
target=json.loads((base/'matching/run01/results.json').read_text())
inner=next(z for z in target['rows'] if z['mu_Mpc_inverse']==25120. and z['r_over_rM']==1.)
outer=next(z for z in target['rows'] if z['mu_Mpc_inverse']==25120. and z['r_over_rM']==60.)
qi=1-inner['phi_geo'];qo=1-outer['phi_geo'];xi=qi-1
ri=inner['r_Mpc'];ro=outer['r_Mpc']
lapse_flux=ro*ro*a*outer['g_over_a0']/qo**2-ri*ri*a*inner['g_over_a0']/qi**2
volume=(ro**3-ri**3)/qi

def floor(mu):
 dd=1/(mu*mu);TT=-math.log1p(-dd)
 M=mu*mu/2*xi*xi/qi*dd/TT
 return M*(Imin-(1-3*math.log(dd))*dd)

def ratio(mu,Lam=0.):return (floor(mu)-Lam/3)*volume/lapse_flux
caps=[]
for Lam in [0.,1e-7,1.1e-7]:
 crit=brentq(lambda z:ratio(z,Lam)-1,198.25,1000,xtol=1e-10)
 caps.append({'Lambda_Mpc_inverse2':Lam,'mu_necessary_upper_Mpc_inverse':crit,'ratio_at_root':ratio(crit,Lam),'ratio_mu198p25':ratio(198.25,Lam),'ratio_mu25120':ratio(25120.,Lam),'assumptions':'Same Q profile,boundaryaccelerations,weakspatialgeometry; energyceilingdelta1/mu²; concavityrectangularQband[1,Qmax],Pi>=0; rho>=0,noaddednegative-activecompensation. IndependentofquietP.'})
result={'quiet_minimal_band_polarized_pressure':quiet,'raw_lapse_necessary_mu_upper_bound':caps,'limitations':['Polarized subtraction result tests quiet constitutive annulus with actualu>=4, not all deformed polarization profiles.','Raw lapse scalar cap permits deformedP subject topositiveenergy andsame Q/force target, but remains conditional on this action class and supplied energy ceiling.','Lambda values are explicit benchmarks, not a refit or measured cosmological claim.','Weak spatial metric approximation is retained; anisotropic stress is included through exact rho+traceS before this approximation.']}
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
Path(args.output).write_text(json.dumps(result,indent=2,allow_nan=False)+'\n');print(json.dumps(result,indent=2,allow_nan=False))
