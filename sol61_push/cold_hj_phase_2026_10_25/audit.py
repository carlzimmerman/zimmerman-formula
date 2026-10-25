import pathlib,json,hashlib,sys,numpy as np
P=pathlib.Path(__file__).resolve().parent;ROOT=P.parents[1];checks=[];count=0

def check(name,value):
 checks.append(dict(name=name,passed=bool(value)));assert value,name
for packet in (P.parent/'cold_lens_phase_2026_10_25',P):
 for f in sorted((packet/'runs').glob('*.json')):
  count+=1;d=json.loads(f.read_text());check(f.stem+' immutable inputs',d['inputs_before']==d['inputs_after'])
  for path,h in d['inputs_after'].items():check(f.stem+' pin '+path,hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==h)
  a=np.load(f.with_suffix('.npz'));m=abs(a['u'])**2;q=a['q'];last=d['history'][-1];init=d['history'][0]
  check(f.stem+' saved subset',q.min()>-1e-10 and np.max(q-m)<1e-10)
  check(f.stem+' saved matches history',abs(m.sum()-last['M'])<1e-10 and abs(q.sum()-last['tag_mass'])<1e-10 and abs(a['times'][-1]-last['t'])<1e-12)
  check(f.stem+' global mass and tag',all(abs(h['M']-init['M'])<1e-10 and abs(h['tag_mass']-init['tag_mass'])<1e-10 for h in d['history']))
  check(f.stem+' aperture subset',all(h['tag_aperture_Msun']<=h['field_aperture_Msun']+1e-5 for h in d['history']))
  check(f.stem+' bond continuity',d['bond_residual']<1e-10)
  check(f.stem+' measured RSS',d['peak_RSS_bytes']<1_000_000_000)
  if 'initial_gauge_energy_identity_residual' in d:check(f.stem+' initial lens invariant energy',abs(d['initial_gauge_energy_identity_residual'])<1e-10)
  else:check(f.stem+' physical drift accounted by gauge defect',all(abs(h['E_relative_error']-h['gauge_signed_relative'])<1e-4 for h in d['history']))
# The dtype repair must not change complex-input physics in the original pilot.
a=np.load(P/'runs/draco_HJ_N64.npz');b=np.load(P/'runs/draco_HJ_v2_N64.npz')
check('original/v2 complex input equivalence',np.linalg.norm(a['u']-b['u'])<1e-11 and np.max(abs(a['q']-b['q']))<1e-12)
# Converged analytic checks, not every coarse benchmark passes physical energy gate.
L=json.loads((P.parent/'cold_lens_phase_2026_10_25/benchmark_refined.json').read_text())['cases'];H=json.loads((P/'benchmark_refined.json').read_text());C=json.loads((P/'conservation_verified.json').read_text())
check('lens finest analytic energy',abs(L[5]['relative_energy_drift'])<.01);check('adaptive finest analytic energy',abs(H['wave_cases'][4]['physical_energy_drift'])<.01)
check('HJ reference refinement',H['HJ_cases'][2]['max_error']<H['HJ_cases'][1]['max_error']<H['HJ_cases'][0]['max_error'])
check('Fisher identity',C['symbolic_partition_residual']=='0' and C['partition_gradient_error']<1e-12)
check('once-counted gravity and mutation',C['gravity_cross_energy_error']<1e-12 and C['double_counted_cross_energy_error']>1e-4)
check('exact discrete gauge',C['gauge_wave_error']<1e-12 and C['gauge_tag_error']<1e-12 and C['gauge_energy_error']<1e-12)
check('Noether local conservation',C['local_polynomial_energy_residual']=='0' and all(x=='0' for x in C['local_polynomial_momentum_residuals']) and C['symmetric_stress'])
result=dict(case_count=count,checks=checks,interpretation='finite identities and numerical failures verified; no four-dwarf physical closure')
pathlib.Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(count,'cases',len(checks),'checks passed')
