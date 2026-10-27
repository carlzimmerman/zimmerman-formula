"""Joint verdict from the complete accepted autonomous history, never probes."""
import argparse,json
from pathlib import Path
import numpy as np
from scipy.interpolate import CubicSpline
from dynamics import model,load,field
from radiative_modes_final import decompose
p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args();dest=Path(args.output);base=Path('sustained_transport_2026_10_26');m=model();chain=[Path('infall_pump_2026_10_25/run_smooth_infall')]+[base/n for n in ['run_continue','run_continue_second','run_continue_large']];tr=[];hist=[];offset={k:0. for k in ['escaped_energy','net_material_to_wave_work','bulk_current_work','conversion_work','far_net_flux']};runs=[]
for root in chain:
 d=json.loads((root/'results.json').read_text());runs.append(d);last=None
 for row in d['trace']:
  if tr and row['time_Myr']<=tr[-1]['time_Myr']+1e-9:continue
  rr=row.copy()
  for k in offset:rr[k]+=offset[k]
  tr.append(rr)
 for k in offset:offset[k]+=d['trace'][-1][k]
 hh=np.load(root/'history.npz')['history']
 for row in hh:
  if not hist or row[0]>hist[-1][0]+1e-9:hist.append(row)
hist=np.array(hist);times=hist[:,0];n=(hist.shape[1]-1)//4;src=hist[:,1+2*n:1+3*n];state=load(chain[-1]/'state.npz');initial=load('infall_pump_2026_10_25/run_smooth_prepare/state.npz');a,x,cp,c,v=state;t=runs[-1]['completed_time_Myr'];rad=decompose(m.wr,c,v,m.c,m.tdyn,500/m.rm,9000/m.rm);I=np.sum(src,axis=1)
# Retrodict the final outgoing field from the entire actual source history.
mask=(m.wr>=500/m.rm)&(m.wr<=9000/m.rm);r=m.wr[mask];h=float(np.mean(np.diff(r)));re=(r[1:]+r[:-1])/2;ut=r*v[mask];u=r*c[mask];out=(ut[1:]+ut[:-1])/2-m.c*np.diff(u)/h;ret=t-re/m.c*m.tdyn;actual=out/2;prediction=np.zeros_like(actual)
for i,ri in enumerate(m.r[:n]):
 sp=CubicSpline(times,src[:,i]);plus=ret+ri/m.c*m.tdyn;minus=ret-ri/m.c*m.tdyn
 val=lambda z:np.where((z>=times[0])&(z<=times[-1]),sp(z),0.)
 prediction-=(val(plus)-val(minus))/(2*m.c*ri)
valid=(ret>.1)&(ret<t-500/(m.c*m.rm/m.tdyn)-.1);pred_err=float(np.linalg.norm(prediction[valid]-actual[valid])/np.linalg.norm(actual[valid]));bins=[]
for lo in np.arange(0,np.floor(np.max(ret)/2)*2,2):
 hi=lo+2;sel=(ret>=lo)&(ret<hi);bins.append({'retarded_interval_Myr':[float(lo),float(hi)],'outgoing_energy_Eunit':float(h/4*np.sum(out[sel]**2)),'mean_power_Eunit_Myr':float(h/4*np.sum(out[sel]**2)/2)})
def enclosed(z,R):
 mass=np.sum(abs(z[0])**2,axis=0);return float(np.interp(R,m.r*m.rm,m.enclosed(mass)*m.r**2))
R=50/m.rm;gb=R/(R*R+m.b*m.b)**1.5;law=(gb+np.sqrt(gb*gb+4*gb))/2;req=R*R*(law-gb);M0=enclosed(initial,50);Mf=enclosed(state,50);f=field(m,state);md=2*np.real(np.conj(a)*f[0]);Mdot=float(np.interp(50,m.r*m.rm,m.enclosed(np.sum(md,axis=0))*m.r**2)/m.tdyn)
fd=m.diagnostics(a,x,c,v);rr=m.r*m.rm;rho=np.sum(abs(a)**2,axis=0)/m.vol;sel=(rr>15)&(rr<1.2*fd['boundary_kpc']);nr=rr[sel];nrho=rho[sel];rebound=nrho/np.minimum.accumulate(nrho);i=int(np.argmax(rebound));j=int(np.argmin(nrho[:i+1]));probe=json.loads((base/'run_probe_evolve/results.json').read_text());fine=json.loads((base/'run_probe_evolve_refined/results.json').read_text());local=json.loads((base/'run_probe_final/results.json').read_text())
comparison=json.loads((base/'run_continue_comparison/results.json').read_text());large=runs[-1];common=min(comparison['completed_time_Myr'],large['completed_time_Myr']);checks={}
for key in ['law_error_percent','boundary_kpc','density_rebound','wave_energy','outer_T_fraction']:
 interp=lambda d:float(np.interp(common,[r['time_Myr'] for r in d['trace']],[r[key] for r in d['trace']]))
 checks[key]={'large_ceiling_run':interp(large),'comparison_run':interp(comparison),'difference':interp(large)-interp(comparison)}
res={'original_joint_goal_passed':False,'original_joint_goal_status':'OPEN','authoritative_chain':[str(x) for x in chain],'actual_final_time_Myr':t,'final_joint':fd,'global_energy_defect':float(m.full_energy(*state)+offset['escaped_energy']-runs[0]['initial_energy']),'global_charge_defect':float(m.charge(a,v)-m.charge(initial[0],initial[4])),'global_mass_defect':float(np.sum(abs(a)**2)-np.sum(abs(initial[0])**2)),'radiation':rad,'cumulative_work':offset,'outgoing_over_net_field_work':rad['outgoing_characteristic_energy']/offset['net_material_to_wave_work'],'retarded_emission_bins':bins,'final_waveform_source_prediction_relative_L2':pred_err,'mass_redistribution':{'initial_enclosed_50_Mb':M0,'final_enclosed_50_Mb':Mf,'law_required_enclosed_50_Mb':req,'inward_gain_50_Mb':Mf-M0,'initial_missing_mass_50_Mb':req-M0,'fraction_initial_deficit_repaired':(Mf-M0)/(req-M0),'final_inward_rate_50_Mb_Myr':Mdot},'density_trough':{'trough_radius_kpc':float(nr[j]),'subsequent_rebound_radius_kpc':float(nr[i]),'trough_density':float(nrho[j]),'rebound_ratio':float(rebound[i]),'interpretation':'Populated transition, but growing nonmonotonic density trough; do not report monotonic gap-free formation.'},'moving_boundary':{'early_probe_time_Myr':5.7,'response_endpoint_Myr':fine['common_endpoint_Myr'],'odd_response_ratio_coarse':probe['odd_response_ratio_final'],'odd_response_ratio_refined':fine['odd_response_ratio_final'],'max_curve_difference_kpc':max(abs(a['odd_displacement_kpc']-b['odd_displacement_kpc']) for a,b in zip(probe['response'],fine['response'])),'final_state_probe_time_Myr':local['base_time_Myr'],'final_state_omega2_01_Myr-2':local['omega2_0.01_Myr-2'],'final_state_omega2_005_Myr-2':local['omega2_0.005_Myr-2'],'non_claim':'One short family returns/overshoots early; final-state local acceleration is restoring. No asymptotic or arbitrary perturbation stability proof.'},'adaptive_ceiling_comparison':{'common_time_Myr':common,'observables':checks,'non_claim':'Both guarded runs shrink their steps; this is not uniform fixed-step halving or proof of a production speedup.'},'per_run_numerics':[{'path':str(root),**{k:d[k] for k in ['status','completed_time_Myr','accepted_steps','rejected_steps','max_absolute_energy_error','max_charge_error','max_mass_error','max_root_error']}} for root,d in zip(chain,runs)],'interpretation':'Continued radiation and inward transfer coexist, but only a tiny mass-deficit fraction is repaired and the law fails. Populated transition develops a trough; local moving-boundary restoration survives; exterior remains effectively F in this finite window.'}
np.savez_compressed(dest.with_name('evidence_arrays.npz'),time_Myr=np.array([r['time_Myr'] for r in tr]),law_error_percent=np.array([r['law_error_percent'] for r in tr]),wave_energy=np.array([r['wave_energy'] for r in tr]),field_work=np.array([r['net_material_to_wave_work'] for r in tr]),far_flux=np.array([r['far_net_flux'] for r in tr]),retarded_time_Myr=ret,actual_outgoing=actual,source_prediction=prediction,source_time_Myr=times,source_monopole=I)
dest.write_text(json.dumps(res,indent=2)+'\n');print({k:res[k] for k in ['actual_final_time_Myr','global_energy_defect','global_charge_defect','mass_redistribution','moving_boundary','final_waveform_source_prediction_relative_L2']})
assert abs(res['global_energy_defect'])<1e-7 and rad['incoming_fraction']<1e-3
assert res['final_joint']['law_error_percent']>17 and not res['original_joint_goal_passed']
assert pred_err<.05
