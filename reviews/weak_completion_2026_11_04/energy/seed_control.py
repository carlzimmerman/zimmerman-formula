"""Exact same split/Picard method, seeded versus unseeded BE Newton guesses."""
from one_step import *
import split_energy_v2 as unseeded
import split_energy_v3 as seeded

def main_seed(out):
 start=time.monotonic();path=ROOT/'reviews/collision_completion_2026_11_04/integration/run_fresh_exact002/result.json';d,bg,model,state,N,J,orb=load(path);rows=[];checks={};result=dict(claim_id='CC11_SEEDED_ENERGY_SOLVE_EQUIVALENCE',rows=rows,checks=checks)
 def save():
  result.update(runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss);Path(out).write_text(json.dumps(result,indent=2)+'\n')
 for name,module in [('unseeded',unseeded),('seeded',seeded)]:
  before=time.monotonic();ns,Jn,on,work,info=module.step(model,bg,averaged_exact_events,N,state,J,5e-5,geometry='midpoint',max_outer=8,outer_tol=2e-5);row=dict(method=name,runtime=time.monotonic()-before,final_J=Jn,final_energy=on['E'],independent_work=work,independent_residual=on['E']-orb['E']+work,final_numbers=ns.numbers().tolist(),info=info);rows.append(row);print(name,row['runtime'],Jn,info['collision']['outer_iterations'],flush=True);save()
 A=np.array(rows[0]['final_numbers']);B=np.array(rows[1]['final_numbers']);result['relative_number_difference']=float(sum(abs(A-B))/sum(abs(B)));result['relative_action_difference']=rows[1]['final_J']/rows[0]['final_J']-1;checks.update(number_equivalence=result['relative_number_difference']<1e-8,action_equivalence=abs(result['relative_action_difference'])<1e-7,physical_bounds=all(r['info']['collision']['min_f']>=0 and r['info']['collision']['max_fermion_f']<=1 for r in rows),independent_energy=all(abs(r['independent_residual'])/(orb['E']-orb['minimum'])<.01 for r in rows));save();assert all(checks.values())
if __name__=='__main__':main_seed(sys.argv[1])
