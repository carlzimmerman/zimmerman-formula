"""Complete energy budget and actual outgoing pulse for the smooth quiet test."""
import argparse,json,sys
from pathlib import Path
import numpy as np
from live_collocated import Collocated
from radiative_modes_final import decompose
sys.path.insert(0,'nonlinear_cascade_2026_10_25')
from fine_cc_run import components
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();base=Path('infall_pump_2026_10_25');m=Collocated(eta=.01,material_h_kpc=.125,wave_R_kpc=10000.);run=json.loads((base/'run_smooth_infall/results.json').read_text());states=[np.load(base/'run_smooth_prepare/state.npz'),np.load(base/'run_smooth_infall/state.npz')];energies=[]
for s in states:
 a,x,p,c,v=[s[k] for k in ['a','alpha','carrier_p','chi','pi']];m.energy_chi=c;d=components(m,a,x,p,c,v);d['scalar_field_energy']=m.diagnostics(a,x,c,v)['wave_energy'];d['full_energy']=m.full_energy(a,x,p,c,v)
 keys=[k for k in d if k.endswith('_energy') and k!='full_energy'];d['component_closure_error']=sum(d[k] for k in keys)-d['full_energy'];energies.append(d)
s=states[-1];t=run['completed_time_Myr'];upper=min(9000.,m.c*m.rm/m.tdyn*t+500.);rad=decompose(m.wr,s['chi'],s['pi'],m.c,m.tdyn,500/m.rm,upper/m.rm)
mask=(m.wr>=500/m.rm)&(m.wr<=upper/m.rm);r=m.wr[mask];u=r*s['chi'][mask];ut=r*s['pi'][mask];h=float(np.mean(np.diff(r)));wout=(ut[1:]+ut[:-1])/2-m.c*np.diff(u)/h;rm=(r[1:]+r[:-1])/2;weight=wout*wout;den=np.sum(weight);meanr=float(weight@rm/den);sigmat=float(np.sqrt(weight@((rm-meanr)**2)/den)/m.c*m.tdyn);rmsomega=float(m.c/m.tdyn*np.sqrt(np.sum(np.diff(wout)**2/h**2)/np.sum(weight)))
early_final=run['trace'][-1];out={'physical_time_Myr':t,'initial_preparation_not_radiation':json.loads((base/'run_smooth_prepare/results.json').read_text())['preparation_energy_change_not_radiation'],'initial_components':energies[0],'final_components':energies[1],'component_changes':{k:energies[1][k]-energies[0][k] for k in energies[0] if k.endswith('_energy')},'radiative_decomposition':rad,'outgoing_energy_over_field_work':rad['outgoing_characteristic_energy']/early_final['net_material_to_wave_work'],'outgoing_packet_rms_frequency_rad_Myr':rmsomega,'outgoing_packet_energy_weighted_duration_Myr':sigmat,'packet_edge_amplitude_fraction':float(max(weight[0],weight[-1])/max(weight)),'joint_metrics':{k:early_final[k] for k in ['law_error_percent','boundary_kpc','density_rebound','transition_min_density','outer_T_fraction','mass','cap_slack']},'interpretation':'Real outgoing radial pulse from initially zero wave fields, internally quiet C4 density; packet RMS is a finite-annulus frequency moment, not coherent material-mode occupation or proof of a sustained cascade. No live boundary-restoration experiment is inferred from finite radius.'};Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(out)
assert all(abs(d['component_closure_error'])<1e-10 for d in energies)
assert rad['incoming_fraction']<1e-3 and abs(rad['decomposition_identity_error'])<1e-12
