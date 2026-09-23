from pathlib import Path
import json, math, sys
import sympy as s
import mpmath as mp
here=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent
d=json.loads((here/'symbolic_observables.json').read_text());v=[s.sympify(z) for z in d['variables']]
af=s.lambdify(v,s.sympify(d['acceleration']),'mpmath',cse=True);of=s.lambdify(v,s.sympify(d['T']),'mpmath',cse=True)
mp.mp.dps=50;results=[]
for c in json.loads((here/'audit_results.json').read_text())['cases'][:2]:
 label=c['case'];bn=mp.mpf(1)/39998 if label=='constant' else mp.mpf('.03');eps=mp.mpf('1e-9');j0=-mp.mpf('1.86')/(1-eps);Gc=1+mp.mpf('1.5')*bn;lam=3*Gc-(eps-1)*j0/2;hub=mp.mpf(299792458)/67400;n0=mp.log(mp.mpf(str(c['a0'])))
 def bg(n):
  aa=mp.exp(n);qq=1-3*eps*n;jj=j0/aa**3;hh=mp.sqrt(((eps-qq)*jj/2+lam)/(3*Gc));hhd=qq*jj/(4*Gc)
  if label=='constant':al=mp.mpf(1)/40000;ad=mp.mpf(0)
  else:vv=mp.mpf('1e-7')*aa**-4;al=mp.mpf('.5')*vv/(mp.mpf('.5')+vv);ad=-4*hh*al*(1-2*al)
  return [aa,hh,qq,jj,eps,mp.mpf('4e-6')/hub,mp.mpf(str(c['k_Mpc']))*hub,al,ad,bn],hhd
 def rhs(n,y):
  args,hd=bg(n);h=args[1];state=mp.matrix([y[0],h*y[1],y[2],h*y[3]]);ac=af(*args)*state/h**2
  return mp.matrix([y[1],ac[0]-hd/h**2*y[1],y[3],ac[1]-hd/h**2*y[3]])
 trials=[]
 for steps in ([2000,4000] if label=='constant' else [8000,16000]):
  n=n0;y=mp.matrix(c['y0']);step=mp.mpf('.1')/steps
  for ii in range(steps):
   k1=rhs(n,y);k2=rhs(n+step/2,y+step*k1/2);k3=rhs(n+step/2,y+step*k2/2);k4=rhs(n+step,y+step*k3);y+=step*(k1+2*k2+2*k3+k4)/6;n+=step
  args,_=bg(n);z=mp.matrix([y[0],args[1]*y[1],y[2],args[1]*y[3]]);obs=of(*args)*z
  trials.append({'steps':steps,'state':[float(z) for z in y],'observables':[float(z) for z in obs]})
 r={'case':label,'dps':50,'delta_N':.1,'trials':trials,'state_relative_step_doubling':float(mp.norm(mp.matrix(trials[0]['state'])-mp.matrix(trials[1]['state']))/mp.norm(mp.matrix(trials[1]['state'])))}
 print(json.dumps(r),flush=True);results.append(r)
(here/'high_precision_results.json').write_text(json.dumps(results,indent=2)+'\n')
