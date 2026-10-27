import argparse,json
from pathlib import Path
import numpy as np
from live_collocated import Collocated
from radiative_modes_final import decompose
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();m=Collocated(eta=.01,material_h_kpc=.125,wave_R_kpc=10000.);base=Path('infall_pump_2026_10_25');early=json.loads((base/'run_quiet_time/results.json').read_text());rows=[]
for name in ['run_quiet_long','run_quiet_long_time']:
 root=base/name;s=np.load(root/'state.npz');data=json.loads((root/'results.json').read_text());t=data['completed_time_Myr'];tr=data['trace'];times=np.array([z['time_Myr'] for z in tr]);flux=np.array([z['far_net_flux'] for z in tr])+early['trace'][-1]['far_net_flux'];bulk=np.array([z['bulk_current_work'] for z in tr])+early['trace'][-1]['bulk_current_work'];upper=min(9000.,m.c*m.rm/m.tdyn*t+500.)
 d=decompose(m.wr,s['chi'],s['pi'],m.c,m.tdyn,500/m.rm,upper/m.rm);idx=np.flatnonzero(flux>=.9*flux[-1]);t90=float(times[idx[0]]) if len(idx) else None
 rows.append({'run':name,'time_Myr':t,'last':tr[-1],'global_net500_flux':float(flux[-1]),'global_bulk_work':float(bulk[-1]),'time_first90percent_final_net_flux_Myr':t90,'detector_light_delay_Myr':float(500/(m.c*m.rm/m.tdyn)),'decomposition':d,'scope':'The90percent time uses finite-radius net flux, including a reactive contribution. Work must be compared with retarded source time, not the same observation time.'})
common=min(z['time_Myr'] for z in rows);comparisons={}
for name in ['wave_energy','far_net_flux','bulk_current_work','law_error_percent','boundary_kpc','outer_T_fraction','transition_min_density']:
 vals=[]
 for run in ['run_quiet_long','run_quiet_long_time']:
  d=json.loads((base/run/'results.json').read_text());vals.append(float(np.interp(common,[z['time_Myr'] for z in d['trace']],[z.get(name,0.) for z in d['trace']])))
 comparisons[name]={'interpolated_values':vals,'absolute_difference':abs(vals[1]-vals[0])}
Path(args.output).write_text(json.dumps({'cases':rows,'common_time_Myr':common,'selected_time_ceiling_comparison':comparisons,'comparison_limit':'Unequal adaptive histories and.1Myr samples; endpoint interpolation is not a high-frequency phase convergence certificate.'},indent=2)+'\n');print(json.dumps(rows,indent=2))
