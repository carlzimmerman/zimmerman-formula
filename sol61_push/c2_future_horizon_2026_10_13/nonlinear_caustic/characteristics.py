"""Exact vacuum Hamilton flow; central fold bounds first smooth caustic time."""
import argparse,json
from pathlib import Path
import numpy as np
import sympy as s
from scipy.integrate import solve_ivp

ap=argparse.ArgumentParser();ap.add_argument('--output-dir',required=True)
OUT=Path(ap.parse_args().output_dir)
root=Path(__file__).parent.parent
src=json.loads((root/'source_snapshot/self_gravity_results.json').read_text())
case=next(c for c in src['cases'] if c['b']==1000)
C=case['Y']**2/2000;E=np.sqrt(1-C)
xx,pp,cc,ee=s.symbols('x p C E',real=True)
bb=1-cc*(2/(3*xx)+xx**2/3);nn=s.sqrt(bb)/ee
HH=nn*s.sqrt(1+bb*pp**2)
func=s.lambdify([xx,pp,cc,ee],[HH,s.diff(HH,xx),s.diff(HH,pp),s.diff(HH,xx,2),s.diff(HH,xx,pp),s.diff(HH,pp,2)],'numpy',cse=True)
def B(x):return 1-C*(2/(3*x)+x*x/3)
def Bp(x):return C*(2/(3*x*x)-2*x/3)
def S(x):return np.sqrt(C)*(x-1)*np.sqrt((x+2)/(3*x))
x0=2.;p0=-S(x0)/B(x0)
pbprime=Bp(x0)/(2*S(x0)*B(x0))+S(x0)*Bp(x0)/B(x0)**2
hpp0=float(func(x0,p0,C,E)[-1]);assert hpp0>0
epsilon=.001
# Analytic cutoff derivative bound plus conservative lower outgoing slope.
outgoing_lower=np.sqrt(C)*.75*np.sqrt((2.25+2)/(3*2.25))
assert epsilon*(1+12.5/1024)<outgoing_lower
initial=np.array([x0,p0,1.,0.,0.,1.])
records=[];arrays={}
for k in [1024,2048,4096,8192]:
 slope=pbprime+epsilon*k
 limit=4/(hpp0*epsilon*k)
 def rhs(t,y,mutate=False):
  x,p=y[:2];M=y[2:].reshape(2,2)
  H,Hx,Hp,Hxx,Hxp,Hpp=func(x,p,C,E)
  A=np.array([[-Hxp,0 if mutate else -Hpp],[Hxx,Hxp]])
  return np.concatenate([[-Hp,Hx],(A@M).ravel()])
 def fold(t,y):
  M=y[2:].reshape(2,2)
  return M[0,0]+M[0,1]*slope
 fold.terminal=True;fold.direction=-1
 stages=[]
 for tight in [False,True]:
  sol=solve_ivp(rhs,(0,limit),initial,events=fold,dense_output=True,method='DOP853',rtol=2e-12 if tight else 2e-10,atol=2e-14 if tight else 2e-12)
  assert sol.success and len(sol.t_events[0])==1,(k,sol.message)
  event=float(sol.t_events[0][0]);end=sol.y_events[0][0]
  stages.append((event,end,sol))
 event,end,sol=stages[-1]
 difference=max(abs(event-stages[0][0]),float(np.max(abs(end-stages[0][1]))))
 assert difference<1e-7
 ts=np.linspace(0,event,501);ys=sol.sol(ts)
 M=ys[2:].T.reshape(-1,2,2)
 J=M[:,0,0]+M[:,0,1]*slope
 K=M[:,1,0]+M[:,1,1]*slope
 energies=np.array([func(x,p,C,E)[0] for x,p in ys[:2].T])
 energy_error=float(np.max(abs(energies-1)))
 det_error=float(np.max(abs(np.linalg.det(M)-1)))
 assert energy_error<1e-9 and det_error<1e-8
 assert ys[0].min()>=1.8 and ys[0].max()<=2.2 and np.all(ys[1]<0) and B(ys[0]).min()>.95
 assert abs(J[-1])<1e-8 and abs(K[-1])>.1
 event_rate=float(rhs(event,end)[2]+rhs(event,end)[3]*slope)
 assert event_rate<0
 mutation=solve_ivp(lambda t,y:rhs(t,y,True),(0,event),initial,t_eval=ts,method='DOP853',rtol=2e-12,atol=2e-14)
 assert mutation.success
 MM=mutation.y[2:].T.reshape(-1,2,2)
 JM=MM[:,0,0]+MM[:,0,1]*slope
 assert JM.min()>.5
 arrays['k'+str(k)]=np.column_stack([ts,ys[0],ys[1],J,K,energies,np.linalg.det(M),JM])
 records.append({'k':k,'epsilon':epsilon,'initial_momentum':p0,'initial_slope':slope,'center_fold_time_t_over_R':event,'first_caustic_interpretation':'first global smooth-caustic time no later than this central projection event','scaled_fold_time':event*hpp0*epsilon*k,'momentum_label_derivative_at_fold':float(K[-1]),'fold_rate':event_rate,'max_refinement_difference':difference,'max_energy_error':energy_error,'max_phase_space_determinant_error':det_error,'min_B':float(B(ys[0]).min()),'event_x':float(end[0]),'min_mutation_J':float(JM.min())})
np.savez_compressed(OUT/'profiles.npz',**arrays)
result={'all_passed':True,'b':1000,'Y':case['Y'],'C':C,'E':float(E),'Hpp0':hpp0,'epsilon':epsilon,'analytic_outgoing_momentum_lower_bound':float(outgoing_lower),'cases':records,'columns':['tau=t/R','x','p','projection_J','momentum_label_K','Hamiltonian','detM','mutation_J'],'scope':'exact X0 vacuum characteristics on unchanged Einstein metric up to first caustic; zero extra current/stress; bounded roots not error certificates; no physical UV cutoff established'}
(OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'all_passed':True,'Hpp0':hpp0,'cases':[{k:v for k,v in c.items() if k in ['k','center_fold_time_t_over_R','scaled_fold_time','max_refinement_difference']} for c in records]}))
