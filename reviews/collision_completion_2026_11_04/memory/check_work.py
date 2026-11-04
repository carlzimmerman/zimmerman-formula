"""Independent ODE test of signed scalar Floquet work and phase source energy."""
import sys,os
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[k]='1'
import json,time,math,resource
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from response_api_v4 import *

def main(out):
    start=time.monotonic();late=json.loads((PRIOR/'kinetics/run_hybrid_bw_001/result.json').read_text())['case']
    packet=json.loads((PRIOR/'gravity_resonance/run_leading001/result.json').read_text())['packet'];omega=math.sqrt(float(packet['local_profile']['radial_curvature_mu2'])/62)
    rows=[]
    for idx in (0,40,79):
        h=late['history'][idx];xmid=h['x_minimum'];amp=(h['x_outer']-h['x_inner'])/2;Tc=h['Tc_over_mu']
        m=float(charged_mass(xmid));dm=charged_mass_derivative(xmid);p1=Tc*2.517216215372447;p2=Tc*3.321558463429335;c=.3
        e1=math.sqrt(m*m+p1*p1);e2=math.sqrt(m*m+p2*p2);ep=math.sqrt(M*M+p1*p1+p2*p2+2*p1*p2*c);boost=M/ep
        delta=((M-2*m)*(M+2*m)+p1*p1+p2*p2+2*p1*p2*c)/(ep+2*m)-p1*p1/(e1+m)-p2*p2/(e2+m)
        aa=amp*m*dm*(1/e1+1/e2);z=aa/omega;nm=int(math.ceil(z+12+4*z**(1/3)));ns=np.arange(-nm,nm+1)
        r=jv(ns,z)[:,None]*COEFF/(WIDTH[None,:]*boost/2+1j*(delta+ns*omega)[:,None])
        rn=np.sum(abs(r)**2*WIDTH[None,:]*boost,axis=1);rate=float(rn.sum());power=float(ns@(omega*rn));residual=float((delta+ns*omega)@rn)
        def rhs(th,y):return -(WIDTH*boost/(2*omega)+1j*(delta/omega-z*math.cos(th)))*y+COEFF
        ts=np.linspace(0,84*math.pi,21505);sol=solve_ivp(rhs,[0,84*math.pi],np.zeros(4,complex),t_eval=ts,rtol=1e-10,atol=2e-12,max_step=.015)
        cut=ts>=80*math.pi;theta=ts[cut];a=sol.y[:,cut]/omega
        current=2*np.einsum('a,at->t',COEFF,a.real);hazard=np.sum(abs(a)**2*WIDTH[:,None]*boost,axis=0)
        mean=lambda v:float(np.trapz(v,theta)/(4*math.pi))
        measuredpower=-aa*mean(np.cos(theta)*current);measuredrate=mean(hazard);Jmean=mean(current)
        phase_removed=mean((ep-delta+aa*np.cos(theta))*current)
        energy_residual=ep*measuredrate-phase_removed
        rows.append(dict(Tc=Tc,Floquet_rate=rate,ODE_rate=measuredrate,
             Floquet_scalar_power=power,ODE_scalar_power=measuredpower,
             scalar_work_relative=abs(measuredpower-power)/max(abs(power),aa*rate*1e-5),
             mean_source_equals_exit_relative=abs(Jmean/measuredrate-1),
             finite_width_ledger_residual=residual,ODE_energy_residual=energy_residual,
             energy_residual_error_relative_to_detuning_bound=abs(energy_residual-residual)/(aa*rate),
             absolute_sideband_power=float(abs(ns*omega)@rn),ODE_success=bool(sol.success)))
    checks=dict(ODE_success=all(x['ODE_success'] for x in rows),signed_scalar_work=all(x['scalar_work_relative']<.002 for x in rows),
                source_exit=all(x['mean_source_equals_exit_relative']<1e-5 for x in rows),
                finite_width_ledger=all(x['energy_residual_error_relative_to_detuning_bound']<.02 for x in rows))
    result=dict(claim_id='CC10_SIGNED_FLOQUET_SCALAR_WORK',checks=checks,rows=rows,
        derivation='J=2Re(v†a); <J>=<a†Γa>. For δ=δ0−Acosθ, Bessel recurrence gives A<cosθ J>=−sum nω r_n. Scalar power is negative particle background work, hence sum nω r_n. EN exit minus phase-weighted charged source energy equals sum(δ0+nω)r_n; this finite-width Markov-decay residual requires matching, not silent radiation.',
        runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    Path(out).write_text(json.dumps(serialize(result),indent=2)+'\n');print(json.dumps(serialize(result)));assert all(checks.values()),checks

if __name__=='__main__':main(sys.argv[1])
