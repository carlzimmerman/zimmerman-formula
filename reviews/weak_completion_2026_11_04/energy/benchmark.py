"""Read-only consolidation of completed fresh matched-energy ancestries."""
from pathlib import Path
import json,math,sys,time,resource,csv
ROOT=Path(__file__).resolve().parents[3]
INITIAL=Path('reviews/collision_completion_2026_11_04/integration/run_initial001/result.json')
OLD_LEDGER=Path('reviews/collision_completion_2026_11_04/history/run_ledger001/result.json')

def ancestry(path):
 path=Path(path);chain=[];seen=set()
 while path!=INITIAL:
  if str(path) in seen:raise RuntimeError('cyclic ancestry')
  seen.add(str(path));d=json.loads((ROOT/path).read_text());chain.append((path,d));path=Path(d['state']['ancestry_checkpoint'])
 chain.reverse();return chain

def main(out,coarse_path,fine_path):
 start=time.monotonic();initial=json.loads((ROOT/INITIAL).read_text());groups=initial['case']['groups'];q=initial['case']['q'];n=len(q);u1=groups.index('F1_1');branches={};curves={};checks={}
 for label,path in [('coarse',coarse_path),('fine',fine_path)]:
  chain=ancestry(path);d=chain[-1][1];state=d['state'];last=d['case']['history'][-1];rows={}
  for p,segment in chain:
   if not all(segment['checks'][k] for k in ['positive','Pauli','entropy','independent_energy_work']):raise RuntimeError('failed prefix invariant')
   for h in segment['case']['history']:rows[round(h['N'],14)]=h
  values=sorted(rows.values(),key=lambda h:h['N']);curves[label]=values;Y=state['Y'];nums=[sum(Y[i*n:(i+1)*n]) for i in range(len(groups))];photino=Y[u1*n:(u1+1)*n];t=.004657258204883617*math.exp(-state['N']);conversion=45*.02**3/(2*math.pi**2*106.75)
  branches[label]=dict(path=str(path),ancestry=[str(p) for p,d in chain],completed=d['checks']['target_reached'],N=state['N'],J=state['J'],orbital_excitation=last['orbital_excitation'],energy=state['E'],independent_work=state['matched_independent_work'],initial_energy=state['matched_initial_energy'],global_energy_work_residual=state['E']+state['matched_independent_work']-state['matched_initial_energy'],global_energy_work_residual_over_excitation=last['energy_work_residual_over_excitation'],maximum_error_over_excitation=d['case']['max_energy_error_over_excitation'],Y_charged=last['Y_charged'],Y_U1=nums[u1]*conversion,U1_mean_p_over_mu=sum(v*t*p for v,p in zip(photino,q))/nums[u1],initial_J=state['J0'],group_numbers=nums,final_numbers=Y)
 a=branches['coarse'];b=branches['fine'];comparison={k:b[k]/a[k]-1 for k in ['J','Y_charged','Y_U1','U1_mean_p_over_mu','orbital_excitation']};comparison['relative_number_L1']=sum(abs(x-y) for x,y in zip(a['final_numbers'],b['final_numbers']))/sum(abs(x) for x in b['final_numbers']);old=json.loads((ROOT/OLD_LEDGER).read_text())['rows']['refined'];checks.update(both_fresh_target=all(v['completed'] for v in branches.values()) and abs(a['N']-b['N'])<1e-13,initial_energy_identical=a['initial_energy']==b['initial_energy'],energy_excitation_threshold=max(v['maximum_error_over_excitation'] for v in branches.values())<.01,retained_positive_actions=min(v['J'] for v in branches.values())>0)
 common=[];fine_by={round(h['N'],12):h for h in curves['fine']}
 for h in curves['coarse']:
  if round(h['N'],12) in fine_by:
   f=fine_by[round(h['N'],12)];common.append(dict(N=h['N'],coarse_J=h['action'],fine_J=f['action'],relative_J=f['action']/h['action']-1,coarse_energy_error=h['energy_work_residual_over_excitation'],fine_energy_error=f['energy_work_residual_over_excitation']))
 result=dict(claim_id='CC11_FRESH_ENERGY_BENCHMARK',checks=checks,branches=branches,coarse_to_fine_relative_changes=comparison,common_N_comparison=common,old_preferred_error_over_excitation=old['absolute_error_fraction_of_excitation'],improvement_factors={k:old['absolute_error_fraction_of_excitation']/abs(v['global_energy_work_residual_over_excitation']) for k,v in branches.items()},scope='Completedfresh25groupenergybenchmark. Ledgerconvergence andstateprecisionreportedseparately; BEstateerrorisnotdeclaredbelow1percent. NocoldDM/candidateclaim.',runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 Path(out).write_text(json.dumps(result,indent=2)+'\n');csvpath=Path(out).with_name('history.csv')
 with csvpath.open('w',newline='') as stream:
  writer=csv.DictWriter(stream,fieldnames=['branch','N','J','Y_charged','orbital_excitation','energy_error_over_excitation']);writer.writeheader()
  for branch,rows in curves.items():
   for h in rows:writer.writerow(dict(branch=branch,N=h['N'],J=h['action'],Y_charged=h['Y_charged'],orbital_excitation=h['orbital_excitation'],energy_error_over_excitation=h['energy_work_residual_over_excitation']))
 print(json.dumps(dict(checks=checks,comparison=comparison,branches={k:{n:v for n,v in d.items() if n not in ('final_numbers','group_numbers','ancestry')} for k,d in branches.items()})));assert all(checks.values())
if __name__=='__main__':main(*sys.argv[1:])
