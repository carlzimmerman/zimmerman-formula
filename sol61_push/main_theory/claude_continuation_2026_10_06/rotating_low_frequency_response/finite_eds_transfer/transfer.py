import argparse,json,sys
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from equations import rhs,quantities,constrained_initial
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--mutation',choices=['omit_constraint_initialization']);args=p.parse_args();runs=[];checks=[]
def ck(name,val,detail):checks.append({'name':name,'passed':bool(val),'detail':detail})
for xi in [100.,1000.]:
 S0=.4;A=S0/(8*xi**2);F0=1-2*xi*A;Z0=1+3*S0/(2*F0);Omega0=np.sqrt(4*xi/3-.25);H0=2/3
 k=np.sqrt(H0**2+2*H0*Omega0/np.sqrt(Z0)) # initial local slowpole equalsH, NOT an asserted true evolving eigenmode.
 y0=constrained_initial(xi,A,k)
 if args.mutation:y0[-1]=0.
 grid=np.log(np.array([1.,2.,10.,100.]));methods=[('DOP853',1e-9),('DOP853',3e-10),('Radau',1e-9)];solutions=[]
 for method,tol in methods:
  sol=solve_ivp(lambda x,y:rhs(x,y,xi,A,k),(0.,grid[-1]),y0,method=method,rtol=tol,atol=tol/100,t_eval=grid)
  ck('solver_success_'+str(xi)+'_'+method+'_'+str(tol),sol.success,sol.message)
  vals=[]
  for x,y in zip(sol.t,sol.y.T):
   q=quantities(x,y,xi,A,k);phiGR=-2/(3*k*k+4);deltaGR=-(1.5*q['P']+2)*phiGR;comGR=-1.5*q['P']*phiGR
   vals.append({'t':float(np.exp(x)),'state':y.tolist(),'Phi':float(y[-1]),'Psi':q['Psi'],'Weyl_ratio_to_GR':q['Weyl']/phiGR,'comoving_density_ratio_to_GR':q['density_comoving']/comGR,'rest_density_ratio_to_GR':y[4]/deltaGR,'Weyl_ratio_to_GR_same_actual_dust':q['Weyl']/(-2*q['density_comoving']/(3*q['P'])),'Weyl_non_dust_fraction_relative_actual_dust':q['Weyl']/(-2*q['density_comoving']/(3*q['P']))-1,'C00':q['C00'],'F':q['F'],'B':q['B'],'p_over_Omega':np.sqrt(q['P'])/Omega0,'local_sigma_slow_over_H':(np.sqrt(q['P']+Omega0**2/(1+12*xi*xi*A*np.exp(-x)/q['F']))-Omega0/np.sqrt(1+12*xi*xi*A*np.exp(-x)/q['F']))/H0})
  solutions.append(sol.y);runs.append({'xi':xi,'A':A,'S0':S0,'k':k,'method':method,'rtol':tol,'nfev':sol.nfev,'samples':vals})
  ck('constraint_residual_'+str(xi)+'_'+method+'_'+str(tol),max(abs(z['C00']) for z in vals)<2e-5, max(abs(z['C00']) for z in vals))
  ck('positive_F_B_'+str(xi)+'_'+method+'_'+str(tol),min(z['F'] for z in vals)>0 and min(z['B'] for z in vals)>0,min(z['F'] for z in vals))
 scale=1+np.abs(solutions[1]);err=max(float(np.max(np.abs(solutions[0]-solutions[1])/scale)),float(np.max(np.abs(solutions[2]-solutions[1])/scale)))
 ck('independent_method_transfer_'+str(xi),err<2e-6,err)
 ck('initial_full_constraint_'+str(xi),abs(quantities(0,y0,xi,A,k)['C00'])<1e-10,quantities(0,y0,xi,A,k)['C00'])
args.out.mkdir(parents=True,exist_ok=True);res={'runs':runs,'checks':checks,'passed':sum(z['passed'] for z in checks),'total':len(checks),'scope':'finite EdS linear transfer; infinitesimal initialdensity; no nonlinear halo, spectral classification or cosmologicalfit'};(args.out/'results.json').write_text(json.dumps(res,indent=2));print(json.dumps({'passed':res['passed'],'total':res['total'],'failed':[z['name'] for z in checks if not z['passed']],'end_samples':[r['samples'][-1] for r in runs if r['method']=='Radau']}));sys.exit(0 if res['passed']==res['total'] else 1)
