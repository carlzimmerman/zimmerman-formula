import argparse,json,sys
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from equations import quantities,rhs,initial,geometric_R_complex_step
ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--mutation',choices=['radiation_R_zero']);args=ap.parse_args();checks=[];runs=[]
def ck(n,b,e):checks.append({'name':n,'passed':bool(b),'detail':e})
floor=1e-8;target=np.log(1e-4)
for xi in [100.,1000.]:
 y0=initial(xi);Q0=quantities(0,y0,xi)['Q'];solutions=[]
 def fun(x,y):
  if args.mutation:
   z=quantities(x,y,xi);H=z['H'];return np.array([y[2]/H,y[3]/H,-3*y[2],-3*y[3],1/H])
  return rhs(x,y,xi)
 def event(x,y):return float(quantities(x,y,xi)['F']-floor)
 event.terminal=True;event.direction=0
 for method,tol in [('DOP853',1e-9),('DOP853',3e-10),('Radau',1e-9)]:
  sol=solve_ivp(fun,(0,target),y0,method=method,rtol=tol,atol=tol*1e-5,events=event,dense_output=True)
  endpoint=float(sol.t[-1]);grid=np.linspace(0,endpoint,81);ys=sol.sol(grid);vals=[];maxQ=0.;maxCg=0.;maxR=0.
  for x,y in zip(grid,ys.T):
   z=quantities(x,y,xi);qerr=abs(z['Q']/Q0-1);cg=abs(z['friedmann'])/max(z['friedmann_scale'],1e-100)
   rg=geometric_R_complex_step(x,y,xi,direction=fun(x,y));re=abs(rg-z['R'])/(abs(z['R'])+6*z['H']**2)
   maxQ=max(maxQ,qerr);maxCg=max(maxCg,cg);maxR=max(maxR,re)
   vals.append({'a':float(np.exp(x)),'state':y.tolist(),'F':z['F'],'B':z['B'],'H':z['H'],'R_over_H2':z['R']/z['H']**2,'ordinary_radiation_over_dust':z['rho_r']/z['rho_d'],'ordinary_fraction_of_3MH2':(z['rho_d']+z['rho_r'])/(3*z['H']**2),'rho_carrier':z['rho_carrier'],'p_carrier':z['p_carrier'],'rho_carrier_raw':z['rho_carrier_raw'],'p_carrier_raw':z['p_carrier_raw'],'carrier_fraction_of_3MH2':z['rho_carrier']/(3*z['H']**2),'Q_relative_error':qerr,'friedmann_relative_error':cg,'geometric_R_relative_error':re})
  recovered=solve_ivp(fun,(endpoint,0),sol.y[:,-1],method=method,rtol=tol,atol=tol*1e-5)
  physical_scales=np.array([np.linalg.norm(y0[:2])]*2+[np.linalg.norm(y0[2:4])]*2+[1.])
  recovery=float(np.max(np.abs(recovered.y[:,-1]-y0)/physical_scales))
  status='target_reached' if endpoint<=target+1e-8 else ('F_positive_floor' if len(sol.t_events[0]) else 'numerical_stop')
  record={'xi':xi,'S_initial_over_M':.4,'method':method,'rtol':tol,'status':status,'endpoint_x':endpoint,'nfev':sol.nfev,'success':sol.success,'message':sol.message,'samples':vals,'max_charge_relative_error':maxQ,'max_friedmann_relative_error':maxCg,'max_geometric_R_scaled_error':maxR,'forward_success':recovered.success,'forward_recovery_error':recovery};runs.append(record);solutions.append((endpoint,sol.y[:,-1]))
  ck('backward_solver_'+str(xi)+method+str(tol),sol.success,sol.message)
  ck('charge_'+str(xi)+method+str(tol),maxQ<2e-5,maxQ)
  ck('friedmann_'+str(xi)+method+str(tol),maxCg<1e-10,maxCg)
  ck('geometry_'+str(xi)+method+str(tol),maxR<1e-8,maxR)
  ck('valid_positive_branch_'+str(xi)+method+str(tol),min(z['F'] for z in vals)>=floor*.99 and min(z['B'] for z in vals)>0,min(z['F'] for z in vals))
  ck('forward_recovery_'+str(xi)+method+str(tol),recovered.success and recovery<2e-4,recovery)
 epdiff=max(abs(solutions[0][0]-solutions[1][0]),abs(solutions[2][0]-solutions[1][0]));ck('independent_endpoint_'+str(xi),epdiff<2e-5,epdiff)
 endscale=np.array([np.linalg.norm(solutions[1][1][:2])]*2+[np.linalg.norm(solutions[1][1][2:4])]*2+[1.]);enderr=max(float(np.max(np.abs(solutions[j][1]-solutions[1][1])/endscale)) for j in [0,2]);ck('independent_endpoint_state_'+str(xi),enderr<2e-5,enderr)
args.out.mkdir(parents=True,exist_ok=True);out={'runs':runs,'checks':checks,'passed':sum(z['passed'] for z in checks),'total':len(checks),'mutation':args.mutation,'scope':'homogeneouscoupledscalar+dust+radiation; Ffloorstopnotphysicalcontinuation; no perturbativehealth,coldabundance,CMBor32piselector'};(args.out/'results.json').write_text(json.dumps(out,indent=2));print(json.dumps({'passed':out['passed'],'total':out['total'],'failed':[z['name'] for z in checks if not z['passed']],'summary':[{k:r[k] for k in ['xi','method','rtol','status','endpoint_x','nfev','max_charge_relative_error','max_geometric_R_scaled_error','forward_recovery_error']} for r in runs]}));sys.exit(0 if out['passed']==out['total'] else 1)
