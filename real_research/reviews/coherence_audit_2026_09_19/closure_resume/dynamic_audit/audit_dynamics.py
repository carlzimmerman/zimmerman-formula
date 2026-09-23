"""Read-only independent tests of archived ADM reduction; only writes beside itself."""
from pathlib import Path
import json, math, time, hashlib, sys
import sympy as s
import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import eigvalsh
start=time.time()
here=Path(__file__).resolve().parent
source=here.parents[1]/'frw_repair'/'run_verified'
record=json.loads((source/'general_reduced.json').read_text())
M,R=[s.sympify(record[z]) for z in ('mass','rest')]
a,h,q,j,ep,xi,k,alpha,adot=[s.sympify(z) for z in record['vars']]
b=next(z for z in M.free_symbols if str(z)=='clock_c2')
gc=1+s.Rational(3,2)*b
hd=q*j/(4*gc)
def Dt(z):
 return s.diff(z,a)*a*h+s.diff(z,h)*hd-3*ep*h*s.diff(z,q)-3*h*j*s.diff(z,j)+adot*s.diff(z,alpha)
def simp(z):return s.factor(z)
K=-M; D=-R[:,[1,3]]; U=-R[:,[0,2]]
helm1=(D+D.T-2*K.applyfunc(Dt)).applyfunc(simp)
helm2=(U-U.T-(D-D.T).applyfunc(Dt)/2).applyfunc(simp)
print('HELMHOLTZ',helm1,helm2,flush=True)
assert helm1==s.zeros(2) and helm2==s.zeros(2)
V=(U+U.T)/2
# Homogeneous trace, not only lapse/charge.
F=ep*j; Lam=3*gc*h*h-(ep-q)*j/2
trace=s.factor(18*gc*h*h+12*gc*hd-3*(F+2*Lam))
assert trace==0
print('TRACE',trace,flush=True)
# Comparison with independent frozen matrices includes a-dot=0 and c2 substitution.
checks={}
for label, filename, bn, an in [('constant','constant_reduced.json',s.Rational(1,39998),s.Rational(1,40000)),('response','response_reduced.json',s.Rational(3,100),None)]:
 rr=json.loads((source/filename).read_text())
 sub={b:bn}
 if an is not None:sub.update({alpha:an,adot:0})
 checks[label]=all(s.factor(v)==0 for nm,z in [('mass',M),('rest',R)] for v in (z.subs(sub)-s.sympify(rr[nm])))
assert all(checks.values())
# Fully differentiated physical observables, after reduced equations.
f,fd,u,ud=s.symbols('f fd u ud'); state=s.Matrix([f,fd,u,ud]); acc=(-M.inv()*R).applyfunc(s.factor)
lapse=s.sympify(record['lapse']); shift=s.sympify(record['shift'])
def field_Dt(z):
 return Dt(z)+s.diff(z,f)*fd+s.diff(z,u)*ud+s.diff(z,fd)*(acc*state)[0]+s.diff(z,ud)*(acc*state)[1]
obs=s.Matrix([f,u,lapse,f+h*u/q,(ud-q*lapse)/ep,f-h*a*shift,lapse+field_Dt(a*shift), q/(q-ep)*((ud-q*lapse)/ep-3*h*a*shift), (-3*(fd+h*lapse)+k*k*shift/a)/h, k*lapse/(a*h)])
obs=obs.applyfunc(s.factor)
T=obs.jacobian(state)
variables=(a,h,q,j,ep,xi,k,alpha,adot,b)
af=s.lambdify(variables,acc,'numpy',cse=True)
tf=s.lambdify(variables,T,'numpy',cse=True)
kf=s.lambdify(variables,K,'numpy',cse=True)
vf=s.lambdify(variables,V,'numpy',cse=True)
def make_case(label,bn,an,nalpha,a0,km,dn):
 eps=1e-9;j0=-1.86/(1-eps);Gc=1+1.5*bn;lam=3*Gc-(eps-1)*j0/2;hub=299792458/67400;xx=4e-6/hub;kk=km*hub
 def bg(n):
  aa=np.exp(n);qq=1-3*eps*n;jj=j0/aa**3;hh=np.sqrt(((eps-qq)*jj/2+lam)/(3*Gc));hhp=qq*jj/(4*Gc)
  if nalpha:
   vv=1e-7*aa**-4;al=.5*vv/(.5+vv);alp=-4*hh*al*(1-2*al)
  else:al=an;alp=0.
  return [aa,hh,qq,jj,eps,xx,kk,al,alp,bn],hhp
 def mat(n):
  args,hhp=bg(n);hh=args[1];ac=np.array(af(*args),float);ac[:,[1,3]]*=hh;ac/=hh**2;ac[0,1]-=hhp/hh**2;ac[1,3]-=hhp/hh**2
  return np.array([[0,1,0,0],ac[0],[0,0,0,1],ac[1]])
 def observ(n,y):
  args,_=bg(n);z=y*np.array([1,args[1],1,args[1]]);return np.array(tf(*args),float)@z
 n0=math.log(a0);n1=n0+dn;ev,evec=np.linalg.eig(mat(n0));idx=np.argmax(ev.real);y0=evec[:,idx].real;y0/=np.linalg.norm(y0)
 sol=solve_ivp(lambda n,y:mat(n)@y,(n0,n1),y0,method='DOP853',rtol=2e-12,atol=1e-15,max_step=dn/100,dense_output=True)
 assert sol.success
 ini=observ(n0,y0);fin=observ(n1,sol.y[:,-1]);interval=[]
 for n in np.linspace(n0,n1,11):
  args,_=bg(n);y=sol.sol(n);obsnow=observ(n,y)
  Kin=np.array(kf(*args),float);Pot=np.array(vf(*args),float)
  try: vr=eigvalsh(Pot,Kin)/args[1]**2
  except Exception: vr=[float('nan')]*2
  interval.append({'N_offset':float(n-n0),'max_instant_eigenvalue':float(max(np.linalg.eigvals(mat(n)).real)),'observables':obsnow.tolist(),'generalized_V_eigenvalues_H2':list(map(float,vr))})
 result={'case':label,'a0':a0,'k_Mpc':km,'delta_N':dn,'y0':y0.tolist(),'y1':sol.y[:,-1].tolist(),'initial_eigenvalues':[[float(z.real),float(z.imag)] for z in ev],'observables':['Phi_clock','P_clock','lapse_clock','Phi_uniform_scalar','deltaQ_over_epsilon','Phi_Newtonian','Psi_Newtonian','delta_rho_Newtonian_over_rho','delta_clock_expansion_over_H','clock_acceleration_over_H'],'initial_observables':ini.tolist(),'final_observables':fin.tolist(),'amplification':(fin/ini).tolist(),'samples':interval}
 print('CASE',label,'obs gain',result['amplification'],'eval',ev,flush=True)
 return result
results=[]
for args in [('constant',1/39998,1/40000,False,.1,.1,.01),('response_n4',.03,None,True,.5,.001,.004)]:results.append(make_case(*args))
summary={'claim_scope':'Exact Helmholtz and trace identities for supplied quadratic ADM system; bounded double-precision physical-observable evolution only.','trace_zero':True,'helmholtz_zero':True,'archived_matrix_matches':checks,'cases':results,'elapsed_seconds':time.time()-start,'inputs_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [source/'general_reduced.json',source/'constant_reduced.json',source/'response_reduced.json']},'python':sys.version,'sympy':s.__version__,'numpy':np.__version__}
out=Path(sys.argv[1]) if len(sys.argv)>1 else here
out.mkdir(exist_ok=True)
(out/'audit_results.json').write_text(json.dumps(summary,indent=2)+'\n')

(out/'symbolic_observables.json').write_text(json.dumps({'observables':[s.srepr(x) for x in obs], 'T':s.srepr(T), 'K':s.srepr(K), 'D':s.srepr(D), 'U':s.srepr(U), 'acceleration':s.srepr(acc), 'variables':[s.srepr(x) for x in variables]},indent=1)+'\n')
print('NEWTONIAN_EQUAL',s.factor(obs[5]-obs[6]),flush=True)
