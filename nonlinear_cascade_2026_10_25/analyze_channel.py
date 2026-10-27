"""Check actual outgoing field spectra; more daughter energy need not cool more."""
import argparse,json
from pathlib import Path
import numpy as np
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();p=Path('nonlinear_cascade_2026_10_25');rows=[]
for name in ['wave_time','wave_grid','wave_omit','wave_zero','wave_no_daughter']:
 d=json.loads((p/('run_'+name)/'results.json').read_text());h=np.load(p/('run_'+name)/'detector.npz');x=h['data'];t=x[:,0];dt=float(np.median(np.diff(t)));assert max(abs(np.diff(t)-dt))<1e-7;pi=x[:,2];c=float(h['c']);rad=float(h['radius']);tdyn=float(h['tdyn']);freq=2*np.pi*np.fft.rfftfreq(len(t),d=dt);bands=[]
 for power in [2,4]:
  window=np.sin(np.pi*(np.arange(len(t))+.5)/len(t))**power;P=np.fft.rfft(pi*window);mult=np.ones(len(P))*2;mult[0]=1
  if len(t)%2==0:mult[-1]=1
  E=dt/tdyn/len(t)*c*rad*rad*mult*abs(P)**2;total=float(sum(E));parent=2*d['frequencies_per_Myr'][0];daughter=2*d['frequencies_per_Myr'][2];bp=(freq>.8*parent)&(freq<1.2*parent);bd=(freq>.8*daughter)&(freq<1.2*daughter);bands.append({'window_power':power,'total_radiation_component_proxy_over_initial_energy':total/d['initial_material_energy_Eunit'],'parent_band_fraction':float(sum(E[bp])/total) if total else 0.,'daughter_band_fraction':float(sum(E[bd])/total) if total else 0.,'daughter_band_energy_over_initial':float(sum(E[bd])/d['initial_material_energy_Eunit'])})
 rows.append({'run':name,'completed_time_Myr':d['completed_time_Myr'],'sponge_escaped_fraction':d['escaped_fraction'],'max_daughter_material_fraction':d['max_daughter_energy_fraction'],'spectral_estimates':bands})
out={'rows':rows,'scope':'Actual radial scalar detector signal, windowed c*r²*pi² radiation-component spectrum conditional on outgoing propagation outside source. Not identical to finite-radius total energy flux (which also has boundary storage), nor sponge loss with different arrival time. Bands surround bare pair frequencies with20% allowance; no all-energy causal attribution to cascade.'};Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(out)
