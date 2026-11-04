"""Cumulative FRW residual compared with actual retained orbital excitation."""
import sys,json,time,resource,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[3]
for path in ('cascades','integration'):sys.path.insert(0,str(ROOT/'reviews/collision_completion_2026_11_04'/path))
from consistent_background import ConsistentVertexBackground
from generic_orbit import GenericOrbit

def main(out):
 start=time.monotonic();base=ROOT/'reviews/collision_completion_2026_11_04';paths=dict(shared_prefix=base/'integration/run_fresh_exact002/result.json',larger_steps=base/'history/run_advance002/result.json',refined=base/'history/run_refine002/result.json',direct_control=base/'history/run_direct001/result.json');bg=ConsistentVertexBackground(base/'cascades/run_vertices001/result.json');rows={}
 for name,path in paths.items():
  r=json.loads(path.read_text());s=r['state'];case=r.get('case',r);q=np.array(case['q']);W=np.array(case['W']);h=case['history'][-1];J=s.get('J',h['action']);model=GenericOrbit(bg,q,W,8);model.J0=s['J0'];model.last_x=s['xmid'];orb=model.orbit(s['N'],np.array(s['Y']),J=J);error=s['E']+s['independent_work']-s['energy_reference_E'];excitation=s['E']-orb['minimum'];rows[name]=dict(path=str(path.relative_to(ROOT)),N=s['N'],energy_reference=s['energy_reference_E'],cumulative_independent_work=s['independent_work'],stored_energy=s['E'],reconstructed_energy=orb['E'],reconstruction_difference=s['E']-orb['E'],potential_minimum=orb['minimum'],orbital_excitation=excitation,harmonic_omega_J=orb['omega']*J,gas_normalization=s['gas0'],cumulative_error=error,error_over_gas=error/s['gas0'],error_over_excitation=error/excitation,absolute_error_fraction_of_excitation=abs(error/excitation))
 for name in ('larger_steps','refined','direct_control'):
  rows[name]['error_increment_after_shared_prefix']=rows[name]['cumulative_error']-rows['shared_prefix']['cumulative_error'];rows[name]['increment_over_endpoint_excitation']=rows[name]['error_increment_after_shared_prefix']/rows[name]['orbital_excitation'];rows[name]['inherited_prefix_error_over_endpoint_excitation']=rows['shared_prefix']['cumulative_error']/rows[name]['orbital_excitation']
 direct=json.loads(paths['direct_control'].read_text());checks=dict(common_reference=max(r['energy_reference'] for r in rows.values())-min(r['energy_reference'] for r in rows.values())<1e-24,common_gas_normalization=max(r['gas_normalization'] for r in rows.values())-min(r['gas_normalization'] for r in rows.values())<1e-24,positive_excitation=all(r['orbital_excitation']>0 for r in rows.values()),target_N_equal=abs(rows['larger_steps']['N']-rows['refined']['N'])<1e-13)
 result=dict(claim_id='CC10_CUMULATIVE_WORK_EXCITATION_AUDIT',rows=rows,checks={k:bool(v) for k,v in checks.items()},preferred_checkpoint='history/run_refine002/result.json',preference_reason='Smaller maximum time step after the same shared prefix, not because its cumulative energy residual is smaller.',direct_control=dict(source='history/run_advance002/result.json',steps=direct['steps_per_period'],periods=1,max_local_relative_work_error=max(abs(h['energy_ledger_error']) for h in direct['history']),initial_action=direct['history'][0]['action'],final_action=direct['history'][-1]['action'],charged_ratio=direct['history'][-1]['charged_fraction']),runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Independent cumulative FRW quadrature is normalized against gas and actual orbital excitation. Shared-prefix error remains. The direct control preserves inherited work but tests local evolution from the larger-step endpoint; it does not repair or independently control the refined history.')
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(result['checks'])
 for name,row in rows.items():print(name,row['error_over_gas'],row['absolute_error_fraction_of_excitation'])
 assert all(result['checks'].values()),result['checks']
if __name__=='__main__':main(sys.argv[1])
