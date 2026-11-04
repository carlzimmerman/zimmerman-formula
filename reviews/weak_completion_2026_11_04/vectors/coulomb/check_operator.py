import sys,json,time,resource,math,gc
from pathlib import Path
HERE=Path(__file__).parent;ROOT=HERE.parents[3];sys.path.insert(0,str(HERE));import numpy as np
from elastic_builder_v2 import grid,screening,event_arrays_chunked,make_events

def main(out):
 start=time.monotonic();stage=json.loads((ROOT/'reviews/collision_completion_2026_11_04/memory/run_stage001/result.json').read_text());old=json.loads((ROOT/'reviews/coupled_trapping_2026_11_04/kinetics/run_hybrid_bw_001/result.json').read_text())['case'];q,W,cells=grid(np.array(stage['q_edges']),1);f=np.full(len(q),1e-45);good=cells>=0;f[good]=2*np.array(stage['final_fS'])[cells[good]];T=old['history'][-1]['Tc_over_mu'];x=old['history'][-1]['x_minimum'];m=.003/2*math.sqrt(x*x+2/(31*.003));md=screening(q,W,f,T,m);rows=[];rhs=[]
 for angle,phi,lg,span in [(4,2,2,3.),(8,2,2,3.),(8,4,3,3.)]:
  a=event_arrays_chunked(q,W,T,m,md,incoming_angles=angle,azimuth=phi,log_order=lg,max_log_span=span,diagnostic_f=f);ev=make_events(a);r=ev.number_rhs(f);rhs.append(r);row=dict(incoming_angles=angle,azimuth=phi,log_order=lg,max_log_span=span,events=len(ev.coefficient),number_rhs=r.tolist(),entropy_production=float(ev.entropy_production(f)),Nrelative=float(abs(sum(r))/sum(abs(r))),Krelative=float(abs(a['kinetic_energy']@r)/sum(abs(a['kinetic_energy']*r))),dropped_dp2_fraction=a['diagnostics']['dropped_dp2_fraction']);rows.append(row);print(angle,phi,len(ev.coefficient),flush=True);del ev,a;gc.collect()
 den=sum(abs(rhs[-1]));errors=[float(sum(abs(r-rhs[-1]))/den) for r in rhs];checks=dict(positive_entropy=bool(all(r['entropy_production']>0 for r in rows)),N=bool(all(r['Nrelative']<1e-12 for r in rows)),K=bool(all(r['Krelative']<1e-10 for r in rows)),angular_RHS=bool(errors[1]<.1),support=bool(all(r['dropped_dp2_fraction']<1e-5 for r in rows)))
 Path(out).write_text(json.dumps(dict(rows=rows,RHS_L1_relative_to_finest=errors,checks=checks,runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Actualcoldmemorypacket nonlinearquantumcollisionRHSangular/logquadraturerefine; same39nodeprojection, notmomentumcontinuumproof.'),indent=2)+'\n');assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
