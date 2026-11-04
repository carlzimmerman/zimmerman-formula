"""Exact lightchargedscalar neutral-parent widths on a conditional densegrid."""
import sys,os
sys.dont_write_bytecode=True
from pathlib import Path
import json,time,resource
import numpy as np
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'reviews/coupled_trapping_2026_11_04/microphysics'))
from scalar_network import one

def main(out):
 start=time.monotonic();xs=np.unique(np.r_[np.linspace(3.8,12,42),np.arange(13,20),np.arange(20,25,.2),np.arange(25,25.5,.025),25.4000254,25.399,25.401,np.arange(25.5,28,.1),29,30,35,40]);rows=[]
 for x in xs:
  d=one(float(x));groups=[]
  for p in d['neutral_parents']:
   W=p['to_light_scalar_pair'];M=p['mass']
   if W<=0:continue
   match=next((q for q in groups if abs(q[0]-M)<1e-9),None)
   if match is None:groups.append([M,W])
   else:match[1]+=W
  rows.append(dict(x=float(x),mS=d['m_light_S'],parents=groups,checks=d['checks']))
 result=dict(claim_id='CT09_LIGHT_SCALAR_WIDTH_TABLE',cases=rows,checks={'upstream_internal_checks':all(all(r['checks'].values()) for r in rows)},runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Rigid tree inclusive partialwidths of neutralrealparents to lightest physicalchargedscalarpair. Degenerate parents grouped bywidthsum; diagonal widths only, interference of exactlydegenerate neutralparents not resolved here. Not irreversiblebranching.')
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ('checks','runtime_seconds','peak_rss_bytes')}));assert all(result['checks'].values())
if __name__=='__main__':main(sys.argv[1])
