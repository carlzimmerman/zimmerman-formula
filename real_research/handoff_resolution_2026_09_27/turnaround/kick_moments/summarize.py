from pathlib import Path
import json,hashlib
import numpy as np
p=Path(__file__).resolve().parent;j=json.loads((p/'results.json').read_text());runs=j['runs'];rg=np.array(j['rgrid_kpc'])
def get(foot,cad,N,eta,shift=0.):
 return runs[f'{foot}/cadence{cad}/N{N}/eta{eta}/shift{shift}']
def compare(a,b):
 ra=np.array(a['Md']);rb=np.array(b['Md']);mask=(rg>=5)&(rg<=min(a['r200'],b['r200']))
 return {'h_fractional_change':b['hmax']/a['hmax']-1,'conversion_fraction_change':b['conversion_fraction']/a['conversion_fraction']-1,'converted_mass_fractional_change':b['budget']['converted']/a['budget']['converted']-1,'escaped_mass_fractional_change':b['budget']['escaped']/a['budget']['escaped']-1,'profile_max_relative_5kpc_to_minr200':float(np.max(abs(rb[mask]-ra[mask])/np.maximum(ra[mask],1e8)))}
cm={}
for foot in sorted(set(v['foot'] for v in runs.values())):
 for cad in [5,1]:
  cm[f'{foot}/cadence{cad}/tinyP']=compare(get(foot,cad,600,.03),get(foot,cad,600,.03,1e-7))
  for N in [600,1000,2000]:cm[f'{foot}/cadence{cad}/halfstep{N}']=compare(get(foot,cad,N,.03),get(foot,cad,N,.015))
  for eta in [.03,.015]:
   cm[f'{foot}/cadence{cad}/N1000to2000_eta{eta}']=compare(get(foot,cad,1000,eta),get(foot,cad,2000,eta))
 for N in [600,1000,2000]:
  for eta in [.03,.015]:cm[f'{foot}/cadence5to1/N{N}_eta{eta}']=compare(get(foot,5,N,eta),get(foot,1,N,eta))
col=p.parents[1]/'collapse';prior=json.loads((col/'matched_results.json').read_text())['runs']
for N in [600,1000,2000]:
 a=prior['refresh_after_events/'+str(N)];b=get('canonical',5,N,.03)
 assert a['initial_profile_sha256']==b['initial_profile_sha256']
 cm[f'canonical/random64toexact/N{N}']=compare(a,b)
assert prior['refresh_after_events/600_tiny_spectrum_shift']['initial_profile_sha256']==get('canonical',5,600,.03,1e-7)['initial_profile_sha256']
source=col/'engine_constant_j_force_refresh.py';pin=json.loads((p/'clone_provenance.json').read_text())['source_sha256'];assert hashlib.sha256(source.read_bytes()).hexdigest()==pin
(p/'comparisons.json').write_text(json.dumps(cm,indent=2))
lines=['| Footing | Cadence | N | eta | power shift | hmax | converted / final dark M200 |','|---|---:|---:|---:|---:|---:|---:|']
for v in runs.values():lines.append(f"| {v['foot']} | {v['cadence']} | {v['N']} | {v['eta']} | {v['power_shift']} | {v['hmax']:.9f} | {v['conversion_fraction']:.9f} |")
(p/'TABLE.md').write_text('\n'.join(lines)+'\n')
print('runtime',j['runtime_seconds'],'runs',len(runs),'original_source_unchanged',True)
for name,m in cm.items():print(name,'h%',round(m['h_fractional_change']*100,4),'converted%',round(m['converted_mass_fractional_change']*100,4),'fc%',round(m['conversion_fraction_change']*100,4))
