import argparse,json
from pathlib import Path
import numpy as np
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();p=Path('nonlinear_cascade_2026_10_25');full=json.loads((p/'run_probe_finer/results.json').read_text());half=json.loads((p/'run_probe_finer_half/results.json').read_text());coarse=json.loads((p/'run_probe_infall/results.json').read_text());keys=['law_error_percent','boundary_kpc','density_rebound','far_flux_energy','wave_energy','kinetic_energy'];rows=[]
for name,left in [('time_halving_same_fine_grid',half),('material_h_halving',coarse)]:
 t=left['completed_time_Myr'];tf=np.array([r['time_Myr'] for r in full['trace']]);a={k:float(np.interp(t,tf,[r[k] for r in full['trace']])) for k in keys};b={k:float(left['trace'][-1][k]) for k in keys};rows.append({'comparison':name,'time_Myr':t,'reference_interpolation':a,'other_last_sample':b,'absolute_differences':{k:abs(a[k]-b[k]) for k in keys},'qualification':'Compare actual sampled time, with linear interpolation of reference trace; not full convergence of unresolved fast carrier spectrum.'})
out={'comparisons':rows,'scope':'Selected global-observable convergence checks within overlapping completed times; no late-time or full spectral certificate.'};Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(out)
