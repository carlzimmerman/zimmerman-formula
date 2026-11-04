"""Observed vectorized-builder speed, exact equivalence and composite memory QA."""
import sys,json,time,resource,gc,math
from pathlib import Path
import numpy as np
from network import ROOT
from angular_exact import exact_events
from angular_fast import exact_events_fast,averaged_exact_fast
from consistent_background_frozen import ConsistentVertexBackground

def relative(a,b):return float(sum(abs(np.asarray(a)-np.asarray(b)))/max(sum(abs(np.asarray(a))),1e-300))
def jrelative(a,b):
 diff=(a-b).tocsr();return float(sum(abs(diff.data))/max(sum(abs(a.data)),1e-300))

def main(out):
 start=time.monotonic();p=ROOT/'reviews/collision_completion_2026_11_04/cascades';checkpoint=json.loads((p/'warm_checkpoint001.json').read_text());c=checkpoint['case'];q=np.array(c['q']);W=np.array(c['W']);Y=np.array(checkpoint['state']['Y']);t=.004657258204883617*math.exp(-checkpoint['state']['N']);bg=ConsistentVertexBackground(p/'run_vertices001/result.json');cases=[];measure=None
 for x in (3.6,3.83742513487,4.08,25.4000254000381):
  d=bg.at(x);ts=time.perf_counter();old=exact_events(d,t,q,W,source=d['current_source']);oldtime=time.perf_counter()-ts;ts=time.perf_counter();new=exact_events_fast(d,t,q,W,source=d['current_source']);newtime=time.perf_counter()-ts;f=Y/new.measure;av=1+new.eta*f;measure=new.measure;rhs0=old.number_rhs(f,av);rhs1=new.number_rhs(f,av);J0=old.number_jacobian(f,av);J1=new.number_jacobian(f,av);row=dict(x=x,segments_old=len(old.coefficient),segments_new=len(new.coefficient),same_indices=bool(np.array_equal(old.index,new.index)),weights_a_max=float(np.max(abs(old.a-new.a))),weights_b_max=float(np.max(abs(old.b-new.b))),coefficient_relative=relative(old.coefficient,new.coefficient),RHS_relative=relative(rhs0,rhs1),Jacobian_relative=jrelative(J0,J1),gross_relative=relative(old.number_gross(f,av),new.number_gross(f,av)),omission_relative=relative(old.omitted_by_parent,new.omitted_by_parent),old_build_seconds=oldtime,new_build_seconds=newtime,speedup=oldtime/newtime);cases.append(row);print(row,flush=True);del old,new,J0,J1;gc.collect()
 h=c['history'][-1];mid=(h['x_inner']+h['x_outer'])/2;amp=(h['x_outer']-h['x_inner'])/2;xs=mid-amp*np.cos(np.pi*(np.arange(8)+.5)/8);w=np.ones(8)/8;expected_rhs=np.zeros(len(Y));expected_gross=np.zeros(len(Y));expected_J=None;f=Y/measure;reference_time=0.
 for x,weight in zip(xs,w):
  d=bg.at(float(x));ts=time.perf_counter();op=exact_events(d,t,q,W,source=d['current_source']);av=1+op.eta*f;expected_rhs+=weight*op.number_rhs(f,av);expected_gross+=weight*op.number_gross(f,av);J=weight*op.number_jacobian(f,av);expected_J=J if expected_J is None else expected_J+J;reference_time+=time.perf_counter()-ts;del op,J;gc.collect()
 ts=time.perf_counter();composite=averaged_exact_fast(bg,xs,w,t,q,W);buildtime=time.perf_counter()-ts;av=1+composite.eta*f;ts=time.perf_counter();rhs=composite.number_rhs(f,av);rhstime=time.perf_counter()-ts;ts=time.perf_counter();J=composite.number_jacobian(f,av);jtime=time.perf_counter()-ts;gross=composite.number_gross(f,av);combined=dict(phases=8,segments=composite.segment_count,build_seconds=buildtime,RHS_seconds=rhstime,Jacobian_seconds=jtime,reference_build_RHS_J_seconds=reference_time,RHS_relative=relative(expected_rhs,rhs),Jacobian_relative=jrelative(expected_J,J),gross_relative=relative(expected_gross,gross),local_energy_residual=composite.local_energy_residual)
 checks=dict(same_segment_counts=all(r['segments_old']==r['segments_new'] and r['same_indices'] for r in cases),weights_equivalent=max(max(r['weights_a_max'],r['weights_b_max']) for r in cases)<1e-12,point_RHS=max(r['RHS_relative'] for r in cases)<1e-11,point_Jacobian=max(r['Jacobian_relative'] for r in cases)<1e-10,omission=max(r['omission_relative'] for r in cases)<1e-11,composite_RHS=combined['RHS_relative']<1e-11,composite_Jacobian=combined['Jacobian_relative']<1e-10,composite_gross=combined['gross_relative']<1e-11)
 checks={k:bool(v) for k,v in checks.items()};result=dict(claim_id='CC10_FAST_EXACT_ANGULAR_EQUIVALENCE',cases=cases,composite=combined,checks=checks,runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Vectorized construction compared against frozen exactangularbuilder onactualwarm/pole points andeightphasewarmspan; sameanalyticmomentbackend. Measuredperformance/RSS for thisenvironment, no universalperformanceclaim. Memoryleanphasecomposite checked bysumofindependentreferencephaseoperators.')
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(checks,combined,'RSS',result['peak_rss_bytes_macos']);assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
