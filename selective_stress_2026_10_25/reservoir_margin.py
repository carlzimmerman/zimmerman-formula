"""Frozen halo phase-margin test for the reciprocal pulse; no nonlinear claim."""
import argparse,json,sys
from pathlib import Path
import numpy as np,torch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'physical_completion_2026_10_25'))
from two_field import TwoField
from joint import T
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output)
m=TwoField(J=30);old=json.loads(Path('physical_completion_2026_10_25/run_two_field/J_30.0.json').read_text());n=m.n;mass=np.array(old['mass']);q=np.array(old['q']);x=T(old['v'][n:2*n]);rho=mass/m.vol.numpy();rad=np.array(old['r']);R=old['scaled_boundary_kpc'];mt=T(mass*q).requires_grad_(True)
u=m.A@mt;w,F=m.functions(u);s=torch.sin(torch.pi*x)**2/torch.pi**2;ff=m.functions((u[1:]+u[:-1])/2)[1]
response=torch.sum(m.vol*(w+m.beta*.95*s*F))+torch.sum(m.tw*m.functions(mt.sum()*m.tt**2)[0]/m.tt**4)+.5*m.ell2*torch.sum(m.rf**2/m.dr*ff*(x[1:]-x[:-1])**2)
Psi=torch.autograd.grad(response,mt)[0].detach().numpy();hF=2.5*m.K*(rho*(1-q))**(2/3);c=np.pi**2/4
A=m.volume_cost+m.J*rho+(m.beta*.95/c)*F.detach().numpy()
margin=Psi-hF-m.eps+m.J-m.J**2*rho/A;outside=rad>1.2*R
release=json.loads(Path('physical_completion_2026_10_25/run_free_finish/results.json').read_text())['released_energy_Eunit'];Mt=float(mass@q);factor=release/Mt
waves=json.loads(Path('selective_stress_2026_10_25/run_reciprocal_refine/results.json').read_text());tests=[]
for wave in waves['runs']:
 # The oscillator potential D=.25 is scaled to the actual benchmark release.
 # Coupling is to total converted mass M_T*N, so divide drive by M_T.
 drive=wave['maximum_exterior_chemical_drive_over_conversion_energy_per_fraction']*factor
 tests.append({'spacing':wave['spacing'],'domain':wave['domain'],'maximum_pulse_drive_in_halo_specific_energy_units':drive,'minimum_frozen_outer_phase_margin':float(min(margin[outside])),'margin_after_global_drive_upper_bound':float(min(margin[outside])-drive),'positive_pointwise_phase_Schur_margin':bool(min(margin[outside])>drive)})
out={'scope':'Sufficient local outer-F phase-Hessian positivity for frozen halo density and the measured global exterior drive envelope of the reduced smooth-source pulse. No nonlinear nucleation, density evolution, or actual halo-source-profile transport tested.','minimum_outer_phase_margin':float(min(margin[outside])),'maximum_outer_T_fraction_local':float(max(q[outside])),'converted_mass_Mb':Mt,'release_Eunit':release,'release_per_converted_mass':factor,'tests':tests,'derivation':'At outer x=y=0 the phase quadratic/c has matrix [[B+Jrho+beta*C*F/c,-Jrho],[-Jrho,rho*(Psi-hF-epsilon+J-drive)]]. Dropped gradient terms are positive. Its Schur complement divided by rho gives the stated margin.','r':rad.tolist(),'outer_margin':margin.tolist(),'outer_selector':outside.tolist(),'non_claims':['The source pulse is reduced-model output, not a self-consistent full halo evolution','Actual density/carrier/matter variables remain frozen for this response check','Alignment-only gap is not used; simultaneous carrier/matter conversion is included','Static law and stiffness preservation do not repair existing multi-mass failures']}
dest.write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items() if k in ['minimum_outer_phase_margin','maximum_outer_T_fraction_local','converted_mass_Mb','release_Eunit','tests']},flush=True)
