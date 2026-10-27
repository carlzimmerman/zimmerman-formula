import argparse,json
from pathlib import Path
import numpy as np
from live_collocated import Collocated
from radiative_modes import decompose
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();m=Collocated(eta=.01,material_h_kpc=.125,wave_R_kpc=10000.);rows=[]
for name in ['run_components_time','run_quiet_time','run_constant_current_control','run_rest_checked','run_restart_checked']:
 root=Path('infall_pump_2026_10_25')/name;s=np.load(root/'state.npz');data=json.loads((root/'results.json').read_text());time=data['completed_time_Myr'];upper=min(9000.,m.c*m.rm/m.tdyn*time+500.)
 row={'run':name,'time_Myr':time,'scope':'Source-free far annulus, static1/r energy separated. Windowed spectrum is finite-window proxy, especially poorly resolved below1rad/Myr.','decomposition':decompose(m.wr,s['chi'],s['pi'],m.c,m.tdyn,500/m.rm,upper/m.rm)};rows.append(row)
Path(args.output).write_text(json.dumps({'cases':rows},indent=2)+'\n');print(json.dumps(rows,indent=2))
