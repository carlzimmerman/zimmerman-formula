"""Actual signed work/action moments on the newly evolved changing-fS stage."""
import sys,os
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[k]='1'
import json,time,math,resource
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp,cumulative_trapezoid
from response_api_v4 import *

def work_kernel(xmid,amplitude,omega,Tc,edges,radial=2,angular=12):
    d=cell_modes(xmid,amplitude,omega,Tc,edges,radial,angular)
    delta,z,b,pref=(d[x] for x in ('delta','z','boost','pref'))
    nm=int(math.ceil(float(max(z))+12+4*float(max(z))**(1/3)))
    rate=np.zeros(len(delta));power=rate.copy();absolute=rate.copy();residual=rate.copy()
    for n in range(-nm,nm+1):
        ds=delta+n*omega
        rn=pref*jv(n,z)**2*b*np.sum(abs(COEFF)[None,:]**2*WIDTH[None,:]/((WIDTH[None,:]*b[:,None]/2)**2+ds[:,None]**2),axis=1)
        rate+=rn;power+=n*omega*rn;absolute+=abs(n*omega)*rn;residual+=ds*rn
    return dict(K=_bin(rate,d),power=_bin(power,d),absolute=_bin(absolute,d),residual=_bin(residual,d),
                incoming_mean_energy=_bin(d['Echarged']*rate,d))

def main(out):
    start=time.monotonic();here=Path(__file__).resolve().parent
    kernels=json.loads((here/'run_stage001/kernels.json').read_text());stage=json.loads((here/'run_stage001/result.json').read_text())
    late=json.loads((PRIOR/'kinetics/run_hybrid_bw_001/result.json').read_text())['case']
    packet=json.loads((PRIOR/'gravity_resonance/run_leading001/result.json').read_text())['packet']
    Ns=np.asarray(kernels['N']);Ks=np.asarray(kernels['K']);edges=np.asarray(kernels['q_edges']);W=(edges[1:]**3-edges[:-1]**3)/3;f0=np.asarray(stage['initial_fS'])
    omega=math.sqrt(float(packet['local_profile']['radial_curvature_mu2'])/62);N0=Ns[0];H0=late['history'][0]['H_over_oscillation']*omega
    def thermal(N):return late['history'][0]['Tc_over_mu']*math.exp(-(N-N0)),H0*math.exp(-2*(N-N0))
    def rhs(N,y):
        i=int(np.clip(np.searchsorted(Ns,N)-1,0,len(Ns)-2));a=(N-Ns[i])/(Ns[i+1]-Ns[i]);K=(1-a)*Ks[i]+a*Ks[i+1]
        Tc,H=thermal(N);return -K@(12*Tc**3/(2*math.pi**2)*W*np.exp(y))/H
    sol=solve_ivp(rhs,[Ns[0],Ns[-1]],np.log(f0),t_eval=Ns,rtol=3e-8,atol=2e-9,max_step=.005);fg=np.exp(sol.y.T)
    rows=[];powers=[];absolutes=[];residuals=[];projections=[]
    for i,h in enumerate(late['history']):
        Tc,H=thermal(Ns[i]);args=dict(xmid=h['x_minimum'],amplitude=(h['x_outer']-h['x_inner'])/2,omega=omega,Tc=Tc,edges=edges)
        k=work_kernel(**args);n=12*Tc**3/(2*math.pi**2)*W*fg[i];pair=n[:,None]*n[None,:]
        P=float(np.sum(pair*k['power']));B=float(np.sum(pair*k['absolute']));R=float(np.sum(pair*k['residual']))
        rz,rw=leggauss(2);q=(edges[:-1,None]+edges[1:,None])/2+(edges[1:,None]-edges[:-1,None])*rz/2
        qw=q*q*(edges[1:,None]-edges[:-1,None])*rw/2/W[:,None]
        Ecell=np.sum(qw*np.sqrt(float(charged_mass(h['x_minimum']))**2+(Tc*q)**2),axis=1)
        projected=float(np.sum(pair*k['K']*(Ecell[:,None]+Ecell[None,:])))
        physical=float(np.sum(pair*k['incoming_mean_energy']));projection=projected-physical
        scale=H*h['action']*omega;powers.append(P/(omega*H));absolutes.append(B/(omega*H));residuals.append(R/(omega*H));projections.append(projection/(omega*H))
        row=dict(N=float(Ns[i]),Tc=Tc,scalar_power_mu5=P,absolute_scalar_power_bound_mu5=B,
                 finite_width_energy_residual_mu5=R,cell_projection_energy_residual_mu5=projection,
                 dlogJ_collision=P/scale,absolute_dlogJ_bound=B/scale,
                 finite_width_residual_over_field_energy_per_N=R/scale,
                 cell_projection_residual_over_field_energy_per_N=projection/scale,
                 K_reconstruction_relative=float(np.max(abs(k['K']-Ks[i]))/np.max(Ks[i])))
        if i in (0,40,79):
            full=band_kernel(**args,radial=2,angular=12)
            row['full_matrix_power_relative']=float(np.max(abs(k['power']-full['scalar_field_power_pair']))/max(np.max(abs(k['power'])),1e-300))
        rows.append(row)
    exp3=np.exp(3*(Ns-N0));J0=late['history'][0]['action'];Jbase=J0/exp3
    Jnew=(J0+cumulative_trapezoid(exp3*np.asarray(powers),Ns,initial=0))/exp3
    Jbound=cumulative_trapezoid(exp3*np.asarray(absolutes),Ns,initial=0)/exp3
    Rbound=cumulative_trapezoid(exp3*abs(np.asarray(residuals)),Ns,initial=0)/exp3
    Projbound=cumulative_trapezoid(exp3*abs(np.asarray(projections)),Ns,initial=0)/exp3
    checks=dict(changing_shape_reconstruction=float(np.max(abs(fg[-1]/np.asarray(stage['final_fS'])-1)))<1e-9,
                K_reconstruction=max(x['K_reconstruction_relative'] for x in rows)<1e-12,
                full_matrix_moment=max(x.get('full_matrix_power_relative',0) for x in rows)<1e-10,
                action_positive=bool(np.all(Jnew>0)),passive_work_bound=all(abs(x['dlogJ_collision'])<=x['absolute_dlogJ_bound']*(1+1e-12) for x in rows))
    result=dict(claim_id='CC10_CHANGING_SHAPE_SIGNED_MEMORY_ACTION',checks=checks,rows=rows,
        action_on_prescribed_orbit=Jnew.tolist(),maximum_relative_action_correction=float(np.max(abs(Jnew/Jbase-1))),
        maximum_absolute_action_bound=float(np.max(Jbound/Jbase)),
        maximum_finite_width_residual_action_bound=float(np.max(Rbound/Jbase)),
        maximum_cell_projection_residual_action_bound=float(np.max(Projbound/Jbase)),
        maximum_absolute_dlogJ_bound=max(x['absolute_dlogJ_bound'] for x in rows),
        scope='Signed scalar work from actual sideband currents on newly evolving fS stage, including separate finite-width on-shell exit energy residual and finite-cell projection energy residual. Action response evaluated on recorded orbit as controlled first correction; root must close common field/cascade ledger and match finite-width daughter energies.',
        runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    Path(out).write_text(json.dumps(serialize(result),indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('rows','action_on_prescribed_orbit')}));assert all(checks.values()),checks

if __name__=='__main__':main(sys.argv[1])
