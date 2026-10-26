import json,math
from pathlib import Path
p=Path(__file__).resolve().parent
f=json.load(open(p/'floquet/result.json'));units=json.load(open(p.parent/'cold_real_field_2026_10_25/run/result.json'));rows=[]
wave=json.load(open(p.parent/'cold_wave_relaxation_2026_10_25/run/result.json'))['rows'];speed={(r['name'],r['model'],r['footing'],r['shell']):r['sigma_kms'] for r in wave if r['sigma_factor']==1}
for r in json.load(open(p/'lattice/result.json'))['rows']:
 b=f['rows'][r['index']];m=math.sqrt((r['d']-8)/4);v2=(speed[(b['name'],b['model'],b['footing'],b['shell'])]/299792.458)**2
 rows.append(dict(name=r['name'],time_days=40/m*units['time_unit_years']*365.25,box_pc=2*math.pi/r['k_over_m']/m*units['length_unit_pc'],pressure_over_gravity_proxy=r['late_P_over_E']/v2,excitation_compactness_scale=units['kappa']*r['target_E']*(2*math.pi/r['k_over_m']/m)**2))
(p/'physical_scales.json').write_text(json.dumps(rows,indent=2)+'\n')
