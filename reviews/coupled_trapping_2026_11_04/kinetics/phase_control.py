"""Narrow scalarpole phasequadrature control on fixedharmonic testorbits."""
import sys
sys.dont_write_bytecode=True
import json,math,time,resource
import numpy as np
from numpy.polynomial.legendre import leggauss
from resolved_v2 import Resolved
from two_species import ROOT,HERE

def main(out):
 start=time.monotonic();p=json.loads((ROOT/'reviews/gravity_completion_2026_11_03/thermal_kinetic/run_stationary_002/result.json').read_text())['points'][1];s=json.loads((ROOT/'reviews/gravity_completion_2026_11_03/thermal/run_static_001/result.json').read_text())['points'][1]['spins'][0];m=Resolved(p,s,bins=24,orbitn=16);pole=m.poles[1];rows=[]
 for t in (.0005,.0001,.00002):
  mid=pole-.001;amp=.2;xl=mid-amp;xr=mid+amp;dm=.003*pole/(2*math.sqrt(pole*pole+2/(31*.003)));base=t*t/(2*math.sqrt(.006)/2*dm);bounds=[0.,math.pi]
  for factor in (0.,.05,.2,1.,4.,16.,64.,256.):
   x=pole-factor*base
   if xl<x<xr:bounds.append(math.acos((mid-x)/amp))
  bounds=sorted(set(bounds));rates={}
  for n in (4,8,16):
   z,w=leggauss(n);total=0;nodes=0
   for a,b in zip(bounds[:-1],bounds[1:]):
    theta=(a+b)/2+(b-a)*z/2
    for th,ww in zip(theta,w*(b-a)/2):
     x=mid-amp*math.cos(th);rate=m.scalar_kernel(x,t)@m.f0/(t**3*m.W);total+=ww*float((m.W*m.f0)@rate)/(m.W@m.f0)/math.pi;nodes+=1
   rates[n]=float(total)
  rows.append(dict(Tc=t,mean_x=mid,amplitude=amp,split_intervals=len(bounds)-1,rates_mu=rates,relative_4_vs_16=abs(rates[4]/rates[16]-1),relative_8_vs_16=abs(rates[8]/rates[16]-1)))
 threshold=abs(.003*math.sqrt(pole*pole+2/(31*.003))/math.sqrt(.006)-1);checks={'scalar_pole_mass_identity':threshold<1e-14,'four_vs_sixteen_phase_nodes':max(r['relative_4_vs_16'] for r in rows)<.03,'eight_vs_sixteen_phase_nodes':max(r['relative_8_vs_16'] for r in rows)<.005};result=dict(claim_id='CT09_LATE_PHASE_QUADRATURE',checks=checks,scalar_pole=pole,threshold_relative_error=threshold,cases=rows,runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Conditional scalarparentabsorption on three prescribedharmonicorbits, momentumgridfixed. Controls sharp phasesamplingonly; no selfconsistentnewphysicalhistory or allphaseprofile guarantee.')
 (HERE/Path(out).name).exists() if False else None
 from pathlib import Path
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));assert all(checks.values())
if __name__=='__main__':main(sys.argv[1])
