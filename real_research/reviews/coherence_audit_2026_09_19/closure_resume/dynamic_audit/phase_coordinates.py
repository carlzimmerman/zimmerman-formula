from pathlib import Path
import json,math,time,sys
import numpy as np
import sympy as s
from scipy.integrate import solve_ivp
here=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent;d=json.loads((here/'symbolic_observables.json').read_text());v=[s.sympify(z) for z in d['variables']];a,h,q,j,ep,xi,k,al,ald,b=v;gc=1+s.Rational(3,2)*b;hd=q*j/(4*gc)
acc=s.sympify(d['acceleration']);TT=s.sympify(d['T']);f,fd,u,ud=s.symbols('f fd u ud');state=s.Matrix([f,fd,u,ud]);obs=TT*state
Ac=s.Matrix([[0,1,0,0],list(acc[0,:]),[0,0,0,1],list(acc[1,:])])
aldd=s.Symbol('alpha_ddot',real=True)
def dt(z):return a*h*s.diff(z,a)+hd*s.diff(z,h)-3*ep*h*s.diff(z,q)-3*h*j*s.diff(z,j)+ald*s.diff(z,al)+aldd*s.diff(z,ald)
# State: Newtonian metric potential, Newtonian density contrast,
# H times clock time shift relative to Newtonian slicing, and its log-a derivative.
clock=h*(f-obs[5])/h
clockd=(dt(clock)+(s.Matrix([clock]).jacobian(state)*Ac*state)[0])/h
ph=s.Matrix([obs[5],obs[7],clock,clockd]).applyfunc(s.factor)
S=ph.jacobian(state)
Sd=(S.applyfunc(dt)+S*Ac)/h
print('phase matrix derived',flush=True)
sf=s.lambdify(v,S,'numpy',cse=True);sdf=s.lambdify(v+[aldd],Sd,'numpy',cse=True);af=s.lambdify(v,acc,'numpy',cse=True);tf=s.lambdify(v,TT,'numpy',cse=True)
results=[]
for c in json.loads((here/'audit_results.json').read_text())['cases'][:2]:
 label=c['case'];bn=1/39998 if label=='constant' else .03;eps=1e-9;j0=-1.86/(1-eps);Gc=1+1.5*bn;lam=3*Gc-(eps-1)*j0/2;hub=299792458/67400;n0=math.log(c['a0'])
 def bg(n):
  aa=np.exp(n);qq=1-3*eps*n;jj=j0/aa**3;hh=np.sqrt(((eps-qq)*jj/2+lam)/(3*Gc));hhd=qq*jj/(4*Gc)
  if label=='constant':alpha=1/40000;ad=0.
  else:vv=1e-7*aa**-4;alpha=.5*vv/(.5+vv);ad=-4*hh*alpha*(1-2*alpha)
  return [aa,hh,qq,jj,eps,4e-6/hub,c['k_Mpc']*hub,alpha,ad,bn],hhd
 def mat(n):
  args,hhd=bg(n);hh=args[1];ac=np.array(af(*args),float);ac[:,[1,3]]*=hh;ac/=hh**2;ac[0,1]-=hhd/hh**2;ac[1,3]-=hhd/hh**2
  return np.array([[0,1,0,0],ac[0],[0,0,0,1],ac[1]])
 def phase(n,y):
  args,_=bg(n);z=y*np.array([1,args[1],1,args[1]]);sval=np.array(sf(*args));alpha,ad=args[7:9]; add=0. if label=='constant' else -4*(bg(n)[1]*alpha*(1-2*alpha)+args[1]*ad*(1-4*alpha));sdval=np.array(sdf(*args,add));B=np.linalg.solve(sval.T,sdval.T).T
  return {'physical_state':(sval@z).tolist(),'eigenvalues':[[float(x.real),float(x.imag)] for x in np.linalg.eigvals(B)],'matrix':B.tolist(),'transform_condition':float(np.linalg.cond(sval)), 'observable_values':(np.array(tf(*args))@z).tolist()}
 y0=np.array(c['y0']);sol=solve_ivp(lambda n,y:mat(n)@y,(n0,n0+.1),y0,rtol=1e-11,atol=1e-15,max_step=.0001,dense_output=True)
 assert sol.success
 rr={'case':label,'phase_names':['Phi_Newtonian','density_Newtonian','H_clock_shift','d_H_clock_shift_dN'],'samples':[{'delta_N':dn,**phase(n0+dn,sol.sol(n0+dn))} for dn in [0,c['delta_N'],.02,.05,.1]]}
 print(json.dumps(rr),flush=True);results.append(rr)
(here/'phase_results.json').write_text(json.dumps(results,indent=2)+'\n')
(here/'phase_transform.json').write_text(json.dumps({'S_cosmic_state':s.srepr(S),'dS_plusSA_overH':s.srepr(Sd),'variables':d['variables']+[s.srepr(aldd)]},indent=1)+'\n')
