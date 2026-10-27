import argparse,json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
p=argparse.ArgumentParser();p.add_argument('--output');args=p.parse_args()
fb=1/6.364;fc=1-fb;ell=.0004404221297174536;t0=.012074272908402984;H0=67.4*1000/3.085677581491367e22*365.25*86400*1e9;Om=.315;N0=-np.log(1101);end=-np.log(11)
base=json.loads(Path('sol61_push/early_precursors_2026_10_23/run/result.json').read_text());rows=[]
for M in sorted(set(x['M'] for x in base['rows'])):
 k=next(x['k'] for x in base['rows'] if x['M']==M)
 def rhs(N,y):
  b,bp,c,cp,X,Xp,Y,Yp=y;A=np.exp(N);q=k*ell/A;H=H0*np.sqrt(Om)*A**(-1.5)*t0;Jc=1.5*fc*H*H;h=Jc*c/(1+q*q);source=h*h/4
  return [bp,-.5*bp+1.5*(fb*b+fc*c),cp,-.5*cp+1.5*(fb*b+fc*c/(1+q*q)),Xp,-1.5*Xp-(.005*X-source)/(.125*H*H),Yp,-1.5*Yp-((.005+.125*4*q*q)*Y-source)/(.125*H*H)]
 grid=np.linspace(N0,end,3001);outs=[]
 for tol in [1e-9,1e-11]:
  s=solve_ivp(rhs,(N0,end),[1,1,1,1,0,0,0,0],method='DOP853',rtol=tol,atol=tol*1e-3,t_eval=grid);assert s.success
  response=np.abs(s.y[4])+np.abs(s.y[6]);imax=int(np.argmax(response));outs.append((s,response,imax))
 s,response,imax=outs[-1];maximum=float(response[imax]);densitymax=np.maximum(s.y[0],s.y[2]);dphase=np.sqrt(.1/np.maximum(response,1e-300));ddensity=1/densitymax
 # Phase .1 reached while density stays below1 along this monotone growth history iff dphase<ddensity at some time.
 ratio=dphase/ddensity;idx=int(np.argmin(ratio))
 A=np.exp(grid);q=k*ell/A;HH=H0*np.sqrt(Om)*A**(-1.5)*t0;Pcoef=q*(1.5*fc*HH*HH)*s.y[2]/(1+q*q);Pmax=np.maximum.accumulate(abs(Pcoef));validity=np.maximum(densitymax,10*Pmax)*dphase;iv=int(np.argmin(validity))
 rows.append(dict(P_max_for_delta001=float(.01*max(Pmax)),P_max_for_delta0001=float(.001*max(Pmax)),min_combined_validity_at_phase01=float(validity[iv]),P_at_best_phase_ratio=float(Pmax[idx]*dphase[idx]),initial_delta_at_best_phase_ratio=float(dphase[idx]),M=M,k=k,phase_coefficient_max=maximum,z_phase_max=float(np.exp(-grid[imax])-1),delta_i_for_phase01=float(np.sqrt(.1/maximum)),min_phase_to_density_threshold=float(ratio[idx]),z_min_ratio=float(np.exp(-grid[idx])-1),density_at_phase01=float(ratio[idx]),relative_repeat=float(np.max(abs(response-outs[0][1]))/max(maximum,1e-30))))
checks=[dict(name='phase_tolerance_repeat',passed=max(x['relative_repeat'] for x in rows)<1e-6,value=max(x['relative_repeat'] for x in rows))]
Path(args.output).write_text(json.dumps(dict(checks=checks,rows=rows),indent=2)+'\n')
