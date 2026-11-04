"""Ordinary soft vertex versus background derivative and vector index orientation."""
import os,sys,json,math,time,resource
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import numpy as np
from matching import model,parent,coefficients,amplitude,ROOT
sys.path.insert(0,str(ROOT/'reviews/collision_completion_2026_11_04/neutral_loop'))
from gaugino_vertex import displaced
sys.path.insert(0,str(ROOT/'reviews/radial_ir_cold_2026_11_01/gapless_charge'))
from gaugino_threshold import threshold

def main(out):
 start=time.monotonic();d=model();rows=[];checks={}
 for name in ('S8_0','S3_0'):
  p=parent(d,name);tt=coefficients(d,p);soft=[];uv=[]
  for xi in (.5,1.,2.):
   a=amplitude(d,p,tt,xi,s=0.);v=sum(a.values());on=sum(amplitude(d,p,tt,xi).values())
   h=.001;plus=threshold(displaced(d['d'],h*p['ep']),d['ext'],xi=xi);minus=threshold(displaced(d['d'],-h*p['ep']),d['ext'],xi=xi)
   sc=(plus['scalar']-minus['scalar'])/(2*h);vc=(plus['vector']-minus['vector'])/(2*h)
   corr=(sc+vc.conj())[p['b'],11];old=(sc+vc)[p['b'],11]
   soft.append(dict(xi=xi,ordinary=[v.real,v.imag],on_shell=[on.real,on.imag],background_correct_vector_orientation=[corr.real,corr.imag],background_historical_vector_orientation=[old.real,old.imag]))
  a=amplitude(d,p,tt,1.);b=amplitude(d,p,tt,1.,uv=1.)
  uv={k:[(b[k]-a[k]).real,(b[k]-a[k]).imag] for k in a}
  ref=complex(*soft[1]['ordinary']);on=complex(*soft[1]['on_shell']);corr=complex(*soft[1]['background_correct_vector_orientation'])
  rows.append(dict(id=name,cases=soft,UV_by_topology=uv,finite_over_soft_amplitude=[(on/ref).real,(on/ref).imag],
   ordinary_soft_vs_corrected_background_relative_difference=abs(ref-corr)/abs(ref)))
  checks[name+'_separate_UV_cancellation']=max(abs(complex(*v)) for v in uv.values())/abs(on)<1e-8
  checks[name+'_soft_bridge']=abs(ref-corr)/abs(ref)<1e-4
 checks={k:bool(v) for k,v in checks.items()}
 result=dict(claim_id='CC11_SOFT_ORDINARY_BACKGROUND_BRIDGE',states=rows,checks=checks,runtime_seconds=time.monotonic()-start,
  peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(checks,flush=True);assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
