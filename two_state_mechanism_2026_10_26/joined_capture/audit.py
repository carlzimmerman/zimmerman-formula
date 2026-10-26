import json,argparse,hashlib
from pathlib import Path
import numpy as np
p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();b=Path(__file__).resolve().parent
labels=['fourth_h10','fourth_h05','fourth_h025','fourth_h0125','wall_h05','wall_h025','wall_h0125','inner01','inner005','outer40','ry3_h05','ry3_h025','ry4_h025']
table=[]
for label in labels:
 d=json.loads((b/('run_'+label)/'results.json').read_text())
 for r in d['rows']:
  assert r['unitarity_error']<1e-7 and r['reciprocity_error']<1e-7
  table.append(dict(run=label,**d['settings'],energy=r['energy'],probability=r['ground_to_other'],unitarity=r['unitarity_error'],reciprocity=r['reciprocity_error']))
m=json.loads((b/'run_map/results.json').read_text());assert len(m['rows'])==27
maps={k:max(r[k] for r in m['rows']) for k in ['H_max_error','embedded_H_max_error','isometry_error','optical_error']}
nonlocal_rows=json.loads((b/'run_nonlocal_v2/results.json').read_text())['rows']
assert [r['open_vibrational_modes'] for r in nonlocal_rows]==[1,2]
assert all(r['maximum_open_relative_error']<1e-12 and r['maximum_closed_absolute_error']<1e-12 for r in nonlocal_rows)
# Verify copied orbital files against the original recorded scattering inputs.
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for R in [2,3,4]:
 src=b.parent/'continuum/run_physical_radial25/h2+.molden' if R==2 else b.parent/'nuclear_flux'/('run_capture_R%d'%R)/'h2+.molden'
 assert sha(src)==sha(b/'inputs'/('R%d_h2+.molden'%R))
artifacts=[dict(path=str(p.relative_to(b)),sha256=sha(p),size=p.stat().st_size) for p in sorted(b.glob('run_*/*.npz'))]
Path(a.output).write_text(json.dumps(dict(map_checks=maps,nuclear_table=table,nonlocal_rows=nonlocal_rows,operator_checks=json.loads((b/'run_checks/results.json').read_text()),auxiliary_arrays=artifacts,physical_DR_rates_derived=False,new_physical_photon_runs=0,galaxy_separation_established=False),indent=2)+'\n')
print(json.dumps(maps),flush=True)
