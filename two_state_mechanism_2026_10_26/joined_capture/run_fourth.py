import sys,json,argparse,time
from pathlib import Path
import numpy as np
from fourth import diagonal,link,response
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'nuclear_flux'))
from electronic import states,overlap
from lead import modes
p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--basis',required=True);p.add_argument('--h',type=float,required=True);p.add_argument('--end',type=float,default=30);a=p.parse_args()
# Fix the outermost site at end; add a single inner point if needed for paired blocks.
N=round((a.end-.5)/a.h)+1
if N%2:N+=1
R=a.end-np.arange(N-1,-1,-1)*a.h;Es=[-.62,-.6,-.58];Gs=[None]*len(Es);prev=None;t=1/(100*a.h*a.h);start=time.monotonic()
for i in range(0,N,2):
 pair=[states(R[i+j],a.basis) for j in [0,1]];n=len(pair[0][3]);H=diagonal(pair[0][3],pair[1][3],overlap(*pair),t);I=np.eye(2*n)
 if prev is not None:W=link(overlap(prev[0],pair[0]),overlap(prev[1],pair[0]),overlap(prev[1],pair[1]),t)
 As=[]
 for j,E in enumerate(Es):
  A=E*I-H
  if prev is not None:A-=W.T@Gs[j]@W
  Gs[j]=np.linalg.inv(A);As.append(A)
 prev=pair
 if i%100==0:print(i,N,'seconds',time.monotonic()-start,flush=True)
future=[states(a.end+(j+1)*a.h,a.basis) for j in [0,1]]
# Match each repeated site gauge to its corresponding site in the terminal block.
for j in [0,1]:
 O=overlap(pair[j],future[j]);sign=np.sign(np.diag(O));assert np.all(sign!=0)
 m,C,ci,V=future[j];future[j]=(m,C,ci*sign[:,None,None],V)
W=link(overlap(pair[0],future[0]),overlap(pair[1],future[0]),overlap(pair[1],future[1]),t)
rows=[]
for j,E in enumerate(Es):
 row=response(As[j],H,W,E,modes);row['energy']=E;rows.append(row);print(E,row['ground_to_other'],flush=True)
Path(a.output).write_text(json.dumps(dict(settings=dict(basis=a.basis,h=a.h,end=a.end,Rmin=float(R[0]),electronic_states=n,mu=50,rotation='omitted fixed-axis',lead='repeat final two-site block, future overlap links'),rows=rows,seconds=time.monotonic()-start,physical_DR_rates_derived=False),indent=2)+'\n')
