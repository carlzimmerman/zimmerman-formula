"""Arctan-angular finiteBW kernel versus independent splitcosine API."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import json,time,resource
import numpy as np
from finite_bw import pair_fast,pole

def main(out):
 start=time.monotonic();q=np.array([.01,.1,.3,1,2,3,5,8,13,20.]);w=q*q/(np.exp(q)+1);rows=[]
 for x,t in ((pole.DATA['xpole']-.001,.0005),(pole.DATA['xpole'],.00001),(pole.DATA['xpole']+.000001,.00001)):
  ref=pole.pair_matrix(x,t,q,32)
  for n in (8,12,24):
   a=pair_fast(x,t,q,n);rows.append(dict(x=x,t=t,n=n,weighted_relative_error=abs(float(w@a@w)/float(w@ref@w)-1),max_relative_entry_error=float(np.max(abs(a/ref-1))),minimum=float(np.min(a)),symmetric_error=float(np.max(abs(a-a.T)))))
 checks={'twelve_node_weighted_agreement':max(r['weighted_relative_error'] for r in rows if r['n']==12)<.005,'twentyfour_node_weighted_agreement':max(r['weighted_relative_error'] for r in rows if r['n']==24)<.001,'positivity_symmetry':all(r['minimum']>=0 and r['symmetric_error']<1e-14 for r in rows)};result=dict(claim_id='CT09_FINITE_BW_ANGULAR_CONTROL',checks=checks,cases=rows,runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Staticfixedpolecoefficientpairkernel, finitecellcenters, threepoints. Doesnotestablish Markovlocality inoscillatingfield, mediumoccupations oractualneutraldaughterfeedback.')
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));assert all(checks.values())
if __name__=='__main__':main(sys.argv[1])
