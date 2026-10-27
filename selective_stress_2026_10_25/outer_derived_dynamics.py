"""Canonical relative-material phase response to the measured outgoing pulse.

Density frozen, carrier adiabatic, local spatial gradients omitted. This is a
conditional dynamical test rather than inferring stability from a positive
instantaneous energy matrix.
"""
import argparse,json,sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'physical_completion_2026_10_25'))
from two_field import TwoField
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output)
m=TwoField(J=30);halo=json.loads(Path('physical_completion_2026_10_25/run_two_field/J_30.0.json').read_text());margin=json.loads(Path('selective_stress_2026_10_25/run_reservoir_halo_margin/results.json').read_text());wave=next(w for w in json.loads(Path('selective_stress_2026_10_25/run_derived_inertia_wave/results.json').read_text())['runs'] if w['case']=='whole_release_hypothesis' and w['exact_gapped_state_kinetic'])
rad=np.array(halo['r']);rho=np.array(halo['mass'])/m.vol.numpy();q=np.array(halo['q']);u=m.A.numpy()@(np.array(halo['mass'])*q);F=u*u/(1-u);A=m.volume_cost+m.J*rho+m.beta*.95*F/(np.pi**2/4);b=np.array(margin['outer_margin']);aa=b+m.J**2*rho/A
R=halo['scaled_boundary_kpc'];pr=np.array(wave['probe_r_over_R'])*R;a0=np.interp(pr,rad,aa);b0=np.interp(pr,rad,b)
release=margin['release_Eunit'];Mt=margin['converted_mass_Mb'];pulse=np.array(wave['pulse']);times=pulse[:,0];drive=pulse[:,1:]*release/(.25*Mt)
# Canonical Schroedinger material action has sigma=sqrt(kappa) in dynamical
# units. Inertia was not inferred from the static branch; it is an explicit
# canonical dynamical completion consistent with the previous wave coefficient.
kpc=3.085677581491367e19;Myr=365.25*86400*1e6;A0_SI=9.3603e-11;vunit=np.sqrt(A0_SI*m.rm*kpc);tdyn=m.rm*kpc/vunit/Myr;tquant=(m.material_length/m.rm)*tdyn;pulse_time_Myr=100.;sigma=tquant/pulse_time_Myr
out={'runs':[],'canonical_material_time_Myr':tquant,'pulse_time_unit_Myr':pulse_time_Myr,'sigma_in_pulse_units':sigma,'probe_r_over_R':wave['probe_r_over_R'],'a0':a0.tolist(),'b0':b0.tolist(),'non_claims':['Local frozen-density canonical spinor dynamics with fast adiabatic carrier; no full nonlinear mobile halo','No continuum or nonradial stability theorem','Canonical time action and100Myr pulse scale are stated hypotheses','Wave backreaction from infinitesimal T perturbation is second order and omitted']}
for pulse_time_Myr in [wave['physical_time_unit_Myr']]:
 sigma=tquant/pulse_time_Myr
 for sub in [1,2,4]:
  S=np.tile(np.eye(2),(len(pr),1,1));maxgain=np.ones(len(pr));maxdet=np.zeros(len(pr));mingap=np.full(len(pr),np.inf)
  for i in range(len(times)-1):
   dt=(times[i+1]-times[i])/sub
   for j in range(sub):
    d=drive[i]+(j+.5)/sub*(drive[i+1]-drive[i]);a=a0-d;b=b0-d;assert min(b)>0 and min(a)>0
    omega=np.sqrt(a*b)/sigma;arg=omega*dt;cs=np.cos(arg);ss=np.sin(arg);M=np.zeros_like(S);M[:,0,0]=cs;M[:,1,1]=cs;M[:,0,1]=ss*np.sqrt(a/b);M[:,1,0]=-ss*np.sqrt(b/a);S=M@S
    # Energy-normalized singular value bounds ALL initial perturbation phases.
    W=S*np.sqrt(np.array([b,a]).T)[:,:,None]/np.sqrt(np.array([b0,a0]).T)[:,None,:]
    tr=np.sum(W*W,axis=(1,2));det=W[:,0,0]*W[:,1,1]-W[:,0,1]*W[:,1,0];gain=(tr+np.sqrt(np.maximum(tr*tr-4*det*det,0)))/2
    maxgain=np.maximum(maxgain,gain);ds=S[:,0,0]*S[:,1,1]-S[:,0,1]*S[:,1,0];maxdet=np.maximum(maxdet,abs(ds-1));mingap=np.minimum(mingap,b)
  r={'pulse_time_unit_Myr':pulse_time_Myr,'sigma_in_pulse_units':sigma,'substeps_per_pulse_sample':sub,'maximum_perturbation_energy_gain_over_initial':maxgain.tolist(),'minimum_phase_gap_during_pulse':mingap.tolist(),'symplectic_determinant_error':maxdet.tolist(),'final_transfer_matrix':S.tolist()};assert max(maxdet)<1e-8;out['runs'].append(r);dest.write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in r.items() if k!='final_transfer_matrix'},flush=True)
