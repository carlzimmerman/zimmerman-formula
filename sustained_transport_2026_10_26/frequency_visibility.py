"""Exact radial retarded form factor for the linear common-transport source."""
import argparse,json
from pathlib import Path
import numpy as np
from dynamics import model,load
p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args();m=model();a=load('infall_pump_2026_10_25/run_smooth_prepare/state.npz')[0];rho=abs(a)**2/m.vol;re=(m.r[:-1]+m.r[1:])/2;dr=np.diff(m.r);AT=re**2*np.sqrt(rho[0,:-1]*rho[0,1:]);A=AT+re**2*np.sqrt(rho[1,:-1]*rho[1,1:]);B=A*dr
ref=np.load('infall_pump_2026_10_25/run_static_polish/state.npz')['a'];target=np.sum(abs(ref)**2,axis=0);target*=5.364/np.sum(target);delta=np.cumsum(target-np.sum(abs(a)**2,axis=0))[:-1];sel=(B>max(B)*1e-14)&(re*m.rm<200);v=np.zeros_like(A);v[sel]=-delta[sel]/A[sel];kin=float(B@(v*v));rows=[]
for omega in [0.,.1,1.,3.,10.,30.,100.,300.,500.,1000.]:
 k=omega*m.tdyn/m.c;form=np.sinc(k*m.r/np.pi);L=m.g2*AT*((-1.5*rho[0,:-1]+.5*rho[0,1:])*form[:-1]+(1.5*rho[0,1:]-.5*rho[0,:-1])*form[1:]);bright=np.zeros_like(A);bright[sel]=L[sel]/B[sel];norm=float(B@(bright*bright));q=float(L@v)
 rows.append({'frequency_rad_Myr':omega,'retarded_source_functional_on_required_tangent':q,'bright_kinetic_fraction':q*q/(kin*norm),'source_functional_dual_norm_squared':norm,'photon_power_per_unit_harmonic_velocity_squared_Eunit_Myr':float(omega*omega*m.tdyn/m.c**3*q*q)})
# Independent radial source-cell construction of the same form-factor sum.
j=AT*v;src=np.zeros(m.n);src[:-1]+=m.g2*j*(-1.5*rho[0,:-1]+.5*rho[0,1:]);src[1:]+=m.g2*j*(1.5*rho[0,1:]-.5*rho[0,:-1]);errors=[]
for r in rows:
 form=np.sinc(r['frequency_rad_Myr']*m.tdyn/m.c*m.r/np.pi);errors.append(abs(float(form@src)-r['retarded_source_functional_on_required_tangent']))
assert max(errors)<1e-10
out={'cases':rows,'independent_source_sum_max_error':max(errors),'non_claim':'Frozen linear common-transport source at a chosen harmonic frequency; no oscillation/population is imposed in formation runs. Power coefficient is conditional on that harmonic velocity, not a generated or sustained power measurement. Nonlinear mode conversion remains open.'};Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(rows)
