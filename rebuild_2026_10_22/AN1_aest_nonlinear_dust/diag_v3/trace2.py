"""A3 audit on disclosed side-test rows only. Usage: key mu N stop(A1|snap) [Cf]. No grade."""
import sys,os,time,numpy as np
a=sys.argv[1:]; sys.argv=[sys.argv[0],'x']+[x for x in a if x.startswith('--')]; ARG=[x for x in a if not x.startswith('--')]
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
import an1_v3 as v, an1
key,mu,N,stop=ARG[0],float(ARG[1]),int(ARG[2]),ARG[3]; Cf=float(ARG[4]) if len(ARG)>4 else 1e-4
v.OPT['stop']=stop
R=v.build(key,mu,'canonical',N=N); R.forces(); t0=time.time(); vmax=0
while R.t<R.t0-1e-12 and time.time()-t0<1500:
    R.step(R.t0)
    if getattr(R,'crossed',False): print('crossed');break
    vmax=max(vmax,np.abs(R.v[1:]).max())
    if R.fold(Cf,R.dq): print('FOLD line');break
A=R.aval();dr=np.diff(R.r);i=int(np.argmin(dr))
print(key,mu,N,stop,'z %.4f step %d rej %d imin %d C %.2e r %.4g vmax %.1f turnbelow n %d m %.3g'%(1/A-1,R.nstep,getattr(R,'nrej',0),i,dr[i]/(A*R.dq),R.r[i],vmax,getattr(R,'n_turnbelow',0),getattr(R,'m_turnbelow',0)),'r1-4',np.array2string(R.r[1:5],precision=3),'v',np.array2string(R.v[1:5],precision=1),'wall %.0f'%(time.time()-t0),flush=True)
