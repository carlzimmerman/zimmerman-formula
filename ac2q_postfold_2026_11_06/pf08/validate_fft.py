import argparse,json,time
import numpy as np
from fft_constraints import FFTSystem,FFTPadded,Dense
from evolve_projected import rk4
from dealias import Padded
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();t0=time.time();out={};checks={}
f=FFTSystem(63,128);d=Dense(63,128);y=f.initial();d.P=f.P.copy();R,J,ff=f.fields(y,f.P,True);Rd,Jd,fd=d.fields(y,d.P,True)
th=2*np.pi*np.arange(63)/63;v=np.sin(th)+.3*np.cos(4*th)+.2;apply,_=J;ep=1e-10
rp,_,_=f.fields(y,f.P+ep*v);rm,_,_=f.fields(y,f.P-ep*v)
err=float(np.max(abs((rp-rm)/(2*ep)-apply(v)))/np.max(abs(apply(v))));out['JVP_finite_difference']=err;checks['JVP_FD']=err<1e-4
err=float(np.max(abs(Jd@v-apply(v)))/np.max(abs(apply(v))));out['JVP_dense']=err;checks['JVP_dense']=err<1e-10
rf=f.rhs(y);rd=d.rhs(y);err=float(np.max(abs(rf-rd)));out['initial_RHS_dense']=err;checks['initial_RHS_dense']=err<1e-7
# Nontrivial smooth state, with identical constraint solve tolerances.
y[1:64]+=1e-7*np.cos(th);y[127:]+=1e-4*np.sin(2*th)
f.P*=0;d.P*=0
rf=f.rhs(y);rd=d.rhs(y);err=float(np.max(abs(rf-rd)));out['smooth_RHS_dense']=err;checks['smooth_RHS_dense']=err<1e-6
f=FFTPadded(31,evaluation=93);d=Padded(31,factor=3);yf=f.initial();yd=d.initial()
for _ in range(200):yf=rk4(f,yf,.0025);yd=rk4(d,yd,.0025)
fldf=f.fine.constrain(f.fine.project(f.lift(yf,93)));fldd=d.fine.constrain(d.fine.project(d.lift(yd,93)))
errors={k:float(np.max(abs(fldf[k]-fldd[k])))for k in ['q','N','b','pb']};out['endpoint_t05']=errors;checks['endpoint_q']=errors['q']<1e-8;checks['endpoint_pb']=errors['pb']<1e-4
f=FFTPadded(31);y=f.initial(True)
for _ in range(40):y=rk4(f,y,.0025)
t=.1;ss=.01;V=.01;yy=np.sqrt(2*V/ss)*np.sinh(np.arcsinh(np.sqrt(ss/(2*V)))-np.sqrt(3*ss/2)*t);B=-np.log(yy)/3;H=np.sqrt((ss/2+V*np.exp(6*B))/3)
err=float(max(abs(y[0]-B),max(abs(y[1:32]-B)),max(abs(y[32:63]+2*H)),max(abs(y[63:]+4*H))));out['FRW_error']=err;checks['FRW']=err<1e-8
out.update(checks={k:bool(v)for k,v in checks.items()},all_pass=bool(all(checks.values())),seconds=time.time()-t0);open(a.output,'w').write(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));raise SystemExit(0 if out['all_pass']else 1)
