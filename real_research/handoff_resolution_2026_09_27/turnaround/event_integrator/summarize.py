from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent;j=json.loads((p/'results.json').read_text());r=j['runs'];prior=json.loads((p.parent/'kick_moments/results.json').read_text())['runs']
def row(foot,N,eta,shift=0.):return r[f'{foot}/N{N}/eta{eta}/shift{shift}']
def cmp(a,b):return {'h_fractional_change':b['hmax']/a['hmax']-1,'converted_mass_fractional_change':(b['budget']['converted']/a['budget']['converted']-1) if a['budget']['converted'] else None,'conversion_fraction_change':(b['conversion_fraction']/a['conversion_fraction']-1) if a['conversion_fraction'] else None}
comparisons={}
for foot in ['canonical','alt']:
 for N in [600,1000]:
  if all(f'{foot}/N{N}/eta{eta}/shift0.0' in r and row(foot,N,eta)['complete'] for eta in [.03,.015]):comparisons[f'{foot}/halfstep{N}']=cmp(row(foot,N,.03),row(foot,N,.015))
 if all(f'{foot}/N600/eta0.03/shift{s}' in r and row(foot,600,.03,s)['complete'] for s in [0.,1e-7]):comparisons[f'{foot}/tinyP']=cmp(row(foot,600,.03),row(foot,600,.03,1e-7))
 for N in [600,1000]:
  for eta in [.03,.015]:
   key=f'{foot}/N{N}/eta{eta}/shift0.0'
   if key in r and r[key]['complete']:
    old=prior[f'{foot}/cadence1/N{N}/eta{eta}/shift0.0'];assert old['initial_profile_sha256']==r[key]['initial_profile_sha256'];comparisons[f'{foot}/endpoint_to_events/N{N}/eta{eta}']=cmp(old,r[key])
checks={'all_requested_cases_completed':len(r)==12 and all(v['complete'] for v in r.values()),'mass_accounting':all(abs(v['mass_accounting_relative'])<1e-12 for v in r.values() if v['complete']),'time_brackets':all(v['max_bracket_relative_width']<=1.00001e-6 for v in r.values() if v['complete']),'phase_residual_below_1e-5_km_s':all(v['max_phase_velocity_residual']<1e-5 for v in r.values() if v['complete']),'pressure_residual_below_1e-3_cap':all(v['max_pressure_relative_excess']<1e-3 for v in r.values() if v['complete'])}
checks['original_exact_engine_unchanged']=hashlib.sha256((p.parent/'kick_moments/engine_exact.py').read_bytes()).hexdigest()==json.loads((p/'provenance.json').read_text())['source_sha256']
(p/'comparisons.json').write_text(json.dumps({'checks':checks,'comparisons':comparisons},indent=2));print(json.dumps({'checks':checks,'comparisons':comparisons},indent=2))
lines=['| Footing | N | eta | P shift | hmax | converted/final dark M200 | phase residual km/s | pressure excess/Pcap |','|---|---:|---:|---:|---:|---:|---:|---:|']
for v in r.values():
 if v['complete']:lines.append(f"| {v['foot']} | {v['N']} | {v['eta']} | {v['power_shift']} | {v['hmax']:.9f} | {v['conversion_fraction']:.9f} | {v['max_phase_velocity_residual']:.6g} | {v['max_pressure_relative_excess']:.6g} |")
 else:lines.append(f"| {v['foot']} | {v['N']} | {v['eta']} | {v['power_shift']} | incomplete: {v['error']} | | | |")
(p/'TABLE.md').write_text('\n'.join(lines)+'\n')
