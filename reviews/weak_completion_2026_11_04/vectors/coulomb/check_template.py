import sys,json,time,resource,math,gc
from pathlib import Path
HERE=Path(__file__).parent;ROOT=HERE.parents[3];sys.path.insert(0,str(HERE));import numpy as np
from elastic_builder_v2 import grid,screening,event_arrays_chunked,make_events
from template import template_arrays

def main(out):
 start=time.monotonic();stage=json.loads((ROOT/'reviews/collision_completion_2026_11_04/memory/run_stage001/result.json').read_text());edges=np.array(stage['q_edges']);q,W,cells=grid(edges,1);fi=np.full(len(q),1e-45);ff=fi.copy();good=cells>=0;fi[good]=2*np.array(stage['initial_fS'])[cells[good]];ff[good]=2*np.array(stage['final_fS'])[cells[good]];m=.003/2*math.sqrt(25.4000254000381**2+2/(31*.003));Tref=1e-6;ref=event_arrays_chunked(q,W,Tref,m,screening(q,W,ff,Tref,m),incoming_angles=8,azimuth=2,log_order=2,max_log_span=3.);ref['reference_screening_f']=ff.copy();rows=[]
 for name,T,f in [('initial',1e-5,fi),('middle',math.sqrt(1e-11),np.sqrt(fi*ff)),('final',1e-6,ff)]:
  temp=template_arrays(ref,T,f);te=make_events(temp);rt=te.number_rhs(f);kt=temp['kinetic_energy'];number=float(abs(sum(rt))/sum(abs(rt)));energy=float(abs(kt@rt)/sum(abs(kt*rt)));del te,temp;gc.collect();a=event_arrays_chunked(q,W,T,m,screening(q,W,f,T,m),incoming_angles=8,azimuth=2,log_order=2,max_log_span=3.);ev=make_events(a);rf=ev.number_rhs(f);scale=float(rt@rf/(rt@rt));error=float(sum(abs(rt-rf))/sum(abs(rf)));shape=float(sum(abs(rt*scale-rf))/sum(abs(rf)));row=dict(name=name,Tc=T,RHS_L1_relative=error,best_scale=scale,RHS_shape_residual_after_best_scale=shape,number_residual_relative=number,energy_residual_relative=energy,entropy_production=float(ev.entropy_production(f)));rows.append(row);print(row,flush=True);del ev,a;gc.collect()
 checks=dict(template=bool(max(r['RHS_L1_relative'] for r in rows)<.05),N=bool(max(r['number_residual_relative'] for r in rows)<1e-12),energy=bool(max(r['energy_residual_relative'] for r in rows)<1e-10),entropy=bool(min(r['entropy_production'] for r in rows)>0))
 Path(out).write_text(json.dumps(dict(rows=rows,checks=checks,runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='ThreeactualcoldT/shapecontrolsforNRleadinglogtemplate,reprojectedexactnewKconservatively. Dynamiclogscalingapproximation, notexactTc-invariance; testedRHSresidualboundsapplyonlythesepackets.'),indent=2)+'\n');assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
