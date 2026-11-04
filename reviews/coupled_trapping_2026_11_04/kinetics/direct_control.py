"""Four resolved initial orbits versus the averaged f/action sink calculation."""
import sys,os
sys.dont_write_bytecode=True
import json,time,math,resource
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from averaged_v2 import Model,evolve,ROOT,HERE,PREF,MASS

def main(out):
 start=time.monotonic();stat=json.loads((ROOT/'reviews/gravity_completion_2026_11_03/thermal_kinetic/run_stationary_002/result.json').read_text());spins=json.loads((ROOT/'reviews/gravity_completion_2026_11_03/thermal/run_static_001/result.json').read_text());p=stat['points'][0];s=next(z for z in spins['points'] if z['kind']==p['kind'])['spins'][0];model=Model(p,s,bins=24,orbitn=24);yavg=model.setup();f0=model.f0;orb=model.orbital(0,f0,J=model.J0);period=orb['period'];H0=model.H(0);scale=model.scale;n=len(f0)
 def deriv(u,y):
  x,vel,N=y[:3];f=np.exp(np.clip(y[3:3+n],-700,0));t=model.t0*math.exp(-N);H=model.H(N);m=float(model.mass(x));dm=float(model.mass(x,1));en=np.sqrt(m*m+(t*model.q)**2);rho=PREF*t**3*float((model.W*f)@en);pr=PREF*t**3/3*float((model.W*f)@((t*model.q)**2/en));force=PREF*t**3*float((model.W*f)@(m*dm/en));c=model.collision(x,t,f);q=-PREF*t**3*float(model.W@(en*c));rad=y[-2]*scale;return np.r_[vel,-3*H*period*vel-period**2*(float(model.v(x,1))+force)/MASS,H*period,period*c/np.maximum(f,1e-300),period*(q-4*H*rad)/scale,3*H*period*(MASS*(vel/period)**2+rho+pr+4*rad/3)/scale]
 rows=[]
 for tol in (2e-7,5e-8):
  y0=np.r_[model.x0,0.,0.,np.log(f0),0.,0.];sol=solve_ivp(deriv,[0,4],y0,rtol=tol,atol=tol*1e-4,max_step=.02);y=sol.y[:,-1];f=np.exp(y[3:3+n]);x=y[0];N=y[2];t=model.t0*math.exp(-N);E=MASS/2*(y[1]/period)**2+float(model.potential(x,t,f)[0]);ledger=(E+(y[-2]+y[-1])*scale-model.E0)/scale;avg=evolve(model,True,N,1e-7);fa=np.array(avg['final_f']);weights=model.W*f0
  rows.append(dict(rtol=tol,success=bool(sol.success),nfev=sol.nfev,N=float(N),period_mu_inverse=period,initial_H_over_oscillation=H0*period/(2*math.pi),survival_direct=float(model.W@f/(model.W@f0)),survival_averaged=avg['history'][-1]['survival'],weighted_absolute_occupation_disagreement=float(model.W@abs(f-fa)/(model.W@f0)),max_initial_number_relevant_fractional_disagreement=float(max(abs((f-fa)/f0)[weights>max(weights)*1e-4])),energy_ledger_error=float(ledger),final_x=float(x)))
 result=dict(claim_id='CT09_DIRECT_AVERAGING_CONTROL',cases=rows,checks={'resolved_integrations':all(q['success'] for q in rows),'direct_energy_ledger':max(abs(q['energy_ledger_error']) for q in rows)<1e-6,'direct_averaged_initial_number_agreement':max(q['weighted_absolute_occupation_disagreement'] for q in rows)<.001,'tolerance_repeat':abs(rows[0]['survival_direct']-rows[1]['survival_direct'])<1e-5},runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Only four initial resolved orbits,24 bulk bins, scalar-parent absorbing limit. Verifies early averaging and energy exchange, not all subsequent orbits or actual daughter network.')
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));assert all(result['checks'].values())
if __name__=='__main__':main(sys.argv[1])
